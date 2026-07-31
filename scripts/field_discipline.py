#!/usr/bin/env python3
"""field_discipline.py — genre in the genre field, condition in the condition field.

PATHOLOGY-30 (Atlas v0.7). A record's condition was written into `content_type`,
`version` and keywords as well as `body_status.class`. Those three fields carry
other claims and must not carry this one.

    content_type   genre only.   For a capture, the genre is "Metadata capture" —
                                 an accurate description of the object actually
                                 deposited. When canonical bytes are recovered
                                 they supersede it and declare their own genre.
    version        a version only. "semi-restored v1.0" is malformed on both axes.
    keywords       subject only.  "semi-restored" is not a subject.

WHAT THIS WILL NOT DO
---------------------
Where a record is classed `full` but its `content_type` holds nothing but
condition language, the genre is genuinely unknown: the mint-time frontmatter
holds the same condition string, so there is nothing to recover it from.
Inventing a genre would be another unchecked assertion. Those records are
flagged for ruling and left untouched.

    python3 scripts/field_discipline.py            # report
    python3 scripts/field_discipline.py --apply
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from record_modification import touch  # noqa: E402

REG = ROOT / "data" / "registry.json"
FLAGS = ROOT / "data" / "worklists" / "genre-unknown.json"

CAPTURE_CLASSES = {"metadata_capture"}
CONDITION = re.compile(r"semi[- ]restored|metadata[- ]only|metadata capture|"
                       r"full text seated|recovered work|no full text", re.I)
COND_KEYWORDS = {"semi-restored", "semi restored", "metadata-only", "metadata only",
                 "severed doi", "zenodo termination"}
CAPTURE_GENRE = "Metadata capture"
VERSION_STRIP = re.compile(r"semi[- ]restored\s*|restored\s*(?=v)", re.I)


def main():
    apply_ = "--apply" in sys.argv
    reg = json.loads(REG.read_text())
    n_ct = n_v = n_k = 0
    flags = []
    for d in reg["deposits"]:
        bs = d.get("body_status") or {}
        cls = bs.get("class")
        # ── content_type: genre only ──
        ct = str(d.get("content_type") or "")
        if CONDITION.search(ct):
            if cls in CAPTURE_CLASSES:
                if ct != CAPTURE_GENRE:
                    n_ct += 1
                    if apply_:
                        touch(d, "content_type",
                              "Genre and condition are different claims (Atlas v0.7, "
                              "PATHOLOGY-30). The genre of a metadata capture is "
                              "'Metadata capture' — what was deposited is a capture. "
                              "Condition lives in body_status.class.",
                              was=ct, now=CAPTURE_GENRE, when="2026-07-31")
                        d["content_type"] = CAPTURE_GENRE
            else:
                # classed as holding a work, but the genre field holds only
                # condition language. Nothing to recover it from; do not invent.
                flags.append({"deposit_number": d["deposit_number"], "class": cls,
                              "content_type": ct, "title": d["title"][:80],
                              "issue": "genre unknown — content_type holds condition only",
                              "status": "pending ruling"})
        # ── version: a version only ──
        v = str(d.get("version") or "")
        if CONDITION.search(v):
            nv = VERSION_STRIP.sub("", v).strip() or "v1.0"
            n_v += 1
            if apply_:
                touch(d, "version",
                      "Version field carried restoration condition. Condition lives "
                      "in body_status.class (Atlas v0.7, PATHOLOGY-30).",
                      was=v, now=nv, when="2026-07-31")
                d["version"] = nv
        # ── keywords: subject only ──
        kws = d.get("keywords") or []
        if isinstance(kws, str):
            kws = [k.strip() for k in kws.split(",") if k.strip()]
        keep = [k for k in kws if str(k).strip().lower() not in COND_KEYWORDS]
        if len(keep) != len(kws):
            n_k += 1
            if apply_:
                touch(d, "keywords",
                      "Removed condition terms from the subject keyword set "
                      "(Atlas v0.7, PATHOLOGY-30).",
                      was=f"{len(kws)} terms", now=f"{len(keep)} terms", when="2026-07-31")
                d["keywords"] = keep
    print(f"{'' if apply_ else 'DRY RUN — '}field discipline")
    print(f"    content_type → genre        {n_ct}")
    print(f"    version      → version only {n_v}")
    print(f"    keywords     → subject only {n_k}")
    print(f"    genre unknown, flagged      {len(flags)}")
    if apply_:
        REG.write_text(json.dumps(reg, indent=1, ensure_ascii=False), encoding="utf-8")
        FLAGS.parent.mkdir(parents=True, exist_ok=True)
        FLAGS.write_text(json.dumps({
            "description": (
                "Records classed as holding a work whose content_type holds only "
                "restoration condition, leaving genre unrecoverable from the registry "
                "or the mint-time frontmatter. Ruling required; nothing inferred."),
            "dateModified": "2026-07-31", "count": len(flags), "entries": flags,
        }, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    written → {FLAGS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
