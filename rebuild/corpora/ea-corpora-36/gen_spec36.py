"""EA-CORPORA-36 spec generator: Sappho's reception, with the future-reader frameworks, in the open record. Twenty-seven seats, each
in its original language, at the operator's word of 2026-11-07 ("i think we need a sappho reception history ea-corpora, whatever's public.
translators, scholars ..."; "sappho reception history + future reader frameworks and related"). Part A (36/01–36/18) holds the translators,
editors and critics of Sappho from Hall's Longinus (1652) to Cox (1925); Part B (36/19–36/27) holds the future-reader strata of #1548 Part II
that the library did not already hold. Strata already seated are entered as cross-references (xref36.py); works behind pay-, access- and
rights-walls are entered as declared absences (absences36.py).   python3 gen_spec36.py"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
RULING = ("Lee Sharks, 2026-11-07: \"i think we need a sappho reception history ea-corpora, whatever's public. translators, scholars. theres some "
          "ground work in the archive, notes towards a future reader i believe. the seating can include everything thats publicly available as well "
          "as declared absences and pointers for material behind pay- and access- and rights-walls\"; and: \"sappho reception history + future reader "
          "frameworks and related\".")
SEATING = "EA-CORPORA-36, the thirty-sixth seating: Sappho's reception and the future reader, 1652–1993, 2026-11-07"
RESEARCH = ("The revision of Closing the Fragment (v7, a draft of 2026-11-07 for Alexanarch), whose §6 controls the January composition against the "
            "translators from Hall (1652) to Carson and whose §8 declares an exposure-checked panel; and the Sappho Future Reader framework, whose "
            "groundwork is Research Notes Towards the Future Reader (#1548: Part I the scholarly field, Part II the future reader in twelve strata), "
            "and whose reading by a signed-out ChatGPT on 2026-11-07 is seated as capture 0C3D "
            "(sappho-future-reader-framework-constitutive-materials-chatgpt-20261107).")
NORM = ("Originals as fetched under original/: Internet Archive text layers (_djvu.txt) as served; Project Gutenberg plain text as served, header "
        "and licence kept; Perseus TEI as served at a pinned commit; the Text Creation Partnership's TEI as served; a Wikisource page as served with "
        "its revision id. text/<slug>.* derived by code: OCR and Gutenberg text with line endings normalized; TEI reduced to lines (the TCP's "
        "end-of-line hyphen marks removed so the word is joined, original spelling and long s kept); Wikisource parser output with navigation "
        "dropped. No text corrected by hand; the loci keep the OCR's readings (long s read as f, double spaces, broken accents).")
GB = lambda n: f"https://www.gutenberg.org/cache/epub/{n}/pg{n}.txt"
PERSEUS_L = "https://raw.githubusercontent.com/PerseusDL/canonical-latinLit/8b536bdf3ed1f43494055efe112433b4a58eab67/"
US_ONLY = lambda yr, who: (f"Public domain in the United States: published {yr}, before 1931. Outside the United States the term runs from "
                           f"{who}; the seat is held for the United States and the record says so.")


def ia(slug, work, ident, cls):
    return {"kind": "ia", "slug": slug, "work": work, "identifier": ident, "files": [f"{ident}_djvu.txt"], "class": cls}


def gb(slug, work, n, cls):
    return {"kind": "text", "slug": slug, "work": work, "url": GB(n), "path": f"gutenberg/pg{n}.txt",
            "source": f"Project Gutenberg #{n}", "licence": "The Project Gutenberg License (header and footer kept as served)", "class": cls}


A = "Sappho's reception, 1652–1925"
B = "the future reader"
SEATS = [
 # ---- Part A: the translators, editors and critics ----
 ("hall-peri-hypsous-1652", "01", "John Hall, Peri hypsous, or Dionysius Longinus of the height of eloquence (London, 1652), the first English Longinus", "eng",
  "Public domain everywhere (1652; Hall died 1656). The TCP transcription is released under CC0 1.0, as its <availability> states.",
  [{"kind": "tcp", "slug": "hall-1652", "work": "J. Hall, Peri hypsous (London: Roger Daniel for Francis Eaglesfield, 1652), EEBO-TCP A88516",
    "url": "https://raw.githubusercontent.com/textcreationpartnership/A88516/master/A88516.xml", "path": "tcp/A88516.xml", "tcp_id": "A88516",
    "stc": "Wing L2999; Thomason E1294_2; ESTC R202778", "class": A}],
  "The book whole, as the Text Creation Partnership keyboarded it.",
  "The first English rendering of fr. 31, inside Longinus's chapter 10, in four stanzas, and the fifth stanza's opening carried over as a closing line: "
  "'Yet ſince I'me wretched I muſt dare.' (Closing the Fragment v7 §6.)"),
 ("boileau-traite-du-sublime-1683", "02", "N. Boileau-Despréaux, Traité du sublime ou du merveilleux dans le discours, traduit du grec de Longin, in Œuvres diverses du sieur D*** (Paris, 1683)", "fra",
  "Public domain everywhere (1683; Boileau died 1711).",
  [ia("boileau-1683", "N. Boileau-Despréaux, Œuvres diverses du sieur D***, avec le Traité du sublime (Paris, 1683)", "bub_gb_DF2vAFjaG5YC", A)],
  "The volume whole. The first edition of the Traité (1674) was not located in an open text layer in session; this is the 1683 printing.",
  "The French fr. 31 of the Traité, ch. VIII, three quatrains and then the fifth stanza's opening as a closing line, that all must be hazarded, the version the Spectator quotes in 1711 and calls 'rather an Imitation than a Translation'."),
 ("spectator-229-1711", "03", "The Spectator, ed. H. Morley (London, 1891), vols. I–III, holding Addison's Nos. 223 and 229 (15 and 22 November 1711) with Ambrose Philips's fr. 1 and fr. 31", "eng",
  "Public domain everywhere (1711; Morley's edition 1891, Morley died 1894).",
  [gb("spectator-1891", "The Spectator, ed. H. Morley, 3 vols. (London: Routledge, 1891), Project Gutenberg #12030", 12030, A)],
  "The three volumes whole; Nos. 223 and 229 are the Sappho papers.",
  "Addison prints Boileau's French and Philips's English of fr. 31 in No. 229 and judges between them; Philips's four stanzas close 'I fainted, sunk, "
  "and dy'd away.' (v7 §6)."),
 ("pope-sapho-to-phaon", "04", "Alexander Pope, Sapho to Phaon (1712), from Ovid's Heroides XV, in The Poetical Works of Alexander Pope, ed. G. Gilfillan, vol. II (Edinburgh, 1856)", "eng",
  "Public domain everywhere (1712; Gilfillan's edition 1856).",
  [gb("pope-poetical-works-ii", "The Poetical Works of Alexander Pope, ed. G. Gilfillan, vol. II (1856), Project Gutenberg #9601", 9601, A)],
  "The volume whole; Sapho to Phaon is one poem in it. Ovid's Latin is seated at EA-CORPORA-29/03 (ovid, text/heroides.txt, poem 15).",
  "The Ovidian Sappho, the abandoned lover of Phaon, in the English the eighteenth century read her through; the epistle's Latin opens with the "
  "letter recognized by its hand, a reader addressed through the writing."),
 ("fawkes-anacreon-sappho-1760", "05", "Francis Fawkes, The Works of Anacreon, Sappho, Bion, Moschus and Musaeus (London, 1760)", "eng",
  "Public domain everywhere (1760; Fawkes died 1777).",
  [ia("fawkes-1760", "F. Fawkes, The Works of Anacreon, Sappho, Bion, Moschus and Musaeus (London, 1760)", "worksofanacreons00fawkuoft", A)],
  "The volume whole.", "Fawkes's Sappho, with a note judging the first three lines of Philips's version rough and awkward; his fr. 31 stands in "
  "the teaching gallery of thirteen English versions (v7 §6)."),
 ("welcker-sappho-1816", "06", "F. G. Welcker, Sappho von einem herrschenden Vorurtheil befreyt (Göttingen, 1816)", "deu",
  "Public domain everywhere (1816; Welcker died 1868).",
  [ia("welcker-1816", "F. G. Welcker, Sappho von einem herrschenden Vorurtheil befreyt (Göttingen, 1816), the Bayerische Staatsbibliothek copy", "10066488bsb", A)],
  "The volume whole. The Google scan (sapphovoneinemh00welcgoog) was fetched first and set aside: its OCR reads the Fraktur as noise; this copy's text layer reads it.", "The defence of Sappho's character, the poet 'freed of a ruling prejudice', which set the terms of the nineteenth-century "
  "debate; Mure's history (36/08) argues the other side."),
 ("merivale-poems-1838", "07", "J. H. Merivale, Poems Original and Translated, vol. I (London, 1838)", "eng",
  "Public domain everywhere (1838; Merivale died 1844).",
  [ia("merivale-1838-i", "J. H. Merivale, Poems Original and Translated, vol. I (London: Pickering, 1838)", "poemsoriginaltra01meri", A)],
  "Volume I whole (the 1813 'From Sappho. A Fragment' stands in it). Volume II's text layer returned an error at the Archive in session.",
  "Merivale's fr. 31 in four stanzas that end at the failing of sight and sound, one of the renderings Wharton reprints (v7 §5.3)."),
 ("mure-critical-history-1850", "08", "W. Mure, A Critical History of the Language and Literature of Antient Greece, vol. III (London, 1850)", "eng",
  "Public domain everywhere (1850; Mure died 1860).",
  [ia("mure-1850-iii", "W. Mure, A Critical History of the Language and Literature of Antient Greece, vol. III (London, 1850)", "criticalhistoryo03mureuoft", A)],
  "Volume III whole (book III, the lyric poets: Alcaeus, Sappho, Damophyla, Erinna).",
  "The Victorian prosecution of Sappho's character, which Welcker's defence had provoked, in the history the English schools read."),
 ("swinburne-poems-and-ballads-1866", "09", "A. C. Swinburne, Poems and Ballads (London, 1866)", "eng",
  "Public domain everywhere (1866; Swinburne died 1909).",
  [gb("swinburne-1866", "A. C. Swinburne, Poems and Ballads, First Series, Project Gutenberg #35402", 35402, A)],
  "The volume whole: Anactoria and Sapphics stand in it.", "Anactoria, Sappho given a dramatic monologue, and Sapphics, the stanza in English; "
  "Anactoria's speaker claims the future for the songs: 'Yea, though thou diest, I say I shall not die.'"),
 ("higginson-atlantic-essays-1871", "10", "T. W. Higginson, Atlantic Essays (Boston, 1871), with 'Sappho' (1871)", "eng",
  "Public domain everywhere (1871; Higginson died 1911).",
  [ia("higginson-1871", "T. W. Higginson, Atlantic Essays (Boston: Osgood, 1871)", "atlanticessays01higggoog", A)],
  "The volume whole; 'Sappho' is the essay of 1871.", "The American defence of Sappho, by Dickinson's correspondent and, with Todd, her first editor: the two "
  "ends of the future-reader genealogy meet in one editor."),
 ("symonds-studies-greek-poets-1873", "11", "J. A. Symonds, Studies of the Greek Poets (London, 1873)", "eng",
  "Public domain everywhere (1873; Symonds died 1893).",
  [ia("symonds-1873", "J. A. Symonds, Studies of the Greek Poets (London: Smith, Elder, 1873)", "cu31924022691822", A)],
  "The volume whole.", "Symonds on the Lesbian lyric, the critic whose fr. 31 Wharton prints (v7 §5.3), in the first series of his Studies."),
 ("vivien-sapho-1903", "12", "Renée Vivien, Sapho: traduction nouvelle avec le texte grec (Paris, 1903)", "fra",
  "Public domain everywhere (1903; Vivien died 1909).",
  [ia("vivien-1903", "R. Vivien, Sapho: traduction nouvelle avec le texte grec (Paris: Lemerre, 1903)", "saphotraduction00sappgoog", A)],
  "The volume whole.", "The French Sappho with the Greek facing, by a poet who answered the fragments in her own poems: fr. 31 given twice, as "
  "prose translation, which carries the fifth stanza's opening ('Mais il faut oser tout...'), and as the poem made from it."),
 ("carman-sappho-1904", "13", "Bliss Carman, Sappho: One Hundred Lyrics (Boston, 1904; the printing of 1907)", "eng",
  "Public domain in the United States (published 1904) and in Canada and the EU (Carman died 1929).",
  [gb("carman-1907", "B. Carman, Sappho: One Hundred Lyrics (1907 printing), Project Gutenberg #12389", 12389, A)],
  "The volume whole.", "The fragments completed as a hundred whole lyrics; Charles G. D. Roberts's introduction likens the method to restoring "
  "statues of Polyclitus or Praxiteles from a broken arm: closure as the stated method of a book."),
 ("wharton-sappho-1908", "14", "H. T. Wharton, Sappho: Memoir, Text, Selected Renderings and a Literal Translation, 5th edn (London, 1908)", "eng",
  "Public domain everywhere (1908; Wharton died 1895).",
  [gb("wharton-1908", "H. T. Wharton, Sappho, 5th edn (London and New York: John Lane, 1908), Project Gutenberg #57390", 57390, A)],
  "The volume whole, with the renderings Wharton chose and the Greek in Gutenberg's transliteration.",
  "The anthology the English tradition reached Sappho through, and the source the January composition's closing line aligns with (v7 §5.3)."),
 ("renderings-1910-1920", "15", "Two renderings: J. M. O'Hara, The Poems of Sappho: An Interpretative Rendition into English (Portland, 1910), and H. de Vere Stacpoole, Sappho: A New Rendering (London, 1920)", "eng",
  "Public domain in the United States (both published before 1931) and life-plus-seventy (O'Hara died 1944, Stacpoole 1951).",
  [gb("ohara-1910", "J. M. O'Hara, The Poems of Sappho (Portland: Smith & Sale, 1910), Project Gutenberg #42166", 42166, A),
   gb("stacpoole-1920", "H. de Vere Stacpoole, Sappho: A New Rendering (London: Hutchinson, 1920), Project Gutenberg #42543", 42543, A)],
  "Both volumes whole.", "Two English Sapphos of the generation before Lobel's edition (1925): an interpretative rendition and a new rendering, "
  "each with its own account of what a fragment asks of a translator."),
 ("wilamowitz-sappho-und-simonides-1913", "16", "U. von Wilamowitz-Moellendorff, Sappho und Simonides: Untersuchungen über griechische Lyriker (Berlin, 1913)", "deu",
  "Public domain everywhere (1913; Wilamowitz died 1931).",
  [ia("wilamowitz-1913", "U. von Wilamowitz-Moellendorff, Sappho und Simonides (Berlin: Weidmann, 1913)", "sapphoundsimonid00wilauoft", A)],
  "The volume whole.", "The German philology of Sappho in Wilamowitz's hands, with the reading of her circle that Parker's 'Sappho "
  "Schoolmistress' (1993) argues against."),
 ("robinson-sappho-and-her-influence-1924", "17", "D. M. Robinson, Sappho and Her Influence (Boston, 1924), Our Debt to Greece and Rome", "eng",
  US_ONLY(1924, "Robinson's death in 1958"),
  [ia("robinson-1924", "D. M. Robinson, Sappho and Her Influence (Boston: Marshall Jones, 1924)", "sapphoherinfluen0000davi", A)],
  "The volume whole.", "A reception history in the series Our Debt to Greece and Rome: appreciations ancient and modern, the life, and the "
  "influence on later poets named in its title."),
 ("cox-poems-of-sappho-1925", "18", "E. M. Cox, The Poems of Sappho, with Historical and Critical Notes, Translations, and a Bibliography (London and New York, 1925)", "eng",
  US_ONLY(1925, "Cox's death, which was not established in session"),
  [ia("cox-1925", "E. M. Cox, The Poems of Sappho (London: Williams & Norgate; New York: Scribner, 1925)", "poemsofsapphowit0000edwi", A)],
  "The volume whole.", "The Greek text with notes, translations and a bibliography of editions: the reception inventoried the year "
  "Lobel's edition appeared."),
 # ---- Part B: the future reader ----
 ("cicero-tusculanae", "19", "Cicero, Tusculanae Disputationes, ed. M. Pohlenz (Leipzig, 1918), via Perseus", "lat",
  "Perseus Digital Library TEI under CC BY-SA 4.0 (the packaging); Pohlenz's edition is in the public domain in the United States (published 1918).",
  [{"kind": "tei", "slug": "tusculanae", "work": "Cicero, Tusculanae Disputationes, ed. Pohlenz (Perseus phi0474.phi049, lat2)",
    "url": PERSEUS_L + "data/phi0474/phi049/phi0474.phi049.perseus-lat2.xml", "path": "perseus/phi0474.phi049.perseus-lat2.xml",
    "source": "PerseusDL/canonical-latinLit", "repository": "https://github.com/PerseusDL/canonical-latinLit",
    "commit": "8b536bdf3ed1f43494055efe112433b4a58eab67", "file": "data/phi0474/phi049/phi0474.phi049.perseus-lat2.xml", "class": B}],
  "The five books whole.", "Ennius's epitaph as Cicero quotes it, 'volito vivos per ora virum' (Tusc. 1.34): the poet living in the mouths of men, "
  "stratum IV of #1548's genealogy; the library's Cicero seat (EA-CORPORA-13/03) holds other works."),
 ("dante-commedia", "20", "Dante Alighieri, La Divina Commedia (Italian; the Project Gutenberg text)", "ita",
  "Public domain everywhere (Dante died 1321); the Gutenberg file under its licence.",
  [gb("commedia", "Dante, La Divina Commedia, complete, Project Gutenberg #1000", 1000, B)],
  "The poem whole.", "The addresses to the reader ('Pensa, lettor', Inf. 8.94 and after; 'O voi che siete in piccioletta barca', Par. 2.1), the "
  "corpus of Auerbach's 'Dante's Addresses to the Reader' (1954), stratum VI."),
 ("chaucer-troilus", "21", "Geoffrey Chaucer, Troilus and Criseyde (the Project Gutenberg text)", "enm",
  "Public domain everywhere (Chaucer died 1400); the Gutenberg file under its licence.",
  [gb("troilus", "Chaucer, Troilus and Criseyde, Project Gutenberg #257", 257, B)],
  "The poem whole.", "The envoi 'Go, litel book, go litel myn tragedie' (5.1786) and the stanza after it on scribal miswriting: the book "
  "dispatched to readers it cannot choose, with its transmission in view, stratum VI."),
 ("shakespeare-sonnets", "22", "William Shakespeare, Sonnets (1609; the Project Gutenberg text in modern spelling)", "eng",
  "Public domain everywhere (1609); the Gutenberg file under its licence.",
  [gb("sonnets", "Shakespeare's Sonnets, Project Gutenberg #1041 (modern spelling; the quarto's numbering)", 1041, B)],
  "The 154 sonnets whole. The 1609 quarto's own spelling is not seated; this text is modernized.",
  "The English monumentum: 18, 55, 65, 107, and 81's 'Which eyes not yet created shall o'er-read', the future reader stated as plainly as the "
  "language allows, stratum VI."),
 ("milton-paradise-lost", "23", "John Milton, Paradise Lost (1674 text; the Project Gutenberg text)", "eng",
  "Public domain everywhere (1674); the Gutenberg file under its licence.",
  [gb("paradise-lost", "Milton, Paradise Lost, Project Gutenberg #26", 26, B)],
  "The poem whole.", "'fit audience find, though few' (7.31): the future reader as select, stratum VI."),
 ("romantic-posterity", "24", "The Romantic culture of posterity in its own words: Wordsworth (1815), Keats (1818), Shelley (1821), Stendhal (1839)", "eng, fra",
  "Public domain everywhere (Wordsworth died 1850, Keats 1821, Shelley 1822, Stendhal 1842; Grosart's edition 1876, Colvin's 1891); the Gutenberg files under their licence.",
  [gb("wordsworth-prose", "The Prose Works of William Wordsworth, ed. A. B. Grosart, 3 vols. (London, 1876), Project Gutenberg #16550 (the letters to Lady Beaumont, 1807, and the Essay, Supplementary to the Preface, 1815)", 16550, B),
   gb("keats-letters", "Letters of John Keats to His Family and Friends, ed. S. Colvin (London, 1891), Project Gutenberg #35698", 35698, B),
   gb("shelley-defence", "P. B. Shelley, A Defence of Poetry and Other Essays, Project Gutenberg #5428", 5428, B),
   gb("stendhal-chartreuse", "Stendhal, La Chartreuse de Parme (1839), Project Gutenberg #796", 796, B)],
  "The four texts whole.", "Stratum VII, the posterity Bennett's Romantic Poets and the Culture of Posterity (1999) reads as a poetics: the "
  "writer who 'must himself create the taste by which he is to be relished' (Wordsworth's letter of 1807, giving it as Coleridge's remark; the "
  "Essay of 1815 has 'the task of creating the taste by which he is to be enjoyed'), 'among the English Poets after my death', poets as 'mirrors of the "
  "gigantic shadows which futurity casts upon the present', and the novel dedicated at its last line 'TO THE HAPPY FEW'. Nietzsche's 'Einige "
  "werden posthum geboren' is seated at EA-CORPORA-27/03 (nietzsche, text/ecce-homo-pg.txt)."),
 ("dickinson-poems-1890-1896", "25", "Emily Dickinson, Poems, Three Series, ed. M. L. Todd and T. W. Higginson (Boston, 1890–1896)", "eng",
  "Public domain everywhere (Dickinson died 1886; published 1890–1896); the Gutenberg file under its licence.",
  [gb("dickinson-1890-1896", "Poems by Emily Dickinson, Three Series, Complete, ed. Todd and Higginson, Project Gutenberg #12242", 12242, B)],
  "The three series whole, as Todd and Higginson edited them. The manuscripts are seated at EA-CORPORA-02/14 (dickinson-mss).",
  "'This is my letter to the world, / That never wrote to me': the dispatch to unknown readers, edited for its first readers by the same "
  "Higginson whose 'Sappho' is 36/10, stratum VIII."),
 ("baratynsky-moi-dar-ubog", "26", "Е. А. Боратынский, «Мой дар убог и голос мой не громок» (1828), Wikisource (ru)", "rus",
  "Public domain everywhere (1828; Baratynsky died 1844). The Wikisource page's text under CC BY-SA 4.0 for the site's contributions.",
  [{"kind": "ws", "slug": "moi-dar-ubog", "work": "Боратынский, «Мой дар убог и голос мой не громок» (1828), ru.wikisource", "lang": "ru",
    "title": "Мой дар убог и голос мой не громок (Боратынский)", "class": B}],
  "The poem whole.", "'И как нашёл я друга в поколенье, / Читателя найду в потомстве я': the reader found in posterity, the poem Mandelstam's "
  "'О собеседнике' (1913) opens from, the first link of the Russian line in stratum VIII. The page's commentary quotes the bottle passage of «О собеседнике»: "
  "'Письмо, запечатанное в бутылке, адресовано тому, кто найдет её.' The essay whole is a declared absence."),
 ("wipp-markers-sandia-1993", "27", "K. M. Trauth, S. C. Hora and R. V. Guzowski, Expert Judgment on Markers to Deter Inadvertent Human Intrusion into the Waste Isolation Pilot Plant, SAND92-1382 (Albuquerque, 1993)", "eng",
  "SAND92-1382 is an Unlimited Release of Sandia National Laboratories, prepared for the United States Department of Energy; the Internet Archive item is marked Public Domain Mark 1.0.",
  [ia("sandia-1993", "Trauth, Hora and Guzowski, SAND92-1382, Unlimited Release (Sandia National Laboratories, November 1993)", "long-term-warning", B)],
  "The report whole, with its appendices (the two expert teams' reports).", "Stratum XI, the literal engineering turn: a message designed for "
  "readers ten thousand years out, with its drafted text, 'This place is not a place of honor', and its problem stated as design: deixis that "
  "survives the loss of its context."),
]
for corpus, n, title, lang, lic, items, scope, why in SEATS:
    spec = {"corpus": corpus, "seat": f"EA-CORPORA-36/{n}", "title": title, "language": lang, "fetched": "2026-11-07", "spine": "EA-CORPORA-36",
            "ruling": RULING, "seating": SEATING, "license": {"payload": lic, "record": "CC-BY-4.0 applies to this seat record only."},
            "normalization": NORM, "items": items, "loci": [], "scope": scope, "why_seated": why, "research": RESEARCH}
    f = H / f"spec36-{corpus}.json"
    if f.exists():
        spec["loci"] = json.loads(f.read_text(encoding="utf-8")).get("loci", [])   # keep loci entered by add_loci36.py
    f.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", corpus)
