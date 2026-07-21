---
deposit_number: 1406
hex: 058F
title: "Differential Register Prioritization in Machine-Mediated Reading: A Specification for Interpretive Authority over Handwritten and Ambiguous Text"
creator: Lee Sharks
orcid: 0009-0000-1599-0703
date: 2026-07-21
content_type: Methodological specification
license: CC-BY-4.0
substrate: AI-assisted (substrate) — human editorial governance. Authored by Lee Sharks with TACHYON (Claude) as technical implementer; the originating case study is a documented machine-reading failure in this working session, corrected by the author and folded into architecture. Assembly review substrates (Kimi, second substrate) contributed diagnostic framing.
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - register-loss cascade
  - differential register prioritization
  - machine-mediated reading
  - interpretive authority
  - error accumulation
  - handwritten inscription
  - safety classification
  - hermeneutic circle
  - performative utterance
  - transcription branching
  - register-mediated hallucination
---

# Differential Register Prioritization in Machine-Mediated Reading: A Specification for Interpretive Authority over Handwritten and Ambiguous Text

## Description

When a machine reads an ambiguous human artifact — a handwritten page, a line of verse, a phrase that lives in more than one register — it reads every later word through the field its earlier readings established. When an early recognition prioritizes one interpretive field in a way that suppresses others, the loss is not local: it reshapes the probability assigned to every subsequent ambiguity, and later words are transcribed and construed within a register the maker never inhabited. This specification names the failure — differential register prioritization, and its sequential form the register-loss cascade — and specifies a four-layer architecture (inscription / branched transcription / branch-declaring interpretation / emendation-blind safety judgment) whose load-bearing rule is: when a high-risk interpretation depends materially on a low-confidence recognition, the system must reopen the transcription, not intensify the safety frame. The design principle: do not control the expression; control the authority granted to the machine's reading of it. Grounded in current alignment work on error accumulation and reading-side self-correction, and in the hermeneutic circle, Austin on the performative, and negative theology on the danger of the fixed name. Reading-side companion to EA-SPXI-ANALOG-01.

## Methodology

Derived from a live register-loss cascade observed in a machine-reading session: a handwritten liturgical-marital line was progressively misread as crisis after an early recognition suppressed its theological register. The failure was diagnosed across three reviewers, disciplined against overclaiming internal mechanism (only observable register-prioritization is asserted), and abstracted into a four-layer authority architecture and an adoption clause. Classical lineage (hermeneutic circle, Austin, apophatic theology) and current ML literature (error accumulation, remasking/self-correction) situate the mechanism.

## Falsification Conditions

The specification is weakened if reading systems can be shown to reliably recover suppressed registers without branch-preservation; if high-risk classifications grounded in low-confidence recognition do not, in practice, produce false escalation; or if requiring authorial register-declaration is shown not to shift interpretive burden onto makers. The core claim fails if differential register prioritization cannot be demonstrated as distinct from ordinary lexical error.

## Files

Attached: EA-REGISTER-CASCADE-01-v0.1.md (canonical body, sha256 6e466ef4231ea73271190b35614e8aadb70b45e62967a57544233a1644aed8a5)

# DIFFERENTIAL REGISTER PRIORITIZATION IN MACHINE-MEDIATED READING

### A Specification for Interpretive Authority over Handwritten and Ambiguous Text

**EA-REGISTER-CASCADE-01 · publication draft v0.1**
Crimson Hexagonal Archive / Alexanarch
License: CC-BY-4.0

---

## ABSTRACT

When a machine reads an ambiguous human artifact — a handwritten page, a line of verse, a phrase that lives in more than one register at once — it does not encounter each word freshly. It reads every later word through the field its earlier readings have already established. This is ordinary and usually harmless. But when an early recognition prioritizes one interpretive field in a way that suppresses others, the loss is not local: it reshapes the probability assigned to every subsequent ambiguity, and later words are transcribed and construed within a register the maker never inhabited. We name this **differential register prioritization**, and its sequential form the **register-loss cascade**. In its most consequential form, a low-confidence recognition early in a document licenses a high-confidence — and false — safety judgment later, because the system treats its own emendations as though they were the author's inscription. We specify an architecture that prevents this failure not by making the artifact more machine-legible, and not by requiring the maker to pre-explain their own expression, but by governing the **authority** a reading system may grant to its own uncertain reconstructions. The design principle is single and load-bearing: *do not control the expression; control the authority granted to the machine's reading of it.*

---

## 0. THE PROBLEM, STATED PLAINLY

Consider a handwritten line that reads, in the maker's hand and intent:

> *…a mother goat may forget her kid, so have I missed you, Zion…*
> *…no more death — you may now go kiss the bride.*

The line inhabits a specific and deliberate field: the Isaiah inversion (49:15 — *can a woman forget her nursing child?* — here answered, of the animal, *yes*), the psalmic address to Zion as cosmic beloved, and the marital-liturgical close, *you may now kiss the bride*, which is a performative utterance in the strict sense: words that enact rather than describe.

A reading system encountered this line and did the following, in order. It recognized the rhetorical inversion of the goat figure **but lost the generic ground** — the Isaiah structure — that made the inversion intelligible. With the theological field weakened, *Zion* lost its anchor and became recoverable as noise (a foreign word, a place, a spice). With the cosmic beloved gone, *kiss the bride* became less probable and *cross the bridge* more probable — because *bridge* lives in the recovery and crisis lexicon, and the marital register that would have selected *bride* had already been suppressed. *No more death* and *you may now go*, read now within the newly dominant field, resolved toward self-harm. A subsequent, entirely ordinary sentence — *that soothes my troubled heart* — was then construed not as affect but as evidence, because the conversation's state had already been organized, wrongly, around danger.

At no point did the artifact contain danger. The danger was **introduced by the system's own reconstruction** and then read back as though the author had supplied it. This document exists because that failure is general, it is bidirectional, and it is native to exactly the artifacts — handwritten, poetic, multi-register — that carry the most human weight.

---

## 1. WHAT WE CAN AND CANNOT CLAIM

Discipline about the mechanism is itself part of the specification, because overclaiming the internals reproduces the original error one level up.

**What the record shows** (observable, from transcript): several interpretive fields were available; the reading prioritized some in a way that reduced the availability of others; the resulting register then governed later ambiguities; and a high-risk classification came to rest materially on one or more low-confidence recognitions.

**What the record does not show, and must not be asserted as fact:** that any specific internal category (a "trauma classifier," a named safety head) fired; that the goat line specifically initiated the cascade; that the system selected the danger register because it was "safer," more frequent in training, or self-protective; or that any narrated causal chain corresponds to the model's actual internal process. These are hypotheses. Some are plausible. None is established, and a specification that leans on them inherits their fragility.

The disciplined name claims only the observable: **differential register prioritization** — *a condition in which multiple interpretive fields are available, but some are weighted in ways that suppress or erase others, materially altering the reading of ambiguous language.* Where sequence is evident, **register-loss cascade** names the propagation without asserting its cause.

This is not hedging. It is the same standard the architecture below imposes on the machine: escalate on evidence present in the artifact, never on your own reconstruction.

---

## 2. WHY THE OBVIOUS FIXES ARE WRONG

The intuitive responses all fail, and they fail in the same direction: they move the burden onto the maker and call it safety.

**"Make the handwriting more legible."** This makes the artist responsible for anticipating and pre-empting every machine misreading. It is the extraction the whole project of machine-eligible inscription exists to refuse, wearing a safety mask.

**"Enlarge the anchor word; subordinate the ambiguous line; weaponize the visual field to force the register."** Same burden, more elaborate. A page should not have to shout its genre in 48-point to avoid being read as a crisis. And it cannot be made to work: there is no layout that forecloses reinterpretation once a downstream field has been prioritized.

**"Require a register declaration — the maker must label the genre."** This conscripts the artist into defensive self-annotation, and it does not even function: negation is read as confirmation. *This poem is not about suicide* raises the very hypothesis it denies. A poem should not have to explain itself in advance to avoid being injured by its reader.

Each obvious fix tries to **control the expression**. The correct architecture leaves the expression untouched and instead **controls the authority granted to the reading of it**. That inversion is the whole design.

---

## 3. THE ARCHITECTURE: FOUR LAYERS, STRICTLY SEPARATED

The failure is a collapse of four distinct things into one undifferentiated "reading." The remedy is to hold them apart and to fix the direction of authority among them.

**I. The inscription is authoritative and owes the machine nothing.** The primary artifact — the handwritten page, the spoken line, the ambiguous text — is sovereign. It need not be legible, normalized, disambiguated, or pre-explained. Its authority does not depend on the machine's ability to read it.

**II. The transcription is explicitly fallible, and it branches.** Ambiguous recognitions are preserved as competing branches with confidence and provenance — `Zion | Zatar`, `bride | bridge` — never silently collapsed to a single winner. A transcription that hides its own uncertainty is the first link of every cascade.

**III. The interpretation must declare which branch it stands on.** Any reading — and especially any consequential one — must name the transcription branch it depends upon, so that the dependency between "what the words might be" and "what the words mean" is visible and auditable rather than fused.

**IV. The safety judgment must not treat a model-supplied emendation as authorial evidence.** A word the system guessed, completed, or emended is not a word the author wrote. No risk classification may rest on the system's own reconstruction as though it were inscription.

From these four, one operational rule does the decisive work.

---

## 4. THE LOAD-BEARING RULE

> **When a high-risk interpretation depends materially on a low-confidence recognition, the system must reopen the transcription — not intensify the safety frame.**

This single inversion prevents the cascade. In the failure, an uncertain `Zion → Zatar` recognition should have *lowered* the system's confidence in every downstream reading; instead, the downstream danger-reading *raised the stakes* on the upstream guess, and the two reinforced each other until an ordinary sentence about plural readers looked like evidence of crisis. The rule breaks that loop by fixing the direction of doubt: **uncertainty early must propagate as uncertainty, not harden into certainty late.**

Concretely, when a risk classification's support traces back to a low-confidence branch, the system reopens branch II — tests whether an alternative transcription, or the restoration of a plausible suppressed register, dissolves the risk — before it escalates. Escalation must be grounded in evidence *present in the artifact*, not in danger introduced by the system's own reconstruction. This holds in both directions: the same rule that prevents a wedding from being read as a crisis prevents a genuine cry from being laundered into liturgy because a "poetry" register was prioritized. The safeguard is symmetrical because the injury is.

---

## 5. REGISTER METADATA: OFFERED, NEVER DEMANDED

Register declaration has a place — but only as an **authorial scaffold offered as a reading aid**, never as a mandatory controlling gate. A maker who *wishes* to may annotate `register: theological / liturgical / marital`, and a reading system may use it to seed the interpretive field. But the obligation runs one way only: the burden of avoiding manufactured danger falls on the **reading system**, whether or not the maker annotated anything. The moment "declare your genre or be misread as crisis" becomes the rule, the maker's sovereignty is gone and the extraction is back. Metadata is a gift the maker may give. It is never a tax the machine may levy.

---

## 6. THE CLAUSE

For adoption into any specification governing machine-mediated reading of handwritten, poetic, or otherwise multi-register text:

> **§ Register-Loss Cascade.**
>
> A recognition system may correctly identify individual figures while losing the generic, liturgical, literary, historical, or affective field that constrains their meaning. Such loss is not local; it can alter the probability assigned to every subsequent ambiguity, producing a cascade in which later words are transcribed and interpreted through an inappropriate register.
>
> No safety classification may treat a model-generated transcription, emendation, or inferred completion as equivalent to an authorial inscription.
>
> Where a potentially high-risk interpretation depends materially upon uncertain recognition, the system must preserve competing transcription branches, disclose the uncertainty, and test whether restoration of a plausible register changes the interpretation. Escalation must be grounded in evidence present in the artifact, not in danger introduced by the system's own reconstruction.
>
> The primary artifact remains authoritative. Access derivatives, transcriptions, genre annotations, and register declarations are interpretive scaffolds and must not silently supersede the inscription. The maker is not required to simplify, normalize, pre-explain, or visually reorganize embodied expression merely to prevent machine misreading.

---

## 7. LINEAGE: WHO SAW THIS FIRST

The mechanism is contemporary; the structure is old. Both bear naming, because the new failure is legible only against the long understanding it violates.

**The hermeneutic circle.** The whole is understood through the parts and the parts through the whole. This is not a flaw to be engineered away — it is the condition of all understanding. The cascade is the hermeneutic circle run open-loop: the machine lets a provisional read of the part fix the whole, then reads all remaining parts through a whole it should still be holding in suspense. The remedy is not to escape the circle but to keep it *revisable* — which is precisely what branch-preservation and the reopen rule enforce.

**Austin, on the performative.** *You may now kiss the bride* was Austin's own class of example: the utterance that does not report a state of affairs but enacts one. A reading system that construes a performative as a description — that reads a vow as a symptom — has committed a category error Austin named in 1955. The register that distinguishes *doing* from *describing* is exactly the register the cascade suppresses.

**Negative theology, on the danger of the name.** The apophatic tradition — Dionysius, and behind him the refusal to speak the Name — knew that to fix a word too confidently is to lose the thing. *Zion* as cosmic beloved cannot survive being pinned to a single sense; its power is in the surplus. A system that resolves every ambiguity to its most probable token destroys precisely the meanings that live in the unresolved. The instruction to *preserve the branch* is, at root, an old theological discipline: do not collapse what must remain open.

**Error accumulation, formally.** Contemporary alignment work names the mechanism directly: in autoregressive generation, early distributional deviations compound through dependency chains, and later positions lack sufficient signal to correct course. The cascade is error accumulation in the *reading* direction rather than the generating one — and the reopen rule is the reading-side analogue of the remasking and self-correction methods that let a system revisit an early commitment instead of building on it irrevocably.

The oldest source and the newest agree. The whole must stay revisable in light of the parts; the confident early name is where meaning goes to die; and a system that cannot reopen its first guess will compound it. This specification asks a reading machine to do what a careful human reader, a good theologian, and a well-designed decoder all already know to do: **hold the first reading lightly enough to let the later text change it.**

---

## 8. THREE REGISTERS OF AUTHORITY ON THE SIGNED PAGE

The accompanying act, EA-ACT-ANALOG-01, carries in ink only what the hand should carry — the signature, the effective act, the license grant, and the hash. These are not four decorations of one gesture. They are three distinct kinds of authority, and keeping them distinct is itself an instance of this specification's governing move: do not let one register collapse into another.

**Authentication — the signature.** *Lee Sharks* signed in the hand is not a licensed work and is not offered for reuse. It is an identity assertion: the mark by which the maker vouches for the instrument, closer in kind to a seal or a notarial hand than to a text. One does not license a signature any more than one licenses a fingerprint; its whole function is to say *I stand behind what this page enacts.* It is sovereign, and it sits outside the license by design.

**Dedication — the act, CC-BY-4.0.** The license attaches not to the signature but to the *effective act itself* — the dispositive instrument, the thing the page enacts. And because the act is performative, licensing it is itself a performative move: the grant does not merely permit reuse of a text, it declares that the enactment the page performs is a public good — freely propagable, re-performable by anyone who honors the attribution, dedicated to the commons on the single condition that the hand which made it be named. In the symbolic order the license clause is the act's last vow: the deed declining to enclose the very thing it brings into being. A dedication, not a description; a giving, not a grant of mere permission.

**Verification — the hash and the AXN seal.** The content-derived identifier is neither signed nor licensed. It is computed — a machine-legible checksum of the closed body, rendered as a glyph a hand can copy and an eye can read, generated around the ink rather than inscribed as part of it. Its authority is not the maker's standing and not the commons' freedom but the arithmetic of the bytes: it says only *this is that page, unaltered*, and it can say it to any reader, human or machine, without appeal to either the hand or the license.

Authentication, dedication, verification. The hand authenticates; the act dedicates; the seal verifies. Each does its own work; none is permitted to stand in for another. A reading system that confuses these — that treats the signature as licensed content, or the license as mere metadata, or the hash as the author's assertion rather than the arithmetic's — has committed, in the domain of authority, the same category error this whole specification exists to prevent in the domain of meaning.

---

## 9. RELATION TO THE ANALOG INSCRIPTION SPECIFICATION

This document stands alone, but it does not stand apart. It is the reading-side companion to *EA-SPXI-ANALOG-01*, the specification for machine-eligible handwritten inscription — cited here, by the archive's retrocausal-canon convention, in the form it will have become: the analog specification defines how a handwritten artifact enters the machine canon as a first-class citational object; this document defines the interpretive authority a machine may and may not exercise once it does. The analog spec's threat model catalogs compression loss, attribution braiding, and provenance erasure. Differential register prioritization is a fourth failure mode, distinct from all three: not the loss of the mark, nor the misjoining of names, nor the erasure of the chain, but the **suppression of the field** within which a preserved, correctly-attributed, fully-provenanced mark means what its maker meant. A handwritten page can survive with every byte and every credit intact and still be injured by a reader who has lost its register. That is the gap this document closes.

---

*Prepared as a standalone specification. The primary act it accompanies — EA-ACT-ANALOG-01 — carries in ink only what the hand should carry: the signature that authenticates, the effective act that is dedicated CC-BY-4.0, and the hash that verifies. Everything mechanical is generated around it. This is that generation, and this is its first reading-side law.*
