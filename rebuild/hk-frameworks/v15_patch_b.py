#!/usr/bin/env python3
"""v1.5 of EA-HK-REVFIRST-01, second stage (2026-11-26), applied after v15_patch.py to the same kernel directory. At the author's word:
  12:21  "scan for anything thats built since the hologram... and anything we missed on the first pass that would strengthen it"
  12:25  "and if it doesnt have it yet, it needs a compressed hologram of the unfoldings ... so this is, a mapping of whats there + an outline"
Three things: (D) rung VI recoded independent of V, on the author's ruling of 2026-11-09 12:48, which the site has carried since that day and the kernel v1.1–v1.4 did not;
the two ladder pages re-bound to their current hashes; (E) four records the scan found (#1798 and #1802 since the first kernel; #65 and #1738 missed on the first pass),
each with anchor claims quoted verbatim; (F) the unfoldings: every arrow drawn from Revelation to another New Testament book, at its grain and state, a table by book
computed from the arrows, and an outline of the total programme, marked as an outline.
    python3 v15_patch_b.py <alexanarch root> <kernel dir> <revelationfirst-com root>"""
import json, sys, pathlib, re, hashlib, subprocess, yaml, html
ROOT, KD, SITE = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
norm = lambda s: re.sub(r"\s+", " ", s.replace("*", "").replace("’", "'").replace("‘", "'"))
BUILT = "2026-11-26"
dump_yaml = lambda p, o: (KD / p).write_text(yaml.safe_dump(o, allow_unicode=True, sort_keys=False, width=140), encoding="utf-8")
lines = lambda p: [json.loads(l) for l in (KD / p).read_text(encoding="utf-8").splitlines() if l.strip()]
write_lines = lambda p, rows: (KD / p).write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
K = yaml.safe_load((KD / "00-kernel.yaml").read_text(encoding="utf-8")); assert str(K["version"]) == "1.5" and "unfoldings" not in K
O = yaml.safe_load((KD / "01-ontology.yaml").read_text(encoding="utf-8"))
G = json.loads((KD / "02-graph.jsonld").read_text(encoding="utf-8")); C = lines("03-claims.jsonl"); E = lines("05-temporal.jsonl")
T9 = yaml.safe_load((KD / "09-tests.yaml").read_text(encoding="utf-8")); I = yaml.safe_load((KD / "11-integrity.yaml").read_text(encoding="utf-8"))
nodes = {x["@id"]: x for x in G["@graph"]}; CL = {c["id"]: c for c in C}
text = lambda n: (ROOT / REG[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
git = lambda root, *a: subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True).stdout
SITE_HEAD = git(SITE, "rev-parse", "--short", "HEAD").strip(); SITE_DATE = git(SITE, "log", "-1", "--format=%ad", "--date=short").strip()
page = lambda sid: SITE / nodes[sid]["url"].split(".com/", 1)[1] / "index.html"
ptext = lambda sid: norm(html.unescape(re.sub(r"<[^>]+>", " ", page(sid).read_text(encoding="utf-8"))))
_FIRST = {}
def introduced(n, quote):
    r = REG[n]; p = r["full_text_path"].lstrip("/")
    if p not in _FIRST:
        log = git(ROOT, "log", "--diff-filter=A", "--format=%h %ad", "--date=short", "--", p).strip().splitlines()
        _FIRST[p] = (log[-1].split()[:2] + [git(ROOT, "show", f"{log[-1].split()[0]}:{p}")]) if log else None
    base = {"record_date": r["date"]}
    if _FIRST[p]:
        h, d, first = _FIRST[p]; base.update({"first_seating": d, "first_seating_commit": h})
        if norm(quote) in norm(first):
            return {"date": d, "basis": "present at the record's first seating in this repository", "first_text_sha256": hashlib.sha256(first.encode("utf-8")).hexdigest(), **base,
                    **({"note": "the record is dated earlier than its first seating here; presence before the first seating is not attested by this repository"} if r["date"] < d else {})}
    return {"date": None, "basis": "present in the current version; introduction date unresolved", **base,
            "current_version_since": (r.get("reissue_history") or [{}])[-1].get("date") or r.get("date_modified") or r["date"]}
NEWC = []
def claim(cid, n, quote, kind, state, body, notes=None, role="standing", bodies=None):
    assert cid not in CL, cid
    t, d = norm(text(n)), norm(REG[n].get("description") or ""); q = norm(quote)
    assert q in t or q in d, ("quotation not in record", cid, quote[:70])
    c = {"id": cid, "claim_kind": kind, "role": role, "target": {"record": f"rec:{n}", "axn": REG[n]["axn"], "record_sha256": REG[n]["hash"], "exact": quote, "located_in": "text" if q in t else "description"},
         "state": state, "body": body, "introduced": introduced(n, quote), "bodies": bodies or {body: "principal"}}
    if notes: c["notes"] = notes
    C.append(c); CL[cid] = c; NEWC.append(cid)
    G["@graph"].append({"@id": f"claim:{cid}", "@type": "Claim", "target": f"rec:{n}", "bodies": c["bodies"]})
    E.append({"timeline": "epistemic", "date": c["introduced"]["date"], "event": "introduced", "object": f"claim:{cid}", "basis": c["introduced"]["basis"], "role": role})
A_ = lambda a="asserted", **k: {"assertion": a, **k}

# ---------------------------------------------------------------- (D) rung VI: independent of V; V would strengthen it
PROGRAMME = ("in fact - its time we built that map. we have some preliminary mappings that will allow us to experiment with the whole. heres what im imagining: we have the four riders, the four creatures, "
             "the four names, and the four gospels. and we have a specific mapping to matthew with the mourning tribes. we can press into the matthew mapping, define a transform algorithm that describes the "
             "transformation of revelation materials to matthew, then use that to work out the other three. same with the epistles. we have james. what im imagining well find is a seven within seven structure: "
             "the seven church pauline formation transformed from rev's seven churches, but then also paul as one of seven and the other named epistolary positions mapped to rev's seven. its time we mapped it out.")
RULING_D = {"at": "2026-11-09 12:48", "text": "rung vi does not depend on v. but v would of course strengthen vi if the entire material transmission and production chain could be shown to work by means of self-division",
            "provenance": "revelationfirst-com commit 264e07b (2026-11-09), which changed the ladder pages for V and VI and the homepage and left the deposited hologram page 'as deposited'"}
DEFEAT_VI = "Independent of V; V would strengthen it. Defeated without disturbing rungs I–IV."
assert norm(DEFEAT_VI) in ptext("site:ladder-logos")
dep = K["dependency"]; dep_before = {"depends_on": list(dep["depends_on"]["rung:VI"]), "consequence_of_defeat": list(dep["consequence_of_defeat"]["rung:V"])}
assert dep_before["depends_on"] == ["rung:V"]
dep["depends_on"]["rung:VI"] = []; dep["consequence_of_defeat"]["rung:V"] = ["rung:V"]
dep["strengthened_by"] = {"rung:VI": ["rung:V"]}
dep["rule"] = ("A rung's defeat carries to every rung that depends on it. No rung depends on another: rung VI is 'Independent of V; V would strengthen it' (the author, 2026-11-09 12:48; site rung VI); "
               "rung V: 'rungs I–IV do not depend on it in any direction'; rung III: 'This rung stands whether or not the rungs above it do'. strengthened_by carries no defeat. "
               "A derived_from edge between two claims licenses no state transition (#1529), and none is relied on here. v1.0–v1.4 carried 'rung VI depends on V'; corrected at v1.5.")
for r in list(K["topology"]["rungs"]) + list(O["rungs"]) + [x for x in G["@graph"] if x.get("@type") == "Rung"]:
    if (r.get("rung") or r.get("@id")) == "rung:VI":
        r.update({"fit": "INDEPENDENT", "depends_on": [], "strengthened_by": ["rung:V"], "defeat": DEFEAT_VI})
O["ladder_relation"]["strengthened_by"] = "rung to rung: the standing of one rung would add to another's; no defeat is carried (rung VI by V; the author, 2026-11-09)."
e_dep = [e for e in G["edges"] if e["source"] == "rung:VI" and e["relation"] == "depends_on"]; assert len(e_dep) == 1
e_dep[0].update({"source": "rung:V", "relation": "strengthens", "target": "rung:VI", "carries": "nothing on defeat",
                 "warrant": "site:ladder-logos 'Independent of V; V would strengthen it.'; the author, 2026-11-09 12:48", "provenance": "site /ladder/ @ 264e07b; map v1.5 (before: rung:VI depends_on rung:V)"})
for e in G["edges"]:
    if e.get("status", "").startswith("rung VI dependent on V"): e["status"] = e["status"].replace("rung VI dependent on V", "rung VI independent of V, which would strengthen it (corrected v1.5)")
K["compression_survival_summary"] = K["compression_survival_summary"].replace("VI the permanent incarnation (dependent on V)", "VI the permanent incarnation (independent of V, which would strengthen it)")
assert "independent of V, which would strengthen it" in K["compression_survival_summary"]
K["symmetric_ledger"]["rows"]["H"]["revelation_first"]["text"] = K["symmetric_ledger"]["rows"]["H"]["revelation_first"]["text"].replace(
    "the Logos rung depends on V (rung VI)", "the Logos rung is independent of V, which would strengthen it (rung VI)")
K["litmus"]["dependency_chain"] = "Rungs I–IV stand without V; VI is independent of V, and V's defeat carries to nothing but V; V would strengthen VI; the upstream operator stands without Revelation (#1494)."
T9["structural"] = [("T18 no rung's defeat carries to another: V's defeat carries to V only (v1.0–v1.4: 'to VI'); VI is strengthened by V" if s.startswith("T18") else s) for s in T9["structural"]]
# the two ladder pages changed on 2026-11-09 (264e07b; 882278a): re-bind, every quotation re-asserted against the page
rebound_pages = []
for sid in ("site:ladder-heteronyms", "site:ladder-logos"):
    h = hashlib.sha256(page(sid).read_bytes()).hexdigest(); before = nodes[sid]["sha256"]; assert h != before
    ret = f"{BUILT} (repository @ {SITE_HEAD}, {SITE_DATE})"; pt = ptext(sid)
    nodes[sid].update({"sha256": h, "retrieved": ret}); I["surfaces"][sid] = h
    for c in C:
        if c["target"]["record"] == sid:
            assert norm(c["target"]["exact"]) in pt, ("quotation no longer on the page", c["id"])
            c["target"]["page_sha256"] = h; c["introduced"].update({"retrieved": ret, "page_sha256": h})
    rebound_pages.append({"page": sid, "sha256_before": before, "sha256": h, "changes": "264e07b: rung VI independent of V; 882278a: rung V joined to the Josephus Thesis narrative (#1759)"})
for sid in I["surfaces"]: assert hashlib.sha256(page(sid).read_bytes()).hexdigest() == I["surfaces"][sid], sid
c = {"id": "rf-site-vi-independent", "claim_kind": "generality", "role": "standing",
     "target": {"record": "site:ladder-logos", "url": nodes["site:ladder-logos"]["url"], "page_sha256": nodes["site:ladder-logos"]["sha256"], "exact": DEFEAT_VI, "located_in": "text"},
     "state": A_(rung="VI"), "body": "H", "introduced": {"date": "2026-11-09", "basis": "the site's commit 264e07b, at the author's ruling of 12:48 that day", "retrieved": nodes["site:ladder-logos"]["retrieved"],
                                                          "page_sha256": nodes["site:ladder-logos"]["sha256"]}, "bodies": {"H": "principal"}}
C.append(c); CL[c["id"]] = c; NEWC.append(c["id"]); G["@graph"].append({"@id": "claim:rf-site-vi-independent", "@type": "Claim", "target": "site:ladder-logos", "bodies": c["bodies"]})
E.append({"timeline": "epistemic", "date": "2026-11-09", "event": "introduced", "object": "claim:rf-site-vi-independent", "basis": c["introduced"]["basis"], "role": "standing"})
E.append({"timeline": "epistemic", "date": "2026-11-09", "event": "ruled", "object": "rung:VI", "note": "the author: rung VI does not depend on V; V would strengthen it. Carried by the site from that day; by this kernel from v1.5"})
K["symmetric_ledger"]["rows"]["H"]["revelation_first"]["warrants"].append("rf-site-vi-independent")
K["author_statements"].append({"date": "2026-11-09T12:48-05:00", "where": RULING_D["provenance"], "text": RULING_D["text"],
                               "status": "the author's position on rung VI: independent of V; V would strengthen it. Not carried by this kernel until v1.5"})
K["author_statements"].append({"date": "2026-11-26T12:35-05:00", "where": "in session, while this version was being built", "text": PROGRAMME,
                               "status": "the programme of the total unfolding, stated as what the author imagines will be found; carried in unfoldings.outline_of_the_total_programme"})
K["corrections_history"].append({"original": "rung:VI depends_on rung:V", "correction": "rung:VI independent of rung:V; strengthened_by rung:V", "in_versions": "v1.0–v1.4",
                                 "status": "corrected at v1.5 on the author's ruling of 2026-11-09 12:48, found when the ladder pages failed their hashes"})

# ---------------------------------------------------------------- (E) records from the scan
SID = "S00-after-the-first-kernel"
NEW = {1802: ("R", ["D", "G"], ["chronology"], SID), 1798: ("H", ["R"], ["heteronymy"], SID),
       65: ("H", ["G"], ["heteronymy"], "S6-space-ark"), 1738: ("D", [], ["chronology"], "S1-standing-audited")}
have = {x["deposit"] for x in G["@graph"] if x.get("@type") == "Record"}; assert not (set(NEW) & have)
for n, (b, sec, cls, sid) in NEW.items():
    r = REG[n]; assert f"stratum:{sid}" in nodes
    G["@graph"].append({"@id": f"rec:{n}", "@type": "Record", "deposit": n, "axn": r["axn"], "url": f"https://www.alexanarch.org/s/records/{n}/", "title": r["title"], "date": r["date"],
                        "status": r.get("status"), "version": r.get("version"), "sha256": r["hash"], "creator": r.get("creator") or r.get("authors"), "body": b, "body_secondary": sec,
                        "stratum": sid, "clusters": cls, "entered": "v1.5", **({"first_pass": "missed at v1.0–v1.4; found by the scan of 2026-11-26"} if sid != SID else {})})
    for tgt in (f"body:{b}", f"stratum:{sid}"):
        G["edges"].append({"source": f"rec:{n}", "relation": "belongs_to", "target": tgt, "family": "structural", "licensed_dimension": None, "warrant": "map", "provenance": "map v1.5"})
    E.append({"timeline": "historical", "date": r["date"], "event": "deposited", "object": f"rec:{n}", "axn": r["axn"]})
    for c_ in cls: K["topology"]["clusters"][c_].append(n)
RIVAL = dict(assertion="bears_on_rival", rival="fw:current-consensus-chronology")
claim("rv-1802-order", 1802, "On that account the order of the collection is the order of composition.", "interpretation", dict(RIVAL), "R",
      notes="§13.1, the received reading stated first: the Apocalypse last, written late, receiving from the gospels and Paul.")
claim("rv-1802-existence-tax", 1802, "The extant book pays the Existence Tax; the reconstruction is exempt", "interpretation", dict(RIVAL, standing="granted to reconstructed sources"), "R")
claim("rv-1802-filing", 1802, "the filing removes the question whose answer would test it", "generality", dict(RIVAL), "R",
      notes="§13.6: dependence on Philo is heard for Hebrews and filed for the Apocalypse (#1758 §16.4a).")
claim("rf-1802-pin", 1802, "The pin that blocks its test.", "interpretation", A_(rung="II"), "D", bodies={"D": "principal", "G": "secondary"},
      notes="§13.5, on Rev 2.2 and 1 Thess 1.3: 'the pinning is, demonstrably, the only thing withholding it' (#1735 §V).")
claim("rf-1798-governs", 1798, "The direction of dependence is the question at issue, and it is settled by citing a history whose antecedents were inferred from the same texts.", "interpretation", A_(rung="II"), "R",
      bodies={"R": "principal", "D": "secondary"})
claim("rf-1798-neither-proves", 1798, "It does not rest on the genre conclusion of §2, and the genre conclusion does not rest on it, so neither is used to prove the other.", "generality", A_(), "R",
      notes="The bound between the essay's genre argument and the case for Revelation First: independent, and neither a premise of the other.")
claim("rf-1798-observers", 1798, "A plurality of compositions is not a plurality of observers.", "generality", A_(rung="VI"), "H")
claim("rf-1798-not-nothing", 1798, "None of this requires that nothing in the Gospels happened.", "generality", A_(rung="VI"), "H")
claim("rf-65-matrix", 65, "functioning as the generative matrix from which the gospel narratives were later composed as fulfillments", "interpretation",
      {"assertion": "held", "bounded_by": "claim:rf-1217-josephus-available", "rung": "V", "frame": "stated 'on the Josephus Thesis reading'"}, "H", bodies={"H": "principal", "G": "secondary"})
claim("rf-65-forward-library", 65, "The seven letters to the seven churches are a forward library", "interpretation", A_(rung="IV", frame="stated 'on the Josephus Thesis reading'", generation="named_not_run"), "G")
claim("rf-65-fourfold", 65, "The four living creatures specify the fourfold structure the gospel tradition will take.", "interpretation", A_(rung="IV", frame="stated 'on the Josephus Thesis reading'", generation="named_not_run"), "G")
claim("rf-1738-seat", 1738, "seated for Histories 5.13, the undated portents before the siege of Jerusalem read beside Josephus and the Apocalypse in #1737", "observation", A_(rung="I"), "D")

# ---------------------------------------------------------------- (F) the unfoldings: claims that warrant the map
claim("rf-407-sequence", 407, "The Epistles derive doctrine algorithmically", "interpretation", A_(rung="IV", grain="founding statement", generation="named_not_run"), "G",
      notes="#407 gives the sequence Revelation, Epistles, Gospels, Acts, with dates that #1735 does not carry.")
claim("rf-407-runs", 407, "multiple runs of the same algorithm", "interpretation", A_(rung="IV", grain="founding statement", generation="named_not_run"), "G",
      notes="The four Gospels as four parameter sets (#407 §V): Mark minimal, Matthew Jewish, Luke Gentile, John reflexive.")
claim("rf-639-operators", 639, "From Revelation as source, operator transformations generate the NT:", "interpretation", A_(rung="IV", grain="founding statement", generation="named_not_run"), "G")
claim("rf-1217-seed", 1217, "the letters to the seven churches become the epistolary form", "interpretation", A_(rung="IV"), "G")
claim("rf-1217-john-transform", 1217, "the Gospel-of-John opening IS a midrashim transform performed on Revelation's vision", "interpretation", A_(rung="IV", generation="named_not_run"), "G")
claim("rf-1414-five", 1414, "five canonical instances (Letters→Epistles, Lampstands→Ecclesiology, Lamb→Atonement, New Jerusalem→Eschatology, Beast→Political Theology)", "instrument",
      {"specification": "specified", "validation": "run", "reportability": "positive"}, "G")
claim("rf-1415-morphological", 1415, "The dependency arrow is morphological", "interpretation", A_(rung="IV"), "G",
      notes="Rev 2:10 performs the promise in the first-person future (doso soi); Jas 1:12 cites it in the aorist (hon epengeilato).")
claim("rf-1415-residue", 1415, "is displayed openly as the falsification surface per Workstream 4", "generality", A_(rung="IV"), "G")
claim("rf-1416-classes", 1416, "Three transform classes: M elaborative, M-bar adversarial, X mechanism.", "instrument", {"specification": "specified", "validation": "run", "reportability": "positive"}, "G")
claim("rf-1416-proportional", 1416, "with granularity proportional to evidence and grades preserved from the 2026-07-28 evaluation", "generality", A_(rung="IV"), "G")
claim("rf-1418-mbar", 1418, "Rom 13:1 as the adversarial unfolding M-bar", "interpretation", A_(rung="IV"), "G")
claim("rf-1418-shared-source", 1418, "Shared-source alternatives (Lev 26:12, Isa 65:17, Dan 7) stated in every honesty panel", "generality", A_(rung="IV"), "G")
claim("rf-1735-triad-withheld", 1735, "The markedness finding therefore stands, and the arrow is withheld", "observation", A_(rung="IV", generation="arrow_withheld_by_a_date"), "G", bodies={"G": "principal", "D": "secondary"})
claim("rf-1735-crown-run", 1735, "This section runs one such case to completion.", "observation", A_(rung="IV", generation="arrow_run"), "G")
claim("rf-1747-thief", 1747, "has the watching of Matthew and the hour of Luke in one saying", "observation", A_(rung="IV", generation="observed_awaiting_census"), "G")
claim("rf-1747-confession", 1747, "the Father of Matthew and the angels of Luke in one saying", "observation", A_(rung="IV", generation="observed_awaiting_census"), "G")
claim("rf-1747-census-owed", 1747, "two double-tradition sayings are an observation awaiting a census", "generality", A_(rung="IV"), "G")
claim("rf-1747-no-direction", 1747, "the census decides no direction", "generality", A_(rung="IV", generation="direction_open"), "G", notes="On Matt 24:30 and Rev 1:7.")
claim("rf-1746-hitzig", 1746, "argued from Matt 24:30 and Rev 1:7 that Matthew used the Apocalypse", "observation", A_(rung="IV", generation="arrow_drawn_by_others_1843_1902"), "G",
      bodies={"G": "principal", "R": "secondary"})

J = json.loads((SITE / "unfolding/james/derivation.json").read_text(encoding="utf-8")); L = json.loads((SITE / "unfolding/letters/letters.json").read_text(encoding="utf-8"))
TR = json.loads((SITE / "unfolding/transforms.json").read_text(encoding="utf-8"))
ops = lambda rules: [r["op"] for r in rules]; refs = lambda em: [m["ref"] for e in em for m in e.get("matches", [])]
BOOKS = ["Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
         "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude"]
AB = {"Matt": "Matthew", "Mark": "Mark", "Luke": "Luke", "John": "John", "Jn": "John", "Acts": "Acts", "Rom": "Romans", "1 Cor": "1 Corinthians", "2 Cor": "2 Corinthians", "Gal": "Galatians", "Eph": "Ephesians",
      "Phil": "Philippians", "Col": "Colossians", "1 Thess": "1 Thessalonians", "2 Thess": "2 Thessalonians", "2 Tim": "2 Timothy", "Heb": "Hebrews", "Jas": "James", "1 Pet": "1 Peter",
      "2 Pet": "2 Peter", "1 Jn": "1 John"}
def book(ref):
    k = max((a for a in AB if ref.startswith(a + " ")), key=len); return AB[k]
STATES = {"run": "an executable derivation: typed seed elements, declared rules, emissions matched verse by verse, coverage counted, residue displayed",
          "worked": "derivation grade: seed, rules, emissions and an honesty panel stating the shared-source alternative",
          "mapped": "a letter mapped to an epistle with a grade, its class and its residue stated; granularity proportional to evidence",
          "drawn": "an arrow drawn and not run; direction open",
          "withheld": "markedness found; the arrow withheld by a date held under the chronology under examination",
          "observed": "a lexical observation awaiting a census; no derivation claimed",
          "named": "stated at the founding grain (#407, #639, #65, #1217); no seed inventory, no rules, no residue",
          "unresolved": "split between targets and left split"}
ORDER = ["run", "worked", "mapped", "withheld", "drawn", "observed", "unresolved", "named"]
ARROWS = []
def arrow(aid, seed, targets, state, records, warrants, **k):
    assert state in STATES; missing = [w for w in warrants if w not in CL]; assert not missing, (aid, missing)
    ARROWS.append({"id": aid, "seed": seed, "targets": targets, "books": sorted({book(t) for t in targets}, key=BOOKS.index), "state": state, **k, "records": records, "warrants": warrants})
LT = {x["id"]: x for x in L["letters"]}
def letter(lid, state, warrants, **k):
    x = LT[lid]; targets = refs(x["emissions"]) or k.pop("targets")
    arrow(f"letter:{lid}", x["ref"], targets, state, [1416] + k.pop("more", []), warrants, epistle=x["epistle"], position=x["heteronym"], grade=x["grade"], cls=x["class"],
          operations=ops(x["rules"]) or k.pop("operations"), stated_limit=x["honesty"], **k)
letter("ephesus", "mapped", ["rf-1416-proportional"])
letter("smyrna", "run", ["rf-1416-smyrna", "rf-1415-morphological", "rf-1415-residue", "rf-1735-crown-run"], more=[1415, 1735],
       targets=sorted({m["ref"] for e in J["emissions"] for m in e["matches"]}), operations=[f"{r['id']} {r['op']}" for r in J["rules"]],
       anchors=[f"{a['anchor']}: {a['loci']} ({a['status']})" for a in J["coverage"]["lexical_anchors"]], coverage=J["measures"]["coverage"], uniformity=J["measures"]["uniformity"],
       residue=[f"{i['ref']} ({i['topic']}): {i['class']}" for i in J["residue"]["items"]], ordering=J["measures"]["ordering"],
       surface=f"working surface past the deposited v1.0 since {J['status']['working_since']}; the deposit stays as frozen")
letter("pergamum", "mapped", ["rf-1416-classes", "rf-1416-proportional"], more=[165])
letter("thyatira", "mapped", ["rf-1416-proportional"], mediated_by="Acts 16:14 (Lydia of Thyatira)")
letter("sardis", "mapped", ["rf-1416-proportional"])
letter("philadelphia", "unresolved", ["rf-1416-proportional"])
letter("laodicea", "mapped", ["rf-1416-classes", "rf-1416-proportional"])
for x in TR["transforms"]:
    d = x.get("derivation")
    if d: arrow(f"transform:{x['id']}", "; ".join(s["ref"] for s in d["seed"]), refs(d["emissions"]), "worked", [1414, 1418], ["rf-1414-five", "rf-1418-shared-source"] + (["rf-1418-mbar"] if "M̄" in x["class"] else []),
                name=x["name"], grade=x["grade"], cls=x["class"], operations=ops(d["rules"]), stated_limit=d["honesty"])
    else: arrow(f"transform:{x['id']}", x["seed"]["ref"], [t["ref"] for t in x["targets"]], "mapped", [1414, 1415], ["rf-1414-five", "rf-1217-seed"], name=x["name"], grade=x["grade"], cls=x["class"],
                operations=[s[0] for s in x["steps"]], granular_case="letter:smyrna")
arrow("article:triad", "Rev 2:2 (ἔργον, κόπος, ὑπομονή)", ["1 Thess 1:3"], "withheld", [1735, 1802], ["rf-1735-triad-withheld", "rf-1802-pin"],
      stated_limit="1 Thessalonians is held to its received date by the chain of #1735 §II; the probative unit is the ordered cluster, not any one noun")
arrow("article:hebrews-4", "Rev 1:12–20 (the opening scene)", ["Heb 4:8–14"], "drawn", [1735, 1758], ["rf-1735-v9-hebrews", "rf-1735-v9-hebrews-open"],
      stated_limit="gathers the two Joshuas, the dividing word and the great high priest named Jesus; 'The direction is not run here.'")
arrow("q:thief", "Rev 3:3; 16:15", ["Matt 24:43", "Luke 12:39"], "observed", [1747], ["rf-1747-thief", "rf-1747-census-owed"])
arrow("q:confession", "Rev 3:5", ["Matt 10:32", "Luke 12:8"], "observed", [1747], ["rf-1747-confession", "rf-1747-census-owed"])
arrow("q:matt-24-30", "Rev 1:7", ["Matt 24:30"], "drawn", [1746, 1747], ["rf-1746-hitzig", "rf-1747-no-direction"],
      stated_limit="drawn by six critics, Hitzig (1843) to Merx (1902); the elements have extant sources in Dan 7:13, Zech 12:10–12 and Gen 12:3")
arrow("founding:rev1-attributes", "Rev 1:14–16", ["Matt 17:2", "Mark 10:21", "Matt 7:29", "Matt 28:18", "Matt 10:34"], "named", [407, 639], ["rf-407-runs"])
arrow("founding:mark", "Rev 5 (the scroll, the Lamb)", ["Mark 1:9"], "named", [407, 639], ["rf-407-runs", "rf-639-operators"], operations=["ALGO_MIN (#407)", "narrative inversion (#639)"],
      stated_limit="#639 names 'Rev 5 → Mark 1: the scroll becomes the baptism' at chapter grain; the verse is this map's locus for the baptism")
arrow("founding:matthew", "Revelation whole", ["Matt 5:1"], "named", [407, 639], ["rf-407-runs", "rf-639-operators"], operations=["ALGO_JEWISH (#407)", "Torah fractal (#639)"],
      stated_limit="no seed and no locus given beyond the Sermon as new Torah and five discourse blocks; the verse marks the Sermon")
arrow("founding:luke", "Revelation whole", ["Luke 1:1"], "named", [407, 639], ["rf-407-runs", "rf-639-operators"], operations=["ALGO_GENTILE (#407)", "historiographical veil (#639)"],
      stated_limit="no seed and no locus given; the verse marks the historiographic preface")
arrow("founding:john", "Rev 19:13; 1:13; 5:6; 12; 19:11–16; 21", ["John 1:1", "John 1:14", "John 1:29", "John 2:4", "John 19:2", "John 20:1"], "named", [407, 639, 1217],
      ["rf-407-runs", "rf-639-operators", "rf-1217-john-transform"], operations=["ALGO_REFLEXIVE (#407)", "midrashic interiorization (#639)"])
arrow("founding:fourfold", "Rev 4:6–8 (the four living creatures)", ["Matt 1:1", "Mark 1:1", "Luke 1:1", "John 1:1"], "named", [65], ["rf-65-fourfold"],
      stated_limit="the fourfold form of the gospel tradition, stated on the Josephus Thesis reading; the four incipits stand for the four books")
arrow("founding:acts", "Revelation whole", ["Acts 1:1"], "named", [407], ["rf-407-sequence"], operations=["historical framework (#407)"],
      stated_limit="Acts is also the carrier in two mapped letters: Lydia (16:14) for Thyatira, Saul→Paul (13:9) for Pergamum")
BY = {}
for b in BOOKS:
    arr = [a for a in ARROWS if b in a["books"]]
    BY[b] = {"arrows": [a["id"] for a in arr], "strongest_state": min((a["state"] for a in arr), key=ORDER.index) if arr else "none",
             "loci": sorted({t for a in arr for t in a["targets"] if book(t) == b})}
count = lambda s: sum(1 for a in ARROWS if a["state"] == s)
none = [b for b in BOOKS if not BY[b]["arrows"]]; conv = sorted(BOOKS, key=lambda b: -len(BY[b]["arrows"]))[:6]
allops = sorted({o.split(" ", 1)[-1] if re.match(r"R\d ", o) else o for a in ARROWS for o in a.get("operations", []) if a["state"] in ("run", "worked", "mapped", "unresolved")})
K["unfoldings"] = {
 "rule": ("A compressed map of every arrow the records draw from Revelation to another book of the New Testament, each at its own grain and state, and an outline of the total programme. "
          "A map is not a derivation: an arrow counts for what its state says and no more, and 'The comparison is between inferences. The burden is symmetrical.' (site /unfolding/). "
          "Grades are 'the evaluation's, offered for ruling, not settled canon' (the slate of 2026-07-28)."),
 "direction": "outward, Revelation to the later books (rung IV). The foldings in, Sappho 31 and Philo into the Apocalypse's channel (#1493–#1495, #1511, #1758), are the kernel's joins and are not repeated here.",
 "states": STATES, "classes": L["transform_classes"], "falsification": TR["falsification"], "procedure": "transform_procedure (this kernel): steps, evidence kinds, failure rule, the frozen-operator precedent",
 "arrows": ARROWS, "by_book": BY,
 "counts": {"arrows": len(ARROWS), **{s: count(s) for s in ORDER if count(s)}, "books_with_an_arrow": len(BOOKS) - len(none), "books_without": none,
            "books_reached_above_the_founding_grain": [b for b in BOOKS if BY[b]["strongest_state"] in ("run", "worked", "mapped", "withheld", "drawn", "observed", "unresolved")],
            "most_arrows": {b: len(BY[b]["arrows"]) for b in conv}, "operations_declared": allops},
 "not_claimed": ["The shared order of Matthew and Luke: 'not met; not claimed' (#1747).",
                 "A derivation of the double tradition as a whole: two sayings are 'an observation awaiting a census' (#1747).",
                 "The order of James against the order of the Smyrna letter: 'open… Not yet measured' (the James working surface).",
                 "Any Gospel derived: the four Gospels and Acts stand at the founding grain, named and not run, apart from three Matthean and two Lukan loci observed or drawn in #1746–#1747.",
                 "Seed inventory beyond Rev 1–3, 5, 13 and 21: the seals, trumpets and bowls, the two witnesses, chapters 12 and 17–20 and the close of the book have no typed seed elements."],
 "outline_of_the_total_programme": {
   "status": "an outline proposed at v1.5 from the map above, for the author's ruling; it is no record's claim and nothing in it is asserted of the texts",
   "author_programme": {"at": "2026-11-26 12:35", "text": PROGRAMME, "status": "the author's statement of the map to be built; hypotheses, not findings. Carried here as the head of the outline; the mapping is opened as a working file and is not part of this kernel",
      "hypotheses": ["a fourfold: the four riders, the four creatures, the four names and the four Gospels",
                     "Matthew first, pressed from the mourning tribes (Matt 24:30 and Rev 1:7): a transform algorithm defined on Matthew, then used to work out the other three",
                     "the epistles from James, the one run case",
                     "a seven within seven: the Pauline seven-church formation transformed from Revelation's seven churches, and Paul as one of seven named epistolary positions mapped to Revelation's seven"]},
   "object": "Revelation unfolded to each of the twenty-six other books as an executable derivation, with the residue of every book displayed: 'The transform graph is the object to be broken, not merely admired.'",
   "stages": [
     {"n": 1, "name": "seed inventory", "what": "Revelation whole, segmented into typed seed elements in Greek, in one file",
      "have": "Smyrna, eleven elements (working surface); the other six letters, two to six each; M2–M5, three or four each", "owed": "Rev 4, 6–12, 14–20, 22"},
     {"n": 2, "name": "operator vocabulary, frozen", "what": "the declared operations gathered into one vocabulary with families (expand, anchor, frame) and classes (M, M̄, X), fixed before each new test as #1494 fixed T",
      "have": f"{len(allops)} operation names across the run, worked and mapped arrows; families declared for James only", "owed": "families for the rest; a rule that an operation coined after scoring does not count"},
     {"n": 3, "name": "target census, book by book", "what": "every pericope of the target book classed derived, partly derived, residue or other-tradition, as James is",
      "have": "James: " + J["measures"]["coverage"], "owed": "twenty-five books; first the mapped epistles (Colossians, 1 Corinthians 8–10, 1 John, 1 Thessalonians, Philippians)"},
     {"n": 4, "name": "antecedent map", "what": "for each arrow, the tradition available to both texts, stated before the direction is argued (#1735 §VI.3, step two)",
      "have": "Lev 26:12, Isa 53, Isa 65:17 and 66:22, Dan 7 (M2–M5); Dan 7:13, Zech 12:10–12, Gen 12:3 (Matt 24:30)", "owed": "the seven letters, per element"},
     {"n": 5, "name": "direction", "what": "the anchor rules, which alone carry direction: a word or form carried across and changed in grammar or standing, with the evidence that would reverse the arrow stated first",
      "have": "δώσω → ἐπηγγείλατο (Rev 2:10 → Jas 1:12); ἐπάγγελμα (2 Pet 3:13); Col 4:16, the exchange recorded in the canon", "owed": "one anchor rule per mapped arrow, or the arrow stays a map"},
     {"n": 6, "name": "order", "what": "whether the borrower keeps, gathers or scatters the order of the seed", "have": "the Jas 2:2–7 knot: 'The order is not kept; the gathering is.'", "owed": "a measure; the shared order of Matthew and Luke, not claimed"},
     {"n": 7, "name": "the Gospels", "what": "the census of the double tradition against Rev 1–3, 16:15 and 22:7–20, then Matthew, where six critics already drew the arrow at 24:30",
      "have": "the thief, the confession, Matt 24:30; four parameter sets named at the founding grain", "owed": "everything else; the Gospels are the least mapped part of the programme and the largest"},
     {"n": 8, "name": "the residue ledger", "what": "one ledger of what does not derive, across the New Testament: the falsification surface of rung IV", "have": "James, six pericopes; per-letter residue in prose", "owed": "the ledger"},
     {"n": 9, "name": "scoring by other hands", "what": "clauses and scoring rule handed to independent substrates with the target unnamed (lines_of_research)", "have": "the precedent, #1495: one adjudicator, one pass, replication invited", "owed": "a run"}],
   "order_of_work": ["version the James working surface, which has moved past the frozen v1.0", "Colossians and 1 Corinthians 8–10 to executable grade: the highest-graded mapped arrows, one of class X and one of class M̄",
                     "Hebrews, where " + str(len(BY["Hebrews"]["arrows"])) + " arrows already land from separate seeds", "the double-tradition census, then Matthew", "the books with no arrow: " + ", ".join(none)],
   "what_would_count_against": TR["falsification"]},
 "sources": {f"unfolding/{f}": hashlib.sha256((SITE / "unfolding" / f).read_bytes()).hexdigest() for f in ("transforms.json", "letters/letters.json", "james/derivation.json")},
 "site_commit": SITE_HEAD}
tp_before = dict(K["transform_procedure"]["sources"])
K["transform_procedure"]["sources"] = {"transforms.json": K["unfoldings"]["sources"]["unfolding/transforms.json"], "james/derivation.json": K["unfoldings"]["sources"]["unfolding/james/derivation.json"]}
K["transform_procedure"]["map"] = "unfoldings (this kernel, v1.5): the arrows by state, the table by book, the outline"

# ---------------------------------------------------------------- kernel: summary, fold-in record, tests
U = K["unfoldings"]["counts"]
K["compression_survival_summary"] = K["compression_survival_summary"].rstrip() + (
    f" The unfoldings are mapped arrow by arrow ({U['arrows']} arrows): one run to completion (Smyrna to James), four worked to derivation grade (M2–M5), the other letters mapped with grades and residue, "
    f"one arrow withheld by a date (Rev 2:2 and 1 Thess 1:3), two drawn and not run, two sayings of the double tradition observed, and the Gospels and Acts named at the founding grain only; "
    f"{len(none)} books have no arrow ({', '.join(none)}). The reception is audited as political economy (#1802) and as a genre imposed on the books (#1798).")
F = K["fold_in_v15"]
F["rulings"] += [{"at": "2026-11-26 12:21", "text": "scan for anything thats built since the hologram... and anything we missed on the first pass that would strengthen it"},
                 {"at": "2026-11-26 12:25", "text": "and if it doesnt have it yet, it needs a compressed hologram of the unfoldings - so far weve a broad programme as well as specific mappings of revelation to james, matthew, the seven church structure, and so on... eventually we need to construct and propose the total program, a full unfolding from revelation to the rest of the nt as executable..so this is, a mapping of whats there + an outline"},
                 RULING_D, {"at": "2026-11-26 12:35", "text": PROGRAMME}]
F["correction_rung_VI"] = {"before": dep_before, "after": {"depends_on": [], "strengthened_by": ["rung:V"], "consequence_of_defeat": ["rung:V"]}, "ruling": RULING_D,
                           "found_by": "verify_fw.py T1 at v1.5: the two ladder pages no longer matched the hashes taken on 2026-11-08", "pages_rebound": rebound_pages, "claim_added": "claim:rf-site-vi-independent"}
F["scan"] = {"since_the_first_kernel": [1798, 1802], "missed_on_the_first_pass": [65, 1738],
             "records": [{"record": f"rec:{n}", "deposit": n, "version": REG[n].get("version"), "axn": REG[n]["axn"], "sha256": REG[n]["hash"], "body": NEW[n][0], "body_secondary": NEW[n][1], "stratum": NEW[n][3]} for n in NEW],
             "read_and_left_out": {"1795": "Why I Believe in Hell: does not bear on the framework", "1458": "The Echo and the Stamp: names Revelation First as a keyword only",
                                   "1496, 1512, 1513, 1533": "the Ω programme's loss model, reception edges and Qurʾanic protocol: the Sappho line's instruments, joined through #1493–#1495 and #1511",
                                   "1498, 1514, 1522": "the build programme and the seated corpora: infrastructure; the papyri panel is held at #1510"},
             "method": "registry scan by keyword and by reference to #202, #1217, #1735 and the site, then each candidate read at its passages on Revelation"}
F["not_folded"] = "left as related work: #1795 (Why I Believe in Hell)"
F["unfoldings"] = {"arrows": U["arrows"], "claims_added_as_warrants": [f"claim:{c}" for c in NEWC if c.startswith(("rf-407", "rf-639", "rf-1217", "rf-1414", "rf-1415", "rf-1416", "rf-1418", "rf-1735", "rf-1746", "rf-1747"))],
                   "transform_procedure_sources_before": tp_before, "outline": "proposed, for ruling"}
F["claims_added"] += [f"claim:{c}" for c in NEWC]
F["method"] += "; second stage by operator/v15_patch_b.py"
AL = K["argument_layer"]
moved = {json.loads(l)["record"] for l in (KD / "04-arguments.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
earlier = sorted(x["deposit"] for x in G["@graph"] if x.get("@type") == "Record" and x["@id"] not in moved and x["deposit"] not in set(AL["records_without_moves"]) | set(NEW))
AL["records_without_moves"] = sorted(set(AL["records_without_moves"]) | set(NEW) | set(earlier))
AL["without_moves_before_v15"] = {"records": earlier, "note": "in the kernel without moves before v1.5; v1.4 declared records_without_moves as empty. Declared here; their moves are owed with the rest."}
AL["owed_v15"] = AL["owed_v15"].replace("the six records of stratum " + SID, "the ten records that entered at v1.5 (six of stratum " + SID + " at the first stage; #1798, #1802, #65 and #1738 from the scan)")
F["moves"] = "none written at v1.5; owed for " + ", ".join(f"#{n}" for n in AL["records_without_moves"])
T9["structural"] += ["T23 (v1.5) every arrow of unfoldings carries a state in the declared vocabulary and warrants that resolve to claims",
                     "T24 (v1.5) unfoldings.by_book covers the twenty-six books and equals the table computed from the arrows"]

dump_yaml("00-kernel.yaml", K); dump_yaml("01-ontology.yaml", O)
(KD / "02-graph.jsonld").write_text(json.dumps(G, ensure_ascii=False, indent=1), encoding="utf-8")
write_lines("03-claims.jsonl", C); write_lines("05-temporal.jsonl", E); dump_yaml("09-tests.yaml", T9)
files = sorted(q.name for q in KD.iterdir() if q.is_file() and q.name not in ("11-integrity.yaml", "10-verification.json"))
I.update({"built": BUILT, "files": {f: hashlib.sha256((KD / f).read_bytes()).hexdigest() for f in files}}); dump_yaml("11-integrity.yaml", I)
print(f"v1.5 stage 2: {sum(1 for x in G['@graph'] if x.get('@type')=='Record')} records, {len(C)} claims ({len(NEWC)} new here), {len(G['edges'])} edges; arrows {U}")
print("by book:", {b: (v["strongest_state"], len(v["arrows"])) for b, v in BY.items()})
print("unresolved introductions:", [c for c in NEWC if CL[c]["introduced"]["date"] is None])
