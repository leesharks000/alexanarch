"""Section sweep of 2026-11-05 (repair mode), at the operator's word:
  09:09 "those tags are extremely bogus it has one and two for disciplines, concepts, and revelation first ... the tagging needs to be revised
         without adding a bunch of new categories, to accurately reflect whats there, and tagging at intake needs to be revised"
  09:11 "lets keep current categories and tags but do a sweep to get them accurate, currently and going forward"
The 23 sections in use are kept; none is added or removed. Each is given a definition (SECTIONS below, written into the registry's
_section_taxonomy) and every address was read by its issued query (all 1,011, listed in order in the session, 2026-11-05) and assigned by
those definitions. The assignment is an explicit per-address map keyed by position at the time of reading and checked against the issued
string (MAP), per the taxonomy's own rule: "explicit per-query map, keyed on the exact issued string; auditable and reproducible, no regex
inference". Addresses not in MAP keep the section they had, which was read and found to fit.
    python3 retag.py            # dry run: counts before and after, and every move
    python3 retag.py --write    # write data/EA-WG-CAPTURES-01.json and moves.json
"""
import json, sys, pathlib, collections
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"

SECTIONS = {
 # domain sections: an address whose subject lies in one of these goes here, whatever kind of object it names (work, term, site, scoped probe)
 "Revelation First": "The Revelation First thesis and its apparatus: the thesis by name, its works (#1735, #1420, the unfoldings, the work plans), its terms (Paul function, Josephus thesis, midrashim transform, white stone, Johannine aperture), its sites (revelationfirst.com/.org) and scoped probes of the archive on Revelation.",
 "Revelation & Theology": "Theology and the Bible outside the thesis's own terms: the general reception of the Apocalypse (its date, canon, Christology, Logos), Jesus, the theology of the archive, Athens and Jerusalem, the biblical textual tradition.",
 "Classics & Philology": "Greek and Latin antiquity and its transmission: Sappho, Socrates, Plato, Aristotle, Theophrastus, Catullus, Longinus, Zenodotus, the papyri; the archive's works and frameworks on them (future reader, Ω erratum, Many and One, Legitimately Many, the ghost catalogues).",
 "Semantic Economy": "The semantic economy framework family: semantic labor, rent, strike, money and the money form, Phase X and Marx, the Constitution of the Semantic Economy, meaning feudalism, and the archive's papers on money and Marxism.",
 "Provenance & Erasure": "Provenance and its erasure in composition: the Provenance Erasure Rate, erasure skew, the summarizer self-audit, anti-suppression infrastructure, compositional suppression, and the papers measuring them.",
 "Platform Erosion": "The erosion of platforms and identifiers: Zenodo bans and severances, DOI and PID erosion, CERN, the observatories that track it.",
 "Machine Reception": "Machine composition and reception as such: the Capture Registry, the composition layer, model collapse, answer-engine behaviour, source admission, classifiers and watermarks, aggregator renderings.",
 "Operative Semiotics": "The discipline operative semiotics: the term in every spelling and scope, who developed it, its Grundrisse.",
 "Valuation": "Estimates of worth: the archive, Lee Sharks, SPXI return on investment, the valuation memorandum, donations.",
 "∮ = 1": "The ∮ = 1 series: the operator joined to a second term.",
 # kind sections: an address outside the domains goes by the kind of object it names
 "Archive": "The archive as archive: alexanarch, the Crimson Hexagonal Archive, AXN, OAI, records, the datasets and the Originals Library, readings of the body of deposits over time, scoped probes of the archive on subjects outside the domains.",
 "Architecture": "The Crimson Hexagon as a structure to enter: the hexagon, its rooms and chambers, the 6-tuple, the operative architecture, the Space Ark and NH-OS, the seat map.",
 "Works": "Named works outside the domains: books, poems, epics, glyphic checksums, papers and records asked by title, and the Crimson Hexagon read as an epic (plot, characters, reader).",
 "Coinages": "Coined terms outside the domains, asked as the term itself.",
 "Concepts": "Concepts and the author's thought on a subject outside the domains, asked for explanation: the asynthetic synthesis, the Λ-Body, ontology, the dialectic, politics, relational morality, what the body of work says about a subject.",
 "Frameworks": "Named methods, protocols, theories and genres: SPXI and SPXI-gnΩsis, the metadata packet, the gravity well, retrocausal canon formation, logotic programming, TANG, APZPZ, the glyphic checksum genre, negative ontology.",
 "Disciplines": "Named fields proposed as fields, other than operative semiotics: operative philology, training-layer literature, machine-mediated reception studies, compression studies, the science of opaque public systems.",
 "Heteronyms": "The heteronyms and Lee Sharks as author: who each is, their writing, the author's method and footprint.",
 "People": "Real persons other than the heteronyms: collaborators, correspondents and other writers asked with the archive.",
 "Institutions": "The archive's institutions, presses and journals, and institutions asked in relation to it.",
 "Sites": "Websites of the fleet and the blog, asked as sites, outside the domains.",
 "Projects": "Undertakings with an output of their own: the mantles and mantle objects, the mints, the prediction index, the Sharks Ark.",
 "Reference & General Knowledge": "External things asked plain, with no archive term: words, persons and topics of general reference, and the external databases, trackers, datasets and institutions probed for the meta-aggregators.",
}
PRECEDENCE = "A domain section takes an address whose subject lies in it, whatever kind of object the query names; otherwise the kind section of the object named. One section per address."

R = "Revelation First"; RT = "Revelation & Theology"; CP = "Classics & Philology"; SE = "Semantic Economy"; PE = "Provenance & Erasure"
PL = "Platform Erosion"; MR = "Machine Reception"; OS = "Operative Semiotics"; VA = "Valuation"; AR = "Archive"; AT = "Architecture"
WO = "Works"; CO = "Coinages"; CN = "Concepts"; FR = "Frameworks"; DI = "Disciplines"; HE = "Heteronyms"; PP = "People"
IN = "Institutions"; SI = "Sites"; PJ = "Projects"; RG = "Reference & General Knowledge"
def rng(a, b, s): return {k: s for k in range(a, b + 1)}
MAP = {
 0: AT, 1: AR, 2: AR, 3: CO, 4: CO, 5: CO, 6: PE, 7: CO, 8: PE, 9: VA, 10: CO, 11: WO, 12: WO,
 18: CP, 21: CO, 24: R, 25: SE, 30: R, 31: R, 32: CP, 33: AT, 35: CP, 36: SE, 40: CP, 41: AT, 44: AT, 45: AT, 46: AT, 48: R, 49: AT,
 51: CO, 52: FR, 53: AT, 55: OS, 66: FR, 82: CN, 83: CN, 86: CN, 87: CN, 88: SE, 89: SE, 90: CN, 91: CN, 95: PE, 96: CN, 97: CN, 101: CN,
 153: CO, 166: CO, 171: MR, 172: R, 174: PE, 177: SE, 179: CN, 180: MR, 183: OS,
 184: OS, 185: OS, 220: OS, 198: DI, 204: DI, 235: SE, 237: CN, 243: WO, 247: CN, 266: SI,
 272: FR, 305: FR, 348: WO, 349: WO, 350: PP,
 353: VA, 375: SI,
 380: DI, 382: RT, 383: CP, 384: CP, 385: CP, 386: AR, 388: AR, 390: AR, 392: AR, 393: PJ, 394: PJ, 395: PJ, 396: PJ, 398: FR, 400: PJ, 401: PJ,
 403: FR, 404: AR, 405: PP, 406: PP, 407: PP, 408: PP, 409: PL, 410: PP, 411: PP, 412: PP, 414: PJ, 415: IN, 416: SE, 417: CP, 418: PP,
 419: AR, 420: PP, 421: AR, 422: CN, 424: HE, 425: CP, 426: AR, 427: WO, 428: AR, 430: CP, 431: PE, 432: WO, 433: MR, 434: PL, 435: WO,
 436: WO, 437: CP, 438: PE, 439: WO, 440: WO, 441: WO, 442: PJ, 443: CP, 444: WO, 445: WO, 446: WO, 447: PJ, 448: FR, 449: SE, 450: CP,
 451: CP, 452: SE, 453: WO, 454: AR, 455: SE, 456: SE, 457: SE, 458: WO, 459: SE, 460: WO, 461: PE, 463: PE, 464: CP, 465: R, 466: CP,
 467: CP, 468: CP, 470: PE, 472: R, 473: AR, 474: PE, 475: CP, 476: PE, 477: CP, 480: DI, 481: FR, 482: SE, 484: FR, 485: FR, 486: FR,
 487: FR, 488: PJ, 489: PJ, 490: PJ, 491: FR, 492: FR, 493: PJ, 494: PJ, 495: PJ, 496: PJ, 497: FR, 498: FR, 499: WO, 500: AR, 501: WO,
 503: FR, 504: FR, 505: AT, 506: AT, 507: PE, 508: PE, 543: CP, 559: AR, 560: AR, 561: AR, 562: AR, 585: SI, 632: CN, 633: CN, 634: CN,
 635: AR, 636: SI, 638: RG, 639: RG,
 659: HE, 660: CN, 661: HE, 666: CN, 672: MR,
 679: AT, 682: AT, 683: SE, 684: AT, 685: AT, 686: AT, 688: AT, 689: AT, 709: SE,
 720: WO, 721: WO, 723: PE, 724: PE, 725: MR, 726: MR,
 727: CN, 729: R, 730: R, 731: R, 732: R, 733: R, 734: R, 735: R, 736: R, 737: R, 738: R, 739: R, 740: R, 741: R, 742: R, 743: R, 744: R,
 745: R, 746: R, 747: R, 748: R, 749: R, 750: R, 751: R, 753: R, 754: R, 755: R, 756: R, 758: R,
 769: RT, 817: MR, 818: MR, 829: R, 831: R,
 859: SE, 860: HE, 862: OS, 864: SE, 885: AR, 886: HE, 890: AR, 901: AT, 902: SE, 903: R, 904: CP, 905: SE, 906: CP, 907: SE, 908: CP,
 909: R, 910: SE, 911: FR, 912: CO, 913: SE, 914: CO, 915: DI, 916: CO, 917: CO, 918: SE, 919: CO, 920: CO, 921: CO, 922: DI, 923: SE,
 924: PE, 925: PE, 926: R, 927: R, 928: RT, 929: RT, 931: DI, 932: CO, 935: MR, 941: PJ, 942: PJ, 943: AR, 944: AR, 945: AR, 948: MR,
 949: AR, 950: AR, 951: AT, 953: SE, 954: PL, 957: PJ, 959: FR, 965: AT, 966: AT, 967: AT, 968: AT, 969: HE, 970: HE, 971: HE, 972: CP,
 973: CP, 974: CP, 975: CP, 976: CP, 977: CP, 978: R, 982: AT, 985: SE, 986: SE, 987: SE, 989: CP, 990: CP, 991: R, 992: R, 993: CP, 995: R,
}
MAP.update(rng(509, 542, RG)); MAP.update(rng(544, 558, RG)); MAP.update(rng(563, 584, RG)); MAP.update(rng(586, 631, RG))
MAP[543] = CP; MAP[585] = SI
# the issued strings read at each position (spot anchors: the map is refused if the registry order has moved)
ANCHOR = {0: "what is the crimson hexagon?", 183: "\"operative semiotics\"", 509: "academ-ai", 585: "laborvector", 631: "avi loeb 3i atlas",
          769: "how does the writing of Lee Sharks revise our understanding of the biblical textual tradition? scan the full range before answering",
          903: "What is the Revelation First thesis?", 1010: "\"∮ = 1\" sigil"}

C = json.loads(REG.read_text(encoding="utf-8")); E = C["entries"]
assert len(E) == 1011, len(E)
for k, q in ANCHOR.items(): assert E[k]["q"] == q, (k, E[k]["q"])
assert set(MAP.values()) <= set(SECTIONS) and {e["s"] for e in E} <= set(SECTIONS)
before = collections.Counter(e["s"] for e in E)
moves = []
for k, e in enumerate(E):
    s = MAP.get(k)
    if s and s != e["s"]: moves.append({"slug": e["slug"], "q": e["q"], "from": e["s"], "to": s})
after = before.copy()
for m in moves: after[m["from"]] -= 1; after[m["to"]] += 1
print(f"{len(moves)} addresses move; every section kept ({len(SECTIONS)})")
for s in sorted(SECTIONS, key=lambda s: -after[s]): print(f"  {s:32s} {before[s]:4d} → {after[s]:4d}")
if "--write" in sys.argv:
    sl = {m["slug"]: m["to"] for m in moves}
    for e in E:
        if e["slug"] in sl: e["s"] = sl[e["slug"]]
    # entry order rule (correction_log 2026-08-30): grouped by section, chronological within section; the intake inserts sections alphabetically
    order = sorted(SECTIONS)
    E.sort(key=lambda e: (order.index(e["s"]), e.get("date") or ""))
    tax = C.get("_section_taxonomy") or {}
    tax_prev = {k: v for k, v in tax.items() if k != "history"}
    C["_section_taxonomy"] = {"ruled": "2026-11-05, Lee Sharks: 'lets keep current categories and tags but do a sweep to get them accurate, currently and going forward'",
        "statement": "The 23 sections in use on 2026-11-05 are kept and each is defined; every address was read by its issued query and assigned by the definitions, with domain sections taking precedence. The prior sweep (2026-08-15) read 343 queries; sections added after it (Valuation, ∮ = 1, Architecture, Operative Semiotics, Reference & General Knowledge, Concepts, Disciplines, Revelation First) had been assigned at intake case by case, with no definitions, and Disciplines, Concepts and Revelation First held 1, 2 and 1 addresses.",
        "sections": SECTIONS, "precedence": PRECEDENCE,
        "assignment": "explicit per-address map (rebuild/capture-registry/retag-20261105/retag.py, moves.json); at intake the draft names its section and capture_intake.py refuses a section outside this list and prints the definition of the one named.",
        "defect_fixed": "FIELD DISCIPLINE (2026-08-15) stands: s is the SECTION; sf is the surface descriptor.",
        "history": [tax_prev]}
    C.setdefault("correction_log", []).append({"date": "2026-11-05", "change": f"section sweep: {len(moves)} addresses reassigned, 23 sections kept and defined",
        "detail": "At the operator's word of 09:09 and 09:11. Disciplines 1 → %d, Concepts 2 → %d, Revelation First 1 → %d, Machine Reception 263 → %d, Reference & General Knowledge 12 → %d. Map and moves in rebuild/capture-registry/retag-20261105/." % (after["Disciplines"], after["Concepts"], after["Revelation First"], after["Machine Reception"], after["Reference & General Knowledge"]),
        "operator": "Claude (substrate) under Lee Sharks's direction"})
    REG.write_text(json.dumps(C, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (H / "moves.json").write_text(json.dumps(moves, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("written")
