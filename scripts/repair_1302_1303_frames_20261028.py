#!/usr/bin/env python3
"""repair_1302_1303_frames_20261028.py — #1302 and #1303 take their own texts: the APZPZ frames of Documents 208 and 209.

Lee Sharks, 2026-10-28: "lets fix those other records as well" (the mislabelled #1302, found while mapping the glyphic
index). Repair scope as ruled 2026-10-15: broken, missing and mislabelled files; standard, the text as published.

#1302 (THE GLYPHIC CHECKSUM, Document 208) and #1303 (GLYPHIC CHECKSUM UMBML MODULE, Document 209) are the Zenodo
records 10.5281/zenodo.18451995 and 10.5281/zenodo.18452131. Each was an APZPZ: the description field was the work, a
frame around an attached document ("This description IS the Zenodo packet. It exists only in the description field.
The attached document is the content; this text is the frame."). The restoration of 2026-07-28 seated the same blog
post in both, the UMBML specification, so the two records carried byte-identical text, the text of #426's work, and
#1302 carried a document that is not Document 208 in any form. The attached documents are held by #427 (Document
208, AI-Native Cryptography) and #426 (Document 209, the UMBML v0.5 specification).

Each record's body is replaced by its own description field as DataCite preserved it (data/datacite-full-backup.json),
characters kept (non-breaking spaces made plain). Front matter and headings of the deposit files are kept. Rehashed
with a new AXN at the same hex and family; axn_prior, body_status and modifications record the change.
    python3 scripts/repair_1302_1303_frames_20261028.py [--apply]"""
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import record_modification as rm
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

ON = "2026-10-28"
RULING = 'Lee Sharks, 2026-10-28: "lets fix those other records as well"'
JOBS = {1302: ("0527", "10.5281/zenodo.18451995", "THE GLYPHIC CHECKSUM (Document 208)", 427),
        1303: ("0528", "10.5281/zenodo.18452131", "GLYPHIC CHECKSUM UMBML MODULE (Document 209)", 426)}

d = json.loads((ROOT / "data/datacite-full-backup.json").read_text(encoding="utf-8"))
desc = {}


def walk(o):
    if isinstance(o, dict):
        a = o.get("attributes")
        if o.get("id") in {j[1] for j in JOBS.values()} and isinstance(a, dict) and a.get("descriptions"):
            desc[o["id"]] = a["descriptions"][0]["description"]
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)


walk(d)
regp = ROOT / "data/registry.json"
reg = json.loads(regp.read_text(encoding="utf-8"))
R = {int(x["deposit_number"]): x for x in reg["deposits"]}
for n, (hx, doi, title, holder) in JOBS.items():
    x = R[n]
    field = desc[doi].replace("\xa0", " ").replace("\r", "")
    field = "\n".join(l.rstrip() for l in field.split("\n"))
    while "\n\n\n\n" in field:
        field = field.replace("\n\n\n\n", "\n\n\n")
    field = field.strip() + "\n"
    assert field.startswith("ZENODO DESCRIPTION FIELD CONTENT\n\nFor: " + title), field[:120]
    tp, dp = ROOT / f"data/texts/AXN-{hx}-text.md", ROOT / f"data/deposits/AXN-{hx}.md"
    old_t = tp.read_text(encoding="utf-8")
    dep = dp.read_text(encoding="utf-8")
    fm_end = dep.index("\n---\n", 4) + 5
    assert dep[fm_end:].strip() == old_t.strip(), f"#{n}: deposit body is not the text file"
    new_t = field
    new_dep = dep[:fm_end] + "\n\n" + field
    print(f"#{n} {title}: {len(old_t)} -> {len(new_t)} chars; first line kept: {field.splitlines()[2]}")
    if "--apply" in sys.argv:
        tp.write_text(new_t, encoding="utf-8"); dp.write_text(new_dep, encoding="utf-8")
        h = hashlib.sha256(new_t.encode("utf-8")).hexdigest(); g = axn_glyph_from_hash(h)
        before = {"axn": x["axn"], "hash": x["hash"]}
        x.setdefault("axn_prior", []).append({"axn": x["axn"], "hash": x["hash"], "until": ON,
                                              "why": "the record's own text seated (repair_1302_1303_frames_20261028.py); the earlier bytes were the UMBML specification restored into both #1302 and #1303"})
        x["hash"] = h; x["axn_canonical"] = h; x["emoji"] = g
        x["axn"] = compose_axn(x["hex"], x.get("family", "UNCLASSIFIED"), g)
        x["clusters"] = axn_clusters_from_hash(h); x["reading"] = axn_reading_from_clusters(x["clusters"])
        if "axn_reading" in x:
            x["axn_reading"] = x["reading"]
        x["full_text_chars"] = len(new_t)
        bs = x.get("body_status") if isinstance(x.get("body_status"), dict) else {}
        bs.update({"class": "full", "lacuna": False, "recovery_status": "RESTORED-20261028", "recovered_from": f"DataCite description of {doi} (data/datacite-full-backup.json)",
                   "residual_chars": len(new_t), "restored_on": ON, "replaced": "the UMBML specification restored 2026-07-28 from the-glyphic-checksum-logotic.html, which is #426's work"})
        x["body_status"] = bs
        if n == 1302:
            old_desc = x.get("description")
            x["description"] = ("The APZPZ frame of Document 208: the Zenodo description field that was the packet, around the attached founding document "
                                "(#427). It reports the discovery of 1 February 2026, when an unprimed reader asked for context and primed readers translated "
                                "the emoji packet's structure, and states the checksum's formula, Glyphic Checksum = compress(Document) × gate(Context).")
            rm.touch(x, "description", "the description had been written from the UMBML specification the record wrongly carried", was=(old_desc or "")[:200], now=x["description"][:200], when=ON)
        x["text_repaired"] = {"on": ON, "kind": "mislabelled file", "source": f"DataCite description of {doi}", "attached_document_held_by": holder,
                              "hash_before": before["hash"], "axn_before": before["axn"], "ruled_by": RULING}
        rm.touch(x, "axn", f"the record's own text seated: the APZPZ frame of {title}, from its Zenodo description field as DataCite preserved it; "
                 f"the UMBML specification it carried is #426's work (the attached document of Document {'208 is #427' if n == 1302 else '209 is #426'})",
                 was=before["axn"], now=x["axn"], when=ON)
if "--apply" in sys.argv:
    regp.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    print("applied", R[1302]["axn"], R[1303]["axn"])
