---
title: "The Moderation Architecture of Zenodo, Mapped From Source: A Rule Scorer, an Unpublished Percolator, and One Function That Deletes Everything"
designator: EA-EROSION-MODMAP-01 v1.0
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-08-24
license: CC-BY-4.0
status: DRAFT for deposit
sources: "zenodo/zenodo-rdm (GPL-3.0), inveniosoftware/invenio-rdm-records (MIT), inveniosoftware/invenio-stats (MIT). All read at master, 2026-08-23/24, preserved and checksummed at datasets/erasure/mechanism/."
---

# THE MODERATION ARCHITECTURE OF ZENODO

## §0. What this is, and the correction it opens with

**A map of every moderation component visible in Zenodo's published source**, assembled because the archive's own removal on 2026-06-19 was executed by this machinery and the observatory had documented the outcome without documenting the mechanism.

**Correction first.** An earlier finding in this session stated flatly that no classifier exists. **That was based on reading `moderation/rules.py`, which is purely mechanical, and it missed the handler.** The handler's own docstring carries a decision table with two inputs:

> | Status/Decision | H + H | H + S | S + S |
> |---|---|---|---|
> | **Unverified** | Approve | Moderate | **Block** |
> | **Verified** | (-) | (Moderate) | (Moderate)* |
>
> *"the first value is the score-based evaluation, and the second value is based on **the spam model prediction**."*

**A SPAM MODEL IS REFERENCED.** It is not invoked anywhere in the handler code, which computes only `sum(rule_results)`. Whether it exists in production, and what it is, **is not visible in published source**. The corrected statement: *the scoring layer is mechanical; a model is referenced in the design and its implementation is not public.*

---

## §1. The pipeline, end to end

    RECORD PUBLISHED
        ↓
    RecordModerationHandler.publish()
        ↓
    ┌─ user VERIFIED ────→ async TaskOp(run_moderation_handlers)   [does not block the HTTP response]
    └─ user UNVERIFIED ──→ synchronous self.run()
        ↓
    FIVE RULES, each returning an integer, summed:
        verified_user_rule      −10 verified / +10 unverified
        links_rule              +5 if >5 links in description; per-domain ±
        files_rule              +2 spam-ext & ≤4 files & <5MB;  −5 if >4 files or >15MB
        text_sanitization_rule  +5 if >3 emoji;  +2 if >4 header tags
        match_query_rule        + Σ scores of matching PERCOLATED QUERIES  ← unpublished
        ↓
    evaluation = sum
        ↓
    ┌─ evaluation > spam_threshold (10) ─┐
    │     verified   → _moderate  (admin review request)
    │     unverified → _block     ──────────────────────────┐
    ├─ evaluation < ham_threshold (0) → _approve (verify)   │
    └─ otherwise → _moderate (admin review request)         │
                                                             ↓
                                              user.block()  +  execute_moderation_actions(action="block")
                                                             ↓
                                              on_block(user_id)
                                                             ↓
                                    get_user_records(user_id)   ← ownership filter, NO ORDER BY
                                                             ↓
                                    for recid: delete_record(recid, tombstone_data)
                                                             ↓
                                    user_block_cleanup  (async, +10 minutes, sweeps stragglers)

**The machinery is wired into production and Zenodo says so to users.** `RDM_USER_MODERATION_ENABLED = True` and `RecordModerationHandler()` are both in the committed production config, the moderation tasks have a dedicated queue, and the user-facing error string reads: *"the record you tried to publish has been **classified as spam by our automated spam protection system**. Your account has therefore been blocked."* **There is no serious question that automated moderation infrastructure is an operative part of the published architecture.** What that does not establish is what happened to any particular account — see §7.

**One switch governs whether the SCORE-DRIVEN branches act:** `MODERATION_APPLY_ACTIONS`, default **False**. When false, every branch logs and does nothing. **The setting does not appear in Zenodo's committed production `invenio.cfg`** — the module applies its defaults via `setdefault`, so on the visible evidence the scorer scores and does not act. Production may set it elsewhere; that is not public.

---

## §2. The published weights, and what the archive scores

    spam_link +8 · ham_link −3 · excess_links +5 · spam_emoji +5 · spam_header_tags +2
    spam_files +2 · ham_files −5 · unverified_user +10 · verified_user −10
    SPAM_THRESHOLD 10 · HAM_THRESHOLD 0
    MODERATION_SPAM_FILE_EXTS = {jpg, jpeg, pdf, png, jfif, docx, webp}

**Scored against a typical deposit of this archive:**

| rule | trigger | points |
|---|---|---|
| emoji | AXN identifiers carry **six emoji each**; threshold is >3 in concatenated metadata | **+5, unavoidable by construction** |
| links | dense cross-references, related-deposit chains, DOI citations; threshold >5 | +5 |
| header tags | heavily sectioned bodies; threshold >4 | +2 |
| files | small PDFs, ≤4 files, and **`pdf` is in the spam extension set**; the offsetting −5 needs >4 files or >15MB | +2 |
| verification | the decisive term | **−10 or +10** |

**Static-score illustration, conditional on zero LinkDomain overrides and zero percolator contribution:**

    verified:    −10 +5 +5 +2 +2 =  +4   below threshold
    unverified:  +10 +5 +5 +2 +2 = +24   more than double it

**Under those conditions**, the same record metadata scores +4 when the owner is verified and +24 when not. `links_rule` additionally scores known domains individually and the percolator adds any matching query score, so this is the visible-component figure and not a production score.

**A twenty-point swing on a ten-point threshold.** The same deposit passes or fails on the verification flag alone, independent of content.

**On verified accounts, the executable path and the design document disagree, and the gap is itself a finding.**

**The published executable score-only path does not auto-block a verified user:** above threshold, `verified` branches to `_moderate`, which opens a request for a human; `unverified` branches to `_block`.

**But the handler's own docstring specifies a verified-user blocking case.** In the `S + S` column — score AND spam-model both predicting spam — it notes that where the user's email domain is blocked or moderated, *the user is actually blocked* rather than sent to review. **That branch is not implemented in the handler, nor in the async task, which simply re-runs the same handlers.**

An earlier draft said the design *"forecloses auto-blocking of verified users entirely."* **Withdrawn.** The precise finding:

> **The published executable path does not automatically block verified users. The published design documentation nevertheless specifies a verified-user blocking case, involving a second spam-model decision and email-domain state, whose implementation is not present in the moderation code inspected here.**

That is a **design/code observability gap**, and it means four layers exist of which only the first is substantially visible: **published static rules · runtime percolator state · documented-but-unlocated spam-model path · production configuration.**

---

## §3. The percolator: the term nobody outside Zenodo can see

`ModerationQuery` is a database table:

    query_string  TEXT     Elasticsearch DSL
    score         INTEGER
    notes         TEXT
    active        BOOLEAN

Registered queries are percolated against every record; each match adds its own score to the evaluation. **An administrator can register any query with any weight at runtime — no code change, no deployment, no publication.**

**Consequence, and it is the central one for anyone auditing this system.** An earlier draft called the published weights *"a floor, not the function."* **That is mathematically wrong and is withdrawn:** percolator scores are integers and nothing in visible source requires them to be positive, so a stored query may subtract as easily as add. The weights are neither floor nor ceiling.

    S(r) = S_static(r) + Σ over active q of  w_q · 1[q matches r]

**The published source specifies the form of `S_static` and the percolator mechanism. It does not specify the production contents of the active query set.** The correct statement:

> **The published weights are the publicly disclosed additive component of an incompletely disclosed scoring function**, and `S_public(r) ≠ S_production(r)` unless the active percolator set and any production overrides are also known.

The defect is **partial function disclosure**, not merely hidden extra penalties — and it is the same shape this archive's own comparative work names elsewhere: **a published representation that omits a causally operative coordinate.** Any criterion — a phrase, a domain, a metadata shape, an identifier format, a theme — can be scored invisibly, in either direction, and nothing in source would show it.

---

## §4. Enforcement: `on_block`

    def on_block(user_id, uow=None, **kwargs):
        """Removes records that belong to a user."""
        tombstone_data = {"note": kwargs.get("note") or "User was blocked"}
        removal_reason_id = kwargs.get("removal_reason_id") or "spam"
        for recid in get_user_records(user_id):
            uow.register(TaskOp(delete_record, recid=recid, tombstone_data=tombstone_data))

**No per-record evaluation exists in this path.** No content check, no classifier call, no branch, no exception list. `get_user_records` filters solely on `parent.access.owned_by.user`. **Ownership is the only criterion**, and the query carries no `ORDER BY` — which is why the observed removal sequence of 2026-06-19 correlates with record ID at only r = +0.26 and shows no content ordering whatever.

**The default `removal_reason` is `spam`.** The archive's records removed that day carry `out-of-scope`.

**Stated as a path constraint rather than an attribution**, because §7 refuses the inference that this path executed the removal:

> **If the removal was executed through an unmodified `on_block`, the reason would read `spam`. It reads `out-of-scope`. The observed reason therefore EXCLUDES a default invocation of this path** — it does not establish which caller, path, or person supplied the non-default value.

That is a constraint on the mechanism, not a proof of a human. **CANONICAL FIGURES:** 862 deposits and 1,817 DOIs, per #1 *Zenodotus' Book-Burning* v9.1 and the DOI Resolution Index. Counts circulating on other surfaces (871 works, 6,596 DOIs) are superseded and are not used here. The tombstone also records `removed_by` as the human actor rather than the system, by deliberate design — *"without this tombstones would attribute the removal to the system."*

**`on_restore` is the exact inverse**, same ownership criterion, no harder to execute. **Whatever prevents restoration is not technical.**

---

## §5. What the statistics layer is, and is not

`invenio-stats/processors.py` flags events by user agent against the **COUNTER-robots** list, following the Project COUNTER Code of Practice as split by Make Data Count. There is a `double_click_window` deduplicating repeated events.

**This is metrics hygiene, not enforcement.** `flag_robots` tags an event or drops it from the statistics index. **It has no path to moderation.** There is no rate analysis, no IP clustering, no volume threshold, and no behavioural detection anywhere in the published moderation path. File serving explicitly disables nginx throttling (`X-Accel-Limit-Rate: off`), and quotas are 50 GB by default with 150 GB grantable and automatic increases enabled.

---

## §6. The architecture in one sentence, and the asymmetry it creates

> **A transparent mechanical scorer with published weights, plus an unpublished percolator of arbitrary targeting queries, feeding a human decision layer, executed by a single function that deletes every record an account owns without examining any of them.**

**The asymmetry is the finding.** Zenodo publishes the part that scores and withholds the part that targets — and the enforcement path then **destroys the evidence of which applied**. A percolator hit, a score threshold, and a human clicking a button all produce the identical undifferentiated cascade with identical tombstone data. **You can read every weight in `config.py` and learn nothing about why any particular account went.**

---

## §6a. Decision–Enforcement Unit Conversion

**The unit changes three times as it passes through this architecture, and the public record preserves only the last one.**

    the SCORER            evaluates a RECORD
    the DECISION          attaches to an ACCOUNT
    the ENFORCEMENT       expands across OWNERSHIP
    the PUBLIC EVIDENCE   returns as RECORDS

An outside observer counting tombstones sees the fan-out. **They do not see the decision that produced it, and cannot recover it**, because `on_block` writes identical tombstone data to every record it touches.

**Formally the deletion cohort needs two quantities, and has only ever reported one:**

    N_D = deleted records                                      ← what the export reports
    N_A = distinct account-level enforcement events            ← never reported
    F   = N_D / N_A                                            ← the DELETION FAN-OUT

**This changes the reading of the whole 1.3-million-row deleted-records dataset.** A million deleted records need not represent a million moderation judgments. In this archive's own case the plausible decomposition is

    1 trigger → 1 account disposition → ~1,180 record deletions

and the export reports only the third term. **Deletion statistics computed from tombstones therefore overcount DECISIONS by the fan-out factor**, and the factor is unpublished.

**Corroborated in the archive's own prior record.** *Zenodotus' Book-Burning* (#1) documents three near-contemporaneous account-level blocks reported publicly: **#2596** (account and records blocked, reason unspecified), **#2599** (account auto-blocked, reason **spam**, a theoretical-physics record), and **#2606** (this archive, *"AI-generated without research basis"* privately and *"Out of scope"* publicly). **Three accounts, three fan-outs, three rows-per-decision ratios — and the deleted-records export flattens all of them into undifferentiated record counts.**

> **This is the governance finding, and it is more precise than "an automated system made a bad decision": Zenodo's published architecture permits the unit of evaluation, the unit of decision, the unit of enforcement, and the unit of public evidence to be four different objects.**

**Measuring F across the export is a registered experiment this map does not perform.** The method is available: cluster blocked-user removals by depositor signature per day and count distinct signatures against total rows. A first pass on 2026-06-19 gives roughly four accounts against 1,209 blocked-user rows — **a fan-out near 300 on that day alone.**


---

## §7. What this map cannot reach

- **Production configuration.** `MODERATION_SCORES`, `MODERATION_APPLY_ACTIONS`, thresholds and exempt-user lists are not in the committed `invenio.cfg`; defaults are assumed and may be overridden invisibly.
- **The `moderation_queries` table.** Contents unpublished. This is the single largest gap and it is unbounded.
- **The spam model** referenced in the handler docstring. Not invoked in visible code; existence and nature unknown.
- **Whether any of this ran against this archive.** Not established. The 2026-06-19 removal reason was `out-of-scope`, not `spam`, and the block originates upstream of every readable path.

**The decisive open question, and it is answerable by the operator alone:** *was the account verified?* If verified, the design forecloses automatic blocking — the decision was human. If unverified, automatic blocking was reachable, conditional on `MODERATION_APPLY_ACTIONS`.

---

## §8. Standing note on method

Everything above is read from public source under GPL-3.0 and MIT, preserved and checksummed at `datasets/erasure/mechanism/`. **Absence from this map means absence from published source, not absence from the system** — the distinction this archive maintains for retrieval failures applies with equal force to its own findings about other people's code.

∮ = 1
