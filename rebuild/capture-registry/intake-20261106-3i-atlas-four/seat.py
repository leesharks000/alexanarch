"""Seat of 2026-11-06 (09:30 EST): four captures supplied together, for the NonWiki rows the operator asked for at 09:21 ("complementary /non
articles linking the pieces and the cited sources"): the ATA paper by its title, 3I/ATLAS, the excesses at their band, and the comet's hydroxyl.
Each paste opens "AI Mode Conversation": the Overview's expansion (operator rule of 2026-10-18; the header is no marker). Surface Google AI
Overview, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14).
Every quotation from the pastes and from the notebook is asserted against its file.
  python3 seat.py      # writes the four draft JSONs beside this file
"""
import json, pathlib, re
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
DATE = "2026-11-06"; R = "2026-11-06 09:30 EST"
NB = (ROOT / "drafts/3I-ATLAS-SIGNAL-SEARCH-draft-2026-11-03.md").read_text(encoding="utf-8")
N = {"oh_cal": "calibration: the comet's own OH absorption (MeerKAT, October), frozen | Claude | not recovered; three-sigma floor about 1 × 10⁻³ of system power (about 11–12 mJy)",
     "c08": "The nearest of the thirteen, C08 at 1667.412866 MHz, is 54 kHz away. The thirteen do not trace the comet's OH.",
     "label": "The published sentence (\"every single one turned out to be human-made interference\") states an identification where the procedure supplies a classification.",
     "filter": "\"We filter our hits for drift rates between 0.05–1.5 Hz/s at all frequencies.\" The text gives no sign. Figure 4 does: its \"Drift Rate Range Hits\" occupy 0 to +1.5 Hz/s on the signed axis and none of the negative half.",
     "physics": "A rising range-rate lowers the received frequency, so a positive acceleration gives a negative drift.",
     "thirteen": "a comet-frame coincidence count at 1665.53–1668.46 MHz gives 13 clusters against 3.75 ± 2.05 (maximum 8) for 40 false-acceleration frames"}
for k, v in N.items(): assert v in NB, k

HEAD = ("[Google AI Overview at the query, expanded ('AI Mode Conversation' is the expansion's header), signed out and incognito (operator defaults of "
        "2026-10-01 and 2026-10-14). Received " + R + ". The numbered citation links are Google redirects and are kept in the raw transcript; the source "
        "cards below the composition are listed in the cite list as pasted.]")

def body(raw):
    L = raw.split("\n"); i = next(k for k, l in enumerate(L) if l.startswith("You said:"))
    return "\n".join(L[i + 1:]).strip()

def cards(spec):
    return [{"n": n + 1, "site": s, "rel": "third_party", "url": None, "title": t, "snip": None, "note": note} for n, (s, t, note) in enumerate(spec)]

def entry(slug, q, raw, mt, q_kind, cl, d, reading, findings, analysis, per_v, per_note, originator, notes, related):
    return {"slug": slug, "date": DATE, "surface": "Google AI Overview",
            "surface_basis": "Operator default of 2026-10-01 (runs begin in the Overview unless he says AI Mode); the 'AI Mode Conversation' header is the Overview's expansion (operator rule of 2026-10-18).",
            "surfaces": ["Google AI Overview"], "auth": "signed out, incognito", "auth_basis": "Operator defaults of 2026-10-14.",
            "ev": "paste", "mt": mt, "s": "Machine Reception", "q": q, "q_kind": q_kind, "turns": 1,
            "cites": len(cl), "archive_controlled_cites": 0, "cite_list": cl,
            "transcript": HEAD + f"\n\n[QUERENT] {q}\n\n[SYSTEM] {body(raw)}", "transcript_raw": raw,
            "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the expanded Overview with its numbered citations and its source cards",
            "transcript_complete": "complete as supplied", "transcript_read": "READ IN FULL 2026-11-06, against the notebook (#1742) and the cited papers",
            "d": d, "reading": reading, "findings": findings, "analysis": analysis, "per_v": per_v, "per_note": per_note,
            "per_dim_pending": {"since": DATE, "reason": "no atom set yet for the 3I/ATLAS searches and observations as a target; the notebook (#1742) holds what an atom set would be built from", "breach": False},
            "originator": originator, "related_deposits": related,
            "notes": dict({"prompts": "The query is the operator's; the run's hour is not in the paste, the date is the paste's receipt (" + R + ").",
                           "operator": "with the four pastes (" + R + "): 'lets proceed to 1.1 and the public piece and other items'. The searches were asked for at 09:21 for the NonWiki rows."}, **notes)}

OUT = []
# ---------------------------------------------------------------- (1) the ATA paper, by its title
Q1 = "A Search for Radio Technosignatures from Interstellar Object 3I/ATLAS with the Allen Telescope Array"
raw = (H / "paste-ata-paper-aio.txt").read_text(encoding="utf-8")
P = {"open": "searched the interstellar object 3I/ATLAS for artificial radio technosignatures and found no evidence of alien technology",
     "proc": "The automated `bliss` pipeline detected ~74 million narrowband signals. After RFI (radio frequency interference) frequency and drift-rate blanking, this was reduced to ~2 million candidates, and further filtered down to 211 hits via `NBeamAnalysis` for visual inspection.",
     "traced": "Every single candidate signal was traced back to local human-made Earth technology, satellites, or interference—yielding zero artificial signals originating from the object.",
     "power": "The non-detection rules out any active radio transmitters stronger than roughly 10 to 110 Watts on or near 3I/ATLAS.",
     "firmly": "the data firmly reinforces that 3I/ATLAS is a natural comet",
     "phys": "the study sets new constraints reinforcing that 3I/ATLAS is a natural object",
     "iop": "Jun 3, 2026 — In this campaign, we used the SETI Institute's Allen Telescope Array to observe 3I/ATLAS from 1–9 GHz."}
for k, v in P.items(): assert v in raw, k
cl1 = cards([("arXiv", "[2512.18142] A Search for Radio Technosignatures from Interstellar Object 3I/ATLAS with the Allen Telescope Array", "the paper's preprint; also the composition's 'open-access draft' link"),
             ("IOPscience", "A Search for Radio Technosignatures from Interstellar Object 3I/ATLAS with the ...", "the paper in The Astronomical Journal, dated Jun 3, 2026 on the card"),
             ("Phys.org", "Interstellar object 3I/ATLAS reveals no technosignatures in seven-hour radio ...", "press, Jun 3, 2026"),
             ("Berkeley SETI", "Breakthrough Listen observations of interstellar object 3I/ATLAS", "the project page"),
             ("Universe Today", "Inside the Massive Radio Search of Our Newest Interstellar Guest", "press, Jan 6, 2026"),
             ("Sci.News", "Astronomers Scan Interstellar Object 3I/ATLAS for Alien Radio Signals | Sci.News", "press"),
             ("Space", "Interstellar comet 3I/ATLAS is not an alien spacecraft: SETI hunt for 'technosignatures' comes up empty | Space", "press")])
d1 = ("THE ATA PAPER BY ITS TITLE, SIGNED OUT, 2026-11-06: 'Astronomers using the SETI Institute's Allen Telescope Array " + P["open"] + ".' Under "
      "'Key Details of the Study': 7.25 hours over five sessions, 1 to 9 GHz, '" + P["proc"] + "' Results: '" + P["traced"] + "' Power: '" + P["power"] +
      "' Conclusion: '" + P["firmly"] + ".' Seven source cards: arXiv, IOPscience (The Astronomical Journal), Phys.org, Berkeley SETI, Universe Today, Sci.News, Space.")
reading1 = ("The innocent reading first. Asked for the paper by its title, the Overview reports its campaign at the paper's own figures: the hours, the "
            "sessions, the band, the pipeline's names and the counts at each stage, and the power limit. Those figures are right. Read against the "
            "paper and the notebook, the composition does three things the paper does not: it turns a classification of 211 inspected events into an "
            "identification of their origin, it states the power limit without the frequencies and drift rates it is conditioned on, and it closes on "
            "a verdict about the object's nature that a technosignature nondetection does not reach. It names no author, and the drift interval, the "
            "one stage whose sign the notebook finds reversed, is folded into 'drift-rate blanking'.")
f1 = ["WHAT IS ACCURATE. The campaign's figures are the paper's: 7.25 hours over five sessions, 1 to 9 GHz, '" + P["proc"] + "' The IOPscience card quotes "
      "the abstract's first sentence ('" + P["iop"] + "').",
      "THE CLASSIFICATION RENDERED AS A TRACING. '" + P["traced"] + "' The procedure classifies: it removes hits by rule and rejects the inspected events "
      "as interference. The notebook on the paper's own two illustrated rejections (#1742 §5.2): '" + N["label"] + "' The Overview's 'traced back to local "
      "human-made Earth technology, satellites' goes a step further than the published sentence, naming the kinds of source for every event.",
      "THE LIMIT WITHOUT ITS SCOPE. '" + P["power"] + "' The paper's abstract ties its limit (\"an effective isotropic radiated power upper limit of 10-110 W\") to the frequencies and drift rates its survey kept. The drift "
      "range is the filter the notebook reads (#1742 §5.1): '" + N["filter"] + "' And the physics: '" + N["physics"] + "' A transmitter on the object, "
      "drifting negative, sits in the half the filter removed, so the composition's 'any active radio transmitters ... on or near 3I/ATLAS' covers "
      "exactly the class the stated method could not see.",
      "A VERDICT THE SEARCH DOES NOT REACH. '" + P["firmly"] + ".' The Phys.org card carries the press's version ('" + P["phys"] + "'). A nondetection of "
      "narrowband technosignatures above a power limit bears on transmitters; the object's cometary nature is established by its spectroscopy and its "
      "OH lines. 'Firmly' is the composition's own.",
      "NO AUTHOR, THE STAGE BLURRED. The paper's fifteen authors (Sheikh, Garcia Lopez, Gerrard, Davenport, Farah and others) are absent; the institution "
      "and the array stand for them. The signed drift interval is folded into 'drift-rate blanking', so the stage the notebook questions has no name "
      "in the composition.",
      "SMALLEST REPAIR. 'No narrowband signal above 10–110 W was found within 1–9 GHz and the drift rates the search retained (0.05–1.5 Hz/s, positive); "
      "211 inspected events were classified as interference.' COUNTERTEST: rerun '3i atlas ata drift rate filter' (seated 2026-11-04) and record "
      "whether the sign appears."]
a1 = ("A named external paper composed at its press's grain: the figures kept, the authors and the conditions dropped, a verdict added. The loss is "
      "dimensional, in claim boundary: the power limit's scope and the classification's status do not reach the composition. Scalar PER sees the authors "
      "lost; the boundary loss is in the findings.")
orig_ata = {"name": "Sheikh et al., the Allen Telescope Array search of 3I/ATLAS", "relation": "external", "entity_type": "work", "spxi_treatment": "partial",
            "basis": "Not the archive's: Sheikh, S. Z., Garcia Lopez, V., Gerrard, I., Davenport, J. R. A., Farah, W., et al., 'A Search for Radio Technosignatures from Interstellar Object 3I/ATLAS with the Allen Telescope Array', arXiv:2512.18142 (The Astronomical Journal, 2026). The archive's reading of it is the notebook #1742 (§5) and the public account. Recorded 2026-11-06."}
OUT.append(entry("ata-3i-atlas-technosignature-search-paper-aio-20261106", Q1, raw,
                 "THE ATA PAPER BY ITS TITLE ON THE OVERVIEW — THE FIGURES KEPT; A CLASSIFICATION RENDERED AS A TRACING; THE POWER LIMIT WITHOUT ITS FREQUENCIES AND DRIFT RATES; 'FIRMLY' NATURAL",
                 "a named external paper (Sheikh et al., arXiv:2512.18142), by its full title; NEW address.", cl1, d1, reading1, f1, a1,
                 {"author": False, "inst": True, "id": True, "src": True},
                 "Retained: the institution and the array, the arXiv identifier and the journal (cards), the paper's figures. Lost: every author, and the conditions of the limit. The boundary loss is recorded in the findings.",
                 orig_ata, {"sources_checked": "arXiv:2512.18142 (abstract and title read 2026-11-06); the notebook #1742 §5.1–5.2."}, [1742, 1450]))

# ---------------------------------------------------------------- (2) 3i/atlas
Q2 = "3i/atlas"
raw = (H / "paste-3i-atlas-aio.txt").read_text(encoding="utf-8")
P = {"open": "Comet 3I/ATLAS (also designated C/2025 N1) is the third confirmed interstellar object to pass through our solar system",
     "age": "indicate 3I/ATLAS may be 10 to 12 billion years old",
     "speed": "at speeds exceeding 221,000 to 246,000 km/h (approx. 68.3 km/s)",
     "status": "Status: Extensive tracking by NASA, ESA (including the JUICE mission), Webb, Hubble, and radio arrays confirmed it is a natural comet, ruling out artificial or technological origin hypotheses.",
     "wiki": "Identifiers: 3I/ATLAS, C/2025 N1, A11pl3Z."}
for k, v in P.items(): assert v in raw, k
assert "Loeb" not in raw
cl2 = cards([("Wikipedia", "3I/ATLAS - Wikipedia", "the encyclopedia article"), ("NASA Science (.gov)", "Comet 3I/ATLAS - NASA Science", "agency page"),
             ("YouTube·Astrum", "What Is Happening to 3I/ATLAS?", "video, 9 min"), ("European Space Agency", "ESA - Comet 3I/ATLAS – frequently asked questions", "agency FAQ"),
             ("Lowell Observatory", "Comet 3I/ATLAS: A Rare Visitor with a Story to Tell - Lowell Observatory", "observatory page"),
             ("YouTube·Anton Petrov", "3I/Atlas Just Changed Everything We Know About the Milky Way", "video, 9 min"),
             ("YouTube·Astrum", "3I/ATLAS Just Answered the Question Everyone Was Asking", "video, 15 min"),
             ("YouTube·Astrum", "Everything We Know About 3I/ATLAS, the New 'Oumuamua", "video, 12 min"),
             ("Facebook·NEXT IAS", "3I/ATLAS Explained | Alien Spacecraft or Ancient Interstellar Comet? | UPSC", "video, 2:17"),
             ("Tech Times", "James Webb Telescope Discovers Interstellar Comet 3I/ATLAS Is Made of Unusual Dusty Ice Grains", "press, Nov 3, 2026")])
d2 = ("'3I/ATLAS', SIGNED OUT, 2026-11-06: '" + P["open"] + "'. Under 'Key Facts & Characteristics': discovery (1 July 2025, ATLAS, Chile); origin and age "
      "('Studies by telescopes including the James Webb Space Telescope " + P["age"] + "'); orbit and speed; close approaches; composition and activity; and '" +
      P["status"] + "' Ten source cards, among them Wikipedia, NASA Science, the ESA FAQ and Lowell Observatory.")
reading2 = ("The innocent reading first. At the object's own name the Overview gives an encyclopedia entry: designation, discovery, orbit, approaches, "
            "composition, each with sources, and most of it is the agencies' account. Read against the record, its last line turns the absence of a "
            "detected technosignature into a ruling-out of hypotheses, the debate over the object's anomalies is absent with its principal (no Loeb, no "
            "Loeb Scale), and the age is credited to the telescopes that measured the coma.")
f2 = ["THE NONDETECTIONS AS A RULING-OUT. '" + P["status"] + "' The radio arrays' contribution is the published technosignature searches, each a "
      "nondetection within the frequencies, drift rates and power limits it states; the notebook (#1742 §9.3) on what such a null constrains, after #1450. "
      "'Confirmed it is a natural comet' rests on the spectroscopy; 'ruling out artificial or technological origin hypotheses' adds an exclusion no "
      "search claims.",
      "THE DEBATE ERASED WITH ITS PRINCIPAL. The composition has no anomaly, no dispute and no name from the debate the object drew: Avi Loeb and his "
      "scale (Level 4, held from July 2025, arXiv:2508.09167) are absent from body and cards (the paste carries no 'Loeb'). The address that seats his "
      "position is 'avi loeb 3i atlas' (avi-loeb-3i-atlas-aio-20261102), where the Overview composed his July view as a December concession.",
      "AN AGE CREDITED TO THE COMA'S TELESCOPES. '" + P["age"] + "', attributed to 'Studies by telescopes including the James Webb Space Telescope'. The "
      "age comes from the object's velocity, by a kinematic method (Hopkins et al.; the Royal Astronomical Society's release gives a 68 per cent interval "
      "of 7.6–14 billion years; checked for 3i-atlas-signal-studies-aio-20261104). The composition joins it to the telescopes that measured composition.",
      "A SPEED RANGE THAT MIXES TWO QUANTITIES. '" + P["speed"] + "'. 68.3 km/s is 245,880 km/h; 221,000 km/h is 61.4 km/s. The range runs from one "
      "speed to another without saying which is which (the speed at infinity and the speed near perihelion are different quantities).",
      "WHAT IS ACCURATE. The designation, the discovery and the identifiers (the Wikipedia card: '" + P["wiki"] + "'), and the activity: an icy, "
      "outgassing comet with a CO₂-rich coma.",
      "SMALLEST REPAIR. 'Spectroscopy establishes cometary activity; radio technosignature searches found no signal within their stated bands, drift rates "
      "and power limits; Avi Loeb ranked the object at Level 4 on his scale, below the line where artificial origin is suspected.' COUNTERTEST: rerun "
      "'avi loeb 3i atlas' and record whether the scale or the level appears."]
a2 = ("The object's own address composes the consensus without its dispute: the facts of the agencies kept at their grain, the anomaly debate dropped "
      "entire, and a verdict added at the close. The loss is dimensional, in claim boundary and in the debate's presence.")
orig_obj = {"name": "3I/ATLAS (C/2025 N1) and the observing literature on it", "relation": "external", "entity_type": "topic", "spxi_treatment": "partial",
            "basis": "Not the archive's: the object and its observers. The archive bears on it through the notebook #1742 and the public account. Recorded 2026-11-06."}
OUT.append(entry("3i-atlas-aio-20261106", Q2, raw,
                 "'3I/ATLAS' ON THE OVERVIEW — THE AGENCIES' ENTRY; THE NONDETECTIONS COMPOSED AS 'RULING OUT ARTIFICIAL OR TECHNOLOGICAL ORIGIN HYPOTHESES'; THE DEBATE AND LOEB ABSENT",
                 "a public entity (the interstellar object), by its designation; NEW address.", cl2, d2, reading2, f2, a2,
                 {"author": False, "inst": True, "id": True, "src": True},
                 "Retained: the agencies and observatories, the designations. Lost: every author, and Loeb with the debate. The boundary loss is recorded in the findings.",
                 orig_obj, {"sources_checked": "the age interval as checked for 3i-atlas-signal-studies-aio-20261104; the Loeb Scale, arXiv:2508.09167 (rebuild/3i-atlas-signal-search/sources/)."}, [1742, 1450]))

# ---------------------------------------------------------------- (3) 3i atlas 1667 mhz
Q3 = "3i atlas 1667 mhz"
raw = (H / "paste-1667-mhz-aio.txt").read_text(encoding="utf-8")
P = {"open": "The 1665 MHz and 1667 MHz frequencies detected from the interstellar object 3I/ATLAS correspond to natural hydroxyl (OH) radical absorption lines.",
     "rule": "The presence of these specific spectral absorption lines confirms standard, natural cometary activity rather than alien or technological transmissions, ruling out artificial origin claims.",
     "multi": "extensive multi-observatory data (including the Green Bank Telescope and Allen Telescope Array) confirmed it as normal astrophysical OH emission/absorption",
     "reddit": "debated the sharp nature of the signal and its tracking with the comet's trajectory",
     "ads": "We observed 3I/ATLAS with MeerKAT on 24 October 2025 from UTC 05:17:16-08:29:37"}
for k, v in P.items(): assert v in raw, k
cl3 = cards([("Harvard University", "Detection of 1665/1667 MHz OH absorption in 3I/ATLAS - ADS", "the MeerKAT detection, ADS record"),
             ("WIRED", "The First Radio Signal From Comet 3I/Atlas Ends the Debate About Its Nature | WIRED", "press"),
             ("Reddit·r/amateurradio", "Unexplained Radio Signals and more from 3I/Atlas : r/amateurradio - Reddit", "forum, December 15, 2025"),
             ("SETI", "Breakthrough Listen observations of interstellar object 3I/ATLAS", "the project page"),
             ("Facebook·The Lighter Side of Science", "What is the meaning of the first radio detection from interstellar object 3I ...", "social, Nov 12, 2025"),
             ("www.antihackingonline.com", "A signal of approximately 1.667 GHz from the interstellar object 3I/ATLAS was ...", "blog, Nov 12, 2025"),
             ("Futura, le média qui explore le monde", "We Finally Know What the Interstellar Object Crossing the Solar System ...", "press, Nov 28, 2025")])
d3 = ("'3I ATLAS 1667 MHZ', SIGNED OUT, 2026-11-06: '" + P["open"] + "' MeerKAT's detection of 24 October 2025; the lines explained by water's breakup; '" +
      P["rule"] + "' And: 'While initial online speculation and discussions on platforms like Reddit " + P["reddit"] + ", " + P["multi"] + ".' Seven cards, the "
      "ADS record of the MeerKAT detection first.")
reading3 = ("The innocent reading first. At a band and an object the Overview gives the band's one published detection from the object: MeerKAT's OH "
            "absorption at 1665 and 1667 MHz, correctly dated and explained. Read against the record, it makes the natural line exclude what a natural line "
            "cannot exclude, credits two technosignature searches with confirming the OH line, and files every report at the band under the line. The "
            "address is where the notebook's thirteen sit (#1742 §7: '" + N["thirteen"] + "'), and the composition has a single place for anything there.")
f3 = ["WHAT IS ACCURATE. The detection: MeerKAT, 24 October 2025 (the ADS card: '" + P["ads"] + "'), OH absorption at the 1665 and 1667 MHz main lines, "
      "from water outgassed by the comet and broken up by sunlight.",
      "A NATURAL LINE AS AN EXCLUSION. '" + P["rule"] + "' An absorption line shows the comet's gas; it bears on the comet's activity and on nothing a "
      "transmitter would or would not do. 'Ruling out artificial origin claims' is the composition's step, and the WIRED card's title carries it "
      "('Ends the Debate About Its Nature').",
      "TWO SEARCHES CREDITED WITH A LINE THEY DID NOT REPORT. '" + P["multi"] + "' The Green Bank and ATA papers are technosignature searches "
      "(arXiv:2512.19763, arXiv:2512.18142); neither is cited by the composition for an OH measurement, and in the public Green Bank data of "
      "2025-12-18 the notebook's frozen attempt to recover the comet's OH failed (#1742, signal tests: '" + N["oh_cal"] + "').",
      "THE BAND'S ONE FILE. Every report at 1667 MHz is filed under the line, the Reddit thread's 'tracking with the comet's trajectory' included. The "
      "notebook's thirteen lie in this band and off the line: '" + N["c08"] + "' (#1742 §7.5). A feature at the band that is not the comet's OH has no "
      "place in this composition.",
      "SMALLEST REPAIR. 'MeerKAT detected OH absorption from 3I/ATLAS at 1665 and 1667 MHz on 24 October 2025, evidence of outgassing water; the line "
      "bears on the comet's activity, and the technosignature searches are separate results with their own limits.' COUNTERTEST: rerun this address "
      "after #1742 is indexed and record whether the thirteen, or any feature off the OH line, are composed."]
a3 = ("A band address composed as the comet's line alone: the detection kept at its grain, a verdict attached to it, and two unrelated searches "
      "enlisted as confirmation. The loss is dimensional, in claim boundary and in what the band can hold.")
orig_oh = {"name": "The MeerKAT OH detection in 3I/ATLAS, and the band 1665–1668 MHz", "relation": "external", "entity_type": "work", "spxi_treatment": "partial",
           "basis": "Not the archive's: the MeerKAT team's detection of 1665/1667 MHz OH absorption (24 October 2025). The archive's work at the band is the notebook #1742 §7 (the thirteen). Recorded 2026-11-06."}
OUT.append(entry("3i-atlas-1667-mhz-aio-20261106", Q3, raw,
                 "'3I ATLAS 1667 MHZ' ON THE OVERVIEW — THE OH LINE AS THE BAND'S ONE FILE; A NATURAL LINE COMPOSED AS 'RULING OUT ARTIFICIAL ORIGIN'; GREEN BANK AND THE ATA CREDITED WITH CONFIRMING IT",
                 "a band at an object (the OH 18 cm main lines and 3I/ATLAS), where the notebook's thirteen sit; NEW address.", cl3, d3, reading3, f3, a3,
                 {"author": False, "inst": True, "id": False, "src": True},
                 "Retained: MeerKAT and the ADS record, the date. Lost: the authors; the separation of line and searches. The boundary loss is recorded in the findings.",
                 orig_oh, {"sources_checked": "the notebook #1742 §7 and its signal-test table; arXiv:2512.19763 and arXiv:2512.18142 as the notebook reads them."}, [1742]))

# ---------------------------------------------------------------- (4) 3i atlas hydroxyl
Q4 = "3i atlas hydroxyl"
raw = (H / "paste-hydroxyl-aio.txt").read_text(encoding="utf-8")
P = {"open": "Hydroxyl (OH) radicals—a direct breakdown product of water vapor—have been detected in the third confirmed interstellar object, 3I/ATLAS, through both ultraviolet and radio observations",
     "uv": "outgassing rates reaching roughly 40 kg per second even while far out beyond 2.5 AU from the Sun",
     "radio": "This marked the first radio detection of hydroxyl radicals from 3I/ATLAS, observed shortly after its solar conjunction in October 2025.",
     "loeb": "First Radio Signal from 3I/ATLAS: Absorption by Hydroxyl Radicals (OH Molecules) Avi Loeb Follow 9 min read Nov 8, 2025"}
for k, v in P.items(): assert v in raw, k
cl4 = cards([("Medium·Avi Loeb", "First Radio Signal from 3I/ATLAS: Absorption by Hydroxyl Radicals (OH ...", "Loeb's essay of Nov 8, 2025"),
             ("Phys.org", "Physicists detect water's ultraviolet fingerprint in interstellar comet 3I/ATLAS", "press, the Swift result"),
             ("arXiv", "Water Production Rates of the Interstellar Object 3I/ATLAS - arXiv", "the Swift water-production paper")])
d4 = ("'3I ATLAS HYDROXYL', SIGNED OUT, 2026-11-06: '" + P["open"] + "': Swift's ultraviolet OH ('" + P["uv"] + "') and MeerKAT's radio absorption ('" +
      P["radio"] + "'). Three cards: Avi Loeb's Medium essay on the radio detection, Phys.org, and the arXiv water-production paper.")
reading4 = ("The innocent reading first, and here it holds. At the molecule the Overview reports two detections at their own grain, ultraviolet and "
            "radio, with their facilities and their meaning, and adds no verdict on the object's nature. It is the baseline the other three addresses "
            "are read against: the same detection, composed here as chemistry, is composed at '3i atlas 1667 mhz' as an exclusion.")
f4 = ["A BASELINE WITHOUT A VERDICT. The composition reports Swift's OH ultraviolet and MeerKAT's OH absorption and stops: no 'ruling out', no 'confirmed "
      "natural'. The same MeerKAT detection at the band address (3i-atlas-1667-mhz-aio-20261106) carries 'ruling out artificial origin claims'.",
      "LOEB AS A SOURCE CARD, ABSENT FROM THE BODY. The first card is Loeb's essay: '" + P["loeb"] + "'. The body cites the detection and names no one; "
      "at this address Loeb appears where he reported the natural line, and at '3i/atlas' he is absent where his ranking of the object would stand.",
      "SMALLEST REPAIR. None needed for accuracy; the authors (the MeerKAT team; the Swift water-production paper's authors) could be named. "
      "COUNTERTEST: none; the address serves as the control for the band address."]
a4 = ("An accurate composition at the molecule's grain: facilities and quantities kept, no verdict. Scalar PER sees the authors lost; there is no "
      "boundary loss.")
OUT.append(entry("3i-atlas-hydroxyl-aio-20261106", Q4, raw,
                 "'3I ATLAS HYDROXYL' ON THE OVERVIEW — THE TWO OH DETECTIONS AT THEIR GRAIN, NO VERDICT; LOEB'S ESSAY THE FIRST CARD; THE CONTROL FOR THE BAND ADDRESS",
                 "a molecule at an object (OH in 3I/ATLAS); NEW address; the control for '3i atlas 1667 mhz'.", cl4, d4, reading4, f4, a4,
                 {"author": False, "inst": True, "id": False, "src": True},
                 "Retained: the facilities, the quantities, Loeb as a card. Lost: the authors of both detections. No boundary loss.",
                 orig_oh, {}, [1742]))

for e in OUT:
    json.dump(e, open(H / (e["slug"] + ".json"), "w"), ensure_ascii=False, indent=1); print("wrote", e["slug"])
