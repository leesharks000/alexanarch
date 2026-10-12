#!/usr/bin/env python3
"""Author the capture 'what is stabilized node watch by lee sharks', ChatGPT, logged out, incognito, 2026-10-12, one answer. Source: the
answer pasted inline in the operator's message of 00:38 EDT (no interface furniture), the query and attestation in his message of 00:41
('both logged out and incognito: what is stabilized node watch by lee sharks'). NEW address; the same night's AI Overview run at #166's
full title cited nothing and invented a specification (search-form test run 17)."""
import json, re, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(ROOT))
from _chatgpt_common_20261008 import parse, transcript, cite_list
from wire_deposit import search_title_urls
from urllib.parse import quote_plus
raw = (HERE / "snw-answer-20261012-0038.txt").read_text(encoding="utf-8")
Q = "what is stabilized node watch by lee sharks"
(a1,), seen = parse("ChatGPT said:\n" + raw, {"SciVora", "TGRS", "GitHub"})
for s in ["a research framework by Lee Sharks, published in June 2026", "Establish a baseline", "Detect drift",
          "Investigate the cause: Separate observable changes from hypotheses about why they happened",
          "leaves out the researcher’s name while retaining the earlier influences and the theory itself",
          "SNW is a proposed monitoring methodology, not proof that a particular AI system is deliberately suppressing people",
          "[full Stabilized Node Watch paper (v2.0) ](https://doi.org/10.5281/zenodo.20589685)"]:
    assert s in a1, s
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
assert not any(e["q"] == Q for e in caps["entries"])
n = 166; x = reg[n]
assert x["date"] == "2026-06-08" and x["version"] == "v2.0" and x["creator"] == "Lee Sharks"
T = re.sub(r"\s+", " ", (ROOT / x["full_text_path"].lstrip("/")).read_text(encoding="utf-8"))
for s in ["Initial Observational Baseline", "Reference Commitment Model", "graded inference", "consensus core", "contestation envelope"]:
    assert s in T or s in x["description"], s
assert "distinguishes directly observed surface drift from graded inference about its cause" in x["description"]
assert "20589685" not in json.dumps(x) and "Stabilized Node Watch v2.0 (doi:10.5281/zenodo.20589685)" in (ROOT / reg[187]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
for s in ["consensus core", "contestation envelope", "Reference Commitment Model", "changepoint"]: assert s.lower() not in a1.lower(), s
RUN17 = (ROOT / "rebuild/record-pages/search-form-test/run-17-166-title-unquoted-20261012-0007.txt").read_text(encoding="utf-8")
assert "BLAKE3" in RUN17 and "Watcher Daemons" in RUN17
cl = cite_list(seen, {"GitHub": "authored_surface"})
b, ex = search_title_urls(x)
SEAT = "Seated 2026-10-12 from the answer pasted in the operator's message of 00:38 EDT, the query and attestation given at 00:41 ('both logged out and incognito')."
d = {"q": Q, "date": "2026-10-12", "surface": "ChatGPT",
 "surface_basis": "The operator's message of 00:41 (the Encyclotron run 'and' this one: 'both'); the answer's chips (SciVora +1, TGRS, GitHub +1) are ChatGPT's source-chip form. The paste carries no interface furniture.",
 "auth": "logged out, incognito", "auth_basis": "'both logged out and incognito' — operator, 2026-10-12 00:41 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "stabilized-node-watch-by-lee-sharks-chatgpt-20261012",
 "q_kind": "a framework's name with its author, after 'what is'. NEW address; the same night's AI Overview run at #166's full title cited nothing and invented a specification (search-form test run 17).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "protocol", "spxi_treatment": "full",
                "basis": "Stabilized Node Watch (#166, v2.0) is Lee Sharks's. Recorded 2026-10-12."},
 "related_deposits": [n, 187],
 "intended": {"deposit": n, "axn": x["axn"], "title": x["title"], "record": f"https://www.alexanarch.org/s/records/{n}/", "search": b, "search_exact": ex, "reached": False},
 "mt": "THE FRAMEWORK AT ITS AUTHOR'S GRAIN, ITS CAUSAL RESTRAINT KEPT",
 "d": ("THE FRAMEWORK AT ITS AUTHOR'S GRAIN, ITS CAUSAL RESTRAINT KEPT: asked what Stabilized Node Watch is, by Lee Sharks, ChatGPT gives it "
       "as his research framework of June 2026 (#166 is dated 8 June) for monitoring how AI systems represent established topics over "
       "time: a baseline, repeated observation, drift detected as missing citations, omitted contributors and narrowed arguments, and the "
       "cause investigated separately ('Separate observable changes from hypotheses about why they happened'), the specification's own "
       "distinction between observed surface drift and graded inference about its cause. Its worked example is an attribution case (a "
       "researcher's name dropped while the theory and its influences are kept), and it closes on the framework's limit ('a proposed "
       "monitoring methodology, not proof that a particular AI system is deliberately suppressing people'), linking the v2.0 paper at the "
       "DOI the archive's own #187 cites for it. The specification's machinery (the consensus core and contestation envelope, the "
       "Reference Commitment Model, changepoint detection) does not appear. Minutes earlier the AI Overview, at #166's full title, cited "
       "nothing and invented a specification under it (layers 0–3, BLAKE3 anchors, watcher daemons)."),
 "cites": sum(seen.values()) + 1, "cite_list": cl + [{"n": len(cl) + 1, "site": "doi.org", "rel": "authored_surface", "title": "full Stabilized Node Watch paper (v2.0)", "snip": None,
                                                     "url": "https://doi.org/10.5281/zenodo.20589685", "note": "inline link; the DOI #187 cites as 'Stabilized Node Watch v2.0'; resolution not checked (the archive's Zenodo account was terminated)"}],
 "archive_controlled_cites": 0,
 "sf": "Source chips expose labels only: " + "; ".join(f"{s} ×{k}" for s, k in seen.most_common()) + ". Inline link: the v2.0 paper's DOI.",
 "per": 0.75, "per_v": {"author": True, "inst": False, "id": True, "src": True},
 "per_note": "Retained: the author, the date, the version and its DOI, the method's four stages and its causal restraint. Lost: the archive and the record (#166), the specification's named components.",
 "transcript": transcript("[ChatGPT (chatgpt.com), logged out, incognito, 2026-10-12. The answer pasted inline by the operator at 00:38 EDT without interface furniture; the query from his message of 00:41. Source chips rendered inline as [chip: site +N].]", [Q], [a1]),
 "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (ONE ANSWER, PASTED INLINE; QUERY FROM THE OPERATOR'S MESSAGE; CHIPS INLINE)",
 "transcript_complete": "One answer, complete as pasted inline; the query given separately by the operator.", "transcript_read": "READ IN FULL 2026-10-12",
 "reading": ("Checked against #166. The date (2026-06-08), version (v2.0) and author agree; the description's 'distinguishes directly observed "
             "surface drift from graded inference about its cause' is the answer's fourth stage. #166's record carries no Zenodo DOI; #187's "
             "text cites 'Stabilized Node Watch v2.0 (doi:10.5281/zenodo.20589685)', the answer's link. The consensus core, contestation "
             "envelope, Initial Observational Baseline (named only as 'a baseline'), Reference Commitment Model and changepoint detection "
             "are #166's and absent."),
 "analysis": ("With the author named, the answer composes the framework at the grain of its purpose and keeps its limit, where the "
              "Overview, given the title alone, built a different object under the same name. What it carries is the specification's "
              "account of itself; what it does not carry is the apparatus that makes the account an instrument. " + SEAT),
 "findings": ["ATTRIBUTED AND DATED. Lee Sharks, June 2026, v2.0.",
              "THE CAUSAL RESTRAINT KEPT. 'Separate observable changes from hypotheses about why they happened' — #166's distinction.",
              "THE LIMIT STATED. 'a proposed monitoring methodology, not proof that a particular AI system is deliberately suppressing people'.",
              "THE APPARATUS ABSENT. Consensus core, contestation envelope, Reference Commitment Model, changepoint detection.",
              "AGAINST THE SAME NIGHT'S OVERVIEW. At the full title the AI Overview cited nothing and invented a specification (search-form test run 17)."],
 "rerun": "https://chatgpt.com/?q=" + quote_plus(Q),
 "notes": {"date_basis": "The operator's messages of 2026-10-12, 00:38 and 00:41 EDT.",
           "paired_overview": "rebuild/record-pages/search-form-test/run-17-166-title-unquoted-20261012-0007.txt",
           "verified": "Compared 2026-10-12 against #166 and the text of #187."}}
(HERE / "capture-stabilized-node-watch-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", d["cites"], dict(seen))
