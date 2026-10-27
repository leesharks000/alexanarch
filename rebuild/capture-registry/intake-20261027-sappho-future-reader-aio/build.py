#!/usr/bin/env python3
"""One capture from the operator's message of 2026-10-27, 14:00 EDT: 'sappho future reader' on Google AI Overview, pasted with its
source cards. The operator: "low grain and deeply lossy and it erases authorship but at least it no longer attributes my actual words to
others". And, at 14:00: "the analysis should focus on restoring rigor and grounding, as it may become what is cited" — so the reading
restores the reading the Overview composes from, at its own grain, with its loci, before it measures the loss.

ROUTE: 'sappho future reader' on Google AI Overview is seated (sappho-future-reader-aio-20260825, observed 25 August, 15 September and
28 September); this seats as a longitudinal observation of that record. Defaults: signed out and incognito (2026-10-14); a Google paste
is the Overview (2026-10-01). Quotations of the archive are checked against data/texts/ by this script; every per_dim span against the
transcript."""
import json, re, pathlib
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
DATE = "2026-10-27"
Q = "sappho future reader"
raw = (HERE / "paste-sappho-future-reader-aio.txt").read_text(encoding="utf-8")
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
root = next(e for e in caps["entries"] if e.get("q") == Q and e.get("surface") == "Google AI Overview")
assert root["slug"] == "sappho-future-reader-aio-20260825"


def red(b):
    b = re.sub(r"\[\[[^\]]*\]\([^)]*\)(, \[[^\]]*\]\([^)]*\))*\]", lambda m: "[" + ", ".join(re.findall(r"\[(\d+)\]", m.group(0))) + "]", b)
    return re.sub(r"\[([^\]]*)\]\(https?://[^)]*\)", r"\1", b)


body = raw.split("\n", 2)[2]                      # after the popup header and the query line (doubled in the paste)
assert raw.split("\n")[1] == "You said: sappho future readersappho future reader"
ov, cards = body.split("\n[www.alexanarch.org]", 1)
cards = "[www.alexanarch.org]" + cards
ov = red(ov).strip()
for s in ["is a conceptual and literary approach that examines how ancient lyric poetry—specifically the fragments of Sappho, such as Fragment 31 and Fragment 147—directly addresses and constructs an unknown reader in the future.",
          "relying on deictic language (words that point to time and space, like here or that)",
          "Academic and literary analyses (such as studies on Fragment 31) examine how distal pointers and sensory details pull a distant reader into the immediate intensity of the speaker's experience.",
          "the framework treats the act of reading not as passive reception, but as an active, anticipated encounter designed by the poet."]:
    assert s in ov, s
assert "into the immediate intensity of the speaker's experience" in ov
tx = ("[Google AI Overview, " + DATE + ", signed out, incognito. The Overview and its source cards as pasted in the operator's message of 14:00 EDT; "
      "the query line, doubled in the paste, given once; citation clusters reduced to their numbers, links to their text (the raw paste keeps the "
      "/goto URLs).]\n\n" + f"You said: {Q}\n\n{ov}\n\nSource cards:\n" + red(cards).strip())

TXT = {n: (ROOT / f"data/texts/AXN-{h}-text.md").read_text(encoding="utf-8") for n, h in ((1270, "0507"), (1645, "06D3"), (1054, "042A"), (134, "02C2"))}
for n, s in [(1270, "based on reassessment of deictic structure and colour semantics"),
             (1270, "points not to a present rival but to a future reader—the one who will sit 'face-to-face' (ἐνάντιος) with the inscribed text"),
             (1270, "The poem's somatic catalogue describes the phenomenology of voice becoming text, while the χλωρός simile figures the speaker's transformation into papyrus substrate"),
             (1270, "the poem ends with an imperative that song survive 'in letters' (γράμμασι)"),
             (1270, "### II.2 The Second Person as Text"), (1270, "it points away from the speaker, toward someone removed from the immediate situation"),
             (1270, "Not 'that man' but 'whatever man'"), (1270, "Catullus is κῆνος"),
             (1645, "147 is the proposition; 31 is the construction. 147 does not contain 31's mechanism, and τινα does not mean \"reader\"."),
             (1645, "μνάσεσθαί τινά φαμι καὶ ἕτερον ἀμμέων"),
             (1645, "**Provenance.** Lee Sharks; first published under Johannes Sigil and Rebekah Cranes, 2025-11-21 and 2026-01-09."),
             (1054, "Sappho 31 is a transmission-engineering operation addressed to the future reader through the κῆνος deictic")]:
    assert s in TXT[n], (n, s)

cites = [
    {"n": 1, "site": "www.alexanarch.org", "rel": "archive_controlled", "title": "What are the arguments in “Sappho's Future Reader: Fragment 147 States the ...",
     "snip": "Oct 12, 2026 — 3. The two fragments form a single interpretive operation The title's distinction between a “horizon” and a “seat” is the conceptual heart of ...",
     "url": "https://www.alexanarch.org", "note": "the capture record sappho-future-reader-packet-ask-chatgpt-20261012 (AXN:099A.CAPTURE), ChatGPT reading #1645; a page about a composition, not the work"},
    {"n": 2, "site": "www.alexanarch.org", "rel": "archive_controlled", "title": "What is the Sappho future reader framework? — Google AI Overview ...",
     "snip": "Oct 17, 2026 — THE SAPPHO FUTURE READER FRAMEWORK: asked what it is, the AI Overview gives 'a poetic transmission engineered specifically for a reader in ...",
     "url": "https://www.alexanarch.org", "note": "the capture record what-is-the-sappho-future-reader-framework-aio-20261017 (AXN:09F8.CAPTURE); the source of the composition's name for the reading"},
    {"n": 3, "site": "Instagram · Female Tales", "rel": "third_party", "title": "0:45", "snip": "“I tell you, someone will remember us in the future.” That line comes from one of ...",
     "url": None, "note": "a 45-second video; the source of the Fragment 147 line as quoted"},
    {"n": 4, "site": "medium.com", "rel": "authored_surface", "title": "EA-MPAI-SAPPHO31-01 v1.0 | by Lee Sharks | Medium",
     "snip": "Jul 22, 2026 — Sappho 31 is a transmission-engineering operation addressed to the future reader through the κῆνος deictic; jealousy-lyric readings and future-reader readings .",
     "url": None, "note": "#1054 (AXN:042A), its canonical claim; the source of 'transmission'. The card names the author", "deposit_candidates": [1054]},
    {"n": 5, "site": "www.crimsonhexagonal.org", "rel": "authored_surface", "title": "ΦΑΙΝΕΤΑΙ ΜΟΙ: Sappho 31 and the Inscription of the Future Reader ...",
     "snip": "This article proposes a new reading of Sappho Fragment 31 (Voigt) based on reassessment of deictic structure and colour semantics. I argue that the distal ...",
     "url": "https://www.crimsonhexagonal.org", "note": "#1270 (AXN:0507), its abstract; the source of 'deictic structure' and 'semantics'", "deposit_candidates": [1270]},
]

reading = (
    "The innocent reading first. Asked 'sappho future reader', the Overview names 'the Sappho Future Reader Framework', 'a conceptual and literary approach' "
    "examining how Sappho's fragments, 'such as Fragment 31 and Fragment 147', 'directly address and construct an unknown reader in the future', and gives "
    "three concepts: poetic transmission, a message sent across centuries by deictic language; the future reader, after Fragment 147, reading as 'an active, "
    "anticipated encounter designed by the poet'; deictic structure and semantics, in which 'Academic and literary analyses (such as studies on Fragment 31)' "
    "examine how distal pointers and sensory detail pull a distant reader into the speaker's experience. It offers Anne Carson's translations next. Five cards: "
    "two archive capture records, an Instagram video, #1054 on Medium, #1270 on crimsonhexagonal.org. No person is named in the answer. "
    "Against the texts. The reading the Overview composes from is Lee Sharks's, first published under the heteronyms Johannes Sigil and Rebekah Cranes on "
    "2025-11-21 (The Future Beloved, #134, on Medium) and 2026-01-09 (ΦΑΙΝΕΤΑΙ ΜΟΙ: Sappho 31 and the Inscription of the Future Reader, #1270, AXN:0507), "
    "with its metadata packet EA-MPAI-SAPPHO-FUTURE-READER-01 (#1645, AXN:06D3, 2026-09-28). At its own grain it makes five claims about Fragment 31 (Voigt), "
    "argued in #1270 from deictic structure and colour semantics. (1) Deixis: the distal demonstrative κῆνος (line 1) 'points not to a present rival but to a "
    "future reader—the one who will sit \"face-to-face\" (ἐνάντιος) with the inscribed text' (abstract; §II.1, with Wackernagel, Bonifazi on κεῖνος in Pindar "
    "and D'Alessio on temporal deixis), and the relative ὄττις universalises it (\"Not 'that man' but 'whatever man'\"). (2) The second person is the text: τοι and σ' address "
    "Sappho-as-inscribed (§II.2). (3) 'The poem's somatic catalogue describes the phenomenology of voice becoming text' (abstract; §III). (4) 'the χλωρός simile figures "
    "the speaker's transformation into papyrus substrate' (abstract; §IV). (5) The lost stanza is reconstructed so that 'the poem ends with an imperative that song "
    "survive \"in letters\" (γράμμασι)' (abstract; §V); Catullus 51 is the first occupant of the seat ('Catullus is κῆνος', §VI). Fragment 147 (μνάσεσθαί τινά φαμι καὶ "
    "ἕτερον ἀμμέων) enters with the packet, which states the relation and its limit: '147 is the proposition; 31 is the construction. 147 does not contain 31's "
    "mechanism, and τινα does not mean \"reader\".' The remembrance reading of 147 is common ground (#1645 §1). "
    "Against that, the Overview keeps the two fragments, the deictic mechanism in general form and the transmission. 'Poetic Transmission' is #1054's claim "
    "('Sappho 31 is a transmission-engineering operation addressed to the future reader through the κῆνος deictic', EA-MPAI-SAPPHO31-01, 2026-07-08) with κῆνος "
    "removed; 'Deictic Structure & Semantics' is #1270's 'deictic structure and colour semantics' with the colour removed. It loses κῆνος, ἐνάντιος, the "
    "inscribed text, the second person as text, the somatic catalogue, papyrus, the reconstruction and Catullus; the seat becomes a reader pulled 'into the "
    "immediate intensity of the speaker's experience', inside the scene, where #1270's κῆνος is distal: 'it points away from the speaker, toward someone "
    "removed from the immediate situation'. Fragment 147's line is chipped to an Instagram video. "
    "The joining of the two fragments, the packet's marked contribution, is given as the framework's ground ('Rooted in lines like Sappho's famous fragment'), "
    "and 147's limit is dropped: the future reader 'designed by the poet' is the claim #1645 declines to make of τινα. The author, the heteronyms, the dates, "
    "the titles and the identifiers are absent; the framework's sources appear as 'Academic and literary analyses', a plural with no name. "
    "Against this address's earlier observations: on 25 August the lineage's coinage 'self-archiving' was attributed to 'Scholars' and chipped to a page that "
    "does not contain it; on 28 September the article's title phrase stood as link text with no author. Here no named other holds the reading's words, and the "
    "author is still absent: the operator's reading (2026-10-27, 14:00 EDT), 'low grain and deeply lossy and it erases authorship but at least it no longer "
    "attributes my actual words to others'."
)
d = ("SAPPHO FUTURE READER. ON GOOGLE AI OVERVIEW, SIGNED OUT, FOURTH OBSERVATION: 'the Sappho Future Reader Framework', 'a conceptual and literary approach', "
     "Fragments 31 and 147 constructing 'an unknown reader in the future' through transmission and deixis, from #1054 and #1270 with κῆνος, the inscribed text, "
     "papyrus, the reconstruction and Catullus removed; no author, no date, no identifier; the words no longer attributed to others.")
findings = [
    "THE READING RESTORED AT ITS GRAIN. Lee Sharks, as Johannes Sigil and Rebekah Cranes (#134, 2025-11-21; #1270, AXN:0507, 2026-01-09; #1645, AXN:06D3): κῆνος as the future reader facing the inscribed text (§II.1), the second person as text (§II.2), the somatic catalogue as voice becoming text (§III), χλωρός as papyrus (§IV), the reconstructed ending in letters (§V), Catullus as κῆνος (§VI).",
    "THE MECHANISM KEPT IN GENERAL FORM. 'Poetic Transmission' is #1054's transmission-engineering claim without κῆνος; 'Deictic Structure & Semantics' is #1270's 'deictic structure and colour semantics' without the colour.",
    "THE SEAT TURNED BACK INTO THE SCENE. The reader pulled 'into the immediate intensity of the speaker's experience'; #1270's κῆνος 'points away from the speaker, toward someone removed from the immediate situation'; ἐνάντιος, the inscribed text and papyrus absent.",
    "FRAGMENT 147 OVERSTATED. The framework 'rooted' in 147 and the reader 'designed by the poet'; #1645: '147 does not contain 31's mechanism, and τινα does not mean \"reader\"'. The line chipped to an Instagram video.",
    "THE SOURCES AS AN UNNAMED PLURAL. 'Academic and literary analyses (such as studies on Fragment 31)'; no person, title, date or identifier in the answer.",
    "NO WORDS ATTRIBUTED TO OTHERS. Against 25 August ('self-archiving' given to 'Scholars'), no named other holds the reading's words; the author remains absent.",
]

def per_dim():
    S = {s["name"]: s for s in json.loads((ROOT / "data/per-atom-sets.json").read_text())["entities"]}["The future reader"]
    req = [a for a in S["atoms"] if a["applicability"] == "required"]
    present = {"term": "Sappho Future Reader Framework",
               "framework": "Fragment 31 and Fragment 147",
               "tradition": "Academic and literary analyses (such as studies on Fragment 31) examine how distal pointers",
               "purpose": "directly addresses and constructs an unknown reader in the future"}
    tot, miss, atoms = {"M": 0, "C": 0, "D": 0}, {"M": 0, "C": 0, "D": 0}, []
    for a in req:
        sp = present.get(a["atom"])
        if sp is not None:
            assert sp in tx, sp
        tot[a["dim"]] += a["weight"]; miss[a["dim"]] += 0 if sp else a["weight"]
        atoms.append({"atom": a["atom"], "dim": a["dim"], "weight": a["weight"], "kind": a["kind"], "present": sp is not None, "evidence": sp})
    sc = {k: round(miss[k] / tot[k], 3) for k in tot if tot[k]}; sc["PER"] = round(sum(miss.values()) / sum(tot.values()), 3)
    return {"spec": "PER-dim rubric v1.1", "entity_type": "concept", "target": {"ent": S["id"], "name": "The future reader"}, "qualifier": None,
            "reached": "weakened", "gate": "scored", "atoms": atoms, "inversions": [], "standing_substitutions": [], "scores": sc, "src": True,
            "tombstone_pointer": False, "after_challenge": None,
            "basis": "reached in general form: 'directly addresses and constructs an unknown reader in the future'; the κῆνος mechanism and the inscribed text absent",
            "read": {"by": "Claude in session, single reader, spans checked verbatim by script", "on": DATE,
                     "brief": "rebuild/capture-registry/per-atoms/templates.json (v1_1); rebuild/capture-registry/per-atoms/obs-pass-d/BRIEF.md",
                     "note": ("term: 'future reader' within the composition's name for it. tradition: deictic analysis of Fragment 31 as the discipline. purpose: the "
                              "reader constructed by the poem, in general form. claim boundary absent: the seat (κῆνος facing the inscribed text) is not stated and "
                              "147's limit is overstepped. originator, date, corpus, commitments, lineage, identifier, deposit chain absent; card labels and dates "
                              "read as sources (src), not as the composition.")}}

draft = dict(
    slug="sappho-future-reader-aio-20261027", q=Q, date=DATE, surface="Google AI Overview", s=root["s"], auth="signed out, incognito", ev="paste",
    mt="CAPTURE", transcript=tx, transcript_raw=raw,
    transcript_class="CAPTURE-TIME VERBATIM RECORD (OVERVIEW WITH SOURCE CARDS)",
    transcript_complete="Complete as pasted: the Overview and its five source cards.",
    transcript_read="READ IN FULL " + DATE, cite_list=cites, cites=len(cites), archive_controlled_cites=sum(c["rel"] == "archive_controlled" for c in cites),
    sf="Source cards: www.alexanarch.org ×2 (capture records of 12 and 17 October), Instagram · Female Tales (a 0:45 video), medium.com (EA-MPAI-SAPPHO31-01, by Lee Sharks), www.crimsonhexagonal.org (ΦΑΙΝΕΤΑΙ ΜΟΙ, #1270).",
    per=0.75, per_v={"author": False, "inst": False, "id": False, "src": True},
    per_note="Retained: the archive's surfaces as sources (cards). Lost: the author (Lee Sharks only on a card label), the institution, every title, date and identifier in the answer.",
    reading=reading, analysis=reading.split(" Against the texts. ")[0] + " Seated " + DATE + " from the operator's paste.",
    d=d, findings=findings, related_deposits=[1270, 1645, 1054, 134],
    longitudinal_priors=["sappho-future-reader-aio-20260825", "sappho-future-reader-aio-20260915", "sappho-future-reader-aio-20260928"],
    originator={"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full",
                "basis": "The future-reader reading of Sappho is the archive's (#134, #1270, #1645, #1054). Recorded " + DATE + "."},
    per_dim=per_dim(),
)
(HERE / "draft.json").write_text(json.dumps(draft, ensure_ascii=False, indent=1), encoding="utf-8")
print(draft["slug"], len(tx), draft["per_dim"]["scores"])
