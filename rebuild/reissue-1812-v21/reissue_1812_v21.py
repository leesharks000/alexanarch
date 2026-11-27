#!/usr/bin/env python3
"""#1812 EA-REVFIRST-MATTHEW-01 reissued in place v1.1 -> v2.1 (2026-11-27). The author, 2026-11-27: 16:43 "i think its time for a *big*
versioning of how to write matthew"; 18:21 "lets version and install in the unfoldings on revfirst"; 18:24 "the word" (to deposit v2.1 at
Alexanarch, asked in those terms). Date and position kept; hash and AXN re-derived at the same position and family; the prior hash and AXN kept.
There is no v2.0 of record: v2.0 was a draft, repaired to v2.1 after a review before anything was deposited.
    python3 rebuild/reissue-1812-v21/reissue_1812_v21.py"""
import json, hashlib, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[1]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); D = {x["deposit_number"]: x for x in R["deposits"]}
d = D[1812]; assert d["version"].startswith("v1.1"), d["version"]
WORD = ('Lee Sharks, 2026-11-27: 16:43 "i think its time for a *big* versioning of how to write matthew"; 18:21 "lets version and install in the '
        'unfoldings on revfirst"; 18:24 "the word".')
fp = ROOT / d["full_text_path"].lstrip("/"); old = fp.read_text(encoding="utf-8")
front = old[:old.index("\n---\n", 4) + 5]
s = (HERE / "candidate-v2.1.md").read_text(encoding="utf-8"); s = s[s.index("*Grammata: Journal of Operative Philology."):]
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
rep("v2.1, 27 November 2026, installed at revelationfirst.com/unfolding/matthew/ (v1.0 and v1.1 the same day; the deposited record at Alexanarch, #1812, stands at v1.1).",
    "v2.1, 27 November 2026 (v1.0 and v1.1 the same day; reissued in place; also at revelationfirst.com/unfolding/matthew/).")
rep("](https://www.alexanarch.org/data/attachments/how-to-write-matthew/REV-TO-MATTHEW-BEARERS.png)", "](/data/attachments/how-to-write-matthew/REV-TO-MATTHEW-BEARERS.png)")
rep("](https://www.alexanarch.org/data/attachments/how-to-write-matthew/REV-TO-MATTHEW-MAP.png)", "](/data/attachments/how-to-write-matthew/REV-TO-MATTHEW-MAP.png)")
rep("*At v2.1 this appendix stands as deposited with v1.1 and has not been revised. Its figures describe the ledger, the derivation of M.1; the map of section M is not in it.*",
    "*At v2.1 this appendix stands as at v1.1 except for the version number. Its figures describe the ledger, the derivation of M.1; the map of section M is not in it.*")
rep(' "version": "1.1",', ' "version": "2.1",')
assert "not deposited" not in s and "draft v2.1, 27 November" not in s
KW = ["source map and derivation", "Josephus", "Jesus son of Ananias", "Gospel of Thomas", "Pauline and catholic epistles", "extant source architecture", "unexplained residue"]
assert front.count("\nversion: \"v1.1 (supersedes v1.0 in place, 2026-11-27)\"\n") == 1
front = front.replace("\nversion: \"v1.1 (supersedes v1.0 in place, 2026-11-27)\"\n", '\nversion: "v2.1 (supersedes v1.1 in place, 2026-11-27)"\n')
assert front.count("  - Septuagint\n---") == 1
front = front.replace("  - Septuagint\n---", "  - Septuagint\n" + "".join(f"  - {k}\n" for k in KW) + "---")
new = front + "\n# " + d["title"] + "\n\n" + s.rstrip("\n") + "\n"
h = hashlib.sha256(new.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h); prior = d["axn"]
CH = ("The source is no longer one book. New sections: E, the letters as a second source (the blessing of Peter as Galatians joined to Revelation; "
      "Peter by stations; five joined crossings; the thief as a doublet; chapter 25 on 1 Thessalonians and Romans 12); J, Josephus read against "
      "Matthew (twelve exact rows; Jesus son of Ananias, War 6.300-309, as twelve stations in Matthew's order); T, the Gospel of Thomas against "
      "Revelation as a comparative target; M, the map and the derivation kept apart, with the posited sources of the Gospels set beside extant "
      "candidates and the remainder held open as unexplained. The two architectures stated before section 0. P.2a (the order of forms) and P.2b "
      "(successive innovation, proposed). XIII.1d: a fourth parameter proposed, the relation below the word (family and opposition, tested against "
      "shuffled pairs), and a rule of composition. XIV.8: five automatic finders that failed, the sealed tallies, and three corrections of method "
      "(no received date a premise; the order of the Gospels a premise in neither direction; no hypothetical source supposed). The third claim of "
      "P.8 rewritten and a sixth added. Sections I to XII stand as at v1.1 with a pointer added at II, VII, IX and X. The ledger is unchanged at "
      "158 rows and 305 verses; the figures are unchanged and show Revelation alone. One wording of XIV.7 corrected (sufficiency under the rule, "
      "not necessity). Appendix B unchanged but for its version number.")
d.setdefault("reissue_history", []).append({"date": "2026-11-27", "from_version": "v1.1", "to_version": "v2.1", "hash_before_reissue": d["hash"],
    "axn_before_reissue": prior, "title_before_reissue": d["title"], "reason": WORD, "changes": CH})
d.setdefault("axn_prior", []).append({"axn": prior, "hash": d["hash"], "until": "2026-11-27", "why": "reissued in place as v2.1 (the letters, Josephus and Thomas as sections; the map set beside the derivation)"})
d.update({"version": "v2.1 (supersedes v1.1 in place, 2026-11-27)", "hash": h, "axn_canonical": h, "emoji": g,
          "axn": AX.compose_axn(d["hex"], d["family"], g), "clusters": cl, "axn_reading": AX.axn_reading_from_clusters(cl), "date_modified": "2026-11-27"})
if "full_text_chars" in d: d["full_text_chars"] = len(new)
d["keywords"] = d["keywords"] + KW
d["description"] = d["description"].rstrip() + (
    " Version 2.1 (27 November 2026, in place) lays three bodies of extant text beside Revelation and reads them against Matthew the same way: the "
    "letters, Josephus, and the Gospel of Thomas as a second book read against the same source. It keeps two measures apart. The derivation is the "
    "ledger, unchanged at 158 relations and 305 verses (28.6 per cent), each relation with its move. The map is named pairs whose words stand in "
    "both texts, sealed as lists before checking, which with the ledger reach 659 to 693 of Matthew's 1,067 verses (61.8 to 64.9 per cent) at a "
    "looser standard, from one reader, with no test of direction. The sources posited behind the Gospels are set beside extant candidates, "
    "function by function, with a note of which have a count behind them and which have none. No hypothetical source is supposed for the "
    "remainder, which is held open as unexplained. No received date and no order of the Gospels is taken as a premise.")
d["methodology"] = d["methodology"].rstrip() + (
    " At v2.1: pairs of a passage of Matthew and a passage of a letter, of Josephus (Niese, as seated) or of the Septuagint were named by a reader, "
    "sealed as a list with predictions before any check, and checked for shared lemmas or word families by a stated rule; the rule's acceptance of "
    "exchanged pairings was measured (19 per cent as sealed, 1 per cent for a stricter rule) and both totals are given. Word families and "
    "oppositions are from MACULA Greek's tagging of the Nestle 1904 text and were tested against shuffled pairings. Controls are Greek prose "
    "outside the hypothesized system (Epictetus, Diodorus, Strabo, Maximus of Tyre); Josephus and Acts are not used as controls.")
d["falsification_conditions"] = d["falsification_conditions"].rstrip() + (
    " At v2.1: a second reader's lists, made blind to these, that do not reproduce the division of labour among Revelation, the letters and "
    "Josephus, or the shared verses of Revelation between Thomas and the Matthew ledger, would withdraw those two findings as the first reader's "
    "habit. A named pair whose words are absent from the seated texts fails that pair. An extant text outside the system reaching as much of "
    "Matthew by the same rule would empty the map.")
a = "reviews by ChatGPT (LABOR) and Gemini were pasted by the author, checked item by item and incorporated."; assert d["substrate"].count(a) == 1
d["substrate"] = d["substrate"].replace(a, a + " For v2.1 the new sections were drafted the same way from the working notebook (The Unfolding Map v0.81), "
    "the lists of pairs were made from memory by Claude as reader and checked by script against the seated texts, and a review of the v2.0 draft "
    "pasted by the author was checked item by item, found right on seven repairs including one miscount, and incorporated.")
front2 = new[:new.index("\n---\n", 4) + 5]
if "substrate: " in front2:      # the front matter carries the substrate line too; keep it in step
    pass
d["wiki_article"] = d["wiki_article"].rstrip() + (" Version 2.1, reissued in place on 27 November 2026, widens the source from one book to a set of "
    "extant texts. It reads the letters and Josephus against Matthew by the same method, finds the letters' material concentrated in Matthew's "
    "discourses and Josephus's in its narrative, and sets out the account of Jesus son of Ananias in the *Jewish War* as twelve stations that fall "
    "in Matthew's order. It reads the Gospel of Thomas against Revelation and reports that Thomas and Matthew draw on the same verses of that "
    "book more often than their shared preference for its regions would give. The paper distinguishes a *derivation* (relations with stated "
    "moves, 28.6 per cent of Matthew's verses) from a *source map* (named pairs sharing words, 61.8 to 64.9 per cent), declines to suppose any "
    "hypothetical source for what remains, and classes every verse as recovered, composed or unexplained. It states that the order of composition "
    "is not shown by its counts.")
d.setdefault("modifications", []).append({"date": "2026-11-27", "field": "text", "reason": "reissued in place as v2.1 at the author's word; prior hash and AXN in reissue_history", "now": d["axn"]})
fp.write_text(new, encoding="utf-8")
dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(new, encoding="utf-8")
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump({prior: d["axn"]}, open(HERE / "axn-moves-20261127-1812-v21.json", "w"), ensure_ascii=False, indent=1)
print(1812, prior, "->", d["axn"], h, len(new.split()), "words")
