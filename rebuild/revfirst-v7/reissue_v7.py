#!/usr/bin/env python3
"""Reissue in place: #1735 v6 -> v7. The Gallio synchronism restated throughout as the chain it is
(a stone that dates a proconsul; Acts placing Paul before him; an itinerary from Acts joining the letter to the visit),
granted nowhere as an independent date for 1 Thessalonians. At the author's ruling of 2026-11-06."""
import json, hashlib, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
RULING = ("Lee Sharks, 2026-11-06 14:28: \"it is very important that we do not endorse the gallio reading. the gallio inscription doesn't put thessalonian anywhere. "
          "it puts gallio around 50, and *acts* put paul around gallio. that is the same sort of circularity\"; 14:33: \"lets version 1735 in place and update it on revfirst as well\"")
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))
d = next(x for x in R["deposits"] if x["deposit_number"] == 1735); assert d["version"] == "v6"
T = ROOT / d["full_text_path"].lstrip("/"); s = T.read_text(encoding="utf-8")
E = []
def r(a, b): E.append((a, b))
r("The chronological gate confronting the maximal claim is priced, not dissolved.",
  "The chronological gate confronting the maximal claim is audited: its one material anchor, the Delphi inscription, dates Gallio and names no letter, and every link from it to a date for 1 Thessalonians is the corpus's own.")
# §II.2, paragraph by paragraph
r("The conventional dating of Paul is not direct in the sense of a dated autograph, but neither is it merely a circular habit projected backward from later canon formation. Its strongest fixed point is the Gallio synchronism. The Delphi inscription dates Gallio’s proconsulship of Achaia to July 51 – June 52 CE on the usual restoration, with some placing it a year later. Acts 18.12–17 places Paul before Gallio during his Corinthian residence. When that episode is correlated with the movements presupposed in 1 Thessalonians, the letter is normally dated around 50–51 CE. The correlation depends on the historical use of Acts and on reconstruction of Paul’s itinerary, and it is anchored at exactly one end: the stone dates the proconsul, while every further step is reconstruction from the corpus itself (Sánchez Bosch 1991: 336–47; Riesner 2011).",
  "The conventional dating of Paul rests on the Gallio synchronism. The Delphi inscription dates Gallio’s proconsulship of Achaia to July 51 – June 52 CE on the usual restoration, with some placing it a year later. Acts 18.12–17 places Paul before Gallio during his Corinthian residence. When that episode is correlated with the movements presupposed in 1 Thessalonians, the letter is dated around 50–51 CE. The correlation depends on the historical use of Acts and on a reconstruction of Paul’s itinerary, and it is anchored at exactly one end: the stone dates the proconsul, and every further step is reconstruction from the corpus itself (Sánchez Bosch 1991: 336–47; Riesner 2011).")
r("This is the hardest evidence against absolute Revelation First, and the argument becomes credible only by naming it. If Rev. 13.18 requires a date after 54, while 1 Thessalonians belongs around 50–51, the strongest claim fails under the standard chronology.",
  "The field sets this before absolute Revelation First as its hardest evidence, and the argument has to name it. If Rev. 13.18 requires a date after 54, and 1 Thessalonians is placed around 50–51, the strongest claim fails under the standard chronology.")
r("Its one material element – the Delphi inscription – constrains Gallio: it names a proconsul and a year, and it says nothing of Paul.",
  "Its one material element – the Delphi inscription – constrains Gallio: it names a proconsul and a year, and it says nothing of Paul or of Thessalonica.")
r("Revelation’s internal evidence was ruled permissive rather than coercive above. Paul’s internal evidence is owed the same verdict, and the same vocabulary. What remains of the gate under symmetrical audit is one stone that dates a proconsul, and a narrative that the question itself places under examination. The symmetry must not flatten degrees: the Gallio chain is stronger than the ambiguous Irenaean verb, and ‘corpus-internal’ names a class, not an equivalence – Acts is an independent narrative with historiographical claims of its own, not a self-dating colophon. Stated exactly, what would have to fail for absolute priority to pass is not the date of Acts but the historicity of the Gallio episode as an episode in Paul’s life, or its correlation with this letter. The synchronism raises the evidentiary cost of the maximal claim; it does not remove the model from comparison.",
  "Revelation’s internal evidence was ruled permissive above. Paul’s internal evidence is owed the same verdict, and the same vocabulary. The circularity is the one source criticism shows elsewhere: a date for the corpus is derived from the corpus, and then used to rule on the corpus’s order. What remains of the gate under symmetrical audit is one stone that dates a proconsul, and a narrative that the question itself places under examination. Stated exactly, what absolute priority must meet is the historicity of the Gallio episode as an episode in Paul’s life, and its correlation with this letter, both of them reported by the corpus whose order is in question. The synchronism leaves the model in comparison.")
r("treat the Acts correlation as the contested, corpus-internal datum it is – not a hypothetical maneuver but a live position in the field;",
  "treat the Acts correlation as the contested, corpus-internal datum it is, a live position in the field;")
r("The conventional date is strong because the links cohere, not because an inscription directly dates the letter. This distinction matters. It prevents the Gallio synchronism from becoming a talisman, while also preventing an absolute-priority argument from dissolving a serious historical chain by calling it merely inferential.",
  "The links cohere because they are drawn from one narrative; no inscription dates the letter. Stated so, the synchronism has no standing as a talisman, and an argument for absolute priority meets it at its links.")
r("An adequate maximal case must therefore attack a link rather than the existence of linkage. A letters-only Pauline chronology would need to place 1 Thessalonians later and then explain why its movements still fit the Corinthian episode that Acts synchronizes with Gallio.",
  "An adequate maximal case therefore meets the chain at a link. A letters-only Pauline chronology would place 1 Thessalonians by the letters’ own evidence, and would then answer for the movements the letter shares with the Corinthian episode Acts synchronizes with Gallio.")
r("The chronological gate is not a reason to close the question. It is the place where the strongest form becomes answerable.",
  "The chronological gate is no reason to close the question. It is the place where the strongest form becomes answerable.")
r("The result is not a concealed concession but a clarified claim ladder. Absolute priority is a priced hypothesis, and its price can now be stated exactly: the documentary status of the Acts correlation – a status contested in the field and unavailable, on this article’s method, as foreclosure.",
  "The result is a clarified claim ladder. Absolute priority is a priced hypothesis, and its price can now be stated exactly: the documentary status of the Acts correlation, contested in the field and unavailable, on this article’s method, as foreclosure.")
# §II.3
r("but to identify the chain on each side: Gallio is a stronger absolute synchronism than the ambiguous Irenaean verb, though its application to a particular letter still passes through Acts, and manuscript survival must not masquerade as a date of composition.",
  "but to identify the chain on each side: the Delphi inscription dates Gallio and reaches a particular letter only through Acts; the Irenaean verb has its subject unexpressed; and manuscript survival must not masquerade as a date of composition.")
# §V
r("because 1 Thessalonians is held to its date by the synchronism of Section II.",
  "because 1 Thessalonians is held to its received date by the chain of Section II, whose every link after the stone is the corpus’s own.")
# §VII
r("First Thessalonians is held to its conventional date by the Gallio synchronism; any arrow drawn toward it must first engage Section II.",
  "First Thessalonians is held to its conventional date by the Gallio chain of Section II, a stone that dates a proconsul joined to the letter by Acts; any arrow drawn toward it must first meet that chain.")
# §VIII
r(" – contestable, though not equally contestable at every link. A pre-70 date", ". A pre-70 date")
# §IX
r("A Neronian reading of the beast number and the Gallio synchronism create a genuine chronological gate, and the standard reconstruction places 1 Thessalonians before the earliest plausible Neronian Apocalypse – on the strength of a stone that dates a proconsul, and a narrative internal to the corpus under examination. Any case for absolute priority must address that gate directly. This article has not pretended to pass it; it has identified the exact links at which it can be passed or lost, and has shown where the load-bearing link sits under the same audit the article applies throughout – contestable in kind, strongest of its kind.",
  "A Neronian reading of the beast number and the Gallio synchronism form the chronological gate the field sets before it: the standard reconstruction places 1 Thessalonians before the earliest plausible Neronian Apocalypse on the strength of a stone that dates a proconsul, and a narrative internal to the corpus under examination. Any case for absolute priority meets that gate at its links. This article has identified the links, and shown that every one after the stone is the corpus’s own.")
vh = ("# Version history\n\nv6 (27 August 2026), deposited 3 November 2026. v7 (6 November 2026, in place), at the author's ruling (\"it is very important that we do not endorse the gallio reading. "
      "the gallio inscription doesn't put thessalonian anywhere. it puts gallio around 50, and *acts* put paul around gallio. that is the same sort of circularity\"). The Gallio synchronism is restated "
      "throughout as the chain it is: the Delphi inscription dates the proconsul and names neither Paul nor Thessalonica; Acts places Paul before him; an itinerary drawn from Acts and 1 Thessalonians joins the letter to the visit. "
      "The sentences that granted the chain standing beyond its links (that it is the hardest evidence, a stronger synchronism than the Irenaean verb, strong because its links cohere, contestable in kind and strongest of its kind) are withdrawn "
      "(abstract, §II.2, §II.3, §V, §VII, §VIII, §IX). No finding changed.\n\n# Bibliography")
r("# Bibliography", vh)
NB = lambda x: re.sub(r"([A-Za-z])\. (?=\d)", "\\1.\u00a0", x)
for a, b in E:
    if s.count(a) != 1: a, b = NB(a), NB(b)
    assert s.count(a) == 1, a[:90]; s = s.replace(a, b)
s2 = re.sub(r"^version: v6$", "version: v7", s, count=1, flags=re.M); assert s2 != s; s = s2
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = A.axn_glyph_from_hash(h); cl = A.axn_clusters_from_hash(h)
d.setdefault("reissue_history", []).append({"date": "2026-11-06", "from_version": "v6", "to_version": "v7", "hash_before_reissue": d["hash"], "axn_before_reissue": d["axn"], "reason": RULING,
  "changes": "The Gallio synchronism restated as its chain (stone dates proconsul; Acts places Paul before him; itinerary from Acts joins the letter), granted nowhere as an independent date for 1 Thessalonians; sentences granting it further standing withdrawn (abstract, §II.2, §II.3, §V, §VII, §VIII, §IX); version history added. Hash and AXN re-derived."})
prior = d["axn"]
d.update({"version": "v7", "hash": h, "axn_canonical": h, "emoji": g, "axn": A.compose_axn(d["hex"], d["family"], g), "clusters": cl, "axn_reading": A.axn_reading_from_clusters(cl)})
if d.get("wiki_article") and "priced, not dissolved" in d["wiki_article"]:
    d["wiki_article"] = d["wiki_article"].replace("priced, not dissolved", "audited: its one material anchor dates Gallio and names no letter")
a = "prices the chronological gate (the Nero cipher and the Gallio synchronism) without dissolving it"
assert a in d["description"]
d["description"] = d["description"].replace(a, "audits the chronological gate (the Nero cipher, and the Gallio synchronism, whose one material anchor dates the proconsul and names no letter)")
T.write_text(s, encoding="utf-8"); (ROOT / f"data/deposits/AXN-{d['hex']}.md").write_text(s, encoding="utf-8")
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump({prior: d["axn"]}, open(ROOT / "rebuild/revfirst-v7/axn-moves.json", "w"), ensure_ascii=False); print(prior, "->", d["axn"])
