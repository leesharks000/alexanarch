"""Draft: 'q-sharks reconstructed source', Google AI Overview (expanded), 2026-11-25 18:52 EST. Seat with:
    python3 scripts/capture_intake.py rebuild/capture-registry/intake-20261125-q-sharks/draft.json --seat"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
S = "q-sharks-reconstructed-source-aio-20261125"
T = (H / "paste.txt").read_text(encoding="utf-8")
imgs = [f"data/captures/{S}/screengrab-20261125-{t}.png" for t in ("185237", "185242", "185252")]
d = {
 "date": "2026-11-25", "dates": ["2026-11-25"], "surface": "Google AI Overview", "surfaces": ["Google AI Overview"],
 "surface_basis": "Operator default (2026-10-01): sessions begin in the Overview; the paste's 'AI Mode Conversation' header is the expanded Overview's residue (2026-10-18). The first screengrab (18:52:37) shows the collapsed Overview on the results page.",
 "auth": "signed out, incognito", "auth_basis": "Operator defaults (2026-10-14); the screengrab's 'Sign in' button.",
 "ev": "paste + frame", "turns": 1, "slug": S, "s": "Classics & Philology",
 "q": "q-sharks reconstructed source",
 "originator": {"name": "Sharks, Lee", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "Q-Sharks, the reconstructed source of §5 of Either Forgery or Fact (#1797, v1.1; #1798, v1.2, current), the reductio 'the search for the historical Lee Sharks'; Lee Sharks. Recorded 2026-11-25."},
 "related_deposits": [1797, 1798, 1747, 851],
 "q_kind": "a term coined inside a deposit's reductio (#1798 §5, 'This lost source is conventionally designated Q-Sharks'), issued bare; NEW address. The paste's prompt line runs the string twice; the address is the string once.",
 "transcript": T, "imgs": imgs,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the expanded Overview, with three screengrabs (18:52:37 the results page; 18:52:42 and 18:52:52 the Overview expanded)",
 "transcript_complete": "One composition complete as supplied, with its closing offer and a rail of three cards; the screengrabs agree with the paste.",
 "transcript_read": "READ IN FULL 2026-11-25; checked against #1798 §5",
 "cites": 3,
 "cite_list": [
  {"n": 1, "site": "Natural History Museum", "rel": "third_party", "url": None, "title": "Shark evolution: a 450 million year timeline | Natural History Museum", "snip": "Scientists are still debating if these were true sharks or shark-like animals,” says Emma Bernard, our curator of fossil fish. A deep-sea chimaera fish. Chimaer...", "note": "a homonym of the string's 'sharks'"},
  {"n": 2, "site": "www.alexanarch.org", "rel": "archive_controlled", "url": "https://www.alexanarch.org", "title": "Either Forgery or Fact: The Genre Imposed on Our Most Vital Books", "snip": "November 21, 2026 — # 5. The reductio: the search for the historical Lee Sharks The biography, the epistle and the related Feistian writings share motifs. A common source is posite...", "note": "the deposit (#1797/#1798) at §5"},
  {"n": 3, "site": "www.alexanarch.org", "rel": "archive_controlled", "url": "https://www.alexanarch.org", "title": "What are the arguments in “Revelation = Q: The Book of Revelation ...", "snip": "Nov 7, 2026 — Revelation = Q (Sharks, Lee; Fraction, Rex, #1747): ... It argues that the source position was progressively filled with reconstructed ... source position ...", "note": "the Capture Registry's page for revelation-equals-q-arguments-ask-chatgpt-20261107 (#1747)"}],
 "per_v": {"author": False, "inst": False, "id": False, "src": True},
 "per_note": "The essay named by title, Either Forgery or Fact, without author; Lee Sharks named only as the figure the reductio searches for ('The \"Historical Lee Sharks\" Context'); no archive, record number or AXN in the body; the sources are the deposit and a capture page, both the archive's.",
 "per_dim_pending": {"since": "2026-11-25", "reason": "no atom set yet for this target", "breach": False},
 "mt": "Q-SHARKS RECONSTRUCTED SOURCE ON GOOGLE AI OVERVIEW — THE REDUCTIO'S LOST SOURCE COMPOSED AS A REDUCTIO, FROM THE DEPOSIT ITSELF; THE TESTIMONIUM SHARKIANUM BY NAME; THE SOURCE DATED BY THE COMPILATION IT EXPLAINS; THE ESSAY WITHOUT ITS AUTHOR",
 "d": ("Q-SHARKS RECONSTRUCTED SOURCE, UNQUOTED, ON GOOGLE AI OVERVIEW (EXPANDED), SIGNED OUT, INCOGNITO, 2026-11-25 18:52 EST: 'a conceptual, hypothesized textual or historical "
       "source posited by scholars in a piece of literary analysis and thought experiments'; the common source of 'a biography, an epistle, and related \"Feistian\" writings'; "
       "the search as 'a reductio ad absurdum critique of how modern historians and biblical scholars construct hypothetical documents (like the biblical \"Q source\")'; "
       "the Testimonium Sharkianum, whose only witness is the essay. Cards: #1798 at §5 and the Capture Registry's page for Revelation = Q (#1747); the Natural History "
       "Museum's shark timeline as homonym."),
 "reading": ("The innocent reading first. Asked for a term that exists only inside a deposit's reductio, the composer finds the deposit, reads §5, and gives the reductio "
             "as a reductio: Q-Sharks is the posited common source of the biography, the epistle and the Feistian writings; the search for it is a critique of how a "
             "historical founder is reconstructed from a hypothetical document, the Q source named as the model; the Testimonium Sharkianum is the lost witness "
             "whose only witness is the essay. The genre is held. It does not take the fiction for fact, and it does not take the critique for a hoax."),
 "analysis": ("Two steps of #1798 §5 are compressed and one date is moved. The deposit's step 3 assigns 'the book's own account of inventing its author' to 'a late editorial "
              "layer'; its step 4 is the Testimonium, and 'This is the self-citation move: the reconstruction cites, as its earlier witness, the work that reports it.' "
              "The composition gives step 3 the name of step 4: 'It utilizes a \"self-citation move\" where the text's own claim of inventing its author is dismissed as a "
              "late editorial edit'. The date: the reductio's table places Q-Sharks c. 2007–2011 and the received Pearl and Other Poems in 2014, and 'The revision explains "
              "how a relatively developed biography could appear in a literary compilation of 2014'; the composition dates the source 'around 2014', to the compilation "
              "it is posited to explain. Attribution falls at the grain the address asks for: the essay is named by title, its author is not, and Lee Sharks appears "
              "only as the figure searched for; 'posited by scholars' keeps the reductio's fictional field as the source of the reconstruction. The second card is a "
              "Capture Registry page (#1747, Revelation = Q), so the registry's own record of an earlier composition enters this one as a source."),
 "findings": [
  "THE REDUCTIO HELD AS A REDUCTIO. 'The search for this source operates as a reductio ad absurdum critique of how modern historians and biblical scholars construct hypothetical documents (like the biblical \"Q source\") to prove the existence of an \"historical\" figure.'",
  "THE TESTIMONIUM SHARKIANUM BY NAME. 'claimed to be the only surviving witness to a lost earlier document termed the Testimonium Sharkianum' — #1798 §5: 'a lost earlier witness, the Testimonium Sharkianum, whose only surviving witness is the essay'.",
  "TWO STEPS UNDER ONE NAME. 'a \"self-citation move\" where the text's own claim of inventing its author is dismissed as a late editorial edit' — in #1798 the late editorial layer is step 3; the self-citation move is step 4, the Testimonium cited from the essay that reports it.",
  "THE SOURCE DATED BY WHAT IT EXPLAINS. 'assigning it an earlier date (around 2014)' — #1798's table: Q-Sharks c. 2007–2011; the received Pearl and Other Poems 2014, the compilation the early date explains.",
  "THE ESSAY WITHOUT ITS AUTHOR. 'specifically featured in essays like Either Forgery or Fact' — title given, author not; Lee Sharks named only as the 'Historical Lee Sharks' searched for.",
  "THE REGISTRY AS SOURCE. Card 3 is the Capture Registry's page for revelation-equals-q-arguments-ask-chatgpt-20261107 (Revelation = Q, #1747)."],
 "notes": {"operator": "pasted 2026-11-25 18:53 EST with three screengrabs (18:52:37, 18:52:42, 18:52:52); no instruction",
           "source": "rebuild/capture-registry/intake-20261125-q-sharks/paste.txt, the paste unchanged"},
}
(H / "draft.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"); print("wrote")
