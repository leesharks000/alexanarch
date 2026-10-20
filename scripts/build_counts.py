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
    _entries = lex.get("terms") or lex.get("entries") or []
    # 2026-10-12 (lexicon pass 7): the lexicon is the entries read as archive coinages or archive-reworked terms;
    # the rest of the registry is extraction residue kept for addressability, and is not a count of terms.
    n_terms = sum(1 for t in _entries if t.get("entry_class") in ("coinage", "archive-reworked term"))
    n_entries = len(_entries)

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
        "lexicon": {"terms_minted": n_terms, "registry_entries": n_entries,
                    "note": "terms_minted counts entries classed coinage or archive-reworked term; registry_entries includes extraction residue kept for addressability",
                    "_derived_from": "data/lexical-minting-registry.json"},
        "fleet": {"domains": n_domains, "_derived_from": "data/fleet-domains.json"},
    }
    if n_posts:
        counts["blog"] = {"posts": n_posts, "since": 2013,
                          "_derived_from": "datasets/blog-index/manifest.json"}

    # Figures with no machine source in-repo. Declared, with the deposit that fixes them,
    # so a reader can tell a derived number from an asserted one.
    prev = _load("data/api/counts.json", {})
    counts["hexagon"] = dict(prev.get("hexagon", {}))
    counts["hexagon"]["_status"] = ("DECLARED for the taxonomy (loci, rooms, specials, hosted_cosmologies, shadow_spaces, fields, "
                                    "transversals) and typed_relations (crimsonhexagonal.org/relation_record.json); DERIVED for the seats")
    # THE SEATS ARE DERIVED (2026-10-16). Until the room reading of that day there was no machine source for how many
    # records the Hexagon seats, and `seated_documents` was a hand-set 355 — the interface's seated corpus of August.
    # data/hexagon-seats.json is that source now: the interface's assignment, the 2026-10-16 reading and the operator's
    # rulings over it, read by the record pages and /s/rooms/. Low-confidence seats are proposals, not seats.
    _hs = _load("data/hexagon-seats.json", {})
    if _hs.get("seats"):
        _reg = {str(d["deposit_number"]): d.get("status") for d in _load("data/registry.json", {}).get("deposits", [])}
        _S = _hs["seats"]
        _seated = [n for n, v in _S.items() if v.get("rooms")]
        counts["hexagon"].update({
            "seated_records": len(_seated),
            "seated_records_active": sum(1 for n in _seated if _reg.get(n) == "ACTIVE"),
            "active_records": sum(1 for s in _reg.values() if s == "ACTIVE"),
            "seats": sum(len(v.get("rooms") or []) for v in _S.values()),
            "proposed_seats": sum(len(v.get("proposed") or []) for v in _S.values()),
            "loci_in_seat_map": len(_hs.get("rooms") or {}),
            "seated_documents": len(_seated),
            "_seats_derived_from": "data/hexagon-seats.json",
            # Beside the 47 loci (operator, 2026-10-16: "i like the sound of 47 loci"): named, not counted among them.
            "arks": sum(1 for r in (_hs.get("rooms") or {}).values() if r.get("cat") == "ark"),
            "further_shadow_documents": sum(1 for r in (_hs.get("rooms") or {}).values() if r.get("cat") == "shadow") - 1,
            "meta_structures": sum(1 for r in (_hs.get("rooms") or {}).values() if r.get("cat") == "structure" and r.get("type") == "META-STRUCTURE"),
            "_beside_the_loci": "48 loci (47 until R:r.41, the Stellar Orbit Fluid Dynamics Institute, 2026-10-20); beside them seven Arks — the five Arks (SP.05–SP.09) and the two shadow Arks, EA-ARK-01-SHADOW (SP.10) and the Lunar Arm shadow Ark (SP.11) (ruled 2026-10-18) — two further shadow documents (ZPZP, the Shadow Burn) and UMBML, the meta-structure over the three transversals (ruled 2026-10-16)",
            "_superseded_figures": {"355": "seated_documents, hand-set (the interface's seated corpus of August 2026)",
                                    "220": "typed relations as stated on crimsonhexagonal.org before 2026-10-16"},
        })
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
