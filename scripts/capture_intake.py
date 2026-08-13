#!/usr/bin/env python3
"""capture_intake.py — THE INTAKE CONTRACT for the Capture Registry.

MANUS, 2026-08-13, setting the rule:

    "new captures require a minimum of transcript, date, and state / surface —
     logged in out, incognito not. checked against existing, exactly same
     semantic addresses (attending to quotes) go sub-captures of one address,
     novel addresses as new capture entries. from there, data extracted,
     generated, populated to schema same — analysis, observations, sources
     extraction; and locked in populating to render & machine-facing — those
     records appear the same every time."

Four stages, in order, each refusing to proceed on failure.

  1. ADMIT      minimum fields present, or the capture is not seated
  2. ROUTE      exact-string address match decides observation vs new record
  3. NORMALISE  the same derivations, computed the same way, every time
  4. EMIT       deterministic output — same input, byte-identical result

WHY EACH RULE EXISTS. Every one is a defect this registry actually sustained:

  transcript required   — 20 observations carried claims with no evidence at all.
  date required         — 5 carried the STRING "null" as a date, breaking every
                          longitudinal comparison silently.
  surface required      — 60 sat at UNRESOLVED and could not be re-run, compared
                          across surfaces, or counted by layer.
  auth required         — a blanket date rule assigned "signed in" to 161
                          observations and DESTROYED the corpus's only
                          authentication-controlled pair.
  exact-string address  — addr_id once keyed on (query, surface), so one query
                          captured on AI Overview and AI Mode became two records
                          and the page doubled.
  QUOTES ARE SIGNIFICANT— «operative semiotics» held 5 of 5 archive cards quoted
                          and 1 of 8 unquoted, and by 13 August resolved ONLY
                          under the exact-phrase operator. Quoted and unquoted
                          are DIFFERENT ADDRESSES. Normalising them together
                          would erase the corpus's decisive measured variable.
  deterministic emit    — the projection went stale within the hour of a reseat,
                          and a render defect became a data claim twice.
"""
import json, re, sys, hashlib, pathlib, unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
CANON = ROOT / "rebuild/capture-registry/EA-WG-CAPTURES-01-REBUILD.json"

VALID_AUTH = {"signed in", "signed out", "incognito", "incognito, signed out", "undetermined"}


class Refused(Exception):
    """An intake refusal. The capture is NOT seated and nothing is written."""


# ---------------------------------------------------------------- 1. ADMIT
def admit(cap):
    """Minimum viable capture. Refuse rather than seat a record that cannot be read.

    A capture without a transcript is an assertion. Without a date it cannot enter
    a series. Without a surface it cannot be re-run or compared. Without an auth
    state its result cannot be attributed to personalisation or its absence.
    """
    missing = []
    if not str(cap.get("transcript") or "").strip():
        missing.append("transcript — a capture without machine text is an assertion, not an observation")
    d = str(cap.get("date") or "").strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
        missing.append("date — must be YYYY-MM-DD, Michigan local (UTC-4 EDT). The string 'null' is not a date")
    if not str(cap.get("surface") or "").strip() or cap.get("surface") == "UNRESOLVED":
        missing.append("surface — the product and layer observed, e.g. 'Google AI Mode (native)'")
    auth = cap.get("auth") or {}
    if not isinstance(auth, dict) or auth.get("authenticated") is None:
        missing.append("auth.authenticated — true or false. Never inferred from a date")
    if isinstance(auth, dict) and auth.get("incognito") is None:
        missing.append("auth.incognito — true or false. Separate dimension from authentication")
    if missing:
        raise Refused("CAPTURE NOT ADMITTED. Missing:\n  - " + "\n  - ".join(missing))
    return True


# ---------------------------------------------------------------- 2. ROUTE
def address_key(q):
    """The address key IS the exact issued string.

    Unicode-normalised to NFC and stripped of leading/trailing whitespace, and
    NOTHING ELSE. Case is preserved. Punctuation is preserved. QUOTATION MARKS
    ARE PRESERVED, because quoting is the decisive measured variable in this
    corpus and folding the two forms together would destroy the measurement.
    """
    if q is None:
        return None
    return unicodedata.normalize("NFC", str(q)).strip()


def route(cap, registry):
    """Exact address match -> observation of that record. Novel -> new record."""
    k = address_key(cap.get("q"))
    if k is None:
        return ("new", None, "no query string; a non-query address (artifact, record render) is always novel")
    for a in registry["addresses"]:
        if address_key(a["semantic_address"].get("q_as_issued")) == k:
            return ("observation", a,
                    "EXACT ADDRESS MATCH — seats as an observation of the existing record, not a new capture")
    return ("new", None, "novel address — no existing record carries this exact string")


# ------------------------------------------------------------ 3. NORMALISE
def extract_defects(obs):
    """The same defect vocabulary, computed the same way, on every capture."""
    d = []
    cs = obs.get("citations_and_sources", {}) or {}
    cits = [c for c in (cs.get("citations") or []) if c.get("relation") != "unresolvable"]
    cc = (obs.get("classification") or {}).get("capture_conditions") or {}
    if cc.get("interaction_required_to_reveal_more"):
        d.append("truncated-by-interface")
    if (cs.get("citation_summary") or {}).get("_do_not_count"):
        d.append("unsupported-citations")
    if not cits:
        d.append("citations-null")
    if not obs.get("observed_on") or obs.get("observed_on") == "null":
        d.append("date-unresolved")
    anl = max((str(r.get("value") or "") for r in ((obs.get("analysis") or {}).get("records") or [])),
              key=len, default="")
    if anl and not (obs.get("classification") or {}).get("finding"):
        d.append("analysis-without-finding")
    return sorted(set(d))


def per_vector(obs):
    """PER is a FOUR-UNIT VECTOR. The scalar is a projection of it, never the record.

    Two receptions can both score 0.5 and be semantically opposite: author lost
    with institution kept is not institution lost with author kept.
    """
    mf = obs.get("measurement_flags") or {}
    if mf.get("per_score") is None:
        return None
    return {"author": mf.get("author_retained"), "institution": mf.get("institution_retained"),
            "identifier": mf.get("doi_retained"), "own_source": mf.get("composition_source_included"),
            "scalar": mf.get("per_score")}


# ---------------------------------------------------------------- 4. EMIT
def fingerprint(obj):
    """Deterministic fingerprint. Same input, same bytes, every run."""
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("usage: capture_intake.py <capture.json>  [--seat]")
        print("\ncapture.json minimum:")
        print(json.dumps({"q": '"exact query as issued"', "date": "2026-08-13",
                          "surface": "Google AI Mode (native)",
                          "auth": {"authenticated": False, "incognito": True},
                          "transcript": "…verbatim machine text…"}, indent=2))
        return 0
    cap = json.loads(pathlib.Path(sys.argv[1]).read_text())
    try:
        admit(cap)
    except Refused as e:
        print(e)
        return 1
    print("1. ADMIT      ok — transcript, date, surface and auth all present")
    reg = json.loads(CANON.read_text())
    kind, addr, why = route(cap, reg)
    print("2. ROUTE      %s\n              %s" % (kind.upper(), why))
    if kind == "observation":
        print("              record: «%s» (%d existing observations)"
              % (addr["semantic_address"].get("q_as_issued"), len(addr["observations"])))
    print("3. NORMALISE  defects, PER vector, citations and source strip derive from the "
          "seated observation by the same functions used on every other record")
    print("4. EMIT       fingerprint %s" % fingerprint(cap)[:16])
    print("\nDRY RUN — nothing written. Seating runs through scripts/deposit_pipeline.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
