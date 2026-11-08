import sys
p = sys.argv[1]; t = open(p, encoding="utf-8").read()
def rep(a, b):
    global t
    assert t.count(a) == 1, (t.count(a), a[:90]); t = t.replace(a, b)
rep("9.1 Your reports performed the first two kinds of check and stopped there. They compared figures with captions, and the form's count with the figures. They did not ask whether the evidence supports the argument, or whether an objection defeats it. You did not read the question the manuscript was sent to ask.",
    "9.1 State what the reports examined. They examined the January witness and its evidentiary standing, the absence of a query protocol, the separation of the author's roles, the opacity of the platform, the choice between an essay and an empirical study, the figures and their captions, two terms, the disclosure of language models, and the style. Each objection was answerable, and each is answered (Appendix A of #1749). They did not examine the philology: the Greek at the poem's edge, the translation history the argument stands on, the alignment of the output with its witnesses, the reading of κῆνος and τόλματον, or the question the manuscript was sent to ask. You raised methodological objections and left the reception study unread.")
rep("A count of figures decided whether the argument would be examined at all. The lower check governed, and the examination never came.",
    "The objections to method and presentation decided the manuscript's fate, and the philological examination it called for never came. The lower checks governed what the higher one was permitted to reach.")
rep("A misnumbered figure is what remains to assess when the substance is left unread.",
    "A protocol and a figure count are what remain to assess when the philology is left unread.")
open(p, "w", encoding="utf-8").write(t); print(len(t.split()))
