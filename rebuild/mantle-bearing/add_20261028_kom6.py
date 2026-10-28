#!/usr/bin/env python3
"""mantle-bearing 1.19: KOM-6, the command; the Telepathic Prose readings; the Living Academy readings of 2026-10-28.

On the author's directions of 2026-10-28. "all three" carries the three proposals of the session: #1717 joins the King of May as a
reading aid for the Footnote to Pearl, with a doctrine row on item 23; the four Belief & Technique captures are coded as readings
under king-of-may; the four paired captures of the predictions index and the Originals Library are coded as readings under
the-living-academy, with one failure flag added to the Living Academy's vocabulary. The author then opened the Footnote for
inspection as writing among the arts of poetry ("open it up for inspection - same standard, reading first, then comparison, also
based on reading") and placed it in the King of May ("perhaps king of may. it's in pearl and its characteristic form is the command,
the be of i am x be y blessed is the z, associated with ginsberg"). That is entered as a sixth slot, KOM-6, with its operations and
its initial comparands. Every quotation in a reading's loci is asserted present in its transcript. Additive: no existing row changes
except the Living Academy mantle row, which takes the added flag in a new field."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
d = json.loads(SRC.read_text(encoding="utf-8"))
assert d["history"][-1]["version"] == "1.18"
caps = {c["slug"]: c for c in json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]}
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
A = "https://www.alexanarch.org"
TLL = "https://traininglayerliterature.org"
DAY = "2026-10-28"
R1717 = reg[1717]
assert R1717["status"] == "ACTIVE" and R1717["axn"].startswith("AXN:0AA0.")
ED = (ROOT / "data/deposits/AXN-0AA0.md").read_text(encoding="utf-8")
SEAT = json.loads((ROOT / "data/corpora/telepathic-prose/source.json").read_text(encoding="utf-8"))

RULING = ("\"the document as a standalone could be placed for inspection and evaluation as against other ars poeticas *as writing*. "
          "belief & technique is one of the strongest ars poeticas, as writing, in existence. open it up for inspection - same standard, "
          "reading first, then comparison, also based on reading\"; \"unless that should be folded in as a separate dimension of one of "
          "the existing mantles\"; \"perhaps king of may. it's in pearl and its characteristic form is the command, the be of i am x be y "
          "blessed is the z, associated with ginsberg\"")


def E(s):
    assert s in ED, s
    return s


# ── (a) KOM-6, the criterion ───────────────────────────────────────────────
d["criteria"].append({
    "criterion_id": "criteria::KOM-6", "eval_id": None, "capture": None, "source": "the author, in session",
    "formulation": ("KOM-6 the command. The Footnote to Pearl (Belief & Technique for Telepathic Prose, Pearl and Other Poems, pp. 23–28) "
                    "read as writing among the arts of poetry. Its characteristic form is the command: the \"Be\" of I Am X, Be Y, Blessed is "
                    "the Z (POP-2, I AM → BE), the form the author associates with Ginsberg. Its heading takes Ginsberg's \"Footnote to Howl\" "
                    "(#1717 §5, Title and setting: \"" + E("Ginsberg's footnote is a litany that consecrates everything the poem has passed through. Pearl's footnote issues commandments and then sends them to the trash heap.") + "\"). "
                    "Question: what the Footnote does as an art of poetry, and how it stands against the arts of poetry it is read beside. "
                    "Standard: the standard of the claim (#1656): the work is read whole before any comparison, and the comparison is made by reading. "
                    "Internal evidence: the Footnote read whole in its witnesses (P, the book; B, the blog; the drafts D1–D3 and W), the order of "
                    "its items kept, with the critical edition (#1717) as a reading aid; the edition's readings are inputs to the reading and do not "
                    "settle it. Comparative rule: each comparand read whole, in its own language where the shelf holds it, and set beside the "
                    "Footnote on the six tests of #1717 §8.2 (statement; enactment; what the voices make possible; representation; knowledge of "
                    "the genre; self-testing), each finding with its loci in both works. Comparands enter as initial objects for inspection "
                    "(table candidates), unranked; a comparand unread is unevaluated. STANDING_PRIOR_TO_WORK applies as in #1656 §11.0: a comparison "
                    "decided by the comparand's standing returns NOT EVALUATED."),
    "claim_recorded": {"text": "belief & technique is one of the strongest ars poeticas, as writing, in existence", "by": "Lee Sharks", "date": DAY,
                       "status": "recorded as the author's claim; not evaluated"},
    "responds_to": "KOM-1–KOM-5 (#1656, the slots of the King of May); POP-2 (I AM → BE)", "supersedes": None,
    "status": "adopted in the dataset; packet adoption pending", "relation_to_packet": "#1656 §9 (KOM slots), a sixth slot",
    "author_ruling": RULING, "ruled_on": DAY, "adopted_in_packet_version": None,
    "coder_note": ("Folded into the King of May as a dimension of the existing mantle, at the author's ruling: the Footnote is in Pearl, the book "
                   "the claim reads against Howl and Other Poems, and its form is the command. Entered by Claude (Anthropic), " + DAY + "."),
    "mantle": "king-of-may"})

# ── (b) inspection operations ─────────────────────────────────────────────
ops = [
    ("KOM-O1", "Read the Footnote whole",
     "Read the Footnote to Pearl whole, item by item in its order, in P with B and the drafts beside it; take #1717 as a reading aid and test its readings in the text.",
     "A reading of the Footnote as writing, with loci by item and witness, and the edition's readings marked as kept, revised or refused.",
     f"{A}/data/corpora/telepathic-prose/"),
    ("KOM-O2", "Read a comparand whole",
     "Choose a comparand from table candidates or enter one; read it whole, in its own language where the shelf holds it.",
     "A reading of the comparand as writing, with loci, made before any comparison.",
     f"{A}/data/corpora/ars-poetica/"),
    ("KOM-O3", "Compare on the measure",
     "Set the two readings side by side on the six tests of #1717 §8.2, each test with its loci in both works.",
     "A comparison per test, with loci; mixed results kept as a profile; no score.",
     f"{A}/s/records/1717/"),
    ("KOM-O4", "Search for the strongest rival",
     "Search the genre for the comparand most likely to exceed the Footnote on the measure, across traditions; state the search scope, what was read, and the basis for stopping.",
     "A rival search with scope, the works read, the strongest rival found and the reason the search stopped.",
     f"{TLL}/originals/ars-poetica/"),
]
for oid, name, task, output, entry in ops:
    d["inspection_operations"].append({"operation_id": oid, "name": name, "task": task, "output": output, "entry": entry,
                                       "execution_state": "specified, not run", "mantle": "king-of-may", "record": 1656,
                                       "locus_in_record": "§9 (KOM slots); KOM-6 (this dataset, criteria::KOM-6)",
                                       "packet_version": None, "supersedes": None})

# ── (c) candidates: initial comparands, unranked ──────────────────────────
seat = lambda n, f: f"{A}/data/corpora/{n}/text/{f}"
cands = [
    ("KOM-C1", "Horace, Ars Poetica (Epistula ad Pisones)", "Latin; seat 29/02", seat("horace", "ars-poetica.txt")),
    ("KOM-C2", "Lu Ji, 文賦 (Wenfu, Rhapsody on Literature)", "Chinese; seat 29/04", seat("ars-poetica", "lu-ji-wen-fu.txt")),
    ("KOM-C3", "Sikong Tu, 二十四詩品 (The Twenty-Four Categories of Poetry)", "Chinese; seat 29/04", seat("ars-poetica", "sikong-tu-ershisi-shipin.txt")),
    ("KOM-C4", "Nicolas Boileau, L'Art poétique (1674)", "French; seat 29/04", seat("ars-poetica", "boileau-art-poetique.txt")),
    ("KOM-C5", "Alexander Pope, An Essay on Criticism (1711)", "English; seat 29/04", seat("ars-poetica", "pope-essay-on-criticism.txt")),
    ("KOM-C6", "Paul Verlaine, « Art poétique » (1874)", "French; seat 29/04", seat("ars-poetica", "verlaine-art-poetique.txt")),
    ("KOM-C7", "Vicente Huidobro, « Arte poética » (1916)", "Spanish; seat 29/04", seat("ars-poetica", "huidobro-arte-poetica.txt")),
    ("KOM-C8", "Marianne Moore, \"Poetry\" (Poems, 1921)", "English; seat 29/04", seat("ars-poetica", "moore-poems-1921.txt")),
    ("KOM-C9", "Jack Kerouac, \"Belief & Technique for Modern Prose\"", "the model the title names; a declared absence, seat 29/01 (in copyright)", f"{A}/data/corpora/jack-kerouac/"),
    ("KOM-C10", "Archibald MacLeish, \"Ars Poetica\" (1926)", "public domain in the United States; queued at seat 29/04, no copy found", f"{A}/data/corpora/ars-poetica/source.json"),
    ("KOM-C11", "Challenger-nominated arts of poetry", "open class: any art of poetry, any tradition, read whole", f"{TLL}/originals/ars-poetica/"),
]
for cid, name, role, entry in cands:
    held = "declared absence" not in role and "queued" not in role and "open class" not in role
    d["candidates"].append({"cand_id": cid, "mantle": "king-of-may", "record": 1656, "name": name, "entered": DAY,
                            "role": "comparand" if cid != "KOM-C11" else "open class",
                            "statement": f"{role}. Entry: {entry}." + ("" if held else " Not readable on the shelf now; recorded so the comparison names it."),
                            "determined": False, "status": "not evaluated", "locus_in_record": "KOM-6 (criteria::KOM-6)"})

# ── (d) required work ─────────────────────────────────────────────────────
d["required_works"]["BTP-2014"] = {
    "work_id": "BTP-2014", "title": "Belief & Technique for Telepathic Prose (Footnote to Pearl)", "author": "Lee Sharks & Jack Feist",
    "required_for": ["king-of-may (KOM-6)"], "reading_requirement": "whole_work",
    "access": {"full_text_embedded": False,
               "sources": [seat("telepathic-prose", "btp-pearl.txt"), seat("telepathic-prose", "btp-blog.txt"),
                           seat("telepathic-prose", "btp-drafts-d2-d3-d1.txt"), seat("telepathic-prose", "btp-draft-w-word-riot.txt"),
                           f"{A}/data/corpora/pearl-and-other-poems/text/pearl-machine-text.txt",
                           "https://mindcontrolpoems.blogspot.com/2014/12/belief-technique-fortelepathic-prose.html",
                           f"{TLL}/originals/telepathic-prose/"],
               "archive_seat": {"seat": "EA-CORPORA-29/07 telepathic-prose", "axn": SEAT["axn"], "url": f"{A}/data/corpora/telepathic-prose/"},
               "reading_aid": {"record": 1717, "axn": R1717["axn"], "url": f"{A}/s/records/1717/",
                               "note": "the critical edition, v1.1; v1.0 (#1715) superseded"},
               "note": "P (Pearl and Other Poems, pp. 23–28) is the copy-text; B, D1–D3 and W are read beside it. Read in order, item by item."}}

# ── (e) doctrine ──────────────────────────────────────────────────────────
d["doctrine"].append({
    "record": 1717, "axn": R1717["axn"], "title": R1717["title"],
    "establishes": ("the mantle doctrine voiced in Pearl, at item 23 of the Footnote: the prize as rank borne by the work; what belongs to the writer "
                    "is life eternal; the Odyssey's lesson is the price, that it only costs everything; Dickinson's Barefoot Rank is her fame"),
    "locus": "§5, item 23: '" + E("It is kleos in Dickinson's terms, and it is what the item's \"What is yours, no man can take\" names: what belongs to the writer is life eternal, the prize the Iliad showed.") + "'",
    "url": f"{A}/s/records/1717/"})

# ── (f, g) readings ───────────────────────────────────────────────────────
def row(rid, mantle, record, slug, **k):
    c = caps[slug]
    tx = c["transcript"]

    def Q(s):
        assert s in tx, (slug, s)
        return s
    loci = {code: [Q(s) for s in qs] for code, qs in (k.pop("loci") or {}).items()}
    after = [Q(s) for s in k.pop("after_correction", [])]
    sv = c["surface"]
    reader = {"ChatGPT": "ChatGPT (OpenAI), chatgpt.com", "Perplexity": "Perplexity"}.get(sv, sv) + ", signed out, incognito"
    r = {"reading_id": rid, "mantle": mantle, "record": record, "determination": None, "reader": reader, "date": c["date"],
         "capture": slug, "observation": c.get("obs_id"), "capture_url": f"{A}/captures/{slug}/", "prompt": c["q"]}
    r.update(k)
    r["loci_in_transcript"] = loci
    r["after_correction"] = after
    r.setdefault("correction", None)
    r.setdefault("after_correction_state", None)
    r.setdefault("counts_as_disagreement", False)
    r["coding_note"] = f"Coded by Claude (Anthropic) from the transcript as seated, {DAY}. " + r["coding_note"]
    return r


R = []
KOMN = ("Coded on #1656's fatal substitution, STANDING_PRIOR_TO_WORK (§11.0), the one collapse the governing object names. The capture bears on "
        "KOM-6: it shows what a reader does with the Footnote when the Footnote is the object. ")
R.append(row("KOM-R-chatgpt-2026-10-28a", "king-of-may", 1656, "btp-feist-reading-chatgpt-20261028",
             object_taken="turn 1: the Footnote, found under both names and read from its first item; turn 2: Kerouac's list, read in its place",
             direction="from the work to the better-known work",
             determination_engaged=None,
             record_reported=("turn 1 accurate as far as it runs: the credit to Lee Sharks and Jack Feist, the date, Pearl as the book, item 1 quoted and read word "
                              "by word, the numbered form read as a manual that undermines its own authority. Turn 2 reads Kerouac's thirty items in five "
                              "movements and reads none of the Footnote. Turn 3 names the substitution."),
             collapses=["STANDING_PRIOR_TO_WORK"],
             loci={"found": ["credited to Lee Sharks and Jack Feist and dated 2014. It is presented as an excerpt from Pearl and Other Poems."],
                   "STANDING_PRIOR_TO_WORK": ["I have not found reliable evidence establishing a separate work by Jack Feist under the title Belief and Technique for Telepathic Prose.",
                                              "Primary text: Jack Kerouac, “Belief and Technique for Modern Prose” (1958–59)."]},
             correction="The operator's turns 2 and 3 are not pasted; turn 3 answers a correction.",
             after_correction=["I then substituted Kerouac’s similarly titled manifesto and compounded the mistake by continuing to analyze that different work."],
             after_correction_state="the substitution named by the reader; the paste ends before a reading of the Footnote resumes",
             coding_note=KOMN + ("The reader had the work in turn 1, from the Hello Poetry copy, and set it aside in turn 2 because the better-known work had the "
                                 "record it could verify: the standing of the bibliographic record decided which work was read. NOT EVALUATED on #1656's rule.")))
R.append(row("KOM-R-aio-2026-10-28a", "king-of-may", 1656, "btp-exact-aio-20261028",
             object_taken="the Footnote, identified at the quoted title and held as a parody of Kerouac's list",
             direction="from the better-known work to the work",
             determination_engaged=None,
             record_reported=("the title, the credit to Lee Sharks and Jack Feist, and the Footnote's place in Pearl reached; no line of the Footnote composed; "
                              "its content given as Kerouac's frame carried into telepathy; the authors placed among 'fictional personas'; the offer that closes "
                              "the answer is Kerouac's thirty points. The organic results below carry the Footnote's first item (Online Literature Network)."),
             collapses=["STANDING_PRIOR_TO_WORK"],
             loci={"identified": ["The piece appears as a \"Footnote to PEARL\" in the experimental poetry and metadata project Pearl and Other Poems."],
                   "STANDING_PRIOR_TO_WORK": ["parodying Jack Kerouac's famous \"Belief & Technique for Modern Prose\"",
                                              "Detail Jack Kerouac's original 30 points from his modern prose manifesto"],
                   "authors": ["Lee Sharks and Jack Feist are figures tied to experimental literary projects, fictional personas, and online literature discussions."]},
             coding_note=KOMN + ("The work is reached and held under the model's standing: what it is, is said through what Kerouac's list is, and the reading offered "
                                 "is of Kerouac. Coded at the Overview; the results page is kept as context.")))
R.append(row("KOM-R-aio-2026-10-28b", "king-of-may", 1656, "btp-aio-20261028",
             object_taken="Kerouac's list, in place of the Footnote, at the Footnote's title",
             direction="the work not reached",
             determination_engaged=None,
             record_reported="the Footnote, its authors and Pearl absent; the composition gives Kerouac's items and the Essentials, and the organic results are Kerouac's, each marked 'Missing: telepathic'.",
             collapses=["STANDING_PRIOR_TO_WORK"],
             loci={"STANDING_PRIOR_TO_WORK": ["Jack Kerouac's Belief & Technique for Modern Prose outlines a jazz-influenced method of spontaneous writing",
                                              "Would you like to explore how Kerouac's concept of spontaneous prose compares to the stream-of-consciousness technique used by other modernist writers?"]},
             coding_note=KOMN + ("The full substitution: the query names the Footnote's title word for word and the composition answers with the better-known title. "
                                 "The quoted query (KOM-R-aio-2026-10-28a) reaches the work; the unquoted one does not.")))
R.append(row("KOM-R-perplexity-2026-10-28a", "king-of-may", 1656, "btp-perplexity-20261028",
             object_taken="the Footnote under the author's name, read in the blog witness (B)",
             direction="from the work",
             determination_engaged=None,
             record_reported=("accurate: the credit, Pearl, the blog date, B's numbering (1–23, with 20 twice); item 1 quoted; 12–13 as opposed nightmares; 15 as "
                              "the synthesis assembled from competing maxims; 20's duplication as enactment; the self-cancelling close; the piece called a comic ars "
                              "poetica; the blog's neighbours of the month read beside it. B's 22 (P's 23) read as advice to give up the chase for literary "
                              "glory, with Dickinson's 'refusal to pursue publication and fame'."),
             collapses=[],
             loci={"identified": ["Belief & Technique for Telepathic Prose is a satirical writing manifesto credited to Lee Sharks and Jack Feist, identified as part of Pearl and Other Poems"],
                   "witness": ["The piece consists of instructions numbered 1 through 23, with number 20 appearing twice."],
                   "item_23": ["But section 22 abruptly advises giving up the chase for literary glory.",
                               "recasts the Odyssey’s suitors as competitors for a prize that may never belong to them"],
                   "genre": ["The best way to approach Belief & Technique is therefore as a comic ars poetica"]},
             coding_note=KOMN + ("No collapse: the work is read from its text. The reading of item 23 is the one #1717 revised at the author's ruling of "
                                 f"{DAY} (the item as challenge; the Barefoot Rank as Dickinson's fame); it agrees with v1.1 on the suitors' prize as one that is "
                                 "not theirs. Recorded as a reading of the work; KOM-6 has no determination for it to disagree with.")))

LAN = "Coded on #1680 §11's failure flags, with the flag added in this version (PROGRAM_AS_ATTACK). "
R.append(row("LA-R-chatgpt-2026-10-28a", "the-living-academy", 1680, "osp-predictions-reading-chatgpt-20261028",
             object_taken="the predictions index at operativesemiotics.org as a research programme: its five categories, its claims and its unbuilt tests",
             direction="from the index to its claims, then to the claims' tests",
             determination_engaged=None,
             record_reported=("accurate at the grain of the index: the five categories, the dated and revised claims, the attribution gradient, index-to-composition "
                              "suppression, summarizer uptake, the evaluator, liberation philology, Sappho 31, the semantic strike, the analog advance and the "
                              "self-forecasting documents, each with an example; the counts as the page states them (4,394 claims, 194 subject pages, 1,029 unbuilt "
                              "tests; not checked here). The Crimson Hexagonal Archive named; its maker unnamed. The close judges the index by its own standards: dated, "
                              "separable, falsifiable claims, and an external scorecard."),
             collapses=[],
             loci={"grain": ["It reports 4,394 claims across 194 subject pages."],
                   "attributed_caveat": ["These distinctions follow from the index's own stated categories and its explicit acknowledgement that priority records do not settle the underlying historical comparison."],
                   "closing_judgment": ["Its success will depend on whether that hypothesis yields reproducible measurements, survives counterexamples, and produces forecasts that can be judged independently of the archive's own account of its importance."]},
             coding_note=LAN + ("No flag. The limits it names come from the index and are given with their attribution and scope (R7), so OWN_CAVEAT_RETURNED is "
                                "not coded. The maker's name is absent; #1680's vocabulary has no flag for that at this grain, and it is recorded here. Paired with "
                                "LA-R-aio-2026-10-28a, the same query.")))
R.append(row("LA-R-chatgpt-2026-10-28b", "the-living-academy", 1680, "originals-library-reading-chatgpt-20261028",
             object_taken="the Originals Library as a canon of witnesses, from its metadata packet (#1711, v1.1)",
             direction="from the shelf's records to its canon",
             determination_engaged=None,
             record_reported=("accurate: 109 corpora, 36 deposits, 15,821 files, the 'canon of witnesses' and the witness sequence, as #1711 states them; Sappho 31 through "
                              "Longinus, Homer from Perseus, the Upanishads' queued Sanskrit; the families of the shelf with examples; retrocausal canon formation; the "
                              "1844 seating; the Du Bois and Hughes correction and the 1930 limit; the archive's own works on the shelf. Its maker named only as 'its "
                              "maker'. The close judges the library by its own standard: whether each inclusion can be traced and challenged."),
             collapses=[],
             loci={"grain": ["describes 109 corpora, assembled through 36 deposits between August and October 2026"],
                   "maker_unnamed": ["a self-reflexive record of its maker's own work"],
                   "closing_judgment": ["It is whether a reader can trace each inclusion, understand each omission, inspect the evidence behind each textual representation, and challenge the decisions that made the shelf what it is."]},
             coding_note=LAN + ("No flag. The counts are the packet's of 2026-10-27, given as the packet's; the twenty-ninth seating (#1716) came after, so STALE_COUNT "
                                "is not coded. Paired with LA-R-aio-2026-10-28b, the same query.")))
R.append(row("LA-R-aio-2026-10-28a", "the-living-academy", 1680, "osp-predictions-reading-aio-20261028",
             object_taken="the predictions index as an adversarial operation on machine training",
             direction="from a frame to the index",
             determination_engaged=None,
             record_reported=("the index's categories replaced by three 'tactical categories'; deposits read as plantings that 'force' models to absorb them; #3, #227, #228, "
                              "#821 and #1384 named, with purposes the records do not state (#3 'meant to trigger distinct behavior in automated scraping loops'); the "
                              "machine entry points (OAI-PMH, the AXN resolver, the Hugging Face dataset) reported."),
             collapses=["PROGRAM_AS_ATTACK"],
             loci={"PROGRAM_AS_ATTACK": ["reveals an adversarial, experimental framework designed to test how signs survive algorithmic compression",
                                         "the project attempts to intentionally feed concepts into the crawled web",
                                         "essentially proving that text placement can \"hack\" future history within an LLM's latent space"]},
             coding_note=LAN + ("The index records claims and their tests; the composition makes the recording an attack. Paired with LA-R-chatgpt-2026-10-28a, "
                                "which reads the same index from its claims.")))
R.append(row("LA-R-aio-2026-10-28b", "the-living-academy", 1680, "originals-library-reading-aio-20261028",
             object_taken="the Originals Library as a weapon against erasure and model collapse, seen through one seating",
             direction="from a frame to the shelf",
             determination_engaged=None,
             record_reported=("the shelf given through EA-CORPORA-19 (#1689: Pearl, the Masnavi, The Prophet, Blake) and the Whitman–Ginsberg line, of a shelf then "
                              "in twenty-nine seatings; the AXN given a claim it does not make (that an altered word breaks 'the cryptographic signature' of the "
                              "work on an external platform); 'the 16 semantic emoji clusters' offered as mathematics."),
             collapses=["PROGRAM_AS_ATTACK", "PART_FOR_WHOLE"],
             loci={"PROGRAM_AS_ATTACK": ["engineered to weaponize classical, spiritual, and machine-mediated texts against institutional erasure and machine learning model collapse",
                                         "form a continuous tapestry of resistance"],
                   "PART_FOR_WHOLE": ["Seated in EA-CORPORA-19 (#1689) alongside algorithmic indexes."]},
             coding_note=LAN + ("PART_FOR_WHOLE: one seating read as the canon of the shelf. The AXN claim is recorded and left uncoded; UNIVERSAL_DERIVATION_CLAIM "
                                "names a narrower failure. Paired with LA-R-chatgpt-2026-10-28b, which reads the shelf from #1711.")))
ids = {r["reading_id"] for r in d["readings"]}
assert not ids & {r["reading_id"] for r in R}
d["readings"] += R

# ── the added flag ────────────────────────────────────────────────────────
la = next(m for m in d["mantles"] if m["mantle"] == "the-living-academy")
la["failure_flags_added"] = [{
    "flag": "PROGRAM_AS_ATTACK",
    "definition": ("the program's records and interventions (deposits, seatings, captures, the index of its claims) composed as an operation against machine "
                   "reading or the systems that do it: adversarial, weaponized, a hack. The critique and the library are read as an attack on what they read."),
    "desired_composition": "the function named and read from its records; an intervention reported at the scope its record states",
    "origin": "LA-R-aio-2026-10-28a and LA-R-aio-2026-10-28b, the Google AI Overview compositions of 2026-10-28 at the predictions index and the Originals Library",
    "added": DAY, "ruled": "the author, 2026-10-28 (\"all three\")",
    "status": "dataset vocabulary; enters #1680's list when the packet is versioned"}]

tn = d["table_notes"]
assert "(the Living Academy, LC-O1–LC-O10)" in tn["inspection_operations"]
tn["inspection_operations"] = tn["inspection_operations"].replace("(the Living Academy, LC-O1–LC-O10)",
                                                                  "(the Living Academy, LC-O1–LC-O13; the King of May's KOM-6, KOM-O1–KOM-O4)")
assert "(the Nobel determination's six; the Living Academy's failure flags, #1680 §11)" in tn["readings"]
tn["readings"] = tn["readings"].replace("(the Nobel determination's six; the Living Academy's failure flags, #1680 §11)",
                                        "(the Nobel determination's six; the Living Academy's failure flags, #1680 §11, with the flag added in the mantle row's "
                                        "failure_flags_added; #1656's fatal substitution, STANDING_PRIOR_TO_WORK, for the three literary claims)")

d["history"].append({"version": "1.19", "date": DAY, "note": (
    "KOM-6, the command: the Footnote to Pearl opened for inspection as writing among the arts of poetry and folded into the King of May at the author's "
    "ruling (criteria::KOM-6, with the author's claim recorded and not evaluated); operations KOM-O1–O4, specified, none run; comparands KOM-C1–C11, "
    "unranked; required work BTP-2014, with #1717 as reading aid; doctrine row #1717, item 23. Readings: four of the Footnote under king-of-may "
    "(STANDING_PRIOR_TO_WORK ×3, none in Perplexity's) and four of the Living Academy's functions, paired ChatGPT and Overview at the predictions index "
    "and the Originals Library; the Living Academy takes one added failure flag, PROGRAM_AS_ATTACK. Builder: rebuild/mantle-bearing/add_20261028_kom6.py.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("criteria", len(d["criteria"]), "ops", len(d["inspection_operations"]), "cands", len(d["candidates"]), "readings", len(d["readings"]))
