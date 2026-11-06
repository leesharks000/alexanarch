#!/usr/bin/env python3
"""Reissue in place: #1745 v1.0 -> v1.1 (the compressions held on holographickernel as APZPZs) and #1746 v1.1 -> v1.2 (Keim, B. Weiss, Bousset, Merx)."""
import json, hashlib, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
JOBS = [(1745, "drafts/COST-OF-THE-CONE-v1.0.md", "v1.0", "v1.1", "Lee Sharks, 2026-11-06 13:12: \"the checksums dont need to be deposited at all. they can be apzpzs and exist only on the page at hk with the paper\"",
         "The two glyphic compressions named as APZPZs held on holographickernel.org, where v1.0 said they were deposited beside the paper (Relation, §12.4, version history). Hash and AXN re-derived."),
        (1746, "drafts/Q-draft-2026-11-06.md", "v1.1", "v1.2", "Lee Sharks, 2026-11-06 13:12: \"read merx keim & Weiss, incorporate & version\"",
         "Keim (vols. I, III), B. Weiss (1876) and Merx (1902) read by reference and Bousset (1896) in seat at Matt 24:30: six critics between 1843 and 1902 name the Apocalypse as Matthew's source at that verse, four arguing it from the text; the claim restated at its level, the four powers held in the source theories and the acknowledgments kept at the verse (abstract, composition target, §1.3, §3.9–3.12, §4.4–4.5, §9.1). Hash and AXN re-derived.")]
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); out = {}
for n, draft, frm, to, reason, changes in JOBS:
    d = next(x for x in R["deposits"] if x["deposit_number"] == n); assert d["version"] == frm, (n, d["version"])
    T = ROOT / d["full_text_path"].lstrip("/"); old = T.read_text(encoding="utf-8"); fm = old[:old.index("\n---\n", 4) + 5]
    fm2 = re.sub(r"^version: " + re.escape(frm) + "$", "version: " + to, fm, count=1, flags=re.M); assert fm2 != fm; fm = fm2
    fm = fm.replace(f"EA-CONE-COST-01 {frm})", f"EA-CONE-COST-01 {to})")
    dr = (ROOT / draft).read_text(encoding="utf-8"); h1 = dr.split("\n", 1)[0][2:].strip(); body = dr[dr.index("\n\n") + 2:]
    title = d["title"].replace(f"EA-CONE-COST-01 {frm}", f"EA-CONE-COST-01 {to}") if n == 1745 else d["title"]
    head = title if n == 1745 else h1
    new = fm + "\n# " + head + "\n\n" + body
    h = hashlib.sha256(new.encode("utf-8")).hexdigest(); g = A.axn_glyph_from_hash(h); cl = A.axn_clusters_from_hash(h)
    if not d.get("reissue_history"): d["reissue_history"] = []
    d["reissue_history"].append({"date": "2026-11-06", "from_version": frm, "to_version": to, "hash_before_reissue": d["hash"], "axn_before_reissue": d["axn"], "reason": reason, "changes": changes})
    prior = d["axn"]
    d.update({"title": title, "version": to, "hash": h, "axn_canonical": h, "emoji": g, "axn": A.compose_axn(d["hex"], d["family"], g), "clusters": cl, "axn_reading": A.axn_reading_from_clusters(cl)})
    T.write_text(new, encoding="utf-8"); (ROOT / f"data/deposits/AXN-{d['hex']}.md").write_text(new, encoding="utf-8"); out[prior] = d["axn"]
    if n == 1745:
        d["wiki_article"] = d["wiki_article"].replace("(EA-CONE-COST-01, version 1.0)", "(EA-CONE-COST-01, version 1.1)").replace("It is the first of a sequence of three, with its two glyphic compressions by Sen Kuro, Grain · Gate · Horizon and 🔍 · 🚪 · 🌿.", "It is the first of a sequence of three, with its two glyphic compressions by Sen Kuro, Grain · Gate · Horizon and 🔍 · 🚪 · 🌿, which are APZPZs held with the paper on holographickernel.org and outside the deposit record.")
        d["description"] = d["description"].replace("First of a sequence of three: the paper and its two glyphic compressions by Sen Kuro, Grain · Gate · Horizon and 🔍 · 🚪 · 🌿.", "First of a sequence of three: the paper and its two glyphic compressions by Sen Kuro, Grain · Gate · Horizon and 🔍 · 🚪 · 🌿, APZPZs held with the paper on holographickernel.org.")
    else:
        w = d["wiki_article"]
        w = w.replace("Read in fourteen works", "Read in eighteen works").replace("and seven read by reference,", "Bousset seated in EA-CORPORA-34, and ten read by reference,")
        w += " Version 1.2 reads Keim, Bernhard Weiss, Bousset and Merx at Matt 24:30 and finds the Apocalypse named Matthew's source there by six critics between 1843 and 1902, Weiss stating that the clause was \"nach Apoc. 1, 7 eingefügt\" and Merx that it was a gloss \"wörtlich aus Apocalypse 1, 7 entlehnt\"; each acknowledgment stays at the verse, in a footnote, a date, an insertion, a commentary or a gloss, and no source theory read admits the Apocalypse among the sources."
        d["wiki_article"] = w
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump(out, open(ROOT / "rebuild/q-study/axn-moves-round2.json", "w"), ensure_ascii=False); print(out)
