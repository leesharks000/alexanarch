#!/usr/bin/env python3
"""
build_snapshots.py — pull GoatCounter Stats Export API for each configured
site, write data/view-counts.json (path-keyed) and data/network-witness.json
(network-wide roll-up).

Design principles (see docs/counter-architecture.md):
  - Fail loudly on API errors; do NOT write zeroed data over the prior snapshot.
  - Preserve prior snapshot verbatim if the run fails mid-way for a given site.
  - Only overwrite a site's entry on a fully-successful pull for that site.
  - Aggregated network total is computed only from sites that reported cleanly
    in the current run (partial roll-ups are marked with `partial: true`).

Configuration:
  - data/goatcounter-sites.json declares which sites to poll and which env var
    holds the API key for each.
  - API keys are read from environment variables (GitHub Actions secrets),
    never from files or logs.

GoatCounter API endpoints used (v0):
  GET /api/v0/me            → verify token, return site info (canary check)
  GET /api/v0/stats/total   → site total pageviews (all-time by default)
  GET /api/v0/stats/hits    → per-path aggregation, paginated

Bearer token in Authorization header. Docs: https://www.goatcounter.com/api
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "data" / "goatcounter-sites.json"
VIEW_COUNTS_PATH = REPO_ROOT / "data" / "view-counts.json"
NETWORK_WITNESS_PATH = REPO_ROOT / "data" / "network-witness.json"

REQUEST_TIMEOUT = 30
PAGINATION_LIMIT = 100          # server cap for /stats/hits (spec); paginate with exclude_paths
INTER_REQUEST_SLEEP = 0.35      # be polite to the API even from CI


class GoatCounterError(RuntimeError):
    pass


def _get(url: str, token: str) -> dict[str, Any]:
    """One authenticated GET against a GoatCounter API URL."""
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": "alexanarch-snapshot/1.0 (+https://alexanarch.org)",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:500] if e.fp else ""
        raise GoatCounterError(f"HTTP {e.code} on {url}: {detail}") from e
    except urllib.error.URLError as e:
        raise GoatCounterError(f"URL error on {url}: {e.reason}") from e
    except json.JSONDecodeError as e:
        raise GoatCounterError(f"non-JSON response from {url}: {e}") from e


def _canary(host: str, token: str) -> None:
    """/api/v0/me: verify token works before doing expensive pulls.

    2026-08-12 — the 11 August run failed here with HTTP 404 and the message
    said only that. Probing the host WITHOUT a token returns 401, which means
    the endpoint and host are correct and present. GoatCounter answers 404
    rather than 403 for a token it does not recognise — a deliberate
    non-disclosure. So a 404 HERE means the TOKEN IS GONE (deleted, revoked, or
    the secret was rotated), not that the API moved or the site vanished.

    That distinction cost a day of misdiagnosis across three audits, so the
    error now states it rather than leaving the next reader to rediscover it.
    """
    # 2026-09-02: the hosted API answers 404 (and 502) TRANSIENTLY — the same
    # secret failed at 19:20Z and succeeded at 19:24Z on identical code. So a
    # single 404 is not proof the token is gone; three in a row, spaced, is.
    last = None
    for attempt in range(3):
        try:
            _get(f"{host}/api/v0/me", token)
            return
        except GoatCounterError as e:
            last = e
            if attempt < 2 and ("HTTP 404" in str(e) or "HTTP 502" in str(e) or "HTTP 503" in str(e)):
                time.sleep(20 * (attempt + 1))
                continue
            break
    try:
        raise last
    except GoatCounterError as e:
        msg = str(e)
        if "HTTP 404" in msg:
            raise GoatCounterError(
                f"{msg}\n"
                f"    DIAGNOSIS: /api/v0/me exists — unauthenticated it returns 401, not 404.\n"
                f"    GoatCounter answers 404 for a token it does not recognise — but also, transiently, for a valid one (three spaced attempts all 404'd).\n"
                f"    THE API TOKEN IS INVALID OR HAS BEEN DELETED.\n"
                f"    FIX: {host}/user/api → create a token with 'Read statistics'\n"
                f"         then update the GOATCOUNTER_API_KEY repository secret.\n"
                f"    This is NOT an API deprecation and NOT a site outage; the /count\n"
                f"    tracker endpoint is a separate path and keeps collecting regardless."
            ) from e
        if "HTTP 401" in msg:
            raise GoatCounterError(
                f"{msg}\n    DIAGNOSIS: token present but rejected — check it was copied whole."
            ) from e
        raise


# ── THE WINDOW (2026-09-02) ──────────────────────────────────────────────────
# GoatCounter's /stats/total and /stats/hits are NOT all-time by default: per
# the published API spec (https://www.goatcounter.com/api.json) `start`
# defaults to ONE WEEK AGO and `end` to now. Every snapshot this script wrote
# before today was therefore the trailing seven days, published as the
# archive's all-time total, and per-record counts silently reset each week
# (2026-09-01 snapshot: "total=838" was one week of visitors). Both endpoints
# now get an explicit window from the archive's founding to the current hour.
SITE_EPOCH = "2026-06-19T00:00:00Z"   # alexanarch founding; GoatCounter site predates no traffic

def _window() -> dict[str, str]:
    now = dt.datetime.now(dt.timezone.utc).replace(minute=0, second=0, microsecond=0)
    return {"start": SITE_EPOCH, "end": now.strftime("%Y-%m-%dT%H:%M:%SZ")}


def _get_total(host: str, token: str) -> tuple[int, int]:
    """/api/v0/stats/total over the explicit all-time window. Returns (total, 0).

    `total` is GoatCounter's count of VISITORS (its unit since v2; there is no
    separate pageview or "unique" figure in the API). The second element is
    kept at 0 for schema stability with consumers that read total_unique.
    """
    url = f"{host}/api/v0/stats/total?{urllib.parse.urlencode(_window())}"
    data = _get(url, token)
    total = int(data.get("total", 0))
    return total, 0


def _get_hits_all_pages(host: str, token: str) -> list[dict[str, Any]]:
    """/api/v0/stats/hits over the all-time window, paginated the way the API
    actually paginates.

    There is no `after` cursor. The spec's mechanism is `exclude_paths` (path
    IDs already received) with `limit` (server-capped at 100), and a `more`
    flag. The previous single-page fetch returned exactly 100 paths and
    stopped, so every record outside the top hundred had no count at all.
    """
    hits: list[dict[str, Any]] = []
    seen_ids: list[int] = []
    page = 0
    base = _window()
    while True:
        page += 1
        if page > 200:
            raise GoatCounterError("pagination runaway (>200 pages)")
        qs: dict[str, Any] = dict(base)
        qs["limit"] = PAGINATION_LIMIT
        if seen_ids:
            qs["exclude_paths"] = ",".join(str(i) for i in seen_ids)
        url = f"{host}/api/v0/stats/hits?{urllib.parse.urlencode(qs)}"
        data = _get(url, token)
        page_hits = data.get("hits", []) or []
        if not isinstance(page_hits, list):
            raise GoatCounterError(f"'hits' not a list at {url}: {type(page_hits)}")
        if not page_hits:
            break
        hits.extend(page_hits)
        new_ids = [int(h["path_id"]) for h in page_hits if h.get("path_id") is not None]
        if not new_ids:
            break
        seen_ids.extend(new_ids)
        if not data.get("more"):
            break
        time.sleep(INTER_REQUEST_SLEEP)
    return hits


def _fold_hits_to_paths(hits: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    """Reduce API hits list into a path → {count, count_unique} map.

    GoatCounter may return per-day arrays; if so, we sum. If a hit already has
    scalar `count` / `count_unique`, we take them as-is.
    """
    out: dict[str, dict[str, int]] = {}
    for h in hits:
        path = h.get("path") or h.get("name")
        if not path:
            continue
        # Scalar shape
        if "count" in h and not isinstance(h["count"], list):
            count = int(h.get("count") or 0)
            count_unique = int(h.get("count_unique") or 0)
        else:
            # Array shape: sum per-day
            count = sum(int(x.get("count") or 0) for x in (h.get("stats") or []))
            count_unique = sum(int(x.get("count_unique") or 0) for x in (h.get("stats") or []))
        # Merge (defensive; same path shouldn't appear twice, but be safe)
        cur = out.get(path, {"count": 0, "count_unique": 0})
        out[path] = {
            "count": cur["count"] + count,
            "count_unique": cur["count_unique"] + count_unique,
        }
    return out


def _now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def pull_site(site_cfg: dict[str, Any], dry_run: bool = False) -> dict[str, Any]:
    """Pull one site. Returns a site-result dict for network-witness.json.

    Raises GoatCounterError on any failure. Side effect: if this site is
    configured with include_paths_in_view_counts=true, updates view-counts.json.
    """
    domain = site_cfg["domain"]
    host = site_cfg["goatcounter_host"].rstrip("/")
    api_env = site_cfg["api_env_var"]

    token = os.environ.get(api_env)
    if not token:
        raise GoatCounterError(
            f"missing {api_env} env var (repo secret) for {domain}; refusing to run"
        )

    print(f"[{domain}] canary check via {host}/api/v0/me")
    _canary(host, token)

    print(f"[{domain}] fetching site total")
    total, total_unique = _get_total(host, token)
    print(f"[{domain}] total={total:,}  total_unique={total_unique:,}")

    site_result = {
        "total": total,
        "total_unique": total_unique,
        "source": "goatcounter",
        "goatcounter_host": host,
        "as_of": _now_iso(),
    }

    if site_cfg.get("include_paths_in_view_counts", False):
        print(f"[{domain}] fetching path-level hits (paginated)")
        hits = _get_hits_all_pages(host, token)
        paths_map = _fold_hits_to_paths(hits)
        print(f"[{domain}] path-level counts collected: {len(paths_map):,} paths")

        snapshot = {
            "schema_version": "v1",
            "generated_at": _now_iso(),
            "generator": "goatcounter-snapshot workflow",
            "source": host,
            "total": total,
            "total_unique": total_unique,
            "paths": paths_map,
        }
        if not dry_run:
            _write_json(VIEW_COUNTS_PATH, snapshot)
            print(f"[{domain}] wrote {VIEW_COUNTS_PATH.relative_to(REPO_ROOT)}")
        else:
            print(f"[{domain}] DRY RUN — would write view-counts.json ({len(paths_map)} paths)")

    return site_result


def main() -> int:
    ap = argparse.ArgumentParser(description="Build view-count snapshots from GoatCounter.")
    ap.add_argument("--dry-run", action="store_true", help="Do not write output files")
    args = ap.parse_args()

    cfg = json.loads(CONFIG_PATH.read_text())
    sites = cfg.get("sites", [])
    if not sites:
        print(f"no sites configured in {CONFIG_PATH.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 2

    # Preserve prior network-witness on partial success
    prior_network = _load_json(NETWORK_WITNESS_PATH, {"sites": {}})
    prior_sites = prior_network.get("sites", {}) if isinstance(prior_network, dict) else {}

    new_sites: dict[str, Any] = {}
    failures: list[tuple[str, str]] = []

    for site_cfg in sites:
        domain = site_cfg["domain"]
        try:
            new_sites[domain] = pull_site(site_cfg, dry_run=args.dry_run)
        except GoatCounterError as e:
            print(f"[{domain}] FAILED: {e}", file=sys.stderr)
            failures.append((domain, str(e)))
            # Keep the prior entry rather than dropping the site from the roll-up
            if domain in prior_sites:
                kept = dict(prior_sites[domain])
                kept["as_of_note"] = f"stale — pull failed at {_now_iso()}"
                new_sites[domain] = kept

    # Compute network totals from *fresh* entries only (not stale carry-forwards)
    fresh_domains = {d for d in new_sites if "as_of_note" not in new_sites[d]}
    network_total = sum(new_sites[d]["total"] for d in fresh_domains)
    network_total_unique = sum(new_sites[d].get("total_unique", 0) for d in fresh_domains)

    witness = {
        "schema_version": "v1",
        "generated_at": _now_iso(),
        "generator": "goatcounter-snapshot workflow",
        "network_total": network_total,
        "network_total_unique": network_total_unique,
        "partial": bool(failures),
        "sites": new_sites,
    }
    if failures:
        witness["failures"] = [{"domain": d, "reason": r} for d, r in failures]

    if not args.dry_run:
        _write_json(NETWORK_WITNESS_PATH, witness)
        print(f"wrote {NETWORK_WITNESS_PATH.relative_to(REPO_ROOT)}")
    else:
        print(f"DRY RUN — would write network-witness.json (network_total={network_total:,})")

    # Exit non-zero if any site failed (even if others succeeded)
    if failures:
        print(f"partial success: {len(failures)}/{len(sites)} sites failed", file=sys.stderr)
        return 1
    print(f"all sites succeeded: network_total={network_total:,}, network_total_unique={network_total_unique:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
