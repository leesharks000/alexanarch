#!/usr/bin/env python3
"""EA-CORPORA-29/08 (session tool): the Pali Tipiṭaka in its root text, the harvest the Dhammapada seat (02/17) queued.

Source: suttacentral/bilara-data, branch published, at a pinned commit; the root Pali of the Mahāsaṅgīti edition
(root/pli/ms: sutta, vinaya, abhidhamma). The original is held as one byte-reproducible archive of that tree
(`git archive --format=tar <commit> root/pli/ms | gzip -n`), with the commit and the tree hash recorded, so that the
7,288 segment files are carried in the form the repository serves them without 7,288 manifest rows. The text layer is
one file per collection or book, each line `segment-id<TAB>text` in the repository's segment order, as the 02/17
Dhammapada layer is.
    python3 pali29.py <bilara-clone> <stage>"""
import json, pathlib, re, subprocess, sys, hashlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "ea-corpora-27"))
import seat as S

REPO, STAGE = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
COMMIT = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip()
TREE = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD:root/pli/ms"], text=True).strip()
seat = STAGE / "pali-tipitaka"
(seat / "original").mkdir(parents=True, exist_ok=True); (seat / "text").mkdir(parents=True, exist_ok=True)
arc = seat / "original" / f"bilara-data-{COMMIT[:12]}-root-pli-ms.tar.gz"
tar = subprocess.check_output(["git", "-C", str(REPO), "archive", "--format=tar", COMMIT, "root/pli/ms"])
arc.write_bytes(subprocess.run(["gzip", "-n", "-9"], input=tar, capture_output=True, check=True).stdout)
ROOT = REPO / "root/pli/ms"


def nat(p):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", p.as_posix())]


NAMES = {
 "sutta/dn": "Dīgha Nikāya", "sutta/mn": "Majjhima Nikāya", "sutta/sn": "Saṁyutta Nikāya", "sutta/an": "Aṅguttara Nikāya",
 "sutta/kn/kp": "Khuddakapāṭha", "sutta/kn/dhp": "Dhammapada", "sutta/kn/ud": "Udāna", "sutta/kn/iti": "Itivuttaka",
 "sutta/kn/snp": "Suttanipāta", "sutta/kn/vv": "Vimānavatthu", "sutta/kn/pv": "Petavatthu", "sutta/kn/thag": "Theragāthā",
 "sutta/kn/thig": "Therīgāthā", "sutta/kn/tha-ap": "Theraapadāna", "sutta/kn/thi-ap": "Therīapadāna", "sutta/kn/bv": "Buddhavaṁsa",
 "sutta/kn/cp": "Cariyāpiṭaka", "sutta/kn/ja": "Jātaka", "sutta/kn/mnd": "Mahāniddesa", "sutta/kn/cnd": "Cūḷaniddesa",
 "sutta/kn/ps": "Paṭisambhidāmagga", "sutta/kn/mil": "Milindapañha", "sutta/kn/ne": "Nettippakaraṇa", "sutta/kn/pe": "Peṭakopadesa",
 "vinaya/pli-tv-bu-pm": "Bhikkhupātimokkha", "vinaya/pli-tv-bi-pm": "Bhikkhunīpātimokkha", "vinaya/pli-tv-bu-vb": "Suttavibhaṅga (bhikkhu)",
 "vinaya/pli-tv-bi-vb": "Suttavibhaṅga (bhikkhunī)", "vinaya/pli-tv-kd": "Khandhaka", "vinaya/pli-tv-pvr": "Parivāra",
 "abhidhamma/ds": "Dhammasaṅgaṇī", "abhidhamma/vb": "Vibhaṅga", "abhidhamma/dt": "Dhātukathā", "abhidhamma/pp": "Puggalapaññatti",
 "abhidhamma/kv": "Kathāvatthu", "abhidhamma/ya": "Yamaka", "abhidhamma/patthana": "Paṭṭhāna"}
PIT = {"sutta": "Suttapiṭaka", "vinaya": "Vinayapiṭaka", "abhidhamma": "Abhidhammapiṭaka"}
works = []
for key, name in NAMES.items():
    d = ROOT / key
    files = sorted(d.rglob("*.json"), key=nat) if d.is_dir() else ([ROOT / f"{key}_root-pli-ms.json"] if (ROOT / f"{key}_root-pli-ms.json").exists() else [])
    if not files:
        raise SystemExit(f"missing {key}")
    slug = key.split("/")[-1].replace("pli-tv-", "")
    out = [f"# {name} — root Pali (Mahāsaṅgīti) · suttacentral/bilara-data@{COMMIT[:12]} · seat EA-CORPORA-29/08", ""]
    for f in files:
        for sid, txt in json.load(open(f, encoding="utf-8")).items():
            out.append(f"{sid}\t{txt.strip()}")
    tr = f"text/{key.split('/')[0]}-{slug}.txt"
    (seat / tr).write_text("\n".join(out) + "\n", encoding="utf-8")
    works.append({"slug": f"{key.split('/')[0]}-{slug}", "work": f"{name} ({PIT[key.split('/')[0]]}), root Pali, Mahāsaṅgīti edition — {len(files)} segment files of root/pli/ms/{key}",
                  "class": PIT[key.split("/")[0]], "text": tr, "originals": [f"original/{arc.name}"], "lines": len(out), "segment_files": len(files)})
LOCI = [("DN 1, Brahmajāla", "text/sutta-dn.txt", "Evaṁ me sutaṁ"), ("MN 1, Mūlapariyāya", "text/sutta-mn.txt", "mn1:1.1"),
        ("SN 56.11, Dhammacakkappavattana", "text/sutta-sn.txt", "sn56.11"), ("Snp 1.8, the Metta Sutta", "text/sutta-snp.txt", "Karaṇīyamatthakusalena"),
        ("Dhp 1", "text/sutta-dhp.txt", "Manopubbaṅgamā dhammā"), ("Bhikkhupātimokkha", "text/vinaya-bu-pm.txt", "pātimokkh"),
        ("Dhammasaṅgaṇī, the mātikā", "text/abhidhamma-ds.txt", "Kusalā dhammā"), ("Milindapañha", "text/sutta-mil.txt", "Milind")]
ver, miss = [], []
for lab, tr, find in LOCI:
    (ver if S.norm(find) in S.norm((seat / tr).read_text(encoding="utf-8")) else miss).append(f"{lab} — '{find}'")
nfiles = sum(w["segment_files"] for w in works)
src = {
 "corpus": "pali-tipitaka", "seat": "EA-CORPORA-29/08",
 "title": "The Pali Tipiṭaka: the Sutta, Vinaya and Abhidhamma Piṭakas in root Pali (Mahāsaṅgīti), from SuttaCentral",
 "edition": f"The Mahāsaṅgīti Tipiṭaka root text as published by SuttaCentral in suttacentral/bilara-data (branch published, commit {COMMIT}): {len(works)} collections and books, {nfiles} segment files.",
 "language": "pli", "fetched": "2026-10-28",
 "license": {"payload": "The root Pali of the canon is in the public domain; SuttaCentral distributes its Bilara data under CC0 (the repository's LICENSE.md and https://suttacentral.net/licensing), as recorded at the Dhammapada seat (02/17).",
             "record": "CC-BY-4.0 applies to this seat record only."},
 "origin": {"items": [{"source": "SuttaCentral (suttacentral/bilara-data)", "repository": "https://github.com/suttacentral/bilara-data", "branch": "published",
                       "commit": COMMIT, "path": "root/pli/ms", "tree": TREE, "file": f"original/{arc.name}",
                       "archive": "git archive --format=tar <commit> root/pli/ms | gzip -n -9", "sha256": S.sha(arc)}],
            "fetched": "2026-10-28", "transport": "in-session fetch (Transport D); No-Double-Draw"},
 "works": {"count": len(works), "units": "one text file per collection or book; each line segment-id TAB text", "list": works},
 "normalization": "The original is the repository's tree at the commit, archived by git (byte-reproducible from the commit and the command recorded). text/ joins each collection's segment files in natural order of their paths, one line per segment, the segment id kept, the text stripped of edge whitespace. Nothing corrected.",
 "scope": "The three piṭakas complete as SuttaCentral holds them in root Pali: the four Nikāyas and the Khuddaka books (with the Milindapañha, Nettippakaraṇa and Peṭakopadesa of the Burmese recension), the Vinaya (Suttavibhaṅga, Khandhaka, Parivāra, both Pātimokkhas) and the seven Abhidhamma books. The translations are held out; Sujato's Dhammapada is at 02/17.",
 "verified_loci": ver, "loci_not_found": miss, "lines_total": sum(w["lines"] for w in works),
 "why_seated": "The canon harvest the Dhammapada seat queued (02/17: 'CANON HARVEST QUEUED'), seated at the author's direction of 2026-10-28 for the twenty-ninth seating: 'we need buddhist canon, various traditions, mahayana included.'",
 "cross_references": {"pali-canon": "02/17 holds the Dhammapada in both layers (root and Sujato's English); this seat holds the whole root canon, the Dhammapada again inside the Khuddaka Nikāya."},
 "spine": "29/08", "ruling": "The author's direction of 2026-10-28.", "seating": "EA-CORPORA-29"}
(seat / "source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(seat / "MANIFEST.sha256").write_text("\n".join(f"{S.sha(p)}  {p.relative_to(seat).as_posix()}" for p in sorted(seat.rglob('*')) if p.is_file() and p.name not in ('MANIFEST.sha256', 'source.json')) + "\n")
print("pali-tipitaka", len(works), "works", nfiles, "files", src["lines_total"], "lines; loci ok", len(ver), "missing", miss)
