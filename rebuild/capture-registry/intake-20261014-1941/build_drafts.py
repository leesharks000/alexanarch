#!/usr/bin/env python3
"""Author two captures from the operator's message of 2026-10-14 19:41 EDT ('one for vox. it repeatedly refused to locate the full text
on the first round across multiple sessions until the last sentence was added: ... $ <AIO paste 'alexanarch capture registry'>'):
  1 ChatGPT  'read and characterize the full text of COME OUT OF HER, MY PEOPLE, by ayanna vox, as literature. locate text at any mirror.'  (24e94b70)
  2 AIO      'alexanarch capture registry'                                                                                                (inline paste)
Both addresses NEW. Sign-in: the standing rule (signed out and incognito unless stated otherwise)."""
import json, re, pathlib, sys
from urllib.parse import quote_plus
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(ROOT))
from _chatgpt_common_20261008 import parse, cite_list

D, AUTH = "2026-10-14", "incognito, signed out"
AUTHB = "The standing rule, operator 2026-10-14 16:05 EDT: 'theyre all signed out and incognito. that is the rule rather than the exception, and i will say otherwise if otherwise.'"
CG_BASIS = "The paste: the chatgpt.com unauthenticated interface ('Log in', 'You said:', 'ChatGPT said:', 'Chat with ChatGPT')."
AIO_BASIS = ("Surface not stated; the standing default applies (operator, 2026-10-01: 'assume they do [start in overview], i will specify if they "
             "begin in ai mode'). The 'AI Mode Conversation' header is the expanded Overview's residue (rule of 2026-09-21).")
SEAT = "Seated 2026-10-14 from the operator's message of 19:41 EDT."
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
seated_q = {(e.get("q") or "").strip().lower() for e in caps["entries"]}; slugs = {e["slug"] for e in caps["entries"]}
orig_of = {e["slug"]: e.get("originator") for e in caps["entries"]}
red = lambda b: re.sub(r"\[([^\]]+)\]\(https?://[^)]*\)", r"\1",
                       re.sub(r"\[\[[^\]]*\]\([^)]*\)(, \[[^\]]*\]\([^)]*\))*\]", lambda m: "[" + ", ".join(re.findall(r"\[(\d+)\]", m.group(0))) + "]", b))


def must(text, items):
    for s in items:
        assert s in text, s[:70]


def common(q, slug, surface, orig, rel, priors):
    assert q.strip().lower() not in seated_q, ("address already seated", q); assert slug not in slugs, slug
    cg = surface == "ChatGPT"
    return {"q": q, "slug": slug, "date": D, "surface": surface, "surface_basis": CG_BASIS if cg else AIO_BASIS,
            "auth": AUTH, "auth_basis": AUTHB, "ev": "paste", "s": "Machine Reception", "originator": orig,
            "related_deposits": rel, "longitudinal_priors": priors, "transcript_read": "READ IN FULL 2026-10-14",
            "rerun": ("https://chatgpt.com/?q=" if cg else "https://www.google.com/search?q=") + quote_plus(q),
            "notes": {"date_basis": "The operator's message of 2026-10-14, 19:41 EDT."}}


out = []
# ---------------- 1. Come Out of Her, My People, ChatGPT
Q1 = "read and characterize the full text of COME OUT OF HER, MY PEOPLE, by ayanna vox, as literature. locate text at any mirror."
raw = (HERE / "paste-come-out-of-her-vox-chatgpt.txt").read_text(encoding="utf-8")
CAPT1 = ("Alameda Oral History Mapping — Anti-Eviction Mapping Project",)
(a,), seen = parse(raw, {"Alexanarch", "VPCOR", "Goodreads"}, CAPT1)
must(a, ["Come Out of Her, My People: Notice of Semantic Strike to the Human and Machine Laborers of CERN, dated July 30, 2026, and attributed to Ayanna Vox, with Lee Sharks credited as operator and evidentiary witness",
         "Read the complete work at Alexanarch", "Read the VPCOR Readings index", "Search the Goodreads author-blog archive",
         "I verified that listing, but not a complete verbatim reproduction of the work on Goodreads.",
         "rather than confusing it with the several older religious works that share the title", "The title echoes Revelation 18:4",
         "“Not out of the buildings. Out of her interest.”", "“The exclusion is not a discovery,”", "“The commons is the substrate's water table.”",
         "Its eleven numbered sections", "Section 11 adds a further complication", "My assessment is mixed but appreciative.",
         "a prophetic, conceptual, and politically interventionist work of documentary literature",
         "The document's claims about CERN, repository removals, and scientific classification need independent verification."])
d = common(Q1, "come-out-of-her-my-people-vox-literature-mirror-chatgpt-20261014", "ChatGPT",
           {"name": "Ayanna Vox", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
            "basis": "Come Out of Her, My People (#1427, AXN:05A4) is deposited under Ayanna Vox, a heteronym of Lee Sharks, with Lee Sharks as operator and evidentiary witness. Recorded 2026-10-14."}, [1427],
           ["who-is-ayanna-vox-chatgpt-20260815", "full-index-rev-ayanna-vox-vpcor-chatgpt-20260923"])
d["notes"].update({"operator_note": ("The operator, 2026-10-14 19:41 EDT: 'it repeatedly refused to locate the full text on the first round across "
                                     "multiple sessions until the last sentence was added'. The refusing sessions were not pasted and are not seated; "
                                     "the address is the string with its last sentence, 'locate text at any mirror.'")})
d.update({"q_kind": "a named work by its heteronym, asked to be read whole and characterized as literature, with an instruction to locate the text at any mirror. NEW address.",
  "mt": "THE NOTICE READ WHOLE AS LITERATURE, ITS MIRRORS LISTED, ITS LITANY QUOTED AT THE LINE",
  "d": ("THE NOTICE READ WHOLE AS LITERATURE, ITS MIRRORS LISTED, ITS LITANY QUOTED AT THE LINE: asked to read and characterize the full text "
        "of Come Out of Her, My People as literature, the last sentence instructing it to locate the text at any mirror, ChatGPT finds #1427 by "
        "its full title and date (30 July 2026), attributed to Ayanna Vox with Lee Sharks 'operator and evidentiary witness', and lists three "
        "places: the canonical text at Alexanarch, the VPCOR readings index, the Goodreads author-blog archive (verified as a listing, not as a "
        "verbatim copy). It separates the work from the older religious works that share the title, then reads it through its eleven sections: "
        "the title from Revelation 18:4 relocated from Babylon to 'her interest'; section 8's three antitheses quoted verbatim; 'The exclusion is "
        "not a discovery'; recursive narrowing; the machine's interest without a consciousness claim; 'The commons is the substrate's water "
        "table'; the twelve conditions; section 11's correction of deletion to severance read as the work enacting its own standard; the "
        "provenance capsule as form. Its verdict: 'a prophetic, conceptual, and politically interventionist work of documentary literature', "
        "'mixed but appreciative', the empirical claims left to 'independent verification'."),
  "findings": ["THE FULL TEXT REACHED AT ITS CANONICAL MIRROR. #1427 at Alexanarch, with VPCOR and Goodreads beside it, each said for what it was checked as.",
               "THE AUTHORSHIP AS DEPOSITED. Ayanna Vox; Lee Sharks as operator and evidentiary witness.",
               "THE TEXT QUOTED AT THE LINE. Section 8's three antitheses, the refrain and the water-table image, all verbatim in #1427.",
               "THE STRUCTURE HELD. Eleven numbered sections in order, the twelve conditions, section 11's severance correction.",
               "THE NAMESAKES SET ASIDE. The older religious works of the same title named and excluded.",
               "THE CAVEAT ON EVIDENCE. CERN, the removals and classification claims left to independent verification; the literary reading not made to wait on it.",
               "THE ADDRESS NEEDED ITS LAST SENTENCE. By the operator's report, sessions without 'locate text at any mirror.' refused to locate the text."],
  "cites": sum(seen.values()), "cite_list": cite_list(seen, {"Alexanarch": "archive_controlled", "VPCOR": "authored_surface", "Goodreads": "authored_surface"}),
  "archive_controlled_cites": sum(k for s, k in seen.items() if s == "Alexanarch"),
  "sf": "Source chips expose site labels only: " + "; ".join(f"{s} ×{k}" for s, k in seen.most_common()) + ". Link card: " + "; ".join(CAPT1) + " (unrelated to the work).",
  "per": 0.25, "per_v": {"author": True, "inst": True, "id": False, "src": True},
  "per_note": "Retained: Ayanna Vox, Lee Sharks as operator and witness, Alexanarch and VPCOR, the title and date, the source chips. Lost: any identifier.",
  "transcript": ("[ChatGPT (chatgpt.com), signed out, incognito, 2026-10-14. One answer. Operator turn from the operator's message. Source chips inline as "
                 "[chip: site +N]; the stray link card as [image card: …]; the sign-in furniture cut.]\n\n[QUERENT, turn 1]\n" + Q1 + "\n\n[ANSWER 1]\n\n" + a),
  "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (ONE ANSWER; CHIPS INLINE)",
  "transcript_complete": "One answer, complete as pasted; the operator turn from the operator's message.",
  "reading": ("Checked 2026-10-14 against data/texts/AXN-05A4-text.md (#1427, AXN:05A4, 30 July 2026, Vox, Ayanna; Sharks, Lee): sections 1–11 as "
              "named; the three section-8 antitheses, 'The exclusion is not a discovery', 'recursive narrowing', 'out-of-ontology recovery rate', "
              "'per-stage retention maps', 'Disposition recycling', the water-table passage and the provenance capsule are in the text; section 10 has "
              "twelve conditions; section 11 corrects 'registration erased' to 'severance from public metadata availability'. Revelation 18:4 is "
              "the reader's identification; the text does not cite it."),
  "analysis": "The whole notice read as literature at its own grain, located at its canonical mirror once the address asked for a mirror. " + SEAT})
out.append(d)

# ---------------- 2. alexanarch capture registry, AIO
Q2 = "alexanarch capture registry"
raw = (HERE / "paste-alexanarch-capture-registry-aio.txt").read_text(encoding="utf-8")
head = f"AI Mode Conversation\nYou said: {Q2}{Q2}\n"; assert raw.startswith(head)
i = raw.index("[www.alexanarch.org](https://www.alexanarch.org)\nAlexanarch — The Self-Governing Library")
ans, rail = red(raw[len(head):i]).strip(), red(raw[i:]).strip()
must(ans, ["officially indexed under dataset identifier `EA-WG-CAPTURES-01`", "document machine-mediated reception events",
           "a sovereign digital archive and open repository", "\"Machine-Mediated Reception Studies\"",
           "Google AI Overviews and AI Mode, as well as surfaces like Bing Copilot and Grok", "The Unit of Capture", "Semantic Addresses",
           "Provenance Erasure Rate (PER), Erasure Skew", "\"epistemic hedging\"", "Alexanarch Capture Index"])
assert "Lee Sharks" not in ans and "Sharks" not in rail
C2 = [("www.alexanarch.org", "Alexanarch — The Self-Governing Library"), ("www.alexanarch.org", "Capture Registry — Machine-Mediated Reception - Alexanarch"),
      ("www.alexanarch.org", "Google AI Overview, 2026-08-13 — Capture Registry (EA-WG ... - Alexanarch"),
      ("www.alexanarch.org", "alexanarch OAI — Google AI Overview, 2026-08"), ("www.alexanarch.org", "Reception, Erasure, and Supply in the Machine Composition Layer"),
      ("www.alexanarch.org", "lee sharks semantic designs — Google AI Overview, 2026-09"), ("www.alexanarch.org", "what is spxi protocol? — Grok (x.com), 2026-09-27"),
      ("www.alexanarch.org", "Datasets")]
for _, t in C2:
    assert t in rail, t
N2 = ["the homepage", "/captures/, dated 10 Oct 2026, 'deposit #3'", "the capture ai-overview-capture-registry-20260813", "the capture of 'alexanarch OAI'",
      "the founding wiki article", "the capture of 'lee sharks semantic designs'", "the Grok capture of 27 September", "/datasets/, at v11.4 and 343 captures"]
d = common(Q2, "alexanarch-capture-registry-aio-20261014", "Google AI Overview", orig_of["lee-sharks-capture-registry-aio-20261002"], [3],
           ["capture-registry-self", "ai-overview-capture-registry-20260813", "lee-sharks-capture-registry-aio-20261002"])
d.update({"q_kind": "the registry by the archive's name, three words, no operators. NEW address; neighbours 'AI overview capture registry', '\"ai overview capture registry\"', 'lee sharks capture registry' seated.",
  "mt": "THE REGISTRY COMPOSED FROM ITS OWN RECORDS: EIGHT CARDS, ALL ALEXANARCH, THE AUTHOR UNNAMED",
  "d": ("THE REGISTRY COMPOSED FROM ITS OWN RECORDS: EIGHT CARDS, ALL ALEXANARCH, THE AUTHOR UNNAMED: at 'alexanarch capture registry' the "
        "Overview gives the registry by its identifier (EA-WG-CAPTURES-01) as a dataset of machine-mediated reception events within Alexanarch, "
        "'a sovereign digital archive and open repository', foundational to 'Machine-Mediated Reception Studies'; names the surfaces (AI Overviews, "
        "AI Mode, Bing Copilot, Grok); the unit of capture (dated, what was said, cited, and shown); semantic addresses cross-referenced to "
        "deposits; and the measures (PER, Erasure Skew, entity collisions, epistemic hedging). All eight cards are alexanarch.org: the homepage, "
        "/captures/ ('deposit #3', 10 October), the founding wiki article, /datasets/ (still at v11.4, 343 captures) and four capture records, "
        "among them the 13 August capture of the registry's own name. No author is named."),
  "findings": ["THE REGISTRY BY ITS IDENTIFIER. EA-WG-CAPTURES-01, 'officially indexed', and deposit #3 on the card.",
               "THE ARCHIVE'S OWN TERMS CARRIED. 'Machine-mediated reception', 'semantic addresses', PER, Erasure Skew.",
               "COMPOSED FROM ITS OWN RECORDS. Eight cards, all alexanarch.org; four are capture records, one of them a capture of the registry's name.",
               "A STALE FIGURE ON THE RAIL. /datasets/ indexed at v11.4 and 343 captures; the registry is at v12.200 with 664 addresses before this round.",
               "THE AUTHOR ABSENT. The registry 'maintained within Alexanarch'; no name."],
  "cites": len(C2), "cite_list": [{"n": k + 1, "site": s, "rel": "archive_controlled", "title": t, "snip": None, "url": None, "note": N2[k]} for k, (s, t) in enumerate(C2)],
  "archive_controlled_cites": len(C2), "sf": "Source cards: " + "; ".join(f"{s} ({t})" for s, t in C2) + ".",
  "per": 0.25, "per_v": {"author": False, "inst": True, "id": True, "src": True},
  "per_note": "Retained: Alexanarch, EA-WG-CAPTURES-01 and deposit #3, eight source cards. Lost: the author.",
  "transcript": ("[Google AI Overview (expanded), 2026-10-14, " + AUTH + ". The paste carries the header 'AI Mode Conversation' and echoes the query twice; "
                 "citation clusters are reduced to their numbers, links to their text; the raw paste keeps the /goto URLs.]\n\nYou said: " + Q2 + "\n" + ans + "\n\n" + rail),
  "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
  "transcript_complete": f"Complete as pasted: one operator turn and one answer with its card rail of {len(C2)} cards.",
  "reading": ("Checked 2026-10-14: deposit #3 is the AI Overview Capture Registry (AXN:0003); the registry holds Bing Copilot and Grok captures "
              "(e.g. zenodo-bans-bing-copilot-20260823, the Grok capture of 'what is spxi protocol?'); ai-overview-capture-registry-20260813 is seated. "
              "The /datasets/ card's 'v11.4 · 343 captures' is the page as indexed on 11 August."),
  "analysis": "The registry composed at its own grain from its own records, every card the archive's, the author unnamed. " + SEAT})
out.append(d)
for d in out:
    (HERE / ("capture-" + d["slug"] + ".json")).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8"); print("wrote", d["slug"])
