#!/usr/bin/env python3
"""audit_orphan_captures.py — evidence that exists and was never recorded.

THE HOLE THIS CLOSES
On 2026-08-07 the capture registry got a citation grammar, binding slug rules, an
adding-a-capture sequence in atlas §7.3, and three pipeline gates. All of it
landed. **None of it could catch what MANUS found the next day.**

Every one of those checks iterates FROM THE REGISTRY:

    audit_capture_citability   for each entry, is it citable?
    build_capture_links        for each entry, does it carry its links?
    build_capture_gallery      for each entry, render a card

So the apparatus asks, exhaustively, *is every record complete?* It never asks
*is every capture recorded?* A screenshot taken, uploaded to a gallery, and never
written into the registry is invisible to all of it — not because a check failed
but because no check was pointed that way.

MANUS reported a capture he had posted publicly and could not find in the
registry. The scan said no such capture; I reported that the capture did not
exist. It did. **Reporting the absence of a record as the absence of the thing is
the same error the archive exists to document**, committed by its own audit.

A whole session from 2026-08-03/04 — symbolon reception, stamp reception, the
constitution, the OAI surface — sits on the image hosts and in no registry.

WHAT THIS DOES
Iterates the IMAGE HOSTS and reports every image no entry references, split into:
  · MATCHABLE  — an entry exists whose slug matches; the link is simply missing
  · UNRECORDED — no entry exists at all; the capture was never written down

Usage:
    python3 scripts/audit_orphan_captures.py            # report
    python3 scripts/audit_orphan_captures.py --link     # attach matchable images
    python3 scripts/audit_orphan_captures.py --stubs    # emit a stub sheet
"""
import json, os, re, sys, pathlib, argparse, urllib.request, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
HOSTS = {
    "godkinggoogle": "https://godkinggoogle.vercel.app/captures/",
    "leesharks.com": "https://leesharks.com/captures/",
}


def token():
    try:
        u = subprocess.run(["git", "remote", "get-url", "origin"],
                           capture_output=True, text=True, cwd=ROOT).stdout
        return u.split("x-access-token:")[1].split("@")[0]
    except Exception:
        return os.environ.get("GITHUB_TOKEN", "")


def host_images(pat):
    out = {}
    for repo in HOSTS:
        try:
            req = urllib.request.Request(
                f"https://api.github.com/repos/leesharks000/{repo}/contents/captures?per_page=400",
                headers={"Authorization": f"Bearer {pat}"} if pat else {})
            for f in json.load(urllib.request.urlopen(req, timeout=45)):
                if f["name"].lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                    out.setdefault(f["name"], []).append(repo)
        except Exception as e:
            print(f"  (could not list {repo}: {e})", file=sys.stderr)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--link", action="store_true", help="attach matchable images to their entries")
    ap.add_argument("--stubs", action="store_true", help="emit a stub sheet for unrecorded captures")
    a = ap.parse_args()

    reg = json.loads(REG.read_text())
    entries = reg["entries"]
    by_slug = {e["slug"]: e for e in entries if e.get("slug")}
    renamed = {h["was"]: e["slug"] for e in entries for h in (e.get("slug_history") or [])}
    referenced = {os.path.basename(u.split("?")[0])
                  for e in entries
                  for u in (e.get("imgs") or []) + (e.get("imgs_origin") or [])
                  if isinstance(u, str)}

    imgs = host_images(token())
    orphans = {n: r for n, r in imgs.items() if n not in referenced}

    matchable, unrecorded = [], []
    for name, repos in sorted(orphans.items()):
        stem = re.sub(r"-\d+$", "", name.rsplit(".", 1)[0])
        tgt = None
        if stem in by_slug:
            tgt = stem
        elif stem in renamed:
            tgt = renamed[stem]
        else:
            cand = [s for s in by_slug if s.startswith(stem + "-20")]
            if len(cand) == 1:
                tgt = cand[0]
        (matchable if tgt else unrecorded).append((name, tgt, repos))

    print(f"images on hosts: {len(imgs)} · referenced by the registry: "
          f"{len(referenced & set(imgs))} · orphaned: {len(orphans)}")
    print(f"  MATCHABLE  (entry exists, link missing): {len(matchable)}")
    print(f"  UNRECORDED (no entry at all):            {len(unrecorded)}")

    if a.link and matchable:
        n = 0
        for name, tgt, repos in matchable:
            e = by_slug[tgt]
            url = HOSTS[repos[0]] + name
            e.setdefault("imgs", [])
            if url not in (e.get("imgs_origin") or []):
                e.setdefault("imgs_origin", []).append(url)
            if not any(name in str(x) for x in e["imgs"]):
                e["imgs"].append(url)
                n += 1
        REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1))
        print(f"\nlinked {n} image(s) to existing entries")

    if a.stubs and unrecorded:
        print("\n" + "=" * 74)
        print("UNRECORDED CAPTURES — stub sheet")
        print("Evidence exists on a host and no entry was ever written. The images are")
        print("dated and named, so the subject is recoverable; the READING is not — what")
        print("the layer said and what it means has to come from whoever ran the query.")
        print("=" * 74)
        groups = {}
        for name, _, repos in unrecorded:
            m = re.match(r"(\d{8})-(.+?)(?:-\d+)?\.\w+$", name)
            key = (m.group(1), m.group(2)) if m else ("undated", name.rsplit(".", 1)[0])
            groups.setdefault(key, []).append((name, repos))
        for (date, subject), files in sorted(groups.items()):
            d = f"{date[:4]}-{date[4:6]}-{date[6:]}" if date != "undated" else "?"
            slug = re.sub(r"[^a-z0-9-]", "-", subject.lower()).strip("-")
            slug = f"{slug}-{date}" if date != "undated" else slug
            print(f"\n  slug : {slug}")
            print(f"  date : {d}")
            print(f"  q    : ?  ← the query run")
            print(f"  mt   : ?  ← what the layer did")
            print(f"  d    : ?  ← the reading")
            for f, repos in files:
                print(f"  img  : {HOSTS[repos[0]]}{f}")
    return 1 if unrecorded else 0


if __name__ == "__main__":
    sys.exit(main())
