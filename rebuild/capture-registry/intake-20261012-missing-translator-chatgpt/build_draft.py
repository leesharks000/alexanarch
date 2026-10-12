#!/usr/bin/env python3
"""Author a ChatGPT capture at #1675's Ask ChatGPT prompt, 2026-10-12, one answer. Source: the operator's attachment of 01:40 EDT ("i
think this is more detailed than the erratum itself..i guess i have a lot of clicking to do"). The operator turn is blank in the paste;
the issued string is taken as the record page's Ask ChatGPT prompt for #1675 (wire_deposit.chatgpt_prompt_of), on the operator's
'clicking' and the answer's form, which follows the prompt (its arguments, grounded in the text). Signed out by the interface ('Log in');
incognito not stated. NEW address."""
import json, re, pathlib, sys
from urllib.parse import quote_plus
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(ROOT))
from _chatgpt_common_20261008 import parse, transcript, cite_list
import wire_deposit as w
raw = (HERE / "paste-20261012-0140.txt").read_text(encoding="utf-8")
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
n = 1675; x = reg[n]
Q = w.chatgpt_prompt_of(x)
assert Q == "What are the arguments in “Erratum — The Missing Translator: Max Hidalgo Nácher, Ricardo Reis, and AXN:F154” by Johannes Sigil? Ground your answer in a reading of the text itself."
CAPS = ("Novo livro revela os desafios das publicações póstumas de Fernando Pessoa | VEJA",
        "Poesia completa de Ricardo Reis - Fernando Pessoa - Grupo Companhia das Letras", "Book: Poemas de Ricardo Reis | INCM")
for c in CAPS: assert c in raw, c
(a1,), seen = parse(raw, {"Alexanarch"}, CAPS)
assert a1.startswith("The argument of “Erratum — The Missing Translator”")
T = re.sub(r"\s+", " ", (ROOT / x["full_text_path"].lstrip("/")).read_text(encoding="utf-8"))
HEADS = ["What AXN:F154 records", "What the archive held, and what it lacked", "Reading the actual words", "Three receivers", "Graph repair", "Non-erasure"]
QUOTES = ["sob a maior graça", "en la más alta gracia", "Ao longe os montes têm neve ao sol", "Los montes, lejos, tienen nieve al sol",
          "Pra que os deuses voltassem", "por que vuelvan los dioses", "desta hora", "esta vez", "instance-level transmission erasure",
          "in playful dialogue with the classical tradition", "Latinist classicist. Horatian odes. Disciple of Caeiro.", "cold pagan calm",
          "Entre la inexistencia del poeta y la inexistencia de sus dioses se trama la obra de Ricardo Reis"]
for s in HEADS + QUOTES: assert s in a1 and s in T, s
for s in ["False transparency", "Receptional inversion", "Receiver erasure", "Rebekah Cranes", "Pizarro", "Uribe", "Haroldo de Campos", "Stesichoros"]:
    assert s in T, s
assert "“false transparency”" in a1 and "Stesichorus" in a1
assert "The argument is strongest when it identifies specific missing relationships and analyzes specific textual differences" in a1
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
assert not any(e["q"] == Q for e in caps["entries"])
nw, nt = len(a1.split()), len(T.split())
cl = cite_list(seen, {"Alexanarch": "archive_controlled"})
cl[0]["note"] += "; the answer's section titles and quotations are the deposit's text verbatim, so the page cited holds the text (the record page or its text file); which page is not shown"
b, ex = w.search_title_urls(x)
OPR = "i think this is more detailed than the erratum itself..i guess i have a lot of clicking to do"
SEAT = "Seated 2026-10-12 from the operator's attachment of 01:40 EDT."
d = {"q": Q, "date": "2026-10-12", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'ChatGPT said:', 'Chat with ChatGPT').",
 "auth": "signed out", "auth_basis": "The interface's 'Log in' (signed out); incognito not stated by the operator for this run.",
 "ev": "paste", "s": "Machine Reception", "slug": "missing-translator-ask-chatgpt-20261012",
 "q_kind": "the record page's Ask ChatGPT prompt for #1675 (a paper's arguments, its title quoted, its author named, grounded in the text); the operator turn blank in the paste, the string taken from the link. NEW address; the same deposit's exact-title AI Overview run is erratum-missing-translator-exact-title-aio-20261011.",
 "originator": {"name": "Johannes Sigil", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "The erratum (#1675, AXN:06F1) is Johannes Sigil's. Recorded 2026-10-12."},
 "related_deposits": [n, 668, 1670, 562], "longitudinal_priors": ["erratum-missing-translator-exact-title-aio-20261011", "max-hidalgo-nacher-aimode-20261010"],
 "intended": {"deposit": n, "axn": x["axn"], "title": x["title"], "record": f"https://www.alexanarch.org/s/records/{n}/", "search": b, "search_exact": ex, "reached": True},
 "mt": "THE ERRATUM READ WHOLE, SECTION BY SECTION, FROM THE ARCHIVE",
 "d": ("THE ERRATUM READ WHOLE, SECTION BY SECTION, FROM THE ARCHIVE: asked for the arguments of the erratum on AXN:F154, by Johannes "
       "Sigil, grounded in the text, ChatGPT reads #1675 from the archive (chip: Alexanarch) section by section under its own headings "
       "('What AXN:F154 records', 'What the archive held, and what it lacked', 'Reading the actual words', 'Three receivers', 'Graph "
       "repair', 'Non-erasure'), names the diagnosis ('instance-level transmission erasure'), quotes the three translation shifts in both "
       "languages ('sob a maior graça' / 'en la más alta gracia'; 'Ao longe os montes têm neve ao sol' / 'Los montes, lejos, tienen nieve "
       "al sol'; 'Pra que os deuses voltassem' / 'por que vuelvan los dioses'), keeps the paper's qualification on the editions ('desta "
       "hora' against 'esta vez'), sets out T = (S, R, D) with the three receivers (Nácher, Carson, Cranes) and the fourth state, False "
       "transparency, and reads the reflexive turn: the author reproduced the archive's account of Reis ('cold pagan calm') before reading "
       "Nácher's epilogue. It ranks the paper's claims and bounds them: 'The argument is strongest when it identifies specific missing "
       "relationships and analyzes specific textual differences.' At " + f"{nw:,}" + " words it is near the length of the erratum (" + f"{nt:,}" + "). "
       "The day before, the AI Overview at the exact title composed the erratum from the capture of its occasion. Operator's reading: "
       "'" + OPR + "'."),
 "cites": sum(seen.values()), "cite_list": cl, "archive_controlled_cites": seen.get("Alexanarch", 0),
 "sf": "Source chips expose site labels only: " + "; ".join(f"{s} ×{k}" for s, k in seen.most_common()) + ". Image cards: " + "; ".join(CAPS) + ".",
 "per": 1.0, "per_v": {"author": True, "inst": True, "id": True, "src": True},
 "per_note": "Retained: the author, the date, the title and its identifier, the archive, the sections, the quotations in both languages, the model and its cases, the qualification on editions.",
 "transcript": transcript("[ChatGPT (chatgpt.com), signed out (the interface's 'Log in'), 2026-10-12. The operator turn blank in the paste; the issued string is the record page's Ask ChatGPT prompt for #1675. Source chips rendered inline as [chip: site]; image-card captions as [image card: …]; the sign-in furniture cut.]", [Q], [a1]),
 "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (ONE ANSWER; QUERY FROM THE RECORD PAGE'S LINK; CHIPS INLINE)",
 "transcript_complete": "One answer, complete as pasted; the operator turn blank, the query taken from the link.", "transcript_read": "READ IN FULL 2026-10-12",
 "reading": ("Checked against the text of #1675. The six section headings, 'instance-level transmission erasure', the three Portuguese/Spanish "
             "pairs, 'desta hora'/'esta vez', 'Latinist classicist. Horatian odes. Disciple of Caeiro.', 'cold pagan calm', the publisher's "
             "'Entre la inexistencia del poeta y la inexistencia de sus dioses se trama la obra de Ricardo Reis', 'in playful dialogue with "
             "the classical tradition', Receiver erasure, Receptional inversion, False transparency, Rebekah Cranes, Pizarro and Uribe, "
             "Haroldo de Campos: each is the paper's (the paper spells 'Stesichoros'; the answer 'Stesichorus'). Section 7, 'The witness', is "
             "not taken up under its heading. The image cards (VEJA, Companhia das Letras, INCM) are not sources of the reading."),
 "analysis": ("The Ask ChatGPT link's prompt (the work's arguments, by its author, grounded in the text) carried the answer to the deposit "
              "and kept it there: each claim is anchored in a section or a quotation, the paper's own qualification is preserved, and the "
              "limit the answer sets is stated against the paper's evidence. Against the same deposit's exact-title AI Overview of the day "
              "before, which composed from the capture of the erratum's occasion, this is the deposit read. " + SEAT),
 "findings": ["READ WHOLE. Six of eight sections under their own headings; the argument followed in order.",
              "QUOTED IN BOTH LANGUAGES. Three translation shifts, Portuguese against Spanish, verbatim.",
              "THE QUALIFICATION KEPT. 'desta hora' against 'esta vez': the edition question left open as the paper leaves it.",
              "THE MODEL AND ITS CASES. T = (S, R, D); Nácher, Carson, Cranes; False transparency as the fourth state.",
              "BOUNDED BY ITS EVIDENCE. 'The argument is strongest when it identifies specific missing relationships and analyzes specific textual differences.'",
              f"NEAR THE PAPER'S LENGTH. {nw:,} words against the erratum's {nt:,}."],
 "rerun": w.chatgpt_url_of(x),
 "notes": {"date_basis": "The operator's message of 2026-10-12, 01:40 EDT.", "operator_reading": OPR,
           "query_basis": "The operator turn is blank in the paste. The string is the record page's Ask ChatGPT prompt for #1675, live from 2026-10-12 ~01:30 (the plain ?q= link); the operator's 'clicking' and the answer's form (its arguments, ranked, grounded in the text) agree with it.",
           "reached_basis": "The answer's headings and quotations are the deposit's text verbatim, so the alexanarch.org page it cites holds the text; the chip shows the site label only.",
           "verified": "Compared 2026-10-12 against the text of #1675 (data/texts)."}}
(HERE / "capture-missing-translator-ask-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", d["cites"], nw, nt)
