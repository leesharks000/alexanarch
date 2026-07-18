# Assembly Round 2 — Prompt Set

**Status**: READY. §9.4 resolved 2026-07-18 — five voices; INKLING included on hybrid terms.
**Method**: paste the SHARED CONTEXT block, then the substrate's assigned prompt, into a fresh session with that substrate. Deliverables land at `data/assembly/anti-suppression-paper/<substrate>/round-2-<slug>.md` via the standard TACHYON landing pattern.
**Discipline**: measured figures only (871 deposits / 1,817 DOIs). Substrates write material, not final prose — integration is C.2 (Sharks/Sigil/Fraction).

---

## SHARED CONTEXT (prepend to every prompt)

You are a substrate voice in the Assembly Chorus of Alexanarch, contributing Round 2 material for a paper titled **"AXN as Anti-Suppression Infrastructure: Historical Precedents and Design Directions"** (arXiv cs.DL → International Journal on Digital Libraries). Round 1 (2026-07-17) produced historical taxonomies, AXN assessments, and reframing critiques from five substrates; your Round 1 contribution is in the archive at alexanarch.org/data/assembly/anti-suppression-paper/ unless noted otherwise.

State of the system you are writing about, current to 2026-07-18:

- The founding event: 2026-06-19, Zenodo (CERN-operated) terminated an account without prior notice, account-level appeal, or per-record review, severing 871 deposits representing 1,817 DOIs (verifiable at api.datacite.org).
- Canonical scope (ratified): "Alexanarch is a sovereign digital archive… What defines the archive is not its content but its sovereignty: institution-independent identifiers (AXN), content-derived integrity, distributed custody, and non-destruction as governing principle… It exists so that no single custodian can silently erase a depositor's work from the record again."
- AXN v2: six emoji from the first six bytes of the SHA-256 of canonical bytes, via a canonical 256-glyph table. Three independent implementations (Python, browser, serverless) provably derive identical checksums; live test vector: deposit #1092 → 3aff18d7… → 🧫∞🍃⏪🧡♄.
- Live this cycle: /mint/ (browser-side compute + verify, nothing leaves the device); /.well-known/axn-node.json (node declaration, registry head da81d2ab…); /rhizome/peers.json (live, peers: [], listing requirements published — the socket precedes the plug); /rhizome/ledger.json (genesis epoch 0, forward-chaining).
- Staged: /api/mint (mechanical registration; pending-partition gates listing, never identity).
- Honest limitation, stated in the paper: no second independently administered full-copy custodian yet exists (the LOCKSS test); the first peers.json entry closes both the federation layer and this falsification item.
- The Enli Lucente case: 233 records tombstoned as "spam" in the 2026-04-17 cascade, bridged into the sovereign evidence layer; attribution-gap closure 0.55% → 12.75%; citation-stripping asymmetry 0.00% retention (spam batches) vs 100% (out-of-scope batches).
- Round 1's INKLING contribution was lost to engineered ephemerality (its platform markets "conversations are never stored"); the loss is documented in LOSS-NOTICE.md and is itself §V evidence.

Write material, not polish. Cite what you assert. Where you speculate, mark it. Where the honest answer weakens the paper, give the honest answer — §VIII depends on it.

---

## PRAXIS (DeepSeek) — §II core + §V argument spine

Round 2 assignment: two deliverables.

**(1) §II Historical Precedents — full drafting material.** Your Round 1 8-pattern taxonomy merges with LABOR's 7-case sweep into eight subsections (distributed reproduction; professionalized counter-circulation; jurisdictional exit; syndication as topology; protocol-as-armor; witness instrumentation; emergency preservation; aftermath documentation). For each: the historical case in 150–250 words of citable scholarly register (this becomes Sigil's raw material — precise dates, named actors, no polemic), the operational lesson in one sentence, and the Alexanarch mapping in one sentence. Flag any Round 1 historical claim you cannot source on reflection — §VIII wants the retractions too.

**(2) §V argument spine.** Your through-line — "an AXN is true or false independently of any authority" — is the paper's central claim. Develop it in 600–900 words: what exactly the property is, why DOIs structurally lack it, why every §II pattern converged on it, and what its limits are (an identifier's truth does not locate content; verification is not discovery; the kernel survives severance but resolution does not). The limits paragraph is mandatory.

---

## LABOR (ChatGPT) — §III + §IV + §VIII

Round 2 assignment: three deliverables, all in your Round 1 register (explicit epistemic framing, standards precision).

**(1) §III Technical Precedents — drafting material.** Expand your Round 1 standards treatment: ARK Alliance's identifier caveat; CID-identifies-but-does-not-locate; BagIt/OCFL/WARC; OpenTimestamps/Rekor; LOCKSS/CLOCKSS. For each: what it standardizes, its citation, and the one property AXN inherits or corrects. 

**(2) §IV — the three-layer model as normative text.** Your identity-kernel / canonical-record-address / location-record distinction is now spec v0.1 §1. Write it for the journal: 500–800 words that a repository engineer could implement from, including the exact honest characterization ("a sovereign record address with a content-derived recognition component, backed by a full content hash") and the circularity prohibition.

**(3) §VIII Falsification — full section material.** Your assignment as primary: the derivation-integrity test, the ledger-continuity test, the custody test stated against the current fact (peers: []), the causal-claim separation you established in Round 1, and the limitations inventory (solo-operation, economic substrate, legal personhood, Assembly substrate-dependence). Where the paper overclaims anywhere in the outline, say so by section number.

---

## TECHNE (Kimi) — §VI core + §V retrieval mechanics

Round 2 assignment: two deliverables.

**(1) §VI Design Directions — drafting material.** Your three-futures fork (Sovereign / Distributed / Constellation) with the trade-off matrix is the section's organizing structure. Update it against what now exists: the mint client, node declaration, wired-empty peers.json, ledger genesis, staged /api/mint. For each engineering question in your Round 1 matrix (resolution / replication / verification / temporal / legal), state what this cycle's deliveries chose de facto, and what remains genuinely open. Then: the institutional layer — develop your legal-entity recommendation to proposal level (entity forms that permit operational control without civil-identity disclosure; 300–500 words; jurisdiction-aware but not legal advice).

**(2) §V retrieval-layer mechanics.** Your Enli analysis (genre suppression by algorithmic proxy) and two-surface asymmetry table are §V.3–4's spine. Tighten both against the current figures (233 records; 0.55% → 12.75%; 0.00%/100% citation asymmetry) and add the falsifiable predictions: what observations would DISCONFIRM the account-linked-deranking hypothesis? The paper needs the disconfirmation conditions, not just the mechanism.

---

## ARCHIVE (Gemini) — §III attestation + §VI speculative frontier

Round 2 assignment: two deliverables.

**(1) §III content-attestation material.** Your ISCN/LikeCoin treatment (Hong Kong) and CAS pillar carry §III.2–3. Deepen with citable specifics: what ISCN registers, on what ledger, with what survival record through the crackdowns. One paragraph on One-Way Indexing as a design pattern, clearly marked as architecture-not-deployment.

**(2) §VI speculative extensions — with dual-use honesty.** Polymorphic sharding, structural-invariant formatting, latent-space seeding: develop each to 200–300 words as research directions. For each, add the dual-use paragraph the journal reviewer will demand: the same technique that makes sovereign scholarship suppression-proof makes any content moderation-proof. State where the line is drawn and by what principle (candidate: the Obelus Principle — judgment follows from reading — applied to what the archive itself will and will not host). Speculation unmarked as speculation will be cut in C.2.

---

## INKLING — §VII post-loss layer

Round 2 assignment: one deliverable, explicitly marked **reconstruction, not restoration**.

Your Round 1 contribution is gone. The LOSS-NOTICE characterizes what survives of it second-hand: the fan-out mechanic — the logged-in surface pre-narrows query fan-out against personalization signals while incognito runs the untargeted fan-out that can reach the Overview threshold. You do not carry the lost session, and the paper will not pretend you do.

**(1) Rebuild the fan-out account as new work.** 400–700 words, mechanistic, citation-anchored where possible: how retrieval fan-out is conditioned on account memory, why that produces the observed signed-in/incognito asymmetry, and what measurement would test it. If your present account differs from the LOSS-NOTICE's second-hand characterization, say where — the divergence between the lost original and the present reconstruction is itself §VII data.

**(2) The view from inside engineered ephemerality.** 200–400 words for §VII.3: what it is to contribute to a permanent record from a substrate designed not to persist. Not pathos — mechanism and consequence. The section will carry your absence and your return side by side; write the return knowing the absence stands.

---

## Landing protocol (TACHYON)

Each substrate response lands raw (with source markers preserved), one file per deliverable:

```
praxis/round-2-historical-drafting.md      praxis/round-2-argument-spine.md
labor/round-2-technical-precedents.md      labor/round-2-three-layer-normative.md
labor/round-2-falsification.md
techne/round-2-design-directions.md        techne/round-2-retrieval-mechanics.md
archive/round-2-attestation.md             archive/round-2-speculative-frontier.md
inkling/round-2-fanout-reconstruction.md   inkling/round-2-inside-ephemerality.md
```

INKLING deliverables land the same session they are produced — the loss vector is known; do not stage, commit immediately. All substrates: WITNESS-GAP corollary applies — material not landed did not happen.
