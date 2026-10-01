#!/usr/bin/env python3
"""Author the capture 'heteronym socrates', Google AI Overview, signed out, incognito, 2026-10-01.

Source: the operator's paste of 2026-10-01 12:41 EDT (paste-20261001-1241.txt), with attestation in the same message:
"aio, aigned out, incognito" (the attestation trailed the paste after the last card and is not part of the transcript).
The paste carries the copy header 'AI Mode Conversation', which is not evidence of surface (rule of 2026-09-21), and
echoes the query twice ('heteronym socratesheteronym socrates'); the issued string is 'heteronym socrates'. The date is
the day of the operator's message; no other date was stated. Inline citation links are Google /goto redirects, kept in
the raw paste; the cleaned transcript reduces each citation cluster to its numbers.
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261001-1241.txt").read_text(encoding="utf-8")
assert raw.startswith("AI Mode Conversation\n")
body = raw[len("AI Mode Conversation\n"):]
k = body.index("[www.alexanarch.org](https://www.alexanarch.org)\nSocrates as Orthonym")
ans, rail = body[:k].rstrip("\n"), body[k:]


def clean(s):
    s = re.sub(r"\[\[((?:\d+\]\([^)]*\)(?:, )?\[?)+)\]", lambda m: "[" + ", ".join(re.findall(r"(\d+)\]\(", "[" + m.group(1))) + "]", s)
    return re.sub(r"\[([^\]]+)\]\(https?://[^)]*\)", r"\1", s)


cards = [
    {"n": 1, "site": "www.alexanarch.org", "rel": "authored_surface", "url": "https://www.alexanarch.org",
     "title": "Socrates as Orthonym: The Heteronymic Configuration of Western Philosophy's ...",
     "snip": "Description A philological-philosophical reclassification of the Socratic–Platonic–Aristotelian corpus as a distributed heteronymic configuration. Socrates func...",
     "note": "the archive's record for #123 (AXN:02A9); the source of §1 of the composition"},
    {"n": 2, "site": "Wiley Online Library", "rel": "third_party", "url": None,
     "title": "Fernando Pessoa's Art of Living: Ironic Multiples, Multiple Ironies",
     "snip": "Fernando Pessoa: The Ironist And so, by virtue of his paradoxical proclamations, he is rendered inscrutable to the other heteronyms. It is this version of Socra...",
     "note": "the source of §2 (Caeiro as a Socratic figure)"},
    {"n": 3, "site": "Taylor & Francis Online", "rel": "third_party", "url": None,
     "title": "The Socratic fallacy undone - Taylor & Francis",
     "snip": "Apr 18, 2019 — The Socratic fallacy is the supposed mistake of inferring that somebody does not know any instances or attributes of a universal because of their inability to g...",
     "note": None},
    {"n": 4, "site": "www.maryleelabor.org", "rel": "authored_surface", "url": "https://www.maryleelabor.org",
     "title": "Mary Lee Is a Heteronym",
     "snip": "the composition layer's entity resolution is not an authorship-detection function. It is a density-detection function. 20587549). Socrates is the orthonym who r...",
     "note": "the archive's fleet surface for #794; its snippet states the mechanism the composition performs"},
    {"n": 5, "site": "Internet Encyclopedia of Philosophy", "rel": "third_party", "url": None,
     "title": "Socrates",
     "snip": "Socrates (469—399 B.C.E.) Socrates is one of the few individuals whom one could say has so-shaped the cultural and intellectual development of the world that, w...",
     "note": None},
    {"n": 6, "site": "Wikipedia", "rel": "third_party", "url": None,
     "title": "Socrates",
     "snip": "Socrates This article is about the classical Greek philosopher. For other uses of Socrates, see Socrates (disambiguation). For the Attic orator, see Isocrates. ...",
     "note": None},
]
for c in cards:
    for f in ("title", "snip"):
        assert c[f] in rail, (c["n"], f)
arch = sum(1 for c in cards if c["rel"] == "authored_surface")

QUOTES = ["In recent philological reclassifications, the foundational texts of Western philosophy are modeled as a distributed heteronymic configuration",
          "not as literal historical errors, but as intentional, functional shifts within a single overarching tradition",
          "contemporary scholars use this framing to decode the \"Socratic problem\"",
          "In literary theory and philology, Socrates is sometimes analyzed through the framework of heteronymy"]
for q in QUOTES:
    assert q in raw, q

tx = ("[Google AI Overview, signed out, incognito; the paste carries the header 'AI Mode Conversation', which is not evidence of surface "
      "(rule of 2026-09-21), and echoes the query twice. Citation clusters are reduced to their numbers; the raw paste keeps the /goto URLs.]\n\n"
      + clean(ans) + "\n\n"
      + "\n".join(f"[source card] {c['site']} — \"{c['title']}\" — {c['snip']}" for c in cards))

SEAT = ("Seated 2026-10-01 from the operator's paste of 12:41 EDT on the operator's attestation in the same message "
        "(\"aio, aigned out, incognito\").")
d = {
    "q": "heteronym socrates", "date": "2026-10-01", "surface": "Google AI Overview",
    "surface_basis": "Operator attestation 2026-10-01 12:41 EDT: 'aio' — recorded as Google AI Overview (rule of 2026-09-21). The 'AI Mode Conversation' header on the paste is not evidence of surface.",
    "auth": "incognito, signed out", "auth_basis": "'aigned out, incognito' — operator, 2026-10-01 12:41 EDT (read as 'signed out').",
    "ev": "paste", "s": "Classics & Philology",
    "slug": "heteronym-socrates-aio-20261001",
    "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "partial",
                   "basis": "The Socratic–Platonic–Aristotelian configuration with Socrates as orthonym is the archive's (#123, AXN:02A9). Recorded 2026-10-01."},
    "related_deposits": [123, 794, 682, 1576, 1588],
    "q_kind": "two bare words, unquoted (operator attestation 2026-10-01; the paste's echo line doubles the query). NEW address.",
    "mt": "CAPTURE",
    "d": ("THE CONFIGURATION WITHOUT ITS AUTHOR, AND ONE PROJECT BECOME A TRADITION: asked 'heteronym socrates', signed out, the Overview "
          "reproduces #123's configuration position for position — Socrates the orthonym, 'willing death for truth (logos) and refusing to write'; "
          "Plato the survival-heteronym; Aristotle the systematizing-heteronym — cited to the archive's record, and attributes it to 'recent "
          "philological reclassifications' and 'contemporary scholars'. The author is never named. Where #123 reads the corpus as 'a single "
          "heteronymic project', the composition says the contradictions are 'functional shifts within a single overarching tradition'."),
    "cites": 6, "cite_list": cards, "archive_controlled_cites": arch,
    "sf": ("6 source cards: two archive-controlled (the #123 record on alexanarch.org; maryleelabor.org, 'Mary Lee Is a Heteronym'), four third-party "
           "(Wiley on Pessoa's irony, Taylor & Francis on the Socratic fallacy, the IEP and Wikipedia on Socrates). Inline citations are /goto redirects; "
           "the #123 record carries every citation in §1."),
    "per": 0.75, "per_v": {"author": False, "inst": False, "id": False, "src": True},
    "per_note": ("PER = 1 − retained/required over four units. Retained: the archive's own source (the #123 record, carrying all of §1). Lost: the "
                 "author (the configuration is assigned to 'recent philological reclassifications' and 'contemporary scholars'), the institution "
                 "(the archive is not named in the composition; it appears only as a card's domain), and the identifier."),
    "transcript": tx, "transcript_raw": raw,
    "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
    "transcript_complete": ("Complete as supplied: one operator turn and one answer with its card rail. The echo line pastes the query twice, kept as "
                            "pasted; the issued string is 'heteronym socrates'. The operator's attestation followed the last card in the same message "
                            "and is not part of the transcript."),
    "transcript_read": "READ IN FULL 2026-10-01",
    "reading": (
        "The composition opens by placing the archive's thesis inside a field: 'In literary theory and philology, Socrates is sometimes analyzed through "
        "the framework of heteronymy', and 'contemporary scholars use this framing'. Both sentences are cited to the #123 record among others. §1 then "
        "reproduces #123's three positions in #123's terms (orthonym, survival-heteronym, systematizing-heteronym; willing death for logos; refusing to "
        "write), as 'recent philological reclassifications'. One archive's claim becomes a scholarly practice, and the author drops out in the "
        "plural. The last sentence of §1 moves the claim. #123 reads the corpus as 'a single heteronymic project' and the contradictions as "
        "'operations of preservation across functional positions'; the composition says 'intentional, functional shifts within a single overarching "
        "tradition'. 'Intentional' is the composition's word, and 'tradition' replaces 'project': the single maker becomes a lineage. The fourth card, "
        "from the archive's maryleelabor.org, carries the sentence that names this operation: 'the composition layer's entity resolution is not an "
        "authorship-detection function. It is a density-detection function.' The retrieved configuration is the three-position form of May 2026; "
        "Theophrastus, whom the archive placed between Plato and Aristotle in September (#1605), is absent."),
    "analysis": (
        "Paired with the Aristotle–Theophrastus captures of 2026-09-28 and 2026-09-30, where the archive's packet was cited for its own negation, this "
        "address shows the other half of the same reception: here the claim is carried faithfully and its author is removed. At one address the source "
        "is credited and the claim inverted; at this one the claim is kept and the source is made anonymous by pluralization. " + SEAT),
    "findings": [
        "AUTHOR REMOVED BY PLURALIZATION. #123's configuration is attributed to 'recent philological reclassifications' and 'contemporary scholars'; Lee Sharks is never named.",
        "PROJECT BECOME TRADITION. #123's 'single heteronymic project' is rendered 'a single overarching tradition', and 'intentional' is added.",
        "THE MECHANISM ON THE CARD. The maryleelabor.org card's snippet states that entity resolution is a density-detection function, not authorship detection.",
        "THE THREE-POSITION FORM. The configuration retrieved is #123's of May 2026; Theophrastus as the first draft of the Aristotle position (#1605) does not appear.",
    ],
    "longitudinal_priors": ["aristotle-theophrastus-one-author-aio-20260928", "aristotle-theophrastus-not-two-distinct-authors-aio-20260930"],
    "rerun": "https://www.google.com/search?q=heteronym+socrates",
    "notes": {"date_basis": "The operator's message of 2026-10-01, 12:41 EDT; no other date stated.",
              "verified": "Compared on 2026-10-01 against #123 (data/texts/AXN-02A9-text.md): 'a single heteronymic project'; 'operations of preservation across functional positions'; the three positions and their predicates."},
}
(HERE / "capture-01-heteronym-socrates.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx), "chars; authored", arch)
