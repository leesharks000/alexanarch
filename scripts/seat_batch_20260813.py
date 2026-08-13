#!/usr/bin/env python3
"""seat_batch_20260813.py — seat the 2026-08-13 batch and apply the surface retraction.

TWO OPERATIONS, both ruled by MANUS 2026-08-13.

1. SURFACE RETRACTION. 150 observations carried `Google AI Mode (native)` and not
   one had a basis establishing it from an image: 67 from a blanket rule unimaged,
   28 from an `AI Mode Conversation` marker unimaged, 25 from the blanket rule with
   an image the rule never consulted. The marker is falsified by this very batch —
   all twenty pastes carry it and all twenty are confirmed Overview popups.
   Ruling: June (64) -> UNDETERMINED. July and August (86) -> Google AI Overview,
   by exclusion on operator attestation. Retraction to unknown is a SUBTRACTION;
   asserting Overview across all of them would be the auth blanket inverted.

2. SEATING, STRING-KEYED. The intake contract keys an address on the exact issued
   string and nothing else; canonical still declared (q, surface). Where this batch
   matches an existing string it seats as an observation of it, migrating that
   record to string-keying. Records this batch does not touch are left for the
   full migration pass.
"""
import json, pathlib, unicodedata, hashlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CANON = ROOT / "rebuild/capture-registry/EA-WG-CAPTURES-01-REBUILD.json"
INTAKE = ROOT / "rebuild/capture-registry/intake-20260813"

def key(q): return unicodedata.normalize("NFC", str(q)).strip() if q is not None else None

def retract(reg):
    june = jul_aug = 0
    for a in reg["addresses"]:
        if a["semantic_address"]["surface"] != "Google AI Mode (native)":
            continue
        for o in a["observations"]:
            d = str(o.get("observed_on") or "")
            if d.startswith("2026-06"):
                o["surface"] = "UNDETERMINED"; june += 1
                o["surface_basis"] = ("RETRACTED 2026-08-13. The AI Mode label rested on a blanket rule or on the "
                    "'AI Mode Conversation' marker, which the 2026-08-13 batch falsifies: all twenty pastes carry "
                    "the marker and all twenty are confirmed Overview. No image establishes this surface. "
                    "Operator estimates ~20 genuine AI Mode natives corpus-wide, not individually identifiable.")
            else:
                o["surface"] = "Google AI Overview"; jul_aug += 1
                o["surface_basis"] = ("Google AI Overview BY EXCLUSION, operator attestation 2026-08-13: AI Mode was "
                    "avoided after June. The expanded Overview presented as AI Mode chrome and was recorded as the surface.")
        a["semantic_address"]["surface"] = "MIXED — see observations"
    return june, jul_aug

def seat(reg, caps):
    idx = {}
    for a in reg["addresses"]:
        idx.setdefault(key(a["semantic_address"].get("q_as_issued")), []).append(a)
    new = obs = 0
    for c in caps:
        k = key(c["q"])
        o = {"observed_on": c["date"], "surface": c["surface"], "surface_basis": c["surface_basis"],
             "auth_state": {"authenticated": c["auth"]["authenticated"], "incognito": c["auth"]["incognito"],
                            "derivation": "operator attestation 2026-08-13: signed out, incognito",
                            "basis": "stated by the operator; the Sign in pill is also present in every frame"},
             "machine_output": {"records": [{"text": c["transcript"],
                 "evidence_class": "CLEANED TRANSCRIPT — formal wrapper granted; semantic content canonical",
                 "field_of_origin": "authored at intake against the frame"}],
                 "_rule": "cleaned text is canonical; the raw paste is retained as source_transcription"},
             "source_transcription": c.get("source_transcription"),
             "transcript_wrapper": c["transcript_wrapper"],
             "citations_and_sources": {"citations": c["cite_list"], "citation_summary": {"n": c["cites"]}},
             "analysis": {"records": [{"value": c["analysis"]}]},
             "classification": {"finding": c["finding"], "capture_conditions": c["capture_conditions"]},
             "measurement_flags": {"per_v": c["per_v"], "per_score": c["per_v"].get("scalar")},
             "evidence": c["evidence"], "ai_overview_triggered": True,
             "observation_id": "OBS-" + hashlib.sha256(
                 json.dumps(c, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]}
        if k in idx:
            a = idx[k][0]
            a["observations"].append(o)
            a["longitudinal"]["n_observations"] = len(a["observations"])
            a["longitudinal"]["dates"] = sorted({x.get("observed_on") for x in a["observations"] if x.get("observed_on")})
            a["longitudinal"]["last_observed"] = max(a["longitudinal"]["dates"])
            a["longitudinal"]["is_longitudinal_series"] = len(a["longitudinal"]["dates"]) > 1
            a["semantic_address"]["_rule"] = "STRING-KEYED per the intake contract; surface demoted to the observation"
            obs += 1
        else:
            reg["addresses"].append({
                "semantic_address": {"q_as_issued": c["q"], "surface": c["surface"],
                    "address_id": "ADDR-" + hashlib.sha256(k.encode()).hexdigest()[:12],
                    "_rule": "STRING-KEYED per the intake contract",
                    "rerun_url": "https://www.google.com/search?q=" + c["q"].replace(" ", "+")},
                "address_provenance": {"surface_determined_by": "collapsed frame, 2026-08-13 batch"},
                "longitudinal": {"n_observations": 1, "first_observed": c["date"], "last_observed": c["date"],
                                 "dates": [c["date"]], "is_longitudinal_series": False},
                "observations": [o]})
            new += 1
    return new, obs

def main():
    reg = json.loads(CANON.read_text())
    before = (len(reg["addresses"]), sum(len(a["observations"]) for a in reg["addresses"]))
    june, jul_aug = retract(reg)
    caps = [json.loads(p.read_text()) for p in sorted(INTAKE.glob("capture-*.json"))]
    new, obs = seat(reg, caps)
    reg["n_addresses"] = len(reg["addresses"])
    reg["n_observations"] = sum(len(a["observations"]) for a in reg["addresses"])
    reg["date"] = "2026-08-13"
    reg["build"] = "rebuild-v0.2"
    reg["manus_rulings"].append({"date": "2026-08-13",
        "ruling": "AI Mode labels are batch mislabels of expanded Overview popups. June to null; July-August to Overview by exclusion; ~20 genuine AI Mode natives corpus-wide, not individually identifiable.",
        "applied": f"{june} observations retracted to UNDETERMINED, {jul_aug} reclassified to Google AI Overview"})
    reg["manus_rulings"].append({"date": "2026-08-13",
        "ruling": "Clean lineation, formatting and citation structure may be granted retroactively without demoting canonical status. Faithful semantic content is canonical.",
        "applied": "20 captures seated with formal wrapper granted; raw pastes retained as source_transcription"})
    CANON.write_text(json.dumps(reg, indent=1, ensure_ascii=False))
    print(f"before: {before[0]} addresses / {before[1]} observations")
    print(f"retraction: {june} -> UNDETERMINED, {jul_aug} -> Google AI Overview")
    print(f"seating: {new} new addresses, {obs} observations onto existing strings")
    print(f"after:  {reg['n_addresses']} addresses / {reg['n_observations']} observations")

if __name__ == "__main__":
    sys.exit(main())
