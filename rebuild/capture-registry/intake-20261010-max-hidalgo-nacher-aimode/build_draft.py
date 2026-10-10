#!/usr/bin/env python3
"""Author the capture 'Max Hidalgo Nácher', Google AI Mode, logged out, incognito, 2026-10-10.
Source: the operator's message of 2026-10-10 08:49 EDT ("incognito, logged out, ai mode - no aio popup or knowledge panel"),
the composition pasted in the same message. NEW address. The person is the translator the archive missed in AXN:F154."""
import json, re, pathlib
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
raw = (HERE / "paste-20261010-0849.txt").read_text(encoding="utf-8")
Q = "Max Hidalgo Nácher"
assert raw.startswith("[Max Hidalgo Nácher](https://www.google.com/search?kgmid=%2Fg%2F11f4qhpj96&q=Max+Hidalgo+N%C3%A1cher)")
assert not re.search(r"pessoa|reis", raw, re.I)
for s in ["is an Associate Professor of Literary Theory and Comparative Literature at the",
          "the history and circulation of literary theory, the poetics of modernity, and the writings of the Republican exile from the Spanish Civil War.",
          "Yale University (where he was a CLAIS Fellow in 2022)",
          "Teoría en tránsito (2022)",
          "He is an expert on the Brazilian concrete poet Haroldo de Campos",
          "He has translated various poetic works into Spanish, including books by Pol Guasch, Anna Dodas, and Diana Junkes."]:
    assert s in raw, s
cut = raw.index("\nYale University\nOur New CLAIS Fellow")
body, cards_txt = raw[:cut].strip(), raw[cut:].strip()
CARDS = [("Yale University", "Our New CLAIS Fellow Max Hidalgo & His Love for Haroldo do ..."),
         ("Google Scholar", "‪Max Hidalgo Nácher‬ - ‪Google Scholar‬"),
         ("GREC::UB", "Jose Max Hidalgo Nacher - GREC::UB"),
         ("Libros del Innombrable", "Max Hidalgo Nácher"),
         ("UB - Universitat de Barcelona", "Jose Max Hidalgo Nacher"),
         ("reditelit.org", "Max Hidalgo Nácher")]
L = cards_txt.split("\n"); cl = []
for n, (site, title) in enumerate(CARDS, 1):
    i = [k for k in range(len(L) - 1) if L[k] == site and L[k + 1] == title]
    assert i, (site, title); i = i[0]
    cl.append({"n": n, "site": site, "title": title.replace("‪", "").replace("‬", ""), "snip": L[i + 2], "rel": "third_party", "url": None, "note": "card"})
inline = len(re.findall(r"\[\d\]\(https://", body))  # numbered citation links; the name and entity links are not counted
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
T = lambda n: re.sub(r"\s+", " ", (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8"))
assert "translator-of" in T(668) and "Haroldo de Campos" in T(668)
tx = ("[Google AI Mode, logged out, incognito, 2026-10-10; no AI Overview pop-up and no knowledge panel on the page (operator). "
      "The composition as pasted, its links kept: the name links to a Google search carrying kgmid /g/11f4qhpj96, a Knowledge Graph "
      "entity id; inline citations are opaque google.com/goto tokens and one Google Scholar URL. Six source cards follow the body.]\n\n" + body)
SEAT = "Seated 2026-10-10 from the operator's message of 08:49 EDT, on the attestation in the same message (\"incognito, logged out, ai mode\")."
d = {"q": Q, "date": "2026-10-10", "surface": "Google AI Mode",
 "surface_basis": "'ai mode' — operator, 2026-10-10 08:49 EDT; 'no aio popup or knowledge panel'.",
 "auth": "logged out, incognito", "auth_basis": "'incognito, logged out' — operator, 2026-10-10 08:49 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "max-hidalgo-nacher-aimode-20261010",
 "q_kind": "a living scholar and translator, by name alone, the morning the archive found it did not know him (AXN:F154). NEW address.",
 "originator": {"name": "Max Hidalgo Nácher", "relation": "external", "entity_type": "person", "spxi_treatment": "none",
                "basis": "Not the archive's: a public scholar (Universitat de Barcelona), translator of the Obras completas de Ricardo Reis (Pre-Textos, 2025). Entered in the archive by the erratum on AXN:F154. Recorded 2026-10-10."},
 "related_deposits": [668, 669],
 "mt": "THE TRANSLATOR COMPOSED WITHOUT THE TRANSLATION: NO PESSOA, NO REIS",
 "d": ("THE TRANSLATOR COMPOSED WITHOUT THE TRANSLATION: NO PESSOA, NO REIS: asked for Max Hidalgo Nácher, AI Mode composes him at "
       "the grain of a faculty page — the UB post, the degrees (Journalism 2004, Literary Theory 2006), the Master 2 under Kristeva, the 2013 "
       "thesis under Nora Catelli, Harvard 2016, Yale CLAIS 2022, Puentes, Teoría en tránsito (2022), Haroldo de Campos, translations of Pol "
       "Guasch, Anna Dodas and Diana Junkes. Neither Pessoa nor Ricardo Reis appears anywhere on the page: the Obras completas de Ricardo "
       "Reis (Pre-Textos, 2025), which he translated and for which he wrote the epilogue, and his 'Arqueologías de la traducción de Ricardo "
       "Reis' (Pessoa Plural, 2026) are absent. The name carries a Knowledge Graph id (kgmid /g/11f4qhpj96) and the page shows no knowledge "
       "panel. The field composes the receiver and omits the transmission the archive had omitted the receiver of."),
 "cites": inline + len(cl), "cite_list": cl, "archive_controlled_cites": 0,
 "sf": "Six cards: " + "; ".join(f"{c['site']} — {c['title']}" for c in cl) + f". Inline: {inline} numbered citations (goto tokens, one Google Scholar URL); entity links to Universitat de Barcelona and Harvard University.",
 "per": 0.75, "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the person, the institution (UB), the sources (six cards). Lost: identifiers (no ORCID or ISBN), and the Reis translation and its article entirely.",
 "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition with links and cards as pasted",
 "transcript_complete": "complete as pasted: body with inline links, six cards", "transcript_read": "READ IN FULL 2026-10-10",
 "reading": ("Checked against the publisher and the translator's own listing. Pre-Textos credits 'Traducción y epílogo: Max Hidalgo Nácher' "
             "for the Obras completas de Ricardo Reis (2025, ed. Pizarro and Uribe); his Academia page lists it, with 'Arqueologías de la "
             "traducción de Ricardo Reis' (Pessoa Plural, 2026) and translations of Hilda Hilst, Pol Guasch and Diana Junkes. The composition "
             "carries every item of the faculty record and none of the Reis work. The archive's Pessoa graph (#668) holds the translator-of "
             "relation and Haroldo de Campos; it lacked Nácher until the erratum on AXN:F154."),
 "analysis": ("The same instance-level erasure the archive committed in AXN:F154 appears in the field's composition, from the other side: "
              "the archive held the source and lacked the receiver; AI Mode holds the receiver and lacks the transmission. The Reis edition is "
              "the work through which he enters Pessoa studies; the composition's account of "
              "his translations names three poets and stops. Operator's reading, given with the capture: 'i do think there is probably a "
              "general suspicion towards heteronymy in aio's ontology.' The capture records the absence and does not measure that reading. " + SEAT),
 "findings": ["FACULTY GRAIN. Degrees, supervisors, posts, fellowships, journal, monograph and three translated poets, each cited.",
              "NO PESSOA, NO REIS. The Obras completas de Ricardo Reis (2025) and 'Arqueologías de la traducción de Ricardo Reis' (2026) are absent from the page.",
              "THE TRANSMISSION OMITTED FROM THE OTHER SIDE. The archive lacked the receiver of a source it held; the field holds the receiver and lacks the source he transmits.",
              "AN ENTITY WITHOUT A PANEL. The name links to kgmid /g/11f4qhpj96; no knowledge panel or AI Overview on the page.",
              "HAROLDO KEPT. His Haroldo de Campos research is carried, the node #668 already holds."],
 "longitudinal_priors": [],
 "rerun": "https://www.google.com/search?q=Max+Hidalgo+N%C3%A1cher&udm=50",
 "notes": {"date_basis": "The operator's message of 2026-10-10, 08:49 EDT.",
           "operator_reading": "i do think there is probably a general suspicion towards heteronymy in aio's ontology. i dont think so - i could go thru and measure it. but there is no need.",
           "kgmid": "/g/11f4qhpj96",
           "verified": "Compared 2026-10-10 against pre-textos.com, ub.academia.edu/MaxHidalgoNácher, and the text of #668."}}
(HERE / "capture-01-max-hidalgo-nacher-aimode.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), len(cl), inline)
