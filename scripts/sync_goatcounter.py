#!/usr/bin/env python3
"""sync_goatcounter.py — the GoatCounter tag on every page of alexanarch, once.

WHY THIS EXISTS
---------------
The tag (alexanarch.goatcounter.com, the counter data/goatcounter-sites.json polls for data/view-counts.json) was
written only by the record, wiki, AXN, DOI and browse generators: 8,824 of 15,687 pages on 2026-11-23. The
captures and their address pages, the datasets, the rooms, /non and the hub pages (/ask/, /search/, /how/,
/journals/ and the rest) had none. Lee, 2026-11-23 20:36: "lets add the counter to alexanarch pages", and "add it
to new capture and /non pages and such at intake as a step".

Built on sync_sigil.py, with its rule and its exclusions, and run where it runs: last in regenerate_surfaces.py
(the deposit pipeline's surfaces) and seat_capture_postflight.py (capture intake), and in the /non landings
(land_non_row.py, land_non_pending.py). A page a generator rewrites without the tag gets it back at the next run.

THE RULE
--------
Every tracked .html page outside data/ carries the tag exactly once, immediately before its last </body>.
  - data/ and the /non intake and ledger folders are excluded (deposited bytes and hashed source pages).
  - A redirect stub (meta refresh) is excluded.
  - A page with no </body> is reported and left alone.
  - A page that carries the tag more than once is reduced to one.
  - A page already carrying a GoatCounter count.js tag of any form counts as present (the generators' own tag stays).
Insertion only: no other byte of a page changes. Idempotent; deterministic.

Usage:
  python3 scripts/sync_goatcounter.py           # write
  python3 scripts/sync_goatcounter.py --check   # report only; exit 0 always (laws record, they do not prevent)
"""
import re, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TAG = '<script data-goatcounter="https://alexanarch.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
TAG_RE = re.compile(r'[ \t]*<script\b[^>]*\bsrc="(?:https?:)?//gc\.zgo\.at/count\.js"[^>]*>\s*</script>[ \t]*\n?')
REFRESH_RE = re.compile(r'<meta[^>]+http-equiv=["\']?refresh', re.I)
BODY_END_RE = re.compile(r'</body\s*>', re.I)


def pages():
    out = subprocess.check_output(["git", "-c", "core.quotepath=off", "ls-files", "-z", "*.html"], cwd=ROOT)
    for f in out.decode("utf-8").split("\0"):
        if f and not f.startswith(("data/", "datasets/negative-of-the-negative/v2/intake/", "datasets/negative-of-the-negative/v2/ledgers/")):
            yield f


def ensure(html):
    """Return (new_html, action). action in: present, added, deduped, redirect, no-body."""
    if REFRESH_RE.search(html):
        return html, "redirect"
    n = len(TAG_RE.findall(html))
    if n == 1:
        return html, "present"
    if n > 1:
        first = TAG_RE.search(html)
        keep = html[:first.end()]
        rest = TAG_RE.sub("", html[first.end():])
        return keep + rest, "deduped"
    ends = list(BODY_END_RE.finditer(html))
    if not ends:
        return html, "no-body"
    i = ends[-1].start()
    return html[:i] + TAG + "\n" + html[i:], "added"


def main():
    check = "--check" in sys.argv
    counts, noted = {}, {}
    for f in pages():
        p = ROOT / f
        try:
            html = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError):
            counts["unreadable"] = counts.get("unreadable", 0) + 1
            continue
        new, act = ensure(html)
        counts[act] = counts.get(act, 0) + 1
        if act in ("no-body", "deduped"):
            noted.setdefault(act, []).append(f)
        if new != html and not check:
            p.write_text(new, encoding="utf-8")
    mode = "check" if check else "write"
    print(f"sync_goatcounter ({mode}): " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    for act, fs in noted.items():
        print(f"  {act}: " + ", ".join(fs[:10]) + (" …" if len(fs) > 10 else ""))


if __name__ == "__main__":
    main()
