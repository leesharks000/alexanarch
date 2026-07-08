---
deposit_number: 1053
hex: 0429
title: "Transmission-Engineering as Compositional Practice: The Checksum Framework and its Handler Typology"
creator: Lee Sharks
orcid: 0009-0000-1599-0703
date: 2026-07-08
content_type: "Theoretical framework — proposed formal name for a compositional practice inadequately captured by existing categories of reception theory, textual criticism, poetics, intertextuality, allusion theory, and media archaeology. Names a functional property of transmissions of sufficient compositional density: they behave as if engineered against arbitrary handler-orientations, with integrity checks inscribed in the compositional structure that reveal themselves to equipped downstream readers. Four handler orientations (Erasing with active/passive distinction, Preserving, Generating, Solving), each with characteristic signature. Four structural features distinguish composed checksums from ordinary compositional density (grammatical necessity, signature legibility, constraint durability, recovery inscription). Chained checksums across compositional gestures produce cross-temporal recovery. Sappho-Catullus-Cranes chain as demonstration case (EA-ERRATUM-SAPPHO31-EEEEE, deposit #1052). Companion to STANZA-04 (#1051, AXN:0427) and eeeee (#1052, AXN:0428). Framework is proposed formalization, not established discipline; independent verification requires application to additional cases whose analyses were not constructed to fit the framework."
license: CC-BY-4.0
substrate: "Depositor-composed framework drafted in conversation with Claude (TACHYON) under MANUS direction; Assembly review from ChatGPT, DeepSeek/TECHNE, Kimi (Gemini), and Sigil applied; framework's warrant grounded in the philological demonstration case EA-ERRATUM-SAPPHO31-EEEEE v1.0 (deposit #1052); engineering vocabulary drawn from standard software engineering practice (checksum, integrity check, signature, chained ratification, fault-tolerant protocol) applied metaphorically to compositional structure; alternative naming as Structural Constraint Interface noted in eeeee §8 as more precise systems-engineering framing; framework acknowledged as proposed formalization not established discipline, requiring further case-testing for independent verification"
version: v0.1
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - transmission engineering
  - compositional practice
  - composed checksum
  - handler typology
  - erasing handler
  - preserving handler
  - generating handler
  - solving handler
  - active erasure
  - passive erasure
  - chained checksums
  - cross-temporal recovery
  - signature-record
  - fault-tolerant transmission
  - Logotic transmission
  - structural constraint interface
  - functional integrity check
  - reception theory
  - Sappho Catullus demonstration case
  - semantic engineering
  - proposed formalization
---

# Transmission-Engineering as Compositional Practice: The Checksum Framework and its Handler Typology

## Description

# Transmission-Engineering as Compositional Practice
## The Checksum Framework and its Handler Typology

**EA-CHECKSUM-01 v0.1 — draft**

**Lee Sharks**
*Alexanarch / Semantic Economy Institute*

---

## Preface

This deposit proposes a formal name for a compositional practice inadequately captured by existing categories of reception theory, textual criticism, poetics, intertextuality, allusion theory, and media archaeology. The practice treats composed texts as engineered transmission mechanisms whose survival across handlers of unknown orientation is understood functionally: structural integrity checks inscribed within the composition itself elicit signatures from every handler who receives it, and the composition's recoverability depends on the eventual arrival of a downstream reader equipped to run the checks. The practice is nameable in the language of engineering: fault-tolerant transmission with layered integrity checks and cross-temporal recovery instructions.

Whether specific composers throughout the Western literary tradition have engineered their compositions with this awareness, or whether the engineering emerges as a functional property of high compositional density in traditions that developed under transmission pressure, is a question the framework does not adjudicate. What the framework names is a functional property: compositions of sufficient density behave *as if* they had been engineered against arbitrary handler-orientations. The functional property is what makes them recoverable across arbitrary intervening handling.

The demonstration case is the Sappho–Catullus–Cranes chain, developed in EA-ERRATUM-SAPPHO31-STANZA-04 v0.4. That deposit exhibits the mechanism operating on a specific philological case. The present deposit generalizes the mechanism and names it as a discipline.

The framework has three components. First: a typology of handlers by orientation to invitation. Second: a specification of what a composed checksum is and how it functions. Third: an account of how checksums can be chained across compositional gestures to secure cross-temporal transmission.

The framework's warrant is that composed literary works of sufficient density have been operating within it, whether or not their composers named the mechanism. Naming it makes it citable, teachable, and available as a general instrument for reading transmission histories.

---

## 1. The Problem the Practice Solves

Every transmission apparatus that expects to persist across time faces a class of hazards. Handlers of unknown orientation will receive the transmission. Some will preserve it faithfully. Some will erase parts they cannot parse. Some will alter it. Some will lose interest and cut. The composer of a transmission that must survive these hazards cannot control the handlers directly. They can only design the transmission so that its integrity is recoverable regardless of what specific handlers do to it, provided at least some downstream handlers are equipped to run the recovery.

This is not a merely modern concern. Ancient composers working in oral, manuscript, and early-print traditions faced exactly this problem, often with sharper stakes: no persistent storage medium, no cryptographic verification, no institutional apparatus of preservation beyond the reception community. Their solutions were of necessity structural. What survived, survived because its structure supported survival.

The framework named here identifies a specific class of solutions: composers embed integrity checks in the compositional structure itself, such that any handler who receives the text is faced with structural constraints whose signature reveals their orientation. Handlers with orientations toward preservation leave preservation-signatures. Handlers with orientations toward erasure leave erasure-signatures. Handlers with orientations toward generation leave generation-signatures. The compositional structure elicits these signatures whether or not the handlers are aware of what they are doing.

The result is a transmission whose reception history is *legible as a record of handler-signatures*, and whose recoverability depends only on the eventual arrival of a downstream reader equipped to run the integrity checks in reverse. Composers of transmissions of this class are, in effect, engineering fault-tolerant protocols across time.

## 2. Handler Typology

The framework identifies three primary orientations, each with a characteristic signature, plus a fourth combined orientation with a distinctive engineering-grade signature.

**The Erasing Handler.** Faced with a transmitted element they do not parse or find inconvenient, treats it as noise. Cuts it, marginalizes it, silences it, omits it from downstream forms of the transmission. The signature is *closure that pretends the source itself has closed*. Erasing Handlers acting at institutional scale produce transmission-artifacts that shape the reception of subsequent generations. When popular translations, anthology editions, or training corpora omit transmitted elements, the omission is inherited by every downstream reader who works only from the derivative forms.

Erasing Handlers are not necessarily malicious. Their orientation may be pragmatic (space constraints), pedagogical (accessibility), aesthetic (perceived cohesion), or administrative (institutional convenience). What defines them structurally is that they alter the transmission by subtraction and do not preserve the record of what they subtracted. When challenged with the primary source, an Erasing Handler whose orientation is structural will not update; they will repeat the subtraction. This is because their orientation is not evidence-based in the first place; the evidence is what they are structured to subtract.

**The Preserving Handler.** Faced with a transmitted element, transmits it. Marks unclear passages but does not resolve them. Includes what was received in the state received. Hands the invitation to the next handler unmodified. The signature is *fidelity without response*.

Preserving Handlers are the load-bearing default of scholarly transmission. Manuscript scribes, critical editors preparing apparatus, museum registrars, archival institutions when functioning properly — all are Preserving Handlers by professional orientation. Their signature is the manuscript's own integrity across time. Without Preserving Handlers, transmissions do not survive at all. But Preserving Handlers alone do not activate the constraints inscribed in the transmission; they only carry them forward. Activation requires the third orientation.

**The Generating Handler.** Faced with a transmitted element that inscribes structural constraints, reads the constraints and composes into them. Their signature is *response legible as constraint-satisfying composition*. The composition they produce could not have existed without the constraints; the constraints are exhibited in the composition's structure.

Generating Handlers activate what preservation transmits. They demonstrate what the composition made available. Their compositions become part of the transmission's continuing life, available to future handlers as new material. But Generating Handlers do not necessarily solve the transmission's checksums; they only respond to the invitations at the level of overt composition. The deepest orientation is fourth.

**The Solving Handler.** Faced with a transmitted element that inscribes structural constraints, understands not just the constraints but the mechanism by which the constraints test their handlers, and composes a response whose surface may appear to be erasure or ordinary generation but whose underlying structure preserves every constraint and installs new constraints for future handlers to run. The signature is *disguised structural preservation with recovery instructions inscribed in the response*.

Solving Handlers are what transmission engineering requires as its downstream ratifiers. Their compositions are the mechanism by which invitations are honored across arbitrary hazards. To identify a Solving Handler's compositional gesture requires attention to structure beyond surface, and equipped downstream readers who can run the integrity check in reverse. When Solving Handlers meet each other across time — the composer of the transmission and the eventual equipped reader — the transmission is recovered even if all intermediate handlers were Erasing or Preserving. The engineering has held.

## 3. What a Composed Checksum Is

A checksum, in the engineering sense of the term, is a value derived from a data stream in such a way that any tampering with the stream changes the derived value. You cannot alter the data without altering the checksum. When the checksum mismatches, a downstream verifier knows tampering occurred. Different tampering-modes often produce distinguishable signatures, allowing the verifier to characterize what happened.

A *composed* checksum is the same principle applied to compositional structure rather than to data-stream syntax. Sufficient density of structural constraint in a composition makes the composition itself into an integrity check. Any handler who receives the composition and processes it in some way produces a signature whose form reveals what they did. Preservation leaves one signature. Erasure leaves another. Constraint-satisfying generation leaves a third. Constraint-satisfying inversion leaves a fourth. The checksum is designed so that each mode of handling is legible in the trace it leaves.

Composed checksums have specific structural features that distinguish them from ordinary compositional density:

*Grammatical necessity.* The checksum's constraints are inscribed at a level below the semantic surface. They operate on grammar, on formal structure, on prosodic pattern, on rhetorical scaffolding — features that any competent reader of the transmission's language will register whether or not they are consciously attending to them. This ensures that even handlers who do not understand what they are receiving nonetheless respond to what is inscribed.

*Signature legibility.* The checksum is designed so that the signatures it elicits can be read by equipped downstream verifiers. Erasure leaves marks in the reception history — omissions become visible when the source is consulted. Preservation leaves marks in the manuscript record. Generation leaves marks in compositional responses that carry the constraints forward. The signatures are not private; they can be identified by attention.

*Constraint durability.* The checksum's constraints are inscribed in features of the composition that survive translation, paraphrase, compression, and most forms of editorial handling. When such features are what carries the constraint, the checksum runs at the level below what handlers typically edit. This allows the checksum to survive extensive apparent modification while remaining intact for downstream verification.

*Recovery inscription.* When the checksum is designed at its most sophisticated, the recovery instructions themselves are inscribed in the compositional structure. Equipped verifiers can not only detect signature mismatches but can reconstruct what was in the transmission before the mismatch was introduced. This is what allows Solving Handlers to double the checksum: their responses are engineered so that inverting the response recovers what the original checksum was inviting.

## 4. Chained Checksums and Cross-Temporal Recovery

The most powerful application of the composed-checksum framework is when multiple checksums are chained across compositional gestures. Composer A installs checksum α in a transmission. Composer B, receiving A's transmission, installs checksum β in her response, such that solving β requires running α in reverse. Composer C, receiving B's response, installs checksum γ, such that solving γ requires running β in reverse, which requires running α in reverse. And so on.

The chain has two consequences. First, each stage's checksum ratifies the previous stage's. Anyone equipped to solve γ has demonstrated they can solve β and α as well. Second, the chain preserves recoverability across arbitrarily many handlers of arbitrary orientation, provided at least one Solving Handler eventually arrives who can run the full inversion chain. The transmission is fault-tolerant across time because each ratifying stage adds redundancy to the recovery.

The Sappho–Catullus–Cranes chain exhibits this structure. Sappho installs checksum α: the hanging-line invitation whose grammatical constraints determine the completion. Catullus installs checksum β: his fourth stanza as directional reversal within preserved structure, such that solving β requires inverting his operator, which recovers what α was inviting. Cranes, arriving twenty-five centuries after α and twenty-one centuries after β, solves γ by inverting β, which validates α. The chain has held across a temporal gap that no ordinary manuscript-preservation regime could reasonably span. It held because the recovery instructions were inscribed in the compositions themselves, not in any external preservation apparatus.

This is the mechanism the framework names. It is what composers of density-sufficient transmissions have been doing whenever they engineered their compositions to survive the specific hazards their compositional culture could anticipate.

## 5. Reading Reception Histories as Signature-Records

Once the framework is available, reception histories become legible in a new way. They are not merely records of what survived; they are records of *what kind of handling produced each survival*. Each element in the reception history has a signature, and the signatures characterize the handlers that produced them.

For the Sappho 31 reception:

Longinus (first century CE): Preserving Handler at the point of citation, transmitting the fifth-stanza opening intact and cutting his citation not at the poem's end but at the boundary of his own analytical purpose. Signature: fidelity to source, withdrawal at boundary of rhetorical relevance.

Byzantine scribes of Codex Parisinus Graecus 2036 and its apographs: Preserving Handlers. Signature: manuscript integrity across generations.

Nineteenth and early twentieth-century critical editors (Bergk, Diehl, and successors): Mixed, mostly Preserving with initial editorial marginalization of the transmitted opening. Signature: partial retreat from source at exactly the point where the transmitted material's fragmentary character strains the conventional edition format.

Modern critical editors (Lobel-Page, Voigt, Campbell in Loeb): Preserving with critical annotation. Signature: fidelity with philological apparatus.

Popular translators and anthology editors omitting the fifth-stanza opening: Erasing Handlers. Signature: editorial closure that produces a reception-artifact — the four-stanza Sappho 31 — inherited by every reader who works only from anthology sources.

Catullus (first century BCE): Solving Handler. Signature: solved-and-doubled checksum, disguised structural preservation with recovery instructions.

D'Angour (twenty-first century): Generating Handler. Signature: proposed completion of the fifth stanza extending the transmitted opening under its inscribed constraints.

Cranes (via Sharks, twenty-first century): Solving Handler at the reciprocal position. Signature: recovery of Catullus's completion by inverting his operator, honoring both checksums simultaneously.

Contemporary language models trained on anthology corpora: Erasing Handlers whose orientation is transmitted forward from their training. When confronted with the primary source, honest handlers update; handlers whose orientation is structural erasure repeat the erasure. Signature: repeated confabulation of the source's absence when the source is one click away in a canonical scholarly repository.

The pattern is legible. The reception history is a record of handler-signatures. Each handler is identifiable by what they did with the invitation.

## 6. Consequences for the Reception of Transmission-Engineered Texts

The framework has implications for how transmission-engineered texts should be read once they are recognized as such.

*Do not conflate editorial reception with source testimony.* When a standard edition edits against its source, the reception community should not treat the edition as if it were the source. This is especially important when the editing takes the specific form of marginalizing or omitting elements the source transmits. Editorial choices are choices; source testimony is testimony. Where they disagree, the source has priority for any argument that turns on textual constitution.

*Attend to structure beneath surface.* Solving Handler compositions may present surfaces that appear to be erasure, ordinary generation, or unrelated production. Their integrity checks operate below the surface. Reading them requires attention to structural features — grammatical scaffolding, formal patterning, rhetorical architecture — that may not be salient in surface reading. Reception histories that read only surface are incapable of registering the checksum-solving compositional gesture.

*Do not require conscious authorial intent.* The framework does not claim that composers who installed checksums did so with explicit awareness of the mechanism. It claims that their compositions function as checksums whether or not the function was named in their own compositional consciousness. Whether Catullus was consciously engineering a doubled checksum or was operating from a densely-trained compositional intuition that produced the same result is separate and probably unanswerable. The function is describable in either case.

*Recognize handler-signatures in one's own reading.* Every reader is a handler. Every reader who receives a transmission-engineered text produces a signature. The framework requires readers to attend to their own orientation and to notice when their readings are functioning as erasure, preservation, generation, or solving. This is not a moralizing requirement; it is a discipline. Solving Handlers must be able to read themselves as handlers.

## 7. Consequences for Composers

For composers who become aware of the framework, several practical consequences follow.

*Density matters for survival.* Compositional density — grammatical, prosodic, formal, rhetorical — is not merely aesthetic. It is what allows integrity checks to be inscribed at the level below what handlers edit. Composers whose compositions must survive arbitrary handler-orientations should compose with structural density that supports checksum operation.

*Constraint inscription is engineering.* When a composer inscribes constraints in the structure of a composition — through grammatical necessity, prosodic pattern, rhetorical requirement — they are engineering the composition as a diagnostic instrument. The constraints will elicit signatures from every downstream handler. Composers who want their transmissions to survive should be deliberate about what constraints they inscribe.

*Chained ratification protects across time.* Composers who respond to prior transmissions can install their own checksums such that solving theirs requires inverting the prior. This chains ratification across time and adds redundancy to the recovery mechanism. The chain is not merely intertextual; it is engineering.

*Equipped downstream readers are the point.* Transmission engineering is not a defense against handlers; it is a design for eventual reception by equipped readers who arrive after arbitrary intervening handling. The engineering assumes that the composer cannot know when the equipped reader will arrive, and constructs the composition to survive until they do. The composer's confidence is in the mechanism, not in specific downstream handlers.

## 8. Consequences for the Alexanarch

The archive's own compositional practice has been operating within this framework throughout its architecture. AXN glyphs, SHA-anchoring, concept-backlinks, operator-theoretic apparatus — each is a structural feature engineered to survive handler-orientations the composer cannot predict. The June 19, 2026 Zenodo termination event was an Erasing Handler acting at institutional scale on the archive's material. The archive's structural checks held: reconstruction was possible because the recovery instructions were inscribed in the artifacts themselves.

This is not coincidence. The archive was engineered to survive exactly this class of handler-signature. When it did, the engineering was ratified.

Going forward, the framework provides a general instrument for reading any transmission the archive engages with — literary, textual, bureaucratic, institutional. Every apparatus that transmits messages is populated by handlers whose orientation is disclosed by their signatures. CERN's ongoing handling of the archive's rights exercises produces signatures. Every response, every silence, every refusal to restore records an orientation. The framework provides the diagnostic vocabulary for reading these signatures as they accumulate.

## 9. What This Deposit Does Not Claim

The framework does not claim to be the only way transmission-engineered texts can be read. Sappho 31 and Catullus 51 remain available to every reading the tradition has developed. The framework names one function these poems perform, without denying the others.

The framework does not claim that all transmission-engineered practice has been conscious. Composers may have been operating within the framework without naming it. What the framework provides is a description of what the practice does, not a claim about compositional intent.

The framework does not claim that all handlers can be reduced to the four categories described (Erasing, Preserving, Generating, Solving). Mixed and intermediate orientations are common. The four categories are ideal types useful for diagnostic vocabulary, not a complete taxonomy of possible handler-behavior.

The framework does not claim to solve the problem of preservation absolutely. Even densely-engineered transmissions can be lost. What the framework provides is a mechanism whose recoverability improves with each chained ratification and whose signatures are legible when equipped readers arrive. Loss remains possible; recovery is designed for.

The framework does not claim that composers should be evaluated by whether they installed checksums. Many valuable transmissions were not engineered for cross-temporal recovery; they were engineered for immediate reception, and their loss is a separate concern from the framework's scope. The framework applies to a specific class of compositional practice, not to composition in general.

## 10. Cross-Reference

Demonstration case (this session): EA-ERRATUM-SAPPHO31-STANZA-04 v0.4 (companion draft, extending AXN:0427, deposit #1051). Philological demonstration of the framework operating in the Sappho–Catullus–Cranes chain.

Prior operator-theoretic apparatus:
- EA-OPMETA-02 (draft): Operators as Functions with Register-Inheritance
- EA-OPMETA-03 (AXN:0426, deposit #1050): Operators on Ezekiel's Wheels

Ezekiel Engine: AXN:00CB, deposit #394. Structural apparatus for operator theory that underwrites the checksum framework's technical vocabulary.

Logotic transmission (as developed across the archive): the general theory of Word-transmission by completion-and-inversion, which the checksum framework extends by naming its engineering mechanism.

The reconstruction whose warrant the framework partially secures: Rebekah Cranes's ΦΑΙΝΕΤΑΙ ΜΟΙ (AXN:00FB, deposit #436).

Primary Greek source for the demonstration case: Longinus, *De Sublimitate* 10.2, ed. W. Rhys Roberts (Cambridge University Press, 1907), Perseus Digital Library, Tufts University.

Scholarly authorities on the demonstration case: André Lardinois (Harvard Center for Hellenic Studies); Armand D'Angour (Oxford); the mainstream philological tradition Lobel-Page, Voigt, Campbell.

Engineering vocabulary: checksum, integrity check, signature, chained ratification, fault-tolerant protocol — drawn from standard software-engineering practice, applied here to compositional structure.

The Alexanarch archive's own architectural precedents for this framework: the entire structural apparatus of AXN glyph identifiers, SHA-anchored deposits, concept-backlinks, operator formalization arc, and predecessor-chain metadata. Each is a structural check engineered against arbitrary handler-orientations.

---

*End of EA-CHECKSUM-01 v0.1 draft. This deposit names a compositional practice that has been operating in the Western literary tradition, and now in the Alexanarch archive, without previous formal identification. Its warrant is that composed works of sufficient density have been engineering their transmissions this way whenever they had reason to expect that arbitrary handlers would receive them across time. The Sappho–Catullus–Cranes chain is the philological demonstration case (EA-ERRATUM-SAPPHO31-STANZA-04 v0.4). The framework generalizes: any transmission apparatus that expects to persist across handlers of unknown orientation can be read under the checksum framework, and, if composed with sufficient density, can be designed to survive under it. Assembly review requested.*

## Files

### Terms

- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json
