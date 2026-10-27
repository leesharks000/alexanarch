#!/usr/bin/env python3
"""nonreg_axn.py — the AXN mint route of the /non register (ruled 2026-10-27).

MANUS, 2026-10-27, asked whether the observations of the /non register take AXNs as captures do: "yes, they should probably
also have a [n axn]". The rulings of the morning hold for them: "one observation / analysis / measure should have one
axn" and "one position per address".

THE REGISTER. datasets/negative-of-the-negative/v2/register.json records public knowledge at the addresses of the /non
panel, where the archive is most often not represented (Lee Sharks, 2026-10-06). A panel run that returns the archive is
seated in both registers and the two observations share one obs_id (ruled 2026-10-06).

THE UNIT. Each observation (the entry itself, and each item of its observations list) is sealed with its reading and its
measures in datasets/negative-of-the-negative/v2/sealed/<observation slug>.json, canonical JSON (keys sorted, UTF-8, no
insignificant whitespace) of
    observation   q, surface, date, auth, ev, entity, transcript, transcript_raw, transcript_removed, transcript_sha256,
                  transcript_class, transcript_complete, transcript_read
    reading       archive_present, archive_basis, notes, capture_ref
    measures      cites, cite_list, sf
The AXN is not written into the register (as the /non rows carry none of theirs); the ledger holds it.

THE POSITION. One per address, from the shared allocation ledger (data/symbolon-registry/allocation.json), root
AXN:<HEX>.PANEL; each observation AXN:<HEX>.PANEL.<glyphs>, table v2.1, from the SHA-256 of its sealed file. An observation
seated in both registers is one observation: it carries the Capture Registry's AXN (data/captures/axn.json, by obs_id),
and no second AXN is minted for it. A changed observation is re-derived with its earlier form kept in history.

Ledger: datasets/negative-of-the-negative/v2/register-axn.json.
    python3 scripts/nonreg_axn.py --check
    python3 scripts/nonreg_axn.py --apply [--reason "..."]
"""
import datetime, hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import axn_lib as A

V2 = ROOT / "datasets/negative-of-the-negative/v2"
REG = V2 / "register.json"
LEDGER = V2 / "register-axn.json"
SEALED = V2 / "sealed"
ALLOC = ROOT / "data/symbolon-registry/allocation.json"
FAMILY = "PANEL"
OBS = ["q", "surface", "date", "auth", "ev", "entity", "transcript", "transcript_raw", "transcript_removed", "transcript_sha256",
       "transcript_class", "transcript_complete", "transcript_read"]
REA = ["archive_present", "archive_basis", "notes", "capture_ref"]
MEA = ["cites", "cite_list", "sf"]


def canon(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def units(e):
    out = [dict(e)]
    for o in e.get("observations") or []:
        x = dict(o)
        for k in ("q", "entity"):
            x.setdefault(k, e.get(k))
        out.append(x)
    return out


def sealed(e, o):
    slug = o.get("slug") or e["slug"]
    keep = lambda ks: {k: o[k] for k in ks if o.get(k) not in (None, "", [])}
    body = {"observation": keep(OBS), "reading": keep(REA), "measures": keep(MEA),
            "address": {"q": e.get("q"), "record": e["slug"], "register": "datasets/negative-of-the-negative/v2/register.json"}, "slug": slug}
    return slug, canon(body)


def main():
    apply = "--apply" in sys.argv
    reason = sys.argv[sys.argv.index("--reason") + 1] if "--reason" in sys.argv else "the observation's sealed bytes changed"
    today = datetime.date.today().isoformat()
    reg = json.loads(REG.read_text(encoding="utf-8"))
    led = json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {
        "_what_this_is": ("The AXN ledger of the /non register: one position per address (root AXN:<HEX>.PANEL), one AXN per observation "
                          "sealed with its reading and measures (AXN:<HEX>.PANEL.<glyphs>, glyphs from the SHA-256 of "
                          "datasets/negative-of-the-negative/v2/sealed/<observation>.json). An observation seated in both registers carries "
                          "the Capture Registry's AXN. history keeps every earlier form."),
        "ruling": 'Lee Sharks, 2026-10-27: "yes, they should probably also have a[n axn]" — with "one observation / analysis / measure should have one axn" and "one position per address".',
        "family": FAMILY, "minted_by": "scripts/nonreg_axn.py", "glyph_table": A.AXN_GLYPH_TABLE, "addresses": {}}
    cap = json.loads((ROOT / "data/captures/axn.json").read_text(encoding="utf-8"))["addresses"]
    cap_by_obs = {o.get("obs_id"): (a["root"], o["axn"], o["file"]) for a in cap.values() for o in a["observations"].values() if o.get("obs_id")}
    alloc = json.loads(ALLOC.read_text(encoding="utf-8"))
    deps = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]
    nxt = max(int(alloc["next_hex"], 16), max(int(d["hex"], 16) for d in deps if d.get("hex")) + 1)
    order = sorted(reg["entries"], key=lambda e: (min(str(u.get("date") or "") for u in units(e)), e["slug"]))
    new_pos, minted, shared, rederived, files = 0, 0, 0, 0, {}
    for e in order:
        us = units(e)
        own = [u for u in us if u.get("obs_id") not in cap_by_obs]
        a = led["addresses"].get(e["slug"])
        if not a:
            a = {"q": e.get("q"), "surface": e.get("surface"), "addr_id": e.get("addr_id"), "entity": e.get("entity"), "observations": {}}
            if own:
                hx = f"{nxt:04X}"; nxt += 1; new_pos += 1
                a.update({"hex": hx, "root": f"AXN:{hx}.{FAMILY}", "allocated": today})
            led["addresses"][e["slug"]] = a
        for u in us:
            slug, b = sealed(e, u)
            if u.get("obs_id") in cap_by_obs:
                croot, caxn, cfile = cap_by_obs[u["obs_id"]]
                if slug not in a["observations"]:
                    shared += 1
                a["observations"][slug] = {"axn": caxn, "shared_with_capture_registry": {"root": croot, "sealed": cfile},
                                           "obs_id": u["obs_id"], "date": u.get("date"), "surface": u.get("surface")}
                continue
            if "hex" not in a:   # an address whose first observations were all shared, now with one of its own
                hx = f"{nxt:04X}"; nxt += 1; new_pos += 1
                a.update({"hex": hx, "root": f"AXN:{hx}.{FAMILY}", "allocated": today})
            h = hashlib.sha256(b).hexdigest()
            axn = A.derive_axn(h, a["hex"], FAMILY)
            cur = a["observations"].get(slug)
            if cur and cur.get("sha256") == h:
                continue
            if cur:
                cur.setdefault("history", []).append({"axn": cur["axn"], "sha256": cur["sha256"], "until": today, "reason": reason})
                cur.update({"axn": axn, "sha256": h, "date_derived": today}); rederived += 1
            else:
                a["observations"][slug] = {"axn": axn, "sha256": h, "obs_id": u.get("obs_id"), "date": u.get("date"), "surface": u.get("surface"),
                                           "file": f"/datasets/negative-of-the-negative/v2/sealed/{slug}.json", "date_derived": today}
                minted += 1
            files[slug] = b
    print(f"/non register: {len(led['addresses'])} addresses ({new_pos} new positions; next position {alloc['next_hex']} -> {nxt:04X}); "
          f"observations minted {minted}, shared with the Capture Registry {shared}, re-derived {rederived}")
    if not apply:
        return
    SEALED.mkdir(parents=True, exist_ok=True)
    for slug, b in files.items():
        (SEALED / f"{slug}.json").write_bytes(b)
    LEDGER.write_text(json.dumps(led, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if new_pos:
        alloc["next_hex"] = f"{nxt:04X}"; alloc["last_allocated"] = f"{nxt - 1:04X}"
        alloc["last_allocated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        alloc["last_allocator"] = "the /non register (scripts/nonreg_axn.py)"
        ALLOC.write_text(json.dumps(alloc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("applied")


if __name__ == "__main__":
    main()
