#!/usr/bin/env python3
"""Write the EA-CORPORA-24 deposit issue body (a DRAFT until minted) from the four seat records.
Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-24-issue.md"""
import json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = ROOT / "data/corpora"
SEATS = [("latter-day-saints", "Seat 24/01 — The Latter Day Saints, to the Succession of 1844",
          "The Book of Mormon as first printed and as revised, the revelations, and the succession contested in Nauvoo and Voree"),
         ("babi-bahai", "Seat 24/02 — The Bab, the Babis and the Baha'is",
          "The Qayyum al-Asma' of 1844 and the Persian Bayan in manuscript, the Kitab-i Iqan and al-Kitab al-Aqdas, and the two histories of the division"),
         ("millerite-adventist", "Seat 24/03 — The Millerites and the Disappointment of 22 October 1844",
          "Miller's computation, the papers that set the day, and the Sabbatarian Adventists who came out of it"),
         ("taiping", "Seat 24/04 — The Taiping Heavenly Kingdom",
          "Hong Xiuquan's tracts, the books issued under the Heavenly King's seal, the Taiping Bible, and Yang Xiuqing's voice of God, in Chinese")]
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


title = ("EA-CORPORA-24 — The Twenty-Fourth Seating: 1844. The Book of Mormon and the Latter Day Saint Succession, the Bab and the "
         "Babi–Baha'i Division, the Millerite Disappointment and the Taiping Heavenly Kingdom, Each in Its Original Language")
parts, tot, nw = [], 0, 0
for c, h, sub in SEATS:
    t, s = section(c, h, sub); parts.append(t); tot += s["lines_total"]; nw += s["works"]["count"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())

hdr = f"""# {title}

# EA-CORPORA-24 — The Twenty-Fourth Seating

MANUS, 27 October 2026: "need to seat the book of mormon but im not doing it without several diverging simultaneous traditions in the batch" — and, offered the traditions that divided in 1844 or the Book of Mormon's own diverging editions: "1. definitely. lets go."

The seating is a year. On the night of 22–23 May 1844 the Bab declared his mission in Shiraz and began the Qayyum al-Asma'. On 27 June Joseph Smith was killed at Carthage, Illinois, and the church he founded divided over who should lead it. The Millerites, who had reckoned the return of Christ for 1843, fixed it in August at 22 October 1844, and the day passed. In the same year Hong Xiuquan, who had seen his vision in 1837, went out preaching into Guangxi with Feng Yunshan, where the God Worshippers' Society that became the Taiping Heavenly Kingdom took shape. Each tradition is seated with the scripture it began from and with the documents of the division that followed: the Twelve and Strang, Baha'u'llah and Subh-i Azal, the Sabbatarian Adventists, and the Taiping kingdom whose God spoke through Yang Xiuqing.
"""
tail = f"""## Not seated, and why

- The 1837 Kirtland edition of the Book of Mormon: not found in an open scan. QUEUED. Strang's Book of the Law of the Lord (1851; 1856), the Reorganized Church's editions (from 1874; the Authorized Version of 1908), the Pearl of Great Price (1851): QUEUED. The manuscripts in the Joseph Smith Papers are under that project's terms.
- The UCLA manuscript of the Persian Bayan (a 199 MB scan, over the repository's file limit); the Arabic Bayan, found only in a 1962 printing; writings of Subh-i Azal in his own name: QUEUED.
- A Word to the "Little Flock" (1847): found only in a facsimile with a twentieth-century foreword. The New York and Boston Millerite papers and the non-Sabbatarian Adventist bodies: QUEUED.
- The Taiping books Wikisource does not hold (among them the Taiping Imperial Declaration, the army organization and the calendar) and the Gospel of John of the Taiping New Testament; scans of the original Nanjing imprints: QUEUED.
- Translations, by the shelf's rule.

## How the seats were made

Sources located on the Internet Archive (advanced search; item metadata read for access restriction and files; each item's text layer read for its title page, so that the 1840 Book of Mormon, the 1845 Doctrine and Covenants and the Browne volumes are identified from their own title pages), in H-Bahai's digital library (the Iran National Baha'i Archives volumes and the digital reprints of the Iqan lithographs and Tumanskii's Aqdas, each with its descriptive page read), on Project Gutenberg (Bates) and on Chinese Wikisource (the Taiping books, each page fetched at a recorded revision as wikitext and rendered HTML, with the text layer derived by code). Every Internet Archive file checked against the md5 the Archive publishes; none differed. H-Bahai publishes no checksums: its files are hashed as fetched. Every file hashed into its seat's MANIFEST.sha256. Every verified locus of a text layer is a string found in it by rebuild/corpora/ea-corpora-24/seat.py; the loci of the manuscripts and lithographs, which have no text layer, are read from the scan and recorded with the page. {nw} works in 4 seats; {nfiles} files; {tot:,} lines of text layer.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail

desc = (f"Four seats on the originals shelf, {nw} works in their original languages, for the year 1844, in which four traditions began "
        "or divided. The Latter Day Saints: the Book of Mormon in the first edition (Palmyra, 1830) and the revised third (Nauvoo, 1840), "
        "the Book of Commandments (1833), the Doctrine and Covenants of 1835 and 1845, the Times and Seasons of September 1844, and "
        "James J. Strang's Voree counter-claim (1846; 1848). The Bab and the Baha'is: the Qayyum al-Asma', begun the night of the "
        "Bab's declaration, the Persian Bayan and Panj Sha'n in manuscript, Baha'u'llah's Kitab-i Iqan in the Bombay lithographs "
        "(c. 1882; 1893) and al-Kitab al-Aqdas in Tumanskii's edition (1899), the Traveller's Narrative (1891) and the Nuqtat al-Kaf "
        "(1910). The Millerites: Miller's Evidence (1842), the Western Midnight Cry, the True Midnight Cry that set 22 October 1844, "
        "Bates's Seventh Day Sabbath (1847) and Ellen G. White's Sketch (1851). The Taiping: Hong Xiuquan's Yuandao tracts, the "
        "imperially sanctioned books including the Taiping Bible (1853), and Hong Rengan's New Treatise (1859), in Chinese. What is "
        "not seated is named.")

kw = ("corpus seating, primary sources, original language, public domain, 1844, Book of Mormon, Joseph Smith, Latter Day Saints, "
      "Book of Commandments, Doctrine and Covenants, succession crisis, Times and Seasons, Sidney Rigdon, "
      "Quorum of the Twelve, James J. Strang, Voree, Strangites, the Bab, Babi, Qayyum al-Asma, Persian Bayan, Baha'u'llah, "
      "Kitab-i Iqan, Kitab-i Aqdas, Subh-i Azal, Azali, Baha'i, Traveller's Narrative, Nuqtat al-Kaf, Edward G. Browne, "
      "Iran National Baha'i Archives, H-Bahai, William Miller, Millerites, Great Disappointment, Midnight Cry, "
      "Joseph Bates, Seventh Day Sabbath, Ellen G. White, Sabbatarian Adventists, Taiping Heavenly Kingdom, Hong Xiuquan, "
      "Yang Xiuqing, Hong Rengan, Taiping Bible, God Worshippers' Society, Training Layer Literature, originals shelf, EA-CORPORA")

issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nSharks, Lee\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-10-27\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. Sources located, fetched, checked against the Internet Archive's "
    "published md5 sums and against their title pages, assembled into seats, hashed and indexed, the text loci found in the seated "
    "text and the scan loci read from the page, all in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. "
    "The request (the Book of Mormon, only beside several diverging simultaneous traditions) and the choice of 1844 are Lee "
    "Sharks's; the witnesses were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records; "
    "each payload carries its own licence, stated per seat.\n",
    f"### Keywords\n\n{kw}\n",
    "### Related Identifiers\n\nAXN deposit #1706 — EA-CORPORA-23: the preceding seating, the hadith, whose form this one follows\n"
    "AXN deposit #1700 — EA-CORPORA-22: the form of a multi-seat seating\n"
    "AXN deposit #1580 — EA-CORPORA-12: the rule that seatings are periodically gathered\n"
    "AXN deposit #1531 — EA-CORPORA-02: the Qur'an, the Hebrew Bible and the Greek New Testament on the same shelf\n",
    "### Version\n\nv1.0\n",
    "### Methodology\n\nSources located on the Internet Archive, in H-Bahai's digital library, on Project Gutenberg and on Chinese "
    "Wikisource; each item's title page or descriptive page read against the edition claimed for it, with nothing asserted beyond "
    "it. Internet Archive files checked against the Archive's md5; Wikisource pages fetched at recorded revisions as wikitext and "
    "rendered HTML, the text layer derived by code. Every file hashed into its seat's MANIFEST.sha256. Text loci are strings found "
    "in the seated text by rebuild/corpora/ea-corpora-24/seat.py; scan loci are read from the page and recorded with it. Licences "
    "stated per seat (payload/record split). The builders, the specifications and this body are under "
    "rebuild/corpora/ea-corpora-24/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; "
    "if a seated Internet Archive file's md5 differs from the Archive's; if a Wikisource text differs from the page at the revision "
    "recorded for it; if an edition statement misstates the title page or descriptive page of the file it describes; if a verified "
    "text locus cannot be found in the seated text, or a scan locus does not stand on the page named; if an item stated public "
    "domain is not; or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
    f"### Body\n\n{body}"])
out = ROOT / "data/issue-bodies/EA-CORPORA-24-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", nw, "works;", tot, "lines;", nfiles, "files")
