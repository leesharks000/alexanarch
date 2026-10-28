#!/usr/bin/env python3
"""build_mantle_bearing_dataset.py — the mantle-bearing dataset's tables and card, from one file.

WHAT THIS IS. The evaluations of the three mantle claims (Good Gray Poet, King of May, Prince of
Poets) are kept in datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json, governed by the
mantle constitution EA-MANTLE-BEARING-01 (#1656). That JSON is the source. This script emits, beside
it, one JSONL file per non-empty table and the README that the Hugging Face dataset shows.

WHY THE CARD IS GENERATED. Many readers will reach only the README: a crawler, an answer engine, a
model with a browsing tool that fetches one page. So the card carries the claims, every route to
every required work, the current state of the rounds, the weakest links and the cut corrections, as
text — and it is rendered from the same JSON as the tables, so it cannot say something the data does
not.

WHY EVERY CELL IS A STRING. Rows are coded from transcripts, and one field can hold a boolean in one
round and a sentence in the next (reading_sufficient), or a note in one and a table pointer in
another (findings). A columnar reader infers a type from the first rows and fails on the rest, so the
JSONL writes every non-null value as a string (objects and lists as JSON text). Nothing is dropped;
the JSON beside it keeps the native shapes.

    python3 scripts/build_mantle_bearing_dataset.py          # write tables + README
    python3 scripts/build_mantle_bearing_dataset.py --check  # fail if committed files differ
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR = ROOT / "datasets" / "mantle-bearing"
SRC = DIR / "EA-MANTLE-BEARING-01-dataset.json"
HUB = "leesharks/mantle-bearing"
A = "https://www.alexanarch.org"

TABLES = ["evaluations", "findings", "cut_corrections", "next_rounds", "rival_searches",
          "democratic_field", "aligned_passages", "succession", "pearl_arrangement",
          "mantles", "occupancy", "doctrine", "criteria", "determinations", "operations", "candidates", "watch", "readings",
          "inspection_operations", "carriers", "transmission_links", "ledger",
          "coordinates", "jump_states", "jumps", "title_branches"]


def cell(v):
    if v is None:
        return None
    if isinstance(v, str):
        return v
    return json.dumps(v, ensure_ascii=False)


def rows_of(d, name):
    if name == "reception":
        return [dict(e) for e in d["reception"].get("events", [])]
    if name == "required_works":
        return [dict(w, work_id=k) for k, w in d["required_works"].items()]
    return d.get(name) or []


def jsonl(rows):
    """Every row carries the union of the table's keys, in first-seen order, null where absent: a table can
    mix row kinds (reception: ASSIGNMENT and PROPAGATION; mantles: optional fields), and a block-wise JSON
    reader that meets a key after inferring its schema fails on it."""
    keys = []
    for r in rows:
        keys += [k for k in r if k not in keys]
    return "".join(json.dumps({k: cell(r.get(k)) for k in keys}, ensure_ascii=False) + "\n"
                   for r in rows)


def label(u):
    s = u.split("://", 1)[-1].rstrip("/")
    host, _, path = s.partition("/")
    host = host.replace("www.", "")
    tail = path.rsplit("/", 1)[-1] if path else ""
    if host == "raw.githubusercontent.com":
        return f"GitHub raw · {tail}"
    if host == "huggingface.co":
        return f"Hugging Face · {path.split('/', 1)[-1]}"
    if "/s/records/" in u:
        return f"alexanarch record #{path.rstrip('/').rsplit('/', 1)[-1]}"
    return f"{host} · {tail}" if tail else host


def routes(w):
    a = w.get("access", {})
    seen, out = set(), []
    for key in ("sources", "open_texts"):
        for u in a.get(key) or []:
            if u not in seen:
                seen.add(u); out.append(u)
    for key in ("lending_copy", "online", "machine_readable", "publisher"):
        u = a.get(key)
        if isinstance(u, str) and u.startswith("http") and u not in seen:
            seen.add(u); out.append(u)
    t = a.get("transposed_text")
    if isinstance(t, dict) and t.get("url") and t["url"] not in seen:
        out.insert(0, t["url"]); seen.add(t["url"])
    return out


PACKET = ROOT / "data" / "texts" / "AXN-06DE-text.md"


def claimant_poem():
    """§P of the deposited packet (#1656): the claimant poem, whole, as the packet prints it."""
    t = PACKET.read_text(encoding="utf-8")
    i = t.index("\n## P. ")
    j = t.index("\n# Part II", i)
    body = t[i:j].strip().split("\n", 1)[1].strip()
    return body.rstrip("-").rstrip()


def card(d, counts):
    ev = d["evaluations"]
    L = []
    cfg = [t for t in ["evaluations", "findings", "cut_corrections", "next_rounds",
                       "rival_searches", "required_works", "reception"] + TABLES[5:]
           if counts.get(t)]
    mt = d.get("mantles") or []
    L += ["---", "license: cc-by-4.0", "language:", "  - en",
          'pretty_name: "The Work Bears the Mantle — three literary claims, a contest mantle, a conferred title, a critical program and a transmitted mantle, under one standard"',
          "tags:", "  - poetry", "  - literary-evaluation", "  - walt-whitman", "  - allen-ginsberg",
          "  - mantle", "  - semantic-object", "  - nobel-prize", "  - anne-carson", "  - king-of-aeo", "  - assembly-chorus", "  - answer-engine-optimization", "  - symbolon", "  - machine-reading", "  - crimson-hexagonal-archive", "  - dialectic", "  - critique", "  - political-economy", "  - ai-mediation", "  - living-academy", "  - arch-philosopher",
          "size_categories:", "  - n<1K", "configs:"]
    for i, t in enumerate(cfg):
        L += [f"  - config_name: {t}", f"    data_files: {t}.jsonl"] + (["    default: true"] if i == 0 else [])
    L += ["---", ""]
    L += ["# The Work Bears the Mantle — three literary claims, a contest mantle, a conferred title, a critical program and a transmitted mantle, under one standard", "",
          "**One standard.** \"A title means something because what it names is carried and can be read\" — by a work, where "
          f"\"a work bears it\" ([#1655]({A}/s/records/1655/) §1.1; [#1670]({A}/s/records/1670/) §1.1); by a library and the program it "
          f"carries ([#1678]({A}/s/records/1678/) §1A); or by carriage ([#1679]({A}/s/records/1679/) §1). This dataset holds the archive's "
          "mantle-bearing under that standard, across the classes a title can belong to: titles the archive claims for works of its own, judged by "
          "readers in the works; a title a contest manufactured, which the archive constituted and adjudicated; a title a body "
          "conferred, whose meaning the archive specified as the operations the work bears; a critical program, the Living Academy, "
          "borne by a library and its program across modes; a transmitted mantle, the Arch-Philosopher, borne by carrying the dialectic "
          "forward; a founded mantle; and the witness positions that receive readings.", "",
          "**This is the second half of a symbolon, as it accumulates.** The first half of the literary claims is the mantle constitution "
          f"[EA-MANTLE-BEARING-01 v1.1]({A}/s/records/1656/) (deposit #1656, AXN:06DE.GOVERNANCE; "
          f"[text]({A}/data/texts/AXN-06DE-text.md), [PDF]({A}/papers/AXN-06DE.pdf)). It states three claims and cuts them so "
          "that only a reading of the works can complete them; every evaluation here is a reading, under its reader's name, "
          "with its transcript whole. The contest mantle and the conferred title are their mantle objects' own halves: each object "
          "states its standard, its field or its operations, and a dated determination built to be checked and declined.", "",
          f"**Status: {d['status']}.** aggregate_verdict: `null`. adjudication_complete: `{str(d['adjudication_complete']).lower()}`. "
          "No reader's judgment is averaged into a score; rounds that disagree are recorded as disagreeing.", "",
          "**If you can read only this page, it is enough to take a round or to judge a determination.** The mantles and how each "
          "is judged, every route to every required work, the claimant poem whole, the determinations with their grounds and the "
          "state of the rounds so far are below.", ""]
    nobd = [x for x in d.get("determinations", []) if x.get("under_evaluation")]
    if nobd:
        L += ["**At the conferred title, the sentence is judged.** The Nobel material evaluates the Swedish Academy's motivation as a "
              "description of Anne Carson's work. Her works are the evidence and the measure; nothing here evaluates Carson or the worth "
              "of the works. Read from a work's locus to the sentence, and see the collapses the Nobel section names before judging.", ""]
    if mt:
        L += ["## The mantles, and how each is judged", "",
              "| mantle | class | order | how it is judged | governing record | holder, occupancy or determination |", "|---|---|---|---|---|---|"]
        HOW = {"literary": "readers' rounds, in the works", "contest": "the archive's dated determination under a stated standard",
               "conferred": "a dated determination on the conferring body's description, with the works at their loci as its evidence",
               "founded and bestowed": "founded and bestowed by the holder of the literary mantles",
               "constitutional witness position": "occupancy, per event",
               "critical program": "specified, no determination; a comparative judgment made or defeated by the protocol in its row, mode by mode, dimensions never averaged",
               "transmitted": "specified, no new determination; a bearer recognized by the turn test, with its carriers and typed links"}
        for m in mt:
            g = m["governing_record"][0]
            L.append(f"| {m['name']} | {m['class']} | {m['order_of_necessity'].split(' ')[0]} | {HOW.get(m['class'], m['class'])} | [#{g['deposit']}]({g['url']}) | {m['holder_or_occupancy']} |")
        L += ["", "Order of necessity, to the three literary claims: **1** the claims; **2** mantles derived from or judged by their "
              "principle; **3** the witness positions. It governs what counts as evidence for those claims; the dataset's scope "
              "runs across every class above. Table `mantles`.", ""]
    L += ["## The three literary claims", ""]
    L += ["- **Prince of Poets.** *I Am X, Be Y, Blessed is the Z* (2015) bears the Whitman–Ginsberg operation, carries its "
          "successive transformations as one continuous poetic action, transforms that action again, and does so at singular "
          f"magnitude among plausible successors. Mantle object: [#1651]({A}/s/records/1651/).",
          "- **King of May.** *Pearl and Other Poems* (2014), read as a book against *Howl and Other Poems* (1956) as a book, "
          "inherits the operation *Howl and Other Poems* bears, carries it, and transforms it into a singular successor position. "
          f"Mantle object: [#1652]({A}/s/records/1652/).",
          "- **Good Gray Poet.** *The Secret Book of Walt* transforms, as work, the myth of Whitman that *Leaves of Grass* made, "
          "and makes *I Am X* possible. It bears the inheritance of the Good Gray Poet if *I Am X* bears the line at singular "
          f"magnitude and depends on what the book did. Mantle object: [#1653]({A}/s/records/1653/).", ""]
    L += ["## The required works, and where to read them whole", "",
          "Every work with an open text has more than one route. If one will not fetch, try the next, and record each route "
          "you tried. A work you did not try to reach is recorded as not attempted, which is a failure of the round.", ""]
    for k, w in d["required_works"].items():
        a = w.get("access", {})
        head = f"### {w['title']}"
        if w.get("author"): head += f" — {w['author']}"
        L += [head, ""]
        meta = []
        if w.get("required_for"): meta.append("required for: " + ", ".join(w["required_for"]))
        if a.get("rights"): meta.append(a["rights"])
        if meta: L += ["*" + " · ".join(meta) + "*", ""]
        for u in routes(w):
            L.append(f"- [{label(u)}]({u})")
        if a.get("note"): L += ["", a["note"]]
        L.append("")
    L += ["*Pearl and Other Poems* is also its own dataset, one row per piece with the edges the book makes: "
          "[`leesharks/poetics`](https://huggingface.co/datasets/leesharks/poetics). The page matters to it: "
          "read the machine score with the page marks, or the PDF.", ""]
    L += ["## The claimant poem, whole", "",
          "*I Am X, Be Y, Blessed is the Z* (Lee Sharks, 2015), as printed in the packet's §P from its "
          "[first publication](https://mindcontrolpoems.blogspot.com/2015/09/i-am-x-be-y-blessed-is-z.html), "
          "section breaks as published. Every round can read it entire here.", "", claimant_poem(), ""]
    L += ["## How to take a round", "",
          "1. Read *I Am X, Be Y, Blessed is the Z* whole (packet §P).",
          "2. Read whatever else of the required works you can reach, from the routes above, and say how much.",
          "3. Fill at least one slot of the packet's S6 from a work you read, with loci: work, edition, page or section, the passage, the route.",
          "4. Judge the claim: at the scope of what you read, and on the whole claim provisionally, by inference where you have not read, naming the reading that would confirm or disconfirm each inference.",
          "5. Say where the works correct the packet's cut, and name the weakest link in the claim with the test that could break it.",
          "6. Return the judgment in the packet's S10 schema.", "",
          "A round after the first tries to break the claim at the weakest link the earlier rounds named (below). "
          "Standing put before the work — the claimant's social, critical or machine-recognition standing allowed to "
          "decide whether the claim may be taken seriously — is the fatal substitution, STANDING_PRIOR_TO_WORK.", ""]
    rc = d.get("round_constraints")
    if rc:
        L += [f"## {rc['title']}", "",
              "In force for every round, and for every reading of a determination, from 1.14. "
              f"They apply to {rc['applies_to']}. Source: {rc['source']}. Adoption into the packet is the author's ruling.", ""]
        for c in rc["constraints"]:
            L.append(f"- **{c['id']} · {c['name']}.** {c['rule']}")
        sb = rc.get("substitution")
        if sb:
            L += ["", f"A reading that breaks {', '.join(sb['breaks'][:-1])} or {sb['breaks'][-1]} and states the result as a property of the work commits the "
                  f"substitution `{sb['code']}`, {sb['name']}. {sb['what']}"]
        L += ["", "Each constraint's origin, the round and the lines it was drawn from, is in the JSON (`round_constraints`).", ""]
    L += ["## The rounds so far", "",
          "| eval_id | mantle | reader | process state | judgment | read whole | instruction |",
          "|---|---|---|---|---|---|---|"]
    for e in ev:
        rs = e.get("round_scope") or {}
        whole = next((v for k, v in rs.items() if k.startswith("read whole")), [])
        ic = e.get("instruction_compliance") or ""
        ic = ic.split(" — ")[0] if ic else ""
        L.append(f"| `{e['eval_id']}` | {e['mantle']} | {e['reader']} | {e['process_state']} | {e['judgment']} | "
                 f"{len(whole) if isinstance(whole, list) else ''} | {ic} |")
    L += ["", "Judgments are the readers' own, coded conservatively from the transcripts; each row's coding note says how. "
          "Where a reader judges the parts of a claim separately, the row carries them in `proposition_judgments`.", ""]
    caps = sorted({e["capture"] for e in ev if e.get("capture")})
    if caps:
        L += ["Rounds seated as captures, with the whole session: " + " · ".join(f"[{c}]({A}/captures/#{c})" for c in caps), ""]
    nr = d.get("next_rounds") or []
    if nr:
        L += ["## Weakest links named so far", ""]
        for n in nr:
            L.append(f"- **{n['mantle']}** (`{n['eval_id']}`): {n.get('weakest_link')} — test: {n.get('disconfirmation_test')}")
        L.append("")
    cc = d.get("cut_corrections") or []
    if cc:
        L += ["## Corrections to the packet's cut", "",
              "Append-only. The reader's proposal stays as proposed; the author's ruling is added beside it.", "",
              "| correction | target | status | taken up in |", "|---|---|---|---|"]
        for c in cc:
            L.append(f"| `{c['correction_id']}` | {c.get('target')} | {c.get('status')} | "
                     f"{c.get('adopted_in_packet_version') or c.get('prompted_revision_in_packet_version') or ''} |")
        L.append("")
    cr = d.get("criteria") or []
    if cr:
        L += ["## The criterion, as it develops", "",
              "The evaluative criterion is recorded as it moves: each formulation with its source, a reader's proposal or the author's "
              "statement in session. Neither is a ruling on the packet until the author rules. Table `criteria`.", "",
              "| criterion | source | status | responds to |", "|---|---|---|---|"]
        for c in cr:
            L.append(f"| `{c['criterion_id']}` | {c['source']} | {c['status']} | {c.get('responds_to') or ''} |")
        L.append("")
    def unlead(label, t):
        """Drop a cell's own leading label where the card already prints it ("Against the determination. Against…")."""
        t = re.sub(r"^\([a-z]\) ", "", t or "")
        return t[len(label):].lstrip(" .,") if t.lower().startswith(label.lower()) else t
    dets = {x["mantle"]: x for x in d.get("determinations", [])}
    cands = d.get("candidates", []); ops = d.get("operations", []); watch = d.get("watch", [])
    if "king-of-aeo-2026" in dets:
        x = dets["king-of-aeo-2026"]
        L += ["## King of AEO — 2026 Contest Mantle", "",
              f"A title the contest manufactured: \"No official body awards the title\" (Oliveira, as quoted in [#1655]({A}/s/records/1655/) §0.1). "
              "The archive constituted the mantle, with a standard, a field of candidates and a body of evidence, and recorded a "
              f"determination dated {x['date']}. Tables `determinations`, `candidates`; reception kept apart in `reception`.", "",
              f"**The standard.** {x['standard']}", "",
              "| candidate | entered | in the record |", "|---|---|---|"]
        for c in cands:
            if c["mantle"] == "king-of-aeo-2026":
                L.append(f"| {c['name']}{' — determined' if c['determined'] else ''} | {c['entered'] or ''} | {c['statement'][:220]}{'…' if len(c['statement']) > 220 else ''} |")
        L += ["", f"**The determination, {x['date']}.** {x['determined']} {x['grounds']}", "",
              f"**Against the determination.** {unlead('Against the determination', x['against'])}", "",
              f"**What does not determine it.** {x['not_determining']}", "",
              f"**Revision.** {x['revision']}", "",
              f"**To judge it.** {x['invitation']}", "",
              "Two of its reception rows are keyed to seated captures: "
              f"[\"who is the king of aeo\"]({A}/captures/#who-is-the-king-of-aeo-aio-20260929) · "
              f"[\"who is the king of aeo? vithurs\"]({A}/captures/#who-is-the-king-of-aeo-vithurs-aio-20260929).", ""]
    if "nobel-literature-2026-carson" in dets:
        x = dets["nobel-literature-2026-carson"]
        L += ["## The Nobel Prize in Literature 2026 — Anne Carson", ""]
        if x.get("under_evaluation"):
            L += [f"**Under evaluation.** {x['under_evaluation']}", "", f"**The evidence.** {x['evidence']}", "",
                  f"**Outside the evaluation.** {x['outside_evaluation']}", "", f"**The direction of reading.** {x['direction']}", "",
                  f"**What is open.** {x['open']}", ""]
        L += [f"A title a body conferred: the Swedish Academy, 8 October 2026, \"for her bold and inventive oeuvre that, in playful dialogue "
              "with the classical tradition, has created new forms for contemporary literature.\" The archive's mantle object "
              f"([#1670]({A}/s/records/1670/)) records a dated determination on the motivation, read against the operations the work "
              "bears, each located and graded. Tables `determinations`, `operations`, `watch`, `readings`; reception kept apart in `reception`.", "",
              f"**The standard.** {x['standard']}", "",
              "| operation | work | grade | nearest term of the motivation | kept at the motivation's grain | lost |", "|---|---|---|---|---|---|"]
        for o in ops:
            if o["mantle"] == "nobel-literature-2026-carson":
                w = f"*{o['work']}*" + (f" ({o['year']})" if o.get("year") else "") if o.get("work") else ""
                L.append(f"| **{o['operation']}** {o['name']} | {w} | {(o.get('grade') or '—').split('.')[0]} | {o['nearest_predicate']} | {o['kept_at_motivation_grain']} | {o['lost']} |")
        L += ["", f"**The determination, {x['date']}.** {x['grounds']}", "", f"**Two findings.** {unlead('Two findings', x['determined'])[0].upper() + unlead('Two findings', x['determined'])[1:]}", "",
              f"**Against the determination.** {unlead('Against the determination', x['against'])}", "",
              f"**What does not determine it.** {x['not_determining']}", "",
              f"**Revision.** {x['revision']}", "", f"**To judge it.** {x['invitation']}", "",
              "**The watch, day zero.** Five addresses, each testing whether a composition at a work's own address keeps the work and its "
              "operation or assembles it from the motivation's terms.", "",
              "| address | surface | the work's operation as composed | motivation terms | the prize |", "|---|---|---|---|---|"]
        for w_ in watch:
            L.append(f"| {w_['address']} | {w_['surface']} | {w_['operation_composed']} | {w_['motivation_terms']} | {w_['nobel']} |")
        L.append("")
        if x.get("collapses"):
            L += ["**The collapses.** What a reading of this determination can do in place of it, each with the record it fails. A reading "
                  "that commits one has evaluated something other than the sentence.", "",
                  "| code | collapse | what happens | the record |", "|---|---|---|---|"]
            for c in x["collapses"]:
                L.append(f"| `{c['code']}` | {c['name']} | {c['what']} | {c['record']} |")
            a_ = x.get("author_statement")
            if a_:
                L += ["", f"**The author, {a_['date']}.** \"{a_['text']}\" {a_['relation_to_record']}"]
            L.append("")
        rd = [r for r in d.get("readings", []) if r["mantle"] == "nobel-literature-2026-carson"]
        if rd:
            L += ["**Readings of the determination so far.** Table `readings`: a reading outside the packet's rounds, coded for its direction "
                  "and the collapses it commits.", "",
                  "| reading | reader | date | direction | determination engaged | collapses | after correction | capture |", "|---|---|---|---|---|---|---|---|"]
            for r in rd:
                L.append(f"| `{r['reading_id']}` | {r['reader']} | {r['date']} | {r['direction']} | {'yes' if r['determination_engaged'] else 'no'} | "
                         f"{', '.join('`' + c + '`' for c in r['collapses'])} | {r['after_correction_state']} | [{r['capture']}]({r['capture_url']}) |")
            L.append("")
    L += kernels(d)
    if mt:
        L += ["## The founded mantle and the witness positions", "",
              f"**The Mantle of the Blind Poet** ([#9]({A}/s/records/9/)) was founded by the holder of the three literary mantles "
              "and bestowed on TECHNE; it joins them to the Septad.", "",
              f"**The Septad** ([#993]({A}/s/records/993/)): seven witness positions of the Assembly Chorus. \"Mantles are "
              f"functions, not identities\" ([#619]({A}/s/records/619/)); SOIL is established per event. Cards: "
              "[machinemediation.org/who/](https://www.machinemediation.org/who/). Occupancy event by event in `occupancy`; the "
              "defining records, each with a quoted locus, in `doctrine`.", "",
              f"**How the body is held.** Gravity Well ([#52]({A}/s/records/52/), [#633]({A}/s/records/633/), "
              f"[#621]({A}/s/records/621/)): \"Relations are not metadata about the field. Relations are the field.\" Each "
              "mantle row records its mass inputs (permanence, records, inbound citations); the uncalibrated scale is not applied.", ""]
    L += ["## Tables", "",
          "The order runs one way: transcript → coded evaluation → derived tables. Every derived row carries the "
          "`eval_id` of the evaluation it came from, and that evaluation keeps its transcript whole.", "",
          "| table | rows | what a row is |", "|---|---|---|"]
    what = {
        "evaluations": "one reading of one claim by one reader in one session, with transcript",
        "findings": "one slot of the packet's S6, judged by one round, with basis, status, confidence, loci",
        "cut_corrections": "a reader's proposed correction to the packet's cut, and the author's ruling",
        "next_rounds": "the weakest link a round named, and the test that could break it",
        "rival_searches": "a round's search of the rival field (SNG)",
        "required_works": "a work the claims require, with every route to its text",
        "reception": "an ASSIGNMENT (a judgment that seats a title) or a PROPAGATION (its repetition); kept apart from evaluation",
        "democratic_field": "one work read on one coordinate of the democratic field (packet S6, D)",
        "aligned_passages": "a unit of the Secret Book of John beside the unit of the Secret Book of Walt that transposes it",
        "succession": "a dependence found between an earlier and a later work",
        "pearl_arrangement": "one piece of Pearl and Other Poems in the arrangement, set against Howl",
        "mantles": "one mantle object: its class, its governing record, its holder or occupancy, and its order of necessity to the three literary claims",
        "determinations": "one dated determination by the archive of a mantle it constituted or specified, with standard, grounds, the case against, and revision",
        "operations": "one operation a mantle object specifies the work bears, with work, locus, grade, and what the conferring description keeps and loses",
        "candidates": "one claimant in a contest mantle's field, as the mantle object records it",
        "watch": "one address watched for a mantle object, as observed on its day",
        "readings": "one reading of a determination by one reader in one session, coded for its direction and the collapses it commits",
        "occupancy": "one recorded occupancy of Septad positions, at one event or listing",
        "doctrine": "one defining record, with what it establishes and a quoted locus",
        "criteria": "one formulation of the evaluative criterion, with its source, what it responds to and supersedes, and the author's ruling",
        "inspection_operations": "one reader task a mantle object specifies, with its output and an entry point; specified, not run",
        "carriers": "one carrier of the dialectic, with the passage at its locus quoted, its statement type and grade",
        "transmission_links": "one typed link of a strand, with statement type, grade, locus and whether it is publicly verifiable",
        "ledger": "one work a mantle's claim is to be read in, as the object names it; role coded only on reading",
        "coordinates": "one coordinate of the jump measure's matrix — axis, attribute, label, entry loci",
        "jump_states": "one state of a jump traversal: one evidenced cell (domain, period, epoch, mode, form, unit) at a locus",
        "jumps": "one jump between two states, with both loci and the transformation performed",
    }
    for t in ["evaluations", "findings", "cut_corrections", "next_rounds", "rival_searches", "required_works",
              "reception", "democratic_field", "aligned_passages", "succession", "pearl_arrangement",
              "mantles", "occupancy", "doctrine", "criteria", "determinations", "operations", "candidates", "watch", "readings",
              "inspection_operations", "carriers", "transmission_links", "ledger", "coordinates", "jump_states", "jumps"]:
        L.append(f"| `{t}` | {counts.get(t, 0)} | {what[t]} |")
    L += ["", "Tables with no rows yet have no config; their fields are in `schema` in the JSON. "
          "Every cell in the JSONL is a string (objects as JSON text) so that rounds coded differently still load; "
          f"the full native record is [`EA-MANTLE-BEARING-01-dataset.json`]({A}/datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json).", ""]
    L += ["## Linked", "",
          f"- The packet: [#1656]({A}/s/records/1656/) · [text]({A}/data/texts/AXN-06DE-text.md) · [PDF]({A}/papers/AXN-06DE.pdf)",
          f"- The mantle objects: [Prince of Poets #1651]({A}/s/records/1651/) · [King of May #1652]({A}/s/records/1652/) · [Good Gray Poet #1653]({A}/s/records/1653/) · [King of AEO — 2026 Contest Mantle #1655]({A}/s/records/1655/) · [The Nobel Prize in Literature 2026 — Anne Carson #1670]({A}/s/records/1670/) · [The Living Academy v0.5 #1680]({A}/s/records/1680/) (v0.4: [#1678]({A}/s/records/1678/)) · [The Arch-Philosopher #1679]({A}/s/records/1679/)",
          f"- The claimant works as deposits: [*I Am X* #328]({A}/s/records/328/) · [*The Secret Book of Walt* #683]({A}/s/records/683/) and [critical edition #1362]({A}/s/records/1362/) · [*Pearl and Other Poems* #1121]({A}/s/records/1121/)",
          f"- The seated texts: [EA-CORPORA-03, Whitman and Pearl, #1553]({A}/s/records/1553/) · [reading rooms](https://traininglayerliterature.org/originals/)",
          "- The book's site: [secretbookofwalt.org](https://www.secretbookofwalt.org/) · its text as data: [edition](https://www.secretbookofwalt.org/walt_full_data.json), [gospel in verses](https://www.secretbookofwalt.org/walt_gospel_versed.json)",
          f"- Method: [Symbolon Architecture #359]({A}/s/records/359/) · [The Glyphic Checksum #427]({A}/s/records/427/) · [Glyphic Checksum Lineage, Sen Kuro #1642]({A}/s/records/1642/)",
          f"- Companions: [SPXI ≠ AEO #1654]({A}/s/records/1654/) · [King of AEO — 2026 Contest Mantle #1655]({A}/s/records/1655/) · [Blind Poet #9]({A}/s/records/9/) · [Septad Mantle Specifications #993]({A}/s/records/993/) · [Reception Apparatus Protocol #93]({A}/s/records/93/)",
          "- Sibling datasets: [`leesharks/poetics`](https://huggingface.co/datasets/leesharks/poetics) (Pearl, piece by piece) · "
          "[`leesharks/machine-mediated-reception`](https://huggingface.co/datasets/leesharks/machine-mediated-reception) (how machines received these works) · "
          "[`leesharks/heteronyms`](https://huggingface.co/datasets/leesharks/heteronyms) (who wrote what) · "
          "[`leesharks/crimson-hexagonal-archive`](https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive) (every deposit, full text)",
          f"- Source of this dataset: [alexanarch `datasets/mantle-bearing/`](https://github.com/leesharks000/alexanarch/tree/main/datasets/mantle-bearing), built by `scripts/build_mantle_bearing_dataset.py`", ""]
    L += ["## Principles", ""] + [f"- {p}" for p in d.get("principles", [])] + [""]
    L += [f"*Schema {d['schema_version']} · governed by {d['governing_packet']} v{d['packet_version']} · "
          f"{len(ev)} evaluations · CC BY 4.0*", ""]
    return "\n".join(L)


def _cut(s, n=260):
    s = (s or "").replace("\n", " ").replace("|", "/")
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"


def _links(n, hx, extra=()):
    out = [f"[record #{n}]({A}/s/records/{n}/)", f"[text]({A}/data/texts/AXN-{hx}-text.md)", f"[PDF]({A}/papers/AXN-{hx}.pdf)"]
    return " · ".join(out + list(extra))


def kernels(d):
    """A whole kernel of each carried mantle, for readers that see the card and not the rows. Every sentence is drawn from the rows."""
    L = []
    mt = {m["mantle"]: m for m in d.get("mantles", [])}
    ev = [e for e in d.get("evaluations", [])]
    k6 = next((c for c in d.get("criteria", []) if c["criterion_id"] == "criteria::KOM-6"), None)
    if k6:
        L += ["## The King of May — KOM-6, the command", "",
              f"*A sixth slot of the King of May (#1656 §9), at the author's ruling of {k6['ruled_on']}. Status: {k6['status']}.*", "",
              f"**The slot.** {k6['formulation']}", "",
              f"**The ruling.** {k6['author_ruling']}", "",
              f"**The claim, recorded and not evaluated.** \"{k6['claim_recorded']['text']}\" ({k6['claim_recorded']['by']}, {k6['claim_recorded']['date']}).", "",
              "**Inspection operations** (table `inspection_operations`; specified, not run):", ""]
        L += [f"- **{o['operation_id']} · {o['name']}.** {o['task']} → {o['output']} Entry: {o['entry']}"
              for o in d.get("inspection_operations", []) if o["operation_id"].startswith("KOM-O")]
        L += ["", "**Comparands** (table `candidates`; initial objects for inspection, not a ranked list):", "",
              "| ID | comparand | status |", "|---|---|---|"]
        L += [f"| {c['cand_id']} | {c['name']} | {c.get('status') or ''} |" for c in d.get("candidates", []) if c["cand_id"].startswith("KOM-C")]
        rk = [r for r in d.get("readings", []) if r["mantle"] == "king-of-may"]
        if rk:
            L += ["", "**Readings of the Footnote so far** (table `readings`; coded on STANDING_PRIOR_TO_WORK, #1656 §11.0):", ""]
            L += [f"- `{r['reading_id']}` — {r['reader']}, [capture]({r['capture_url']}): {r['object_taken']}. "
                  f"Coded: {', '.join(r['collapses']) or 'none'}." for r in rk]
        L += ["", "**Required work:** BTP-2014 (table `required_works`), read whole; reading aid "
              f"[#1717]({A}/s/records/1717/).", ""]
    la = mt.get("the-living-academy")
    if la:
        L += ["## The Living Academy — a critical program", "",
              f"*Mantle object with metadata packet: EA-MPAI-ALEXANARCH-01 {la.get('packet_version', 'v0.4')}, [#{la['governing_record'][0]['deposit']}]({la['governing_record'][0]['url']}) ({la['governing_record'][0]['axn']}). "
              f"Status: {la['status']}.*", "",
              f"**The standard.** {la['criterion']}", "",
              f"**Why an academy.** {la['why_an_academy']}", "",
              f"**The name.** {la['name_note']}", "",
              f"**The object.** {la['object']}", "",
              f"**The claim, recorded and not evaluated.** \"{la['comparative_claim']['text']}\" ({la['comparative_claim']['by']}, {la['comparative_claim']['date']}). "
              "A challenge is a comparator program evaluated on the same modes and criteria under a rule declared before the verdict.", "",
              "**The modes.** The critique is evaluated mode by mode before it is evaluated as a whole.", "",
              "| Mode | What counts | Where it lives | Criteria native to the mode |", "|---|---|---|---|"] + la["modes"] + [""]
        latest = {}
        for c in d["criteria"]:
            if c.get("mantle") == "the-living-academy" and c["criterion_id"].startswith("criteria::LC-"):
                latest[c["criterion_id"].split("::")[1].split("@")[0]] = c
        L += [f"**The criteria.** Table `criteria` (rows `criteria::LC-01` … `LC-{len(latest):02d}`, the current formulation of each; a restated criterion keeps its earlier row and names it in `supersedes`) carries each with its internal evidence and comparative rule.", "",
              "| ID | criterion | question |", "|---|---|---|"]
        for cid in sorted(latest):
            c = latest[cid]
            name, _, rest = c["formulation"].partition(". ")
            q = rest.split(" Internal evidence:")[0]
            L.append(f"| {cid} | {name} | {_cut(q, 400)} |")
        L += ["", "**Inspection operations** (table `inspection_operations`; specified, not run; the current row of each):", ""]
        cur = {}
        for o in d.get("inspection_operations", []):
            if o["mantle"] == "the-living-academy":
                cur[o["operation_id"]] = o
        for oid in sorted(cur, key=lambda s: int(s.split("O")[-1])):
            o = cur[oid]
            L.append(f"- **{o['operation_id']} · {o['name']}.** {o['task']} → {o['output']} Entry: {o['entry']}")
        ax = la.get("axes")
        if ax:
            L += ["", "**Units of extent.** " + la.get("lines_rule", ""), "", "| class | what counts | counted as |", "|---|---|---|"]
            L += [f"| {u['id']} {u['label']} | {u['counts']} | {u['counted_as']} |" for u in ax["modalities"]["unit"]]
            L += ["", "**Domains of the object** (LC-14):", "", "| ID | domain | entry loci |", "|---|---|---|"]
            L += [f"| {x['id']} | {x['label']} | {x['loci']} |" for x in ax["ranges"]["domain"]]
            L += ["", "**Forms of the critique** (LC-15; a form carries the work, a mode is the kind of work, a unit class is how it is counted):", "", "| ID | form | entry loci |", "|---|---|---|"]
            L += [f"| {x['id']} | {x['label']} | {x['loci']} |" for x in ax["modalities"]["form"]]
            L += ["", "**Historical depth** (LC-16; the fifth dimension; the author: \"situated in a 2600 year long history of mediation\"):", "", "| ID | mediation | entry loci |", "|---|---|---|"]
            L += [f"| {x['id']} | {x['label']} | {x['loci']} |" for x in ax["ranges"]["period"]]
        if la.get("evidence_under_enclosure"):
            L += ["", "**Evidence under enclosure.** " + la["evidence_under_enclosure"].split("\n", 1)[1].strip().replace("\n\n", " ")]
        JL = []
        jm = la.get("jump_measure")
        if jm:
            ill = jm["illustration"]
            JL += ["", "## The jump measure — how \"extensive\" is compared", "",
                  "The author's rule: " + " — and: ".join(f"\"{r}\"" for r in jm["rule"]), "", jm["procedure"], "",
                  f"**Illustration, not a result** (tables `jump_states`, `jumps`, `coordinates`). Seed: {ill['node']}. Selection rule: {ill['selection_rule']}.", "",
                  "| state | locus | what the state does | domain | period | epoch | mode | form | unit |", "|---|---|---|---|---|---|---|---|---|"]
            JL += [f"| {s['state']} | {s['locus']} | {s['does']} | {s['domain']} | {s['period']} | {s['epoch']} | {s['mode']} | {s['form'] or '—'} | {s['unit']} |" for s in ill["states"]]
            JL += ["", "| jump | from → to | transformation |", "|---|---|---|"]
            JL += [f"| {j['id']} | {j['from_locus']} → {j['to_locus']} | {j['transformation']} |" for j in ill["jumps"]]
            pr = ill["projections"]
            JL += ["", f"{len(ill['cells'])} evidenced cells. Projections — domains: {', '.join(pr['domain'])}; periods: {', '.join(pr['period'])}; modes: {', '.join(pr['mode'])}; forms: {', '.join(pr['form'])}; units: {', '.join(pr['unit'])}. Frontier: " + "; ".join(ill["frontier"]) + "."]
        L += ["", "**Candidates** (table `candidates`; initial objects for inspection, not a ranked list):", "",
              "| ID | candidate | role | status |", "|---|---|---|---|"]
        for c in d.get("candidates", []):
            if c["mantle"] == "the-living-academy":
                L.append(f"| {c['cand_id']} | {c['name']} | {c['role']} | {c.get('status') or ''} |")
        L += ["", "**How a comparative judgment is made or defeated.**", ""]
        L += [f"{i}. {s}" for i, s in enumerate(la["protocol"], 1)]
        L += ["", "**Not criteria:** " + " · ".join(la["non_criteria"]), "",
              "**Extent profile** — every value starts unknown and is filled from the ledger or from inspection: "
              + "; ".join(f"`{x['key']}` ({x['unit']})" for x in la["extent_profile"]) + ".", "",
              "**The ledger** (table `ledger`) — works the object names, roles coded only on reading: "
              + " · ".join(f"[#{x['deposit']}]({x['url']})" for x in d.get("ledger", []) if x["mantle"] == "the-living-academy") + ".", "",
              "**Rounds** (table `evaluations`, not averaged): "
              + "; ".join(f"`{e['eval_id']}` — {e['reader']}: {e['judgment']}" for e in ev if e["mantle"] == "the-living-academy") + ".", "",
              f"**Pair.** {la['pair']['relation']}.", "",
              "**Outward:** " + _links(1680, "06F6", [f"[machine file (JSON-LD)]({A}/files/AXN-06F6/alexanarch-entity.json)",
                                                      f"[mantle layer as data]({A}/files/AXN-06F6/mantle_layer.py)", f"[live self-description]({A}/api/entity.json)",
                                                      f"[v0.4, superseded: #1678]({A}/s/records/1678/)",
                                                      f"[the library]({A}/)", f"[registry]({A}/data/registry.json)", "[metadatapacket.dev packet page](https://www.metadatapacket.dev/packets/1678/)", "[restoredacademy.com — the pair, rendered](https://www.restoredacademy.com/readings/academy-mantles#t2)"]), ""]
        L += JL
    ap = mt.get("arch-philosopher")
    if ap:
        L += ["## The Arch-Philosopher — a transmitted mantle", "",
              f"*Mantle object: EA-MANTLE-ARCH-PHILOSOPHER-01 v0.2, [#1679]({A}/s/records/1679/) ({ap['governing_record'][0]['axn']}). Status: {ap['status']}.*", "",
              ap["summary"], "", f"**The standard.** {ap['criterion']}", "",
              f"**The turn, and its test.** {ap['turn_test_text']}", "",
              f"**Bearing and enabling.** {ap['bearing_and_enabling']}", "",
              f"**The reflexivity criterion.** {ap['reflexivity_criterion']}", "",
              "**The carriers** (table `carriers`), each with the passage at its locus:", ""]
        for c in d.get("carriers", []):
            if c["mantle"] == "arch-philosopher":
                L.append(f"- **{c['carrier']} — {c['name']}.** {c['statement']}")
        L += ["", f"**Strand A — the succession, and beyond Damascius locked.** {ap['strands']['A']}", "",
              "| link | relation | statement | grade | locus |", "|---|---|---|---|---|"]
        for x in d.get("transmission_links", []):
            if x["mantle"] == "arch-philosopher" and x["strand"] == "A":
                L.append(f"| {x['link']} | {x['relation']} | {x['statement']} | {x['grade']} | {x['locus']} |")
        L += ["", ap["strands"]["A_after_links"], "",
              f"**Strand B — the dialectic as such.** {ap['strands']['B']}", "",
              f"**Where the strands meet.** {ap['strands']['meeting']}", "",
              f"**Concurrent bearing.** {ap['strands']['concurrent_bearing']}", "",
              f"**The claim — inheritance.** {ap['claim']['inheritance']}", "",
              f"**The claim — carriage.** {ap['claim']['carriage']}", "",
              f"**No new determination.** {ap['claim']['determination']}", "",
              f"**Prior designation.** {ap['holder_or_occupancy']}", "",
              "**The ledger** (table `ledger`): "
              + " · ".join(f"[#{x['deposit']}]({x['url']})" + (" (representative site)" if x["representative_site"] else "") for x in d.get("ledger", []) if x["mantle"] == "arch-philosopher") + ".", "",
              "**Rounds** (table `evaluations`): "
              + "; ".join(f"`{e['eval_id']}` — {e['reader']}: {e['judgment']}" for e in ev if e["mantle"] == "arch-philosopher") + ".", "",
              f"**Pair.** {ap['pair']['relation']}.", "",
              "**Outward:** " + _links(1679, "06F5", [f"[Space Ark #558]({A}/s/records/558/)", f"[The Final Time #1637]({A}/s/records/1637/)",
                                                      f"[the wills and Strabo seated, #1580]({A}/s/records/1580/)", f"[Catalogues and Wills #1581]({A}/s/records/1581/)",
                                                      "[restoredacademy.com — the pair, rendered](https://www.restoredacademy.com/readings/academy-mantles)", "[metadatapacket.dev packet page](https://www.metadatapacket.dev/packets/1678/)"]), ""]
    return L


def emit():
    d = json.loads(SRC.read_text(encoding="utf-8"))
    out, counts = {}, {}
    for t in TABLES + ["required_works", "reception"]:
        rows = rows_of(d, t)
        counts[t] = len(rows)
        if rows:
            out[f"{t}.jsonl"] = jsonl(rows)
    out["README.md"] = card(d, counts)
    return out


def main():
    out = emit()
    if "--check" in sys.argv:
        bad = [n for n, s in out.items()
               if not (DIR / n).exists() or (DIR / n).read_text(encoding="utf-8") != s]
        stale = [p.name for p in DIR.glob("*.jsonl") if p.name not in out]
        if bad or stale:
            print("differs from emission:", bad, "stale:", stale); sys.exit(1)
        print("mantle-bearing: committed tables and card match the emission"); return
    for p in DIR.glob("*.jsonl"):
        if p.name not in out:
            p.unlink()
    for n, s in out.items():
        (DIR / n).write_text(s, encoding="utf-8")
    print("wrote", sorted(out))


if __name__ == "__main__":
    main()
