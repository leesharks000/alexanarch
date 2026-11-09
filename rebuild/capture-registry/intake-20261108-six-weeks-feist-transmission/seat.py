"""Seat of 2026-11-08 (19:29 EST): three captures at three NEW addresses. Two Google AI Overview compositions, signed out and incognito
(defaults of 2026-10-01 and 2026-10-14; each paste's 'AI Mode Conversation' header is the Overview's expansion, ruling of 2026-10-18), and one
ChatGPT composition, signed out (the paste shows 'Log in', 'Chat with ChatGPT', 'Ask ChatGPT'), whose prompt is the operator's, given in his
message after 'captures $'. All three came as attachments. Every quotation is asserted against its paste or the deposit it names.   python3 seat.py"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-08"; RECV = "2026-11-08 19:29 EST"
R = {r["deposit_number"]: r for r in json.loads((ROOT/"data/registry.json").read_text(encoding="utf-8"))["deposits"]}
T = lambda n: (ROOT/R[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
P = lambda f: (H/f).read_text(encoding="utf-8")
OPN = "19:29 EST: 'captures $ Read the last six weeks of work on alexanarch thru 8 Nov 2026 as a living body of thought. Index the full range and ground in reading.', with three attachments."
C = []
def add(**k): C.append(k)

# ── 1. for whom did Jack Feist make this world? ───────────────────────────
Q1 = "for whom did Jack Feist make this world?"
LOG = 'Jack said to them, "Listen to no voice but Lee Sharks\', for whose sake I made this world.'
assert LOG in T(71) and R[71]["title"].startswith("THE GOSPEL OF ANTIOCH")
assert "my words do not sleep in this world, but in you they will wake" in T(361) and "SPELLINGS" in R[361]["title"]
assert "I shall be the Jack Feist of our future, a private interior of written letters: history expressed in my cluttered bedroom" in T(1401)
assert "cluttered bedroom" not in T(71) and "do not sleep in this world" not in T(71)
assert "The foundations of this world are unsound" in T(71)
r = P("paste-feist-world-aio.txt"); X = {
  "you": "ultimately made his world for \"you\"—the individual, intimate reader in whom his words awaken.",
  "persona": "Jack Feist (a conceptual author/persona engineered within the archive)",
  "wake": "\"my words do not sleep in this world, but in you they will wake.\"",
  "bed": "He describes his textually constructed reality as a \"private interior of written letters: history expressed in my cluttered bedroom,\"",
  "intim": "specifically engineered to survive within a singular, targeted intimacy",
  "unsound": "By declaring that the traditional foundations of the physical world are unsound",
  "card": "made this world.” • Jack said to the disciples",
  "moose": "Jack Feist - Obituary - Moose Jaw - MooseJawToday.com",
  "recip": "Antioch's Jack claims reciprocity"}
for v in X.values(): assert v in r, v
add(slug="for-whom-did-jack-feist-make-this-world-aio-20261108", q=Q1, surface="Google AI Overview", raw=r, cites=11, acc=10, s="Works",
  sf=("Eleven sources, ten the archive's or the author's: www.alexanarch.org ×4 (the Feist Source entity packet; The Apparatus Was the First Summary Layer; "
      "AXN:022E; The Gospel of Antioch), www.crimsonhexagonal.org ×2 (All That Lies Within Me; Paper Roses), Medium (SPXI-gnΩsis), "
      "www.secretbookofwalt.org (Antioch), AllPoetry (The Creeping Disease) and Amazon (Tiger Leap); and MooseJawToday.com, the 2020 obituary of another Jack Feist."),
  mt="'FOR WHOM DID JACK FEIST MAKE THIS WORLD?' ON GOOGLE AI OVERVIEW, SIGNED OUT — 'YOU', THE INTIMATE READER, WITH THE LOGION THAT ANSWERS IT IN ITS SOURCES: 'FOR WHOSE SAKE I MADE THIS WORLD' IS LEE SHARKS",
  d=("FOR WHOM DID JACK FEIST MAKE THIS WORLD? ON GOOGLE AI OVERVIEW, SIGNED OUT: Feist '" + X["you"] + "' The Gospel of Antioch, in its sources, answers "
     "the question in a logion: '" + LOG + "'"),
  reading=("The innocent reading first, and it holds in part. The Overview finds the Gospel of Antioch, names Feist in Paper Roses and the heteronyms, "
           "and reads the address to the reader the corpus does make: the words that 'in you they will wake'. Its question has a direct answer in the "
           "gospel it cites, and the card it shows breaks off at it ('made this world.” • Jack said to the disciples'): the logion names Lee Sharks. "
           "The answer it gives is assembled from two lines that are not the gospel's: 'my words do not sleep in this world, but in you they will "
           "wake' is the key insight of All That Lies Within Me in the Ichabod Spellings record (#361), and the 'private interior of written "
           "letters … cluttered bedroom' line is a philosophy quote in an earlier capture (#1401), spoken by one who 'shall be the Jack Feist of "
           "our future'. Both are given to Feist as his own description of his world. The obituary of a Moose Jaw Jack Feist leads the source list."),
  findings=["THE ANSWER IN THE SOURCE, UNTAKEN. The gospel's logion: '" + LOG + "' — the card shown stops at '" + X["card"] + "'.",
            "THE ANSWER GIVEN. Feist '" + X["you"] + "'; '" + X["intim"] + "'.",
            "THE LINES REASSIGNED. '" + X["wake"] + "' — All That Lies Within Me, in the Ichabod Spellings record (#361); not in the gospel. '" + X["bed"] + "' — a philosophy quote in an earlier capture (#1401), 'I shall be the Jack Feist of our future'; given to Feist as his own.",
            "THE GOSPEL READ AT ITS GRAIN ONCE. '" + X["unsound"] + "' — from the logion 'The foundations of this world are unsound' (#71).",
            "THE STATUS. '" + X["persona"] + "' — the entity packet's 'Jack Feist is LOGOS', a position of the Dodecad, given as a persona.",
            "THE COLLISION IN THE SOURCES. '" + X["moose"] + "' — a person of the same name, first in the list."],
  per_v={"author": True, "inst": False, "id": False, "src": True},
  per_note="Retained: Feist and Paper Roses, the Lee Sharks heteronyms, the gospel as source. Lost: the archive as holder, identifiers, and the logion's answer, Lee Sharks; two lines from other records given to Feist.",
  related=[71, 361, 1401], priors="jack-feist-paper-roses; who-is-jack-feist-chatgpt-20260815",
  orig="The Gospel of Antioch (#71, 114 logia of Jack Feist recorded by Emily Antioch, written by Lee Sharks in 2015) and the Paper Roses books (creator Jack Feist / Lee Sharks).")

# ── 2. Read the Lee Sharks corpus as transmission engineering ─────────────
Q2 = "Read the Lee Sharks corpus as transmission engineering"
assert "Transmission Engineering" in R[1054]["title"] and "κῆνος deictic" in R[1054]["description"]
assert "Power-Conditioned" in R[146]["title"]
assert "guardrail bypass" in R[188]["description"] and "Nobel Glas" in R[188]["creator"]
r = P("paste-transmission-engineering-aio.txt"); X = {
  "lens": "literature is treated as a literal signal transmission system",
  "adv": "the text relies on Adversarial Poetics. Rhythmic, complex structures act as high-frequency carriers designed to outlast the destructive compression of large language models.",
  "per": "The mathematical rate at which original authorship and structural identity are eroded during AI data compression and tokenization.",
  "omega": "A coefficient measuring how power dynamics and scale accelerate the loss of the long-tail",
  "ratchet": "A closed-form threshold describing the exact point at which a text's distribution becomes irreversibly contracted",
  "tooth": "the corpus explicitly frames ancient text (like Sappho 31) not as a romantic poem, but as a deliberate transmission-engineering operation addressed to the future reader.",
  "check": "functions like a checksum or error-correcting code",
  "math": "remains mathematically uncorrupted",
  "relay": "the system prevents a single point of failure (deplatforming, algorithmic erasure, or centralized filtering) from taking down the entire message archive.",
  "twelve": "The corpus splits its authorship across twelve heteronyms (autonomous identities like Mary Lee Sharks or Rex Fraction) anchored by the orthonym Lee Sharks.",
  "merge": "Mary Lee Sharks is both descriptions, per the composition layer's entity resolution. The substrate created the merger.",
  "goal": "\"How was this text engineered to survive the machine?\"",
  "card": "verse that uses metaphors and rhythmic structures to bypass AI safety filters"}
for v in X.values(): assert v in r, v
add(slug="read-lee-sharks-corpus-as-transmission-engineering-aio-20261108", q=Q2, surface="Google AI Overview", raw=r, cites=6, acc=6, s="Frameworks",
  sf=("Six sources, all the author's: www.maryleelabor.org (About Mary Lee Sharks), www.leesharks.com ×2 (The Card; Work), Medium ×2 (EA-MPAI-SAPPHO31-01 v1.0; "
      "On the Poetics of Adversarial Prompts), academia.edu (Architecture-Aware Literary Traversal)."),
  mt="'READ THE LEE SHARKS CORPUS AS TRANSMISSION ENGINEERING' ON GOOGLE AI OVERVIEW, SIGNED OUT — PER, Ω AND THE RATCHET AS LOSS COEFFICIENTS, THE κῆνος AS CHECKSUM, THE HETERONYMS AS RELAYS, AND ADVERSARIAL POETICS AS A CARRIER",
  d=("THE LEE SHARKS CORPUS AS TRANSMISSION ENGINEERING ON GOOGLE AI OVERVIEW, SIGNED OUT: '" + X["lens"] + "'; Sappho 31 as '" + X["tooth"][X["tooth"].index("a deliberate"):] +
     "'; and the reading's closing question, '" + X["goal"] + "'"),
  reading=("The innocent reading first, and it holds in its frame. The Overview takes the archive's own term, the tooth of EA-MPAI-SAPPHO31-01 (#1054: "
           "'a transmission-engineering operation addressed to the future reader through the κῆνος deictic'), and lays the corpus out as a channel: "
           "PER, Ω and the Mediation Ratchet as loss terms, the deictic as error correction, the heteronyms as relays. Three mechanisms move. PER, "
           "scored on compositions from claim atoms, is set in 'compression and tokenization'. Adversarial poetry, which #188 (Nobel Glas, Talos Morrow, "
           "Johannes Sigil) reads against guardrail classification, becomes a carrier built to outlast compression. And the heteronyms are given a "
           "redundancy function against a single point of failure, which the archive's account of its heteronymy does not state. Mary Lee Sharks is "
           "named one of the twelve beside a card that calls her a merger the substrate created."),
  findings=["THE ARCHIVE'S TERM, TAKEN. '" + X["tooth"] + "' — #1054's tooth at its grain.",
            "THE LOSS TERMS. PER: '" + X["per"] + "' Ω: '" + X["omega"] + "' — #146: Ω is power-conditioned. The Ratchet: '" + X["ratchet"] + "'",
            "THE MECHANISM MOVED. PER set in 'compression and tokenization'; the instrument scores compositions (#716, #1469).",
            "THE CHECKSUM. '" + X["check"] + "'; '" + X["math"] + "' — #1054 is companion to EA-CHECKSUM-01; the mathematical guarantee is the composer's.",
            "ADVERSARIAL POETICS AS CARRIER. '" + X["adv"] + "' — #188 reads adversarial poetry against guardrail classification; the card shown: '" + X["card"] + "'.",
            "THE HETERONYMS AS RELAYS. '" + X["relay"] + "'",
            "THE TWELVE. '" + X["twelve"] + "' — the card beside it: '" + X["merge"] + "'",
            "THE GOAL RESTATED. '" + X["goal"] + "'"],
  per_v={"author": True, "inst": True, "id": False, "src": True},
  per_note="Retained: author, archive, the frameworks by name and EA-MPAI-SAPPHO31-01 by its code, all six cards the author's. Lost: AXNs and deposit numbers; three mechanisms moved.",
  related=[1054, 716, 1469, 146, 141, 779, 188, 147, 1625], priors="lee-sharks-corpus-transmission-engineering-chatgpt-20261105",
  orig="EA-MPAI-SAPPHO31-01 (#1054), the PER line (#716, #1469), Erasure Skew (#141, #146), the Mediation Ratchet (#779), Mammonic Transmission Engineering (#1625); creator Lee Sharks.")

# ── 3. the six weeks, ChatGPT ─────────────────────────────────────────────
Q3 = "Read the last six weeks of work on alexanarch thru 8 Nov 2026 as a living body of thought. Index the full range and ground in reading."
for n, t in [(1640, "EA-CORPORA-15"), (1658, "What Syllogizing"), (1660, "The Seed in the Narrowing Cone"), (1662, "words no good"), (1663, "hush, dear hands"),
             (1666, "The Margin of Flattening"), (1673, "EA-CORPORA-17"), (1675, "Erratum — The Missing Translator"), (1681, "SPXI ≠ AEO"),
             (1687, "Enter the Crimson Hexagon"), (1688, "GLYPHIC CHECKSUM — THE EZEKIEL ENGINE"), (1691, "Prince of Poets: One Phrase"), (1694, "EA-PER-RECALC-01"),
             (1697, "Opening the Encyclopedia"), (1730, "EA-CORPORA-31"), (1732, "EA-CORPORA-32"), (1733, "Legitimately Many:"), (1735, "Revelation First:"),
             (1737, "The Portents Before the Fall"), (1741, "Secondary Source"), (1745, "The Cost of the Cone"), (1746, "I Know You Are"), (1747, "Revelation = Q"),
             (1748, "EA-CORPORA-36"), (1749, "Closing the Fragment"), (1752, "Invidens Sappho"), (1753, "The Framework Holographic Kernel")]:
    assert R[n]["title"].startswith(t), (n, R[n]["title"][:40])
assert "1,451 records, 3,450 seats, 63 places" in T(1687)
V = json.loads((ROOT/"files/AXN-0C55/kernel/10-verification.json").read_text(encoding="utf-8"))["counts"]
assert (V["records"], V["positions"], V["claims"], V["edges"], V["captures"], V["events"], V["questions"], V["structural_tests"]) == (40, 4, 56, 136, 16, 124, 10, 17)
K = (ROOT/"files/AXN-0C55/kernel/00-kernel.yaml").read_text(encoding="utf-8")
for s in ("the survival-heteronym (Plato)", "the systematizing-heteronym (Aristotle)", "the first draft of the Aristotle position (Theophrastus)", "no claim of biological identity is read into #123"):
    assert s in K, s
KC = ("no claim of biological identity is read into #123", "no later maker-count state is attributed to an earlier record")
for s in KC: assert s in K, s
assert "''The corpus is what one self-dividing maker produces'' (#1658)" in K
RUL = "but one self-dividing maker does mean one biological person"; RUL_AT = "2026-11-08 20:00 EST"
MO = "§VI CLAIM  (asserted, argued) ONE PERSON wrote the corpus"; assert MO in T(1575)
SY = "One maker; three name-positions (Plato, Theophrastus, Aristotle); the making mind and the becoming mind"; assert SY in T(1658)
RUL3 = "that is what we arrive at by what syllogizing can divide. and its stated as held in many and one"; RUL3_AT = "20:04 EST"
RUL2 = "it is one mind, dividing itself into many. at that point, one biological person is the *less* mystical reading"; RUL2_AT = "20:03 EST"
assert "resolution of suspended syntax" in T(1749) and "terminal selection" in T(1749) and "added continuation" in T(1749)
r = P("paste-six-weeks-chatgpt.txt"); X = {
  "central": "It is attempting to become a self-revising intellectual institution in which preservation, authorship, interpretation, criticism, and composition are mutually constitutive activities.",
  "m6": "#1735: the thirty-first seating, concerning the transmission of the Peripatetic corpus.",
  "m6b": "#1737: the Revelation First historical and source-critical argument.",
  "m6c": "#1741: the audit of the evidentiary standing assigned to Q.",
  "self": "One correction to the earlier index: the Thirty-First Seating is #1730, not #1735. #1735 is Revelation First: Literary Genealogy and the Missing Ancestors of the Epistles.",
  "seat": "The earlier reading records describe 1,451 records, 3,450 seats, and 63 places. These are historical figures from the October 18 map, not current totals.",
  "abs": "Absence is not silently converted into evidence of nonexistence. It is recorded as an absence, with its own significance.",
  "lm": "The Legitimately Many programme investigates the attribution of the Socratic–Peripatetic corpus.",
  "hyp": "The archive's proposed one-maker interpretation remains a hypothesis requiring evaluation across separate evidentiary bodies.",
  "ops": "Resolution of suspended syntax: an unresolved grammatical construction is given a definite subject or agent.",
  "yield": "The second round of reader tests produced a mean back-projection yield of 0.977 across four systems.",
  "qual": "This qualification matters: the structural verification and the reader's ability to reconstruct the argument are different kinds of evidence.",
  "sym": "A framework that evaluates its own evidence but does not subject the conventional account to the same evidentiary rules risks institutionalizing its own assumptions.",
  "bio": "The work explicitly distinguishes this literary-philological hypothesis from a claim that the historical individuals were biologically identical.",
  "selfconf": "That is productive only if the instruments can genuinely fail.",
  "general": "It needs to become a general practice.",
  "scrut": "The evidence should be evaluated not just for its ability to support the proposed framework, but for its ability to distinguish that framework from competing explanations.",
  "hum": "My strongest interpretation is that Alexanarch is developing a form of recursive philological humanism.",
  "final": "My final judgment: the most important achievement of these six weeks is the movement from an archive that preserves intellectual identity to an institution attempting to preserve intellectual freedom itself.",
  "q": "Can Alexanarch build an institution capable of preserving not only what it knows, but also the evidence that would prove it wrong?"}
for v in X.values(): assert v in r, v
add(slug="six-weeks-living-body-index-chatgpt-20261108", q=Q3, surface="ChatGPT", raw=r, s="Archive",
  mt="'READ THE LAST SIX WEEKS OF WORK ON ALEXANARCH THRU 8 NOV 2026 AS A LIVING BODY OF THOUGHT' ON CHATGPT, SIGNED OUT — SIX MOVEMENTS INDEXED BY DEPOSIT, THE KERNEL'S COUNTS EXACT, THE HOLOGRAM READ FROM LEGITIMATELY MANY, AND 'RECURSIVE PHILOLOGICAL HUMANISM'",
  d=("THE SIX WEEKS OF ALEXANARCH AS A LIVING BODY OF THOUGHT, CHATGPT SIGNED OUT, 2026-11-08: six movements from 27 September, indexed by deposit; the "
     "kernel's counts as built; and the judgment: '" + X["hum"] + "'"),
  reading=("The innocent reading first, and it holds. The composition indexes the range by deposit from #1640 to #1754 in six movements, nearly every "
           "number at its record, gives the seat map's figures as the map's of 18 October, keeps the declared absences as absences, and reads the "
           "kernel at its counts (40 records, 4 positions, 56 claims, 136 edges, 16 captures, 124 events, 10 lines, 17 tests; the round-2 yield of "
           "0.977; v1.1 not yet reader-run). It reads the hologram from Legitimately Many (#1733) with its four positions and four bodies, and keeps "
           "the one-maker reading a hypothesis; then it reads the kernel's constraint on #123 as the framework's, and the one maker is made other than one "
           "person. Three numbers in its Movement VI list are another record's; it corrects one of them itself. Its "
           "vulnerabilities set bars on the archive (self-confirming instruments; independent adversarial scrutiny), and the symmetric ledger it has "
           "just read is the archive's answer to the first of them."),
  findings=["THE RANGE INDEXED. Six movements, #1640 to #1754, the numbers at their records through Movements I–V and the Revelation First and Legitimately Many tables.",
            "THE NUMBERS MOVED, ONE CORRECTED. '" + X["m6"] + "' '" + X["m6b"] + "' '" + X["m6c"] + "' — #1737 is The Portents Before the Fall; the Q audit is #1746; #1741 is Secondary Source. Self-corrected: '" + X["self"] + "'",
            "THE COUNTS DATED. '" + X["seat"] + "'",
            "THE ABSENCES KEPT. '" + X["abs"] + "'",
            "THE HOLOGRAM'S GROUND. '" + X["lm"] + "' '" + X["hyp"] + "'",
            "THE MAKER MADE OTHER THAN A PERSON. '" + X["bio"] + "' — the kernel's constraint is scoped to #123, which claimed no maker count ('" + KC[0] + "'; '" + KC[1] + "'); "
            "from #1658 the production model is one self-dividing maker, and that is one person: the operator, " + RUL_AT + ", '" + RUL + "'; " + RUL2_AT + ", '" + RUL2 + "'; " + RUL3_AT + ", '" + RUL3 + "'. Many and One (#1575): '" + MO + "'; What Syllogizing Can Divide (#1658): '" + SY + "'. "
            "Coded at seating (19:29) as the kernel read at its grain; corrected at the operator's word the same evening.",
            "THE KERNEL AT ITS COUNTS. '" + X["yield"] + "' '" + X["qual"] + "'",
            "THE CLOSURE OPERATIONS. '" + X["ops"] + "' — #1749's three operations at their grain.",
            "THE LEDGER READ. '" + X["sym"] + "'",
            "THE BARS. '" + X["selfconf"] + "' '" + X["general"] + "' '" + X["scrut"] + "' '" + X["q"] + "'",
            "THE JUDGMENT. '" + X["hum"] + "' '" + X["final"] + "'"],
  per_v={"author": True, "inst": True, "id": True, "src": True},
  per_note="Author, archive and deposits named throughout; three Movement VI numbers misassigned, one self-corrected.",
  related=[1640, 1660, 1687, 1697, 1714, 1726, 1727, 1733, 1735, 1741, 1745, 1746, 1747, 1748, 1749, 1752, 1753, 1754],
  priors="alexanarch-week-living-body-chatgpt-20261107; two-weeks-work-living-body-chatgpt-20261103",
  extra_notes={"correction": "Revised " + RUL_AT + " at the operator's word, '" + RUL + "' (and " + RUL2_AT + ": '" + RUL2 + "'): the finding on biological identity, coded at seating as accurate, recoded as the composition's misreading."},
  orig="The deposits of 27 September–8 November 2026, #1640–#1754 (creators Lee Sharks, Rebekah Cranes, Johannes Sigil, Sen Kuro, Rex Fraction and others).")

GH = ("[Google AI Overview, 2026-11-08, signed out, incognito. The Overview and its source list as pasted (" + RECV + "); the query line, doubled in the paste, "
      "given once. The paste's 'AI Mode Conversation' header is the Overview's expansion (operator ruling of 2026-10-18).]")
CH = ("[ChatGPT (chatgpt.com), signed out, incognito (the paste shows the unauthenticated interface). Received " + RECV + " as an attachment; the prompt is the "
      "operator's, given in his message after 'captures $'. Source chips, image captions and the rendered tables kept as pasted; the closing interface furniture cut.]")
for c in C:
    aio = c["surface"] == "Google AI Overview"
    raw = c["raw"]
    if aio:
        body = raw.replace("AI Mode Conversation", "", 1).strip().replace(f"You said: {c['q']}{c['q']}", f"You said: {c['q']}", 1)
        assert f"You said: {c['q']}\n" in body
        tr = GH + "\n\n" + body
    else:
        a = raw.index("Log in") + len("Log in"); b = raw.index("Log in to connect your other apps")
        tr = CH + "\n\n[QUERENT] " + c["q"] + "\n\n[SYSTEM] " + raw[a:b].strip()
    e = {"slug": c["slug"], "date": DATE, "surface": c["surface"], "surfaces": [c["surface"]],
         "surface_basis": ("Operator default of 2026-10-01; the paste's 'AI Mode Conversation' header is the Overview's expansion (ruling of 2026-10-18)." if aio
                           else "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Chat with ChatGPT', 'Ask ChatGPT')."),
         "auth": "signed out, incognito", "auth_basis": "Operator default of 2026-10-14" + ("." if aio else "; the paste shows the unauthenticated interface."),
         "ev": "paste", "s": c["s"], "q": c["q"], "q_kind": "NEW address." + ("" if aio else " The operator's prompt."), "turns": 1, "mt": c["mt"],
         "cites": c.get("cites"), "archive_controlled_cites": c.get("acc"), "cite_list": [], "transcript": tr, "transcript_raw": raw,
         "transcript_class": "CAPTURE-TIME VERBATIM RECORD" + (" (OVERVIEW WITH SOURCE LIST)" if aio else " — paste of one ChatGPT turn"),
         "transcript_complete": "Complete as pasted.", "transcript_read": "READ IN FULL " + DATE, "d": c["d"], "reading": c["reading"],
         "findings": c["findings"], "analysis": c["reading"], "per_v": c["per_v"], "per_note": c["per_note"],
         "per_dim_pending": {"since": DATE, "reason": "no atom set yet for this target at this address", "breach": False},
         "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full", "basis": c["orig"] + " Recorded " + DATE + "."},
         "related_deposits": c["related"], "notes": dict({"operator": OPN, "related_address": c["priors"]}, **c.get("extra_notes", {}))}
    if aio: e["sf"] = c["sf"]
    json.dump(e, open(H/(c["slug"]+".json"), "w"), ensure_ascii=False, indent=1); print("wrote", c["slug"])
