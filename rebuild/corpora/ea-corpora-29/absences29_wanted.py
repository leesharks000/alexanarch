#!/usr/bin/env python3
"""EA-CORPORA-29 (session tool): ars-poetica-wanted (29/06), a declared absence in the form of absences29.py — the
arts of poetry the twenty-ninth seating could not hold: the copyrighted moderns, the Language writers, conceptual
writing, the contemporary arts of poetry, and public-domain works for which no copy could be fetched.
    python3 absences29_wanted.py <stage>"""
import json, hashlib, pathlib, sys
ST = pathlib.Path(sys.argv[1])
REN = " if its copyright was renewed (a United States work published before 1964 needed renewal; the renewal is to be checked)"
def us(y, renew=False):
    return f"{y + 96}-01-01" + (REN if renew else "")
def fo(y):
    return f"{y + 96}-01-01 in the United States (ninety-five years from first publication abroad)"
def life(d):
    return f"{d + 71}-01-01, seventy years after the author's death"
LIVING = "seventy years after the author's death (living author)"
PD = "open now (public domain in the United States); wanted: no fetchable copy found this session"

W = [
 # Public domain, wanted
 ("Public domain, no copy found", "William Carlos Williams", "Spring and All", "Contact Publishing Co., Paris", 1923, PD),
 ("Public domain, no copy found", "Gertrude Stein", "Composition as Explanation", "Hogarth Press, London", 1926, PD),
 ("Public domain, no copy found", "André Breton", "Manifeste du surréalisme. Poisson soluble", "Éditions du Sagittaire, Kra, Paris", 1924, PD),
 ("Public domain, no copy found", "Tristan Tzara", "Sept manifestes Dada", "Jean Budry, Paris", 1924, PD),
 ("Public domain, no copy found", "Mina Loy", "Aphorisms on Futurism, in Camera Work 45", "Alfred Stieglitz, New York", 1914, PD),
 ("Public domain, no copy found", "Mário de Andrade", "Paulicéa desvairada, with the Prefácio interessantíssimo", "Casa Mayença, São Paulo", 1922, PD),
 ("Public domain, no copy found", "Oswald de Andrade", "Manifesto Antropófago, in Revista de Antropofagia 1", "São Paulo", 1928, PD),
 ("Public domain, no copy found", "Rainer Maria Rilke", "Briefe an einen jungen Dichter", "Insel-Verlag, Leipzig", 1929, PD + " (the Internet Archive copies are access-restricted)"),
 ("Public domain, no copy found", "西脇順三郎 (Nishiwaki Junzaburō)", "超現実主義詩論 (Surrealist Poetics)", "厚生閣書店, Tokyo", 1929, PD + "; in copyright in Japan until 2053"),
 ("Public domain, no copy found", "Zeami Motokiyo", "風姿花伝 (Fūshikaden), in a public-domain edition", "", None, PD),
 ("Public domain, no copy found", "Moses ibn Ezra", "Kitāb al-muḥāḍara wa-l-mudhākara; Hebrew tr. B. Halper, Shirat Yisrael", "A. J. Stybel, Leipzig", 1924, PD),
 # The copyrighted moderns
 ("Modern", "Pablo Neruda", "Arte poética, in Residencia en la tierra (1925–1935)", "Cruz y Raya, Madrid", 1935, fo(1935)),
 ("Modern", "Paul Valéry", "Poésie et pensée abstraite", "Clarendon Press, Oxford", 1939, fo(1939)),
 ("Modern", "Marina Tsvetaeva", "Искусство при свете совести (Art in the Light of Conscience)", "Современные записки, Paris", 1932, fo(1932)),
 ("Modern", "Ai Qing (艾青)", "詩論 (On Poetry)", "Guilin", 1941, fo(1941)),
 ("Modern", "Wallace Stevens", "Of Modern Poetry, in Parts of a World", "Alfred A. Knopf", 1942, us(1942, True)),
 ("Modern", "Federico García Lorca", "Juego y teoría del duende (lecture of 1933)", "", 1942, fo(1942) + "; the date of first printing to be checked"),
 ("Modern", "Aimé Césaire", "Poésie et connaissance, in Tropiques 12", "Fort-de-France", 1945, fo(1945)),
 ("Modern", "Raymond Queneau", "Exercices de style", "Gallimard", 1947, fo(1947)),
 ("Modern", "Isidore Isou", "Introduction à une nouvelle poésie et à une nouvelle musique", "Gallimard", 1947, fo(1947)),
 ("Modern", "Charles Olson", "Projective Verse, in Poetry New York 3", "New York", 1950, us(1950, True)),
 ("Modern", "Gottfried Benn", "Probleme der Lyrik", "Limes Verlag, Wiesbaden", 1951, fo(1951)),
 ("Modern", "Eugen Gomringer", "vom vers zur konstellation", "", 1954, fo(1954) + "; the place of first printing to be checked"),
 ("Modern", "Octavio Paz", "El arco y la lira", "Fondo de Cultura Económica, México", 1956, fo(1956)),
 ("Modern", "Augusto de Campos, Décio Pignatari, Haroldo de Campos", "plano-piloto para poesia concreta, in Noigandres 4", "São Paulo", 1958, fo(1958)),
 ("Modern", "Jorge Luis Borges", "Arte poética, in El hacedor", "Emecé, Buenos Aires", 1960, fo(1960)),
 ("Modern", "Paul Celan", "Der Meridian", "S. Fischer, Frankfurt am Main", 1961, fo(1961)),
 ("Modern", "Frank O'Hara", "Personism: A Manifesto, in Yugen 7", "Totem Press, New York", 1961, us(1961, True)),
 ("Modern", "Nazik al-Malaʾika (نازك الملائكة)", "قضايا الشعر المعاصر (Issues of Contemporary Poetry)", "Baghdad", 1962, fo(1962) + "; the first publisher to be checked"),
 ("Modern", "Denise Levertov", "Some Notes on Organic Form, in Poetry 106.6", "Modern Poetry Association, Chicago", 1965, us(1965)),
 ("Modern", "Amiri Baraka (LeRoi Jones)", "Black Art, in Black Magic: Collected Poetry 1961–1967", "Bobbs-Merrill", 1969, us(1969)),
 ("Modern", "Robert Duncan", "Towards an Open Universe, in Poets on Poetry, ed. Howard Nemerov", "Basic Books", 1966, us(1966)),
 ("Modern", "Osip Mandelstam", "Разговор о Данте (Conversation about Dante; written 1933)", "Искусство, Moscow", 1967, fo(1967)),
 ("Modern", "Czesław Miłosz", "Ars poetica?, in Miasto bez imienia", "Instytut Literacki, Paris", 1969, fo(1969)),
 ("Modern", "Kim Su-yeong (김수영)", "시여, 침을 뱉어라 (Poetry, Spit!)", "Seoul", 1968, fo(1968)),
 ("Modern", "Adonis (أدونيس)", "مقدمة للشعر العربي (Introduction to Arab Poetry)", "Dār al-ʿAwda, Beirut", 1971, fo(1971)),
 ("Modern", "Adrienne Rich", "When We Dead Awaken: Writing as Re-Vision, in College English 34.1", "NCTE", 1972, us(1972)),
 ("Modern", "Oulipo", "La Littérature potentielle", "Gallimard", 1973, fo(1973)),
 ("Modern", "Audre Lorde", "Poetry Is Not a Luxury, in Chrysalis 3", "Los Angeles", 1977, us(1977)),
 ("Modern", "Jack Spicer", "The Vancouver Lectures (1965), in The House That Jack Built, ed. Peter Gizzi", "Wesleyan University Press", 1998, life(1965)),
 # Language writing
 ("Language writing", "Bruce Andrews and Charles Bernstein, eds.", "The L=A=N=G=U=A=G=E Book", "Southern Illinois University Press", 1984, LIVING),
 ("Language writing", "Lyn Hejinian", "The Rejection of Closure, in Poetics Journal 4", "Berkeley", 1984, LIVING),
 ("Language writing", "Susan Howe", "My Emily Dickinson", "North Atlantic Books", 1985, LIVING),
 ("Language writing", "Barrett Watten", "Total Syntax", "Southern Illinois University Press", 1985, LIVING),
 ("Language writing", "Steve McCaffery", "North of Intention: Critical Writings 1973–1986", "Roof Books", 1986, LIVING),
 ("Language writing", "Ron Silliman", "The New Sentence", "Roof Books", 1987, LIVING),
 ("Language writing", "Charles Bernstein", "Artifice of Absorption, in A Poetics", "Harvard University Press", 1992, LIVING),
 # Elsewhere, after 1978
 ("After 1978", "Kamau Brathwaite", "History of the Voice", "New Beacon Books, London", 1984, life(2020)),
 ("After 1978", "Joseph Brodsky", "Uncommon Visage (Nobel lecture)", "Nobel Foundation", 1987, life(1996)),
 ("After 1978", "Édouard Glissant", "Poétique de la Relation", "Gallimard", 1990, life(2011)),
 ("After 1978", "Alice Notley", "The Poetics of Disobedience", "", 1998, LIVING),
 ("After 1978", "Christian Bök", "ʼPataphysics: The Poetics of an Imaginary Science", "Northwestern University Press", 2002, LIVING),
 # Conceptual writing and the contemporary
 ("Conceptual writing", "Vanessa Place and Robert Fitterman", "Notes on Conceptualisms", "Ugly Duckling Presse", 2009, LIVING),
 ("Conceptual writing", "Craig Dworkin and Kenneth Goldsmith, eds.", "Against Expression: An Anthology of Conceptual Writing", "Northwestern University Press", 2011, LIVING),
 ("Conceptual writing", "Kenneth Goldsmith", "Uncreative Writing", "Columbia University Press", 2011, LIVING),
 ("Contemporary", "Mary Ruefle", "Madness, Rack, and Honey", "Wave Books", 2012, LIVING),
 ("Contemporary", "Lisa Robertson", "Nilling", "BookThug", 2012, LIVING),
 ("Contemporary", "Cathy Park Hong", "Delusions of Whiteness in the Avant-Garde, in Lana Turner 7", "", 2014, LIVING),
 ("Contemporary", "Ben Lerner", "The Hatred of Poetry", "Farrar, Straus and Giroux", 2016, LIVING),
]
title = "Ars Poetica, wanted — a declared absence: the copyrighted moderns, the Language writers, conceptual writing and the contemporary arts of poetry, with the public-domain arts no copy could be found for"
why = ("The arts of poetry the twenty-ninth seating could not hold, declared beside the ones it holds (ars-poetica, 29/04; avant-garde-ii, 29/05), at the author's direction to "
       "'go further into language poetry and contemporary ars poetica for wanted' (2026-10-28). Most are in copyright and open on the dates given; eleven are open now and wanted "
       "because no copy could be fetched this session. The list is a beginning: each entry names what would be seated, and the shelf grows as the works open or the copies are found.")
wanted = ("Wanted: the public-domain entries first, as scans of their first printings; then the moderns as they open, and permission from living authors and estates "
          "for the Language, conceptual and contemporary works, which the library would seat beside their predecessors here.")
shelf = ("Beside ars-poetica (29/04), avant-garde-ii (29/05) and telepathic-prose (29/07); the declared absences of Allen Ginsberg (28/03), Anne Carson (28/04), "
         "Tao Lin (28/05) and Jack Kerouac (29/01).")
seat = ST / "ars-poetica-wanted"; (seat / "declared").mkdir(parents=True, exist_ok=True)
L = [dict(**{"class": c}, author=a, title=t, first_publisher=p, first_published=y, opens=o) for c, a, t, p, y, o in W]
doc = {"declared_absence": title, "kind": "copyright, and copies not found", "rights": "The authors, their estates and first publishers, as named.", "works": L,
       "wanted": wanted, "on_the_shelf": shelf, "note": "This seat holds no text of the works it names. The dates follow the terms stated; they are not legal advice."}
(seat / "declared/absence.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
md = [f"# {title}", "", why, "", "| Class | Author | Work | First publisher | Year | Opens |", "|---|---|---|---|---|---|"]
md += [f"| {w['class']} | {w['author']} | {w['title']} | {w['first_publisher'] or '—'} | {w['first_published'] or '—'} | {w['opens']} |" for w in L]
md += ["", wanted, "", shelf, "", doc["note"]]
(seat / "declared/absence.md").write_text("\n".join(md) + "\n", encoding="utf-8")
src = {"corpus": "ars-poetica-wanted", "seat": "EA-CORPORA-29/06", "title": title,
       "edition": "No edition held. The seat holds the declaration of what it would hold: declared/absence.json and declared/absence.md.",
       "language": "mul", "license": {"payload": "The declaration is the archive's own, CC-BY-4.0. The works it names are not held.", "record": "CC-BY-4.0 applies to this seat record only."},
       "fetched": "2026-10-28",
       "origin": {"items": [{"source": "Alexanarch deposit", "file": "declared/absence.json"}, {"source": "Alexanarch deposit", "file": "declared/absence.md"}],
                  "fetched": "2026-10-28", "transport": "written in session (Transport D); No-Double-Draw"},
       "works": {"count": 0, "units": f"no works held; {len(L)} declared", "list": []},
       "normalization": "None: the declaration is held as written.",
       "scope": "Declared without text: " + "; ".join(f"{w['author']}, {w['title']}" + (f" ({w['first_publisher']}, {w['first_published']})" if w['first_published'] else "") + f", opens: {w['opens']}" for w in L) + ". " + wanted,
       "classes": sorted({w["class"] for w in L}, key=[x[0] for x in W].index),
       "declared_absences": L, "verified_loci": [], "loci_not_found": [], "lines_total": 0,
       "why_seated": why, "spine": "29/06", "ruling": "A declared absence: the works named, with their rights and opening dates, and no text (the author's direction of 2026-10-28).",
       "seating": "EA-CORPORA-29 (gathered; the deposit that assigns its AXN is pending)"}
(seat / "source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
m = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(seat).as_posix()}" for p in sorted(seat.rglob('*')) if p.is_file() and p.name not in ('MANIFEST.sha256', 'source.json')]
(seat / "MANIFEST.sha256").write_text("\n".join(m) + "\n")
print("ars-poetica-wanted", len(L), "declared")
