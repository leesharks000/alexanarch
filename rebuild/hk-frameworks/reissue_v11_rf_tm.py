#!/usr/bin/env python3
"""Reissue in place, at the author's words of 2026-11-09 ("the hologram needs deeper density of compressed evidentiary claims and argumentation. it is
supposed to be a hologram of the whole"; "same as sappho"; "yes lets 1.1 on both"): #1755 EA-HK-REVFIRST-01 v1.0 -> v1.1 and #1756 EA-HK-TENTHMUSE-01
v1.0 -> v1.1. Each hologram's attached files are replaced by the v1.1 build (the kernel now carries 04-arguments.jsonl, the argument layer) and its file
list re-hashed; the body is the v1.1 map, generated from the kernel; hash and AXN re-derived at the same position and family, the prior hash, AXN and
title kept in reissue_history.
   python3 rebuild/hk-frameworks/reissue_v11_rf_tm.py <staged deposit-revfirst dir> <staged deposit-tenthmuse dir>"""
import json, hashlib, pathlib, shutil, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
STAGED = {1755: pathlib.Path(sys.argv[1]), 1756: pathlib.Path(sys.argv[2])}
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); D = {x["deposit_number"]: x for x in R["deposits"]}
WORD = ('Lee Sharks, 2026-11-09: 09:52, on an unprimed ChatGPT reading of the v1.0 hologram that reported the Josephus thesis withdrawn, "to my knowledge i '
        'have not withdrawn the josephus thesis - i have suspended advancing the argument"; 09:55, "the hologram needs deeper density of compressed evidentiary '
        'claims and argumentation. it is supposed to be a hologram of the whole"; 10:02, "same as sappho"; 10:08, "i would call it the current consensus '
        'reading"; 10:14, on the earlier records\' wording; 10:15, "yes lets 1.1 on both".')
CHANGES = {
 1755: ("The argument layer new (04-arguments.jsonl: every record of the framework read in full by parallel readers, its argument compressed into moves, each "
        "a verbatim quotation bound to its record's hash, joined by typed edges; tests T20, T21). The Josephus thesis held: #1217's relation to #639's and "
        "#1101's statements recoded from a withdrawal to a bound, both held at their tiers, the author's statement of 09:52 seated (held, advancement "
        "suspended). The working date of 66 CE (#1737) on its axis. The rival named the current consensus chronology. Map regenerated from the kernel; "
        "attached files replaced and re-hashed. Hash and AXN re-derived."),
 1756: ("The argument layer new (04-arguments.jsonl, as for #1755). The rival named the current consensus reading and carried with its dated making "
        "(#1752, #1748); the earlier records' wording kept as published and marked as their state (INV-8); the author's statements of 10:08 and 10:14 "
        "seated. #1484 read as repaired the same day. Map regenerated from the kernel; attached files replaced and re-hashed. Hash and AXN re-derived.")}
DESC = {1755: (" Version 1.1 (9 November 2026, in place) adds the argument layer, every record's argument compressed into verbatim moves joined by typed "
               "edges, and holds the Josephus thesis at the strengths its records give it, its advancement suspended by the author."),
        1756: (" Version 1.1 (9 November 2026, in place) adds the argument layer, every record's argument compressed into verbatim moves joined by typed "
               "edges, and names the rival the current consensus reading, carried with its dated making.")}
WIKI = {1755: (" Version 1.1, the same day, compresses the argument of every record into verbatim moves joined by typed edges, and holds the Josephus thesis "
               "at the strengths its records give it: bounded as an available reading the framework does not require, its advancement suspended by the "
               "author until the literary-genetic argument is more firmly established."),
        1756: (" Version 1.1, the same day, compresses the argument of every record into verbatim moves joined by typed edges, and names the rival the "
               "current consensus reading: available in antiquity and no consensus there, formed in the eighteenth century, written into the text in 1816 "
               "and consolidated in 1955.")}
moves = {}
for n, ST in STAGED.items():
    d = D[n]; assert d["version"] == "v1.0", (n, d["version"])
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
        "axn_before_reissue": d["axn"], "title_before_reissue": d["title"], "reason": WORD, "changes": CHANGES[n] + f" ({len(changed)} files new or re-hashed.)"})
    prior = d["axn"]
    d.update({"title": title, "version": "v1.1", "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl,
              "axn_reading": AX.axn_reading_from_clusters(cl), "files": files, "full_text_chars": len(s)})
    d["description"] = d["description"].rstrip() + DESC[n]
    if d.get("wiki_article"): d["wiki_article"] = d["wiki_article"].rstrip() + WIKI[n]
    (ROOT / d["full_text_path"].lstrip("/")).write_text(s, encoding="utf-8")
    dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
    if dp.exists(): dp.write_text(s, encoding="utf-8")
    moves[prior] = d["axn"]; print(n, prior, "->", d["axn"], "| files changed:", len(changed))
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump(moves, open(pathlib.Path(__file__).parent / "axn-moves-20261109-v11.json", "w"), ensure_ascii=False, indent=1)
