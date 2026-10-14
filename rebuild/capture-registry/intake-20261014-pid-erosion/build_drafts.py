#!/usr/bin/env python3
"""Author three captures from the operator's message of 2026-10-14 15:02 EDT ('new entiry.. signed out incognito both: <paste> $
<paste> $ <paste>'):
  1 AIO      'what is the pid erosion observatory?'       (paste 1; NEW address)
  2 ChatGPT  'what is the pid erosion observatory?'       (paste 2; NEW address on this surface; pair of 1)
  3 AIO      'persistent identifier erosion observatory'  (paste 3; NEW address)
Both Google pastes carry the 'AI Mode Conversation' header: the standing default records the Overview (operator, 2026-10-01).
The pastes are kept verbatim beside this script; the operator's words before them are kept in notes."""
import json, re, pathlib, sys
from urllib.parse import quote_plus
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(ROOT))
from _chatgpt_common_20261008 import parse, cite_list

OPWORDS = "new entiry.. signed out incognito both:"
Q1 = "what is the pid erosion observatory?"
Q3 = "persistent identifier erosion observatory"
AUTH = "incognito, signed out"; AUTHB = "'signed out incognito both' — operator, 2026-10-14 15:02 EDT."
SEAT = "Seated 2026-10-14 from the operator's message of 15:02 EDT, on the attestation in the same message ('signed out incognito both')."
AIO_BASIS = ("Surface not stated; the standing default applies (operator, 2026-10-01: 'assume they do [start in overview], i will specify if they "
             "begin in ai mode'). The 'AI Mode Conversation' header is the expanded Overview's residue (rule of 2026-09-21).")
ORIG = {"name": "Lee Sharks", "relation": "archive", "entity_type": "site", "spxi_treatment": "full",
        "basis": ("The PID Erosion Observatory (persistentidentifiers.org) is the archive's measurement instrument: founded 2026-07-06 as the "
                  "Platform Erosion Observatory (EA-EROSION-01, #1045), renamed on 2026-07-12 with its domain; SPXI method 0.15. Recorded 2026-10-14.")}
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
slugs = {e["slug"] for e in caps["entries"]}
PRIOR = "platform-erosion-observatory-20260811"; assert PRIOR in slugs
S1, S2, S3 = "pid-erosion-observatory-what-is-aio-20261014", "pid-erosion-observatory-what-is-chatgpt-20261014", "persistent-identifier-erosion-observatory-aio-20261014"
for s in (S1, S2, S3):
    assert s not in slugs, s
for e in caps["entries"]:
    assert (e.get("q") or "").strip().lower() not in (Q1, Q3), ("address already seated", e["slug"])
out = []


def aio(raw, q, rail_start, cards):
    head = f"AI Mode Conversation\nYou said: {q}{q}\n"; assert raw.startswith(head)
    i = raw.index(rail_start); ans, rail = raw[len(head):i], raw[i:]
    for s, t in cards:
        assert t in rail, t
    red = lambda b: re.sub(r"\[([^\]]+)\]\(https?://[^)]*\)", r"\1",
                           re.sub(r"\[\[[^\]]*\]\([^)]*\)(, \[[^\]]*\]\([^)]*\))*\]", lambda m: "[" + ", ".join(re.findall(r"\[(\d+)\]", m.group(0))) + "]", b))
    return red(ans).strip(), red(rail).strip()


# ---------------- 1. the Overview at 'what is the pid erosion observatory?'
raw1 = (HERE / "paste-pid-erosion-what-is-aio.txt").read_text(encoding="utf-8")
C1 = [("www.persistentidentifiers.org", "Persistent Identifiers — The PID Erosion Observatory"),
      ("Institut de Ciències del Mar. ICM-CSIC", "Ocean and Littoral Sedimentary Processes"),
      ("GitHub", "Account blocked and records removed — request manual review #2596 - GitHub"),
      ("www.axnidentifiers.com", "Why AXN exists — identifier erosion, measured at registry scale"),
      ("www.alexanarch.org", "platform erosion observatory — Google AI Overview, 2026-08-11 ..."),
      ("github.com", "Activity · leesharks000/platform-erosion-observatory · GitHub")]
R1 = {"www.persistentidentifiers.org": ("authored_surface", "the observatory's own page"), "Institut de Ciències del Mar. ICM-CSIC": ("third_party", "marine sedimentology; no PIDs"),
      "GitHub": ("third_party", "zenodo/zenodo issue #2596, the independent case collection; the snippet is a comment pointing to persistentidentifiers.org"),
      "www.axnidentifiers.com": ("authored_surface", "axnidentifiers.com, 'Why AXN exists'"),
      "www.alexanarch.org": ("archive_controlled", "the Capture Registry's own record of 2026-08-11 at 'platform erosion observatory'"),
      "github.com": ("authored_surface", "the observatory's repository, leesharks000/platform-erosion-observatory")}
a1, rail1 = aio(raw1, Q1, "[www.persistentidentifiers.org](https://www.persistentidentifiers.org)\nPersistent Identifiers", C1)
for s in ["the observatory treats platform modification as an active sedimentary system", "exact request hashes and `curl` data",
          "documentation published on the Zenodo GitHub Repository", "sweeping unstandardized AI-native theories or niche physics records",
          "closely tied to initiatives like AXN Identifiers (under dataset logs like `EA-EROSION-01`)",
          "sometimes referred to or built upon the codebase of the Platform Erosion Observatory"]:
    assert s in a1, s
assert "Sharks" not in a1
d1 = {"q": Q1, "slug": S1, "date": "2026-10-14", "surface": "Google AI Overview", "surface_basis": AIO_BASIS,
      "auth": AUTH, "auth_basis": AUTHB, "ev": "paste", "s": "Platform Erosion", "originator": ORIG,
      "q_kind": "the observatory's current name as a question. NEW address; the same string asked of ChatGPT the same day.",
      "related_deposits": [1045, 1081, 1408], "longitudinal_priors": [PRIOR],
      "mt": "THE OBSERVATORY AT ITS GRAIN, A MARINE CARD IN ITS METHOD, ONE INSTRUMENT SPLIT IN TWO",
      "d": ("THE OBSERVATORY AT ITS GRAIN, A MARINE CARD IN ITS METHOD, ONE INSTRUMENT SPLIT IN TWO: asked 'what is the pid erosion "
            "observatory?', the Overview names it at persistentidentifiers.org, an 'empirical measurement project that tracks identifier "
            "erosion', and gives its method from the page: dated captures, published curls, topically coherent removal waves ('AI-native "
            "theories or niche physics records'). Two things enter from outside the observatory. A marine-sedimentology card (ICM-CSIC, "
            "'Dynamics of active sedimentary systems') enters the method: 'the observatory treats platform modification as an active "
            "sedimentary system'. The zenodo/zenodo issue thread #2596 becomes 'documentation published on the Zenodo GitHub Repository'. "
            "Its last line makes the Platform Erosion Observatory a second thing the PID Erosion Observatory is 'built upon'; they are one "
            "instrument, renamed on 2026-07-12. No author is named; one card is the Capture Registry's own record of 2026-08-11."),
      "findings": ["THE INSTRUMENT AT ITS GRAIN. Dated captures, the curls published, removal waves by topic: the page's own method.",
                   "A MARINE CARD IN THE METHOD. 'an active sedimentary system', from the ICM-CSIC card on ocean and littoral sediments; erosion read across fields.",
                   "A THREAD AS DOCUMENTATION. Issue #2596 on zenodo/zenodo, an independent case collection, is given as 'documentation published on the Zenodo GitHub Repository'.",
                   "ONE INSTRUMENT AS TWO. 'built upon the codebase of the Platform Erosion Observatory': the founding name (#1045, 2026-07-06) given as a predecessor; renamed 2026-07-12.",
                   "AN EMBELLISHED FIGURE. 'exact request hashes and curl data'; the page: 'Every number on this page resolves to a dated capture; the curls are published.'",
                   "THE AUTHOR ABSENT; THE REGISTRY CITED. No name in the answer; card 5 is the Capture Registry's record at 'platform erosion observatory', 2026-08-11."],
      "cites": len(C1), "cite_list": [{"n": i + 1, "site": s, "rel": R1[s][0], "title": t, "snip": None, "url": None, "note": R1[s][1]} for i, (s, t) in enumerate(C1)],
      "archive_controlled_cites": 1,
      "sf": "Source cards: " + "; ".join(s for s, _ in C1) + ".",
      "per": 0.5, "per_v": {"author": False, "inst": False, "id": True, "src": True},
      "per_note": "Retained: the domain, the founding identifier EA-EROSION-01, the repository and the registry as cards. Lost: the author and the institution.",
      "transcript": ("[Google AI Overview (expanded), 2026-10-14, " + AUTH + ". The paste carries the header 'AI Mode Conversation' and echoes the query "
                     "twice; citation clusters are reduced to their numbers, links to their text; the raw paste keeps the /goto URLs.]\n\nYou said: " + Q1 + "\n" + a1 + "\n\n" + rail1),
      "transcript_raw": raw1, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
      "transcript_complete": f"Complete as pasted: one operator turn and one answer with its card rail of {len(C1)} cards.", "transcript_read": "READ IN FULL 2026-10-14",
      "reading": ("Checked 2026-10-14 against persistentidentifiers.org (live) and the archive: the page says 'Every number on this page resolves to a dated "
                  "capture; the curls are published', and names an 'AI-native' collateral category and a heterodox-physics sweep; it carries no "
                  "'sedimentary'. Its provenance line: 'founded 2026-07-06 as the Platform Erosion Observatory (EA-EROSION-01, deposit #1045) · "
                  "renamed the PID Erosion Observatory on 2026-07-12'. Issue #2596 on zenodo/zenodo is the independent case collection named in "
                  "the archive's CERN correspondence. EA-EROSION-01 is #1045, the observatory's founding deposit, not an AXN Identifiers log."),
      "analysis": ("The Overview holds the observatory's method at the grain of its page and loses its person; two third-party cards enter the "
                   "account as the observatory's own (a marine sedimentology programme as method, an issue thread as the host's documentation), "
                   "and the founding name is given as a second instrument. Paired with ChatGPT at the same string. " + SEAT),
      "rerun": "https://www.google.com/search?q=" + quote_plus(Q1),
      "notes": {"date_basis": "The operator's message of 2026-10-14, 15:02 EDT.", "operator_words": OPWORDS, "pair": S2}}
out.append(("capture-pid-erosion-what-is-aio-20261014.json", d1))

# ---------------- 2. ChatGPT at the same string
raw2 = (HERE / "paste-pid-erosion-what-is-chatgpt.txt").read_text(encoding="utf-8")
(a2,), seen = parse(raw2, {"The PID Erosion Observatory", "NOAA Library"})
for s in ["The PID Erosion Observatory is a website that monitors whether persistent identifiers (PIDs) continue to work as intended",
          "Comparing research databases: Checking whether deleted or retracted records disappear consistently across services such as DataCite and OpenAlex.",
          "Preserving evidence: Publishing dated observations and reproducible methods",
          "One important caveat: The PID Erosion Observatory describes itself as an independent monitoring project."]:
    assert s in a2, s
assert "Sharks" not in a2 and "SPXI" not in a2
d2 = {"q": Q1, "slug": S2, "date": "2026-10-14", "surface": "ChatGPT",
      "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'You said:', 'ChatGPT said:', 'Chat with ChatGPT').",
      "auth": AUTH, "auth_basis": AUTHB, "ev": "paste", "s": "Platform Erosion", "originator": ORIG,
      "q_kind": "the observatory's current name as a question. NEW address on this surface; the same string asked of the Overview the same day.",
      "related_deposits": [1045, 1081], "longitudinal_priors": [S1],
      "mt": "THE OBSERVATORY ANSWERED FROM ITS PAGE, QUALIFIED ONCE, ITS PERSON ABSENT",
      "d": ("THE OBSERVATORY ANSWERED FROM ITS PAGE, QUALIFIED ONCE, ITS PERSON ABSENT: asked 'what is the pid erosion observatory?', "
            "ChatGPT answers in one turn from persistentidentifiers.org (four chips, 'The PID Erosion Observatory'): a website that "
            "monitors whether persistent identifiers 'continue to work as intended'; its four areas (DOIs, Zenodo deletion records, "
            "DataCite against OpenAlex, dated observations and reproducible methods); 'erosion' as four kinds of breakdown. It adds one "
            "caveat ('describes itself as an independent monitoring project ... its methods and underlying evidence should be examined'), "
            "names no operator, no deposit and no measurement, and does not connect the observatory to SPXI."),
      "findings": ["THE PAGE HELD. The four areas and the four forms of erosion are the page's (DataCite, OpenAlex, Zenodo deletion records, dated captures).",
                   "NO FIGURE. None of the page's measurements (findable DOIs, per-epoch declines, OpenAlex persistence, retraction propagation) is given.",
                   "ONE CAVEAT. 'describes itself as an independent monitoring project'; the page names its instrument operator, Lee Sharks.",
                   "THE PERSON AND THE IDENTIFIER ABSENT. No operator, no EA-EROSION-01, no #1045; no SPXI."],
      "cites": sum(seen.values()), "cite_list": cite_list(seen, {"The PID Erosion Observatory": "authored_surface"}),
      "archive_controlled_cites": 0,
      "sf": "Source chips expose site labels only: " + "; ".join(f"{s} ×{k}" for s, k in seen.most_common()) + ".",
      "per": 0.75, "per_v": {"author": False, "inst": False, "id": False, "src": True},
      "per_note": "Retained: the observatory's site, linked and chipped. Lost: the operator, the institution, any identifier.",
      "transcript": ("[ChatGPT (chatgpt.com), signed out, incognito, 2026-10-14. One answer. Source chips inline as [chip: site +N]; the sign-in "
                     "furniture cut.]\n\n[QUERENT, turn 1]\n" + Q1 + "\n\n[ANSWER 1]\n\n" + a2),
      "transcript_raw": raw2, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (ONE ANSWER; CHIPS INLINE)",
      "transcript_complete": "One operator turn and one answer, complete as pasted.", "transcript_read": "READ IN FULL 2026-10-14",
      "reading": ("Checked 2026-10-14 against persistentidentifiers.org (live): the page measures DataCite findability, OpenAlex persistence and the "
                  "OpenAIRE Graph against Zenodo's deletion records, publishes dated epoch captures and curls, and names 'instrument operator = "
                  "Lee Sharks (maintainer of this observatory)'. The NOAA Library chip stands at the general definition of a DOI."),
      "analysis": ("ChatGPT takes the page as its one source and holds it: the four areas are the page's own, the caveat is a reader's, and the "
                   "operator the page names is not carried. Paired with the Overview at the same string. " + SEAT),
      "rerun": "https://chatgpt.com/?q=" + quote_plus(Q1),
      "notes": {"date_basis": "The operator's message of 2026-10-14, 15:02 EDT.", "operator_words": OPWORDS, "pair": S1}}
out.append(("capture-pid-erosion-what-is-chatgpt-20261014.json", d2))

# ---------------- 3. the Overview at 'persistent identifier erosion observatory'
raw3 = (HERE / "paste-pid-erosion-observatory-aio.txt").read_text(encoding="utf-8")
C3 = [("www.persistentidentifiers.org", "Persistent Identifiers — The PID Erosion Observatory"),
      ("www.alexanarch.org", "The Platform Erosion Observatory: The Zenodo Removal Census as ..."),
      ("GitHub", "persistent-identifiers · GitHub Topics"),
      ("www.alexanarch.org", "platform erosion observatory — Google AI Overview, 2026-08-11 ..."),
      ("github.com", "GitHub - leesharks000/platform-erosion-observatory: Platform ..."),
      ("www.axnidentifiers.com", "Why AXN exists — identifier erosion, measured at registry scale"),
      ("medium.com", "THE OBELUS AND THE TOMBSTONE: On the Two Marks of ...")]
N3 = ["the observatory's own page", "#1045's wiki article", "GitHub's persistent-identifiers topic, listing the observatory's repository",
      "the Capture Registry's own record of 2026-08-11 at 'platform erosion observatory'", "the observatory's repository",
      "axnidentifiers.com, 'Why AXN exists'", "THE OBELUS AND THE TOMBSTONE (#1068), on Medium"]
REL3 = ["authored_surface", "archive_controlled", "third_party", "archive_controlled", "authored_surface", "authored_surface", "authored_surface"]
a3, rail3 = aio(raw3, Q3, "[www.persistentidentifiers.org](https://www.persistentidentifiers.org)\nPersistent Identifiers", C3)
for s in ["The Platform Erosion Observatory (also known as the PID Erosion Observatory)", "PIDs are not permanent strings, but rather maintained relations",
          "Measuring \"Custody Separation\"", "the \"shape of absence\"", "Acting as its primary case study instrument (Case 001), it tracks a specific cohort of over 14,000 DOIs",
          "vanish from the Zenodo repository", "spearheaded by researcher Lee Sharks", "The Severance Registry / Resolution Index",
          "The Capture Registry: An engine designed to capture asymmetry in how corrections and representation changes are documented across repositories."]:
    assert s in a3, s
d3 = {"q": Q3, "slug": S3, "date": "2026-10-14", "surface": "Google AI Overview", "surface_basis": AIO_BASIS,
      "auth": AUTH, "auth_basis": AUTHB, "ev": "paste", "s": "Platform Erosion", "originator": ORIG,
      "q_kind": "the observatory's name spelled out, without the article or a question. NEW address.",
      "related_deposits": [1045, 1068, 1067, 1408, 1044], "longitudinal_priors": [PRIOR, S1],
      "mt": "BOTH NAMES HELD, THE OPERATOR NAMED, CASE 001 MOVED TO ZENODO",
      "d": ("BOTH NAMES HELD, THE OPERATOR NAMED, CASE 001 MOVED TO ZENODO: at 'persistent identifier erosion observatory' the Overview "
            "gives the instrument under both names ('The Platform Erosion Observatory (also known as the PID Erosion Observatory)'), its "
            "premise ('PIDs are not permanent strings, but rather maintained relations'), its measures (custody separation, tombstone "
            "compliance, 'the shape of absence'), its roadmap, and names its operator: 'a broader, sovereign alternative tracking "
            "architecture spearheaded by researcher Lee Sharks'. It places the Severance Registry / Resolution Index and the Capture Registry "
            "beside it, the latter in the archive's own words (#1067: 'the Capture Registry measures representation and correction "
            "asymmetry'). One figure moves: Case 001, the 14,284 DataCite DOIs of the Firenze client crui.unifi (#1408), becomes 'a specific "
            "cohort of over 14,000 DOIs' tracked for 'how, why, and when records vanish from the Zenodo repository'."),
      "findings": ["ONE INSTRUMENT, BOTH NAMES. 'The Platform Erosion Observatory (also known as the PID Erosion Observatory)'; at the 'what is' string the same day the two were split.",
                   "THE OPERATOR NAMED. 'spearheaded by researcher Lee Sharks'.",
                   "THE ARCHIVE'S OWN DIVISION OF LABOUR. Custody separation (the observatory), correction asymmetry (the Capture Registry): #1067's sentence, distributed.",
                   "CASE 001 MOVED. The Firenze crui.unifi corpus at DataCite (14,284 DOIs; #1408) given as the Zenodo Removal Census's Zenodo cohort.",
                   "THE REGISTRY CITED. Card 4 is the Capture Registry's record at 'platform erosion observatory', 2026-08-11; card 2 is #1045's wiki article."],
      "cites": len(C3), "cite_list": [{"n": i + 1, "site": s, "rel": REL3[i], "title": t, "snip": None, "url": None, "note": N3[i]} for i, (s, t) in enumerate(C3)],
      "archive_controlled_cites": 2,
      "sf": "Source cards: " + "; ".join(s for s, _ in C3) + ".",
      "per": 0.5, "per_v": {"author": True, "inst": False, "id": False, "src": True},
      "per_note": "Retained: the operator by name and the observatory's surfaces as cards. Lost: the institution and any identifier.",
      "transcript": ("[Google AI Overview (expanded), 2026-10-14, " + AUTH + ". The paste carries the header 'AI Mode Conversation' and echoes the query "
                     "twice; citation clusters are reduced to their numbers, links to their text; the raw paste keeps the /goto URLs.]\n\nYou said: " + Q3 + "\n" + a3 + "\n\n" + rail3),
      "transcript_raw": raw3, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
      "transcript_complete": f"Complete as pasted: one operator turn and one answer with its card rail of {len(C3)} cards.", "transcript_read": "READ IN FULL 2026-10-14",
      "reading": ("Checked 2026-10-14: 'Rate measures attribution separation; the Platform Erosion Observatory measures custody separation; the Capture "
                  "Registry measures representation and correction asymmetry' is #1067's; 'a 14,284-DOI control cohort' and 'the shape of absence' "
                  "are the observatory's own description (spxi.dev, method 0.15); PEO Case 001 is #1408, 'T0 Enumeration of the Firenze crui.unifi "
                  "Corpus (14,284 DOIs)', a DataCite client collapse (14,283 → 0, 13–20 July 2026), not a Zenodo cohort; 1,838 severed identifiers "
                  "through the Resolution Index is #1068's card snippet."),
      "analysis": ("At the spelled-out name the Overview holds the instrument whole, both names as one, with its operator named and the archive's "
                   "own division of labour among its instruments; the error is at one figure, a DataCite case carried into the Zenodo census. "
                   "Against the 'what is' Overview the same day, the names that one split are here joined. " + SEAT),
      "rerun": "https://www.google.com/search?q=" + quote_plus(Q3),
      "notes": {"date_basis": "The operator's message of 2026-10-14, 15:02 EDT.", "operator_words": OPWORDS}}
out.append(("capture-persistent-identifier-erosion-observatory-aio-20261014.json", d3))

for name, d in out:
    (HERE / name).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", name, "|", d["slug"])
