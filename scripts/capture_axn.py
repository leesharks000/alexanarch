#!/usr/bin/env python3
"""capture_axn.py — the AXN mint route of the Capture Registry (ruled 2026-10-27).

MANUS, 2026-10-27: "one observation / analysis / measure should have one axn. that is the unit of the capture
record, and i dont want summarizers citing the captures without the analysis. the summarizers had their chance to
compose from my work, and its recorded; and i have my opportunity to compose from their composition, as well -
thats what makes the captures an instrument, not just a record." On the position: "one position per address."

THE UNIT. Each observation of the registry (a run of the address's query on one surface, on one date), sealed with
its analysis and its measures, is one file:  data/captures/sealed/<observation slug>.json  — canonical JSON (keys
sorted, UTF-8, no insignificant whitespace) of
    observation   q, oq, q_kind, s, surface, sf, date, auth, ev, turns, transcript, transcript_raw,
                  transcript_cleaned, transcript_class, transcript_complete, transcript_read, model_attribution,
                  operator_disclosure, and each screenshot's file name with the SHA-256 of its bytes
    analysis      d, d_full, reading, analysis, findings, notes, match, match_note, mt, defects, heteronym,
                  originator, intended, notice, availability
    measures      per, per_v, per_note, per_corrected, per_dim, per_dim_v1_0, cites, cite_list,
                  archive_controlled_cites, sf_derived
The fields the builder generates (links, URLs, related-deposit joins, sibling lists, collisions, reruns, series,
longitudinal links, instrument metadata) are left out, so a rebuild changes nothing. The AXN is not written into
the sealed file.

THE POSITION. Each address (one registry record: one exact query string, per the record rule of 2026-08-13) takes
one position from the shared allocation ledger (data/symbolon-registry/allocation.json, rule max(registry hex,
ledger) + 1, advanced past each allocation). Its root AXN:<HEX>.CAPTURE names the address across its runs; each
observation is AXN:<HEX>.CAPTURE.<glyphs>, the glyphs derived (table v2.1) from the SHA-256 of its sealed file. A
later run at the address joins its position. When an observation's sealed bytes change (a corrected transcript, a
revised analysis or score), its AXN is re-derived and the earlier form kept in the ledger's history.

Ledger: data/captures/axn.json. The registry entries carry axn_root and, on each observation, axn.
    python3 scripts/capture_axn.py --check      # what would be minted or re-derived; writes nothing
    python3 scripts/capture_axn.py --apply [--date YYYY-MM-DD] [--reason "..."]
"""
import datetime, hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import axn_lib as A

REG = ROOT / "data/EA-WG-CAPTURES-01.json"
LEDGER = ROOT / "data/captures/axn.json"
SEALED = ROOT / "data/captures/sealed"
ALLOC = ROOT / "data/symbolon-registry/allocation.json"
FAMILY = "CAPTURE"
OBS = ["q", "oq", "q_kind", "s", "surface", "sf", "date", "auth", "ev", "turns", "transcript", "transcript_raw",
       "transcript_cleaned", "transcript_class", "transcript_complete", "transcript_read", "model_attribution",
       "operator_disclosure"]
ANA = ["d", "d_full", "reading", "analysis", "findings", "notes", "match", "match_note", "mt", "defects", "heteronym",
       "originator", "intended", "notice", "availability"]
MEA = ["per", "per_v", "per_note", "per_corrected", "per_dim", "per_dim_v1_0", "cites", "cite_list",
       "archive_controlled_cites", "sf_derived"]


def canon(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def img_sha(slug, name):
    for p in (ROOT / name.lstrip("/"), ROOT / "data/captures" / slug / name, ROOT / "data/captures-images" / name, ROOT / "data/captures-images" / pathlib.Path(name).name):
        if p.is_file():
            return hashlib.sha256(p.read_bytes()).hexdigest()
    return None


def observations(e):
    """The record's observations, each with the record-level fields it does not carry itself (the primary)."""
    obs = e.get("observations") or []
    if not obs:
        return [dict(e)]
    out = []
    for o in obs:
        x = dict(o)
        if o.get("slug") == e.get("slug"):
            for k in OBS + ANA + MEA + ["imgs"]:
                if k not in x and k in e:
                    x[k] = e[k]
        out.append(x)
    return out


def sealed(e, o):
    slug = o.get("slug") or e["slug"]
    body = {"observation": {k: o[k] for k in OBS if o.get(k) not in (None, "", [])},
            "analysis": {k: o[k] for k in ANA if o.get(k) not in (None, "", [])},
            "measures": {k: o[k] for k in MEA if o.get(k) not in (None, "", [])},
            "address": {"q": e.get("q"), "record": e["slug"]},
            "slug": slug}
    imgs = o.get("imgs") or []
    if imgs:
        body["observation"]["evidence_files"] = [{"file": str(i), "sha256": img_sha(e["slug"], str(i))} for i in imgs]
    return slug, canon(body)


def next_hex(alloc, reg_hex_max):
    return max(int(alloc["next_hex"], 16), reg_hex_max + 1)


def main():
    apply = "--apply" in sys.argv
    date = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else datetime.date.today().isoformat()
    reason = sys.argv[sys.argv.index("--reason") + 1] if "--reason" in sys.argv else "first mint"
    reg = json.loads(REG.read_text(encoding="utf-8"))
    led = json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {
        "_what_this_is": ("The AXN ledger of the Capture Registry: one position per address (root AXN:<HEX>.CAPTURE), one AXN per "
                          "observation sealed with its analysis and measures (AXN:<HEX>.CAPTURE.<glyphs>, glyphs from the SHA-256 of "
                          "data/captures/sealed/<observation>.json). history keeps every earlier form of an observation's AXN."),
        "family": FAMILY, "minted_by": "scripts/capture_axn.py", "glyph_table": A.AXN_GLYPH_TABLE, "addresses": {}}
    alloc = json.loads(ALLOC.read_text(encoding="utf-8"))
    deps = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]
    reg_max = max(int(d["hex"], 16) for d in deps if d.get("hex"))
    nxt = max(next_hex(alloc, reg_max), __import__('axn_positions').next_free())  # 2026-10-28: the floor includes origin/main (no stale-checkout collisions)
    order = sorted(reg["entries"], key=lambda e: (min([str(o.get("date") or "") for o in observations(e)] or [""]), e["slug"]))
    new_pos, minted, rederived, files = 0, 0, 0, {}
    for e in order:
        a = led["addresses"].get(e["slug"])
        if not a:
            hx = f"{nxt:04X}"; nxt += 1; new_pos += 1
            a = led["addresses"][e["slug"]] = {"hex": hx, "root": f"AXN:{hx}.{FAMILY}", "q": e.get("q"), "addr_id": e.get("addr_id"),
                                               "allocated": date, "observations": {}}
        for o in observations(e):
            slug, b = sealed(e, o)
            h = hashlib.sha256(b).hexdigest()
            axn = A.derive_axn(h, a["hex"], FAMILY)
            cur = a["observations"].get(slug)
            if cur and cur["sha256"] == h:
                continue
            if cur:
                cur.setdefault("history", []).append({"axn": cur["axn"], "sha256": cur["sha256"], "until": date, "reason": reason})
                cur.update({"axn": axn, "sha256": h, "date_derived": date, "surface": o.get("surface")}); rederived += 1   # the surface follows the record (repair of 0B15, 2026-10-30)
            else:
                a["observations"][slug] = {"axn": axn, "sha256": h, "obs_id": o.get("obs_id"), "date": o.get("date"),
                                           "surface": o.get("surface"), "file": f"/data/captures/sealed/{slug}.json", "date_derived": date}
                minted += 1
            files[slug] = b
    print(f"addresses: {len(led['addresses'])} ({new_pos} new positions; next position {alloc['next_hex']} -> {nxt:04X}); "
          f"observations minted {minted}, re-derived {rederived}")
    if not apply:
        return
    SEALED.mkdir(parents=True, exist_ok=True)
    for slug, b in files.items():
        (SEALED / f"{slug}.json").write_bytes(b)
    LEDGER.write_text(json.dumps(led, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for e in reg["entries"]:
        a = led["addresses"][e["slug"]]
        e["axn_root"] = a["root"]
        for o in (e.get("observations") or []):
            if o.get("slug") in a["observations"]:
                o["axn"] = a["observations"][o["slug"]]["axn"]
        if e["slug"] in a["observations"]:
            e["axn"] = a["observations"][e["slug"]]["axn"]
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if new_pos:
        last = f"{nxt - 1:04X}"
        alloc["next_hex"] = f"{nxt:04X}"; alloc["last_allocated"] = last
        alloc["last_allocated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        alloc["last_allocator"] = "capture-registry (scripts/capture_axn.py)"
        ALLOC.write_text(json.dumps(alloc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("applied")


if __name__ == "__main__":
    main()
