#!/usr/bin/env python3
"""The midrashim transform as an executable: a seed read from a seated text, operators applied to it in a declared order, an emission predicted,
and the emission checked against the seated target and against controls. Nothing is asserted that the run does not show.

A seed is one or more verses with MEMBERS, each a named piece of wording given as a pattern over the Greek with accents and case removed.
An operator changes the list of members. The emission is the list after the last operator: which members are kept and in what order, which are
dropped, which are replaced, what marker is added. The target passes a check when the seated verse shows that. Controls are other verses (the
Septuagint source, the Synoptic parallel, the upstream text) scored against the same emission: a control that scores as well as the target is an
equally good source or an equally good borrower, and the run says so.
    python3 midrash.py <alexanarch root> <derivations.json> <out.json>"""
import sys, re, json, unicodedata, pathlib, functools
OPS = {
 "PARTITION":          "keep some members of the seed's sentence and drop the others; another borrower may keep what this one drops",
 "REORDER":            "set the kept members in a new order",
 "SUBSTITUTE":         "replace one member by another of the same function (a word for a word)",
 "SUBSTITUTE-OBJECT":  "keep the verb and its frame and change the object it acts on",
 "TRANSFER-ATTRIBUTE": "move an attribute from the figure of the vision to a figure of the narrative",
 "EVENT":              "set a sign of the vision as an event at a hinge of the narrative (no change of wording; the change is of place)",
 "CITE-AS-SCRIPTURE":  "mark the member as written: the borrower reports as scripture what the seed says",
 "CITE-AS-PROMISE":    "change of who speaks: what the seed says in the first person as a promise, the borrower refers to as a promise already given",
 "REVERSE-DOER":       "keep the deed and its object and change who does it, from the adversary to the Christ or back",
 "UNDO":               "remove the seed's 'no more': what a judgment takes away is present in the borrower",
 "STATION":            "make one into several, each answerable for itself (one lampstand of seven lamps into seven lampstands)",
 "HIDE":               "what the source says is not known, the borrower says is hidden and promised",
 "ADD":                "add a member the seed does not have (recorded, so that an addition is never silent)",
 "NEGATE":             "deny for the borrower's own what the seed inflicts: the harm stays in the words and a 'not' is set on it",
}
def norm(s):
    s = unicodedata.normalize("NFD", s); s = "".join(c for c in s if not unicodedata.combining(c)).lower().replace("ς", "σ")
    return re.sub(r"[^α-ω ]+", " ", s)
class Seats:
    def __init__(self, root): self.C = pathlib.Path(root) / "data/corpora"
    @functools.lru_cache(None)
    def _lines(self, corpus):
        d, seen = {}, {}
        for p in sorted((self.C / corpus / "text").glob("*.txt")):
            for l in p.read_text(encoding="utf-8", errors="ignore").splitlines():
                if "\t" in l:
                    r, t = l.split("\t", 1); n = seen[r.strip()] = seen.get(r.strip(), 0) + 1
                    d.setdefault(r.strip(), t.strip()); d[f"{r.strip()}#{n}"] = t.strip()   # a ref met twice in one seat (Philo's two books of the Life of Moses): '#2' is the second
                    d.setdefault("".join(c for c in unicodedata.normalize("NFD", r.strip()) if not unicodedata.combining(c)), t.strip())
        return d
    @functools.lru_cache(None)
    def _orig(self, corpus):
        d = {}
        for p in sorted((self.C / corpus / "text").glob("*.txt")):
            for l in p.read_text(encoding="utf-8", errors="ignore").splitlines():
                if "\t" in l:
                    r, t = l.split("\t", 1)
                    if re.search(r"\d+:\d+$", r.strip()): d.setdefault(r.strip(), t.strip())
        return d
    def get(self, loc):
        corpus, ref = loc.split(":", 1); L = self._lines({"gnt": "gnt-nestle1904", "lxx": "lxx-swete", "philo": "philo"}[corpus])
        refs = []
        for part in ref.split(" + "):
            m = re.match(r"(.+ \d+:)(\d+)-(\d+)$", part) or re.match(r"(.+ )(\d+)-(\d+)$", part)
            refs += [f"{m.group(1)}{i}" for i in range(int(m.group(2)), int(m.group(3)) + 1)] if m else [part]
        missing = [r for r in refs if r not in L]; assert not missing, ("not in seat", loc, missing)
        return " ".join(L[r] for r in refs)
def run(D, S):
    seed_text = S.get(D["seed"]); ns = norm(seed_text); M = {m["id"]: m for m in D["members"]}
    seed_check = {k: bool(re.search(m["rx"], ns)) for k, m in M.items() if m.get("in_seed", True)}
    state = [k for k, m in M.items() if m.get("in_seed", True)]; state.sort(key=lambda k: re.search(M[k]["rx"], ns).start() if re.search(M[k]["rx"], ns) else 10**6)
    dropped, marker, absent_rx, required, trace = [], None, [], [], [{"op": "SEED", "state": list(state)}]
    for st in D["steps"]:
        op = st["op"]; assert op in OPS, op
        if op == "PARTITION": dropped += [k for k in state if k not in st["keep"]]; state = [k for k in state if k in st["keep"]]
        elif op == "REORDER": assert sorted(st["order"]) == sorted(state), (D["id"], st["order"], state); state = list(st["order"])
        elif op in ("SUBSTITUTE", "SUBSTITUTE-OBJECT", "TRANSFER-ATTRIBUTE", "REVERSE-DOER", "STATION", "HIDE"):
            i = state.index(st["old"]); state[i] = st["new"]; dropped.append(st["old"])
        elif op == "ADD": state.insert(st.get("at", len(state)), st["new"])
        elif op in ("CITE-AS-SCRIPTURE", "CITE-AS-PROMISE"): marker = st["marker"]
        elif op == "NEGATE": required.append(st["negation"])
        elif op == "UNDO": absent_rx.append(st["negation"]); assert re.search(st["negation"], ns), (D["id"], "the seed has no such negation")
        trace.append({"op": op, "does": OPS[op], **{k: v for k, v in st.items() if k != "op"}, "state": list(state)})
    def score(loc):
        t = S.get(loc) if isinstance(loc, str) else loc[1]; nt = norm(t); pos = {k: (re.search(M[k]["rx"], nt).start() if re.search(M[k]["rx"], nt) else None) for k in state}
        present = [k for k in state if pos[k] is not None]; at, ordered = 0, True
        for k in state:      # the emitted order holds if each member can be found after the one before it
            mm = re.compile(M[k]["rx"]).search(nt, at)
            if not mm: ordered = False; break
            at = mm.start() + 1
        checks = {"kept members present": (len(present), len(state)),
                  "in the emitted order": (int(ordered), 1) if len(state) > 1 and not D.get("unordered") else None,
                  "dropped members absent": (sum(1 for k in dropped if not re.search(M[k]["rx"], nt)), len(dropped)) if dropped else None,
                  "marker present": (int(bool(re.search(marker, nt))), 1) if marker else None,
                  "negation absent": (sum(1 for r in absent_rx if not re.search(r, nt)), len(absent_rx)) if absent_rx else None,
                  "the borrower's 'not' present": (sum(1 for r in required if re.search(r, nt)), len(required)) if required else None}
        checks = {k: v for k, v in checks.items() if v}
        got, of = sum(v[0] for v in checks.values()), sum(v[1] for v in checks.values())
        return {"loc": loc if isinstance(loc, str) else loc[0], "text": t, "checks": checks, "score": round(got / of, 2), "passes": got == of, "missing": [k for k in state if pos[k] is None],
                "kept_but_should_be_dropped": [k for k in dropped if re.search(M[k]["rx"], nt)]}
    out = {"id": D["id"], "title": D["title"], "family": D["family"], "seed": {"loc": D["seed"], "text": seed_text, "members_found": seed_check},
           "members": {k: {"gloss": m["gloss"], "greek": m["greek"]} for k, m in M.items()}, "trace": trace, "emission": {"members": state, "dropped": dropped, "marker": marker, "negation_removed": bool(absent_rx), "negation_set": bool(required)},
           "target": score(D["target"]), "controls": [dict(score(c["loc"]), label=c["label"]) for c in D.get("controls", [])], "note": D.get("note"), "records": D.get("records", [])}
    # the search: every verse of the seated New Testament outside Revelation, and every verse of the seated Septuagint, scored against the same emission
    mr = re.search(r"(\d+)-(\d+)$", D["target"]); tv = (int(mr.group(2)) - int(mr.group(1)) + 1) if mr else 1; hits = {}
    for corpus, name in (("gnt-nestle1904", "new_testament"), ("lxx-swete", "septuagint")):
        seedrefs = set(re.findall(r"[A-Za-z0-9]+ \d+:\d+", D["seed"]))
        L = [(r, t) for r, t in S._orig(corpus).items() if r not in seedrefs]
        L = list(dict(L).items()); found = []
        for i, (r, t) in enumerate(L):
            txt = t if tv == 1 else " ".join(x[1] for x in L[i:i + tv])
            if score((r, txt))["passes"]: found.append(r)
        hits[name] = {"verses_searched": len(L), "passing": len(found), "refs": found[:12]}
    out["search"] = hits
    out["seed_ok"] = all(seed_check.values()); best = max([c["score"] for c in out["controls"]], default=0)
    out["verdict"] = ("seed not as declared" if not out["seed_ok"] else "target fails the emission" if not out["target"]["passes"] else
                      "passes; a control passes as well" if any(c["passes"] for c in out["controls"]) else "passes; no control passes" + (f" (best control {best})" if out["controls"] else " (no control set)"))
    return out
if __name__ == "__main__":
    S = Seats(sys.argv[1]); DS = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")); R = [run(d, S) for d in DS["derivations"]]
    json.dump({"engine": __doc__, "operators": OPS, "frozen": DS["frozen"], "runs": R}, open(sys.argv[3], "w"), ensure_ascii=False, indent=1)
    for r in R: print(f"{r['id']:26} {r['target']['score']:>4}  controls {[c['score'] for c in r['controls']]}  {r['verdict']}" + ("" if r["seed_ok"] else f"  SEED {r['seed']['members_found']}"))
