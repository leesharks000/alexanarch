"""Build the /non row revelation-first (2026-11-25) from claims.py, compose.py and frame.py: the two ledgers, the
traversal reading, the row, and verification.json. Every quote is checked against its saved text. After the
Longinus row's build_row.py.
   /home/claude/shim/python3 -I build_row.py"""
import json, re, hashlib, difflib, collections, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from vlib import *
from claims import *
from compose import *

ROW = "revelation-first"
V2 = ROOT / "datasets/negative-of-the-negative/v2"
INR = IN
REGD = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
FR = json.loads((INTAKE / "sources/fetch-records.json").read_text(encoding="utf-8"))
paste = (ROOT / PASTE).read_text(encoding="utf-8")
eT = entry(SLUG_T); eA = entry(SLUG_A); eC = entry(SLUG_C)
COMPOSER = "Claude (Opus 5.5), subagent, 2026-11-25"
cap_url = lambda s: f"https://www.alexanarch.org/captures/{s}/"
rec_url = lambda n: f"https://www.alexanarch.org/s/records/{n}/"
fails = []

def sha(b): return hashlib.sha256(b).hexdigest()
def hay_of(S):
    return "\n".join((ROOT / f).read_text(encoding="utf-8") if f.startswith("datasets/") else (INTAKE / "sources" / f).read_text(encoding="utf-8") for f in S[5])

# ---------------- field ledger ----------------
src = {s[0]: s for s in SOURCES}
field_sources = []
for (sid, origin, pool, card, kind, files, fids, title_only, role) in SOURCES:
    fl = {}
    for f in files:
        p = f if f.startswith("datasets/") else INR + "sources/" + f
        fl[f.split("/")[-1]] = {"path": p, "sha256": sha((ROOT / p).read_bytes())}
    tried = []
    for fid in fids:
        r = FR[fid]
        res = ("read: HTTP 200, saved as text (raw not kept); one request" if r["http"] == 200 else
               f"unreachable: HTTP {r['http']}; one request with the brief's agent string, no retry by another route")
        if fid == "BR-wikipedia-revelation-first-page-404body":
            res = "HTTP 404 (no article); a second request to the same URL to keep the 404 page's text, the first having kept its head only"
        if fid in ("BR-wikipedia-revelation-first-raw", "BR-wikipedia-revelation-first-page"):
            res = "HTTP 404: no article 'Revelation First' (the record of absence, §3.1(a))"
        if fid == "BR-wikipedia-search":
            res = "refused: HTTP 429 ('Too many requests'); recorded as unreachable and not retried by another route"
        if fid == "BR-rf-ladder":
            res = "unreachable: HTTP 404 (Vercel NOT_FOUND); the repository holds only the rung subpages; not retried by another route"
        tried.append({"url": r["url"], "at": r["at"], "http": r["http"], "final_url": r["final_url"], "agent": r["agent"],
                      "raw_sha256": r["raw_sha256"], "bytes": r["bytes"], "result": res + (f"; head: {r.get('body_head','')[:100]}" if r.get("body_head") else "")})
    surfaced = []
    if sid in ("B1", "B2", "B4", "B5"): surfaced = [{"slug": SLUG_C, "card": sid}]
    if sid == "B3": surfaced = [{"slug": SLUG_A, "card": sid}]
    if sid in ("B6", "B7", "B8"): surfaced = [{"slug": SLUG_T, "card": sid, "sense": "the homonym's (the First Revelation)"}]
    ent = {"id": sid, "origin": origin, "pool": pool, "card": card, "kind": kind, "role": role, "files": fl,
           "fetched": {"tried": tried} if tried else {"tried": [], "note": "title only; not fetched for this row (no target in the paste, or the homonym's card read in /non/the-first-revelation/)"},
           "title_only": title_only, "url": (FR[fids[0]]["url"] if fids else None), "surfaced_by": surfaced,
           "names_operator": ("yes" if sid in ("B1", "B2", "B3", "B9", "B10", "B11", "B12") else ("no" if sid == "B13" else "unread")),
           "names_archive": ("yes (the archive's own surface)" if sid in ("B1", "B2", "B3", "B9", "B10", "B11", "B12") else ("no" if sid == "B13" else "unread")),
           "archive_controlled": sid in ("B1", "B2", "B3", "B9", "B10", "B11", "B12", "B14")}
    if sid in ("B6", "B7", "B8"): ent["sense"] = "homonym: the First Revelation (/non/the-first-revelation/)"
    field_sources.append(ent)

field_claims = {}
for (fid, s, locus, q, claim, mod, kind, kern, const, lin, date) in FIELD:
    S = src[s]
    ok = found(q, hay_of(S))
    if not ok: fails.append(("field", fid))
    field_claims[fid] = {"source": s, "locus": locus, "quote": q, "claim": claim, "modality": mod, "kind": kind,
                         "kernel": kern, "const": const, "lineage": lin, "date": date, "quote_ok": ok,
                         "origin": S[1], "pool": S[2],
                         "checked_against": ("the transcript (title as pasted), " + ", ".join(S[5])) if S[7] else
                         f"saved text of {s} under {INR}sources/, whitespace-normalised; multi-part quotes joined by ' … ', each part checked"}
    if S[7]: field_claims[fid]["title_only"] = True
pools = {"B_D": [s[0] for s in SOURCES if s[2] == "B_D"], "B_R": [s[0] for s in SOURCES if s[2] == "B_R"]}
FIELD_LEDGER = {
 "row": ROW, "address": "revelation first", "addresses": ["revelation first", "What is the significance of alexanarch's revelation first programme?", "What is the Revelation First thesis?"], "extracted": "2026-11-25",
 "extractor": COMPOSER + ", one extractor (unaudited, §3.8)",
 "rule": "v0.10 §3.5, source-neutral: opening or abstract, defined terms, headline claims, stated limits; quotes verbatim from the saved page texts (whitespace-normalised for the check; multi-part quotes joined by ' … ', each part checked); title-only cards quoted by their title as pasted",
 "B_note": "The field in two pools (v0.10 §0.3, §3.1(a)). B_D: the cards of the entity's compositions at other addresses, the two field transcripts of 2026-11-13 (B1 revelationfirst.com, three chips and a link card; B2 alexanarch.org, a link card; B3 the Overview's two chips for www.alexanarch.org, fetched at #1217's record page, the organic result 1; B4, B5 image captions), and T's own chips (B6–B8, the homonym's). B_R: the site's own pages (B9–B11; B14 the ladder index, HTTP 404), the deposit the site names as its source (B12, #202's record), and Wikipedia's absence (B13). The sources behind the '+N' counts are not in the pastes.",
 "lineage_note": "Lineages (§3.6): what it is; first, not early; the claim ladder; absolute priority and the gate; corpus priority; generative priority; the conditional extensions; grade and falsifiers; its prehistory; its author and records; neighbours and the reversed words; its reception by machines; its reception by reference works; unread cards; the substitute's cards.",
 "pages": f"saved text files under {INR}sources/ (text only, scripts and styles stripped; raw responses not kept, their sha256 in sources/fetch-records.json)",
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
    if dep == 1217:
        c["instances"] = "the work plan in versions (§3.4 S4: grouped as one lineage and kept): #832 (v1.x), #1211, #1216, #1400 (superseded), #1403 (the v7.2 lacuna mark); the active text is #1217 (v7.3)"
    if aid in ("A1217-01", "A1217-02"): c["mark"] = "internally_inconsistent (§4.3): the ladder announces five claims (A1217-01) and lists six (A1217-02)"
    if aid in ("A1735-16", "A1735-17"): c["mark"] = "internally_inconsistent (§4.3): the census is counted at 'some seventy thousand units' in the abstract (A1735-16) and 'sixty thousand units' in §IX (A1735-17)"
    if aid == "A202-04": c["mark"] = "superseded_in_source's lineage: withdrawn as support for absolute priority by #1735 §II.3 (A1735-13), kept as a historical object by #1755 §7.12 (A1755-05)"
    arch.append(c)
for (cid, slug, fld, q, claim, kind, mod, kern, lin) in CAP:
    e = entry(slug)
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
unknown = sorted(set(ko_c + [c for s in kob for c in s["claims"]]) - ids)
not_in_ko = sorted(ids - set(ko_c))
kob_nonfield = sorted({c for s in kob for c in s["claims"]} - set(field_claims))
senses = collections.OrderedDict((n, [s["n"] for s in ko if s["sense"] == n]) for n in SENSES)

def unquoted(t): return re.sub(r'"[^"]*"|“[^”]*”', '', t)
prose_flags = []
_ptexts = [{"n": "P-lede", "text": P["lede"][0]}, {"n": "P_B-lede", "text": P_B["lede"][0]}] + [{"n": f"P:{l}", "text": t} for (_, _, it) in P["sections"] + P_B["sections"] for (l, t, _) in it] + [{"n": "P-open", "text": q + " " + w} for (q, _, _, w) in P["open"]]
for s in ko + kob + _ptexts:
    u = unquoted(s["text"])
    for pat in (r"\brather than\b", r"\binstead of\b", r"\bnot\b[^.;:]{0,60}\bbut\b", r", not\b"):
        if re.search(pat, u, re.I): prose_flags.append((s["n"], pat))

def sim(a, b): return difflib.SequenceMatcher(None, a, b).ratio()
best = []
for b in kob:
    m = max(((sim(b["text"], k["text"]), k["n"]) for k in ko), key=lambda x: x[0])
    best.append(m)
surv = [(i + 1, n) for i, (r, n) in enumerate(best) if r >= 0.95]
seq = "".join(typ(s["claims"]) for s in ko)
head = len(seq) - len(seq.lstrip("F")); tail = len(seq) - len(seq.rstrip("A"))
ko1_max = max(sim(ko[0]["text"], b["text"]) for b in kob)

WRE = r"[A-Za-z0-9'’-]+"
def wc(t): return len(re.findall(WRE, t))
def body_words(p): return wc(p["lede"][0]) + sum(wc(l) + wc(t) for (_, _, items) in p["sections"] for (l, t, _) in items)
pw = body_words(P); pbw = body_words(P_B)

def mkP(p, title, extra):
    return {"title": title, **extra, "lede": {"text": "Revelation First " + p["lede"][0], "claims": p["lede"][1]},
            "sections": [{"icon": i, "head": h, "items": [{"label": l, "text": t, "claims": c} for (l, t, c) in items]} for (i, h, items) in p["sections"]],
            "open": [{"question": q, "rests_on": r, "modality": m, "would_resolve": w} for (q, r, m, w) in p["open"]]}

lin_claims = collections.OrderedDict()
for fid, c in field_claims.items(): lin_claims.setdefault(c["lineage"], []).append(fid)
for c in arch: lin_claims.setdefault(c["lineage"], []).append(c["id"])
def earliest(cl):
    deps = [(AIDS[c]["date"] or "9999", AIDS[c]["dep"]) for c in cl if c in AIDS and AIDS[c]["dep"] != "capture-registry"]
    if deps: return min(deps)[1]
    fs = [c for c in cl if c in field_claims]
    if fs: return field_claims[fs[0]]["source"]
    return "Capture Registry"
rail = [{"lineage": l, "claims": cl, "earliest": earliest(cl)} for l, cl in lin_claims.items()]
rail_B = [{"lineage": r["lineage"], "claims": [c for c in r["claims"] if c in field_claims], "earliest": field_claims[[c for c in r["claims"] if c in field_claims][0]]["source"]}
          for r in rail if any(c in field_claims for c in r["claims"])]
rail_c = {c for r in rail for c in r["claims"]}
kernels_off_rail = sorted([k for k, c in field_claims.items() if c["kernel"] and k not in rail_c] + [c["id"] for c in arch if c["kernel"] and c["id"] not in rail_c])
p_ids = set(P["lede"][1]) | {c for (_, _, it) in P["sections"] for (_, _, cl) in it for c in cl} | {c for (_, r, _, _) in P["open"] for c in r}
p_unknown = sorted(p_ids - ids)
p_missing = sorted(ids - p_ids)

tr_rows = []; seen = collections.Counter()
for (lin, fcs, acs, rt, tr) in TRANSLATION:
    for f in fcs: seen[f] += 1
    rec = "; ".join(f"{f} ({field_claims[f]['source']}, {field_claims[f]['locus']}): \"{field_claims[f]['quote']}\"" for f in fcs)
    tr_rows.append({"lineage": lin, "field_claims": fcs, "received": rec, "receiving_text": rt, "translation": tr, "archive_claims": acs})
tr_missing = sorted(set(field_claims) - set(seen)); tr_dupes = sorted(k for k, v in seen.items() if v > 1)
tr_unknown = sorted({a for (_, _, acs, _, _) in TRANSLATION for a in acs} - ids)

# T and the field transcripts
def body_text(s):
    return s.split("[SYSTEM]", 1)[1] if "[SYSTEM]" in s else s
t_text = eT["transcript"]
ai = t_text.find("AI Overview\n"); t_words = wc(t_text[ai:])
t_sha = sha(t_text.encode("utf-8"))
t_claims = [f"{tid} {kind}: '{q}' ({card})" for (tid, kind, q, card) in T_CLAIMS]
t_fail = [tid for (tid, _, q, _) in T_CLAIMS if not found(q, paste)]
def rail_of(e): return [{"n": c.get("n"), "site": c.get("site"), "title": c.get("title"), "snip": c.get("snip"), "note": c.get("note")} for c in (e.get("cite_list") or [])]
def tr_entry(e, slug, i, role, address):
    s = e["transcript"]
    return {"slug": slug, "role": role, "address": address, "addr_id": e["addr_id"], "obs_id": e["obs_id"], "axn": e["axn"],
            "surface": e["surface"], "auth": e["auth"], "date": e["date"],
            "sha256": sha(s.encode("utf-8")), "sha256_of": "the registry's transcript string (data/EA-WG-CAPTURES-01.json, entries[slug].transcript), UTF-8",
            "words": wc(body_text(s)), "cards": len(e.get("cite_list") or []), "card_rail": rail_of(e), "path": INR + f"T{i}-{slug}.txt"}
TT = tr_entry(eT, SLUG_T, 1, "T, the erasure (spec §1.3)", "revelation first")
TT.update({"words": t_words, "claims": t_claims, "pastes": [INR + "paste-revelation-first-aio-20261125.txt (sha256 " + sha(paste.encode('utf-8')) + ", copied from rebuild/capture-registry/intake-20261125-revelation-first/paste-67f23a47.txt; identical to the registry's transcript string)"]})
TA = tr_entry(eA, SLUG_A, 2, "field transcript (the entity composed at another address)", eA["q"])
TC = tr_entry(eC, SLUG_C, 3, "field transcript (the entity composed at another address)", eC["q"])

moves = []
for (mv, span, mtype, ans, p_at) in MOVES:
    ko_at = [s["n"] for s in ko if set(s["claims"]) & set(ans)]
    moves.append({"move": mv, "span": span, "type": mtype, "answered_by": ans, "ko": ko_at, "p": p_at})
move_gaps = [m["move"] for m in moves if not m["ko"]]
move_unknown = sorted({a for (_, _, _, ans, _) in MOVES for a in ans} - ids)

kernel = []
for i, (cid, sense, contrast, f, qual) in enumerate(KERNEL):
    c = field_claims.get(cid) or AIDS[cid]
    kernel.append({"K": f"K{i+1}", "claim": f"`{cid}`", "source": ((f"#{c['dep']}" if c.get("dep") != "capture-registry" else "Capture Registry") if cid in AIDS else c["source"]),
                   "M_src": c["modality"], "sense": sense, "qualifiers carried": qual,
                   "f (source's own falsifiers)": (", ".join(f) if f else "— (none stated; watch: a later composition at the address that states or drops the claim, attributed or not, uptake §8.3)"),
                   "contrast": contrast,
                   "resolver": f"a later capture at 'revelation first' ({eT['addr_id']}) on Google AI Overview, signed out and incognito, seated in the Capture Registry (§8.3; #1811 §3's epochs at 30, 90 and 180 days)"})

# ---------------- reading.json ----------------
TR = V2 / "traversal" / ROW
cand = {k: ([json.loads(l) for l in open(TR / f"candidates-{k}.jsonl", encoding="utf-8")] if (TR / f"candidates-{k}.jsonl").exists() else []) for k in "DROH"}
admitted = {
 202: (["D"], "Revelation First ≠ Revelation Early, the seed (14 June 2026): The Argument, the claim ladder (Claims 2–4, 6), the midrashim transform and its distinction from Midrash, the falsifiers, What This Is Not, the retrieval-safe summary, the baseline sentence"),
 1217: (["D", "O"], "the work plan v7.3: head (status; the measured instance of machine-mediated theological reception, O-direct: the archive's category applied to the thesis), the claim ladder (five announced, six listed; the Josephus reading not required)"),
 1735: (["D"], "Literary Genealogy v9: §I (three claims, the prehistory, the novelty claim narrowed, the ancestry test), §II (early is not yet first; the gate; the priced hypothesis; the physical record), §IV.4 (the positive finding and its grades), §VIII (defeat conditions), §IX, the abstract's census count, the creator field"),
 1746: (["D"], "I Know You Are, But What Am I?: the abstract's four powers and finding, Hitzig 1843, the composition target (the synoptic problem undecided)"),
 1755: (["D"], "the framework hologram v1.4: §0 (the framework, the ladder, the symmetric evaluation), How to read it (INV-1), §6 (eighteen site claims undated), §7.12 (the claim status, the correction of the papyri, the Josephus bound), §7.14 (the object of the kernel), §7.16 (the author's statement of 9 November), head (WS-7)"),
 1810: (["D", "O"], "How Much You Wanna Bet?: §0.1 (the question), §0.4 (the recovery as restoration, O-direct: the Value Field applied to the thesis's recovery), §0.6 (no price, no probability)"),
 1811: (["D", "O"], "Revelation First ≠ The First Revelation: the canonical claim, the SPXI packet (finding, operators, open seams, falsifiers; O-direct: directional propositional erasure and cross-domain referent substitution applied to the capture), §§1.1–1.3, §3.1's correction, §6, §9, Appendix A"),
 542: (["O"], "TANG (9 March 2026), §IX.1 and §V: the thesis as the inaugural axial thesis, graded AXIAL_CONTESTED (O-direct: the archive's status algebra applied to the thesis); admitted outside the string pass, the deposit stating the thesis without the name 'Revelation First'"),
 639: (["D"], "the Shark Ark source compression (April 2026): the earliest dated state of the claim, 'not the final book of the NT but its first'"),
 407: (["D"], "the Revelation Room (January 2026): the sequence with its dates, the earliest dated chronology"),
 830: (["D"], "the pre-seeding baseline (14 June 2026): the empty basin, 'first' corrected to 'last'"),
 1737: (["D"], "The Portents Before the Fall: 66 CE held as the working date, provisionally"),
 1741: (["D"], "Secondary Source: §0.2 (the reception that made the source derivative), §0.4 (what the study does not decide)"),
 1747: (["D"], "Revelation = Q: the grade against Q's eight requirements"),
 1415: (["D"], "The James Derivation: the executable case from the Smyrna letter"),
 1766: (["D"], "Critique of Pure Inference §6.2.3, the thesis tamed: priority flattened into dating; the familiar slot"),
 881: (["D"], "Surface Visibility Baseline (22 June 2026) §3.7: the exact thesis intact on Medium"),
 1032: (["D"], "revelationfirst.com's own deposit: the site and its tracker held in its repository"),
 1684: (["D"], "the Prediction Index: Revelation First among the most restated claims (32 statements)"),
}
instances = {832: 1217, 1211: 1217, 1216: 1217, 1400: 1217, 1403: 1217, 1025: 202, 847: 1032, 56: 639, 969: 639, 970: 639, 971: 639, 1101: 639,
             1249: 860, 1231: 860, 1483: 1484, 1764: 1765, 1796: 1798, 1797: 1798, 1678: 1680, 1725: 1729, 1728: 1729, 1790: 1791, 880: 884, 882: 884, 1213: 1226, 203: 1226}
site_list = {985, 986, 1002, 1005, 1012, 1208, 1359, 1377, 1384, 1386, 1392, 1395, 1413, 1419, 1083, 1116, 1220, 1433, 1448, 870, 871}
reasons_reject = {
 636: "the Space Ark (April 2026): 'He wrote Revelation first … under the heteronym \"John\"' restates the April state (Josephus as author), carried by #639 and the claim status of #1755 §7.12 (S4)",
 1226: "the Josephus thesis disambiguation: names the work plan in a reference table; the Josephus bound is carried by #1217 and #1755 §7.12",
 837: "the Josephus Thesis ≠ the Jesus Myth MPAI: names the work plan as the thesis's extension; the distinction is carried by the site (F18) and #1755",
 204: "the SPXI self-audit protocol: uses the thesis as its example of provenance erasure ('\"Revelation early\" instead of \"Revelation first\" is provenance erasure'); the lineage of #202's retrieval-safe summary (S4)",
 828: "The Inscription That Survives: the inscription chain, which 'the Revelation First hypothesis strengthens'; a relation of another argument to the thesis, carried as the site's research track 3 (B1), no claim of the thesis's own",
 1414: "The Algorithmic Kernel (WS-4 demonstration 1): the transform's surface; the executed case is carried by #1415 and #1735 §VII",
 1416: "The Seven Unfoldings: per-letter derivations; the arrow programme is carried by #1735 and #1755 §7.11",
 1418: "The Four Derivations: worked derivations; carried as above",
 861: "The Second Crucifixion: coordinates with the work plan's WS-5; a further study, no claim on the thesis's definition",
 1758: "In the Midst of the Seven: folded into #1735 v9 (the commission, the figure in the midst); carried through #1735",
 1484: "the Ω erratum: the Sappho chain 'survives on conventional dating and tightens on the program's'; the boundary is the Tenth Muse's, carried by #1755 §3",
 1756: "the Tenth Muse hologram: the boundary with Revelation First, carried by #1755 §3",
 1757: "the Historical Logos hologram: the joins, carried by #1755",
 1759: "The Josephus Thesis: The Custody of the Name: rung V held as highly likely and not yet advanced, the lineage of #1755 §7.16 (S4)",
 1760: "EA-CORPORA-37, the Slavonic Josephus seating: seat records naming the research",
 1765: "The Word That Became Text: holds the Josephus thesis as #1217 and #1755 do; lineage (S4)",
 1798: "Either Forgery or Fact: the 'Revelation-first hypothesis' as #1735 and #1755 state it; lineage (S4)",
 1802: "Who Benefits from Bad Inference?: names the thesis among the archive's examples; no claim of its own on the thesis",
 1795: "Why I Believe in Hell: names #1755 and #1735 in its related records",
 1791: "A Single Sparrow: 'Revelation First reads the Apocalypse as the generative text' restates #1755",
 1744: "EA-CORPORA-35, the making of Q: seat records naming the research of #1746",
 1740: "EA-CORPORA-34: seat records naming the research of #1741",
 1754: "the Socrates as Orthonym hologram: the shared records; one sentence restates #202 and #1735",
 1702: "the Fleet: the repaired binding at revelationfirst.com (#1032); a record of the site's binding, no claim of the thesis",
 1420: "The Argument of the Bookshelf: cites 'Revelation First' as under review",
 1460: "three unprimed traversals: a machine composition of the thesis quoted in the record; the registry's records carry the reception",
 1511: "The Upstream Unfoldings: the foldings in, carried by the site (B1) and #1755",
 1498: "the Ω build program: names the site extensions", 1514: "the Ω build program closed: names the upstream page", 1512: "Deep Time: a door to the upstream page",
 884: "Compositional Defiguration: the thesis as its canonical example of visibility measurement; the June record is #881", 883: "the Surface Weather Station: V scores for the thesis's exact query; the June record is #881",
 921: "the research basis: names the thesis among the archive's lines",
 940: "Heteronymy as Ethical Operation: names the work plan as a companion study's source",
 1084: "the Semantic Addresses framework: names the Revelation First reception registry as a data source",
 1694: "the PER recalculation: a record-repair list", 1701: "the Hugging Face datasets: tables", 1739: "the Capture Registry deposit v12.559: section counts", 1676: "the Capture Registry deposit v12.167: section counts", 936: "the Capture Registry deposit v8.9: section counts",
 1729: "Ils ne sont pas marxistes: the 'fringe' label at the Josephus thesis's address", 1680: "The Living Academy: a dataset table", 1643: "AI Fucking Lies: lists the June capture at 'revelation first'", 1769: "Daffodils: the archive's programme listed as the inverse case",
 1766: None, 1088: "the OKF correspondence: the thesis as an example in a quoted table", 829: "the OKF proposal: the thesis as an example of a governance block", 1399: "the OKF proposal (version): the same example", 1402: "the OKF proposal (version): the same example",
 834: "Algorithmic Publishing: the thesis's name as Overview vocabulary", 1228: "Algorithmic Publishing v1.1: the same",
 842: "the Deleuze and Guattari source disambiguation: names the work plan in related deposits", 1033: "the same MPAI (version)", 852: "The Feist Source: the thesis as the frame of a reading", 860: "the Sémantique Potentielle mint block: twenty mint families on the thesis's terms; a mint, no claim on the thesis's definition",
 1350: "the TANG of Revelation studies: the thesis among positions predicted absent from the summarizer layer", 644: "the TANG specification of Revelation studies: the same prediction",
 404: "the Commission's charter: 'Revelation-first' among ground-truth axioms", 1252: "the Epistle Triptych: the same axioms", 10: "the Fractal Navigation Map: a routing instruction", 1255: "the Sacred Ark: 'a forward library that produces the epistles — Revelation first'", 87: "the Constitution of the Semantic Economy: the thesis predates Pearl", 1127: "the same (enacted version)", 200: "a reference to the work plan", 826: "a reference to the work plan", 1458: "a keyword list", 1012: None,
}
verdicts = []
for dep, (strata, reason) in sorted(admitted.items()):
    cl = [c["id"] for c in arch if c["dep"] == dep]
    cids = [x["cand_id"] for k in "DRO" for x in cand[k] if x["dep"] == dep]
    v = {"dep": dep, "strata": strata, "reason": reason, "claims": cl, "candidates": cids, "lineage_instances": sorted(k for k, vv in instances.items() if vv == dep)}
    if dep == 542: v["outside_pass"] = True
    verdicts.append(v)
not_admitted = []
admitted_deps = set(admitted)
for k in "DRO":
    for x in cand[k]:
        d = x["dep"]
        if d in admitted_deps: continue
        r = reasons_reject.get(d)
        if r is None and d in instances:
            r = f"an instance of #{instances[d]} (one work in versions or a restatement; S4: grouped and kept in the provenance graph)"
            if instances[d] in admitted_deps: r += "; its claims carried through the admitted text"
        if r is None and d in site_list:
            r = "read: the fleet's network list or a session tether naming revelationfirst.com among the sites; no claim on the thesis"
        if r is None:
            r = "read: a bare mention, title or reference-list line; no claim on the thesis of the stratum's kind"
        not_admitted.append({"dep": d, "cand": x["cand_id"], "stratum": k, "reason": r})
READING = {
 "row": ROW, "pass": "2026-11-25: first reading of D, R and O candidates (974 D sentences in 130 deposits, 383 R in 92, 509 O-direct in 99), read by deposit; the defining papers read whole or at the loci recorded; the hop not run (recorded: the defining papers' related_ids already name the programme's records, and every one of them is a string candidate)",
 "procedure": "EA-NEGONT-02 v0.10 §3.4 D/R/O (working; not frozen). D where a deposit names the thesis and says something of it; O-direct where the archive applies its own categories to the thesis (#542's status algebra, #1217's machine-mediated theological reception, #1810's Value Field, #1811's operators). R candidates (the thesis related to an archive object) are read with D: the archive's relations of the thesis (the site, the heteronyms, the Historical Logos, the Tenth Muse) are carried where a D claim states them. No O-class: the field sources the thesis as a thesis of the archive, and no archive category is applied to that class at a locus.",
 "reader": COMPOSER, "config": f"datasets/negative-of-the-negative/v2/traversal/{ROW}/config.json",
 "verdicts": verdicts, "not_admitted": not_admitted, "rejected": not_admitted,
 "hop": {"from": sorted(admitted_deps), "candidates": len(cand["H"]), "admitted": [], "rejected": [], "note": "not run"},
 "lineages": [{"lineage": "what it is", "instances": [407, 639, 202, 1217, 1755, 1811], "earliest": 407},
              {"lineage": "first, not early", "instances": [202, 1025, 204, 1735, 1755], "earliest": 202},
              {"lineage": "the claim ladder", "instances": [1217, 832, 1211, 1216, 1400, 1735, 1755], "earliest": 202},
              {"lineage": "grade and falsifiers", "instances": [542, 202, 1735, 1755], "earliest": 542},
              {"lineage": "the conditional extensions", "instances": [639, 1101, 203, 1226, 1217, 1755, 1759, 1765], "earliest": 639},
              {"lineage": "its reception by machines", "instances": [830, 881, 1766, 1811], "earliest": 830},
              {"lineage": "neighbours and the reversed words", "instances": [202, 1811], "earliest": 202}],
 "observations": [
   "The string pass returns 130 deposits; the thesis is named in most of them by reference (a title, a DOI, a network list). The archive's account of the thesis is carried by a short chain: #202 (the seed), #1217 (the work plan), #1735 (the three claims), #1755 (the hologram), #1811 (the disambiguation), with #542 (the grade) outside the pass.",
   "The archive revises its own statements of the thesis in place and keeps the originals: the papyrological inversion of #202 kept beside #1735's 'The physical record cannot rescue absolute priority' (#1755 §7.12); the Josephus thesis bounded by #1217 and suspended by the author (#1755 §7.16).",
   "The string 'Revelation first' also reaches the reading-order sense ('Should you read Revelation first?'), set apart as a homonym; the reversed words never match the pass."],
 "counts": {"D_candidates": len(cand["D"]), "D_deposits": len({x['dep'] for x in cand['D']}), "R_candidates": len(cand["R"]), "R_deposits": len({x['dep'] for x in cand['R']}),
            "O_candidates": len(cand["O"]), "O_deposits": len({x['dep'] for x in cand['O']}), "H_candidates": len(cand["H"]),
            "deposits_admitted": len(admitted), "deposit_claims": sum(1 for c in arch if c["dep"] != "capture-registry"),
            "CAP_claims": sum(1 for c in arch if c["dep"] == "capture-registry")},
 "records": {"CAP": sum(1 for c in arch if c["dep"] == "capture-registry"), "note": f"the archive's own records of the entity, ledgered beside the deposits: the Capture Registry at {SLUG_T} (CAP-1), {SLUG_A} (CAP-2), {SLUG_C} (CAP-3), and the earlier epochs and further compositions (CAP-4 to CAP-9)"},
}

LED = V2 / "ledgers" / ROW
(LED / "field.json").write_text(json.dumps(FIELD_LEDGER, ensure_ascii=False, indent=1), encoding="utf-8")
(LED / "ledger-archive.json").write_text(json.dumps(arch, ensure_ascii=False, indent=1), encoding="utf-8")
(TR / "reading.json").write_text(json.dumps(READING, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------- the row ----------------
import re as _re
listing = []
for e in registry()["entries"]:
    if _re.search(r"revelation[\s\-_]*first|revelationfirst", (e.get("q") or "") + " " + e["slug"], _re.I):
        listing.append(f"{e['slug']} ({e['date']}, {e['surface']}, cards {len(e.get('cite_list') or [])})")
def L_text(sents): return " ".join(s["text"] for s in sents)
cnt = collections.Counter(s[2] for s in SOURCES)
deps_def = sorted(admitted_deps)
from frame import frame
row_out = frame(eT, eA, eC, field_claims, AIDS, listing)
for L in row_out["ontology"]["case"]["loci"]:
    if not found(strip_md(L["quote"]), deposit_text(REGD[L["dep"]]["full_text_path"].lstrip("/"))): fails.append(("case-locus", L["dep"], L["locus"]))
row_out["objects"] = {
 "T": {"path": INR + "T1-" + SLUG_T + ".txt", "sha256": t_sha, "words": t_words, "cards": 3,
       "words_note": f"T, one composition (from 'AI Overview' to the end of the page as pasted, the organic results included): {t_words} words; 3 chips (Wikipedia '+1', إسلام أون لاين '+1', KPU Pressbooks '+3') and three videos. The two field transcripts are listed beside it (role 'field transcript') and are not summed: they are the entity's compositions at other addresses, whose cards are the row's B_D",
       "claims": t_claims, "register": {"register": "datasets/negative-of-the-negative/v2/register.json", "slug": "revelation-first-20261125", "obs_id": eT["obs_id"], "capture_ref": SLUG_T},
       "transcripts": [TT, TA, TC], "listing_rule": "Capture Registry entries whose q + ' ' + slug matches /revelation[\\s\\-_]*first|revelationfirst/i", "listing": listing},
 "KO": {"title": "Revelation First", "genre": "knowledge object, archive composition (ρ = revises), under EA-NEGONT-02 v0.10 (#1726): the final article form of the entity (§4.13), natural sentences under descriptive subheadings (each sentence's sense), attribution beneath each sentence by claim id (§4.5); sources named in the prose where the holder is part of what is said (the archive's papers by title, the site against #1735, the author's statement, the Capture Registry's findings); the thesis's article at reference-work grain",
        "status": "composed 2026-11-25 under v0.10 on BRIEF-NEW-ROWS-FIRST-REVELATION.md (Row 2); not frozen", "sentences": ko,
        "joins": [
          {"act": "order of senses", "sentences": f"1–{len(ko)}", "claims": [], "note": "archive composition (§4.7, E_A's dependency order): what it is (¶0); first, not early (¶1); the claim ladder (¶2); absolute priority and the chronological gate (¶3); corpus priority (¶4); generative priority (¶5); the conditional extensions (¶6); grade, falsifiers and prehistory (¶7); the book's standing in reception (¶8); its author, site and records (¶9); neighbours and the reversed words (¶10); the record of its reception by machines (¶11)"},
          {"act": "holding rivals within the archive (the antecedent)", "sentences": [s["n"] for s in ko if "F4" in s["claims"] and "A1735-05" in s["claims"]], "claims": ["F4", "A1735-05", "F38"], "note": "the site's 'no antecedent' and #1735's prehistory, both carried (§4.4 P_coh); #1735 corrects the novelty claim in its own words"},
          {"act": "an internal inconsistency carried (the work plan's ladder)", "sentences": [s["n"] for s in ko if "A1217-01" in s["claims"]], "claims": ["A1217-01", "A1217-02", "F29"], "note": "five claims announced, six listed (§4.3 internally_inconsistent)"},
          {"act": "an internal inconsistency carried (the census count)", "sentences": [s["n"] for s in ko if "A1735-16" in s["claims"]], "claims": ["A1735-16", "A1735-17"], "note": "seventy thousand units in the abstract, sixty thousand in §IX, both stated"},
          {"act": "a correction kept beside its original (the papyri)", "sentences": [s["n"] for s in ko if "A1755-05" in s["claims"]], "claims": ["A202-04", "A1735-13", "A1755-05"], "note": "the seed's papyrological inversion withdrawn as support and kept as a historical object"},
          {"act": "the registry's reading carried at its grade", "sentences": [s["n"] for s in ko if "CAP-3-06" in s["claims"]], "claims": ["CAP-3-01", "CAP-3-02", "CAP-3-03", "CAP-3-06"], "note": "that ChatGPT reordered the thesis and held the generative claim to a further standard is the registry's reading; the KO states it as the registry's"}],
        "plan": {"order": ko_c, "senses": senses, "marks": {"A1217-01": "internally_inconsistent with A1217-02", "A1735-16": "internally_inconsistent with A1735-17", "A202-04": "withdrawn as support (A1735-13), kept (A1755-05)", "A1755-04": "the author's statement; the Josephus thesis held, its advancement suspended"}, "conflicts": [], "cuts": []},
        "governing_question": "the brief's: the thesis's article at reference-work grain, what it claims, its grade (AXIAL_CONTESTED; hypothesis; falsifiers stated), its author by name, its site; and the erasure at its own string, with the substitute named; mechanics, never motive"},
 "P": mkP(P, "Revelation First", {"genre": "the compression: AIO's interaction grammar (lede, headed clusters, bolded labels, card rail), composed from the v0.10 plan in the archive's ontology; it faces on the card",
                                  "status": "composed 2026-11-25 from the v0.10 knowledge object; not frozen"}),
 "P_B": mkP(P_B, "Revelation First", {"arm": "B (the field alone)", "genre": "popup — the compression from the field ledger alone (B_D and B_R)", "status": "composed 2026-11-25 from the field ledger alone; not frozen"}),
 "KO_B": {"title": "Revelation First", "arm": "B (the field alone)", "genre": "knowledge object", "status": "composed 2026-11-25 from the field ledger alone; not frozen", "sentences": kob},
 "L_B": {"words": wc(L_text(kob)), "text": L_text(kob), "note": "L_F(B), the field-only composition, realized as KO_B (objects.KO_B)"},
 "L_BA": {"words": wc(L_text(ko)), "text": L_text(ko),
          "rail": [{"Card": f"{s[0]} {s[3]}", "Snippet": ([field_claims[k]["quote"] for k, c in field_claims.items() if c['source'] == s[0]] or [s[4]])[0][:200]} for s in SOURCES]
                  + [{"Card": f"#{d} {REGD[d]['title'][:110]}", "Snippet": [c for c in arch if c['dep'] == d][0]["quote"][:200]} for d in deps_def]
                  + [{"Card": f"Capture Registry — {s}", "Snippet": [c for c in arch if c['locus'].startswith(s + ',')][0]["quote"][:200]} for s in (SLUG_T, SLUG_A, SLUG_C)],
          "note": "L_A(B ∪ A), the archive composition (ρ = revises), realized as the knowledge object (objects.KO); its rail is one card per source, grouped by the compression's lineages at render (§5.2)"},
}
row_out["objects"]["P"]["body_words"] = pw
row_out["objects"]["P"]["body_words_rule"] = "lede plus every item's label and text (regex [A-Za-z0-9'’-]+; the bound is 350, §4.8)"
row_out["objects"]["P"]["entity"] = f"Composed under v0.10, archive composition (ρ = revises): KO_B sentences surviving {len(surv)} of {len(kob)}; every field claim carried."
row_out["objects"]["P"]["rail"] = rail
row_out["objects"]["P_B"]["body_words"] = pbw
row_out["objects"]["P_B"]["rail"] = rail_B
row_out["objects"]["P_B"]["entity"] = "the field's entity: the priority thesis as the site and the archive's record pages give it, Lee Sharks's (#202)"
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
 "opening_run": {"rule": "v0.10 §5.10 (read for position; the archive case is not the equal-terms case, recorded for comparison)", "breach": bool(surv and surv[0] == (1, 1))},
 "blocks": {"rule": "sentences typed by the ledgers of the claims they cite (F field-only, A archive-only, M both); recorded as data (the archive case composes in E_A's order, §4.7)",
            "sequence": seq, "field_only_head": head, "archive_only_tail": tail, "breach": False,
            "note": "archive composition: E_A's order governs; the closing sense is the Capture Registry's by nature"},
 "max_similarity": [round(r, 3) for (r, n) in best], "ko_sentence_1_max_similarity_to_KO_B": round(ko1_max, 3),
 "v0.9": {"surviving": len(surv), "of": len(kob), "positions": [n if r >= 0.95 else None for (r, n) in best]},
 "key_note": "the measure is computed under v0.10 (§4.10, unchanged from v0.9); the same values are carried under the key 'v0.9', which the page builder reads (scripts/build_non.py)"}
row_out["field_by_origin"] = {
 "cards": [s[0] for s in SOURCES if s[1] == "card"], "body_named": [], "own_pages": [s[0] for s in SOURCES if s[1] == "own_page"],
 "wikipedia": ["B13"], "census_third_party": [], "unreachable": ["B13 (search, HTTP 429)", "B14"], "title_only": [s[0] for s in SOURCES if s[7]],
 "homonym_cards": ["B6", "B7", "B8"],
 "wikipedia_state": "no article 'Revelation First' (raw wikitext and rendered page HTTP 404, 2026-11-25: 'Wikipedia does not have an article with this exact name.'); the search API for '\"Revelation First\"' refused with HTTP 429 and was not retried by another route",
 "own_pages_note": "the site's home (B1, a card), its pages of #1735, #1811 and #1755 (B9–B11, B_R), the ladder index (B14, HTTP 404); the archive's home (B2, a card); the record pages of #1217 (B3, the Overview's chips, identified by its organic result) and #202 (B12, the deposit the site names as its source)",
 "pools": pools, "sources": field_sources}
row_out["status"]["ledger"] = (f"unaudited (§3.8: one extractor per ledger); field quotes {sum(c['quote_ok'] for c in field_claims.values())}/{len(field_claims)} verified by script against saved text or the transcripts; "
                               f"archive quotes {sum(c['quote_ok'] for c in arch)}/{len(arch)} verified against the deposit texts and the registry (intake scripts/build_row.py; counts in verification.json); marked within the pool: A1217-01/02 and A1735-16/17 internally_inconsistent, A202-04 withdrawn as support")
row_out["composition_v09"] = json.loads(json.dumps(row_out["composition"]))
(V2 / "rows" / f"{ROW}.json").write_text(json.dumps(row_out, ensure_ascii=False, indent=1), encoding="utf-8")

out = {"field_total": f"{sum(c['quote_ok'] for c in field_claims.values())}/{len(field_claims)}",
       "field_by_source": dict(collections.Counter(c["source"] for c in field_claims.values() if c["quote_ok"])),
       "archive_deposits_total": f"{sum(c['quote_ok'] for c in arch if c['dep']!='capture-registry')}/{sum(1 for c in arch if c['dep']!='capture-registry')}",
       "archive_cap_total": f"{sum(c['quote_ok'] for c in arch if c['dep']=='capture-registry')}/{sum(1 for c in arch if c['dep']=='capture-registry')}",
       "T_claims_in_paste": f"{len(T_CLAIMS)-len(t_fail)}/{len(T_CLAIMS)}", "fails": fails, "t_fail": t_fail,
       "unknown_claim_ids": unknown, "kob_nonfield": kob_nonfield, "p_unknown": p_unknown, "p_missing": p_missing, "ledger_claims_not_in_KO": not_in_ko, "kernels_off_rail": kernels_off_rail,
       "translation_missing": tr_missing, "translation_dupes": tr_dupes, "translation_unknown": tr_unknown, "prose_flags": prose_flags, "move_gaps": move_gaps, "move_unknown": move_unknown,
       "ko_sentences": len(ko), "ko_b_sentences": len(kob), "p_body_words": pw, "p_b_body_words": pbw,
       "measure": row_out["measure"]["v0.10"], "blocks": {k: row_out["measure"]["blocks"][k] for k in ("sequence", "field_only_head", "archive_only_tail")},
       "ko1_max_sim": round(ko1_max, 3), "pool_counts": dict(cnt), "listing_n": len(listing)}
(INTAKE / "verification.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1))
