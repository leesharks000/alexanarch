#!/usr/bin/env python3
"""seat_20260813_rerun.py — the 18:57 rerun batch: 17 captures, 19 images.

WHY THESE ADDRESSES. Every one had NO IMAGE. Sixteen of the seventeen carried the
`Google AI Mode (native)` label, which no image in the corpus ever established.
Recaptured with frames, they are confirmed Overview popups — the retraction is
now corroborated by evidence rather than by attestation alone.

AUTH. Signed in, NOT incognito: Google has disabled AI Overview in incognito, so
the authentication-controlled pair is no longer obtainable on this surface.

SURFACE. Overview for sixteen. `"broke Marxist poet"` is AI Mode native, and for
the first time the determination rests on the FRAME: the AI Mode tab is SELECTED
in the tab strip. An expanded Overview adopts AI Mode chrome but does not select
that tab. This is the discriminator the corpus lacked.
"""
import json, pathlib, re, hashlib, sys
sys.path.insert(0, "/tmp/r2")
from authored import R

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJ = ROOT / "data/EA-WG-CAPTURES-01.json"
DATE, SITTING = "2026-08-13", "20260813-1857"
PLACED = json.loads(pathlib.Path("/tmp/placed.json").read_text())


def slug(q):
    return re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")[:56].strip("-") + "-" + SITTING


def cites(rows):
    return [{"n": i, "site": s, "rel": rel, "title": t, "snip": sn, "url": None, "note": nt}
            for i, (s, rel, t, d, sn, nt) in enumerate(rows, 1)] or None


def main():
    proj = json.loads(PROJ.read_text())
    by_q = {e.get("q"): e for e in proj["entries"]}
    seated = missing = 0
    for q, c in R.items():
        e = by_q.get(q)
        if not e:
            print("NO EXISTING ENTRY for", repr(q)); missing += 1; continue
        sl = slug(q)
        imgs = PLACED[q]
        a, i_, id_, src, sc = c["per"]
        row = {
            "slug": sl, "date": DATE, "surface": c.get("surface", "Google AI Overview"),
            "auth": "signed in", "ev": "paste",
            "cites": len(c["cites"]) or None, "per": sc,
            "per_v": {"author": a, "inst": i_, "id": id_, "src": src},
            "mt": "CAPTURE", "d": c["d"], "reading": None, "analysis": c["an"],
            "transcript": c["tr"],
            "transcript_class": "CAPTURE-TIME VERBATIM RECORD — raw paste, cleaned at intake with a formal wrapper granted",
            "transcript_complete": ("COMPLETE — the collapsed Overview was expanded and the whole answer copied; the "
                                    "citation card row is a sideways scroller and is captured as data, not in frame"),
            "transcript_read": "READ IN FULL 2026-08-13",
            "cite_list": cites(c["cites"]), "collisions": None, "oq": None,
            "imgs": imgs, "defects": None, "rounds": None,
            "rerun": "https://www.google.com/search?q=" + q.replace(" ", "+"),
            "q": q, "s": c["s"],
            "addr_id": e.get("addr_id"),
            "obs_id": "OBS-" + hashlib.sha256((q + SITTING).encode()).hexdigest()[:12],
            "q_kind": None, "series": None,
            "img_urls": ["https://www.alexanarch.org/" + p for p in imgs],
            "surface_basis": ("AI Mode native — THE AI MODE TAB IS SELECTED IN THE FRAME. An expanded Overview adopts "
                              "AI Mode chrome without selecting that tab; this is the first determination in the corpus "
                              "to rest on the frame rather than on a paste marker."
                              if c.get("surface") else
                              "Google AI Overview — collapsed popup in frame, All tab active."),
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
        # DISPLAY IMAGE INHERITED FROM THE ADDRESS. These entries had none; the
        # rerun is the whole point, so the newest imaged observation supplies it.
        e["imgs"], e["img_urls"] = row["imgs"], row["img_urls"]
        seated += 1
    proj["version"] = "10.2"
    proj["date"] = DATE
    proj["observation_count"] = sum(len(e.get("observations") or [e]) for e in proj["entries"])
    proj["address_count"] = proj["total_captures"] = len(proj["entries"])
    PROJ.write_text(json.dumps(proj, indent=1, ensure_ascii=False))
    print(f"seated {seated} observations onto existing addresses | no entry found: {missing}")
    print(f"entries {proj['address_count']} | observations {proj['observation_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
