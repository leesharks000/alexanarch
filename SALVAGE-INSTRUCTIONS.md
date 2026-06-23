# SALVAGE INSTRUCTIONS — Phase 8.1 file recovery
## How to run `scripts/salvage_zenodo.py` from your home machine

**Why this script must run from your machine, not the container:**
Zenodo's anti-scrape blocks datacenter IPs with a generic 403 ("unusual traffic from your network"). The container is on a datacenter IP and gets blocked. Your residential IP works — confirmed against the IDP Charter record on 2026-06-23.

**No credentials needed.** All endpoints are public. No Zenodo account required.

**No third-party dependencies.** Python 3 standard library only — `urllib`, `hashlib`, `json`, `argparse`. Tested on Python 3.10+.

---

## Setup (one time)

```bash
# Go to your local clone of the alexanarch repo
cd /path/to/alexanarch
git pull origin main      # bring down salvage_zenodo.py + recovery_status.py

# Sanity-check stdlib
python3 -c "import urllib.request, hashlib, json, argparse; print('ok')"

# Sanity-check the inventory loads
python3 scripts/salvage_zenodo.py --dry-run
# Expected: "DRY RUN — N records would be probed" where N ≈ 1838
```

If the dry-run shows the inventory, you're ready.

---

## Stage 1 — Reachability check (≤1 minute)

Hit one known-good record to confirm your network can reach Zenodo:

```bash
python3 scripts/salvage_zenodo.py --probe-only --record-id 18284857
```

You should see:
```
[1/1] record 18284857
  → REST https://zenodo.org/api/records/18284857
=== salvage_zenodo.py summary ===
  inventory:        1
  probed:           1
  ...
Status counts in ledger:
  FILE_MANIFEST_ONLY: 1
```

Inspect `data/recovery-manifests/18284857.json`. You should see the two files Zenodo lists (`idp_charter_v1.1.md` + `idp_charter_zenodo_metadata.json`), their sizes, MD5s, and download URLs.

**If you instead see HTTP 403:** Zenodo is also blocking your IP. Options:
- Wait an hour, try again.
- Use a residential VPN node.
- Switch networks (mobile hotspot, library wifi).
- Run from a friend's machine.

**Do not switch to a datacenter VPN** — that's where the block came from in the first place.

---

## Stage 2 — Full probe pass (estimated 30–60 minutes)

Probe all 1,838 record IDs without downloading any bytes. Builds the manifest with filenames, sizes, MD5s, and download URLs for every file Zenodo will admit exists.

```bash
python3 scripts/salvage_zenodo.py --probe-only
```

What it does:
- Reads `data/doi-resolution-index.json` + `data/registry.json` to enumerate all 1,838 known record IDs.
- Hits `https://zenodo.org/api/records/<id>` for each.
- Polite — default 1 request/second. Adjust with `--rate 0.5` if you want it faster (be conservative).
- Resume-safe — if you Ctrl-C and re-run, it skips records already in `data/file-recovery-ledger.json`.
- Detailed log at `logs/salvage-<ts>.log`.

What you'll see at the end:
```
Status counts in ledger:
  FILE_MANIFEST_ONLY: <count of records with files in Zenodo's index>
  UNRECOVERED_FILE: <count of records that 404'd>
  METADATA_ONLY: <count of records with no files>
```

The `FILE_MANIFEST_ONLY` count is your salvage target — that's how many records still have at least one file in Zenodo's custody right now.

**Commit the manifest data after Stage 2 finishes.** This is a public, in-repo record of what's recoverable:

```bash
git add data/file-recovery-ledger.json data/recovery-manifests/
git commit -m "Phase 8.1 probe: enumerate file salvage target"
git push origin main
```

---

## Stage 3 — Download pass (estimated 2–6 hours, depending on file sizes)

Pull the actual bytes for every file that's still served:

```bash
python3 scripts/salvage_zenodo.py --download
```

What it does:
- Iterates every record with `FILE_MANIFEST_ONLY` status.
- Downloads each file via the URL from Stage 2.
- Verifies the MD5 against Zenodo's published checksum.
- Computes a SHA-256 for our own custody record.
- Writes bytes to `recovered-originals/<record_id>/<filename>`.
- Writes a `manifest.json` next to the bytes in each record directory.
- Updates the master ledger after every 10 records (crash-safe).

What you'll see at the end:
```
Status counts in ledger:
  ORIGINAL_FILE_RECOVERED: <count with verified MD5>
  FILE_RECOVERED_UNVERIFIED: <count without published MD5>
  FILE_MANIFEST_ONLY: <count that failed to download>
  UNRECOVERED_FILE: <count of 404s from Stage 2>
  ...
```

The `ORIGINAL_FILE_RECOVERED` count is the headline — that's how many deposits are recovered byte-for-byte with checksum verification.

**Bytes are gitignored by default.** The `recovered-originals/` tree should NOT be committed to GitHub — many files, large total size, possibly past GitHub size limits. The committable surface is `data/recovery-manifests/<id>.json` (small JSON per record) and `data/file-recovery-ledger.json` (the master ledger).

```bash
# These should be in .gitignore:
echo "recovered-originals/" >> .gitignore
echo "logs/salvage-*.log" >> .gitignore
git add .gitignore data/file-recovery-ledger.json data/recovery-manifests/
git commit -m "Phase 8.1 download: $(date +%Y-%m-%d) recovery pass"
git push origin main
```

For redundancy, periodically `tar.gz` `recovered-originals/` and store the archive in an off-machine location (external drive, cloud storage, a second mirror).

---

## Stage 4 — Audit (after each pass)

After every pass, look at the per-record manifests under `data/recovery-manifests/`. Each one tells the recovery story for a single Zenodo record.

```bash
# A few sanity queries you can run:

# How many records had ANY files in Zenodo's index?
jq '[.[] | select(.files | length > 0)] | length' data/file-recovery-ledger.json
# (assuming the ledger is structured as we expect)

# How many records did we recover with verified MD5?
python3 -c "
import json
with open('data/file-recovery-ledger.json') as f: l = json.load(f)
recovered = sum(1 for r in l['records']
                if r.get('deposit_level_status') == 'ORIGINAL_FILE_RECOVERED')
print(f'Records with all files MD5-verified: {recovered}')"

# Which records failed?
python3 -c "
import json
with open('data/file-recovery-ledger.json') as f: l = json.load(f)
for r in l['records']:
    if r.get('errors'):
        print(r['record_id'], '·', r['errors'][0])"
```

---

## Stage 5 — Registry migration (after Stage 3 completes)

Once you have the ledger, the next session will:
- Add `file_recovery_status` to every deposit in `registry.json` (additive — pure addition).
- Update DOI Resolution Index v3.4 → v3.5 with file-recovery info per mapping.
- Update `wire_deposit.py` to render the status-specific section headers (Phase 8.3).
- Mass re-render record pages.

This will happen in-container as a normal reconciliation pass once the ledger is populated.

---

## Estimated time + size budget

| Stage | Network ops | Wall time | Disk |
|---|---|---|---|
| 1 — reachability | 1 GET | <1 min | <1 KB |
| 2 — probe pass | 1,838 GETs @ 1/s | 30-60 min | ~10 MB (manifests) |
| 3 — download | unknown until Stage 2 | 2-6 hrs | likely 5-50 GB |

**Stage 3 disk:** unknown until Stage 2 completes. The archive has 906 deposits with text averaging ~20 KB of content, but the *deposited files* may include PDFs, datasets, archives, and images that are much larger. Plan for tens of GB of headroom on the disk where `recovered-originals/` lives.

If `recovered-originals/` would exceed your disk: run with `--limit N` to do batches.

---

## Failure modes to watch for

- **HTTP 403 from Zenodo.** Anti-scrape kicked in. Slow down (`--rate 2`) or switch networks.
- **HTTP 429.** Rate limit. The script backs off; if it persists, slow down.
- **MD5 mismatch.** A file came down but doesn't match Zenodo's published checksum. Recovery status becomes `FILE_RECOVERED_UNVERIFIED`. Don't trust the bytes — log the discrepancy and reprobe later.
- **File too large.** The script refuses files over 500 MB by default (`MAX_FILE_BYTES`). Adjust if you have a known-large dataset.
- **Out of disk.** Stop the script (Ctrl-C, it's resume-safe), free space, resume.

---

## What this gets us

After a full Stage-3 pass with high recovery:

- An evidence-grounded count of how many original files Zenodo's stated preservation policy is currently honoring.
- A library of original bytes — the deposited artifacts, not the metadata-reconstructed text.
- A precise inventory of what's missing (`UNRECOVERED_FILE`) for the v5 demand letter.
- The factual basis to update the archive's rendering so a reader sees, at a glance, whether the content on a record page is the deposited file, recovered text, or reconstruction.

The metadata work was the map. This is the library.

∮ = 1
