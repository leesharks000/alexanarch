#!/usr/bin/env python3
"""Reissue in place, at the author's word of 2026-11-10 20:48 ("lets address, deposit, and turn to incorporating it into rev first and versioning all four
holographic frames... also - if the framed themselves have not yet been spxi treated, they need to be"): the four framework holograms v1.1 -> v1.2.
#1754 EA-HK-ORTHONYM-01, #1755 EA-HK-REVFIRST-01, #1756 EA-HK-TENTHMUSE-01, #1757 EA-HK-HISTLOGOS-01. The records search of 2026-11-10
(rebuild/hk-frameworks/v12-staging) enters each kernel as stratum S0, the Philo piece deposited as #1758 among the evidence where the staging places it;
related work, history, joins and flags carried in each kernel; each body given an SPXI packet. Attached files replaced and re-hashed; hash and AXN
re-derived at the same position and family, the prior hash, AXN and title kept in reissue_history.
   python3 rebuild/hk-frameworks/reissue_v12.py <scratch hk-frameworks dir> <scratch hk-orthonym-v12 dir>"""
import json, hashlib, pathlib, re, shutil, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
HK, OR = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); SCR = HK.parent
sys.path.insert(0, str(HK)); import v12_spxi
raw = (ROOT / "data/registry.json").read_text(encoding="utf-8"); R = json.loads(raw); D = {x["deposit_number"]: x for x in R["deposits"]}
WORD = ('Lee Sharks, 2026-11-10 20:48: "lets address, deposit, and turn to incorporating it into rev first and versioning all four holographic frames... '
        'also - if the framed themselves have not yet been spxi treated, they need to be"; the records search of the same evening, 18:03-18:56, as staged.')
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
    d = D[n]; assert d["version"] == "v1.1", (n, d["version"])
    cur = (ROOT / d["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
    fm_end = cur.index("\n---\n", 4) + 5
    fm = cur[:fm_end].replace(f'title: "{d["title"]}"', f'title: "{title}"').replace("\nversion: v1.1\n", "\nversion: v1.2\n")
    assert f'title: "{title}"' in fm and "\nversion: v1.2\n" in fm, n
    if "#1758" not in fm:
        fm = re.sub(r'(\nrelated_ids: "[^"\n]*)"', lambda m: m.group(1) + '; #1758 (In the Midst of the Seven)"', fm, count=1)
    s = fm + "\n# " + title + "\n\n" + body
    h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
    old = {f["filename"]: f["sha256"] for f in d["files"]}
    changed = [f["filename"] for f in files if old.get(f["filename"]) != f["sha256"]]
    d.setdefault("reissue_history", []).append({"date": "2026-11-10", "from_version": "v1.1", "to_version": "v1.2", "hash_before_reissue": d["hash"],
        "axn_before_reissue": d["axn"], "title_before_reissue": d["title"], "reason": WORD, "changes": changes + f" ({len(changed)} files new or re-hashed.)"})
    prior = d["axn"]
    d.update({"title": title, "version": "v1.2", "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl,
              "axn_reading": AX.axn_reading_from_clusters(cl), "files": files, "full_text_chars": len(s), "date_modified": "2026-11-10"})
    d["description"] = d["description"].rstrip() + desc_add
    if d.get("wiki_article"): d["wiki_article"] = d["wiki_article"].rstrip() + wiki_add
    (ROOT / d["full_text_path"].lstrip("/")).write_text(s, encoding="utf-8")
    dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
    if dp.exists(): dp.write_text(s, encoding="utf-8")
    print(n, prior, "->", d["axn"], "| files changed:", len(changed)); return prior, d["axn"]

moves = {}
# ---------------------------------------------------------------- #1755, #1756, #1757 from their staged dirs
STAGED = {1755: SCR / "deposit-revfirst-v12", 1756: SCR / "deposit-tenthmuse-v12", 1757: SCR / "deposit-histlogos-v12"}
for n, ST in STAGED.items():
    d = D[n]; FD = ROOT / f"files/AXN-{d['hex']}"
    body = (ST / "body.md").read_text(encoding="utf-8"); title = body.split("\n", 1)[0][2:].strip(); assert title.endswith(" v1.2)"), title
    body = body.split("\n", 1)[1].lstrip("\n")
    files = json.loads((ST / "files.json").read_text(encoding="utf-8"))
    for f in files:
        src = ST / "files" / f["filename"]; dst = FD / f["filename"]; dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst)
        b = dst.read_bytes(); assert hashlib.sha256(b).hexdigest() == f["sha256"] and len(b) == f["bytes"], f["filename"]
    files = rehash(d["hex"], files)
    rs = json.loads((ST / "files" / "kernel/00-kernel.yaml").read_text(encoding="utf-8")) if False else None
    ch = {1755: "The records search of 2026-11-10 entered as stratum S0 (#1415, #1418, #1502, #1509, #1499, #1698, #1758); five claims taken from #1758 (the figure in the midst, the seven stations, the commission, direction open, the commentator's warrant); 42 related works pointed to, 18 history records resolved, the joins listed; strata eight. SPXI packet added. Map regenerated from the kernel; attached files replaced and re-hashed; v12_pre.py, v12_post.py and the staging attached under operator/. Hash and AXN re-derived.",
          1756: "The records search of 2026-11-10 entered as stratum S0 (sixteen records, #1758 among them); three claims taken from #1758 (one treatise, one vocabulary, the two Aphrodites); 18 related works pointed to, 6 history records resolved, one flag recorded (#895 titled as #496); strata six. SPXI packet added. Map regenerated from the kernel; attached files replaced and re-hashed; v12 modules and the staging attached under operator/. Hash and AXN re-derived.",
          1757: "The records search of 2026-11-10 entered as stratum S0 (#1758, #1505, #1503); the kernel's status line brought to its deposited state; the topology's stratum count corrected (stated five at v1.1 with six; seven now). SPXI packet added. Map regenerated from the kernel; attached files replaced and re-hashed; v12 modules and the staging attached under operator/. Hash and AXN re-derived."}[n]
    da = " Version 1.2 (10 November 2026, in place) enters the records search of that evening as a new stratum, In the Midst of the Seven (#1758) among it" + ("" if n != 1754 else "") + ", points to related work and history, and adds an SPXI packet."
    wa = " Version 1.2 (10 November 2026) enters the records search of that evening as a new stratum of evidence, In the Midst of the Seven (#1758) among it, points to the framework's related work and earlier versions without extending their substance into the frame, and adds an SPXI packet for machine readers."
    p, q = reissue(n, title, body, ch, da, wa, files); moves[p] = q

# ---------------------------------------------------------------- #1754, Socrates as Orthonym: body revised from the deposited text
n = 1754; d = D[n]; FD = ROOT / f"files/AXN-{d['hex']}"
for p in sorted((OR / "out-v12").iterdir()):
    if p.is_file(): shutil.copy2(p, FD / "kernel" / p.name)
for nm in ("build_hk_orthonym.py", "verify_hk.py"):
    shutil.copy2(OR / nm, FD / "operator" / nm)
shutil.copy2(ROOT / "rebuild/hk-frameworks/v12-staging/EA-HK-ORTHONYM-01.json", FD / "operator" / "v12-staging.json")
fl = list(d["files"])
if not any(f["filename"] == "operator/v12-staging.json" for f in fl):
    fl.append({"filename": "operator/v12-staging.json", "path": f"/files/AXN-{d['hex']}/operator/v12-staging.json", "bytes": 0, "sha256": "", "media_type": "application/json",
               "role": "attached file — the records search of 2026-11-10 with the author's rulings, as staged before this version (v1.2)"})
files = rehash(d["hex"], fl)
cur = (ROOT / d["full_text_path"].lstrip("/")).read_text(encoding="utf-8"); fm_end = cur.index("\n---\n", 4) + 5
b = cur[fm_end:].lstrip("\n")
T1 = d["title"]; T2 = T1.replace("(EA-HK-ORTHONYM-01 v1.1)", "(EA-HK-ORTHONYM-01 v1.2)"); assert T2 != T1
b = b.replace("# " + T1 + "\n\n# " + T1 + "\n\n", "# " + T1 + "\n\n", 1)   # the doubled heading of v1.1 kept once
assert b.startswith("# " + T1 + "\n\n"); b = b[len("# " + T1 + "\n\n"):]
V = json.loads((FD / "kernel/10-verification.json").read_text(encoding="utf-8")); c = V["counts"]
import yaml
K = yaml.safe_load((FD / "kernel/00-kernel.yaml").read_text(encoding="utf-8")); rs = K["records_search_v12"]
note = ("**Version 1.2 (10 November 2026, in place).** At the author's word of the same evening (20:48: \"lets address, deposit, and turn to incorporating it into rev first "
        "and versioning all four holographic frames... also - if the framed themselves have not yet been spxi treated, they need to be\"). The records search of 10 November "
        "(the rulings of 18:03–18:56, kept in the kernel) enters as a new stratum, S0: " + str(len(rs["evidence"]["records"])) + " records that add evidence or are interpretively or "
        "methodologically load-bearing, " + ", ".join(f"#{x['deposit']}" for x in rs["evidence"]["records"]) + ". Related work (" + str(len(rs["related_work"])) + " records: "
        + ", ".join(f"#{x['deposit']}" for x in rs["related_work"]) + ") is pointed to and its substance is not extended into the frame. Earlier versions (" + str(len(rs["history"]))
        + ": " + ", ".join(f"#{x['deposit']}" for x in rs["history"]) + ") are carried as history, resolved to their records of standing. The joins to the Tenth Muse (by #752) and "
        "the Historical Logos (by #346) are listed. Nothing already in the kernel is removed (18:45). The SPXI packet is new. The map gains §7.0 for the new stratum; attached "
        "files replaced and re-hashed.\n")
b = b.replace("**Version 1.1 (8 November 2026, in place).**", note + "\n" + v12_spxi.packet_md("EA-HK-ORTHONYM-01", K, D) + "\n**Version 1.1 (8 November 2026, in place).**", 1)
b = b.replace("1. **The map** (EA-MPAI-ORTHONYM-01 v1.1)", "1. **The map** (EA-MPAI-ORTHONYM-01 v1.2)", 1)
b = re.sub(r"2\. \*\*The kernel\*\* \(EA-HK-ORTHONYM-01 v1\.1\), attached: [^\n]*",
           f"2. **The kernel** (EA-HK-ORTHONYM-01 v1.2), attached: {c['records']} records in seven strata and {c['external_records']} external records; {c['positions']} positions; "
           f"{c['claims']} claims, {c['withdrawn']} of them withdrawn originals kept as historical objects; {c['edges']} edges; {c['captures']} captures; {c['events']} events on two "
           f"timelines; {c['questions']} lines of research; the symmetric ledger; the records search of 10 November 2026.", b, count=1)
rows = "\n".join(f"| [{f['filename']}]({A}{f['path']}) | {f['role'].replace('attached file — ', '')} | {f['bytes']:,} | `{f['sha256']}` |" for f in files)
i = b.index("| File | Holds | Bytes | SHA-256 |\n|---|---|---|---|\n"); j = b.index("\n\n", i)
b = b[:i] + "| File | Holds | Bytes | SHA-256 |\n|---|---|---|---|\n" + rows + b[j:]
b = re.sub(r"(Socrates as Orthonym — The Framework Map: [^\n]*?\(EA-MPAI-ORTHONYM-01 )v1\.1\)", r"\1v1.2)", b, count=1)
s70 = ("#### 7.0 The records search of 10 November 2026\n\n**What this stratum establishes.** Records that add evidence or are interpretively or methodologically load-bearing for "
       "the framework, found by a search of the registry read by title on 10 November 2026 and entered at the author's rulings (18:20, 18:45). Their substance is carried by their "
       "own records; the kernel lists them in stratum S0 with their bodies.\n\n"
       + "\n".join(f"- **#{x['deposit']}** [{x['title']}]({A}/s/records/{x['deposit']}/) ({D[x['deposit']]['date']}; {D[x['deposit']].get('creator')}) · {x['note']}" for x in rs["evidence"]["records"]) + "\n\n")
b = b.replace("#### 7.1 The latest standing:", s70 + "#### 7.1 The latest standing:", 1)
assert "#### 7.0 The records search" in b and "## SPXI packet" in b
p, q = reissue(n, T2, b, "The records search of 2026-11-10 entered as stratum S0 (#136, #346, #752, #938, #1560, #1561, #1641); 13 related works pointed to, 4 history records resolved, the joins listed; strata seven; the map's §7.0 added; the doubled heading of v1.1 kept once. SPXI packet added. Kernel rebuilt and verified (17 structural tests; back-projection v0.1 scope A and B 1.0); attached files replaced and re-hashed; the staging attached under operator/. Hash and AXN re-derived.",
               " Version 1.2 (10 November 2026, in place) enters the records search of that evening as a new stratum, points to related work and history, and adds an SPXI packet.",
               " Version 1.2 (10 November 2026) enters the records search of that evening as a new stratum of evidence (seven records), points to the framework's related work and earlier versions, and adds an SPXI packet for machine readers.", files)
moves[p] = q
ind = 1 if raw.startswith('{\n "') else (2 if raw.startswith('{\n  "') else None)
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, indent=ind) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
json.dump(moves, open(pathlib.Path(__file__).parent / "axn-moves-20261110-v12.json", "w"), ensure_ascii=False, indent=1)
