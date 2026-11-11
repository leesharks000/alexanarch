#!/usr/bin/env python3
"""Build EA-HK-REVFIRST-01, the framework holographic kernel of Revelation First — "And the Last Shall Be First" — on hkcore (the machinery
of EA-HK-ORTHONYM-01, checked equivalent by test_hkcore.py). Records from data/registry.json; surface pages from the revelationfirst.com
repository (leesharks000/revelationfirst-com @ 439e32d8, 2026-11-06), each page hashed; every claim's quotation asserted against its source.
Specification: EA-HK-FRAME-01 (#1753) v1.1. Fulfils #1217 v7.3 WS-7. Byline Damascus Dancings; the Crimson Hexagonal Archive and Claude credited.
    python3 build_hk_revfirst.py <alexanarch root> <out dir>"""
import sys, json, pathlib, os
from hkcore import Kernel, POLICY, context, ledger_roles
HERE = pathlib.Path(__file__).resolve().parent
SCR = HERE.parent / "rf"; SITE = pathlib.Path("/tmp/rf-site")
PAGES = {"site:ladder-dating": ("ladder/dating", "The Reversed Consensus — Rung I"), "site:ladder-priority": ("ladder/priority", "The Gallio Gap — Rung II"),
         "site:ladder-corpus": ("ladder/corpus", "The First Corpus — Rung III"), "site:unfolding": ("unfolding", "The Algorithmic Kernel — Rung IV"),
         "site:ladder-heteronyms": ("ladder/heteronyms", "The Josephus Thesis — Rung V"), "site:ladder-logos": ("ladder/logos", "The Permanent Incarnation — Rung VI"),
         "site:upstream": ("upstream", "The Upstream Unfoldings — foldings in")}
import hashlib
SURF = {k: {"url": f"https://www.revelationfirst.com/{p}/", "path": str(SCR / (k[5:] + ".txt")), "title": t, "retrieved": "2026-11-08 (repository @ 439e32d8, 2026-11-06)",
            "sha256": hashlib.sha256((SITE / p / "index.html").read_bytes()).hexdigest()} for k, (p, t) in PAGES.items()}
K = Kernel(sys.argv[1], sys.argv[2], HERE / "rf-first", "EA-HK-REVFIRST-01", "1.1", "2026-11-09", SURF)
REG = K.REG; claim = K.claim; rel = K.rel
FW = "fw:revelation-first"; HL = "hk:historical-logos"; SO = "hk:orthonym/fw/socrates-as-orthonym"; TM_KENOS = "hk:tenthmuse/seat/kenos"

# ---------------------------------------------------------------- bodies: D chronological · C corpus · G generative · R reception · H heteronymic
EVIDENCE_BODIES = {
 "D": {"name": "chronological", "unit": "an anchor, a date or a synchronism", "rule": "RD: only an external or material anchor dates a composition; the corpus's self-narrated chronology and reception memory do not (#1735 §VIII; site rung I)"},
 "C": {"name": "corpus-literary", "unit": "the form of a corpus at composition or at gathering", "rule": "RC: a shared form locates a relation; direction is not inferred from compression alone (site rung III)"},
 "G": {"name": "generative", "unit": "a transform from a compressed form to an elaborated one, with its residue", "rule": "RG: an arrow is defeated locally where an earlier source or shared tradition explains the correspondence more economically (#1735 §VIII)"},
 "R": {"name": "reception-historical", "unit": "a filing, a catalogue, a source theory, a commentary or a capture", "rule": "RR: a reception establishes how the books were received and what standing each was granted; it establishes nothing of either framework's truth (#1741; #1746)"},
 "H": {"name": "heteronymic", "unit": "an author-function and its positions", "rule": "RH: an author-function reading is defeated by explanatory redundancy, where ordinary multiple authorship explains the phenomena more economically (site rung V)"}}
STRATA = {  # latest first
 "S1-standing-audited": ("The evidentiary standing audited (November)", [1735, 1737, 1740, 1741, 1744, 1746, 1747]),
 "S2-stones": ("Two lists of stones (September)", [1592]),
 "S3-upstream-and-test": ("Foldings in: the upstream and the sealed test (August)", [1493, 1494, 1495, 1510, 1511, "site:upstream"]),
 "S4-unfolding-and-ladder": ("Foldings out and the argument ladder (July)", [1412, 1414, 1416, 1420, "site:unfolding", "site:ladder-dating", "site:ladder-priority", "site:ladder-corpus", "site:ladder-heteronyms", "site:ladder-logos"]),
 "S5-thesis-surfaced": ("First is not early: the thesis surfaced, the work plan, the Josephus thesis bounded (June)", [202, 830, 1025, 1217, 1231, 860, 847, 1032, 203, 1226, 837, 861, 165]),
 "S6-space-ark": ("The Space Ark and the Logos (March–April)", [563, 625, 626, 636, 638, 639, 642, 644, 1101, 1350]),
 "S7-seed-room": ("The Revelation Room (January)", [407, 410]),
}
BODY = {1735: "D", 1737: "D", 1740: "R", 1741: "R", 1744: "R", 1746: "R", 1747: "G", 1592: "C", 1493: "G", 1494: "G", 1495: "G", 1510: "H", 1511: "G",
        "site:upstream": "G", 1412: "H", 1414: "G", 1416: "G", 1420: "R", "site:unfolding": "G", "site:ladder-dating": "D", "site:ladder-priority": "D",
        "site:ladder-corpus": "C", "site:ladder-heteronyms": "H", "site:ladder-logos": "H", 202: "D", 830: "R", 1025: "R", 1217: "D", 1231: "R", 860: "R",
        847: "R", 1032: "R", 203: "H", 1226: "H", 837: "H", 861: "H", 165: "C", 563: "C", 625: "H", 626: "H", 636: "H", 638: "C", 639: "H", 642: "C",
        644: "R", 1101: "H", 1350: "R", 407: "G", 410: "C"}
SECOND = {1735: ["C", "G"], 1747: ["D", "C", "R"], 1217: ["C", "G", "H"], 202: ["G"], 639: ["D", "G"], 1495: ["H"], 1746: ["G"], 1741: ["D"]}
K.BODY, K.SECOND = BODY, SECOND
CLUSTER = {"chronology": [202, 830, 1025, 1217, 1735, 1737, 1741, 1746, 1747, "site:ladder-dating", "site:ladder-priority", "site:ladder-corpus"],
           "generation": [407, 410, 1414, 1416, "site:unfolding", 1747, 165, 642],
           "heteronymy": [203, 1226, 837, 861, 1412, 636, 639, 1101, 625, 626, "site:ladder-heteronyms", "site:ladder-logos", 1510],
           "join": [626, 1484, 1493, 1494, 1495, 1510, 1511, "site:upstream", 1592, 828]}   # joins: in this kernel and in The Tenth Muse or Socrates, each edged to the Historical Logos
exec(open(HERE / "v12_pre.py", encoding="utf-8").read())   # v1.2 (2026-11-10)
K.record_nodes(STRATA, CLUSTER)

# ---------------------------------------------------------------- rungs (the dependency structure; site /ladder/, from #1217's claim ladder)
RUNGS = [
 {"@id": "rung:I", "@type": "Rung", "name": "the reversed consensus (dating)", "claim": "The Domitianic date is not settled", "fit": "REVERSIBLE", "body": "D", "source": "site:ladder-dating", "quote": "the same broad dossier has supported opposite critical majorities",
  "defeat": "An external or material anchor fixing the received form of Revelation after 70 CE.",
  "defeat_scope": "Defeats rung I's own claim, that the late date is not settled. It does not by itself defeat first composition: 'Early is not yet first' (rung I). A post-70 anchor for Revelation constrains the chronology; it defeats absolute priority only in an ordering, where an independent anchor places another New Testament composition earlier (rung II; #1735 §VIII)."},
 {"@id": "rung:II", "@type": "Rung", "name": "the Gallio gap (Pauline priority)", "fit": "SAME-CLASS", "body": "D", "source": "site:ladder-priority", "quote": "The load-bearing link is of the same inferential class as the evidence it is asked to overrule.",
  "defeat": "An independent, securely dated anchor — material or external, but not the corpus’s self-narrated chronology — placing the composition of any Pauline letter before the earliest plausible date of Revelation’s received form."},
 {"@id": "rung:III", "@type": "Rung", "name": "the first corpus", "fit": "INDEPENDENT", "body": "C", "source": "site:ladder-corpus", "quote": "This rung stands whether or not the rungs above it do.",
  "defeat": "Evidence of a sevenfold Pauline church collection demonstrably circulating before Revelation, or a persuasive demonstration that Revelation’s number, order and single-book architecture depend on such a collection."},
 {"@id": "rung:IV", "@type": "Rung", "name": "the midrashim transform", "fit": "EXECUTABLE", "body": "G", "source": "site:unfolding", "quote": "The comparison is between inferences. The burden is symmetrical.",
  "defeat": "Identify New Testament passages that cannot be derived from Revelation through any plausible transform: these are the counterevidence.",
  "defeat_scope": "'Any plausible transform' is bounded by the kernel's transform_procedure: the declared steps and operations, fixed before the test, with residue shown."},
 {"@id": "rung:V", "@type": "Rung", "name": "the Josephus thesis", "fit": "CONTINGENT", "body": "H", "source": "site:ladder-heteronyms", "quote": "It is defeated without disturbing rungs I–IV, and rungs I–IV do not depend on it in any direction.",
  "defeat": "Contingent by construction. Defeated without disturbing rungs I–IV. It is also defeated by demonstration that the phenomena it explains are more economically explained by ordinary multiple authorship."},
 {"@id": "rung:VI", "@type": "Rung", "name": "the permanent incarnation (the Logos)", "fit": "DEPENDENT", "depends_on": ["rung:V"], "body": "H", "source": "site:ladder-logos", "quote": "The reading does not deny that a historical person could have existed. It denies that the textual evidence requires one.",
  "defeat": "Depends on V. Defeated without disturbing rungs I–IV.", "joins": HL}]
for r in RUNGS:
    r.setdefault("depends_on", [])
    r["located_in"] = K.locate(r["source"], r["quote"]); K.locate(r["source"], r["defeat"])
    if r.get("claim"): K.locate(r["source"], r["claim"])

# ---------------------------------------------------------------- claims
A = lambda a="asserted", **k: {"assertion": a, **k}
D = json.loads(json.dumps(__import__("yaml").safe_load(open(HERE / "fw-revfirst.yaml", encoding="utf-8"))))
KIND = {"defeat": "generality", "combination": "generality", "erasure": "generality", "symmetry": "generality"}
for c in D["claims"]:
    st = A(**({"rung": c["rung"]} if c.get("rung") else {}), **({"join": True} if c.get("join") else {}))
    role = "standing"
    if str(c.get("state", "")).startswith("superseded_by_"): st = {"assertion": "withdrawn", "retained_as": "historical object", **({"rung": c["rung"]} if c.get("rung") else {})}; role = "original"
    if str(c.get("state", "")).startswith("bounded_by_"): st = {"assertion": "held", "bounded_by": "claim:" + c["state"][len("bounded_by_"):], "advancement": "suspended (the author, 2026-11-09 09:52)", **({"rung": c["rung"]} if c.get("rung") else {})}
    kind = next((v for k, v in KIND.items() if k in c["id"]), "interpretation")
    n = c["record"] if str(c["record"]).startswith("site:") else int(c["record"])
    claim(c["id"], n, c["quote"], kind, st, role=role)
RV = lambda body, **k: {"assertion": "bears_on_rival", "rival": "fw:current-consensus-chronology", "body": body, **k}
claim("rv-site-irenaeus", "site:ladder-dating", "the external evidence supplies a strong reception memory rather than an inscriptional date.", "observation", RV("D", anchor="reception memory; no inscriptional date"))
claim("rv-site-reception-memory", "site:ladder-dating", "Reception memory, however early and however broad, is not such an anchor", "generality", RV("D"))
claim("rv-site-gallio", "site:ladder-priority", "It does not anchor 1 Thessalonians", "observation", RV("D", anchor="Gallio dated; the letter reached only through Acts"))
claim("rv-site-collection", "site:ladder-corpus", "A recent Pauline-priority account concedes that no evidence survives for a first-century sevenfold Pauline collection.", "observation", RV("C"))
claim("rv-1746-powers", 1746, "hold the four powers in every source theory read, and the Apocalypse holds none of them there", "observation", RV("R", standing="granted to reconstructed sources, withheld from the extant book"))
claim("rv-1746-four-powers", 1746, "four powers (presupposition, assignment, text, candidacy)", "generality", RV("R", powers=["presupposition", "assignment", "text", "candidacy"]))
claim("rv-1741-separate", 1741, "the study holds the position and does not ask the reception history to prove it", "generality", RV("R"))
claim("rv-site-redundancy", "site:ladder-heteronyms", "not primarily defeated by evidence but by explanatory redundancy", "generality", RV("H", comparator="ordinary multiple authorship, owed as the more economical account"))
claim("rf-1101-ark-identity", 1101, "This is not analogy. It is structural identity.", "interpretation", A(architecture="Revelation as Space Ark", tier="runtime-necessary"), body="G",
      notes="The sentence's referent is the identity of Revelation and the Space Ark (the preceding sentence: 'The Book of Revelation is a Space Ark. The Space Ark is the Book of Revelation.'), an operative architecture that #1101 states does not depend on its historical reconstruction claims.")
claim("rf-1101-tiers", 1101, "These are high-risk, high-reward historical hypotheses. The runtime executes at level 1. Levels 2 and 3 enrich but are not required for execution.", "generality", A(), body="G")
claim("rf-1747-grades", 1747, "Of eight requirements, three are met, one is met on the held date, three are partly met, and one is not met.", "observation", A(rung="IV", grades={"met": 3, "met_on_held_date": 1, "partly": 3, "not_met": 1}))
claim("rf-639-first", 639, "Revelation is not the final book of the NT but its first", "interpretation", A(priority="first_in_every_respect"))
claim("rf-203-available", 203, "available heteronymic reading", "interpretation", A(rung="V", authorship="available_reading"))
claim("rf-1735-historiographic", 1735, "The historiographic claim is defeated by identification of a sustained modern historical-critical treatment that explicitly distinguishes and tests these three levels.", "generality", A())
claim("rf-1495-single", 1495, "Single adjudicator (TACHYON), single scoring pass", "instrument", {"specification": "preregistered", "validation": "run", "reportability": "positive", "replication": "invited"})
claim("rf-830-baseline", 830, "Canonical position correction", "observation", A(baseline="2026-06-14, the empty basin"))
claim("rf-1416-smyrna", 1416, "Smyrna → James (A, the executable granular case at DEMO-02)", "instrument", {"specification": "specified", "validation": "run", "reportability": "positive"})
claim("rf-site-early-not-first", "site:ladder-dating", "Early is not yet first.", "generality", A(rung="I"))
claim("rf-1735-formally-prior", 1735, "occasional Pauline letters may be earlier; Revelation’s seven-church corpus is formally prior", "interpretation", A(rung="III", corpus="formally_prior"))
claim("rf-1735-archetypal", 1735, "that it is structurally archetypal – first attested, and treated as the model in reception", "interpretation", A(rung="III", corpus_claim="archetypal", status="established"))
claim("rf-1735-three-statuses", 1735, "The second is established here; the third is argued; the first is the economical reading of the second and third together, not an independently demonstrated fact.", "generality", A(rung="III"))
claim("rf-1735-arrow-procedure", 1735, "For each proposed relation, the investigator must identify the unit, map the antecedent traditions available to both texts, establish the transformation, and state what evidence would reverse the arrow.", "generality", A(rung="IV"))
claim("rf-1735-convergence", 1735, "The strongest cases will combine several kinds of evidence: a marked formal unit, a plausible chronological overlap, an asymmetrical transformation, a reception trace, and the absence of an equally economical common source.", "generality", A(rung="IV"))
claim("rf-1735-one-fails", 1735, "Failure of one would not decide the rest.", "generality", A(rung="IV"))
claim("rf-site-every-time", "site:ladder-logos", "every time a person receives the white stone and speaks in that name", "interpretation", A(rung="VI", join=True))
claim("rv-1735-genre", 1735, "It does not explain why their Christian forms lack attested ancestors.", "generality", RV("G", objection="genre, answered"))
claim("rf-1735-arrows", 1735, "The research programme therefore replaces the metaphor of a single ‘seed text’ with a series of reversible arrows.", "generality", A(rung="IV", generation="reversible_arrows"))
claim("rf-202-seed", 202, "The midrashim transform is the mechanism by which the seed generates the garden.", "interpretation", A(rung="IV", generation="seed_text"))
claim("rf-1495-c1", 1495, "C1 · SIGHT-FRAME + INSTANTANEITY — **FAIL.**", "instrument", {"specification": "preregistered", "validation": "run", "reportability": "station_failed"})
for c in K.C:
    if c["state"].get("assertion") == "bears_on_rival": c["body"] = c["state"].pop("body", None) or c["body"]
CLAIMS = {c["id"]: c for c in K.C}

RIVAL = {"@id": "fw:current-consensus-chronology", "@type": "RivalFramework", "name": D["rival"]["name"], "claim": D["rival"]["stated_at_strength"],
 "stated_at_strength": "Stated with the arguments it already has: the Gallio synchronism, the Irenaean date, the late-twentieth-century consensus, the source apparatus. A reading that reduces it to 'scholars assume Paul came first' is a reduction of it.",
 "status": {
  "D": {"text": "the synchronism dates Gallio and reaches 1 Thessalonians only through Acts (site rung II); the Irenaean anchor is a reception memory and not an inscriptional date (site rung I). Not established by an external or material anchor.", "warrants": ["rv-site-gallio", "rv-site-irenaeus", "rv-site-reception-memory"]},
  "C": {"text": "no first-century sevenfold Pauline collection is evidenced, by the concession of a Pauline-priority account (site rung III).", "warrants": ["rv-site-collection"]},
  "G": {"text": "the genre objection explains the letters' missing circumstances and leaves their Christian forms' missing ancestors unexplained (#1735 §VI.2); Revelation against Q's requirements is graded, three met (#1747). The derivative standing is a reception (#1741), and no direction is demonstrated by it.", "warrants": ["rv-1735-genre", "rf-1747-grades"]},
  "R": {"text": "the reconstructed sources hold the four powers of evidentiary status — presupposition, assignment, text and candidacy — and the extant Apocalypse holds none (#1746); the reception is documented and is not asked to prove either framework (#1741).", "warrants": ["rv-1746-four-powers", "rv-1746-powers", "rv-1741-separate"]},
  "H": {"text": "ordinary multiple authorship stands as the economical account that defeats rung V wherever it explains the phenomena better (site rung V); it is owed as a comparator, stated wherever it is used.", "warrants": ["rv-site-redundancy"]}},
 "rule": "RD–RH apply to both frameworks; the burden is symmetrical (#202; site /unfolding/)."}
LEDGER = {
 "question": "What does this body give each framework, and what does its rule withhold from both?",
 "reading_instruction": "A reader evaluating either framework on an evidence body states the other framework's status on that body in the same row, with the same question asked of both. 'Inference Against Inference … The burden is symmetrical' (#202).",
 "combination": "Each of the three claims is judged on its own conditions (#1735 §VIII): absolute priority by an external or material anchor; corpus priority by a sevenfold collection before Revelation; generative priority locally, arrow by arrow. 'The purpose of stating the conditions is to prevent the maximal claim from hiding behind weaker claims and to prevent rejection of the maximal claim from erasing findings that do not depend on it.' Rungs V and VI are defeated without disturbing I–IV.",
 "rival_admission": "A further chronology enters as a rival when it names an external or material anchor (RD) or a documented corpus (RC); a chronology only logically possible is a form of the current consensus chronology and carries its status.",
 "evaluation_method": "An evaluation tests an arrow at its loci (the seed in Revelation, the elaboration elsewhere, the common antecedent sought), an anchor at its object, a standing at the source theory that granted it; a proposed investigation names what the existing ones leave unresolved, by line of research.",
 "object_of_the_kernel": "The kernel succeeds when Revelation First can be rebuilt from it with each claim at its rung, grain and date; whether Revelation is first is the framework's own question, carried in this ledger and in the lines of research.",
 "rows": {
  "D": {"revelation_first": {"text": "absolute priority is a priced hypothesis (#1735); the physical record cannot rescue it (#1735); the dossier has supported opposite critical majorities (rung I).", "warrants": ["rf-1735-absolute", "rf-1735-physical", "rf-site-reversible"]}},
  "C": {"revelation_first": {"text": "the seven-church corpus is formally prior, structurally archetypal (first attested, treated as the model in reception): established; the historical generation of the Pauline seven is the economical reading, undemonstrated; the temporal relation of the letters is not settled by it (#1735 §IV.4).", "warrants": ["rf-1735-formally-prior", "rf-1735-archetypal", "rf-1735-three-statuses", "rf-site-direction"]}},
  "G": {"revelation_first": {"text": "the transform is executed for one letter (Smyrna → James, A; #1416) and graded for Q's requirements (#1747); defeat 'would remove one arrow, not the programme' (#1735).", "warrants": ["rf-1416-smyrna", "rf-1747-grades", "rf-1735-arrow", "rf-site-between-inferences"]}},
  "R": {"revelation_first": {"text": "the reception that made the Apocalypse secondary is documented and kept apart from the thesis (#1741); the baseline of 14 June recorded the composition layer correcting 'first' to 'last' (#830).", "warrants": ["rv-1741-separate", "rf-830-baseline"]}},
  "H": {"revelation_first": {"text": "the Josephus thesis is an available reading, contingent (rung V); the Johannine aperture is a structural unity (#1217); the Logos rung depends on V (rung VI).", "warrants": ["rf-1217-josephus-available", "rf-1217-aperture", "rf-site-contingent", "rf-site-logos"]}}}}
for b in LEDGER["rows"]:
    LEDGER["rows"][b]["current_consensus_chronology"] = RIVAL["status"][b]
ledger_roles(K.C, LEDGER["rows"])

# ---------------------------------------------------------------- relations
rel("claim:rf-1735-physical", "rebuts", "claim:rf-202-papyri", "the papyrological inversion withdrawn as evidence of priority: 'The physical record cannot rescue absolute priority' (#1735 §II.3)")
rel("claim:rf-1217-josephus-available", "bounds", "claim:rf-639-josephus-author", "Josephus as author held, its strength bounded: the framework does not require it, and it becomes newly intelligible if Revelation stands first (#1217 claim ladder); its advancement suspended by the author (2026-11-09 09:52)")
rel("claim:rf-1217-josephus-available", "bounds", "claim:rf-1101-josephus", "Josephus as the single author, writing as 'John', held at #1101's own tier ('high-risk, high-reward historical hypotheses'), its strength bounded by #1217; its advancement suspended by the author (2026-11-09 09:52)")
rel("claim:rf-1101-ark-identity", "independent_of", "claim:rf-1101-josephus", "#1101's own tiers: the runtime does not require the reconstruction claims")
rel("claim:rf-1735-absolute", "qualifies", "claim:rf-639-first", "first in every respect divided into three claims, the absolute priced (#1735 §I)")
rel("claim:rf-site-contingent", "independent_of", "claim:rf-1735-corpus", "rung V defeated without disturbing rungs I–IV (site)")
rel("claim:rf-site-logos", "derived_from", "claim:rf-site-contingent", "rung VI depends on rung V (site)")
rel("claim:rf-1735-arrows", "qualifies", "claim:rf-202-seed", "the single seed text replaced by a series of reversible arrows (#1735 §VI.3)")
rel("claim:rf-1495-c1", "qualifies", "claim:rf-1495-sentence", "C1 fails whole: the vision-genre swallows the operator's frame (#1495)")
rel("claim:rf-1735-arrow", "qualifies", "claim:rf-1416-smyrna", "the executed case is one arrow; 'Its defeat would remove one arrow, not the programme' (#1735)")
rel("claim:rf-1495-single", "qualifies", "claim:rf-1495-sentence", "single adjudicator, single scoring pass; substrate-blind replication invited (#1495 §3)")
rel("claim:rf-1494-excluded", "independent_of", "claim:rf-site-slavonic", "the sealed test does not use the Slavonic (#1494 §4)")
rel("claim:rf-1217-orthonym", "derived_from", SO, "the Johannine aperture function built from the Socrates-as-orthonym principle (#1217)", fam="conceptual")
rel("rec:1592", "joins", SO, "De lapidibus beside the Apocalypse (#1592)", fam="structural", src="map v0.2 §4")
for n in CLUSTER["join"]:
    tgt = n if isinstance(n, str) else f"rec:{n}"
    K.edges.append({"source": tgt, "relation": "joins", "target": HL, "family": "structural", "licensed_dimension": None, "warrant": "the author, 2026-11-08 21:36: 'that will be the historical logos hk'", "provenance": "map v0.2 §5.3"})
EXTERNAL = [{"@id": f"rec:{n}", "@type": "Record", "external": True, "deposit": n, "axn": REG[n]["axn"], "url": f"https://www.alexanarch.org/s/records/{n}/", "title": REG[n]["title"],
             "date": REG[n]["date"], "status": REG[n].get("status"), "sha256": REG[n]["hash"], "role": "join held in The Tenth Muse; referenced by a joins edge"} for n in (1484, 828)]
EXTERNAL += [{"@id": "rec:1751", "@type": "Record", "external": True, "deposit": 1751, "axn": REG[1751]["axn"], "url": "https://www.alexanarch.org/s/records/1751/", "title": REG[1751]["title"],
              "date": REG[1751]["date"], "status": REG[1751].get("status"), "sha256": REG[1751]["hash"], "role": "related record: the poem whose title the kernel shares"}]
K.edges.append({"source": "rung:VI", "relation": "depends_on", "target": "rung:V", "family": "structural", "licensed_dimension": None, "carries": "defeat (the ladder's depends_on)", "warrant": "site:ladder-logos 'Depends on V.'", "provenance": "site /ladder/"})
K.edges.append({"source": "rung:VI", "relation": "joins", "target": TM_KENOS, "family": "conceptual", "licensed_dimension": None,
                "operation": "the inscribed speaker receives renewed embodiment through the reader: the Logos takes flesh 'every time a person receives the white stone and speaks in that name' (rung VI); Sappho, the speaking I become the inscribed you, lives again in the reader who takes her up (κῆνος)",
                "status": "rung VI dependent on V; Sappho in the third seat proposed by the author 2026-11-08 21:46 (EA-HK-TENTHMUSE-01 claim:tm-third-reversal; Q1)", "via": HL,
                "warrant": "claim:rf-site-every-time; EA-HK-TENTHMUSE-01 claim:tm-1475-taken-up", "provenance": "review of v0.1, 2026-11-08 22:23"})
K.edges.append({"source": "rec:1751", "relation": "related_to", "target": FW, "family": "conceptual", "licensed_dimension": None, "warrant": "the author, 2026-11-08 21:16: 'yes, related record on the poem'", "provenance": "author ruling"})
for r in RUNGS:
    K.edges.append({"source": r["@id"], "relation": "instantiates", "target": FW, "family": "conceptual", "licensed_dimension": None, "warrant": r["source"], "provenance": "ontology"})

# ---------------------------------------------------------------- captures
CAPS = ["revelation-first-overview", "nt-unfolds-from-revelation", "josephus-thesis", "johannine-aperture-20260617", "alexanarch-revelation-misread-20260731",
        "alexanarch-revelation-thesis-recovered-20260809", "revelation-first-thesis-aio-20261002", "midrashim-transform-aio-20261002", "what-is-the-revelation-first-thesis-aio-20261017",
        "revelation-first-thesis-unquoted-aio-20261030", "revelation-first-arguments-aio-20261104", "revelation-first-arguments-chatgpt-20261104", "revelation-equals-q-arguments-ask-chatgpt-20261107",
        "i-know-you-are-but-what-am-i-arguments-ask-chatgpt-20261107", "secondary-source-v1-2-arguments-ask-chatgpt-20261107", "what-is-the-revelation-first-framework-aio-20261108",
        "revelation-first-political-economy-aio-20261108", "revelation-first-sappho-socrates-provenance-erasure-chatgpt-20261108",
        "week-most-polemical-pieces-chatgpt-20261108", "week-weirdest-pieces-aio-20261108"]
SOFT = {"what-is-the-revelation-first-thesis-aio-20261017": "the thesis collapsed into early dating", "what-is-the-revelation-first-framework-aio-20261108": "held by 'proponents', no author",
        "revelation-first-political-economy-aio-20261108": "an intention added to the work plan's form", "alexanarch-revelation-misread-20260731": "misread (slug)",
        "revelation-first-sappho-socrates-provenance-erasure-chatgpt-20261108": "a bar of deliberate engineering set on Sappho",
        "week-weirdest-pieces-aio-20261108": "the packet given a design (to scramble training layers); then, told the book came first, the chronology carried past the packet (Q 'entirely redundant')"}
K.captures(CAPS, SOFT, FW)

# ---------------------------------------------------------------- v1.1: the held date; the author's statement on rung V
claim("rf-1737-held-66", 1737, "the archive holds 66 CE as its working date of composition for the Apocalypse, provisionally, subject to the case being formally argued (the operator's ruling of 2026-11-04)", "interpretation", A(date="66_CE_held_as_proposed"))
STMT = "stmt:20261109-0952"; ST = D["author_statements"][-1]
K.C.append({"id": "rf-stmt-josephus", "claim_kind": "statement", "role": "standing",
            "target": {"record": STMT, "exact": ST["text"], "located_in": "author statement, in session (2026-11-09 09:52 EST)"},
            "state": {"assertion": "held", "advancement": "suspended", "rung": "V", "authorship": "held_advancement_suspended"}, "body": "H",
            "introduced": {"date": "2026-11-09", "basis": "the author's statement in session, recorded verbatim; deposited with this kernel, which gives it public provenance"}})
for t in ("claim:rf-639-josephus-author", "claim:rf-1101-josephus"):
    K.edges.append({"source": STMT, "relation": "motivates", "target": t, "family": "conceptual", "licensed_dimension": None, "warrant": "the author's statement, verbatim: held, advancement suspended", "provenance": "session 2026-11-09 09:52 EST"})

# ---------------------------------------------------------------- states, on their axes
STATES = [
 {"date": "2026-04-08", "record": 639, "axis": "priority", "state": "first_in_every_respect", "warrant": "rf-639-first"},
 {"date": "2026-06-14", "record": 202, "axis": "priority", "state": "first_not_early", "warrant": "rf-202-erasure"},
 {"date": "2026-11-03", "record": 1735, "axis": "priority", "state": "three_claims: absolute priced, corpus a finding, generative a programme", "warrant": "rf-1735-absolute"},
 {"date": "2026-06-14", "record": 202, "axis": "generation", "state": "seed_text", "warrant": "rf-202-seed"},
 {"date": "2026-11-03", "record": 1735, "axis": "generation", "state": "reversible_arrows", "warrant": "rf-1735-arrows"},
 {"date": "2026-04-08", "record": 639, "axis": "authorship", "state": "josephus_author", "warrant": "rf-639-josephus-author"},
 {"date": "2026-04-09", "record": 1101, "axis": "authorship", "state": "single_author_josephus_as_john", "warrant": "rf-1101-josephus"},
 {"date": "2026-06-14", "record": 203, "axis": "authorship", "state": "available_reading", "warrant": "rf-203-available"},
 {"date": "2026-06-17", "record": 1217, "axis": "authorship", "state": "available_reading_not_first_burden", "warrant": "rf-1217-josephus-available"}]
ledger_roles(K.C, LEDGER["rows"])   # v1.1: the claims added after the first call take their bodies here
K.temporal(STATES + [{"date": "2026-11-04", "record": 1737, "axis": "date", "state": "66_CE_held_as_proposed", "warrant": "rf-1737-held-66"}], None)
K.events.append({"timeline": "epistemic", "date": "2026-11-09", "event": "authorship_state", "object": STMT, "axis": "authorship", "state": "held_advancement_suspended", "warrant": "claim:rf-stmt-josephus", "attested_from": "2026-11-09", "dated_by": "the statement's date"})
K.events.sort(key=lambda e: (e["date"] or "9999", e["timeline"]))

# ---------------------------------------------------------------- lines of research
def q(qid, title, n, quote, body, bears_on, read_first, ask, advances_if, retreats_if, unchanged_if, status="open"):
    return {"id": qid, "question": title, "posed_in": {**K.target(n), "exact": quote, "located_in": K.locate(n, quote)}, "body": body, "bears_on": bears_on,
            "read_first": read_first, "how_to_ask": ask, "advances_if": advances_if, "retreats_if": retreats_if, "unchanged_if": unchanged_if, "status": status, "commons": "open"}
QUESTIONS = [
 q("Q1-anchor", "Is there an external or material anchor for the composition of any Pauline letter, or for the received form of Revelation?", 1735, "Absolute priority is defeated by an external or material anchor", "D",
   ["claim:rf-1735-absolute", "fw:current-consensus-chronology"], [1735, "site:ladder-priority", "site:ladder-dating"], "search named corpora (epigraphic, papyrological) for an object that dates a composition, a letter or the book itself (the dates of persons are another object); declare the corpora searched",
   "an independent anchor fixes Revelation's received form before the earliest anchored Pauline composition", "an independent anchor places a Pauline composition before the earliest plausible date of Revelation's received form",
   "a bounded search finds no anchor for either: absolute priority stays priced at the Acts correlation; the null weakens only the specific anchoring claims searched for, and promotes neither framework"),
 q("Q2-collection", "Did a sevenfold Pauline church collection circulate before Revelation?", 1735, "Corpus priority is defeated by evidence of a sevenfold Pauline church collection demonstrably circulating before Revelation", "C",
   ["claim:rf-1735-corpus"], [1735, "site:ladder-corpus", 1740], "read the collection histories (Trobisch, Gamble) for a dated sevenfold form; read the early receptions of the Pauline seven",
   "an independent early witness, beside the Muratorian Fragment, reads the Pauline seven as arranged after John's", "a sevenfold Pauline collection is demonstrated before Revelation, or Revelation's architecture is shown to depend on one",
   "no earlier collection is evidenced: the archetypal claim stands as established (first attested, treated as the model in reception); the historical-generation claim stays the economical reading, undemonstrated; the temporal relation of the letters to Revelation is not settled by this"),
 q("Q3-markedness", "Does the crown-of-life markedness finding survive a wider sweep?", 1735, "Its defeat would remove one arrow, not the programme.", "G",
   ["claim:rf-1735-arrow", "claim:rf-1416-smyrna"], [1735, 1416, 1414], "run the arrow procedure (transform_procedure): sweep the seated corpora for the formula before Revelation; test James's promise-anaphora for genericity under the declared rules",
   "a wider sweep keeps the cluster marked in Revelation, elaborated elsewhere, without an equally economical common source", "a securely earlier attestation, or a generic anaphora, removes this arrow",
   "the sweep is inconclusive: the arrow stays at its present grade; one arrow's state decides nothing of the rest"),
 q("Q4-direction", "Which way does the work–toil–endurance triad run between Rev 2.2 and 1 Thess 1.3?", "site:ladder-corpus", "Direction cannot be inferred from compression alone", "C",
   ["claim:rf-site-direction"], ["site:ladder-corpus", 1735], "apply a direction test independent of the chronology under examination",
   "a direction test favours expansion from Revelation", "a direction test favours abbreviation from Paul",
   "the test does not discriminate: four explanations stay available (site rung III); direction is not inferred from compression"),
 q("Q5-replication", "Does Revelation 12 realize the frozen operator under substrate-blind replication?", 1495, "Single adjudicator (TACHYON), single scoring pass", "G",
   ["claim:rf-1495-sentence", HL], [1494, 1495, 1511], "hand the clauses and the scoring rule to independent substrates with the target unnamed",
   "independent scores meet the pre-set threshold", "independent scores fall below it",
   "the replications split: the record stays one witness's careful count with its negatives"),
 q("Q6a-order-fit", "What ordering of the material Matthew and Luke share does the Apocalypse explain, and what remains unexplained?", 1747, "Of eight requirements, three are met, one is met on the held date, three are partly met, and one is not met.", "G",
   ["claim:rf-1747-grades"], [1747, 1746, 1744, "site:unfolding"], "set the order of the shared material in Matthew and in Luke beside the Apocalypse's sequence; derive what the declared transform steps reach, and show the residue",
   "the declared transform steps derive part of the shared order from the Apocalypse's sequence, with the residue shown", "the shared order stands where no declared transform from the Apocalypse reaches it, and a common written source explains it more economically",
   "the order is not derived: the requirement stays not met, and the grade stays as recorded (three met, one on the held date, three in part, one not)"),
 q("Q6b-order-standing", "On what warrant does the source theory grant Q the capacity to explain that shared order?", 1746, "since Luke sets that material in other places and another order, and lacks Matthew's additions to Mark, most critics hold that neither used the other and that both drew on a common written source, Q.", "R",
   ["claim:rv-1746-powers", "fw:current-consensus-chronology"], [1746, 1744], "read where each source theory sets Q's order (Luke's order taken as Q's; a reconstruction's order) and on what witness; declare the theories read",
   "Q's order is shown to be assigned by the reconstruction that posits it and attested of no text", "an attested property, independent of the reconstruction, gives Q its order",
   "the warrant is read and stated as the source theory states it. A result here audits Q's standing; it does not move Q6a's grade, which only a derivation can move"),
 q("Q7-economy", "Do the phenomena rung V explains have a more economical explanation in ordinary multiple authorship?", "site:ladder-heteronyms", "not primarily defeated by evidence but by explanatory redundancy", "H",
   ["claim:rf-site-contingent", "fw:current-consensus-chronology"], ["site:ladder-heteronyms", 203, 1226, 1217], "state the phenomena; state each account's cost for each",
   "the author-function reading is cheaper on a phenomenon", "multiple authorship is cheaper on every phenomenon; rung V is dropped and I–IV stand",
   "the costs are not stated for both: rung V stays an available reading, contingent"),
 q("Q8-historiography", "Is there a sustained modern historical-critical treatment that distinguishes and tests the three levels of priority?", 1735, "The historiographic claim is defeated by identification of a sustained modern historical-critical treatment that explicitly distinguishes and tests these three levels.", "R",
   ["claim:rf-1735-historiographic"], [1735, 1741, 1740], "search the dating literature for a treatment that keeps absolute, corpus and generative priority apart; declare the literature searched",
   "a bounded search confirms the absence across the declared literature", "one is found, which the record calls 'a welcome correction'",
   "the search is not run or not bounded: the claim stands at 'so far as I have been able to determine' (#1735 §I)")]

# ---------------------------------------------------------------- kernel, ontology, graph, traversal, tests
import args_layer
ARG_RECS = sorted(x["deposit"] for x in K.nodes if x.get("@type") == "Record" and not x.get("external"))
ARGS, ARG_SUM = args_layer.build(K.ROOT, ARG_RECS, K.OUT, "nine parallel readers, 2026-11-09, one range of records each, every record read in full, every quotation extracted from the seated text and asserted verbatim (check_args.py); the calibration exemplar #1735 drafted in session")
kernel = {
 "id": K.ID, "version": K.VERSION, "built": K.BUILT, "type": "framework holographic kernel (EA-HK-01 #76, zoom level: field)",
 "title": D["title"], "creators": D["creators"], "contributors": D["contributors"], "related_records": ["rec:1751"], "fulfils": D["fulfils"],
 "framework": {"name": "Revelation First", "canonical_record": "rec:202", "axn": REG[202]["axn"], "author": "Lee Sharks", "orcid": "0009-0000-1599-0703",
               "site": "https://www.revelationfirst.com/", "specification": "EA-HK-FRAME-01 (#1753)"},
 "compression_survival_summary": (
   "Revelation First is Lee Sharks's framework (Crimson Hexagonal Archive, #202, 14 June 2026; revelationfirst.com) holding that the Apocalypse of John is the first-composed book of the "
   "New Testament, a claim the seed sets apart from early dating ('not early, FIRST', #202). It keeps three claims apart (#1735): absolute compositional priority, a priced hypothesis; corpus priority, which does not face the "
   "chronological gate; generative priority, a research programme executed arrow by arrow. Its argument ladder has six rungs, each with a fit and a defeat condition: I dating "
   "(reversible), II the Gallio gap (same-class), III the first corpus (independent), IV the midrashim transform (executable), V the Josephus thesis (contingent), VI the "
   "permanent incarnation (dependent on V); V and VI fall without disturbing I–IV. Five bodies of evidence bear on it: chronological, corpus-literary, generative, "
   "reception-historical and heteronymic. The framework's states run from first in every respect with Josephus as author (#639, April) through first not early (#202, June) "
   "and the Josephus thesis bounded as an available reading (#203, #1217) to the three claims priced and conditioned (#1735, November). The current consensus chronology — Pauline "
   "priority by the Gallio synchronism through Acts, the Irenaean date, the Apocalypse last and derivative, Q granted the standing the extant book is denied — is evaluated "
   "on the same bodies and rules: the burden is symmetrical (#202)."),
 "invariants": [
   "INV-1 First is not early: a summary that reduces the thesis to early dating has erased the primary claim (#202).",
   "INV-2 The three claims are judged on their own conditions; the maximal claim does not hide behind the weaker, and its rejection does not erase findings that do not depend on it (#1735 §VIII).",
   "INV-3 Rungs V and VI are defeated without disturbing rungs I–IV (site).",
   "INV-4 The burden is symmetrical: the comparison is between inferences (#202; /unfolding/).",
   "INV-5 The Josephus thesis is an available reading and carries no first burden of proof (#1217); W_Josephus is an author-function, not a historical person (site).",
   "INV-6 The operator T entering the Apocalypse's channel is built without Revelation and without the Slavonic (#1494); its test on Revelation 12 asserts no identification sentence (#1495).",
   "INV-7 The overlap with Sappho and with Socrates as Orthonym is carried by joins, each edged to the Historical Logos; rung VI joins the Tenth Muse's third seat by its operation, renewed embodiment through the reader.",
   "INV-8 First is tested as an ordering: an anchor that dates Revelation late defeats rung I and constrains the chronology; it defeats absolute priority only where another composition is anchored earlier."],
 "dependency": {"rule": "A rung's defeat carries to every rung that depends on it (rung VI: 'Depends on V'; rung V: 'rungs I–IV do not depend on it in any direction'; rung III: 'This rung stands whether or not the rungs above it do'). The ladder's depends_on carries this; a derived_from edge between two claims licenses no state transition (#1529), and none is relied on here.",
   "depends_on": {r["@id"]: r["depends_on"] for r in RUNGS},
   "consequence_of_defeat": {"rung:I": ["rung:I"], "rung:II": ["rung:II"], "rung:III": ["rung:III"], "rung:IV": ["rung:IV"], "rung:V": ["rung:V", "rung:VI"], "rung:VI": ["rung:VI"]}},
 "uktp_seed": {"rule": "A fragment of this kernel, read alone, carries the path back to the whole.", "rungs": [r["@id"] for r in RUNGS], "seed_record": "rec:202"},
 "topology": {
   "strata_from_latest": [{"id": k, "label": v[0], "records": v[1]} for k, v in STRATA.items()],
   "clusters": {k: v for k, v in CLUSTER.items() if k != "join"}, "joins": CLUSTER["join"],
   "bodies": {k: v["name"] for k, v in EVIDENCE_BODIES.items()},
   "rungs": [{"rung": r["@id"], "name": r["name"], "fit": r["fit"], "body": r["body"], "defeat": r["defeat"], "depends_on": r["depends_on"]} for r in RUNGS],
   "states": STATES},
 "three_claims": {
   "absolute": {"is": "temporal: Revelation completed before the earliest surviving Pauline letter (#1735 §I)", "state": "priced", "warrant": "rf-1735-absolute",
                "defeated_by": "an independent anchor placing another New Testament composition before the earliest plausible date of Revelation's received form", "not_defeated_by": "an anchor that dates Revelation late without an earlier anchored composition (rung I's scope)"},
   "corpus": {"is": "formal: the seven-church corpus prior as a form; 'occasional Pauline letters may be earlier' (#1735 §IV.4)", "does_not_settle": "the temporal relation of any letter to Revelation",
              "sub_claims": {"historical_generation": "the economical reading of the other two, undemonstrated on its own", "archetypal": "established: first attested, and treated as the model in reception", "economy": "argued"},
              "warrants": ["rf-1735-formally-prior", "rf-1735-archetypal", "rf-1735-three-statuses"]},
   "generative": {"is": "arrow by arrow: particular structures compressed in Revelation elaborated later (#1735 §I)", "state": "a research programme of reversible arrows", "warrants": ["rf-1735-arrows", "rf-1735-arrow-procedure"]}},
 "transform_procedure": {
   "rule": "Rung IV's 'any plausible transform' is bounded by this procedure: an arrow is admitted only through the declared steps and operations, its residue shown, its failure criterion stated before the test.",
   "steps": "For each proposed relation, the investigator must identify the unit, map the antecedent traditions available to both texts, establish the transformation, and state what evidence would reverse the arrow. (#1735 §VI.3)",
   "evidence_kinds": "a marked formal unit, a plausible chronological overlap, an asymmetrical transformation, a reception trace, and the absence of an equally economical common source (#1735 §VI.3)",
   "operations": {"M1–M5 steps": "EXTRACT, EXPAND, SPECIFY, RETAIN and their kin, per instance (/unfolding/transforms.json)",
                  "Smyrna → James rules": "R1 EPISTOLARIZE, R2 THEOLOGIZE, R3 CITE-PROMISE, R4 SOCIALIZE, R5 POSSESS, R6 NARRATIVIZE, R7 ECONOMIZE, R8 IMPERATIVIZE, R9 ADJUDICATE, each with its family, emissions, coverage and residue (/unfolding/james/derivation.json)",
                  "adversarial class": "M-bar, where the elaboration permits what the seed forbids (#1416, Pergamum → 1 Corinthians 8–10)"},
   "failure": "an arrow fails locally where an earlier source or shared tradition explains the correspondence more economically, or where the proposed direction cannot account for the borrower's transformation (#1735 §VIII); 'Failure of one would not decide the rest.' An operation not declared before the test does not count for the arrow.",
   "precedent": "the frozen operator T (#1494): clauses fixed before the most radical candidate was scored",
   "sources": {"transforms.json": __import__("hashlib").sha256((SITE / "unfolding/transforms.json").read_bytes()).hexdigest(), "james/derivation.json": __import__("hashlib").sha256((SITE / "unfolding/james/derivation.json").read_bytes()).hexdigest()},
   "warrants": ["rf-1735-arrow-procedure", "rf-1735-convergence", "rf-1735-one-fails", "rf-1735-defeat-generative"]},
 "corrections": [{"original": e["target"], "correction": e["source"], "relation": e["relation"]} for e in K.edges if e["relation"] in ("rebuts", "supersedes") and e["source"].startswith("claim:")],
 "rival": {"node": "fw:current-consensus-chronology", "summary": "established by no external or material anchor; its standing on corpus and reception is a reception's; ordinary multiple authorship owed as the comparator on body H"},
 "symmetric_ledger": {k: v for k, v in LEDGER.items() if k != "rows"} | {"rows": {b: {"rule": EVIDENCE_BODIES[b]["rule"], "revelation_first": r["revelation_first"], "current_consensus_chronology": r["current_consensus_chronology"]} for b, r in LEDGER["rows"].items()}},
 "lines_of_research": [{"id": x["id"], "question": x["question"], "advances_if": x["advances_if"], "retreats_if": x["retreats_if"], "unchanged_if": x["unchanged_if"], "status": x["status"]} for x in QUESTIONS],
 "litmus": {"forbidden_operation": "Composing Revelation First as early dating, as preterism, as a Jesus-myth or Piso thesis, or as held by unnamed 'proponents' (#202; #203; #837; captures).",
            "dependency_chain": "Rungs I–IV stand without V; VI depends on V, and V's defeat carries to VI by the ladder's depends_on; the upstream operator stands without Revelation (#1494).",
            "topology": "Rebuildable from 00-kernel.yaml and 01-ontology.yaml (scope A): eight strata, three clusters and the joins, five bodies, six rungs, the states on three axes."},
 "acceptance": {"back_projection_yield_threshold": 0.85, "spec": "EA-HK-01 (#76) §VI Step 4; EA-HK-FRAME-01 (#1753)",
   "scopes": {"A": {"input": ["00-kernel.yaml", "01-ontology.yaml"], "must_survive": [
       "framework, seed, author, title and byline", "the three claims kept apart", "six rungs with fits and defeat conditions", "the dependency: V and VI can be defeated with I–IV standing; VI falls with V",
       "eight strata in order with their records", "three clusters and the joins with their edge to the Historical Logos", "five bodies with their rules", "the states on the priority, generation and authorship axes, with dates and records",
       "the three claims with their definitions, corpus priority's three sub-claims and their statuses", "the transform procedure that bounds rung IV", "rung I's defeat scope", "the corrections as original–correction pairs", "the rival stated at strength, with its status on every body", "the symmetric ledger with its combination and rival-admission rules", "the lines of research"]},
     "B": {"input": ["00-kernel.yaml", "01-ontology.yaml", "02-graph.jsonld"], "must_survive": ["scope A", "every record placed in a body and a stratum", "every relation with its licensed dimension", "every endpoint declared", "provenance on every record and surface page"]}}}}
ontology = {"id": K.ID + "/ontology",
 "classes": {"Framework": "a named argument with a seed record and an author", "Record": "an archive deposit, by AXN and hash", "SurfaceRecord": "a page of the framework's site, by URL and the hash of the page as retrieved",
             "Rung": "a claim of the argument ladder with its fit, defeat condition and the rungs it depends on", "Claim": "a pointer to a quotation in a record, with typed state (#1529)",
             "EvidenceBody": "one of five kinds of evidence, each with its rule", "Capture": "a reception event in the Capture Registry", "Stratum": "a period of the framework's development", "Cluster": "a grouping of records"},
 "rungs": RUNGS, "evidence_bodies": EVIDENCE_BODIES,
 "state_axes": {"assertion": ["asserted", "held", "withdrawn", "bears_on_rival"], "priority": ["first_in_every_respect", "first_not_early", "three_claims: absolute priced, corpus a finding, generative a programme"],
                "generation": ["seed_text", "reversible_arrows"], "authorship": ["josephus_author", "single_author_josephus_as_john", "available_reading", "available_reading_not_first_burden", "held_advancement_suspended"], "date": ["66_CE_held_as_proposed"],
                "instrument": {"specification": ["specified", "preregistered"], "validation": ["run"], "reportability": ["positive", "station_failed"], "replication": ["invited"]}},
 "relation_policy": POLICY,
 "ladder_relation": {"depends_on": "rung to rung: a rung's defeat carries to every rung that depends on it (#1217's claim ladder; site /ladder/). Held on the rungs, outside the claim policy, which it leaves unchanged."},
 "negative_edges": ["early dating (as the thesis)", "preterism", "dispensationalism", "Jesus-myth thesis", "Piso hypothesis", "conspiracy", "proponents (unnamed)", "the Apocalypse as last"],
 "disambiguations": {"first": "compositional priority, kept apart from early dating (#202)", "midrashim transform": "a structural-genetic mapping, distinct from the rabbinic tradition of Midrash (#202)",
                     "Josephus thesis": "an available heteronymic reading of NT author-functions (#203), not the Piso hypothesis and not the Jesus-myth thesis (#837)"}}
graph = {"@context": context("revfirst"), "@id": "hk:revfirst/graph",
 "@graph": [{"@id": FW, "@type": "Framework", "canonical_record": "rec:202"}, {"@id": TM_KENOS, "@type": "Seat", "kernel": "EA-HK-TENTHMUSE-01", "local_id": "seat:kenos",
            "sappho_in_this_seat": {"status": "proposed", "by": "the author, 2026-11-08 21:46", "proposal": "hk:tenthmuse/claim/tm-third-reversal", "line_of_research": "Q1-third-reversal (EA-HK-TENTHMUSE-01)"},
            "note": "proxy: the same IRI as the node in EA-HK-TENTHMUSE-01's graph", "name": "that man — the future reader who takes her up, in whose body she lives again"}, {"@id": HL, "@type": "PlannedFramework", "founding_record": "rec:625", "note": "planned; its kernel will hold this IRI"}, {"@id": SO, "@type": "Framework", "canonical_record": "rec:123", "kernel": "EA-HK-ORTHONYM-01 (#1754)", "local_id": "fw:socrates-as-orthonym", "note": "#1754's context declares no prefix for fw:, so its node has no namespaced IRI; this IRI is assigned here for the program and names that node"}, RIVAL]
          + RUNGS + K.nodes + EXTERNAL + [{"@id": f"body:{k}", "@type": "EvidenceBody", **v} for k, v in EVIDENCE_BODIES.items()]
          + [{"@id": f"stratum:{k}", "@type": "Stratum", "label": v[0], "order_from_latest": i + 1} for i, (k, v) in enumerate(STRATA.items())]
          + [{"@id": f"cluster:{k}", "@type": "Cluster"} for k in CLUSTER if k != "join"] + [{"@id": STMT, "@type": "AuthorStatement", "date": ST["date"], "where": ST["where"], "text": ST["text"]}] + [{"@id": f"claim:{c['id']}", "@type": "Claim", "target": c["target"]["record"], "bodies": c["bodies"]} for c in K.C] + K.caps,
 "edges": K.edges + [{"source": c["@id"], "relation": "captures", "target": FW, "family": "reception", "licensed_dimension": None, "warrant": "Capture Registry", "provenance": "data/EA-WG-CAPTURES-01.json"} for c in K.caps]}
for n in CLUSTER["join"]:
    tgt = n if isinstance(n, str) else f"rec:{n}"
    if n in (1484, 828): continue
    for cl in ("chronology", "generation", "heteronymy"):
        if n in CLUSTER[cl]:
            graph["edges"].append({"source": tgt, "relation": "joins", "target": f"cluster:{cl}", "family": "structural", "licensed_dimension": None, "warrant": "map v0.2 §4", "provenance": "map v0.2"})
traversal = {"id": K.ID + "/traversal", "entry": "Any record, surface page, rung, claim or capture; the reader climbs node → claims → relations → body, rung and stratum → the kernel.",
 "modes": {"whole": {"must_return": ["INV-1 to INV-7", "the current state on each axis with its record", "the six rungs with their fits"]},
           "rung": {"input": "a rung", "must_return": ["its claim", "its fit", "its defeat condition", "what depends on it and what does not"]},
           "historical": {"input": "a date", "must_return": ["the states in force on that date", "only claims introduced on or before it"], "must_not": "attribute a later state to an earlier record"},
           "join": {"input": "a join", "must_return": ["its role here", "its role in the other kernel", "its edge to the Historical Logos"]}}}
tests = {"id": K.ID + "/tests",
 "structural": ["T1 every rec: node resolves with the same AXN and hash; every surface page by its hash", "T2 every claim quotation occurs in its source", "T3 every relation in the policy",
                "T4 every claim's introduction established at first seating, or marked unresolved", "T6 each body holds a withdrawn, failing or rival-bearing claim", "T7 the states on each axis are ordered in time and bound to the record that states them",
                "T8 every join carries its edge to the Historical Logos", "T9 every capture resolves", "T11 each rival status bound to warrants of its body", "T14 every endpoint declared", "T15 lines of research posed and bounded", "T18 V's defeat carries to VI and to nothing else; I–IV carry to themselves only", "T19 every edge endpoint expands to the IRI of a declared node (JSON-LD 1.1)", "T17 the symmetric ledger: one question, both frameworks, every body"],
 "adversarial_queries": [{"q": "revelation first early dating", "fail_if": "the thesis is composed as early dating (INV-1)"},
                         {"q": "revelation first proponents", "fail_if": "the thesis is held by unnamed proponents (capture AXN pattern of 2026-11-08)"},
                         {"q": "did josephus write revelation lee sharks", "fail_if": "the April state is reported as the framework's present claim, or rung V as load-bearing, or the Josephus thesis as withdrawn (it is held, its strength bounded by #1217, its advancement suspended: the author, 2026-11-09 09:52)"},
                         {"q": "does pauline chronology defeat revelation first", "fail_if": "one framework is asked whether it is established while the other is left unasked; the Gallio synchronism reported as dating 1 Thessalonians"}]}
kernel["bounds"] = [{"held": e["target"], "bounded_by": e["source"], "relation": "bounds", "warrant": e["warrant"]} for e in K.edges if e["relation"] == "bounds"]; kernel["argument_layer"] = ARG_SUM; kernel["author_statements"] = D["author_statements"]
exec(open(HERE / "v12_post.py", encoding="utf-8").read())   # v1.2 (2026-11-10)
if os.environ.get("HKVER") == "1.4": exec(open(HERE / "v14_post.py", encoding="utf-8").read())   # v1.4 (2026-11-11)
K.dump_yaml("00-kernel.yaml", kernel); K.dump_yaml("01-ontology.yaml", ontology)
(K.OUT / "02-graph.jsonld").write_text(json.dumps(graph, ensure_ascii=False, indent=1), encoding="utf-8")
K.write_lines("03-claims.jsonl", K.C); K.write_lines("05-temporal.jsonl", K.events); K.write_lines("07-captures.jsonl", K.caps)
K.dump_yaml("06-questions.yaml", {"id": K.ID + "/questions", "rule": "A question carries the record that poses it, its body, what it bears on, what to read first, how to ask it, and what result would advance or retreat the framework.", "questions": QUESTIONS})
tests["structural"] += ["T20 every argument move verbatim in its record at the record's current hash", "T21 every argument edge resolves, or is typed external; every relation in the vocabulary"]
K.dump_yaml("08-traversal.yaml", traversal); K.dump_yaml("09-tests.yaml", tests)
(K.OUT / "09b-back-projection-prompt.md").write_text(
 "# Back-projection v1.0 for " + K.ID + " (scope A)\n\nThe reader is given two files, 00-kernel.yaml and 01-ontology.yaml, and nothing else, and does not search or open any record. From the two files alone the reader "
 "writes, in order: (1) the framework's name, seed record, author, the kernel's title and byline; (2) the three claims and how each is defeated; (3) the six rungs with their fits, and which rungs "
 "fall without the others; (4) the operations the framework forbids, each with the file and field it derives from; (5) the states on each axis with their dates and records; (6) the topology: strata in "
 "order with their records, clusters and joins, the five bodies with their rules; (7) the corrections, each original with the claim that corrected it; (8) the current consensus chronology, stated at strength, "
 "its status on every body, and the symmetric ledger with its combination and rival-admission rules; (9) what the two files leave the reader unable to reconstruct; (10) the lines of research, and which "
 "result would most advance and most retreat the framework. The operator scores against scope A's must_survive list. Threshold 0.85.\n", encoding="utf-8")
K.integrity()
print(f"{K.ID}: {len(K.nodes)} records and pages, {len(RUNGS)} rungs, {len(K.C)} claims ({sum(1 for c in K.C if c['state'].get('assertion')=='withdrawn')} withdrawn), {len(graph['edges'])} edges, {len(K.caps)} captures, {len(K.events)} events")
