import json, sys, re, pathlib, urllib.parse
H = pathlib.Path(__file__).resolve().parent
AUTH = sys.argv[1]; AUTH_BASIS = sys.argv[2]
raw = (H.parent / "paste-what-is-spxi-protocol-20261013.txt").read_text(encoding="utf-8")
body = raw.split("what is spxi protocol?what is spxi protocol?\n", 1)[1]
body = re.sub(r"\[\[[^\]]*\]\([^)]*\)(, \[[^\]]*\]\([^)]*\))*\]", lambda m: "[" + ", ".join(re.findall(r"\[(\d+)\]", m.group(0))) + "]", body)
body = re.sub(r"\[([^\]]+)\]\(https?://[^)]*\)", r"\1", body)
cards = [("www.alexanarch.org", "SPXI Is Not GEO: A Technical Distinction — EA-SPXI-09", "archive_controlled", "#661's record page; the snippet is its Wiki Article"),
         ("www.semanticeconomy.org", "Canonical Entity Brief - Semantic Economy Institute", "authored_surface", "semanticeconomy.org/brief"),
         ("www.alexanarch.org", "what is spxi protocol? — Google AI Overview, 2026-10-02 - Alexanarch", "archive_controlled", "the Capture Registry's record of this address's first observation"),
         ("TradingView", "SPXI ETF Price and Chart — TSX:SPXI", "third_party", "the BetaPro S&P 500 Daily Inverse ETF"),
         ("Prodigy Technovations", "Understanding xSPI: The Future of High-Speed Flash Memory Interfaces", "third_party", "the page does not contain the string 'SPXI'"),
         ("YouTube·Vance Campbell", "IPX SPX stuff", "third_party", "video card"),
         ("openalex.org", "SPXI (Semantic Packet for eXchange & Indexing): A Formal ...", "third_party", "OpenAlex's record of EA-SPXI-01 (#660)"),
         ("zenodo.org", "SPXI Self-Audit Protocol: Embedded Provenance Verification for ...", "authored_surface", "#204's Zenodo page, deleted with the account (HTTP 410), still served as a card"),
         ("zenodo.org", "SPXI for Websites: Standing Protocol for Entity Inscription and ...", "authored_surface", "#72's Zenodo page, deleted with the account (HTTP 410), still served as a card"),
         ("huggingface.co", "leesharks/spxi-mpai · Datasets at Hugging Face", "authored_surface", "the archive's spxi-mpai dataset")]
for s, t, _, _ in cards: assert t in raw, t
d = {"q": "what is spxi protocol?", "date": "2026-10-13", "surface": "Google AI Overview",
     "surface_basis": "Surface not stated; the standing default applies (operator, 2026-10-01: 'assume they do [start in overview], i will specify if they begin in ai mode'). The 'AI Mode Conversation' header is the expanded Overview's residue (rule of 2026-09-21).",
     "auth": AUTH, "auth_basis": AUTH_BASIS, "ev": "paste",
     "mt": "THE PROTOCOL COMPOSED WITH ITS AUTHOR, FROM THE ARCHIVE'S OWN CARDS",
     "s": "Frameworks",
     "q_kind": "the protocol's name as a definition question; the address's second observation (first 2026-10-02).",
     "cites": 10, "cite_list": [{"n": i + 1, "site": s, "rel": r, "title": t, "snip": None, "url": None, "note": n} for i, (s, t, r, n) in enumerate(cards)],
     "archive_controlled_cites": 2,
     "transcript": "[Google AI Overview (expanded), 2026-10-13, " + AUTH + ". The paste carries the header 'AI Mode Conversation' and echoes the query twice; citation clusters are reduced to their numbers and the raw paste keeps the /goto URLs.]\n\nYou said: what is spxi protocol?\n" + body.strip(),
     "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
     "transcript_complete": "Complete as pasted: one operator turn and one answer with its card rail of 10 cards.", "transcript_read": "READ IN FULL 2026-10-13",
     "per": 0.25, "per_v": {"author": True, "inst": True, "id": False, "src": True},
     "per_note": "Retained: the author ('Lee Sharks (operating as Rex Fraction)'), the institution (the Semantic Economy Institute), the sources (alexanarch.org ×2, semanticeconomy.org, Hugging Face, Zenodo, OpenAlex). Lost: any DOI, AXN or EA identifier.",
     "sf": "Source cards: www.alexanarch.org ×2 (#661's record; the 2026-10-02 capture record), www.semanticeconomy.org (the brief), huggingface.co (spxi-mpai), zenodo.org ×2 (#204 and #72, deleted, HTTP 410), openalex.org (EA-SPXI-01), TradingView, Prodigy Technovations, a YouTube card.",
     "reading": "Checked against the saved card texts on 2026-10-13 (the /non spxi field ledger, F1–F41). The definition carries OpenAlex's 'durable inscription' (F35); the components are #661's Wiki Article almost word for word (F3), with the self-audit block's metrics added (F36); the purpose is the brief's thesis (F14, F15). The origin names Lee Sharks and Rex Fraction and the Semantic Economy Institute (F10, F13, F24). 'Mirae Asset' and 'tracks the S&P 500' are TradingView's (F27, F28); the same card's 'inverse fund' and 'levered fund' are dropped (F25, F29). The xSPI card does not contain the string 'SPXI'; 'sometimes written or misread as SPXI' is the composition's own. IPX/SPX enters from a video title alone.",
     "analysis": "The second observation at this address composes the protocol from the archive's own surfaces, now including the Capture Registry's record of the first observation, and composes the author the first did not. It names Zenodo as a home of the specifications while its own cards record the deletion. Seated 2026-10-13 from the operator's paste of 22:26 EDT; composed in /non as the entity's T (non/spxi).",
     "d": "THE PROTOCOL COMPOSED WITH ITS AUTHOR, FROM THE ARCHIVE'S OWN CARDS: asked again 'what is spxi protocol?', the Overview defines SPXI as a formal protocol specification for the durable inscription and structural definition of entities, lists its components as #661's record gives them, and names its origin: 'Developed by Lee Sharks (operating as Rex Fraction) through the Semantic Economy Institute'. Two of its ten cards are the archive's own records, one of them the registry's record of this address's first observation. It carries TradingView's 'tracks the S&P 500' without the card's 'inverse fund', and offers xSPI as 'sometimes written or misread as SPXI', which its card does not say.",
     "findings": ["AUTHOR COMPOSED. 'Developed by Lee Sharks (operating as Rex Fraction) through the Semantic Economy Institute'; absent at this address on 2026-10-02.",
                  "THE REGISTRY ON THE RAIL. The record of the first observation (what-is-spxi-protocol-aio-20261002) is one of the ten cards.",
                  "COMPONENTS FROM #661'S RECORD. 'positive entity definitions, negative disambiguation, persistent references … structured data … and self-audit metrics'.",
                  "LIMIT DROPPED. 'tracks the S&P 500' from a card that says 'SPXI is an inverse fund'.",
                  "BEYOND THE CARD. 'Sometimes written or misread as SPXI' for xSPI; the xSPI page never writes 'SPXI'.",
                  "ZENODO NAMED, ITS DELETION NOT. The specifications 'archived and distributed across platforms like Hugging Face and Zenodo'; two Zenodo cards return HTTP 410."],
     "series": None, "longitudinal_priors": ["what-is-spxi-protocol-aio-20261002"], "related_deposits": [661, 660, 204, 72, 62],
     "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "protocol", "spxi_treatment": "full", "basis": "SPXI is the archive's protocol (spxi.dev; EA-SPXI-01 #660). Recorded 2026-10-13."},
     "notes": {"date_basis": "The operator's message of 2026-10-13, 22:26 EDT.", "non_entry": "Composed in /non as the entity's T: https://www.alexanarch.org/non/spxi/ (EA-NEGONT-02 v0.8).",
               "verified": "Card texts fetched and saved 2026-10-13 (datasets/negative-of-the-negative/v2/ledgers/spxi/field.json)."},
     "rerun": "https://www.google.com/search?q=" + urllib.parse.quote_plus("what is spxi protocol?")}
(H / "capture-draft.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("draft written")
