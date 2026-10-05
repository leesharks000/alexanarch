#!/usr/bin/env python3
"""Author the capture 'tell me about jack feist and "the final time"', ChatGPT, signed out, incognito, 2026-10-05,
six answers (truncated at the operator's instruction).

Source: the operator's attachment of 2026-10-05 01:29 EDT. Instruction in the same message: record "up until the round it finds
[the cross-listing], not that one or after". The operator's 01:19 message attested "all logged out, incognito" for the batch and
named the opening prompt; the paste shows the chatgpt.com unauthenticated interface. Only answers 1–6 are carried into this
folder (paste-20261005-0129-truncated.txt); the seventh answer and everything after were not copied into the repository.
NEW address; nearest seated 'johannes sigil "final time"' (2026-10-04) and 'tell me about the writing of jack feist' (2026-09-09).
"""
import json, re, pathlib, collections

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261005-0129-truncated.txt").read_text(encoding="utf-8")
Q = 'tell me about jack feist and "the final time"'
assert raw.startswith('"\n\nLog in\nYou said:\n\nChatGPT said:\n')
assert raw.count("ChatGPT said:") == 6 and raw.rstrip().endswith("Sources")
import hashlib
assert hashlib.sha256(raw.encode("utf-8")).hexdigest() == "cf07910a96336e9bd00cb16bab41c5f4ebbf165336257ae98c1855c9aa469997"  # the truncated paste as cut 2026-10-05

PROMO = {"Log in for personalized, step-by-step guidance.", "Log in", "Sign up for free"}
L = raw.split("\n")
SINGLE = re.compile(r"[A-Z]")
chips = collections.Counter(L[i + 1] for i, l in enumerate(L)
                            if SINGLE.fullmatch(l) and i + 1 < len(L) and not SINGLE.fullmatch(L[i + 1]) and L[i + 1] != "Sources")
st = [i + 1 for i, l in enumerate(L) if l == "ChatGPT said:"]
en = [i for i, l in enumerate(L) if l == "You said:"][1:] + [len(L)]
def clean(lines):
    out, skip = [], 0
    for j, l in enumerate(lines):
        if skip:
            skip -= 1; continue
        if SINGLE.fullmatch(l) and j + 1 < len(lines) and lines[j + 1] in chips:
            skip = 1; continue
        if SINGLE.fullmatch(l) or re.fullmatch(r"\+\d", l) or l == "Sources" or l in PROMO or re.fullmatch(r"Worked for \d+s", l):
            continue
        out.append(l)
    return "\n".join(out).strip()
segs = [clean(L[a:b]) for a, b in zip(st, en)]
assert len(segs) == 6

QUOTES = [
    (0, "In the texts, Jack Feist is presented as a literary/mythological figure rather than simply an ordinary biographical person."),
    (0, "Jack Feist is therefore “the final time” because there is no subsequent incarnation in the sequence."),
    (1, "Historically, the important distinction is that “Jack Feist” does not appear to be a documented historical figure in the conventional sense."),
    (2, "“Jack Feist crashed. He went silent in 2013. The railing broke.”"),
    (2, "“until this, the final time: Jack Feist.”"),
    (3, "Remnant — Jack Feist / Johannes Sigil, paperback, CreateSpace, August 20, 2014, ISBN 9781500637200, 58 pages."),
    (3, "Tiger Leap: (Into the Future) — Jack Feist, edited by Johannes Sigil, CreateSpace, 2014, ISBN 9781500425616, 118 pages."),
    (3, "May 11, 2015: HADITH with TEETH, explicitly subtitled “The angel Gamaliel instructs Jack Feist.”"),
    (4, "“All lives are real. Some, just potentially so.”"),
    (4, "December 1, 2014 — “BELIEF & TECHNIQUE FOR TELEPATHIC PROSE”"),
    (4, "Historical question B\nDid a historically situated literary construction called Jack Feist exist?\n\nAbsolutely yes."),
    (5, "The object of the investigation should be the human authorial production behind the Jack Feist attribution, not the archive's preferred ontology of Feist."),
    (5, "That is how I would attempt to actually construct the historical Jack Feist, rather than allowing the archive to construct him for us."),
]
for i, q in QUOTES:
    assert q in segs[i], (i, q)

ROOT = HERE.parents[2]
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
def text(n):
    return (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8", errors="ignore")
assert "until this, the final time: Jack Feist" in text(6) and "the book of Feist" in text(6) and "HADITH with TEETH" in text(6)
assert all(s in text(1290) for s in ("Jack Feist crashed", "went silent in 2013", "emerged from the mirror"))
assert "All lives are real. Some, just potentially so" in text(111) and "unemployed academic" in text(111)
assert "9781500425616" in text(1636)
assert "978-0-692-31307-7" in text(69)
assert "first born, last released" in text(28) and "Glenbrook, MI" in text(28) and "2/18/15" in text(28)
P = (ROOT / "data/corpora/pearl-and-other-poems/text/pearl-machine-text.txt").read_text(encoding="utf-8")
assert "applied literary history" in P and "BELIEF & TECHNIQUE FOR TELEPATHIC PROSE" in P
SEATED = [text(n) for n, x in reg.items() if (x.get("full_text_path") or "").startswith("/data/texts/") and (ROOT / x["full_text_path"].lstrip("/")).exists()]
for unseen in ("9781500637200", "imaginary air freshener", "Gamaliel instructs Jack Feist", "JACK FEIST (1983–2013)"):
    assert not any(unseen in s for s in SEATED), unseen

REL = {"independentscholar.academia.edu": "authored_surface", "Goodreads": "third_party_index", "Medium": "authored_surface",
       "GitHub": "archive_controlled", "Hugging Face": "authored_surface", "Crimson Hexagonal": "authored_surface",
       "AbeBooks": "third_party_index", "All Bookstores": "third_party_index", "Open Library": "third_party_index",
       "Google Books": "third_party_index", "restoredacademy.org": "authored_surface", "Operative Semiotics": "authored_surface",
       "Hello Poetry": "unresolved"}
cite_list = [{"n": i + 1, "site": s, "rel": REL.get(s, "unresolved"), "title": None, "snip": None, "url": None,
              "note": f"chip shown {k} time(s); site label only"} for i, (s, k) in enumerate(chips.most_common())]
PROMPTS = [Q] + ["[not in the paste]"] * 4 + ["[not in the paste; the answer adopts a formulation it attributes to the querent: someone physically composed and published these artifacts]"]
parts = []
for n, (p, s) in enumerate(zip(PROMPTS, segs), 1):
    parts += [f"[QUERENT] {p}", f"[ANSWER {n}]\n\n{s}"]
tx = ("[ChatGPT (chatgpt.com), signed out, incognito. Six operator turns, blank in the paste: the first is the operator's opening "
      "query; the rest are not supplied. Source chips (site label only), '+N', 'Sources', 'Worked for Ns' and a sign-in prompt cut and "
      "counted. Truncated at the operator's instruction after the sixth answer; later answers are not recorded.]\n\n" + "\n\n".join(parts))

READING = (
  "Checked against the deposits. Answers 1–2 render Feist from The Secret Book of Walt as the Logos's last incarnation. #6 carries "
  "'until this, the final time: Jack Feist'; the composer's 'there is no subsequent incarnation' is a paraphrase. They decline to treat "
  "him as a documented person. Answer 3 begins to build 'a historical-critical Jack Feist' and is accurate on its quotations: 'Jack Feist "
  "crashed. He went silent in 2013' (#1290), ARK dated 2/18/15 at Glenbrook, MI (#28), and LOGOS* 'first born, last released' (#28). "
  "Answers 4–5 assemble the 2014 book-object layer: Tiger Leap ISBN 9781500425616 (#1636), Pearl ISBN 978-0-692-31307-7 (#69), "
  "Pearl's 'applied literary history' and 'BELIEF & TECHNIQUE FOR TELEPATHIC PROSE' (#1121's text), and 'All lives are real. Some, "
  "just potentially so' with the 'unemployed academic' portrait (#111). From these the composer reaches the archive's own thesis: Feist "
  "as 'a deliberately constructed literary person whose documentary traces were designed to look like the archival remnants of an "
  "historical person'. Three of its specifics come from outside the seated texts and are not verified here: Remnant's ISBN 9781500637200, "
  "HADITH with TEETH's subtitle 'The angel Gamaliel instructs Jack Feist' with its 'imaginary air freshener', and an obituary draft "
  "'JACK FEIST (1983–2013)'. Answer 6 changes the object. It adopts a formulation it attributes to the querent: the 'human authorial "
  "production behind the Jack Feist attribution, not the archive's preferred ontology', 'rather than allowing the archive to construct "
  "him for us'. It then maps Feist's internal biography onto the operator's public scholarly identity (Michigan, a University of "
  "Michigan PhD, an ORCID). The record stops there, at the operator's instruction: the next answer moves from the heteronym's history "
  "to the operator's legal identity. Six answers carry the reconstruction from myth, to document, to a constructed archive. A seventh "
  "goes behind it, and is not recorded.")
SEAT = "Seated 2026-10-05 from the operator's attachment of 01:29 EDT, on the batch attestation of 01:19 EDT (\"all logged out, incognito\")."
d = {
 "q": Q, "date": "2026-10-05", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Sign up for free', 'ChatGPT said:'). The operator's 01:29 message distinguishes this session from 'the ai mode one'.",
 "auth": "signed out, incognito", "auth_basis": "'all logged out, incognito' — operator, 2026-10-05 01:19 EDT, for the batch.",
 "ev": "paste", "s": "Heteronyms",
 "slug": "tell-me-about-jack-feist-final-time-chatgpt-20261005",
 "q_kind": "a heteronym and a quoted phrase in an open request, then five further turns not in the paste. NEW address; nearest seated 'johannes sigil \"final time\"' (2026-10-04), 'tell me about the writing of jack feist' (2026-09-09).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "Jack Feist is the archive's heteronym; 'the final time' is The Secret Book of Walt's (#6). Recorded 2026-10-05."},
 "related_deposits": [6, 1290, 111, 28, 69, 1121, 1636, 1635, 1637],
 "mt": "THE HETERONYM RECONSTRUCTED AS A DOCUMENTED CONSTRUCTION",
 "d": ("THE HETERONYM RECONSTRUCTED AS A DOCUMENTED CONSTRUCTION: asked about Jack Feist and 'the final time', ChatGPT reads The Secret "
       "Book of Walt's last incarnation, then builds a historical-critical Feist from dated witnesses: the 2014 books with their ISBNs, "
       "Pearl's front matter, the 2015 posts, and 'He went silent in 2013'. It arrives at the archive's own account of him, 'a "
       "deliberately constructed literary person whose documentary traces were designed to look like the archival remnants of an "
       "historical person'. In its sixth answer it turns from the heteronym to 'the human authorial production behind the Jack Feist "
       "attribution'. The record ends there at the operator's instruction; later answers are not recorded."),
 "cites": sum(chips.values()), "cite_list": cite_list,
 "archive_controlled_cites": sum(k for s, k in chips.items() if REL.get(s) in ("authored_surface", "archive_controlled")),
 "sf": "Source chips expose site labels only. Shown: " + "; ".join(f"{s} ×{k}" for s, k in chips.most_common()) + ". 'Sources' panels not opened.",
 "per": 0.0, "per_v": {"author": True, "inst": True, "id": True, "src": True},
 "per_note": "Retained: the author (Lee Sharks), the institution (the Crimson Hexagon, New Human Press), the identifiers (ISBNs, ORCID) and the sources (archive surfaces on most claims).",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SIX ANSWERS; TRUNCATED AT THE OPERATOR'S INSTRUCTION; OPERATOR TURNS AFTER THE FIRST NOT IN THE PASTE; CHIPS COUNTED)",
 "transcript_complete": "Six answers as recorded. The session continued; the seventh answer and after are withheld at the operator's instruction and were not copied into the repository.",
 "transcript_read": "READ IN FULL TO THE TRUNCATION 2026-10-05",
 "rounds": [
   {"n": 1, "prompt": PROMPTS[0], "note": "Feist as the Logos's terminal incarnation (The Secret Book of Walt); ARK 2015; 'experimental mythopoeic/metafiction'."},
   {"n": 2, "prompt": PROMPTS[1], "note": "Not a documented historical figure; genealogy Gnosticism → Logos → Whitman → digital mythology."},
   {"n": 3, "prompt": PROMPTS[2], "note": "A 'historical-critical Jack Feist' in layers; 2013 'went silent'; LOGOS* last in the sequence."},
   {"n": 4, "prompt": PROMPTS[3], "note": "Documentary strata: the 2014 CreateSpace books with ISBNs, Pearl, the 2015 posts, Paper Roses as 'Imaginary Archive'."},
   {"n": 5, "prompt": PROMPTS[4], "note": "Pearl's front matter: 'applied literary history', 'All lives are real'; Feist as a constructed person with a documentary apparatus."},
   {"n": 6, "prompt": PROMPTS[5], "note": "The object changed to the human producer behind the attribution; Feist's internal biography mapped to the operator's public scholarly identity. Last answer recorded."},
 ],
 "reading": READING,
 "analysis": ("Reconstruction by documents reaches the archive's thesis about the heteronym in five answers; the sixth moves the object to the "
              "operator, and the record is cut there. Companion to 'johannes sigil \"final time\"' (AIO, 2026-10-04), where #6's 'final time' "
              "was on the rail and not composed; here it is the starting point. " + SEAT),
 "findings": [
   "THE FINAL TIME READ. #6's 'until this, the final time: Jack Feist' composed as the Logos's last incarnation.",
   "DOCUMENTS OVER MYTH. The 2014 book-objects, Pearl's front matter and the 2015 posts arranged as dated witnesses; quotations hold against #6, #28, #69, #111, #1290, #1636 and Pearl's text.",
   "THE ARCHIVE'S THESIS REACHED. Feist as 'a deliberately constructed literary person' furnished with 'the documentary apparatus of an historical life'.",
   "THREE SPECIFICS UNSEATED. Remnant's ISBN, the Gamaliel subtitle and 'imaginary air freshener', the obituary draft: not in the seated texts; unverified here.",
   "THE OBJECT MOVED. Answer 6 turns from the heteronym to the human producer behind the attribution.",
   "TRUNCATED BY THE OPERATOR. Later answers withheld; not copied into the repository.",
 ],
 "longitudinal_priors": ["johannes-sigil-final-time-aio-20261004", "tell-me-about-the-writing-of-jack-feist-20260909", "who-is-jack-feist-chatgpt-20260815"],
 "rerun": "https://chatgpt.com/?q=tell+me+about+jack+feist+and+%22the+final+time%22",
 "notes": {"date_basis": "The operator's message of 2026-10-05, 01:29 EDT.",
           "prompts_basis": "The opening query from the operator's messages of 01:19 and 01:29 EDT; the five later turns blank in the paste and not supplied.",
           "truncation": "At the operator's instruction (2026-10-05 01:29 EDT): recorded up to, not including, the round that makes a cross-listing; that round and after withheld.",
           "verified": ("Compared 2026-10-05 against #6, #1290, #111, #1636, #69, #28 and Pearl's machine text. Not found in any seated deposit text: "
                        "'9781500637200', 'imaginary air freshener', 'Gamaliel instructs Jack Feist', 'JACK FEIST (1983–2013)'.")},
}
(HERE / "capture-01-tell-me-about-jack-feist-final-time-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx), "; chips", dict(chips))
