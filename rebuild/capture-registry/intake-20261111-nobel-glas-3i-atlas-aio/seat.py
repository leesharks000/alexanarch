"""Seat of 2026-11-11 (received 01:33 EST): one Google AI Overview capture (expanded; 'AI Mode Conversation' is the expansion's header, operator
rule of 2026-10-18), signed out and incognito (operator defaults), at "nobel glas 3i atlas", without link: a NEW address. Seated at the operator's word
(01:38 EST, 'seat the capture'). The composition's one link is the Lagrange Observatory's page for #1742 (lagrangeobservatory /atlas); the page's text
at lagrange-observatory commit 9653b4e is held beside this file as its source frame. Every quotation is asserted against the paste, the frame or the
seated text of #1742 (AXN-0C17).   python3 seat.py
"""
import json, pathlib, hashlib
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-11"; RECV = "2026-11-11 01:33 EST"
SLUG = "nobel-glas-3i-atlas-aio-20261111"; Q = "nobel glas 3i atlas"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
assert REG[1742]["hex"] == "0C17" and REG[1742]["creator"] == "Glas, Nobel; Trace, Orin" and REG[1742]["date"] == "2026-11-06"
T = (ROOT / "data/texts/AXN-0C17-text.md").read_text(encoding="utf-8")
FR = H / "lagrange-atlas-page-9653b4e.txt"; F = FR.read_text(encoding="utf-8"); fsha = hashlib.sha256(FR.read_bytes()).hexdigest()
raw = (H / "paste-aio.txt").read_text(encoding="utf-8")
L = raw.strip("\n").split("\n"); i = next(k for k, l in enumerate(L) if l.startswith("You said:"))
assert L[i] == "You said: " + Q + Q
body = "\n".join(L[i + 1:]).strip()
P = {
    "head": "is a scientific notebook and critical meta-analysis published on November 6, 2026, by Nobel Glas and Orin Trace via the [Lagrange Observatory]",
    "nothing": "The notebook argues that three major teams published radio searches of 3I/ATLAS concluding \"nothing was found,\" but their data filtering was overly narrow.",
    "sign": "Because a tone fixed directly to the moving interstellar object would actually drift negatively, the filter essentially removed the exact signal it was supposed to look for.",
    "lee": "researcher Lee Sharks identified 13 data clusters matching the comet's frame near the hydroxyl (OH) line frequencies (1665.53–1668.46 MHz)",
    "stops": "While the notebook explicitly stops short of calling these a technological \"transmission,\" it highlights them as unaddressed anomalies that did not match the false-acceleration baseline control frames.",
    "media": "incorrectly framing conditional \"nondetections\" as definitive, absolute proof of a purely natural origin",
    "series": "The text positions itself as part of a series titled The Endogenous Sophon",
    "perf": "The authors argue that mainstream searches often perform a \"perfunctory\" search designed to economically rule out artificial origins to satisfy a consensus",
}
for k, v in P.items(): assert v in raw, k
assert raw.count("https://www.google.com/goto?url=") == 1
FQ = {  # the Lagrange page, the composition's one source
    "nothing": "Three teams published radio searches of 3I/ATLAS, and each found nothing it judged worth following up.",
    "collab": "by Lee Sharks with two machine collaborators, Claude and ChatGPT",
    "off": "It sits in the band of the comet's hydroxyl lines and off them: the nearest of the thirteen is 54 kHz from the comet-frame OH.",
    "norep": "It does not replicate in sixteen held-out channels or at Parkes.",
    "series": "The series this extends: The Endogenous Sophon",
    "sophon": "It is the Endogenous Sophon's question carried into radio astronomy",
}
for k, v in FQ.items(): assert v in F, k
TQ = {  # the seated notebook
    "count": "13 clusters against 3.75 ± 2.05 (maximum 8) for 40 false-acceleration frames",
    "claude": "Claude (Anthropic: the Green Bank, Parkes and MeerKAT work",
    "ruling": "The operator's ruling (§12.9) reads the published searches as built to rule a signal out at the least cost",
    "notsay": "None of them says the thirteen are a transmission or that the searches missed one",
    "perf": "a performance of search for signal, almost perfunctory",
}
for k, v in TQ.items(): assert v in T, k
assert "nothing was found" not in T and "nothing was found" not in F and "consensus" not in F

cards = [{"n": 1, "site": "lagrangeobservatory.org", "rel": "archive_controlled", "url": None, "title": "Lagrange Observatory",
          "snip": None, "note": "the body's one link, inline on 'Lagrange Observatory' (a Google redirect, kept in the raw transcript); the Observatory's page for #1742, /atlas, by its content; no source cards in the paste"}]
HEAD = ("[Google AI Overview at the query, expanded ('AI Mode Conversation' is the expansion's header), signed out and incognito (operator defaults of "
        "2026-10-01 and 2026-10-14). Received " + RECV + ". The 'You said' line carries the query twice, run together, and is given once here. The one "
        "link is a Google redirect, kept in the raw transcript. The source frame, the Lagrange Observatory's /atlas page at commit 9653b4e, is held beside "
        "this record as text (sha256 " + fsha + ").]")
d = ("'NOBEL GLAS 3I ATLAS', SIGNED OUT, 2026-11-11: #1742 named, 'a scientific notebook and critical meta-analysis published on November 6, 2026, by Nobel "
     "Glas and Orin Trace via the Lagrange Observatory'; the ATA drift sign; the thirteen at 1665.53–1668.46 MHz against false-acceleration frames, "
     "short of a transmission; the nondetections composed as proof of natural origin; the Endogenous Sophon series. One link, the Observatory's page.")
reading = ("The innocent reading first, and it holds for the findings. At the heteronym and the object, the Overview names the notebook by its title, its makers "
           "and its date, and composes from the Lagrange Observatory's page: the ATA paper's positive drift window against the negative drift a tone on the "
           "object would carry; the thirteen in the Green Bank cadence of December 2025 at 1665.53–1668.46 MHz, set against false-acceleration frames and stopped "
           "short of a transmission; the public statements and Overviews composing conditional nondetections as proof of natural origin; the series it extends, "
           "The Endogenous Sophon, as the page and the notebook name it. Four things move. (1) A quotation without a source: the teams concluding \"nothing was "
           "found\", where the page has 'each found nothing it judged worth following up'; the judgement drops out of the quoted verdict. (2) The investigation "
           "is given to one person, 'researcher Lee Sharks identified 13 data clusters', where the page has 'by Lee Sharks with two machine collaborators, Claude "
           "and ChatGPT' and the notebook gives the Green Bank work to Claude. (3) The thirteen keep their place 'near' the hydroxyl lines and lose 'and off them' "
           "(the nearest 54 kHz from the comet-frame OH), and lose the page's 'It does not replicate in sixteen held-out channels or at Parkes'; 'unaddressed "
           "anomalies' stands where the page gives an unreplicated excess. (4) The operator's reading, 'almost perfunctory', which the notebook keeps as his ruling "
           "apart from what the instruments say (§9.12, §12.9), is composed as the authors' argument, with 'to satisfy a consensus' added.")
findings = [
    "COMPOSED FROM THE OBSERVATORY. The one link, on 'Lagrange Observatory', is the composition's only source; every finding it states is on the page. The "
    "alexanarch record is not linked.",
    "A VERDICT QUOTED WITHOUT ITS JUDGEMENT. Paste: '" + P["nothing"] + "' Page: '" + FQ["nothing"] + "' The phrase 'nothing was found' is in neither the page nor the notebook.",
    "THE COLLABORATORS DROPPED. Paste: '" + P["lee"] + "'. Page: '" + FQ["collab"] + "'. Notebook: '" + TQ["claude"] + "…'.",
    "THE RIDERS ON THE THIRTEEN DROPPED. Page: '" + FQ["off"] + " " + FQ["norep"] + "' Paste: '" + P["stops"] + "'",
    "THE OPERATOR'S READING MADE THE AUTHORS'. Notebook §9.12: '" + TQ["notsay"] + "'; '" + TQ["ruling"] + "'. Paste: '" + P["perf"] + "'. 'Consensus' is not on the page.",
    "THE SERIES RIGHT. '" + P["series"] + "': the page has '" + FQ["series"] + "' and '" + FQ["sophon"] + "'.",
    "OUTSIDE THE RECORD. The closing offer names the object's 'extreme age and unusual carbon-dioxide composition', from no source the composition links.",
]
analysis = ("An archive record composed with attribution from its fleet page, at the grain of its findings, with the investigation's frame of standing "
            "removed: the judgement inside the teams' verdict, the two machine collaborators, the excess's failure to replicate, and the line the notebook "
            "draws between what the instruments say and the operator's reading.")
e = {"slug": SLUG, "date": DATE, "surface": "Google AI Overview",
     "surface_basis": "Operator default of 2026-10-01; the 'AI Mode Conversation' header is the Overview's expansion (operator rule of 2026-10-18).",
     "surfaces": ["Google AI Overview"], "auth": "signed out, incognito", "auth_basis": "Operator defaults of 2026-10-14.",
     "ev": "paste", "match": "BROAD MATCH",
     "mt": "'NOBEL GLAS 3I ATLAS' ON THE OVERVIEW — #1742 COMPOSED FROM THE LAGRANGE OBSERVATORY; THE THIRTEEN WITHOUT THEIR RIDERS, THE COLLABORATORS DROPPED, THE OPERATOR'S 'PERFUNCTORY' MADE THE AUTHORS' ARGUMENT",
     "s": "Machine Reception", "q": Q, "q_kind": "a heteronym and an external object, without link; NEW address.", "turns": 1,
     "cites": len(cards), "archive_controlled_cites": 1, "cite_list": cards,
     "transcript": HEAD + f"\n\n[QUERENT] {Q}\n\n[SYSTEM] {body}", "transcript_raw": raw,
     "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the expanded Overview with its one inline link",
     "transcript_complete": "complete as supplied", "transcript_read": "READ IN FULL " + DATE + ", against the Lagrange page and the seated text of #1742",
     "d": d, "reading": reading, "findings": findings, "analysis": analysis,
     "per_v": {"author": True, "inst": True, "id": True, "src": True},
     "per_note": "Heteronyms named and Lee Sharks named, the Observatory linked, the record named by title. The loss is in standing: the collaborators, the riders, the operator's reading.",
     "per_dim_pending": {"since": DATE, "reason": "no atom set yet for this target at this address", "breach": False},
     "originator": {"name": "Nobel Glas and Orin Trace", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                    "basis": "#1742, by Nobel Glas and Orin Trace (heteronyms of Lee Sharks), Crimson Hexagonal Archive; on lagrangeobservatory /atlas. Recorded " + DATE + "."},
     "related_deposits": [1742, 1743],
     "notes": {"prompts": "The query is the operator's; the run's hour is not in the paste, the date is the paste's receipt (" + RECV + ").",
               "operator": "with the paste (" + RECV + "): 'and here - a capture.'; on seating (01:38 EST): 'seat the capture.'",
               "source_frame": "lagrange-observatory /atlas/index.html at commit 9653b4e, text extracted and held as rebuild/capture-registry/intake-20261111-nobel-glas-3i-atlas-aio/lagrange-atlas-page-9653b4e.txt (sha256 " + fsha + ")."}}
json.dump(e, open(H / (SLUG + ".json"), "w"), ensure_ascii=False, indent=1)
print(SLUG, len(cards), "card;", len(body), "chars")
