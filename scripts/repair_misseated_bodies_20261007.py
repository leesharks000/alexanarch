#!/usr/bin/env python3
"""repair_misseated_bodies_20261007.py — two canonical bodies returned to their works (operator, 2026-10-07:
"lets make these fixes"), under the recorded-correction protocol of restore_in_place.py (2026-07-28):
seat the canonical body with a provenance header, new hash and glyph, AXN recomposed same-family, the prior AXN
and the superseded bytes' sha256 kept in `restoration`, a remediation note and a record_modifications entry.

#436 (AXN:00FB) APZPZ C: ΦΑΙΝΕΤΑΙ ΜΟΙ. Recovery wave 1 (d7811088b1, 2026-08-05) seated the text of #1048
  (EA-ERRATUM-SAPPHO31-STANZA-02) here under a 0.60 title-overlap probe, and recorded #1048 as "other instance of
  this work". The record's original seated text (4cf085230d, 2026-06-20), byte-identical to its wrapper
  data/deposits/AXN-00FB.md, is the APZPZ C document itself, and is returned.
#1032 (AXN:0414) revelationfirst.com — Thesis Site, Impact Tracker, and Staging Materials. The body seated
  2026-07-20 from a blog mirror is the staging document the title and the DataCite abstract name, in a degraded
  conversion: its opening characters cut ("VELATION FIRST"), headings, emphasis, rules and tables flattened. The
  canonical file STAGING.md in leesharks000/revelationfirst-com (git blob be2b3e566d…) is seated.

Departure from restore_in_place, stated: the superseded bytes are NOT appended. For #436 they are another
deposit's canonical text, held whole at #1048; appending them would seat that work here a second time. For #1032
they are a lossy conversion of the same document. In both, the superseded bytes stay in git history and their
sha256 and source are kept in `restoration`.

Usage: python3 scripts/repair_misseated_bodies_20261007.py <path-to-STAGING.md>
"""
import json, hashlib, subprocess, sys, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

TODAY = "2026-10-07"
STAGING_BLOB = "be2b3e566d0404039a3d7b83f32cfffbf125ac5a"
STAGING_SRC = "https://github.com/leesharks000/revelationfirst-com/blob/18d3eed852224e22129d98787856cdaa1af4ccf9/STAGING.md"


def git_blob(b):
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def seat(d, header, body, source, superseded, note, extra_bs=None):
    hx, fam = d["hex"], d.get("family", "ARCHIVAL")
    tp = (d.get("full_text_path") or f"/data/texts/AXN-{hx}-text.md").lstrip("/")
    old = (ROOT / tp).read_bytes()
    text = header + body.rstrip("\n") + "\n"
    (ROOT / tp).write_text(text, encoding="utf-8")
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    old_axn = d.get("axn")
    glyph = axn_glyph_from_hash(h)
    d.update({"hash": h, "axn_canonical": h, "emoji": glyph, "axn": compose_axn(hx, fam, glyph),
              "clusters": axn_clusters_from_hash(h), "version": "v0.2-restored", "full_text_path": "/" + tp})
    d["reading"] = axn_reading_from_clusters(d["clusters"])
    r = d.get("restoration") if isinstance(d.get("restoration"), dict) else {}
    r.update({"fulltext": "restored", "fulltext_source": source, "restored_at": TODAY, "axn_before_restoration": old_axn,
              "superseded_body_sha256": hashlib.sha256(old).hexdigest(), "superseded_body": superseded,
              "ruled_by": "operator, 2026-10-07: 'lets make these fixes'"})
    d["restoration"] = r
    d["remediation_note"] = f"{TODAY} BODY RETURNED TO ITS WORK (in-place, recorded correction): {note}"
    d["canonical_text_status"] = "recovered_full_text"
    prev = d.get("body_status") if isinstance(d.get("body_status"), dict) else {}
    bs = {"class": "full", "lacuna": False, "recovery_status": "RESTORED-20261007", "recovered_from": source,
          "residual_chars": len(text), "audited_at": datetime.datetime.now(datetime.UTC).isoformat(),
          "audit_version": "repair_misseated_bodies-20261007", "class_before_restoration": prev.get("class"),
          "superseded_status": {k: prev[k] for k in ("recovery_status", "recovered_from", "source_recovery", "semi_audit") if k in prev}}
    bs.update(extra_bs or {})
    d["body_status"] = bs
    d.setdefault("record_modifications", []).append({"date": TODAY, "field": "canonical_text", "note": note,
                                                     "axn_before": old_axn, "axn_after": d["axn"]})
    return old_axn, d["axn"], len(text)


def main():
    staging = pathlib.Path(sys.argv[1]).read_bytes()
    assert git_blob(staging) == STAGING_BLOB, "STAGING.md is not the canonical blob"
    reg_p = ROOT / "data" / "registry.json"
    reg = json.loads(reg_p.read_text(encoding="utf-8"))
    by = {d["deposit_number"]: d for d in reg["deposits"]}

    # 436
    d = by[436]
    orig = subprocess.run(["git", "show", "4cf085230d:data/texts/AXN-00FB-text.md"], cwd=ROOT, capture_output=True, check=True).stdout
    assert orig == (ROOT / "data/deposits/AXN-00FB.md").read_bytes(), "original seating no longer matches the wrapper"
    assert "ΦΑΙΝΕΤΑΙ ΜΟΙ" in orig.decode() and "Rebekah Cranes" in orig.decode()
    hdr = (f"# {d['title']}\n\n**{d.get('creator')}** · restored {TODAY}\n\n"
           f"**AXN:** AXN:{d['hex']} — Alexanarch deposit #436 (self-reference in root form by pre-hash necessity)\n"
           "**Restoration status:** RESTORED (v0.2) — the record's original seated text (2026-06-20), byte-identical to its "
           "deposit wrapper, returned as the canonical body. The 2026-08-05 recovery wave had seated the text of #1048 "
           "(EA-ERRATUM-SAPPHO31-STANZA-02) here under a title-overlap probe; that work is held whole at #1048.\n"
           "**Dead DOI:** 10.5281/zenodo.18459573 — severed 2026-06-19.\n\n---\n\n")
    note436 = ("the canonical text held the text of #1048 (EA-ERRATUM-SAPPHO31-STANZA-02), seated by recovery wave 1 "
               "(2026-08-05) under a 0.60 title-overlap probe; the record's original seated text (2026-06-20), the APZPZ C "
               "document and byte-identical to its wrapper, is returned. The false relation to #1048 as 'other instance of "
               "this work' is removed; the open audit directive (Cranes as editor/translator, critical-edition typing, "
               "licence) stands.")
    prev = d.get("body_status") or {}
    ri = prev.get("related_instances") if isinstance(prev.get("related_instances"), dict) else None
    extra = {}
    if ri:
        kept = {k: v for k, v in ri.items() if k != "instances"}
        kept["instances"] = [i for i in ri.get("instances", []) if i.get("deposit_number") != 1048]
        kept["removed"] = [{"deposit_number": 1048, "date": TODAY,
                            "reason": "a different work (the erratum to the erratum on stanza numbering); matched by title overlap only"}]
        extra["related_instances"] = kept
    for k in ("work_sha256", "prior_bytes_sha256", "measured_prose_words", "measured_at"):
        if k in prev:
            extra.setdefault("superseded_measures", {})[k] = prev[k]
    print(436, *seat(d, hdr, orig.decode("utf-8"), "data/deposits/AXN-00FB.md (original seating, commit 4cf085230d)",
                     "text of #1048 seated by recovery wave 1, 2026-08-05", note436, extra))

    # 1032
    d = by[1032]
    hdr = (f"# {d['title']}\n\n**{d.get('creator')}** · restored {TODAY}\n\n"
           f"**AXN:** AXN:{d['hex']} — Alexanarch deposit #1032 (self-reference in root form by pre-hash necessity)\n"
           f"**Restoration status:** RESTORED (v0.2) — the staging document this deposit's title and DataCite abstract name, "
           f"seated from its canonical source file ({STAGING_SRC}). It replaces a blog-mirror conversion of the same "
           "document seated 2026-07-20, whose opening characters were cut and whose headings, emphasis, rules and tables "
           "were flattened. The thesis site and impact tracker are live at revelationfirst.com and held in that repository.\n"
           "**Dead DOI:** 10.5281/zenodo.20735337 — severed 2026-06-19.\n\n---\n\n")
    note1032 = ("the body seated 2026-07-20 from a blog mirror was the staging document in a degraded conversion (opening "
                "characters cut: 'VELATION FIRST'; headings, emphasis, rules and tables flattened); the canonical STAGING.md "
                f"from leesharks000/revelationfirst-com (git blob {STAGING_BLOB}) is seated.")
    print(1032, *seat(d, hdr, staging.decode("utf-8"), STAGING_SRC,
                      "blog-mirror conversion of the staging document, seated 2026-07-20", note1032))

    reg["last_updated"] = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    reg_p.write_text(json.dumps(reg, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


if __name__ == "__main__":
    main()
