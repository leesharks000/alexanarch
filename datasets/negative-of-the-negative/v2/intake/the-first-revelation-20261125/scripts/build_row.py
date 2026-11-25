"""Build the /non row the-first-revelation (2026-11-25) from claims.py, compose.py and frame.py: the two ledgers, the
traversal reading, the row, and verification.json. Every quote is checked against its saved text.
After the longinus-on-the-sublime row's build_row.py.
   /home/claude/shim/python3 -I build_row.py"""
import json, re, hashlib, difflib, collections, sys, pathlib
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from vlib import *
from claims import *
from compose import *

ROW = "the-first-revelation"
V2 = ROOT / "datasets/negative-of-the-negative/v2"
INR = IN
REGD = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
FR = json.loads((INTAKE / "sources/fetch-records.json").read_text(encoding="utf-8"))
paste = (ROOT / PASTE).read_text(encoding="utf-8")
t1 = (ROOT / T1F).read_text(encoding="utf-8")
t2 = (ROOT / T2F).read_text(encoding="utf-8")
e1 = nonreg_entry(SLUG_1); e2 = entry(SLUG_2)
COMPOSER = "Claude (Opus 5.5), subagent, 2026-11-25"
cap_url = lambda s: f"https://www.alexanarch.org/captures/{s}/"
rec_url = lambda n: f"https://www.alexanarch.org/s/records/{n}/"
fails = []
def sha(b): return hashlib.sha256(b).hexdigest()
def manifest(path):
    m = (ROOT / path).parent.parent / "MANIFEST.sha256"
    for line in m.read_text(encoding="utf-8").splitlines():
        h, f = line.split(None, 1)
        if f.lstrip("./") == "original/" + pathlib.Path(path).name: return h
    return None

# ---------------- field ledger ----------------
src = {s[0]: s for s in SOURCES}
field_sources = []
for (sid, origin, pool, card, kind, files, fids, title_only, role, hay) in SOURCES:
    fl = {}
    for f in files:
        p = f if hay == "seat" else INR + "sources/" + f
        h = sha((ROOT / p).read_bytes())
        fl[f.split("/")[-1]] = {"path": p, "sha256": h}
        if hay == "seat":
            fl[f.split("/")[-1]]["manifest_sha256"] = manifest(f); fl[f.split("/")[-1]]["manifest_match"] = (manifest(f) == h)
    tried = []
    for fid in fids:
        r = FR[fid]
        tried.append({"url": r["url"], "at": r["at"], "http": r["http"], "final_url": r["final_url"], "agent": r["agent"],
                      "raw_sha256": r["raw_sha256"], "bytes": r["bytes"],
                      "result": ("read: HTTP 200, saved as text (raw not kept); raw sha256 recorded" if r["http"] == 200 else
                                 f"unreachable: HTTP {r['http']}; one request with the row's agent string, no retry by another route")
                      + (f"; {r.get('body_head','')[:120]}" if r.get("body_head") else "")})
    if sid == "B6":
        tried.append({"search": ["WebSearch 'Britannica \"At what age did Muhammad receive his first revelation according to Islamic tradition\"' (2026-11-25)",
                                 "WebSearch 'britannica.com question \"first revelation\" Muhammad age \"Created from Britannica articles using AI\"' (2026-11-25)"],
                      "result": "no page under the title found; the card snippet stands as its text"})
    if sid == "B8":
        tried.append({"search": ["WebSearch 'KPU Pressbooks \"An Account of the First Revelation to the Prophet\" Niall Christie' (2026-11-25)"],
                      "result": "the page found by title at kpu.pressbooks.pub/ancientandmedievalworld/chapter/the-beliefs-of-islam/; the fetch refused (HTTP 403)"})
    if sid == "B9":
        tried.append({"search": ["WebSearch 'إسلام أون لاين بدء الوحي غار حراء اقرأ' (2026-11-25)"],
                      "result": "several Arabic pages of the site on the beginning of revelation; none identifiable as the chip's page (the chip's target is not in the paste); not fetched"})
    if hay == "seat":
        tried.append({"seat": files[0], "result": "read from the archive's seat; sha256 checked against the seat's MANIFEST.sha256"})
    ent = {"id": sid, "origin": origin, "pool": pool, "card": card, "kind": kind, "role": role, "files": fl,
           "fetched": {"tried": tried} if tried else {"tried": [], "note": "title only; not fetched (no target in the paste)"},
           "title_only": title_only, "url": (FR[fids[0]]["url"] if fids else None),
           "surfaced_by_T": ([{"slug": SLUG_1, "card": sid}] if sid in ("B1", "B2", "B3", "B4", "B5", "B6", "B7") else []) +
                            ([{"slug": SLUG_2, "card": sid}] if sid in ("B1", "B8", "B9", "B10") else []),
           "names_operator": "no" if (files and hay != "seat") else ("not applicable (a seated original)" if hay == "seat" else "unread"),
           "names_archive": "no" if (files and hay != "seat") else ("not applicable (a seated original)" if hay == "seat" else "unread")}
    if sid in ("B3", "B4"): ent["also_origin"] = "body_named"
    if sid == "B1": ent["revision"] = {"oldid": 1377806243, "last_edited": "2026-10-01T05:24Z"}; ent["also_surfaced_by"] = "T2 chip 'Wikipedia +1'"
    field_sources.append(ent)

def hay_of(S):
    h = S[9]
    if h == "files": return "\n".join((INTAKE / "sources" / f).read_text(encoding="utf-8") for f in S[5])
    if h == "T1": return paste
    if h == "T2": return t2
    if h == "seat": return seat_text(S[5][0])
    if h == "fetch404": return "\n".join(FR[i].get("body_head", "") for i in S[6])
field_claims = {}
for (fid, s, locus, q, claim, mod, kind, kern, const, lin, date) in FIELD:
    S = src[s]
    ok = found(q, hay_of(S))
    if not ok: fails.append(("field", fid))
    chk = {"files": f"saved text of {s} under {INR}sources/, whitespace-normalised; multi-part quotes joined by ' … ', each part checked",
           "T1": "the paste (title and snippet as pasted), " + PASTE, "T2": "the T2 transcript (chip or title as pasted), " + T2F,
           "seat": f"the seated original {(S[5] or ['?'])[0]} (OpenITI '~~' wraps joined; whitespace-normalised)",
           "fetch404": "the 404 bodies recorded in sources/fetch-records.json"}[S[9]]
    field_claims[fid] = {"source": s, "locus": locus, "quote": q, "claim": claim, "modality": mod, "kind": kind,
                         "kernel": kern, "const": const, "lineage": lin, "date": date, "quote_ok": ok,
                         "origin": S[1], "pool": S[2], "checked_against": chk}
    if S[7]: field_claims[fid]["title_only"] = True
pools = {"B_D": [s[0] for s in SOURCES if s[2] == "B_D"], "B_R": [s[0] for s in SOURCES if s[2] == "B_R"]}
FIELD_LEDGER = {
 "row": ROW, "address": "the first revelation", "addresses": ["the first revelation", "revelation first"], "extracted": "2026-11-25",
 "extractor": COMPOSER + ", one extractor (unaudited, §3.8)",
 "rule": "v0.10 §3.5, source-neutral: opening or abstract, defined terms, headline claims, stated limits; quotes verbatim from the saved page texts, the transcripts or the seated originals (whitespace-normalised for the check; multi-part quotes joined by ' … ', each part checked); title-only cards quoted by their title or chip as pasted",
 "B_note": "The field in two pools (v0.10 §0.3, §3.1(a)). B_D: T1's rail and body cards (B1 Wikipedia, B2 IslamOnline, B3 Quran.com, B4 IIUM, B5 Lumen Learning, B6 Britannica, B7 the videos) and T2's chips and videos (B1 Wikipedia again, carried once; B8 KPU Pressbooks; B9 the Arabic IslamOnline chip; B10 the videos). B_R: Wikipedia's absence under 'First revelation' (B11) and the seated originals (B12 the Qur'an; B13 al-Bukhārī; B14 al-Kāfī). The sources behind T2's '+N' counts are not in the paste.",
 "lineage_note": "Lineages (§3.6): what it is; the account; readings of the account; the verses; its date; the pause and after; how revelation came; unread and composed cards.",
 "pages": f"saved text files under {INR}sources/ (text only, scripts and styles stripped; raw responses not kept, their sha256 in sources/fetch-records.json); seated originals read in place",
 "field": field_sources, "field_claims": field_claims, "field_sources": {s[0]: s[3] for s in SOURCES}, "pools": pools}

# ---------------- archive ledger ----------------
arch = []
for (aid, dep, locus, q, claim, kind, mod, strata, kern, lin) in ARCH:
    d = REGD[dep]; f = d["full_text_path"].lstrip("/")
    ok = found(strip_md(q), deposit_text(f))
    if not ok: fails.append(("archive", aid))
    creator = d.get("creator") or d.get("creators")
    if isinstance(creator, list): creator = "; ".join(c if isinstance(c, str) else c.get("name", "") for c in creator)
    arch.append({"id": aid, "dep": dep, "axn": d.get("axn"), "claim": claim, "kind": kind, "modality": mod, "strata": strata,
                 "locus": locus, "quote": q, "kernel": kern, "const": False, "lineage": lin, "date": d.get("date"),
                 "title": d.get("title"), "creator": creator, "file": f, "record": {"url": rec_url(dep), "label": f"#{dep}"},
                 "quote_ok": ok, "quote_check": "within the deposit text as loaded (whitespace-normalised; markdown emphasis stripped)"})
for (cid, reg, slug, fld, q, claim, kind, mod, kern, lin) in CAP:
    if reg == "nonreg":
        ok = found(q, nonreg_text(slug)); e = e1
        title = f"/non register (datasets/negative-of-the-negative/v2/register.json), entry {slug} ({e['obs_id']})"; file = "datasets/negative-of-the-negative/v2/register.json"
        url = "https://www.alexanarch.org/non/the-first-revelation/"
        chk = "within the register entry's archive_basis, notes, transcript_complete, surface_basis, auth_basis and sf fields as loaded (whitespace-normalised)"
    else:
        ok = found(q, entry_text(slug)); e = e2
        title = f"Capture Registry (EA-WG-CAPTURES-01), entry {slug} ({e['obs_id']}, {e['axn']})"; file = "data/EA-WG-CAPTURES-01.json"
        url = cap_url(slug)
        chk = "within the entry's reading, analysis, findings, d, per_note, per_dim basis and notes fields as loaded (whitespace-normalised)"
    if not ok: fails.append(("cap", cid))
    arch.append({"id": cid, "dep": "capture-registry" if reg == "capreg" else "non-register", "record": {"url": url, "label": "CAP"}, "surface": {"url": url},
                 "claim": claim, "kind": kind, "modality": mod, "strata": ["D"], "locus": f"{slug}, {fld}", "quote": q,
                 "kernel": kern, "const": False, "lineage": lin, "date": e["date"], "title": title,
                 "creator": "Lee Sharks (the registry)" if reg == "capreg" else "Lee Sharks (the /non register)", "file": file, "quote_ok": ok, "quote_check": chk})
AIDS = {c["id"]: c for c in arch}

# ---------------- KO and its plan ----------------
ids = set(field_claims) | set(AIDS)
def typ(cl):
    f = any(c in field_claims for c in cl); a = any(c in AIDS for c in cl)
    return "M" if f and a else ("F" if f else "A")
ko = [{"n": i + 1, "para": s, "sense": SENSES[s], "text": t, "claims": cl} for i, (s, t, cl) in enumerate(KO)]
kob = [{"n": i + 1, "para": s, "text": t, "claims": cl} for i, (s, t, cl) in enumerate(KO_B)]
ko_c = [c for s in ko for c in s["claims"]]
unknown = sorted(set(ko_c) - ids) + sorted({c for s in kob for c in s["claims"]} - set(field_claims))
not_in_ko = sorted(ids - set(ko_c))
senses = collections.OrderedDict((n, [s["n"] for s in ko if s["sense"] == n]) for n in SENSES)

def unquoted(t): return re.sub(r'"[^"]*"|“[^”]*”', '', t)
prose_flags = []
for s in ko + kob:
    u = unquoted(s["text"])
    for pat in (r"\brather than\b", r"\binstead of\b", r"\bnot\b[^.;:]{0,60}\bbut\b", r", not\b"):
        if re.search(pat, u, re.I): prose_flags.append((s["n"], pat))

def sim(a, b): return difflib.SequenceMatcher(None, a, b).ratio()
best = []
for b in kob:
    best.append(max(((sim(b["text"], k["text"]), k["n"]) for k in ko), key=lambda x: x[0]))
surv = [(i + 1, n) for i, (r, n) in enumerate(best) if r >= 0.95]
seq = "".join(typ(s["claims"]) for s in ko)
head = len(seq) - len(seq.lstrip("F")); tail = len(seq) - len(seq.rstrip("A"))
ko1_max = max(sim(ko[0]["text"], b["text"]) for b in kob)

WRE = r"[A-Za-z0-9'’-]+"
def wc(t): return len(re.findall(WRE, t))
def body_words(p): return wc(p["lede"][0]) + sum(wc(l) + wc(t) for (_, _, items) in p["sections"] for (l, t, _) in items)
pw = body_words(P); pbw = body_words(P_B)

def mkP(p, title, extra):
    return {"title": title, **extra, "lede": {"text": "The First Revelation " + p["lede"][0], "claims": p["lede"][1]},
            "sections": [{"icon": i, "head": h, "items": [{"label": l, "text": t, "claims": c} for (l, t, c) in items]} for (i, h, items) in p["sections"]],
            "open": [{"question": q, "rests_on": r, "modality": m, "would_resolve": w} for (q, r, m, w) in p["open"]]}

lin_claims = collections.OrderedDict()
for fid, c in field_claims.items(): lin_claims.setdefault(c["lineage"], []).append(fid)
for c in arch: lin_claims.setdefault(c["lineage"], []).append(c["id"])
def earliest(cl):
    fs = [c for c in cl if c in field_claims]
    if fs: return field_claims[fs[0]]["source"]
    deps = [(AIDS[c]["date"] or "9999", AIDS[c]["dep"]) for c in cl if isinstance(AIDS[c]["dep"], int)]
    if deps: return min(deps)[1]
    return "Capture Registry"
rail = [{"lineage": l, "claims": cl, "earliest": earliest(cl)} for l, cl in lin_claims.items()]
rail_B = [r for r in rail if all(c in field_claims for c in r["claims"])]
rail_c = {c for r in rail for c in r["claims"]}
kernels_off_rail = sorted([k for k, c in field_claims.items() if c["kernel"] and k not in rail_c] + [c["id"] for c in arch if c["kernel"] and c["id"] not in rail_c])
p_ids = set(P["lede"][1]) | {c for (_, _, it) in P["sections"] for (_, _, cl) in it for c in cl} | {c for (_, r, _, _) in P["open"] for c in r}
p_unknown = sorted(p_ids - ids)
p_missing = sorted(ids - p_ids)

tr_rows = []; seen = collections.Counter()
for (lin, fcs, acs) in TRANSLATION:
    for f in fcs: seen[f] += 1
    rec = "; ".join(f"{f} ({field_claims[f]['source']}, {field_claims[f]['locus']}): \"{field_claims[f]['quote']}\"" for f in fcs)
    tr_rows.append({"lineage": lin, "field_claims": fcs, "received": rec, "receiving_text": "—",
                    "translation": "untranslated: composed as received beside " + ", ".join(acs), "archive_claims": acs})
tr_missing = sorted(set(field_claims) - set(seen)); tr_dupes = sorted(k for k, v in seen.items() if v > 1)
tr_unknown = sorted({a for (_, _, acs) in TRANSLATION for a in acs} - set(AIDS))

def body_after(t, marker):
    return t.split(marker, 1)[1] if marker in t else t
t1_words = wc(t1.split("\n", 1)[1]); t2_words = wc(body_after(t2, "AI Overview").split("Bible Gateway", 1)[0])
t1_sha = sha(t1.encode("utf-8")); t2_sha = sha(t2.encode("utf-8"))
tc1 = [f"{tid} {kind}: '{q}' ({card})" for (tid, kind, q, card) in T_CLAIMS_1]
tc2 = [f"{tid} {kind}: '{q}' ({card})" for (tid, kind, q, card) in T_CLAIMS_2]
t_fail = [tid for (tid, _, q, _) in T_CLAIMS_1 if not found(q, paste)] + [tid for (tid, _, q, _) in T_CLAIMS_2 if not found(q, t2)]
rail1 = [{"n": c["n"], "site": c["site"], "title": c.get("title"), "snip": c.get("snip")} for c in e1["cite_list"]]
rail2 = [{"n": c["n"], "site": c["site"], "title": c.get("title"), "snip": c.get("snip"), "note": c.get("note")} for c in e2["cite_list"]]

moves = []; span_fail = []
for (mv, span, mtype, ans, p_at) in MOVES:
    if not (found(span, paste) or found(span, t2)): span_fail.append(mv)
    ko_at = [s["n"] for s in ko if set(s["claims"]) & set(ans)]
    p_lab = [it["label"] for sec in P["sections"] for it in [{"label": l, "claims": c} for (l, _, c) in sec[2]] if set(it["claims"]) & set(ans)]
    moves.append({"move": mv, "span": span, "type": mtype, "answered_by": ans, "ko": ko_at, "p": sorted(set(p_at) | set(p_lab))})
move_gaps = [m["move"] for m in moves if not m["ko"] or not m["p"]]

kernel = []
for i, (cid, sense, contrast, f, qual) in enumerate(KERNEL):
    c = field_claims.get(cid) or AIDS[cid]
    srcname = (f"#{c['dep']}" if isinstance(c.get("dep"), int) else ("Capture Registry" if c.get("dep") == "capture-registry" else "/non register")) if cid in AIDS else c["source"]
    kernel.append({"K": f"K{i+1}", "claim": f"`{cid}`", "source": srcname, "M_src": c["modality"], "sense": sense, "qualifiers carried": qual,
                   "f (source's own falsifiers)": (", ".join(f) if f else "— (none stated; watch: a later composition at the address that states or drops the claim, attributed or not, uptake §8.3)"),
                   "contrast": contrast,
                   "resolver": "a later capture at 'the first revelation' (ADDR-636485941bef) or at 'revelation first' (ADDR-045f1f77fcb4) on Google AI Overview, seated in the /non register or the Capture Registry (§8.3)"})

# ---------------- reading.json ----------------
TR = V2 / "traversal" / ROW
cand = {k: [json.loads(l) for l in open(TR / f"candidates-{k}.jsonl", encoding="utf-8")] for k in "DROH"}
admitted = {1811: (["D", "R", "O"], "Revelation First ≠ The First Revelation (EA-MPAI-REVFIRST-02 v1.0): §1.2 defines the event (entity_name, place, date, text, primary witnesses; the definition from the Qur'an and the report from ʿĀʾisha; what 'first' means; the packet's limit); §0 and the canary sentence (the name's grammar; the report's own order); §1.4 and §2 (the directional distinction; usage, method, radical); §3.1 and §5 (the composition at the reversed words and its sources); §6, §7, §10, §12, §14, §18 (the matrix row, the identity rule's event markers, no path, the aliases, no authority over the event). R: the event related to the archive's thesis Revelation First and to the archive's Capture Registry; O-direct: the archive's operators (directional propositional erasure, cross-domain referent substitution) applied to the composition of the event at the reversed words, by the archive itself (§4)")}
reasons_reject = {832: "'The archive is the first Revelation reception project…': 'first' qualifies a reception project of the Book of Revelation; another sense of the words, no claim on the event",
                  1211: "the same sentence (an instance of the Revelation work plan line)", 1216: "the same sentence", 1217: "the same sentence (EA-LOGOS-REVFIRST-PLAN v7.3)", 1400: "the same sentence"}
verdicts = [{"dep": 1811, "strata": admitted[1811][0], "reason": admitted[1811][1], "claims": [c["id"] for c in arch if c["dep"] == 1811],
             "candidates": [x["cand_id"] for k in "DRO" for x in cand[k] if x["dep"] == 1811], "lineage_instances": []}]
not_admitted = []
for k in "DRO":
    for x in cand[k]:
        if x["dep"] == 1811: continue
        not_admitted.append({"dep": x["dep"], "cand": x["cand_id"], "stratum": k, "reason": reasons_reject.get(x["dep"], "read: no claim on the event of the stratum's kind")})
hop_reason = {1531: "EA-CORPORA-02: the seat record of the Qur'an (02/08); no sentence says anything of the event; its seated text is B_R (B12), per the brief",
              1706: "EA-CORPORA-23: the seat record of the hadith; no sentence says anything of the event; its seated texts are B_R (B13, B14), per the brief",
              1757: "The Historical Logos: 'The Qur'an is not a book. It is the Uthmanic recension, c. 650 CE.' (a finding on the Qur'an's text); no claim on the event",
              1758: "In the Midst of the Seven: names Muhammad son of ʿAbdallah in a Mandaean colophon; no claim on the event"}
hop_rej = [{"cand": x["cand_id"], "dep": x["dep"], "direction": x["direction"], "via": x["via_admitted"],
            "verdict": "rejected: " + hop_reason.get(x["dep"], "term-absent hop candidate read for the event (Qur'an, Islam, Muhammad, Hira, Gabriel, hadith, Bukhari, Mecca searched in its text: no occurrence); it bears on the Revelation First thesis, the MPAI and SPXI instruments or other entities, and says nothing of the event")}
           for x in cand["H"]]
READING = {
 "row": ROW, "pass": f"2026-11-25: first reading of D, R and O candidates ({len(cand['D'])} D sentences in {len({x['dep'] for x in cand['D']})} deposits, {len(cand['R'])} R in {len({x['dep'] for x in cand['R']})}, {len(cand['O'])} O-direct in {len({x['dep'] for x in cand['O']})}); one citation hop forward and back from #1811 ({len(cand['H'])} candidates)",
 "procedure": "EA-NEGONT-02 v0.10 §3.4 D/R/O (working; not frozen). D where a deposit names the event and says something of it; R where it relates the event to an archive object (the thesis Revelation First; the Capture Registry); O-direct where the archive applies its own categories to the composition of the event (#1811 §4). No O-class: the field sources the event as an event of Islamic tradition (B1, B3) and no archive category is applied to that class at a locus.",
 "reader": COMPOSER, "config": f"datasets/negative-of-the-negative/v2/traversal/{ROW}/config.json",
 "verdicts": verdicts, "not_admitted": not_admitted, "rejected": not_admitted,
 "hop": {"from": [1811], "candidates": len(cand["H"]), "admitted": [], "rejected": hop_rej},
 "lineages": [{"lineage": "what it is", "instances": [1811], "earliest": 1811}, {"lineage": "its name", "instances": [1811], "earliest": 1811},
              {"lineage": "the archive's limit on the name", "instances": [1811], "earliest": 1811}, {"lineage": "the directional distinction", "instances": [1811], "earliest": 1811},
              {"lineage": "the record of its composition by machines", "instances": [1811], "earliest": 1811}],
 "observations": [
   "The archive names the event in one deposit, #1811 (25 November 2026), written in answer to the composition of the event at the reversed words; every D, R and O candidate in it was read, and its claims on the event are ledgered by locus (A1811-01 to A1811-38).",
   "The string 'first revelation' reaches a second sense in five deposits (#832, #1211, #1216, #1217, #1400): 'the first Revelation reception project', the archive's description of itself as a reception project of the Book of Revelation; set aside.",
   "The archive's seats of the Qur'an (#1531) and the hadith (#1706) are reached by the hop; their records say nothing of the event, and their seated texts enter the field as B_R (B12–B14), per the brief.",
   "No archive deposit before #1811 names the event; the thesis whose name reverses it is carried from #202 (2026-06-14), and its row is /non/revelation-first/."],
 "counts": {"D_candidates": len(cand["D"]), "D_deposits": len({x['dep'] for x in cand['D']}), "R_candidates": len(cand["R"]), "R_deposits": len({x['dep'] for x in cand['R']}),
            "O_candidates": len(cand["O"]), "O_deposits": len({x['dep'] for x in cand['O']}), "H_candidates": len(cand["H"]),
            "deposits_admitted": 1, "deposit_claims": sum(1 for c in arch if isinstance(c["dep"], int)),
            "CAP_claims": sum(1 for c in arch if not isinstance(c["dep"], int))},
 "records": {"CAP": sum(1 for c in arch if not isinstance(c["dep"], int)), "note": f"the archive's own records of the entity, ledgered beside the deposit: the /non register's entry {SLUG_1} (CAP-1-NN) and the Capture Registry's entry {SLUG_2} (CAP-2-NN)"},
}

LED = V2 / "ledgers" / ROW
(LED / "field.json").write_text(json.dumps(FIELD_LEDGER, ensure_ascii=False, indent=1), encoding="utf-8")
(LED / "ledger-archive.json").write_text(json.dumps(arch, ensure_ascii=False, indent=1), encoding="utf-8")
(TR / "reading.json").write_text(json.dumps(READING, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------- the row ----------------
def L_text(sents): return " ".join(s["text"] for s in sents)
cnt = collections.Counter(s[2] for s in SOURCES)
from frame import frame
counts = {"D": len(cand["D"]), "Dd": len({x['dep'] for x in cand['D']}), "R": len(cand["R"]), "Rd": len({x['dep'] for x in cand['R']}),
          "O": len(cand["O"]), "Od": len({x['dep'] for x in cand['O']}), "H": len(cand["H"])}
row_out = frame(e1, e2, field_claims, AIDS, counts)
for L in row_out["ontology"]["case"]["loci"]:
    if not found(strip_md(L["quote"]), deposit_text(REGD[L["dep"]]["full_text_path"].lstrip("/"))): fails.append(("case-locus", L["dep"], L["locus"]))
transcripts = [
 {"slug": SLUG_1, "address": "the first revelation", "addr_id": e1["addr_id"], "obs_id": e1["obs_id"], "axn": None, "register": "/non register",
  "sha256": t1_sha, "sha256_of": "the /non register's transcript string (datasets/negative-of-the-negative/v2/register.json, entries[slug].transcript), UTF-8; equals the entry's transcript_sha256",
  "words": t1_words, "cards": 10, "card_rail": rail1, "claims": tc1, "path": T1F,
  "pastes": [PASTE + " (sha256 " + sha(paste.encode('utf-8')) + "; equals the register's transcript_raw)"],
  "address_note": "the entity at its own address"},
 {"slug": SLUG_2, "address": "revelation first", "addr_id": e2["addr_id"], "obs_id": e2["obs_id"], "axn": e2["axn"], "register": "Capture Registry",
  "sha256": t2_sha, "sha256_of": "the Capture Registry's transcript string (data/EA-WG-CAPTURES-01.json, entries[slug].transcript), UTF-8; identical to rebuild/capture-registry/intake-20261125-revelation-first/paste-67f23a47.txt",
  "words": t2_words, "cards": 3, "card_rail": rail2, "claims": tc2, "path": T2F,
  "pastes": ["rebuild/capture-registry/intake-20261125-revelation-first/paste-67f23a47.txt (sha256 " + t2_sha + ")"],
  "address_note": "the entity composed whole at another's address (the thesis's string); the organic results beneath the Overview are outside the composition (the registry: the panel is not drawn from its page)"}]
row_out["objects"] = {
 "T": {"path": T1F, "sha256": t1_sha, "words": t1_words + t2_words, "cards": 13,
       "words_note": f"two transcripts of one composition (§2.3): T1 at 'the first revelation', {t1_words} words (the register's cleaned transcript, query line excluded), ten rail cards, two inline links, three body videos; T2 at 'revelation first', {t2_words} words (the Overview from its title to its videos; the results page's header and the organic page beneath excluded), three chips and three videos; summed",
       "claims": tc1 + tc2, "register": {"register": "datasets/negative-of-the-negative/v2/register.json", "slug": SLUG_1, "obs_id": e1["obs_id"]},
       "transcripts": transcripts},
 "KO": {"title": "The First Revelation", "genre": "knowledge object, equal case, under EA-NEGONT-02 v0.10 (#1726): the final article form of the entity (§4.13), natural sentences under descriptive subheadings (each sentence's sense), attribution beneath each sentence by claim id (§4.5); sources named in the prose only where the holder is part of what is said (the scholars' readings and reckonings, the field's two counts of the verses, the archive's limit and audit, the registers' findings)",
        "status": "composed 2026-11-25 under v0.10 on BRIEF-NEW-ROWS-FIRST-REVELATION.md (Row 1); not frozen", "sentences": ko,
        "joins": [
          {"act": "order of senses", "sentences": f"1–{len(ko)}", "claims": [], "note": "equal case (§4.7): what it is (¶0); the account (¶1); the verses (¶2); the date (¶3); the pause and what followed (¶4); how revelation came (¶5); the name and its reversed homonym (¶6); the record of its composition by machines (¶7). Field and archive claims ordered together by genealogy within each sense"},
          {"act": "holding rivals (the count of the verses)", "sentences": [17], "claims": ["F70", "F40", "F28", "F12", "F33"], "note": "three verses in the report (al-Bukhārī; IIUM; IslamOnline) beside five in Wikipedia and Quran.com, each with its holders (§4.4 P_coh)"},
          {"act": "holding rivals (the date)", "sentences": [18, 19, 20], "claims": ["F1", "F46", "F7", "F8", "F27", "F26"], "note": "610 and 609; 21 Ramadan and 13–14 December 610, each with its reckoner"},
          {"act": "holding rivals (the second revelation and the pause)", "sentences": [25], "claims": ["F19", "F20", "F49"], "note": "chapter 74 and chapter 68; three years (Lumen; Ibn Ishaq to public preaching)"},
          {"act": "holding the archive's audit beside the article as fetched", "sentences": [40], "claims": ["A1811-20", "F4", "F23"], "note": "#1811 §5's 'no hatnote' and no Laylat al-Qadr beside the section hatnote and the Commons label (§4.4 P_coh); neither made wrong at its date"},
          {"act": "the registry's reading and the packet's at their grade", "sentences": [36], "claims": ["CAP-2-03", "CAP-2-04", "A1811-17", "A1811-19"], "note": "'careful and orderly' is the registry's interpretation; the reading of the string as 'first revelation' is the packet's inference, stated as inferential"}],
        "plan": {"order": ko_c, "senses": senses, "marks": {"A1811-19": "inferential (the packet's own register)", "A1811-20": "contradicted in part by F4, F23 (the article as fetched): both carried"}, "conflicts": [], "cuts": []},
        "governing_question": "the brief's: the event's article as the field holds it, its dating disagreements as the field holds them, read by people inside the tradition at reference-work grain, with the archive's one limit on the name beside it at its grade; no judgment on the truth of revelation; mechanics, never motive"},
 "P": mkP(P, "The First Revelation", {"genre": "the compression: AIO's interaction grammar (lede, headed clusters, bolded labels, card rail), composed from the v0.10 plan in one claim space; it faces on the card",
                                      "status": "composed 2026-11-25 from the v0.10 knowledge object; not frozen"}),
 "P_B": mkP(P_B, "The First Revelation", {"arm": "B (the field alone)", "genre": "popup — the compression from the field ledger alone (B_D and B_R)", "status": "composed 2026-11-25 from the field ledger alone; not frozen"}),
 "KO_B": {"title": "The First Revelation", "arm": "B (the field alone)", "genre": "knowledge object", "status": "composed 2026-11-25 from the field ledger alone; not frozen", "sentences": kob},
 "L_B": {"words": wc(L_text(kob)), "text": L_text(kob), "note": "L_F(B), the field-only composition, realized as KO_B (objects.KO_B)"},
 "L_BA": {"words": wc(L_text(ko)), "text": L_text(ko),
          "rail": [{"Card": f"{s[0]} {s[3]}", "Snippet": (field_claims[[k for k, c in field_claims.items() if c['source'] == s[0]][0]]["quote"])[:200]} for s in SOURCES]
                  + [{"Card": "#1811 " + REGD[1811]["title"][:110], "Snippet": [c for c in arch if c['dep'] == 1811][0]["quote"][:200]}]
                  + [{"Card": "/non register — " + SLUG_1, "Snippet": AIDS["CAP-1-01"]["quote"][:200]},
                     {"Card": "Capture Registry — " + SLUG_2, "Snippet": AIDS["CAP-2-01"]["quote"][:200]},
                     {"Card": "Linked row — /non/revelation-first/", "Snippet": "Revelation First, Lee Sharks's thesis (#202): the reversed words, a distinct entity; no sameAs (#1811 §6)"},
                     {"Card": "Linked row — /non/book-of-revelation/", "Snippet": "the Book of Revelation, the work the reversed words' thesis concerns"}],
          "note": "L(B ∪ A) in the equal-terms case (§0.4), realized as the knowledge object (objects.KO); its rail is one card per source, grouped by the compression's lineages at render (§5.2); the two linked rows close the rail"},
}
row_out["objects"]["P"]["body_words"] = pw
row_out["objects"]["P"]["body_words_rule"] = "lede plus every item's label and text (regex [A-Za-z0-9'’-]+; the bound is 350, §4.8)"
row_out["objects"]["P"]["entity"] = f"Composed under v0.10, equal case (ρ = extends): KO_B sentences surviving {len(surv)} of {len(kob)}; every field claim carried."
row_out["objects"]["P"]["rail"] = rail
row_out["objects"]["P"]["cross_links"] = ["/non/revelation-first/", "/non/book-of-revelation/"]
row_out["objects"]["P_B"]["body_words"] = pbw
row_out["objects"]["P_B"]["rail"] = rail_B
row_out["objects"]["P_B"]["entity"] = "the field's entity: Muhammad's first revelation at the Cave of Hira, as Wikipedia, IslamOnline, Quran.com, IIUM, Lumen Learning and the seated originals give it"
row_out["field"] = [{"id": s["id"], "card": s["card"], "fetched": ("; ".join(f"{t.get('url', t.get('seat', 'search'))} {t.get('result','')}" for t in s["fetched"]["tried"])[:400] or s["fetched"].get("note")), "origin": s["origin"], "pool": s["pool"]} for s in field_sources]
row_out["field_claims"] = field_claims
row_out["field_sources"] = FIELD_LEDGER["field_sources"]
row_out["delta"]["correction"]["moves"] = moves
row_out["delta"]["correction"]["check"] = ("every move answered by a knowledge-object sentence and a compression line; no gap" if not move_gaps else f"gaps: {move_gaps}")
al = row_out["delta"]["alignment"]
al["T_composed"] = sorted(set(T1_COMPOSED), key=lambda x: int(x[1:])); al["T2_composed"] = sorted(set(T2_COMPOSED), key=lambda x: int(x[1:]))
al["T_composed_note"] = ("T1: F7 and F27 composed and assigned to 'Many Sunni traditions' (assigned to another); F4 at a coarse grain ('Laylat al-Qadr' from the hatnote 'Night of Power'); F12 composed in Wikipedia's English with '[clot]' added; F16 composed with its qualifier dropped ('a scholar of scripture'); F53–F59 as titles. "
                         "T2 (what of E_F it composes at another's address): the account and the dates from B1 (F1, F2, F7, F8, F9–F13, F15, F17), the Night of Power from the hatnote (F4), the chips and videos as titles; nothing of B2–B7, which are T1's")
al["T_not_composed"] = sorted([k for k, c in field_claims.items() if c["pool"] == "B_D" and k not in set(T1_COMPOSED) | set(T2_COMPOSED)], key=lambda x: int(x[1:]))
row_out["kernel"] = kernel
row_out["kernel_T"] = [{"claim": c, "note": n} for (c, n) in KERNEL_T]
row_out["ontology"]["translation"] = tr_rows
row_out["measure"] = {
 "rule": "v0.10 §4.10: KO_B sentences surviving in the KO at similarity ≥ 0.95, with positions (difflib.SequenceMatcher ratio, the best KO sentence for each KO_B sentence, as apply_v09.py does)",
 "v0.10": {"surviving": len(surv), "of": len(kob), "positions": [n if r >= 0.95 else None for (r, n) in best]},
 "opening_run": {"rule": "v0.10 §5.10 (equal-terms case): the field-only KO's sentences as the KO's opening run in their own order", "breach": bool(surv and surv[0] == (1, 1))},
 "blocks": {"rule": "v0.10 §4.1 (equal-terms case): the KO does not open with the field as a block or close with the archive as one; sentences typed by the ledgers of the claims they cite (F field-only, A archive-only, M both)",
            "sequence": seq, "field_only_head": head, "archive_only_tail": tail, "breach": head > 5 or tail > 12,
            "note": "the senses 'the name and its reversed homonym' and 'the record of its composition by machines' are the archive's and the registers' by nature (#1811, CAP), with the field's hatnote and Commons label beside the audit in the closing sentence"},
 "max_similarity": [round(r, 3) for (r, n) in best], "ko_sentence_1_max_similarity_to_KO_B": round(ko1_max, 3),
 "v0.9": {"surviving": len(surv), "of": len(kob), "positions": [n if r >= 0.95 else None for (r, n) in best]},
 "key_note": "the measure is computed under v0.10 (§4.10, unchanged from v0.9); the same values are carried under the key 'v0.9', which the page builder reads (scripts/build_non.py)"}
row_out["field_by_origin"] = {
 "cards": [s[0] for s in SOURCES if s[1] == "card"], "body_named": ["B3", "B4"], "own_pages": [s[0] for s in SOURCES if s[1] == "own_page"],
 "wikipedia": ["B1", "B11"], "census_third_party": [], "unreachable": ["B6", "B8"], "title_only": [s[0] for s in SOURCES if s[7]],
 "wikipedia_state": "article 'Muhammad's first revelation' (rendered HTTP 200 and raw wikitext HTTP 200, 2026-11-25), revision 1377806243, last edited 1 October 2026; a card of T1 and a chip of T2 (B1, in B_D); no top hatnote; section hatnote 'See also: Night of Power'; the titles 'First revelation' and 'The First Revelation' have no article (HTTP 404; B11, in B_R)",
 "own_pages_note": "the event's own texts, held by the archive's seats: the Qur'an (B12, Tanzil Uthmani v1.1), al-Bukhārī hadith 3 (B13), al-Kāfī on 27 Rajab (B14); each sha256 checked against its seat's MANIFEST.sha256",
 "pools": pools, "sources": field_sources}
row_out["status"]["ledger"] = (f"unaudited (§3.8: one extractor per ledger); field quotes {sum(c['quote_ok'] for c in field_claims.values())}/{len(field_claims)} verified by script against saved text, the transcripts or the seated originals; "
                               f"archive quotes {sum(c['quote_ok'] for c in arch)}/{len(arch)} verified against the deposit text, the Capture Registry and the /non register (intake scripts/build_row.py; counts in verification.json)")
row_out["homonym_names"] = row_out["homonyms"]["names"]
row_out["homonym_basis"] = row_out["homonyms"]["basis"].split(" The panel's")[0]
row_out["composition_v09"] = json.loads(json.dumps(row_out["composition"]))
(V2 / "rows" / f"{ROW}.json").write_text(json.dumps(row_out, ensure_ascii=False, indent=1), encoding="utf-8")

out = {"field_total": f"{sum(c['quote_ok'] for c in field_claims.values())}/{len(field_claims)}",
       "field_by_source": dict(collections.Counter(c["source"] for c in field_claims.values() if c["quote_ok"])),
       "archive_deposits_total": f"{sum(c['quote_ok'] for c in arch if isinstance(c['dep'], int))}/{sum(1 for c in arch if isinstance(c['dep'], int))}",
       "archive_cap_total": f"{sum(c['quote_ok'] for c in arch if not isinstance(c['dep'], int))}/{sum(1 for c in arch if not isinstance(c['dep'], int))}",
       "case_loci_total": f"{len(row_out['ontology']['case']['loci']) - len([f for f in fails if f[0]=='case-locus'])}/{len(row_out['ontology']['case']['loci'])}",
       "T_claims_in_transcripts": f"{len(T_CLAIMS_1)+len(T_CLAIMS_2)-len(t_fail)}/{len(T_CLAIMS_1)+len(T_CLAIMS_2)}", "move_spans_in_transcripts": f"{len(MOVES)-len(span_fail)}/{len(MOVES)}",
       "fails": fails, "t_fail": t_fail, "span_fail": span_fail,
       "unknown_claim_ids": unknown, "p_unknown": p_unknown, "ledger_claims_not_in_KO": not_in_ko, "ledger_claims_not_in_P": p_missing, "kernels_off_rail": kernels_off_rail,
       "translation_missing": tr_missing, "translation_dupes": tr_dupes, "translation_unknown": tr_unknown, "prose_flags": prose_flags, "move_gaps": move_gaps,
       "ko_sentences": len(ko), "ko_b_sentences": len(kob), "p_body_words": pw, "p_b_body_words": pbw,
       "measure": row_out["measure"]["v0.10"], "blocks": {k: row_out["measure"]["blocks"][k] for k in ("sequence", "field_only_head", "archive_only_tail", "breach")},
       "ko1_max_sim": round(ko1_max, 3), "pool_counts": dict(cnt), "seat_manifest_match": {s["id"]: [v.get("manifest_match") for v in s["files"].values()] for s in field_sources if s["origin"] == "own_page"}}
(INTAKE / "verification.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1))
