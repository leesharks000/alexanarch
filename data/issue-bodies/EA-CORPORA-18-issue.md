### Protocol Version

alexanarch-deposit-protocol/v1

### Title

EA-CORPORA-18 — The Eighteenth Seating: The Avant-Garde and Its Sources — Pound and the Cantos as First Printed, the Italian Lyric, Futurism, Dada, Jarry, Farce, Nonsense and Constraint, Visual Poetry, Stein, and Russian Formalism

### Creator

Sharks, Lee

### ORCID

0009-0000-1599-0703

### Date

2026-10-15

### Description

Ten seats on the originals shelf, 97 works and 515,012 lines, for the modern avant-garde and the sources it read, in the editions a reader of their time could open, every one public domain in the United States. Pound's further volumes and the Cantos as first printed (Three Cantos, Poetry, 1917) with his Cavalcanti of 1912; the Italian lyric of the thirteenth and fourteenth centuries, the Sicilian school to the stilnovisti, with Rossetti's English; Italian and Russian Futurism and the English Vortex; Dada, the journal entire; Jarry, Ubu to Faustroll; French farce; the nonsense and constraint the Oulipo named as its plagiarists by anticipation; visual poetry from Optatianus to Mallarmé and Apollinaire, the line behind concrete poetry; Stein; and Russian Formalism, OPOJAZ's Poetika of 1919 and Shklovsky to 1930. Each seat holds the files as fetched, scans where the page is the text, one text per work, a provenance record with its verified loci, and a SHA-256 manifest; each has a card on the Training Layer Literature shelf. What is still in copyright — the Oulipo itself, the concrete poets proper, the Cantos after XXX — is named and not seated.

### Content Type

Dataset

### License

CC-BY-4.0

### Substrate Disclosure

Human–machine collaborative. Sources located, fetched, verified against their front matter, assembled into seats, hashed and indexed, and every locus found in the seated text, all in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction. The selection — which movements, which authors, Pound and the Cantos, the Italian lyric, Jarry and Shklovsky — is Lee Sharks's. CC-BY-4.0 applies to this record and the seat records; each payload carries its own licence, stated per seat.

### Keywords

corpus seating, primary sources, public domain, avant-garde, Ezra Pound, The Cantos, Guido Cavalcanti, dolce stil novo, Scuola siciliana, Giacomo da Lentini, Dante Gabriel Rossetti, Futurism, F. T. Marinetti, parole in libertà, zaum, Velimir Khlebnikov, Aleksei Kruchenykh, Vladimir Mayakovsky, Vorticism, Blast, Dada, Tristan Tzara, Francis Picabia, Hugo Ball, Alfred Jarry, pataphysics, farce, nonsense, Lewis Carroll, Christian Morgenstern, Raymond Roussel, Lautréamont, Oulipo, constraint, visual poetry, concrete poetry, Stéphane Mallarmé, Un coup de dés, Guillaume Apollinaire, Calligrammes, Gertrude Stein, Russian Formalism, OPOJAZ, Viktor Shklovsky, ostranenie, Yury Tynyanov, Boris Eikhenbaum, Training Layer Literature, originals shelf, EA-CORPORA

### Related Identifiers

AXN deposit #1673 — EA-CORPORA-17: the preceding seating
AXN deposit #1580 — EA-CORPORA-12: the rule that seatings are periodically gathered
Seat EA-CORPORA-05/01 (browning) and 05/02 (pound) — the constructed-voice series this seating extends

### Version

v1.0

### Methodology

Sources located on Project Gutenberg (catalogue searched by author), the Internet Archive (advanced search, item metadata read for access restriction and files) and Wikisource (fr, ru; rendered pages, the single-page text where one exists). Each item's front matter read against the edition claimed for it and the edition statement corrected to what the file shows; publishers not shown in a file are not asserted. Gutenberg texts stripped at the START/END markers; Internet Archive scans seated with their OCR text layers, uncorrected, the scan as witness; Wikisource texts as rendered from the proofread transcription, their page lists kept. Every file hashed into the seat's MANIFEST.sha256. Every verified locus is a string found in the seated text by rebuild/corpora/ea-corpora-18/build_seats.py; a locus not found is recorded as not found. Licences stated per seat, with the EU term carried where it differs (payload/record split, EA-CORPORA-02/01). The builders, the seat specification and this body are under rebuild/corpora/ea-corpora-18/.

### Falsification Conditions

A seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a seated file differs from the file at the origin its source.json names; if an edition statement misstates the front matter of the file it describes; if a verified locus cannot be found in the seated text; if an item stated public domain in the United States was published in or after 1931 by an author not in the public domain in the source country on 1 January 1996; or if the four surfaces (seat, index, deposit, shelf) disagree.

### Body

# EA-CORPORA-18 — The Eighteenth Seating

MANUS, 15 October 2026: "we need more seatings of avant garde literature. dada. farce. oulipo. futurist. - whatevers in the public domain. originals is good on classics, impoverished on modern. and i want the italian troubadours. and pound, more pound. need the cantos." — "and the concrete poets" — "also need jarry, shklovsky, etc".

## Seat 18/01 — Pound II

*Ezra Pound, 1909–1920, and the Cantos as first printed — the further volumes, the Romance studies, the Cavalcanti, and Three Cantos (Poetry, 1917)*

- Editions:
  - Exultations (London: Elkin Mathews, 1909)
  - Provença: Poems Selected from Personae, Exultations, and Canzoniere (Boston: Small, Maynard, 1910)
  - The Spirit of Romance: An Attempt to Define Somewhat the Charm of the Pre-Renaissance Literature of Latin Europe (London: J. M. Dent, 1910) — Cornell copy
  - Canzoni (1911) & Ripostes (1912), whereto are appended the Complete Poetical Works of T. E. Hulme (London: Elkin Mathews, 1913)
  - Sonnets and Ballate of Guido Cavalcanti, with translations of them and an introduction by Ezra Pound (London: Stephen Swift, 1912) — University of Toronto copy
  - Des Imagistes: An Anthology, ed. Ezra Pound (New York: Albert and Charles Boni, 1914)
  - Three Cantos [I], Poetry: A Magazine of Verse 10.3 (June 1917) — the first printing of the Cantos (JSTOR Early Journal Content)
  - Three Cantos [II], Poetry 10.4 (July 1917) (JSTOR Early Journal Content)
  - Three Cantos: III, Poetry 10.5 (August 1917) (JSTOR Early Journal Content)
  - Instigations, together with An Essay on the Chinese Written Character by Ernest Fenollosa (New York: Boni and Liveright, 1920)
  - Hugh Selwyn Mauberley (London: Ovid Press, 1920)
- Licence: Public domain in the United States: every item published 1909–1920. NOT public domain in the EU or UK (Pound d. 1972 → 2043): payload/record split per the DSS precedent (EA-CORPORA-02/01); the seat's US ground is stated and redistribution is scoped accordingly. Project Gutenberg packaging under the PG licence; Internet Archive scans of public-domain volumes; JSTOR Early Journal Content, free to anyone in the world.
- Verified locus: Three Cantos I (Poetry, June 1917) — the opening address to Browning, 'Hang it all, there can be but one Sordello!' (the text layer reads 'ANG it all': the drop capital is lost; the scan is the witness)
- Verified locus: Sonnets and Ballate of Guido Cavalcanti (1912) — Sonetto IV, 'Io priego questa donna, che pietate', the Italian on the facing page (the text layer reads '10' for 'Io')
- Verified locus: Hugh Selwyn Mauberley (1920) — the first poem, E. P. Ode pour l'élection de son sépulchre (the Gutenberg text prints the heading 'E.P. ODE POUR SELECTION DE SON SEPULCHRE')
- Verified locus: The Spirit of Romance (1910) — the chapter on Arnaut Daniel
- Verified locus: Des Imagistes (1914) — Pound's 'Fan-Piece, for Her Imperial Lord'
- Scope: Seated beside card 05/02 (Personae, Lustra, Cathay, Poems 1918–21 with Cantos IV–VII), which is left as deposited. THE CANTOS: the seatable Cantos are those printed before 1931. Three Cantos (Poetry, 1917) are seated here; Cantos IV–VII are in 05/02 (Poems 1918–21). A Draft of XVI Cantos (Paris: Three Mountains Press, 1925), A Draft of the Cantos 17–27 (London: John Rodker, 1928) and A Draft of XXX Cantos (Paris: Hours Press, 1930) are public domain in the United States, but no public-domain witness was reachable from the session: the Internet Archive holds only the 1990 New Directions reprint, lending-restricted; HathiTrust is not reachable from this workspace. QUEUED: the periodical first printings 1922–1930 (The Dial, The Criterion, The Transatlantic Review), located on the Internet Archive and not yet read for the Canto pages. Cantos XXXI onward are in copyright in the United States (Eleven New Cantos, 1934 → 2030) and are not seated.
- Why seated: More Pound, and the Cantos from their first printing. Three Cantos (1917) open by arguing with Browning's Sordello — the series Browning, Pound, Pessoa that cards 05/01–05/03 measure, now with its hinge in print. The Cavalcanti of 1912 is Pound's Italian source on the facing page, and The Spirit of Romance is his map of the Provençal and Italian lyric that card 18/02 seats in its own languages.
- Files: [the seat](https://www.alexanarch.org/data/corpora/pound-ii/) — [source.json](https://www.alexanarch.org/data/corpora/pound-ii/source.json), [MANIFEST.sha256](https://www.alexanarch.org/data/corpora/pound-ii/MANIFEST.sha256). Shelf: [traininglayerliterature.org/originals/pound-ii](https://traininglayerliterature.org/originals/pound-ii/)

## Seat 18/02 — Italian Lyric

*The Italian lyric of the thirteenth and fourteenth centuries — the Sicilian school, the Siculo-Tuscans, the dolce stil novo, and the comic poets, in the nineteenth- and early twentieth-century editions, with Rossetti's English*

- Editions:
  - Poeti del primo secolo della lingua italiana, vol. I (Firenze, 1816) — University of Toronto copy
  - Poeti del primo secolo della lingua italiana, vol. II (Firenze, 1816) — University of Toronto copy
  - Rime di Dante Alighieri; si aggiungono le rime di Guido Guinizzelli, di Guido Cavalcanti, di Cino da Pistoia (Milano: N. Bettoni, 1828) — Google Books copy
  - Le rime di Guido Cavalcanti, testo critico pubblicato dal prof. Nicola Arnone (Firenze: Sansoni, 1881) — Google Books copy
  - I rimatori pistoiesi dei secoli XIII e XIV, ed. Guido Zaccagnini (Pistoia: Tipografia Sinibuldiana, 1907) — Google Books copy
  - Rimatori siculo-toscani del dugento. Serie prima: Pistoiesi, Lucchesi, Pisani, ed. Guido Zaccagnini and Amos Parducci (Bari: Laterza, 1915)
  - Jacopone da Todi, Le Laude secondo la stampa fiorentina del 1490, ed. Giovanni Ferri (Bari: Laterza, Scrittori d'Italia, 1915)
  - Cecco d'Ascoli, L'Acerba, ed. Pasquale Rosario (Lanciano: Carabba, 1916)
  - Dante Gabriel Rossetti, Dante and his Circle, with the Italian Poets preceding him (1100–1200–1300): a collection of lyrics (London: Ellis and White, 1874) — Google Books copy
  - Dante Alighieri, The New Life (La Vita Nuova), translated by Dante Gabriel Rossetti — the Siddal Edition (London: Ellis and Elvey, 1899)
- Licence: Public domain: the poems are medieval; every edition seated was published 1816–1907 (United States); Project Gutenberg packaging under the PG licence; Internet Archive scans (Google Books and University of Toronto copies) of public-domain volumes.
- Verified locus: Poeti del primo secolo I (1816) — 'Di Notaro Iacopo da Lentino': Giacomo da Lentini, the Notary, under the name the 1816 edition gives him
- Verified locus: Cavalcanti, Rime, ed. Arnone (1881) — the canzone 'Donna mi prega', the poem Pound translates in Canto XXXVI
- Verified locus: Rime (1828) — the rime of Guido Guinizzelli, added to Dante's
- Verified locus: Rossetti, Dante and his Circle (1874) — the Cavalcanti section
- Verified locus: Jacopone, Laude XCIII — 'Donna del paradiso, lo tuo figliolo è preso', the dramatic lauda of the Passion
- Scope: The poets Pound calls the Tuscans and Dante calls the dolce stil novo, with the Sicilian court of Frederick II before them and the comic-realist and religious poets beside them, in editions a reader of 1910 could open. NOT SEATED: the Italians who wrote in Occitan — Sordello, Lanfranc Cigala, Bonifaci Calvo, Rambertino Buvalelli — no public-domain edition was located in the session; QUEUED. Modern critical editions (Contini, Poeti del Duecento, 1960; Antonelli, I poeti della Scuola siciliana, 2008) are in copyright and are not seated: they are the finding aids this seat routes around, back to the editions they correct.
- Why seated: The Italian troubadours, and the source of the Cavalcanti Pound translated and the Dante's circle Rossetti translated. The originals shelf held Dante's Commedia nowhere and the duecento lyric not at all; this seat brings the canzone and the sonnet in at their invention.
- Files: [the seat](https://www.alexanarch.org/data/corpora/italian-lyric/) — [source.json](https://www.alexanarch.org/data/corpora/italian-lyric/source.json), [MANIFEST.sha256](https://www.alexanarch.org/data/corpora/italian-lyric/MANIFEST.sha256). Shelf: [traininglayerliterature.org/originals/italian-lyric](https://traininglayerliterature.org/originals/italian-lyric/)

## Seat 18/03 — Futurism

*Futurism — Italian (Marinetti, Palazzeschi, Govoni; parole in libertà, the synthetic theatre), Russian (Hylaea, Mayakovsky, Khlebnikov, Kruchenykh) and the English Vortex (Blast)*

- Editions:
  - I manifesti del futurismo, lanciati da Marinetti, Boccioni, Carrà, Russolo, Balla, Severini, Pratella, Mme de Saint-Point, Apollinaire, Palazzeschi (Milano: Movimento futurista, n.d.; the manifestos dated 1909–1913, the first the Figaro manifesto of 20 February 1909)
  - F. T. Marinetti, Distruzione: poema futurista, tr. Decio Cinti (Milano: Edizioni futuriste di Poesia, 1911)
  - F. T. Marinetti, Zang Tumb Tuuum: Adrianopoli ottobre 1912, parole in libertà (Milano, 1914) — scan with text layer
  - F. T. Marinetti, Emilio Settimelli, Bruno Corra, Teatro futurista sintetico (Piacenza: Ghelfi, for the Istituto editoriale italiano, Biblioteca teatrale n. 10, 1921) — the synthetic theatre of 1915–16, in its 1921 collected printing
  - Aldo Palazzeschi, L'Incendiario, col rapporto sulla vittoria futurista di Trieste (Milano: Edizioni futuriste di Poesia, 1910)
  - Corrado Govoni, Rarefazioni e parole in libertà (1915) — scan; the visual tables are the text
  - Пощечина общественному вкусу [A Slap in the Face of Public Taste] (Москва, 1912; dated 1913 in the item): Д. Бурлюк, Н. Бурлюк, А. Крученых, В. Кандинский, Б. Лившиц, В. Маяковский, В. Хлебников
  - Футуристы. Рыкающий Парнас [The Roaring Parnassus] (Санкт-Петербург, 1914): Маяковский, Игорь Северянин, Хлебников and others; drawings by Д. Бурлюк, Иван Пуни, Павел Филонов, О. Розанова
  - Владимир Маяковский, Владимир Маяковский: трагедия (Москва, 1914), drawings by Vladimir and David Burliuk
  - Владимир Маяковский, Облако в штанах [A Cloud in Trousers] (1915) — Russian Wikisource text, after Полное собрание сочинений в 13 т. (Москва, 1955–1961)
  - Владимир Маяковский, Простое как мычание (Петроград: Парус, 1916)
  - Владимир Маяковский, Война и мир (Петроград: Парус, 1917)
  - Владимир Маяковский, Про это (Москва–Петроград: Госиздат, 1923), with photomontage cover and illustrations
  - Велимир Хлебников, Время мера мира (Петроград, 1916)
  - Велимир Хлебников, Заклятие смехом [Incantation by Laughter] (Студия импрессионистов, 1910) — Russian Wikisource text, after Творения (Москва, 1986)
  - Велимир Хлебников, «Бобэоби пелись губы» (Пощечина общественному вкусу, 1912) — Russian Wikisource text
  - Алексей Кручёных, «Дыр бул щыл» (Помада, 1913) — Russian Wikisource text
  - Blast: Review of the Great English Vortex, No. 1, ed. Wyndham Lewis (London: John Lane, 20 June 1914) — scan with text layer
- Licence: Public domain in the United States: every printed item published 1909–1923. EU status varies by author and is stated per item: PD-EU — Marinetti (d. 1944), Khlebnikov (d. 1922), Mayakovsky (d. 1930), Kandinsky (d. 1944); NOT PD-EU — Palazzeschi (d. 1974), Govoni (d. 1965), Corra (d. 1976), the Burliuks (D. d. 1967), Kruchenykh (d. 1968), Wyndham Lewis (d. 1957 → 2028). Payload/record split per EA-CORPORA-02/01. Wikisource transcriptions CC BY-SA 4.0 over public-domain texts; their source editions are named.
- Verified locus: Fondazione e Manifesto del Futurismo (1909), point 1: 'Noi vogliamo cantare l'amor del pericolo'
- Verified locus: Zang Tumb Tuuum (1914) — the title-page onomatopoeia, in the text layer of the scan
- Verified locus: Kruchenykh, 'Дыр бул щыл' (1913) — the zaum poem
- Verified locus: Khlebnikov, 'Заклятие смехом' — 'О, рассмейтесь, смехачи!'
- Verified locus: Blast 1 (1914) — the Vortex manifestos
- Verified locus: Mayakovsky, 'Облако в штанах' — the prologue, 'Вашу мысль, мечтающую на размягченном мозгу'
- Scope: Books and first printings to 1923. The Futurist journals (Poesia, Lacerba) are on the Internet Archive issue by issue and are not seated here: QUEUED as a separate run. Blast 2 (1915) is access-restricted on the Internet Archive (HTTP 401) and is not seated. Kruchenykh and Khlebnikov's Победа над солнцем (1913) not located in a public-domain witness; QUEUED.
- Why seated: The movement that put the word on the page as an object. Parole in libertà and zaum are the two ends of the operation the archive calls a constructed language: Marinetti's typography makes the sentence a field; Kruchenykh's 'дыр бул щыл' makes a word that answers to nothing before it.
- Files: [the seat](https://www.alexanarch.org/data/corpora/futurism/) — [source.json](https://www.alexanarch.org/data/corpora/futurism/source.json), [MANIFEST.sha256](https://www.alexanarch.org/data/corpora/futurism/MANIFEST.sha256). Shelf: [traininglayerliterature.org/originals/futurism](https://traininglayerliterature.org/originals/futurism/)

## Seat 18/04 — Dada

*Dada, Zurich, Paris and Berlin, 1917–1921 — the journal Dada (nos. 1–8), Der Dada no. 1, Tzara, Picabia, Serner and Ball*

- Editions:
  - Dada: recueil littéraire et artistique, nos. 1–8, ed. Tristan Tzara (Zürich, July 1917 – Paris, September 1921) — scans of all eight issues, with their text layers
  - Tristan Tzara, Vingt-cinq poèmes, with ten woodcuts by Hans Arp (Zürich: Collection Dada, 1918)
  - Francis Picabia, Poèmes et dessins de la fille née sans mère: 18 dessins, 51 poèmes (Lausanne: Imprimeries réunies, 1919; 'Terminé à Gstaad, 5 avril 1918')
  - Francis Picabia, Pensées sans langage, poème, preceded by a preface by 'Udnie' (Paris: Eugène Figuière, 1919), dedicated to Ribemont-Dessaignes, Duchamp and Tzara
  - Der Dada, no. 1, ed. Raoul Hausmann (Berlin, June 1919) — scan
  - Walter Serner, Letzte Lockerung: manifest dada (Hannover: Paul Steegemann, 1920) — Google Books copy
  - Hugo Ball, Flametti, oder vom Dandysmus der Armen, Roman (1918), dedicated to Emmy Hennings
  - Adolf Knoblauch, Dada, with a woodcut by Lyonel Feininger (Leipzig: Kurt Wolff, Der jüngste Tag, 1919)
- Licence: Public domain in the United States: every item published 1917–1921. EU status per author: PD-EU — Ball (d. 1927), Serner (d. 1942), Picabia (d. 1953), Knoblauch (d. 1951); NOT PD-EU — Tzara (d. 1963), Arp (d. 1966), Hausmann (d. 1971), Feininger (d. 1956 → 2027). Payload/record split per EA-CORPORA-02/01. Project Gutenberg packaging under the PG licence.
- Verified locus: Dada 3 (December 1918) — Tzara's manifesto of 1918, opening 'Pour lancer un manifeste' (the text layer reads 'il faut vouioir' for 'il faut vouloir')
- Verified locus: Vingt-cinq poèmes (1918) — the Arp woodcuts credited
- Verified locus: Serner, Letzte Lockerung (1920) — the title, in the text layer
- Verified locus: Picabia, Pensées sans langage (1919) — the dedication to Ribemont-Dessaignes, Marcel Duchamp and Tristan Tzara
- Scope: Cabaret Voltaire (Zürich, 1916) is on the Internet Archive only in the 1981 reprint and is not seated. Ball's sound poems ('Karawane', 'Gadji beri bimba') were printed in the Dada Almanach (Berlin, 1920), not located in a public-domain witness; QUEUED. Schwitters's Anna Blume (1919) not located; Ursonate (1932) is in copyright in the United States until 2028.
- Why seated: The negation the archive's negative ontology has to stand next to. Dada declares that the work is its own refusal, and the journal is where the refusal was printed as a programme, issue by issue.
- Files: [the seat](https://www.alexanarch.org/data/corpora/dada/) — [source.json](https://www.alexanarch.org/data/corpora/dada/source.json), [MANIFEST.sha256](https://www.alexanarch.org/data/corpora/dada/MANIFEST.sha256). Shelf: [traininglayerliterature.org/originals/dada](https://traininglayerliterature.org/originals/dada/)

## Seat 18/05 — Jarry

*Alfred Jarry — Ubu, Faustroll and pataphysics, the novels, the plays and the almanacs, 1894–1911 and the posthumous editions*

- Editions:
  - Ubu Roi, ou les Polonais, drame en cinq actes en prose (1896) — Gutenberg text from the Gallica (BnF) scan
  - Ubu enchaîné, précédé de Ubu Roi (Paris: Éditions de La Revue blanche, 1900) — scan
  - Les Minutes de sable mémorial (1894) — Wikisource text proofread against the Fasquelle reissue of 1932
  - César-Antéchrist (1895) — Wikisource text proofread against the Fasquelle reissue of 1932
  - L'Autre Alceste (La Revue blanche, t. 11, 1896)
  - Les Paralipomènes d'Ubu (La Revue blanche, t. 11, 1896)
  - De l'inutilité du théâtre au théâtre (Mercure de France, t. 19, 1896)
  - Questions de théâtre (La Revue blanche, t. 12, 1897)
  - Les Jours et les nuits, roman d'un déserteur (Paris: Société du Mercure de France, 1897)
  - L'Amour en visites (Paris: Pierre Fort, 1898)
  - L'Amour absolu (Paris: Mercure de France, 1899)
  - Almanach du Père Ubu illustré (1899)
  - Messaline, roman de l'ancienne Rome (La Revue blanche, tomes 22 and 23, 1900)
  - Almanach illustré du Père Ubu (XXe siècle) (1901)
  - Le Surmâle, roman moderne (Paris: Éditions de La Revue blanche, 1902)
  - Ubu sur la Butte (Paris: Sansot, 1906)
  - Par la taille, un acte comique et moral (Paris: Théâtre mirlitonesque, 1906)
  - Le Moutardier du Pape, opérette bouffe en trois actes (Paris, 1907)
  - Gestes et opinions du docteur Faustroll, pataphysicien, roman néo-scientifique (Paris: Fasquelle, 1911)
  - Ubu cocu, restitué en son intégrité tel qu'il a été représenté par les marionnettes du Théâtre des Phynances (Éditions des Trois Collines, 1944; posthumous)
- Licence: Public domain: Jarry d. 1907. The posthumous editions (Faustroll 1911; Ubu cocu 1944; the 1932 reissue of Les Minutes de sable mémorial) are public domain in the United States because the work was public domain in France on 1 January 1996 and so was never restored (17 U.S.C. §104A). Project Gutenberg packaging under the PG licence; Internet Archive scan; Wikisource (fr) transcriptions CC BY-SA 4.0 over the public-domain editions they were proofread against.
- Verified locus: Ubu Roi I.1 — the first word, 'Merdre'
- Verified locus: Faustroll II.8 — 'La pataphysique est la science des solutions imaginaires'
- Verified locus: Faustroll — the definition of pataphysics, 'la science des solutions imaginaires'
- Verified locus: Le Surmâle — the opening sentence, 'L'amour est un acte sans importance, puisqu'on peut le faire indéfiniment'
- Scope: Wikisource texts are the proofread transcriptions of the editions named; the scans behind them are the Wikisource index files recorded in each item's pages.json. La Dragonne (1943) and Pantagruel (1911) are on Wikisource at lower proofreading levels and are not seated in this pass. The Collège de 'Pataphysique and the Oulipo it founded (1960) are in copyright.
- Why seated: Jarry is the root of the line from farce to the Oulipo: Ubu is the farce that broke the theatre, and pataphysics — 'the science of imaginary solutions' — is the science the Oulipo was founded inside, as a sub-commission of the Collège de 'Pataphysique.
- Files: [the seat](https://www.alexanarch.org/data/corpora/jarry/) — [source.json](https://www.alexanarch.org/data/corpora/jarry/source.json), [MANIFEST.sha256](https://www.alexanarch.org/data/corpora/jarry/MANIFEST.sha256). Shelf: [traininglayerliterature.org/originals/jarry](https://traininglayerliterature.org/originals/jarry/)

## Seat 18/06 — Farce

*French farce and the comic monologue of the fin de siècle — Labiche, Courteline, Allais*

- Editions:
  - Eugène Labiche and Édouard Martin, Le Voyage de Monsieur Perrichon, comédie en quatre actes (1860), in an American school edition with an English introduction (c. 1905)
  - Georges Courteline, Messieurs les ronds-de-cuir (1893), in the edition with fifteen watercolours by Sem (Paris: Javal et Bourdeaux, 1927)
  - Alphonse Allais, À se tordre: histoires chatnoiresques (1891)
  - Alphonse Allais, Deux et deux font cinq (2 + 2 = 5) (Paris: Ollendorff, 1895)
- Licence: Public domain: Labiche d. 1888, Martin d. 1866, Courteline d. 1929, Allais d. 1905. Project Gutenberg packaging under the PG licence.
- Verified locus: Le Voyage de Monsieur Perrichon — the title role
- Verified locus: À se tordre — 'histoires chatnoiresques', the Chat Noir cabaret
- Scope: The farce proper is also seated in 18/05 (Ubu) and 18/03 (the Futurist synthetic theatre). Feydeau's plays and the medieval Farce de Maître Pathelin were not located on the reachable sources in this pass; QUEUED. Aristophanes and Plautus are on the shelf already (cards 03/xx, aristophanes).
- Why seated: The comic mechanism the avant-garde inherited: Labiche's machinery of misunderstanding and Allais's deadpan. Allais's blank rectangle, 'Première communion de jeunes filles chlorotiques par un temps de neige' (the Incohérents, 1883; printed in the Album primo-avrilesque, 1897), is the monochrome thirty years before Malevich and the joke Dada would make a programme.
- Files: [the seat](https://www.alexanarch.org/data/corpora/farce/) — [source.json](https://www.alexanarch.org/data/corpora/farce/source.json), [MANIFEST.sha256](https://www.alexanarch.org/data/corpora/farce/MANIFEST.sha256). Shelf: [traininglayerliterature.org/originals/farce](https://traininglayerliterature.org/originals/farce/)

## Seat 18/07 — Nonsense & Constraint

*Nonsense and constraint before the Oulipo — the 'plagiarists by anticipation': Carroll, Lear, Morgenstern, Lautréamont, Roussel*

- Editions:
  - Lewis Carroll, Alice's Adventures in Wonderland (1865)
  - Lewis Carroll, Through the Looking-Glass, and What Alice Found There (1871)
  - Lewis Carroll, Phantasmagoria and Other Poems (1869), with A. B. Frost's illustrations (London: Macmillan, 1911)
  - Lewis Carroll, The Hunting of the Snark: An Agony in Eight Fits (1876)
  - Edward Lear, Nonsense Books, with all the original illustrations (1894): A Book of Nonsense (1846), Nonsense Songs (1871), More Nonsense (1872), Laughable Lyrics (1877)
  - Christian Morgenstern, Galgenlieder nebst dem 'Gingganz' (first 1905; 22nd printing, Berlin: Bruno Cassirer, 1917, with Karl Walser's cover drawing)
  - Le comte de Lautréamont, Les Chants de Maldoror, chants I–VI (printed 1869, withheld by the publisher; the Gutenberg text is of a later reprint 'revue et corrigée d'après le manuscrit original')
  - Isidore Ducasse, Poésies I–II (1870)
  - Raymond Roussel, Locus Solus (Paris: Lemerre, 1914)
- Licence: Public domain: Carroll d. 1898, Lear d. 1888, Morgenstern d. 1914, Lautréamont d. 1870, Roussel d. 1933 (PD-EU since 2004; Locus Solus 1914, PD in the United States). Project Gutenberg packaging under the PG licence.
- Verified locus: Through the Looking-Glass — 'Jabberwocky', and Humpty Dumpty's portmanteau gloss of it
- Verified locus: Galgenlieder — 'Fisches Nachtgesang', the poem made only of metrical signs
- Verified locus: Ducasse, Poésies II — 'La poésie doit être faite par tous. Non par un.'
- Verified locus: Locus Solus — Martial Canterel's garden of machines
- Scope: The Oulipo itself (founded 1960; Queneau, Perec, Calvino, Roubaud) is in copyright and is not seated. What is seated is the line the Oulipo named for itself: its 'plagiaires par anticipation'. Roussel's Comment j'ai écrit certains de mes livres (1935) is in copyright in the United States until 2031 and is not seated; Impressions d'Afrique (1910) was not located on the reachable sources in this pass; QUEUED.
- Why seated: Constraint as the engine of a text. Roussel built his novels from homophones and Carroll built his poems from rules; both are the precedent for treating a procedure, rather than an intention, as the author of a sentence.
- Files: [the seat](https://www.alexanarch.org/data/corpora/nonsense-and-constraint/) — [source.json](https://www.alexanarch.org/data/corpora/nonsense-and-constraint/source.json), [MANIFEST.sha256](https://www.alexanarch.org/data/corpora/nonsense-and-constraint/MANIFEST.sha256). Shelf: [traininglayerliterature.org/originals/nonsense-and-constraint](https://traininglayerliterature.org/originals/nonsense-and-constraint/)

## Seat 18/08 — Visual Poetry

*Visual poetry before concrete — Optatianus Porphyrius's grid poems, Mallarmé's Un coup de dés (1914), Apollinaire's Calligrammes (1918)*

- Editions:
  - Publilius Optatianus Porfyrius, Panegyricus Constantino Augusto dictus — the carmina cancellata (grid poems with an inner text picked out in the lattice); scan, edition unidentified in the item's metadata
  - Stéphane Mallarmé, Un coup de dés jamais n'abolira le hasard: poème (1914; first in Cosmopolis, 1897) — scan; the page spread is the text
  - Guillaume Apollinaire, Calligrammes: poèmes de la paix et de la guerre (1913–1916) (Paris: Mercure de France, 1918) — scan; the figured poems are the text
  - Guillaume Apollinaire, Calligrammes (1918) — Project Gutenberg transcription, with the figured poems as images
- Licence: Public domain: Optatianus (4th c.), Mallarmé d. 1898, Apollinaire d. 1918; scans of public-domain volumes (Internet Archive); Project Gutenberg packaging under the PG licence. The edition of Optatianus behind the Internet Archive scan is not named in its metadata: recorded as unidentified, pending a reading of the scan's front matter.
- Verified locus: Un coup de dés (1914) — 'N'ABOLIRA LE HASARD', in the scan's text layer
- Verified locus: Calligrammes — 'Il pleut', the poem set as falling rain
- Verified locus: Optatianus — the Panegyricus to Constantine, in the scan's text layer
- Scope: Concrete poetry proper (Gomringer, 1953; the Noigandres group, 1952; Finlay; Garnier) is in copyright and is not seated. What is seated is its line: the late-antique grid poem, Mallarmé's spatial page and Apollinaire's figured verse, with the Futurist parole in libertà (Marinetti's Zang Tumb Tuuum, Govoni's Rarefazioni) in card 18/03 and Morgenstern's typographic poems in 18/07. The Hellenistic technopaegnia (Simmias, Theocritus's Syrinx) are in the theocritus seat and the Greek Anthology. Rabanus Maurus's In honorem sanctae crucis and George Herbert's 'Easter Wings' were not located in this pass; QUEUED.
- Why seated: The concrete poets, as far back as the public domain reaches. A poem whose layout is part of its meaning cannot be seated as running text alone, so this seat carries the scans.
- Files: [the seat](https://www.alexanarch.org/data/corpora/visual-poetry/) — [source.json](https://www.alexanarch.org/data/corpora/visual-poetry/source.json), [MANIFEST.sha256](https://www.alexanarch.org/data/corpora/visual-poetry/MANIFEST.sha256). Shelf: [traininglayerliterature.org/originals/visual-poetry](https://traininglayerliterature.org/originals/visual-poetry/)

## Seat 18/09 — Stein

*Gertrude Stein — Tender Buttons (1914) and Geography and Plays (1922)*

- Editions:
  - Tender Buttons: Objects, Food, Rooms (1914)
  - Geography and Plays, with an introduction by Sherwood Anderson (1922)
- Licence: Public domain in the United States (published 1914 and 1922) and in the EU (Stein d. 1946). Sherwood Anderson's introduction to Geography and Plays (Anderson d. 1941) public domain. Project Gutenberg packaging under the PG licence.
- Verified locus: Tender Buttons, 'Objects' — the first entry, 'A CARAFE, THAT IS A BLIND GLASS'
- Verified locus: Geography and Plays — 'Sacred Emily', 'Rose is a rose is a rose is a rose'
- Scope: Three Lives (1909) and The Making of Americans (1925) are public domain and not seated in this pass.
- Why seated: The English sentence made into an object. Stein's repetitions are the American case of what the Futurists and Dada did to the page, done inside syntax.
- Files: [the seat](https://www.alexanarch.org/data/corpora/stein/) — [source.json](https://www.alexanarch.org/data/corpora/stein/source.json), [MANIFEST.sha256](https://www.alexanarch.org/data/corpora/stein/MANIFEST.sha256). Shelf: [traininglayerliterature.org/originals/stein](https://traininglayerliterature.org/originals/stein/)

## Seat 18/10 — Russian Formalism

*Russian Formalism, 1919–1930 — OPOJAZ's Poetika (1919), Shklovsky, Tynyanov, Eikhenbaum*

- Editions:
  - Поэтика. Сборники по теории поэтического языка, I–II (Петроград: 18-я Государственная типография, 1919): О. Брик, Е. Поливанов, В. Шкловский, Б. Эйхенбаум, Л. Якубинский — with Shklovsky's «Искусство как прием»
  - Виктор Шкловский, Развертывание сюжета (Петроград: ОПОЯЗ, 1921)
  - Юрий Тынянов, Достоевский и Гоголь (к теории пародии) (Петроград: ОПОЯЗ, 1921)
  - Б. Эйхенбаум, Мелодика стиха (Петербург: Общество изучения теории поэтического языка, 1922)
  - Б. Эйхенбаум, Молодой Толстой (Петербург, 1922)
  - Виктор Шкловский, Сентиментальное путешествие: воспоминания (1923)
  - Ю. Тынянов, Проблема стихотворного языка (Ленинград: Academia, 1924)
  - Б. Эйхенбаум, Сквозь литературу: сборник статей (Ленинград: Academia, 1924)
  - В. Шкловский, Их настоящее (Москва–Ленинград, 1927)
  - Виктор Шкловский, О теории прозы (Москва: Федерация, 1929)
  - В. Шкловский, Техника писательского ремесла (Москва: Молодая гвардия, 1930)
- Licence: Public domain in the United States: every item published in Russia 1919–1930 (pre-1931). EU status per author: PD-EU — Tynyanov (d. 1943), Polivanov (d. 1938), Yakubinsky (d. 1945), Brik (d. 1945); NOT PD-EU — Shklovsky (d. 1984 → 2055), Eikhenbaum (d. 1959 → 2030). Payload/record split per EA-CORPORA-02/01.
- Verified locus: Poetika (1919) — Shklovsky, «Искусство как прием» (Art as Device), the essay that names остранение
- Verified locus: О теории прозы (1929) — остранение (estrangement), in the text layer
- Verified locus: Tynyanov, Достоевский и Гоголь — 'к теории пародии'
- Scope: Shklovsky's Воскрешение слова (1914), Zoo (1923), Ход коня (1923) and Третья фабрика (1926) were not located on the reachable sources; QUEUED. Архаисты и новаторы (Tynyanov, 1929) is on the Internet Archive only in a scan filed under 1985 and is not seated until its printing is established. Jakobson's Новейшая русская поэзия (Prague, 1921) not located; QUEUED. Text layers are the Internet Archive's OCR, uncorrected; the scans are the witnesses.
- Why seated: Shklovsky's device, and the school that read Futurism (card 18/03) as it happened: «Искусство как прием» is the theory of what zaum and parole in libertà do — make the word strange so it can be seen. Tynyanov's parody essay is the theory of the move the archive's heteronymic practice makes.
- Files: [the seat](https://www.alexanarch.org/data/corpora/russian-formalism/) — [source.json](https://www.alexanarch.org/data/corpora/russian-formalism/source.json), [MANIFEST.sha256](https://www.alexanarch.org/data/corpora/russian-formalism/MANIFEST.sha256). Shelf: [traininglayerliterature.org/originals/russian-formalism](https://traininglayerliterature.org/originals/russian-formalism/)

## Not seated, and why

- The Oulipo (founded 1960) and the Collège de 'Pataphysique: in copyright. The seat is its anticipatory line (18/05, 18/07).
- The concrete poets proper (Gomringer, the Noigandres group, Finlay, Garnier): in copyright. The seat is the line behind them (18/08, with 18/03 and 18/07).
- The Cantos after XXX: in copyright in the United States (Eleven New Cantos, 1934, until 2030). The 1925, 1928 and 1930 Drafts are public domain in the United States, but no public-domain witness was reachable in the session.
- The Italians who wrote in Occitan (Sordello and others): no public-domain edition located; queued.
- Everything marked QUEUED in a seat's scope.

### Terms

- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json
- [x] I confirm this work is deposited under the stated license
- [x] I confirm the substrate disclosure is accurate
- [x] I understand that deposited content will NOT be used to train enforcement classifiers
