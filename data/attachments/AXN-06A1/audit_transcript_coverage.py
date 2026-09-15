#!/usr/bin/env python3
"""audit_transcript_coverage.py — every citable unit of the Capture Registry must carry its machine text.

THE RULE (operator, 2026-09-09): the transcript IS the capture. "without the transcript / evidence, do
you have a capture? you do not." A unit that is citable and has no transcript advertises evidence it
cannot produce. Intake has refused thin drafts since the contract; nothing checked the units seated
BEFORE it, so the gaps were invisible unless someone ran an audit by hand. This is that audit, run as a
gate: --check fails on any unit without a transcript that is not on the declared legacy list.

Legacy list: units seated before the transcript rule was enforced, enumerated here so the count can only
go down and each one is visible. Removing a slug from the list without supplying its transcript will fail
the gate; that is the point.
"""
import json, sys, argparse, pathlib, collections, statistics

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "data" / "EA-WG-CAPTURES-01.json"

# Seated before the transcript rule was enforced at intake (2026-06-17 to 2026-08-08), plus one stub.
# Each is a unit the registry can cite and cannot evidence. They are listed, not hidden.
LEGACY = {
    "maryleelabor-org-zero-index", "lee-sharks-entity-resolution-mary-lee", "lee-sharks-full-profile-adoption",
    "lee-sharks-heteronyms-dodecad-adoption", "lee-sharks-poet-vs-sharkey", "indexed-perfective-academia-laundering-20260627",
    "mary-lee-canonical-referent-inversion-20260627", "maryleelabor-overview-composition-20260627",
    "negentropic-kernel-archive-walled-site-20260630", "johannes-sigil-first-ai-overview-typo-resolution",
    "lee-sharks-bing-copilot-biography-20260711", "zenodo-doi-severance-cha-canonical-case",
    "chatgpt-psychosis-trilogy-scholar", "lee-sharks-pearl-multiturn-arc", "scilynk-archon-v30-aggregator-render-20260718",
    "parable-of-mary-lee-genre-competence-20260718", "schops-thiel-authorship-conflict-composition-20260731",
    "semantic-strike-directed-recovery-20260808",
    "cha-chatgpt-unprimed-three-turns-no-decay-hf-led-20260908-obs1",
}

def units(reg):
    for e in reg["entries"]:
        yield ("entry", e["slug"], e.get("date"), e.get("surface"), e.get("transcript"))
        for o in (e.get("observations") or []):
            if isinstance(o, dict):
                yield ("obs", o.get("slug") or e["slug"], o.get("date"), o.get("surface") or e.get("surface"), o.get("transcript"))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--check", action="store_true"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    reg = json.load(open(REG, encoding="utf-8"))
    us = list(units(reg))
    have = [u for u in us if u[4]]; none = [u for u in us if not u[4]]
    unlisted = [u for u in none if u[1] not in LEGACY]
    stale = sorted(LEGACY - {u[1] for u in none})   # a legacy slug that now HAS its transcript
    w = [len(u[4].split()) for u in have]
    report = {
        "units": len(us), "with_transcript": len(have), "without": len(none), "legacy_declared": len(LEGACY),
        "unlisted_without_transcript": [{"kind": u[0], "slug": u[1], "date": u[2], "surface": u[3]} for u in unlisted],
        "legacy_now_supplied": stale,
        "words": {"median": int(statistics.median(w)), "mean": int(sum(w) / len(w)), "min": min(w), "max": max(w), "total": sum(w)},
        "without_by_month": dict(sorted(collections.Counter((u[2] or "")[:7] for u in none).items())),
        "coverage": round(len(have) / len(us), 4),
    }
    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        print(f"transcript coverage: {len(have)}/{len(us)} units ({report['coverage']:.2%}) · "
              f"{report['words']['total']:,} words · median {report['words']['median']} · max {report['words']['max']}")
        print(f"  without transcript: {len(none)} — {len(LEGACY)} declared legacy, {len(unlisted)} unlisted")
        for u in unlisted:
            print(f"  FAIL  {u[2]} {u[0]:5s} {u[1]} ({u[3]}) — citable with no machine text", file=sys.stderr)
        if stale:
            print(f"  note: {len(stale)} legacy slug(s) now carry a transcript and can be removed from LEGACY: {', '.join(stale)}")
    if a.check and unlisted:
        print("\nThe transcript IS the capture. A citable unit without one advertises evidence it cannot produce.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
