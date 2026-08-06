#!/usr/bin/env python3
"""WAVE-HEXPOS-01 · Phase 2 (as executed 2026-08-06) — contested-position resolution.

Rulings implemented (adopted by MANUS 2026-08-06, "adopted on all / lets implement";
F6/D5 executed under the same adopted principle, flagged for explicit ratification):
  0365 — #856 keeps (priority);        #869 -> 05B0
  0391 — #901 keeps (priority + hex inscribed in sealed canonical bytes); #913 -> 05B1
  05AF — #1433 keeps (chain tether, minted 2026-08-04T08:56Z, one day prior);
         symbolon witnessing 6b48617ee0e64e8f (registered 2026-08-05T04:37Z) -> 05B2
  Ledger: next_hex -> 05B3 (root cause of 05AF: deposit-side allocator read the
  shared ledger but never wrote it; fixed separately in mint_deposit.py).

Every prior label is preserved: axn_history entries on records, prior_position on
the symbolon entry, pointer files at every renamed path. Idempotent."""
import json, pathlib, datetime, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
TODAY = datetime.date.today().isoformat()
NOW = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
REASON = "contested_position_reallocation (WAVE-HEXPOS-01 Phase 2, MANUS ruling 2026-08-06)"
MOVES = {869: "05B0", 913: "05B1"}
SYM_ENTRY, SYM_NEW = "6b48617ee0e64e8f", "05B2"
LEDGER_NEXT = "05B3"

reg_path = ROOT/"data/registry.json"
reg = json.loads(reg_path.read_text()); deps = reg["deposits"]
held = {(d.get("hex") or "").upper().zfill(4) for d in deps if d.get("hex")}
touched = False
for n, h in MOVES.items():
    d = next(x for x in deps if x["deposit_number"] == n)
    if d["hex"] == h: print(f"#{n}: already {h} — skip"); continue
    assert h not in held, f"position {h} already held"
    old_hx, old_axn = d["hex"], d["axn"]
    d.setdefault("axn_history", []).append({"axn": old_axn,
        "schema_version": d.get("axn_schema_version","v2"), "retired_at": TODAY, "reason": REASON})
    d["hex"], d["axn"] = h, old_axn.replace(f"AXN:{old_hx}.", f"AXN:{h}.", 1)
    held.add(h); touched = True
    # rename ONLY artifacts this record actually OWNS. EXECUTION INCIDENT
    # (2026-08-06, caught same-session, pre-commit): the first form of this
    # block renamed by label alone — but on a CONTESTED label the files named
    # AXN-<label>-* belong to the KEEPER, not the mover. It moved #856's
    # canonical text to #869's new address before being reverted from git.
    # Ownership gate: full_text_path must name the file, or the sibling is
    # renamed only when the record's own full_text_path carried the label
    # (i.e., the AXN-<label> filename family is this record's). Canonical
    # texts move as EXACT BYTES — never edited (sealed core).
    owns_label_family = f"AXN-{old_hx}" in (d.get("full_text_path") or "")
    for tmpl in (f"data/texts/AXN-{old_hx}-text.md", f"data/deposits/AXN-{old_hx}.md",
                 f"data/external-metadata/AXN-{old_hx}.json"):
        if not owns_label_family: break
        oldp = ROOT/tmpl
        if oldp.exists():
            newrel = tmpl.replace(f"AXN-{old_hx}", f"AXN-{h}")
            newp = ROOT/newrel
            if not newp.exists():
                body = oldp.read_text()
                if not tmpl.startswith("data/texts/"):
                    # presentation artifacts only: bring identifier strings current
                    body = body.replace(f"AXN:{old_hx}.", f"AXN:{h}.")
                newp.write_text(body)
                oldp.write_text(f"superseded path — deposit #{n} moved to /{newrel} on {TODAY} "
                                f"(label {old_hx} retired under WAVE-HEXPOS-01 Phase 2; prior form "
                                f"preserved in the record's axn_history)\n")
            if tmpl.startswith("data/texts/"): d["full_text_path"] = "/"+newrel
            print(f"#{n}: {tmpl} -> {newrel} (pointer left)")
    print(f"#{n}: {old_axn} -> {d['axn']}")

# stale deposit-md identifier lines for the Phase-1 records (#1-#3): bring the
# presentation artifacts' AXN strings to current canonical (padded + v2 glyphs)
for n in (1, 2, 3):
    d = next(x for x in deps if x["deposit_number"] == n)
    cur = d["axn"]; hx = d["hex"]
    p = ROOT/f"data/deposits/AXN-{hx}.md"
    if p.exists():
        body = p.read_text(); orig = body
        # replace any historical AXN form for this record (unpadded and/or v1 glyphs)
        for h in (d.get("axn_history") or []):
            body = body.replace(h["axn"], cur)
        body = re.sub(rf"AXN:0*{int(hx,16):X}\.([A-Z]+)\.", f"AXN:{hx}.\\1.", body)
        if body != orig:
            p.write_text(body); print(f"#{n}: deposit-md identifier lines -> {cur}")

if touched or True:
    reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=2))
    print("registry.json written")

# symbolon entry reallocation
sp = ROOT/f"data/symbolon-registry/entries/{SYM_ENTRY}.json"
s = json.loads(sp.read_text())
if s.get("position") != SYM_NEW:
    old_pos, old_axn = s.get("position"), s.get("axn")
    s["position"] = SYM_NEW
    if old_axn: s["axn"] = old_axn.replace(f"AXN:{old_pos}.", f"AXN:{SYM_NEW}.", 1)
    s.setdefault("position_history", []).append({"position": old_pos, "axn": old_axn,
        "retired_at": NOW, "reason": REASON + " — 05AF was already held by deposit #1433 "
        "(minted 2026-08-04T08:56Z, before this witnessing's 2026-08-05T04:37Z allocation); "
        "root cause: deposit-side allocator did not write the shared ledger"})
    sp.write_text(json.dumps(s, ensure_ascii=False, indent=1))
    print(f"symbolon {SYM_ENTRY}: {old_pos} -> {SYM_NEW} ({old_axn} -> {s['axn']})")
else:
    print(f"symbolon {SYM_ENTRY}: already {SYM_NEW} — skip")

# shared allocation ledger: bump past every reallocated position
lp = ROOT/"data/symbolon-registry/allocation.json"
led = json.loads(lp.read_text())
if int(led["next_hex"], 16) < int(LEDGER_NEXT, 16):
    led["next_hex"] = LEDGER_NEXT
    led["last_allocated"] = SYM_NEW
    led["last_allocated_at"] = NOW
    led["reallocation_2026_08_06"] = ("05B0/05B1/05B2 assigned by MANUS ruling under WAVE-HEXPOS-01 "
        "Phase 2 (contested 0365/0391/05AF); next_hex advanced past them")
    lp.write_text(json.dumps(led, ensure_ascii=False, indent=1))
    print(f"allocation ledger: next_hex -> {LEDGER_NEXT}")
else:
    print("allocation ledger: already advanced — skip")
print("Phase 2 complete. Run the propagator for 1 2 3 856 869 901 913 1433, then kernel-index, surfaces, coherence.")
