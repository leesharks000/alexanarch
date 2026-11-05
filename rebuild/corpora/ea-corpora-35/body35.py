#!/usr/bin/env python3
"""Write the EA-CORPORA-35 deposit issue body from the four seat records (the form of body34.py).
Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-35-issue.md"""
import json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = ROOT / "data/corpora"
SEATS = [("scrivener-plain-introduction-1894", "Seat 35/01 — Scrivener, A Plain Introduction, 4th ed. (1894)", "The manuscripts of the Apocalypse and the printed editions"),
         ("delitzsch-handschriftliche-funde-1861", "Seat 35/02 — Delitzsch, Handschriftliche Funde (1861)", "Reuchlin's codex, the one exemplar of the first printed Apocalypse"),
         ("tregelles-printed-text-1854", "Seat 35/03 — Tregelles, An Account of the Printed Text (1854)", "The succession from Erasmus to the received text"),
         ("erasmus-novum-instrumentum-1516", "Seat 35/04 — Erasmus, Novum Instrumentum (1516)", "The first printed Greek New Testament, its Apocalypse; the scan is the witness")]
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



title = "EA-CORPORA-35 — The Thirty-Fifth Seating: Secondary Source — the Carriage of the Apocalypse, Its Manuscripts and Its Succession into Print (Scrivener, Delitzsch, Tregelles, Erasmus 1516)"
parts, tot, nw = [], 0, 0
for c, h, sub in SEATS:
    t, s = section(c, h, sub); parts.append(t); tot += s["lines_total"]; nw += s["works"]["count"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())
hdr = f"""# {title}

# EA-CORPORA-35 — The Thirty-Fifth Seating

The author asked for the seating on 2026-11-05: "we should also be tracking material manuscript transmission and succession, that seems particularly important with revelation and less-often and -critically studied than pure reception"

The research occasion is Secondary Source (design v0.4, not deposited), which now counts the book's carriage apart from its order, standing and derivation: what materially carries the Apocalypse and from what each carrier descends. These four seats hold the account of its manuscripts and of its succession into print. Erasmus made the Apocalypse of 1516 from one manuscript lent by Reuchlin, in which text and commentary were mixed; its last verses were wanting, and he supplied them from the Latin. Delitzsch found that manuscript again in 1861; Tregelles and Scrivener trace what it became in the printed text. Erasmus's own 1516 printing is seated as the witness.

Declared and not pursued: Hoskier, Concerning the Text of the Apocalypse (1929), its term unclear.
"""
tail2 = """## How the seats were made

Every seat was fetched in session and hashed into its MANIFEST.sha256, with a source.json recording edition, origin, licence, normalization, the loci verified in the text layer, and the research the seat was made for. The builders are under rebuild/corpora/ea-corpora-35/: gen_spec35.py writes the specs, build35.py builds each seat, index_seats35.py enters the seats in the index, and body35.py writes this body.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail2
desc = ("The thirty-fifth seating of the originals shelf, four seats, the carriage of the Apocalypse for Secondary Source: Scrivener's Plain Introduction (1894) for "
        "the manuscripts and the printed editions; Delitzsch's Handschriftliche Funde (1861), on Reuchlin's codex, the one exemplar of Erasmus's Apocalypse; Tregelles's "
        "Account of the Printed Text (1854), on the succession into the received text and the last six verses supplied from the Latin; and Erasmus's Novum Instrumentum of 1516.")
kw = ("EA-CORPORA, originals shelf, Secondary Source, Apocalypse, Revelation, manuscripts, transmission, succession, carriage, Andreas of Caesarea, Reuchlin, Erasmus, Novum Instrumentum, Textus Receptus, Delitzsch, Tregelles, Scrivener, printed text")
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nCranes, Rebekah\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-11-05\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. Rebekah Cranes is a heteronym of Lee Sharks, the standing authority on the EA-CORPORA deposits (named by the author on 2026-11-04 and held at his word of 2026-11-05). The sources found, fetched, verified, hashed and indexed, and the records drafted, in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The request and the research occasion are Lee Sharks's; the editions within each seat were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records.\n",
    f"### Keywords\n\n{kw}\n",
    "### Related Identifiers\n\nAXN deposit #1735 — Revelation First: Literary Genealogy and the Missing Ancestors of the Epistles, whose dating record and Muratorian premise the study takes as given\n"
    "AXN deposit #1420 — The Argument of the Bookshelf, whose mechanism the study tests\n"
    "AXN deposit #1740 — EA-CORPORA-34: the thirty-fourth seating, the first sources of Secondary Source\n"
    "AXN deposit #1733 — Legitimately Many, the companion reception study\n",
    "### Version\n\nv1.0\n",
    "### Methodology\n\nEach seat fetched in session from the source its record names (the Internet Archive), kept as served, reduced to a text layer by code and hashed into its MANIFEST.sha256; licences read at the file; loci verified by substring in the text layer; public-domain status checked against first publication and the editor's death. No text corrected by hand. The builders and this body are under rebuild/corpora/ea-corpora-35/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a verified locus is absent from the text layer it names; if a work is misattributed, misdated or assigned to the wrong edition; if a licence recorded for an item is not the one its source states; if a work seated as public domain is not, in the jurisdiction stated; or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
    f"### Body\n\n{body}",
    "### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n"])
out = ROOT / "data/issue-bodies/EA-CORPORA-35-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", nw, "works;", tot, "lines;", nfiles, "files")
