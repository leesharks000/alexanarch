"""Capture repair 2026-10-31: AXN:0B4B (ChatGPT) and AXN:0B4C (Google AI Mode), the two readings of #1723. Their findings said the
terms 'compression saving' and 'routing gain' are #1723 §6.7's parentheticals, "which #1666's text does not carry", and that the
readers carried a misquotation as the authors' claim. #1666 defines both (§2.1 "The compression saving, S"; §2.2 "The routing gain,
G"); #1723's defect was setting them inside a quoted sentence that does not carry them. The readers composed them as the authors'
terms, correctly. Repaired: the first finding of each, their mt, analysis and related deposits (adding #1724, the v1.1 that
corrected #1723). Every other field stands. Repair mode, one operation, its own commit; fields taken whole from the intake drafts
rebuilt from the repaired parts.py.
  python3 repair-terms-20261031.py [--check]"""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
reg = json.loads(REG.read_text(encoding="utf-8"))
for slug in ("the-layer-is-a-party-chatgpt-20261031", "the-layer-is-a-party-aimode-20261031"):
    new = json.loads((H / (slug + ".json")).read_text(encoding="utf-8"))
    e = [x for x in reg["entries"] if x.get("slug") == slug]; assert len(e) == 1; e = e[0]
    assert "does not carry" in json.dumps(e["findings"]), (slug, "already repaired?")
    ch = []
    for k in ("findings", "mt", "analysis", "related_deposits"):
        if e.get(k) != new[k]: e[k] = new[k]; ch.append(k)
    for o in e.get("observations") or []:
        for k in ("findings", "mt", "analysis", "related_deposits"):
            if k in o and o[k] != new[k]: o[k] = new[k]; ch.append("obs." + k)
    print(slug, ch)
if "--check" not in sys.argv:
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
