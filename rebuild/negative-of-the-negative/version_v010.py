"""version_v010.py — EA-NEGONT-02 v0.10 from v0.9, transformed in place on the operator's rulings of 2026-10-31 (21:52 and 22:22 EDT), adopting the
NonWiki audit of the same day (each finding checked against the repository by the session before adoption).

Reads data/issue-bodies/EA-NEGONT-02-v09-issue.md; writes data/issue-bodies/EA-NEGONT-02-v010-issue.md.
Every change is an exact replacement that must match once; a miss stops the build."""
import pathlib, sys
R = pathlib.Path(__file__).resolve().parents[2]
src = (R / "data/issue-bodies/EA-NEGONT-02-v09-issue.md").read_text()
out = src
def rep(old, new, count=1):
    global out
    n = out.count(old)
    if n != count:
        sys.exit(f"expected {count} of: {old[:90]!r}, found {n}")
    out = out.replace(old, new)

def field(name):
    return out.split(f"### {name}\n\n", 1)[1].split("\n\n### ", 1)[0]

rep("and a First Traversal of Howl (EA-NEGONT-02 v0.9)", "and a First Traversal of Howl (EA-NEGONT-02 v0.10)", count=2)
rep("### Date\n\n2026-10-18", "### Date\n\n2026-10-31")
rep("### Version\n\nv0.9", "### Version\n\nv0.10")
rep("### Supersedes\n\n1671", "### Supersedes\n\n1690")
rep("**Specification · v0.9 · 2026-10-18 · supersedes v0.8 (#1671)**", "**Specification · v0.10 · 2026-10-31 · supersedes v0.9 (#1690)**")

D = field("Description")
rep(D, D + " Version 0.10 (2026-10-31) records the procedure as the dataset now runs it, on the operator's rulings adopting an outside audit of the /non entries: the field's two pools are held apart, the sources the composition disclosed and the reference sources added by research, and each comparison names its pool (§0.3, §3.1); every knowledge object's sources stand beneath its sentences (§4.5); the sentence quota is withdrawn (§4.12); the article comes first on the page (§4.13); and a kernel or delta derived from an earlier composition is labelled with it (§8.2). The historical rows stand as composed.")

S = field("Substrate Disclosure")
rep(S, S.replace("in session on 4–8 and 18 October 2026", "in session on 4–8, 18 and 31 October 2026")
        .replace("through nine versions transformed in place; the object, its confine, the premises of v0.8 and v0.9, the law of the suppressed witness and the rulings are the operator's",
                 "through ten versions transformed in place; the object, its confine, the premises of v0.8 and v0.9, the law of the suppressed witness, the rulings of v0.10 and all other rulings are the operator's")
        .replace("verified against the text before adoption, and the corrections are recorded in the specification.",
                 "verified against the text before adoption, and the corrections are recorded in the specification; v0.10 adopts an audit of the /non entries by ChatGPT (2026-10-31), each finding checked against the repository before adoption."))

K = field("Keywords")
rep(K, K.replace("disclosed field,", "disclosed field, disclosed pool, reference pool, attribution beneath,"))

RI = field("Related Identifiers")
rep(RI, "#1690 (EA-NEGONT-02 v0.9, superseded by this version); " + RI.replace("#1671 (EA-NEGONT-02 v0.8, superseded by this version)", "#1671 (v0.8)") + "; #1704 (What Is a /non Article?, whose account of the page this version adopts); #1719 (Meta-Aggregators of the Crimson Hexagon, whose census rows admitted the reference pool)")

M = field("Methodology")
rep(M, M + " Version 0.10 adds no measured case: it records the procedure the dataset follows since the rulings of 2026-10-29 and 2026-10-31, from an audit of 90 entry records and 13 close readings, each finding checked against the repository (the recomposition script's retained kernels and deltas, the attribution rule set against #1704, sentence lengths over 103 rows, three articles that reported an error their sources resolve, one saved file whose ledger hash did not match).")

# §0: the two questions and the confine
rep("0.3. The two questions, in order. **First:** what does the composition layer make of the sources it itself surfaces (T against L_F(B))?",
    "0.3. The two questions, in order. **First:** what does the composition layer make of the sources it itself surfaces (T against L_F(B_D), the disclosed pool alone, §3.1)?")
rep("**Second:** what would public knowledge look like, and how would it meet later reality, if the archive were admitted on equal terms, or composed in the archive's ontology where it is the suppressed witness, with the field carried whole (L_F(B) against L_A(B ∪ A))?",
    "**Second:** what would public knowledge look like, and how would it meet later reality, if the archive were admitted on equal terms, or composed in the archive's ontology where it is the suppressed witness, with the field carried whole (L_F(B) against L_A(B ∪ A), B the disclosed and reference pools together)? A source found only by reference research never stands as evidence of what the composition had before it.")

rep("The **disclosed field** B is the set of sources the layer surfaced for the address, by card or by name in its body.",
    "The **disclosed pool** B_D is the set of sources the layer surfaced for the address, by card, by source panel or by name in its body; the reference pool B_R is added by research (§3.1), and B written alone is the two together.")

# §3.1(a): the two pools
A0 = out.split("(a) **The disclosed field.** ", 1)[1].split("\n", 1)[0]
FIRST = "Every source on the transcript's card rail and every source its body names, fetched and saved as text, SHA-256 and fetch date recorded."
assert A0.startswith(FIRST), A0[:200]
rep("(a) **The disclosed field.** " + A0,
    "(a) **The field, in two pools**, kept apart and marked by origin in the field ledger. **B_D, the disclosed pool:** every source on the transcript's card rail, every title in its source panel and every source its body names. **B_R, the reference pool:** the entity's own pages, its Wikipedia article (or the record of its absence or redirect), and third-party sources a census record read, admitted on the operator's ruling of 2026-10-29 (\"as against their wikipedia articles if they exist, their own pages, etc.\"). A source in both is carried once, in B_D. B written alone is B_D ∪ B_R. A delta that finds a source available and not composed names B_D; a source of B_R alone cannot show what the composition had. " + A0.replace(FIRST, "For both pools, every source is fetched and saved as text, SHA-256 and fetch date recorded.", 1))

# §4.5 attribution beneath; §4.12–4.13 added after §4.11
rep("4.5. **Attribution.** Every composed claim carries its source in the sentence that states it.",
    "4.5. **Attribution.** The knowledge object is prose without provenance in its sentences. Every sentence's sources stand beneath it, by claim id, each with its locus and modality, so every claim stays inspectable sentence by sentence. A source is named in the prose only where who holds the claim is part of what is said: a reading held by a named scholar against another, a contest within the archive, a finding of the Capture Registry about a composition. Modality stays in the grammar of the sentence. (Version 0.9 put the source in the sentence that states each claim; the rows composed under it stand as composed.)")
rep("The compression faces on the card; AIO's transcript T is a record within it, opened on expansion (ruled 2026-10-08).",
    "The compression faces on the card; AIO's transcript T is a record within it, opened on expansion (ruled 2026-10-08). On the entity's page the knowledge object stands first (§4.13).")
i = out.index("\n## 5. Stage V")
out = out[:i].rstrip("\n") + ("\n\n4.12. **Length and form.** No sentence quota. The knowledge object is written in natural sentences under descriptive subheadings. Coverage is complete over the composed parts (body, rail, open block, channel log), and restatements are grouped by lineage under §3.6. No distinction is cut to shorten an article; what does not belong in the main account goes to the reception analysis or stays reachable in the apparatus."
                               "\n\n4.13. **The page.** The knowledge object, the final article form, comes first on the entity's page. The compression, the transcript, the field arm, the objects and the earlier instantiations follow it. The provisional steps are kept and reachable, and none of them precedes the article.\n") + out[i:]

# §8.2: derived objects labelled
rep("- **Authorship.** K is derived by script from the plan; no composer writes it.",
    "- **Authorship.** K is derived by script from the plan; no composer writes it.\n- **Correspondence.** A kernel or delta derived from an earlier composition is kept as a dated historical object, labelled with the composition it derives from, and does not evaluate the current one. A kernel written by a composer is labelled so until it is derived. The build records any row whose kernel or delta derives from a composition other than its current one and carries no such label; the record is a breach written into the output, never a block.")

# §11: rulings
rep("## 11. Rulings log\n\n",
    "## 11. Rulings log\n\n- 2026-10-31: on an audit of the /non entries by ChatGPT, each finding checked against the repository by the session: \"1. beneath. 2. split. 3. yes. adopted on all. id also say, that my understanding is that the provisional steps currently precede the final article form, and that that precedence should probably be reversed\" (21:52 EDT; §4.5, §3.1, §4.12, §4.13); then \"lets record the new procedure but leave historical records as they are for now\" (22:22 EDT). Applied the same evening: the page order in scripts/build_non.py; the derivative labels on all 103 rows (§8.2); the corrections of the Yale, WikiWho and Data Workers' Inquiry articles, their earlier sentences kept under row.corrections; the GDPval saved-file hash corrected to the bytes as saved. The 103 rows stand as composed under v0.9; their recomposition under §4.5 and §4.12 waits for the operator.\n")

(R / "data/issue-bodies/EA-NEGONT-02-v010-issue.md").write_text(out)
print("written", len(out))
