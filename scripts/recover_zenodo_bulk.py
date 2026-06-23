#!/usr/bin/env python3
"""
recover_zenodo_bulk.py — Extract Crimson Hexagonal Archive metadata from the Zenodo monthly bulk export.

Background
----------
On 2026-06-19, Zenodo terminated the leesharks000 account, removing 879 deposits and severing
1,817 DataCite DOIs from their public registration metadata. Zenodo publishes monthly metadata
snapshots; the snapshot generated 2026-06-07 (~12 days before termination) is the last
pre-termination capture. This script streams that 5.5 GB tar.gz from Zenodo, filters in-line
for the CHA record IDs, and writes one DataCite XML file per record to ./output/.

Reference: https://developers.zenodo.org/  (Bulk exporter section)

Usage
-----
    python3 recover_zenodo_bulk.py [--snapshot-url URL] [--output-dir DIR]

Expected runtime
----------------
At ~10 MB/sec network throughput, ~10 minutes for full pass through 5.5 GB.
At 1 MB/sec, ~80 minutes. The script prints progress every 100 MB processed.

Output
------
./output/<record_id>.xml — DataCite v4 XML, one per matched record. Approximately 1,500
files expected (the 1,675 unique severed DOIs minus those minted after 2026-06-07).

The script is idempotent: re-running skips files already written.
"""
import argparse
import gzip
import io
import json
import os
import sys
import tarfile
import time
import urllib.request

DEFAULT_SNAPSHOT_URL = (
    # 2026-06-07 head snapshot of global Zenodo records-xml.tar.gz (5.55 GB).
    # Get current URL/checksum from: curl -s https://zenodo.org/api/exporter
    "https://zenodo.org/api/exporter/records-xml.tar.gz/"
    "839f6c8b-29d0-438e-b8c9-602200a28bac"
)


def load_target_ids(resolution_index_path: str) -> set:
    """Read alexanarch's doi-resolution-index.json and return a set of Zenodo record IDs."""
    with open(resolution_index_path) as f:
        data = json.load(f)
    ids = set()
    for m in data.get('mappings', []):
        doi = m.get('dead_doi', '')
        if doi.startswith('10.5281/zenodo.'):
            try:
                rid = doi.split('zenodo.')[1]
                # Filter out the placeholder example DOIs (zenodo.1, .18, .189 etc)
                if int(rid) > 1000:
                    ids.add(rid)
            except ValueError:
                continue
    return ids


def stream_extract(url: str, target_ids: set, output_dir: str):
    """
    Stream the tar.gz from Zenodo through gzip → tarfile.
    Write only entries whose name matches <record_id>.xml for record_id ∈ target_ids.
    """
    os.makedirs(output_dir, exist_ok=True)
    already_have = {fn.replace('.xml', '') for fn in os.listdir(output_dir) if fn.endswith('.xml')}
    pending = target_ids - already_have
    print(f"Targets: {len(target_ids):,}  already have: {len(already_have):,}  pending: {len(pending):,}")

    if not pending:
        print("Nothing to do.")
        return

    req = urllib.request.Request(url, headers={
        'User-Agent': 'Alexanarch-Recovery/1.0 (mailto:archive@alexanarch.org)',
        'Accept-Encoding': 'identity',  # already gzipped at app level
    })

    bytes_read = 0
    last_progress = time.time()
    extracted = 0
    skipped = 0
    start = time.time()
    
    print(f"\nStreaming {url}\n")
    
    with urllib.request.urlopen(req, timeout=60) as resp:
        # Wrap resp with a counting reader for progress tracking
        class CountingReader:
            def __init__(self, fp):
                self.fp = fp
            def read(self, n=-1):
                nonlocal bytes_read, last_progress
                chunk = self.fp.read(n)
                bytes_read += len(chunk)
                now = time.time()
                if now - last_progress > 5:
                    mb = bytes_read / 1024 / 1024
                    speed = bytes_read / (now - start) / 1024 / 1024
                    print(f"  read {mb:,.1f} MB  ({speed:.1f} MB/s)  extracted {extracted}  pending {len(pending)-extracted}", flush=True)
                    last_progress = now
                return chunk
        
        counter = CountingReader(resp)
        
        # gzip → tar streaming
        with gzip.GzipFile(fileobj=counter, mode='rb') as gz:
            with tarfile.open(fileobj=gz, mode='r|') as tar:
                for member in tar:
                    if not member.isfile():
                        continue
                    name = os.path.basename(member.name)
                    if not name.endswith('.xml'):
                        continue
                    rid = name[:-4]  # strip .xml
                    if rid not in pending:
                        skipped += 1
                        continue
                    
                    # Extract
                    fp = tar.extractfile(member)
                    if fp is None:
                        continue
                    data = fp.read()
                    out_path = os.path.join(output_dir, name)
                    with open(out_path, 'wb') as f:
                        f.write(data)
                    extracted += 1
                    pending.discard(rid)
                    
                    if extracted % 50 == 0:
                        print(f"  ✓ {extracted} extracted, {len(pending)} pending  ({(time.time()-start)/60:.1f} min)", flush=True)
                    
                    if not pending:
                        print("All target records extracted.")
                        break

    elapsed = time.time() - start
    total_mb = bytes_read / 1024 / 1024
    print(f"\nDone in {elapsed/60:.1f} min  ({total_mb:.0f} MB read)")
    print(f"Extracted: {extracted}")
    print(f"Still missing: {len(pending)}")
    if pending:
        print("Missing IDs (likely minted after 2026-06-07 snapshot):")
        for r in sorted(pending, key=int)[:20]:
            print(f"  {r}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--snapshot-url', default=DEFAULT_SNAPSHOT_URL,
                   help="URL of the records-xml.tar.gz snapshot to stream")
    p.add_argument('--resolution-index', default='data/doi-resolution-index.json',
                   help="Path to alexanarch's DOI resolution index")
    p.add_argument('--output-dir', default='./output',
                   help="Where to write extracted <id>.xml files")
    args = p.parse_args()
    
    if not os.path.exists(args.resolution_index):
        print(f"ERROR: resolution index not found at {args.resolution_index}")
        print("Run this script from the alexanarch repo root, or pass --resolution-index.")
        sys.exit(1)
    
    target_ids = load_target_ids(args.resolution_index)
    print(f"Loaded {len(target_ids):,} target Zenodo record IDs")
    stream_extract(args.snapshot_url, target_ids, args.output_dir)


if __name__ == '__main__':
    main()
