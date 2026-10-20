#!/usr/bin/env python3
"""per_atoms.py — instantiate the dimensional PER atom set of every entity the Capture Registry can target (2026-10-19).

THE RULING (operator, 2026-10-19): "schema change. standardize atoms by entity type. and then we rescore ALL the entries,
retaining the historical scalar numbers." The templates, one per entity type, are rebuild/capture-registry/per-atoms/templates.json
(#1469 Rules 1-6; #1530 §2). This script fills each template for each entity in data/entities.json with its canonical tokens and
registered aliases, taken from externally checkable objects only (#1530 §2.3, Measurement Sovereignty): the registry record of the
entity's defining deposits, the DOI resolution index (confirmed and probable mappings), the heteronym records, the fleet manifest.
Never from a surface's rendering.

An atom whose template names a source the entity does not have (a person with no stated dates, a concept with no defining record)
is NOT INSTANTIABLE: it is listed as such and left out of the required set, so it neither counts against nor for the composition.
An entity whose name atom cannot be instantiated has no atom set (gate no_atom_set).

Writes data/per-atom-sets.json (published with every score, Rule 1).
  python3 scripts/per_atoms.py [--check]
"""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
T = json.loads((ROOT / "rebuild/capture-registry/per-atoms/templates.json").read_text(encoding="utf-8"))
ENTS = json.loads((ROOT / "data/entities.json").read_text(encoding="utf-8"))["entities"]
REG = {int(d["deposit_number"]): d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
IDX = json.loads((ROOT / "data/doi-resolution-index.json").read_text(encoding="utf-8"))["mappings"]
FLEET = json.loads((ROOT / "data/fleet-domains.json").read_text(encoding="utf-8"))["domains"]
HET = {}
for p in sorted((ROOT / "datasets/heteronyms/records").glob("*.json")):
    r = json.loads(p.read_text(encoding="utf-8"))
    if r.get("name"):
        HET[r["name"].lower()] = r
OUT = ROOT / "data/per-atom-sets.json"

CREATOR = {"Sharks, L.": "Lee Sharks", "Sharks, Lee": "Lee Sharks", "L. Sharks": "Lee Sharks", "Lee Sharks (MANUS)": "Lee Sharks"}
CORPUS = ["Crimson Hexagonal Archive", "Crimson Hexagon Archive", "Crimson Hexagonal", "Crimson Hexagon", "Alexanarch"]
ORCID = "0009-0000-1599-0703"
LIC = {"CC-BY-4.0": ["CC BY 4.0", "CC-BY-4.0", "CC BY", "Creative Commons Attribution 4.0"],
       "CC-BY-SA-4.0": ["CC BY-SA 4.0", "CC-BY-SA-4.0", "CC BY-SA", "Creative Commons Attribution-ShareAlike"]}

dois = {}
for m in IDX:
    mem = str((m.get("envelope") or {}).get("archive_membership") or "")
    rec = re.search(r"/s/records/(\d+)/", str(m.get("alexanarch_record") or ""))
    if rec and mem in ("confirmed", "probable"):
        dois.setdefault(int(rec.group(1)), []).append(m["dead_doi"])
by_id = {e["id"]: e for e in ENTS}
surfaces = {}
for e in ENTS:
    if e.get("surface_of"):
        surfaces.setdefault(e["surface_of"], []).extend(e["aliases"])
FRAME_TYPES = {"concept", "protocol", "institution", "dataset", "archive"}
frames = sorted({a for e in ENTS if e["type"] in FRAME_TYPES for a in [e["name"]] + e["aliases"] if len(a) >= 5}, key=len, reverse=True)


def names_of(cr):
    """The persons a registry creator string names, normalised ('Sharks, Lee' -> 'Lee Sharks'); parentheticals and
    'No explicit author line' notes dropped. Machine co-creators (TACHYON, Claude, the Assembly) are kept as named."""
    cr = str(cr or "")
    if not cr or cr.lower().startswith("no explicit"):
        return []
    cr = re.sub(r"\([^)]*\)", "", cr)
    out = []
    for part in re.split(r";|·|/|\bwith\b|\band\b|, MANUS|\bunder\b", cr):
        part = part.strip(" .,")
        if not part:
            continue
        m = re.fullmatch(r"([A-Z][\w'-]+), ([A-Z][\w.' -]*)", part)
        if m:
            first = m.group(2).strip()
            part = ("Lee" if first in ("L.", "L") and m.group(1) == "Sharks" else first) + " " + m.group(1)
        out.append(CREATOR.get(part, part))
    return out


def uniq(xs):
    out, seen = [], set()
    for x in xs:
        x = (x or "").strip()
        if len(x) >= 3 and x.lower() not in seen:
            seen.add(x.lower()); out.append(x)
    return out


def records(e):
    return [int(n) for n in (e.get("defining_deposits") or e.get("deposits") or []) if str(n).isdigit() and int(n) in REG]


def build(e):
    """One entity's atom set under the rubric's templates. Every atom gets an applicability (rubric: required | inapplicable |
    unknown): required atoms carry their tokens (token and role atoms) or their reference text (reading atoms); an atom the
    reference record does not state is UNKNOWN, a gap in the record never charged to the composition; an atom that does not
    apply to this target is INAPPLICABLE. The entity pass (readers, with provenance) confirms records, applicability, the
    framework, tradition and lineage tokens and the claim-boundary reference; this script gives the mechanical first state."""
    typ = T["aliases_of_types"].get(e["type"], e["type"])
    tpl = T["templates"].get(typ)
    if tpl is None:
        return {"id": e["id"], "name": e["name"], "type": e["type"], "gate": "no_atom_set", "basis": f"no template for entity type {e['type']}"}
    recs = records(e)
    R = [REG[n] for n in recs]
    het = HET.get(e["name"].lower())
    text = " ".join(str(d.get(k) or "") for d in R for k in ("title", "description", "keywords"))
    desc = (R[0].get("description") if R else None)
    creators = uniq([n for d in R for n in names_of(d.get("creator"))])
    atoms = []
    for a in tpl:
        tok, ref, app, why = [], None, "required", None
        n = a["atom"]
        if n in ("title", "term", "name"):
            tok = uniq([e["name"]] + e["aliases"] + (CORPUS[:4] if typ == "archive" else []))
        elif n in ("author", "originator", "producer", "operator", "founder"):
            tok = creators or (["Lee Sharks"] if e["relation"] == "archive" and typ in ("archive", "site", "institution") else [])
        elif n == "archival authority":
            prod = creators[:1]
            if e["relation"] == "archive" and prod and prod[0] != "Lee Sharks" and "Lee Sharks" in creators + ["Lee Sharks"]:
                tok = ["Lee Sharks"]
            else:
                app, why = "inapplicable", "the record names no archival authority separate from the producer"
        elif n in ("date", "dates"):
            tok = [t for t in uniq([str(d.get("date") or "")[:4] for d in R] + [str(e.get("created") or "")[:4]]) if re.fullmatch(r"\d{4}", t)]
        elif n == "claim boundary":
            ref = desc or e.get("presents")
            if typ == "person" and het:
                ref = f"{het.get('function')} ({het.get('identity_type')}; orthonym relation: {json.dumps(het.get('orthonym_relation'), ensure_ascii=False)})"
        elif n in ("tradition", "commercial interest", "heteronymy"):
            ref = desc if typ != "archive" else "the archive's primers (#269, #287, #288, #1102)"
            if n == "commercial interest" and not re.search(r"commerc|servic|client|sell|price|market", text, re.I):
                app, why, ref = "inapplicable", "the record states no commercial standing", None
        elif n == "lineage":
            ref = desc if typ != "person" else (json.dumps((het or {}).get("orthonym_relation"), ensure_ascii=False) if het else None)
            if typ == "archive":
                ref = "the archive's primers (#269, #287, #288, #1102)"
        elif n == "works":
            if any(e["name"] in names_of(d.get("creator")) for d in REG.values()):
                tok = uniq([re.split(r"[:—–(]", d["title"])[0] for d in REG.values() if e["name"] in names_of(d.get("creator")) and len(d["title"]) > 8])
        elif n == "corpus":
            tok = CORPUS
        elif n in ("framework", "institution"):
            if typ == "person" and het:
                tok = uniq([t for t in (het.get("claims") or {}).get("terms") or [] if t.lower() not in {c.lower() for c in CORPUS + ["CHA"]}])
            else:
                own = {x.lower() for x in [e["name"]] + e["aliases"]} | {c.lower() for c in CORPUS} | {"cha"}
                cands = [x for x in frames if x.lower() not in own and re.search(r"(?<![A-Za-z])" + re.escape(x) + r"(?![A-Za-z])", text, re.I)]
                if n == "institution":
                    names = {y.lower() for x in ENTS if x["type"] == "institution" for y in [x["name"]] + x["aliases"]}
                    cands = [x for x in cands if x.lower() in names]
                tok = uniq(cands)
        elif n == "presents":
            tok = uniq([e.get("presents") or ""] + ([by_id[e["surface_of"]]["name"]] if e.get("surface_of") in by_id else []))
        elif n == "identifier":
            for nn in recs:
                tok += dois.get(nn, []) + ["AXN:" + REG[nn]["hex"], "#" + str(nn)]
            if typ == "person":
                tok += ([het["het_id"]] if het and het.get("het_id") else []) + ([ORCID] if e["relation"] == "archive" else [])
            if typ == "archive":
                tok += ["alexanarch.org"]
            tok = uniq(tok)
        elif n == "deposit chain":
            tok = ["alexanarch.org/s/records/%d" % nn for nn in recs] + surfaces.get(e["id"], [])
            if het:
                tok += [re.sub(r"^https?://(www\.)?", "", str((het.get("surface") or {}).get("canonical") or "")).split("/")[0]]
            tok = uniq(tok)
        elif n == "licence":
            tok = uniq([t for d in R for t in LIC.get(str(d.get("license") or ""), [])]) or (["CC BY 4.0"] if typ == "archive" else [])
        if app == "required" and a["kind"] != "reading" and not tok:
            app, why = "unknown", "the reference record does not state it (" + a["token_from"] + ")"
        if app == "required" and a["kind"] == "reading" and not ref:
            app, why = "unknown", "no reference record to read it against"
        row = {"atom": n, "dim": a["dim"], "weight": a["weight"], "kind": a["kind"], "applicability": app}
        if tok and app == "required":
            row["tokens"] = tok
        if ref and app == "required":
            row["reference"] = ref
        if why:
            row["why"] = why
        atoms.append(row)
    if not any(x["atom"] in ("title", "term", "name") and x["applicability"] == "required" for x in atoms):
        return {"id": e["id"], "name": e["name"], "type": e["type"], "gate": "no_atom_set", "basis": "the name atom cannot be instantiated"}
    req = {d: sum(x["weight"] for x in atoms if x["dim"] == d and x["applicability"] == "required") for d in "MCD"}
    return {"id": e["id"], "name": e["name"], "type": e["type"], "template": typ, "relation": e["relation"], "records": recs,
            "atoms": atoms, "required": req, "state": "mechanical first state; the entity pass confirms it"}


def main():
    sets = [build(e) for e in ENTS]
    ok = [s for s in sets if s.get("atoms")]
    T_RUBRIC = T.get("rubric")
    doc = {"name": "PER atom sets, per entity (EA-WG-CAPTURES-01, dimensional PER)", "templates": "rebuild/capture-registry/per-atoms/templates.json",
           "rubric": T.get("rubric"), "templates_status": T["status"], "built_from": ["data/entities.json", "data/registry.json", "data/doi-resolution-index.json (confirmed, probable)",
                                                           "datasets/heteronyms/records/", "data/fleet-domains.json"],
           "rule": "Measurement Sovereignty (#1530 §2.3): tokens from externally checkable objects only. Applicability per atom: required (scored), inapplicable (not scored), unknown (the record does not state it: not scored, listed as the record's gap)",
           "count": len(sets), "with_atom_set": len(ok), "entities": sets}
    print(f"per atom sets: {len(sets)} entities, {len(ok)} with an atom set, {len(sets) - len(ok)} without")
    import collections
    print(" applicability:", collections.Counter(x["applicability"] for s in ok for x in s["atoms"]))
    print(" unknown by atom:", collections.Counter(x["atom"] for s in ok for x in s["atoms"] if x["applicability"] == "unknown").most_common(10))
    if "--check" not in sys.argv:
        OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
