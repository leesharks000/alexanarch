# Dataflow Atlas — v0.9 addendum (2026-08-06)
## The axn-identifiers node, the singular/plural naming incident, and the qf1g retirement

**Supplements:** atlas v0.2 + addenda v0.3–v0.8. Registers a new rhizome node and closes a
fossilized-name incident of the PATHOLOGY-01 class.

---

## NEW NODE — axn-identifiers (product surface / "the door")

| | |
|---|---|
| Repo | `leesharks000/axn-identifiers` (standalone; seeded 2026-08-06 from `alexanarch/axnidentifiers-site/`) |
| Domains | **axnidentifiers.org** (canonical) · axnidentifiers.com · axnidentifier.org · axnidentifier.com — all owned (Namecheap, privacy ON); non-canonical hosts 308-redirect |
| Role | Public presentation surface for the AXN identifier system: landing, design language, stamp/verify entry points |
| Authority relation | **derived — alexanarch is the authority.** Canonical derivation (`scripts/axn_lib.py`), the central registry (`data/axn-central-registry.json`), the symbolon endpoint (`/api/register-symbolon`), the Constitution, and all governance remain on alexanarch. This node holds no registry state and mints nothing. |
| Consumes | `data/axn-central-registry.json` (verify/lookup flows), `/mint/stamp/` + `/api/register-symbolon` (stamp flows link through to alexanarch), `axn/assets/` marks |
| Produces | Nothing canonical. Design-language specimens (`design/specimen-v0.*.html`) are proposals until MANUS ratification, per their own SIG·0 changelog fields. |
| Custody | Same administrator, same platform as the rest of the fleet (PATHOLOGY-13 applies unchanged). |

## INCIDENT — the singular/plural fossilized name (2026-08-02 → 08-06, CLOSED)

On launch day the domains **axnidentifier.org/.com (singular)** were registered and their DNS
correctly configured (apex A 216.198.79.1; www CNAME to a Vercel per-project name). Every surface
built afterward — landing copy, launch notes, working docs, memory records, and four days of
diagnostic effort — referenced **axnidentifiers (plural)**, which did not exist. The plural was
propagated from notes without verification against the registration: *a name written once was a
claim true never.* Census at closure: plural in exactly 4 editable files, 0 sealed canonical texts;
singular in 0 files. Resolution (MANUS, 2026-08-06): plural purchased; **plural canonical**; all
four spellings held defensively (the typo-neighbor of a provenance service is a phishing surface
if left ownable); singular 308s. Mechanism lesson joins PATHOLOGY-01: displayed values must read
from state — and *names* are displayed values; the authoritative state for a domain name is the
registrar, not the notes.

## RETIREMENT — vercel project `alexanarch-qf1g`

A second Vercel import of the alexanarch repo (created 2026-08-01) served as a stand-in
axnidentifiers surface at `alexanarch-qf1g.vercel.app`. Retired 2026-08-06 in favor of the
standalone node above; the duplicate-import pattern (one repo, two projects) is deprecated —
it doubled the DNS/deploy surface and produced the cross-zone record confusion this addendum
closes. `alexanarch/axnidentifiers-site/` is scheduled for pointer-note retirement after the
new domain verifies live (non-destructive: file replaced by a one-line pointer, per WAVE-HEXPOS-01
practice).

## DNS custody note

All fleet DNS zones live at **Namecheap** (nameservers `registrar-servers.com`) — not at Vercel.
Vercel holds only hostname *claims* per project. During the incident, `alexanarch.com`'s www CNAME
was set to another project's issued vercel-dns name; it serves correctly regardless (Vercel routes
by hostname claim, not CNAME target), but should be realigned to the value shown on the alexanarch
project's own Domains panel. Hygiene, not outage.
