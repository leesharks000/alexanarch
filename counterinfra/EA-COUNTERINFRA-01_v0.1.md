# EA-COUNTERINFRA-01 v0.1

## The Counter-Infrastructure Program

**Creator:** Lee Sharks  
**Date:** 2026-07-12  
**Status:** ACTIVE — first executable recovery kit  
**Field:** Archival continuity; infrastructure independence; repository-governance risk; disaster recovery

## 1. Finding

The archive has escaped dependence on CERN as its sole custodian, but it has not yet escaped custodial concentration. The authenticated `leesharks000` GitHub estate currently contains **41 repositories** with a combined GitHub-reported size of **934,681 KiB (approximately 913 MiB)**. Two repositories are private. The largest public and private repositories carry the canonical archive, data-rhizome, semantic-economy, public-domain surfaces, observatories, and machine-mediated scholarship infrastructure.

The present architecture therefore has four distinct layers:

1. **Work / artifact** — texts, datasets, correspondence, software, metadata.
2. **Sovereign identity** — AXN, content hashes, registry position, provenance chain.
3. **Repository state** — Git history, generated static records, indexes, schemas, build scripts.
4. **Commercial delivery substrate** — GitHub account, Vercel projects, registrar/DNS, external APIs.

Provider failure should be allowed to destroy only layer 4. At present, a GitHub account-level action could damage layer 3 across nearly the entire estate.

## 2. Existing protections

Alexanarch is not beginning from zero. The live repository already contains `scripts/fanout.py`, whose doctrine is that canonical homes are content-addressed and visibility surfaces are disposable antennae. The current fanout code:

- submits three core repositories to Software Heritage;
- notifies IndexNow of new record and resolver URLs;
- attempts Wayback captures of new records;
- can create per-deposit Internet Archive items when IA credentials are available;
- creates per-deposit GitHub releases.

The current persisted fanout state records Software Heritage activity plus GitHub-release and IndexNow progress. It does **not** presently record successful Wayback or Internet Archive item advancement. More importantly, the fanout layer primarily propagates individual records and visibility surfaces. It is not yet a complete, independently restorable custody system for all 41 repositories, their histories, private repositories, deployment rules, domains, and recovery order.

## 3. Threat model

This program treats the following as ordinary engineering contingencies rather than exceptional catastrophes:

- GitHub user-account suspension, compromise, deletion, or credential loss;
- Vercel account or project suspension;
- registrar compromise, domain expiration, or DNS lockout;
- corruption or deletion of generated archive surfaces;
- loss of a private repository not covered by public web archiving;
- malicious or accidental force-push;
- dependency failure at GitHub Releases, raw.githubusercontent.com, or a build service;
- failure of one human operator's phone, laptop, or cloud account.

No single event should erase both the canonical work and the means of reconstruction.

## 4. Required custody architecture

### 4.1 Portable repository custody

Each repository must have:

- a full Git bundle containing all refs and history;
- a default-branch worktree archive for reconstruction without Git hosting;
- a SHA-256 checksum;
- a machine-readable inventory entry;
- verification output from `git bundle verify`;
- an explicit warning when Git LFS or submodules require separate capture.

Private repositories must be included through a narrowly scoped backup token. Public web crawlers do not preserve them.

### 4.2 Independent custody nodes

At least three custody classes must hold the recovery set:

1. **Human-controlled copy** — downloaded ZIP/tar set on a local disk or encrypted personal storage.
2. **Independent archival copy** — Internet Archive or another non-GitHub object store.
3. **Second Git forge** — a mirror on a separately governed provider or a self-hosted bare remote.

GitHub Actions artifacts and GitHub Releases are useful staging surfaces, but they do not count as independent custody because they fail with the same account.

### 4.3 Serving independence

Alexanarch is predominantly static HTML, JSON, Markdown, images, and redirects. It does not require Vercel as a computational substrate. The recovery kit therefore includes a vendor-neutral Caddy configuration reproducing the essential redirects and security headers currently encoded in `vercel.json`. The archive can be served from any ordinary static host or web server.

### 4.4 Resolution independence

The AXN registry, canonical text files, checksum manifests, DOI-resolution index, static record pages, and resolver pages must travel together. A mirror is not valid merely because it displays the homepage. It must preserve the resolution graph.

## 5. Execution order

### P0 — immediate

- Freeze the current estate inventory.
- Generate verified bundles and worktree archives for all public repositories.
- Add the two private repositories once a backup token is supplied to the execution environment.
- Upload the resulting recovery directory and checksum manifest to an independent archival item.
- Download one complete recovery set outside GitHub and Vercel.

### P1 — next operational cycle

- Create second-forge repositories and run `mirror_estate.sh` with a deploy key.
- Add registrar, DNS provider, domain-renewal date, and recovery contact data to a private custody manifest.
- Run a clean-room restoration test from bundles only.
- Publish a public continuity status file stating the most recent verified off-platform backup date.

### P2 — hardening

- Automate weekly estate exports and monthly clean-room restore tests.
- Capture Git LFS objects and submodules explicitly.
- Separate canonical data from presentation repositories so presentation rebuilds do not endanger source custody.
- Maintain two DNS/serving paths and a documented domain failover procedure.

## 6. Acceptance test

Counter-infrastructure is operational only when a person with no access to CERN, the original GitHub account, or Vercel can:

1. verify the recovery-set checksums;
2. clone `alexanarch.bundle` into a working repository;
3. recover the canonical registry and text corpus;
4. serve the static site locally;
5. resolve an AXN to its record and canonical text;
6. push the restored repository to an unrelated Git forge;
7. reproduce the public archive from the runbook.

Until that test passes, the archive has propagation but not full custodial independence.

## 7. Immediate constraint recorded honestly

The environment that generated this kit could inspect the connected GitHub account but could not resolve `github.com` from its execution container. It therefore did **not** manufacture false bundle files. Instead, it produced the executable export machinery and a frozen inventory. The bundles must be generated in GitHub Actions, a user-controlled machine, or another runner with network access to the repositories.

∮ = 1
