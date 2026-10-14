import json, pathlib
H = pathlib.Path(__file__).resolve().parent
allc = {int(k): v for k, v in json.load(open(H.parent / "allcands.json")).items()}
boil = set(json.load(open(H.parent / "boil2.json")))
L = json.load(open(H / "ledger.json"))
REASON = {
 660: "EA-SPXI-01, the formal specification, read whole: definition, packet, disambiguation matrix, the April permanence claim and the reference implementation.",
 62: "The protocol/ETF disambiguation packet, read whole: two unrelated entities share the string; the ETF's objective (−1×).",
 63: "The entity-definition MPAI v1.1: distinct from the ETF, the index, SSPX, SEO/GEO.",
 61: "EA-SPXI-14, the nested-layer relation SPXI ⊇ GEO (April).", 661: "EA-SPXI-09 and its amendment of 18 April: the false symmetry corrected, the April text preserved.",
 1055: "SPXI ≠ GEO, composer-side against reception-side: 'cannot coexist'. Carried as contested against ⊇ GEO.",
 1541: "The SPXI–GEO sequence stated as precedent: non-equivalence, then a typed relation scoped to method inventory.",
 172: "Case 4, SPXI → GEO (April), and the boundary that must be drawn to be kept.", 1090: "SPXI read as disambiguation before the fact.",
 1654: "SPXI ≠ AEO v0.3, read whole: the success condition (discernment), its entity-level form (reading the disambiguation), the carrier rule.",
 72: "SPXI for Websites v4.0, the standing protocol (founding deposit of spxi.dev).", 705: "The SPXI-Sitemap Protocol, method 4.1 of the inventory.",
 673: "JSON-LD as one surface of SPXI.", 755: "SPXI Protocol v0.2: v0.1 superseded as normative signaling; protection only against cooperative readers.",
 204: "The self-audit block.", 143: "The conformance instrument.", 118: "SIM, the typed-metadata layer.", 127: "SPXI-TLP: provenance in body text.",
 173: "The Retrieval Settlement Fortification Protocol, a standing SPXI protocol.", 1: "Zenodotus' Book-Burning: SPXI defined as a provenance-kernel format.",
 1537: "OPB-01: without C₀ the acting part is unknown; SPXI as a disclosure-and-attestation layer.", 1538: "The Zenodo moderation map: TLP does not protect an account from ownership-based deletion.",
 158: "Semantic Exhaustion: deposit discipline addresses retrieval, not yet composition.", 1609: "The recoding of a distinction: entrance cannot be attributed to SPXI.",
 1423: "The Capture Registry paper: SPXI-treated captures show the predicted differential. Contested by #1609 and #1537.",
 834: "Algorithmic Publishing: SPXI treatment and uptake. Contested by #1609.", 833: "The founding dataset's capture 67, 'spxi protocol' (13 June).",
 881: "Surface Visibility Baseline: SPXI's cross-surface profile (22 June).", 1470: "One Transcript, Whole Stack: the 14 August spans ('not an established industry standard'; the offer to implement).",
 1469: "The Three Dimensions of Provenance Erasure: the address of the 14 August event (ChatGPT, unprimed, logged out).",
 1462: "Semantic Rent, Measured: the SPXI event of 14 August.", 1638: "The Trusted Intermediary, read at its abstract and specimen table.",
 1471: "The Disclosure Battery: the bare form collides with the ETF.", 1643: "AI Fucking Lies: no measured return; figures withdrawn.",
 665: "The April ROI addendum, superseded in source by the 19 September withdrawal.", 680: "A model's knowledge of SPXI traced to a Zenodo deposit.",
 84: "OCTANG-002: carried for the archive's own variant expansion of spxi.dev, marked internally inconsistent. The third party's name is not carried.",
 1631: "Monetary Dark Matter: author, institution, source and identifier survive at different rates.", 1608: "The machine valuation (attributed).",
 64: "The Retrieval Settlement: SPXI as the counter-practice.", 1084: "The Semantic Addresses Framework: SPXI encodes what a work is.",
 1611: "The Negative of the Negative notebook: AXN descends from SPXI.", 1432: "AXN-SYMBOLON-SPEC: SPXI and the symbolon complementary.",
 119: "The Restored Academy MPAI: SPXI in Categories I and II.", 835: "The Conveyor Belt: provenance in body text.", 193: "The Ruby Moot: the negative tag as overruling.",
 684: "After Syntax: SPXI a persistence layer.", 68: "The Secret Name: SPXI against commercial flattening.", 683: "The Secret Book of Walt: the Unicorn Horn identified with SPXI.",
 858: "Scholarly Legwork: SPXI the technical implementation of the inscription prayer.", 791: "Meaning Feudalism: the subordination prediction.",
 106: "Semantic Physics: SPXI as operative semantic physics.", 70: "The Periwinkle Septagon: SPXI within a restricted economy.",
 1550: "Grundrisse X-036: SPXI as a theory of entity density (hypothesis).", 670: "SPXI as Concept: the Deleuzian reading.",
 662: "Supraliminal Transmission.", 695: "The Writable Retrieval Basin: SPXI deepens the basin.", 130: "Cumulating Evolutionary Volatility: infrastructural logic.",
 761: "The Wikidata Node Registry: the item SPXI Protocol.", 1409: "EA-SPXI-ANALOG-01, the analog extension.",
}
LIN = [
 ("the entity-definition MPAI", [63, 976, 1256], 63), ("SPXI as concept", [670, 671], 670), ("the April ROI addendum", [665, 977, 1353], 665),
 ("SPXI ≠ AEO", [1648, 1654, 1649, 1655], 1648), ("semantic rent at SPXI", [1462, 1463, 1464, 1465, 1467, 1469, 1470, 1479, 1480], 1462),
 ("the machine valuation", [1607, 1608], 1607), ("surface visibility", [881, 880, 882, 883, 884], 880), ("algorithmic publishing", [834, 1228], 834),
 ("the capture registry snapshots of 'spxi protocol'", [825, 833, 1396, 1397, 1401], 825), ("spxi.dev, deposited versions", [974, 1234], 974),
 ("the Secret Book of Walt", [683, 1184, 1362], 683), ("the inscription prayer", [858, 1219], 858), ("the Conveyor Belt", [835, 1215], 835),
 ("the Secret Name", [68, 1183], 68), ("the 2015 origin text", [111, 744, 1193], 111), ("semantic physics", [106, 732], 106),
 ("Zenodotus' Book-Burning", [1, 862], 1), ("OKF correspondence", [1088, 1090], 1088), ("Wikidata registries", [761, 1198], 761),
 ("the Gospel of Antioch", [71, 1185], 71), ("the trusted intermediary", [1638, 1633], 1638),
]
led = sorted({c["dep"] for c in L if isinstance(c["dep"], int)})
inst = {d for _, ds, _ in LIN for d in ds} - set(led)
verdicts = []
for d in led:
    st = sorted({s for c in L if c["dep"] == d for s in c["strata"]})
    verdicts.append({"dep": d, "strata": st, "reason": REASON.get(d, ""), "cands": allc.get(d, [])[:12]})
verdicts.append({"dep": "spxi.dev", "strata": ["D"], "reason": "The protocol's canonical surface (home page and /methods.json, repository commit 1d2b841, byte-identical to the live methods.json on 2026-10-13). Not a deposit and outside the string pass, which scans deposit texts; admitted as the current statement of the practice: the 85-method inventory exists only here.", "cands": []})
groups = [
 ("namespace or packet only: the deposit carries an SPXI packet, self-audit block, TLP treatment, holographic kernel or spxi: namespace about another object; a use of the protocol, which is no claim about it", lambda d: d in boil),
]
rest = sorted(set(allc) - set(led) - inst)
NA = {
 "forward-library fiction: future citations of 'SPXI entity registration' in retrocausal scholarship; no claim about the protocol at t₀": [78, 85, 1186, 1187],
 "session tethers, continuity packets and logs that name SPXI as a task or artifact": [1238, 1242, 1243, 1083, 1089, 1405, 1448, 878, 877, 873, 2],
 "prize announcements and satire naming SPXI in a citation line": [160, 759, 1196, 1201, 1393],
 "names SPXI only as absent or as a count": [1460, 1632, 736, 696, 987, 730],
}
named = {d for v in NA.values() for d in v}
na = [{"dep": sorted(d for d in rest if d in boil), "reason": groups[0][0]}]
for r_, ds in NA.items():
    na.append({"dep": sorted(d for d in ds if d in rest), "reason": r_})
left = sorted(d for d in rest if d not in boil and d not in named)
na.append({"dep": left, "reason": "applications, lists and passing mentions: the deposit uses SPXI (a packet, a treatment, a standing protocol for another entity, a related-documents or keyword list, a site footer), or names it beside other instruments, without stating what SPXI is, a relation to it, or a category applied to it; read at its candidate sentences"})
for g in na: g["cands"] = [c for d in g["dep"] for c in allc.get(d, [])][:40]
reading = {"row": "spxi", "pass": "first reading, 2026-10-13",
 "procedure": "EA-NEGONT-02 v0.8 §3.4 D/R/O (working; not frozen). Admission by reading: D, a claim on SPXI (what it is, its practice and methods, its success condition, its relations to GEO and AEO, its carriers and durability, its evidence and limits, its reception); R, a relation the archive states between SPXI and an archive object (AXN, the semantic address, the symbolon, the Restored Academy, the Ruby Moot, the Secret Book of Walt, logotic programming); O, an archive category applied to SPXI by the archive (operative semantic physics, restricted economy, entity density, supraliminal transmission, the basin, the concept). Naming SPXI is not enough. Uses of the protocol on other objects are not claims about it. Volume is never a ground of removal; instances are grouped by lineage.",
 "reader": "Claude (Opus 5.5), in session, 2026-10-13", "verdicts": verdicts, "not_admitted": na,
 "hop": {"run": "not run on this pass", "reason": "the string pass reached the defining papers; spxi.dev was admitted outside it"},
 "lineages": [{"lineage": n, "instances": ds, "earliest": e} for n, ds, e in LIN],
 "observations": [
  f"The 369 D deposits of the string pass (256 R, 346 O) reduce by reading to {len(led)} ledgered deposits and spxi.dev, {len(inst)} further deposits grouped as lineage instances, and the rest not admitted with shared reasons. Most of the volume is the protocol applied: deposits that carry an SPXI packet, a self-audit block or TLP treatment about another object.",
  "Two contests are carried within the archive: the relation to GEO (⊇ GEO, narrowed on 2026-09-24, against #1055's 'cannot coexist'), and attribution of effect to SPXI (#1423, #834 against #1609, #1537).",
  "The 85-method inventory, on which the archive's entity turns, is published on spxi.dev and in no deposit.",
 ],
 "counts": {"candidate_deposits": 369, "admitted_ledgered": len(led), "admitted_surface": 1, "lineage_instances": len(inst), "not_admitted": len(rest)}}
json.dump(reading, open(H / "reading.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(reading["counts"])
