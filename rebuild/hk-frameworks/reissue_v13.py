#!/usr/bin/env python3
"""v1.3 (2026-11-10, at the author's word of 21:31: "lets do the argument moves"): #1755, #1756 and #1757 reissued in place v1.2 -> v1.3, the argument
moves of the records that entered at v1.2 without moves, each record read in full (the scratch args/build_s*.py, attached as operator/v13-moves.zip).
#1754 has no argument layer and is not reissued. Adapted from the v1.2 script below.
   python3 rebuild/hk-frameworks/reissue_v13.py <scratch hk-frameworks dir>

v1.2: Reissue in place, at the author's word of 2026-11-10 20:48 ("lets address, deposit, and turn to incorporating it into rev first and versioning all four
holographic frames... also - if the framed themselves have not yet been spxi treated, they need to be"): the four framework holograms v1.1 -> v1.2.
#1754 EA-HK-ORTHONYM-01, #1755 EA-HK-REVFIRST-01, #1756 EA-HK-TENTHMUSE-01, #1757 EA-HK-HISTLOGOS-01. The records search of 2026-11-10
(rebuild/hk-frameworks/v12-staging) enters each kernel as stratum S0, the Philo piece deposited as #1758 among the evidence where the staging places it;
related work, history, joins and flags carried in each kernel; each body given an SPXI packet. Attached files replaced and re-hashed; hash and AXN
re-derived at the same position and family, the prior hash, AXN and title kept in reissue_history.
   python3 rebuild/hk-frameworks/reissue_v12.py <scratch hk-frameworks dir> <scratch hk-orthonym-v12 dir>"""
import json, hashlib, pathlib, re, shutil, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
HK = pathlib.Path(sys.argv[1]); SCR = HK.parent
sys.path.insert(0, str(HK)); import v12_spxi
raw = (ROOT / "data/registry.json").read_text(encoding="utf-8"); R = json.loads(raw); D = {x["deposit_number"]: x for x in R["deposits"]}
WORD = 'Lee Sharks, 2026-11-10 21:31: "lets do the argument moves"; the records that entered at v1.2 without moves, each read in full.'
A = "https://www.alexanarch.org"

def rehash(hx, files):
    FD = ROOT / f"files/AXN-{hx}"
    out = []
    for f in files:
        b = (FD / f["filename"]).read_bytes(); out.append(dict(f, bytes=len(b), sha256=hashlib.sha256(b).hexdigest()))
    listed = sorted(f["filename"] for f in out); present = sorted(p.relative_to(FD).as_posix() for p in FD.rglob("*") if p.is_file())
    assert listed == present, ("listed/present differ", sorted(set(present) - set(listed))[:5], sorted(set(listed) - set(present))[:5])
    return out

def reissue(n, title, body, changes, desc_add, wiki_add, files):
    d = D[n]; assert d["version"] == "v1.2", (n, d["version"])
    cur = (ROOT / d["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
    fm_end = cur.index("\n---\n", 4) + 5
    fm = cur[:fm_end].replace(f'title: "{d["title"]}"', f'title: "{title}"').replace("\nversion: v1.2\n", "\nversion: v1.3\n")
    assert f'title: "{title}"' in fm and "\nversion: v1.3\n" in fm, n
    if "#1758" not in fm:
        fm = re.sub(r'(\nrelated_ids: "[^"\n]*)"', lambda m: m.group(1) + '; #1758 (In the Midst of the Seven)"', fm, count=1)
    s = fm + "\n# " + title + "\n\n" + body
    h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
    old = {f["filename"]: f["sha256"] for f in d["files"]}
    changed = [f["filename"] for f in files if old.get(f["filename"]) != f["sha256"]]
    d.setdefault("reissue_history", []).append({"date": "2026-11-10", "from_version": "v1.2", "to_version": "v1.3", "hash_before_reissue": d["hash"],
        "axn_before_reissue": d["axn"], "title_before_reissue": d["title"], "reason": WORD, "changes": changes + f" ({len(changed)} files new or re-hashed.)"})
    prior = d["axn"]
    d.update({"title": title, "version": "v1.3", "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl,
              "axn_reading": AX.axn_reading_from_clusters(cl), "files": files, "full_text_chars": len(s), "date_modified": "2026-11-10"})
    d["description"] = d["description"].rstrip() + desc_add
    if d.get("wiki_article"): d["wiki_article"] = d["wiki_article"].rstrip() + wiki_add
    (ROOT / d["full_text_path"].lstrip("/")).write_text(s, encoding="utf-8")
    dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
    if dp.exists(): dp.write_text(s, encoding="utf-8")
    print(n, prior, "->", d["axn"], "| files changed:", len(changed)); return prior, d["axn"]

moves = {}
import yaml
STAGED = {1755: SCR / "deposit-revfirst-v13", 1756: SCR / "deposit-tenthmuse-v13", 1757: SCR / "deposit-histlogos-v13"}
for n, ST in STAGED.items():
    d = D[n]; FD = ROOT / f"files/AXN-{d['hex']}"
    owed = yaml.safe_load((FD / "kernel/00-kernel.yaml").read_text(encoding="utf-8"))["argument_layer"]["records_without_moves"]
    body = (ST / "body.md").read_text(encoding="utf-8"); title = body.split("\n", 1)[0][2:].strip(); assert title.endswith(" v1.3)"), title
    body = body.split("\n", 1)[1].lstrip("\n")
    files = json.loads((ST / "files.json").read_text(encoding="utf-8"))
    for f in files:
        src = ST / "files" / f["filename"]; dst = FD / f["filename"]; dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst)
        b = dst.read_bytes(); assert hashlib.sha256(b).hexdigest() == f["sha256"] and len(b) == f["bytes"], f["filename"]
    files = rehash(d["hex"], files)
    K3 = yaml.safe_load((FD / "kernel/00-kernel.yaml").read_text(encoding="utf-8")); al = K3["argument_layer"]; assert str(K3["version"]) == "1.3" and not al["records_without_moves"]
    ch = (f"The argument moves of the records that entered at v1.2 without moves ({', '.join('#' + str(x) for x in owed)}), each read in full and compressed into verbatim moves bound to its hash; "
          f"the argument layer now {al['moves']:,} moves from {al['records_with_moves']} records, {al['edges']:,} edges, no record without moves; T20 and T21 re-run, every structural test passing. "
          "SPXI packet reissued at v1.3. Map regenerated from the kernel; attached files replaced and re-hashed; the move builders attached as operator/v13-moves.zip. Hash and AXN re-derived.")
    da = " Version 1.3 (10 November 2026, in place) reads in full the records that entered at v1.2 and adds their argument moves."
    wa = " Version 1.3 (10 November 2026) reads in full each record that entered at v1.2 and compresses its argument into moves, so that every record the hologram holds carries its argument."
    p, q = reissue(n, title, body, ch, da, wa, files); moves[p] = q
ind = 1 if raw.startswith('{\n "') else (2 if raw.startswith('{\n  "') else None)
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, indent=ind) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
json.dump(moves, open(pathlib.Path(__file__).parent / "axn-moves-20261110-v13.json", "w"), ensure_ascii=False, indent=1)
