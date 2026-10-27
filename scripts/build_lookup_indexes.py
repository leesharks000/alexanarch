#!/usr/bin/env python3
"""build_lookup_indexes.py — the archive's lookup indexes for SPXI-gnΩsis's paid lookups (ruled 2026-10-27).

MANUS, 2026-10-27: three lookups over records the archive already publishes, each answered without a model and sold at 1¢
per call ("paid at 1¢ - we look to the models of what agents are actually paying for"). The records stay free at their own
URLs; the charge is for the assembly. These indexes are what the service reads; they are generated, deterministic, and
carry no reading of their own.

Writes data/api/lookup/ (served at /api/lookup/):
  deposits.json         every deposit: number, AXN, hex, title, creator, date, status, licence, the canonical text's path
                        and SHA-256, the record page. The passage lookup narrows by the body index (/api/body-shards/)
                        and reads the texts from these paths.
  entities.json         the entities of the PER-dim rubric's atom sets (data/per-atom-sets.json): id, name, type, aliases
                        (the tokens of its name, term or title atom), its defining records, its /non entry where one
                        exists, and the counts behind its file. alias_index maps each normalised name and alias to ids.
  entities/<id>.json    one entity: its disambiguation, quoted from its defining records (each section whose heading is a
                        disambiguation, entity-definition, levels-of-difference or misreading section, verbatim, with its
                        line range and the record's AXN; the relation-table rows that set it apart from a neighbour), its
                        /non homonym register where its row has one, and every observation of the Capture Registry scored
                        against it under the PER-dim rubric (scores, atoms with their quoted spans, standing substitutions,
                        inversions, the observation's AXN, surface, date, query and description).
Nothing is paraphrased; a section longer than the cap is cut at a line and marked, its full text at the record's text URL.
"""
import collections, hashlib, json, pathlib, re, shutil
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data/api/lookup"
SITE = "https://www.alexanarch.org"
CAP = 6000
HEAD = re.compile(r"^(#{1,4})\s+(.+?)\s*$")
DIS = re.compile(r"disambig|entity[- ]definition|definitions?\b.*\bdifference|levels? of difference|usage-level difference|misreading|"
                 r"what .{1,40} is not|is not the|\bdistinct|definition face|canonical definition|primary entity definition", re.I)
REL = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(distinctFrom|notSameAs|notIdenticalTo|disambiguates?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|", re.M)


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s∮=]", " ", str(s).lower())).strip()


def sections(text):
    lines = text.split("\n")
    heads = [(i, len(m.group(1)), m.group(2)) for i, l in enumerate(lines) if (m := HEAD.match(l))]
    out = []
    for k, (i, lvl, title) in enumerate(heads):
        if not DIS.search(title):
            continue
        end = next((j for j, l2, _ in heads[k + 1:] if l2 <= lvl), len(lines))
        body = "\n".join(lines[i:end]).rstrip()
        cut = len(body) > CAP
        if cut:
            body = body[:body.rfind("\n", 0, CAP)]
        out.append({"heading": title, "lines": [i + 1, i + 1 + body.count("\n")], "text": body, "truncated": cut})
    # a section nested inside another taken section is already quoted with it
    keep = []
    for s in out:
        if not any(o is not s and o["lines"][0] <= s["lines"][0] and s["lines"][1] <= o["lines"][1] and not o["truncated"] for o in out):
            keep.append(s)
    return keep


def main():
    reg = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]
    by_n = {d["deposit_number"]: d for d in reg}
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "entities").mkdir(parents=True)
    deps = {}
    for d in reg:
        p = d.get("full_text_path")
        deps[str(d["deposit_number"])] = {"axn": d.get("axn"), "hex": d.get("hex"), "title": d.get("title"), "creator": d.get("creator") or d.get("author"),
                                          "date": d.get("date"), "status": d.get("status"), "licence": d.get("license"),
                                          "text": p, "sha256": d.get("hash"), "record": f"{SITE}/s/records/{d['deposit_number']}/"}
    import sys; sys.path.insert(0, str(ROOT / "scripts")); from build_body_index import _STOPWORDS
    (OUT / "deposits.json").write_text(json.dumps({"name": "deposit lookup index", "generated_from": "data/registry.json", "count": len(deps),
                                                   "body_index": {"shards": "/api/body-shards/{first two characters}.json", "tokens": "[a-z0-9]{3,}, case-folded",
                                                                  "stopwords": sorted(_STOPWORDS)},
                                                   "deposits": deps}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    # /non entries and their homonym registers
    non = json.loads((ROOT / "datasets/negative-of-the-negative/v2/axn.json").read_text(encoding="utf-8"))["entries"]
    panel = {x["entity"]: x for x in json.loads((ROOT / "datasets/negative-of-the-negative/v2/panel/panel.json").read_text(encoding="utf-8"))["entities"]}
    non_by_name = {}
    for k, x in non.items():
        nm = (panel.get(k) or {}).get("name") or k.replace("-", " ")
        row = json.loads((ROOT / x["row"]).read_text(encoding="utf-8"))
        non_by_name[norm(nm)] = {"entity": k, "name": nm, "axn": x["axn"], "page": f"{SITE}{x['page']}", "row": f"{SITE}/{x['row']}",
                                 "homonyms": row.get("homonyms")}
    # captures by target
    caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]
    cax = json.loads((ROOT / "data/captures/axn.json").read_text(encoding="utf-8"))["addresses"]
    axn_of = {s: o["axn"] for a in cax.values() for s, o in a["observations"].items()}
    by_target = collections.defaultdict(list)
    for e in caps:
        for o in (e.get("observations") or [e]):
            pd = o.get("per_dim") or (e.get("per_dim") if o is e else None)
            if not pd or not pd.get("target") or pd.get("gate") != "scored":
                continue
            slug = o.get("slug") or e["slug"]
            by_target[pd["target"].get("ent")].append({
                "observation": slug, "axn": axn_of.get(slug), "record": f"{SITE}/captures/{e['slug']}/", "q": o.get("q") or e.get("q"),
                "surface": o.get("surface") or e.get("surface"), "date": o.get("date") or e.get("date"), "description": o.get("d") or e.get("d"),
                "rubric": pd.get("spec"), "reached": pd.get("reached"), "scores": pd.get("scores"),
                "atoms": [{k: a.get(k) for k in ("atom", "dim", "weight", "present", "evidence")} for a in pd.get("atoms") or []],
                "standing_substitutions": pd.get("standing_substitutions") or [], "inversions": pd.get("inversions") or [],
                "after_challenge": ({"scores": pd["after_challenge"].get("scores")} if isinstance(pd.get("after_challenge"), dict) else None)})
    ents = json.loads((ROOT / "data/per-atom-sets.json").read_text(encoding="utf-8"))["entities"]
    summary, alias_index, texts = [], collections.defaultdict(list), {}
    for s in ents:
        nameatom = next((a for a in s.get("atoms") or [] if a["atom"] in ("name", "term", "title")), None)
        aliases = list(dict.fromkeys([s["name"]] + list((nameatom or {}).get("tokens") or [])))
        recs = [r["deposit"] for r in s.get("records") or [] if isinstance(r, dict) and str(r.get("deposit", "")).isdigit()]
        dis, rels = [], []
        for n in recs:
            d = by_n.get(int(n))
            if not d or not d.get("full_text_path"):
                continue
            p = ROOT / d["full_text_path"].lstrip("/")
            if not p.is_file() or p.suffix != ".md":
                continue
            t = texts.setdefault(str(p), p.read_text(encoding="utf-8"))
            for sec in sections(t):
                dis.append({"deposit": int(n), "axn": d["axn"], "title": d.get("title"), "text_url": f"{SITE}{d['full_text_path']}",
                            "text_sha256": hashlib.sha256(p.read_bytes()).hexdigest(), **sec})
            for m in REL.finditer(t):
                rels.append({"subject": m.group(1), "relation": m.group(2), "object": m.group(3), "basis": m.group(4), "deposit": int(n), "axn": d["axn"],
                             "line": t[:m.start()].count("\n") + 1})
        nonrow = next((non_by_name[norm(a)] for a in aliases if norm(a) in non_by_name), None)
        obs = sorted(by_target.get(s["id"], []), key=lambda x: (str(x["date"]), x["observation"]))
        rec = {"id": s["id"], "name": s["name"], "type": s.get("template"), "aliases": aliases,
               "defining_records": [{"deposit": int(n), "axn": by_n[int(n)]["axn"], "title": by_n[int(n)].get("title"),
                                     "record": f"{SITE}/s/records/{n}/"} for n in recs if int(n) in by_n],
               "non": {k: v for k, v in nonrow.items() if k != "homonyms"} if nonrow else None,
               "disambiguation": dis, "relations": rels, "homonyms": (nonrow or {}).get("homonyms"),
               "captures": obs, "rubric_basis": "data/per-atom-sets.json (PER-dim rubric v1.1)"}
        (OUT / "entities" / f"{s['id']}.json").write_text(json.dumps(rec, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        summary.append({"id": s["id"], "name": s["name"], "type": s.get("template"), "aliases": aliases, "non": bool(nonrow),
                        "disambiguation_sections": len(dis), "relations": len(rels), "captures": len(obs)})
        for a in aliases:
            if s["id"] not in alias_index[norm(a)]:
                alias_index[norm(a)].append(s["id"])
    (OUT / "entities.json").write_text(json.dumps({"name": "entity lookup index", "generated_from": ["data/per-atom-sets.json", "data/EA-WG-CAPTURES-01.json",
                                                    "datasets/negative-of-the-negative/v2/axn.json", "the defining records' texts"],
                                                   "count": len(summary), "entities": summary, "alias_index": dict(sorted(alias_index.items()))},
                                                  ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    c = collections.Counter()
    for x in summary:
        c["with_disambiguation"] += x["disambiguation_sections"] > 0; c["with_captures"] += x["captures"] > 0; c["with_non"] += x["non"]
    print(f"lookup indexes: {len(deps)} deposits; {len(summary)} entities ({dict(c)}); {sum(len(v) for v in by_target.values())} scored observations")


if __name__ == "__main__":
    main()
