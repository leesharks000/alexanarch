#!/usr/bin/env python3
"""build_rhizome_card.py — the dataset card, emitted from the grammar.

WHY GENERATED AND NOT WRITTEN. The card declares the HF configs, and the Hugging Face
viewer shows nothing without them. Hand-writing one per body means a fourth body ships
with no card, or with a card that describes the third. The grammar already holds what a
card needs — what the body is, where it germinated, its roles, its cautions, its measured
disagreements — so the card is a rendering of the grammar and drifts only when it does.

The first body's card is NOT regenerated: it was hand-authored over several passes, carries
the poetics table and the laws, and is longer and better than anything this produces. It is
left alone and this script skips it.

Usage: python3 scripts/build_rhizome_card.py <grammar.json>
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def counts_line(body_dir):
    """The hand-authored card is not regenerated, so its counts go stale silently. The
    skip message now prints what the spore says, so a build makes the drift visible."""
    import json as _j
    c = _j.loads((body_dir / "spore.json").read_text(encoding="utf-8")).get("counts", {})
    return f"{c.get('nodes')} nodes / {c.get('edges')} edges / {c.get('stolons')} stolons"


def card(g, body_dir):
    b = g["body"]
    files = {f.stem: f for f in body_dir.glob("*.jsonl")}
    configs = "\n".join(
        f'  - config_name: {n}\n    data_files: {n}.jsonl' for n in sorted(files))
    counts = json.loads((body_dir / "spore.json").read_text(encoding="utf-8")).get("counts", {})

    germ = g.get("germinated_from") or {}
    parents = germ.get("spores") or ([germ.get("spore")] if germ.get("spore") else [])
    stol = germ.get("stolons") or ([germ["stolon"]] if germ.get("stolon") else [])

    L = []
    L.append("---")
    L.append("license: cc-by-4.0")
    L.append("configs:")
    L.append(configs)
    L.append("---")
    L.append("")
    L.append(f"*{g['maxim']}*")
    L.append("")
    L.append(f"# {b['rhizome_id']} — {b['slug'].replace('-', ' ')}")
    L.append("")
    L.append(g.get("what", ""))
    L.append("")
    # THE BODIES ARE SYMBOLA AND THE CARD MUST SAY SO (2026-09-16). An unprimed traversal
    # read the card, the field names and the landing page, said competent things about the
    # vocabulary, and resolved no referent at all -- then proposed to read one capture's
    # metadata "as prose" with that capture's own machine text one link away. Nothing in any
    # card said that a row is half a token and the referent is the other half. The cards
    # explained how rows GOT IN and never how to get OUT, so a reader inferring from the card
    # read the card. This section is emitted SECOND, before the counts, because a reader who
    # stops early should have stopped after being told what they are holding.
    htr = g.get("how_to_read")
    if htr:
        L.append("## These are symbola. They are for traversal.")
        L.append("")
        L.append(f"> {htr['definition']}")
        L.append("")
        L.append(f"*{htr['source']}*")
        L.append("")
        L.append(f"**A row is an index, not a text.** {htr['what_a_row_is']}")
        L.append("")
        L.append(f"**The other half is `source_uri`.** {htr['the_other_half']}")
        L.append("")
        L.append("**The traversal:**")
        L.append("")
        for i, step in enumerate(htr["the_traversal"], 1):
            L.append(f"{i}. {step}")
        L.append("")
        L.append(f"**Atomized for reassembly.** {htr['atomization_is_for_reassembly']}")
        L.append("")
        L.append(f"**A failure mode, recorded.** {htr['the_failure_mode_named']}")
        L.append("")
        L.append(f"**Check.** {htr['how_to_verify_you_have_read_it']}")
        L.append("")
        L.append(f"**What the rows will not give you.** {htr['what_the_rows_will_not_give_you']}")
        L.append("")

        # THE FIGURE IS FRACTAL AND THE CARD SHOULD SHOW IT (2026-09-16). Naming the row/referent
        # fracture alone understated the architecture: the same relation holds at five scales, and
        # the archive was already machine-checking one of them in CI without calling it a symbolon.
        # The verification column is the point -- it weakens outward until the last fit can only be
        # closed by a reader, which is where the reader finds themselves on the ladder.
        lad = htr.get("the_ladder")
        if lad:
            L.append("### The figure is fractal")
            L.append("")
            L.append("| scale | one half | the other half | the fit is checked by | who can check it |")
            L.append("|---|---|---|---|---|")
            for r in lad:
                L.append(f"| **{r['scale']}** | {r['half_a']} | {r['half_b']} | {r['fit_is_checked_by']} | {r['who_can_check']} |")
            L.append("")
            if htr.get("ladder_note"):
                L.append(htr["ladder_note"])
                L.append("")
            for r in lad:
                L.append(f"- **{r['scale']}** — {r['note']}")
            L.append("")
            if htr.get("your_scale"):
                L.append(f"**{htr['your_scale']}**")
                L.append("")

    L.append("## Counts")
    L.append("")
    L.append(" · ".join(f"**{v}** {k}" for k, v in counts.items()))
    L.append("")

    if stol:
        L.append("## It was advertised before it existed")
        L.append("")
        L.append("**A spore is not a template that gets copied. It germinates, and the site is "
                 "written down in advance.**")
        L.append("")
        for s in stol:
            par = s.get("parent") or (parents[0] if parents else "?")
            L.append(f"- `{s['from']}` --**{s['predicate']}**--> `{s.get('to_rhizome', b['slug'])}`  "
                     f"·  declared by **{par}**")
        L.append("")
        if germ.get("unresolved_relation"):
            L.append(f"**The question the parent could not finish:** {germ['unresolved_relation']}")
            L.append("")

    if g.get("vocabulary_source"):
        L.append("## The vocabulary is the archive's, not the emitter's")
        L.append("")
        L.append(g["vocabulary_source"])
        L.append("")

    if g.get("why_three_principles"):
        L.append("## Why more than one selection principle")
        L.append("")
        L.append(g["why_three_principles"])
        L.append("")

    cp = g.get("core_principles") or {}
    if cp:
        L.append("| principle | basis | caution |")
        L.append("| --- | --- | --- |")
        for k, v in cp.items():
            L.append(f"| **{k}** | `{v.get('basis','')}` | {v.get('caution','')} |")
        L.append("")

    md = g.get("measured_disagreement")
    if md:
        L.append("## The disagreement is the primary datum")
        L.append("")
        L.append("```")
        for k, v in md.items():
            if isinstance(v, int):
                L.append(f"{k:34} {v}")
        L.append("```")
        L.append("")
        L.append(md.get("reading", ""))
        L.append("")
        if md.get("caution"):
            L.append(f"**Caution.** {md['caution']}")
            L.append("")

    L.append("## Roles")
    L.append("")
    L.append("**Order is the classifier** — `role_for` returns on first match, so a broad pattern "
             "above a narrow one swallows it.")
    L.append("")
    L.append("| role | what it names |")
    L.append("| --- | --- |")
    for r in g["roles"]:
        L.append(f"| `{r['role']}` | {r.get('note','')} |")
    L.append("")
    if g.get("roles_note"):
        L.append(g["roles_note"])
        L.append("")
    L.append(f"A node matching nothing falls to `{g.get('default_role','observation')}`, "
             "whose count is this grammar's own error bar.")
    L.append("")

    _sibs = sorted({d.name for d in (ROOT / "rhizomes").iterdir()
                    if d.is_dir() and d.name != "_grammars"} - {g["body"]["slug"]})
    if _sibs:
        L.append("## The other bodies")
        L.append("")
        L.append("**Each is emitted by one generator from a grammar file, and each declares stolons naming "
                 "the siblings it advertises and does not contain.**")
        L.append("")
        for _s in _sibs:
            L.append(f"- [`leesharks/{_s}`](https://huggingface.co/datasets/leesharks/{_s})")
        L.append("")

    L.append("## Where it points and does not go")
    L.append("")
    L.append("**Advertised, not included.** The outside stays outside and stays reachable.")
    L.append("")
    # A STOLON NAMES A SIBLING DATASET AND THE CARD RENDERED IT AS PLAIN TEXT (2026-09-14).
    # Each satellite card linked only to the parent, so a reader landing on one body could
    # reach the parent and nothing else — and where a search index served a stale parent
    # card naming one satellite, the reachable set was two datasets out of nine.
    # The stolons already declare the siblings. They are now links.
    _BODIES = {d.name for d in (ROOT / "rhizomes").iterdir()
               if d.is_dir() and d.name != "_grammars"}
    for s in (g.get("stolons") or []):
        frm, pred, to, note = (s + [None] * 4)[:4]
        _t = (f"[`{to}`](https://huggingface.co/datasets/leesharks/{to})"
              if to in _BODIES else f"`{to}`")
        L.append(f"- **{_t}** — `{pred}` from `{frm}`")
        if note:
            L.append(f"  {note}")
    L.append("")

    L.append("## Reproducing it")
    L.append("")
    L.append("```")
    L.append(f"RHIZOME_GRAMMAR=rhizomes/_grammars/{pathlib.Path(sys.argv[1]).name} \\")
    L.append("  python3 scripts/build_rhizome_mc.py")
    L.append("```")
    L.append("")
    L.append(f"`spore.json` carries the recipe and the commit of the ledger it came from. The "
             f"grammar is read, not carried: every determining rule above lives in "
             f"`rhizomes/_grammars/`, and a different body means a different grammar file, not a "
             f"fork of the generator.")
    L.append("")
    L.append(f"Emitted from the [Crimson Hexagonal Archive]"
             f"(https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive) · "
             f"[alexanarch.org](https://www.alexanarch.org/)")
    return "\n".join(L) + "\n"


def main():
    gp = pathlib.Path(sys.argv[1])
    g = json.loads(gp.read_text(encoding="utf-8"))
    body = ROOT / "rhizomes" / g["body"]["slug"]
    out = body / "README.md"
    if out.exists() and g["body"]["slug"] == "model-collapse-anti-collapse":
        print(f"  {g['body']['slug']}: card is hand-authored, left alone — "
              f"spore says {counts_line(body)}; VERIFY THE CARD STATES THIS")
        return
    out.write_text(card(g, body), encoding="utf-8")
    print(f"  {g['body']['slug']}: card written, {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
