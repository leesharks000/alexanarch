#!/usr/bin/env python3
"""per_dim_write.py — write the dimensional PER (rebuild/capture-registry/per-atoms/obs-pass/scored.json) into the Capture
Registry, beside the historical scalar (2026-10-19; operator: "rescore ALL the entries, retaining the historical scalar numbers").

Every observation the pass read receives per_dim; per, per_v and per_corrected are left exactly as they are. Observations whose
target the readers showed to be wrong are HELD: no per_dim is written for them until they are retargeted and re-read, and the
hold is listed in the registry's correction log with its reason. Observations the pass did not read (no transcript, controls,
targets with no atom set) receive per_dim with the matching gate and a null score, so every observation carries the field.
  python3 scripts/per_dim_write.py [--check]
"""
import json, pathlib, re, sys, collections
ROOT = pathlib.Path(__file__).resolve().parents[1]
P = ROOT / "data/EA-WG-CAPTURES-01.json"
OP = ROOT / "rebuild/capture-registry/per-atoms/obs-pass"
T = json.loads((ROOT / "rebuild/capture-registry/per-atoms/templates.json").read_text(encoding="utf-8"))
SC = json.loads((OP / "scored.json").read_text(encoding="utf-8"))
ROWS = json.loads((ROOT / "data/entity-relations.json").read_text(encoding="utf-8"))["rows"]
SETS = {s["id"]: s for s in json.loads((ROOT / "data/per-atom-sets.json").read_text(encoding="utf-8"))["entities"]}

# HOLDS: targets the readers showed to be wrong (reasons from the observation pass reports, 2026-10-19)
QUALIFIER = re.compile(r"alexanarch", re.I)
KEEP_ARCHIVE = re.compile(r"deposits|recent|records|living body|evolving|semantic economic relationship|network of materials|originals library|^\W*$", re.I)
HOLD_KEYS = {
    "OBS-c7cbe8b9d776": "concept-title query scored against the person (the logotic-loop line, #24)",
    "OBS-339f58c26ae0": "concept-title query scored against the person (Empirical Phenomenology)",
    "OBS-1a68954384a5": "concept-title query scored against the person (The Argument of the Bookshelf, #1420)",
    "OBS-df69df288b66": "'mantles as semantic object' scored against the person; the target is the mantle concept",
    "OBS-f2f54b823db3": "the Institute for Comparative Poetics scored against Johannes Sigil the person",
    "OBS-5cbed0e26f63": "misfiled transcript: the seated text is the 'johannes sigil grundrisse' Overview",
    "OBS-95b758af80c1": "misfiled transcript: the screenshot's query is 'heteronyms provenance theory'",
    "OBS-87bf2f7894a4": "the composed object is the archive's Sappho-to-Revelation argument, scored against the Book of Revelation (no atom set)",
    "OBS-e53011f27f45": "the address and composition concern PER-2 (the Wound Gauge), scored against Provenance erasure",
    "OBS-e3ced27b1466": "the query asks for the Semantic Economy Institute, scored against the concept",
    "OBS-abcdda9ac5d4": "FBDP, a component, scored against the archive",
    "OBS-1d1dc18f868a": "the 6-tuple, a component, scored against the archive",
    "OBS-e2f1086da3e6": "the 6-tuple, a component, scored against the archive",
    "OBS-692ef66b3c77": "the APZPZ genre scored against Zenodo",
    "OBS-a223ffee5ded": "the Water Giraffe Cycle volume scored against its navigation book",
    "OBS-c48bd774210e": "the Water Giraffe Cycle volume scored against its navigation book",
    "OBS-45644af1ef47": "the subject (Sen Kuro, Lee Sharks, Alexanarch) scored against Zenodo",
    "OBS-f205c9ebcb83": "the subject scored against Zenodo",
    "OBS-f6fe6a2bedbc": "the subject scored against Zenodo",
    "OBS-aee9147298c6": "the subject scored against Zenodo",
    "OBS-758eb1e187cf": "the poem 'Socrates — Let My Teacher Go From Hell' scored against Socrates the person",
    "OBS-4db0546ca4fa": "the companion paper (Protocols for Scientific Training-Layer Literature) scored against TLL",
    "OBS-c9c6e2ff6d25": "the Hugging Face dataset leesharks/the-final-time scored against leesharks.com",
    "OBS-27cb20676e73": "the Hugging Face dataset leesharks/the-final-time scored against leesharks.com",
    "OBS-f1a5eb949d41": "the leesharks Hugging Face datasets scored against leesharks.com",
    "OBS-06c9e59d156f": "the leesharks Hugging Face datasets scored against leesharks.com",
    "OBS-5b22d4c9e592": "The Final Time scored against leesharks.com",
    "OBS-a622d6153d70": "the leesharks Hugging Face datasets scored against leesharks.com",
}
SAPPHO_PRE = {("OBS-bd0bcc1a4571", "2026-06-15"), ("OBS-bd0bcc1a4571", "2026-07-27"), ("OBS-c518b3ac018e", "2026-09-15")}


def hold_reason(r, q, date):
    if r["key"] in HOLD_KEYS:
        return HOLD_KEYS[r["key"]]
    if (r["key"], str(date)) in SAPPHO_PRE:
        return "captured before the packet #1645 existed (2026-09-28); the target at the date is the reading ΦΑΙΝΕΤΑΙ ΜΟΙ (#1270)"
    if r["target"]["name"] == "Alexanarch" and QUALIFIER.search(q or ""):
        rest = QUALIFIER.sub("", q).strip(" \"?:")
        if rest and not KEEP_ARCHIVE.search(rest):
            return "'alexanarch' qualifies the address; the target is '" + rest[:60] + "' as the archive holds it"
    return None


def main():
    reg = json.loads(P.read_text(encoding="utf-8"))
    by = collections.defaultdict(list)
    for r in SC["rows"]:
        by[(r["entry"], r["obs_index"])].append(r)
    rel = collections.defaultdict(list)
    for x in ROWS:
        rel[x["entry"]].append(x)
    stats, holds = collections.Counter(), []
    for e in reg["entries"]:
        obs = e["observations"] if e.get("observations") else [e]
        for i, o in enumerate(obs, 1):
            r = (by.get((e["slug"], i)) or [None])[0]
            if r is None:
                rr = next((x for x in rel[e["slug"]] if str(x["date"]) == str(o.get("date"))), None)
                kind = (rr or {}).get("reached", {}).get("kind")
                tgt = (rr or {}).get("target", [{"ent": "unassigned"}])[0]["ent"]
                gate = "control" if kind == "control" else "no_atom_set"
                basis = ("control observation" if gate == "control" else
                         "no transcript seated" if not o.get("transcript") else
                         "the target has no atom set (no defining record, or unassigned)")
                o["per_dim"] = {"spec": T["rubric"], "entity_type": None, "target": {"ent": tgt, "name": (SETS.get(tgt) or {}).get("name")},
                                "reached": kind if kind in ("same", "weakened", "collision", "substitute", "proximal_substitute", "generic", "refused", "control") else "unread",
                                "gate": gate, "atoms": [], "scores": {"PER": None, "M": None, "C": None, "D": None}, "src": None, "basis": basis}
                stats[gate] += 1
                continue
            why = hold_reason(r, e.get("q"), o.get("date"))
            if why:
                holds.append({"entry": e["slug"], "obs": o.get("slug") or e["slug"], "key": r["key"], "reason": why})
                o.pop("per_dim", None); stats["held"] += 1
                continue
            o["per_dim"] = {"spec": T["rubric"], "entity_type": r["target"].get("template"), "target": {"ent": r["target"]["id"], "name": r["target"]["name"]},
                            "reached": r["reached"], "gate": r["gate"],
                            "atoms": [{k: a[k] for k in ("atom", "dim", "weight", "kind", "present", "evidence")} | {"token": None} for a in r["atoms"] if a["applicability"] == "required"],
                            "scores": r["scores"], "src": r["src"], "after_challenge": r["after_challenge"],
                            "basis": "; ".join(x for x in [("reached: " + str(r["reached_basis"])[:300]) if r.get("reached_basis") else "",
                                                           ("beneath the gate: PER " + str((r.get("beneath") or {}).get("PER"))) if r.get("beneath") else "",
                                                           "tombstone pointer: a severed record presented as live" if r.get("tombstone_pointer") else "",
                                                           "scored object: " + str(r.get("scored_object") or "")[:120]] if x),
                            "read": {"by": "observation pass reader, batch %d" % r["batch"], "on": "2026-10-19",
                                     "brief": "rebuild/capture-registry/per-atoms/obs-pass/BRIEF.md", "normalised": sorted({a["normalised"] for a in r["atoms"] if a.get("normalised")})}}
            stats[r["gate"]] += 1
        if e.get("observations"):
            root = next((x for x in e["observations"] if x.get("obs_id") and x.get("obs_id") == e.get("obs_id")), e["observations"][0])
            if root.get("per_dim"):
                e["per_dim"] = root["per_dim"]
            else:
                e.pop("per_dim", None)
    print(dict(stats), "holds", len(holds))
    if "--check" in sys.argv:
        return
    old = reg["version"]; mj, mn = old.split(".")
    reg["version"] = f"{mj}.{int(mn) + 1}"; reg["date"] = "2026-10-19"
    reg.setdefault("correction_log", []).append({
        "date": "2026-10-19", "change": f"version {old} → {reg['version']}; dimensional PER (per_dim, PER-dim rubric v1.0) written beside the historical scalar",
        "detail": ("Operator, 2026-10-19 21:49 EDT: 'schema change. standardize atoms by entity type. and then we rescore ALL the entries, retaining the historical scalar numbers.' "
                   "Rubric rebuild/capture-registry/per-atoms/templates.json; atom sets data/per-atom-sets.json (entity pass, 7,823 record quotes checked); 915 observations read "
                   "by 24 readers with verbatim spans (0 misses), scores computed by scripts/per_dim_score.py. per, per_v and per_corrected unchanged. "
                   f"Gates written: {dict(stats)}. Held for retargeting (no per_dim until re-read): {len(holds)}."),
        "held": holds})
    P.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    (OP / "held.json").write_text(json.dumps(holds, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
