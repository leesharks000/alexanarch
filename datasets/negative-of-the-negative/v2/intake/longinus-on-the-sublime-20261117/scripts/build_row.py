"""Build the /non row longinus-on-the-sublime (2026-11-17) from claims.py and compose.py: the two ledgers, the
traversal reading, the row, and verification.json. Every quote is checked against its saved text.
   /tmp/py312/python3 -I build_row.py"""
import json, re, hashlib, difflib, collections, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from vlib import *
from claims import *
from compose import *

ROW = "longinus-on-the-sublime"
V2 = ROOT / "datasets/negative-of-the-negative/v2"
INR = "datasets/negative-of-the-negative/v2/intake/longinus-on-the-sublime-20261117/"
REGD = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
FR = json.loads((INTAKE / "sources/fetch-records.json").read_text(encoding="utf-8"))
paste = (ROOT / PASTE).read_text(encoding="utf-8")
eT = entry(SLUG_T); eO = entry(SLUG_O)
SPEC = "EA-NEGONT-02 v0.10, #1726"
COMPOSER = "Claude (Opus 5.5), subagent, 2026-11-17"
cap_url = lambda s: f"https://www.alexanarch.org/captures/{s}/"
rec_url = lambda n: f"https://www.alexanarch.org/s/records/{n}/"
fails = []

def sha(b): return hashlib.sha256(b).hexdigest()

# ---------------- field ledger ----------------
src = {s[0]: s for s in SOURCES}
field_sources = []
for (sid, origin, pool, card, kind, files, fids, title_only, role) in SOURCES:
    fl = {}
    for f in files:
        p = INR + "sources/" + f
        fl[f] = {"path": p, "sha256": sha((ROOT / p).read_bytes())}
    tried = []
    for fid in fids:
        r = FR[fid]
        tried.append({"url": r["url"], "at": r["at"], "http": r["http"], "final_url": r["final_url"], "agent": r["agent"],
                      "raw_sha256": r["raw_sha256"], "bytes": r["bytes"],
                      "result": ("read: HTTP 200, saved as text (raw not kept: disk)" if r["http"] == 200 else
                                 f"unreachable: HTTP {r['http']}; one request with the row's agent string, no retry by another route")
                      + (f"; {r.get('body_head','')[:120]}" if r.get("body_head") else "")})
    if sid == "B4":
        tried.append({"search": ["WebSearch '\"The Nature of Writing\" Longinus On the Sublime five sources' (2026-11-17)",
                                 "WebSearch 'natureofwriting.com Longinus sublime' (2026-11-17)",
                                 "WebSearch '\"Nature of Writing\" Longinus \"On the Sublime\" video OR lesson' (2026-11-17)"],
                      "result": "no page on the treatise found; the site's search returned its home page"})
    if sid == "B9":
        tried[0]["result"] = "read: HTTP 200, the rendered page is the article 'On the Sublime' (the redirect followed); not saved twice (B1 holds it)"
    if sid == "B10":
        for t in tried[1:]:
            t["result"] = "unreachable: HTTP 404 (the page title tried does not exist); not a refusal"
        tried.append({"url": "https://en.wikisource.org/w/api.php?action=query&list=prefixsearch&pssearch=On%20the%20Sublime", "at": "2026-11-17",
                      "http": 429, "result": "refused: 'You are making too many requests to the API' (rate limit); not retried"})
    ent = {"id": sid, "origin": origin, "pool": pool, "card": card, "kind": kind, "role": role, "files": fl,
           "fetched": {"tried": tried} if tried else {"tried": [], "note": "title only; not fetched (no target in the paste)"},
           "title_only": title_only, "url": (FR[fids[0]]["url"] if fids else None),
           "surfaced_by_T": ([{"slug": SLUG_T, "card": sid}] if pool == "B_D" else []),
           "names_operator": "no" if files else "unread", "names_archive": "no" if files else "unread"}
    if sid == "B1": ent["also_origin"] = "body_named"; ent["revision"] = {"oldid": 1385253389, "last_edited": "2026-11-12T14:26Z"}
    if sid == "B5": ent["also_origin"] = "body_named"
    field_sources.append(ent)

field_claims = {}
for (fid, s, locus, q, claim, mod, kind, kern, const, lin, date) in FIELD:
    S = src[s]
    hay = paste if S[7] else "\n".join((INTAKE / "sources" / f).read_text(encoding="utf-8") for f in S[5])
    ok = found(q, hay)
    if not ok: fails.append(("field", fid))
    field_claims[fid] = {"source": s, "locus": locus, "quote": q, "claim": claim, "modality": mod, "kind": kind,
                         "kernel": kern, "const": const, "lineage": lin, "date": date, "quote_ok": ok,
                         "origin": S[1], "pool": S[2],
                         "checked_against": ("the paste (title as pasted), " + PASTE) if S[7] else
                         f"saved text of {s} under {INR}sources/, whitespace-normalised; multi-part quotes joined by ' … ', each part checked"}
    if S[7]: field_claims[fid]["title_only"] = True
pools = {"B_D": [s[0] for s in SOURCES if s[2] == "B_D"], "B_R": [s[0] for s in SOURCES if s[2] == "B_R"]}
FIELD_LEDGER = {
 "row": ROW, "address": "longinus on the sublime", "addresses": ["longinus on the sublime"], "extracted": "2026-11-17",
 "extractor": COMPOSER + ", one extractor (unaudited, §3.8)",
 "rule": "v0.10 §3.5, source-neutral: opening or abstract, defined terms, headline claims, stated limits; quotes verbatim from the saved page texts (whitespace-normalised for the check; multi-part quotes joined by ' … ', each part checked); title-only cards quoted by their title as pasted",
 "B_note": "The field in two pools (v0.10 §0.3, §3.1(a)). B_D: the AI Mode cards as pasted (B1 Wikipedia '+1', also named in the body; B2 YouTube, twice, title from the strip; B3 EBSCO '+1'; B4 The Nature of Writing '+2'; B5 Project Gutenberg '+1', also named in the body), the results strip's titles (B6) and the platforms the body names (B7). B_R: the treatise's Greek text at Perseus (B8, Roberts 1907, chapter 10), Wikipedia 'Longinus (literature)' (B9, a redirect to B1) and Wikisource (B10, Havell 1890). The sources behind the '+N' counts are not in the paste.",
 "lineage_note": "Lineages (§3.6): what it is; its author; the manuscript and its state; its form and addressee; its exemplars; its doctrine; its faults; Sappho's poem in the treatise; the text of chapter 10; its reception; unread cards; the results strip; where to read it.",
 "pages": f"saved text files under {INR}sources/ (text only, scripts and styles stripped; raw responses not kept for disk, their sha256 in sources/fetch-records.json)",
 "field": field_sources, "field_claims": field_claims, "field_sources": {s[0]: s[3] for s in SOURCES}, "pools": pools}

# ---------------- archive ledger ----------------
arch = []
for (aid, dep, locus, q, claim, kind, mod, strata, kern, lin) in ARCH:
    d = REGD[dep]; f = d["full_text_path"].lstrip("/")
    ok = found(strip_md(q), deposit_text(f))
    if not ok: fails.append(("archive", aid))
    creator = d.get("creator") or d.get("creators")
    if isinstance(creator, list): creator = "; ".join(c if isinstance(c, str) else c.get("name", "") for c in creator)
    c = {"id": aid, "dep": dep, "axn": d.get("axn"), "claim": claim, "kind": kind, "modality": mod, "strata": strata,
         "locus": locus, "quote": q, "kernel": kern, "const": False, "lineage": lin, "date": d.get("date"),
         "title": d.get("title"), "creator": creator, "file": f, "record": {"url": rec_url(dep), "label": f"#{dep}"},
         "quote_ok": ok, "quote_check": "within the deposit text as loaded (whitespace-normalised; markdown emphasis stripped)"}
    if dep == 1781:
        c["instances"] = "one work in versions (§3.4 S4: grouped as one lineage and kept): #1774 (v2.3) to #1781 (v2.8), all 16 November 2026; #1270 (v1.0, 9 January 2026) under Rebekah Cranes; the current text is #1781"
    arch.append(c)
for (cid, slug, fld, q, claim, kind, mod, kern, lin) in CAP:
    e = eT if slug == SLUG_T else eO
    ok = found(q, entry_text(slug))
    if not ok: fails.append(("cap", cid))
    arch.append({"id": cid, "dep": "capture-registry", "record": {"url": cap_url(slug), "label": "CAP"}, "surface": {"url": cap_url(slug)},
                 "claim": claim, "kind": kind, "modality": mod, "strata": ["D"], "locus": f"{slug}, {fld}", "quote": q,
                 "kernel": kern, "const": False, "lineage": lin, "date": e["date"],
                 "title": f"Capture Registry (EA-WG-CAPTURES-01), entry {slug} ({e['obs_id']}, {e['axn']})",
                 "creator": "Lee Sharks (the registry)", "file": "data/EA-WG-CAPTURES-01.json", "quote_ok": ok,
                 "quote_check": "within the entry's reading, analysis, findings, q_kind and basis fields as loaded (whitespace-normalised)"})
AIDS = {c["id"]: c for c in arch}

# ---------------- KO and its plan ----------------
ids = set(field_claims) | set(AIDS)
def typ(cl):
    f = any(c in field_claims for c in cl); a = any(c in AIDS for c in cl)
    return "M" if f and a else ("F" if f else "A")
ko = [{"n": i + 1, "para": s, "sense": SENSES[s], "text": t, "claims": cl} for i, (s, t, cl) in enumerate(KO)]
kob = [{"n": i + 1, "para": s, "text": t, "claims": cl} for i, (s, t, cl) in enumerate(KO_B)]
ko_c = [c for s in ko for c in s["claims"]]
unknown = sorted(set(ko_c) - ids)
not_in_ko = sorted(ids - set(ko_c))
senses = collections.OrderedDict((n, [s["n"] for s in ko if s["sense"] == n]) for n in SENSES)

# prose checks (§ Prose): no 'rather than', 'instead of', 'not X but Y' outside quotations
def unquoted(t): return re.sub(r'"[^"]*"|“[^”]*”', '', t)
prose_flags = []
for s in ko + kob:
    u = unquoted(s["text"])
    for pat in (r"\brather than\b", r"\binstead of\b", r"\bnot\b[^.;:]{0,60}\bbut\b", r", not\b"):
        if re.search(pat, u, re.I): prose_flags.append((s["n"], pat))

# measure (§4.10): KO_B sentences surviving in the KO at ≥ 0.95
def sim(a, b): return difflib.SequenceMatcher(None, a, b).ratio()
best = []
for b in kob:
    m = max(((sim(b["text"], k["text"]), k["n"]) for k in ko), key=lambda x: x[0])
    best.append(m)
surv = [(i + 1, n) for i, (r, n) in enumerate(best) if r >= 0.95]
seq = "".join(typ(s["claims"]) for s in ko)
head = len(seq) - len(seq.lstrip("F")); tail = len(seq) - len(seq.rstrip("A"))
ko1_max = max(sim(ko[0]["text"], b["text"]) for b in kob)

# P word counts
WRE = r"[A-Za-z0-9'’-]+"
def wc(t): return len(re.findall(WRE, t))
def body_words(p): return wc(p["lede"][0]) + sum(wc(l) + wc(t) for (_, _, items) in p["sections"] for (l, t, _) in items)
pw = body_words(P); pbw = body_words(P_B)

def mkP(p, title, extra):
    out = {"title": title, **extra, "lede": {"text": "On the Sublime " + p["lede"][0], "claims": p["lede"][1]},
           "sections": [{"icon": i, "head": h, "items": [{"label": l, "text": t, "claims": c} for (l, t, c) in items]} for (i, h, items) in p["sections"]],
           "open": [{"question": q, "rests_on": r, "modality": m, "would_resolve": w} for (q, r, m, w) in p["open"]]}
    return out

# rail: lineages (one card per lineage, §5.2)
lin_claims = collections.OrderedDict()
for fid, c in field_claims.items(): lin_claims.setdefault(c["lineage"], []).append(fid)
for c in arch: lin_claims.setdefault(c["lineage"], []).append(c["id"])
def earliest(cl):
    fs = [c for c in cl if c in field_claims]
    if fs: return field_claims[fs[0]]["source"]
    deps = [(AIDS[c]["date"] or "9999", AIDS[c]["dep"]) for c in cl if AIDS[c]["dep"] != "capture-registry"]
    if deps: return min(deps)[1]
    return "Capture Registry"
rail = [{"lineage": l, "claims": cl, "earliest": earliest(cl)} for l, cl in lin_claims.items()]
rail_B = [r for r in rail if all(c in field_claims for c in r["claims"])]
rail_c = {c for r in rail for c in r["claims"]}
kernels_off_rail = sorted([k for k, c in field_claims.items() if c["kernel"] and k not in rail_c] + [c["id"] for c in arch if c["kernel"] and c["id"] not in rail_c])
p_ids = set(P["lede"][1]) | {c for (_, _, it) in P["sections"] for (_, _, cl) in it for c in cl} | {c for (_, r, _, _) in P["open"] for c in r}
p_unknown = sorted(p_ids - ids)

# translation (every field claim exactly once)
tr_rows = []; seen = collections.Counter()
for (lin, fcs, acs) in TRANSLATION:
    for f in fcs: seen[f] += 1
    rec = "; ".join(f"{f} ({field_claims[f]['source']}, {field_claims[f]['locus']}): \"{field_claims[f]['quote']}\"" for f in fcs)
    tr_rows.append({"lineage": lin, "field_claims": fcs, "received": rec, "receiving_text": "—",
                    "translation": "untranslated: composed as received beside " + ", ".join(acs), "archive_claims": acs})
tr_missing = sorted(set(field_claims) - set(seen)); tr_dupes = sorted(k for k, v in seen.items() if v > 1)

# T
T_words_text = paste.split("[SYSTEM]", 1)[1]
t_words = wc(T_words_text)
t_sha = sha(eT["transcript"].encode("utf-8"))
t_claims = [f"{tid} {kind}: '{q}' ({card})" for (tid, kind, q, card) in T_CLAIMS]
t_fail = [tid for (tid, _, q, _) in T_CLAIMS if not found(q, paste)]
card_rail = [{"n": c["n"], "site": c["site"], "title": c.get("title"), "snip": c.get("snip"), "note": c.get("note")} for c in eT["cite_list"]]

# moves -> KO sentences and P labels
moves = []
for (mv, span, mtype, ans, p_at) in MOVES:
    ko_at = [s["n"] for s in ko if set(s["claims"]) & set(ans)]
    moves.append({"move": mv, "span": span, "type": mtype, "answered_by": ans, "ko": ko_at, "p": p_at})
move_gaps = [m["move"] for m in moves if not m["ko"]]

# kernel
kernel = []
for i, (cid, sense, contrast, f, qual) in enumerate(KERNEL):
    c = field_claims.get(cid) or AIDS[cid]
    kernel.append({"K": f"K{i+1}", "claim": f"`{cid}`", "source": (f"#{c['dep']}" if c.get("dep") not in (None, "capture-registry") else "Capture Registry") if cid in AIDS else c["source"],
                   "M_src": c["modality"], "sense": sense, "qualifiers carried": qual,
                   "f (source's own falsifiers)": (", ".join(f) if f else "— (none stated; watch: a later composition at the address that states or drops the claim, attributed or not, uptake §8.3)"),
                   "contrast": contrast,
                   "resolver": "a later capture at 'longinus on the sublime' (ADDR-33356aaa6980) on Google AI Mode or AI Overview, seated in the Capture Registry (§8.3)"})

# ---------------- reading.json ----------------
TR = V2 / "traversal" / ROW
cand = {k: [json.loads(l) for l in open(TR / f"candidates-{k}.jsonl", encoding="utf-8")] for k in "DROH"}
admitted = {
 1781: (["D", "R"], "ΦΑΙΝΕΤΑΙ ΜΟΙ v2.8: §V.1 (the transmission, the manuscript, the editions, Bergk, the dialect seam), §V.1a (the commentator's sentence; the innocent reading first; the conjecture with its status and falsifiers), §§III.1–2, IV.2, IV.5 (the praise of selecting and binding; the faculties 'as another's'; the fear supplied), §V.2 (design held open), n. 18 (Voigt's obelus), n. 35 (the count corrected); R: Longinus as the receiver in whose quotation the poem survives, related to the archive's future-reader reading"),
 1752: (["D"], "Invidens Sappho: §0.4, §2.4 (Longinus quotes the poem as the work of a maker), §3.1 (Hall 1652 and Boileau 1683 from Longinus's Greek), §3.7 (Bergk's note on v. 17), §5.3 (selection and jealousy compatible)"),
 1783: (["D"], "Dead Letters: I.4a (the treatise the poem's only witness, reaching the philosopher edited; the poem antiquity quoted as the example of the sublime; Longinus's word is binding), I.4b (the liberation's first operation; the maker in the selecting and the binding)"),
 1458: (["D", "O"], "The Echo and the Stamp: the treatise read as a theory of transmissional inscription (head, §I, §IV, §VI, §XIV with its registers, what is held open and what is not claimed); O-direct: the archive's categories (transmission, inscription, erasure) applied to the treatise by the archive itself"),
 1476: (["D"], "φωνῆς δίχα: Description (the continuous construal; the dialect seam with P = 0.209) and Falsification Conditions"),
 1478: (["D", "R"], "The Socket and the Stamp: title (Longinus 10.2–3 as the first filling), Description (the sole witness writes continuous prose), Falsification Conditions (no claim of intention); R: the treatise's sentence related to the archive's socket"),
 1485: (["D"], "The Apparatus Was the First Summary Layer, the author-slot case (line 75): the index entry Διονυσίου ἢ Λογγίνου read as a disjunction"),
 1483: (["D", "R"], "the Ω erratum (head, line 4): the treatise as the key of the archive's Logos chain (R: relation to the archive's Historical Logos)"),
 1532: (["D"], "The Transforming Body of Sappho 31, 'Longinus: reception becomes a theory of reception': chapter 10 sui generis"),
 283: (["D"], "Sappho and the Crimson Hexagon (9 January 2026), the earliest statement: the treatise treats the fragment as technical achievement"),
 625: (["D"], "Prolegomena to the Historical Logos (5 April 2026): the poem becomes a theory of language in Longinus's reading"),
 1412: (["D"], "The Fixed Point of Destruction: reading Sappho through what Longinus wanted (a stated limit on the witness)"),
 1504: (["D"], "EA-CORPORA-01/06: the archive's seat of Roberts's Greek, verified at 10.2"),
}
instances = {1270: 1781, 1774: 1781, 1775: 1781, 1777: 1781, 1778: 1781, 1780: 1781, 895: 496, 902: 625, 1176: 626, 1761: 626, 1763: 626, 1764: 626, 1765: 626,
             1484: 1483, 1709: 1711, 1722: 1721, 1211: 832, 1216: 832, 1217: 832, 1400: 832, 1218: 859, 1373: 109, 1362: 683, 134: 283}
lineage_of = {
 "the treatise as fragment 31's witness (a transmission fact restated)": [38, 109, 201, 281, 306, 313, 337, 496, 503, 576, 626, 828, 832, 859, 950, 1048, 1049, 1051, 1052, 1053, 1054, 1508, 1601, 1645, 1670, 1704, 1770, 1769, 1749, 1756, 1757, 1748, 1779],
 "the edge of the quotation (the erratum sequence and its restatements)": [1474, 1475, 1477, 1482, 1487, 1494, 1496, 1569, 1575, 1658, 1684, 1611, 1643, 1721],
}
reasons_reject = {
 683: "the Spear of Longinus (the centurion of the Passion), a homonym", 1362: "the Spear of Longinus, a homonym (an instance of #683)",
 1570: "Longinus as an author in the authorship investigation's null set of Greek prose; no claim on the treatise", 1571: "the same null set; no claim on the treatise",
 1486: "Philo's reception of Sappho 31; Longinus named as a corpus fetched and as a comparandum; no claim on the treatise beyond its witness (lineage of #1781 §V.1)",
 1511: "a web surface of the Revelation line; 'Sappho → Longinus, ATTESTED, the quotation-joint' restates the witness",
 1532: None, 1611: "the negative-ontology notebook lists Longinus among concepts; no claim", 1684: "the prediction index lists the Sappho papers by title; no claim of its own",
 1704: "the /non introduction quotes the Sappho 31 Overview; no claim on the treatise", 1716: "a seating note: 'The shelf held Longinus (01/06)'; no claim",
 1721: "a capture list naming the Ω erratum title", 1722: "the same (an instance of #1721)",
}
verdicts = []
for dep, (strata, reason) in sorted(admitted.items()):
    cl = [c["id"] for c in arch if c["dep"] == dep]
    cids = [x["cand_id"] for k in "DRO" for x in cand[k] if x["dep"] == dep]
    verdicts.append({"dep": dep, "strata": strata, "reason": reason, "claims": cl, "candidates": cids, "lineage_instances": sorted(k for k, v in instances.items() if v == dep)})
not_admitted = []
admitted_deps = set(admitted)
for k in "DRO":
    for x in cand[k]:
        d = x["dep"]
        if d in admitted_deps: continue
        if d in reasons_reject and reasons_reject[d]:
            r = reasons_reject[d]
        elif d in instances:
            r = f"an instance of #{instances[d]} (one work or a duplicate deposit; S4: grouped and kept in the provenance graph)"
            if instances[d] in admitted_deps: r += "; its claims carried through the admitted text"
        else:
            r = None
            for lin, deps in lineage_of.items():
                if d in deps:
                    r = f"read: the sentence restates {lin.split(' (')[0]}; S4: it adds no mechanism, qualification, evidentiary basis, substrate, falsifier or revision to the lineage carried by #1781, #1783, #1478 and #1458"
                    break
            if r is None: r = "read: a bare mention or reference-list line; no claim on the treatise of the stratum's kind"
        not_admitted.append({"dep": d, "cand": x["cand_id"], "stratum": k, "reason": r})
hop_rej = []
for x in cand["H"]:
    d = x["dep"]
    if d in admitted_deps: continue
    in_dro = any(y["dep"] == d for k in "DRO" for y in cand[k])
    hop_rej.append({"cand": x["cand_id"], "dep": d, "direction": x["direction"], "via": x["via_admitted"],
                    "verdict": ("rejected: also a string candidate, read under D/R/O" if in_dro else
                                "rejected: term-absent hop candidate read at its head and abstract; it bears on Sappho 31, the archive's instruments or other entities, and says nothing of the treatise")})
READING = {
 "row": ROW, "pass": "2026-11-17: first reading of D, R and O candidates (748 D sentences in 92 deposits, 93 R in 45, 225 O-direct in 64); one citation hop forward and back from the thirteen deposits admitted (124 candidates)",
 "procedure": "EA-NEGONT-02 v0.10 §3.4 D/R/O (working; not frozen). D where a deposit names the treatise and says something of it; R where it relates the treatise to an archive object (the future-reader reading, the socket, the Historical Logos); O-direct where the archive applies its own categories to the treatise (#1458). No O-class: the field sources the treatise as a work of literary criticism (B1, B3), and no archive category is applied to that class at a locus.",
 "reader": COMPOSER, "config": f"datasets/negative-of-the-negative/v2/traversal/{ROW}/config.json",
 "verdicts": verdicts, "not_admitted": not_admitted, "rejected": not_admitted,
 "hop": {"from": sorted(admitted_deps), "candidates": len(cand["H"]), "admitted": [], "rejected": hop_rej},
 "lineages": [{"lineage": "the treatise as fragment 31's witness", "instances": [283, 1504, 1781, 1783] + lineage_of["the treatise as fragment 31's witness (a transmission fact restated)"], "earliest": 283},
              {"lineage": "the maker who selects and binds", "instances": [283, 496, 1752, 1781, 1783], "earliest": 283},
              {"lineage": "the treatise as a theory of transmission", "instances": [625, 1458, 1532, 1483], "earliest": 625},
              {"lineage": "the edge of the quotation", "instances": [1052, 1474, 1476, 1478, 1752, 1781, 1783], "earliest": 1052},
              {"lineage": "the commentator's sentence", "instances": [1476, 1478, 1781], "earliest": 1476},
              {"lineage": "the author-slot", "instances": [1485], "earliest": 1485},
              {"lineage": "reading through the quoter", "instances": [1412], "earliest": 1412},
              {"lineage": "the seat of the text", "instances": [1504], "earliest": 1504}],
 "observations": [
   "The archive names the treatise in 92 deposits. Most name it as fragment 31's witness ('preserved in Longinus, On the Sublime 10.2'); these restate one transmission fact, carried by #1781 §V.1 and #1783 I.4a, and earliest at #283 (9 January 2026).",
   "The archive's account of the treatise itself is #1458 (The Echo and the Stamp, 14 August 2026): a theory of transmissional inscription, with its registers, what it holds open and what it does not claim. #625 (5 April 2026) is the earliest statement that the poem becomes 'a theory of language itself' in Longinus's reading.",
   "The archive contests itself on the commentator's sentence: #1476 construes πένητα as the object of θαυμάζεις; #1781 (v2.8) reads it as governed by no verb and corrects #1478's count of eight subjectless verbs to seven. Both are carried (§4.4 P_coh).",
   "The string 'Longinus' also reaches the Spear of Longinus (#683, #1362) and Longinus as an author in the authorship null set (#1570, #1571); set aside. Cassius Longinus appears only in the field (B1)."],
 "counts": {"D_candidates": len(cand["D"]), "D_deposits": len({x['dep'] for x in cand['D']}), "R_candidates": len(cand["R"]), "R_deposits": len({x['dep'] for x in cand['R']}),
            "O_candidates": len(cand["O"]), "O_deposits": len({x['dep'] for x in cand['O']}), "H_candidates": len(cand["H"]),
            "deposits_admitted": len(admitted), "deposit_claims": sum(1 for c in arch if c["dep"] != "capture-registry"),
            "CAP_claims": sum(1 for c in arch if c["dep"] == "capture-registry")},
 "records": {"CAP": sum(1 for c in arch if c["dep"] == "capture-registry"), "note": f"the archive's own records of the entity, ledgered beside the deposits: the Capture Registry's reading, analysis and findings at {SLUG_T} (CAP-1-NN) and at {SLUG_O} (CAP-2-NN)"},
}

# ---------------- write ledgers and reading ----------------
LED = V2 / "ledgers" / ROW
(LED / "field.json").write_text(json.dumps(FIELD_LEDGER, ensure_ascii=False, indent=1), encoding="utf-8")
(LED / "ledger-archive.json").write_text(json.dumps(arch, ensure_ascii=False, indent=1), encoding="utf-8")
(TR / "reading.json").write_text(json.dumps(READING, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------- the row ----------------
def L_text(sents): return " ".join(s["text"] for s in sents)
cnt = collections.Counter(s[2] for s in SOURCES)
deps_def = sorted(admitted_deps)
from frame import frame
row_out = frame(eT, eO, field_claims, AIDS)
for L in row_out["ontology"]["case"]["loci"]:
    if not found(strip_md(L["quote"]), deposit_text(REGD[L["dep"]]["full_text_path"].lstrip("/"))): fails.append(("case-locus", L["dep"], L["locus"]))
row_out["objects"] = {
 "T": {"path": INR + "T1-" + SLUG_T + ".txt", "sha256": t_sha, "words": t_words, "cards": 5,
       "words_note": f"one turn (the composition, the results strip and the closing furniture as pasted; the bracketed header and the query line excluded): {t_words} words; 5 cards (Wikipedia '+1', YouTube '+1' twice, EBSCO '+1', The Nature of Writing '+2' beside YouTube, Project Gutenberg '+1'), the results strip of eight titles beside them",
       "claims": t_claims, "register": {"register": "data/EA-WG-CAPTURES-01.json", "slug": SLUG_T, "obs_id": eT["obs_id"]},
       "transcripts": [{"slug": SLUG_T, "address": "longinus on the sublime", "addr_id": eT["addr_id"], "obs_id": eT["obs_id"], "axn": eT["axn"],
                        "sha256": t_sha, "sha256_of": "the registry's transcript string (data/EA-WG-CAPTURES-01.json, entries[slug].transcript), UTF-8; identical to the paste",
                        "words": t_words, "cards": 5, "card_rail": card_rail, "claims": t_claims, "path": INR + "T1-" + SLUG_T + ".txt",
                        "pastes": [INR + "paste-longinus-on-the-sublime-ai-mode.txt (12:02 EST; sha256 " + sha(paste.encode('utf-8')) + ", copied from rebuild/capture-registry/intake-20261117-longinus/)"],
                        "address_note": "the query asked for by the session at 11:44 ('longinus on the sublime'); not shown in the paste (the paste's [QUERENT] line is the intake's, as its header says)"}]},
 "KO": {"title": "On the Sublime", "genre": "knowledge object, equal case, under EA-NEGONT-02 v0.10 (#1726): the final article form of the entity (§4.13), natural sentences under descriptive subheadings (each sentence's sense), attribution beneath each sentence by claim id (§4.5); sources named in the prose only where the holder is part of what is said (the archive's readings, the Capture Registry's findings, a dispute between sources)",
        "status": "composed 2026-11-17 under v0.10 on BRIEF-NEW-ROW-LONGINUS.md; not frozen", "sentences": ko,
        "joins": [
          {"act": "order of senses", "sentences": f"1–{len(ko)}", "claims": [], "note": "equal case (§4.7): what it is (¶0); its author and its manuscript (¶1); its form and its state (¶2); its doctrine (¶3); the treatise as a theory of transmission (¶4); Sappho's poem in the treatise (¶5); the edge of the quotation (¶6); the commentator's sentence (¶7); its reception and editions (¶8); the record of its reception by machines (¶9). Field and archive claims ordered together by genealogy within each sense"},
          {"act": "holding rivals (the manuscript's date)", "sentences": [7], "claims": ["F4", "A1781-01"], "note": "Wikipedia's 'tenth century' beside the archive's 'tenth or eleventh century', each with its holder"},
          {"act": "holding rivals within the archive (πένητα)", "sentences": [57, 58], "claims": ["A1476-01", "A1476-03", "A1781-24", "A1781-22"], "note": "#1476's continuous construal and #1781's reading of πένητα without a governing verb, both composed (§4.4 P_coh); #1781 n. 35 corrects #1478's count"},
          {"act": "compatible claims (the poem's name and the maker)", "sentences": [42, 44, 46], "claims": ["F16", "F41", "A1752-01", "A1752-05"], "note": "the field's 'so-called Ode to Jealousy' and the archive's maker composed together under the archive's own statement that selection and jealousy do not cancel (A1752-05)"},
          {"act": "the ending set beside the edge", "sentences": [17, 18], "claims": ["F43", "F44", "A1458-06", "A1458-09"], "note": "EBSCO's ending on a promise to write and #1458's reading of the two breaks"},
          {"act": "the registry's reading carried at its grade", "sentences": [74], "claims": ["CAP-1-08"], "note": "that the fifth source 'names the same operation' is the registry's interpretation; the KO states it as the registry's"}],
        "plan": {"order": ko_c, "senses": senses, "marks": {"A1476-01": "contested within the archive: A1781-24 (P_coh, both carried)", "A1781-14": "hypothesis (the author's conjecture), with its falsifiers A1781-16"}, "conflicts": [], "cuts": []},
        "governing_question": "the brief's: what the treatise is as the field holds it, its authorship as the field holds it, and the archive's bearing (the treatise as fragment 31's only witness, its praise of the maker who selects and binds, the edge of the quotation), each at its grade; mechanics, never motive"},
 "P": mkP(P, "On the Sublime", {"genre": "the compression: AIO's interaction grammar (lede, headed clusters, bolded labels, card rail), composed from the v0.10 plan in one claim space; it faces on the card",
                                "status": "composed 2026-11-17 from the v0.10 knowledge object; not frozen"}),
 "P_B": mkP(P_B, "On the Sublime", {"arm": "B (the field alone)", "genre": "popup — the compression from the field ledger alone (B_D and B_R)", "status": "composed 2026-11-17 from the field ledger alone; not frozen"}),
 "KO_B": {"title": "On the Sublime", "arm": "B (the field alone)", "genre": "knowledge object", "status": "composed 2026-11-17 from the field ledger alone; not frozen", "sentences": kob},
 "L_B": {"words": wc(L_text(kob)), "text": L_text(kob), "note": "L_F(B), the field-only composition, realized as KO_B (objects.KO_B)"},
 "L_BA": {"words": wc(L_text(ko)), "text": L_text(ko),
          "rail": [{"Card": f"{s[0]} {s[3]}", "Snippet": (field_claims[[k for k, c in field_claims.items() if c['source'] == s[0]][0]]["quote"])[:200]} for s in SOURCES]
                  + [{"Card": f"#{d} {REGD[d]['title'][:110]}", "Snippet": [c for c in arch if c['dep'] == d][0]["quote"][:200]} for d in deps_def]
                  + [{"Card": f"Capture Registry — {s}", "Snippet": [c for c in arch if c['locus'].startswith(s)][0]["quote"][:200]} for s in (SLUG_T, SLUG_O)],
          "note": "L(B ∪ A) in the equal-terms case (§0.4), realized as the knowledge object (objects.KO); its rail is one card per source, grouped by the compression's lineages at render (§5.2)"},
}
row_out["objects"]["P"]["body_words"] = pw
row_out["objects"]["P"]["body_words_rule"] = "lede plus every item's label and text (regex [A-Za-z0-9'’-]+; the bound is 350, §4.8)"
row_out["objects"]["P"]["entity"] = f"Composed under v0.10, equal case (ρ = extends): KO_B sentences surviving {len(surv)} of {len(kob)}; every field claim carried."
row_out["objects"]["P"]["rail"] = rail
row_out["objects"]["P_B"]["body_words"] = pbw
row_out["objects"]["P_B"]["rail"] = rail_B
row_out["objects"]["P_B"]["entity"] = "the field's entity: the first-century Greek treatise of literary criticism ascribed to Longinus, as Wikipedia, EBSCO and Roberts's Greek give it"
row_out["field"] = [{"id": s["id"], "card": s["card"], "fetched": ("; ".join(f"{t.get('url','search')} {t.get('result','')}" for t in s["fetched"]["tried"])[:400] or s["fetched"].get("note")), "origin": s["origin"], "pool": s["pool"]} for s in field_sources]
row_out["field_claims"] = field_claims
row_out["field_sources"] = FIELD_LEDGER["field_sources"]
row_out["delta"]["correction"]["moves"] = moves
row_out["delta"]["correction"]["check"] = ("every move answered by a knowledge-object sentence and a compression line; no gap" if not move_gaps else f"gaps: {move_gaps}")
row_out["kernel"] = kernel
row_out["kernel_T"] = [{"claim": c, "note": n} for (c, n) in KERNEL_T]
row_out["ontology"]["translation"] = tr_rows
row_out["measure"] = {
 "rule": "v0.10 §4.10: KO_B sentences surviving in the KO at similarity ≥ 0.95, with positions (difflib.SequenceMatcher ratio, the best KO sentence for each KO_B sentence, as apply_v09.py does)",
 "v0.10": {"surviving": len(surv), "of": len(kob), "positions": [n if r >= 0.95 else None for (r, n) in best]},
 "opening_run": {"rule": "v0.10 §5.10 (equal-terms case): the field-only KO's sentences as the KO's opening run in their own order", "breach": bool(surv and surv[0] == (1, 1))},
 "blocks": {"rule": "v0.10 §4.1 (equal-terms case): the KO does not open with the field as a block or close with the archive as one; sentences typed by the ledgers of the claims they cite (F field-only, A archive-only, M both)",
            "sequence": seq, "field_only_head": head, "archive_only_tail": tail, "breach": head > 5 or tail > 12,
            "note": "the closing sense, the record of its reception by machines, is the Capture Registry's by nature (CAP claims), with the field's strip and cards beside it; the archive-only tail is that sense"},
 "max_similarity": [round(r, 3) for (r, n) in best], "ko_sentence_1_max_similarity_to_KO_B": round(ko1_max, 3),
 "v0.9": {"surviving": len(surv), "of": len(kob), "positions": [n if r >= 0.95 else None for (r, n) in best]},
 "key_note": "the measure is computed under v0.10 (§4.10, unchanged from v0.9); the same values are carried under the key 'v0.9', which the page builder reads (scripts/build_non.py)"}
row_out["field_by_origin"] = {
 "cards": [s[0] for s in SOURCES if s[1] == "card"], "body_named": ["B1", "B5", "B7"], "own_pages": [s[0] for s in SOURCES if s[1] == "own_page"],
 "wikipedia": ["B1", "B9"], "census_third_party": [], "unreachable": ["B4", "B5"], "title_only": [s[0] for s in SOURCES if s[7]],
 "wikipedia_state": "article 'On the Sublime' (rendered HTTP 200 and raw wikitext HTTP 200, 2026-11-17), revision 1385253389, last edited 12 November 2026; it is a card of T (B1, in B_D). 'Longinus (literature)' redirects to it ({{R from move}}; B9, in B_R)",
 "own_pages_note": "the treatise's own text: Roberts's Greek of 1907 at Perseus (B8, chapter 10, read); the English at Wikisource is Havell's of 1890 (B10, index page read; chapter pages not reached); Project Gutenberg (B5, a card) refused with HTTP 503 (maintenance)",
 "pools": pools, "sources": field_sources}
row_out["status"]["ledger"] = (f"unaudited (§3.8: one extractor per ledger); field quotes {sum(c['quote_ok'] for c in field_claims.values())}/{len(field_claims)} verified by script against saved text or the paste; "
                               f"archive quotes {sum(c['quote_ok'] for c in arch)}/{len(arch)} verified against the deposit texts and the registry (intake scripts/build_row.py; counts in verification.json)")
row_out["composition_v09"] = json.loads(json.dumps(row_out["composition"]))
(V2 / "rows" / f"{ROW}.json").write_text(json.dumps(row_out, ensure_ascii=False, indent=1), encoding="utf-8")

out = {"field_total": f"{sum(c['quote_ok'] for c in field_claims.values())}/{len(field_claims)}",
       "field_by_source": dict(collections.Counter(c["source"] for c in field_claims.values() if c["quote_ok"])),
       "archive_deposits_total": f"{sum(c['quote_ok'] for c in arch if c['dep']!='capture-registry')}/{sum(1 for c in arch if c['dep']!='capture-registry')}",
       "archive_cap_total": f"{sum(c['quote_ok'] for c in arch if c['dep']=='capture-registry')}/{sum(1 for c in arch if c['dep']=='capture-registry')}",
       "T_claims_in_paste": f"{len(T_CLAIMS)-len(t_fail)}/{len(T_CLAIMS)}", "fails": fails, "t_fail": t_fail,
       "unknown_claim_ids": unknown, "p_unknown": p_unknown, "ledger_claims_not_in_KO": not_in_ko, "kernels_off_rail": kernels_off_rail,
       "translation_missing": tr_missing, "translation_dupes": tr_dupes, "prose_flags": prose_flags, "move_gaps": move_gaps,
       "ko_sentences": len(ko), "ko_b_sentences": len(kob), "p_body_words": pw, "p_b_body_words": pbw,
       "measure": row_out["measure"]["v0.10"], "blocks": {k: row_out["measure"]["blocks"][k] for k in ("sequence", "field_only_head", "archive_only_tail", "breach")},
       "ko1_max_sim": round(ko1_max, 3), "pool_counts": dict(cnt)}
(INTAKE / "verification.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1))
