#!/usr/bin/env python3
"""indexnow_submit.py — notify participating engines the moment a record lands.

WHY
---
Passive discovery makes a deposit wait for a crawler that has no reason to come
back. IndexNow inverts that: the archive tells the index it changed. Google does
not participate, but Bing, Yandex, Naver and Seznam do — and those are the
substrates behind several composition systems whose reception behavior this
archive exists to measure. Getting a deposit into that index quickly is not a
marketing act here; it is the difference between a work being available to the
layer under study and being absent from it.

WHAT COUNTS AS A SUBMISSION-WORTHY EVENT
----------------------------------------
The same rule as date_modified (scripts/record_modification.py): the record
changed. A new mint, a corrected title, a seated body, a repaired pointer.
NOT: page regeneration, enrichment passes, derived-surface rebuilds. Submitting
unchanged URLs teaches the endpoint to discount the source, which is the same
failure mode as stamping <lastmod> on every sweep.

LEDGER
------
Every submission is recorded in data/indexnow-ledger.json with the URL, the
timestamp, the endpoint response, and the reason. Acceptance means the
notification was received — never that anything was indexed — and the ledger
says so in its own schema rather than letting a 200 be read as success.

USAGE
  python3 scripts/indexnow_submit.py --deposits 1425
  python3 scripts/indexnow_submit.py --deposits 1425,1426 --reason "title correction"
  python3 scripts/indexnow_submit.py --all            # full-corpus push (rare)
  python3 scripts/indexnow_submit.py --since 2026-07-30
"""
import argparse
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = "www.alexanarch.org"
KEY = "3249baca550fef5539f92f7e652e9187"
ENDPOINTS = ["https://api.indexnow.org/IndexNow", "https://www.bing.com/indexnow"]
LEDGER = ROOT / "data" / "indexnow-ledger.json"
BATCH = 10000  # protocol maximum


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def record_url(n):
    return f"https://{HOST}/s/records/{n}/"


def submit(urls, endpoint=ENDPOINTS[0]):
    """POST a batch. Returns (status_code, note). Never raises on HTTP error."""
    payload = json.dumps({
        "host": HOST, "key": KEY,
        "keyLocation": f"https://{HOST}/{KEY}.txt",
        "urlList": urls,
    }).encode()
    req = urllib.request.Request(
        endpoint, data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, "received"
    except urllib.error.HTTPError as e:
        return e.code, {
            400: "bad request", 403: "key not valid for host",
            422: "urls do not belong to host", 429: "rate limited",
        }.get(e.code, "http error")
    except Exception as e:
        return 0, f"transport: {e}"


def load_ledger():
    if LEDGER.exists():
        return json.loads(LEDGER.read_text())
    return {
        "$schema": "https://www.alexanarch.org/schemas/indexnow-ledger.json",
        "name": "IndexNow submission ledger",
        "description": (
            "Record of URLs announced to IndexNow participants. A 200 or 202 "
            "response means the notification was RECEIVED. It does not mean the "
            "URL was crawled, and it does not mean the URL was indexed. This "
            "ledger records what the archive said, not what any engine did."),
        "host": HOST, "submissions": [],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deposits", help="comma-separated deposit numbers")
    ap.add_argument("--all", action="store_true", help="full-corpus push")
    ap.add_argument("--since", help="deposits with date_modified or date >= YYYY-MM-DD")
    ap.add_argument("--reason", default="deposit minted or record modified")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    reg = json.loads((ROOT / "data" / "registry.json").read_text())
    deps = reg["deposits"]
    if a.deposits:
        want = {int(x) for x in a.deposits.split(",") if x.strip()}
        sel = [d for d in deps if d.get("deposit_number") in want]
    elif a.since:
        sel = [d for d in deps
               if (d.get("date_modified") or d.get("date") or "") >= a.since]
    elif a.all:
        sel = deps
    else:
        ap.error("one of --deposits / --since / --all is required")

    urls = [record_url(d["deposit_number"]) for d in sel if d.get("deposit_number")]
    if not urls:
        print("  [indexnow] nothing to submit")
        return
    print(f"  [indexnow] {len(urls)} url(s) · {a.reason}")
    if a.dry_run:
        for u in urls[:5]:
            print("   ", u)
        return

    ledger = load_ledger()
    for i in range(0, len(urls), BATCH):
        batch = urls[i:i + BATCH]
        code, note = submit(batch)
        if code not in (200, 202):           # one retry on the alternate endpoint
            code2, note2 = submit(batch, ENDPOINTS[1])
            if code2 in (200, 202):
                code, note = code2, note2 + " (via bing endpoint)"
        ledger["submissions"].append({
            "submitted_at": now(), "count": len(batch),
            "response": code, "note": note, "reason": a.reason,
            "urls": batch if len(batch) <= 50 else batch[:50] + ["…truncated"],
            "meaning": "notification received; not a crawl and not an index event",
        })
        print(f"  [indexnow] batch {len(batch)} → {code} ({note})")
    LEDGER.write_text(json.dumps(ledger, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"  [indexnow] ledger: {LEDGER.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
