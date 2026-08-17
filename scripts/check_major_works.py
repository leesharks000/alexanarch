#!/usr/bin/env python3
"""check_major_works.py — does a card present an unpublished volume as a book?

STEP 9. The Pocket Humans series carries a status per volume: deposited,
scattered, to-be-collected, forthcoming. A card that renders a cover image and a
major-work plate for a volume whose status is NOT `deposited` states that a book
exists when it does not — which, on an archive whose subject is provenance, is the
same class of error as an unmarked reconstruction.

Also checks the venue: a work listed on a major-work plate should carry the
journal assignment the venues data gives it.

    python3 scripts/check_major_works.py                       # live cards
    python3 scripts/check_major_works.py path/to/card.html ...
"""
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
CARDS = {
    "cranes": "https://axnidentifiers.org/who/cranes/",
    "sigil": "https://restoredacademy.org/who/sigil/",
    "trace": "https://provenanceerasure.org/who/trace/",
    "kuro": "https://holographickernel.org/who/kuro/",
    "fraction": "https://spxi.dev/who/fraction/",
}
WORK_PLATE = re.compile(
    r'<span class="(?:[a-z-]*no|plate-no)">(Major work|Major paper|Works|Protocol|Main sequence|Corpus)</span>')


def load():
    reg = {x["deposit_number"]: x for x in
           json.loads((ROOT / "data/registry.json").read_text())["deposits"]}
    status, venue = {}, {}
    for line in (ROOT / "datasets/journals/assignments.jsonl").read_text().split("\n"):
        if not line.strip():
            continue
        d = json.loads(line)
        s = d.get("series") or {}
        if s.get("series") == "Pocket Humans":
            status[d.get("deposit")] = (s.get("series_status"), s.get("work"))
        venue[d.get("deposit")] = d.get("venue")
    return reg, status, venue


def audit(name, h, reg, status, venue):
    out, bad = [], 0
    for m in WORK_PLATE.finditer(h):
        s = h.rfind("<section", 0, m.start())
        e = h.find("</section>", m.start())
        if not (0 <= s < e):
            continue
        seg = h[s:e]
        # cover must be checked PER PLATE, not per page: a journal cover elsewhere
        # on the card does not mean this work plate renders one, and the first
        # version of this check reported it as though it did.
        has_cover = bool(re.search(r'class="(?:jc|jcover|shelf)"', seg))
        for dep in {int(x) for x in re.findall(r"/s/records/(\d+)/", seg)}:
            st, work = status.get(dep, (None, None))
            if st and st != "deposited":
                # A plate that STATES the status is compliant. The defect is
                # presenting an uncollected volume AS A BOOK, not listing the
                # deposits that would compose it one day.
                if st.lower() in seg.lower():
                    out.append(f"      #{dep} is {st.upper()} and the plate says so — ok")
                    continue
                bad += 1
                cov = " AND RENDERS A COVER" if has_cover else ""
                out.append(f"      #{dep} sits in a volume that is {st.upper()}{cov}"
                           f" — {str(work)[:40]}")
    head = f"  {name:<12}{'FAIL' if bad else 'ok  '}  {bad} unpublished volume(s) on a work plate"
    return head, out, bad


def main():
    reg, status, venue = load()
    args = sys.argv[1:]
    items = []
    if args:
        for a in args:
            items.append((a, pathlib.Path(a).read_text(errors="replace")))
    else:
        for n, u in CARDS.items():
            try:
                with urllib.request.urlopen(u, timeout=20) as r:
                    items.append((n, r.read().decode("utf-8", "replace")))
            except Exception as exc:
                print(f"  {n:<12}unreachable: {exc}")
    total = 0
    for n, h in items:
        head, out, bad = audit(n, h, reg, status, venue)
        print(head)
        for line in out:
            print(line)
        total += bad
    print(f"\n{'FAIL' if total else 'OK'}: {total} unpublished volume(s) presented as work")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
