#!/usr/bin/env python3
"""#1812 EA-REVFIRST-MATTHEW-01 reissued in place v1.0 -> v1.1 (2026-11-27). The author, 2026-11-27: 04:16 "matthew. is treating. revelation.
like scripture."; 04:24, that more of the argument has to be rehearsed in How to Write Matthew ("so we remain accurate about what how to write
matthew shows, and we are bold in our claims about what we believe revelation first *will* show"); 05:01 "yup lets proceed" (the fold of the
body); 09:45 "yup, lets version 1.1. it should not show up twice on alexanarch home". Date and position kept; hash and AXN re-derived at the
same position and family; the prior hash, AXN and Figure 2 kept.   python3 rebuild/reissue-1812-v11/reissue_1812_v11.py"""
import json, hashlib, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[1]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); D = {x["deposit_number"]: x for x in R["deposits"]}
d = D[1812]; assert d["version"] == "v1.0", d["version"]
WORD = ('Lee Sharks, 2026-11-27: 04:16 "matthew. is treating. revelation. like scripture."; 04:24 "more of the argument has to be rehearsed ... '
        'so we remain accurate about what how to write matthew shows, and we are bold in our claims about what we believe revelation first *will* show"; '
        '09:45 "yup, lets version 1.1. it should not show up twice on alexanarch home".')
fp = ROOT / d["full_text_path"].lstrip("/"); old = fp.read_text(encoding="utf-8")
front = old[:old.index("\n---\n", 4) + 5]
s = (HERE / "candidate-v0.10.md").read_text(encoding="utf-8"); s = s[s.index("### The generative grammar"):]
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
a = s[s.index("*Grammata: Journal of Operative Philology. Draft v0.10"):s.index("**For the machine reader.**")]
rep(a, "*Grammata: Journal of Operative Philology. EA-REVFIRST-MATTHEW-01, v1.1, 27 November 2026 (v1.0 the same day; reissued in place). With the "
       "Crimson Hexagonal Archive and Claude (TACHYON; Anthropic) as contributors. The research record behind every claim is The Unfolding Map, v0.63; "
       "its ledger of relations (158 rows, each checked in a tagged text) is this paper's evidence. Greek is quoted from Nestle 1904 as seated in the "
       "archive, the Septuagint from Swete and Philo from Cohn–Wendland as seated; every quotation here was verified against those seats by machine.*\n\n")
rep("Two figures accompany this draft.", "Two figures accompany this paper.")
rep("Written down before counting, for this draft.", "Written down before counting, for the first version of this paper.")
rep("M7, new in this draft, the speaker's", "M7 the speaker's")
rep("Verified for this draft by bibliographic record:", "Verified for this paper by bibliographic record:")
rep("](REV-TO-MATTHEW-BEARERS.svg)", "](/data/attachments/how-to-write-matthew/REV-TO-MATTHEW-BEARERS.png)")
rep("](REV-TO-MATTHEW-MAP.svg)", "](/data/attachments/how-to-write-matthew/REV-TO-MATTHEW-MAP.png)")
a = s[s.index("Data: The Unfolding Map v0.63, sections 2AG–2BI"):]; a = a[:a.index("\n")]
rep(a, "Data: [The Unfolding Map v0.63](https://www.alexanarch.org/files/EA-HK-REVFIRST-02/notebook/UNFOLDING-MAP-v0.63-2026-11-27.md), sections 2AG–2BI, "
       "the working notebook, hosted beside the relations hologram (#1813) and replaced as it grows, each replaced copy kept by date; the notebook as it "
       "stood at the first version of this paper is [v0.52](https://www.alexanarch.org/drafts/UNFOLDING-MAP-v0.52-2026-11-27.md); the two figures as "
       "vector files ([Figure 1](https://www.alexanarch.org/data/attachments/how-to-write-matthew/REV-TO-MATTHEW-BEARERS.svg), "
       "[Figure 2](https://www.alexanarch.org/data/attachments/how-to-write-matthew/REV-TO-MATTHEW-MAP.svg); Figure 2 as it stood at v1.0, from 86 rows, "
       "is [kept](https://www.alexanarch.org/data/attachments/how-to-write-matthew/REV-TO-MATTHEW-MAP-v1.0.svg)); "
       "[the ledger](https://github.com/leesharks000/alexanarch/blob/main/rebuild/unfolding-map/map/rev-matthew-ledger.json) and the rest in the "
       "repository: `rebuild/unfolding-map/map/rev-matthew-ledger.json` (the ledger and its checking script); `rebuild/unfolding-map/tm/` (the pack "
       "and all run outputs, verbatim); `rebuild/unfolding-map/scripture/`, `strands/`, `heldout/`, `speaker/` (the counts of sections 0.6, S and XIV).")
rep(' "version": "0.7 (draft)",', ' "identifier": "EA-REVFIRST-MATTHEW-01",\n "version": "1.1",')
rep('"Matthew\'s material shared with Mark", "Matthew 15",', '"Matthew\'s material shared with Mark", "the control: the same procedure from another book into Matthew", "a published index of allusions and a lemmatized Septuagint for the scripture counts", "the unsearched verses of Matthew 11-12",')
assert "Not deposited" not in s and "this draft" not in s, [l[:80] for l in s.split("\n") if "this draft" in l or "Not deposited" in l]
KW = ["scriptural composition", "tacit scripture", "Septuagint"]
front = front.replace("\nversion: v1.0\n", '\nversion: "v1.1 (supersedes v1.0 in place, 2026-11-27)"\n'); assert "v1.1 (supersedes" in front
front = front.replace("  - Crimson Hexagonal Archive\n---", "  - Crimson Hexagonal Archive\n" + "".join(f"  - {k}\n" for k in KW) + "---"); assert "tacit scripture" in front
new = front + "\n# " + d["title"] + "\n\n" + s.rstrip("\n") + "\n"
h = hashlib.sha256(new.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h); prior = d["axn"]
CH = ("Sections 0 and P rewritten: the literary-genetic argument (#1735), how Revelation was kept from candidacy as a source (#1746, #1741), why the "
      "reach matters, and what the programme claims it will show, kept apart from what the paper shows. New section S, Matthew and scripture: five "
      "operations Matthew performs on the Septuagint set beside the same operations on Revelation. The ledger grown from 86 rows and 178 verses to 158 "
      "rows and 305 of 1,067 verses, the new regions in their steps (I.5a, II.6a, V.6a, VI.6c, VIII.5a, IX.4a, X.5a); XIII.1c; XIV with the new counts "
      "and failures (no order found; the count on direction did not decide); the machine-reader packet; Figure 2 redrawn from 158 rows, the v1.0 "
      "figure kept. One sentence reversed: v1.0 P.6 called the burden between an extant book and a supposed document symmetrical; v1.1 lays it on "
      "the supposed one. 321 quotations verified against the seats (221 at v1.0).")
d.setdefault("reissue_history", []).append({"date": "2026-11-27", "from_version": "v1.0", "to_version": "v1.1", "hash_before_reissue": d["hash"],
    "axn_before_reissue": prior, "title_before_reissue": d["title"], "reason": WORD, "changes": CH})
d.setdefault("axn_prior", []).append({"axn": prior, "hash": d["hash"], "until": "2026-11-27", "why": "reissued in place as v1.1 (the argument rehearsed; Matthew and scripture; the ledger at 158 rows)"})
d.update({"version": "v1.1 (supersedes v1.0 in place, 2026-11-27)", "hash": h, "axn_canonical": h, "emoji": g,
          "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl, "axn_reading": AX.axn_reading_from_clusters(cl), "date_modified": "2026-11-27"})
if "full_text_chars" in d: d["full_text_chars"] = len(new)
d["keywords"] = d["keywords"] + KW
a = "221 Greek quotations verified by machine against the seated texts."; assert a in d["description"]
d["description"] = d["description"].replace(a, "321 Greek quotations verified by machine against the seated texts (221 at v1.0).").rstrip() + (
    " Version 1.1 (27 November 2026, in place) rehearses the argument the demonstration sits inside (the literary-genetic argument; how Revelation "
    "was kept from candidacy as a source; why the reach matters), adds a section showing that Matthew handles Revelation as it handles the scripture "
    "it does not name, operation by operation beside the Septuagint, and brings the ledger to 158 relations reaching 305 of Matthew's 1,067 verses "
    "(86 and 178 at v1.0). It reports that no order of Revelation is kept in Matthew except one walk through the infancy, and that a count meant to "
    "decide direction did not.")
d["wiki_article"] = d["wiki_article"].rstrip() + (" Version 1.1, reissued in place on 27 November 2026, sets the demonstration inside the argument of "
    "the Revelation First programme and keeps apart what the paper shows, what the programme holds on grounds argued in other records, and what the "
    "programme claims it will show. Its new section on scripture sets five operations Matthew performs on the Septuagint at undisputed places (a "
    "phrase kept, a saying staged as an event, a scene told again with another bearer, two scriptures in one line, scripture turned in the open) "
    "beside the same operations performed on Revelation. The ledger stands at 158 relations reaching 305 of Matthew's 1,067 verses. The paper "
    "reports that Matthew draws on Revelation in no order, as it draws on Isaiah and the Psalms, with one exception in the infancy narrative, and "
    "that the question of direction is not decided by its counts.")
d.setdefault("modifications", []).append({"date": "2026-11-27", "field": "text", "reason": "reissued in place as v1.1 at the author's word; prior hash and AXN in reissue_history", "now": d["axn"]})
fp.write_text(new, encoding="utf-8")
dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(new, encoding="utf-8")
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump({prior: d["axn"]}, open(HERE / "axn-moves-20261127-1812-v11.json", "w"), ensure_ascii=False, indent=1)
print(1812, prior, "->", d["axn"], h, len(new.split()), "words")
