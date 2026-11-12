# EA-CORPORA-37 — The Slavonic Josephus

At the operator's words of 2026-11-12 (12:48, 13:16, 13:20, 13:28 EST), with Rebekah Cranes as the standing authority on the EA-CORPORA deposits. Research occasion: The Josephus Thesis (#1759) and the challenge to the consensus reading of the Slavonic as spurious. Supplies the text layer of EA-CORPORA-01/12 (#1510).

- 37/01–37/04: `build_seats37a.py <download dir>` (Meshcherskii 1958 from Internet Archive 1958_20250223, cut to lines 9334–31517; Berendts–Grass, Tartu OJS articles 29178, 29182, 29169, 29164, pdftotext; Loeb III josephuswithengl03joseuoft; Eisler iesousbasileusou0001eisl, 0002eisl), then the index entries.
- 37/05–37/07: built in session with build_seats37a.py's write_seat helper: Berendts 1906 cut from texteundunter28v29akad lines 69133–73289; Berendts 1904 cut from dreigeorgischerh26hippuoft lines 24850–29439; Berendts 1895 studienberzachar0000bere whole.
- 37/08–37/12: the same helper: Eisler themessiahjesusand; eisler-robert-flavius-josephus-studien-i.-das-testimonium-flavianum-methuen-1938-64pp-os; orpheusfisher0000robe; MN41506ucmf_0; weltenmantelundh01eisl and 02eisl.
- After the deposit: `python3 rebuild/corpora/ea-corpora-37/seat_axns37.py <N> --apply`; body: `python3 rebuild/corpora/ea-corpora-37/body37.py`.
