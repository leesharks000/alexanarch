#!/usr/bin/env python3
"""The version field returned to the archive's convention, a bare version (2026-11-18). From #1773 on, twelve records had their supersession
chains written into `version`, which the record page prints under the title. The author, 2026-11-18 11:44: "listing each version supersession
under the title on deposit cards is new, an introduced novelty rather than a preexisting convention, far as i know, and it's getting a bit
obnoxious esp with phainetai moi". The chains stay where they belong: previous_version, related_deposits and the version-series list.
Registry metadata only for sealed records (their minted bytes are untouched); for #1779 and #1783, reissued in place in the same commit and
not yet landed, the front matter is set to match and the hash and AXN re-derived at the same position and family."""
import json, hashlib, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))
moves_p = pathlib.Path(__file__).parent / "axn-moves-20261118-mpai12-dl11.json"; moves = json.loads(moves_p.read_text())
for d in R["deposits"]:
    v = str(d.get("version") or "")
    if d["deposit_number"] < 1773 or not re.search(r"supersedes|; |notebook", v): continue
    short = re.match(r"v[\d.]+", v).group(0)
    d.setdefault("modifications", []).append({"date": "2026-11-18", "field": "version", "was": v, "now": short,
        "reason": "the version field returned to a bare version; the supersession chain is carried by previous_version, related_deposits and the version series (the author, 2026-11-18 11:44)"})
    d["version"] = short
    if d["deposit_number"] in (1779, 1783):
        fp = ROOT / d["full_text_path"].lstrip("/"); s = fp.read_text(encoding="utf-8")
        assert s.count(f'version: "{v}"') == 1; s = s.replace(f'version: "{v}"', f"version: {short}")
        h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
        old_axn = d["axn"]
        d.update({"hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl,
                  "axn_reading": AX.axn_reading_from_clusters(cl), "full_text_chars": len(s)})
        fp.write_text(s, encoding="utf-8")
        dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
        if dp.exists(): dp.write_text(s, encoding="utf-8")
        for k, val in list(moves.items()):
            if val == old_axn: moves[k] = d["axn"]
    print(d["deposit_number"], short, d["axn"])
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
moves_p.write_text(json.dumps(moves, ensure_ascii=False, indent=1))
