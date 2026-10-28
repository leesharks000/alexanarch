#!/usr/bin/env python3
"""Writes spec29-telepathic-prose.json (EA-CORPORA-29/07)."""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
R = pathlib.Path("/home/claude/alexanarch")
PEARL = "data/corpora/pearl-and-other-poems/text/pearl-machine-text.txt"
ED = "data/deposits/AXN-0A9A.md"
n_ed = sum(1 for _ in open(R / ED, encoding="utf-8"))
items, loci = [], []


def add(cls, kind, slug, work, find, **kw):
    items.append({"kind": kind, "slug": slug, "work": work, "class": cls} | kw)
    loci.append({"label": work.split(" — ")[0], "text": f"text/{slug}.txt", "find": find})


def pearl(slug, work, a, b, find):
    add("Pearl text (P)", "extract", slug, work, find, **{"from": str(R / PEARL), "from_rel": PEARL, "lines": [a, b], "seat_of_source": "pearl-and-other-poems"})


def blog(slug, work, url, date, find):
    add("Blog text (B)", "blogger", slug, work, find, url=url, path=f"blog-{slug}.html", published=date)


pearl("btp-pearl", "Lee Sharks & Jack Feist, “Belief & Technique for Telepathic Prose”, the Footnote to Pearl, Pearl and Other Poems (Ann Arbor: New Human Press, 2014), pp. 23–28 — P, copied from the Pearl seat", 2152, 2394, "Compose real poems telepathically, with mind control powers, inside your glorious brain")
blog("btp-blog", "Lee Sharks & Jack Feist, “Belief & Technique for Telepathic Prose”, Mind Control Poems, 1 December 2014 — B, the blog page as served", "https://mindcontrolpoems.blogspot.com/2014/12/belief-technique-fortelepathic-prose.html", "2014-12-01", "Compose real poems telepathically")
pearl("make-it-human-pearl", "Lee Sharks, “Make It Human”, Pearl and Other Poems (2014), pp. 91–95 — P, copied from the Pearl seat", 5229, 5451, "Make It Human")
blog("make-it-human-blog", "Lee Sharks, “Make It Human”, Mind Control Poems, 26 February 2015 — B", "https://mindcontrolpoems.blogspot.com/2015/02/make-it-human.html", "2015-02-26", "Make It Human")
pearl("telepathicist-manifesto-pearl", "Lee Sharks & John Johnson, “A Telepathicist Manifesto”, Pearl and Other Poems (2014), pp. 114–119 — P, copied from the Pearl seat", 6327, 6595, "Telepathicism is about having thoughts, telepathically")
blog("telepathicist-manifesto-blog", "Lee Sharks & John Johnson, “A Telepathicist Manifesto”, Mind Control Poems, 14 March 2015 — B", "https://mindcontrolpoems.blogspot.com/2015/03/a-telepathicist-manifesto.html", "2015-03-14", "Telepathicism is about having thoughts")
D = "/home/claude/drafts/telepathic-prose/drive/"
add("Drafts (2014)", "drive", "btp-drafts-d2-d3-d1", "Lee Sharks, “Belief and Technique for Telepathic Prose”, the drafts of April–May 2014: the Drive file of that title, its states stacked newest first (D2, D3, D1 headed “Begun 4/27/14, Sunday”), with the Kierkegaard journal entry of 20 November 1847 copied after D1 and the notebook entries of 2 and 3 May 2014 — the connector's text export", "Begun 4/27/14, Sunday",
    **{"from": D + "belief-and-technique-drafts.txt", "drive_title": "BELIEF AND TECHNIQUE FOR TELEPATHIC PROSE.docx", "file_id": "0B1alN_rJZUKKU293OUt6ZlBicms", "size": 83044, "created": "2014-07-12T21:43:07Z (a bulk upload; it does not date composition)"})
add("Drafts (2014)", "drive", "btp-draft-w-word-riot", "Lee Sharks, “Belief and Technique for Telepathic Prose”, the copy submitted to Word Riot (W), spring 2014: the Drive file “word riot 4.docx” — the connector's text export", "Penelope weaves impening glory",
    **{"from": D + "word-riot-4.txt", "drive_title": "word riot 4.docx", "file_id": "0B1alN_rJZUKKZW04TVUyazFrcEU", "size": 22890, "created": "2014-07-12T21:40:45Z (a bulk upload; it does not date composition)"})
add("Edition", "extract", "btp-critical-edition-1715", "Belief & Technique for Telepathic Prose: A Critical Edition — the Footnote to Pearl (EA-BTP-EDITION-01; #1715, AXN:0A9A), the deposit's body as minted 2026-10-28 — copied from data/deposits", "sublation",
    **{"from": str(R / ED), "from_rel": ED, "lines": [1, n_ed], "seat_of_source": "#1715"})

spec = {
 "corpus": "telepathic-prose",
 "seat": "EA-CORPORA-29/07",
 "title": "Telepathic Prose: Belief & Technique for Telepathic Prose in its drafts, the book and the blog, Make It Human and A Telepathicist Manifesto, with the critical edition",
 "language": "eng",
 "fetched": "2026-10-28",
 "license": {"payload": "CC-BY-4.0, by the author: the corpus and the seating institution are the same party (as at the Pearl seat).", "record": "CC-BY-4.0."},
 "normalization": "P texts are line ranges of the Pearl seat's machine text, copied with that file's path and sha256, page-number lines kept as the machine text has them. B texts are the Blogger pages as served, under original/, with text/<slug>.txt reduced by code from the post body. The drafts (D1, D2, D3 and W) are the Drive connector's text exports of the two .docx files the edition collates (its §3), seated at the author's ruling of 2026-10-28; the exports escape two characters as Markdown does (a backslash before # and *), kept as served, and the .docx files are recorded by Drive id, size and created time. The edition is the deposit body of #1715 as minted. No text corrected: Pearl is the canonical form, not to be altered (the author's ruling of 2026-10-28), so 'retrictio s' and the repeated item stand.",
 "units": "one text file per witness; class names the witness (P, B, edition)",
 "items": items,
 "loci": loci,
 "classes": ["Pearl text (P)", "Blog text (B)", "Drafts (2014)", "Edition"],
 "cross_references": {
  "pearl": "The whole book is seated at pearl-and-other-poems; these are its telepathic pieces drawn out to stand with the arts of poetry (29/04).",
  "kerouac": "Jack Kerouac's 'Belief & Technique for Modern Prose' (1959), the list the Footnote answers, is declared at jack-kerouac (29/01), where it is described and cited by item number and its text is held out.",
  "seismograph": "Johannes Sigil's 'Tradition and the Individual Seismograph' (Pearl pp. 96–100) is seated in ars-poetica beside Eliot's essay.",
  "captures": "AXN:0A96–0A99.CAPTURE, the four machine readings of 2026-10-28 to which the edition is anchored."
 },
 "scope": "The telepathic pieces of Pearl and Other Poems in both their witnesses, with the critical edition: the ars poetica of the archive itself, set at the end of the twenty-ninth seating's arts of poetry.",
 "why_seated": "At the author's direction: 'lets gather up an extremely pluriform ars poetica bundle … include telepathic prose.'",
 "spine": "29/07",
 "ruling": "The author's directions of 2026-10-28.",
 "seating": "EA-CORPORA-29 (gathered; the deposit that assigns its AXN is pending)"
}
(HERE / "spec29-telepathic-prose.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(items), "items")
