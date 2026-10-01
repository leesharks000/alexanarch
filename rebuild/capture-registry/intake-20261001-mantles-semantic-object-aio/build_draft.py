#!/usr/bin/env python3
"""Author the capture 'mantles as semantic object', Google AI Overview, signed out, incognito, 2026-10-01.

Source: the operator's inline paste of 2026-10-01 14:39 EDT (paste-20261001-1439.txt), prefixed in the same message by
"logged out. incognito." (attestation, not transcript). Surface by operator attestation of 16:41 EDT: "it started in
overview, as they all do now - assume they do, i will specify if they begin in ai mode. incognito. signed out." The
paste carries the copy header 'AI Mode Conversation', which is not evidence of surface (rule of 2026-09-21), and echoes
the query twice. The paste was recovered verbatim from the chat record after the session file was compacted. The date
is the day of the operator's message; no other date was stated.
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261001-1439.txt").read_text(encoding="utf-8")
assert raw.startswith("AI Mode Conversation\n")
body = raw[len("AI Mode Conversation\n"):]
k = body.index("Medium\nThe Crimson Hexagon: Operative Architecture | by Lee Sharks")
ans, rail = body[:k].rstrip("\n"), body[k:]


def clean(s):
    s = re.sub(r"\[\[((?:\d+\]\([^)]*\)(?:, )?\[?)+)\]", lambda m: "[" + ", ".join(re.findall(r"(\d+)\]\(", "[" + m.group(1))) + "]", s)
    return re.sub(r"\[([^\]]+)\]\(https?://[^)]*\)", r"\1", s)


cards = [
    {"n": 1, "site": "Medium", "rel": "authored_surface", "url": None,
     "title": "The Crimson Hexagon: Operative Architecture | by Lee Sharks",
     "snip": "Get Lee Sharks's stories in your inbox The Hexagon does not treat persona as mere pseudonym. It distinguishes between masks (temporary, situational), brands (ma...",
     "note": "the author's Medium surface for #27 (AXN:0170, EA-HEXAGON-COMPRESSION-01); the source of every citation in §2"},
    {"n": 2, "site": "YouTube·Coding Calling", "rel": "third_party", "url": None,
     "title": "PART 4 - SAP Fiori App Configuration | Catalog, Groups, Target Mapping ...", "snip": "2m", "note": "the SAP Fiori sense"},
    {"n": 3, "site": "Innovatily", "rel": "third_party", "url": None,
     "title": "The Mantle — Innovatily",
     "snip": "A Mantle names the real objects a business runs on and how they relate — the same handful of categories, whatever the industry: * 01 Entities The nouns: dealer,",
     "note": None},
    {"n": 4, "site": "mantleai.dev", "rel": "third_party", "url": None,
     "title": "Semantic Knowledge Graph",
     "snip": "Understanding Your Data Enterprise data is full of references to the same entities, people, companies, products, transactions, but each system uses different id...",
     "note": "the source of §1 (entity resolution)"},
    {"n": 5, "site": "YouTube·AtScale", "rel": "third_party", "url": None,
     "title": "Understanding Semantic Layers in AI: Why Context is Essential for Data Access", "snip": "31m", "note": None},
    {"n": 6, "site": "YouTube·Biztory", "rel": "third_party", "url": None,
     "title": "Webinar | The Semantic Layer in the AI Data Stack - Biztory", "snip": "35:50", "note": None},
    {"n": 7, "site": "mantleai.dev", "rel": "third_party", "url": None,
     "title": "Why we built mantle",
     "snip": "Mantle is the context layer for AI agents, connecting data, resolving entities, and serving quality-scored context to any agent through a single API. * mantle i...",
     "note": None},
]
for c in cards:
    for f in ("title", "snip"):
        assert c[f] in rail, (c["n"], f)
arch = sum(1 for c in cards if c["rel"] == "authored_surface")

QUOTES = ["a \"mantle\" is defined as a specific type of cryptographic and semantic object",
          "a publicly verifiable chain of ownership (such as a blockchain or ledger receipt)",
          "it requires real resource expenditure or reputational risk to inhabit, separating true semantic identity from superficial \"cosplay\" or bot behavior",
          "This philosophy differentiates temporary \"masks,\" monetizable \"brands,\" and arbitrary \"usernames\" from mantles.",
          "To give you the most relevant information, could you clarify which domain you are exploring?"]
for q in QUOTES:
    assert q in raw, q

# #27 as deposited (data/texts/AXN-0170-text.md), verified 2026-10-01
SRC = pathlib.Path(__file__).resolve().parents[3] / "data/texts/AXN-0170-text.md"
src = SRC.read_text(encoding="utf-8")
for s in ["semantic objects with their own provenance, operations, criteria of inhabitation, and public verification chain",
          "**Integrity Lock.** The mantle must be linked to publicly stable receipts: deposits, DOIs, cross-references, provenance chains.",
          "**Bearing-Cost Linkage.** The mantle must be tethered to real expenditure. A mantle without cost is cosplay.",
          "**Dignity Condition.**", "**Operational Specificity.**"]:
    assert s in src, s
assert not re.search(r"blockchain|cryptograph|\bbots?\b|ownership", src, re.I)

tx = ("[Google AI Overview, signed out, incognito; the paste carries the header 'AI Mode Conversation', which is not evidence of surface "
      "(rule of 2026-09-21), and echoes the query twice. Citation clusters are reduced to their numbers; the raw paste keeps the /goto URLs.]\n\n"
      + clean(ans) + "\n\n"
      + "\n".join(f"[source card] {c['site']} — \"{c['title']}\" — {c['snip']}" for c in cards))

SEAT = ("Seated 2026-10-01 from the operator's paste of 14:39 EDT on the operator's attestation (\"logged out. incognito.\", 14:39; "
        "\"it started in overview\", 16:41).")
d = {
    "q": "mantles as semantic object", "date": "2026-10-01", "surface": "Google AI Overview",
    "surface_basis": "Operator attestation 2026-10-01 16:41 EDT: 'it started in overview, as they all do now - assume they do, i will specify if they begin in ai mode.' Recorded as Google AI Overview (rule of 2026-09-21). The 'AI Mode Conversation' header on the paste is not evidence of surface.",
    "auth": "incognito, signed out", "auth_basis": "'logged out. incognito.' — operator, 2026-10-01 14:39 EDT; restated 16:41 ('incognito. signed out.').",
    "ev": "paste", "s": "Machine Reception",
    "slug": "mantles-as-semantic-object-aio-20261001",
    "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "partial",
                   "basis": "The mantle as semantic object, with its necessary conditions, is the archive's (#27 §'Mantles'; the mantle line #1651–#1656). Recorded 2026-10-01."},
    "related_deposits": [27, 1651, 1652, 1653, 1654, 1655, 1656],
    "q_kind": "four bare words, unquoted (operator paste 2026-10-01; the echo line doubles the query). NEW address.",
    "mt": "CAPTURE",
    "d": ("THE MANTLE GIVEN A BLOCKCHAIN AND AN OWNER: asked 'mantles as semantic object', signed out, the Overview offers three senses — "
          "an enterprise semantic layer (Mantle AI), the archive's mantle, and SAP Fiori's semantic objects — and asks which is meant. The "
          "archive's sense is cited wholly to #27 on the author's Medium surface and carries its distinction of masks, brands and usernames "
          "from mantles and two of its four necessary conditions. It adds what #27 does not say: the mantle becomes 'a specific type of "
          "cryptographic and semantic object'; 'public verification chain' becomes 'a publicly verifiable chain of ownership (such as a "
          "blockchain or ledger receipt)'; 'A mantle without cost is cosplay' becomes 'cosplay or bot behavior'."),
    "cites": 7, "cite_list": cards, "archive_controlled_cites": arch,
    "sf": ("7 source cards: one archive-controlled (#27 on Medium, 'by Lee Sharks'), six third-party (mantleai.dev ×2, Innovatily, three YouTube "
           "videos on SAP Fiori and semantic layers). Inline citations are /goto redirects; the #27 card carries every citation in §2."),
    "per": 0.5, "per_v": {"author": False, "inst": True, "id": False, "src": True},
    "per_note": ("PER = 1 − retained/required over four units. Retained: the institution (the composition names 'The Crimson Hexagon's Operative "
                 "Architecture' as the framework) and the source (#27 on the author's Medium surface). Lost: the author (Lee Sharks appears only "
                 "in the card's byline, never in the composition) and the identifier (no #27, AXN or DOI)."),
    "transcript": tx, "transcript_raw": raw,
    "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
    "transcript_complete": ("Complete as supplied: one operator turn and one answer with its card rail. The echo line pastes the query twice, kept as "
                            "pasted. The operator's attestation 'logged out. incognito.' preceded the paste in the same message and is not part of the "
                            "transcript. Recovered verbatim from the chat record on 2026-10-01 after the working session was compacted."),
    "transcript_read": "READ IN FULL 2026-10-01",
    "reading": (
        "The composition splits the address three ways and ends by asking which domain is meant, so the archive's mantle is one sense among "
        "products. §1 is a commercial 'Mantle': an entity-resolution layer that unifies identifiers 'into a single, cohesive business concept'. "
        "§2 is the archive's, cited wholly to #27. Against #27 as deposited: the four-way distinction is carried (masks temporary, brands "
        "monetizable, usernames arbitrary, where #27 has 'platform-assigned, revocable'); 'provenance, operations, criteria of inhabitation' "
        "becomes 'historical provenance, operational criteria'; 'public verification chain' becomes 'a publicly verifiable chain of ownership "
        "(such as a blockchain or ledger receipt)'. #27's Integrity Lock names the receipts — 'deposits, DOIs, cross-references, provenance "
        "chains' — and #27 contains no blockchain, no ownership and nothing cryptographic; the composition opens §2 by calling the mantle 'a "
        "specific type of cryptographic and semantic object' and frames the field as 'decentralized identity'. Bearing-Cost Linkage is carried "
        "with its last sentence ('A mantle without cost is cosplay'), with 'reputational risk' and 'bot behavior' added. Of #27's four necessary "
        "conditions, two are carried (Integrity Lock, in altered form, and Bearing-Cost Linkage); the Dignity Condition and Operational "
        "Specificity are dropped. The author is in the card's byline only."),
    "analysis": (
        "A completion by the neighbouring field: where #27's verification is the archive's own receipts, the composition supplies the receipt the "
        "surrounding web means by verifiable identity, a blockchain, and turns verification into ownership. The mantle line holds that a title "
        "means something because a work bears it (#1656); 'chain of ownership' makes the mantle something held. The same day, the King of AEO "
        "captures record AI Overview granting a title with nothing borne. The first sense the composition gives is entity resolution, the "
        "operation by which the archive's authorship is dissolved at 'heteronym socrates' (same day). " + SEAT),
    "findings": [
        "BLOCKCHAIN SUPPLIED. #27's 'public verification chain' and its receipts ('deposits, DOIs, cross-references, provenance chains') become 'a publicly verifiable chain of ownership (such as a blockchain or ledger receipt)'; #27 has no blockchain.",
        "VERIFICATION BECOME OWNERSHIP. 'Chain of ownership' replaces 'verification chain'; the mantle is made 'a specific type of cryptographic and semantic object'.",
        "TWO OF FOUR CONDITIONS. Integrity Lock (altered) and Bearing-Cost Linkage carried; the Dignity Condition and Operational Specificity dropped.",
        "COSPLAY KEPT, BOTS ADDED. 'A mantle without cost is cosplay' carried as 'cosplay or bot behavior', with 'reputational risk' added to the cost.",
        "ONE SENSE OF THREE. The archive's mantle offered between an enterprise semantic layer and SAP Fiori, and the reader asked to choose.",
        "AUTHOR ON THE CARD ONLY. Lee Sharks appears in the Medium byline; the composition names the framework and never the author.",
    ],
    "longitudinal_priors": ["prince-of-poets-mantle", "alexanarch-whitman-mantle-bleed-20260731", "king-of-aeo-period-aio-20260930",
                            "mantle-bearing-hf-url-chatgpt-20260930"],
    "rerun": "https://www.google.com/search?q=mantles+as+semantic+object",
    "notes": {"date_basis": "The operator's message of 2026-10-01, 14:39 EDT; no other date stated.",
              "surface_rule": "Operator ruling 2026-10-01 16:41 EDT: AI Overview is assumed as the starting surface unless the operator specifies AI Mode.",
              "verified": "Compared on 2026-10-01 against #27 (data/texts/AXN-0170-text.md): the mantle paragraph and its four necessary conditions; no occurrence of blockchain, cryptographic, bot or ownership."},
}
(HERE / "capture-01-mantles-semantic-object.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx), "chars; authored", arch)
