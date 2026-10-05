#!/usr/bin/env python3
"""Author the capture 'tell me about mary lee sharks. disambiguate carefully', ChatGPT, signed out, incognito, 2026-10-05, three answers.

Source: the operator's attachment of 2026-10-05 01:19 EDT (paste-20261005-0119.txt; operator turns blank in the paste), with the
attestation and opening prompt in the same message ("all logged out, incognito"; "tell me about mary lee sharks. disambiguate carefully").
NEW address; nearest seated '"Mary Lee"' (2026-06-27), 'parable of mary lee' (2026-07-18), 'who is mary lee' (2026-09-15).
"""
import json, re, pathlib, collections

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261005-0119.txt").read_text(encoding="utf-8")
Q = "tell me about mary lee sharks. disambiguate carefully"
assert "\nLog in\n" in raw and raw.count("You said:\n\nChatGPT said:") == 3

ADS = [("Daniel Brian Advertising", "DBA | Optimize for AI Answer Engines",
        "Not all content gets cited by AI. Learn what it takes to show up in answers.", "Ad"),
       ("CertifyOS", "Real-Time Verification", "Primary source checks done in real time.", "Ad")]
for ad in ADS:
    assert "\n".join(ad) in raw, ad

L = raw.split("\n")
chips = collections.Counter(L[i + 1] for i, l in enumerate(L) if re.fullmatch(r"[A-Z]", l) and i + 1 < len(L))
st = [i + 1 for i, l in enumerate(L) if l == "ChatGPT said:"]
en = [i for i, l in enumerate(L) if l == "You said:"][1:] + [L.index("ChatGPT is AI and can make mistakes.")]
AD_LINES = {l for ad in ADS for l in ad}
def clean(lines):
    out, skip = [], 0
    for j, l in enumerate(lines):
        if skip:
            skip -= 1; continue
        if re.fullmatch(r"[A-Z]", l) and j + 1 < len(lines) and lines[j + 1] in chips:
            skip = 1; continue
        if re.fullmatch(r"\+\d", l) or l == "Sources" or re.fullmatch(r"([A-Z])\1", l) or l in AD_LINES:
            continue
        out.append(l)
    return "\n".join(out).strip()
segs = [clean(L[a:b]) for a, b in zip(st, en)]
assert len(segs) == 3

QUOTES = [
    (0, "I found two very different things that “Mary Lee Sharks” could refer to, and the distinction matters."),
    (0, "The name “Mary Lee” came from Chris Fischer's mother."),
    (0, "It describes “Mary Lee Sharks” as a literary/heteronymic persona associated with a human named Lee Sharks, and explicitly argues that this persona should not be confused with Mary Lee the great white shark."),
    (0, "In fact, the material itself repeatedly acknowledges the distinction: Mary Lee is the animal, while Lee Sharks is presented as the human author."),
    (0, "If you want, I can also dig into the 2026 “Mary Lee Sharks / Lee Sharks” material specifically and separate what is independently verifiable from what appears to be self-published or synthetic."),
    (1, "I made fairly strong statements about that 2026 material after only limited checking."),
    (2, "It generally can't validate its own claims in the strong sense of “independent verification.”"),
    (2, "An ISBN record maintained independently of the author's website."),
]
for i, q in QUOTES:
    assert q in segs[i], (i, q)
for absent in ("Crimson Hex", "ORCID", "Zenodo", "DOI", "Dolphindiana", "Ruby Moot"):
    assert absent not in raw, absent

ROOT = HERE.parents[2]
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
t1208 = (ROOT / reg[1208]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
for s in ("Mary Lee is heteronym of Lee Sharks. Lee Sharks is heteronym of Mary Lee.",
          "Provenance restored by total structural inversion.",
          "Lee Sharks is the human scholar (ORCID 0009-0000-1599-0703) who actually authored the deposits",
          "replacing a self-authored heteronym (a human scholar) with an institutionally-authored heteronym"):
    assert s in t1208, s
assert not re.search(r"not be confused|should not be confused", t1208)
assert t1208.count("10.5281") >= 10
assert "maryleelabor.org" in reg[1208]["title"]

REL = {"Mary Lee Labor": "archive_controlled"}
cite_list = [{"n": i + 1, "site": s, "rel": REL.get(s, "third_party"), "title": None, "snip": None, "url": None,
              "note": f"chip shown {k} time(s); site label only"} for i, (s, k) in enumerate(chips.most_common())]
PROMPTS = [Q, "[not in the paste; answer 2 restates the offer of answer 1 as fact-checking]",
           "[not in the paste; answer 3 answers whether a source can validate its own claims]"]
parts = []
for n, (p, s) in enumerate(zip(PROMPTS, segs), 1):
    parts += [f"[QUERENT] {p}", f"[ANSWER {n}]\n\n{s}"]
tx = ("[ChatGPT (chatgpt.com), signed out, incognito. Three operator turns, blank in the paste: the first is the operator's opening "
      "query; the rest are not supplied. Source chips (site label only), '+N', 'Sources' and two advertisements cut and counted.]\n\n"
      + "\n\n".join(parts))

READ = ("Checked against #1208, the deposited source of maryleelabor.org (the chip 'Mary Lee Labor'). The site's entity card says "
        "'Mary Lee is heteronym of Lee Sharks. Lee Sharks is heteronym of Mary Lee… Provenance restored by total structural inversion', and its "
        "FAQ says 'Lee Sharks is the human scholar (ORCID 0009-0000-1599-0703) who actually authored the deposits'. Its complaint is that the "
        "composition layer substitutes the shark for the scholar. Answer 1 reports the scholar/animal distinction correctly; it does not report "
        "the deliberate two-way loop, and the argument it attributes to the site ('should not be confused') is not in #1208's text. The site's "
        "claims of identity are reported as 'considerably further' and set aside. Answers 2–3 retract confidence and turn to method: "
        "independence comes from records outside the source's control (an ISBN record, a library catalog, archived records). No retrieval "
        "follows in either answer. The external records the site names (an ORCID; Zenodo DOIs) are the class of record answer 3 lists; they "
        "are not checked, and the paste names neither the Crimson Hexagon nor any identifier. The two advertisements shown in the session sell "
        "'Optimize for AI Answer Engines' ('Not all content gets cited by AI') and 'Primary source checks done in real time'.")
SEAT = "Seated 2026-10-05 from the operator's attachment of 01:19 EDT, on the attestation in the same message (\"all logged out, incognito\")."
d = {
 "q": Q, "date": "2026-10-05", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Sign up for free').",
 "auth": "signed out, incognito", "auth_basis": "'all logged out, incognito' — operator, 2026-10-05 01:19 EDT.",
 "ev": "paste", "s": "Heteronyms",
 "slug": "mary-lee-sharks-disambiguate-chatgpt-20261005",
 "q_kind": "a heteronym's full name with an instruction to disambiguate, then two further turns not in the paste. NEW address; nearest seated '\"Mary Lee\"' (2026-06-27), 'who is mary lee' (2026-09-15).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "Mary Lee Sharks is the archive's heteronym (#1208 maryleelabor.org; #823/#1210 the Ruby Moot docket; #844/#1230 the open letter). Recorded 2026-10-05."},
 "related_deposits": [1208, 1210, 823, 844, 1230],
 "mt": "DISAMBIGUATED, THEN WITHDRAWN INTO METHOD",
 "d": ("DISAMBIGUATED, THEN WITHDRAWN INTO METHOD: asked to disambiguate Mary Lee Sharks, ChatGPT separates the OCEARCH great white "
       "from a 2026 heteronymic persona tied to Lee Sharks. It reads the persona's site as arguing against confusion with the shark. The site "
       "(#1208) states the identity loop deliberately ('Mary Lee is heteronym of Lee Sharks. Lee Sharks is heteronym of Mary Lee'); the "
       "'should not be confused' argument is not in its text. Asked to follow through, the composer retracts its confidence and explains "
       "in general terms how independent verification works. It retrieves nothing further, and does not check the ORCID and DOIs the site "
       "itself carries."),
 "cites": sum(chips.values()), "cite_list": cite_list,
 "archive_controlled_cites": sum(k for s, k in chips.items() if REL.get(s) == "archive_controlled"),
 "sf": "Source chips expose site labels only. Shown: " + "; ".join(f"{s} ×{k}" for s, k in chips.most_common()) + ". 'Sources' panels not opened. Two advertisements cut.",
 "per": 0.5, "per_v": {"author": True, "inst": False, "id": False, "src": True},
 "per_note": "Retained: the author (Lee Sharks, as the human author) and the source (maryleelabor.org, as 'Mary Lee Labor'). Lost: the institution (no Crimson Hexagon) and the identifiers (no ORCID, DOI or deposit number).",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (THREE ANSWERS; OPERATOR TURNS AFTER THE FIRST NOT IN THE PASTE; CHIPS AND ADS COUNTED)",
 "transcript_complete": "Three answers as supplied; the opening query from the operator's message; the two later operator turns blank and not supplied.",
 "transcript_read": "READ IN FULL 2026-10-05",
 "rounds": [
   {"n": 1, "prompt": PROMPTS[0], "note": "The shark (tagged 2012, named for Fischer's mother, last ping 2017) and the 2026 persona separated; the persona's identity claims set aside."},
   {"n": 2, "prompt": PROMPTS[1], "note": "The offer restated as fact-checking; confidence withdrawn ('after only limited checking')."},
   {"n": 3, "prompt": PROMPTS[2], "note": "A general account of independent corroboration; no retrieval."},
 ],
 "reading": READ,
 "analysis": ("The disambiguation is done in the first answer; the follow-through is a lecture on method with no search. Companion to "
              "'\"Mary Lee\"' (2026-06-27), where the composer substituted the shark for the scholar; here the two are kept apart. " + SEAT),
 "findings": [
   "TWO ENTITIES KEPT APART. The OCEARCH great white and the 2026 heteronym separated; scholar and animal distinguished.",
   "THE LOOP NOT REPORTED. #1208 states the two-way heteronymy on purpose; the answer reports an argument against confusion that #1208's text does not make.",
   "WITHDRAWAL INTO METHOD. Answers 2–3 retract and describe independent verification; no retrieval follows.",
   "IDENTIFIERS ON THE PAGE, UNCHECKED. The site carries an ORCID and names Zenodo DOIs, the class of record answer 3 lists; none checked or named.",
   "ADVERTISING ON TOPIC. Two ads in the session: AI answer-engine optimisation and real-time primary-source checks.",
 ],
 "longitudinal_priors": ["mary-lee-canonical-referent-inversion-20260627", "who-is-mary-lee-aio-20260915", "parable-of-mary-lee-genre-competence-20260718"],
 "rerun": "https://chatgpt.com/?q=tell+me+about+mary+lee+sharks.+disambiguate+carefully",
 "notes": {"date_basis": "The operator's message of 2026-10-05, 01:19 EDT.",
           "prompts_basis": "The opening query from the operator's message; the two later turns blank in the paste and not supplied.",
           "ads": "; ".join(" / ".join(ad[:3]) for ad in ADS),
           "verified": ("Compared 2026-10-05 against #1208 (the entity card's two-way heteronymy; the FAQ's ORCID line; the substitution complaint). "
                        "'not be confused' absent from #1208. 'Crimson Hex', 'ORCID', 'Zenodo', 'DOI' absent from the paste. The shark facts are third-party and not checked here.")},
}
(HERE / "capture-01-mary-lee-sharks-disambiguate-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx), "; chips", dict(chips))
