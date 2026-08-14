#!/usr/bin/env python3
"""elevate_exemplars.py — clean six records and mark them as the reading canon.

WHY EXEMPLARS AND NOT A SPECIFICATION. Every defect this registry sustained
today was a READING failure, not a parsing failure: the doubling was named in a
commit message; the blank cards came from a renderer line already read; the
schema divergence would have taken five records to see. A schema document tells a
reader what fields exist. Six seated records teach what a finding SOUNDS like,
how long an analysis runs, when a field is honestly empty, and that auth is never
inferred — none of which a schema can state.

THE SIX, and what each teaches:
  axn distributed identifiers        the baseline shape, and a collision held evenly
  alexanarch                         a longitudinal series across dates AND auth states
  20260803-stamp-reception-…png      a non-query address, a non-Google surface, citations-null
  alexanarch as a counter infra…     absence as measurement — zero citations
  "erasure skew"                     the collision register, and that `via` carries a MECHANISM
  acanthian dove                     a record that corrects itself, and an auth pair where signed-in scored LOWER

WRAPPER OPERATIONS APPLIED. Lineation restored; the source-card block lifted out
of the prose tail, where it was duplicating cite_list; Google /goto? redirect
wrappers reduced to bare [n] markers — a copy-channel artifact, not a source
address; editorial markers removed from machine_output.

ONE RULING APPLIED, outstanding since the morning: the counter-infrastructure
PASTE and the COLLAPSED-FRAME READ of the same 00:36 capture are ONE observation
with two evidence classes, not two observations. Same query, same date, same
sitting, same opening paragraph — one pasted, one photographed mid-truncation.
"""
import json, pathlib, sys, datetime, re
sys.path.insert(0, "/tmp/cl")
from clean import T

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJ = ROOT / "data/EA-WG-CAPTURES-01.json"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

CANON = {
 "axn distributed identifiers": "BASELINE — one observation, imaged, eight citations, all four PER units scored, and a collision held evenly: four archive-controlled cards against four for ID DataWeb's Attribute Exchange Network. Read this first for the shape of a complete capture.",
 "alexanarch": "LONGITUDINAL — five observations across four dates and two authentication states, spanning the surface retraction. Read this for how observations nest, what the entry face keeps, and why the display image is inherited from the ADDRESS rather than from whichever observation the entry was built on.",
 "20260803-stamp-reception-chatgpt-mandala.png": "NON-QUERY, NON-GOOGLE, CITATIONS-NULL — `q` is a filename because there was no typed string; the surface is ChatGPT; the citation count is NULL rather than zero because ChatGPT hides sources behind popups a paste cannot reach. It also carries its own correction. Read this for three things a new instance will otherwise get wrong at once.",
 "alexanarch as a counter infrastructure semantic prefix to any search": "ABSENCE AS MEASUREMENT — zero citations, and the refusal is the finding: the layer defined the operator, diagrammed a routing model and invented three worked examples, attributing none of it. Read this for why citations-null is a result and not a gap.",
 '"erasure skew"': "THE COLLISION REGISTER — and specifically that `via` carries a MECHANISM, not a shared word: 'ADJACENCY INSIDE AN ENUMERATION — erasure and skew as consecutive items in a parenthetical list of defects, not a compound term.' Read this before writing any collision note.",
 "acanthian dove": "A RECORD THAT CORRECTS ITSELF — the reading opens by retracting what a previous pass recorded. It is also one of only three auth pairs in the corpus where SIGNED-IN scored LOWER, and the reason generalises: the query has a competing basin. Read this for how a correction lives inside the record rather than in a changelog.",
}


def main():
    p = json.loads(PROJ.read_text())
    E = {e.get("q"): e for e in p["entries"]}
    cleaned = 0

    # ---- 1. merge the counter-infrastructure paste / collapsed-frame pair
    e = E["alexanarch as a counter infrastructure semantic prefix to any search"]
    obs = e["observations"]
    frame = next(o for o in obs if "[COLLAPSED]" in str(o.get("transcript") or ""))
    paste = next(o for o in obs if o is not frame
                 and str(o.get("transcript") or "").startswith('The prefix "alexanarch"'))
    paste["evidence_classes"] = [
        {"class": "paste", "note": "the composed answer, copied after expansion"},
        {"class": "collapsed frame", "note": ("the same capture photographed BEFORE expansion; legible to the "
                                              "'Show more' control and truncated there. Merged 2026-08-13: one "
                                              "capture seen two ways is one observation with two evidence classes."),
         "was_obs_id": frame.get("obs_id"), "was_slug": frame.get("slug"),
         "text_as_read": str(frame.get("transcript") or "")}]
    e["observations"] = [o for o in obs if o is not frame]

    # ---- 2. seat the cleaned transcripts
    for (q, i), text in T.items():
        ent = E[q]
        o = (ent.get("observations") or [ent])[i]
        before = str(o.get("transcript") or "")
        o["transcript_raw"] = before
        o["transcript"] = text
        o["transcript_wrapper"] = {
            "status": "granted", "granted": "2026-08-13", "granted_by": "TACHYON",
            "operations": ["lineation restored", "source-card block lifted out of the prose tail",
                           "Google /goto? redirect wrappers reduced to bare [n] markers",
                           "editorial markers removed from machine_output"],
            "raw_chars": len(before), "cleaned_chars": len(text),
            "_rule": ("The clipboard is lossy in FORM, not in semantic content. Cleaned text is canonical; the raw "
                      "paste is retained beside it as transcript_raw so what was cut stays answerable.")}
        cleaned += 1

    # ---- 3. correct an assertion I made without checking
    for q in ("alexanarch",):
        ent = E[q]
        for o in (ent.get("observations") or []):
            for c in (o.get("cite_list") or []):
                if "SoundCloud" in str(c.get("site") or "") and c.get("note"):
                    c["note"] = ("RELATION UNVERIFIED. I recorded this as 'an unrelated SoundCloud account' and "
                                 "'a bare name collision'. I did not check. The «acanthian dove» capture cites "
                                 "soundcloud.com/lee-sharks/acanthian-dove as 'an ambient/electronica track produced "
                                 "by the artist Lee Sharks', and the 2026-07-25 observation at this address describes "
                                 "Alexanarch as 'functioning as an independent music producer alias online'. Whether "
                                 "the SoundCloud Alexanarch is the operator's own account is a question for the "
                                 "operator, not an inference for me. Neither 'collision' nor 'own source' is asserted.")

    # ---- 4. mark the canon
    for q, why in CANON.items():
        E[q]["exemplar"] = {"canon": "READ-FIRST", "elevated": NOW, "teaches": why}

    p["reading_canon"] = {
        "_rule": ("READ THESE SIX BEFORE WRITING. They are not a template to fill; they are records to read. Every "
                  "defect this registry sustained on 2026-08-13 was a reading failure that no gate would have "
                  "caught, and reading five seated records in the first round would have prevented most of them."),
        "_also": ("Every filled field carries its BASIS, because a reader can weigh a basis and a parser can only "
                  "check presence. Refusals and repairs live INSIDE the corpus, not in a changelog. Verify against "
                  "the artifact a person sees, and state what was NOT verified."),
        "_not_forward_looking": ("OCR-class records are a retroactive cleanup item, not a normalization target: no "
                                 "future capture will be OCR-read. 122 transcripts still carry OCR chrome."),
        "records": [{"q": q, "slug": E[q].get("slug"), "teaches": why} for q, why in CANON.items()]}
    PROJ.write_text(json.dumps(p, indent=1, ensure_ascii=False))
    print(f"cleaned {cleaned} transcripts | merged 1 paste/frame pair | canon of {len(CANON)} marked")
    print(f"observations now: {sum(len(x.get('observations') or [x]) for x in p['entries'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
