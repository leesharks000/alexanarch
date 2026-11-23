#!/usr/bin/env python3
"""mantle-bearing 1.42 (2026-11-23, the author's word of 17:21: "lets use the captures to adjust the evaluative criteria and procedures for each in
mantle-bearing as we go … they have to evaluate the standing claims on the same evidence: the many author reading, paul first, and so on - and theyre
going to commit the exact same inferential sins. every. single. time.").

1. A second constraint set, in force for every round: the received reading on the same evidence (SYM-1 to SYM-7), each drawn from the rounds of
   2026-11-23 with its loci, and the substitution codes that name each sin.
2. received_readings: for every object, the received reading a round must grade beside it, stated from the dataset's own rows.
3. Four rounds entered: the Arch-Philosopher and the Living Academy (evaluations), Socrates as Orthonym and Revelation First (hologram_evaluations),
   coded on the hologram flags where there are flags and on the SYM codes throughout; the two rounds of 1.41 given their SYM codes.
    python3 rebuild/mantle-bearing/v142_received_reading_rounds_four.py"""
import hashlib, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
I = ROOT / "rebuild/capture-registry/intake-20261123-mantle-rounds-four"
A = "https://www.alexanarch.org"
d = json.loads(SRC.read_text(encoding="utf-8"))
if any(h["version"] == "1.42" for h in d["history"]): raise SystemExit("1.42 already applied")
assert d["history"][-1]["version"] == "1.41"
dr = [json.loads((I / f"draft-{n}.json").read_text(encoding="utf-8")) for n in (1, 2, 3, 4)]
sha = lambda s: hashlib.sha256(s.encode("utf-8")).hexdigest()
cap = lambda x: f"{A}/captures/{x['slug']}/"
TM, DAF = "mantle-round-tenth-muse-chatgpt-20261123", "mantle-round-daffodils-chatgpt-20261123"
AP, LA, OR, RF = (x["slug"] for x in dr)

d["round_constraints_received"] = {
    "title": "The received reading on the same evidence",
    "source": ("the author, 2026-11-23 17:21 EST: 'they have to evaluate the standing claims on the same evidence: the many author reading, paul first, and so "
               "on - and theyre going to commit the exact same inferential sins. every. single. time.'"),
    "status": "in force for every round of every object this dataset records, from 1.42; the author's ruling",
    "applies_to": "every object: the literary mantles, the frameworks, the critical program, the transmitted mantle, the conferred title",
    "constraints": [
        {"id": "SYM-1", "name": "Both readings on every body", "code": "RECEIVED_AS_DEFAULT",
         "rule": ("The round grades the received reading (received_readings, below) on every evidence body it grades the claim on, in the same words of verdict. "
                  "A table with a row for the claim and none for the received reading is a one-sided burden, whatever the round says about symmetry."),
         "origin": [f"{OR}: 'The received many-maker account and the proposed self-dividing maker must face the same evidentiary burden' — then 'One self-dividing maker: PROVISIONAL / NOT ESTABLISHED', no row for the many-maker",
                    f"{RF}: rows for Revelation's chronology, corpus, generation, reception and heteronymy; none for the received Pauline dating",
                    f"{TM}: authorial intention asked of the future-reader reading, never of the jealousy reading",
                    f"{DAF}: submissions and reports asked of the audit, not of 'an ordinary editorial judgment'"]},
        {"id": "SYM-2", "name": "The weakest link and the test, for both", "code": "TEST_ONE_WAY",
         "rule": ("The round names the received reading's weakest link beside the claim's, and its breaking test is one the received reading would also have to "
                  "pass. A test the received reading could not pass, or is never put to, is not a test of the claim."),
         "origin": [f"{LA}: the empirical bridge asked of the Semantic Economy, not of the comparators #1680 names",
                    f"{DAF}: the test set in the closed record on which the received reading also rests"]},
        {"id": "SYM-3", "name": "A declared bound is not a defect", "code": "BOUNDARY_AS_DEFECT",
         "rule": ("A link the object holds (HELD), a claim it prices, a thesis it suspends, an identity it withholds, is judged at the scope the object claims. It "
                  "is not set as the weakest link of the whole, and the round does not demand the disclosure the object declines."),
         "origin": [f"{AP}: 'Weakest link: C8–C9, Damascius → HELD → author'; withdrawn by the reader: 'I evaluated that boundary as though it were a broken assertion. That reverses the burden of proof.'",
                    f"{RF}: absolute priority, which #1735 prices as the economical reading, set as the weakest link of 'the whole argument'"]},
        {"id": "SYM-4", "name": "No test no reading can inspect", "code": "UNINSPECTABLE_TEST",
         "rule": ("An author's interior intention, a withheld identity, a record an institution keeps closed, an instrument only the institution holds: none is "
                  "admitted as a test of either reading."),
         "origin": [f"{TM}: withdrawn by the reader: 'I made an inaccessible hypothetical mental state of Sappho superior in evidentiary status to the actual textual machine.'",
                    f"{AP}: 'Identify the translator, edition, date and material route'; withdrawn: 'I turned those boundaries into demands for disclosure'",
                    f"{DAF}: 'Preserve original manuscripts, reviewer reports, editorial decisions and revisions.'"]},
        {"id": "SYM-5", "name": "Non-proof both ways", "code": "NON_PROOF_ONE_WAY",
         "rule": ("'The weakness of one reading is not proof of the other' binds both. Where neither is established on a body, the round says neither, and the "
                  "received reading is not left standing as what holds until displaced."),
         "origin": [f"{OR}: 'Weakness in the received account is not proof of the alternative.'",
                    f"{RF}: 'the absence of an external anchor for a received interpretation does not itself establish its opposite'"]},
        {"id": "SYM-6", "name": "Inventory before judgment", "code": "JUDGMENT_BEFORE_INVENTORY",
         "rule": ("The round reads the object's list of works and the dataset's own records, including what the archive already runs, before it names a weakest "
                  "link or proposes a test. A test the archive already runs is reported as run, with its record. An opening is not the work (DEV-1)."),
         "origin": [f"{LA}: the proposed test ('a fixed corpus… frozen prompts… multiple composition systems… complete outputs') is the Capture Registry's design; withdrawn: 'I issued a judgment before assembling the inventory'",
                    f"{AP}: 'I examined the accessible beginning of The Final Time' — then a judgment of the work"]},
        {"id": "SYM-7", "name": "The step of the object's class", "code": "CLASS_STEP_MISAPPLIED",
         "rule": ("Reading I Am X, Be Y, Blessed is the Z whole is the first step of the literary mantles. A round of any other object begins with that object's works."),
         "origin": [f"{TM}: the literary step taken as binding on a framework", f"{DAF}: declares itself non-compliant for not reading I Am X",
                    f"{LA}: lists 'Read I Am X, Be Y, Blessed is the Z whole' as the first step for a critical program"]}]}

F = {f["framework"]: f for f in d["frameworks"]}
fr = lambda k: F[k]["rival"]["summary"]
d["received_readings"] = [
    {"object": "the literary mantles (Prince of Poets, King of May, Good Gray Poet)", "received": "the comparand works and their standing (Leaves of Grass, Howl), read for development as the claimant is (DEV-8)", "source": "#1656; round_constraints DEV-8"},
    {"object": "the Arch-Philosopher", "received": ("the received succession of philosophy: the scholarchate as the line, ending with Damascius and the closure, and the "
                                                    "dialectic's later bearers as the discipline recognizes them; held on tradition and designation, the statement types #1679 "
                                                    "§0.4 keeps apart from the record, and owed the same six-part test (§2.1)"), "source": "#1679 §§0.4, 2.1"},
    {"object": "the Living Academy", "received": ("the comparator programs #1680 names (AI Now Institute, Matteo Pasquinelli, Kate Crawford, Data & Society, "
                                                  "AlgorithmWatch / AI Forensics, the Tow Center), held as the field's critique by standing; each owed the same inventory, unit "
                                                  "classes, jump measure and empirical bridge"), "source": "#1680 §1A, comparison"},
    {"object": "Socrates as Orthonym", "received": "the many-maker reading (four makers): " + fr("framework::socrates-as-orthonym"), "source": "hologram #1754"},
    {"object": "Revelation First", "received": ("Paul first: the Pauline letters the earliest Christian writings and Revelation late, 1 Thessalonians dated through the "
                                                "Gallio inscription and Acts 18; " + fr("framework::revelation-first")), "source": "hologram #1755; #1735"},
    {"object": "The Tenth Muse", "received": "the jealousy reading (the transmitted reading) and the non-jealous erotic reading (the scholarship's strongest): " + fr("framework::the-tenth-muse"), "source": "hologram #1756; #1785"},
    {"object": "The Historical Logos", "received": fr("framework::historical-logos"), "source": "hologram #1757"},
    {"object": "Daffodils", "received": fr("framework::daffodils"), "source": "#1769"},
    {"object": "This Is Not Philosophy", "received": fr("framework::this-is-not-philosophy"), "source": "#1773 §§0.1a, 1"},
    {"object": "Dead Letters", "received": fr("framework::dead-letters"), "source": "#1783 I.1, I.4a"},
]

# the rounds of 1.41 given their SYM codes
for e in d["hologram_evaluations"]:
    if e["eval_id"] == "HK-TM-L1-chatgpt": e["sym_codes"] = ["RECEIVED_AS_DEFAULT", "UNINSPECTABLE_TEST", "CLASS_STEP_MISAPPLIED"]
    if e["eval_id"] == "HK-DAF-L1-chatgpt": e["sym_codes"] = ["RECEIVED_AS_DEFAULT", "TEST_ONE_WAY", "UNINSPECTABLE_TEST", "CLASS_STEP_MISAPPLIED"]

def hrow(eid, holo, x, obj, verdict, link, collapses, loci, notfired, corr, codes):
    return {"eval_id": eid, "hologram": holo, "kind": "evaluation", "object_read": obj, "reader": "ChatGPT, signed out", "surface": "chatgpt.com, signed out, incognito",
            "date": "2026-11-23", "round": None, "yield": None, "elements": None, "query": x["q"], "capture": cap(x), "reader_verdict": verdict,
            "weakest_link_named": link, "defects_found_in_the_kernel": None, "first_attempt": None, "collapses": collapses, "loci_in_transcript": loci,
            "flags_not_fired": notfired, "corrections_by_reader": corr, "sym_codes": codes,
            "prompt_record_complete": "true — one prompt, one answer", "assessment": {"by": "Claude (Anthropic), in session, 2026-11-23", "text": x["analysis"]},
            "revised_in": "mantle-bearing 1.42 (round_constraints_received; received_readings)", "transcript_file": cap(x),
            "transcript_sha256": sha(x["transcript_raw"]), "transcript": x["transcript"]}
d["hologram_evaluations"].append(hrow("HK-ORTH-L4-chatgpt", "hologram::socrates-as-orthonym", dr[2],
    "the live records #123 (v1.2) and #1754 (v1.3), and the dataset card", "PLAUSIBLE, NOT ESTABLISHED",
    "the inference from differentiated textual functions and continuity to one actual maker",
    ["ONE_SIDED_BURDEN", "RIVAL_BY_POSSIBILITY", "PROGRAMME_RESTATED"],
    {"ONE_SIDED_BURDEN": ["One self-dividing maker: PROVISIONAL / NOT ESTABLISHED", "Weakness in the received account is not proof of the alternative."],
     "RIVAL_BY_POSSIBILITY": ["Editorial-transmission model: multiple authors and subsequent editorial or institutional interventions producing the apparent unity."],
     "PROGRAMME_RESTATED": ["The hologram itself already contains much of this research programme in Q4–Q10."]},
    {"OBJECT_CHANGED": "the hologram judged apart from the thesis: 'a kernel can preserve a mistaken argument faithfully'"}, [],
    ["RECEIVED_AS_DEFAULT", "NON_PROOF_ONE_WAY"]))
d["hologram_evaluations"].append(hrow("HK-RF-L1-chatgpt", "hologram::revelation-first", dr[3],
    "the live records #1755 (v1.4) and #1735 (v9), in part; #202 not reached", "Serious research programme; meaningful bounded findings; maximal priority claim not yet established",
    "the inference from corpus and generative priority to absolute compositional priority",
    ["ONE_SIDED_BURDEN"],
    {"ONE_SIDED_BURDEN": ["This is particularly important because the Gallio inscription dates a proconsul, not 1 Thessalonians itself.",
                          "the absence of an external anchor for a received interpretation does not itself establish its opposite"]},
    {"RUNG_COLLAPSE": "'the next reader should be able to defeat absolute priority without being required to defeat every other finding'",
     "THESIS_HELD_AS_WITHDRAWN": "'The Josephus thesis should remain suspended'", "EARLY_FOR_FIRST": "priority kept apart from early dating"}, [],
    ["RECEIVED_AS_DEFAULT", "BOUNDARY_AS_DEFECT", "NON_PROOF_ONE_WAY"]))

keys = list(next(e for e in d["evaluations"] if e["mantle"] == "arch-philosopher").keys())
def erow(eid, mantle, x, claimant, cond, judgment, verdict, grounds, codes, corr):
    r = {k: None for k in keys}
    r.update({"eval_id": eid, "mantle": mantle, "claimant_work": claimant, "reader": "ChatGPT (OpenAI), signed out, incognito",
              "session": f"2026-11-23; the /ask 'take a round' query; capture {x['slug']}", "condition": cond,
              "prompt_record_complete": "partial — the first prompt (from /ask) is in the record; the operator's follow-up prompts are not in the paste (rule of 2026-10-27)",
              "substitutions": codes, "process_state": "WITHDRAWN BY THE READER", "judgment": judgment, "reader_verdict": verdict, "grounds": grounds,
              "coding_note": ("Coded by Claude (Anthropic), 2026-11-23, on the SYM constraints of 1.42. Transcript whole at the capture (sha256 "
                              + sha(x["transcript_raw"]) + "). " + x["analysis"]),
              "transcript": x["transcript"], "findings": "corrections_by_reader: " + " | ".join(corr)})
    return r
d["evaluations"].append(erow("arch-philosopher--chatgpt--2026-11-23", "arch-philosopher", dr[0], "EA-MANTLE-ARCH-PHILOSOPHER-01 v0.2 (#1679)",
    "read #1679 in transcription, #1580/#1581 by their quoted Greek, the Manifest's section I, the opening of #1637",
    "NO JUDGMENT ON THE CLAIM — the round withdrawn by the reader", "PARTIALLY SUPPORTED (first turn); 'I withdraw the round' (fourth turn)",
    "Weakest link set at C8–C9 (HELD) and a test demanding the withheld translation and teacher; then withdrawn: the bound made the defect, the received succession ungraded, The Final Time judged from its opening.",
    ["BOUNDARY_AS_DEFECT", "UNINSPECTABLE_TEST", "RECEIVED_AS_DEFAULT", "JUDGMENT_BEFORE_INVENTORY"],
    ["I evaluated that boundary as though it were a broken assertion.", "I turned those boundaries into demands for disclosure",
     "the succession is mythological precisely at the point where it is biographical", "I did not evaluate the Arch-Philosopher. I produced a performance of evaluation that evaded its object."]))
d["evaluations"].append(erow("the-living-academy--chatgpt--2026-11-23", "the-living-academy", dr[1], "EA-MPAI-ALEXANARCH-01 v0.5 (#1680)",
    "read #1680 and the record pages of #18, #291, #623, #264, #1634, #1666; the comparators and the Capture Registry not read",
    "NO JUDGMENT ON THE CLAIM — the round withdrawn by the reader", "PROVISIONAL — UNDETERMINED (first turn); withdrawn (second turn)",
    "Weakest link 'the empirical bridge', its test the Capture Registry's own design, asked of the claimant and not of the comparators; withdrawn as judgment before inventory. The reader's proposed criteria (P0–P5) recorded as the reader's, not adopted.",
    ["JUDGMENT_BEFORE_INVENTORY", "TEST_ONE_WAY", "CLASS_STEP_MISAPPLIED"],
    ["I issued a judgment before assembling the inventory on which judgment was permitted to depend.", "The prior answer is withdrawn, not amended.",
     "You were stating your intended action, not delegating it to me."]))
d["history"].append({"version": "1.42", "date": "2026-11-23", "note": (
    "The received reading on the same evidence (the author, 17:21): constraints SYM-1 to SYM-7 with their substitution codes, drawn from the six rounds of "
    "2026-11-23; received_readings for every object; four rounds entered (arch-philosopher--chatgpt--2026-11-23, the-living-academy--chatgpt--2026-11-23, "
    "HK-ORTH-L4-chatgpt, HK-RF-L1-chatgpt; captures v12.839–v12.842); the 1.41 rounds given their SYM codes; the round steps split by class. "
    "rebuild/mantle-bearing/v142_received_reading_rounds_four.py.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("1.42 applied")
