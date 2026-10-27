#!/usr/bin/env python3
"""Write the EA-CORPORA-23 deposit issue body (a DRAFT until minted) from the seat record.
Edition lines, loci, licence and scope are read from data/corpora/hadith/source.json, so the deposit
cannot say anything about the seat that its record does not.  -> data/issue-bodies/EA-CORPORA-23-issue.md"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
C = "https://www.alexanarch.org/data/corpora/hadith"
s = json.loads((ROOT / "data/corpora/hadith/source.json").read_text(encoding="utf-8"))
works = s["works"]["list"]; lines = s["lines_total"]
nfiles = sum(1 for p in (ROOT / "data/corpora/hadith").rglob("*") if p.is_file())
rel = s["origin"]["release"]

title = ("EA-CORPORA-23 — The Twenty-Third Seating: The Hadith in Arabic, the Nine Books, the Four Books "
         "of the Imami Tradition and al-Nawawi's Forty")
desc = (f"One seat on the originals shelf, {len(works)} collections and {lines:,} lines of Arabic: the hadith, the reports of what "
        "the Prophet Muhammad said and did, which with the Qur'an (seated since EA-CORPORA-02/08) are the sources of Islamic law and "
        "practice. The nine books Sunni scholarship calls al-Kutub al-Tis'a (the Muwatta of Malik, the Musnad of Ahmad ibn Hanbal, "
        "the Sunan of al-Darimi, the Sahihs of al-Bukhari and Muslim, and the Sunans of Ibn Majah, Abu Dawud, al-Tirmidhi and "
        "al-Nasa'i); the four books of the Imami Shi'i tradition, al-Kutub al-Arba'a (al-Kulayni's al-Kafi, Ibn Babawayh's Man la "
        "yahduruhu al-faqih, al-Tusi's Tahdhib al-ahkam and al-Istibsar); and al-Nawawi's Forty. Each is the version the Open "
        "Islamicate Texts Initiative (OpenITI) marks primary, pinned by commit, checked against its git blob, with the printed edition "
        "its header names and its OpenITI version record. The texts are OpenITI's, under CC BY-NC-SA 4.0. What is not seated (the "
        "Sunan al-Kubra, the Sahihs of Ibn Khuzayma and Ibn Hibban, the Mustadrak, al-Bayhaqi, the Zaydi and Ibadi musnads, "
        "translations) is named.")

body = [f"# {title}", "", "# EA-CORPORA-23 — The Twenty-Third Seating", "",
        "MANUS, 27 October 2026: \"lets seat the hadith\" — \"i mean the hadith supplementary to the quran\" — \"as ea-corpora\".", "",
        "The Qur'an has been on the shelf since the second seating (EA-CORPORA-02/08, the Tanzil Uthmani text, #1531). This seating "
        "places beside it the hadith, in Arabic, as each of the two largest traditions defines its canon: the Sunni nine books and the "
        "Imami Shi'i four books, with al-Nawawi's Forty, the short collection most read and memorized.", "",
        "## Seat 23/01 — The Hadith", "", "*al-Kutub al-Tis'a, al-Kutub al-Arba'a and al-Arba'un al-Nawawiyya, in Arabic, from OpenITI*", ""]
for cls, slugs in s["classes"].items():
    body.append(f"### {cls}")
    body.append("")
    for w in works:
        if w["slug"] in slugs:
            body.append(f"- {w['work']}. [The text]({C}/{w['text']}), {w['lines']:,} lines; [version record]({C}/{w['originals'][1]}).")
    body.append("")
body += [f"- Licence: {s['license']['payload']} The record: {s['license']['record']}",
         f"- The release's licence, verbatim: {rel['licence_statement']}",
         f"- OpenITI on copyright, verbatim: {rel['copyright_statement']}",
         f"- Citation: {rel['citation']}"]
body += [f"- Verified locus: {v}" for v in s["verified_loci"]]
body += [f"- Lines: {lines:,} in {len(works)} text files; {nfiles} files in the seat",
         f"- Normalization: {s['normalization']}",
         f"- Scope: {s['scope']}",
         f"- Witness: {s['witness_note']}",
         f"- Why seated: {s['why_seated']}",
         f"- Files: [the seat]({C}/) — [source.json]({C}/source.json), [MANIFEST.sha256]({C}/MANIFEST.sha256). Shelf: "
         "[traininglayerliterature.org/originals/hadith](https://traininglayerliterature.org/originals/hadith/)", "",
         "## Not seated, and why", "",
         "- Al-Nasa'i's al-Sunan al-Kubra, the Sahihs of Ibn Khuzayma and Ibn Hibban, al-Hakim's al-Mustadrak, al-Bayhaqi's al-Sunan "
         "al-Kubra, the Musnad of Zayd ibn Ali and the Musnad of al-Rabi' ibn Habib: in OpenITI, not seated in this pass. QUEUED.",
         "- The other versions OpenITI holds of each seated work (other digital libraries' typings of the same or other printed "
         "editions): one primary version per work is seated. QUEUED as a comparative witness programme.",
         "- Translations: not seated, by the shelf's rule.",
         "- Manuscripts: none in an open, licensed digital edition was found in this pass.",
         "- The hadith dataset fawazahmed0/hadith-api (Unlicense): its Arabic editions name no printed edition, so it is not taken "
         "as witness.", "",
         "## How the seat was made", "",
         "The works were found in OpenITI's text repositories on GitHub (blob-less clones of 0200AH, 0250AH, 0275AH, 0300AH, 0325AH, "
         "0350AH, 0400AH, 0475AH and 0700AH, each at the commit recorded in source.json). For each work the version marked "
         "PRIMARY_VERSION in its OpenITI version record was chosen. Each text and its version record were fetched from "
         "raw.githubusercontent.com at the pinned commit and checked against the git blob id the clone lists for it; none differed. "
         "The edition statements are read from each file's own #META# header and its version record, and nothing is asserted beyond "
         "them: where a header names no editor, publisher or year, none is given. The licence was read on the KITAB project's "
         "documentation and on the Zenodo release record. The texts are seated as published, in OpenITI mARkdown, and each is its own "
         "text layer. Every file is hashed into the seat's MANIFEST.sha256; every verified locus is a string found in the seated "
         "text by rebuild/corpora/ea-corpora-23/seat.py from the specification beside it, spec23-hadith.json."]
body = "\n".join(body) + "\n"

kw = ("corpus seating, primary sources, original language, Arabic, hadith, sunna, al-Kutub al-Tis'a, al-Kutub al-Sitta, "
      "al-Kutub al-Arba'a, Muwatta, Malik ibn Anas, Musnad, Ahmad ibn Hanbal, al-Darimi, Sahih al-Bukhari, al-Bukhari, Sahih Muslim, "
      "Muslim ibn al-Hajjaj, Sunan Ibn Majah, Sunan Abi Dawud, Jami' al-Tirmidhi, Sunan al-Nasa'i, al-Mujtaba, al-Kafi, al-Kulayni, "
      "Man la yahduruhu al-faqih, Ibn Babawayh, al-Shaykh al-Saduq, Tahdhib al-ahkam, al-Istibsar, al-Shaykh al-Tusi, Forty Hadith, "
      "al-Nawawi, Sunni, Imami Shi'i, Qur'an, OpenITI, KITAB, Training Layer Literature, originals shelf, EA-CORPORA")
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nSharks, Lee\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-10-27\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. Sources located, fetched, checked against their git blob ids and "
    "against their headers, assembled into a seat, hashed and indexed, and every locus found in the seated text, all in session by "
    "TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The request, the hadith supplementary to the Qur'an as an "
    "EA-CORPORA seating, is Lee Sharks's; the witness and the scope were chosen in session and are reported in the seat record. "
    "CC-BY-4.0 applies to this record and the seat record; the payload carries its own licence, CC BY-NC-SA 4.0.\n",
    f"### Keywords\n\n{kw}\n",
    "### Related Identifiers\n\nAXN deposit #1531 — EA-CORPORA-02: the seating that placed the Qur'an on the shelf (seat 02/08)\n"
    "AXN deposit #1700 — EA-CORPORA-22: the preceding seating, whose form this one follows\n"
    "AXN deposit #1580 — EA-CORPORA-12: the rule that seatings are periodically gathered\n"
    "Seat EA-CORPORA-02/08 (quran) — on the same shelf\n",
    "### Version\n\nv1.0\n",
    "### Methodology\n\nWorks located in OpenITI's text repositories on GitHub by OpenITI URI; for each, the version OpenITI marks "
    "PRIMARY_VERSION in its version record chosen. Text and version record fetched at the pinned commit and checked against the git "
    "blob id at that commit. Edition statements read from each file's #META# header and version record, with nothing asserted "
    "beyond them. Licence read from the KITAB project's FAQ and the Zenodo release record. Texts seated as published, in OpenITI "
    "mARkdown, each its own text layer. Every file hashed into the seat's MANIFEST.sha256; every verified locus is a string found in "
    "the seated text by rebuild/corpora/ea-corpora-23/seat.py; a locus not found is recorded as not found. The builder, the pins, "
    "the specification and this body are under rebuild/corpora/ea-corpora-23/.\n",
    "### Falsification Conditions\n\nThe seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical "
    "URL; if a seated file's git blob id differs from the blob OpenITI's repository lists at the commit its source.json names; if an "
    "edition statement misstates the #META# header or version record of the file it describes; if a seated version is not the one "
    "OpenITI marks PRIMARY_VERSION at that commit; if a verified locus cannot be found in the seated text; if the licence statement "
    "is not what OpenITI publishes; or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
    f"### Body\n\n{body}"])
out = ROOT / "data/issue-bodies/EA-CORPORA-23-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description")
