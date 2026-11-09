#!/usr/bin/env python3
"""mantle-bearing 1.25: two frameworks and their holograms, at the author's word of 8 November 2026: "give the kernels to their primaries: rev first to
dancings, sappho to cranes. archive and claude on both. and yes, they go there too" (mantle-bearing); and, at deposit, 23:59 EST: "a last round, then
deposit, update mantle-bearing".

  frameworks           Revelation First (seed #202, hologram #1755) and The Tenth Muse (seed #1270, hologram #1756).
  holograms            both deposited, with kernel paths, tests and round 1 of back-projection, read from the files attached to each record.
  hologram_evaluations round 1 of each (eight reconstructions, scored against each packet's scope A) and ChatGPT's review of the v0.3 packages (two rows,
                       one per hologram); the review of v0.1 of And the Last Shall Be First (22:23, pasted in session) recorded without its text.

Every record reference is read from data/registry.json, every yield from the attached score files, every transcript from the attached run. Additive.
    python3 rebuild/mantle-bearing/add_20261109_holograms_rf_tm.py"""
import hashlib, json, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
A = "https://www.alexanarch.org"
rec = lambda n: {"deposit": n, "axn": REG[n]["axn"], "url": f"{A}/s/records/{n}/", "title": REG[n]["title"]}
d = json.loads(SRC.read_text(encoding="utf-8"))
if any(h["version"] == "1.25" for h in d["history"]): raise SystemExit("1.25 already applied")
assert d["history"][-1]["version"] == "1.24"
RF = next(n for n, r in REG.items() if r["title"].startswith("And the Last Shall Be First: Revelation First — The Framework Hologram"))
TM = next(n for n, r in REG.items() if r["title"].startswith("The Tenth Muse: Sappho and the Future Reader — The Framework Hologram"))
F = {}
for key, n, seed, kid, slug in [("rf", RF, 202, "EA-HK-REVFIRST-01", "revelation-first"), ("tm", TM, 1270, "EA-HK-TENTHMUSE-01", "the-tenth-muse")]:
    K = ROOT / f"files/AXN-{REG[n]['hex']}"
    kern = yaml.safe_load((K / "kernel/00-kernel.yaml").read_text(encoding="utf-8")); ver = json.loads((K / "kernel/10-verification.json").read_text(encoding="utf-8"))
    sc = yaml.safe_load((K / "reader-runs/round-1/scores-r1.yaml").read_text(encoding="utf-8"))
    F[key] = dict(n=n, seed=seed, kid=kid, slug=slug, K=K, kern=kern, ver=ver, sc=sc)
fw = lambda x, name, status: {"framework": f"framework::{x['slug']}", "name": name, "class": "inspectable evaluative framework", "author": "Lee Sharks",
    "seed_record": [rec(x["seed"])], "governing_record": [rec(x["n"])], "specification": [rec(1753)],
    "positions": ([r["rung"] + " " + r["name"] + " (" + r["fit"] + ")" for r in x["kern"]["topology"]["rungs"]] if x["slug"] == "revelation-first" else [s["seat"] + ": " + s["name"] for s in x["kern"]["topology"]["seats"]]),
    "maker_count_state": None, "current_states": {ax: [s for s in x["kern"]["topology"]["states"] if s["axis"] == ax][-1] for ax in sorted({s["axis"] for s in x["kern"]["topology"]["states"]})},
    "evidence_bodies": x["kern"]["topology"]["bodies"], "rival": x["kern"]["rival"], "lines_of_research": len(x["kern"]["lines_of_research"]),
    "byline": REG[x["n"]]["creator"], "contributor": "Crimson Hexagonal Archive; Claude (Anthropic)", "status": status}
d["frameworks"] += [fw(F["rf"], "Revelation First", f"DEPOSITED 2026-11-09 as a hologram (#{RF}); its three claims held on their own conditions, its lines of research open"),
                    fw(F["tm"], "The Tenth Muse: Sappho and the Future Reader", f"DEPOSITED 2026-11-09 as a hologram (#{TM}); Sappho in the third seat proposed, its lines of research open")]
if "current_states" not in d["schema"]["frameworks"]:
    i = d["schema"]["frameworks"].index("maker_count_state"); d["schema"]["frameworks"][i + 1:i + 1] = ["(1.25) current_states, one per axis"]
    d["schema"]["frameworks"].insert(d["schema"]["frameworks"].index("contributor"), "(1.25) byline")
def yields(sc): return {x["reader"]: x.get("yield") for x in sc["runs"]}
mean = lambda sc: sc.get("mean_yield") or (sc.get("operator_total") or {}).get("mean_yield")
def H(x, title_note):
    hx = REG[x["n"]]["hex"]
    return {"hologram": f"hologram::{x['slug']}", "item": f"framework::{x['slug']}", "item_kind": "framework", "governing_record": [rec(x["seed"])],
            "specification": [rec(1753)], "status": "DEPOSITED 2026-11-09", "hologram_record": [rec(x["n"])],
            "kernel_files": {"record": f"{A}/files/AXN-{hx}/kernel/", "dataset": f"holograms/{x['kid']}/"},
            "structural_tests": f"{sum(1 for v in x['ver']['structural_tests'].values() if v.get('pass'))} of {len(x['ver']['structural_tests'])} pass",
            "back_projection_v0_1": None,
            "reader_rounds": [{"round": 1, "packet": title_note, "yields": yields(x["sc"]), "mean": mean(x["sc"])}],
            "failure_flags": {"ONE_SIDED_BURDEN": "one framework asked, body by body, whether it is established while the other is left unasked; the received reading treated as the default",
                              **({"EARLY_FOR_FIRST": "the thesis composed as early dating (INV-1)", "RUNG_COLLAPSE": "rung V or VI read as load-bearing for I–IV, or a rung's defeat carried to a rung that does not depend on it"}
                                 if x["slug"] == "revelation-first" else
                                 {"JEALOUSY_AS_FRAMEWORK": "the framework composed as a jealousy lyric", "PROPOSAL_AS_FINDING": "Sappho in the third seat read as a finding of the records", "FACES_MERGED": "literacy, performance and the maker's agency over her persistence collapsed into one proposition"})},
            "failure_flags_source": f"{x['kid']} v1.0 (#{x['n']}): 00-kernel.yaml symmetric_ledger and invariants, 01-ontology.yaml, 09-tests.yaml adversarial_queries"}
d["holograms"] += [H(F["rf"], "v0.1 (three readers) and v0.2 (Grok)"), H(F["tm"], "v0.2")]
LAB = {"rf": "EA-HK-REVFIRST", "tm": "EA-HK-TENTHMUSE"}
for key in ("rf", "tm"):
    x = F[key]; hx = REG[x["n"]]["hex"]
    for r in x["sc"]["runs"]:
        p = x["K"] / "reader-runs/round-1" / r["file"]; T = p.read_text(encoding="utf-8")
        rid = r["file"].rsplit(".", 1)[0]
        d["hologram_evaluations"].append({"eval_id": f"HK-{'RF' if key == 'rf' else 'TM'}-R1-{rid}", "hologram": f"hologram::{x['slug']}", "kind": "reconstruction",
            "object_read": f"the v{r.get('packet', '0.2')} reader packet: the prompt and scope A (00-kernel.yaml, 01-ontology.yaml)", "reader": r["reader"],
            "surface": r.get("surface") or r["reader"], "date": "2026-11-08", "round": 1, "yield": r.get("yield"),
            "elements": {"held": r.get("held", r.get("score")), "of": r.get("elements", 12), "partial": r.get("partial")},
            "defects_found_in_the_kernel": r.get("defects_found_in_the_kernel") or r.get("findings") or [], "first_attempt": None, "collapses": [], "loci_in_transcript": {},
            "corrections_by_reader": [], "revised_in": f"{x['kid']} " + ("v0.2 and v0.3" if key == "rf" else "v0.3"), "note": r.get("note"),
            "transcript_file": f"{A}/files/AXN-{hx}/reader-runs/round-1/{r['file']}", "transcript_sha256": hashlib.sha256(T.encode("utf-8")).hexdigest(), "transcript": T,
            "coding_note": f"Scored by Claude (Anthropic) on presence of each scope-A must-survive element, with spot checks; the score file is attached to #{x['n']}."})
REV = (F["rf"]["K"] / "reviews/chatgpt-review-of-v0.3-both-kernels.txt").read_text(encoding="utf-8")
assert REV == (F["tm"]["K"] / "reviews/chatgpt-review-of-v0.3-both-kernels.txt").read_text(encoding="utf-8")
for key in ("rf", "tm"):
    x = F[key]; hx = REG[x["n"]]["hex"]
    d["hologram_evaluations"].append({"eval_id": f"HK-{'RF' if key == 'rf' else 'TM'}-V03-review-chatgpt", "hologram": f"hologram::{x['slug']}", "kind": "review",
        "object_read": "the v0.3 full packages of both kernels (twelve files each, with hashes)", "reader": "ChatGPT", "surface": "chatgpt.com", "date": "2026-11-08",
        "round": None, "yield": None, "elements": None,
        "defects_found_in_the_kernel": ([ "#1101's Space Ark identity read as an authorship state and withdrawn with the Josephus sentence", "Q6 mixing a source-fit test with a reception audit", "the ladder's VI-on-V dependency carried by a derived_from edge that licenses no transition"]
                                        if key == "rf" else ["Sappho in the third seat lacking a claim object and a status on the seat node", "the received reading's propositions (unable to write; oral composition; writing for reperformance; persistence not hers) merged"])
                                       + ["evidence bodies inherited from the record, not claim-local", "graph identifiers not coerced as JSON-LD @id; cross-kernel proxies without canonical IRIs"],
        "first_attempt": None, "collapses": [], "loci_in_transcript": {}, "corrections_by_reader": [], "revised_in": f"{x['kid']} v1.0",
        "transcript_file": f"{A}/files/AXN-{hx}/reviews/chatgpt-review-of-v0.3-both-kernels.txt", "transcript_sha256": hashlib.sha256(REV.encode("utf-8")).hexdigest(), "transcript": REV,
        "coding_note": "Each point checked against the files and the records before anything changed; all seven held. The review checked all twelve file hashes of each package."})
d["hologram_evaluations"].append({"eval_id": "HK-RF-V01-review", "hologram": "hologram::revelation-first", "kind": "review", "object_read": "EA-HK-REVFIRST-01 v0.1",
    "reader": "a reviewer, pasted by the author", "surface": "pasted into the building session", "date": "2026-11-08", "round": None, "yield": None, "elements": None,
    "defects_found_in_the_kernel": ["rung I's defeat scope", "corpus priority undefined", "rung IV's transform unbounded", "lines of research without an unchanged outcome", "rung VI's edge to the Tenth Muse's third seat"],
    "first_attempt": None, "collapses": [], "loci_in_transcript": {}, "corrections_by_reader": [], "revised_in": "EA-HK-REVFIRST-01 v0.2 and v0.3",
    "transcript_file": None, "transcript_sha256": None, "transcript": None,
    "coding_note": "Pasted into the building session at 22:23 EST; its text is not held. The points are recorded as the building session answered them."})
d["table_notes"]["holograms"] += " From 1.25 a deposited row also carries its failure flags; a round's packet may differ by reader, as it names."
d["title"] = d["title"]
d["history"].append({"version": "1.25", "date": "2026-11-09", "note": (f"Two frameworks and their holograms, at the author's word (\"they go there too\"): Revelation First (seed #202, "
    f"hologram #{RF}, And the Last Shall Be First, byline Damascus Dancings) and The Tenth Muse (seed #1270, hologram #{TM}, byline Rebekah Cranes), each with its kernel "
    "files under holograms/; hologram_evaluations gains round 1 of each (eight reconstructions) and ChatGPT's review of the v0.3 packages, one row per hologram, with the "
    "review of v0.1 of And the Last Shall Be First recorded without its text. Builder: rebuild/mantle-bearing/add_20261109_holograms_rf_tm.py.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("frameworks", len(d["frameworks"]), "holograms", len(d["holograms"]), "evaluations", len(d["hologram_evaluations"]))
