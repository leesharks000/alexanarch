#!/usr/bin/env python3
"""build_dc_series.py — the DC lane as a series: every weekly registry-wide DataCite sweep held in data/,
with the registry total, cern.zenodo's findable count, and per-epoch net declines among clients counted in both
adjacent epochs (a client's net decline is a lower bound on its departures: additions in the same week offset it).
Writes data/datacite-registrywide-series.json."""
import json, glob, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]
fs = sorted(glob.glob(str(ROOT / "data/datacite-registrywide-2026-*.json")))
rows, prev = [], None
for i, f in enumerate(fs, 1):
    d = json.load(open(f)); pc = d["per_client_findable"]
    failed = set(x if isinstance(x, str) else (x.get("client") if isinstance(x, dict) else x) for x in d.get("failed_counts") or [])
    row = {"epoch": f"DC-E{i}", "captured_at": d["captured_at"], "file": "/data/" + pathlib.Path(f).name,
           "status": d["epoch_status"], "registry_total_findable": d["registry_total_findable"],
           "clients_enumerated": d["clients_enumerated"], "cern_zenodo_findable": pc.get("cern.zenodo")}
    if prev:
        common = [c for c in pc if c in prev[0] and pc[c] is not None and prev[0][c] is not None and c not in failed and c not in prev[1]]
        dec = sorted(((c, prev[0][c] - pc[c]) for c in common if pc[c] < prev[0][c]), key=lambda t: -t[1])
        row.update({"clients_compared": len(common), "clients_with_net_decline": len(dec),
                    "summed_net_decline": sum(v for _, v in dec), "largest_declines": [{"client": c, "net_decline": v} for c, v in dec[:5]]})
    rows.append(row); prev = (pc, failed)
out = {"name": "DataCite registry-wide findability series (DC lane)", "instrument": "PID Erosion Observatory · EA-EROSION-01 (#1045)",
       "generated": datetime.date.today().isoformat(), "method": "weekly enumeration of DataCite clients and per-client meta.total; "
       "comparison restricted to clients counted in both adjacent epochs; partial epochs are marked and their failed clients excluded",
       "epochs": rows}
(ROOT / "data/datacite-registrywide-series.json").write_text(json.dumps(out, indent=1) + "\n")
print(len(rows), rows[-1])
