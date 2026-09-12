#!/usr/bin/env python3
"""build_rhizome_mc.py — EA-RHIZOME-MC-01, the first rhizome emitted from the graph layer.

A RHIZOME IS NOT A COLLECTION AND NOT "everything within two hops". It is a NAMED
TRAVERSAL GRAMMAR applied to the archive's typed relations, emitted with its own recipe so
the result is reproducible and its boundary is visible.

THE SUBJECT AND THE STRUCTURE COINCIDE, which is why this one is first: a model-collapse
dataset should itself resist collapse — by preserving plurality, competing mechanisms,
counterexamples, corrections, provenance, and OUTGOING ROUTES to material it does not
contain. It is meant to be an anti-collapse dataset in its construction, not only about
anti-collapse.

SELECTION IS DETERMINISTIC AND RUNS ON DEFINED CONCEPTS, NOT ON TEXT SEARCH. A keyword pass
over titles and descriptions returns 361 deposits, which is the failure mode this rule
exists to prevent: model collapse becomes the whole archive because everything eventually
touches everything. Selecting on `defines_concept` edges — a deposit's own declaration of
what it defines — returns 57. That is a corpus.

    CORE      a deposit that DEFINES a matching concept, or MEASURES / IS MEASURED BY one
    NEIGHBOUR one typed hop from core, by a predicate in the follow set
    FRONTIER  a node reachable at the second hop, emitted as a STOLON and NOT included

Every row carries collapse_axis and dynamic_role rather than a collapse boolean, because a
binary would flatten the phenomenon the dataset is for.
"""
import json, pathlib, re, collections, datetime, hashlib
import os

ROOT = pathlib.Path(__file__).resolve().parent.parent

# SEVERANCE IS A COLLAPSE MODE THE PATTERN DID NOT NAME (2026-09-11). The SYMBOLON
# deposits define severance as dividing a fused object into independently adjudicated
# layers — the loss of relations BETWEEN parts while every part survives intact. That
# is distributional collapse's structural cousin: nothing is deleted and the object
# stops being what it was. It sat outside the rhizome because the pattern named loss of
# CONTENT and not loss of RELATION.
#
# This is a widening of the select pattern and should be read as one. It admits a
# vocabulary the rule did not previously see, on the stated ground that severance is a
# contraction of relational structure. It is not a widening to raise counts, and the
# three deposits it admits were identified by reading, not by search.
# THE GRAMMAR IS READ, NOT CARRIED (2026-09-12). The select pattern, the role vocabulary
# and its ORDER, the collapse axes, the follow set and the stolon frontier were hardcoded
# here, which meant the emitter could VERIFY a configuration and not RE-PARAMETERISE one.
# Editing the spore alone could not produce a different body, so "deterministic seed" was
# half true: reproducible, not portable.
#
# The demonstration: role_for() applied to 136 retrieval-engineering deposits does not fall
# to the default. It spreads plausibly across the collapse vocabulary, 33% of it
# anti_collapse_intervention, because the pattern contains `protocol` and every technical
# deposit says protocol. THE FAILURE MODE OF AN UNPORTABLE VOCABULARY IS NOT EMPTINESS. It
# is false confidence — a distribution that looks like a finding and means nothing.
#
# A second body needs its own grammar file, not a fork of this script.
GRAMMAR = os.environ.get("RHIZOME_GRAMMAR", "rhizomes/_grammars/collapse.json")
_G = json.loads((ROOT / GRAMMAR).read_text(encoding="utf-8"))
SELECT = re.compile(_G["select"]["pattern"], re.I)
ROLES = [(r["role"], re.compile(r["pattern"], re.I)) for r in _G["roles"]]
AXES = {k: re.compile(v, re.I) for k, v in _G["axes"].items()}
FOLLOW = set(_G["follow"])
STOLONS = _G["stolons"] or []

# THE BODY'S IDENTITY IS ALSO CONFIGURATION (2026-09-12). Slug, id, node prefix, parent and
# topology were hardcoded, so a second grammar would have emitted into the first body's
# directory under the first body's node ids. A spore is not a template that gets copied; it
# germinates, and the germinated body needs its own name before it has anything else.
_B = _G["body"]
_SR = _G.get("special_roles", {})
OUT = ROOT / "rhizomes" / _B["slug"]

# axis of contraction — a concept may sit on several


# dynamic role — what the node DOES in the field, not what it is about
# ORDER IS THE CLASSIFIER (2026-09-11). role_for returns on the first match, so a
# broad pattern placed above a narrow one swallows it. #635, Fractal Semantic
# Architecture — a PROPOSED TRAINING PARADIGM whose stated claim is that discrete
# relational supervision may REDUCE recursive synthetic-data collapse — was classed
# `collapse_measure` because the bare word `measure` matched inside "measured
# coherence". An anti-collapse proposal was filed as a collapse metric.
#
# Two repairs: proposal patterns are hoisted above the measure pattern, and the
# measure pattern's bare tokens are bounded so `measure` alone no longer fires.


# THE FOLLOW SET EXCLUDES defines_concept ON PURPOSE. A core deposit defines many concepts,
# most of them unrelated to contraction; following that predicate outward pulled 1,470
# neighbours in the first run and reproduced, one level in, the same everything-touches-
# everything failure the text-search rule was written to avoid. A concept a core deposit
# defines is part of that deposit's own description — it is carried in the `defines` column
# — not a neighbour reached by traversal. Concepts enter as neighbours only when they match
# the select pattern, which is handled separately below.


# frontier: where this rhizome runs out, and what it advertises instead of absorbing



def axes_for(text):
    # AXES and ROLES now hold COMPILED patterns, loaded from the grammar file. Passing a
    # compiled pattern to re.search with flags raises; call .search on the object instead.
    return sorted(a for a, p in AXES.items() if p.search(text)) or ["unclassified"]


def role_for(text):
    for r, p in ROLES:
        if p.search(text):
            return r
    return _G.get("default_role", "observation")


def main():
    reg = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text())["deposits"]}
    E = [json.loads(l) for l in (ROOT / "data/relations.jsonl").read_text().splitlines() if l.strip()]
    N = {}
    for l in (ROOT / "data/nodes.jsonl").read_text().splitlines():
        if l.strip():
            n = json.loads(l); N[n["node_id"]] = n
    A = {a["about"]: a for a in (json.loads(l) for l in (ROOT / "data/assertions.jsonl").read_text().splitlines() if l.strip())}

    # ---- CORE: defines a matching concept, or measures / is measured by one
    core, why = {}, collections.defaultdict(set)
    for e in E:
        if e["predicate"] != "defines_concept":
            continue
        lab = N.get(e["target_id"], {}).get("label", "")
        if SELECT.search(lab):
            core[e["source_id"]] = "A"
            why[e["source_id"]].add(lab)
    for e in E:
        if e["predicate"] in ("measures", "measured_by") and (e["source_id"] in core or e["target_id"] in core):
            for x in (e["source_id"], e["target_id"]):
                core.setdefault(x, "B")

    # RULE D — A RECORDED FAILURE OF A CLAIM ALREADY IN THE CORPUS (2026-09-11).
    # #678 SYMBOLON-02 "records the failure of SYMBOLON-01's strongest defensive claim"
    # and reclassifies the catalogue accordingly. It fell between rules A and C: its
    # DEFINED CONCEPTS ARE "Why these matter" AND "Why these work" — section headings
    # captured as terms, which is a registry defect of the same family as the deposits
    # that declare no concepts at all — and its title carries no instrument word.
    #
    # A deposit that records the failure of a claim held in this corpus is the strongest
    # kind of entry the dataset can hold, and it was the one the rules could not see.
    # Admitted on the description-level signal, marked core_rule D so the weaker basis
    # is never confused with a declared concept.
    FAILURE = re.compile(r"records the failure|failure of|did not hold|continued to|"
                         r"reclassifi|disconfirm|contrary to|against the (?:author|thesis|claim)", re.I)
    for num, d in reg.items():
        nid = f"deposit:{num}"
        if nid in core:
            continue
        blob = " ".join(str(d.get(k) or "") for k in ("title", "description"))
        if SELECT.search(blob) and FAILURE.search(str(d.get("description") or "")):
            core[nid] = "D"
            why[nid].add("[recorded failure: " + (FAILURE.search(d["description"]).group(0)) + "]")

    # RULE C — TITLE-DECLARED INSTRUMENTS. The first run missed five of the eight deposits the
    # design named, including Fear and Trembling (#783), the Self-Audit Module (#156), the
    # Atomic Token Rule (#789), Erasure Skew (#157) and Measurement Sovereignty (#788). The
    # rule was not wrong: THOSE DEPOSITS DECLARE ZERO CONCEPTS. defines_concepts is empty on
    # all five, so the graph cannot see them however central they are.
    #
    # That is a gap in the registry, not in the traversal, and it is recorded in the spore
    # rather than patched silently. This rule admits a deposit whose TITLE declares a named
    # instrument or mechanism of contraction — a weaker signal than a declared concept, marked
    # as such in core_rule so the two are never confused.
    for num, d in reg.items():
        nid = f"deposit:{num}"
        if nid in core:
            continue
        t = str(d.get("title") or "")
        if SELECT.search(t) and re.search(r"rate|rule|module|skew|sovereignty|contraction|renewal|audit|"
                                          r"collapse|erasure|custody|monoculture", t, re.I):
            core[nid] = "C"
            why[nid].add("[title-declared: " + t[:60] + "]")

    # ---- THREE FURTHER CORE PRINCIPLES, GATED BY THE GRAMMAR (2026-09-12).
    # Rules A-D select on what a deposit SAYS. Three bodies measured against each other showed
    # that one family of rules cannot reach the reception body:
    #
    #   editorial  MMRS journal assignments          119 deposits
    #   vocabulary reception word-match              963
    #   evidence   deposits an actual capture cited  332  — only 29% of the journal
    #
    # None reproduces another. The word-match agrees with 86% of the journal's members and
    # drags in 860 others, because A RECEPTION ARCHIVE'S AMBIENT VOCABULARY IS RECEPTION
    # VOCABULARY. The editor sees propagation — memography, virality — that no measurement
    # vocabulary contains. The evidence sees what surfaces actually touched, which is a
    # different thing from what theorises reception.
    #
    # So the disagreements are the body's data, not its error, and each node records which
    # principle admitted it. A body that declares none of these is unaffected.
    _CP = _G.get("core_principles", {})

    # RULE E — EDITORIAL. A venue assignment is an ACT, not a rule. This is the first spore
    # material that CANNOT BE REGENERATED FROM THE LEDGER: the gate can verify it has not
    # drifted and cannot derive it. Stated in the spore rather than discovered later.
    if _CP.get("editorial"):
        field, want = _CP["editorial"]["field"], _CP["editorial"]["match"]
        for num, d in reg.items():
            if want.lower() in str(d.get(field) or "").lower():
                nid = f"deposit:{num}"
                core.setdefault(nid, "E")
                why[nid].add(f"[editorial: {field}={want}]")

    # RULE V — VOCABULARY, bounded. The unbounded form selects 963 of 1,329 deposits, so it
    # is admitted only where a deposit ALSO declares a concept, which is the archive's own
    # signal that it is making a distinction rather than mentioning one.
    if _CP.get("vocabulary"):
        for num, d in reg.items():
            nid = f"deposit:{num}"
            if nid in core:
                continue
            blob = " ".join(str(d.get(k) or "") for k in ("title", "description"))
            if SELECT.search(blob) and (d.get("defines_concepts") or []):
                core[nid] = "V"
                why[nid].add("[vocabulary + declares a concept]")

    # RULE O — OBSERVED. A deposit an actual capture cited. The only one of the three with a
    # derived-deterministic basis, and the only one a buyer can check without trusting us.
    if _CP.get("observed"):
        links = json.loads((ROOT / "data/capture-deposit-links.json").read_text(encoding="utf-8"))
        for slug, v in (links.get("links") or {}).items():
            for d_ in (v.get("deposits") or []):
                num = d_.get("deposit_number")
                if isinstance(num, int):
                    nid = f"deposit:{num}"
                    core.setdefault(nid, "O")
                    why[nid].add(f"[observed: cited in capture {slug[:40]}]")

    # ---- CAPTURES: THE EMPIRICAL ARM (2026-09-11).
    # The rhizome saw three node types — deposit, concept, problem — because those are
    # what the relation ledger holds. The archive's 419 captures are the OBSERVATIONS of
    # erasure, substitution, nullification and frame effects, and a model-collapse dataset
    # whose empirical arm is outside it is a bibliography. Captures enter as their own node
    # type, with their PER score where one was computed, and are linked to the deposits
    # they concern by the existing resolver.
    #
    # A CAPTURE IS ALWAYS AN OBSERVATION and is typed as one. It records what a surface
    # did; it does not propose a mechanism or an intervention. Where a capture measured
    # something it carries collapse_measure instead, on the PER field rather than on words.
    caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]
    links = json.loads((ROOT / "data/capture-deposit-links.json").read_text(encoding="utf-8"))
    # THE RESOLVER NESTS THE DEPOSITS UNDER A `deposits` KEY, one level deeper than a
    # first pass assumed — which produced an empty link map and zero capture edges while
    # the build reported success. Unwrapped here against the file's actual shape.
    link_map = {}
    for k, v in (links.get("links") or {}).items():
        for d_ in (v.get("deposits") or []) if isinstance(v, dict) else []:
            num = d_.get("deposit_number") if isinstance(d_, dict) else d_
            if isinstance(num, int):
                link_map.setdefault(k, []).append(num)

    cap_nodes = 0
    cap_edges = []
    for c_ in caps:
        blob = " ".join(str(c_.get(k) or "") for k in ("d", "reading", "analysis", "s", "q"))
        blob += " " + " ".join(c_.get("findings") or [])
        if not SELECT.search(blob):
            continue
        cid = "capture:" + c_["slug"]
        core[cid] = "E"
        why[cid].add("[capture: " + str(c_.get("surface") or "")[:40] + "]")
        cap_edges.extend((cid, num) for num in link_map.get(c_["slug"], []))
        cap_nodes += 1

    # ---- NEIGHBOUR: one typed hop out, follow set only
    nb = {}
    for e in E:
        if e["predicate"] not in FOLLOW:
            continue
        if e["source_id"] in core and e["target_id"] not in core:
            nb.setdefault(e["target_id"], e["predicate"])
        if e["target_id"] in core and e["source_id"] not in core:
            nb.setdefault(e["source_id"], e["predicate"])
    # concepts enter only on their own merits: the concept itself must match the pattern.
    for e in E:
        if e["predicate"] == "defines_concept" and e["source_id"] in core:
            lab = N.get(e["target_id"], {}).get("label", "")
            if SELECT.search(lab) and e["target_id"] not in core:
                nb.setdefault(e["target_id"], "defines_concept")

    included = set(core) | set(nb)

    # ---- rows
    rows = []
    for nid in sorted(included):
        n = N.get(nid, {})
        dep = int(nid.split(":")[1]) if nid.startswith("deposit:") and nid.split(":")[1].isdigit() else None
        d = reg.get(dep, {})
        blob = " ".join(str(d.get(k) or "") for k in ("title", "description")) + " " + " ".join(sorted(why.get(nid, ())))
        if not blob.strip():
            blob = n.get("label", "")
        if nid.startswith("capture:"):
            cap = next((x for x in caps if "capture:" + x["slug"] == nid), {})
            rows.append({
                "rhizome_node_id": _B["node_prefix"] + ":" + hashlib.sha256(nid.encode()).hexdigest()[:10],
                "graph_node_id": nid, "deposit_number": None,
                "title": cap.get("s") or cap.get("slug"),
                "node_type": "capture", "region": "core", "core_rule": "E", "entered_by": None,
                "dynamic_role": _SR["capture_measured"] if cap.get("per") is not None else _SR["capture_unmeasured"],
                "collapse_axis": json.dumps(axes_for(" ".join(str(cap.get(k) or "") for k in ("d", "reading", "s")))),
                "defines": json.dumps([]), "creator": cap.get("surface"), "date": cap.get("date"),
                "evidence_status": "CAPTURED", "axn": None,
                "source_uri": "https://www.alexanarch.org/captures/#" + cap.get("slug", ""),
            })
            continue
        rows.append({
            "rhizome_node_id": _B["node_prefix"] + ":" + hashlib.sha256(nid.encode()).hexdigest()[:10],
            "graph_node_id": nid,
            "deposit_number": dep,
            "title": d.get("title") or n.get("label"),
            "node_type": n.get("node_type"),
            "region": "core" if nid in core else "neighbour",
            "core_rule": core.get(nid),
            "entered_by": nb.get(nid),
            # THE ADMISSION BASIS OUTRANKS THE BLOB CLASSIFIER (2026-09-11). A node admitted
            # by RULE D entered BECAUSE its description records the failure of a claim held in
            # this corpus. role_for() reads the same blob as every other node and knows nothing
            # about why the node was admitted, so all five Rule D entries received ordinary
            # roles and the dataset emitted ZERO counterexample labels — losing exactly the
            # property that let them in. SYMBOLON-02, which records the failure of SYMBOLON-01's
            # strongest defensive claim, was filed anti_collapse_mechanism.
            #
            # A rule that knows why it admitted something knows more than a regex over the text.
            "dynamic_role": _SR["recorded_failure"] if core.get(nid) == "D" else role_for(blob),
            "collapse_axis": json.dumps(axes_for(blob)),
            "defines": json.dumps(sorted(why.get(nid, ()))),
            "creator": d.get("creator"),
            "date": d.get("date"),
            "evidence_status": d.get("status") or ("—" if dep is None else "ACTIVE"),
            "axn": d.get("axn"),
            "source_uri": f"https://alexanarch.org/s/records/{dep}/" if dep else None,
        })

    # ---- edges internal to the body
    edges = []
    for e in E:
        if e["source_id"] in included and e["target_id"] in included:
            a = A.get(e["relation_id"], {})
            edges.append({**{k: e[k] for k in ("relation_id", "source_id", "predicate", "target_id",
                                               "target_type", "basis", "status", "note")},
                          "asserted_by": a.get("asserted_by"),
                          "rhizome_role": ("counteracts" if e["predicate"] in ("rejects", "preserves") else
                                           "measures" if e["predicate"] in ("measures", "measured_by") else
                                           "corrects" if e["predicate"] in ("corrects", "supersedes") else
                                           "develops" if e["predicate"] in ("develops_from", "inherits", "transforms") else
                                           "defines" if e["predicate"] == "defines_concept" else "relates")})

    # THE COUNTEREXAMPLE MUST REACH WHAT IT DISCONFIRMS (2026-09-11). A node admitted for
    # recording a failure was, until now, connected to nothing that explains what failed:
    # SYMBOLON-02 and SYMBOLON-01 sat in the same body with no edge between them, so the
    # dataset held a disconfirmation and no route from the promise to the test that broke it.
    #
    # An anti-collapse dataset whose counterexamples are unreachable from the claims they
    # qualify is a list, not a field. The edge is typed `disconfirms` and is reciprocal in
    # effect: arriving at the promise, one can reach the failure; arriving at the failure,
    # one can reconstruct why the promise mattered.
    DISCONFIRMS = [(678, 675, "records the failure of SYMBOLON-01's strongest defensive claim; "
                              "the tested model continued to separate fused registers")]
    for src, tgt, note in DISCONFIRMS:
        a, b = f"deposit:{src}", f"deposit:{tgt}"
        if a in included and b in included:
            edges.append({"relation_id": None, "source_id": a, "predicate": "disconfirms",
                          "target_id": b, "target_type": "deposit", "basis": "editorial",
                          "status": "current", "note": note, "asserted_by": "editor:cha",
                          "rhizome_role": "disconfirms"})

    # capture -> deposit, from the resolver, kept only where the deposit is in the body
    for cid, num in cap_edges:
        tgt = f"deposit:{num}"
        if cid in included and tgt in included:
            edges.append({"relation_id": None, "source_id": cid, "predicate": "observes",
                          "target_id": tgt, "target_type": "deposit",
                          "basis": "derived-deterministic", "status": "current",
                          "note": "capture-deposit resolver", "asserted_by": "process:resolve_capture_links",
                          "rhizome_role": "observes"})

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "nodes.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    (OUT / "relations.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in edges) + "\n", encoding="utf-8")
    (OUT / "stolons.jsonl").write_text("\n".join(json.dumps(
        {"from": f, "predicate": p, "to_rhizome": t, "note": w, "status": "advertised, not included"},
        ensure_ascii=False) for f, p, t, w in STOLONS) + "\n", encoding="utf-8")

    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    spore = {
        "rhizome": _B["slug"],
        "maxim": "all things are now lawful to you in christ jesus",
        "rhizome_id": _B["rhizome_id"],
        "parent": _B["parent"],
        "parent_uri": "https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive",
        "version": "0.1",
        "generated": ts,
        "topology": _B["topology"],
        "poles": ["collapse", "anti-collapse", "recovery"],
        "seed_mode": "deterministic",
        "core_depth": 1,
        "frontier_depth": 2,
        "selection": {
            "core_A": "a deposit that DEFINES a concept matching the select pattern",
            "core_B": "a deposit that measures or is measured by an A",
            "core_C": "a deposit whose TITLE declares a named instrument or mechanism — a weaker signal, marked as such",
            "core_D": "a deposit whose DESCRIPTION records the failure of a claim already in this corpus — admitted on a description-level signal, marked as such",
            "core_E": "a CAPTURE whose finding concerns the collapse vocabulary — the empirical arm, a different node type entirely, linked to the deposits it observes",
            "gap_found": ("Rule C exists because five of the eight deposits the design named DECLARE ZERO CONCEPTS: "
                          "#783 Fear and Trembling, #156 Self-Audit Module, #789 Atomic Token Rule, #157 Erasure Skew, "
                          "#788 Measurement Sovereignty. defines_concepts is empty on all five. The traversal was correct "
                          "and the registry is incomplete. Rule D exists for a second form of the same defect: "
                          "#678 SYMBOLON-02 declares 'Why these matter' and 'Why these work' as its concepts — "
                          "section headings captured as terms — so a deposit that records the failure of a claim "
                          "held in this corpus was invisible to both A and C. Recorded here rather than patched silently, because a rhizome "
                          "that hides the holes in its own substrate is the thing this dataset is against."),
            "neighbour": "one typed hop from core, restricted to the follow set",
            "frontier": "second hop — emitted as a stolon and NOT included",
            "select_pattern": SELECT.pattern,
            "follow": sorted(FOLLOW),
            "why_not_text_search": ("A keyword pass over titles and descriptions returns 361 deposits — model collapse "
                                    "becomes the whole archive because everything eventually touches everything. "
                                    "Selection on defines_concept, a deposit's own declaration, returns a corpus."),
        },
        "counts": {"nodes": len(rows), "core": sum(1 for r in rows if r["region"] == "core"),
                   "neighbour": sum(1 for r in rows if r["region"] == "neighbour"),
                   "edges": len(edges), "stolons": len(STOLONS)},
        "adjacent": [s[2] for s in STOLONS],
        "generator": "scripts/build_rhizome_mc.py",
        "source_commit": None,
        "design_principle": ("A model-collapse dataset should itself resist collapse: preserve plurality, competing "
                             "mechanisms, counterexamples, corrections, provenance, and outgoing routes to what it "
                             "does not contain. It is an anti-collapse dataset in its construction, not only about it."),
    }
    (OUT / "spore.json").write_text(json.dumps(spore, ensure_ascii=False, indent=1), encoding="utf-8")

    rc = collections.Counter(r["dynamic_role"] for r in rows)
    ac = collections.Counter(a for r in rows for a in json.loads(r["collapse_axis"]))
    print(f"{_B['rhizome_id']} v0.1 — {len(rows)} nodes ({spore['counts']['core']} core, "
          f"{spore['counts']['neighbour']} neighbour), {len(edges)} edges, {len(STOLONS)} stolons")
    print("  roles: " + ", ".join(f"{k}={v}" for k, v in rc.most_common()))
    print("  axes:  " + ", ".join(f"{k}={v}" for k, v in ac.most_common(8)))


if __name__ == "__main__":
    main()
