"""Check the archive quotations inside the selected capture findings against the deposit texts they name
(report only; nothing in the registry is changed).   /tmp/py312/python3 check_caps.py"""
import json, re
from vlib import *
R = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text())["deposits"]}
def dtext(n): return deposit_text(R[n]["full_text_path"].lstrip("/"))
checks = [
 ("sappho-illiterate-jealous-aio-20261113", 1, 1752, ["Hermann rewrote the last two transmitted lines, said so (\"refinxi\"), and then read the poem off his rewriting"]),
 ("sappho-illiterate-jealous-aio-20261113", 2, 1752, ["Mure (1850) gives the rival as the scene's situation", "what lies between Hermann and Mure; Heller 1856", "the ancient account is a love in ecstasy, and the amendment to jealousy is his, \"We may amend\""]),
 ("sappho-future-reader-aio-20261107", 2, 134, ["Catullus 51 as Recognition Event"]),
 ("sappho-future-reader-aio-20261107", 2, 1270, ["points away from the speaker"]),
 ("detail-sappho-future-reader-framework-aio-20261030", 1, 1054, ["is the papyrus itself"]),
 ("detail-sappho-future-reader-framework-aio-20261030", 1, 1270, ["because he possesses what should be impossible: presence with the dead."]),
 ("detail-sappho-future-reader-framework-chatgpt-20261030", 1, 1645, ["The seat is a reading, and the reading has an author."]),
 ("detail-sappho-future-reader-framework-chatgpt-20261030", 1, 1270, ["it locates that content within a different temporal structure"]),
 ("sappho-future-reader-aio-20261027", 3, 1645, ["147 does not contain 31's mechanism, and τινα does not mean \"reader\""]),
 ("sappho-future-reader-aio-20261027", 2, 1270, ["points away from the speaker, toward someone removed from the immediate situation"]),
 ("sappho-future-reader-framework-aio-20261030", 0, 1645, ["The seat is a reading, and the reading has an author."]),
]
out = []
for slug, i, dep, qs in checks:
    f = entry(slug)["findings"][i]
    t = dtext(dep)
    for q in qs:
        inf = norm(q) in norm(f)
        ind = norm(q) in norm(t)
        out.append({"slug": slug, "finding": i, "dep": dep, "quote": q, "in_finding": inf, "in_deposit": ind})
        print("OK " if ind else "NOT IN DEPOSIT", slug, i, dep, q[:80])
# absence claims of sappho-future-reader-framework-aio-20261030 findings[1]
for term in ["camera lens", "unbundling", "activation mechanism"]:
    hits = [n for n in (134, 281, 1270, 1054, 1548, 1645, 1646) if term.lower() in dtext(n).lower()]
    out.append({"slug": "sappho-future-reader-framework-aio-20261030", "finding": 1, "absence_term": term, "found_in": hits})
    print("absence", term, hits)
(STAGE / "capture-checks.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
