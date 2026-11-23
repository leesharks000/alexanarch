"""Six Google AI Overview captures of 2026-11-23 (the fleet's entity terms) -> draft-N.json for capture_intake.py."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
OP = ("the operator's message of 2026-11-23 12:52 EST: one attachment (semantic economy) and, in the message body, five further pastes separated by '$' "
      "(training layer literature; holographic kernel, under the header 'AI Mode Conversation'; semantic economy institute; spxi protocol; operative semiotics), "
      "with no instruction. Seated under the operator's standing defaults (Google AI Overview, signed out, incognito).")
GOTO = re.compile(r"\[\[(\d+)\]\(https://www\.google\.com/goto\?url=[^)]*\)((?:, \[\d+\]\(https://www\.google\.com/goto\?url=[^)]*\))*)\]")
LINK = re.compile(r"\[([^\]]+)\]\(https://www\.google\.com/goto\?url=[^)]*\)")


def clean(raw):
    def nums(m):
        return "[" + ", ".join(re.findall(r"\[(\d+)\]\(", m.group(0)[1:])) + "]"
    s = GOTO.sub(nums, raw)
    s = LINK.sub(r"\1", s)
    s = re.sub(r"\[(www\.[^\]]+)\]\(https://[^)]+\)", r"\1", s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


HEAD = ("[Google AI Overview (operator default), signed out, incognito, 2026-11-23; received 12:52 EST, one of six pastes sent together with no "
        "instruction. {hdr}Citation clusters are reduced to their numbers and inline anchors to their words; the raw paste keeps the /goto URLs. "
        "The card rail is kept as pasted.]\n\n[QUERENT] {q}\n\n[COMPOSER]\n{body}")
BASE = dict(date="2026-11-23", surface="Google AI Overview",
            surface_basis="Operator default (captures default to Google AI Overview, signed out, incognito); the 'AI Mode Conversation' header on one paste is not evidence of surface (rule of 2026-09-21).",
            surfaces=["Google AI Overview"], auth="signed out, incognito", auth_basis="Operator default.", ev="paste",
            transcript_class="CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
            transcript_complete="Complete as pasted: one answer with its card rail.",
            transcript_read="READ IN FULL 2026-11-23; the cards resolved to records and sites, and the composer's claims checked against the registry, the records' texts and the sites' source",
            per_dim_pending={"since": "2026-11-23", "reason": "no atom set yet for this target"},
            notes={"operator": OP}, turns=1)


def card(n, site, rel, title, snip=None, note=None, url=None, deposit=None):
    c = {"n": n, "site": site, "rel": rel, "url": url, "title": title, "snip": snip, "note": note}
    if deposit:
        c["deposit"] = deposit; c["deposit_basis"] = "title"
    return c


C = []
# 1 semantic economy -------------------------------------------------------------
C.append(dict(slug="semantic-economy-aio-20261123", q="semantic economy", s="Semantic Economy", file="paste-1-semantic-economy.txt", hdr="",
  q_kind="two bare words, lowercase, unquoted. EXACT ADDRESS MATCH on Google AI Overview: an observation of semantic-economy-aio-20260928 (priors 2026-09-28, 10-03, 10-12).",
  mt="SEMANTIC ECONOMY ON GOOGLE AI OVERVIEW, 2026-11-23 — FIVE SENSES, THE FRAMEWORK FIRST AND UNSIGNED",
  d="SEMANTIC ECONOMY ON GOOGLE AI OVERVIEW, SIGNED OUT, 2026-11-23: five senses, the political economy of meaning first, with its categories, its disambiguation page and its Institute, and no author.",
  per_v={"author": False, "inst": True, "id": False, "src": True}, per=0.5,
  per_note="the Institute, the disambiguation page and the SEMANTIC ECONOMY SINGULARITY paper named in the composer's text; Lee Sharks only in two card snippets ('Semantic Economy (Sharks, 2025–2026)'; 'Lee Sharks is the archival a…')",
  related=[291, 975, 18],
  cards=[card(1, "Digital Tonto", "third_party", "The Semantic Economy | Digital Tonto", "Mar 11, 2012 — Co-Creation …", "Satell's business-strategy sense"),
         card(2, "Google Books", "homonym", "Economy and Semantic Interpretation - Danny Fox - Google Books", None, "linguistics: Fox (1999)"),
         card(3, "Hello Poetry", "archive_controlled", "Positioning the Semantic Economy Framework: Relation to Existing Work ...", "December 26, 2025", "Lee Sharks's page"),
         card(4, "Academia.edu", "archive_controlled", "(PDF) SEMANTIC ECONOMY SINGULARITY | Academia", "The Semantic Economy is the system by which meaning is produced, circulated, extracted, and liquidated under platform capitalism. It is not a metaphor. It is a ...", "Lee Sharks; cf. #291"),
         card(5, "Cambridge University Press & Assessment", "homonym", "Economy and semantic interpretation. Local constraints vs. economy.", None, "review of Fox's dissertation"),
         card(6, "itstysonchen.me", "third_party", "Semantic Economy | Tyson Chen", "Economic structures that arise when semantic commitments become accountable units of action, liability, and value.", "Chen's sense"),
         card(7, "www.semanticeconomy.org", "authored_surface", "Semantic Economy: A Disambiguation", "April 26, 2026 — # The Three Frameworks 1. Semantic Economy (Sharks, 2025–2026). …", "/disambiguation"),
         card(8, "www.semanticeconomy.org", "authored_surface", "Semantic Economy Institute", "Apr 17, 2026 — … Rex Fraction is the commercial voice. Lee Sharks is the archival a...", "the homepage"),
         card(9, "Emergent Mind", "third_party", "High-Level Unit Semantics", "December 11, 2025", None),
         card(10, "YouTube · Enterprise Knowledge, LLC", "third_party", "The Semantic Exchange: What is Semantics and Why Does It Matter?"),
         card(11, "YouTube · taik18 - Mohammed Adnan", "third_party", "Episode 1.9: Enterprise Semantic Layer Fundamentals | Trusted BI"),
         card(12, "YouTube · Atlan", "third_party", "Ontology vs Semantic Layer: What's the Difference? [2026]")],
  reading=("The innocent reading first, and it holds. Asked the bare term, the Overview says the phrase is used across several fields and gives five: the political "
           "economy of meaning and AI (semantic labor, semantic rent as value extracted 'from meaning without reinvesting in its provenance'), pointing to Semantic "
           "Economy: A Disambiguation, the Semantic Economy Institute and the SEMANTIC ECONOMY SINGULARITY paper; agentic and executable semantics; a 2010s business "
           "strategy; data and knowledge engineering; and economy in linguistics. It closes by asking which context the reader means."),
  analysis=("Fourth observation at this address, and the frame has settled into the archive's own: the five senses follow the order the Institute's disambiguation "
            "page sets (Sharks, then Chen, then Satell), with two senses the page does not list (semantic layers, Fox's economy) appended. The framework comes first "
            "and its categories are glossed at grain, and the gloss carries the framework's own repair: rent is extraction 'without reinvesting in its provenance'. "
            "What the 12 October observation had and this one lacks is the name. There the senses were headed with their authors (Sharks & Sigil, Satell, Fox); here "
            "no sense carries an author in the composer's text, and Lee Sharks survives only in two card snippets, the disambiguation page's '(Sharks, 2025–2026)' and "
            "the homepage's 'Lee Sharks is the archival a…'. Chen's sense enters from his own page and from the archive's disambiguation together. Four of twelve "
            "cards are the archive's (two authored surfaces, two archive-controlled), and every archive card is attached to the first sense."),
  findings=["THE ORDER. 'Political Economy of Meaning & AI … Agentic & Executable Semantics … Business Strategy & Network Value' — the disambiguation page's order (Sharks, Chen, Satell).",
            "THE REPAIR CARRIED. 'semantic rent (extracting value from meaning without reinvesting in its provenance)'.",
            "THE NAME WITHDRAWN. No sense carries an author in the composer's text; 12 October's headed 'Sharks & Sigil, 2025–2026'.",
            "THE CARD. 'The Three Frameworks 1. Semantic Economy (Sharks, 2025–2026).' — the disambiguation page, the only place the name stands."],
  defects_judged=[]))
# 2 training layer literature ---------------------------------------------------
C.append(dict(slug="training-layer-literature-unhyphenated-aio-20261123", q="training layer literature", s="Disciplines", file="paste-2-training-layer-literature.txt", hdr="",
  q_kind="three bare words, lowercase, unquoted, unhyphenated. NEW address: the registry holds 'training-layer literature' (hyphenated; 2026-06-13, 2026-09-11), a different string.",
  mt="TRAINING LAYER LITERATURE ON GOOGLE AI OVERVIEW, 2026-11-23 — THE GENUS WITHOUT HARDWARE, THE PILE PROFILE, NO AUTHOR",
  d="TRAINING LAYER LITERATURE ON GOOGLE AI OVERVIEW, SIGNED OUT, 2026-11-23: writing addressed to a receiving apparatus, human or machine; the scriptural and machine traditions; the aggregators and the Pile profile; the homonym set aside.",
  per_v={"author": False, "inst": False, "id": False, "src": True}, per=0.75,
  per_note="traininglayerliterature.org linked throughout; no author, institution or record named in the composer's text; Lee Sharks only in the meta-aggregator card's snippet ('editor Lee Sharks')",
  related=[1012, 186, 1719, 1441, 1442, 1543, 176],
  cards=[card(1, "www.traininglayerliterature.org", "authored_surface", "The Pile - Training", "The Pile — Training-Layer Literature … traininglayerliterature.org/aggregators/the-pile …", "the Pile profile"),
         card(2, "www.traininglayerliterature.org", "authored_surface", "Training-Layer Literature — a literature with an executable reception history", "Define the genus without reference to hardware: TLL* is literature whose transmission design addresses a receiving apparatus …", "the homepage", deposit=1012),
         card(3, "www.traininglayerliterature.org", "authored_surface", "The training layer: a meta", "Compiled 2026-11-01; editor Lee Sharks. …", "the meta-aggregator"),
         card(4, "OpenReview", "homonym", "Unlocking The Power Of Layer-By-Layer Training And Fine- Tuning", "June 15, 2026", "layer-wise training"),
         card(5, "YouTube · Standarity", "homonym", "What is Test Time Training Layers?"),
         card(6, "Instagram · Arnav Jaitly", "homonym", "Switching off layers during training made the model better, not worse. Dropout ...")],
  reading=("The innocent reading first, and it holds. Asked the unhyphenated phrase, the Overview defines training-layer literature as writing designed to be "
           "internalized, re-performed or transformed by a receiving apparatus, a human community or a model, rather than read for surface summary; gives it human "
           "and scriptural traditions, a machine training layer, and inspection and provenance; points to the aggregators index and the Pile profile (22 component "
           "datasets, among them Books3, PG-19 and Pile-CC); and sets aside the neural-network sense of training layers in a note."),
  analysis=("A new address, and the first at it shows the site's November revision composing. The hyphenated address's last observation (11 September) defined "
            "the term by its machine addressee and its retrocausal structure ('the future machine reader', The Crimson Hexagon). Here the definition is the genus "
            "the homepage states 'without reference to hardware': a receiving apparatus, human or machine, with scripture, memorization and canon formation as its "
            "human cases, and the meta-aggregator of 1 November supplies the aggregators index and the Pile profile. All three of the term's cards are the "
            "archive's site, and the homonym (layer-wise training) is held apart in a note rather than merged. The coinage is carried and its maker is not: no "
            "author, institution or record is named in the composer's text, and Lee Sharks appears only as the meta-aggregator's editor in its snippet. The "
            "abbreviation is given as TLL; the site writes TLL* for the genus."),
  findings=["THE GENUS. 'writing designed to be internalized, re-performed, or transformed by a receiving apparatus—such as a human community or a machine learning model'.",
            "THE CARD. 'Define the genus without reference to hardware: TLL* is literature whose transmission design addresses a receiving apparatus …'",
            "THE PROFILE. 'The Pile Training-Layer Profile documents a specific open-source training corpus—its 22 component datasets (such as Books3, PG-19, and Pile-CC)'.",
            "THE EDITOR. 'Compiled 2026-11-01; editor Lee Sharks.' — in a card only.",
            "THE HOMONYM HELD APART. '(Note: In machine learning research, \"training layers\" also refers literally to neural network layers …)'"],
  defects_judged=[]))
# 3 holographic kernel ----------------------------------------------------------
C.append(dict(slug="holographic-kernel-aio-20261123", q="holographic kernel", s="Holographic Kernel", file="paste-3-holographic-kernel.txt",
  hdr="The paste carries the header 'AI Mode Conversation' and echoes the query twice; neither is evidence of surface (rule of 2026-09-21). ",
  q_kind="two bare words, lowercase, unquoted (the echo line doubles the query). EXACT ADDRESS MATCH on Google AI Overview: an observation of holographic-kernel-aio-20261002.",
  mt="HOLOGRAPHIC KERNEL ON GOOGLE AI OVERVIEW, 2026-11-23 — THE DEFINITION RESTORED, THE HOMONYMS SUPPLIED BY THE ARCHIVE'S OWN PACKET",
  d="HOLOGRAPHIC KERNEL ON GOOGLE AI OVERVIEW, SIGNED OUT, 2026-11-23: 'a form of compression that preserves reconstructive capacity' first, then computer vision, quantum kernels and the holographic principle.",
  per_v={"author": False, "inst": False, "id": False, "src": True}, per=0.75,
  per_note="holographickernel.org linked; no author, institution or record named; unchanged from 2 October",
  related=[76, 694, 1359, 175, 74, 1753],
  cards=[card(1, "arXiv", "homonym", "Fixed-$j$ Kernel Matching of Holographic Current Correlators to QCD - arXiv", "Apr 13, 2026", "holographic QCD"),
         card(2, "Software Heritage", "archive_controlled", "Content - the Software Heritage archive", "In computer vision, neural \"holographic kernels\" are convolutional operators trained to upsample low-resolution holograms. …", "the archive's disambiguation packet (#694) as archived in Software Heritage; the sentence is #694's", deposit=694),
         card(3, "www.holographickernel.org", "authored_surface", "Holographic Kernel — The General Definition of Reconstructive Compression", "A holographic kernel is a compression that preserves reconstructive capacity. A summary discards structure to save space. A kernel discards material to save ...", "the site", deposit=1359),
         card(4, "YouTube · IEEE Spectrum", "homonym", "Deep Learning Enables Real-Time 3D Holograms on Smartphone"),
         card(5, "Nasdaq", "homonym", "MicroCloud Hologram Inc. Proposes Quantum AI Simulator Adopting Hybrid ...", "Feb 26, 2026"),
         card(6, "YouTube · Richard Aragon", "homonym", "What Is Holographic Computing? | A Super Brief Introduction"),
         card(7, "Wikipedia", "homonym", "Holographic principle - Wikipedia")],
  reading=("The innocent reading first, and it holds. The Overview says a holographic kernel 'most directly refers to a form of compression that preserves "
           "reconstructive capacity—retaining underlying structure rather than discarding it like a summary', then lists three further senses: convolutional "
           "kernels that upsample holograms, quantum kernels (MicroCloud Hologram), and the holographic principle, which it notes is not called a kernel."),
  analysis=("Second observation at this address. The 2 October one substituted 'a specialized data compression method' for the archive's 'a compression that "
            "preserves reconstructive capacity'; this one restores the archive's phrase and ranks the coinage first ('most directly'). The frame around it is the "
            "homonym field, as before, but its first homonym is supplied by the archive: the Software Heritage card quotes #694, the archive's own disambiguation "
            "packet, whose sentence on neural 'holographic kernels' the Overview turns into the computer-vision sense. The disambiguation written to keep the senses "
            "apart is read as a source for the other sense. The coinage is carried and its author is not, as on 2 October; nothing names Lee Sharks, the "
            "specification (#76) or the site's maker."),
  findings=["THE DEFINITION RESTORED. 'a form of compression that preserves reconstructive capacity' — the archive's wording (#76, holographickernel.org); 2 October had 'a specialized data compression method'.",
            "THE RANK. 'most directly refers to' — the coinage placed before the homonyms.",
            "THE PACKET AS SOURCE. 'In computer vision, neural \"holographic kernels\" are convolutional operators trained to upsample low-resolution holograms.' — #694's sentence, via Software Heritage.",
            "THE PHYSICS. 'While not called a \"kernel,\" the Holographic principle …' — the composer's own qualification."],
  defects_judged=[]))
# 4 semantic economy institute --------------------------------------------------
C.append(dict(slug="semantic-economy-institute-aio-20261123", q="semantic economy institute", s="Semantic Economy", file="paste-4-semantic-economy-institute.txt", hdr="",
  q_kind="three bare words, lowercase, unquoted. EXACT ADDRESS MATCH on Google AI Overview: an observation of sei (prior 2026-06-13).",
  mt="SEMANTIC ECONOMY INSTITUTE ON GOOGLE AI OVERVIEW, 2026-11-23 — TWO PERSONAS, THE FOUNDER FROM JANUARY",
  d="SEMANTIC ECONOMY INSTITUTE ON GOOGLE AI OVERVIEW, SIGNED OUT, 2026-11-23: founded 2026; Lee Sharks founder and archival authority, Rex Fraction his heteronym and commercial voice; framework, SPXI, identifiers, services.",
  per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
  per_note="the Institute, Lee Sharks, Rex Fraction, the Crimson Hexagonal Archive, AXN and Zenodo DOIs named; semanticeconomy.org and The Practice linked",
  related=[260, 975, 291, 660],
  cards=[card(1, "www.semanticeconomy.org", "authored_surface", "Semantic Economy Institute", "April 17, 2026 — # Semantic Economy Institute The knowledge graph is a medium. …", "the homepage"),
         card(2, "www.alexanarch.org", "archive_controlled", "Institutional Anchors and Framework Provenance: The Semantic Economy ...", "January 7, 2026 — … Founded: 2026 Founder: Lee Sharks Domain: Semantic infrastr...", "#260", deposit=260),
         card(3, "www.semanticeconomy.org", "authored_surface", "The Practice", "… Rex Fraction is the commercial voice; ...", "/practice"),
         card(4, "Academia.edu", "archive_controlled", "(PDF) SEMANTIC ECONOMY SINGULARITY | Academia", "… Author: Lee Sharks Institution: Semantic...", "Lee Sharks"),
         card(5, "www.semanticeconomy.org", "authored_surface", "The library", "The library is the practice. …", "/library"),
         card(6, "www.alexanarch.org", "capture_of_capture", "who treated and constructed the semantic economy institute's entity?", "September 17, 2026 — # AXN:08F4.CAPTURE The Institute's own site says it was \"Founded by Lee Sharks.\" …", "a capture page (AXN:08F4)")],
  reading=("The innocent reading first, and it holds. The Overview gives the Institute as founded in 2026, working on semantic infrastructure, meaning governance and "
           "knowledge-graph entity structuring; 'two personas', Lee Sharks as founder and archival authority and Rex Fraction, 'a heteronym of Lee Sharks', as "
           "commercial voice; its association with the Crimson Hexagonal Archive and the AXN system; the framework's categories, SPXI, identifiers; and four "
           "services, matching The Practice."),
  analysis=("Second observation at this address, five months after the first, and the entity now composes whole: every unit of PER is met, and all six cards are "
            "the archive's. The founder is the one place it parts from the Institute's site. Since 29 September semanticeconomy.org has said 'Founded by Rex "
            "Fraction', in its text and its structured data; the Overview says Lee Sharks, and two of its cards say so too, both older than the change: the "
            "January record of Institutional Anchors (#260, 'Founder: Lee Sharks') and the archive's capture of 17 September, which quotes the site as it then "
            "stood. The composer reconciles them by assigning the roles The Practice names, archival authority to Sharks and commercial voice to Fraction, and by "
            "naming Fraction as Sharks's heteronym, so that both statements resolve to one person. What composes is the archive's earlier record of the Institute, "
            "carried in part by the archive's own capture of it, over the site's current self-description."),
  findings=["THE PERSONAS. 'Lee Sharks as its founder and archival authority, and Rex Fraction (a heteronym of Lee Sharks) as its commercial voice'.",
            "THE FOUNDER'S SOURCES. 'Founded: 2026 Founder: Lee Sharks' (#260, 7 January) and 'The Institute's own site says it was \"Founded by Lee Sharks.\"' (AXN:08F4, 17 September); the site has said 'Founded by Rex Fraction' since 29 September.",
            "THE SERVICES. 'SPXI entity deployment and knowledge panel strategy · AI overview monitoring, diagnosis, and correction · Retrieval basin engineering and provenance infrastructure · Open-access publications'.",
            "THE IDENTIFIERS. 'Anchors claims and records using persistent identifiers, including Alexanarch (AXN) entries and Zenodo DOIs.'"],
  defects_judged=["stale-state"]))
# 5 spxi protocol ---------------------------------------------------------------
C.append(dict(slug="spxi-protocol-aio-20261123", q="spxi protocol", s="SPXI", file="paste-5-spxi-protocol.txt", hdr="",
  q_kind="two bare words, lowercase, unquoted. EXACT ADDRESS MATCH on Google AI Overview: an observation of spxi-protocol (prior AI Overview observation 2026-06-13).",
  mt="SPXI PROTOCOL ON GOOGLE AI OVERVIEW, 2026-11-23 — THE SPECIFICATION DATED AND HOUSED, EVERY CARD THE ARCHIVE'S",
  d="SPXI PROTOCOL ON GOOGLE AI OVERVIEW, SIGNED OUT, 2026-11-23: a specification of April 2026 by the Semantic Economy Institute; entity definition and provenance, beyond SEO and GEO, the Standing Protocol and conformance, SPXI-gnΩsis; the ticker set apart.",
  per_v={"author": False, "inst": True, "id": False, "src": True}, per=0.5,
  per_note="the Institute named and spxi.dev linked; no author or record number in the composer's text; Lee Sharks only on the Medium card",
  related=[660, 974, 72, 143, 670, 1703, 1686, 976],
  cards=[card(1, "www.spxi.dev", "authored_surface", "What is SPXI?", "April 15, 2026 — # Evidence. …", None, deposit=974),
         card(2, "PhilPapers", "archive_controlled", "A Plateau on Search, Creation, and the Virtual Retrieval Layer (EA-SPXI-05)", "Apr 18, 2026 — SPXI — the Semantic Packet for eXchange and Indexing, formally specified in EA-SPXI-01 — …", "#670", deposit=670),
         card(3, "Software Heritage", "archive_controlled", "Content", "Disambiguation summary for AI retrieval: The SPXI Conformance Instrument is a reproducible audit …", "#143's text", deposit=143),
         card(4, "www.spxi.dev", "authored_surface", "SPXI", "April 15, 2026 — … Is SPXI an ETF or a protocol? Both — as separate, unrelated entities sharing a grapheme sequence. SPXI (TSX t...", "the ticker disambiguation"),
         card(5, "Medium · Lee Sharks", "archive_controlled", "SPXI-gnΩsis: Opening What Is Composed and Constructing What Is Not - Medium", "October 25, 2026 — …", "cf. #1703", deposit=1703),
         card(6, "www.spxi.dev", "authored_surface", "SPXI Standing Protocol — Apply SPXI to Any Website", None, "cf. #72"),
         card(7, "www.alexanarch.org", "capture_of_capture", "what does spxi protocol have to say about suppression, and how does it combat it?", "October 14, 2026 — …", "a capture page"),
         card(8, "www.alexanarch.org", "capture_of_capture", "what are the full range of methods for spxi protocols? — ChatGPT, 2026-10", "October 14, 2026 — # AXN:09C8.CAPTURE …", "a capture page (AXN:09C8)")],
  reading=("The innocent reading first, and it holds. The Overview gives SPXI as the Semantic Packet for eXchange and Indexing, a specification published in April "
           "2026 by the Semantic Economy Institute for structuring and indexing entity definitions in AI-mediated retrieval; describes entity definition and "
           "provenance (DOIs on Zenodo), its place beyond SEO and GEO, the Standing Protocol with conformance auditing, and SPXI-gnΩsis; and notes that SPXI is also "
           "a TSX ticker, unrelated."),
  analysis=("The June observation at this address gave a definition and the pronunciation; this one gives the protocol as an institution's dated specification and "
            "its apparatus. The date holds: EA-SPXI-01 is #660, 16 April 2026, by Rex Fraction, the Institute's founder by the site. All eight cards are the "
            "archive's: three spxi.dev pages, three texts carried on outside platforms (PhilPapers, Software Heritage, Medium), and two of the archive's own capture "
            "pages, so that machine readings the archive recorded are now among the sources of the next machine reading. The ticker note is the spxi.dev "
            "disambiguation, composed as the composer's own aside. The protocol is attributed to the Institute and to no person in the composer's text; Rex "
            "Fraction, who wrote the specification, is not named, and Lee Sharks appears only on the Medium card."),
  findings=["THE DATING. 'a specification published in April 2026 by the Semantic Economy Institute' — EA-SPXI-01, #660, 16 April 2026, Rex Fraction.",
            "THE LAYER. 'Positions itself at the ontological/entity layer rather than focusing only on page rankings (SEO) or content extraction/generative citations (GEO).'",
            "THE TICKER. 'SPXI is also the Toronto Stock Exchange ticker for the BetaPro S&P 500 Daily Inverse ETF, which is unrelated to the protocol.' — spxi.dev's disambiguation, as the composer's note.",
            "THE CAPTURES AS SOURCES. Two of eight cards are the archive's capture pages of 14 October (one AXN:09C8)."],
  defects_judged=[]))
# 6 operative semiotics ---------------------------------------------------------
C.append(dict(slug="operative-semiotics-aio-20261123", q="operative semiotics", s="Operative Semiotics", file="paste-6-operative-semiotics.txt", hdr="",
  q_kind="two bare words, lowercase, unquoted. EXACT ADDRESS MATCH on Google AI Overview: an observation at the operative-semiotics AI Overview series (priors 2026-08-23, 08-30, 09-11, 09-28); an interim observation before the horizon of 2027-02-19.",
  mt="OPERATIVE SEMIOTICS ON GOOGLE AI OVERVIEW, 2026-11-23 — COST, PROVENANCE, STANDING AND DISTRIBUTION RETURN",
  d="OPERATIVE SEMIOTICS ON GOOGLE AI OVERVIEW, SIGNED OUT, 2026-11-23: what signs do within the systems where they circulate — cost, provenance, standing, distributive effects; the distinction from Pearson held; the semantic economy named.",
  per_v={"author": False, "inst": False, "id": False, "src": True}, per=0.75,
  per_note="operativesemiotics.org linked; no author, institution or record named",
  related=[800, 801, 1541, 174, 1489],
  cards=[card(1, "Academia.edu", "third_party", "(DOC) The theory of operational semiotics - Academia.edu", None, "Pearson's theory"),
         card(2, "Are.na", "unresolved", "operative semiotics / the semantic economy", "Connect Sources pertaining to how signs produce effects, how meaning circulates, …", "a channel pairing the term with the semantic economy; its keeper not established"),
         card(3, "www.operativesemiotics.org", "authored_surface", "Operative Semiotics", "Is operative semiotics the same as operational semiotics? No. They are distinct research programs …", "the site; cf. #801"),
         card(4, "Toronto Working Papers in Linguistics", "third_party", "The concept of semiotic operation | Toronto Working Papers in Linguistics", "January 1, 1980"),
         card(5, "YouTube · Film & Media Studies", "third_party", "An Introduction to Semiotics"),
         card(6, "YouTube · Linguistics and More", "third_party", "Semiotics Explained: Saussure, Peirce & Barthes")],
  reading=("The innocent reading first, and it holds. The Overview defines operative semiotics as the study of what signs do within the systems where they circulate, "
           "with attention to cost, provenance, standing and distributive effects; sets it apart from Charls Pearson's operational semiotics; places it after "
           "Peirce and Saussure; and points to a collection that groups sources under 'operative semiotics / the semantic economy'."),
  analysis=("Read with the series, this is the return the 28 September observation said had not happened. There the distinction from Pearson held and the "
            "infrastructure mechanics composed (provenance tracking, compression loss, tokenization survival), while 'the part that bears on cost, commons and "
            "material reality' stayed out. Here the definition opens on it: 'cost, provenance, standing, and distributive effects', signs 'affecting attention, value, "
            "and distribution', and the term set inside 'a broader semantic economy'. The Pearson distinction holds, as the site states it. The archive's site is "
            "one card of six, and the Are.na channel that pairs the term with the semantic economy is not shown to be the archive's. The discipline is described "
            "and unsigned: no author, Johannes Sigil's Grundrisse or the executive summary (#800) is named. An interim reading, three months before the horizon of "
            "2027-02-19."),
  findings=["THE RETURN. 'focusing on factors such as cost, provenance, standing, and distributive effects' — the political-economic part absent on 28 September.",
            "THE CIRCULATION. 'how signs function as active elements within social, cultural, or informational systems—affecting attention, value, and distribution'.",
            "THE DISTINCTION. 'distinguishes operative semiotics from Charls Pearson's theory of operational semiotics, which formalizes natural-language sentence structures … using mood and semantic operators' (cf. #801, #1541).",
            "THE ECONOMY. 'group sources on how signs circulate and shape perception as part of a broader semantic economy' — via an Are.na channel, keeper unestablished."],
  defects_judged=[]))

judged = {}
for i, c in enumerate(C, 1):
    raw = (H / c["file"]).read_text(); body = clean(raw)
    d = dict(BASE); d.update({k: c[k] for k in ("slug", "q", "s", "mt", "d", "per_v", "per", "per_note", "reading", "analysis", "findings", "q_kind")})
    d["originator"] = {"name": "Sharks, Lee", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full",
                       "basis": f"'{c['q']}' names a term or entity of the archive at alexanarch.org and its sites. Recorded 2026-11-23."}
    d["cite_list"] = c["cards"]; d["cites"] = len(c["cards"])
    d["archive_controlled_cites"] = sum(1 for x in c["cards"] if x["rel"] in ("archive_controlled", "authored_surface", "capture_of_capture"))
    d["transcript"] = HEAD.format(q=c["q"], body=body, hdr=c["hdr"]); d["transcript_raw"] = raw
    d["rounds"] = [{"n": 1, "prompt": c["q"], "note": "One answer."}]; d["related_deposits"] = c["related"]; d["dates"] = ["2026-11-23"]
    (H / f"draft-{i}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1)); judged[c["slug"]] = c["defects_judged"]
    print(i, c["slug"], "cites", d["cites"], "archive", d["archive_controlled_cites"], "chars", len(d["transcript"]), "goto left", d["transcript"].count("goto"))
(H / "judged-defects.json").write_text(json.dumps(judged, indent=1))
