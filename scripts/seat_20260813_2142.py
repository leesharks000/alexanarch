#!/usr/bin/env python3
"""seat_20260813_2142.py — the 21:42 batch: 7 captures, 7 images, all AI Overview.

SIX RECAPTURES, ONE NEW ADDRESS. «"ChatGPT Psychosis: A Love Story"» is new: the
UNQUOTED form stopped returning the work, so the operator ran it quoted. Quoted
and unquoted are different addresses, so the July Google Scholar capture at the
unquoted string stands as its own record and the pair measures the change.

AUTH: SIGNED IN, NOT INCOGNITO — operator attestation, 2026-08-13. Seated first
as UNATTESTED rather than assumed from the 18:57 sitting, then set on the
operator's word. The frames corroborate the authentication dimension: no Sign in
pill in any of the seven, and a partial account-avatar ring at the header edge.
They cannot corroborate the incognito dimension — no frame can — so that half
rests on the attestation alone. Two dimensions, two bases.
"""
import json, pathlib, re, shutil, hashlib, sys
sys.path.insert(0, "/tmp/r3")
from a import R

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJ = ROOT / "data/EA-WG-CAPTURES-01.json"
SRC = pathlib.Path("/mnt/user-data/uploads")
DATE, SIT = "2026-08-13", "20260813-2142"


def slug(q):
    return re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")[:56].strip("-") + "-" + SIT


def main():
    proj = json.loads(PROJ.read_text())
    by_q = {e.get("q"): e for e in proj["entries"]}
    new = app = 0
    for q, c in R.items():
        sl = slug(q)
        fn = f"screengrab-20260813-{c['img']}.png"
        d = ROOT / "data/captures" / sl
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy(SRC / fn, d / fn)
        rel = f"data/captures/{sl}/{fn}"
        au, inst, idr, src, sc = c["per"]
        row = {
            "slug": sl, "date": DATE, "surface": "Google AI Overview",
            "auth": "UNATTESTED", "ev": "paste",
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
            "q": q, "s": c["s"],
            "obs_id": "OBS-" + hashlib.sha256((q + SIT).encode()).hexdigest()[:12],
            "q_kind": None, "series": None,
            "img_urls": ["https://www.alexanarch.org/" + rel],
            "surface_basis": "Google AI Overview — collapsed popup in frame, All tab active.",
            "auth_basis": ("NOT ATTESTED. No Sign in pill in any of the seven frames of this sitting and a partial "
                           "account-avatar ring at the header edge; both consistent with signed in, neither "
                           "sufficient. Auth is never inferred — awaiting operator statement."),
        }
        e = by_q.get(q)
        if e:
            row["addr_id"] = e.get("addr_id")
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
            app += 1
        else:
            row["addr_id"] = "ADDR-" + hashlib.sha256(q.encode()).hexdigest()[:12]
            e = dict(row)
            e["observations"] = [dict(row)]
            e["n_observations"] = 1
            e["dates"] = [DATE]
            e["surfaces"] = ["Google AI Overview"]
            e["other_slugs"] = None
            e["links"] = [{"url": f"https://www.alexanarch.org/captures/#{sl}", "authority": "canonical",
                           "note": "the archive holds the registry and the images; citations resolve here"}]
            e["cite"] = f"https://www.alexanarch.org/captures/#{sl}"
            e["d_full"] = row["d"]; e["d_truncated"] = len(row["d"]) > 240
            e["rerun_alt"] = {"q": q.strip('"'), "label": "unquoted",
                              "why": ("This address was captured QUOTED, after the UNQUOTED form stopped returning "
                                      "the work. Running it unquoted tests whether that is still true.")}
            e["transcript_raw"] = None
            proj["entries"].append(e); by_q[q] = e; new += 1
    proj["entries"].sort(key=lambda x: re.sub(r"^[^0-9A-Za-z]+", "", str(x.get("q") or "")).lower())
    proj["version"] = "10.3"; proj["date"] = DATE
    proj["address_count"] = proj["total_captures"] = len(proj["entries"])
    proj["observation_count"] = sum(len(x.get("observations") or [x]) for x in proj["entries"])
    PROJ.write_text(json.dumps(proj, indent=1, ensure_ascii=False))
    print(f"new addresses {new} | appended {app}")
    print(f"entries {proj['address_count']} | observations {proj['observation_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
