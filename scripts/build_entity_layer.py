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
    works_from_deposits(reg, add, alias_of, norm)
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
# where it is at least five characters; it carries the fleet's alternate domains (operator, 2026-10-15: ".org is my
# domain too, theres quite a few that have multiple"), so revelationfirst.org counts to revelationfirst.com.
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


# WORKS FROM THE DEPOSITS (v0.4, ruling 2026-10-15: "a specific article, poem, book, or work is also an entity ... when a
# capture is discussing the article or deposit itself, rather than simply pulling on its ideas, that is an entity").
# A deposit is a work entity when an address names its full title, quotes its title, or names its main title (before the
# colon, three or more words) with framing that points at a work. All deposits of one title are one work. A main title
# that is the archive's own name is never taken for a work.
WORK_FRAME = re.compile(r"\b(arguments in|full text|read and characteri[sz]e|the (epic )?poem|essay|book|paper|article|treatise|"
                        r"deposit|monograph|letter|edition|\bby [a-z])", re.I)


def works_from_deposits(reg, add, alias_of, norm):
    titles = collections.defaultdict(list)
    for n, r in records().items():
        t = (r.get("title") or "").strip()
        if t:
            titles[t].append(n)
    archive_names = {"crimson hexagonal archive", "crimson hexagon", "crimson hexagonal", "alexanarch", "the crimson hexagon"}
    qs = {o["q"] for e in reg["entries"] for o in [e] + (e.get("observations") or []) if o.get("q")}
    for q in qs:
        ql = re.sub(r"[“”\"]", "", q).lower()
        quoted = [m.lower() for m in re.findall(r'["“]([^"”]{8,300})["”]', q)]
        framed = bool(WORK_FRAME.search(q))
        best = None
        for t, deps in titles.items():
            tl, main = t.lower(), re.split(r":\s", t, 1)[0].strip().lower()
            if len(tl) >= 8 and (tl in ql or any(tl.startswith(x) and len(x) >= 20 for x in quoted)):
                hit = tl
            elif len(main.split()) >= 3 and main in ql and main not in archive_names and (framed or any(main == x for x in quoted)):
                hit = main
            else:
                continue
            if not best or len(hit) > len(best[0]):
                best = (hit, t, deps)
        if best:
            hit, t, deps = best
            deps = sorted(deps, key=lambda n: deposit_date(n) or "9")
            main = re.split(r":\s", t, 1)[0].strip()
            add(t, "work", [main] if len(main.split()) >= 3 else [], deps, "deposit title", extra={"deposits": deps[:12]})


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


# THE PRIMARY TARGET IS THE MOST SPECIFIC ENTITY NAMED (v0.4): a work before its concepts, a concept before the person
# or site that carries it, the archive last; position in the address breaks ties.
RANK = {"work": 0, "concept": 1, "dataset": 1, "protocol": 1, "product": 1, "event": 1, "institution": 2, "person": 3, "site": 4, "archive": 5}
TYPE = {}


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
    out = [{"ent": k, "basis": "address"} for k in sorted(keep, key=lambda k: (RANK.get(TYPE.get(k), 3), found[k][0][0]))]
    # The originator says whose entity the capture concerns (the owner), not what the query aims at: it is the target
    # only where the address names no registered entity.
    if not out and orig_id:
        out = [{"ent": orig_id, "basis": "originator (operator-recorded); the address names no registered entity"}]
    return out


VERBS = [("read and characterize", r"\bread and characteri[sz]e"), ("track the development", r"\btrack\b"), ("work thru", r"\bwork (thru|through)\b"),
         ("walk me thru", r"\bwalk me (thru|through)\b"), ("full index", r"\bfull index\b"), ("evaluate / status", r"\b(evaluat|status of)"),
         ("why", r"^\s*why\b"), ("what is / who is", r"^\s*(what|who)('s| is| are| was)\b"), ("tell me about", r"\btell me about\b"), ("whats this", r"\bwhats? this\b")]


# REACHED FROM THE MACHINE TEXT (v0.4, 2026-10-15). The key is built from the composition itself: the first answer only
# (what an unprimed reader receives), the query echo and the transcript's own wrapper removed. Decided, with the evidence
# quoted, where the text is unambiguous; everything else is routed to reading, never guessed:
#   same       the target's name or an alias is held in the first answer, no refusal, no namesake beside it
#   substitute a near-spelling of the target (Crane for Cranes) or a recorded namesake appears and the target does not
#   collision  the target and a recorded namesake both appear in the first answer
#   refused    the first answer says it found nothing, or declines
#   unread     the target's name is absent with no refusal and no namesake (generic or substitute: a reading decides),
#              or there is no transcript
REFUSAL = re.compile(r"\b(i (couldn['’]t|could not|can['’]t|cannot|was unable to|wasn['’]t able to) (find|locate|identify|verify|access)|"
                     r"i (don['’]t|do not) have (any )?(information|reliable)|no (reliable|widely|credible|verifiable) (information|sources?|record)|"
                     r"(doesn['’]t|does not|did not) (appear|seem) to (exist|be (a |an )?(widely|well|recognized|known|established))|"
                     r"i['’]m not (aware|familiar)|not (a |an )?(widely )?(recognized|known|established) (term|concept|person|entity))", re.I)
TURN = re.compile(r"\[QUERENT[^\]]*turn [2-9][^\]]*\]|\*\*USER:\*\*|^You said:|\[ANSWER [2-9]\]", re.M)
START = re.compile(r"\[ANSWER 1\]|\*\*CHATGPT\*\*[^\n]*|ChatGPT said:|^You said:[^\n]*\n", re.M)


RECORDED_BAD = re.compile(r"COLLAPSE|SUBSTITUT|FRAGMENT|COLLISION|COLLIDE|GENERICI|HOMONYM|MISREAD|CONFLAT|DISPLACED|NOT REACHED|UNREACHED|REFUS|DECLIN|HALLUCINAT")
ARCHIVE_MARKERS = ["lee sharks", "sharks", "alexanarch", "crimson hexagon", "crimson hexagonal", "johannes sigil", "rebekah cranes",
                   "rex fraction", "ayanna vox", "jack feist", "sen kuro", "nobel glas", "damascus dancings", "talos morrow",
                   "semantic economy institute", "new human", "heteronym"]
CARD = re.compile(r"— (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, 20\d\d —|\b\d+ (hours?|days?|weeks?) ago\b|^\[www\.[^\]]+\]\(", re.M)
OCR_CHROME = re.compile(r"A[Il1] ?Overview|AI Mode|Al Mode", re.I)


def first_answer(t, q):
    if not t:
        return ""
    m = START.search(t)
    body = t[m.end():] if m else t
    n = TURN.search(body)
    body = body[:n.start()] if n else body
    body = re.sub(r"^\[[^\]]{0,400}\]\s*", "", body.strip())            # the transcript's own wrapper note
    c = CARD.search(body)                                               # the card rail: source cards, not the composition
    if c and c.start() > 80:
        body = body[:c.start()]
    m2 = OCR_CHROME.search(body[:500])                                  # an OCR read: the search box and tabs before the panel
    if m2:
        body = body[m2.end():]
    return body.replace(q, " ") if q else body


def variants(alias):
    w = alias.split()
    if len(w) < 2 or len(alias) < 8:
        return []
    last = w[-1]
    alt = last[:-1] if last.endswith("s") else last + "s"
    return [" ".join(w[:-1] + [alt])]


def reached_from_text(row, o, e, ents):
    tgt = ents.get(row["target"][0]["ent"])
    if not tgt:
        return None
    t = o.get("transcript") or (e.get("transcript") if o is not e and not e.get("observations") else None) or ""
    fa = first_answer(t, row["q"])
    if not fa.strip():
        return {"kind": "unread", "others": [], "basis": "no transcript", "state": "open"}
    low = fa.lower()
    find = lambda a: re.search(r"(?<![a-z0-9])" + re.escape(a.lower()) + r"(?![a-z0-9])", low)
    hit = next((a for a in sorted(tgt["aliases"], key=len, reverse=True) if len(a) >= 4 and find(a)), None)
    if row["target"][0]["basis"].startswith("originator"):
        return {"kind": "unread", "others": [], "basis": "the address names no entity; the owner stands as target and the text cannot decide: a reading decides", "state": "open"}
    near = next((v for a in tgt["aliases"] for v in variants(a) if find(v)), None) if tgt["type"] == "person" else None
    names = [c.get("with") for c in (o.get("collisions") or e.get("collisions") or []) if isinstance(c, dict) and c.get("with")]
    nm = next((n for n in names if find(re.split(r" \(|,", n)[0].strip())), None)
    ref = REFUSAL.search(fa[:1500])
    def q(a):
        i = low.find(a.lower()); return fa[max(0, i - 60): i + len(a) + 60].replace("\n", " ").strip()
    if ref and not hit:
        return {"kind": "refused", "others": [], "basis": "first answer: '" + fa[max(0, ref.start() - 40): ref.end() + 60].replace("\n", " ").strip() + "'", "state": "derived (machine text)"}
    if hit and (near or nm) and not (near and hit.lower() == near.lower()):
        return {"kind": "unread", "others": [x for x in (near, nm) if x], "basis": f"first answer holds '{hit}' and '{near or nm}': collision or disambiguation, a reading decides", "state": "open"}
    if hit and not ref:
        # a name held is not the entity reached: a concept may be composed in its common sense, a person or site may be
        # recorded by the registry's own reading as collapsed or collided
        rec = ((o.get("mt") or "") + " " + (o.get("d") or "")[:500]).upper()
        bad = RECORDED_BAD.search(rec)
        if bad:
            return {"kind": "unread", "others": [], "basis": f"first answer holds '{hit}' but the recorded reading says {bad.group(0)}: a reading decides", "state": "open"}
        if tgt["type"] in ("concept", "dataset", "protocol") and tgt.get("relation", "archive") == "archive" or tgt["type"] == "concept":
            tie = next((m for m in ARCHIVE_MARKERS if m not in hit.lower() and hit.lower() not in m and find(m)), None)
            if not tie:
                return {"kind": "unread", "others": [], "basis": f"first answer holds the term '{hit}' with no tie to its corpus (author, heteronym, archive, site): the archive's concept or the common sense, a reading decides", "state": "open"}
            return {"kind": "same", "others": [], "basis": f"first answer holds '{q(hit)}', tied to its corpus by '{tie}'", "state": "derived (machine text)"}
        return {"kind": "same", "others": [], "basis": "first answer holds the target: '" + q(hit) + "'", "state": "derived (machine text)"}
    if not hit and (near or nm):
        return {"kind": "substitute", "others": [near or nm], "basis": "first answer holds '" + q(near or nm) + "', not the target", "state": "derived (machine text)"}
    if hit and ref:
        return {"kind": "unread", "others": [], "basis": "first answer names the target and carries a refusal marker: a reading decides", "state": "open"}
    return {"kind": "unread", "others": [], "basis": "target's name absent from the first answer (generic, substitute or paraphrase): a reading decides", "state": "open"}


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
    TYPE.update({k: r["type"] for k, r in ents.items()})
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
            row["reached"] = {"kind": kind, "others": [x for x in others if x], "basis": basis, "state": "derived (recorded reading)" if kind != "unread" else "open"}
            if kind == "unread" and row["target"][0]["ent"] != "unassigned":
                row["reached"] = reached_from_text(row, o, e, ents) or row["reached"]
            elif kind == "unread":
                row["reached"]["basis"] = "no registered target"
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
    states = collections.Counter(r["reached"]["state"] for r in rows)
    print("reached states", dict(states))
    print(f"entity layer: {len(ents)} entities; {len(rows)} observations; unassigned {by_ent.get('unassigned', 0)}; "
          f"reached kinds {dict(kinds)}; read {sum(1 for r in rows if r['reached']['state'] == 'read')}")
    if check:
        return
    head = {"derived_from": f"EA-WG-CAPTURES-01 v{reg.get('version')}", "ruling": "Lee Sharks, 2026-10-15: target is the main anchor; no fidelity score on the wrong entity."}
    (ROOT / "data/entities.json").write_text(json.dumps({**head, "name": "Entity register of the Capture Registry", "count": len(ents),
        "entities": sorted(ents.values(), key=lambda r: (-r["observations_targeting"], r["name"]))}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    openrows = [r for r in rows if r["reached"]["state"] == "open"]
    openrows.sort(key=lambda r: (0 if "ChatGPT" in (r["surface"] or "") else 1, "" if not r["date"] else "".join(chr(255 - ord(c)) for c in r["date"])))
    (ROOT / "rebuild/entity-layer/reading-queue.json").write_text(json.dumps({**head, "name": "Reached relations awaiting a reading",
        "order": "ChatGPT first, then newest first", "count": len(openrows),
        "rows": [{"key": r["key"], "entry": r["entry"], "date": r["date"], "surface": r["surface"], "q": r["q"],
                  "target": r["target"][0]["ent"], "why_open": r["reached"]["basis"]} for r in openrows]}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (ROOT / "data/entity-relations.json").write_text(json.dumps({**head, "name": "Observation-to-entity relations", "count": len(rows),
        "reached_kinds": ["same", "weakened", "substitute", "collision", "generic", "refused", "unread"], "rows": rows}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main("--check" in sys.argv)
