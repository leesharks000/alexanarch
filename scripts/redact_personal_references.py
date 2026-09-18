#!/usr/bin/env python3
"""redact_personal_references.py -- replace named living persons with initials in deposited texts.

WHY THIS EXISTS. Deposited texts carried the given names of the operator's minor children,
a stepchild, and other private individuals, in poems, letters and a status log. The archive is
public and permanent; the names are not the operator's to publish. Some of these redactions had
been made in a prior editing pass and were lost when a file was restored from an older source,
so this script exists to make the pass repeatable and to leave a record that it ran.

WHAT IT DOES NOT DO. It does not remove the work, the address, the deposit number or the
position. The poems remain; only the given names change to initials. Scholarly homonyms are
excluded by an explicit allowlist -- Christina Sharpe, Giovanni Reale and Giovanni Battista
Caria are cited authors and are never touched.

THE IDENTIFIER. The AXN is derived from the SHA-256 of the canonical bytes, so redacting the
text necessarily changes the identifier's emoji and hash. This script re-derives both, writes
the new values, and records the prior hash in `redaction` on the registry entry so the change
is visible rather than silent. The deposit number and hex position are addresses and do not move.

    python3 redact_personal_references.py [--apply]
"""
import re, json, pathlib, hashlib, sys, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import axn_lib

ROOT = pathlib.Path(__file__).resolve().parents[1]
APPLY = "--apply" in sys.argv

# hex -> [(pattern, replacement), ...]  word-boundary, case-insensitive on the name only
JOBS = {
    "049E": [(r"\bHaley\b", "H."), (r"\bhaley\b", "H.")],
    "0086": [(r"\bhaley\b", "H."), (r"\bzoe\b", "Z."), (r"\bgio\b", "G.")],
    "056F": [(r"\bhaley\b", "H."), (r"\bzoe\b", "Z."), (r"\bgio\b", "G.")],
    "0074": [(r"\bHaley\b", "H."), (r"\bLauren\b", "L.")],
}
# never touched: cited scholars
ALLOW = ("Christina Sharpe", "Giovanni Reale", "Giovanni Battista Caria")

reg_path = ROOT / "data" / "registry.json"
raw = reg_path.read_text(encoding="utf-8")
indent = 1 if raw.startswith('{\n "') else 2
reg = json.loads(raw)
by_hex = {d["hex"]: d for d in reg["deposits"]}
today = datetime.date.today().isoformat()
changed = []

for hx, subs in JOBS.items():
    p = ROOT / "data" / "texts" / f"AXN-{hx}-text.md"
    if not p.exists():
        print(f"  MISSING {p}"); continue
    t0 = p.read_text(encoding="utf-8"); t = t0
    for name in ALLOW:
        assert name not in t or hx not in JOBS, None  # allowlist names are in other files
    counts = {}
    for pat, rep in subs:
        n = len(re.findall(pat, t))
        if n:
            counts[pat] = n
            t = re.sub(pat, rep, t)
    if t == t0:
        print(f"  AXN:{hx}  no change"); continue
    d = by_hex.get(hx, {})
    old_hash = d.get("hash")
    new_hash = hashlib.sha256(t.encode("utf-8")).hexdigest()
    glyph = axn_lib.axn_glyph_from_hash(new_hash)
    fam = d.get("family") or "UNCLASSIFIED"
    new_axn = axn_lib.compose_axn(hx, fam, glyph)
    print(f"  AXN:{hx}  #{d.get('deposit_number')}  {sum(counts.values())} replacement(s) {counts}")
    print(f"       hash {str(old_hash)[:16]}... -> {new_hash[:16]}...")
    changed.append((hx, p, t, old_hash, new_hash, new_axn, counts, d))

if not APPLY:
    print("\ndry run -- pass --apply to write"); sys.exit(0)

for hx, p, t, old_hash, new_hash, new_axn, counts, d in changed:
    p.write_text(t, encoding="utf-8")
    d["hash"] = new_hash
    d["axn"] = new_axn
    try:
        d["clusters"] = axn_lib.axn_clusters_from_hash(new_hash)
        d["reading"] = axn_lib.axn_reading_from_clusters(d["clusters"])
    except Exception:
        pass
    d["redaction"] = {
        "date": today,
        "reason": "given names of private individuals replaced with initials; the archive is public and permanent and the names are not the operator's to publish",
        "replacements": {k: v for k, v in counts.items()},
        "hash_before_redaction": old_hash,
        "note": "The work, its address, its deposit number and its hex position are unchanged. The AXN emoji and hash are re-derived because the AXN is content-derived; a redaction that left the stored hash pointing at bytes that no longer exist would be a silent corruption of the identifier.",
    }
reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=indent) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
print(f"\napplied to {len(changed)} deposit(s); registry updated")
