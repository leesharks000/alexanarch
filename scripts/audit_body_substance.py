#!/usr/bin/env python3
"""audit_body_substance.py — classify a deposit by its body, not by its label.

THE DEFECT THIS EXISTS TO CATCH
-------------------------------
`body_status.class` is a stored declaration. It can be wrong, and when it is
wrong it is wrong in the direction that hides the problem: a record whose body
is a 2.8 KB metadata stub declaring `class: full` is invisible to every sweep
that searches for records declared incomplete. The population most needing
restoration is precisely the population whose declaration is false.

Worse, downstream repairs trust it. On 2026-07-30 a status-reconciliation pass
took `class` as authoritative and propagated "full text seated" outward into
content_type, description, keywords and wiki articles for records whose bodies
were stubs — making the archive assert, in five more places, something it had
already got wrong in one. A declaration was corrected against another
declaration. Nothing measured the file.

THE RULE
--------
Substance is measured, never declared. This script reads the body, strips
frontmatter and known scaffold blocks, counts what prose remains, and reports
disagreement with the stored class. Registry fields are derived from the
measurement; the measurement is derived from the bytes.

    python3 scripts/audit_body_substance.py            # report
    python3 scripts/audit_body_substance.py --apply    # correct declarations
    python3 scripts/audit_body_substance.py --strict   # exit 1 on disagreement (CI)
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
QUEUE = ROOT / "data" / "worklists" / "restoration-queue.json"

# Scaffold the mint pipeline or a metadata capture adds around a body. None of
# it is the work; all of it inflates a naive length check.
SCAFFOLD = [
    re.compile(r"^---\n.*?\n---\n", re.S),                      # YAML frontmatter
    re.compile(r"SEMI-RESTORED RECORD.*?(?=\n#|\Z)", re.S | re.I),
    re.compile(r"Appendix — metadata-capture body.*\Z", re.S),  # retained appendix
    re.compile(r"^\s*(deposit_number|hex|title|creator|orcid|date|content_type|"
               r"license|substrate|version|related_ids|axn_schema_version|"
               r"protocol_version|keywords)\s*:.*$", re.M),
    re.compile(r"^\s*-\s+[A-Za-z@#][\w @#.\-']{0,40}$", re.M),  # bare keyword list items
    re.compile(r"Full text not yet recovered\..*?(?=\n|\Z)", re.S | re.I),
    re.compile(r"Restoration status:.*?(?=\n|\Z)", re.S),
    re.compile(r"Dead DOI\(s\):.*?(?=\n|\Z)", re.S),
    re.compile(r"Captured (description|subjects|citation):.*?(?=\n\n|\Z)", re.S | re.I),
]

STUB_WORDS = 400          # below this, a body is not a work
NATIVE_SHORT_OK = {"native_short", "stub_short", "dataset_pointer", "notice", "pointer"}


def substance(path):
    """Return (raw_bytes, prose_words) with scaffold removed."""
    p = ROOT / path.lstrip("/")
    if not p.is_file():
        return None, None
    raw = p.read_text(encoding="utf-8", errors="ignore")
    t = raw
    for pat in SCAFFOLD:
        t = pat.sub(" ", t)
    t = re.sub(r"https?://\S+", " ", t)            # bare URLs are not prose
    t = re.sub(r"[#*`>|\-_=]{2,}", " ", t)          # rules and markup runs
    words = [w for w in re.findall(r"[A-Za-z\u00C0-\u024F\u4e00-\u9fff\u3040-\u30ff]{2,}", t)]
    return len(raw), len(words)


def main():
    apply_ = "--apply" in sys.argv
    strict = "--strict" in sys.argv
    reg = json.loads(REG.read_text())
    findings = []
    for d in reg["deposits"]:
        bs = d.setdefault("body_status", {})
        cls = bs.get("class")
        fp = d.get("full_text_path")
        if not fp:
            continue
        raw, words = substance(fp)
        if raw is None:
            findings.append({"n": d["deposit_number"], "issue": "body_file_missing",
                             "declared": cls, "words": None, "title": d["title"][:70]})
            continue
        bs["measured_prose_words"] = words
        bs["measured_at"] = "2026-07-31"
        if cls == "full" and words < STUB_WORDS and cls not in NATIVE_SHORT_OK:
            findings.append({"n": d["deposit_number"], "issue": "declared_full_body_is_stub",
                             "declared": cls, "words": words, "bytes": raw,
                             "recovery_status": bs.get("recovery_status"),
                             "title": d["title"][:70]})
            if apply_:
                bs["class_before_substance_audit"] = cls
                bs["class"] = "metadata_capture"
                bs["substance_audit"] = (
                    f"Reclassified 2026-07-31: declared full, measured {words} prose "
                    f"words after scaffold removal. Substance is measured, not declared.")
                touch(d, "body_status",
                      "Body-substance audit: record declared class=full while its body "
                      "measured as a metadata stub. Reclassified from the bytes.",
                      was=cls, now="metadata_capture", when="2026-07-31")
    print(f"{'' if apply_ else 'DRY RUN — '}deposits audited: {len(reg['deposits'])}")
    print(f"  declared full / body is a stub : "
          f"{sum(1 for f in findings if f['issue']=='declared_full_body_is_stub')}")
    print(f"  body file missing              : "
          f"{sum(1 for f in findings if f['issue']=='body_file_missing')}")
    if apply_:
        REG.write_text(json.dumps(reg, indent=1, ensure_ascii=False), encoding="utf-8")
        QUEUE.parent.mkdir(parents=True, exist_ok=True)
        QUEUE.write_text(json.dumps({
            "description": (
                "Deposits whose bodies measure as stubs. Each is a restoration target: "
                "the work exists somewhere (blog, repo, mirror, print) and the archive "
                "holds only its metadata. Measured, not declared."),
            "rule": f"prose words < {STUB_WORDS} after scaffold removal",
            "dateModified": "2026-07-31", "count": len(findings),
            "entries": sorted(findings, key=lambda f: f.get("words") or 0),
        }, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"  registry corrected; queue → {QUEUE.relative_to(ROOT)}")
    if strict and findings:
        print("::error title=body substance::A deposit declares full text it does not hold.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
