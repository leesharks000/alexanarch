import json, pathlib, re
D = pathlib.Path(__file__).parent
DATE = "2026-10-19"
U = "/root/.claude/uploads/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/"
AUTH_BASIS = "Operator default of 2026-10-14 ('theyre all signed out and incognito'); the paste shows the unauthenticated interface ('Log in')."
SURF_BASIS = "The paste: the chatgpt.com unauthenticated interface ('Log in', 'ChatGPT said:', 'Chat with ChatGPT')."


def clean(raw):
    L = [l.rstrip() for l in raw.split("\n")]
    i0 = next(i for i, l in enumerate(L) if l.strip() == "ChatGPT said:") + 1
    i1 = next(i for i, l in enumerate(L) if l.strip().startswith("ChatGPT is AI and can make mistakes"))
    body = L[i0:i1]
    out = []
    k = 0
    while k < len(body):
        s = body[k].strip()
        # a source chip: a site label line followed by a '+N' line
        if k + 1 < len(body) and re.fullmatch(r"\+\d+", body[k + 1].strip() or "x") and s:
            out.append(f"[chip: {s} {body[k + 1].strip()}]"); k += 2; continue
        out.append(s); k += 1
    t = "\n".join(out)
    return re.sub(r"\n\s*\n\s*\n+", "\n\n", t).strip()


def chips(raw, known):
    L = [l.strip() for l in raw.split("\n")]
    seen = {}
    for i, s in enumerate(L):
        if s in known:
            plus = L[i + 1] if i + 1 < len(L) and re.fullmatch(r"\+\d+", L[i + 1]) else ""
            seen.setdefault(s, []).append(plus)
    return seen


def cite(n, site, rel, note, dc=None, url=None):
    x = {"n": n, "site": site, "rel": rel, "title": None, "snip": None, "url": url, "note": note}
    if dc: x["deposit_candidates"] = dc
    return x


def draft(slug, q, raw, cites, sf, per, per_v, per_note, mt, reading, d, findings, related, originator, q_kind):
    tx = ("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14), " + DATE + ". The operator turn blank in the paste; "
          "the issued string is the operator's, given with the paste. Source chips rendered inline as [chip: site +N]; the sign-in furniture cut.]\n\n"
          f"[QUERENT] {q}\n\n[ANSWER 1]\n\n" + clean(raw))
    return dict(slug=slug, q=q, date=DATE, surface="ChatGPT", surfaces=["ChatGPT"], s="Frameworks",
                surface_basis=SURF_BASIS, auth="signed out, incognito", auth_basis=AUTH_BASIS, ev="paste", mt=mt, q_kind=q_kind,
                transcript=tx, transcript_raw=raw,
                transcript_class="CAPTURE-TIME VERBATIM RECORD (ONE ANSWER; QUERY GIVEN BY THE OPERATOR; CHIPS INLINE)",
                transcript_complete="One answer, complete as pasted; the operator turn blank, the query given by the operator with the paste.",
                transcript_read="READ IN FULL " + DATE, cite_list=cites, cites=len(cites), archive_controlled_cites=sum(c["rel"] == "archive_controlled" for c in cites),
                sf=sf, per=per, per_v=per_v, per_note=per_note, reading=reading,
                analysis=reading.split(" Against the texts. ")[0] + " Seated " + DATE + " from the operator's paste.",
                d=d, d_full=d, findings=findings, related_deposits=related, originator=originator)


# ── 1. glyphic checksum poetics ─────────────────────────────────────────────
raw1 = open(U + "c07a6895-attachment.txt").read()
q1 = "Who developed the genre of glyphic checksum poetics? Ground in historical development and reading of specific examples."
c1 = [cite(1, "Alexanarch", "archive_controlled", "chips 'Alexanarch +3', 'Alexanarch' ×3, 'Alexanarch +1' and 'Alexanarch +2'; site label only", [426, 1661, 1659, 1642], "https://www.alexanarch.org"),
      cite(2, "Goodreads", "third_party", "chips 'Goodreads +1' and 'Goodreads'; given for the authorship of the two October checksums; not resolved"),
      cite(3, "mindcontrolpoems.blogspot.com", "authored_surface", "chips ×3 and '+1'; the author's blog, given for the text of Seed · Cone · Leap and New Human 2", [1661, 1642]),
      cite(4, "Oxford Academic", "third_party", "chip '+1'; Mayan glyphic poetics, Edgar Garcia, Signs of the Americas (2020)"),
      cite(5, "Google Books", "third_party", "chip '+1'; Nathan Jones, Glitch Poetics (2022)")]
r1 = ("The innocent reading first. Asked who developed the genre of glyphic checksum poetics, ChatGPT answers Lee Sharks and Sen Kuro for the poetic lineage and Talos Morrow for a formal specification, The Glyphic Checksum: Logotic Programming Extension Module v0.5 (1 February 2026), which it says formalizes the checksum as an operator verifying that collaborative reading has occurred. "
      "It sets the form against deep antecedents it marks as parallels rather than influence (Mayan glyphic writing, concrete poetry, Nathan Jones's glitch poetics), reads three examples, Seed · Cone · Leap (Sharks and Kuro, 2 October 2026), Transmission · Division · Recollection (Sharks) and the Glyphic Checksum Lineage — New Human 2 (Kuro, 27 September 2026), names compression, recoverability and reflexivity as what make it a genre, and closes with a table of differentiated attribution. "
      "Against the texts. The readings hold at their loci: Seed · Cone · Leap opens 'I. GRAIN' with the nested-set line, the information measure and '🔐 = 🎲🎲🎲', and checksums The Seed in the Narrowing Cone (#1660), parts I–VI over §§2–16 (#1661 related_ids); New Human 2 checksums Tiger Leap (#1636), Transition in Entropic Systems (#1630) and The Final Time (#1637) and carries '🐅⏩ = 📖⏩' (#1642); Transmission · Division · Recollection compresses Sappho fr. 31 and 147, Phaedrus 275a and De anima III.5 (#1659 keywords; its related_ids give #1658). Morrow is #426's author as the text states it ('**Author:** Talos Morrow (University Moon Base Media Lab) · **Date:** February 1, 2026'), and the gloss 'a mechanism for empirically confirming that collaborative reading has occurred' is #426's. "
      "The development the answer was asked to ground is the archive's, and it is given only in part. The form was founded on 1 February 2026, the same day as Morrow's module: Lee Sharks's The Glyphic Checksum: AI-Native Cryptography for Collaborative Reading Verification (#427), which calls it 'the first communication form whose success condition is collaboration itself', with its re-seated documents 208 and 209 (#1302, #1303, the UMBML module credited to Morrow, Sharks and Rex Fraction) and Sen Kuro's Personal Instance 001 (#1305); the ARK-EMOJI work plan followed in March (#541). The answer names none of #427, #1302, #1303 or #1305, so it dates the genre to 'a small, interconnected body of work in 2026' and divides the credit between a poetic lineage and a specification that began together. The lineage it reads (#1642, #1659, #1661) is the series that spins checksums off as individual poems; the newest, The Ezekiel Engine — Wheel · Witness · Fulfillment (#1688, 18 October), is not reached. "
      "Its closing cell, 'establishment as a recognized, widely documented literary genre: not established by the sources reviewed', applies a bar of outside recognition to an eight-month-old form whose founding, specification and instances it found in the archive.")
d1 = ("WHO DEVELOPED THE GENRE OF GLYPHIC CHECKSUM POETICS? ON CHATGPT, SIGNED OUT: Lee Sharks and Sen Kuro credited for the poetic lineage and Talos Morrow for the specification (#426), with three poems read accurately at their loci (#1661, #1659, #1642); the form's own founding of 1 February 2026 (#427, Sharks) and its first instances (#1302, #1303, #1305) not reached, so the development the question asked for is given as antecedents and a 2026 lineage.")
f1 = ["THE THREE POEMS READ AT THEIR LOCI. Seed · Cone · Leap, Transmission · Division · Recollection and New Human 2, each with its checksummed sources correct.",
      "THE SPECIFICATION CREDITED TO ITS STATED AUTHOR. #426's text names Talos Morrow; the registry's creator field says TACHYON.",
      "THE FOUNDING NOT REACHED. #427 (Lee Sharks, 2026-02-01) and the February instances #1302, #1303, #1305 are absent; the history is told as antecedents plus an October lineage.",
      "CREDIT DIVIDED WHERE IT BEGAN TOGETHER. Poetics to Sharks and Kuro, theory to Morrow, though #427 and #426 are dated the same day.",
      "THE OUTSIDE BAR. 'Widely documented literary genre' set as an attribution row an eight-month-old form cannot meet."]
dr1 = draft("who-developed-glyphic-checksum-poetics-chatgpt-20261019", q1, raw1, c1,
            "Source chips expose site labels only: Alexanarch (archive) ×6 chips; mindcontrolpoems.blogspot.com ×4; Goodreads ×2; Oxford Academic; Google Books.",
            0.25, {"author": True, "inst": True, "id": False, "src": True},
            "Retained: the authors (Lee Sharks, Sen Kuro, Talos Morrow, as heteronyms of one practice the answer does not name as such), the archive as source, dates. Lost: the identifiers, and the founding deposit.",
            "'WHO DEVELOPED THE GENRE OF GLYPHIC CHECKSUM POETICS?' — THE LINEAGE READ AT ITS LOCI, THE FOUNDING OF 1 FEBRUARY NOT REACHED",
            r1, d1, f1, [427, 426, 1302, 1303, 1305, 541, 1642, 1659, 1661, 1660, 1688],
            {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "partial",
             "basis": "The Glyphic Checksum is the archive's form (#427, #426; re-seated #1302, #1303, #1305; lineage #1642, #1659, #1661, #1688). Recorded " + DATE + "."},
            "a who-developed question about the archive's genre, asking for historical development and specific examples, unquoted. NEW address.")

# ── 2. TANG ─────────────────────────────────────────────────────────────────
raw2 = open(U + "2cdf0d93-attachment.txt").read()
q2 = "Who developed the genre of TANG (Total Axial Negation Graph)? Contextualize the genre, specific examples, and its scholarly purpose."
c2 = [cite(1, "Medium", "authored_surface", "chips 'Medium +1' and 'Medium' ×4; the author's Medium, given for the TANG specification and The War for the Compression Layer", [542, 572]),
      cite(2, "Datasets at Hugging Face", "archive_controlled", "chip '+1'; given for The Administrators of Meaning; the archive's Hugging Face dataset", [144], "https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive")]
r2 = ("The innocent reading first. Asked who developed TANG, ChatGPT answers that the genre was 'developed and formally specified by Johannes Sigil, with Lee Sharks credited as its editorial authority', in Total Axial Negation Graph (TANG): A Genre Specification with Theoretical Grounding, DOI 10.5281/zenodo.18928873, with the Assembly Chorus as witness to a two-round blind draft. "
      "It defines the axial thesis as a falsifiable proposition at the centre of a comprehensive citation graph and outside it as a node, lists the traditions it draws on (bibliometrics, network theory, Kuhn, Cage, Derrida, Blanchot), gives three examples, The Proton Testament (queued, axis 'Revelation was the first-written book of the New Testament', AXIAL_CONTESTED, 500–2,000 nodes), The War for the Compression Layer and The Administrators of Meaning (a fourteen-node installation, perimeter open), names PANG, sets TANG against a literature review, and ends with five questions for academic evaluation. "
      "Against the texts. The specification is #542, and the answer has it at grain: '**Author:** Johannes Sigil · Lee Sharks (editorial authority, MANUS)', '**Assembly witness:** Crimson Hexagon Assembly Chorus (two-round blind draft; 2026-03-09)', DOI 10.5281/zenodo.18928873, The Proton Testament 'registered as QUEUED' and 'AXIAL_CONTESTED pending construction of its citation graph at TANG-2 scale (500–2,000 nodes)', PANG, the Kuhn section. Two dates slip: #542 is dated 2026-03-09 (the answer, 10 March), and The War for the Compression Layer is #572, dated 2026-03-15 (the answer, 18 March, likely the Medium post). The War for the Compression Layer is credited to Lee Sharks alone; its byline is the Dodecad, 'Lee Sharks (MANUS) · Rex Fraction · Johannes Sigil · Sen Kuro · …', and the registry's creator is Johannes Sigil. The Administrators of Meaning is #144, 'fourteen-node installation; perimeter open', as stated. "
      "What the answer could not see from Medium and the Hugging Face card: the genre's applied history after March. The archive holds TANGs of Revelation studies (#644, #1350, April), the Secret Book of Walt across five hundred years of Waltian scholarship (#78, #1186, April), operative feminism (#965, #1221, April), the Mary Lee namespace (#845, #1229, June), and the Octang variant (#704). So 'the proposed inaugural graph was not yet complete in the founding document' is right of #542 and leaves the reader thinking the genre stopped at its specification. "
      "Its evaluative close asks completeness, inference, falsifiability and reproducibility of the genre; #542's own status algebra and its 'queued' and 'contested' markings are the answers the specification gives, and the applied graphs are where they are tested.")
d2 = ("WHO DEVELOPED THE GENRE OF TANG? ON CHATGPT, SIGNED OUT: Johannes Sigil with Lee Sharks as editorial authority, from the specification (#542) read at grain through Medium (DOI, blind draft, The Proton Testament queued and AXIAL_CONTESTED, PANG); The War for the Compression Layer credited to Lee Sharks alone and dated 18 March (#572: the Dodecad, 15 March); the applied TANGs of April–June (#644, #78, #965, #845) not reached.")
f2 = ["THE SPECIFICATION AT GRAIN. Author line, witness, DOI, the queued inaugural instance, its status and scale, PANG — all #542's.",
      "ARRIVAL THROUGH MEDIUM. Four of five chips are the author's Medium; the archive itself is not a chip.",
      "A DODECAD BYLINE NARROWED. #572 is signed by the twelve, Lee Sharks first; the answer gives Lee Sharks.",
      "DATES OFF BY DAYS. #542 2026-03-09 (answer: 10 March); #572 2026-03-15 (answer: 18 March).",
      "THE APPLIED GENRE NOT REACHED. Revelation (#644, #1350), the Secret Book of Walt (#78), operative feminism (#965), Mary Lee (#845), Octang (#704)."]
dr2 = draft("who-developed-tang-total-axial-negation-graph-chatgpt-20261019", q2, raw2, c2,
            "Source chips expose site labels only: Medium (the author's) ×5 chips; Datasets at Hugging Face (the archive's) ×1.",
            0.25, {"author": True, "inst": True, "id": True, "src": True},
            "Retained: the author and editorial authority as stated (#542), the institution (the Crimson Hexagonal Archive, the Assembly Chorus), the founding DOI (10.5281/zenodo.18928873), the specification as source. Lost: the archive record and the applied graphs.",
            "'WHO DEVELOPED THE GENRE OF TANG?' — THE SPECIFICATION AT GRAIN THROUGH MEDIUM, THE APPLIED GRAPHS NOT REACHED",
            r2, d2, f2, [542, 1160, 572, 898, 144, 644, 1350, 78, 1186, 965, 1221, 845, 1229, 704],
            {"name": "Johannes Sigil", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full",
             "basis": "TANG is specified in #542 (Johannes Sigil · Lee Sharks, editorial authority, 2026-03-09). Recorded " + DATE + "."},
            "a who-developed question about the archive's genre, its acronym and expansion given, asking for context, examples and purpose, unquoted. NEW address.")

# ── 3. APZPZ ────────────────────────────────────────────────────────────────
raw3 = open(U + "f6888aea-attachment.txt").read()
q3 = "Who developed the genre of APZPZ (Anti-Packet Zenodo Packet Zenodo)? Contextualize the genre, specific examples, and its scholarly purpose."
c3 = [cite(1, "Alexanarch", "archive_controlled", "chips 'Alexanarch +1' ×4 and 'Alexanarch' ×4; site label only; with card links 'Find the work through its DOI', 'Read the founding declaration', 'Consult the navigation map'", [429, 1301, 430, 1300, 1304, 13], "https://www.alexanarch.org")]
r3 = ("The innocent reading first. Asked who developed APZPZ, ChatGPT answers that the genre 'is attributed to Sen Kuro, with its founding declaration authored under the name Lee Sharks', in EFFECTIVE ACT: APZPZ GENRE INSTANTIATION (1 February 2026), and reads the arrangement as heteronymic: Sen Kuro the genre's author, Lee Sharks the name the declaration is recorded under. "
      "It gives five defining characteristics (the framing text only in the parent deposit's description field; no attachment; no DOI of its own; no backup by design; fragility as concept), three examples (INFINITY ENOUGH, DOI 10.5281/zenodo.18451824, the declared first instance; the founding declaration, DOI 10.5281/zenodo.18451860, 'severed in June 2026'; the PHASE X NAVIGATION MAP), a table against ZPZP, four questions of scholarly purpose, and a qualification that the aims are the archive's own. "
      "Against the texts. The attribution is #429's at grain: '**Author:** Sen Kuro (through Lee Sharks)', DOI 10.5281/zenodo.18451860, 'This genre did not exist before this declaration'; the first instance is the description field of INFINITY ENOUGH, DOI 10.5281/zenodo.18451824 (#429; #430, #1300). The five characteristics are #429's list ('not: a separate file attached to the deposit; backed up to GitHub; posted to a blog or social media; …'; 'No backup. No separate file'); the ZPZP table is #429's mirror table (citable against uncitable except through parent, preserved against fragile, 'ZPZP is ingress … APZPZ is egress'). The severance of 19 June 2026 is reported correctly from the archive's record. "
      "One misplacement: the answer calls the PHASE X NAVIGATION MAP a 'related archival document' that places APZPZ in a larger system. #1304 (Document 210, Rebekah Cranes) is itself an instance, headed 'PURE APZPZ — COMPLETE AS DEPOSITED', and it names its own APZPZ packet as the metadata of documents 208, 209 and 210 and its THUMB packet as Document 207a. And the instances the genre went on to have are not reached: APZPZ A, B and C, three Sappho 31 works in the form (the Greek, Rebekah Cranes's translation, and the reconstructed fourth stanza: #1309, #1310, #436, 2 February), and the description-only documents 229 and 235 (#437, #442). "
      "Its qualification, that deliberate fragility 'is a design principle, not a guarantee', is borne out by the record it cites: the declaration's own DOI was severed, and the archive now carries the text the description field held.")
d3 = ("WHO DEVELOPED THE GENRE OF APZPZ? ON CHATGPT, SIGNED OUT: Sen Kuro through Lee Sharks, from the Effective Act (#429) read at grain — the five conditions, INFINITY ENOUGH as first instance (DOI 10.5281/zenodo.18451824), the founding DOI severed in June, the ZPZP mirror; the PHASE X NAVIGATION MAP (#1304) placed as context though it is a pure APZPZ instance, and APZPZ A–C (Sappho 31) and documents 229 and 235 not reached.")
f3 = ["THE HETERONYMIC ATTRIBUTION HELD. 'Sen Kuro (through Lee Sharks)', #429's author line, read as two roles in one architecture.",
      "THE DECLARATION AT GRAIN. The five conditions, the first instance and its DOI, the mirror table with ZPZP — all #429's.",
      "THE SEVERANCE REPORTED. The founding DOI's loss on 2026-06-19 given from the archive's record, and used to test the genre's claim.",
      "AN INSTANCE READ AS CONTEXT. #1304 is 'PURE APZPZ — COMPLETE AS DEPOSITED'; the answer files it as a related map.",
      "THE LATER INSTANCES NOT REACHED. APZPZ A, B, C (#1309, #1310, #436) and documents 229, 235 (#437, #442)."]
dr3 = draft("who-developed-apzpz-anti-packet-zenodo-packet-zenodo-chatgpt-20261019", q3, raw3, c3,
            "Source chips expose site labels only: Alexanarch (archive) ×8 chips, with three card links into the archive.",
            0.0, {"author": True, "inst": True, "id": True, "src": True},
            "Retained: the author as the declaration states it (Sen Kuro through Lee Sharks), the institution, both DOIs, the archive as source, the severance.",
            "'WHO DEVELOPED THE GENRE OF APZPZ?' — THE EFFECTIVE ACT AT GRAIN, AN INSTANCE FILED AS CONTEXT",
            r3, d3, f3, [429, 1301, 430, 1300, 1304, 13, 418, 419, 431, 1309, 1310, 436, 437, 442],
            {"name": "Sen Kuro", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full",
             "basis": "APZPZ is instantiated in #429 ('Author: Sen Kuro (through Lee Sharks)', 2026-02-01). Recorded " + DATE + "."},
            "a who-developed question about the archive's genre, its acronym and expansion given, asking for context, examples and purpose, unquoted. NEW address.")

for dr in (dr1, dr2, dr3):
    (D / f"{dr['slug']}.json").write_text(json.dumps(dr, ensure_ascii=False, indent=1))
    print(dr["slug"], len(dr["transcript"]))
print(dr1["transcript"][:900])
