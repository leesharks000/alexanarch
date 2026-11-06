"""EA-CORPORA-35 spec generator: the sources of the study of Q (working title "I Know You Are, But What Am I? ... — Revelation First", Johannes Sigil and
Rebekah Cranes, Provenance: Journal of Forensic Semiotics), seated before drafting at the operator's word of 2026-11-06 11:07 EST ("we need ea-corpora
before the q paper"). Seven seats, the hypothetical source's making from Weisse to Streeter, each in its original language.   python3 gen_spec35.py"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
RULING = ("Lee Sharks, 2026-11-06 11:07 EST: \"so we need factual repairs versioned in place and the ea-corpora for q - lets do those as one bundle. "
          "we need ea-corpora before the q paper. and byline... lets say sigil and cranes. provenance\"; and 10:31 EST: \"we're coming for Q next\".")
SEATING = "EA-CORPORA-35, the thirty-fifth seating: the making of Q — the hypothetical source from Weisse to Streeter, 1838–1925, 2026-11-06"
RESEARCH = ("The study of Q opened 2026-11-06 (working title 'I Know You Are, But What Am I?: Or, How a Completely Hypothetical, Uninspectable Text Is "
            "Granted Evidentiary Status Symmetrical to One That Is Inspectable Because It Exists — Revelation First'; Johannes Sigil and Rebekah Cranes, "
            "Provenance: Journal of Forensic Semiotics), the companion of Secondary Source (#1741), whose §6.5 reads Holtzmann, Wernle and Weiss by reference.")
NORM = ("The Internet Archive's own text layer (_djvu.txt) as served, under original/<identifier>/, copied to text/<slug>.ocr.txt with line endings "
        "normalized. The PDF of each item is held by reference at its Archive URL and not copied. No text was corrected by hand; the loci keep the OCR's readings.")
SEATS = [
 ("weisse-evangelische-geschichte-1838", "01", "C. H. Weisse, Die evangelische Geschichte kritisch und philosophisch bearbeitet, 2 vols. (Leipzig, 1838)", "deu",
  "Public domain everywhere: published 1838; Weisse died 1866.",
  [("weisse-1838-i", "C. H. Weisse, Die evangelische Geschichte, vol. I (Leipzig, 1838)", "dieevangelischeg0000weis"),
   ("weisse-1838-ii", "C. H. Weisse, Die evangelische Geschichte, vol. II (Leipzig, 1838)", "dieevangelischeg0002weis")],
  "Both volumes whole.", "The two-source hypothesis stated: Mark first, and a collection of sayings read out of Papias's λόγια as the second source of Matthew and Luke."),
 ("holtzmann-synoptische-evangelien-1863", "02", "H. J. Holtzmann, Die synoptischen Evangelien: ihr Ursprung und geschichtlicher Charakter (Leipzig, 1863)", "deu",
  "Public domain everywhere: published 1863; Holtzmann died 1910.",
  [("holtzmann-1863", "H. J. Holtzmann, Die synoptischen Evangelien (Leipzig, 1863)", "diesynoptischen00holtgoog")],
  "The volume whole.", "The sources lettered: 'Quelle A (Urmarcus)' and Λ, the sayings source (the OCR reads the Λ as A or ^), given as documents; the life of Jesus drawn from them (#1741 §6.5, L54)."),
 ("wernle-synoptische-frage-1899", "03", "P. Wernle, Die synoptische Frage (Freiburg i. B., Leipzig and Tübingen, 1899)", "deu",
  "Public domain everywhere: published 1899; Wernle died 1939.",
  [("wernle-1899", "P. Wernle, Die synoptische Frage (Freiburg i. B., 1899)", "diesynoptischefr00wern")],
  "The volume whole.", "The source named Q: 'Die — hypothetische — Quelle sei mit Q bezeichnet' (#1741 §6.5, L55)."),
 ("weiss-alteste-evangelium-1903", "04", "J. Weiss, Das älteste Evangelium: ein Beitrag zum Verständnis des Markus-Evangeliums und der ältesten evangelischen Überlieferung (Göttingen, 1903)", "deu",
  "Public domain everywhere: published 1903; Johannes Weiss died 1914.",
  [("weiss-1903", "J. Weiss, Das älteste Evangelium (Göttingen, 1903)", "dasaltesteevange0000joha")],
  "The volume whole.", "Mark declared 'das älteste Evangelium', and 'nicht mehr Quelle, sondern schon Sammelbecken' (#1741 §6.5, L56)."),
 ("wellhausen-einleitung-1905", "05", "J. Wellhausen, Einleitung in die drei ersten Evangelien (Berlin, 1905)", "deu",
  "Public domain everywhere: published 1905; Wellhausen died 1918.",
  [("wellhausen-1905", "J. Wellhausen, Einleitung in die drei ersten Evangelien (Berlin, 1905)", "einleitungindied00well")],
  "The volume whole.", "Q weighed against Mark by a philologist of the Hebrew Bible: the sayings source as a document with a date and a dependence."),
 ("harnack-spruche-und-reden-1907", "06", "A. Harnack, Sprüche und Reden Jesu: die zweite Quelle des Matthäus und Lukas, Beiträge zur Einleitung in das Neue Testament II (Leipzig, 1907)", "deu",
  "Public domain everywhere: published 1907; Harnack died 1930.",
  [("harnack-1907", "A. Harnack, Sprüche und Reden Jesu (Leipzig, 1907)", "sprucheundredenj0000adol")],
  "The volume whole.", "The hypothetical source given a printed text: Harnack's reconstruction of Q's wording, the first full text of the document no one has."),
 ("streeter-four-gospels-1925", "07", "B. H. Streeter, The Four Gospels: A Study of Origins (London, 1924; the impression of 1925)", "eng",
  "Public domain in the United States (published 1924/1925, before 1929) and in the United Kingdom and the EU (Streeter died 1937).",
  [("streeter-1925", "B. H. Streeter, The Four Gospels: A Study of Origins (London, 1925 impression)", "fourgospels0000stre")],
  "The volume whole.", "The four-document hypothesis: Mark, Q, M and L, the hypothetical source fixed among three others."),
]
for corpus, n, title, lang, lic, items, scope, why in SEATS:
    spec = {"corpus": corpus, "seat": f"EA-CORPORA-35/{n}", "title": title, "language": lang, "fetched": "2026-11-06", "spine": "EA-CORPORA-35",
            "ruling": RULING, "seating": SEATING, "license": {"payload": lic, "record": "CC-BY-4.0 applies to this seat record only."},
            "normalization": NORM,
            "items": [{"kind": "ia", "slug": s, "work": w, "identifier": i, "files": [f"{i}_djvu.txt"], "class": "the making of Q, 1838–1925"} for s, w, i in items],
            "loci": [], "scope": scope, "why_seated": why, "research": RESEARCH}
    (H / f"spec35-{corpus}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", corpus)
