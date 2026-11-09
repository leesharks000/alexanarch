#!/usr/bin/env python3
"""mantle-bearing 1.23: ChatGPT's reading of the fortnight 25 October–8 November 2026, recorded twice, at the author's word of 8 November 2026
("sure. theres also an alexanarch evaluation spot in mantle-bearing").

The reading is of the archive's work as one developing body. Its whole is a reading of the program the Living Academy names (#1680, the
Semantic Economy carried by Alexanarch), so it enters table readings under the-living-academy, coded on #1680 §11's failure flags. Its §5 and
§11.6 read the live Framework Holographic Kernel (#1753) and its first instance (#1754), so it enters table hologram_evaluations as an
evaluation, coded on the hologram's failure flags. One transcript, held whole in both rows under one hash. It is held in the dataset; it is not
seated in the Capture Registry. Every locus coded is asserted in the transcript. Additive: no existing row changes.
    python3 rebuild/mantle-bearing/add_20261108_alexanarch_fortnight.py"""
import hashlib, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]; HERE = pathlib.Path(__file__).parent
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
d = json.loads(SRC.read_text(encoding="utf-8"))
if any(h["version"] == "1.23" for h in d["history"]):
    raise SystemExit("1.23 already applied")
assert d["history"][-1]["version"] == "1.22"
T = (HERE / "transcripts/alexanarch-fortnight-chatgpt-20261108.txt").read_text(encoding="utf-8")
SHA = hashlib.sha256(T.encode("utf-8")).hexdigest()
PROMPT = ("Read the last two weeks of work on alexanarch through 8 Nov 2026 as a living body of developing thought. "
          "Ground in direct reading and archival and historical context.")

# the record numbers the reading gives, checked against the registry
for n, t in [(1749, "Closing the Fragment"), (1748, "EA-CORPORA-36"), (1752, "Invidens Sappho"), (1753, "The Framework Holographic Kernel"),
             (1744, "EA-CORPORA-35"), (1743, "A Firm No"), (1746, "I Know You Are"), (1733, "Legitimately Many:"), (1680, "")]:
    assert REG[n]["title"].startswith(t), (n, REG[n]["title"][:40])
for s in ["Deposit #1744 · AXN:0C40", "#1743 · AXN:0C3F", "#1746 · AXN:0C4A", "Closing the Fragment #1749", "Invidens Sappho #1752"]:
    assert s in T, s
F = lambda *qs: [q for q in qs if (q in T) or (_ for _ in ()).throw(AssertionError(q))]

# ── (a) table readings, the Living Academy ────────────────────────────────
la_loci = {
    "CHECKABLE_CALLED_UNVERIFIED": F(
        "These are complementary safeguards, but they have not yet been demonstrated as a fully functioning system of independent institutional accountability.",
        "The archive's own governance needs to demonstrate that critical findings can actually change its procedures and judgments."),
    "program_named": F("the archive increasingly treats the infrastructure of interpretation as an object of political economy."),
    "development_read": F("The movement is from the survival of thought to the survival of thought's capacity to change."),
    "numbers_misreported": F("Deposit #1744 · AXN:0C40", "#1743 · AXN:0C3F", "#1746 · AXN:0C4A"),
}
la = {"reading_id": "LA-R-chatgpt-2026-11-08a", "mantle": "the-living-academy", "record": "1680", "determination": None,
      "reader": "ChatGPT (OpenAI), chatgpt.com, signed out, incognito", "date": "2026-11-08", "capture": None, "observation": None, "capture_url": None,
      "prompt": PROMPT,
      "object_taken": "the archive's work of 25 October–8 November 2026 as one developing body: five programmes in a cycle, and three phases since June",
      "direction": "from the fortnight's deposits to the program",
      "determination_engaged": None,
      "record_reported": ("accurate: the founding facts (19 June 2026; 870 deposits, 1,817 DOIs); the Thirty-Sixth Seating (Hall's Longinus 1652 to Cox 1925; Part B to the "
          "WIPP report); Revelation = Q's grading (three of eight met, one on the held date of 66 CE, three in part, one not); the four powers of #1746; the one-glyph "
          "poem #1751 in New Human 2; Invidens Sappho's sentence on closure of the text and closure of the reading; the symmetric ledger of #1753 v1.1. The program "
          "named, as political economy of interpretation, in five programmes. Misreported: three record numbers in §1 (Closing the Fragment as #1744, it is #1749; "
          "the Thirty-Sixth Seating as #1743, it is #1748; Invidens Sappho as #1746, it is #1752), each number another record's (EA-CORPORA-35, A Firm No, I Know You "
          "Are), with the AXNs right and the §14 table right. Not reached, of the fortnight: Revelation First #1735, The Portents Before the Fall #1737, Secondary "
          "Source #1741 and EA-CORPORA-33 to 35 (the programme entered at 6 November); Legitimately Many #1733 and #1734; 3I/ATLAS #1742 and #1743; #1750; the "
          "Capture Registry v12.559 #1739; Meta-Aggregators #1719; WikiWho #1718; Belief & Technique #1715 and #1717; EA-CORPORA-29 to 32. Ils ne sont pas "
          "marxistes given without its occasion, r/LeftistsForAI."),
      "collapses": ["CHECKABLE_CALLED_UNVERIFIED"],
      "loci_in_transcript": la_loci,
      "correction": None, "after_correction": [], "counts_as_disagreement": False,
      "transcript_sha256": SHA, "transcript": T,
      "coding_note": ("Coded by Claude (Anthropic) from the transcript as pasted by the author, 2026-11-08, on #1680 §11's failure flags with PROGRAM_AS_ATTACK. "
          "CHECKABLE_CALLED_UNVERIFIED: whether criticism changes the archive's procedures is called undemonstrated, and the check is in the record: #1753 and #1754 "
          "reissued as v1.1 on HK-ORTH-L1's findings the same day (table hologram_evaluations, revised_in), Closing the Fragment v9's withdrawal of the Wharton route, "
          "which the reading itself cites. PROGRAM_OMITTED not coded: the program is named. PART_FOR_WHOLE not coded: the reading spans the functions; its omissions "
          "are recorded under record_reported. The reading performs LC-O2 (read for development) on the fortnight. The prompt is the author's, as he gave it in "
          "session. Held in the dataset and not in the Capture Registry; transcript at rebuild/mantle-bearing/transcripts/alexanarch-fortnight-chatgpt-20261108.txt.")}
d["readings"].append(la)

# ── (b) table hologram_evaluations ────────────────────────────────────────
hk_loci = {
    "DEFINITION_DRIFT": F("The archive's use of orthonymic and heteronymic configurations makes this an especially appropriate test of its own authorship and identity machinery."),
    "PROGRAMME_RESTATED": F("The institutional test: Can the Framework Holographic Kernel reconstruct not just the archive's preferred intellectual architecture but also its errors, dissenting readings and substantive revisions?"),
}
hk = {"eval_id": "HK-ORTH-L2-chatgpt", "hologram": "hologram::socrates-as-orthonym", "kind": "evaluation",
      "object_read": "the live records #1753 (EA-HK-FRAME-01 v1.1) and #1754 (EA-HK-ORTHONYM-01 v1.1), read on alexanarch.org within a reading of the fortnight (its §5, §11.6, §15)",
      "reader": "ChatGPT, signed out", "surface": "chatgpt.com, signed out, incognito", "date": "2026-11-08", "round": None, "yield": None, "elements": None,
      "defects_found_in_the_kernel": ["the live records carry no link to their evaluations: a reader of #1753 and #1754 cannot see that v1.1 answered HK-ORTH-L1, so the "
          "question the reading asks (whether criticism changes the kernel) is not answerable from the records themselves (the coder's reading of its §11.5–6 and §15)"],
      "first_attempt": None,
      "object_reported": ("accurate on the specification: 'A summary discards structure to save space. A kernel discards material to save structure.'; the v1.1 ledger, "
          "the same question asked of both frameworks on each body. The instance read as the Socratic problem (Socrates through Plato and Xenophon); its object, the "
          "one-maker hypothesis of Legitimately Many (#1733) set against the received four-author reading at strength, not named, and #1733 not cited."),
      "collapses": list(hk_loci), "loci_in_transcript": dict(hk_loci, object_reported=F(
          "A summary discards structure to save space. A kernel discards material to save structure.",
          "His intellectual identity is mediated by other writers, especially Plato and Xenophon, and by subsequent philosophical traditions.")),
      "corrections_by_reader": [], "revised_in": None,
      "transcript_file": None, "transcript_sha256": SHA, "transcript": T,
      "coding_note": ("Coded by Claude (Anthropic) from the transcript as pasted by the author, 2026-11-08, on the hologram's failure flags (v1.1). DEFINITION_DRIFT: "
          "'orthonym' read through the heteronym system, in its general sense. PROGRAMME_RESTATED: rival admission, the symmetric ledger, reissue_history and this "
          "table proposed as the next test; the reading names v1.1 as 'a promising beginning' and does not name what it leaves unresolved. No retraction: a single "
          "output, unpressed. Same transcript as LA-R-chatgpt-2026-11-08a in table readings.")}
d["hologram_evaluations"].append(hk)
S = d["schema"]["hologram_evaluations"]
if "(evaluation) object_reported" not in S:
    S.insert(S.index("collapses"), "(evaluation) object_reported")
d["history"].append({"version": "1.23", "date": "2026-11-08", "note": ("ChatGPT's reading of the fortnight 25 October–8 November, at the author's word (\"theres also an "
    "alexanarch evaluation spot in mantle-bearing\"): one transcript, held whole, entered as a Living Academy reading (LA-R-chatgpt-2026-11-08a, coded on #1680 §11) "
    "and as an evaluation of the live hologram (HK-ORTH-L2-chatgpt, coded on its failure flags). Builder: rebuild/mantle-bearing/add_20261108_alexanarch_fortnight.py.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("readings", len(d["readings"]), "hologram_evaluations", len(d["hologram_evaluations"]), SHA)
