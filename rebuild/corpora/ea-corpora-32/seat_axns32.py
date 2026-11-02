#!/usr/bin/env python3
"""seat_axns32.py — give the eleven seats of EA-CORPORA-32 their AXNs, in the form of seat_axns_20261027.py
(AXN:<HEX>.ORIGINAL.<glyphs>, HEX the position of the seating's deposit, the glyphs from the SHA-256 of the seat's
MANIFEST.sha256), now that the seating is deposited (DEP). Touches only these eleven seats: writes `axn`,
`axn_basis` and the deposited `spine` into each source.json (outside the MANIFEST), drops the pending `seating` note,
and writes `axn` into data/api/corpora.json and datasets/corpora/corpora.json.
    python3 rebuild/corpora/ea-corpora-32/seat_axns32.py <deposit number> [--apply]"""
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
DEP = int(sys.argv[1])
NAMES = ['pseudo-archytas', 'aldine-aristotle-1497', 'theophrastus-metaphysics-wimmer-1866', 'philodemus-index-academicorum', 'dionysius-ad-ammaeum', 'cicero-ad-atticum', 'schleiermacher-platons-werke-1804', 'campbell-sophistes-politicus', 'tennemann-platonische-philosophie', 'hegel', 'legitimately-many-wanted']
d = next(x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"] if x["deposit_number"] == DEP)
I = json.loads((ROOT / "data/api/corpora.json").read_text(encoding="utf-8"))
M = json.loads((ROOT / "datasets/corpora/corpora.json").read_text(encoding="utf-8"))
out = []
for n in NAMES:
    seat = ROOT / "data/corpora" / n
    h = hashlib.sha256((seat / "MANIFEST.sha256").read_bytes()).hexdigest()
    out.append((n, seat, h, A.derive_axn(h, d["hex"], "ORIGINAL")))
for n, _, _, a in out:
    print(" ", n, "->", a)
if "--apply" in sys.argv:
    ax = dict((n, a) for n, _, _, a in out)
    for n, seat, h, a in out:
        sj = seat / "source.json"; s = json.loads(sj.read_text(encoding="utf-8"))
        s["axn"] = a
        s["axn_basis"] = {"sha256_of": "MANIFEST.sha256", "sha256": h, "hex_of": f"#{DEP} ({d['axn']})", "family": "ORIGINAL",
                          "glyph_table": A.AXN_GLYPH_TABLE, "assigned": "2026-11-02"}
        s["spine"] = f"EA-CORPORA-32 (#{DEP})"
        s.pop("seating", None)
        sj.write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for c in I["corpora"]:
        if c["corpus"] in ax:
            c["axn"] = ax[c["corpus"]]
    for x in M["seats"]:
        if x["corpus"] in ax:
            x["axn"] = ax[x["corpus"]]
    (ROOT / "data/api/corpora.json").write_text(json.dumps(I, ensure_ascii=False, indent=1), encoding="utf-8")
    (ROOT / "datasets/corpora/corpora.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")
    print("applied")
