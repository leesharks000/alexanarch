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

**One switch governs whether any of this acts:** `MODERATION_APPLY_ACTIONS`, default **False**. When false, every branch logs and does nothing. **The setting does not appear in Zenodo's committed production `invenio.cfg`** — the module applies its defaults via `setdefault`, so on the visible evidence the scorer scores and does not act. Production may set it elsewhere; that is not public.

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

    verified:    −10 +5 +5 +2 +2 =  +4   below threshold
    unverified:  +10 +5 +5 +2 +2 = +24   more than double it

**A twenty-point swing on a ten-point threshold.** The same deposit passes or fails on the verification flag alone, independent of content.

**And the design forecloses auto-blocking of verified users entirely.** Per the decision table, a verified account never reaches `_block`; it reaches `_moderate`, which opens a request for a human. **Automatic blocking is reachable only for unverified accounts.**

---

## §3. The percolator: the term nobody outside Zenodo can see

`ModerationQuery` is a database table:

    query_string  TEXT     Elasticsearch DSL
    score         INTEGER
    notes         TEXT
    active        BOOLEAN

Registered queries are percolated against every record; each match adds its own score to the evaluation. **An administrator can register any query with any weight at runtime — no code change, no deployment, no publication.**

**Consequence, and it is the central one for anyone auditing this system:** publishing `MODERATION_SCORES` does not disclose the operative scoring. `match_query_rule` contributes an unbounded, unpublished term. **The public weights are a floor, not the function.** Any targeting criterion — a phrase, a domain, a metadata shape, an identifier format, a theme — can be given a score invisibly, and nothing in source would show it.

---

## §4. Enforcement: `on_block`

    def on_block(user_id, uow=None, **kwargs):
        """Removes records that belong to a user."""
        tombstone_data = {"note": kwargs.get("note") or "User was blocked"}
        removal_reason_id = kwargs.get("removal_reason_id") or "spam"
        for recid in get_user_records(user_id):
            uow.register(TaskOp(delete_record, recid=recid, tombstone_data=tombstone_data))

**No per-record evaluation exists in this path.** No content check, no classifier call, no branch, no exception list. `get_user_records` filters solely on `parent.access.owned_by.user`. **Ownership is the only criterion**, and the query carries no `ORDER BY` — which is why the observed removal sequence of 2026-06-19 correlates with record ID at only r = +0.26 and shows no content ordering whatever.

**The default `removal_reason` is `spam`.** All 1,180 archive records removed that day carry `out-of-scope`, so **a non-default value was passed explicitly**. The tombstone also records `removed_by` as the human actor rather than the system, by deliberate design — *"without this tombstones would attribute the removal to the system."*

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
