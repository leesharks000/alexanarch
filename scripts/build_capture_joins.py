#!/usr/bin/env python3
"""build_capture_joins.py — every observation returns to the work, entity and surface it concerns (2026-10-14).

WORKPLAN-2026-10-14-CAPTURE-JOIN v0.2, on the operator's go. The join is DERIVED and rebuilt at every seat; it writes
nothing into the seated records and leaves the capture schema as it is (AGENTS §6: adding is safe, touching is not).

THE UNIT is the observation (its obs_id). Records, deposit pages, /non entries and surfaces aggregate observations; none
merges them.

TWO KINDS OF RELATION.
  source        read off the card, exact, confirmed on derivation:
                  appeared_in surface:<domain>   a card's host is a fleet domain (or a chip's label maps to one: candidate)
                  appeared_in deposit:<n>        the card resolved to a deposit at intake (link_cards), or the card's
                                                 title is a fleet page's own title and that page declares the record
  derived       what an instrument did to the observation: held_by instrument:0.9, held_by instrument:0.8,
                scored_by instrument:0.6 (where PER is scored)
  interpretive  decided by reading: about non:<entity>, represents_faithfully / distorts (with finding and excerpt),
                mentions_instrument, mentions deposit, corrected_by non:<entity>, pair_of observation:<obs_id>.
                Proposed as candidates by rule (defining papers, issued strings); asserted or decided in
                data/capture-joins-decisions.json, which records rejection as well as confirmation.

Each relation's id is a hash of (obs_id, verb, object, basis). A decision binds to that id and to the evidence revision
it was read against; if the basis changes, the relation is new and returns for reading, and the old decision stays.
States are inventory (unjoined, candidate, confirmed, rejected) and block nothing.

RENDER SCOPE. Until the first circuit is verified live, projections render only the observations named in the decisions
file's `render_scope`. Widening the scope is one edit there.

Writes data/capture-joins.json and data/surface-joins/<domain>.json.
"""
import hashlib, html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
OUT = ROOT / "data/capture-joins.json"
DEC = ROOT / "data/capture-joins-decisions.json"
SURF_DIR = ROOT / "data/surface-joins"
BASE = "https://www.alexanarch.org"

# chips that show a site label and no host: label → fleet domain (candidates until read)
LABELS = {"Semantic Packet for eXchange & Indexing": "spxi.dev", "Alexanarch": "alexanarch.org", "Lee Sharks": "leesharks.com"}
# an entity's surface: where its block renders
ENTITY_SURFACE = {"spxi": "spxi.dev"}
INSTRUMENT = {"0.6": "Provenance Erasure Rate", "0.8": "Semantic Addresses Framework", "0.9": "Capture Registry",
              "0.10": "Conformance Instrument", "0.15": "Platform Erosion Observatory", "5.4": "Canary Registry"}


def rid(obs_id, verb, obj, basis):
    return "REL-" + hashlib.sha1(f"{obs_id}|{verb}|{obj}|{basis}".encode()).hexdigest()[:12]


def host(s):
    s = (s or "").strip().lower()
    s = re.sub(r"^https?://", "", s).split("/")[0]
    return s[4:] if s.startswith("www.") else s


def observations(e):
    """(obs, is_root) for each observation of an entry; the root is observation 1 when no list exists."""
    obs = e.get("observations") or []
    if not obs:
        yield dict(e, obs_slug=e["slug"]), True
        return
    for o in obs:
        merged = dict(e); merged.update(o); merged["obs_slug"] = o.get("slug") or e["slug"]
        merged["obs_id"] = o.get("obs_id") or e.get("obs_id")
        yield merged, False


def fleet_pages():
    """title → (url, record) for fleet pages read locally; the circuit indexes spxi.dev."""
    out = {}
    root = ROOT.parent / "spxi-dev"
    for p in root.glob("**/index.html"):
        if "node_modules" in p.parts:
            continue
        s = p.read_text(encoding="utf-8", errors="replace")
        t = re.search(r"<title>([^<]+)</title>", s)
        rec = re.search(r'"sameAs":\s*"https?://(?:www\.)?alexanarch\.org/s/records/(\d+)/?"', s)
        rel = p.parent.relative_to(root).as_posix()
        url = "https://www.spxi.dev/" + ("" if rel == "." else rel)
        if t:
            out[html.unescape(t.group(1)).strip()] = (url, int(rec.group(1)) if rec else None)
    return out


def non_entities():
    """entity → (defining deposits, issued strings), from the /non rows and their ledgers."""
    out = {}
    for f in sorted((ROOT / "datasets/negative-of-the-negative/v2/rows").glob("*.json")):
        r = json.loads(f.read_text(encoding="utf-8"))
        try:
            L = json.loads((ROOT / r["ledger"]["archive"]).read_text(encoding="utf-8"))
        except Exception:
            continue
        cl = L["claims"] if isinstance(L, dict) else L
        defin = {int(c["dep"]) for c in cl if str(c.get("dep")).isdigit() and c.get("kernel")}
        addrs = {a.strip().lower() for a in ([r.get("address")] + list(r.get("addresses") or [])) if a}
        out[f.stem] = (defin, addrs)
    return out


def main():
    reg = json.loads(REG.read_text(encoding="utf-8"))
    dec = json.loads(DEC.read_text(encoding="utf-8")) if DEC.exists() else {"decisions": [], "asserted": [], "render_scope": []}
    domains = {d["domain"] for d in json.loads((ROOT / "data/fleet-domains.json").read_text(encoding="utf-8"))["domains"]}
    pages = fleet_pages()
    ents = non_entities()
    rels, seen_obs = [], {}

    def add(o, verb, obj, basis, kind, state, evidence=None):
        r = {"id": rid(o["obs_id"], verb, obj, basis), "obs_id": o["obs_id"], "entry": o["slug"], "obs_slug": o["obs_slug"],
             "date": o.get("date"), "surface": o.get("surface"), "q": o.get("q"), "verb": verb, "object": obj, "basis": basis,
             "kind": kind, "state": state}
        if evidence:
            r["evidence"] = evidence
        rels.append(r)

    for e in reg["entries"]:
        for o, _ in observations(e):
            if not o.get("obs_id"):
                continue
            seen_obs[o["obs_id"]] = o
            for c in o.get("cite_list") or []:
                h = host(c.get("site"))
                card = {"n": c.get("n"), "site": c.get("site"), "title": c.get("title"), "url": c.get("url")}
                if h in domains:
                    add(o, "appeared_in", f"surface:{h}", "card host", "source", "confirmed", card)
                elif c.get("site") in LABELS:
                    add(o, "appeared_in", f"surface:{LABELS[c['site']]}", "chip label", "source", "candidate", card)
                if isinstance(c.get("deposit"), int):
                    add(o, "appeared_in", f"deposit:{c['deposit']}", f"card resolved at intake ({c.get('deposit_basis')})", "source", "confirmed", card)
                t = (c.get("title") or "").strip()
                if t in pages:
                    url, rec = pages[t]
                    if rec:
                        add(o, "appeared_in", f"deposit:{rec}", f"card title is {url}'s own title; the page declares #{rec}", "source", "confirmed", dict(card, page=url))
            add(o, "held_by", "instrument:0.9", "seated in the Capture Registry", "derived", "confirmed")
            add(o, "held_by", "instrument:0.8", "keyed to its semantic address", "derived", "confirmed")
            if o.get("per") is not None:
                add(o, "scored_by", "instrument:0.6", f"PER {o.get('per')}", "derived", "confirmed")
            rel_dep = set(n for n in (o.get("related_deposits") or []) if isinstance(n, int))
            q = (o.get("q") or "").strip().lower()
            for ent, (defin, addrs) in ents.items():
                hit = sorted(rel_dep & defin)
                if q in addrs:
                    add(o, "about", f"non:{ent}", "issued string of the entity", "interpretive", "candidate")
                elif len(hit) >= 2:
                    add(o, "about", f"non:{ent}", "defining papers " + ", ".join(f"#{n}" for n in hit[:6]), "interpretive", "candidate")

    # decisions on proposed relations; asserted readings (relations a reader states, with finding and excerpt)
    by_id = {r["id"]: r for r in rels}
    for a in dec.get("asserted", []):
        o = seen_obs.get(a["obs_id"])
        assert o, a["obs_id"]
        if a.get("excerpt"):
            assert a["excerpt"] in (o.get("transcript") or ""), ("excerpt not in transcript", a["obs_id"], a["excerpt"])
        r = {"id": rid(a["obs_id"], a["verb"], a["object"], a["basis"]), "obs_id": a["obs_id"], "entry": o["slug"], "obs_slug": o["obs_slug"],
             "date": o.get("date"), "surface": o.get("surface"), "q": o.get("q"), "verb": a["verb"], "object": a["object"], "basis": a["basis"],
             "kind": "interpretive", "state": "confirmed", "decision": {k: a[k] for k in ("reader", "date", "revision") if k in a}}
        for k in ("finding", "excerpt"):
            if a.get(k):
                r[k] = a[k]
        if r["id"] not in by_id:
            rels.append(r); by_id[r["id"]] = r
    for d in dec.get("decisions", []):
        r = by_id.get(d["id"])
        if r is None:
            continue  # basis changed: the decision stays as history in the decisions file
        r["state"] = d["decision"]; r["decision"] = {k: d[k] for k in ("reader", "date", "reason", "revision") if k in d}

    joined = {r["obs_id"] for r in rels if r["kind"] != "derived" and r["state"] == "confirmed"}
    inv = {"observations": len(seen_obs), "joined_confirmed": len(joined), "unjoined": len(seen_obs) - len(joined),
           "relations": len(rels), "by_state": {}, "by_verb": {}}
    for r in rels:
        inv["by_state"][r["state"]] = inv["by_state"].get(r["state"], 0) + 1
        inv["by_verb"][r["verb"]] = inv["by_verb"].get(r["verb"], 0) + 1
    scope = set(dec.get("render_scope", []))
    out = {"name": "Capture joins: observations to deposits, /non entities, surfaces and instruments", "derived_from": f"EA-WG-CAPTURES-01 v{reg.get('version')}",
           "rule": "Source relations are read off the card and confirmed; interpretive relations are decided by reading; every relation carries its observation's identity. Projections render confirmed relations within render_scope.",
           "render_scope": sorted(scope), "inventory": inv, "relations": rels}
    # one relation per line: the file diffs by relation, and stays a fraction of the indented size
    head = json.dumps({k: v for k, v in out.items() if k != "relations"}, ensure_ascii=False, indent=1)[:-2]
    OUT.write_text(head + ',\n "relations": [\n' + ",\n".join(json.dumps(r, ensure_ascii=False) for r in rels) + "\n ]\n}\n", encoding="utf-8")

    # one file per surface: rows for observations in scope that appeared in the surface or are about its entity
    SURF_DIR.mkdir(parents=True, exist_ok=True)
    surfaces = {}
    for r in rels:
        if r["state"] != "confirmed" or r["obs_id"] not in scope:
            continue
        if r["verb"] == "appeared_in" and r["object"].startswith("surface:"):
            surfaces.setdefault(r["object"][8:], set()).add(r["obs_id"])
        if r["verb"] == "about" and r["object"].startswith("non:") and r["object"][4:] in ENTITY_SURFACE:
            surfaces.setdefault(ENTITY_SURFACE[r["object"][4:]], set()).add(r["obs_id"])
    for dom, ids in surfaces.items():
        rows = []
        for oid in ids:
            o = seen_obs[oid]
            mine = [r for r in rels if r["obs_id"] == oid and r["state"] == "confirmed"]
            f = next((r for r in mine if r["verb"] in ("distorts", "represents_faithfully")), None)
            rows.append({"obs_id": oid, "date": o.get("date"), "engine": o.get("surface"), "q": o.get("q"), "auth": o.get("auth"),
                         "observation": f"{BASE}/captures/{o['slug']}/#{o['obs_slug']}",
                         "verdict": f["verb"] if f else None, "finding": f.get("finding") if f else None, "excerpt": f.get("excerpt") if f else None,
                         "appeared_in": sorted({r["object"] for r in mine if r["verb"] == "appeared_in"}),
                         "non": sorted({r["object"][4:] for r in mine if r["verb"] in ("about", "corrected_by") and r["object"].startswith("non:")}),
                         "instruments": sorted({(r["verb"], r["object"][11:]) for r in mine if r["object"].startswith("instrument:")}),
                         "pairs": [{"obs_id": p, "observation": f"{BASE}/captures/{seen_obs[p]['slug']}/#{seen_obs[p]['obs_slug']}"}
                                   for p in sorted({r["object"][12:] for r in mine if r["verb"] == "pair_of"}) if p in seen_obs]})
        rows.sort(key=lambda x: (x["date"] or "", x["obs_id"]), reverse=True)
        (SURF_DIR / f"{dom}.json").write_text(json.dumps({"surface": dom, "as_of": reg.get("date"), "registry_version": reg.get("version"),
                                                          "source": f"{BASE}/data/capture-joins.json", "rows": rows}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"capture joins: {inv['observations']} observations, {inv['relations']} relations, {inv['joined_confirmed']} joined (confirmed), "
          f"{inv['unjoined']} unjoined; states {inv['by_state']}; surfaces in scope: {', '.join(f'{d} ({len(i)})' for d, i in surfaces.items()) or 'none'}")


if __name__ == "__main__":
    main()
