#!/usr/bin/env python3
"""Regenerate api/counts.json from source.

WHY. counts.json already declares the rule: "Every surface that states a number
should fetch it from here rather than hand-setting it. Regenerated on deposit."
It was not regenerated on deposit, because NOTHING GENERATED IT — the file was
hand-written, so every figure in it drifted the moment the archive moved.

The result was visible on crimsonhexagonal.org, which stated THREE DIFFERENT
DEPOSIT COUNTS ON ONE PAGE — 1488 in the header, 482 twice in the body, and 1,520
in the network list — none of them current, all of them hand-set.

A canonical-counts endpoint that is itself hand-maintained is not a source of
truth; it is one more surface to drift. This derives every figure it can from the
registry and the data files, and marks the rest as declared with its provenance.
"""
import json, re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(p, default=None):
    f = ROOT / p
    if not f.exists():
        return default
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return default


def build() -> dict:
    reg = _load("data/registry.json", {"deposits": []})
    deps = reg.get("deposits", [])
    nums = sorted(d["deposit_number"] for d in deps if d.get("deposit_number"))
    gaps = [n for n in range(nums[0], nums[-1] + 1) if n not in set(nums)] if nums else []

    caps = _load("data/EA-WG-CAPTURES-01.json", {})
    n_caps = len(caps.get("entries", [])) if isinstance(caps, dict) else 0

    fleet = _load("data/fleet-domains.json", {})
    n_domains = fleet.get("count") or len(fleet.get("domains", []) or [])

    blog = _load("datasets/blog-index/manifest.json", {}) or _load("data/datasets/blog-index/manifest.json", {})
    n_posts = (blog or {}).get("total_posts") or (blog or {}).get("posts")

    lex = _load("data/lexical-minting-registry.json", {})
    n_terms = len(lex.get("terms") or lex.get("entries") or [])

    counts = {
        "_note": ("Canonical counts for the fleet. Every surface that states a number should "
                  "FETCH IT FROM HERE rather than hand-setting it. Derived from source by "
                  "scripts/build_counts.py — not hand-maintained, because a hand-maintained "
                  "canonical count is just another surface that drifts."),
        "_source": "https://www.alexanarch.org/api/counts.json",
        "_generator": "scripts/build_counts.py",
        "_generated": date.today().isoformat(),
        "deposits": {
            "total": len(deps),
            "highest_number": nums[-1] if nums else 0,
            "gaps": gaps,
            "note": ("total is the count of entries; highest_number is the latest mint. "
                     f"They differ by {len(gaps)} declared gap(s)." if gaps else
                     "total equals highest_number; no gaps."),
            "_derived_from": "data/registry.json",
        },
        "captures": {"total": n_caps, "_derived_from": "data/EA-WG-CAPTURES-01.json"},
        "lexicon": {"terms_minted": n_terms, "_derived_from": "data/lexical-minting-registry.json"},
        "fleet": {"domains": n_domains, "_derived_from": "data/fleet-domains.json"},
    }
    if n_posts:
        counts["blog"] = {"posts": n_posts, "since": 2013,
                          "_derived_from": "datasets/blog-index/manifest.json"}

    # Figures with no machine source in-repo. Declared, with the deposit that fixes them,
    # so a reader can tell a derived number from an asserted one.
    prev = _load("data/api/counts.json", {})
    counts["hexagon"] = dict(prev.get("hexagon", {}))
    counts["hexagon"]["_status"] = "DECLARED — no machine source in-repo; update by hand with the ruling that changes it"
    counts["heteronyms"] = dict(prev.get("heteronyms", {}))
    counts["heteronyms"]["_status"] = "DECLARED"
    counts["zenodo"] = {
        "status": "TERMINATED", "date": "2026-06-19",
        "deposits_deleted": 862, "dois_tombstoned": 1817,
        "_authority": "deposit #1 — Zenodotus' Book-Burning v9.1, triple-checked",
        "_superseded_figures": {"871": "machinemediation registry surface", "870": "prior counts.json"},
        "note": ("Do not present Zenodo DOIs from this corpus as resolvable. "
                 "The AXN is the sovereign identifier."),
    }
    return counts


if __name__ == "__main__":
    c = build()
    # ONE PATH ONLY: data/api/. The rewrite /api/(.*)\.json → /data/api/$1.json
    # already serves it at the advertised address.
    #
    # An earlier version of this script also wrote api/counts.json "to be safe",
    # and that is the fd8de940 failure class: api/ is VERCEL'S FUNCTIONS
    # NAMESPACE, and a static file there works until someone adds a function
    # beside it, at which point the whole directory flips and 1,012 static JSON
    # files 404 silently. This exact file had been moved out of api/ at 07:18 the
    # same day for that reason; writing it back re-armed the mine, and the
    # Endpoint Guardian caught it within the hour.
    #
    # STATIC DATA BELONGS IN /data/. api/ HOLDS EXECUTABLES ONLY.
    f = ROOT / "data/api/counts.json"
    f.write_text(json.dumps(c, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("  wrote data/api/counts.json  (served at /api/counts.json via rewrite)")
    d = c["deposits"]
    print(f"  deposits {d['total']} (highest {d['highest_number']}, gaps {d['gaps']}) · "
          f"captures {c['captures']['total']} · terms {c['lexicon']['terms_minted']} · "
          f"domains {c['fleet']['domains']}")
