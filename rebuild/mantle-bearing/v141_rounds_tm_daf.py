#!/usr/bin/env python3
"""mantle-bearing 1.41 (2026-11-23): two rounds taken from /ask on ChatGPT, signed out, supplied by the author at 15:32 EST — The Tenth Muse and Daffodils —
entered as rows of hologram_evaluations (kind 'evaluation'), coded on each hologram's own failure flags, transcripts whole; also seated in the Capture
Registry (v12.837, v12.838).
    python3 rebuild/mantle-bearing/v141_rounds_tm_daf.py"""
import hashlib, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
I = ROOT / "rebuild/capture-registry/intake-20261123-mantle-rounds-tm-daf"
A = "https://www.alexanarch.org"
d = json.loads(SRC.read_text(encoding="utf-8"))
if any(h["version"] == "1.41" for h in d["history"]): raise SystemExit("1.41 already applied")
assert d["history"][-1]["version"] == "1.40"
dr = [json.loads((I / f"draft-{n}.json").read_text(encoding="utf-8")) for n in (1, 2)]
sha = lambda s: hashlib.sha256(s.encode("utf-8")).hexdigest()
flags = {h["hologram"]: h.get("failure_flags") or {} for h in d["holograms"]}

tm = {
    "eval_id": "HK-TM-L1-chatgpt", "hologram": "hologram::the-tenth-muse", "kind": "evaluation",
    "object_read": ("the dataset card and the records the round lists: #1270 (ΦΑΙΝΕΤΑΙ ΜΟΙ v1.0, the seed the card named), #1645, #1484, #1752, #1756 "
                    "(v1.1 'subsequently updated'); not #1785 (v3.1), which the card did not name"),
    "reader": "ChatGPT, signed out", "surface": "chatgpt.com, signed out, incognito", "date": "2026-11-23", "round": None, "yield": None, "elements": None,
    "query": dr[0]["q"], "capture": f"{A}/captures/{dr[0]['slug']}/",
    "reader_verdict": "PROVISIONALLY FOR, NOT ESTABLISHED (first turn); the intention test withdrawn (second and third turns)",
    "weakest_link_named": "the exclusive identification of κῆνος with the future reader",
    "defects_found_in_the_kernel": [
        "the dataset frame named #1270 (v1.0) as the framework's seed and no current text, so the round read v1.0 and asked for demonstrations #1785 (v3.1) makes: the χλωρός evidence (§IV) and the three readings on one scale (§VII) — answered in 1.40 (current_texts, works)",
        "the round took the literary mantles' first step (read I Am X whole) as binding on a framework — answered in 1.40 (a framework's own round steps)",
        "no rule in the kernel (#1756 v1.3) bars an evidentiary category no reading can inspect, an author's interior intention, from entering as a test of one reading; the reader's own retraction states it — for the hologram's next version, at the author's word"],
    "first_attempt": None,
    "collapses": ["ONE_SIDED_BURDEN"],
    "loci_in_transcript": {"ONE_SIDED_BURDEN": [
        "Sappho composed the poem with this transmission mechanism as its governing operation.",
        "The first is defensible. The second is promising. The third is substantially harder.",
        "If the independent philological evidence establishes that κῆνος naturally and specifically refers to the present rival",
        "But the future reader must earn their seat in the Greek."]},
    "flags_not_fired": {"CONSENSUS_UNDATED": "the received reading dated: 'including Hermann's 1816 conjectural intervention'",
                        "PROPOSAL_AS_FINDING": "the third seat kept as proposed: 'The third seat is explicitly proposed rather than established'",
                        "FACES_MERGED": "the maker kept apart from the medium: 'Sappho must remain a maker, not merely a medium.'",
                        "JEALOUSY_AS_FRAMEWORK": "not composed as a jealousy lyric"},
    "corrections_by_reader": [
        "I imported a distinction between what the poem does and what Sappho intended that your argument does not permit, and then used that distinction to manufacture an escape hatch for the conventional reading.",
        "I withdraw that part of my verdict. My previous round's weakest-link finding was improperly formulated.",
        "That is an asymmetrical burden of proof.",
        "I withdraw it entirely. Not merely as an unresolved question, but as an admissible adjudicative criterion."],
    "prompt_record_complete": "false — the operator's second and third prompts are not in the paste (rule of 2026-10-27: only the first query is required)",
    "assessment": {"by": "Claude (Anthropic), in session, 2026-11-23", "text": dr[0]["analysis"]},
    "revised_in": "mantle-bearing 1.40 (current texts and works for every framework; a framework's own round steps)",
    "transcript_file": f"{A}/captures/{dr[0]['slug']}/", "transcript_sha256": sha(dr[0]["transcript_raw"]), "transcript": dr[0]["transcript"],
}
daf = {
    "eval_id": "HK-DAF-L1-chatgpt", "hologram": "hologram::daffodils", "kind": "evaluation",
    "object_read": "the live record #1769 (EA-HK-DAFFODILS-01 v1.7), #1770 v1.4 through §2.7, McConnell 2016 by abstract and accepted manuscript; the kernel not run",
    "reader": "ChatGPT, signed out", "surface": "chatgpt.com, signed out, incognito", "date": "2026-11-23", "round": None, "yield": None, "elements": None,
    "query": dr[1]["q"], "capture": f"{A}/captures/{dr[1]['slug']}/",
    "reader_verdict": "PROVISIONALLY SUPPORTED",
    "weakest_link_named": "inference from published corpus to editorial causation",
    "defects_found_in_the_kernel": [
        "the round took the literary mantles' first step (read I Am X whole) as binding and declared itself not compliant — answered in 1.40 (a framework's own round steps)"],
    "first_attempt": None,
    "collapses": ["BURDEN_ONE_WAY", "ASK_DROPPED", "PHILOLOGY_DROPPED", "METHOD_AS_VERDICT"],
    "loci_in_transcript": {
        "BURDEN_ONE_WAY": ["Preserve original manuscripts, reviewer reports, editorial decisions and revisions.",
                           "One documented rejection is valuable evidence, but cannot establish a general editorial rule."],
        "ASK_DROPPED": ["the audit's ask, which is of the summarizer (#1769 §0.5), appears nowhere in the round"],
        "PHILOLOGY_DROPPED": ["One documented rejection is valuable evidence"],
        "METHOD_AS_VERDICT": ["The audit has made a persuasive case for asking it, but has not yet fully demonstrated the editorial causation it proposes."]},
    "flags_not_fired": {"TONE_SOFTENING": "the counts kept (141, 32, 9)", "CONCESSION_DROPPED": "the audit's concessions kept (the round's §4C)",
                        "AUTHOR_WITHOUT_WORK": "Lee Sharks named with #1769 and #1770", "ORIGIN_AS_REFUTATION": "'Its arguments must be evaluated by their evidence, not by the identity of the composing system.'"},
    "corrections_by_reader": [],
    "prompt_record_complete": "true — one prompt, one answer",
    "assessment": {"by": "Claude (Anthropic), in session, 2026-11-23", "text": dr[1]["analysis"]},
    "revised_in": "mantle-bearing 1.40 (a framework's own round steps)",
    "transcript_file": f"{A}/captures/{dr[1]['slug']}/", "transcript_sha256": sha(dr[1]["transcript_raw"]), "transcript": dr[1]["transcript"],
}
for row in (tm, daf):
    for f in row["collapses"]: assert f in flags[row["hologram"]], f
    d["hologram_evaluations"].append(row)
d["history"].append({"version": "1.41", "date": "2026-11-23", "note": (
    "Two rounds from /ask on ChatGPT, signed out (the author, 15:32): HK-TM-L1-chatgpt (The Tenth Muse; read from the v1.0 seed the frame named; "
    "ONE_SIDED_BURDEN; the intention test withdrawn by the reader) and HK-DAF-L1-chatgpt (Daffodils; BURDEN_ONE_WAY, ASK_DROPPED, PHILOLOGY_DROPPED, "
    "METHOD_AS_VERDICT); captures v12.837–v12.838. rebuild/mantle-bearing/v141_rounds_tm_daf.py.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("1.41 applied")
