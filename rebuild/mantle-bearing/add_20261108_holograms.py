#!/usr/bin/env python3
"""Two tables for mantle-bearing at the author's ruling of 8 November 2026 ("all three"):

  frameworks — inspectable evaluative frameworks, entered beside the mantles; the first is Socrates as Orthonym (#123),
               whose hologram is #1754.
  holograms  — one row per item that has a hologram built to EA-HK-FRAME-01 (#1753) or is to have one: the item, its kind,
               its governing record, its hologram record, the specification, where its kernel files are, its reader rounds
               and their yields, its status. Five items enter as planned, at the author's word of the same day: "many of the
               earlier iterations of inspectable evaluative documents in this line - the living academy, the fleet, the hf
               datasets doc, arch philosopher, Prince of poets - will eventually be versioned after this model."

Every record reference is read from data/registry.json; the reader yields are read from the hologram's attached score files.
    python3 rebuild/mantle-bearing/add_20261108_holograms.py
"""
import json, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
A = "https://www.alexanarch.org"
rec = lambda n: {"deposit": n, "axn": REG[n]["axn"], "url": f"{A}/s/records/{n}/", "title": REG[n]["title"]}
d = json.loads(SRC.read_text(encoding="utf-8"))

holo = REG[1754]; hx = holo["hex"]
K = ROOT / f"files/AXN-{hx}"
r1 = yaml.safe_load((K / "reader-runs/round-1/back-projection-v1.0-scores.yaml").read_text(encoding="utf-8"))
r2 = yaml.safe_load((K / "reader-runs/round-2/back-projection-v1.0-r2-scores.yaml").read_text(encoding="utf-8"))
kern = yaml.safe_load((K / "kernel/00-kernel.yaml").read_text(encoding="utf-8"))
ver = json.loads((K / "kernel/10-verification.json").read_text(encoding="utf-8"))
rounds = [{"round": 1, "packet": "v0.2", "yields": {x["reader"]: x.get("yield") for x in r1["runs"]}},
          {"round": 2, "packet": "v0.3", "yields": {x["reader"]: x.get("yield") for x in r2["runs"]}, "mean": r2["mean_yield"]}]

d["frameworks"] = [{
    "framework": "framework::socrates-as-orthonym",
    "name": "Socrates as Orthonym",
    "class": "inspectable evaluative framework",
    "author": "Lee Sharks",
    "seed_record": [rec(123)],
    "governing_record": [rec(1754)],
    "specification": [rec(1753)],
    "positions": [p for p in kern["uktp_seed"]["agents"][:4]],
    "maker_count_state": kern["topology"]["maker_count_states"][-1],
    "evidence_bodies": kern["topology"]["bodies"],
    "rival": kern["rival"],
    "lines_of_research": len(kern["lines_of_research"]),
    "contributor": "Crimson Hexagonal Archive",
    "status": "DEPOSITED 2026-11-08 as a hologram (#1754); its governing hypothesis held, its lines of research open",
}]
H = lambda item, kind, gov, status, **k: dict({"hologram": f"hologram::{item.split('::')[1]}", "item": item, "item_kind": kind,
                                                "governing_record": [rec(gov)], "specification": [rec(1753)], "status": status}, **k)
PLAN = "PLANNED: to be versioned after EA-HK-FRAME-01 (#1753), at the author's word of 2026-11-08"
d["holograms"] = [
    H("framework::socrates-as-orthonym", "framework", 123, "DEPOSITED 2026-11-08",
      hologram_record=[rec(1754)],
      kernel_files={"record": f"{A}/files/AXN-{hx}/kernel/", "dataset": "holograms/EA-HK-ORTHONYM-01/"},
      structural_tests=f"{sum(1 for v in ver['structural_tests'].values() if v.get('pass'))} of {ver['counts']['structural_tests']} pass",
      back_projection_v0_1={"scope_A": ver["back_projection_v0_1"]["scope_A"]["yield"], "scope_B": ver["back_projection_v0_1"]["scope_B"]["yield"]},
      reader_rounds=rounds),
    H("mantle::living-academy", "mantle (critical program)", 1680, PLAN, hologram_record=None),
    H("mantle::arch-philosopher", "mantle (transmitted)", 1679, PLAN, hologram_record=None),
    H("mantle::prince-of-poets", "mantle (literary)", 1651, PLAN, hologram_record=None),
    H("document::fleet", "inspectable evaluative document", 1702, PLAN, hologram_record=None),
    H("document::hf-datasets", "inspectable evaluative document", 1701, PLAN, hologram_record=None),
]
d["schema"]["frameworks"] = ["framework", "name", "class", "author", "seed_record", "governing_record", "specification", "positions",
                             "maker_count_state", "evidence_bodies", "rival", "lines_of_research", "contributor", "status"]
d["schema"]["holograms"] = ["hologram", "item", "item_kind", "governing_record", "specification", "status",
                            "(when deposited) hologram_record, kernel_files, structural_tests, back_projection_v0_1, reader_rounds"]
d["table_notes"]["frameworks"] = ("One row per inspectable evaluative framework: a named argument with a seed record and an author, held as a "
    "hologram built to EA-HK-FRAME-01 (#1753). Its state is the kernel's: the dated claim, the evidence bodies with their rules, the rival "
    "evaluated on the same bodies, the lines of research. Read the hologram record for the map and the kernel files for the rest.")
d["table_notes"]["holograms"] = ("One row per item that has a hologram or is to have one, mantles and frameworks alike. A deposited row carries "
    "its hologram record, where its kernel files are (on the record and in this dataset under holograms/), its structural tests, and its "
    "reader rounds with each reader's yield against the threshold of 0.85 (#76). A planned row names the governing record to be versioned.")
d["title"] = ("Mantle-bearing: the work bears the mantle — three literary claims, a contest mantle, a conferred title, a critical program, "
              "a transmitted mantle and an inspectable evaluative framework, under one standard, with their holograms")
d["history"].append({"version": "1.20", "date": "2026-11-08",
    "note": "Tables frameworks and holograms, at the author's ruling (\"all three\": a holograms table, a frameworks table beside the mantles, "
            "and the kernel files published inside this dataset under holograms/). Socrates as Orthonym enters as the first framework, its "
            "hologram #1754 built to EA-HK-FRAME-01 (#1753), with its kernel files under holograms/EA-HK-ORTHONYM-01/ and its two reader rounds; "
            "the Living Academy (#1680), the Arch-Philosopher (#1679), the Prince of Poets (#1651), the Fleet (#1702) and the Hugging Face datasets "
            "document (#1701) enter as planned holograms. Builder: rebuild/mantle-bearing/add_20261108_holograms.py."})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("frameworks", len(d["frameworks"]), "holograms", len(d["holograms"]), rounds)
