#!/usr/bin/env python3
"""build_axn_relations.py — typed relations between AXN-identified objects (adopted 2026-10-27).

A hash names bytes; it supplies no relation. Relations are read only from fields that record them, never from prose:

  /non rows (datasets/negative-of-the-negative/v2/rows/*.json), subject the row's current AXN
    follows      the row's spec (`spec`, the "#N" it names): the deposit whose procedure the composition follows
    opens        a capture observation the row registers (any `obs_id` field of the row outside its superseded versions); since 2026-10-27
                 an observation of the /non register has its own AXN (scripts/nonreg_axn.py); one without is given by its locator
    grounds_in   a deposit a kernel claim takes its source from (`kernel[].source`, "#N")
    read         a defining paper read for the composition (`composition_v09.defining_papers_read[]`, with the extent read)
  capture joins (data/capture-joins.json), confirmed relations only (its render rule), subject the observation's AXN
    appeared_in, mentions, pair_of, about, distorts — as the join records them; a deposit, an observation or a /non entry
    as object is given by its AXN, an SPXI instrument method or a surface by its URL
  releases (data/releases/axn.json), subject the object's root
    follows      a rhizome dataset's grammar; the Capture Registry's intake instrument
    scored_by    the Capture Registry's PER-dim rubric
    documented_in the deposit that documents an instrument

Each relation carries the file and field it was read from. Writes data/axn-relations.json: the relations, and an index
by hex of outgoing and incoming relations, which the resolver pages render in both directions.
"""
import collections, glob, json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = "https://www.alexanarch.org"


def load(p, default=None):
    try:
        return json.loads((ROOT / p).read_text(encoding="utf-8"))
    except Exception:
        return default


def main():
    deps = load("data/registry.json")["deposits"]
    by_n = {d["deposit_number"]: d for d in deps}
    cap = (load("data/captures/axn.json") or {}).get("addresses", {})
    by_obs = {}
    for a in cap.values():
        for k, o in a["observations"].items():
            if o.get("obs_id"):
                by_obs[o["obs_id"]] = o["axn"]
    for a in ((load("datasets/negative-of-the-negative/v2/register-axn.json") or {}).get("addresses") or {}).values():
        for k, o in a["observations"].items():
            if o.get("obs_id"):
                by_obs.setdefault(o["obs_id"], o["axn"])   # /non register observations (scripts/nonreg_axn.py, 2026-10-27)
    non = (load("datasets/negative-of-the-negative/v2/axn.json") or {}).get("entries", {})
    rel_led = (load("data/releases/axn.json") or {}).get("objects", {})
    non_reg = {e["obs_id"]: e.get("slug") for e in ((load("datasets/negative-of-the-negative/v2/register.json") or {}).get("entries") or []) if e.get("obs_id")}
    rels = []

    def dep(n):
        if not str(n).strip().isdigit():
            return None
        d = by_n.get(int(n))
        return d["axn"] if d else None

    def add(s, verb, o, src, field, basis=None, label=None):
        if s and o:
            r = {"subject": s, "verb": verb, "object": o, "source": src, "field": field}
            if basis:
                r["basis"] = basis
            if label:
                r["object_label"] = label
            rels.append(r)

    for k, x in sorted(non.items()):
        src = x["row"]
        row = load(src) or {}
        s = x["axn"]
        for n in re.findall(r"#(\d+)", str(row.get("spec") or "")):
            add(s, "follows", dep(n), src, "spec", row.get("spec"))
        def walk(o, path):
            if isinstance(o, dict):
                if re.fullmatch(r"OBS-[0-9a-f]{12}", str(o.get("obs_id") or "")):
                    if o["obs_id"] in by_obs:
                        add(s, "opens", by_obs[o["obs_id"]], src, path + ".obs_id", o["obs_id"])
                    elif o["obs_id"] in non_reg:
                        # an observation of the /non register (not seated in the Capture Registry): located, not identified
                        add(s, "opens", f"{SITE}/datasets/negative-of-the-negative/v2/register.json#{o['obs_id']}", src, path + ".obs_id",
                            o["obs_id"], f"/non register observation {non_reg[o['obs_id']]}")
                for kk_, vv in o.items():
                    if kk_ != "superseded":
                        walk(vv, f"{path}.{kk_}" if path else kk_)
            elif isinstance(o, list):
                for i_, vv in enumerate(o):
                    walk(vv, f"{path}[{i_}]")
        walk(row, "")
        for kk in row.get("kernel") or []:
            for n in re.findall(r"#(\d+)", str(kk.get("source") or "")):
                add(s, "grounds_in", dep(n), src, f"kernel[{kk.get('K')}].source", kk.get("sense"))
        for pr in ((row.get("composition_v09") or {}).get("defining_papers_read") or []):
            if pr.get("dep"):
                add(s, "read", dep(pr["dep"]), src, "composition_v09.defining_papers_read", pr.get("read"))

    j = load("data/capture-joins.json") or {}
    for r in j.get("relations", []):
        if r.get("state") != "confirmed" or r.get("verb") in ("held_by", "scored_by"):
            continue   # held_by / scored_by name the SPXI method of every observation; carried once per release below
        s = by_obs.get(r.get("obs_id"))
        kind, _, val = str(r.get("object") or "").partition(":")
        o = label = None
        if kind == "deposit" and val.isdigit():
            o = dep(val)
        elif kind == "observation":
            o = by_obs.get(val)
        elif kind == "non" and val in non:
            o = non[val]["axn"]
        elif kind == "instrument":
            o, label = f"https://www.spxi.dev/methods/#m-{val.replace('.', '-')}", f"SPXI method {val}"
        elif kind == "surface":
            o, label = None, None   # the surface a card appeared on is the observation's own field, not a relation between objects
        add(s, r["verb"], o, "data/capture-joins.json", r.get("id"), r.get("basis"), label)

    def root(key):
        return (rel_led.get(key) or {}).get("root")
    for key, L in sorted(rel_led.items()):
        if L.get("instrument"):
            add(L["root"], "follows", root(L["instrument"]), "data/releases/axn.json", f"objects.{key}.instrument")
        if L.get("documented_in"):
            add(L["root"], "documented_in", dep(L["documented_in"]), "data/releases/axn.json", f"objects.{key}.documented_in")
    if root("capture-registry"):
        add(root("capture-registry"), "follows", root("capture-intake"), "scripts/build_axn_relations.py", "the registry's intake path (AGENTS.md §5, PIPELINE.md)")
        add(root("capture-registry"), "scored_by", root("per-dim-rubric"), "scripts/build_axn_relations.py", "per_dim on every observation (spec: the rubric)")

    seen, out = set(), []
    for r in rels:
        k = (r["subject"], r["verb"], r["object"])
        if k not in seen:
            seen.add(k); out.append(r)

    def hx(a):
        m = re.match(r"AXN:([0-9A-F]+)", str(a))
        return m.group(1) if m else None
    idx = collections.defaultdict(lambda: {"out": [], "in": []})
    for i, r in enumerate(out):
        if hx(r["subject"]):
            idx[hx(r["subject"])]["out"].append(i)
        if hx(r["object"]):
            idx[hx(r["object"])]["in"].append(i)
    verbs = collections.Counter(r["verb"] for r in out)
    doc = {"name": "AXN relations", "description": __doc__.split("\n\n")[1].strip(), "count": len(out), "verbs": dict(verbs),
           "relations": out, "by_hex": dict(sorted(idx.items()))}
    (ROOT / "data/axn-relations.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"axn relations: {len(out)} ({dict(verbs)}); {len(idx)} hexes")


if __name__ == "__main__":
    main()
