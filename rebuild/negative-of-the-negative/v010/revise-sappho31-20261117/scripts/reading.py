"""Write traversal/reading-20261117.json: the reading of the D/R/O rerun's candidates in deposits new to the pass, and of the
Capture Registry's Sappho captures since 2026-10-07, with admission verdicts and reasons (§3.4).   /tmp/py312/python3 reading.py"""
import json
from vlib import *
import claims_new as C
adm = {}
for c in C.A:
    adm.setdefault(c["dep"], []).append(c["id"])
brief = {1781: "named by the brief; the reading's current text", 1752: "named by the brief", 1756: "named by the brief", 1774: "named by the brief (the decline and its record)", 1783: "named by the brief (I.4a–I.4b)"}
rerun = {1779: ("D", "EA-MPAI-SAPPHO31-01 v1.1: the incompatibility restated at five features, superseding #1054 (cand D1754, D1757)"),
         1749: ("D", "Closing the Fragment v10: the composition layer's closure of the poem on 'But I must dare all.' (cand D1460)"),
         1748: ("R", "EA-CORPORA-36: the seating of the jealousy reading's sources, Hermann 1816 (cand D1415)"),
         1058: ("R", "an archive poem stated as the papyrus-grass equivalent of fr. 31's catalogue (cand D0750)"),
         1670: ("D", "the Carson mantle object: Carson does not make the future-reader reading (cand D1336)"),
         1766: ("O", "Critique of Pure Inference §0.3: Hermann's rewriting as its case of a reading after the inference (cand D1656)"),
         1048: ("D", "the stable formulation's sentence, which #436's re-seated text no longer carries (A436-01's quote, found in AXN-0424)")}
not_adm = {
    1409: "names #1054 as an instrument; no claim on the poem", 1680: "lists #1270 among the academy's entry loci; no claim on the poem",
    1684: "the prediction index counts statements on κῆνος (28) and lists prediction pages; a fact about the archive's predictions, not the poem; its loci are the papers already admitted",
    1687: "the seat map: the Sappho Room's page holds fr. 31; a fact about the room", 1704: "the /non introduction uses this row as its example; the row's own reception",
    1711: "the originals library: 'no papyrus witness exists for fr. 31' (01/10), the lineage of the sole witness (#1052), adding nothing (S4)",
    1713: "a seating cross-reference to the seat of fr. 31", 1714: "the 27 October ChatGPT capture's bar on one side, carried as CAP-7 from the registry",
    1719: "the Oracle kernel calibrated on Sappho 31; a fact about the instrument", 1722: "lists captures at the #1484 address",
    1738: "the seating of Sappho whole; the seat, not a claim on fr. 31", 1750: "the open letter cites the 7 November Overview (CAP-4's address); carried from the registry",
    1755: "Revelation First hologram: the operator T running from Sappho 31; lineage of #1484/#1494 already admitted",
    1757: "Historical Logos hologram: the chain from Sappho 31 and the three seats; lineages of #1484 and #1756 admitted",
    1758: "Philo and the channel of Sappho 31 (#1484, #1494, #1511); lineage admitted", 1762: "Gellius's Valerius Aedituus as a Latin Sappho 31; lineage of #1532 (A1532-07)",
    1765: "the Slavonic Josephus and si fas est; lineage of #626 (A626-01)", 1769: "Daffodils: 'The jealousy reading of Sappho 31 is such a construction (#1752)'; lineage of #1752",
    1770: "Who Speaks for the Classics §5.3.3: the jealousy reading's making as #1752 gives it; lineage of #1752, cited by #1783 I.4b",
    1774: None,
    1775: "ΦΑΙΝΕΤΑΙ ΜΟΙ v2.4, an instance of #1781's lineage (superseded); grouped", 1777: "v2.5, instance (superseded); grouped", 1778: "v2.6, instance (superseded); grouped", 1780: "v2.7, instance (superseded); grouped",
    1696: "superseded instance of #1697", 1697: "Opening the Encyclopedia: names Sappho 31 among examples", 1709: "superseded instance of #1711", 1721: "superseded instance of #1722",
    1761: "superseded instance of #1765", 1763: "superseded instance of #1765", 1764: "superseded instance of #1765"}
out = {"row": "sappho-31", "pass": "second reading, 2026-11-17 (revision)", "procedure": "EA-NEGONT-02 v0.10 §3.4 D/R/O, the row's config unchanged; admission by reading at loci; volume never a ground of removal; instances of one work grouped (S4)",
       "reader": "Claude (Opus 5.5), subagent, 2026-11-17", "candidates_dir": "traversal/ (candidates-D.jsonl, -R, -O, summary.json; H not run)",
       "admitted": [{"dep": d, "strata": sorted({s for c in C.A if c["dep"] == d for s in c["strata"]}), "claims": ids,
                     "reason": brief.get(d) or rerun.get(d, ("", ""))[1]} for d, ids in adm.items()],
       "not_admitted": [{"dep": d, "reason": r} for d, r in not_adm.items() if r],
       "captures_admitted": [{"slug": s, "findings": ix, "claims": [c["id"] for c in C.ALL if c["dep"] == "capture-registry" and c["locus"].startswith(s + ",")]} for s, ix, _ in C.CAPS],
       "captures_not_admitted": [{"slug": s, "reason": r} for s, r in C.NOT_ADMITTED_CAPS.items()]}
(STAGE / "traversal/reading-20261117.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out["admitted"]), len(out["not_admitted"]), len(out["captures_admitted"]), len(out["captures_not_admitted"]))
