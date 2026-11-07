#!/usr/bin/env python3
"""seat_axns36.py — give the twenty-seven seats of EA-CORPORA-36 their AXNs, in the form of seat_axns_20261027.py
(AXN:<HEX>.ORIGINAL.<glyphs>, HEX the position of the seating's deposit, the glyphs from the SHA-256 of the seat's
MANIFEST.sha256), now that the seating is deposited (DEP). Touches only these twenty-seven seats: writes `axn`,
`axn_basis` and the deposited `spine` into each source.json (outside the MANIFEST), drops the pending `seating` note,
and writes `axn` into data/api/corpora.json and datasets/corpora/corpora.json.
    python3 rebuild/corpora/ea-corpora-36/seat_axns36.py <deposit number> [--apply]"""
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
DEP = int(sys.argv[1])
ASSIGNED = "2026-11-07"
ONLY = [a for a in sys.argv[2:] if not a.startswith("--")]
NAMES = ["hall-peri-hypsous-1652", "boileau-traite-du-sublime-1683", "spectator-229-1711", "pope-sapho-to-phaon", "fawkes-anacreon-sappho-1760", "welcker-sappho-1816", "merivale-poems-1838", "mure-critical-history-1850", "swinburne-poems-and-ballads-1866", "higginson-atlantic-essays-1871", "symonds-studies-greek-poets-1873", "vivien-sapho-1903", "carman-sappho-1904", "wharton-sappho-1908", "renderings-1910-1920", "wilamowitz-sappho-und-simonides-1913", "robinson-sappho-and-her-influence-1924", "cox-poems-of-sappho-1925", "cicero-tusculanae", "dante-commedia", "chaucer-troilus", "shakespeare-sonnets", "milton-paradise-lost", "romantic-posterity", "dickinson-poems-1890-1896", "baratynsky-moi-dar-ubog", "wipp-markers-sandia-1993"]
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
        s["spine"] = f"EA-CORPORA-36 (#{DEP})"
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
