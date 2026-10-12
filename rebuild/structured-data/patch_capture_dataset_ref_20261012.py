#!/usr/bin/env python3
"""Patch the stale capture-registry Dataset reference in record pages' JSON-LD (2026-10-12).

Search Console's Dataset report (2026-10-09): 'Missing field "description"' (35 items), 'license' and 'creator'
(34). 39 record pages carry an old subjectOf/isPartOf form — {"@type":"Dataset","name":"EA-WG-CAPTURES-01","url":
"https://www.machinemediation.org/data/registry.json"} — written before wire_deposit.py's reference was completed.
They cannot be re-rendered: the renderer refuses pages carrying retirement apparatus (atlas addendum v1.3). So the
one string is replaced, in place, with the reference wire_deposit.py now writes; nothing else on the page changes.
Idempotent.
"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from build_capture_gallery import CAPTURE_DATASET_REF
OLD = '"isPartOf": {"@type": "Dataset", "name": "EA-WG-CAPTURES-01", "url": "https://www.machinemediation.org/data/registry.json"}'
REF = dict(CAPTURE_DATASET_REF, distribution={"@type": "DataDownload", "encodingFormat": "application/json",
                                              "contentUrl": "https://www.alexanarch.org/data/EA-WG-CAPTURES-01.json"})
NEW = '"isPartOf": ' + json.dumps(REF, ensure_ascii=False)
n = 0
for p in sorted((ROOT / "s/records").glob("*/index.html")):
    h = p.read_text(encoding="utf-8")
    if OLD in h:
        p.write_text(h.replace(OLD, NEW), encoding="utf-8"); n += 1
print("patched", n, "record pages")
