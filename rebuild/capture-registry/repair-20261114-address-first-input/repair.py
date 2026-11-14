"""Repair of 2026-11-14: the address is the first-round input. Operator's rulings, 2026-11-14 13:30 EST: 'a second round input is not an
address'; 13:46 EST: 'correct the string, keep the old id'. Four records carried later-round inputs joined to the first with ' · ' in q.
Each q is set to its first [QUERENT] input; every input of the session is kept in notes.address_correction.session_inputs; addr_id is kept as recorded and the
prior q is kept in notes.address_correction. No record is re-keyed.   python3 repair.py"""
import json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[3]; REG = ROOT / "data/EA-WG-CAPTURES-01.json"
SLUGS = ["traverse-crimson-hexagon-sappho-room-aio-20261030", "traverse-crimson-hexagon-ichabod-spellings-aio-20261103",
         "classical-receptions-journal-ai-mediation-aio-20261110", "vox-letter-crj-stewardship-chatgpt-20261110"]
RULING = "2026-11-14 13:30 EST: 'a second round input is not an address'; 13:46 EST: 'correct the string, keep the old id'"
reg = json.loads(REG.read_text(encoding="utf-8")); done = []
for s in SLUGS:
    e = [x for x in reg["entries"] if x["slug"] == s]; assert len(e) == 1, s; e = e[0]
    inputs = re.findall(r"\[QUERENT\] ([^\n]*)", e["transcript"]); assert inputs, s
    prior = e["q"]; first = inputs[0].strip()
    assert " · " in prior and prior.startswith(first), (s, prior[:60], first[:60])
    clash = [x["slug"] for x in reg["entries"] if x is not e and (x.get("q") or "") == first and x.get("surface") == e["surface"]]; assert not clash, clash
    e["q"] = first
    e.setdefault("notes", {}); e["notes"] = e["notes"] if isinstance(e["notes"], dict) else {"prior": e["notes"]}
    e["notes"]["address_correction"] = {"date": "2026-11-14", "ruling": RULING, "prior_q": prior, "addr_id_kept": e["addr_id"], "session_inputs": inputs,
        "note": "The address is the first-round input. The addr_id was derived from the prior string and is kept as recorded so that every citation of it holds."}
    done.append((s, first[:70], len(inputs)))
REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
for d in done: print(*d, sep=" | ")
