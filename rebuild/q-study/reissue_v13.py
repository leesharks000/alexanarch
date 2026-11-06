#!/usr/bin/env python3
"""Reissue in place: #1746 v1.2 -> v1.3 (the superseded v1.1 table of §3.11 and its paragraph removed)."""
import json, hashlib, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))
d = next(x for x in R["deposits"] if x["deposit_number"] == 1746); assert d["version"] == "v1.2"
T = ROOT / d["full_text_path"].lstrip("/"); old = T.read_text(encoding="utf-8"); fm = old[:old.index("\n---\n", 4) + 5]
fm2 = re.sub(r"^version: v1\.2$", "version: v1.3", fm, count=1, flags=re.M); assert fm2 != fm
dr = (ROOT / "drafts/Q-draft-2026-11-06.md").read_text(encoding="utf-8"); h1 = dr.split("\n", 1)[0][2:].strip(); body = dr[dr.index("\n\n") + 2:]
new = fm2 + "\n# " + h1 + "\n\n" + body
h = hashlib.sha256(new.encode("utf-8")).hexdigest(); g = A.axn_glyph_from_hash(h); cl = A.axn_clusters_from_hash(h)
d["reissue_history"].append({"date": "2026-11-06", "from_version": "v1.2", "to_version": "v1.3", "hash_before_reissue": d["hash"], "axn_before_reissue": d["axn"],
  "reason": "The v1.2 text carried the v1.1 table of §3.11 and the paragraph under it beside the table and paragraph that supersede them, found while drafting the Revelation = Q packet",
  "changes": "The superseded table and paragraph (\"One critic tested the extant book…\"; \"admission twice more\") removed; the opening of §3.9 tidied; version history entry added. No finding changed. Hash and AXN re-derived."})
prior = d["axn"]
d.update({"version": "v1.3", "hash": h, "axn_canonical": h, "emoji": g, "axn": A.compose_axn(d["hex"], d["family"], g), "clusters": cl, "axn_reading": A.axn_reading_from_clusters(cl)})
T.write_text(new, encoding="utf-8"); (ROOT / f"data/deposits/AXN-{d['hex']}.md").write_text(new, encoding="utf-8")
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump({prior: d["axn"]}, open(ROOT / "rebuild/q-study/axn-moves-v13.json", "w"), ensure_ascii=False); print(prior, "->", d["axn"])
