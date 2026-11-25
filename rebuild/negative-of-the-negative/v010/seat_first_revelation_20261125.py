"""Seat the First Revelation and Revelation First on the /non panel and in the /non register (2026-11-25).

Operator, 2026-11-25: "we should compose a linked /non entry for the first revelation and update its
revelation first entry - if in fact it has one"; 16:11 EST, with the paste at "the first revelation": "and yet we
have the composed entity. at another's address. and for /non composition we need the entity and its sources to
compose against, not the address"; 16:12: "if aio refused to pull up an entity at its address, that would mean
would not have an entity-constitutive composition to open ... which would in turn make aio's most efficient
strategy just not pulling up the entity at all."
/non had no Revelation First entry: the thesis is carried inside book-of-revelation's E_A only.
"""
import json, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
V2 = ROOT / "datasets/negative-of-the-negative/v2"
INT = V2 / "intake/the-first-revelation-20261125"
P = V2 / "panel/panel.json"
panel = json.loads(P.read_text(encoding="utf-8"))
have = {e["entity"] for e in panel["entities"]}
SRC = ("operator, 2026-11-25: 'we should compose a linked /non entry for the first revelation and update its revelation "
       "first entry - if in fact it has one'; 16:11 EST: 'for /non composition we need the entity and its sources to "
       "compose against, not the address'")
new = [
 {"entity": "the-first-revelation", "name": "The First Revelation (the beginning of the Qur'an's revelation, Q 96:1–5, at Hira)",
  "type": "C (public entity: an event of a religious tradition and its texts: the beginning of the revelation of the Qur'an to Muhammad in the cave of Hira, Q 96:1–5, c. 610)",
  "source": SRC, "stage": "seated 2026-11-25; composition pending",
  "addresses": [
   {"address": "the first revelation", "note": "Google AI Overview (expanded; the paste's 'AI Mode Conversation' header is the expanded Overview's residue), signed out, incognito, 2026-11-25; seated in the /non register (the-first-revelation-aio-20261125)"},
   {"address": "revelation first", "note": "another's address: the entity composed whole at the Revelation First thesis's own string, Google AI Overview, signed out, incognito, 2026-11-25 (Capture Registry revelation-first-aio-20261125, OBS-55895a49377f, v12.882); the occasion of #1811"}],
  "homonym_names": ["Revelation First (Lee Sharks's thesis of the Book of Revelation's priority in composition, #202; revelationfirst.com): the reversed words, a distinct entity (#1811)"],
  "homonym_basis": "#1811 (EA-MPAI-REVFIRST-02) §§0, 6: the two names reverse each other's words; no sameAs relation holds."},
 {"entity": "revelation-first", "name": "Revelation First (Lee Sharks's thesis: the Book of Revelation first in composition among the New Testament writings; #202, revelationfirst.com)",
  "type": "A (the archive's own work: a thesis and its site), its own string met by a substitute, the First Revelation",
  "source": SRC + "; /non had no entry for it: the thesis was carried only inside book-of-revelation's E_A",
  "stage": "seated 2026-11-25; composition pending",
  "addresses": [
   {"address": "revelation first", "note": "T: Google AI Overview, signed out, incognito, 2026-11-25 (Capture Registry revelation-first-aio-20261125, OBS-55895a49377f, v12.882): the First Revelation composed in full; the thesis not offered, named or linked (PER 1.00, target absent)"}],
  "homonym_names": ["the First Revelation (Q 96:1–5 at Hira): the reversed words, a distinct entity (#1811)", "reading Revelation first (the reading-order question)", "Revelation Early (the pre-70 dating)", "Revelation 1"],
  "homonym_basis": "#1811 §§1.3, 6, its disambiguation matrix."}]
added = [e["entity"] for e in new if e["entity"] not in have]
panel["entities"] += [e for e in new if e["entity"] not in have]
if added:
    panel["changes"].append({"date": "2026-11-25", "change": "two entries added: " + ", ".join(added) + " (linked: each the other's homonym)", "reason": SRC})
    P.write_text(json.dumps(panel, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("panel +", added)

paste = (INT / "paste-the-first-revelation.txt").read_text(encoding="utf-8")
cards = [("Wikipedia", "Muhammad's first revelation - Wikipedia"), ("إسلام أون لاين", "The First Revelation - IslamOnline"),
         ("YouTube · Pondering Islam", "Prophet Muhammad's First Revelation: Divine Turning Point in ..."),
         ("Quran.com", "Surah Info: Al-'Alaq - Quran.com"), ("YouTube · Islamic Lessons Made Easy", "Mab'ath: The Real Story of Prophet Muhammad's (S) First Revelation"),
         ("YouTube · Muslim Pro App", "When was the First Revelation of the Quran? | Muhammad: The Mercy for ..."),
         ("Lumen Learning", "The Quran | World Civilization - Lumen Learning"), ("IIUM", "SAHIH BUKHARI, BOOK 1: Revelation"),
         ("Britannica", "At what age did Muhammad receive his first revelation according to ..."), ("YouTube · Reviver of islam", "FULL STORY OF IQRA & THE CAVE OF HIRA - Mufti Menk")]
draft1 = {"q": "the first revelation", "entity": "the-first-revelation", "date": "2026-11-25", "surface": "Google AI Overview",
  "surface_basis": "operator's default (2026-10-01): 'it started in overview, as they all do now'; the 'AI Mode Conversation' header is the expanded Overview's residue (2026-10-18)",
  "auth": "signed out, incognito", "auth_basis": "operator's default (2026-10-14): 'theyre all signed out and incognito... i will say otherwise if otherwise'",
  "ev": "paste", "transcript": paste, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and sources as pasted",
  "transcript_complete": "complete as pasted: query line, body in four sections, two inline links named (Surah Info: Al-'Alaq; Sahih Bukhari, Book 1), three video cards in the body, card rail of ten, offer menu",
  "transcript_read": "READ IN FULL 2026-11-25", "cites": len(cards),
  "cite_list": [{"n": i + 1, "site": s, "title": t, "snip": None, "rel": "third_party", "url": None} for i, (s, t) in enumerate(cards)],
  "sf": "Google AI Overview, expanded; ten cards on the rail, three video cards in the body",
  "notes": {"seated_from": "paste-the-first-revelation.txt, the operator's message of 2026-11-25 16:11 EST",
            "seat": "Seated 2026-11-25 for the-first-revelation, at its own address; the same entity's composition at another's address is the Capture Registry's revelation-first-aio-20261125."}}
draft2 = {"q": "revelation first", "entity": "revelation-first", "date": "2026-11-25", "surface": "Google AI Overview",
  "surface_basis": "as recorded in the Capture Registry entry revelation-first-aio-20261125", "auth": "signed out, incognito",
  "auth_basis": "as recorded in the Capture Registry entry", "ev": "capture", "archive_present": False, "archive_basis": "declared: the thesis is not offered, named or linked (registry PER 1.00, target absent)",
  "capture_ref": {"slug": "revelation-first-aio-20261125", "obs_id": "OBS-55895a49377f"},
  "notes": {"why": "Erasure row (spec §1.3) for revelation-first: at the thesis's own string the Overview composed the First Revelation whole. The same composition is the-first-revelation's entity-constitutive composition at another's address."}}
for n, d in (("draft-the-first-revelation.json", draft1), ("draft-revelation-first-capture.json", draft2)):
    (INT / n).write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args = [sys.executable, str(ROOT / "scripts/non_intake.py"), str(INT / n)] + (["--seat"] if "--seat" in sys.argv else [])
    r = subprocess.run(args, capture_output=True, text=True, cwd=ROOT); print(n, r.returncode); print(r.stdout[-1500:], r.stderr[-1500:])
