#!/usr/bin/env python3
"""compute_evidentiary_table.py — the SPXI evidentiary table, computed from the Capture Registry.

The table on spxi.dev (#evidence) was first computed by hand on 2026-09-23 from registry v11.7. This script
states every row as a definition and computes it, so the table can be re-run against any version and checked by
anyone. Run against the v11.7 file of 2026-09-23 it reproduces every published figure but two, noted below.

Usage:
    python3 scripts/compute_evidentiary_table.py [REGISTRY.json [CAPTURE-DEPOSIT-LINKS.json]] [--json]
Defaults: data/EA-WG-CAPTURES-01.json and data/capture-deposit-links.json.

Rows and definitions
  addresses            len(entries): one record per semantic address (query as issued + surface).
  observations         the registry's observation_count (the sum of n_observations).
  surfaces             per address, the entry's `surface`, with raw variants collapsed to a surface family
                       (every ChatGPT string → ChatGPT, Grok (x.com) → Grok, Perplexity (agentic) → Perplexity);
                       UNDETERMINED / UNRESOLVED counted apart; 'generative' = families that compose an answer.
  signed_out           observations whose sign-in condition (the observation's, else the entry's) records
                       signed out, logged out, incognito (not 'non-incognito') or unauthenticated. v11.7 gives 329; the 2026-09-23 hand
                       count was 328 by a filter not recorded.
  post_termination     addresses whose earliest date (dates / observation dates) is after 2026-06-19, the day the
                       deposit host terminated the account.
  after_410            addresses whose PRIMARY linked deposit has a DOI returning 410 and which have a date after
                       2026-06-19; observations = the count of such dates in each address's `dates` list.
  repeat               addresses with n_observations >= 2; span = last − first date in `dates`; the median is over
                       addresses whose dates differ (span > 0).
  per                  provenance erasure rate over entries carrying a numeric `per`.
  originator_external  addresses whose ruled originator relation is 'external' (entities originated outside the
                       archive), by name and entity type, with their SPXI treatment. (Added 2026-09-25.)
Not computed: 'distinct named targets' (412, 166 minted, on 2026-09-23). The registry has no field naming a query's
target; that row was a hand reading and is reported as such until a target field exists.
"""
import json, sys, statistics, datetime, collections, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
TERMINATION = "2026-06-19"
GENERATIVE = {"Google AI Overview", "Google AI Mode", "ChatGPT", "Grok", "Bing Copilot", "Perplexity",
              "Claude", "Gemini", "Qwen", "Kimi", "ScholaRef (generated article)"}

def family(s):
    s = str(s or "")
    low = s.lower()
    if "chatgpt" in low: return "ChatGPT"
    if low.startswith("grok"): return "Grok"
    if low.startswith("perplexity"): return "Perplexity"
    if low.startswith("claude"): return "Claude"
    if "gemini" in low: return "Gemini"
    if low.startswith("qwen"): return "Qwen"
    if low.startswith("kimi"): return "Kimi"
    return s

def obs(e):
    return [o for o in (e.get("observations") or []) if isinstance(o, dict)] or [e]

def dates(e):
    return sorted(d for d in (e.get("dates") or [e.get("date")]) if d and d != "null")

def compute(reg_path, links_path):
    R = json.load(open(reg_path)); E = R["entries"]
    L = json.load(open(links_path)).get("links", {}) if pathlib.Path(links_path).exists() else {}
    out = {"registry_version": R.get("version"), "registry_date": R.get("date")}
    out["addresses"] = len(E)
    out["observations"] = R.get("observation_count") or sum(int(e.get("n_observations") or 1) for e in E)
    fam = collections.Counter(family(e.get("surface")) for e in E)
    undetermined = sum(fam.pop(k, 0) for k in ("UNDETERMINED", "UNRESOLVED"))
    out["surfaces"] = {"by_family": dict(fam.most_common()), "families": len(fam),
                       "generative_families": sorted(k for k in fam if k in GENERATIVE),
                       "raw_strings": len({e.get("surface") for e in E} - {"UNDETERMINED", "UNRESOLVED"}),
                       "surface_undetermined_addresses": undetermined}
    def auth(e, o):
        a = o.get("auth") or e.get("auth") or ""
        return str(a).lower()
    import re as _re
    def is_out(a):  # "signed in, non-incognito" must not count as incognito
        return bool(_re.search(r"signed out|logged out|unauthenticated|(?<!non-)incognito", a))
    so = sum(1 for e in E for o in obs(e) if is_out(auth(e, o)))
    out["signed_out"] = so
    out["post_termination"] = sum(1 for e in E if dates(e) and dates(e)[0] > TERMINATION)
    na = no = 0
    for e in E:
        deps = [x for x in ((L.get(e.get("slug")) or {}).get("deposits") or []) if x.get("primary")]
        if not any(any("410" in str(s) for s in ((x.get("doi_status") or {}).get("statuses") or [])) for x in deps):
            continue
        post = [d for d in dates(e) if d > TERMINATION]
        if post: na += 1; no += len(post)
    out["after_410"] = {"addresses": na, "observations": no}
    rep = [e for e in E if int(e.get("n_observations") or 1) >= 2]
    D = datetime.date.fromisoformat
    spans = [(D(dates(e)[-1]) - D(dates(e)[0])).days for e in rep if len(dates(e)) >= 2]
    pos = [s for s in spans if s > 0]
    out["repeat"] = {"addresses": len(rep), "median_span_days": statistics.median(pos) if pos else None,
                     "max_span_days": max(spans) if spans else None, "addresses_with_distinct_dates": len(pos)}
    per = [e["per"] for e in E if isinstance(e.get("per"), (int, float))]
    out["per"] = {"n": len(per), "mean": round(statistics.mean(per), 2) if per else None,
                  "median": statistics.median(per) if per else None}
    ext = [e for e in E if (e.get("originator") or {}).get("relation") == "external"]
    by = collections.Counter(((e["originator"].get("name")), e["originator"].get("entity_type")) for e in ext)
    out["originator_external"] = {"addresses": len(ext),
                                  "by_name_and_type": {f"{n} ({t})": c for (n, t), c in sorted(by.items())},
                                  "spxi_treatment": sorted({e["originator"].get("spxi_treatment") for e in ext})}
    dd = sorted(d for e in E for d in dates(e))
    out["span"] = {"first": dd[0] if dd else None, "last": dd[-1] if dd else None}
    return out

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    reg = args[0] if args else ROOT / "data/EA-WG-CAPTURES-01.json"
    links = args[1] if len(args) > 1 else ROOT / "data/capture-deposit-links.json"
    res = compute(reg, links)
    print(json.dumps(res, ensure_ascii=False, indent=1))
