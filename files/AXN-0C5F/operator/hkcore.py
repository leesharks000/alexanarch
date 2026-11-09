"""hkcore — the shared machinery of a framework holographic kernel (EA-HK-FRAME-01, #1753), lifted from the Socrates builder
(build_hk_orthonym.py v1.1) without change of behaviour: record text, quotation location, introduction from first seating, claims, the
relation policy and its edges, record nodes, temporal events, captures, and the integrity manifest. A framework module supplies its data
and calls these. Equivalence with the Socrates builder is checked by test_hkcore.py against the deposited EA-HK-ORTHONYM-01 v1.1 claims."""
import json, hashlib, pathlib, re, yaml

BASE = "https://www.alexanarch.org/s/records/"
POLICY = {"motivates": None, "interprets": None, "instantiates": None, "supports": None, "derived_from": None, "independent_of": None,
          "qualifies": "scope", "generalizes": "establishment", "undercuts": "establishment,validation", "rebuts": "establishment", "supersedes": "identity,history"}


def norm(s):
    return re.sub(r"\s+", " ", s.replace("*", "").replace("’", "'").replace("‘", "'"))


class Kernel:
    def __init__(self, root, out, first_dir, kid, version, built, surfaces=None):
        self.ROOT = pathlib.Path(root); self.OUT = pathlib.Path(out); self.OUT.mkdir(parents=True, exist_ok=True)
        self.REG = {r["deposit_number"]: r for r in json.loads((self.ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
        self.CAP = {c["slug"]: c for c in json.loads((self.ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]}
        self.FIRSTDIR = pathlib.Path(first_dir) / "first"
        self.FIRST = json.loads((pathlib.Path(first_dir) / "first-seating.json").read_text())
        self.ID, self.VERSION, self.BUILT = kid, version, built
        self.SURF = surfaces or {}          # surface records: id -> {"url", "path" (local text), "sha256", "title", "retrieved"}
        self.C, self.edges, self.nodes, self.events, self.caps = [], [], [], [], []
        self.BODY, self.SECOND = {}, {}

    # ---------------------------------------------------------------- text and quotation
    def text(self, n):
        if isinstance(n, str):
            return pathlib.Path(self.SURF[n]["path"]).read_text(encoding="utf-8", errors="ignore")
        p = self.REG[n].get("full_text_path"); f = self.ROOT / p.lstrip("/") if p else None
        return f.read_text(encoding="utf-8", errors="ignore") if f and f.exists() else ""

    def locate(self, n, q):
        """The quotation must occur in the record's seated text or its description; return where."""
        if norm(q) in norm(self.text(n)): return "text"
        if not isinstance(n, str) and norm(q) in norm(self.REG[n].get("description") or ""): return "description"
        raise SystemExit(f"quotation not found in #{n}: {q[:90]}")

    def introduced(self, n, quote):
        """Introduction is established only where the quotation is present in the record's first seated text or its description at that commit."""
        if isinstance(n, str):
            s = self.SURF[n]
            return {"date": None, "basis": "surface page as retrieved; introduction date unresolved from this repository", "retrieved": s["retrieved"], "page_sha256": s["sha256"]}
        f = self.FIRST[str(n)]; t = norm((self.FIRSTDIR / f"{n}.md").read_text(encoding="utf-8", errors="ignore")); d = norm((self.FIRSTDIR / f"{n}.desc").read_text(encoding="utf-8"))
        base = {"record_date": self.REG[n]["date"], "first_seating": f["date"], "first_seating_commit": f["commit"]}
        if norm(quote) in t or norm(quote) in d:
            return {"date": f["date"], "basis": "present at the record's first seating in this repository", "first_text_sha256": f["text_sha256"], **base,
                    **({"note": "the record is dated earlier than its first seating here; presence before the first seating is not attested by this repository"} if self.REG[n]["date"] < f["date"] else {})}
        return {"date": None, "basis": "present in the current version; introduction date unresolved", **base,
                "current_version_since": (self.REG[n].get("reissue_history") or [{}])[-1].get("date") or self.REG[n]["date"]}

    def target(self, n):
        if isinstance(n, str):
            s = self.SURF[n]; return {"record": n, "url": s["url"], "page_sha256": s["sha256"]}
        return {"record": f"rec:{n}", "axn": self.REG[n]["axn"], "record_sha256": self.REG[n]["hash"]}

    def claim(self, cid, n, quote, kind, state, body=None, notes=None, role="standing", original_wording=None):
        tgt = self.target(n)
        if quote is None:
            tgt.update({"exact": None, "located_in": "not seated", "original_wording": original_wording}); intro = {"date": None, "basis": "original wording not seated in the record", "record_date": self.REG[n]["date"]}
        else:
            tgt.update({"exact": quote, "located_in": self.locate(n, quote)}); intro = self.introduced(n, quote)
        self.C.append({"id": cid, "claim_kind": kind, "role": role, "target": tgt, "state": state, "body": body or self.BODY[n], "introduced": intro, **({"notes": notes} if notes else {})})

    # ---------------------------------------------------------------- relations
    def rel(self, s, r, t, warrant, fam="evidentiary", src="map v0.1"):
        self.edges.append({"source": s, "relation": r, "target": t, "family": fam, "licensed_dimension": POLICY.get(r), "warrant": warrant, "provenance": src})

    # ---------------------------------------------------------------- records
    def record_nodes(self, strata, clusters):
        for k, (label, ns) in strata.items():
            for n in ns:
                if isinstance(n, str):
                    s = self.SURF[n]
                    self.nodes.append({"@id": n, "@type": "SurfaceRecord", "url": s["url"], "title": s["title"], "retrieved": s["retrieved"], "sha256": s["sha256"],
                                       "body": self.BODY[n], "body_secondary": self.SECOND.get(n, []), "stratum": k, "clusters": [c for c, v in clusters.items() if n in v]})
                    continue
                r = self.REG[n]
                self.nodes.append({"@id": f"rec:{n}", "@type": "Record", "deposit": n, "axn": r["axn"], "url": f"{BASE}{n}/", "title": r["title"],
                                   "date": r["date"], "status": r.get("status"), "version": r.get("version"), "sha256": r["hash"],
                                   "creator": r.get("creator") or r.get("authors"), "body": self.BODY[n], "body_secondary": self.SECOND.get(n, []),
                                   "stratum": k, "clusters": [c for c, v in clusters.items() if n in v]})
        for x in self.nodes:
            self.edges.append({"source": x["@id"], "relation": "belongs_to", "target": f"body:{x['body']}", "family": "structural", "licensed_dimension": None, "warrant": "map", "provenance": "map"})
            self.edges.append({"source": x["@id"], "relation": "belongs_to", "target": f"stratum:{x['stratum']}", "family": "structural", "licensed_dimension": None, "warrant": "map", "provenance": "map"})

    def captures(self, slugs, soft, framework_id):
        for s in slugs:
            c = self.CAP[s]
            self.caps.append({"@id": f"cap:{s}", "@type": "Capture", "slug": s, "axn": c.get("axn"), "date": c["date"], "surface": c.get("surface"), "query": c.get("q"),
                              "url": f"https://www.alexanarch.org/captures/{s}/", "reading": (c.get("d") or "")[:600], "per_note": (c.get("per_note") or "")[:400],
                              "distortion": soft.get(s), "establishes": "the composition's behaviour at the address only (rule R4)"})

    # ---------------------------------------------------------------- temporal
    def temporal(self, states, state_axis_name):
        CL = {c["id"]: c for c in self.C}
        for x in sorted([y for y in self.nodes if y["@type"] == "Record"], key=lambda y: (y["date"], y["deposit"])):
            self.events.append({"timeline": "historical", "date": x["date"], "event": "deposited", "object": x["@id"], "axn": x["axn"]})
            for h in self.REG[x["deposit"]].get("reissue_history") or []:
                self.events.append({"timeline": "historical", "date": h.get("date"), "event": "reissued_in_place", "object": x["@id"], "from": h.get("from_version"),
                                    "to": h.get("to_version"), "axn_before": h.get("axn_before_reissue")})
        for c in self.C:
            self.events.append({"timeline": "epistemic", "date": c["introduced"]["date"], "event": "introduced", "object": f"claim:{c['id']}", "basis": c["introduced"]["basis"], "role": c["role"]})
        for e in [x for x in self.edges if x["relation"] in ("rebuts", "supersedes") and x["source"].startswith("claim:")]:
            corr = CL[e["source"].split(":", 1)[1]]
            self.events.append({"timeline": "epistemic", "date": corr["introduced"]["date"], "event": "withdrawn", "object": e["target"], "by": e["source"], "basis": corr["introduced"]["basis"]})
        for c in self.caps:
            self.events.append({"timeline": "historical", "date": c["date"], "event": "captured", "object": c["@id"]})
        for st in states:   # each state on its named axis, bound to the record that states it and the claim that warrants it
            w = CL[st["warrant"]]["introduced"]
            self.events.append({"timeline": "epistemic", "date": st["date"], "event": f"{st['axis']}_state", "object": f"rec:{st['record']}", "axis": st["axis"], "state": st["state"],
                                **({"note": st["note"]} if st.get("note") else {}), "warrant": f"claim:{st['warrant']}", "attested_from": w["date"], "dated_by": "the record's date"})
        self.events.sort(key=lambda e: (e["date"] or "9999", e["timeline"]))

    # ---------------------------------------------------------------- output
    def dump_yaml(self, p, obj):
        (self.OUT / p).write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=140), encoding="utf-8")

    def write_lines(self, p, rows):
        (self.OUT / p).write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")

    def integrity(self):
        files = sorted(p.name for p in self.OUT.iterdir() if p.is_file() and p.name not in ("11-integrity.yaml", "10-verification.json"))
        self.dump_yaml("11-integrity.yaml", {"id": self.ID + "/integrity", "built": self.BUILT,
            "not_hashed_here": {"10-verification.json": "written by the verifier after this file; its hash is carried in the facsimile"},
            "registry_sha256": hashlib.sha256((self.ROOT / "data/registry.json").read_bytes()).hexdigest(),
            "captures_sha256": hashlib.sha256((self.ROOT / "data/EA-WG-CAPTURES-01.json").read_bytes()).hexdigest(),
            "surfaces": {k: v["sha256"] for k, v in self.SURF.items()},
            "files": {f: hashlib.sha256((self.OUT / f).read_bytes()).hexdigest() for f in files}})


# ---------------------------------------------------------------- v1.0 additions (2026-11-09; additive, the Socrates path untouched)
HK = "https://www.alexanarch.org/hk/"
SCHEMES = ("claim", "cap", "site", "stratum", "rung", "body", "cluster", "fw", "seat", "stmt")


def context(slug):
    """JSON-LD context: every local scheme a prefix under the kernel's namespace, so that 'rung:VI' in one kernel and the proxy
    'hk:revfirst/rung/VI' in another expand to the same IRI; identifier-valued properties coerced with @type @id (JSON-LD 1.1 §4.2.2)."""
    ctx = {"@vocab": f"{HK}{slug}#", "hk": HK, "rec": "https://www.alexanarch.org/s/records/", "prov": "http://www.w3.org/ns/prov#",
           "sameAs": {"@id": "http://schema.org/sameAs", "@type": "@id"}}
    ctx.update({s: f"{HK}{slug}/{s}/" for s in SCHEMES})
    for p in ("source", "target", "via", "joins", "canonical_record", "founding_record", "proposes", "posed_by"):
        ctx[p] = {"@type": "@id"}
    for p in ("warrants", "depends_on", "proposals"):
        ctx[p] = {"@type": "@id", "@container": "@set"}
    ctx["edges"] = {"@container": "@set"}
    return ctx


def ledger_roles(claims, rows):
    """A claim's body is claim-local: its principal body (the record's) and every ledger row that uses it, each role named."""
    CL = {c["id"]: c for c in claims}
    for c in claims:
        c["bodies"] = {c["body"]: "principal"}
    for b, row in rows.items():
        for side, cell in row.items():
            if not isinstance(cell, dict) or "warrants" not in cell: continue
            for w in cell["warrants"]:
                c = CL[w]
                if b not in c["bodies"]: c["bodies"][b] = f"ledger row {b} ({side})"
                elif c["bodies"][b] == "principal": c["bodies"][b] = f"principal; ledger row {b} ({side})"
    return CL
