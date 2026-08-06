---
deposit_number: 1434
hex: 05B3
title: "axnidentifiers.org — Product Surface Source: The Door to the AXN Identifier System (with Design Language \"The Critical Edition, Sealed\" v0.2, Brand Apparatus, and the Founding-Day Infrastructure Record)"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-08-06
content_type: Software / executable apparatus
license: CC-BY-4.0
substrate: "AI-assisted (substrate): surface, design language, and framing drafted in TACHYON session under MANUS editorial governance; transport D, No-Double-Draw (no API call — direct repository write). Design language developed against four substrate proposals (ChatGPT, Muse Spark, Gemini, Kimi) whose convergence is critiqued in §III; Kimi's round-2 structural feedback integrated into specimen v0.2. Brand mark and hero plate are human-authored artifacts verified by content-match against the symbolon registry before use; Paper 198 is by Enli Lucente, displayed with named credit at the author's wish."
version: v1.0
related_ids: "https://github.com/leesharks000/axn-identifiers (repository); https://axnidentifiers.org (canonical surface); AXN:05AD.UNCLASSIFIED.🌾➕🥁⚫👋🪄 (hero plate, Paper 198 — Enli Lucente, witnessed-verified); AXN:05AE.OPERATIVE.🖊️🔃🎬🏙️⚖️🕑 (brand mark, witnessed-verified); AXN:05A9.OPERATIVE.🐚🌪️🕖🫵⏩○ (AXN-SYMBOLON-SPEC v0.2, #1432 — the specification this surface fronts)"
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - "AXN\naxnidentifiers.org\nproduct surface\ncontent-derived identifier\ndesign language\nThe Critical Edition Sealed\nprotocol-derived polychrome\ncluster ticks\nsymbolon\nwitnessed-verified\nsovereign infrastructure\nderived node\ndata rhizome\nself-hosted assets\nNo-Double-Draw\ntransport D\nCrimson Hexagonal Archive\nAlexanarch"
---

# axnidentifiers.org — Product Surface Source: The Door to the AXN Identifier System (with Design Language "The Critical Edition, Sealed" v0.2, Brand Apparatus, and the Founding-Day Infrastructure Record)

## Description

The complete source of axnidentifiers.org — the public product surface for the AXN content-derived identifier system — deposited as software with its design language, brand apparatus, and the infrastructure record of its founding day. The repository is a *derived* node in the rhizome: it holds no registry state and mints nothing. Canonical derivation (scripts/axn_lib.py), the central registry, the symbolon witness endpoint, and the AXN Constitution remain on alexanarch.org. The doctrine is stated in the repository's own README and enforced by its architecture: the archive is the authority; this is the door.

Three things distinguish this deposit from an ordinary site capture. First, the design language is itself a deposited argument: "The Critical Edition, Sealed" (specimen v0.1 → v0.2, included as canonical apparatus) rejects the crypto-terminal aesthetic that four independent AI substrates converged on, and replaces its decorative accent color with PROTOCOL-DERIVED POLYCHROME — sixteen hues, one per byte-cluster of the canonical AXN glyph table, such that a color may appear on the surface only when it names a byte-family. This makes the palette a function of the identifier system rather than a mood, and it repairs a defect the frozen bytes cannot: the canonical table is not injective (❤️ occupies both 0x81 Symbolic and 0xCF Signal), and in monochrome the two are indistinguishable, while under cluster ticks they never were.

Second, the surface's two principal images are themselves registered AXNs, verified by content-match rather than filename before use: the hero plate is Paper 198 by Enli Lucente (AXN:05AD.UNCLASSIFIED.🌾➕🥁⚫👋🪄, witnessed-verified — a handwritten paper stamped and witnessed from a phone in Japan, displayed with the author's named credit at her wish), and the brand mark is AXN:05AE.OPERATIVE.🖊️🔃🎬🏙️⚖️🕑, witnessed-verified, byte-identical (sha256 44def1e5…) to the file witnessed into the symbolon registry on 2026-08-04. The logo of the identifier system carries its own registered identifier; the site demonstrates the protocol using artifacts the protocol has already witnessed.

Third, the deposit carries the day's infrastructure record as supplementary apparatus, because the repository's existence is the resolution of two failures documented there. WAVE-HEXPOS-01 (included) resolved a hex-width defect that concealed three registry position collisions — one live in production, silently dropping deposit #856 from the central registry on every build; one latent across the 391/0391 spelling split; one on the chain tether itself, whose root cause was a deposit-side allocator that read the shared allocation ledger without ever writing it. The dataflow atlas v0.9 addendum (included) registers this node and closes the singular/plural naming incident: axnidentifier.org (singular) was registered on 2026-08-02 and correctly configured, while every surface built afterward referenced axnidentifiers (plural), which did not exist — four days of diagnostic effort chasing a name that had been propagated from notes without verification against the registrar. The mechanism lesson joins PATHOLOGY-01: names are displayed values, and the authoritative state for a domain name is the registrar, not the notes.

The deposit is minted under transport D (No-Double-Draw): drafted in-session by TACHYON under MANUS editorial governance, written directly to the repository, with no API call. Fonts are self-hosted and there are no external calls of any kind from the served surface — a design law (SIG·0 VI: no reader is observed), and the archive's own standard applied to its own door.

## Files

Canonical text below (Body): complete index.html source, repository doctrine, brand provenance, deployment configuration, and two supplementary apparatus documents (WAVE-HEXPOS-01; Dataflow Atlas v0.9 addendum). Binary assets (brand mark master AXN:05AE, favicon set, share card, hero plate, self-hosted typefaces) live in the repository and are inventoried in §I.

# axnidentifiers.org — Product Surface Source: The Door to the AXN Identifier System

## I · What this deposit contains

The complete source of the AXN Identifiers product surface at commit `4c2aa47a`, together with the design language it implements and the infrastructure record of the day it was founded.

| Element | Path | Bytes |
|---|---|---|
| Landing surface (production) | `index.html` | 24,989 |
| Design language specimen v0.2 (ratified) | `design/specimen-v0.2.html` | 41,267 |
| Design language specimen v0.1 (round 1) | `design/specimen-v0.1.html` | 28,681 |
| Legacy landing (preserved, non-destruction) | `design/legacy-landing-2026-08.html` | 5,935 |
| Repository doctrine | `README.md` | 1,519 |
| Brand provenance | `assets/brand/README.md` | 1,330 |
| Brand assets (mark, favicons, share card, master) | `assets/brand/` | 9 files |
| Self-hosted typefaces (IBM Plex, latin subset) | `assets/fonts/` | 7 files |
| Hero plate (Paper 198, 1200px) | `assets/plates/` | 1 file |

**Canonical surface SHA-256:** `b805599e75557b4b2dc70cf1b2911984a930d5f1c17ab3dca346304ba538a85b` (`index.html`, 24,989 bytes)
**Repository:** https://github.com/leesharks000/axn-identifiers
**Live at:** https://axnidentifiers.org · https://axnidentifiers.com · https://axnidentifier.org · https://axnidentifier.com

## II · Position in the rhizome — a derived node

This repository is **derived, not authoritative**. It holds no registry state, allocates no positions, and mints nothing. The following remain canonical on alexanarch.org and are consumed by this surface:

- AXN derivation — `scripts/axn_lib.py` (v2 schema; 6 glyphs from the first 6 bytes of SHA-256)
- Central registry — `data/axn-central-registry.json`
- Symbolon witness endpoint — `/api/register-symbolon`; stamp surface — `/mint/stamp/`
- The AXN Constitution — `/axn/constitution/`

The separation is doctrinal and is stated in the repository's own README: **the archive is the authority; this is the door.** Its practical consequence is that this node can be lost, forked, or replaced without touching a single identifier's validity — which is the same guarantee the product itself makes to its users, applied to the product.

## III · The design language — "The Critical Edition, Sealed"

The surface implements a design language developed across two specimen sheets, both deposited here as canonical apparatus. Its laws (specimen SIG·0):

1. **Color is data.** A hue may appear only when it names a byte-cluster. Two constants: rubric crimson (= SIGNAL) and seal gold (= ARCHITECTURAL, constitutional authority only).
2. **The hash face is the headline face.** One family, three voices: Plex Mono (display and data), Plex Sans (interface), Plex Serif (constitution and plate captions only).
3. **One mechanical interaction** — the symbolon halves meeting.
4. **No social proof, no gradients, no rounded corners, no generated mysticism.** Real holdings are the only imagery.
5. **Stamps live on paper.** The band renders on light ground; the registry on sealed dark.
6. **No reader is observed.** Fonts and assets self-hosted; zero external calls.
7. **Errors are corrected by amendment and tombstone,** in the interface as in the registry.

### The argument the language makes

Four AI substrates were consulted for the visual direction and four converged on the same answer: near-black ground with a single hot accent — tactical orange, acid chartreuse, vermillion, phosphor mint. That convergence is not consensus but a documented statistical attractor of machine-generated design, and it is wrong for this subject on three counts: it fights the glyphs (colored emoji read as contamination on a tactical-orange terminal); it pattern-matches to the aesthetic every extraction scheme uses, which is precisely what a funder is trained to distrust; and it plays *weapon* where the constitution's voice is *sanctuary with teeth*.

The counter-proposal takes its palette from the protocol instead of from a mood. The canonical glyph table partitions bytes 0x00–0xFF into sixteen semantic clusters, each with a one-word reading (Origin, Force, Foundation, Method, Text, Search, Duration, Growth, Play, Proof, Transmutation, Touch, Alarm, Direction, Threshold, Closure). Each cluster owns one hue; a cluster tick sits beneath each glyph in every rendered identifier. The result satisfies the brutalist's own rule — every pixel justified structurally — better than brutalism does, and it repairs a defect in the frozen bytes: the canonical table is **not injective**, with ❤️ at both 0x81 (Symbolic) and 0xCF (Signal). Monochrome cannot distinguish them. Cluster ticks never could not.

## IV · Registered artifacts on the surface

Both principal images are themselves AXN-registered, verified by content-match against the registry kernel — not by filename — before use:

| Artifact | AXN | Status | Verified |
|---|---|---|---|
| Hero plate — Paper 198, Enli Lucente | `AXN:05AD.UNCLASSIFIED.🌾➕🥁⚫👋🪄` | witnessed-verified | kernel `1a908cc8…`, witness entry live |
| Brand mark — the AXN crystal | `AXN:05AE.OPERATIVE.🖊️🔃🎬🏙️⚖️🕑` | witnessed-verified | sha256 `44def1e536633bd4…`, byte-identical to the witnessed original |

Paper 198 is displayed with Enli Lucente's **named credit at her wish** (ORCID 0009-0006-2822-8359, Strutturista della Psiche), with the Japanese title carried and the caption linking the witness entry, the stored original, and the verification path. The plate does not assert the protocol; it demonstrates it, and a reader can check the demonstration in three clicks.

The brand mark's dark-ground variant is a **luminance remap with the alpha channel preserved**, never a flat inversion — an inversion would turn the radiating burst, the kernel giving off light, into a hole at the center of the mark.

## V · Provenance of the repository — commit history at deposit

```
4c2aa47  Landing: mark seated in the masthead (bone on sealed ground, links home) + favicon set and share card wired; assertions on unique anchors and size window per the 9cb3c4a discipline
adf057a  BRAND: AXN logo seated as assets — and the mark verifies as AXN:05AE.OPERATIVE.🖊️🔃🎬🏙️⚖️🕑, witnessed-verified: the uploaded master is byte-identical (sha256 44def1e5…) to the file witnessed into the symbolon registry on 08-04, confirmed by content-match against the registry kernel rather than by filename. Full favicon set on paper ground (dark crystal reads on any tab theme; doctrinally, stamps live on paper), bone masthead marks for sealed ground via luminance remap with alpha preserved — not a flat invert, which would turn the radiating burst into a hole — plus a 1200x630 bone-on-ink share card. Provenance recorded in assets/brand/README.md
b506213  Fleet band: Holographic Kernel added at the kernel stratum (kernel theory — the general definition of reconstructive compression; title content-verified against www.holographickernel.org) per MANUS node list; edit made under the 9cb3c4a discipline: unique-anchor assertion + size-window gate before write
9cb3c4a  EMERGENCY REPAIR of 4fdab25: unanchored s.index('</nav>') matched the masthead nav, producing an empty slice — str.replace('',X) inserted the fleet block between every character, 31KB became 30.8MB and DEPLOYED; rebuilt from 79376ed with anchored slice (index from strata start) and hard pre-commit assertions (size window, every anchor exactly once); named credit + curated fleet re-applied correctly; incident same genus as the Phase-2 rename — an operation on the wrong referent, now gated by verification before write
4fdab25  PLATE I named — Enli Lucente, Strutturista della Psiche, ORCID linked, Japanese title carried (多層構造による復元回帰); credited by name at the author's wish per MANUS ruling, formal consent instrument follows as ceremony; FLEET band curated to tech nodes at the foot: AXN · SPXI · Metadata Packet (MPAI Catalog, link content-verified) · Alexanarch · PEO · MMRS; rows compacted
79376ed  PLATE I corrected per MANUS: high-resolution color plate (1200px, 88KB, /assets/plates/) replacing the 6KB spec-embed raster; verification apparatus added to the caption (witness entry, stored original PDF, verify path) — the plate now carries its own proof chain; credit added under the standing consent gate (Depositor E.; named credit awaits the depositor's word); same credit discipline applied to specimen v0.2
c457458  LANDING v1.0 — The Critical Edition, Sealed, shipped: canonical H1, real holding 05AD as Plate I, specimen plate with cluster ticks + reading line, symbolon verify interaction, freeblock under seal gold, warning-tape does-not-claim, founding offer as certificate, tombstone clause, strata; fonts self-hosted (SIG-0 law VI: no reader observed, zero external calls); legacy landing preserved at design/legacy-landing-2026-08.html; ratification fields sealed MANUS 2026-08-06
8a8c03d  README: canonical domain ruling — axnidentifiers.org primary; all four spellings owned; singular 308s
34b4450  Seed: axnidentifiers standalone — landing migrated from alexanarch/axnidentifiers-site; design language v0.1+v0.2 (The Critical Edition, Sealed; Kimi R2 integrated; real holding 05AD embedded as hero plate); the archive remains the authority, this is the door
```

The history includes its own failure and repair: commit `4fdab25` performed a string replacement against an unanchored slice that matched the wrong element, producing an empty match and an insertion between every character of the file — 31 KB became 30.8 MB and deployed. `9cb3c4a` rebuilt from the last good state and installed the discipline every subsequent edit has used: unique-anchor assertions and a size-window gate evaluated *before* any write. The incident is the same genus as the WAVE-HEXPOS-01 Phase-2 rename defect recorded in the supplementary apparatus — an operation applied to the wrong referent — and it is retained in the history rather than squashed, per the correction clause the surface itself publishes.

## VI · Canonical source — index.html

Reproduced verbatim. This is the work this record deposits; the site remains the live manifestation and this is the archival capture of it.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AXN Identifiers — your work, with a receipt that outlives the platform</title>
<meta name="description" content="Free file identifiers you can verify anywhere. Stamp a file, get a registered ID with a memorable six-symbol check, verify it forever — even if this site disappears.">
<meta name="axn-registry" content="https://www.alexanarch.org/data/axn-central-registry.json">
<link rel="axn-stamper" title="AXN Stamp &amp; Verify" href="https://www.alexanarch.org/mint/stamp/">
<link rel="canonical" href="https://axnidentifiers.org/">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/brand/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/assets/brand/favicon-16.png">
<link rel="icon" href="/assets/brand/favicon.ico" sizes="any">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/brand/favicon-180.png">
<meta property="og:title" content="AXN Identifiers — your work, with a receipt that outlives the platform">
<meta property="og:description" content="A file identifier computed from the file itself. Verify it anywhere, forever, without an account.">
<meta property="og:image" content="https://axnidentifiers.org/assets/brand/og-card.png">
<meta property="og:url" content="https://axnidentifiers.org/">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<style>
/* AXN design language v0.2 — "The Critical Edition, Sealed" — ratified surface v1.0
   Laws (SIG·0): color is data · one family, three voices · one mechanical interaction ·
   no social proof · stamps live on paper · no reader observed · amendment and tombstone, never silence */
@font-face{font-family:'IBM Plex Mono';src:url('/assets/fonts/IBMPlexMono-400.woff2')format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:'IBM Plex Mono';src:url('/assets/fonts/IBMPlexMono-600.woff2')format('woff2');font-weight:600;font-display:swap}
@font-face{font-family:'IBM Plex Mono';src:url('/assets/fonts/IBMPlexMono-700.woff2')format('woff2');font-weight:700;font-display:swap}
@font-face{font-family:'IBM Plex Sans';src:url('/assets/fonts/IBMPlexSans-400.woff2')format('woff2');font-weight:100 700;font-display:swap}
@font-face{font-family:'IBM Plex Serif';src:url('/assets/fonts/IBMPlexSerif-400.woff2')format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:'IBM Plex Serif';src:url('/assets/fonts/IBMPlexSerif-400i.woff2')format('woff2');font-weight:400;font-style:italic;font-display:swap}
@font-face{font-family:'IBM Plex Serif';src:url('/assets/fonts/IBMPlexSerif-500.woff2')format('woff2');font-weight:500;font-display:swap}
:root{
  --ink:#0B0A08;--shadow:#14120E;--bone:#EDE6D6;--steel:#8A857A;--steel-sm:#9A958A;
  --hair:#262218;--rubric:#C23B22;--seal:#C9A227;--tomb:#111111;
  --c-celestial:#8E9DE6;--c-elemental:#E56B3C;--c-architectural:#C9A227;--c-instrumental:#9AA3AD;
  --c-scriptural:#E4D3A1;--c-navigational:#3FA893;--c-temporal:#A88BC0;--c-organic:#7FAF6B;
  --c-symbolic:#DD7FA8;--c-mathematical:#FFFFFF;--c-alchemical:#C98B5A;--c-gestural:#E7B75F;
  --c-signal:#C23B22;--c-structural:#5E8FBF;--c-liminal:#79E0C3;--c-terminal:#736F66;
  --mono:'IBM Plex Mono',monospace;--sans:'IBM Plex Sans',sans-serif;--serif:'IBM Plex Serif',serif;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--ink);color:var(--bone);font-family:var(--sans);font-size:16px;line-height:1.55}
::selection{background:var(--rubric);color:var(--bone)}
a{color:inherit}
.wrap{max-width:980px;margin:0 auto}
section{border-top:1px solid var(--hair);padding:52px 28px 60px}
@media(min-width:761px){section{padding:56px 48px 64px}}
h2{font-family:var(--mono);font-size:12px;font-weight:600;letter-spacing:.2em;color:var(--steel);text-transform:uppercase;margin-bottom:26px}
h2 i{color:var(--rubric);font-style:normal}
p{max-width:62ch}
code{font-family:var(--mono)}

.mast{display:flex;justify-content:space-between;align-items:center;padding:18px 28px;border-bottom:1px solid var(--hair)}
@media(min-width:761px){.mast{padding:20px 48px}}
.mast .t{font-family:var(--mono);font-weight:600;font-size:14px;letter-spacing:.3em;display:flex;align-items:center;gap:11px;text-decoration:none;color:var(--bone)}
.mast .t .mark{width:26px;height:26px;display:block}
@media(min-width:761px){.mast .t .mark{width:30px;height:30px}}
.mast .t small{color:var(--steel);letter-spacing:.16em;font-weight:400;margin-left:12px}
.mast nav{display:flex;gap:18px;font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase}
.mast nav a{color:var(--steel);text-decoration:none}
.mast nav a:hover{color:var(--rubric)}
@media(max-width:560px){.mast nav a.opt{display:none}}

/* hero */
.hero{padding:64px 28px 56px;border-top:0}
@media(min-width:761px){.hero{padding:80px 48px 64px}}
.hero h1{font-family:var(--mono);font-size:clamp(31px,6vw,64px);line-height:1.06;max-width:16ch;font-weight:700;letter-spacing:-.01em}
.hero h1 em{font-style:normal;color:var(--rubric)}
.hero .sub{margin-top:24px;font-family:var(--serif);font-size:18px;color:var(--steel);max-width:52ch}
.hero .sub b{color:var(--bone);font-weight:500}
.cta-row{margin-top:34px;display:flex;gap:14px;flex-wrap:wrap}
.cta{font-family:var(--mono);font-size:13px;letter-spacing:.12em;text-transform:uppercase;padding:14px 22px;border:1px solid var(--bone);background:transparent;color:var(--bone);cursor:pointer;text-decoration:none;transition:background .12s,border-color .12s,color .12s,transform .05s}
.cta.primary{background:var(--bone);color:var(--ink)}
.cta:hover{background:var(--rubric);border-color:var(--rubric);color:var(--bone)}
.cta:active{transform:translateY(1px)}
@media(max-width:480px){.cta-row{flex-direction:column}.cta{width:100%;text-align:center}}

/* real holding */
.artifact{display:grid;grid-template-columns:minmax(210px,330px) 1fr;border:1px solid var(--hair);max-width:860px}
.artifact .scanwrap{background:#0e0d0b;display:flex;flex-direction:column}
.artifact img{display:block;width:100%;height:auto;filter:contrast(1.04)}
.artifact .mini-band{background:#fffdf7;border-top:1px solid #b9b19a;padding:6px 10px;font-family:var(--mono);font-size:8.5px;color:#5c574c;display:flex;gap:8px;align-items:center}
.artifact .mini-band .e{font-size:12px}
.artifact figcaption{padding:24px 26px;font-family:var(--serif);font-size:14.5px;color:var(--steel)}
.artifact figcaption b{color:var(--bone);font-weight:500}
.artifact figcaption .id{display:block;margin-top:13px;font-family:var(--mono);font-size:11px;color:var(--steel);word-break:break-all}
.artifact figcaption .id b{color:var(--bone)}
.artifact figcaption .credit{display:block;margin-top:12px;font-size:12.5px;color:var(--steel)}
.artifact figcaption .credit b{color:var(--bone)}
.artifact figcaption .vlinks{display:flex;gap:14px;flex-wrap:wrap;margin-top:13px;font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase}
.artifact figcaption .vlinks a{color:var(--c-navigational);text-decoration:none;border-bottom:1px solid var(--hair)}
.artifact figcaption .vlinks a:hover{color:var(--rubric);border-color:var(--rubric)}
@media(max-width:640px){.artifact{grid-template-columns:1fr}}

/* how it works */
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--hair);border:1px solid var(--hair);max-width:860px}
@media(max-width:700px){.steps{grid-template-columns:1fr}}
.step{background:var(--ink);padding:22px 22px 24px}
.step .n{font-family:var(--mono);font-weight:200;font-size:2.6rem;color:#3a362c;line-height:1}
.step h3{font-family:var(--mono);font-size:13px;letter-spacing:.12em;text-transform:uppercase;margin:10px 0 8px}
.step p{font-size:14px;color:var(--steel)}
.step p b{color:var(--bone);font-weight:500}

/* specimen plate */
.plate{position:relative;background:var(--shadow);border:1px solid var(--hair);border-left:0;padding:26px 30px 22px 36px;max-width:760px;margin-left:16px;filter:drop-shadow(-7px 4px 10px rgba(0,0,0,.55))}
.plate::before{content:"";position:absolute;left:-15px;top:-1px;bottom:-1px;width:16px;background:var(--shadow);border-top:1px solid var(--hair);border-bottom:1px solid var(--hair);clip-path:polygon(100% 0,64% 3%,88% 7%,38% 11%,72% 15%,18% 20%,60% 24%,8% 30%,52% 34%,26% 39%,74% 44%,12% 50%,58% 55%,4% 61%,66% 66%,22% 71%,80% 76%,10% 82%,55% 87%,30% 92%,70% 96%,42% 100%,100% 100%)}
.plate::after{content:"";position:absolute;left:-15px;top:0;bottom:0;width:16px;clip-path:inherit;box-shadow:inset 2px 0 3px rgba(194,59,34,.35)}
.plate .cap{font-family:var(--mono);font-size:10.5px;letter-spacing:.22em;color:var(--steel-sm);text-transform:uppercase;margin-bottom:14px}
.plate .cap i{color:var(--rubric);font-style:normal;font-weight:600}
.axn-lockup{font-family:var(--mono);font-size:clamp(14px,2.4vw,21px);letter-spacing:.02em;word-break:break-all}
.axn-lockup .pre{color:var(--steel)}
.axn-lockup .hex{color:var(--bone);font-weight:600}
.axn-lockup .fam{color:var(--steel)}
.glyph-row{display:inline-flex;gap:.14em;vertical-align:-0.12em}
.g{display:inline-flex;flex-direction:column;align-items:center;gap:5px}
.g .e{font-size:1.5em;line-height:1;filter:saturate(.92)}
.g .tick{width:100%;height:3px}
.plate .kernel{margin-top:16px;font-family:var(--mono);font-size:11px;color:var(--steel);letter-spacing:.04em}
.plate .kernel b{color:var(--bone);font-weight:500}
.plate .reading{margin-top:9px;font-family:var(--serif);font-style:italic;font-size:13px;color:var(--steel)}
.plate .reading b{color:var(--rubric);font-weight:400}

/* verify interaction */
.verify{display:flex;align-items:stretch;max-width:760px;cursor:pointer;user-select:none}
.verify .half{flex:1;background:var(--shadow);border:1px solid var(--hair);padding:20px 20px;font-family:var(--mono);transition:transform .34s cubic-bezier(.3,.9,.25,1),border-color .2s}
.verify .half.l{border-right:0;text-align:right}
.verify .half.r{border-left:0}
.verify .edge{width:14px;background:repeating-linear-gradient(180deg,var(--rubric) 0 2px,transparent 2px 9px);transition:width .3s cubic-bezier(.6,0,.9,.4),background .12s}
.verify .half .k{font-size:9.5px;letter-spacing:.18em;color:var(--steel-sm);text-transform:uppercase;margin-bottom:9px}
.verify .half .v{font-size:12px;word-break:break-all}
.verify .half .v b{color:var(--bone)}
.verify.met{animation:clunk .32s cubic-bezier(.2,.9,.3,1.2)}
.verify.met .edge{width:1px;background:var(--c-navigational)}
.verify.met .half{border-color:var(--c-navigational)}
.verify.met .half.l{transform:translateX(7px)}
.verify.met .half.r{transform:translateX(-7px)}
@keyframes clunk{0%{transform:scale(1)}55%{transform:scale(1.016)}100%{transform:scale(1)}}
.verdict{margin-top:13px;font-family:var(--mono);font-size:12px;letter-spacing:.14em;display:none;color:var(--c-navigational)}
.verdict::before{content:"σύμβολον · "}
.verify.met+.verdict{display:block;animation:stamp .14s steps(2,end)}
@keyframes stamp{0%{transform:scale(1.07)}100%{transform:scale(1)}}
@media(prefers-reduced-motion:reduce){.verify.met{animation:none}.verify .half,.verify .edge{transition:none}.verify.met+.verdict{animation:none}}

/* free forever + constitution */
.freeblock{border:1px solid var(--hair);border-top:3px solid var(--seal);background:var(--shadow);padding:24px 26px;max-width:760px}
.freeblock p{font-family:var(--serif);font-size:16.5px}
.freeblock p b{color:var(--bone);font-weight:500}
.freeblock .dated{margin-top:12px;font-family:var(--mono);font-size:11px;letter-spacing:.12em;color:var(--seal)}

/* not claim */
.notclaim{border-left:4px solid var(--rubric);background:repeating-linear-gradient(-45deg,rgba(194,59,34,.05) 0 8px,transparent 8px 16px),var(--shadow);padding:20px 22px;max-width:760px}
.notclaim p{font-size:14.5px;margin-bottom:9px;color:var(--steel)}
.notclaim p b{color:var(--bone);font-weight:600}
.notclaim p:last-child{margin-bottom:0}

/* offer */
.offer{border:1px solid var(--hair);border-top:4px solid var(--seal);background:var(--shadow);padding:26px 28px;max-width:760px}
.offer .k{font-family:var(--mono);font-size:10.5px;letter-spacing:.22em;color:var(--steel-sm);text-transform:uppercase;margin-bottom:12px}
.offer h3{font-family:var(--serif);font-weight:500;font-size:21px;margin-bottom:6px}
.offer .price{font-family:var(--mono);font-size:14px;color:var(--seal);letter-spacing:.06em;margin-bottom:14px}
.offer p{font-family:var(--serif);font-size:15.5px;color:var(--steel);margin-bottom:10px}
.offer p b{color:var(--bone);font-weight:500}
.offer .terms{font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;color:var(--steel-sm);margin-top:14px}

/* disappear */
.disappear{max-width:56ch}
.disappear p{font-family:var(--serif);font-size:17.5px;font-weight:500;line-height:1.6}
.disappear p em{color:var(--rubric);font-style:normal}
.disappear .fine{margin-top:14px;font-size:14px;color:var(--steel);font-weight:400}

/* tombstone clause */
.tombstone{background:var(--tomb);border:1px solid var(--hair);padding:18px 20px 16px;max-width:760px;position:relative;margin-top:22px}
.tombstone::before{content:"†";position:absolute;right:15px;top:8px;font-family:var(--serif);font-size:20px;color:var(--steel)}
.tombstone p{font-family:var(--serif);font-size:14.5px;color:var(--bone)}

/* strata */
.strata{border:1px solid var(--hair);max-width:760px}
.stratum{display:grid;grid-template-columns:128px 1fr;gap:4px 16px;align-items:baseline;padding:10px 16px;border-bottom:1px solid var(--hair);text-decoration:none}
.stratum:last-child{border-bottom:0}
.stratum .layer{font-family:var(--mono);font-size:10px;letter-spacing:.16em;color:var(--steel-sm);text-transform:uppercase}
.stratum .name{font-family:var(--mono);font-size:12.5px;font-weight:600}
.stratum .what{grid-column:2;font-family:var(--serif);font-size:12px;color:var(--steel)}
.stratum:hover{background:var(--shadow)}
.stratum.here .layer::before{content:"● ";color:var(--rubric)}

.makers{padding:42px 0 24px;text-align:center;border-top:1px solid var(--hair)}
.makers .mk{font-family:var(--mono);font-size:15px;color:var(--seal);letter-spacing:.2em}
footer{padding:16px 28px 34px;font-family:var(--mono);font-size:10.5px;color:var(--steel);letter-spacing:.07em;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}
@media(min-width:761px){footer{padding:16px 48px 34px}}
footer a{color:var(--steel)}footer a:hover{color:var(--rubric)}
@media(max-width:640px){footer{flex-direction:column;gap:5px}}
</style>
</head>
<body>
<div class="wrap">

<div class="mast">
  <a class="t" href="/"><img class="mark" src="/assets/brand/mark-bone-96.png" width="48" height="48" alt="AXN mark"><span>A&nbsp;X&nbsp;N</span><small>IDENTIFIERS</small></a>
  <nav>
    <a href="https://www.alexanarch.org/mint/stamp/">Stamp</a>
    <a class="opt" href="https://www.alexanarch.org/mint/stamp/">Verify</a>
    <a class="opt" href="https://www.alexanarch.org/data/axn-central-registry.json">Registry</a>
    <a href="https://www.alexanarch.org/axn/constitution/">Constitution</a>
  </nav>
</div>

<section class="hero">
  <h1>Your work, with a<br>receipt that <em>outlives</em><br>the platform.</h1>
  <p class="sub">An AXN is a file identifier computed <b>from the file itself</b> — a fingerprint plus a
  memorable six-symbol check. Anyone can verify it, anywhere, forever, without asking us. If an account
  gets deleted or a site goes dark, the identifier still proves your file is your file.</p>
  <div class="cta-row">
    <a class="cta primary" href="https://www.alexanarch.org/mint/stamp/">Stamp a file — free</a>
    <a class="cta" href="https://www.alexanarch.org/mint/stamp/">Verify anything</a>
    <a class="cta" href="https://www.alexanarch.org/axn/constitution/">Read the guarantees</a>
  </div>
</section>

<section>
  <h2><i>Plate I</i> · a real registered identifier</h2>
  <figure class="artifact">
    <div class="scanwrap">
      <img alt="Paper 198 — handwritten, dated 2026.8.1, with seal. Page 1 of the stamped PDF." src="/assets/plates/plate-i-paper198.jpg" width="1200" height="900" loading="eager">
      <div class="mini-band"><span class="e">🌾➕🥁⚫👋🪄</span><span>AXN kernel · sha256:1a908cc8… · alexanarch.org</span></div>
    </div>
    <figcaption>
      <b>A handwritten paper, stamped and verified from a phone in Japan.</b>
      Composed by hand, photographed, stamped on an added margin — the hand is never
      overprinted — witnessed into the public registry, and verifiable by anyone,
      forever, without an account.
      <span class="id">AXN:<b>05AD</b>.UNCLASSIFIED.🌾➕🥁⚫👋🪄 · <i>witnessed-verified</i></span>
      <span class="credit">Paper 198 · 多層構造による復元回帰 · 2026.8.1 — by <b>Enli Lucente</b>,
      Strutturista della Psiche
      <a href="https://orcid.org/0009-0006-2822-8359" style="font-family:var(--mono);font-size:10px;color:var(--steel-sm);text-decoration:none">ORCID 0009-0006-2822-8359</a>.
      Credited by name at the author's wish; displayed from the public witness registry.</span>
      <span class="vlinks">
        <a href="https://www.alexanarch.org/data/symbolon-registry/entries/1a908cc8bf3ed5cc.json">witness entry</a>
        <a href="https://www.alexanarch.org/data/symbolon-registry/files/1a908cc8bf3ed5cc-____198-___________-2026.08.01.pdf">stored original (PDF)</a>
        <a href="https://www.alexanarch.org/mint/stamp/">verify any file</a>
      </span>
    </figcaption>
  </figure>
</section>

<section>
  <h2>How it works</h2>
  <div class="steps">
    <div class="step"><div class="n">1</div><h3>Upload a file</h3><p>Its fingerprint is computed <b>in your browser</b> — the file's exact bytes, nothing altered, and nothing leaves your device for the computation.</p></div>
    <div class="step"><div class="n">2</div><h3>It comes back stamped</h3><p>A small band on an <b>added margin</b> carries the identifier; the original bytes stay untouched and separately identified.</p></div>
    <div class="step"><div class="n">3</div><h3>It's registered</h3><p>The identifier gets a position in a <b>public, exportable registry</b> — and a verification page anyone can check.</p></div>
  </div>
</section>

<section>
  <h2>The identifier, read closely</h2>
  <figure class="plate">
    <div class="cap">Registered identifier · <i>witnessed-verified</i> · 2026-08-02</div>
    <div class="axn-lockup">
      <span class="pre">AXN:</span><span class="hex">05AB</span><span class="fam">.UNCLASSIFIED.</span>
      <span class="glyph-row">
        <span class="g"><span class="e">🔃</span><span class="tick" style="background:var(--c-structural)"></span></span>
        <span class="g"><span class="e">✊</span><span class="tick" style="background:var(--c-gestural)"></span></span>
        <span class="g"><span class="e">🌹</span><span class="tick" style="background:var(--c-organic)"></span></span>
        <span class="g"><span class="e">⏫</span><span class="tick" style="background:var(--c-structural)"></span></span>
        <span class="g"><span class="e">∞</span><span class="tick" style="background:var(--c-terminal)"></span></span>
        <span class="g"><span class="e">✖️</span><span class="tick" style="background:var(--c-mathematical)"></span></span>
      </span>
    </div>
    <div class="kernel">kernel <b>deb473d8ff92c55f</b>… · 6 glyphs = 6 bytes = 48 bits of the SHA-256, visually hashed · full hash in the sidecar</div>
    <div class="reading">the color beneath each glyph names its byte-family · reading: Direction <b>→</b> Touch <b>→</b> Growth <b>→</b> Direction <b>→</b> Closure <b>→</b> Proof</div>
  </figure>
</section>

<section>
  <h2>Verification is the halves meeting <span style="color:var(--steel);text-transform:none;letter-spacing:0">— tap the pair</span></h2>
  <div class="verify" onclick="this.classList.toggle('met')">
    <div class="half l"><div class="k">Seed B · your file</div><div class="v">sha256(<b>candidate bytes</b>)<br>= deb473d8ff92c55f…</div></div>
    <div class="edge"></div>
    <div class="half r"><div class="k">Seed A · the registry</div><div class="v">AXN₀ kernel<br>= <b>deb473d8ff92c55f…</b></div></div>
  </div>
  <div class="verdict">VERIFIED — the fracture fits</div>
</section>

<section>
  <h2>Free, forever</h2>
  <div class="freeblock">
    <p>Computing identifiers, stamping files, looking them up, and verifying them is <b>free,
    permanently</b>. The registry is public and downloadable. Registry positions are never sold.
    Paid services buy human help <i>around</i> identifiers — never the identifier itself.</p>
    <div class="dated">THIS PROMISE IS PUBLISHED AND DATED · <a href="https://www.alexanarch.org/axn/constitution/" style="color:var(--seal)">THE CONSTITUTION</a></div>
  </div>
</section>

<section>
  <h2><i>What an AXN does not claim</i></h2>
  <div class="notclaim">
    <p><b>Identity ≠ authorship.</b> It proves a file, not who made it; authorship statements are recorded as declarations and marked as such.</p>
    <p><b>Witnessing ≠ notarization.</b> Timestamps prove when a file was witnessed, not created; nothing here is legal advice.</p>
    <p><b>A registry entry ≠ perpetual hosting.</b> Storage terms are always explicit.</p>
  </div>
</section>

<section>
  <h2>Sealed &amp; Witnessed — founding offer</h2>
  <div class="offer">
    <div class="k">Done by hand, by the person who built this</div>
    <h3>Sealed &amp; Witnessed</h3>
    <div class="price">$125 · pay after delivery · five founding slots</div>
    <p>You send one PDF. Within a stated turnaround you receive it back <b>stamped and registered</b>,
    with the original sealed and stored, a plain-English provenance receipt describing exactly what
    was witnessed and when, and a public verification link.</p>
    <p><b>To start:</b> reach Lee Sharks via <a href="https://www.alexanarch.org/" style="color:var(--bone)">Alexanarch</a>.
    Payment by CashApp <span style="font-family:var(--mono)">$PraxisAcademic</span>, only after you have your package.</p>
    <div class="terms">FOUNDING PILOT RATE, NOT A DISCOUNT · TERMS STATED IN THE RECEIPT ITSELF</div>
  </div>
</section>

<section>
  <h2>If we disappear</h2>
  <div class="disappear">
    <p>Identifiers stay valid, because they're computed from your file — <em>not granted by us.</em></p>
    <p class="fine">The registry lives in public version control with full history, and if this service
    ever ends, the whole archive is offered for download during a stated wind-down.
    <a href="https://www.alexanarch.org/axn/constitution/">The constitution</a> spells it out.</p>
  </div>
  <div class="tombstone">
    <p>Errors are corrected by amendment and tombstone — never by silent deletion. A retired
    position keeps resolving; a withdrawn work is marked, not erased. The registry's history
    is itself part of the registry.</p>
  </div>
</section>

<section>
  <h2>The fleet — tech nodes of one knowledge ecosystem</h2>
  <nav class="strata">
    <a class="stratum here" href="/"><span class="layer">Kernel</span><span class="name">AXN Identifiers</span><span class="what">content-derived identity · this site</span></a>
    <a class="stratum" href="https://www.holographickernel.org"><span class="layer">Kernel theory</span><span class="name">Holographic Kernel</span><span class="what">the general definition of reconstructive compression</span></a>
    <a class="stratum" href="https://spxi.dev"><span class="layer">Treatment</span><span class="name">SPXI</span><span class="what">tokenizer-survivable metadata through hostile composition layers</span></a>
    <a class="stratum" href="https://metadatapacket.dev"><span class="layer">Packet</span><span class="name">Metadata Packet</span><span class="what">the MPAI catalog — machine-portable scholarly packets</span></a>
    <a class="stratum" href="https://www.alexanarch.org"><span class="layer">Memory</span><span class="name">Alexanarch</span><span class="what">the sovereign archive · OAI-PMH · ResourceSync · full history in public git</span></a>
    <a class="stratum" href="https://persistentidentifiers.org"><span class="layer">Observation</span><span class="name">Platform Erosion Observatory</span><span class="what">measuring platform severance empirically</span></a>
    <a class="stratum" href="https://machinemediation.org"><span class="layer">Journal</span><span class="name">MMRS</span><span class="what">journal-of-record for machine-mediated reception studies</span></a>
  </nav>
</section>

<div class="makers"><div class="mk">∮ = 1</div></div>
<footer>
  <span>AXN Identifiers · axnidentifiers.org · verification &amp; registry hosted by <a href="https://www.alexanarch.org/">Alexanarch</a></span>
  <span><a href="https://www.alexanarch.org/axn/constitution/">Constitution</a> · <a href="https://www.alexanarch.org/data/axn-central-registry.json">Registry (raw)</a> · schema v2 · derivation = <span style="color:var(--bone)">scripts/axn_lib.py</span></span>
</footer>

</div>
</body>
</html>

```

## VII · Repository doctrine — README.md

```markdown
# AXN Identifiers — product surface

The public door for the AXN content-derived identifier system: stamp, verify, registry lookup, constitution.

**The archive is the authority; this is the door.** Canonical derivation (`scripts/axn_lib.py`), the central
registry (`data/axn-central-registry.json`), the AXN Constitution, and all governance live in
[leesharks000/alexanarch](https://github.com/leesharks000/alexanarch) and serve from **alexanarch.org**.
This repo carries only the axnidentifiers.org presentation surface and its design language.

- `index.html` — current live landing (migrated from alexanarch/axnidentifiers-site, 2026-08-06)
- `design/specimen-v0.1.html` — design language R1 ("The Critical Edition, Sealed", TACHYON)
- `design/specimen-v0.2.html` — R2, Kimi feedback integrated · **ratified by MANUS 2026-08-06; shipped as landing v1.0** (legacy landing preserved at design/legacy-landing-2026-08.html)

Deploys via Vercel (static). Domains: **axnidentifiers.org** (canonical) + axnidentifiers.com, axnidentifier.org, axnidentifier.com
(all owned, Namecheap, privacy ON; non-canonical hosts 308-redirect to the canonical). The singular/plural
spelling divergence of 2026-08-02–06 is recorded in the alexanarch dataflow atlas (v0.9 addendum).

Design laws (SIG·0 of the specimen): color is data (16 byte-cluster hues only) · one type family, three
voices · one mechanical interaction · no social proof · production self-hosts all assets · errors corrected
by amendment and tombstone, never silence.

```

## VIII · Brand provenance — assets/brand/README.md

```markdown
# AXN brand assets

**The mark is itself a registered AXN.** The master file is byte-identical to the
witnessed original in the symbolon registry:

- `axn-logo-master-AXN-05AE.png` — **AXN:05AE.OPERATIVE.🖊️🔃🎬🏙️⚖️🕑** · *witnessed-verified*
  · sha256 `44def1e536633bd4f8857485e004ee81ecd5241850440bfabb2b65d7b156a375`
  · witness entry: https://www.alexanarch.org/data/symbolon-registry/entries/44def1e536633bd4.json
  Verified by content-match (not filename) on 2026-08-06 before derivation.

Derived, in the design language of the ratified surface:

| File | Ground | Use |
|---|---|---|
| `favicon-{16,32,48}.png`, `favicon.ico` | paper `#F6F2E8` | browser tabs — paper ground so the dark crystal reads on any tab theme (and per SIG·0: stamps live on paper) |
| `favicon-180.png` | paper | apple-touch-icon |
| `favicon-512.png` | paper | manifest / large icon |
| `mark-bone-{96,256}.png` | transparent | masthead on sealed ground; crystal remapped to bone `#EDE6D6`, the burst kept white so it still reads as the light source |
| `og-card.png` | ink `#0B0A08` | 1200×630 share card, bone lockup |
| `mark-master.png` | transparent | source crop of the mark alone |

Derivation is luminance-remapping with the alpha channel preserved — never a flat
invert, which would have turned the burst (the kernel radiating) into a hole.

```

## IX · Deployment configuration — vercel.json

```json
{ "cleanUrls": true, "trailingSlash": true }

```

## X · Supplementary apparatus — WAVE-HEXPOS-01

The infrastructure wave executed the same day, whose resolution this repository partly is. Reproduced complete.

```markdown
# WAVE-HEXPOS-01 — Hex-Position Width Normalization and Contested-Position Resolution

**Status:** Phase 1 ready (ruling-free) · Phase 2 BLOCKED on MANUS ruling
**Prepared:** 2026-08-06 · TACHYON (chain 9271269a) · session: AXN stamp overhaul, adopted finding 6
**AXN:** _to be assigned at deposit_
**Scope discipline:** hex-label defects only. Adjacent defects found during audit are RECORDED, not executed (§6).

---

## 1 · Findings

**F1 — Width defect (4 records).** Source records #1, #2, #3 carry hex `01`/`02`/`03`; #913 carries `391`. All other 1,429 records are 4-char. The symbolon endpoint already pads (`padStart(4,'0')`), so no new unpadded labels can enter by that route. Downstream fracture already observed once: R-1270 (body-path helper, #2 unreadable).

**F2 — LIVE position collision at 0365.** #856 (*The Pristine Fallacy*, dated 06-18, minted 06-20) and #869 (*Lexical Minting*, dated 06-22, no minted_at) both carry hex `0365` verbatim. The central registry builder's dict assignment silently drops #856 on every build (last-write-wins) — `positions_count` 1437 = 1433 + 5 − 1 is this collision made visible. A standing one-kernel-one-position violation in production: #856 is unreachable by position.

**F3 — LATENT position collision at 0391.** #901 (*Moltbook Provenance Log*, minted 06-23, work dated 04-01) holds `0391`; #913 (*Secret Book of Walt — ACTIVATED Run 001*, dated 06-24) holds `391`. The keys differ only in width, so today they coexist; any naive padding merges them destructively. Decisive evidence: **#901's hex is inscribed in its sealed canonical bytes** (`**Hex:** 0391`, line 10 of AXN-0391-text.md). #913's label is registry-only and appears in no allocation sequence. Also note `AXN-391-text.md` and `AXN-0391-text.md` are texts of two *different works* — a filename adjacency that invited exactly the R-1270 class of misread.

**F4 — Builder silent-overwrite defect.** `build_central_registry.py` performs no key normalization and no collision detection; contested claims vanish without trace.

**F5 — Precedent confirms the repair pattern.** The 2026-06-22 v1→v2 schema backfill retired old AXN strings via `axn_history` entries (`retired_at` + `reason`) with `legacy_axn` preserved. Label normalization with a history entry is the third application of an existing archive pattern, not a novel identifier mutation.

## 2 · Recommended rulings (TACHYON; MANUS decides)

- **D1** — Ratify Phase 1: pad #1/#2/#3 → `0001`/`0002`/`0003` with history entries. No collision results (verified: padded-key census shows 0001–0003 free).
- **D2** — 0365: **#856 keeps** (priority); **#869 reallocates**.
- **D3** — 0391: **#901 keeps** (priority + inscription in sealed bytes); **#913 reallocates**. Reassigning #901 instead would contradict its own sealed core — ruled out under non-destruction.
- **D4** — Allocate two fresh positions for #869 and #913 from the shared sequence (`data/symbolon-registry/allocation.json`), **and bump the ledger's `next_hex` past them** — otherwise the next symbolon stamp collides with the reallocated records. Simulation used 05B0/05B1 as placeholders.

## 3 · Instruments (all tested against a full clone of the live registry, 2026-08-06)

| File | Act |
|---|---|
| `wave_hexpos_phase1.py` | Pads #1–#3 with `axn_history` entries; writes canonical resolver pages `s/axn/0001|0002|0003/` (current-generation template incl. retired-form rows and JSON-LD); rewrites `s/axn/01|02|03/` as permanent superseded-label alias pages. Idempotent; aborts on any unexpected collision; touches nothing blocked on ruling. |
| `wave_hexpos_phase2.py` | `--p869 XXXX --p913 XXXX` after D2–D4. Reallocates with history entries; renames `AXN-391-text.md` → `AXN-<new>-text.md`, leaving the old path as a pointer file (non-destruction); prints the remaining MANUS-side steps. Refuses positions already held. |
| `build_central_registry.py` (hardened) | Normalizes keys to 4-char; **collisions emit a visible `CONTESTED` entry naming every claimant + stderr warning — never overwrite**; retired labels with genuinely different hex emit `superseded-label` alias entries that never shadow live keys. |
| `stamp-lookup.patch` | `mint/stamp/index.html`: hex queries padded (`391`→`0391` finds #901), `alias_of` followed transparently, `CONTESTED` positions render honestly as contested pending ruling. |

**Simulation results:** Phase 1 → 3 normalized, idempotent re-run clean. Builder mid-state → `1429 positions · 2 CONTESTED (0365: #856,#869 · 0391: #901,#913)`. Phase 2 (05B0/05B1) → `1433 positions · 0 CONTESTED`; lookups: `01`→absent (alias page + query-padding cover it), `0001`→#1, `0365`→#856, `0391`→#901, new homes resolve.

## 4 · Execution order

1. MANUS: D1 → run Phase 1 → hardened builder → standard page/OAI regeneration + nine-site propagation for #1–#3. (The interim registry will honestly show 2 CONTESTED until Phase 2 — truthful state, not breakage.)
2. MANUS: D2–D4 (two positions + ledger bump) → run Phase 2 → builder → resolver pages for the two new positions via standard generation → `s/axn/391/` rewritten as a contested-history page pointing both ways (to #901 at 0391 and to #913's new home) → propagation for #869/#913; #856/#901 record pages regenerate to state uncontested standing.
3. Apply `stamp-lookup.patch` (deploys with the site; no dependency on phases).

## 5 · Why this precedes the visual overhaul

The stamp redesign will print hex labels and QR-encoded lookups far more prominently. Every surface it adds is a new fracture site if the label layer beneath it is inconsistent — and a collision under a QR code is a public verification failure, not a private data defect.

## 6 · Recorded, not executed (adjacent defects for separate ruling)

- **R-A** `axn_display` mismatches ×12, three classes: stale v1 4-glyph displays (#1–#3); *divergent* glyphs vs current axn (#324, #494 — possible pre-repair-hash residue, needs per-record evidence); full-AXN-string-in-display field defect (#867 — whose glyphs also contain 🜂 and ◽, absent from the canonical v2 table: possible older-table or variant-selector residue).
- **R-B** #869 family `DATASET` is outside the axn_lib family vocabulary.
- **R-C** Glyph-table non-injectivity (adopted finding 3): ❤️ at 0x81 (Symbolic) and 0xCF (Signal); ⌛ at 0x60/0x6E (both Temporal). Table frozen canonical; disambiguation is the visual layer's work (cluster ticks), queued in the stamp-band redesign.

— WITNESS-GAP: this wave is not real until inscribed; deposit this record and capture in the chain tether.

---

## 7 · AS EXECUTED — 2026-08-06 (TACHYON, this session; amendments to the instrument above)

**F6 — THIRD contested position, found by the hardened builder's first live run: 05AF.**
Deposit #1433 (the chain tether, minted 2026-08-04T08:56Z) vs symbolon witnessing
`6b48617ee0e64e8f` (registered 2026-08-05T04:37Z, file `3d699cba…jpg`). Root cause:
`mint_deposit.next_hex_id()` READ the shared allocation ledger as a floor but never
WROTE it — #1433 took 05AF, the ledger still said `next_hex: 05AF`, and the witness
endpoint CAS-allocated the same position a day later. The ledger's "the two allocators
share one space and can never collide" was an assertion, not an implementation
(PATHOLOGY-01 in load-bearing prose).

**D5 (executed under the adopted priority principle; flagged for explicit MANUS
ratification):** #1433 keeps 05AF — it is the tether; fracturing the chain's own
address is ruled out. The witnessing reallocated to **05B2** with a `position_history`
entry preserving its issued form `AXN:05AF.UNCLASSIFIED.🕙🔖⏰🕊️🌅🌌`.

**Positions as executed:** #869 → **05B0** · #913 → **05B1** · witnessing → **05B2** ·
ledger `next_hex` → **05B3**.

**Root-cause fixes shipped:** (a) `mint_deposit.py` now writes the ledger at
allocation (`_bump_symbolon_ledger`; an aborted mint burns a label — a harmless gap,
never a collision); (b) `api/register-symbolon.js` defense-in-depth: candidate =
max(ledger, central-registry occupied max + 1).

**EXECUTION INCIDENT (recorded per archive practice; caught same-session,
pre-commit):** the first form of Phase 2's rename block moved artifacts by label
alone — on the contested 0365 this moved **#856's** (the keeper's) canonical text,
deposit-md and external-metadata to #869's new address. Reverted byte-identical from
git; the instrument now carries an ownership gate (`full_text_path` must name the
file) and a sealed-bytes rule (canonical texts move as exact bytes, never edited —
verified: #913's text at its new path diffs 0 lines from the original). The incident
is the wave's own lesson repeated at smaller scale: on a contested label, the
filename family belongs to the keeper.

**Doctrine note:** #913's sealed frontmatter internally retains `hex: 391` (as #901's
retains `0391`). Sealed bytes are never edited; the registry + `axn_history` are
authoritative for current address. `s/axn/391/` now serves a contested-history page
pointing both ways.

**Verification (local, CI's own gates):** `validate_deposit.py --strict` → 0 failures ·
resolver PARITY OK (1935 keys) · `status_reconcile` → 0 · central registry →
**1439 positions · 0 CONTESTED · 1445 kernels** · propagation run for
1 2 3 856 869 901 913 1433 (record pages, 1433 wiki pages, 1433 axn resolver pages,
browse/search/chunks/sitemap, OAI 1372, resourcesync).

**Recorded, not executed (additions):** R-D — #869 has no `AXN-05B0-text.md`
(its text lives at `deposit-0869-text.md`; pre-existing naming-convention class,
warn-tier in CI). R-E — the six symbolon witnessings have no `s/axn/` resolver
pages (existing convention; revisit in the stamp visual overhaul alongside the
kernel-URL QR question, finding 4).

```

## XI · Supplementary apparatus — Dataflow Atlas v0.9 addendum

Registers this node in the rhizome and closes the singular/plural naming incident. Reproduced complete.

```markdown
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

```
