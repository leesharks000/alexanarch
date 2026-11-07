"""EA-CORPORA-36 loci: each asserted present, whitespace-normalized, in the text layer it names, in the layer's own readings (long s, OCR
breaks and all), then written into the seat's spec.   python3 add_loci36.py"""
import json
C = '../../../data/corpora/'
norm = lambda s: " ".join(s.split())
L = {
'hall-peri-hypsous-1652': [
 ("Hall: Sappho's choice and binding of the accidents of love", "hall-1652", "Thus did Sappho ſingle out all thoſe accidents that are either inherent or conſequentiall to love and melancholy"),
 ("Hall's fr. 31, its first line", "hall-1652", "He that ſits next thee now and hears Thy charming voyce to me appears"),
 ("Hall's fr. 31, the closing line carried over from the fifth stanza", "hall-1652", "I ſeem a Ghoſt. Yet ſince I'me wretched I muſt dare.")],
'boileau-traite-du-sublime-1683': [
 ("Boileau: when Sappho would express the furies of love (OCR)", "boileau-1683", "Ainfi, quand Sapho veut exprimer les fureurs de P Amour"),
 ("Boileau's fr. 31, its first line (OCR)", "boileau-1683", "Heureux ! qui près de toi , pour toi feule foupire"),
 ("Boileau's fr. 31, the fifth stanza's opening as its closing line (OCR)", "boileau-1683", "Mats quand on na plus rien^il faut tout hasar- der")],
'spectator-229-1711': [
 ("Spectator No. 229, Addison, 22 November 1711", "spectator-1891", "No. 229. Thursday, Nov. 22, 1711. Addison."),
 ("Addison on Boileau's version", "spectator-1891", "The Reader will see that this is rather an Imitation than a Translation."),
 ("Philips's fr. 31, its first line", "spectator-1891", "Blest as th'immortal Gods is he,"),
 ("Philips's fr. 31, its last line", "spectator-1891", "I fainted, sunk, and dy'd away."),
 ("Morley's note: a line wanting in the copies, supplied by conjecture", "spectator-1891", "Wanting in copies then known, it is here supplied by conjecture.")],
'pope-sapho-to-phaon': [
 ("Pope: Sappho to Phaon, from the fifteenth of Ovid's epistles", "pope-poetical-works-ii", "SAPPHO TO PHAON. FROM THE FIFTEENTH OF OVID'S EPISTLES."),
 ("Pope: the letter known by its hand", "pope-poetical-works-ii", "Can Phaon's eyes forget his Sappho's hand?")],
'fawkes-anacreon-sappho-1760': [
 ("Fawkes on Philips's first three lines (OCR)", "fawkes-1760", "the three firft Lines are ama- zingly rough and awkward"),
 ("Fawkes quoting Philips's first line (OCR)", "fawkes-1760", "Bleft as th' immortal Gods is he")],
'welcker-sappho-1816': [
 ("Welcker's title: freed of a ruling prejudice (OCR)", "welcker-1816", "von einem herrſchenden Vorurtheil befreyt")],
'merivale-poems-1838': [
 ("Merivale: From Sappho. A Fragment (1813)", "merivale-1838-i", "ADDITIONAL EPIGRAMS. 1813. FROM SAPPHO. A FRAGMENT. Blest as the immortal Gods is he,"),
 ("Merivale's fr. 31, its close at the failing of sight and sound", "merivale-1838-i", "I grow ; and then — together fail Both sight and sound !")],
'mure-critical-history-1850': [
 ("Mure's contents: Sappho, her love for Phaon, her Leucadian leap (OCR)", "mure-1850-iii", "7. Her love for Phaon. Her lyeucadian leap."),
 ("Mure's appendix on Sappho's character (OCR)", "mure-1850-iii", "On the personal characters of Anacreoii, Archilochus, and Sappho")],
'swinburne-poems-and-ballads-1866': [
 ("Swinburne: Anactoria, with its Greek epigraph from fr. 1", "swinburne-1866", "ANACTORIA [Greek: tinos au ty peithoi maps sageneusas philotata?] SAPPHO."),
 ("Swinburne: the speaker claims the future", "swinburne-1866", "Yea, though thou diest, I say I shall not die."),
 ("Swinburne: Sapphics, its first line", "swinburne-1866", "SAPPHICS All the night sleep came not upon my eyelids,")],
'higginson-atlantic-essays-1871': [
 ("Higginson's 'Sappho', its opening (OCR)", "higginson-1871", "THE voyager in the -^gean Sea, who has grown weary of the prevailing barrenness of the Grecian Isles")],
'symonds-studies-greek-poets-1873': [
 ("Symonds's contents: the flourishing period of Lesbos, Sappho (OCR)", "symonds-1873", "The Flourishing Period of Lesbos. — Sappho.—Alczeus.—Anacreon"),
 ("Symonds: Sappho simply sings her love", "symonds-1873", "Sappho simply sings her love ; Archilochus, his hatred")],
'vivien-sapho-1903': [
 ("Vivien's prose fr. 31, 'Ode à une Femme aimée' (OCR)", "vivien-1903", "Ode à une Femme aimée Il me parait l'égal des Dieux"),
 ("Vivien's prose fr. 31 carries the fifth stanza's opening", "vivien-1903", "je semble presque une morte... Mais il faut oser tout..."),
 ("Vivien's verse fr. 31, its first line", "vivien-1903", "L'homme fortuné qu'enivre ta présence Me semble l'égal des Dieux")],
'carman-sappho-1904': [
 ("Roberts's introduction: restoring statues from a broken arm", "carman-1907", "to restore some statues of Polyclitus or Praxiteles of which he had but a broken arm"),
 ("Roberts: each lost lyric imagined as discovered, then translated", "carman-1907", "Mr. Carman’s method, apparently, has been to imagine each lost lyric as discovered, and then to translate it")],
'wharton-sappho-1908': [
 ("Wharton's edition statement: the fifth edition, 1908", "wharton-1908", "_Fifth Edition. Fcap. 8vo. Pp._ xxxii+217."),
 ("Wharton's literal fr. 31: the closing the January composition aligns with", "wharton-1908", "But I must dare all, since one so poor_ ...")],
'renderings-1910-1920': [
 ("O'Hara's title page (1910)", "ohara-1910", "An Interpretative Rendition into English BY JOHN MYERS O'HARA PORTLAND: MDCCCCX"),
 ("Stacpoole's preface, its opening", "stacpoole-1920", "Sappho lies remote from us, beyond the fashions and the ages")],
'wilamowitz-sappho-und-simonides-1913': [
 ("Wilamowitz: on Welcker's tracks", "wilamowitz-1913", "von ihren Versen in ihre Seele vorzudringen, auf Welckers Spuren."),
 ("Wilamowitz: no mascula Sappho", "wilamowitz-1913", "sie war keine mascula Sappho und unter die Suffragettes wäre sie nicht gegangen.")],
'robinson-sappho-and-her-influence-1924': [
 ("Robinson's epigraph (Lucy Milburn): nations yet unborn", "robinson-1924", "This title till the stars do fall, Nations yet unborn shall call And glorify her name."),
 ("The series: Our Debt to Greece and Rome (OCR)", "robinson-1924", "CONTRIBUTORS TO THE “OUR DEBT TO GREECE AND ROME FUND,”")],
'cox-poems-of-sappho-1925': [
 ("Cox's bibliography: the 1680 English Longinus, the second translation of fr. 31 (OCR)", "cox-1925", "translated out of French by Mr. J. Pulteney. London, 1680. 8vo. Second translation of"),
 ("Cox's bibliography: Dacier's Sappho of 1681 (OCR)", "cox-1925", "Les Poesies d’Anacréon et de Sappho traduites de Grec en Francois avec des Remarques. Paris, 1681.")],
'remembrance-dossier': [
 ("Dio Chrysostom Or. 37.47 (Favorinus): fr. 147, 'finely said by Sappho'", "dio-orationes", "μνάσεσθαί τινά φαμι καὶ ἕτερον ἀμμέων. πάνυ γὰρ καλῶς εἶπεν ἡ Σαπφώ"),
 ("Dio 37.47: Hesiod on undying report, and the speaker's own statue set up beside the goddess", "dio-orationes", "φήμη δ’ οὔτις πάμπαν ἀπόλλυται, ἥντινα λαοὶ πολλοὶ φημίξωσι· θεός νύ τίς ἐστι καὶ αὐτή. ἐγώ σε ἀναστήσω παρὰ τῇ θεῷ"),
 ("Plutarch, Coniugalia praecepta 145f–146a: Sappho proud of the καλλιγραφία of her songs, writing to a rich woman", "plutarch-coniugalia", "διὰ τὴν ἐν τοῖς μέλεσι καλλιγραφίαν ἐφρόνει τηλικοῦτον ὥστε γράψαι πρός τινα πλουσίαν"),
 ("Plutarch, Coniugalia praecepta (fr. 55, with the editor's text from 646f): no memory of you", "plutarch-coniugalia", "κατθανοῦσα δὲ κείσεαι, οὐδέ τις μναμοσύνα σέθεν ἔσεται"),
 ("Plutarch, Quaestiones convivales 646e–f: Sappho to an unmusical and unlearned woman", "plutarch-quaestiones-convivales", "μεμνῆσθαί μοι δοκῶ Σαπφοῦς λεγούσης πρός τινα τῶν ἀμούσων καὶ ἀμαθῶν γυναικῶν"),
 ("Stobaeus 3.4.12 (Hense): Sappho to an uneducated woman (OCR)", "stobaeus-hense-iii", "Σαπφοῦς πρὸς ἁπαίδευτον γυναῖκα"),
 ("P.Oxy. XV 1787: Sappho, Book IV (OCR)", "oxyrhynchus-papyri-xv", "1787. SAPPHO, BOOK iv."),
 ("P.Oxy. XV 1790 (Ibycus): Polycrates promised imperishable fame (OCR)", "oxyrhynchus-papyri-xv", "In the penultimate line the author addresses Polycrates, to whom he ascribes imperishable fame.")],
'anthology-sappho-epigrams': [
 ("AP 7.15 (Antipater): 'my name is Sappho'", "anthology-vol-ii", "οὔνομά μευ Σαπφώ. τόσσον δʼ ὑπερέσχον ἀοιδὰν"),
 ("AP 7.16 (Pinytus): the tomb holds the bones and mute name; her wise words are immortal", "anthology-vol-ii", "ὀστέα μὲν καὶ κωφὸν ἔχει τάφος οὔνομα Σαπφοῦς·"),
 ("AP 7.17 (Tullius Laurea): the stranger at the Aeolian tomb", "anthology-vol-ii", "Αἰολικὸν παρὰ τύμβον ἰών, ξένε, μή με θανοῦσαν"),
 ("AP 9.506 (attributed to Plato): Sappho the tenth Muse", "anthology-vol-iii", "ἠνίδε καὶ Σαπφὼ Λεσβόθεν ἡ δεκάτη."),
 ("AP 9.521: the Muses grant Sappho imperishable speech", "anthology-vol-iii", "σοὶ γὰρ ῥῆσιν ἐνεύσαμεν ἄφθιτον εἶμεν,")],
'smyth-greek-melic-poets-1900': [
 ("Smyth prints fr. 147 under Horace's 'non omnis moriar' (OCR)", "smyth-1900", "SAPPHO. X. (32). NON OMNIS MORIAR."),
 ("Smyth's fr. 147 (OCR)", "smyth-1900", "Μνάσεσθαί τινά φαμι καὶ ὕστερον ἀμμέων."),
 ("Smyth prints fr. 55 under 'Neglect of the Muses' (OCR)", "smyth-1900", "XXIV. (68). NEGLECT OF THE MUSES. Κατθάνοισα δὲ κείσεαι")],
'jebb-growth-and-influence-1893': [
 ("Jebb: Sappho's period, and the mass of fiction or calumny (OCR)", "jebb-1893", "From the mass of fiction or calumny which later literature")],
'wikipedia-sappho-20261106': [
 ("Wikipedia, 'Ancient editions': the 'some scholars' sentence and its one footnote", "wikipedia-sappho", "Some scholars believe that she wrote her own poetry down for future readers; others that if she wrote her works down it was as an aid to reperformance rather than as a work of literature in its own right.{{sfn|Lardinois|2008|pp=79&ndash;80}}")],
'cicero-tusculanae': [
 ("Ennius's epitaph as Cicero quotes it (Tusc. 1.34)", "tusculanae", "volito vivos per ora virum.")],
'dante-commedia': [
 ("Inf. 8.94: 'Pensa, lettor'", "commedia", "Pensa, lettor, se io mi sconfortai nel suon de le parole maladette"),
 ("Par. 2.1: the readers in the little boat", "commedia", "O voi che siete in piccioletta barca, desiderosi d’ascoltar")],
'chaucer-troilus': [
 ("Troilus 5.1786: the envoi", "troilus", "Go, litel book, go litel myn tragedie,"),
 ("Troilus 5.1795: against miswriting", "troilus", "So preye I god that noon miswryte thee,")],
'shakespeare-sonnets': [
 ("Sonnet 81: eyes not yet created", "sonnets", "Your monument shall be my gentle verse, Which eyes not yet created shall o’er-read;"),
 ("Sonnet 55: not marble", "sonnets", "Not marble, nor the gilded monuments Of princes, shall outlive this powerful rhyme;")],
'milton-paradise-lost': [
 ("Paradise Lost 7.31: fit audience, though few", "paradise-lost", "Urania, and fit audience find, though few.")],
'romantic-posterity': [
 ("Wordsworth to Lady Beaumont (1807), Coleridge's remark", "wordsworth-prose", "every great and original writer, in proportion as he is great or original, must himself create the taste by which he is to be relished"),
 ("Wordsworth, Essay, Supplementary to the Preface (1815)", "wordsworth-prose", "has had the task of _creating_ the taste by which he is to be enjoyed"),
 ("Keats to George and Georgiana Keats (October 1818)", "keats-letters", "I think I shall be among the English Poets after my death."),
 ("Shelley, A Defence of Poetry (1821)", "shelley-defence", "the mirrors of the gigantic shadows which futurity casts upon the present"),
 ("Stendhal, La Chartreuse de Parme, the last line", "stendhal-chartreuse", "TO THE HAPPY FEW")],
'dickinson-poems-1890-1896': [
 ("Dickinson: the letter to the world", "dickinson-1890-1896", "This is my letter to the world, That never wrote to me,")],
'baratynsky-moi-dar-ubog': [
 ("Baratynsky: the reader found in posterity", "moi-dar-ubog", "И как нашёл я друга в поколеньи, Читателя найду в потомстве я."),
 ("The page's commentary, Mandelstam's 'О собеседнике': the letter in the bottle", "moi-dar-ubog", "Письмо, запечатанное в бутылке, адресовано тому, кто найдет её.")],
'wipp-markers-sandia-1993': [
 ("SAND92-1382, Unlimited Release (OCR)", "sandia-1993", "Unlimited Release Printed November 1993 Expert Judgment on Markers to Deter"),
 ("The drafted message (OCR)", "sandia-1993", "This place is not a place of honor...no highly esteemed deed is commemorated here")],
}
for c, ls in L.items():
    f = f'spec36-{c}.json'; d = json.load(open(f, encoding="utf-8")); out = []
    texts = {w["slug"]: w for w in json.load(open(C + c + "/source.json", encoding="utf-8"))["works"]["list"]}
    for lab, item, find in ls:
        rel = texts[item]["text"]
        t = norm(open(C + c + "/" + rel, encoding="utf-8", errors="replace").read())
        assert norm(find) in t, (c, find)
        out.append({"label": lab, "text": rel, "find": find})
    d['loci'] = out
    json.dump(d, open(f, 'w', encoding="utf-8"), ensure_ascii=False, indent=1)
    print(c, len(out))
