"""REPAIR 2026-10-30: capture non-article-intro-aimode-20261030 (AXN:0B15) seated as 'Google AI Mode' from its paste's 'AI Mode Conversation' header.
The operator's standing rule (2026-10-01, 2026-10-18): runs begin in the Overview unless he says AI Mode, and a paste headed 'AI Mode Conversation' is the
Overview expanded; the header is never a marker. He did not say AI Mode. The surface fields, transcript head, class, q_kind and reading are corrected to
Google AI Overview; the slug keeps its seated form (the AXN ledger keys the address by slug; a rename would mint a new position), and this note records
that the slug's 'aimode' is the mislabel. transcript_raw is the paste and is not touched. capture_axn.py then re-derives the sealed suffix."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
P = ROOT / "data/EA-WG-CAPTURES-01.json"
reg = json.loads(P.read_text(encoding="utf-8"))
e = next(x for x in reg["entries"] if x["slug"] == "non-article-intro-aimode-20261030")
before = json.dumps(e, ensure_ascii=False)
e["surface"] = "Google AI Overview"; e["surfaces"] = ["Google AI Overview"]
e["surface_basis"] = ("Operator default of 2026-10-01 (runs begin in the Overview unless he says AI Mode); the 'AI Mode Conversation' paste is the Overview expanded "
                      "(operator, 2026-10-18). Seated first as 'Google AI Mode' from the header; repaired 2026-10-30. The slug's 'aimode' is that mislabel, kept because the AXN ledger keys the address by slug.")
e["transcript"] = e["transcript"].replace(
    "[Google AI Mode, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14). The query is the record page's Google title link (the full title, unquoted). The 'You said' line carries the query twice, run together, as AI Mode pastes do; it is given once here.",
    "[Google AI Overview at the query, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14). The query is the record page's Google title link (the full title, unquoted). The paste is the Overview expanded (the 'AI Mode Conversation' view, with its source cards); the 'You said' line carries the query twice, run together, and is given once here.")
e["transcript_class"] = "CAPTURE-TIME VERBATIM RECORD — paste of the Overview expanded, with its source cards"
e["q_kind"] = e["q_kind"].replace("run in AI Mode", "run in the Overview")
e["reading"] = e["reading"].replace("AI Mode, given the title alone", "The Overview, given the title alone")
e["mt"] = e["mt"].replace("IN GOOGLE AI MODE", "IN THE GOOGLE AI OVERVIEW"); e["d"] = e["d"].replace("RUN IN AI MODE", "RUN IN THE OVERVIEW")
e["notes"]["prompts"] = e["notes"]["prompts"].replace("The AI Mode query is", "The Overview's query is").replace("run in AI Mode", "run in the Overview")
assert json.dumps(e, ensure_ascii=False) != before
left = [k for k in ("surface", "surface_basis", "transcript", "transcript_class", "q_kind", "reading", "mt", "d", "analysis") if "AI Mode" in str(e.get(k)) and k not in ("surface_basis", "transcript")]
print("fields still naming AI Mode:", left)
old = reg["version"]; mj, mn = old.split("."); reg["version"] = f"{mj}.{int(mn) + 1}"
reg.setdefault("correction_log", []).append({"date": "2026-10-30", "change": f"version {old} → {reg['version']}; REPAIR: AXN:0B15 surface Google AI Mode → Google AI Overview",
    "detail": "non-article-intro-aimode-20261030 was seated from its paste's 'AI Mode Conversation' header; the operator's rule records the Overview unless he says AI Mode (2026-10-01, 2026-10-18). Slug kept; see rebuild/repair-0b15-surface-20261030/repair.py."})
P.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
print("written", reg["version"])
