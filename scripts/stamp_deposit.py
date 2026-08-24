#!/usr/bin/env python3
"""stamp_deposit.py — symbolon-stamp a deposit's canonical bytes.

Implements the https://axnidentifiers.org/stamp/ client algorithm (AXN-SYMBOLON-SPEC
v0.3, chiastic/addressed inscription, stamp_generation 2) for archive deposits, and
registers the pairing through the public witness endpoint:

  axn0 = SHA-256 of the CANONICAL bytes (== the registry `hash`) — the sealed core.
  stamped copy = canonical + suffix comment block carrying the deposit's full AXN,
                 the kernel glyphs, hash, date, and spec line. This is the
                 DISTRIBUTION artifact — what circulates outside the archive.
  axn1 = SHA-256 of the stamped copy — tamper witness of the circulating form.
  Seed A sidecar → POST /api/register-symbolon with store = THE SEALED CORE
                 (the endpoint refuses, correctly, to store any bytes that do not
                 hash to axn0 — the archive stores only the core; the stamped copy
                 travels).

First use: deposit #1540 (2026-08-24), allocated AXN:063C.GOVERNANCE and
witnessed-verified; store verifier at 33 cores, 0 alerts.

Notes:
  - One endpoint call = one GitHub commit by the symbolon service = one deploy.
    Fine at mint cadence; do NOT loop this over the back catalog without a batch
    plan (allocation semantics live server-side — a local batch writer would have
    to replicate them exactly, which is a MANUS ruling, not a script default).
  - Idempotent: skips if entries/{axn0}.json already exists in the live registry.
  - Canonical bytes are never modified. The stamp is a copy operation.

Usage:
  python3 scripts/stamp_deposit.py --deposit-number 1540 [--out /tmp/AXN-063A.stamped.md] [--dry-run]
"""
import argparse, base64, datetime, hashlib, json, pathlib, sys, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from axn_lib import axn_glyph_from_hash  # single source of glyph truth

ENDPOINT = "https://www.alexanarch.org/api/register-symbolon"
ENTRIES = "https://www.alexanarch.org/data/symbolon-registry/entries/{}.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deposit-number", type=int, required=True)
    ap.add_argument("--out", help="path for the stamped circulating copy "
                                  "(default: /tmp/AXN-{hex}.stamped.md)")
    ap.add_argument("--dry-run", action="store_true",
                    help="build stamp + sidecar; do not POST")
    args = ap.parse_args()

    reg = json.load(open(ROOT / "data" / "registry.json"))
    d = next((x for x in reg["deposits"]
              if x.get("deposit_number") == args.deposit_number), None)
    if not d:
        sys.exit(f"deposit #{args.deposit_number} not in registry")
    hexid = d.get("hex") or ""
    # Resolve the SEALED CORE by hash. For most deposits full_text_path bytes ==
    # registry hash. Facsimile deposits (body_status: primary-source-facsimile,
    # e.g. #1539) deliberately diverge: full_text_path serves the page-image
    # reader while data/deposits/AXN-{hex}.md preserves the mint bytes the
    # registry hash anchors. The core is whichever surface hashes to the
    # registry hash — never a guess.
    candidates = [(d.get("full_text_path") or f"/data/texts/AXN-{hexid}-text.md").lstrip("/"),
                  f"data/deposits/AXN-{hexid}.md",
                  f"data/texts/AXN-{hexid}-text.md"]
    canon, path, h0 = None, None, None
    tried = []
    for p in dict.fromkeys(candidates):
        fp = ROOT / p
        if not fp.exists():
            continue
        b = fp.read_bytes()
        h = hashlib.sha256(b).hexdigest()
        tried.append(f"{p}={h[:12]}")
        if not d.get("hash") or h == d["hash"]:
            canon, path, h0 = b, p, h
            break
    if canon is None:
        sys.exit(f"REFUSING: no canonical surface hashes to registry hash "
                 f"{(d.get('hash') or '?')[:12]} — tried {tried}; repair the "
                 f"divergence before stamping")
    g0 = axn_glyph_from_hash(h0)

    # idempotency: already witnessed?
    try:
        with urllib.request.urlopen(ENTRIES.format(h0), timeout=30) as r:
            prior = json.load(r)
            print(f"already witnessed: {prior.get('axn')} ({prior.get('status')}) — nothing to do")
            return
    except Exception:
        pass  # not found → proceed

    today = datetime.date.today().isoformat()
    stamp = (f"\n\n<!-- AXN-STAMP-BEGIN\nAXN: {d['axn']}\nAXN-KERNEL: {g0}\n"
             f"SHA256: {h0}\nDATE: {today}\n"
             f"SPEC: AXN-SYMBOLON-SPEC v0.3 (chiastic inscription)\nAXN-STAMP-END -->\n")
    stamped = canon + stamp.encode()
    h1 = hashlib.sha256(stamped).hexdigest()
    g1 = axn_glyph_from_hash(h1)

    out = pathlib.Path(args.out or f"/tmp/AXN-{hexid}.stamped.md")
    out.write_bytes(stamped)

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    seed = {
        "axn_spec": "AXN-SYMBOLON-SPEC v0.2",
        "spec_record": "https://www.alexanarch.org/s/records/1432/",
        "spec_axn": "AXN:05A9.OPERATIVE.🐚🌪️🕖🫵⏩○",
        "reconstruction_class": "content-addressed",
        "stamp_generation": 2,
        "axn0": {"glyphs": g0, "sha256": h0,
                 "role": "identity kernel of the sealed core (the original, pre-stamp bytes)"},
        "axn1": {"glyphs": g1, "sha256": h1,
                 "role": "kernel of the stamped file as it circulates (tamper witness; not a name)"},
        "manifest": [{"part": 1, "filename": pathlib.Path(path).name,
                      "sha256": h0, "bytes": len(canon)}],
        "stamp_geometry": {"format": "text", "method": "suffix_comment_block",
                           "delimiters": ["<!-- AXN-STAMP-BEGIN", "AXN-STAMP-END -->"],
                           "strip_reversible": True},
        "created": now,
        "generator": "scripts/stamp_deposit.py (in-session, transport D; algorithm per https://axnidentifiers.org/stamp/)",
        "family": d.get("family", "GOVERNANCE"),
        "deposit_number": d["deposit_number"],
        "deposit_axn": d["axn"],
        "registration": "kernel is authority-independent; registry witnessing via " + ENDPOINT,
    }
    sidecar = out.with_suffix(".axn.json")
    sidecar.write_text(json.dumps(seed, indent=1, ensure_ascii=False))
    print(f"axn0 {g0} {h0[:16]}…  axn1 {g1} {h1[:16]}…")
    print(f"stamped copy: {out}  sidecar: {sidecar}")

    if args.dry_run:
        print("dry run — not registered")
        return
    payload = dict(seed, store={"filename": pathlib.Path(path).name,
                                "content_b64": base64.b64encode(canon).decode()})
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"},
                                 method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            resp = json.load(r)
            print(f"witnessed: {r.status} {resp.get('status')} → {resp.get('axn')}")
            print(f"record: {resp.get('record')}")
    except urllib.error.HTTPError as err:
        sys.exit(f"endpoint refused: {err.code} {err.read().decode()[:300]}")


if __name__ == "__main__":
    main()
