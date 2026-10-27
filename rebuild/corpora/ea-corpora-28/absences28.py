#!/usr/bin/env python3
"""EA-CORPORA-28 (session tool): the declared absences of the wanted seating. Each seat holds its declaration
(declared/absence.json and declared/absence.md), a source.json and a MANIFEST.sha256, and no text of the works it names.
    python3 absences28.py <stage>"""
import json, hashlib, pathlib, sys
ST = pathlib.Path(sys.argv[1])
Q = ("MANUS, 27 October 2026, after the twenty-seventh seating entered Deleuze and Guattari as a declared absence: "
     "\"and a declared absence/ wanted seating: hypatia, d & g, pkd, allen ginsberg, anne carson, and tao lin - including the mandalas. "
     "and paul klee. too many files and too many image copyright landmines.\" ")
US_PRE64 = "if its copyright was renewed (a United States work published before 1964 needed renewal; the renewal is to be checked)"
def us(y, renew=False):
    return f"{y+96}-01-01" + (f" {US_PRE64}" if renew else "")
SEATS = [
 dict(corpus="hypatia", seat="01", lang="grc (the witnesses declared)",
  title="Hypatia of Alexandria — a declared absence: the lost works named, and the witnesses in which her work and her life survive",
  kind="lost", holder="No rights holder: the works are lost, or survive only inside other authors' texts, where the attribution is a scholarly judgment.",
  why="Hypatia is entered as an absence of a different kind from the others of this seating. Her works are not held back by copyright; they are lost, or they survive inside other texts under other names. The Suda names a commentary on Diophantus, a commentary on Apollonius' Conics and an Astronomical Canon, and the heading of Theon's commentary on the third book of Ptolemy's Almagest credits the text to an edition \"revised by my daughter Hypatia, the philosopher\". What can be seated are the witnesses: Synesius' letters to her, the historians who record her life and death, and the texts in which her editing is believed to stand.",
  works=[("Hypatia","Commentary on Diophantus, Arithmetica","attributed by the Suda; the Greek books I–VI of the Arithmetica and the four books in Arabic are argued by some scholars to carry it",None,"lost or embedded"),
         ("Hypatia","Commentary on Apollonius of Perga, Conics","attributed by the Suda",None,"lost"),
         ("Hypatia","Astronomical Canon","attributed by the Suda; either an edition of Ptolemy's Handy Tables or a commentary on the Almagest",None,"lost"),
         ("Hypatia","Ptolemy, Almagest III, the revised text","credited in the heading of Theon's commentary on Book III",None,"embedded in the Almagest as transmitted")],
  wanted="Wanted, and open: Synesius of Cyrene's letters to and about her, in Greek (seven to her survive, none of hers to him); Socrates Scholasticus, Historia ecclesiastica VII.15; the Suda (Υ 166), with Damascius' Life of Isidore as it carries; Philostorgius and Hesychius as quoted; John of Nikiu's chronicle, in Ge'ez; the heading of Theon's commentary on Almagest III; Diophantus' Arithmetica in Tannery's edition (1893–1895). QUEUED.",
  shelf="Beside the shelf's Greek mathematics and philosophy: Euclid (20/04), Plato (01/08), Aristotle (04/01), Plotinus (04/02)."),
 dict(corpus="philip-k-dick", seat="02", lang="eng",
  title="Philip K. Dick — a declared absence: the novels, the late trilogy and the Exegesis named, with the stories already open",
  kind="copyright", holder="The estate of Philip K. Dick; the first publishers named.",
  why="Philip K. Dick (1928–1982) is entered as wanted. His novels and the Exegesis are in copyright: the works published before 1978 run ninety-five years from publication, those after it seventy years from his death, to 1 January 2053.",
  works=[("Philip K. Dick","Solar Lottery","Ace Books",1955,us(1955,True)),("Philip K. Dick","Time Out of Joint","J. B. Lippincott",1959,us(1959,True)),
         ("Philip K. Dick","The Man in the High Castle","G. P. Putnam's Sons",1962,us(1962,True)),("Philip K. Dick","Martian Time-Slip","Ballantine Books",1964,us(1964)),
         ("Philip K. Dick","The Three Stigmata of Palmer Eldritch","Doubleday",1965,us(1965)),("Philip K. Dick","Do Androids Dream of Electric Sheep?","Doubleday",1968,us(1968)),
         ("Philip K. Dick","Ubik","Doubleday",1969,us(1969)),("Philip K. Dick","Flow My Tears, the Policeman Said","Doubleday",1974,us(1974)),
         ("Philip K. Dick","A Scanner Darkly","Doubleday",1977,us(1977)),("Philip K. Dick","VALIS","Bantam Books",1981,"2053-01-01"),
         ("Philip K. Dick","The Divine Invasion","Timescape Books",1981,"2053-01-01"),("Philip K. Dick","The Transmigration of Timothy Archer","Timescape Books",1982,"2053-01-01"),
         ("Philip K. Dick","The Exegesis of Philip K. Dick, ed. Pamela Jackson and Jonathan Lethem","Houghton Mifflin Harcourt",2011,"2053-01-01")],
  wanted="Open now, and wanted for seating at the operator's word: thirteen stories of the early 1950s whose copyrights were not renewed, in Project Gutenberg's transcriptions from their magazine printings: Beyond Lies the Wub, The Gun, The Skull, The Crystal Crypt, The Defenders, Mr. Spaceship, Piper in the Woods, The Variable Man, Second Variety, The Eyes Have It, Beyond the Door, Tony and the Beetles, The Hanging Stranger (Project Gutenberg EBooks #28554, #29132, #30255, #28698, #28767, #32522, #32832, #32154, #32032, #31516, #28644, #40964, #41562).",
  shelf="Beside the shelf's Gnostic and Hermetic seats, which the late trilogy reads: the Coptic Gnostic texts (01/15), the Nag Hammadi library (02/15), the Corpus Hermeticum (22/01)."),
 dict(corpus="allen-ginsberg", seat="03", lang="eng",
  title="Allen Ginsberg — a declared absence: Howl, Kaddish and the books of poems to Death & Fame",
  kind="copyright", holder="The Allen Ginsberg Estate; the first publishers named.",
  why="Allen Ginsberg (1926–1997) is entered as wanted: the poet of the American line that runs from Whitman (03/01), whom \"A Supermarket in California\", in Howl and Other Poems, addresses. His books are in copyright: those published before 1978 run ninety-five years from publication, those after it seventy years from his death, to 1 January 2068.",
  works=[("Allen Ginsberg","Howl and Other Poems","City Lights",1956,us(1956,True)),("Allen Ginsberg","Kaddish and Other Poems 1958–1960","City Lights",1961,us(1961,True)),
         ("Allen Ginsberg","Empty Mirror: Early Poems","Totem Press / Corinth Books",1961,us(1961,True)),("Allen Ginsberg","Reality Sandwiches","City Lights",1963,us(1963,True)),
         ("Allen Ginsberg","Planet News","City Lights",1968,us(1968)),("Allen Ginsberg","The Fall of America: Poems of These States 1965–1971","City Lights",1973,us(1973)),
         ("Allen Ginsberg","Mind Breaths","City Lights",1977,us(1977)),("Allen Ginsberg","Plutonian Ode","City Lights",1982,"2068-01-01"),
         ("Allen Ginsberg","Collected Poems 1947–1980","Harper & Row",1984,"2068-01-01"),("Allen Ginsberg","White Shroud","Harper & Row",1986,"2068-01-01"),
         ("Allen Ginsberg","Cosmopolitan Greetings","HarperCollins",1994,"2068-01-01"),("Allen Ginsberg","Death & Fame","HarperFlamingo",1999,"2068-01-01")],
  wanted="Wanted: the recordings of the readings, held by their recorders and archives under their terms; the manuscripts at Stanford University Libraries.",
  shelf="Beside Whitman (03/01), Blake (19/04), whose voice Ginsberg heard in his Harlem vision of 1948, and the Millerite and Latter Day Saint seats of the American visionary line (24/01, 24/03)."),
 dict(corpus="anne-carson", seat="04", lang="eng (with the Greek she translates)",
  title="Anne Carson — a declared absence: the books from Eros the Bittersweet to The Gender of Sound, and the translations from the Greek",
  kind="copyright", holder="Anne Carson; the first publishers named.",
  why="Anne Carson (b. 1950), awarded the Nobel Prize in Literature on 8 October 2026, is entered as wanted. She is living, and her works open seventy years after her death. They stand on the shelf's own ground: If Not, Winter translates the Sappho the shelf holds as fragment 31 (01/10), Autobiography of Red is built on Stesichorus, Economy of the Unlost reads Simonides with Celan.",
  works=[(a,t,p,y,"seventy years after the author's death (the author is living)") for a,t,p,y in [
         ("Anne Carson","Eros the Bittersweet","Princeton University Press",1986),("Anne Carson","Short Talks","Brick Books",1992),
         ("Anne Carson","Glass, Irony, and God","New Directions",1995),("Anne Carson","Plainwater","Alfred A. Knopf",1995),
         ("Anne Carson","Autobiography of Red","Alfred A. Knopf",1998),("Anne Carson","Economy of the Unlost","Princeton University Press",1999),
         ("Anne Carson","Men in the Off Hours","Alfred A. Knopf",2000),("Anne Carson","The Beauty of the Husband","Alfred A. Knopf",2001),
         ("Anne Carson (trans.)","If Not, Winter: Fragments of Sappho","Alfred A. Knopf",2002),("Anne Carson","Decreation","Alfred A. Knopf",2005),
         ("Anne Carson (trans.)","Grief Lessons: Four Plays by Euripides","New York Review Books",2006),("Anne Carson (trans.)","An Oresteia","Farrar, Straus and Giroux",2009),
         ("Anne Carson","Nox","New Directions",2010),("Anne Carson","Antigonick","New Directions",2012),("Anne Carson","Red Doc>","Alfred A. Knopf",2013),
         ("Anne Carson","Float","Alfred A. Knopf",2016),("Anne Carson","Norma Jeane Baker of Troy","Oberon Books",2019),
         ("Anne Carson","H of H Playbook","New Directions",2021),("Anne Carson","Wrong Norma","New Directions",2024),("Anne Carson","The Gender of Sound","Spiral House",2025)]],
  wanted="Wanted: whatever Carson or her publishers release under an open licence. The Greek she translates is partly on the shelf already, and the rest is open: Stesichorus, Simonides, Euripides, Aeschylus and Sophocles in their Greek, QUEUED.",
  shelf="Beside Sappho (01/10), Catullus (01/02), Longinus (01/06) and the literary papyri (01/11)."),
 dict(corpus="tao-lin", seat="05", lang="eng",
  title="Tao Lin — a declared absence: the books from you are a little bit happier than i am to Leave Society, and the mandalas",
  kind="copyright", holder="Tao Lin; the first publishers named. The mandalas: Tao Lin, the drawings and their images.",
  why="Tao Lin (b. 1983) is entered as wanted, the mandalas with the books. He is living, and his works open seventy years after his death. The mandalas, which he began drawing in 2014 and first sold on eBay, are images whose every reproduction is his to license.",
  works=[(a,t,p,y,"seventy years after the author's death (the author is living)") for a,t,p,y in [
         ("Tao Lin","this emotion was a little e-book","Bear Parade",2006),("Tao Lin","you are a little bit happier than i am","Action Books",2006),
         ("Tao Lin","Today the Sky Is Blue and White with Bright Blue Spots and a Small Pale Moon and I Will Destroy Our Relationship Today","Bear Parade",2006),
         ("Tao Lin","Eeeee Eee Eeee","Melville House",2007),("Tao Lin","Bed","Melville House",2007),("Tao Lin","cognitive-behavioral therapy","Melville House",2008),
         ("Tao Lin","Shoplifting from American Apparel","Melville House",2009),("Tao Lin","Richard Yates","Melville House",2010),("Tao Lin","Taipei","Vintage Books",2013),
         ("Tao Lin","Selected Tweets","Short Flight/Long Drive Books",2015),("Tao Lin","Trip: Psychedelics, Alienation, and Change","Vintage Books",2018),
         ("Tao Lin","Leave Society","Vintage Books",2021),("Tao Lin","the mandalas (drawings, from 2014)","sold by the artist",2014)]],
  wanted="Wanted: whatever Lin releases openly; his writing on the web as he dates and publishes it, under his terms.",
  shelf="Beside the shelf's machine-authored and networked texts (15/01) and the avant-garde (18/01–18/10)."),
 dict(corpus="paul-klee", seat="06", lang="deu",
  title="Paul Klee — a declared absence: the pictures, the Pädagogisches Skizzenbuch and the writings, held back by their number and by the rights in their photographs",
  kind="volume and images", holder="The works: in the public domain in Switzerland and the European Union since 1 January 2011 (Klee died in 1940). The photographs of them: their museums, archives and photographers, under terms that differ by holder and by country.",
  why="Paul Klee (1879–1940) is entered as wanted for a reason of his own: \"too many files and too many image copyright landmines.\" His work runs to some ten thousand pictures, scattered across collections whose reproductions carry their own claims, and the shelf takes no file whose licence cannot be verified at the file.",
  works=[("Paul Klee","Schöpferische Konfession, in Tribüne der Kunst und Zeit XIII","Erich Reiss",1920,"open (published before 1931)"),
         ("Paul Klee","Pädagogisches Skizzenbuch (Bauhausbücher 2)","Albert Langen",1925,"open (published before 1931)"),
         ("Paul Klee","Über die moderne Kunst (the Jena lecture of 1924)","Benteli",1945,"1 January 2041 in the United States, if its term was restored"),
         ("Paul Klee, ed. Jürg Spiller","Das bildnerische Denken","Benno Schwabe",1956,"the editor's apparatus under its own terms"),
         ("Paul Klee, ed. Felix Klee","Tagebücher 1898–1918","DuMont Schauberg",1957,"the editor's apparatus under its own terms"),
         ("Paul Klee","the pictures (about ten thousand works, 1883–1940)","their collections",None,"the works open; the photographs under their holders' terms")],
  wanted="Wanted, and open: the Pädagogisches Skizzenbuch (1925) and the Schöpferische Konfession (1920) in their first printings, with their drawings, from a scan whose licence is verified at the file. The pictures wait on a source whose images carry an open licence of their own.",
  shelf="Beside the Bauhaus decade's avant-garde (18/03 Futurism, 18/04 Dada, 18/08 visual poetry), and Blake's illuminated books (19/04)."),
]
lic = {"payload": "The declaration is the archive's own, CC-BY-4.0. The works it names are not held.", "record": "CC-BY-4.0 applies to this seat record only."}
for s in SEATS:
    seat = ST / s["corpus"]; (seat / "declared").mkdir(parents=True, exist_ok=True)
    W = [dict(author=a, title=t, first_publisher=p, first_published=y, opens=o) for a, t, p, y, o in s["works"]]
    doc = {"declared_absence": s["title"], "kind": s["kind"], "rights": s["holder"], "works": W, "wanted": s["wanted"],
           "on_the_shelf": s["shelf"], "note": "This seat holds no text of the works it names. The dates follow the terms stated; they are not legal advice."}
    (seat / "declared/absence.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    md = [f"# {s['title']}", "", s["why"], "", f"Rights: {s['holder']}", "", "| Author | Work | First publisher | Year | Opens |", "|---|---|---|---|---|"]
    md += [f"| {w['author']} | {w['title']} | {w['first_publisher']} | {w['first_published'] or '—'} | {w['opens']} |" for w in W]
    md += ["", s["wanted"], "", s["shelf"], "", doc["note"]]
    (seat / "declared/absence.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    src = {"corpus": s["corpus"], "seat": f"EA-CORPORA-28/{s['seat']}", "title": s["title"],
           "edition": "No edition held. The seat holds the declaration of what it would hold: declared/absence.json and declared/absence.md.",
           "language": s["lang"], "license": lic, "fetched": "2026-10-27",
           "origin": {"items": [{"source": "Alexanarch deposit", "file": "declared/absence.json"}, {"source": "Alexanarch deposit", "file": "declared/absence.md"}],
                      "fetched": "2026-10-27", "transport": "written in session (Transport D); No-Double-Draw"},
           "works": {"count": 0, "units": f"no works held; {len(W)} declared", "list": []},
           "normalization": "None: the declaration is held as written.",
           "scope": "Declared, not seated: " + "; ".join(f"{w['author']}, {w['title']}" + (f" ({w['first_publisher']}, {w['first_published']})" if w['first_published'] else "") + f", opens: {w['opens']}" for w in W) + ". " + s["wanted"],
           "declared_absences": W, "verified_loci": [], "loci_not_found": [], "lines_total": 0,
           "why_seated": Q + s["why"], "spine": "EA-CORPORA-28 (#1713)",
           "ruling": "A declared absence, the wanted seating: the works named, with their rights and opening dates, and no text (MANUS, 2026-10-27)."}
    (seat / "source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    m = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(seat).as_posix()}" for p in sorted(seat.rglob('*')) if p.is_file() and p.name not in ('MANIFEST.sha256', 'source.json')]
    (seat / "MANIFEST.sha256").write_text("\n".join(m) + "\n")
    print(s["corpus"], len(W), "declared")
