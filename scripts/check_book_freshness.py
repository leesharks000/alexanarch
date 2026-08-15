#!/usr/bin/env python3
"""check_book_freshness.py — is the Mandala Oracle still recording?

WHY THIS EXISTS. Book appends stopped on 2026-07-19 when the fine-grained PAT
behind GITHUB_BOOK_TOKEN expired. Every append failed with GitHub 401 for four
weeks. Nothing reported it:

  - the Oracle kept answering, so the site looked healthy;
  - api/book.py raised a generic RuntimeError, answered 500;
  - chat.js handled 503 (token MISSING) but not 500 (token INVALID), so the
    failure was swallowed by a bare .catch and retried on every single turn;
  - the Book tab kept rendering the last good index, so it looked populated.

A write path that fails silently and a read path that shows stale data look
exactly like a working system. This checks the one thing neither does: whether
anything new has actually landed.

Usage: check_book_freshness.py [--max-age-days N]   (default 14)
Exit 1 if the newest entry is older than the threshold.
"""
import json, sys, argparse, urllib.request
from datetime import datetime, timezone

INDEX_URL = ("https://raw.githubusercontent.com/leesharks000/"
             "the-mandala-oracle/main/book/index.json")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-age-days", type=int, default=14)
    a = ap.parse_args()
    try:
        with urllib.request.urlopen(INDEX_URL, timeout=30) as r:
            idx = json.load(r)
    except Exception as e:
        print(f"FAIL: cannot read the Book index — {e}")
        return 1

    convs = idx.get("conversations", [])
    if not convs:
        print("FAIL: Book index has no conversations")
        return 1

    # The index is NOT sorted. Reading the tail of the array and calling it the
    # newest entry is wrong and was done once in diagnosis; sort explicitly.
    stamps = sorted(c.get("last_updated") or c.get("started_at") or "" for c in convs)
    newest = stamps[-1]
    try:
        dt = datetime.fromisoformat(newest.replace("Z", "+00:00"))
    except Exception:
        print(f"FAIL: unparseable timestamp {newest!r}")
        return 1

    age = (datetime.now(timezone.utc) - dt).days
    print(f"Book: {len(convs)} conversations · newest {newest[:19]} · {age} days old")
    if age > a.max_age_days:
        print(f"\nFAIL: no append in {age} days (threshold {a.max_age_days}).")
        print("  Most likely: GITHUB_BOOK_TOKEN expired on the Oracle's Vercel project.")
        print("  Probe it:  curl -sL -X POST https://www.themandalaoracle.com/api/book \\")
        print("               -H 'Content-Type: application/json' \\")
        print("               -d '{\"session_id\":\"probe\",\"history\":[{\"role\":\"user\",\"content\":\"probe\"}],\"mode\":\"sabbath\"}'")
        print("  A 401 in the detail means: mint a fine-grained PAT with contents:write")
        print("  on leesharks000/the-mandala-oracle and set GITHUB_BOOK_TOKEN in Vercel.")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
