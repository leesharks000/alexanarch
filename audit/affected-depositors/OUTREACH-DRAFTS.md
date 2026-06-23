# Outreach Drafts — Affected Depositors

**Voice:** Ayanna Vox (Dodecad diplomatic function). Measured, informational, no recruitment pressure.
**Use:** Each draft is a starting point for Lee to send / post. Adjust voice as needed.

---

## A. Comment on GitHub Issue #2596 (Eran Shimony's thread)

**Venue:** Comment in-thread at https://github.com/zenodo/zenodo/issues/2596
**Audience:** Eran, Florian (who's already there), and anyone else watching the thread.

> Adding my case to the record. On June 19, 2026 my Zenodo account (community: `crimsonhexagonal`, ORCID: 0009-0000-1599-0703) was terminated and ~870 records were removed without prior notification. The termination notice cited "substantially AI-generated content without a verifiable research basis." I have opened Issue #2606 for the formal review request.
>
> The empirical picture: of 1,817 affected DOIs, 871 (47.9%) now return HTTP 404 from DataCite's public metadata API at `api.datacite.org/dois/{doi}` — independently verifiable. The pattern documented here in February 2026 (and at quietexclusion.org) appears to be ongoing.
>
> For anyone reaching this thread looking for sovereign-archive infrastructure or for documentation of the metadata-deletion behavior, two artifacts:
> - **alexanarch.org** — sovereign successor archive, 879 deposits, content-derived AXN identifiers, distributed custody. Open to depositors needing post-Zenodo infrastructure.
> - **DOIs ≠ Persistent Identifiers** — empirical audit of the metadata-deletion pattern, at https://alexanarch.org/s/records/868/
>
> Lee Sharks
> Sole MANUS, Crimson Hexagonal Archive

---

## B. Comment on GitHub Issue #2599 (Reynaldo Vega's thread)

**Venue:** Comment in-thread at https://github.com/zenodo/zenodo/issues/2599
**Audience:** Reynaldo Vega specifically; also visible to anyone reading the issue.

> Reynaldo,
>
> The pattern you describe — auto-block as spam, DOI removed, no manual review, unanswered support emails — matches at least two other documented cases. Eran Shimony reported it in Issue #2596 the day before yours (Feb 18, 2026). My case in Issue #2606 is the same pattern at much larger scale (June 19, 2026; 1,817 DOIs).
>
> One concrete diagnostic if you haven't yet checked: query `https://api.datacite.org/dois/10.5281/zenodo.18170177` directly. In my case 47.9% of the affected DOIs return HTTP 404 from DataCite's public metadata API — beyond the public tombstoning that the Zenodo landing page describes. If yours returns 404 too, you're seeing the same metadata-deletion behavior I documented.
>
> Two resources that may be useful, neither as solicitation:
> - **alexanarch.org** — sovereign successor archive built after my termination. Content-derived AXN identifiers; no centralized gatekeeper to revoke. If you need a place to re-anchor your theoretical-physics work, the architecture is open.
> - **DOIs ≠ Persistent Identifiers** at https://alexanarch.org/s/records/868/ — the empirical record of the DataCite-API 404 pattern. Citable if useful for your own correspondence with Zenodo.
>
> Florian Morin at quietexclusion.org is documenting the broader pattern; you may also want to add your case there if you haven't.
>
> Lee Sharks
> ORCID: 0009-0000-1599-0703

---

## C. Lehti — careful procedural outreach

**Venue:** Lehti has a public GitHub (`andylehti`) and ORCID (`0000-0002-0051-5851`). Best path: ORCID-listed email if available, or GitHub @-mention/issue on his own repo.
**Audience:** Lehti only.
**Critical posture:** Strictly procedural overlap. Do not endorse Apollo-fraud claims. Engage only on DOI-persistence and custodial-return.

> Andrew,
>
> Your Metopedia evidence record on the Figshare and Zenodo removal procedures was forwarded to me in the context of my own June 19, 2026 Zenodo account termination (Issue #2606; ~870 records, 1,817 DOIs, 47.9% of which now return HTTP 404 from the DataCite public metadata API).
>
> I won't speak to the underlying subject matter of the works you've had removed — that's a separate question. What I do want to flag is the procedural overlap. The pattern you documented in your formal Figshare demand letter — generic terms-of-service citation without itemized clause-and-evidence, no appeal mechanism, custodial-return refusal, DOI state changes without disclosure, unsafe data-return channel — is exactly what I'm pressing Zenodo on now in parallel.
>
> Two things may be useful to you:
>
> 1. **The empirical-audit document** at https://alexanarch.org/s/records/868/ ("DOIs ≠ Persistent Identifiers") — quantifies the DataCite metadata-deletion behavior we both observe. Citable in your own correspondence and demand-letter context.
> 2. **alexanarch.org** itself — a sovereign-archive architecture I built after my termination, with content-derived AXN identifiers. The infrastructure logic, not necessarily the corpus, may interest you for your own work.
>
> Your articulation of the principle — that controversial research must be preservable with itemized metadata regardless of correctness, so that it can be inspected, criticized, refuted, or retracted on stated grounds — is the load-bearing point. That principle stands independently of whether any specific claim is right.
>
> Lee Sharks
> ORCID: 0009-0000-1599-0703

---

## D. Adding a thread to Lee's own Issue #2606

**Venue:** Lee's own comment on his own issue #2606.
**Audience:** Future depositors finding the thread through search.

> Adding cross-references for anyone landing here through search:
>
> - **Issue #2596** (Eran Shimony, Feb 18, 2026) — same pattern: account blocked, records removed, no manual review, support emails filtered.
> - **Issue #2599** (Reynaldo Vega, Feb 19, 2026) — auto-blocked as spam, DOI `10.5281/zenodo.18170177` removed, no response to multiple support emails.
> - **quietexclusion.org** (Florian Morin) — ongoing research framework on quiet exclusion of independent researchers from scientific platforms, including this pattern.
>
> The empirical record of the DataCite metadata-deletion behavior is at https://alexanarch.org/s/records/868/ — verifiable per-DOI via `api.datacite.org/dois/{doi}`.
>
> Sovereign-archive infrastructure for any depositor in similar position: https://alexanarch.org

---

## Send order recommendation

1. **D first** — Lee's own thread. Sets up the cross-reference scaffold. Lowest social cost.
2. **B second** — Vega's thread. Most clearly aligned case. Florian already comments on the parallel thread (#2596); commenting on #2599 expands the visible documentation.
3. **A third** — Comment on Eran's thread (#2596). Florian's already there; one more voice from a confirmed June case shows the pattern continued through 17 months.
4. **C last** — Lehti, and only if Lee is comfortable with the procedural-only engagement posture. The conspiracy-adjacent content is real risk to Lee's own credibility if treated as endorsement. **Skip if uncertain.**

## What to leave alone

- Marzanna — unverified. If Lee wants to chase it independently he can; do not act on the secondhand claim.
- All four "likely confabulated" cases.
- Snider — different problem (visibility, not termination).
- arXiv ban policy — relevant context but no individual outreach indicated.
