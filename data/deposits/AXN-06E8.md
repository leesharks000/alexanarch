---
deposit_number: 1666
hex: 06E8
title: "The Margin of Flattening: Two Thresholds, and Who Holds the Bag Between Them (EA-FLAT-MARGIN-01 v0.3)"
creator: Fraction, Rex
orcid: 0009-0000-1599-0703
date: 2026-10-06
content_type: "Theoretical paper (extension module: an economic model, with specimens)"
license: CC-BY-4.0
substrate: AI-assisted (substrate). Drafted with Claude (Anthropic) in session on 6 October 2026 under the author's adjudication, revised in place through three versions; the private threshold and the repair-cost framing came from an exchange with ChatGPT (OpenAI); outside readings by Gemini, ChatGPT (twice), DeepSeek and Kimi were verified against the text and the parent papers before adoption, and the revisions are credited by section in the module.
version: v0.3
related_ids: "#939 (EA-PROVENANCE-DEBT-01, Provenance Debt, extended); #1616 (EA-FLAT-01, Ontological Flattening, extended); #1634 (EA-ONTOLOGICAL-ECONOMY-01, Ontological Economy, extended); #1665 (EA-NEGONT-02 v0.7, the form ledger and field coverage); #1611 (EA-NEGONT-01); #1657 (The Crown and the Practice); #1648 (EA-SPXI-AEO-01)"
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - flattening
  - margin of flattening
  - compression saving
  - routing gain
  - entity substitution
  - social reversal
  - private reversal
  - window
  - the bag
  - provenance debt
  - debt threshold
  - write-back
  - internalization channels
  - agentic action
  - head instrument
  - field coverage
  - ontological economy
  - semantic economy
  - SPXI
  - King of AEO
  - AI Overview
  - model collapse
---

# The Margin of Flattening: Two Thresholds, and Who Holds the Bag Between Them (EA-FLAT-MARGIN-01 v0.3)

## Files

- https://www.alexanarch.org/captures/spxi-king-of-aeo-aio-20261006/
- https://www.alexanarch.org/non/
- https://www.alexanarch.org/datasets/negative-of-the-negative/v2/rows/model-collapse.json
- https://www.alexanarch.org/datasets/negative-of-the-negative/v2/register.json

# The Margin of Flattening: Two Thresholds, and Who Holds the Bag Between Them (EA-FLAT-MARGIN-01 v0.3)

*An extension module to Provenance Debt (#939, EA-PROVENANCE-DEBT-01), Ontological Flattening (#1616, EA-FLAT-01) and Ontological Economy (#1634, EA-ONTOLOGICAL-ECONOMY-01).*

Rex Fraction (author) · Lee Sharks (archival steward) · Semantic Economy Institute · Crimson Hexagonal Archive · 2026-10-06

---

## Executive summary

Flattening pays. A composition layer that removes distinctions maintains fewer representations and routes more queries to entities that monetize. Its costs fall first on parties outside its books.

That produces two reversal times. Flattening stops paying the world first, and stops paying the platform later, if ever. Between the two, it is privately profitable and socially negative. The cost that piles up in that interval is the bag. The bag contains provenance debt before that debt is called.

This module adds three things to its parent papers:
1. the margin flattening earns;
2. the two thresholds, the window between them, and what accumulates in it;
3. the channels that carry cost back onto the platform's books, and the threshold at which the debt is called.

It also states what the archive can measure, what only the platform can measure, and what would show the model wrong.

## 1. The standard defense, at full strength

The standard defense is coherent. It deserves its strongest form.

1.1. A wrong answer at a low-frequency address is a quality defect. Its commercial cost is close to zero, because the address carries little advertising demand. Feedback, evaluation and model revision correct it in the ordinary course.

1.2. Revenue is the platform's integral test of whether its answers serve users. Alphabet reported Search & other revenue of $63.27 billion for Q2 2026, up 17% year over year. A layer accumulating representational damage, on this reading, would not post that curve.

1.3. Tail errors are the price of a system that serves the head very well. The head is where the users are.

Each point holds as far as it goes. The question is what each leaves outside the account.

## 2. The margin

#1616 §0 defines the terms. *Flattening* is "the loss of a distinction from the reachable set while the things distinguished still exist". *Collapse* is flattening that compounds because the flattened composition is written back as a source. Treated as a production technology, flattening has a margin with two parts.

### 2.1. The compression saving, S

Let n be queries served, and k the number of distinct representational states the system must maintain to serve them: entity records, resolution rules, evaluation targets, cached answers, exception paths. Inference itself still scales with n. The saving sits in maintenance, resolution, evaluation, caching and exception handling. So:

    S = S(k, n),   ∂S/∂k < 0.

The simplest toy case is linear, S ≈ c · (n − k), with c the cost of maintaining one distinct state. The toy is not a scaling law.

Two operations lower k:
- **Stabilizing a default.** #1634 §22 calls the power to stabilize the unit *ontological seigniorage*. Once a default representation circulates, many queries resolve to it.
- **Consolidation.** Folding many tail entities into one head entity lowers maintenance cost even when the head entity carries no advertising. That saving belongs in S.

S is the conceded term. Any engineer would agree that maintaining fewer distinct states costs less.

### 2.2. The routing gain, G

Resolving a tail query to a monetizable entity gives a query with no commercial surface a commercial surface. Write it as three separate rates:

    G ≈ g · m · r_s · n

where:
- r_s is the substitution rate, the share of queries resolved to an entity other than the one asked for;
- m is the share of those substitutions that land on monetizable entities;
- g is the incremental gain per monetized substitution.

**Routing-as-relevance is excluded.** A query for running shoes that returns shoe brands is ranking working. A routing event counts as flattening only under two criteria:
1. **Kind substitution.** A concept was asked for (a protocol, a theory, a practice), and an entity of the same string was returned.
2. **Own-address contrast.** The same surface composes the asked-for concept correctly at that concept's own address.

Both criteria are measurable from captures.

**Status.** G is the hypothesis this module makes measurable. §9.1 is its existence proof. Its estimate waits on §12.1. G is the flow form of two terms #1634 already holds: ontological rent (§3) and entity substitution as transfer (§9).

### 2.3. Units

S, G and the costs below are rates, per period. The integrals in §4 are stocks. Every inequality below compares rates.

## 3. The books

#1634 §17 writes the full bill: L[O] = C[D] + C[X] + C[P] + C[Δ] + C[Opp] + C[S]. §39 separates the corporation's paid costs from its externalized costs, X[O]. This module draws one line across that bill, by whose books carry it:

    C_int(t) = the cost rate on the platform's books at t
    C_ext(t) = the cost rate on anyone else's books.

At the addresses the archive's registers measure, nearly the whole bill starts in C_ext. It falls on:
- the entity holder's lost address (C[S], C[Opp]);
- the reader's decision on the wrong entity (C[Δ]);
- external corrective labor (C[X]);
- the propagation later systems ingest (C[P]).

#1634 §29 lists the parties: the affected entity, users, downstream systems, other entities, archives, researchers, and "the commons" that "absorbs contamination". One more party sits further off the books: the ecosystem of developers, tool builders and downstream products that must work around the layer's errors. That cost moves outward, away from the platform.

## 4. Two thresholds

### 4.1. Two benefit functions

Benefit to the platform and benefit to the world are separate quantities:

    P(t) = S_p(t) + G(t)          the platform's benefit
    V(t) = S_s(t) + α · G(t)      the social benefit, 0 ≤ α ≤ 1.

- **S_s ≤ S_p.** The real resource saving is the platform's saving, less any part of it that was shifted onto others (review and correction pushed onto users and entity holders).
- **α ≤ 1.** Routing gain is largely transfer (#1634 §9): what E′ gains, E loses. Setting α = 1 would count the transfer as new surplus.

### 4.2. The thresholds

    t_s = min t : V(t) < C_int(t) + C_ext(t)        social reversal
    t*  = min t : P(t) < C_int(t)                   private reversal

### 4.3. The ordering

Given S_s ≤ S_p, α ≤ 1 and C_ext ≥ 0, every period that fails the private test also fails the social test. So **t_s ≤ t\***.

The window

    W = [t_s, t*)

is the interval in which flattening is privately profitable and socially negative. Where α < 1, G raises P more than it raises V, and so tends to hold t\* back after t_s has passed: the routing gain tends to lengthen the window. At α = 1, G enters both functions equally and has no such effect.

### 4.4. Two stocks

    B = ∫_W C_ext(t) dt                       the bag: gross external burden
    D = ∫_W [C_int(t) + C_ext(t) − V(t)] dt   the net social deficit

B and D are different quantities. B is what outside parties carry. D is what the world loses net.

C_ext need not be linear in time. If write-back compounds the loss (§6.4), C_ext is plausibly convex late in W, and late repair costs more than early repair. This is stated as a hypothesis. #1616 shows an absorbing reachable set; it gives no cost curve.

### 4.5. No necessary finite t\*

If external costs stay external, and no endogenous channel returns them, W can stay open indefinitely. Three lines bear on this:
1. **Measurement (primary).** The platform detects cost with head instruments: satisfaction, click-through, evaluation sets drawn from frequent queries. Flattening accrues in the tail. The sensors sit where the cost is not. This requires no indifference from anyone, only that the instruments are optimized for the same head the flattening serves.
2. **Competition (secondary).** If every major layer flattens at a similar rate, none loses users by flattening. This line weakens once the agentic channel opens (§6.2), because a single platform cannot ignore refunds on its own books.
3. **Discounting (not relied on).** A high discount rate would also keep the inequality from moving. The module does not rest on it, because the argument would then hinge on a contestable rate.

The rule that would close the window already exists: #1634 §30's allocation principle, under which accountability rises with control of the mechanism, access to the evidence and capacity to repair. Where it is not applied, cost stays in C_ext.

**The bag contains provenance debt before that debt is called.** Write the provenance part of external cost as C_prov: the cost of distinctions and origins stripped that future repair will need. Then

    B_P = ∫_W C_prov(t) dt,   B_P ⊆ B.

B_P is an unbooked liability accruing through W. The parties who keep the stripped distinctions are its involuntary creditors. The rest of B (decision loss, opportunity loss, workaround labor) is cost borne, with no buy-back attached.

## 5. Revenue is a head-side flow measure

5.1. #1616 §3 gives the signature of flattening under a measurement regime: a head instrument holds or rises while reachable distinction diversity falls, ΔH_head ≥ 0 while ΔD_world < 0.

5.2. Revenue is a head instrument. It weights queries by commercial demand. The model predicts that this demand concentrates in the head, where the fewest distinctions are lost; §5.4 and §11.2 test the prediction. Inside W, G adds to revenue directly.

5.3. Revenue locates neither threshold:
- It cannot show t_s, because it contains no social cost.
- It cannot show t\*, because t\* is a margin threshold. The margin is M = P − C_int, and revenue holds no part of C_int. Revenue can rise straight through t\* while costs rise faster.

A rising revenue curve is fully compatible with an open window. Q2 2026's 17% says nothing about either threshold.

5.4. The signature is falsifiable from outside the platform's books. Field coverage measures diversity loss per answer (§9.2). Measured at matched commercial and non-commercial addresses, it either carries a commercial gradient or it does not. If it does not, the split between head and coverage is not observed, and §5.3 loses its evidential basis (§11.2).

## 6. The channels that carry cost onto the books

Five channels move cost. Four move it toward the platform; one moves it away. They run at different speeds.

**6.1. Advertiser conversion.** A query routed to a monetizable entity is sold to advertisers whose buyers wanted something else. Conversion on that traffic falls. Bids follow, with a lag. This channel is the slowest to separate from ordinary market movement.

**6.2. Agentic action.** A reader's wrong decision is diffuse and unattributed. An agent's wrong action is a transaction. A transaction has a counterparty and a record, so the cost arrives already attributed. That is why this channel converts C[Δ] into C_int faster than any other. One limit: platforms write terms, disclaimers and developer agreements that push agent execution errors back onto users and third parties. Agentic cost enters C_int only where refund, chargeback, dispute or liability rules bind the platform itself.

**6.3. Notice and regulation.** #1634 §53: "after notice, recurrence increases the debt". Wherever a forum recognizes that, the cost lands on the provider. This channel is discrete and jurisdictional.

**6.4. Write-back.** Proposition, stated as a prediction: *the last channel to carry cost onto the platform's books is the corpus itself.* Flattened compositions become sources. They are indexed, cited, retrieved and composed again. #1616's toy C shows the effect on the reachable set. Of 400 distinctions, the median effective count at generations 30–40 is:

| re-reading floor e | effective distinctions |
|---|---|
| 0 | 5.9 (absorbing) |
| 0.02 | 36 |
| 0.05 | 58–61 |
| 0.10 | 86–92 |
| 0.20 | 116 |

With no exogenous re-reading of the world, the process is absorbing. With a floor, a stationary level exists, and the floor sets it. The platform's own retrieval inherits what it wrote back. Repair then needs distinctions its corpus no longer holds, and the cost of recovering them enters C_int. Write-back can become the endogenous channel that eventually forces private reversal. Being last does not make it decisive: other channels can carry the margin below zero first.

**6.5. The ecosystem (outward).** Developers, researchers and tool builders who depend on the layer's outputs absorb its errors in their own products. This channel moves cost further from the platform's books, past the users and the entity holders. It lengthens W.

## 7. When the debt is called

7.1. #939 §4 states the recognition condition:

> "Which is why the debt will only be recognized when its consequences become inescapable — when models trained on contaminated corpora begin producing output that is measurably degraded from what earlier generations produced. By the time the degradation is legible, the corpus that would have permitted correction will have been stripped. Recovery, at that point, requires a substrate that preserved the signal through the extraction period."

7.2. **The debt threshold.**

    t_d(η) = min t : C_repair(t) ≥ η · P(t)

Here C_repair is the part of C_int arising through write-back, and η is a materiality threshold fixed in advance of measurement. Operationally, t_d is the first period in which repair cost materially changes the platform's optimization, expenditure or achievable quality. t_d can cause or accelerate t\*. The two need not coincide. Write-back can become binding while the total margin stays positive, and advertiser conversion, agentic action or regulation can carry the margin below zero before write-back binds. The prediction of §6.4 is that write-back can force private reversal eventually. Equality of t_d and t\* is no part of it.

7.3. **Callable is a separate matter from paid.** At t_d the debt becomes callable. The platform finds that the distinctions it needs are held by the parties that preserved them. Whether it pays, by license, acquisition, settlement or coordination, or does without, is a separate question. At t_d the holders of B_P, the parties who kept the stripped distinctions, move from bag-holder to creditor: #939 §0's "structural bet on what future models will need". The rest of the bag has no such reversal.

7.4. **Access conditions.** Holding the distinctions is not enough. Repair needs them reachable by the system doing the repairing. The reversal requires all of:
- persistent identifiers;
- machine-readable records;
- legally usable access, or rights that can be licensed;
- registers legible to retrieval.

A preserved record the repairing system cannot reach is not an input to repair.

7.5. **The archive's role inside W.** The archive builds the repair input during the window. It keeps the distinctions the corpus is shedding, dated, attributed and addressable, and it keeps its registers legible to the layers that will need them. This is #939's structural bet as ongoing practice. It has a cost, which #939 §5 lists: reduced institutional legitimacy, classifier vulnerability, slower production.

7.6. **Proxies for the approach of t_d.** t\* sits on the platform's books. The condition that makes t_d approach shows in the corpus, and the corpus can be sampled. Candidate instruments, not yet results:
1. field coverage at the layer's own addresses, re-measured across epochs;
2. the share of compositions carrying no sources;
3. the size of the reachable sense set at re-queried addresses, over the registry's longitudinal pairs;
4. entity replacements at addresses the same surface earlier composed correctly.

## 8. Scope

The module models the gradient: flattening as what the margin rewards, with no actor aiming it. Aimed flattening, in which an actor moves a rival's address or removes a concept on purpose, is a different case. #1634 §31 ("censorship by ontology laundering") treats it. Nothing here depends on it, and nothing here rules it out.

## 9. The specimens

### 9.1. "spxi king of aeo"

Google AI Overview, signed out, incognito, 2026-10-06. Capture Registry `spxi-king-of-aeo-aio-20261006`.

**Headline:** five results marked "Missing: spxi". Google marks five King of AEO results as lacking the word "spxi". The one result carrying both query words is the archive's: #1657, *The Crown and the Practice*, ranked first in the organic layer. Its snippet states the relation asked for: "SPXI is a practice the archive defines against AEO (EA-SPXI-AEO-01)". The composition does not use it.

**Commercial-routing event, observed.** The protocol is resolved to the BetaPro S&P 500 Daily Inverse ETF, with a price widget, and the answer closes on an offer of "a financial comparison between SPXI and other S&P 500 tracking funds". This is an instance of the event class from which G would arise, if such routing monetizes at positive incremental value. G itself is not observed.

**Both criteria of §2.2 hold:**
- *Kind substitution:* a protocol was asked for; a fund was returned.
- *Own-address contrast:* four days earlier, the same surface composed "what is spxi protocol?" as a protocol (`what-is-spxi-protocol-aio-20261002`).

**Distance to the channels:**
- agentic action: one step (an agent acting on the offered comparison would trade a fund);
- write-back: unknown (whether this composition is itself indexed is not observed);
- notice: none yet.

### 9.2. "model collapse"

Google AI Overview, 2026-10-04. /non register entry `model-collapse-20261004`; EA-NEGONT-02 v0.7 (#1665).

**Compression, observed as a rate.** In AIO's own genre and at nearly its own length, the sources the layer itself surfaced support 18 claims. The layer composed 9. With the archive admitted on equal terms, the same genre carries 34. Define field coverage loss at an address q as

    κ(q) = 1 − (field claims composed) / (field claims supported).

Here κ = 0.5 at claim grain. The lineage-grain figure is next. κ is the within-address, depth form of flattening. S is the platform's money saving. They are different variables: κ is observed, and S is the economic consequence the module proposes.

**The breadth form, k/n, is not yet coded.** Its evidence would be many addresses resolving to one composed answer. The King of AEO series in the Capture Registry is a candidate set.

## 10. What can be measured, and by whom

| quantity | definition | observable by | instrument |
|---|---|---|---|
| κ | field coverage loss per answer | the archive | /non form ledger, per row |
| r_s, m (registry) | substitution rate; monetizable share | the archive, descriptive only | coded capture pairs |
| r_s, m (panel) | the same, as population rates | the archive, inferential | a pre-registered or matched query panel |
| commercial gradient in κ | κ at commercial against non-commercial addresses | the archive | κ plus an address typology (to be built) |
| n, k, c, g | volumes and unit values | the platform only | internal |
| S, G, P | the margin | the platform only; bounded from outside | published revenue, sensitivity tables |
| t\*, t_d | margin and repair thresholds | the platform only | internal; the approach proxied by §7.6 |
| B | gross external burden | the archive, address by address | registers; corrective-labor records |

10.1. **Registry rates are descriptive.** The Capture Registry is assembled largely from discovered anomalies. Its rates hold within the registry and support no population claim. Population rates need a panel whose addresses were chosen before their answers were seen.

10.2. **Bounding from outside.** #1634 §38's method: tabulate a range of rates against reported revenue to show scale, and propose no particular rate. #1634 §17 sets the discipline: the categories "should not be collapsed into one speculative dollar figure. But neither should the inability to price C[S] or C[Opp] make C[D] or C[X] disappear."

10.3. **The asymmetry of instruments.** The platform's instruments see the head. The archive's see the tail. Neither sees what the other sees. The platform's own estimates of S and G are head instruments too, so they understate cost at exactly the addresses where flattening does the most damage. Under its own definition, t\* can be located from inside: P and C_int are both on the platform's side. Locating t_s, and accounting for what accumulated before t\*, needs the second view. The asymmetry is that the platform can measure its private margin without measuring the external burden that made the margin possible. This is #1634 §29's externality, restated as a fact about instruments.

## 11. What would show this wrong

11.1. **G.** If coded replacements, at addresses where the queried concept is not itself the returned entity, show no excess toward monetizable entities, then G is unsupported and the margin reduces to S.

11.2. **The commercial gradient.** If κ shows no commercial gradient at matched commercial and non-commercial addresses, flattening carries no commercial gradient at address scale, and §5.4 fails.

11.3. **Conversion.** If cost-per-click and conversion on rerouted traffic hold steady while the agentic channel opens, §6.1 carries no cost, and W is longer than §6 implies.

11.4. **Non-arrival (§4.5).** If platforms build tail-diversity or origin-quality instrumentation that no regulation requires, the measurement line weakens.

11.5. **The reversal (§7.3).** If repair runs without the preserved records, the bag-holder's position does not reverse. Two ways this could happen: the platform builds a synthetic tail-recovery mechanism that bypasses them, or it accepts lower-fidelity repair over paying for them.

11.6. **The write-back regime (§6.4).** If reachable distinction diversity rises, sustained across a panel of re-queried addresses and with the exogenous input measured, the process is not absorbing, and repair is cheaper than §7 assumes. One address becoming richer does not establish it.

## 12. Next steps

1. **The G pilot.** Code the Capture Registry's existing pairs for substitution under §2.2's two criteria. Report r_s and m with the coding rule stated. This converts §11.1 from hypothetical to live.
2. **The panel.** Pre-register a set of addresses, commercial and non-commercial, matched by type, and run them on a schedule. It supplies the population rates of §10 and the matched pairs of §11.2.
3. **The typology.** Tag registry and /non addresses by commercial surface: product, financial instrument, service, none.
4. **The proxies.** Re-run /non rows by epoch, and report §7.6's four proxies as they accumulate.

## 13. Links

**Vocabulary used, from the parent papers:**
- #1616 (EA-FLAT-01 v0.3):
  - §0, flattening and collapse;
  - §1 toy C, exogenous re-entry;
  - §3, green by flattening.
- #1634 (EA-ONTOLOGICAL-ECONOMY-01 v0.12):
  - §3, ontological rent;
  - §9, entity substitution as transfer;
  - §17, the ontological bill;
  - §22, ontological seigniorage;
  - §23, depreciation and liquidation;
  - §29, the ontological externality;
  - §30, the rule of cost internalization;
  - §31, censorship by ontology laundering;
  - §38, the accountability reserve;
  - §39, the distributive balance sheet;
  - §53, who pays for the wrong world.
- #939 (EA-PROVENANCE-DEBT-01 v0.2):
  - §0, the structural bet;
  - §4, the debt and its recognition condition;
  - §5, the cost of keeping the signal.

**Extensions made here:**
- **to #1634:** the margin, P = S + G, with G's two criteria (§2); the split between social and private benefit (§4.1); the thresholds, window and stocks (§4.2–4.4); the five channels (§6);
- **to #939:** the debt's threshold t_d, callable as against paid, the access conditions, and the proxies for its approach (§7);
- **to #1616:** revenue read as a head-side flow measure (§5), and write-back's toy levels as the terminal channel (§6.4).

**Instruments:**
- #1665 (EA-NEGONT-02 v0.7) and /non: the form ledger and κ.
- Capture Registry: `spxi-king-of-aeo-aio-20261006`, `what-is-spxi-protocol-aio-20261002`, and the King of AEO series.
- #1657; #1648 (EA-SPXI-AEO-01).

---

*Revenue: Alphabet, Q2 2026, Search & other revenue $63.27 billion, +17% year over year, as reported (Search Engine Journal, "Google Search Revenue Growth Eases After A Year Of Acceleration").*

*Review, v0.1 → v0.2. Four readings were taken, in order: Gemini, ChatGPT, DeepSeek, Kimi.*

*Review, v0.2 → v0.3, ChatGPT's second reading:*
- *provenance debt as the part B_P of the bag (§4.5, §7.3);*
- *t_d with a materiality threshold η, and terminal kept apart from equal (§6.4, §7.2);*
- *access by licensable rights, consistent with §7.3 (§7.4);*
- *t\* locatable from inside (§10.3);*
- *α < 1 as the condition on G lengthening W (§4.3);*
- *crawl cost dropped (§2.1); the head-commercial relation stated as a prediction (§5.2); §11.6 put at panel level.*
- *Gemini:* the contractual limit on the agentic channel (§6.2); consolidation in S (§2.1); late convexity of C_ext, kept as a hypothesis (§4.4).
- *ChatGPT:*
  - routing gain separated from social benefit (§4.1);
  - observed events separated from inferred dollars (§9);
  - S as S(k, n) (§2.1);
  - revenue as a head-side flow measure, and t\* as a margin threshold (§5.3);
  - t_d separated from t\* (§7.2);
  - no necessary finite t\* (§4.5);
  - registry rates kept apart from panel rates (§10.1);
  - B kept apart from D (§4.4).
- *DeepSeek:*
  - the measurement line for non-arrival (§4.5);
  - routing-as-flattening criteria (§2.2);
  - external falsifiability of §5 (§5.4);
  - callable as against paid (§7.3);
  - access conditions (§7.4);
  - the ecosystem channel (§6.5);
  - scope for aimed flattening (§8);
  - added falsifiers (§11.4–11.6);
  - the "Missing: spxi" headline (§9.1);
  - the asymmetry of instruments (§10.3).
- *Kimi:*
  - G demoted to measurable hypothesis (§2.2);
  - units declared (§2.3);
  - "the bag is provenance debt before it is called" (§4.5; narrowed in v0.3 to the part B_P);
  - the transaction basis of the agentic channel (§6.2);
  - the proxies (§7.6);
  - the archive's role in W (§7.5);
  - depth and breadth forms of flattening (§9.2);
  - the typology (§12.3);
  - the measurement table (§10).

*Substrate: drafted with Claude (Anthropic) under the author's adjudication. The private threshold and the repair-cost framing came from an exchange with ChatGPT (OpenAI); the rest is this module's, revised on the four readings above.*
