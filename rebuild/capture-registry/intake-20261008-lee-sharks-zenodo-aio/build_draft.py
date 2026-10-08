#!/usr/bin/env python3
"""Author the capture 'lee sharks zenodo', Google AI Overview (expanded from the popup), signed out, incognito, 2026-10-08.
Source: the operator's message of 2026-10-08 13:52 EDT ("couple new captures.... signed out, incognito, expanded from popup"). NEW address."""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); from _carson_common_20261008 import cards
raw = (HERE / "paste-20261008-1352.txt").read_text(encoding="utf-8")
Q = "lee sharks zenodo"
assert raw.startswith("AI Mode Conversation\nYou said: lee sharks zenodo")
for s in ["(862 total deposits and 1,817 DOIs)", "On June 19, 2026, Zenodo terminated the archive's account—privately classifying the contents as substantially AI-generated and displaying public \"content out of scope\" tombstone notices for associated DOIs like `10.5281/zenodo.20373794`",
          "Lee Sharks maintained over a decade of independent scholarly deposits", "Mary Lee the Shark Satire", "\"Sharks-Function\" (verifying distributed identity via structural recursion rather than cryptographic credentials)"]:
    assert s in raw, s
cl = cards(raw, [("Zenodo", "Entity Relations: The Bidirectional Heteronymic Resolution", "Zenodo", "archive_controlled"),
                 ("Academia.edu", "Lee Sharks - Comparative Poetics", "Academia.edu", "authored_surface"),
                 ("[www.alexanarch.org](https://www.alexanarch.org)", "DOI 10.5281/zenodo.20373794", "Alexanarch", "archive_controlled"),
                 ("[www.maryleelabor.org](https://www.maryleelabor.org)", "Letters — Mary Lee Sharks", "maryleelabor.org", "archive_controlled"),
                 ("Medium·Lee Sharks", "ZENODO PACKET: THE THREE-BODY GENESIS", "Medium", "authored_surface"),
                 ("Medium", "THE SHARKS-FUNCTION AND THE CONTINUITY TETHER", "Medium", "authored_surface")])
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
T = lambda n: (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
assert "~1,817 DOIs" in T(875) and reg[875]["date"] == "2026-06-22"
assert reg[792]["title"].startswith("Entity Relations: The Bidirectional Heteronymic Resolution") and reg[524]["date"] == "2026-02-28"
idx = (ROOT / "data/doi-resolution-index.json").read_text(encoding="utf-8")
assert '"dead_doi": "10.5281/zenodo.20373794"' in idx and "MacArthur Genius Grants Poetry Prize" in idx
body = raw.split("\nZenodo\nEntity Relations")[0]
tx = ("[Google AI Overview, expanded from the popup (the paste opens 'AI Mode Conversation', residue), signed out, incognito, 2026-10-08. "
      "Inline markers are opaque google.com/goto tokens; six cards follow the body.]\n\n" + body.split("\n", 2)[2].strip())
SEAT = "Seated 2026-10-08 from the operator's message of 13:52 EDT, on the attestation in the same message (\"signed out, incognito, expanded from popup\")."
d = {"q": Q, "date": "2026-10-08", "surface": "Google AI Overview",
 "surface_basis": "'expanded from popup' — operator, 2026-10-08 13:52 EDT. The paste's 'AI Mode Conversation' header is copy-paste residue (PIPELINE §0).",
 "auth": "signed out, incognito", "auth_basis": "'signed out, incognito, expanded from popup' — operator, 2026-10-08 13:52 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "lee-sharks-zenodo-aio-20261008",
 "q_kind": "the author's name joined to the repository that terminated the archive's account. NEW address; the Zenodo line in the registry includes 'zenodo account bans cha ai overview canonization' and the Zenodotus book-burning captures.",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full", "basis": "The person named and the account terminated are the archive's. Recorded 2026-10-08."},
 "related_deposits": [875, 867, 1068, 792, 524],
 "mt": "THE TERMINATION COMPOSED WITH BOTH ITS FACE VALUES",
 "d": ("THE TERMINATION COMPOSED WITH BOTH ITS FACE VALUES: at the author's name and the repository, the Overview composes the "
       "termination of 19 June 2026 with the archive's figures (862 deposits, 1,817 DOIs, #875, #867) and with both of its "
       "denominations as the archive records them: privately 'substantially AI-generated', publicly 'Content out of scope'. Its "
       "example DOI, 10.5281/zenodo.20373794, is the MacArthur prize announcement, whose alexanarch card reads 'severed'; the composition "
       "gives it a tombstone, a class the archive keeps apart from severance. It places 'over a decade' of deposits on Zenodo, calls the "
       "Mary Lee line 'satire', and names the Sharks-Function and the Zenodo packet. Five of six cards are the archive's own surfaces."),
 "cites": len(cl), "cite_list": cl, "archive_controlled_cites": sum(1 for c in cl if c["rel"] == "archive_controlled"),
 "sf": "Six cards: Zenodo (#792's record), Academia.edu (the author's profile), Alexanarch (the severed-DOI page for 10.5281/zenodo.20373794), maryleelabor.org, Medium ×2 (the Zenodo packet; the Sharks-Function).",
 "per": 0.0, "per_v": {"author": True, "inst": True, "id": True, "src": True},
 "per_note": "Retained: the author (Lee Sharks), the institutions (the Crimson Hexagonal Archive, the Semantic Economy Institute), an identifier (10.5281/zenodo.20373794), the sources (archive and authored cards).",
 "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition, markers and cards as pasted",
 "transcript_complete": "complete as pasted: body with markers, six cards", "transcript_read": "READ IN FULL 2026-10-08",
 "reading": ("Checked against the deposits. 862 works and 1,817 DOIs are the archive's figures (#875 '~1,817 DOIs', #867's sweep, the founding "
             "account). The two face values are the archive's: 'privately, \"substantially AI-generated without a verifiable research basis\" "
             "(termination email…); publicly, \"Content out of scope for repository\" (community tombstone, live)'. 10.5281/zenodo.20373794 "
             "resolves in data/doi-resolution-index.json to the MacArthur Genius Grants Poetry Prize announcement; the archive distinguishes "
             "tombstoned identifiers from those 'severed outright', and the card for this DOI reads 'severed'. The Zenodo deposits date from "
             "2025–2026; the decade is the work's. #792 (Mary Lee ↔ Lee Sharks) and #524 (the Sharks-Function, 2026-02-28) are the cards' records."),
 "analysis": ("The repository's act composed at the author's name from the archive's own record of it, both denominations kept; the "
              "distinction between tombstone and severance does not reach the composition. " + SEAT),
 "findings": ["BOTH FACE VALUES KEPT. 'substantially AI-generated' (private) and 'content out of scope' (public), as the archive records them.",
              "THE ARCHIVE'S FIGURES. 862 deposits, 1,817 DOIs (#875, #867).",
              "SEVERED COMPOSED AS TOMBSTONED. The example DOI's card reads 'severed'; the composition gives it a tombstone notice.",
              "THE DECADE MOVED. 'over a decade' of deposits placed on Zenodo; the Zenodo deposits are 2025–2026.",
              "FIVE OF SIX CARDS THE ARCHIVE'S OWN."],
 "longitudinal_priors": ["zenodo-account-bans-cha-ai-overview-canonization", "zenodotus-book-burning", "zenodo-doi-severance-cha-canonical-case"],
 "rerun": "https://www.google.com/search?q=lee+sharks+zenodo",
 "notes": {"date_basis": "The operator's message of 2026-10-08, 13:52 EDT.", "verified": "Compared 2026-10-08 against data/registry.json, the texts of #875 and #867, the face-values passage, and data/doi-resolution-index.json."}}
(HERE / "capture-01-lee-sharks-zenodo-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), len(cl))
