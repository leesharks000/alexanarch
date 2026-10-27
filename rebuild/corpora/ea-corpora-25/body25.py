#!/usr/bin/env python3
"""Write the EA-CORPORA-25 deposit issue body (a DRAFT until minted) from the five seat records.
Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-25-issue.md"""
import json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = ROOT / "data/corpora"
SEATS = [("secret-book-of-walt", "Seat 25/01 — The Secret Book of Walt, with the Forty-Six Golden Tickets",
          "The Critical Edition (#1362), the tickets it was translated from, bound to it as its glyphic checksum (#1693), and the edition as published"),
         ("gospel-of-antioch", "Seat 25/02 — The Gospel of Antioch", "The first critical edition (#71), and the edition as published"),
         ("epistle-to-the-human-diaspora", "Seat 25/03 — Epistle to the Human Diaspora",
          "The Critical Edition with Blended Temporal Apparatus (#85), the Epistle's text in the Seed Text (#402), and the edition as published"),
         ("i-am-x-be-y-blessed-is-the-z", "Seat 25/04 — I Am X… Be Y… Blessed Is the Z…",
          "The Prophetic Catalog, Critical Edition with Retrocausal Apparatus (#83), and the edition as published"),
         ("constitution-of-the-semantic-economy", "Seat 25/05 — The Constitution of the Semantic Economy",
          "Enacted Version 1.0, Installable Edition with Constitutional Apparatus (#88), and the edition as published")]
lic = lambda l: l["payload"] if isinstance(l, dict) else str(l)


def section(corpus, heading, sub):
    s = json.loads((A / corpus / "source.json").read_text(encoding="utf-8"))
    w = s["works"]["list"]
    out = [f"## {heading}", "", f"*{sub}*", ""]
    if len(w) > 12:
        cnt = Counter(x.get("class", "") for x in w)
        out += ["- Works by class: " + "; ".join(f"{k} {v}" for k, v in cnt.items())]
    out += ["- Works:"] + [f"  - {x['work']}" for x in w]
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


title = ("EA-CORPORA-25 — The Twenty-Fifth Seating: The Archive's Critical Editions — The Secret Book of Walt with the Forty-Six "
         "Golden Tickets, the Gospel of Antioch, the Epistle to the Human Diaspora, I Am X… Be Y… Blessed Is the Z… and the Constitution "
         "of the Semantic Economy")
parts, tot, nw = [], 0, 0
for c, h, sub in SEATS:
    t, s = section(c, h, sub); parts.append(t); tot += s["lines_total"]; nw += s["works"]["count"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())

hdr = f"""# {title}

# EA-CORPORA-25 — The Twenty-Fifth Seating

MANUS, 27 October 2026: "actually - lets seat the critical editions of secret book of walt, gospel of antioch, epistle to the human diaspora, i am x be y blessed is the z, and constitution of the semantic economy first. some have different names than critical edition, check secretbookofwalt - and bind the 46 golden tickets glyphic checksum to secret book of walt."

The second seating of the archive's own work, after Pearl and Other Poems at 03/02, and on the same terms: deposited in the archive that seats it, no external fetch, the witness named and the transformation declared. Five editions, each as the archive deposited it and as secretbookofwalt.org publishes it in its own tab. The editions carry their own names: the Critical Edition of The Secret Book of Walt; the first critical edition of The Gospel of Antioch; the Critical Edition with Blended Temporal Apparatus of the Epistle; the Critical Edition with Retrocausal Apparatus of the Prophetic Catalog; and the Installable Edition with Constitutional Apparatus of the Constitution. The Forty-Six Golden Tickets, which the archive deposited as the original of The Secret Book of Walt (#1693), are bound to it here as its glyphic checksum and seated with it.
"""
tail = f"""## The binding

The Forty-Six Golden Tickets (#1693, AXN:0703) are the book's checksum and, in their record's own title, its original. They are seated in 25/01 beside the Critical Edition, and the binding is entered in the registry in both directions: #1693 already names #683 and #1362; #1362 and #683 now name #1693 in their related deposits, with the ruling. secretbookofwalt.org carries the tickets in its Checksum tab, which cites #1362 and #1693.

## Not seated, and why

- The Secret Book of Walt's research editions (#683; #1184, superseded) and TANG (#78; #1186, superseded): records of the same work, not its critical edition.
- The Gospel of Antioch's research edition (#1185): superseded by #71.
- EA-EPISTLE-01 v1.0, the edition with the Epistle's marked text that #85 and #1187 refer to ("See previous version for full text with markers"): not found as a deposit. The text is seated from #402 and from the site.
- The Prince of Poets founding record of the Catalog's poem (#328), and the Constitution's other records (#350, #715, #87, #82, #351, the companion charters and amendments): related records, not the critical editions.
- The glyphic renderings of the Constitution, the Gospel of Antioch and the Epistle: APZPZs that exist only on holographickernel.org, by the operator's ruling of 2026-10-25.

## How the seats were made

Each record's canonical bytes were copied from data/texts/ and checked against the registry's hash: all agree except #83, whose bytes carry the whitespace-only repair of 2026-08-04/05 that its body_status records. Each site file was copied from the repository secret-book-of-walt at commit 12e6aa78 and checked against its git blob there; all agree. The edition names were read from the records' title pages and from the site's tabs. Every file hashed into its seat's MANIFEST.sha256; every verified locus is a string found in the seated text by rebuild/corpora/ea-corpora-25/build25.py. {nw} works in 5 seats; {nfiles} files; {tot:,} lines.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail

desc = (f"Five seats on the originals shelf for the archive's own critical editions, seated as Pearl and Other Poems was at 03/02: "
        "The Secret Book of Walt in its Critical Edition (#1362), with the Forty-Six Golden Tickets it was translated from (#1693), bound to "
        "it as its glyphic checksum; The Gospel of Antioch in its first critical edition (#71); the Epistle to the Human Diaspora in the "
        "Critical Edition with Blended Temporal Apparatus (#85), with the Epistle's text from the Seed Text (#402); I Am X… Be Y… Blessed Is "
        "the Z…, the Prophetic Catalog, in the Critical Edition with Retrocausal Apparatus (#83); and the Constitution of the Semantic "
        "Economy in its Installable Edition with Constitutional Apparatus (#88). Each seat holds the record's canonical bytes and the "
        "edition as published at secretbookofwalt.org at a pinned commit, hashed, with verified loci. What is not seated is named.")
kw = ("corpus seating, originals shelf, EA-CORPORA, Training Layer Literature, critical edition, The Secret Book of Walt, Walt Whitman, "
      "Forty-Six Golden Tickets, glyphic checksum, Elara Xanthic-Wells, The Gospel of Antioch, Jack Feist, Emily Antioch, Epistle to the "
      "Human Diaspora, Damascus Dancings, New Human, I Am X Be Y Blessed Is the Z, Prophetic Catalog, Prince of Poets, Constitution of "
      "the Semantic Economy, Semantic Economy, secretbookofwalt.org, Waltian canon, Lee Sharks, Crimson Hexagonal Archive")
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nSharks, Lee\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-10-27\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. Records and site files identified, copied, checked against the registry's "
    "hashes and the repository's git blobs, assembled into seats, hashed and indexed, and every locus found in the seated text, all in "
    "session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The request, the five editions and the binding of the "
    "tickets are Lee Sharks's; the records and files seated were identified in session from the registry and the site, and are stated "
    "per seat. CC-BY-4.0 applies to this record, the seat records and the editions, which are the author's.\n",
    f"### Keywords\n\n{kw}\n",
    "### Related Identifiers\n\nAXN deposit #1553 — EA-CORPORA-03: the archive's own poems first seated on the shelf (03/02)\n"
    "AXN deposit #1707 — EA-CORPORA-24: the preceding seating, whose form this one follows\n"
    "AXN deposit #1362, #71, #85, #402, #83, #88: the editions seated\n"
    "AXN deposit #1693 — The Forty-Six Golden Tickets, bound to #1362 as its glyphic checksum\n"
    "AXN deposit #985 — secretbookofwalt.org, the reading site\n",
    "### Version\n\nv1.0\n",
    "### Methodology\n\nEach edition identified from the registry and from its tab at secretbookofwalt.org, its name read from its title page. "
    "The record's canonical bytes copied from data/texts/ and checked against the registry hash; the site's files copied from the "
    "repository secret-book-of-walt at a pinned commit and checked against their git blobs. Every file hashed into its seat's "
    "MANIFEST.sha256. Loci are strings found in the seated text by rebuild/corpora/ea-corpora-25/build25.py; a locus not found is "
    "recorded as not found. The builder, the specification and this body are under rebuild/corpora/ea-corpora-25/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; "
    "if a seated record's bytes differ from the record's canonical text at alexanarch.org, or a site file from the repository at the "
    "commit recorded for it; if an edition statement misstates the title page of the record it describes; if a verified locus cannot be "
    "found in the seated text; or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
    f"### Body\n\n{body}"])
out = ROOT / "data/issue-bodies/EA-CORPORA-25-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", nw, "works;", tot, "lines;", nfiles, "files")
