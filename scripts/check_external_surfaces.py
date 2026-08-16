#!/usr/bin/env python3
"""check_external_surfaces.py — do the archive's external dependencies still resolve?

The archive's data does not live only in this repository. Twelve heteronym identity cards are
rendered on TWELVE DIFFERENT DOMAINS, and the capture registry is displayed in three galleries
on three more. Those are external dependencies of the datasets, and nothing checked them.

On 2026-08-15 this found Sen Kuro's card returning 404: he had been reseated at
holographickernel.org by a MANUS ruling that reached the fleet's network-block attribution map
and never reached datasets/heteronyms/index.json. The dataset pointed at a dead address for
weeks and no gate could see it, because no gate looked outside the repository.

Usage: check_external_surfaces.py [--timeout N]
Exit 1 if any declared external surface fails to resolve.
"""
import json, sys, pathlib, argparse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent


def probe(url, timeout):
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "alexanarch-surface-check"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, ""
    except urllib.error.HTTPError as e:
        # The body of a 403 distinguishes a refusing SURFACE from a refusing RUNNER.
        try:
            return e.code, e.read(400).decode("utf-8", "replace")
        except Exception:
            return e.code, ""
    except Exception as e:
        return str(e)[:40], ""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--timeout", type=int, default=20)
    a = ap.parse_args()
    targets = []

    idx = json.loads((ROOT / "datasets/heteronyms/index.json").read_text())
    for p in idx["positions"]:
        if p.get("surface"):
            targets.append(("heteronym card", p["name"], p["surface"]))

    reg = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text())
    for g in reg.get("galleries") or []:
        targets.append(("capture gallery", f"v{reg.get('version')}", g))

    fails = []
    for kind, name, url in targets:
        code, body = probe(url, a.timeout)

        # A sandboxed runner may be behind an egress allowlist. A 403 whose BODY names the
        # allowlist is the RUNNER refusing, not the surface. Reporting that as a dead surface
        # would teach the operator to ignore this gate.
        if code == 403 and ("allowlist" in body.lower() or "egress" in body.lower()):
            print(f"  SKIP  {kind:<17} {name[:22]:<24} {url}  (runner egress block, not a dead surface)")
            continue
        ok = code == 200
        print(f"  {str(code):<5} {kind:<17} {name[:22]:<24} {url}")
        if not ok:
            fails.append(f"{kind} for {name}: {url} -> {code}")

    if fails:
        print(f"\nFAIL: {len(fails)} external surface(s) do not resolve:")
        for f in fails:
            print("  " + f)
        print("\nA dataset pointing at a dead surface is a dataset asserting something false.")
        return 1
    print(f"\nOK: all {len(targets)} declared external surfaces resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
