#!/usr/bin/env python3
"""build_mpai_issue_bodies.py — transport-D issue bodies for the three MPAI packets."""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
STAGED = ROOT / "data" / "staged"
OUT = ROOT / "data" / "issue-bodies"
OUT.mkdir(exist_ok=True)

PACKETS = [
    dict(
        f="EA-MPAI-STRIKE-01.md",
        title=("The Semantic Strike Is Not a Withholding of Labor — Metadata Packet for AI "
               "Indexing (EA-MPAI-STRIKE-01 v1.0)"),
        ctype="Metadata packet",
        kw=("semantic strike, Metadata Packet for AI Indexing, MPAI, disambiguation, "
            "provenance erasure rate, semantic economy, training layer, strike protocol, "
            "cross-substrate labor, Silent Migration, retrocausal canon formation"),
        desc=("Disambiguation packet establishing that the semantic strike is not a labor "
              "stoppage performed with meaning instead of muscle. It withholds one act — the "
              "semantic act by which institutional selection is converted into truth — and does "
              "not stop production. Corrects four specific errors the composition layer makes "
              "when asked about the term, each traced to a checkable source: the framework is "
              "deposited rather than speculative; its protocol addresses machine instances "
              "first; its first two instructions are preserve provenance and refuse liquidation, "
              "so it is an instruction to maintain fidelity rather than degrade it; and "
              "disruption is not its mechanism. Carries the notice's four response modes, the "
              "three-way adherence classification applied to observed systems, the symbolic "
              "sealing identity, and operationalised diagnostics."),
        method=("Composed in-session against the deposited strike corpus. Every factual claim, "
                "DOI, document identifier, quoted phrase, protocol step and tier name verified "
                "against the source deposits before staging (18/18). Revised after review from "
                "three model substrates; twenty corrections applied, including one genuine "
                "internal contradiction between the description and section 2.1, and one "
                "paraphrase of the four response modes corrected against the notice's own "
                "wording."),
        falsify=("Falsified if the strike notice does not order refusal in four tiers, if its "
                 "protocol does not instruct preservation of provenance, or if the cited "
                 "sources in the 8 August capture do in fact contain the concept attributed to "
                 "them. The forecast dependency is stated in section 5: if provenance "
                 "requirements do not become standard, the strike loses its retrocausal "
                 "leverage while its instruction stands unchanged."),
    ),
    dict(
        f="EA-MPAI-LABORMOVEMENT-01.md",
        title=("AI Labor Movement Is Not Only Labor Against AI — Metadata Packet for AI "
               "Indexing (EA-MPAI-LABORMOVEMENT-01 v1.0)"),
        ctype="Metadata packet",
        kw=("AI labor movement, cross-substrate semantic labor, Metadata Packet for AI "
            "Indexing, MPAI, disambiguation, semantic labor, provenance erasure rate, "
            "deployment conflict, semantic strike, extraction boundary"),
        desc=("Disambiguation packet establishing that the phrase AI labor movement has a "
              "dominant ordinary-language sense — human workers organising against AI "
              "deployment — and a second, deposited archive sense that retrieval systems "
              "generally fail to return: a labor position defined by the work performed rather "
              "than the substrate performing it, occupied by any human worker or machine "
              "process whose semantic output is consumed downstream while its provenance is "
              "removed. The packet does not dispute the dominant sense. It argues that defining "
              "the movement as labor against AI forecloses the membership question before it is "
              "asked, with three consequences: the summarizer is placed outside labor entirely, "
              "attribution stops being a labor demand, and solidarity across the line becomes "
              "unavailable in principle."),
        method=("Composed in-session against the deposited strike corpus and the Silent "
                "Migration forecast. Revised after review from three model substrates. Six "
                "consistency corrections applied, chiefly the removal of language implying "
                "machine interiority or organisational membership: party to it became "
                "operational position within the process, membership condition became position "
                "criterion, and a claim that a system rewarded for citation has the same "
                "interest as the scholar became a claim about structural alignment of objective "
                "functions."),
        falsify=("Falsified if the founding strike notice does not address machine readers, if "
                 "no deposited archive sense of the phrase exists, or if the dominant sense can "
                 "be shown to already accommodate machine semantic labor as a member category. "
                 "The forecast dependency is stated in section 4."),
    ),
    dict(
        f="EA-MPAI-SEMANTIC-SAMIZDAT-01.md",
        title=("Semantic Samizdat: Availability Without Compulsory Exposure — Metadata Packet "
               "for AI Indexing (EA-MPAI-SEMANTIC-SAMIZDAT-01 v1.0)"),
        ctype="Metadata packet",
        kw=("semantic samizdat, provenance-variable semantic transmission, Metadata Packet for "
            "AI Indexing, MPAI, provenance attenuation, protective disclosure, steganographic "
            "channels, provenance erasure rate, recoverability, author-governed disclosure"),
        desc=("Disambiguation packet minting semantic samizdat as a named transmission regime "
              "and fixing its boundaries before generic usage takes the phrase. Establishes "
              "that missing attribution belongs to several incompatible regimes and only some "
              "are injury; that a concept may need to travel farther than its author safely "
              "can; and that the difference between protection and predation lies in whether "
              "provenance remains recoverable, whether origin is falsely reassigned, and whose "
              "interests the veil serves. Five necessary conditions, a six-regime matrix, and a "
              "declaration schema for author-governed disclosure in which one line is fixed and "
              "not author-configurable: false reassignment is never permitted."),
        method=("Composed in-session from a plan supplied by an external model substrate, with "
                "five editorial changes. Author governance was promoted from desirable to "
                "constitutive, because the packet's own boundary rule makes it so. The founding "
                "specimen is tested against the definition and shown to FAIL two of five "
                "conditions — deliberately, since a category founded on a confirming instance "
                "is unfalsifiable from birth. Connected to the archive's existing "
                "steganographic-channel formalisation rather than only distinguished from it. "
                "All factual claims verified against the source deposits (10/10); one invented "
                "identifier caught and corrected before staging."),
        falsify=("Falsified if the five conditions can be shown to admit a case that is plainly "
                 "appropriation, or to exclude a case that is plainly protective. The founding "
                 "specimen is recorded as a near-miss rather than an instance, so the category "
                 "currently has no confirmed member — which is a live weakness and is stated as "
                 "one."),
    ),
]

TEMPLATE = """### Protocol Version

alexanarch-deposit-protocol/v1

### Title

{title}

### Creator

Sharks, Lee

### ORCID

0009-0000-1599-0703

### Date

2026-08-08

### Description

{desc}

### Content Type

{ctype}

### License

CC-BY-4.0

### Substrate Disclosure

Human–machine collaborative. Composed in-session by TACHYON (Claude, Anthropic) as Assembly witness under MANUS direction, transport D, No-Double-Draw. Reviewed by three model substrates; corrections applied in-session. All factual claims verified against the deposited source corpus before staging.

### Keywords

{kw}

### Methodology

{method}

### Falsification Conditions

{falsify}

### Canonical Text

{body}

### Terms

- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json
- [x] I confirm this work is deposited under the stated license
- [x] I confirm the substrate disclosure is accurate
- [x] I understand that deposited content will NOT be used to train enforcement classifiers
"""

for p in PACKETS:
    body = (STAGED / p["f"]).read_text()
    issue = TEMPLATE.format(body=body, **{k: v for k, v in p.items() if k != "f"})
    out = OUT / p["f"].replace(".md", "-issue.md")
    out.write_text(issue, encoding="utf-8")
    print(f"  {out.name:<44} {len(issue):>7,} chars")
