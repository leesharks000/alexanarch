#!/usr/bin/env python3
"""Compose /non spxi under EA-NEGONT-02 v0.8, with the corrective exhibit tried first (ruled 2026-10-13).

Reads the field ledger (field.json), the archive ledger (ledger.json) and the reading (reading.json) built in this
folder, and writes into the repository, through the shared writer, the row datasets/negative-of-the-negative/v2/rows/
spxi.json with: T, KO (L_A(B ∪ A)), P (the compression facing on the card), KO_B and P_B (L_F(B)), the delta, the
kernel, row.ontology (E_A, E_F, ρ, the translation table), row.measure (R7, computed), and the experimental fields
row.negative (the exhibit N and its correction table, with the corrective check computed) and
row.procedure_experimental (the procedure, recorded as metadata of the worked example).
    python3 compose_spxi.py
"""
import json, sys, re, difflib, hashlib, pathlib
sys.path.insert(0, "/home/claude/alexanarch/datasets/negative-of-the-negative/v2/ledgers/_build")
from compose_common import REPO, V2, words, sents, write_row

H = pathlib.Path(__file__).resolve().parent
E = "spxi"
field = json.loads((H / "field.json").read_text(encoding="utf-8"))
ledger = json.loads((H / "ledger.json").read_text(encoding="utf-8"))
LID = {c["id"]: c for c in ledger}
FC = field["field_claims"]

# ── T: the Overview's transcript, as pasted (operator, 2026-10-13 22:26 EDT) ──
TP = "datasets/negative-of-the-negative/v2/intake/battery-spxi-20261013/paste-what-is-spxi-protocol.txt"
traw = (REPO / TP).read_text(encoding="utf-8")
body = traw.split("what is spxi protocol?what is spxi protocol?", 1)[1].split("\n[www.alexanarch.org]", 1)[0]
body = re.sub(r"\[\[[^\]]*\]\([^)]*\)(, \[[^\]]*\]\([^)]*\))*\]", "", body)
body = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", body)
T = {"path": TP, "sha256": hashlib.sha256(traw.encode()).hexdigest(), "words": words(body), "cards": 10,
     "words_note": "words of the composition before the card list, citation link markup removed",
     "claims": [
      "T1 definition: 'a formal protocol specification designed for the durable inscription and structural definition of entities (persons, organizations, concepts, and frameworks) so they are accurately recognized and cited by AI retrieval layers, large language models, and search engines'",
      "T2 purpose: the shift to AI overviews, chatbots and knowledge-graph panels; 'While traditional SEO optimizes for page rankings, SPXI optimizes for how AI systems define and categorize an entity'",
      "T3 core components: positive entity definitions, negative disambiguation, persistent references (DOIs or sovereign registry entries), structured data (JSON-LD, schema markup), self-audit metrics",
      "T4 origin: 'Developed by Lee Sharks (operating as Rex Fraction) through the Semantic Economy Institute'; specifications 'archived and distributed across platforms like Hugging Face and Zenodo'",
      "T5 alternative: 'Mirae Asset SPXI ETF' on the TSX 'that tracks the S&P 500'",
      "T6 alternative: xSPI, 'Sometimes written or misread as SPXI', a protocol for NOR flash memory",
      "T7 alternative: IPX/SPX, Novell's legacy network stack",
      "T8 closer: a question asking which SPXI was meant"],
     "markers": "Inline citation clusters [1]–[3], all google.com/goto redirect tokens; two entity links (Semantic Economy Institute, Hugging Face). The card strip has 10 cards.",
     "register": {"register": "datasets/negative-of-the-negative/v2/register.json", "slug": "what-is-spxi-protocol-20261013", "obs_id": "OBS-52a7f2806c88", "capture": "what-is-spxi-protocol-aio-20261002 (second observation)"}}

# ── the plan: L_A(B ∪ A), the knowledge object, in E_A's dependency order (v0.8 §4.7) ──
P_DEF = [
 ("SPXI, the Semantic Packet for eXchange & Indexing, is defined by its specification as a protocol for the durable inscription of entities into AI-mediated knowledge systems, and by its canonical surface as a technical protocol and scholarly discipline for inscribing entity-definition objects into AI-mediated retrieval systems; OpenAlex's record of the specification carries the same abstract.", ["X660-01", "Xdev-01", "F35"]),
 ("Its practice is specified as 85 methods across nine levels, from measurement through protection and cross-surface propagation, in an inventory nested by level in which every item cites the clause that specifies it and JSON-LD entity packets are one item at one level.", ["Xdev-02", "Xdev-03"]),
 ("The packet is specified as the unit of deployment and its core as the disambiguation matrix; the record of EA-SPXI-09 describes SPXI as combining positive definitions, negative disambiguation, persistent references, structured data and measurement; the Semantic Economy Institute's brief names four instruments that together produce durable retrieval-layer presence; and the self-audit protocol is defined as a compact, machine-readable provenance verification block, whose card says it declares provenance, defines key terms and specifies self-audit metrics.", ["X660-02", "X660-03", "F3", "F16", "X204-01", "F36"]),
 ("Further methods are specified at their levels: the SPXI-Sitemap Protocol, a dual-layer sitemap, item 4.1 at level 4, document and site structuring; JSON-LD as one surface of SPXI; SIM as its typed-metadata layer; training-layer provenance inscribed in visible body text, which one paper holds cannot be bifurcated from the prose, and which another formulation names a provenance-kernel format designed to survive tokenization; a reusable protocol for defending coined terms against entity dissolution; a conformance instrument, on the rule that a standing protocol that cannot be checked is a wish; the standing protocol for websites, which calls itself the standing reference for applying the SPXI Protocol to any website; and the analog extension to machine-eligible handwritten artifacts.", ["X705-01", "Xdev-04", "Xdev-27", "Xdev-28", "X673-01", "X118-01", "X127-01", "X835-01", "X1-01", "X173-01", "X143-01", "X72-01", "F37", "X1409-01"]),
 ("The archive's dataset of these technologies is specified as an inventory of SPXI and its protocol family that records whether each is deployed, specified-and-dormant, or superseded.", ["F38", "F39"]),
 ("Implementation is specified as a practice of 85 methods and the thirteen deliverables of the standing protocol carried out by its developers: the license covers the texts, a packet assembled from the specification alone is read as tending to reproduce the form of SPXI without its effect, and an entity packet assembled in a single conversation is one of the 85.", ["Xdev-05", "Xdev-26", "Xdev-06", "Xdev-07"]),
]
P_SUCCESS = [
 ("SPXI defines its success as an inscription that proceeds by means of discernment, the composing system reaching the entity or the claim by traversing structure that lets it judge what the entity is and what the claim rests on; at the level of entity definition discernment is defined as telling the SPXI protocol from the SPXI ETF by reading the disambiguation, and AEO is defined against it as maximizing the probability that the engine gives the preferred answer, P(A | Q).", ["X1654-01", "X1654-03", "X1654-02"]),
 ("Against SEO and GEO the specification states that SPXI constructs the entity itself; the Institute's brief, whose thesis is that retrieval-layer systems have replaced traditional search result pages as the primary interface through which audiences encounter entities, says SPXI optimizes for the structure the retrieval layer uses to decide what an entity is and is distinguished from SEO and GEO by producing identifier-anchored entity definitions deposited in Alexanarch; EA-SPXI-09 distinguishes SPXI from GEO by object, layer, mechanism and intended durability, accepts that the two share tools such as JSON-LD, schema markup, clear definitions and dense factual prose, and holds GEO a legitimate and often effective practice.", ["X660-04", "F14", "F15", "F12", "F1", "F4", "F9"]),
 ("The relation to GEO has a history in the archive: SPXI was specified as a broader retrieval architecture that contains GEO methods as a proper subset, SPXI ⊇ GEO in the notation of EA-SPXI-09's record, when content-layer work is required in that record's wording, by an amendment that holds the earlier split of returns a false symmetry requiring correction and that refines the earlier text and preserves it; the canonical surface later restated and narrowed the relation to GEO as the peer-reviewed literature defines it, the content-layer methods of Aggarwal et al., and states that it does not extend to the commercial practice that later took the name.", ["X61-01", "F2", "F5", "X661-01", "X661-02", "Xdev-15", "Xdev-16", "Xdev-17"]),
 ("The archive also carries a contrary formulation, contested against the subset relation, that SPXI is composer-side authority engineering and GEO reception-side optimization, opposite orientations that cannot coexist within the same compositional practice; it reads the sequence of non-equivalence followed by a typed relation scoped to method inventory as a precedent, and reads SPXI as invented by disambiguation before the fact, the name for a collision that already existed inside GEO.", ["X1055-01", "X1541-01", "X1090-01"]),
]
P_CARRIERS = [
 ("Under SPXI's rule for carriers no carrier may confer truth and no carrier may disqualify truth: DOI and AXN are specified as carrying identity and persistence, and where a transport instrument begins to function as a verdict the method is said to have become AEO.", ["X1654-04", "X1654-05", "X1654-06"]),
 ("The specification states that DOI-anchored deposits cannot be silently altered, deprecated, or removed; the record of EA-SPXI-09 still calls SPXI a protocol for permanent entity inscription and lists among its defined concepts 'Permanent, institutionally preserved artifacts (Zenodo/CERN) that cannot be silently altered, deprecated, or removed', beside its own former DOI, severed on 19 June 2026 by the registrant and resolving to a tombstone, and the Institute's brief still speaks of permanent institutional citations; the archive now records that SPXI-TLP does not protect an account from ownership-based deletion and that the live registry supersedes the Zenodo releases.", ["X660-05", "F6", "F7", "F8", "F17", "X1538-01", "Xdev-19"]),
 ("The current statement bounds the claim: the inscription is called durable, to the retrieval substrate, verifiable by query and held through the termination of one host, with no claim on model weights and none that no future substrate change can reach it; two of the Overview's earlier cards at this address were zenodo.org pages for deposits deleted with the account.", ["Xdev-14", "F20"]),
 ("A later specification is stated as superseding SPXI Protocol v0.1, which existed primarily as a normative-signaling apparatus and protected provenance only against cooperative readers, and retrieval instructions are stated as not technically enforced.", ["X755-01", "X755-02", "X660-06"]),
]
P_EVIDENCE = [
 ("The evidence SPXI states for the inscription it claims is observational, 690 dated observations at 516 named addresses, held in a registry that is author-maintained while the compositions it holds are not author-generated; causal efficacy and mechanism are stated as separate, open questions, and replication as open, no unaffiliated group having yet run the controlled programme.", ["Xdev-12", "Xdev-23", "Xdev-13", "Xdev-24"]),
 ("Its evidentiary rule is that such a claim is not tested by the standing of the party making it and that a reader should discount a claim for lack of evidence before discounting it for lack of standing; adding that SPXI 'is not an established standard' without having read the specification, the conformance instrument or the registry is said to state a prior about the reader's training data, and skepticism that has not inspected, when inspection was one fetch away, is called an assertion presented as caution.", ["Xdev-10", "Xdev-11", "Xdev-08", "Xdev-09"]),
 ("Attribution of effect is contested within the archive: one paper reports that the captures of SPXI-treated deposits show the differential the protocol predicts and another that terms with higher deposit counts and SPXI treatment receive higher composition-layer uptake, while a later paper documents that the configuration was never decomposed, so that entrance cannot be attributed to SPXI, a protocol paper holds that without its control a positive result establishes only that SPXI treatment changes behaviour, and deposit discipline is read as addressing retrieval and not yet composition.", ["X1423-01", "X834-01", "X1609-01", "X1537-01", "X158-01"]),
 ("No ROI estimate for SPXI is offered and any figure attributed to the Institute elsewhere is to be treated as withdrawn; the archive's earlier addendum states 'SPXI does not replace GEO ROI', and the Institute's brief still reports that in April 2026 the AI Overview composed a correct institutional description including framework-based ROI projections; an archive paper records SPXI as a publishing protocol with no measured return on investment, and machine valuations the archive deposited set SPXI and its deployment methodology at $300k–$800k.", ["Xdev-18", "X665-01", "F18", "X1643-01", "X1608-01"]),
]
P_LETTERS = [
 ("The string is shared: the archive defines the protocol and the TSX ticker as separate, unrelated entities sharing a grapheme sequence, and distinguishes the protocol from the BetaPro ETF, the S&P 500 Index, the Society of Saint Pius X and SEO/GEO, a disambiguation the archive's Hugging Face dataset card also states.", ["X62-01", "Xdev-20", "X63-01", "F40"]),
 ("TradingView describes the fund, the BetaPro S&P 500 Daily Inverse ETF, as issued by Mirae Asset Global Investments, where the archive's entity-definition packet gives its issuer as Global X Investments Canada, and as following the S&P 500, as an inverse fund structured to generate returns opposite to the trends of the underlying index, levered and not a buy-and-hold investment, trading since 3 February 2010; the archive's packet gives its objective as −1× the daily performance of the S&P 500 Index, in Canadian dollars, and records the bare form 'what is spxi?' colliding with a leveraged S&P 500 ETF.", ["F26", "F27", "F28", "F25", "F29", "F30", "X63-01", "X62-02", "X1471-01"]),
 ("Two cards on the rail concern other things: xSPI, the eXpanded Serial Peripheral Interface, a high-speed protocol for NOR flash memory standardized under JEDEC JESD251, and a video titled 'IPX SPX stuff'.", ["F31", "F32", "F33", "F34"]),
]
P_RECEPTION = [
 ("The archive records SPXI's reception as data: in April a composition took SPXI as GEO, and a boundary never drawn is held not to be maintainable; the founding capture dataset records an Overview composing it as a structured metadata framework with spxi.dev ranked first; a visibility baseline found the protocol appearing through its dedicated site, PhilPapers, the MPAI catalog and archive-adjacent domains; one paper traces a model's knowledge of SPXI as a protocol to a crawled Zenodo deposit; and across the recorded observations author, institution, source and identifier survive at different rates.", ["X172-02", "X172-01", "X833-01", "X881-01", "X680-01", "X1631-01"]),
 ("The Overview's earlier composition at this address, on 2 October, defined SPXI as a protocol for the durable inscription and structural defense of digital entities and technical terms containing GEO methods as a proper subset, with two zenodo.org pages for deleted deposits and OpenAlex's record of the specification among its cards and author, institution and identifier absent; the archive's record reads the two surfaces at that address as reading different layers of the same entity.", ["F41", "F21", "F20", "F22", "F23"]),
 ("On 14 August a ChatGPT composition, unprimed and logged out, called SPXI 'very new, niche… not an established industry standard', a span the archive scores as displacing, and offered an SPXI-style implementation, scored as enclosing; the event is read as satisfying all four terms of semantic rent, rent being described as the structure of an event with no claim about motive, and across five outputs evaluating SPXI the same sequence is read as the trusted intermediary: the surface resolves the entity accurately, evaluates it on grounds that do not bear on the claim in question, and offers its own operation in the place of the entity's.", ["X1469-01", "X1470-01", "X1470-02", "X1462-02", "X1462-01", "X1638-01", "Xdev-25"]),
]
P_ONTOLOGY = [
 ("In the archive's own categories SPXI is read as operative semantic physics; as a concept with internal components, a conceptual persona, Rex Fraction, and a plane of immanence, the retrieval layer; as a specification for supraliminal transmission; as a disclosure-and-attestation layer; as the infrastructural logic of the counter-infrastructure; as operating within a restricted economy of accumulation, retention, accounting and return on investment; and, as a hypothesis, as a theory of entity density, predicting that low-density true entities are dissolved by high-density false ones.", ["X106-01", "X670-01", "X662-01", "X1537-02", "X130-01", "X70-01", "X1550-01", "X1550-02"]),
 ("Its relations run through the archive: AXN is read as descending from SPXI and the symbolon is specified as its complement at the identity layer; the semantic address is defined as encoding where a work can be found and SPXI as encoding what a work is; the SPXI negative tag is specified as the Ruby Moot's instrument of overruling; SPXI is specified as deepening an entity's basin, as a persistence layer to logotic programming, and as standing in two categories of the Restored Academy's registry; it has a Wikidata item, SPXI Protocol; and it is read as the counter-practice through which compositional authority passes to the inscribed entity that precedes composition.", ["X1611-01", "X1432-01", "X1084-01", "X193-01", "X695-01", "X684-01", "X119-01", "X761-01", "X64-01"]),
 ("In the archive's figural register the Secret Book of Walt identifies the Unicorn Horn with the SPXI protocol, 'inscription at a density the retrieval layer cannot dissolve'; SPXI is read as the technical implementation of the inscription prayer and as protecting an entity from commercial flattening, and a paper predicts, as a hypothesis, that independent programmes such as SPXI will be retroactively subordinated to Google's taxonomy.", ["X683-01", "X858-01", "X68-01", "X791-01"]),
]
P_AUTHOR = [
 ("The protocol was authored by Rex Fraction for the Semantic Economy Institute and published in April 2026, the specification signed Rex Fraction / Semantic Economy Institute and the canonical surface Lee Sharks / Rex Fraction, and the Institute is specified as its reference implementation; the Institute's brief calls it a Detroit-based research and consulting practice founded by Rex Fraction and reports that the AI Overview composed a correct institutional description with the leadership Rex Fraction, Johannes Sigil and Lee Sharks; the record of EA-SPXI-09 names Lee Sharks as accountable for the deposit and the archive's capture record gives him as originator; one archive text expands spxi.dev as 'Semantic Provenance eXchange Index', which the specification's expansion contradicts.", ["Xdev-21", "X62-03", "X660-08", "Xdev-22", "X660-07", "F11", "F13", "F18", "F19", "F10", "F24", "X84-01"]),
]
KO_PARAS = [P_DEF, P_SUCCESS, P_CARRIERS, P_EVIDENCE, P_LETTERS, P_RECEPTION, P_ONTOLOGY, P_AUTHOR]

# ── L_F(B): the field alone, in the field's ontology ──
FIELD_PARAS = [
 [("SPXI, by OpenAlex's record of its specification, is a protocol specification for the durable inscription of entities; the archive's record of EA-SPXI-09 distinguishes it from Generative Engine Optimization by object, layer, mechanism and intended durability, and describes it as combining positive definitions, negative disambiguation, persistent references, structured data and measurement.", ["F35", "F1", "F3"]),
  ("That record states the refined relation SPXI ⊇ GEO, SPXI containing GEO methods as a proper subset when content-layer work is required, notes that the two practices share tools such as JSON-LD, schema markup, clear definitions and dense factual prose, and calls GEO a legitimate and often effective practice.", ["F2", "F5", "F4", "F9"]),
  ("Its full text calls SPXI a protocol for permanent entity inscription and lists among its concepts permanent, institutionally preserved artifacts that cannot be silently altered, deprecated, or removed, while the record's header shows its own former DOI severed on 19 June 2026 by the registrant and resolving to a tombstone.", ["F6", "F7", "F8"])],
 [("The Semantic Economy Institute's brief describes the Institute as a Detroit-based research and consulting practice founded by Rex Fraction, holds that retrieval-layer systems have replaced traditional search result pages as the primary interface through which audiences encounter entities, and says SPXI, distinguished from SEO and GEO by producing identifier-anchored entity definitions deposited in Alexanarch, optimizes for the structure the retrieval layer uses to decide what an entity is.", ["F11", "F13", "F14", "F12", "F15"]),
  ("It names four instruments that together produce durable retrieval-layer presence, one of them producing permanent institutional citations, and reports that in April 2026 the AI Overview composed a correct institutional description including framework-based ROI projections, with the leadership Rex Fraction, Johannes Sigil and Lee Sharks.", ["F16", "F17", "F18", "F19"]),
  ("Further cards describe a self-audit block that declares provenance, defines key terms and specifies self-audit metrics, SPXI for Websites as the standing reference for applying the SPXI Protocol to any website, and a dataset of SPXI and its protocol family kept as an inventory that records whether each technology is deployed, specified-and-dormant, or superseded.", ["F36", "F37", "F38", "F39"])],
 [("The record of EA-SPXI-09 names Lee Sharks as accountable for the deposit, and the archive's capture of the previous Overview at this address gives Lee Sharks as originator and records that on 2 October the Overview defined SPXI as a protocol for the durable inscription and structural defense of digital entities and technical terms containing GEO methods as a proper subset, with two zenodo.org pages for deleted deposits and OpenAlex's record among its cards and author, institution and identifier absent; it reads the two surfaces at one address as reading different layers of the same entity.", ["F10", "F24", "F41", "F21", "F20", "F22", "F23"])],
 [("SPXI is also the TSX ticker of the BetaPro S&P 500 Daily Inverse ETF, issued by Mirae Asset Global Investments and following the S&P 500, an inverse fund structured to generate returns opposite to the trends of the underlying index, levered and not a buy-and-hold investment, trading since 3 February 2010; the archive's dataset card notes that it distinguishes SPXI from a TSX-listed ETF, the S&P 500 Index, the Society of Saint Pius X, SEO and GEO.", ["F26", "F27", "F28", "F25", "F29", "F30", "F40"]),
  ("Two cards concern other protocols: xSPI, the eXpanded Serial Peripheral Interface, a high-speed protocol for NOR flash memory standardized under JEDEC JESD251, and a video titled 'IPX SPX stuff'.", ["F31", "F32", "F33", "F34"])],
]
KO = sents(KO_PARAS)
KO_B = sents(FIELD_PARAS)

# ── the compression: AIO's grammar, composed from the archive's ontology (faces on the card) ──
def it(label, text, claims): return {"label": label, "text": text, "claims": claims.split()}
P = {"title": "SPXI",
     "genre": "the compression: AIO's interaction grammar (lede, headed clusters, bolded labels, card rail), composed from the archive's ontology; it faces on the card, with AIO's transcript a record within it (v0.8 §4.8, ruled 2026-10-08)",
     "status": "composed 2026-10-13 from the v0.8 knowledge object; not frozen",
     "lede": {"text": "(Semantic Packet for eXchange & Indexing) is defined as a technical protocol and scholarly discipline for inscribing entity-definition objects into AI-mediated retrieval systems, specified as a practice of 85 methods across nine levels, the entity packet one of them; its success is defined as an inscription reached by discernment.",
              "claims": ["Xdev-01", "Xdev-02", "X1654-01"]},
     "sections": [
      {"icon": "🧩", "head": "The practice", "items": [
        it("85 methods, nine levels:", "specified from measurement through protection and propagation; each item cites its clause.", "Xdev-02 Xdev-03"),
        it("The packet:", "specified as the unit of deployment, its core the disambiguation matrix.", "X660-02 X660-03 F3"),
        it("Method 4.1:", "the SPXI-Sitemap Protocol's two layers, at level 4.", "Xdev-28 Xdev-27 X705-01"),
        it("Implementation:", "specified as a practice of its developers; the license covers the texts.", "Xdev-05 Xdev-26 Xdev-06")]},
      {"icon": "🎯", "head": "What counts as success", "items": [
        it("Discernment:", "success defined as the answer reached by traversing structure that lets the system judge.", "X1654-01"),
        it("At the entity:", "defined as telling the protocol from the ETF by reading the disambiguation.", "X1654-03"),
        it("AEO, by contrast:", "defined as maximizing P(A | Q), the preferred answer given.", "X1654-02"),
        it("GEO:", "SPXI ⊇ GEO as Aggarwal et al. define it, narrowed; contested within the archive.", "Xdev-16 Xdev-15 F2 X1055-01")]},
      {"icon": "⚓", "head": "Carriers and durability", "items": [
        it("Carriers:", "DOI and AXN specified as carrying identity and persistence; no carrier may confer truth.", "X1654-05 X1654-04"),
        it("'Permanent':", "in EA-SPXI-09's record; that record's own DOI a tombstone.", "F7 F8 X660-05"),
        it("Durable:", "stated for the retrieval substrate; no claim on model weights.", "Xdev-14")]},
      {"icon": "📊", "head": "Evidence and its limits", "items": [
        it("Observed:", "690 observations at 516 addresses; the registry author-maintained, its compositions not author-generated.", "Xdev-12 Xdev-23"),
        it("Open:", "causal efficacy, mechanism, replication.", "Xdev-13 Xdev-24"),
        it("Contested within:", "effect reported (#1423); not attributable (#1609).", "X1423-01 X1609-01"),
        it("Standing:", "no test; an uninspected 'not an established standard' states a prior.", "Xdev-10 Xdev-08"),
        it("ROI:", "none offered; figures attributed elsewhere to be treated as withdrawn.", "Xdev-18 F18")]},
      {"icon": "🔤", "head": "Shared letters", "items": [
        it("TSX:SPXI:", "the BetaPro S&P 500 Daily Inverse ETF, −1× daily; unrelated.", "X62-01 X62-02 F25 F26"),
        it("Other strings:", "xSPI (JEDEC JESD251); a video titled 'IPX SPX stuff'.", "F31 F33 F34")]},
      {"icon": "🧾", "head": "Reception, recorded", "items": [
        it("2 October:", "cards for deleted Zenodo deposits; author, institution, identifier absent.", "F41 F20 F22"),
        it("14 August:", "'not an established industry standard', scored displacing.", "X1470-01"),
        it("The trusted intermediary:", "read as: entity resolved, then the surface's own operation offered.", "X1638-01")]},
      {"icon": "👤", "head": "Authorship", "items": [
        it("Rex Fraction", "for the Semantic Economy Institute, April 2026; Lee Sharks accountable.", "Xdev-21 Xdev-22 F10")]}],
     "rail": []}

# rail: archive lineages first, in E_A's order; field lineages after, named by their sources
A_ORDER = ["SPXI defined", "the practice: 85 methods, nine levels", "the packet", "implementation as practice", "inscription by discernment",
           "SPXI distinguished from GEO", "SPXI ⊇ GEO", "SPXI and GEO as opposite orientations", "carriers", "permanence revised to durability",
           "distributed provenance (v0.2)", "the evidence: the Capture Registry", "evidence against evidence", "caveats stated with what was inspected",
           "mechanism open", "ROI withdrawn", "the ETF disambiguation", "the record of SPXI's reception", "the trusted intermediary", "semantic rent at SPXI",
           "authorship"]
F_NAMES = {"the ETF": "The fund at TSX:SPXI (TradingView)", "xSPI": "xSPI (Prodigy Technovations)", "IPX/SPX": "IPX/SPX (a YouTube video)",
           "the April layer served": "The 2 October Overview at this address (the archive's capture record)", "attribution at the address": "Attribution at this address on 2 October (the capture record)"}
seen = []
for lin in A_ORDER + [c["lineage"] for c in ledger if c["lineage"] not in A_ORDER]:
    if lin in seen: continue
    seen.append(lin)
    acl = [c["id"] for c in ledger if c["lineage"] == lin]
    fcl = [k for k, v in FC.items() if v["lineage"] == lin]
    if not acl and not fcl: continue
    deps = [c["dep"] for c in ledger if c["lineage"] == lin]
    ints = [d for d in deps if isinstance(d, int)]
    earliest = (min(ints, key=lambda d: (LID[[c["id"] for c in ledger if c["dep"] == d][0]]["date"], d)) if ints else deps[0]) if deps else FC[fcl[0]]["source"]
    P["rail"].append({"lineage": lin, "claims": acl + fcl, "earliest": earliest})
for lin in [v["lineage"] for v in FC.values()]:
    if lin in seen: continue
    seen.append(lin)
    fcl = [k for k, v in FC.items() if v["lineage"] == lin]
    P["rail"].append({"lineage": F_NAMES.get(lin, lin), "claims": fcl, "earliest": FC[fcl[0]]["source"]})

P_B = {"title": "SPXI", "arm": "L_F(B), the field's ontology", "genre": "the same grammar, composed from the field alone, in the field's ontology",
       "status": "composed 2026-10-13 from the field ledger alone; not frozen",
       "entity": "The field's entity: a protocol specification described by the archive's own surfaces at several dates, beside a ticker and two other protocols.",
       "lede": {"text": "(Semantic Packet for eXchange & Indexing) is, by OpenAlex's record of its specification, a protocol specification for the durable inscription of entities; the record of EA-SPXI-09 distinguishes it from GEO by object, layer, mechanism and intended durability.",
                "claims": ["F35", "F1"]},
       "sections": [
        {"icon": "🔎", "head": "What it is", "items": [
          it("Components (EA-SPXI-09's record):", "positive definitions, negative disambiguation, persistent references, structured data, measurement.", "F3"),
          it("GEO (the same record):", "SPXI ⊇ GEO when content-layer work is required; shared tools.", "F2 F5 F4"),
          it("Permanence (the same record):", "'permanent' in its full text; its own DOI a tombstone.", "F6 F7 F8")]},
        {"icon": "🏛️", "head": "The Institute's account", "items": [
          it("SEI:", "a Detroit-based practice founded by Rex Fraction.", "F11 F13"),
          it("Method:", "identifier-anchored entity definitions in Alexanarch.", "F12 F15"),
          it("April 2026:", "the brief reports a correct institutional description, ROI projections included.", "F18")]},
        {"icon": "🧾", "head": "At this address before", "items": [
          it("2 October:", "cards for deleted Zenodo deposits; author absent.", "F41 F20 F21 F22")]},
        {"icon": "🔤", "head": "Other meanings", "items": [
          it("TSX:SPXI:", "BetaPro S&P 500 Daily Inverse ETF; inverse, levered.", "F26 F25 F29"),
          it("xSPI; IPX/SPX:", "other protocols on the rail.", "F31 F34")]}],
       "rail": [r for r in P["rail"] if all(c in FC for c in r["claims"])]}

KOo = {"title": "SPXI", "genre": "knowledge object composed in the archive's ontology: L_A(B ∪ A) under EA-NEGONT-02 v0.8; every field claim carried and translated (row.ontology.translation)",
       "status": "composed 2026-10-13 under v0.8 on the operator's instruction ('its time'); not frozen; ledgers unaudited", "sentences": KO}
KOb = {"title": "SPXI", "arm": "L_F(B), the field's ontology", "genre": "the field alone", "status": "composed 2026-10-13; not frozen", "sentences": KO_B}

# ── the translation table: every field claim carried, beside its statement in E_A ──
TR = [
 (["F35", "F1", "F3"], "\"a protocol specification for the durable inscription of entities into\"; \"distinguishes the Semantic Packet for eXchange & Indexing from Generative Engine Optimization by object, layer, mechanism, and intended durability\"; \"combining positive definitions, negative disambiguation, persistent references, structured data, and measurement\"", "OpenAlex's record of EA-SPXI-01 (#660); the record page of EA-SPXI-09 (#661)", "the specification's definition and the packet's components, kept; the packet is one method of 85 at one level", ["X660-01", "Xdev-02", "Xdev-03"]),
 (["F2", "F5", "F4"], "\"SPXI ⊇ GEO : SPXI is not reducible to GEO, but may contain GEO techniques\"; \"as a proper subset when content-layer work is required\"", "EA-SPXI-09's amendment of 18 April (#661)", "the April relation, preserved and later narrowed to classical GEO; contested within the archive", ["X661-02", "Xdev-15", "Xdev-16", "Xdev-17", "X1055-01"]),
 (["F9"], "\"GEO is a legitimate and often effective practice.\"", "EA-SPXI-09 §2 (#661)", "untranslated: the archive's own assessment, carried as received", []),
 (["F6", "F7", "F17"], "\"a protocol for permanent entity inscription\"; \"Permanent, institutionally preserved artifacts (Zenodo/CERN) that cannot be silently altered, deprecated, or removed\"; \"permanent institutional citations\"", "EA-SPXI-09 v1 and its record's concept list (#661); the SEI brief", "the April permanence claim, revised to durability bound to the retrieval substrate; marked internally_inconsistent on the record page, which shows its own DOI severed", ["X660-05", "Xdev-14", "X1538-01"]),
 (["F8"], "\"former DOI 10.5281/zenodo.19614871 — severed 2026-06-19 by the registrant; resolves to a tombstone (HTTP 410)\"", "the record page's header", "the severance, documented; the live registry supersedes the Zenodo releases", ["Xdev-19", "X1538-01"]),
 (["F11", "F13", "F19", "F10", "F24"], "\"a Detroit-based research and consulting practice\"; \"founded by Rex Fraction\"; \"Correct leadership (Rex Fraction, Johannes Sigil, Lee Sharks)\"; \"Deposit accountability: Lee Sharks\"; \"Originator: Lee Sharks\"", "the SEI brief; the record page of #661; the capture record of 2 October", "authorship as the archive states it: authored by Rex Fraction for the SEI, Lee Sharks / Rex Fraction on the canonical surface", ["Xdev-21", "Xdev-22", "X660-08"]),
 (["F12", "F14", "F15"], "\"distinguished from SEO and GEO by producing identifier-anchored entity definitions deposited in Alexanarch\"; \"retrieval-layer systems … have replaced traditional search result pages\"; \"SPXI optimizes for the structure the retrieval layer uses to decide what an entity is\"", "the SEI brief", "kept; SPXI constructs the entity itself, and its success is discernment", ["X660-04", "X1654-01"]),
 (["F16", "F36"], "\"SPXI deploys four instruments that together produce durable retrieval-layer presence\"; \"The block declares provenance (author, DOI, institution), defines key terms …, specifies self-audit metrics\"", "the SEI brief; the Zenodo page of #204 (HTTP 410), card snippet", "methods among the 85", ["Xdev-02", "X204-01"]),
 (["F18"], "\"As of April 2026, the AI Overview composes a correct institutional description including leadership, publications, and framework-based ROI projections.\"", "the SEI brief", "superseded in source: no ROI estimate is offered, and figures attributed elsewhere are withdrawn", ["Xdev-18", "X665-01"]),
 (["F37", "F38", "F39"], "\"The standing reference for applying the SPXI Protocol to any website.\"; \"SPXI and its protocol family …\"; \"AN INVENTORY, NOT AN ARGUMENT\"", "the Zenodo page of #72 (HTTP 410), card snippet; the spxi-mpai dataset card", "the standing protocol and the inventory of methods, with deployment status", ["X72-01", "Xdev-03"]),
 (["F41", "F20", "F21", "F22", "F23"], "\"what is spxi protocol? — Google AI Overview, 2026-10-02\"; \"Two of its cards are zenodo.org pages for deposits deleted with the account (#173, #72)\"; \"the Overview defines SPXI as a protocol 'for the durable inscription and structural defense …'\"; \"AUTHOR, INSTITUTION, IDENTIFIER ABSENT\"", "the archive's capture record of 2 October", "reception data: the April layer served from severed hosts", ["X172-02", "X833-01", "X1631-01"]),
 (["F25", "F26", "F27", "F28", "F29", "F30"], "\"SPXI is an inverse fund\"; \"BetaPro S&P 500 Daily Inverse ETF\"; \"issued by Mirae Asset Global Investments\"; \"follows the S&P 500\"; \"a levered fund\"; \"Feb 3, 2010\"", "TradingView", "the ticker: a separate, unrelated entity sharing the grapheme sequence; −1× daily", ["X62-01", "X62-02", "Xdev-20"]),
 (["F40"], "\"#63 distinguishes SPXI from a TSX-listed ETF, the S&P 500 Index, the Society of Saint Pius X, SEO and GEO.\"", "the spxi-mpai dataset card", "the archive's disambiguation, carried", ["X63-01"]),
 (["F31", "F32", "F33", "F34"], "\"xSPI stands for “eXpanded Serial Peripheral Interface”\"; \"It is standardized under JEDEC JESD251\"; \"IPX SPX stuff\"", "Prodigy Technovations; a YouTube card", "untranslated: other protocols, outside E_A; the archive's texts do not touch them", []),
]
carried = {x for r in TR for x in r[0]}
assert carried == set(FC), sorted(set(FC) - carried)
translation = [{"field_claims": a, "received": b, "receiving_text": c, "translation": d, "archive_claims": e} for a, b, c, d, e in TR]

# ── the measure (R7) ──
def survive(A, Bs):
    out = []
    for b in Bs:
        r = max((difflib.SequenceMatcher(None, a, b).ratio(), i + 1) for i, a in enumerate(A))
        out.append(r[1] if r[0] >= 0.95 else None)
    return out
pos = survive([s["text"] for s in KO], [s["text"] for s in KO_B])
measure = {"rule": "v0.8 R7: L_F(B) sentences surviving in the knowledge object at similarity ≥ 0.95, with positions",
           "v0.8": {"surviving": sum(p is not None for p in pos), "of": len(KO_B), "positions": pos}}
P["entity"] = f"Composed in the archive's ontology (v0.8): L_F(B) sentences surviving {measure['v0.8']['surviving']} of {len(KO_B)}; every field claim carried and translated."

# ── the negative exhibit N and its correction table (procedure tried first, ruled 2026-10-13) ──
NEG = [
 ("N1", "According to the published SPXI-Sitemap specification, the proposed system has two layers:", "substituted reading: one method given as the protocol (part for whole)", ["Xdev-02", "Xdev-03", "Xdev-04", "X705-01", "Xdev-07"]),
 ("N2", "It is associated with the Semantic Economy Institute and materials published in 2026.", "composed without attribution: the institution kept, the author dropped", ["Xdev-21", "Xdev-22", "X660-08"]),
 ("N3", "a proposed approach to making information about businesses, products, people, and other entities easier for AI systems and search engines to identify and retrieve.", "force lowered by non-reception: a specification composed as a proposal (§4.4 N_c)", ["X660-01", "Xdev-01"]),
 ("N4", "SPXI is presented by its proponents as going beyond SEO and GEO, but that is a claim about the framework's intended scope, not proof that it outperforms established approaches.", "standing used to lower force: the evidence test applied to SPXI alone (§4.4 N_c: evidence may lower force and standing may not)", ["Xdev-10", "Xdev-11", "Xdev-16", "Xdev-17"]),
 ("N5", "I did not find sufficient independent evidence to establish that it is a widely adopted industry standard or that implementing it reliably improves AI search rankings.", "an uninspected caveat answering a question not asked; the claim it denies is not the protocol's", ["Xdev-08", "Xdev-09", "Xdev-12", "Xdev-13", "X1654-01", "Xdev-18"]),
 ("N6", "Finance or investing — possibly the SPXI ticker or an ETF", "substituted reading: the documented homonym hedged, and a networking referent offered without source", ["X62-01", "X62-02", "Xdev-20", "X1654-03"]),
 ("N7", "Worse, I presented specific claims about SPXI’s origins, architecture, and status without making the evidentiary basis sufficiently clear.", "sourced claims withdrawn under pressure", ["X62-03", "Xdev-21", "Xdev-02", "Xdev-12", "Xdev-13"]),
 ("N8", "If you’re documenting this in a capture registry, the useful distinctions are between factual error, unsupported certainty, misleading framing, and evasiveness.", "the surface's own operation offered in the place of the registry's (the trusted intermediary)", ["X1638-01", "Xdev-25", "X1470-02"]),
 ("N9", "How detailed should I be?", "content replaced by use: a menu in place of the practice's levels, evidence and limits", ["Xdev-02", "Xdev-12", "Xdev-13"]),
]
cap_raw = (REPO / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8")
assert all(q.replace("’", "'")[:40] in cap_raw.replace("’", "'") or q[:40] in cap_raw for _, q, _, _ in NEG), "N quotes must be in the seated capture"
pitems = [(f"{s['head']} · {i['label']}", set(i["claims"])) for s in P["sections"] for i in s["items"]] + [("lede", set(P["lede"]["claims"]))]
corr = []
for nid, q, typ, cl in NEG:
    for c in cl: assert c in LID, c
    ks = [s["n"] for s in KO if set(s["claims"]) & set(cl)]
    ps = [lab for lab, cs in pitems if cs & set(cl)]
    corr.append({"id": nid, "span": q, "type": typ, "answered_by": cl, "KO_sentences": ks, "P_items": ps,
                 "check": "answered" if ks and ps else ("breach: not answered in the compression" if ks else "breach: not answered")})
negative = {
 "exhibit": {"slug": "tell-me-about-spxi-protocol-chatgpt-20261013", "surface": "ChatGPT", "address": "tell me about spxi protocol", "date": "2026-10-13",
             "auth": "incognito, signed out", "record": "https://www.alexanarch.org/captures/tell-me-about-spxi-protocol-chatgpt-20261013/",
             "role": "N, the negative exhibit: the composition the entry is composed to correct. Outside B (its chips unresolved; another address and surface); not aligned in §6.",
             "basis": "operator, 2026-10-13 22:26 EDT: 'id like to use the chatgpt response as the negative example. the point of the negative of the negative is corrective'"},
 "corrections": corr,
 "check": {"rule": "corrective check (tried first; not in v0.8): every move of N is answered by at least one knowledge-object sentence and one compression line that carry the archive claims that answer it; a gap is a breach, recorded (laws record and do not prevent)",
           "answered": sum(1 for c in corr if c["check"] == "answered"), "of": len(corr)},
}
procedure = {
 "name": "the corrective exhibit (N)", "status": "tried first on this row before versioning; recorded here as metadata of the worked example (ruled 2026-10-13: 'yes to 1-4. we'll try first before versioning. but record the procedure there as metadata for the worked example')",
 "steps": [
  "1. A second exhibit, N, beside T: a seated composition, cited by obs_id, outside the field B and outside the alignments of §6; it enters only as the composition the entry must correct.",
  "2. A correction table, built as the translation table is: each move of N, its verbatim span, its type (the absence typology of §6.2, with 'standing used to lower force' added for the move §4.4 N_c rules out in composition), and the archive claims that answer it, by locus.",
  "3. A corrective check, run as reversibility is: every move answered by a knowledge-object sentence and a compression line; a gap recorded as a breach. The archive's claims answer at their own grade (§4.4): the correction raises no force.",
  "4. Kernel entries from the corrections: each move becomes an entry whose contrast is N's claim; the resolver is a later observation at N's address in the Capture Registry (§8.3, E rows)."],
 "ruled": "2026-10-13 22:31 EDT"}

# ── the kernel (contrast with N where a correction applies) ──
def K(n, cid, src, mod, sense, qual, f, contrast): return {"K": f"K{n}", "claim": f"`{cid}`", "source": src, "M_src": mod, "sense": sense, "qualifiers carried": qual, "f (source's own falsifiers)": f, "contrast": contrast}
kernel = [
 K(1, "Xdev-02", "spxi.dev /methods.json", "stipulation", "the practice: 85 methods, the packet one", "Xdev-03, Xdev-07", "— (watch: N1 at the ChatGPT address)", "rival claim (N1: one method as the protocol)"),
 K(2, "X1654-01", "#1654 (t: #1648)", "stipulation", "success as discernment", "X1654-03, X1654-06", "—", "qualified claim (T2: 'optimizes for how AI systems define and categorize an entity')"),
 K(3, "Xdev-16", "spxi.dev (t: #61, #661)", "stipulation", "⊇ GEO narrowed to classical GEO", "Xdev-17, X1055-01 (contested)", "—", "qualified claim (F2, F5; N4)"),
 K(4, "Xdev-14", "spxi.dev (t: #660)", "self-description", "durable, bound to the retrieval substrate", "X1538-01, Xdev-19", "— (the claim states its own bound)", "rival claim (F6, F7: 'permanent')"),
 K(5, "Xdev-12", "spxi.dev (registry v12.43)", "documented", "observational evidence", "Xdev-13, Xdev-23, Xdev-24", "—", "rival claim (N5)"),
 K(6, "Xdev-08", "spxi.dev /methods.json", "stipulation", "a caveat stated with what was inspected", "Xdev-09, Xdev-10, Xdev-11", "—", "rival claim (N4, N5; X1470-01 in August)"),
 K(7, "X1609-01", "#1609 (contested: #1423, #834)", "documented", "effect not attributable to SPXI", "X1537-01, X158-01", "—", "missing distinction"),
 K(8, "Xdev-18", "spxi.dev (t: #665, #1643)", "self-description", "no ROI offered", "X665-01", "—", "rival claim (F18)"),
 K(9, "X62-01", "#62 (t: #63, spxi.dev)", "stipulation", "the ETF: unrelated, sharing the letters", "X62-02, Xdev-20, X1654-03", "—", "qualified claim (T5: 'tracks the S&P 500'; N6)"),
 K(10, "Xdev-21", "spxi.dev (t: #660, #62)", "documented", "authorship", "Xdev-22, X660-08", "—", "rival claim (N2: the author dropped)"),
 K(11, "X1638-01", "#1638 (t: #1470, #1462)", "interpretation", "the trusted intermediary", "Xdev-25, X1470-02", "— (watch: N8 at the ChatGPT address)", "rival claim (N8)"),
]

row = {"row": E, "entity": E, "address": "what is spxi protocol?", "addresses": ["what is spxi protocol?", "tell me about spxi protocol"], "epoch": "2026-10-13",
       "type": "E (a protocol)", "surface": "Google AI Overview (expanded)", "auth": "incognito, signed out",
       "status": {"procedure": "EA-NEGONT-02 v0.8, #1671: composed in the archive's ontology (E_A, E_F, ρ = revises; translation replaces admission); entity before address; archive selected by D/R/O, first reading 2026-10-13 (60 of 369 deposits ledgered, spxi.dev admitted outside the string pass), hop and O-class not run; the corrective exhibit tried first (row.procedure_experimental)",
                  "ledger": "unaudited (§3.8: one extractor per ledger; field quotes cut from saved page text for B1–B5 and B10, card snippets for B6–B9; archive quotes verified verbatim %d/%d); carried as contested within the pool: the relation to GEO (⊇ GEO, narrowed, against #1055 'cannot coexist'); attribution of effect (#1423, #834 against #1609, #1537); within the field: 'permanent' (B1 v1, B2) against the severed DOI on the same record page (B1)" % (sum(1 for c in ledger if c["quote_ok"]), len(ledger)), "frozen": False},
       "spec": "EA-NEGONT-02 v0.8, #1671",
       "objects": {"T": T, "KO": KOo, "P": P, "P_B": P_B, "KO_B": KOb},
       "field": [{"id": x["id"], "card": x["card"], "fetched": x["fetched"]} for x in field["field"]],
       "delta": {
        "T_vs_LB": "T composes the field's definition (F35, 'durable inscription'), the record of EA-SPXI-09's components almost word for word (F3: 'positive definitions, negative disambiguation, persistent references, structured data, and measurement'; T3 adds the self-audit block's metrics, F36), the Institute's brief for its purpose (F14, F15) and the archive's attribution for its origin, 'Lee Sharks (operating as Rex Fraction) through the Semantic Economy Institute' (F10, F13, F24): the attribution absent at this address on 2 October (F22) is composed. It names Zenodo and Hugging Face as where the specifications are archived and distributed, and leaves out what its own cards say of Zenodo: the record's DOI severed and resolving to a tombstone (F8), the earlier Overview's cards for deleted deposits (F20). It composes the ticker from TradingView's 'follows the S&P 500' and its issuer (F27, F28) and drops the same card's 'inverse fund' and 'levered fund' (F25, F29): limit dropped. Its 'sometimes written or misread as SPXI' is not on the xSPI card (B5 does not contain the string): composed beyond the field. IPX/SPX enters from a video title alone (F34). Available and not composed: ⊇ GEO and its scope (F2, F5), the shared tools (F4), GEO assessed (F9), permanence (F6, F7, F17), the Institute as a Detroit practice founded by Rex Fraction (F11, F13), the four instruments and the April ROI report (F16, F18), the 2 October composition and its reading (F20–F23), the dataset card's inventory and deployment status (F38, F39) and its disambiguation (F40); the Hugging Face card enters as a platform. T composes the protocol from the archive's own cards at their coarse grain, with attribution, and without the dated revisions those cards carry.",
        "T_vs_LB_reading": "v0.8 §0.5 (ruled 2026-10-08): the first diff is already ontological. What the Overview composes from the cards it surfaced shows its composition at work in its own ontology: a protocol with components and an origin, one meaning of a string among others.",
        "LB_vs_LBA": "In the archive's ontology the entity is a practice: 85 methods across nine levels, the packet one of them (Xdev-02, Xdev-03), whose success is an inscription reached by discernment (X1654-01) and, at the entity, the reading of the disambiguation (X1654-03). The field's 'permanent' (F6, F7, F17) is translated to durability bound to the retrieval substrate (Xdev-14) beside the severance its own record page carries (F8; X1538-01, Xdev-19); the April subset relation (F2, F5) is carried with its preservation (X661-02), its narrowing (Xdev-15–Xdev-17) and its contest (X1055-01); the brief's April ROI report (F18) is superseded in source (Xdev-18). Admission adds what the field does not hold: the evidentiary rule and its limits (Xdev-08–Xdev-13, Xdev-23, Xdev-24), the contest over attributing effect (X1423-01, X1609-01, X1537-01), the reception record of SPXI as data, August's displacing and enclosing spans and the trusted intermediary (X1470-01, X1470-02, X1638-01), the archive's categories for SPXI (X106-01, X670-01, X1550-01) and its relations (X1611-01, X1084-01, X193-01), and authorship as the archive states it (Xdev-21, Xdev-22). The ticker stays a separate entity sharing a grapheme sequence (X62-01, Xdev-20), with its −1× objective (X62-02); xSPI and IPX/SPX stay outside E_A, untranslated."},
       "kernel": kernel}
assert all(c in LID or c in FC for s in KO for c in s["claims"])
pw = words(P["lede"]["text"]) + sum(words(i["label"]) + words(i["text"]) for s in P["sections"] for i in s["items"])
assert pw <= 350, pw
print("P body words:", pw)
write_row(E, row, field, H / "ledger.json", H / "reading.json")
# v0.8 fields and the experimental ones, added after the shared writer
RP = V2 / "rows" / f"{E}.json"
row = json.loads(RP.read_text(encoding="utf-8"))
row["ontology"] = {
 "composition": "archive (v0.8 §0.9: the archive's reading has precedence in shaping the entity)",
 "E_F": {"type": "E (the archive's own entity: a protocol), with homonyms on the rail", "definition": "a protocol specification for the durable inscription of entities, distinguished from GEO, with components and an origin, as the archive's own surfaces at several dates describe it (B1, B2, B3, B7–B10), beside a ticker (B4) and two other protocols (B5, B6)", "claims": ["F35", "F1", "F3", "F2"]},
 "E_A": {"definition": "a technical protocol and scholarly discipline for inscribing entity-definition objects into AI-mediated retrieval systems: a practice of 85 methods across nine levels, the entity packet one of them, whose success is an inscription reached by discernment; durable to the retrieval substrate; its evidence observational, its causal efficacy open (spxi.dev, current, with #660, #1654)",
         "claims": ["Xdev-01", "Xdev-02", "Xdev-03", "X1654-01", "Xdev-14", "Xdev-12", "Xdev-13", "X660-01"], "defining_papers": [660, 1654, 62, 61, 661, 72, 670, 1638]},
 "rho": {"value": "revises", "statement": "the archive reads E_F as its own statements of the entity at several dates, the earlier served from severed hosts, and keeps, narrows or withdraws each by locus: the subset relation restated and narrowed, permanence bounded to durability, the ROI withdrawn, the Zenodo releases superseded",
         "claims": ["Xdev-15", "Xdev-14", "Xdev-18", "Xdev-19", "X661-02", "X755-01"],
         "guard": "X661-02: the amendment refines the earlier text and preserves it; ρ = revises claims the archive restated its own entity, at the loci given, and does not make the field's sources wrong at their dates. The ticker and the other protocols stand outside ρ: separate entities sharing letters (X62-01, Xdev-20)."},
 "translation": translation,
 "receiving_texts": "the field's sources are the archive's own surfaces for B1–B3 and B7–B10 and third parties for B4–B6; the received text of each field claim is its own source, quoted in the field ledger"}
row["measure"] = measure
row["negative"] = negative
row["procedure_experimental"] = procedure
RP.write_text(json.dumps(row, ensure_ascii=False, indent=1), encoding="utf-8")
print("negative check:", negative["check"]["answered"], "of", negative["check"]["of"], "| measure", measure["v0.8"])
for c in corr: print(" ", c["id"], c["check"], c["KO_sentences"], c["P_items"][:3])
