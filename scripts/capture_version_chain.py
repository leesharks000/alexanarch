"""The version chain of the Capture Registry (EA-WG-CAPTURES-01), bound in one file.

    python3 scripts/capture_version_chain.py --check     # report any snapshot deposit or frozen copy missing from the chain
    python3 scripts/capture_version_chain.py --markdown  # print the chain section for a snapshot deposit's body

The chain lives at rebuild/capture-registry/VERSION-CHAIN.json: every edition the registry has had, in order, whether deposited
as a snapshot, kept as a frozen copy in the repository, published only at machinemediation.org, or released on Zenodo and severed.
--check reads the deposit registry for every deposit of series 'ea-wg-captures' (or titled as an edition of EA-WG-CAPTURES-01) and every
frozen copy on disk named EA-WG-CAPTURES-01-v*.json, and reports any not in the chain. Laws record; they do not prevent: the check prints
what is missing and exits 0, so a build never stops on it; the snapshot's author adds the missing edition to the chain before drafting.
Written 2026-11-05 at the operator's word: "lets please make sure that chain is bound together so we can stop doing that".
"""
import json, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
CHAIN = ROOT / "rebuild/capture-registry/VERSION-CHAIN.json"

def deposits():
    R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))
    D = R["deposits"] if isinstance(R, dict) else R
    out = []
    for d in D:
        t = d.get("title") or ""
        if d.get("version_series_id") in ("ea-wg-captures", "SERIES-EA-WG-CAPTURES-01") or re.match(r"AI Overview Capture Registry( —|\s+EA-WG|\s+v\d)", t):
            out.append(d)
    return out

def frozen():
    return sorted(str(p.relative_to(ROOT)) for p in ROOT.glob("data/**/EA-WG-CAPTURES-01-v*.json"))

def check():
    C = json.loads(CHAIN.read_text(encoding="utf-8"))
    held_dep = {n for e in C["editions"] for n in e.get("deposits", [])}
    held_file = {e["file"] for e in C["editions"] if e.get("file")}
    miss_d = [(d.get("deposit_number"), d.get("title", "")[:90]) for d in deposits() if d.get("deposit_number") not in held_dep]
    miss_f = [f for f in frozen() if f not in held_file]
    for n, t in miss_d: print(f"MISSING deposit #{n}: {t}")
    for f in miss_f: print(f"MISSING frozen copy: {f}")
    if not miss_d and not miss_f:
        print(f"chain bound: {len(C['editions'])} editions; every snapshot deposit ({len(held_dep)}) and frozen copy ({len(held_file)}) is in it")
    return miss_d, miss_f

def markdown():
    C = json.loads(CHAIN.read_text(encoding="utf-8"))
    parts = []
    for e in C["editions"]:
        v = e["version"]
        if e.get("deposits"): parts.append(f"{v} ({', '.join('#%d' % n for n in e['deposits'])})")
        elif e.get("file"): parts.append(f"{v} (frozen copy, `{e['file']}`)")
        else: parts.append(f"{v} ({e['kind'].replace('_', ' ')})")
    print("## Version chain\n\n" + " → ".join(parts) + "\n\nThe chain is bound in `rebuild/capture-registry/VERSION-CHAIN.json`, which lists each edition's date, count, kind and location; `scripts/capture_version_chain.py --check` reports any snapshot deposit or frozen copy missing from it.")

if __name__ == "__main__":
    if "--markdown" in sys.argv: markdown()
    else: check()
