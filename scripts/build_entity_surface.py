#!/usr/bin/env python3
"""build_entity_surface.py — Alexanarch's machine self-description, live, at /data/api/entity.json.

WHAT THIS IS. EA-MPAI-ALEXANARCH-01 v0.4 (#1678) describes the library function by function:
seventeen functions on one deposit registry and identifier spine, their joins as an eighteenth,
each with its own field, comparators, criteria, checks and evidence boundary, and the program the
library carries. Its machine file is attached to the deposit (files/AXN-06F4/alexanarch-entity.json)
and is frozen there: the witness of the registry at deposit.

The self-description a reader fetches today needs today's counts. This script runs the deposit's
own attached builder, unchanged, against the deposited text and the current repository, and writes
the result here with a pointer back to the frozen witness. Nothing in the description is written
by this script: the functions, rules, modes and mantle come from the deposited text and its attached
mantle layer; every count is computed from the registry and the surfaces it names.

WHY THE ATTACHED BUILDER AND NOT A COPY. A copy drifts from the deposit. Running the attached
file keeps one source of the description, and its sha256 is checked against the registry's
files[] before it runs.

    python3 scripts/build_entity_surface.py          # write data/api/entity.json
    python3 scripts/build_entity_surface.py --check  # report whether the committed file is current
"""
import hashlib, json, pathlib, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEPOSIT = 1678
OUT = ROOT / "data/api/entity.json"
A = "https://www.alexanarch.org"


def main():
    reg = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))
    d = next(x for x in reg["deposits"] if x["deposit_number"] == DEPOSIT)
    files = {f["filename"]: f for f in d.get("files") or []}
    for fn in ("build_entity_json.py", "mantle_layer.py", "alexanarch-entity.json"):
        f = files[fn]
        got = hashlib.sha256((ROOT / f["path"].lstrip("/")).read_bytes()).hexdigest()
        if got != f["sha256"]:
            print(f"entity surface: {fn} does not match #{DEPOSIT} files[] ({got[:12]} ≠ {f['sha256'][:12]}); not built")
            return 1
    builder = ROOT / files["build_entity_json.py"]["path"].lstrip("/")
    text = ROOT / d["full_text_path"].lstrip("/")
    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td) / "entity.json"
        r = subprocess.run([sys.executable, str(builder), str(text), str(tmp)], cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            print("entity surface: builder failed\n" + r.stderr[-2000:])
            return 1
        j = json.loads(tmp.read_text(encoding="utf-8"))
    j["surface"] = {
        "kind": "live self-description",
        "url": f"{A}/api/entity.json",
        "regenerated_by": "scripts/build_entity_surface.py (via scripts/regenerate_surfaces.py, surface 'entity')",
        "described_by": {"deposit": DEPOSIT, "axn": d["axn"], "record": f"{A}/s/records/{DEPOSIT}/",
                         "text": f"{A}{d['full_text_path']}"},
        "frozen_witness": {"url": f"{A}{files['alexanarch-entity.json']['path']}", "sha256": files["alexanarch-entity.json"]["sha256"],
                           "note": "the same file as built at deposit; it keeps the registry state of that day"},
        "builder": {"url": f"{A}{files['build_entity_json.py']['path']}", "sha256": files["build_entity_json.py"]["sha256"]},
        "note": "The description is the deposit's; the counts are today's. Fetch a count's named source rather than repeating it.",
    }
    s = json.dumps(j, ensure_ascii=False, indent=1) + "\n"
    if "--check" in sys.argv:
        cur = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        strip = lambda t: {k: v for k, v in (json.loads(t) if t else {}).items() if k != "as_of"}
        print("  ok    entity surface current" if strip(cur) == strip(s) else "  STALE entity surface — run without --check")
        return 0
    OUT.write_text(s, encoding="utf-8")
    print(f"entity surface: {len(j['functions'])} functions · {len(j.get('discrepancies', []))} discrepancies · "
          f"head {j['as_of']['registry_head'][:12]} → data/api/entity.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
