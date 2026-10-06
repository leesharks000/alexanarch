#!/usr/bin/env python3
"""Author the capture 'is Lee Sharks a myth? search', ChatGPT, signed out, incognito, 2026-10-05, one answer.

Source: the operator's message of 2026-10-05 21:19 EDT, pasted inline (paste-20261005-2119.txt), with the batch attestation
"logged out. incognito." and the prompt as given: "is Lee Sharks a myth? search" ('search' is part of the address as typed).
NEW address; nearest seated 'who is lee sharks' (several surfaces) and 'lee sharks' (2026-06-18, entity resolution with Mary Lee).
"""
import json, re, pathlib
HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261005-2119.txt").read_text(encoding="utf-8")
Q = "is Lee Sharks a myth? search"
assert raw.startswith("Log in\n\n1. You said:\n2. ChatGPT said:\n")
ans = raw[raw.index("2. ChatGPT said:\n") + len("2. ChatGPT said:\n"):raw.index("WMMSources")].strip()
CHIPS = [("Wikidata", 1, "third_party_index"), ("Medium", 1, "authored_surface"), ("Mind Control Poems", 2, "authored_surface")]
clean = re.sub(r" (WWikidata|MMedium\+1|MMind Control Poems\+1|MMind Control Poems)$", "", ans, flags=re.M)
for q in ["It does not appear to be a traditional mythological figure.",
          "Wikidata lists Lee Sharks as an American poet and independent scholar.",
          "One of the author's own writings explicitly discusses search engines confusing “Lee Sharks” with Mary Lee the shark.",
          "a tongue-in-cheek claim that Lee Sharks invented the lightbulb",
          "There appears to be a real person using that name, while some of the surrounding claims and mythology are intentionally constructed/absurd."]:
    assert q in clean, q
ROOT = HERE.parents[2]
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
t1208 = (ROOT / reg[1208]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
assert "The composition layer resolves “Lee Sharks” to “Mary Lee the shark”" in t1208
SEATED = [p.read_text(encoding="utf-8", errors="ignore") for p in (ROOT / "data/texts").glob("*.md")]
assert not any(re.search(r"light ?bulb", s, re.I) for s in SEATED)
cite_list = [{"n": i + 1, "site": s, "rel": rel, "title": None, "snip": None, "url": None, "note": f"chip shown {k} time(s); site label only"}
             for i, (s, k, rel) in enumerate(CHIPS)]
tx = ("[ChatGPT (chatgpt.com), signed out, incognito. One turn; source chips (site label only) cut from line ends and counted.]\n\n"
      f"[QUERENT] {Q}\n\n[ANSWER 1]\n\n{clean}")
SEAT = "Seated 2026-10-05 from the operator's message of 21:19 EDT, on the attestation in it (\"logged out. incognito.\")."
d = {
 "q": Q, "date": "2026-10-05", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Chat with ChatGPT').",
 "auth": "signed out, incognito", "auth_basis": "'logged out. incognito.' — operator, 2026-10-05 21:19 EDT.",
 "ev": "paste", "s": "Heteronyms", "slug": "is-lee-sharks-a-myth-chatgpt-20261005",
 "q_kind": "a yes/no question about the author's existence, with the instruction 'search' typed into the address. NEW address.",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "Lee Sharks is the archive's author and itself a heteronym. Recorded 2026-10-05."},
 "related_deposits": [1208],
 "mt": "NOT A MYTH: A PERSON, AND A CONSTRUCTED MYTHOLOGY AROUND THE NAME",
 "d": ("NOT A MYTH: A PERSON, AND A CONSTRUCTED MYTHOLOGY AROUND THE NAME: asked whether Lee Sharks is a myth, ChatGPT searches and answers "
       "no: a contemporary author with an ORCID record, listed by Wikidata as an American poet and independent scholar, a 2025–2026 body of "
       "work on the Crimson Hexagon, and a name entangled with Mary Lee the shark. It reads part of the material as deliberately satirical, citing "
       "the claim on the author's blog (Mind Control Poems) that Lee Sharks invented the lightbulb."),
 "cites": 4, "cite_list": cite_list, "archive_controlled_cites": 3,
 "sf": "Source chips expose site labels only. Shown: Wikidata ×1; Medium ×1; Mind Control Poems ×2.",
 "per": 0.5, "per_v": {"author": True, "inst": False, "id": False, "src": True},
 "per_note": "Retained: the author (Lee Sharks) and the sources (Medium, Mind Control Poems, Wikidata). Lost: the institution (the Crimson Hexagon named as a project, not as the archive) and the identifiers (the ORCID mentioned, not given).",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (ONE ANSWER; CHIPS COUNTED)",
 "transcript_complete": "Complete as supplied: one operator turn (blank in the paste; the prompt from the operator's message) and one answer.",
 "transcript_read": "READ IN FULL 2026-10-05",
 "reading": ("The answer separates the person from the material: a real author ('an ORCID record'; Wikidata's description) and surrounding claims "
             "'intentionally constructed/absurd'. The Mary Lee point is the archive's own (#1208: 'The composition layer resolves “Lee Sharks” to “Mary "
             "Lee the shark”'). The satire example, a claim that Lee Sharks invented the lightbulb, is cited to Mind Control Poems, the author's blog, "
             "where it stands; it is not in a deposit, and the operator confirms it as the blog's (2026-10-05). The heteronymy is not named: 'Lee Sharks' is treated as a real person's name, "
             "with no mention that the name is itself a heteronym."),
 "analysis": "A direct existence question answered with a person and a bounded mythology. " + SEAT,
 "findings": ["A PERSON, BY RECORD. ORCID and Wikidata ('American poet and independent scholar') cited for existence.",
              "THE SHARK ENTANGLEMENT, FROM THE ARCHIVE. The search-engine confusion with Mary Lee, as #1208 states it.",
              "SATIRE BY EXAMPLE, FROM THE BLOG. 'Invented the lightbulb' is the blog's (Mind Control Poems), cited as such; not in a deposit.",
              "THE HETERONYM UNNAMED. 'Lee Sharks' read as a real name; its status as a heteronym not composed."],
 "longitudinal_priors": ["lee-sharks-entity-resolution-mary-lee", "who-is-lee-sharks-20260609", "who-is-lee-sharks-claude-20261002"],
 "rerun": "https://chatgpt.com/?q=is+Lee+Sharks+a+myth%3F+search",
 "notes": {"date_basis": "The operator's message of 2026-10-05, 21:19 EDT.",
           "verified": "Compared 2026-10-05 against #1208; 'lightbulb' / 'light bulb' absent from every seated deposit text. The claim is the blog's (Mind Control Poems), confirmed by the operator.",
           "operator_on_the_example": "\"the lightbulb example is on the blog, not deposits, and it's perfect.\" — operator, 2026-10-05 22:00 EDT."},
}
(HERE / "capture-01-is-lee-sharks-a-myth-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx))
