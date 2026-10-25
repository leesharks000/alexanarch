#!/usr/bin/env python3
"""land_non_row.py — land a /non row composed by SPXI-gnΩsis into the archive (ruled 2026-10-24).

It is run for every composed row by scripts/land_non_pending.py, from .github/workflows/land-non-rows.yml, and can be run by hand.
It takes a landing tree — what the service writes under its execution key: datasets/negative-of-the-negative/v2/…
paths mirroring the archive's, landing/panel-entry.json, and landing/manifest.json naming every file with its sha256 —
from a local folder (--tree) or from the service (--result R-…, read from /v1/results/<id>/landing).

  1. Every file in the manifest is read and hashed; any mismatch, any path outside the row's own folders, or any file
     the manifest does not name refuses the whole landing. Nothing is copied until everything verifies.
  2. A row whose T the caller attested (provenance class "attested") is held, as the service itself holds it, until
     the registry's intake seats the composition as a capture: --seated <capture slug> records that it has.
  3. Where the entity already has a row, every file the tree would replace is first copied, as it stood, to
     datasets/negative-of-the-negative/v2/history/<row>/<date>-<sha12 of the replaced row>/, so the earlier
     composition stays inspectable; the entity page lists it.
  4. The files are copied; the panel entry is merged into panel.json (a new entity is appended; an existing one keeps
     its name and type, takes the new stage and source, and gains any address it did not have).
  5. The landing is recorded in datasets/negative-of-the-negative/v2/landings.json; scripts/non_axn.py mints the
     entry's AXN, or a new version of it, with the landing as its reason; /non and the AXN surfaces are rebuilt.

Usage:
    python3 scripts/land_non_row.py --tree <dir>            # a landing tree on disk (the folder holding landing/)
    python3 scripts/land_non_row.py --result R-0123456789abcdef [--service https://gnosis.spxi.dev]
    … --dry-run                                             # verify and report; write nothing
    … --seated <capture-slug>                               # for an attested T, the capture that seats it
    … --no-build                                            # land the files and ledgers; skip the rebuild
"""
import argparse, datetime, hashlib, json, pathlib, re, shutil, subprocess, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
V2REL = "datasets/negative-of-the-negative/v2"
V2 = ROOT / V2REL
LANDINGS = V2 / "landings.json"
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{0,80}$")


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def allowed(path, row):
    """The row's own folders, and nothing else."""
    if path.startswith("/") or ".." in path.split("/") or "\\" in path:
        return False
    return (path == f"{V2REL}/rows/{row}.json"
            or path.startswith(f"{V2REL}/ledgers/{row}/")
            or path.startswith(f"{V2REL}/traversal/{row}/")
            or re.match(rf"^{re.escape(V2REL)}/intake/{re.escape(row)}-[0-9]+/", path) is not None
            or path == "landing/panel-entry.json")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "alexanarch-land-non-row/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def read_tree(a):
    """Return (manifest, {path: bytes}, source description)."""
    if a.tree:
        base = pathlib.Path(a.tree)
        mp = base / "landing/manifest.json"
        if not mp.exists():
            sys.exit(f"refused: no landing/manifest.json under {base}")
        man = json.loads(mp.read_text(encoding="utf-8"))
        files = {}
        for f in man["files"]:
            p = base / f["path"]
            files[f["path"]] = p.read_bytes() if p.is_file() else None
        # a file in the tree the manifest does not name refuses the landing
        named = {f["path"] for f in man["files"]} | {"landing/manifest.json"}
        extra = sorted(str(p.relative_to(base)) for p in base.rglob("*") if p.is_file() and str(p.relative_to(base)) not in named)
        return man, files, f"tree {base}", extra
    svc = a.service.rstrip("/")
    man = json.loads(fetch(f"{svc}/v1/results/{a.result}/landing"))
    files = {}
    for f in man["files"]:
        try:
            files[f["path"]] = fetch(f"{svc}/v1/results/{a.result}/landing/{f['path']}")
        except Exception as e:
            files[f["path"]] = None
            print(f"  could not fetch {f['path']}: {e}", file=sys.stderr)
    return man, files, f"{svc}/v1/results/{a.result}/landing", []


def main():
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--tree")
    src.add_argument("--result")
    ap.add_argument("--service", default="https://gnosis.spxi.dev")
    ap.add_argument("--seated", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-build", action="store_true")
    ap.add_argument("--date", default=datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d"))
    a = ap.parse_args()

    man, files, source, extra = read_tree(a)
    row = man.get("row") or ""
    problems = []
    if not SLUG.match(row):
        problems.append(f"row key {row!r} is not a slug")
    for f in man["files"]:
        p = f["path"]
        if not allowed(p, row):
            problems.append(f"path outside the row's folders: {p}")
        elif files.get(p) is None:
            problems.append(f"missing: {p}")
        elif sha_bytes(files[p]) != f["sha256"]:
            problems.append(f"sha256 mismatch: {p} (manifest {f['sha256'][:12]}…, file {sha_bytes(files[p])[:12]}…)")
    for p in extra:
        problems.append(f"in the tree, not in the manifest: {p}")
    rowp = f"{V2REL}/rows/{row}.json"
    if rowp not in files:
        problems.append(f"the manifest names no row ({rowp})")
    if "landing/panel-entry.json" not in files:
        problems.append("the manifest names no panel entry (landing/panel-entry.json)")
    if problems:
        print(f"refused: {len(problems)} problem(s) in {source}", file=sys.stderr)
        for x in problems:
            print("  " + x, file=sys.stderr)
        return 1

    R = json.loads(files[rowp])
    prov = ((R.get("objects") or {}).get("T") or {}).get("provenance") or {}
    if prov.get("class") == "attested" and not a.seated:
        print("held: T is a composition the caller attests and the service did not observe; the row lands once the registry's "
              "intake seats it as a capture (--seated <capture slug>)", file=sys.stderr)
        return 1
    cg = R.get("composition_gnosis") or {}
    panel_entry = json.loads(files["landing/panel-entry.json"])

    # what an existing row loses, kept before anything is written
    cur = V2 / "rows" / f"{row}.json"
    replaced = None
    if cur.exists():
        old = cur.read_bytes()
        if sha_bytes(old) == man_sha(man, rowp):
            print(f"nothing to land: the archive's {rowp} is already this row (sha256 {sha_bytes(old)[:12]}…)")
            return 0
        hdir = f"{V2REL}/history/{row}/{a.date}-{sha_bytes(old)[:12]}"
        kept = [f["path"] for f in man["files"] if f["path"] != "landing/panel-entry.json" and (ROOT / f["path"]).exists()]
        replaced = {"row_sha256": sha_bytes(old), "epoch": json.loads(old).get("epoch"), "kept_at": hdir, "files": kept}

    print(f"landing {row} from {source}")
    print(f"  {len(man['files'])} files verified against the manifest; execution key {str(man.get('key'))[:16]}…")
    print(f"  composed by {(cg.get('service') or {}).get('name', '?')} {(cg.get('service') or {}).get('version', '')}, "
          f"protocol {cg.get('protocol', '?')}; T provenance: {prov.get('class', '?')}")
    composed = bool((R.get("objects") or {}).get("KO"))
    if not composed:
        print(f"  note: this row carries no composition ({(R.get('objects') or {}).get('note', 'no knowledge object')}); "
              f"its breaches: {', '.join(b.get('check', '?') for b in R.get('breaches') or []) or 'none recorded'}")
    if replaced:
        print(f"  replaces the row of epoch {replaced['epoch']} (sha256 {replaced['row_sha256'][:12]}…); "
              f"{len(replaced['files'])} files kept at {replaced['kept_at']}/")
        if not composed and (json.loads(cur.read_bytes()).get("objects") or {}).get("KO"):
            print("  note: the row it replaces carries a composition and this one does not; the earlier row stays on the page, "
                  "under its history", file=sys.stderr)
    if a.dry_run:
        print("dry run: nothing written")
        return 0

    if replaced:
        for p in replaced["files"]:
            dst = ROOT / replaced["kept_at"] / p[len(V2REL) + 1:]
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / p, dst)
    for f in man["files"]:
        if f["path"] == "landing/panel-entry.json":
            continue
        dst = ROOT / f["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(files[f["path"]])

    pp = V2 / "panel/panel.json"
    praw = pp.read_text(encoding="utf-8")
    panel = json.loads(praw)
    ex = next((x for x in panel["entities"] if x["entity"] == panel_entry["entity"]), None)
    if ex is None:
        panel["entities"].append(panel_entry)
        pnote = "appended"
    else:
        ex["stage"] = panel_entry.get("stage", ex.get("stage"))
        ex["source"] = panel_entry.get("source", ex.get("source"))
        have = {d["address"].lower() for d in ex.get("addresses", [])}
        for d in panel_entry.get("addresses", []):
            if d["address"].lower() not in have:
                ex.setdefault("addresses", []).append(d)
        pnote = "merged (name and type kept)"
    pp.write_text(json.dumps(panel, ensure_ascii=False, indent=1 if praw.startswith("{\n \"") else 2) + "\n", encoding="utf-8")

    L = json.loads(LANDINGS.read_text(encoding="utf-8")) if LANDINGS.exists() else {
        "_what_this_is": ("Every /non row landed from SPXI-gnΩsis, in order: what landed, from where, verified against which manifest, "
                          "and what it replaced. Written by scripts/land_non_row.py."),
        "landings": []}
    man_bytes = json.dumps(man, ensure_ascii=False, sort_keys=True).encode()
    L["landings"].append({
        "row": row, "entity": panel_entry["entity"], "landed": a.date, "source": source,
        "result_id": a.result or None, "execution_key": man.get("key"), "manifest_sha256": sha_bytes(man_bytes),
        "service": cg.get("service"), "protocol": cg.get("protocol"), "models": cg.get("models"),
        "archive_release": cg.get("archive_release"), "cost_usd": cg.get("cost_usd"),
        "t_provenance": prov or None, "seated_as": a.seated,
        "files": [{"path": f["path"], "sha256": f["sha256"]} for f in man["files"] if f["path"] != "landing/panel-entry.json"],
        "panel": pnote, "replaced": replaced})
    LANDINGS.write_text(json.dumps(L, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    reason = f"landed the SPXI-gnΩsis composition {str(man.get('key'))[:16]}" + (f" (result {a.result})" if a.result else "")
    run = lambda *c: subprocess.run([sys.executable, *c], cwd=ROOT, check=True)
    run("scripts/non_axn.py", "--date", a.date, "--reason", reason)
    if not a.no_build:
        run("scripts/build_non.py")
        run("scripts/build_central_registry.py")
        run("scripts/generate_axn_resolver.py")
        run("scripts/sync_sigil.py")
    print(f"landed {row}; panel {pnote}; recorded in {LANDINGS.relative_to(ROOT)}")
    return 0


def man_sha(man, path):
    return next((f["sha256"] for f in man["files"] if f["path"] == path), None)


if __name__ == "__main__":
    sys.exit(main())
