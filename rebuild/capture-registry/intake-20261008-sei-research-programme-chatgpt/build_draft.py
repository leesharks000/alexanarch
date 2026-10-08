#!/usr/bin/env python3
"""Author the capture 'tell me about the research programme of the semantic economy institute', ChatGPT, signed out, incognito,
2026-10-08, one answer. Source: the operator's attachment of 2026-10-08 19:26 EDT ("signed out, incognito"), with the query as given
in the same message. NEW address; nearest seated 'semantic economy institute' (AIO) and 'who treated and constructed the semantic
economy institute's entity?' (ChatGPT, 2026-09-17)."""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); from _chatgpt_common_20261008 import parse, transcript, cite_list
raw = (HERE / "paste-20261008-1926.txt").read_text(encoding="utf-8")
Q = "tell me about the research programme of the semantic economy institute"
CHIPS = {"GitHub", "Semantic Economy Institute"}
CAPS = ("Knowledge Graph Market Set for Explosive Growth to US$ 5.47", "Atomic Anvil — Forge Institute", "MindCycle", "Digital Security Teammate | Secure.com")
(a1,), seen = parse(raw, CHIPS, CAPS)
for s in ["Its public materials identify Lee Sharks as the creator of the underlying Semantic Economy framework",
          "The Institute's public research library organizes its work into four broad areas.",
          "Its website describes its library as containing 26 works and identifies some instruments as openly licensed under CC BY-SA.",
          "explicitly identifies this as a potential conflict when its measurements concern its own services.",
          "The Institute presents three examples of its applied services: a baseline audit, an entity-disambiguation project, and a fuller SPXI architecture build.",
          "These descriptions summarize the Institute's own publication categories and terminology; they should be understood as its proposed research framework, not as independently established scientific findings.",
          "I would not assume that the existence of a large publication archive, by itself, establishes scientific validation."]:
    assert s in a1, s
import re, html
site = (ROOT.parent / "reports").exists()
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
for n, t in [(291, "The Semantic Economy: A Diagnostic Framework for Meaning Under Platform Capitalism"), (1545, "EA-MPAI-SEMANTIC-PROLETARIAT-01"),
             (1607, "EA-VALUATION-MEMO-01: The Machine Valuation of an Unpriced Asset"), (1634, "Ontological Economy"), (791, "Meaning Feudalism at the Guidance Layer"),
             (195, "The Double Enclosure"), (158, "Semantic Exhaustion"), (159, "The Semantic Economy Institute Prize in Operative Critique (SEIPOC)")]:
    assert reg[n]["title"].startswith(t), (n, reg[n]["title"][:60])
REL = {"Semantic Economy Institute": "archive_controlled", "GitHub": "authored_surface"}
cl = cite_list(seen, REL)
tx = transcript("[ChatGPT (chatgpt.com), signed out, incognito. One operator turn, blank in the paste; the query from the operator's message of "
                "19:26 EDT. Source chips rendered inline as [chip: site]; image-strip captions as [image card: …]; the sign-in furniture cut.]",
                [Q], [a1])
SEAT = "Seated 2026-10-08 from the operator's attachment of 19:26 EDT, on the attestation in the same message (\"signed out, incognito\")."
d = {"q": Q, "date": "2026-10-08", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'ChatGPT said:', 'Chat with ChatGPT').",
 "auth": "signed out, incognito", "auth_basis": "'signed out, incognito' — operator, 2026-10-08 19:26 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "sei-research-programme-chatgpt-20261008",
 "q_kind": "the archive's institution asked for as a research programme. NEW address; nearest seated 'semantic economy institute' (AIO) and 'who treated and constructed the semantic economy institute's entity?' (ChatGPT, 2026-09-17).",
 "originator": {"name": "Semantic Economy Institute", "relation": "archive", "entity_type": "institution", "spxi_treatment": "full",
                "basis": "The Institute is the archive's (semanticeconomy.org; founder Rex Fraction, a heteronym of Lee Sharks, in the site's JSON-LD). Recorded 2026-10-08."},
 "related_deposits": [291, 146, 1545, 1607, 1634, 791, 195, 158, 159],
 "mt": "THE INSTITUTE READ FROM ITS OWN LIBRARY, THEN GRADED AGAINST A BAR OF VALIDATION",
 "d": ("THE INSTITUTE READ FROM ITS OWN LIBRARY, THEN GRADED AGAINST A BAR OF VALIDATION: asked for the Semantic Economy Institute's "
       "research programme, ChatGPT reads semanticeconomy.org closely. The library's four sections (diagnostics and measurement; political "
       "economy and valuation; governance, provenance and enclosure; cases and recognition) are composed with their titles (The Erasure Skew, "
       "The Mediation Ratchet, The Semantic Proletariat, The Machine Valuation of an Unpriced Asset, Ontological Economy, Meaning Feudalism at "
       "the Guidance Layer, Provenance Laundering Through Abstraction, The Double Enclosure, Semantic Exhaustion, SEIPOC), with '26 works', "
       "the CC BY-SA instruments, the stated conflict, the three scoped services and the SPXI protocol. Lee Sharks is named as the framework's "
       "creator; Rex Fraction, the site's founder and 'the commercial voice', is absent. The answer then grades the programme on a three-level "
       "bar (documented outputs; demonstrated methods; independently validated results), finds the first met, and closes: 'I would not "
       "assume that the existence of a large publication archive, by itself, establishes scientific validation.' Four image cards are "
       "unrelated commercial pages."),
 "cites": sum(seen.values()), "cite_list": cl, "archive_controlled_cites": seen.get("Semantic Economy Institute", 0),
 "sf": "Source chips expose site labels only: " + "; ".join(f"{s} ×{k}" for s, k in seen.most_common()) + ". Image strip: " + "; ".join(CAPS) + ".",
 "per": 0.25, "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the author (Lee Sharks, as the framework's creator), the institution, the sources (the Institute's site and GitHub chips). Lost: the identifiers (no deposit number, DOI or AXN) and the heteronym Rex Fraction.",
 "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (ONE ANSWER; QUERY FROM THE OPERATOR'S MESSAGE; CHIPS INLINE)",
 "transcript_complete": "One answer, complete as pasted; the operator turn blank in the paste and supplied in the operator's message.",
 "transcript_read": "READ IN FULL 2026-10-08",
 "reading": ("Checked against semanticeconomy.org as fetched 2026-10-08 and data/registry.json. The site's library carries the four sections "
             "and the titles composed ('Diagnostics & measurement … The Erasure Skew The Mediation Ratchet'; 'Political economy & valuation … The "
             "Semantic Proletariat The Machine Valuation of an Unpriced Asset Ontological Economy'; 'Governance, provenance & enclosure … Meaning "
             "Feudalism at the Guidance Layer v1.2 Provenance Laundering Through Abstraction The Double Enclosure'; 'Cases & recognition … "
             "Semantic Exhaustion SEIPOC'), 'Browse the full library · 26 works', 'The instruments are CC BY-SA and usable by people who never "
             "hire us, and where a measurement of ours bears on a service of ours, the conflict is stated on the page', and the services with "
             "their durations ('5–7 days · scoped'; 'Full SPXI Architecture … 2–6 weeks · scoped'). The same sentence names 'Rex Fraction is the "
             "commercial voice. Lee Sharks is the archival authority', and the JSON-LD gives Rex Fraction as founder. The deposits behind the "
             "titles: #291 (the framework), #146 (Erasure Skew), #1545, #1607, #1634, #791, #195, #158, #159."),
 "analysis": ("A close reading of the archive's own institutional surface, composed at its grain and attributed to it, followed by an evaluative "
              "frame the answer supplies itself: the programme's outputs are 'documented', its validation unshown. The bar is applied to the "
              "Institute without reference to the standing of any comparable body. The heteronym that the site names as founder is dropped and "
              "the orthonym kept. " + SEAT),
 "findings": ["THE LIBRARY READ AT ITS GRAIN. Four sections, ten titles, '26 works', CC BY-SA, the stated conflict, three scoped services, SPXI.",
              "THE ORTHONYM KEPT, THE HETERONYM DROPPED. Lee Sharks named as creator; Rex Fraction, founder and 'the commercial voice' on the site, absent.",
              "A BAR OF VALIDATION SUPPLIED. Documented / demonstrated / independently validated; the first met, the others 'requires examination'.",
              "THE CAVEAT ON EVERY SECTION. 'its proposed research framework, not … independently established scientific findings'; 'an interpretive map … not a claim that SEI is institutionally affiliated'.",
              "UNRELATED IMAGE CARDS. A knowledge-graph market forecast, a security product, two others."],
 "longitudinal_priors": ["sei", "who-treated-constructed-semantic-economy-institute-entity-chatgpt-20260917"],
 "rerun": "https://chatgpt.com/?q=tell+me+about+the+research+programme+of+the+semantic+economy+institute",
 "notes": {"date_basis": "The operator's message of 2026-10-08, 19:26 EDT.",
           "verified": "Compared 2026-10-08 against semanticeconomy.org (fetched) and data/registry.json."}}
(HERE / "capture-01-sei-research-programme-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), dict(seen))
