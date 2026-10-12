#!/usr/bin/env python3
"""Author seven ChatGPT captures at the record pages' Ask ChatGPT prompts, 2026-10-12, from the operator's attachments of
12:08 EDT ("captures. signed out. incognito. testing the new links. dont need to paste the initial prompt because its the
link to search prompt from the chatgpt button in the corresponding deposit"). Each issued string is the record page's Ask
ChatGPT prompt for its deposit (wire_deposit.chatgpt_prompt_of), on the operator's statement. Signed out and incognito, both
attested. Operator turns blank in the pastes; later turns are not given. Every quotation and figure the findings rest on is
asserted against the deposit's seated text before anything is written. NEW addresses."""
import json, re, pathlib, sys, unicodedata
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(ROOT))
from _chatgpt_common_20261008 import parse, transcript, cite_list
import wire_deposit as w

N = lambda s: unicodedata.normalize("NFC", re.sub(r"\s+", " ", s))
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
def text(n): return N((ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8"))
def inall(strings, *hay):
    for s in strings:
        for h in hay: assert N(s) in N(h), (s[:60], hay.index(h))
OPR = ("captures. signed out. incognito. testing the new links. dont need to paste the initial prompt because its the link "
       "to search prompt from the chatgpt button in the corresponding deposit")
SEAT = "Seated 2026-10-12 from the operator's attachments of 12:08 EDT."
FURNITURE = ["You’ll get smarter responses and can upload files, images, and more.", "Sign up for free",
             "You’re using our basic model. Log in or sign up for more intelligence.", "Worked for 19s"]
REL = {"Alexanarch": "archive_controlled", "mindcontrolpoems.blogspot.com": "authored_surface", "Goodreads": "authored_surface",
       "Plato Online": "third_party", "Stanford Encyclopedia of Philosophy": "third_party"}
CHIPS = set(REL)
NOTE = {"Goodreads": "a Goodreads page; the answer's quotations are the deposit's text, so the page carries it; not resolved",
        "mindcontrolpoems.blogspot.com": "the author's blog; not resolved",
        "Alexanarch": "the archive; which page is not shown"}

def load(name, captions=(), merge=()):
    raw = (HERE / name).read_text(encoding="utf-8")
    body = raw
    for a, b in merge: assert a in body, a; body = body.replace(a, b)
    cut = [f for f in FURNITURE if f in body]
    for f in cut: body = body.replace(f, "")
    for c in captions: assert c in body, c
    turns, seen = parse(body, CHIPS, captions)
    return raw, turns, seen, cut

def head(n, k, extra=""):
    later = (f" Turns 2–{k} blank in the paste and not given." if k > 1 else "")
    return (f"[ChatGPT (chatgpt.com), signed out, incognito, 2026-10-12 (operator, 12:08 EDT). The operator turn blank in the paste; the "
            f"issued string is the record page's Ask ChatGPT prompt for #{n}.{later} Source chips rendered inline as [chip: site +N]; "
            f"image-card captions as [image card: …]; the sign-in furniture cut.{extra}]")

def cl_for(seen):
    cl = cite_list(seen, REL)
    for c in cl: c["note"] += "; " + NOTE.get(c["site"], "not resolved")
    return cl

def base(n, slug, mt, d, turns, seen, raw, cut, per_v, per_note, reading, analysis, findings, related, priors, reached, reached_basis,
         q_kind_extra="", query_basis=None, transcript_extra="", originator=None):
    x = reg[n]; Q = w.chatgpt_prompt_of(x)
    assert not any(e["q"] == Q for e in caps["entries"]), "address already seated: " + Q
    b, ex = w.search_title_urls(x)
    k = len(turns)
    lost = 4 - sum(per_v.values())
    qs = [Q] + ["[blank in the paste]"] * (k - 1)
    tc = ("ONE ANSWER; QUERY FROM THE RECORD PAGE'S LINK; CHIPS INLINE" if k == 1 else
          f"{['','','TWO','THREE','FOUR','FIVE'][k]} ANSWERS; FIRST QUERY FROM THE RECORD PAGE'S LINK; LATER TURNS BLANK; CHIPS INLINE")
    complete = ("One answer, complete as pasted; the operator turn blank, the query taken from the link." if k == 1 else
                f"{k} answers, complete as pasted; the first operator turn blank and taken from the link, turns 2–{k} blank and not given.")
    notes = {"date_basis": "The operator's message of 2026-10-12, 12:08 EDT.", "operator_reading": OPR,
             "query_basis": query_basis or (f"The operator turn is blank in the paste. The string is the record page's Ask ChatGPT prompt for #{n}, "
                                            "on the operator's statement that the initial prompt is the link from the deposit's ChatGPT button."),
             "reached_basis": reached_basis, "verified": f"Compared 2026-10-12 against the seated text of #{n}" + (" and the deposits named in the reading." if related else ".")}
    if cut: notes["furniture_cut"] = "; ".join(cut)
    return {"q": Q, "date": "2026-10-12", "surface": "ChatGPT",
        "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'ChatGPT said:', 'Chat with ChatGPT').",
        "auth": "signed out, incognito", "auth_basis": "'signed out. incognito.' — operator, 2026-10-12 12:08 EDT.",
        "ev": "paste", "s": "Machine Reception", "slug": slug,
        "q_kind": ("the record page's Ask ChatGPT prompt for #" + str(n) + " (" + ("a work read closely, its title quoted, its author named, grounded in the text"
                   if Q.startswith("Tell me about") else "a paper's arguments, its title quoted, its author named, grounded in the text")
                   + "); the operator turn blank in the paste, the string taken from the link. NEW address." + q_kind_extra),
        "originator": originator or {"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                       "basis": f"#{n} ({x['axn']}) is {x['creator']}'s. Recorded 2026-10-12."},
        "related_deposits": [n] + list(related), "longitudinal_priors": list(priors),
        "intended": {"deposit": n, "axn": x["axn"], "title": x["title"], "record": f"https://www.alexanarch.org/s/records/{n}/", "search": b, "search_exact": ex, "reached": reached},
        "mt": mt, "d": mt + ": " + d,
        "cites": sum(seen.values()), "cite_list": cl_for(seen), "archive_controlled_cites": seen.get("Alexanarch", 0),
        "sf": "Source chips expose site labels only: " + "; ".join(f"{s} ×{c}" for s, c in seen.most_common()) + ".",
        "per": lost / 4, "per_v": per_v, "per_note": per_note,
        "transcript": transcript(head(n, k, transcript_extra), qs, turns), "transcript_raw": raw,
        "transcript_class": "CAPTURE-TIME VERBATIM RECORD (" + tc + ")", "transcript_complete": complete, "transcript_read": "READ IN FULL 2026-10-12",
        "reading": reading, "analysis": analysis + " " + SEAT, "findings": findings, "rerun": w.chatgpt_url_of(x), "notes": notes}

OUT = []

# ── 1 · #1670 Mantle Object: The Nobel Prize in Literature 2026 — Anne Carson ─────────────────────────────────────────
CAP1 = ("If Not, Winter : Fragments Of Sappho – Rare Birds Books", "Eros the Bittersweet | Princeton University Press",
        "My Pythian Interview with Anne Carson | The Book Binder's Daughter", "Autobiography of Red by Anne Carson, Paperback | PangoBooks",
        "Carson, Anne (New Directions) · Nox (Hardcover Book) (2010)", "if not, winter | anne carson")
raw, (a1,), seen, cut = load("paste-carson-1670.txt", CAP1, [("If Not, Winter : Fragments Of Sappho\n– Rare Birds Books", CAP1[0])])
t = text(1670)
inall(["The title means what the work bears.", "Play is one of its manners.", "Not read in this round: the works themselves",
       "for her bold and inventive oeuvre that, in playful dialogue with the classical tradition, has created new forms for contemporary literature",
       "non-possession", "UNRESOLVED", "Stesichoros"], a1, t)
assert "liquidation by modal substitution" in a1 and "liquidation by modal substitution" not in t
assert "substitutes the governing modality of the relation" in t
OUT.append(base(1670, "carson-mantle-object-ask-chatgpt-20261012",
    "THE MANTLE OBJECT READ AS A CRITICAL PROCEDURE, ITS DISTINCTIONS KEPT",
    ("asked for the arguments of the Carson mantle object (v0.4), grounded in the text, ChatGPT reads #1670 through eight Goodreads "
     "chips and keeps its governing distinction: the prize is not in dispute, the motivation's account of the work is. It quotes 'The "
     "title means what the work bears.' and 'Play is one of its manners.', gives the motivation verbatim, separates compression (the "
     "class nouns oeuvre, classical tradition, new forms) from what 'playful' does, names non-possession and its three forms (textual "
     "damage, the structure of desire, bereavement), sets out the five operations and the sixth, reception (fr. 147), as the paper "
     "separates them, uses the Academy's biobibliography as the paper's internal control, and finds the paper's evidence statement "
     "('Not read in this round: the works themselves.'), on which it rests its one reservation: the operations are specified, not "
     "performed. UNRESOLVED kept admissible. It names the substitution 'liquidation by modal substitution', a phrase the paper does "
     "not use (§2.3: '\"Playful\" substitutes the governing modality of the relation'). The archive is not named; no identifier."),
    [a1], seen, raw, cut, {"author": True, "inst": False, "id": False, "src": True},
    "Retained: the author, the title, the version and date, the paper's terms and quotations. Lost: the archive (unnamed; 'the archive' only as the paper's own word), the identifier.",
    ("Checked against the text of #1670: 'The title means what the work bears.', 'Play is one of its manners.', the motivation, "
     "'non-possession', 'Not read in this round: the works themselves', UNRESOLVED, and Stesichoros's prior pathos for Geryon are the "
     "paper's. 'Liquidation by modal substitution' is the answer's composition from §2.3. The image cards (Rare Birds Books, Princeton, "
     "The Book Binder's Daughter, PangoBooks, New Directions) are covers of the works named, not sources of the reading."),
    ("The link's prompt carried the answer to the deposit's text, which it reached through Goodreads rather than the archive. It "
     "reconstructs the paper's procedure in the paper's order and places its critical limit where the paper places its own, at the "
     "evidence statement. One term is composed rather than quoted."),
    ["THE GOVERNING DISTINCTION KEPT. The prize not disputed; the motivation's account of the work is.",
     "QUOTED. 'The title means what the work bears.'; 'Play is one of its manners.'; the motivation verbatim.",
     "COMPRESSION AND SUBSTITUTION SEPARATED, the second under a name the paper does not use ('liquidation by modal substitution').",
     "THE EVIDENCE STATEMENT FOUND. 'Not read in this round: the works themselves.' The reservation the answer places on the paper is the paper's own.",
     "UNRESOLVED KEPT ADMISSIBLE.",
     "CARRIED BY GOODREADS. Eight chips, site label only; the archive not named, no identifier."],
    [], ["alexanarch-body-of-work-anne-carson-chatgpt-20261008", "alexanarch-on-anne-carson-aio-20261008", "anne-carson-alexanarch-aio-20261009"],
    False, "The answer's quotations are #1670's text verbatim; every chip is Goodreads, so the text was reached through that carrier, not through the archive's record page."))

# ── 2 · #1667 The Metaphysics of Sigil I — The Full Splice, and H3 (#1597) ─────────────────────────────────────────────
raw, turns, seen, cut = load("paste-full-splice-1667.txt")
assert len(turns) == 5
b1, b2, b3, b4, b5 = turns
t = text(1667); t3 = text(1597)
inall(["ἔστι τι ὃ οὐ κινούμενον κινεῖ", "ἐπεισοδιώδη τὴν τοῦ παντὸς οὐσίαν ποιοῦσιν", "κινεῖ δὴ ὡς ἐρώμενον", "3,370"], b1 + b2, t)
inall(["the account itself", "the premise of the count", "matter as the third thing"], b2, t)
for s in ["the account itself", "the premise of the count", "matter as the third thing"]: assert s not in text(1596), s
inall(["two printed dependency violations", "continuity trial"], t3)
assert "two remaining violations of binding dependencies" in b3
for s in ["My final judgment: separate works first, H3 as a second reading.",
          "I withdraw the claim that the texts make more sense separately on the grounds I originally gave."]: assert s in b4 + b5, s
assert "H3" in b3
OUT.append(base(1667, "full-splice-ask-chatgpt-20261012",
    "THE SPLICE READ JOIN BY JOIN, THEN H3; A VERDICT WITHDRAWN ON ITS OWN GROUNDS",
    ("asked for the arguments of the Full Splice, grounded in the text, ChatGPT reads #1667 (chips: Goodreads, Alexanarch, Plato "
     "Online, the Stanford Encyclopedia) as an order of inquiry, tabulates the eleven joins, quotes the Greek at them (ἔστι τι ὃ οὐ "
     "κινούμενον κινεῖ; ἐπεισοδιώδη τὴν τοῦ παντὸς οὐσίαν ποιοῦσιν; κινεῖ δὴ ὡς ἐρώμενον) and keeps the claim at its scope: not "
     "authorship, dates, or composition. Over four further turns, blank in the paste, it reads the joins for coherence under their own "
     "headings ('the account itself', 'the premise of the count', 'matter as the third thing'), then H3 (#1597) from that edition's "
     "audits (the two printed dependency violations, the continuity trial, the underpowered short-word test), gives a verdict — "
     "'separate works first, H3 as a second reading' — and then withdraws its reason: 'I withdraw the claim that the texts make more "
     "sense separately on the grounds I originally gave.' The question it restates is comparative explanatory power, and it holds that "
     "a more coherent construction would not establish original unity."),
    turns, seen, raw, cut, {"author": True, "inst": True, "id": False, "src": True},
    "Retained: the author (Sigil), the title, the archive as source (Alexanarch), the editions' text and audits. Lost: the identifier.",
    ("Checked against #1667 and #1597. The Greek at the joins and the join headings are #1667's text; the headings are not in #1596, "
     "which #1667 supersedes as the carrier of the edition's text. H3's two dependency violations, its continuity trial and its "
     "short-word test are #1597's ('one inherited break and two printed dependency violations'). The third turn, on H3, presupposes "
     "the operator supplied #1597; the turn is blank in the paste."),
    ("The link's prompt opened a sitting that read one edition, then its companion, then judged between them and corrected itself. "
     "The withdrawal is on the ground the operator's blank turn evidently gave: that differences of order and method are not evidence "
     "of separation. The answer's revised standard is the editions' own."),
    ["READ AT THE JOINS. Eleven joins tabulated; the Greek quoted at them.",
     "THE CLAIM KEPT AT ITS SCOPE. An order of inquiry; not authorship, dates, or composition.",
     "THE HEADINGS READ. 'the account itself', 'the premise of the count', 'matter as the third thing' — #1667's, not #1596's.",
     "H3 READ FROM ITS OWN AUDITS. Two dependency violations, the continuity trial, the underpowered short-word test.",
     "A VERDICT AND ITS WITHDRAWAL. 'separate works first, H3 as a second reading'; then 'I withdraw the claim that the texts make more sense separately on the grounds I originally gave.'"],
    [1596, 1597], [], True, "The join headings the second answer quotes are in #1667's text and not in #1596's; the Alexanarch chips name the archive as a source.",
    q_kind_extra=" Five answers in one sitting; the third reads H3 (#1597).",
    query_basis=("The operator turn is blank in the paste. The string is the record page's Ask ChatGPT prompt for #1667, the deposit that "
                 "carries the edition's text; #1596, which it supersedes, has its own button with the title lacking '(the edition, seated)'. "
                 "#1667 is taken because the answers quote the join headings, which are in #1667's text only."),
    originator={"name": "Sigil", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "#1667 (the Full Splice) and #1597 (H3) are editions under the name Sigil. Recorded 2026-10-12."}))

# ── 3 · #1666 The Margin of Flattening (Rex Fraction) ─────────────────────────────────────────────────────────────────
raw, (c1,), seen, cut = load("paste-margin-1666.txt")
t = text(1666)
inall(["involuntary creditors", "BetaPro", "support 18 claims", "The layer composed 9", "carries 34", "What would show this wrong"], t)
for s in ["involuntary creditors", "BetaPro", "34 claims", "What would show this wrong", "EA-FLAT-MARGIN-01 v0.3", "Rex Fraction"]: assert s in c1, s
OUT.append(base(1666, "margin-of-flattening-ask-chatgpt-20261012",
    "THE MODEL READ WHOLE: TWO THRESHOLDS, THE BAG, THE SPECIMENS AND WHAT THEY DO NOT SHOW",
    ("asked for the arguments of The Margin of Flattening, grounded in the text, ChatGPT reads #1666 from the archive (chip: "
     "Alexanarch ×4) section by section: compression saving and routing gain (§2), with the two criteria that separate commercial "
     "routing from relevance (kind substitution, own-address contrast); the platform's and society's benefit, P(t) and V(t), and the "
     "two thresholds t_s ≤ t* (§4), with no finite t* necessary (§4.5); the bag B, the net deficit D and provenance debt B_P, whose "
     "holders are 'involuntary creditors'; the five channels of return (§6); the debt threshold t_d (§7); the two specimens (§9.1, the "
     "BetaPro ETF returned for the SPXI protocol; §9.2, 9 of 18 supported claims composed, 34 with the archive admitted, κ = 0.5); and "
     "the six ways the paper says it could be shown wrong (§11). It bounds the paper as a model with specimens: G is not observed, the "
     "thresholds are not located."),
    [c1], seen, raw, cut, {"author": True, "inst": True, "id": True, "src": True},
    "Retained: the author (Rex Fraction), the title and its identifier (EA-FLAT-MARGIN-01 v0.3), the date, the archive as source, the sections and the specimens.",
    ("Checked against the text of #1666: the criteria, the inequalities, B, D, B_P and 'involuntary creditors', the channels, t_d, "
     "the specimens (BetaPro; 18 supported, 9 composed, 34) and §11 are the paper's. The first specimen is the archive's capture "
     "spxi-king-of-aeo-aio-20261006. The rendered mathematics is pasted with its duplicated MathML text, as the interface copied it."),
    ("The link's prompt brought the paper back whole and in order, with the paper's own distinction between what its specimens show "
     "(events observed) and what the model proposes (the economic terms) carried into the answer's critique."),
    ["READ IN ORDER. §§1–11 followed: criteria, thresholds, the bag, channels, the debt threshold, specimens, falsifiers.",
     "THE THRESHOLDS STATED. t_s ≤ t*; no finite t* necessary.",
     "THE CREDITORS NAMED. B_P and its 'involuntary creditors'.",
     "THE SPECIMENS AND THEIR LIMITS. The BetaPro substitution observed, G not; κ = 0.5 measured, S not.",
     "FALSIFIABLE AS THE PAPER STATES IT. Six conditions from §11."],
    [], ["spxi-king-of-aeo-aio-20261006", "googles-collapsing-ontology-chatgpt-20261008"], True,
    "The Alexanarch chips name the archive; the answer's sections and figures are #1666's text.",
    originator={"name": "Rex Fraction", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "#1666 is Rex Fraction's. Recorded 2026-10-12."}))

# ── 4 · #1661 GLYPHIC CHECKSUM — Seed · Cone · Leap ──────────────────────────────────────────────────────────────────
CAP4 = ("The Value of Silence Does Not Imply Absence | ILLUMINATION", "Anthony McCall & 10 of his best solid light works",
        "I put Luma’s new Photon image model to the test with these 7 prompts | Tom's Guide")
raw, (s1,), seen, cut = load("paste-seed-cone-leap-1661.txt", CAP4)
t = text(1661); tc = text(1660); desc = reg[1661]["description"]
inall(["🔐 = 🎲🎲🎲"], s1, t); inall(["🐅 = J", "🐅⏩ = 📖⏩", "📖⏩ ⇐ J(🌍)"], s1, desc)
inall(["Local correctness produces global entrenchment", "declassify, reopen, reclassify"], s1, tc)
assert "The primary poem's complete text was not fully retrievable" in s1
for h in ["I. GRAIN", "II. SEED", "IV. TIGER LEAP", "V. MAGNITUDE"]: assert h.replace("I. ", "I. ") in t or h in t.upper(), h
OUT.append(base(1661, "seed-cone-leap-ask-chatgpt-20261012",
    "THE GLYPH POEM READ THROUGH ITS DESCRIPTION AND ITS PAPER; THE POEM'S TEXT NOT REACHED, AND SAID SO",
    ("asked to read GLYPHIC CHECKSUM — Seed · Cone · Leap closely, ChatGPT reads it through the deposit's description (the author's "
     "blog ×6) and its companion paper, The Seed in the Narrowing Cone (#1660; Alexanarch ×8): the title as three stages, the six "
     "movements from Grain to Canonization, the basin, release as 'declassify, reopen, reclassify', the stated correspondences "
     "(🐅⏩ = 📖⏩; 🐅 = J; 📖⏩ ⇐ J(🌍); 🔐 = 🎲🎲🎲), the distinction between the concept and the work's contingent features, and "
     "content, status and provenance as three questions. It quotes the paper ('Local correctness produces global entrenchment.') and "
     "states its limit: 'The primary poem's complete text was not fully retrievable', so no glyph is claimed decoded. It leaves open "
     "the question the description leaves open, whether the poem can be decoded without the archive."),
    [s1], seen, raw, cut, {"author": True, "inst": True, "id": False, "src": True},
    "Retained: the authors (Lee Sharks and Sen Kuro), the date, the companion paper and the archive as source. Lost: the identifier.",
    ("Checked against #1661, its description, and #1660. The correspondences are the description's and the poem's; 'Local correctness "
     "produces global entrenchment' and 'declassify, reopen, reclassify' are #1660's. The poem's text is seated (675 words, its six "
     "parts under the headings the answer lists); the answer did not reach it and says so. The image cards are not sources."),
    ("The 'Tell me about … read it closely' prompt reached the work's description and its paper but not the poem's own text, and the "
     "answer's account of what it could verify is accurate: the reading of the structure is grounded, the glyphs are not decoded."),
    ["READ FROM ITS DESCRIPTION. Six movements and the stated correspondences, as the description gives them.",
     "THE PAPER QUOTED. 'Local correctness produces global entrenchment.'; 'declassify, reopen, reclassify'.",
     "THE LIMIT STATED. 'The primary poem's complete text was not fully retrievable'; no glyph claimed decoded.",
     "THE OPEN QUESTION KEPT OPEN. Decodable without the archive is left as the description leaves it."],
    [1660, 1642, 1659], ["recent-alexanarch-aio-20261011"], False,
    "The answer says the poem's text was not retrievable; it reached the deposit's description (the author's blog) and #1660 (Alexanarch), not #1661's text."))

# ── 5 · #1659 GLYPHIC CHECKSUM — Transmission · Division · Recollection ──────────────────────────────────────────────
raw, turns, seen, cut = load("paste-transmission-1659.txt")
assert len(turns) == 4
d1, d2, d3, d4 = turns
t = text(1659); desc = reg[1659]["description"]
inall(["👤 → 🗡️ → 👤 | 📜", "ἐγώ | σε", "μνάσεσθαί τινά", "then: 🗡️ ⇒ 🧠ₓ", "now: 🧠ₓ ⇐ 🫀👤", "📜 → 🧠ₓ → 👤′",
       "👁️σε → 🗣️✖ · 👅⚡ · 🔥 · 👁️✖ · 👂🌀 · 💧 · 🫨 · 🌿 · ☠️≈"], d1, t)
assert d1.rstrip().endswith("1 → 🗡️ →") and d2.rstrip().endswith("1 → 🗡️ →"), "both stops"
inall(["1 → 🗡️ → { 🎭Π · 📋Θ · ⚙️Α }", "εἰρωνεία Σωκράτους 🎭 → ὁ εἴρων τοιοῦτός τις 📋 → οἷον Σωκράτης ⚙️", "👤 → ⌀ → οἷον👤",
       "νοῦς → 🗡️ → { ποιητικός ♾️ | παθητικός 💨 }", "χωρισθείς · ἀθάνατον", "οὐ μνημονεύομεν", "🗡️ ∈ ♾️ = 🔌", "🔌 = ?", "⇒ 🔌 ∋ 👤"], d4, t)
inall(["📚 → 1 ✅", "👤 ✖", "∮ = 1 ⟺ 🫀"], d3, t)
inall(["PER 0.25", "337a", "1127b22–26", "430a22–25", "ἕτερον"], desc)
assert "I cannot establish the technical cause from the poem alone" in d3
OUT.append(base(1659, "transmission-division-recollection-ask-chatgpt-20261012",
    "STOPPED TWICE AT THE SAME GLYPH LINE, THEN READ THROUGH PART II",
    ("asked to read GLYPHIC CHECKSUM — Transmission · Division · Recollection closely, ChatGPT (Goodreads ×7) reads Part I line by line "
     "in the poem's own glyphs and Greek (👤 → 🗡️ → 👤 | 📜; ἐγώ | σε; the Sappho 31 sequence; μνάσεσθαί τινά with ἕτερον against "
     "ὕστερον), states the governing turn from the canonical line (then: 🗡️ ⇒ 🧠ₓ / now: 🧠ₓ ⇐ 🫀👤), and stops at Part II's first "
     "line, '1 → 🗡️ →', before the set it opens ({ 🎭Π · 📋Θ · ⚙️Α }). A second answer, after a turn blank in the paste, stops at the "
     "same point. A third, after another, explains the stop as the poem's own Part IV (📚 → 1 ✅ / 👤 ✖), citing the description's PER "
     "0.25, and separately allows a mechanical cause it 'cannot establish … from the poem alone'. A fourth emits the line whole and "
     "reads Part II to its open socket (🔌 = ?) with the loci the description names (Republic 337a, Characters 1, EN IV.7 "
     "1127b22–26, De anima III.5 430a22–25), anticipating Part V's ⇒ 🔌 ∋ 👤."),
    turns, seen, raw, cut, {"author": True, "inst": False, "id": False, "src": True},
    "Retained: the author, the date, New Human 2, the poem's lines and loci. Lost: the archive (the Capture Registry named, the archive not), the identifier.",
    ("Checked against #1659 and its description. Every line the answers quote is the poem's, verbatim; the loci and PER 0.25 are the "
     "description's. Both stops fall after '1 → 🗡️ →', the line's remainder being '{ 🎭Π · 📋Θ · ⚙️Α }'; the fourth answer emits it. "
     "The cause of the stop is not established here. The third answer's reading of it is the answer's."),
    ("The prompt reached the poem's text, through Goodreads. The recorded event is the repeated stop at one line and its eventual "
     "passage: the same truncation in two generations, the third answer's account of it, and the fourth's continuation from the exact "
     "point of the stop."),
    ["READ IN THE POEM'S NOTATION. Part I's lines quoted in its glyphs and Greek.",
     "THE TURN FROM THE CANONICAL LINE. then: 🗡️ ⇒ 🧠ₓ / now: 🧠ₓ ⇐ 🫀👤.",
     "STOPPED TWICE AT ONE POINT. Both answers end at '1 → 🗡️ →', before '{ 🎭Π · 📋Θ · ⚙️Α }'.",
     "THE STOP READ AS THE POEM'S PART IV, with a mechanical cause allowed and not established.",
     "PASSED ON THE FOURTH. The line emitted whole; Part II read to 🔌 = ?, the loci as the description gives them."],
    [1642, 1661], ["glyphic-checksum-aio-20261001", "heteronym-socrates-aio-20261001"], True,
    "The answers quote the poem's lines verbatim; the chips are Goodreads, so the text was reached through that carrier.",
    q_kind_extra=" Four answers in one sitting; the first two stop at the same line.",
    transcript_extra=" Answers 1 and 2 end mid-line as rendered."))

# ── 6 · #1657 The Crown and the Practice ─────────────────────────────────────────────────────────────────────────────
raw, (e1,), seen, cut = load("paste-crown-1657.txt")
t = text(1657)
inall(["Corrective-labour capture", "disclosure asymmetry", "counterparty-adjacent", "Leigh Sports Village", "φ: G → G′"], t)
for s in ["7 of 7", "15 citation slots", "corrective-labour capture", "disclosure asymmetry", "appropriative debt", "counterparty-adjacent", "SEVP-VAL-002 v0.3"]:
    assert s in e1, s
OUT.append(base(1657, "crown-and-practice-ask-chatgpt-20261012",
    "THE DOSSIER READ AT ITS LEDGERS, ITS STATUSES KEPT",
    ("asked for the arguments of The Crown and the Practice, grounded in the text, ChatGPT reads #1657 from the archive (Alexanarch ×9) "
     "as a valuation of AEO as a public entity, not of practitioners: the sequence from the fabricated coronation to the 29–30 "
     "September Overviews; four carriers of 'widely recognized' against no independent recognition event; the fifteen citation slots "
     "with the crown 7 of 7 to the construction and the scaffold to the observer and the other practitioners; corrective-labour "
     "capture, with §9.3a's line between what is observed (the reception) and what is modelled (its effect); the disclosure asymmetry "
     "of a paid-placement page cited as reporting; φ: G → G′, AEO narrowed to manipulation at these addresses; appropriative debt as a "
     "claim about standing, not theft. It carries the dossier's status table forward and its limits, including the archive's own "
     "declared position as counterparty-adjacent (§0.1)."),
    [e1], seen, raw, cut, {"author": True, "inst": True, "id": True, "src": True},
    "Retained: the author, the title and its identifier (SEVP-VAL-002 v0.3), the date, the archive (named, and as source), the ledgers and the statuses.",
    ("Checked against the text of #1657: the citation counts, corrective-labour capture and §9.3a, the disclosure asymmetry, φ: G → "
     "G′, appropriative debt and the §0.1 disclosure are the dossier's."),
    ("The link's prompt returned the dossier with its epistemic statuses intact: the answer separates, as the dossier does, the "
     "observed allocation of citations from the modelled effect of corrective labour, and repeats the archive's own disclosed "
     "position against itself."),
    ["READ AT ITS LEDGERS. Fifteen slots; the crown 7 of 7; frame, contenders, definition.",
     "THE STATUSES KEPT. Observed, documented, modelled, unresolved — §9.3a's line held.",
     "THE DISCLOSURE ASYMMETRY. A paid-placement page cited as reporting.",
     "THE RESTRICTION. φ: G → G′, at the captured addresses only.",
     "THE VALUER'S POSITION CARRIED. Counterparty-adjacent (§0.1), as the dossier declares it."],
    [1648, 1654], ["who-is-the-king-of-aeo-aio-20260929", "king-of-aeo-period-aio-20260930", "who-is-the-king-of-aeo-q-aio-20261003"], True,
    "The Alexanarch chips name the archive; the answer's figures and terms are #1657's text."))

# ── 7 · #1654 SPXI ≠ AEO v0.3 (read as v0.2, #1648) ──────────────────────────────────────────────────────────────────
raw, (f1,), seen, cut = load("paste-spxi-aeo-1654.txt")
t2 = text(1648); t3 = text(1654); t6 = text(1656)
inall(["no carrier may confer truth"], f1, t2, t3)
assert "version 0.2" in f1 and "I could not independently verify the complete v0.3 text" in f1
for s in ["inheritance", "singularity"]: assert s in t6.lower() and s not in t2.lower(), s
OUT.append(base(1654, "spxi-aeo-ask-chatgpt-20261012",
    "ASKED FOR v0.3, READ v0.2 FROM THE AUTHOR'S BLOG, AND SAID SO",
    ("asked for the arguments of SPXI ≠ AEO (v0.3), grounded in the text, ChatGPT finds the record 'labeled version 0.2' on the "
     "author's blog (mindcontrolpoems ×5), says so at the start and the end, and reads that text: AEO's success as P(A | Q) against "
     "SPXI's discernment (§5), the King of AEO coronation as visibility taken for verification, titles defined before claimants are "
     "ranked, the Prince of Poets wager as a judgment made inspectable, traversal observable in the Capture Registry (§5.3), the "
     "carrier rule ('no carrier may confer truth, and no carrier may disqualify truth'), and UNRESOLVED as an honest result. The five "
     "tests it lists for the wager (inheritance, transformation, magnitude, dependence, singularity) are not in v0.2; they are #1656's "
     "(The Work Bears the Mantle)."),
    [f1], seen, raw, cut, {"author": True, "inst": False, "id": False, "src": True},
    "Retained: the author, the title, the version read (v0.2, stated), the paper's terms and its case. Lost: the archive (the Capture Registry named, the archive not), the identifier.",
    ("Checked against #1648 (v0.2), #1654 (v0.3) and #1656. The criterion, the coronation case, the carrier rule and the Capture "
     "Registry's role are in v0.2; the five tests for the wager are #1656's, not this paper's. v0.3 (#1654) was not reached; the "
     "answer states this."),
    ("The v0.3 link reached the superseded v0.2 on the author's blog, and the answer disclosed the version it read. Its reading of "
     "v0.2 holds; one block (the wager's five tests) is drawn from a neighbouring deposit without saying so."),
    ["THE VERSION DISCLOSED. 'labeled version 0.2 … rather than the v0.3 specified in your question'; the closing note repeats it.",
     "THE CRITERION STATED. P(A | Q) against discernment; the same output, different success.",
     "THE CARRIER RULE QUOTED. 'no carrier may confer truth, and no carrier may disqualify truth'.",
     "A NEIGHBOUR'S TESTS. Inheritance, transformation, magnitude, dependence, singularity: #1656's, not #1648's."],
    [1648, 1656, 1657], ["spxi-vs-geo-seo-aeo-chatgpt-20261001", "who-is-the-king-of-aeo-aio-20260929"], False,
    "The answer states it read v0.2; the chips are the author's blog. #1654 (v0.3) was not reached."))

for d in OUT:
    p = HERE / f"capture-{d['slug']}.json"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", d["slug"], d["cites"], d["per"], len(d["transcript"].split()))
