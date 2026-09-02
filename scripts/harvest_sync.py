#!/usr/bin/env python3
"""harvest_sync.py — one trigger for every surface that tells a harvester how big the archive is.

THE DEFECT (audit 2026-09-02)
-----------------------------
On one day the archive stated its own size four ways:

  data/registry.json / .well-known/axn-node.json    1573
  llms.txt                                          1557
  resourcesync/resourcelist.xml (served)            1546
  OAI-PMH completeListSize (served)                 1507

The node declaration is computed on every commit and gated on every push
(generate_node_declaration.py --check). The other three were regenerated only
when someone remembered: build_oai_index.py and build_resourcesync.py are
called by propagate_record_state.py but not by the mint workflow;
coherence_sync.py (which rewrites the llms.txt count) is called by
deposit_pipeline stage_commit but by nothing else. A harvester that trusted
OAI got 66 fewer records than the registry held.

THE RULE
--------
Whatever regenerates the node declaration regenerates the harvest surfaces
first, and the PR gate refuses drift between them. There is one entry point:

    python3 scripts/harvest_sync.py          # rebuild OAI index, ResourceSync, llms.txt count, node declaration
    python3 scripts/harvest_sync.py --check  # gate: fail if any of those would change on rebuild

--check rebuilds into a scratch copy and compares content with run timestamps
masked, so a rebuild that changes only the "generated at" stamp passes and a
rebuild that changes a record count or a record set fails and names the file.
"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Files whose content must agree with the registry. Order matters only for the
# report; the builders decide the content.
SURFACES = [
    "data/oai-index.json",
    "resourcesync/resourcelist.xml",
    "resourcesync/changelist.xml",
    "resourcesync/capabilitylist.xml",
    "llms.txt",
]

BUILDERS = [
    ["scripts/build_oai_index.py"],
    ["scripts/build_resourcesync.py"],
    ["scripts/coherence_sync.py"],   # llms.txt + api index; ends by regenerating the node declaration
]

# Run-time stamps that legitimately differ between two builds of identical state.
_MASKS = [
    re.compile(r'\b(at|completed|datetime|hashed_at|last_updated|generated_at|built_at)="[^"]*"'),
    re.compile(r'"(hashed_at|last_updated|generated_at|built_at|declared_at)":\s*"[^"]*"'),
]


def _masked(text: str) -> str:
    for m in _MASKS:
        text = m.sub(lambda mo: mo.group(0).split("=")[0].split(":")[0] + "=<ts>", text)
    return text


def _run_builders(cwd: pathlib.Path) -> None:
    for b in BUILDERS:
        r = subprocess.run([sys.executable, *b], cwd=cwd, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-2000:], r.stderr[-2000:], sep="\n")
            raise SystemExit(f"harvest_sync: {b[0]} failed (exit {r.returncode})")
        last = (r.stdout.strip().splitlines() or [""])[-1]
        print(f"  {b[0]}: {last}")


def _count(path: pathlib.Path) -> str:
    t = path.read_text(errors="replace")
    if path.name == "oai-index.json":
        import json
        return f"{len(json.loads(t).get('records', []))} records"
    if path.suffix == ".xml":
        return f"{t.count('<url>')} urls"
    m = re.search(r"archive of (\d[\d,]*) deposits", t)
    return f"{m.group(1)} deposits" if m else "?"


def sync() -> int:
    print("harvest_sync: rebuilding harvest surfaces")
    _run_builders(ROOT)
    for s in SURFACES:
        print(f"  {s}: {_count(ROOT / s)}")
    return 0


def check() -> int:
    """Rebuild in a scratch copy of the working tree and diff against the committed surfaces."""
    with tempfile.TemporaryDirectory(prefix="harvest-check-") as tmp:
        scratch = pathlib.Path(tmp) / "repo"
        # The builders read the registry, texts, and scripts; copy the tree minus
        # the heavy rendered pages. shutil.copytree follows the ignore list.
        shutil.copytree(
            ROOT, scratch,
            ignore=shutil.ignore_patterns(".git", "s", "records", "wiki", "node_modules",
                                          "build", "artifacts", "captures", "triage"),
        )
        _run_builders(scratch)
        drift = []
        for s in SURFACES:
            a = _masked((ROOT / s).read_text(errors="replace"))
            b = _masked((scratch / s).read_text(errors="replace"))
            if a != b:
                drift.append(f"  DRIFT {s}: committed {_count(ROOT / s)} → rebuilt {_count(scratch / s)}")
        if drift:
            print("harvest_sync --check: FAIL — committed harvest surfaces disagree with the registry")
            print("\n".join(drift))
            print("  fix: python3 scripts/harvest_sync.py, then commit the regenerated files")
            return 1
    print("harvest_sync --check: PASS — OAI index, ResourceSync, and llms.txt agree with the registry")
    return 0


if __name__ == "__main__":
    sys.exit(check() if "--check" in sys.argv else sync())
