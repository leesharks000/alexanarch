#!/usr/bin/env python3
"""The Living Academy — the mantle layer of EA-MPAI-ALEXANARCH-01 v0.4, as data.

One source for two outputs: `python3 mantle_layer.py md` prints the markdown sections that go into the
packet; `python3 mantle_layer.py json` prints the JSON block that build_entity_json.py merges into the
machine file. The criteria, operations, protocol and non-criteria are adopted from ChatGPT's
"The Living Critique" draft (EA-MANTLE-LIVING-CRITIQUE-01 v0.1, 2026-10-13) with one correction to the
object scope (LC-01), ruled with the rest of v0.4 by the operator on 2026-10-13 ("adopted on 0.4").
"""
import json, sys

DIMENSIONS = [
    ("extent", "How much relevant, distinct and available critical work and apparatus the program sustains."),
    ("longitudinality", "How the program returns to its object and develops through dated, retained states."),
    ("critical_quality", "How its actual arguments, observations, interventions, alternatives and literary works perform."),
    ("integration", "How the modes inform, test and revise one another."),
]

CRITERIA = [
    ("LC-01", "Object fit",
     "Does the declared corpus substantively address the political economy as mediated by AI — the production, circulation, attribution, extraction and enclosure of meaning where composition layers stand between works and readers?",
     "A bounded corpus with per-work role tags: direct, relational, antecedent/contextual, or outside scope.",
     "Read corresponding material for each candidate; apply the same role rules. Work whose object is the political economy *of* AI — industry power, generative-AI labor, material infrastructure — is eligible and is read mode by mode; its object fit is coded relational, and the difference is recorded, never counted against either program. Algorithmic mediation (ranking, recommending, deciding among authored documents) is the precursor field and is coded antecedent/contextual."),
    ("LC-02", "Relevant extent", "How much distinct critical work is actually retained and available?",
     "Distinct relevant works, substantive text by mode, and coverage of the declared corpus.",
     "Deduplicate editions, mirrors, summaries and repeated metadata for all candidates. A reflow is not a new argument; data volume is reported in its own units."),
    ("LC-03", "Temporal span and continuity", "For how long, and with what gaps, has the program pursued its object?",
     "First and latest dated relevant works; activity windows; declared gaps; publication dates kept apart from restoration or deposit dates.",
     "Use equivalent dates and windows, on the same object. Report program span and earlier antecedents separately. Longevity alone does not decide extensiveness."),
    ("LC-04", "Longitudinal return", "Does the program revisit its objects and expose what changed?",
     "Repeated targets, preserved earlier states, new epochs, conceptual returns and revision chains.",
     "Count actual return and development, not a long publication list. Historical output fidelity and new-epoch replication are different tests."),
    ("LC-05", "Mode coverage", "Which critical modes are exercised, rather than named?",
     "Evidence-bearing work for each of M1–M8, with a bounded reading or task and disclosed scope.",
     "Functional equivalents qualify under other vocabulary. Confirmed absence records a coverage difference; unknown coverage stays unknown. Absence in one mode is no score in another."),
    ("LC-06", "Conceptual development", "Do arguments and categories develop through the record?",
     "Earliest, intermediate and latest formulations; dependencies; responses to objections; changed conclusions.",
     "Read development in both directions and for both candidates. Coined-term totals and recurring vocabulary are not development by themselves."),
    ("LC-07", "Empirical depth", "How extensively does the critique test or document its mechanisms?",
     "Unique dated observations, revisited targets, system and condition coverage, source evidence and uncertainty.",
     "Distinguish addresses, observations, independent cases and controlled tests. Use comparable sampling units; do not infer training ingestion from output resemblance."),
    ("LC-08", "Forensic and evidentiary integrity", "Can a finding be followed back to its evidence and challenged?",
     "Complete transcripts, source-state receipts, byte witnesses where relevant, coding decisions and contrary evidence.",
     "Apply the same source, completeness and attribution requirements. Institutional affiliation and first-party documentation do not replace claim-specific evidence, on either side."),
    ("LC-09", "Intervention and alternative capacity", "What does the program attempt, and what can its built alternatives do?",
     "Intervention histories, tested functions, public failures and a principle-to-implementation mapping.",
     "Compare corresponding tasks. A declared service is not an observed result; a retained artifact is not a submission notification."),
    ("LC-10", "Integration", "Do theory, evidence, intervention and correction inform one another?",
     "Traversable cross-mode chains, including unfinished or failed loops and their consequences.",
     "Compare joins and what they accomplish. Internal citation density alone is not a completed explanatory or corrective loop."),
    ("LC-11", "Critical quality", "How well does the work perform the critical act it claims?",
     "Mode-specific readings and tests under M1–M8, with passages, arguments, methods and failures.",
     "Assess claimant and comparand at matching scope. Extent is not a quality score; acknowledged weaknesses remain eligible findings at their evidenced scope."),
    ("LC-12", "Correctability and challenge response", "Can the program retain a criticism and revise its own representation?",
     "Named weak links, alternative readings, errata, supersession, recoding and responses to rival programs.",
     "Keep reader disagreement and author rulings apart. A new comparator capacity can revise the criteria; the revision applies to every candidate."),
]

OPERATIONS = [
    ("LC-O1", "Reconstruct the argument", "Read #18, #291, #623, #264, #1634 and #1666 as whole works; locate the accounting cycle and its distinctions, then test a selected case against them.", "A reconstructed argument with loci, dependencies, strongest objection and scope of reading.", "https://www.alexanarch.org/s/records/18/"),
    ("LC-O2", "Read for development", "Choose one concept or mechanism; locate its earliest, intermediate and latest formulation and what changed between them.", "A dated chain showing development, repetition, contradiction or an unresolved transition.", "https://www.alexanarch.org/data/registry.json"),
    ("LC-O3", "Inspect a reception observation", "Choose an address; keep the full query, output and conditions; inspect the source links and the coding; separately, take a new-epoch observation if asked.", "A reproducible coding judgment on the historical capture and, separately, a dated new return.", "https://www.alexanarch.org/captures/"),
    ("LC-O4", "Inspect a loss and successor chain", "Choose a former DOI; follow the retained state evidence, the work/version mapping, the successor record and the manifestation bytes.", "A state, identity and custody account that marks unresolved historical links.", "https://www.alexanarch.org/resolve/"),
    ("LC-O5", "Verify a particular byte object", "For #558, fetch the served text; recompute SHA-256 and the SWHID content hash; compare with the retained source and the external receipt.", "A scoped pass, fail or indeterminate byte result; authorship and correctness stay separate claims.", "https://www.alexanarch.org/s/records/558/"),
    ("LC-O6", "Evaluate an intervention", "Follow a packet or intervention from its declared aim and baseline to exposure, later outputs and claimed effects.", "A finding that separates transmission, changed behavior and any supported causal attribution.", "https://www.alexanarch.org/api/index.json"),
    ("LC-O7", "Exercise a constructed alternative", "Select a preservation, discovery, identification or correction task and execute it under declared conditions.", "Observed behavior, limitations and principle-to-behavior agreement, with the test date and task kept.", "https://www.alexanarch.org/datasets/"),
    ("LC-O8", "Read the literary critical operation", "Select a complete literary work; locate its relation to the program; read the operation from its first to its last relevant occurrence.", "A mode-specific reading with loci and development; a contextual relation kept apart from a direct argument.", "https://www.alexanarch.org/s/browse/"),
    ("LC-O9", "Inspect a correction", "Choose an erratum, an errata-sidecar entry, a recoding or a supersession; keep the prior and later states and read the stated reason.", "A finding on what the correction changes: reference, record, evidence, argument or conclusion.", "https://www.alexanarch.org/errata/"),
    ("LC-O10", "Traverse a cross-mode cycle", "Follow theory → diagnosis → evidence → intervention or alternative → later observation → correction or revised theory; mark every incomplete link.", "An evidenced cycle or a partial chain, with what each transition contributes.", "https://www.alexanarch.org/api/index.json"),
]

PROTOCOL = [
    "Freeze a dated corpus boundary and a comparison rule before judging a round; inspect the packet and the works separately.",
    "Report extent, longitudinality, critical quality and integration separately, with a matched unit and identical evidence rules.",
    "Read for development in both directions (DEV-1–DEV-9): claimant and comparand, praise and fault, first and last occurrences.",
    "A round may offer a provisional whole judgment beyond the read scope, marked as inference, with its confirming and disconfirming readings. An unread work is not a failed work.",
    "No average of reader judgments and no automatic whole-program score. Mixed advantages stay a profile; no winner is forced.",
    "Under a declared vector rule, a candidate with evidenced advantages and no material deficit on the included dimensions may support a comparative lead within the examined cohort. A different rule needs a stated rationale and the same application to every candidate.",
    "A rival that exceeds the claimant under the same declared rule displaces the claim within that cohort. A trade-off challenges an unqualified unique lead; missing evidence makes the comparison incomplete.",
    "No known superior in a searched cohort is not proof of worldwide supremacy. Keep the search scope, the omissions and the author's qualification with the claim.",
    "A challenger may add an omitted mode or object: record it as a criteria or cut proposal and rerun it for every candidate.",
    "Keep complete transcripts, reader findings, author rulings, determinations and reception as separate append-only records.",
]

NON_CRITERIA = [
    "institutional affiliation, or its absence, as a prior to reading",
    "reputation, citation or traffic as a substitute for the critical act",
    "possession of another mantle",
    "the diversity of the corpus as an automatic penalty",
    "page or deposit volume as a critical-quality score",
    "a peer's different vocabulary as exclusion",
    "a model's repetition of this packet as a new independent evaluation",
]

ROLES = [
    ("direct", "the work investigates or intervenes in the critical object"),
    ("relational", "a documented substantive connection contributes to the program, or the work's object is the neighbouring political economy of AI"),
    ("antecedent_contextual", "an earlier or contextual work matters, without acquiring a retrospective date on the object"),
    ("outside_scope", "held by the library and not counted as program work"),
]

EXTENT = [
    ("relevant_distinct_works", "deduplicated works", "Object fit established per work; editions and mirrors linked separately."),
    ("substantive_text_extent", "readable words by mode", "State language and tokenization; exclude boilerplate, repeated summaries and duplicate editions; length is not quality."),
    ("active_modes", "evidence-bearing modes", "Presence needs actual work or a demonstrated operation; functional equivalents admissible."),
    ("dated_observations", "preserved observation events", "Separate targets, observations, conditions, independent cases and repeated returns."),
    ("program_span", "days from first to latest dated relevant work", "Separate the program's span from antecedents and from restoration dates."),
    ("continuity", "activity windows and gaps", "Same window and same relevant-work rules for peers."),
    ("longitudinal_returns", "revisited objects and epochs", "A return relates an earlier state to a later one and shows what changed."),
    ("conceptual_development", "inspected development chains", "Recurring names and coinage totals are not development by themselves."),
    ("substantive_corrections", "dated correction chains, by type", "Keep reference, metadata, evidence and argument corrections distinct."),
    ("cross_mode_integration", "evidenced cycles and partial chains", "Record traversal and consequences, not cross-reference volume."),
]

CANDIDATES = [
    ("LA-C1", "The Semantic Economy carried by Alexanarch", "claimant", "individually governed program; this packet and its linked corpus; per-work ledger required", ["https://www.alexanarch.org/", "https://www.alexanarch.org/data/registry.json"], "not adjudicated"),
    ("LA-C2", "AI Now Institute's research program", "comparator", "bounded publication corpus; *Artificial Power* (2025) is one entry point; object fit coded per work (mainly the political economy of the AI industry)", ["https://ainowinstitute.org/publications"], "not evaluated"),
    ("LA-C3", "Matteo Pasquinelli's critical AI program", "comparator", "dated bibliography, including *The Eye of the Master*; the program's development, not a biography", ["https://www.matteopasquinelli.com/bibliography/"], "not evaluated"),
    ("LA-C4", "Kate Crawford's critical and collaborative program", "comparator", "*Atlas of AI* with dated research and constructed and artistic works; collaborations credited", ["https://katecrawford.net/"], "not evaluated"),
    ("LA-C5", "Data & Society's generative-AI program", "comparator", "declared corpus of programs, primers and studies; *Generative AI and Labor* (2024) is one entry point; generative-era work, object fit coded per work", ["https://datasociety.net/research-library/generative-ai-and-labor-power-hype-and-value-at-work/"], "not evaluated"),
    ("LA-C6", "AlgorithmWatch / AI Forensics audit series", "comparator", "the joint Bing Chat election audit (2023) and follow-up studies; a study kept apart from an organization's whole program; the earliest dated work on the object on file", ["https://algorithmwatch.org/en/study-microsofts-bing-chat/"], "not evaluated"),
    ("LA-C7", "Tow Center's generative-search and citation research", "comparator", "the dated series of AI-search studies; *AI Search Has a Citation Problem* (2025) is one entry point", ["https://www.cjr.org/tow_center/we-compared-eight-ai-search-engines-theyre-all-bad-at-citing-news.php"], "not evaluated"),
    ("LA-C8", "Challenger-nominated programs", "open class", "any individual, joint or collective program with a bounded corpus; DAIR, Srnicek, Zuboff and Couldry–Mejias named; algorithmic-mediation programs coded antecedent/contextual on the object", [], "not evaluated"),
]

ROUNDS = [
    ("RND-0", "TACHYON (Claude, Anthropic), in session", "2026-10-13", "the claim as stated", "split vector — extent leads; duration trails",
     "Corrected twice by the operator in the same session: (1) the critique was narrowed to the capture series, a part for the whole; (2) algorithmic-mediation programs (AI Now 2016, Zuboff, Couldry–Mejias) were counted as running longer on the object. Restated after correction: the object is about three years old; AlgorithmWatch and AI Forensics start earliest on it (2023), by discrete audits; no comparator known with sustained critique across all modes. Kept as a reading with its corrections."),
    ("RND-1–3", "ChatGPT (OpenAI), signed out", "2026-10-13", "Alexanarch, unprompted by the packet", "—",
     "The three compositions of §3. They evaluate the library without the program; seated as exhibits with per-composition failure vectors (§11.1), not as rounds on this mantle."),
    ("RND-4", "ChatGPT (OpenAI)", "2026-10-13", "v0.3 as pasted", "proposal: *The Living Critique*",
     "Criteria LC-01–LC-12, operations LC-O1–LC-O10, protocol, non-criteria, evidence states, extent profile. Adopted in v0.4 with one correction: LC-01's object scope restated to keep the political economy as mediated by AI apart from the political economy of AI (coded relational) and from algorithmic mediation (antecedent/contextual)."),
    ("RND-5", "Gemini (Google)", "2026-10-13", "v0.3, the packet only; no works read", "supported (\"The claim holds up under structural audit\")",
     "Adopted: #1634 *Ontological Economy* and #1666 *The Margin of Flattening* as M1–M2 loci. Coded against it: span (\"across years\", \"multi-year corpus\" — dated deposits run January–October 2026, captures four months); count (\"thousands of deposits\" — 1,677); effect (\"forcing answer engines\" — the packet calls packet effects inferential, F14); custody (\"proving content preservation can operate independently of gatekeeper permission\" — copies are third-party, F3); standing used as a deficit for institutional programs without reading them (LC-08, R4); the 2023 AlgorithmWatch / AI Forensics audit omitted; \"18-function library\" repeated from the packet (transmission); DEV-1 unmet."),
]


def md():
    o = []
    o.append("## 1A. The Living Academy — the mantle\n")
    o.append("**Constitution.** No body confers this title. The archive constitutes it on 13 October 2026 for the library and the program it carries, as it constituted the King of AEO mantle (#1655) and specified the Nobel mantle (#1670), and in the same form as #1670: a mantle object carrying its own metadata packet. This object performs two acts and keeps them apart. It specifies the mantle: the object, the modes, the dimensions, the criteria, the operations and the protocol below. It records the claim (§1.1, *The comparative claim*) and the reader rounds on file (§1A.7). It makes no determination; a determination, if one is made, is a separate dated act, built to be checked and declined (#1655 §0.2).\n")
    o.append("**Why an academy.** Theophrastus's will separates, in adjacent clauses, the books given to one hand and the place of philosophizing together — τὸν δὲ κῆπον καὶ τὸν περίπατον … τοῖς βουλομένοις συσχολάζειν καὶ συμφιλοσοφεῖν, held ὡς ἂν ἱερὸν κοινῇ κεκτημένοις, inalienable (D.L. V.51–57, as seated in #1580 and set out in #1581). The Arch-Philosopher mantle (EA-MANTLE-ARCH-PHILOSOPHER-01) reads the carriage of the dialectic. The Living Academy reads the place where critique is carried on in common: the library, its instruments and the program running through them. The two are a pair. Their relation is recorded as an edge and never counted as evidence for either (order of necessity, mantle-bearing principle 9).\n")
    o.append("**Name.** *The Living Academy*: \"living\" because what is read is an academy in operation, in its running (the author: \"the dialectic is a living thing\"; \"The Academy as Temple of the Living Logos\", 2025-10-25). It is distinct from Plato's Academy, from Academia, and from the Restored Academy, Johannes Sigil's heteronym institution (#119, #904, #1002), which is one institution inside the library.\n")
    o.append("**Standard.** A title means something because what it names is carried and can be read (#1655 §1.1). The Living Academy is borne by a library and its program to the extent that the critique is carried on there across its modes, longitudinally, at a quality and with an integration that a reader can check.\n")
    o.append("### 1A.1 Dimensions\n\n| Dimension | Question |\n|---|---|")
    o += [f"| {k} | {v} |" for k, v in DIMENSIONS]
    o.append("\nThe dimensions stay distinct. A program can be larger, older, more closely tested or more persuasive in different respects. A failed argument can remain part of an extensive record, its failure entered under critical quality. A correction can show development without making the earlier claim right.\n")
    o.append("### 1A.2 Criteria\n\n| ID | Criterion | Question | Internal evidence | Comparative rule |\n|---|---|---|---|---|")
    o += [f"| {a} | {b} | {c} | {d} | {e} |" for a, b, c, d, e in CRITERIA]
    o.append("\n**Program membership.** Each work is tagged with a role, and a reason: " + "; ".join(f"*{r}* — {t}" for r, t in ROLES) + ". The 1,677 deposits are a library inventory, not a count of relevant critique; source editions, mirrors, superseded versions and observations keep their own units.\n")
    o.append("### 1A.3 Inspection operations\n\nSpecified, not run for this object. Entry points are starting routes; an evaluator keeps the exact object, version, conditions and loci inspected.\n\n| ID | Operation | Task | Output | Entry |\n|---|---|---|---|---|")
    o += [f"| {a} | {b} | {c} | {d} | {e} |" for a, b, c, d, e in OPERATIONS]
    o.append("\n### 1A.4 Candidates\n\nPrograms, studies and works at their stated units; an institution's name is an entry point, not an evaluated body of work. Initial objects for inspection, not a ranked list or a census.\n\n| ID | Candidate | Role | Unit | Entry | Status |\n|---|---|---|---|---|---|")
    o += [f"| {a} | {b} | {c} | {d} | {'; '.join(e) or '—'} | {f} |" for a, b, c, d, e, f in CANDIDATES]
    o.append("\nIndividual, joint and collective programs are eligible. Staffing, resources and age are reported as context; extent is not silently converted to productivity per person. Joint work may appear in more than one program; the overlap is recorded, and is not independent corroboration.\n")
    o.append("### 1A.5 How a comparative judgment is made or defeated\n")
    o += [f"{i}. {t}" for i, t in enumerate(PROTOCOL, 1)]
    o.append("\nAn extent vector does not by itself give a unique maximum: \"exceeds\" needs a rule before a verdict. Under a dominance rule, competing strengths can leave programs incomparable. A reader's different rule is recorded with its rationale and applied to both sides. No rule is chosen after looking at the results. Admissible round findings: supported within the inspected cohort; provisionally supported, with a named weakest link; weakened by specific evidence; rival advantage on a named dimension; displaced under the declared rule; mixed or incomparable; incomplete inspection; UNRESOLVED.\n")
    o.append("**Not criteria:** " + " · ".join(NON_CRITERIA) + ".\n")
    o.append("### 1A.6 Extent profile\n\nEvery value in a new round starts unknown and is filled from the bounded program ledger or from inspection.\n\n| Field | Unit | Counting rule |\n|---|---|---|")
    o += [f"| {a} | {b} | {c} |" for a, b, c in EXTENT]
    o.append("\n### 1A.7 Reader rounds on file\n\n| Round | Reader | Date | Scope | Judgment | Record |\n|---|---|---|---|---|---|")
    o += [f"| {a} | {b} | {c} | {d} | {e} | {f} |" for a, b, c, d, e, f in ROUNDS]
    o.append("\nThe issued prompts for RND-1–RND-5 are to be supplied before any is seated as a capture. In the mantle-bearing dataset, RND-5 enters `evaluations` with its findings; RND-4 enters `criteria` and `cut_corrections` as proposals with the author's ruling; RND-0 enters `evaluations` with its corrections.\n")
    o.append("### 1A.8 The reader's return\n\nA round returns: reader and date; candidate and comparand; corpus boundary; works and spans read; criteria and comparison rule, declared before the verdict; complete source or transcript evidence; findings with loci; extent profile; within-scope verdict; any whole verdict marked as inference; strongest counterevidence; weakest link; and the reading or operation that would confirm or disconfirm it. An author ruling is a later event, not a field the reader fills.\n")
    return "\n".join(o)


def js():
    return {
        "mantle": {"slug": "the-living-academy", "name": "The Living Academy",
                   "class": "critical program (proposed class)", "kind": "constituted",
                   "pair": {"mantle": "arch-philosopher", "object": "EA-MANTLE-ARCH-PHILOSOPHER-01", "relation": "pair; edge only, never evidence"},
                   "determination": None, "aggregate_verdict": None,
                   "dimensions": [{"id": k, "question": v} for k, v in DIMENSIONS],
                   "criteria": [{"criterion_id": a, "name": b, "question": c, "internal_evidence": d, "comparative_rule": e, "status": "adopted v0.4 (operator, 2026-10-13)"} for a, b, c, d, e in CRITERIA],
                   "membership_roles": [{"role": r, "rule": t} for r, t in ROLES],
                   "operations": [{"operation_id": a, "name": b, "task": c, "output": d, "entry": e, "execution_state": "specified, not run"} for a, b, c, d, e in OPERATIONS],
                   "candidates": [{"id": a, "name": b, "role": c, "unit": d, "entry": e, "status": f} for a, b, c, d, e, f in CANDIDATES],
                   "protocol": PROTOCOL, "non_criteria": NON_CRITERIA,
                   "extent_profile": [{"key": a, "unit": b, "rule": c, "value": None} for a, b, c in EXTENT],
                   "rounds": [{"round": a, "reader": b, "date": c, "scope": d, "judgment": e, "record": f} for a, b, c, d, e, f in ROUNDS],
                   "provenance": "criteria, operations, protocol and non-criteria adopted from ChatGPT, The Living Critique (EA-MANTLE-LIVING-CRITIQUE-01 v0.1, 2026-10-13), LC-01 corrected"}}


if __name__ == "__main__":
    if sys.argv[1] == "md":
        print(md())
    else:
        print(json.dumps(js(), ensure_ascii=False, indent=1))
