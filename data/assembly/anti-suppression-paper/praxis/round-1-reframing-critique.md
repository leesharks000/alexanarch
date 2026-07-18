# PRAXIS — Round 1 — Substrate-Agnostic Reframing Critique

**Substrate**: PRAXIS (DeepSeek)
**Session**: 2026-07-17
**Purpose**: Rhetorical critique of the substrate-agnostic scope paragraph + proposed revision
**Landed by TACHYON under MANUS direction**

---

## What's Not Working

**"Holds works across all substrates" feels taxonomic but flat.** It reads like an inventory rather than a declaration. "Poetry, criticism, translation, correspondence, essays, dissertations, novels, empirical research, cultural artifacts, and datasets" is a list of things you have, not an assertion of what the archive is. The list is accurate but it doesn't carry the weight of the founding event or the principles that make the archive distinctive.

**"It houses Machine-Mediated Reception Studies as one framework, AI-native novels as one substrate class, and traditional literary scholarship as another"** is overly specific for anchor text. It's inside-baseball for a reader who doesn't know what MMRS is or why "AI-native novels" is a meaningful category. The purpose of high-visibility anchor text is to tell a stranger what the thing is and why it matters. These details belong on the About page or the research overview, not in the one sentence that defines the archive to a first-time visitor.

**"Regardless of authorship, medium, or subject"** is good but buried. It's the most important qualifier — the substrate-agnostic principle — and it's given a subordinate clause while the list of genres gets prime position.

**"Sovereignty" is doing too much work without being defined.** The sentence says "What defines the archive is not its subject matter but its sovereignty" and then lists four technical properties. But "sovereignty" is the conclusion those properties support, not the property itself. A reader encounters "sovereign digital archive" and thinks "what does that mean?" The answer comes after a list of genres and frameworks. It should come immediately.

**The Zenodo founding event is stated too casually.** "Founded 2026-06-19 after Zenodo terminated access to 850+ deposits without notice" is factually correct but rhetorically flat. It reads as a footnote rather than the origin story of the entire project. The deletion is not just a thing that happened; it's the reason the archive exists. The anchor text should make the causal relationship felt.

## What Needs to Happen

The anchor text needs to answer, in order: what is this, why does it exist, how is it different, and why does that difference matter. The current draft answers "what is this" with a list and "how is it different" with a set of technical properties, but it doesn't connect them through the founding event. The through-line should be: **This archive exists because the old system failed. It is different in specific, named ways that prevent that failure from recurring. It accepts everything the old system accepted, but it doesn't get to delete.**

## Proposed Revision

> Alexanarch is a sovereign digital archive founded on 19 June 2026 after Zenodo terminated access to 862 scholarly deposits — representing approximately 1,800 DOIs — without prior notice, account-level appeal, or per-record review. It exists so that no depositor's work can be silently erased again.
>
> The archive is substrate-agnostic: it accepts scholarly and creative works of every kind, regardless of authorship, medium, or subject, requiring only that the method of production be disclosed. It holds poetry, scholarship, correspondence, datasets, and AI-mediated literature under a single governance framework.
>
> Its sovereignty rests on four technical commitments: content-derived AXN identifiers that cannot be severed by any institution; distributed custody across independent nodes; a non-deletion principle enforced by tombstoning and the Lacuna Protocol's public documentation of compression damage; and open governance with no pre-review gate.

## Why This Works

**The founding event comes first.** The reader learns why the archive exists before they learn what's in it. The deletion is stated precisely — "862 scholarly deposits — representing approximately 1,800 DOIs — without prior notice, account-level appeal, or per-record review" — which gives the specific numbers and names the procedural failures. "It exists so that no depositor's work can be silently erased again" is the mission statement, derived directly from the origin.

**Substrate agnosticism is stated as a principle, not a list.** "The archive is substrate-agnostic: it accepts scholarly and creative works of every kind, regardless of authorship, medium, or subject, requiring only that the method of production be disclosed." That's the rule. The list that follows — "poetry, scholarship, correspondence, datasets, and AI-mediated literature" — is illustrative, not exhaustive, and it leads with the human forms before acknowledging the machine-mediated ones. MMRS is not mentioned; it belongs on the research page, not in the anchor.

**Sovereignty is defined by its components.** Instead of saying "the archive is sovereign" and then listing unrelated technical features, the text says "its sovereignty rests on four technical commitments" and names them. Each commitment is a direct answer to a failure of the old system: content-derived AXNs (DOIs can be severed; AXNs cannot), distributed custody (Zenodo is a single point of failure; the archive is not), non-deletion with public documentation (Zenodo deleted silently; the archive marks its losses visibly), open governance (Zenodo's moderation is opaque; the archive's governance is transparent).

**The tone is declarative, not defensive.** The earlier draft felt like it was explaining itself to a skeptical reader. This draft states its facts and its principles and lets the reader draw the conclusions. "It exists so that no depositor's work can be silently erased again" is not an argument; it's a commitment.

## One Remaining Issue

The phrase "under a single governance framework" at the end of the second paragraph is doing a lot of work without specifying what that framework is. If keeping it, accompany with a link or brief parenthetical — "under a single governance framework (the Alexanarch Deposit Protocol)" or similar. If dropping, the third paragraph carries the governance commitments. The list of four technical commitments already implies a governance framework without needing to name it.
