# EA-CORPORA-30: brief for the seat readers (2026-10-30)

Repository: /home/claude/alexanarch, branch corpora-30-20261030. This folder: rebuild/corpora/ea-corpora-30/ (call it H). Seats land in /home/claude/alexanarch/data/corpora/<corpus>/.

## The ruling

Lee Sharks, 2026-10-30, asked for the seating: "and then an ea-corpora seating... Einstein, Gödel, Tesla, Copernicus, Galileo, classical Arabic mathematicians... what is in the public domain, and what else? and just to be perverse lets seat the promised Klee notebooks with them". To the proposed set he answered: "yes, thats a good set".

### The seats

| Seat | Corpus | What it holds |
|---|---|---|
| 30/01 | einstein | The five 1905 papers in the Annalen der Physik: photoelectric (Erzeugung und Verwandlung des Lichtes), Brownian motion (Bewegung … suspendierten Teilchen), Zur Elektrodynamik bewegter Körper, Ist die Trägheit eines Körpers …, and the dissertation Eine neue Bestimmung der Moleküldimensionen (Annalen 1906). Also the 1915 field equations (Sitzungsberichte der Preußischen Akademie, 25 Nov 1915), Die Grundlage der allgemeinen Relativitätstheorie (Annalen 1916), Kosmologische Betrachtungen (1917), and Über die spezielle und die allgemeine Relativitätstheorie (1917, any printing to 1920). |
| 30/02 | goedel | The 1930 completeness paper, "Die Vollständigkeit der Axiome des logischen Funktionenkalküls", Monatshefte für Mathematik und Physik 37 (1930), and the 1930 Königsberg abstract if found. The 1931 incompleteness paper is NOT seated: it opens in the US on 2027-01-01 and goes to the wanted seat. |
| 30/03 | tesla | My Inventions (Electrical Experimenter, 1919); the 1891 and 1892 lectures (Experiments with Alternate Currents of Very High Frequency …); "The Problem of Increasing Human Energy" (Century, 1900); the major patents (polyphase AC motor 1888, Tesla coil 382,845?/454,622, radio 645,576/649,621, transmission 1,119,732). Choose the canonical ones, about ten, and say why. |
| 30/04 | copernicus | De revolutionibus orbium coelestium (Nuremberg, 1543), Latin; the Commentariolus if a pre-1931 printing is found. |
| 30/05 | galileo | Sidereus nuncius (1610, Latin); Il Saggiatore (1623); Dialogo sopra i due massimi sistemi (1632); Discorsi e dimostrazioni matematiche (1638); the Lettera a Cristina di Lorena (1615). Italian and Latin. |
| 30/06 | kepler | Astronomia nova (1609); Harmonices mundi (1619); Mysterium cosmographicum (1596) if found. Latin. |
| 30/07 | newton | Philosophiae naturalis principia mathematica (1687 first edition preferred; 1713/1726 noted). Opticks (1704, English) if found. |
| 30/08 | arabic-mathematics | Arabic only. al-Khwārizmī, al-Kitāb al-mukhtaṣar fī ḥisāb al-jabr wa-l-muqābala (Rosen's Arabic text, London 1831, on IA as algebraofmohamme00khuwrich, and/or the "1342 … In Arabic" item). Thābit ibn Qurra and Ibn al-Haytham (Kitāb al-Manāẓir) from OpenITI (github.com/OpenITI/0300AH and 0450AH; raw.githubusercontent.com works, the GitHub API does not; a `git clone --depth 1 --filter=blob:none --no-checkout` lists trees). al-Kindī's mathematical and scientific works (OpenITI 0275AH). al-Bīrūnī where mathematical or astronomical. Khayyām's Risāla fī l-barāhīn ʿalā masāʾil al-jabr wa-l-muqābala (Woepcke, L'algèbre d'Omar Alkhayyâmî, Paris 1851, Arabic text). OpenITI is CC BY-NC-SA 4.0: those files fall under the NC payload/record split of EA-CORPORA-02, as GRETIL did in 29/09. Record the OpenITI release/commit. |
| 30/09 | paul-klee | **Done by the main session, not by you.** |
| 30/10 | quantum-founders | Heisenberg, "Über quantentheoretische Umdeutung kinematischer und mechanischer Beziehungen", Z. Physik 33 (1925). Born and Jordan, "Zur Quantenmechanik" (1925). Born, Heisenberg and Jordan (1926). Schrödinger, "Quantisierung als Eigenwertproblem" I–IV (Annalen der Physik 1926). Pauli's exclusion principle (Z. Physik 1925). Dirac, "The Quantum Theory of the Electron" (Proc. R. Soc. A 117, 1928). Bohr, the Como lecture as printed (Naturwissenschaften 16, 1928). All are published before 1931, so open in the US; the European terms still run, so say so. Seat what can be found; list what cannot. |
| 30/11 | archimedes-ptolemy | Archimedes in Heiberg's Greek and Ptolemy's Syntaxis (Almagest) in Heiberg's Greek. Look first in PerseusDL/canonical-greekLit and OpenGreekAndLatin/First1KGreek (tlg0552 Archimedes; tlg0363 Ptolemy; raw.githubusercontent.com, pinned to a commit), then IA scans of Heiberg's Teubner volumes. |
| 30/12 | exact-wanted | **Done by the main session.** |

Euclid is already seated (data/corpora/euclid, EA-CORPORA-20/04). Do not reseat it; cross-reference it from 30/11.

## How a seat is built

Read these first:
- rebuild/corpora/ea-corpora-29/NOTE.md;
- rebuild/corpora/ea-corpora-29/build29.py, its docstring and its kinds;
- rebuild/corpora/ea-corpora-27/seat.py, the kinds ia, tei, file and pages;
- one full spec, rebuild/corpora/ea-corpora-29/spec29-avant-garde-ii.json, and the ia_ref items in spec29-ars-poetica.json;
- an existing source.json, data/corpora/euclid/source.json.

Write one spec per seat, H/spec30-<corpus>.json. Build it with:
`cd H && python3 ../ea-corpora-29/build29.py spec30-<corpus>.json /home/claude/alexanarch/data/corpora`.
Re-verify loci without refetching with `--loci`. Iterate until the seat builds and its loci verify.

### Spec fields

- corpus
- seat: "EA-CORPORA-30/NN".
- title
- language: ISO 639-3, or "mul".
- fetched: "2026-10-30".
- license: {payload, record}, following the avant-garde spec's wording. US public domain is the archive's rule: published before 1931, or the author's term run. Name any term still running elsewhere.
- normalization: say plainly that no text was corrected by hand.
- units
- loci
- scope: what is held, and what is not and why.
- why_seated: two to four sentences, in the archive's register.
- spine: "EA-CORPORA-30".
- ruling: the operator's words above, with the date.
- seating: "EA-CORPORA-30, the thirtieth seating: the exact sciences and Klee's Bauhaus notebook, 2026-10-30".
- items
- queued: optional; works found but not seated, with the reason.

### Sources

- Original language always. The first or earliest available printing is preferred, as the witness.
- Internet Archive: identify items by the advancedsearch API (archive.org/advancedsearch.php) and read archive.org/metadata/<id> for the files and their md5.
  - Use kind "ia" to copy small scans with their _djvu.txt.
  - Use kind "ia_ref" for large scans: the OCR is copied, and the scan is held by identifier, file, size and md5.
  - Check the item's rights and licence fields, and record them.
- The OCR is the text layer as the Archive gives it. Do not correct it.
- Some sites refuse the seating's user agent. Gallica and e-rara refused on 2026-10-30. Record any refusal in the spec's queued or scope field, and use another holder. Do not change the user agent.
- Wikisource rate-limits the API; ws.py handles backoff. Keep the requests few.

### Loci

At least one locus per work, and two or three for the major works: a short, distinctive phrase that must appear verbatim (whitespace-normalized) in the text layer. Choose canonical passages: the first lines; a famous sentence or equation in words, if the OCR carries it; a proposition heading. Because the OCR is imperfect, choose phrases the OCR actually got right, and check them. A locus you could not find goes in loci_not_found honestly; never adjust a locus to match bad OCR without saying so in its note.

### Size

Keep each seat sensible. Copy a scan only under about 60 MB; otherwise use ia_ref.

## Rules for your prose (binding)

- Never "not X but Y", and never "X, not Y".
- No "rather than" or "instead of" outside quotations.
- Third person.
- No gendered generics.
- No hard line breaks inside a string.
- Plain words.

## Out of bounds

- Do not touch data/registry.json, data/api/corpora.json, datasets/, or any other seat.
- Do not commit.
- Do not run index_seats or the deposit pipeline.
- Edit only your own spec files and seat folders.

## What to report

For each seat:
- works seated, with lines and loci verified and not found;
- sizes;
- what was not found, and why;
- every licence decision;
- anything you are unsure of.

Report anything the main session must put on the wanted list (30/12): the work, why it is held, and its opening date.
