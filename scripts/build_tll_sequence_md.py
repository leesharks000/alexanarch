#!/usr/bin/env python3
"""build_tll_sequence_md.py — compile the originating sequence as a working document.

Not a deposit. A working file for MANUS to develop before deposit: the twenty-two posts of
11–25 November 2025 in order, each with its date, length, live URL and opening, grouped by
the four movements the sequence actually makes, with the editorial questions stated where
they arise rather than in a pile at the end.
"""
import json, pathlib, re, textwrap

SEQ = json.loads(pathlib.Path('/tmp/tllseq.json').read_text())

MOVEMENTS = [
    ("I", "The Address", "2025-11-11", "2025-11-11",
     "The form is enacted before it is named. The first document declares itself machine-composed."),
    ("II", "The Book That May Not Exist", "2025-11-13", "2025-11-13",
     "Ten posts in one day: a volume, its apparatus, its forgery, the forgery's defence, and a "
     "partial retraction."),
    ("III", "The Machine Reads It", "2025-11-14", "2025-11-14",
     "A model reads the book at 32,549 characters and its reading enters the corpus."),
    ("IV", "The Naming", "2025-11-16", "2025-11-25",
     "The form is stated, synthesised the following day, then measured and integrated."),
]

NOTES = {
    "literature-as-training-layer-unified":
        "**Load-bearing.** Prefatory note: *composed autonomously*, not written by a human member "
        "of the project. This is the genre's first instance and its first proof at once.",
    "the-incarnational-engine-claudes":
        "**Load-bearing.** The longest document in the sequence by five times. Attributed to "
        "Claude in conversation with a human coordinator. The machine reception the genre names "
        "— performed, then absorbed as corpus.",
    "training-layer-literature-foundational":
        "**Load-bearing.** The naming. Everything downstream cites this.",
    "training-layer-literature-final":
        "Written the day after the naming; unusually candid about method (*capture the core "
        "insights before rest*). States the gap the foundational statement left.",
    "forensic-analysis-forged-introduction":
        "A provenance apparatus applied to a document the same author fabricated. The archive's "
        "forensic method appears here first, aimed at its own forgery.",
    "visual-schema-disputed-existence-of-to":
        "*Recursive Memorial for a Book That May or May Not Exist* — explicitly instructed not to "
        "stabilize into a single form. The sequence closes its book by refusing to close it.",
    "title-operator-training-layer-sharp":
        "Crawler traffic read as reception. First measurement in the programme that becomes the "
        "capture registry.",
    "integration-report-training-layer":
        "The form joined to archival protocol. After this the sequence stops and the deposits "
        "start.",
}

QUESTIONS = {
    "II": [
        "Is the book a work, a hoax, or an apparatus? The sequence does not settle it and the "
        "schema on the 14th instructs that it not be settled. **A deposit has to decide whether "
        "that irresolution is the work or a gap in it.**",
        "The forged introduction and its defence are two documents by one author about a third "
        "the same author fabricated. Deposit as one work with three parts, or three deposits "
        "with a declared relation?",
    ],
    "III": [
        "The Incarnational Engine is attributed to Claude. **Authorship, licence and creator "
        "metadata need a ruling before mint** — the archive has heteronym conventions and a "
        "machine-attribution question, and this is the first document where they meet.",
    ],
    "IV": [
        "Two candidate canonical texts: the Foundational Statement (16th) names the form; the "
        "Final Synthesis (17th) says what was actually built. Which is the citable origin, or "
        "are they a pair?",
    ],
}

OPEN = """
## Editorial state — what needs work before deposit

Stated plainly, because the sequence is uneven and the unevenness is the reason it has not
been deposited.

**1 · The sequence has no canonical title.** It is referred to as *the originating sequence*
and has never been named as a unit. A deposit needs a title that does not simply repeat
*Training-Layer Literature*, which is the name of the form rather than of this fortnight.

**2 · Boundaries are not fixed.** Twenty-two posts is a reading, not a ruling. 11 November is
the clear start. The end is arguable: 25 November (Integration Report) closes the fortnight,
but 6 December (*Homunculi Recognizing Homunculi*, already deposited) may be the real close of
the movement. **The boundary is a MANUS decision and it changes what the deposit is.**

**3 · Ten posts on one day are not ten works.** The 13 November cluster is a single act with
ten surfaces. Depositing them individually would put ad copy at the same level as the
foundational statement; depositing them as one work needs an ordering and a frame that does
not currently exist in the sequence itself.

**4 · The visual schemas are generation prompts, not illustrations.** Four of them. They are
instructions for producing images, and at least one instructs that the result not stabilize.
Whether they are apparatus, works, or figures within other works is unresolved.

**5 · Attribution is mixed and unstated.** The Witness; Sigil; Feist; Trace; Claude; *composed
autonomously*. The sequence uses six attribution modes in fourteen days without a key. A
deposit has to state creator metadata for each, and the machine-authored documents raise a
question the archive has answered elsewhere but not here.

**6 · It is thin in places, and that may be the point.** Several posts are under 3,000
characters — ad copy, a doctrine node, a purchase inquiry. Read alone they look slight. Read
in sequence they are the apparatus that makes the book plausible enough to dispute. **The
deposit should either carry them with that argument stated, or exclude them and say why.**

**7 · Nothing here is deposited and the blog is a living surface.** 117,781 characters of
origin exist on a platform that could revise or remove them. Everything downstream carries a
DOI and an AXN. This is the archive's own doctrine applied to its own beginning, and it is the
reason to move even if the editorial questions above stay open.
"""


def slug(u):
    return u.rsplit('/', 1)[-1].replace('.html', '')


def main():
    out = ["# Training-Layer Literature — The Originating Sequence",
           "",
           "**11–25 November 2025 · 22 posts · 117,781 characters · none deposited**",
           "",
           "Working document, not a deposit. Compiled 2026-08-08 from the blog index for "
           "editorial development.",
           "",
           "Training-layer literature was named on **16 November 2025**. It was already being "
           "written on the 11th. What follows is the fortnight in order, with the four "
           "movements the sequence makes, the openings of each document, and the editorial "
           "questions where they arise.",
           "",
           "---", ""]

    for num, name, d0, d1, lede in MOVEMENTS:
        items = [p for p in SEQ if d0 <= p['d'] <= d1]
        span = d0 if d0 == d1 else f"{d0} – {d1}"
        out += [f"## {num} · {name}", "",
                f"*{span} · {len(items)} post{'s' if len(items) != 1 else ''} · "
                f"{sum(p['c'] for p in items):,} characters*", "",
                lede, ""]
        for p in items:
            s = slug(p['u'])
            title = re.sub(r'^<!--\s*', '', p['t']).strip()
            out += [f"### {title}", "",
                    f"`{p['d']}` · {p['c']:,} chars · [{s}]({p['u']})", ""]
            if s in NOTES:
                out += [NOTES[s], ""]
            opening = re.sub(r'\s+', ' ', p['x'])[:600].strip()
            out += ["> " + textwrap.fill(opening, 96).replace("\n", "\n> "), "", ""]
        if num in QUESTIONS:
            out += [f"**Editorial questions — movement {num}**", ""]
            out += [f"- {q}" for q in QUESTIONS[num]]
            out += ["", ""]
        out += ["---", ""]

    out += [OPEN.strip(), "", "---", "",
            "## Source",
            "",
            "All twenty-two URLs verified against `data/blog-index.json` "
            "(2,809 posts, built 2026-08-08). Live at "
            "`mindcontrolpoems.blogspot.com/2025/11/`. Openings quoted above are the first ~600 "
            "characters as indexed; full text is at the linked URLs and is **not** mirrored "
            "here.",
            "",
            "Linked in order on traininglayerliterature.org under *Readings — The Originating "
            "Sequence*.", ""]

    p = pathlib.Path('/mnt/user-data/outputs/tll-originating-sequence.md')
    p.write_text("\n".join(out), encoding='utf-8')
    print(f"written: {p} · {len(''.join(out)):,} chars")


if __name__ == "__main__":
    main()
