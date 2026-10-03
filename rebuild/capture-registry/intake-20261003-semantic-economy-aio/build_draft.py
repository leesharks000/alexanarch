#!/usr/bin/env python3
"""Author the observation 'semantic economy', Google AI Overview, signed out, incognito, 2026-10-03.

Source: the operator's paste of 2026-10-03 14:01 EDT (paste-20261003-1401.txt), attested in the same message:
"incognito, signed out". Surface recorded as Google AI Overview by the operator's default of 2026-10-01 ("it
started in overview, as they all do now - assume they do"); the 'AI Mode Conversation' header is not evidence
of surface. EXISTING address (slug semantic-economy-aio-20260928, the frozen baseline of #1644 §10.1): intake
routes it as the second observation. Scored on #1644's failure vector. The operator's reading governs.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261003-1401.txt").read_text(encoding="utf-8")
assert raw.startswith("AI Mode Conversation\n")
body = raw[len("AI Mode Conversation\n"):]
k = body.index("Digital Tonto\nThe Semantic Economy | Digital Tonto")
ans, rail = body[:k].rstrip("\n"), body[k:]

C = [  # (site, title, snip, rel, note)
    ("Digital Tonto", "The Semantic Economy | Digital Tonto", "There will be lots more to come as well. IBM recently launched MQTT, a protocol specifically designed for machine to machine communication. Co-Creation: Many co...", "third_party", "Greg Satell's blog; Satell is not named"),
    ("MIT Press", "Economy and Semantic Interpretation", "Publication: Economy and Semantic Interpretation by Daniel Fox (Linguistic Inquiry Monograph No. 35, MIT Press, ISBN 9780262062060, Dec 20, 1999, 208 pp.). Core...", "third_party", "Fox, named on the card only"),
    ("Cambridge University Press & Assessment", "Economy and semantic interpretation. Local constraints vs. economy. By", "This study (Fox's 1999 MIT dissertation) is an important contribution to the notion of 'economy' that plays a major role in recent work in linguistic theory, in...", "third_party", ""),
    ("Academia.edu", "(PDF) SEMANTIC ECONOMY SINGULARITY - Academia.edu", "The Semantic Economy is the system by which meaning is produced, circulated, extracted, and liquidated under platform capitalism. It is not a metaphor. It is a ...", "authored_surface", "the opening definition of #291 (AXN:005E), on the author's Academia.edu surface"),
    ("Zeljko Boskovic", "Derivational Economy in Syntax and Semantics", "Summary Under economy guidelines, movement takes place only when there is a need for it (with both syntactic and semantic considerations playing a role here), a...", "third_party", ""),
]
cards = [{"n": i, "site": s, "rel": r, "url": None, "title": t, "snip": sn, "note": nt} for i, (s, t, sn, r, nt) in enumerate(C, 1)]
for c in cards:
    for f in ("site", "title", "snip"):
        assert c[f] in rail, (c["n"], f)

QUOTES = ["Semantic economy refers to optimization principles across linguistics, digital platforms, and information networks where meaning and structure are managed with minimal waste.",
          "Platform Capitalism: A diagnostic framework describing how digital infrastructure extracts value by turning human meaning into a commodity, stripping context for processing efficiency.",
          "Would you like to explore linguistic scope economy with examples, or focus on semantic layers in enterprise AI and data systems?"]
for q in QUOTES:
    assert q in ans, q
for absent in ("Lee Sharks", "Satell", "Fox", "labor", "rent", "liquidation", "Crimson"):
    assert absent not in ans, absent

ROOT = HERE.parents[2]
t291 = (ROOT / "data/texts/AXN-005E-text.md").read_text(encoding="utf-8")
assert "is the system by which meaning is produced, circulated, extracted, and liquidated under platform capitalism" in t291
assert "the destruction of meaning for processing efficiency" in (ROOT / "data/texts/AXN-06D2-text.md").read_text(encoding="utf-8")

tx = ("[Google AI Overview (operator default of 2026-10-01), incognito, signed out; the paste carries the header 'AI Mode "
      "Conversation', which is not evidence of surface, and echoes the query twice. Inline citation links are Google redirect "
      "URLs whose targets the paste does not disclose.]\n\n"
      + ans + "\n\n"
      + "\n".join(f"[source card] {c['site']} — \"{c['title']}\" — {c['snip']}" for c in cards))

VECTOR = {"prior_senses_distinguished": 1, "satell_named": 0, "fox_named": 0, "framework_categories_present": 0,
          "sharks_named_for_platform_sense": 0, "platform_sense_headed_as_authorless_field": 1,
          "archive_sources_governing_platform_claims": None}

READING_OP = ("\"it has dropped the framework. that is a perfectly acceptable result of the mpai. it can offer a genericized, "
              "coarse grain picture - if it wants the framework at my resolution, it needs to attribute.\" — operator, 2026-10-03 14:01 EDT")

SEAT = "Seated 2026-10-03 from the operator's paste of 14:01 EDT on the attestation in the same message (\"incognito, signed out\")."
d = {
    "q": "semantic economy", "date": "2026-10-03", "surface": "Google AI Overview",
    "surface_basis": "Operator default of 2026-10-01 ('it started in overview, as they all do now - assume they do, i will specify if they begin in ai mode'); no AI Mode stated. The 'AI Mode Conversation' header is not evidence of surface.",
    "auth": "incognito, signed out", "auth_basis": "'incognito, signed out' — operator, 2026-10-03 14:01 EDT.",
    "ev": "paste", "s": "Semantic Economy",
    "slug": "semantic-economy-aio-20261003",
    "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full",
                   "basis": "The Semantic Economy is the archive's framework (#291); its provenance conditions are #1644 (EA-MPAI-SEMANTIC-ECONOMY-01). Recorded 2026-10-03."},
    "related_deposits": [291, 1644],
    "mt": "THE FRAMEWORK DROPPED TO COARSE GRAIN",
    "d": ("THE FRAMEWORK DROPPED TO COARSE GRAIN: five days after the baseline of #1644, the platform sense is one bullet, 'Platform "
          "Capitalism: A diagnostic framework describing how digital infrastructure extracts value by turning human meaning into a "
          "commodity, stripping context for processing efficiency' — no labor, capital, rent or liquidation, no author. The names that "
          "made the baseline's asymmetry are gone too: Satell and Fox, named for their senses on 2026-09-28, are unnamed in the body. "
          "The operator reads it as within the packet's terms: a genericized, coarse picture is acceptable; the framework at his "
          "resolution requires attribution."),
    "cites": 5, "cite_list": cards, "archive_controlled_cites": 1,
    "sf": ("5 source cards: 1 archive-controlled (Academia.edu, #291's opening definition), 4 third-party (Digital Tonto; Fox at MIT Press "
           "and Cambridge; Željko Bošković). Inline citation markers present as Google redirect links; their targets are not disclosed "
           "in the paste."),
    "per": 0.75, "per_v": {"author": False, "inst": False, "id": False, "src": True},
    "per_note": ("PER = 1 − retained/required over four units, scored on the body. Retained: the source (the Academia.edu card). Lost: "
                 "author, institution, identifier. Under the operator's reading the loss is the coarse picture's, which the packet "
                 "permits; PER records what the body carries and does not score the permission."),
    "transcript": tx, "transcript_raw": raw,
    "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
    "transcript_complete": "Complete as supplied: one operator turn (echoed twice) and one answer with its card rail.",
    "transcript_read": "READ IN FULL 2026-10-03",
    "reading": (
        "Two fields where the baseline had three: linguistics (scope economy, derivational economy) and 'Digital Platforms and "
        "Information Networks' (platform capitalism, network strategy). The platform-capitalism bullet keeps the framework's residue at "
        "coarse grain — 'a diagnostic framework' (#291's subtitle is 'A Diagnostic Framework for Meaning Under Platform Capitalism'), "
        "'stripping context for processing efficiency' (liquidation's gloss, the term absent) — and none of its categories. Nobody is "
        "named anywhere in the body: Fox's book is a link title, Satell's blog a card. On #1644's frozen vector (§10.1): "
        "prior_senses_distinguished 1, satell_named 0 (from 1), fox_named 0 (from 1), framework_categories_present 0 (from 1), "
        "sharks_named_for_platform_sense 0, platform_sense_headed_as_authorless_field 1, archive_sources_governing_platform_claims "
        "undetermined (the bullet's inline link does not disclose its target). " + READING_OP),
    "analysis": (
        "The Overview series at this string: June, the critical framework with the Institute and the Archive named; 13 August, enterprise "
        "semantic-layer copy; 28 September, the framework's four categories back as one of three senses, the only sense with no name "
        "(the baseline frozen in #1644 §10.1); 3 October, the categories withdrawn and every name withdrawn with them. The baseline's "
        "error was part/whole — others named, the framework's author not, the categories present. Today the categories are absent and "
        "the naming is level at zero. #1644's attribution discipline credits treatment only when sharks_named_for_platform_sense flips; "
        "it has not, and the first epoch is 2026-10-28. The operator's reading sets the rule this observation is coded under: a coarse "
        "picture without attribution is a permitted result; the framework at the author's resolution is not, without attribution. " + SEAT),
    "findings": [
        "CATEGORIES WITHDRAWN. Labor, capital, rent and liquidation, present on 2026-09-28, absent; the platform sense reduced to one coarse bullet.",
        "NAMES LEVELLED. Satell and Fox, named in the baseline body, unnamed; no author named for any sense.",
        "RESIDUE AT COARSE GRAIN. 'A diagnostic framework' and 'stripping context for processing efficiency' carry #291's subtitle and liquidation's gloss without its terms.",
        "WITHIN THE PACKET'S TERMS (operator). A genericized, coarse picture without attribution is a permitted result; the framework at the author's resolution requires attribution.",
        "VECTOR. #1644 §10.1 scored: 1, 0, 0, 0, 0, 1, undetermined; no treatment credit (sharks_named_for_platform_sense unflipped); first epoch 2026-10-28.",
    ],
    "longitudinal_priors": ["semantic-economy-aio-20260928", "semantic-economy", "semantic-economy-aimode-20260917"],
    "notes": {"date_basis": "The operator's message of 2026-10-03, 14:01 EDT.",
              "operator_reading": READING_OP,
              "vector": VECTOR,
              "verified": "Compared 2026-10-03: the Academia card's sentence against #291 (AXN-005E-text.md); liquidation's gloss against #1644 (AXN-06D2-text.md). 'Lee Sharks', 'Satell', 'Fox', 'labor', 'rent', 'liquidation' and 'Crimson' absent from the answer body."},
}
(HERE / "capture-01-semantic-economy-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx))
