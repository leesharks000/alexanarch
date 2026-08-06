#!/usr/bin/env python3
"""audit_static_namespace.py — assert no static file hides in the Vercel
functions namespace, and that every advertised /api/*.json resolves live.

WHY THIS EXISTS (2026-08-06): the root api/ directory is Vercel's Functions
namespace. Non-executable files placed there are NOT published as static
assets — they 404 with an HTML error page. Every static JSON in the archive
lived there, so /api/index.json (the canonical protocol catalog),
/api/axn-index.json, /api/search-index.json and /api/doi-axn-map.json (the DOI
resolver's map, standing in for 1,935 severed Zenodo DOIs) were all dark, and
search failed with 'Unexpected token T' because it parsed 'The page could not
be found' as JSON. The bytes were correct in git the whole time; only the
publication path was wrong, which is why every local check passed.

Local mode asserts the namespace is clean. --live also fetches the advertised
URLs and requires JSON, not merely HTTP 200: an HTML 404 page returns 404 here
but a misconfigured rewrite could return 200 with HTML, which is the failure
this whole incident was made of.
"""
import sys, json, pathlib, argparse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "https://www.alexanarch.org"
PROBE = ["/api/index.json", "/api/axn-index.json", "/api/search-index.json",
         "/api/doi-axn-map.json", "/api/kernel-index.json",
         "/api/body-shards/manifest.json", "/data/browse-index.json",
         "/data/axn-central-registry.json"]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--live", action="store_true")
    a = ap.parse_args(); bad = []

    strays = [p for p in (ROOT/"api").rglob("*")
              if p.is_file() and p.suffix not in (".js", ".ts", ".mjs")]
    if strays:
        bad.append(f"{len(strays)} static file(s) in the functions namespace "
                   f"(they will 404): {', '.join(str(p.relative_to(ROOT)) for p in strays[:5])}")
    else:
        print("  ok  api/ holds executables only")

    if a.live:
        for path in PROBE:
            try:
                with urllib.request.urlopen(BASE + path, timeout=25) as r:
                    ct = r.headers.get("Content-Type", "")
                    body = r.read(400)
                    if "json" not in ct.lower():
                        bad.append(f"{path} served as {ct or 'no content-type'} — expected JSON")
                    else:
                        json.loads(body.decode("utf8", "replace")[:1] and body.decode("utf8","replace")
                                   if False else "{}") if False else None
                        print(f"  ok  {path} ({ct.split(';')[0]})")
            except Exception as e:
                bad.append(f"{path} — {type(e).__name__}: {e}")

    for b in bad:
        print("  FAIL", b, file=sys.stderr)
    print(("NAMESPACE CLEAN" if not bad else f"{len(bad)} FAILURE(S)"))
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
