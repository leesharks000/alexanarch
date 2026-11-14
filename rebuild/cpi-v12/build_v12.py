#!/usr/bin/env python3
"""Build CPI v1.2 from the deposited v1.0 text of #1766 (data/texts/AXN-0C8B-text.md), adding:
§11.5 from the v1.1 working draft (with its seat references brought up to EA-CORPORA-38), §11.6 rewritten
(sec11-6-expanded.md), step 5a in §11.3, a pointer in §11.0j, the seats in the §11.2 table, the abstract's
sentence on the reception history, and the v1.1 and v1.2 entries in Appendix B. Every replacement must match once.
    python3 build_v12.py <alexanarch root> <out.md>"""
import pathlib, re, sys

ROOT = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2]); H = pathlib.Path(__file__).parent
dep = (ROOT / "data/texts/AXN-0C8B-text.md").read_text(encoding="utf-8")
v11 = (H / "Critique-of-Pure-Inference-v1.1.md").read_text(encoding="utf-8")
s116 = (H / "sec11-6-expanded.md").read_text(encoding="utf-8").strip()


def once(s, a, b):
    assert s.count(a) == 1, (s.count(a), a[:90]); return s.replace(a, b)


# §11.5 as it stands in v1.1
i = v11.index("### 11.5 Chapter: logic complete since Aristotle"); j = v11.index("### 11.6 The witnesses between")
s115 = v11[i:j].strip()
s115 = once(s115, "The text is staged from First1KGreek tlg0732.tlg005. The locus reported for it is Wallies 124.8–13, which is to be checked against the printed page before it is relied on.",
            "The text is seated from First1KGreek tlg0732.tlg005 (EA-CORPORA-38/02), where it stands on Wallies's page 124 by the file's marks; the standard citation is 124.8, and the line is to be checked against the printed page.")
s115 = once(s115, "Those witnesses are tranche D of EA-CORPORA-38.",
            "They are seated in EA-CORPORA-38 (#1768) and read in §11.6, which also revises the claim. What the witnesses show is several operations, O1–O6, whose relations reception preserves and severs by turns (11.6.0b).")
k = s115.index("11.5.8 **To do before this chapter is deposited.**")
s115 = s115[:k] + ("11.5.8 **What remains owed here.** Alexander is seated (38/02) and the companions' rule stands on Wallies's page 124 by the file's marks; its line is to be read on the printed page. "
                   "Kant's AA III page numbers for B ix and A133/B172 are to be given from the seated page images. The *Metaphysics* loci are to be given by Usener's pages. "
                   "The transmission witnesses are seated and read in §11.6, and what they leave owed is listed at 11.6.17.")
assert "\\(" not in s115 + s116 and "\\[" not in s115 + s116

t = dep
t = once(t, "\nversion: v1.0\n", "\nversion: v1.2\n")
t = once(t, "Lee Sharks · v1.0 · 13 November 2026", "Lee Sharks · v1.2 (14 November 2026, in place) · v1.0 13 November 2026")
t = once(t, "and the history of every version is kept in Appendix B.*",
         "and the history of every version is kept in Appendix B. v1.2 (14 November 2026, in place) adds the reception history of §11.5–11.6, read from the witnesses seated for it in EA-CORPORA-38 (#1768), revised on two reviews by ChatGPT (LABOR).*")
t = once(t, "It applies equally to the archive that runs it.\n",
         "It applies equally to the archive that runs it. A reception history read from witnesses seated for it (§11.5–11.6) follows several operations of the Peripatetic logic from Theophrastus to Frege. It shows them preserved, reassigned, rejected and made productive again, and shows how an operation can stay available while its contribution becomes hard to recognize under the received account of the discipline.\n")
t = once(t, "| AA III, Hegel WdL 1812/1832 (to seat) |", "| kant-akademie-ausgabe, hegel-wissenschaft-der-logik (EA-CORPORA-38); read in §11.5–11.6 |")
t = once(t, "| Epictetus (staged) |", "| epictetus-dissertationes-schenkl-1916 (EA-CORPORA-38/05) |")
step5 = re.search(r"\n5\. \*\*Carry the grade\.\*\*[^\n]*\n", t).group(0)
t = once(t, step5, step5 + ("5a. **Carry the route of each premise.** Record how each premise was established: by induction, from a hypothesis, from evidence, or through an inference with its own grade. "
                            "Keep the route attached for as long as the premise is used, so that a premise admitted by induction does not enter a later derivation as if demonstrated (§11.6.1a). "
                            "The classification of routes is Theophrastus's, reported by Alexander (*In APr* 388); the requirement is derived from §3.10, §3.14 and the prohibition on unearned strengthening.\n"))
m = re.search(r"\n11\.0j \*\*The executor\.\*\*[^\n]*\n", t).group(0)
t = once(t, m, m.rstrip("\n") + (" Alexander names the gap in another setting. Holding arguments already reduced to the figures is \"τήρησιν … ἀναίτιον ἀλλ᾿ οὐκ ἐπιστήμην\", "
                                 "an observation without the cause and not knowledge, set against the method by which a new argument is analysed (*In APr* 340; §11.6.1, O5). "
                                 "The comparison names a common absence and does not identify the cases.\n"))
t = once(t, "\n# Part III. The practice of critique\n", "\n" + s115 + "\n\n" + s116 + "\n\n# Part III. The practice of critique\n")
b = v11[v11.index("**v1.1 (working).**"):v11.index("**v1.0.** The consolidating rewrite")]
b = b.replace("**v1.1 (working).**", "**v1.1 (working draft, not deposited).**")
v12 = ("**v1.2 (14 November 2026, reissued in place).** §11.6 rewritten from the witnesses seated in EA-CORPORA-38 (#1768): Alexander (the five moods at 69 and 110; Theophrastus's own *Analytics* at 390; the routes of an added premise at 388; method against a stock of reductions at 340), Philoponus (123–124, 205, 242, 302), Cicero's *Topica* §6, Epictetus 2.19, Boethius in PL 64, Ibn Sīnā's *Ishārāt*, the Nyāyasūtra with Vātsyāyana, Meier's *Auszug* §372, Kant 1762 (AA II 53–55), Hegel's *Wissenschaft der Logik*, Peirce 1867 and 1878, Frege's *Begriffsschrift* §6 and Carroll. "
       "Revised on ChatGPT (LABOR)'s review of the expanded draft. The governing claim is reorganized around six operations (O1–O6) whose relations reception preserves or severs. Alexander's classification of premise routes is kept as a classification, and the requirement to carry a route is argued from §3 (11.6.1a; §11.3 step 5a). Kant's correspondence with the Theophrastean placement is held to the organization and reduction of syllogistic forms. Hegel is read for what his framing removes. "
       "v1.1's reading of Jäsche's \"nicht zweifelhaft\" as a dropped hedge is withdrawn (11.6.13): its object is the ascertainability of Kant's judgment. Peirce is held to co-presence and structural affinity, and the 1867 print is the witness for 1867. The Nyāya is made the control: classification out of a proof is not loss from the knowledge practice. The crocodile is reported as Ibn Sīnā's counterexample. "
       "Also: §11.0j points to O5; §11.3 gains step 5a; the §11.2 table names the seats; the abstract gains a sentence; §11.5's seat references are brought up to #1768. Nothing in v1.0 is removed.\n\n")
t = once(t, "**v1.0.** The consolidating rewrite", v12 + b + "**v1.0.** The consolidating rewrite")
for chk in ("version: v1.2", "### 11.5 Chapter: logic complete since Aristotle", "### 11.6 The witnesses between: what reception does", "5a. **Carry the route", "**v1.2 (14 November 2026"):
    assert t.count(chk) == 1, chk
OUT.write_text(t, encoding="utf-8")
print(OUT, len(t.split()), "words")
