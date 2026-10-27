#!/usr/bin/env python3
"""rederive_axns_20261027.py — every deposit's AXN made to derive from the record it names.

MANUS, 2026-10-27: "i think its time to address the batch hashed axns. axns should match their records."
On the scope: "1. all 762." On the texts that quote an old AXN: "2. leave as is as long as old axns resolve
correctly." On the glyph table: "fill the two." (scripts/axn_lib.py, table v2.1: 0x6E "⏳", 0xCF "🖤").

WHAT IT DOES
For every registry entry whose canonical text file exists, the SHA-256 of that file is taken and the AXN derived
from it with the current table, keeping the entry's hex position and family. Where the result differs from the
stored AXN, the entry's hash, glyphs, clusters, reading and AXN are set to the derived values, and the prior form is
appended to `axn_prior` (with the hash it carried, the date and the reason), so that the old string still names
the record. Reasons:
  batch           the 2026-06-20 batch assignment: the stored hash is of no bytes the archive holds
  text_changed    the AXN was derived at mint; the canonical text was changed afterwards (repairs, recovered text)
  glyph_table     the hash is the text's, the glyphs were not derived from it with the canonical table
  table_v2_1      the AXN was right under table v2.0 and passes through one of the two slots filled on 2026-10-27
No canonical text is changed. Other records' texts that quote a prior AXN are left as published; the prior forms
resolve through /api/axn-aliases.json, the resolver pages and the record pages.

Writes: data/registry.json (compact form, as main keeps it), data/api/axn-aliases.json, one record_modification
entry per changed deposit. --dry-run prints the changes and a sample, writes nothing.
    python3 scripts/rederive_axns_20261027.py --dry-run [--sample N...]
    python3 scripts/rederive_axns_20261027.py --apply
"""
import hashlib, json, pathlib, sys, collections
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import axn_lib as A
import record_modification as rm

ON = "2026-10-27"
RULED = ('Lee Sharks, 2026-10-27: "axns should match their records" — "1. all 762." — '
         '"2. leave as is as long as old axns resolve correctly." — "fill the two."')


def classify(d, hf):
    fam = d["axn"].split(".")[1]
    if A.derive_axn(hf, d["hex"], fam) == d["axn"]:
        return None
    if A.compose_axn(d["hex"], fam, A.axn_glyph_from_hash(hf, A.AXN_GLYPHS_V20)) == d["axn"]:
        return "table_v2_1"
    if "founding_event" in d and d.get("hash") != hf:
        return "batch"
    if d.get("hash") != hf:
        return "text_changed"
    return "glyph_table"


WHY = {"batch": "the 2026-06-20 batch assignment; the stored hash is of no bytes the archive holds",
       "text_changed": "derived at mint; the canonical text was changed afterwards, and the AXN stayed on the earlier bytes",
       "glyph_table": "the hash is the text's; the glyphs were not derived from it with the canonical table",
       "table_v2_1": "derived under glyph table v2.0; passes through a slot filled in table v2.1 (2026-10-27)"}


def main():
    apply = "--apply" in sys.argv
    reg_path = ROOT / "data/registry.json"
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    changes, kinds = [], collections.Counter()
    for d in reg["deposits"]:
        p = ROOT / str(d.get("full_text_path", "")).lstrip("/")
        if not p.is_file():
            continue
        hf = hashlib.sha256(p.read_bytes()).hexdigest()
        k = classify(d, hf)
        if not k:
            continue
        fam = d["axn"].split(".")[1]
        new = A.derive_axn(hf, d["hex"], fam)
        prior = {"axn": d["axn"], "hash": d.get("hash"), "until": ON, "why": WHY[k]}
        changes.append((d, k, new, hf, prior)); kinds[k] += 1
    print(f"{len(changes)} AXNs to re-derive:", dict(kinds))
    if "--sample" in sys.argv:
        want = {int(x) for x in sys.argv[sys.argv.index("--sample") + 1:] if x.isdigit()}
        for d, k, new, hf, prior in changes:
            if d["deposit_number"] in want:
                print(f"  #{d['deposit_number']} [{k}] {prior['axn']}  ->  {new}")
    if not apply:
        return
    aliases = {}
    for d, k, new, hf, prior in changes:
        cl = A.axn_clusters_from_hash(hf)
        d.setdefault("axn_prior", []).append(prior)
        d["hash"] = hf; d["axn_canonical"] = hf
        d["emoji"] = A.axn_glyph_from_hash(hf); d["axn"] = new
        d["clusters"] = cl; d["axn_reading"] = A.axn_reading_from_clusters(cl)
        if "reading" in d:
            d["reading"] = d["axn_reading"]
        d["axn_glyph_table"] = A.AXN_GLYPH_TABLE
        fe = d.get("founding_event")
        if isinstance(fe, dict) and fe.get("batch_axn_current"):
            fe["batch_axn_current"] = False
            fe["batch_axn_superseded"] = {"on": ON, "by": new, "ruled_by": RULED}
        rm.touch(d, "axn", f"AXN re-derived from the canonical text ({k})", was=prior["axn"], now=new, when=ON)
    for d in reg["deposits"]:
        forms = [x["axn"] for x in d.get("axn_prior", [])]
        rd = d.get("axn_rederived")
        if isinstance(rd, dict) and rd.get("axn_before"):
            forms.insert(0, rd["axn_before"])
        fe = d.get("founding_event")
        if isinstance(fe, dict) and fe.get("batch_axn"):
            forms.insert(0, fe["batch_axn"])
        for f in dict.fromkeys(forms):
            if f != d["axn"]:
                aliases[f] = {"deposit_number": d["deposit_number"], "hex": d["hex"], "axn": d["axn"],
                              "record": f"https://www.alexanarch.org/s/records/{d['deposit_number']}/"}
    reg_path.write_text(json.dumps(reg, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    out = {"name": "AXN aliases", "generated": ON, "glyph_table": A.AXN_GLYPH_TABLE,
           "description": ("Every prior form of an archive AXN, each mapped to the record it names and that record's current AXN. "
                           "A prior form is a full AXN string the record once carried: a batch assignment of 2026-06-20, an AXN "
                           "derived from an earlier state of the text, or a glyph string not derived with the canonical table. "
                           "The hex position never changes; the glyphs follow the record's bytes."),
           "ruling": RULED, "count": len(aliases), "aliases": aliases}
    (ROOT / "data/api/axn-aliases.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"applied: {len(changes)} re-derived; {len(aliases)} prior forms in data/api/axn-aliases.json")


if __name__ == "__main__":
    main()
