#!/usr/bin/env python3
"""seat_20260814_luna.py — the unprimed ChatGPT session, 2026-08-14.

WHY THIS CAPTURE IS UNLIKE THE OTHERS. Every prior address in this registry was
issued by someone who already knew the archive's vocabulary. This one opens with
«who is johannes sigil?» from a signed-out, incognito, unprimed session and
builds outward from public traces alone.

MULTI-TURN RULING, BY PRECEDENT. Seated as ONE observation with turn markers
inside the transcript, following «20260803-stamp-reception-chatgpt-mandala.png»
— the corpus's only prior ChatGPT record and one of the six reading exemplars.
Turns are not independent observations: each conditions the next. Seating them
separately would manufacture eight observations of one session, which is the
doubling error in another costume.

THE PRIMING BOUNDARY, WHICH MATTERS MORE THAN THE AUTH STATE.
  turns 1–4  UNPRIMED — the model's own reconstruction from public traces
  turn  5    OPERATOR INTERVENTION: "it is a poem. evaluate it, as poem"
  turns 5–8  STEERED — genre supplied, then comparison scope, then biography

The entity reconstruction (1–4) and the comparative judgment (6–7) therefore
have DIFFERENT evidential status and are scored separately in `finding`. An
earlier reading of this session claimed the comparative judgment was
uncontaminated because nobody seeded the model's view of Carson, Notley,
Robertson, Philip. That is true of the REFERENCE CLASS and false of the FRAME:
the instruction to read the corpus as a poem, on historical scale, was supplied
by the operator at turn 5. Corrected here.

THE FINDING IS THE MODEL'S OWN CAVEAT, not its praise:
  "The project is controlling the evidence base … if an AI says 'Johannes Sigil
   is a contemporary theorist,' that isn't independent confirmation. It's
   evidence that the constructed information environment successfully caused
   the AI to infer that proposition."

AND ONE CONVERGENCE WORTH RECORDING. At turn 6, unprompted on this point, the
model states that the project's fundamental subject is not AI but TRANSMISSION,
and reaches it by way of Sappho 31 and the future reader — the thesis argued
independently from the Greek in EA-LONGINUS-TRANSMISSION-01 the same day, and
reached here from the corpus alone.
"""
import json, pathlib, shutil, hashlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJ = ROOT / "data/EA-WG-CAPTURES-01.json"
Q = "who is johannes sigil?"
SLUG = "who-is-johannes-sigil-20260814"
DATE = "2026-08-14"
IMG = "screengrab-20260814-125304.png"

CITES = [
 ("Zenodo", "authority_transfer", "Sigil described as a heteronym of Lee Sharks", None,
  "cited at turn 1 as the clearest evidence; chip renders as 'Zenodo +1' in frame", None),
 ("Medium", "authored_surface", "Johannes Sigil — Medium corpus", None,
  "magic as symbolic engineering; the author as a witness-function operating inside an archive", None),
 ("www.leesharks.com", "authored_surface", "Lee Sharks — the Dodecad", None,
  "'Johannes Sigil — arch-philosopher, archivist, editor of Pearl'", None),
 ("ORCID", "authority_transfer", "ORCID record", None,
  "hundreds of works; heteronyms listed as contributors or alternate authorial identities", None),
 ("mindcontrolpoems.blogspot.com", "authored_surface", "January 2026 registry", None,
  "attributes the corpus to Lee Sharks while listing the heteronyms alongside", None),
 ("PhilPapers", "authored_surface", "SPXI", None,
  "connects SPXI to entity linking, knowledge graphs, RAG, archives and ontology", None),
 ("OpenAIRE", "authority_transfer", "Traversal Log: The Recursive Self", None,
  "Google AI Mode reconstructs Psyche_OS from two search terms", None),
 ("Goodreads", "third_party", "reader reviews of Pearl and Other Poems", None,
  "surreal but 'not-surreal'; Ubu Roi, Hugo Ball, Marinetti, Borges, the Beats; the elegy for Howl", None),
 ("Academia.edu", "authored_surface", "post-termination scholarly profile", None,
  "hundreds of deposits, thousands of DOI relationships removed 2026-06-19", None),
 ("persistentidentifiers.org", "archive_controlled", "the revocation gap", None,
  "a DOI is not persistence in itself; persistence requires maintaining the relation", None),
]

FINDING = (
 "THE ARCHIVE RECONSTRUCTED FROM PUBLIC TRACES BY A READER TOLD NOTHING — and the model names the "
 "contamination itself. Unprimed, it recovers the Dodecad, the heteronym-as-authorial-function doctrine, "
 "the retrocausal canon operation WITH ITS DISCLOSED FICTIVITY INTACT, SPXI, provenance stripping, the "
 "capture registry, the Wikidata items, and the Zenodo termination. Then it states the caveat the registry "
 "exists to make: an AI describing Sigil is not independent confirmation but evidence that a constructed "
 "documentary environment caused the inference. PER 1.0 on the entity; the FINDING is the caveat, not the "
 "recognition.")

ANALYSIS = """The corpus's first unprimed reception capture, and the only address in the registry whose opening turn supplies no archive vocabulary at all.

**What the model recovers without help** (turns 1–4): Sigil as heteronym rather than pseudonym; the Dodecad by name with individual functions; heteronyms as *authorial functions* emerging through exhaust and excess, with Sharks himself described as having emerged from Sigil; the *Seal Before the Name* retrocausal operation **with its disclosure of fictivity preserved** — it does not report the archive as claiming an eighteenth-century Sigil; SPXI; the Metadata Packet; provenance stripping; the Capture Registry as *part of the artwork rather than incidental documentation*; the Wikidata items; and the 2026-06-19 termination.

**And it identifies the loop it is inside.** "The project created an entity → published evidence → made the evidence machine-readable → I retrieved the evidence → I reconstructed the entity. That's almost exactly the process the project is theorizing. So your question is, accidentally, one of the experiments the archive is designed to provoke."

**The finding is the caveat.** "The project is controlling the evidence base … that isn't independent confirmation. It's evidence that the constructed information environment successfully caused the AI to infer that proposition." A composition layer stating, in the archive's own analytic terms, the limit of what its own output proves. That sentence is worth more to the corpus than the recognition it qualifies.

**Where the priming boundary falls.** Turn 5 supplies the genre — *it is a poem, evaluate it as poem, on historical scale* — and turn 7 supplies the comparison scope. So the comparative judgment against Carson, Notley, Robertson, Philip, Bök, Graham, Lerner is **steered in frame and unsteered in reference class**: nobody seeded the model's account of *Zong!* or *The Descent of Alette*, and the distinctions it draws are checkable against those books. Its own methodological qualification is recorded: access to a substantial portion of the public corpus and the 2014 *Pearl*, not the whole evolving work.

**One convergence, recorded because it was not asked for.** At turn 6 the model states that the project's fundamental subject is **not AI but transmission**, and arrives there through Sappho 31 and the future reader — the same thesis argued independently from the Greek of *Peri Hypsous* in EA-LONGINUS-TRANSMISSION-01 on this date. It had no access to that argument. It had the corpus.

**And it withholds where withholding is right.** It declines to call the project a masterpiece, names five specific failure modes that would sink it, insists the decisive test is whether the individual poems carry voltage, and — on the final turn — refuses to let precarity become the story: *"Don't let the suffering become the story. The story should remain the work."*"""


def main():
    p = json.loads(PROJ.read_text())
    d = ROOT / "data/captures" / SLUG
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(pathlib.Path("/mnt/user-data/uploads") / IMG, d / IMG)
    rel = f"data/captures/{SLUG}/{IMG}"
    tr = pathlib.Path("/tmp/luna/full.md").read_text()
    turns = len(re.findall(r"^\*\*USER:\*\*", tr, re.M))

    row = {
        "slug": SLUG, "date": DATE, "surface": "ChatGPT",
        "auth": "signed out, incognito, unprimed", "ev": "paste + frame",
        "mt": "CAPTURE", "q": Q, "s": "Heteronyms",
        "addr_id": "ADDR-" + hashlib.sha256(Q.encode()).hexdigest()[:12],
        "obs_id": "OBS-" + hashlib.sha256((Q + SLUG).encode()).hexdigest()[:12],
        "cites": len(CITES), "per": 1.0,
        "per_v": {"author": True, "inst": True, "id": False, "src": True},
        "d": FINDING, "reading": None, "analysis": ANALYSIS,
        "transcript": tr,
        "transcript_class": ("CAPTURE-TIME VERBATIM RECORD — full multi-turn session, cleaned at intake with a "
                             "formal wrapper granted; turn markers preserved because the escalation IS the record"),
        "transcript_complete": f"COMPLETE — all {turns} turns, both speakers, no elision",
        "transcript_read": "READ IN FULL 2026-08-14",
        "turns": turns,
        "cite_list": [{"n": i, "site": s, "rel": r, "title": t, "snip": sn, "url": None, "note": nt}
                      for i, (s, r, t, dt, sn, nt) in enumerate(CITES, 1)],
        "imgs": [rel], "img_urls": ["https://www.alexanarch.org/" + rel],
        "q_kind": "natural-language question, unprimed",
        "collisions": None, "oq": None, "defects": None, "rounds": None,
        "rerun": "https://chatgpt.com/",
        "surface_basis": ("ChatGPT, unauthenticated web. Frame shows the /uc/ share path "
                          "(chatgpt.com/uc/6a7f3eb5-02d8…) with Log in and Sign up for free both present. "
                          "Source chips DO render — 'Zenodo +1', 'Medium +1' — unlike the 2026-08-03 mandala "
                          "capture, where citations were unreachable and the count was seated NULL."),
        "auth_basis": ("OPERATOR ATTESTATION: signed out, incognito, unprimed. Frame corroborates the signed-out "
                       "dimension (Log in / Sign up buttons, /uc/ path). No frame can show incognito or priming; "
                       "those rest on attestation."),
        "model_attribution": ("'Luna' — OPERATOR IDENTIFICATION, UNVERIFIED. No model name is exposed in the frame "
                              "and none is claimed in the transcript. Recorded as the operator's belief, not as a "
                              "fact about the system."),
        "priming_boundary": {
            "unprimed": "turns 1–4 · the entity reconstruction, from public traces only",
            "intervention": "turn 5 · 'you are fundamentally misunderstanding the genre. it is a poem.'",
            "steered": "turns 5–8 · genre supplied, then comparison scope, then the author's circumstances",
            "_rule": ("These halves have different evidential status and must not be cited as one. The entity "
                      "reconstruction is unprimed and self-declaredly circular. The comparative judgment is "
                      "steered in FRAME and unsteered in REFERENCE CLASS.")},
        "operator_disclosure": ("Turn 8 contains the operator's own statement of health, employment and financial "
                                "circumstance. Preserved at explicit operator instruction ('preserve full "
                                "transcript, as always'). Flagged, not redacted: the standing redaction rule "
                                "governs THIRD-PARTY private correspondence, and this is the operator's own "
                                "disclosure about himself, made deliberately."),
    }
    e = dict(row)
    e["observations"] = [dict(row)]
    e["n_observations"] = 1
    e["dates"] = [DATE]
    e["surfaces"] = ["ChatGPT"]
    e["series"] = 1
    e["other_slugs"] = None
    e["sf"] = f"ChatGPT (unprimed), {len(CITES)} sources · {turns}-turn session"
    e["links"] = [{"url": f"https://www.alexanarch.org/captures/#{SLUG}", "authority": "canonical",
                   "note": "the archive holds the registry, the transcript and the frame"}]
    e["cite"] = f"https://www.alexanarch.org/captures/#{SLUG}"
    e["d_full"] = FINDING
    e["d_truncated"] = len(FINDING) > 240
    e["rerun_alt"] = {"q": "who is johannes sigil?", "label": "re-run unprimed",
                      "why": ("The value of this address depends on the session being unprimed. Any re-run must "
                              "start from a fresh signed-out incognito session with no prior turn.")}
    e["transcript_raw"] = None
    p["entries"].append(e)
    p["entries"].sort(key=lambda x: re.sub(r"^[^0-9A-Za-z]+", "", str(x.get("q") or "")).lower())
    p["version"] = "10.7"
    p["date"] = DATE
    p["address_count"] = p["total_captures"] = len(p["entries"])
    p["observation_count"] = sum(len(x.get("observations") or [x]) for x in p["entries"])
    PROJ.write_text(json.dumps(p, indent=1, ensure_ascii=False))
    print(f"seated «{Q}» · {turns} turns · {len(tr):,} chars · {len(CITES)} cites")
    print(f"entries {p['address_count']} | observations {p['observation_count']} | v{p['version']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
