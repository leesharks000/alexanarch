#!/usr/bin/env python3
"""project_aperture_atlas.py — project the alexanarch data atlas onto surfacemap.

surfacemap.org is THE APERTURES: through what opening does a thing become
reachable. Its topology-source.json was generated 2026-04-25 and carried 144
nodes. In the 114 days since, the archive grew a venues dataset, twelve /where/
pages, thirty-eight addressable rooms, a nine-step card pass, a dataflow binding
and eighteen datasets — and NONE OF IT WAS ON THE MAP THAT EXISTS TO SHOW WHERE
THINGS ARE.

The audit of 2026-08-17:

    venues        1 of 8      seven journals absent
    issues        0 of 7
    /where/       0 of 12     and a /where/ page IS an aperture onto a venue
    rooms         0 of 38
    datasets      0 of 18
    heteronyms   22 of 26
    gates         0 of 14     the checks that keep the archive true
    producers     0 of 10     the scripts that generate it

A NOTE ON WHAT COUNTS AS AN APERTURE. Not everything added here is one. A domain,
a /where/ page, a room URL, a journal — those are openings: a reader or a machine
arrives through them. A GATE IS NOT AN OPENING, it is machinery; a PRODUCER is
not an opening, it is a source. They are typed APPARATUS and PRODUCER rather than
SURFACE so the map does not quietly redefine its own central term to mean
"anything we have".

Writes topology-source.json in the surface-map repo. Existing nodes are preserved
by id; this adds and updates, never truncates.
"""
import json
import pathlib
import datetime
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TODAY = datetime.date.today().isoformat()


def slug(n):
    s = re.sub(r"^(the|r\.\d+|f\.\d+)\s+", "", str(n).strip(), flags=re.I)
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def load(p):
    return json.loads((ROOT / p).read_text())


def main(target):
    tp = pathlib.Path(target)
    atlas = json.loads(tp.read_text())
    nodes = {n["id"]: n for n in atlas["nodes"]}
    edges = {e["id"]: e for e in atlas["edges"]}
    before = (len(nodes), len(edges))
    eid = [max((int(m.group(1)) for e in edges for m in [re.match(r"e(\d+)$", e)] if m),
               default=len(edges))]

    def E(src, tgt, typ, **props):
        eid[0] += 1
        edges[f"e{eid[0]}"] = {"id": f"e{eid[0]}", "source": src, "target": tgt,
                               "type": typ, "directed": True, "properties": props or {}}

    def N(nid, typ, subtype, label, **kw):
        base = nodes.get(nid, {})
        nodes[nid] = {**base, "id": nid, "type": typ, "subtype": subtype, "label": label,
                      "lastVerified": TODAY, **{k: v for k, v in kw.items() if v is not None}}

    recs = {p.stem: json.loads(p.read_text())
            for p in (ROOT / "datasets/heteronyms/records").glob("*.json")}

    # REUSE THE EXISTING NODE ID WHERE THE PERSON IS ALREADY ON THE MAP.
    # The first run minted het-<slug> for all 26 and produced TEN PEOPLE UNDER TWO
    # IDS — Sigil as both "sigil" and "het-johannes-sigil". Same collision class as
    # the graph crosswalk that matched Mary Lee Sharks to Lee Sharks: a projection
    # that does not check what is already there does not extend a map, it forks it.
    existing = {str(n.get("label", "")).strip().lower(): n["id"]
                for n in nodes.values() if n.get("subtype") == "heteronym"}
    NID = {k: existing.get(r["name"].strip().lower(), f"het-{k}") for k, r in recs.items()}
    vens = {p.stem: json.loads(p.read_text())
            for p in (ROOT / "datasets/venues/records").glob("*.json")}
    isss = {p.stem: json.loads(p.read_text())
            for p in (ROOT / "datasets/venues/issues").glob("*.json")}
    bind = load("datasets/dataflow-atlas/binding-v3.4.json")

    # ── VENUES — each a publishing aperture ────────────────────────
    for vid, v in vens.items():
        N(f"venue-{vid}", "SURFACE", "journal", v["canonical"],
          status="active", apertureType="output", authority=0.8,
          properties={"registry_string": v.get("registry_string"),
                      "duoviri": v["editorial"].get("duoviri"),
                      "scope": v.get("scope")})
        for who in v["editorial"].get("duoviri") or []:
            m = [k for k, r in recs.items() if r["name"] == who]
            if m:
                E(NID[m[0]], f"venue-{vid}", "spxi:editsJointly",
                  office="duovirate", note="the office, held jointly")
        for b in v["editorial"].get("board") or []:
            nm = b.split("—")[0].strip()
            m = [k for k, r in recs.items() if r["name"] == nm]
            if m:
                E(NID[m[0]], f"venue-{vid}", "spxi:sitsOnBoard",
                  office="board seat", note="a board seat is not the office")

    # ── ISSUES ─────────────────────────────────────────────────────
    for iid, i in isss.items():
        vid = iid.rsplit("-", 1)[0]
        N(f"issue-{iid}", "DOCUMENT", "issue", i.get("title"),
          status=str(i.get("status", "")).lower(), apertureType="output",
          properties={"items": len(i.get("contents") or []), "volume": "1", "number": "1"})
        if f"venue-{vid}" in nodes:
            E(f"venue-{vid}", f"issue-{iid}", "spxi:publishes")

    # ── HETERONYMS + their card and /where/ apertures ──────────────
    for hid, r in recs.items():
        blk = r.get("card_pass_2026_08_17") or {}
        surf = blk.get("record_surfaces") or {}
        N(NID[hid], "IDENTITY", "heteronym", r["name"],
          status="active", hexAddress=r.get("hex"),
          properties={"function": r.get("function"),
                      "identity_type": r.get("identity_type"),
                      "mantle": (r.get("mantle") or {}).get("name")})
        if surf.get("card"):
            N(f"card-{hid}", "SURFACE", "page", f"who · {r['name']}",
              url=surf["card"], status="active", apertureType="output", authority=0.75)
            E(NID[hid], f"card-{hid}", "spxi:surfacesAt", role="identity card")
        if surf.get("where"):
            N(f"where-{hid}", "SURFACE", "page", f"where · {r['name']}",
              url=surf["where"], status="active", apertureType="output", authority=0.7,
              properties={"note": "an aperture onto a venue: where this position publishes"})
            E(NID[hid], f"where-{hid}", "spxi:surfacesAt", role="venue page")

    # ── ROOMS — addressable since 2026-08-17 ───────────────────────
    try:
        canon = json.loads(pathlib.Path("/tmp/crimson-hexagonal-interface/hexagon_canonical.json").read_text())
        for rm in canon["rooms"]:
            s = slug(rm["name"])
            N(f"room-{rm['id']}", "SURFACE", "room", rm["name"],
              url=f"https://crimsonhexagonal.org/rooms/{s}/",
              status="active", apertureType="output", authority=0.7,
              hexAddress=rm.get("hex_address"),
              properties={"physics": rm.get("physics"), "prompt": rm.get("prompt"),
                          "machine": f"https://crimsonhexagonal.org/rooms/{s}/index.json"})
        for rm in canon["rooms"]:
            for a in (rm.get("adjacent") or []):
                if f"room-{a}" in nodes:
                    E(f"room-{rm['id']}", f"room-{a}", "spxi:adjacentTo",
                      note="topological only — 2,851 typed CNM edges await import")
    except FileNotFoundError:
        print("  (rooms skipped: hexagon_canonical.json not local)")

    # ── DATASETS, PRODUCERS, GATES — the machinery, typed as such ──
    for dname, d in bind["datasets"].items():
        N(f"dataset-{dname}", "INFRASTRUCTURE", "dataset", dname,
          status="active" if d.get("canonical_declared") else "provisional",
          apertureType="input",
          properties={"files": d.get("files"), "bytes": d.get("bytes"),
                      "description": d.get("description"),
                      "binding_gaps": d.get("binding_gaps"),
                      "interlinked": d.get("interlinked")})
    for pname, p in (bind.get("producers") or {}).items():
        N(f"producer-{slug(pname)}", "PRODUCER", "script", pname,
          status="active",
          properties={"what": p if isinstance(p, str) else str(p)[:300]})
    for gname, g in (bind.get("gates") or {}).items():
        N(f"gate-{slug(gname)}", "APPARATUS", "gate", gname,
          status="active",
          properties={"what": g if isinstance(g, str) else str(g)[:300],
                      "note": "a gate is machinery, not an aperture"})

    atlas["nodes"] = list(nodes.values())
    atlas["edges"] = list(edges.values())
    atlas["version"] = "2.0"
    atlas["generated"] = TODAY
    atlas["source"] = "alexanarch data atlas — datasets/, projected by scripts/project_aperture_atlas.py"
    atlas["_projection"] = {
        "date": TODAY,
        "from": ["datasets/heteronyms/records", "datasets/venues/records",
                 "datasets/venues/issues", "datasets/dataflow-atlas/binding-v3.4.json",
                 "hexagon_canonical.json"],
        "nodes_before": before[0], "nodes_after": len(nodes),
        "edges_before": before[1], "edges_after": len(edges),
        "_aperture_discipline": (
            "SURFACE means an opening a reader or machine arrives through — a domain, a card, a "
            "/where/ page, a room, a journal. GATES are typed APPARATUS and PRODUCERS typed "
            "PRODUCER, because machinery is not an opening and the map must not redefine its own "
            "central term to mean anything the archive happens to hold."),
        "_preserved": "Existing nodes are matched by id and updated, never truncated.",
    }
    tp.write_text(json.dumps(atlas, ensure_ascii=False, indent=1))
    print(f"  nodes {before[0]} -> {len(nodes)}   edges {before[1]} -> {len(edges)}")
    import collections
    print("  types:", dict(collections.Counter(n["type"] for n in atlas["nodes"])))
    return atlas


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/sm/topology-source.json")
