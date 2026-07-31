#!/usr/bin/env python3
"""status_reconcile.py — one status, derived everywhere.

THE DEFECT
----------
A deposit's restoration status was stored independently in six places:

  body_status.class        the body's actual shape        AUTHORITATIVE
  canonical_text_status    the availability declaration   AUTHORITATIVE
  content_type             display string
  description              prose prefix ("SEMI-RESTORED RECORD…")
  keywords                 ["semi-restored", "metadata-only"]
  wiki_article             prose descriptor
  version                  e.g. "semi-restored v1.0"

When a record was restored — canonical bytes recovered and seated — the two
authoritative fields were updated and the four display fields were not. The
record then declared itself semi-restored on its own page, in its own keywords,
in its own encyclopedia entry, and in its own citation metadata, while holding
the full text directly beneath. Deposit #1230 is the exemplar: restored
2026-07-28, still announcing "no full text" in five places on 2026-07-30.

This is not a cosmetic problem. A reader, a crawler, and a composition layer all
read the display fields. An archive that documents provenance erasure cannot
publish a record whose own status is wrong in five of seven places.

THE RULE
--------
body_status.class and canonical_text_status are the source of truth. Every other
status expression is DERIVED from them. This script derives them, and the
validator gate refuses drift so it cannot silently return.

WHAT IS NOT TOUCHED
-------------------
Canonical bytes. The deposited text is immutable; where a restored record's body
retains an appendix recording the superseded metadata capture, that appendix
stays — it is the record's own history, kept per non-destruction.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from record_modification import touch  # noqa: E402

REG = ROOT / "data" / "registry.json"

# class → (is the body a capture?, canonical_text_status it implies)
CAPTURE_CLASSES = {"metadata_capture", "semi_apparatus", "stub_short",
                   "description_only", "excerpt_crossref"}

SR = re.compile(r"semi[- ]restored|metadata[- ]only|metadata capture", re.I)
SR_KEYWORDS = {"semi-restored", "metadata-only", "semi restored", "metadata only"}

# Prose sentences that assert capture status; removed when the record is full.
SR_SENTENCES = [
    re.compile(r"SEMI-RESTORED RECORD\s*\(metadata capture only;? no full text\)\.\s*", re.I),
    re.compile(r"SEMI-RESTORED RECORD\s*—\s*metadata capture only\s*", re.I),
    re.compile(r"Source tier:\s*DataCite full-metadata capture\.\s*", re.I),
    re.compile(r"Full text not yet recovered\.[^.]*\.\s*", re.I),
    re.compile(r"Restored under the metadata_only class[^.]*\.\s*", re.I),
]

CONTENT_TYPE_FOR_FULL = "Recovered work (full text seated)"


def is_capture(d):
    return (d.get("body_status") or {}).get("class") in CAPTURE_CLASSES


def reconcile(d, when=None):
    """Derive display status from the authoritative pair. Returns list of changes."""
    cap = is_capture(d)
    changed = []

    # canonical_text_status must agree with class
    cts = d.get("canonical_text_status")
    want_cts = "metadata_only" if cap else cts
    if cap and cts != "metadata_only":
        d["canonical_text_status"] = "metadata_only"
        changed.append(("canonical_text_status", cts, "metadata_only"))
    if not cap and cts == "metadata_only":
        new = "recovered_full_text"
        d["canonical_text_status"] = new
        changed.append(("canonical_text_status", cts, new))

    if cap:
        return changed  # captures may legitimately carry capture language

    # ── record is NOT a capture: strip capture language from display fields ──
    ct = str(d.get("content_type") or "")
    if SR.search(ct):
        d["content_type"] = CONTENT_TYPE_FOR_FULL
        changed.append(("content_type", ct, CONTENT_TYPE_FOR_FULL))

    v = str(d.get("version") or "")
    if SR.search(v):
        nv = re.sub(r"semi[- ]restored\s*", "", v, flags=re.I).strip() or "v1.0"
        d["version"] = nv
        changed.append(("version", v, nv))

    desc = str(d.get("description") or "")
    if SR.search(desc[:400]):
        nd = desc
        for pat in SR_SENTENCES:
            nd = pat.sub("", nd)
        nd = re.sub(r"\s{2,}", " ", nd).strip()
        if nd != desc:
            d["description"] = nd
            changed.append(("description", desc[:60] + "…", nd[:60] + "…"))

    kws = d.get("keywords") or []
    if any(str(k).strip().lower() in SR_KEYWORDS for k in kws):
        nk = [k for k in kws if str(k).strip().lower() not in SR_KEYWORDS]
        d["keywords"] = nk
        changed.append(("keywords", f"{len(kws)} terms", f"{len(nk)} terms"))

    wa = str(d.get("wiki_article") or "")
    if SR.search(wa[:400]):
        nw = re.sub(
            r"is an?\s+[\d,]+-word semi-restored record\s*\([^)]*\)",
            "is a recovered work with its full text seated", wa, flags=re.I)
        nw = re.sub(
            r"SEMI-RESTORED RECORD\s*\(metadata capture only;? no full text\)\.\s*",
            "", nw, flags=re.I)
        nw = re.sub(r"Source tier:\s*DataCite full-metadata capture\.\s*", "", nw, flags=re.I)
        nw = re.sub(r"\s{2,}", " ", nw).strip()
        if nw != wa:
            d["wiki_article"] = nw
            changed.append(("wiki_article", "capture language", "recovered language"))

    return changed


def main():
    dry = "--apply" not in sys.argv
    reg = json.loads(REG.read_text())
    touched = 0
    field_counts = {}
    for d in reg["deposits"]:
        ch = reconcile(d)
        if not ch:
            continue
        touched += 1
        for f, was, now in ch:
            field_counts[f] = field_counts.get(f, 0) + 1
            if not dry:
                touch(d, f, "Status declaration derived from body_status.class and "
                            "canonical_text_status; display field had retained capture "
                            "language after the record was restored.",
                      was=was, now=now, when="2026-07-30")
    print(f"{'DRY RUN — ' if dry else ''}records reconciled: {touched}")
    for f, n in sorted(field_counts.items(), key=lambda x: -x[1]):
        print(f"    {f:24s} {n}")
    if not dry:
        REG.write_text(json.dumps(reg, indent=1, ensure_ascii=False), encoding="utf-8")
        print("  registry written; modifications logged")
    else:
        print("  (re-run with --apply to write)")


if __name__ == "__main__":
    main()
