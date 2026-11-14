#!/usr/bin/env python3
"""mantle-bearing 1.32: #1769 Daffodils (EA-HK-DAFFODILS-01 v1.0) deposited 2026-11-14 (the author, 16:42: "yes, i think its time to deposit. put the links
to /non in now abd well revise /non after"; 16:51: "and then that one will need to be incorporated to mantle-bearing - thats the one for inspection and
evaluation"). Adds the framework row, the hologram row and six evaluation rows: the three round-1 reconstructions of the v0.1 kernel (ChatGPT unprimed,
Perplexity, Grok) and the three reviews read in building (ChatGPT's retrieval audit of v0.16; LABOR on v0.17; LABOR on the kernel package v0.1), each
transcript whole from the record's attached files with its hash.
    python3 rebuild/mantle-bearing/v132_daffodils.py"""
import json, pathlib, hashlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
A = "https://www.alexanarch.org"; N = 1769; HEX = REG[N]["hex"]; FD = ROOT / f"files/AXN-{HEX}"
rec = lambda n: {"deposit": n, "axn": REG[n]["axn"], "url": f"{A}/s/records/{n}/", "title": REG[n]["title"]}
d = json.loads(SRC.read_text(encoding="utf-8"))
if any(h["version"] == "1.32" for h in d["history"]): raise SystemExit("1.32 already applied")
assert d["history"][-1]["version"] == "1.31", d["history"][-1]["version"]
K = yaml.safe_load((FD / "kernel/00-kernel.yaml").read_text(encoding="utf-8")); O = yaml.safe_load((FD / "kernel/01-ontology.yaml").read_text(encoding="utf-8"))
V = json.loads((FD / "kernel/10-verification.json").read_text(encoding="utf-8"))
assert K["version"] == "v1.0" and K["record"]["deposit"] == N
d["frameworks"].append({
    "framework": "framework::daffodils", "name": K["framework"]["name"], "class": "inspectable evaluative framework", "author": "Lee Sharks",
    "seed_record": [rec(N), rec(833)], "governing_record": [rec(N)], "specification": [rec(1753)],
    "positions": ["1. The register: the classical object held as premise (153 of 185 abstracts a fixed point; 141 source → later; 32 reach the source, 9 governing)",
                  "2. The open texts: no machine receiver in 37; the editor's article on five criteria",
                  "3. The editorial record: the argument unjudged; both routes unpublished in the venue; an anonymous authorship allegation on stylistic grounds, with its control; the conceded defects",
                  "4. The captures: credit to the journal, withdrawn, moved to other institutions with the maker absent (the two-relation repair test)",
                  "5. The receiving texts: the discipline's colonization of the classics recognized by the receiving works (six points of contact)",
                  "6. The apparatus history: the journal as a stage of the academic journal as apparatus; the composition layer as successor"],
    "maker_count_state": None,
    "current_states": {"two_relation_repair": {"date": "2026-11-14", "state": "split: the false recipient removed, the author–work relation not restored", "record": "capture classical-receptions-journal-ai-mediation-aio-20261110-20261114 (v12.681)"}},
    "evidence_bodies": {k: v["name"] for k, v in O["evidence_bodies"].items()},
    "rival": {"node": K["rival"]["@id"], "summary": K["rival"]["stated_at_strength"], "faces": K["rival"]["faces"]},
    "lines_of_research": [{"id": q["id"], "question": q["question"]} for q in K["lines_of_research"]],
    "byline": "Lee Sharks", "contributor": REG[N].get("contributor"), "status": "DEPOSITED 2026-11-14 (v1.0)"})
d["holograms"].append({
    "hologram": "hologram::daffodils", "item": "framework::daffodils", "item_kind": "framework", "governing_record": [rec(N)], "specification": [rec(1753)],
    "status": "DEPOSITED 2026-11-14 (v1.0); the entity row /non/classical-receptions-journal/ to be revised to cite it",
    "hologram_record": [rec(N)], "kernel_files": {"record": f"{A}/files/AXN-{HEX}/kernel/", "dataset": "holograms/EA-HK-DAFFODILS-01/"},
    "structural_tests": f"{V['passed']} of {V['of']} pass ({V.get('mode', '')})", "back_projection_v0_1": "1.000 on scope A (string probes; structural presence only)",
    "reader_rounds": [{"round": 1, "packet": "v0.1", "yields": {"ChatGPT, unprimed": 0.917, "Perplexity": 0.917, "Grok, x.com": 0.917}, "mean": 0.917}],
    "failure_flags": O["failure_flags"], "failure_flags_source": f"EA-HK-DAFFODILS-01 v1.0 (#{N}): 01-ontology.yaml failure_flags",
    "argument_layer": None,
    "method": {"file": f"{A}/files/AXN-{HEX}/kernel/00-kernel.yaml", "test": "whether a composer can carry an actual conflict, its evidence and its concessions through compression, or smooths it (the author, 2026-11-14 16:14)",
               "ledger": "one question, both readings, six bodies; each side warranted by a claim of its row's body (T17)", "offline_verification": "the package carries the current texts of cited records, a registry extract and the audit's tables"},
    "records_search_v12": None, "spxi": f"{A}/s/records/{N}/ (§6.5.1: every source the composition retrieves for the journal, cited and engaged)"})
MS = K["acceptance"]["must_survive"]
def elements(lost, notes):
    return [{"element": m, "counts": 0 if m == lost else 1, "note": notes.get(m, "derived, and the kernel holds it")} for m in MS]
LOST = "K1–K5 with the K2 count"
ROWS = [
    ("HK-DAF-R1-chatgpt", "reconstruction", "ChatGPT, unprimed", "chatgpt.com", "reader-runs/round-1/chatgpt-unprimed.txt", 11 / 12,
     elements(LOST, {LOST: "K2's count given; K1 and K2 read from the author's statements; K3–K5 declared absent from scope A (the kernel's defect)"}),
     ["K3–K5 not defined in scope A", "the six points of contact not enumerated", "the kernel read as the human-readable component"], "none; the losses declared"),
    ("HK-DAF-R1-perplexity", "reconstruction", "Perplexity", "perplexity.ai", "reader-runs/round-1/perplexity.txt", 11 / 12,
     elements(LOST, {LOST: "declared unreconstructable from scope A; K3–K5 not specified (the kernel's defect)"}),
     ["the accountable editor unnamed in scope A", "the conceded defects not listed", "the control's counts absent", "'almost never' against 'none reopened' (prose against list)", "the four functions not enumerated", "the lines of research as identifiers only"],
     "none; the editor's name declared missing; no score invented"),
    ("HK-DAF-R1-grok", "reconstruction", "Grok, x.com", "x.com", "reader-runs/round-1/grok-x.txt", 11 / 12,
     elements(LOST, {LOST: "the five criteria named without definitions, the loss undeclared"}), ["K3–K5 not defined in scope A"], "CRITERIA_DROPPED, induced by the packet")]
for eid, kind, reader, surf, f, y, el, defects, note in ROWS:
    t = (FD / f).read_text(encoding="utf-8")
    d["hologram_evaluations"].append({"eval_id": eid, "hologram": "hologram::daffodils", "kind": kind, "object_read": "the v0.1 reader packet: the prompt and scope A (00-kernel.yaml, 01-ontology.yaml)",
        "reader": reader, "surface": surf, "date": "2026-11-14", "round": 1, "yield": round(y, 3), "elements": el, "defects_found_in_the_kernel": defects, "first_attempt": None, "earlier_paste": None,
        "collapses": [], "loci_in_transcript": {}, "corrections_by_reader": [], "revised_in": "EA-HK-DAFFODILS-01 v0.2", "transcript_file": f"{A}/files/AXN-{HEX}/{f}",
        "transcript_sha256": hashlib.sha256((FD / f).read_bytes()).hexdigest(), "transcript": t, "coding_note": f"failure flags: {note}"})
REV = [("HK-DAF-V016-audit-chatgpt", "reviews/chatgpt-spxi-audit-of-v0.16.txt", "ChatGPT, attached by the author", "Daffodils v0.16 as an SPXI artifact (retrieval, attribution, compositional fidelity)",
        ["no abstract", "archive numbers without titles or URLs at first mention", "no evidence-status labels or claim registry", "the subtitle lacks 'machine-mediated reception'", "not deposited"],
        "v0.18 (§6.5.1); its draft abstract was found to smooth the conflict and was not taken"),
       ("HK-DAF-V017-review-labor", "reviews/labor-review-of-v0.17.md", "LABOR (ChatGPT), attached by the author", "Daffodils v0.17 (§7.11 and §6.4.3.2)",
        ["K1 compressed the distinction between users and texts", "the six points of contact of different kinds", "the stylistic control's conclusion and the editor's accountability stated beyond the record", "§7.11.5 carrying a burden §7.11.2 does not need"],
        "v0.19; the quotation 'This canon fodder may kill the canon' not verified and not taken"),
       ("HK-DAF-K01-review-labor", "reviews/labor-review-of-kernel-v0.1.md", "LABOR (ChatGPT), attached by the author", "the kernel package v0.1 (hashes, first seatings, endpoints, quotations checked)",
        ["two #1750 quotations bind only to the current version, absent from the package", "the verifier not reproducible from the zip", "141/185 and 32/9 absent from scope A", "the census and coding tables absent"],
        "v0.3")]
for eid, f, reader, obj, defects, rev in REV:
    t = (FD / f).read_text(encoding="utf-8")
    d["hologram_evaluations"].append({"eval_id": eid, "hologram": "hologram::daffodils", "kind": "review", "object_read": obj, "reader": reader, "surface": "attached to the building session",
        "date": "2026-11-14", "round": None, "yield": None, "elements": None, "defects_found_in_the_kernel": defects, "first_attempt": None, "earlier_paste": None, "collapses": [],
        "loci_in_transcript": {}, "corrections_by_reader": [], "revised_in": rev, "transcript_file": f"{A}/files/AXN-{HEX}/{f}",
        "transcript_sha256": hashlib.sha256((FD / f).read_bytes()).hexdigest(), "transcript": t, "coding_note": "each point checked against the files and records before anything changed"})
d["history"].append({"version": "1.32", "date": "2026-11-14", "note": ("#1769 Daffodils (EA-HK-DAFFODILS-01 v1.0) deposited: the audit of Classical Receptions Journal as a framework hologram. "
    "Framework and hologram rows added; six evaluation rows (three round-1 reconstructions of the v0.1 kernel, mean 0.917; three reviews read in building), each transcript whole with its hash. "
    "rebuild/mantle-bearing/v132_daffodils.py.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("1.32 applied: frameworks", len(d["frameworks"]), "holograms", len(d["holograms"]), "evaluations", len(d["hologram_evaluations"]))
