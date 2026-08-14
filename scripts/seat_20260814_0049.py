#!/usr/bin/env python3
"""seat_20260814_0049.py — 17 captures, and the first measured frame/paste divergence.

THE FINDING THIS SITTING PRODUCED. The operator reported that some answers
"literally force regenerated in the three minutes between grabbing the screenshot
and copying the transcripts." That is measurable, and it was measured: the visible
answer text was OCR'd from each frame and compared against the pasted opening.

    12 of 17  IDENTICAL — frame and paste are the same composition
     5 of 17  DIVERGENT — the layer regenerated between them

The sharpest is «johannes aigil», where the two generations offer ENTIRELY
DIFFERENT disambiguation branches: the frame proposes genealogical records for a
"Johannes Aigle", the paste proposes an agile work concept and the classical
philologist Johannes Ilberg. Neither alternative appears in the other.

WHY THIS MATTERS TO EVERY PRIOR RECORD. This corpus has always treated the frame
and the paste as two views of ONE observation — the ruling applied to the
counter-infrastructure pair earlier in this session says so explicitly. That
assumption is now falsified for at least 29% of one sitting. The frame
establishes SURFACE; the paste establishes TEXT; and where they diverge they are
two observations minutes apart that happen to share a query.

So every capture in this registry carries an unmeasured divergence risk, and the
frames are not decoration — they are the only evidence of what the surface said
at the moment it was photographed. Recorded per observation as
`frame_paste_divergence`, with the frame text preserved where it differs.
"""
import json, pathlib, re, shutil, hashlib, sys, datetime
sys.path.insert(0, "/tmp/r5")
sys.path.insert(0, "/tmp")
from div import D, IDENTICAL
from opens import O

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJ = ROOT / "data/EA-WG-CAPTURES-01.json"
SRC = pathlib.Path("/mnt/user-data/uploads")
DATE, SIT = "2026-08-14", "20260814-0049"
PAIRS = dict(l.split("|", 1) for l in pathlib.Path("/tmp/pairs.txt").read_text().split("\n") if l.strip())
TS = {q: t for t, q in PAIRS.items()}


def slug(q):
    return re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")[:56].strip("-") + "-" + SIT


def main():
    proj = json.loads(PROJ.read_text())
    by = {e.get("q"): e for e in proj["entries"]}
    n = 0
    for q, opening in O.items():
        e = by[q]
        sl = slug(q)
        fn = f"screengrab-20260814-{TS[q]}.png"
        d = ROOT / "data/captures" / sl
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy(SRC / fn, d / fn)
        rel = f"data/captures/{sl}/{fn}"
        dv = D.get(q)
        row = {
            "slug": sl, "date": DATE, "surface": "Google AI Overview",
            "auth": "signed in", "ev": "paste + frame",
            "mt": "CAPTURE", "q": q, "s": e.get("s"), "addr_id": e.get("addr_id"),
            "obs_id": "OBS-" + hashlib.sha256((q + SIT).encode()).hexdigest()[:12],
            "imgs": [rel], "img_urls": ["https://www.alexanarch.org/" + rel],
            "transcript": None,  # seated from the operator's paste in a following pass
            "transcript_class": "CAPTURE-TIME VERBATIM RECORD — raw paste, cleaned at intake",
            "surface_basis": "Google AI Overview — collapsed popup in frame, All tab active.",
            "auth_basis": "OPERATOR ATTESTATION 2026-08-14: signed in, not incognito.",
            "frame_paste_divergence": {
                "measured": True, "method": ("frame OCR'd and compared against the pasted opening; "
                                             "difflib ratio on normalised text"),
                "gap": "~3 minutes between screenshot and copy",
                "verdict": dv["verdict"] if dv else "IDENTICAL",
                "similarity": dv["ratio"] if dv else 1.0,
                "frame_text": dv["frame"] if dv else None,
                "note": dv["note"] if dv else None,
                "_rule": ("Where the verdict is DIVERGENT the frame and the paste are TWO COMPOSITIONS, not two "
                          "views of one. The frame establishes SURFACE; the paste establishes TEXT; PER and the "
                          "citation list score the PASTE, and the frame text is preserved here so the difference "
                          "stays answerable.")},
        }
        e.setdefault("observations", [{k: v for k, v in e.items()
                                       if k not in ("observations", "n_observations", "dates", "surfaces",
                                                    "other_slugs", "links", "cite", "d_full", "d_truncated",
                                                    "rerun_alt", "transcript_raw", "sf", "sf_derived")}])
        e["observations"].append(row)
        e["n_observations"] = len(e["observations"])
        e["dates"] = sorted({o["date"] for o in e["observations"] if o.get("date")})
        e["surfaces"] = sorted({o["surface"] for o in e["observations"] if o.get("surface")})
        e["series"] = len(e["observations"])
        if not e.get("imgs"):
            e["imgs"], e["img_urls"] = row["imgs"], row["img_urls"]
        n += 1
    proj["_regeneration_finding"] = {
        "sitting": "2026-08-14 00:49, signed in, not incognito, 17 addresses",
        "measured": "12 of 17 identical, 5 of 17 DIVERGENT across a ~3 minute gap",
        "rate": round(5 / 17, 3),
        "sharpest": ("«johannes aigil» — the frame proposes genealogical records for a 'Johannes Aigle', the paste "
                     "proposes an agile work concept and the philologist Johannes Ilberg. Neither alternative "
                     "appears in the other."),
        "consequence": ("The corpus has always treated frame and paste as two views of ONE observation. That is "
                        "falsified for 29% of this sitting. Every prior capture carries an unmeasured divergence "
                        "risk, and no earlier record can be retroactively resolved — the frames were kept, the "
                        "second generation was not."),
        "measured_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    proj["version"] = "10.6"
    proj["date"] = DATE
    proj["address_count"] = proj["total_captures"] = len(proj["entries"])
    proj["observation_count"] = sum(len(x.get("observations") or [x]) for x in proj["entries"])
    PROJ.write_text(json.dumps(proj, indent=1, ensure_ascii=False))
    print(f"seated {n} observations | divergent {len(D)} | identical {len(IDENTICAL)}")
    print(f"entries {proj['address_count']} | observations {proj['observation_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
