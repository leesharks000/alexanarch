"""REPAIR 2026-11-07: the 14 June 2026 frame of sappho-rebekah-stanza restored to its record.

BELIEF AND EVIDENCE. The record sappho-rebekah-stanza (q "sappho rebekah cranes stanza", 2026-06-14) held as its frame a
byte-identical copy of johannes-sigil-grundrisse-3.png (sha1 8ca5f67e…), and its OCR transcript had been read from that
copy ("Q. johannes sigil grundrisse …"). Its annotation, written from the true screen, quotes "Rebekah Crane" and a 22:57
timestamp. An OCR search of every capture image held by the archive and its sites (679 unique files, 2026-11-07) found the
true frame filed as data/captures/heteronymic-provenance-theory/heteronymic-provenance-theory-2.png: the query "sappho
rebekah cranes stanza", 10:57 PM, AI Mode view, "Day and Night: Conversations with Sapphic Desire by author Rebekah Crane".
That frame's OCR had been appended to the 2026-06-14 observation of heteronyms-provenance-theory, whose own frame is -1.
The wrong copy originates on godkinggoogle (captures/sappho-rebekah-stanza.png), from which the archive mirrored it; the
origin is repaired in the same pass so a later mirror cannot restore it.

WHAT CHANGES. (1) The stanza frame's bytes become the true frame's. (2) The stanza transcript becomes the OCR of the true
frame, taken from the segment already in the registry (the earlier, fuller read) and checked against a fresh read; the
prior transcript is kept whole under notes.transcript_prior. (3) The provenance capture keeps every path and every word (the
registry's no-loss law): its 06-14 observation transcript gains a seam note marking the foreign segment, and the entry records
under collisions that frame -2 belongs to sappho-rebekah-stanza. Files held as deposit evidence (#1739 snapshot, deposit
manifests, AXN-034E's text, the v9.6 snapshot) are not touched. Ruling: Lee Sharks, 2026-11-07 11:05 EST: "we have
literally attempted to fix that divergence at the source about three times, so lets fix it well and truly please".
"""
import hashlib, json, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[3]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
TRUE = ROOT / "data/captures/heteronymic-provenance-theory/heteronymic-provenance-theory-2.png"
STZ = ROOT / "data/captures/sappho-rebekah-stanza/sappho-rebekah-stanza.png"
GKG = ROOT.parent / "fleet/godkinggoogle/captures/sappho-rebekah-stanza.png"
sha = lambda b: hashlib.sha1(b).hexdigest(); s256 = lambda s: hashlib.sha256(s.encode()).hexdigest()
ON = "2026-11-07"
assert sha(STZ.read_bytes()).startswith("8ca5f67e") and sha((ROOT/"data/captures/johannes-sigil-grundrisse/johannes-sigil-grundrisse-3.png").read_bytes()).startswith("8ca5f67e")
tb = TRUE.read_bytes()
reg = json.loads(REG.read_text(encoding="utf-8"))
E = {e["slug"]: e for e in reg["entries"]}
s = E["sappho-rebekah-stanza"]; h = E["heteronyms-provenance-theory-20260610"]
ho = [o for o in h["observations"] if o.get("slug") == "heteronymic-provenance-theory"][0]
SEAM = "AlMode_ All Images Videos Shopping Forums sappho rebekah cranes stanza 10:57 PM"
t = ho["transcript"]; j = t.index(SEAM)
own, foreign = t[:j].rstrip(), t[j:]
assert "Rebekah Crane" in foreign and "heteronym" in own.lower()
NOTE_S = (f"[Frame and transcript restored {ON}. The frame previously held here was a copy of johannes-sigil-grundrisse-3.png "
          f"and the transcript was its OCR (sha256 {s256(s['transcript'])[:16]}…). The true frame was found filed as "
          "heteronymic-provenance-theory-2.png; this transcript is that frame's OCR, as first read into the heteronyms-provenance-theory "
          "record, checked against a fresh read. OCR, chrome interleaved.]\n\n")
new_t = NOTE_S + foreign
for x in [s] + [o for o in s["observations"] if o.get("slug") == "sappho-rebekah-stanza"]:
    x.setdefault("notes", {}) if isinstance(x.get("notes"), dict) or x.get("notes") is None else None
    if x.get("notes") is None: x["notes"] = {}
    x["notes"]["transcript_prior"] = x.get("transcript") or ""
    x["notes"]["transcript_prior_why"] = "OCR of a copy of johannes-sigil-grundrisse-3.png, held here as this record's frame until " + ON
    x["transcript"] = new_t
    if "transcript_raw" in x: x["transcript_raw"] = foreign
    if "transcript_cleaned" in x: x["transcript_cleaned"] = foreign
    x["transcript_read"] = f"FRAME RESTORED AND OCR RE-READ {ON} (repair-20261107-stanza-frame)"
if s.get("notes") is None: s["notes"] = {}
s["notes"]["frame_repair"] = {"on": ON, "what": "frame and transcript restored from heteronymic-provenance-theory-2.png",
    "prior_frame_sha1": sha(STZ.read_bytes()), "true_frame_sha1": sha(tb), "ruled_by": "Lee Sharks, 2026-11-07 11:05 EST"}
NOTE_H = (f"\n\n[SEAM NOTE {ON}: from 'AlMode_ All Images Videos Shopping Forums sappho rebekah cranes stanza 10:57 PM' onward, this "
          "transcript is the OCR of heteronymic-provenance-theory-2.png, which is the 14 June capture of 'sappho rebekah cranes stanza' "
          "and is restored to that record. The text is kept here whole; it is not part of this observation.]")
ho["transcript"] = t + NOTE_H
h["collisions"] = (h.get("collisions") or []) + [{"on": ON, "img": "data/captures/heteronymic-provenance-theory/heteronymic-provenance-theory-2.png",
    "belongs_to": "sappho-rebekah-stanza", "note": "frame of another capture, filed here at intake; kept in place as evidence and cited by deposits; its OCR seam is marked in the 06-14 observation",
    "ruled_by": "Lee Sharks, 2026-11-07 11:05 EST"}]
STZ.write_bytes(tb)
if GKG.exists() and sha(GKG.read_bytes()).startswith("8ca5f67e"):
    GKG.write_bytes(tb); print("origin repaired:", GKG)
REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
print("stanza frame", sha(STZ.read_bytes()), "| stanza transcript", len(new_t), "| provenance obs", len(ho["transcript"]))
