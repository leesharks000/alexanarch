#!/usr/bin/env python3
"""Playback index: which records carry an AI-playback recording, and which current records do not.

    python3 scripts/build_playback_index.py [--since 2026-11-01]

Writes data/api/playbacks.json. Read from data/registry.json only: nothing is inferred.
- "with": every record whose registry entry carries playback[], with the audio's public URL, so that the recordings can
  be embedded on other surfaces (fleet sites, the dataset projections) by URL and SHA-256.
- "without": current records (the latest version of each version series) dated on or after --since that carry none.
"""
import argparse, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "https://www.alexanarch.org"
ap = argparse.ArgumentParser(); ap.add_argument("--since", default="2026-11-01"); a = ap.parse_args()
R = json.load(open(ROOT / "data/registry.json"))["deposits"]

superseded = {str(d["previous_version"]).lstrip("#") for d in R if d.get("previous_version")}
series_latest = {}
for d in R:
    s = d.get("version_series_id")
    if s and (s not in series_latest or int(d["deposit_number"]) > int(series_latest[s]["deposit_number"])):
        series_latest[s] = d


def current(d):
    s = d.get("version_series_id")
    if s: return series_latest[s] is d
    return str(d["deposit_number"]) not in superseded


def row(d):
    return {"n": int(d["deposit_number"]), "axn": d.get("axn"), "title": d.get("title"), "date": d.get("date"),
            "version": d.get("version"), "creator": d.get("creator"), "record": f"{BASE}/s/records/{d['deposit_number']}/"}


with_, without = [], []
for d in sorted(R, key=lambda x: int(x["deposit_number"])):
    pb = d.get("playback")
    if pb:
        r = row(d); r["playbacks"] = [{"url": BASE + p["file"], "recorded": p.get("recorded"), "duration_s": p.get("duration_s"),
                                       "sha256": p.get("sha256"), "source": p.get("source"), "label": p.get("label")} for p in pb]
        r["current"] = current(d); with_.append(r)
    elif current(d) and str(d.get("date", "")) >= a.since:
        without.append(row(d))

out = {"generated_from": "data/registry.json", "since": a.since,
       "note": "AI playback recordings attached to record pages (scripts/attach_playback.py). 'with' lists every record carrying one, with the audio URL and SHA-256 for embedding elsewhere; 'without' lists current records (latest in their version series) dated on or after 'since' that carry none.",
       "counts": {"with": len(with_), "without": len(without)}, "with": with_, "without": without}
(ROOT / "data/api/playbacks.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
print(out["counts"])
for r in without: print("  without", r["n"], r["date"], (r["title"] or "")[:80])
