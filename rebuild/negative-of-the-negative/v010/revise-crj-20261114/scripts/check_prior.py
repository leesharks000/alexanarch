import json, sys
from vlib import *
A = json.loads((ROOT/"datasets/negative-of-the-negative/v2/ledgers/classical-receptions-journal/ledger-archive.json").read_text())
bad=0
for c in A:
    if c["dep"]=="capture-registry":
        slug=c["locus"].split(",")[0]
        ok=found(c["quote"], entry_text(slug))
    else:
        ok=found(strip_md(c["quote"]), deposit_text(c["file"]))
    if not ok: bad+=1; print("FAIL",c["id"],c["locus"],c["quote"][:150])
print("archive", len(A)-bad, "/", len(A))
F = json.loads((ROOT/"datasets/negative-of-the-negative/v2/ledgers/classical-receptions-journal/field.json").read_text())
