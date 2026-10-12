#!/usr/bin/env python3
"""Backfill `intended` on v12.109 (erratum-missing-translator-exact-title-aio-20261011): the run was issued from #1675's record page;
the composition cited the registry mirror and Pre-Textos, not the record page, so reached is false. Operator, 2026-10-11: 'captures
would need to include links to the title and link they were *supposed* to point to, even when they dont appear in overview cards'."""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]; sys.path.insert(0, str(ROOT))
from wire_deposit import search_title_of
from urllib.parse import quote_plus
P = ROOT / "data/EA-WG-CAPTURES-01.json"
caps = json.loads(P.read_text(encoding="utf-8"))
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
d = reg[1675]
e = [e for e in caps["entries"] if e["slug"] == "erratum-missing-translator-exact-title-aio-20261011"][0]
assert all("alexanarch.org/s/records/1675" not in (c.get("url") or "") for c in e["cite_list"])
e["intended"] = {"deposit": 1675, "axn": d["axn"], "title": d["title"], "record": "https://www.alexanarch.org/s/records/1675/",
                 "search": "https://www.google.com/search?q=" + quote_plus('"' + search_title_of(d) + '"'), "reached": False}
P.write_text(json.dumps(caps, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(e["intended"], ensure_ascii=False))
