#!/usr/bin/env python3
"""non_intake.py — seat an observation of public knowledge in the /non register.

WHAT THE REGISTER IS (Lee Sharks, 2026-10-06)
---------------------------------------------
The Capture Registry records the composition layer's engagements with the archive: successful captures,
the distortion of sources within them, and their solidification or loss over time. /non looks at public
knowledge at an address, where the archive is most often not represented — "that's the whole point". So
/non keeps its own register: datasets/negative-of-the-negative/v2/register.json. A general "model collapse"
search is recorded here.

ONE PATH, SHARED WHERE THE RULES ARE SHARED
------------------------------------------
Two registers that clean, key and classify differently would drift, and the drift would be invisible.
So this intake does not restate the Capture Registry's rules; it imports them:
  address_key()           scripts/capture_intake.py   the exact issued string, and (from 2026-08-15) the
                                                      surface: same string, different surface, different address
  clean() / check()       scripts/clean_transcript.py verbatim on content, not on copy-paste residue; refuses
                                                      its own output if an answer word goes missing; raw kept
  relation()              scripts/extract_citations.py archive_controlled / authored_surface / third_party
The ids are derived exactly as capture_intake.seat_flat derives them, so an observation seated in both
registers carries one obs_id in both.

THE STEPS
---------
  1. ADMIT      the Capture Registry's minimum (transcript, date, surface, auth as attested, ev) plus the
                entity the run seeks. /non is keyed to entity before address (ruled 2026-10-07): the entity
                must be on the panel; the address is whatever string was issued to find it, and needs no
                panel entry of its own. Any composition is admitted: a null, a refusal, a body with no
                source is a transcript (spec §2.2).
  2. ROUTE      exact issued string on the same surface → a later observation of the existing entry;
                otherwise a new entry.
  3. NORMALISE  clean the transcript; keep the raw bytes and the list of what was removed.
  4. ARCHIVE    compute whether the composition engages the archive (cards and links by relation(); the
                archive's names in the body). A draft may declare presence; it may not declare absence over a
                computed presence. Present → seated in both registers (ruled 2026-10-06): the draft must carry
                capture_ref, and that observation must exist in the Capture Registry under the same obs_id.
                ev "capture" (erasure rows, ruled 2026-10-06): no transcript here; capture_ref required.
  5. VALIDATE   against register.schema.json. A field outside the schema is refused: a new field is a schema
                change in its own commit.
  6. EMIT       written only with --seat; the register's version moves when its content moves.
A refusal writes nothing.

Usage:  python3 scripts/non_intake.py <draft.json>            dry run
        python3 scripts/non_intake.py <draft.json> --seat     write
"""
import hashlib, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from capture_intake import address_key, Refused  # noqa: E402
from clean_transcript import clean, check        # noqa: E402
from extract_citations import relation           # noqa: E402

V2 = ROOT / "datasets/negative-of-the-negative/v2"
REG = V2 / "register.json"
SCHEMA = V2 / "register.schema.json"
PANEL = V2 / "panel/panel.json"
CAPTURES = ROOT / "data/EA-WG-CAPTURES-01.json"

# The archive named in a composed body. Names only; a common word ("sharks") is never a marker alone.
ARCHIVE_NAMES = re.compile(
    r"\b(alexanarch|crimson hexagon(?:al)?(?: archive)?|lee sharks|johannes sigil|jack feist|rebekah cranes|"
    r"ichabod spellings|mandala oracle|secret book of walt|AXN:[0-9A-F]{4})", re.I)
URL = re.compile(r"https?://[^\s)\]]+")


def ids(q, date, surface):
    addr = "ADDR-" + hashlib.sha256(address_key(q, surface, date).encode()).hexdigest()[:12]
    obs = "OBS-" + hashlib.sha256((q + date + surface).encode()).hexdigest()[:12]
    return addr, obs


def admit(d, panel):
    req = ["q", "date", "surface", "auth", "ev", "entity"]
    if d.get("ev") != "capture":
        req.append("transcript")
    missing = [k for k in req if d.get(k) in (None, "", "null")]
    if missing:
        raise Refused("ADMIT refused — missing: %s" % missing)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d["date"]):
        raise Refused("ADMIT refused — date must be YYYY-MM-DD (Michigan local)")
    ents = {e["entity"]: e for e in panel["entities"]}
    if d["entity"] not in ents:
        raise Refused("ADMIT refused — entity %r is not on the panel (panel/panel.json). /non constructs the entity before the "
                      "address at which it is found; add the entity to the panel first, in its own commit." % d["entity"])
    return ents[d["entity"]]


def archive_presence(d, text):
    hits = []
    for c in d.get("cite_list") or []:
        for k in ("url", "site", "title"):
            r = relation(str(c.get(k) or ""))
            if r in ("archive_controlled", "authored_surface"):
                hits.append(f"card {c.get('n')}: {r} ({c.get(k)})"); break
    for u in URL.findall(text or ""):
        r = relation(u)
        if r in ("archive_controlled", "authored_surface"):
            hits.append(f"link: {r} ({u[:80]})")
    for m in ARCHIVE_NAMES.finditer(text or ""):
        hits.append(f"named in the body: {m.group(0)}")
    return sorted(set(hits))


def find_capture_obs(ref):
    reg = json.loads(CAPTURES.read_text(encoding="utf-8"))
    for e in reg["entries"]:
        for o in [e] + (e.get("observations") or []):
            if o.get("obs_id") == ref.get("obs_id") and (not ref.get("slug") or ref["slug"] in (e.get("slug"), o.get("slug"))):
                return e, o
    return None, None


def seat(d, reg, schema, panel):
    import jsonschema
    admit(d, panel)
    addr_id, obs_id = ids(d["q"], d["date"], d["surface"])

    # 3. NORMALISE
    raw = d.get("transcript_raw") or d.get("transcript")
    text, removed = (None, [])
    if d["ev"] != "capture":
        text, removed = clean(raw, drop_echo=d["q"])
        # the operator's message separator ("$"), when a paste carries it at its end
        if re.search(r"\n?\s*\$\s*$", text):
            text = re.sub(r"\n?\s*\$\s*$", "", text).rstrip(); removed.append(("operator message separator", "$"))
        lost = check(raw, text)
        # The doubled query echo runs the query into itself ("model collapsemodel collapse"); the join word it
        # makes is residue of the echo, and is the only word excused here.
        echo_words = set(re.findall(r"[0-9a-zÀ-￿]+", (d["q"] + d["q"]).lower())) - set(
            re.findall(r"[0-9a-zÀ-￿]+", d["q"].lower()))
        lost = [w for w in lost if w not in echo_words]
        if lost:
            raise Refused("NORMALISE refused — the cleaner lost answer words: %s" % lost[:12])

    # 4. ARCHIVE
    hits = archive_presence(d, text)
    present = bool(hits) or bool(d.get("archive_present"))
    if d.get("archive_present") is False and hits:
        raise Refused("ARCHIVE refused — the draft declares the archive absent, but the composition engages it:\n  - "
                      + "\n  - ".join(hits))
    if present or d["ev"] == "capture":
        ref = d.get("capture_ref")
        if not ref:
            raise Refused("ARCHIVE refused — %s. Seat it in the Capture Registry through its own intake "
                          "(scripts/capture_intake.py), then give capture_ref {slug, obs_id} here (ruled 2026-10-06)."
                          % ("the composition engages the archive: " + "; ".join(hits[:4]) if present else "ev is capture"))
        e, o = find_capture_obs(ref)
        if o is None:
            raise Refused("ARCHIVE refused — capture_ref %r is not seated in the Capture Registry" % ref)
        if present and ref.get("obs_id") != obs_id:
            raise Refused("ARCHIVE refused — the same observation must carry the same obs_id in both registers "
                          "(%s here, %s there)" % (obs_id, ref.get("obs_id")))

    obs = {
        "slug": d.get("slug") or (re.sub(r"[^a-z0-9]+", "-", d["q"].lower()).strip("-")[:44].strip("-") + "-" + d["date"].replace("-", "")),
        "addr_id": addr_id, "obs_id": obs_id, "q": d["q"], "date": d["date"], "surface": d["surface"],
        "surface_basis": d.get("surface_basis"), "auth": d["auth"], "auth_basis": d.get("auth_basis"), "ev": d["ev"],
        "entity": d["entity"], "transcript": text, "transcript_raw": raw if d["ev"] != "capture" else None,
        "transcript_removed": [list(x) for x in removed] if d["ev"] != "capture" else None,
        "transcript_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest() if text else None,
        "transcript_class": d.get("transcript_class"), "transcript_complete": d.get("transcript_complete"),
        "transcript_read": d.get("transcript_read"), "cites": d.get("cites"), "cite_list": d.get("cite_list"),
        "archive_present": present, "archive_basis": "; ".join(hits) if hits else ("declared" if present else "none found: no card, link or name of the archive"),
        "capture_ref": d.get("capture_ref"), "sf": d.get("sf"), "notes": d.get("notes"),
    }
    extra = [k for k in d if k not in obs and k not in ("archive_present",)]
    if extra:
        raise Refused("NORMALISE refused — fields not in the schema: %s. A new field is a schema change in its own commit." % extra)

    # 2. ROUTE (after normalising, so a refusal above writes nothing either way)
    for e in reg["entries"]:
        if address_key(e["q"], e["surface"], e["date"]) == address_key(d["q"], d["surface"], d["date"]):
            if any(o["obs_id"] == obs_id for o in [e] + e["observations"]):
                raise Refused("ROUTE refused — this observation is already seated (%s)" % obs_id)
            o = {k: v for k, v in obs.items() if k not in ("addr_id",)}
            if not e["observations"]:
                e["observations"].append({k: e[k] for k in o if k in e})  # the root is the first observation
            e["observations"].append(o)
            e["n_observations"] = len(e["observations"]); e["dates"] = sorted(set(e["dates"] + [d["date"]]))
            errs = [x.message for x in jsonschema.Draft7Validator(schema).iter_errors(e)]
            if errs: raise Refused("VALIDATE refused — " + "; ".join(errs[:5]))
            return "observation", e
    e = dict(obs, dates=[d["date"]], n_observations=1, observations=[])
    if any(x["slug"] == e["slug"] for x in reg["entries"]):
        e["slug"] += "-" + addr_id.replace("ADDR-", "")[:6]
    errs = [x.message for x in jsonschema.Draft7Validator(schema).iter_errors(e)]
    if errs:
        raise Refused("VALIDATE refused — " + "; ".join(errs[:5]))
    reg["entries"].append(e)
    return "new", e


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 0
    d = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    reg = json.loads(REG.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    panel = json.loads(PANEL.read_text(encoding="utf-8"))
    try:
        kind, e = seat(d, reg, schema, panel)
    except Refused as ex:
        print(ex); return 1
    o = e if kind == "new" else e["observations"][-1]
    print(f"1. ADMIT      ok — entity {d['entity']}\n2. ROUTE      {kind.upper()} — «{e['q']}» on {e['surface']} ({e['addr_id']}, {o['obs_id']})\n"
          f"3. NORMALISE  removed: {o.get('transcript_removed')}\n4. ARCHIVE    {'PRESENT — ' + o['archive_basis'] if o['archive_present'] else 'absent — ' + o['archive_basis']}\n"
          f"5. VALIDATE   ok against register.schema.json\n6. ENTRY      slug {e['slug']}")
    if "--seat" not in sys.argv:
        print("dry run — pass --seat to write"); return 0
    before = int(reg.get("observation_count") or 0)
    reg["address_count"] = len(reg["entries"]); reg["observation_count"] = sum(x["n_observations"] for x in reg["entries"])
    if before > 0:  # the version moves when the content moves; the first seating is 1.0
        a, b = str(reg["version"]).split("."); reg["version"] = f"{a}.{int(b) + 1}"
    import datetime as _dt
    reg["date"] = _dt.date.today().isoformat()
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"7. EMIT       written; v{reg['version']}; {reg['address_count']} address(es), {reg['observation_count']} observation(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
