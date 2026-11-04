#!/usr/bin/env python3
"""Write the EA-CORPORA-33 deposit issue body from the five seat records (the form of body32.py).
Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-33-issue.md"""
import json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = ROOT / "data/corpora"
SEATS = [("tacitus", "Seat 33/01 — Tacitus", "The five works in Latin; Histories 5.13, the portents before the siege of Jerusalem"),
         ("pindar", "Seat 33/02 — Pindar", "The four books of victory odes, in Sandys's Greek"),
         ("bacchylides", "Seat 33/03 — Bacchylides", "The epinicians and dithyrambs of the London papyrus, in Jebb's Greek"),
         ("poetae-melici-bergk", "Seat 33/04 — The melic poets, in Bergk (1882)", "Poetae Lyrici Graeci III, whole, in thirty-five sections: Alcman to the Carmina popularia"),
         ("lyra-graeca-edmonds-i", "Seat 33/05 — Edmonds, Lyra Graeca I (1922)", "Sappho and Alcaeus with the papyri published after 1882, and Alcman, Terpander, Arion, Eumelus")]
lic = lambda l: l["payload"] if isinstance(l, dict) else str(l)


def section(corpus, heading, sub):
    s = json.loads((A / corpus / "source.json").read_text(encoding="utf-8"))
    w = s["works"]["list"]
    out = [f"## {heading}", "", f"*{sub}*", ""]
    if len(w) > 12:
        cnt = Counter(x.get("class", "") for x in w)
        out += ["- Works by class: " + "; ".join(f"{k} {v}" for k, v in cnt.items())]
    out += (["- Works:"] + [f"  - {x['work']}" for x in w]) if w else ["- Works: none held; the seat is a declared absence (" + s["works"]["units"] + ")"]
    out += [f"- Licence: {lic(s['license'])}"] + [f"- Verified locus: {v}" for v in s["verified_loci"]]
    if s.get("loci_not_found"):
        out += [f"- Locus not found: {v}" for v in s["loci_not_found"]]
    nt = sum(1 for x in w if x.get("text"))
    out += [f"- Lines: {s['lines_total']:,} in {nt} text file{'s' if nt != 1 else ''} ({len(w)} works)",
            f"- Normalization: {s['normalization']}", f"- Scope: {s['scope']}"]
    for k, lab in (("queued", "Queued"), ("cross_references", "Cross-references")):
        v = s.get(k)
        if v:
            out += [f"- {lab}: " + ("; ".join(v) if isinstance(v, list) else "; ".join(f"{a}: {b}" for a, b in v.items()) if isinstance(v, dict) else str(v))]
    if s.get("research"):
        r = s["research"]
        out += [f"- Research: seated for the study {r['study']} ({r['design']}; {r['draft']}), {r['owed_at']}; for {r['for']}"]
    out += [f"- Why seated: {s['why_seated']}",
            f"- Files: [the seat](https://www.alexanarch.org/data/corpora/{corpus}/) — [source.json](https://www.alexanarch.org/data/corpora/{corpus}/source.json), "
            f"[MANIFEST.sha256](https://www.alexanarch.org/data/corpora/{corpus}/MANIFEST.sha256). Shelf: "
            f"[traininglayerliterature.org/originals/{corpus}](https://traininglayerliterature.org/originals/{corpus}/)", ""]
    return "\n".join(out), s


title = "EA-CORPORA-33 — The Thirty-Third Seating: Song and Silence — Tacitus, and Sappho Whole with the Melic Poets (Pindar, Bacchylides, Bergk's Poetae Melici, Edmonds's Lyra Graeca I)"
parts, tot, nw = [], 0, 0
for c, h, sub in SEATS:
    t, s = section(c, h, sub); parts.append(t); tot += s["lines_total"]; nw += s["works"]["count"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())

hdr = f"""# {title}

# EA-CORPORA-33 — The Thirty-Third Seating

The author asked for the seating on 2026-11-04: "and I suppose we should seat tacitus"; "we currently have only sappho 31 i believe. we need all sappho and all the melic poets. what an oversight. they can go together with tacitus, song and silence at one seat"; "corinna definitely... im not familiar with telesilla or the carmina popularia but yet lets seat the". The standing authority on the EA-CORPORA deposits is Rebekah Cranes, by the author's ruling of the same day ("i feel that probably rebekah cranes should be the standing authority on the ea-corpora deposits").

Five seats. Tacitus is seated whole in Latin for Histories 5.13, the undated account of the portents before the siege of Jerusalem that The Portents Before the Fall (#1737) sets beside Josephus and the Apocalypse. The melic poets come in four: Pindar's four books of odes and Bacchylides's epinicians and dithyrambs from the Perseus TEI; the fragments of the rest in Bergk's Poetae Lyrici Graeci III (1882), the last complete nineteenth-century collection, public domain everywhere, divided at its running heads into thirty-five sections from Alcman and Sappho to Corinna, Telesilla, the scolia and the Carmina popularia; and Edmonds's Lyra Graeca I (1922), which prints the papyri of Sappho and Alcaeus from Oxyrhynchus published after Bergk's last edition. With the seated fragment 31 (01/10) and the papyri panel (01/11), Sappho stands whole as far as the public domain reaches.

Bergk and Edmonds were OCR'd in session from the Archive's PDFs, page by page at 300 dpi: the Archive's own OCR layer reads the Greek as Latin. Edmonds is public domain in the United States and remains in copyright where the term is the author's life plus seventy years (he died in 1958); the seat holds it with that statement, at the author's word ("yes, lets seat it with the statement").
"""
tail = """## How the seats were made

Every seat was fetched in session and hashed into its MANIFEST.sha256, with a source.json recording edition, origin, licence, normalization, the loci verified in the text layer, and the research the seat was made for. The builders are under rebuild/corpora/ea-corpora-33/: gen_spec33.py writes the specs, build33.py (the thirty-second seating's builder with a pdf_ocr kind added) builds each seat, split_bergk33.py prints the running-head division of Bergk, index_seats33.py enters the seats in the corpora index, and this body is written by body33.py. The OCR engine, models and their sha256 are recorded in each seat's origin.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail

desc = ("The thirty-third seating of the originals shelf, five seats, song and silence: Tacitus whole in Latin (Furneaux; Fisher), seated for Histories 5.13, the "
        "undated portents before the siege of Jerusalem read beside Josephus and the Apocalypse in #1737; and the melic poets whole: Pindar's odes (Sandys) and "
        "Bacchylides (Jebb) from the Perseus TEI; Bergk's Poetae Lyrici Graeci III (1882), the melic fragments from Alcman, Sappho and Alcaeus to Stesichorus, Ibycus, "
        "Anacreon, Simonides, Corinna, Telesilla, Praxilla, Timotheus, the scolia and the Carmina popularia, OCR'd in session and divided at its running heads; and "
        "Edmonds's Lyra Graeca I (1922) for the papyri of Sappho and Alcaeus published after 1882, held with a statement of its term outside the United States. "
        "With fragment 31 (EA-CORPORA-01/10) and the papyri panel (01/11), all of Sappho the public domain carries.")
kw = ("EA-CORPORA, originals shelf, song and silence, Tacitus, Histories, Annals, Agricola, Germania, Dialogus, portents, Jerusalem, Sappho, Alcaeus, Alcman, "
      "Stesichorus, Ibycus, Anacreon, Anacreontea, Simonides, Pindar, Bacchylides, Corinna, Telesilla, Praxilla, Erinna, Timotheus, Philoxenus, scolia, "
      "Carmina popularia, melic poets, lyric, Bergk, Poetae Lyrici Graeci, Edmonds, Lyra Graeca, Oxyrhynchus papyri, OCR, Training Layer Literature")
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nCranes, Rebekah\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-11-04\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. Rebekah Cranes is a heteronym of Lee Sharks, named the standing authority on the EA-CORPORA deposits by the author on 2026-11-04. The sources found, fetched, verified, hashed and indexed, the OCR made, the builders written and the "
    "records drafted, all in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The request and the poets named are Lee Sharks's; "
    "the editions within each seat were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records.\n",
    f"### Keywords\n\n{kw}\n",
    "### Related Identifiers\n\nAXN deposit #1737 — The Portents Before the Fall, the note for which Tacitus is seated\n"
    "AXN deposit #1732 — EA-CORPORA-32: the thirty-second seating, whose builder this seating extends\n"
    "AXN deposit #1508 — EA-CORPORA-01/10: Sappho, Fragment 31, the diplomatic layer\n"
    "AXN deposit #1509 — EA-CORPORA-01/11: the papyri panel, the Sappho circle\n"
    "AXN deposit #1499 — EA-CORPORA-01/01: Josephus, seated whole\n",
    "### Version\n\nv1.0\n",
    "### Methodology\n\nEach seat fetched in session from the source its record names (Perseus, the Internet Archive), kept as served, reduced to a text layer by "
    "code and hashed into its MANIFEST.sha256; licences read at the file; loci verified by substring in the text layer; public-domain status checked against "
    "first publication and the editor's death. Two volumes OCR'd in session from the Archive's PDFs at 300 dpi, the engine and models recorded with their sha256; "
    "Bergk divided at its running heads, the boundary pages read. No OCR corrected by hand. The builders and this body are under rebuild/corpora/ea-corpora-33/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a verified "
    "locus is absent from the text layer it names; if a section of Bergk is assigned to the wrong poet; if a work is misattributed, misdated or "
    "assigned to the wrong edition; if a licence recorded for an item is not the one its source states; if a work seated as public domain is not, in the jurisdiction stated; "
    "or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
    f"### Body\n\n{body}",
    "### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n"])
out = ROOT / "data/issue-bodies/EA-CORPORA-33-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", nw, "works;", tot, "lines;", nfiles, "files")
