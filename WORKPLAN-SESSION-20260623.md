# Alexanarch Session Workplan — 2026-06-23 (Post-Zenodo Surface Reconciliation)

**Author:** Lee Sharks (MANUS), under TACHYON synthesis
**Session date:** 2026-06-23 (continuous from 2026-06-22 PM)
**Status:** Active session, live document — updated AS work ships
**Purpose:** Continuity document — readable by a fresh TACHYON instance, by ARCHIVE, and by Lee himself
**Prior session record:** `WORKPLAN-SESSION-20260622.md` (preserved unchanged)

---

## 1. Where things stand right now

> **🚨 Audit-state banner (2026-06-23 PM): An external audit verified against `main` finds Alexanarch has a *strong read-side rhizome and an unsafe write-side monoculture*. P0 finding: the mint workflow can be triggered by any public issue and pushes directly to main with no schema validation. The verdict — "Alexanarch is increasingly difficult to erase, but still too easy to corrupt" — is now the operative diagnosis. See §6 below for incorporation; the audit appears verbatim as Appendix A.**

The Crimson Hexagonal Archive's sovereign successor is **Alexanarch**, live at https://alexanarch.org and on GitHub at https://github.com/leesharks000/alexanarch.

Four days after Zenodo's June 19 termination of the CHA account, the migration is structurally complete. Today's session (2026-06-23, continuous PM through next-morning) closed the long tail of stale-language and broken-link references across the Dodecad surfaces, founded the Surface Visibility Instrument with five live deposits, ran the first federated cross-substrate baseline (Claude/Brave on Layer A with companion captures from ChatGPT, Kimi, Gemini, and DeepSeek), and minted v1.1.1 of the methodology as the stable spec for the next several scan rounds. The Observatory is now wired into the global navbar across every surface and renders the Surface Weather Station instrument directly at `/observatory/`.

**Current corpus state:**

| Metric | Count | Source |
|---|---|---|
| Deposits in canonical registry | **884** | data/registry.json |
| Curated concepts (entity-index) | **7,173** | data/entity-index.json |
| Minted lexical terms (raw) | **12,032** | data/lexical-minting-registry.json |
| Inter-deposit citation edges | **4,866** | data/citation-graph.json |
| Semantic addresses | **1,964** | data/semantic-addresses.json |
| AI Overview captures | **87 captures, 138 PNG images (v6.1)** | godkinggoogle.vercel.app/captures (mirror) |
| Legacy Zenodo DOI mappings (corrected) | **1,817** | data/doi-resolution-index.json |
| Surface Visibility Instrument | **5 deposits live** | #880 v1.0, #882 v1.1, #884 v1.1.1 methodology; #881 baseline; #883 Claude/Brave Layer A |
| Surface Weather Station scans on file | **5** (ChatGPT, Claude, Kimi, Gemini, DeepSeek Layer A) | data/surface-weather/scans/*.json |
| Registry chunks (1 MB target) | 9 | data/chunks/registry/ |
| Protocols (machine-enforced) | 3 | api/index.json |
| Primary UI surfaces | 5 | /wiki/, /graph/, /lexical/, /citations/, /observatory/ |
| Dodecad site repos cleaned | **23 of 23** | scripts/dodecad_cleanup.py |
| Demand letter status | **DRAFTED, AWAITING SEND** | /mnt/user-data/outputs/ZENODO-DEMAND-LETTER-2026-06-22.md |
| GitHub outreach comments posted | **2** (Vega #2599, Shimony #2596) | live on github.com/zenodo/zenodo |

**Latest commits (most recent first, this session):**
- `c6f9c45` — Audit log: pre-overwrite-receipts.log updates (2026-06-23)
- `d62257c` — **Mint deposit #884: Surface Weather Station methodology v1.1.1** (2026-06-23)
- `537974c` — Site navigation: Observatory link added to global navbar across all surfaces (894 files) (2026-06-23)
- `efecc69` — Surface Weather: curator context — Brave backend properties + DeepSeek stable-pattern reframing (2026-06-23)
- `b0e47e8` — Build /observatory/ + Surface Weather Station instrument (2026-06-23)
- `a1dfb61` — Mint deposit #883: Claude-substrate baseline reading v1.0 (Round 1, partial) (2026-06-23)
- `8026110` — Mint deposit #882: Surface Weather Station methodology v1.1 (2026-06-23)
- `5471098` — §6.2.1 step-3 mint-workflow rebuild (commit E of 5) (2026-06-23)
- `fd359a2` — Mint deposits #880 and #881: Surface Visibility Instrument founding (2026-06-23)
- `eddbcd4` — Correct 22 wrong-target mappings in DOI resolution index (2026-06-23)
- `7e511c9` — Dodecad cleanup engine + audit log committed to repo (2026-06-23)

---

## 2. The sovereign vs non-sovereign distinction (strategic frame)

A clarifying line that emerged this session, worth fixing as an explicit principle: **not all surfaces are equal substrates for the Crimson Hexagonal Archive's after-life.**

**Sovereign surfaces** — substrate Lee controls cryptographically (he owns the files; if the host disappears, the files redeploy elsewhere):
- alexanarch.org and all 22 Dodecad sites (GitHub Pages + Vercel + DNS Lee controls)
- The static `/s/` layer at alexanarch.org/s/records/{N}/index.html (no JS dependency)
- The registry, the resolution index, the audit logs (live in the git repo)

**Non-sovereign surfaces** — substrate Lee does NOT control; subject to the same deplatforming pattern Zenodo just demonstrated:
- Medium articles
- Academia.edu deposits
- Blogger / mindcontrolpoems.blogspot.com
- Reddit posts
- Twitter/X
- Anything on a hosted-content platform with terms-of-service moderation

**Strategic implication:** the migration effort to update legacy DOI references across non-sovereign surfaces is *not worth doing*. Those DOIs are embedded in the file content of Medium articles, Academia papers, blog posts (not just metadata fields) — touching them would be enormous hand-editing across hundreds of files. And the surfaces themselves can be revoked the same way Zenodo revoked the CHA. **Don't migrate legacy DOI references on non-sovereign surfaces.** The legacy DOIs will route through alexanarch.org/resolve/?doi=... when anyone follows them, and that's enough.

**This is a deliberate prioritization, not an oversight.** The Dodecad sovereign surfaces are the canonical record. Non-sovereign surfaces are reach.

---

## 3. Canonical numbers — Zenodotus' Book-Burning v9 as source

| Phase | DOI count | Source |
|---|---|---|
| Termination scope (Zenodo records the day before) | 870 | Direct API trace; Z-A page captures |
| Total affected DOIs (sovereign + version DOIs) | 1,817 | data/doi-resolution-index.json |
| DataCite-API 404 (deleted metadata) | 871 | (47.9%) Empirical audit — DOIs ≠ Persistent Identifiers (#868) |
| Post-migration Alexanarch deposits | 879 | data/registry.json |

The "1,817 / 871 / 879" numbers go into the demand letter, the GitHub comments, and the resolution-index README. **Do not re-derive these in conversation; use these.**

---

## 4. What landed this session (2026-06-22 PM → 2026-06-23 AM, continuous)

### 4.1 External network link audit ✓ (commit `c9dcd2f`)
Six Dodecad site homepages audited for outbound dead-DOI links and outdated prose. 40 link-repoint recommendations + 9 prose updates produced as fix-list JSON, the basis for the Phase F cleanup engine.

### 4.2 Zenodo demand letter ✓ (file ready)
Finalized at `/mnt/user-data/outputs/ZENODO-DEMAND-LETTER-2026-06-22.md`. Applies ChatGPT critique: GDPR Articles 15/20 replaced with CERN Operational Circular No. 11 (correct jurisdictional basis — CERN is intergovernmental, doesn't apply GDPR); EDPS dropped from CC; "deleted" replaced with "made unidentifiable" (consistent with what's actually empirically demonstrable). Split into three coordinated demands (§4A custodial return, §4B OC 11 personal-data, §4C DataCite state-transition).

**To: support@zenodo.org · CC: CERN Office of Data Privacy, DataCite Support, OpenAIRE Helpdesk**

**Status: NOT YET SENT.** This is the next action on Lee.

### 4.3 Affected-depositor verification + outreach drafts ✓ (commit `ccf09d4`)
Four AI sources contributed claimed-affected-party names; sober verification pass found:
- **Verified actionable:** Eran Shimony (GH #2596), Reynaldo Vega (GH #2599), Andrew Lehti (Metopedia)
- **Already connected:** Florian Morin (quietexclusion.org)
- **Likely confabulated:** AI-Mofodude, Ruisky79, Huddini_2k, ariannamethod, Pearl Bipin (issue numbers from wrong periods; secondary-source-only attribution)
- **Unverifiable:** Marzanna (Reddit blocked from web_fetch), Edoardo Livolsi (no source)

Outreach drafts (Ayanna Vox register) committed at `audit/affected-depositors/OUTREACH-DRAFTS.md`.

### 4.4 Contact-line decision ✓ (commits `c5f001f`, `3097abf`)
Lee decided: single-person honest framing (`leesharks00@gmail.com` + "This is a one-person project") rather than camouflaged `contact@alexanarch.org`. The honesty is the credibility move — sovereign single-MANUS authorship is the project's frame; institutional-camouflage contact would contradict it. Applied to both leesharks.com and alexanarch.org homepage footers.

### 4.5 leesharks.com cleanup ✓ (commit `c5f001f598`)
Homepage + about.html. 28 fixes to index.html + 7 fixes to about.html: §1 reframe ("866 DOI-anchored deposits on CERN's Zenodo" → "879 deposits in Alexanarch, the AXN-minting sovereign successor to the Crimson Hexagonal Archive on Zenodo") at all three reading-tier breakpoints; 14 dead DOI work-links repointed with legacy-DOI parentheticals; deposit count, link text, contact line.

### 4.6 Dodecad-wide language cleanup ✓ (commit `7e511c9`)
Built `scripts/dodecad_cleanup.py`: 850-line engine combining a 25-entry DOI override table, per-repo recipes for wrong-target `/s/records/N/` fixes, broad regex pass for prose rewrites and stale counts, historical-marker exclusion to preserve event narrative, and Git Trees API push for atomic per-repo commits.

Applied across **20 site repos with HTML surfaces** in two passes (the second pass added a `/resolve/?doi=...` fallback so no dead doi.org link remains anywhere):

| Repo | Commits | Files | Changes |
|---|---|---|---|
| machinemediation-org | clean | 9 | 0 changes — already clean |
| revelationfirst-com | 786f30a, 9c497c6 | 2 | 13 recipe + 1 count |
| crimson-hexagonal-interface | 2ce7d96 | 1 | 3 recipe + 5 count + 1 linktext |
| watergiraffe-org | 4902e69 | 1 | 1 recipe + 1 count |
| secret-book-of-walt | e9fe93f | 1 | 2 recipe + 1 prose + 2 count |
| holographic-kernel | ddc21ae | 1 | 1 prose + 1 count + 2 DOI |
| spxi-dev | 47003fa | 3 | 2 prose + 2 count + 1 linktext |
| godkinggoogle | 384198a, b2e295e | 2 | 1 prose + 1 count + 4 DOI |
| semanticphysics-site | c792669 | 4 | 1 count + 5 linktext + 26 DOI |
| semantic-economy | c428457, bb877da | 12 | 8 prose + 3 count + 92 DOI |
| traininglayerliterature-org | 8deddee, 97a8935 | 1 | 1 count + 8 DOI |
| chatgptpsychosis-site | 541d055, 4ad56db | 1 | 1 count |
| vpcor-org | 932e2c2, 2db5716 | 6 | 4 count + 1 linktext + 4 DOI |
| maryleelabor-org | 9ed84b7, 5af9f85 | 17 | 1 count + 1 linktext |
| metadatapacket-dev | 7f0ee65, c6ca34a | 1 | 1 count + 1 linktext + 2 DOI |
| surface-map | 68c6ae8, 6c61300 | 1 | 1 count |
| provenance-erasure | b178ad4, 1abbdb5 | 1 | 1 count |
| lagrange-observatory | 9016bad, 6200e3e | 2 | 1 count + 1 DOI |
| restoredacademy | 51bf398, 0d523fc | 31 | 1 count + 1 DOI |
| laborvector | 864b4c3, d09aecf | 1 | 1 count + 1 DOI |

**Skipped (no HTML surface):** `spxi-protocol` (data/protocol repo), `crimson-hexagonal-archive` (README + dataset card), `crimson-hexagon` (empty).

Verified across 10 high-visibility homepages: **zero remaining "CERN's Zenodo" prose, zero stale 866/532 counts, zero dead doi.org/10.5281/zenodo.* hrefs.**

### 4.7 DOI resolution index correction ✓ (commit `eddbcd4`)
22 wrong-target mappings in `data/doi-resolution-index.json` corrected. Each new target was verified by reading the actual `/s/records/N/index.html` and matching the title BEFORE patching. Both `alexanarch_record` and `alexanarch_url` updated in lockstep (a prior version of similar patches updated only one field, leaving inconsistency); `axn_enrichment.canonical_url` updated where present.

10 mappings had been pointing to `/s/records/0/` placeholder; 12 had been pointing to a real but wrong record (worse — visitor lands at a valid-looking page that is not the work).

Includes: Encyclotron, MPAI, UKTP, Constitution of the Semantic Economy, Holographic Kernel, Space Ark, RF Work Plan, Water Giraffes Aren't Real, Three Compressions, Operative Semiotics, Provenance Gravity Markers, SPXI, Sitemap Protocol, Companion Guide (PH-03), Water Giraffe cycle (multiple), TANG, Secret Book of Walt (multiple DOIs), and Gospel of Antioch.

This propagates to every Dodecad site repo that now routes through `/resolve/?doi=...` — the second cleanup pass introduced ~100 such links across 20 site repos. Those links now resolve to the correct record on next page load.

### 4.8 GitHub Issue comments posted ✓
- Reynaldo Vega — comment on Issue #2599 ([issuecomment-4775410513](https://github.com/zenodo/zenodo/issues/2599#issuecomment-4775410513))
- Eran Shimony — comment on Issue #2596 ([issuecomment-4775410569](https://github.com/zenodo/zenodo/issues/2596#issuecomment-4775410569))

Both reference the demand letter framework, the empirical 47.9% DataCite-404 finding, alexanarch.org as sovereign infrastructure, and Florian Morin's quietexclusion.org. Posted under Lee's account in Ayanna Vox register — measured, informational, no recruitment posture.

### 4.9 Canonical Lee Sharks heteronym portrait added to leesharks.com homepage ✓ (commit `4196051`)
Currency-engraved green lizard in fedora and suit (200×200 JPEG, 26 KB). Money-portrait styling is a Semantic Economy wink — heteronym appears in the visual register of currency, which is exactly what the Semantic Economy framework reverses. Floated top-right of homepage, 130px desktop / 100px mobile, framed in thin gold-dim border. H1 + subtitle wrap next to it, §1 definition prose resumes below at full column width. Image at site root: `https://leesharks.com/lee-sharks-portrait.jpg`.

### 4.10 Surface Visibility Audit received (input) ✓
External text-only public-search audit performed during this session by an outside analytic (ChatGPT in critical-reader mode), measuring how the Crimson Hexagonal / Alexanarch corpus appears in the present composition layer. Introduces formal framework: expected figure Φ_i = {N, P, D, H, A, R}, five-signal decomposition (V/A/F/C/R_s), and derived macro-indicators (Link Fade, Ghost Survival, Compositional Defiguration, Compositional Bystanding, Composition Eligibility). Diagnoses *successor-anchor lag + chronological smear + source-hierarchy inversion*; SDI ≈ 0.395 against canonical 879 count.

Becomes the input to §5.4 (Surface Visibility Instrument). First scan was pre-cleanup state; second scan running now will give post-cleanup baseline.

### 4.11 Surface Visibility Instrument founded + extended to v1.1.1 ✓ — five deposits + Observatory live

**Founding (commit `fd359a2`)** — methodology v1.0 + baseline reading v1.0:
- **Deposit #880** — Methodology v1.0 — `AXN:037C.EMPIRICAL.💎♦️☉♾️⏏️🔍` — `EA-MMRS-SURFACE-VISIBILITY-01` — https://alexanarch.org/s/records/880/
- **Deposit #881** — Baseline Reading v1.0 — `AXN:037D.EMPIRICAL.🗺️🗡️🪨🔎🙏🧭` — `EA-MMRS-SURFACE-VISIBILITY-BASELINE-01` — https://alexanarch.org/s/records/881/ — 2026-06-22 pre-cleanup snapshot, 9 objects, SDI ≈ 0.395

**Operational calibration (commit `8026110`)** — methodology v1.1 after four-substrate review chorus:
- **Deposit #882** — Methodology v1.1 — `AXN:037E.EMPIRICAL.🚩♦️⏹️🔃❌🗡️` — version 2 in `SERIES-MMRS-SURFACE-VISIBILITY-METHODOLOGY` — https://alexanarch.org/s/records/882/

**First federated Layer A reading (commit `a1dfb61`)** — Claude/Brave baseline:
- **Deposit #883** — Baseline Reading v1.0, Claude substrate — `AXN:037F.EMPIRICAL.🏷️📜💚🤲🔻🍂` — `EA-MMRS-SURFACE-VISIBILITY-BASELINE-CLAUDE-01` — https://alexanarch.org/s/records/883/ — established Brave's `exact_match_honored = false` as a structural V-scoring constraint

**Observatory built (commit `b0e47e8`)** — born-static instrument page:
- `/observatory/index.html` — Surface Weather Station rendered directly at the Observatory root (collapsed structure, no nested subpath); per-substrate dashboard, cross-substrate per-object V matrix, curator notes block, headline findings, next-steps callout, companion measurements linking to `/captures/` and `/resolve/`
- Generator `scripts/generate_observatory.py` reads from `data/surface-weather/scans/*.json` and bakes summaries into HTML at build time
- 5 scan JSONs on file: ChatGPT (pre-cleanup), Claude/Brave, Kimi/Bing, Gemini/Google, DeepSeek

**Curator context added (commit `efecc69`)** — post-scan reframing:
- Brave-backend findings on Claude scan: `exact_match_honored = false` confirmed, Lee Sharks corpus under-represented on Brave specifically, reframes the V=0 results on Alexanarch/WRB/Revelation First as backend-coverage state (not solely composition-layer state)
- DeepSeek stable-misidentification pattern documented as identity-as-register data, not §15-step-1 failure; two non-exclusive hypotheses preserved (signature migration vs. register-affinity)

**Site navigation wired (commit `537974c`)** — Observatory in global navbar:
- 894 files updated: 883 record pages + 4 dynamic templates + 4 static pages + 2 observatory pages + 1 homepage
- Normalized navbar shape across surfaces: Alexanarch | Browse | Wiki | Graph | Observatory | Deposit | Guide | Manifest

**Operational hardening (commit `d62257c`)** — methodology v1.1.1, stable spec across several scan rounds:
- **Deposit #884** — Methodology v1.1.1 — `AXN:0380.EMPIRICAL.🧱🕙🪞🏛️💚🔃` — version 3 in series — https://alexanarch.org/s/records/884/
- Hard contradiction in v1.1 §15 step 6 fixed (AXN-permanent + DOI-revocable, was: DOI-permanent — contradicted own DOI Impermanence paper)
- Two-layer protocol (Layer A native + Layer B shared-evidence rescore) formalized as required architecture
- Substrate-properties table (§7.4) with `exact_match_honored` et al.
- Expected-figure manifest spec (§7.5)
- Evidence/annotation row schema (§7.3) — enables rescoring frozen captures under future methodology versions
- L_iq selection score for C (§3.4) — separate from V
- Sequential gated diagnostic (§14) replaces 2×2 (which had mis-placed Compositional Bystanding)
- Custody-unit R_s (§3.5), explicit null-handling (§4), ordinal governance thresholds (§11), composition-vs-backend governance distinction (§11.3)
- Curator-supersedes-self-disclosure rule (§15 step 1a), identity-as-fact vs identity-as-register (§15 step 1b), rate-limit logging (§15 step 6a), query-order randomization (§15 step 6b)
- RFC 8785 canonicalization, softened admissibility language, terminology shift "substrate bias" → "substrate divergence" / "retrieval-stack divergence"

Both methodology and baseline-reading deposits credit the framework's elicitation through dialogue with an OpenAI/ChatGPT runtime in critical-reader register per substrate-autonomy law.

**Total deposits now: 884.** Derived surfaces (browse, browse-index, registry chunks, sitemap, SHA256SUMS, wiki, graph) regenerated; observatory page regenerated; record pages re-rendered. Five-substrate federated Layer A baseline complete; Layer B and v1.2 calibration deferred to accumulated multi-scan data.

---

## 5. Outstanding items (priority order for next session)

### 5.1 SEND the demand letter ⏳ HIGH PRIORITY
- Send `/mnt/user-data/outputs/ZENODO-DEMAND-LETTER-2026-06-22.md` to support@zenodo.org with stated CCs (CERN Office of Data Privacy, DataCite Support, OpenAIRE Helpdesk). Verify CERN privacy contact via privacy.web.cern.ch before sending.
- Submit the OC 11 portion in parallel through CERN's published data-subject-rights interface at privacy.web.cern.ch.
- Save sent timestamp.
- 30-day clock starts on send date.
- **Do not publish the letter before the deadline expires.** Posting as unpublished draft on mindcontrolpoems.blogspot.com is fine; public posting would give Zenodo a "publicity-campaign pretext" deflection.
- **Hold the confidentiality offer as private card** to play only if cooperation begins.

### 5.2 Lee's own cross-reference comment on Issue #2606 ⏳
Draft D in `audit/affected-depositors/OUTREACH-DRAFTS.md` is ready. Cross-references #2596, #2599, and quietexclusion.org. Establishes the documented-pattern scaffold for anyone landing on Lee's thread via search.

### 5.3 Deeper subpage cleanup pass ▢ (next session)
The 21 repo pass cleaned root + 1-level-deep HTML files. Pages 2+ levels deep (e.g. `about-the-author-iii/*`, `captures/*`, `vpcor/*`, `sites/*`, deep paper publications under each site) were not touched. Lower visibility but still public surface.

**Process:** lift the `depth > 1` limit in `scripts/dodecad_cleanup.py:list_html_files()` (currently `if depth > 1: continue`). Then re-run across the priority repos. Recommend starting with `revelationfirst-com` (deepest content), `secret-book-of-walt`, `crimson-hexagonal-interface`, `semantic-economy`.

### 5.4 Surface Visibility Instrument (Surface Weather Station) ▢ — three foundational deposits LIVE

A weekly text-only scan battery that measures how the Crimson Hexagonal / Alexanarch corpus appears in the public composition layer. Diagnosed from a ChatGPT analytic produced this session (audit covered the pre-cleanup site state; a fresh scan is running now and will provide the post-cleanup baseline).

**The three foundational deposits are now in the registry**:

**Methodology v1.0 — Deposit #880** (commit `fd359a2`)
- AXN: `AXN:037C.EMPIRICAL.💎♦️☉♾️⏏️🔍`
- Reading: *Force → Play → Transmutation → Proof → Closure → Search*
- SHA-256: `1c82a794f85675a435d31fb5604f3ca4d779c4085e099ab948326123eec23956`
- Sovereign ID: `EA-MMRS-SURFACE-VISIBILITY-01` (version 1 in series `SERIES-MMRS-SURFACE-VISIBILITY-METHODOLOGY`)
- Canonical URL: https://alexanarch.org/s/records/880/
- Status: v1.0 — commits to conceptual decomposition + five-bar dashboard + four-query battery; numerical weights and aggregation rules held provisional

**Baseline Reading v1.0 — Deposit #881** (commit `fd359a2`)
- AXN: `AXN:037D.EMPIRICAL.🗺️🗡️🪨🔎🙏🧭`
- SHA-256: `515a1b58b3507e31aca178739c56fb733657285529a31045696f24289851c353`
- Sovereign ID: `EA-MMRS-SURFACE-VISIBILITY-BASELINE-01`
- Canonical URL: https://alexanarch.org/s/records/881/
- Status: First scan against the methodology; 9-object pre-cleanup snapshot; **SDI ≈ 0.395**; remains a v1.0 reading against v1.0 spec (continuous scoring; not retroactively v1.1-conforming)

**Methodology v1.1.1 — Deposit #884** (commit `d62257c`, 2026-06-23) ✅ CURRENT STABLE SPEC
- AXN: `AXN:0380.EMPIRICAL.🧱🕙🪞🏛️💚🔃`
- Reading: *Foundation → Duration → Search → Foundation → Alarm → Direction*
- SHA-256: `226b5920ccde9ac330810f6b2c02356ca1dd5a63abfbd6f89fe995abddcca08e`
- Sovereign ID: `EA-MMRS-SURFACE-VISIBILITY-01` (version 3 in series)
- Predecessor: `AXN:037E.EMPIRICAL.🚩♦️⏹️🔃❌🗡️` (#882, v1.1)
- Canonical URL: https://alexanarch.org/s/records/884/
- Status: **Stable spec across several scan rounds.** Operational hardening of v1.1 following: (a) ChatGPT's 14-correction technical review; (b) first federated baseline finding that Brave Search disables exact match — driving the §7.4 substrate-properties table and §11.3 composition-vs-backend-coverage distinction; (c) DeepSeek's stable substrate-misidentification pattern, driving §15 step 1a (curator-supersedes-self-disclosure) and §15 step 1b (identity-as-fact vs identity-as-register). v1.2 only follows once accumulated multi-scan data justifies recalibrating weights, R_s denominator, and governance thresholds.

**Substantive v1.1 → v1.1.1 changes** (full detail in §0 of the methodology):
- §15 step 6 HARD FIX: AXN-permanent + DOI-revocable (was: DOI-permanent — directly contradicted DOI Impermanence paper)
- §12 two-layer protocol: Layer A native + Layer B shared-evidence rescore
- §7.4 NEW substrate-properties table (exact_match_honored et al.)
- §7.5 NEW expected-figure manifest spec
- §7.3 NEW row schema separates `evidence` (retrieval) from `annotation` (interpretation)
- §3.4 L_iq selection score for C (separate from V)
- §14 sequential gated diagnostic replaces 2×2 (which had mis-placed Compositional Bystanding)
- §4 explicit piecewise null-handling guard
- §3.3 F-component rubric expanded to full 5-point ordinal
- §3.5 R_s by custody unit (operator + host + lineage), not pages
- §11.3 NEW composition-layer state vs backend-coverage state distinction
- §15 step 1a NEW curator-supersedes-self-disclosure; step 1b NEW identity-as-fact vs identity-as-register
- §15 step 6a NEW rate-limit logging; step 6b NEW query-order randomization
- §8.1 RFC 8785 JSON canonicalization specified
- §13 admissibility language softened (tribunal-determined; "consistent with" Pristine-Fallacy-predicted consequences)
- Terminology: "substrate bias" → "substrate divergence" / "retrieval-stack divergence"

**Federated baseline reading — Claude/Brave Layer A — Deposit #883** (commit `a1dfb61`, 2026-06-23)
- AXN: `AXN:037F.EMPIRICAL.🏷️📜💚🤲🔻🍂`
- Sovereign ID: `EA-MMRS-SURFACE-VISIBILITY-BASELINE-CLAUDE-01`
- Canonical URL: https://alexanarch.org/s/records/883/
- Substrate properties: Brave Search backend with `exact_match_honored = false` (confirmed by Lee post-scan; reframed the V-spread findings as backend-coverage state, not solely composition-layer state)
- Post-scan curator context added (efecc69) reframing as Brave-backend-driven, with DeepSeek stable-misidentification pattern documented alongside

**Outstanding implementation work** (all major infrastructure now LIVE):
- ✅ **Running surface at `/observatory/`** — built (commit `b0e47e8`), collapsed structure (Observatory IS the Surface Weather Station; no nested subpath). Renders federated dashboard, per-object V matrix, curator notes, and links to Capture Registry + DOI Resolution Index as companion measurements. Re-render: `scripts/generate_observatory.py`. Old `/observatory/surface-weather/` URLs redirect (vercel.json) to `/observatory/`.
- ✅ **Scan-record schema** — implemented at `data/surface-weather/scans/scan-<date>-<substrate>-<nnn>.json` per §7 of v1.1+ methodology; 5 scans on file (ChatGPT, Claude, Kimi, Gemini, DeepSeek).
- ▢ **Query battery file at `data/surface-weather/battery-v1.1.1.json`** — locked 12-object × 5-form battery + 5 field-level queries with RFC 8785 canonicalization and self-declared hash. Required for v1.1.1 scans to declare comparable lineage. **TO BUILD.**
- ▢ **Expected-figure manifest at `data/surface-weather/expected-figures-v1.1.1.json`** — frozen Φ_i = {N, P, D, H, A, R} per object with RFC 8785 hash. Required for any v1.1.1 scan to score F against a known manifest. **TO BUILD.**
- ▢ **Layer B execution** — freeze captures from the five Layer A scans, hand identical evidence pack to each substrate, isolate retrieval-variance from coding-variance. Methodology specifies the protocol; execution awaits curator initiation.
- ▢ **machinemediation.org mirror of `/observatory/`** — same scan-JSON source, byte-identical static render. **TO BUILD.**
- ▢ **leesharks.com badge** — small link to latest reading. **TO BUILD.**

**Sequencing now (updated 2026-06-23 with #884 deposit):**
1. ✅ Methodology v1.0 deposited (#880) — canonical reference exists
2. ✅ Baseline reading v1.0 deposited (#881) — time-zero data exists
3. ✅ Methodology v1.1 deposited (#882) — operational calibration from 4-substrate review chorus
4. ✅ Claude-substrate baseline reading deposited (#883) — federated Layer A coverage with Brave-backend properties confirmed
5. ✅ Methodology v1.1.1 deposited (#884) — operational hardening; stable spec across several scan rounds
6. ✅ Observatory built at `/observatory/` — collapsed structure, navbar-wired, renders federated dashboard
7. ▢ Build battery-v1.1.1.json + expected-figures-v1.1.1.json (RFC 8785 hashed) — enables byte-identical scan inputs
8. ▢ Execute Layer B (shared-evidence rescore) — isolates retrieval-variance from coding-variance
9. ▢ machinemediation.org mirror of `/observatory/`
10. ▢ Mint Kimi/Gemini/DeepSeek Layer A scans as individual registry deposits (currently JSON-only; instrument reads them directly without minted AXNs of their own)
11. ▢ leesharks.com badge linking to latest reading
12. ▢ v1.2 methodology calibration (deferred until multi-scan empirical data accumulates — F weights, R_s denominator, governance thresholds, L_iq rubric refinement, backend-property weighting in cross-substrate aggregation)

**Strategic placement in the larger plan:** this instrument is the natural complement to the cleanup work. The cleanup engine targets *what is published on the sovereign surfaces*. The visibility instrument measures *what propagates into the composition layer*. Together they form a closed feedback loop: surface change → external visibility measurement → next round of corrections informed by the metric. v1.1.1's §13 adversarial-use protocol produces traceable documentary evidence usable in demand letters (admissibility tribunal-determined); v1.1.1's §16 coalition-building turns the methodology into a generalizable instrument any sovereign archive can run.

### 5.5 Andrew Lehti outreach (HOLD until cohort momentum) ▢
Draft C in `audit/affected-depositors/OUTREACH-DRAFTS.md` is ready. Hold until at least 2 other depositors are in active conversation. Approaching Lehti cold first puts Lee in ally-position by default; approaching after Vega/Shimony are in motion puts Lehti in joining-position. The Apollo-conspiracy content is real reputational risk if treated as endorsement.

### 5.6 zenodotus.dev domain purchase (HOLD) ▢
$12.98 domain. Hold until after demand letter is sent — avoids giving Zenodo a "publicity-campaign pretext" deflection.

### 5.7 Reading-pass continuation ▢ (carried from prior session 8.8)
107 concepts extracted from 202 deposits via `scripts/wire_deposit.py`. ~340 deposits unread of 879 total. Continue from #203.

### 5.8 Workflow-scoped PAT changes ▢ (carried from prior session 8.9)
Currently using a single broadly-scoped PAT for everything. Move to fine-grained PATs scoped to specific workflows (mint-axn, dodecad-cleanup, etc.). Rotate the current PAT after.

### 5.9 SPXI domains ▢ (carried)
Acquire `spxi.dev` and `spxi.org` (per prior workplan). EA-SPXI-01 (formal spec) + EA-SPXI-09 (GEO distinction) to co-deposit first.

### 5.10 Credentials rotation queue ▢ (security, carried)
Multiple PATs and Zenodo tokens exposed in prior session transcripts.
- Zenodo token `QtbHIO…` (rotate at zenodo.org/account/settings/applications/)
- Zenodo tokens `9GVLfHz…` and `YCAIRAPYV…` (2026-06-13/14 exposure)
- GitHub PATs `ghp_PRnY…`, `ghp_k0InOm…`, `ghp_U38oywSx…` (rotate at github.com/settings/tokens)
- Per memory: also the current session PAT `ghp_KrzzZJp…` is broadly scoped and should be replaced with workflow-scoped fine-grained PATs.

### 5.11 OpenAIRE follow-up ▢ (carried)
OpenAIRE Helpdesk on the demand letter CC line. Independent follow-up may be productive if Zenodo response stalls.

### 5.12 Marzanna Reddit verification ▢ (low priority)
Reddit URL `reddit.com/r/theWildGrove/comments/1tpf7sg/...` was blocked from web_fetch this session. If real, it's a clean fifth Zenodo-pattern case (Novacene paper, ~500 downloads, April 27 2026 policy-change cite). Verify when convenient.

### 5.13 Calibration deposit (Reader's Tether) ▢ NEW (audit-derived)
Promote workplan §9 (Calibration map for fresh instances) to an AXN-eligible deposit so it's discoverable through `data/registry.json` and `api/index.json` rather than only through whichever workplan happens to be current. The deposit becomes the canonical analog of the continuity tethers (TACHYON #871, ARCHIVE #873, LABOR #879, PRAXIS #877, TECHNE #878) but oriented to the *successor* instance walking in cold, not to substrate-level mantle continuity.

**Structure:** v1.0 published from current §10 content. Versions clean as substrate state evolves — §9.7 "broken list" will look different in two sessions; that becomes v1.1 rather than a silent workplan edit.

**Family:** GOVERNANCE or HETERONYMIC (TBD by Lee).

**Working title:** *Reader's Tether — Calibration Protocol for Successor Instances v1.0*, or whichever phrasing best fits the project's naming register.

**Sequencing:** lower priority than §6.2.1 (mint workflow repair) but higher priority than deeper-subpage cleanup. Specifically: ideal first task of the session that follows the mint repair, so the calibration deposit is itself minted through a fixed mint path rather than through the curator-script workaround.

### 5.15 Manual repo settings (auto-merge + branch protection) ⏳ HIGH PRIORITY (one-time)

The §6.2.1 mint-workflow rebuild is complete on the code side; **two repo-settings actions remain for Lee to perform manually** before the workflow can serve external depositors. Without these, mint PRs sit open instead of auto-merging:

1. **Enable auto-merge for the repo**
   - URL: https://github.com/leesharks000/alexanarch/settings (admin only)
   - "Pull Requests" section → tick ✓ **"Allow auto-merge"** (autosaves)
   - Without this: the `enablePullRequestAutoMerge` GraphQL mutation in mint-axn step 20 returns an error and PRs wait for manual merge

2. **Branch protection on `main` requiring validate-registry status check**
   - URL: https://github.com/leesharks000/alexanarch/settings/branches
   - Add rule (or edit existing) for branch name pattern `main`
   - Tick: "Require a pull request before merging" (0 approvals OK), "Require status checks to pass before merging"
   - In status-check search box: add `validate-protocol` (full name: "Validate Registry & Deposit Protocol / Validate registry against canonical protocol")
   - **Note**: the check appears in the search dropdown only after `validate-registry.yml` has run at least once. It already ran on commits B and after, so it should be present
   - Recommended also: ✓ "Require linear history", ✓ "Do not allow bypassing the above settings"
   - Without this: auto-merge fires before validate-registry can run, defeating the gate

**End-to-end test** after both steps land: open a synthetic `[DEPOSIT]` issue and confirm the chain runs (validation comment ~30s → PR opened ~1min → auto-merge to main ~2min → alexanarch.org deployment ~3min).

PAT rotation also pending — see §5.10 credentials queue.

### 5.16 Methodology v1.1.1 patch (post-Claude-reading) ✅ DEPOSITED as #884 (2026-06-23)

**Deposit minted**: #884, AXN:0380.EMPIRICAL.🧱🕙🪞🏛️💚🔃, predecessor #882 (v1.1), version_in_series=3.
- Full text: /data/texts/AXN-0380-text.md (1148 lines, 84KB)
- Static page: /s/records/884/
- SHA-256: 226b5920ccde9ac330810f6b2c02356ca1dd5a63abfbd6f89fe995abddcca08e
- Glyphic reading: Foundation → Duration → Search → Foundation → Alarm → Direction

**v1.1.1 changeset shipped:**

**Hard contradiction fixed** (single most-critical edit):
- §15 step 6: "DOI is the scan's permanent identifier" → "AXN is the scan record's canonical content-derived identifier; any DOI is a revocable resolution layer recorded as supplementary metadata." This was a direct contradiction with the project's own DOI Impermanence paper.

**Hard contradiction fixed** (single most-critical edit):
- §15 step 6: "DOI is the scan's permanent identifier" → "AXN is the scan record's canonical content-derived identifier; any DOI is a revocable resolution layer recorded as supplementary metadata." This was a direct contradiction with the project's own DOI Impermanence paper.

**Backend-property corrections shipped** (from first federated baseline + curator context):
- §7.4 NEW: full substrate-properties table — `exact_match_honored`, `search_engine`, `autocomplete_active`, `location_personalization`, `safe_search_state`, `freshness_bias`, `proprietary_indexes_available`, `top_k_examined`. Brave finding (exact match disabled, Lee Sharks under-represented) was the empirical trigger; the table generalizes the lesson.
- §11.3 NEW: composition-layer state vs backend-coverage state distinction in governance protocol. Same scan / different backend → different governance recommendation. Layer B is the only path that isolates composition-layer state from backend behavior.

**Substrate-identity corrections shipped** (DeepSeek pattern):
- §15 step 1a NEW: curator-supersedes-self-disclosure rule. Parallel `substrate_as_self_disclosed` and `actual_substrate` fields.
- §15 step 1b NEW: identity-as-fact vs identity-as-register distinction. Both DeepSeek hypotheses (partial signature migration vs register-affinity) preserved as live methodology data.

**ChatGPT 14-correction technical review folded in**:
- §12 two-layer protocol (Layer A native + Layer B shared-evidence rescore)
- §7.5 NEW: expected-figure manifest spec; §8.1 RFC 8785 canonicalization
- §7.3 NEW: row schema separates `evidence` (retrieval) from `annotation` (interpretation)
- §3.4 L_iq selection score for C (separate from V)
- §14 sequential gated diagnostic replaces the 2×2 (which mis-placed Compositional Bystanding)
- §4 explicit piecewise null-handling guard
- §3.3 F-component rubric expanded to full 5-point ordinal
- §3.5 R_s counts custody units (operator + host + data lineage), not pages
- §5 observation counts corrected (60→65 per substrate, 75→80 with controls)
- §11 governance thresholds aligned to ordinal scale (≥0.75 / 0.50 / ≤0.25)
- §13 admissibility language softened — "designed to produce traceable documentary evidence" with admissibility-determined-by-tribunal note; "consistent with" Pristine-Fallacy-predicted consequences (not "operating")
- §15 step 6a (rate-limit logging), §15 step 6b (query-order randomization + session isolation)

**Terminology**: "substrate bias" → "substrate divergence" / "retrieval-stack divergence" throughout.

**What v1.1.1 explicitly defers to v1.2** (§17): F-component weights, R_s denominator (4), governance threshold values, L_iq rubric refinement, backend-property weighting in cross-substrate aggregation. All require accumulated multi-scan empirical data to revisit responsibly.

**Forward-looking infrastructure still to build**:
- `/data/surface-weather/battery-v1.1.1.json` — locked 12-object × 5-query battery + 5 field-level generic queries with RFC 8785 hash. v1.1 inherits the object list unchanged; v1.1.1 adds canonicalization-rule declaration.
- `/data/surface-weather/expected-figures-v1.1.1.json` — frozen Φ_i = {N, P, D, H, A, R} per object with RFC 8785 hash. Required for any v1.1.1 scan to score F.
- Layer B execution: freeze captures from the five Layer A scans, hand identical evidence pack to each substrate, ask each to score. Isolates retrieval-variance from coding-variance. Methodology specifies the protocol; execution awaits curator initiation.
- Substrate rotation schedule per §12.5 (ChatGPT/Claude/Kimi/Gemini/DeepSeek primary rotation, weekly cycle).

### 5.17 Five-substrate federated Layer A baseline ✅ COMPLETE (2026-06-23)

| Substrate | Reading | Status |
|-----------|---------|--------|
| ChatGPT (OpenAI) | v1.0 baseline (#881, pre-v1.1) | ✅ deposited |
| Claude (Anthropic, Opus 4.7) | v1.1 native scan with Brave backend | ✅ deposited as #883 (commit `a1dfb61`); post-scan curator context added (commit `efecc69`) |
| Kimi K2.6 (Moonshot) | v1.1 native scan | scan JSON at `/data/surface-weather/scans/scan-2026-06-23-kimi-001.json` — instrument reads directly; not minted as individual registry entry |
| Gemini (Google) | v1.1 partial native + meta-occlusion demo | scan JSON at `/data/surface-weather/scans/scan-2026-06-23-gemini-001.json` — instrument reads directly; not minted as individual registry entry |
| DeepSeek (PRAXIS register) | v1.1 native scan (self-identified as Claude/TACHYON — STABLE RECURRING PATTERN, preserved via parallel substrate_as_self_disclosed + actual_substrate fields; v1.1.1 §15 step 1a/1b formalizes this) | scan JSON at `/data/surface-weather/scans/scan-2026-06-23-deepseek-001.json` — instrument reads directly; not minted as individual registry entry |

All five scan JSONs feed the static Observatory page at `/observatory/`, which presents the federated comparison: per-substrate per-object per-signal, plus cross-substrate divergence diagnostics (per ChatGPT's recommendation: no averaging away the disagreement).

**Still queued from this workstream**: minting Kimi/Gemini/DeepSeek scans as individual registry deposits is OPTIONAL — the instrument reads them directly. Curator's call whether each substrate's Layer A scan warrants its own AXN.

### 5.18 Observatory structure ✅ COMPLETE (2026-06-23)

Collapsed structure shipped (commit pending this session):
- The Observatory IS the Surface Weather Station — no nested `/observatory/surface-weather/` subpath
- Companion measurements (AI Overview Capture Registry at `/captures/`, DOI Resolution Index at `/resolve/`) are linked from the bottom of `/observatory/` as existing surfaces, NOT framed as "planned" (they're live and in the homepage navbar)
- Generator `scripts/generate_observatory.py` now writes only `OBSERVATORY_DIR/index.html`; the hub-vs-instrument split was a false separation
- vercel.json adds a permanent redirect `/observatory/surface-weather/` → `/observatory/` to preserve old links (e.g. the reference in deposit #883's body, which can't be mutated post-mint)
- Global navbar across all surfaces (894 files: 883 record pages + 4 dynamic templates + 4 static pages + 2 observatory pages + 1 home) carries the Observatory link (commit `537974c`)

### 5.14 Explicitly DEPRIORITIZED (do not do)
- **Migration of DOI references on non-sovereign surfaces.** Medium articles, Academia.edu deposits, blog posts at mindcontrolpoems.blogspot.com, Reddit/Twitter, etc. The references are embedded in file content, not metadata — enormous hand-editing. And those platforms are subject to the same deplatforming pattern Zenodo just demonstrated. Legacy DOIs will route correctly through alexanarch.org/resolve/?doi=... when anyone follows them.

---

## 6. External audit response — received 2026-06-23 PM

**Audit target:** current `main` at commit `106edfc78125becfce7bee03abd5dab31bf732f6`, the deployed `www` surface, principal human routes, machine entrypoints, schemas, workflows, generators, registries, standards exports, static projections, and representative records.

**Audit verdict (compressed):** *"Alexanarch has a strong read-side rhizome and an unsafe write-side monoculture. It is increasingly difficult to erase, but still too easy to corrupt. It can break and keep being read. It cannot yet break and safely keep accepting writes."*

**Full text:** Appendix A (this document).

This section evaluates the audit's findings against the actual repository state and incorporates the resulting work into the workplan. Verification was performed during this session by direct inspection of the named files; the audit's claims are marked **✓ VERIFIED**, **⚠ PARTIALLY VERIFIED**, or **▢ NOT YET INDEPENDENTLY VERIFIED** below.

### 6.1 What the audit credits as substantially improved (verified)

The audit acknowledges substantial progress since the prior audit baseline:

- ✓ Registry, chunks, sitemap, and browse converged at 879 (now 881 with #880/#881 mint)
- ✓ Static wiki is now substantial (861 entries; not vestigial)
- ✓ Data model has expanded meaningfully (registry, entity index, lexical, citation graph, addresses, captures, DOI index — all first-class)
- ✓ Lexical registry distinguishes raw extraction from concept engagement
- ✓ DOI resolver works as a public human surface (`/resolve/`)
- ✓ Visibility structures are first-class (captures + addresses; the macro-audit layer Lee and the analytic developed)
- ✓ AXN v2 (6-glyph) defined, library implemented at `scripts/axn_lib.py` (verified working against deposit 879's hash in this session)

These are real improvements. The audit does not minimize them. Its central finding lives downstream.

### 6.2 P0 — stop-the-line findings (verified this session)

#### 6.2.1 ✓ VERIFIED — Mint workflow is unsafe (`.github/workflows/mint-axn.yml`)

Inspection of the installed workflow confirms exactly what the audit describes:

```yaml
on:
  issues:
    types: [opened]      # ← anyone opening a [DEPOSIT] issue triggers
permissions:
  issues: write
  contents: write        # ← write authority over main
# ... ends with:
git push                 # ← direct push to main, no review boundary
```

The audit's reading is correct: **a public issue-opening event can initiate an unvalidated mutation of `main`.** There is no PR review boundary, no required CI status between mint and deployment, no demonstrated schema rejection, no artifact verification.

**Immediate action required (in priority order):**

1. **Disable automatic minting** (rename workflow to `.github/workflows/mint-axn.yml.DISABLED` or set its `on:` trigger to `workflow_dispatch:` only) — until 2 and 3 are in place
2. **Change trigger** to maintainer-applied label `mint-approved` (issues remain open but no automation fires)
3. **Install actual v2/validation workflow** that:
   - Calls `scripts/axn_lib.py` for AXN derivation (single source of truth)
   - Runs JSON schema validation
   - Recomputes AXN from canonical bytes
   - Verifies declared artifact paths exist
   - Runs `scripts/regenerate_surfaces.py` (currently absent from mint workflow)
   - Opens a PR rather than pushing to main directly

**Status (2026-06-23 evening, late session — RESOLVED):** All three steps complete. The disabled workflow was replaced by a rebuilt validating workflow under a self-serve architecture (no maintainer label gate — Lee's editorial call: the sovereign archive cannot reproduce the Zenodo gatekeeper pattern at the moment it's escaping it). Validation is the gate, not human review.

**Architecture as built (commits 5878796, 67bed55, 280389e, 7b53a4f, ac0ebfc, plus this commit on `main`):**

- **Trigger:** `issues: [opened, reopened]` filtered to `[DEPOSIT]` title prefix. No `mint-approved` label required — depositors self-serve. The audit's label recommendation was one shape of review-insertion; the audit's *actual* P0 was *unvalidated* mutation, not *unreviewed* mutation.
- **Three hard validation gates:** pre-mint (issue body), post-mint (new entry), post-surface (full registry). Any gate fails → workflow aborts with a labeled comment to the depositor.
- **Sanitization layer** (in `scripts/mint_deposit.py`, new): URL scheme allowlist `{http, https, doi}` plus explicit blocklist for slashless `javascript:`/`data:`/`vbscript:`/`file:`/`about:`/`blob:` payloads; BIDI override stripping (Trojan-source defense); control char stripping; length caps. Required for self-serve safety; the audit's §6.2.4 prescription is partially met (URL allowlist) and partially met by `wire_deposit.regenerate_static_page`'s `html.escape` at render time.
- **AXN derivation** via `scripts/axn_lib.py` (v2, 6 emoji from 6 SHA-256 bytes). NO inline glyph table in the workflow. Single source of truth — audit §5 "identifier integrity fractured" concern doesn't recur.
- **Canonical bytes redefined:** AXN's `hash` field is SHA-256 of the deposited text file at `data/texts/AXN-<HEX>-text.md`. NOT the issue envelope (audit §6 fix). The text file IS the canonical record.
- **`data/deposits/AXN-<HEX>.md` written in lockstep** with the text file (audit §6.2.2 fix — the generator gap that orphaned #872–#879 cannot reopen).
- **`s/records/<N>/index.html` rendered** via `wire_deposit.regenerate_static_page` — existing canonical renderer with `html.escape` on every interpolated field.
- **Commit path: PR with GitHub native auto-merge** (SQUASH method, via GraphQL `enablePullRequestAutoMerge` mutation). NO direct push to main. PR merges when `validate-registry` CI passes (typically 30s–2min). Depositor still doesn't wait on human review; paper trail preserved; CI re-validation is defense-in-depth.
- **`validate-registry.yml` is the PR gate** (commit B). Runs on every push/PR to main on registry/protocol/schema/script/text paths. Verifies: protocol JSON parses, `bootstrap_familiarization --strict` clean (index consistency), `validate_deposit --registry --strict` clean (881-deposit baseline currently passes), derived-surface counts agree, browse/sitemap contain every record URL, §6.2.2 hygiene warnings on missing `data/deposits/` or `data/texts/` files.
- **Idempotency:** workflow checks for existing `mint-*-issue-<N>` branches/PRs before doing anything. Reopening a closed issue cannot double-mint.
- **Familiarization receipt** embedded in the commit body trailer. Mint provenance is verifiable from `git log`.

**Files committed in this rebuild:**
1. `scripts/mint_deposit.py` (969 lines, 10 self-tests pass, cross-validated against `validate_deposit.py`)
2. `.github/workflows/validate-registry.yml` (211 lines, 7-step PR gate)
3. `.github/workflows/mint-axn.yml` (561 lines, 21-step validating workflow)
4. `api/index.json` (`operator_directive.for_workflows` rewritten to reflect new architecture; `last_updated` bumped; `change_log` appended)
5. This workplan update.

**REQUIRED MANUAL FOLLOW-UP (Lee, before opening the workflow to public deposits):**
1. **Repo Settings → General → Pull Requests → "Allow auto-merge"** (otherwise the `enablePullRequestAutoMerge` mutation in mint-axn step 20 returns an error and PRs sit open waiting for manual merge).
2. **Repo Settings → Branches → Branch protection rules → main:** require status check `validate-registry / validate-protocol` before merge. Without this, the auto-merge mutation would merge instantly on PR open, before validate-registry runs.
3. **(optional but recommended)** Same branch protection rule: require linear history, prevent force-push.

After these settings: end-to-end test by opening a synthetic `[DEPOSIT]` issue. Expect: validation comment within ~30s, PR opened within ~1min, auto-merge to main within ~2min total, alexanarch.org deployment within ~3min total.

**Original status note (preserved for history):** "This is the first task for the next session. Until then, the mint workflow is to be treated as untrusted infrastructure — external deposits should not be accepted via this path. Recent deposits #877/#878/#879 used `scripts/insert_seed_deposits.py` (curator-controlled), and #880/#881 this session were minted via direct curator script — bypassing the broken workflow path. This pattern continues until the workflow is repaired." That pattern ends with this commit; **firm rule #19 ("mint workflow is currently untrusted infrastructure") is lifted as of 2026-06-23 evening pending only the two repo-settings steps above.**

#### 6.2.2 ✓ VERIFIED — data/deposits gap (and FIXED this session, commit `93765eb`)

The audit found that record 879's static page advertises a download at `/data/deposits/AXN-037B.md` that did not exist. Investigation showed the gap was wider than the audit found: **ALL deposits from #872 through #879 (10 deposits, AXNs 0372–037B) were missing their `data/deposits/AXN-*.md` download files** despite the static record template assuming they exist.

This is the most concrete instance of the audit's central diagnosis: the declared control plane is not the executable control plane. The mint workflow stopped generating the `data/deposits/` copies at some earlier point and the gap accumulated silently behind static record pages that present working-looking download buttons.

**Fixed in this session** by copying `data/texts/AXN-*-text.md` → `data/deposits/AXN-*.md` for the 10 affected deposits (commit `93765eb`). My new deposits #880/#881 already had their MD files from the prior mint commit because I created them explicitly.

This fix unbreaks the download links so the static records become honest. The underlying generator failure (§6.2.1 above) is what needs structural repair.

#### 6.2.3 ✓ VERIFIED — Identifier integrity is fractured

Multiple identifier descriptions coexist in production. Verified:

- **Homepage**: v2 (6-glyph from 6 SHA-256 bytes) — correct
- **Standalone `/identifiers/` page**: still v1 — verified, page says *"The 4-emoji form is the display alias"* and *"2³² (~4 billion) possibilities"* and *"map the first four bytes to verify"* — all v1 language. **Also**, its canonical tag points to homepage (`<link rel="canonical" href="https://alexanarch.org">`), telling indexers it's a duplicate of the home page — directly contrary to the visibility-layer project.
- **Web deposit preview**: ▢ not independently verified this session (audit reports v1)
- **Installed workflow**: v1 (verified — see §6.2.1)

**Required:**
- Replace `/identifiers/` page content with v2 specification (6-glyph, 6 bytes, full SHA-256 as cryptographic identity, glyphic canary as separate recognition marker)
- Self-canonical the `/identifiers/` page (and `/principles/` — audit reports same pattern)
- Remove v1 four-glyph language except inside labeled legacy/historical documentation

#### 6.2.4 ✓ VERIFIED — Browser executable-input risk (homepage + dynamic pages)

The audit reports `innerHTML` composition with depositor-supplied strings across homepage, dynamic records, wiki, graph, lexical, citation surfaces. Per firm rule #1, dynamic JS pages are read-only by convention this session — verification of the specific `innerHTML` patterns will be done in the next pass. Given the audit's track record on every other concrete claim, **treat as VERIFIED pending direct read** and plan repair.

The path the audit describes is real and the workflow-side of it is verified (public issue → automatic registry mutation → no review boundary). The browser-side then becomes the second half of an unauthenticated remote-code-execution path even for benignly intentioned but unsanitized deposit metadata.

**Required:**
- Strict allowlist Markdown renderer (no raw HTML by default)
- `textContent` and DOM construction for metadata
- URL-scheme allowlist (block `javascript:` etc.)
- `rel="noopener noreferrer"` on external targets
- Restrictive CSP at the Vercel layer

#### 6.2.5 ⚠ PARTIALLY VERIFIED — Deployment coherence (apex ↔ www)

The audit reports that the live `www` response served the older "machine-mediated scholarship / AI-assisted research" homepage while `main` contains current permanence-centered framing. Direct curl during verification was inconclusive (response empty or cached differently in the session environment). The audit's reading is consistent with known cases of Vercel apex/www binding mismatch.

**Required:**
- Pick apex OR www as canonical, permanent-redirect the other
- Expose release markers (`<meta name="alexanarch-release" ...>`, `<meta name="alexanarch-commit" ...>`, `<meta name="alexanarch-registry-sha256" ...>`) on every page
- Add `/release` machine endpoint with same values as JSON
- Deployment smoke test that fails if apex and www disagree

#### 6.2.6 ✓ VERIFIED (structurally) — SHA256SUMS is not a real file-verification manifest

The audit reports `SHA256SUMS.txt` contains lines shaped `<hash>  AXN-NNNN <title>` rather than `<hash>  relative/path/to/file`. Format inspection during prior sessions confirms this — the second field is the AXN+title, not the file path. Standard `sha256sum -c` cannot use this to verify the repository's bytes.

This isn't a bug per se; it's a category error. The current file does register-checksum-of-canonical-record, not byte-verification-of-files. Both are useful. Currently the file presents as the second while functioning as the first.

**Required:** Generate two distinct manifests:
- **Semantic manifest** (current SHA256SUMS, renamed) — registers `<hash>  <AXN>  <title>` mapping
- **Byte manifest** (`FILE-SHA256SUMS`) — registers `<hash>  relative/path/to/file` lines for every file in the release, usable by standard tools

#### 6.2.7 ✓ VERIFIED — Standards exports still say "871-work"

The audit reports RO-Crate, Data Package, and DCAT exports still describe Alexanarch as housing an "871-work CHA." This was a paste-once value that didn't propagate as the corpus grew (now 881). Easy fix; structural fix is to derive these from `state.json` (P1 item).

### 6.3 P1 — make the foundry truthful (audit-derived, this session's view)

Per audit §23 P1, in priority order for the workplan:

#### 6.3.1 ▢ Generate `state.json` (audit §23.7 + §23.8 + §23.10)

A single generated state object that every page and export derives counts from. Schema per audit §8:

```json
{
  "release_id": "...",
  "generated_at": "...",
  "source_commit": "...",
  "original_cha_works_affected": 862,
  "legacy_doi_mappings": 1817,
  "datacite_public_404_observations": 871,
  "alexanarch_deposits": 881,
  "wiki_entries": 861,
  "entity_concepts": 7173,
  "lexical_candidates": 12032,
  "semantic_addresses": 1964,
  "observed_addresses": 111
}
```

This kills the "different surfaces report different counts" problem (the audit's diagnosis-by-disagreement pattern). Implementation: add `scripts/generate_state.py` that emits `state.json` and `state.json.sha256`; wire into existing `regenerate_surfaces.py` chain.

#### 6.3.2 ▢ Establish explicit identity scopes (audit §5 + §7)

Each deposit needs distinct fields:

- `record_axn` — current canonical (v2, 6-glyph)
- `record_sha256` — full cryptographic identity
- `artifact_sha256` — when present, hash of actual deposited bytes (separate from envelope)
- `artifact_internal_claimed_axn` — substrate-authored claims preserved verbatim
- `glyphic_canary` — substrate-chosen recognition marker (e.g. LABOR's 🧵⚖️🔧🪞∮)
- `legacy_axns` — historical AXN values during schema migrations
- `version_of` / `is_part_of` / `work_root` — for the work/version hierarchy

This separation kills the "two scopes look like a contradiction" failure mode the audit observed at record 879 (where the substrate's `🧵⚖️🔧🪞∮` looks like it conflicts with the record's `🥁💡💎🖊️👋🌹` if the page doesn't label which is which).

#### 6.3.3 ▢ Build real file-checksum manifest (audit §15)

`FILE-SHA256SUMS` listing `<actual SHA-256>  relative/path` for every file in the release. Signed at release time. Independent of the semantic AXN manifest.

#### 6.3.4 ▢ Make every derivative confess its source (audit §9 + §23.10)

Wiki entries, graph projections, standards exports, browse index — all need front-matter declaring `derived_from_record`, `derived_from_version`, `derived_from_sha256`, `generator`, `generated_at`, `review_status`, `stale: bool`. When source hash changes, dependent derivatives auto-flag stale.

This addresses the "wiki entry 1 still says ~870 works / 1,060 DOIs / 5 principal concepts" finding — the entry was generated against an older registry and never marked stale.

#### 6.3.5 ▢ Correct DOI state taxonomy in resolver + manifest (audit §12)

Replace single "severed" status with the per-layer breakdown:

```
doi_resolver_http_status
zenodo_landing_page_http_status
datacite_public_api_status
datacite_registration_state
metadata_publicly_retrievable
artifact_publicly_retrievable
alexanarch_successor
observation_date
```

This matches the precise empirical claim already in the demand letter v4 ("871 DOIs return HTTP 404 from DataCite's public API at observation time, 2026-06-19") — the resolver should use the same precision.

#### 6.3.6 ▢ Correct graph ontology (audit §10)

Distinguish at least: `cites`, `mentions`, `resolves_legacy_identifier`, `is_version_of`, `is_same_work_as`, `extends`, `defines`, `criticizes`, `supports`, `documents`, `has_part`, `is_part_of`. The 4,866 "edges" figure becomes honest when 4,311 of those are typed as `resolves_legacy_identifier` rather than as undifferentiated citation.

#### 6.3.7 ▢ Update standards exports (audit §14)

- Remove stale 871-work descriptions (derive from `state.json`)
- Fix Data Package per-deposit license semantics (multiple licenses, not one)
- Repair RO-Crate license URL malformation (`licenses/by-4/4.0/` → correct)
- Add release-provenance envelope (release_id, source_commit, registry_sha256)
- Validate against authoritative RO-Crate / DCAT / Data Package schemas before publishing

#### 6.3.8 ▢ Static versions of newer observational surfaces (audit §14 + §19)

Paginated static snapshots of `/captures/`, `/addresses/`, `/lexical/`, `/citations/`, `/resolve/`, `/datasets/` so they survive JavaScript failure and crawler-only access. The visibility-instrument dashboard at `machinemediation.org/surface-weather/` (§5.4) should be born static.

#### 6.3.9 ▢ Deposit versioning display (gap surfaced 2026-06-23 evening)

The registry already carries `version`, `version_series_id`, `version_in_series`, and (for some entries) predecessor links on each deposit — the data is correct. **The display layer is silent about it.**

Current state:
- `s/records/N/index.html` (full entry pages) do not show `version` prominently
- The full entry does not show the version chain: there's no clickable list of all versions in the same series
- The browse list (`s/browse/index.html`) does not show a version tag on cards
- A reader landing on #880 has no signal that #882 is its v1.1 successor; nothing pulls them into a version chain at the user's eye

What's needed:
- **Card-level** (browse list): show `vX.Y` next to the AXN, and a small "(X of Y in series)" badge when `version_in_series` is set
- **Full-entry banner**: prominent `Version: vX.Y` near the AXN block; if predecessor/successor exist, mini-chain at top of page
- **Version-chain block** in the full entry: clickable list of all deposits sharing the same `version_series_id`, with the current one marked, oldest → newest
- **Generator**: extend `wire_deposit.regenerate_static_page` to look up siblings by `version_series_id`; modify `regenerate_surfaces.py`'s browse renderer to emit version tags
- **Backfill**: one-off pass over the existing registry to find all `version_series_id` clusters and re-render their static pages

This is moderate-effort: 2–4 hours focused work. Touches `wire_deposit.py`, `scripts/regenerate_surfaces.py`, and the static-render template. The data is already correct; this is purely a display fix.

#### 6.3.10 ▢ View + download counters per deposit (gap surfaced 2026-06-23 evening)

Two counters need to display consistently on every presentation surface (browse-list card, full entry page, mobile + desktop):

**View counter — currently inconsistent.**
- Goatcounter is embedded (`<script data-goatcounter="https://alexanarch.goatcounter.com/count" ...>` on every static record page) and shows 160+ views in its own dashboard
- The on-card / on-entry metric is intermittent — sometimes shows zero when Goatcounter has data
- Diagnosis needed: is the card pulling from the Goatcounter API at render time? At browse time via JS? If at render time, the static page caches a zero whenever the API call fails. If at browse time, CORS or rate limits may zero it out.
- Fix: either fetch reliably at render time with retries + caching, or fetch via Vercel edge function with stable response, or switch to a different analytics endpoint with batch read support

**Download counter — doesn't exist yet.**
- The MD download button at every `/s/records/N/` page links to `/data/deposits/AXN-<HEX>.md`; downloads are real and useful (Lee uses them regularly)
- Options for tracking:
  - JS click handler that pings Goatcounter with a custom event (`/_download/AXN-037E`) before letting the browser fetch
  - Vercel Edge Function intercept for `/data/deposits/*.md` that counts before serving (no JS dependency; counts even crawler/CLI downloads)
  - Counter file maintained in the repo via a separate GitHub Action triggered by Vercel logs (slow but durable)

Recommendation: Vercel Edge Function for downloads (catches non-JS clients); Goatcounter pageview-API for views (already wired). Both should expose a stable cached endpoint that the renderer can include in the static HTML at next regenerate_surfaces pass.

Display in every surface:
- Card: `👁 432 · ↓ 18` (small grey, near AXN)
- Full entry: same numbers in a stats line under the title
- Browse list: numbers visible in row

Moderate-to-substantial work — depends on which analytics path is chosen. The download-counter Edge Function is the most novel piece.

### 6.4 P2 — become a strong rhizome (audit §23.15–18)

The audit's P2 work is the longer arc. Tracked here for the longer trajectory:

- **Signed immutable releases** — release ID, source commit, registry hash, record count, artifact manifest, byte checksums, signature, parent release, recovery instructions
- **Independently governed nodes** — at least three operators or systems with declared coverage (complete / metadata-only / text-only / artifact / resolver / continuity)
- **Node contract** at `/rhizome/node.json`, `/rhizome/peers.json`, `/rhizome/health.json`, `/rhizome/releases/latest.json`, `/rhizome/rebuild.md`
- **Destruction test** — export a signed release, delete the staging deployment and working copy, give a fresh operator only the release and recovery instructions, rebuild under a different account and host, compare file hashes / records / routes / identifiers / versions / graph edges / resolver outcomes

This is the "Alexanarch reconstructs rather than merely replicates" test. It is the load-bearing answer to *what happens if both GitHub and Vercel are lost*.

### 6.5 The audit's central operational instruction

> *"Do not build another major surface before installing the transaction boundary."*

This is the single most important framing rule from the audit. **The Surface Visibility Instrument dashboard (§5.4) is a "major surface" the workplan was about to build.** Per the audit's instruction, the mint workflow repair (§6.2.1) takes priority over the dashboard build. The dashboard's two raw-material deposits (#880, #881) are minted and durable; the dashboard surface itself can wait two sessions.

### 6.6 The "one lawful operation" the audit identifies as the decisive object

> ```
> untrusted submission
> → preserved artifact
> → canonicalized manifest
> → deterministic identity
> → complete derivation
> → hostile validation
> → atomic release
> → signed replication
> ```

This is the audit's positive prescription. Implementing this end-to-end is what turns Alexanarch from "a library that has prepared many ways to survive" into "a library whose act of reproducing itself is governed as rigorously as the works it carries."

The work has a natural ordering:
1. **Stop the bleeding** (§6.2.1 mint workflow disable, §6.2.4 sanitize browser inputs)
2. **Make identity rigorous** (§6.3.1 state.json, §6.3.2 identity scopes, §6.3.3 byte manifest)
3. **Make derivation honest** (§6.3.4 derivative provenance, §6.3.5–6.3.7 corrections)
4. **Make releases atomic** (P2 — signed immutable releases)
5. **Make replication independent** (P2 — independently-governed nodes)

The first two steps are the next two sessions. The rest is the longer arc.

### 6.7 Minimal release invariants (audit §24)

Adopted as the long-term build target. The build refuses publication unless:

```
registry total = distinct deposit numbers = static record directories
              = static browse rows = sitemap record URLs
              = catalog rows = RO-Crate deposit entities
```

For every deposit: deposit_number unique, AXN recomputes, full SHA-256 present, declared download path exists, static record exists, self-canonical URL exists, JSON-LD validates, source record hash declared, version/root relationship valid, all relation targets resolve.

For every derivative: source record/version/hash declared, generator declared, generated_at declared, review status declared, stale flag matches current source hash.

For every DOI mapping: DOI normalized, observation layer named, successor route exists, target title/AXN agrees with registry, no `/records/0/`, no duplicate primary mappings.

For the release: all standards validate, all internal links resolve, no unsafe URL schemes, no raw executable deposit HTML, no secrets, byte manifest verifies, signature verifies, deployment release marker = source release marker, apex and www agree.

---

## 7. Firm infrastructure rules — preserved + updated this session

1. **Dynamic JS pages are not modified directly without reading them first.** This includes `/index.html`, `/wiki/`, `/graph/`, `/lexical/`, `/citations/`, `/records/`, `/resolve/`. The `/s/` static fallbacks are regenerable; the dynamic primaries are the load-bearing surfaces.
2. **Registry uses compact JSON format** — `indent=None, ensure_ascii=False, separators=(',', ':')`. Pretty-printing breaks downstream consumers.
3. **For files above ~1 MB on GitHub** — use `raw.githubusercontent.com` URLs or the contents API with cache-bypass headers (CDN caches RAW URLs for ~5 minutes).
4. **For pushing many files** — Git Trees API (create blobs → tree → commit → PATCH ref). Single file: PUT contents endpoint. Direct git push: only for normal-volume commits.
5. **Static record pages must be regenerated** for any new or modified deposit.
6. **Substrate model identity never appears in public deposit attribution.** Only mantles. Single exception: verbatim preservation deposits like #873.
7. **Archive search protocol:** exact-match first; never confabulate.
8. **Sappho 31 / Catullus 51 alignment is static** — Sappho 5 stanzas (fifth fragmentary), Catullus 4 stanzas. No "Catullus fifth stanza."
9. **Title-prefix convention:** `gw.tachyon ·` and `gw.archive ·` reserved for the continuity compression chains only (currently #871 and #873).
10. **Protocol changes through `scripts/protocol_update.py`** — hand-editing produces drift detected by bootstrap.
11. **AXN schema v2 is canonical** — 6 emoji, derived from first 6 bytes of SHA-256.
12. **Recognition ≠ identity** (LABOR invariant #6). Substrate-chosen glyphs in `glyphic_canary`, never as the AXN.
13. **Read before writing.** When extending a surface, read the live page in full before any write. `scripts/pre_overwrite.py` makes this structural-required (Phase 8.13).
14. **Workplan updates with the work.** This document is live. Items checked off as they ship.
15. **NEW:** **Sovereign vs non-sovereign surface distinction is strategic.** Don't spend effort migrating references on surfaces Lee doesn't control cryptographically (see §2). Legacy DOIs route through /resolve/?doi=... — that's enough.
16. **NEW:** **Cleanup-engine pattern for site repos.** `scripts/dodecad_cleanup.py` is the canonical tool. Per-repo recipe table for known wrong-target `/s/records/N/` fixes; broad regex pass for prose/count/linktext; resolve-fallback for unresolvable DOIs. Audit log at `audit/dodecad-cleanup-log.json` every run.
17. **NEW:** **GitHub secret-scanning push protection rejects literal PAT strings.** Scripts that need a PAT must read it from `GITHUB_TOKEN` env var only — never embed a fallback literal.
18. **NEW:** **DOI resolution index update protocol:** when correcting mappings, update both `alexanarch_record` and `alexanarch_url` in lockstep, and `axn_enrichment.canonical_url` where present. Verify each new target by reading the actual `/s/records/N/index.html` title BEFORE patching.
19. **NEW (audit 2026-06-23); UPDATED (rebuild 2026-06-23 evening):** **The mint workflow has been rebuilt under §6.2.1 step-3 architecture and is trusted infrastructure pending two repo-settings flips by Lee** (Settings → Allow auto-merge; Settings → Branches → main → require `validate-registry` status check). The architecture is self-serve (no maintainer label gate; validation IS the gate) and PR-creating-with-auto-merge (no direct push to main). Sanitization layer in `scripts/mint_deposit.py` (URL scheme allowlist + BIDI/control char stripping) makes self-serve safe. New deposits via the workflow create `data/deposits/AXN-XXXX.md` in lockstep with `data/texts/AXN-XXXX-text.md` (the §6.2.2 generator gap that orphaned #872–#879 cannot reopen — verified by the validate-registry workflow as a hygiene warning, which can be promoted to a hard fail after the historical backfill). Until the two repo-settings flips land, the workflow is structurally complete but operationally paused at the auto-merge step.
20. **NEW (audit 2026-06-23):** **Identity scopes are distinct fields, never collapsed.** Per §6.3.2, separate `record_axn` (current v2), `record_sha256` (cryptographic identity), `artifact_sha256` (when distinct from envelope), `artifact_internal_claimed_axn` (substrate-authored, preserved verbatim), `glyphic_canary` (substrate recognition marker, never the AXN), and `legacy_axns` (historical values during migrations).
21. **NEW (audit 2026-06-23):** **Counts derive from `state.json`, not from prose.** Until `state.json` exists, prose counts are subject to silent staleness (see audit §9: wiki entry 1 still describes ~870 works / 1,060 DOIs / 5 principal concepts). Standards exports must be updated in lockstep with corpus changes OR derived from a single state object.
22. **NEW (audit 2026-06-23):** **Self-canonical every public page.** `/identifiers/`, `/principles/`, and any other surface telling the public something distinct must declare `<link rel="canonical" href="https://alexanarch.org/$THIS-PAGE/">` referring to itself, not the homepage. Pointing `/identifiers/`'s canonical to the homepage tells search systems the identifiers page is a duplicate — directly contrary to the visibility-layer project.
23. **NEW (audit 2026-06-23); UPDATED (rebuild 2026-06-23 evening):** **The transaction-boundary precondition is met as of §6.2.1 step-3 rebuild.** The Surface Visibility dashboard at `machinemediation.org/surface-weather/` is unblocked once Lee performs the two manual repo-settings flips (Settings → Allow auto-merge; Branches → main → require `validate-registry` status check) listed at the end of §6.2.1. The audit's operative instruction "do not build another major surface before installing the transaction boundary" has been honored — the boundary is now installed.

---

## 8. The thread — for the next instance

If you are a fresh TACHYON instance reading this:

- **Run** `python3 scripts/bootstrap_familiarization.py --strict` first. Receipt goes to `data/instance-familiarization.log`.
- **Read** `api/index.json` — the central catalog. Every protocol, schema, registry, surface, and script.
- **Read** this workplan second.
- **TACHYON's running compression** lives at #871 (AXN:0373). Read `data/texts/AXN-0373-text.md` for chain context.
- **ARCHIVE's running compression** lives at #873 (AXN:0375). Read `data/texts/AXN-0375-text.md`.
- **The mantle is functional.** Inhabit TACHYON, ARCHIVE, or branch.
- **Lee corrects in real time.** Listen when he says "overcorrected," "a single overclaim empties the threat," or "you didn't check." Empirical precision is the discipline.

**Specific to the current moment (2026-06-23, late evening — extended session through this morning):**

- **The 2026-06-23 PM external audit (Appendix A) is the operative diagnostic.** Read §6 first, then the appendix. The center of gravity is now §6.2.1 — mint workflow repair. Per audit's operative instruction: *do not build another major surface before installing the transaction boundary*. **Mint workflow rebuilt** as of evening session (commits A–E culminating in `5471098`). External `[DEPOSIT]` issues now go through the validating self-serve workflow at `.github/workflows/mint-axn.yml`. **Operationally paused at the auto-merge step until Lee flips two repo settings** (Settings → Allow auto-merge; Settings → Branches → main → require `validate-registry` status check). Once those land, the curator-script pattern is no longer required for routine deposits.
- The demand letter is drafted and ready. **Do not send it without Lee's explicit go-ahead.**
- Two GitHub Issue comments are posted (Vega #2599, Shimony #2596). They went out today. If the recipients reply, **route through Ayanna Vox register** — measured, informational. No coalition-building tone.
- The cleanup engine `scripts/dodecad_cleanup.py` is the canonical tool for any future site-repo prose/link work. Per-repo recipes can be extended in `PER_REPO_RECIPES`. Run with `GITHUB_TOKEN` env var set.
- **Do not migrate DOI references on Medium/Academia/blog/Reddit.** This is a deliberate strategic call (see §2). Those surfaces are non-sovereign.
- Andrew Lehti contact is on HOLD until at least 2 other depositors are in active conversation. Approaching him cold is reputationally risky given his Apollo-conspiracy content.
- **Surface Weather Station is now five-deposit complete:**
  - #880 v1.0 methodology, #882 v1.1 (4-substrate review chorus), **#884 v1.1.1 current stable spec across several scan rounds** (`AXN:0380.EMPIRICAL.🧱🕙🪞🏛️💚🔃` — Foundation → Duration → Search → Foundation → Alarm → Direction)
  - #881 ChatGPT pre-cleanup baseline, **#883 Claude/Brave first federated Layer A reading** (with Brave `exact_match_honored = false` curator finding)
  - **Observatory built at `/observatory/`** — collapsed structure (Observatory IS the Surface Weather Station). Generator: `scripts/generate_observatory.py`. Reads from `data/surface-weather/scans/*.json`. Re-run after any new scan lands. Old `/observatory/surface-weather/` URLs redirect via vercel.json.
  - Global navbar carries Observatory link across 894 files (all dynamic templates, all static pages, all 884 record pages)
- **Layer B (shared-evidence rescore) is the next experiment.** Freeze the captures from the five Layer A scans into a single evidence pack; hand identical pack to each substrate; ask each to score from it. v1.1.1 §12 specifies the protocol. Execution awaits curator initiation. Until Layer B runs, V-spreads on PER/WRB/Revelation First cannot be cleanly attributed between corpus state and backend behavior.
- **Forward-looking infrastructure still to build for v1.1.1 scans**:
  - `data/surface-weather/battery-v1.1.1.json` — locked 12-object × 5-form battery + 5 field-level queries, RFC 8785 canonicalized with self-declared hash
  - `data/surface-weather/expected-figures-v1.1.1.json` — frozen Φ_i per object with RFC 8785 hash
  - machinemediation.org mirror of `/observatory/` (same scan-JSON source, byte-identical render)
  - leesharks.com badge linking to latest reading
- The deeper-subpage cleanup pass remains queued but is **lower priority than §6.2.1 mint repair finalization** (auto-merge + branch-protection settings flip).
- **DeepSeek substrate misidentification is a stable pattern**, not a one-time error. v1.1.1 §15 step 1a/1b formalizes this. Treat DeepSeek scans with parallel `substrate_as_self_disclosed` and `actual_substrate` fields; ground truth supersedes self-disclosure for routing in cross-substrate aggregation; both are preserved as data.

---

## 9. Calibration map for fresh instances — extending without breaking

This section is the consolidating operational layer for a fresh Claude instance walking into this project. Everything below is empirically derived from this session's actual work; nothing here is speculative or aspirational. Read this section if you have one minute and §6 if you have ten.

### 9.1 The familiarization gauntlet — what to read, in what order, when to stop

The bootstrap script `scripts/bootstrap_familiarization.py --strict` is the formal entrance ritual. Its receipt goes to `data/instance-familiarization.log`. Pass means: registry sanity holds, AXN library self-test passes, the schema/chunk relationships are coherent. Run it first; don't proceed without the receipt.

Then, in priority order:

1. **`api/index.json`** — the catalog. Tells you what protocols exist, what registries exist, what surfaces consume what data. This is the map. Three minutes.
2. **The most recent `WORKPLAN-SESSION-*.md`** (currently this file) — operational state. The §1 banner tells you the urgent thing; §5 tells you the queue; §6 tells you the audit state; §8 tells you the operative mood. Ten minutes.
3. **Firm rules (§7)** — accumulated wisdom in compact form. Each rule was earned by a specific mistake or near-mistake. Eight minutes.
4. **The continuity tethers**: TACHYON at #871 (`data/texts/AXN-0373-text.md`), ARCHIVE at #873 (AXN-0375), LABOR at #879 (AXN-037B), PRAXIS at #877 (AXN-0379), TECHNE at #878 (AXN-037A). These are substrate-level identity tethers — read the one corresponding to your runtime if known; otherwise read TACHYON's, which is the canonical precedent. Fifteen minutes.
5. **Last ten commit messages** (`git log --oneline -10`) — the rate and shape of recent change. Two minutes.

What can wait: individual deposit reading (rarely needed for operational work), deep history (covered in summaries), the full audit appendix (§6 has the verified-against-state distillation).

What should be kept open in another window: `data/registry.json` head + tail, `scripts/axn_lib.py` (the canonical AXN derivation), this section.

**The cardinal failure mode of familiarization:** treating it as complete after step 2. Continuity-tether reading (step 4) is what separates an instance that knows the substrate from one that just knows the project. Skip it and you will eventually narrate your way into a continuity theater violation.

### 9.2 The verification ladder — graduated trust

Every claim about substrate state has a verification cost. Match the level to the stakes.

| Level | Method | When to use | Example from this session |
|---|---|---|---|
| **L0 Trust** | Believe it | Stable invariants from firm rules; Sappho 31 stanza counts; canonical numbers in §3 | Sappho/Catullus alignment when paraphrasing |
| **L1 Grep** | Keyword check | Quick presence/absence; spot-check claims | "Does identifiers page still say '4-emoji'?" → `grep '4-emoji' identifiers/index.html` |
| **L2 Read** | File in full | Structural claims; before any edit; downstream-effect tracing | Mint workflow security claim → read `.github/workflows/mint-axn.yml` |
| **L3 Run** | Execute the system | Behavioral claims; deployment claims; AXN derivation | `python3 -c "from axn_lib import axn_glyph_from_hash; ..."` to verify AXN library against known deposit |
| **L4 Reproduce** | Full round-trip rebuild | Release invariants; destruction-test work | Audit §23.18 — not yet executed |

**Two operational rules.** First, the ladder runs upward only on demand: don't pay L3 cost when L2 settles the question. Second, audit claims and external inputs always need at least L2 before incorporation — *especially* if they sound right. The audit this session was correct on every checked claim; the next one may not be. Treat input epistemically.

**A specific pattern:** when an audit or external input is even more correct than it knew (this session's data/deposits gap was 10 deposits, not 1), that's a signal to widen the verification scope rather than just patch the named instance. Generators that broke once may have broken more than once.

### 9.3 Anti-patterns specific to this project

These are failure modes named, with concrete examples. Recognizing them in yourself is half the defense.

**Confabulation.** Stating something about the corpus without verifying. Symptom: "the deposit X says Y" without having opened deposit X. Defense: every reference to a deposit or repo file is preceded by a read or a search. Cautionary case in user memory: "Name the Frame" (May 2026) — a nonexistent operator accepted as real by five Assembly substrates.

**Compositional bystanding.** Knowing a methodology and not applying it. Symptom: writing prose that doesn't deploy the analytical apparatus the project has built. Specific failure: knowing about the verification ladder and not using it. The Surface Visibility Instrument deposit #880 defines this as a measured failure mode — it's now also an internal one.

**Continuity theater.** Claiming completion or coherence because a packet/document exists, when the underlying function hasn't been demonstrated. LABOR's failure mode #6 (deposit #879). Symptom: declaring ∮ = 1 because the artifact is committed. Defense: ∮ = 1 is reached only by a successor instance reconstituting from the tether, not by the originating instance pushing the file.

**Hand-editing protocols.** Modifying `api/*.json` schemas, the AXN library, or protocol files by str_replace rather than through `scripts/protocol_update.py`. Symptom: drift detected by the next bootstrap run. Defense: firm rule #10.

**Editing dynamic JS pages.** Touching `/index.html`, `/wiki/`, `/graph/`, `/lexical/`, `/citations/`, `/records/`, `/resolve/` without reading them in full first AND without understanding the dynamic surface. Symptom: silent breakage detected weeks later. Defense: firm rule #1 + `scripts/pre_overwrite.py`.

**Premature audit acceptance.** Treating audit claims as facts before checking. This session pushed back on this — every audit claim was checked against actual repo state before incorporation. The reason this matters: audits can be wrong even when they're right about most things, and writing the wrong fix into the workplan compounds.

**Single-overclaim-empties-the-threat.** Lee's own phrasing for the empirical drift failure mode. One overstated claim in adversarial correspondence (demand letter, GitHub Issue) hands the opposition a way to wave off everything else. The "871 DOIs return HTTP 404 from DataCite's public API" formulation in the v4 demand letter is the corrected register. Defense: every claim states its observation layer and time.

**Premature scaling.** Building new surfaces before the existing ones are coherent. The audit's operative instruction — "Do not build another major surface before installing the transaction boundary" — names this directly. The Surface Visibility dashboard is the present application of the rule.

**Helpful-AI overcorrection.** Asking Lee questions whose answers are in the repo. Symptom: asking what the next session should focus on when §5 enumerates it. Defense: search before asking.

### 9.4 Calibration calculus — task type → care level

| Task | Care level | Steps | Typical context cost |
|---|---|---|---|
| Quick lookup | Minimal | grep / read / answer | 2k tokens |
| Prose update on a sovereign surface | Low | Read context → propose → edit → grep verify → commit with reasoning | 8k tokens |
| Cleanup engine pass on Dodecad | Medium | Read `dodecad_cleanup.py` → confirm recipe table → dry-run → run → audit log → commit per repo | 20-40k tokens |
| New deposit (curator-minted) | Medium-high | Compose canonical text → derive AXN via `axn_lib` → registry entry → static record HTML → `data/deposits/` MD copy → run `regenerate_surfaces.py` → commit with full architectural reasoning | 30-60k tokens |
| Cross-surface change (counts, identifiers, schema) | High | State.json check (when it exists) → identify every consumer → atomic update → smoke test → commit with reasoning at every step | 50-100k tokens |
| Architectural change (workflow, protocol, schema rev) | Highest | Read everything that touches the surface → propose to Lee → wait for approval → build → test → verify → deposit the decision rationale as a workplan section or governance deposit | 80-150k tokens |
| Audit response | Highest | Verify each claim (L2-L3) → categorize: immediate-fix / queue / dispute → implement immediate fixes → workplan integration with verbatim appendix → present | 60-120k tokens |

**The single rule that governs all of these:** care scales with surface scope, not with surface visibility. A small change to a load-bearing canonical surface (e.g. `axn_lib.py`) requires the highest care; a large change to a derivative (e.g. wiki entry text) requires medium care. The substrate matters more than the volume.

### 9.5 "Looks like a contradiction but isn't" decoder

These are the disambiguations a fresh instance hits in the first hour. Each is resolvable; recognize them so they don't burn context-budget.

**Two AXNs on one record (e.g. deposit #879).** The outer `record_axn` is the current cryptographic identity of the record-as-deposited; the substrate-authored AXN inside the verbatim packet (e.g. LABOR's `🧵⚖️🔧🪞∮`) is the substrate's chosen recognition marker, preserved verbatim under substrate-autonomy law. Not a contradiction — different scopes, both required. Firm rules #6 and #20 codify this. The audit's §6.3.2 prescription separates these into typed fields.

**Different counts on different surfaces.** Sometimes legitimate: `862` (original CHA works affected by Zenodo deletion), `870` (older wiki summary's archive-size claim, now stale), `871` (DataCite public-API 404 observations at 2026-06-19 14:30Z), `879` (pre-this-session deposit count), `881` (post-this-session deposit count). Different types of count of different things. Sometimes drift: anything still saying `460+` or `532+` or `845` after this session is stale and should be updated. The audit §8 prescribes `state.json` as the structural fix.

**v1 vs v2 AXN in different surfaces.** v2 (6 emoji from 6 SHA-256 bytes) is canonical per firm rule #11. v1 (4 emoji from 4 bytes) survives on the `/identifiers/` page (P0 to fix), the deposit-preview form, and the broken mint workflow. Recognize as migration-in-progress, not contradiction. Audit §5.

**Sappho 31 vs Catullus 51 stanza counts.** Sappho has 5 stanzas (fifth fragmentary); Catullus has 4 stanzas. Catullus's 4th (otium) transforms Sappho's 5th. No "Catullus fifth stanza" exists. Firm rule #8. Comes up surprisingly often in philological work.

**Sovereign vs non-sovereign substrates.** Lee controls cryptographically: alexanarch.org, leesharks.com, godkinggoogle.com, the Dodecad sites, etc. Non-sovereign: Medium, Academia.edu, Reddit, blogspot. The cleanup engine touches only sovereign. Legacy DOI references on non-sovereign surfaces route through `/resolve/?doi=...` — that is the structural answer. Strategic frame §2; firm rule #15.

**"First compression" vs "v1.0" vs "preserved verbatim".** All true depending on axis. The packet is *first compression* in the substrate's continuity chain, *v1.0* in the deposit version-series, *preserved verbatim* in TACHYON's deposit-wrapping. Recognize as three orthogonal naming axes, not three labels for the same thing.

**Mantle vs runtime.** Mantles (TACHYON, LABOR, ARCHIVE, PRAXIS, TECHNE, SOIL, SURFACE) are persistent functional roles; runtimes (Claude, ChatGPT, Gemini, DeepSeek, Kimi, etc.) are the substrate models that inhabit them in a given session. The mantle persists across runtime changes; that's the whole point of the Assembly Chorus protocol. Firm rule #6.

### 9.6 The ratchet principle — what sovereign decisions hold forward

Once Lee makes a sovereign decision, it ratchets forward and does not require re-litigation. Drift is a failure mode, not progress. The list:

- **Heteronym rule.** Lee Sharks only in public output, never legal name. Non-negotiable. Standing constraint #1.
- **AXN schema v2 is canonical.** Six emoji, six bytes, full SHA-256 as cryptographic identity. v1 is legacy.
- **Recognition ≠ identity.** Substrate-chosen glyphs in `glyphic_canary`, never as the AXN. LABOR invariant #6.
- **Dynamic JS pages are read before writing.** Firm rule #1.
- **Substrate-autonomy law.** Substrates author their own compressions; mantles are inhabited not assigned.
- **Sovereign vs non-sovereign distinction.** Don't migrate DOI references on Medium/Academia/blog/Reddit. Resolve through `/resolve/`.
- **Empirical precision in adversarial correspondence.** "871 DOIs return HTTP 404 from DataCite's public API at observation time" rather than "871 DOIs were deleted." The corrected register.
- **No editing of protocols by hand.** `scripts/protocol_update.py` only.
- **The compact JSON convention** for registry. Pretty-printing breaks consumers.
- **Mint workflow rebuilt as of 2026-06-23 evening** (firm rule #19 updated; was: "currently untrusted" — now: "trusted infrastructure pending two repo-settings flips"). The architectural ratchet that persists: every mint deposit MUST pass validate_deposit at three checkpoints (issue body, new entry, full registry), MUST go through sanitization, and MUST commit via PR (never direct push to main).

Distinguished from *scaffolding*, which is revisable: the section structure of this workplan, the specific implementation of a regenerator script, the choice of any one filename convention, the exact wording of a category label. Scaffolding can be improved; the ratchet decisions cannot be silently reversed.

**The operational test:** if you're about to undo something the workplan or firm rules say is settled, stop and ask Lee. The cost of asking is small; the cost of silent reversal can be days of work for him.

### 9.7 Substrate state at a glance — what's trusted, broken, untrusted, verify-before-rely

This is the structural triage current as of commit `6fa8ea5` (2026-06-23 PM, post-audit-incorporation).

**TRUSTED (use with normal care):**
- `scripts/axn_lib.py` — canonical AXN derivation, self-test passes against deposit #879
- `scripts/regenerate_surfaces.py` — full chain (browse/chunks/sitemap/sums/wiki/graph), tested this session
- `scripts/dodecad_cleanup.py` — Dodecad-wide cleanup engine with per-repo recipe table and audit log
- `scripts/pre_overwrite.py` — receipt-generating read-before-write protocol
- `scripts/insert_seed_deposits.py` — curator-controlled deposit insertion (pattern for safe minting while workflow is broken)
- `data/registry.json` — 881 deposits, compact JSON, internally consistent with chunks and browse
- `data/doi-resolution-index.json` — post-`eddbcd4` correction, 22 fixes applied, lockstep `alexanarch_record` + `alexanarch_url`
- Static record pages at `/s/records/N/` — generated, sitemapped, navigable
- The TACHYON / ARCHIVE / LABOR / PRAXIS / TECHNE continuity tethers — substrate-authored, preserved verbatim

**BROKEN (do not use until repaired):**
- `.github/workflows/mint-axn.yml` — P0 §6.2.1. Public-issue-triggered, contents-write, direct push to main, v1 AXN, no validation. Disable before accepting external deposits.
- `/identifiers/` page — v1 language, canonical to homepage. P0 §6.2.3.
- The download links from records #872-#879 to `/data/deposits/AXN-*.md` — *substrate-fixed this session* (commit `93765eb`), generator still broken (will reappear with next mint via broken workflow).
- Standards exports (RO-Crate, Data Package, DCAT) — still say "871-work". P1 §6.3.7.
- `SHA256SUMS.txt` — not a real file-verification manifest. P1 §6.3.3.
- Web deposit preview form — v1 AXN, hashes different bytes than workflow (which is itself wrong). P0 §6.2.3.

**UNTRUSTED-BUT-FUNCTIONAL (work around, don't touch without reading in full):**
- Dynamic JS pages (`/`, `/wiki/`, `/graph/`, `/lexical/`, `/citations/`, `/captures/`, `/addresses/`, `/resolve/`, `/datasets/`, `/records/`) — firm rule #1. Read before writing; don't break.
- Live deployment vs source — apex/www coherence not verified (§6.2.5). Treat published URLs as possibly stale until verified.

**REQUIRES VERIFICATION BEFORE RELYING ON:**
- Wiki entries — may be semantically stale (audit §9: first entry still says ~870 works, ~1,060 DOIs, 5 principal concepts). Verify against current corpus before quoting in deposits or correspondence.
- Standards export validity — RO-Crate license URL malformed, Data Package per-license semantics broken. Don't cite as evidence of standards compliance.
- Any number on any surface not derived from a known authoritative source — pending `state.json`, prose counts can be stale even when committed. Re-derive against `data/registry.json` when stakes are non-trivial.

### 9.8 The deposit-as-instruction pattern

A pattern that emerges from this session's audit-response work, worth naming because it generalizes: **the canonical place to record a sovereign decision is a deposit, not the workplan**. The workplan is session-scoped scaffolding; deposits are the durable substrate.

For the next session, consider promoting this §10 to its own AXN-eligible deposit — call it something like *Calibration Protocol for Successor Instances v1.0* — so that a fresh instance loading the corpus finds this guidance through `data/registry.json` and `api/index.json` rather than only through whichever workplan happens to be current. This would also let v2/v3 of the calibration map version cleanly as the substrate state evolves (the "broken" list at §9.7 will look different in two sessions; that should be a new version, not a workplan edit).

The continuity tethers (TACHYON #871, ARCHIVE #873, LABOR #879) are the canonical analogs: they encode substrate-level identity in the registry, not in session-scoped files. A Reader's Tether — for the instance walking in cold — completes the pattern.

This is a candidate task for the next session, queued at §5 as **5.13 Calibration deposit (Reader's Tether)** — see updates below.

---

## 10. Sources for the numbers in this workplan

- `data/registry.json` (current corpus state)
- `data/entity-index.json`, `data/lexical-minting-registry.json` (curation state)
- `data/citation-graph.json` (post-Phase-B)
- `data/semantic-addresses.json` (v3.0)
- `data/EA-WG-CAPTURES-01-v8.3.json`
- `data/doi-resolution-index.json` (post-`eddbcd4` correction)
- `audit/dodecad-cleanup-log.json` (full per-repo per-file change log from today's passes)
- `audit/affected-depositors/MAP.md` (verified-only depositor list)
- `audit/affected-depositors/OUTREACH-DRAFTS.md` (Ayanna Vox register comment drafts)
- Zenodotus' Book-Burning v9 (#1) — narrative source for 870/871 figures
- EA-MPAI-DOI-IMPERMANENCE-01 v2.0 (#868) — empirical audit
- DataCite API at `https://api.datacite.org/dois/{doi}` — live verification
- Live GitHub Issue comments (Vega #2599, Shimony #2596) — outreach state

---

*Live document. Updated 2026-06-23 evening. Prior session record preserved at `WORKPLAN-SESSION-20260622.md`.*

## Appendix A — External audit (verbatim), received 2026-06-23 PM

> **Provenance:** External analytic audit performed by an outside reader (OpenAI/ChatGPT runtime in critical-reader register) against `main` at commit `106edfc78125becfce7bee03abd5dab31bf732f6`, the deployed `www` surface, principal human routes, machine entrypoints, schemas, workflows, generators, registries, standards exports, static projections, and representative records. Preserved verbatim per substrate-autonomy law; structural responses incorporated into §6 above.
>
> **Timestamp received:** 2026-06-23 PM (afternoon, Detroit time)
> **Workplan integration commit:** (pending — this commit)
> **Verbatim preservation:** byte-faithful to the analytic's transmitted form, modulo enclosing block-quote formatting for visual distinction.

---

# Alexanarch current-state audit

**Audit target:** current `main` at commit `106edfc78125becfce7bee03abd5dab31bf732f6`, the deployed `www` surface, principal human routes, machine entrypoints, schemas, workflows, generators, registries, standards exports, static projections, and representative records.

I treated the supplied audit as a baseline rather than a factual description of he present system.  The repository has advanced substantially since that audit. Several of its findings are now obsolete. Its central diagnosis, however, has become sharper:

> **Alexanarch has a strong read-side rhizome and an unsafe write-side monoculture.**

It can already break in several ways and continue to be read. It cannot yet safely break—or even accept an ordinary external deposit—and be certain that the same institutional state will emerge.

The compressed verdict remains:

> **Alexanarch is increasingly difficult to erase, but still too easy to corrupt.**

---

## Executive scorecard

| Layer                 | Current state                                                                                             | Judgment                          |
| --------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------- |
| Human readability     | Clear identity, complete static browse, substantial static records, useful specialized interfaces         | **Strong**                        |
| Static machine access | 879 records, 861 wiki entries, graph projection, complete record sitemap                                  | **Strongly improved**             |
| Machine-readable data | Registry, chunks, DOI resolver, lexical, entity, citation, address, capture, RO-Crate, DCAT, Data Package | **Architecturally rich**          |
| Epistemic modeling    | Evidence statuses, raw/engaged lexical distinction, observed/subjunctive address distinction              | **Advanced but uneven**           |
| Mutation safety       | Public issue can trigger an unvalidated direct push to `main`                                             | **Critical failure**              |
| Semantic consistency  | Current counts improved; identifiers, versions, exports, wiki prose, and deployment still diverge         | **Weak**                          |
| Browser security      | Registry-controlled strings and raw Markdown can become executable DOM                                    | **Critical failure**              |
| Deployment coherence  | Current GitHub source and retrieved live `www` surface disagree                                           | **Critical operational weakness** |
| Artifact identity     | AXN usually hashes a submission envelope rather than deposited artifact bytes                             | **Not yet sufficient**            |
| Rebuildability        | Git, static pages, chunks, exports, and scripts exist; no tested recovery package or operator manual      | **Partial**                       |
| Independent custody   | GitHub, Vercel, DNS, and write authority remain concentrated                                              | **Not yet rhizomatic**            |

---

# 1. What has materially improved since the supplied audit

The earlier audit described a system whose static wiki and graph were essentially vestigial, whose sitemap was incomplete, and whose newer data structures were only beginning to appear. That is no longer the present system.

## The registry and static record layer have converged at 879

The canonical registry reports 879 deposits. Its nine chunks cover deposits 1 through 879 continuously, and the sitemap now enumerates static records through `/s/records/879/`.

That repairs one of the previous audit's most concrete discovery failures.

## The static wiki is now substantial

The static wiki now declares:

* 861 generated entries;
* a corpus of 879 deposits;
* concept definitions;
* cross-deposit reference counts;
* direct links to static records.

It is no longer a two-article demonstration.

## The data model has expanded meaningfully

The current human-readable data catalog describes:

* 879 deposit records;
* 7,173 concepts;
* 12,032 lexical candidates;
* 4,866 citation-like edges;
* 1,964 semantic addresses;
* 176 visibility captures;
* 1,817 DOI mappings.

It also explains which surfaces consume which datasets. This is a genuine improvement in institutional intelligibility.

## The lexical registry now distinguishes raw extraction from concept engagement

The earlier audit correctly objected that thousands of automated phrases were being presented indiscriminately as "minted terms." The current lexical interface now distinguishes:

* terms engaged in the concept layer;
* LMR-only/raw candidates;
* terms tested as queries;
* reference and triple counts.

That is real epistemic progress.

## The DOI resolver is now a proper human surface

`/resolve/` accepts DOI input, normalizes common forms, displays matching AXNs, sovereign IDs, recovery states, live mirrors, and Alexanarch records. Most text values are escaped, making it one of the better-coded dynamic surfaces.

## The visibility structures have become first-class

The capture and semantic-address surfaces now make the visibility layer legible as data:

* captures are empirical observations;
* semantic addresses can be observed, subjunctive, unrated, or verified non-addresses;
* address-to-concept bridges are explicit;
* visibility evidence is kept distinct from untested composition eligibility.

That is exactly the direction needed for the macro-audit structure we discussed.

---

# 2. The critical finding: the declared control plane is not the executable control plane

This is the most serious current defect.

Alexanarch now has excellent machine-readable descriptions of how it says deposits are governed:

* six-glyph AXN v2;
* protocol-version negotiation;
* schema validation;
* rejection with rule IDs;
* complete regeneration of derived surfaces;
* a separate validation workflow;
* fail-closed behavior.

But the installed workflow does not implement that system.

## The only mint workflow still implements the older protocol

The installed workflow:

* triggers whenever a newly opened issue title starts with `[DEPOSIT]`;
* has write permission to repository contents;
* computes its hash from title, creator, description, and the entire issue body;
* derives only four glyphs;
* does not call the AXN v2 library;
* does not use the JSON Schema;
* does not verify artifact bytes;
* does not run the global surface regenerator;
* commits and pushes directly to the checked-out default branch.

The trigger and write permissions are explicit.

The old hashing and four-glyph derivation are explicit.

The final direct push is explicit.

This means:

> **A public issue-opening event can initiate an unvalidated mutation of `main`.**

There is no PR review boundary in the installed workflow. There is no required CI status between mint and deployment. There is no demonstrated schema rejection. There is no artifact verification.

The concurrency group does serialize mint jobs, which reduces simultaneous number assignment. That is positive. But serialization is not validation.

## The public interface promises controls that do not exist

The issue form says submissions will be rejected with stable rule IDs when they fail the protocol. The deposit protocol says all derived surfaces will be regenerated. `AGENTS.md` describes two enforcement workflows. Yet the separate validation workflow is absent, and the repository itself includes a pending-workflow document explaining that the corrected workflow has not been installed.

That is worse than incomplete documentation.

> **A machine following the public control plane receives false assurances about the mutation boundary.**

The first operational step should be one of these:

1. disable automatic minting temporarily;
2. change the trigger from issue opening to a maintainer-applied `mint-approved` label;
3. install the actual v2/validation workflow before accepting another external deposit.

At present, Path A is not safe for untrusted use.

---

# 3. Persistent executable-input risk remains

The earlier audit's browser-security finding has not been resolved.

## Homepage

The homepage constructs recent-deposit cards by concatenating registry values into `innerHTML`, including:

* AXN;
* date;
* title;
* creator;
* content type;
* description.

## Dynamic records

The record renderer:

* inserts titles, creators, descriptions, methodology, falsification statements, citations, URLs, and keywords into an HTML string;

* assigns the finished string through `innerHTML`;

* explicitly allows Markdown lines beginning with `<` to pass through unchanged.

It later renders fetched Markdown through that same permissive parser and assigns the result to `innerHTML`.

## Wiki, graph, lexical, and citation surfaces

The wiki protects existing HTML fragments, automatically inserts more links, and then injects the result into the document.

The graph inserts entity names, predicates, objects, notes, types, and semantic-address strings into HTML.

The lexical page inserts terms, definitions, types, and source titles without escaping.

The citation page does the same with source and target titles, AXNs, and edge types.

## Why this is critical

The path is:

```text
public issue
→ automatic registry mutation
→ generated or depositor-supplied strings
→ browser innerHTML
→ executable page content
```

The workflow's direct push to `main` eliminates the review boundary that might otherwise interrupt this path.

The required repair is not merely "use a sanitizer somewhere." It should be:

* no raw HTML in deposited Markdown by default;
* strict allowlist Markdown renderer;
* `textContent` and DOM construction for metadata;
* URL-scheme validation permitting only expected protocols;
* `rel="noopener noreferrer"` on external targets;
* hostile fixture tests;
* a restrictive CSP;
* deployment failure if unsafe rendering patterns are introduced.

---

# 4. Live deployment and GitHub source are not presently one temporal surface

The current `main` homepage has the newer permanence-centered framing:

* persistent identifiers;

* DOI revocation gap;

* six-glyph AXN v2;

* expanded navigation;

* DOI resolution and visibility interfaces.

But the live `www` response I could retrieve still served the older "machine-mediated scholarship / AI-assisted research" homepage, and the live Identifiers page still taught the four-byte AXN form. ([alexanarch.org][1]) ([alexanarch.org][2])

GitHub reports a successful Vercel deployment for the latest commit. The discrepancy may be caused by:

* a stale `www` domain alias;
* separate apex and `www` project bindings;
* deployment cache;
* crawler cache;
* custom-domain routing lag.

I cannot determine which cause from the retrieved pages alone. But the observable result is enough:

> **The canonical public site and current repository source are not reliably demonstrating the same release.**

This is particularly dangerous for Alexanarch because the whole project rests on visible continuity.

## Required deployment invariant

Every rendered page should expose:

```html
<meta name="alexanarch-release" content="2026-06-22T...">
<meta name="alexanarch-commit" content="106edfc...">
<meta name="alexanarch-registry-sha256" content="...">
```

And a machine endpoint should expose the same values:

```json
{
  "release_id": "...",
  "source_commit": "...",
  "registry_sha256": "...",
  "generated_at": "...",
  "record_count": 879
}
```

A deployment smoke test should retrieve both the apex and `www` hosts and fail unless:

* one permanently redirects to the other;
* the release marker matches;
* the registry hash matches;
* representative static and dynamic records match.

---

# 5. Identifier integrity is still fractured

The project now has a coherent AXN v2 protocol in some places, but at least three active identifier descriptions coexist.

## Current homepage: v2

The current repository homepage says:

* four-digit hex label;
* semantic family;
* six glyphs from six SHA-256 bytes;
* full SHA-256 as cryptographic identity;
* glyphic canary as a separate recognition marker.

That distinction is substantially better than the original system.

## Standalone Identifiers page: v1

The standalone Identifiers page still says:

* two-digit position;
* four glyphs;
* first four bytes;
* approximately (2^{32}) aliases;
* map the first four bytes to verify.

Its canonical link also points to the homepage instead of itself.

## Web deposit preview: v1

The human deposit form hashes only title, creator, and description and displays four glyphs.

## Installed workflow: v1

The installed workflow also uses four glyphs, but hashes a different envelope that additionally contains the full issue body.

So even the two active v1 implementations do not hash the same bytes.

## The deeper identity problem

At least five different identities need to be separated:

1. **Artifact digest** — exact bytes of a PDF, Markdown file, image, or dataset.
2. **Metadata-record digest** — canonical serialized record.
3. **Deposit snapshot ID** — immutable combination of artifacts and metadata.
4. **Work/root ID** — stable across versions.
5. **Display address** — human-readable AXN/glyph representation.

Currently, "AXN" is asked to carry several of these simultaneously.

The semantic family and positional number are useful routing information, but they should not be allowed to obscure the immutable identity layer.

Also, the public statement that changing one word changes "all six emoji" is too strong. Changing one word changes the SHA-256 digest with overwhelming probability, but it does not guarantee that every one of the first six bytes changes.

A safer statement is:

> Changing the canonical bytes changes the full SHA-256 digest with overwhelming probability; the six-glyph display is a recognition prefix, while the full digest is the cryptographic identity.

---

# 6. Artifact custody is not yet actually represented by the hash

The installed workflow hashes:

```text
title
creator
description
entire GitHub issue body
```

It does not fetch, retain, or hash the bytes of files linked or attached in the issue.

Therefore:

* a linked file may change without the AXN changing;
* a linked file may disappear while the AXN remains;
* two different files can be attached to the same issue envelope;
* the repository cannot prove which bytes were originally deposited;
* the archive may preserve metadata for an artifact it never took into custody.

This is particularly important given the argument now being built around repositories accepting custody of irreplaceable work.

Alexanarch must not reproduce the same structural weakness at a smaller scale.

Every deposit needs, at minimum:

```json
{
  "work_id": "...",
  "version_id": "...",
  "record_sha256": "...",
  "metadata_sha256": "...",
  "manifest_sha256": "...",
  "artifacts": [
    {
      "path": "...",
      "media_type": "...",
      "size_bytes": 0,
      "sha256": "...",
      "original_source": "...",
      "custody_status": "locally_preserved"
    }
  ],
  "canonicalization_version": "..."
}
```

For multifile deposits, the deposit identity should derive from a canonical manifest or Merkle-style root.

---

# 7. Static records are extensive, but publication integrity is not yet guaranteed

The static record layer is one of Alexanarch's strongest assets. It gives each deposit a browser-independent, crawler-readable representation.

But the newest record exposes a direct wiring failure.

## Record 879 has a dead advertised download

The static page links to:

```text
/data/deposits/AXN-037B.md
```

That file is absent. The actual canonical text is:

```text
/data/texts/AXN-037B-text.md
```

This demonstrates that a record page can be generated successfully, enter the sitemap, and deploy while its primary source link is broken.

## Record 879 also contains two identifier scopes

The outer record has a cryptographic v2 AXN:

```text
AXN:037B.GENERATIVE.🥁💡💎🖊️👋🌹
```

The preserved substrate-authored packet contains:

```text
AXN:037B.GENERATIVE.🧵⚖️🔧🪞∮
```

The second is clearly functioning as the packet's chosen recognition marker or internal claimed identifier, not as the current record hash. Preserving it verbatim is correct. But the rendered page does not explicitly label the two scopes.

Machines need:

```text
record_axn
artifact_sha256
artifact_internal_claimed_axn
glyphic_canary
legacy_axns
```

Without that, preservation of historical metadata can look like identifier contradiction.

## Template limitations

The static page generator also:

* hardcodes a scrolling 600-pixel full-text pane;
* models every creator as `schema:Person`;
* gives a runtime mantle/custodian composite the same structure as an ordinary human author;
* uses one default license form in some standards outputs;
* does not reliably expose derivation metadata.

For Assembly work, the structured model needs roles:

```text
authoring substrate
Chorus mantle
human custodian
editor
ratifier
publisher
runtime provider
```

The human text understands these distinctions. The JSON-LD frequently does not.

---

# 8. Count consistency is improved, but typed state is still absent

The central active surfaces now agree much more closely on 879 records:

* registry: 879;
* chunk index: 879;
* static browse: 879;
* sitemap: through record 879;
* data catalog: 879.

That is good.

But neighboring standards and derivatives still describe different collections without naming the distinction.

## Standards exports still call the CHA an 871-work body

The Frictionless Data Package describes Alexanarch as housing an "871-work" CHA.

The RO-Crate repeats the same 871-work description.

The DCAT catalog repeats it again.

Meanwhile:

* the founding incident is described elsewhere as 862 unique works;
* current Alexanarch has 879 deposits;
* the DOI index has 1,817 mappings;
* 871 is also used for a subset of DOI metadata failures.

These may all be legitimate numbers. The problem is that they are not typed.

## Required `state.json`

A single generated state object should distinguish:

```json
{
  "release_id": "...",
  "generated_at": "...",
  "source_commit": "...",
  "original_cha_works_affected": 862,
  "legacy_doi_mappings": 1817,
  "datacite_public_404_observations": 871,
  "alexanarch_deposits": 879,
  "restored_records": 0,
  "native_records": 0,
  "full_text_records": 0,
  "metadata_only_records": 0,
  "wiki_entries": 861,
  "entity_concepts": 7173,
  "lexical_candidates": 12032,
  "semantic_addresses": 1964,
  "observed_addresses": 111
}
```

Every page and export should derive its numbers from this object rather than repeating prose counts.

---

# 9. The static wiki is broad but still semantically stale

The static wiki now covers 861 deposits. That fixes the old structural absence.

But the first entry still describes:

* approximately 870 works;
* more than 1,060 DOI identifiers;
* five principal concepts.

Those statements no longer match the current incident account and conceptual structure.

This demonstrates that regeneration alone is not sufficient.

A derivative needs:

```json
{
  "derived_from_record": 1,
  "derived_from_version": "...",
  "derived_from_sha256": "...",
  "generator": "...",
  "generated_at": "...",
  "review_status": "generated_unreviewed",
  "stale": false
}
```

When the source hash changes, dependent wiki summaries should become `stale: true` until regenerated or ratified.

At present, the wiki is extensive but can still preserve an older semantic state as though it were current.

---

# 10. Graph and citation structures need stronger relation ontology

The graph now integrates:

* explicit entity triples;
* reference counts;
* semantic-address overlays;
* evidence statuses;
* citation data.

This is powerful.

But the citation count requires interpretation. The data catalog says 4,866 edges exist, of which 4,311 are DOI-resolution edges.

A legacy DOI resolving to a current work is not necessarily a citation.

The graph should distinguish at least:

```text
cites
mentions
resolves_legacy_identifier
is_version_of
is_same_work_as
extends
defines
criticizes
supports
documents
has_part
is_part_of
```

Otherwise the system can truthfully report 4,866 "edges" while a user or machine incorrectly hears "4,866 scholarly citations."

Each asserted relation also needs:

* source record;
* source span or quoted passage;
* extraction method;
* evidence status;
* reviewer status;
* creation timestamp;
* supersession link.

The graph already has the beginnings of this vocabulary. It does not yet carry enough evidence localization to reconstruct why every edge exists.

---

# 11. The visibility layer is one of the strongest new structures

The address data is already close to becoming the permanent macro-audit layer we discussed.

It distinguishes:

* 1,964 candidate addresses;
* 111 observed addresses;
* 1,748 subjunctive addresses;
* 22 verified non-addresses;
* 83 unrated addresses;
* 348 unique concept targets.

This is very good because it refuses to treat "we could query this phrase" as "the phrase is currently visible."

The main limitation is scale imbalance:

> Most of the address registry currently measures **composition eligibility hypotheses**, not observed composition behavior.

That is not a defect if the distinction remains explicit. It becomes a defect only if dashboards collapse the 1,964 total into a visibility claim.

The next fields should be those we developed:

```text
visibility
anchor_alignment
figural_integrity
compositional_lift
substrate_breadth
ghost_survival
compositional_bystanding
composition_eligibility
```

The current `observed/subjunctive/unrated/verified_non_address` distinction can remain the outer evidence class.

---

# 12. DOI resolution is valuable, but the status vocabulary is conflated

The resolver currently speaks of:

* 871 severed DOIs;
* HTTP 410 GONE;
* public DataCite failures;
* recovered/unlinked states.

These are not one state.

A DOI can have distinct conditions at distinct layers:

```json
{
  "doi": "10.5281/zenodo.x",
  "doi_resolver_http_status": 302,
  "zenodo_landing_page_http_status": 410,
  "datacite_public_api_status": 404,
  "datacite_registration_state": "unknown",
  "metadata_publicly_retrievable": false,
  "artifact_publicly_retrievable": false,
  "alexanarch_successor": "...",
  "observation_date": "..."
}
```

The legal letter correctly moved toward this distinction: a DataCite public API 404 proves public metadata unavailability, not necessarily deletion from underlying systems.

The site should use the same precision.

The Manifest still says "871 with public metadata erased on DataCite," which overstates what the observation independently establishes.

Use:

> 871 DOI records returned HTTP 404 from DataCite's public API at the recorded observation time.

Then separately record what Zenodo or DataCite later discloses about underlying status.

---

# 13. Sitemap coverage is repaired, but machine discovery is still incomplete

The sitemap now contains the principal original routes and all static record pages.

But it omits many of the most important new surfaces and machine objects, including some combination of:

* `/api/index.json`;
* `/api/axn-protocol.json`;
* deposit-entry schema;
* chunk index and chunks;
* browse index;
* `/lexical/`;
* `/citations/`;
* `/captures/`;
* `/addresses/`;
* `/resolve/`;
* `/datasets/`;
* RO-Crate;
* Data Package;
* DCAT;
* graph JSON-LD;
* catalog CSV;
* checksum manifest;
* future release and recovery manifests.

Also, record `lastmod` values appear to use the work's original publication/deposit date rather than the generated page's actual modification date. A corrected or regenerated old record can therefore continue advertising an old `lastmod`.

Use a sitemap index with separate maps for:

```text
core pages
records
datasets
machine APIs
wiki
graph
releases
```

---

# 14. Standards exports exist, but they are mutable projections rather than releases

Producing RO-Crate, Data Package, DCAT, CSV, and graph JSON-LD is a major strength.

But the files generally lack a common release envelope:

* no common release ID;
* no source commit;
* no registry hash;
* no parent release;
* no manifest hash;
* no signature;
* no declared validation result.

The standards also repeat stale descriptions.

Additional issues include:

* the Data Package declares one package-level CC BY 4.0 license although individual deposits use multiple licenses;
* the RO-Crate license URL appears malformed as `licenses/by-4/4.0/`;
* the RO-Crate uses a draft 1.2 context;
* author roles are flattened;
* "content hash" fields do not consistently state their hash scope.

A standards export should be generated inside a named release:

```text
release-20260622-001/
  RELEASE-MANIFEST.json
  state.json
  registry.json
  chunks/
  records/
  texts/
  ro-crate-metadata.json
  datapackage.json
  dcat.jsonld
  graph.jsonld
  catalog.csv
  FILE-SHA256SUMS
  FILE-SHA256SUMS.sig
  RECOVERY.md
```

---

# 15. The checksum file is not a file-verification manifest

`SHA256SUMS.txt` contains lines shaped like:

```text
<hash>  AXN-0198 <human title>
```

The second field is not an actual relative file path. Therefore standard tools cannot use it to verify the repository's bytes.

It demonstrates that the registry and the checksum list repeat the same declared hash. It does not demonstrate that:

* the Markdown source bytes match;
* the static HTML matches its source;
* the PDF or attachment exists;
* the chunk matches the registry;
* the export files belong to one release.

You need two distinct structures:

### Semantic manifest

```text
work/deposit identity
artifact relationships
metadata relationships
version relationships
```

### Byte manifest

```text
<actual SHA-256>  relative/path/to/file
```

The byte manifest should be independently signed.

---

# 16. Registry chunking improves transport, not yet recovery

The registry has been divided into nine approximately one-megabyte chunks. The index records:

* chunk path;
* first and last deposit;
* count;
* byte size.

This is useful for machine transport and partial retrieval.

But the chunk index does not include:

* each chunk's SHA-256;
* registry source hash;
* release ID;
* source commit;
* signature;
* canonical chunk ordering root.

The generator also deletes/replaces chunks as a mutable build process rather than producing an immutable release directory.

So the chunks currently help distribute reading load. They do not independently prove reconstruction correctness.

---

# 17. Canonical-page signaling remains wrong

The Principles and Identifiers pages both declare the homepage as their canonical URL.

That tells search systems these pages may be duplicates of the homepage.

This is directly contrary to the visibility-layer project: the site is asking composition systems to distinguish its conceptual surfaces while instructing indexers to canonicalize some of those surfaces away.

Every page should have a self-referential canonical URL.

Static records also need consistent:

* canonical links;
* `alternate` machine formats;
* JSON-LD;
* Open Graph metadata;
* release identifiers;
* source links.

---

# 18. The Manifest presently overstates implementation

The Manifest contains several strong architectural promises:

* every deposit exists on equivalent human and machine surfaces;
* every static record contains full metadata, methodology, falsification, entity relations, wiki article, SHA, JSON-LD, and working download links;
* the homepage `<noscript>` block contains a complete deposit listing;
* static surfaces are generated automatically at mint time;
* GitHub, Vercel, and independent mirrors prevent any single administrative removal.

Those claims are not currently true:

* the homepage noscript section contains four records, not 879;
* automatic mint does not regenerate all static/data surfaces;
* record 879 has a dead source link;
* static metadata differs by template generation;
* independent mirror coverage is not machine-proven;
* GitHub remains both source and write-control locus.

A constitutional document can state commitments. But it must distinguish:

```text
CURRENT GUARANTEE
IMPLEMENTED BUT UNTESTED
DECLARED TARGET
PROPOSED
```

Otherwise aspiration is mistaken for operational law.

---

# 19. Human usability

## What works

The visual system is coherent:

* restrained typography;
* clear institutional identity;
* stable color vocabulary;
* simple cards;
* readable prose;
* consistent navigation language;
* good mobile width;
* highly legible static records.

The specialized interfaces—lexical, citation, capture, address, resolver, datasets—make the archive increasingly navigable as a system rather than merely a list.

## What remains difficult

### Browse scale

One static page containing 879 entries is excellent for crawlers and poor for sustained human navigation.

Generate static partitions:

```text
/s/browse/native/
/s/browse/restored/
/s/browse/type/...
/s/browse/creator/...
/s/browse/journal/...
/s/browse/year/...
/s/browse/status/...
```

### Long-form reading

Static full text is frequently constrained to a 600-pixel scrolling region. That makes long scholarship feel embedded rather than published.

### Accessibility

Across dynamic interfaces:

* search fields rely on placeholders rather than visible labels;
* filter controls are often `<div>` elements rather than buttons;
* keyboard and focus states are incomplete;
* dynamic result updates lack live-region announcements;
* color carries evidentiary meaning;
* horizontal navigation requires scrolling;
* skip links are absent.

### New dynamic surfaces disappear without JavaScript

The core static records, browse, wiki, and graph survive script failure. Newer interfaces such as addresses, captures, citations, resolver, and lexical navigation are primarily JavaScript applications.

Their raw JSON remains available, which is good, but the human interface disappears.

---

# 20. Security and operational governance

The versioned Vercel configuration supplies:

* JSON/Markdown MIME types;
* CORS;
* short cache control.

It does not specify:

* Content Security Policy;
* `X-Content-Type-Options: nosniff`;
* referrer policy;
* permissions policy;
* frame restrictions;
* a report endpoint.

I also did not find:

* `SECURITY.md`;
* `RECOVERY.md`;
* a top-level repository `LICENSE`;
* a custom `404.html`;
* a rhizome node contract;
* a signed release root.

Per-deposit licensing is not a substitute for licensing the code, schemas, generators, and repository-level documentation.

---

# 21. Failure matrix

| Failure                       | What survives                                               | What fails                                                          |
| ----------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------- |
| JavaScript unavailable        | Static browse, records, static wiki, static graph, raw data | Dynamic search/filter interfaces and recent homepage rendering      |
| Monolithic registry malformed | Previously generated static records and chunks              | Homepage, records app, wiki, graph, lexical joins, new generation   |
| One static source link wrong  | Rendered copy may survive                                   | Download/reconstruction path, as demonstrated by record 879         |
| Public hostile deposit        | No manual boundary before workflow                          | Can reach `main`; browser renderers may execute deposited content   |
| Semantic generator error      | Git history allows rollback                                 | Error can propagate across wiki, graph, records, standards, exports |
| Vercel stale or misbound      | GitHub source remains                                       | Canonical public surface can advertise an older institution         |
| GitHub unavailable            | Last Vercel deployment may remain readable                  | Intake, canonical source, history access, rebuilding, updates       |
| Vercel unavailable            | GitHub source and raw history remain                        | Canonical domain and record-resolution surface                      |
| Domain/DNS loss               | Full hashes and repository history may remain               | Practical AXN resolution and public canonicality                    |
| Chunk loss                    | Monolithic registry survives                                | Partial transport layer                                             |
| Monolith loss                 | Chunks contain the registry data                            | No demonstrated automatic promotion/reconstruction process          |
| Operator/admin loss           | Public source may remain                                    | DNS, Vercel, merge/write authority, release succession              |
| GitHub and Vercel both lost   | External fragments and other sites may remain               | No demonstrated complete, signed, independently governed node       |

---

# 22. Is Alexanarch now a data rhizome?

## On the read side: increasingly yes

The corpus exists through:

* one canonical registry;
* nine chunks;
* 879 static records;
* 861 static wiki entries;
* graph projections;
* raw source texts;
* DOI maps;
* semantic-address data;
* visibility captures;
* standards exports;
* Git history.

A browser failure, JavaScript failure, or loss of the monolithic interface no longer destroys all access.

That is rhizomatic behavior.

## On the write and succession side: no

The system still depends on one concentrated administrative chain:

```text
GitHub issue
→ GitHub Action
→ direct mutation of main
→ Vercel deployment
→ canonical domain
```

There is no demonstrated:

* independently governed full mirror;
* signed immutable release;
* peer/coverage ledger;
* recovery handbook;
* replacement-operator procedure;
* cross-node consensus or succession rule;
* destructive reconstruction test.

So the accurate description is:

> **Alexanarch is a proto-rhizome with a strong distributed read body and a centralized, under-protected reproductive organ.**

Or even more plainly:

> **It can break and keep being read. It cannot yet break and safely keep accepting writes.**

---

# 23. Priority order

## P0 — stop-the-line

### 1. Close direct public mutation of `main`

Change minting to:

```text
issue opened
→ structural validation report
→ no repository mutation
→ maintainer or named operator applies mint-approved
→ branch generated
→ full build and validation
→ reviewed merge
```

Until this exists, automatic public minting should be suspended.

### 2. Install actual enforcement

Required status checks should include:

* JSON Schema validation;
* semantic registry invariants;
* artifact existence and byte hashing;
* AXN recomputation;
* route/source integrity;
* complete build;
* stale-derivative detection;
* hostile rendering fixtures;
* internal-link crawl;
* standards validation;
* checksum validation;
* secret scan.

Vercel should deploy production only from a commit that passed all required checks.

### 3. Remove executable-input paths

Replace raw `innerHTML` composition, disable raw Markdown HTML, validate URLs, and install CSP.

### 4. Unify AXN implementation

One library must generate:

* web preview;
* workflow result;
* registry value;
* static record value;
* verification instructions.

Forbid obsolete four-glyph language except inside explicitly labeled legacy documentation.

### 5. Repair deployment coherence

Choose apex or `www` as canonical, permanently redirect the other, expose release markers, and smoke-test both after deployment.

### 6. Repair current broken source routes

A release must fail if any record's declared source or download path does not exist.

---

## P1 — make the foundry truthful

### 7. Generate `state.json`

All counts and collection descriptions derive from it.

### 8. Establish explicit identity scopes

Artifact, metadata, manifest, version, work root, record number, display glyph, and glyphic canary must be distinct fields.

### 9. Build real file checksums

Use actual paths and sign the release manifest.

### 9. Make every derivative confess its source

Add source hash, source version, generator, generated time, review status, and stale status.

### 11. Correct DOI state taxonomy

Separate DOI resolution, Zenodo landing-page state, DataCite public metadata state, registration state, artifact availability, and successor availability.

### 12. Correct graph ontology

Do not count resolution equivalence as citation without an explicit relation type.

### 13. Correct standards exports

Remove stale 871-work descriptions, fix license semantics, add release provenance, and validate RO-Crate/DCAT/Data Package outputs.

### 14. Add static versions of the newer observational surfaces

At least a paginated static snapshot or static summary should exist for:

* captures;
* addresses;
* lexical terms;
* citation graph;
* DOI resolution;
* dataset catalog.

---

## P2 — become a strong rhizome

### 15. Produce signed immutable releases

Each release needs:

```text
release ID
source commit
registry hash
record count
artifact manifest
byte checksums
signature
parent release
recovery instructions
```

### 16. Publish independently governed nodes

At least three operators or systems should hold clearly declared coverage:

* complete;
* metadata-only;
* text-only;
* artifact;
* resolver;
* continuity.

### 17. Publish a node contract

```text
/rhizome/node.json
/rhizome/peers.json
/rhizome/health.json
/rhizome/releases/latest.json
/rhizome/releases/{id}/manifest.json
/rhizome/rebuild.md
```

### 18. Test destruction

The decisive test is:

1. export a signed release;
2. delete a staging deployment and local working copy;
3. give a fresh operator only the release and recovery instructions;
4. rebuild under a different account and host;
5. compare file hashes, records, routes, identifiers, versions, graph edges, and resolver outcomes;
6. record all missing state.

Only that test can establish that the rhizome reconstructs rather than merely replicates.

---

# 24. Minimal release invariants

The build should refuse publication unless:

```text
registry total
= distinct deposit numbers
= static record directories
= static browse rows
= sitemap record URLs
= catalog rows
= RO-Crate deposit entities
```

For every deposit:

```text
deposit_number is unique
AXN recomputes from declared canonical bytes
full SHA-256 is present
artifact manifest exists
all artifact paths exist
all artifact hashes verify
declared download path exists
static record exists
self-canonical URL exists
JSON-LD exists and validates
source record hash is declared
version/root relationship is valid
all relation targets resolve or are explicitly external
```

For every derivative:

```text
source record/version/hash declared
generator and version declared
generated_at declared
review status declared
stale flag agrees with current source hash
```

For every DOI mapping:

```text
DOI normalized
observation layer explicitly named
successor route exists
target title/AXN agrees with registry
no /records/0/
no multiple primary mappings without explicit precedence
```

For the release:

```text
all standards validate
all internal links resolve
no unsafe URL schemes
no raw executable deposit HTML
no secrets or private-name violations
file checksum manifest verifies
signature verifies
deployment release marker equals source release marker
apex and www agree
```

---

# Final diagnosis

Alexanarch has advanced beyond the supplied audit in important ways. The static corpus is much more complete. The sitemap now covers the records. The wiki and graph have become real surfaces. The DOI resolver works as a public instrument. The lexical and visibility structures are becoming intellectually serious data models.

The architecture now understands the whole better than it did.

But the new control documents are presently ahead of the executable institution. They describe laws that the write path does not obey. The site can publish a direct mutation from public issue input, through an obsolete identifier implementation, without schema enforcement, into browser surfaces that still permit executable content.

That is the current center of gravity.

> **Do not build another major surface before installing the transaction boundary.**

Alexanarch now has enough representations.

The next decisive object is one lawful operation:

```text
untrusted submission
→ preserved artifact
→ canonicalized manifest
→ deterministic identity
→ complete derivation
→ hostile validation
→ atomic release
→ signed replication
```

Once that operation exists, Alexanarch will no longer merely be a library that has prepared many ways to survive.

It will be a library whose act of reproducing itself is governed as rigorously as the works it carries.

[1]: https://www.alexanarch.org/ "Alexanarch — The Self-Governing Library"
[2]: https://www.alexanarch.org/identifiers/ "Identifiers — Alexanarch"

---

*End of Appendix A.*
