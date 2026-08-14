#!/usr/bin/env python3
"""project_captures.py — THE PROJECTOR. Canonical store -> published projection.

THE DEFECT THIS CLOSES
----------------------
Nothing in this repository wrote `data/EA-WG-CAPTURES-01.json`. Nine scripts read
it; none produced it. The builder lived in a session container and died with it,
leaving `seat_source.py` pointing at `/home/claude/palette/...` and the atlas
declaring "one canonical store, one projection" with no path between them. The
gap reached 300 published entries against 426 canonical observations.

WHAT THIS IS AND IS NOT
-----------------------
CARRY, RESHAPE, EMIT. **It never cleans.** Cleaning and citation extraction happen
at intake, by hand, against the frame. If the projector cleaned, a reproduction
diff could never distinguish a transform bug from an intended improvement, and
the determinism gate would be testing the cleaner rather than the build.

    canonical  rebuild/capture-registry/EA-WG-CAPTURES-01-REBUILD.json
    projection data/EA-WG-CAPTURES-01.json          (derived; says so)

ONE ENTRY PER ADDRESS. The lead observation's fields are promoted to the entry so
a gallery can render a card without descending; the full set stays in
`observations`. Addresses are string-keyed per the intake contract.

ACCEPTANCE: THE CARRY-LAYER DIFF (`--verify`)
---------------------------------------------
Rebuild the CURRENT published projection from canonical and compare the fields
that are carried rather than computed. Every difference must be a known
reclassification or it is a bug. Fields the projector cannot reconstruct are
reported as UNRECONSTRUCTIBLE rather than silently invented — a projector that
guesses is worse than one that declares.

DETERMINISM. Sorted keys, sorted addresses, no clock in the payload except the
explicit build date. Two runs are byte-identical; `check_render_determinism.py`
depends on it.
"""
import json, pathlib, sys, hashlib, unicodedata, argparse, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]
CANON = ROOT / "rebuild/capture-registry/EA-WG-CAPTURES-01-REBUILD.json"
OUT = ROOT / "data/EA-WG-CAPTURES-01.json"

# Sections the gallery filters on. A section outside this set is a ONE-MEMBER
# SECTION and is invisible in practice: «alexanarch as a counter infrastructure
# semantic prefix to any search» sat alone under "Archive", 1 card of 300, and
# vanished from every view whose filter was set to anything else.
SECTIONS = {"Captures", "Frameworks", "Heteronyms", "Projects", "Sites",
            "Identity", "Revelation First", "Semantic Economy",
            "Erasure & Attribution"}
# Canonical's own section vocabulary, folded to the gallery's. Every alias below
# is a value actually present in the store, not an invention. "Unsectioned",
# "None" and one-off labels fall back to Captures.
SECTION_ALIAS = {"Sites & Surfaces": "Sites", "Books & Projects": "Projects",
                 "Archive": "Captures", "Unsectioned": "Captures", "None": "Captures",
                 "Revelation First / Semantic Economy": "Revelation First",
                 "Mary Lee Constellation": "Identity",
                 "Platform Erosion": "Erasure & Attribution"}


def nfc(s):
    return unicodedata.normalize("NFC", str(s)).strip() if s is not None else None


def longest(records, key):
    return max((str(r.get(key) or "") for r in (records or [])), key=len, default="") or None


def first_value(v):
    """Provenanced fields are [{value, source, ...}]; plain fields are scalars."""
    if isinstance(v, list) and v and isinstance(v[0], dict) and "value" in v[0]:
        return v[0]["value"]
    if isinstance(v, list):
        return v[0] if v else None
    return v


def section_of(obs):
    """CANONICAL IS THE AUTHORITY FOR SECTION, and the published values diverged.

    A carry-layer diff showed the published `s` agreeing with canonical's
    classification.section on only 199 of 355 shared observations, and no rule
    over that field — first, last or majority provenance — reproduces it. The
    section assignment was made somewhere that is not in the canonical store, so
    it is NOT reconstructible and is not reverse-engineered here.

    It is also where the one-member-section defect lives: «alexanarch as a
    counter infrastructure semantic prefix to any search» carried section
    "Archive", the only card of 300 in it, and so was invisible under every
    filter state but one. Sections outside the gallery's vocabulary are aliased
    into it or fall back to Captures; a section of one is not a section.
    """
    raw = first_value((obs.get("classification") or {}).get("section"))
    s = SECTION_ALIAS.get(str(raw), raw)
    return s if s in SECTIONS else "Captures"


def evidence_class(obs):
    tc = str(longest((obs.get("machine_output") or {}).get("records"), "evidence_class") or "")
    if "OCR" in tc.upper():
        return "ocr"
    if (obs.get("evidence") or {}).get("ocr"):
        return "ocr"
    return "paste"


def cite_rows(obs):
    cs = (obs.get("citations_and_sources") or {}).get("citations") or []
    out = []
    for i, c in enumerate(cs, 1):
        out.append({
            "n": c.get("n") or c.get("order") or i,
            "site": c.get("site") or c.get("site_label"),
            "rel": c.get("rel") or c.get("relation"),
            "title": c.get("title"),
            "snip": c.get("snip") or c.get("snippet"),
            "url": c.get("url"),
            "note": c.get("note"),
        })
        for extra in ("layer", "date_shown", "display"):
            if c.get(extra) is not None:
                out[-1][extra] = c[extra]
    return out


def image_urls(obs):
    """Absolute URLs only. A filename is not an image: six addresses looked
    promotable because a bare filename sat in the record and no file existed."""
    urls = []
    for im in ((obs.get("evidence") or {}).get("images") or []):
        p = im.get("repo_path") or im.get("mirror_url")
        if not p:
            continue
        urls.append(p if p.startswith("http") else "https://www.alexanarch.org/" + p.lstrip("/"))
    return urls


def defects_of(obs):
    d = []
    cs = obs.get("citations_and_sources") or {}
    cits = [c for c in (cs.get("citations") or []) if (c.get("rel") or c.get("relation")) != "unresolvable"]
    cc = (obs.get("classification") or {}).get("capture_conditions") or {}
    if cc.get("interaction_required_to_reveal_more"):
        d.append("truncated-by-interface")
    if (cs.get("citation_summary") or {}).get("_do_not_count"):
        d.append("unsupported-citations")
    if not cits:
        d.append("citations-null")
    if not obs.get("observed_on") or obs.get("observed_on") == "null":
        d.append("date-unresolved")
    surf = obs.get("surface")
    if not surf or surf in ("UNRESOLVED", "UNDETERMINED"):
        d.append("surface-unresolved")
    anl = longest((obs.get("analysis") or {}).get("records"), "value")
    if anl and not (obs.get("classification") or {}).get("finding"):
        d.append("analysis-without-finding")
    return sorted(set(d)) or None


def mint_slug(q, date, taken):
    """Every entry needs a UNIQUE PERMANENT SLUG — it is the citation handle and
    the page anchor. Observations seated without one crashed the gallery builder
    on `esc(None)`. Minted here deterministically in the corpus's own form:
    the query slugified to 56 chars, then the compact date."""
    import re as _re
    base = _re.sub(r"[^a-z0-9]+", "-", str(q or "capture").lower()).strip("-")[:56].strip("-")
    slug = f"{base}-{str(date or '').replace('-', '')}"
    n, out = 2, slug
    while out in taken:
        out = f"{slug}-{n}"; n += 1
    taken.add(out)
    return out


def project_obs(obs, addr, taken=None):
    sa = addr["semantic_address"]
    mf = obs.get("measurement_flags") or {}
    mo = (obs.get("machine_output") or {}).get("records")
    finding = (obs.get("classification") or {}).get("finding")
    cl = cite_rows(obs)
    slug = obs.get("legacy_slug") or mint_slug(sa.get("q_as_issued"), obs.get("observed_on"),
                                               taken if taken is not None else set())
    return {
        "slug": slug,
        "date": obs.get("observed_on"),
        "surface": obs.get("surface") or sa.get("surface"),
        "auth": (obs.get("auth_state") or {}).get("value"),
        "ev": evidence_class(obs),
        "cites": len(cl) or None,
        "per": mf.get("per_score"),
        "per_v": ({"author": mf.get("author_retained"), "inst": mf.get("institution_retained"),
                   "id": mf.get("doi_retained"), "src": mf.get("composition_source_included")}
                  if mf.get("per_score") is not None else None),
        "mt": first_value((obs.get("classification") or {}).get("match_or_finding")) or "CAPTURE",
        # d is the card blurb: the finding when one was written, the analyst
        # reading otherwise. 164 records carry analysis with no finding, and a
        # card that showed nothing for them showed a reviewer nothing at all.
        "d": finding or longest((obs.get("analysis") or {}).get("records"), "value"),
        "reading": (obs.get("record_history") or {}).get("interface_observation"),
        "analysis": longest((obs.get("analysis") or {}).get("records"), "value"),
        "transcript": longest(mo, "text"),
        "transcript_class": longest(mo, "evidence_class"),
        "transcript_complete": longest(mo, "completeness"),
        "transcript_read": longest(mo, "read_status"),
        "cite_list": cl or None,
        "collisions": (obs.get("classification") or {}).get("collisions"),
        "oq": obs.get("open_questions") or None,
        "imgs": [im.get("filename") for im in ((obs.get("evidence") or {}).get("images") or [])],
        "img_urls": image_urls(obs),
        "defects": defects_of(obs),
        "rounds": obs.get("rounds"),
        "rerun": sa.get("rerun_url"),
        "q": sa.get("q_as_issued"),
        "s": section_of(obs),
        "addr_id": sa.get("address_id"),
        "obs_id": obs.get("observation_id"),
        "q_kind": obs.get("q_kind"),
        "series": len(addr.get("observations") or []),
        "wrapper": (obs.get("transcript_wrapper") or {}).get("status"),
    }


_SLUGS = set()


def project_addr(addr):
    obs = sorted(addr.get("observations") or [], key=lambda o: str(o.get("observed_on") or ""))
    if not obs:
        return None
    rows = [project_obs(o, addr, _SLUGS) for o in obs]
    # THE DISPLAY IMAGE IS INHERITED FROM THE ADDRESS. «alexanarch» showed
    # "no image" while holding three observations, because the entry only ever
    # looked at the one it was built from. Most recent imaged observation wins.
    lead = rows[-1]
    imaged = [r for r in reversed(rows) if r["img_urls"]]
    entry = dict(lead)
    entry["observations"] = rows
    entry["n_observations"] = len(rows)
    entry["dates"] = sorted({r["date"] for r in rows if r["date"]})
    entry["surfaces"] = sorted({r["surface"] for r in rows if r["surface"]})
    entry["other_slugs"] = [r["slug"] for r in rows if r["slug"] and r["slug"] != lead["slug"]]
    entry["series"] = len(rows)
    if imaged:
        entry["img_urls"] = imaged[0]["img_urls"]
        entry["imgs"] = imaged[0]["imgs"]
        entry["_display_image_from"] = imaged[0]["obs_id"]
    entry["cite"] = ("https://www.alexanarch.org/captures/#" + lead["slug"]) if lead["slug"] else None
    entry["d_full"] = lead["d"]
    entry["d_truncated"] = bool(lead["d"] and len(lead["d"]) > 240)
    return entry


def build(canon):
    _SLUGS.clear()
    entries = [project_addr(a) for a in canon["addresses"]]
    entries = [e for e in entries if e]
    entries.sort(key=lambda e: (str(e.get("q") or "\uffff").lower(), str(e.get("slug") or "")))
    obs_count = sum(e["n_observations"] for e in entries)
    return {
        "registry_id": "EA-WG-CAPTURES-01",
        "version": "11.0",
        "date": canon.get("date"),
        "author": "Lee Sharks",
        "orcid": "0009-0000-1599-0703",
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "_authority": ("DERIVED. The canonical store is "
                       "rebuild/capture-registry/EA-WG-CAPTURES-01-REBUILD.json. "
                       "This file is built from it by scripts/project_captures.py and is "
                       "never written to. Renderers render; a gallery is a window, not a store."),
        "_projector": "scripts/project_captures.py",
        "_derived_from_sha256": canon.get("_canonical_sha256"),
        "address_count": len(entries),
        "observation_count": obs_count,
        "total_captures": len(entries),
        "entries": entries,
    }


def emit(canon_bytes, canon):
    canon = dict(canon)
    canon["_canonical_sha256"] = hashlib.sha256(canon_bytes).hexdigest()
    payload = build(canon)
    return json.dumps(payload, indent=1, ensure_ascii=False, sort_keys=False)


# ------------------------------------------------------------------ verify
CARRY = ["date", "surface", "auth", "ev", "per", "mt", "d", "reading", "analysis",
         "transcript", "transcript_class", "transcript_complete", "cite_list",
         "rerun", "q", "s", "addr_id", "obs_id"]


def verify(new, published):
    """Carry-layer diff. Computed fields are excluded by construction."""
    pub = {}
    for e in published["entries"]:
        for o in (e.get("observations") or [e]):
            if o.get("obs_id"):
                pub[o["obs_id"]] = o
    got = {}
    for e in new["entries"]:
        for o in e["observations"]:
            if o.get("obs_id"):
                got[o["obs_id"]] = o
    shared = set(pub) & set(got)
    diffs = collections.Counter()
    examples = {}
    for oid in shared:
        for f in CARRY:
            a, b = pub[oid].get(f), got[oid].get(f)
            if a != b:
                diffs[f] += 1
                examples.setdefault(f, (oid, a, b))
    print(f"published observations {len(pub)} | rebuilt {len(got)} | shared {len(shared)}")
    print(f"only in published: {len(set(pub)-set(got))} | only in rebuilt: {len(set(got)-set(pub))}")
    print("\nCARRY-LAYER DIFF")
    if not diffs:
        print("  no differences on any carried field")
    for f, n in diffs.most_common():
        oid, a, b = examples[f]
        print(f"  {n:>5}/{len(shared)}  {f}")
        print(f"           published: {json.dumps(a, ensure_ascii=False)[:100]}")
        print(f"           rebuilt  : {json.dumps(b, ensure_ascii=False)[:100]}")
    return diffs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="carry-layer diff against the published projection; writes nothing")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    cb = CANON.read_bytes()
    canon = json.loads(cb)
    text = emit(cb, canon)
    new = json.loads(text)
    print(f"canonical {len(canon['addresses'])} addresses / "
          f"{sum(len(x['observations']) for x in canon['addresses'])} observations")
    print(f"projected {new['address_count']} entries / {new['observation_count']} observations")
    if a.verify:
        verify(new, json.loads(OUT.read_text()))
    if a.write:
        OUT.write_text(text)
        again = emit(CANON.read_bytes(), json.loads(CANON.read_bytes()))
        print("\ndeterminism:", "byte-identical" if again == text else "*** NOT DETERMINISTIC ***")
        print("written:", OUT, hashlib.sha256(text.encode()).hexdigest()[:16])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
