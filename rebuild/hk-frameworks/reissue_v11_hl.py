#!/usr/bin/env python3
"""Reissue in place, at the author's words of 2026-11-09 (15:56 "counterfeit orthodoxies. check that work."; 15:58 on the stylometric work and the censuses;
16:00 "yes, lets read the remaining records and build"; 16:55 "lets address, decent pass, and version"): #1757 EA-HK-HISTLOGOS-01 v1.0 -> v1.1. The attached
files are replaced by the v1.1 build (the method of operational transmission in five instruments, fifteen records joined, the Counterfeit Orthodoxies join,
the rival's settlement step D5) and the file list re-hashed; the body is the v1.1 map, generated from the kernel; hash and AXN re-derived at the same
position and family, the prior hash, AXN and title kept in reissue_history.
   python3 rebuild/hk-frameworks/reissue_v11_hl.py <staged deposit-histlogos-v11 dir>"""
import json, hashlib, pathlib, shutil, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
ST = pathlib.Path(sys.argv[1]); N = 1757
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); D = {x["deposit_number"]: x for x in R["deposits"]}
WORD = ('Lee Sharks, 2026-11-09, on ChatGPT\'s reconstruction of v1.0 (attached): 15:55, the language of \'christian tradition\' "a super compressed inferential '
        'settlement colonizing the corpus of the nt"; 15:56, "counterfeit orthodoxies. check that work."; 15:57, that the frame "needs to detail more of its method '
        'for establishing operational transmission"; 15:58, "the stylometric work, the vast censuses of work - this is literary methdology that is drawing on things '
        'that are newly possible at this scale in the age of ai"; 16:00, "yes, lets read the remaining records and build"; 16:55, on the review of the v1.1 draft, '
        '"lets address, decent pass, and version".')
CHANGES = ("The method by which the framework establishes operational transmission, in five instruments read from their records: construction under fixed "
           "transforms (the unfoldings and foldings, #1414, #1415, #1416, #1511, #1532); blind reconstruction (#1486); frozen pre-registered operators and the "
           "append-only ledger (#1494, #1495, #1533, #1571); the suppression signature (#1496); measurement at corpus scale, the censuses and the stylometry "
           "(#1572, #1586, #1590, #1605, #1730, #1733). Each with controls marked run or specified, results at the status its record gives them, defeat "
           "conditions and the losses the records keep; the method set out bridge by bridge. Fifteen records joined, each read in full by a parallel reader. "
           "Counterfeit Orthodoxies joined (#978 the current state, #674 the prior; #65's seating carried as data). The rival's fifth disputed step, the "
           "settlement, in four objects, with Athanasius's Festal Letter 39 and Irenaeus, Against Heresies III.11, fetched and hashed; the flag "
           "SETTLEMENT_AS_CORPUS raised on the inference. At the review of the draft: M-D1 restored to #1576's four propositions; the several-maker accounts "
           "stated with their costs; the semantic challenges. Map regenerated from the kernel; attached files replaced and re-hashed. Hash and AXN re-derived.")
DESC = (" Version 1.1 (9 November 2026, in place) sets out the method by which the framework establishes operational transmission in five instruments "
        "(construction under fixed transforms, blind reconstruction, frozen operators, the suppression signature, measurement at corpus scale), each with its "
        "controls, results and recorded losses, and reads the settlement under which the corpus is filed as 'Christian' in four objects, joining Counterfeit Orthodoxies.")
WIKI = (" Version 1.1, the same day, sets out the method by which the framework establishes that a later text realizes an earlier one's operation: five "
        "instruments, from construction under fixed transforms to stylometry and census at corpus scale, each with its controls and the losses its records keep. "
        "It reads the settlement under which the New Testament corpus is filed as 'Christian' in four objects: the texts' operations, their competing "
        "appropriations (Irenaeus), one collection's boundary (Athanasius, 367 CE), and the later treatment of that configuration as the texts' own.")
d = D[N]; assert d["version"] == "v1.0", d["version"]
body = (ST / "body.md").read_text(encoding="utf-8"); title = body.split("\n", 1)[0][2:].strip()
assert title.endswith(" v1.1)"), title
FD = ROOT / f"files/AXN-{d['hex']}"
files = json.loads((ST / "files.json").read_text(encoding="utf-8"))
for f in files:
    src = ST / "files" / f["filename"]; dst = FD / f["filename"]; dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst)
    b = dst.read_bytes(); assert hashlib.sha256(b).hexdigest() == f["sha256"] and len(b) == f["bytes"], f["filename"]
assert sorted(p.relative_to(FD).as_posix() for p in FD.rglob("*") if p.is_file()) == sorted(f["filename"] for f in files), "unlisted file"
old = {f["filename"]: f["sha256"] for f in d["files"]}
changed = [f["filename"] for f in files if old.get(f["filename"]) != f["sha256"]]
cur = (ROOT / d["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
fm_end = cur.index("\n---\n", 4) + 5
fm = cur[:fm_end].replace(f'title: "{d["title"]}"', f'title: "{title}"').replace("\nversion: v1.0\n", "\nversion: v1.1\n")
assert f'title: "{title}"' in fm and "\nversion: v1.1\n" in fm
s = fm + "\n# " + title + "\n\n" + body
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
d.setdefault("reissue_history", []).append({"date": "2026-11-09", "from_version": "v1.0", "to_version": "v1.1", "hash_before_reissue": d["hash"],
    "axn_before_reissue": d["axn"], "title_before_reissue": d["title"], "reason": WORD, "changes": CHANGES + f" ({len(changed)} files new or re-hashed.)"})
prior = d["axn"]
d.update({"title": title, "version": "v1.1", "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl,
          "axn_reading": AX.axn_reading_from_clusters(cl), "files": files, "full_text_chars": len(s)})
d["description"] = d["description"].rstrip() + DESC
if d.get("wiki_article"): d["wiki_article"] = d["wiki_article"].rstrip() + WIKI
(ROOT / d["full_text_path"].lstrip("/")).write_text(s, encoding="utf-8")
dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(s, encoding="utf-8")
print(N, prior, "->", d["axn"], "| files changed:", len(changed), "of", len(files))
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump({prior: d["axn"]}, open(pathlib.Path(__file__).parent / "axn-moves-20261109-hl-v11.json", "w"), ensure_ascii=False, indent=1)
