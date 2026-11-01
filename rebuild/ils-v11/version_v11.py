"""version_v11.py — Ils ne sont pas marxistes v1.1 from v1.0 (#1725), transformed in place on the operator's ruling of 2026-11-01
("lets go ahead w 1.1"): the post of #517 to r/LeftistsForAI, its removal under Rule 6 and the ban, which v1.0 did not carry, and the
Reddit account suspension that followed. Reads data/texts/AXN-0B50-text.md and the registry entry; writes
data/issue-bodies/ILS-NE-SONT-PAS-MARXISTES-v1.1-issue.md. Every change is an exact replacement that must match once."""
import json, pathlib, sys
R = pathlib.Path(__file__).resolve().parents[2]
txt = (R / "data/texts/AXN-0B50-text.md").read_text()
body = txt.split("\n---\n", 1)[1].lstrip("\n")
d = json.loads((R / "data/registry.json").read_text())["deposits"][1724]
assert d["deposit_number"] in (1725, "1725")
out = body
def rep(old, new, count=1):
    global out
    n = out.count(old)
    if n != count: sys.exit(f"expected {count} of: {old[:90]!r}, found {n}")
    out = out.replace(old, new)

rep("| r/LeftistsForAI, Feb 2026 | Left critique of AI mediation, cross-posted by Lee Sharks | Two works removed under the topicality rule; author's recorded exit (#517, AXN:0154, lines 24–30, 208) | Rule enforcement before reading |",
    "| r/LeftistsForAI, Feb 2026 | Left critique of AI mediation, cross-posted by Lee Sharks | Two works removed under the topicality rule; the analysis of that removal (#517), posted there, removed under Rule 6, \"Bad Faith\", and its author banned; author's recorded exit (#517, AXN:0154, lines 24–30, 208) | Rule enforcement before reading; the critic reclassified |")

rep("Three records concern the same subreddit across eight months. A first-hand deposit records a removal on or about 25 February 2026.",
    "Four records concern the same subreddit across eight months. A first-hand deposit records a removal on or about 25 February 2026. Its author's account, given in session at the time and restated on 1 November 2026, records what followed when the deposit was posted to the subreddit: a second removal and a ban.")

NEW = """

### The analysis posted, and the ban

The innocent reading first. A subreddit that has removed two posts can read a third post analysing that removal as a dispute brought into its space, and its rules provide for it: Rule 6, "Bad Faith", and Rule 8, "No factional flamewar", stand in the sidebar beside Rule 7. A moderator who removes the post and bans its author is ending a conflict, the ordinary work of keeping a forum quiet.

Lee Sharks posted #517 itself to r/LeftistsForAI, between its deposit on 26 February 2026 and the morning of 27 February. The moderators removed it under Rule 6, which the sidebar gives as a title with no text, and began messaging him privately; he declined the private channel. They banned him from the subreddit. His account at the time, given in session: "they removed the piece I posted about rule 7, citing rule 6 as the resson"; and "Posting that article there was the exact opposite of bad faith - it was good faith under extended duress when bad faith had already been demonstrated, as discussed in the piece". The ban is his first-hand account, stated again on 1 November 2026: "i posted that very article to leftistsforai and they immediately banned me". The subreddit's rules are quoted from the sidebar he pasted into the same session. He posted it expecting the ban: "i knew they would ban me for posting that. that is my function and always has been" (1 November 2026). Two or three days after the post he had stated the method: "We're not *posting* to platforms - we're probing their very boundaries, mapping them out. Don't mistake method for martyr complex. I am going to get banned one by one. And that is part of the process." (session of 1 March 2026). The post was a probe of whether the group could hold a critique of itself, its outcome was predicted, and the ban is the measurement.

The sequence is this report's case in one exchange. The first removal ruled on the works' topic. The second ruled on their author's intent, the "Bad Faith" title applied to an analysis that sets out its own boundaries: "I do not seek reinstatement. I do not appeal the moderators' decision." (AXN:0154, line 208); "I am not calling for harassment. Do not brigade the subreddit. Do not attack the moderators personally." (line 316). #517 had stated the mechanism in advance: "Identity does not evaluate the analysis. It evaluates the analyst." (line 186). The critique arrived in the space it concerned, addressed to the people it named, and its reply was exclusion with no reading. It is the move the opening sections trace from the Tenth Congress onward: the critic reclassified, and the procedure for answering suspended.

On or about 27 February Reddit suspended the account itself, by an automated email citing "technical irregularities" (#1172, AXN:04A5, line 93). Restored on 1 March, the account found the communities it had built banned; on 6 March, within hours of the formal demand's transmission, it was deleted (#26, AXN:016E, line 57). Lee Sharks considers it possible that a complaint arising from the subreddit played a part, and records that he has no evidentiary basis for it. The record holds the sequence: a critique posted, the critic banned from the group it addressed, the account suspended from the platform within a day. The mechanism joining the last two steps is closed to an outside reader, and this report's question applies to it: an exclusion that gives no reason leaves the excluded nothing to answer."""
anchor = "\n\n### The Overview at \"the failure of marxism as identity\" (17 October 2026)"
rep(anchor, NEW + anchor)

rep("Synthesis followed where the defeated critique kept three things: an organ in which it could keep being stated, a holder with standing independent of the executive, and a route by which the majority could later adopt it without calling that adoption surrender.",
    "Synthesis followed where the defeated critique kept three things: an organ in which it could keep being stated, a holder with standing independent of the executive, and a route by which the majority could later adopt it without calling that adoption surrender. The report's own first case met the variable directly: the analysis of the February removal, posted to the subreddit it concerned, was removed as bad faith and its author banned, and the critique kept its organ only because the archive held it.")

F = lambda k, v: f"### {k}\n\n{v}\n\n"
desc = d["description"] + " Version 1.1 (2026-11-01) adds what version 1.0 did not carry: the analysis of the removal, posted to r/LeftistsForAI, was removed under the subreddit's 'Bad Faith' rule and its author banned, and Reddit suspended the account within a day; the sequence is recorded from the author's account at the time and its restatement, with the account suspension from the archive's own record."
sub = d["substrate"] + " Version 1.1 transformed in place on 2026-11-01 by Claude (Anthropic) in session, at the operator's word, from his first-hand account in the sessions of 26–27 February, 1 March and 1 November 2026, every archive quotation checked at its seated line."
rel = (d.get("related_identifiers_raw") or "").strip()
rel = "#1725 (version 1.0, superseded by this version); #26 (The Archival Reclamation Protocol); #1172 (the same, restated)" + ("; " + rel if rel else "")
kw = d["keywords"] if isinstance(d["keywords"], list) else json.loads(d["keywords"])
kw = kw + ["Rule 6", "bad faith", "subreddit ban", "Reddit account suspension"]
ib = (F("Protocol Version", "alexanarch-deposit-protocol/v1") + F("Title", d["title"]) + F("Creator", "Sharks, Lee") + F("ORCID", "0009-0000-1599-0703")
      + F("Date", "2026-11-01") + F("Description", desc) + F("Content Type", d["content_type"]) + F("License", "CC-BY-4.0")
      + F("Substrate Disclosure", sub) + F("Keywords", ", ".join(kw)) + F("Related Identifiers", rel) + F("Version", "v1.1")
      + F("Methodology", d["methodology"] + " Version 1.1: the post, the Rule 6 removal and the ban from the author's account in session (26–27 February 2026) and its restatement (1 November 2026); the post as probe from his statements of 1 March and 1 November 2026; the subreddit's rules from the sidebar he pasted that day; the account suspension and deletion from #1172 (line 93) and #26 (line 57).")
      + F("Falsification Conditions", d["falsification_conditions"]) + F("Supersedes", "1725") + "### Body\n\n" + out.rstrip("\n") + "\n\n"
      + "### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n")
(R / "data/issue-bodies/ILS-NE-SONT-PAS-MARXISTES-v1.1-issue.md").write_text(ib)
print("written", len(ib))
