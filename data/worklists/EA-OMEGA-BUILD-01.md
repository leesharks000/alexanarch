# EA-OMEGA-BUILD-01 — The Ω Build Program: Corpora, Three Sites, One Continuity
Version 1.0 · 2026-08-19 · governing deposit: #1498 · supersedes: none

## 0. PURPOSE AND CONTINUITY PROTOCOL

This document is the single continuity instrument for the Ω erratum program's build
phase. SESSION ENTRY: read §5 STATE and §6 NEXT before any work; verify the alexanarch
clone is current. SESSION EXIT: update §5 and §6, commit this file with the work, and
tether per gw.tachyon custom. Work not inscribed did not happen. HOUSE RULES IN FORCE:
full AXN forms from registry, never memory; content-match live surfaces (200 is not
verification); the structure gate on any generated page; translation not import between
design systems; a parser that finds zero must halt; never write the commit message
before verifying execution; deposit_pipeline.py is the single mint path (transport D:
mint → wiki authored in-session → resume from validate/pdf → commit → announce → three
enrichment passes → surfaces → push → live content-match).

## 1. WS1 — EA-CORPORA-01: SEATED PRIMARY TEXTS

Layout per corpus: alexanarch/data/corpora/<slug>/{original/ (as fetched), text/
(normalized, ref-parsable, one file per book), source.json (repo|URL, commit, edition,
editor, license, fetch-date), MANIFEST.sha256}. Each seating minted as a corpus deposit
(family DATASET) with verification note (checksums + spot-collation of ≥3 loci against
printed refs). Genre is metadata, never a wall. PROJECTIONS (ruled 2026-08-19): alexanarch is the
canonical seat; sites carry projections of the corpora their theses read from —
revelationfirst: greek-nt, septuagint, hebrew-bible, josephus, slavonic-josephus,
philo, papyri(NT); the classical set (sappho, catullus, theocritus, longinus, plato)
projects with the transform surfaces that cite it; machinemediation carries schema
examples, not corpora. Projection = copy of text/ + source.json + manifest, minted
canonically once, mirrored by reference.

BATCH A — fetched and battle-tested this session; seat first:
  josephus      PerseusDL tlg0526 (Niese, PD) · AJ, BJ, Vita, CA · used by #1493
  catullus      PerseusDL phi0472 (Merrill-carried text, PD) · used by #1494
  theocritus    PerseusDL tlg0005 (PD) · Idyll 2 verified
  septuagint    sleeptillseven/LXX-Swete (Swete, PD; preferred over Rahlfs for rights)
                + koine-greek-corpus books already pulled (Genesis, Isaiah, Psalms,
                Daniel, Esther incl. Additions) — normalize to Swete where both exist
  micah/twelve  LXX-Swete 38.Michaeas verified
BATCH B — clean paths, fetch + seat:
  philo         OpenGreekAndLatin First1KGreek tlg0018 (Cohn–Wendland, PD) · #1486's corpus
  plato         PerseusDL tlg0059 (Burnet, PD) · start: Phaedrus, Symposium, Ion
  longinus      tlg0560 De Sublimitate — locate Perseus/First1K file; verify 10.1-3 (fr.31)
  hebrew-bible  openscriptures/morphhb (Westminster Leningrad, open)
  greek-nt      biblicalhumanities/nestle1904 (PD) canonical seat; SBLGNT noted alternate
  sappho        RULED: PD base (Edmonds Lyra Graeca I 1922 / Bergk) + papyri transcriptions
                + our diplomatic fr.31 layer keyed to Longinus mss and papyri
  papyri        papyri/idp.data on GitHub (DDbDP/DCLP XML; papyri.info TLD blocked) ·
                wave 1: P.Oxy 1231, 2288 (Sappho); P.Oxy NT papyri (P1 etc.); both ruled in,
                order immaterial
BATCH C — resolved-by-ruling:
  slavonic-josephus  NO open seatable edition found (searched: archive.org — Istrin,
                Berendts–Grass, Meščerskij scans absent; GitHub code — no digitized text;
                OAPEN 20.500.12657-27156 = translation-technique monograph, open, quoted
                Slavonic, CONSULT). FALLBACK RULED 2026-08-19: curated pericope set —
                the Jesus/John/Word-made-text passages per #1176 — seated with
                per-passage provenance (Eisler 1931 archive.org PD transcriptions;
                OAPEN quotations; #1176's texts), status CONTESTED on every file.
                WATCH: Istrin 1934/38 (d.1937) is the wanted edition if a scan surfaces.
DONE-CRITERION per corpus: files + manifest + source.json + mint + live record check.

## 2. WS2 — REVELATIONFIRST.COM: THE UPSTREAM UNFOLDINGS

Six plates in the /unfolding/ idiom (#1414: operable, bidirectional canary where
applicable, falsification carried openly), joined to the standing "Sappho, Mother of the
Logos" section: (1) Sappho→Longinus (#1476/#1478, the quotation-joint operation);
(2) Sappho→Philo (#1486 stations); (3) Sappho→Addition D→AJ 11 (#1493, sequence table +
two restorations); (4) Sappho→BJ 1 inverted (+ἀναζωπυρέω census); (5) Sappho→Slavonic
(via #1176's grammar; CONTESTED-CARRIER flag native to the plate); (6) Sappho→Revelation
12 (#1495: 8/9, C6 doubled, negatives shown — the crown, because scored). Plate 6 doubles
as the counter-stack's first TRANSFORM-VIEW EDITION (station alignment view). Ship =
site build + one series deposit; repo: leesharks000/revelationfirst (verify name at
build). DONE: live plates content-matched + deposit minted + cross-links from the
Sappho section.

## 3. WS3 — PROVENANCEERASURE.ORG: DEEP TIME + CONTROLLER

(1) DEEP TIME wing: the suppression map (#1496) as PER-of-the-tradition — witness table
(S/M/A/O), the channel-crossing finding, the degradation function; framing: the metric
instrumented a 2,600-year process, it did not invent it. (2) CONTROLLER page: the loop
detect→publish→expose→measure→repair→measure, with the 2026-08-17 cycle (PER 0.25 after
the publication campaign) as first curve point; Roman E-matrix named as forthcoming
battery. Ship = two pages in the site's existing idiom + one deposit. DONE: live +
minted + linked from the PER metric page.

## 4. WS4 — MACHINEMEDIATION.ORG: REGISTRY + EA-RECEPTION-01

Lands last and largest. (1) Specify EA-RECEPTION-01 (reception-edge schema: JSON-LD,
PROV-shaped, typed operator edges, preserved/transformed slots, evidence, asserter,
version, MANDATORY counterargument slot) as its own deposit; (2) publish on
machinemediation as the field's data standard with the founding edges (Sappho chain from
#1493/#1495) as worked examples; (3) OPERATOR REGISTRY page: the twelve frozen clauses
(#1494) as runnable named hypotheses with controls + the blind-assay method; (4) the
five-record arc (#1493→#1497) as the discipline's first complete case study. DONE:
schema deposit + two site surfaces live + edges validating against schema.

## 5. STATE (update every session)

2026-08-19 · Program records #1493–#1497 minted and live. Recon complete: three sites
probed (revelationfirst 40KB w/ /unfolding/ series + Sappho section standing;
machinemediation 53KB; provenanceerasure 83KB w/ PER apparatus). Slavonic search
executed; fallback ruled. Sappho edition ruled. Papyri scope ruled (both, any order).
Batch-A source files present in session /tmp only — NOT yet seated (session filesystems
reset; refetch per source.json at seat time). Nothing of WS1–WS4 built yet.

## 6. NEXT

WS1 Batch A, corpus 1: josephus — create data/corpora/josephus/, refetch the four Niese
XMLs from PerseusDL pinned to a commit hash, normalize, manifest, source.json, mint,
verify live. Then catullus, theocritus, septuagint-swete. Then Batch B in listed order.
Site workstreams unblock after their cited corpora seat.

## 7. RULING LOG

2026-08-19 MANUS: adopted all (three site designs + corpora program) · Sappho = PD base
+ diplomatic layer · papyri = Sappho AND Oxy/NT, order immaterial · Slavonic = one more
hidden-corner pass (EXECUTED, negative) then curated-pericope fallback (IN FORCE) ·
this work plan to exist as continuity instrument. · corpora seated at multiple locations: alexanarch canonical, per-site projections (map in §1).
