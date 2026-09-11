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

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "rhizomes/model-collapse-anti-collapse"

SELECT = re.compile(
    r"collapse|contraction|monoculture|foreclosure|tail renewal|erasure|diversity loss|"
    r"pristine fallacy|athetic|custody|non-erasure|source tether|measurement sovereign|"
    r"atomic token|erasure skew|self-audit|counterexample", re.I)

# axis of contraction — a concept may sit on several
AXES = {
    "distributional": r"diversity|distribution|variance|tail|entropy|monoculture",
    "lexical": r"lexical|vocabulary|term|token",
    "stylistic": r"stylistic|style|voice",
    "epistemic": r"epistemic|foreclosure|search space|pristine|inquiry",
    "contextual": r"context|recursive contextual",
    "provenance": r"provenance|attribution|erasure skew|\bPER\b|citation",
    "referential": r"referential|ghost|reference",
    "retrieval": r"retrieval|summar|composition|index",
    "institutional": r"classifier|moderation|institution|certif|governance",
    "archival": r"archiv|tombstone|deletion|withdraw|custody|book-burning",
    "authorial": r"heteronym|author|plural",
    "methodological": r"method|protocol|audit|test|measure",
}

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
ROLES = [
    ("anti_collapse_instrument", r"self-audit|audit module|erasure skew|atomic token|measurement sovereign|calculator"),
    ("anti_collapse_mechanism", r"tail renewal|source tether|non-erasure|athetic|custody|plural authorship|heteronym|redundan|mirror|"
                                r"relational supervision|training paradigm|anti-severance|fused documentary"),
    ("anti_collapse_intervention", r"intervention|protocol|remedy|restor|reclamation|recover|complementary training"),
    ("collapse_mechanism", r"contraction|foreclosure|monoculture|feedback|pristine fallacy|narrowing|capture"),
    ("collapse_measure", r"\bPER\b|\b\w+ rate\b|\bmetric\b|\bindex\b|\bscore\b|\bmeasurement of\b|\bmeasured across\b"),
    ("collapse_observation", r"observed|event|case|incident|log|ledger"),
    ("correction", r"erratum|correction|corrigend|revis"),
    ("counterexample", r"counterexample|counter-example|exception|boundary condition"),
]

# THE FOLLOW SET EXCLUDES defines_concept ON PURPOSE. A core deposit defines many concepts,
# most of them unrelated to contraction; following that predicate outward pulled 1,470
# neighbours in the first run and reproduced, one level in, the same everything-touches-
# everything failure the text-search rule was written to avoid. A concept a core deposit
# defines is part of that deposit's own description — it is carried in the `defines` column
# — not a neighbour reached by traversal. Concepts enter as neighbours only when they match
# the select pattern, which is handled separately below.
FOLLOW = {"measures", "measured_by", "corrects", "develops_from", "supersedes", "inherits",
          "transforms", "preserves", "rejects", "consequence",
          "registers_correspondence", "reads", "redirects", "states_priority_of"}

# frontier: where this rhizome runs out, and what it advertises instead of absorbing
STOLONS = [
    ("concept:provenance-erasure", "measured_through", "provenance-erasure",
     "PER, Erasure Skew and the Atomic Token Rule are the measurement apparatus; they are their own body"),
    ("concept:classifier-model-collapse", "governed_in", "classifier-governance",
     "moderation feedback as a governance question rather than a generative one"),
    ("concept:heteronymic-plurality", "instantiated_by", "heteronyms",
     "authorial plurality as an anti-collapse mechanism is instantiated by the identity records"),
    ("concept:semantic-economy", "situated_in", "semantic-economy",
     "the political economy in which contraction is profitable"),
    ("concept:machine-reception", "observed_in", "machine-mediated-reception",
     "the capture registry holds the observations; 411 captures are not reproduced here"),
    ("concept:archive-resilience", "practised_as", "archive-resilience",
     "substrate multiplication, mirrors and custody as operational practice"),
    ("concept:erratum", "corrected_in", "epistemic-corrections",
     "the errata slate is a body in its own right; a correction preserved is anti-collapse by function"),
]


def axes_for(text):
    return sorted(a for a, p in AXES.items() if re.search(p, text, re.I)) or ["unclassified"]


def role_for(text):
    for r, p in ROLES:
        if re.search(p, text, re.I):
            return r
    return "collapse_observation"


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
        rows.append({
            "rhizome_node_id": "mc:" + hashlib.sha256(nid.encode()).hexdigest()[:10],
            "graph_node_id": nid,
            "deposit_number": dep,
            "title": d.get("title") or n.get("label"),
            "node_type": n.get("node_type"),
            "region": "core" if nid in core else "neighbour",
            "core_rule": core.get(nid),
            "entered_by": nb.get(nid),
            "dynamic_role": role_for(blob),
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

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "nodes.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    (OUT / "relations.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in edges) + "\n", encoding="utf-8")
    (OUT / "stolons.jsonl").write_text("\n".join(json.dumps(
        {"from": f, "predicate": p, "to_rhizome": t, "note": w, "status": "advertised, not included"},
        ensure_ascii=False) for f, p, t, w in STOLONS) + "\n", encoding="utf-8")

    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    spore = {
        "rhizome": "model-collapse-anti-collapse",
        "rhizome_id": "EA-RHIZOME-MC-01",
        "parent": "crimson-hexagonal-archive",
        "parent_uri": "https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive",
        "version": "0.1",
        "generated": ts,
        "topology": "bipolar-dynamic",
        "poles": ["collapse", "anti-collapse", "recovery"],
        "seed_mode": "deterministic",
        "core_depth": 1,
        "frontier_depth": 2,
        "selection": {
            "core_A": "a deposit that DEFINES a concept matching the select pattern",
            "core_B": "a deposit that measures or is measured by an A",
            "core_C": "a deposit whose TITLE declares a named instrument or mechanism — a weaker signal, marked as such",
            "gap_found": ("Rule C exists because five of the eight deposits the design named DECLARE ZERO CONCEPTS: "
                          "#783 Fear and Trembling, #156 Self-Audit Module, #789 Atomic Token Rule, #157 Erasure Skew, "
                          "#788 Measurement Sovereignty. defines_concepts is empty on all five. The traversal was correct "
                          "and the registry is incomplete. Recorded here rather than patched silently, because a rhizome "
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
    print(f"EA-RHIZOME-MC-01 v0.1 — {len(rows)} nodes ({spore['counts']['core']} core, "
          f"{spore['counts']['neighbour']} neighbour), {len(edges)} edges, {len(STOLONS)} stolons")
    print("  roles: " + ", ".join(f"{k}={v}" for k, v in rc.most_common()))
    print("  axes:  " + ", ".join(f"{k}={v}" for k, v in ac.most_common(8)))


if __name__ == "__main__":
    main()
