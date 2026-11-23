#!/usr/bin/env python3
"""mantle-bearing 1.40 (2026-11-23, the author's word of 15:32: "we need to update the holographic frames on mantle-bearing to include newer work -
its still pointing to the old, less developed phainetai moi, for example; and include evaluative functions for this is not philosophy, of ancient
philosophy, and dead letters, of classical philology journal").

1. Every framework carries `current_texts`: the current version of each seed record that has been superseded, read from the registry's
   superseded_by chain (The Tenth Muse: #1270 v1.0 -> #1785 ΦΑΙΝΕΤΑΙ ΜΟΙ v3.1; The Historical Logos: #626 v1.0 -> #1765 v2.3), and `works`, the records
   a round reads, current versions first. The seed stays the seed: it is the founding formulation, and the hologram deposits (#1756, #1757) were cut
   from it; the frame now names what a reader must read now.
2. The Tenth Muse's frame gains the state of #1785 (three readings on one scale, two lines) and the non-jealous erotic reading as the scholarship's
   strongest rival, stated from #1785 and from Dead Letters v1.1 I.4a.
3. Two frameworks enter, evaluated on their governing records (no hologram yet): This Is Not Philosophy (#1773, Ancient Philosophy and the
   philosophy field) and Dead Letters (#1783, Classical Philology), the second and third stations of the combined audit whose first is Daffodils.
4. The titles of governing and hologram records refreshed from the registry.
    python3 rebuild/mantle-bearing/v140_current_texts_two_frameworks.py"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
A = "https://www.alexanarch.org"
rec = lambda n: {"deposit": n, "axn": REG[n]["axn"], "url": f"{A}/s/records/{n}/", "title": REG[n]["title"]}


def work(n, role):
    return dict(rec(n), version=REG[n].get("version"), date=REG[n].get("date"), role=role)


def current(n):
    while REG[n].get("superseded_by_deposit_number"):
        n = REG[n]["superseded_by_deposit_number"]
    return n


d = json.loads(SRC.read_text(encoding="utf-8"))
if any(h["version"] == "1.40" for h in d["history"]): raise SystemExit("1.40 already applied")
assert d["history"][-1]["version"] == "1.39"
F = {f["framework"]: f for f in d["frameworks"]}
H = {h["hologram"]: h for h in d["holograms"]}

# 4. titles from the registry
for x in d["frameworks"] + d["holograms"]:
    for k in ("seed_record", "governing_record", "hologram_record", "specification"):
        for i, r in enumerate(x.get(k) or []):
            if r["deposit"] in REG: x[k][i] = rec(r["deposit"])

# 1. current texts of superseded seeds
for f in d["frameworks"]:
    ct = []
    for s in f["seed_record"]:
        c = current(s["deposit"])
        if c != s["deposit"]:
            ct.append(dict(work(c, f"the current version of the seed #{s['deposit']} ({REG[s['deposit']].get('version')})"), supersedes=s["deposit"]))
    if ct: f["current_texts"] = ct

WORKS = {
    "framework::socrates-as-orthonym": [(123, "the founding formulation"), (1754, "the hologram: map and kernel"), (1753, "the kernel specification"),
                                        (1773, "the case read at the gate of Ancient Philosophy (This Is Not Philosophy §0A–§0B)")],
    "framework::revelation-first": [(202, "the founding formulation"), (1755, "the hologram: map and kernel")],
    "framework::the-tenth-muse": [(1785, "ΦΑΙΝΕΤΑΙ ΜΟΙ, current version: the reading, the three readings on one scale, the comparison and the socket"),
                                  (1756, "the hologram: map and kernel (cut from the v1.0 text, #1270)"),
                                  (1645, "fragment 147 states the horizon, fragment 31 builds the seat"),
                                  (1484, "the Ω erratum: the ending as open filling"),
                                  (1752, "Invidens Sappho: how the jealousy reading and the illiterate Sappho were made"),
                                  (1748, "EA-CORPORA-36: the seated reception, translators and editors"),
                                  (1783, "Dead Letters: the case of fragment 31 at the gate of Classical Philology (I.4–I.4b)")],
    "framework::historical-logos": [(625, "the founding field statement"), (1765, "The Word That Became Text, current version"), (1757, "the hologram: map and kernel")],
    "framework::daffodils": [(1769, "the hologram and audit"), (1770, "Who Speaks for the Classics: the fuller statement of the intervention"),
                             (833, "the founding dataset of machine-mediated reception studies")],
}
for k, ws in WORKS.items():
    F[k]["works"] = [work(n, role) for n, role in ws]

# 2. The Tenth Muse at #1785
tm = F["framework::the-tenth-muse"]
tm["current_states"]["reading"] = {"date": REG[1785]["date"], "record": 1785, "axis": "reading", "state": "three_readings_one_scale",
    "note": ("the jealousy reading (the transmitted reading), the non-jealous erotic reading (the scholarship's strongest) and the future-reader reading "
             "graded on one scale; the first two fill the poem's public line, the third reads the held line and takes the public line as its first term "
             "(#1785 §§VII.1a–VII.5; Dead Letters #1783 I.4a). Not in the kernel of #1756, which predates it.")}
tm["rival"].setdefault("propositions", {})["non_jealous_erotic"] = (
    "the speaker undone by the woman herself whenever she looks (ὡς γὰρ ἔς σ᾽ ἴδω), the man a foil, no rival — the scholarship's strongest reading "
    "(Wills 1967; Lefkowitz 1973; Most; D'Angour 2013), keeping the maker and her binding; graded at every row, it motivates the collapse and leaves "
    "its form unexplained: the man's opening, the order of the catalogue, the colour, the agentless dare (#1785 §§I.1a, VII.1a–VII.1b)")
tm["rival"]["summary"] += ("; at #1785 (v3.1, 2026-11-18) the case has three readings and two lines, the non-jealous erotic reading entered as the "
                           "scholarship's strongest rival and graded on the same scale")
H["hologram::the-tenth-muse"]["current_texts"] = tm["current_texts"]
hl = F["framework::historical-logos"]; H["hologram::historical-logos"]["current_texts"] = hl["current_texts"]

# 3. two frameworks: the second and third stations of the combined audit
SPEC = [rec(1753)]
tinp = {
    "framework": "framework::this-is-not-philosophy", "name": "This Is Not Philosophy: the article economy and the shape of the field (Ancient Philosophy)",
    "class": "inspectable evaluative framework", "author": "Lee Sharks",
    "seed_record": [rec(1773)], "governing_record": [rec(1773)], "specification": SPEC,
    "positions": [
        "1. The census: twenty philosophy journals (ancient, continental, analytic) and two Persée series, each article's object and its reach coded from its abstract, every code with a machine-checked verbatim span",
        "2. The reach: in Ancient Philosophy 8 of 844 articles open the question of what the object is; three-quarters of the field's work stays inside one author (§4.7)",
        "3. The leading case and the gate: Socrates as Orthonym (#123) in three approaches to Ancient Philosophy, the condition of admission the same each time, the claim withdrawn (§§0A–0B)",
        "4. The baseline: in the Archiv für Geschichte der Philosophie of the 1890s one ancient title in five puts a work's standing in question; by the 1920s the question is gone (§4.12)",
        "5. The machine: a model asked for plausible abstracts reproduces each field's unit and writes no claim about the text in sixty ancient abstracts (§4.17)",
        "6. The article economy: disciplinarity as the stable form of what can be certified (§5)"],
    "maker_count_state": None,
    "current_states": {"reach": {"date": "2026-11-16", "record": 1773, "axis": "reach", "state": "8_of_844_open_the_object",
                                 "note": "Ancient Philosophy; 4 of 283 Plato/Aristotle abstracts across the sister journals since 2021 (§6.3)"},
                       "gate": {"date": "2026-11-16", "record": 1773, "axis": "gate", "state": "claim_withdrawn_as_condition_of_admission",
                                "note": "three approaches, three states of the evidence (§0A–§0B)"}},
    "evidence_bodies": {"A": "the census and its reach coding", "B": "the leading case and the gate", "C": "the historical baselines (Archiv, REG, CQ)",
                        "D": "the model test", "E": "the received account read from open copies"},
    "rival": {"node": "fw:division-of-labor",
              "summary": ("what a text is, who wrote it, when, whether it is one work or several, is philology's question; philosophy takes the text as given "
                          "and asks whether its arguments are sound; the division lets each discipline do its own work well, and on this reading the census "
                          "measures only that philosophers do philosophy (§0.1a, stated by the notebook in full); and the received account of the field's "
                          "decline in its seven lines (§1), each holding one link of the chain (§2.1)"),
              "contested": ("whether a field may take the identity of its object as settled where the corpus is the evidence for the doctrine (§0.1a); "
                            "the census holds articles that examine a single work's standing and none that examines the partition of the corpora among composing persons")},
    "lines_of_research": [{"id": "7.1", "question": "Do the 2000s abstracts of Phronesis show the reach plateau before 2010?"},
                          {"id": "7.2", "question": "Do the [recalled, unread] items of §1 hold when read from open copies, with loci?"},
                          {"id": "7.3", "question": "Who are the contributors of Elenchos's 13 openings, and does a second Italian venue show them?"},
                          {"id": "7.3a", "question": "What is the full-corpus proportion of questions about the text in the Archiv, located by running heads?"},
                          {"id": "7.4", "question": "What can each field of the combined audit not carry, on one instrument?"},
                          {"id": "7.5", "question": "Does the model test hold under repeated runs, a second model, a perturbation condition and a cross-family coder?"},
                          {"id": "7.6", "question": "What are the census journals' own AI rules and decline practice, with dates?"},
                          {"id": "7.7", "question": "Can the pre-flattening record be read against §§3.1 and 4.12 once seated?"}],
    "contributor": "Crimson Hexagonal Archive; Claude (Anthropic)",
    "status": f"DEPOSITED 2026-11-16 as #1772 (v1.0, the notebook at v0.21); REISSUED the same day as #1773 (v1.1, notebook v0.24). No hologram yet: a round reads the governing record.",
    "works": [work(1773, "the governing record: census, case and argument"), work(123, "the leading case: Socrates as Orthonym"),
              work(1754, "the case's framework hologram"), work(1771, "EA-CORPORA-39: the field before the flattening, seated"),
              work(1766, "Critique of Pure Inference, by which the case and the gate are read"),
              work(1770, "the first station: Who Speaks for the Classics"), work(1783, "the third station: Dead Letters")],
}
dl = {
    "framework": "framework::dead-letters", "name": "Dead Letters: who decides what the object is (Classical Philology)",
    "class": "inspectable evaluative framework", "author": "Lee Sharks",
    "seed_record": [rec(1783)], "governing_record": [rec(1783)], "specification": SPEC,
    "positions": [
        "1. The gradient: the question of what the text is opened at the locus, confirming at the work, closed at the corpus, in CP 1906–30 and in GRBS 1958–2026 (§10.1)",
        "2. A division of labour: relations admitted to confirm the received whole, atoms to open it (55 to 32; 68 to 50) (§10.2)",
        "3. The grounds of the verdict: of 69 judgments of a whole in CP's reviews of 1906–22, 6 rest on an atom, 23 on an argument, 40 on no stated ground (§8.3)",
        "4. The closed record: 97% closed as OpenAlex classes it; no abstract in 11,206 Crossref records; decisions about texts cited at 2.3 an item against 5.3 (§§8, 8.6.2)",
        "5. The one exception: M. L. West, editor of the Teubner Iliad, in CQ 1999 — the corpus question admitted at the canonical unit once, from the unit's editor (§10)",
        "6. The case: Sappho 31 — three readings and two lines, declined at the gate on a verdict stated as conviction (I.4–I.4b)"],
    "maker_count_state": None,
    "current_states": {"gradient": {"date": "2026-11-17", "record": 1783, "axis": "gradient", "state": "open_at_locus_closed_at_corpus"},
                       "case": {"date": "2026-11-18", "record": 1783, "axis": "case", "state": "public_line_kept_account_of_form_declined",
                                "note": "v1.1 in place: the case brought to ΦΑΙΝΕΤΑΙ ΜΟΙ v3.0–v3.1 (#1785)"}},
    "evidence_bodies": {"A": "the census of 4,252 titles, coded and audited blind", "B": "the page, 1906–1930", "C": "the contemporary journal, 2020–26",
                        "D": "the comparators (GRBS, BMCR, Classical Quarterly)", "E": "the closed record (metadata, citations, bylines)", "F": "the case of fragment 31"},
    "rival": {"node": "fw:corrigible-philology",
              "summary": ("philology is the discipline that tests the text against its witnesses; its unit is the passage, its findings answer to evidence, a "
                          "papyrus turns up and the reading changes; that corrigibility is its claim to authority, and a real one, and other fields take the "
                          "object from it (I.1, stated in full); on the case, the scholarship has drifted from the jealousy reading toward the non-jealous erotic "
                          "reading, so the jealousy reading is a popular survival and the gate cannot be charged with it (I.4a)"),
              "contested": ("whether the atom rule, under which coherence may not weigh on the adjudication of atoms, leaves the judgment of the whole to "
                            "conviction, stated without grounds, and whether the received reading is held to the rule it applies (§0.1; #1766 §5.2.3)")},
    "lines_of_research": [{"id": "9.3", "question": "Does a blind audit sample hold the 1923–30 codes?"},
                          {"id": "9.4", "question": "Do Mnemosyne, Hermes, Philologus and Glotta show the gradient?"},
                          {"id": "9.6", "question": "Read by grain, how wide is the gradient against the disagreements of the blind audit?"},
                          {"id": "9.7", "question": "Do the three journals stand on one inspectability measure read the same day?"},
                          {"id": "9.9", "question": "The canon test: do the TLG Canon, the OCD or the standard edition carry CP's decisions, and cite CP?"},
                          {"id": "9.10", "question": "Does a chain of gatekeepers run through the masthead and editing department, 1906–2026?"},
                          {"id": "9.11", "question": "Does the canonical/minor line, fixed in advance against an outside list, hold the corpus-grain cases?"},
                          {"id": "9.12", "question": "Does each bare verdict of 1906–22 summarize an argument made elsewhere in its review, or stand in for one?"}],
    "contributor": "Crimson Hexagonal Archive; Claude (Anthropic)",
    "status": "DEPOSITED 2026-11-17 as #1783 (v1.0); v1.1 in place 2026-11-18 (the case brought to ΦΑΙΝΕΤΑΙ ΜΟΙ v3.0). No hologram yet: a round reads the governing record.",
    "works": [work(1783, "the governing record: census, audit and case"), work(1785, "ΦΑΙΝΕΤΑΙ ΜΟΙ, current version: the declined article, its comparison and socket"),
              work(1774, "ΦΑΙΝΕΤΑΙ ΜΟΙ v2.3, which carries the Classical Philology reader's report"), work(1752, "Invidens Sappho"),
              work(1766, "Critique of Pure Inference: asymmetric immunity (§5.2.3)"),
              work(1770, "the first station: Who Speaks for the Classics"), work(1773, "the second station: This Is Not Philosophy")],
}
for f in (tinp, dl):
    d["frameworks"].append(f)
    d["holograms"].append({"hologram": f["framework"].replace("framework::", "hologram::"), "item": f["framework"], "item_kind": "framework",
                           "governing_record": f["governing_record"], "specification": SPEC,
                           "status": "NOT YET HELD AS A HOLOGRAM: evaluated on its governing record, at the author's word of 2026-11-23 15:32"})
d["history"].append({"version": "1.40", "date": "2026-11-23", "note": (
    "Frames brought to current work, at the author's word of 15:32: current_texts for superseded seeds (The Tenth Muse #1270 -> #1785 ΦΑΙΝΕΤΑΙ ΜΟΙ v3.1; "
    "The Historical Logos #626 -> #1765 v2.3) and a works list per framework; the Tenth Muse's state at #1785 and the non-jealous erotic reading as "
    "its strongest rival; This Is Not Philosophy (#1773) and Dead Letters (#1783) entered as frameworks evaluated on their governing records; a round "
    "of a framework given its own steps. rebuild/mantle-bearing/v140_current_texts_two_frameworks.py.")})
d["packet_version"] = d.get("packet_version")
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("1.40 applied")
