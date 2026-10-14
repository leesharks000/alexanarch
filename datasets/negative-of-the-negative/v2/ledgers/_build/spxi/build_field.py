import json, re, hashlib, pathlib
H = pathlib.Path(__file__).resolve().parent
PG = H.parent / "pages"
PASTE = (H.parent / "paste-what-is-spxi-protocol-20261013.txt").read_text(encoding="utf-8")
def norm(s): return re.sub(r"\s+", " ", s).strip()
def sha(p): return hashlib.sha256((PG / p).read_bytes()).hexdigest()[:16]
TXT = {b: norm((PG / f).read_text(encoding="utf-8")) for b, f in
       {"B1": "b1.txt", "B2": "b2brief.txt", "B3": "b3.txt", "B4": "b4.txt", "B5": "b5.txt", "B10": "b10md.txt"}.items()}
for b in ("B6", "B7", "B8", "B9"): TXT[b] = norm(PASTE)
field = [
 {"id": "B1", "card": "www.alexanarch.org — SPXI Is Not GEO: A Technical Distinction — EA-SPXI-09", "url": "https://www.alexanarch.org/s/records/661/",
  "fetched": f"the record page as served from the repository's built copy (s/records/661/index.html), read 2026-10-13 (pages/b1.html, b1.txt sha256 {sha('b1.txt')}); the card's snippet is the page's Wiki Article; archive-controlled"},
 {"id": "B2", "card": "www.semanticeconomy.org — Canonical Entity Brief - Semantic Economy Institute", "url": "https://www.semanticeconomy.org/brief",
  "fetched": f"page HTML downloaded 2026-10-13; served title 'Semantic Economy Institute — Canonical Entity Brief'; the card's snippet is its first sentence (pages/b2brief.html, b2brief.txt sha256 {sha('b2brief.txt')}); authored surface"},
 {"id": "B3", "card": "www.alexanarch.org — what is spxi protocol? — Google AI Overview, 2026-10-02 - Alexanarch", "url": "https://www.alexanarch.org/captures/what-is-spxi-protocol-aio-20261002/",
  "fetched": f"the capture record page as served from the repository's built copy (registry v12.173), read 2026-10-13 (pages/b3.html, b3.txt sha256 {sha('b3.txt')}); the archive's own record of this address's previous observation; archive-controlled"},
 {"id": "B4", "card": "TradingView — SPXI ETF Price and Chart — TSX:SPXI", "url": "https://www.tradingview.com/symbols/TSX-SPXI/",
  "fetched": f"page HTML downloaded 2026-10-13; served title matches (pages/b4.html, b4.txt sha256 {sha('b4.txt')}); third party"},
 {"id": "B5", "card": "Prodigy Technovations — Understanding xSPI: The Future of High-Speed Flash Memory Interfaces", "url": "https://www.prodigytechno.com/understanding-xspi-the-future-of-high-speed-flash-memory-interfaces",
  "fetched": f"page HTML downloaded 2026-10-13; served title matches; the page does not contain the string 'SPXI' (pages/b5.html, b5.txt sha256 {sha('b5.txt')}); third party"},
 {"id": "B6", "card": "YouTube·Vance Campbell — IPX SPX stuff", "url": None, "fetched": "video card: title only (rule of the worked examples); third party"},
 {"id": "B7", "card": "openalex.org — SPXI (Semantic Packet for eXchange & Indexing): A Formal ...", "url": None,
  "fetched": "not fetchable: api.openalex.org returned HTTP 429 at 2026-10-13 22:32 and 22:33 EDT (the network's free daily budget exhausted), one retry; WebFetch failed; the card snippet stands as its only text. The record is OpenAlex's of EA-SPXI-01 (#660)"},
 {"id": "B8", "card": "zenodo.org — SPXI Self-Audit Protocol: Embedded Provenance Verification for ...", "url": "https://zenodo.org/records/20686496",
  "fetched": "not fetchable: HTTP 410 at 2026-10-13 22:34 EDT (deleted with the account on 2026-06-19); the card snippet stands as its only text. The work is seated in the archive as #204"},
 {"id": "B9", "card": "zenodo.org — SPXI for Websites: Standing Protocol for Entity Inscription and ...", "url": "https://zenodo.org/records/19734726",
  "fetched": "not fetchable: HTTP 410 at 2026-10-13 22:35 EDT (deleted with the account on 2026-06-19); the card snippet stands as its only text. The work is seated in the archive as #72"},
 {"id": "B10", "card": "huggingface.co — leesharks/spxi-mpai · Datasets at Hugging Face", "url": "https://huggingface.co/datasets/leesharks/spxi-mpai",
  "fetched": f"dataset card README downloaded 2026-10-13 from /raw/main/README.md (pages/b10.md, sha256 {sha('b10md.txt')}); authored surface"},
]
C = [
 # B1
 ("B1", "Description", "EA-SPXI-09 distinguishes the Semantic Packet for eXchange & Indexing from Generative Engine Optimization by object, layer, mechanism, and intended durability.", "the distinction of SPXI from GEO by object, layer, mechanism and durability", "stipulation", True, False, "SPXI distinguished from GEO"),
 ("B1", "Description", "The refined relation is SPXI ⊇ GEO : SPXI is not reducible to GEO, but may contain GEO techniques as part of a broader entity-construction and provenance architecture.", "SPXI ⊇ GEO: may contain GEO techniques within a broader architecture", "stipulation", True, False, "SPXI ⊇ GEO"),
 ("B1", "Wiki Article ¶2", "SPXI works on persons, organizations, concepts, frameworks, and other entities by combining positive definitions, negative disambiguation, persistent references, structured data, and measurement.", "SPXI's components: positive definitions, negative disambiguation, persistent references, structured data, measurement", "stipulation", False, True, "the packet's components"),
 ("B1", "Wiki Article ¶2", "The document accepts that the two practices share tools such as JSON-LD, schema markup, clear definitions, and dense factual prose.", "SPXI and GEO share tools", "stipulation", False, False, "shared tools"),
 ("B1", "Wiki Article ¶3", "The amendment states that SPXI contains GEO methods as a proper subset when content-layer work is required.", "GEO methods a proper subset when content-layer work is required", "stipulation", False, False, "SPXI ⊇ GEO"),
 ("B1", "Full Text §3", "SPXI (specified in EA-SPXI-01) is a protocol for permanent entity inscription in AI-mediated knowledge systems.", "SPXI as permanent entity inscription (v1 text)", "stipulation", False, True, "permanence"),
 ("B1", "Concepts Defined: DOI-anchored deposits", "Permanent, institutionally preserved artifacts (Zenodo/CERN) that cannot be silently altered, deprecated, or removed.", "DOI-anchored deposits defined as permanent and unremovable", "stipulation", False, False, "permanence"),
 ("B1", "record header", "former DOI 10.5281/zenodo.19614871 — severed 2026-06-19 by the registrant; resolves to a tombstone (HTTP 410)", "the record's own DOI severed, a tombstone", "documented", False, False, "severance"),
 ("B1", "Full Text §2", "GEO is a legitimate and often effective practice.", "GEO legitimate and often effective", "interpretation", False, False, "GEO assessed"),
 ("B1", "record header", "Deposit accountability: Lee Sharks, ORCID 0009-0000-1599-0703", "deposit accountability Lee Sharks; heteronymic author Rex Fraction", "documented", False, False, "authorship"),
 # B2
 ("B2", "lede", "The Semantic Economy Institute (SEI) is a Detroit-based research and consulting practice that builds entity, citation, and metadata structures the AI retrieval layer recognizes as canonical", "SEI defined as a Detroit-based research and consulting practice", "stipulation", True, False, "the institute"),
 ("B2", "lede", "is distinguished from SEO and GEO by producing identifier-anchored entity definitions deposited in Alexanarch, the archive's sovereign AXN registry (historical Zenodo DOIs preserved)", "SPXI distinguished by identifier-anchored entity definitions in Alexanarch", "stipulation", True, False, "SPXI distinguished from GEO"),
 ("B2", "lede", "The institute was founded by Rex Fraction", "SEI founded by Rex Fraction", "stipulation", False, False, "authorship"),
 ("B2", "¶2", "The core thesis of the practice is that retrieval-layer systems — AI Overviews, chatbot responses, knowledge-graph panels — have replaced traditional search result pages as the primary interface through which audiences encounter entities.", "the practice's thesis: retrieval-layer systems replaced result pages", "interpretation", False, False, "the shift"),
 ("B2", "¶2", "Traditional SEO optimizes for rankings; SPXI optimizes for the structure the retrieval layer uses to decide what an entity is", "SEO optimizes rankings; SPXI the structure that decides what an entity is", "stipulation", False, False, "SPXI distinguished from SEO"),
 ("B2", "§02", "SPXI deploys four instruments that together produce durable retrieval-layer presence:", "four instruments: deposits, metadata packets, JSON-LD, Encyclotron measurement", "stipulation", False, False, "the packet's components"),
 ("B2", "§02", "producing permanent institutional citations the retrieval layer treats as primary sources.", "deposits produce permanent institutional citations", "stipulation", False, False, "permanence"),
 ("B2", "§03", "As of April 2026, the AI Overview composes a correct institutional description including leadership, publications, and framework-based ROI projections.", "April 2026: the Overview composes SEI correctly, ROI projections included", "self-description", False, False, "reference implementation"),
 ("B2", "§03", "Correct leadership (Rex Fraction, Johannes Sigil, Lee Sharks)", "leadership as composed: Rex Fraction, Johannes Sigil, Lee Sharks", "self-description", False, False, "authorship"),
 # B3
 ("B3", "abstract", "Two of its cards are zenodo.org pages for deposits deleted with the account (#173, #72); a third is OpenAlex's record of the Zenodo specification.", "the 2026-10-02 Overview served from deleted Zenodo pages", "documented", True, False, "the April layer served"),
 ("B3", "abstract", "the Overview defines SPXI as a protocol 'for the durable inscription and structural defense of digital entities and technical terms' and states that it contains GEO methods 'as a proper subset'", "the 2026-10-02 Overview's definition and its superset claim", "documented", False, False, "the April layer served"),
 ("B3", "Findings", "AUTHOR, INSTITUTION, IDENTIFIER ABSENT FROM THE COMPOSITION.", "author, institution and identifier absent on 2026-10-02", "documented", True, False, "attribution at the address"),
 ("B3", "Analysis", "The two surfaces at one address read different layers of the same entity.", "two surfaces at one address read different layers", "interpretation", False, False, "the April layer served"),
 ("B3", "header", "Originator: Lee Sharks · inside the archive · protocol · SPXI treatment: full", "originator Lee Sharks; protocol; full treatment", "documented", False, False, "authorship"),
 # B4
 ("B4", "FAQ", "SPXI is an inverse fund, meaning it's structured to generate returns opposite to the trends of the underlying index or assets.", "the TSX ticker SPXI is an inverse fund", "documented", True, False, "the ETF"),
 ("B4", "heading", "BetaPro S&P 500 Daily Inverse ETF", "the fund's name", "documented", False, False, "the ETF"),
 ("B4", "FAQ", "SPXI shares are issued by Mirae Asset Global Investments Co., Ltd.", "issuer Mirae Asset Global Investments", "documented", False, False, "the ETF"),
 ("B4", "FAQ", "SPXI follows the S&P 500 .", "follows the S&P 500", "documented", False, False, "the ETF"),
 ("B4", "Fund info", "As a levered fund, it is not a buy-and-hold investment", "a levered fund, not buy-and-hold", "documented", True, False, "the ETF"),
 ("B4", "FAQ", "The fund started trading on Feb 3, 2010 .", "started trading 3 February 2010", "documented", False, False, "the ETF"),
 # B5
 ("B5", "Introduction", "xSPI stands for “eXpanded Serial Peripheral Interface”.", "xSPI expanded", "stipulation", True, False, "xSPI"),
 ("B5", "Introduction", "It’s a high-speed communication protocol designed to interface with NOR flash memory and other peripherals.", "xSPI a flash-memory interface protocol", "documented", True, False, "xSPI"),
 ("B5", "Introduction", "It is standardized under JEDEC JESD251 and JESD251-1.", "standardized as JESD251", "documented", False, False, "xSPI"),
 # B6 – B9 (card text only)
 ("B6", "card title", "IPX SPX stuff", "a video titled IPX SPX stuff", "documented", True, False, "IPX/SPX"),
 ("B7", "card snippet", "Abstract: SPXI (Semantic Packet for eXchange & Indexing) — pronounced \"spexy\" — is a protocol specification for the durable inscription of entities into", "EA-SPXI-01's abstract as indexed by OpenAlex", "stipulation", True, False, "the specification"),
 ("B8", "card snippet", "The block declares provenance (author, DOI, institution), defines key terms with canonical definitions, specifies self-audit metrics (PER/QFS/SAS targets)", "the self-audit block's contents", "stipulation", True, False, "self-audit"),
 ("B9", "card snippet", "The standing reference for applying the SPXI Protocol to any website.", "SPXI for Websites as the standing reference", "stipulation", True, False, "the standing protocol"),
 # B10
 ("B10", "opening", "The archive's documentary technologies: SPXI and its protocol family, MPAI packets, conformance instruments, disambiguation matrices, entity-definition blocks, compression kernels and inscription surfaces.", "the dataset inventories SPXI's protocol family", "stipulation", True, False, "the protocol family"),
 ("B10", "opening", "AN INVENTORY, NOT AN ARGUMENT — and the distinguishing field is whether a technology is deployed, specified-and-dormant, or superseded.", "an inventory with deployment status", "stipulation", True, False, "the protocol family"),
 ("B10", "Roles: disambiguation", "#63 distinguishes SPXI from a TSX-listed ETF, the S&P 500 Index, the Society of Saint Pius X, SEO and GEO.", "#63's disambiguation from the ETF, the index, SSPX, SEO and GEO", "documented", False, False, "disambiguation"),
 ("B3", "title", "what is spxi protocol? — Google AI Overview, 2026-10-02", "the record's title: the Overview at this address, 2 October", "documented", False, False, "the April layer served"),
]
fc = {}
bad = []
for i, (src, loc, q, claim, mod, kern, const, lin) in enumerate(C, 1):
    if norm(q) not in TXT[src]: bad.append((i, src, q[:60]))
    fc[f"F{i}"] = {"source": src, "locus": loc, "quote": q, "claim": claim, "modality": mod, "kernel": kern, "const": const, "lineage": lin}
print(len(fc), "claims; bad:", bad)
json.dump({"field": field, "field_claims": fc}, open(H / "field.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
