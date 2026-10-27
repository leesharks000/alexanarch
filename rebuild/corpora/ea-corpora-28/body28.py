#!/usr/bin/env python3
"""Write the EA-CORPORA-28 deposit issue body (a DRAFT until minted) from the four seat records.
Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-28-issue.md"""
import json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = ROOT / "data/corpora"
SEATS = [("hypatia", "Seat 28/01 — Hypatia of Alexandria", "Lost works, and the witnesses in which her work and her life survive"),
         ("philip-k-dick", "Seat 28/02 — Philip K. Dick", "The novels, the late trilogy and the Exegesis; thirteen stories already open"),
         ("allen-ginsberg", "Seat 28/03 — Allen Ginsberg", "Howl, Kaddish and the books of poems to Death & Fame"),
         ("anne-carson", "Seat 28/04 — Anne Carson", "The books from Eros the Bittersweet to The Gender of Sound, and the translations from the Greek"),
         ("tao-lin", "Seat 28/05 — Tao Lin", "The books, and the mandalas"),
         ("paul-klee", "Seat 28/06 — Paul Klee", "The pictures and the writings, held back by their number and by the rights in their photographs")]
lic = lambda l: l["payload"] if isinstance(l, dict) else str(l)


def section(corpus, heading, sub):
    s = json.loads((A / corpus / "source.json").read_text(encoding="utf-8"))
    w = s["works"]["list"]
    out = [f"## {heading}", "", f"*{sub}*", ""]
    if len(w) > 12:
        cnt = Counter(x.get("class", "") for x in w)
        out += ["- Works by class: " + "; ".join(f"{k} {v}" for k, v in cnt.items())]
    out += (["- Works:"] + [f"  - {x['work']}" for x in w]) if w else ["- Works: none held; the seat is a declared absence"]
    out += [f"- Licence: {lic(s['license'])}"] + [f"- Verified locus: {v}" for v in s["verified_loci"]]
    if s.get("loci_not_found"):
        out += [f"- Locus not found: {v}" for v in s["loci_not_found"]]
    nt = sum(1 for x in w if x.get("text"))
    out += [f"- Lines: {s['lines_total']:,} in {nt} text file{'s' if nt != 1 else ''} ({len(w)} works)",
            f"- Normalization: {s['normalization']}", f"- Scope: {s['scope']}"]
    if s.get("contested"):
        out += [f"- Contested: {s['contested']}"]
    out += [f"- Why seated: {s['why_seated']}",
            f"- Files: [the seat](https://www.alexanarch.org/data/corpora/{corpus}/) — [source.json](https://www.alexanarch.org/data/corpora/{corpus}/source.json), "
            f"[MANIFEST.sha256](https://www.alexanarch.org/data/corpora/{corpus}/MANIFEST.sha256). Shelf: "
            f"[traininglayerliterature.org/originals/{corpus}](https://traininglayerliterature.org/originals/{corpus}/)", ""]
    return "\n".join(out), s


title = ("EA-CORPORA-28 — The Twenty-Eighth Seating, the Wanted: Hypatia, Philip K. Dick, Allen Ginsberg, Anne Carson, Tao Lin with the Mandalas, and Paul Klee, as Declared Absences")
parts, tot, nw = [], 0, 0
for c, h, sub in SEATS:
    t, s = section(c, h, sub); parts.append(t); tot += s["lines_total"]; nw += s["works"]["count"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())

hdr = f"""# {title}

# EA-CORPORA-28 — The Twenty-Eighth Seating

MANUS, 27 October 2026, after the twenty-seventh seating entered Deleuze and Guattari as a declared absence: "and a declared absence/ wanted seating: hypatia, d & g, pkd, allen ginsberg, anne carson, and tao lin - including the mandalas. and paul klee. too many files and too many image copyright landmines."

The seating holds no text. It is the shelf's list of the wanted, each seat a declaration of what the shelf would hold, who holds it, why it is not held, and when or how it opens. The absences are of three kinds. Hypatia's works are lost, or survive inside other authors' texts, and what can be seated are the witnesses. Philip K. Dick, Allen Ginsberg, Anne Carson and Tao Lin are in copyright, two of them living. Paul Klee's work is in the public domain where he lived and died, and is held back by its number and by the rights claimed in its photographs. Deleuze and Guattari, named in the request, were declared at 27/07 (#1712) and are not seated twice.
"""
tail = f"""## What opens, and when

- Hypatia: no term; the witnesses are open and QUEUED (28/01).
- Philip K. Dick: thirteen stories open now, their copyrights not renewed; the works published before 1978 ninety-five years after publication; the rest on 1 January 2053 (28/02).
- Allen Ginsberg: the works published before 1978 ninety-five years after publication; the rest on 1 January 2068 (28/03).
- Anne Carson and Tao Lin: seventy years after each author's death (28/04, 28/05).
- Paul Klee: open in Switzerland and the European Union since 1 January 2011; the shelf waits on images whose licence is verified at the file (28/06).
- Deleuze and Guattari: 2063 and 2066 in France, 2049 to 2088 in the United States (27/07, #1712).

## How the seats were made

Each seat holds a declaration written in session, declared/absence.json and declared/absence.md, hashed into its MANIFEST.sha256, and a source.json; no text of the works named. Bibliographies were checked against current reference sources on the day (for Carson and Lin, the bibliographies published with them; for Hypatia, the attributions as the Suda and Theon's heading give them; for Dick, the Project Gutenberg catalogue of his open stories). Terms follow the rules stated in each seat; they are not legal advice. {len(SEATS)} seats; {nfiles} files.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail

desc = ("Six seats on the originals shelf that hold no text: the wanted, each a declared absence naming the works, their rights, "
        "why they are not held and when or how they open. Hypatia of Alexandria, whose works are lost or survive inside other texts, with "
        "the witnesses wanted; Philip K. Dick, the novels, the late trilogy and the Exegesis, with thirteen stories already open; Allen "
        "Ginsberg, Howl to Death & Fame; Anne Carson, Nobel laureate of 2026, from Eros the Bittersweet to The Gender of Sound; Tao Lin, the "
        "books and the mandalas; Paul Klee, in the public domain and held back, in the operator's words, by \"too many files and too many "
        "image copyright landmines\". Deleuze and Guattari, declared at 27/07, are referred to and not seated twice.")

kw = ("declared absence, wanted, originals shelf, EA-CORPORA, copyright, public domain, Hypatia, Alexandria, Theon, Synesius, Diophantus, "
      "Almagest, Philip K. Dick, VALIS, Exegesis, The Man in the High Castle, Allen Ginsberg, Howl, Kaddish, City Lights, Anne Carson, "
      "Nobel Prize in Literature 2026, If Not Winter, Autobiography of Red, Sappho, Stesichorus, Tao Lin, mandalas, Taipei, Leave Society, "
      "Paul Klee, Pädagogisches Skizzenbuch, Bauhaus, image rights, Deleuze and Guattari, Training Layer Literature")
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nSharks, Lee\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-10-27\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. The declarations written, the bibliographies checked against reference sources "
    "on the day, the terms computed, hashed and indexed, all in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. "
    "The request, the six names and the reason given for Klee are Lee Sharks's; the works listed and the witnesses wanted were drawn up in "
    "session and are stated per seat. CC-BY-4.0 applies to this record and the seat records.\n",
    f"### Keywords\n\n{kw}\n",
    "### Related Identifiers\n\nAXN deposit #1712 — EA-CORPORA-27: the seating whose declared absence (27/07) this one follows and refers to\n"
    "AXN deposit #1711 — EA-MPAI-ORIGINALS-01 v1.1: the inspection packet of the originals library\n"
    "AXN deposit #1508 — EA-CORPORA-01/10: Sappho, fragment 31, beside which Carson is wanted\n",
    "### Version\n\nv1.0\n",
    "### Methodology\n\nEach seat's declaration written in session and hashed into its MANIFEST.sha256; the bibliographies checked on the day against "
    "reference sources (published bibliographies, the Project Gutenberg catalogue); terms computed from the rules each seat states (the United "
    "States: ninety-five years from publication for works published before 1978, renewal required before 1964; seventy years from the author's "
    "death after 1978 and in Switzerland, the European Union and Canada). No text of a work named is held. The builder and this body are under "
    "rebuild/corpora/ea-corpora-28/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a work "
    "it names is misdated or assigned to the wrong first publisher; if a date of opening misstates the term it follows; if a work declared "
    "absent is in fact open under a licence verified at the file (it is then to be seated); or if the four surfaces (seat, index, deposit, "
    "shelf) disagree.\n",
    f"### Body\n\n{body}"])
out = ROOT / "data/issue-bodies/EA-CORPORA-28-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", nw, "works;", tot, "lines;", nfiles, "files")
