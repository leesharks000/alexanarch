#!/usr/bin/env python3
"""check_works_cited.py — record, at deposit, whether a record carries a standard works-cited list.

The author, 2026-11-23 20:40: "we have to keep standard works cited lists alongside axn citations - aggregators read
citations as authority. full stop. google scholar wont index without it." Adopted 20:48 as a step at deposit. The list
is read by scripts/references_lib.py; the finding is one of: list (with its count of entries), section without entries
(sources given as prose), footnotes only, none.

Laws record; they do not prevent. The finding is written to data/works-cited-ledger.json and printed; the deposit goes
on either way. A poem, a dataset seating or a capture snapshot has no list to keep, and its finding says so plainly
rather than being skipped.

    python3 scripts/check_works_cited.py --deposit-number N
    python3 scripts/check_works_cited.py --from 1700 --to 1804      # a range, e.g. an audit
"""
import argparse, json, pathlib, sys, datetime
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import references_lib as R

LEDGER = ROOT / "data/works-cited-ledger.json"


def text_of(d):
    p = ROOT / (d.get("full_text_path") or "").lstrip("/")
    if not p.exists() or p.suffix not in (".md", ".txt"):
        p = ROOT / f"data/texts/AXN-{d['hex']}-text.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deposit-number", type=int)
    ap.add_argument("--from", dest="lo", type=int)
    ap.add_argument("--to", dest="hi", type=int)
    a = ap.parse_args()
    reg = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
    ns = [a.deposit_number] if a.deposit_number else [n for n in sorted(reg) if (a.lo or 0) <= n <= (a.hi or 10 ** 9)]
    led = json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {
        "_note": "One finding per record: whether its text carries a standard works-cited list (scripts/references_lib.py). "
                 "Recorded at deposit by scripts/check_works_cited.py; laws record, they do not prevent.",
        "records": {}}
    today = datetime.date.today().isoformat()
    for n in ns:
        d = reg.get(n)
        if not d:
            continue
        f = R.finding(text_of(d))
        f.update({"checked": today, "content_type": (d.get("content_type") or "")[:80]})
        led["records"][str(n)] = f
        print(f"works cited #{n}: {f['state']}" + (f" ({f['entries']} entries)" if f["entries"] else ""))
    led["records"] = dict(sorted(led["records"].items(), key=lambda kv: int(kv[0])))
    LEDGER.write_text(json.dumps(led, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
