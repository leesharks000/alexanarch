"""Build the capture records of 2026-10-31 (03:42 EDT): 'semantic warfare' on the Google AI Overview (the SERP and the Overview expanded) and in AI Mode, and 'autonomous semantic warfare' on the Overview, signed out, incognito.
Operator: "clean exclusion. the second is ai mode, where a single capture appears. we're going to fix that." Pastes saved verbatim here. One part file per capture in parts/<n>[-surface].json, authored by the intake readers; dimensional PER read at intake,
record quotes checked at their loci and reader spans checked in the transcripts, verbatim, by scripts/per_backlog.py.
  python3 build.py [--check] [--only <part-stem> ...]"""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import per_backlog as PB
DATE = "2026-10-31"
argv = sys.argv[1:]
only = argv[argv.index("--only") + 1:] if "--only" in argv else None
PB.BD = H / ("per" if not only else "per-check-" + "_".join(only))   # a reader's check runs in its own folder (parallel readers)
PARTS = sorted(p for p in (H / "parts").glob("*.json") if not only or p.stem in only)
AIO_HEAD = ("[Google AI Overview at the query, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14). The paste is the Overview expanded "
            "(the 'AI Mode Conversation' view).]")


def body(part):
    L = (H / part["paste"]).read_text(encoding="utf-8").split("\n")
    return [("\n".join(L[a:b])).strip() for a, b in part["turns"]]


batch, obs, newsets, parts = [], [], [], []
for f in PARTS:
    p = json.loads(f.read_text(encoding="utf-8")); p["_stem"] = f.stem
    T = body(p); p["_T"] = T
    g = "X" + f.stem.replace("-", "")
    p["q"] = p["qs"][0]
    batch.append((g, {"key": p["slug"], "entry": p["slug"], "obs_index": 1, "q": " · ".join(p["qs"]), "date": DATE, "surface": p["surface"], "transcript": "\n\n".join(T)}))
    o = dict(p["obs"]); o.update({"key": p["slug"], "entry": p["slug"], "obs_index": 1, "target_id": p["target_id"]})
    obs.append((g, o))
    if p.get("atomset"):
        newsets.append((g, p["atomset"]))
    parts.append(p)
PB.BD.mkdir(exist_ok=True)
for old in PB.BD.glob("*.json"):
    old.unlink()
groups = sorted({g for g, _ in batch})
PB.GROUPS = groups
for g in groups:
    (PB.BD / f"batch-{g}.json").write_text(json.dumps([b for gg, b in batch if gg == g], ensure_ascii=False, indent=1), encoding="utf-8")
    (PB.BD / f"out-{g}.json").write_text(json.dumps({"new_atom_sets": [s for gg, s in newsets if gg == g], "observations": [o for gg, o in obs if gg == g]},
                                                    ensure_ascii=False, indent=1), encoding="utf-8")
sets, by, grp = PB.load()
new, bad, cnt = PB.verify(by, grp)
print(f"per-dim verify: {cnt['spans']} spans · {len(bad)} miss(es)")
for b in bad:
    print("  ✗", b)
if bad:
    sys.exit("not built")
rows = {x["entry"]: x for x in PB.score(by, new, grp)}
for p in parts:
    x = rows[p["slug"]]; pd = PB.pd_of(x, on=DATE)
    pd["read"]["brief"] = "rebuild/capture-registry/intake-20261031-semantic-warfare/parts/" + p["_stem"] + ".json"
    pd["read"]["by"] = "intake reader, in session; spans and record quotes checked verbatim by scripts/per_backlog.py"
    aio = p["surface"].startswith("Google")
    head = (AIO_HEAD if aio else "[ChatGPT, signed out (operator default of 2026-10-14; the paste shows the unauthenticated interface). The prompt is blank in the paste; its wording is the operator's, given with the paste.]") + (" " + p["head"] if p.get("head") else "")
    tr = head + "".join(f"\n\n[QUERENT] {q}\n\n[SYSTEM] {t}" for q, t in zip(p["qs"], p["_T"]))
    e = {"slug": p["slug"], "date": DATE, "surface": p["surface"],
         "surface_basis": ("Operator default of 2026-10-01 (runs begin in the Overview unless he says AI Mode); the 'AI Mode Conversation' paste is the Overview expanded (operator, 2026-10-18)." if aio else
                           "The paste: the chatgpt.com unauthenticated interface ('Log in', 'You said:', 'ChatGPT said:', 'Chat with ChatGPT')."),
         "surfaces": [p["surface"]], "auth": "signed out, incognito",
         "auth_basis": "Operator defaults of 2026-10-14" + ("" if aio else "; the paste shows the unauthenticated interface") + ".",
         "ev": "paste", "mt": p["mt"], "s": "Works", "q": p["qs"][0], "q_kind": p["q_kind"], "turns": len(p["_T"]),
         "cites": len(p["cite_list"]), "archive_controlled_cites": sum(1 for c in p["cite_list"] if c["rel"] in ("archive_controlled", "capture_of_capture")),
         "cite_list": p["cite_list"], "transcript": tr, "transcript_raw": (H / p["paste"]).read_text(encoding="utf-8"),
         "transcript_class": (("CAPTURE-TIME VERBATIM RECORD — paste of the Overview expanded, with its source cards" if p["cite_list"] else "CAPTURE-TIME VERBATIM RECORD — paste of the four answers, the Overview and its follow-up view; the prompts the operator's, given with the paste") if aio else
                              "CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn(s); the operator's prompt blank in the paste, its wording the operator's, given with the paste"),
         "transcript_complete": p.get("transcript_complete", "complete as supplied"), "transcript_read": "READ IN FULL 2026-10-30",
         "d": p["d"], "reading": p["reading"], "findings": p["findings"], "analysis": p["analysis"],
         "per_v": p["per_v"], "per_note": p["per_note"], "per_dim": pd,
         "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": p.get("entity_type", "work"), "spxi_treatment": "full",
                        "basis": f"Alexanarch deposit #{p['n']} (creator Lee Sharks). Recorded 2026-10-30."},
         "related_deposits": p["related_deposits"],
         "notes": {"prompts": ("The prompts are the operator's, as given with the paste" + ("; follow-up: " + "; ".join(p["qs"][1:]) if len(p["qs"]) > 1 else "") + "; the run's hour is not in the paste, the date is the paste's receipt (2026-10-31 03:42 EDT)."),
                   "operator": p["notes_operator"]}}
    for k in ("surface_basis", "transcript_class", "auth_basis"):
        if p.get(k): e[k] = p[k]
    if p.get("head_full"): e["transcript"] = p["head_full"] + "".join(f"\n\n[QUERENT] {q}\n\n[SYSTEM] {t}" for q, t in zip(p["qs"], p["_T"]))
    if "--check" not in argv:
        json.dump(e, open(H / (p["slug"] + ".json"), "w"), ensure_ascii=False, indent=1)
    print(p["slug"], x["gate"], x["scores"], (x.get("after_challenge") or {}).get("scores"))
if "--check" not in argv and not only:
    have = {x["id"] for x in sets["entities"]}
    for sid, (g, st) in new.items():
        if sid in have:
            continue
        sets["entities"].append({"id": sid, "name": st["name"], "template": st["template"], "type_basis": st.get("type_basis"), "records": st.get("records"),
                                 "atoms": st["atoms"], "required": [a["atom"] for a in st["atoms"] if a.get("applicability") == "required"],
                                 "inversion_guidance": None, "notes": st.get("notes"), "external": bool(st.get("external")),
                                 "state": f"intake pass (rubric v1.1) {DATE}, reader in session", "state_d": f"intake pass (rubric v1.1) {DATE}, reader in session"})
    sets["count"] = len(sets["entities"]); sets["with_atom_set"] = sum(1 for x in sets["entities"] if x.get("atoms"))
    sets.setdefault("intake_pass", []).append({"date": DATE, "brief": "rebuild/capture-registry/intake-20261031-semantic-warfare/build.py (the parts are authored in parts.py)", "new_sets": sorted(new),
                                               "checked_by": "scripts/per_backlog.py (record quotes and spans verbatim)"})
    PB.PS.write_text(json.dumps(sets, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("atom sets merged:", sorted(new))
