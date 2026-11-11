#!/usr/bin/env python3
"""#1754 Socrates as Orthonym reissued in place v1.2 -> v1.3 (2026-11-10, at the author's word of 21:58: "yup lets build the argument layer"): the
argument layer the three sister kernels carry. Thirty-four of the kernel's 47 records had no moves; eight parallel readers each read a range in full
(the brief and every builder attached as operator/v13-moves.zip), every quotation asserted verbatim (mlib.py, check_args.py); the thirteen records
shared with the sister kernels keep their moves of 2026-11-09. The builder and verifier gain the layer and tests T20 and T21. Body revised from the
deposited text; hash and AXN re-derived at the same position and family, the prior hash, AXN and title kept in reissue_history.
   python3 rebuild/hk-frameworks/reissue_v13_orthonym.py <scratch hk-orthonym-v13 dir> <scratch hk-frameworks dir>"""
import json, hashlib, pathlib, re, shutil, sys, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
OR, HK = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); sys.path.insert(0, str(HK)); import v12_spxi
raw = (ROOT / "data/registry.json").read_text(encoding="utf-8"); R = json.loads(raw); D = {x["deposit_number"]: x for x in R["deposits"]}
A = "https://www.alexanarch.org"; n = 1754; d = D[n]; assert d["version"] == "v1.2", d["version"]; FD = ROOT / f"files/AXN-{d['hex']}"
for p in sorted((OR / "out-v13").iterdir()):
    if p.is_file(): shutil.copy2(p, FD / "kernel" / p.name)
for nm in ("build_hk_orthonym.py", "verify_hk.py", "v13-moves.zip"): shutil.copy2(OR / nm, FD / "operator" / nm)
shutil.copy2(HK / "args_layer.py", FD / "operator" / "args_layer.py"); shutil.copy2(HK / "check_args.py", FD / "operator" / "check_args.py")
fl = list(d["files"]); have = {f["filename"] for f in fl}
ADD = [("kernel/04-arguments.jsonl", "application/jsonl", "the argument layer (v1.3): each record's argument compressed into moves (data, counts, inferences, findings, prices, rivals and replies, defeat conditions, methods, hypotheses and dated states), each a verbatim quotation bound to its record's hash, joined by typed edges"),
       ("operator/v13-moves.zip", "application/zip", "v1.3: the readers' brief, the eight readers' builders (build_o_g1–g8.py) and their outputs (o*.jsonl), and mlib.py, which asserts each quotation verbatim"),
       ("operator/args_layer.py", "text/x-python", "writes the argument layer from the readers' moves, re-asserting each quotation at the record's current hash; tests T20 and T21"),
       ("operator/check_args.py", "text/x-python", "the readers' check: every quotation verbatim in its seated record, every edge resolved, every kind and relation in the vocabulary")]
i0 = next(i for i, f in enumerate(fl) if f["filename"] == "kernel/03-claims.jsonl") + 1
for fn, media, role in ADD:
    if fn in have: continue
    e = {"filename": fn, "path": f"/files/AXN-{d['hex']}/{fn}", "bytes": 0, "sha256": "", "media_type": media, "role": "attached file — " + role}
    if fn.startswith("kernel/"): fl.insert(i0, e)
    else: fl.append(e)
out = []
for f in fl:
    b = (FD / f["filename"]).read_bytes(); out.append(dict(f, bytes=len(b), sha256=hashlib.sha256(b).hexdigest()))
listed = sorted(f["filename"] for f in out); present = sorted(p.relative_to(FD).as_posix() for p in FD.rglob("*") if p.is_file())
assert listed == present, (sorted(set(present) - set(listed)), sorted(set(listed) - set(present)))
files = out
K = yaml.safe_load((FD / "kernel/00-kernel.yaml").read_text(encoding="utf-8")); al = K["argument_layer"]; assert str(K["version"]) == "1.3" and not al["records_without_moves"]
V = json.loads((FD / "kernel/10-verification.json").read_text(encoding="utf-8")); st = V["structural_tests"]; npass = sum(1 for x in st.values() if x["pass"]); assert npass == len(st) == 19
cur = (ROOT / d["full_text_path"].lstrip("/")).read_text(encoding="utf-8"); fm_end = cur.index("\n---\n", 4) + 5
T1 = d["title"]; T2 = T1.replace("(EA-HK-ORTHONYM-01 v1.2)", "(EA-HK-ORTHONYM-01 v1.3)"); assert T2 != T1
fm = cur[:fm_end].replace(f'title: "{T1}"', f'title: "{T2}"').replace("\nversion: v1.2\n", "\nversion: v1.3\n"); assert "\nversion: v1.3\n" in fm and T2 in fm
b = cur[fm_end:].lstrip("\n"); assert b.startswith("# " + T1 + "\n\n"); b = b[len("# " + T1 + "\n\n"):]
i = b.index("**Version 1.2 (10 November 2026, in place).**"); j = b.index("\n", i); v12 = b[i:j + 1]
k1 = b.index("**Version 1.1 (8 November 2026, in place).**"); assert b.index("## SPXI packet") > j and b.index("## SPXI packet") < k1
NEWREC = sorted(int(x) for x in json.loads(json.dumps([m.split("o")[1].split(".")[0] for m in __import__("zipfile").ZipFile(OR / "v13-moves.zip").namelist() if re.match(r"o\d{4}\.jsonl$", m)])))
note = ("**Version 1.3 (10 November 2026, in place).** At the author's word of 21:58 (\"yup lets build the argument layer\"). The kernel gains the argument layer its three sister "
        "kernels carry (`04-arguments.jsonl`, tests T20 and T21). Of its 47 records, " + str(len(NEWREC)) + " had no moves: eight parallel readers each read a range of them in full, "
        "and every quotation was asserted verbatim against the seated text (the readers' brief and builders attached as `operator/v13-moves.zip`). The other "
        + str(47 - len(NEWREC)) + " records, shared with Revelation First, the Tenth Muse and the Historical Logos, keep their moves of 9 November. "
        f"The layer holds {al['moves']:,} moves from {al['records_with_moves']} records, joined by {al['edges']:,} edges; corrections the records make to themselves are carried as dated states with the correcting move pointing to them. "
        f"All {npass} structural tests pass, and back-projection v0.1 still gives scope A 1.0 and scope B 1.0. Nothing else in the kernel is changed. The readers noted text defects in several records; "
        "they are recorded for the author and the records are left as deposited. The SPXI packet is reissued at v1.3. Attached files replaced and re-hashed.\n")
pk = v12_spxi.packet_md("EA-HK-ORTHONYM-01", K, D, version="1.3", note="the argument layer, every record of the kernel read in full")
b = note + "\n" + pk + "\n" + v12 + "\n" + b[k1:]
b = b.replace("1. **The map** (EA-MPAI-ORTHONYM-01 v1.2)", "1. **The map** (EA-MPAI-ORTHONYM-01 v1.3)", 1)
b = b.replace("; the symmetric ledger; the records search of 10 November 2026.", f"; the symmetric ledger; the records search of 10 November 2026; the argument layer, {al['moves']:,} moves from {al['records_with_moves']} records joined by {al['edges']:,} edges.", 1)
b = b.replace("2. **The kernel** (EA-HK-ORTHONYM-01 v1.2)", "2. **The kernel** (EA-HK-ORTHONYM-01 v1.3)", 1)
b = b.replace("3. **The operator**, attached: the builder, the verifier, the first-seating resolver and its texts, and the facsimile writer.",
              "3. **The operator**, attached: the builder, the verifier, the first-seating resolver and its texts, the facsimile writer, and the argument layer's writer, check and moves.", 1)
assert "All 17 structural tests pass." in b; b = b.replace("All 17 structural tests pass.", f"All {npass} structural tests pass (T20 and T21, the argument layer, added at v1.3).", 1)
b = re.sub(r"(Socrates as Orthonym — The Framework Map: [^\n]*?\(EA-MPAI-ORTHONYM-01 )v1\.2\)", r"\1v1.3)", b, count=1)
rows = "\n".join(f"| [{f['filename']}]({A}{f['path']}) | {f['role'].replace('attached file — ', '')} | {f['bytes']:,} | `{f['sha256']}` |" for f in files)
i = b.index("| File | Holds | Bytes | SHA-256 |\n|---|---|---|---|\n"); j = b.index("\n\n", i)
b = b[:i] + "| File | Holds | Bytes | SHA-256 |\n|---|---|---|---|\n" + rows + b[j:]
for chk in ("(EA-HK-ORTHONYM-01 v1.3)", "**Version 1.3", "**Version 1.2", "**Version 1.1", "## SPXI packet", "04-arguments.jsonl"): assert chk in b, chk
s = fm + "\n# " + T2 + "\n\n" + b
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
old = {f["filename"]: f["sha256"] for f in d["files"]}; changed = [f["filename"] for f in files if old.get(f["filename"]) != f["sha256"]]
d.setdefault("reissue_history", []).append({"date": "2026-11-10", "from_version": "v1.2", "to_version": "v1.3", "hash_before_reissue": d["hash"], "axn_before_reissue": d["axn"],
    "title_before_reissue": d["title"], "reason": 'Lee Sharks, 2026-11-10 21:58: "adopted on all. and yup lets build the argument layer and update versions"',
    "changes": f"The argument layer: {len(NEWREC)} records read in full by eight parallel readers, {al['moves']:,} moves from {al['records_with_moves']} records, {al['edges']:,} edges; builder and verifier gain T20 and T21; {npass} of {npass} structural tests pass; SPXI packet reissued at v1.3. ({len(changed)} files new or re-hashed.) Hash and AXN re-derived."})
prior = d["axn"]
d.update({"title": T2, "version": "v1.3", "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl,
          "axn_reading": AX.axn_reading_from_clusters(cl), "files": files, "full_text_chars": len(s), "date_modified": "2026-11-10"})
d["description"] = d["description"].rstrip() + " Version 1.3 (10 November 2026, in place) adds the argument layer, every record of the kernel read in full and its argument compressed into verbatim moves."
if d.get("wiki_article"): d["wiki_article"] = d["wiki_article"].rstrip() + " Version 1.3 (10 November 2026) adds an argument layer: each of the kernel's records read in full and compressed into moves, each a verbatim quotation bound to its record's hash."
(ROOT / d["full_text_path"].lstrip("/")).write_text(s, encoding="utf-8"); dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(s, encoding="utf-8")
ind = 1 if raw.startswith('{\n "') else (2 if raw.startswith('{\n  "') else None)
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, indent=ind) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
json.dump({prior: d["axn"]}, open(pathlib.Path(__file__).parent / "axn-moves-20261110-v13-orthonym.json", "w"), ensure_ascii=False, indent=1)
print(n, prior, "->", d["axn"], "| files changed:", len(changed), "| new-read records:", len(NEWREC))
