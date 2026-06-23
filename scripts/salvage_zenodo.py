#!/usr/bin/env python3
"""salvage_zenodo.py — Phase 8.1 file salvage operation.

Goal: recover the original deposited byte streams from Zenodo before they
disappear. The metadata reconciliation passes (Phase 1-4) told us *what* was
deposited under which DOI. This tool retrieves *the files themselves*.

Run from Lee's residential machine. Datacenter IPs are blocked by Zenodo's
anti-scrape with a generic 403 ("unusual traffic from your network"). Lee's
home IP works.

Three modes:
    --dry-run        list record IDs that would be probed; no network calls
    --probe-only     hit REST endpoints, build ledger with per-file manifests
                     (filename, size, MD5, download URL) — no downloads
    --download       full download pass, MD5 verify, SHA-256 compute,
                     write bytes to recovered-originals/<id>/<filename>

Modes are additive: run --probe-only first to enumerate the salvage target,
then --download to fetch the bytes. Both are resume-safe — re-running skips
records that completed successfully.

Inputs:
    data/doi-resolution-index.json     source of record IDs (1,838 mappings)
    data/registry.json                 source of deposit_number ↔ DOI links

Outputs:
    data/file-recovery-ledger.json     master ledger of all records probed
    data/recovery-manifests/<id>.json  per-record manifest (committable JSON)
    recovered-originals/<id>/...       per-record bytes + manifest.json
    logs/salvage-<ts>.log              detailed log of the run

Politeness:
    User-Agent: Alexanarch-Salvage/1.0 (contact@alexanarch.org)
    Default rate limit: 1.0 req/sec (configurable via --rate)
    Exponential backoff on 429/503
    No authentication, all endpoints public
    Read-only — no destructive operations against Zenodo
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ───────────────────────────── module-local taxonomy import ───────────────
THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))
import recovery_status as RS  # noqa: E402

# ───────────────────────────── constants ──────────────────────────────────

USER_AGENT = "Alexanarch-Salvage/1.0 (contact@alexanarch.org; +https://alexanarch.org)"
ZENODO_HOST = "https://zenodo.org"
REPO_ROOT = THIS_DIR.parent
LEDGER_PATH = REPO_ROOT / "data" / "file-recovery-ledger.json"
MANIFESTS_DIR = REPO_ROOT / "data" / "recovery-manifests"
RECOVERED_DIR = REPO_ROOT / "recovered-originals"
LOG_DIR = REPO_ROOT / "logs"

DEFAULT_RATE = 1.0  # seconds between requests
MAX_FILE_BYTES = 500 * 1024 * 1024  # 500 MB per file, refuse anything larger
TIMEOUT = 60  # seconds


# ───────────────────────────── HTTP helpers ───────────────────────────────

class RateLimiter:
    def __init__(self, seconds_per_request):
        self.gap = max(0.0, float(seconds_per_request))
        self._last = 0.0

    def wait(self):
        now = time.monotonic()
        elapsed = now - self._last
        if elapsed < self.gap:
            time.sleep(self.gap - elapsed)
        self._last = time.monotonic()


def http_get_json(url, rate, log, max_retries=5):
    """GET a URL expecting JSON. Returns (status, body_dict_or_none, headers)."""
    return _http_get(url, rate, log, max_retries=max_retries, parse_json=True)


def http_get_bytes(url, rate, log, max_retries=5):
    """GET a URL expecting bytes. Returns (status, bytes_or_none, headers)."""
    return _http_get(url, rate, log, max_retries=max_retries, parse_json=False)


def _http_get(url, rate, log, max_retries, parse_json):
    rate.wait()
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/json" if parse_json else "*/*",
    })
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                body = r.read()
                hdrs = dict(r.headers.items())
                if parse_json:
                    try:
                        return r.status, json.loads(body.decode("utf-8")), hdrs
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        log(f"  ! non-JSON response from {url}: {e}")
                        return r.status, None, hdrs
                return r.status, body, hdrs
        except urllib.error.HTTPError as e:
            code = e.code
            hdrs = dict(e.headers.items()) if e.headers else {}
            if code in (429, 502, 503, 504) and attempt < max_retries - 1:
                sleep = (2 ** attempt) * rate.gap
                log(f"  ! HTTP {code} from {url}; backoff {sleep:.1f}s")
                time.sleep(sleep)
                continue
            try:
                body = e.read()
            except Exception:
                body = b""
            log(f"  ! HTTP {code} from {url}: {body[:200]!r}")
            return code, None, hdrs
        except urllib.error.URLError as e:
            if attempt < max_retries - 1:
                sleep = (2 ** attempt) * rate.gap
                log(f"  ! URL error on {url}: {e}; backoff {sleep:.1f}s")
                time.sleep(sleep)
                continue
            log(f"  ! URL error (final) on {url}: {e}")
            return 0, None, {}
        except Exception as e:
            log(f"  ! unexpected error on {url}: {type(e).__name__}: {e}")
            return 0, None, {}
    return 0, None, {}


# ───────────────────────────── record-id inventory ────────────────────────

RECORD_ID_RE = re.compile(r"10\.5281/zenodo\.(\d+)$")


def load_inventory():
    """Read the resolution index + registry to assemble the salvage target.

    Returns a list of dicts:
        {"record_id": "...", "doi": "10.5281/zenodo.NNN",
         "deposit_number": int_or_None, "axn": str_or_None, "title": str_or_None}
    """
    res_path = REPO_ROOT / "data" / "doi-resolution-index.json"
    reg_path = REPO_ROOT / "data" / "registry.json"

    targets = {}

    # 1. Resolution index — primary inventory
    with open(res_path) as f:
        res = json.load(f)
    for m in res.get("mappings", []):
        doi = m.get("dead_doi") or ""
        mrec = RECORD_ID_RE.search(doi)
        if not mrec:
            continue
        rid = mrec.group(1)
        if rid in targets:
            continue
        targets[rid] = {
            "record_id": rid,
            "doi": doi,
            "deposit_number": None,  # filled below
            "axn": m.get("axn"),
            "title": m.get("title"),
        }

    # 2. Registry — backfill deposit_number from sovereign_id / zenodo_dois
    with open(reg_path) as f:
        reg = json.load(f)
    for d in reg.get("deposits", []):
        dn = d.get("deposit_number")
        for doi in (d.get("zenodo_dois") or []):
            mrec = RECORD_ID_RE.search(doi)
            if not mrec:
                continue
            rid = mrec.group(1)
            if rid in targets and targets[rid].get("deposit_number") is None:
                targets[rid]["deposit_number"] = dn
                if not targets[rid].get("axn"):
                    targets[rid]["axn"] = d.get("axn")
                if not targets[rid].get("title"):
                    targets[rid]["title"] = d.get("title")
            elif rid not in targets:
                targets[rid] = {
                    "record_id": rid,
                    "doi": doi,
                    "deposit_number": dn,
                    "axn": d.get("axn"),
                    "title": d.get("title"),
                }

    inventory = sorted(targets.values(),
                       key=lambda t: int(t["record_id"]))
    return inventory


# ───────────────────────────── ledger state ───────────────────────────────

def load_ledger():
    if LEDGER_PATH.exists():
        with open(LEDGER_PATH) as f:
            return json.load(f)
    return {
        "schema_version": "v1.0",
        "purpose": ("Master ledger of file recovery state across all Zenodo "
                    "records once associated with the Crimson Hexagonal "
                    "Archive. Companion to registry.json (which carries "
                    "deposit-level recovery_status fields)."),
        "generated_at": None,
        "tool_version": "salvage_zenodo.py v1.0",
        "total_records_probed": 0,
        "by_status": {s: 0 for s in RS.ALL_STATUSES + [RS.STATUS_MIXED]},
        "records": [],
    }


def save_ledger(ledger):
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    ledger["generated_at"] = datetime.now(timezone.utc).isoformat()
    # Recompute by_status from records
    ledger["by_status"] = {s: 0 for s in RS.ALL_STATUSES + [RS.STATUS_MIXED]}
    for rec in ledger["records"]:
        s = rec.get("deposit_level_status")
        if s in ledger["by_status"]:
            ledger["by_status"][s] += 1
    ledger["total_records_probed"] = len(ledger["records"])
    with open(LEDGER_PATH, "w") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2, sort_keys=False)


def save_per_record_manifest(rec):
    """Write the per-record manifest to data/recovery-manifests/<id>.json.

    This is the committable surface — small JSON, in-repo, public record of
    what was attempted and recovered. The actual bytes live under
    recovered-originals/ (gitignored).
    """
    MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)
    path = MANIFESTS_DIR / f"{rec['record_id']}.json"
    with open(path, "w") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2, sort_keys=False)


# ───────────────────────────── probe + download ────────────────────────────

def probe_record(target, rate, log):
    """Hit REST endpoint, return a record entry for the ledger.

    Does not download file bytes. File entries get filename, size, MD5,
    download URL — and a recovery_status of FILE_MANIFEST_ONLY (because we
    know the file exists in Zenodo's index but have no bytes yet).
    """
    rid = target["record_id"]
    rest_url = f"{ZENODO_HOST}/api/records/{rid}"
    log(f"  → REST {rest_url}")

    code, data, hdrs = http_get_json(rest_url, rate, log)

    entry = {
        "record_id": rid,
        "doi": target["doi"],
        "deposit_number": target.get("deposit_number"),
        "axn": target.get("axn"),
        "title": target.get("title"),
        "probed_at": datetime.now(timezone.utc).isoformat(),
        "http_status_rest": code,
        "record_status": None,
        "files": [],
        "deposit_level_status": None,
        "errors": [],
    }

    if code == 200 and data:
        # Zenodo REST: data.status ∈ {"published","draft","unsubmitted",...}
        # For tombstoned records, the API may still return metadata.
        entry["record_status"] = data.get("status") or "published"
        # File listing in data.files (array)
        files = data.get("files") or []
        for f in files:
            md5_raw = f.get("checksum") or ""
            md5 = md5_raw[4:] if md5_raw.startswith("md5:") else md5_raw
            entry["files"].append({
                "filename": f.get("key") or "",
                "size_zenodo": f.get("size"),
                "md5_zenodo": md5,
                "mime_zenodo": f.get("mimetype"),
                "download_url": (f.get("links") or {}).get("self") or
                                f"{ZENODO_HOST}/records/{rid}/files/{f.get('key','')}",
                "local_path": None,
                "size_recovered": None,
                "md5_recovered": None,
                "md5_verified": None,
                "sha256_recovered": None,
                "retrieved_at": None,
                "http_status_download": None,
                "recovery_status": RS.STATUS_FILE_MANIFEST_ONLY,
            })
    elif code == 404:
        entry["record_status"] = "404"
        entry["errors"].append("record returned HTTP 404")
    elif code == 410:
        entry["record_status"] = "tombstoned"
        entry["errors"].append("record returned HTTP 410 Gone")
    elif code == 403:
        entry["errors"].append(
            "HTTP 403 — likely datacenter IP block. "
            "Run from a residential network."
        )
        return entry  # don't roll up — we don't know the state
    else:
        entry["errors"].append(f"unexpected HTTP {code}")

    # Compute deposit-level rollup
    if entry["files"]:
        entry["deposit_level_status"] = RS.rollup(
            [f["recovery_status"] for f in entry["files"]]
        )
    elif entry["record_status"] in ("404", "tombstoned"):
        entry["deposit_level_status"] = RS.STATUS_UNRECOVERED_FILE
    else:
        entry["deposit_level_status"] = RS.STATUS_METADATA_ONLY

    return entry


def download_files(entry, rate, log):
    """Pull bytes for every file in entry that doesn't yet have local_path."""
    rid = entry["record_id"]
    target_dir = RECOVERED_DIR / rid
    target_dir.mkdir(parents=True, exist_ok=True)

    for f in entry["files"]:
        if f.get("local_path") and Path(REPO_ROOT / f["local_path"]).exists():
            log(f"  · skip (already downloaded): {f['filename']}")
            continue
        url = f["download_url"]
        if not url:
            f["recovery_status"] = RS.STATUS_FILE_MANIFEST_ONLY
            continue
        if (f.get("size_zenodo") or 0) > MAX_FILE_BYTES:
            log(f"  · skip (too large): {f['filename']} = {f['size_zenodo']} bytes")
            f["recovery_status"] = RS.STATUS_FILE_MANIFEST_ONLY
            continue

        log(f"  ↓ GET {url}")
        code, body, hdrs = http_get_bytes(url, rate, log)
        f["http_status_download"] = code
        if code != 200 or body is None:
            f["recovery_status"] = RS.STATUS_FILE_MANIFEST_ONLY
            continue

        # Write to disk
        safe_name = _safe_filename(f["filename"])
        local_rel = f"recovered-originals/{rid}/{safe_name}"
        local_abs = REPO_ROOT / local_rel
        with open(local_abs, "wb") as fh:
            fh.write(body)

        # Hash
        md5 = hashlib.md5(body).hexdigest()
        sha = hashlib.sha256(body).hexdigest()

        f["local_path"] = local_rel
        f["size_recovered"] = len(body)
        f["md5_recovered"] = md5
        f["sha256_recovered"] = sha
        f["retrieved_at"] = datetime.now(timezone.utc).isoformat()

        if f.get("md5_zenodo"):
            f["md5_verified"] = (md5 == f["md5_zenodo"].lower())
            if f["md5_verified"]:
                f["recovery_status"] = RS.STATUS_ORIGINAL_FILE_RECOVERED
                log(f"  ✓ {safe_name}: MD5 verified")
            else:
                f["recovery_status"] = RS.STATUS_FILE_RECOVERED_UNVERIFIED
                log(f"  ! {safe_name}: MD5 MISMATCH "
                    f"(reported={f['md5_zenodo']}, got={md5})")
        else:
            f["md5_verified"] = None
            f["recovery_status"] = RS.STATUS_FILE_RECOVERED_UNVERIFIED
            log(f"  ✓ {safe_name}: recovered, no published checksum")

    # Also write a per-record manifest into the bytes directory
    if entry["files"]:
        mpath = target_dir / "manifest.json"
        with open(mpath, "w") as fh:
            json.dump(entry, fh, ensure_ascii=False, indent=2)

    # Recompute deposit-level rollup
    entry["deposit_level_status"] = RS.rollup(
        [f["recovery_status"] for f in entry["files"]]
    )


def _safe_filename(name):
    """Make a filename safe for the local filesystem while preserving most chars."""
    safe = re.sub(r'[/\\\x00-\x1f]', "_", name or "unnamed")
    if not safe.strip(): safe = "unnamed"
    if len(safe) > 200: safe = safe[:200]
    return safe


# ───────────────────────────── orchestration ──────────────────────────────

def make_logger(verbose):
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"salvage-{ts}.log"
    log_fh = open(log_path, "w")

    def log(msg):
        log_fh.write(msg + "\n")
        log_fh.flush()
        if verbose:
            print(msg, file=sys.stderr)
    log(f"# salvage_zenodo.py started {ts}")
    return log, log_path


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true",
                      help="list inventory; no network calls")
    mode.add_argument("--probe-only", action="store_true",
                      help="probe REST endpoints; build manifest entries; no downloads")
    mode.add_argument("--download", action="store_true",
                      help="full pass: probe + download bytes + verify checksums")

    p.add_argument("--limit", type=int, default=0,
                   help="limit to N records (0 = all)")
    p.add_argument("--rate", type=float, default=DEFAULT_RATE,
                   help=f"seconds between requests (default {DEFAULT_RATE})")
    p.add_argument("--skip-completed", action="store_true", default=True,
                   help="skip records already in ledger with terminal status (default)")
    p.add_argument("--force-rescan", action="store_true",
                   help="re-probe even if ledger has an entry")
    p.add_argument("--record-id", type=str, default=None,
                   help="probe only this record_id (overrides inventory)")
    p.add_argument("--quiet", action="store_true",
                   help="suppress stderr progress (logfile still written)")
    args = p.parse_args()

    log, log_path = make_logger(verbose=not args.quiet)

    # Inventory
    if args.record_id:
        inventory = [{"record_id": args.record_id, "doi": f"10.5281/zenodo.{args.record_id}",
                      "deposit_number": None, "axn": None, "title": None}]
    else:
        inventory = load_inventory()
    if args.limit > 0:
        inventory = inventory[:args.limit]
    log(f"Inventory: {len(inventory)} records")

    # Dry run — just print the inventory
    if args.dry_run:
        print(f"DRY RUN — {len(inventory)} records would be probed")
        print(f"  first 5: {[i['record_id'] for i in inventory[:5]]}")
        print(f"  last 5:  {[i['record_id'] for i in inventory[-5:]]}")
        print(f"  log:     {log_path}")
        return 0

    # Load existing ledger (resume-safe)
    ledger = load_ledger()
    existing = {r["record_id"]: r for r in ledger["records"]}
    log(f"Ledger: {len(existing)} existing record entries")

    rate = RateLimiter(args.rate)

    new_or_updated = 0
    skipped = 0
    errors = 0
    started = time.time()

    for i, target in enumerate(inventory, 1):
        rid = target["record_id"]
        prefix = f"[{i}/{len(inventory)}] record {rid}"
        log(prefix)

        existing_entry = existing.get(rid)
        # Decide whether to re-probe
        need_probe = (
            args.force_rescan
            or existing_entry is None
            or (args.download and any(
                f.get("recovery_status") == RS.STATUS_FILE_MANIFEST_ONLY
                for f in (existing_entry or {}).get("files", [])
            ))
        )
        # Probe (or reuse)
        if need_probe:
            entry = probe_record(target, rate, log)
            new_or_updated += 1
        else:
            entry = existing_entry
            skipped += 1

        # Download phase
        if args.download and entry.get("files"):
            download_files(entry, rate, log)

        if entry.get("errors"):
            errors += 1

        # Persist
        if existing_entry is not None:
            for j, r in enumerate(ledger["records"]):
                if r["record_id"] == rid:
                    ledger["records"][j] = entry
                    break
        else:
            ledger["records"].append(entry)

        # Save every 10 records to be crash-safe
        if i % 10 == 0:
            save_ledger(ledger)
            save_per_record_manifest(entry)

        save_per_record_manifest(entry)

    save_ledger(ledger)

    elapsed = time.time() - started
    log(f"# done in {elapsed:.1f}s — "
        f"probed {new_or_updated}, skipped {skipped}, errors {errors}")
    print()
    print(f"=== salvage_zenodo.py summary ===")
    print(f"  inventory:        {len(inventory)}")
    print(f"  probed:           {new_or_updated}")
    print(f"  skipped (cached): {skipped}")
    print(f"  errors:           {errors}")
    print(f"  elapsed:          {elapsed:.1f}s")
    print(f"  ledger:           {LEDGER_PATH.relative_to(REPO_ROOT)}")
    print(f"  manifests dir:    {MANIFESTS_DIR.relative_to(REPO_ROOT)}/")
    if args.download:
        print(f"  bytes dir:        {RECOVERED_DIR.relative_to(REPO_ROOT)}/")
    print(f"  log:              {log_path.relative_to(REPO_ROOT)}")
    print()
    print("Status counts in ledger:")
    for s, n in sorted(ledger["by_status"].items(), key=lambda x: -x[1]):
        if n:
            print(f"  {s}: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
