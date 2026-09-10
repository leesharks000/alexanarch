#!/usr/bin/env python3
"""build_relations.py — the canonical typed relation ledger, emitted from what the archive already holds.

WHY THIS EXISTS (2026-09-09). The archive knows several distinct geometries — citation
networks, supersession chains, lines of thought with development edges, instruments that
measure claims, journal issues as ordered selections, heteronymic frames — and until now
each lived as a differently-shaped field on a deposit row. Consumers therefore had to know
the archive's field names to traverse it, and one untyped array (`related_deposits`, 801
edges) carried relations of no stated kind at all.

THE OCCASION was a defect. data/named-entities.json declares itself a register of persons
the works DEAL WITH. Deposit #1604, whose title is "Rebekah Cranes ≠ Rebekah Crane",
carried entities: ["sappho"] — correct under that contract, since it is ABOUT Sappho and
BY Cranes. Adding the heteronyms to that register to "fix" it made the array mean two
things at once. The right repair is not a wider register but a typed edge:

    deposit:1604 --created_by--> heteronym:rebekah-cranes
    deposit:1604 --about--> person:sappho

NOTHING IS CURATED HERE. Every edge is derived from an existing substrate, and every edge
carries a `basis` recording how it was obtained. The ledger is a NORMALISATION, not a new
assertion layer; the denormalised columns on `deposits` remain, and become projections of
this file rather than the authoritative store of the relation.

BASIS VOCABULARY — controlled, not a confidence score:
  asserted              a person stated it in the record (pressure blocks, develops_from)
  editorial             an editorial decision recorded in a registry (journal assignment)
  derived-deterministic computed by a rule with no judgement (series chains, inverses)
  pattern-detected      matched by an explicit stated pattern (named-entity aboutness)
"""
import json, pathlib, re, unicodedata, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_E = ROOT / "data/relations.jsonl"
OUT_N = ROOT / "data/nodes.jsonl"


def slug(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main():
    reg = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]
    act = [d for d in reg if (d.get("status") or "ACTIVE") == "ACTIVE"]
    by_n = {d["deposit_number"]: d for d in reg if d.get("deposit_number")}

    ents = json.loads((ROOT / "data/named-entities.json").read_text(encoding="utf-8"))["entities"]
    for e in ents:
        e["_rx"] = re.compile(e["pattern"], re.I)

    # heteronymic identities: canonical store is datasets/heteronyms/records/
    hets = {}
    for f in sorted((ROOT / "datasets/heteronyms/records").glob("*.json")):
        h = json.loads(f.read_text(encoding="utf-8"))
        pid = h.get("person_id") or slug(h.get("name", ""))
        hets[pid] = h

    E, N = [], {}

    def node(nid, ntype, label, **kw):
        if nid not in N:
            N[nid] = {"node_id": nid, "node_type": ntype, "label": label, **{k: v for k, v in kw.items() if v}}
        return nid

    import hashlib

    def rid(s, p, t):
        """A stable id for the relation itself, so an assertion can point AT it and a
        reified relation can hang off it. Content-derived: the same triple always gets the
        same id, across rebuilds and across machines."""
        return "rel:" + hashlib.sha256(f"{s}|{p}|{t}".encode()).hexdigest()[:16]

    def edge(s, p, t, basis, ttype, note=None, src=None, frame=None):
        E.append({"relation_id": rid(s, p, t),
                  "source_id": s, "predicate": p, "target_id": t, "target_type": ttype,
                  "basis": basis, "note": note, "provenance": src, "frame_id": frame})

    # ---- nodes: deposits, identities, aboutness persons
    for d in act:
        node(f"deposit:{d['deposit_number']}", "deposit", d.get("title", ""),
             axn=d.get("axn"), record_url=f"https://alexanarch.org/s/records/{d['deposit_number']}/")
    for pid, h in hets.items():
        it = h.get("identity_type", "identity")
        node(f"{'heteronym' if 'heteronym' in it else 'identity'}:{pid}", it, h.get("name", pid),
             function=h.get("function"), office=(h.get("office") or {}).get("title"))
    for e in ents:
        node(f"person:{e['id']}", "person", e["name"], wikidata=e.get("wikidata"), floruit=e.get("floruit"))

    # ---- created_by: the creator string resolved to an identity node where one exists
    hname = {h.get("name", "").lower(): pid for pid, h in hets.items()}
    # "Sharks, Lee" and "Lee Sharks" both occur
    def resolve_creator(c):
        c = (c or "").strip()
        if not c: return None
        flat = c.lower()
        if "," in c:
            flat = " ".join(reversed([x.strip() for x in c.split(",", 1)])).lower()
        for nm, pid in hname.items():
            if nm and (nm in flat or flat in nm): return pid
        return None

    for d in act:
        pid = resolve_creator(d.get("creator"))
        s = f"deposit:{d['deposit_number']}"
        if pid:
            it = hets[pid].get("identity_type", "identity")
            edge(s, "created_by", f"{'heteronym' if 'heteronym' in it else 'identity'}:{pid}",
                 "derived-deterministic", it, f"creator field: {d.get('creator')}", "registry.creator")
        else:
            edge(s, "created_by", f"agent:{slug(d.get('creator') or 'unattributed')}",
                 "derived-deterministic", "agent", d.get("creator"), "registry.creator")

    # ---- about: the aboutness register, pattern-detected
    for d in act:
        blob = " ".join(str(d.get(k) or "") for k in ("title", "description", "wiki_article")) \
               + " " + " ".join(d.get("keywords") or [])
        for e in ents:
            if e["_rx"].search(blob):
                edge(f"deposit:{d['deposit_number']}", "about", f"person:{e['id']}",
                     "pattern-detected", "person", f"pattern: {e['pattern'][:40]}", "named-entities.json")

    # ---- the registry's own typed fields
    for d in act:
        s = f"deposit:{d['deposit_number']}"
        for t in (d.get("cited_by") or []):
            if isinstance(t, int): edge(f"deposit:{t}", "cites", s, "derived-deterministic", "deposit", None, "registry.cited_by")
        for r in (d.get("develops_from") or []):
            t = r.get("deposit") if isinstance(r, dict) else r
            edge(s, "develops_from", f"deposit:{t}", "asserted", "deposit",
                 (r.get("what") if isinstance(r, dict) else None), "registry.develops_from")
        for r in (d.get("measured_by") or []):
            t = r.get("deposit") if isinstance(r, dict) else r
            edge(s, "measured_by", f"deposit:{t}", "asserted", "instrument",
                 (r.get("what") if isinstance(r, dict) else None), "registry.measured_by")
        sup = d.get("supersedes")
        for t in ([sup] if isinstance(sup, int) else (sup or [])):
            edge(s, "supersedes", f"deposit:{t}", "asserted", "deposit", None, "registry.supersedes")
        for t in (d.get("related_deposits") or []):
            if not isinstance(t, int): continue
            # RELATION OF NO STATED KIND. Kept, and kept marked: 801 of these exist and
            # collapsing them into a specific predicate would invent an assertion.
            edge(s, "related_unspecified", f"deposit:{t}", "derived-deterministic", "deposit",
                 "kind not stated in the source field", "registry.related_deposits")
        if d.get("line"):
            node(f"line:{slug(d['line'])}", "line", d["line"])
            edge(s, "part_of_line", f"line:{slug(d['line'])}",
                 "asserted" if d.get("line_basis") == "stated" else "derived-deterministic",
                 "line", f"basis: {d.get('line_basis')}", "registry.line")
        if d.get("version_series_id"):
            node(f"series:{slug(d['version_series_id'])}", "series", d["version_series_id"])
            edge(s, "part_of_series", f"series:{slug(d['version_series_id'])}", "asserted", "series", None, "registry.version_series_id")
        for c in (d.get("defines_concepts") or []):
            term = c.get("term") if isinstance(c, dict) else c
            if not term: continue
            node(f"concept:{slug(term)}", "concept", term)
            edge(s, "defines_concept", f"concept:{slug(term)}", "asserted", "concept", None, "registry.defines_concepts")
        # pressure: the archive's own typed predicates, already in the shape this ledger wants
        for pr in ((d.get("pressure") or {}).get("backward") or []):
            k, t = pr.get("k"), pr.get("to")
            if k is None: continue
            if isinstance(t, int):
                edge(s, k, f"deposit:{t}", "asserted", "deposit", pr.get("note"), "registry.pressure")
            else:
                pid = f"problem:{slug(str(t))[:60]}"
                node(pid, "problem", str(t))
                edge(s, k, pid, "asserted", "problem", pr.get("note"), "registry.pressure")

    # ---- published_in: editorial assignment
    ja = ROOT / "datasets/journals/assignments.jsonl"
    if ja.exists():
        for line in ja.read_text(encoding="utf-8").splitlines():
            if not line.strip(): continue
            r = json.loads(line)
            v = r.get("journal")
            if not (r.get("deposit") and v): continue
            node(f"journal:{slug(v)}", "journal", v)
            edge(f"deposit:{r['deposit']}", "published_in", f"journal:{slug(v)}", "editorial", "journal", None, "journals/assignments.jsonl")

    # ---- heteronym affiliations, from the canonical identity records
    for pid, h in hets.items():
        it = h.get("identity_type", "identity")
        s = f"{'heteronym' if 'heteronym' in it else 'identity'}:{pid}"
        for a in (h.get("institutional_affiliations") or []):
            inst = a.get("institution") if isinstance(a, dict) else a
            if not inst: continue
            node(f"institution:{slug(inst)}", "institution", inst)
            edge(s, "affiliated_with", f"institution:{slug(inst)}", "asserted", "institution",
                 (a.get("role") if isinstance(a, dict) else None), "heteronyms/records")
        orth = h.get("orthonym_relation")
        if isinstance(orth, dict) and orth.get("target"):
            edge(s, "orthonymic_relation", f"identity:{slug(orth.get('target'))}", "asserted", "identity",
                 orth.get("relation"), "heteronyms/records")

    # ---- STATUS AND VALIDITY, derived from the endpoints (2026-09-10).
    # Before this, 210 edges touched a superseded or withdrawn deposit and were
    # indistinguishable from current ones: the ledger said a relation held without saying
    # whether either end still stood. An edge is only as live as its endpoints.
    dstat = {f"deposit:{d['deposit_number']}": (d.get("status") or "ACTIVE") for d in reg}
    ddate = {f"deposit:{d['deposit_number']}": d.get("date") for d in reg}
    LIVE = {"ACTIVE", "CANONICAL"}
    # SOME PREDICATES REQUIRE A DEAD ENDPOINT. `supersedes` points at a superseded record
    # BY DEFINITION; marking it stale would report the edge doing its job as a defect. The
    # first run of this flagged 14 supersedes edges that way.
    EXPECTS_DEAD_TARGET = {"supersedes"}
    for e in E:
        ends = [dstat.get(e["source_id"])]
        if e["predicate"] not in EXPECTS_DEAD_TARGET:
            ends.append(dstat.get(e["target_id"]))
        dead = [x for x in ends if x and x not in LIVE]
        e["status"] = "current" if not dead else f"endpoint_{dead[0].lower()}"
        # the edge is asserted no earlier than the record that asserts it
        e["valid_from"] = ddate.get(e["source_id"])
        e["valid_to"] = None
    OUT_E.write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in E) + "\n", encoding="utf-8")
    OUT_N.write_text("\n".join(json.dumps(n, ensure_ascii=False) for n in N.values()) + "\n", encoding="utf-8")
    # ---- ASSERTIONS: the speech act, separate from its content.
    # An edge is WHAT is claimed. An assertion is WHO claimed it, WHEN, on WHAT BASIS, and
    # whether that claim still stands. Keeping them apart matters because the same relation
    # can be asserted by different parties at different times: the registry's creator field
    # and a person's stated pressure block are not the same kind of act, and one can be
    # revised without the other. Assertions point at relation_id, so they can equally attach
    # to a membership or to a reified relation later without changing shape.
    ASSERTERS = {
        "registry.pressure":        ("person:lee-sharks", "stated in the deposit's own pressure block"),
        "registry.develops_from":   ("person:lee-sharks", "stated development edge"),
        "registry.measured_by":     ("person:lee-sharks", "stated instrument relation"),
        "registry.supersedes":      ("person:lee-sharks", "stated supersession"),
        "registry.defines_concepts":("person:lee-sharks", "concepts declared by the deposit"),
        "registry.line":            ("person:lee-sharks", "line membership; basis field says stated or derived"),
        "journals/assignments.jsonl":("editor:cha", "editorial assignment to a venue"),
        "heteronyms/records":       ("person:lee-sharks", "the identity record"),
        "registry.creator":         ("process:build_relations", "resolved from the creator field, no judgement"),
        "registry.cited_by":        ("process:extract_citations", "extracted from the text"),
        "registry.related_deposits":("process:build_relations", "carried over; the source field states no kind"),
        "named-entities.json":      ("process:build_relations", "matched by the register's stated pattern"),
    }
    A = []
    for e in E:
        who, how = ASSERTERS.get(e.get("provenance") or "", ("process:build_relations", "derived"))
        A.append({"assertion_id": "as:" + hashlib.sha256(
                      f"{e['relation_id']}|{who}|{e['provenance']}".encode()).hexdigest()[:16],
                  "about": e["relation_id"],
                  "about_type": "relation",
                  "asserted_by": who,
                  "act": how,
                  "basis": e["basis"],
                  "on_date": e.get("valid_from"),
                  "status": e["status"],
                  "source": e.get("provenance"),
                  "retracted_by": None})
    (ROOT / "data/assertions.jsonl").write_text(
        "\n".join(json.dumps(a, ensure_ascii=False) for a in A) + "\n", encoding="utf-8")

    pc = collections.Counter(e["predicate"] for e in E)
    bc = collections.Counter(e["basis"] for e in E)
    nt = collections.Counter(n["node_type"] for n in N.values())
    sc = collections.Counter(e["status"] for e in E)
    ac = collections.Counter(a["asserted_by"] for a in A)
    print(f"relations: {len(E):,} edges over {len(N):,} nodes; {len(A):,} assertions")
    print("  status:     " + ", ".join(f"{k}={v:,}" for k, v in sc.most_common()))
    print("  asserted_by:" + ", ".join(f" {k}={v:,}" for k, v in ac.most_common()))
    print("  predicates: " + ", ".join(f"{k}={v:,}" for k, v in pc.most_common()))
    print("  basis:      " + ", ".join(f"{k}={v:,}" for k, v in bc.most_common()))
    print("  node types: " + ", ".join(f"{k}={v:,}" for k, v in nt.most_common()))


if __name__ == "__main__":
    main()
