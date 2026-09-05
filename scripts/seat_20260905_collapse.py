#!/usr/bin/env python3
"""seat_20260905_collapse.py — one new address: ChatGPT, signed out, unprimed, five turns on the archive's
model-collapse program (2026-09-05). Operator's paste, verbatim, in rebuild/capture-registry/intake-20260905/.

WHAT THE CAPTURE SHOWS (the reading, stated before the commit per PIPELINE.md):
  1. The Hub dataset (huggingface.co/datasets/leesharks/crimson-hexagonal-archive, published 2026-09-03) is
     already in the composer's retrieval: three citations, structurally correct (1,576 rows, substrate
     disclosures, supersession, the predictions/studies/captures/heteronyms/venues/tombstones tables).
  2. Nine citations are labelled Zenodo — the composer is composing from DOI records severed 2026-06-19
     (410) — GHOST CITATION: either Bing's pre-termination cache or the DataCite metadata that stayed
     findable while the object was withdrawn. The DOI shadow pages (s/doi/, 2026-09-04) exist for exactly
     this arrival; whether they displace the ghosts is Thursday's question.
  3. Evidence status HELD: unprompted, "the Reverse Turing Test explicitly says that it does not run the
     experiment"; three epistemic levels separated in turn 2 ("should not be collapsed into one
     evidentiary category"). The distinction the erratum #1577 protects arrived intact — the inverse of
     the SE 34 result (#1574) on the same class of surface one week earlier.
  4. Turn 5 states a transmission-boundary instrument (A→D→R→U→P; matched-corpus legibility test;
     semantic twin; "preservation is not transmission") and its limit — the epistemic missing-data
     problem: only the propositions already known to look for can be measured as exclusions.
  5. Operator's qualification: the composer saw the Hub but did not use it to find the collapse studies;
     they were reached via the Zenodo ghosts. The dataset is not yet legible as strands.
Surface: ChatGPT (web search). Auth: signed out (login prompt visible), unprimed. Evidence: paste.
"""
import json, pathlib, hashlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[1]
CANON = ROOT / "data/EA-WG-CAPTURES-01.json"
DATE = "2026-09-05"
q = "what does the crimson hexagonal archive have to say about model collapse?"
sl = "cha-model-collapse-chatgpt-unprimed-20260905"
def main():
    canon = json.loads(CANON.read_text())
    assert q not in {e.get("q") for e in canon["entries"]}, "address already seated"
    assert sl not in {e.get("slug") for e in canon["entries"]}
    tpath = ROOT / "rebuild/capture-registry/intake-20260905" / f"transcript-{sl}.md"
    transcript = tpath.read_text()
    d = ("THE COMPOSER FOUND THE HUB IN A DAY AND THE GHOSTS FIRST — asked what the archive says about model "
         "collapse, signed-out ChatGPT cited the Hugging Face dataset three times, structurally correctly, and Zenodo "
         "nine times: DOI records severed 2026-06-19 and resolving 410, composed from as if live (ghost citation). "
         "Pushed once ('you're cherry picking two deposits from a research program'), it reconstructed five strands "
         "and then the program's trajectory; evidence status held throughout (the Reverse Turing Test 'does not run "
         "the experiment'; three epistemic levels 'should not be collapsed'). Turn 5 states a transmission-boundary "
         "instrument (A→D→R→U→P) and its limit, the epistemic missing-data problem. Operator: it saw the Hub but did "
         "not use it to find the collapse studies — the dataset is not yet legible as strands.")
    entry = {
        "slug": sl, "date": DATE, "surface": "ChatGPT", "surfaces": ["ChatGPT"], "dates": [DATE],
        "auth": "signed out, unprimed", "ev": "paste",
        "q": q, "q_kind": "open question, five turns", "s": "Model collapse program",
        "cites": 21, "cite_list": None,
        "archive_controlled_cites": 12,
        "per": None, "per_v": None, "per_note": "PER not scored as a vector; the measured quantities are (a) time-to-Hub-retrieval (published 2026-09-03, cited 2026-09-05), (b) ghost-citation share (9 of 21 citations to severed Zenodo records), (c) evidence-status retention (held: proposal not converted to result).",
        "mt": "CAPTURE", "d": d, "d_full": d, "d_truncated": False,
        "reading": ("Retrieval reached the Hub dataset within two days of publication and read its card structurally; the same "
                    "composer's citation set is dominated by severed Zenodo DOIs (410), i.e. it composes from the certificate of "
                    "absence as if it were the record — the mechanism the DOI shadow pages (2026-09-04) were built to intercept. "
                    "Evidence status survived composition without priming: the RTT was reported as a protocol, not a result, "
                    "and the erratum's distinction (#1577) was reproduced by the surface it was written against."),
        "analysis": ("Three findings and one limit. (1) Hub ingress is fast: the second executable representation entered "
                     "ChatGPT's retrieval in ≤2 days. (2) Ghost citation: nine Zenodo citations name records that return 410; "
                     "either Bing's pre-termination cache or DataCite's findable metadata is supplying the content — index "
                     "divergence on the DOI axis, with the composer trusting the ghost. (3) Evidence status held, unprimed — the "
                     "inverse of #1574 on the same surface class one week earlier; the difference is that here the archive's own "
                     "apparatus states the status at the point of use. Limit (operator): the Hub was cited but not used to locate "
                     "the collapse strand; the dataset exposes rows and relations, not strands — the composer reconstructed the "
                     "program from ghosts and site pages. Turn 5's instrument (A→D→R→U→P, matched-corpus legibility, semantic "
                     "twin) and its stated blind spot (the missing-data problem) are the design for the work plan's WS5."),
        "transcript": transcript,
        "transcript_class": "CAPTURE-TIME VERBATIM RECORD — operator's paste of the full five-turn session; page chrome removed; inline source labels retained",
        "transcript_complete": "complete as supplied; five turns; the 'Sources' widget contents (per-citation URLs) were not expanded in the paste and are recorded by label only (Z/A/C/H)",
        "transcript_read": f"READ IN FULL {DATE}",
        "collisions": None, "oq": None, "imgs": [], "img_urls": [], "defects": None, "rounds": [{"n": 1, "prompt": q, "note": "two deposits returned; evidence status stated"}, {"n": 2, "prompt": "yes - but youre cherry picking two deposits froma. research program.", "note": "five strands; Hub cited; three epistemic levels"}, {"n": 3, "prompt": "yes", "note": "trajectory; recursive semantic compression"}, {"n": 4, "prompt": "and what does it mean that this archive is seemingly holistically excluded from human-mediated knowledge exchange and production?", "note": "five exclusion mechanisms; preservation is not transmission"}, {"n": 5, "prompt": "how would one measure that, and what would be the point if measuring exclusion is precisely what the system is immune to?", "note": "A\u2192D\u2192R\u2192U\u2192P; missing-data limit"}],
        "rerun": "https://chatgpt.com/?q=" + q.replace(" ", "+").replace("?", "%3F"),
        "rerun_alt": {"q": q, "label": "primed", "why": "captured UNPRIMED and signed out; a signed-in or primed rerun tests whether the ghost-citation share and the Hub citation are properties of the surface or of the session"},
        "addr_id": "ADDR-" + hashlib.sha256(q.encode()).hexdigest()[:12],
        "obs_id": "OBS-" + hashlib.sha256((q + DATE + "ChatGPT").encode()).hexdigest()[:12],
        "n_observations": 1,
        "links": [{"url": f"https://www.alexanarch.org/captures/#{sl}", "authority": "canonical", "note": "the archive holds the registry and this entry"},
                  {"url": "https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive", "authority": "cited by the composer", "note": "the Hub dataset, published 2026-09-03"}],
        "cite": f"https://www.alexanarch.org/captures/#{sl}",
        "sf": "ChatGPT, web search enabled; signed out (login prompt visible); unprimed; five turns; the operator pushed once on selection ('cherry picking') and once on exclusion.",
        "citable_unit": "address — the exact issued string on one surface, per the Surface Rule (MANUS, 2026-08-15)",
        "related_deposits": [1574, 1577, 1578, 161, 856, 783, 1573, 1556, 1540],
        "longitudinal_priors": ["what-is-the-crimson-hexagon-20260821"],
    }
    canon["entries"].append(entry)
    canon["total_captures"] = canon.get("total_captures", 0) + 1
    canon["address_count"] = canon.get("address_count", 0) + 1
    canon["observation_count"] = canon.get("observation_count", 0) + 1
    canon["version"] = "11.7"; canon["date"] = DATE
    CANON.write_text(json.dumps(canon, ensure_ascii=False, indent=1))
    (ROOT / "rebuild/capture-registry/intake-20260905" / f"{sl}.json").write_text(json.dumps({k: v for k, v in entry.items() if k != "transcript"}, ensure_ascii=False, indent=1))
    print(f"seated 1 new address; totals: {canon['total_captures']} captures")
if __name__ == "__main__": main()
