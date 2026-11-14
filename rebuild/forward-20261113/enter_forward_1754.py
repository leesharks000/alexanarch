"""Enter the first forward pointer (2026-11-13): #1754 Socrates as Orthonym, the router, routes #1733 §1.8 to #1767.
Lee Sharks's rulings are quoted in the entry. Idempotent: replaces any entry with the same from/to pair."""
import json, pathlib
P = pathlib.Path(__file__).resolve().parents[2] / "data/registry.json"
reg = json.loads(P.read_text(encoding="utf-8"))
D = {d["deposit_number"]: d for d in reg["deposits"]}
E = {"date": "2026-11-13", "kind": "stands as a section", "from_deposit": 1733, "from_locus": "§1.8", "to_deposit": 1767,
     "note": "The Production of Readers (#1767) stands as §1.8 of Legitimately Many (#1733), \"Why the one divides\": the production "
             "account of the separation that §1.5 there leaves open. Routed by the Socrates as Orthonym framework hologram (#1754) for its next build, before consolidation.",
     "raised_by": "Lee Sharks (2026-11-13)",
     "ruling": "\"im seeing this as a standalone piece that is also a section of legitimately many... deposited on its own but legitimately "
               "many points forward to it\"; \"it can be added as metadata, in the same way as the errata... the content identity does not "
               "need to change to point and maintain its developing relations\"; \"the socrates as orthonym holographic frame is the place "
               "for the metadata note - its the router\"",
     "status": "recorded; the bytes and AXN of #1733, #1754 and #1767 are unchanged"}
d = D[1754]
d["forward"] = [x for x in (d.get("forward") or []) if (x.get("from_deposit"), x.get("to_deposit")) != (1733, 1767)] + [E]
P.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("entered forward pointer on #1754:", E["from_deposit"], E["from_locus"], "->", E["to_deposit"])
