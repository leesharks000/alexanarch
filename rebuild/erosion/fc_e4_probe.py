#!/usr/bin/env python3
"""fc_e4_probe.py — FC-E4: re-query the 871 founding-case DOIs at the DataCite public API (same keys as FC-E3).
Usage: fc_e4_probe.py <fc-e3 json> <out json>"""
import json, sys, datetime, urllib.request, urllib.error, concurrent.futures as cf, time
src = json.load(open(sys.argv[1])); keys = list(src["per_doi_http"])
def st(doi):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(f"https://api.datacite.org/dois/{doi}", headers={"User-Agent": "PID-Erosion-Observatory/1.3"}), timeout=60) as r:
                return doi, str(r.status)
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(5 * (i + 1)); continue
            return doi, str(e.code)
        except Exception:
            time.sleep(3 * (i + 1))
    return doi, "error"
t0 = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
with cf.ThreadPoolExecutor(6) as ex: res = dict(ex.map(st, keys))
prev = src["per_doi_http"]
restored = [k for k in keys if prev[k] == "404" and res[k] == "200"]
lost = [k for k in keys if prev[k] == "200" and res[k] == "404"]
from collections import Counter
out = {"epoch": "FC-E4", "name": "DataCite Severance Re-Capture — Fourth Epoch", "instrument": "PID Erosion Observatory · EA-EROSION-01 (#1045)",
       "captured_at": t0, "finished_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
       "baseline": "data/datacite-epoch3-2026-07-11.json (FC-E3, same 871 keys)",
       "finding": {"queried": len(keys), "status_counts": dict(Counter(res.values())),
                   "restored_to_findable_since_fc_e3": len(restored), "newly_absent_since_fc_e3": len(lost),
                   "restored": restored, "newly_absent": lost},
       "per_doi_http": res}
json.dump(out, open(sys.argv[2], "w"), indent=1); print(json.dumps(out["finding"])[:600])
