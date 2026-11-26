#!/usr/bin/env python3
"""v1.5 (2026-11-26, at the author's word: "yes, lets correct the hologram, and while we're at it we might as well update and expand it"): #1755 EA-HK-REVFIRST-01
reissued in place v1.4 -> v1.5. The kernel is the v1.4 kernel patched by operator/v15_patch.py and operator/v15_patch_b.py and verified (verify_fw.py, T1–T24);
this script copies it into files/AXN-0C5F/, patches the deposited body by hand-written replacements (the v1.4 builder's scratch is not held), rehashes and records
the reissue. #1756 and #1757 are not reissued. Adapted from reissue_v14_rf.py.
   python3 rebuild/hk-frameworks/reissue_v15_rf.py <patched kernel dir> <operator dir holding verify_fw.py, v15_patch.py, v15_patch_b.py>"""
import json, hashlib, pathlib, re, shutil, sys, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
KD, OP = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
raw = (ROOT / "data/registry.json").read_text(encoding="utf-8"); R = json.loads(raw); D = {x["deposit_number"]: x for x in R["deposits"]}
WORD = ('Lee Sharks, 2026-11-26: 12:03, "it should not have withdrawn it. it is not evidence of priority but it *is* evidence that pauline priority is inferential rather than grounded in material witness."; '
        '12:18, "yes, lets correct the hologram, and while we\'re at it we might as well update and expand it"; 12:21, "scan for anything thats built since the hologram... and anything we missed on the first pass that would strengthen it"; '
        '12:25, "it needs a compressed hologram of the unfoldings ... a mapping of whats there + an outline".')
n = 1755; d = D[n]; assert d["version"] == "v1.4", d["version"]; FD = ROOT / f"files/AXN-{d['hex']}"
K = yaml.safe_load((KD / "00-kernel.yaml").read_text(encoding="utf-8")); assert str(K["version"]) == "1.5" and "unfoldings" in K
V = json.loads((KD / "10-verification.json").read_text(encoding="utf-8")); tests = V["structural_tests"]; assert all(t["pass"] for t in tests.values()) and all(V["integrity"].values())
G = json.loads((KD / "02-graph.jsonld").read_text(encoding="utf-8")); C = [json.loads(l) for l in (KD / "03-claims.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
nodes = {x["@id"]: x for x in G["@graph"]}; F15 = K["fold_in_v15"]; U = K["unfoldings"]; AL = K["argument_layer"]

# ---- files
for p in KD.iterdir():
    if p.is_file(): shutil.copy2(p, FD / "kernel" / p.name)
NEWOP = {"verify_fw.py": None, "v15_patch.py": "v1.5, first stage: records, claims and moves re-bound to current hashes; the papyri recoded held and bounded; the stratum after the first kernel",
         "v15_patch_b.py": "v1.5, second stage: rung VI independent of V; the two ladder pages re-bound; the four records of the scan; the unfoldings, by arrow and by book, and the outline"}
for f in NEWOP: shutil.copy2(OP / f, FD / "operator" / f)
files = [dict(f) for f in d["files"]]; byname = {f["filename"]: f for f in files}
for f, role in NEWOP.items():
    if role: files.append({"filename": f"operator/{f}", "path": f"/files/AXN-{d['hex']}/operator/{f}", "media_type": "text/x-python", "role": "attached file — " + role}); byname[f"operator/{f}"] = files[-1]
changed = []
for f in files:
    b = (FD / f["filename"]).read_bytes(); h = hashlib.sha256(b).hexdigest()
    if f.get("sha256") != h: changed.append(f["filename"])
    f["bytes"], f["sha256"] = len(b), h
listed = sorted(f["filename"] for f in files); present = sorted(p.relative_to(FD).as_posix() for p in FD.rglob("*") if p.is_file()); assert listed == present, (set(listed) ^ set(present))

# ---- body
cur = (ROOT / d["full_text_path"].lstrip("/")).read_text(encoding="utf-8"); fm_end = cur.index("\n---\n", 4) + 5
title = d["title"].replace(" v1.4)", " v1.5)"); assert title != d["title"]
fm = cur[:fm_end].replace(f'title: "{d["title"]}"', f'title: "{title}"').replace("\nversion: v1.4\n", "\nversion: v1.5\n"); assert f'title: "{title}"' in fm and "\nversion: v1.5\n" in fm
body = cur[fm_end:]
def sub(old, new, count=1):
    global body
    assert body.count(old) == count, (old[:80], body.count(old)); body = body.replace(old, new)
rec_n = sum(1 for x in G["@graph"] if x.get("@type") == "Record"); pages = sum(1 for x in G["@graph"] if x.get("@type") == "SurfaceRecord"); strata = sum(1 for x in G["@graph"] if x.get("@type") == "Stratum")
held = sum(1 for c in C if c["state"].get("assertion") == "held"); uc = U["counts"]; none = uc["books_without"]
caps = sum(1 for l in (KD / "07-captures.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())
sub("(EA-HK-REVFIRST-01 v1.4)", "(EA-HK-REVFIRST-01 v1.5)", body.count("(EA-HK-REVFIRST-01 v1.4)")); sub("(EA-MPAI-REVFIRST-01 v1.4)", "(EA-MPAI-REVFIRST-01 v1.5)", body.count("(EA-MPAI-REVFIRST-01 v1.4)"))
sub("EA-HK-REVFIRST-01 v1.4 (kernel); EA-MPAI-REVFIRST-01 v1.4 (map)", "EA-HK-REVFIRST-01 v1.5 (kernel); EA-MPAI-REVFIRST-01 v1.5 (map)")
sub(' "version": "1.4",', ' "version": "1.5",', 2)
sub('"spxi:pillarStatus": "v1.4, reissued in place on 2026-11-11: the fold-in of #1758 v1.1 and #1735 v9, for Revelation First"',
    '"spxi:pillarStatus": "v1.5, reissued in place on 2026-11-26: the papyri held and bounded; rung VI independent of V; ten records entered; the unfoldings mapped by arrow and by book, with an outline of the total programme"')
gf = re.search(r'"spxi:governingFinding": ("(?:[^"\\]|\\.)*")', body); assert gf and "dependent on V" in gf.group(1)
body = body.replace(gf.group(1), json.dumps(K["compression_survival_summary"], ensure_ascii=False))
V15 = (f"**Version 1.5 (26 November 2026, in place).** At the author's word. Four things. "
  f"(1) *The papyri.* v1.0–v1.4 coded the papyrological inversion of #202 (𝔓52, 𝔓98, 𝔓46) as withdrawn, rebutted by #1735 §II.3. The author, 12:03: \"it should not have withdrawn it. it is not evidence of priority but it *is* evidence that pauline priority is inferential rather than grounded in material witness.\"; \"its just about what kind of evidence it is\"; \"its not evidence of priority but its also not not evidence of priority\"; \"its a relevant datum in any case\". The claim is held and its strength bounded (claim:rf-202-papyri, bounded by claim:rf-1735-physical); the edge is *bounds*, on strength; no claim in the kernel is withdrawn. Six sentences of #202 Claim 3 and #1735 §II.3 enter as claims, among them \"Pauline priority is inferential, not direct material fact.\" "
  f"(2) *Rung VI.* The author ruled on 9 November, 12:48: \"rung vi does not depend on v. but v would of course strengthen vi if the entire material transmission and production chain could be shown to work by means of self-division\". The site carried the ruling from that day; this kernel did not, through four versions. Rung VI is now INDEPENDENT, strengthened by V; no rung's defeat carries to another. The verifier found it: the two ladder pages no longer matched their hashes. "
  f"(3) *Records.* Ten enter. Since the first kernel: the Josephus thesis told (#1759) and its Slavonic text seated and scored (#1760, #1765), The Crossing of Names (#1762), the recovery valued from both ends (#1810), the name kept apart from the First Revelation (#1811), the genre imposed on the books (#1798), the economy of bad inference (#1802). Missed on the first pass: Counterfeit Orthodoxies (#65, April), which states the forward library and the fourfold; the Tacitus seat (#1738). Three records had a References list added in place on 23 November (#1737, #1741, #1747); their claims and {F15['moves_rebound']} moves are re-bound to the current hashes, every quotation re-asserted verbatim. "
  f"(4) *The unfoldings* (map §7.17; `unfoldings` in 00-kernel.yaml). Every arrow the records draw from Revelation to another book of the New Testament, at its grain and state: {uc['arrows']} arrows, {uc['run']} run to completion, {uc['worked']} worked to derivation grade, {uc['mapped']} mapped, {uc['unresolved']} unresolved, {uc['withheld']} withheld by a date, {uc['drawn']} drawn and not run, {uc['observed']} observed, {uc['named']} named at the founding grain; a table by book, computed from the arrows, with {len(none)} books unreached ({', '.join(none)}); and an outline of the total programme, headed by the author's statement of 12:35 and marked as an outline. "
  f"The kernel holds {rec_n} records, {len(C)} claims and {len(G['edges'])} edges. The argument moves of the ten new records are not written and are declared owed, with three earlier records that v1.4 declared complete and were not (#828, #1484, #1751): T22. Back-projection was not re-run. All {len(tests)} structural tests pass. The kernel was patched in place by two scripts, attached; the v1.4 builder was not re-run.\n\n")
sub("**Version 1.4 (11 November 2026, in place).**", V15 + "**Version 1.4 (11 November 2026, in place).**")
old205 = re.search(r"2\. \*\*The kernel\*\* \(EA-HK-REVFIRST-01 v1\.5\), attached: .*?\n", body).group(0)
body = body.replace(old205, f"2. **The kernel** (EA-HK-REVFIRST-01 v1.5), attached: {rec_n} records and {pages} site pages in {strata} strata; {len(C)} claims, none withdrawn, {held} held with a stated bound; {len(G['edges'])} edges; {caps} captures; "
    f"9 lines of research; the symmetric ledger; the unfoldings ({uc['arrows']} arrows, the table by book, the outline); {AL['moves']:,} argument moves from {AL['records_with_moves']} records, joined by {AL['edges']:,} edges; {len(AL['records_without_moves'])} records without moves, declared.\n")
sub("All 16 structural tests pass (T1, T2, T3, T4, T6, T7, T8, T9, T11, T14, T15, T17, T18, T19, T20, T21); integrity holds on every kernel file.",
    f"All {len(tests)} structural tests pass ({', '.join(t.split()[0] for t in tests)}); integrity holds on every kernel file. T22–T24 are new at v1.5: records without moves declared; every arrow with a declared state and warrants that resolve; the table by book equal to the table computed from the arrows. Back-projection was last run on v0.1 and v0.2 and was not re-run at v1.5.")
for f in files:   # the file table: size and hash per row; two new operator rows
    m = re.search(r"(\| \[" + re.escape(f["filename"]) + r"\]\([^)]*\) \| [^|]* \| )[\d,]+( \| `)[0-9a-f]{64}(` \|)", body)
    if m: body = body.replace(m.group(0), f"{m.group(1)}{f['bytes']:,}{m.group(2)}{f['sha256']}{m.group(3)}")
    else:
        assert f["filename"] in ("operator/v15_patch.py", "operator/v15_patch_b.py"), f["filename"]
        anchor = re.search(r"\| \[operator/v14_post\.py\].*\n", body).group(0)
        body = body.replace(anchor, anchor + f"| [{f['filename']}](https://www.alexanarch.org{f['path']}) | {f['role'].split(' — ', 1)[1]} | {f['bytes']:,} | `{f['sha256']}` |\n") if f["filename"].endswith("v15_patch.py") else \
               body.replace(re.search(r"\| \[operator/v15_patch\.py\].*\n", body).group(0), re.search(r"\| \[operator/v15_patch\.py\].*\n", body).group(0) + f"| [{f['filename']}](https://www.alexanarch.org{f['path']}) | {f['role'].split(' — ', 1)[1]} | {f['bytes']:,} | `{f['sha256']}` |\n")
sub("I REVERSIBLE, II SAME-CLASS, III INDEPENDENT, IV EXECUTABLE, V CONTINGENT, VI DEPENDENT. The ladder is the kernel's dependency structure; a rung's defeat carries to the rungs that depend on it, and only to them.",
    "I REVERSIBLE, II SAME-CLASS, III INDEPENDENT, IV EXECUTABLE, V CONTINGENT, VI INDEPENDENT of V, which would strengthen it (the author, 2026-11-09; v1.0–v1.4 carried DEPENDENT). The ladder is the kernel's dependency structure; no rung depends on another, and a rung's defeat carries to itself only.")
sub("  - `rf-202-papyri` (interpretation; withdrawn; rung I): “the papyrological inversion (𝔓52/𝔓98/𝔓46)”",
    "  - `rf-202-papyri` (interpretation; held, bounded by `rf-1735-physical` on kind of evidence; rung I): “the papyrological inversion (𝔓52/𝔓98/𝔓46)”. Coded withdrawn in v1.0–v1.4; the author, 2026-11-26: not evidence of priority, and not not evidence of priority; evidence that Pauline priority is inferential rather than grounded in material witness.")
sub("— DEPENDENT, body H; depends on V. The site:", "— INDEPENDENT, body H; independent of V, strengthened by V. The site:")
sub("Defeat: “Depends on V. Defeated without disturbing rungs I–IV.”", "Defeat: “Independent of V; V would strengthen it. Defeated without disturbing rungs I–IV.”")
old999 = re.search(r"\nA rung's defeat carries to every rung that depends on it \(rung VI: 'Depends on V'.*?\n", body).group(0); body = body.replace(old999, "\n" + K["dependency"]["rule"] + "\n")
sub("- “the papyrological inversion (𝔓52/𝔓98/𝔓46)” (rec:202) — rebuts by “The physical record cannot rescue absolute priority” (rec:1735)",
    "- “the papyrological inversion (𝔓52/𝔓98/𝔓46)” (rec:202) — held; bounded on strength by “The physical record cannot rescue absolute priority” (rec:1735). Recorded as rebutted and withdrawn in v1.0–v1.4.")
sub("the Logos rung depends on V (rung VI).", "the Logos rung is independent of V, which would strengthen it (rung VI).")
sub("- `claim:rf-1735-physical` **rebuts** `claim:rf-202-papyri` (establishment) — the papyrological inversion withdrawn as evidence of priority: 'The physical record cannot rescue absolute priority' (#1735 §II.3)",
    "- `claim:rf-1735-physical` **bounds** `claim:rf-202-papyri` (strength) — the papyrological inversion held, its strength bounded by kind of evidence: not evidence of priority, and not not evidence of priority; evidence that Pauline priority is inferential rather than grounded in material witness (the author, 2026-11-26). 'The physical record cannot rescue absolute priority, but it also cannot close the bounded questions' (#1735 §II.3)")
sub("- `rung:VI` **depends_on** `rung:V` — site:ladder-logos 'Depends on V.'", "- `rung:V` **strengthens** `rung:VI` — site:ladder-logos 'Independent of V; V would strengthen it.'; no defeat carried")
sub("- “does pauline chronology defeat revelation first”", "- “revelation first papyri” — fails if the papyri are reported as proof of priority, or as withdrawn (they are held: evidence that Pauline priority is inferential rather than grounded in material witness; the author, 2026-11-26)\n"
    "- “does the logos rung depend on the josephus thesis” — fails if rung VI is reported as dependent on V (independent; V would strengthen it: the author, 2026-11-09 12:48)\n"
    "- “which books of the new testament does revelation first derive from revelation” — fails if a mapped, drawn, observed or named arrow is reported as a derivation (one arrow is run: Smyrna to James), or if the Gospels are reported as derived\n"
    "- “does pauline chronology defeat revelation first”")
sub("- The Historical Logos, which will take the joins as members, is planned and unbuilt.",
    "- The Historical Logos, which will take the joins as members, is planned and unbuilt.\n"
    f"- Thirteen records carry anchor claims and no argument moves: the ten that entered at v1.5 and #828, #1484 and #1751, which v1.4 declared complete. Their moves are owed, each record to be read in full.\n"
    "- The outline of the total programme (§7.17) is proposed and not ruled. The mapping the author called for on 26 November (12:35) is opened as a working file, apart from this record.\n"
    "- #1735 §II.3 reads “The material finding is therefore neutral”. The kernel scopes the sentence to dates of composition and does not edit the article.\n"
    "- Back-projection has not been run on v1.5.")
stmt = lambda s: f"- {s['date']}, {s['where']}: “{s['text']}” Status: {s['status']}"
old1084 = re.search(r"\n- 2026-11-09T09:52-05:00, in session, on an unprimed ChatGPT reading.*?\n", body).group(0)
body = body.replace(old1084, old1084 + "".join(stmt(s) + "\n" for s in sorted(K["author_statements"], key=lambda s: s["date"]) if s["date"] > "2026-11-09T09:52-05:00"))

# §7.0: what entered at v1.5
def cl_line(c):
    st = c["state"]; a = st.get("assertion") or "; ".join(f"{k} {v}" for k, v in st.items())
    extra = "; ".join(x for x in ([f"rung {st['rung']}"] if st.get("rung") else []) + ([f"bounded by `{st['bounded_by'].split(':')[1]}`"] if st.get("bounded_by") else []) + ([f"generation {st['generation']}"] if st.get("generation") else []))
    return f"  - `{c['id']}` ({c['claim_kind']}; {a}{'; ' + extra if extra else ''}): “{c['target']['exact']}”" + (f" {c['notes']}" if c.get("notes") else "")
def rec_line(n):
    x = nodes[f"rec:{n}"]; cr = x.get("creator"); cr = "; ".join(cr) if isinstance(cr, list) else cr
    return f"- **#{n}** [{x['title']}]({x['url']}) ({x['date']}; {cr}) · body {x['body']}" + (f"; also {', '.join(x['body_secondary'])}" if x["body_secondary"] else "")
added = [c.split(":", 1)[1] for c in F15["claims_added"]]; CLD = {c["id"]: c for c in C}; newrecs = [r["deposit"] for r in F15["records"]] + [r["deposit"] for r in F15["scan"]["records"]]
S70 = ["#### 7.0 After the first kernel (11–26 November), and the scan of 26 November", "",
       "Ten records entered at v1.5 with anchor claims quoted verbatim and bound to their hashes. Their argument moves are owed. Eight were deposited after the first kernel; two (#65, #1738) were missed on the first pass and sit in the kernel at the strata of their dates.", ""]
for n in sorted(newrecs, reverse=True):
    S70.append(rec_line(n) + (" · missed on the first pass" if n in F15["scan"]["missed_on_the_first_pass"] else ""))
    S70 += [cl_line(CLD[c]) for c in added if CLD[c]["target"]["record"] == f"rec:{n}"]
S70 += ["", "Claims added at v1.5 to records and pages already in the map:", ""]
for tgt in sorted({CLD[c]["target"]["record"] for c in added if CLD[c]["target"]["record"].startswith("site:") or int(CLD[c]["target"]["record"][4:]) not in newrecs}, key=lambda t: (t.startswith("site:"), -int(t[4:]) if t.startswith("rec:") else 0)):
    S70.append(f"- **{'#' + tgt[4:] if tgt.startswith('rec:') else tgt}** {nodes[tgt]['title']}")
    S70 += [cl_line(CLD[c]) for c in added if CLD[c]["target"]["record"] == tgt]
lo = F15["scan"]["read_and_left_out"]
S70 += ["", "Read in the scan and left out: " + "; ".join(f"#{k} ({v})" for k, v in lo.items()) + ".", "", ""]
sub("#### 7.1 The records search of 10 November 2026", "\n".join(S70) + "#### 7.1 The records search of 10 November 2026")

# §7.17: the unfoldings
A = U["arrows"]; P = U["outline_of_the_total_programme"]
S717 = ["#### 7.17 The unfoldings: the arrows, the table by book, the outline", "", U["rule"], "",
        "States: " + " ".join(f"**{k}**, {v}." for k, v in U["states"].items()), "",
        "Classes (#1416): " + " ".join(f"**{k}**, {v}." for k, v in U["classes"].items()), "",
        "| Arrow | Seed in Revelation | Lands at | State | Grade · class | Operations | Records |", "|---|---|---|---|---|---|---|"]
for a in A:
    tg = "; ".join(a["targets"]) if len(a["targets"]) <= 8 else f"{len(a['targets'])} loci: " + "; ".join(a["targets"][:6]) + " …"
    S717.append(f"| `{a['id']}`{' ' + a['name'] if a.get('name') else ''}{' → ' + a['epistle'] if a.get('epistle') else ''} | {a['seed']} | {tg} | {a['state']} | {a.get('grade', '—')} · {a.get('cls', '—')} | {', '.join(a.get('operations', [])) or '—'} | {', '.join('#' + str(r) for r in a['records'])} |")
S717 += ["", "Stated limits, in the records' words: " + " ".join(f"`{a['id']}`: {a['stated_limit']}" for a in A if a.get("stated_limit")), ""]
sm = next(a for a in A if a["id"] == "letter:smyrna")
S717 += [f"The one run case, Smyrna to James (#1415; the site's working surface): {sm['coverage']}; {sm['uniformity']}. Anchors: " + "; ".join(sm["anchors"]) + ". Residue: " + "; ".join(sm["residue"]) + f". Ordering: {sm['ordering']}", "",
         "**By book** (computed from the arrows; the strongest state reached, and the loci):", ""]
for b, v in U["by_book"].items():
    S717.append(f"- **{b}** — {v['strongest_state']}" + (f"; {len(v['arrows'])} arrow{'s' if len(v['arrows']) != 1 else ''} ({', '.join('`' + x + '`' for x in v['arrows'])}); " + "; ".join(v["loci"][:10]) + (" …" if len(v["loci"]) > 10 else "") if v["arrows"] else ""))
S717 += ["", "**Not claimed:** " + " ".join(f"({i}) {x}" for i, x in enumerate(U["not_claimed"], 1)), "",
         "**The outline of the total programme.** " + P["status"][0].upper() + P["status"][1:] + ".", "",
         f"The author, {P['author_programme']['at']}: “{P['author_programme']['text']}”", "",
         "Object: " + P["object"], ""]
S717 += [f"{s['n']}. **{s['name'][0].upper() + s['name'][1:]}.** {s['what'][0].upper() + s['what'][1:]}. Have: {s['have']}. Owed: {s['owed']}." for s in P["stages"]]
S717 += ["", "Order of work proposed: " + "; ".join(f"({i}) {x}" for i, x in enumerate(P["order_of_work"], 1)) + ".", "", "What would count against it: “" + P["what_would_count_against"] + "”", "", ""]
sub("### 8. Captures", "\n".join(S717) + "### 8. Captures")
spine = "".join(f"- #{n} {nodes[f'rec:{n}']['axn']} — [{nodes[f'rec:{n}']['title']}]({nodes[f'rec:{n}']['url']})\n" for n in sorted(newrecs))
m = re.search(r"- #1509 AXN:[^\n]*\n", body); body = body.replace(m.group(0), m.group(0) + spine)
assert "withdrawn; rung I" not in body and "— DEPENDENT, body H" not in body

s = fm + body
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
d.setdefault("reissue_history", []).append({"date": "2026-11-26", "from_version": "v1.4", "to_version": "v1.5", "hash_before_reissue": d["hash"], "axn_before_reissue": d["axn"],
    "title_before_reissue": d["title"], "reason": WORD,
    "changes": (f"The papyri claim of #202 recoded from withdrawn to held and bounded (edge bounds, on strength), six claims added from #202 Claim 3 and #1735 §II.3; rung VI recoded independent of V and strengthened by it, on the author's ruling of 2026-11-09 12:48, "
                f"the two ladder pages re-bound; three records and {F15['moves_rebound']} moves re-bound to current hashes; ten records entered (#1759, #1760, #1762, #1765, #1798, #1802, #1810, #1811; #65 and #1738 from the first pass) with anchor claims, their moves owed; "
                f"the unfoldings added: {uc['arrows']} arrows by state, the table by book, and an outline of the total programme headed by the author's statement of 12:35; tests T22–T24; {len(C)} claims, {len(G['edges'])} edges. Files changed: {len(changed)}.")})
prior = d["axn"]
d.update({"title": title, "version": "v1.5", "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl,
          "axn_reading": AX.axn_reading_from_clusters(cl), "files": files, "full_text_chars": len(s), "date_modified": "2026-11-26"})
d["description"] = d["description"].rstrip() + (" Version 1.5 (26 November 2026, in place) holds the papyri as evidence that Pauline priority is inferential rather than grounded in material witness, where earlier versions had them withdrawn; sets rung VI independent of V, "
    "which would strengthen it; enters ten records, among them the Josephus Thesis narrative, the Slavonic text and its census, The Crossing of Names, the recovery's valuation, and Revelation First ≠ The First Revelation; and maps the unfoldings arrow by arrow and book by book, "
    f"{uc['arrows']} arrows from Smyrna to James (run) to the four Gospels (named only), with an outline of the total programme.")
if d.get("wiki_article"): d["wiki_article"] = d["wiki_article"].rstrip() + (" Version 1.5 (26 November 2026) corrects two codings on the author's word, the papyri (held, not withdrawn) and rung VI (independent of V), enters ten records, and adds a map of the unfoldings from Revelation to the other books of the New Testament with an outline of the programme.")
(ROOT / d["full_text_path"].lstrip("/")).write_text(s, encoding="utf-8"); dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(s, encoding="utf-8")
ind = 1 if raw.startswith('{\n "') else (2 if raw.startswith('{\n  "') else None)
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, indent=ind) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
json.dump({prior: d["axn"]}, open(pathlib.Path(__file__).parent / "axn-moves-20261126-v15-rf.json", "w"), ensure_ascii=False, indent=1)
print(n, prior, "->", d["axn"], "| files changed:", len(changed), "| chars", len(s))
