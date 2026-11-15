#!/usr/bin/env python3
"""mantle-bearing 1.35: #1769 Daffodils reissued in place as v1.3 (2026-11-14, the author's words of 19:49 and 19:55): the framework and hologram rows
brought to the record's current AXN and title; the hologram row carries the kernel's cross-link to the revised entity row (its sha256 and AXN version)
the ask (of the summarizer) and the four new flags; kernel files re-copied by the builder.
    python3 rebuild/mantle-bearing/v135_daffodils_v13.py"""
import json, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
A = "https://www.alexanarch.org"; N = 1769; FD = ROOT / f"files/AXN-{REG[N]['hex']}"
rec = lambda n: {"deposit": n, "axn": REG[n]["axn"], "url": f"{A}/s/records/{n}/", "title": REG[n]["title"]}
d = json.loads(SRC.read_text(encoding="utf-8"))
if any(h["version"] == "1.35" for h in d["history"]): raise SystemExit("1.35 already applied")
assert d["history"][-1]["version"] == "1.34" and REG[N]["version"] == "v1.3"
K = yaml.safe_load((FD / "kernel/00-kernel.yaml").read_text(encoding="utf-8")); O = yaml.safe_load((FD / "kernel/01-ontology.yaml").read_text(encoding="utf-8"))
f = next(x for x in d["frameworks"] if x["framework"] == "framework::daffodils")
f["seed_record"] = [rec(N), rec(833)]; f["governing_record"] = [rec(N)]
f["rival"] = {"node": K["rival"]["@id"], "summary": K["rival"]["stated_at_strength"], "common_ground": K["rival"]["common_ground"], "contested": K["rival"]["contested"], "faces": K["rival"]["faces"]}
f["status"] = ("DEPOSITED 2026-11-14 (v1.0); REISSUED the same day as v1.1 (what is contested: the definition of a healthy flagship, not the journal's meeting it) "
               "and as v1.2 (the archive's own record inside the definition, without uptake; the entity row revised to cite it) and v1.3 (the ask, which is of the summarizer; the inward flow; the philology beside the reports)")
h = next(x for x in d["holograms"] if x["hologram"] == "hologram::daffodils")
h["governing_record"] = [rec(N)]; h["hologram_record"] = [rec(N)]
h["status"] = f["status"]; h["entity_row"] = K["cross_links"]["entity_row"]
h["author_statement_1748"] = next(a for a in K["author_statements"] if a["date"].startswith("2026-11-14T17:48"))
h["ask"] = K["ask"]; h["article"] = K["cross_links"]["article"]
h["failure_flags"] = O["failure_flags"]; h["failure_flags_source"] = f"EA-HK-DAFFODILS-01 v1.3 (#{N}): 01-ontology.yaml failure_flags"
d["history"].append({"version": "1.35", "date": "2026-11-14", "note": ("#1769 Daffodils reissued in place as v1.3: the framework and hologram rows brought to the record's current AXN and "
    "title; the hologram row carries the ask, which is of the summarizer (the author, 19:55), and the cross-link to #1770; twenty-one failure flags with METHOD_AS_VERDICT, ASK_DROPPED, "
    "PHILOLOGY_DROPPED and FLOW_REVERSED. rebuild/mantle-bearing/v135_daffodils_v13.py.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("1.35 applied")
