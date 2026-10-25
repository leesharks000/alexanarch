#!/usr/bin/env python3
"""land_non_pending.py — land in /non every row SPXI-gnΩsis has composed and the archive has not landed (2026-10-25).

/non is populated by itself, the way the Mandala Oracle's Book records its conversations: no one taps per row ("a
microservice that would require thousands … of uses to be profitable, and me hand clicking every one. it does not
compute"). Run by .github/workflows/land-non-rows.yml on a schedule and on dispatch; it can be run by hand the same way.

  1. GET <service>/v1/landable lists the composed rows: result id, row, execution key, the row file's sha256.
  2. A result already in datasets/negative-of-the-negative/v2/landings.json is skipped, and so is a row whose file in the
     archive already hashes to the listed row.
  3. Each remaining result is landed by scripts/land_non_row.py --result <id> --no-build, oldest first. That tool
     verifies every file against the manifest and refuses the whole landing on any mismatch; keeps a replaced row under
     history/; merges the panel entry; records the landing; mints the AXN.
  4. A refusal is recorded in datasets/negative-of-the-negative/v2/landing-refusals.json with what the tool said, and that
     result is not tried again unless its listing changes. A row whose T the caller attests is held by the tool until its
     capture is seated; it is left to be tried again, and not recorded. Anything else (the service unreachable) is left
     for the next run.
  5. If anything landed, /non and the AXN surfaces are rebuilt once. Committing is the workflow's step.

Prints one line per result; the last line is `landed: <rows>` (or `landed: none`), which the workflow reads.

Usage: python3 scripts/land_non_pending.py [--service https://gnosis.spxi.dev] [--dry-run]
"""
import argparse, datetime, hashlib, json, pathlib, shutil, subprocess, sys, tempfile, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
V2 = ROOT / "datasets/negative-of-the-negative/v2"
LANDINGS = V2 / "landings.json"
REFUSALS = V2 / "landing-refusals.json"


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "alexanarch-land-non-pending/1.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


# What landing one row can change: the files every landing touches, and the row's own folders. Kept before each row so a
# row taken back out leaves the checkout as it was.
SHARED = [V2 / "panel" / "panel.json", LANDINGS, V2 / "axn.json", ROOT / "data" / "symbolon-registry" / "allocation.json"]
def row_paths(row):
    return [V2 / "rows" / f"{row}.json", V2 / "ledgers" / row, V2 / "traversal" / row, V2 / "history" / row] + sorted((V2 / "intake").glob(f"{row}-*"))

def snapshot(row):
    keep = tempfile.mkdtemp(prefix="land-")
    snap = {"dir": keep, "row": row, "paths": {}}
    for i, p in enumerate(SHARED + row_paths(row)):
        dst = pathlib.Path(keep) / str(i)
        if p.is_dir(): shutil.copytree(p, dst); snap["paths"][str(p)] = ("dir", str(dst))
        elif p.exists(): shutil.copy2(p, dst); snap["paths"][str(p)] = ("file", str(dst))
        else: snap["paths"][str(p)] = ("absent", None)
    return snap

def restore(snap):
    for p in [pathlib.Path(x) for x in snap["paths"]] + [x for x in row_paths(snap["row"]) if str(x) not in snap["paths"]]:
        kind, src = snap["paths"].get(str(p), ("absent", None))
        if p.is_dir(): shutil.rmtree(p)
        elif p.exists(): p.unlink()
        if kind == "dir": shutil.copytree(src, p)
        elif kind == "file": shutil.copy2(src, p)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--service", default="https://gnosis.spxi.dev")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    listed = get_json(a.service.rstrip("/") + "/v1/landable").get("landable") or []
    LL = json.loads(LANDINGS.read_text(encoding="utf-8")).get("landings", []) if LANDINGS.exists() else []
    landed_ids = {L.get("result_id") for L in LL}
    # A row already landed is replaced only by a composition made on or after its latest landing: an earlier composition
    # listed beside it (2026-10-25: R-2c2717089a3c0c81, composed in the equal case under ρ = constructs, listed beside the
    # landed R-d744378a9776dfdb) is superseded and is not landed over it. A listing with no composition date predates the
    # list and is superseded wherever the row has a landing.
    last_landed = {}
    for L in LL:
        last_landed[L.get("row")] = max(last_landed.get(L.get("row"), ""), str(L.get("landed_at") or L.get("landed") or ""))
    refusals = json.loads(REFUSALS.read_text(encoding="utf-8")) if REFUSALS.exists() else {
        "_what_this_is": ("Composed /non rows the archive's landing tool refused, with what it said. A refused result is not tried "
                          "again unless its listing changes. Written by scripts/land_non_pending.py."), "refused": {}}

    landed, held = [], []
    for item in listed:
        rid, row = item.get("result_id"), item.get("row")
        if not rid or not row or rid in landed_ids:
            continue
        if row in last_landed and str(item.get("composed_at") or "")[:10] < last_landed[row][:10]:
            print(f"{row} ({rid}): superseded by the row's landing of {last_landed[row][:10]}")
            continue
        cur = V2 / "rows" / f"{row}.json"
        if item.get("row_sha256") and cur.exists() and hashlib.sha256(cur.read_bytes()).hexdigest() == item["row_sha256"]:
            continue
        prior = refusals["refused"].get(rid)
        if prior and prior.get("execution_key") == item.get("execution_key") and prior.get("row_sha256") == item.get("row_sha256"):
            continue
        if a.dry_run:
            print(f"would land {row} from {rid}")
            continue
        snap = snapshot(row)
        p = subprocess.run([sys.executable, "scripts/land_non_row.py", "--result", rid, "--service", a.service, "--no-build"],
                           cwd=ROOT, capture_output=True, text=True)
        out = (p.stdout + p.stderr).strip()
        if p.returncode == 0 and out.startswith("nothing to land"):
            print(f"{row} ({rid}): already this row")
        elif p.returncode == 0:
            # The row must build: a row the /non builder cannot render is taken back out and recorded as refused, so it
            # cannot stop every other row from landing (2026-10-25: the first operator row, its ontology unread, broke
            # the builder; one build ran after all the rows, so it would have stopped them all).
            b = subprocess.run([sys.executable, "scripts/build_non.py"], cwd=ROOT, capture_output=True, text=True)
            if b.returncode == 0:
                print(f"{row} ({rid}): landed")
                landed.append(row)
                landed_ids.add(rid)
            else:
                restore(snap)
                said = (b.stdout + b.stderr).strip()[-2000:]
                print(f"{row} ({rid}): refused, the /non build failed on it\n  " + said.replace("\n", "\n  "))
                refusals["refused"][rid] = {"row": row, "execution_key": item.get("execution_key"), "row_sha256": item.get("row_sha256"),
                                            "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                                            "said": "the /non build failed on this row; it was taken back out: " + said}
                REFUSALS.write_text(json.dumps(refusals, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        elif "held:" in out:
            print(f"{row} ({rid}): held until its capture is seated")
            held.append(row)
        elif "refused:" in out:
            print(f"{row} ({rid}): refused\n  " + out.replace("\n", "\n  "))
            refusals["refused"][rid] = {"row": row, "execution_key": item.get("execution_key"), "row_sha256": item.get("row_sha256"),
                                        "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                                        "said": out[-2000:]}
            REFUSALS.write_text(json.dumps(refusals, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        else:
            print(f"{row} ({rid}): not landed this run, tried again next run\n  " + out[-1500:].replace("\n", "\n  "))

    if landed:
        for s in ("scripts/build_central_registry.py", "scripts/generate_axn_resolver.py", "scripts/sync_sigil.py"):
            subprocess.run([sys.executable, s], cwd=ROOT, check=True)
    print("landed: " + (", ".join(landed) if landed else "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
