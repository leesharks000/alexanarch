#!/usr/bin/env python3
"""per_dim_score.py — compute the dimensional PER of every read observation (PER-dim rubric v1.0, 2026-10-19).

Reads the observation pass (rebuild/capture-registry/per-atoms/obs-pass/batch-N.json with the readers' out-N.json, joined by
position: the batches carry duplicate keys), the merged atom sets (data/per-atom-sets.json) and the rubric. Readers decided
reached, abn, atom presence with verbatim spans, src, tombstone pointers and after_challenge; scores are computed here, never by
a reader. Uniform normalisations applied after reading, each stated and counted:
  N1  identifiers exempt from own-name pruning: an identifier token that is also a registered name (EA-WG-CAPTURES-01) is
      present when the name atom is present on that token;
  N2  a person's works: present when the first segment names the person and carries the full title of a deposit the
      registry credits to that person (the readers flagged the merged works lists as too narrow); titles that are also an
      entity's registered name (the archive, a framework, an institution) are excluded, since naming them is not crediting a work;
  N3  dates written out: an ISO date token counts in its written forms ('September 29, 2026', '29 September 2026') in the
      first segment (readers divided on this; the rubric's normalisation covers format);
  where 'first segment' is the transcript before its second operator turn marker ('You said:').
Gates: control (not read here); abn -> every score null; reached substitute | proximal_substitute | generic | refused ->
target_absent, every score 1.0, the atoms kept beneath; otherwise PER = 1 - present/required over required atoms, per dimension
null where nothing is required.
Writes rebuild/capture-registry/per-atoms/obs-pass/scored.json. The registry is not touched here.
"""
import json, pathlib, re, datetime, collections, os
ROOT = pathlib.Path(__file__).resolve().parents[1]
OP = ROOT / "rebuild/capture-registry/per-atoms/obs-pass"
BD = pathlib.Path(os.environ.get("PER_BATCHES", OP))  # the batch inputs (reproducible from the registry; membership and hashes in obs-pass/batches-index.json)
T = json.loads((ROOT / "rebuild/capture-registry/per-atoms/templates.json").read_text(encoding="utf-8"))
SETS = {s["id"]: s for s in json.loads((ROOT / "data/per-atom-sets.json").read_text(encoding="utf-8"))["entities"]}
REG = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]
ABSENT = {"substitute", "proximal_substitute", "generic", "refused"}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def names_of(cr):
    cr = re.sub(r"\([^)]*\)", "", str(cr or ""))
    out = []
    for part in re.split(r";|·|/|\bwith\b|\band\b|, MANUS|\bunder\b", cr):
        part = part.strip(" .,")
        m = re.fullmatch(r"([A-Z][\w'-]+), ([A-Z][\w.' -]*)", part)
        if m:
            part = ("Lee" if m.group(2).strip() in ("L.", "L") and m.group(1) == "Sharks" else m.group(2).strip()) + " " + m.group(1)
        if part:
            out.append(part)
    return out


WORKS = collections.defaultdict(set)
for d in REG:
    t = re.split(r"\s[—–:]\s|:\s", d.get("title") or "")[0].strip()
    if len(t) >= 18 and not d.get("status", "").startswith("SUPERSEDED"):
        for n in names_of(d.get("creator")):
            WORKS[n].add(t)


ENTNAMES = {re.sub(r"\s+", " ", x).strip().lower().removeprefix("the ") for e in json.loads((ROOT / "data/entities.json").read_text(encoding="utf-8"))["entities"]
            for x in [e["name"]] + e["aliases"]}
for n in list(WORKS):  # a title that is also an entity's name (the archive, a framework) is that entity, not a work credited by naming
    WORKS[n] = {w for w in WORKS[n] if re.sub(r"\s+", " ", w).strip().lower().removeprefix("the ") not in ENTNAMES}


def first_segment(t):
    i = [m.start() for m in re.finditer(r"You said:", t)]
    return t[: i[1]] if len(i) > 1 else t


def norm(s):
    return re.sub(r"\s+", " ", s or "").lower()


def written(iso):
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", iso)
    if not m:
        return []
    y, mo, d = m.group(1), MONTHS[int(m.group(2)) - 1], str(int(m.group(3)))
    return [f"{mo} {d}, {y}", f"{d} {mo} {y}", f"{mo} {d} {y}"]


def score(atoms, req):
    out = {}
    for d in "MCD":
        w = sum(a["weight"] for a in req if a["dim"] == d)
        p = sum(a["weight"] for a in req if a["dim"] == d and atoms.get(a["atom"]))
        out[d] = None if w == 0 else round(1 - p / w, 3)
    W = sum(a["weight"] for a in req); P = sum(a["weight"] for a in req if atoms.get(a["atom"]))
    out["PER"] = None if W == 0 else round(1 - P / W, 3)
    return out


def main():
    rows, norms = [], collections.Counter()
    for i in range(1, 25):
        B = json.loads((BD / f"batch-{i}.json").read_text(encoding="utf-8"))
        O = json.loads((OP / f"out-{i}.json").read_text(encoding="utf-8"))
        for it, r in zip(B, O):
            s = SETS[it["target"]["id"]]
            req = [a for a in s["atoms"] if a["applicability"] == "required"]
            seg = norm(first_segment(it["transcript"]))
            pres = {a["atom"]: bool(a.get("present")) for a in r.get("atoms", [])}
            spans = {a["atom"]: a.get("span") for a in r.get("atoms", [])}
            how = {}
            name_atom = next((a for a in req if a["atom"] in ("name", "title", "term")), None)
            for a in req:
                n = a["atom"]
                if pres.get(n):
                    continue
                if n == "identifier" and name_atom and pres.get(name_atom["atom"]):
                    both = set(a.get("tokens") or []) & set(name_atom.get("tokens") or [])
                    if any(norm(x) in norm(spans.get(name_atom["atom"]) or "") for x in both):
                        pres[n] = True; how[n] = "N1"; norms["N1"] += 1
                if n == "works" and s.get("template") == "person":
                    nm = [x for x in (name_atom or {}).get("tokens") or [] if norm(x) in seg]
                    if nm:
                        hit = next((w for w in WORKS.get(s["name"], ()) if norm(w) in seg), None)
                        if hit:
                            pres[n] = True; spans[n] = hit; how[n] = "N2"; norms["N2"] += 1
                if n in ("date", "dates"):
                    hit = next((w for tk in a.get("tokens") or [] for w in written(tk) if norm(w) in seg), None)
                    if hit:
                        pres[n] = True; spans[n] = hit; how[n] = "N3"; norms["N3"] += 1
            kind = (r.get("reached") or {}).get("kind")
            abn = bool((r.get("reached") or {}).get("abn"))
            gate = "abn" if abn else ("target_absent" if kind in ABSENT else "scored")
            sc = score(pres, req)
            final = {d: None for d in sc} if gate == "abn" else ({d: (1.0 if sc[d] is not None else None) for d in sc} if gate == "target_absent" else sc)
            ac = r.get("after_challenge")
            ac_out = None
            if ac:
                ap = {a["atom"]: bool(a.get("present")) for a in ac.get("atoms", [])}
                ak = (ac.get("reached") or {}).get("kind")
                ac_out = {"turn": ac.get("turn"), "reached": ak, "scores": ({d: 1.0 for d in "MCD"} | {"PER": 1.0}) if ak in ABSENT else score(ap, req)}
            rows.append({"key": it["key"], "entry": it["entry"], "obs_index": it["obs_index"], "slug": it["slug"], "target": it["target"],
                         "co_targets": it["co_targets"], "reached": kind, "abn": abn, "gate": gate, "scores": final, "beneath": sc if gate != "scored" else None,
                         "src": r.get("src"), "tombstone_pointer": r.get("tombstone_pointer"), "scored_object": r.get("scored_object"),
                         "atoms": [{"atom": a["atom"], "dim": a["dim"], "weight": a["weight"], "kind": a.get("kind"), "applicability": "required",
                                    "present": pres.get(a["atom"], False), "evidence": spans.get(a["atom"]), "normalised": how.get(a["atom"])} for a in req]
                                  + [{"atom": a["atom"], "dim": a["dim"], "weight": a["weight"], "kind": a.get("kind"), "applicability": a["applicability"],
                                      "present": None, "evidence": None, "normalised": None} for a in s["atoms"] if a["applicability"] != "required"],
                         "after_challenge": ac_out, "reached_basis": (r.get("reached") or {}).get("span"), "notes": r.get("notes"), "batch": i})
    (OP / "scored.json").write_text(json.dumps({"rubric": T["rubric"], "computed": datetime.date.today().isoformat(), "normalisations": dict(norms), "rows": rows},
                                               ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    g = collections.Counter(r["gate"] for r in rows)
    print(f"{len(rows)} scored; gates {dict(g)}; normalisations {dict(norms)}")
    sc = [r["scores"]["PER"] for r in rows if r["gate"] == "scored" and r["scores"]["PER"] is not None]
    print(f"scored PER mean {sum(sc)/len(sc):.3f} over {len(sc)}")


if __name__ == "__main__":
    main()
