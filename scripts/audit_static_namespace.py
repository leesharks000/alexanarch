#!/usr/bin/env python3
"""audit_static_namespace.py — the archive publishes static files. This asserts
that it actually does, in production, and refuses to let it stop again.

═══════════════════════════════════════════════════════════════════════════════
THE INCIDENT THIS EXISTS TO PREVENT — forensic record, closed 2026-08-06
═══════════════════════════════════════════════════════════════════════════════

WHAT BROKE IT
  Commit fd8de940, 2026-07-31T03:20:21Z — "OAI-PMH 2.0 endpoint at /oai".
  It added ONE file: api/oai.js. Nothing else in that commit touched api/.

WHY THAT BROKE IT
  The root api/ directory is Vercel's FUNCTIONS namespace. With no executable in
  it, Vercel published its contents as ordinary static assets and everything
  worked — which is why static JSON had lived there happily since 2026-07-03.
  The moment a .js file appeared, Vercel began treating api/ as a functions
  source directory, and non-executable files in a functions directory are NOT
  deployed as static assets. They 404 with an HTML error page.
  The irony is exact: an endpoint added to make the archive MORE harvestable
  took the entire machine-readable layer dark.

WHAT WENT DARK, INSTANTLY AND SILENTLY — 1,012 files
    /api/index.json           the protocol catalog DEPOSIT-FLOW.md calls authoritative
    /api/deposit-protocol.json + /api/schemas/*   the deposit contract itself
    /api/doi-axn-map.json     the DOI resolver's map — /go/ resolves against this,
                              standing in for 1,817 severed Zenodo DOIs
    /api/axn-index.json       the machine index every AXN resolver page advertises
    /api/search-index.json    + 996 body shards — hence the reported search failure
  3,412 HTML surfaces advertise these URLs. All were pointing at 404s.

WHY IT SURVIVED SIX DAYS UNDETECTED
  Every check the archive owned looked at the wrong layer:
    · validate_deposit.py and bootstrap_familiarization.py read from DISK, where
      the bytes were perfectly correct, and verified their sha256 happily;
    · deposit_pipeline stage_verify probes record pages and PDFs only — never a
      machine endpoint;
    · no workflow ever fetched a single /api/*.json URL.
  THE BYTES WERE NEVER WRONG. ONLY THE PUBLICATION WAS. Local validity and
  published availability are different properties, and the archive had rich
  instrumentation for the first and none whatsoever for the second.
  Worse: two later commits wrote updates INTO doi-axn-map.json after it went
  dark — the archive kept carefully maintaining a file no reader could fetch.
  It was found only because search failed loudly enough to be reported: the page
  parsed "The page could not be found" as JSON and threw on the letter T.

THE RULE THIS ENFORCES
  1. api/ holds executables only. A static file there is invisible. That is not
     a style preference; it is a publication failure.
  2. Every advertised machine endpoint must return real JSON in production —
     not merely HTTP 200. A misconfigured rewrite serving 200-with-HTML is the
     exact shape of this incident and must fail exactly as hard as a 404.
  3. This is a GATE, not a report. CI fails on it; the deposit pipeline refuses
     to commit through it. A check whose output does not stop the release is a
     check that gets read after the outage instead of before it.

Usage:
    python3 scripts/audit_static_namespace.py            # local: namespace only
    python3 scripts/audit_static_namespace.py --live     # + fetch and parse production
"""
import sys, json, pathlib, argparse, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "https://www.alexanarch.org"
CONTRACT = ROOT / "data/api/endpoint-contract.json"
EXEC_SUFFIXES = {".js", ".ts", ".mjs", ".cjs"}


def namespace_check():
    """api/ must contain executables and nothing else."""
    api = ROOT / "api"
    if not api.is_dir():
        return [], ["api/ does not exist (no functions namespace to collide with)"]
    strays = [p.relative_to(ROOT) for p in api.rglob("*")
              if p.is_file() and p.suffix not in EXEC_SUFFIXES]
    if strays:
        return [f"{len(strays)} STATIC FILE(S) IN THE FUNCTIONS NAMESPACE — these will "
                f"404 in production, silently: " + ", ".join(str(s) for s in strays[:6]) +
                (f" … and {len(strays) - 6} more" if len(strays) > 6 else "")], []
    n = len([p for p in api.rglob("*") if p.suffix in EXEC_SUFFIXES])
    return [], [f"api/ holds executables only ({n} function file(s))"]


def live_check(endpoints):
    """Every advertised endpoint must return parseable JSON, not merely 200."""
    fails, oks = [], []
    for ep in endpoints:
        url = BASE + ep["path"]
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "alexanarch-endpoint-guardian"})
            with urllib.request.urlopen(req, timeout=30) as r:
                ct = (r.headers.get("Content-Type") or "").lower()
                raw = r.read()
            if "json" not in ct:
                fails.append(f"{ep['path']} — served as '{ct or 'no content-type'}', expected "
                             f"JSON. This is how an HTML error page hides behind a 200.")
                continue
            try:
                doc = json.loads(raw.decode("utf-8", "replace"))
            except Exception as e:
                fails.append(f"{ep['path']} — HTTP 200 but the body is not valid JSON: {e}")
                continue
            key = ep.get("must_contain_key")
            if key and key not in doc:
                fails.append(f"{ep['path']} — JSON parsed but required key '{key}' is absent; "
                             f"the wrong document is being served")
                continue
            oks.append(f"{ep['path']}  ({len(raw):,} bytes)  {ep.get('why','')}")
        except urllib.error.HTTPError as e:
            fails.append(f"{ep['path']} — HTTP {e.code} — {ep.get('why', 'advertised endpoint')}")
        except Exception as e:
            fails.append(f"{ep['path']} — {type(e).__name__}: {e}")
    return fails, oks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true",
                    help="also fetch every contracted endpoint from production")
    a = ap.parse_args()

    fails, oks = namespace_check()

    if a.live:
        if not CONTRACT.exists():
            fails.append(f"endpoint contract missing at data/api/endpoint-contract.json — "
                         f"cannot verify what the archive advertises")
        else:
            eps = json.loads(CONTRACT.read_text())["endpoints"]
            f2, o2 = live_check(eps)
            fails += f2
            oks += o2

    for o in oks:
        print(f"  ok    {o}")
    for f in fails:
        print(f"  FAIL  {f}", file=sys.stderr)

    # SUPERSESSION TERMINALITY (2026-08-08). A banner reading "Current version: #N"
    # must name a record that IS current. Seventeen records named their immediate
    # successor under that word while the successor was itself superseded: #1216
    # announced #832 as current on a page where #832 announced it was superseded by
    # #1217, and the DOI registry lineage ran six deep. The pointer was right and the
    # label was the defect, so wire_deposit now walks to the terminal for the label
    # and prints the immediate link beside it. This checks the RENDERING.
    import re as _re, json as _json
    _reg = _json.loads((ROOT / 'data/registry.json').read_text())
    _D = {x['deposit_number']: x for x in _reg['deposits']}
    def _sup(_r):
        _b = (_r or {}).get('body_status') or {}
        return _b.get('superseded_by') or (_r or {}).get('superseded_by_deposit_number')
    _bad = []
    for _p in sorted((ROOT / 's/records').glob('*/index.html')):
        _m = _re.search(r'Current version:.*?#(\d+)', _p.read_text(errors='replace'), _re.S)
        if _m and _sup(_D.get(int(_m.group(1)))):
            _bad.append(f"#{_p.parent.name}->#{_m.group(1)}")
    if _bad:
        fails.append(f"{len(_bad)} record(s) name a SUPERSEDED record as the current "
                     f"version: {', '.join(_bad[:6])}")

    # THREE DISTINCT DEFECTS, kept distinct (2026-08-08). A first version of this
    # check conflated them and reported 132 records as "asserting the work is not
    # held", which was true of none of them by then. A gate whose message does not
    # match its finding sends a reader looking for the wrong thing.
    import re as _re2, json as _j2
    _r2 = _j2.loads((ROOT / 'data/registry.json').read_text())

    def _scan(pat):
        out = []
        for _d in _r2['deposits']:
            if (_d.get('body_status') or {}).get('class') != 'full':
                continue
            for _f in ('description', 'wiki_article'):
                if _re2.search(pat, str(_d.get(_f) or ''), _re2.I):
                    out.append(f"#{_d['deposit_number']}/{_f}")
                    break
        return out

    # (1) HARD FAIL. A record holding its work while telling readers and crawlers the
    # work is absent. This renders into the meta description, so the contradiction
    # reaches every summarizer. Thirty-nine records carried it earlier today.
    _contra = _scan(r'this record is a metadata capture|the complete work is not seated here|'
                    r'\bis held as a \*{0,2}metadata capture')
    if _contra:
        fails.append(f"{len(_contra)} record(s) hold their work while asserting it is NOT held: "
                     f"{', '.join(_contra[:6])}")

    # (2) and (3) REPORTED, NOT BLOCKING. Placeholder text and capture provenance
    # prose standing where an account of the work belongs. Both are real and neither
    # is a publication failure, so they are counted here and repaired in their own
    # pass rather than stopping every deploy.
    _stub = _scan(r'structured data rather than prose|belongs to the description/wiki review stream')
    _prov = _scan(r'^\s*(DOI\(s\):|Source tier:)|Zenodo removal forensics')
    if _stub or _prov:
        print(f"  note  {len(_stub)} record(s) carry a placeholder description/wiki stub; "
              f"{len(_prov)} carry capture provenance prose where the work should be described "
              f"(reported, not blocking)")

    if fails:
        print("\n" + "=" * 74, file=sys.stderr)
        print("STATIC PUBLICATION IS BROKEN — the fd8de940 class of failure:", file=sys.stderr)
        print("the bytes can be perfect on disk and invisible to every reader.", file=sys.stderr)
        print("Do not commit or deploy through this. See this file's header.", file=sys.stderr)
        for _f in fails:
            print(f"  FAIL  {_f}", file=sys.stderr)
        print("=" * 74, file=sys.stderr)
        return 1
    print("\nSTATIC PUBLICATION VERIFIED" + (" (namespace + live)" if a.live else " (namespace)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
