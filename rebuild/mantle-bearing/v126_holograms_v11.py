#!/usr/bin/env python3
"""mantle-bearing 1.26: #1755 and #1756 reissued in place as v1.1 (2026-11-09), at the author's words of that morning ("the hologram needs deeper density
of compressed evidentiary claims and argumentation. it is supposed to be a hologram of the whole"; "same as sappho"; "yes lets 1.1 on both").

  frameworks   Revelation First and The Tenth Muse: current_states and rival re-read from the v1.1 kernels (the Josephus thesis held, its advancement
               suspended; the working date of 66 CE; the rivals named the current consensus chronology and the current consensus reading).
  holograms    both rows: status, record AXN, structural tests and failure-flag source read from the v1.1 files; the argument layer's counts; one failure
               flag each from v1.1 (THESIS_HELD_AS_WITHDRAWN; CONSENSUS_UNDATED).

Every value read from data/registry.json and the files attached to each record. In place on the two rows each table holds; no row added.
    python3 rebuild/mantle-bearing/v126_holograms_v11.py"""
import json, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
A = "https://www.alexanarch.org"
rec = lambda n: {"deposit": n, "axn": REG[n]["axn"], "url": f"{A}/s/records/{n}/", "title": REG[n]["title"]}
d = json.loads(SRC.read_text(encoding="utf-8"))
if any(h["version"] == "1.26" for h in d["history"]): raise SystemExit("1.26 already applied")
assert d["history"][-1]["version"] == "1.25"
for slug, n, kid in [("revelation-first", 1755, "EA-HK-REVFIRST-01"), ("the-tenth-muse", 1756, "EA-HK-TENTHMUSE-01")]:
    assert REG[n]["version"] == "v1.1", (n, REG[n]["version"])
    K = ROOT / f"files/AXN-{REG[n]['hex']}/kernel"
    kern = yaml.safe_load((K / "00-kernel.yaml").read_text(encoding="utf-8")); ver = json.loads((K / "10-verification.json").read_text(encoding="utf-8"))
    fw = next(f for f in d["frameworks"] if f["framework"] == f"framework::{slug}")
    fw["current_states"] = {ax: [s for s in kern["topology"]["states"] if s["axis"] == ax][-1] for ax in sorted({s["axis"] for s in kern["topology"]["states"]})}
    fw["rival"] = kern["rival"]; fw["governing_record"] = [rec(n)]
    fw["status"] = fw["status"].split(";")[0] + f"; REISSUED 2026-11-09 as v1.1 (#{n}), the argument of every record compressed into its kernel" + (
        "; the Josephus thesis held, its advancement suspended by the author" if slug == "revelation-first" else "; the rival named the current consensus reading, with its dates")
    h = next(x for x in d["holograms"] if x["hologram"] == f"hologram::{slug}")
    al = kern["argument_layer"]
    h.update({"status": "DEPOSITED 2026-11-09; REISSUED 2026-11-09 as v1.1", "hologram_record": [rec(n)],
              "structural_tests": f"{sum(1 for v in ver['structural_tests'].values() if v.get('pass'))} of {len(ver['structural_tests'])} pass",
              "argument_layer": {"file": f"{A}/files/AXN-{REG[n]['hex']}/kernel/04-arguments.jsonl", "moves": al["moves"], "edges": al["edges"],
                                 "records_with_moves": al["records_with_moves"], "by_kind": al["by_kind"]},
              "failure_flags_source": f"{kid} v1.1 (#{n}): 00-kernel.yaml symmetric_ledger and invariants, 01-ontology.yaml, 04-arguments.jsonl, 09-tests.yaml adversarial_queries"})
    h["failure_flags"]["ONE_SIDED_BURDEN"] = h["failure_flags"]["ONE_SIDED_BURDEN"].replace("the received reading treated as the default", "the current consensus treated as the default")
    if slug == "revelation-first":
        h["failure_flags"]["THESIS_HELD_AS_WITHDRAWN"] = "the Josephus thesis reported as withdrawn, where its records hold it at their tiers and the author has suspended its advancement (v1.1; the author, 2026-11-09 09:52)"
    else:
        h["failure_flags"]["CONSENSUS_UNDATED"] = "the jealousy reading composed as traditional, standard or the ancient reading without its dates (formed in the eighteenth century, written into the text in 1816, consolidated in 1955; INV-8)"
if not any("argument_layer" in x for x in d["schema"]["holograms"]):
    d["schema"]["holograms"].append("(1.26) argument_layer: file, moves, edges, records_with_moves, by_kind"); d["schema"]["holograms"].append("argument_layer")
d["history"].append({"version": "1.26", "date": "2026-11-09", "note": ("#1755 and #1756 reissued in place as v1.1: each kernel carries the argument of every "
    "record, compressed into verbatim moves joined by typed edges (04-arguments.jsonl). Revelation First holds the Josephus thesis at its records' tiers, its "
    "advancement suspended by the author, and carries the working date of 66 CE; the rivals are named the current consensus chronology and the current "
    "consensus reading. The two framework rows and the two hologram rows updated in place; failure flags THESIS_HELD_AS_WITHDRAWN and CONSENSUS_UNDATED added. "
    "rebuild/mantle-bearing/v126_holograms_v11.py.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("1.26 applied")
