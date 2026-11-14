#!/usr/bin/env python3
"""mantle-bearing 1.33: #1769 Daffodils reissued in place as v1.1 (2026-11-14, the author's words of 17:38, 17:40, 17:41): the framework and hologram rows
brought to the record's current AXN and title; the rival row restated with its common ground and contested point; the failure flags read from the v1.1
ontology (DEFINITION_ASSUMED added); kernel files re-copied by the builder.
    python3 rebuild/mantle-bearing/v133_daffodils_v11.py"""
import json, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
A = "https://www.alexanarch.org"; N = 1769; FD = ROOT / f"files/AXN-{REG[N]['hex']}"
rec = lambda n: {"deposit": n, "axn": REG[n]["axn"], "url": f"{A}/s/records/{n}/", "title": REG[n]["title"]}
d = json.loads(SRC.read_text(encoding="utf-8"))
if any(h["version"] == "1.33" for h in d["history"]): raise SystemExit("1.33 already applied")
assert d["history"][-1]["version"] == "1.32" and REG[N]["version"] == "v1.1"
K = yaml.safe_load((FD / "kernel/00-kernel.yaml").read_text(encoding="utf-8")); O = yaml.safe_load((FD / "kernel/01-ontology.yaml").read_text(encoding="utf-8"))
f = next(x for x in d["frameworks"] if x["framework"] == "framework::daffodils")
f["seed_record"] = [rec(N), rec(833)]; f["governing_record"] = [rec(N)]
f["rival"] = {"node": K["rival"]["@id"], "summary": K["rival"]["stated_at_strength"], "common_ground": K["rival"]["common_ground"], "contested": K["rival"]["contested"], "faces": K["rival"]["faces"]}
f["status"] = "DEPOSITED 2026-11-14 (v1.0); REISSUED the same day as v1.1 (what is contested: the definition of a healthy flagship, not the journal's meeting it)"
h = next(x for x in d["holograms"] if x["hologram"] == "hologram::daffodils")
h["governing_record"] = [rec(N)]; h["hologram_record"] = [rec(N)]
h["status"] = f["status"] + "; the entity row /non/classical-receptions-journal/ revised to cite it"
h["failure_flags"] = O["failure_flags"]; h["failure_flags_source"] = f"EA-HK-DAFFODILS-01 v1.1 (#{N}): 01-ontology.yaml failure_flags"
d["history"].append({"version": "1.33", "date": "2026-11-14", "note": ("#1769 Daffodils reissued in place as v1.1: the framework and hologram rows brought to the record's "
    "current AXN and title; the rival restated with its common ground (the journal meets the received definition of a healthy flagship) and its contested point (whether "
    "that definition defines health); seventeen failure flags with DEFINITION_ASSUMED. rebuild/mantle-bearing/v133_daffodils_v11.py.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("1.33 applied")
