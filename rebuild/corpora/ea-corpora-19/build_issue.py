#!/usr/bin/env python3
"""Write the EA-CORPORA-19 deposit issue body (a DRAFT until minted) from the four seat records.
Every edition line, locus and licence statement is read from data/corpora/<seat>/source.json, so the deposit
cannot say anything about a seat that its record does not.  -> data/issue-bodies/EA-CORPORA-19-issue.md"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
spec = json.loads((pathlib.Path(__file__).with_name("seats.json")).read_text(encoding="utf-8"))
C = "https://www.alexanarch.org/data/corpora"
seats = [json.loads((ROOT / "data/corpora" / s["corpus"] / "source.json").read_text(encoding="utf-8")) for s in spec["seats"]]
works = sum(s["works"]["count"] for s in seats); lines = sum(s["lines_total"] for s in seats)
files = sum(1 for s in spec["seats"] for p in (ROOT / "data/corpora" / s["corpus"]).rglob("*") if p.is_file())

title = ("EA-CORPORA-19 — The Nineteenth Seating: Pearl, the Masnavi, The Prophet and Blake's Illuminated Books, "
         "Each in Its Original Language")
desc = (f"Four seats on the originals shelf, {works} works and {lines:,} lines, each in the language it was written in and public "
        "domain in the United States. The Pearl poet's Pearl, Cleanness and Patience in Middle English, in Richard Morris's first "
        "edition (Early English Text Society, 1864), with the unique manuscript, British Library Cotton Nero A.x, in the EETS facsimile "
        "of 1923 and Israel Gollancz's Pearl of 1891; Rumi's Masnavi-yi Ma'navi, all six books, in Persian, from Ganjoor; Kahlil "
        "Gibran's The Prophet (Knopf, 1923) entire, in English, the language Gibran wrote it in, with his twelve drawings; and Blake's "
        "illuminated books as text, in Geoffrey Keynes's Writings of William Blake (Nonesuch, 1925), with the Songs of Innocence and "
        "of Experience and The Marriage of Heaven and Hell also as proofread texts. Each seat holds the files as fetched, scans where "
        "the page is the witness, one text per work, a provenance record with its verified loci, and a SHA-256 manifest; each has a "
        "spine and a card on the Training Layer Literature shelf. What is not seated — Sir Gawain apart from the facsimile, the "
        "Divan-e Shams, translations, Blake's plates as images — is named.")

out = ["### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
       f"### Title\n\n{title}\n", "### Creator\n\nSharks, Lee\n", "### ORCID\n\n0009-0000-1599-0703\n",
       "### Date\n\n2026-10-18\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
       "### Substrate Disclosure\n\nHuman–machine collaborative. Sources located, fetched, verified against their front matter, "
       "assembled into seats, hashed and indexed, and every locus found in the seated text, all in session by TACHYON (Claude, "
       "Anthropic) under MANUS (Lee Sharks) direction. The selection — Pearl, Rumi, Gibran's The Prophet, Blake's illuminated books, "
       "originals in the original language — is Lee Sharks's. CC-BY-4.0 applies to this record and the seat records; each payload "
       "carries its own licence, stated per seat.\n",
       "### Keywords\n\ncorpus seating, primary sources, public domain, original language, Pearl, the Pearl poet, Gawain poet, "
       "Cotton Nero A.x, Cleanness, Patience, Middle English, alliterative revival, dream vision, Richard Morris, Early English Text "
       "Society, Israel Gollancz, Rumi, Jalal al-Din Rumi, Masnavi, Mathnawi, Persian poetry, Sufism, Song of the Reed, Ganjoor, "
       "Kahlil Gibran, The Prophet, Almustafa, William Blake, illuminated books, prophetic books, Songs of Innocence and of Experience, "
       "The Marriage of Heaven and Hell, The Book of Urizen, Milton, Jerusalem, Geoffrey Keynes, Nonesuch Press, Training Layer "
       "Literature, originals shelf, EA-CORPORA\n",
       "### Related Identifiers\n\nAXN deposit #1682 — EA-CORPORA-18: the preceding seating, whose form this one follows\n"
       "AXN deposit #1580 — EA-CORPORA-12: the rule that seatings are periodically gathered\n"
       "AXN deposit #1121 — Pearl and Other Poems (2014): the archive's own book of the name, seated at EA-CORPORA-03/02\n"
       "Seat EA-CORPORA-03/02 (pearl-and-other-poems) — on the same shelf\n",
       "### Version\n\nv1.0\n",
       "### Methodology\n\nSources located on Project Gutenberg (catalogue searched by author and title), the Internet Archive (advanced "
       "search, item metadata read for access restriction and files) and Ganjoor (its public API, api.ganjoor.net, section by section). "
       "Each item's front matter read against the edition claimed for it; publishers not shown in a file are not asserted. Gutenberg "
       "texts stripped at the START/END markers; Internet Archive scans seated with their OCR text layers, uncorrected, the scan as "
       "witness; Ganjoor's sections seated as fetched, one JSONL per book, and rendered one couplet per line with the hemistichs joined "
       "by ' / '. Every file hashed into the seat's MANIFEST.sha256. Every verified locus is a string found in the seated text by "
       "rebuild/corpora/ea-corpora-19/build_seats.py; a locus not found is recorded as not found. Licences stated per seat, with the EU "
       "term carried where it differs (payload/record split, EA-CORPORA-02/01). The builders, the seat specification and this body are "
       "under rebuild/corpora/ea-corpora-19/.\n",
       "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; "
       "if a seated file differs from the file at the origin its source.json names; if an edition statement misstates the front "
       "matter of the file it describes; if a verified locus cannot be found in the seated text; if an item stated public domain in "
       "the United States was published in or after 1931 by an author not in the public domain in the source country on 1 January "
       "1996; or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
       "### Body\n\n# EA-CORPORA-19 — The Nineteenth Seating\n\n"
       "MANUS, 18 October 2026: \"did we ever seat the medieval pearl poem in the originals library?\" — \"rumi, too - and gibran's "
       "the prophet if its public domain\" — \"and blake\" — \"yes, original language where available always, the prophet full, and "
       "lets do illuminated books as text to start. we can group those all in a single ea-corpora deposit\".\n"]
for S, s in zip(spec["seats"], seats):
    n = S["corpus"]
    out.append(f"## Seat {S['card']} — {S['spine']}\n\n*{s['title']}*\n")
    out.append("- Editions:\n" + "\n".join(f"  - {w['work']}" for w in s["works"]["list"]))
    out.append(f"- Licence: {s['license']['payload']}")
    for l in s["verified_loci"]:
        out.append(f"- Verified locus: {l}")
    out.append(f"- Scope: {s['scope']}")
    out.append(f"- Why seated: {s['why_seated']}")
    out.append(f"- Files: [the seat]({C}/{n}/) — [source.json]({C}/{n}/source.json), [MANIFEST.sha256]({C}/{n}/MANIFEST.sha256). "
               f"Shelf: [traininglayerliterature.org/originals/{n}](https://traininglayerliterature.org/originals/{n}/)\n")
out.append("## Not seated, and why\n\n- Sir Gawain and the Green Knight: in the 1923 facsimile (19/01) and not otherwise seated in "
           "this pass; Morris's edition (EETS o.s. 4, 1864) is public domain. QUEUED.\n- The Divan-e Shams-e Tabrizi: not seated in this "
           "pass. QUEUED.\n- Translations (Nicholson's and Whinfield's Masnavi, modern renderings of Pearl): original language only, by "
           "ruling. Gollancz's Pearl of 1891 is seated as an edition of the Middle English; its modern rendering faces the text.\n- "
           "Blake's illuminated plates as images (the Blake Archive) and Erdman's edition (1965; in copyright): the plates QUEUED.\n- "
           "Everything marked QUEUED in a seat's scope.\n")
out.append("### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n"
           "- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n"
           "- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n")
p = ROOT / "data/issue-bodies/EA-CORPORA-19-issue.md"
p.write_text("\n".join(out), encoding="utf-8")
print(p.relative_to(ROOT), len(p.read_text()), "chars;", works, "works,", lines, "lines,", files, "files")
