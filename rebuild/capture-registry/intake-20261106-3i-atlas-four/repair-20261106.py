"""Capture repair of 2026-11-06, on the NonWiki composers' reports for the rows avi-loeb-3i-atlas, ata-3i-atlas-search and 3i-atlas-1665-1668-mhz,
each point checked against the saved sources (datasets/negative-of-the-negative/v2/intake/<row>/, rebuild/3i-atlas-signal-search/sources/,
rebuild/capture-registry/intake-20261102-loeb-3i-atlas/). Edits in place; every replaced string asserted present once.   python3 repair-20261106.py"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]; F = ROOT / "data/EA-WG-CAPTURES-01.json"
raw = F.read_text(encoding="utf-8"); C = json.loads(raw); caps = C.get("captures") or C.get("entries") or C
M = {x["slug"]: x for x in caps}
I = ROOT / "datasets/negative-of-the-negative/v2/intake"
src = lambda p: (I / p).read_text(encoding="utf-8")
def rep(slug, field, old, new, idx=None):
    x = M[slug]; v = x[field] if idx is None else x[field][idx]
    assert v.count(old) == 1, (slug, field, idx, old[:50]); v = v.replace(old, new)
    if idx is None: x[field] = v
    else: x[field][idx] = v
B6, B7, B2 = src("ata-3i-atlas-search-20261106/B6.txt"), src("ata-3i-atlas-search-20261106/B7.txt"), src("ata-3i-atlas-search-20261106/B2.txt")
S6 = "All traced back to technology on the surface of the Earth or our own Earth-orbiting satellites."
S7 = "The observations place upper limits on the power of any radio transmitter on or near 3I/ATLAS, ruling out signals stronger than about 10-110 W — approximately the power of a household appliance — over the detected frequencies."
DB = "After drift-rate blanking, ∼2 million hits remained."
F3 = "reducing the total number of hits by 97.4%"
assert S6 in B6 and S7 in B6 and DB in B2 and F3 in B2
A = "ata-3i-atlas-technosignature-search-paper-aio-20261106"
rep(A, "findings", "The Overview's 'traced back to local human-made Earth technology, satellites' goes a step further than the published sentence, naming the kinds of source for every event.",
    "The step past the paper's classification is the press's: the Sci.News card reads '" + S6 + "', and the Space card carries the same wording. The Overview copies it into the paper's account (repaired 2026-11-06 on the ata-3i-atlas-search composer's report).", 1)
rep(A, "findings", "to the frequencies and drift rates its survey kept.",
    "to the frequencies and drift rates its survey kept. The composition's sentence takes the SETI Institute's statement as the Sci.News and Space cards carry it ('" + S7 + "'), drops its closing 'over the detected frequencies' and adds 'active' (repaired 2026-11-06).", 2)
rep(A, "findings", "The signed drift interval is folded into 'drift-rate blanking', so the stage the notebook questions has no name in the composition.",
    "'Drift-rate blanking' is the paper's own term ('" + DB + "'), and the paper's own summary sentences leave the signed interval unnamed as well; the composition carries that naming, and the stage the notebook questions has no sign in either (repaired 2026-11-06).", 4)
D = "3i-atlas-ata-drift-rate-filter-aio-20261104"
rep(D, "reading", "and the reduction in hits, which matches the press (Astrobiology Web: 'reducing the total number of hits by 97.4%').",
    "and the reduction in hits, which matches the paper's own Figure 3 caption ('" + F3 + "'), carried by the press (Astrobiology Web; repaired 2026-11-06).")
rep(D, "findings", "The figure agrees with the press account's 'reducing the total number of hits by 97.4%'.",
    "The figure agrees with the paper's Figure 3 caption ('" + F3 + "'), which the press account repeats (repaired 2026-11-06).", 3)
L = "avi-loeb-3i-atlas-aio-20261102"
SC = (ROOT / "rebuild/3i-atlas-signal-search/sources/arxiv-2508.09167.txt").read_text(encoding="utf-8")
rep(L, "findings", "The ranking dates from November 2025 and is restated after the concession.",
    "The ranking dates from August 2025 (the Loeb Scale paper, arXiv:2508.09167, submitted 6 August 2025, places 3I/ATLAS at Level 4) and is restated after the concession (repaired 2026-11-06 on the avi-loeb-3i-atlas composer's report).", 0)
rep(L, "findings", "each anomaly is set beside a 'potential techno-signature'",
    "the anomalies are set beside a 'Potential techno-signature' or a 'Possible techno-signature', one beside a 'Potential bio-signature' (repaired 2026-11-06)", 3)
rep(L, "findings", "(PER-D in #1469's sense: purpose and commitments)", "(PER-D under rubric v1.1, purpose and commitments, #1694 §3.9; #1469 defines the deep dimension otherwise; repaired 2026-11-06)", 4)
rep(L, "mt", "HIS OWN LATER ESSAYS, LEVEL 4 KEPT, CARDED AND UNUSED", "HIS OWN LATER ESSAY CARDED AND UNUSED; LEVEL 4 IN THE APRIL ESSAY AND THE SCALE PAPER")
x = M[L]; x["notes"]["source_frame"] = x["notes"]["source_frame"].replace("The Level 4 ranking's first date (November 2025) is from press reports:", "Press reports of the Level 4 ranking (its first date is August 2025, the scale paper; repaired 2026-11-06):")
assert "places 3I/ATLAS" in SC or "3I/ATLAS" in SC
H = "3i-atlas-1667-mhz-aio-20261106"; B4 = src("3i-atlas-1665-1668-mhz-20261106/B4.txt")
BL = "No artificial radio emission was detected at a limit of 0.17 W over the 900 - 1670 MHz range"
assert BL in B4
rep(H, "per_note", "Lost: the authors;", "Lost: the authors, against the reference pool only (no readable card of T names the team; the ADS card refused the fetch);")
rep(H, "findings", "the Reddit thread's 'tracking with the comet's trajectory' included.", "the composition's own account of the Reddit discussion ('tracking with the comet's trajectory', T's wording) included.", 3)
rep(H, "findings", "(about 11–12 mJy)').", "(about 11–12 mJy), near the October strength of the deeper line'). The composition's 'emission/absorption' carries a detection (emission, ATel #17499) on no card of T (repaired 2026-11-06).", 2)
M[H]["findings"].insert(4, "THE ONE SEARCH ON THE RAIL THAT COVERS THE BAND, LEFT OUT (added 2026-11-06 on the 3i-atlas-1665-1668-mhz composer's report). The Breakthrough Listen card (card 4) reports MeerKAT's BLUSE search: '" + BL + "'. Its range contains the band; the composition, which enlists Green Bank and the ATA for the line, leaves out the one result on its own rail that bears on transmitters at 1667 MHz.")
F.write_text(json.dumps(C, ensure_ascii=False, indent=1 if raw.startswith('{\n "') else (2 if raw.startswith('{\n  "') else None)) if raw.startswith('{\n') else json.dumps(C, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print("repaired")
