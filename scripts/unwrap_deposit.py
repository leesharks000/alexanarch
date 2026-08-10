#!/usr/bin/env python3
"""unwrap_deposit.py — remove wrap artifacts, keep every encoded break.

MANUS, 2026-08-09: "an artificially rendered linebreak due to container width is
*not* a linebreak — a deliberately encoded linebreak or tab, is."

That distinction is the whole tool. A canonical body flows; wrapping is display's
job and cannot be undone once bytes are sealed. But a poem's lineation, a list's
items, a table's rows and an indented block's shape are the work, and a tool that
flattens them to fix wrapping has destroyed more than it repaired.

HOW A WRAP ARTIFACT IS RECOGNISED

Not by line length alone, and not by whether a line ends mid-sentence — enjambment
does that on purpose. The signal is MECHANICAL REGULARITY. A tool wrapping at a
column produces a block whose every line but the last crowds the same maximum:
lines of 91, 94, 88, 93, 47. Verse does not do that. Its lines vary because they
are chosen.

So a block is joined only when ALL of these hold:

  · every line but the last falls within 18 characters of the block's longest
  · the longest line sits between 60 and 110 characters — a plausible wrap column
  · the block has three or more lines, so two-line blocks are never guessed at
  · no line begins with whitespace (indentation is deliberate shape)
  · no line carries a markdown marker: heading, list, quote, table, rule
  · the block is not inside a fenced code block
  · no line ends with two spaces, which is markdown's own encoded hard break

Anything failing any test is left exactly as written. The tool is built to refuse.

    python3 scripts/unwrap_deposit.py --check
    python3 scripts/unwrap_deposit.py --deposit 1438 --apply
    python3 scripts/unwrap_deposit.py --all --apply
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

MARKER = re.compile(r"^\s*(#{1,6}\s|[-*+]\s|\d+[.)]\s|>|\||```|~~~|---\s*$|===)")
_re_align = re.compile(r"\S {2,}\S")
_re_label = re.compile(r"^[A-Z][A-Za-z0-9 ()§.\u2013-]{1,34}:\s")
BAND = 18          # how close to the longest a line must sit to look mechanical
MIN_COL, MAX_COL = 60, 110
MIN_LINES = 3


def blocks(text):
    """Split into (kind, lines) runs: 'fence' passes through untouched."""
    out, cur, fenced = [], [], False
    for line in text.split("\n"):
        if line.lstrip().startswith(("```", "~~~")):
            if cur:
                out.append(("body", cur))
                cur = []
            fenced = not fenced
            out.append(("fence", [line]))
            continue
        if fenced:
            out.append(("fence", [line]))
            continue
        if not line.strip():
            if cur:
                out.append(("body", cur))
                cur = []
            out.append(("blank", [line]))
        else:
            cur.append(line)
    if cur:
        out.append(("body", cur))
    return out


def is_wrapped(lines):
    """True only when the block shows mechanical regularity and nothing deliberate."""
    if len(lines) < MIN_LINES:
        return False
    if any(l[:1] in " \t" for l in lines):
        return False                      # indentation is shape
    if any(MARKER.match(l) for l in lines):
        return False                      # heading, list, quote, table, rule
    if any(l.endswith("  ") for l in lines[:-1]):
        return False                      # markdown hard break, encoded on purpose

    # FOUND BY READING, 2026-08-09. Two kinds of table survive every test above
    # because neither announces itself at the start of a line.
    #
    # #31, the DOI registry, holds rows like
    #   **18166347** | 10.5281/zenodo.18166347 | T4 | theoretical_fra | E:0
    # — pipe-delimited, but beginning with a bolded field rather than a pipe, so the
    # marker test never sees it.
    #
    # #557 holds a state-transition table aligned with runs of spaces:
    #   RATIFIED  → DEPOSITED    (DOI retracted; re-audit required)
    #   DEPOSITED → PROVISIONAL  (DOI invalid or points to wrong content)
    # — no markers at all, lengths mechanically regular, and joining it would
    # collapse a table into a sentence.
    #
    # Alignment is encoded structure exactly as indentation is. Both refuse.
    # ANY, NOT A MAJORITY. A first version required half the block's lines to look
    # structured, and #557 slipped through on a three-line run where only one line
    # carried alignment — an operator definition beside a bracketed note. Joining a
    # block destroys every structured line in it, so one is enough to refuse. Prose
    # paragraphs do not contain pipes or internal column runs; anything that does is
    # not a prose paragraph.
    if any(" | " in l for l in lines):
        return False                      # pipe-delimited rows, however they begin
    if any(_re_align.search(l) for l in lines):
        return False                      # columns aligned with runs of spaces

    # PARALLEL LABEL LISTS, found by reading #557. Three lines reading
    #   Strong Form: Full recovery from any RATIFIED component.
    #   Working Form: Partial recovery; degrades gracefully with status.
    #   Extended Form: With Pi enabled, any PAREIDOLIA reading + K -> partial H.
    # are three definitions, not one wrapped paragraph, and they carry no marker,
    # no pipe and no alignment. Two or more lines opening with a short capitalised
    # label and a colon is a list whatever its punctuation says.
    if sum(1 for l in lines if _re_label.match(l)) >= 2:
        return False
    body = [len(l.rstrip()) for l in lines[:-1]]
    longest = max(body)
    if not (MIN_COL <= longest <= MAX_COL):
        return False
    if min(body) < longest - BAND:
        return False                      # varied lengths: chosen, not wrapped
    return True


# POETRY IS NEVER TOUCHED (2026-08-09).
#
# The first deposit read under this tool was #331, "Antioch: A Volume of Poems",
# 894 candidate joins. Its lines are mechanically regular — 66, 71, 70, 4 — which
# is exactly what wrapped prose looks like and exactly what metrical verse looks
# like. THE TEST CANNOT TELL THEM APART, and in a volume of poems the cost of being
# wrong is the work itself.
#
# 14 of the 205 affected deposits are poetry or creative work and carry 1,422 of
# the breaks. The tool refuses them by content_type and by title, and refuses
# anything it cannot classify, because the failure is asymmetric: an unjoined
# paragraph is untidy, a joined poem is destroyed.
POETIC = _re_poetic = __import__("re").compile(
    r"poe|verse|creative|literary|fiction|lyric|stanza|song|hymn|psalm", __import__("re").I)


def is_poetry(entry):
    """Refuse on any signal. Absence of a content_type is itself a refusal."""
    ct = str(entry.get("content_type") or "")
    ti = str(entry.get("title") or "")
    kw = " ".join(entry.get("keywords") or [])
    if not ct:
        return True
    return bool(POETIC.search(ct) or POETIC.search(ti) or POETIC.search(kw))


def unwrap(text):
    out, joined = [], 0
    for kind, lines in blocks(text):
        if kind != "body" or not is_wrapped(lines):
            out.extend(lines)
            continue
        out.append(" ".join(l.strip() for l in lines))
        joined += len(lines) - 1
    return "\n".join(out), joined


def words(t):
    return re.findall(r"[0-9A-Za-z\u00c0-\u024f']+", t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deposit", type=int)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    reg_p = ROOT / "data/registry.json"
    reg = json.loads(reg_p.read_text())
    D = {d["deposit_number"]: d for d in reg["deposits"]}
    targets = ([D[a.deposit]] if a.deposit else
               reg["deposits"] if a.all else reg["deposits"][-45:])

    touched, refused, skipped_poetry = [], 0, 0
    for d in targets:
        fp = d.get("full_text_path")
        if not fp:
            continue
        p = ROOT / fp.lstrip("/")
        if not p.exists():
            continue
        if is_poetry(d):
            skipped_poetry += 1
            continue
        old = p.read_text(errors="replace")
        new, joined = unwrap(old)
        if not joined:
            continue
        if words(old) != words(new):
            refused += 1
            print(f"  REFUSED #{d['deposit_number']}: word content would change")
            continue
        touched.append((d["deposit_number"], joined, len(old), len(new)))
        if a.apply:
            p.write_text(new)
            import hashlib
            h = hashlib.sha256(new.encode()).hexdigest()
            d["hash"] = h
            d.setdefault("body_status", {})["work_sha256"] = h
            d.setdefault("record_modifications", []).append({
                "date": "2026-08-09", "field": "canonical_text",
                "note": (f"WRAP ARTIFACTS REMOVED — {joined} line break(s) that existed only "
                         "because prose had been hard-wrapped at a column. Canonical bodies "
                         "flow; wrapping is display's job and cannot be undone once bytes are "
                         "sealed. Deliberate structure was left untouched: verse lineation, "
                         "indentation, list items, table rows, fenced code, headings, and "
                         "markdown hard breaks are all excluded by the tool, and word content "
                         "was verified identical before writing.")})

    if a.apply and touched:
        reg_p.write_text(json.dumps(reg, ensure_ascii=False, indent=2))

    print(f"\n  {len(touched)} deposit(s) with wrap artifacts, {refused} refused, "
          f"{skipped_poetry} skipped as poetry or unclassified")
    for n, j, o, w in touched[:20]:
        print(f"    #{n:<6} {j:>4} breaks joined · {o:>7,}c → {w:,}c")
    print(f"\n{'APPLIED' if a.apply else 'CHECK ONLY'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
