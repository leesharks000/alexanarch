#!/usr/bin/env python3
"""build_resourcesync.py — autodiscovery for a repository nobody registered.

WHY
---
OpenArchives discontinued registration of OAI-PMH data providers on 2025-07-18.
The protocol is unaffected; the central directory is closed. A repository can no
longer be listed by asking. It can only be *found*.

So this archive publishes the standard discovery surfaces and lets harvesters
find it the way harvesters now actually work:

  /.well-known/resourcesync          Source Description (ResourceSync entry point)
  /resourcesync/capabilitylist.xml   what this source offers
  /resourcesync/resourcelist.xml     every record, with lastmod
  /resourcesync/changelist.xml       what changed, for incremental sync
  <link rel="resourcesync">          HTML autodiscovery
  <link rel="alternate" …oai>        OAI-PMH autodiscovery
  robots.txt                         both endpoints announced

ResourceSync (ANSI/NISO Z39.99-2017) is the successor standard to OAI-PMH and is
sitemap-shaped, which means crawlers that ignore OAI entirely can still walk it.
Publishing both costs one build step and doubles the number of harvester species
that can reach the corpus.

The changelist is the one that matters for a living archive: it is generated from
date_modified (scripts/record_modification.py), so a record repaired today is
re-offered to harvesters today, and a record untouched since deposit is not.
"""
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.alexanarch.org"
RS = ROOT / "resourcesync"
WK = ROOT / ".well-known"
NS = ('xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
      'xmlns:rs="http://www.openarchives.org/rs/terms/"')


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def doc(md_capability, urls, up=None, extra_md=""):
    ln = f'  <rs:ln rel="up" href="{up}"/>\n' if up else ""
    body = "".join(urls)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset {NS}>\n{ln}'
            f'  <rs:md capability="{md_capability}"{extra_md}/>\n{body}</urlset>\n')


def main():
    idx = json.loads((ROOT / "data" / "oai-index.json").read_text())
    recs = idx["records"]
    RS.mkdir(exist_ok=True)
    WK.mkdir(exist_ok=True)
    t = now()

    # Source Description — the entry point a harvester probes first
    (WK / "resourcesync").write_text(doc(
        "description",
        [f'  <url>\n    <loc>{BASE}/resourcesync/capabilitylist.xml</loc>\n'
         f'    <rs:md capability="capabilitylist"/>\n  </url>\n'],
    ))

    # Capability List
    caps = "".join(
        f'  <url>\n    <loc>{BASE}/resourcesync/{n}.xml</loc>\n'
        f'    <rs:md capability="{c}"/>\n  </url>\n'
        for n, c in [("resourcelist", "resourcelist"), ("changelist", "changelist")])
    caps += (f'  <url>\n    <loc>{BASE}/oai?verb=Identify</loc>\n'
             f'    <rs:ln rel="describedby" href="{BASE}/oai?verb=Identify"/>\n'
             f'    <rs:md capability="resourcelist" type="application/xml"/>\n  </url>\n')
    (RS / "capabilitylist.xml").write_text(
        doc("capabilitylist", [caps], up=f"{BASE}/.well-known/resourcesync"))

    # Resource List — the whole corpus
    urls = [
        f'  <url>\n    <loc>{BASE}/s/records/{r["id"]}/</loc>\n'
        f'    <lastmod>{r["datestamp"]}</lastmod>\n'
        f'    <rs:md hash="" length="" type="text/html"/>\n  </url>\n'
        for r in recs]
    (RS / "resourcelist.xml").write_text(doc(
        "resourcelist", urls, up=f"{BASE}/resourcesync/capabilitylist.xml",
        extra_md=f' at="{t}" completed="{t}"'))

    # Change List — only what moved, newest first
    stamped = sorted((r for r in recs if r.get("datestamp")),
                     key=lambda r: r["datestamp"], reverse=True)[:500]
    ch = [
        f'  <url>\n    <loc>{BASE}/s/records/{r["id"]}/</loc>\n'
        f'    <lastmod>{r["datestamp"]}</lastmod>\n'
        f'    <rs:md change="updated" datetime="{r["datestamp"]}T00:00:00Z"/>\n  </url>\n'
        for r in stamped]
    (RS / "changelist.xml").write_text(doc(
        "changelist", ch, up=f"{BASE}/resourcesync/capabilitylist.xml",
        extra_md=f' from="{stamped[-1]["datestamp"]}T00:00:00Z"' if stamped else ""))

    # robots.txt — announce both endpoints.
    # ROOT-CAUSE FIX (2026-08-04 decisions row, RECURRING truncation class):
    # in sparse checkouts robots.txt is absent from the working tree, and this
    # writer used to FABRICATE a minimal stub in its place — losing the
    # agent-guidance block and Sitemap lines on every propagation run (step 7).
    # Rule now: read-modify-write against HEAD content when the checkout copy is
    # absent or truncated; never fabricate; skip when no canonical source exists.
    # A truncated working copy is restored from HEAD (self-healing), never
    # accepted as a base.
    rp = ROOT / "robots.txt"
    MARKER = "# AI agents:"  # sentinel for the canonical agent-guidance block
    txt = rp.read_text() if rp.exists() else ""
    if MARKER not in txt:
        head = subprocess.run(
            ["git", "-C", str(ROOT), "show", "HEAD:robots.txt"],
            capture_output=True, text=True)
        if head.returncode == 0 and MARKER in head.stdout:
            txt = head.stdout  # recover canonical bytes; restore on write below
        elif not txt:
            txt = None  # nothing in checkout, nothing in HEAD: do not invent
            print("resourcesync: robots.txt absent from checkout and HEAD — "
                  "SKIPPED robots write (no fabrication)")
    if txt is not None:
        add = []
        if "resourcesync" not in txt:
            add.append(f"# ResourceSync (ANSI/NISO Z39.99) source description")
            add.append(f"Sitemap: {BASE}/resourcesync/resourcelist.xml")
        if "/oai" not in txt:
            add.append(f"# OAI-PMH 2.0 base URL: {BASE}/oai")
        new = txt.rstrip() + "\n\n" + "\n".join(add) + "\n" if add else txt
        current = rp.read_text() if rp.exists() else ""
        if new != current:
            rp.write_text(new)
            print("resourcesync: robots.txt "
                  + ("restored from HEAD" if MARKER in new and MARKER not in current
                     else "updated"))

    print(f"resourcesync: {len(recs)} resources, {len(ch)} changes, "
          f"source description at /.well-known/resourcesync")


if __name__ == "__main__":
    main()
