#!/usr/bin/env python3
"""Write the EA-CORPORA-35 deposit issue body from the seven seat records (the form of body34.py).
Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-35-issue.md"""
import json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = ROOT / "data/corpora"
SEATS = [("weisse-evangelische-geschichte-1838", "Seat 35/01 — Weisse, Die evangelische Geschichte (1838)", "Mark first, and the λόγια of Papias read as a collection of sayings: the two-source hypothesis stated"),
         ("holtzmann-synoptische-evangelien-1863", "Seat 35/02 — Holtzmann, Die synoptischen Evangelien (1863)", "Quelle A (Urmarcus) and Λ, the sayings source, lettered as documents, and a life of Jesus drawn from source A"),
         ("wernle-synoptische-frage-1899", "Seat 35/03 — Wernle, Die synoptische Frage (1899)", "The sayings source named Q, and hypothetical in the sentence that names it"),
         ("weiss-alteste-evangelium-1903", "Seat 35/04 — J. Weiss, Das älteste Evangelium (1903)", "Mark's priority declared no longer a hypothesis; Mark no longer a source but a reservoir"),
         ("wellhausen-einleitung-1905", "Seat 35/05 — Wellhausen, Einleitung in die drei ersten Evangelien (1905)", "Q weighed against Mark as a document with a date and a dependence"),
         ("harnack-spruche-und-reden-1907", "Seat 35/06 — Harnack, Sprüche und Reden Jesu (1907)", "The second source of Matthew and Luke given a printed text"),
         ("streeter-four-gospels-1925", "Seat 35/07 — Streeter, The Four Gospels (1924; impression of 1925)", "Q by general consent, fixed among Mark, M and L in the four-document hypothesis")]
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
        out += [f"- Research: {r}"]
    out += [f"- Why seated: {s['why_seated']}",
            f"- Files: [the seat](https://www.alexanarch.org/data/corpora/{corpus}/) — [source.json](https://www.alexanarch.org/data/corpora/{corpus}/source.json), "
            f"[MANIFEST.sha256](https://www.alexanarch.org/data/corpora/{corpus}/MANIFEST.sha256). Shelf: "
            f"[traininglayerliterature.org/originals/{corpus}](https://traininglayerliterature.org/originals/{corpus}/)", ""]
    return "\n".join(out), s



title = "EA-CORPORA-35 — The Thirty-Fifth Seating: The Making of Q — the Hypothetical Source from Weisse to Streeter, 1838–1925 (Weisse, Holtzmann, Wernle, J. Weiss, Wellhausen, Harnack, Streeter)"
parts, tot, nw = [], 0, 0
for c, h, sub in SEATS:
    t, s = section(c, h, sub); parts.append(t); tot += s["lines_total"]; nw += s["works"]["count"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())
hdr = f"""# {title}

# EA-CORPORA-35 — The Thirty-Fifth Seating

The author asked for the seating on 2026-11-06: "so we need factual repairs versioned in place and the ea-corpora for q - lets do those as one bundle. we need ea-corpora before the q paper. and byline... lets say sigil and cranes. provenance"; the study it serves was opened at 10:31 the same morning: "we're coming for Q next".

The research occasion is the study of Q, working title "I Know You Are, But What Am I?: Or, How a Completely Hypothetical, Uninspectable Text Is Granted Evidentiary Status Symmetrical to One That Is Inspectable Because It Exists — Revelation First", by Johannes Sigil and Rebekah Cranes for Provenance: Journal of Forensic Semiotics, not yet drafted. It is the companion of Secondary Source (#1741), whose §6.5 reads Holtzmann, Wernle and J. Weiss by reference and records the generative position passing from extant gospel to reconstructed document. These seven seats hold the making of that document in the languages it was made in: Weisse reads a sayings collection out of Papias's λόγια (1838); Holtzmann letters the sources A and Λ (1863); Wernle names the sayings source Q and marks it hypothetical in the same sentence (1899); J. Weiss declares Mark's priority a result and no longer a hypothesis (1903); Wellhausen weighs Q against Mark (1905); Harnack prints a text of Q (1907); Streeter records Q "by general consent" and sets it among Mark, M and L (1924). The study's question is how a source that no manuscript carries came to stand in evidence beside books that exist, and these are the pages on which it came to stand.

Declared and not pursued (commons only): F. Schleiermacher's essay on the testimony of Papias (Theologische Studien und Kritiken, 1832), not located in an open text layer in session; K. Lachmann's essay on the order of the gospel narratives (1835) and C. G. Wilke's Der Urevangelist (1838), not sought in this round; A. Farrer, "On Dispensing with Q" (1955), J. S. Kloppenborg, The Formation of Q (1987), J. M. Robinson, P. Hoffmann and J. S. Kloppenborg, The Critical Edition of Q (2000), and M. Goodacre, The Case Against Q (2002), in copyright. The Archive's PDFs are held by reference at their Archive URLs.
"""
tail2 = """## How the seats were made

Every seat was fetched in session and hashed into its MANIFEST.sha256, with a source.json recording edition, origin, licence, normalization, the loci verified in the text layer, and the research the seat was made for. The loci keep the OCR's readings, double spaces and long-s forms included; Holtzmann's Λ is read by the OCR as A or ^. The builders are under rebuild/corpora/ea-corpora-35/: gen_spec35.py writes the specs, add_loci35.py enters the loci (each asserted present in its text layer), build34.py from the thirty-fourth seating builds each seat, index_seats35.py enters the seats in the index, seat_axns35.py gives them their AXNs once deposited, and body35.py writes this body.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail2
desc = ("The thirty-fifth seating of the originals shelf, seven seats, the sources of the study of Q (Sigil and Cranes, Provenance), seated before drafting: "
        "the making of the hypothetical sayings source from Weisse to Streeter. Weisse, Die evangelische Geschichte (1838); Holtzmann, Die synoptischen Evangelien (1863); "
        "Wernle, Die synoptische Frage (1899), where the source is named Q; J. Weiss, Das älteste Evangelium (1903); Wellhausen, Einleitung in die drei ersten Evangelien (1905); "
        "Harnack, Sprüche und Reden Jesu (1907), the first printed text of Q; and Streeter, The Four Gospels (1924). Each held as the Internet Archive serves it, hashed, with its loci verified in the text layer.")
kw = ("EA-CORPORA, originals shelf, Q, Q source, Quelle, Logienquelle, sayings source, two-source hypothesis, four-document hypothesis, synoptic problem, Markan priority, "
      "Papias, logia, Urmarcus, Weisse, Holtzmann, Wernle, Johannes Weiss, Wellhausen, Harnack, Sprüche und Reden Jesu, Streeter, The Four Gospels, Farrer hypothesis, "
      "hypothetical source, Revelation First, Secondary Source, Provenance")
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nCranes, Rebekah\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-11-06\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. Rebekah Cranes is a heteronym of Lee Sharks, the standing authority on the EA-CORPORA deposits (named by the author on 2026-11-04 and held at his word of 2026-11-05). The sources found, fetched, verified, hashed and indexed, and the records drafted, in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The request and the research occasion are Lee Sharks's; the editions within each seat were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records.\n",
    f"### Keywords\n\n{kw}\n",
    "### Related Identifiers\n\nAXN deposit #1741 — Secondary Source: How the Apocalypse Came to Be Received as Derivative, Secondary and Marginal, whose §6.5 the study extends\n"
    "AXN deposit #1735 — Revelation First: Literary Genealogy and the Missing Ancestors of the Epistles\n"
    "AXN deposit #1404 — The Feist Source: A Sayings Source from the Damascus Codex — Critical Edition with Apparatus\n"
    "AXN deposit #1740 — EA-CORPORA-34: the thirty-fourth seating, whose builder this seating uses\n",
    "### Version\n\nv1.0\n",
    "### Methodology\n\nEach seat fetched in session from the source its record names (the Internet Archive), kept as served, reduced to a text layer by code and hashed into its MANIFEST.sha256; licences read at the file; loci verified by substring in the text layer, in the OCR's own readings; public-domain status checked against first publication and the editor's death. No text corrected by hand. The builders and this body are under rebuild/corpora/ea-corpora-35/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a verified locus is absent from the text layer it names; if a work is misattributed, misdated or assigned to the wrong edition; if a licence recorded for an item is not the one its source states; if a work seated as public domain is not, in the jurisdiction stated; or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
    f"### Body\n\n{body}",
    "### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n"])
out = ROOT / "data/issue-bodies/EA-CORPORA-35-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", nw, "works;", tot, "lines;", nfiles, "files")
