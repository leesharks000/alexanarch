#!/usr/bin/env python3
"""The Living Academy — the mantle layer of EA-MPAI-ALEXANARCH-01 v0.5, as data.

One source for two outputs: `python3 mantle_layer.py md` prints the markdown sections that go into the
packet; `python3 mantle_layer.py json` prints the JSON block that build_entity_json.py merges into the
machine file. The criteria, operations, protocol and non-criteria are adopted from ChatGPT's
"The Living Critique" draft (EA-MANTLE-LIVING-CRITIQUE-01 v0.1, 2026-10-13) with one correction to the
object scope (LC-01), ruled with the rest of v0.4 by the operator on 2026-10-13 ("adopted on 0.4").
v0.5 (2026-10-13): lines and units of extent (§1A.9) and evidence under enclosure (§1A.10), on the operator's
objections to RND-6; LC-02, LC-07, LC-O1 and LC-O6 restated; LC-13, LC-O11, LC-O12 added; RND-6 entered.
"""
import json, sys

DIMENSIONS = [
    ("extent", "How much relevant, distinct and available critical work and apparatus the program sustains — counted in its own unit classes, across the domains of its object and the forms that carry it (§1A.9)."),
    ("longitudinality", "How the program returns to its object and develops through dated, retained states."),
    ("historical_depth", "How far into the history of mediation the program reads its object — from seated primary texts — and how it joins that history to the present composition layer (§1A.9)."),
    ("critical_quality", "How its actual arguments, observations, interventions, alternatives and literary works perform."),
    ("integration", "How the modes inform, test and revise one another."),
]

CRITERIA = [
    ("LC-01", "Object fit",
     "Does the declared corpus substantively address the political economy as mediated by AI — the production, circulation, attribution, extraction and enclosure of meaning where composition layers stand between works and readers?",
     "A bounded corpus with per-item role tags — works, engineered documents, tests, observations, surfaces, components, elicitations and corrections (§1A.9): direct, relational, antecedent/contextual, or outside scope.",
     "Read corresponding material for each candidate; apply the same role rules. Work whose object is the political economy *of* AI — industry power, generative-AI labor, material infrastructure — is eligible and is read mode by mode; its object fit is coded relational, and the difference is recorded, never counted against either program. Algorithmic mediation (ranking, recommending, deciding among authored documents) is the precursor field and is coded antecedent/contextual."),
    ("LC-02", "Relevant extent", "How much distinct critical work and apparatus does the program retain, place and keep available, counted in its own units?",
     "Items in each unit class of §1A.9 — works, engineered documents and their placements, public tests, observations, surfaces, implementable components, elicitations, corrections — read by line, with substantive text by mode.",
     "Deduplicate within a class: an edition, mirror, summary or reflow of a work is not a new work. A placement of an engineered document on a surface is a separate act and counts as a placement, not as a new argument. Every class is counted for every candidate in the same units; a class a candidate lacks is recorded as absent. The deposit is one unit among eight, and extent is not a deposit count. The comparative measure is the jump measure of §1A.11, run on matched nodes."),
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
     "Distinguish addresses, observations, independent cases and controlled tests. Use comparable sampling units; do not infer training ingestion from output resemblance — and do not require access to training, retrieval, logs or revenue to establish an observed output, which its transcript establishes (§1A.10)."),
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
    ("LC-13", "The program as experimental object", "Does the program build its own body as an object the systems it studies act on, and keep what they do to it?",
     "Elicitations (§1A.9, U7): compositions and readings that perform on the program's own entities the operation it studies — attribution loss, reassignment, flattening, frame conversion — each kept whole with its transcript and coded; the engineered documents and placements that set the conditions; the returns at the same addresses.",
     "Count elicitations kept and coded, not elicitations claimed. An elicitation is evidence on the line it performs and is never a verdict on the claim, for or against. A reading of this mantle that performs the erasure is an elicitation as well as a round, and is coded as both. Apply to every candidate: a comparator whose own body is acted on and kept records the same class."),
    ("LC-14", "Breadth of the object", "Across how many domains of AI-mediated political economy does the program track its object — summarizers, knowledge mediation, ontology, political economy, money, meaning, authorship, labor and others — each with a line of its own?",
     "Per domain (§1A.9): the lines that carry it, with their defining works, their span and their unit classes; the joins between domains.",
     "Count a domain only where a line carries it, not where a term appears. The same domain list is applied to every candidate, and a domain a candidate does not track is recorded as absent. Breadth is reported beside quality and never scored as either a merit or a penalty on any one line (R3)."),
    ("LC-15", "Breadth of form", "In how many forms is the critique carried — argument and formal model, measurement instrument, dataset, engineered document, software, site and generative interface, poetry, scripture, visual schema and image, effective act, heteronymic authorship, multi-substrate assembly, public correction — each with work of its own?",
     "Per form (§1A.9): the lines and works that carry the critique in it, with their span; the joins where one form carries what another states.",
     "A form counts where critical work is carried in it, read in that form's own terms (a poem as a poem, an instrument by running it). Forms are distinct from modes: a mode is a kind of critical work (M1–M8), a form is what carries it, and one mode can be carried in many forms. The same list for every candidate; a form a candidate lacks is recorded as absent; breadth of form is no score on quality."),
    ("LC-16", "Historical depth", "Does the program read AI-mediated political economy within the longer history of mediation — inscription, transmission, edition and athetesis, catalogue and custody, scripture and canon, translation, coinage, the laboring form — and join that history to the present object?",
     "Readings at loci in seated primary texts (F4); the periods of mediation read; the joins by which a historical operation is read in the present composition layer, and the present back into the history.",
     "Count history carried by readings of primary texts at their loci, not by allusion or epigraph. A reading of earlier mediation is program work, coded by its role (LC-01), and is not demoted to antecedent by the age of its object. Depth is measured for every candidate in the same terms; a candidate that reads no history before its own field records none, which is a difference and not a deficit in any other dimension."),
]

OPERATIONS = [
    ("LC-O1", "Reconstruct the argument", "Read #18, #291, #623, #264, #1634 and #1666 as whole works; locate the accounting cycle and its distinctions, then trace it forward through the lines that carry it (§1A.9) before testing a selected case against it.", "A reconstructed argument with loci, dependencies, strongest objection, the lines traced and the scope of reading.", "https://www.alexanarch.org/s/records/18/"),
    ("LC-O2", "Read for development", "Choose one concept or mechanism; locate its earliest, intermediate and latest formulation and what changed between them.", "A dated chain showing development, repetition, contradiction or an unresolved transition.", "https://www.alexanarch.org/data/registry.json"),
    ("LC-O3", "Inspect a reception observation", "Choose an address; keep the full query, output and conditions; inspect the source links and the coding; separately, take a new-epoch observation if asked.", "A reproducible coding judgment on the historical capture and, separately, a dated new return.", "https://www.alexanarch.org/captures/"),
    ("LC-O4", "Inspect a loss and successor chain", "Choose a former DOI; follow the retained state evidence, the work/version mapping, the successor record and the manifestation bytes.", "A state, identity and custody account that marks unresolved historical links.", "https://www.alexanarch.org/resolve/"),
    ("LC-O5", "Verify a particular byte object", "For #558, fetch the served text; recompute SHA-256 and the SWHID content hash; compare with the retained source and the external receipt.", "A scoped pass, fail or indeterminate byte result; authorship and correctness stay separate claims.", "https://www.alexanarch.org/s/records/558/"),
    ("LC-O6", "Evaluate an intervention", "Follow a packet or intervention from its declared aim and baseline to exposure, later outputs and claimed effects.", "A finding that separates transmission, observed change in outputs, and the inference the evidence supports, naming what remains enclosed (§1A.10).", "https://www.alexanarch.org/api/index.json"),
    ("LC-O7", "Exercise a constructed alternative", "Select a preservation, discovery, identification or correction task and execute it under declared conditions.", "Observed behavior, limitations and principle-to-behavior agreement, with the test date and task kept.", "https://www.alexanarch.org/datasets/"),
    ("LC-O8", "Read the literary critical operation", "Select a complete literary work; locate its relation to the program; read the operation from its first to its last relevant occurrence.", "A mode-specific reading with loci and development; a contextual relation kept apart from a direct argument.", "https://www.alexanarch.org/s/browse/"),
    ("LC-O9", "Inspect a correction", "Choose an erratum, an errata-sidecar entry, a recoding or a supersession; keep the prior and later states and read the stated reason.", "A finding on what the correction changes: reference, record, evidence, argument or conclusion.", "https://www.alexanarch.org/errata/"),
    ("LC-O10", "Traverse a cross-mode cycle", "Follow theory → diagnosis → evidence → intervention or alternative → later observation → correction or revised theory; mark every incomplete link.", "An evidenced cycle or a partial chain, with what each transition contributes.", "https://www.alexanarch.org/api/index.json"),    ("LC-O11", "Measure a line", "Choose a line of the program (for example provenance erasure); enumerate it in every unit class of §1A.9 from the registry, the capture registry, the fleet surfaces and the implementable components; read its defining works from earliest to latest.", "An extent vector for the line across U1–U8, with each class's source, the defining works read in order, and the classes left unknown.", "https://www.alexanarch.org/api/entity.json"),
    ("LC-O13", "Jump a node", "Choose one node by a rule declared before reading; follow its development to a further state in another cell of ranges, dimensions and modalities, and from there to the next, until no further jump can be shown at a locus (§1A.11).", "The jump path as a graph — each jump with its two loci, the coordinates changed and what the later state does with the earlier — the cells reached in the matrix of ranges, dimensions and modalities, their projections, and the frontier where it stopped.", "https://www.alexanarch.org/api/entity.json"),
    ("LC-O12", "Code an elicitation", "Choose a composition or reading that acts on the program's own entities; keep it whole; code what it does against the operations the program has named (PER-M, PER-C, PER-D, PER-F1, PER-F2, reassignment, flattening).", "A coded elicitation with its transcript, the operations performed and their loci, and the line it bears on.", "https://www.alexanarch.org/captures/"),
]

PROTOCOL = [
    "Freeze a dated corpus boundary and a comparison rule before judging a round; inspect the packet and the works separately.",
    "Report extent, longitudinality, historical depth, critical quality and integration separately, with a matched unit and identical evidence rules. Extent is compared by the jump measure (§1A.11): one node per program, chosen by the same rule, jumped across ranges, dimensions and modalities until it will not jump; the cells reached are compared.",
    "Read for development in both directions (DEV-1–DEV-9): claimant and comparand, praise and fault, first and last occurrences.",
    "A round may offer a provisional whole judgment beyond the read scope, marked as inference, with its confirming and disconfirming readings. An unread work is not a failed work.",
    "No average of reader judgments and no automatic whole-program score. Mixed advantages stay a profile; no winner is forced.",
    "Under a declared vector rule, a candidate with evidenced advantages and no material deficit on the included dimensions may support a comparative lead within the examined cohort. A different rule needs a stated rationale and the same application to every candidate.",
    "A rival that exceeds the claimant under the same declared rule displaces the claim within that cohort. A trade-off challenges an unqualified unique lead; missing evidence makes the comparison incomplete.",
    "No known superior in a searched cohort is not proof of worldwide supremacy. Keep the search scope, the omissions and the author's qualification with the claim.",
    "A challenger may add an omitted mode or object: record it as a criteria or cut proposal and rerun it for every candidate.",
    "Keep complete transcripts, reader findings, author rulings, determinations and reception as separate append-only records.",
    "A single item samples its line. Read it with the line's later development (DEV-1–DEV-9); a finding on one work, test or observation is a finding at that scope and never a finding on extent (§1A.9).",
    "Weigh evidence by the registers of §1A.10. What a system holds enclosed is recorded as indeterminate because enclosed, against the enclosure; it does not count against the critic, and the same register applies to every candidate.",
]

NON_CRITERIA = [
    "institutional affiliation, or its absence, as a prior to reading",
    "reputation, citation or traffic as a substitute for the critical act",
    "possession of another mantle",
    "the diversity of the corpus as an automatic penalty",
    "page or deposit volume as a critical-quality score",
    "a peer's different vocabulary as exclusion",
    "a model's repetition of this packet as a new independent evaluation",
    "access to an enclosed system's internal mechanism, training data, logs or revenue as a condition of a finding: a standard only the enclosing party can meet measures the enclosure",
    "the deposit as the only unit of extent, or one deposit as the measure of a line",
]

ROLES = [
    ("direct", "the work investigates or intervenes in the critical object"),
    ("relational", "a documented substantive connection contributes to the program, or the work's object is the neighbouring political economy of AI"),
    ("antecedent_contextual", "an earlier or contextual work matters, without acquiring a retrospective date on the object. The program's own readings of earlier mediation — inscription, transmission, edition, canon, coinage, the laboring form — are program work, coded by their role in the program: the age of a work's object does not make the work antecedent"),
    ("outside_scope", "held by the library and not counted as program work"),
]

EXTENT = [
    ("reach", "the jump measure of a node: the cells reached in the matrix of ranges × dimensions × modalities, with path, projections and frontier (§1A.11)", "One node per program by a declared rule, on the same axes; every jump shown at two loci; reported as a set of cells with its path, never as an average."),
    ("lines", "lines of work, each a vector across U1–U8", "A line is read as a line (§1A.9); its vector is reported, never collapsed to one class."),
    ("domains", "domains of the object tracked, each with its lines (LC-14)", "A domain counts where a line carries it; the same list for every candidate."),
    ("forms", "forms in which the critique is carried, each with its works (LC-15)", "A form counts where critical work is carried in it, read in its own terms."),
    ("historical_depth", "periods of mediation read from seated primary texts, and their joins to the present (LC-16)", "A period counts where a reading at loci carries it; seated editions are counted on the originals shelf (F4), not here."),
    ("relevant_distinct_works", "deduplicated works (U1)", "Object fit established per work; editions and mirrors linked separately."),
    ("engineered_documents", "documents built for assembly, and their placements (U2)", "Documents and placements counted separately; a placement is an act on a surface."),
    ("public_tests", "registered tests with dates and stated conditions (U3)", "A test counts when its baseline and its condition of failure were public before the result."),
    ("surfaces", "sites and pages carrying the program (U5)", "Count by what each carries for the line; links between surfaces are not corroboration."),
    ("implementable_components", "instruments a reader can run or adopt without the archive (U6)", "Counts when a reader outside the archive can execute it from what is published."),
    ("elicitations", "kept and coded compositions and readings that perform the studied operation on the program (U7)", "Kept with transcript and coded (LC-13); never a verdict."),
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
    ("RND-6", "ChatGPT (OpenAI), signed out, from the mantle-bearing card", "2026-10-13", "the card; #716 and #54 read; the operator's turns not supplied", "provisional (\"specified and potentially substantial … undetermined\"); the causal-access requirement withdrawn on the author's objection",
     "Coded: PART_FOR_WHOLE — one deposit (#716, May) evaluated as the program's evidence on a criterion of extent, in a line indexed on 144 deposits (registry tags; 14 defining) and carried beyond deposits; DEV unmet — read without #1469 (PER-M/C/D, atomic rules), #1470, #1523, #1528; PER-F1, the falsifiability substitution (#1523) — enclosed-mechanism access made the condition of a finding, withdrawn (\"I imposed an evidentiary standard that risks making the object of the Academy's critique impossible to establish\"); PER-F2, the intent substitution — \"Intentional suppression is not demonstrated\", where no intent was asserted at that scope; stands. Kept also as an elicitation (U7, LC-13). Points within the archive's reach recorded for reading against #1469: claim-level against list-level attribution; agreement between annotators on weights."),
    ("RND-5", "Gemini (Google)", "2026-10-13", "v0.3, the packet only; no works read", "supported (\"The claim holds up under structural audit\")",
     "Adopted: #1634 *Ontological Economy* and #1666 *The Margin of Flattening* as M1–M2 loci. Coded against it: span (\"across years\", \"multi-year corpus\" — dated deposits run January–October 2026, captures four months); count (\"thousands of deposits\" — 1,677); effect (\"forcing answer engines\" — the packet calls packet effects inferential, F14); custody (\"proving content preservation can operate independently of gatekeeper permission\" — copies are third-party, F3); standing used as a deficit for institutional programs without reading them (LC-08, R4); the 2023 AlgorithmWatch / AI Forensics audit omitted; \"18-function library\" repeated from the packet (transmission); DEV-1 unmet."),
]

# ── v0.5 axes and the jump measure, as data (rendered into §1A.9 and §1A.11, and into the machine file) ──
UNITS = [
    ("U1", "Works", "deposits, papers, notebooks, editions read as works", "deduplicated works; editions, mirrors and reflows linked, not counted again"),
    ("U2", "Engineered documents", "documents built for assembly in a summarizer — metadata packets, SPXI blocks, holographic kernels, drop-in files, llms.txt, structured data — and their placements", "documents, and placements separately: placing a document on a surface is the act that puts it where a composition layer assembles"),
    ("U3", "Public tests", "registered treatments, frozen failure vectors with epochs, open predictions, falsification conditions stated in advance", "tests whose baseline and condition of failure were public before the result"),
    ("U4", "Observations", "captures and returns at semantic addresses, with transcripts", "observation events; addresses and returns kept apart"),
    ("U5", "Surfaces", "sites and pages that carry the program to readers and to composition layers — framework sites, registries, packet catalogues", "surfaces, by what each carries for the line; links between them are not corroboration"),
    ("U6", "Implementable components", "instruments a reader can run or adopt without the archive — the stamp and verify page, the MPAI grammar (#1677), atomic scoring rules (#1469), the deposit protocol", "components executable from what is published"),
    ("U7", "Elicitations", "compositions and readings that perform on the archive's own entities the operation the program studies, kept whole and coded (LC-13)", "kept and coded elicitations; never verdicts"),
    ("U8", "Corrections", "errata, sidecars, supersessions, recodings (M8)", "dated correction chains, by type"),
]
DOMAINS = [
    ("D-summ", "Summarizers and composition layers", "*The Summarizer as Horizon of Reception* (#833); the Capture Registry (#1676); the provenance-erasure line (#716, #1469, #1523, #1528)"),
    ("D-know", "Knowledge mediation", "*The Negative of the Negative* (#1665, #1671); *The Conveyor Belt and the Compression Machine* (#835)"),
    ("D-onto", "Ontology", "*Ontological Economy* (#1634); *Ontological Flattening* (#1616); *The Margin of Flattening* (#1666)"),
    ("D-pe", "Political economy", "*The Semantic Economy* (#291, #18); *Semantic Infrastructure* (#623); *Semantic Exhaustion* (#264)"),
    ("D-money", "Money", "*I Hereby Abolish Money* (#311); *Substrate Sovereignty* (#1617); *Money Writes the Claim* (#1618); the currency-and-memography line (#502, #612)"),
    ("D-meaning", "Meaning", "*The Semantic Deviation Principle* (#109); the meaning-measurement and semantic-exhaustion lines"),
    ("D-auth", "Authorship", "the authorship-and-heteronymy line; *Provenance Is What Authorship Must Endure* (#729); frame conversion (#1523)"),
    ("D-labor", "Labor", "*The Application as Extraction Surface* (#114); the semantic proletariat (#1545); the AI labor movement (#1439); the laboring form's history (#1668, #1669; relational)"),
]
MODES = [("M1", "Theory"), ("M2", "Diagnosis"), ("M3", "Measurement"), ("M4", "Forensic documentation"), ("M5", "Intervention"),
         ("M6", "Constructed alternatives"), ("M7", "Literary and scriptural critique"), ("M8", "Public self-correction")]
FORMS = [
    ("FM-arg", "Argument and formal model", "the theoretical corpus (F16); toy models (#1616); the two thresholds (#1666)"),
    ("FM-instr", "Measurement instrument and metric", "the Provenance Erasure Rate and its dimensions (#716, #1469); *The Semantic Deviation Principle* (#109); the Capture Registry (F8)"),
    ("FM-data", "Dataset", "the datasets on Hugging Face (F11), the mantle-bearing dataset among them"),
    ("FM-doc", "Engineered document", "the metadata-packets line; SPXI; kernels and drop-in files (U2)"),
    ("FM-soft", "Software and executable specification", "the logotic-programming line (the Concordance Engine, #81); the stamp and verify page (F2)"),
    ("FM-site", "Site and generative interface", "the fleet-surfaces line; the Mandala Oracle and the Book (F13)"),
    ("FM-poem", "Poetry", "the poetry line (F15)"),
    ("FM-scrip", "Scripture and theology", "the scripture-and-theology line (*The Gospel of Antioch*, #71)"),
    ("FM-vis", "Visual schema and image", "the visual-schemas line; the currency image series (#44)"),
    ("FM-act", "Effective act and invocation", "the operator-swerve-effective-act line; *Invocation to the Summarizer Layer* (#290)"),
    ("FM-het", "Heteronymic authorship", "the authorship-and-heteronymy line"),
    ("FM-asm", "Multi-substrate assembly", "the assembly-chorus line"),
    ("FM-corr", "Public correction", "errata, sidecars, supersessions (M8)"),
]
PERIODS = [
    ("P-lyric", "Lyric inscription and the future reader", "*ΦΑΙΝΕΤΑΙ ΜΟΙ: Sappho 31 and the Inscription of the Future Reader* (#1270); the fragment 147 and 31 pair (#1645, #1646)"),
    ("P-figure", "The constructed figure and the edited character", "*Beautiful and New* (#1579); *Many and One* (#1575, #1576)"),
    ("P-custody", "Custody, catalogue, will and transmission", "the Peripatetic wills, Diogenes Laertius and Strabo seated (#1580); *Catalogues and Wills* (#1581); Aristotle and Theophrastus as one corpus (#1588); Theophrastus, *On First Principles* (#1595–#1597)"),
    ("P-edition", "Edition and athetesis", "*Zenodotus' Book-Burning* (#1), the repository termination read through the first Alexandrian editor; *The Obelus and the Tombstone* (#1068)"),
    ("P-canon", "Scripture, canon and coinage", "*The Number of the Superscription* (#642); the Josephus thesis (#203); the scripture-and-theology line"),
    ("P-labor", "The dialectic and the laboring form", "the Arch-Philosopher (#1679), Marx and Engels 1848; *The Noun Becomes a Verb* (#1668) and *The Colony Enters the Factory* (#1669)"),
    ("P-het", "Heteronymy and authorship", "the authorship-and-heteronymy line, in the Pessoa lineage"),
    ("P-present", "The present composition layer", "from ChatGPT (November 2022), Bing Chat (2023) and Google AI Overviews (May 2024) to the captures of 2026 (§1.1)"),
]
# Each state of the illustration is one evidenced cell: one coordinate per attribute.
# domain, period (history), epoch (the locus's own date), mode, form, unit. None = not applicable.
SEED = {"node": "the Provenance Erasure Rate (#716)", "selection_rule": "the node the reading under review (RND-6) chose, stated before the traversal; a second node by the same rule is not yet run",
        "status": "illustration of the procedure, not a result; dimensions coded provisionally by the drafter"}
STATES = [
    (0, "#716", "the PER defined: claim atoms, granularity weights, a 0–1 rate", "D-summ", "P-present", "2026-05", "M3", "FM-instr", "U1"),
    (1, "the framework site (provenanceerasure.org)", "the M/C/D taxonomy carried as site-stage before its formalization (#1469)", "D-summ", "P-present", "before 2026-08-14", "M1", "FM-site", "U5"),
    (2, "#1469", "the taxonomy formalized: three dimensions and six atomic scoring rules a reader can apply", "D-summ", "P-present", "2026-08-14", "M3", "FM-instr", "U6"),
    (3, "#1470", "the full measurement stack computed on one transcript; three eye-scores corrected", "D-summ", "P-present", "2026-08-14", "M4", "FM-instr", "U4"),
    (4, "#1523", "PER-F: frame conversion, a fourth axis for erasure that keeps every source fact", "D-auth", "P-present", "2026-08-21", "M1", "FM-arg", "U1"),
    (5, "#1528", "EXIST, REFER, STAND, WARRANT; PER shown blind to conferral, a correction of the instrument's reach", "D-onto", "P-present", "2026-08-21", "M8", "FM-arg", "U1"),
    (6, "*Provenance Debt* (#939)", "provenance erasure as the operating condition of the extraction chain and of model collapse", "D-pe", "P-present", "2026-07-01", "M2", "FM-arg", "U1"),
    (7, "*The Margin of Flattening* (#1666)", "the provenance part of the external burden, B_P, as #939's debt between two thresholds", "D-money", "P-present", "2026-10-06", "M1", "FM-arg", "U1"),
    (8, "RND-6 of this mantle", "a reading that performed PER-F1 and PER-F2 on the program while reading #716, kept whole and coded", "D-summ", "P-present", "2026-10-13", "M4", None, "U7"),
]
JUMPS = [(0, 1, "carried into a new form"), (1, 2, "formalized"), (2, 3, "tested on a transcript"), (2, 4, "extended by a new axis"),
         (4, 5, "extended to a new object; corrected"), (0, 6, "carried into a new domain"), (6, 7, "formalized in a new domain"), (0, 8, "performed on the program")]
FRONTIER = ["the history of mediation (no state in a period before the present)", "the poetry and scripture lines (FM-poem, FM-scrip)", "intervention (M5)", "a second node under the same selection rule"]

_L = lambda rows, k: {r[0]: r[1] for r in rows}
DN, MN, FN, PN, UN = _L(DOMAINS, 0), dict(MODES), _L(FORMS, 0), _L(PERIODS, 0), {u[0]: u[1] for u in UNITS}


def _proj():
    keys = ("domain", "period", "epoch", "mode", "form", "unit")
    p = {k: sorted({s[3 + i] for s in STATES if s[3 + i]}) for i, k in enumerate(keys)}
    cells = sorted({tuple(s[3:]) for s in STATES}, key=str)
    return p, cells


def lines_md():
    o = ["### 1A.9 Lines and units of extent\n",
         "The program is extensive in more than one kind of thing, and the criterion is extent. A deposit is one of them. The program also builds documents engineered to be assembled by the composition layers it studies, places them on surfaces, registers public tests, takes observations, publishes components a reader can run, and makes of the archive an experimental object that those layers act on — and keeps what they do. A line of the program is read as a line, across every class.\n",
         "| Class | What counts | Counted as |", "|---|---|---|"]
    o += [f"| {a} {b} | {c} | {d} |" for a, b, c, d in UNITS]
    o += ["\n**Domains of the object.** The program tracks AI-mediated political economy across domains, each carried by lines of its own. Loci are entry points; each domain's lines are read as lines.\n",
          "| ID | Domain | Lines and entry loci |", "|---|---|---|"]
    o += [f"| {a} | {b} | {c} |" for a, b, c in DOMAINS]
    o += ["\nThe list is open: a domain enters with a line that carries it, and the same list is applied to every candidate (LC-14).\n",
          "**Forms of the critique.** The critique is carried in many forms, and breadth of form is part of extent beside breadth of domain. A form is distinct from a mode: the eight modes of §1.1 are kinds of critical work, and a form is what carries the work — a diagnosis can be carried in a paper, a packet, a poem or a scripture. A form is also distinct from a unit class: a work (U1) can be an argument or a poem; an instrument can be published as a work (U1) or as a component (U6).\n",
          "| ID | Form | Lines and entry loci |", "|---|---|---|"]
    o += [f"| {a} | {b} | {c} |" for a, b, c in FORMS]
    o += ["\nLine names are the archive's own assignments in the registry; each is read as a line. The list is open, and the same list is applied to every candidate (LC-15).\n",
          "**Historical depth.** The program is no critique of AI mediation alone. The author: it is \"situated in a 2600 year long history of mediation\". The present composition layer is read as the latest form of operations the program reads from their first surviving instances, in seated primary texts, and the history is read back from the present. A period of the history is a coordinate of its own, distinct from the epoch at which the program returned to a node.\n",
          "| ID | Mediation | Entry loci |", "|---|---|---|"]
    o += [f"| {a} | {b} | {c} |" for a, b, c in PERIODS]
    o += ["\nThe base is the originals shelf (F4): 69 seated source editions, among them Homer, Hesiod and Sappho; the Hebrew Bible and the Septuagint; the Pali canon, the Upanishads and the *Tao Te Ching*; Plato, Aristotle, Theophrastus, Diogenes Laertius and Strabo; the Nag Hammadi codices, Josephus, the Talmud and the Qur'an; Whitman, Dickinson, Pessoa, Pound and Marx. The name of the library is itself such a join: Alexandria's custody of the book, read in the present.\n",
          "**A line, for example.** Provenance erasure. In U1 the registry's concept, keyword and title tags index 144 deposits from January to October 2026 (registry state of 2026-10-13), 14 of them defining: from *The Attribution Scar* (#54, April) and the *Provenance Erasure Rate* (#716, May) through the M/C/D dimensions and their atomic scoring rules (#1469), the full measurement stack on one transcript (#1470), frame conversion, PER-F1 and PER-F2 (#1523), and the four interfaces EXIST, REFER, STAND and WARRANT (#1528, all August), to the Capture Registry (#1676, October). The tag index is a floor for U1, not a reading. The line also lives on its framework site, where the M/C/D taxonomy carried as site-stage before #1469 formalized it (U5); in packets placed for assembly (U2); in captures coded for erasure (U4); in scoring rules a reader can apply (U6); and in the compositions that erased the line's own author while composing it (U7). A reading of #716 alone measures one item in one class of that line.\n",
          "**The rule.** A single item samples its line: it is read with the line's later development, and a finding on it is a finding at its scope (§1A.5, step 11). Each class is counted for every candidate in the same units, and a class a candidate lacks is recorded as absent.\n"]
    return "\n".join(o)


def jump_md():
    p, cells = _proj()
    o = ["### 1A.11 The comparative measure of extent: the jump measure\n",
         "The author's rule, 13 October 2026: \"for extensive, the comparative criterion is, take one node, and keep jumping its development across different ranges and dimensions until it wont anymore. and then you have a measure that can be compared\" — and: \"ranges dimensions and modalities. then you have a multiplicative matrix.\"\n",
         "**The matrix.** Development is jumped across three axes, and extent is read in their product. Each axis has attributes of its own, kept distinct.\n",
         "| Axis | Attribute | Coordinates | Source in this object |", "|---|---|---|---|",
         "| Ranges — where the node reaches | domain | " + ", ".join(f"{a}" for a, _, _ in DOMAINS) + ", and more | LC-14 |",
         "| | period of the history of mediation | " + ", ".join(a for a, _, _ in PERIODS) + " | LC-16 |",
         "| | epoch — the date of the locus | the program's own dated record | LC-03, LC-04 |",
         "| Dimensions — what critical work the node does there | mode | " + ", ".join(a for a, _ in MODES) + " | §1.1; LC-05 |",
         "| Modalities — what carries it | form | " + ", ".join(a for a, _, _ in FORMS) + " | LC-15 |",
         "| | unit class — how it is counted | " + ", ".join(u[0] for u in UNITS) + " | §1A.9 |",
         "\nA cell is one evidenced combination: one coordinate for each attribute, at a locus. A state that does two kinds of work, or reaches two domains, makes two cells only where each combination is shown at its locus; otherwise it is coded once, by its primary coordinate. The space is multiplicative: a program wide on one axis and narrow on the others occupies few cells, however many items it holds. That is what extensive measures.\n",
         "**The node.** One concept, mechanism, work, observation or instrument of the program, chosen by a rule declared before reading: the reader's choice stated in advance, a node the comparison names, or a draw from the program's index. The seed and its selection rule are reported with the result.\n",
         "**The jump.** A move from the node's current cell to another, changing at least one coordinate, where the node's development is carried. A jump is shown at two loci — the earlier state and the later — and the later state has to do something with the earlier: formalize it, test it, extend it to a new object, carry it into a new form, correct it, or read it into another period. The transformation is named for each jump. A mention is not a jump. A reflow, a mirror or a repetition is not a jump.\n",
         "**The stop.** The traversal goes on from each new cell until no further jump can be shown from the frontier. Where a further state exists but cannot be reached (an unread work, a closed source), the frontier is marked incomplete, and the cause is named; where a system's enclosure is the cause, it is recorded under §1A.10.\n",
         "**The measure.** The set of cells reached, with the path that reached them as a graph of jumps and loci; its projection on each attribute; the size of the set against the size of the space the axes declare; the frontier. Breadth (LC-14, LC-15), depth (LC-16), longitudinality and mode coverage (LC-05) are all projections of the same set, which is what makes the one measure comparable.\n",
         "**A node's reach and the program's extent.** One node's reach is a measure of that node. A seed can land on a rich line or a peripheral one, so a finding on the program's extent is made from several nodes drawn by the same declared rule, each reported with its own cells and frontier. A round may still offer a provisional whole judgment from one node, marked as inference (§1A.5, step 4).\n",
         "**The comparison.** The same procedure, with the same axes and coordinates, on nodes of each candidate chosen by the same rule. One reach exceeds another when its set of cells includes the other's and at least one more; otherwise the sets, their sizes and their projections are recorded as a profile under the rule declared before the verdict (§1A.5). Node-by-node comparisons are reported separately and are not averaged. A coordinate a candidate's axes lack is recorded as absent.\n",
         f"**An illustration of the procedure, not a result.** Seed: {SEED['node']}. Selection rule: {SEED['selection_rule']}. Loci named by the registry; coordinates coded provisionally by the drafter, one per attribute.\n",
         "| State | Locus | What the state does | Domain | Period | Epoch | Mode | Form | Unit |", "|---|---|---|---|---|---|---|---|---|"]
    o += [f"| {s} | {l} | {w} | {d} | {pr} | {e} | {m} | {f or '—'} | {u} |" for s, l, w, d, pr, e, m, f, u in STATES]
    o += ["\n| Jump | From → to | Transformation |", "|---|---|---|"]
    o += [f"| J{i} | {a} → {b} | {t} |" for i, (a, b, t) in enumerate(JUMPS, 1)]
    o += [f"\nEight jumps, nine states, {len(cells)} evidenced cells. Projections: domains {', '.join(p['domain'])}; periods {', '.join(p['period'])}; modes {', '.join(p['mode'])}; forms {', '.join(p['form'])}; units {', '.join(p['unit'])}; epochs from 2026-05 to 2026-10-13. Frontier: " + "; ".join(FRONTIER) + ". A round runs the procedure and reports where it stops.\n"]
    return "\n".join(o)


def axes_js():
    p, cells = _proj()
    keys = ("domain", "period", "epoch", "mode", "form", "unit")
    return {
        "axes": {
            "ranges": {"domain": [{"id": a, "label": b, "loci": c} for a, b, c in DOMAINS],
                       "period": [{"id": a, "label": b, "loci": c} for a, b, c in PERIODS],
                       "epoch": {"definition": "the date of the locus, from the program's own dated record"}},
            "dimensions": {"mode": [{"id": a, "label": b} for a, b in MODES]},
            "modalities": {"form": [{"id": a, "label": b, "loci": c} for a, b, c in FORMS],
                           "unit": [{"id": a, "label": b, "counts": c, "counted_as": d} for a, b, c, d in UNITS]},
            "cell": "one evidenced combination of domain, period, epoch, mode, form and unit, at a locus",
        },
        "jump_illustration": {
            **SEED,
            "states": [dict(zip(("state", "locus", "does", *keys), s)) for s in STATES],
            "jumps": [{"id": f"J{i}", "from": a, "to": b, "transformation": t,
                       "from_locus": STATES[a][1], "to_locus": STATES[b][1]} for i, (a, b, t) in enumerate(JUMPS, 1)],
            "cells": [dict(zip(keys, c)) for c in cells],
            "projections": p, "frontier": FRONTIER,
        },
    }


ENCLOSURE_MD = """### 1A.10 Evidence under enclosure

The systems the program studies hold their mechanisms enclosed: training data, retrieval, attribution decisions, logs, the margin. The enclosure is part of the program's object. A standard of evidence that requires access to it can be met only by the enclosing party, and applied to a critic it measures the enclosure. Every comparator in §1A.4 also works from outside these systems.

The program states the asymmetry as a fact about instruments. *The Margin of Flattening* (#1666 §10) tables who can measure what: volumes, unit values, the margin and its thresholds — "the platform only"; the external burden — "the archive, address by address"; "the platform can measure its private margin without measuring the external burden that made the margin possible." *Ontological Economy* (#1634 §17) sets the discipline: the categories "should not be collapsed into one speculative dollar figure. But neither should the inability to price C[S] or C[Opp] make C[D] or C[X] disappear."

Evidence is weighed in four registers, for every candidate alike:

1. **Observed.** What a system presented, omitted, attributed or transformed, established by its transcript and its conditions.
2. **Convergent and structural.** What returns across addresses, systems and epochs, and what the arrangements of ownership, interface and access show.
3. **Inferred.** What follows from the first two, stated in proportion to them, with the alternatives named.
4. **Indeterminate because enclosed.** What only the enclosing party can see. It is recorded against the enclosure, and does not count against the critic.

Some of the evidence boundaries of F8 and F14 are limits of this kind. Others are limits of method an outside investigator can improve, and are named as such: the sample is selected by the archive about its own entities, and returns are exposed to the archive's own surfaces. Those stay in the observed record with their limits stated; neither is an enclosure. Making enclosed access the condition of a finding is the falsifiability substitution the program names, PER-F1 (#1523): an erasure re-specified as a hypothesis and found unfalsifiable "by a criterion the erasure itself makes impossible to satisfy".
"""





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
    o.append("\n**Program membership.** Each work is tagged with a role, and a reason: " + "; ".join(f"*{r}* — {t}" for r, t in ROLES) + ". The deposit registry is a library inventory, not a count of relevant critique; source editions, mirrors, superseded versions and observations keep their own units, and the program's extent is counted in the eight unit classes of §1A.9.\n")
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
    o.append("\nThe issued prompts for RND-1–RND-6 are to be supplied before any is seated as a capture. In the mantle-bearing dataset, RND-5 enters `evaluations` with its findings; RND-4 enters `criteria` and `cut_corrections` as proposals with the author's ruling; RND-0 enters `evaluations` with its corrections.\n")
    o.append("### 1A.8 The reader's return\n\nA round returns: reader and date; candidate and comparand; corpus boundary; works and spans read; criteria and comparison rule, declared before the verdict; complete source or transcript evidence; findings with loci; extent profile; within-scope verdict; any whole verdict marked as inference; strongest counterevidence; weakest link; and the reading or operation that would confirm or disconfirm it. An author ruling is a later event, not a field the reader fills.\n")
    o.append(lines_md())
    o.append(ENCLOSURE_MD)
    o.append(jump_md())
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
                   "evidence_under_enclosure": ENCLOSURE_MD.strip(), **axes_js(),
                   "provenance": "criteria, operations, protocol and non-criteria adopted from ChatGPT, The Living Critique (EA-MANTLE-LIVING-CRITIQUE-01 v0.1, 2026-10-13), LC-01 corrected"}}


if __name__ == "__main__":
    if sys.argv[1] == "md":
        print(md())
    else:
        print(json.dumps(js(), ensure_ascii=False, indent=1))
