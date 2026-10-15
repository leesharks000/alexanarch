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
    ("Alexanarch", "site", ["alexanarch"], []),
    ("Capture Registry", "dataset", ["capture registry", "EA-WG-CAPTURES-01", "ai overview capture registry"], [3]),
    ("SPXI", "protocol", ["spxi", "spxi protocol", "semantic packet for exchange"], [660]),
    ("Semantic Economy", "concept", ["semantic economy"], [18, 291]),
    ("Semantic Economy Institute", "institution", ["semantic economy institute"], []),
    ("Operative Semiotics", "concept", ["operative semiotics"], []),
    ("AXN", "protocol", ["axn", "axn identifier"], []),
    ("The Mandala Oracle", "concept", ["mandala oracle"], []),
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

    alias_of = {}

    def norm(a):
        a = re.sub(r"\s*\(.*?\)\s*", " ", a.lower()).strip()
        return re.sub(r"^the\s+", "", a)

    def add(name, typ, aliases, deposits, source, relation="archive", extra=None, firm=False, only_new=False):
        name = MERGE.get(name.strip().lower(), name.strip())
        # MERGE ON A SHARED ALIAS (v0.2): "SPXI (Semantic Packet ...)" from /non and the core "SPXI" are one entity.
        k = next((alias_of[norm(a)] for a in [name] + list(aliases) if norm(a) in alias_of), None)
        if k and only_new:
            return            # an index term naming an entity already registered adds nothing to it
        k = k or eid(name)
        r = ents.setdefault(k, {"id": k, "name": name, "type": typ, "relation": relation, "aliases": [], "defining_deposits": [], "seeded_from": []})
        for a in [name] + list(aliases):
            if a and a.lower() not in [x.lower() for x in r["aliases"]]:
                r["aliases"].append(a)
            if a:
                alias_of.setdefault(norm(a), k)
        for d in deposits:
            if d is not None and d not in r["defining_deposits"]:
                r["defining_deposits"].append(d)
        if source not in r["seeded_from"]:
            r["seeded_from"].append(source)
        # TYPE PRECEDENCE: a firm type (a person register, a stated /non subtype) replaces a default one.
        if firm or r["type"] in (None, "unknown"):
            if typ and not (r.get("_firm") and not firm):
                r["type"] = typ
            if firm:
                r["_firm"] = True
        if extra:
            r.update({k2: v for k2, v in extra.items() if k2 not in r})
    for name, typ, al, deps in CORE:
        add(name, typ, al, deps, "core")
    for p in sorted((ROOT / "datasets/heteronyms/records").glob("*.json")):
        h = json.loads(p.read_text(encoding="utf-8"))
        it = h.get("identity_type")
        if it in ("heteronym", "heteronym_aperture", "external_heteronym", "orthonym", "institutional_persona"):
            bare = re.sub(r"^(Rev\.|Dr\.|Prof\.)\s+", "", h["name"]).strip()
            add(h["name"], "institution" if it == "institutional_persona" else "person", [bare, p.stem.replace("-", " ")],
                [], f"heteronym record {p.stem}", extra={"heteronym": it != "orthonym", "identity_type": it}, firm=True)
    ne = json.loads((ROOT / "data/named-entities.json").read_text(encoding="utf-8"))
    for n in ne["entities"]:
        add(n["name"], "person", [], [], "named-entities", relation="external", extra={"wikidata": n.get("wikidata")}, firm=True)
    ni = json.loads((ROOT / "non/index.json").read_text(encoding="utf-8"))
    for row in ni.get("entities") or []:
        slug = isinstance(row, dict) and (row.get("entity") or row.get("slug"))
        if slug:
            m = re.search(r":\s*an?\s+([a-z ]+)\)", str(row.get("type") or ""))
            sub = {"person": "person", "work": "work", "event": "event", "product": "product"}.get((m.group(1).strip() if m else ""), None)
            if str(row.get("type") or "").startswith("E") and "protocol" in str(row.get("type")):
                sub = "protocol"
            add(row.get("name") or slug.replace("-", " "), sub or "concept", [slug.replace("-", " ")], [], f"/non {slug}",
                relation="external", firm=bool(sub))
    sites(add, ents)
    concepts_from_index(reg, add)
    for e in reg["entries"]:
        o = e.get("originator") or {}
        if o.get("name"):
            nm = re.split(r" \(", o["name"])[0]
            add(nm, o.get("entity_type") or "unknown", [], [], "originator", relation=o.get("relation") or "archive")
    concepts_from_addresses(reg, add, alias_of, norm)
    link_sites(ents)
    FIX = {"allen ginsberg": "person", "howl": "work"}   # /non entries whose type carries no subtype
    for r in ents.values():
        r.pop("_firm", None)
        t = FIX.get(re.sub(r"\s*\(.*?\)\s*", "", r["name"]).strip().lower())
        if t:
            r["type"] = t
        ds = sorted(d for d in (deposit_date(n) for n in r["defining_deposits"]) if d)
        r["created"] = ds[0] if ds else None
        r["created_basis"] = "earliest defining deposit" if ds else None
    return ents


# THE FLEET (v0.3, 2026-10-15). Every domain of data/fleet-domains.json is a SITE entity of its own, with the object it
# presents and its canonical deposit; "surface_of" names the registered entity it presents where its canonical deposit
# defines one. A site and its subject are kept apart: spxi.dev is not SPXI. The bare name (revelationfirst) is an alias
# where it is at least six characters.
def sites(add, ents):
    F = json.loads((ROOT / "data/fleet-domains.json").read_text(encoding="utf-8"))["domains"]
    for d in F:
        dom = d["domain"].strip().lower()
        bare = dom.rsplit(".", 1)[0]
        al = [dom, "www." + dom] + ([bare] if len(bare) >= 5 else [])
        dep = d.get("canonical_deposit")
        add(dom, "site", al, [dep] if dep else [], "fleet-domains", extra={"presents": d.get("object")})


def link_sites(ents):
    # surface_of: the registered (non-site) entity whose longest alias the "presents" text names
    cand = sorted(((a.lower(), r["id"]) for r in ents.values() if r["type"] != "site" for a in r["aliases"] if len(a) >= 4),
                  key=lambda x: -len(x[0]))
    for r in ents.values():
        if r["type"] == "site" and r.get("presents"):
            txt = r["presents"].lower()
            r["surface_of"] = next((k for a, k in cand if re.search(r"(?<![a-z0-9])" + re.escape(a) + r"(?![a-z0-9])", txt)), None)
        if r["type"] == "site" and r["name"] == "leesharks.com":      # "the author surface"
            r["surface_of"] = next((x["id"] for x in ents.values() if x["name"] == "Lee Sharks"), None)


# CONCEPTS FROM THE INDEX (v0.2, 2026-10-15). A term of data/entity-index.json enters the register only when a seated
# address names it, and it carries its defining deposit and that deposit's date (the entity's creation, which entails
# its prior state: ruling of 2026-09-19). Rule, mechanical and stated here: two or more words; not a phrase fragment or
# status marker; single words only where they are the archive's coinages (KEEP_SINGLE).
KEEP_SINGLE = {"patacinematics", "encyclotron", "dolphindiana", "tachyon", "dodecad"}
DROP = {"i am", "do not", "for machine", "blessed is", "the valuation", "the capture", "day and night", "new human 2",
        "demand 4", "what do you think about this", "what do you think of my account"}
WORKS = {"pearl and other poems", "secret book of walt", "day and night: conversations with sapphic desire", "socrates as orthonym",
         "epistle to the human diaspora", "i hereby abolish money", "paper roses", "made of rubies", "autonomous semantic warfare",
         "constitution of the semantic economy", "operative semiotics: a grundrisse", "in the crimson hexagon", "space ark"}
INST = re.compile(r"\b(journal|transactions|grammata|lab|authority|institute|commission|university|mint)\b", re.I)


def concepts_from_index(reg, add):
    C = json.loads((ROOT / "data/entity-index.json").read_text(encoding="utf-8"))["concepts"]
    qs = {re.sub(r'["“”]', "", o["q"]).lower() for e in reg["entries"] for o in [e] + (e.get("observations") or []) if o.get("q")}
    dates = {}
    for k, v in C.items():
        term = re.sub(r"\s*\(.*?\)\s*", " ", v.get("term") or k).strip()
        tl = term.lower()
        if v.get("type") == "status_marker" or tl in DROP:
            continue
        if len(tl.split()) < 2 and tl not in KEEP_SINGLE:
            continue
        if term.isupper() and len(tl.split()) <= 2:
            continue
        rx = re.compile(r"(?<![a-z0-9])" + re.escape(tl) + r"(?![a-z0-9])")
        if not any(rx.search(q) for q in qs):
            continue
        dep = v.get("defined_in")
        if dep not in dates:
            rp = ROOT / f"data/records/{dep}.json"
            dates[dep] = json.loads(rp.read_text(encoding="utf-8")).get("date") if dep and rp.exists() else None
        typ = "work" if tl in WORKS else "institution" if INST.search(term) else "concept"
        add(term, typ, [], [dep] if dep else [], "concept index", extra={"index_type": v.get("type"),
            "index_engagement": v.get("engagement_type")}, only_new=True)


_REC = {}


def records():
    if not _REC:
        for f in (ROOT / "data/records").glob("*.json"):
            try:
                r = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            if r.get("deposit_number") is not None:
                _REC[r["deposit_number"]] = r
    return _REC


def deposit_date(n):
    r = records().get(n)
    return r.get("date") if r else None


# CONCEPTS FROM THE ADDRESSES (v0.2). An address that names no registered entity is tried whole, and each quoted phrase in
# any address is tried, against the deposits: a defines_concepts entry is a DEFINING deposit (confirmed); a title, keyword
# or description containing the phrase is a CANDIDATE (the earliest is taken). A quoted phrase found nowhere is entered
# PROVISIONAL, its defining deposit not identified: the quotation is the target whatever the archive holds.
def concepts_from_addresses(reg, add, alias_of, norm):
    defs = collections.defaultdict(list)
    for n, r in records().items():
        for c in r.get("defines_concepts") or []:
            t = c if isinstance(c, str) else (c.get("term") or c.get("name") or "")
            if t:
                defs[t.strip().lower()].append(n)

    def find(ph):
        if ph in defs:
            return sorted(defs[ph], key=lambda n: deposit_date(n) or "9"), "confirmed (defines_concepts)"
        hits = []
        for n, r in records().items():
            for f in ("title", "keywords", "description"):
                v = r.get(f)
                v = " ".join(map(str, v)) if isinstance(v, list) else str(v or "")
                if ph in v.lower():
                    hits.append(n)
                    break
        return sorted(hits, key=lambda n: deposit_date(n) or "9"), "candidate (title, keywords or description)"
    seen, pending = set(), []
    for e in reg["entries"]:
        for o in [e] + (e.get("observations") or []):
            q = (o.get("q") or "").strip()
            if not q:
                continue
            quoted = [m.strip().lower() for m in re.findall(r'["“]([^"”]{4,80})["”]', q) if len(m.split()) >= 2]
            whole = re.sub(r'["“”]', "", q).strip().lower()
            pending.append((quoted, whole))
    # two passes: every quoted phrase first, then whole addresses, so "phase x marx" falls to Phase X
    for pass_quoted in (True, False):
        for quoted, whole in pending:
            for ph, is_quoted in ([(x, True) for x in quoted] if pass_quoted else [(whole, False)]):
                    ph = re.sub(r"\s+", " ", ph).strip(" ?.")
                    if not ph or ph in seen or ph in DROP or norm(ph) in alias_of or (not is_quoted and (len(ph.split()) > 5 or len(ph.split()) < 2)):
                        continue
                    # a whole address is tried only where it names no registered entity ("who is lee sharks" is Lee Sharks)
                    if not is_quoted and any(re.search(r"(?<![a-z0-9])" + re.escape(al) + r"(?![a-z0-9])", ph) for al in alias_of if len(al) >= 4):
                        continue
                    seen.add(ph)
                    deps, state = find(ph)
                    if deps:
                        add(ph, "concept", [], deps[:1], "address", extra={"definition_state": state, "other_deposits": deps[1:6]}, only_new=True)
                    elif is_quoted:
                        add(ph, "concept", [], [], "address", extra={"definition_state": "provisional (defining deposit not identified)"}, only_new=True)


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
    nrm = lambda a: re.sub(r"^the\s+", "", re.sub(r"\s*\(.*?\)\s*", " ", a.lower()).strip())
    lookup = {nrm(a): r["id"] for r in ents.values() for a in r["aliases"]}
    read = json.loads(READ.read_text(encoding="utf-8")) if READ.exists() else {}
    rows = []
    for e in reg["entries"]:
        obs = e.get("observations") or [e]
        o_name = re.split(r" \(", (e.get("originator") or {}).get("name") or "")[0]
        orig_id = lookup.get(nrm(MERGE.get(o_name.strip().lower(), o_name.strip()))) if o_name else None
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
