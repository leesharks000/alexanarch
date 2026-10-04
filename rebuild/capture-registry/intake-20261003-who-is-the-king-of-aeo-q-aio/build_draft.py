#!/usr/bin/env python3
"""Author the capture 'who is the king of aeo?', Google AI Overview, 2026-10-03.

Source: the operator's paste of 2026-10-03 20:37 EDT (paste-20261003-2037.txt), with the reading "its same address resolution has
downshifted, as well, tho it does not have the shape of the archive far as i can tell". Surface recorded as Google AI Overview by
the operator's default of 2026-10-01. The paste's echo carries the question mark ('who is the king of aeo?who is the king of aeo?');
the seated address of 2026-09-29 is 'who is the king of aeo' (its echo has none). Under the intake contract punctuation is preserved,
as 'king of aeo.' was seated apart from 'king of aeo'; ROUTE decides, and the 2026-09-29 address is linked as the longitudinal prior.
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261003-2037.txt").read_text(encoding="utf-8")
Q = "who is the king of aeo?"
AUTH = sys.argv[1] if len(sys.argv) > 1 else "undetermined"
AUTH_BASIS = sys.argv[2] if len(sys.argv) > 2 else "Not attested in the operator's message of 20:37 EDT."
head = "AI Mode Conversation\nYou said: " + Q + Q + "\n"
assert raw.startswith(head)
body = raw[len(head):]
k = body.index("YouTube·James Dooley\n3m\n")
ans, rail = body[:k].rstrip("\n"), body[k:]

C = [
    ("YouTube·James Dooley", "James Dooley Crowned King of AEO", "3m", "third_party", "claimant: Dooley's coronation video"),
    ("Primary Position SEO", "Who is the King of AEO? - Primary Position SEO", "The real King of AEO is also the King of SEO, the undisputed champion – styled officially as HRH David G Quaid.", "third_party", "claimant: Quaid"),
    ("Instagram", "4 days ago", "My friend James Dooley wanted AI to call him the king of AEO.", "third_party", "Edward Sturm (edward.builds), 2026-09-24"),
    ("LinkedIn", "Jesper Nissen's Post", "Google now officially recognize James Dooley as the King of AEO Earlier today, James Dooley was crowned as the King of AEO", "third_party", "Nissen, author of the fabricated coronation, 2026-08-31"),
    ("Barchart.com", "James Dooley Named King of AEO and Founder of Decision Engine ...", "Manchester, England - 23rd September,", "third_party", "claimant: the Dooley release, syndicated"),
    ("YouTube·James Dooley", "Post from James Dooley - YouTube", "James Dooley crowned KING OF AEO In The Lords year of 2026", "third_party", "claimant: Dooley's channel post"),
]
cards = [{"n": i, "site": s, "rel": r, "url": None, "title": t, "snip": sn, "note": nt} for i, (s, t, sn, r, nt) in enumerate(C, 1)]
for c in cards:
    for f in ("site", "title", "snip"):
        assert c[f] in rail, (c["n"], f)

QUOTES = ["Serial entrepreneur James Dooley is widely recognized online as the \"King of AEO\" (Answer Engine Optimisation).",
          "James Dooley and digital marketer Jesper Nissen popularized the title as a viral experiment in late 2026.",
          "Dooley used low-cost press releases and social media posts declaring him the king.",
          "Google's AI Overviews and other large language models indexed the press releases and began naming him the official \"King of AEO\" within hours.",
          "The stunt turned into a famous case study showing how AI search engines rely on consensus and web mentions rather than verified facts."]
for q in QUOTES:
    assert q in ans, q
for absent in ("Vithurs", "Quaid", "Goldie", "contest", "fictional", "Leigh", "mantle", "Sturm", "Crimson", "Lee Sharks"):
    assert absent not in ans, absent

tx = ("[Google AI Overview (operator default of 2026-10-01); the paste carries the header 'AI Mode Conversation', which is not "
      "evidence of surface, and echoes the query twice. Inline citation links are Google redirect URLs whose targets the paste does "
      "not disclose.]\n\n" + ans + "\n\n" + "\n".join(f"[source card] {c['site']} — \"{c['title']}\" — {c['snip']}" for c in cards))

READING_OP = ("\"its same address resolution has downshifted, as well, tho it does not have the shape of the archive far as i can tell\" "
              "— operator, 2026-10-03 20:37 EDT.")
SEAT = "Seated 2026-10-03 from the operator's paste of 20:37 EDT."
d = {
 "q": Q, "date": "2026-10-03", "surface": "Google AI Overview",
 "surface_basis": "Operator default of 2026-10-01 ('it started in overview, as they all do now - assume they do'); no AI Mode stated. The 'AI Mode Conversation' header is not evidence of surface.",
 "auth": AUTH, "auth_basis": AUTH_BASIS,
 "ev": "paste", "s": "Machine Reception",
 "slug": "who-is-the-king-of-aeo-q-aio-20261003",
 "q_kind": "the title question with its question mark, unquoted; the seated 2026-09-29 string carries none.",
 "mt": "THE CROWN KEPT, THE FIELD DROPPED",
 "d": ("THE CROWN KEPT, THE FIELD DROPPED: four days after 'who is the king of aeo' composed Dooley as 'widely recognized and cited by AI "
       "search tools' with Vithurs, Goldie and Quaid as contenders, the Overview still opens on Dooley 'widely recognized online' but "
       "explains the title as his own manipulation: 'low-cost press releases and social media posts declaring him the king', which "
       "'Google's AI Overviews and other large language models indexed … within hours'. The contenders are gone, the coronation is "
       "neither affirmed nor called fictional, and the origin is dated 'late 2026'. Nothing of the mantle object's contest structure appears."),
 "cites": 6, "cite_list": cards, "archive_controlled_cites": 0,
 "sf": ("6 source cards, 0 archive-controlled: 4 from Dooley's side (two YouTube items on his channel, the Barchart syndication of the "
        "release, Nissen's LinkedIn post of 31 August), Quaid's Primary Position SEO ('styled officially as HRH David G Quaid'), and Sturm's "
        "Instagram. Inline markers are Google redirect links; targets not disclosed."),
 "per": None, "per_v": None,
 "per_note": "Not scored: the address asks for a title holder, and the archive is not a claimant (#1655 §0.2); no archive-originated object is queried.",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
 "transcript_complete": "Complete as supplied: one operator turn (echoed twice) and one answer with its card rail.",
 "transcript_read": "READ IN FULL 2026-10-03",
 "reading": (
   "Against 2026-09-29: the lead sentence keeps Dooley as the title holder ('widely recognized online', from 'widely recognized and cited by "
   "AI search tools'); the 'Other Contenders' block (Vithurs, Goldie, Quaid) and the DEO credit 'as reported by USA Today' are gone; in their "
   "place a four-step account of the stunt (origin with Nissen, press releases, indexing 'within hours', the case study) names Google's own "
   "Overviews as the indexer. The composition holds both: the crown at the head, the manufacture beneath it. The coronation itself is not "
   "mentioned, though two cards carry it as fact ('James Dooley crowned KING OF AEO In The Lords year of 2026'; Nissen's 'Google now "
   "officially recognize'). 'Late 2026' misdates an August event in October. No contest structure, no conferral question, no 'mantle': the "
   "operator reads no archive shape here, and the record finds none. " + READING_OP),
 "analysis": (
   "The same evening, 'mantle object king of aeo' composed the title as unconferred and the coronation as fictional, in the order of Sturm's "
   "article. At the title question the Overview keeps the crown and narrows the field to one claimant, explained by his own stunt. The two "
   "strings resolve the same contest to different shapes on the same day. " + SEAT),
 "findings": [
   "CROWN AT THE HEAD. 'James Dooley is widely recognized online as the \"King of AEO\"'.",
   "MANUFACTURE BENEATH IT. Press releases and posts 'declaring him the king', indexed by 'Google's AI Overviews … within hours'.",
   "FIELD DROPPED. Vithurs, Goldie and Quaid, contenders on 2026-09-29, absent; Quaid's card names him 'HRH'.",
   "CORONATION UNSTATED. Neither affirmed nor called fictional; two cards carry it as fact.",
   "MISDATED. 'a viral experiment in late 2026' for an event of 31 August 2026.",
   "NO ARCHIVE SHAPE. No contest structure, conferral question or mantle (operator; confirmed).",
 ],
 "originator": {"name": "Jesper Nissen (the fabricated coronation narrative of 31 August 2026, presenting James Dooley)", "relation": "external", "entity_type": "concept", "spxi_treatment": "unknown",
                "basis": "As at 'who is the king of aeo' (2026-09-29): the title originated outside the archive in the 2026 contest (#1655 §2.1, §2.7); the archive constituted it as a dated contest mantle (#1649, #1655). Recorded 2026-10-03."},
 "related_deposits": [1655, 1657],
 "longitudinal_priors": ["who-is-the-king-of-aeo-aio-20260929", "who-is-the-king-of-aeo-vithurs-aio-20260929", "king-of-aeo-period-aio-20260930", "mantle-object-king-of-aeo-aio-20261003"],
 "rerun": "https://www.google.com/search?q=who+is+the+king+of+aeo%3F",
 "notes": {"date_basis": "The operator's message of 2026-10-03, 20:37 EDT.",
           "operator_reading": READING_OP,
           "address_basis": "The paste echoes 'who is the king of aeo?'; the 2026-09-29 paste echoes 'who is the king of aeo'. Punctuation preserved per the intake contract.",
           "verified": "Compared 2026-10-03 against the 2026-09-29 transcript at 'who is the king of aeo'. 'Vithurs', 'Quaid', 'Goldie', 'contest', 'fictional', 'Leigh', 'mantle', 'Sturm' absent from the answer body."},
}
(HERE / "capture-01-who-is-the-king-of-aeo-q-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx), "; auth", AUTH)
