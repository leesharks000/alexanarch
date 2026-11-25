"""Later observation of through-anothers-mouth-dialogue-heteronyms-aio-20261125: the same string, Google AI Overview, 18:20 EST, four screengrabs."""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
S = "through-anothers-mouth-dialogue-heteronyms-aio-20261125"
imgs = [f"data/captures/{S}/screengrab-20261125-{t}.png" for t in ("182003", "182012", "182017", "182026")]
d = {"q": "Through Another's Mouth: A Dialogue between Heteronyms", "date": "2026-11-25", "surface": "Google AI Overview",
 "auth": "signed out, incognito", "ev": "ocr", "s": "Literature",
 "originator": {"name": "Sigil, Johannes", "relation": "archive", "entity_type": "work", "spxi_treatment": "full", "basis": "Through Another's Mouth, #1807 (Johannes Sigil; heteronym of Lee Sharks). Recorded 2026-11-25."},
 "transcript": (H / "transcript.txt").read_text(encoding="utf-8"), "imgs": imgs, "cites": 3, "per_v": {"author": True, "inst": True, "id": True, "src": True},
 "d": ("THROUGH ANOTHER'S MOUTH, UNQUOTED, ON GOOGLE AI OVERVIEW, 2026-11-25 18:20 EST, FOUR SCREENGRABS (the results page and the Overview expanded): "
       "the composition of 15:30 the same day returned word for word — Sigil as author of a Dodecad heteronym's dialogue, #1806 as companion, Wells, Cranes, "
       "Glas, 'by nature or by chance', Lee Sharks entering 'strictly in his own verbatim words', Tyrannion, 'beast, god, or by chance', EA-HET-DODECAD-01; "
       "the same chips (PhilPapers +1, PhilPapers +2) and the PhilPapers card for Sappho as Initiatory Figure; below it, Medium's own result, 23 hours old. "
       "A stable composition at the address within the day.")}
(H / "draft.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"); print("wrote")
