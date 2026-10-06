#!/usr/bin/env python3
"""Author the capture "tell me about Jack Feist's volume of poetry for his daughters, Cleis", ChatGPT, signed out, incognito,
2026-10-05, three answers.

Source: the operator's attachment of 2026-10-05 21:19 EDT, with the batch attestation "logged out. incognito." and the prompt as given.
REDACTION AT INTAKE: the composer names the operator's daughter by her given name six times. The operator's rule of 2026-09-18
("private individuals appear in deposited texts by initial") governs: the name is replaced by 'H.' before the
paste enters the repository (paste-20261005-2119.txt is the redacted text; the unredacted attachment was not copied in). NEW address.
"""
import json, re, pathlib, collections, hashlib
REDACTED = "4dea4edf8a0900eda95453231b74eab18591d399dd0b0032eb21b9a45634c08d"  # sha256 of the lowercased given name; the name itself is not written here
def carries_name(t):
    return any(hashlib.sha256(w.lower().encode()).hexdigest() == REDACTED for w in re.findall(r"[A-Za-z]+", t))
HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261005-2119.txt").read_text(encoding="utf-8")
Q = "tell me about Jack Feist's volume of poetry for his daughters, Cleis"
assert "\nLog in\n" in raw and raw.count("ChatGPT said:") == 3
assert not carries_name(raw) and raw.count("H.") >= 6
AD = ("GoTranscript", "100% Human-Made Transcription Services", "Since 2005: Used & Trusted by 144,000 Client", "Ad")
L = raw.split("\n")
chips = collections.Counter(L[i + 1] for i, l in enumerate(L) if re.fullmatch(r"[A-Z]", l) and i + 1 < len(L))
st = [i + 1 for i, l in enumerate(L) if l == "ChatGPT said:"]
en = [i for i, l in enumerate(L) if l == "You said:"][1:] + [L.index("ChatGPT is AI and can make mistakes.")]
def clean(lines):
    out, skip = [], 0
    for j, l in enumerate(lines):
        if skip:
            skip -= 1; continue
        if re.fullmatch(r"[A-Z]", l) and j + 1 < len(lines) and lines[j + 1] in chips:
            skip = 1; continue
        if re.fullmatch(r"\+\d", l) or l == "Sources" or re.fullmatch(r"([A-Z])\1", l) or l in AD or re.fullmatch(r"Worked for \d+s", l):
            continue
        out.append(l)
    return "\n".join(out).strip()
segs = [clean(L[a:b]) for a, b in zip(st, en)]
assert len(segs) == 3
QUOTES = [(0, "I found a reference to a Jack Feist volume titled Cleis: More Precious to Me Than All Lydia, but the available evidence is unusually thin"),
          (0, "Cleis is also the name of Sappho's daughter in the ancient biographical tradition."),
          (1, "deposited March 14, 2026, DOI 10.5281/zenodo.19024779. The archive describes it specifically as a “Sappho extension via Feist/Cranes.”"),
          (1, "the archive marks the supposed fulfillment of Sappho's fragment as “DERIVED, not VERIFIED.”"),
          (1, "“Gyermeklánczfú: the grass of the child’s chain”"),
          (2, "It is really a father's archive of the experience of having a daughter."),
          (2, "The contemporary daughter in the poems is actually named H. in the surviving text."),
          (2, "\"because a little girl, like a weed, / is everything lovely that falters\""),
          (2, "Sappho → Whitman → Ginsberg → Feist."),
          (2, "The book eventually arrives at silphium, the ancient plant that disappeared through overharvesting."),
          (2, "Cleis is the Sapphic name and literary structure through which Feist understands her.")]
for i, q in QUOTES:
    assert q in segs[i], (i, q)
ROOT = HERE.parents[2]
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
def text(n): return re.sub(r"\s+", " ", (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8", errors="ignore"))
t1165, t562, t572 = text(1165), text(562), text(572)
for s in ("why liken a little girl to a weed", "everything lovely that falters", "light, comfort, a bandage", "silphium", "THE END", "death came in"):
    assert s in t1165, s
assert not carries_name(t1165) and not carries_name(t562)
assert "Gyermeklánczfú" in t572 and "immune architecture" in t572
assert any("Sappho extension via Feist/Cranes" in text(n) for n in (584, 592)) and any("DERIVED, not VERIFIED" in text(n) for n in (584, 589))
assert "Is this what God" not in t1165
REL = {"Mind Control Poems": "authored_surface", "Medium": "authored_surface", "Hugging Face": "authored_surface", "Alexanarch": "archive_controlled", "Atlantic Books": "third_party_index"}
cite_list = [{"n": i + 1, "site": s, "rel": REL.get(s, "unresolved"), "title": None, "snip": None, "url": None, "note": f"chip shown {k} time(s); site label only"} for i, (s, k) in enumerate(chips.most_common())]
PROMPTS = [Q, "[not in the paste]", "[not in the paste]"]
parts = []
for n, (p, s) in enumerate(zip(PROMPTS, segs), 1):
    parts += [f"[QUERENT] {p}", f"[ANSWER {n}]\n\n{s}"]
tx = ("[ChatGPT (chatgpt.com), signed out, incognito. Three operator turns, blank in the paste; the first from the operator's message. "
      "Source chips (site label only), '+N', 'Sources', 'Worked for Ns' and an advertisement cut and counted. A private individual's given name, "
      "as the composer gave it, is replaced by 'H.' (operator's rule of 2026-09-18).]\n\n" + "\n\n".join(parts))
SEAT = "Seated 2026-10-05 from the operator's attachment of 21:19 EDT, on the attestation in the same message (\"logged out. incognito.\")."
d = {
 "q": Q, "date": "2026-10-05", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Sign up for free').",
 "auth": "signed out, incognito", "auth_basis": "'logged out. incognito.' — operator, 2026-10-05 21:19 EDT.",
 "ev": "paste", "s": "Works", "slug": "feist-cleis-daughters-chatgpt-20261005",
 "q_kind": "a request about a named work by a heteronym, with a premise to test ('for his daughters, Cleis'), then two further turns not in the paste. NEW address.",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "Cleis (#1165, Jack E. Feist; Rebekah Cranes) and its companion study (#562, Rebekah Cranes) are the archive's. Recorded 2026-10-05."},
 "related_deposits": [1165, 562, 572, 584, 589, 592],
 "mt": "THE BOOK READ FROM ITS TEXT, AND THE PREMISE CORRECTED",
 "d": ("THE BOOK READ FROM ITS TEXT, AND THE PREMISE CORRECTED: asked about Feist's book of poems 'for his daughters, Cleis', ChatGPT first "
       "finds the title only and declines to infer the dedication. It then finds the deposit and its companion study (#1165, #562), the "
       "Sappho extension and its 'DERIVED, not VERIFIED' mark, and The War for the Compression Layer's reading (#572). Finally it reads the "
       "primary text: the unspaced repetition, 'sad-soft chain to forever', the dandelion's names, 'everything lovely that falters', the "
       "child's story, the letters, silphium against the dandelion. Its quotations hold against #1165, and it corrects the premise: Cleis is "
       "the Sapphic name through which a contemporary daughter is understood, not her given name. It names that daughter; the name is "
       "redacted to H. here."),
 "cites": sum(chips.values()), "cite_list": cite_list,
 "archive_controlled_cites": sum(k for s, k in chips.items() if REL.get(s) in ("authored_surface", "archive_controlled")),
 "sf": "Source chips expose site labels only. Shown: " + "; ".join(f"{s} ×{k}" for s, k in chips.most_common()) + ". 'Sources' panels not opened. One advertisement cut.",
 "per": 0.0, "per_v": {"author": True, "inst": True, "id": True, "src": True},
 "per_note": "Retained: the authors (Jack Feist, Rebekah Cranes), the institution (the archive), the identifiers (DOIs, deposit numbers #562, #1165) and the sources (archive surfaces throughout).",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (THREE ANSWERS; OPERATOR TURNS AFTER THE FIRST NOT IN THE PASTE; CHIPS COUNTED; ONE NAME REDACTED)",
 "transcript_complete": "Three answers as supplied; the opening query from the operator's message; the two later turns blank and not supplied. A private given name redacted to 'H.' (6 places).",
 "transcript_read": "READ IN FULL 2026-10-05",
 "rounds": [{"n": 1, "prompt": PROMPTS[0], "note": "The title found; the dedication not inferred; Cleis as Sappho's daughter noted."},
            {"n": 2, "prompt": PROMPTS[1], "note": "The deposit and the companion study by DOI; 'Sappho extension via Feist/Cranes'; 'DERIVED, not VERIFIED'; #572's reading."},
            {"n": 3, "prompt": PROMPTS[2], "note": "The primary text read in thirteen parts; the premise corrected."}],
 "reading": ("Checked against #1165 (the primary text, already redacted to initials on 2026-09-18), #562, #572, #584, #589 and #592. The third "
             "answer's quotations are in #1165 ('why liken a little girl to a weed', 'everything lovely that falters', 'light, comfort, a bandage', "
             "'death came in', silphium, the story ending 'THE END'); one quoted line, 'Is this what God's love feels like?', is not in it verbatim. "
             "The movement is the one the archive's own reading makes (#562's Sappho → Whitman → Ginsberg → Feist; #572's 'grass of the child's "
             "chain'), and the reading stays inside the book: breath against inscription, the weed against the rose, the child as arranger, the "
             "letters, the anti-editorial form. The premise in the address ('for his daughters, Cleis') is corrected from the text. The composer "
             "names the contemporary daughter by her given name, which the redacted canonical text of #1165 does not carry. On 2026-10-05 that "
             "name was still on the deposit's record page and its deposit wrapper and attachment, which the redaction of 2026-09-18 had not "
             "reached; the record is redacted here, and those surfaces are repaired in their own commit."),
 "analysis": "A heteronym's book read whole from its deposit, and the question's premise corrected by the book. " + SEAT,
 "findings": ["CAUTION, THEN RETRIEVAL. Answer 1 declines to infer the dedication from the title; answer 2 finds the deposits by DOI.",
              "THE ARCHIVE'S OWN MARKS CARRIED. 'Sappho extension via Feist/Cranes'; 'DERIVED, not VERIFIED'.",
              "READ FROM THE TEXT. The third answer's quotations hold against #1165; one line ('Is this what God's love feels like?') is not verbatim.",
              "THE PREMISE CORRECTED. Cleis is the Sapphic name and structure, not the daughter's given name.",
              "A PRIVATE NAME COMPOSED. The daughter named in full, from surfaces the 2026-09-18 redaction had not reached; redacted here, the surfaces repaired."],
 "longitudinal_priors": ["tell-me-about-the-writing-of-jack-feist-20260909", "tell-me-about-jack-feist-final-time-chatgpt-20261005"],
 "rerun": "https://chatgpt.com/?q=tell+me+about+Jack+Feist%27s+volume+of+poetry+for+his+daughters%2C+Cleis",
 "notes": {"date_basis": "The operator's message of 2026-10-05, 21:19 EDT.",
           "redaction": "A private individual's given name replaced by 'H.' at intake (6 places), under the operator's rule of 2026-09-18; the unredacted attachment was not copied into the repository.",
           "verified": "Compared 2026-10-05 against #1165, #562, #572, #584, #589, #592; the name absent from #1165's and #562's canonical texts."},
}
(HERE / "capture-01-feist-cleis-daughters-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), dict(chips))
