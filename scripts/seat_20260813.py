#!/usr/bin/env python3
"""seat_20260813.py — seat the 2026-08-13 batch into the published projection.

Shape taken from an existing entry, field for field: `axn-distributed-identifiers-20260811`.
Nothing invented, nothing renamed, no new machinery.

  IMAGES live at data/captures/{slug}/{file}. Committed at the repository root
  they resolve nowhere: image_urls() in build_capture_gallery.py maps repo-relative
  data/ paths to alexanarch.org and BARE FILENAMES to the leesharks host, where a
  root-level file 404s. That is why none of them displayed.

  SIX ARE RECAPTURES of addresses already in the registry. They append to that
  entry's `observations` and do not mint a second card — quoted and unquoted stay
  distinct, but the same exact string is one address.
"""
import json, pathlib, re, shutil, hashlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJ = ROOT / "data/EA-WG-CAPTURES-01.json"
INTAKE = pathlib.Path("/tmp/intake")
DATE = "2026-08-13"

SECTION = {
    "lee sharks the network is the porm": "Frameworks", "stable visionary loci": "Frameworks",
    '"endogenous" sophon alexanarch': "Frameworks", "alexanarch": "Sites",
    '"semantic samizdat"': "Frameworks", "semantic economy": "Frameworks",
    "alexanarch records": "Sites", '"the network is the poem"': "Frameworks",
    '"epic without hero"': "Frameworks", '"10,000 macarthur genius grants"': "People",
    "who is lee sharks?": "People", "alexanarch surface weather observatory": "Sites",
    '"operative semiotics"': "Frameworks", "alexanarch:omega": "Sites",
    "alexanarch:boats": "Sites",
    "alexanarch as a counter infrastructure semantic prefix to any search": "Sites",
    "alexanarch:revelation": "Frameworks", "alexanarch:classics": "Frameworks",
    "alexanarch:datasets": "Sites", '"ai overview capture registry"': "Projects",
}


def slugify(q):
    return re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")[:64].strip("-") + "-" + DATE.replace("-", "")


def per_v(c):
    p = c["per_v"]
    return {"author": p["author"], "inst": p["institution"], "id": p["identifier"], "src": p["own_source"]}


def cite_list(c):
    return [{"n": x["n"], "site": x["site"], "rel": x["rel"], "title": x.get("title"),
             "snip": x.get("snip"), "url": x.get("url"), "note": x.get("note")}
            for x in c["cite_list"]] or None


def rerun(q):
    from urllib.parse import quote_plus
    return "https://www.google.com/search?q=" + quote_plus(q)


def rerun_alt(q):
    quoted = q.startswith('"') and q.endswith('"')
    return {"q": (q[1:-1] if quoted else '"%s"' % q),
            "label": "unquoted" if quoted else "exact match",
            "why": ("This address was captured QUOTED. Running it unquoted tests the same string "
                    "against the broad basin." if quoted else
                    "This address was captured UNQUOTED. Running it quoted tests the same string "
                    "against the exact-phrase basin.")}


def row(c, slug, img_rel):
    d = c["finding"]
    return {
        "slug": slug, "date": DATE, "surface": "Google AI Overview",
        "auth": "incognito, signed out", "ev": "paste",
        "cites": c["cites"] or None, "per": c["per_v"]["scalar"], "per_v": per_v(c),
        "mt": "CAPTURE", "d": d, "reading": None, "analysis": c["analysis"],
        "transcript": c["transcript"],
        "transcript_class": "CAPTURE-TIME VERBATIM RECORD — raw paste, cleaned at intake with a formal wrapper granted",
        "transcript_complete": ("COMPLETE — the collapsed Overview was expanded and the whole answer copied; "
                                "the citation card row is a sideways scroller and is captured as data, not in frame"),
        "transcript_read": "READ IN FULL 2026-08-13",
        "cite_list": cite_list(c),
        "collisions": None, "oq": None,
        "imgs": [img_rel], "defects": (["citations-null"] if not c["cites"] else None),
        "rounds": None, "rerun": rerun(c["q"]), "q": c["q"], "s": SECTION[c["q"]],
        "addr_id": "ADDR-" + hashlib.sha256(c["q"].encode()).hexdigest()[:12],
        "obs_id": "OBS-" + hashlib.sha256((c["q"] + DATE).encode()).hexdigest()[:12],
        "q_kind": None, "series": None,
        "img_urls": ["https://www.alexanarch.org/" + img_rel],
    }


def main():
    proj = json.loads(PROJ.read_text())
    by_q = {e.get("q"): e for e in proj["entries"]}
    new, appended = 0, 0
    for f in sorted(INTAKE.glob("capture-*.json")):
        c = json.loads(f.read_text())
        q = c["q"]
        slug = slugify(q)
        fn = c["evidence"]["images"][0]["filename"]
        dest = ROOT / "data/captures" / slug
        dest.mkdir(parents=True, exist_ok=True)
        src = ROOT / fn
        if src.exists():
            shutil.move(str(src), str(dest / fn))
        img_rel = f"data/captures/{slug}/{fn}"
        r = row(c, slug, img_rel)

        if q in by_q:                                   # RECAPTURE — append, do not mint a card
            e = by_q[q]
            e.setdefault("observations", [dict({k: v for k, v in e.items()
                                                if k not in ("observations", "n_observations", "dates",
                                                             "surfaces", "other_slugs", "links", "cite",
                                                             "d_full", "d_truncated", "rerun_alt",
                                                             "transcript_raw")})])
            e["observations"].append(r)
            e["n_observations"] = len(e["observations"])
            e["dates"] = sorted({o["date"] for o in e["observations"] if o.get("date")})
            e["surfaces"] = sorted({o["surface"] for o in e["observations"] if o.get("surface")})
            e["other_slugs"] = [o["slug"] for o in e["observations"] if o["slug"] != e.get("slug")] or None
            e["series"] = len(e["observations"])
            if not e.get("imgs"):                        # display image inherited from the address
                e["imgs"], e["img_urls"] = r["imgs"], r["img_urls"]
            appended += 1
        else:
            e = dict(r)
            e["observations"] = [dict(r)]
            e["n_observations"] = 1
            e["dates"] = [DATE]
            e["surfaces"] = ["Google AI Overview"]
            e["other_slugs"] = None
            e["links"] = [{"url": f"https://www.alexanarch.org/captures/#{slug}",
                           "authority": "canonical",
                           "note": "the archive holds the registry and the images; citations resolve here"}]
            e["cite"] = f"https://www.alexanarch.org/captures/#{slug}"
            e["d_full"] = r["d"]
            e["d_truncated"] = bool(r["d"] and len(r["d"]) > 240)
            e["rerun_alt"] = rerun_alt(q)
            e["transcript_raw"] = None
            proj["entries"].append(e)
            by_q[q] = e
            new += 1

    proj["entries"].sort(key=lambda e: re.sub(r"^[^0-9A-Za-z]+", "", str(e.get("q") or "")).lower())
    proj["version"] = "10.1"
    proj["date"] = DATE
    proj["total_captures"] = len(proj["entries"])
    proj["address_count"] = len(proj["entries"])
    proj["observation_count"] = sum(len(e.get("observations") or [e]) for e in proj["entries"])
    PROJ.write_text(json.dumps(proj, indent=1, ensure_ascii=False))
    print(f"new entries {new} | observations appended to existing addresses {appended}")
    print(f"entries {proj['address_count']} | observations {proj['observation_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
