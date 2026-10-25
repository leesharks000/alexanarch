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
import argparse, datetime, hashlib, json, pathlib, subprocess, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
V2 = ROOT / "datasets/negative-of-the-negative/v2"
LANDINGS = V2 / "landings.json"
REFUSALS = V2 / "landing-refusals.json"


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "alexanarch-land-non-pending/1.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--service", default="https://gnosis.spxi.dev")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    listed = get_json(a.service.rstrip("/") + "/v1/landable").get("landable") or []
    landed_ids = {L.get("result_id") for L in (json.loads(LANDINGS.read_text(encoding="utf-8")).get("landings", []) if LANDINGS.exists() else [])}
    refusals = json.loads(REFUSALS.read_text(encoding="utf-8")) if REFUSALS.exists() else {
        "_what_this_is": ("Composed /non rows the archive's landing tool refused, with what it said. A refused result is not tried "
                          "again unless its listing changes. Written by scripts/land_non_pending.py."), "refused": {}}

    landed, held = [], []
    for item in listed:
        rid, row = item.get("result_id"), item.get("row")
        if not rid or not row or rid in landed_ids:
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
        p = subprocess.run([sys.executable, "scripts/land_non_row.py", "--result", rid, "--service", a.service, "--no-build"],
                           cwd=ROOT, capture_output=True, text=True)
        out = (p.stdout + p.stderr).strip()
        if p.returncode == 0 and out.startswith("nothing to land"):
            print(f"{row} ({rid}): already this row")
        elif p.returncode == 0:
            print(f"{row} ({rid}): landed")
            landed.append(row)
            landed_ids.add(rid)
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
        for s in ("scripts/build_non.py", "scripts/build_central_registry.py", "scripts/generate_axn_resolver.py", "scripts/sync_sigil.py"):
            subprocess.run([sys.executable, s], cwd=ROOT, check=True)
    print("landed: " + (", ".join(landed) if landed else "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
