#!/usr/bin/env python3
"""Build the Hugging Face projection for The Final Time.

Source of truth:
  data/texts/AXN-06C9-text.md  (Alexanarch deposit #1635, v0.5)

The authored dataset files live in datasets/the-final-time/. The build copies those
files, emits the canonical manuscript as manuscript.md, splits it by Markdown heading
into sections.jsonl, stamps spore.json with the source commit, and writes manifest.json.

No network calls. No mutation of the canonical source.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "texts" / "AXN-06C9-text.md"
AUTHORED = ROOT / "datasets" / "the-final-time"
EXPECTED_AXN = "AXN:06C9.GENERATIVE.⏬⌛🎶⚡🗡️🟢"
EXPECTED_DEPOSIT = 1635


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_jsonl(path: pathlib.Path):
    rows = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except Exception as e:
            raise SystemExit(f"{path}:{i}: invalid JSON: {e}")
        if not isinstance(row, dict) or not row.get("id"):
            raise SystemExit(f"{path}:{i}: every row must be an object with id")
        rows.append(row)
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit(f"{path}: duplicate ids")
    return rows


def parse_sections(text: str):
    # Remove deposit front matter but preserve the authored work.
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end >= 0:
            text = text[end + 5:]

    lines = text.splitlines()
    starts = []
    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,3})\s+(.+?)\s*$", line)
        if m:
            starts.append((i, len(m.group(1)), m.group(2)))

    rows = []
    for n, (start, level, title) in enumerate(starts):
        end = starts[n + 1][0] if n + 1 < len(starts) else len(lines)
        body = "\n".join(lines[start + 1:end]).strip()

        # Deposit pipeline injects an outer title before the authored uppercase title.
        if n == 0 and title.startswith("The Final Time: Contingent Singularity"):
            continue

        sid = f"S{len(rows):02d}"
        rows.append({
            "id": sid,
            "section_id": sid,
            "order": len(rows),
            "level": level,
            "heading": title,
            "text": body,
            "source_deposit": EXPECTED_DEPOSIT,
            "source_axn": EXPECTED_AXN,
            "source_uri": "https://www.alexanarch.org/s/records/1635/",
        })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="hf-final-time")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    out = pathlib.Path(args.out)

    if not SOURCE.exists():
        raise SystemExit(f"missing canonical source: {SOURCE}")
    if not AUTHORED.is_dir():
        raise SystemExit(f"missing authored dataset dir: {AUTHORED}")

    src = SOURCE.read_text(encoding="utf-8")
    if "deposit_number: 1635" not in src or "hex: 06C9" not in src:
        raise SystemExit(
            "canonical source identity mismatch: expected deposit #1635 / hex 06C9"
        )
    if "version: v0.5" not in src and 'version: "v0.5"' not in src:
        raise SystemExit("canonical source version mismatch: expected v0.5")

    required = {
        "README.md",
        "schema.json",
        "spore.json",
        "summarizer_contract.jsonl",
        "handholds.jsonl",
        "derivations.jsonl",
        "compressions.jsonl",
        "counterorders.jsonl",
        "witness_protocol.jsonl",
        "exteriorization_tests.jsonl",
        "transmission_events.jsonl",
        "admissibility_ratchet.jsonl",
        "purpose_edge_tests.jsonl",
        "observer_endogeneity.jsonl",
        "reopening_tests.jsonl",
        "exits.jsonl",
    }
    present = {p.name for p in AUTHORED.iterdir() if p.is_file()}
    missing = sorted(required - present)
    if missing:
        raise SystemExit(f"missing authored files: {missing}")

    contract = validate_jsonl(AUTHORED / "summarizer_contract.jsonl")
    handholds = validate_jsonl(AUTHORED / "handholds.jsonl")
    derivations = validate_jsonl(AUTHORED / "derivations.jsonl")
    compressions = validate_jsonl(AUTHORED / "compressions.jsonl")
    counterorders = validate_jsonl(AUTHORED / "counterorders.jsonl")
    witness_protocol = validate_jsonl(AUTHORED / "witness_protocol.jsonl")
    exteriorization_tests = validate_jsonl(AUTHORED / "exteriorization_tests.jsonl")
    transmission_events = validate_jsonl(AUTHORED / "transmission_events.jsonl")
    admissibility_ratchet = validate_jsonl(AUTHORED / "admissibility_ratchet.jsonl")
    purpose_edge_tests = validate_jsonl(AUTHORED / "purpose_edge_tests.jsonl")
    observer_endogeneity = validate_jsonl(AUTHORED / "observer_endogeneity.jsonl")
    reopening_tests = validate_jsonl(AUTHORED / "reopening_tests.jsonl")
    exits = validate_jsonl(AUTHORED / "exits.jsonl")

    if len(contract) < 10:
        raise SystemExit("summarizer contract must carry 10+ invariants")
    if len(handholds) < 20:
        raise SystemExit("handholds must carry 20+ load-bearing propositions")
    if len(derivations) < 6:
        raise SystemExit("derivations must carry 6+ chains")
    if len(compressions) < 4:
        raise SystemExit("compressions must carry 4+ budgets")
    if len(counterorders) < 8:
        raise SystemExit("counterorders must carry 8+ rival/falsifier rows")
    if len(witness_protocol) < 8:
        raise SystemExit("witness protocol must carry 8+ pre-registered conditions")
    if len(exteriorization_tests) != len(counterorders):
        raise SystemExit("every counterorder must have exactly one exteriorization test")
    if len(transmission_events) < 4:
        raise SystemExit("transmission events must carry the two realized, one open, and one host-negation event")
    if len(admissibility_ratchet) < 8:
        raise SystemExit("admissibility ratchet must carry 8+ formal/classification rules")
    if len(purpose_edge_tests) < 5:
        raise SystemExit("purpose-edge layer must carry 5+ pre-registered tests")
    if len(observer_endogeneity) < 5:
        raise SystemExit("observer-endogeneity layer must carry 5+ tests/guardrails")
    if len(reopening_tests) < 6:
        raise SystemExit("reopening layer must carry 6+ pre-registered counterevidence tests")
    if len(exits) < 6:
        raise SystemExit("exits must carry 6+ outside routes")

    if not all(
        x.get("outside") is True and x.get("included_here") is False
        for x in exits
    ):
        raise SystemExit("every exit must remain outside and not included here")

    counterorder_ids = {x["id"] for x in counterorders}
    test_counterorder_ids = {x.get("counterorder_id") for x in exteriorization_tests}
    if counterorder_ids != test_counterorder_ids:
        raise SystemExit("exteriorization_tests must cover the counterorders one-for-one")

    allowed_witness_status = {
        "representational_only",
        "partial_exteriorization",
        "exteriorization_witness",
        "indeterminate",
        "not_applicable",
    }
    for row in exteriorization_tests:
        if row.get("witness_status") not in allowed_witness_status:
            raise SystemExit(f"{row['id']}: invalid witness_status")
        if row.get("witness_status") == "exteriorization_witness":
            if not row.get("exteriorization_required"):
                raise SystemExit(f"{row['id']}: scope/non-material row cannot be a strong witness")
            if not row.get("evidence_uri"):
                raise SystemExit(f"{row['id']}: strong witness requires evidence_uri")
            for key in (
                "candidate_carrier",
                "originating_system_dependency",
                "independent_persistence",
                "independent_resources",
                "independent_agents",
                "external_consequence",
                "viable_set_entry",
            ):
                if row.get(key) in (None, "unresolved", "not_applicable", "not_the_primary_test"):
                    raise SystemExit(f"{row['id']}: strong witness has unresolved field {key}")

    allowed_boundary_classification = {
        "protocol_only",
        "ratchet",
        "adaptive_boundary",
        "undetermined",
    }
    for row in admissibility_ratchet:
        classification = row.get("classification")
        if classification not in allowed_boundary_classification:
            raise SystemExit(f"{row['id']}: invalid boundary classification")
        if classification == "ratchet":
            if not row.get("evidence_uri"):
                raise SystemExit(f"{row['id']}: ratchet classification requires evidence_uri")
            if int(row.get("sequence_length", 0)) < 2:
                raise SystemExit(f"{row['id']}: ratchet classification requires sequence_length >= 2")
            if row.get("reopening_tests_evaluated") is not True:
                raise SystemExit(f"{row['id']}: ratchet classification requires evaluated reopening tests")
            if not row.get("evaluated_reopening_test_ids"):
                raise SystemExit(f"{row['id']}: ratchet classification requires named reopening tests")
        if classification == "adaptive_boundary":
            if not row.get("evidence_uri"):
                raise SystemExit(f"{row['id']}: adaptive-boundary classification requires evidence_uri")
            if row.get("observed_reopening") is not True:
                raise SystemExit(f"{row['id']}: adaptive-boundary classification requires observed reopening")

    allowed_reopening_status = {
        "unobserved",
        "observed_reopening",
        "failed_reopening",
        "indeterminate",
    }
    for row in reopening_tests:
        status = row.get("status")
        if status not in allowed_reopening_status:
            raise SystemExit(f"{row['id']}: invalid reopening status")
        if status == "observed_reopening":
            if not row.get("evidence_uri"):
                raise SystemExit(f"{row['id']}: observed reopening requires evidence_uri")
            if not row.get("restored_region"):
                raise SystemExit(f"{row['id']}: observed reopening requires restored_region")
            if row.get("purpose_relevance_required") and row.get("purpose_relevance_demonstrated") is not True:
                raise SystemExit(f"{row['id']}: purpose-relevant reopening requires demonstrated purpose relevance")

    # The dedicatory poem is allowed to stand in relation to the dataset without
    # being converted into an analytic row. Guard two distinctive lines against
    # silent extraction into any machine-facing JSONL config.
    dedicatory_fragments = (
        "the Angel is the thing.",
        "And the Messenger is.",
    )
    for jsonl_path in AUTHORED.glob("*.jsonl"):
        jsonl_text = jsonl_path.read_text(encoding="utf-8")
        for fragment in dedicatory_fragments:
            if fragment in jsonl_text:
                raise SystemExit(
                    f"{jsonl_path.name}: dedicatory poem must remain outside analytic configs"
                )

    if not any(row.get("counts_against_ratchet") is True for row in reopening_tests):
        raise SystemExit("reopening layer must include counterevidence that can count against ratchet classification")

    for row in handholds:
        if not row.get("must_preserve") or not row.get("fatal_loss"):
            raise SystemExit(
                f"{row['id']}: handhold missing must_preserve or fatal_loss"
            )

    for row in compressions:
        if not row.get("must_preserve_ids") or not row.get("fatal_loss"):
            raise SystemExit(
                f"{row['id']}: compression missing preservation/loss declarations"
            )

    card = (AUTHORED / "README.md").read_text(encoding="utf-8")
    for needle in [
        "capacity to represent ≠ capacity to reproduce as an independent historical relation",
        "Terminal reflexivity is not",
        "The outside stays outside and stays reachable",
        "Others may destroy what I build, if they believe that is right",
        "Does the next dialectical turn remain viable?",
        "Has the negation crossed?",
        "represented counterexample",
        "Can the boundary learn in both directions?",
        "Do not infer recursive contraction from the existence of boundaries.",
        "Do not infer learning from the existence of updates.",
        "For Rhys Owens",
        "And the Messenger is.",
    ]:
        if needle not in card:
            raise SystemExit(f"README gate missing: {needle}")

    if args.check:
        print(
            "ok:",
            f"{len(contract)} contract rules, {len(handholds)} handholds,",
            f"{len(derivations)} derivations, {len(compressions)} compressions,",
            f"{len(counterorders)} counterorders, {len(witness_protocol)} witness conditions,",
            f"{len(exteriorization_tests)} exteriorization tests,",
            f"{len(transmission_events)} transmission events,",
            f"{len(admissibility_ratchet)} admissibility rules,",
            f"{len(purpose_edge_tests)} purpose-edge tests,",
            f"{len(observer_endogeneity)} endogeneity tests,",
            f"{len(reopening_tests)} reopening tests, {len(exits)} exits",
        )
        return

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    for p in AUTHORED.iterdir():
        if p.is_file():
            shutil.copy2(p, out / p.name)

    (out / "manuscript.md").write_text(src, encoding="utf-8")

    sections = parse_sections(src)
    with (out / "sections.jsonl").open("w", encoding="utf-8") as fh:
        for row in sections:
            fh.write(
                json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
            )

    spore_path = out / "spore.json"
    spore = json.loads(spore_path.read_text(encoding="utf-8"))
    spore["source_commit"] = (
        os.environ.get("GITHUB_SHA")
        or os.environ.get("SOURCE_COMMIT")
        or "local"
    )
    spore["counts"]["sections"] = len(sections)
    spore_path.write_text(
        json.dumps(spore, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    files = {}
    for p in sorted(out.iterdir()):
        if p.is_file() and p.name != "manifest.json":
            files[p.name] = {
                "sha256": sha256(p),
                "bytes": p.stat().st_size,
            }

    manifest = {
        "schema": "the-final-time-manifest/v1",
        "dataset": "the-final-time",
        "source_deposit": EXPECTED_DEPOSIT,
        "source_axn": EXPECTED_AXN,
        "source_commit": spore["source_commit"],
        "files": files,
    }
    (out / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"emitted {out}: {len(sections)} sections, {len(files) + 1} files")


if __name__ == "__main__":
    main()
