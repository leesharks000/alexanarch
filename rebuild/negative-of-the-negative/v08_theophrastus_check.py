#!/usr/bin/env python3
"""Checks for the EA-NEGONT-02 v0.8 draft's worked case (Theophrastus), run against the draft file.

    python3 rebuild/negative-of-the-negative/v08_theophrastus_check.py <draft.md>

1. Every claim id the draft cites exists in the entity's field or archive ledger.
2. Every field claim F1..F62 is carried in the translation table (R2, D_pres).
3. The KO's coverage of field and archive claims.
4. KO_B sentences surviving in the draft KO (R7): similarity >= 0.95, with positions.
5. Every Greek string the table quotes from a receiving text is present in the seated text (#1580).
6. The /non register's v0.7 KO, for comparison: KO_B sentences surviving there."""
import json, re, sys, difflib, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
draft = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
L = ROOT / "datasets/negative-of-the-negative/v2/ledgers/theophrastus"
field = json.loads((L / "field.json").read_text(encoding="utf-8"))["field_claims"]
arch = {c["id"]: c for c in json.loads((L / "ledger-archive.json").read_text(encoding="utf-8"))}
row = json.loads((ROOT / "datasets/negative-of-the-negative/v2/rows/theophrastus.json").read_text(encoding="utf-8"))
KO_B = [s["text"] for s in row["objects"]["KO_B"]["sentences"]]
KO7 = [s["text"] for s in row["objects"]["KO"]["sentences"]]

def expand(tok):
    m = re.fullmatch(r"F(\d+)[–-]F(\d+)", tok)
    return [f"F{i}" for i in range(int(m.group(1)), int(m.group(2)) + 1)] if m else [tok]

ids = set(re.findall(r"\b(?:F\d+(?:[–-]F\d+)?|T\d+-\d+)\b", draft))
cited = {x for t in ids for x in expand(t)}
bad = sorted(x for x in cited if x not in field and x not in arch)
print("1. cited ids not in either ledger:", bad or "none")

tab = draft.split("### 3.2. The translation table")[1].split("### 3.3.")[0]
tab_f = {x for t in re.findall(r"\bF\d+(?:[–-]F\d+)?\b", tab) for x in expand(t)}
missing = sorted((k for k in field if k not in tab_f), key=lambda k: int(k[1:]))
print(f"2. field claims carried in the translation table: {len(field) - len(missing)} of {len(field)}; missing:", missing or "none")

ko = draft.split("### 3.3. The knowledge object (draft)")[1].split("### 3.4.")[0]
sents = re.findall(r"^\d+\. (.+?) `([^`]+)`\s*$", ko, re.M)
ko_ids = {x for _, c in sents for t in c.split() for x in expand(t)}
kf = sorted((k for k in field if k in ko_ids), key=lambda k: int(k[1:]))
ka = sorted(k for k in arch if k in ko_ids)
print(f"3. KO: {len(sents)} sentences; field claims cited {len(kf)} of {len(field)}; archive claims cited {len(ka)} of {len(arch)}")
print("   field claims not cited in the KO:", sorted((k for k in field if k not in ko_ids), key=lambda k: int(k[1:])) or "none")

def survive(B, A):
    out = []
    for b in B:
        r = max((difflib.SequenceMatcher(None, a, b).ratio(), i + 1) for i, a in enumerate(A))
        out.append(r[1] if r[0] >= 0.95 else None)
    return out
pos8 = survive(KO_B, [s for s, _ in sents]); pos7 = survive(KO_B, KO7)
print(f"4. v0.8 draft: KO_B sentences surviving {sum(p is not None for p in pos8)} of {len(KO_B)}, positions {pos8}")
print(f"6. v0.7 KO:    KO_B sentences surviving {sum(p is not None for p in pos7)} of {len(KO_B)}, positions {pos7}")

ws = lambda s: re.sub(r"\s+", " ", s)   # the seated text breaks lines inside sentences
DL = ws((ROOT / "data/corpora/diogenes-laertius/text/tlg001.txt").read_text(encoding="utf-8"))
ST = ws((ROOT / "data/corpora/strabo/text/tlg001.txt").read_text(encoding="utf-8"))
greek = re.findall(r"(DL V\.\d+(?:–\d+)?|Strabo XIII\.\d\.\d+): ([Ͱ-Ͽἀ-῿ ,ʼ·]+[Ͱ-Ͽἀ-῿])", tab)
print("5. Greek quoted from receiving texts:")
for loc, g in greek:
    src = ST if loc.startswith("Strabo") else DL
    print(f"   {'ok ' if g.strip() in src else 'MISSING'} {loc}: {g.strip()[:70]}")
