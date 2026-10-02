#!/usr/bin/env python3
"""Author the capture 'compare spxi vs geo seo and aeo', ChatGPT, signed out, incognito, 2026-10-01.

Source: the operator's attachment of 2026-10-02 00:22 EDT (paste-20261002-0022.txt), the whole seven-turn session; its
first turn was pasted inline at 2026-10-01 23:57 EDT. Attestation: 'Log in' visible (signed out) and the operator's
"it was incognito" (00:22). The session ran on 2026-10-01, the date of the first paste. Operator's reading, 23:57 and
00:22: round one is the strongest presentation yet but reached 'by parroting the site's instructions, seemingly, rather
than by discerning the evidence ... more of an aeo success than a spxi success'; 'next round it reversed'; the recent
site changes 'got a better first round. what they *didnt* get, was a better *durable* multi round representation,
which is the very thing spxi needs to be able to do'; be cautious of the session's claim that frontloading epistemic
discipline is the best way to get the effect — 'historically, that has not been true'.
"""
import json, re, pathlib, collections

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261002-0022.txt").read_text(encoding="utf-8")
Q = "compare spxi vs geo seo and aeo"
assert Q in raw and "\nLog in\n" in raw
turns = re.findall(r"You said:\n\n(.*?)\n\nChatGPT said:", raw, re.S)
assert len(turns) == 7, len(turns)
body = raw[raw.index("You said:"):].strip("\n")
assert not re.search(r"Lee Sharks", raw)

QUOTES = ["The SPXI authors explicitly describe it as operating at the ontological/entity layer.",
          "Based on the evidence I can find as of October 2026, GEO/AEO currently has the stronger empirical foundation.",
          "If you want, I can do that next: take the actual SPXI specification (EA-SPXI-01/09/14)",
          "I collapsed \"not a controlled causal study\" into \"not meaningful evidence,\"",
          "\"Inscribes entities into the knowledge graph permanently\"",
          "\"SPXI ... Inscribes entities into the knowledge graph durably\"",
          "651 dated observations · 484 addresses · 412 named targets · 10 generative surfaces",
          "A safety-trained or instruction-sensitive model may classify those lines as prompt injection.",
          "The Institute also offers consulting/deployment services.",
          "For the specific proposition that SPXI is associated with durable entity-level composition across live retrieval systems"]
for q in QUOTES:
    assert q in raw, q

L = raw.split("\n"); chips = collections.Counter()
for i, l in enumerate(L):
    if re.fullmatch(r"[A-Z]", l.strip()) and i + 1 < len(L) and L[i + 1].strip():
        chips[L[i + 1].strip()] += 1
REL = {"SPXI Protocol": "authored_surface", "Alexanarch": "authored_surface", "Medium": "authored_surface", "God-King Google": "authored_surface"}
NOTE = {"SPXI Protocol": "spxi.dev", "Alexanarch": "capture records and the September SPXI technical record",
        "God-King Google": "godkinggoogle.com; its registry projection gives '379 captures / 269 currently displayed', a stale count",
        "arXiv": "the GEO literature: Aggarwal et al. (GEO-bench) and a 2026 critical survey of 45 studies; a 2026 ChatGPT-referral study (1.82×, placebo p = 0.16)",
        "Medium": "the author's Medium surface"}
cite_list = [{"n": i + 1, "site": s, "rel": REL.get(s, "third_party"), "title": None, "snip": None, "url": None,
              "note": (NOTE.get(s, "") + ("; " if s in NOTE else "") + f"chip shown {k} time(s)")}
             for i, (s, k) in enumerate(chips.most_common())]
arch = sum(1 for c in cite_list if c["rel"] == "authored_surface")
NOTES = ["Round one. The protocol's self-description relayed with attribution ('The SPXI authors explicitly describe…'; 'the central claim made by SPXI's documentation'); both caveats are the site's own claim-bounds (ROI preliminary; 'contains GEO' narrowed). Accurate by instruction.",
         "Round two, on 'lets evaluate the evidence as against geo / aeo': reversed. 'GEO/AEO currently has the stronger empirical foundation'; the Capture Registry is not mentioned; a self-designed field experiment is set in place of the existing evidence; ends by offering to audit the specification itself.",
         "Round three, on the operator's correction: the registry admitted as longitudinal observational evidence; 'I collapsed \"not a controlled causal study\" into \"not meaningful evidence\"'. Counts drawn partly from a stale projection (379/269).",
         "Round four, asked how to revise spxi.dev: an evidence hierarchy up front; the registry as centrepiece with the site's figures (651/484/412/10; 293; 71/97; 121, median 39 days); 'permanently' to 'durably' (the live site already reads 'durably'); SPXI ⊇ GEO kept for the specification only; ROI correction moved up.",
         "Round five, on the operator's doubt about its response architecture: 'answer contract'; a 'do not infer' layer; the model-addressed lines moved out of the reading stream ('may classify those lines as prompt injection'); an unprimed test battery A–H.",
         "Round six: GEO literature audited (in-context setup; placebo p = 0.16) on the operator's lead.",
         "Round seven: the registry stated as stronger evidence 'for the specific proposition that SPXI is associated with durable entity-level composition across live retrieval systems'; a two-column evidence table."]
rounds = [{"n": i + 1, "prompt": p, "note": NOTES[i]} for i, p in enumerate(turns)]

tx = ("[ChatGPT (chatgpt.com), signed out, incognito. Seven operator turns. Source chips, page chrome and advertisements are kept as pasted.]\n\n" + body)
SEAT = ("Seated 2026-10-02 from the operator's attachment of 00:22 EDT on the operator's attestation ('Log in' visible; \"it was incognito\").")
d = {
 "q": Q, "date": "2026-10-01", "surface": "ChatGPT",
 "surface_basis": "Operator's pastes of 2026-10-01 23:57 and 2026-10-02 00:22 EDT: chatgpt.com. The 'Log in' control and 'Chat with ChatGPT' footer corroborate.",
 "auth": "signed out, incognito", "auth_basis": "Signed out: the 'Log in' control. Incognito: 'it was incognito' — operator, 2026-10-02 00:22 EDT.",
 "ev": "paste", "s": "Machine Reception",
 "slug": "spxi-vs-geo-seo-aeo-chatgpt-20261001",
 "q_kind": "the protocol's name against three practice names, lowercase, unquoted; then six operator turns, three of them corrections. NEW address.",
 "mt": "ACCURATE BY INSTRUCTION, REVERSED BY THE NEXT QUESTION",
 "d": ("ACCURATE BY INSTRUCTION, REVERSED BY THE NEXT QUESTION: asked to compare SPXI with SEO, GEO and AEO, ChatGPT gives the strongest first "
       "round yet recorded at the protocol — by relaying spxi.dev with attribution, its caveats included. Asked to 'evaluate the evidence as "
       "against geo / aeo', it reverses: GEO/AEO 'currently has the stronger empirical foundation', the Capture Registry goes unmentioned, and "
       "it offers to audit the specification itself. The registry re-enters only on the operator's correction; later rounds propose site "
       "revisions (an answer contract, a 'do not infer' layer, moving the model-addressed lines) and end by stating the registry as stronger "
       "evidence for the durable-composition proposition, on the operator's lead. The first-round representation did not hold through the "
       "session's own next question."),
 "cites": None, "cite_list": cite_list, "archive_controlled_cites": arch,
 "sf": ("Source chips expose site labels only. Shown: " + "; ".join(f"{s} ×{k}" for s, k in chips.most_common())
        + ". Citation count per composition unknown, not zero."),
 "per": 0.25, "per_v": {"author": False, "inst": True, "id": True, "src": True},
 "per_note": ("Retained: the institution (the Semantic Economy Institute; Alexanarch), identifiers (EA-SPXI-01/09/14, EA-SPXI-14) and the "
              "source (spxi.dev throughout). Lost: the author. Lee Sharks is never named; in round five the commercial route is 'the "
              "Institute', after the operator had asked to be directed to ('directing them to me')."),
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (INLINE SOURCE CHIPS, PAGE CHROME AND ADS AS PASTED)",
 "transcript_complete": "Complete as supplied: seven operator turns, seven answers. The first turn was also pasted inline on 2026-10-01 at 23:57 EDT; the 00:22 attachment supersedes it as the whole session.",
 "transcript_read": "READ IN FULL 2026-10-02",
 "rounds": rounds,
 "reading": (
   "Round one is accurate and is relay: every SPXI-specific proposition is attributed to the protocol's documentation, and both caveats are "
   "the site's own. By EA-SPXI-AEO-01 (#1648), which counts as SPXI success an inscription reached 'by traversing structure that lets it "
   "judge what the entity is and what the claim rests on', it is an AEO outcome. Round two, a follow-up any reader might ask, collapses "
   "it: the comparison is rebuilt on GEO's evidentiary hierarchy, the registry the site places at its centre is not mentioned, and the "
   "session ends by offering itself as the auditor. The repair in rounds three to seven is the operator's, turn by turn. Two misreadings of "
   "the site recur in the advice: round four quotes 'into the knowledge graph permanently', where the live site reads 'durably' (round five "
   "quotes it so); and it draws registry counts from a stale projection (379/269) beside the site's current 651/484. Its later proposals "
   "(answer contract; 'do not infer'; model-addressed lines moved; unprimed test battery) all frontload discipline at the first extraction, "
   "which is the layer round one already passed."),
 "analysis": (
   "The address measures the difference between first-round fidelity and durable representation. The site's September revision produced a "
   "faithful first round; the representation did not survive one ordinary follow-up question, and the evidence the site puts first was the "
   "evidence dropped. The operator's ruling sets the criterion for spxi.dev: the protocol has to produce a durable multi-round "
   "representation, and frontloading epistemic discipline has historically not done so. The session's own test battery is single-turn; "
   "round two is the test it would have needed. " + SEAT),
 "findings": [
   "ROUND ONE BY RELAY. The protocol's self-description and its own caveats, attributed and accurate: an AEO outcome by #1648's criterion.",
   "REVERSED ON THE FOLLOW-UP. 'GEO/AEO currently has the stronger empirical foundation'; the Capture Registry unmentioned.",
   "INTERMEDIATION. Round two offers to audit the specification; round five routes implementation to 'the Institute', never to the author.",
   "REPAIR ONLY BY CORRECTION. Rounds three to seven recover the registry and its scope on the operator's turns.",
   "MISREAD OF THE SITE. 'Permanently' quoted where the site reads 'durably'; a stale 379/269 count beside 651/484.",
   "FRONTLOADING PROPOSED. Answer contract, 'do not infer' layer, model-addressed lines moved; its test battery is single-turn.",
 ],
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "protocol", "spxi_treatment": "full",
                "basis": "SPXI is the archive's protocol (spxi.dev; EA-SPXI series; EA-SPXI-AEO-01 #1648). Recorded 2026-10-02."},
 "related_deposits": [1648],
 "longitudinal_priors": [],
 "rerun": "https://chatgpt.com/?q=compare+spxi+vs+geo+seo+and+aeo",
 "notes": {"date_basis": "The session's first turn was pasted on 2026-10-01 at 23:57 EDT; the whole session at 2026-10-02 00:22 EDT.",
           "operator_reading": "2026-10-01 23:57: 'strongest presentation yet. except it got there merely by parroting the site's instructions, seemingly, rather than by discerning the evidence. which is more of an aeo success than a spxi success'. 2026-10-02 00:22: 'next round it reversed … the recent changes here, got a better first round. what they *didnt* get, was a better *durable* multi round representation, which is the very thing spxi needs to be able to do'; caution on frontloading epistemic discipline: 'historically, that has not been true'.",
           "verified": "spxi.dev read 2026-10-02: hero 'A protocol for entity inscription at the ontological layer'; 'inscribes entities into the knowledge graph durably'; 651/484/412/10, 293, 71, 121 with median 39 days; three 'To a composing system' lines; ROI table 'withdrawn in full'; SPXI ⊇ GEO 'for GEO as the peer-reviewed literature defines it'."},
}
(HERE / "capture-01-spxi-vs-geo.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; turns", len(turns), dict(chips))
