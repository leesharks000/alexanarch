#!/usr/bin/env python3
"""Writes spec29-ars-poetica.json (EA-CORPORA-29/04). Kept as a generator so the item list reads as one table."""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
PG = "https://www.gutenberg.org/cache/epub/{0}/pg{0}.txt"
GR = "https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/a6eb0cc3e6f6e382934a2c8b33577d2fb4371e00/data/"
LA = "https://raw.githubusercontent.com/PerseusDL/canonical-latinLit/8b536bdf3ed1f43494055efe112433b4a58eab67/data/"
GT = "https://gretil.sub.uni-goettingen.de/gretil/corpustei/"
NC = "CC BY-NC-SA 4.0, stated in the file's <licence>"
items, loci = [], []


def add(cls, kind, slug, work, find=None, label=None, **kw):
    it = {"kind": kind, "slug": slug, "work": work, "class": cls} | kw
    items.append(it)
    if find:
        txt = kw.get("_text") or (f"text/{slug}.ocr.txt" if kind in ("ia", "ia_ref") else f"text/{slug}.txt")
        loci.append({"label": label or work.split(" — ")[0], "text": txt, "find": find})


def perseus(cls, slug, work, base, path, find, label=None):
    repo = "canonical-greekLit" if "greek" in base else "canonical-latinLit"
    commit = base.split("/")[5]
    add(cls, "tei", slug, work, find, label, path=path.split("/")[-1], url=base + path, source=f"PerseusDL/{repo}",
        repository=f"https://github.com/PerseusDL/{repo}", commit=commit, file="data/" + path)


# Greek
perseus("Greek", "demetrius-peri-hermeneias", "Demetrius, Περὶ ἑρμηνείας (On Style) — W. Rhys Roberts (Cambridge, 1902), via Perseus grc2", GR, "tlg0613/tlg001/tlg0613.tlg001.perseus-grc2.xml", "ἑρμηνεία")
perseus("Greek", "dionysius-de-compositione", "Dionysius of Halicarnassus, Περὶ συνθέσεως ὀνομάτων (On the Arrangement of Words) — Usener and Radermacher (Leipzig: Teubner, 1904), via Perseus grc2", GR, "tlg0081/tlg012/tlg0081.tlg012.perseus-grc2.xml", "συνθέσεως")
perseus("Greek", "lucian-quomodo-historia", "Lucian, Πῶς δεῖ ἱστορίαν συγγράφειν (How to Write History) — Teubner (1913), via Perseus grc2", GR, "tlg0062/tlg053/tlg0062.tlg053.perseus-grc2.xml", "ἱστορία")
# Latin
perseus("Latin", "quintilian-institutio", "Quintilian, Institutio oratoria, books I–XII — H. E. Butler, Loeb Classical Library (London: Heinemann; Cambridge, Mass.: Harvard, 1920–1922), the Latin text, via Perseus lat2", LA, "phi1002/phi001/phi1002.phi001.perseus-lat2.xml", "facilitas")
add("Latin", "ws", "dante-de-vulgari-eloquentia", "Dante Alighieri, De vulgari eloquentia, libri I–II (c. 1302–1305) — Latin Wikisource", "Vulgarem locutionem", lang="la", titles=["De Vulgari Eloquentia/Liber I", "De Vulgari Eloquentia/Liber II"])
add("Latin", "ia_ref", "vida-poemata-1550", "Marco Girolamo Vida, Poemata omnia (1550), containing the De arte poetica libri III (first printed 1527) — scan (Google Books via the Internet Archive), OCR layer", "Vida", identifier="bub_gb_9zY01iiFVYYC", scan="bub_gb_9zY01iiFVYYC.pdf")
add("Latin", "ia_ref", "faral-arts-poetiques-1924", "Edmond Faral, Les arts poétiques du XIIe et du XIIIe siècle (Paris: Champion, 1924): the Latin texts of Matthew of Vendôme's Ars versificatoria, Geoffrey of Vinsauf's Poetria nova and Documentum, Evrard the German's Laborintus and John of Garland, with Faral's French studies — OCR layer", "Poetria", identifier="lesartspoetiquesdudouzfaral", scan="lesartspoetiquesdudouzfaral.pdf")
# Sanskrit (GRETIL)
for slug, f, work, find in [
    ("bharata-natyasastra", "sa_bharata-nATyazAstra-1-1618-303335-37.xml", "Bharata, Nāṭyaśāstra (the rasa-sūtra in adhyāya 6)", "vibhāvānubhāvavyabhicārisaṃyogādrasaniṣpattiḥ"),
    ("bhamaha-kavyalamkara", "sa_bhAmaha-kAvyAlaMkAra.xml", "Bhāmaha, Kāvyālaṃkāra", "śabdārthau sahitau kāvyaṃ"),
    ("dandin-kavyadarsa-1-2", "sa_daNDin-kAvyAdarza-1-2.xml", "Daṇḍin, Kāvyādarśa, paricchedas 1–2", "śarīraṃ tāvad iṣṭārthavyavacchinnā"),
    ("dandin-kavyadarsa-3", "sa_daNDin-kAvyAdarza-3.xml", "Daṇḍin, Kāvyādarśa, pariccheda 3 (yamaka and the figures of sound)", "yamakaṃ tac ca pādānām"),
    ("vamana-kavyalamkarasutra", "sa_vAmana-kAvyAlaMkArasUtra.xml", "Vāmana, Kāvyālaṅkārasūtravṛtti", "rītirātmā kāvyasya"),
    ("anandavardhana-dhvanyaloka", "sa_Anandavardhana-dhvanyAloka.xml", "Ānandavardhana, Dhvanyāloka", "kāvyasyātmā dhvanir"),
    ("rajasekhara-kavyamimamsa", "sa_rAjazekhara-kAvyamImAMsA-1.xml", "Rājaśekhara, Kāvyamīmāṃsā (the Kāvyapuruṣa)", "kāvyapuruṣa"),
    ("kuntaka-vakroktijivita", "sa_kuntaka-vakroktijIvita-comm.xml", "Kuntaka, Vakroktijīvita, with the author's vṛtti", "śabdārthau sahitau vakrakavivyāpāraśālini"),
    ("mammata-kavyaprakasa", "sa_mammaTa-kAvyaprakAza.xml", "Mammaṭa, Kāvyaprakāśa", "tadadoṣau śabdārthau")]:
    add("Sanskrit", "gretil", slug, f"{work} — GRETIL TEI ({f})", find, url=GT + f, path=f, source="GRETIL (Göttingen Register of Electronic Texts in Indian Languages)", licence=NC)
# Tamil
add("Tamil", "ws", "tolkappiyam-porulatikaram", "Tolkāppiyam, Poruḷatikāram, the nine iyals (Akattiṇaiyiyal … Ceyyuḷiyal, Marapiyal) — Tamil Wikisource", "மாத்திரை எழுத்து இயல் அசை வகை", lang="ta",
    titles=["தொல்காப்பியம்/பொருளதிகாரம்/" + x for x in ["அகத்திணையியல்", "புறத்திணையியல்", "களவியல்", "கற்பியல்", "பொருளியல்", "மெய்ப்பாட்டியல்", "உவமயியல்", "செய்யுளியல்", "மரபியல்"]])
# Chinese
add("Chinese", "ws", "mao-shi-xu", "《毛詩》序 (the Great Preface to the Odes), as in the Wenxuan, juan 45 — Chinese Wikisource", "詩者，志之所之也", lang="zh", title="毛詩序")
add("Chinese", "ws", "cao-pi-lun-wen", "曹丕《典論·論文》 (Cao Pi, A Discourse on Literature), as in the Wenxuan — Chinese Wikisource", "文人相輕", lang="zh", title="典論/論文")
add("Chinese", "ws", "lu-ji-wen-fu", "陸機《文賦》 (Lu Ji, Rhapsody on Literature) — Chinese Wikisource", "恒患意不稱物", lang="zh", title="文賦")
add("Chinese", "ws", "liu-xie-wenxin-diaolong", "劉勰《文心雕龍》 (Liu Xie, The Literary Mind and the Carving of Dragons), the fifty chapters (全覽) — Chinese Wikisource", "神思", lang="zh", title="文心雕龍 (全覽)")
add("Chinese", "ws", "sikong-tu-ershisi-shipin", "司空圖《二十四詩品》 (Sikong Tu, The Twenty-Four Categories of Poetry) — Chinese Wikisource", "大用外腓，真體內充", lang="zh", title="二十四詩品")
add("Chinese", "ws", "yan-yu-canglang-shihua", "嚴羽《滄浪詩話》 (Yan Yu, Canglang's Remarks on Poetry), juan 1–5 and the letter to Wu Jingxian — Chinese Wikisource", "妙悟", lang="zh",
    titles=["滄浪詩話/卷1", "滄浪詩話/卷2", "滄浪詩話/卷3", "滄浪詩話/卷4", "滄浪詩話/卷5", "滄浪詩話/附录"])
# Japanese
add("Japanese", "ws", "kokinshu-kanajo", "紀貫之『古今和歌集』仮名序 (Ki no Tsurayuki, the Kana Preface to the Kokinshū, 905) — Japanese Wikisource", "やまとうたは、人のこゝろをたねとして", lang="ja", title="古今和歌集仮名序")
add("Japanese", "aozora", "masaoka-shiki-utayomi", "正岡子規『歌よみに与ふる書』 (Masaoka Shiki, Letters to the Tanka Poets, 1898) — Aozora Bunko, from the Iwanami Bunko text (1955; 1983 reset)", "貫之《つらゆき》は下手な歌よみ", url="https://www.aozora.gr.jp/cards/000305/files/2533_16281.html", path="aozora-2533_16281.html", card="https://www.aozora.gr.jp/cards/000305/card2533.html", base_text="「歌よみに与ふる書」岩波文庫、岩波書店、1955（1983改版）")
add("Japanese", "aozora", "hagiwara-shi-no-genri", "萩原朔太郎『詩の原理』 (Hagiwara Sakutarō, The Principles of Poetry, Daiichi Shobō, 1928) — Aozora Bunko, from the Shinchō Bunko text (1954)", "詩とは何ぞや", url="https://www.aozora.gr.jp/cards/000067/files/2843_26253.html", path="aozora-2843_26253.html", card="https://www.aozora.gr.jp/cards/000067/card2843.html", base_text="「詩の原理」新潮文庫、新潮社、1954")
# Korean
add("Korean", "ws", "yi-illo-pahanjip", "이인로『파한집』(破閑集) (Yi Illo, Jottings to Break Idleness, compiled before 1220; printed 1260), books 上·中·下, in literary Chinese — Korean Wikisource", "破閑", lang="ko", titles=["파한집/권상", "파한집/권중", "파한집/권하"])
# Hebrew
add("Hebrew", "ws", "bialik-shiratenu-ha-tseira", "חיים נחמן ביאליק, «שירתנו הצעירה» (Bialik, Our Young Poetry, 1907) — Hebrew Wikisource", "שירתנו", lang="he", title="שירתנו הצעירה")
add("Hebrew", "ws", "bialik-giluy-ve-khisuy", "חיים נחמן ביאליק, «גילוי וכיסוי בלשון» (Bialik, Revealment and Concealment in Language, 1915) — Hebrew Wikisource", "בני אדם זורים בכל יום לרוח", lang="he", title="גילוי וכיסוי בלשון")
# Arabic
add("Arabic", "ws", "qudama-naqd-al-shir", "قدامة بن جعفر، كتاب نقد الشعر (Qudāma ibn Jaʿfar, The Criticism of Poetry, 10th c.) — Arabic Wikisource", "العلم بالشعر ينقسم أقساماً", lang="ar", title="كتاب نقد الشعر")
add("Arabic", "ws", "jurjani-dalail-al-ijaz", "عبد القاهر الجرجاني، دلائل الإعجاز (ʿAbd al-Qāhir al-Jurjānī, The Proofs of Inimitability, 11th c.), parts 1–5 — Arabic Wikisource", "النظم", lang="ar",
    titles=["دلائل الإعجاز - الجزء الأول", "دلائل الإعجاز - الجزء الثاني", "دلائل الإعجاز - الجزء الثالث", "دلائل الإعجاز - الجزء الرابع", "دلائل الإعجاز - الجزء الخامس"])
# Persian
add("Persian", "ws", "nizami-aruzi-chahar-maqala-2", "نظامی عروضی سمرقندی، چهار مقاله، مقالت دوم در ماهیت علم شعر (Niẓāmī ʿArūḍī, Four Discourses, c. 1156, the Second Discourse, on poetry) — Persian Wikisource, the text of Mīrzā Muḥammad Qazvīnī (Berlin: Iranschähr, 1927)", "شاعری صناعتی است", lang="fa", title="چهار مقاله/مقالت دوم")
# Old Norse
add("Old Norse", "ia_ref", "snorra-edda-1907", "Snorri Sturluson, Edda (Prologue, Gylfaginning, Skáldskaparmál, Háttatal), ed. Finnur Jónsson (Reykjavík: S. Kristjánsson, 1907) — OCR layer", "SKALDSKAPARMAL", identifier="eddasnorrasturlu00edda", scan="eddasnorrasturlu00edda.pdf")
# Irish
add("Irish", "ia_ref", "auraicept-na-neces-1917", "Auraicept na n-Éces: The Scholars' Primer, ed. and tr. George Calder (Edinburgh: John Grant, 1917) — OCR layer", "Auraicept", identifier="auraicept00calduoft", scan="auraicept00calduoft.pdf")
# Occitan
add("Occitan", "ia_ref", "leys-damors-1841-1", "Las Flors del gay saber, estier dichas Las Leys d'Amors, vol. I, ed. Gatien-Arnoult (Toulouse: Paya, 1841), Occitan with French translation — OCR layer", "LEYS", identifier="lasflorsdelgaysa01gatiuoft", scan="lasflorsdelgaysa01gatiuoft.pdf")
# Italian
add("Italian", "ws", "pascoli-il-fanciullino", "Giovanni Pascoli, Il fanciullino (1897; in Pensieri e discorsi, Bologna: Zanichelli, 1907), chapters I–XX — Italian Wikisource", "fanciullino", lang="it",
    titles=[f"Pensieri e discorsi/Il fanciullino/{r}" for r in "I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX XX".split()])
# French
add("French", "ws", "du-bellay-deffence", "Joachim du Bellay, La Deffence, et illustration de la langue françoyse (Paris: Arnoul l'Angelier, 1549) — French Wikisource, the 1549 text", "illvstration", lang="fr", title="Défense et illustration de la langue française")
add("French", "ws", "boileau-art-poetique", "Nicolas Boileau, L'Art poétique (1674), in Œuvres poétiques (Paris: Imprimerie générale, 1872) — French Wikisource", "Ce que l’on conçoit bien", lang="fr", title="Boileau - Œuvres poétiques/L’Art poétique/Texte Entier")
add("French", "ws", "rimbaud-lettre-du-voyant", "Arthur Rimbaud, letter to Paul Demeny, 15 May 1871 (the Lettre du voyant), text of Roger Gilbert-Lecomte (Éditions des cahiers libres, 1929) — French Wikisource", "Je est un autre", lang="fr", title="Lettre de Rimbaud à Paul Demeny - 15 mai 1871")
add("French", "ws", "verlaine-art-poetique", "Paul Verlaine, « Art poétique » (1874), in Jadis et naguère (Paris: Léon Vanier, 1884) — French Wikisource", "De la musique avant toute chose", lang="fr", title="Jadis et naguère (1884)/Art poétique")
add("French", "ws", "mallarme-crise-de-vers", "Stéphane Mallarmé, « Crise de vers », in Divagations (Paris: Fasquelle, 1897) — French Wikisource", "Je dis : une fleur", lang="fr", title="Divagations (1897)/Crise de vers")
add("French", "ws", "apollinaire-esprit-nouveau", "Guillaume Apollinaire, « L'Esprit nouveau et les poètes », Mercure de France 130, no. 491 (1 December 1918) — French Wikisource", "esprit nouveau", lang="fr", title="L’Esprit nouveau et les poètes")
# Spanish
add("Spanish", "ws", "lope-arte-nuevo", "Lope de Vega, Arte nuevo de hacer comedias en este tiempo (1609) — Spanish Wikisource", "Arte nuevo", lang="es", title="Arte nuevo de hacer comedias en este tiempo")
add("Spanish", "ws", "dario-palabras-liminares", "Rubén Darío, « Palabras liminares », Prosas profanas (1896; the 1917 edition) — Spanish Wikisource", "un manifiesto", lang="es", title="Prosas profanas: Palabras liminares")
add("Spanish", "ws", "huidobro-arte-poetica", "Vicente Huidobro, « Arte poética », El espejo de agua (Buenos Aires: Orión, 1916) — Spanish Wikisource", "El poeta es un pequeño Dios", lang="es", title="Arte poética")
add("Spanish", "ws", "quiroga-decalogo", "Horacio Quiroga, « Decálogo del perfecto cuentista », Babel (Buenos Aires, July 1927) — Spanish Wikisource", "Cree en un maestro", lang="es", title="Decálogo del perfecto cuentista")
# Portuguese
add("Portuguese", "ws", "bilac-profissao-de-fe", "Olavo Bilac, « Profissão de fé », Poesias (Rio de Janeiro, 1888) — Portuguese Wikisource", "Invejo o ourives quando escrevo", lang="pt", title="Profissão de Fé")
# German
add("German", "text", "opitz-deutsche-poeterey", "Martin Opitz, Buch von der Deutschen Poeterey (Breslau, 1624) — Project Gutenberg #34806", "Poeterey", url=PG.format(34806), path="gutenberg-34806.txt", source="Project Gutenberg")
add("German", "text", "lessing-laokoon", "Gotthold Ephraim Lessing, Laokoon: oder über die Grenzen der Mahlerey und Poesie (Berlin: Voß, 1766) — Project Gutenberg #6889", "Laokoon", url=PG.format(6889), path="gutenberg-6889.txt", source="Project Gutenberg")
add("German", "ia_ref", "schiller-naive-sentimentalische-1885", "Friedrich Schiller, Über naive und sentimentalische Dichtung (1795–1796), school edition with introduction (1885; Bayerische Staatsbibliothek copy) — OCR layer", "sentimentalische", identifier="11640865bsb", scan="11640865bsb.pdf")
# Russian
add("Russian", "ws", "pushkin-poetu", "Александр Пушкин, «Поэту» (Pushkin, To the Poet, 1830) — Russian Wikisource", "Поэт! не дорожи любовию народной", lang="ru", title="Поэту (Пушкин)")
add("Russian", "ws", "mayakovsky-kak-delat-stikhi", "Владимир Маяковский, «Как делать стихи?» (Mayakovsky, How Are Verses Made?, 1926) — Russian Wikisource", "Как делать стихи", lang="ru", title="Как делать стихи? (Маяковский)")
# English
add("English", "text", "sidney-defence", "Sir Philip Sidney, A Defence of Poesie (1595), with Poems — Project Gutenberg #1962", "Now for the poet, he nothing", url=PG.format(1962), path="gutenberg-1962.txt", source="Project Gutenberg")
add("English", "text", "pope-essay-on-criticism", "Alexander Pope, An Essay on Criticism (1711) — Project Gutenberg #7409", "A little learning is a dang", url=PG.format(7409), path="gutenberg-7409.txt", source="Project Gutenberg")
add("English", "text", "wordsworth-lyrical-ballads-1800", "William Wordsworth, Lyrical Ballads, with Other Poems (1800), vol. 1, with the Preface — Project Gutenberg #8905", "spontaneous overflow of powerful feelings", url=PG.format(8905), path="gutenberg-8905.txt", source="Project Gutenberg")
add("English", "text", "coleridge-biographia", "Samuel Taylor Coleridge, Biographia Literaria (1817) — Project Gutenberg #6081", "willing suspension of disbelief", url=PG.format(6081), path="gutenberg-6081.txt", source="Project Gutenberg")
add("English", "text", "keats-letters", "Letters of John Keats to His Family and Friends, ed. Sidney Colvin (1891) — Project Gutenberg #35698", "Negative Capability", url=PG.format(35698), path="gutenberg-35698.txt", source="Project Gutenberg")
add("English", "text", "shelley-defence", "Percy Bysshe Shelley, A Defence of Poetry (written 1821, printed 1840), and Other Essays — Project Gutenberg #5428", "unacknowledged legislators", url=PG.format(5428), path="gutenberg-5428.txt", source="Project Gutenberg")
add("English", "text", "emerson-essays-second-series", "Ralph Waldo Emerson, Essays: Second Series (1844), opening with “The Poet” — Project Gutenberg #2945", "metre-making argument", url=PG.format(2945), path="gutenberg-2945.txt", source="Project Gutenberg")
add("English", "ws", "poe-philosophy-of-composition", "Edgar Allan Poe, “The Philosophy of Composition”, Graham's Magazine (April 1846) — English Wikisource", "Nevermore", lang="en", title="The Philosophy of Composition")
add("English", "ws", "poe-poetic-principle", "Edgar Allan Poe, “The Poetic Principle” (1850), in The Works of the Late Edgar Allan Poe, vol. 2 (1859) — English Wikisource", "heresy of The Didactic", lang="en", title="The Works of the Late Edgar Allan Poe (1859)/Volume 2/The Poetic Principle")
add("English", "text", "moore-poems-1921", "Marianne Moore, Poems (London: Egoist Press, 1921), with “Poetry” — Project Gutenberg #62833", "imaginary gardens with real toads", url=PG.format(62833), path="gutenberg-62833.txt", source="Project Gutenberg")
add("English", "ws", "eliot-tradition-individual-talent", "T. S. Eliot, “Tradition and the Individual Talent” (The Egoist, 1919), in The Sacred Wood (London: Methuen, 1920) — English Wikisource", "historical sense", lang="en", title="The Sacred Wood/Tradition and the Individual Talent")
add("English", "extract", "sigil-tradition-individual-seismograph", "Johannes Sigil, “Tradition and the Individual Seismograph, or, Developing the Historical Poetics of Some Themes Introduced in Lee Sharks' ‘Pearl’”, in Pearl and Other Poems (2014), pp. 96–100 — copied from this library's Pearl seat, to stand beside Eliot's", "The poet is like a seismograph",
    **{"from": "/home/claude/alexanarch/data/corpora/pearl-and-other-poems/text/pearl-machine-text.txt", "from_rel": "data/corpora/pearl-and-other-poems/text/pearl-machine-text.txt", "lines": [5452, 5654], "seat_of_source": "pearl-and-other-poems"})

spec = {
 "corpus": "ars-poetica",
 "seat": "EA-CORPORA-29/04",
 "title": "Ars Poetica: the art of poetry in twenty traditions — Greek, Latin, Sanskrit, Tamil, Chinese, Japanese, Korean, Hebrew, Arabic, Persian, Old Norse, Irish, Occitan, Italian, French, Spanish, Portuguese, German, Russian and English",
 "language": "mul",
 "fetched": "2026-10-28",
 "license": {
  "payload": "Per item, recorded in origin.items. The underlying works are in the public domain in the United States (first published before 1931, or ancient and medieval texts in editions published before 1931), except Sigil's essay, which is the archive's own (CC BY 4.0, by the author). Packagings: Perseus TEI CC BY-SA 4.0; Wikisource pages CC BY-SA 4.0 for the site's contributions; Project Gutenberg texts under the PG licence; Aozora Bunko texts under its terms for public-domain works. The GRETIL Sanskrit files are CC BY-NC-SA 4.0 at the file: handled under the NC payload/record split ruled at EA-CORPORA-02 — the NonCommercial payload licence is carried forward unmodified and does not attach to this seat record. The Arabic Wikisource pages do not name the printed edition they transcribe: edition-level status recorded as UNVERIFIED AT SEAT TIME.",
  "record": "CC-BY-4.0 applies to this seat record only."
 },
 "normalization": "Originals as fetched under original/ (TEI, Wikisource HTML as served with its revision id, Gutenberg text, Aozora XHTML in Shift_JIS, Internet Archive OCR layers and scans). text/<slug>.txt derived by code: TEI reduced to lines; Wikisource parser output with navigation, edit links and reference markers dropped (several pages of one work joined under '=== <title> ===' headings); Aozora main text with ruby readings kept in 《》 after their base; Gutenberg and OCR text with line endings normalized. No text corrected by hand. Drop capitals set as images or styled initials on Wikisource can fall out of the text layer (Darío's first word reads 'espués').",
 "units": "one text file per work; each work carries its tradition as class",
 "items": items,
 "loci": loci,
 "classes": ["Greek", "Latin", "Sanskrit", "Tamil", "Chinese", "Japanese", "Korean", "Hebrew", "Arabic", "Persian", "Old Norse", "Irish", "Occitan", "Italian", "French", "Spanish", "Portuguese", "German", "Russian", "English"],
 "cross_references": {
  "already_on_the_shelf": "Not seated twice: Plato's Ion, Phaedrus and Republic (plato); Aristotle's Poetics (aristotle); Longinus, On the Sublime (longinus); Horace's Ars Poetica and Epistles (horace, 29/02); Ovid's Ars amatoria, Remedia, Tristia and Ex Ponto (ovid, 29/03); Aristophanes' Frogs (aristophanes); Whitman's 1855 Preface (whitman, LG1855); Blake (blake); Dickinson's manuscripts and her letters to Higginson in the Letters of 1894 (dickinson-mss); Langston Hughes's 'The Negro Artist and the Racial Mountain' in The Nation of 23 June 1926 (langston-hughes); the Futurist and Russian Futurist manifestos (futurism); Dada (dada); Pound's essays and Des Imagistes (pound, pound-ii); Stein (stein); Pessoa (pessoa, pessoa-full); the Russian Formalists (russian-formalism); Mallarmé's Coup de dés and Apollinaire's Calligrammes (visual-poetry); Belief & Technique for Telepathic Prose, Make It Human and Sigil's essay in the whole (pearl-and-other-poems; 29/07)",
  "beside_eliot": "Sigil's 'Tradition and the Individual Seismograph' is seated next to Eliot's 'Tradition and the Individual Talent' by the author's ruling: the essay takes Eliot's historical sense as its tool and turns the poet from recorder into seismograph whose tremors may create the earthquake they register."
 },
 "queued": [
  "Archibald MacLeish, “Ars Poetica”, Streets in the Moon (Boston: Houghton Mifflin, 1926): public domain in the United States; not on English Wikisource, and no scan found this session",
  "Rainer Maria Rilke, Briefe an einen jungen Dichter (Leipzig: Insel, 1929): both Internet Archive copies (the 1932 printing) are access-restricted (lending library), and no other copy was found",
  "Moses ibn Ezra, Kitāb al-muḥāḍara wa-l-mudhākara (the Hebrew poetics in Judaeo-Arabic) and its Hebrew translation by B. Halper, Shirat Yisrael (Leipzig, 1924): no fetchable copy found this session",
  "Zeami, Fūshikaden: no public-domain digital text found (Aozora Bunko and Japanese Wikisource hold none)",
  "Ibn Qutayba, al-Shiʿr wa-l-shuʿarāʾ: the Arabic Wikisource transcription is incomplete",
  "Raimon Vidal, Razos de trobar: no fetchable copy found this session",
  "Torquato Tasso, Discorsi dell'arte poetica: not found on Italian Wikisource",
  "Geoffrey of Vinsauf, Poetria nova, and the twelfth- and thirteenth-century Latin arts are seated inside Faral (1924) only as OCR"
 ],
 "scope": "Arts of poetry: treatises, prefaces, letters, manifestos and poems about the making of poems, chosen for range — one or more per tradition, from the Nāṭyaśāstra and the Great Preface to the Odes through Mayakovsky, Hagiwara and MacLeish. Copyrighted moderns and contemporary arts of poetry are declared in 29/06 (ars-poetica-wanted).",
 "why_seated": "Gathered for the next EA-CORPORA deposit at the author's direction ('an extremely pluriform ars poetica bundle … include telepathic prose'; 'take that extremely pluriform further globally, hebrew, sanskrit, korean'), around Belief & Technique for Telepathic Prose (#1715), Jack Feist's art of poetry, so that the comic ars poetica stands among the arts it answers.",
 "spine": "29/04",
 "ruling": "The author's directions of 2026-10-28; 'Tradition and the Individual Seismograph' beside Eliot's by his ruling.",
 "seating": "EA-CORPORA-29 (gathered; the deposit that assigns its AXN is pending)"
}
(HERE / "spec29-ars-poetica.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(items), "items", len(loci), "loci")
