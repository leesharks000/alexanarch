#!/usr/bin/env python3
"""EA-CORPORA-43: build the four seats of the primary record of the Alpöge–Claude proof (the form of build_seats42.py).

    python3 -I build_seats43.py <stage-dir> <seats-dir>

<stage-dir> holds the files as fetched on 2026-11-22 19:02 UTC (MANIFEST.txt there gives their SHA-256) and the mirror's
tree listing. <seats-dir> is a staging folder until the operator says seat, then data/corpora/. Must print `missing 0`.

Licensing, at the author's ruling (2026-11-22 14:06 EST): "full copies where non contradicted by licensing or ethics but
exemption from cc by and carrying the original licensing status, even if that is none declared; declared records only for
everything else." No file seated here declares a licence; each is held as published, exempt from the archive's CC BY 4.0,
carrying "none declared". The Lean archive itself (239,275,554 bytes) is pinned, not carried: by SHA-256, by the mirror's
commit and its full tree of object ids.
"""
import hashlib, html, json, pathlib, re, shutil, subprocess, sys

ST = pathlib.Path(sys.argv[1]); SEATS = pathlib.Path(sys.argv[2])
TODAY = "2026-11-22"; FETCHED = "2026-11-22T19:02Z"
RULING = ("Lee Sharks, 2026-11-22 14:06 EST: \"full copies where non contradicted by licensing or ethics but exemption from cc by "
          "and carrying the original licensing status, even if that is none declared; declared records only for everything else\"; "
          "14:20 EST: \"yup lets seat riemann sources and prep the ea corpora deposit and tll spine and card\". Rebekah Cranes is the "
          "standing authority on the EA-CORPORA deposits (2026-11-22 00:33).")
RESEARCH = {"study": "EA-IPRH-01, The Inferential Provenance of the Riemann Result (working collation, Sen Kuro and Dr. Orin Trace, "
                     "not deposited)",
            "for": "the primary record of the Alpöge–Claude proof as published and as verified, read by the collation's checks"}
SPINE = "EA-CORPORA-43 (assembled 2026-11-22, not deposited)"
NONE = ("None declared. The publisher states no licence (checked 2026-11-22 on the file and the page that serves it). Held here "
        "as published, byte-exact, exempt from this archive's CC BY 4.0, and carrying the original status: none declared. "
        "Rights remain with the author(s).")
RECORD = "CC-BY-4.0 applies to this seat record and its derived text layer only, not to the files under original/."


def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def norm(s): return re.sub(r"\s+", " ", s)


def pdftext(src, dst):
    subprocess.run(["pdftotext", "-layout", str(src), str(dst)], check=True)


def webtext(src, dst):
    s = pathlib.Path(src).read_text(encoding="utf-8", errors="replace")
    s = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1>", "", s)
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = re.sub(r"(?i)</(p|div|li|tr|h[1-6]|section|article|table|pre|dd|dt)>", "\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    s = "\n".join(re.sub(r"[ \t]+", " ", l).strip() for l in s.splitlines())
    pathlib.Path(dst).write_text(re.sub(r"\n{3,}", "\n\n", s).strip() + "\n", encoding="utf-8")


WHY = {
    "alpoge-remark-2026": "THE ANNOUNCEMENT. The one line credited to Claude ('Claude's suggested length of chain of theta lifts ... was sqrt X'), and the twenty dated steps of a timeline 'Claude provided after a thorough search'.",
    "alpoge-claude-zeta-exposition-2026": "THE THREE-MODEL EXPOSITION. A byline that records a configuration at model grain; the dependency census of the 1,478,198 declarations; the discovery record set against the dependency record (section I.9); why the exponent is one half (section I.8).",
    "alpoge-lean-archive-2026": "THE FORMAL ARTIFACT, PINNED. What the collation's checks read, fixed by hash and by the tree of every file's object id, without carrying 239 MB that declares no licence.",
    "alpoge-claude-verification-records-2026-11": "THE VERIFICATION LAYER, DATED. Pages that update in place, held as they stood when the collation read them; the verification runs are themselves Claude-mediated ('checks run with Claude Code').",
}


def seat(name, meta, originals, texts, loci):
    d = SEATS / name
    if d.exists(): shutil.rmtree(d)
    (d / "original").mkdir(parents=True); (d / "text").mkdir()
    rows = []
    for src, rel in originals:
        shutil.copyfile(ST / src, d / rel); rows.append(rel)
    for src, rel, kind in texts:
        (pdftext if kind == "pdf" else webtext)(ST / src, d / rel); rows.append(rel)
    (d / "MANIFEST.sha256").write_text("".join(f"{sha(d / r)}  {r}\n" for r in sorted(rows)))
    found, missing = [], []
    for label, needle in loci:
        hit = [r for _, r, _ in texts if norm(needle) in norm((d / r).read_text(encoding="utf-8"))]
        (found if hit else missing).append(f"{label}: '{needle}' ({hit[0] if hit else 'not found'})")
    lines = sum((d / r).read_text(encoding="utf-8").count("\n") for _, r, _ in texts)
    meta.setdefault("scope", "the files as published, whole")
    meta["works"].update({"count": len(meta["works"]["list"]), "units": "texts"})
    meta.update({"lines_total": lines, "why_seated": WHY[name], "fetched": FETCHED})
    meta.update({"license": {"payload": NONE, "record": RECORD}, "research": RESEARCH, "ruling": RULING, "spine": SPINE,
                 "seated": TODAY, "verified_loci": found, "loci_not_found": missing,
                 "files": {r: ("as published, byte-exact" if r.startswith("original/") else "reading text reduced by code (build_seats43.py)") for r in rows},
                 "normalization": "text/ is derived by code: pdftotext -layout for PDFs; for pages, script and style dropped, block "
                                  "elements to lines, entities decoded. No text was corrected by hand."})
    (d / "source.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(name, "missing", len(missing))
    return len(missing)


M = {l.split()[1]: l.split()[0] for l in (ST / "MANIFEST.txt").read_text().splitlines()[1:]}
bad = 0
bad += seat("alpoge-remark-2026", {
    "seat": "EA-CORPORA-43/01", "corpus": "alpoge-remark-2026",
    "title": "Levent Alpöge, the announcement of the Riemann Hypothesis proof, with the twenty-step timeline (remark.pdf, 4 pp., 20 November 2026)",
    "edition": "https://alpo.ge/remark.pdf as served on 2026-11-22", "language": "English",
    "origin": {"url": "https://alpo.ge/remark.pdf", "fetched": FETCHED, "sha256_as_fetched": M["alpoge-remark.pdf"]},
    "works": {"list": [{"title": "The announcement, its remarks and the timeline 'Claude provided after a thorough search'", "text": "text/remark.txt"}]}},
    [("alpoge-remark.pdf", "original/remark.pdf")], [("alpoge-remark.pdf", "text/remark.txt", "pdf")],
    [("the attributed line", "Claude’s suggested"), ("the timeline's source", "So here is a rough timeline Claude provided after a thorough search"),
     ("step 8", "Iterated theta lifts"), ("step 14", "one would stop at 2/3 a priori")])
bad += seat("alpoge-claude-zeta-exposition-2026", {
    "seat": "EA-CORPORA-43/02", "corpus": "alpoge-claude-zeta-exposition-2026",
    "title": "The Alpöge–Claude proof of the Riemann hypothesis explained for the Riemann zeta function, by Claude Fable 5.2, Codex Astra 6.2 and Gemini Carbon at the behest of Michael O. Rubinstein (working draft, 21 November 2026, 164 pp.)",
    "edition": "zeta-paper.pdf on Michael Rubinstein's Waterloo page, as served on 2026-11-22", "language": "English (mathematics)",
    "origin": {"url": "https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/zeta-paper.pdf", "fetched": FETCHED, "sha256_as_fetched": M["rubinstein-zeta-paper.pdf"]},
    "byline_as_printed": "Claude Fable 5.2, Codex Astra 6.2, and Gemini Carbon at the behest of Michael O. Rubinstein",
    "works": {"list": [{"title": "Parts I–III, Computations, References", "text": "text/zeta-paper.txt"}]}},
    [("rubinstein-zeta-paper.pdf", "original/zeta-paper.pdf")], [("rubinstein-zeta-paper.pdf", "text/zeta-paper.txt", "pdf")],
    [("the byline", "at the behest of Michael O. Rubinstein"), ("the dependency set", "1,478,198 declarations"),
     ("§I.8", "Why the exponent is one half"), ("§I.9", "Dictionary with Alpöge’s announcement"),
     ("the parallel formulations", "These are parallel or earlier formulations")])
bad += seat("alpoge-lean-archive-2026", {
    "seat": "EA-CORPORA-43/03", "corpus": "alpoge-lean-archive-2026",
    "title": "The Lean archive of the Alpöge–Claude proof (lean.tar.gz, 14 parts, 239,275,554 bytes joined), pinned: its SHA-256, the CocoSgt mirror's commits and the full tree of its 175,192 entries; the mirror's README",
    "edition": "alpo.ge/lean.tar.gz.part01–part14 (20 November 2026); mirror github.com/CocoSgt/riemann-hypothesis-lean at 0fb9869c (content) and 7cbf7a0c (README)",
    "language": "Lean 4", "origin": {"archive_sha256": "9631b4f020199e580ba86178cb56c6e9b09f690c2369a80dc4334aa93f49c7fc",
        "archive_bytes": 239275554, "archive_sha256_attested_by": ["the mirror's commit message (0fb9869c)", "Andrew Sutherland's verification record, math.mit.edu/~drew/grh/ (seat 43/04)"],
        "mirror": {"repo": "CocoSgt/riemann-hypothesis-lean", "content_commit": "0fb9869c6e6d7b54b67de803af0e0be29d37fc22", "readme_commit": "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4",
                   "co_author_line": "both commits: Co-Authored-By: Claude Opus 5.5"},
        "fetched": FETCHED, "transport": "git over HTTPS, --filter=blob:none: the tree of object ids only, no file contents"},
    "scope": "Pinned, not carried: the 175,192 files of the archive stay out of this archive. original/GIT-TREE-0fb9869c.txt.gz is git ls-tree -r of the content commit (mode, type, object id, path); the README is the mirror's own (no licence declared; the mirror states that it adds none to an archive published without one).",
    "works": {"list": [{"title": "The mirror's README", "text": "text/mirror-README.txt"}]}},
    [("GIT-TREE-0fb9869c.txt.gz", "original/GIT-TREE-0fb9869c.txt.gz"), ("cocosgt-mirror-README.md", "original/mirror-README.md")],
    [("cocosgt-mirror-README.md", "text/mirror-README.txt", "web")],
    [("the credit line", "The proof in this repository is the work of"), ("the licence statement", "without a stated license")])
bad += seat("alpoge-claude-verification-records-2026-11", {
    "seat": "EA-CORPORA-43/04", "corpus": "alpoge-claude-verification-records-2026-11",
    "title": "The verification and reading records of the Alpöge–Claude proof as they stood on 22 November 2026: Sutherland's verification files (MIT), Rubinstein's index and the independent GRH Lean check (Waterloo), and the Riemann Proof Atlas",
    "edition": "the four pages as served on 2026-11-22 19:02 UTC; each updates in place, so these are dated snapshots", "language": "English",
    "origin": {"pages": [
        {"url": "https://math.mit.edu/~drew/grh/", "who": "Andrew Sutherland (MIT); 'checks run with Claude Code'", "sha256_as_fetched": M["mit-sutherland-grh.html"], "file": "original/mit-sutherland-grh.html"},
        {"url": "https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/", "who": "Michael Rubinstein (Waterloo)", "sha256_as_fetched": M["rubinstein-index.html"], "file": "original/rubinstein-index.html"},
        {"url": "https://mrubinst.github.io/grh-lean-verification/", "who": "the independent GRH Lean check linked from Rubinstein's page", "sha256_as_fetched": M["mrubinst-grh-lean-check.html"], "file": "original/mrubinst-grh-lean-check.html"},
        {"url": "https://rlankenau.github.io/rh/alpoge/", "who": "the Riemann Proof Atlas (rlankenau); 'Source at commit e50d0981'", "sha256_as_fetched": M["rlankenau-atlas.html"], "file": "original/rlankenau-atlas.html"}],
        "fetched": FETCHED},
    "works": {"list": [{"title": t, "text": f"text/{n}.txt"} for n, t in (("mit-sutherland-grh", "Verification files (Sutherland)"),
              ("rubinstein-index", "Alpöge/Claude proof of the GRH (Rubinstein)"), ("mrubinst-grh-lean-check", "GRH Lean Check"),
              ("rlankenau-atlas", "Riemann Proof Atlas"))]}},
    [(f"{n}.html", f"original/{n}.html") for n in ("mit-sutherland-grh", "rubinstein-index", "mrubinst-grh-lean-check", "rlankenau-atlas")],
    [(f"{n}.html", f"text/{n}.txt", "web") for n in ("mit-sutherland-grh", "rubinstein-index", "mrubinst-grh-lean-check", "rlankenau-atlas")],
    [("the archive's hash", "9631b4f020199e580ba86178cb56c6e9b09f690c2369a80dc4334aa93f49c7fc"), ("the Claude Code line", "checks run with Claude Code"),
     ("the atlas's commit", "e50d0981"), ("Rubinstein's announcement line", "found with Anthropic's Claude")])
print("missing total", bad)
