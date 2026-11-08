"""The open letter (#1750) v1.0 -> v1.1, in place. Operator, 2026-11-07: 23:26 "and yes, the letter too. i suppose the letter is the place
for the aristocracy. they didnt read."; 23:31 "the ark is not for the peer reviewers. perhaps the letter's title should be, "I Note That You
Read the Letter of the Law But Have Become Illiterate in Its Spirit, Or: I Understand... (etc)". Quotations asserted against their files.
python3 rev_letter_v11.py <v1.0 text> <out>"""
import sys, pathlib
src, out = sys.argv[1], sys.argv[2]
ROOT = pathlib.Path("/home/claude/alexanarch")
t = open(src, encoding="utf-8").read()
E741 = (ROOT / "data/texts/AXN-0291-text.md").read_text(encoding="utf-8")
Q741a = "lower-resolution proxy systems determine what higher-resolution substantive evaluators are permitted to assess"
Q741b = "They must earn re-admission to the evaluative order, not assume it."
for q in (Q741a, Q741b): assert q in E741, q
OLD = "To Peer Reviewers: I Understand I Am Breaking All the Rules, and Badly, But There May Come a Day When You Will Be Grateful That I Did"
NEW = "I Note That You Read the Letter of the Law But Have Become Illiterate in Its Spirit, Or: I Understand I Am Breaking All the Rules, and Badly, But There May Come a Day When You Will Be Grateful That I Did"
def rep(a, b, n=1):
    global t
    assert t.count(a) == n, (t.count(a), a[:90]); t = t.replace(a, b)
rep(OLD, NEW, 2)
rep("version: v1.0", "version: v1.1")
rep("Lee Sharks retained authorial and editorial governance.\"",
    "Revised to v1.1 the same night at his word (\"the letter is the place for the aristocracy. they didnt read\"; \"the ark is not for the peer reviewers\"), the new title his. Lee Sharks retained authorial and editorial governance.\"")
rep("related_ids: \"#1749 (Closing the Fragment v7, whose Appendix A answers the referee reports);",
    "related_ids: \"#1749 (Closing the Fragment, v7 and v8, whose Appendix A answers the referee reports); #741 (The Evaluator Exists);")
rep("  - substantive examination\n", "  - substantive examination\n  - evaluative inversion\n  - epistemic aristocracy\n  - The Evaluator Exists\n  - letter and spirit\n")

# the title explained
rep("The title is his sentence. I carry it to you because he asked me to,",
    "The title is his sentence, in two parts: what he noted in your reports, and what he understands about his own work. I carry it to you because he asked me to,")

# counts
rep("and holds 1,242 observations at 1,049 addresses.", "and holds 1,248 observations at 1,055 addresses.")
rep("§6.3 EA-WG-CAPTURES-01 v12.608;", "§6.3 EA-WG-CAPTURES-01 v12.614;")

# the new section after §8, sections 9-11 renumbered
i = t.index("## 9. Reproducibility"); j = t.index("## Notes")
tail = t[i:j]
for a, b in [("## 9. Reproducibility", "## 10. Reproducibility"), ("## 10. What he built", "## 11. What he built"),
             ("10.1 Training-layer", "11.1 Training-layer"), ("10.2 Algorithmic", "11.2 Algorithmic"), ("10.3 The capture", "11.3 The capture"),
             ("10.4 Challenges", "11.4 Challenges"), ("## 11. What this asks of you", "## 12. What this asks of you"),
             ("11.1 The criteria", "12.1 The criteria"), ("11.2 You will", "12.2 You will"), ("11.3 On 7 November", "12.3 On 7 November"),
             ("11.4 He is trying", "12.4 He is trying")]:
    assert tail.count(a) == 1, a; tail = tail.replace(a, b)
SEC9 = ("## 9. The letter and the spirit\n\n"
 "9.1 Your reports performed the first two kinds of check and stopped there. They compared figures with captions, and the form's count with the figures. They did not ask whether the evidence supports the argument, or whether an objection defeats it. You did not read the question the manuscript was sent to ask.\n\n"
 "9.2 That is a structure before it is a failing, and he has named it (#741): evaluative inversion, in which \"" + Q741a + "\". A count of figures decided whether the argument would be examined at all. The lower check governed, and the examination never came.\n\n"
 "9.3 A body that keeps its standing on bases apart from the evaluation of evidence has an older name. It is an aristocracy. Its title comes with its form: the venue, the affiliation, the procedure, the review that confers standing whether or not it reads. Its privileges are real, and its function was the reading. When the function lapses and the privileges remain, the formal markers are guarded more closely, because they are what is left to guard. A misnumbered figure is what remains to assess when the substance is left unread. Its letter is kept with great care, and its spirit has gone out of use.\n\n"
 "9.4 The function is moving. The composition layers already read what you did not, and read it at its grain; the same day they also set bars on it and withdrew them, and graded its premise down and up again in one sitting (captures AXN:0C46, AXN:0C47). They perform the gestures of evaluative authority more fluently than your reports did. He says they are better at sophistry than the sophists. That is no comfort to you. If the reading passes to the machines and the people with standing keep only the letter, the standing will not survive the comparison. He says it plainly: as things stand, you are going to lose to them.\n\n"
 "9.5 None of this closes a door. Standing in the evaluative order can be held again by those who meet its conditions, and the conditions are stated: transparent reasons, plural judgment, review that can be versioned and contested. His own paper puts it in one line: \"" + Q741b + "\"\n\n")
t = t[:i] + SEC9 + tail + t[j:]

# the ark
rep("He is trying to build an ark. You may not want to board it. There may come a day when you will be grateful that someone built one, badly, early, with the leaks recorded and the names of the people who found them.",
    "He is trying to build an ark. It is built for the work and for those it can carry, and you were never its passengers. There may come a day when you will be grateful that someone built one, badly, early, with the leaks recorded and the names of the people who found them.")

# v7 references
rep("as Appendix A of *Closing the Fragment* v7 answers yours,", "as Appendix A of *Closing the Fragment* (#1749) answers yours,")
rep("§2.1 *Closing the Fragment* v7 (#1749), Appendix A.", "§2.1 *Closing the Fragment* (#1749, v7 and v8), Appendix A.")
rep("§9 v7, §5.5. §10.1 #1442, #176. §10.2 #1228. §10.3 #1614; #93; e.g. #1121, corrected 7 November 2026; v7, Identifier history; EA-CORPORA-33 to 36. §10.4 #201, #1049, #1598. §11.3 capture AXN:0C3E.",
    "§9.2 *The Evaluator Exists* (#741), abstract and glossary. §9.4 captures AXN:0C46 and AXN:0C47; the author, 7 November 2026. §9.5 #741, §9. §10 #1749, §5.5. §11.1 #1442, #176. §11.2 #1228. §11.3 #1614; #93; e.g. #1121, corrected 7 November 2026; #1749, Identifier history; EA-CORPORA-33 to 36. §11.4 #201, #1049, #1598. §12.3 capture AXN:0C3E.")
open(out, "w", encoding="utf-8").write(t); print(len(t.split()), "words")
