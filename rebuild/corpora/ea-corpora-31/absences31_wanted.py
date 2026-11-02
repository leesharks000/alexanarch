#!/usr/bin/env python3
"""EA-CORPORA-31 (session tool): transmission-wanted (31/11), a declared absence in the form of absences30_wanted.py — the
editions and studies of the Peripatetic transmission the thirty-first seating could not hold: the modern editions and
studies still in their United States term, and the public-domain witnesses no usable copy was found for this session.
    python3 absences31_wanted.py <stage>      (the stage is data/corpora)"""
import json, hashlib, pathlib, sys
ST = pathlib.Path(sys.argv[1])
def fo(y):
    return f"{y + 96}-01-01 in the United States (ninety-five years from first publication abroad)"
PD = "open now (public domain in the United States); wanted: no usable copy found this session"

W = [
 ("Public domain, no copy found", "Sotion of Alexandria", "Διαδοχαὶ τῶν φιλοσόφων (Successions of the Philosophers), fragments", "", None,
  PD + " (Sotion is not among the authors the DFHG gives on 2026-11-01; his fragments are quoted in Diogenes Laertius, seated, and in Athenaeus, seated at 31/01)"),
 ("Public domain, no copy found", "Ibn Abī Uṣaybiʿa, ed. A. Müller", "ʿUyūn al-anbāʾ fī ṭabaqāt al-aṭibbāʾ", "Cairo; Königsberg", 1882,
  PD + "; the text is seated from a modern printing at 31/05"),
 ("Public domain, no copy found", "Ibn al-Qifṭī, ed. J. Lippert", "Taʾrīkh al-ḥukamāʾ", "Dieterich, Leipzig", 1903,
  PD + " (OpenITI holds an uncorrected OCR, 0646IbnQifti.TarikhHukama.Kraken220308195636-ara1, not seated); the Ikhbār is seated at 31/05"),
 ("Public domain, found, not seated", "Valentin Rose", "Aristoteles pseudepigraphus", "Teubner, Leipzig", 1863,
  "open now (public domain); the Internet Archive holds several copies (valentiniroseari00aris and others) whose OCR reads the Greek as Latin; to be seated with an OCR made for it"),
 ("Opening", "Paul Moraux", "Les listes anciennes des ouvrages d'Aristote", "Éditions universitaires, Louvain", 1951, fo(1951)),
 ("Opening", "Ingemar Düring", "Aristotle in the Ancient Biographical Tradition (Studia Graeca et Latina Gothoburgensia 5)", "Almqvist & Wiksell, Göteborg", 1957, fo(1957)),
 ("Opening", "Ingemar Düring", "Aristoteles: Darstellung und Interpretation seines Denkens", "Carl Winter, Heidelberg", 1966, fo(1966)),
 ("Opening", "Rudolf Pfeiffer", "Callimachus I: Fragmenta", "Clarendon Press, Oxford", 1949, fo(1949)),
 ("Opening", "Rudolf Pfeiffer", "Callimachus II: Hymni et epigrammata", "Clarendon Press, Oxford", 1953, fo(1953)),
 ("Opening", "Fritz Wehrli", "Die Schule des Aristoteles, Supplementband I: Hermippos der Kallimacheer", "Schwabe, Basel", 1974, fo(1974)),
 ("Opening", "Fritz Wehrli", "Die Schule des Aristoteles, Supplementband II: Sotion", "Schwabe, Basel", 1978, fo(1978)),
 ("Opening", "Jan Bollansée", "Die Fragmente der griechischen Historiker Continued IV A 3: Hermippos of Smyrna", "Brill, Leiden", 1999, fo(1999)),
 ("Opening", "Rudolf Blum", "Kallimachos und die Literaturverzeichnung bei den Griechen", "Buchhändler-Vereinigung, Frankfurt am Main", 1977, fo(1977)),
 ("Opening", "Paul Moraux", "Der Aristotelismus bei den Griechen I: Die Renaissance des Aristotelismus im I. Jh. v. Chr.", "de Gruyter, Berlin", 1973, fo(1973)),
 ("Opening", "L. G. Westerink", "Anonymous Prolegomena to Platonic Philosophy", "North-Holland, Amsterdam", 1962, fo(1962)),
 ("Opening", "W. W. Fortenbaugh, P. M. Huby, R. W. Sharples, D. Gutas", "Theophrastus of Eresus: Sources for his Life, Writings, Thought and Influence", "Brill, Leiden", 1992, fo(1992)),
]
title = "The Transmission, wanted — a declared absence: Moraux, Düring, Pfeiffer, Wehrli and the modern editions of the lists, lives and fragments, with the public-domain witnesses no usable copy was found for"
why = ("The editions and studies of the Peripatetic transmission the thirty-first seating could not hold, declared beside the texts it holds (31/01–31/10), at the author's "
       "direction to gather and seat the debts of the study Legitimately Many (2026-11-01). Twelve are still in their United States term and open on the dates given; four are "
       "open now and wanted because no usable copy was found this session. The modern editions are where the twentieth century numbered the lists and fragments the seated "
       "texts carry, so each entry names what the study cites from it.")
wanted = ("Wanted: Rose's Aristoteles pseudepigraphus with an OCR made for it, Müller's Ibn Abī Uṣaybiʿa and Lippert's Ibn al-Qifṭī first; then Pfeiffer in 2046 and 2050, "
          "Moraux in 2047, Düring in 2054.")
shelf = ("Beside athenaeus (31/01), galen (31/02), porphyry (31/03), aristotle-commentators (31/04), arabic-biobibliography (31/05), hermippus (31/06), hesychian-catalogue "
         "(31/07), callimachus-pinakes (31/08), bekker-aristotle-1831 (31/09) and jaeger-aristoteles (31/10); Diogenes Laertius, Strabo, Plutarch, Aristotle and Theophrastus "
         "are seated already.")
seat = ST / "transmission-wanted"; (seat / "declared").mkdir(parents=True, exist_ok=True)
L = [dict(**{"class": c}, author=a, title=t, first_publisher=p, first_published=y, opens=o) for c, a, t, p, y, o in W]
doc = {"declared_absence": title, "kind": "copyright, and copies not found", "rights": "The authors, their estates and first publishers, as named.", "works": L,
       "wanted": wanted, "on_the_shelf": shelf, "note": "This seat holds no text of the works it names. The dates follow the terms stated; they are not legal advice."}
(seat / "declared/absence.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
md = [f"# {title}", "", why, "", "| Class | Author | Work | First publisher | Year | Opens |", "|---|---|---|---|---|---|"]
md += [f"| {w['class']} | {w['author']} | {w['title']} | {w['first_publisher'] or '—'} | {w['first_published'] or '—'} | {w['opens']} |" for w in L]
md += ["", wanted, "", shelf, "", doc["note"]]
(seat / "declared/absence.md").write_text("\n".join(md) + "\n", encoding="utf-8")
src = {"corpus": "transmission-wanted", "seat": "EA-CORPORA-31/11", "title": title,
       "edition": "No edition held. The seat holds the declaration of what it would hold: declared/absence.json and declared/absence.md.",
       "language": "mul", "license": {"payload": "The declaration is the archive's own, CC-BY-4.0. The works it names are not held.", "record": "CC-BY-4.0 applies to this seat record only."},
       "fetched": "2026-11-01",
       "origin": {"items": [{"source": "Alexanarch deposit", "file": "declared/absence.json"}, {"source": "Alexanarch deposit", "file": "declared/absence.md"}],
                  "fetched": "2026-11-01", "transport": "written in session (Transport D); No-Double-Draw"},
       "works": {"count": 0, "units": f"no works held; {len(L)} declared", "list": []},
       "normalization": "None: the declaration is held as written.",
       "scope": "Declared without text: " + "; ".join(f"{w['author']}, {w['title']}" + (f" ({w['first_publisher']}, {w['first_published']})" if w['first_published'] else "") + f", opens: {w['opens']}" for w in L) + ". " + wanted,
       "classes": sorted({w["class"] for w in L}, key=[x[0] for x in W].index),
       "declared_absences": L, "verified_loci": [], "loci_not_found": [], "lines_total": 0,
       "why_seated": why, "spine": "EA-CORPORA-31",
       "ruling": 'Lee Sharks, 2026-11-01, of the texts named in §5 of the design Legitimately Many: "lets gather and seat those. with an ea-corpora".',
       "seating": "EA-CORPORA-31, the thirty-first seating: the transmission of the Peripatetic corpus, 2026-11-01"}
(seat / "source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
m = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(seat).as_posix()}" for p in sorted(seat.rglob('*')) if p.is_file() and p.name not in ('MANIFEST.sha256', 'source.json')]
(seat / "MANIFEST.sha256").write_text("\n".join(m) + "\n")
print("transmission-wanted", len(L), "declared")
