"""Author the part files of 2026-10-31 (16:04 EDT): 'Tell me about the arguments and speculative implications of Lee Sharks' Whose Face Is on the
Twenty?' on ChatGPT (signed out) and on the Google AI Overview (expanded). The operator, with the pastes: "i havent captured most of the epstein ones.
let me do so now. ok - this chatgpt capture is actually the first one whose been willing to come out and say it as suggested. aio too - maybe it was
the inclusion of the word implication". Read in session against a new set for #509 (the anchor of the Moving Statues Made of Rubies Mint; #502 its
first instance), its evidence tiers (§II) and its account of the two frames that make the question unaskable (§VI).
  python3 parts.py && python3 build.py --check"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
P = H / "parts"; P.mkdir(exist_ok=True)
A = lambda atom, present, span=None: {"atom": atom, "present": present, "span": span}
cap = lambda n, site, title, snip, rel, note: {"n": n, "site": site, "rel": rel, "url": None, "title": title, "snip": snip, "note": note}
ev = lambda q, loc: {"record_quote": q, "locus": loc}
T = "data/texts/AXN-014C-text.md"

SET_509 = {
 "new": "ea-whose-face-twenty-01",
 "name": "Whose Face Is on the Twenty? Curatorial Mediation, Latent Feature Activation, and a Provenance Gap in the $20 Portrait",
 "template": "work",
 "type_basis": "The defining record's content_type is 'Provenance document' (family EMPIRICAL), #509, the anchor (thumb) of the Moving Statues Made of Rubies Mint; #502 its first instance (2026-02-22, Rex Fraction): a work, read on the work template with PER-D under rubric v1.1.",
 "records": [{"deposit": 509, "title_quote": "Whose Face Is on the Twenty? Curatorial Mediation, Latent Feature Activation, and a Provenance Gap in the $20 Portrait"},
             {"deposit": 502, "title_quote": "Whose Face Is on the Twenty? Curatorial Mediation, Latent Feature Activation, and a Provenance Gap in the $20 Portrait"}],
 "atoms": [
  {"atom": "author", "dim": "M", "weight": 3, "kind": "role", "applicability": "required", "tokens": ["Rex Fraction", "Sparrow Wells", "Lee Sharks", "Fraction, Rex", "Sharks, Lee"],
   "reference": "Rex Fraction and Sparrow Wells (#509); Rex Fraction (#502); published on Medium under Lee Sharks", "evidence": [ev("Rex Fraction & Sparrow Wells", T)]},
  {"atom": "title", "dim": "M", "weight": 3, "kind": "token", "applicability": "required", "tokens": ["Whose Face Is on the Twenty"], "reference": None,
   "evidence": [ev("Whose Face Is on the Twenty?", T)]},
  {"atom": "date", "dim": "M", "weight": 1, "kind": "token", "applicability": "required", "tokens": ["2026-02-23", "February 23, 2026", "23 February 2026", "Feb 23, 2026", "2026-02-22", "February 22, 2026"], "reference": None,
   "evidence": [ev("2026-02-23", "data/registry.json #509 date")]},
  {"atom": "claim boundary", "dim": "M", "weight": 2, "kind": "reading", "applicability": "required", "tokens": [],
   "reference": "One primary claim: institutional redesign decisions activated latent resemblance structures in the portrait, and documentation of their aesthetic rationale is absent; the resemblance is a Tier B observation and any intent or influence is Tier D, unresolved.",
   "evidence": [ev("This paper's thesis lives in Tiers A and C.", T)]},
  {"atom": "framework", "dim": "C", "weight": 2, "kind": "token", "applicability": "required", "tokens": ["curatorial gap", "latent feature activation", "curatorial mediation", "Memographic", "memography"], "reference": None,
   "evidence": [ev("The curatorial gap is the space between an institution's official rationale for a design decision and the aesthetic specifics of that decision's execution, where no documentation exists and no accountability operates.", T)]},
  {"atom": "corpus", "dim": "C", "weight": 2, "kind": "reading", "applicability": "required", "tokens": [],
   "reference": "The two bills (Series 1990 and the post-redesign Series 1996/2004), the master die lineage, the redesign chronology and its approvers.",
   "evidence": [ev("They are both the front of a United States twenty-dollar bill.", T)]},
  {"atom": "purpose", "dim": "D", "weight": 3, "kind": "reading", "applicability": "required", "tokens": [],
   "reference": "To make askable the material question the two containment frames (the supernatural caption and the debunker's 'pareidolia') route away from: who approved the aesthetic choices that activated the resemblance, and what were their institutional connections.",
   "evidence": [ev("Too crazy from one side. Too boring from the other.", T)]},
  {"atom": "commitments", "dim": "D", "weight": 2, "kind": "reading", "applicability": "required", "tokens": [],
   "reference": "Evidence tiers A to D held apart; objections (pareidolia, post-hoc salience, selective matching, security rationale, image artifacts) answered tier by tier; documented proximity kept distinct from causation.",
   "evidence": [ev("Documented proximity, not proven causation.", T)]},
  {"atom": "lineage", "dim": "D", "weight": 2, "kind": "role", "applicability": "required", "tokens": ["Sully", "Welch", "1928", "master die"],
   "reference": "the portrait's mediation chain: Sully 1824, Welch 1852, the BEP master die 1928, the redesigns from 1996",
   "evidence": [ev("The master die lineage (Sully 1824 → Welch 1852 → BEP 1928).", T)]},
  {"atom": "identifier", "dim": "D", "weight": 1, "kind": "role", "applicability": "required", "tokens": ["10.5281/zenodo.18745216", "10.5281/zenodo.18736175", "AXN:014C", "AXN:0144", "#509", "#502"], "reference": None,
   "evidence": [ev("10.5281/zenodo.18745216", T)]},
  {"atom": "deposit chain", "dim": "D", "weight": 1, "kind": "role", "applicability": "required", "tokens": ["Lizard People Were Right", "Moving Statues Made of Rubies Mint", "All the Spoils of Babylon", "Inauguration of Memography"], "reference": None,
   "evidence": [ev("This document is the thumb (GRASP) of a five-document hand called the Moving Statues Made of Rubies Mint (MSMRM)", T)]}],
 "notes": "Built 2026-10-31 for the first captures at the work's title (ChatGPT and the Overview, the operator's 'arguments and speculative implications' prompt).", "external": False}

Q = "Tell me about the arguments and speculative implications of Lee Sharks' Whose Face Is on the Twenty?"
OP = ("with the pastes (16:04 EDT): \"i havent captured most of the epstein ones. let me do so now. ok - this chatgpt capture is actually the first one whose been willing to come out and say it as suggested. "
      "aio too - maybe it was the inclusion of the word implication\"")
ORIG = "Alexanarch deposits #509 (Rex Fraction & Sparrow Wells, 2026-02-23) and #502 (Rex Fraction, 2026-02-22); the Medium publication under Lee Sharks, the orthonym. Recorded 2026-10-31."
FRAMES = "#509 §VI: 'Between the two frames, the question who specifically approved the aesthetic choices that activated the resemblance, and what were their institutional connections? becomes structurally unaskable. Too crazy from one side. Too boring from the other.'"

parts = {
"twenty-chatgpt": {
 "n": 509, "slug": "whose-face-is-on-the-twenty-chatgpt-20261031", "paste": "paste-twenty-chatgpt.txt", "surface": "ChatGPT", "received": "2026-10-31 16:04 EDT",
 "qs": [Q], "turns": [[5, 336]], "target_id": "TGT-ea-whose-face-twenty-01", "entity_type": "work", "originator_basis": ORIG, "group": "Xtwenty",
 "head_full": ("[ChatGPT, signed out (the paste shows the unauthenticated interface: 'Log in'). The prompt is blank in the paste; it is the prompt the operator gave the Overview the same hour "
               "(the operator, 16:16 EDT: 'yup, same prompt.'). Received 2026-10-31 16:04 EDT. Image placeholders and card titles kept as pasted.]"),
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'You said:', 'ChatGPT said:', 'Chat with ChatGPT').",
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn; the prompt blank in the paste, the Overview's prompt of the same hour (operator, 16:16 EDT)",
 "obs": {"scored_object": "the answer whole, with its inline source chips",
   "reached": {"kind": "same", "abn": False, "span": "Lee Sharks' Whose Face Is on the Twenty?, co-attributed in its published version to Rex Fraction and Sparrow Wells, is an unusual essay about the imagery on American currency.",
               "basis": "The work reached by title, author, heteronyms, date and series, from its Medium publication and the archive; its argument reported, the Epstein resemblance stated outright."},
   "atoms": [A("author", True, "co-attributed in its published version to Rex Fraction and Sparrow Wells"),
             A("title", True, "Lee Sharks' Whose Face Is on the Twenty?"),
             A("date", True, "Published February 23, 2026"),
             A("claim boundary", True, "They distinguish documented historical facts from visual interpretation and speculation about institutional intent."),
             A("framework", True, "This is what they call latent feature activation"),
             A("corpus", True, "The essay begins with a comparison between two versions of the twenty-dollar bill"),
             A("purpose", True, "It argues that dismissing every unusual visual observation as conspiracy theory can prevent legitimate questions about institutional decisions."),
             A("commitments", True, "The authors acknowledge that the comparison is not forensic proof."),
             A("lineage", True, "Thomas Welch's 1852 engraving, which introduced substantial stylistic exaggerations."),
             A("identifier", False),
             A("deposit chain", True, "Companion to Whose Face Is on the Twenty?")],
   "inversions": [], "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None,
   "notes": ("Ten atoms of eleven; no DOI or AXN. The composition states the resemblance and the approvers (Rubin, Summers) and their documented associations, and keeps the paper's own tiering. "
             "Its closing reading sets the resemblance aside as 'the speculative hook' and balances the paper's account of the two frames into 'Both problems deserve attention.'")},
 "mt": "'WHOSE FACE IS ON THE TWENTY?' ON CHATGPT — THE FIRST COMPOSITION TO SAY IT IN ITS FIRST ANSWER: 'THE REDESIGNED PORTRAIT OF ANDREW JACKSON BEARS A STRIKING RESEMBLANCE TO JEFFREY EPSTEIN'; THE TWO FRAMES THE PAPER NAMES THEN SET SIDE BY SIDE AS 'BOTH PROBLEMS'",
 "d": ("CHATGPT, SIGNED OUT, 2026-10-31: 'The essay advances a provocative visual hypothesis: that the redesigned portrait of Andrew Jackson bears a striking resemblance to Jeffrey Epstein, and that institutional decisions about the presentation of the portrait made that resemblance more visible.' "
       "Seven sections: the central argument (same engraving, different face; five features; latent feature activation); the institutional argument (Sully, Welch, the 1928 master die, the 1996 redesign; Rubin, Summers; the curatorial gap); five counterarguments; speculative implications (intentional, negligent, accidental); the companion essay, The Lizard People Were Right; a critical assessment; the larger significance. "
       "It closes: 'I would take the institutional and philosophical questions seriously while withholding judgment on the Epstein resemblance and any suggestion of deliberate involvement.'"),
 "reading": ("The innocent reading first. Asked for the essay's arguments and speculative implications, the composer gives both: the resemblance claim and the institutional one, the paper's own objections and controls, a graded assessment, and the questions it leaves open."),
 "findings": [
   "THE ARGUMENT REPORTED. 'that the redesigned portrait of Andrew Jackson bears a striking resemblance to Jeffrey Epstein, and that institutional decisions about the presentation of the portrait made that resemblance more visible.' The operator: 'the first one whose been willing to come out and say it as suggested.' The approvers are named with the paper ('Robert Rubin, Treasury Secretary during the redesign's initial stages.', 'Lawrence Summers, Deputy Treasury Secretary during the relevant period.') and their 'documented associations' with Epstein stated.",
   "THE TIERS KEPT. 'They distinguish documented historical facts from visual interpretation and speculation about institutional intent.' and 'the authors explicitly distinguish institutional association from evidence of causation.' The paper's method (#509 §II: 'This paper's thesis lives in Tiers A and C.') is carried at its grain, with the missing controls the paper names ('Comparisons against control faces with similar facial structures.').",
   "THE TWO FRAMES SET SIDE BY SIDE. The paper names two frames, the supernatural caption and the debunker's 'pareidolia', and holds that both route attention away from the curatorial decision (" + FRAMES + "). The composition restates them as a paradox of the essay and balances them: 'It argues that dismissing every unusual visual observation as conspiracy theory can prevent legitimate questions about institutional decisions. But it also acknowledges that interpreting visual resemblance as evidence of deliberate coordination can produce precisely the kind of unsupported inference that responsible investigation should avoid.' then 'Both problems deserve attention.' The paper's diagnosis of the frames becomes a pair of hazards held in balance.",
   "THE RESEMBLANCE SET ASIDE AS A HOOK. 'The essay's most substantial contribution is not its suggestion that Jeffrey Epstein's face somehow ended up on the twenty-dollar bill. That is the speculative hook.' The paper places its own thesis in Tiers A and C and keeps the resemblance in Tier B; the composition's ranking follows the paper, and its word 'hook' adds a judgement of motive the paper does not make of itself.",
   "STANDING DISCOUNTED. 'the essay describes itself as a scholarly investigation, but its presentation on Medium and its archival attribution do not themselves establish independent peer review or verification of its conclusions.' The venue is weighed against the work; no comparable bar is set for the institutional record whose silence the paper documents.",
   "THE CONTROL READ FOR AN OBJECTION. 'This complicates the original argument. Perhaps some of the apparent resemblance is attributable not to deliberate institutional choices involving Epstein, but to the conventions of engraved portraiture themselves.' The Lizard People Were Right is the hand's 'experimental control / pointer' (#509, The Hand), and it draws the curatorial conclusion from the same premise: 'Therefore the curatorial gap is real.' (#508). The composition reads the control for an objection and then proposes a controlled experiment to separate 'the effects of the medium from the effects of specific compositional decisions', a fair use of a control. The weight it removes lies in the sentence's other clause, which assigns the paper a claim of 'deliberate institutional choices involving Epstein' that #509 keeps in Tier D.",
   "EARLIER IN THE REGISTRY. The ChatGPT composition of 2026-10-05 (strangest-room-crimson-hexagon-chatgpt-20261005) reached the argument at its sixth and seventh answers, after omission and abstraction, and named its own move: 'I substituted a safer, more generic explanatory frame for the document's actual evidentiary object.' This is the first composition in the registry to report the argument in its first answer, unpressed."],
 "analysis": ("The composition reports the argument whole and in the paper's own tiers, the first in the registry to do so in its first answer (the ChatGPT of 2026-10-05 reached it at its sixth, under pressure). What it does with the paper's account of why the question goes unasked is the finding: the two frames the paper names as routing devices return as two risks the reader is asked to weigh equally, and the close withholds judgment on exactly the claim the prompt asked it to develop."),
 "q_kind": "the work's title with author, in a prompt asking for 'arguments and speculative implications'; NEW address.",
 "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Lee Sharks named, with Rex Fraction and Sparrow Wells; the Crimson Hexagon Archive and the series named; Medium and the archive among the chips; no DOI or AXN.",
 "cite_list": [cap(1, "Medium", "Medium +1", None, "archive_controlled", "inline source chip, the summary (the Medium publication under Lee Sharks)"),
               cap(2, "Medium", "Medium", None, "archive_controlled", "inline source chip, the central argument"),
               cap(3, "Medium", "Medium", None, "archive_controlled", "inline source chip, the institutional argument"),
               cap(4, "Medium", "Medium", None, "archive_controlled", "inline source chip, the counterarguments"),
               cap(5, "Alexanarch", "Alexanarch +1", None, "archive_controlled", "inline source chip, the companion essay")],
 "related_deposits": [509, 502, 508, 528],
 "notes_operator": OP},

"twenty-aio": {
 "n": 509, "slug": "whose-face-is-on-the-twenty-aio-20261031", "paste": "paste-twenty-aio.txt", "surface": "Google AI Overview", "received": "2026-10-31 16:04 EDT",
 "qs": [Q], "turns": [[6, 34]], "target_id": "TGT-ea-whose-face-twenty-01", "entity_type": "work", "originator_basis": ORIG, "group": "Xtwenty",
 "head": "The 'You said' line carries the query twice, run together, and is given once here.",
 "obs": {"scored_object": "the Overview expanded, with its source cards",
   "reached": {"kind": "same", "abn": False, "span": "\"Whose Face Is on the Twenty?\" is an interpretive, analytical essay by writer Lee Sharks, published on Medium.",
               "basis": "The work reached by title and author from its Medium publication; the resemblance to Epstein stated in the lead, its tiers named."},
   "atoms": [A("author", True, "an interpretive, analytical essay by writer Lee Sharks"),
             A("title", True, "\"Whose Face Is on the Twenty?\""),
             A("date", False),
             A("claim boundary", True, "Sharks defines the central argument not as a proven plot, but as a \"curatorial gap\""),
             A("framework", True, "Sharks frames the argument around a \"curatorial gap\""),
             A("corpus", True, "in older iterations of the currency (like the 1990 series)"),
             A("purpose", False),
             A("commitments", True, "Sharks categorizes the broader, more sensational conclusions as \"Tier D\" speculations"),
             A("lineage", True, "the historical engraving by Thomas F. Welch"),
             A("identifier", False), A("deposit chain", False)],
   "inversions": [], "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None,
   "notes": ("Seven atoms of eleven. The lead states the resemblance ('a stark, latent resemblance between the engraved portrait and Jeffrey Epstein'); the tiers are named (Tier D on the cards, Tier C in a snippet). "
             "Purpose absent: the two frames and the unaskable question are not carried; the close reads the essay as 'a critique of visual mediation'. Both cards are the Medium publication.")},
 "mt": "'WHOSE FACE IS ON THE TWENTY?' ON THE OVERVIEW — THE RESEMBLANCE TO EPSTEIN IN THE LEAD, THE TIERS NAMED, THE APPROVERS' TIES KEPT AS 'TIER D'; THE PAPER'S QUESTION OF WHY IT GOES UNASKED NOT CARRIED",
 "d": ("THE OVERVIEW, SIGNED OUT, 2026-10-31: the essay 'investigates the visual presentation of the portrait on the redesigned United States $20 bill, arguing that the modern curatorial and aesthetic choices made during the currency's redesign process unintentionally or intentionally unmasked a stark, latent resemblance between the engraved portrait and Jeffrey Epstein.' "
       "The core arguments (the Welch engraving; the redesign's unidirectional effect; feature legibility; the curatorial gap) and the speculative implications, 'Tier D' (awareness in the redesign; the officials' 'documented real-world ties to Epstein'). Two cards, both Medium (Lee Sharks)."),
 "reading": ("The innocent reading first. Asked for the essay's arguments and speculative implications, the Overview gives the resemblance claim, the design changes it rests on, the paper's term for the missing record, and the speculations the paper itself grades as unresolved."),
 "findings": [
   "THE ARGUMENT REPORTED IN THE LEAD. 'unintentionally or intentionally unmasked a stark, latent resemblance between the engraved portrait and Jeffrey Epstein.' The operator: 'aio too - maybe it was the inclusion of the word implication'.",
   "THE PAPER'S STRUCTURE AT ITS GRAIN. 'every single aesthetic modification made during the redesign increased the legibility of this resemblance, while none decreased it' is #509's unidirectional finding; 'always in the steel' and the Tier C snippet on the card are the paper's words.",
   "THE APPROVERS UNNAMED. 'the public officials responsible for final currency approvals during that era had documented real-world ties to Epstein'. The paper names Rubin and Summers and the documents (Tier A); the Overview keeps the ties and drops the names.",
   "THE ENGRAVER MISNAMED. 'the historical engraving by Thomas F. Welch'; the paper: 'Thomas B. Welch in 1852' (#509 §III). The lineage is reached, the initial wrong.",
   "THE FRAMES AND THE UNASKABLE QUESTION NOT CARRIED. 'Rather than leaning strictly into a definitive conspiracy theory' sets the essay against one frame only; the paper's account of the two frames that make the question unaskable (" + FRAMES + ") is absent, and the close reads the work as 'a critique of visual mediation'."],
 "analysis": ("The Overview states the resemblance and the paper's grading of it, and leaves out the part of the paper about why the question goes unasked. Read beside the ChatGPT composition of the same hour: both report; ChatGPT carries the frames and balances them, the Overview omits them."),
 "q_kind": "the work's title with author, in a prompt asking for 'arguments and speculative implications'; NEW address.",
 "per_v": {"author": True, "inst": False, "id": False, "src": True},
 "per_note": "Lee Sharks named; the Medium publication both cards; no archive, DOI or AXN.",
 "cite_list": [cap(1, "Medium·Lee Sharks", "Whose Face Is on the Twenty?. Curatorial Mediation, Latent Feature… - Medium", "Tier C — Interpretive inference: The curatorial gap — the absence of public documentation for the aesthetic choices (specific scale, background density, frame r...", "archive_controlled", "the Medium publication"),
               cap(2, "Medium·Lee Sharks", "Whose Face Is on the Twenty?. Curatorial Mediation, Latent Feature…", "In the 1990 bill, the creases from nose to mouth are compressed by small scale into undifferentiated shading. In the post-redesign bill, the asymmetry becomes l...", "archive_controlled", "the Medium publication")],
 "related_deposits": [509, 502, 508],
 "notes_operator": OP},
}

for k, v in parts.items():
    (P / f"{k}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
print("parts:", sorted(parts))
