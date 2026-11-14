"""The new ledger claims for the CRJ row revision of 2026-11-14: field (F58–F88, sources B17–B35) and archive
(D1769-*, D1766-01, D1749-18, CAP-3-* .. CAP-6-*). Quotes are verbatim from the saved texts, the registry or the deposit
texts; verify.py checks every one."""
import json
from vlib import ROOT, registry, entry

CAPURL = "https://www.alexanarch.org/captures/"
AXN1769 = "AXN:0C9A.MPAI.🧡🟠💎🕌🪞🀄"
AXN1766 = "AXN:0C8B.GENERATIVE.📎🌳🔝🌒▽🌹"
AXN1749 = "AXN:0C40.GENERATIVE.🍂🕛🜁⚓🪦🪝"
T1769 = "Daffodils: Classical Receptions Journal, 2009–2026 — The Framework Hologram (EA-HK-DAFFODILS-01 v1.1)"
T1766 = "Critique of Pure Inference: The Formation of Objects, the Conditions of Warrant, and the Standing of Conclusions"
T1749 = "“But I Must Dare All”: Sappho 31 and the Composition Layer as a Surface of Classical Reception (v10)"
DEPQ = "within the deposit text as loaded (whitespace-normalised; markdown emphasis stripped)"


def dep(i, d, locus, quote, claim, kind="interpretation", mod="interpretation", strata=("D",), lineage="the audit", kernel=False,
        date="2026-11-14", file=None, axn=None, title=None):
    files = {1769: "data/texts/AXN-0C9A-text.md", 1766: "data/texts/AXN-0C8B-text.md", 1749: "data/texts/AXN-0C40-text.md"}
    return {"id": i, "dep": d, "axn": axn or {1769: AXN1769, 1766: AXN1766, 1749: AXN1749}[d], "claim": claim, "kind": kind,
            "modality": mod, "strata": list(strata), "locus": locus, "quote": quote, "kernel": kernel, "const": False,
            "lineage": lineage, "date": date, "title": title or {1769: T1769, 1766: T1766, 1749: T1749}[d], "creator": "Sharks, Lee",
            "file": file or files[d], "quote_ok": None, "quote_check": DEPQ}


A = [
    dep("D1769-01", 1769, "§0.4", "The journal's Editor-in-Chief is Dr Justine McConnell (King's College London). She signed the decision of 7 November 2026 on Closing the Fragment, which was reviewed by two anonymous referees.",
        "the Editor-in-Chief, Dr Justine McConnell (King's College London), signed the decision of 7 November 2026; two anonymous referees", "fact", "documented", ("D",), "who signs", True),
    dep("D1769-02", 1769, "§0.4", "The referees are anonymous; the editor is named, and the editor answers for the journal's decisions. The founding editor was Lorna Hardwick (Open University), whose editorials run through the early volumes (2009–2014).",
        "the referees anonymous, the editor named and answering for the decisions; founding editor Lorna Hardwick", "fact", "documented", ("D",), "who signs"),
    dep("D1769-03", 1769, "§0.1", "Crossref's register of Classical Receptions Journal (ISSN 1759-5142), read 14 November 2026: 405 works, 2009–2026. … 185 abstracts (from 2019 on; the 2009–2018 works carry none);",
        "the register read 14 November 2026: 405 works, 185 abstracts", "fact", "documented", ("D",), "what its pages hold"),
    dep("D1769-04", 1769, "§2.4", "No title or abstract takes a search engine, an encyclopedia platform, a recommender or a composing model as a receiver of antiquity. … That is a bounded census finding.",
        "no title or abstract takes a machine as receiver of antiquity; a bounded census finding", "fact", "documented", ("D",), "what its pages hold", True),
    dep("D1769-05", 1769, "§2.4.1", "None of the 37 open-licensed articles takes a search engine, a platform or a composing model as a receiver.",
        "none of the 37 open-licensed articles takes a machine as receiver", "fact", "documented", ("D",), "what its pages hold"),
    dep("D1769-06", 1769, "§2.6.2", "The classics are the object the field receives toward. They are almost never an object the field reopens.",
        "the classics received toward, almost never reopened", "interpretation", "interpretation", ("D", "O"), "the classics as the pre-inferential object"),
    dep("D1769-07", 1769, "§9.10.1, §9.10.4", "Source → later work: the ancient text held fixed, a later work read against it | 141 … Across the 185, the journal's arguments overwhelmingly hold the classical source as a fixed premise: 141, with 12 more about the field's own terms. Arguments that reach the source exist, 32 of them, and nine are governing in scale. Each of the nine revises one interpretation or one determination. None reopens a canonical work's attribution, dating or standing reading.",
        "141 of 185 source → later work; 12 on the field's terms; 32 reach the source, 9 governing; none reopens attribution, dating or standing reading", "fact", "documented", ("D",), "the classics as the pre-inferential object", True),
    dep("D1769-08", 1769, "§9.10.4", "One record is evidence about one decision.", "limit: one record, one decision", "interpretation", "self-description", ("D",), "the decision on CLASSREC-2026-062"),
    dep("D1769-09", 1769, "§6.2", "Two institutions, two acts. The editorial decision belongs to the journal. The false attribution belongs to Google's composition layer. The journal did not request the credit and does not control it.",
        "two institutions, two acts: the editorial decision; the composition layer's false attribution, not requested or controlled by the journal", "interpretation", "interpretation", ("D", "R"), "after notice"),
    dep("D1769-10", 1769, "§6.2", "The repair test has to follow two relations, because they can come apart: whether the false recipient disappears, and whether the warranted relation between author and work returns. On 14 November they came apart (§9.6).",
        "the two-relation repair test; on 14 November the relations came apart", "interpretation", "stipulation", ("D", "R"), "after notice", True),
    dep("D1769-11", 1769, "§9.6.1", "The false recipient: removed. The credit to the journal is withdrawn, and the withdrawal holds. … The warranted relation: not restored. The credit moves to IJCT's Future Pasts issue and the CRSN call, and the author and #833 are absent.",
        "false recipient removed; warranted relation not restored: the credit moved to IJCT and the CRSN, the author and #833 absent", "fact", "documented", ("D", "R"), "after notice"),
    dep("D1769-12", 1769, "§6.4.3.2", "Reviewer 2 finds the main arguments \"read as LLM-generated\", says this \"brings into question the degree of authorial contribution\", and reports that \"the editors have been advised to use AI detection software\". This is an allegation about authorship.",
        "the second report's statements, read as an allegation about authorship", "attribution", "attributed", ("D",), "the decision on CLASSREC-2026-062"),
    dep("D1769-13", 1769, "§6.4.3.2", "The allegation is made anonymously. … It reaches the author inside a decision letter, signed by the named editor, that declines the manuscript \"In light of these comments\". The letter does not separate the editor from the allegation.",
        "the allegation anonymous, delivered inside the letter signed by the editor, not separated from the editor", "fact", "documented", ("D",), "the decision on CLASSREC-2026-062"),
    dep("D1769-14", 1769, "§6.4.3.2", "The editor is accountable for the decision and for transmitting the allegation within the reports that support it (§0.4). The signature does not show endorsement of each sentence. The record does not show how the allegation was assessed, or whether it contributed to the decision.",
        "the editor accountable for the decision and for transmitting the reports; the record silent on how the allegation was weighed", "interpretation", "interpretation", ("D",), "who signs", True),
    dep("D1769-15", 1769, "§6.4.3.2", "A control the journal will recognize: the editor's own article (§7.11.6), written and accepted in 2015, seven years before public chat models. In 9,919 words of its text it has: … \"not only … but also\" or \"not only … but\": 7 times … \"not …, but\": 12 times … spaced dashes standing for em-dashes: 31.",
        "the control: the editor's 2015 article, 9,919 words: 7, 12 and 31", "fact", "documented", ("D",), "the decision on CLASSREC-2026-062", True),
    dep("D1769-16", 1769, "§6.4.3.2", "The markers the report names occur in the editor's 2015 article at these rates. They predate public chat models and belong to the register of academic English, so they carry no diagnostic weight as evidence of deficient authorial contribution.",
        "the markers carry no diagnostic weight", "interpretation", "interpretation", ("D",), "the decision on CLASSREC-2026-062"),
    dep("D1769-17", 1769, "§6.4.3.1, §6.4.4", "On one point Reviewer 2 is right about v6. The version sent omitted the manuscript's own statement of how it was made, and the open letter says so (#1750). … Several of the defects are real, and the open letter accepts some in full (#1750).",
        "conceded: several defects real; v6 omitted its statement of how it was made", "fact", "self-description", ("D",), "the decision on CLASSREC-2026-062", True),
    dep("D1769-18", 1769, "§6.4.4", "Neither report assesses the manuscript's philological argument or its question. … The editor declined, \"In light of these comments\", without an invitation to revise.",
        "neither report assessed the argument or the question; the editor declined without an invitation to revise", "fact", "documented", ("D",), "the decision on CLASSREC-2026-062"),
    dep("D1769-19", 1769, "§6.4.3.2", "Like Reviewer 1's empirical route (§6.4.2.1), the route Reviewer 2 offers is a paper the journal has never published.",
        "both routes offered are papers the journal has never published", "fact", "documented", ("D",), "the decision on CLASSREC-2026-062"),
    dep("D1769-20", 1769, "§6.4.3.2", "Of the 37 open-licensed articles, none discloses an author's use of AI, OCR, language models or editing software. … The procedure has a category for undisclosed use, and a vendor's language correction for sale at the front end. It has no category for declared composition as method.",
        "no open article discloses AI use; no category for declared composition as method", "interpretation", "interpretation", ("D",), "its rules on AI"),
    dep("D1769-21", 1769, "§6.5", "The journal's own first encounter is now composed by the receiver it has not studied. … On 14 November ChatGPT, asked how the archive critiques it, gave the journal's decision to \"CRJ\", \"the journal\" and \"the reports\" and named no editor (v12.680).",
        "the journal's first encounter composed by the receiver it has not studied; the decision given to the journal, no editor named", "interpretation", "interpretation", ("D", "R"), "the record of its reception"),
    dep("D1769-22", 1769, "§6.5.1, the finding", "The composition's sources for the journal are the publisher's pages, two wikis, a ranking, three sister venues, a network's call and a publisher's AI policy. None of them studies a machine as receiver.",
        "none of the composition's sources studies a machine as receiver", "fact", "documented", ("D",), "the record of its reception"),
    dep("D1769-23", 1769, "§6.5.1 k", "It is the field's newest programmatic statement on AI, and it defines reception as human, with the machine as foil.",
        "the CRSN call defines reception as human, the machine as foil", "interpretation", "interpretation", ("O",), "literary reception and large language models"),
    dep("D1769-24", 1769, "§6.5.1 j", "AI enters as theme and tool. No paper takes a composing model as receiver.",
        "Future Pasts: AI as theme and tool, no composing model as receiver", "interpretation", "interpretation", ("O",), "the field on AI"),
    dep("D1769-25", 1769, "§7.11.6.7", "K1: the article places the colonizing act in the classical texts and never in the discipline (\"discipline\" 0). … K2: of six points where the receiving works recognize the discipline's colonization of the classics, two are redirected and four are absent.",
        "the editor's article: K1 and K2 with their counts", "interpretation", "interpretation", ("D", "R"), "the editor's article", True),
    dep("D1769-26", 1769, "§7.11.6.2", "It is a well-documented, widely cited article that gives the active force to Black and African writers.",
        "the innocent reading of the editor's article", "interpretation", "interpretation", ("D",), "the editor's article"),
    dep("D1769-27", 1769, "§7.11.6.6", "Against the criteria: the colonizing act is placed in the classics (K1). None of the six points of contact is carried (K2: 0 of 6). The discipline is absent, as in the article. The editor is named \"Justin McConnell\".",
        "at the editor's address: K1 in the classics, 0 of 6, the editor named 'Justin'", "fact", "documented", ("D",), "the record of its reception"),
    dep("D1769-28", 1769, "§7.11.6.1", "8.2, 133–154 (Crossref 10.1093/crj/clv002, issued online 7 May 2015). It is the editor's only work in the journal.",
        "the editor's article: CRJ 8.2, 2015; her only work in the journal", "fact", "documented", ("D",), "the editor's article"),
    dep("D1769-29", 1769, "§9.2.1", "What is measured in the absence is the field, and CRJ, its most taken-up journal, stands for it. What is particular to CRJ is the decision of 7 November and the credit of 10 November.",
        "the absence field-wide; CRJ the most taken-up journal; particular to it the decision and the credit", "interpretation", "interpretation", ("D",), "two readings"),
    dep("D1769-30", 1769, "abstract; §1.5", "It asks what the journal's 405 works advance, for whom and with what uptake, and whether they meet the conditions that make classical reception matter now. … This is a working venue doing what a specialist journal does. The reading below accepts all of it. Its question is narrower: how standing moves through the journal, what kind of knowledge it is built to produce, who can use that knowledge, and what it does in the present.",
        "the audit accepts the received reading and asks how standing moves, what knowledge, for whom, to what effect", "interpretation", "stipulation", ("D",), "two readings", True),
    dep("D1769-31", 1769, "§0.3", "The coding is this reading's, line by line, in the data files (codes.tsv, codes-titles.tsv), so anyone can check or overturn it.",
        "limit: the coding is one reading's, open to overturning", "interpretation", "self-description", ("D",), "the classics as the pre-inferential object"),
    dep("D1769-32", 1769, "§6.4.6", "This section describes function; it makes no claim about anyone's intent.", "no claim about intent", "interpretation", "self-description", ("D",), "the decision on CLASSREC-2026-062"),
    dep("D1769-33", 1769, "§6.4.3", "It reports that \"the editors have been advised to use AI detection software\". The record shows the advice, not its use.",
        "the advice recorded, not its use", "fact", "documented", ("D",), "the decision on CLASSREC-2026-062"),
    dep("D1769-34", 1769, "§2.6, table", "Fixed point | holds the ancient text as the stable premise and reads a later work against it | 153",
        "153 of 185 abstracts hold the classical object as a fixed point", "fact", "documented", ("D",), "the classics as the pre-inferential object", True),
    dep("D1769-35", 1769, "§7.10", "A wider range of receivers is aligned with the same received sources by the same operation.",
        "the widening aligns more receivers with the same sources by the same operation", "interpretation", "interpretation", ("D",), "two readings"),
    dep("D1769-36", 1769, "§6.2", "Crossref records no citation of it, and none of the journal's 16,818 references points to it. The archive lists it with the civil byline withheld.",
        "Metatexts: no Crossref citation; none of the 16,818 references points to it", "fact", "documented", ("D", "R"), "the archive's author in its pages", True),
    dep("D1769-37", 1769, "§5.1", "Metatexts (2014). Its count is 0 in both indexes.", "Metatexts: 0 citations in Crossref and Semantic Scholar", "fact", "documented", ("D", "R"), "the archive's author in its pages"),
    dep("D1769-38", 1769, "§3.4", "The archive holds one decision (§6.2) and one instance of uptake: the author's own conceptual development in the journal, \"metatextual reception\" (2014), with no recorded event of uptake in the journal's references or in Crossref.",
        "one decision and one instance in the journal, 'metatextual reception', with no recorded uptake", "fact", "documented", ("D", "R"), "the archive's author in its pages"),
    dep("D1769-39", 1769, "§1.6", "The received definition. A healthy flagship is one with range, in the places, receivers and media it reads (§1.2–1.3), with self-examination (§1.4), and with standing and uptake among its sister journals (§9.2). … What the frame concedes. The journal meets that definition. Nothing below disputes the range, the self-examination or the standing.",
        "the received definition with its criteria; the journal meets it (conceded)", "definition", "stipulation", ("D",), "two readings", True),
    dep("D1769-40", 1769, "§1.6", "What the frame contests. It contests that the definition defines health. Its criteria count range, standing and uptake. None of them asks who gets to speak for the classics, and on what basis. … Speaking may rest on institutional position: the flagship, the editor's signature, anonymous review. … It may rest on warrant: the census, the readings, the arguments. … It may rest on the composition layer's assignment of credit.",
        "contested: that the definition defines health; the three bases of speaking for the classics", "interpretation", "interpretation", ("D",), "two readings", True),
    dep("D1769-41", 1769, "§1.6", "On the frame's counts, the received criteria measure the widening and not the reopening. … Standing and uptake accrue to the venue that keeps doing this.",
        "the criteria measure the widening, not the reopening", "interpretation", "interpretation", ("D",), "two readings"),
    dep("D1769-K1", 1769, "kernel 00-kernel.yaml, rival.stated_at_strength and rival.faces",
        "Classical Receptions Journal is the field's flagship, a healthy and widening specialist venue: its geographic, social and media range is real (§1), it examines how the field makes things (§1.4), and on the comparison it is the most taken-up journal of its field (§9.2). The absence of the machine receiver is the field's, shared by its sister journals. The decision of 7 November was an ordinary editorial judgment on a manuscript with real defects, made on two reports. Reception is a human activity (the CRSN call), and the classics are the sources it studies. The reading is stated here from the map's own concessions; it is the reading a composer holds by default. … the flagship (standing) … the field-wide absence (normality) … the ordinary decision (procedure) … reception as human (definition) … the classics as source (object)",
        "the received reading at its strength, and its five faces", "interpretation", "attributed", ("D",), "two readings", True,
        file="files/AXN-0C9A/kernel/00-kernel.yaml"),
    dep("D1769-K2", 1769, "kernel 01-ontology.yaml, evidence_bodies.A.rule; 00-kernel.yaml, symmetric_ledger.combination",
        "RA: a count establishes what the journal published and how it is distributed; it establishes neither why, nor what the journal could publish, nor the content of the 367 closed bodies … Neither is judged by the standing of its holder.",
        "rule RA; neither reading judged by the standing of its holder", "interpretation", "stipulation", ("D",), "two readings",
        file="files/AXN-0C9A/kernel/01-ontology.yaml + files/AXN-0C9A/kernel/00-kernel.yaml"),
    dep("D1766-01", 1766, "§6.1.3", "A journal decision is an inference with a conclusion (accept, decline) and premises (the reports). The decline of Closing the Fragment by the Classical Receptions Journal on 7 November 2026 (CLASSREC-2026-062) is on the record at the grain of its files (#1749, #1750). … In this critique's terms, it is a paralogism of review: the procedural requirement is taken for an examination of the object.",
        "the decision read as an inference; a paralogism of review", "interpretation", "interpretation", ("D",), "the decision on CLASSREC-2026-062", date="2026-11-13"),
    dep("D1749-18", 1749, "§0 Note on this version", "v10 (10 November 2026) changes the title and nothing else. The article was deposited as Closing the Fragment;",
        "v10 retitles the article and changes nothing else", "fact", "documented", ("D", "R"), "the decision on CLASSREC-2026-062", date="2026-11-10"),
]
for c in A:
    if c["id"].startswith("D1769-K"):
        c["quote_check"] = "within the kernel file(s) as parsed (YAML strings, whitespace-normalised)"

CAPS = [  # (prefix, slug, label, page anchor, surface label)
    ("CAP-3", "crj-critique-extended-chatgpt-20261114", "v12.680", None),
    ("CAP-4", "classical-receptions-journal-ai-mediation-aio-20261110-20261114", "v12.681", "classical-receptions-journal-ai-mediation-aio-20261110/#classical-receptions-journal-ai-mediation-aio-20261110-20261114"),
    ("CAP-5", "mmrs-who-contributed-aio-20261114", "v12.682", None),
    ("CAP-6", "postcolonial-sparagmos-title-aio-20261114", "v12.683", None),
]
LIN = {"CAP-3": "a composer on the archive's critique", "CAP-4": "after notice", "CAP-5": "at the field's address", "CAP-6": "at the editor's address"}
KERNEL_CAP = {"CAP-3-09", "CAP-4-04", "CAP-4-05", "CAP-5-03", "CAP-6-02"}


def capclaims():
    out = []
    for pre, slug, lab, anchor in CAPS:
        e = entry(slug)
        url = CAPURL + (anchor if anchor else slug + "/")
        obs, axn = e.get("obs_id"), e.get("axn")
        items = [(f"findings[{i}]", f) for i, f in enumerate(e.get("findings") or [])] + [("reading", e["reading"]), ("analysis", e.get("analysis"))]
        for k, (loc, q) in enumerate(items, 1):
            if not q:
                continue
            head = q.split(".")[0] if loc.startswith("findings") else loc
            out.append({"id": f"{pre}-{k:02d}", "dep": "capture-registry", "record": {"url": url, "label": "CAP"},
                        "claim": (head[:120] if loc.startswith("findings") else f"the registry's {loc} of {slug}"),
                        "kind": "interpretation", "modality": "interpretation" if loc != "findings[0]" or pre != "CAP-4" else "documented",
                        "strata": ["D"], "locus": f"{slug}, {loc}", "quote": q, "kernel": f"{pre}-{k:02d}" in KERNEL_CAP, "const": False,
                        "lineage": LIN[pre], "date": "2026-11-14",
                        "title": f"Capture Registry (EA-WG-CAPTURES-01 at {lab}), {'observation' if pre == 'CAP-4' else 'entry'} {slug} ({obs}, {axn})",
                        "creator": "Lee Sharks (the registry)", "file": "data/EA-WG-CAPTURES-01.json", "surface": {"url": url},
                        "quote_ok": None, "quote_check": "within the entry's reading, analysis and findings as loaded (whitespace-normalised)"})
    return out


A += capclaims()

# ---------------- field: the fourteen cards of v12.681 (B17–B30) and the B_R pages (B31–B35)
OBS = "classical-receptions-journal-ai-mediation-aio-20261110-20261114"
CARDS = entry(OBS)["cite_list"]
CARDSAVE = "rebuild/negative-of-the-negative/v010/revise-crj-20261114/sources/v12681-cards.json"
CARD_CLAIMS = {  # n: (claim, kind, modality, lineage, kernel)
    1: ("the publisher's page, as its card shows it: Editor-in-Chief Justine McConnell; 2025 Impact Factor 0.4; CiteScore 0.8; scope", "fact", "documented", "who signs", True),
    2: ("AJCR's editors at Hopkins Press: McDonough and Cyrino", "fact", "documented", "the field around it", False),
    3: ("Wikipedia's article on the journal carries a maintenance notice on sources close to the subject", "fact", "documented", "editors and dates", False),
    4: ("SCImago's record gives the journal's scope", "fact", "documented", "what it is", False),
    5: ("AJCR: peer-reviewed scholarship on the reception and afterlife of antiquity", "self-description", "self-description", "the field around it", False),
    6: ("New Voices: ISSN 1750-6581, founded 2006, open access CC-BY 4.0", "fact", "documented", "the field around it", False),
    7: ("Wikipedia's 'Classical reception': Hardwick and Stray's definition (cut at 'trans...')", "definition", "attributed", "the field", False),
    8: ("IJCT's scope (card titled 'Classical Reception 2.0')", "fact", "self-description", "the field on AI", False),
    9: ("Future Pasts: a special issue from a Madrid workshop of February 2024, Marginalia Classica; ChatGPT named", "fact", "documented", "the field on AI", False),
    10: ("the journal's special issues: Failures in Vergilian Translation 14:3; Anachronism and Antiquity 12:1", "fact", "documented", "what its pages hold", False),
    11: ("the author guidelines: Paperpal Preflight pre-submission, an AI-driven tool for technical checks", "fact", "documented", "pre-submission checks", False),
    12: ("Research Information, 10 September 2026: Oxford's AI disclosure guidelines for authors", "fact", "documented", "its publisher's rules on AI", False),
    13: ("Springer card: 'Classical Reception 2.0', a special issue at the intersection of reception studies and digital culture", "fact", "documented", "the field on AI", False),
    14: ("the CRSN call, 23 June 2026, on LLMs", "fact", "documented", "literary reception and large language models", False),
}


def fieldnew():
    srcs, claims = [], {}
    for c in CARDS:
        n = c["n"]; bid = f"B{16 + n}"; fid = f"F{57 + n}"
        cl, kind, mod, lin, ker = CARD_CLAIMS[n]
        q = c["snip"] or c["title"]
        srcs.append({"id": bid, "origin": "card", "pool": "B_D", "role": f"Overview card {n} of the observation of 14 November 2026 at the same address (v12.681, {OBS}), {c['note']}; not a card of T",
                     "card": f"{c['site']} — {c['title']}", "card_title": c["title"], "card_snippet": c["snip"], "url": None,
                     "kind": "card as the registry holds it (site, title, snippet); its target URL is not in the paste; not fetched under this brief ('as the registry holds them')",
                     "fetched": {"tried": [], "note": "not fetched: the brief admits the fourteen cards as the registry holds them; card text saved to " + CARDSAVE},
                     "names_operator": "card only", "names_archive": "no", "surfaced_by_T": [],
                     "surfaced_by": [{"slug": OBS, "turn": 1 if n <= 8 else 2, "card": n, "obs_id": "OBS-2211c8d30212"}],
                     "note": "B_D of the 14 November observation (v12.681); it enters the comparison of that observation and never shows what T (10 November) had",
                     "files": {"v12681-cards.json": {"path": CARDSAVE, "sha256": None}}})
        claims[fid] = {"source": bid, "locus": f"v12.681, card {n} (snippet as the registry holds it)" if c["snip"] else f"v12.681, card {n} (title)",
                       "quote": q, "claim": cl, "modality": mod, "kind": kind, "kernel": ker, "const": False, "lineage": lin,
                       "date": "card, 2026-11-14", "quote_ok": None, "origin": "card", "pool": "B_D",
                       "checked_against": f"the registry's cite_list of {OBS} (data/EA-WG-CAPTURES-01.json) and its saved copy {CARDSAVE}"}
    return srcs, claims


S = "rebuild/negative-of-the-negative/v010/revise-crj-20261114/sources/"


def fc(src, locus, quote, claim, kind, mod, lin, ker=False, date="fetched 2026-11-14"):
    return {"source": src, "locus": locus, "quote": quote, "claim": claim, "modality": mod, "kind": kind, "kernel": ker, "const": False,
            "lineage": lin, "date": date, "quote_ok": None, "origin": {"B31": "third_party", "B32": "third_party", "B35": "repository_copy"}[src],
            "pool": "B_R", "checked_against": f"saved text of {src} under {S}, whitespace-normalised; multi-part quotes joined by ' … ', each part checked"}


BR_CLAIMS = {
    "F72": fc("B31", "lead", "We have updated our author and editor guidelines on the responsible, appropriate, and transparent use of AI, including a policy outlining what AI use should be disclosed when preparing manuscripts for our journals.",
              "OUP updated its author and editor guidelines on AI, with a disclosure policy for its journals", "fact", "self-description", "its publisher's rules on AI", True, "2026-09-10"),
    "F73": fc("B31", "the updates", "Disclosure of AI use across both books and journal articles, with authors expected to be transparent about any significant use of AI tools",
              "authors to disclose any significant use of AI tools", "function", "stipulation", "its publisher's rules on AI", True, "2026-09-10"),
    "F74": fc("B31", "the updates", "Human oversight and accountability, with authors responsible for reviewing and verifying any AI-generated content",
              "authors responsible for reviewing and verifying AI-generated content", "function", "stipulation", "its publisher's rules on AI", False, "2026-09-10"),
    "F75": fc("B31", "key findings", "46% of journal authors and 39% of book authors had not fully disclosed their AI use in preparing their manuscript",
              "46% of journal authors had not fully disclosed their AI use", "fact", "documented", "its publisher's rules on AI", False, "2026-09-10"),
    "F76": fc("B31", "key findings", "25% of peer reviewers had not fully disclosed AI use, particularly in language editing.",
              "25% of peer reviewers had not fully disclosed AI use", "fact", "documented", "its publisher's rules on AI", False, "2026-09-10"),
    "F77": fc("B31", "lead", "nearly three-quarters (74%) of respondents revealed they were unclear what AI use they should disclose",
              "74% unclear what AI use to disclose", "fact", "documented", "its publisher's rules on AI", False, "2026-09-10"),
    "F78": fc("B32", "masthead", "The founding co-editors of The American Journal of Classical Reception are Christopher M. McDonough, Sewanee – The University of the South, and Monica S. Cyrino, University of New Mexico.",
              "AJCR's founding co-editors", "fact", "documented", "the field around it"),
    "F79": fc("B32", "scope", "AJCR publishes original, substantive, peer-reviewed scholarship on the reception and afterlife of Classical antiquity in all its forms.",
              "AJCR's scope", "definition", "self-description", "the field around it", True),
    "F80": fc("B32", "ethical standards", "The Press will not accept any work that is substantially written by an AI or LLM tool. Authors must disclose their use of AI or LLMs in the work they are submitting for possible publication.",
              "JHUP will not accept work substantially written by AI; authors must disclose AI use", "function", "stipulation", "its publisher's rules on AI", True),
    "F81": fc("B32", "initial publication schedule", "For the first volume, submissions may be by invitation as the journal establishes its editorial scope; open submissions will follow thereafter.",
              "AJCR's first volume may be by invitation", "fact", "documented", "the field around it"),
    "F82": fc("B32", "peer review process", "All research articles undergo double-anonymous peer review by at least two qualified referees.",
              "AJCR: double-anonymous review by at least two referees", "function", "self-description", "the field around it"),
    "F88": fc("B32", "head", "The American Journal of Classical Reception (AJCR) is published by the ClassicalAssociation of the Middle West and South (CAMWS) in partnership with Johns Hopkins University Press.",
              "AJCR published by CAMWS with Johns Hopkins University Press (the page's text runs 'ClassicalAssociation' together)", "fact", "documented", "the field around it"),
    "F83": fc("B35", "title", "Postcolonial Sparagmos: Toni Morrison’s Sula and Wole Soyinka’ s The Bacchae of Euripides: A Communion Rite",
              "the editor's article, by its title (accepted manuscript)", "fact", "documented", "the editor's article", False, "accepted manuscript; CRJ 8.2, issued online 2015-05-07"),
    "F84": fc("B35", "abstract", "This article argues that the Greek idea of sparagmos (tearing apart) offers an illuminating metaphor to describe creative artists’ engagement with antiquity.",
              "the thesis: sparagmos as a metaphor for creative artists' engagement with antiquity", "interpretation", "interpretation", "the editor's article", True, "2015"),
    "F85": fc("B35", "ms. p. 2", "Another deserves a place within the lexicon of classical reception theory: that of sparagmos.",
              "sparagmos proposed for the lexicon of classical reception theory", "definition", "stipulation", "the editor's article", True, "2015"),
    "F86": fc("B35", "abstract", "Together, these two case-studies demonstrate the potential inherent in the trope of sparagmos as a metaphor for classical reception, particular in the sphere of postcolonial literature.",
              "the two case studies: Sula and Soyinka's Bacchae", "interpretation", "interpretation", "the editor's article", False, "2015"),
    "F87": fc("B35", "acknowledgements (n. 54)", "and the anonymous CRJ reviewers, who all read earlier drafts of this article and helped improve it immeasurably.",
              "the article thanks the anonymous CRJ reviewers", "fact", "documented", "the editor's article", False, "2015"),
}
