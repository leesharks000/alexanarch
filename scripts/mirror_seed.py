#!/usr/bin/env python3
"""mirror_seed.py — make the archive cheap to keep.

THE PROBLEM THIS ADDRESSES (2026-09-10). A machine reader asked to assess the archive's
long-term survival named the unmet threshold as INDEPENDENT CUSTODIANSHIP: until parties
other than the originating creator preserve it, survival is a one-person dependency. The
operator's response was that nobody will volunteer, which is almost certainly correct and
is the normal case for archives.

The custody that actually works is INDIFFERENT, not committed. Nobody decided to preserve
most of what survives; a pipeline ingested it because ingesting was cheap. Software Heritage
crawls public git repositories and keeps them permanently, with no relationship to the
author and no opinion about the contents. It cannot be talked out of it and does not have
to care.

WHAT THIS SCRIPT FOUND. alexanarch is ALREADY THERE — ten visits, most recent full snapshot
2026-09-09, roughly every two days. The fleet is not: the surfaces that carry the heteronym
/who/ pages, the MPAI catalogue, and the Pessoa lineage graph return 404. So the archive's
core is redundantly held and the surrounding apparatus is not.

    python3 scripts/mirror_seed.py --check          report ingest status for every repo
    python3 scripts/mirror_seed.py --save           request ingest for the ones missing

Save Code Now is a public, unauthenticated endpoint with a rate limit; requests are queued,
not immediate. Re-running is safe.
"""
import json, sys, time, urllib.request, urllib.error, pathlib, argparse

SWH = "https://archive.softwareheritage.org/api/1"
OWNER = "leesharks000"


def repos():
    """Every public repo the archive keeps, from the fleet checkout plus the core."""
    fleet = pathlib.Path("/home/claude/fleet")
    names = sorted(p.name for p in fleet.iterdir() if (p / ".git").exists()) if fleet.exists() else []
    return ["alexanarch"] + [n for n in names if n != "alexanarch"]


def get(url):
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception:
        return 0, None


def status(name):
    origin = f"https://github.com/{OWNER}/{name}"
    code, _ = get(f"{SWH}/origin/{urllib.parse.quote(origin, safe=':/')}/get/")
    if code != 200:
        return origin, "ABSENT", None
    code, v = get(f"{SWH}/origin/{urllib.parse.quote(origin, safe=':/')}/visits/")
    if code != 200 or not v:
        return origin, "KNOWN", None
    full = [x for x in v if x.get("status") == "full"]
    return origin, ("HELD" if full else "KNOWN"), (full[0]["date"][:10] if full else None)


def save(origin):
    req = urllib.request.Request(f"{SWH}/origin/save/git/url/{origin}/", method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read()).get("save_request_status", "?")
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}"
    except Exception as e:
        return str(e)[:40]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", action="store_true", help="request ingest for repos not yet held")
    a = ap.parse_args()
    rs = repos()
    print(f"{len(rs)} repositories\n")
    missing = []
    for n in rs:
        origin, st, when = status(n)
        print(f"  {st:6} {when or '—':12} {n}")
        if st != "HELD":
            missing.append(origin)
        time.sleep(0.4)
    print(f"\n  held by Software Heritage: {len(rs) - len(missing)}/{len(rs)}")
    if not missing:
        return 0
    if not a.save:
        print(f"  {len(missing)} not held — pass --save to request ingest")
        return 0
    print(f"\nrequesting ingest for {len(missing)}:")
    for o in missing:
        print(f"  {save(o):22} {o}")
        time.sleep(1.2)
    print("\nRequests are queued, not immediate. Re-run in a day to confirm and to")
    print("retry anything rate-limited — Save Code Now returns HTTP 429 after roughly")
    print("twenty requests in a window, and the script skips whatever is already HELD.")
    return 0


if __name__ == "__main__":
    import urllib.parse
    sys.exit(main())
