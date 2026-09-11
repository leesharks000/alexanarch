#!/usr/bin/env python3
"""build_potential_atlas.py — EA-ATLAS-01, the potential dataset atlas.

WHAT THIS IS. The archive publishes what it holds. This publishes what it CAN
GENERATE: each possible dataset as an addressable object with an identity, a
specification, a status, and the articulation through which it was named — before
its rows exist.

IT IS EMITTED, NOT AUTHORED. Every entry is derived from something already on disk:
a realized rhizome's spore, or a stolon that named an adjacent body without building
it. Nothing here is a wish list. A stolon is a proposed dataset that has already been
specified far enough to say where it starts, what relation it follows, and why.

STATUS IS NOT A RANKING. It states what kind of availability is being claimed:

    proposed    named, with an articulation, no specification
    specified   inputs, operations and conditions explicit
    executable  an implementation exists
    realized    a run produced an output
    validated   the output passed named checks

AND THE ATLAS RECORDS CONTRACTION, which is the part an ordinary dataset catalogue
has no place for. A specification can become unrealizable because its material was
removed. That is not a failed possibility; it is evidence that the composition layer
can shrink the space of what is generable, and it belongs here with the same
evidentiary weight as a realization. The archive's June 2026 termination is the
reason this field exists.

THREE IDENTITIES ARE KEPT SEPARATE, per the provenance argument: the specification,
the execution, and the output. Two outputs with identical rows and different
histories are not the same object, and deduplicating them would erase the history.
"""
import json, pathlib, datetime, hashlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data/potential-atlas.json"
RHI = ROOT / "rhizomes"


def spec_id(name):
    return "potential:" + name


def main():
    families, relations = [], []

    # ---- REALIZED: every rhizome that has a spore
    for sp in sorted(RHI.glob("*/spore.json")):
        s = json.loads(sp.read_text(encoding="utf-8"))
        nid = spec_id(s["rhizome"])
        families.append({
            "id": nid,
            "rhizome_id": s.get("rhizome_id"),
            "kind": "dataset_family",
            "status": "realized",
            "title": s["rhizome"].replace("-", " "),
            "parent": s.get("parent"),
            "topology": s.get("topology"),
            "unit": "node and typed edge",
            "specification": {
                "seed_mode": s.get("seed_mode"),
                "selection": s.get("selection"),
                "core_depth": s.get("core_depth"),
                "frontier_depth": s.get("frontier_depth"),
            },
            "generation": {"recipe": s.get("generator"), "execution_status": "run"},
            "realization": {"counts": s.get("counts"), "generated": s.get("generated"),
                            "source_commit": s.get("source_commit")},
            "articulated_by": "operator-directed, 2026-09-10",
            "contraction": None,
        })

        # ---- PROPOSED: each stolon names an adjacent body, with its articulation
        st = sp.parent / "stolons.jsonl"
        if st.exists():
            for line in st.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                x = json.loads(line)
                pid = spec_id(x["to_rhizome"])
                if any(f["id"] == pid for f in families):
                    continue
                families.append({
                    "id": pid,
                    "rhizome_id": None,
                    "kind": "dataset_family",
                    "status": "proposed",
                    "title": x["to_rhizome"].replace("-", " "),
                    "parent": s.get("parent"),
                    "topology": None,
                    "unit": None,
                    "specification": {"seed_mode": None, "selection": None,
                                      "core_depth": None, "frontier_depth": None},
                    "generation": {"recipe": None, "execution_status": "not_run"},
                    "realization": None,
                    # THE ARTICULATION IS THE POINT. A proposed dataset that cannot say
                    # how it was named is a wish; one that can is an address with
                    # constraints attached, which later work can take up or depart from.
                    "articulated_by": {"from_node": x["from"], "predicate": x["predicate"],
                                       "named_in": s.get("rhizome_id"), "note": x.get("note")},
                    "contraction": None,
                })
                relations.append({"source": nid, "relation": "advertises", "target": pid,
                                  "via": x["predicate"], "basis": "stolon"})

    # ---- CONTRACTION: what the archive currently cannot generate, and why
    reg = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]
    unseated = [d["deposit_number"] for d in reg
                if (d.get("body_status") or {}).get("recovery_status") == "PASS_COMPLETE_TEXT_NOT_SEATED"]
    nonactive = [d["deposit_number"] for d in reg if (d.get("status") or "ACTIVE") not in ("ACTIVE", "CANONICAL")]

    constraints = [
        {"id": "constraint:unseated-text",
         "what": "Deposits whose record declares a work and whose canonical bytes are metadata only.",
         "count": len(unseated),
         "blocks": "any family whose unit requires full text of an affected deposit",
         "evidence": "registry body_status.recovery_status == PASS_COMPLETE_TEXT_NOT_SEATED",
         "reversible": True,
         "note": "Detected 2026-07-31 and unrepaired for six weeks on the one case examined (#1095, seated as #1606). The text may exist elsewhere in the repository; unseated is not lost."},
        {"id": "constraint:severed-external-doi",
         "what": "Records severed from their original repository in the June 2026 termination.",
         "count": 1136,
         "blocks": "any family requiring resolution through the original registrar",
         "evidence": "data/tombstones — the kill ledger",
         "reversible": False,
         "note": "THE ORIGINATING REASON THIS FIELD EXISTS. The archive re-identified and re-routed; a DOI resolution index maps all 1,817 DOIs, preserved and severed, to current locations. The possibility was contracted at one registrar and restored at another, and both facts are part of the record."},
        {"id": "constraint:non-active-endpoint",
         "what": "Deposits that are superseded, withdrawn, draft, or preserved as historical seed.",
         "count": len(nonactive),
         "blocks": "families that select only on ACTIVE status",
         "evidence": "registry status field; relations ledger marks 204 edges with a non-current endpoint",
         "reversible": False,
         "note": "Not a defect. A superseded record is still addressable and still generable FROM; what contracts is the set of families that silently assume currency."},
    ]

    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    doc = {
        "maxim": "all things are now lawful to you in christ jesus",
        "$schema": "https://www.alexanarch.org/api/schemas/potential-atlas.schema.json",
        "atlas_id": "EA-ATLAS-01",
        "version": "0.1",
        "what": "The space of datasets this archive can generate, published as addressable objects before their rows exist.",
        "emitted_not_authored": ("Every entry derives from something on disk: a realized rhizome's spore, or a stolon "
                                 "that named an adjacent body without building it. Nothing here is a wish list."),
        "status_vocabulary": {
            "proposed": "named, with an articulation recorded, no specification",
            "specified": "inputs, operations and conditions explicit",
            "executable": "an implementation exists",
            "realized": "a run produced an output",
            "validated": "the output passed named checks",
        },
        "status_is_not_a_ranking": ("These state what kind of availability is being claimed, not intellectual worth. "
                                    "A failed generation and an empty result are also data about the space."),
        "three_identities": ("Specification, execution and output are distinct. Two outputs with identical rows and "
                             "different histories are not the same object; deduplicating them would erase the history "
                             "the archive exists to keep."),
        "generated": ts,
        "counts": {"families": len(families),
                   "by_status": dict(collections.Counter(f["status"] for f in families)),
                   "relations": len(relations),
                   "constraints": len(constraints)},
        "families": families,
        "relations": relations,
        "contraction": constraints,
        "not_yet_modelled": [
            "Grammar records — what counts as an object under DOI-anchor, neural annotation, mesh-distributed, post-singular authorship, holographic deposit, post-retrieval. The Forward Library (#1447) specifies these; the atlas does not yet carry them, and they are not views of one object but distinct ontologies.",
            "Translations between grammars, and what each loses. A consultation becoming a citation is not a format conversion.",
            "Parameter domains as enumerable spaces rather than fixed values.",
            "Operation families — the atlas currently maps selections. A family that generates alignments, contrasts or new text exceeds the power set of existing records and needs its own space.",
        ],
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"EA-ATLAS-01 v0.1 — {len(families)} families "
          f"({', '.join(f'{k}={v}' for k, v in doc['counts']['by_status'].items())}), "
          f"{len(relations)} relations, {len(constraints)} contraction constraints")
    for c in constraints:
        print(f"  contraction: {c['id']:34} {c['count']:>5} · reversible={c['reversible']}")


if __name__ == "__main__":
    main()
