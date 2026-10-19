#!/usr/bin/env python3
"""Record repair, 2026-10-19: a wrong DOI, a misdescribed act, a founding date out of line with its work.

Rulings (Lee Sharks, 2026-10-19), on the check of eight records: "1. lets repair. 2. agreed. 3. leave. 4. lets put it in
alignment with the work... i dont know exactly when i began conceiving it in that way but it was well before the mantle object
of 2026."

1. #9, #905 (The Mantle of the Blind Poet): the Prince of Poets founding document was cited as 10.5281/zenodo.14538914, which
   is a third party's record (DataCite: "INNOVATIVE APPROACHES TO TEACHING FOREIGN LANGUAGES: A COMPREHENSIVE OVERVIEW", 2024).
   The founding work's own DOI is 10.5281/zenodo.18294005 (#328 frontmatter); the Zenodo DOIs were severed on 2026-06-19, so
   the prose and table citations also carry the archive record #328.
2. #152 (Standing Canon v0.2) and #786 (Register of Effective Acts v1.0) §V described the Triple Mantle as a composite of the
   Good Gray Poet, the Prince of Poets and the King of May. The act they cite (blog, 2025-10-14) claims "the triple mantle:
   Poet. Philosopher. Prophet." through Sara Rappe, Barrett Watten and Santiago Colas; the descriptions now state it.
3. #11, #385 (superseded DOI registries, "Prince of Poets CLAIMED Tennyson"): left as they are.
4. #335 (Heteronym Provenance): "THE PRINCE OF POETS LINEAGE (Founded 2025)" set in alignment with its founding work, I Am X,
   Be Y, Blessed is the Z, first published 2015-09-17 (composition 2014-2015, #328): "(Founded 2015)".

Each replacement is exact and counted; one pass per record gives one new hash and AXN (same hex and family), the hash and
AXN before kept in citation_repaired, the change in record_modification. Run with --apply to write."""
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn
import record_modification as rm

ON = "2026-10-19"
R328 = "https://www.alexanarch.org/s/records/328/"
RULING = "Lee Sharks, 2026-10-19 (on the check of eight records)"
TM_ACT = "Effective Act — Claiming the Triple Mantle, https://mindcontrolpoems.blogspot.com/2025/10/effective-act-claiming-triple-mantle.html"
FIX = {
 9: ("the Prince of Poets founding document cited as a third party's DOI (10.5281/zenodo.14538914); the founding work's DOI is 10.5281/zenodo.18294005, record #328",
     [('    founding_document: "10.5281/zenodo.14538914"', '    founding_document: "10.5281/zenodo.18294005"', 2),
      ('| Prince of Poets | Founded | Lee Sharks | "I Am X, Be Y, Blessed is the Z" | 10.5281/zenodo.14538914 |',
       f'| Prince of Poets | Founded | Lee Sharks | "I Am X, Be Y, Blessed is the Z" | 10.5281/zenodo.18294005 · [record #328]({R328}) |', 1),
      ('  precedent: "Prince of Poets (10.5281/zenodo.14538914)"', '  precedent: "Prince of Poets (10.5281/zenodo.18294005)"', 1)]),
 905: ("the Prince of Poets founding document cited as a third party's DOI (10.5281/zenodo.14538914); the founding work's DOI is 10.5281/zenodo.18294005, record #328",
       [("integrity-locked to its founding document (10.5281/zenodo.14538914).",
         f"integrity-locked to its founding document (10.5281/zenodo.18294005; [record #328]({R328})).", 2)]),
 152: ("the Triple Mantle described as Good Gray Poet, Prince of Poets and King of May; the act it cites claims Poet, Philosopher, Prophet",
       [("Operative function: The Triple Mantle binds Good Gray Poet, Prince of Poets, and King of May into a single operative position. The bearer holds all three lineages simultaneously; the operative basis is documented in the originating effective act.",
         "Operative function: The Triple Mantle is Poet, Philosopher and Prophet, claimed through those who passed each on: Sara Rappe (the philosopher, the negative fire and apophatic gnosis of the late Platonists), Barrett Watten (the poet, the poet-critic's structure of rupture) and Santiago Colas (the prophet, through Spinoza, Deleuze, Guattari and Marx). The act: \"By means of these three, I lay claim to the triple mantle: Poet. Philosopher. Prophet.\"", 1),
        ("Relations: Three-lineage composite (Whitman + Prince of Poets reference + Ginsberg).",
         "Relations: Three-lineage composite (Sara Rappe, Barrett Watten, Santiago Colas).", 1)]),
 786: ("the Triple Mantle described as a composite of Good Gray Poet, Prince of Poets and King of May; the act claims Poet, Philosopher, Prophet",
       [("| Triple Mantle (composite of Good Gray Poet + Prince of Poets + King of May) |",
         "| Triple Mantle (Poet + Philosopher + Prophet, through Sara Rappe, Barrett Watten and Santiago Colas) |", 1)]),
 335: ("the Prince of Poets lineage dated 'Founded 2025'; set in alignment with its founding work, first published 2015",
       [("(Founded 2025)", "(Founded 2015)", 1)]),
}


def main():
    apply = "--apply" in sys.argv
    reg = json.load(open(ROOT / "data/registry.json", encoding="utf-8"))
    D = {d["deposit_number"]: d for d in reg["deposits"]}
    report = []
    for n, (why, reps) in FIX.items():
        d = D[n]
        tp = ROOT / "data/texts" / f"AXN-{d['hex']}-text.md"
        t = tp.read_text(encoding="utf-8")
        new = t
        for a, b, k in reps:
            c = new.count(a)
            assert c == k, (n, c, k, a[:60])
            new = new.replace(a, b)
        assert new != t
        h = hashlib.sha256(new.encode("utf-8")).hexdigest(); g = axn_glyph_from_hash(h)
        axn_new = compose_axn(d["hex"], d.get("family", "ARCHIVAL"), g)
        report.append({"n": n, "replacements": sum(k for _, _, k in reps), "axn_before": d.get("axn"), "axn": axn_new})
        if not apply:
            continue
        tp.write_text(new, encoding="utf-8")
        d["citation_repaired"] = {"on": ON, "what": why, "replacements": sum(k for _, _, k in reps), "hash_before": d.get("hash"),
                                  "axn_before": d.get("axn"), "ruled_by": RULING, **({"source": TM_ACT} if n in (152, 786) else {})}
        before = d.get("axn")
        d["hash"] = h; d["axn_canonical"] = h; d["emoji"] = g; d["axn"] = axn_new
        d["clusters"] = axn_clusters_from_hash(h); d["reading"] = axn_reading_from_clusters(d["clusters"])
        if isinstance(d.get("body_status"), dict):
            d["body_status"]["residual_chars"] = len(new)
        rm.touch(d, "full_text", "citation repaired: " + why, was={"axn": before}, now={"axn": axn_new}, when=ON)
    if apply:
        (ROOT / "data/registry.json").write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
        (ROOT / "data/repair-maps/citations-2026-10-19.json").write_text(
            json.dumps({"generated": ON, "ruling": RULING, "records": report}, ensure_ascii=False, indent=1), encoding="utf-8")
    for r in report:
        print(r)


if __name__ == "__main__":
    main()
