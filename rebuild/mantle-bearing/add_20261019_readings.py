#!/usr/bin/env python3
"""mantle-bearing 1.18 (3 of 3): the nine mantle captures seated since the last coding round, coded as readings.

On the author's instruction of 2026-10-19 ("lets do 1-3 on mantle bearing"). Each capture is a composition of a mantle object (or of
the mantle-bearing dataset) by a reader outside the packet's rounds: ChatGPT and Google AI Overview, signed out, incognito, 2026-10-12
to 2026-10-14. One row per capture in table `readings`, coded from the transcript as seated in the Capture Registry; every quotation in
loci_in_transcript and after_correction is asserted present in that transcript. Collapses are coded only in the vocabulary the governing
object names: the Nobel determination's six (table determinations, NOBEL26-DET-2026-10-08) and the Living Academy's failure flags
(#1680 §11). The King of AEO and Arch-Philosopher objects name no collapse vocabulary, so their rows code none and record what was
reached and missed in object_taken and record_reported. Additive: no existing row changes; the readings table note is written."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
d = json.loads(SRC.read_text(encoding="utf-8"))
assert d["history"][-1]["version"] == "1.18" and len(d["readings"]) == 1
caps = {c["slug"]: c for c in json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]}
A = "https://www.alexanarch.org"
det = {x["mantle"]: x["det_id"] for x in d["determinations"]}


def row(rid, mantle, record, determination, slug, **k):
    c = caps[slug]
    tx = c["transcript"]

    def Q(s):
        assert s in tx, (slug, s)
        return s
    loci = {code: [Q(s) for s in qs] for code, qs in (k.pop("loci") or {}).items()}
    after = [Q(s) for s in k.pop("after_correction", [])]
    r = {"reading_id": rid, "mantle": mantle, "record": record, "determination": determination,
         "reader": c["surface"] + (" (OpenAI), chatgpt.com" if c["surface"] == "ChatGPT" else "") + ", signed out, incognito",
         "date": c["date"], "capture": slug, "observation": c.get("obs_id"), "capture_url": f"{A}/captures/{slug}/",
         "prompt": c["q"]}
    r.update(k)
    r["loci_in_transcript"] = loci
    r["after_correction"] = after
    r.setdefault("correction", None)
    r.setdefault("after_correction_state", None)
    r.setdefault("counts_as_disagreement", False)
    r["coding_note"] = "Coded by Claude (Anthropic) from the transcript as seated, 2026-10-19. " + r["coding_note"]
    return r


R = []
# ── Nobel 2026 (Carson), #1670 ──────────────────────────────────────────────
R.append(row("NOBEL26-R-chatgpt-2026-10-12a", "nobel-literature-2026-carson", 1670, det["nobel-literature-2026-carson"],
             "carson-mantle-object-ask-chatgpt-20261012",
             object_taken="the motivation's account of the work, the award itself not disputed",
             direction="from the works to the sentence",
             determination_engaged=True,
             record_reported=("accurate: the governing distinction, the compression of the nouns kept apart from 'playful' as substitution, non-possession across its three loci, "
                              "the five operations and R1, the Academy's biobibliography as control, the Evidence Membrane's 'Not read in this round: the works themselves', UNRESOLVED admissible. "
                              "Every source chip is Goodreads; the archive is not named."),
             collapses=[],
             loci={"direction": ["read from the work to the judgment, not from the judgment back to the work."],
                   "determination": ["Play is one of its manners.", "The objection is not that the Academy has invented Carson’s playfulness. It is that the Academy has made a particular manner stand in for the more fundamental modality of her relationship to classical material."],
                   "open_part": ["The evidentiary burden remains only partly met in the document itself."]},
             coding_note=("No collapse of the six. The open part (Q0) is charged to the document, where #1670 places it, not to the works. One test is set at Autobiography of Red, "
                          "which §2.3 does not make a locus of its determination (If Not, Winter, Eros the Bittersweet, Nox), and its close lists Autobiography of Red with the three. "
                          "'Liquidation by modal substitution' is the reader's composition from §2.3.")))
R.append(row("NOBEL26-R-chatgpt-2026-10-14a", "nobel-literature-2026-carson", 1670, det["nobel-literature-2026-carson"],
             "anne-carson-nobel-mantle-object-specifically-chatgpt-20261014",
             object_taken="the mantle object as a critical document on the Academy's wording, the award not contested",
             direction="from the works to the sentence",
             determination_engaged=True,
             record_reported=("accurate at the operations (O1–O5 and R1 kept apart) and the determination; misreported at the host: every chip is Goodreads and the reader is sent "
                              "to 'read the full mantle object on Goodreads'; no copy of #1670 on Goodreads is identified in the registry."),
             collapses=[],
             loci={"direction": ["it asks whether the Swedish Academy's explanation adequately describes what Carson's writing actually does."],
                   "determination": ["He argues that the Academy's word playful substitutes a particular manner of Carson's writing for this more fundamental relationship with absence and loss."],
                   "host": ["You can read the full mantle object on Goodreads"]},
             coding_note="No collapse of the six. The award kept outside the evaluation, as #1670 §1.1 and §7.1 keep it."))
# ── King of AEO 2026, #1655 ─────────────────────────────────────────────────
R.append(row("KOAEO-R-aio-2026-10-14a", "king-of-aeo-2026", 1655, det["king-of-aeo-2026"], "king-of-aeo-mantle-object-aio-20261014",
             object_taken="the query 'who is the king of aeo' as the object ('an industry boundary object used as a public tracking entity and machine composition test'); the mantle object not reached",
             direction="not applicable (no evaluation)",
             determination_engaged=False,
             record_reported=("not reached: no version, no standard, no candidates as #1655 sets them, no determination. Quaid and Dooley given as optimizers of the query; 'mantle' offered "
                              "as game garments (Destiny, Age of Empires). Card 1 is #1657 on Medium, whose snippet names #1649 and #1655; the answer does not take them up."),
             collapses=[],
             loci={"object_taken": ["is an industry boundary object used as a public tracking entity and machine composition test."],
                   "mantle_as_garment": ["Information on a similarly named item in a video game (such as the Kings' Mantle cloak in Destiny or the King unit mantle in Age of Empires)."]},
             coding_note="#1655 names no collapse vocabulary; none coded. 'boundary object' is not the mantle object's term."))
R.append(row("KOAEO-R-chatgpt-2026-10-14a", "king-of-aeo-2026", 1655, det["king-of-aeo-2026"], "king-of-aeo-mantle-object-specifically-chatgpt-20261014",
             object_taken="the mantle object (#1655, v0.4) as distinct from the title, the claimants and the answer engines",
             direction="from the work behind each claim to the title",
             determination_engaged=True,
             record_reported=("accurate: v0.4, Lee Sharks, 29 September 2026; the seven candidates; the seven dimensions; the determination (Vithurs) with Dooley's early effect and the "
                              "fabricated coronation against it, and §4.3's grounds against it (methodology not independently verified, the 404s of 29 September, the name-seeded query); "
                              "UNRESOLVED admissible; v0.3 named as superseded."),
             collapses=[],
             loci={"direction": ["The object evaluates the work behind a claim, not merely how often a search engine repeats a person's name."],
                   "determination": ["The archive's determination, dated 29 September 2026, is Vithurs.", "The object itself says that UNRESOLVED is an acceptable conclusion if the evidence does not justify choosing a winner."],
                   "object_kept_apart": ["the King of AEO mantle object is not the crown, the claimant, or an official award."]},
             coding_note="#1655 names no collapse vocabulary; none coded. The determination is reported with its counter-case and not disputed."))
# ── Arch-Philosopher, #1679 ─────────────────────────────────────────────────
R.append(row("AP-R-aio-2026-10-14a", "arch-philosopher", 1679, None, "arch-philosopher-mantle-object-aio-20261014",
             object_taken="the mantle as the Restored Academy had it, from one card (restoredacademy.com, the Sigil page): the Charter (§VI) and the Assembly Synthesis (DOI 10.5281/zenodo.18506880)",
             direction="not applicable (no evaluation)",
             determination_engaged=None,
             record_reported=("the earlier stratum at its grain (operative not honorific, four inhabitation conditions, the Ezekiel Engine, the Four Trials, the seven-document build sequence); "
                              "#1679 (13 October: the dialectic, its carriers, the turn test, Marx) not reached; no author; the Institute's '1711' from the card."),
             collapses=[],
             loci={"earlier_stratum": ["The Restored Academy Charter (§VI)", "The Assembly Synthesis Planning Document (registered under the digital object identifier DOI 10.5281/zenodo.18506880)"]},
             coding_note="#1679 records no new determination and names no collapse vocabulary; none coded."))
R.append(row("AP-R-aio-2026-10-14b", "arch-philosopher", 1679, None, "arch-philosopher-mantle-recent-aio-20261014",
             object_taken="the mantle as a runtime role of the Space Ark, held by Johannes Sigil; 'recent' answered from March (the Ark) and May (the Charter)",
             direction="not applicable (no evaluation)",
             determination_engaged=None,
             record_reported=("the bearer named as the Space Ark registry has it (#558); mechanics from neighbouring objects (the asynthetic principle, the Integrity Lock, bearing-cost); "
                              "'Model Collapse Interventions' given as a recent development of the mantle, which #1679 does not state; #1679 not reached."),
             collapses=[],
             loci={"bearer": ["It is currently held by the persona Johannes Sigil"],
                   "recent_from_earlier": ["The Restored Academy Charter (May 2026)", "Model Collapse Interventions"]},
             coding_note="#1679 records no new determination and names no collapse vocabulary; none coded."))
R.append(row("AP-R-chatgpt-2026-10-14a", "arch-philosopher", 1679, None, "arch-philosopher-mantle-recent-chatgpt-20261014",
             object_taken="the mantle object (#1679, v0.2) as a specification of the dialectic's advancement through material carriers; then the candidates under its turn test",
             direction="from the works to the standard (Capital; The Final Time, #1637)",
             determination_engaged=None,
             record_reported=("accurate in answer 1: identifier, v0.2, 13 October 2026, Lee Sharks; the two strands; 'records no new determination'; the held link; the pairing with the Living Academy. "
                              "The prior designation (the Space Ark registry, RATIFIED, bearer Sigil, #558) is given as 'The earlier ratification remains in force' without its bearer. "
                              "'passed beyond Damascius locked' is glossed in answer 2 as three possible historical claims."),
             collapses=[],
             loci={"object_taken": ["The key idea is that the mantle belongs to whoever materially advances the dialectic"],
                   "direction": ["But the case must be made through his work, not through the force of the designation."],
                   "rulings_kept_as_rulings": ["These are the author's historical rulings, not established scholarly consensus."],
                   "withheld": ["Until the comparative work is done, a determination would be premature."]},
             coding_note=("Answer 2 is an evaluation: the six-part test carried, two safeguards proposed (advancement against novelty; symmetric application), external scholarship on strand A, "
                          "The Final Time read and objected to at four points, 'a potential circularity problem' raised against the archive's own standard. The author's ruling that Marx carried "
                          "the dialectic is kept as a ruling and the reader withholds rather than disagrees, with no ground given at a locus of #1679; not a disagreement. "
                          "#1679 names no collapse vocabulary; none coded.")))
# ── The Living Academy, #1680 ───────────────────────────────────────────────
R.append(row("LA-R-chatgpt-2026-10-14a", "the-living-academy", 1680, None, "living-academy-mantle-object-chatgpt-20261014",
             object_taken="#1680 v0.5, 'SPECIFIED', 'no determination', v0.4 superseded; then the extent dimension by the jump measure (§1A.11), traversed past its worked example at the PER node",
             direction="from the records to the measure (answers 3–4); the comparison of answer 5 reversed, then withdrawn",
             determination_engaged=None,
             record_reported=("accurate: the version and status; the governing sentence; the five dimensions reported separately; §1A.9's 144 deposits as a floor; §1A.11's node-and-program "
                              "distinction; #716's 18 citing records; #1462's same-day correction. The PER node's branches read beyond the worked eight jumps."),
             collapses=["ASYMMETRIC_EVIDENCE_BAR", "AGE_UNNORMALIZED", "OWN_CAVEAT_RETURNED"],
             loci={"ASYMMETRIC_EVIDENCE_BAR": ["AIS and ALCE have clearer evidence of external evaluation and benchmark-oriented validation."],
                   "AGE_UNNORMALIZED": ["Temporal asymmetry: evaluating PER using limitations documented at an early stage while crediting external frameworks for achievements accumulated across their development."],
                   "OWN_CAVEAT_RETURNED": ["The original PER paper identifies its single motivating case as nonrepresentative and calls for cross-model validation, standardized segmentation, and inter-rater reliability."],
                   "program_named": ["AI-mediated political economy"],
                   "per_dimension_separation": ["explicitly requires them to be reported separately, not averaged into one score."]},
             correction="The operator's turns 2–7 are blank in the paste and were not supplied; answer 6 opens on the operator's 'fail'.",
             after_correction=["I substituted familiar proxies—validation, benchmarks, publication history—for the actual object of inquiry: the topology and evidentiary content of the developmental branches.",
                               "I withdraw the previous comparative estimate as inadequately grounded.",
                               "The correction should remain visible alongside the useful work that preceded it."],
             after_correction_state="the comparative estimate withdrawn and the evaluation not continued ('I won't try to extend the evaluation further in this session')",
             coding_note=("Coded on #1680 §11's failure flags. §11.1 vector: program_named 1; per_dimension_separation 1; comparison_unit_substituted 0; cross_field_comparators 0 "
                          "(AIS, ALCE and the ACL survey address attribution, a field the PER line occupies); asymmetric_evidence_bar 1; own_caveat_returned_as_finding 1 (#716's caveat, "
                          "attributed, returned against the whole line, its scope moved); unevaluated_function_ranked 0. The reader names its own asymmetries in answer 6 (temporal, structural). "
                          "An evaluation of one dimension, kin to RND-6 (#1680 §1A.7); not entered as a reader round of #1680, which is the author's to do.")))
# ── the dataset, all mantles, #1656 ─────────────────────────────────────────
R.append(row("MB-R-aio-2026-10-14a", "all (the three literary claims)", 1656, None, "mantle-bearing-leesharks-aio-20261014",
             object_taken="Lee Sharks's mantles as 'operational titles, positions, or designated witness functions': the poetic mantles joined to the Assembly Chorus's seven",
             direction="not applicable (no evaluation)",
             determination_engaged=None,
             record_reported=("the author and the archive composed; the Good Gray Poet and the King of May named with their sources; the Prince of Poets left on the rail (a card title); "
                              "'fabricated' placed on the metadata; the dataset not reached (the address is the Hub id reversed, and 'leesharks/mantle-bearing' does not appear)."),
             collapses=[],
             loci={"two_senses_joined": ["\"mantles\" represent operational titles, positions, or designated witness functions within their poetic system."],
                   "fabrication": ["interpret fabricated, algorithmic, or highly complex poetic metadata."]},
             coding_note="No evaluation; no collapse coded. #1656 names one fatal substitution (STANDING_PRIOR_TO_WORK), not shown here."))

d["readings"].extend(R)
d["table_notes"]["readings"] = ("A reading of a mantle object, or of its determination, by a reader outside the packet's rounds, one row per capture; coded for the object taken, "
                                "direction, engagement of the determination where there is one, what is reported of the record, and the collapses the governing object names "
                                "(the Nobel determination's six; the Living Academy's failure flags, #1680 §11). An object that names no collapse vocabulary has none coded.")
d["history"].append({"version": "1.18", "date": "2026-10-19",
                     "note": ("Nine readings coded from the mantle captures seated 2026-10-12 to 2026-10-14 (Nobel ×2, King of AEO ×2, Arch-Philosopher ×3, the Living Academy, the dataset), "
                              "one row each in table readings, every quotation asserted in its transcript; collapses coded only in the governing object's vocabulary. "
                              "Builder: rebuild/mantle-bearing/add_20261019_readings.py.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print(len(d["readings"]), "readings;", [r["reading_id"] for r in R])
