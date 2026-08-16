#!/usr/bin/env python3
"""check_datasets_tab.py — does the datasets tab describe what is actually there?

The tab is a hand-maintained page over a corpus that moves. On 2026-08-15 an audit found:
eight of ten checkable figures stale (captures 204/v9.6 against 343/v11.4; citation edges
4,866 against 9,992; registry.json 5.97 MB against 23.4 MB), TEN datasets present and
unlisted, one malformed card, and scripts listed as datasets.

This does not rewrite the page. It reports what disagrees, so the drift is visible without
someone counting by hand.

Usage: check_datasets_tab.py
"""
import json, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
TAB = ROOT / "datasets/index.html"


def size_of(p):
    p = ROOT / p
    if p.is_dir():
        return sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
    return p.stat().st_size if p.exists() else 0


def count_json(path, key=None):
    p = ROOT / path
    if not p.exists():
        return None
    d = json.loads(p.read_text())
    if key and isinstance(d, dict) and key in d:
        return len(d[key]) if hasattr(d[key], "__len__") else d[key]
    if isinstance(d, list):
        return len(d)
    for k in ("deposits", "edges", "concepts", "terms", "addresses", "conversations"):
        if isinstance(d, dict) and k in d and hasattr(d[k], "__len__"):
            return len(d[k])
    return len(d) if hasattr(d, "__len__") else None


def main():
    html = TAB.read_text()
    fails = []

    # 1 — datasets present but unlisted
    present = {p.name for p in (ROOT / "datasets").iterdir() if p.is_dir()}
    listed = set(re.findall(r'datasets/([a-z0-9-]+)/', html))
    missing = sorted(present - listed)
    if missing:
        fails.append(f"{len(missing)} dataset(s) present and NOT on the tab: " + ", ".join(missing))

    # 2 — malformed cards
    for card in re.findall(r'<div class="ds">(.*?)\n</div>', html, re.S):
        # the name may wrap a link or an <em> marker; require TEXT, not a bare string
        m = re.search(r'<span class="ds-name">(.*?)</span>', card, re.S)
        if not m or not re.sub(r"<[^>]+>", "", m.group(1)).strip():
            fails.append("a card has no ds-name text — malformed")

    # 3 — checkable figures
    figs = [
        # anchor on the registry card, not the first "deposits" anywhere on the page —
        # the preliminary-mapping card also says "864 deposits" and matched first.
        ("registry deposits", count_json("data/registry.json"),
         r'registry\.json</span>\s*<span class="ds-meta">[^<]*<strong[^>]*>(\d[\d,]*)</strong>\s*deposits'),
        ("citation edges", count_json("data/citation-graph.json"), r"(\d[\d,]*)\s*edges"),
    ]
    for label, actual, pat in figs:
        m = re.search(pat, html)
        if m and actual is not None:
            claimed = int(m.group(1).replace(",", ""))
            if claimed != actual:
                fails.append(f"{label}: tab says {claimed:,}, actual {actual:,}")

    # 4 — capture registry version (three near-identical filenames; the wrong one has been read)
    live = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text())
    lv, ln = live.get("version"), live.get("total_captures")
    if f"v{lv}" not in html:
        m = re.search(r"v(\d+\.\d+)[^<]{0,40}captur|captur[^<]{0,40}v(\d+\.\d+)", html, re.I)
        fails.append(f"capture registry: live is v{lv} with {ln} captures; the tab does not name v{lv}")

    # 5 — scripts on a datasets tab. They may appear, but only under a heading that says
    # what they are: a script is a PRODUCER, not a dataset, and listing the two alike is how
    # a reader comes to think the tab enumerates data when it enumerates whatever was added.
    n = len(re.findall(r'<span class="ds-name">scripts/', html))
    if n and not re.search(r'<h2[^>]*>\s*Producers', html):
        fails.append(f"{n} script(s) listed as datasets with no Producers heading — "
                     "a script is a producer, not a dataset")

    # 6 — superseded artefacts still presented as current
    if "JOURNAL-MAPPING-PRELIMINARY" in html and "superseded" not in html.lower():
        fails.append("JOURNAL-MAPPING-PRELIMINARY.json is listed without being marked superseded "
                     "(superseded 2026-08-15 by datasets/journals)")

    if fails:
        print(f"FAIL: {len(fails)} problem(s) on the datasets tab:")
        for f in fails:
            print("  " + f)
        return 1
    print("OK: the datasets tab agrees with the corpus")
    return 0


if __name__ == "__main__":
    sys.exit(main())
