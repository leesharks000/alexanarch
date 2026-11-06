#!/usr/bin/env python3
"""Reissue #1743 as v1.1 and #1742 as v1.2, in place, from the repaired drafts (repair_drafts.py). The canonical text is the
frontmatter (title and version updated) + the draft's body under '# Title (ID vN)'; the AXN keeps its position and family and
takes its glyphs from the new hash; the prior hash and AXN go into reissue_history."""
import json, hashlib, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
WORD = "Lee Sharks, 2026-11-06 (11:07): \"so we need factual repairs versioned in place and the ea-corpora for q - lets do those as one bundle.\""
JOBS = [
 (1743, "drafts/3I-ATLAS-PUBLIC-draft-2026-11-06.md", "EA-3I-ATLAS-PUBLIC-01", "v1.0", "v1.1",
  "Three factual repairs on the composers' findings, each checked against its source: MeerKAT's technosignature search added as a fourth published search (ATel #17499: 0.17 W over 900-1670 MHz, its 23,689 signals judged interference); the hydroxyl line described as the comet's absorption and emission (absorption from 24 October 2025, emission on 11 and 12 November, ATel #17499); probabilities for four of Loeb's anomalies in the April essay, where v1.0 said each. A version note added at the end. Hash and AXN re-derived from the new bytes."),
 (1742, "drafts/3I-ATLAS-SIGNAL-SEARCH-draft-2026-11-03.md", "EA-3I-ATLAS-NOTEBOOK-01", "v1.1", "v1.2",
  "Factual repairs on the composers' findings (§13.7): MeerKAT's search added as a fourth (§2.1, §9.3, §9.6; ATel #17499); probabilities for four of Loeb's anomalies (§1.3); PER-D cited under rubric v1.1, #1694 §3.9 (§9.10); the SPXI packet at v1.2. Hash and AXN re-derived from the new bytes."),
]
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))
for n, draft, ident, frm, to, changes in JOBS:
    d = next(x for x in R["deposits"] if x["deposit_number"] == n)
    assert d.get("version") == frm, (n, d.get("version"))
    T = ROOT / d["full_text_path"].lstrip("/"); old = T.read_text(encoding="utf-8")
    fm_end = old.index("\n---\n", 4) + 5; fm = old[:fm_end]
    dr = (ROOT / draft).read_text(encoding="utf-8"); h1 = dr.split("\n", 1)[0][2:].strip(); body = dr[dr.index("\n\n") + 2:]
    title = f"{h1} ({ident} {to})"
    fm = re.sub(r'^title: ".*"$', 'title: ' + json.dumps(title, ensure_ascii=False), fm, count=1, flags=re.M)
    fm2 = re.sub(r"^version: " + re.escape(frm) + "$", "version: " + to, fm, count=1, flags=re.M); assert fm2 != fm; fm = fm2
    new = fm + "\n# " + title + "\n\n" + body
    h = hashlib.sha256(new.encode("utf-8")).hexdigest(); assert h != d["hash"]
    glyph = A.axn_glyph_from_hash(h); cl = A.axn_clusters_from_hash(h)
    d.setdefault("reissue_history", None)
    if not d["reissue_history"]: d["reissue_history"] = []
    d["reissue_history"].append({"date": "2026-11-06", "from_version": frm, "to_version": to, "hash_before_reissue": d["hash"],
        "axn_before_reissue": d["axn"], "reason": WORD, "changes": changes})
    prior = d["axn"]
    d.update({"title": title, "version": to, "hash": h, "axn_canonical": h, "emoji": glyph,
              "axn": A.compose_axn(d["hex"], d["family"], glyph), "clusters": cl, "axn_reading": A.axn_reading_from_clusters(cl)})
    T.write_text(new, encoding="utf-8"); (ROOT / f"data/deposits/AXN-{d['hex']}.md").write_text(new, encoding="utf-8")
    print(n, prior, "->", d["axn"])
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
