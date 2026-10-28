#!/usr/bin/env python3
"""EA-CORPORA-29 (session tool): the declared absence of Jack Kerouac (29/01), in the form of the 28th seating's
declarations (rebuild/corpora/ea-corpora-28/absences28.py): declared/absence.json and declared/absence.md, a source.json
and a MANIFEST.sha256, and no text of the works it names.
    python3 absences29.py <stage>"""
import json, hashlib, pathlib, sys
ST = pathlib.Path(sys.argv[1])
US_PRE64 = "if its copyright was renewed (a United States work published before 1964 needed renewal; the renewal is to be checked)"
def us(y, renew=False):
    return f"{y+96}-01-01" + (f" {US_PRE64}" if renew else "")
s = dict(corpus="jack-kerouac", seat="01", lang="eng",
  title="Jack Kerouac — a declared absence: Belief & Technique for Modern Prose and Essentials of Spontaneous Prose, with the novels and Mexico City Blues",
  holder="The Estate of Jack Kerouac; the first publishers named.",
  why="Jack Kerouac (1922–1969) is entered as wanted, at the operator's ruling of 2026-10-28 on the proposals of Belief & Technique for Telepathic Prose: A Critical Edition (§11). His two statements of method are the model the Footnote to Pearl names (Dead Letters, #1099, post #4, 10 May 2014): \"Belief & Technique for Modern Prose\", thirty items, written in a letter to Donald Allen in 1958 and printed in Evergreen Review in 1959, and \"Essentials of Spontaneous Prose\", printed in the Black Mountain Review in 1957 and in Evergreen Review in 1958, whose word for what spontaneous prose does to its reader, \"telepathic\", the Footnote takes into its title. His works are in copyright: those published before 1964 needed renewal, which is to be checked work by work; the later works run ninety-five years from publication.",
  works=[("Jack Kerouac","The Town and the City","Harcourt, Brace",1950,us(1950,True)),
         ("Jack Kerouac","Essentials of Spontaneous Prose, in Black Mountain Review 7","Black Mountain College",1957,us(1957,True)),
         ("Jack Kerouac","On the Road","Viking Press",1957,us(1957,True)),
         ("Jack Kerouac","The Subterraneans","Grove Press",1958,us(1958,True)),
         ("Jack Kerouac","The Dharma Bums","Viking Press",1958,us(1958,True)),
         ("Jack Kerouac","Essentials of Spontaneous Prose, in Evergreen Review 2.5","Grove Press",1958,us(1958,True)),
         ("Jack Kerouac","Belief & Technique for Modern Prose: List of Essentials, in Evergreen Review 2.8","Grove Press",1959,us(1959,True)),
         ("Jack Kerouac","Doctor Sax","Grove Press",1959,us(1959,True)),
         ("Jack Kerouac","Mexico City Blues","Grove Press",1959,us(1959,True)),
         ("Jack Kerouac","Book of Dreams","City Lights",1961,us(1961,True)),
         ("Jack Kerouac","Big Sur","Farrar, Straus and Cudahy",1962,us(1962,True)),
         ("Jack Kerouac","Visions of Cody","McGraw-Hill",1972,us(1972)),
         ("Jack Kerouac","Selected Letters, 1957–1969, ed. Ann Charters (the letter of 1958 to Donald Allen)","Viking",1999,"2040-01-01, seventy years after the author's death, for matter first published after 1977; the editor's apparatus under its own terms"),
         ("Jack Kerouac","On the Road: The Original Scroll, ed. Howard Cunnell","Viking",2007,"2040-01-01, seventy years after the author's death; the editors' apparatus under its own terms")],
  wanted="Wanted: the two statements of method first, in their first printings (Black Mountain Review 7, 1957; Evergreen Review 2.5, 1958, and 2.8, 1959), and the 1958 letter to Donald Allen in which the list was written; the renewal record of each work published before 1964, which decides when it opens. Until then the shelf describes the list and cites it by item number (Belief & Technique for Telepathic Prose: A Critical Edition, §7).",
  shelf="Beside Allen Ginsberg's declared absence (28/03), whose Howl and Other Poems is dedicated to him; Whitman (03/01); and Pearl and Other Poems (03/02), whose Footnote takes his title and whose Jack Feist stands in his place.")
lic = {"payload": "The declaration is the archive's own, CC-BY-4.0. The works it names are not held.", "record": "CC-BY-4.0 applies to this seat record only."}
seat = ST / s["corpus"]; (seat / "declared").mkdir(parents=True, exist_ok=True)
W = [dict(author=a, title=t, first_publisher=p, first_published=y, opens=o) for a, t, p, y, o in s["works"]]
doc = {"declared_absence": s["title"], "kind": "copyright", "rights": s["holder"], "works": W, "wanted": s["wanted"],
       "on_the_shelf": s["shelf"], "note": "This seat holds no text of the works it names. The dates follow the terms stated; they are not legal advice."}
(seat / "declared/absence.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
md = [f"# {s['title']}", "", s["why"], "", f"Rights: {s['holder']}", "", "| Author | Work | First publisher | Year | Opens |", "|---|---|---|---|---|"]
md += [f"| {w['author']} | {w['title']} | {w['first_publisher']} | {w['first_published'] or '—'} | {w['opens']} |" for w in W]
md += ["", s["wanted"], "", s["shelf"], "", doc["note"]]
(seat / "declared/absence.md").write_text("\n".join(md) + "\n", encoding="utf-8")
src = {"corpus": s["corpus"], "seat": "EA-CORPORA-29/01 (seated 2026-10-28; the twenty-ninth seating's deposit pending)", "title": s["title"],
       "edition": "No edition held. The seat holds the declaration of what it would hold: declared/absence.json and declared/absence.md.",
       "language": s["lang"], "license": lic, "fetched": "2026-10-28",
       "origin": {"items": [{"source": "Alexanarch deposit", "file": "declared/absence.json"}, {"source": "Alexanarch deposit", "file": "declared/absence.md"}],
                  "fetched": "2026-10-28", "transport": "written in session (Transport D); No-Double-Draw"},
       "works": {"count": 0, "units": f"no works held; {len(W)} declared", "list": []},
       "normalization": "None: the declaration is held as written.",
       "scope": "Declared, not seated: " + "; ".join(f"{w['author']}, {w['title']}" + (f" ({w['first_publisher']}, {w['first_published']})" if w['first_published'] else "") + f", opens: {w['opens']}" for w in W) + ". " + s["wanted"],
       "declared_absences": W, "verified_loci": [], "loci_not_found": [], "lines_total": 0,
       "why_seated": s["why"], "spine": "EA-CORPORA-29 (deposit pending; to be bundled into the next EA-CORPORA deposit, at the operator's ruling of 2026-10-28)",
       "ruling": "A declared absence: the works named, with their rights and opening dates, and no text (MANUS, 2026-10-28)."}
(seat / "source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
m = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(seat).as_posix()}" for p in sorted(seat.rglob('*')) if p.is_file() and p.name not in ('MANIFEST.sha256', 'source.json')]
(seat / "MANIFEST.sha256").write_text("\n".join(m) + "\n")
print(s["corpus"], len(W), "declared")
