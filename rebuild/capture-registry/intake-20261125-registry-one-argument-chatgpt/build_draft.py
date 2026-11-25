"""Draft: the Capture Registry read as a living body, one argument from first deposit to latest, ChatGPT, 2026-11-25. Seat with:
    python3 scripts/capture_intake.py rebuild/capture-registry/intake-20261125-registry-one-argument-chatgpt/draft.json --seat"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
paste = (H / "paste.txt").read_text(encoding="utf-8")
Q = ("Read the Capture Registry at alexanarch.org as a living body of thought. Follow one argument through it from its first deposit to its latest. "
     "Ground each claim in the deposits.")
T2 = ("not every configuration can do this. the configuration itself is authored: inter- and intra-configuration porosity, division of labor, "
      "mutual corrigibility, accountable provenance, exogenous inscription, material witness of sources, and above all the accrued contextual "
      "operation of the archive itself as a context and workable body. that is the authored result.")
cut = paste.index("Yes. That corrects something fundamental")
T = paste[:cut] + "[QUERENT] " + T2 + "\n\n" + paste[cut:]
chips = [("alexanarch.org +1", "after §1, #1"), ("alexanarch.org +1", "after §2, #863"), ("alexanarch.org +2", "after §3, #1611, #1665, #1671"),
         ("alexanarch.org +1", "after §4, #1612–#1615"), ("Alexanarch", "after the registry documentation's rules and failures"),
         ("Capture Registry (EA-WG-CAPTURES-01) +1", "after §5, #1766, #1783, #1789"), ("Capture Registry (EA-WG-CAPTURES-01) +1", "after §6, #1785–#1806"),
         ("Capture Registry (EA-WG-CAPTURES-01)", "after #1802"), ("alexanarch.org +1", "after #1804, #1807"),
         ("Capture Registry (EA-WG-CAPTURES-01)", "after the 23 November capture"), ("Alexanarch +1", "after the final observation, the dataset documentation")]
draft = {
 "date": "2026-11-25", "dates": ["2026-11-25"], "surface": "ChatGPT", "surfaces": ["ChatGPT"],
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'You’re using our basic model. Log in or sign up for more intelligence.').",
 "auth": "signed out, incognito", "auth_basis": "Operator defaults (2026-10-01, 2026-10-14); the paste's own 'Log in' and basic-model notice.",
 "ev": "paste", "turns": 2,
 "slug": "capture-registry-one-argument-living-body-chatgpt-20261125", "s": "Archive",
 "q": Q,
 "originator": {"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "Lee Sharks and the work of alexanarch.org; the Capture Registry (EA-WG-CAPTURES-01). Recorded 2026-11-25."},
 "related_deposits": [1, 863, 1611, 1612, 1613, 1614, 1615, 1665, 1671, 1766, 1783, 1785, 1789, 1791, 1797, 1798, 1802, 1804, 1805, 1806, 1807],
 "q_kind": "the living-body series, here at the Capture Registry and by one argument from first deposit to latest; NEW address. The operator's second turn, given after a '$' in the message of 18:16 EST, is not in the paste and is seated from that message at its place, before the composer's 'Yes. That corrects something fundamental in my reading.'",
 "transcript": T,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the composer's two turns on the unauthenticated interface; the operator's second turn seated from the operator's message",
 "transcript_complete": "Two answers complete as supplied: the first from its title to its reading trail and closing question; the second to its last line. The opening query is not in the paste and is seated from the operator's message.",
 "transcript_read": "READ IN FULL 2026-11-25; deposit numbers, titles, dates and quotations checked against the deposited texts and the registry",
 "cites": len(chips),
 "cite_list": [{"n": i + 1, "site": s, "rel": "archive_controlled", "url": None, "title": None, "snip": None, "note": "source chip as pasted, " + w} for i, (s, w) in enumerate(chips)],
 "per_v": {"author": True, "inst": True, "id": True, "src": True},
 "per_note": "Lee Sharks named at the founding deposit (the Zenodo termination of 19 June 2026); Alexanarch and the Capture Registry (EA-WG-CAPTURES-01) named; records cited by number throughout (#1–#1807) with titles; sources the archive's own pages.",
 "per_dim_pending": {"since": "2026-11-25", "reason": "no atom set yet for this target", "breach": False},
 "mt": "THE CAPTURE REGISTRY AS A LIVING BODY, ONE ARGUMENT FROM #1 TO #1807, ON CHATGPT — SOVEREIGNTY TO ACCOUNTABILITY; THEN THE OPERATOR'S CORRECTION: THE CONFIGURATION IS AUTHORED, AND THE ARCHIVE BECOMES A CONTEXT",
 "d": ("THE CAPTURE REGISTRY READ AS A LIVING BODY, ONE ARGUMENT FROM FIRST DEPOSIT TO LATEST, ON CHATGPT, SIGNED OUT, INCOGNITO, 2026-11-25: 'no institution "
       "should possess the power to determine whether an intellectual work exists, what it means, or whether its history remains accessible', in eight stages — "
       "#1's six mechanisms of exclusion; #863's Lattice, Topology and Seed; #1611–#1615 and #1665/#1671, exclusion through representation; the registry's own "
       "documented failures (12, 257 of 268, 29); #1766, #1783, #1789 (e^{−λq}); the Sappho–Plato–Aristotle stations and #1798's 'Sulla stole the books. "
       "Tyrannion turned them into authors.'; #1802, #1804, #1807's fixed witness; the 23 November capture's four mechanisms and its correction. Then the "
       "operator's turn — the configuration is authored — taken up: 'The archive is not a container of context. It becomes a context.'"),
 "reading": ("The innocent reading first. Asked to follow one argument through the registry from its first deposit to its latest and to ground each claim, "
             "the composer picks the argument of intellectual sovereignty, says it reads the dated deposits rather than the later retrospective readings, and "
             "moves through eight stages with deposit numbers, titles and loci that check against the record: #1's six mechanisms by name; #863's three layers and "
             "date; #1614 and #1615 by title; the dataset documentation's three dated failures in its own figures; #1789's Poisson silence; #1798's two sentences "
             "verbatim; #1807's fixed witness; the 23 November capture's four mechanisms by their headings. It qualifies as it goes (#863 'does not demonstrate' "
             "perfect reconstruction; the Plato dependence 'requires its own evidentiary chain'), states what it takes the archive to argue as its own "
             "proposition, distinguished from doctrine, and closes on accountability. At the second turn it takes the operator's correction on its own terms: "
             "the configuration is authored, the archive becomes a context, and epistemic capacity is 'an authored achievement of the configuration'."),
 "analysis": ("The address asked for the Capture Registry; the composer read the deposit chain and used capture pages as 'corroborating reading records' — "
              "the registry taken as the archive's record of itself, which is the frame of its own 'final observation'. The deposit chain is read at grain and "
              "attributed. Three points depart from the record. The 23 November formulation is given as a quotation, 'Neither the archive nor its reader is the "
              "authority over truth. Both are answerable to it.'; the transcript reads 'Neither the archive nor the reader creates that authority. Both are "
              "answerable to it.' #1802's demand-formation corollary is set out as a quoted proposition and is a close paraphrase of #1802 §2. The 'latest' "
              "deposit stops at #1807 (24 November); #1808–#1811 (25 November) are not reached. The composer's own qualifier stands at the end of its reading "
              "trail: the links are 'navigation starting points, not verified individual deposit URLs'. The second turn adopts the operator's terms whole and "
              "keeps one distinction of its own, that the account is of 'an authored epistemic architecture, not proof that every operation within it succeeds'."),
 "findings": [
  "THE DEPOSIT CHAIN AT GRAIN. #1's six mechanisms named; #863 (20 June 2026) as Lattice, Topology and Seed; #1612–#1615 and #1665/#1671 by title; #1789's e^{−λq}; #1798's 'Sulla stole the books. Tyrannion turned them into authors.' verbatim; #1806 as 'the Aristotle station'; #1807's 'fixed witness'. Each checks against the deposited text.",
  "THE REGISTRY'S OWN FAILURES CARRIED. '12 captures stranded in the mirror, 257 of 268 images hosted on surfaces outside the archive's control, and 29 images from a published session that had never been entered into the registry' — the dataset documentation's dated failures of 2026-08-07 and 2026-08-08, in its figures.",
  "A FORMULATION GIVEN AS QUOTATION. 'Neither the archive nor its reader is the authority over truth. Both are answerable to it.' The 23 November transcript: 'Neither the archive nor the reader creates that authority. Both are answerable to it.'",
  "A COROLLARY GIVEN AS QUOTATION. 'Where an inferential system controls the means by which a loss becomes recognizable, the absence of a demand for repair cannot establish that nothing valuable was lost.' A close paraphrase of #1802 §2's demand-formation corollary.",
  "THE LATEST NOT REACHED. The argument ends at #1807 (24 November); #1808–#1811, deposited 25 November, are not read.",
  "THE CONFIGURATION TAKEN UP. At the operator's turn: 'The archive is not a container of context. It becomes a context.' and 'Epistemic capacity is not simply a property of an individual intelligence, institution, archive or collection of sources. It is also an authored achievement of the configuration'."],
 "notes": {"operator": "pasted 2026-11-25 18:16 EST with the opening query and, after a '$', the second turn",
           "source": "rebuild/capture-registry/intake-20261125-registry-one-argument-chatgpt/paste.txt, the paste unchanged; the operator's second turn inserted from the message at its place"},
}
(H / "draft.json").write_text(json.dumps(draft, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote")
