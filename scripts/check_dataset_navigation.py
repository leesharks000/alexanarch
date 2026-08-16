#!/usr/bin/env python3
"""check_dataset_navigation.py — does every dataset present the same way?

AUDITED AS RENDERED, 2026-08-15. The tab and its subpages had accreted rather than been
designed. Findings on the first run:

  * TWO dataset subpages 404'd — /datasets/journals/ and /datasets/mret/ — both linked from
    the tab the same day they were added. A card was written; the page it pointed at was not.
  * FIVE title forms in use across sixteen pages: the PATH as title ("datasets/venues/ —
    Alexanarch"), "Name — Datasets — Alexanarch", "Name — Alexanarch", "Name — dataset", and
    bare. A reader cannot tell from a tab or a search result which dataset they are in.
  * A TITLE COLLISION: tombstone-mirror and zenodo-datacite-batch both render as
    "Zenodo/DataCite Batch".
  * TWO pages carry no back-link to /datasets/ — capture-registry and
    deletion-conformance-fixture. Once there, the reader is stranded.
  * ZERO pages have sub-navigation. Every dataset is one page linking files directly, which is
    fine and should be stated as the rule rather than left as an accident.

THE SEATING RULE this enforces, stated so a new dataset has a shape to meet:
  1. A directory under datasets/ MUST have an index.html, or it must not be linked.
  2. Title MUST be "<Name> — Datasets — Alexanarch". The path is not a title.
  3. Titles MUST be unique across datasets.
  4. Every page MUST link back to /datasets/.
  5. Every page SHOULD declare its canonical store and what regenerates it (atlas v1.5 rule).
  6. Files are linked directly from the dataset page. One level, no deeper.

Usage: check_dataset_navigation.py [--rendered]   (--rendered probes the live site)
"""
import json, re, sys, pathlib, argparse, collections, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DS = ROOT / "datasets"
SUFFIX = " — Datasets — Alexanarch"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--rendered", action="store_true")
    a = ap.parse_args()
    fails, titles = [], {}
    dirs = sorted(p for p in DS.iterdir() if p.is_dir())

    for d in dirs:
        idx = d / "index.html"
        if not idx.exists():
            fails.append(f"{d.name}: NO index.html — a dataset without a page must not be linked")
            continue
        html = idx.read_text(errors="replace")
        m = re.search(r"<title>([^<]*)</title>", html)
        t = m.group(1).strip() if m else ""
        if not t:
            fails.append(f"{d.name}: no <title>")
        else:
            titles.setdefault(t, []).append(d.name)
            if t.startswith("datasets/"):
                fails.append(f"{d.name}: title is the PATH ({t!r}) — a path is not a title")
            elif not t.endswith(SUFFIX):
                fails.append(f"{d.name}: title {t!r} does not end {SUFFIX!r}")
        if not re.search(r'href="/datasets/?"', html):
            fails.append(f"{d.name}: no back-link to /datasets/ — the reader is stranded")

    for t, names in titles.items():
        if len(names) > 1:
            fails.append(f"TITLE COLLISION {t!r}: " + ", ".join(names))

    # every dataset linked from the tab must exist
    tab = (DS / "index.html").read_text(errors="replace")
    for slug in sorted(set(re.findall(r'href="/datasets/([a-z0-9-]+)/"', tab))):
        if not (DS / slug).is_dir():
            fails.append(f"tab links /datasets/{slug}/ which is not a directory")
        elif not (DS / slug / "index.html").exists():
            fails.append(f"tab links /datasets/{slug}/ which has NO index.html — it will 404")

    if a.rendered:
        for d in dirs:
            u = f"https://alexanarch.org/datasets/{d.name}/"
            try:
                with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "nav-check"}), timeout=20) as r:
                    code, n = r.status, len(r.read())
            except Exception as e:
                code, n = getattr(e, "code", "ERR"), 0
            if code != 200:
                fails.append(f"RENDERED {d.name}: {u} -> {code}")

    if fails:
        print(f"FAIL: {len(fails)} navigation problem(s):")
        for f in fails: print("  " + f)
        return 1
    print(f"OK: {len(dirs)} datasets present the same way")
    return 0


if __name__ == "__main__":
    sys.exit(main())
