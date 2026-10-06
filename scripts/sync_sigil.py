#!/usr/bin/env python3
"""sync_sigil.py — Speak with Sigil on every page of alexanarch, once.

WHY THIS EXISTS
---------------
Speak with Sigil (the Mandala Oracle's panel, served from themandalaoracle.com/embed/sigil.js) went onto
alexanarch on 2026-10-03 (902cab052c) through the record template, the home page and the Book: 1,667 of
10,354 pages. Every other page (the captures gallery and its records, /non, /how, the 4,533 address
pages, the resolvers) had no panel. On leesharks.com and the Secret Book it is on every page. Lee,
2026-10-06: "only on main of alexanarch".

Most pages are written by generators, and many generators write no common footer, so the tag is kept
here, in one place, and this sweep runs last in the two page-writing pipelines (regenerate_surfaces.py
and seat_capture_postflight.py). A page a generator rewrites without the tag gets it back at the next run.

THE RULE
--------
Every tracked .html page outside data/ carries the tag exactly once, immediately before its last </body>.
  - data/ is excluded: it holds deposited artifacts (corpora, attachments, trackers), whose bytes are
    the deposit's and are not the site's to change.
  - A redirect stub (meta refresh) is excluded: nobody reads it.
  - A page with no </body> is reported and left alone (datasets/venues/index.html, 2026-10-06: the page
    ends without </body></html>, a separate defect).
  - A page that carries the tag more than once is reduced to one.
Insertion only: no other byte of a page changes. Idempotent; deterministic.

Usage:
  python3 scripts/sync_sigil.py           # write
  python3 scripts/sync_sigil.py --check   # report only; exit 0 always (laws record, they do not prevent)
"""
import re, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = "https://www.themandalaoracle.com/embed/sigil.js"
TAG = f'<script src="{SRC}" defer></script>'
TAG_RE = re.compile(r'[ \t]*<script\b[^>]*\bsrc="https://www\.themandalaoracle\.com/embed/sigil\.js"[^>]*>\s*</script>[ \t]*\n?')
REFRESH_RE = re.compile(r'<meta[^>]+http-equiv=["\']?refresh', re.I)
BODY_END_RE = re.compile(r'</body\s*>', re.I)


def pages():
    out = subprocess.check_output(["git", "-c", "core.quotepath=off", "ls-files", "-z", "*.html"], cwd=ROOT)
    for f in out.decode("utf-8").split("\0"):
        if f and not f.startswith("data/"):
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
    print(f"sync_sigil ({mode}): " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    for act, fs in noted.items():
        print(f"  {act}: " + ", ".join(fs[:10]) + (" …" if len(fs) > 10 else ""))


if __name__ == "__main__":
    main()
