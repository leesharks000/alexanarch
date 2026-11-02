#!/usr/bin/env python3
"""repair_mcknight_20261102.py — a mislabelled citation repaired in seat 32/11 (legitimately-many-wanted) of EA-CORPORA-32 v1.1
(#1732). The declaration named the 1978 commentator in the Masters exchange "Stephen A. McKnight"; the volume indexes of Political
Theory (open on the Internet Archive: sim_political-theory_1978_6_index, 1979_7_index) give "McKNIGHT, CHRISTOPHER, 'On Masters,
"The Case of Aristotle's Missing Dialogues"' [Communication] 247" (vol. 6, 1978), with Chroust's communication at 7: 537 and
Masters's reply "On Chroust: A Reply" at 7: 545 (1979). The entry is corrected and given its pages. The seat's MANIFEST changes,
so its AXN is re-derived at the same hex and family (#1732, 0BE6, ORIGINAL), the prior form appended to `axn_prior` with its
manifest hash; the indexes take the new AXN and text; the registry entry for #1732 records the correction (record_modification).
The deposited text of #1731 and #1732 is not edited: canonical bytes are immutable, and the correction lives in the registry and
the seat.
    python3 rebuild/corpora/ea-corpora-32/repair_mcknight_20261102.py [--apply]"""
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
from record_modification import touch
SEAT = ROOT / "data/corpora/legitimately-many-wanted"
OLD_A = "Roger D. Masters; Stephen A. McKnight; Anton-Hermann Chroust"
NEW_A = "Roger D. Masters; Christopher McKnight; Anton-Hermann Chroust"
OLD_T = "the exchange on the authorship of the Aristotelian corpus (Masters 1977; McKnight 1978; Chroust 1979; Masters 1979)"
NEW_T = ("the exchange on the authorship of the Aristotelian corpus: Masters, \"The Case of Aristotle's Missing Dialogues: Who Wrote the Sophist, "
         "the Statesman, and the Politics?\", Political Theory 5 (1977), p. 31; McKnight, \"On Masters, 'The Case of Aristotle's Missing Dialogues'\", "
         "6 (1978), p. 247; Chroust, \"On Masters's 'The Case of Aristotle's Missing Dialogues'\", 7 (1979), p. 537; Masters, \"On Chroust: A Reply\", 7 (1979), p. 545")
WHY = ("mislabelled citation repaired: the 1978 commentator is Christopher McKnight (Political Theory 6, 1978, p. 247, per the open volume index), "
       "not Stephen A. McKnight; titles and pages of the four pieces added")
FILES = [SEAT / "declared/absence.json", SEAT / "declared/absence.md", SEAT / "source.json", ROOT / "data/api/corpora.json",
         ROOT / "datasets/corpora/corpora.json", ROOT / "rebuild/corpora/ea-corpora-32/absences32_wanted.py"]
apply = "--apply" in sys.argv
for f in FILES:
    t = f.read_text(encoding="utf-8")
    n = t.count(OLD_A), t.count(OLD_T)
    print(f.relative_to(ROOT), "names", n[0], "titles", n[1])
    assert n[0] >= 1, f
    if apply:
        f.write_text(t.replace(OLD_A, NEW_A).replace(OLD_T, NEW_T.replace('"', '\\"') if f.suffix in (".json", ".py") else NEW_T), encoding="utf-8")
if not apply:
    sys.exit(0)
for f in FILES:
    if f.suffix == ".json":
        json.loads(f.read_text(encoding="utf-8"))  # still valid
m = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(SEAT).as_posix()}" for p in sorted(SEAT.rglob('*')) if p.is_file() and p.name not in ('MANIFEST.sha256', 'source.json')]
(SEAT / "MANIFEST.sha256").write_text("\n".join(m) + "\n")
h = hashlib.sha256((SEAT / "MANIFEST.sha256").read_bytes()).hexdigest()
reg = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))
d = next(x for x in reg["deposits"] if x["deposit_number"] == 1732)
a = A.derive_axn(h, d["hex"], "ORIGINAL")
sj = SEAT / "source.json"; s = json.loads(sj.read_text(encoding="utf-8"))
old_a, old_h = s["axn"], s["axn_basis"]["sha256"]
prior = s.get("axn_prior") or []
prior = [prior] if isinstance(prior, dict) else prior
prior.append({"axn": old_a, "manifest_sha256": old_h, "deposit": 1732, "until": "2026-11-02", "why": WHY})
s["axn_prior"] = prior; s["axn"] = a; s["axn_basis"]["sha256"] = h; s["axn_basis"]["repaired"] = "2026-11-02"
sj.write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
for f, key in ((ROOT / "data/api/corpora.json", "corpora"), (ROOT / "datasets/corpora/corpora.json", "seats")):
    j = json.loads(f.read_text(encoding="utf-8"))
    for c in j[key]:
        if c["corpus"] == "legitimately-many-wanted":
            c["axn"] = a
    f.write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
touch(d, "corrections", f"seat 32/11 (legitimately-many-wanted): {WHY}; seat AXN re-derived {old_a} -> {a}", was="Stephen A. McKnight", now="Christopher McKnight")
d.setdefault("corrections", []).append({"date": "2026-11-02", "locus": "seat 32/11, declared/absence.json, the Masters exchange",
                                         "was": "Stephen A. McKnight", "now": "Christopher McKnight", "source": "Political Theory 6 (1978), volume index, p. 247", "seat_axn": a})
(ROOT / "data/registry.json").write_text(json.dumps(reg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(old_a, "->", a)
