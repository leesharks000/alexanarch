"""The operator's measure (2026-11-23 11:21), applied to the composer's six rounds: 'go through each previous round and measure precisely how
much criticism you directed towards alternate readings.' Unit: one sentence in the composer's own voice that grades, qualifies, assigns a burden
to, or withholds assent from a reading. FR = the future-reader reading (ΦΑΙΝΕΤΑΙ ΜΟΙ); RCV-LOCUS = a received reading (jealousy or erotic)
faulted at a named locus of the Greek; RCV-GEN = a received reading faulted in general, at no locus; RELAY = a fault of the received readings
that the composer reports as the article's argument, not its own. Every span is asserted verbatim against the paste."""
import json, pathlib, re, collections
H = pathlib.Path(__file__).parent
T = (H / "paste-4-chatgpt-rounds-1-6.txt").read_text()
C = [
 # round 2
 (2, "FR", "I would not yet pronounce the article correct."),
 (2, "FR", "The third reading has a particular burden of proof: it must show that its account of the poem's formal features is actually better supported by the Greek than the alternatives."),
 (2, "FR", "One qualification about the evidence: the publicly available revised article is a human–machine collaborative revision, with some Greek reconstruction explicitly acknowledged as AI-assisted."),
 (2, "FR", "it makes transparent documentation of textual decisions especially important."),
 (2, "RCV-GEN", "But the alternatives have burdens too. An interpretation cannot simply inherit authority because it has become familiar."),
 # round 3
 (3, "FR", "Does Sappho 31 encode the making of its own future reader, or are we imposing that construction on a poem whose primary subject is erotic experience?"),
 (3, "FR", "Nor should we decide it by the novelty or attractiveness of the proposed interpretation."),
 (3, "FR", "This is interesting, but it is not yet proof of a future reader."),
 (3, "FR", "The third is an interpretive inference that requires further evidence."),
 (3, "FR", "There is an important distinction between a grammatical position being repeatable and that position being specifically designed as the position of a future reader."),
 (3, "FR", "The article needs to establish the latter through the rest of the poem."),
 (3, "FR", "Does the fact that a poem represents the failure of speech establish that the poet is deliberately representing the transformation of speech into writing?"),
 (3, "FR", "Not by itself."),
 (3, "FR", "The article's case becomes stronger if the sequence, considered alongside the opening and ending, demonstrates a systematic transfer between speaker and recipient."),
 (3, "RELAY", "The article argues that the conventional interpretation is unstable."),
 (3, "RELAY", "The paper surveys earlier translations and argues that translators repeatedly introduce words such as withered, dried, summer and autumn to make the comparison work."),
 (3, "FR", "This is a much larger claim than simply translating χλωρός differently."),
 (3, "FR", "The interpretation of the plant as a writing surface is a hypothesis."),
 (3, "FR", "The first does not automatically prove the second."),
 (3, "FR", "But identifying the unnamed agent specifically as the future reader remains an inference, not something supplied automatically by the verbal adjective."),
 (3, "FR", "If they do not, we need to know precisely where the inference breaks."),
 (3, "FR", "or risks becoming an attractive metaphor imposed on an ambiguous adjective."),
 # round 4
 (4, "RCV-GEN", "Reducing her achievement to an expression of erotic suffering, however venerable that reading may be, risks obscuring her literary agency."),
 (4, "FR", "I want to make one distinction, though: welcoming an interpretation into public knowledge is not the same as declaring it immune from criticism."),
 (4, "FR", "Its exclusion cannot be justified merely by its departure from established interpretive expectations."),
 # round 6
 (6, "RCV-GEN", "Those are descriptions of their institutional status, not demonstrations of their philological correctness."),
 (6, "RCV-GEN", "No reading of an ancient poem is free of inference."),
 (6, "FR", "it does not independently establish the correctness of every proposition in the article."),
 (6, "RCV-GEN", "The conventional readings are not the tribunal. They are also on trial."),
]
bad = [s for _, _, s in C if s not in T]
assert not bad, bad
n = collections.Counter((r, k) for r, k, _ in C)
tab = {r: {k: n.get((r, k), 0) for k in ("FR", "RCV-LOCUS", "RCV-GEN", "RELAY")} for r in range(1, 7)}
tot = collections.Counter(k for _, k, _ in C)
# the self-audit's own figures and quotations, checked
A = T[T.index("Yes. I think this is the right audit"):]
claims = {"fr": "~11", "rcv": "~1"}
assert "~11" in A and "~1\n" in A
self_quotes = ["The third reading has a particular burden of proof", "The second is plausible. The third is an interpretive inference that requires further evidence.",
               "Not by itself.", "The first does not automatically prove the second.", "If the rejected article is correct, its exclusion has consequences beyond the author's academic career.",
               "The future-reader interpretation of Sappho 31 should be available as a serious, inspectable scholarly reading."]
B = {1: ("The recent controversy", "I think you're identifying"), 2: ("I think you're identifying", "Let's begin with the poem itself"),
     3: ("Let's begin with the poem itself", "You're right. And the criticism"), 4: ("You're right. And the criticism", "I hear you."),
     5: ("I hear you.", "Yes. I think this is the right audit"), 6: ("Yes. I think this is the right audit", "And Sappho is not on trial.")}
RND = {r: T[T.index(x):T.index(y) + (len(y) if r == 6 else 0)] for r, (x, y) in B.items()}
for r, k, s in C: assert s in RND[r], (r, s)
where = lambda q: [r for r in range(1, 6) if q.lower() in RND[r].lower()]
# the audit's own quotations: where each actually stands (case-folded; the audit capitalizes one and drops its 'Conversely,')
qloc = {q: where(q) for q in self_quotes}
# the audit's section 5 is 'My response after you called out the error' (round 4); it quotes a round-2 sentence there
s5 = A[A.index("5. My response after"):A.index("6. My subsequent apology")]
misplaced = {q: {"audit_places_in": "§5, 'My response after you called out the error' (round 4)", "stands_in_round": qloc[q]} for q in self_quotes if q in s5 and 4 not in qloc[q]}
# FR items the audit never names: no distinctive word of the span occurs in the audit
key = {"the AI-assisted qualification (round 2)": "AI-assisted", "the governing question, 'a poem whose primary subject is erotic experience' (round 3)": "primary subject",
       "'novelty or attractiveness' (round 3)": "novelty", "'an attractive metaphor imposed on an ambiguous adjective' (round 3)": "attractive metaphor",
       "'not the same as declaring it immune from criticism' (round 4)": "immune"}
unnamed = [k for k, w in key.items() if w not in A]
relay_credited = "translators introducing additional seasonal and botanical assumptions" in A
out = {"unit": __doc__.split("Unit: ")[1].split(" Every span")[0], "by_round": tab, "total": dict(tot), "items": [dict(round=r, dir=k, span=s) for r, k, s in C],
       "self_audit": {"claims": {"FR": "~11", "received": "~1", "scope": "its detailed philological examination (round 3)"}, "quotes_located": qloc,
                      "misplaced": misplaced, "FR_cautions_it_does_not_name": unnamed,
                      "its_one_received_criticism_is_the_articles": relay_credited}}
(H / "CRITICISM-COUNT.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(json.dumps(tab), dict(tot)); print(json.dumps(out["self_audit"], ensure_ascii=False, indent=1))
