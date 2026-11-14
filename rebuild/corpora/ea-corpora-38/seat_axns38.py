#!/usr/bin/env python3
"""seat_axns37.py — give the sixteen seats of EA-CORPORA-38 their AXNs, in the form of seat_axns_20261027.py
(AXN:<HEX>.ORIGINAL.<glyphs>, HEX the position of the seating's deposit, the glyphs from the SHA-256 of the seat's
MANIFEST.sha256), now that the seating is deposited (DEP). Touches only these sixteen seats: writes `axn`,
`axn_basis` and the deposited `spine` into each source.json (outside the MANIFEST), drops the pending `seating` note,
and writes `axn` into data/api/corpora.json and datasets/corpora/corpora.json.
    python3 rebuild/corpora/ea-corpora-38/seat_axns38.py <deposit number> [--apply]"""
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
DEP = int(sys.argv[1])
ASSIGNED = "2026-11-14"
ONLY = [a for a in sys.argv[2:] if not a.startswith("--")]
NAMES = ["kant-akademie-ausgabe", "alexander-in-apr-wallies-1883", "philoponus-in-apr-wallies-1905", "theophrastus-characteres-diels-1909", "epictetus-dissertationes-schenkl-1916", "cicero-topica-wilkins-1902", "bacon-novum-organum-1620", "hume-treatise-enquiry", "carroll-symbolic-logic-1897", "hegel-wissenschaft-der-logik", "frege-begriffsschrift-1879", "peirce-logic-papers-1867-1878", "boethius-logica-migne-pl64", "nyaya-sutra-vatsyayana-1896", "ibn-sina-isharat-forget-1892", "buridan-sophismata-c1489"]
if ONLY: NAMES = [n for n in NAMES if n in ONLY]
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
                          "glyph_table": A.AXN_GLYPH_TABLE, "assigned": ASSIGNED}
        s["spine"] = f"EA-CORPORA-38 (#{DEP})"
        s.pop("seating", None); s.pop("axn_note", None)
        sj.write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for c in I["corpora"]:
        if c["corpus"] in ax:
            c["axn"] = ax[c["corpus"]]
    for x in M["seats"]:
        if x["corpus"] in ax:
            x["axn"] = ax[x["corpus"]]
    (ROOT / "data/api/corpora.json").write_text(json.dumps(I, ensure_ascii=False, indent=1), encoding="utf-8"); open(ROOT / "data/api/corpora.json","a").write("\n")
    (ROOT / "datasets/corpora/corpora.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")
    print("applied")
