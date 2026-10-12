#!/usr/bin/env python3
"""Give title and concept runs their `intended` record (repair, 2026-10-12).

`intended` (operator, 2026-10-11) is the record a title or identifier run was meant to reach, linked
whether or not the composition cites it. Seated only on 15 captures, by hand. Two rules, nothing guessed:
  1. TITLE RUN — the issued string (operators, 'what is'/'tell me about', quotes and '?' removed) is a
     deposit's whole main title (before its first ':' / '—', ids and parentheticals removed), or its whole
     title, or a title quoted at length (40+ characters) that the deposit resolver matches; version series
     go to the record of standing their supersession names.
  2. CONCEPT RUN — the string is a concept exactly one deposit both defines (defines_concepts) and carries in
     its title. A concept defined in passing elsewhere does not count: 'lee sharks' is defined in Antioch.
A string that both rules resolve, to different deposits, is left alone. reached = the deposit is among the
capture's card-derived related_deposits; absent when the capture's cards were never extracted (unknown).
"""
import json, re, sys, pathlib, collections
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT))
import capture_deposit_links as L, wire_deposit as w
CANON = ROOT / "data/EA-WG-CAPTURES-01.json"
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]; idx = L.Index(R)
N = L.norm


def qtitle(q):
    q = re.sub(r"\b(?:site|alexanarch|academia|medium|zenodo):\S*\s*", "", q or "", flags=re.I).strip()
    q = re.sub(r"^(what is|who is|define|tell me about|what does)\s+(the\s+)?", "", q, flags=re.I)
    return q.strip(' "“”?')


def main_title(t):
    t = re.sub(r"\([^)]*\)", " ", L.strip_ids(t or ""))
    return N(L.SEG.split(t)[0])


defs = collections.defaultdict(set)
for d in R:
    for c in d.get("defines_concepts") or []:
        k = N(c.get("concept") if isinstance(c, dict) else c)
        if k: defs[k].add(d["deposit_number"])


def title_run(q, date):
    t = qtitle(q); k = N(t)
    n, b, _ = idx.resolve({"title": t}, date)
    if n is None: return None
    d = idx.by_n[n]
    if k in (main_title(d["title"]), N(L.strip_ids(d["title"]))) or len(k) >= 40: return n
    if "capture date" in b and N(L.strip_ids(d["title"])).startswith(k):
        return n                     # the only deposit of that title that existed when the run was made
    same = {idx.standing(c) for c in (_ or []) if k == main_title(idx.by_n[c]["title"])}
    return same.pop() if len(same) == 1 else None


def concept_run(q):
    k = N(qtitle(q))
    if len(k) < 6: return None
    # the concept must sit inside one segment of the title: 'SPXI: Protocol and ETF Disambiguation' does not carry 'spxi protocol'
    def carries(t):
        return any(re.search(r"(^| )" + re.escape(k) + r"( |$)", N(g)) for g in L.SEG.split(L.strip_ids(t)))
    hits = {idx.standing(n) for n in defs.get(k, ()) if carries(idx.by_n[n]["title"])}
    return hits.pop() if len(hits) == 1 else None


def main():
    write = "--write" in sys.argv
    reg = json.loads(CANON.read_text(encoding="utf-8")); rows = []
    for e in reg["entries"]:
        if e.get("intended"): continue
        a, c = title_run(e["q"], e.get("date")), concept_run(e["q"])
        n, basis = (a, "title run") if a and (not c or c == a) else ((c, "concept run") if c and not a else (None, None))
        if not n: continue
        d = idx.by_n[n]; s, ex = w.search_title_urls(d)
        rows.append((e["slug"], e["q"], n, basis, d["title"]))
        if write:
            e["intended"] = {"deposit": n, "axn": d["axn"], "title": d["title"], "record": f"https://www.alexanarch.org/s/records/{n}/",
                             "search": s, "search_exact": ex, "reached": n in (e.get("related_deposits") or []),
                             "basis": basis + " (derived 2026-10-12, rebuild/capture-registry/repair-20261012-extract-cards/intended_runs.py)"}
    for r in rows: print(f"{r[0][:46]:46} | {r[1][:44]:44} → #{r[2]} [{r[3]}] {r[4][:60]}")
    print(len(rows), "captures given an intended record")
    if write: CANON.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8"); print("written")


if __name__ == "__main__":
    main()
