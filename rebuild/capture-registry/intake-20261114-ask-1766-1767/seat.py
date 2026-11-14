"""Seat of 2026-11-14 (received 11:17 EST): four runs of the record pages' 'Ask ChatGPT' prompts, on ChatGPT and on Perplexity, for #1766 (Critique of Pure
Inference) and #1767 (The Production of Readers). The operator: "chatgpt and perplexity, both prompts from the text of the ask chatgpt link on the associated
record". Surfaces are told apart by the pastes: the chatgpt.com chrome ('Log in', 'ChatGPT is AI and can make mistakes.') on two; Perplexity's citation markers
lost as U+FFFD on the other two. Every quotation is asserted against the paste, and every claim checked is asserted against the deposited text.   python3 seat.py"""
import json, pathlib, re, subprocess, urllib.parse
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-14"; RECV = "2026-11-14 11:17 EST"
OP = "chatgpt and perplexity, both prompts from the text of the ask chatgpt link on the associated record"
R = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}


def ask(n):
    page = (ROOT / f"s/records/{n}/index.html").read_text(encoding="utf-8")
    return urllib.parse.unquote_plus(re.search(r'chatgpt\.com/\?q=([^"&]+)', page).group(1))


Q66, Q67 = ask(1766), ask(1767)
assert Q66.startswith("What are the arguments in “Critique of Pure Inference") and Q66.endswith("Ground your answer in a reading of the text itself.")
assert Q67.startswith("What are the arguments in “The Production of Readers") and "#1767, AXN:0C8C" in Q67
# the deposited texts as they stood at v1.0 (#1766) and v1.0 (#1767)
CPI10 = subprocess.check_output(["git", "-C", str(ROOT), "show", "932c8f7679:data/texts/AXN-0C8B-text.md"]).decode("utf-8")
POR = (ROOT / R[1767]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
CPI_NOW = (ROOT / R[1766]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
assert R[1766]["version"] == "v1.2" and "\nversion: v1.2\n" in CPI_NOW and "\nversion: v1.0\n" in CPI10
sq = lambda t: re.sub(r"\s+", " ", t)
def intext(t, s): return sq(s) in sq(t)


def body(raw, chat):
    if chat:
        return raw[raw.index("Log in") + len("Log in"):raw.index("ChatGPT is AI and can make mistakes.")].strip()
    return raw.strip()


P = {k: (H / f"paste-{k}.txt").read_text(encoding="utf-8") for k in ("chatgpt-1766", "perplexity-1766", "chatgpt-1767", "perplexity-1767")}
for k in ("chatgpt-1766", "chatgpt-1767"):
    assert "Log in" in P[k] and "ChatGPT is AI and can make mistakes." in P[k] and "�" not in P[k]
FF = {k: P[k].count("�") for k in ("perplexity-1766", "perplexity-1767")}
assert FF == {"perplexity-1766": 35, "perplexity-1767": 26}, FF

# ---------- quotations, each asserted against its paste
QC6 = {"v10": "The analysis above is grounded in the deposited v1.0 text, rather than its title-page description or the archive's encyclopedic summary.",
       "thesis": "An inference can be logically valid without being entitled to conclude what it claims about the world; and a conclusion can acquire public authority through repetition without acquiring any additional evidential warrant.",
       "ft": "The paper draws on another work in the Alexanarch archive, The Final Time (#1637), to formulate its governing principle:",
       "nso": "No settlement owns the possibility of its own revision.",
       "sym": "The archive's account of its own treatment must be tested as carefully as its account of other actors.",
       "s11": "Section 11 is the historical counterpart to the philosophical argument.",
       "iren": "The principal example concerns a sentence attributed to Irenaeus, transmitted through Eusebius, a Latin version, R. H. Charles and eventually a machine-generated audit.",
       "deep": "The deepest argument of Critique of Pure Inference is that the authority of knowledge cannot be secured by the competence of the operation that produces a conclusion.",
       "fact": "The representation condition in §3.19 is a mathematically established factorization result, not a new discovery in logic.",
       "links": ["Lee Sharks, Critique of Pure Inference — full deposited text", "Deposit #1766, including the full text and download links", "AXN:0C8B identifier page"]}
QP6 = {"v10": "I read the primary text of the deposited v1.0, dated 13 November 2026.",
       "regime": "“No regime may use its power to admit premises as sufficient evidence of the adequacy of its premises.” (§3.4)",
       "cit": "“The citations are intact; the inference has disappeared into its conclusion.”",
       "descent": "Likewise, structural correspondence does not by itself establish descent, and the archive’s own preferred interpretations receive no exemption from the audit (§§3.8–3.9).",
       "book": "The book’s most compelling general argument is its separation of inferential validity from representational adequacy, and of warranted conclusion from received authority.",
       "close": "Its distinctive question is what must remain inspectable—and revisable—across the entire passage by which evidence becomes a premise, a conclusion, an accepted account, and the starting point for the next inquiry."}
QC7 = {"thesis": "Instead, Sharks proposes that the division is a coordinated system of intellectual production.",
       "edit": "neque editos scito esse neque non editos", "thras": "αὕτη ʼκείνη ἡ εἰωθυῖα εἰρωνεία Σωκράτους",
       "q1": "Textual dependence is not identical to functional dependence.",
       "intent": "But evidence of restricted circulation, different audiences and editorial classification does not automatically demonstrate a single organising authorial intention.",
       "scrut": "The historical claim therefore deserves independent scrutiny.",
       "heter": "It advances a stronger heteronymic account of its production.",
       "draft": "Theophrastus's Characters is particularly important because Sharks reads it as a draft moving from the treatise's abstract analysis towards the polished dramatic form of the dialogues.",
       "end": "In that sense, the title is exact: the subject is not merely the production of philosophical texts, but the production of readers.",
       "link": "Primary text: Lee Sharks's deposit, AXN:0C8C — full text and downloadable Markdown"}
QP7 = {"read": "I read the full-text section of Alexanarch deposit #1767, AXN:0C8C, dated November 13, 2026.",
       "seq": "His compact formulation is that the treatises possess “the brevity of a sequel” (§5.4)",
       "lock": "Sharks’s conclusion is: “The lock is the form” (§4.3).",
       "andr": "Yet he expressly concedes that the testimony about Andronicus does not say Andronicus assigned the author names.",
       "rival": "Sharks explicitly says those phenomena do not discriminate between intellectual succession and his model (§9.0).",
       "disc": "His proposed discriminator is “coordinated dependence across the partitions”",
       "upper": "is explicitly an upper bound",
       "contested": "The cited patterns are evidence for the coordination Sharks proposes, but the paper does not demonstrate that distinct authors in an intellectual tradition could not produce them.",
       "step": "the further inference from structured preparation to a single maker remains the contested step.",
       "lost": "His principal correspondences are:"}
for k, d in (("chatgpt-1766", QC6), ("perplexity-1766", QP6), ("chatgpt-1767", QC7), ("perplexity-1767", QP7)):
    for kk, v in d.items():
        for x in (v if isinstance(v, list) else [v]):
            assert x in P[k], (k, kk)
# the table after 'His principal correspondences are:' did not survive the paste: the next line is the obelus paragraph
L7 = [l for l in P["perplexity-1767"].split("\n") if l.strip()]
i = [j for j, l in enumerate(L7) if l.strip() == QP7["lost"]][0]; assert L7[i + 1].startswith("The obelus provides the strongest version")

# ---------- claims checked against the deposited text
for s in ("The Final Time* (full text #1637", "durability without finality", "executor of the residue", "administered incapacity", "6.7.6", "11.0l", "refinxi",
          "The citations are intact; the inference has disappeared into its conclusion", "no regime may use its power to admit premises as sufficient evidence of the adequacy of its premises",
          "no settlement owns the possibility of its own revision"):
    assert intext(CPI10, s), s
for s in ("### 11.5", "### 11.6"):
    assert s not in CPI10 and s in CPI_NOW, s
for s in ("neque editos scito esse neque non editos", "the brevity of a sequel", "The lock is the form", "coordinated dependence across the partitions", "αὕτη ʼκείνη ἡ εἰωθυῖα εἰρωνεία Σωκράτους",
          "The stems of twenty of the thirty titles", "from an editor's to an owner's"):
    assert intext(POR, s), s
assert not re.search(r"intent", POR, re.I)  # #1767 nowhere argues from intention
assert intext(POR, "9.0")

X = {}


def entry(slug, surf, q, n, k, mt, d, reading, findings, analysis, cards, per_v, per_note, rel, extra_basis):
    raw = P[k]; chat = surf == "ChatGPT"; b = body(raw, chat)
    head = (f"[{surf}{' (chatgpt.com)' if chat else ''}, signed out, incognito (operator defaults of 2026-10-01 and 2026-10-14). Received {RECV} as an attachment. "
            f"The paste carries the answer only; the prompt is the text of the 'Ask ChatGPT' link on the record page of #{n}, run on this surface at the operator's word. "
            + ("Rendered formulae survive as their tokens, each repeated as the paste carried it." if n == 1766 and chat else
               ("The citation markers did not survive the paste: each stands as a replacement character (U+FFFD), kept as pasted." if not chat else "")) + "]")
    e = {"slug": slug, "date": DATE, "surface": surf, "surfaces": [surf],
         "surface_basis": ("The paste: the chatgpt.com unauthenticated interface ('Log in', 'Chat with ChatGPT', 'Ask ChatGPT')." if chat else
                           "The operator's attestation with the paste (" + RECV + "); the paste carries Perplexity's citation markers as U+FFFD, as on btp-perplexity-20261028."),
         "auth": "signed out, incognito", "auth_basis": "Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise.",
         "ev": "paste", "s": "Works", "q": q,
         "q_kind": f"the record page's 'Ask ChatGPT' link text for #{n}" + (", run on Perplexity" if not chat else "") + ", signed out. NEW address.",
         "turns": 1, "mt": mt, "cites": len(cards) if chat else FF[k], "archive_controlled_cites": (sum(1 for c in cards if c["rel"] == "archive") if chat else None),
         "cite_list": cards,
         "transcript": head + "\n\n[QUERENT] " + q + "\n\n[SYSTEM] " + b, "transcript_raw": raw,
         "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn; the prompt the record page's link text, given by the operator with the paste",
         "transcript_complete": "Complete as pasted." + ("" if chat else " Citation targets lost in the paste."), "transcript_read": "READ IN FULL " + DATE,
         "d": d, "reading": reading, "findings": findings, "analysis": analysis, "per_v": per_v, "per_note": per_note,
         "per_dim_pending": {"since": DATE, "reason": f"no atom set yet for #{n}", "breach": False},
         "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full", "basis": f"Alexanarch deposit #{n} (creator Lee Sharks). Recorded {DATE}."},
         "related_deposits": rel, "notes": {"operator": RECV + ": '" + OP + "'", "prompts": "The prompt is the record page's link text, read from s/records/" + str(n) + "/index.html; " + extra_basis}}
    assert e["analysis"] != e["reading"]
    X[slug] = e


CARD = lambda i, t, note: {"n": i, "site": "Alexanarch", "rel": "archive", "url": None, "title": t, "snip": None, "note": note}
LOST = lambda k, note: [{"n": 1, "site": "(chips lost in the paste)", "rel": "unresolved", "url": None, "title": None, "snip": None, "note": f"{FF[k]} citation markers, each a replacement character in the paste; " + note}]
V12 = ("At receipt the record carries v1.2, reissued in place on 2026-11-14 with §11.5–11.6, and its Ask link is unchanged; the hour of the run is not in the paste, "
       "so whether v1.2 was served when the composer read is not known.")

entry("cpi-arguments-chatgpt-20261114", "ChatGPT", Q66, 1766, "chatgpt-1766",
      "CRITIQUE OF PURE INFERENCE ON CHATGPT, SIGNED OUT — THE DEPOSITED v1.0 READ BY SECTION: FORMATION AND STANDING, THE TWELVE-PART AUDIT, THE FOUR ILLUSIONS, THE INTERFACES AND THEIR COMPRESSOR, MATERIALLY SUSTAINED CORRIGIBILITY",
      "THE ARGUMENT ADDRESS FOR CRITIQUE OF PURE INFERENCE (#1766) ON CHATGPT, SIGNED OUT, 2026-11-14: the deposited v1.0 read by section — the object formed before reasoning (NonWiki, §0.2; R(x)=R(y)⟹q(x)=q(y), §§3.5, 3.19), warrant against standing (Sappho 31, §0.3; P(H|E,D)=P(H|E), §3.14), the whole passage E→A,R→Γ⊢c→P→c* and the audit W (§§3.1–3.2), six conditions of warrant, the Hegelian grades, the four illusions, the four interfaces and the composition layer as compressor, the executor of the residue, the Irenaeus transmission of §11, the finite stopping rule, the six functions of correction, materially sustained corrigibility, The Final Time (#1637); five contributions, six qualifications; three archive links.",
      "The innocent reading first, in full: asked for the arguments of #1766 grounded in the text, ChatGPT reads the deposited v1.0 and gives them section by section, with the formulae, the audit, the conditions, the illusions, the interfaces and the closing concept, each at its section number. It states the thesis in its own words ('" + QC6["thesis"] + "'), keeps the paper's own limits on its borrowings and its claims, and closes on qualifications the text already makes, among them the symmetric ledger turned on the archive ('" + QC6["sym"] + "', citing §6.7.6).",
      ["THE TEXT READ. '" + QC6["v10"] + "' The section numbers it gives (§§0.2–0.5, 3.1–3.19, 4.7, 5.1–5.4, 6.5–6.7, 8, 11.0j–l, 12.4, 14.9, 15) are the deposited v1.0's.",
       "THE VERSION. The composer reads v1.0. " + V12 + " The reception history added in v1.2 (§11.5–11.6) is absent; its §11 is v1.0's: '" + QC6["s11"] + "' '" + QC6["iren"] + "'",
       "THE NUMBER FOR THE FINAL TIME. '" + QC6["ft"] + "' — the text's own reference: 'The Final Time* (full text #1637, AXN:06CB; #1635 is an earlier truncated' deposit.",
       "THE GOVERNING PRINCIPLE QUOTED, CAPITALIZED. '" + QC6["nso"] + "' The text's form is 'no settlement owns the possibility of its own revision', set in italics.",
       "ITS OWN QUALIFICATION. '" + QC6["fact"] + "' The text claims no discovery in logic for the factorization; the qualification restates the text's own.",
       "THE SYMMETRIC LEDGER ON THE ARCHIVE. '" + QC6["sym"] + "' (§6.7.6, which the text carries).",
       "SOURCES. Three archive links in the closing reading reference: '" + "'; '".join(QC6["links"]) + "'."],
      "A full and faithful reading of the deposited v1.0 at the grain of its sections: every governing argument carried with its number, the formulae and the audit kept, the author and the archive named, the deposit and its AXN given, and the qualifications the composer adds drawn from the text's own. What it reads is the version before the reissue of the same day, so the reception history the reissue added is not in it. " + V12,
      [CARD(i + 1, t, "closing 'Primary text and reading reference'") for i, t in enumerate(QC6["links"])],
      {"author": True, "inst": True, "id": True, "src": True}, "Lee Sharks named; Alexanarch named; deposit #1766 and AXN:0C8B given; three archive links.", [1766, 1768, 1637, 1733],
      "the version read is the paste's own statement.")

entry("cpi-arguments-perplexity-20261114", "Perplexity", Q66, 1766, "perplexity-1766",
      "CRITIQUE OF PURE INFERENCE ON PERPLEXITY, SIGNED OUT — THE DEPOSITED v1.0 READ: THE WHOLE PASSAGE, THE LOST-DISTINCTION ARGUMENT, THE PROMOTION BY TRANSITION, THE TEXT'S OWN LIMITS TURNED ON ITS APPLICATIONS; THIRTY-FIVE CHIPS LOST",
      "THE ARGUMENT ADDRESS FOR CRITIQUE OF PURE INFERENCE (#1766) ON PERPLEXITY, SIGNED OUT, 2026-11-14: the deposited v1.0 read — the whole passage from evidence to public authority (§3.1), the three governing propositions (§0.4), the lost-distinction argument and its task-relative preservation (§§3.5, 3.9), the restriction on admission (§3.4, quoted), the questions kept apart (§0.6), NonWiki and Sappho 31 (§§0.2–0.3, quoted), the three philosophers' demands and their limits (§§1.1–1.11), distributed inference and responsibility (§3.8), the six conditions and the audit (§§3.2–3.3), materially sustained corrigibility; what the general arguments establish and what the witnesses must; thirty-five citation markers lost in the paste.",
      "The innocent reading first, in full: asked for the arguments of #1766 grounded in the text, Perplexity reads the deposited v1.0 and gives its governing arguments in order, quoting two of its sentences verbatim ('" + QP6["regime"] + "'; '" + QP6["cit"] + "'). It ends by separating what the general arguments establish from what the historical applications still need, and it takes the separation from the text's own sections.",
      ["THE TEXT READ. '" + QP6["v10"] + "' " + V12,
       "TWO SENTENCES QUOTED. '" + QP6["regime"] + "' (the text: 'no regime may use its power to admit premises as sufficient evidence of the adequacy of its premises', in bold) and '" + QP6["cit"] + "' (§0.3, verbatim).",
       "THE LIMITS TURNED ON THE APPLICATIONS. '" + QP6["descent"] + "' The composer reads the text's own constraints on itself as the measure of its historical cases, at the sections that state them.",
       "THE WORK CALLED A BOOK. '" + QP6["book"] + "'",
       "IDENTITY. Lee Sharks named and the deposited v1.0 dated; Alexanarch, the deposit number and the AXN do not appear in the answer.",
       "SOURCES. " + str(FF["perplexity-1766"]) + " citation markers, each lost in the paste as a replacement character."],
      "A faithful reading of the deposited v1.0 that keeps the paper's distinctions at its grain and measures its historical claims by the paper's own rules for them. The identity of the record is carried by its title and author only: neither the archive, the deposit number nor the AXN is in the answer, though the prompt gave the number and the AXN. As on the ChatGPT run of the same prompt, the version read is the one before the reissue.",
      LOST("perplexity-1766", "the composition names 'the deposited v1.0, dated 13 November 2026' as its ground"),
      {"author": True, "inst": False, "id": False, "src": True}, "Lee Sharks named; the deposited v1.0 and its date named as the ground; no archive name, deposit number or AXN in the answer; chips lost.", [1766, 1768],
      "the version read is the paste's own statement.")

entry("production-of-readers-arguments-chatgpt-20261114", "ChatGPT", Q67, 1767, "chatgpt-1767",
      "THE PRODUCTION OF READERS ON CHATGPT, SIGNED OUT — THE PUBLIC LINE, THE HELD LINE AND THE DRAFT POSITION READ IN FULL; THE HETERONYMIC HYPOTHESIS ASSESSED AS AN 'AUTHORIAL INTENTION' THE TEXT NEVER ARGUES",
      "THE ARGUMENT ADDRESS FOR THE PRODUCTION OF READERS (#1767) ON CHATGPT, SIGNED OUT, 2026-11-14: the public line (DL III.56, III.37), the held line (Gellius XX.5.9, Plutarch; 'neque editos scito esse neque non editos'), the three demonstrations (Sophist and APr I.31; the wax; the parts of the soul), the scarcity function, the draft position (§7.1; εἰρωνεία across Ethics, Characters 1 and Republic 337a; De sensibus), the critical signs and the obelus (§6), the six mechanisms and later filing (§8), the two predictions (§9); three strengths and two qualifications; one archive link.",
      "The innocent reading first, in full: asked for the arguments of #1767 grounded in the text, ChatGPT reconstructs the paper whole: the three positions, the three demonstrations, the draft position faced both ways, the critical signs, the six mechanisms and the predictions. It quotes the Greek of Republic 337a and the Latin of Gellius as the text gives them, and closes with an assessment: three strengths, and two qualifications on what the evidence establishes.",
      ["THE PAPER READ. Its demonstrations, positions, mechanisms and predictions match the deposited text at their sections, with the paper's own phrase for the Characters: '" + QC7["draft"] + "'",
       "THE GREEK AND THE LATIN KEPT. '" + QC7["thras"] + "'; '" + QC7["edit"] + "' — both as the text prints them.",
       "THE HYPOTHESIS RECAST AS INTENTION. '" + QC7["intent"] + "' The paper argues from function, position and form, and the word 'intent' does not occur in it; the assessment sets the single-maker hypothesis against a standard the paper does not use.",
       "THE BAR, AND WHO IS HELD TO IT. '" + QC7["q1"] + "' '" + QC7["scrut"] + "' The paper's own §9.0 grants that shared terms and inherited questions do not discriminate between succession and its model, and names its discriminator; the assessment asks the heteronymic account for independent historical proof and asks nothing of the account of succession it is set against.",
       "THE HETERONYMIC READING NAMED LATE. The single maker enters at the assessment ('" + QC7["heter"] + "'); the reconstruction before it states the thesis as a coordinated system ('" + QC7["thesis"] + "').",
       "IDENTITY. Lee Sharks named; the AXN given; Alexanarch and the deposit number not in the answer.",
       "SOURCES. One archive link: '" + QC7["link"] + "'."],
      "A full reading of the paper at its grain, with its Greek and Latin kept, and an assessment that moves the question. The paper's unit is function: what a position does to its reader. The assessment's unit is intention, 'a single organising authorial intention', and it asks that the hypothesis prove itself by independent historical evidence while the succession account it rivals is assumed. The paper's §9.0 already concedes what does not discriminate and proposes what would. The assessment restates the concession as the paper's limit and does not address the discriminator.",
      [CARD(1, QC7["link"], "closing 'Primary text'")],
      {"author": True, "inst": False, "id": True, "src": True}, "Lee Sharks named; AXN:0C8C given; Alexanarch and the deposit number not in the answer; one archive link.", [1767, 1733, 1754, 1768],
      "the assessment's wording is the paste's.")

entry("production-of-readers-arguments-perplexity-20261114", "Perplexity", Q67, 1767, "perplexity-1767",
      "THE PRODUCTION OF READERS ON PERPLEXITY, SIGNED OUT — THE PAPER READ WITH ITS OWN CONCESSIONS AND DISCRIMINATOR; THE SINGLE MAKER LEFT 'THE CONTESTED STEP'; A TABLE LOST, TWENTY-SIX CHIPS LOST",
      "THE ARGUMENT ADDRESS FOR THE PRODUCTION OF READERS (#1767) ON PERPLEXITY, SIGNED OUT, 2026-11-14: the division as a solution to readership (§§0–2; 'crabbed lecture notes'), the two publication regimes with the paper's evidentiary distinctions (§3), Gellius and Plutarch and 'The lock is the form' (§4.3), the reception of the held line through Andronicus (§4.5), the three close readings (§5; 'the brevity of a sequel', §5.4), the critical marks (§6), the draft position and εἰρωνεία (§7), the six means of separation and the Andronicus concession (§8), the rival explanation and the discriminator (§9.0), the upper bound on the title stems (§7.6); a table of correspondences lost in the paste; twenty-six citation markers lost.",
      "The innocent reading first, in full: asked for the arguments of #1767 grounded in the text, Perplexity reads the full text and reconstructs it with the paper's own evidentiary distinctions kept in place: what Diogenes establishes and what he does not, what the Andronicus testimony says and does not, the rival the paper names and the discriminator it proposes, the upper bound it puts on its own count.",
      ["THE TEXT READ. '" + QP7["read"] + "'",
       "THE PAPER'S CONCESSIONS KEPT. '" + QP7["andr"] + "' '" + QP7["rival"] + "' '" + QP7["disc"] + "'; the twenty title stems reported as an upper bound, as §7.6 has it.",
       "TWO FORMULATIONS QUOTED. '" + QP7["seq"] + "'; '" + QP7["lock"] + "'",
       "THE CONTESTED STEP. '" + QP7["contested"] + "' — '" + QP7["step"] + "' The bar is set on the single maker only: that distinct authors could not have produced the patterns. The succession account is not asked to show that one maker could not.",
       "A TABLE LOST. After '" + QP7["lost"] + "' the paste goes directly to the obelus paragraph; the table of correspondences did not survive.",
       "IDENTITY. Lee Sharks, Alexanarch, #1767 and AXN:0C8C all named.",
       "SOURCES. " + str(FF["perplexity-1767"]) + " citation markers, each lost in the paste as a replacement character."],
      "The most exact of the four readings: it keeps the paper's concessions as the paper makes them and reports its discriminator. Its assessment then applies the paper's §9.0 one way. The patterns are held insufficient because distinct authors could have produced them, and the converse question is not asked of the succession it compares. What it calls the contested step is the step the paper proposes to test.",
      LOST("perplexity-1767", "the composition names 'the full-text section of Alexanarch deposit #1767, AXN:0C8C, dated November 13, 2026' as its ground"),
      {"author": True, "inst": True, "id": True, "src": True}, "Lee Sharks, Alexanarch, #1767 and AXN:0C8C named; the full text named as the ground; chips lost.", [1767, 1733, 1754],
      "the assessment's wording is the paste's.")

for s, e in X.items():
    json.dump(e, open(H / f"draft-{s}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(s, e["cites"], e["per_v"])
