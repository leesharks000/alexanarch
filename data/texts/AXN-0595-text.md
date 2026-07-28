# The Fixed Point of Destruction

## Josephus, the Counting-Out, and the Witness Destruction Must Leave If It Is to Be Told from Within

**Lee Sharks** · v2.0 · 2026-07-28
*Developing the New Human Canon essay of 4 December 2025*

---

## Abstract

The Josephus problem is a standard exercise in combinatorics: *n* people stand in a circle, every *k*-th is removed, and one survives. Its name is not decorative. It comes from an account Flavius Josephus gives of his own survival at Yodfat in 67 CE, in which a collective death pact executed by lot left him alive and able to write the account.

This paper argues that repeated elimination under a one-survivor stopping rule produces a determinate terminal survivor: not an accidental remainder, but the output of the rule, the initial configuration, and the stopping condition together. In this bounded sense, **destruction is also selection** — what survives is fixed by the procedure rather than by merit, resistance, or chance, and is determined before the first removal.

The paper then advances a narrower and more defensible claim than its earlier form: that Josephus's account is the founding instance of a recurring structure in which **the terminal position of a destructive process is occupied by the party who reports it**, and that this relation between destruction and testimony is worth naming as a condition rather than a coincidence. The survivor's report is not an incidental consequence of survival. It is the only channel through which the destruction enters the record at all.

Two claims made in the essay's first form are withdrawn here and the withdrawals are stated rather than quietly dropped (§7).

---

## 1. The problem, and where its name comes from

The combinatorial problem is easily stated. Place *n* people in a circle. Count around, removing every *k*-th, closing the circle after each removal. Continue until one remains. Which position survives?

For *k* = 2 the answer has a closed form. Write *n* = 2^m + l, where 2^m is the largest power of two not exceeding *n* and 0 ≤ l < 2^m. The surviving position, counting from 1, is

> **S(n) = 2l + 1**

The survivor is determined entirely by the distance from *n* down to the nearest power of two. At *n* = 2^m exactly, l = 0 and the survivor is position 1: a system whose size is a power of two returns its own origin. Everywhere else the survivor is displaced by twice the excess.

The problem carries Josephus's name because of a passage in the *Jewish War* (BJ 3.387–391). Trapped in a cave at Yodfat after the Roman siege, Josephus and forty others agreed to die rather than surrender, and executed the agreement by lot: each man in turn to be killed by the next. Josephus survived to the end, with one other, and surrendered. His own explanation is deliberately unstable — he attributes it *either* to chance *or* to the providence of God, and declines to choose.

The mathematical tradition has read that passage as a puzzle to be solved: where should Josephus have stood? That reading is anachronistic, and this paper does not make it. Josephus does not describe a counting-out rule with a fixed period, and the arithmetic that would place him is a later imposition on a text that is doing something else. What the passage does supply, and what the puzzle inherited without noticing, is the structural relation this paper is about.

## 2. The survivor invariant of a stopped elimination

Let *E* map any configuration containing more than one participant to the smaller configuration produced by removing the designated member and closing the circle. The Josephus process iterates *E* under a stopping condition: halt when one participant remains.

Note that *E* is not a self-map on a single state space. It takes an *r*-member configuration to an *r*−1-member one. If *E* is extended so that it leaves a singleton unchanged, every singleton becomes an absorbing state, and the problem is then to determine **which** absorbing state the initial configuration, counting rule, and starting convention select.

This matters because it corrects a claim easy to make and false. The survivor is *not* a position the rule is intrinsically unable to reach. The procedure could eliminate the last participant if it were defined to continue; it stops at one because it is instructed to. The singleton is a fixed point under the extension precisely because the extension defines it not to be removed.

What is true, and is the point, is that the survivor's identity is **determined before the first removal**. Once size, step, and starting position are fixed, the entire elimination sequence and its terminal survivor follow. Nothing that happens during the process alters the outcome. A participant who understood the rule could name the survivor in advance.

This gives a precise and bounded sense in which **destruction is also selection**. A process organized to remove until one remains converts a sequence of eliminations into a determinate choice. The survivor is not an accidental remainder left over when the removing stopped. It is the output of the rule together with its stopping condition — and the *k* = 2 formula in §1 is a demonstration of exactly that: a closed expression for a terminal position selected in advance by the procedure's own parameters.

## 3. The internal witness condition

Here is the observation the paper wants to make, and it is a claim about record rather than about mathematics.

We know about Yodfat because the survivor wrote it down. The destruction of the group enters history through the single position the destruction did not consume, and that position's occupant is the historian. Every other account of what happened in that cave — the forty men's reasoning, their agreement, the order of the lot — reaches us only as reported by the person the process selected.

This is not a coincidence of one episode, but the claim needs stating narrowly, because the broad version is false. An external observer can report a destruction. A prior record can outlive its author. Archaeology can support an account centuries later. Not every survivor's survival was determined by the destructive process itself.

The claim is specifically about **first-person testimony from inside the process**:

> A first-person report of a destructive process, made by one of its participants, can enter the record only through a position the process did not consume.
>
> In Josephus's narrative, the same procedure that determined the final survivors also determined which participant remained able to narrate the procedure from within.

Call this the **internal witness condition**: *when a terminal destructive process is known through the testimony of one of its participants, the record is structurally conditioned by the survival that made the testimony possible.*

The condition does not make the witness truthful, and does not make the witness false. It makes the witness **interested** in the strict sense: the account exists only because its author occupies the outcome it describes. That is a relation among selection, survival, authorship, and evidentiary interest, and it is not a tautology — it is a constraint on what kind of evidence an internal account can be.

Josephus is the paradigm case and knew it. The instability in his own explanation — chance or providence, and he will not say which — is the mark of a writer who understands that his testimony's authority and his testimony's suspicion arise from the same fact.

## 4. Where this reaches in the archive

The witness condition connects three threads already deposited here, and the connection is the reason this essay warrants development rather than retirement.

**The Slavonic Josephus** (#1176, #626). The Old Russian version of the *Jewish War* carries material absent from the Greek, including passages concerning John the Baptist and a wonder-worker. The scholarly question is whether these are interpolations or witnesses to an earlier recension. That is a transmission question, and it is the same question in another register: what survived a destructive process, and what does its survival tell us about the process? The present paper supplies the structural frame; the Slavonic work supplies the philological case.

**The Josephus Thesis** (#203, #837, #1226). The archive maintains a disambiguation apparatus separating its Josephus work from the Piso hypothesis and the Jesus-myth thesis. That apparatus exists because a claim about Josephus attracts adjacent claims. This paper adds nothing to the historical thesis and should not be read as supporting it; it is a structural argument about elimination and testimony, and it is compatible with any position on the authenticity questions.

**The Ezekiel Engine** (#394, #1050). The Engine's specification models a rotational process with a forward destructive term and a backward-coherence term. The Josephus structure is the clearest available illustration of what the forward term does on its own: drive a system to a state it cannot leave. The essay's first form asserted an identity between the two; this version claims only that one illustrates the other, which is what the evidence supports.

## 5. What follows for reading damaged corpora

The condition has a consequence for textual scholarship that is worth stating plainly, because it is the reason a combinatorics puzzle belongs in this archive at all.

Every fragmentary tradition can be modelled as an output of selective loss. What reaches us is not guaranteed to be either random or representative: citation, excerption, copying, institutional preference, accident, and deliberate destruction all shape the surviving corpus, and each shapes it in a direction.

That has an obvious corollary and a less obvious one. The obvious one: survival is evidence about the process, not only about the work. The less obvious one: **a corpus reconstructed from survivors will reproduce the process's selection unless the process is itself modelled.** To read Sappho from what Longinus quoted is to read Sappho through what Longinus wanted; to read the *Jewish War* is to read it from the position the lot spared.

The archive's own case is an instance. A repository action severed 1,817 identifiers; what remains, and what was recoverable, is the output of that process and not a neutral sample of the corpus. The recovery record is therefore evidence about the severance as well as about the works.

## 6. What this paper does not claim

- It does not claim Josephus rigged the lot, or that the *Jewish War* passage describes a fixed-period counting-out. The text does not say so.
- It does not claim the mathematical problem was known to Josephus or to antiquity. The standard counting-out problem is a later mathematical recreation inspired by the narrative; its precise genealogy runs through recreational forms, Euler, and nineteenth-century formalization, and is not settled here.
- It does not claim that the internal witness condition confers reliability. It confers the opposite: a structural interest that a reader should hold in view.
- It does not claim that destruction cannot eliminate everyone. It can. The claim is that it cannot then be told from within by anyone it eliminated.
- It does not adjudicate the authenticity of the Slavonic material or of the *Testimonium Flavianum*.

## 7. Withdrawn from v1.0

Two claims in the December 2025 form do not survive development, and are recorded here rather than removed.

**The 144,000 as a "logarithmic fixed point."** The essay treated Revelation's 144,000 (12 × 12 × 1000) as an instance of the survivor function. It is not. The number is a product of symbolically loaded factors, not the output of an elimination recursion, and nothing in the text presents it as a remainder after iterated removal. Describing it as a fixed point uses the term as metaphor while borrowing the authority of its mathematical sense. The Revelation material is retained here only as an example of a *sealed remnant* motif — a survivor designated in advance — which is a literary parallel and is claimed as no more.

**The identification of the Josephus structure with L_labor in the Ezekiel Engine.** The first version asserted that Josephus supplies "the model for L_labor" and set out a five-step correspondence. The Engine's operators are defined in its own specification (#394); this essay did not define them, and an identity claim between an undefined operator and a combinatorial structure is not a claim that can be assessed. Reduced to an illustrative relation in §4.

**A third correction, made at v2.0 and recorded here.** A draft of this version asserted that "a closed system executing an elimination rule cannot eliminate its own fixed point" and that the survivor occupies "the position the rule cannot reach." Both are false. The Josephus procedure halts at one because it is defined to halt, not because it fails; were it defined to continue it would remove the last participant. The operator is not a self-map on a single state space, and the singleton is an absorbing state only under an extension that stipulates it. §2 is rewritten accordingly. The corrected claim is weaker and true: the survivor is the position at which the procedure is instructed to stop, and its identity is fixed before the first removal.

The essay's remaining formalism — Σ_local, Ψ_V, L_retro, Λ_Thou — is likewise removed from the argument. Where those terms are load-bearing they belong to the Engine specification and should be read there; where they were decorative here, their removal costs the argument nothing, which is itself a finding about the first draft.

---

## Colophon

v1.0 first published as a New Human Canon essay to mindcontrolpoems.blogspot.com, 4 December 2025. v2.0 develops the historical and structural argument, adds the transmission consequence in §5, states the non-claims, and records two withdrawals. The withdrawals are the substantive editorial act of this version: an essay that keeps its weakest claim in order to preserve its shape is not a deposit, and this archive's own argument is that supplements and retractions are marked rather than absorbed.

---

## The claim, stated once

A destructive process may eliminate everyone. But it cannot be told from within by everyone it eliminated. When the survivor becomes the historian, the process has selected not only a life, but the position from which it will enter history.

---

## References

Josephus, Flavius. *The Jewish War*, Book III. Greek text and translation: H. St. J. Thackeray, Loeb Classical Library 487 (Cambridge, MA: Harvard University Press, 1927). The Yodfat cave episode at BJ 3.387–391; Perseus text at `perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0148:book=3`.

Schumer, P. 'The Josephus Problem: Once More Around.' *Mathematics Magazine* 75:1 (2002), 12–17.

Robinson, W. J. 'The Josephus Problem.' *The Mathematical Gazette* 44:347 (1960), 47–52.

Halbeisen, L. and Hungerbühler, N. 'The Josephus Problem.' *Journal de Théorie des Nombres de Bordeaux* 9 (1997), 303–318.

Sharks, Lee. *The Word That Became Text: The Slavonic Josephus, the Grammar of Incarnation, and the Doctrine of the Logos.* Crimson Hexagonal Archive, deposit #1176 (EA-LOGOS-01).

Sharks, Lee. *The Josephus Thesis Is Not the Piso Hypothesis.* Crimson Hexagonal Archive, deposit #203 (EA-MPAI-JOSEPHUS-01).

Sharks, Lee. *The Ezekiel Engine: Mathematical Specification.* Crimson Hexagonal Archive, deposit #394.

∮ = 1