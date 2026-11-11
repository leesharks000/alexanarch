# v1.2, executed inside each builder before the kernel files are written: the records search carried into 00-kernel.yaml, each record resolved against
# the registry at build time; the Philo piece's claims for this kernel (v12_claims, added in v12_pre's wake) listed.
def _res(n, note):
    r = K.REG[n]
    o = {"record": f"rec:{n}", "deposit": n, "axn": r["axn"], "title": r["title"], "status": r.get("status"), "sha256": r["hash"], "note": note}
    if r.get("superseded_by_deposit_number") or r.get("superseded_by"):
        o["superseded_by"] = r.get("superseded_by_deposit_number") or r.get("superseded_by")
    return o
_E = []
for _e in V12_STAGE["evidence"]:
    _n = _e.get("deposit") or V12_PHILO
    _E.append(_res(_n, _e["note"] if _e.get("deposit") else "In the Midst of the Seven: Philo, the Logos Named and Lived, and the Seven Stations of Revelation (EA-MIDST-01 v1.0), the Philo piece of the search, deposited 2026-11-10. " + _e["note"]))
kernel["version"] = "1.2"; kernel["built"] = "2026-11-10"
kernel["records_search_v12"] = {
 "date": "2026-11-10", "rule": V12_STAGE["rule"], "rulings": V12_STAGE["rulings"] + [{"at": "2026-11-10 20:48", "text": "lets address, deposit, and turn to incorporating it into rev first and versioning all four holographic frames"}],
 "evidence": {"stratum": "stratum:S0-records-search-v12", "records": _E,
              "argument_layer": "these records enter the kernel without moves at this version; their moves are owed to a reading of each record in full (04-arguments.jsonl lists them under records_without_moves)"},
 "related_work": [_res(x["deposit"], x.get("note") or "") for x in V12_STAGE["related_work"]],
 "related_work_rule": "pointed to; their substance is not extended into the frame on this pass (18:20, 18:45)",
 "history": [_res(x["deposit"], x.get("note") or "earlier version or duplicate witness, resolved to its record of standing") for x in V12_STAGE["history"]],
 "joins": [_res(x["deposit"], x.get("note") or "") for x in V12_STAGE["joins"]],
 "flags": V12_STAGE["flags"]}
if "V12_CLAIMS" in dir() and V12_CLAIMS:
    kernel["records_search_v12"]["claims_from_1758"] = [f"claim:{c}" for c in V12_CLAIMS]
if K.ID == "EA-HK-HISTLOGOS-01":
    kernel["status"] = "DEPOSITED 2026-11-09 (#1757, AXN position 0C62); v1.1 reissued in place the same day; v1.2 reissued in place 2026-11-10"
