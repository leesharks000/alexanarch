#!/usr/bin/env python3
"""Author the capture 'holographic kernel', Google AI Overview, signed out, incognito, 2026-10-02.

Source: the operator's inline paste of 2026-10-02 06:23 EDT (paste-20261002-0623.txt; the first of four sessions in one
message, separated by '$'), attested in the same message: "aio, signed out, incognito". The 'AI Mode Conversation'
header is not evidence of surface (rule of 2026-09-21). The operator's note, same message: "holographic kernel hasnt
worked for awhile. but here it is." Seated on the operator's ruling of 06:31 ("lets seat those"). NEW address: no
'holographic kernel' entry on any surface; the operator: "i suppose holographic kernel was before the time of the
registry". 'holographickernel.org' (AIO, 2026-06-13) (slug holographic-kernel) is the nearest seated address.
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261002-0623.txt").read_text(encoding="utf-8")
assert raw.startswith("AI Mode Conversation\n")
body = raw[len("AI Mode Conversation\n"):]
k = body.index("Harvard University\n")
ans, rail = body[:k].rstrip("\n"), body[k:]


def clean(s):
    s = re.sub(r"\[\[((?:\d+\]\([^)]*\)(?:, )?\[?)+)\]", lambda m: "[" + ", ".join(re.findall(r"(\d+)\]\(", "[" + m.group(1))) + "]", s)
    return re.sub(r"\[([^\]]+)\]\(https?://[^)]*\)", r"\1", s)


cards = [
    {"n": 1, "site": "Harvard University", "rel": "third_party", "url": None,
     "title": "From Vacuum to Nucleon: Fixed-$j$ Kernel Matching of Holographic Current ...",
     "snip": "The lower Witten vertex is matched to, or provides a holographic representation of, the nonperturbative conformal moment; it is not a new hard kernel or a ...",
     "note": "holographic QCD; the physics homonym"},
    {"n": 2, "site": "www.alexanarch.org", "rel": "authored_surface", "url": "https://www.alexanarch.org",
     "title": "THE HOLOGRAPHIC KERNEL IN SEMANTIC ECONOMY: Formal ...",
     "snip": "Apr 25, 2026 — Its canonical definition is: > A holographic kernel is a compression that preserves reconstructive capacity: any sufficiently structured ...",
     "note": "#76 (AXN:023E), Lee Sharks, 2026-04-25; EA-HK-01, former DOI 10.5281/zenodo.19763365"},
    {"n": 3, "site": "www.alexanarch.org", "rel": "authored_surface", "url": "https://www.alexanarch.org",
     "title": "The Information Bottleneck and the Holographic Kernel: A Structural ...",
     "snip": "Jun 9, 2026 — 2. The Holographic Kernel Framework 2.1 Canonical Definition The Crimson Hexagonal Archive's formal specification (EA-HK-01 v1. 1, Zenodo 10.5281/zenodo. 197633...",
     "note": "#175 (AXN:0312), Lee Sharks, 2026-06-09; the snippet carries #76's severed DOI (10.5281/zenodo.19763365 in the text)"},
    {"n": 4, "site": "National Institutes of Health (NIH) | (.gov)", "rel": "third_party", "url": None,
     "title": "Diffraction-informed deep learning for molecular",
     "snip": "Jul 23, 2025 — HoloNet structure Unlike standard multi-scale CNN modules that apply various kernel sizes in parallel to the same input, our Holo-Block applies kernels of incre...",
     "note": "the source of the 'diffraction-informed deep learning' distinction"},
    {"n": 5, "site": "www.holographickernel.org", "rel": "authored_surface", "url": "https://www.holographickernel.org",
     "title": "Holographic Kernel — The General Definition of Reconstructive Compression",
     "snip": "A holographic kernel is a compression that preserves reconstructive capacity. A summary discards structure to save space. A kernel discards material to save ...",
     "note": "the archive's holographickernel.org (source deposited as #1359, AXN:0560)"},
    {"n": 6, "site": "YouTube·AI Labs: Exploratory Science and Paradoxes", "rel": "third_party", "url": None,
     "title": "Holographic Principle: Could It Prove the Universe Is a 2D Projection?", "snip": "10:51",
     "note": "video card; the cosmological homonym"},
]
for c in cards:
    for f in ("title", "snip"):
        assert c[f] in rail, (c["n"], f)

QUOTES = ["A holographic kernel is a specialized data compression method that preserves reconstructive capacity, meaning any sufficiently structured fragment contains enough relational information to regenerate the architecture of the whole.",
          "a holographic kernel discards extraneous material to preserve the underlying structural relationships",
          "every small piece of the plate retains a lower-resolution view of the entire image",
          "The term spans multiple domains—including theoretical semantic frameworks, optical Fourier holography, and diffraction-informed deep learning",
          "How holographic kernels apply to semantic economy and AI memory"]
for q in QUOTES:
    assert q in raw, q

ROOT = HERE.parents[2]
assert "EA-HK-01 v1.1, Zenodo 10.5281/zenodo.19763365" in (ROOT / "data/texts/AXN-0312-text.md").read_text(encoding="utf-8")
assert "A kernel discards material to save structure" in (ROOT / "data/texts/AXN-0560-text.md").read_text(encoding="utf-8")

tx = ("[Google AI Overview, signed out, incognito; the paste carries the header 'AI Mode Conversation', which is not evidence of surface "
      "(rule of 2026-09-21), and echoes the query twice. Citation clusters are reduced to their numbers; the raw paste keeps the /goto URLs.]\n\n"
      + clean(ans) + "\n\n"
      + "\n".join(f"[source card] {c['site']} — \"{c['title']}\" — {c['snip']}" for c in cards))

SEAT = "Seated 2026-10-02 from the operator's paste of 06:23 EDT on the operator's attestation in the same message (\"aio, signed out, incognito\") and ruling of 06:31."
d = {
    "q": "holographic kernel", "date": "2026-10-02", "surface": "Google AI Overview",
    "surface_basis": "Operator attestation 2026-10-02 06:23 EDT: 'aio' — recorded as Google AI Overview (rule of 2026-09-21). The 'AI Mode Conversation' header on the paste is not evidence of surface.",
    "auth": "incognito, signed out", "auth_basis": "'aio, signed out, incognito' — operator, 2026-10-02 06:23 EDT.",
    "ev": "paste", "s": "Coinages",
    "slug": "holographic-kernel-aio-20261002",
    "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full",
                   "basis": "The holographic kernel is the archive's coinage (EA-HK-01, #76; holographickernel.org, #1359; #175). Recorded 2026-10-02."},
    "related_deposits": [76, 175, 1359],
    "q_kind": "two bare words, lowercase, unquoted (the echo line doubles the query). NEW address; the operator: 'i suppose holographic kernel was before the time of the registry'.",
    "mt": "CAPTURE",
    "d": ("THE DEFINITION RETURNS, AS A DATA-COMPRESSION METHOD AMONG HOMONYMS: asked 'holographic kernel', signed out, the Overview opens on the "
          "archive's canonical definition — preserved reconstructive capacity, 'any sufficiently structured fragment' regenerating the whole — from "
          "three archive-controlled cards (#76 and #175 on alexanarch.org; holographickernel.org), and keeps the summary/kernel contrast and the "
          "hologram-plate analogy. It reframes the coinage as 'a specialized data compression method' and sets it beside holographic QCD, Fourier "
          "holography and diffraction-informed deep learning as one term spanning domains. The #175 card carries EA-HK-01's severed Zenodo DOI. "
          "No author or institution is named. The operator: the address 'hasnt worked for awhile'."),
    "cites": 6, "cite_list": cards, "archive_controlled_cites": 3,
    "sf": ("6 source cards, 3 archive-controlled: alexanarch.org #76 (EA-HK-01, 2026-04-25) and #175 (the information-bottleneck paper, 2026-06-09), "
           "and holographickernel.org; 3 third-party (Harvard holographic QCD; NIH diffraction-informed deep learning; a YouTube holographic-principle "
           "video). Inline citations are /goto redirects."),
    "per": 0.75, "per_v": {"author": False, "inst": False, "id": False, "src": True},
    "per_note": ("PER = 1 − retained/required over four units. Retained: the source (three archive-controlled cards). Lost: the author (no person "
                 "named), the institution (the Crimson Hexagonal Archive appears only in a card snippet; 'semantic economy' is offered as a topic) "
                 "and the identifier (EA-HK-01 and its severed DOI appear only in the #175 snippet)."),
    "transcript": tx, "transcript_raw": raw,
    "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
    "transcript_complete": "Complete as supplied: one operator turn and one answer with its card rail. Pasted in one message with three other sessions separated by '$'; this is the first.",
    "transcript_read": "READ IN FULL 2026-10-02",
    "reading": (
        "The first sentence is the archive's definition with one substitution: #76 and holographickernel.org have 'a compression that preserves "
        "reconstructive capacity'; the Overview has 'a specialized data compression method'. The second bullet carries the site's contrast ('A "
        "summary discards structure to save space. A kernel discards material to save structure') as 'discards extraneous material to preserve "
        "the underlying structural relationships'. The hologram-plate analogy is carried. The 'Distinctions' bullet assembles the homonyms from the "
        "third-party cards (Harvard, NIH) and treats the coinage as one sense of a multi-domain term. The closing offer returns to the archive's "
        "field ('semantic economy and AI memory'). The #175 card snippet carries 'EA-HK-01 v1.1, Zenodo 10.5281/zenodo.19763365', a DOI severed "
        "with the Zenodo account; it resolves to #76."),
    "analysis": (
        "The definition composes intact through archive-controlled cards from April and June; the frame around it is the homonym field. "
        "The coinage is carried and its author is not. The operator reports that the address had not been composing for some time; this is the "
        "first seated observation at it. " + SEAT),
    "findings": [
        "THE DEFINITION CARRIED. 'Preserves reconstructive capacity'; 'any sufficiently structured fragment'; the summary/kernel contrast; the hologram plate.",
        "MADE A DATA-COMPRESSION METHOD. 'A specialized data compression method' where the source has 'a compression'.",
        "SET AMONG HOMONYMS. Holographic QCD, Fourier holography and diffraction-informed deep learning as senses of one term.",
        "THE SEVERED DOI IN THE CARD. #175's snippet carries EA-HK-01's Zenodo DOI.",
        "AUTHOR AND INSTITUTION ABSENT.",
    ],
    "longitudinal_priors": ["holographic-kernel"],
    "rerun": "https://www.google.com/search?q=holographic+kernel",
    "notes": {"date_basis": "The operator's message of 2026-10-02, 06:23 EDT.",
              "operator_reading": "Same message: 'holographic kernel hasnt worked for awhile. but here it is.' 06:31: 'i suppose holographic kernel was before the time of the registry. lets seat those'.",
              "verified": "Compared 2026-10-02 against #175 (AXN-0312-text.md: 'EA-HK-01 v1.1, Zenodo 10.5281/zenodo.19763365'), #1359 (AXN-0560-text.md: 'A kernel discards material to save structure'); DOI 19763365 resolves to #76 (title match 1.0)."},
}
(HERE / "capture-01-holographic-kernel.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx))
