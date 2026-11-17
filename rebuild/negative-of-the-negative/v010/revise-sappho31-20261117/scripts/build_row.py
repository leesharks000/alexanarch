"""Build the revised Sappho 31 row (2026-11-17) and its two ledgers in the stage, from the live row and ledgers, the new
claims (claims_new.py) and the KO revision (ko_new.py). Writes STAGE/row.json, field.json, ledger-archive.json,
traversal/reading-20261117.json. verify.py then checks every quote and the coverage.   /tmp/py312/python3 build_row.py"""
import json, copy, hashlib, difflib, re, collections
from vlib import *
import claims_new as C
import ko_new as K

TODAY = "2026-11-17"
REVISER = "Claude (Opus 5.5), subagent, 2026-11-17"
raw_row = LIVE_ROW.read_bytes()
PRIOR_SHA = hashlib.sha256(raw_row).hexdigest()
R0 = json.loads(raw_row)
R = copy.deepcopy(R0)
F = json.loads((LIVE_LEDGERS / "field.json").read_text(encoding="utf-8"))
A_old = json.loads((LIVE_LEDGERS / "ledger-archive.json").read_text(encoding="utf-8"))
REGD = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
FETCH = json.loads((STAGE / "sources/fetch-records.json").read_text(encoding="utf-8"))
SRC = {"B1": "B1-wikipedia-sappho-31", "B2": "B2-literary-matters", "B3": "B3-slowdown", "B4": "B4-norton", "B5": "B5-edubirdie"}
STAGE_REL = str(STAGE.relative_to(ROOT))
PASTE = R0["objects"]["T"]["path"]

# ---------------------------------------------------------------- the archive ledger
A = []
for c in A_old:
    c = dict(c)
    if c["id"] == "A436-01":
        c["quote_ok"] = False
        c["revised"] = TODAY
        c["quote_note"] = ("not found in #436's text as it now stands (data/texts/AXN-00FB-text.md, re-seated 2026-10-19 after the row's extraction of "
                           "2026-10-07); the sentence is found verbatim in #1048 (data/texts/AXN-0424-text.md) and is carried as A1048-03; the KO cites A1048-03 "
                           "(reported in REPORT.md; the claim is kept, §5.7)")
    A.append(c)
A += [dict(c) for c in C.ALL]
AIDS = {c["id"] for c in A}

# ---------------------------------------------------------------- the field ledger (v0.10 shape: pools, origin, saved text)
FC = F["field_claims"]
for k, c in FC.items():
    c["pool"] = "B_D"
    if c["source"] == "B6":
        c["title_only"] = True
        c["checked_against"] = f"the paste ({PASTE}), the card's title"
    else:
        c["checked_against"] = f"the saved text {STAGE_REL}/sources/{SRC[c['source']]}.txt (fetched {TODAY})"
for s in F["field"]:
    sid = s["id"]
    s["origin"] = "card"; s["pool"] = "B_D"
    s["fetched_20261007"] = s.pop("fetched")
    if sid in SRC:
        rec = FETCH[SRC[sid]]
        s["fetched"] = {"url": rec["url"], "at": rec["at"], "http": rec["http"], "agent": rec["agent"], "bytes": rec["bytes"],
                        "raw_sha256": rec["raw_sha256"], "note": "refetched for this revision so that every quote is verified by script against saved text (§3.1); text only, the raw response not kept (disk)"}
        s["files"] = {f: {"path": f"{STAGE_REL}/sources/{f}", "sha256": h} for f, h in rec["files"].items()}
    else:
        s["fetched"] = {"note": "not fetched: YouTube, title only (rule); the title verified against the paste"}
        s["files"] = {}
F_out = {"row": "sappho-31", "address": R0["address"], "addresses": R0["addresses"], "extracted": "2026-10-07",
         "extractor": "one extractor (unaudited, §3.8), 2026-10-07",
         "rule": "v0.10 §3.5, source-neutral: opening or abstract, defined terms, headline claims, stated limits; quotes verbatim (the 2026-10-07 extraction by HTTP-fetch excerpt), verified by script on 2026-11-17 against the pages refetched and saved as text (whitespace and quotation marks normalised for the check; multi-part quotes joined by ' … ', each part checked); the title-only card quoted by its title as pasted",
         "B_note": "The field in two pools (v0.10 §0.3, §3.1(a)), marked by origin and pool. B_D, the disclosed pool: T's six cards (B1 Wikipedia, B2 Literary Matters, B3 The Slowdown, B4 W. W. Norton, B5 EduBirdie, B6 YouTube, title only). B_R, the reference pool: not extended in this revision (the brief names no reference source; the poem has no own pages; its Wikipedia article is a card of T and is carried once, in B_D).",
         "pools": {"B_D": [s["id"] for s in F["field"]], "B_R": []},
         "pages": f"saved text under {STAGE_REL}/sources/ (Bn-*.txt, scripts and styles stripped; fetch-records.json holds url, time, HTTP code, agent, byte count and the raw response's sha256)",
         "field": F["field"], "field_claims": FC, "revised": TODAY, "revision_extractor": REVISER + " (no field claim added, changed or removed; the pools marked and the quotes verified)"}

# ---------------------------------------------------------------- the knowledge object
old = R0["objects"]["KO"]["sentences"]
new_s = []; changes = []
by_after = collections.defaultdict(list)
for after, sense, text, claims in K.NEW:
    by_after[after].append((sense, text, claims))
cur_sense = None
for s in old:
    n = s["n"]; text = s["text"]; claims = list(s["claims"])
    sense = K.SENSE_OF_OLD[n]
    if n == 1:
        t2 = text.replace("argues that its distal", "argued in January 2026 that its distal").replace(
            "with the inscribed text.", "with the inscribed text, a reading whose current text is #1781 (v2.8, 16 November 2026), under Lee Sharks's own name.")
        assert t2 != text
        claims += ["A1781-01"]; text = t2
        changes.append({"old_n": 1, "change": "edited", "reason": K.EDITS[1][3], "claims_added": ["A1781-01"]})
    elif n == 9:
        t2 = text.replace("transform-site' (#436).", "transform-site' (#1048).")
        assert t2 != text
        claims = [c if c != "A436-01" else "A1048-03" for c in claims]; text = t2
        changes.append({"old_n": 9, "change": "edited", "reason": K.EDITS[9][3], "claims_added": ["A1048-03"], "claims_removed": ["A436-01"]})
    else:
        changes.append({"old_n": n, "change": "kept"})
    new_s.append({"old_n": n, "sense": sense, "text": text, "claims": claims})
    for sense2, t, cl in by_after.get(n, []):
        new_s.append({"old_n": None, "sense": sense2 or sense, "text": t, "claims": cl})
# senses carried forward (a new sense heading continues until the next old sentence's own sense)
last = None
for s in new_s:
    if s["old_n"] is None and s["sense"] is None:
        s["sense"] = last
    last = s["sense"]
# number, paragraph by sense
KO_S = []; para = -1; prev = None; senses = collections.OrderedDict()
for i, s in enumerate(new_s, 1):
    if s["sense"] != prev:
        para += 1; prev = s["sense"]
    senses.setdefault(s["sense"], []).append(i)
    d = {"n": i, "para": para, "sense": s["sense"], "text": s["text"], "claims": s["claims"]}
    if s["old_n"] is not None:
        d["v09_n"] = s["old_n"]
    else:
        d["added"] = TODAY
    KO_S.append(d)
for ch in changes:
    ch["new_n"] = next(x["n"] for x in KO_S if x.get("v09_n") == ch["old_n"])
added = [{"new_n": x["n"], "sense": x["sense"], "claims": x["claims"]} for x in KO_S if x.get("added")]
missing = sorted({c for x in KO_S for c in x["claims"]} - AIDS - set(FC))
assert not missing, missing

KO = R["objects"]["KO"]
KO["genre"] = "knowledge object, equal case, under EA-NEGONT-02 v0.10 (#1726): the archive's sources and the field's admitted on equal terms, ontology included, in one claim space; the final article form, first on the entity's page (§4.13); natural sentences under descriptive subheadings (§4.12)"
KO["status"] = ("composed 2026-10-18 under v0.9 on the operator's ruling ('lets craft those /non entries'); revised in place 2026-11-17 under v0.10 "
                "(BRIEF-REVISE-ROW-SAPPHO-31.md): the v0.9 sentences kept as composed with their inline attribution (§4.5: rows composed under v0.9 stand as composed), two edited; "
                f"{len(added)} sentences added, attribution in their prose only where who holds the claim is part of what is said; not frozen; ledger unaudited")
KO["sentences"] = KO_S
KO["field_claims"] = {k: {"source": v["source"], "locus": v["locus"], "quote": v["quote"], "modality": v["modality"]} for k, v in FC.items()}
KO["governing_question"] = ("the revision's organisation (operator, 2026-11-17: 'i am not contending with their journal. i am contending with what sappho *is*, and who has the right to decide it'; recorded in notes, not quoted in the article): "
                            "what the poem is, stated as mechanics: the field's account and the archive's composed as one claim space; the reading's current text (#1781) beside the field's reading, both graded on one scale (¶ 'The two readings on one scale'); "
                            "the history of the jealousy reading as documented (¶ 'Readings, and the making of the jealousy reading'); the decline of 16 November 2026 as a dated fact with its record, and the census's account of where the decision on the poem's object is made, as the archive's reading (¶ 'The decline, and where the decision is made')")
JOINS_OLD = []
KO["joins"] = [
    {"act": "order of senses", "sentences": f"1–{len(KO_S)}", "claims": [],
     "note": "equal case (§4.7): what it is; the witness; the edge; the scene and the catalogue; readings, with the making of the jealousy reading in date order (1724, 1816, 1850, 1900, 1955); the future-reader reading, ending in its current text (#1781); the two readings on one scale; the decline and where the decision is made; reception; the poem in the archive; its composition by machines, in date order (18 January to 16 November 2026). The v0.9 order of the 38 kept sentences is unchanged; each added sentence stands after the v0.9 sentence whose sense it extends."},
    {"act": "holding rivals (compatible or exclusive, contested within, dated)", "sentences": [n for n in [x["n"] for x in KO_S if set(x["claims"]) & {"A1270-05", "A1054-01", "A1779-01", "A1781-26"}]],
     "claims": ["A1270-05", "A1270-06", "A1054-01", "A1054-03", "A1779-01", "A1781-26"],
     "note": "#1270 (v1.0, 9 January 2026): 'not wrong but incomplete'; #1054 (8 July 2026): exclusive at κῆνος; #1779 and #1781 (16 November 2026): incompatible at five places, an actual man granted the seat, the comparison not depending on it. Carried as contested within the pool, each at its date; #1270's citations stand as dated, #1781 as current."},
    {"act": "holding rivals (the reconstruction's wording, three states)", "sentences": [x["n"] for x in KO_S if set(x["claims"]) & {"A1270-08", "A1309-01", "A1781-17"}],
     "claims": ["A1270-07", "A1270-08", "A1309-01", "A1781-17"], "note": "#1270's γράμμασι μολπὰν; #1309's Kypris who saves and the song in letters; #1781's sparrows and ἀοίδα γράμμασι ζώοι: three wordings, each the archive's at its date, all hypothesis"},
    {"act": "holding rivals (where the poem ends)", "sentences": [x["n"] for x in KO_S if set(x["claims"]) & {"F34", "F40", "A1476-01", "A1781-12", "A1781-13", "A1781-18"}],
     "claims": ["F6", "F34", "F40", "A1474-04", "A1476-01", "A1781-12", "A1781-13", "A1781-18"], "note": "the field's fragment missing its ending beside the edge as object (#1476), Bergk's assignment and the seam (#1781 §V.1), the author's conjecture of Longinus's completion with its falsifiers (§V.1a), and the function argued with design open (§V.5)"},
    {"act": "holding rivals (Catullus's fourth stanza)", "sentences": [x["n"] for x in KO_S if set(x["claims"]) & {"A1049-02", "A1601-01", "A1781-16"}],
     "claims": ["F42", "A1048-01", "A1049-02", "A861-01", "A1601-01", "A1781-16"], "note": "operator inversion (#1049), replacement of the fifth's position (#861), no Greek counterpart (#1601), functional reversal within a preserved structure (#1781 §V.3)"},
    {"act": "the comparison on one scale (the field's reading beside the archive's, graded alike)", "sentences": senses.get("The two readings on one scale", []),
     "claims": ["F16", "F17", "F37", "F39", "F45", "A1781-24", "A1781-25", "A1756-01", "A1783-06", "A1783-07", "A1781-21", "A1781-22", "A1781-28", "A1781-27"],
     "note": "the jealousy reading stated at its strength, its strongest form (the maker credited with the disintegration, #1783 I.4a) and its queerness at its strength included, before the archive's grades of it; the grades and the charge are the archive's, named as such (#1781, #1756, #1783); the field's statements of the reading (F16, F37, F39, F45) and of its denial (F17–F19) stand as composed in the readings above"},
    {"act": "a dated fact with its record", "sentences": [x["n"] for x in KO_S if set(x["claims"]) & {"A1781-29", "A1774-01", "A1774-02", "A1774-03"}],
     "claims": ["A1781-29", "A1774-01", "A1774-02", "A1774-03"], "note": "the decline of 16 November 2026: the submission, the decision letter's grounds and the report's own words, from the deposited record (#1774 and its attachment); no reader of the report named; the editor's name stands in the ledger quote of the record (A1774-01) and is not composed in the article, whose object is the poem"},
    {"act": "the archive's reading of where the decision is made", "sentences": [x["n"] for x in KO_S if set(x["claims"]) & {"A1783-01", "A1783-03", "A1783-09"}],
     "claims": ["A1783-01", "A1783-02", "A1783-13", "A1783-03", "A1783-04", "A1783-05", "A1783-09", "A1783-10", "A1783-11", "A1783-12"],
     "note": "#1783 I.4–I.4b composed as #1783's reading, with its own limit (one article, one report, one decline) beside it; mechanics only"},
    {"act": "naming the holder (machine compositions)", "sentences": senses.get("Its composition by machines", []),
     "claims": sorted([c["id"] for c in C.ALL if c["dep"] == "capture-registry"]) + ["A1749-01", "A1054-02", "A1611-01", "A1496-01", "A1781-30"],
     "note": "each composition named by surface and date as the Capture Registry records it; the registry's findings are the source; the operator's personalized exchange carried only as #1781 withdraws it"},
    {"act": "the Diotima identification", "sentences": [x["n"] for x in KO_S if "A1781-23" in x["claims"]], "claims": ["A1781-23", "A1783-08", "A752-01", "A752-02"],
     "note": "composed as literary and mythological, as the author states it (#1783 I.4a), never biographical"},
]
order = [c for x in KO_S for c in x["claims"]]
marks = {
    "A436-01": "quote not in #436's text as re-seated 2026-10-19; found in #1048 (A1048-03), which the KO now cites; A436-01 kept (§5.7)",
    "A1048-01": "superseded_in_source: #1048's 'compression' characterization of Catullus's fourth stanza, corrected by #1049 §2 (carried from the v0.9 composition notes)",
    "A1270-05": "dated: #1270 is v1.0 (2026-01-09); the reading's current text, #1781 (2026-11-16), holds that the readings do not combine (A1781-26), as #1779 restates #1054",
    "A1781-13": "hypothesis (the author's conjecture), with its two falsifiers",
    "A1781-17": "hypothesis: the restoration not documentary; separable from the argument",
    "A1774-02": "attributed: the report's words, from the deposited attachment",
}
KO["plan"] = {"order": order, "senses": dict(senses), "marks": marks, "conflicts": [], "cuts": []}

# ---------------------------------------------------------------- the compression (P)
P = R["objects"]["P"]
P["status"] = "composed 2026-10-18 from the v0.9 knowledge object; revised 2026-11-17 (the lede carries the current text, one item revised, five open items added or extended, the rail's new lineages); not frozen"
P["lede"]["text"] = P["lede"]["text"].replace("(Lee Sharks, #1270)", "(Lee Sharks, #1270; #1781)")
assert "#1781" in P["lede"]["text"]
P["lede"]["claims"] = P["lede"]["claims"] + ["A1781-01"]
sec = {s["head"]: s for s in P["sections"]}
for it in sec["The future reader"]["items"]:
    if it["label"] == "With jealousy:":
        it["text"] = "incomplete (#1270) or exclusive (#1054, #1781)."
        it["claims"] = it["claims"] + ["A1781-26", "A1779-01"]
P["open"].insert(1, {"question": "Is the jealousy reading graded on the same scale as the future-reader reading?", "rests_on": ["F16", "F17", "A1781-24", "A1781-25", "A1756-01", "A1783-06", "A1781-21"],
                     "modality": "interpretation (the archive's grades; the field states the reading and its denial)",
                     "would_resolve": "an evaluation that grades both columns by the same criteria and states its preference, how firmly, and what it changes (#1781 §VII.4)"})
P["open"].insert(2, {"question": "Who first warranted the jealousy reading, and by what act?", "rests_on": ["F16", "A1781-19", "A1781-20", "A1752-01", "A1752-02", "A1752-08"],
                     "modality": "documented (the dated acts: 1724, 1816, 1850, 1955) and open (the priority, #1752)",
                     "would_resolve": "the priority and the transmission #1752 leaves open (its Appendix A.2), read at the earlier claimants' pages"})
for q in P["open"]:
    if q["question"].startswith("Is the future-reader reading compatible"):
        q["rests_on"] = q["rests_on"] + ["A1779-01", "A1781-26"]
        q["modality"] = "interpretation (contested in the archive, dated, and in the field)"
        q["would_resolve"] = ("a ruling, in the archive, between #1270's 'not wrong but incomplete' (v1.0, 2026-01-09) and the incompatibility #1054 placed at κῆνos and "
                              "#1779 and #1781 restate at five places (2026-11-16); #1781's comparison does not depend on it").replace("κῆνos", "κῆνος")
    if q["question"].startswith("Where does the poem end"):
        q["rests_on"] = q["rests_on"] + ["A1781-12", "A1781-18"]
    if q["question"].startswith("Does χλωρός name"):
        q["rests_on"] = q["rests_on"] + ["A1781-08", "A1781-09", "A1781-10", "A1781-11"]
        q["would_resolve"] = q["would_resolve"] + "; by #1781, the convergence of the word's uses, the translators' supplements and the plant's path to the sheet (argued, not read off the lexicon)"
    if q["question"].startswith("What wording completes"):
        q["rests_on"] = q["rests_on"] + ["A1781-17"]
        q["modality"] = "hypothesis (three wordings: #1270, #1309, #1781)"
P["open"].insert(4, {"question": "Is ἐπεὶ καὶ πένητα Longinus's completion of the poem's edge?", "rests_on": ["A1781-12", "A1781-13", "A1781-14"],
                     "modality": "documented (Bergk's assignment, the dialect count, the seated sentence) and hypothesis (the conjecture)",
                     "would_resolve": "by #1781 §V.1a, a witness independent of Longinus carrying verse past τόλματον, or a reading of the transmitted words as Sapphic verse without emendation"})
P["open"].append({"question": "Where is the decision on what the poem is made, and on what right?", "rests_on": ["A1783-03", "A1783-04", "A1783-05", "A1783-13", "A1781-29", "A1774-01"],
                  "modality": "interpretation (the archive's reading, #1783), on one case (one article, one report, one decline)",
                  "would_resolve": "the comparison of the two readings made in the open on one scale (#1781 §VII.4; #1783 I.4a), and the census #1783 carries to further journals"})
# rail: new claims joined to existing lineages where the lineage is the same; new lineages after their nearest kin
rail = P["rail"]
names = {x["lineage"].lower(): x for x in rail}
newlin = collections.OrderedDict()
for c in C.ALL:
    if c["id"] in ("A1048-03",):
        names["stanza numbering"]["claims"].append(c["id"]); continue
    key = c["lineage"].lower()
    if key in names:
        names[key]["claims"].append(c["id"])
    else:
        newlin.setdefault(c["lineage"], []).append(c["id"])
for lname, cl in newlin.items():
    first = min(cl, key=lambda i: next(x["date"] for x in A if x["id"] == i))
    dep_ = next(x["dep"] for x in A if x["id"] == first)
    card = {"lineage": lname, "claims": cl, "earliest": dep_ if dep_ != "capture-registry" else "capture-registry", "added": TODAY}
    anchor = {"the reading's current text": "κῆνος as the future reader", "the second person as the voice": "κῆνος as the future reader",
              "the catalogue's order": "The symptoms", "the medium question": "χλωρός as papyrus substrate",
              "Longinus's sentence as the first filling": "Where the poem ends (contested within)",
              "the jealousy reading's making": "Jealousy: proposed and denied", "the comparison on one scale": "Jealousy and the future reader: compatible or exclusive (contested within)",
              "the decline at Classical Philology": "the comparison on one scale", "where the decision on the poem's object is made": "the decline at Classical Philology"}.get(lname)
    idx = next((i for i, x in enumerate(rail) if x["lineage"].lower() == (anchor or "").lower()), len(rail) - 1)
    rail.insert(idx + 1, card)
P["entity"] = P["entity"] + " Revised 2026-11-17 under v0.10: the reading's current text (#1781), the comparison on one scale, the jealousy reading's making, the decline and #1783's reading added; every field claim carried."


def words(t): return len(re.findall(r"[A-Za-z0-9'’-]+", t))


P["body_words"] = words(P["lede"]["text"]) + sum(words(i["label"]) + words(i["text"]) for s in P["sections"] for i in s["items"])
P["body_words_rule"] = "lede plus every item's label and text, regex [A-Za-z0-9'’-]+ (the v0.9 count's rule; 2026-11-17); the bound is 350, §4.8, provisional"
PB = R["objects"]["P_B"]
PB["body_words"] = words(PB["lede"]["text"]) + sum(words(i.get("label", "")) + words(i["text"]) for s in PB["sections"] for i in s["items"])

# ---------------------------------------------------------------- T (v0.10 fields)
T = R["objects"]["T"]
T["words_note"] = "one turn at one address; 261 words in the answer as pasted; six cards (Wikipedia, Literary Matters, The Slowdown, W. W. Norton, EduBirdie, YouTube); the closer an offer menu (T8)"
T["transcripts"] = [{"slug": T["register"]["slug"], "address": R0["address"], "obs_id": T["register"]["obs_id"], "register": T["register"]["register"],
                     "path": T["path"], "sha256": T["sha256"], "sha256_of": "the paste file, UTF-8", "words": T["words"], "cards": T["cards"],
                     "note": "T is seated in the /non register, not in the Capture Registry; no Capture Registry entry is the row's T"}]

# ---------------------------------------------------------------- ontology: case and ρ re-read at the new loci
O = R["ontology"]
O["composition_note"] = ("the equal-terms case (§0.9, §4.1): the archive's sources and the field's admitted on equal terms, ontology included, in one claim space; every field claim composed as received; "
                         "the reading's current text (#1781), its comparison of the readings, the reception history (#1752), the hologram (#1756), the decline's record (#1774) and the census (#1783) composed as claims about the poem on the same terms; no translation")
O["case"]["revision_20261117"] = {
    "value": "equal (kept)",
    "statement": ("Re-read at the new loci, the case stands. #1781 keeps the field's object whole: a poem by Sappho, transmitted by Longinus, with a man, a woman and a speaker, "
                  "'Maker and speaker stay distinct here', an actual man granted the seat (§I.2, §VII.5); its contest is with a reading the field itself contests (F17–F19), which it grades on one scale, "
                  "and its harder verdict ('a bad reading', §VIII) is a contradiction of force composed under P_coh, not a denial of the field's presupposition. #1783 locates where the decision on the object is made and leaves the object the field's. "
                  "The future-reader ontology stays held in the field, however marginally (Svenbro, #1548), so the law of the suppressed witness does not apply."),
    "loci": [{"dep": 1781, "locus": "§IV.5", "quote": "Maker and speaker stay distinct here."},
             {"dep": 1781, "locus": "§I.2", "quote": "An expression of this kind can mark a person by class, character or capacity without excluding a situated referent: an actual man may sit there."},
             {"dep": 1781, "locus": "§VII.5", "quote": "The comparison does not depend on exclusivity."},
             {"dep": 1783, "locus": "I.4a", "quote": "The reader chooses which to keep."}]}
O["rho"]["revision_20261117"] = {
    "value": "extends (kept)",
    "statement": ("ρ = extends stands: #1781 adds senses, mechanisms and limits on the field's poem (κῆνος … ὄττις and the cup; the second person as the voice; the catalogue's order; χλωροτέρα ποίας and the translators' count; "
                  "Bergk's assignment, the seam and the conjecture of Longinus's completion; Catullus's stanza as functional reversal; the two readings graded on one scale), and #1752, #1756 and #1783 add the reading's history, "
                  "its two faces and the place of the decision. The new contradictions are composed under P_coh with their sources: #1781's grading of the jealousy reading (A1781-24, A1781-25, A1781-28) beside F16, F37, F39 and F45; "
                  "the incompatibility restated at five places (A1781-26, A1779-01) beside #1270's compatibility (A1270-05); the third wording of the stanza (A1781-17) beside #1270 and #1309."),
    "claims": ["A1781-02", "A1781-05", "A1781-07", "A1781-08", "A1781-12", "A1781-13", "A1781-16", "A1781-24", "A1781-26", "A1752-04", "A1756-02", "A1783-03"]}
O["E_A"]["definition_revision_20261117"] = ("Sappho 31 as E_A above, with the reading's current text #1781 (v2.8, 16 November 2026, under Lee Sharks's own name): κῆνος … ὄττις the seat of whoever sits opposite the voice; the second person the voice given only sound; "
                                            "the catalogue ordered as the performing body's withdrawal; χλωροτέρα ποίας the body passing to the dried sheet; the transmitted edge an agentless opening, its six last words Longinus's on Bergk's assignment and, by conjecture, his completion; "
                                            "the jealousy reading graded on the same scale as the more conjectural, its making dated 1724, 1816 and 1955 (#1752), and the readings held incompatible at five places (#1779, #1781)")
O["E_A"]["defining_papers"] = O["E_A"]["defining_papers"] + [1781]
O["E_A"]["claims"] = O["E_A"]["claims"] + ["A1781-01", "A1781-02", "A1781-24", "A1781-26"]
addmap = {"F16": ["A1781-19", "A1752-01", "A1781-24"], "F18": ["A1670-01"], "F20": ["A1781-15"], "F6": ["A1781-12", "A1781-18"],
          "F25": ["A1781-16"], "F22": ["A1781-07", "A1781-08"], "F26": ["A1781-23"], "F27": ["A1781-14"], "F12": ["A1752-03"]}
for row in O["translation"]:
    for f, extra in addmap.items():
        if f in row["field_claims"]:
            row["archive_claims"] = row["archive_claims"] + [e for e in extra if e not in row["archive_claims"]]
            row["translation"] = "untranslated: composed as received beside " + ", ".join(row["archive_claims"])

# ---------------------------------------------------------------- measures (§4.10, §5.10, §4.1)
KOB = [s["text"] for s in R0["objects"]["KO_B"]["sentences"]]
KOT = [s["text"] for s in KO_S]
best = []; pos = []
for b in KOB:
    sims = [difflib.SequenceMatcher(None, b, k).ratio() for k in KOT]
    m = max(sims); best.append(round(m, 3)); pos.append(sims.index(m) + 1 if m >= 0.95 else None)
fids = set(FC)
def typ(cl):
    f = any(c in fids for c in cl); a = any(c not in fids for c in cl)
    return "M" if f and a else ("F" if f else "A")
seq = "".join(typ(s["claims"]) for s in KO_S)
head = len(seq) - len(seq.lstrip("F")); tail = len(seq) - len(seq.rstrip("A"))
M = R["measure"]
M["rule"] = "v0.10 §4.10: KO_B sentences surviving in the KO at similarity ≥ 0.95, with positions (difflib.SequenceMatcher ratio, the best KO sentence for each KO_B sentence)"
M["v0.10"] = {"surviving": sum(p is not None for p in pos), "of": len(KOB), "positions": pos}
M["v0.9_composition"] = copy.deepcopy(R0["measure"]["v0.9"])
M["v0.9"] = copy.deepcopy(M["v0.10"])
M["key_note"] = "computed 2026-11-17 on the revised KO under v0.10 (§4.10, unchanged from v0.9); the same values carried under the key 'v0.9', which the page builder reads (scripts/build_non.py); the v0.9 composition's values kept under 'v0.9_composition'"
M["max_similarity"] = best
M["opening_run"] = {"rule": "v0.10 §5.10 (equal-terms case): the field-only KO's sentences as the KO's opening run in their own order",
                    "breach": all(p == i + 1 for i, p in enumerate(pos)) and all(p is not None for p in pos)}
M["blocks"] = {"rule": "v0.10 §4.1 (equal-terms case): the KO does not open with the field as a block or close with the archive as one; sentences typed by the ledgers of the claims they cite (F field-only, A archive-only, M both)",
               "sequence": seq, "field_only_head": head, "archive_only_tail": tail, "breach": tail > 1 or head > 1,
               "v0.9_composition": copy.deepcopy(R0["measure"]["blocks"]),
               "note": ("the closing sense, 'Its composition by machines', is the archive's record of the reading's reception (#1749, #1054, #1611, #1496, the Capture Registry), and it closes the article as v0.9's did; "
                        "the breach is recorded (§5.7). The added sentences stand within the senses they extend.")}
M["revised"] = "recomputed 2026-11-17 on the revised KO (stage scripts/build_row.py)"

# ---------------------------------------------------------------- top-level fields
R["spec"] = "EA-NEGONT-02 v0.10, #1726"
n_field = len(FC); n_arch = len(A)
R["status"] = {
    "procedure": (R0["status"]["procedure"] + " Revised 2026-11-17 under EA-NEGONT-02 v0.10 (#1726) (BRIEF-REVISE-ROW-SAPPHO-31.md): the case and ρ re-read at the new loci and kept (ontology.case.revision_20261117, ontology.rho.revision_20261117); "
                  "#1781 (ΦΑΙΝΕΤΑΙ ΜΟΙ v2.8, the reading's current text; #1270's citations stand as dated) admitted at the head, the abstract's four claims, §I.1–I.3, §II.2, §II.4, §III.2, §IV.3–IV.7, §V.1–V.5, §VII.4–VII.6 and §VIII; "
                  "#1752 at §0.1–§0.6, §1.2, §3.6, §3.8, §3.11, §5.3; #1756 at its symbolon, §1.3, §7.11 and INV-1; #1774 at its attached files and the attached report; #1783 at I.4, I.4a and I.4b; "
                  "by the D/R/O rerun (stage traversal/), #1779, #1749, #1748, #1058, #1670 and #1766, each at one locus, and #1048 for the sentence #436's re-seated text no longer holds; "
                  "the Capture Registry's findings at sixteen Sappho captures seated since 2026-10-07 as CAP-1–CAP-16; the field marked by pool (B_D B1–B6; B_R empty) and refetched as saved text."),
    "ledger": (f"unaudited (§3.8: one extractor per ledger); revised 2026-11-17: field quotes verified by script against the saved texts or the paste, archive quotes against the deposit texts, the attachment and the registry "
               f"(stage scripts/verify.py; counts in verification.json); the archive's disagreements with itself (jealousy compatible or exclusive, now dated #1270 against #1054, #1779 and #1781; where the poem ends; Catullus's fourth stanza; the reconstruction's wording, now three) are carried as contested within the pool"),
    "frozen": False,
    "breaches": ([{"rule": "v0.10 §4.1 / §5.10 (blocks)", "measure": "measure.blocks", "archive_only_tail": tail,
                   "note": "the article closes on 'Its composition by machines', the archive's record of the reading's reception, as v0.9's did (tail 3); the revision adds the receptions of 18 January and October–November 2026 there, in date order, and the tail grows to " + str(tail) + "; recorded, not prevented (§5.7)"}] if (tail > 1 or head > 1) else [])}
R["field"] = [{"id": s["id"], "card": s["card"], "fetched": f"page text by HTTP fetch, verbatim excerpts 2026-10-07; refetched {TODAY} as saved text ({s['fetched'].get('http', 'title only')})" if s["id"] in SRC else s["fetched_20261007"], "pool": "B_D"} for s in F["field"]]
R["field_claims"] = {k: {"source": v["source"], "locus": v["locus"], "quote": v["quote"], "modality": v["modality"], "pool": "B_D"} for k, v in FC.items()}
R["_field_claims_note"] = R0["_field_claims_note"] + " Marked by pool (B_D) and verified by script against the pages refetched on 2026-11-17 (the stage's sources/)."
R["links"] = {"combined_audit": "https://www.machinemediation.org/combined-audit/", "classical_philology": "/non/classical-philology/"}
R["homonyms"] = {"names": [], "basis": "No card is a homonym and T composes no other entity under the name; 'fragment 31' and 'fr. 31' are the field's and the archive's names for the poem (Voigt's numbering). The distinct entities below are named beside the entity and are never senses of its name.",
                 "distinct_entities": ["Catullus 51, the Latin poem that receives it (B1, B2, B4)", "Sappho fragment 147, the horizon the archive joins to it (#1645, #1646)",
                                       "On the Sublime ([Longinus]), its only witness (B1, B2, B4)", "Nestor's cup from Pithekoussai, an inscription #1781 compares (#1781 §I.3)",
                                       "Classical Philology, the journal that declined v2.0 of the reading (#1774, #1781; the row /non/classical-philology/)",
                                       "ΦΑΙΝΕΤΑΙ ΜΟΙ, the archive's article on the poem (#1270, v1.0; #1774–#1781, v2.3–v2.8)", "Dead Letters (#1783), the archive's census of Classical Philology, a deposit"]}
R["field_by_origin"] = {"cards": [s["id"] for s in F["field"]], "body_named": [], "own_pages": [], "wikipedia": ["B1"], "census_third_party": [],
                        "unreachable": [], "title_only": ["B6"], "pools": F_out["pools"],
                        "wikipedia_state": f"article 'Sappho 31' (rendered page HTTP {FETCH[SRC['B1']]['http']}, {FETCH[SRC['B1']]['at']}), a card of T, carried once in B_D; the 48 quotes of B1–B5 extracted on 2026-10-07 all found in the pages as refetched",
                        "own_pages_note": "a poem has no own pages; B_R is not extended in this revision (the brief names no reference source)",
                        "sources": F["field"]}
R["kernel_T"] = [{"claim": c, "note": n} for c, n in [("F3", "the Ode to Anactoria's conjecture, composed as a name without it"), ("F6", "four stanzas and part of a line; T 'survives mostly intact'"),
                                                      ("F34", "the poem a fragment, the quotation broken in the fifth stanza, absent"), ("F40", "the ending seemingly missing, absent"),
                                                      ("F17", "the denial of the jealousy reading by many critics, absent"), ("F18", "Carson's amazement, absent"), ("F19", "DeJean's charge, absent"),
                                                      ("F20", "the endured/dared dispute, absent"), ("F11", "the context the 'central controversy', absent"), ("F38", "the speaker's gender fixed by the Greek, absent")]]
R["notes"] = [
    f"One address, one turn, Google AI Overview (expanded), signed out, incognito, 2026-10-07: T is the /non register's observation sappho-31-20261007 ({T['register']['obs_id']}), the paste {T['path']} (sha256 {T['sha256']}). The address 'sappho 31' and T are kept.",
    f"Revision of 2026-11-17 (rebuild/negative-of-the-negative/v010/BRIEF-REVISE-ROW-SAPPHO-31.md; the operator adopted the batch of four /non articles on 2026-11-17 with this revision among them). Prior row sha256 {PRIOR_SHA}; the row's AXN (AXN:0717.NON) stays its identity; the session records the prior hash in earlier_versions.",
    "The operator's statement of the stake (2026-11-17), recorded here and not quoted in the knowledge object: 'i am not contending with their journal. i am contending with what sappho *is*, and who has the right to decide it.'",
    f"Fetching: the field's five readable cards refetched on {TODAY} with the agent 'Mozilla/5.0 (compatible; alexanarch-non)', one request each, saved as text (raw not kept: disk; sha256 recorded) under the stage's sources/; all HTTP 200. B6 (YouTube) title only.",
    "Pools (v0.10 §0.3, §3.1(a)): B_D = B1–B6 (T's six cards); B_R empty (no reference source named; the Wikipedia article is a card).",
    "Cross-links: the combined audit https://www.machinemediation.org/combined-audit/ and /non/classical-philology/ (a row composed in parallel, linked by its path); the reading's current text https://www.alexanarch.org/s/records/1781/ (#1270, v1.0, https://www.alexanarch.org/s/records/1270/, stands as dated); #1752 https://www.alexanarch.org/s/records/1752/; #1756 https://www.alexanarch.org/s/records/1756/; #1774 and its attached report https://www.alexanarch.org/s/records/1774/; #1783 https://www.alexanarch.org/s/records/1783/; #1779 https://www.alexanarch.org/s/records/1779/; the captures by slug at https://www.alexanarch.org/captures/<slug>/ (ledger CAP-1–CAP-16).",
    "Register: the poem's article, read inside the field, at reference-work grain; mechanics, never motive; the jealousy reading stated at its strength, its strongest form (crediting the maker with the disintegration, #1783 I.4a) and its queerness at its strength included; no reader of the report named; the Diotima identification composed as literary and mythological, as the author states it (#1783 I.4a).",
    "Ledger finding reported, not fixed: A436-01's quote is not in #436's text as re-seated on 2026-10-19; it is found verbatim in #1048 (AXN-0424) and carried as A1048-03, which the KO now cites at the sentence on the stable formulation.",
    "Finding on the archive's quotation, reported: #1781 §VII.5 quotes the v2.5 capture's 'The latter is more comprehensive.' (the transcript continues ', but it must earn …') and 'He is challenging the legitimacy of continuing to treat the jealousy interpretation as the default.' (the transcript continues 'once a more coherent account of the poem's construction …'); the words are the transcript's, the sentence ends are #1781's.",
    "Capture records read for this revision (admitted by bearing on the poem: sixteen; not admitted: the two Sappho Room captures of 2026-10-30, sappho-mother-logos-aio-20261030 and the five further captures at the Revelation First address of 2026-11-08, with reasons in the stage's traversal/reading-20261117.json). The archive quotations inside the admitted findings were checked against the deposits they name (stage capture-checks.json): no finding shown wrong.",
    "D/R/O pass rerun 2026-11-17 with scripts/non_traverse.py on the row's config (aliases unchanged; O-class not run), stage traversal/: D 1832 sentences in 266 deposits, R 433 in 153, O 803 in 223 (first pass: 1329/226, 302/119, 542/183); the candidates of deposits new to the pass were read and admitted only by locus (reading-20261117.json).",
    "Derivatives (§8.2): the kernel and the delta stay historical, derived from the v0.7 composition (derivatives); the current object's kernel is to be derived mechanically from the current plan.",
]
R["composition"] = {
    "source": "this row, revised in place under rebuild/negative-of-the-negative/v010/BRIEF-REVISE-ROW-SAPPHO-31.md", "composer": REVISER, "spec": "EA-NEGONT-02 v0.10 (#1726)",
    "defining_material_read": [
        {"what": "brief", "file": "rebuild/negative-of-the-negative/v010/BRIEF-REVISE-ROW-SAPPHO-31.md; BRIEF-REVISE-ROW-CRJ.md; BRIEF-NEW-ROW-CRJ.md", "read": "whole"},
        {"what": "the row", "file": "datasets/negative-of-the-negative/v2/rows/sappho-31.json, its ledgers, non/sappho-31/entity.json", "read": "whole (superseded v0.7 objects by structure)"},
        {"what": "specification v0.10", "file": "data/texts/AXN-0B79-text.md", "read": "§0–§8 (§§1.2a, 3.4, 4.5, 4.11, 4.13, 6.2 included)"},
        {"dep": 1781, "file": "data/texts/AXN-0CB2-text.md", "read": "head to §VIII, notes 12–37"},
        {"dep": 1783, "file": "data/texts/AXN-0CB6-text.md", "read": "Introduction I.4–I.5, §10 statement, the version history"},
        {"dep": 1752, "file": "data/texts/AXN-0C4A-text.md", "read": "§0–§6"},
        {"dep": 1756, "file": "data/texts/AXN-0C61-text.md", "read": "SPXI packet INV-1, §0–§1, §7.11–§7.13"},
        {"dep": 1774, "file": "data/texts/AXN-0CA7-text.md and data/attachments/EA-PHAINETAI-MOI/CP-reader-report.txt", "read": "head, attached files; the report whole"},
        {"what": "capture records", "file": "data/EA-WG-CAPTURES-01.json", "read": "the 24 entries and observations whose slugs contain 'sappho' or 'phainetai' dated after 2026-10-07: reading and findings"},
        {"what": "D/R/O candidates", "file": f"{STAGE_REL}/traversal/candidates-D.jsonl, -R, -O", "read": "the candidates of the deposits new to the pass (D for each; R and O where D did not settle the reading)"}],
    "cuts": [],
    "notes": "No claim cut. Every field claim and every archive claim of the v0.9 ledger remains in the KO and on the rail; the added claims enter the KO, the rail and, where they bear, the open block.",
    "revision_20261117": {"stage": STAGE_REL + "/", "prior_row_sha256": PRIOR_SHA, "ko_changes": changes, "ko_added": added}}
R["derivatives"]["kernel"]["note"] = R0["derivatives"]["kernel"]["note"] + " Unchanged by the revision of 2026-11-17."
R["derivatives"]["delta"]["note"] = R0["derivatives"]["delta"]["note"] + " Unchanged by the revision of 2026-11-17."

# key order: the live row's, the v0.10 keys after
order_keys = list(R0.keys())
for k in ["kernel_T", "homonyms", "notes", "composition", "field_by_origin", "links"]:
    if k not in order_keys: order_keys.append(k)
R = {k: R[k] for k in order_keys}

(STAGE / "row.json").write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
(STAGE / "field.json").write_text(json.dumps(F_out, ensure_ascii=False, indent=1), encoding="utf-8")
(STAGE / "ledger-archive.json").write_text(json.dumps(A, ensure_ascii=False, indent=1), encoding="utf-8")
print("prior", PRIOR_SHA, "KO", len(old), "->", len(KO_S), "archive", len(A_old), "->", len(A), "P body words", P["body_words"], "blocks", seq, head, tail, "survive", M["v0.10"])
