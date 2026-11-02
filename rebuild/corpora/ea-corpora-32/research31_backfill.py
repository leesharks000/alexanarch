#!/usr/bin/env python3
"""Session tool, 2026-11-02. Writes the research field into the EA-CORPORA-31 seats (the operator's rule of that day: a seating
conducted in the course of active research names that research). source.json is outside each seat's MANIFEST.sha256, so the
manifests and the AXNs assigned from them are unchanged.
    python3 research31_backfill.py <stage>      (the stage is data/corpora)"""
import json, pathlib, sys
from gen_spec32 import research
ST = pathlib.Path(sys.argv[1])
FOR = {"athenaeus": "design §3 (the custody stories) and §5", "galen": "design §3 (the acquisition economy and the falsifying of titles) and §5",
       "porphyry": "design §3 (Andronicus's edition as an operation) and §5", "aristotle-commentators": "design §3.9a and draft §2 (Simplicius and the Categories)",
       "arabic-biobibliography": "design §3 (Ptolemy's catalogue with the life and the will) and §5", "hermippus": "design §3 (the catalogue become biography) and §5",
       "hesychian-catalogue": "design §3 (the third list and its pseudepigrapha) and §5", "callimachus-pinakes": "design §3 (the Pinakes, the filing system the lists inherit) and §5",
       "bekker-aristotle-1831": "design §3.10 (the modern edition and the developmental life)", "jaeger-aristoteles": "design §3.10 (the modern edition and the developmental life)",
       "transmission-wanted": "design §5 (the debts declared without text)"}
for c, f in FOR.items():
    p = ST / c / "source.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    if d.get("seat", "").startswith("EA-CORPORA-31/"):
        r = research(f); r["owed_at"] = "design §5, the debts of v0.1 (seated at EA-CORPORA-31, #1730)"
        d["research"] = r
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(c, "ok")
