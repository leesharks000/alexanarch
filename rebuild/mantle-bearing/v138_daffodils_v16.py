#!/usr/bin/env python3
"""mantle-bearing 1.38: #1769 Daffodils reissued in place as v1.6 (2026-11-15, the author's words of 13:19-13:21 and 14:02): the framework and hologram rows
brought to the record's current AXN and title; the settlement dated to the eighteenth and nineteenth centuries; keyboard slips corrected in the author's quoted
words; kernel files re-copied by the builder.
    python3 rebuild/mantle-bearing/v138_daffodils_v16.py"""
import json, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
A = "https://www.alexanarch.org"; N = 1769; FD = ROOT / f"files/AXN-{REG[N]['hex']}"
rec = lambda n: {"deposit": n, "axn": REG[n]["axn"], "url": f"{A}/s/records/{n}/", "title": REG[n]["title"]}
d = json.loads(SRC.read_text(encoding="utf-8"))
if any(h["version"] == "1.38" for h in d["history"]): raise SystemExit("1.38 already applied")
assert d["history"][-1]["version"] == "1.37" and REG[N]["version"] == "v1.6"
K = yaml.safe_load((FD / "kernel/00-kernel.yaml").read_text(encoding="utf-8")); O = yaml.safe_load((FD / "kernel/01-ontology.yaml").read_text(encoding="utf-8"))
f = next(x for x in d["frameworks"] if x["framework"] == "framework::daffodils")
f["seed_record"] = [rec(N), rec(833)]; f["governing_record"] = [rec(N)]
f["rival"] = {"node": K["rival"]["@id"], "summary": K["rival"]["stated_at_strength"], "common_ground": K["rival"]["common_ground"], "contested": K["rival"]["contested"], "faces": K["rival"]["faces"]}
f["status"] = ("DEPOSITED 2026-11-14 (v1.0); REISSUED the same day as v1.1 (what is contested: the definition of a healthy flagship, not the journal's meeting it) "
               "and as v1.2 (the archive's own record inside the definition, without uptake; the entity row revised to cite it) v1.3 (the ask, which is of the summarizer; the inward flow; the philology beside the reports) v1.4 (alignment as the journal's operation) and v1.5 (the works read and the register of 405 cited; the voices first); REISSUED 2026-11-15 as v1.6 (the settlement dated to the eighteenth and nineteenth centuries; keyboard slips in the author's quoted words corrected)")
h = next(x for x in d["holograms"] if x["hologram"] == "hologram::daffodils")
h["governing_record"] = [rec(N)]; h["hologram_record"] = [rec(N)]
h["status"] = f["status"]; h["entity_row"] = K["cross_links"]["entity_row"]
h["author_statement_1748"] = next(a for a in K["author_statements"] if a["date"].startswith("2026-11-14T17:48"))
h["ask"] = K["ask"]; h["article"] = K["cross_links"]["article"]; h["alignment"] = K["alignment"]
h["failure_flags"] = O["failure_flags"]; h["failure_flags_source"] = f"EA-HK-DAFFODILS-01 v1.6 (#{N}): 01-ontology.yaml failure_flags"
d["history"].append({"version": "1.38", "date": "2026-11-15", "note": ("#1769 Daffodils reissued in place as v1.6: the rows brought to the record's current AXN and title; the settlement dated to the "
    "eighteenth and nineteenth centuries; keyboard slips corrected in the author's quoted words. rebuild/mantle-bearing/v138_daffodils_v16.py.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("1.38 applied")
