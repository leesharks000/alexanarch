#!/usr/bin/env python3
"""Writes spec29-avant-garde-ii.json (EA-CORPORA-29/05)."""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
items, loci = [], []


def add(cls, kind, slug, work, find, **kw):
    items.append({"kind": kind, "slug": slug, "work": work, "class": cls} | kw)
    loci.append({"label": work.split(" — ")[0], "text": f"text/{slug}.ocr.txt" if kind in ("ia", "ia_ref") else f"text/{slug}.txt", "find": find})


add("Imagism", "ia", "flint-imagisme-1913", "F. S. Flint, “Imagisme”, Poetry: A Magazine of Verse 1.6 (March 1913), 198–200 — JSTOR Early Journal Content via the Internet Archive, scan and OCR layer", "Direct treatment of the", identifier="jstor-20569729", files=["20569729.pdf", "20569729_djvu.txt"])
add("Imagism", "ia", "pound-few-donts-1913", "Ezra Pound, “A Few Don'ts by an Imagiste”, Poetry 1.6 (March 1913), 200–206 — JSTOR Early Journal Content via the Internet Archive, scan and OCR layer", "emotional complex", identifier="jstor-20569730", files=["20569730.pdf", "20569730_djvu.txt"])
add("American modernism", "ia", "williams-kora-in-hell-1920", "William Carlos Williams, Kora in Hell: Improvisations (Boston: Four Seas, 1920), with the Prologue — scan and OCR layer", "Kora", identifier="korainhellimprov00willrich", files=["korainhellimprov00willrich_bw.pdf", "korainhellimprov00willrich_djvu.txt"])
add("Dada", "ia", "huelsenbeck-en-avant-dada-1920", "Richard Huelsenbeck, En avant Dada: Eine Geschichte des Dadaismus (Hannover: Paul Steegemann, 1920; Die Silbergäule 50/51) — scan and OCR layer", "Dada", identifier="enavantdadaeine00huelgoog", files=["enavantdadaeine00huelgoog.pdf", "enavantdadaeine00huelgoog_djvu.txt"])
add("Surrealism", "ia_ref", "revolution-surrealiste-1-1924", "La Révolution surréaliste, no. 1 (Paris, 1 December 1924), with Boiffard, Éluard and Vitrac's preface and the dream and automatic texts — OCR layer", "surréalis", identifier="la-revolution-surrealisten.-1-1-dicembre-1924", scan="La Revolution Surrealiste,n.1, 1 dicembre 1924.pdf", ocr="La Revolution Surrealiste,n.1, 1 dicembre 1924_djvu.txt")
add("Surrealism", "ia_ref", "revolution-surrealiste-12-1929", "La Révolution surréaliste, no. 12 (Paris, 15 December 1929), with André Breton's Second manifeste du surréalisme — OCR layer", "MANIFESTE", identifier="la-revolution-surrealistea.-vn.-12-15-dicembre-1929", scan="La Revolution Surrealiste,a.V,n.12, 15 dicembre 1929.pdf", ocr="La Revolution Surrealiste,a.V,n.12, 15 dicembre 1929_djvu.txt")
add("Russian avant-garde", "ws", "arvatov-rechetvorchestvo-1923", "Борис Арватов, «Речетворчество (По поводу „заумной“ поэзии)», ЛЕФ 1923, № 2 (Boris Arvatov, Speech-Creation: On 'Transrational' Poetry) — Russian Wikisource", "заумной", lang="ru", title="Речетворчество (Арватов)")
add("Chinese New Literature", "ws", "hu-shi-wenxue-gailiang-1917", "胡適〈文學改良芻議〉 (Hu Shi, Some Modest Proposals for the Reform of Literature), 新青年 2.5 (1 January 1917) — Chinese Wikisource", "須言之有物", lang="zh", title="文學改良芻議")
add("Chinese New Literature", "ws", "chen-duxiu-wenxue-geming-1917", "陳獨秀〈文學革命論〉 (Chen Duxiu, On Literary Revolution), 新青年 2.6 (1 February 1917) — Chinese Wikisource", "文學革命", lang="zh", title="文學革命論")
add("Chinese New Literature", "ws", "hu-shi-tan-xinshi-1919", "胡適〈談新詩（八年來一件大事）〉 (Hu Shi, On New Poetry), 星期評論 (10 October 1919) — Chinese Wikisource", "新诗", lang="zh", title="談新詩（八年來一件大事）")
add("Brazilian modernism", "ws", "prado-poesia-pau-brasil-1925", "Paulo Prado, “Poesia Pau Brasil”, preface to Oswald de Andrade, Pau Brasil (Paris: Au Sans Pareil, 1925) — Portuguese Wikisource", "ovo de Colombo", lang="pt", title="Pau Brasil/Poesia Pau Brasil")

spec = {
 "corpus": "avant-garde-ii",
 "seat": "EA-CORPORA-29/05",
 "title": "The Avant-Garde, II: Imagism, Kora in Hell, En avant Dada, La Révolution surréaliste, LEF, the Chinese New Literature and Pau Brasil",
 "language": "mul",
 "fetched": "2026-10-28",
 "license": {
  "payload": "Per item, recorded in origin.items. All items were first published 1913–1929 and are in the public domain in the United States (published before 1930, or before 1931 for the 1929–1930 items, their term of 95 years run). JSTOR Early Journal Content is free of known restrictions; Wikisource pages CC BY-SA 4.0 for the site's contributions. Two French items are surrealist periodicals whose authors' terms still run in France: seated under United States public domain, the archive's jurisdiction.",
  "record": "CC-BY-4.0 applies to this seat record only."
 },
 "normalization": "Originals as fetched under original/ (Internet Archive scans and OCR layers; Wikisource HTML as served, with its revision id). text/<slug>.ocr.txt is the Archive's OCR with line endings normalized; text/<slug>.txt the Wikisource parser output reduced by code. The two Révolution surréaliste scans are held by reference (identifier, file, size and md5), their OCR layers copied. No text corrected by hand.",
 "units": "one text file per work; each work carries its movement as class",
 "items": items,
 "loci": loci,
 "classes": ["Imagism", "American modernism", "Dada", "Surrealism", "Russian avant-garde", "Chinese New Literature", "Brazilian modernism"],
 "cross_references": {"already_on_the_shelf": "The first avant-garde shelf: futurism (the Italian and Russian manifestos, Blast), dada (Dada 1–8, Tzara, Picabia, Serner, Ball's Flametti, Der Dada), visual-poetry (Mallarmé's Coup de dés, Apollinaire's Calligrammes), nonsense-and-constraint (Lautréamont, Roussel, Morgenstern), jarry, artaud, stein, pound, pound-ii (Des Imagistes, Instigations), russian-formalism, pessoa. Mayakovsky's How Are Verses Made?, Huidobro's Arte poética, Apollinaire's L'Esprit nouveau and Hagiwara's Principles of Poetry are in ars-poetica (29/04)."},
 "queued": [
  "André Breton, Manifeste du surréalisme (Paris: Kra, 1924): no scan of the 1924 edition found; its sequel is seated in La Révolution surréaliste 12",
  "Mário de Andrade, “Prefácio interessantíssimo”, Paulicéa desvairada (São Paulo: Casa Mayença, 1922): Wikisource holds only the index; the Commons scan answered 429 this session",
  "Oswald de Andrade, “Manifesto da Poesia Pau-Brasil” (Correio da Manhã, 18 March 1924) and “Manifesto Antropófago” (Revista de Antropofagia 1, 1928): not found",
  "Mina Loy, “Aphorisms on Futurism”, Camera Work 45 (January 1914): no scan found",
  "Hugo Ball, Die Flucht aus der Zeit (München: Duncker & Humblot, 1927): no scan found",
  "Tristan Tzara, Sept manifestes Dada (Paris: Budry, 1924): only the 1963 edition found, in copyright",
  "Gertrude Stein, Composition as Explanation (London: Hogarth, 1926): no scan found",
  "Ultraísmo: Guillermo de Torre's “Manifiesto vertical” (1920) and Borges's “Ultraísmo” (Nosotros, 1921): not found"
 ],
 "scope": "A second avant-garde shelf, beside the first, gathered with the arts of poetry: the movements' own statements of method from 1913 to 1929, where a public-domain scan or transcription could be fetched and its date verified at the file.",
 "why_seated": "At the author's direction to go 'deeper into the experimentalist dada surrealist etc' within the pluriform ars poetica bundle.",
 "spine": "29/05",
 "ruling": "The author's directions of 2026-10-28.",
 "seating": "EA-CORPORA-29 (gathered; the deposit that assigns its AXN is pending)"
}
(HERE / "spec29-avant-garde-ii.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(items), "items")
