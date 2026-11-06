#!/usr/bin/env python3
"""Factual repairs of #1743 (v1.0 -> v1.1) and #1742 (v1.1 -> v1.2), at the operator's word of 2026-11-06 11:07 EST
("so we need factual repairs versioned in place"). Each point is a composer's finding checked against its source:
ATel #17499 (Pisano et al., posted 2025-11-18) for MeerKAT's OH absorption (from 24 October, ATel #17473; 5 and 6 November),
its emission (11 and 12 November) and its technosignature limit ("a detection limit of 0.17 W over the 900-1670 MHz range");
Loeb's essay of 2026-04-23 for probabilities given to four of the anomalies; #1694 §3.9 for PER-D. Each edit is asserted once."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
def apply(path, pairs):
    p = ROOT / path; s = p.read_text(encoding="utf-8")
    for a, b in pairs:
        n = s.count(a); assert n == 1, (path, a[:80], n); s = s.replace(a, b)
    p.write_text(s, encoding="utf-8"); print(path, len(pairs), "edits")
ATEL = "ATel #17499"
apply("drafts/3I-ATLAS-PUBLIC-draft-2026-11-06.md", [
 ("Lee Sharks · Semantic Economy Institute · Crimson Hexagonal Archive · 6 November 2026\n",
  "Lee Sharks · Semantic Economy Institute · Crimson Hexagonal Archive · 6 November 2026 · version 1.1, in place the same day\n"),
 ("where he set out the anomalies one by one, each with a probability (",
  "where he set out the anomalies one by one, with a probability for four of them ("),
 ("Three teams published radio searches of 3I/ATLAS: the Allen Telescope Array in California (Sheikh et al., arXiv:2512.18142), the Green Bank Telescope in West Virginia (arXiv:2512.19763) and China's FAST. All three found nothing they judged worth following up.",
  "Four teams published radio searches of 3I/ATLAS: the Allen Telescope Array in California (Sheikh et al., arXiv:2512.18142), the Green Bank Telescope in West Virginia (arXiv:2512.19763), China's FAST, and MeerKAT in South Africa with Breakthrough Listen, which reported \"a detection limit of 0.17 W over the 900-1670 MHz range\" and put all 23,689 of its signals down to human interference (" + ATEL + ", 18 November 2025). All four found nothing they judged worth following up."),
 ("near a frequency where comets naturally glow (the hydroxyl line).",
  "near the hydroxyl line, where comets absorb and emit radio light (MeerKAT recorded 3I/ATLAS's hydroxyl in absorption from 24 October 2025 and in emission on 11 and 12 November, " + ATEL + ")."),
 ("The comet's own hydroxyl emission would sit within about 11 kHz of known frequencies;",
  "The comet's own hydroxyl line, in absorption or in emission, would sit within about 11 kHz of known frequencies;"),
 ("All three searches find hits one look at a time, above a threshold,",
  "The ATA, Green Bank and FAST searches find hits one look at a time, above a threshold,"),
])
s = (ROOT / "drafts/3I-ATLAS-PUBLIC-draft-2026-11-06.md").read_text(encoding="utf-8").rstrip("\n")
s += ("\n\n*Version 1.1 (6 November 2026), in place of version 1.0 the same day, on three factual repairs, each checked against its source. MeerKAT's search, a fourth, "
      "is added beside the three: its limit, 0.17 W over 900 to 1670 MHz (" + ATEL + "), sits above the strength of the thirteen. The hydroxyl line is described as "
      "the comet's absorption and emission: MeerKAT's first detections of 3I/ATLAS were in absorption, and its emission came in November. Loeb's April essay gives "
      "probabilities for four of the anomalies, where version 1.0 said each.*\n")
(ROOT / "drafts/3I-ATLAS-PUBLIC-draft-2026-11-06.md").write_text(s, encoding="utf-8")
apply("drafts/3I-ATLAS-SIGNAL-SEARCH-draft-2026-11-03.md", [
 ("EA-3I-ATLAS-NOTEBOOK-01 v1.1 · Nobel Glas · Orin Trace · Transactions on Substrate Engineering · notebook · 2026-11-06, versioned in place the same day",
  "EA-3I-ATLAS-NOTEBOOK-01 v1.2 · Nobel Glas · Orin Trace · Transactions on Substrate Engineering · notebook · 2026-11-06, versioned in place twice the same day"),
 (' "version": "1.1",\n "datePublished"', ' "version": "1.2",\n "datePublished"'),
 ('"spxi:pillarStatus": "v1.1, deposited 2026-11-06 at the operator\'s word and versioned in place the same day (the operator\'s point, §12.9, and §9.12 under it);',
  '"spxi:pillarStatus": "v1.2, deposited 2026-11-06 at the operator\'s word and versioned in place twice the same day (the operator\'s point, §12.9, and §9.12 under it; then the factual repairs of §13.7);'),
 ('the public piece\'s number (#1743) and the pages on lagrangeobservatory.org, provenanceerasure.org and semanticeconomy.org"\n  }\n ],',
  'the public piece\'s number (#1743) and the pages on lagrangeobservatory.org, provenanceerasure.org and semanticeconomy.org"\n  },\n  {\n   "version": "1.2",\n   "date": "2026-11-06",\n   "note": "versioned in place: factual repairs (§13.7): MeerKAT\'s search added as a fourth (ATel #17499, 0.17 W over 900-1670 MHz); probabilities for four of Loeb\'s anomalies; PER-D under rubric v1.1 (#1694 §3.9)"\n  }\n ],'),
 ("set against three published radio searches (§9.3–9.6)", "set against four published radio searches (§9.3–9.6)"),
 ("lists the anomalies by theme with a probability for each (", "lists the anomalies by theme, with a probability for four of them ("),
 ("2.1 Two teams published radio searches: the Allen Telescope Array (Sheikh et al., arXiv:2512.18142v2, accepted manuscript of 2026-05-20) and Green Bank (arXiv:2512.19763v1, observations of 2025-12-18). FAST published a third in 1.05–1.45 GHz.",
  "2.1 Four teams published radio searches: the Allen Telescope Array (Sheikh et al., arXiv:2512.18142v2, accepted manuscript of 2026-05-20), Green Bank (arXiv:2512.19763v1, observations of 2025-12-18), FAST in 1.05–1.45 GHz (arXiv:2603.19023), and MeerKAT with Breakthrough Listen (" + ATEL + ", posted 2025-11-18). MeerKAT's two narrowband searches of 2025-11-05 set \"a detection limit of 0.17 W over the 900-1670 MHz range\"; its 23,689 signals were judged not \"spatially consistent\" with the object and \"likely caused by anthropogenic radio frequency interference (RFI)\". The thirteen (C03 about 26 mW nominal, §13.2) sit below that limit as below the others (§9.3)."),
 ("The three published searches characterize their acceptance in part: frequencies, drift intervals, thresholds and power limits are stated (the ATA's 10–110 W, Green Bank's 100 mW).",
  "The published searches (§2.1) characterize their acceptance in part: frequencies, drift intervals, thresholds and power limits are stated (the ATA's 10–110 W, Green Bank's 100 mW, MeerKAT's 0.17 W)."),
 ("9.6 Correlated blind spots (#1450 §2.3). The three published searches share one approach:",
  "9.6 Correlated blind spots (#1450 §2.3). The ATA, Green Bank and FAST searches share one approach:"),
 ("so redundancy among them adds little below the shared floor.",
  "so redundancy among them adds little below the shared floor. MeerKAT's (§2.1) also counts hits above a limit and judges them by their position, on what its telegram states."),
 ("(PER-D in #1469's sense)", "(PER-D under rubric v1.1, #1694 §3.9)"),
])
s = (ROOT / "drafts/3I-ATLAS-SIGNAL-SEARCH-draft-2026-11-03.md").read_text(encoding="utf-8")
a = s.index("13.6 Version 1.1 (2026-11-06)"); b = s.index("\n", a)
s = s[:b] + ("\n\n13.7 Version 1.2 (2026-11-06), in place of v1.1 the same day, on the composers' findings for the /non rows, each checked against its source (the operator's word, 11:07: \"so we need factual repairs versioned in place\"). MeerKAT's technosignature search, reported in " + ATEL
  + ", is added as a fourth published search (§2.1, §9.3, §9.6): its limit, 0.17 W over 900–1670 MHz, sits above the thirteen as Green Bank's does. Loeb's essay of 2026-04-23 gives probabilities for four of the anomalies, where §1.3 said each. PER-D is cited under rubric v1.1 (#1694 §3.9), where §9.10 cited #1469. The SPXI packet's version, status and history are brought to v1.2.") + s[b:]
(ROOT / "drafts/3I-ATLAS-SIGNAL-SEARCH-draft-2026-11-03.md").write_text(s, encoding="utf-8"); print("13.7 added")
