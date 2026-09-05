#!/usr/bin/env python3
"""check_capture_registry.py — the registry gate (2026-09-05). Three checks, any failure stops the build.

  SCHEMA   every entry validates against rebuild/capture-registry/EA-WG-CAPTURES-01.schema.json
           (additionalProperties false — a new field is a schema change first).
  NO-LOSS  against the last committed registry (git HEAD or --base <rev>): no entry loses or shortens its
           transcript, loses an image path, or loses an image URL. This is the defect the registry was rebuilt
           from the ground up to end — transcripts and images were being discarded on repair.
  ORDER    entries are grouped by section `s` with sections alphabetical (file order is meaningful).

Usage: python3 scripts/check_capture_registry.py [--base origin/main]
"""
import json, sys, subprocess, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"; SCHEMA = ROOT / "rebuild/capture-registry/EA-WG-CAPTURES-01.schema.json"
def main():
    base = sys.argv[sys.argv.index("--base")+1] if "--base" in sys.argv else "HEAD"
    import jsonschema
    P = json.load(open(REG)); E = P["entries"]; S = json.load(open(SCHEMA)); v = jsonschema.Draft7Validator(S)
    fails = []
    for e in E:
        for err in v.iter_errors(e): fails.append(f"SCHEMA {e.get('slug')}: {'/'.join(map(str, err.absolute_path)) or '(entry)'}: {err.message[:90]}")
    try:
        prev = json.loads(subprocess.run(["git", "show", f"{base}:data/EA-WG-CAPTURES-01.json"], cwd=ROOT, capture_output=True, text=True, check=True).stdout)
        pb = {x["slug"]: x for x in prev["entries"]}
        for e in E:
            p = pb.get(e["slug"])
            if not p: continue
            pt, ct = (p.get("transcript") or ""), (e.get("transcript") or "")
            if len(ct) < len(pt): fails.append(f"NO-LOSS {e['slug']}: transcript shortened {len(pt)} → {len(ct)}")
            for k in ("imgs", "img_urls"):
                lost = set(p.get(k) or []) - set(e.get(k) or [])
                if lost: fails.append(f"NO-LOSS {e['slug']}: {k} lost {sorted(lost)[:2]}")
        missing = set(pb) - {e["slug"] for e in E}
        if missing: fails.append(f"NO-LOSS entries removed: {sorted(missing)[:5]}")
    except subprocess.CalledProcessError:
        print(f"no-loss: no base at {base}; skipped")
    secs = [s for s, _ in __import__("itertools").groupby(e["s"] for e in E)]
    if secs != sorted(secs) or len(secs) != len(set(secs)): fails.append(f"ORDER sections not grouped/alphabetical: {secs[:6]}…")
    for f in fails[:40]: print("✗", f)
    print(f"check_capture_registry: {len(E)} entries · {len(fails)} failure(s) · schema {SCHEMA.name} · base {base}")
    return 1 if fails else 0
if __name__ == "__main__": sys.exit(main())
