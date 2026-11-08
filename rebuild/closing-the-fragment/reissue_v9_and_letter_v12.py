#!/usr/bin/env python3
"""Reissue in place: #1749 Closing the Fragment v8 -> v9, and #1750 the open letter v1.1 -> v1.2, at the author's word of 2026-11-08 ("the word"),
on the reconciliation of the reviewed file: the referees read v6; the corrected manuscript of 27 July (CRJ_Closing_the_Fragment_v8.docx in the author's
July numbering) reached the editor before upload; the ScholarOne upload of 30 July carried CRJ_Closing_the_Fragment_v6.docx with a figure count of two.
Hash and AXN re-derived at the same position and family, the prior hash and AXN kept in reissue_history.
   python3 rebuild/closing-the-fragment/reissue_v9_and_letter_v12.py <v9 text> <letter v1.2 text>"""
import json, hashlib, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
V9, LT = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))
D = {x["deposit_number"]: x for x in R["deposits"]}
WORD = ("Lee Sharks, 2026-11-08: \"jesus christ. i had already corrected the main misnamed figure. lets verify everything. this requires reconciliation against "
        "the reviewers and an updated letter.\"; \"and this was not known to the archive *because i forewent my normal practice of publicly versioning because of "
        "the manuscript submission and their policies*\"; \"sloppiness in their own editorial chain retroactively introduced errors into my own which now require "
        "further labor to correct\"; on the reconciliation, \"the word\"")
WORD750 = WORD + ("; \"im not putting up with it anymore, im not pandering to their pipeline, and im not playing the game\"; \"its ai-mediation status is "
        "everywhere disclosed. i neglected a specific manuscript disclosure but there is no suggestion that publishing the manuscript would have falsely presented "
        "human-only mediation of an ai-assisted work\"; \"if they had asked google themselves, instead of complaining about reproducibility ... they would have known "
        "that\"; \"they could have gotten out in front.\"")
def reissue(n, path, frm, to, reason, changes, extra):
    d = D[n]; assert d["version"] == frm, (n, d["version"])
    s = path.read_text(encoding="utf-8"); assert f"\nversion: {to}\n" in s and f"\nhex: {d['hex']}\n" in s
    h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = A.axn_glyph_from_hash(h); cl = A.axn_clusters_from_hash(h)
    d.setdefault("reissue_history", []).append({"date": "2026-11-08", "from_version": frm, "to_version": to, "hash_before_reissue": d["hash"],
                                                "axn_before_reissue": d["axn"], "reason": reason, "changes": changes})
    prior = d["axn"]
    d.update({"version": to, "hash": h, "axn_canonical": h, "emoji": g, "axn": A.compose_axn(d["hex"], d["family"], g), "clusters": cl,
              "axn_reading": A.axn_reading_from_clusters(cl)})
    extra(d)
    (ROOT / d["full_text_path"].lstrip("/")).write_text(s, encoding="utf-8"); (ROOT / f"data/deposits/AXN-{d['hex']}.md").write_text(s, encoding="utf-8")
    print(n, prior, "->", d["axn"]); return prior, d["axn"]
def x749(d):
    d["title"] = "Closing the Fragment: Sappho 31 and the Composition Layer as a Surface of Classical Reception (v9)"
    o = "Version 8 (7 November 2026, in place) withdraws v7's compilation account and restores v6's finding that the output was composed, corrected."
    assert d["description"].endswith(o)
    d["description"] += (" Version 9 (8 November 2026, in place) reconciles the article against the file its referees read: the reports were written on v6, and "
        "the corrected manuscript of 27 July, which had withdrawn v6's misnamed Figure 2 and shown the July capture under its AI Overview label, reached the editor "
        "before upload; v9 restores those corrections, prints the June frames uncropped where the registry holds them, and gives the frame's history from the "
        "registry's record of July.")
    d["wiki_article"] += (" Version 9 (8 November 2026) records that the referees read the file first sent: a corrected manuscript of 27 July, forwarded by the "
        "editor before upload, had already withdrawn the figure Reviewer 2 found showing another query, and the upload of 30 July carried the earlier file.")
OLDA = "It closes on the image of an ark built early, with its leaks recorded and the names of the people who found them, built for the work and for those it can carry."
def x750(d):
    w = d["wiki_article"]; assert OLDA in w
    d["wiki_article"] = w.replace(OLDA, "Version 1.2 (8 November 2026) adds that the figure the reports found showing another query had been withdrawn by the author "
        "before upload, in a corrected manuscript the editor forwarded, while the file uploaded and read was the one it replaced; that the work's AI mediation was "
        "disclosed on every record of the archive the manuscript names; and that the reports asked for reproducibility without asking the surface the manuscript "
        "studies. " + OLDA)
    d["description"] = d["description"].rstrip() + (" Version 1.2 (8 November 2026, in place): the figure the reports found had been corrected before upload and the "
        "superseded file was read (§§2.1, 2.4, 8.3); the AI mediation disclosed throughout (§2.2); reproducibility by asking (§10).")
    for x in d["related_deposits"]:
        if x["deposit"] == 1749: x["relation"] = "Closing the Fragment (v7 to v9), whose Appendix A answers the referee reports and whose B.7 records the reconciliation of the reviewed file"
moves = {}
moves.update([reissue(1749, V9, "v8", "v9", WORD,
    "Reconciled against the file the referees read: note on this version, §5.4 (paragraphs 1 and 3), the June and July figures (kenotic and 15 June frames "
    "uncropped from the registry; the 27 July capture unexpanded under its AI Overview label restored as Fig. 7; Figs 8–9), A.1(4), A.2 (figure 2, numbering, "
    "screenshots, AI-use statement), A.3 rewritten to the registry's July record, B.7 new, production statement. Hash and AXN re-derived.", x749)])
moves.update([reissue(1750, LT, "v1.1", "v1.2", WORD750,
    "§2.1 (the figure corrected before upload; the superseded file read; the portal's count), §2.2 (the AI mediation disclosed throughout), §2.4 new (the labor "
    "the editorial chain added), §7.2, §8.3 rewritten to the record, §9.1, §10 (reproducibility by asking; out in front), signature dated. Hash and AXN re-derived.", x750)])
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump(moves, open(ROOT / "rebuild/closing-the-fragment/axn-moves-20261108.json", "w"), ensure_ascii=False, indent=1)
