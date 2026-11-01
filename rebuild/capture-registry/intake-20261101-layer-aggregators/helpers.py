"""Shared helpers for the part files of 2026-11-01 (09:56 EDT): the 18 names of the traininglayerliterature.org layer census (data/layer-census in the
traininglayerliterature.org repository, built 2026-11-01 from sources fetched once and saved with hashes) not already captured (The NEXT and Output were
captured with the authorship census, AXN:0B89 and 0B87), run by the operator for their /non rows ("captures, then /nons, then single pages"). Sixteen on the
Google AI Overview, expanded; Project Gutenberg and HathiTrust in AI Mode (the operator's notes in the paste: "wikipedia in place of popup so ai mode:",
"no popup. ai mode:"). The Literary History of Artificial Intelligence and The Pile came as two attached files, the rest pasted inline, separated by '$'.
Signed out, incognito (operator default). Each a new external atom set on the site template, its evidence the census's verified quotes in the saved
sources (sources/, manifest.json). Readers import this module from parts-*.py; each writes its own part files."""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
P = H / "parts"; P.mkdir(exist_ok=True)
R = json.load(open(H / "census-rows.json", encoding="utf-8"))
S = "rebuild/capture-registry/intake-20261101-layer-aggregators/sources/"
A = lambda atom, present, span=None: {"atom": atom, "present": present, "span": span}
DIM = {"name": ("M", 3, "token"), "operator": ("M", 3, "role"), "date": ("M", 1, "token"), "claim boundary": ("M", 2, "reading"), "presents": ("C", 2, "token"),
       "corpus": ("C", 2, "reading"), "purpose": ("D", 3, "reading"), "commitments": ("D", 2, "reading"), "lineage": ("D", 2, "role"), "identifier": ("D", 1, "role"),
       "deposit chain": ("D", 1, "role")}
ORDER = list(DIM)
RECEIVED = "2026-11-01 09:56 EDT"
OP = ("with the pastes (09:56 EDT): 'captures, then /nons, then single pages'. The census names as printed for him for their /non rows. His notes in the paste: "
      "at Project Gutenberg, 'wikipedia in place of popup so ai mode:'; at HathiTrust, 'no popup. ai mode:'. The Literary History of Artificial Intelligence "
      "and The Pile came as two attached files.")


def ev(slug, key):
    q = R[slug]["evidence"][key]
    assert q.get("q"), (slug, key, "the census evidence item has no quote (an unread source)")
    return {"record_quote": q["q"], "locus": S + q["src"] + ".txt"}


def aset(slug, spec, type_basis):
    """spec: {atom: (tokens, reference, [census evidence keys])}; atoms absent from spec are recorded unknown (no saved source states them), or
    inapplicable for 'presents' and 'deposit chain'."""
    atoms = []
    for a in ORDER:
        d, w, k = DIM[a]
        if a in spec:
            tok, ref, keys = spec[a]
            atoms.append({"atom": a, "dim": d, "weight": w, "kind": k, "applicability": "required", "tokens": tok, "reference": ref, "evidence": [ev(slug, x) for x in keys]})
        else:
            app = "inapplicable" if a in ("presents", "deposit chain") else "unknown"
            atoms.append({"atom": a, "dim": d, "weight": w, "kind": k, "applicability": app, "tokens": [], "reference": None, "evidence": []})
    srcs = sorted({x["locus"] for at in atoms for x in at["evidence"]})
    return {"new": "ext-tll-" + slug, "name": R[slug]["name"], "template": "site", "external": True, "type_basis": type_basis,
            "records": [{"source": R[slug]["name"] + " (its own pages or a third-party account, saved 2026-11-01)", "path": p, "origin": "census source"} for p in srcs],
            "atoms": atoms, "notes": "Built 2026-11-01 from the traininglayerliterature.org layer census row '" + slug + "' (its quotes verified verbatim in the saved sources), for the operator's run of the census names."}


C = lambda site, title, snip=None, rel="third_party", note=None: {"site": site, "title": title, "snip": snip, "rel": rel, "note": note}


def turns(paste, first=None):
    L = (H / paste).read_text(encoding="utf-8").split("\n")
    if first:
        a = next(i for i, l in enumerate(L) if l.startswith(first))
    else:
        a = next(i for i, l in enumerate(L) if l.startswith("You said: ")) + 1
    return [[a, len(L)]]


def mk(slug, q, aset_, obs_atoms, reached, mt, d, reading, findings, analysis, cites, per_v, per_note, aimode=None, first=None, related=None, notes=None):
    """One part. slug: the census slug (the paste is paste-<slug>.txt). q: the query exactly as run (the census name as printed)."""
    import re
    cslug = re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-") + ("-aimode-" if aimode else "-aio-") + "20261101"
    paste = f"paste-{slug}.txt"
    p = {"n": 1726, "slug": cslug, "paste": paste, "surface": "Google AI Mode" if aimode else "Google AI Overview", "received": RECEIVED, "s": "Machine Reception",
         "qs": [q], "turns": turns(paste, first), "entity_type": "site", "group": "Xtll-" + slug,
         "obs": {"scored_object": "the AI Mode answer, with its source cards" if aimode else "the Overview expanded, with its source cards", "reached": reached,
                 "atoms": obs_atoms, "inversions": [], "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None, "notes": notes or analysis},
         "mt": mt, "d": d, "reading": reading, "findings": findings, "analysis": analysis, "q_kind": "the census name; NEW address.",
         "per_v": per_v, "per_note": per_note, "cite_list": [dict(c, n=i + 1, url=None) for i, c in enumerate(cites)], "related_deposits": related or [1543],
         "notes_operator": OP, "atomset": aset_, "target_id": "NEW:" + aset_["new"],
         "originator": {"name": R[slug]["name"], "relation": "external", "entity_type": "site", "spxi_treatment": "partial",
                        "basis": "Not the archive's: an external resource, entered in the traininglayerliterature.org layer census on 2026-11-01 (data/layer-census, its own pages saved with hashes). Recorded 2026-11-01."}}
    if aimode:
        p["head_full"] = ("[Google AI Mode at the query, signed out and incognito (operator default of 2026-10-14). The operator, in the paste: '" + aimode + "'. The paste opens on "
                          "the search page and the web results above the answer ('Quick results from the web:'), kept in the raw paste and not part of the composition. Received " + RECEIVED + ".]")
        p["surface_basis"] = "The operator's note in the paste ('" + aimode + "'): no Overview popup, the run in AI Mode."
        p["transcript_class"] = "CAPTURE-TIME VERBATIM RECORD — paste of the AI Mode page; the composition and its cards read, the web results above it kept in the raw paste"
    else:
        p["head"] = "The 'You said' line carries the query twice, run together, and is given once here. Inline links are Google redirect URLs, kept as pasted."
    return p


def write(parts):
    for k, v in parts.items():
        (P / f"{k}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
    print("parts:", sorted(parts))
