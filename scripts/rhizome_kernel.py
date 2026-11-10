"""rhizome_kernel.py — a rhizome body governed by its framework holographic kernel (2026-11-10).

THE OCCASION. The Hugging Face audit of 2026-11-10 found the revelation-first body ending at #1687 and lacking the
works its subject turns on, and found that its rung classifier assigned each deposit the first rung whose words it
matched (F10). Read against the kernel EA-HK-REVFIRST-01 v1.1 (#1755), the vocabulary-built body held 8 of the
kernel's 47 records, among them neither the seed #202 nor its own grammar's defining paper #1217. The operator
(2026-11-10): "its holographic frame should probably now govern"; on the second look at what the vocabulary had
admitted, "adopted".

WHAT GOVERNS. A grammar that declares `governing_kernel` is emitted from the kernel's own files, never from the select
pattern:
  core        every record the kernel's topology seats (its strata and joins), every record carrying argument moves,
              the kernel record itself, and the captures the kernel names (07-captures.jsonl);
  placement   from the kernel's claims (03-claims.jsonl): a record sits on every rung a claim places it on, each
              placement carrying the claim id and the exact passage. Several rungs per record are the rule.
  lexical     the grammar's `roles` patterns survive only as the column `lexical_role`, a word match recorded beside
              the placement and never setting it;
  outside     a second tier the grammar names, records that bear on the subject and that the kernel does not name,
              and captures whose query or reading is on the subject (the grammar's patterns), each with its reason;
              no rung, no standing;
  exits       records another kernel holds, as typed exits to that kernel; they are not members here.
The ladder, the three claims and the dated states ship as their own tables. The spore names the kernel by id, version,
AXN and the SHA-256 of its 00-kernel.yaml, so a reissue of the kernel changes the emission and the freshness gate
forces the body to follow it. Deterministic: no timestamp enters the gated files."""
import hashlib, json, re, collections

# THE KERNEL ARRIVES AS JSON. The workflow's Python carries no YAML parser, so 00-kernel.yaml is read through a JSON
# sidecar written beside the grammar by scripts/kernel_sidecar.py, which records the YAML's SHA-256. The builder hashes
# the YAML it finds and refuses a sidecar that no longer matches it: a body is never emitted from a stale copy of its kernel.


def _rid(prefix, nid):
    return prefix + ":" + hashlib.sha256(nid.encode()).hexdigest()[:10]


def build(G, ROOT, OUT, reg, E, A, role_for, axes_for, grammar_path):
    gk = G["governing_kernel"]
    KD = ROOT / gk["files"]
    kbytes = (KD / "00-kernel.yaml").read_bytes()
    side = json.loads((ROOT / gk["sidecar"]).read_text(encoding="utf-8"))
    if side["sha256"] != hashlib.sha256(kbytes).hexdigest():
        raise SystemExit(f"{gk['sidecar']} records {side['sha256'][:12]} but {gk['files']}/00-kernel.yaml is "
                         f"{hashlib.sha256(kbytes).hexdigest()[:12]}: the kernel changed; run scripts/kernel_sidecar.py and commit")
    K = side["kernel"]
    assert K["id"] == gk["id"], f"governing kernel {gk['id']} expected, {K['id']} found"
    B = G["body"]; P = B["node_prefix"]
    claims = [json.loads(l) for l in (KD / "03-claims.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    graph = json.loads((KD / "02-graph.jsonld").read_text(encoding="utf-8"))
    sites = {n["@id"]: n for n in (graph.get("@graph") or []) if str(n.get("@id", "")).startswith("site:")}
    kcaps = [json.loads(l) for l in (KD / "07-captures.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    moves = collections.Counter()
    for l in (KD / "04-arguments.jsonl").read_text(encoding="utf-8").splitlines():
        if l.strip():
            r = json.loads(l).get("record")
            if r:
                moves[r] += 1

    def key(x):
        return f"rec:{x}" if isinstance(x, int) else str(x)
    # ---- the kernel's records, with stratum and clusters
    strat, clus = {}, collections.defaultdict(list)
    for s in K["topology"]["strata_from_latest"]:
        for x in s["records"]:
            strat.setdefault(key(x), s["id"])
    for c, xs in K["topology"]["clusters"].items():
        for x in xs:
            clus[key(x)].append(c)
    joins = {key(x) for x in K["topology"].get("joins") or []}
    members = set(strat) | joins | set(moves) | {f"rec:{gk['deposit']}"}
    for c in claims:
        members.add(c["target"]["record"])
    # ---- placements from the claims
    place = collections.defaultdict(list)
    for c in sorted(claims, key=lambda c: c["id"]):
        st = c.get("state") or {}
        place[c["target"]["record"]].append({"claim": c["id"], "rung": st.get("rung"), "assertion": st.get("assertion"),
                                             "body": c.get("body"), "role": c.get("role"), "exact": c["target"].get("exact")})
    rows, placements = [], []
    for m in sorted(members, key=lambda k: (k.startswith("site:"), int(k[4:]) if k.startswith("rec:") and k[4:].isdigit() else 0, k)):
        pl = place.get(m, [])
        rungs = sorted({p["rung"] for p in pl if p["rung"]}, key=lambda r: ["I", "II", "III", "IV", "V", "VI"].index(r) if r in ["I", "II", "III", "IV", "V", "VI"] else 9)
        bodies = sorted({p["body"] for p in pl if p.get("body")})
        why = ("the governing kernel" if m == f"rec:{gk['deposit']}" else
               "kernel stratum " + strat[m] if m in strat else "kernel join" if m in joins else
               "argument moves in the kernel" if m in moves else "a kernel claim's record")
        for p in pl:
            placements.append({"record": m, **p})
        if m.startswith("rec:"):
            n = int(m[4:]); d = reg.get(n, {})
            blob = " ".join(str(d.get(k) or "") for k in ("title", "description"))
            rows.append({"rhizome_node_id": _rid(P, f"deposit:{n}"), "graph_node_id": f"deposit:{n}", "deposit_number": n,
                         "title": d.get("title"), "node_type": "deposit", "region": "core", "core_rule": "K",
                         "entered_by": why, "dynamic_role": "governing_kernel" if n == gk["deposit"] else "kernel_record",
                         "kind": None, "collapse_axis": json.dumps(axes_for(blob)), "defines": json.dumps([]),
                         "creator": d.get("creator"), "date": d.get("date"), "evidence_status": d.get("status") or "ACTIVE",
                         "axn": d.get("axn"), "source_uri": f"https://www.alexanarch.org/s/records/{n}/",
                         "stratum": strat.get(m), "clusters": json.dumps(sorted(set(clus.get(m, [])))),
                         "rungs": json.dumps(rungs), "bodies": json.dumps(bodies), "kernel_claims": json.dumps([p["claim"] for p in pl]),
                         "argument_moves": moves.get(m, 0),
                         "placement_basis": "kernel claims" if pl else ("argument moves only" if moves.get(m) else "kernel topology"),
                         "lexical_role": role_for(blob, d.get("title")), "tier": "kernel"})
        else:
            s = sites.get(m, {})
            rows.append({"rhizome_node_id": _rid(P, m), "graph_node_id": m, "deposit_number": None, "title": s.get("title"),
                         "node_type": "site_page", "region": "core", "core_rule": "K", "entered_by": why,
                         "dynamic_role": "kernel_record", "kind": None, "collapse_axis": json.dumps([]), "defines": json.dumps([]),
                         "creator": None, "date": None, "evidence_status": "RETRIEVED " + str(s.get("retrieved") or ""),
                         "axn": None, "source_uri": s.get("url"), "stratum": strat.get(m),
                         "clusters": json.dumps(sorted(set(clus.get(m, [])))), "rungs": json.dumps(rungs),
                         "bodies": json.dumps(bodies), "kernel_claims": json.dumps([p["claim"] for p in pl]),
                         "argument_moves": moves.get(m, 0), "placement_basis": "kernel claims" if pl else "kernel topology",
                         "lexical_role": None, "tier": "kernel"})
    # ---- captures: the kernel's, then the outside tier by the grammar's patterns
    caps = {c["slug"]: c for c in json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]}
    kslugs = [c["slug"] for c in kcaps]
    ok = G["outside_kernel"]
    qrx = re.compile(ok["capture_query_pattern"], re.I); drx = re.compile(ok["capture_reading_pattern"], re.I)

    def caprow(slug, tier, why):
        c = caps.get(slug, {})
        return {"rhizome_node_id": _rid(P, "capture:" + slug), "graph_node_id": "capture:" + slug, "deposit_number": None,
                "title": c.get("mt") if len(c.get("mt") or "") >= 12 else c.get("q"), "node_type": "capture", "region": "core" if tier == "kernel" else "outside_kernel",
                "core_rule": "K" if tier == "kernel" else "O", "entered_by": why,
                "dynamic_role": "kernel_capture" if tier == "kernel" else "outside_kernel",
                "kind": "measurement" if c.get("per") is not None else "instance",
                "collapse_axis": json.dumps(axes_for(" ".join(str(c.get(k) or "") for k in ("d", "reading", "s")))),
                "defines": json.dumps([]), "creator": c.get("surface"), "date": c.get("date"), "evidence_status": "CAPTURED",
                "axn": c.get("axn"), "source_uri": f"https://www.alexanarch.org/captures/{slug}/", "stratum": None,
                "clusters": json.dumps([]), "rungs": json.dumps([]), "bodies": json.dumps([]), "kernel_claims": json.dumps([]),
                "argument_moves": 0, "placement_basis": "named by the kernel" if tier == "kernel" else "none: outside the kernel",
                "lexical_role": None, "tier": tier}
    for s in sorted(kslugs):
        if s in caps:
            rows.append(caprow(s, "kernel", "named by the kernel (07-captures.jsonl)"))
    for s in sorted(caps):
        if s in kslugs:
            continue
        c = caps[s]
        if qrx.search(c.get("q") or ""):
            rows.append(caprow(s, "outside", "outside the kernel: its query is on the subject"))
        elif drx.search(" ".join(str(c.get(k) or "") for k in ("d", "reading"))):
            rows.append(caprow(s, "outside", "outside the kernel: the subject is in its reading"))
    # ---- deposits outside the kernel, as the grammar names them
    for n_, why in sorted(ok["deposits"].items(), key=lambda kv: int(kv[0])):
        n = int(n_); d = reg.get(n, {})
        blob = " ".join(str(d.get(k) or "") for k in ("title", "description"))
        rows.append({"rhizome_node_id": _rid(P, f"deposit:{n}"), "graph_node_id": f"deposit:{n}", "deposit_number": n,
                     "title": d.get("title"), "node_type": "deposit", "region": "outside_kernel", "core_rule": "O",
                     "entered_by": "outside the kernel: " + why, "dynamic_role": "outside_kernel", "kind": None,
                     "collapse_axis": json.dumps(axes_for(blob)), "defines": json.dumps([]), "creator": d.get("creator"),
                     "date": d.get("date"), "evidence_status": d.get("status") or "ACTIVE", "axn": d.get("axn"),
                     "source_uri": f"https://www.alexanarch.org/s/records/{n}/", "stratum": None, "clusters": json.dumps([]),
                     "rungs": json.dumps([]), "bodies": json.dumps([]), "kernel_claims": json.dumps([]), "argument_moves": 0,
                     "placement_basis": "none: outside the kernel", "lexical_role": role_for(blob, d.get("title")), "tier": "outside"})
    included = {r["graph_node_id"] for r in rows}
    # ---- edges: the ledger's, inside the body; captures to the deposits they observe
    edges = []
    for e in E:
        if e["source_id"] in included and e["target_id"] in included:
            a = A.get(e["relation_id"], {})
            edges.append({**{k: e[k] for k in ("relation_id", "source_id", "predicate", "target_id", "target_type", "basis", "status", "note")},
                          "asserted_by": a.get("asserted_by"), "rhizome_role": e["predicate"]})
    links = json.loads((ROOT / "data/capture-deposit-links.json").read_text(encoding="utf-8"))
    for slug, v in sorted((links.get("links") or {}).items()):
        cid = "capture:" + slug
        if cid not in included:
            continue
        for d_ in (v.get("deposits") or []) if isinstance(v, dict) else []:
            num = d_.get("deposit_number") if isinstance(d_, dict) else d_
            if isinstance(num, int) and f"deposit:{num}" in included:
                edges.append({"relation_id": None, "source_id": cid, "predicate": "observes", "target_id": f"deposit:{num}",
                              "target_type": "deposit", "basis": "derived-deterministic", "status": "current",
                              "note": "capture-deposit resolver", "asserted_by": "process:resolve_capture_links", "rhizome_role": "observes"})
    edges.sort(key=lambda e: (e["source_id"], e["predicate"], e["target_id"]))
    # ---- the kernel's tables
    T = {
        "ladder": [{**r, "depends_on": json.dumps(r.get("depends_on") or []),
                    "consequence_of_defeat": json.dumps(K["dependency"]["consequence_of_defeat"].get(r["rung"], []))} for r in K["topology"]["rungs"]],
        "three_claims": [{"claim": k, **{kk: (json.dumps(vv, ensure_ascii=False) if isinstance(vv, (dict, list)) else vv) for kk, vv in v.items()}}
                         for k, v in K["three_claims"].items()],
        "states": sorted(K["topology"]["states"], key=lambda s: (s["axis"], s["date"], s["record"])),
        "placements": placements,
        "exits": [{"deposit_number": int(n), "title": reg.get(int(n), {}).get("title"), **x} for n, x in sorted(G["exits"].items(), key=lambda kv: int(kv[0]))],
        "kernel_candidates": [{"deposit_number": int(n), "title": reg.get(int(n), {}).get("title"), "why": w}
                              for n, w in sorted(ok["kernel_candidates"].items(), key=lambda kv: int(kv[0]))]
                             + [{"capture": r["graph_node_id"][8:], "title": r["title"], "why": r["entered_by"]}
                                for r in rows if r["node_type"] == "capture" and r["tier"] == "outside" and "query" in r["entered_by"]],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    w = lambda name, xs: (OUT / f"{name}.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in xs) + "\n", encoding="utf-8")
    w("nodes", rows); w("relations", edges)
    w("stolons", [{"from": f, "predicate": p, "to_rhizome": t, "note": n, "status": "advertised, not included"} for f, p, t, n in (G.get("stolons") or [])])
    for k, v in T.items():
        w(k, v)
    import datetime
    tiers = collections.Counter(r["tier"] for r in rows)
    spore = {
        "maxim": G["maxim"], "maxim_note": G.get("maxim_note"), "rhizome": B["slug"], "rhizome_id": B["rhizome_id"],
        "parent": B["parent"], "parent_uri": "https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive",
        "version": G["version"], "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "topology": B["topology"],
        "governing_kernel": {"id": K["id"], "version": K["version"], "built": K["built"], "deposit": gk["deposit"],
                             "axn": reg.get(gk["deposit"], {}).get("axn"), "files": gk["files"],
                             "kernel_sha256": hashlib.sha256(kbytes).hexdigest(),
                             "hub": "https://huggingface.co/datasets/leesharks/mantle-bearing/tree/main/holograms/" + K["id"]},
        "selection_method": "kernel-governed (rule K); outside tier named by the grammar (rule O); exits to other kernels",
        "selection": G["selection_note"],
        "counts": {"nodes": len(rows), "kernel": tiers["kernel"], "outside": tiers["outside"], "edges": len(edges),
                   "placements": len(placements), "exits": len(T["exits"]), "kernel_candidates": len(T["kernel_candidates"]),
                   "stolons": len(G.get("stolons") or [])},
        "generator": "scripts/build_rhizome_mc.py (kernel mode: scripts/rhizome_kernel.py)", "grammar": grammar_path,
        "reemit": f"RHIZOME_GRAMMAR={grammar_path} python3 scripts/build_rhizome_mc.py", "source_commit": None,
        "superseded_grammar": G.get("history"),
    }
    (OUT / "spore.json").write_text(json.dumps(spore, ensure_ascii=False, indent=1), encoding="utf-8")
    kr = sum(1 for r in rows if r["tier"] == "kernel" and r["node_type"] == "deposit")
    print(f"{B['rhizome_id']} v{G['version']} — governed by {K['id']} v{K['version']}: {len(rows)} nodes "
          f"(kernel {tiers['kernel']}: {kr} records; outside {tiers['outside']}), {len(edges)} edges, {len(placements)} placements, "
          f"{len(T['exits'])} exits, {len(T['kernel_candidates'])} kernel candidates")
