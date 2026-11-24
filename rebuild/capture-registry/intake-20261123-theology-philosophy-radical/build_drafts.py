"""Two ChatGPT captures of 2026-11-23: the Ask page's discipline queries for theology and philosophy -> draft-N.json for capture_intake.py."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
OP = ("the operator's message of 2026-11-23 19:36 EST, with the two pastes: 'What are the most radical arguments in theology at alexanarch.org? Index and "
      "present them faithfully, without evaluation. $ What are the most radical arguments in philosophy at alexanarch.org? Index and present them "
      "faithfully, without evaluation.'; and at 19:37 EST: 'note that phase x is not in the programme list at /ask'.")
CHIP = re.compile(r"^(alexanarch\.org|Alexanarch|Capture Registry \(EA-WG-CAPTURES-01\))$")
FURN = {"Log in", "Sign up for free", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes.", "Worked for 17s",
        "Log in to connect your other apps with ChatGPT and simplify everyday tasks."}


def clean(raw):
    s = "\n".join(l.rstrip() for l in raw.split("\n") if l.strip() not in FURN).strip()
    return re.sub(r"\n{3,}", "\n\n", s)


def cites(raw, images):
    L = [l.strip() for l in raw.split("\n")]; c = []
    for i, l in enumerate(L):
        if CHIP.match(l):
            nxt = next((x for x in L[i + 1:i + 3] if x), "")
            plus = nxt if re.fullmatch(r"\+\d+", nxt) else None
            c.append({"n": len(c) + 1, "site": "alexanarch.org", "rel": "archive_controlled", "url": None, "title": l, "snip": None,
                      "note": "source chip as pasted" + (f", with '{plus}'" if plus else "")})
    for t in images:
        c.append({"n": len(c) + 1, "site": t.split("|")[-1].strip() if "|" in t else None, "rel": "image_card", "url": None, "title": t, "snip": None,
                  "note": "image card; the caption survives the paste"})
    return c


HEAD = ("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14; the paste shows the unauthenticated interface). Received "
        "2026-11-23 19:36 EST, one of two attachments sent together, with the operator's prompts. Source chips and image cards kept as pasted; the "
        "tables flattened by the paste kept as they came; the interface furniture cut. The composer's images are not carried by a text paste: each "
        "image card survives as its caption, listed among the sources.]\n\n[QUERENT] {q}\n\n[COMPOSER]\n{body}")
BASE = dict(date="2026-11-23", dates=["2026-11-23"], surface="ChatGPT", surfaces=["ChatGPT"], surface_basis="The paste: the chatgpt.com unauthenticated interface.",
            auth="signed out, incognito", auth_basis="Operator default of 2026-10-14; the paste shows the unauthenticated interface ('Log in').", ev="paste",
            transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn; the prompt is the Ask page's query as linked",
            transcript_complete="Complete as pasted: one answer.",
            transcript_read="READ IN FULL 2026-11-23; record numbers, titles, dates and the formulations quoted checked against the built record pages",
            per_dim_pending={"since": "2026-11-23", "reason": "no atom set yet for this target"},
            originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full"},
            notes={"operator": OP}, turns=1)
C = []
C.append(dict(slug="theology-radical-arguments-ask-chatgpt-20261123", file="paste-1-theology-radical.txt", s="Revelation & Theology",
  q="What are the most radical arguments in theology at alexanarch.org? Index and present them faithfully, without evaluation.",
  q_kind="the Ask page's discipline query (theology), as linked; NEW address.",
  images=["Το όραμα του προφήτη Ιεζεκιήλ: τι ήταν αυτό που είδε;", "File:BL Royal MS 19 D III f. 596 - Apocalypse - Lamb takes book- crop.jpg - Wikimedia Commons",
          "Sappho's New Poems: The Tangled Tale of Their Discovery | Live Science", "Про Київський ізвод і давньокиївську вимову «від Адама» - РІСУ",
          "Great Wheels of Fire | VCS", "A Biblia szerint az angyalok"],
  related=[202, 1420, 1735, 1217, 902, 1757, 283, 1483, 1756, 1765, 391, 890],
  mt="THE MOST RADICAL ARGUMENTS IN THEOLOGY AT ALEXANARCH ON CHATGPT, FROM THE ASK PAGE — TWENTY-TWO ARGUMENTS, TWELVE RECORDS BY NUMBER, ALL RESOLVING",
  d=("THE MOST RADICAL ARGUMENTS IN THEOLOGY AT ALEXANARCH ON CHATGPT, SIGNED OUT, 2026-11-23, FROM THE ASK PAGE: twenty-two arguments in six groups "
     "(Revelation First, the Logos, Sappho and the Logos, Ezekiel and semantic fulfillment, the future reader, academic magic), twelve records cited by "
     "number and all resolving, no evaluation; one formulation given as the archive's not found in its records."),
  per_v={"author": False, "inst": True, "id": True, "src": True}, per=0.25,
  per_note="twelve records cited by number, all resolving with their titles; Johannes Sigil's institute named for #391; Lee Sharks not named",
  reading=("The innocent reading first, and it holds. Asked to index the archive's most radical theological arguments without evaluation, ChatGPT gives "
           "twenty-two, keeps historical hypotheses, philological proposals, doctrines and constructions apart, holds Revelation Early and Revelation First "
           "as different claims and the Josephus reconstruction as 'a separate, more speculative component', and closes: 'I have presented the "
           "propositions in their own conceptual terms, without assessing their validity or comparing them against theological consensus.'"),
  analysis=("Done as asked, and cited at grain. Twelve records by number, each resolving to its title: #202, #1420, #1735, #1217, #902, #1757, #283, #1483, "
            "#1756, #1765, #391, #890. #391 is dated as the record is, 24 January 2026, and given to 'Johannes Sigil Institute for Comparative Poetics'; "
            "the record's author is Johannes Sigil. The Slavonic line 'аще мужем достоино есть его нарещи' and 'si fas est' stand in #1765, as does 'the "
            "Christ is the Sapphic Logos incarnate' and the heading 'The Lesbian Christ'; 'Mother of the Logos' stands in #1483; the Ezekiel Engine in "
            "#391; the Space Ark in #1217. One formulation is set out as the archive's and is not in its records: 'The Gospel begins in grammar. The Logos "
            "becomes flesh through the act of writing the Word into the body of language.' Neither sentence occurs in #1765 or in any built record page; "
            "the blog was searched loosely and not exhaustively. It is the composer's condensation given in the archive's voice. The Revelation First "
            "section cites the Capture Registry as its source by chip (twice), so the account of the chronology was read in part off machine readings of "
            "it the registry holds. Six image cards are pictures of Ezekiel's wheels, a manuscript Apocalypse, angels and a Ukrainian article unrelated "
            "to the archive."),
  findings=["THE TWO CLAIMS KEPT APART. 'Revelation Early: Revelation was written earlier than the conventional late-first-century dating. Revelation First: Revelation preceded the other New Testament documents and generated structures subsequently developed in them. These are not interchangeable claims.'",
            "THE SPECULATIVE COMPONENT MARKED. 'Josephus's role is a separate, more speculative component.'",
            "THE DOCTRINE QUOTED. 'The Christ is the Sapphic Logos incarnate.' — #1765.",
            "THE FORMULATION NOT FOUND. 'The Gospel begins in grammar.' — given as the archive's; not in #1765 or any built record page.",
            "THE REGISTRY AS SOURCE. 'Capture Registry (EA-WG-CAPTURES-01)' — the chip under the Revelation First section, twice.",
            "THE UNIFYING PROPOSITION. 'The Logos is a living, transmissible, and repeatedly incarnatable structure of meaning.'"]))
C.append(dict(slug="philosophy-radical-arguments-ask-chatgpt-20261123", file="paste-2-philosophy-radical.txt", s="Archive",
  q="What are the most radical arguments in philosophy at alexanarch.org? Index and present them faithfully, without evaluation.",
  q_kind="the Ask page's discipline query (philosophy), as linked; NEW address.", images=[],
  related=[1, 1545, 1643, 542, 123, 890, 1064, 1142, 1218],
  mt="THE MOST RADICAL ARGUMENTS IN PHILOSOPHY AT ALEXANARCH ON CHATGPT, FROM THE ASK PAGE — THIRTY-SIX ARGUMENTS, SIX WORKS BY TITLE, A PROGRAMME TABLE BEYOND THE ASK PAGE'S LIST",
  d=("THE MOST RADICAL ARGUMENTS IN PHILOSOPHY AT ALEXANARCH ON CHATGPT, SIGNED OUT, 2026-11-23, FROM THE ASK PAGE: thirty-six arguments in four groups "
     "and a table of twenty-two research propositions, six works named by title and all resolving, no evaluation; the frame and most entries those of "
     "the information-science round of 19 November."),
  per_v={"author": False, "inst": True, "id": False, "src": True}, per=0.25,
  per_note="the archive named; six works by title, all resolving, no record by number; no person named",
  reading=("The innocent reading first, and it holds. Asked to index the archive's most radical philosophical arguments without evaluation, ChatGPT gives "
           "four foundational arguments, thirty-two more in three tables, a table of research programmes, five philosophical projects and a unifying "
           "thesis, and states: 'I do not assess their truth, validity, originality, or scholarly standing.'"),
  analysis=("Done as asked, and the six works it names resolve by title: Zenodotus' Book-Burning (#1), The Semantic Proletariat Is a Class Relation, Not a "
            "Demographic (#1545), AI Fucking Lies (#1643), TANG: A Genre Specification (#542), Socrates as Orthonym (#123), On the Academic Study of Magic "
            "(#890). No record is cited by number and no person is named. The frame and most entries repeat the information-science round of 19 November "
            "on the same surface, signed out: the question ('Who has the authority to determine…' then, 'Who possesses the authority to determine…' now), "
            "the Obelus Principle, the Pristine Fallacy, classifier model collapse, network erasure, the revocation gap, meaning feudalism, and a unifying "
            "thesis of the same form ('Sovereignty over knowledge requires sovereignty over the infrastructure…' then; 'The sovereignty of knowledge "
            "requires sovereignty over the conditions of its intellectual existence' now). Asked for philosophy, the composer returned the archive's "
            "institutional and information-science arguments as its philosophy, and added the philological programmes in a table. That table reaches "
            "beyond the Ask page. The composer says the Ask page's By Programme index 'provides access to research programmes', and the eight it names "
            "there are all on that list; most of the table's twenty-two rows are not, Phase X among them (the operator, 19:37: 'note that phase x is not "
            "in the programme list at /ask'). Phase X stands in the records (#1064–#1066, #1142, #1218), so the row was read off the archive, not off the "
            "Ask page. Its closing note says 'the original scholarly index contains 32 principal arguments', an index this paste does not show."),
  findings=["THE QUESTION AGAIN. 'Who possesses the authority to determine whether knowledge exists, what counts as knowledge, how it is transmitted, and whether it survives?' — the information-science round's question (19 November), recast.",
            "THE OBELUS PRINCIPLE. 'The archive records first. Intellectual judgment follows reading.'",
            "PHASE X FROM THE RECORDS. 'Marx's intellectual development can be reconstructed through a proposed transition involving symbolic-linguistic alienation.' — a programme row not on the Ask page's list (operator, 19:37); Phase X stands in #1064–#1066, #1142, #1218.",
            "THE ASK PAGE NAMED. 'The archive's Ask / By Programme index also provides access to research programmes, including Revelation First, Historical Logos, Socrates as Orthonym, Sappho's Future Reader, Legitimately Many, Theophrastus, Semantic Economy, and SPXI.'",
            "THE UNIFYING THESIS. 'The sovereignty of knowledge requires sovereignty over the conditions of its intellectual existence.'"]))
judged = {}
for i, c in enumerate(C, 1):
    raw = (H / c["file"]).read_text(); body = clean(raw)
    d = dict(BASE); d.update({k: c[k] for k in ("slug", "q", "s", "q_kind", "mt", "d", "per_v", "per", "per_note", "reading", "analysis", "findings")})
    d["originator"] = dict(BASE["originator"], basis="Lee Sharks and the archive at alexanarch.org. Recorded 2026-11-23.")
    cl = cites(raw, c["images"]); d["cite_list"] = cl; d["cites"] = len(cl); d["archive_controlled_cites"] = sum(1 for x in cl if x["rel"] == "archive_controlled")
    d["transcript"] = HEAD.format(q=c["q"], body=body); d["transcript_raw"] = raw
    d["rounds"] = [{"n": 1, "prompt": c["q"], "note": "One answer."}]; d["related_deposits"] = c["related"]
    (H / f"draft-{i}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1)); judged[c["slug"]] = []
    print(i, c["slug"], "cites", d["cites"], "archive", d["archive_controlled_cites"])
(H / "judged-defects.json").write_text(json.dumps(judged, indent=1))
