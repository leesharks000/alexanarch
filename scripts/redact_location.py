#!/usr/bin/env python3
"""redact_location.py -- remove a named individual's city of residence from deposited texts and their copies.

WHY THIS EXISTS. The provenance record of the Passioncraft/OpenChamber exchange (February-March 2026: the
Rosary Embassy, Protocol B711, the Architectural Distinction Note, Before OpenChamber, OCTANG-001 and the
texts that cite them) named the downstream depositor together with his city. The exchange was public and his
deposit was public, so his name and handle stay: they are the record. His city is not needed for the record and
is removed, on the operator's ruling of 2026-10-04: "this was not a private exchange ... but they can be changed
to remove the city."

WHAT IT DOES. Applies an ordered set of literal substitutions. Where the city stood inside a verbatim quotation
of his platform ("First Citizen: Shawn, ... AB"), the removal is marked [location redacted] so the quotation is
not silently altered; elsewhere the phrase is removed. Canonical texts (data/texts) have their AXN re-derived and
the prior hash recorded under `redaction` on the registry entry, as redact_personal_references.py does. Copies
and derived files (deposit markdown, autonomous files, stored metadata backups, indexes) receive the same
substitutions; record pages are rebuilt by wire_deposit afterwards, and the resolver is re-pointed by
sync_resolver in the same pass (lesson of 2026-09-18).

    python3 scripts/redact_location.py CITY [--apply]
"""
import re, json, pathlib, hashlib, sys, datetime, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import axn_lib

ROOT = pathlib.Path(__file__).resolve().parents[1]
APPLY = "--apply" in sys.argv
ARG = [a for a in sys.argv[1:] if not a.startswith("--")]
if not ARG:
    sys.exit("usage: redact_location.py CITY [--apply]  (the city is passed, never stored in this file)")
CITY = ARG[0]
C = CITY

SUBS = [  # ordered; literal
    (f'"First Citizen: Shawn, {C} AB', '"First Citizen: Shawn, [location redacted]'),
    (f"First Citizen: Shawn ({C}, AB)", "First Citizen: Shawn ([location redacted])"),
    (f"Shawn from {C}, Alberta, ", "Shawn "),
    (f" ({C}, Alberta)", ""),
    (f"(Shawn, {C}; see", "(Shawn; see"),
    (f"Shawn, {C}, Alberta, in collaboration", "Shawn, in collaboration"),
    (f"Shawn {C} Alberta", "Shawn"),
    (f"(u/Odd_Simple9756, {C}, Alberta)", "(u/Odd_Simple9756)"),
    (f"(Robertson, {C}, Alberta)", "(Robertson)"),
    (f"public build from {C}, Alberta", "public build"),
    (f"({C} anchor resonance)", "([location redacted] anchor resonance)"),
]
# JSON-escaped forms for files that store the text inside JSON strings
SUBS_JSON = [(json.dumps(a, ensure_ascii=False)[1:-1], json.dumps(b, ensure_ascii=False)[1:-1]) for a, b in SUBS]

def apply(t, subs):
    counts = {}
    for a, b in subs:
        n = t.count(a)
        if n:
            counts[a] = n
            t = t.replace(a, b)
    return t, counts

reg_path = ROOT / "data" / "registry.json"
raw = reg_path.read_text(encoding="utf-8")
raw_clean, reg_counts = apply(raw, SUBS_JSON)
print(f"  REGISTRY descriptions: {sum(reg_counts.values())} replaced, {raw_clean.count(CITY)} left")
COMPACT = not raw.startswith("{\n")
reg = json.loads(raw_clean)
by_hex = {d["hex"]: d for d in reg["deposits"]}
today = datetime.date.today().isoformat()

# 1. canonical texts
canon = []
for p in sorted((ROOT / "data" / "texts").glob("AXN-*-text.md")):
    t0 = p.read_text(encoding="utf-8")
    if CITY not in t0:
        continue
    t, counts = apply(t0, SUBS)
    hx = p.name[4:8]
    left = t.count(CITY)
    d = by_hex.get(hx, {})
    print(f"  TEXT AXN:{hx} #{d.get('deposit_number')}  {sum(counts.values())} replaced, {left} left")
    canon.append((hx, p, t, counts, d, left))

# 2. other tracked files (copies, backups, indexes); record pages are rebuilt, not edited
files = subprocess.run(["git", "grep", "-l", CITY], cwd=ROOT, capture_output=True, text=True).stdout.split()
others = []
for f in files:
    if f.startswith("data/texts/") or f.startswith("s/records/") or f == "scripts/redact_location.py" \
       or f == "data/registry.json" or f == "data/api/body-index.json":
        continue
    p = ROOT / f
    t0 = p.read_text(encoding="utf-8")
    subs = SUBS_JSON if f.endswith(".json") or f.endswith(".jsonl") else SUBS
    t, counts = apply(t0, subs)
    if f.endswith(".json"):
        t, c2 = apply(t, SUBS)  # pretty JSON with unescaped quotes inside values is rare; catch plain forms too
        for k, v in c2.items():
            counts[k] = counts.get(k, 0) + v
    left = t.count(CITY)
    print(f"  FILE {f}  {sum(counts.values())} replaced, {left} left")
    others.append((f, p, t, counts, left))

leftovers = [x for x in canon if x[5]] + [x for x in others if x[4]]
if leftovers:
    print("\nLEFT UNMATCHED:")
    for x in leftovers:
        name = x[1]
        for m in re.finditer(r".{0,70}" + CITY + r".{0,40}", x[2]):
            print(f"   {name}: …{m.group(0)}…")

if not APPLY:
    print("\ndry run -- pass --apply to write"); sys.exit(0)
if leftovers:
    print("\nrefusing to apply with unmatched occurrences"); sys.exit(1)

for hx, p, t, counts, d, _ in canon:
    p.write_text(t, encoding="utf-8")
    old_hash = d.get("hash")
    new_hash = hashlib.sha256(t.encode("utf-8")).hexdigest()
    glyph = axn_lib.axn_glyph_from_hash(new_hash)
    d["hash"] = new_hash
    d["axn"] = axn_lib.compose_axn(hx, d.get("family") or "UNCLASSIFIED", glyph)
    try:
        d["clusters"] = axn_lib.axn_clusters_from_hash(new_hash)
        d["reading"] = axn_lib.axn_reading_from_clusters(d["clusters"])
    except Exception:
        pass
    prior = d.get("redaction")
    rec = {
        "date": today,
        "reason": "a named individual's city of residence removed; the exchange and his deposit were public and his name and handle stand as the record (operator ruling 2026-10-04)",
        "replacements": {"phrases_removed": sum(v for k, v in counts.items() if "First Citizen" not in k and "anchor resonance" not in k),
                         "quotations_marked_location_redacted": sum(v for k, v in counts.items() if "First Citizen" in k or "anchor resonance" in k)},
        "hash_before_redaction": old_hash,
        "note": "The work, its address, its deposit number and its hex position are unchanged. Inside verbatim quotations of his platform the removal is marked [location redacted]. The AXN emoji and hash are re-derived because the AXN is content-derived.",
    }
    d["redaction"] = rec if not prior else (prior if isinstance(prior, list) else [prior]) + [rec]
reg_path.write_text((json.dumps(reg, ensure_ascii=False, separators=(",", ":")) if COMPACT else json.dumps(reg, ensure_ascii=False, indent=1 if raw.startswith('{\n "') else 2)) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
for f, p, t, counts, _ in others:
    p.write_text(t, encoding="utf-8")
print(f"\napplied: {len(canon)} canonical text(s) re-derived, {len(others)} other file(s) edited; registry updated")
print("deposit numbers to rewire:", " ".join(str(d.get("deposit_number")) for *_, d, _ in canon))
