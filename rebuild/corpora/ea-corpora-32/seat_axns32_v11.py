#!/usr/bin/env python3
"""seat_axns32_v11.py — the seat AXNs at the version of EA-CORPORA-32 (v1.1, deposit DEP, superseding #1731), at the
operator's word of 2026-11-02 ("yes, lets grab them, but fold into 32 and version"). The ten seats whose MANIFEST.sha256 is
unchanged since #1731 keep the AXN #1731 gave them (AXN:0BE1.ORIGINAL), rewritten into the indexes, which index_seats32.py
rebuilds without it. The two seats the version changes take theirs from DEP: nicolaus-damascenus (32/12, new) and
legitimately-many-wanted (32/11, its declaration extended by Drossaart Lulofs 1965), whose prior AXN and manifest hash are
recorded on it. Writes `axn`, `axn_basis`, `spine` into each changed source.json (outside the MANIFEST), drops the pending
`seating` note, and writes `axn` into data/api/corpora.json and datasets/corpora/corpora.json for all twelve.
    python3 rebuild/corpora/ea-corpora-32/seat_axns32_v11.py <deposit number> [--apply]"""
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
DEP = int(sys.argv[1])
KEEP = ["pseudo-archytas", "aldine-aristotle-1497", "theophrastus-metaphysics-wimmer-1866", "philodemus-index-academicorum", "dionysius-ad-ammaeum",
        "cicero-ad-atticum", "schleiermacher-platons-werke-1804", "campbell-sophistes-politicus", "tennemann-platonische-philosophie", "hegel"]
NEW = ["legitimately-many-wanted", "nicolaus-damascenus"]
PRIOR = {"legitimately-many-wanted": {"axn": "AXN:0BE1.ORIGINAL.🪐❌🌘♻️🏰🍃", "manifest_sha256": "0def07fe27187da0dce91d4eb0450fb3dfdad4d0a8d7f1804c141728f43adfc2",
                                      "deposit": 1731, "why": "the declaration extended at the version (Drossaart Lulofs 1965 added)"}}
d = next(x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"] if x["deposit_number"] == DEP)
I = json.loads((ROOT / "data/api/corpora.json").read_text(encoding="utf-8"))
M = json.loads((ROOT / "datasets/corpora/corpora.json").read_text(encoding="utf-8"))
ax = {}
for n in KEEP:
    s = json.loads((ROOT / "data/corpora" / n / "source.json").read_text(encoding="utf-8"))
    h = hashlib.sha256((ROOT / "data/corpora" / n / "MANIFEST.sha256").read_bytes()).hexdigest()
    assert s["axn_basis"]["sha256"] == h, f"{n}: manifest changed since #1731"
    ax[n] = s["axn"]
out = []
for n in NEW:
    seat = ROOT / "data/corpora" / n
    h = hashlib.sha256((seat / "MANIFEST.sha256").read_bytes()).hexdigest()
    a = A.derive_axn(h, d["hex"], "ORIGINAL"); ax[n] = a; out.append((n, seat, h, a))
for n, a in ax.items():
    print(" ", n, "->", a, "(kept from #1731)" if n in KEEP else "")
if "--apply" in sys.argv:
    for n, seat, h, a in out:
        sj = seat / "source.json"; s = json.loads(sj.read_text(encoding="utf-8"))
        s["axn"] = a
        s["axn_basis"] = {"sha256_of": "MANIFEST.sha256", "sha256": h, "hex_of": f"#{DEP} ({d['axn']})", "family": "ORIGINAL",
                          "glyph_table": A.AXN_GLYPH_TABLE, "assigned": "2026-11-02"}
        if n in PRIOR:
            s["axn_prior"] = PRIOR[n]
        s["spine"] = f"EA-CORPORA-32 v1.1 (#{DEP}, superseding #1731)"
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
