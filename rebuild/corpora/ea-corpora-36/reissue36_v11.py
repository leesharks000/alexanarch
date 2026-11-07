#!/usr/bin/env python3
"""Reissue #1748 (EA-CORPORA-36) as v1.1, in place, at the operator's word of 2026-11-07 14:42 EST ("lets expand it to include all materials
well need for the reception study in one bundle"). The form of reissue34_v11.py: the canonical text is rewritten from the regenerated issue body
(title, version, keywords and body); its sha256 is the new hash; the AXN keeps its position (0C3F) and family (DATASET) and takes its glyphs from
the new hash; the prior hash and AXN go into reissue_history.
    python3 rebuild/corpora/ea-corpora-36/reissue36_v11.py"""
import json, hashlib, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
issue = (ROOT / "data/issue-bodies/EA-CORPORA-36-issue.md").read_text(encoding="utf-8")
def field(name):
    m = re.search(r"^### " + re.escape(name) + r"\n\n(.*?)(?=\n### |\Z)", issue, re.S | re.M); return m.group(1).strip()
title, desc, kw, body = field("Title"), field("Description"), [k.strip() for k in field("Keywords").split(",")], field("Body")
T = ROOT / "data/texts/AXN-0C3F-text.md"; old = T.read_text(encoding="utf-8")
fm_end = old.index("\n---\n", 4) + 5; fm = old[:fm_end]
fm = re.sub(r'^title: ".*"$', 'title: ' + json.dumps(title, ensure_ascii=False), fm, count=1, flags=re.M)
fm = re.sub(r"^version: v1\.0$", "version: v1.1", fm, count=1, flags=re.M)
fm = re.sub(r"^keywords:\n(?:  - .*\n)+", "keywords:\n" + "".join(f"  - {k}\n" for k in kw), fm, count=1, flags=re.M)
new = fm + "\n# " + title + "\n\n" + body.rstrip("\n") + "\n"
h = hashlib.sha256(new.encode("utf-8")).hexdigest()
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))
d = next(x for x in R["deposits"] if x["deposit_number"] == 1748)
assert d["version"] == "v1.0", d["version"]
prior = {"hash": d["hash"], "axn": d["axn"]}
glyph = A.axn_glyph_from_hash(h); cl = A.axn_clusters_from_hash(h)
d.setdefault("reissue_history", []).append({"date": "2026-11-07", "from_version": "v1.0", "to_version": "v1.1", "hash_before_reissue": prior["hash"],
    "axn_before_reissue": prior["axn"], "reason": "Lee Sharks, 2026-11-07 14:42 EST: \"lets expand it to include all materials well need for the reception study in one bundle\"; the study is his question of 14:13 EST: \"im particularly interested in how sappho became a jealous woman rather than a writer, which i believe begins with lucretius\".",
    "changes": "Part F added, eight seats 36/33–36/40 (Hermann 1816, Plutarch's Demetrius and Amatorius, Valerius Maximus and Appian, Gellius, Maximus of Tyre, Racine's Phèdre, Smollett, Wikipedia's 'Sappho 31'); fourteen cross-references added to Part C for the jealousy reading; seven absences added to Part E; title, description, keywords, body and wiki article to v1.1. The thirty-two seats of v1.0 unchanged."})
d.update({"title": title, "description": desc, "keywords": kw, "version": "v1.1", "hash": h, "axn_canonical": h, "emoji": glyph,
          "axn": A.compose_axn("0C3F", "DATASET", glyph), "clusters": cl, "axn_reading": A.axn_reading_from_clusters(cl)})
w = d["wiki_article"]
for a, b in [("Part C cross-references twenty-two loci", "Part C cross-references thirty-six loci"),
             ("Part E declares sixty-six works", "Part E declares seventy-three works"),
             ("and seventy-seven loci are verified in the text layers.", "and eighty-nine loci are verified in the text layers.")]:
    assert w.count(a) == 1, a; w = w.replace(a, b)
w += (" Version 1.1 (7 November 2026) adds Part F, eight seats for the reception study of how Sappho became a jealous woman: Gottfried Hermann's "
      "Elementa doctrinae metricae (1816), which states the jealousy reading as the sense of the poem's last line, answered the same year by Welcker; "
      "Plutarch's Demetrius and Amatorius; the Erasistratus story in Valerius Maximus and Appian; Gellius with Valerius Aedituus; Maximus of Tyre; "
      "Racine's Phèdre; Smollett's Roderick Random; and Wikipedia's 'Sappho 31', with Lucretius's division of the poem's symptoms and the other "
      "ancient witnesses entered by reference.")
d["wiki_article"] = w
T.write_text(new, encoding="utf-8"); (ROOT / "data/deposits/AXN-0C3F.md").write_text(new, encoding="utf-8")
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print("prior", prior["axn"], prior["hash"][:12], "→", d["axn"], h[:12])
