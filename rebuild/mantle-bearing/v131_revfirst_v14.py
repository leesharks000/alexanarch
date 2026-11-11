#!/usr/bin/env python3
"""mantle-bearing 1.31: #1755 EA-HK-REVFIRST-01 reissued in place as v1.4 (2026-11-11, the author: "and this is a new folding in, separate from the sappho chain, for revfirst"; "ready"), the fold-in of In the Midst of the Seven v1.1 (#1758) and Revelation First v9 (#1735); the Revelation First hologram row's status, record, tests and argument layer re-read from the v1.4 files. #1754, #1756 and #1757 unchanged. Adapted from the 1.29 script (v129_holograms_v13.py).
    python3 rebuild/mantle-bearing/v131_revfirst_v14.py"""
import json, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
A = "https://www.alexanarch.org"
rec = lambda n: {"deposit": n, "axn": REG[n]["axn"], "url": f"{A}/s/records/{n}/", "title": REG[n]["title"]}
d = json.loads(SRC.read_text(encoding="utf-8"))
if any(h["version"] == "1.31" for h in d["history"]): raise SystemExit("1.31 already applied")
assert d["history"][-1]["version"] == "1.30", d["history"][-1]["version"]
done = []
for n, kid in [(1755, "EA-HK-REVFIRST-01")]:
    assert REG[n]["version"] == "v1.4", (n, REG[n]["version"])
    K = ROOT / f"files/AXN-{REG[n]['hex']}/kernel"
    kern = yaml.safe_load((K / "00-kernel.yaml").read_text(encoding="utf-8")); ver = json.loads((K / "10-verification.json").read_text(encoding="utf-8"))
    h = next((x for x in d["holograms"] if any(r.get("deposit") == n for r in (x.get("hologram_record") or []))), None)
    if h is None: raise SystemExit(f"no hologram row for #{n}")
    st = ver.get("structural_tests") or {}
    passed = sum(1 for v in st.values() if (v.get("pass") if isinstance(v, dict) else v))
    h["status"] = (h.get("status") or "DEPOSITED").split("; REISSUED")[0] + "; REISSUED 2026-11-10 as v1.2 (the records search of 2026-11-10; SPXI packet) and as v1.3 (the argument moves of the records that entered at v1.2); REISSUED 2026-11-11 as v1.4 (the fold-in of #1758 v1.1 and #1735 v9)"
    h["hologram_record"] = [rec(n)]
    h["structural_tests"] = f"{passed} of {len(st)} pass"
    al = kern.get("argument_layer")
    if al:
        h["argument_layer"] = {"file": f"{A}/files/AXN-{REG[n]['hex']}/kernel/04-arguments.jsonl", "moves": al["moves"], "edges": al["edges"],
                               "records_with_moves": al["records_with_moves"], "by_kind": al["by_kind"], "records_without_moves": al.get("records_without_moves", [])}
    rs = kern["records_search_v12"]
    h["records_search_v12"] = {"date": "2026-11-10", "stratum": "S0", "evidence": [r["record"] for r in rs["evidence"]["records"]],
                               "related_work": len(rs["related_work"]), "history": len(rs["history"]), "flags": len(rs["flags"]),
                               "rule": "additive; related work pointed to, its substance not extended into the frame (the author, 2026-11-10 18:20, 18:45)"}
    h["spxi"] = f"{A}/s/records/{n}/ (the SPXI packet in the record's body, added at v1.2, reissued at v1.3 and v1.4)"
    h["failure_flags_source"] = f"{kid} v1.4 (#{n}): " + (h.get("failure_flags_source") or "").split(": ", 1)[-1]
    done.append(n)
d["history"].append({"version": "1.31", "date": "2026-11-11", "note": ("#1755 EA-HK-REVFIRST-01 reissued in place as v1.4: the fold-in of In the Midst of the Seven v1.1 (#1758) and Revelation First v9 (#1735), "
    "seven claims added and the moves of both records brought to their new texts; the Revelation First hologram row updated in place; the Tenth Muse and the Historical Logos unchanged, the fold-in being for Revelation First. rebuild/mantle-bearing/v131_revfirst_v14.py.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("1.31 applied", done)
