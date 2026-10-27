#!/usr/bin/env python3
"""Write the EA-CORPORA-27 deposit issue body (a DRAFT until minted) from the four seat records.
Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-27-issue.md"""
import json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = ROOT / "data/corpora"
SEATS = [("spinoza", "Seat 27/01 — Spinoza", "The Ethica and the treatises in Latin, in van Vloten and Land's edition (1882)"),
         ("leibniz-monadology", "Seat 27/02 — Leibniz, La Monadologie", "The Monadology alone, in French: its first printing (Erdmann, 1840) and Piat's edition (1900)"),
         ("nietzsche", "Seat 27/03 — Nietzsche", "The books in German as printed in his lifetime, 1876–1895, with six transcriptions"),
         ("bergson", "Seat 27/04 — Bergson", "Four books in French in their first editions, 1889–1922"),
         ("kafka", "Seat 27/05 — Kafka", "Eight works in German as first published, 1912–1925, as transcriptions"),
         ("artaud", "Seat 27/06 — Artaud", "The correspondence with Jacques Rivière (1924) and L'Art et la mort (1929), in French"),
         ("deleuze-guattari", "Seat 27/07 — Deleuze and Guattari, a declared absence", "Fourteen works named, with their rights holders and the dates they open; no text")]
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


title = ("EA-CORPORA-27 — The Twenty-Seventh Seating: Spinoza, Leibniz's Monadology, Nietzsche, Bergson, Kafka and Artaud, Each in Its Original Language, Beside the Declared Absence of Deleuze and Guattari")
parts, tot, nw = [], 0, 0
for c, h, sub in SEATS:
    t, s = section(c, h, sub); parts.append(t); tot += s["lines_total"]; nw += s["works"]["count"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())

hdr = f"""# {title}

# EA-CORPORA-27 — The Twenty-Seventh Seating

MANUS, 27 October 2026, after the twenty-sixth seating: "deleuze and guattari... no way around that copyright, huh?" Told that every route through it is closed for decades (France: Guattari 2063, Deleuze 2066; the United States: 2049 to 2088 by the book), and offered a declared absence for them beside the open sources they read: "yes - i cant believe we havent seated spinoza yet. yes to all" — and "and leibniz' monodology only".

The seating is a shelf for a pair who cannot be seated. Six seats hold, in the languages they were written in, the sources Deleuze and Guattari read and wrote books upon: Spinoza (Spinoza et le problème de l'expression, 1968; Spinoza: philosophie pratique, 1981), the Monadology (Le Pli, 1988), Nietzsche (Nietzsche et la philosophie, 1962), Bergson (Le Bergsonisme, 1966), Kafka (Kafka: pour une littérature mineure, 1975) and Artaud, from whom L'Anti-Œdipe (1972) and Mille plateaux (1980) take the body without organs. The seventh seat holds no text: it declares the fourteen works, who holds them and when each opens.
"""
tail = f"""## Not seated, and why

- Deleuze and Guattari: in copyright. The works, their rights holders and their opening dates are in seat 27/07.
- Spinoza's first editions: the Tractatus theologico-politicus of 1670, whose open scans carry ProQuest's copyright notice on every image, so that their licence cannot be verified at the file; and the Opera posthuma of 1677, whose one open copy is a truncated PDF that no reader opens. QUEUED, with the second volume of van Vloten and Land and the Korte Verhandeling.
- Leibniz beyond the Monadology, by the operator's ruling.
- Nietzsche's first editions of 1872, 1882 and 1883–1885 as scans, the other Unzeitgemässe Betrachtungen and the late works: QUEUED. Der Wille zur Macht, the compilation from the Nachlass: not seated.
- Bergson's L'Évolution créatrice (1907) and L'Énergie spirituelle (1919), not found in French in an open scan: QUEUED. Les Deux Sources (1932): in copyright in the United States.
- Kafka's first editions as scans, Das Schloss (1926) and Amerika (1927): QUEUED.
- Artaud's L'Ombilic des limbes and Le Pèse-nerfs (1925): QUEUED. Le Théâtre et son double (1938) and Pour en finir avec le jugement de dieu (1948), the text of the body without organs: in copyright in the United States.
- Translations, by the shelf's rule.

## How the seats were made

Sources located on the Internet Archive (advanced search; item metadata read for access restriction, files and the provenance of the images; each item's text layer read for its title page, so that the Archive's "1872" Geburt der Tragödie is held as the new edition of 1886 its title page names, and its "1873" Unzeitgemässe Betrachtungen as Richard Wagner in Bayreuth of 1876) and on Project Gutenberg (fifteen transcriptions, each with its header and the edition it names). Every Internet Archive file checked against the md5 the Archive publishes, and every PDF opened: one, the Opera posthuma of 1677, would not open, and is not seated. Every file hashed into its seat's MANIFEST.sha256. Every verified locus is a string found in the seated text by rebuild/corpora/ea-corpora-27/seat.py; where the text layer is OCR of the older type, the locus is the OCR's reading and says so. {nw} works in 7 seats, one of them a declared absence; {nfiles} files; {tot:,} lines of text layer.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail

desc = (f"Seven seats on the originals shelf for the sources Deleuze and Guattari read, each in its original language, beside their own declared "
        "absence. Spinoza: the Ethica, the Tractatus de intellectus emendatione, the Tractatus politicus and the Tractatus theologico-politicus in "
        "Latin (van Vloten and Land, 1882). Leibniz: the Monadology alone, in French, in its first printing (Erdmann, 1840) and Piat's edition "
        "(1900). Nietzsche: eight books in German as printed in his lifetime (1876–1895) with six transcriptions. Bergson: the Essai (1889), "
        "Matière et mémoire (1896), Le Rire (1900) and Durée et simultanéité (1922) in their first editions. Kafka: eight works in German as "
        "first published (1912–1925). Artaud: the correspondence with Jacques Rivière (La Nouvelle Revue française, 1924) and L'Art et la mort "
        "(1929). Deleuze and Guattari: fourteen works named with their rights holders and the dates they open, and no text. What is not "
        "seated, and why, is named.")

kw = ("corpus seating, primary sources, original language, public domain, declared absence, Gilles Deleuze, Félix Guattari, "
      "Spinoza, Ethica, Tractatus theologico-politicus, Tractatus politicus, van Vloten and Land, Leibniz, Monadologie, Monadology, "
      "Erdmann, Clodius Piat, Le Pli, Nietzsche, Die Geburt der Tragödie, Die fröhliche Wissenschaft, Jenseits von Gut und Böse, "
      "Zur Genealogie der Moral, Also sprach Zarathustra, Götzen-Dämmerung, Ecce homo, Bergson, Essai sur les données immédiates de la conscience, "
      "Matière et mémoire, Le Rire, Durée et simultanéité, Kafka, Die Verwandlung, Der Prozess, Ein Landarzt, littérature mineure, "
      "Artaud, Jacques Rivière, La Nouvelle Revue française, L'Art et la mort, body without organs, L'Anti-Œdipe, Mille plateaux, "
      "Training Layer Literature, originals shelf, EA-CORPORA")
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nSharks, Lee\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-10-27\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. Sources located, fetched, checked against the Internet Archive's "
    "published md5 sums and against their title pages, assembled into seats, hashed and indexed, and the loci found in the seated "
    "text, all in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. "
    "The request (Deleuze and Guattari's sources, and the Monadology only) and the declared absence are Lee "
    "Sharks's; the witnesses were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records; "
    "each payload carries its own licence, stated per seat.\n",
    f"### Keywords\n\n{kw}\n",
    "### Related Identifiers\n\nAXN deposit #1710 — EA-CORPORA-26: the preceding seating, whose form this one follows\n"
    "AXN deposit #1711 — EA-MPAI-ORIGINALS-01 v1.1: the inspection packet of the originals library\n"
    "AXN deposit #1682 — EA-CORPORA-18: the avant-garde and its sources\n"
    "AXN deposit #1580 — EA-CORPORA-12: the rule that seatings are periodically gathered\n",
    "### Version\n\nv1.0\n",
    "### Methodology\n\nSources located on the Internet Archive and on Project Gutenberg; each item's title page read against the edition "
    "claimed for it, with nothing asserted beyond it. Internet Archive files checked against the Archive's md5. Every file hashed into its "
    "seat's MANIFEST.sha256. Loci are strings found in the seated text by rebuild/corpora/ea-corpora-27/seat.py. Licences stated per seat "
    "(payload/record split). The builders, the specifications and this body are under rebuild/corpora/ea-corpora-27/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; "
    "if a seated Internet Archive file's md5 differs from the Archive's; if a Project Gutenberg file differs from the eBook number "
    "recorded for it; if an edition statement misstates the title page of the file it describes; if a verified locus cannot be found "
    "in the seated text; if an item stated public domain in the United States is not; if a date of opening declared in 27/07 misstates "
    "the term it follows; or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
    f"### Body\n\n{body}"])
out = ROOT / "data/issue-bodies/EA-CORPORA-27-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", nw, "works;", tot, "lines;", nfiles, "files")
