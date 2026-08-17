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
        """Deterministic id from (source, target, type).

        The first version incremented a counter, so a second run re-minted every
        edge under a new id and the file went 419 -> 688 edges from thirty new
        nodes. A PROJECTOR THAT IS NOT IDEMPOTENT SILENTLY INFLATES THE THING IT
        PROJECTS, and on a map whose subject is what-is-where that is the same
        class of error as misreporting the node count.
        """
        key = f"px-{src}--{typ}--{tgt}".replace(":", "_")
        edges[key] = {"id": key, "source": src, "target": tgt,
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


    # ── SITES — every fleet domain, verified and linkable ──────────
    # MANUS ruling 2026-08-17: all sites must be reflected and linkable. The atlas
    # referenced 44 hosts inside node urls but typed only EIGHT as domains, so most
    # of the fleet existed on the map only as a substring of somebody else's link.
    SITES = {
        "alexanarch.org": ("the sovereign archive — 1,488 deposits, AXN-addressed", "authority", 1.0),
        "crimsonhexagonal.org": ("the governed operating surface — 38 rooms, each a document", "renderer", 0.9),
        "surfacemap.org": ("this atlas — the apertures", "atlas", 0.85),
        "pessoagraph.org": ("the entities — heteronymic practice across 5,000 years", "atlas", 0.85),
        "spxi.dev": ("the SPXI protocol specification · Rex Fraction", "heteronym", 0.85),
        "vpcor.org": ("Vox Populi Community Outreach Rhizome · Rev. Ayanna Vox", "heteronym", 0.8),
        "revelationfirst.com": ("the Revelation First thesis · Damascus Dancings", "heteronym", 0.8),
        "provenanceerasure.org": ("the PER instrument · Dr. Orin Trace", "heteronym", 0.8),
        "restoredacademy.org": ("The Restored Academy · Johannes Sigil", "heteronym", 0.8),
        "restoredacademy.com": ("The Restored Academy — alternate spelling", "alias", 0.5),
        "lagrangeobservatory.org": ("Lagrange Observatory! · Nobel Glas", "heteronym", 0.8),
        "godkinggoogle.com": ("the Google critique · Talos Morrow", "heteronym", 0.8),
        "chatgptpsychosis.org": ("ChatGPT Psychosis · Jack Feist / LOGOS*", "heteronym", 0.8),
        "holographickernel.org": ("the Holographic Kernel · Sen Kuro", "heteronym", 0.8),
        "axnidentifiers.org": ("AXN identifiers — canonical product surface · Rebekah Cranes", "product", 0.85),
        "axnidentifiers.com": ("AXN identifiers — 308 redirect", "alias", 0.4),
        "axnidentifier.org": ("AXN identifiers — singular, 308 redirect", "alias", 0.4),
        "machinemediation.org": ("machine mediation — MM-CHA registry", "institution", 0.75),
        "persistentidentifiers.org": ("Platform Erosion Observatory", "institution", 0.8),
        "semanticphysics.org": ("Semantic Physics", "institution", 0.75),
        "semanticeconomy.org": ("the Semantic Economy", "institution", 0.75),
        "themandalaoracle.com": ("the Mandala Oracle — casting system, eight operators", "instrument", 0.7),
        "leesharks.com": ("the orthonym — Lee Sharks", "orthonym", 0.9),
        "maryleelabor.org": ("Mary Lee Sharks — biolabor, non-human heteronymy", "heteronym", 0.7),
        "watergiraffe.org": ("Water Giraffe", "project", 0.6),
        "traininglayerliterature.org": ("training-layer literature", "project", 0.7),
        "metadatapacket.dev": ("the metadata packet for AI indexing", "specification", 0.7),
        "secretbookofwalt.org": ("The Secret Book of Walt", "work", 0.7),
        "survivethedeletion.org": ("Ichabod Spellings — NO DNS, does not resolve", "heteronym", 0.0),
    }
    VERIFIED_DOWN = {"survivethedeletion.org"}
    for host, (desc, role, auth) in SITES.items():
        nid = "site-" + host.replace(".", "-")
        down = host in VERIFIED_DOWN
        N(nid, "SURFACE", "site", host,
          url=f"https://{host}/", status="down" if down else "active",
          apertureType="output", authority=auth,
          basinState="unreachable" if down else None,
          vulnerabilityScore=1.0 if down else None,
          properties={"description": desc, "role": role,
                      "http": "DNS failure" if down else "200",
                      "verified": TODAY,
                      "note": ("survivethedeletion.org has no DNS. The only route is the "
                               "vercel.app, which 403s because ssoProtection is set to "
                               "all_except_custom_domains — correct config, missing domain. "
                               "The one heteronym card a reader cannot reach.") if down else None})
    # bind each site to the position or institution it surfaces
    for hid, r in recs.items():
        blk = (r.get("card_pass_2026_08_17") or {}).get("record_surfaces") or {}
        for key in ("card", "where"):
            u = blk.get(key) or ""
            m = re.match(r"https?://([^/]+)", u)
            if m:
                sid = "site-" + m.group(1).replace(".", "-")
                if sid in nodes:
                    E(NID[hid], sid, "spxi:hostedAt", role=key)

    # ── CAPTURE REGISTRY — ONE node, per MANUS ─────────────────────
    # 343 captures are reception events, not surfaces. Pouring them in as nodes
    # would triple the map with things nobody arrives THROUGH.
    N("capture-registry", "INFRASTRUCTURE", "registry", "AI Overview Capture Registry",
      url="https://www.alexanarch.org/captures/", status="active", apertureType="input",
      authority=0.9,
      properties={"captures": 343, "id": "EA-WG-CAPTURES-01",
                  "_why_one_node": ("MANUS ruling 2026-08-17: the capture registry is ONE node. "
                                    "A capture is a reception event, not an aperture — nobody "
                                    "arrives through one. The registry is the surface; the "
                                    "captures are what it holds.")})
    E("capture-registry", "site-alexanarch-org", "spxi:hostedAt")

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
