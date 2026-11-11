#!/usr/bin/env python3
"""mantle-bearing 1.28: the four framework holograms reissued in place as v1.2 (2026-11-10), at the author's word of that evening ("lets address, deposit,
and turn to incorporating it into rev first and versioning all four holographic frames... also - if the framed themselves have not yet been spxi treated,
they need to be"). Each hologram row: status, record, structural tests and the argument layer's counts read from the v1.2 files; the records search of
2026-11-10 (stratum S0) recorded with its evidence records; the SPXI packet noted. The framework rows keep their states; their governing record re-read.
In place on the rows each table holds; no row added.
    python3 rebuild/mantle-bearing/v128_holograms_v12.py"""
import json, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
A = "https://www.alexanarch.org"
rec = lambda n: {"deposit": n, "axn": REG[n]["axn"], "url": f"{A}/s/records/{n}/", "title": REG[n]["title"]}
d = json.loads(SRC.read_text(encoding="utf-8"))
if any(h["version"] == "1.28" for h in d["history"]): raise SystemExit("1.28 already applied")
assert d["history"][-1]["version"] == "1.27", d["history"][-1]["version"]
done = []
for n, kid in [(1754, "EA-HK-ORTHONYM-01"), (1755, "EA-HK-REVFIRST-01"), (1756, "EA-HK-TENTHMUSE-01"), (1757, "EA-HK-HISTLOGOS-01")]:
    assert REG[n]["version"] == "v1.2", (n, REG[n]["version"])
    K = ROOT / f"files/AXN-{REG[n]['hex']}/kernel"
    kern = yaml.safe_load((K / "00-kernel.yaml").read_text(encoding="utf-8")); ver = json.loads((K / "10-verification.json").read_text(encoding="utf-8"))
    h = next((x for x in d["holograms"] if any(r.get("deposit") == n for r in (x.get("hologram_record") or []))), None)
    if h is None: raise SystemExit(f"no hologram row for #{n}")
    st = ver.get("structural_tests") or {}
    passed = sum(1 for v in st.values() if (v.get("pass") if isinstance(v, dict) else v))
    h["status"] = (h.get("status") or "DEPOSITED").split("; REISSUED")[0] + "; REISSUED 2026-11-10 as v1.2 (the records search of 2026-11-10; SPXI packet)"
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
    h["spxi"] = f"{A}/s/records/{n}/ (the SPXI packet in the record's body, added at v1.2)"
    h["failure_flags_source"] = f"{kid} v1.2 (#{n}): " + (h.get("failure_flags_source") or "").split(": ", 1)[-1]
    done.append(n)
if not any("records_search_v12" in str(x) for x in d["schema"]["holograms"]):
    d["schema"]["holograms"].append("(1.28) records_search_v12: date, stratum, evidence, related_work, history, flags, rule; spxi"); d["schema"]["holograms"] += ["records_search_v12", "spxi"]
d["history"].append({"version": "1.28", "date": "2026-11-10", "note": ("#1754, #1755, #1756 and #1757 reissued in place as v1.2: the records search of 2026-11-10 entered "
    "each kernel as stratum S0, In the Midst of the Seven (#1758) among the evidence of Revelation First, the Tenth Muse and the Historical Logos; related work, history "
    "and flags carried in each kernel; each body given an SPXI packet. The four hologram rows updated in place. rebuild/mantle-bearing/v128_holograms_v12.py.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("1.28 applied", done)
