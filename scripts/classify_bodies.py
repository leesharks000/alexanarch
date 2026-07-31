#!/usr/bin/env python3
"""classify_bodies.py — classify by what the record says, not by how long it is.

HISTORY THIS EXISTS TO CORRECT
------------------------------
On 2026-07-30 a word-count discriminator classified any body under 400 prose
words as a stub. It was wrong in both directions and expensively so. It
condemned as fragments: the complete Greek text of Revelation (its regex did
not count Greek), a complete work in emoji notation, two-line poems, registry
tables, and the canon provenance nodes whose finished form is about 3.5 KB. It
then propagated "full text seated" outward into content_type, description, and
keywords for records that really were captures.

Reading all 207 small undeclared bodies on 2026-07-31 found zero stubs among
them. The backlog the counter produced was almost entirely false.

THE RULE
--------
A capture SAYS it is a capture, in its own first lines. Two header forms are in
use, both from the restoration passes:

    SEMI-RESTORED RECORD (metadata capture only; no full text)
    **Restoration status:** SEMI-RESTORED ...

Everything else holds a work. Length is not evidence. A canon node is 3.5 KB
and finished; a mandala facing-edition is 7 KB and a capture. Only the
declaration distinguishes them, and the declaration is written in words.

IMAGE-BORNE WORKS
-----------------
A third class the reading revealed: bodies consisting of an image reference and
essentially nothing else. The work is the image. Calling these "full text" is
false and queueing them for text restoration is also false. They are classed
`image_borne` and are neither.
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from record_modification import touch  # noqa: E402

REG = ROOT / "data" / "registry.json"
FINDINGS = ROOT / "data" / "worklists" / "body-classification-findings.json"

CAPTURE = re.compile(
    r"SEMI-RESTORED RECORD\s*\(metadata capture only"
    r"|\*\*Restoration status:\*\*\s*SEMI[- ]RESTORED",
    re.I)
IMG = re.compile(r"!?\[[^\]]*\]\(https?://[^)]+\)|<img\b", re.I)


def prose_of(path):
    p = ROOT / path.lstrip("/")
    if not p.is_file():
        return None
    t = p.read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"^---\n.*?\n---\n", t, re.S)
    return t[m.end():] if m else t


def classify(prose):
    """Return one of: metadata_capture, image_borne, full."""
    head = prose[:2500]
    if CAPTURE.search(head):
        return "metadata_capture"
    # image-borne: strip image refs, headings and metadata lines; if almost
    # nothing readable remains, the image is the work.
    t = IMG.sub(" ", prose)
    t = re.sub(r"^#+.*$|^\*\*[^*]+:\*\*.*$|^https?://\S+$", " ", t, flags=re.M)
    words = re.findall(r"[A-Za-z\u00C0-\u024F\u0370-\u03FF\u0590-\u05FF"
                       r"\u0600-\u06FF\u0900-\u097F\u4e00-\u9fff]{2,}", t)
    if IMG.search(prose) and len(words) < 25:
        return "image_borne"
    return "full"


def main():
    apply_ = "--apply" in sys.argv
    reg = json.loads(REG.read_text())
    counts = {}
    changes = []
    for d in reg["deposits"]:
        fp = d.get("full_text_path")
        if not fp:
            continue
        prose = prose_of(fp)
        if prose is None:
            continue
        want = classify(prose)
        counts[want] = counts.get(want, 0) + 1
        bs = d.setdefault("body_status", {})
        have = bs.get("class")
        # native_short / stub_short / dataset_pointer are deliberate mint-time
        # declarations about form, not restoration state. Leave them alone.
        if have in {"native_short", "stub_short", "dataset_pointer", "notice", "pointer"}:
            continue
        if have != want:
            changes.append({"n": d["deposit_number"], "was": have, "now": want,
                            "title": d["title"][:70]})
            if apply_:
                bs["class"] = want
                bs["classified_by"] = "read-audit 2026-07-31 (declaration, not length)"
                for k in ("class_before_substance_audit", "substance_audit",
                          "measured_prose_words", "measured_at", "read_audit"):
                    bs.pop(k, None)
                touch(d, "body_status",
                      "Reclassified by reading the body's own declaration. The prior "
                      "word-count classification misjudged short complete works as "
                      "fragments and missed captures using a second header form.",
                      was=have, now=want, when="2026-07-31")
    print(f"{'' if apply_ else 'DRY RUN — '}classified {sum(counts.values())} bodies")
    for k in sorted(counts, key=lambda x: -counts[x]):
        print(f"    {k:20s} {counts[k]}")
    print(f"  changes: {len(changes)}")
    if apply_:
        REG.write_text(json.dumps(reg, indent=1, ensure_ascii=False), encoding="utf-8")
        FINDINGS.parent.mkdir(parents=True, exist_ok=True)
        FINDINGS.write_text(json.dumps({
            "description": (
                "Body classification by reading each record's own declaration. "
                "Supersedes the 2026-07-30 word-count audit, which produced a "
                "largely false restoration backlog."),
            "dateModified": "2026-07-31",
            "counts": counts, "changes": changes,
        }, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"  written → {FINDINGS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
