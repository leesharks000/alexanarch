#!/usr/bin/env python3
"""seat_axns_20261027.py — give every seat on the originals shelf an AXN (session tool, kept with the seatings).

MANUS, 2026-10-27, on the proposal: "3. agreed." A seat's AXN is
    AXN:<HEX>.ORIGINAL.<glyphs>
where HEX is the hex position of the active deposit that numbers the seat (the single-seat record of the first seating
where one exists, else the seating's gathering record), ORIGINAL is the family, and the six glyphs are derived, with
the current table (scripts/axn_lib.py, v2.1), from the SHA-256 of the seat's MANIFEST.sha256 — the file that lists the
digest of every file the seat holds. Repair a file and the MANIFEST changes, and the AXN with it. Writes `axn` and
`axn_basis` into each seat's source.json (outside the MANIFEST, so the AXN does not alter what it names), and `axn`
into data/api/corpora.json and datasets/corpora/corpora.json.
    python3 rebuild/corpora/seat_axns_20261027.py [--apply]"""
import hashlib, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
D = [d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"] if d["status"] in ("ACTIVE", "CANONICAL")]
single, seating = {}, {}
for d in D:
    m = re.match(r"EA-CORPORA-(\d\d(?:/\d\d)*)(?: · Seat (\d\d))?\b", d["title"])
    if not m:
        continue
    parts = m.group(1).split("/")
    if m.group(2):
        single[f"{parts[0]}/{m.group(2)}"] = d
    elif parts[0] == "01" and len(parts) == 2:
        single["/".join(parts)] = d
    else:
        for p in parts:
            seating.setdefault(p, d)
I = json.loads((ROOT / "data/api/corpora.json").read_text(encoding="utf-8"))
M = json.loads((ROOT / "datasets/corpora/corpora.json").read_text(encoding="utf-8"))
rows, out = {x["corpus"]: x for x in M["seats"]}, []
for c in I["corpora"]:
    no = c["seat"].split("-")[-1]; nn = no.split("/")[0]
    d = single.get(no) or seating.get(nn)
    seat = ROOT / "data/corpora" / c["corpus"]
    h = hashlib.sha256((seat / "MANIFEST.sha256").read_bytes()).hexdigest()
    axn = A.derive_axn(h, d["hex"], "ORIGINAL")
    out.append((c, seat, d, h, axn))
print(len(out), "seats;", len({a for *_, a in out}), "distinct AXNs")
for c, seat, d, h, axn in out[:4] + out[-3:]:
    print(" ", c["seat"], c["corpus"], "->", axn, f"(#{d['deposit_number']})")
if "--apply" in sys.argv:
    for c, seat, d, h, axn in out:
        sj = seat / "source.json"; raw = sj.read_text(encoding="utf-8"); s = json.loads(raw)
        s["axn"] = axn
        s["axn_basis"] = {"sha256_of": "MANIFEST.sha256", "sha256": h, "hex_of": f"#{d['deposit_number']} ({d['axn']})",
                          "family": "ORIGINAL", "glyph_table": A.AXN_GLYPH_TABLE, "assigned": "2026-10-27"}
        sj.write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        c["axn"] = axn
        if c["corpus"] in rows:
            rows[c["corpus"]]["axn"] = axn
    (ROOT / "data/api/corpora.json").write_text(json.dumps(I, ensure_ascii=False, indent=1), encoding="utf-8")
    (ROOT / "datasets/corpora/corpora.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")
    print("applied")
