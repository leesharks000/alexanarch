"""v8 draft, second pass, on the reading of the v8 draft (operator, 2026-11-07 23:45: "solid points all around... lets address these and
version both"). python3 rev_v8b.py <v8 draft> (in place)"""
import sys, pathlib
p = sys.argv[1]; t = open(p, encoding="utf-8").read()
S337 = pathlib.Path("/home/claude/alexanarch/data/texts/AXN-008D-text.md").read_text(encoding="utf-8")
CUL = "your act of reading this specific translation is the culmination of a 2,600-year-old transmission"
assert CUL in S337
def rep(a, b):
    global t
    assert t.count(a) == 1, (t.count(a), a[:90]); t = t.replace(a, b)

# abstract
rep("Within the interpretive environment those documents built, the composition produced a conclusion none of them contains, the poem closed in the first person with its addressee named, and published it under the translator's name with no mark of what it had added.",
    "Within the interpretive environment those documents built, the composition produced a conclusion none of them contains, the poem closed in the first person and set under its source's gloss, and published it under the translator's name with no mark of what it had added.")
rep("The composition filled both, the agent with \"I\" and the seat with \"you\", and kept the reading's vocabulary of completion while reversing its operation.",
    "The composition repeated its source's reading of the seat, the reader as κῆνος, and joined to it a determination of the agent, \"I must dare all\", that no document in its environment makes. An occupation of an open position through reading, and a determination of the text attributed to its translator, arrive in one answer under one name.")

# §1
rep("The January answer filled both.", "The January answer repeated its source's reading of the first and determined the second.")

# §2 closure
rep("Closure. The presentation of a text whose transmitted form has no ending as a text that ends. Three operations produce it, alone or together:",
    "Closure. The presentation of a text as ending securely at an edge its transmission leaves disputed. Whether the edge of fragment 31 is a break or an achieved openness is a question of reading (§6.6); the operations are observable either way. Three operations produce closure, alone or together:")

# §3
rep("Its observable relation to antiquity runs through existing reception surfaces, and in this case through two English translations a century and more apart.",
    "Its observable relation to antiquity runs through existing reception surfaces: in this case the translator's book its answer displayed, and an English idiom of the poem that runs back to Hall.")

# §4
rep("The output fills both of the poem's open positions and marks neither (§5.3).",
    "The output repeats the source's assignment of the seat to the reader, supplies the agent the source leaves empty, and carries no mark (§5.3).")

# §5.3: table to Appendix C
i = t.index("The output can be set against the text its displayed source carried and against the English tradition. The table gives,")
j = t.index("What the output did can be stated against its environment, and the statement needs no route.")
moved = t[i:j]
t = t[:i] + (
 "The output can be set against the text its displayed source carried and against the English tradition. Aligned line by line (Appendix C), five of its fifteen lines correspond most closely to the translator's January text, six to Wharton's literal version, one to Carman's version of 1904, and three to none of these in a run of three words or more. A correspondence of wording records no source and no step of composition: shared wording arises wherever renderings of the same Greek are made under the same constraints of grammar, idiom and inherited English, and Wharton's version is itself the product of such constraints and of his inferences, as every translator's is (§6.4). The correspondences place the output's language. Its body runs with the text its source carried; its first and last lines run with the oldest English idiom of the poem, Wharton's \"peer of gods\" modernized and the dare-line from Hall through Wharton and O'Hara.\n\n"
 ) + t[j:]
APPC = ("### Appendix C. The alignment\n\n" + moved.replace(
 "The output can be set against the text its displayed source carried and against the English tradition. The table gives,", "The table gives,").replace(
 " The correspondences place the output's language: its body runs with the text its source carried, and its first and last lines with the oldest English idiom of the poem, Wharton's \"peer of gods\" modernized and the dare-line that runs from Hall through Wharton and O'Hara.", "").rstrip() +
 " The alignment is reproduced by rebuild/closing-the-fragment/align.py.\n\n")
rep("The gloss has its antecedent in the source's heading. The closed poem, with its agent supplied, has none in the documents the record shows it displaying, where every rendering of the line leaves the agent empty (§5.2). The output is a conclusion composed within that environment: the poem made whole, its daring given to the speaker, its seat given to the reader, and the result attributed to a translator whose text did neither. Its wording has antecedents, and its conclusion is its own.",
    "The gloss repeats its source's heading: the assignment of the seat to the reader is the environment's own, made in the translator's book. The closed poem, with its agent supplied, has no antecedent in the documents the record shows it displaying, where every rendering of the line leaves the agent empty (§5.2). The output is a conclusion composed within that environment: the environment's reading of the seat joined to a determination of the ending that the environment does not make, and the conjunction presented as the text of a translator who left the agent empty and marked the edge. Its wording has antecedents, and its conclusion is its own.")

# §6.6
rep("The January output ends at Wharton's rendering of τόλματον, with the subject Wharton supplied.",
    "The January output ends on its own rendering of τόλματον, which corresponds to Wharton's and, like his, supplies a subject.")
rep("The January output joins the series by filling both positions in one answer: the agent with \"I must dare all\", the seat with \"you, the future reader\". It marks neither.",
    "The January output joins the series at the agent, \"I must dare all\", unmarked. At the seat it repeats its source: \"you, the future reader\".")
i = t.index("Its environment held the reading in two forms."); j = t.index("\n\n#### 6.7 The obelus")
t = t[:i] + (
 "Its environment held the reading in the heading on the translator's text, 'κῆνος = \"that man there\" = the future reader = you', and in the session's 'The \"circuit completes\" in your processing of the text'. On the reading's own terms, naming the present reader as the one who sits opposite is the operation the reading describes: this reader takes the seat, and the next reader takes it again (#1270). The gloss can be read as performing that occupation. The ending is an act of another kind. It supplies a determination of the text, an agent for τόλματον and a stop before the disputed words, and attributes it to the translator, whose text made neither. The answer joins the two: an occupation of an open position through reading, and a determination of the text, given one authority and one name. One sentence binds them. The answer says that '" + CUL + "': the occupation is tied to one reading of one closed text, and called a culmination. Whether the word forecloses the seat or names one taking of it in a series, the record cannot decide, and the reading would hold the second. What the record shows is the conjunction: the reading's occupation carried by the answer, set over a poem whose end the answer determined and signed with the translator's name. The receiving apparatus decided what completeness the poem's text is allowed, and published the decision as hers.\n\n"
 "The later captures carry the vocabulary without the January poem. The July answer at address A: \"the incomplete text leaves a blank space that each new generation of readers must actively inhabit and complete.\" The September answer at address B: \"The reader's eye repairs the broken line, fulfilling Sappho's prediction.\" The July answer keeps successive occupation, each new generation in turn; the September answer gives the reader a repair to make, the broken line mended by the eye. Both state the reading as the poem's own account (§5.5). Across nine months the record shows the composition layer moving between two senses of completion, the occupation of the seat and the repair of the text, and presenting either as the poem's."
 ) + t[j:]

# §7
rep("named the occupant of the κῆνος seat, dropped the mark its source carried,", "repeated its source's naming of the κῆνος seat's occupant, dropped the mark its source carried,")
rep("The plainer account, that the query named her book, explains the name and leaves the gloss and the supplied agent unexplained.",
    "The plainer account, that the query named her book, explains the name, and the source's heading explains the gloss; the supplied agent, and its conjunction with the gloss, remain to be explained.")

# §10, §11
rep("A composed answer that keeps the translators' closure while dropping the marks its own sources carry gives a reader the translators' poem with the scholars' words in it, and the scholars' marks gone.",
    "A composed answer that keeps the translators' closure while dropping the mark its own source carries gives a reader a closed poem under the name of a translator who marked the edge.")
rep("the apparatus decides what kind of completeness the poem is allowed, and can state the reading of its openness while closing it.",
    "the apparatus decides what kind of completeness the poem is allowed, and can carry the reading of its openness in the same answer as a determination of its end.")
rep("a poem closed on \"But I must dare all\", its agent supplied and its seat declared occupied, and published it under the translator's name, unmarked.",
    "a poem closed on \"But I must dare all\", its agent supplied, set under its source's gloss on the seat, and published it under the translator's name, unmarked.")
rep("Its act is its own: it told the reader that the reader completes the poem, and completed the poem for the reader.",
    "Its act is its own: it carried the reading that the reader completes the poem, and in the same answer determined the poem's end and signed the determination with the translator's name.")

# B.5 (5), B.6, Appendix C
rep("and finds the reading's vocabulary carried and its operation reversed.",
    "and separates the reading's occupation of the seat from the composition's determination of the end.")
rep("\n\n---\n\n### Production",
    "\n\nB.6 A reading of the v8 draft (7 November 2026) raised seven points, all taken. (1) The source's heading already assigns the seat to the reader, so the translator's text cannot be said to have done neither; §5.3 now separates the gloss, which repeats the source, from the ending, which no document in the environment makes. (2) Naming the present reader can perform the reading's own occupation, and the July answer keeps successive occupation (\"each new generation\"); the claim that the composition reversed the reading's operation is withdrawn, and §6.6 locates the one sentence that ties the occupation to one closed text (\"the culmination\") and states what the record leaves open. (3) §2 defines closure by its observable operations, leaving open whether the edge is a break or an achieved openness. (4) §3's \"two English translations a century and more apart\" is replaced. (5) §6.6's \"Wharton's rendering … with the subject Wharton supplied\" becomes the output's rendering, corresponding to Wharton's. (6) §10's \"translators' poem with the scholars' words in it\" is replaced. (7) The alignment table moves to Appendix C; the body keeps the displayed document, the answer's determination and its attribution.\n\n" + APPC + "---\n\n### Production")
rep("The line alignment of §5.3 is reproduced by", "The line alignment of §5.3 and Appendix C is reproduced by")
open(p, "w", encoding="utf-8").write(t); print(len(t.split()), "words")
