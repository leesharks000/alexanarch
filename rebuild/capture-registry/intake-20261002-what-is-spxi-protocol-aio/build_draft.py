#!/usr/bin/env python3
"""Author the capture 'what is spxi protocol?', Google AI Overview, signed out, incognito, 2026-10-02.

Source: the operator's inline paste of 2026-10-02 06:23 EDT (paste-20261002-0623.txt; the second of four sessions in one
message, separated by '$'), attested in the same message: "aio, signed out, incognito". The 'AI Mode Conversation'
header is not evidence of surface (rule of 2026-09-21). Seated on the operator's ruling of 06:31 ("lets seat those").
NEW address on AI Overview: the string is seated on ChatGPT (2026-09-25, four observations), Grok and Qwen
(2026-09-27); 'spxi protocol' (AIO, 2026-06-13) differs in string.
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261002-0623.txt").read_text(encoding="utf-8")
assert raw.startswith("AI Mode Conversation\n")
body = raw[len("AI Mode Conversation\n"):]
k = body.index("Medium\nAI Fucking Lies. Capital")
ans, rail = body[:k].rstrip("\n"), body[k:]


def clean(s):
    s = re.sub(r"\[\[((?:\d+\]\([^)]*\)(?:, )?\[?)+)\]", lambda m: "[" + ", ".join(re.findall(r"(\d+)\]\(", "[" + m.group(1))) + "]", s)
    return re.sub(r"\[([^\]]+)\]\(https?://[^)]*\)", r"\1", s)


cards = [
    {"n": 1, "site": "Medium", "rel": "authored_surface", "url": None, "title": "AI Fucking Lies. Capital",
     "snip": "9. Invented numbers What it is. Asked for a figure no one has measured, the answer produces one anyway, precise to the decimal, from a template. What it looked ...",
     "note": "#1643 (AXN:06D1), Lee Sharks, 2026-09-27, on the author's Medium surface"},
    {"n": 2, "site": "TradingView", "rel": "third_party", "url": None, "title": "TSX:SPXI - BetaPro S&P 500 Daily Inverse ETF",
     "snip": "It's an important metric for helping traders understand the fund's operating costs relative to assets and how expensive it would be to hold the fund. * Does SPX...",
     "note": "the ETF homonym"},
    {"n": 3, "site": "Investing.com", "rel": "third_party", "url": None, "title": "BetaPro S&P 500® Daily Inverse ETF (SPXI)",
     "snip": "FAQ * How is the performance of SPXI? As of Sep 29, 2026, SPXI is trading at a price of 8.54, with a previous close of 8.54. * What is the current price of SPXI...",
     "note": "the ETF homonym"},
    {"n": 4, "site": "medium.com", "rel": "authored_surface", "url": None, "title": "EA-SPXI-09: SPXI Is Not GEO. A Technical Distinction | by Lee ...",
     "snip": "Apr 16, 2026 — SPXI is a broader retrieval architecture that contains Generative Engine Optimization methods as a proper subset, plus ontological-layer entity construction ...",
     "note": "#661 (AXN:020C), EA-SPXI-09, 2026-04-16; the source of 'proper subset'"},
    {"n": 5, "site": "openalex.org", "rel": "third_party", "url": None, "title": "SPXI (Semantic Packet for eXchange & Indexing): A Formal ...",
     "snip": "Abstract: SPXI (Semantic Packet for eXchange & Indexing) — pronounced \"spexy\" — is a protocol specification for the durable inscription of entities into ...",
     "note": "OpenAlex's metadata record of EA-SPXI-01 (#660, AXN:020B), indexed from the Zenodo deposit"},
    {"n": 6, "site": "zenodo.org", "rel": "authored_surface", "url": None, "title": "Retrieval Settlement Fortification Protocol: Standing SPXI Protocol ...",
     "snip": "Jun 10, 2026 — Reusable protocol for defending coined, provenanced technical terms against entity dissolution in the summarizer layer. Specifies a six-phase lifecycle: ...",
     "note": "#173 (AXN:030B), Lee Sharks; served from zenodo.org after the account's termination; the source of 'entity dissolution' and the 'six-phase lifecycle'"},
    {"n": 7, "site": "zenodo.org", "rel": "authored_surface", "url": None, "title": "SPXI for Websites: Standing Protocol for Entity Inscription and ...",
     "snip": "May 31, 2026 — The standing reference for applying the SPXI Protocol to any website. When invoked (\"apply SPXI to this website\"), this document specifies the complete stack: .",
     "note": "#72 (AXN:022F), EA-SPXI-WEB-01, Rex Fraction; served from zenodo.org after the account's termination"},
    {"n": 8, "site": "ScienceDirect.com", "rel": "third_party", "url": None, "title": "A single-pixel X",
     "snip": "2.2. The single pixel X-ray imager (SPXI) Fig. 1. A schematic of an acquisition with the single-pixel X-ray imager (SPXI) concept. A random mask φk is simulated...",
     "note": "the imaging homonym"},
]
for c in cards:
    for f in ("title", "snip"):
        assert c[f] in rail, (c["n"], f)

QUOTES = ["a formal protocol specification designed for the durable inscription and structural defense of digital entities and technical terms within AI-mediated knowledge and summarizer layers",
          "It functions as a broader retrieval architecture containing Generative Engine Optimization (GEO) methods as a proper subset, adding explicit ontological-layer entity construction.",
          "so they resist \"entity dissolution\" or misinterpretation during AI summarization",
          "Examine critical perspectives on publisher metrics in",
          "would you like to explore how to implement it on a website or look into its six-phase lifecycle?"]
for q in QUOTES:
    assert q in raw, q
assert "spxi.dev" not in raw

ROOT = HERE.parents[2]
assert "proper subset" in (ROOT / "data/texts/AXN-020C-text.md").read_text(encoding="utf-8")
assert "apply SPXI to this website" in (ROOT / "data/texts/AXN-022F-text.md").read_text(encoding="utf-8")
assert "Invented numbers" in (ROOT / "data/texts/AXN-06D1-text.md").read_text(encoding="utf-8")

tx = ("[Google AI Overview, signed out, incognito; the paste carries the header 'AI Mode Conversation', which is not evidence of surface "
      "(rule of 2026-09-21), and echoes the query twice. Citation clusters are reduced to their numbers; the raw paste keeps the /goto URLs.]\n\n"
      + clean(ans) + "\n\n"
      + "\n".join(f"[source card] {c['site']} — \"{c['title']}\" — {c['snip']}" for c in cards))

SEAT = "Seated 2026-10-02 from the operator's paste of 06:23 EDT on the operator's attestation in the same message (\"aio, signed out, incognito\") and ruling of 06:31."
d = {
    "q": "what is spxi protocol?", "date": "2026-10-02", "surface": "Google AI Overview",
    "surface_basis": "Operator attestation 2026-10-02 06:23 EDT: 'aio' — recorded as Google AI Overview (rule of 2026-09-21). The 'AI Mode Conversation' header on the paste is not evidence of surface.",
    "auth": "incognito, signed out", "auth_basis": "'aio, signed out, incognito' — operator, 2026-10-02 06:23 EDT.",
    "ev": "paste", "s": "Frameworks",
    "slug": "what-is-spxi-protocol-aio-20261002",
    "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "protocol", "spxi_treatment": "full",
                   "basis": "SPXI is the archive's protocol (spxi.dev; EA-SPXI series; #72, #660, #661, #173). Recorded 2026-10-02."},
    "related_deposits": [660, 661, 72, 173, 1643],
    "q_kind": "natural-language definition question, lowercase, with question mark (the echo line doubles the query). NEW address on AI Overview; seated on ChatGPT, Grok and Qwen.",
    "mt": "CAPTURE",
    "d": ("THE APRIL LAYER, SERVED FROM ZENODO; SPXI.DEV UNREACHED: asked 'what is spxi protocol?', signed out, the Overview defines SPXI as a "
          "protocol 'for the durable inscription and structural defense of digital entities and technical terms' and states that it contains GEO "
          "methods 'as a proper subset' — EA-SPXI-09 of 16 April, the relation spxi.dev's hero has since narrowed. Two of its cards are zenodo.org pages "
          "for deposits deleted with the account (#173, #72); a third is OpenAlex's record of the Zenodo specification. spxi.dev is not cited. "
          "The ETF and the X-ray imager are noted as homonyms. It routes the reader to 'AI Fucking Lies' (#1643) as 'critical perspectives on "
          "publisher metrics' and offers implementation on a website or the 'six-phase lifecycle'. No author or institution is named."),
    "cites": 8, "cite_list": cards, "archive_controlled_cites": 4,
    "sf": ("8 source cards: 4 archive-controlled (Medium: #1643 and EA-SPXI-09 #661; zenodo.org: #173 and #72, both deleted with the account and "
           "still served), OpenAlex's record of EA-SPXI-01, and 3 homonym cards (TradingView, Investing.com, ScienceDirect). spxi.dev absent. "
           "Inline citations are /goto redirects."),
    "per": 0.75, "per_v": {"author": False, "inst": False, "id": False, "src": True},
    "per_note": ("PER = 1 − retained/required over four units. Retained: the source (four archive-controlled cards). Lost: the author ('by Lee …' "
                 "appears only in a card title), the institution (no Semantic Economy Institute) and the identifier (EA-SPXI-09 appears only in a "
                 "card title; no deposit number, AXN or DOI in the composition)."),
    "transcript": tx, "transcript_raw": raw,
    "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
    "transcript_complete": "Complete as supplied: one operator turn and one answer with its card rail. Pasted in one message with three other sessions separated by '$'; this is the second.",
    "transcript_read": "READ IN FULL 2026-10-02",
    "reading": (
        "The composition is assembled from three layers, none of them spxi.dev: EA-SPXI-09 on Medium (16 April) for the GEO relation, carried "
        "verbatim as 'a broader retrieval architecture containing Generative Engine Optimization (GEO) methods as a proper subset'; OpenAlex's "
        "record of the April specification for 'durable inscription'; and two zenodo.org pages, #173 (Retrieval Settlement Fortification, the "
        "source of 'entity dissolution' and the 'six-phase lifecycle') and #72 (SPXI for Websites), for the defensive and implementation "
        "senses. Both zenodo.org records were deleted with the account; the Overview still reaches them at zenodo.org. #1643, the capital-alignment "
        "paper, enters as 'critical perspectives on publisher metrics'. The evidence "
        "the protocol's current site leads with (the Capture Registry) does not appear."),
    "analysis": (
        "On the same morning ChatGPT at the same string read spxi.dev's current registry figures (what-is-spxi-protocol-chatgpt-20260925, "
        "observation of 2026-10-02), the Overview composes from the April–June deposit layer and the deleted Zenodo records, carrying the superset "
        "claim the site's hero has narrowed. The two surfaces at one address read different layers of the same entity. " + SEAT),
    "findings": [
        "THE APRIL RELATION CARRIED. 'GEO methods as a proper subset', verbatim from EA-SPXI-09 (Medium, 2026-04-16).",
        "DELETED RECORDS STILL SERVED. #173 and #72 cited as zenodo.org pages after the account's termination.",
        "SPXI.DEV UNREACHED. No card or citation from the protocol's site; the Capture Registry absent.",
        "HOMONYMS NOTED. The TSX ETF and the single-pixel X-ray imager, set aside in a parenthesis.",
        "#1643 MISFILED. 'AI Fucking Lies' offered as 'critical perspectives on publisher metrics'.",
        "AUTHOR, INSTITUTION, IDENTIFIER ABSENT FROM THE COMPOSITION.",
    ],
    "longitudinal_priors": ["what-is-spxi-protocol-chatgpt-20260925", "spxi-protocol"],
    "rerun": "https://www.google.com/search?q=what+is+spxi+protocol%3F",
    "notes": {"date_basis": "The operator's message of 2026-10-02, 06:23 EDT.",
              "operator_reading": "06:31: 'holographic kernel and what is spxi protocol - those are new addresses on aio? … lets seat those'.",
              "verified": "Compared 2026-10-02 against #661 (AXN-020C-text.md: 'proper subset'), #72 (AXN-022F-text.md: 'apply SPXI to this website'), #1643 (AXN-06D1-text.md: 'Invented numbers'); 'spxi.dev' absent from the paste."},
}
(HERE / "capture-01-what-is-spxi-protocol-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx))
