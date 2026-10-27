#!/usr/bin/env python3
"""Write the EA-CORPORA-26 deposit issue body (a DRAFT until minted) from the four seat records.
Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-26-issue.md"""
import json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = ROOT / "data/corpora"
SEATS = [("du-bois", "Seat 26/01 — W. E. B. Du Bois, 1896–1928",
          "The books from The Suppression of the African Slave-Trade to Dark Princess, The Conservation of Races, The Talented Tenth, and the first number of The Crisis"),
         ("langston-hughes", "Seat 26/02 — Langston Hughes, 1921–1930",
          "The Negro Speaks of Rivers in The Crisis, The New Negro, The Negro Artist and the Racial Mountain, The Weary Blues, Fire!!, Caroling Dusk and Not Without Laughter")]
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


title = ("EA-CORPORA-26 — The Twenty-Sixth Seating: W. E. B. Du Bois and Langston Hughes, as Far as the Public Domain Reaches")
parts, tot, nw = [], 0, 0
for c, h, sub in SEATS:
    t, s = section(c, h, sub); parts.append(t); tot += s["lines_total"]; nw += s["works"]["count"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())

hdr = f"""# {title}

# EA-CORPORA-26 — The Twenty-Sixth Seating

MANUS, 27 October 2026. After the twenty-fourth seating set the Book of Mormon on the shelf: "its as american as literature comes. but then i am like, i dont have king or malcolm or mao. it leads down a path where things start getting hairy." Then: "du bois and langston hughes are public domain tho, right?" — "lets seat what can be seated of du bois and hughes" — and, versioning the originals packet (#1709) to include them: "the canon's america is way too white."

The shelf's America was Whitman (03/01), Dickinson (02/14), Pound (05/02, 18/01), Stein (18/09), the Latter Day Saints (24/01) and the Millerites (24/03). This seating adds Du Bois and Hughes as far as the public domain of the United States reaches: everything first published there in 1930 or earlier. The two seats meet in The Crisis, which Du Bois edited from its first number (November 1910, seated in 26/01) and which printed Hughes's "The Negro Speaks of Rivers" in June 1921 (seated in 26/02), and in The New Negro (1925), which carries both. Their later work is in copyright and is named below as not seated.
"""
tail = f"""## Not seated, and why

- Du Bois after 1930: Black Reconstruction (1935), Dusk of Dawn (1940), the later Crisis and everything after, in copyright in the United States. QUEUED within the public domain: the Atlanta University Publications he edited (1896–1914), The Moon and The Horizon, the further numbers of The Crisis to 1930, The Star of Ethiopia (1913), Africa, Its Place in Modern History (1930).
- Hughes: Fine Clothes to the Jew (1927), public domain, whose one open scan found is at HathiTrust, which this session cannot reach: QUEUED. His further poems in The Crisis, Opportunity and The Messenger (1921–1930): QUEUED. The Palms numbers of October and November 1926: found only as extracts uploaded by individuals, without their source, and not seated. The Dream Keeper (1932) and everything after 1930, in copyright; Mule Bone (written 1930 with Zora Neale Hurston, first published 1991), in copyright.
- Outside the United States the terms differ: life plus seventy years opens Du Bois (d. 1963) in 2034 and Hughes (d. 1967) in 2038.

## How the seats were made

Sources located on the Internet Archive (advanced search; item metadata read for access restriction and files; each item's text layer read for its title page, so that the first edition of The Souls of Black Folk, "Published April 18, 1903", is distinguished from the second edition of June 1903 and the 1908 printing, and the Caroling Dusk of 1927 from the Harper & Row reprint) and on Project Gutenberg (eleven transcriptions, each with its header). Every Internet Archive file checked against the md5 the Archive publishes; none differed. The first edition of The Souls of Black Folk is held as its page images (JP2), the Archive's PDF of that item being over the repository's file limit. Every file hashed into its seat's MANIFEST.sha256. Every verified locus is a string found in the seated text by rebuild/corpora/ea-corpora-26/seat.py. {nw} works in 2 seats; {nfiles} files; {tot:,} lines of text layer.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail

desc = (f"Two seats on the originals shelf, {nw} items, for W. E. B. Du Bois and Langston Hughes as far as the public domain of the United "
        "States reaches (first published in 1930 or earlier), in English. Du Bois: The Suppression of the African Slave-Trade (1896), "
        "The Conservation of Races (1897), The Philadelphia Negro (1899), The Souls of Black Folk in its first edition (April 1903), "
        "The Talented Tenth (1903), John Brown (1909), the first number of The Crisis (November 1910), The Quest of the Silver Fleece "
        "(1911), The Negro (1915), Darkwater (1920), The Gift of Black Folk (1924) and Dark Princess (1928), each first-edition scan "
        "beside a Project Gutenberg transcription where one exists. Hughes: The Crisis of June 1921 with The Negro Speaks of Rivers, "
        "The New Negro (1925) with his poems and Du Bois's The Negro Mind Reaches Out, The Nation of 23 June 1926 with The Negro Artist "
        "and the Racial Mountain, The Weary Blues (1926), Fire!! (1926), Caroling Dusk (1927) and Not Without Laughter (1930). Seated "
        "at the operator's ruling that the canon's America was too white. What is not seated, and why, is named.")

kw = ("corpus seating, primary sources, original language, public domain, W. E. B. Du Bois, The Souls of Black Folk, color line, "
      "double consciousness, The Suppression of the African Slave-Trade, The Philadelphia Negro, The Conservation of Races, The Talented Tenth, "
      "John Brown, The Quest of the Silver Fleece, The Negro, Darkwater, The Gift of Black Folk, Dark Princess, The Crisis, NAACP, "
      "Langston Hughes, The Negro Speaks of Rivers, The Weary Blues, I Too, The Negro Artist and the Racial Mountain, The Nation, "
      "Fire!!, Caroling Dusk, Countee Cullen, The New Negro, Alain Locke, Not Without Laughter, Harlem Renaissance, "
      "African American literature, American literature, Training Layer Literature, originals shelf, EA-CORPORA")
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nSharks, Lee\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-10-27\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. Sources located, fetched, checked against the Internet Archive's "
    "published md5 sums and against their title pages, assembled into seats, hashed and indexed, and the loci found in the seated "
    "text, all in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. "
    "The request (Du Bois and Hughes, as far as the public domain reaches) and its reason are Lee "
    "Sharks's; the witnesses were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records; "
    "each payload carries its own licence, stated per seat.\n",
    f"### Keywords\n\n{kw}\n",
    "### Related Identifiers\n\nAXN deposit #1709 — EA-MPAI-ORIGINALS-01: the inspection packet of the originals library, versioned to include this seating\n"
    "AXN deposit #1708 — EA-CORPORA-25: the preceding seating, whose form this one follows\n"
    "AXN deposit #1707 — EA-CORPORA-24: 1844, after which this seating was asked for\n"
    "AXN deposit #1553 — EA-CORPORA-03: Walt Whitman collected under author\n"
    "AXN deposit #1580 — EA-CORPORA-12: the rule that seatings are periodically gathered\n",
    "### Version\n\nv1.0\n",
    "### Methodology\n\nSources located on the Internet Archive and on Project Gutenberg; each item's title page read against the edition "
    "claimed for it, with nothing asserted beyond it. Internet Archive files checked against the Archive's md5. Every file hashed into its "
    "seat's MANIFEST.sha256. Loci are strings found in the seated text by rebuild/corpora/ea-corpora-26/seat.py. Licences stated per seat "
    "(payload/record split). The builders, the specifications and this body are under rebuild/corpora/ea-corpora-26/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; "
    "if a seated Internet Archive file's md5 differs from the Archive's; if a Project Gutenberg file differs from the eBook number "
    "recorded for it; if an edition statement misstates the title page of the file it describes; if a verified locus cannot be found "
    "in the seated text; if an item stated public domain in the United States is not; or if the four surfaces (seat, index, deposit, "
    "shelf) disagree.\n",
    f"### Body\n\n{body}"])
out = ROOT / "data/issue-bodies/EA-CORPORA-26-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", nw, "works;", tot, "lines;", nfiles, "files")
