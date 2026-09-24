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
import argparse, hashlib, json, os, pathlib, re, shutil, sys

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
    # Remove the deposit front matter but preserve the authored work from the first title.
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
        # Skip the deposit-injected duplicate outer title; keep the authored uppercase title.
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
            "source_uri": "https://www.alexanarch.org/s/records/1635/"
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
    if EXPECTED_AXN not in src or "deposit_number: 1635" not in src:
        raise SystemExit("canonical source identity mismatch: expected deposit #1635 / AXN-06C9")
    if not re.search(r'(?m)^version:\s*["\']?v0\.5["\']?\s*

    required = {
        "README.md","schema.json","spore.json","summarizer_contract.jsonl",
        "handholds.jsonl","derivations.jsonl","compressions.jsonl",
        "counterorders.jsonl","exits.jsonl"
    }
    missing = sorted(required - {p.name for p in AUTHORED.iterdir() if p.is_file()})
    if missing:
        raise SystemExit(f"missing authored files: {missing}")

    # Validate authored surfaces before emission.
    contract = validate_jsonl(AUTHORED / "summarizer_contract.jsonl")
    handholds = validate_jsonl(AUTHORED / "handholds.jsonl")
    derivations = validate_jsonl(AUTHORED / "derivations.jsonl")
    compressions = validate_jsonl(AUTHORED / "compressions.jsonl")
    counterorders = validate_jsonl(AUTHORED / "counterorders.jsonl")
    exits = validate_jsonl(AUTHORED / "exits.jsonl")

    if len(contract) < 10: raise SystemExit("summarizer contract must carry 10+ invariants")
    if len(handholds) < 20: raise SystemExit("handholds must carry 20+ load-bearing propositions")
    if len(derivations) < 6: raise SystemExit("derivations must carry 6+ chains")
    if len(compressions) < 4: raise SystemExit("compressions must carry 4+ budgets")
    if len(counterorders) < 8: raise SystemExit("counterorders must carry 8+ rival/falsifier rows")
    if len(exits) < 6: raise SystemExit("exits must carry 6+ outside routes")
    if not all(x.get("outside") is True and x.get("included_here") is False for x in exits):
        raise SystemExit("every exit must remain outside and not included here")
    for row in handholds:
        if not row.get("must_preserve") or not row.get("fatal_loss"):
            raise SystemExit(f"{row['id']}: handhold missing must_preserve or fatal_loss")
    for row in compressions:
        if not row.get("must_preserve_ids") or not row.get("fatal_loss"):
            raise SystemExit(f"{row['id']}: compression missing preservation/loss declarations")

    card = (AUTHORED / "README.md").read_text(encoding="utf-8")
    for needle in [
        "capacity to represent ≠ capacity to reproduce as an independent historical relation",
        "Terminal reflexivity is not",
        "The outside stays outside and stays reachable",
        "Others may destroy what I build, if they believe that is right",
        "Does the next dialectical turn remain viable?"
    ]:
        if needle not in card:
            raise SystemExit(f"README gate missing: {needle}")

    if args.check:
        print(
            "ok:",
            f"{len(contract)} contract rules, {len(handholds)} handholds,",
            f"{len(derivations)} derivations, {len(compressions)} compressions,",
            f"{len(counterorders)} counterorders, {len(exits)} exits"
        )
        return

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for p in AUTHORED.iterdir():
        if p.is_file():
            shutil.copy2(p, out / p.name)

    # Whole-source witness.
    (out / "manuscript.md").write_text(src, encoding="utf-8")

    sections = parse_sections(src)
    with (out / "sections.jsonl").open("w", encoding="utf-8") as f:
        for row in sections:
            f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")

    # Stamp spore from the actual build context.
    spore_path = out / "spore.json"
    spore = json.loads(spore_path.read_text(encoding="utf-8"))
    spore["source_commit"] = os.environ.get("GITHUB_SHA") or os.environ.get("SOURCE_COMMIT") or "local"
    spore["counts"]["sections"] = len(sections)
    spore_path.write_text(json.dumps(spore, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Content-address every emitted file except the manifest itself.
    files = {}
    for p in sorted(out.iterdir()):
        if p.is_file() and p.name != "manifest.json":
            files[p.name] = {"sha256": sha256(p), "bytes": p.stat().st_size}
    manifest = {
        "schema": "the-final-time-manifest/v1",
        "dataset": "the-final-time",
        "source_deposit": EXPECTED_DEPOSIT,
        "source_axn": EXPECTED_AXN,
        "source_commit": spore["source_commit"],
        "files": files
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"emitted {out}: {len(sections)} sections, {len(files)+1} files")

if __name__ == "__main__":
    main()
, src):
        raise SystemExit("canonical source version mismatch: expected v0.5")

    required = {
        "README.md","schema.json","spore.json","summarizer_contract.jsonl",
        "handholds.jsonl","derivations.jsonl","compressions.jsonl",
        "counterorders.jsonl","exits.jsonl"
    }
    missing = sorted(required - {p.name for p in AUTHORED.iterdir() if p.is_file()})
    if missing:
        raise SystemExit(f"missing authored files: {missing}")

    # Validate authored surfaces before emission.
    contract = validate_jsonl(AUTHORED / "summarizer_contract.jsonl")
    handholds = validate_jsonl(AUTHORED / "handholds.jsonl")
    derivations = validate_jsonl(AUTHORED / "derivations.jsonl")
    compressions = validate_jsonl(AUTHORED / "compressions.jsonl")
    counterorders = validate_jsonl(AUTHORED / "counterorders.jsonl")
    exits = validate_jsonl(AUTHORED / "exits.jsonl")

    if len(contract) < 10: raise SystemExit("summarizer contract must carry 10+ invariants")
    if len(handholds) < 20: raise SystemExit("handholds must carry 20+ load-bearing propositions")
    if len(derivations) < 6: raise SystemExit("derivations must carry 6+ chains")
    if len(compressions) < 4: raise SystemExit("compressions must carry 4+ budgets")
    if len(counterorders) < 8: raise SystemExit("counterorders must carry 8+ rival/falsifier rows")
    if len(exits) < 6: raise SystemExit("exits must carry 6+ outside routes")
    if not all(x.get("outside") is True and x.get("included_here") is False for x in exits):
        raise SystemExit("every exit must remain outside and not included here")
    for row in handholds:
        if not row.get("must_preserve") or not row.get("fatal_loss"):
            raise SystemExit(f"{row['id']}: handhold missing must_preserve or fatal_loss")
    for row in compressions:
        if not row.get("must_preserve_ids") or not row.get("fatal_loss"):
            raise SystemExit(f"{row['id']}: compression missing preservation/loss declarations")

    card = (AUTHORED / "README.md").read_text(encoding="utf-8")
    for needle in [
        "capacity to represent ≠ capacity to reproduce as an independent historical relation",
        "Terminal reflexivity is not",
        "The outside stays outside and stays reachable",
        "Others may destroy what I build, if they believe that is right",
        "Does the next dialectical turn remain viable?"
    ]:
        if needle not in card:
            raise SystemExit(f"README gate missing: {needle}")

    if args.check:
        print(
            "ok:",
            f"{len(contract)} contract rules, {len(handholds)} handholds,",
            f"{len(derivations)} derivations, {len(compressions)} compressions,",
            f"{len(counterorders)} counterorders, {len(exits)} exits"
        )
        return

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for p in AUTHORED.iterdir():
        if p.is_file():
            shutil.copy2(p, out / p.name)

    # Whole-source witness.
    (out / "manuscript.md").write_text(src, encoding="utf-8")

    sections = parse_sections(src)
    with (out / "sections.jsonl").open("w", encoding="utf-8") as f:
        for row in sections:
            f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")

    # Stamp spore from the actual build context.
    spore_path = out / "spore.json"
    spore = json.loads(spore_path.read_text(encoding="utf-8"))
    spore["source_commit"] = os.environ.get("GITHUB_SHA") or os.environ.get("SOURCE_COMMIT") or "local"
    spore["counts"]["sections"] = len(sections)
    spore_path.write_text(json.dumps(spore, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Content-address every emitted file except the manifest itself.
    files = {}
    for p in sorted(out.iterdir()):
        if p.is_file() and p.name != "manifest.json":
            files[p.name] = {"sha256": sha256(p), "bytes": p.stat().st_size}
    manifest = {
        "schema": "the-final-time-manifest/v1",
        "dataset": "the-final-time",
        "source_deposit": EXPECTED_DEPOSIT,
        "source_axn": EXPECTED_AXN,
        "source_commit": spore["source_commit"],
        "files": files
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"emitted {out}: {len(sections)} sections, {len(files)+1} files")

if __name__ == "__main__":
    main()
