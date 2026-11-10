"""Repair of 2026-11-10: the record at AXN:0C64 (classical-receptions-journal-ai-mediation-aio-20261110) made the run whole.

THE BELIEF AND ITS EVIDENCE. The record was seated at 12:36 from a paste of the run's first two turns. At 12:57 the operator pasted the same run
continued to five turns ('i went on further rounds with that aio'); the first two answers of the 12:57 paste are byte-identical to the 12:36 paste
(five_turns.py asserts it), so the two pastes are one run, and the record of the address is the run whole. At 12:59 and 13:01 he supplied the
in-text citation [1] at the two paragraphs crediting the journal; it resolves (HTTP 302) to https://www.crimsonhexagonal.org/works/034e, the
archive's page for #833. The composition therefore cites an archive-controlled source, and the record's scope, derived from its citations, moves
from external to archive.

WHAT CHANGES. The fields five_turns.py composes from the 12:57 paste replace their 12:36 values; the citation [1] enters cite_list with
archive_controlled_cites 1; scope is re-derived by the intake's own rule. The 12:36 transcript, raw paste and analysis are kept whole under
notes.first_seat. Every other field is untouched. capture_axn.py --apply then re-derives the observation's AXN (the earlier form kept in the
ledger's history), and the postflight rebakes.    python3 repair.py"""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from capture_intake import derive_scope
SLUG = "classical-receptions-journal-ai-mediation-aio-20261110"
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
reg = json.loads(REG.read_text(encoding="utf-8"))
e = [x for x in reg["entries"] if x["slug"] == SLUG][0]
first = json.loads((ROOT / "rebuild/capture-registry/intake-20261110-crj-vox-stewardship" / (SLUG + ".json")).read_text(encoding="utf-8"))
new = json.loads((H / (SLUG + ".json")).read_text(encoding="utf-8"))
assert e["transcript"] == first["transcript"] and e["turns"] == 2 and e["n_observations"] == 1, "the record stands as seated at 12:36"
assert new["q"] == e["q"] and new["surface"] == e["surface"] and new["date"] == e["date"], "the same address, surface and date"
KEYS = ["mt", "q_kind", "turns", "transcript", "transcript_raw", "transcript_class", "transcript_complete", "transcript_read", "d", "reading",
        "findings", "per_note", "related_deposits"]
e["notes"] = dict(e.get("notes") or {})
e["notes"]["first_seat"] = {"received": "2026-11-10 12:36 EST", "paste": "intake-20261110-crj-vox-stewardship/paste-classical-receptions-journal-aio.txt",
                            **{k: first[k] for k in ("turns", "transcript", "transcript_raw", "d", "reading", "findings", "mt")}}
for k in KEYS:
    e[k] = new[k]
for k in ("operator_continued", "pastes", "citation", "census", "question_for_833"):
    e["notes"][k] = new["notes"][k]
e["notes"]["repair"] = ("2026-11-10: the record made the run whole from the 12:57 paste (turns 1-2 byte-identical to the 12:36 paste); the citation [1] "
                        "at the credit resolved to the archive's page for #833 and entered cite_list; scope re-derived. "
                        "rebuild/capture-registry/repair-20261110-crj-run-whole/.")
e["cite_list"] = [{"n": 1, "site": "www.crimsonhexagonal.org", "rel": "archive_controlled", "title": "The Summarizer as Horizon of Reception (AXN:034E)",
                   "snip": None, "url": "https://www.crimsonhexagonal.org/works/034e",
                   "note": ("in-text citation [1] at both paragraphs crediting the journal (the 'horizon of reception' paragraph and section 1); supplied by "
                            "the operator as google.com/url and google.com/goto links (12:59, 13:01 EST), resolved HTTP 302 on 2026-11-10; the other cards "
                            "(Oxford Academic, Hopkins Press, www.instagram.com, Classical Reception Studies Network, Paperpal) are in the transcript as pasted, unresolved"),
                   "deposit_candidates": [833]}]
e["archive_controlled_cites"] = 1
e["scope"], e["scope_basis"] = derive_scope(e)
assert e["scope"] == "archive"
REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
print("repaired", SLUG, "turns", e["turns"], "scope", e["scope"], "|", e["scope_basis"])
