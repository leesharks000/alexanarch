#!/usr/bin/env python3
"""repair_intake_schema_20260813.py — seat the 2026-08-13 batch in the CORPUS's shape.

THE DEFECT THIS CLOSES
----------------------
I seated twenty captures in a schema of my own rather than the one 406 seated
observations already demonstrate. Reading five records would have shown it;
I read one, in the ninth round, and only to write a projector.

All twenty diverged on six fields, and three of the six degraded the render:

  auth_state       mine {authenticated, incognito}; the corpus keys it {value,
                   derivation, basis, ...} and the projector reads .value — so
                   twenty cards rendered with NO AUTH STATE, on a batch whose
                   whole auth story is "signed out, incognito".
  measurement_flags mine {per_score, per_v}; the corpus keys the four units
                   individually and the projector rebuilds per_v from them — so
                   twenty cards rendered per_v NULL despite an authored vector.
  classification.section  absent, so all twenty defaulted to "Captures" — the
                   same flattening that put a capture alone under "Archive".
  citations        mine {n, site, rel, snip}; the corpus uses {order,
                   site_label, relation, snippet} on 1,150 rows.
  legacy_slug      absent, so the slug lived only in the projection and would
                   move if the projector changed.
  record_history.interface_observation  absent. 244 of 406 carry a reading;
                   absence here is honest — none was authored — and is left.

Authored content is not touched. This is a shape repair: the same values, in
the keys the corpus uses.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CANON = ROOT / "rebuild/capture-registry/EA-WG-CAPTURES-01-REBUILD.json"

# Sections assigned per capture, from the content. Not defaulted.
SECTION = {
    "lee sharks the network is the porm": "Frameworks",
    "stable visionary loci": "Frameworks",
    '"endogenous" sophon alexanarch': "Frameworks",
    "alexanarch": "Sites",
    '"semantic samizdat"': "Frameworks",
    "semantic economy": "Semantic Economy",
    "alexanarch records": "Sites",
    '"the network is the poem"': "Frameworks",
    '"epic without hero"': "Frameworks",
    '"10,000 macarthur genius grants"': "Identity",
    "who is lee sharks?": "Identity",
    "alexanarch surface weather observatory": "Sites",
    '"operative semiotics"': "Frameworks",
    "alexanarch:omega": "Sites",
    "alexanarch:boats": "Sites",
    "alexanarch as a counter infrastructure semantic prefix to any search": "Sites",
    "alexanarch:revelation": "Revelation First",
    "alexanarch:classics": "Frameworks",
    "alexanarch:datasets": "Sites",
    '"ai overview capture registry"': "Projects",
}


def slugify(q, date):
    base = re.sub(r"[^a-z0-9]+", "-", str(q or "capture").lower()).strip("-")[:56].strip("-")
    return f"{base}-{str(date or '').replace('-', '')}"


def domain_of(site):
    s = str(site or "")
    m = re.search(r"([a-z0-9][a-z0-9\-]*\.(?:org|com|edu|net|io|dev|gov|co\.uk))", s, re.I)
    if m:
        return m.group(1).lower()
    return {"Medium·Lee Sharks": "medium.com", "Medium·Johannes Sigil": "medium.com",
            "Medium": "medium.com", "Zenodo": "zenodo.org", "zenodo.org": "zenodo.org",
            "Academia.edu": "academia.edu", "GitHub": "github.com", "Wikipedia": "wikipedia.org",
            "Reddit": "reddit.com", "SciLynk": "scilynk.com", "Amazon.com": "amazon.com",
            "YouTube": "youtube.com"}.get(s)


def repair(o, q):
    changed = []

    a = o.get("auth_state") or {}
    if "value" not in a:
        a = {"value": "incognito, signed out",
             "authenticated": a.get("authenticated", False),
             "incognito": a.get("incognito", True),
             "derivation": "OPERATOR ATTESTATION, 2026-08-13",
             "basis": ("stated by the operator for the whole sitting: signed out and incognito. "
                       "The Sign in pill is also present in every frame, which corroborates the "
                       "authentication dimension but cannot show the incognito one."),
             "signed_out_indicator_visible_in_image": True,
             "image_present": bool((o.get("evidence") or {}).get("images")),
             "_rule": "Authentication state is a SUBFIELD of the address, not part of it."}
        o["auth_state"] = a
        changed.append("auth_state")

    mf = o.get("measurement_flags") or {}
    pv = mf.get("per_v") or {}
    if "author_retained" not in mf and pv:
        o["measurement_flags"] = {
            "author_retained": pv.get("author"), "institution_retained": pv.get("institution"),
            "doi_retained": pv.get("identifier"), "composition_source_included": pv.get("own_source"),
            "per_score": pv.get("scalar"),
            "match_type": None,
            "_method": {"measured": "2026-08-13", "measured_by": "TACHYON",
                        "instrument": "authored at intake against the frame and the source strip"},
            "_note": pv.get("_note")}
        changed.append("measurement_flags")

    cs = o.get("citations_and_sources") or {}
    cits = cs.get("citations") or []
    if cits and "order" not in cits[0]:
        out = []
        for c in cits:
            out.append({"order": c.get("n"), "site_label": c.get("site"),
                        "domain": domain_of(c.get("site")), "relation": c.get("rel"),
                        "title": c.get("title"), "snippet": c.get("snip"),
                        "date": c.get("date_shown"), "url": c.get("url"), "note": c.get("note"),
                        "position": "card",
                        "source_of_record": "authored at intake, 2026-08-13",
                        "read_by": "TACHYON", "read_date": "2026-08-13"})
        cs["citations"] = out
        cs["citation_summary"] = {"total": len(out),
                                  "by_relation": {r: sum(1 for x in out if x["relation"] == r)
                                                  for r in sorted({x["relation"] for x in out if x["relation"]})},
                                  "method": "AUTHORED against the frame; extractor output was a proposal only"}
        o["citations_and_sources"] = cs
        changed.append("citations")

    cl = o.get("classification") or {}
    if not cl.get("section"):
        cl["section"] = [{"value": SECTION.get(q, "Captures"),
                          "source": "authored at intake", "version_date": "2026-08-13"}]
        cl["match_or_finding"] = [{"value": "CAPTURE", "source": "authored at intake",
                                   "version_date": "2026-08-13"}]
        o["classification"] = cl
        changed.append("section")

    if not o.get("legacy_slug"):
        o["legacy_slug"] = slugify(q, o.get("observed_on"))
        changed.append("legacy_slug")

    return changed


def main():
    reg = json.loads(CANON.read_text())
    n = 0
    tally = {}
    for a in reg["addresses"]:
        q = a["semantic_address"].get("q_as_issued")
        for o in a["observations"]:
            if o.get("observed_on") == "2026-08-13" and o.get("transcript_wrapper"):
                ch = repair(o, q)
                if ch:
                    n += 1
                    for c in ch:
                        tally[c] = tally.get(c, 0) + 1
    CANON.write_text(json.dumps(reg, indent=1, ensure_ascii=False))
    print(f"repaired {n} observations")
    for k, v in sorted(tally.items()):
        print(f"   {v:>3}  {k}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
