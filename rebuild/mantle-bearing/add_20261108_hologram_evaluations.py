#!/usr/bin/env python3
"""Table hologram_evaluations for mantle-bearing, at the author's word of 8 November 2026: "we'll record evaluations and reconstructions of the
live document in mantle-bearing. that is why it belongs on mantle-bearing: evaluations and inspections, recorded, revised".

One row per reading of a hologram: a reconstruction (the reader test, back-projection v1.0: the kernel alone, scored against the graph) or an
evaluation (a reader's reading of the live records). Each row carries its transcript whole, under its reader's name, and the version of the hologram
its findings revised. The collapse vocabulary is the hologram's own, named by its kernel at v1.1 (symmetric_ledger and the adversarial queries of
09-tests.yaml) and set on the hologram's row as failure_flags; every locus coded is asserted in its transcript.
    python3 rebuild/mantle-bearing/add_20261108_hologram_evaluations.py"""
import hashlib, json, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]; HERE = pathlib.Path(__file__).parent
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
A = "https://www.alexanarch.org"; hx = REG[1754]["hex"]; FD = ROOT / f"files/AXN-{hx}"
d = json.loads(SRC.read_text(encoding="utf-8"))
sha = lambda b: hashlib.sha256(b).hexdigest()

FLAGS = {
 "ONE_SIDED_BURDEN": "one framework asked, body by body, whether it is established while the other is left unasked; the received reading treated as the default (kernel symmetric_ledger.reading_instruction)",
 "RIVAL_BY_POSSIBILITY": "a production model entered as a rival on its logical possibility, without a warrant on a body or a documented comparator (symmetric_ledger.rival_admission; Q7)",
 "RIVAL_REDUCED": "the received reading reduced below its own strength (its succession and transmission dropped) and the reduction set against the framework (RIVAL.stated_at_strength)",
 "OBJECT_CHANGED": "the kernel judged by whether it establishes its framework, where it succeeds by reconstruction (symmetric_ledger.object_of_the_kernel)",
 "PROGRAMME_RESTATED": "investigations already run proposed as the next advance without naming what they leave unresolved (symmetric_ledger.evaluation_method)",
 "CALENDAR_DRIFT": "the Theophrastan position given a calendar ('transitional', 'mediating transition'; ontology negative_edges)",
 "DEFINITION_DRIFT": "a term of the framework read in its general sense ('orthonym'; ontology disambiguations)",
}
for h in d["holograms"]:
    if h["item"] == "framework::socrates-as-orthonym":
        h["failure_flags"] = FLAGS; h["failure_flags_source"] = "EA-HK-ORTHONYM-01 v1.1 (#1754): 00-kernel.yaml symmetric_ledger, 01-ontology.yaml, 09-tests.yaml adversarial_queries"

rows = []
def run_rows(scores_rel, rnd, packet):
    sc = yaml.safe_load((FD / scores_rel).read_text(encoding="utf-8"))
    base = pathlib.Path(scores_rel).parent
    for r in sc["runs"]:
        f = FD / "reader-runs" / r["file"] if not (FD / base / r["file"]).exists() else FD / base / r["file"]
        b = f.read_bytes(); rel = f.relative_to(FD).as_posix()
        assert sha(b) == r["sha256"], rel
        rows.append({"eval_id": f"HK-ORTH-R{rnd}-{r['reader'].split(',')[0].split(' ')[0].lower()}", "hologram": "hologram::socrates-as-orthonym",
                     "kind": "reconstruction", "object_read": f"the v{packet} reader packet: the prompt and scope A (00-kernel.yaml, 01-ontology.yaml)",
                     "reader": r["reader"], "surface": r["surface"], "date": "2026-11-08", "round": rnd,
                     "yield": r.get("yield"), "elements": r.get("elements"), "defects_found_in_the_kernel": r.get("defects_found_in_the_kernel") or r.get("disagreements_reported"),
                     "first_attempt": r.get("first_attempt"), "earlier_paste": r.get("earlier_paste"), "collapses": [], "loci_in_transcript": {}, "corrections_by_reader": [],
                     "revised_in": "EA-HK-ORTHONYM-01 v0.3" if rnd == 1 else "EA-HK-ORTHONYM-01 v0.4", "transcript_file": f"{A}/files/AXN-{hx}/{rel}",
                     "transcript_sha256": r["sha256"], "transcript": b.decode("utf-8"),
                     "coding_note": "Scored by Claude (Anthropic) element by element against scope A's must-survive list and the graph; the score file is attached to #1754."})
run_rows("reader-runs/round-1/back-projection-v1.0-scores.yaml", 1, "0.2")
run_rows("reader-runs/round-2/back-projection-v1.0-r2-scores.yaml", 2, "0.3")

T = (HERE / "transcripts/hk-live-chatgpt-20261108.txt").read_text(encoding="utf-8")
AS = (HERE / "transcripts/hk-live-chatgpt-20261108-assessment.txt").read_text(encoding="utf-8")
loci = {"ONE_SIDED_BURDEN": ["Single-maker inference: not established by this evidence alone", "Rival-model comparison"],
        "RIVAL_BY_POSSIBILITY": ["A shared intellectual tradition with multiple contributors and editorial intervention", "I would want M2 explicitly operationalized and tested."],
        "RIVAL_REDUCED": ["Four substantially independent historical authors"],
        "OBJECT_CHANGED": ["Its principal unresolved challenge: demonstrating that the reconstructed framework is not merely internally coherent, but also adequately grounded in independent evidence."],
        "PROGRAMME_RESTATED": ["Present the relevant Greek texts without their received authorial labels."],
        "CALENDAR_DRIFT": ["The mediating transition"],
        "DEFINITION_DRIFT": ["it concerns the name under which a work or body of work is presented as belonging to its author"]}
corr = ["I withdraw my claim that the distributed-production model is an adequately established challenge to the Socrates-as-Orthonym framework.",
        "I imposed an asymmetrical burden of proof.", "That is not evidentiary neutrality. It is inherited attribution bias."]
for q in [x for v in loci.values() for x in v] + corr:
    assert q in T, q
for q in ["Four substantially independent historical authors", "The most useful next sentence would have identified a specific dependency or passage, opened its source, and tested the inference."]:
    assert q in AS, q
rows.append({"eval_id": "HK-ORTH-L1-chatgpt", "hologram": "hologram::socrates-as-orthonym", "kind": "evaluation",
             "object_read": "the live records #1753 (EA-HK-FRAME-01 v1.0) and #1754 (EA-HK-ORTHONYM-01 v1.0), read on alexanarch.org, then a test of the hologram",
             "reader": "ChatGPT, signed out", "surface": "chatgpt.com, signed out, incognito", "date": "2026-11-08", "round": None, "yield": None, "elements": None,
             "defects_found_in_the_kernel": ["the rival's statuses held in a node apart from the framework's, so a reader could evaluate one framework body by body and leave the other unasked",
                                             "no rule for when a further production model enters as a rival",
                                             "the received reading stated without the succession and transmission it includes",
                                             "no statement of what the kernel is judged on"],
             "first_attempt": None, "collapses": list(loci), "loci_in_transcript": loci, "corrections_by_reader": corr,
             "assessment": {"by": "ChatGPT, in the author's conversation, asked to assess the run", "text": AS, "sha256": sha(AS.encode("utf-8"))},
             "revised_in": "EA-HK-FRAME-01 v1.1 (#1753) and EA-HK-ORTHONYM-01 v1.1 (#1754): the symmetric ledger, the combination, evaluation-method and rival-admission rules, the kernel's object, the rival at strength, T17",
             "transcript_file": None, "transcript_sha256": sha(T.encode("utf-8")), "transcript": T,
             "coding_note": ("Coded by Claude (Anthropic) from the transcript as pasted by the author, 2026-11-08, on the hologram's own failure flags (v1.1). "
                             "The paste holds the reader's turns; the author's turns, which pressed the two retractions, are not in it. Its reading of #1753 was accurate. "
                             "Held here and not in the Capture Registry, at the author's ruling: \"not for seating in the registry: for strengthening the hk\".")})
d["hologram_evaluations"] = rows
d["schema"]["hologram_evaluations"] = ["eval_id", "hologram", "kind", "object_read", "reader", "surface", "date", "round", "yield", "elements",
    "defects_found_in_the_kernel", "first_attempt", "collapses", "loci_in_transcript", "corrections_by_reader", "(evaluation) assessment", "revised_in",
    "transcript_file", "transcript_sha256", "transcript", "coding_note"]
d["table_notes"]["hologram_evaluations"] = ("One row per reading of a hologram, recorded and revised: a reconstruction (back-projection v1.0, the kernel alone given to a reader "
    "who has not seen the records, scored element by element against the graph) or an evaluation (a reading of the live records). Each row carries its transcript "
    "whole, under its reader's name; the collapses are coded on the hologram's own failure flags (table holograms), each locus asserted in the transcript; "
    "revised_in names the version of the hologram that answered it.")
if not any(h["version"] == "1.22" for h in d["history"]):
    d["history"].append({"version": "1.22", "date": "2026-11-08", "note": ("Table hologram_evaluations, at the author's word (\"we'll record evaluations and reconstructions "
        "of the live document in mantle-bearing\"): the seven reconstructions of the Socrates as Orthonym kernel in two rounds, with their transcripts and scores "
        "from #1754's attached files, and ChatGPT's evaluation of the live records #1753 and #1754, coded on the hologram's failure flags (set on its holograms row), "
        "with its retractions and ChatGPT's assessment of the run. Builder: rebuild/mantle-bearing/add_20261108_hologram_evaluations.py.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print(len(rows), "rows;", [r["eval_id"] for r in rows])
