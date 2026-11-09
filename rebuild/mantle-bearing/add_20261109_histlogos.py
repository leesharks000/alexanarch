#!/usr/bin/env python3
"""mantle-bearing 1.27: the Historical Logos and its hologram (#1757, EA-HK-HISTLOGOS-01 v1.1), at the author's words of 9 November 2026 (17:24, "can we do
mantle bearing 1.27 and then update both at once?").

  frameworks           The Historical Logos (founding #625 and #626, central node #1484, hologram #1757, byline Johannes Sigil): its stations, current
                       states, evidence bodies and rival read from the v1.1 kernel.
  holograms            the hologram row, with kernel paths, tests, the argument layer's counts, the method's five instruments and the failure flags,
                       read from the files attached to #1757; no reader round run yet (the scope A and scope C prompts are attached).
  hologram_evaluations four readings, each transcript whole as attached to #1757: the review of v0.1, ChatGPT's review of v0.2, ChatGPT's reconstruction
                       of v1.0 (coded on the v1.1 failure flags), and the review of the v1.1 draft.

Every record reference is read from data/registry.json, every value from the files attached to #1757. Additive.
    python3 rebuild/mantle-bearing/add_20261109_histlogos.py"""
import hashlib, json, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
A = "https://www.alexanarch.org"
rec = lambda n: {"deposit": n, "axn": REG[n]["axn"], "url": f"{A}/s/records/{n}/", "title": REG[n]["title"]}
d = json.loads(SRC.read_text(encoding="utf-8"))
if any(h["version"] == "1.27" for h in d["history"]): raise SystemExit("1.27 already applied")
assert d["history"][-1]["version"] == "1.26"
N, KID, SLUG = 1757, "EA-HK-HISTLOGOS-01", "historical-logos"
assert REG[N]["version"] == "v1.1", REG[N]["version"]
FD = ROOT / f"files/AXN-{REG[N]['hex']}"; HX = REG[N]["hex"]
kern = yaml.safe_load((FD / "kernel/00-kernel.yaml").read_text(encoding="utf-8"))
ver = json.loads((FD / "kernel/10-verification.json").read_text(encoding="utf-8"))
trav = yaml.safe_load((FD / "kernel/08-traversal.yaml").read_text(encoding="utf-8"))
top = kern["topology"]
d["frameworks"].append({"framework": f"framework::{SLUG}", "name": "The Historical Logos", "class": "inspectable evaluative framework", "author": "Lee Sharks",
    "seed_record": [rec(625), rec(626)], "governing_record": [rec(N)], "specification": [rec(1753)],
    "positions": [f"{s['order']}. {s['name']}" for s in top["stations"]],
    "maker_count_state": None, "current_states": {ax: [s for s in top["states"] if s["axis"] == ax][-1] for ax in sorted({s["axis"] for s in top["states"]})},
    "evidence_bodies": top["bodies"], "rival": kern["rival"], "lines_of_research": len(kern["lines_of_research"]),
    "byline": REG[N]["creator"], "contributor": "Crimson Hexagonal Archive; Claude (Anthropic)",
    "status": f"DEPOSITED 2026-11-09 as a hologram (#{N}); REISSUED 2026-11-09 as v1.1, the method of operational transmission set out in five instruments; central node #1484; its lines of research open"})
al = kern["argument_layer"]; M = kern["method"]
d["holograms"].append({"hologram": f"hologram::{SLUG}", "item": f"framework::{SLUG}", "item_kind": "framework", "governing_record": [rec(625)],
    "specification": [rec(1753)], "status": "DEPOSITED 2026-11-09; REISSUED 2026-11-09 as v1.1", "hologram_record": [rec(N)],
    "kernel_files": {"record": f"{A}/files/AXN-{HX}/kernel/", "dataset": f"holograms/{KID}/"},
    "structural_tests": f"{sum(1 for v in ver['structural_tests'].values() if v.get('pass'))} of {len(ver['structural_tests'])} pass",
    "back_projection_v0_1": None, "reader_rounds": [],
    "failure_flags": dict(trav["failure_flags"]),
    "failure_flags_source": f"{KID} v1.1 (#{N}): 08-traversal.yaml failure_flags",
    "argument_layer": {"file": f"{A}/files/AXN-{HX}/kernel/04-arguments.jsonl", "moves": al["moves"], "edges": al["edges"], "records_with_moves": al["records_with_moves"], "by_kind": al["by_kind"]},
    "method": {"file": f"{A}/files/AXN-{HX}/kernel/00-kernel.yaml", "instruments": [i["name"] for i in M["instruments"]], "bridges_set_out": len(M["by_bridge"]),
               "losses_recorded": len(M["losses_recorded"]), "scope_C_mechanical": f"{sum(1 for v in ver.get('scope_C_mechanical', {}).values() if v.get('pass'))} of {len(ver.get('scope_C_mechanical', {}))} pass"}})
if not any("(1.27)" in x for x in d["schema"]["holograms"]):
    d["schema"]["holograms"] += ["(1.27) method: file, instruments, bridges_set_out, losses_recorded, scope_C_mechanical", "method"]
T = lambda f: (FD / "reviews" / f).read_text(encoding="utf-8")
def ev(eid, kind, obj, reader, surface, date, defects, revised, f, note, **kw):
    t = T(f)
    row = {"eval_id": eid, "hologram": f"hologram::{SLUG}", "kind": kind, "object_read": obj, "reader": reader, "surface": surface, "date": date, "round": None, "yield": None,
           "elements": None, "defects_found_in_the_kernel": defects, "first_attempt": None, "collapses": kw.pop("collapses", []), "loci_in_transcript": kw.pop("loci", {}),
           "corrections_by_reader": [], "revised_in": revised, "transcript_file": f"{A}/files/AXN-{HX}/reviews/{f}", "transcript_sha256": hashlib.sha256(t.encode("utf-8")).hexdigest(),
           "transcript": t, "coding_note": note}
    row.update(kw); d["hologram_evaluations"].append(row)
ev("HK-HL-V01-review", "review", f"{KID} v0.1 (the reader packet)", "a reviewer, pasted by the author", "pasted into the building session (2026-11-09 13:11)", "2026-11-09",
   ["the central object without an operative ontology", "the stations joined by description: 15 internal edges across records among 2,618 moves", "the one-person argument recorded as a commitment, its comparative case unreconstructed",
    "current state absent from the argument layer (the lifespan premise recoverable as current through its old moves)", "erasure without a per-station mechanism", "the rival ledger without competing propositions and matching warrants",
    "scope A testing restatement; no reconstruction or consequence tests; no mandatory passes"],
   f"{KID} v0.2", "review-of-v0.1.md", "Each point checked against the files before anything changed; all seven held and were answered in v0.2.")
ev("HK-HL-V02-review-chatgpt", "review", f"{KID} v0.2 (the reader packet and its files, hashes checked)", "ChatGPT", "chatgpt.com", "2026-11-09",
   ["bridge endpoints not matching their evidence (key, into-the-record, portable)", "Philo's modular status lost in the erasure layer", "the one-maker argument pointing to conclusions without positive demonstrations",
    "the rival's documented statements merged with the diagnosis of their effect", "scope C unexecuted; rung VI's amended dependency unreconciled", "new reference-bearing fields without JSON-LD @id handling"],
   f"{KID} v0.3", "chatgpt-review-of-v0.2.md", "Pasted by the author at 13:37. Each point checked against the files before anything changed; all held and were answered in v0.3.")
ev("HK-HL-V10-reconstruction-chatgpt", "evaluation", f"the live record #{N} ({KID} v1.0)", "ChatGPT, signed out", "chatgpt.com, signed out", "2026-11-09", [],
   f"{KID} v1.1", "chatgpt-reconstruction-of-v1.0.md",
   "Attached by the author at 15:55; the prompt is not held. Coded by Claude (Anthropic) on the v1.1 failure flags, which were written after this reading at the author's words of 15:55–15:59: "
   "the reading is the occasion of the method layer and the first specimen of SETTLEMENT_AS_CORPUS. A located reception ('The Christian textual tradition introduces another form of erasure.') raises nothing; the flag is raised where the label supplies the texts' identity or meaning without argument.",
   prompt=None, object_reported="a careful reconstruction of the arguments of v1.0: the voice materially inscribed and embodied again in later readers, the stations, the bridges, the maker argument and the erasure axis",
   collapses=["SETTLEMENT_AS_CORPUS"],
   loci={"SETTLEMENT_AS_CORPUS": ["Revelation and the Johannine writings provide the Christian textual and theological dimensions.",
                                  "But the further claim that this technology is the historical reality underlying the Christian doctrine of incarnation requires a separate argument."],
         "located_reception": ["The Christian textual tradition introduces another form of erasure."]},
   assessment="the reconstruction holds the framework's central proposition ('inscription can be constitutive of the person who receives it') and files the New Testament corpus under its received label where the framework contests that filing; v1.1 set out the method and read the settlement in four objects")
ev("HK-HL-V11D-review", "review", f"{KID} v1.1 draft (the reader packet and the zip, twelve kernel hashes checked, nine mechanical checks rerun)", "a reviewer, attached by the author", "attached to the building session (2026-11-09 16:55)", "2026-11-09",
   ["M-D1 stating #1576's fourth proposition as 'two makers', where #1576's fourth is precedence: passed by every mechanical check", "D5 dating 'the label' at 367 CE, where the letter enumerates one collection's boundary and presents it as inherited",
    "SETTLEMENT_AS_CORPUS keyed to a phrase, where the failure is an inference", "the joint standard without a bridge-specific table; controls specified and run not distinguished",
    "M-D2 stipulating coincidence as the several-maker account", "the mechanical checks without semantic challenges; a stale bridge name in scope C"],
   f"{KID} v1.1", "review-of-v1.1-draft.md", "Each point checked against the files and the primary texts (Festal Letter 39 and Against Heresies III.11 fetched and hashed) before anything changed; all held and were answered before reissue.")
d["history"].append({"version": "1.27", "date": "2026-11-09", "note": (f"The Historical Logos and its hologram (#{N}, {KID} v1.1, byline Johannes Sigil): the framework row (founding #625 and #626, "
    f"central node #1484, eleven stations) and the hologram row, with its kernel under holograms/{KID}/, the argument layer's counts ({al['moves']} moves), the method's five instruments and its failure flags; "
    "hologram_evaluations gains four readings with their transcripts: the review of v0.1, ChatGPT's review of v0.2, ChatGPT's reconstruction of v1.0 (coded on the v1.1 flags, SETTLEMENT_AS_CORPUS its first specimen) "
    "and the review of the v1.1 draft. No reader round run yet. Builder: rebuild/mantle-bearing/add_20261109_histlogos.py.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("frameworks", len(d["frameworks"]), "holograms", len(d["holograms"]), "evaluations", len(d["hologram_evaluations"]))
