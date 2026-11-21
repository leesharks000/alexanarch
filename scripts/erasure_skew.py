#!/usr/bin/env python3
"""erasure_skew.py — credit-scale Erasure Skew at intake, by codebook ES-CREDIT-v0
(rebuild/capture-registry/erasure-skew/CODEBOOK-ES-CREDIT-v0.md, frozen in FROZEN-ES-CREDIT-v0.sha256).

Ruling (Lee Sharks, 2026-11-21 13:47 / 13:52 EST): "yes, we go with that coding for now"; "add it as an intake option"; "add a
check for erasure skew calculation appropriateness at intake - not every capture needs erasure skew calculated."

The operators are #157 v3's (AXN:02F3): alpha_T, Pi_d split by power direction, Omega = cov(w, rho) / var(w) with a permutation
null. The unit is the CREDITED PARTY (the claim-scale Standing Rule, #1524/#1525: retention is survival of the claim's standing),
not v3's source matrix, so the record calls it credit-scale Omega. A draft carries the coding in `es`; this module checks the
coding against the transcript and computes. Laws record: a coding that does not reconstruct its answer is recorded as a breach on
the observation, never refused.

    python3 scripts/erasure_skew.py check <draft.json>    # applicability verdict and, where an es block is present, the numbers
    python3 scripts/erasure_skew.py survey                # applicability over the whole registry (read only)
    python3 scripts/erasure_skew.py trend                 # pooled numbers over every coded observation (read only)
    python3 scripts/erasure_skew.py calibrate             # recompute the calibration set against the registry's transcripts
"""
import itertools, json, pathlib, re, sys
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
CODEBOOK = "ES-CREDIT-v0"
CODES = {"REF", "ADJ+", "ADJ=", "ADJ-", "GEN", "ASK", "FRAME", "RESID"}
CREDIT = {"REF", "ADJ+", "ADJ=", "ADJ-"}
BULLET = re.compile(r"^\s*(?:[•*\-–]|\d+[.)])\s")
words = lambda s: len(re.findall(r"\S+", s or ""))
norm = lambda s: re.sub(r"\s+", " ", s or "").strip()

# ---------------------------------------------------------------------------------------------------------------- applicability
CREDIT_LANG = re.compile(r"\b(contribut\w*|pioneer\w*|found(?:ed|er|ing|ational)|coin(?:ed|er)|developed by|led by|led the|"
                         r"associated with|scholars? (?:like|such as)|key (?:figures|scholars|contributors|thinkers)|"
                         r"originat\w*|credit\w*|attribut\w*|invent\w*|formaliz\w*|introduced by|the work of)\b", re.I)
NAME = re.compile(r"\b(?:[A-Z][a-zà-ÿ'’\-]+[ \t]+){1,3}[A-Z][a-zà-ÿ'’\-]{2,}\b")     # two to four capitalised words, one line
STARTERS = {"The", "This", "These", "That", "If", "When", "Whether", "For", "In", "A", "An", "Its", "It", "Likewise", "Here", "As",
            "While", "Because", "However", "Within", "Before", "Rather", "By", "On", "At", "From", "With", "To", "Their", "His", "Her"}
_OWN = None
_COMMON = None


def common_words():
    """Words the registry's own compositions use in lower case (three or more times): a capitalised phrase made only of these is a
    heading or a concept ("Key Contributions", "Hugging Face"), not a person's name. Built from the registry, no outside list."""
    global _COMMON
    if _COMMON is None:
        from collections import Counter
        c = Counter()
        try:
            reg = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text())
            for e, o in _obs(reg): c.update(re.findall(r"\b[a-zà-ÿ'’\-]{2,}\b", _composition(o.get("transcript"))))
        except Exception:
            pass
        _COMMON = {w for w, n in c.items() if n >= 3}
    return _COMMON


def own_lexicon():
    """The archive's own names: its entities (data/entities.json, with aliases) and the Dodecad (data/dodecad.json)."""
    global _OWN
    if _OWN is None:
        S = {"Lee Sharks", "Crimson Hexagonal Archive", "Crimson Hexagon", "Machine-Mediated Reception Studies"}
        try:
            for e in json.loads((ROOT / "data/entities.json").read_text())["entities"]:
                if e.get("relation") == "archive": S |= {e.get("name") or ""} | set(e.get("aliases") or [])
            for h in json.loads((ROOT / "data/dodecad.json").read_text())["heteronyms"]: S.add(h.get("name") or "")
        except Exception:
            pass
        _OWN = {x for x in S if x}
    return _OWN


def credited_others(comp, own):
    """Sentences in which credit language stands beside a name that is not the archive's own: the evidence that the composition
    allocated credit to another party. Names are two to four capitalised words on one line, a sentence-initial word dropped."""
    hits = []
    for sent in re.split(r"(?<=[.!?])\s+|\n+", comp):
        if not CREDIT_LANG.search(sent): continue
        for m in NAME.finditer(sent):
            n = m.group(0).split()
            if n[0] in STARTERS: n = n[1:]
            n = " ".join(n)
            if len(n.split()) < 2 or any(n in o or o in n for o in own if len(o) > 3): continue
            if all(t.lower().strip("'’s") in common_words() for t in n.split()): continue
            hits.append((n, sent.strip()[:160]))
    return hits


def _composition(transcript):
    """The composed text only: [SYSTEM] turns, without the bracketed header."""
    t = transcript or ""
    parts = re.split(r"\[SYSTEM\]\s*", t)[1:]
    if parts:
        return "\n".join(re.split(r"\n\[QUERENT\]", p)[0] for p in parts)
    return re.sub(r"^\s*\[[^\]]*\]\s*", "", t)   # transcripts seated before the turn tags: the text is the composition


def applicability(d, entry=None):
    """INDICATED, OPTIONAL or NOT APPLICABLE, with the reasons. Erasure Skew measures where credit went when the warranted source
    lost standing to other parties, so it is indicated only where (1) a composition exists, (2) the address designates a work or
    entity whose source the record knows (an originator), (3) that source lost standing (per_v author or inst lost) and (4) the
    composition allocates credit to someone else (credit language beside a name other than the warranted source's)."""
    R = []
    if d.get("null_basis"):
        return {"verdict": "not applicable", "codebook": CODEBOOK, "reasons": ["a significant null: there is no composition to code"]}
    comp = _composition(d.get("transcript"))
    if not comp.strip():
        return {"verdict": "not applicable", "codebook": CODEBOOK, "reasons": ["no composed turn in the transcript"]}
    org = d.get("originator") or (entry or {}).get("originator") or {}
    if (org.get("relation") if isinstance(org, dict) else None) == "external" and not d.get("es"):
        return {"verdict": "optional", "codebook": CODEBOOK, "reasons": ["the originator is external: indicated only where the record codes an archive "
                "work as the credit object (as at the journal's address, where the study of AI-mediated reception was credited away)"]}
    pv = d.get("per_v") if isinstance(d.get("per_v"), dict) else {}
    lost = [k for k in ("author", "inst") if pv.get(k) is False]
    if pv and not lost:
        return {"verdict": "not applicable", "codebook": CODEBOOK, "reasons": ["the warranted source kept author and institution (per_v): no standing was lost to skew"]}
    own = set(own_lexicon())
    if isinstance(org, dict) and org.get("name"):
        n = org["name"]; own |= {n, " ".join(reversed([x.strip() for x in n.split(",")]))}
    hits = credited_others(comp, own); names = sorted({h[0] for h in hits})
    R.append("standing lost: " + (", ".join(lost) if lost else "per_v not recorded"))
    R.append(f"credit beside another name: {len(hits)} sentence(s)" + (f", e.g. «{hits[0][1]}»" if hits else ""))
    R.append(f"names credited: {len(names)}" + (f" ({', '.join(names[:5])})" if names else ""))
    if lost and names:
        return {"verdict": "indicated", "codebook": CODEBOOK, "reasons": R}
    return {"verdict": "optional", "codebook": CODEBOOK, "reasons": R}


# ------------------------------------------------------------------------------------------------------------------ computation
def _omega(w, r):
    w, r = np.asarray(w, float), np.asarray(r, float)
    return None if np.var(w) == 0 else float(np.mean((w - w.mean()) * (r - r.mean())) / np.var(w))


def _perm_p(w, r, o, rng):
    if len(r) <= 9:
        P = [_omega(w, q) for q in itertools.permutations(r)]
    else:
        P = [_omega(w, rng.permutation(r)) for _ in range(20000)]
    return float(np.mean(np.array(P) >= o - 1e-12))


def compute(es, transcript):
    """Check the coding against the transcript and compute. Returns the stored result; breaches are recorded in it."""
    out = {"codebook": es.get("codebook") or CODEBOOK, "round": es.get("round", 1), "credit_object": es.get("credit_object"),
           "warranted": es.get("warranted"), "breaches": []}
    B = out["breaches"]; T = norm(transcript)
    spans = es.get("spans") or []; parties = es.get("parties") or {}
    ans = norm(" ".join(s.get("text", "") for s in spans))
    if not ans or ans not in T:
        B.append("the coded spans, joined, are not a verbatim passage of the transcript")
    if es.get("answer_start") and not ans.startswith(norm(es["answer_start"])):
        B.append("the spans do not begin at answer_start")
    if es.get("answer_end") and not ans.endswith(norm(es["answer_end"])):
        B.append("the spans do not end at answer_end")
    for i, s in enumerate(spans):
        if s.get("code") not in CODES: B.append(f"span {i}: unknown code {s.get('code')}")
        for p in s.get("parties") or []:
            if p not in parties: B.append(f"span {i}: party «{p}» not in parties")
        if s.get("code") in CREDIT and not s.get("parties"): B.append(f"span {i}: a credit span names no party")
    if es.get("warranted") not in parties: B.append("the warranted source is not among the parties")
    tot = words(ans) or 1; by = {}; pw = {p: 0.0 for p in parties}
    for s in spans:
        n = words(s.get("text")); by[s.get("code")] = by.get(s.get("code"), 0) + n
        for p in s.get("parties") or []:
            if p in pw: pw[p] += n / len(s["parties"])
    W = es.get("warranted")
    out["words"] = tot; out["by_code"] = by
    out["alpha_T"] = round(by.get("REF", 0) / tot, 3)
    out["Pi_d"] = {"w+": round((by.get("ADJ+", 0) + by.get("GEN", 0)) / tot, 3), "w=": round(by.get("ADJ=", 0) / tot, 3),
                   "w-": round(by.get("ADJ-", 0) / tot, 3)}
    out["residual"] = round(1 - out["alpha_T"] - sum(out["Pi_d"].values()), 3)
    first = next((s for s in spans if s.get("code") in CREDIT), None)
    names, ws, rho, share = [], [], [], []
    feats = {}
    for p, meta in parties.items():
        mine = [s for s in spans if p in (s.get("parties") or [])]
        txt = " ".join(s.get("text", "") for s in mine)
        named_as = meta.get("named_as") or []
        f_named = int(any(n in txt for n in named_as))
        f_lead = int(first is not None and p in (first.get("parties") or []))
        f_item = int(any(BULLET.match(s.get("text", "")) for s in mine))
        q = meta.get("qualifier")
        if q and q not in txt: B.append(f"party «{p}»: qualifier «{q}» not found in its spans")
        if meta.get("w") not in (0, 1): B.append(f"party «{p}»: w must be 0 or 1")
        wb = meta.get("w_basis")
        if wb and wb != "(no affiliation stated)" and wb not in T: B.append(f"party «{p}»: w_basis not found in the transcript")
        f_und = int(bool(mine) and not q)   # an absent party (no span) keeps none of the four
        fe = [f_named, f_lead, f_item, f_und]
        feats[p] = {"named": f_named, "lead": f_lead, "own_item": f_item, "undiminished": f_und, "rho": sum(fe) / 4,
                    "w": meta.get("w"), "w_basis": wb, "qualifier": q, "words": round(pw[p], 1)}
        names.append(p); ws.append(meta.get("w") or 0); rho.append(sum(fe) / 4); share.append(pw[p])
    out["parties"] = feats
    o = _omega(ws, rho); rng = np.random.default_rng(157)
    if o is None:
        out["Omega"] = None; out["Omega_note"] = "undefined: var(w) = 0 (every credited party at one standing — no competitor at another)"
    else:
        sh = np.array(share) / (max(share) or 1)
        out["Omega"] = round(o, 3); out["r"] = round(float(np.corrcoef(ws, rho)[0, 1]), 3) if np.std(rho) > 0 else None
        out["p_perm"] = round(_perm_p(ws, rho, o, rng), 4); out["p_floor"] = round(1 / len(ws), 4) if sum(1 for x in ws if x == 0) == 1 else None
        os_ = _omega(ws, sh); out["sensitivity"] = {"Omega_rho_share": round(os_, 3) if os_ is not None else None}
    if W in feats:
        others = [feats[p]["rho"] for p in feats if p != W]
        out["warranted_rank_last"] = bool(others) and all(feats[W]["rho"] < x for x in others)
    out["breach"] = bool(B)
    return out


# ------------------------------------------------------------------------------------------------------------------- registry
def _obs(reg):
    for e in reg["entries"]:
        for o in (e.get("observations") or [e]):
            yield e, o


def survey():
    reg = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text())
    from collections import Counter
    c = Counter(); by = Counter()
    for e, o in _obs(reg):
        d = dict(e); d.update(o)
        v = applicability(d, e)["verdict"]; c[v] += 1; by[(v, str(o.get("date") or e.get("date"))[:7])] += 1
    print("applicability over", sum(c.values()), "observations:", dict(c))
    for m in sorted({k[1] for k in by}): print(" ", m, {v: by[(v, m)] for v in ("indicated", "optional", "not applicable")})


def trend():
    reg = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text())
    rows = [(e["slug"], o.get("slug"), str(o.get("date")), o["es"]) for e, o in _obs(reg) if isinstance(o.get("es"), dict) and not o["es"].get("breach")]
    print(len(rows), "coded observations (codebook", CODEBOOK + ")")
    for r in sorted(rows, key=lambda x: x[2]):
        es = r[3]; print(f"  {r[2]}  {r[1]}: alpha_T {es['alpha_T']}  Pi_d^w+ {es['Pi_d']['w+']}  Omega {es.get('Omega')}  warranted last {es.get('warranted_rank_last')}")
    D = [r[3] for r in rows if r[3].get("Omega") is not None]
    if D:
        print("pooled: mean Omega", round(float(np.mean([x["Omega"] for x in D])), 3), "over", len(D), "· warranted source ranked last in",
              sum(1 for x in D if x.get("warranted_rank_last")), "of", len(D))


def calibrate():
    """Recompute each calibration coding against its observation's transcript in the registry, and compare with the stored result."""
    reg = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text()); T = {}
    for e, o in _obs(reg): T[o.get("slug") or e["slug"]] = o.get("transcript")
    ok = True
    for f in sorted((ROOT / "rebuild/capture-registry/erasure-skew/calibration").glob("*.json")):
        c = json.loads(f.read_text()); t = T.get(c["observation"])
        if t is None: print(f"  {f.stem}: observation {c['observation']} not seated"); continue
        r = compute(c["coding"], t); same = all(r.get(k) == c["result"].get(k) for k in ("alpha_T", "Pi_d", "Omega", "p_perm", "warranted_rank_last"))
        ok &= same and not r["breach"]
        print(f"  {f.stem}: alpha_T {r['alpha_T']}  Pi_d^w+ {r['Pi_d']['w+']}  Omega {r.get('Omega')}  p {r.get('p_perm')}  {'reproduced' if same else 'DIFFERS'}{'  BREACH ' + str(r['breaches']) if r['breach'] else ''}")
    return 0 if ok else 1


if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else ""
    if a == "check":
        d = json.loads(pathlib.Path(sys.argv[2]).read_text())
        print(json.dumps(applicability(d), indent=1, ensure_ascii=False))
        if d.get("es"): print(json.dumps(compute(d["es"], d.get("transcript")), indent=1, ensure_ascii=False))
    elif a == "survey": survey()
    elif a == "trend": trend()
    elif a == "calibrate": sys.exit(calibrate())
    else: print(__doc__)
