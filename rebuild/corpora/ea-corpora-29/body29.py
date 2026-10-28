#!/usr/bin/env python3
"""Write the EA-CORPORA-29 deposit issue body from the eleven seat records (the form of body28.py).
Edition lines, loci, licences and scopes are read from data/corpora/<seat>/source.json.
-> data/issue-bodies/EA-CORPORA-29-issue.md"""
import json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = ROOT / "data/corpora"
SEATS = [("jack-kerouac", "Seat 29/01 — Jack Kerouac", "A declared absence: the statements of method, the novels and Mexico City Blues"),
         ("horace", "Seat 29/02 — Horace", "The poems in Latin, with the Ars Poetica"),
         ("ovid", "Seat 29/03 — Ovid", "The poems in Latin, from the Amores to the Ibis; the Fasti queued"),
         ("ars-poetica", "Seat 29/04 — Ars Poetica", "The art of poetry in twenty traditions"),
         ("avant-garde-ii", "Seat 29/05 — The Avant-Garde, II", "Statements of method, 1913–1929"),
         ("ars-poetica-wanted", "Seat 29/06 — Ars Poetica, wanted", "A declared absence: the moderns, Language writing, conceptual writing and the contemporary"),
         ("telepathic-prose", "Seat 29/07 — Telepathic Prose", "Belief & Technique in its drafts, the book and the blog, with Make It Human, A Telepathicist Manifesto and the critical edition"),
         ("pali-tipitaka", "Seat 29/08 — The Pali Tipiṭaka", "The three piṭakas in root Pali"),
         ("buddhist-sanskrit", "Seat 29/09 — The Buddhist Canon in Sanskrit", "The Mahāyāna sūtras, the śāstras, the kāvya and the avadāna"),
         ("east-asian-buddhism", "Seat 29/10 — The Mahāyāna in East Asia", "The Chinese canon, Chan, Japan and Korea"),
         ("derge-kangyur", "Seat 29/11 — The Derge Kangyur", "Eight volumes in Tibetan")]
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
            out += [f"- {lab}: " + ("; ".join(v) if isinstance(v, list) else "; ".join(f"{a}: {b}" for a, b in v.items()))]
    out += [f"- Why seated: {s['why_seated']}",
            f"- Files: [the seat](https://www.alexanarch.org/data/corpora/{corpus}/) — [source.json](https://www.alexanarch.org/data/corpora/{corpus}/source.json), "
            f"[MANIFEST.sha256](https://www.alexanarch.org/data/corpora/{corpus}/MANIFEST.sha256). Shelf: "
            f"[traininglayerliterature.org/originals/{corpus}](https://traininglayerliterature.org/originals/{corpus}/)", ""]
    return "\n".join(out), s


title = ("EA-CORPORA-29 — The Twenty-Ninth Seating, the Pluriform: Horace and Ovid, the Art of Poetry in Twenty Traditions, the Avant-Garde II, "
         "Telepathic Prose, and the Buddhist Canons in Pali, Sanskrit, Chinese, Korean, Japanese and Tibetan")
parts, tot, nw = [], 0, 0
for c, h, sub in SEATS:
    t, s = section(c, h, sub); parts.append(t); tot += s["lines_total"]; nw += s["works"]["count"]
nfiles = sum(1 for c, _, _ in SEATS for p in (A / c).rglob("*") if p.is_file())

hdr = f"""# {title}

# EA-CORPORA-29 — The Twenty-Ninth Seating

The seating began with Belief & Technique for Telepathic Prose: A Critical Edition (#1715), whose apparatus asked for Kerouac's list (declared, 29/01) and Horace's Ars Poetica (29/02). The author then asked for "an extremely pluriform ars poetica bundle to gather with the others for the next ea-corpora. include telepathic prose", for Ovid entire, for Language writing and the contemporary arts of poetry as wanted, for the experimental, Dada and Surrealist statements of method, and for the bundle to go "further globally, hebrew, sanskrit, korean - this will be the single widest ranging ea corpora deposit", with "Tradition and the Individual Seismograph" beside Eliot's essay. Gathering it for deposit, he widened it once more: "lets just make it a *totally* pluriform bundled ea-corpora - we need buddhist canon, various traditions, mahayana included."

Eleven seats. The arts of poetry run from the Nāṭyaśāstra and the Great Preface to the Odes through Mayakovsky, Hagiwara and Bialik, in twenty traditions, beside the avant-garde's statements of method and the archive's own art of poetry in all its witnesses. The wanted list names what the shelf cannot hold yet, and when each opens. The Buddhist seats set one canon in its several languages. The Pali Tipiṭaka is seated complete, the harvest the Dhammapada seat queued (02/17). The Mahāyāna sūtras and śāstras come in Sanskrit. The Chinese canon comes with Chan, Japan and Korea. The Derge Kangyur gives the same sūtras in Tibetan, so that the Lotus, the Diamond, the Heart and the Vimalakīrti stand on the shelf in Sanskrit, Chinese and Tibetan at once.
"""
tail = f"""## How the seats were made

Every seat was fetched in session and hashed into its MANIFEST.sha256, with a source.json recording edition, origin, licence, normalization and the loci verified in the text layer. The builders are under rebuild/corpora/ea-corpora-29/: build29.py (TEI, Wikisource, GRETIL, Gutenberg, Aozora, Internet Archive, Blogger, Drive and extract kinds, on the 27th seating's seat.py), pali29.py, tib29.py, absences29.py and absences29_wanted.py, with the spec generators. Wikisource pages are kept as served, with their revision ids. Large Internet Archive scans are held by reference, with the Archive's md5. The Pali canon is held as a byte-reproducible git archive of the repository tree at its commit. The NonCommercial GRETIL payloads are handled under the payload/record split of EA-CORPORA-02. Declared absences hold no text of the works they name. Terms follow the rules each seat states; they are not legal advice. {len(SEATS)} seats; {nw} works; {tot:,} lines; {nfiles} files.
"""
body = hdr + "\n" + "\n".join(parts) + "\n" + tail

desc = ("The twenty-ninth seating of the originals shelf, eleven seats. Kerouac declared; Horace and Ovid in Latin. Sixty-four arts of poetry in "
        "twenty traditions, from Bharata, the Great Preface and Lu Ji to Mayakovsky, Hagiwara and Bialik, with Sigil's 'Tradition and the "
        "Individual Seismograph' beside Eliot's essay. The avant-garde's statements of method, 1913–1929, and the arts of poetry still wanted. "
        "Belief & Technique for Telepathic Prose in its 2014 drafts, the book and the blog, with Make It Human, A Telepathicist Manifesto and "
        "the critical edition. And the Buddhist canons: the Pali Tipiṭaka complete; the Mahāyāna sūtras and śāstras in Sanskrit; the Chinese "
        "canon with Chan, Dōgen, the Tannishō, Hakuin and Han Yong-un; and the Derge Kangyur in Tibetan.")
kw = ("EA-CORPORA, originals shelf, ars poetica, art of poetry, poetics, Horace, Ovid, Nāṭyaśāstra, Dhvanyāloka, Great Preface, Wenfu, Wenxin "
      "diaolong, Kokinshū, Pahanjip, Bialik, Qudama, Chahar Maqala, Snorri, Auraicept, Leys d'Amors, Dante, Boileau, Rimbaud, Mallarmé, Lope de "
      "Vega, Mayakovsky, Sidney, Shelley, Eliot, Tradition and the Individual Seismograph, Imagism, Dada, Surrealism, Hu Shi, Language writing, "
      "Belief & Technique for Telepathic Prose, Kerouac, Pali Tipiṭaka, SuttaCentral, Mahāyāna, Lotus Sūtra, Prajñāpāramitā, Heart Sūtra, "
      "Diamond Sūtra, Nāgārjuna, Śāntideva, Vasubandhu, Chan, Platform Sūtra, Linji, Blue Cliff Record, Gateless Barrier, Dōgen, Tannishō, "
      "Hakuin, Han Yong-un, Derge Kangyur, Tibetan, GRETIL, Wikisource, Training Layer Literature")
issue = "\n".join([
    "### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
    f"### Title\n\n{title}\n", "### Creator\n\nSharks, Lee\n", "### ORCID\n\n0009-0000-1599-0703\n",
    "### Date\n\n2026-10-28\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
    "### Substrate Disclosure\n\nHuman–machine collaborative. The sources found, fetched, verified, hashed and indexed, the builders written and the "
    "records drafted, all in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The requests and the choices of tradition "
    "are Lee Sharks's; the works within each seat were chosen in session and are stated per seat. CC-BY-4.0 applies to this record and the seat records.\n",
    f"### Keywords\n\n{kw}\n",
    "### Related Identifiers\n\nAXN deposit #1715 — Belief & Technique for Telepathic Prose: A Critical Edition, whose apparatus began the seating\n"
    "AXN deposit #1713 — EA-CORPORA-28: the wanted, whose declared absences 29/01 and 29/06 continue\n"
    "AXN deposit #1711 — EA-MPAI-ORIGINALS-01 v1.1: the inspection packet of the originals library\n"
    "AXN deposit #1121 — Pearl and Other Poems: the copy-text of the telepathic pieces and of Sigil's essay\n"
    "AXN deposit #1531 — EA-CORPORA-02: the Dhammapada seat (02/17), whose canon harvest the Pali seat completes\n",
    "### Version\n\nv1.0\n",
    "### Methodology\n\nEach seat fetched in session from the source its record names (Perseus, GRETIL, SuttaCentral, Esukhia, Wikisource, Project "
    "Gutenberg, Aozora Bunko, the Internet Archive, JSTOR Early Journal Content, the author's blog and Drive), kept as served, reduced to a text "
    "layer by code and hashed into its MANIFEST.sha256; licences read at the file; loci verified by substring in the text layer; public-domain "
    "status in the United States checked against first publication. No text corrected by hand. The builders and this body are under "
    "rebuild/corpora/ea-corpora-29/.\n",
    "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a verified "
    "locus is absent from the text layer it names; if a work is misattributed, misdated or assigned to the wrong edition; if a licence recorded "
    "for an item is not the one its source states; if a work seated as public domain in the United States is not; or if the four surfaces "
    "(seat, index, deposit, shelf) disagree.\n",
    f"### Body\n\n{body}"])
out = ROOT / "data/issue-bodies/EA-CORPORA-29-issue.md"
out.write_text(issue, encoding="utf-8")
print(out, len(body.split()), "words in body;", len(desc), "chars in description;", nw, "works;", tot, "lines;", nfiles, "files")
