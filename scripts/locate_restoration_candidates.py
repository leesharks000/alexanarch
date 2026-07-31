#!/usr/bin/env python3
"""locate_restoration_candidates.py — propose, with evidence. Seat nothing.

WHY IT ONLY PROPOSES
--------------------
Every automated confidence failure in this archive has the same shape: a
matcher scored a resemblance, the score was trusted, and the assertion entered
the record. A fuzzy title match that seats the wrong text into a deposit is
worse than an empty deposit, because an empty deposit is visibly empty and a
wrong body is invisibly wrong.

So this reports candidate pairings with the evidence that produced them and
stops. A human rules. Nothing is written to the registry, and no body is
touched.

WHAT IT SEARCHES
----------------
The fleet working copies (the works' own repositories, which is where the
Secret Book of Walt was found on 2026-07-31 while its record served a 75-word
stub) plus any local mirror trees. Candidates are prose files large enough to
be the work.

USAGE
  python3 scripts/locate_restoration_candidates.py --roots /tmp/fleet
"""
import argparse
import json
import os
import re
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data" / "worklists" / "restoration-queue.json"
OUT = ROOT / "data" / "worklists" / "restoration-candidates.json"

SKIP_DIRS = {".git", "node_modules", "dist", "build", ".next", "assets", "vendor"}

# Paths the archive GENERATES from the registry. A stub-bodied record renders
# into all of them, so matching against them proposes restoring a record from a
# derivative of its own stub — a perfect title match carrying no new text. The
# first run of this script (2026-07-31) scored such self-matches at 1.0 and had
# to be discarded. Derived surfaces are excluded on principle, not by tuning.
SELF_DERIVED = (
    "/data/autonomous/", "/data/texts/", "/s/records/", "/s/wiki/", "/s/axn/",
    "/s/browse/", "/data/specs/archive/", "/papers/", "/data/external-metadata/",
)
EXT = {".md", ".txt", ".html", ".htm"}
MIN_WORDS = 350


def norm(s):
    s = re.sub(r"\(.*?\)", " ", str(s or ""))
    s = re.sub(r"\b(v\d+(\.\d+)*|EA-[A-Z0-9-]+|AXN:[^\s]+)\b", " ", s, flags=re.I)
    s = re.sub(r"[^a-z0-9 ]+", " ", s.lower())
    return " ".join(s.split())


def toks(s):
    return {w for w in norm(s).split() if len(w) > 3}


def prose_of(p):
    try:
        t = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None, None, None
    if p.suffix in {".html", ".htm"}:
        t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S | re.I)
        t = re.sub(r"<[^>]+>", " ", t)
    head = ""
    m = re.search(r"^#\s+(.+)$", t, re.M) or re.search(r"^(.{6,110})$", t.strip(), re.M)
    if m:
        head = m.group(1).strip()[:110]
    words = len(re.findall(r"[A-Za-z\u00C0-\u024F]{2,}", t))
    return t, head, words


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roots", nargs="+", default=["/tmp/fleet"])
    ap.add_argument("--min-score", type=float, default=0.34)
    a = ap.parse_args()

    q = json.loads(QUEUE.read_text())
    targets = [e for e in q["entries"] if e.get("issue") == "declared_full_body_is_stub"]

    files = []
    for r in a.roots:
        for dirpath, dirnames, filenames in os.walk(r):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                if Path(fn).suffix.lower() not in EXT:
                    continue
                p = Path(dirpath) / fn
                sp = "/" + str(p).replace(os.sep, "/").lstrip("/")
                if any(k in sp for k in SELF_DERIVED):
                    continue
                try:
                    if p.stat().st_size < 3000:
                        continue
                except OSError:
                    continue
                txt, head, words = prose_of(p)
                if not words or words < MIN_WORDS:
                    continue
                files.append({"path": str(p), "head": head, "words": words,
                              "htoks": toks(head), "ftoks": toks(p.stem)})
    print(f"candidate files scanned: {len(files)}")

    results = []
    for t in targets:
        tt = toks(t["title"])
        scored = []
        for f in files:
            # two independent signals: heading overlap and filename overlap,
            # plus a sequence ratio on the normalized strings
            ov_h = len(tt & f["htoks"]) / max(1, len(tt))
            ov_f = len(tt & f["ftoks"]) / max(1, len(tt))
            seq = SequenceMatcher(None, norm(t["title"])[:90],
                                  norm(f["head"])[:90]).ratio()
            score = max(ov_h, ov_f) * 0.7 + seq * 0.3
            # A restoration must bring substantially more text than the stub it
            # replaces. Equal-sized "matches" are renderings, not recoveries.
            if f["words"] < max(1200, (t.get("words") or 0) * 4):
                continue
            if score >= a.min_score:
                scored.append({"score": round(score, 3), "path": f["path"],
                               "candidate_heading": f["head"], "words": f["words"],
                               "title_token_overlap": round(ov_h, 2),
                               "filename_token_overlap": round(ov_f, 2),
                               "heading_sequence_ratio": round(seq, 2)})
        scored.sort(key=lambda x: -x["score"])
        results.append({
            "deposit_number": t["n"], "title": t["title"],
            "stub_words": t.get("words"), "status": "PROPOSED — awaiting MANUS ruling",
            "candidates": scored[:3],
        })

    matched = [r for r in results if r["candidates"]]
    OUT.write_text(json.dumps({
        "description": (
            "Proposed pairings between stub-bodied deposits and candidate source files "
            "located in the fleet working copies. Evidence is reported for each; nothing "
            "is seated. A pairing becomes a restoration only on explicit ruling."),
        "generated": "2026-07-31", "targets": len(targets),
        "with_candidates": len(matched), "entries": results,
    }, indent=1, ensure_ascii=False), encoding="utf-8")

    print(f"targets: {len(targets)} | with at least one candidate: {len(matched)}")
    print(f"\n{'#':>6} {'stub':>5}  {'score':>5} {'words':>6}  candidate")
    for r in sorted(matched, key=lambda x: -x["candidates"][0]["score"])[:20]:
        c = r["candidates"][0]
        print(f"  {r['deposit_number']:>4} {r['stub_words']:>5}w "
              f"{c['score']:>6} {c['words']:>6}w  {Path(c['path']).name[:40]}")
        print(f"         └ {r['title'][:64]}")
    print(f"\nwritten → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
