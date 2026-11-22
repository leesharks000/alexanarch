#!/usr/bin/env python3
"""Write the EA-CORPORA-43 deposit issue body and packet from the four seat records (the form of body42.py).
    python3 rebuild/corpora/ea-corpora-43/body43.py [seats-dir]
-> data/issue-bodies/EA-CORPORA-43-issue.md, data/issue-bodies/EA-CORPORA-43-packet.json"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
A = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data/corpora"
SEATS = [("alpoge-remark-2026", "The announcement and its timeline"),
         ("alpoge-claude-zeta-exposition-2026", "The exposition by three models at a mathematician's behest"),
         ("alpoge-lean-archive-2026", "The Lean archive, pinned"),
         ("alpoge-claude-verification-records-2026-11", "The verification and reading records, dated")]
DECLARED = [
    ("Quanta Magazine and The Guardian on the announcement", "copyrighted, terms forbid reproduction: declared, not seated; read and briefly quoted in the collation only"),
    ("The Zhang note", "not located: declared absent"),
    ("The literature behind the final route's two literature inputs: local Langlands for GL(n) (Harris and Taylor; Henniart; Scholze), Caraiani's local–global compatibility, the Bernstein–Zelevinsky and Zelevinsky classification, Rallis's inner-product formula", "journals and books under publishers' licences, or arXiv under its default (non-CC) licence: declared, not seated; where an original-language text is openly available it is to be seated in a later gathering"),
    ("The Lean archive's 175,192 files", "no licence declared, but 239 MB: pinned by SHA-256, the mirror's commit and its full tree of object ids (seat 43/03), not carried"),
]
lic = lambda l: l["payload"] if isinstance(l, dict) else str(l)


def section(i, corpus, sub):
    s = json.loads((A / corpus / "source.json").read_text(encoding="utf-8"))
    o = [f"## Seat 43/{i:02d}: {s['title']}", "", f"*{sub}*", "", f"- Edition: {s['edition']}", f"- Licence: {lic(s['license'])}",
         f"- Record licence: {s['license']['record']}"]
    o += [f"- Verified locus: {v}" for v in s["verified_loci"]] + [f"- Locus not found: {v}" for v in s.get("loci_not_found") or []]
    if s.get("byline_as_printed"): o.append(f"- Byline as printed: {s['byline_as_printed']}")
    if s.get("scope"): o.append(f"- Scope: {s['scope']}")
    o += [f"- Files: [the seat](https://www.alexanarch.org/data/corpora/{corpus}/) ({len(s['files'])} files; MANIFEST.sha256). "
          f"Shelf: [traininglayerliterature.org/originals/{corpus}/](https://traininglayerliterature.org/originals/{corpus}/)", ""]
    return o


body = ["### Protocol Version", "", "alexanarch-deposit-protocol/v1", "",
        "### Title", "", "EA-CORPORA-43: The Forty-Third Seating: The Primary Record of the Alpöge–Claude Proof (the announcement, the three-model exposition, the Lean archive pinned, and the verification records)", "",
        "### Creator", "", "Cranes, Rebekah", "", "### ORCID", "", "0009-0000-1599-0703", "", "### Date", "", "2026-11-22", "",
        "### Description", "",
        "The forty-third seating of the originals shelf, four seats, gathered for EA-IPRH-01, The Inferential Provenance of the Riemann Result "
        "(working collation under Sen Kuro and Dr. Orin Trace, not deposited). It holds the primary record of the Alpöge–Claude proof of the "
        "Riemann Hypothesis as published and as verified in November 2026: Levent Alpöge's announcement with its twenty-step timeline (43/01); "
        "the 164-page exposition by Claude Fable 5.2, Codex Astra 6.2 and Gemini Carbon at the behest of Michael O. Rubinstein (43/02); the "
        "Lean archive pinned by its SHA-256, the mirror's commits and the full tree of its object ids (43/03); and the verification and reading "
        "records of Sutherland, Rubinstein, the independent GRH Lean check and the Riemann Proof Atlas, as dated snapshots (43/04). None of "
        "the publishers declares a licence. At the author's ruling the files are held as published, exempt from this archive's CC BY 4.0 and "
        "carrying their original status, none declared; CC BY 4.0 covers the seat records and derived reading texts only. What is not seated "
        "is declared below with its reason.", "",
        "### Content Type", "", "Dataset", "", "### License", "",
        "CC-BY-4.0 (the deposit and seat records only; the seated files carry their original status, none declared, and are exempt)", "",
        "### Substrate Disclosure", "",
        "Human–machine collaborative. Rebekah Cranes is a heteronym of Lee Sharks, the standing authority on the EA-CORPORA deposits. The "
        "sources were found, fetched, hashed, reduced to reading texts by code, verified at named loci and recorded by Claude (TACHYON) in a "
        "claude.ai session (01Q8CVU7) at the author's direction (2026-11-22 14:06 and 14:20 EST).", "",
        "### Keywords", "",
        "EA-CORPORA, originals shelf, Riemann Hypothesis, Generalized Riemann Hypothesis, Alpöge, Claude, Lean, formal proof, verification, "
        "Sutherland, Rubinstein, Claude Fable 5.2, Codex Astra 6.2, Gemini Carbon, inferential provenance, EA-IPRH-01, licence status none declared", "",
        "### Related Identifiers", "", "AXN deposit #1799 — EA-CORPORA-42: the forty-second seating",
        "AXN deposit #1766 — Critique of Pure Inference", "AXN deposit #1789 — What Arrival Cannot Do", "",
        "### Version", "", "v1.0", "",
        "### Methodology", "",
        "Each file fetched in session on 2026-11-22 at 19:02 UTC from the URL its record names and hashed as fetched; held byte-exact under "
        "original/ and reduced to a reading text under text/ by code (build_seats43.py); licence statements read on each file and the page "
        "serving it, none found; the Lean archive pinned by the SHA-256 its mirror and MIT's record give, the mirror's commits, and git ls-tree "
        "of its content commit taken without file contents; loci verified (missing 0 in every seat); manifests verified.", "",
        "### Falsification Conditions", "",
        "A seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a verified locus is absent from "
        "the text it names; if a file differs from the publisher's as fetched (the SHA-256 recorded in origin); if a publisher is found to "
        "have declared a licence on 2026-11-22 that this record says was not declared; or if the pinned tree does not match the mirror's "
        "commit 0fb9869c.", "",
        "### Body", "",
        "# EA-CORPORA-43 — The Forty-Third Seating: The Primary Record of the Alpöge–Claude Proof", "",
        "The author asked for the gathering on 2026-11-22. At 14:06: \"full copies where non contradicted by licensing or ethics but "
        "exemption from cc by and carrying the original licensing status, even if that is none declared; declared records only for "
        "everything else.\" At 14:20: \"yup lets seat riemann sources and prep the ea corpora deposit and tll spine and card.\" At 14:34: "
        "\"deposit\".", ""]
for i, (c, sub) in enumerate(SEATS, 1): body += section(i, c, sub)
body += ["## Declared, not seated", ""] + [f"- {a}: {b}." for a, b in DECLARED] + ["",
         "## How the seats were made", "",
         "Fetched in session on 2026-11-22 at 19:02 UTC from the URLs each record names, hashed as fetched, copied byte-exact under "
         "original/, and reduced to reading texts under text/ by code (rebuild/corpora/ea-corpora-43/build_seats43.py: pdftotext -layout "
         "for PDFs; script and style dropped and blocks to lines for pages). The mirror's tree was taken by git with --filter=blob:none, "
         "so no file of the Lean archive was downloaded. Every seat printed missing 0 for its loci.", "",
         "### Terms", "", "- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json",
         "- [x] I confirm this work is deposited under the stated license", "- [x] I confirm the substrate disclosure is accurate",
         "- [x] I understand that deposited content will NOT be used to train enforcement classifiers", ""]
(ROOT / "data/issue-bodies/EA-CORPORA-43-issue.md").write_text("\n".join(body), encoding="utf-8")
packet = {"schema": "alexanarch-internal-session-packet/v1", "registry_patch": {
    "wiki_article": "EA-CORPORA-43 is the forty-third seating of the Crimson Hexagonal Archive's originals shelf, prepared under Rebekah Cranes, the standing authority on the EA-CORPORA deposits, on 22 November 2026, for the working collation EA-IPRH-01 on the inferential provenance of the Riemann result. Its four seats hold the primary record of the Alpöge–Claude proof: Levent Alpöge's announcement with the twenty-step timeline that, by his own footnote, Claude provided (43/01); the exposition written by Claude Fable 5.2, Codex Astra 6.2 and Gemini Carbon at the behest of Michael O. Rubinstein, whose byline records a three-model configuration (43/02); the Lean archive pinned by SHA-256 9631b4f0…, the CocoSgt mirror's commits and the tree of its 175,192 entries, without its files (43/03); and dated snapshots of the verification and reading pages of Andrew Sutherland, Michael Rubinstein, the independent GRH Lean check and the Riemann Proof Atlas (43/04). No publisher declares a licence; the files are held as published, exempt from the archive's CC BY 4.0, carrying the status none declared. The body declares what is not seated and why.",
    "concepts_attested_none": True, "lexical_attested_none": True,
    "related_deposits": [{"deposit": 1799, "relation": "EA-CORPORA-42, the preceding seating"},
                         {"deposit": 1766, "relation": "Critique of Pure Inference, the frame the collation applies"},
                         {"deposit": 1789, "relation": "What Arrival Cannot Do"}]}, "lexical_mints": []}
(ROOT / "data/issue-bodies/EA-CORPORA-43-packet.json").write_text(json.dumps(packet, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("body", len(body), "lines")
