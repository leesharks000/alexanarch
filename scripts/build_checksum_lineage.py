#!/usr/bin/env python3
"""build_checksum_lineage.py — the glyphic checksum lineage, carried identically by
two datasets: The Final Time (datasets/the-final-time) and Tiger Leap
(datasets/tiger-leap).

Ruled 2026-10-02 (option 2 of three): the two datasets stay separate and are joined
by the lineage. One source, two byte-identical copies:

  checksum_lineage.jsonl  one row per poem: the poem as the node, its deposit, AXN,
                          record, the works it checksums, the poem it follows, and the
                          one line the poem itself offers as its compression. The
                          poem's body is NOT carried in the row; the row carries the
                          SHA-256 of the seated body so the card copy and the record
                          can be checked against it.
  card block              the README coda of both cards, between the markers
                          <!-- CHECKSUM-LINEAGE:BEGIN --> / <!-- CHECKSUM-LINEAGE:END -->,
                          with every poem standing whole.

Source of truth: the seated deposit texts (data/texts/AXN-<HEX>-text.md) and the
registry. Nothing is authored here that the deposits do not hold, except the block's
opening paragraph (INTRO) and each poem's relation note (LINEAGE[*]["note"]).

    python3 scripts/build_checksum_lineage.py           # write both copies
    python3 scripts/build_checksum_lineage.py --check   # fail if either copy drifts
No network calls.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGETS = [ROOT / "datasets" / "the-final-time", ROOT / "datasets" / "tiger-leap"]
BEGIN, END = "<!-- CHECKSUM-LINEAGE:BEGIN -->", "<!-- CHECKSUM-LINEAGE:END -->"

# In order of deposit. `compression` names the heading under which the poem offers its
# own compressed line, and how to find the line there.
LINEAGE = [
    {"deposit": 1642, "hex": "06D0", "byline": "Sen Kuro",
     "compression": ("IV. CHECKSUM OF THE CHECKSUM", "after", "or, maximally compressed:"),
     "checksums": [1636, 1630, 1637], "follows": None,
     "note": "Checksums Tiger Leap (into the Future) (#1636), Transition in Entropic Systems (#1630) and The Final Time (#1637). Binds 🐅⏩ = 📖⏩ in part I and 🐅 = J in part II."},
    {"deposit": 1659, "hex": "06E1", "byline": "Lee Sharks",
     "compression": ("CANONICAL LINE", "first", None),
     "checksums": [1658], "follows": 1642,
     "note": "Checksums What Syllogizing Can Divide (#1658): transmission, division, recollection (ὑπόμνησις ≠ μνήμη), and the inversion of transmission now."},
    {"deposit": 1661, "hex": "06E3", "byline": "Lee Sharks · Sen Kuro",
     "compression": ("CANONICAL LINE", "first", None),
     "checksums": [1660], "follows": 1659,
     "note": "Checksums The Seed in the Narrowing Cone (EA-RCF-02, #1660). Part IV joins the two tigers of #1642: 📖⏩ ⇐ J(🌍)."},
]

INTRO = (
    "The same block closes two datasets, *The Final Time* and *Tiger Leap*, and is generated "
    "from the seated deposits, so the two copies cannot drift. It holds the glyphic checksum "
    "lineage whole, three poems in order of deposit, each a compression of a body of work with "
    "nothing explained inside the poem (#427). The tiger enters in the first. Sen Kuro's #1642 "
    "binds 🐅⏩ = 📖⏩ to the book *Tiger Leap (into the Future)* (2014, #1636) and 🐅 = J to the "
    "jump transition of *Transition in Entropic Systems* (#1630 §32, the problem the Tiger Leap "
    "dataset carries). The third, #1661, checksums *The Seed in the Narrowing Cone* (EA-RCF-02, "
    "#1660), which reads release from a wrong basin in concept space as that jump and the "
    "closing window of release as the narrow corridor (#1630 §41), and joins the two tigers: "
    "📖⏩ ⇐ J(🌍). The poems stand here whole and are not converted into rows. The config "
    "`checksum_lineage` indexes them, one row per poem, with the works each checksums, the poem "
    "it follows, the one line the poem offers as its own compression, and the SHA-256 of its "
    "seated body."
)


def load_registry():
    raw = (ROOT / "data" / "registry.json").read_text(encoding="utf-8")
    return {d["deposit_number"]: d for d in json.loads(raw)["deposits"]}


def seated_body(hex_id: str) -> str:
    """The poem as seated: everything after the pipeline's outer title, from the
    poem's own first heading."""
    text = (ROOT / "data" / "texts" / f"AXN-{hex_id}-text.md").read_text(encoding="utf-8")
    if text.startswith("---\n"):
        text = text[text.index("\n---\n", 4) + 5:]
    heads = [m.start() for m in re.finditer(r"(?m)^# ", text)]
    if len(heads) < 2:
        raise SystemExit(f"AXN-{hex_id}: expected the outer title and the poem's own title")
    return text[heads[1]:].rstrip("\n") + "\n"


def sections(body: str):
    out, cur = {}, None
    for line in body.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur is not None and line.strip():
            out[cur].append(line.rstrip())
    return out


def compression_line(body: str, spec) -> str:
    head, how, marker = spec
    lines = sections(body).get(head)
    if not lines:
        raise SystemExit(f"compression heading not found: {head}")
    if how == "first":
        return lines[0]
    i = lines.index(marker)
    return lines[i + 1]


def code_block(body: str) -> str:
    """The card's rendering, as the coda of v0.6 rendered #1642: headings lose their
    marks, lines lose their trailing break spaces, blank lines go, the poem's own
    title and byline line stay in the record."""
    lines, started = [], False
    for line in body.splitlines():
        if line.startswith("## "):
            started = True
            lines.append(line[3:].rstrip())
        elif started and line.strip():
            lines.append(line.rstrip())
    return "```text\n" + "\n".join(lines) + "\n```"


def build():
    reg = load_registry()
    rows, blocks = [], []
    for i, spec in enumerate(LINEAGE, 1):
        d = reg.get(spec["deposit"])
        if not d or d.get("hex") != spec["hex"]:
            raise SystemExit(f"#{spec['deposit']}: not in the registry at hex {spec['hex']}")
        body = seated_body(spec["hex"])
        rows.append({
            "id": f"L{i}",
            "order": i,
            "deposit": spec["deposit"],
            "axn": d["axn"],
            "title": d["title"],
            "creator": d["creator"],
            "byline": spec["byline"],
            "venue": d.get("journal"),
            "date": d["date"],
            "record_uri": f"https://www.alexanarch.org/s/records/{spec['deposit']}/",
            "text_uri": f"https://www.alexanarch.org/data/texts/AXN-{spec['hex']}-text.md",
            "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
            "follows": spec["follows"],
            "checksums": spec["checksums"],
            "own_compression": compression_line(body, spec["compression"]),
            "note": spec["note"],
            "poem_in_card": True,
            "converted_into_rows": False,
        })
        venue = f" · {d['journal']}" if d.get("journal") else ""
        blocks.append(
            f"### {['I', 'II', 'III'][i - 1]}. {d['title']}\n\n"
            f"*{spec['byline']}{venue} · {d['date']} · "
            f"[deposit #{spec['deposit']}](https://www.alexanarch.org/s/records/{spec['deposit']}/), "
            f"`{d['axn']}`*\n\n{code_block(body)}"
        )
    jsonl = "".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows)
    card = (f"{BEGIN}\n## Coda: GLYPHIC CHECKSUM LINEAGE\n\n{INTRO}\n\n"
            + "\n\n".join(blocks) + f"\n{END}")
    return jsonl, card


def splice(readme: str, card: str) -> str:
    if BEGIN in readme:
        a, b = readme.index(BEGIN), readme.index(END) + len(END)
        return readme[:a] + card + readme[b:]
    return readme.rstrip("\n") + "\n\n---\n\n" + card + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    jsonl, card = build()
    drift = []
    for t in TARGETS:
        jp, rp = t / "checksum_lineage.jsonl", t / "README.md"
        readme = rp.read_text(encoding="utf-8")
        if args.check:
            if not jp.exists() or jp.read_text(encoding="utf-8") != jsonl:
                drift.append(f"{jp.relative_to(ROOT)}")
            if BEGIN not in readme or splice(readme, card) != readme:
                drift.append(f"{rp.relative_to(ROOT)} (lineage block)")
        else:
            jp.write_text(jsonl, encoding="utf-8")
            rp.write_text(splice(readme, card), encoding="utf-8")
    if drift:
        print("CHECKSUM LINEAGE DRIFT:", *drift, sep="\n  ")
        sys.exit(1)
    print(("ok: " if args.check else "wrote: ")
          + f"{jsonl.count(chr(10))} poems, identical in {len(TARGETS)} datasets")


if __name__ == "__main__":
    main()
