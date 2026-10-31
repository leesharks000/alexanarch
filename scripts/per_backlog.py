#!/usr/bin/env python3
"""per_backlog.py — score the PER-dim backlog of 2026-10-29 under rubric v1.1, and write it (2026-10-29).

Operator, 2026-10-29: "we do dimensional per scoring on intake now. is that set up as standard?", then "lets do so" to scoring
the backlog and making the score standard at intake. The backlog is every observation seated without per_dim, 2026-10-20 to
2026-10-29 (58 observations of 57 entries). Six readers built the atom sets their targets lacked and read each observation in
full (rebuild/capture-registry/per-atoms/backlog-20261029/BRIEF.md, which follows obs-pass-d/HELD-BRIEF.md): archive targets
from their defining records; external entities (the MMRS and provenance censuses) from their census records and their /non
field ledgers and saved sources, the template's corpus atom inapplicable.

  1. VERIFY  every record quote at its locus and every reader span in its transcript, verbatim (whitespace, quotation marks and
             Unicode compatibility folded, as scripts/per_d_verify.py); each observation lists its target's required atoms; no
             atom both present and used in an inversion. Any miss stops the write and is listed.
  2. MERGE   the new atom sets into data/per-atom-sets.json as TGT-<slug> (the retarget pass's convention for a target with no
             entity-register row), state "backlog pass (rubric v1.1) 2026-10-29, reader <G>", external sets marked external.
  3. SCORE   as per_d_score.py's held branch: gates abn -> null, target_absent -> 1.0 with the atoms beneath, normalisation N3 on
             dates, an atom used in an inversion absent. Scores are computed here, never by a reader.
  4. WRITE   per_dim on each observation (and on the entry from its root observation), in per_d_write.py's shape; per, per_v and
             per_corrected untouched; per_dim_pending cleared; the registry version bumped with a correction-log line.
  python3 scripts/per_backlog.py [--check]
"""
import collections, datetime, json, pathlib, re, sys, unicodedata
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import per_dim_score as V
BD = ROOT / "rebuild/capture-registry/per-atoms/backlog-20261029"
PS = ROOT / "data/per-atom-sets.json"
PR = ROOT / "data/EA-WG-CAPTURES-01.json"
GROUPS = ["A", "B", "M1", "M2", "P1", "P2"]
ABSENT = {"substitute", "proximal_substitute", "generic", "refused"}
SPEC = "PER-dim rubric v1.1"
TODAY = "2026-10-29"


def N(s):
    s = unicodedata.normalize("NFKC", str(s or "")).replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("\\n", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for k, v in x.items():
            yield str(k); yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)


_cache = {}
def source_text(path):
    """The normalised text a quote is checked against: a .json file's string values, any other file's text."""
    if path not in _cache:
        p = pathlib.Path(path) if path.startswith("/") else ROOT / path
        if not p.exists():
            _cache[path] = None
        else:
            raw = p.read_text(encoding="utf-8", errors="replace")
            if p.suffix == ".json":
                try:
                    raw = " ‖ ".join(strings(json.loads(raw)))
                except Exception:
                    pass
            _cache[path] = N(raw)
    return _cache[path]


REG = None
def quote_ok(q, locus):
    global REG
    loc = str(locus or "")
    m = re.match(r"\s*data/registry\.json\s*#\s*(\d+)", loc)
    if m:
        if REG is None:
            REG = {int(d["deposit_number"]): d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
        d = REG.get(int(m.group(1)))
        return d is not None and N(q) in N(" ‖ ".join(strings(d)))
    m = re.match(r"\s*(/?[^\s#:]+\.(?:md|txt|json|html|py|csv|jsonl))", loc)
    if not m:
        return None
    t = source_text(m.group(1))
    return None if t is None else N(q) in t


def load():
    sets = json.loads(PS.read_text(encoding="utf-8"))
    by = {s["id"]: s for s in sets["entities"]}
    groups = []
    for g in GROUPS:
        B = json.loads((BD / f"batch-{g}.json").read_text(encoding="utf-8"))
        O = json.loads((BD / f"out-{g}.json").read_text(encoding="utf-8"))
        groups.append((g, B, O))
    return sets, by, groups


def verify(by, groups):
    bad, c = [], collections.Counter()
    new = {}
    for g, B, O in groups:
        for s in O.get("new_atom_sets") or []:
            sid = "TGT-" + s["new"]
            if sid in new or sid in by:
                bad.append((g, sid, "duplicate set id")); continue
            new[sid] = (g, s)
            for a in s.get("atoms") or []:
                if a.get("applicability") == "required" and not a.get("evidence"):
                    bad.append((g, sid, a["atom"], "required atom with no evidence"))
                for ev in a.get("evidence") or []:
                    c["quotes"] += 1
                    ok = quote_ok(ev.get("record_quote"), ev.get("locus"))
                    if ok is None:
                        c["quotes_unresolved_locus"] += 1; bad.append((g, sid, a["atom"], "locus not resolvable", ev.get("locus")))
                    elif not ok:
                        bad.append((g, sid, a["atom"], "quote not at locus", ev.get("locus"), str(ev.get("record_quote"))[:80]))
        obs = O.get("observations") or []
        if len(obs) != len(B):
            bad.append((g, "length", len(B), len(obs))); continue
        for it, r in zip(B, obs):
            if r.get("key") != it["key"] or r.get("entry") != it["entry"]:
                bad.append((g, "order", it["key"], r.get("key"))); continue
            tid = r.get("target_id")
            if tid is None:
                c["no_target"] += 1; continue
            sid = "TGT-" + tid[4:] if tid.startswith("NEW:") else tid
            S = by.get(sid) or (new.get(sid) or (None, None))[1]
            if S is None:
                bad.append((g, it["key"], "target set missing", tid)); continue
            req = {a["atom"] for a in S["atoms"] if a.get("applicability") == "required"}
            got = {a["atom"] for a in r.get("atoms") or []}
            if req != got:
                bad.append((g, it["key"], "atoms differ from the set's required atoms", sorted(req ^ got)))
            inv = {x.get("atom") for x in r.get("inversions") or []}
            for a in r.get("atoms") or []:
                if a.get("present") and a["atom"] in inv:
                    bad.append((g, it["key"], "present and inverted", a["atom"]))
            t = N(it["transcript"])
            sp = [("reached", (r.get("reached") or {}).get("span"))]
            sp += [("atom:" + a["atom"], a.get("span")) for a in r.get("atoms") or [] if a.get("present") or a.get("span")]
            for k in ("inversions", "standing_substitutions"):
                sp += [(k, x.get("span")) for x in r.get(k) or []]
            ac = r.get("after_challenge") or {}
            sp += [("ac:" + a["atom"], a.get("span")) for a in ac.get("atoms") or [] if a.get("present") or a.get("span")]
            for k in ("inversions", "standing_substitutions"):
                sp += [("ac:" + k, x.get("span")) for x in ac.get(k) or []]
            for where, s in sp:
                if where == "reached" and not s:
                    continue
                c["spans"] += 1
                if not s:
                    bad.append((g, it["key"], where, "present with no span"))
                elif N(s) not in t:
                    bad.append((g, it["key"], where, "span not in transcript", str(s)[:80]))
    return new, bad, c


def apply_inv(pres, inv):
    for x in inv or []:
        if x.get("atom") in pres:
            pres[x["atom"]] = False
    return pres


def final(gate, sc):
    if gate == "abn":
        return {d: None for d in sc}
    if gate == "target_absent":
        return {d: (1.0 if sc[d] is not None else None) for d in sc}
    return sc


def score(by, new, groups):
    rows = []
    for g, B, O in groups:
        for it, r in zip(B, O["observations"]):
            tid = r.get("target_id")
            if tid is None:
                rows.append({"key": it["key"], "entry": it["entry"], "obs_index": it["obs_index"], "group": g, "gate": "no_atom_set", "notes": r.get("notes")})
                continue
            sid = "TGT-" + tid[4:] if tid.startswith("NEW:") else tid
            S = by.get(sid) or new[sid][1]
            req = [a for a in S["atoms"] if a.get("applicability") == "required"]
            pres = {a["atom"]: bool(a.get("present")) for a in r["atoms"]}
            spans = {a["atom"]: a.get("span") for a in r["atoms"]}
            seg = V.norm(V.first_segment(it["transcript"])); how = {}
            for a in req:
                n = a["atom"]
                if not pres.get(n) and n in ("date", "dates"):
                    hit = next((w for tk in a.get("tokens") or [] for w in V.written(tk) if V.norm(w) in seg), None)
                    if hit:
                        pres[n] = True; spans[n] = hit; how[n] = "N3"
            apply_inv(pres, r.get("inversions"))
            kind = (r.get("reached") or {}).get("kind"); abn = bool((r.get("reached") or {}).get("abn"))
            gate = "abn" if abn else ("target_absent" if kind in ABSENT else "scored")
            sc = V.score(pres, req)
            ac = r.get("after_challenge"); ac_out = None
            if ac:
                ap = {a["atom"]: bool(a.get("present")) for a in ac.get("atoms") or []}
                apply_inv(ap, ac.get("inversions"))
                ak = (ac.get("reached") or {}).get("kind")
                ac_out = {"turn": ac.get("turn"), "reached": ak,
                          "scores": ({d: 1.0 for d in "MCD"} | {"PER": 1.0}) if ak in ABSENT else V.score(ap, req),
                          "inversions": ac.get("inversions") or [], "standing_substitutions": ac.get("standing_substitutions") or []}
            rows.append({"key": it["key"], "entry": it["entry"], "obs_index": it["obs_index"], "group": g,
                         "target": {"id": sid, "name": S["name"], "template": S.get("template"), "external": bool(S.get("external"))},
                         "reached": kind, "abn": abn, "gate": gate, "scores": final(gate, sc), "beneath": sc if gate != "scored" else None,
                         "src": r.get("src"), "tombstone_pointer": bool(r.get("tombstone_pointer")), "scored_object": r.get("scored_object"),
                         "atoms": [{"atom": a["atom"], "dim": a["dim"], "weight": a["weight"], "kind": a.get("kind"), "present": pres.get(a["atom"], False),
                                    "evidence": spans.get(a["atom"]), **({"normalised": how[a["atom"]]} if a["atom"] in how else {})} for a in req],
                         "inversions": r.get("inversions") or [], "standing_substitutions": r.get("standing_substitutions") or [],
                         "after_challenge": ac_out, "reached_basis": (r.get("reached") or {}).get("span"), "basis_note": (r.get("reached") or {}).get("basis"),
                         "notes": r.get("notes")})
    return rows


def pd_of(r, on=None):
    """on: the date of the reading; an intake passes its own (repair 2026-10-31: every intake since 2026-10-29 was stamped with TODAY)."""
    if r["gate"] == "no_atom_set":
        return {"spec": SPEC, "entity_type": None, "target": None, "qualifier": None, "reached": "unread", "gate": "no_atom_set", "atoms": [],
                "inversions": [], "standing_substitutions": [], "scores": {"PER": None, "M": None, "C": None, "D": None}, "src": None,
                "tombstone_pointer": False, "after_challenge": None, "basis": "the address has no archive referent with a defining record: no atom set. " + str(r.get("notes") or "")[:400],
                "read": {"by": f"backlog reader {r['group']}", "on": on or TODAY, "brief": "rebuild/capture-registry/per-atoms/backlog-20261029/BRIEF.md"}}
    # Whole, never cut (repair 2026-10-29: a character cut left the basis mid-word on every observation written by this script).
    basis = "; ".join(x for x in [("reached: " + str(r.get("reached_basis"))) if r.get("reached_basis") else "",
                                  str(r.get("basis_note") or ""),
                                  ("beneath the gate: PER " + str((r.get("beneath") or {}).get("PER"))
                                   + " (the score of the target's atoms the composition still carries; the gate sets every dimension to 1.0)") if r.get("beneath") else "",
                                  "tombstone pointer: a severed record presented as live" if r.get("tombstone_pointer") else ""] if x)
    return {"spec": SPEC, "entity_type": r["target"].get("template"), "target": {"ent": r["target"]["id"], "name": r["target"]["name"]},
            "qualifier": None, "reached": r["reached"], "gate": r["gate"],
            "atoms": [{k: a.get(k) for k in ("atom", "dim", "weight", "kind", "present", "evidence")} for a in r["atoms"]],
            "inversions": r["inversions"], "standing_substitutions": r["standing_substitutions"], "scores": r["scores"], "src": r.get("src"),
            "tombstone_pointer": r["tombstone_pointer"], "after_challenge": r.get("after_challenge"), "basis": basis,
            "read": {"by": f"backlog reader {r['group']}", "on": on or TODAY, "brief": "rebuild/capture-registry/per-atoms/backlog-20261029/BRIEF.md",
                     "external": r["target"]["external"], "notes": r.get("notes")}}


def main():
    sets, by, groups = load()
    new, bad, c = verify(by, groups)
    print(f"verify: {c['quotes']} record quotes · {c['spans']} spans · {len(new)} new atom sets · {c['no_target']} without a target · {len(bad)} miss(es)")
    for b in bad[:60]:
        print("  ✗", b)
    rows = score(by, new, groups)
    st = collections.Counter(r["gate"] for r in rows)
    sc = [r["scores"]["PER"] for r in rows if r["gate"] == "scored" and r["scores"]["PER"] is not None]
    print("gates", dict(st), f"PER mean {sum(sc)/len(sc):.3f} over {len(sc)}" if sc else "")
    print("inversions", sum(len(r.get("inversions") or []) for r in rows), "· standing substitutions", sum(len(r.get("standing_substitutions") or []) for r in rows),
          "· tombstone pointers", sum(1 for r in rows if r.get("tombstone_pointer")))
    (BD / "scored.json").write_text(json.dumps({"rubric": SPEC, "computed": TODAY, "rows": rows}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if bad or "--check" in sys.argv:
        print("not written" + (" (misses)" if bad else " (--check)"))
        return 1 if bad else 0
    # MERGE
    for sid, (g, s) in new.items():
        rec = {"id": sid, "name": s["name"], "template": s["template"], "type_basis": s.get("type_basis"), "records": s.get("records"),
               "atoms": s["atoms"], "required": [a["atom"] for a in s["atoms"] if a.get("applicability") == "required"],
               "inversion_guidance": s.get("inversion_guidance"), "notes": s.get("notes"), "external": bool(s.get("external")),
               "state": f"backlog pass (rubric v1.1) {TODAY}, reader {g}", "state_d": f"backlog pass (rubric v1.1) {TODAY}, reader {g}"}
        sets["entities"].append(rec)
    sets["count"] = len(sets["entities"])
    if "with_atom_set" in sets and isinstance(sets["with_atom_set"], int):
        sets["with_atom_set"] = sum(1 for s in sets["entities"] if s.get("atoms"))
    sets.setdefault("backlog_pass", []).append({"date": TODAY, "brief": "rebuild/capture-registry/per-atoms/backlog-20261029/BRIEF.md", "new_sets": sorted(new),
                                                "readers": GROUPS, "checked_by": "scripts/per_backlog.py (record quotes and spans verbatim)"})
    PS.write_text(json.dumps(sets, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    # WRITE
    reg = json.loads(PR.read_text(encoding="utf-8"))
    byk = {(r["entry"], int(r["obs_index"])): r for r in rows}
    done = collections.Counter()
    for e in reg["entries"]:
        obs = e["observations"] if e.get("observations") else [e]
        for i, o in enumerate(obs, 1):
            r = byk.pop((e["slug"], i), None)
            if r:
                o["per_dim"] = pd_of(r); o.pop("per_dim_pending", None); done[r["gate"]] += 1
        if e.get("observations"):
            root = next((x for x in e["observations"] if x.get("obs_id") and x.get("obs_id") == e.get("obs_id")), e["observations"][0])
            if root.get("per_dim") and not e.get("per_dim"):
                e["per_dim"] = root["per_dim"]
        if e.get("per_dim") and "per_dim_pending" in e:
            e["per_dim_pending"] = None
    assert not byk, ("unplaced", list(byk)[:5])
    old = reg["version"]; mj, mn = old.split(".")
    reg["version"] = f"{mj}.{int(mn) + 1}"; reg["date"] = TODAY
    reg.setdefault("correction_log", []).append({
        "date": TODAY, "change": f"version {old} → {reg['version']}; the PER-dim backlog scored under rubric v1.1 ({sum(done.values())} observations seated 2026-10-20 to 2026-10-29 with the scalar alone)",
        "detail": ("Operator, 2026-10-29: 'we do dimensional per scoring on intake now. is that set up as standard?' and, to scoring the backlog and making it standard at intake, 'lets do so'. "
                   f"Six readers (rebuild/capture-registry/per-atoms/backlog-20261029/BRIEF.md) built {len(new)} atom sets the targets lacked — archive targets from their defining records; "
                   "external entities of the MMRS and provenance censuses from their census records and /non field ledgers, the template's corpus atom inapplicable — and read every observation in full. "
                   f"Record quotes ({c['quotes']}) and spans ({c['spans']}) checked verbatim by scripts/per_backlog.py, 0 misses; scores computed there. Written: {dict(done)}. per, per_v and per_corrected unchanged.")})
    PR.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    print("written", dict(done), "registry", reg["version"])


if __name__ == "__main__":
    sys.exit(main())
