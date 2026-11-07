#!/usr/bin/env python3
"""EA-CORPORA-36 declared absences: the works of the reception and the future-reader frameworks that the seating does not hold, each
with the wall that keeps it out and a pointer where one was verified (in session or in the archive's earlier work). Commons only:
paywalled and copyrighted works are declared, not pursued.
  rights   in copyright; held by its publisher
  pay      behind a subscription or purchase wall (journal or database)
  access   open in law but not located in an open text layer in session, or the Archive's text layer returned an error
  private  held by a person; not published
    python3 rebuild/corpora/ea-corpora-36/absences36.py  -> rebuild/corpora/ea-corpora-36/absences36.json"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
P = "Part I §9 of #1548"   # the working bibliography the absence is drawn from
D = [
 # ---- the reception: texts and translations ----
 ("A", "access", "Anne Le Fèvre (Mme Dacier), Les poésies d'Anacréon et de Sapho traduites en françois (Paris, 1681)", "Public domain; no open text layer located in session (the Archive's 'Poésies d'Anacréon et de Sapho' items are of 1855 and 1882)."),
 ("A", "access", "J. P[ulteney], A Treatise of the Loftiness or Elegancy of Speech, translated out of French (London, 1680), the second English fr. 31 (Cox 1925, seated at 36/18, lists it)", "Public domain; the TCP transcription (EEBO-TCP A49144) is Restricted, as the Partnership's catalogue marks it."),
 ("A", "access", "N. Boileau-Despréaux, Traité du sublime, first edition (Paris, 1674)", "Public domain; the 1683 printing is seated at 36/02."),
 ("A", "access", "Aphra Behn (attrib.), the fr. 31 of 1694 in the teaching gallery", "Public domain; the printing was not located in session."),
 ("A", "access", "T. Smollett, The Adventures of Roderick Random (1748), with its fr. 31", "Public domain; not sought in this round (Wharton 1908, seated at 36/14, prints the rendering)."),
 ("A", "access", "Mary Robinson, Sappho and Phaon, in a Series of Legitimate Sonnets (London, 1796)", "Public domain; not located in session (her Poetical Works of 1806, at the Archive as poeticalworksinc01robiuoft and 02robiuoft, do not carry the sequence)."),
 ("A", "access", "Michael Field (K. Bradley and E. Cooper), Long Ago (London, 1889)", "Public domain; not located in session."),
 ("A", "access", "J. H. Merivale, Poems Original and Translated, vol. II (London, 1838)", "Public domain; the Archive's text layer (poemsoriginaltra02meri) returned an error in session. Volume I is seated at 36/07."),
 ("A", "access", "E. Lobel (ed.), Σαπφοῦς μέλη: The Fragments of the Lyrical Poems of Sappho (Oxford, 1925)", "Public domain in the United States (published 1925); in copyright elsewhere (Lobel died 1983). Not located in an open text layer in session."),
 ("A", "rights", "E. Lobel and D. L. Page (eds.), Poetarum Lesbiorum Fragmenta (Oxford, 1955)", "Oxford University Press."),
 ("A", "rights", "D. L. Page, Sappho and Alcaeus (Oxford, 1955)", "Oxford University Press."),
 ("A", "rights", "E.-M. Voigt (ed.), Sappho et Alcaeus: Fragmenta (Amsterdam, 1971)", "Athenaeum–Polak & Van Gennep."),
 ("A", "rights", "D. A. Campbell (ed. and trans.), Greek Lyric I: Sappho and Alcaeus, Loeb Classical Library 142 (1982; rev. 1990)", "Harvard University Press; the Loeb Classical Library online is a subscription."),
 ("A", "rights", "W. C. Williams, his Sappho (1957), in the teaching gallery", "In copyright (New Directions)."),
 ("A", "rights", "M. Barnard, Sappho: A New Translation (Berkeley, 1958)", "University of California Press."),
 ("A", "rights", "R. Lowell, Imitations (New York, 1961), with his Sappho", "Farrar, Straus and Giroux."),
 ("A", "rights", "W. Barnstone, Sappho (1965), in the teaching gallery", "In copyright."),
 ("A", "rights", "A. Carson, Eros the Bittersweet (Princeton, 1986) and If Not, Winter: Fragments of Sappho (New York, 2002)", "Princeton University Press; Knopf."),
 ("A", "rights", "D. J. Rayor, Sappho's Lyre (Berkeley, 1991)", "University of California Press."),
 ("A", "rights", "The anonymous homophonic version of fr. 31 (2013), in the teaching gallery", "In copyright; given in the gallery by reference."),
 ("A", "private", "The teaching gallery: a double-sided sheet of the English fr. 31 through Carson prepared and supplied by Yopie Prins, extended by the author for secondary classrooms", "Held by the author; described in Closing the Fragment v7 §6."),
 # ---- the reception: scholarship ----
 ("A", "rights", "Y. Prins, Victorian Sappho (Princeton, 1999)", "Princeton University Press."),
 ("A", "rights", "J. DeJean, Fictions of Sappho, 1546–1937 (Chicago, 1989)", "University of Chicago Press."),
 ("A", "rights", "M. Williamson, Sappho's Immortal Daughters (Cambridge, MA, 1995)", "Harvard University Press. " + P + "."),
 ("A", "rights", "P. duBois, Sappho Is Burning (Chicago, 1995)", "University of Chicago Press. " + P + "."),
 ("A", "rights", "E. Greene (ed.), Reading Sappho and Re-reading Sappho (Berkeley, 1996)", "University of California Press. " + P + "."),
 ("A", "rights", "M. Reynolds (ed.), The Sappho Companion (London, 2000) and The Sappho History (Basingstoke, 2003)", "Chatto & Windus; Palgrave Macmillan."),
 ("A", "rights", "D. Yatromanolakis, Sappho in the Making: The Early Reception (Washington, DC, 2007)", "Center for Hellenic Studies. " + P + "."),
 ("A", "rights", "E. Greene and M. B. Skinner (eds.), The New Sappho on Old Age (Washington, DC, 2009)", "Center for Hellenic Studies. " + P + "."),
 ("A", "rights", "A. Bierl and A. Lardinois (eds.), The Newest Sappho (Leiden, 2016), with E. Bowie's chapter on sympotic reperformance", "Brill. " + P + "."),
 ("A", "rights", "P. J. Finglass and A. Kelly (eds.), The Cambridge Companion to Sappho (Cambridge, 2021), with L. Kurke's chapter", "Cambridge University Press."),
 ("A", "rights", "F. Ferrari, Sappho's Gift (Ann Arbor, 2010)", "Michigan Classical Press. " + P + "."),
 ("A", "pay", "M. L. West, 'Burning Sappho', Maia 22 (1970), 307–30", "Subscription. " + P + "."),
 ("A", "pay", "R. Parker, 'The Audience of the Lyric Poets', Classical Review 31 (1981), 159–62", "Cambridge University Press (JSTOR)."),
 ("A", "rights", "E. Stein, in W. Kullmann and M. Reichel (eds.), Der Übergang von der Mündlichkeit zur Literatur bei den Griechen (Tübingen, 1990), 268–69", "Narr. Part I §4 of #1548, after Lardinois 2008: 79–80."),
 ("A", "rights", "The skeptics of early readership in Lardinois 2008 n. 3: R. Thomas, Literacy and Orality in Ancient Greece (Cambridge, 1992); A. Ford, in H. Yunis (ed.), Written Texts and the Rise of Literate Culture (Cambridge, 2003); and the performance side in his n. 4: H. Maehler, Die Auffassung des Dichterberufs (Göttingen, 1963), 59–63; A. Hardie (2005)", "Cambridge University Press; Vandenhoeck & Ruprecht. Part I §4 of #1548."),
 ("A", "rights", "E. J. Bakker on memory and performance (2002, 2005), cited at Lardinois 2008 n. 34; G. B. D'Alessio on past and future in lyric self-reference", "Part I §7 of #1548."),
 ("A", "pay", "H. N. Parker, 'Sappho Schoolmistress', TAPA 123 (1993), 309–51", "JSTOR. " + P + "."),
 ("A", "pay", "W. H. Race, '\"That Man\" in Sappho fr. 31', Classical Antiquity 2 (1983), 92–101", "JSTOR. " + P + "."),
 ("A", "pay", "J. B. Lidov, 'The Second Stanza of Sappho 31', AJP 114 (1993), 503–35", "JSTOR. " + P + "."),
 ("A", "pay", "A. Lardinois, 'Subject and Circumstance in Sappho's Poetry', TAPA 124 (1994), 57–84", "JSTOR. " + P + "."),
 ("A", "pay", "A. D'Angour, 'Conquering Love: Sappho 31 and Catullus 51', Classical Quarterly 56 (2006), 297–300", "Cambridge University Press."),
 ("A", "rights", "A. D'Angour, 'Love's Battlefield: Rethinking Sappho Fragment 31', in E. Sanders et al. (eds.), Erôs in Ancient Greece (Oxford, 2013), 59–71", "Oxford University Press; the author's proof is posted at armand-dangour.com (Closing the Fragment v7, References)."),
 ("A", "pay", "L. Battezzato, 'Objects and Memory in Sappho and Alcaeus', Classical Antiquity 43.2 (2024), 217–55", "University of California Press."),
 ("A", "access", "P. J. Finglass, 'Getting Sweaty with Sappho: New College MS 298', New College Notes 24.1 (2025)", "New College, Oxford, published online; read in session for Closing the Fragment v7 §6 by a summarizing fetch, its quotations to be checked against the PDF."),
 ("A", "rights", "B. Gentili, Poetry and Its Public in Ancient Greece (Baltimore, 1988)", "Johns Hopkins University Press. " + P + "."),
 ("A", "rights", "W. Rösler, Dichter und Gruppe (Munich, 1980)", "Fink. " + P + "."),
 ("A", "rights", "E. Stehle, Performance and Gender in Ancient Greece (Princeton, 1997), 262–318", "Princeton University Press. " + P + "."),
 ("A", "rights", "G. O. Hutchinson, Greek Lyric Poetry (Oxford, 2001); J. Herington, Poetry into Drama (Berkeley, 1985); G. Nagy (2013); D. E. Gerber (ed.), A Companion to the Greek Lyric Poets (Leiden, 1997)", P + "."),
 ("A", "access", "R. Garner, 'Oral Tradition and Sappho', Oral Tradition 26.2 (2011)", P + "; the journal publishes in open access; the article was not fetched in session."),
 ("A", "rights", "L. D. Reynolds and N. G. Wilson, Scribes and Scholars, 4th edn (Oxford, 2013); R. Pfeiffer, History of Classical Scholarship (Oxford, 1968)", "Oxford University Press."),
 ("A", "rights", "C. Martindale, Redeeming the Text (Cambridge, 1993); C. Martindale and R. F. Thomas (eds.), Classics and the Uses of Reception (Oxford, 2006); L. Hardwick, Reception Studies (Oxford, 2003); F. Budelmann and J. Haubold, 'Reception and Tradition' (2008)", "Cambridge University Press; Blackwell; Oxford University Press."),
 # ---- the future reader ----
 ("B", "rights", "J. Svenbro, Phrasikleia: anthropologie de la lecture en Grèce ancienne (Paris, 1988); trans. J. Lloyd (Ithaca, 1993), ch. 8", "La Découverte; Cornell University Press. Stratum I."),
 ("B", "rights", "A. Lardinois, '\"Someone, I Say, Will Remember Us\": Oral Memory in Sappho's Poetry', in E. A. Mackay (ed.), Orality, Literacy, Memory in the Ancient Greek and Roman World (Leiden, 2008), 79–96", "Brill; an open copy is held by the Radboud University repository, https://hdl.handle.net/2066/68171 (verified 2026-08-26, #1548 §10)."),
 ("B", "access", "Theognis 237–54, the seal passage addressed to Kyrnos", "Public domain; no open Greek text layer located in session (C. Ziegler's edition of 1880 is at the Archive as theognidiselegi00theogoog; its OCR reads the Greek as Latin). Stratum II."),
 ("B", "access", "О. Мандельштам, «О собеседнике» (Аполлон, 1913)", "Public domain in the United States (published 1913); not located whole in an open text layer in session. Its bottle passage is quoted in the commentary of the Baratynsky page seated at 36/26. Stratum VIII."),
 ("B", "access", "W. Benjamin, 'Die Aufgabe des Übersetzers', preface to Charles Baudelaire, Tableaux parisiens (Heidelberg, 1923)", "Public domain in the United States (published 1923) and the EU (Benjamin died 1940); not located in an open text layer in session. Stratum IX."),
 ("B", "rights", "W. Benjamin, 'Über den Begriff der Geschichte' (1940; first printed 1942)", "Public domain in the EU since 2011; in the United States its status was not established in session. Not located. Stratum IX."),
 ("B", "rights", "P. Celan, 'Ansprache anlässlich der Entgegennahme des Literaturpreises der Freien Hansestadt Bremen' (1958)", "Suhrkamp (Gesammelte Werke III). Stratum VIII."),
 ("B", "rights", "M. M. Bakhtin, 'Проблема текста' (written 1959–61; first printed 1976), the superaddressee", "In copyright; Speech Genres, trans. V. McGee (Austin, 1986). Stratum IX."),
 ("B", "rights", "M. Blanchot, Le Livre à venir (Paris, 1959)", "Gallimard. Stratum IX."),
 ("B", "rights", "W. Iser, Der implizite Leser (1972) and Der Akt des Lesens (1976); H. R. Jauss, Literaturgeschichte als Provokation (1970); U. Eco, Lector in fabula (1979)", "Fink; Suhrkamp; Bompiani. Stratum IX."),
 ("B", "pay", "W. Gibson, 'Authors, Speakers, Readers, and Mock Readers', College English 11 (1950); G. Prince, 'Introduction à l'étude du narrataire', Poétique 14 (1973); W. J. Ong, 'The Writer's Audience Is Always a Fiction', PMLA 90 (1975), 9–21", "JSTOR. Stratum IX."),
 ("B", "rights", "J. Derrida, 'Signature événement contexte' (1971; Marges de la philosophie, 1972) and La Carte postale (1980)", "Minuit; Flammarion. Stratum IX."),
 ("B", "pay", "E. Auerbach, 'Dante's Addresses to the Reader', Romance Philology 7 (1954), 268–78", "JSTOR. Stratum VI; the addresses are seated at 36/20."),
 ("B", "rights", "A. Bennett, Romantic Poets and the Culture of Posterity (Cambridge, 1999)", "Cambridge University Press. Stratum VII; the sentences it reads are seated at 36/24."),
 ("B", "rights", "J. Culler, Theory of the Lyric (Cambridge, MA, 2015); W. Waters, Poetry's Touch: On Lyric Address (Ithaca, 2003); H. Vendler, Invisible Listeners (Princeton, 2005)", "Harvard; Cornell; Princeton University Presses. Stratum X."),
 ("B", "pay", "N. Felson (ed.), The Poetics of Deixis in Alcman, Pindar, and Other Lyric, Arethusa 37.3 (2004), with E. J. Bakker", "Johns Hopkins University Press (Project MUSE). Stratum X."),
 ("B", "access", "Human Interference Task Force, Reducing the Likelihood of Future Human Activities That Could Affect Geologic High-Level Waste Repositories, BMI/ONWI-537 (1984), with T. A. Sebeok, Communication Measures to Bridge Ten Millennia (BMI/ONWI-532, 1984)", "United States government reports; not sought in this round. Stratum XI; SAND92-1382 is seated at 36/27."),
 ("B", "rights", "The Voyager Golden Record (NASA, 1977), and C. Sagan et al., Murmurs of Earth (New York, 1978)", "The record's contents are held by NASA/JPL; the book in copyright. Not sought in this round. Stratum XI."),
]
out = [{"part": p, "wall": w, "work": t, "status": s} for p, w, t, s in D]
(H / "absences36.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
from collections import Counter
print(len(out), "absences", dict(Counter(x["wall"] for x in out)))
