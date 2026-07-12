#!/usr/bin/env python3
"""
build_distribution_index.py — EA-DISTRO-01 §6.

Rebuilds data/distribution-index.json from data/registry.json, preserving any
previously recorded distribution acts. New deposits enter as 'unassigned'.
Never hand-grow the index; regenerate it and record acts via record_act().

Usage:
  python3 scripts/build_distribution_index.py            # rebuild frame
  python3 scripts/build_distribution_index.py --stats    # print stats only
"""

import json
import os
import sys
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, "data", "registry.json")
IDX = os.path.join(ROOT, "data", "distribution-index.json")

CHANNELS = ["figshare", "dataverse", "osf", "mediarxiv", "kcworks",
            "swh", "hal", "philarchive", "philsci", "ssrn",
            "data_rhizome", "wayback", "zenodo_reentry"]

# Curated routing (EA-DISTRO-01 §5). deposit_number -> (priority, planned channels)
FLAGSHIPS = {
    28:  ["kcworks", "figshare"],          # Space Ark — Musical Register
    69:  ["kcworks", "figshare"],          # O Meta-Heterônimo
    79:  ["kcworks", "mediarxiv"],         # Heteronymy Is a Function
    88:  ["kcworks", "figshare"],          # Constitution of the Semantic Economy
    179: ["kcworks"],                       # Sappho — Canon Provenance Node (opener)
    201: ["kcworks"],                       # Sappho 31 Erratum (opener cluster)
    203: ["figshare"],                      # Josephus MPAI
    329: ["kcworks", "figshare"],          # Pearl and Other Poems
    864: ["figshare"],                      # Drain Hypothesis
}
INSTRUMENTS = {
    910:  ["kcworks"],                      # EA-OPMETA-01
    943:  ["kcworks", "mediarxiv"],        # Whitespace as Provenance
    1068: ["figshare", "dataverse"],       # Tombstone Mirror (Obelus)
    1071: ["figshare", "dataverse"],       # Tombstone anchor (Ledger)
    1073: ["kcworks"],                      # doctrinal exposure
    1074: ["figshare"],                     # Counter-infrastructure anchor
    1075: ["figshare", "dataverse", "mediarxiv"],  # NEGSHAPE + appendices
}
# Distribution acts already completed at index creation (verified):
INITIAL_ACTS = {
    1075: {"data_rhizome": {
        "status": "deposited",
        "venue_id": "github.com/leesharks000/data-rhizome negshape-deletion-bibliography/ @2d4d101",
        "date": "2026-07-12",
        "note": "Appendices A-B dataset mirror (paper canonical remains alexanarch)"}},
}


def classify(d):
    """Coarse work-class heuristic; MANUS refines by editing planned routes."""
    t = (d.get("title") or "").lower()
    n = d["deposit_number"]
    if n in FLAGSHIPS:
        return "flagship", FLAGSHIPS[n]
    if n in INSTRUMENTS:
        return "instrument", INSTRUMENTS[n]
    if d.get("date", "") >= "2026-06-19" and ("ea-" in t or t.startswith("ea ")):
        return "instrument", []
    if any(k in t for k in ("capture", "registry v", "fanout", "erratum",
                            "wiring", "enrichment")):
        return "corpus-native", []
    return "unassigned", []


def build():
    reg = json.load(open(REG))
    prior = {}
    if os.path.exists(IDX):
        old = json.load(open(IDX))
        for e in old.get("entries", []):
            acts = {ch: v for ch, v in (e.get("dist") or {}).items()
                    if v.get("status") not in (None, "none", "planned")}
            if acts:
                prior[e["n"]] = acts

    entries = []
    for d in reg["deposits"]:
        n = d["deposit_number"]
        cls, planned = classify(d)
        dist = {}
        for ch in planned:
            dist[ch] = {"status": "planned"}
        for ch, act in INITIAL_ACTS.get(n, {}).items():
            dist[ch] = act
        for ch, act in prior.get(n, {}).items():
            dist[ch] = act  # recorded acts always survive rebuilds
        if cls == "corpus-native":
            dist = dist or {"_policy": {"status": "native",
                                        "note": "alexanarch-native by EA-DISTRO-01 §4"}}
        entry = {"n": n, "hex": d.get("hex"), "title": d.get("title", "")[:120],
                 "date": d.get("date"), "class": cls}
        if dist:
            entry["dist"] = dist
        entries.append(entry)

    distributed = sum(1 for e in entries
                      if any(v.get("status") == "deposited"
                             for v in (e.get("dist") or {}).values()))
    planned_ct = sum(1 for e in entries
                     if any(v.get("status") == "planned"
                            for v in (e.get("dist") or {}).values()))
    idx = {
        "instrument": "EA-DISTRO-01 Total Distribution Index",
        "version": "0.1",
        "generated": datetime.date.today().isoformat(),
        "doctrine": ("Same-commit discipline: no distribution act without its index "
                     "entry. 'deposited' requires venue identifier + Rule 28 v2 "
                     "content-match. Regenerate via scripts/build_distribution_index.py; "
                     "never hand-grow."),
        "channels": CHANNELS,
        "stats": {
            "deposits_total": len(entries),
            "distributed_beyond_alexanarch": distributed,
            "planned_pending": planned_ct,
            "flagships": sum(1 for e in entries if e["class"] == "flagship"),
            "instruments": sum(1 for e in entries if e["class"] == "instrument"),
            "corpus_native": sum(1 for e in entries if e["class"] == "corpus-native"),
            "unassigned": sum(1 for e in entries if e["class"] == "unassigned"),
        },
        "entries": entries,
    }
    json.dump(idx, open(IDX, "w"), indent=1, ensure_ascii=False)
    return idx


if __name__ == "__main__":
    idx = build()
    print(json.dumps(idx["stats"], indent=1))
