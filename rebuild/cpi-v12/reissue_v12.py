#!/usr/bin/env python3
"""Reissue in place: #1766 Critique of Pure Inference, v1.0 -> v1.2, at the author's word of 2026-11-14 09:38
("lets address this, work it into the whole cpi, and run the versioning pipeline on the deposit"), EA-CORPORA-38 (#1768)
being on main. v1.1 was a working draft and was not deposited. The text is rebuild/cpi-v12/Critique-of-Pure-Inference-v1.2.md
(build_v12.py, from the deposited v1.0 text). Hash and AXN re-derived at the same position and family; the prior hash, AXN
and title kept in reissue_history.   python3 rebuild/cpi-v12/reissue_v12.py"""
import json, hashlib, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
raw = (ROOT / "data/registry.json").read_text(encoding="utf-8"); R = json.loads(raw); D = {x["deposit_number"]: x for x in R["deposits"]}
n = 1766; d = D[n]; assert d["version"] == "v1.0", d["version"]
H = pathlib.Path(__file__).parent; s = (H / "Critique-of-Pure-Inference-v1.2.md").read_text(encoding="utf-8")
for chk in ("\nversion: v1.2\n", "v1.2 (14 November 2026, in place)", "### 11.6 The witnesses between: what reception does", "5a. **Carry the route"):
    assert chk in s, chk
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = A.axn_glyph_from_hash(h); cl = A.axn_clusters_from_hash(h)
d.setdefault("reissue_history", []).append({"date": "2026-11-14", "from_version": "v1.0", "to_version": "v1.2", "hash_before_reissue": d["hash"], "axn_before_reissue": d["axn"],
    "title_before_reissue": d["title"],
    "reason": 'Lee Sharks, 2026-11-13: "yes - part of cpi. this is a more substantial work"; 2026-11-14 09:20: "lets keep building the expanded reception history pass while we wait. after that lands well version cpi"; 09:38: "lets address this, work it into the whole cpi, and run the versioning pipeline on the deposit"',
    "changes": ("Adds §11.5 (logic complete since Aristotle) and §11.6 (the witnesses between), read from EA-CORPORA-38 (#1768) and revised on two reviews by ChatGPT (LABOR): six operations (O1–O6) "
                "whose relations reception preserves or severs, from Alexander and Philoponus through Boethius, Ibn Sīnā, the Nyāya, Meier, Kant 1762, Hegel, Peirce, Frege and Carroll; the requirement "
                "to carry a premise's route argued from §3 (11.6.1a) and added to the protocol as §11.3 step 5a; a pointer in §11.0j to Alexander's distinction of method from a stock of reductions; "
                "the seats named in the §11.2 table; a sentence in the abstract; Appendix B entries for v1.1 (the working draft, not deposited) and v1.2. v1.1's reading of Jäsche's \"nicht zweifelhaft\" "
                "as a dropped hedge withdrawn. Nothing in v1.0 removed. Hash and AXN re-derived.")})
prior = d["axn"]
d.update({"version": "v1.2", "hash": h, "axn_canonical": h, "emoji": g, "axn": A.compose_axn(d["hex"], d["family"], g), "clusters": cl,
          "axn_reading": A.axn_reading_from_clusters(cl), "full_text_chars": len(s), "date_modified": "2026-11-14"})
d["description"] = d["description"].rstrip() + (" Version 1.2 (14 November 2026, in place) adds the reception history of §11.5–11.6, read from the witnesses seated for it in EA-CORPORA-38 (#1768). It follows six operations of "
    "the Peripatetic logic, among them the companions' modal rule, Theophrastus's added moods and the distinction between a method and a stock of reduced arguments, from Alexander to Frege. It shows them "
    "preserved, reassigned, rejected and made productive again. Kant's 1762 reduction of the fourth figure reproduces the Theophrastean placement without the name, and the account of logic in which the "
    "completion sentence of 1787 stands has no place for that placement as a contribution.")
if d.get("wiki_article"):
    d["wiki_article"] = d["wiki_article"].rstrip() + (" Version 1.2 (14 November 2026) adds a reception history read from witnesses seated for it. Alexander of Aphrodisias and Philoponus carry the "
        "companions' arguments; Boethius names Theophrastus and Eudemus for five added moods; Meier's handbook teaches them as Galen's figure; Kant in 1762 reduces that figure to the first, where Theophrastus "
        "had placed the moods; Peirce restores the name; and the Nyāyasūtra serves as the control, keeping doubt and purpose in the inquiry while excluding them from the proof.")
for k in ["Theophrastus", "Alexander of Aphrodisias", "Philoponus", "Boethius", "fourth figure", "Peirce", "Frege", "Nyāya", "Ibn Sīnā", "reception history"]:
    if k not in d["keywords"]:
        d["keywords"].append(k)
rel = d.setdefault("related_deposits", [])
if not any(r.get("deposit") == 1768 for r in rel):
    rel.append({"deposit": 1768, "relation": "EA-CORPORA-38, the seating of the witnesses read in §11.5–11.6"})
(ROOT / d["full_text_path"].lstrip("/")).write_text(s, encoding="utf-8"); dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists():
    dp.write_text(s, encoding="utf-8")
ind = 1 if raw.startswith('{\n "') else (2 if raw.startswith('{\n  "') else None)
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, indent=ind) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
json.dump({prior: d["axn"]}, open(H / "axn-moves-20261114-v12.json", "w"), ensure_ascii=False, indent=1)
print(n, prior, "->", d["axn"])
