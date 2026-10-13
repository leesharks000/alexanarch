#!/usr/bin/env python3
"""xr_e3_probe.py — XR-E3: re-probe the XR-E2 sample (same 54 DOIs, same two founding-case controls) on
OpenAIRE Graph API (graph v1), DataCite public API and OpenAlex, one pass, per-DOI HTTP state preserved.
Usage: xr_e3_probe.py <xr-e2 capture json> <out json>"""
import json, sys, time, urllib.request, urllib.error, datetime
src = json.load(open(sys.argv[1])); out = sys.argv[2]
def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "PID-Erosion-Observatory/1.3 (persistentidentifiers.org)"}), timeout=60) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return None, str(e).encode()
def probe(doi):
    row = {"doi": doi}
    st, body = get(f"https://api.openaire.eu/graph/v1/researchProducts?pid={doi}")
    row["openaire_http"] = st
    try: row["openaire_numFound"] = json.loads(body)["header"]["numFound"]
    except Exception: row["openaire_numFound"] = None
    row["openaire_hit"] = bool(row["openaire_numFound"])
    row["datacite_status"] = get(f"https://api.datacite.org/dois/{doi}")[0]
    row["openalex_status"] = get(f"https://api.openalex.org/works/doi:{doi}")[0]
    time.sleep(1.1)
    return row
t0 = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
ctrl = [dict(probe(c["doi"]), xr_e2_openaire_hit=c.get("openaire_hit")) for c in src["founding_case_controls"]]
per = []
for p in src["per_doi"]:
    r = probe(p["doi"]); r.update({k: p[k] for k in ("vintage", "stratum", "removal_date", "removal_reason")})
    r["xr_e2"] = {k: p.get(k) for k in ("openaire_hit", "datacite_status", "openalex_status")}
    per.append(r)
agg = {"n": len(per), "openaire_present": sum(r["openaire_hit"] for r in per),
       "openaire_errors": sum(r["openaire_http"] != 200 for r in per),
       "datacite_absent_404": sum(r["datacite_status"] == 404 for r in per),
       "openalex_present_200": sum(r["openalex_status"] == 200 for r in per),
       "changed_since_xr_e2": sum(1 for r in per if (r["openaire_hit"], r["datacite_status"], r["openalex_status"]) !=
                                  (r["xr_e2"]["openaire_hit"], r["xr_e2"]["datacite_status"], r["xr_e2"]["openalex_status"]))}
json.dump({"epoch": "XR-E3", "lane": "XR (cross-registry propagation — OpenAIRE re-probe of the XR-E2 sample)",
           "instrument": "PID Erosion Observatory · EA-EROSION-01 (deposit #1045)",
           "observed_at_utc": t0, "finished_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
           "method": {"sample": "the 54 DOIs and 2 founding-case controls of XR-E2 (data/xr-e2-openaire-capture-2026-07-12.json), unchanged",
                      "endpoints": {"openaire": "https://api.openaire.eu/graph/v1/researchProducts?pid=<doi>",
                                    "datacite": "https://api.datacite.org/dois/<doi>", "openalex": "https://api.openalex.org/works/doi:<doi>"},
                      "graph_release_at_capture": "v11.4.0 (released 2026-08-31; latest listed in the changelog at capture)"},
           "founding_case_controls": ctrl, "aggregates": agg, "per_doi": per}, open(out, "w"), indent=1)
print(json.dumps(agg), json.dumps(ctrl))
