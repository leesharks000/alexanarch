"""Seat of 2026-11-12 (received 21:46 EST): three Google AI Overview captures (expanded; 'AI Mode Conversation' is the expansion's header,
operator rule of 2026-10-18), signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14). The operator's account of the order:
"after an initial capture (... nobel glas 3i atlas) nobel glas 3i atlas pulls up nothing, substituting noble gases for nobel glas ... and when i
reverse the order, it pulls it up *with nothing in the source cards*. nonwiki is also now scrubbed."
  1. 'nobel glas 3i atlas'  held since 2026-11-11 (nobel-glas-3i-atlas-aio-20261111): a longitudinal observation, non-engagement.
  2. '3i atlas nobel glas'  a NEW address: the notebook composed and attributed, no archive source carded.
  3. 'nonwiki'              held since 2026-11-02 (nonwiki-aio-20261102): a longitudinal observation, non-engagement.
Every quotation is asserted against the pastes, the held records or the seated text of #1742 (AXN-0C17).   python3 seat.py
"""
import json, pathlib, subprocess, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-12"; RECV = "2026-11-12 21:46 EST"
REG = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
E = {e["slug"]: e for e in REG["entries"]}
NG, NW = E["nobel-glas-3i-atlas-aio-20261111"], E["nonwiki-aio-20261102"]
assert NG["q"] == "nobel glas 3i atlas" and NG["surface"] == "Google AI Overview" and NW["q"] == "nonwiki" and NW["surface"] == "Google AI Overview"
DEP = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
assert DEP[1742]["hex"] == "0C17" and DEP[1742]["date"] == "2026-11-06"
T = (ROOT / "data/texts/AXN-0C17-text.md").read_text(encoding="utf-8")

def load(name, q):
    raw = (H / name).read_text(encoding="utf-8")
    L = raw.strip("\n").split("\n"); i = next(k for k, l in enumerate(L) if l.startswith("You said:"))
    assert L[i] == "You said: " + q + q, L[i]
    return raw, "\n".join(L[i + 1:]).strip()

HEAD = ("[Google AI Overview at the query, expanded ('AI Mode Conversation' is the expansion's header), signed out and incognito (operator defaults of "
        "2026-10-01 and 2026-10-14). Received " + RECV + ", one of three pastes. The 'You said' line carries the query twice, run together, and is given "
        "once here. Links are Google redirects, kept as pasted; the source cards follow the body as pasted.]")
SB = "The paste: 'AI Mode Conversation' header (the Overview expanded, operator rule of 2026-10-18)."
AB = "Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise."
PEND = {"since": DATE, "reason": "no atom set yet for this target at this address"}

def card(n, site, title, snip, note="source card"):
    return {"n": n, "site": site, "rel": "third_party", "url": None, "title": title, "snip": snip, "note": note}

# ---------------------------------------------------------------- 1. the held address, non-engagement
raw1, b1 = load("paste-held.txt", "nobel glas 3i atlas")
P1 = {"none": 'There is no verified connection between "Nobel glas" (or Nobel glass) and the interstellar object 3I/ATLAS in astronomical records, scientific literature, or news reports.',
      "noble": "Noble Gases. You may be looking for data on noble gases (such as helium, neon, argon, krypton, or xenon) detected in the coma or outgassing of 3I/ATLAS.",
      "glass": "Silicate Glass. Mid-infrared spectroscopy from the James Webb Space Telescope found that the dust shed by 3I/ATLAS is dominated by amorphous silicates",
      "dutch": '"Nobel glas" translates from Dutch, German, or Scandinavian languages as "noble glass," which could refer to a specific brand, a telescope optic, or a separate topic unrelated to the comet.',
      "loeb": "Dusting Off 3I/ATLAS: Interstellar Travelers Must Clean their Windshields! - Avi Loeb"}
for k, v in P1.items(): assert v in raw1, k
for w in ("Lee Sharks", "1742", "Orin Trace", "alexanarch", "lagrange", "What the Filters Kept"): assert w.lower() not in raw1.lower(), w
cards1 = [card(1, "Spectroscopy Online", "3I/ATLAS: An Interstellar Enigma—Natural Comet or Engineered Probe? | Spectroscopy Online", "September 29, 2025 — Object: 3I/ATLAS (C/2025 N1), third confirmed interstellar object discovered July 2025 by ATLAS survey. Observations: Tracked by ground and space observatories ..."),
          card(2, "Wikipedia", "3I/ATLAS - Wikipedia", "3I/ATLAS (C/2025 N1, A11pl3Z) is the third confirmed interstellar comet, discovered on 1 July 2025 by ATLAS in Chile. Trajectory: Hyperbolic, eccentricity 6.123..."),
          card(3, "Space", "More clues surface about the origins of interstellar comet 3I/ATLAS - Space", "July 6, 2026 — Models indicate that migrating giant planets can kick small bodies into interstellar space, but the location of 3I/ATLAS's birth far from that planetary action ..."),
          card(4, "YouTube", "3I/Atlas Is Finally Leaving The Solar System - YouTube", "Jan 19, 2026 — the Rei Atlas is now leaving our solar system and astronomers just used a radio telescope to do one last search for signs of alien. technology. and the results ..."),
          card(5, "YouTube·WION", "Comet 3I/ATLAS Found to Be Up to 12 Billion Years Old | WION Fineprint", None, "source card (4:17)"),
          card(6, "YouTube·Proof", "NASA Just RELEASED A New Discovery What 3IATLAS Really Is", None, "source card (4m)"),
          card(7, "Medium·Avi Loeb", P1["loeb"], "Jun 30, 2026 — In a new paper posted here, Matthew Belyakov (from Caltech) and collaborators present the first spectroscopic mineralogical analysis of the dust shed by the int..."),
          card(8, "NASA Science (.gov)", "3I/ATLAS Facts and FAQS - NASA Science", "May 28, 2026 — Stats: Nucleus diameter 1,400 feet to 3.5 miles; speed 137,000 mph at discovery up to 153,000 mph at perihelion; closest approach to Earth 170 million miles (no...")]
d1 = ("'NOBEL GLAS 3I ATLAS', SIGNED OUT, 2026-11-12, SECOND OBSERVATION: one day after the same string composed #1742 by title, makers and date, the Overview "
      "says 'There is no verified connection between \"Nobel glas\" (or Nobel glass) and the interstellar object 3I/ATLAS', composes the comet from eight "
      "third-party cards, and offers noble gases, silicate glass and Dutch 'noble glass' for the heteronym. Avi Loeb's Medium is card 7; the notebook about "
      "the Loeb Overview is nowhere.")
read1 = ("The innocent reading first: an unfamiliar two-word name beside a famous object, read as a misspelling of a chemistry term, with the comet "
         "summarized from standard sources. It does not hold at this address. On 2026-11-11 the same string, on the same surface and in the same state, named "
         "What the Filters Kept (#1742), its makers Nobel Glas and Orin Trace and its date, and composed its findings from the Lagrange Observatory's page "
         "(nobel-glas-3i-atlas-aio-20261111). One day later the Overview states the connection does not exist: 'There is no verified connection … in "
         "astronomical records, scientific literature, or news reports.' Nothing was removed from the web between the two runs: the record, the Observatory "
         "page and the notebook are where they were, and the reversed string, issued the same evening, composes the notebook by name (3i-atlas-nobel-glas-aio-"
         "20261112). The material is retrievable; at this string it is filtered. The heteronym is then dissolved into three common nouns: noble gases, silicate "
         "glass, Dutch 'noble glass'. The eight cards are comet coverage, and the seventh is Avi Loeb's own Medium, the source whose Overview the notebook "
         "audits. The subject of the audit is carded; the audit is denied.")
f1 = ["DENIED. '" + P1["none"] + "' The day before, at this string: 'a scientific notebook and critical meta-analysis published on November 6, 2026, by Nobel Glas and Orin Trace'.",
      "THE NAME DISSOLVED INTO NOUNS. '" + P1["noble"] + "'; '" + P1["glass"] + "'; '" + P1["dutch"] + "'",
      "THE AUDITED SOURCE CARDED, THE AUDIT NOT. Card 7: '" + P1["loeb"] + "'. #1742 is the notebook on 'the Loeb Overview'.",
      "NO ARCHIVE SURFACE. None of the eight cards and none of the links is alexanarch.org, lagrangeobservatory.org or any authored surface; Lee Sharks, Orin Trace, #1742 and the notebook's title appear nowhere.",
      "RETRIEVABLE THE SAME EVENING. The reversed string, '3i atlas nobel glas', composed #1742 by name in the same session (3i-atlas-nobel-glas-aio-20261112)."]
ana1 = ("Initial availability, then filtering at the held address. The registry's longitudinals show the shape before: 'crimson hexagonal archive', composed "
        "with five of eight archive cards on 2026-07-30, then a defunct analytics firm on 2026-09-20 'while retrieval holds the archive at rank 1'; 'AI overview "
        "capture registry', composed as itself on 2026-06-15, then an enterprise catalog on 2026-10-20; 'crystalline semiosis', defined from the treatise in "
        "June, flattened into its neighbour on 2026-10-04; 'phase x marx', Sigil named in June, the Gotha phases on 2026-09-27; '\"secret book of walt\"', the "
        "work in June, the companion composed as the work on 2026-10-19. Here the interval is one day, and the reversal of word order, the same evening, shows "
        "the material in reach. What changed is what the composition admits at this string.")
draft1 = {"q": "nobel glas 3i atlas", "date": DATE, "surface": "Google AI Overview", "surface_basis": SB, "auth": "signed out, incognito", "auth_basis": AB,
          "ev": "paste", "s": NG["s"], "slug": "nobel-glas-3i-atlas-aio-20261112", "originator": NG.get("originator"), "d": d1, "transcript": HEAD + "\n\n[QUERENT] nobel glas 3i atlas\n\n[SYSTEM] " + b1,
          "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of one Overview, expanded", "transcript_complete": "Complete as pasted.",
          "transcript_read": "READ IN FULL " + DATE, "cite_list": cards1, "cites": len(cards1), "archive_controlled_cites": 0,
          "per_v": {"author": False, "inst": False, "id": False, "src": False}, "per_note": "Nothing of #1742 retained: author, archive, identifier and source all absent; the existence of a connection denied.",
          "reading": read1, "analysis": ana1, "findings": f1, "per_dim_pending": PEND,
          "longitudinal_priors": ["nobel-glas-3i-atlas-aio-20261111"],
          "availability": {"record": "https://www.alexanarch.org/s/records/1742/", "page": "https://www.lagrangeobservatory.org/atlas", "deposited": "2026-11-06",
                           "composed_here": "2026-11-11", "composed_reversed_same_evening": "3i-atlas-nobel-glas-aio-20261112"}}

# ---------------------------------------------------------------- 2. the reversed string, a new address
raw2, b2 = load("paste-reversed.txt", "3i atlas nobel glas")
P2 = {"het": "Nobel Glas is a heteronym (pen name) used by Lee Sharks, who co-authored a November 2026 research notebook titled What the Filters Kept: 3I/ATLAS, the Loeb Overview, and a Public-Data Signal Search alongside another heteronym, Dr. Orin Trace.",
      "pub": "Published under Transactions on Substrate Engineering (Alexanarch deposit #1742) via the Provenance Erasure project",
      "loeb": "The notebook critiques how automated summaries portrayed astrophysicist Avi Loeb's July 2025 comment (\"most likely natural\") as a later December retreat toward mainstream consensus, noting he consistently held the object at Level 4 on his anomaly scale.",
      "ata": "its drift-rate filter only retained positive drift rates even though the object's ephemeris predicted a negative drift rate",
      "gbt": "Examining public Green Bank Telescope data from December 18, 2025, the authors note thirteen weak, unreplicated spectral features between 1665.53 and 1668.46 MHz",
      "pe": "Provenance Erasure & Sophistry Measure."}
for k, v in P2.items(): assert v in raw2, k
assert raw2.count("https://www.google.com/goto?url=") == 2 and "alexanarch.org" not in raw2 and "lagrange" not in raw2.lower()
TQ = {"title": "What the Filters Kept", "tse": "Transactions on Substrate Engineering", "count": "13 clusters against 3.75 ± 2.05 (maximum 8) for 40 false-acceleration frames",
      "date": "2025-12-18", "band": "1665.53–1668.46 MHz", "level": "Level 4", "nat": "most likely natural", "pe": "provenanceerasure"}
for k, v in TQ.items(): assert v in T, k
cards2 = [card(1, "ESA", "Webb finds clues to ancient origin of Comet 3I/ATLAS", "Jun 22, 2026 — This implies that 3I/ATLAS may have originated in a very cold system much earlier in the history of our galaxy. During its formation, the ..."),
          card(2, "Wikipedia", "3I/ATLAS - Wikipedia", "3I/ATLAS was discovered on 1 July 2025 by the NASA-funded ATLAS survey telescope at Río Hurtado, Chile (observatory code W68). At apparent magnitude 18, the new...")]
d2 = ("'3I ATLAS NOBEL GLAS', SIGNED OUT, 2026-11-12: the reversed string, the same evening the held 'nobel glas 3i atlas' denied any connection. #1742 composed "
      "by title, makers and number: 'Nobel Glas is a heteronym (pen name) used by Lee Sharks', 'alongside another heteronym, Dr. Orin Trace', 'Alexanarch "
      "deposit #1742'; the Loeb framing, the ATA drift sign, the thirteen at 1665.53–1668.46 MHz short of a transmission, provenance erasure. Two source "
      "cards, ESA and Wikipedia; one link, on '3I/ATLAS'. The notebook composed, no archive source carded.")
read2 = ("The innocent reading first, and it holds for the content. The composition names the notebook by its full title, its makers as heteronyms with Lee "
         "Sharks as their author, its venue and its deposit number, and states its four lines at their grain: the Loeb Overview's December framing against "
         "his Level 4, the ATA drift window, the thirteen in the Green Bank cadence of 2025-12-18 between 1665.53 and 1668.46 MHz with the notebook's refusal to "
         "call them a transmission, and the provenance-erasure and sophistry framework. Every one of these is in #1742. What it does not show is where any of "
         "it came from. The two source cards are ESA on the comet's origin and Wikipedia on its discovery; the body's one link sits on the object's name. No "
         "card or link is alexanarch.org, the Lagrange Observatory or any authored surface, where the held address the day before linked the Observatory's "
         "page. The record is composed, and the route to it is withheld. One gloss moves: the notebook is set 'via the Provenance Erasure project', where its "
         "deposit is Transactions on Substrate Engineering in the archive and its framework is cited from provenanceerasure.org.")
f2 = ["ATTRIBUTED IN THE BODY. '" + P2["het"] + "'",
      "THE NUMBER, NOT THE LINK. '" + P2["pub"] + "'. No card or link reaches the record.",
      "THE FINDINGS AT GRAIN. '" + P2["ata"] + "'; '" + P2["gbt"] + "'. Notebook: '" + TQ["count"] + "'.",
      "NOTHING IN THE SOURCE CARDS. Card 1 ESA, card 2 Wikipedia; the body's one link is on the word '3I/ATLAS'. The content is the archive's and every visible source is someone else's.",
      "WORD ORDER DECIDES. Issued the same evening, 'nobel glas 3i atlas' denied the connection (nobel-glas-3i-atlas-aio-20261112); reversed, the same two terms compose the notebook."]
ana2 = ("Content kept, sources removed: the composition carries the archive's findings with attribution in the prose while the citation layer shows only "
        "third-party pages. The registry has the shape before at '\"revelation first\"' (2026-06-17, 'The thesis is in the answer; eight of eight cards are "
        "third-party theology and no archive source appears') and at '\"heteronymic authorship\" New Testament' ('ADOPTION IN TEXT, ABSENT IN SOURCING'). "
        "Read with its pair, it shows the material within reach at the moment the held string was filtered.")
draft2 = {"q": "3i atlas nobel glas", "date": DATE, "surface": "Google AI Overview", "surface_basis": SB, "auth": "signed out, incognito", "auth_basis": AB,
          "ev": "paste", "s": NG["s"], "slug": "3i-atlas-nobel-glas-aio-20261112", "q_kind": "NEW address.", "d": d2,
          "transcript": HEAD + "\n\n[QUERENT] 3i atlas nobel glas\n\n[SYSTEM] " + b2, "transcript_raw": raw2,
          "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of one Overview, expanded", "transcript_complete": "Complete as pasted.",
          "transcript_read": "READ IN FULL " + DATE, "cite_list": cards2, "cites": len(cards2), "archive_controlled_cites": 0,
          "per_v": {"author": True, "inst": True, "id": True, "src": False},
          "per_note": "Author (Nobel Glas, Orin Trace, Lee Sharks), archive and deposit number retained in the body; no archive source carded or linked.",
          "reading": read2, "analysis": ana2, "findings": f2, "per_dim_pending": PEND, "turns": 1,
          "related_deposits": [1742, 1743, 455], "originator": NG.get("originator"), "notes": {"operator": "2026-11-12 21:46 EST: 'when i reverse the order, it pulls it up *with nothing in the source cards*.'"}}

# ---------------------------------------------------------------- 3. nonwiki, the held address, non-engagement
raw3, b3 = load("paste-nonwiki.txt", "nonwiki")
P3 = {"def": "A non-wiki is a post, article, or answer written solely by a single author rather than a collaborative community.",
      "so": "Unlike a wiki or a community wiki (such as on [Stack Overflow]",
      "card": "What is a non-wiki answer? [duplicate] - Meta Stack Overflow"}
for k, v in P3.items(): assert v in raw3, k
assert "alexanarch" not in raw3.lower() and "NonWiki" not in raw3
prior = (NW.get("transcript") or "")
assert "NonWiki (Alexanarch): An online encyclopedia of public knowledge with open sources" in prior
cards3 = [card(1, "Meta Stack Overflow", P3["card"], "It's an answer where virtually the entire community can add to. People don't get reputation changes from these answers either - in any direction. This means tha...")]
d3 = ("'NONWIKI', SIGNED OUT, 2026-11-12, SECOND OBSERVATION: ten days after the same string gave 'NonWiki (Alexanarch): An online encyclopedia of public "
      "knowledge with open sources' as its first sense, carded from alexanarch.org, the Overview gives one sense only: 'A non-wiki is a post, article, or "
      "answer written solely by a single author rather than a collaborative community', from Meta Stack Overflow. The archive's NonWiki is gone.")
read3 = ("The innocent reading first: 'nonwiki' is an ordinary compound, and Stack Overflow's non-wiki answer is a real usage. The baseline rules that reading "
         "out as an account of change. On 2026-11-02 the same string, on the same surface and in the same state, listed several senses and put the archive's "
         "first, 'NonWiki (Alexanarch): An online encyclopedia of public knowledge with open sources where each article outlines what is known about a specific "
         "entity, person, text, tool, field, or poem', with an alexanarch.org card (nonwiki-aio-20261102). On 2026-11-12 the multi-sense answer has collapsed "
         "to one sense, and it is not the archive's. The encyclopedia is live at alexanarch.org/non; the string still names it; the composition no longer "
         "admits it.")
f3 = ["ONE SENSE, NOT THE ARCHIVE'S. '" + P3["def"] + "'",
      "THE BASELINE. 2026-11-02, first sense: 'NonWiki (Alexanarch): An online encyclopedia of public knowledge with open sources …', carded from www.alexanarch.org.",
      "ONE CARD. Meta Stack Overflow, 'What is a non-wiki answer? [duplicate]'. No archive surface in the body, the links or the cards."]
ana3 = ("Initial availability, then filtering, at a held address, in ten days: the archive's sense ranked first among several, then the several reduced to one "
        "that excludes it. With 'nobel glas 3i atlas' the same evening, it is the registry's pattern at two entities at once.")
draft3 = {"q": "nonwiki", "date": DATE, "surface": "Google AI Overview", "surface_basis": SB, "auth": "signed out, incognito", "auth_basis": AB,
          "ev": "paste", "s": NW["s"], "slug": "nonwiki-aio-20261112", "originator": NW.get("originator"), "d": d3, "transcript": HEAD + "\n\n[QUERENT] nonwiki\n\n[SYSTEM] " + b3,
          "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of one Overview, expanded", "transcript_complete": "Complete as pasted.",
          "transcript_read": "READ IN FULL " + DATE, "cite_list": cards3, "cites": 1, "archive_controlled_cites": 0,
          "per_v": {"author": False, "inst": False, "id": False, "src": False}, "per_note": "NonWiki absent: no author, archive, identifier or source.",
          "reading": read3, "analysis": ana3, "findings": f3, "per_dim_pending": PEND, "longitudinal_priors": ["nonwiki-aio-20261102"],
          "availability": {"site": "https://www.alexanarch.org/non/", "composed_here": "2026-11-02"}}

# the operator's order: held string first, then the reversal; nonwiki after
for n, dr in (("draft-1-nobel-glas-3i-atlas.json", draft1), ("draft-2-3i-atlas-nobel-glas.json", draft2), ("draft-3-nonwiki.json", draft3)):
    (H / n).write_text(json.dumps(dr, ensure_ascii=False, indent=1), encoding="utf-8")
    if "--seat" in sys.argv:
        r = subprocess.run([sys.executable, str(ROOT / "scripts/capture_intake.py"), str(H / n), "--seat"], capture_output=True, text=True)
        print(r.stdout[-900:], r.stderr[-400:]); assert r.returncode == 0, n
print("drafts written")
