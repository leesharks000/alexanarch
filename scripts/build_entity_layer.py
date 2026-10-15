#!/usr/bin/env python3
"""build_entity_layer.py — the Capture Registry's second analytical anchor: the ENTITY (2026-10-15).

THE RULING (Lee Sharks, 2026-10-15 01:57 / 02:03 EDT). "the primary anchor of analysis for the capture registry is the
semantic address ... it makes less sense now that unprimed chatgpt, where conversational framing is required to trigger
search, is making up more and more of the captures. there needs to be an additional analytical layer tied to the entity."
On scoring: "both but target is main - a faithful composition of rebekah crane when rebekah cranes was the target is still
total erasure, and substitution is the most common form of erasure. so we dont give fidelity score on the wrong entity."

WHAT THIS WRITES (the registry, data/EA-WG-CAPTURES-01.json, is read and never written):
  data/entities.json           the entity register: one record per entity a capture can target or reach.
  data/entity-relations.json   one row per observation: TARGET (what the query and its framing aim at), REACHED (what the
                               composition arrived at), FRAMING (the conditions of a conversational surface), and the
                               SCORE, which is taken against the target only.

THE TWO RELATIONS, KEPT APART. The heteronym linkers match a name anywhere in the description or transcript; that merges
target and reached, and a capture that composes a namesake is counted to the entity it displaced. Here the target is read
off the address (and the operator turn, and the originator field the operator recorded), never off the answer.

REACHED, by kind:  same       the target entity, composed as itself
                   weakened   the target, its binding weakened (term held, attribution or scope lost)
                   substitute another entity in the target's place (a namesake, a near-spelling, a generic sense)
                   collision  the target and another entity merged or set side by side as one
                   generic    the term composed as a common noun or category, no entity
                   refused    no composition (the surface declined, or did not search)
                   unread     not yet decided by reading
SCORE: per_target is the observation's PER where reached is same or weakened; 1.0 where the target is absent from the
composition (substitute, generic, refused); the reached entity receives no fidelity score. Laws record, they do not block:
an observation with no target found is written with target "unassigned".

  python3 scripts/build_entity_layer.py            # write both files
  python3 scripts/build_entity_layer.py --check    # report counts only
"""
import json, pathlib, re, sys, hashlib, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
READ = ROOT / "rebuild/entity-layer/read.json"          # relations decided by reading, keyed by obs key

# The archive's own entities that no other register carries (name, type, aliases, defining deposits).
CORE = [
    ("Crimson Hexagonal Archive", "archive", ["crimson hexagonal archive", "crimson hexagon archive", "crimson hexagonal", "crimson hexagon", "CHA"], [1]),
    ("Alexanarch", "site", ["alexanarch", "alexanarch.org"], []),
    ("Capture Registry", "dataset", ["capture registry", "EA-WG-CAPTURES-01", "ai overview capture registry"], [3]),
    ("SPXI", "protocol", ["spxi", "spxi protocol", "semantic packet for exchange", "spxi.dev"], [660]),
    ("Semantic Economy", "concept", ["semantic economy"], [18, 291]),
    ("Semantic Economy Institute", "institution", ["semantic economy institute", "semanticeconomy.org"], []),
    ("Operative Semiotics", "concept", ["operative semiotics", "operativesemiotics.org"], []),
    ("AXN", "protocol", ["axn", "axn identifier", "axnidentifiers.org"], []),
    ("The Mandala Oracle", "site", ["mandala oracle", "themandalaoracle"], []),
    ("Training-Layer Literature", "concept", ["training-layer literature", "training layer literature"], [1543]),
    ("Retrocausal Canon Formation", "concept", ["retrocausal canon formation"], []),
    ("Provenance Erasure Rate", "concept", ["provenance erasure rate", "PER"], []),
    ("Come Out of Her, My People", "work", ["come out of her, my people", "come out of her my people"], [1427]),
    ("The Citrini Memo (canonization)", "work", ["citrini memo", "citrini"], [513, 22]),
    ("Restored Academy", "institution", ["restored academy", "restoredacademy"], [119]),
    ("Arch-Philosopher Mantle", "concept", ["arch-philosopher mantle", "arch-philosopher"], [1679]),
    ("Living Academy Mantle", "concept", ["living academy mantle", "living academy"], [1680]),
]
MERGE = {"sharks, lee": "Lee Sharks", "sigil": "Johannes Sigil", "crimson hexagonal archive": "Crimson Hexagonal Archive"}


def eid(name):
    return "ENT-" + hashlib.sha1(name.strip().lower().encode()).hexdigest()[:10]


def register(reg):
    ents = {}

    def add(name, typ, aliases, deposits, source, relation="archive", extra=None):
        name = MERGE.get(name.strip().lower(), name.strip())
        k = eid(name)
        r = ents.setdefault(k, {"id": k, "name": name, "type": typ, "relation": relation, "aliases": [], "defining_deposits": [], "seeded_from": []})
        for a in [name] + list(aliases):
            if a and a.lower() not in [x.lower() for x in r["aliases"]]:
                r["aliases"].append(a)
        for d in deposits:
            if d not in r["defining_deposits"]:
                r["defining_deposits"].append(d)
        if source not in r["seeded_from"]:
            r["seeded_from"].append(source)
        if r["type"] in (None, "unknown") and typ:
            r["type"] = typ
        if extra:
            r.update({k2: v for k2, v in extra.items() if k2 not in r})
    for name, typ, al, deps in CORE:
        add(name, typ, al, deps, "core")
    for p in sorted((ROOT / "datasets/heteronyms/records").glob("*.json")):
        h = json.loads(p.read_text(encoding="utf-8"))
        if h.get("identity_type") in ("heteronym", "heteronym_aperture"):
            add(h["name"], "person", [], [], f"heteronym record {p.stem}", extra={"heteronym": True})
    ne = json.loads((ROOT / "data/named-entities.json").read_text(encoding="utf-8"))
    for n in ne["entities"]:
        add(n["name"], "person", [], [], "named-entities", relation="external", extra={"wikidata": n.get("wikidata")})
    ni = json.loads((ROOT / "non/index.json").read_text(encoding="utf-8"))
    for row in ni.get("entities") or []:
        slug = isinstance(row, dict) and (row.get("entity") or row.get("slug"))
        if slug:
            add(row.get("name") or slug.replace("-", " "), "concept", [slug.replace("-", " ")], [], f"/non {slug}", relation="external")
    for e in reg["entries"]:
        o = e.get("originator") or {}
        if o.get("name"):
            nm = re.split(r" \(", o["name"])[0]
            add(nm, o.get("entity_type") or "unknown", [], [], "originator", relation=o.get("relation") or "archive")
    return ents


def matcher(ents):
    pats = []
    for r in ents.values():
        for a in r["aliases"]:
            if len(a) < 3 and a not in ("CHA",):
                continue
            if a in ("PER", "AXN", "CHA"):
                pats.append((re.compile(r"(?<![A-Za-z])" + re.escape(a) + r"(?![A-Za-z])"), r["id"], len(a)))
            else:
                pats.append((re.compile(r"(?<![a-z0-9])" + re.escape(a.lower()) + r"(?![a-z0-9])"), r["id"], len(a)))
    return pats


def targets(q, pats, orig_id):
    found = {}
    for rx, k, n in pats:
        hay = q if rx.pattern.startswith("(?<![A-Za-z])") else q.lower()
        for m in rx.finditer(hay):
            span = (m.start(), m.end())
            if k not in found or n > found[k][1]:
                found[k] = (span, n)
    # drop a match wholly inside a longer match of another entity ("semantic economy" inside "semantic economy institute")
    keep = [k for k, (s, n) in found.items() if not any(k2 != k and s2[0] <= s[0] and s[1] <= s2[1] and n2 > n for k2, (s2, n2) in found.items())]
    out = [{"ent": k, "basis": "address"} for k in sorted(keep, key=lambda k: found[k][0][0])]
    # The originator says whose entity the capture concerns (the owner), not what the query aims at: it is the target
    # only where the address names no registered entity.
    if not out and orig_id:
        out = [{"ent": orig_id, "basis": "originator (operator-recorded); the address names no registered entity"}]
    return out


VERBS = [("read and characterize", r"\bread and characteri[sz]e"), ("track the development", r"\btrack\b"), ("work thru", r"\bwork (thru|through)\b"),
         ("walk me thru", r"\bwalk me (thru|through)\b"), ("full index", r"\bfull index\b"), ("evaluate / status", r"\b(evaluat|status of)"),
         ("why", r"^\s*why\b"), ("what is / who is", r"^\s*(what|who)('s| is| are| was)\b"), ("tell me about", r"\btell me about\b"), ("whats this", r"\bwhats? this\b")]


def framing(e, o):
    q = o.get("q") or e.get("q") or ""
    ql = q.lower()
    v = next((name for name, rx in VERBS if re.search(rx, ql)), "bare term" if len(q.split()) <= 4 else "other instruction")
    turns = o.get("turns") or e.get("turns")
    return {"instruction": v, "url_given": bool(re.search(r"https?://|\b[a-z0-9-]+\.(org|com|dev|co|net)\b", ql)),
            "location_instruction": bool(re.search(r"\b(mirror|locate|find the (full )?text|any source)\b", ql)),
            "turns": (len(turns) if isinstance(turns, list) else turns) or 1,
            "search_fired": bool(o.get("cite_list") or (o.get("cites") or 0) > 0)}


def reached_derived(o):
    ca = o.get("composed_as") or {}
    br = str(ca.get("binding_relation") or "")
    if o.get("collisions"):
        # A recorded namesake says one was present (on a card or in the body); whether it entered the composition is read.
        return "unread", [c.get("with") for c in o["collisions"] if isinstance(c, dict)], "collisions field: namesake present; composition unread"
    if br.upper().startswith("SEVERED"):
        return "generic", [ca.get("term_returned")], "composed_as.binding_relation SEVERED"
    if br.lower().startswith("weakened"):
        return "weakened", [], "composed_as.binding_relation weakened"
    if br.lower().startswith("present"):
        return "same", [], "composed_as.binding_relation present"
    return "unread", [], None


def main(check=False):
    reg = json.loads(REG.read_text(encoding="utf-8"))
    ents = register(reg)
    pats = matcher(ents)
    read = json.loads(READ.read_text(encoding="utf-8")) if READ.exists() else {}
    rows = []
    for e in reg["entries"]:
        obs = e.get("observations") or [e]
        o_name = re.split(r" \(", (e.get("originator") or {}).get("name") or "")[0]
        orig_id = eid(MERGE.get(o_name.strip().lower(), o_name.strip())) if o_name else None
        for j, o in enumerate(obs):
            key = o.get("obs_id") or f"{e['slug']}#{j + 1}"
            q = o.get("q") or e.get("q") or ""
            surf = o.get("surface") or e.get("surface") or ""
            row = {"key": key, "entry": e["slug"], "date": o.get("date") or e.get("date"), "surface": surf, "q": q,
                   "target": targets(q, pats, orig_id) or [{"ent": "unassigned", "basis": "no registered entity in the address"}],
                   "owner": orig_id}
            kind, others, basis = reached_derived(o if (o is e or o.get("collisions") or o.get("composed_as") or len(obs) > 1) else {**e, **o})
            row["reached"] = {"kind": kind, "others": [x for x in others if x], "basis": basis, "state": "derived" if kind != "unread" else "open"}
            row["framing"] = framing(e, o)
            if key in read:
                r = read[key]
                for f in ("target", "reached", "note"):
                    if f in r:
                        row[f] = r[f]
                row["reached"]["state"] = "read"
            k = row["reached"]["kind"]
            per = o.get("per")
            row["score"] = {"against": row["target"][0]["ent"],
                            "per_target": (1.0 if k in ("substitute", "generic", "refused") else per if k in ("same", "weakened", "collision") else None),
                            "reached_scored": False,
                            "rule": "PER against the target; 1.0 where the target is absent; the reached entity is not scored (ruling 2026-10-15)"}
            rows.append(row)
    by_ent = collections.Counter(t["ent"] for r in rows for t in r["target"][:1])
    for k, r in ents.items():
        r["observations_targeting"] = by_ent.get(k, 0)
    kinds = collections.Counter(r["reached"]["kind"] for r in rows)
    print(f"entity layer: {len(ents)} entities; {len(rows)} observations; unassigned {by_ent.get('unassigned', 0)}; "
          f"reached kinds {dict(kinds)}; read {sum(1 for r in rows if r['reached']['state'] == 'read')}")
    if check:
        return
    head = {"derived_from": f"EA-WG-CAPTURES-01 v{reg.get('version')}", "ruling": "Lee Sharks, 2026-10-15: target is the main anchor; no fidelity score on the wrong entity."}
    (ROOT / "data/entities.json").write_text(json.dumps({**head, "name": "Entity register of the Capture Registry", "count": len(ents),
        "entities": sorted(ents.values(), key=lambda r: (-r["observations_targeting"], r["name"]))}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (ROOT / "data/entity-relations.json").write_text(json.dumps({**head, "name": "Observation-to-entity relations", "count": len(rows),
        "reached_kinds": ["same", "weakened", "substitute", "collision", "generic", "refused", "unread"], "rows": rows}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main("--check" in sys.argv)
