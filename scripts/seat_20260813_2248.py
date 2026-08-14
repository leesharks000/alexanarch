#!/usr/bin/env python3
"""seat_20260813_2248.py — the 22:48 batch: 13 captures, all AI Overview, signed in.

THIRTEEN RECAPTURES, ZERO NEW. Every address had NO IMAGE before this sitting.

«"executable scripture"» IS EXCLUDED at operator instruction. Its frame was
captured, but the transcript came back WITHOUT ITS SOURCES no matter how many
times the page was refreshed — a false positive rather than a citations-null
finding. An apparatus that did not render is not an apparatus that was absent.
NULL is not zero, and a capture that cannot be read is not seated.

AUTH: signed in, not incognito — operator attestation. Chosen deliberately for
comparison: AI Overview is AVAILABLE in incognito again as of this sitting, so
the state was elected rather than forced. That makes 2026-08-13 a four-sitting
day across two auth states with the switch demonstrably ON at both ends.
"""
import json, pathlib, re, shutil, hashlib, sys
sys.path.insert(0, "/tmp/r4")
from a import R

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJ = ROOT / "data/EA-WG-CAPTURES-01.json"
SRC = pathlib.Path("/mnt/user-data/uploads")
DATE, SIT = "2026-08-13", "20260813-2248"


def slug(q):
    return re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")[:56].strip("-") + "-" + SIT


def main():
    proj = json.loads(PROJ.read_text())
    by_q = {e.get("q"): e for e in proj["entries"]}
    n = miss = 0
    for q, c in R.items():
        e = by_q.get(q)
        if not e:
            print("NO ENTRY:", repr(q)); miss += 1; continue
        sl = slug(q)
        fn = f"screengrab-20260813-{c['img']}.png"
        d = ROOT / "data/captures" / sl; d.mkdir(parents=True, exist_ok=True)
        shutil.copy(SRC / fn, d / fn)
        rel = f"data/captures/{sl}/{fn}"
        au, inst, idr, src, sc = c["per"]
        row = {
            "slug": sl, "date": DATE, "surface": "Google AI Overview",
            "auth": "signed in", "ev": "paste",
            "cites": len(c["cites"]) or None, "per": sc,
            "per_v": {"author": au, "inst": inst, "id": idr, "src": src},
            "mt": "CAPTURE", "d": c["d"], "reading": None, "analysis": c["an"],
            "transcript": c["tr"],
            "transcript_class": "CAPTURE-TIME VERBATIM RECORD — raw paste, cleaned at intake with a formal wrapper granted",
            "transcript_complete": ("COMPLETE — the collapsed Overview was expanded and the whole answer copied; the "
                                    "citation card row is a sideways scroller and is captured as data, not in frame"),
            "transcript_read": "READ IN FULL 2026-08-13",
            "cite_list": [{"n": i, "site": s, "rel": r, "title": t, "snip": sn, "url": None, "note": nt}
                          for i, (s, r, t, dt, sn, nt) in enumerate(c["cites"], 1)] or None,
            "collisions": None, "oq": None, "imgs": [rel], "defects": None, "rounds": None,
            "rerun": "https://www.google.com/search?q=" + q.replace(" ", "+"),
            "q": q, "s": c["s"], "addr_id": e.get("addr_id"),
            "obs_id": "OBS-" + hashlib.sha256((q + SIT).encode()).hexdigest()[:12],
            "q_kind": None, "series": None,
            "img_urls": ["https://www.alexanarch.org/" + rel],
            "surface_basis": "Google AI Overview — collapsed popup in frame, All tab active.",
            "auth_basis": ("OPERATOR ATTESTATION: signed in, not incognito. ELECTED, not forced — AI Overview was "
                           "available in incognito at this sitting and the signed-in state was chosen for comparison."),
        }
        e.setdefault("observations", [{k: v for k, v in e.items()
                                       if k not in ("observations", "n_observations", "dates", "surfaces",
                                                    "other_slugs", "links", "cite", "d_full", "d_truncated",
                                                    "rerun_alt", "transcript_raw")}])
        e["observations"].append(row)
        e["n_observations"] = len(e["observations"])
        e["dates"] = sorted({o["date"] for o in e["observations"] if o.get("date")})
        e["surfaces"] = sorted({o["surface"] for o in e["observations"] if o.get("surface")})
        e["other_slugs"] = [o["slug"] for o in e["observations"] if o.get("slug") and o["slug"] != e.get("slug")] or None
        e["series"] = len(e["observations"])
        if not e.get("imgs"):
            e["imgs"], e["img_urls"] = row["imgs"], row["img_urls"]
        n += 1
    proj["version"] = "10.4"; proj["date"] = DATE
    proj["address_count"] = proj["total_captures"] = len(proj["entries"])
    proj["observation_count"] = sum(len(x.get("observations") or [x]) for x in proj["entries"])
    proj["_excluded_20260813_2248"] = {
        "q": '"executable scripture"',
        "reason": ("Frame captured; transcript returned WITHOUT ITS SOURCES across repeated refreshes. A false "
                   "positive, not a citations-null observation. Not seated: a capture that cannot be read is an "
                   "assertion, and an apparatus that failed to render is not an apparatus that was absent.")}
    PROJ.write_text(json.dumps(proj, indent=1, ensure_ascii=False))
    print(f"seated {n} | no entry {miss}")
    print(f"entries {proj['address_count']} | observations {proj['observation_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
