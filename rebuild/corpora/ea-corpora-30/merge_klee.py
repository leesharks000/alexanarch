#!/usr/bin/env python3
"""Seat 30/09 into data/corpora/paul-klee, the seat EA-CORPORA-28/06 opened as a declared absence on 2026-10-27.
The new build (spec30-paul-klee.json, built with build29.py into a staging folder) brings original/ and text/; the
declaration of 27 October is kept at declared/ and its source fields under declared_2026_10_27, with the two works it
named as open and wanted now marked held. The AXN the absence took under #1713 is kept as axn_prior; the seat takes its
new AXN from the EA-CORPORA-30 deposit. MANIFEST.sha256 is rewritten over everything the seat holds.
    python3 merge_klee.py <staging folder>"""
import hashlib, json, pathlib, shutil, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
SEAT = ROOT / "data/corpora/paul-klee"
NEW = pathlib.Path(sys.argv[1]) / "paul-klee"
old = json.loads((SEAT / "source.json").read_text(encoding="utf-8"))
new = json.loads((NEW / "source.json").read_text(encoding="utf-8"))
if old.get("seat") == new["seat"]:
    sys.exit("already merged")
for d in ("original", "text"):
    if (SEAT / d).exists():
        shutil.rmtree(SEAT / d)
    shutil.copytree(NEW / d, SEAT / d)
held = {"Pädagogisches Skizzenbuch": "held at 30/09 (the 1925 first printing)", "Schöpferische Konfession": "held at 30/09 (Tribüne der Kunst und Zeit XIII, 1920)"}
decl = {k: old[k] for k in ("seat", "title", "edition", "scope", "declared_absences", "why_seated", "ruling", "fetched") if k in old}
decl["now_held"] = held
new["declared_2026_10_27"] = decl
new["fulfils"] = "EA-CORPORA-28/06, the declared absence of 2026-10-27, whose two open works this seat holds; its declaration is kept at declared/ and above"
new["axn_prior"] = {"axn": old.get("axn"), "basis": old.get("axn_basis"), "why": "the absence's AXN under #1713; the seat now holds texts and takes its AXN from EA-CORPORA-30"}
(SEAT / "source.json").write_text(json.dumps(new, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
lines = [f"{sha(p)}  {p.relative_to(SEAT).as_posix()}" for p in sorted(SEAT.rglob("*")) if p.is_file() and p.name not in ("MANIFEST.sha256", "source.json")]
(SEAT / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
print("merged:", len(lines), "files;", new["seat"], "fulfils", decl["seat"])
