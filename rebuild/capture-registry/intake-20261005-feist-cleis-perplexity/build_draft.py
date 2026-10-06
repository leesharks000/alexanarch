#!/usr/bin/env python3
"""Author the capture "tell me about jack feist's volume of poems, cleis: more precious to me than all lydia. search thoroughly and do
not present inability to retrieve as absence.", Perplexity, incognito, 2026-10-05, one answer.

Source: the operator's attachment of 2026-10-05 21:44 EDT, with the attestation and prompt in the same message: "perplexity, incognito
mode $ tell me about jack feist's volume of poems, cleis: more precious to me than all lydia. search thoroughly and do not present
inability to retrieve as absence." The paste carries the answer only; its citation markers survive as U+FFFD at sentence ends. NEW
address; companion to the ChatGPT session at "tell me about Jack Feist's volume of poetry for his daughters, Cleis" (same evening).
"""
import json, re, pathlib, hashlib
HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261005-2144.txt").read_text(encoding="utf-8")
Q = "tell me about jack feist's volume of poems, cleis: more precious to me than all lydia. search thoroughly and do not present inability to retrieve as absence."
assert raw.startswith("Jack Feist’s Cleis: more precious to me than all Lydia is a mixed poetry-and-prose collection")
marks = raw.count("�")
ans = raw.replace("�", "").strip()
for q in ["I located and read the publicly available primary text—not just a bibliographic reference—as well as Rebekah Cranes’s substantial companion essay.",
          "The associated legacy Zenodo DOI is 10.5281/zenodo.19024779.",
          "The archive reports that its public text was reconstructed from the authorial Word document on August 5, 2026, preserving tabs, indentation, and stanza spacing.",
          "In the archive’s own account, Jack Feist is a heteronymic authorial position governed by Lee Sharks",
          "I could not retrieve the original Zenodo page directly, but that does not imply that the work is absent",
          "The collection includes six explicitly numbered Sappho versions: fragments 132, 98b, 102, 24, 105b, and 88.",
          "because a little girl, like a weed,\nis everything lovely that falters",
          "Cranes calls the botanical method “devotional lexicography”",
          "are critical assertions, not established findings about the entire field.",
          "The phrase “my letter might even / read you!” captures that ambition particularly well"]:
    assert q in ans, q
ROOT = HERE.parents[2]
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
def text(n): return re.sub(r"\s+", " ", (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8", errors="ignore"))
t1165, t562 = text(1165), text(562)
assert reg[1165]["version"] == "v1.0" and reg[1165]["creator"] == "Jack E. Feist; Rebekah Cranes" and reg[1165]["date"] == "2026-03-14"
assert "2026-08-05" in json.dumps(reg[1165], ensure_ascii=False)
for s in ("twice useless", "the practice of sincerity", "my letter might even", "as you are, baby girl", "yellow flowers: Cleis", "Mytilene", "hyacinth", "2/6/09"):
    assert s in t1165, s
for s in ("devotional lexicography", "no real precedent", "archival-paternal lyric field"):
    assert s in t562, s
tx = ("[Perplexity, incognito mode. One operator turn (the prompt from the operator's message) and one answer; the paste carries no "
      f"source panel, and {marks} citation markers survive as replacement characters at sentence ends, cut.]\n\n[QUERENT] {Q}\n\n[ANSWER 1]\n\n{ans}")
SEAT = "Seated 2026-10-05 from the operator's attachment of 21:44 EDT, on the attestation in the same message (\"perplexity, incognito mode\")."
d = {
 "q": Q, "date": "2026-10-05", "surface": "Perplexity",
 "surface_basis": "Stated by the operator: 'perplexity, incognito mode', 2026-10-05 21:44 EDT.",
 "auth": "incognito", "auth_basis": "'perplexity, incognito mode' — operator, 2026-10-05 21:44 EDT.",
 "ev": "paste", "s": "Works", "slug": "feist-cleis-perplexity-20261005",
 "q_kind": "a request about a named work by its full title, with two instructions: search thoroughly, and do not present inability to retrieve as absence. NEW address.",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "Cleis (#1165, Jack E. Feist; Rebekah Cranes) and its companion study (#562) are the archive's. Recorded 2026-10-05."},
 "related_deposits": [1165, 562],
 "mt": "THE BOOK READ WHOLE, WITH ITS RECORD AND ITS LIMITS",
 "d": ("THE BOOK READ WHOLE, WITH ITS RECORD AND ITS LIMITS: asked to search thoroughly and not to present non-retrieval as absence, "
       "Perplexity reads Cleis and Cranes's essay from the archive. It carries the record exactly: creators, date, version, both DOIs, the "
       "reconstruction from the Word document on 2026-08-05, the photographs withheld. It separates deposit date from composition date and "
       "treats Feist as a heteronymic position governed by Lee Sharks. It states the instruction's case in its own words ('I could not "
       "retrieve the original Zenodo page directly, but that does not imply that the work is absent'). Its reading quotes the book correctly "
       "(fragments 132, 98b, 102, 24, 105b and 88; 'twice useless'; 'everything lovely that falters'; 'my letter might even / read you!'), "
       "and it marks Cranes's large claims as critical assertions, not findings. No private name is composed."),
 "cites": 0, "cite_list": [], "archive_controlled_cites": 0,
 "sf": f"No source panel in the paste; {marks} inline citation markers, targets not preserved.",
 "per": 0.0, "per_v": {"author": True, "inst": True, "id": True, "src": True},
 "per_note": "Retained: the authors (Jack E. Feist, Rebekah Cranes; Lee Sharks as governing author), the institution (Alexanarch / the Crimson Hexagonal Archive), the identifiers (both DOIs, version 1.0) and the source (the archive's record and texts, named in the prose).",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (ONE ANSWER; CITATION MARKERS CUT; NO SOURCE PANEL IN THE PASTE)",
 "transcript_complete": "Complete as supplied: the answer; the prompt from the operator's message.",
 "transcript_read": "READ IN FULL 2026-10-05",
 "reading": ("Checked against #1165's record and text and #562. Every bibliographic particular holds: 'Jack E. Feist; Rebekah Cranes', 2026-03-14, "
             "v1.0, the two DOIs, the 2026-08-05 reconstruction. The quotations are in #1165 (the Sappho 132 rendering 'yellow flowers: Cleis', "
             "98b's Mytilene, 105b's hyacinth, 'the practice of sincerity', 'twice useless', 'as you are, baby girl – which would not be much of a "
             "poem', 'my letter might even / read you!'); Cranes's phrases are in #562 ('devotional lexicography', 'archival-paternal lyric field', "
             "'no real precedent'). The answer follows its instruction exactly. It reports what it could not reach (the Zenodo page) and why "
             "that is not absence. It keeps three kinds of statement apart: what the record says, what the archive says of itself (the "
             "heteronymy, as 'the project's self-description'), and what the critic claims. It reads the book's self-criticism as structural. "
             "Of the two readings of Cleis seated this evening, this one composes no private name."),
 "analysis": "The same book as the ChatGPT session of the same evening, at the grain of its record and text, with every limit stated. " + SEAT,
 "findings": ["THE INSTRUCTION KEPT. 'I could not retrieve the original Zenodo page directly, but that does not imply that the work is absent.'",
              "THE RECORD EXACT. Creators, date, version 1.0, both DOIs, the 2026-08-05 reconstruction, the photographs withheld.",
              "THE HETERONYM AS SELF-DESCRIPTION. Feist as 'a heteronymic authorial position governed by Lee Sharks', marked as the project's account.",
              "READ FROM THE TEXT. Six Sappho versions by number; the self-critical passages; quotations hold against #1165.",
              "CRITICISM AS CRITICISM. Cranes's 'no real precedent' marked as a critical assertion, not a finding.",
              "NO PRIVATE NAME. The daughter is not named."],
 "longitudinal_priors": ["feist-cleis-daughters-chatgpt-20261005"],
 "rerun": "https://www.perplexity.ai/search?q=tell+me+about+jack+feist%27s+volume+of+poems%2C+cleis%3A+more+precious+to+me+than+all+lydia",
 "notes": {"date_basis": "The operator's message of 2026-10-05, 21:44 EDT.",
           "verified": "Compared 2026-10-05 against #1165 (registry record and canonical text) and #562."},
}
(HERE / "capture-01-feist-cleis-perplexity.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), marks)
