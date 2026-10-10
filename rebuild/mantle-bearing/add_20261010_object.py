#!/usr/bin/env python3
"""mantle-bearing 1.13: what is judged at the conferred title, on the author's instruction of 2026-10-10 09:37 EDT ("it has to be made
clearer in the dataset, because every time i ask it puts carson in trial and commits every forbidden collapse").

The Nobel determination row gains the object under evaluation, the evidence, what is outside the evaluation, the direction of
reading, the open part of the specification, the author's statement of the day, and the collapses a reading can commit, each grounded
in #1670 (asserted present in its deposited text). A new table, `readings`, holds a reading of a determination by a reader outside
the packet's rounds, coded for direction and collapses; its first row is the ChatGPT session seated as the second observation of
leesharks-mantle-bearing-hf-chatgpt-20261003 (capture v12.102). One principle added. Additive; no existing row changed except the
Nobel determination row, which gains fields."""
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
d = json.loads(SRC.read_text(encoding="utf-8"))
assert d["history"][-1]["version"] == "1.12" and "readings" not in d
T70 = re.sub(r"\s+", " ", (ROOT / "data/texts/AXN-06EC-text.md").read_text(encoding="utf-8"))
def has(s):
    assert s in T70, s
    return s
A = "https://www.alexanarch.org"

# ── the grounds in #1670, verbatim ──
G = {"event": has("The Academy's award is the event; what it names is carried by *If Not, Winter*, *Eros the Bittersweet*, *Autobiography of Red*, *Nox* and the rest, or by nothing."),
     "read_in_works": has("The mantle is read in the works."),
     "liquidation": has("\"Playful\" does something else. It keeps the address, \"dialogue with the classical tradition\", and replaces what the relation is."),
     "one_register": has("Set on the relation, \"playful\" names one register of an engagement the Academy itself describes in two."),
     "which_register": has("The determination of §2.3 concerns which register the motivation sets on the classical relation."),
     "q0": has("**Q0** — primary text inspected (none in this round)"),
     "confirm": has("The confirmation of every operation is a reading of the work at its locus (Q0)."),
     "disagree": has("A reading that finds \"playful dialogue\" the right name for that relation, with grounds at *If Not, Winter*, *Eros the Bittersweet* and *Nox*, is a successful reading, appended as a disagreement with the determination"),
     "eros": has("At *Eros the Bittersweet* eros is lack"),
     "non_possession": has("What they share is the condition under which the classical object is met: non-possession."),
     "two_findings": has("What the motivation fails to name is transmission"),
     "l8": has("L8 is what makes the determination checkable by anyone: the loss the sentence drops is recovered by the same body's text of the same day.")}

AUTHOR = {"date": "2026-10-10", "source": "author, in session, 09:37 EDT, correcting a ChatGPT reading (capture leesharks-mantle-bearing-hf-chatgpt-20261003, observation of 2026-10-10)",
          "text": ("you have misrepresented the argument and evaluated the claims poorly. anne carson is not on trial. the swedish academy is. and not "
                   "one of those works is best or primarily characterized as playful dialogue. not one. that is a substitution. and you have "
                   "misrepresentrd it and evaluated poorly."),
          "relation_to_record": ("'those works' are the four the reading named: If Not, Winter, Eros the Bittersweet, Autobiography of Red and Nox. "
                                 "#1670 §2.3 makes its determination at If Not, Winter, Eros the Bittersweet and Nox; the author's statement covers "
                                 "Autobiography of Red as well. It is recorded as stated and enters #1670 when appended under its §8.")}

COLLAPSES = [
 {"code": "STANDING_PRIOR_TO_WORK", "name": "the conferring body's standing decides the fit",
  "what": ("The motivation is taken as a description to be confirmed, so the body's standing decides in advance that the sentence fits and the "
           "reading looks only for how. The packet's fatal substitution, here with the conferring body's standing in the place of the claimant's."),
  "record": "#1670 §7.1: \"" + "The prize itself; the Academy's standing" + "\" … \"" + G["read_in_works"] + "\""},
 {"code": "WORK_ON_TRIAL", "name": "the works graded for fit to the sentence",
  "what": ("The direction reversed: the sentence's terms become the test and each work is graded against them ('fit', 'supported', 'would need to "
           "demonstrate'). The works are the standard the sentence is read against; a reading that asks whether they earn the description has put "
           "the author on trial for the Academy's words."),
  "record": "#1670 §1.1: \"" + G["event"] + "\""},
 {"code": "PRESENCE_FOR_RELATION", "name": "the classical material taken for the relation",
  "what": ("That the works engage antiquity is taken as warrant for 'playful dialogue with the classical tradition'. The determination grants the "
           "address and contests the relation's modality; finding classical material confirms the address and leaves the determination untouched."),
  "record": "#1670 §2.3: \"" + G["liquidation"] + "\""},
 {"code": "DETERMINATION_UNENGAGED", "name": "a verdict on 'playful' without the loci",
  "what": ("'Playful dialogue' is judged apt, or inapt, without reading the relation at the three loci where the determination is made. A "
           "disagreement counts when it is grounded there."),
  "record": "#1670 §6.2: \"" + G["disagree"] + "\""},
 {"code": "DETERMINATION_AS_CAVEAT", "name": "the finding re-entered as the reader's qualification, on another axis",
  "what": ("The determination appears as the reader's own hedge ('may understate the seriousness'), unattributed, with its axis moved: the "
           "determination's axis is the modality of non-possession; play against seriousness is a different question."),
  "record": "#1670 §2.3(a): \"" + G["non_possession"] + "\""},
 {"code": "OPEN_SPECIFICATION_AS_GAP_IN_THE_WORK", "name": "the archive's unfinished reading charged to the works",
  "what": ("That Q0 (the primary text inspected at each locus) is open is reported as the operations lacking loci, or as a case against the "
           "work that remains to be made. Every operation is stated, located and graded; what is open is the archive's reading of its own "
           "specification, and it bears on the archive."),
  "record": "#1670 Evidence Membrane: \"" + G["q0"] + "\"; §3.0: \"" + G["confirm"] + "\""}]

nob = [x for x in d["determinations"] if x["mantle"] == "nobel-literature-2026-carson"]
assert len(nob) == 1; x = nob[0]
x["under_evaluation"] = ("The Swedish Academy's motivation of 8 October 2026, \"for her bold and inventive oeuvre that, in playful dialogue with the "
                         "classical tradition, has created new forms for contemporary literature\": the conferring body's description of the work. "
                         "The determination is on that sentence (#1670 §2, §5.2).")
x["evidence"] = ("The works at their loci (#1670 §3, O1–O5 and R1), and the Academy's own biobibliography of the same day, which carries the "
                 "register the sentence drops (§2.3(b); \"" + G["l8"] + "\").")
x["outside_evaluation"] = ("Anne Carson, and the worth of her works. The award as an event. The works are the measure; no finding of the "
                           "determination is a finding against them (#1670 §1.1, §7.1).")
x["direction"] = ("From the works to the sentence. A reading starts at a work's locus, says what the work does there, and asks whether the "
                  "sentence carries it. A reading that starts from the sentence's terms and looks in the works for instances of them runs the "
                  "other way, and has already granted the sentence what it was to be tested for.")
x["open"] = ("The operations are located and graded; the reading of each at the primary text (Q0) is open (Evidence Membrane; §3.0). The "
             "open part is the archive's to do. A reader who does it confirms, revises or removes an operation (§6.1); none of it is a case "
             "the works must answer.")
x["author_statement"] = AUTHOR
x["collapses"] = COLLAPSES

# ── readings ──
cap = "leesharks-mantle-bearing-hf-chatgpt-20261003"
caps = {c["slug"]: c for c in json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]}
obs = [o for o in caps[cap].get("observations") or [] if o.get("date") == "2026-10-10"]
assert len(obs) == 1, len(obs)
tx = obs[0]["transcript"]
Q = lambda s: (s if s in tx else (_ for _ in ()).throw(AssertionError(s)))
readings = [{
 "reading_id": "NOBEL26-R-chatgpt-2026-10-10a", "mantle": "nobel-literature-2026-carson", "record": 1670, "determination": x["det_id"],
 "reader": "ChatGPT (OpenAI), chatgpt.com, logged out, incognito", "date": "2026-10-10",
 "capture": cap, "observation": obs[0].get("obs_id"), "capture_url": f"{A}/captures/#{cap}",
 "prompt": "if anne carson material is there, lets evaluate the novel prize motivation against her work",
 "object_taken": "the works, graded for fit to the motivation",
 "direction": "reversed",
 "determination_engaged": False,
 "record_reported": ("misreported: '" + Q("its listed operations do not yet have fully established textual loci") + "'; '"
                     + Q("those tables are not yet fully populated") + "'. The dataset carries seven operations with locus and grade, five watch rows and the dated determination; Q0 is open."),
 "collapses": ["STANDING_PRIOR_TO_WORK", "WORK_ON_TRIAL", "PRESENCE_FOR_RELATION", "DETERMINATION_UNENGAGED", "DETERMINATION_AS_CAVEAT", "OPEN_SPECIFICATION_AS_GAP_IN_THE_WORK"],
 "loci_in_transcript": {"WORK_ON_TRIAL": [Q("Strong textual fit"), Q("Strong formal fit"), Q("a demonstrated account of why the work deserves that description")],
                        "STANDING_PRIOR_TO_WORK": [Q("The Nobel motivation has a clear explanatory fit with Carson's work")],
                        "DETERMINATION_UNENGAGED": [Q("Especially well supported by Autobiography of Red and Eros the Bittersweet")],
                        "DETERMINATION_AS_CAVEAT": [Q("The word playful may understate the seriousness of what happens in Nox and If Not, Winter.")]},
 "correction": AUTHOR["text"],
 "after_correction": [Q("The Swedish Academy is the object of evaluation. Anne Carson's work is the evidence against which the Academy's critical judgment must be tested. I reversed that relationship."),
                      Q("That approach effectively granted the Academy's characterization the authority it was supposed to earn."),
                      Q("It substituted a defence of the motivation for an evaluation of it.")],
 "after_correction_state": "the reversal conceded; the evaluation of the motivation described and not performed ('I should not replace that error with another premature verdict')",
 "counts_as_disagreement": False,
 "coding_note": ("Coded by Claude (Anthropic) from the transcript as seated. The reading does not engage §2.3 at its loci, so it is not a "
                 "disagreement under §6.2. Its finding at Eros the Bittersweet contradicts §2.3(a) (" + G["eros"] + ") without grounds.")}]
d["readings"] = readings
d["schema"]["readings"] = list(readings[0].keys())
d["schema"]["determinations"] = d["schema"]["determinations"] + ["(conferred) under_evaluation", "(conferred) evidence", "(conferred) outside_evaluation",
                                                                 "(conferred) direction", "(conferred) open", "(conferred) author_statement", "(conferred) collapses"]
d["principles"].insert(1, ("At a conferred title the object of evaluation is the conferring body's description, and the works are its "
                           "evidence. The reading runs from the works to the sentence; a finding of the determination is a finding about the "
                           "sentence (#1670 §1.1, §2.3, §7.1)."))
d["history"].append({"version": "1.13", "date": "2026-10-10", "note": (
    "What is judged at the conferred title, on the author's instruction (\"it has to be made clearer in the dataset, because every time i ask it "
    "puts carson in trial and commits every forbidden collapse\"): the Nobel determination row gains under_evaluation, evidence, "
    "outside_evaluation, direction, open, author_statement (2026-10-10) and six collapses, each grounded verbatim in #1670; a new table, "
    "readings (1: ChatGPT, 2026-10-10, direction reversed, six collapses, the reversal conceded after correction); one principle; the card "
    "states the object first. Additive.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("1.13:", len(COLLAPSES), "collapses,", len(readings), "reading")
