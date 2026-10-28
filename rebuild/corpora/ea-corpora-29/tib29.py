#!/usr/bin/env python3
"""EA-CORPORA-29/11 (session tool): the Derge Kangyur, eight volumes, from Esukhia/derge-kangyur at a pinned commit.

The volumes are kept as the repository serves them (original/<volume file>), and the text layer is the same text
under an ASCII name (text/<slug>.txt), line endings normalized; the repository's markup ([1a], [1b.1], {D21}) stays.
Loci are the Tohoku markers of the sūtras the seat is chosen for, looked up in the volumes that carry them.
    python3 tib29.py <derge-kangyur clone> <stage>"""
import json, pathlib, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "ea-corpora-27"))
import seat as S
REPO, STAGE = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
COMMIT = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip()
VOLS = [("001", "vinaya-ka", "Vinaya ('dul ba), volume ka: the Vinayavastu begins (Toh 1)", "Vinaya"),
        ("033", "prajnaparamita-8000", "Prajñāpāramitā (brgyad stong pa): the Aṣṭasāhasrikā (Toh 12)", "Prajñāpāramitā"),
        ("034", "prajnaparamita-various", "Prajñāpāramitā, various (shes rab sna tshogs): the Diamond (Toh 16) and the Heart (Toh 21) among the shorter sūtras", "Prajñāpāramitā"),
        ("046", "sutra-kha", "Sūtra (mdo sde), volume kha: the Lalitavistara (Toh 95)", "Sūtra"),
        ("049", "sutra-ca", "Sūtra (mdo sde), volume ca: the Laṅkāvatāra (Toh 107)", "Sūtra"),
        ("051", "sutra-ja", "Sūtra (mdo sde), volume ja: the White Lotus of the True Dharma (Toh 113) and the Sukhāvatīvyūha (Toh 115)", "Sūtra"),
        ("060", "sutra-ma", "Sūtra (mdo sde), volume ma: the Teaching of Vimalakīrti (Toh 176)", "Sūtra"),
        ("103", "karchag", "The catalogue of the Derge Kangyur (dkar chag)", "Catalogue")]
LOCI = [("033", "D12", "the Aṣṭasāhasrikā"), ("034", "D16", "the Diamond Sūtra"), ("034", "D21", "the Heart Sūtra"), ("046", "D95", "the Lalitavistara"),
        ("049", "D107", "the Laṅkāvatāra"), ("051", "D113", "the Lotus Sūtra"), ("051", "D115", "the Sukhāvatīvyūha"), ("060", "D176", "the Vimalakīrtinirdeśa")]
seat = STAGE / "derge-kangyur"
(seat / "original").mkdir(parents=True, exist_ok=True); (seat / "text").mkdir(parents=True, exist_ok=True)
works, slugof = [], {}
for num, slug, work, cls in VOLS:
    src = next((REPO / "text").glob(f"{num}_*.txt"))
    b = src.read_bytes()
    (seat / "original" / src.name).write_bytes(b)
    (seat / "text" / f"{num}-{slug}.txt").write_bytes(b.replace(b"\r\n", b"\n"))
    slugof[num] = f"text/{num}-{slug}.txt"
    works.append({"slug": f"{num}-{slug}", "work": f"Derge Kangyur, volume {int(num)}: {work}", "class": cls, "text": slugof[num],
                  "originals": [f"original/{src.name}"], "lines": b.count(b"\n")})
ver, miss = [], []
for num, d, lab in LOCI:
    t = (seat / slugof[num]).read_text(encoding="utf-8")
    (ver if "{" + d + "}" in t else miss).append(f"{lab} — Tohoku marker {{{d}}} in volume {int(num)}")
src = {
 "corpus": "derge-kangyur", "seat": "EA-CORPORA-29/11",
 "title": "The Derge Kangyur in Tibetan: the Vinaya's first volume, the Perfection of Wisdom, the sūtra volumes of the Lalitavistara, the Laṅkāvatāra, the Lotus, the Sukhāvatīvyūha and the Vimalakīrti, and the catalogue",
 "edition": f"The Digital Derge Kangyur of the Esukhia–Barom proofreading project (2014–2018), from the UVA–SOAS 2013 eKangyur, after the Derge woodblock edition held by the Library of Congress (BDRC W4CZ5369): Esukhia/derge-kangyur at commit {COMMIT} (archived; continued as OpenPecha P000001). Eight of its 103 volumes.",
 "language": "bod", "fetched": "2026-10-28",
 "license": {"payload": "Public domain: the repository's README states, under License, 'This work is a mechanical reproduction of a Public Domain work, and as such is also in the Public Domain.'",
             "record": "CC-BY-4.0 applies to this seat record only."},
 "origin": {"items": [{"source": "Esukhia (Esukhia/derge-kangyur)", "repository": "https://github.com/Esukhia/derge-kangyur", "commit": COMMIT,
                       "files": [w["originals"][0] for w in works]}], "fetched": "2026-10-28", "transport": "in-session fetch (Transport D); No-Double-Draw"},
 "works": {"count": len(works), "units": "one text file per volume", "list": works},
 "normalization": "The volumes as the repository serves them under original/; text/ the same text under ASCII names, line endings normalized. The repository's markup is kept: [1a] and [1b.1] for folio and line, {D…} for the Tohoku number at the head of each text.",
 "scope": "Eight volumes, chosen so that the Mahāyāna sūtras seated in Sanskrit (29/09) and in Chinese (29/10) stand also in Tibetan, with the Vinaya's opening and the catalogue by which the rest is found. The other 95 volumes are queued.",
 "verified_loci": ver, "loci_not_found": miss, "lines_total": sum(w["lines"] for w in works),
 "why_seated": "At the author's direction of 2026-10-28 for the twenty-ninth seating: the Buddhist canon in its several traditions, Mahāyāna included.",
 "queued": ["The remaining 95 volumes of the Derge Kangyur (287 MB in all), and the Tengyur (Esukhia/derge-tengyur): too large for one bundle; to be seated by volume groups"],
 "cross_references": {"same_sutras": "Sanskrit: buddhist-sanskrit (29/09); Chinese: east-asian-buddhism (29/10); Pali: pali-tipitaka (29/08)."},
 "classes": ["Vinaya", "Prajñāpāramitā", "Sūtra", "Catalogue"],
 "spine": "29/11", "ruling": "The author's direction of 2026-10-28.", "seating": "EA-CORPORA-29"}
(seat / "source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(seat / "MANIFEST.sha256").write_text("\n".join(f"{S.sha(p)}  {p.relative_to(seat).as_posix()}" for p in sorted(seat.rglob('*')) if p.is_file() and p.name not in ('MANIFEST.sha256', 'source.json')) + "\n")
print("derge-kangyur", len(works), "volumes", src["lines_total"], "lines; loci ok", len(ver), "missing", miss)
