"""The catalogue transform across the Aristotle–Theophrastus line. Plan: PLAN.md, sha256 87f81394aa4152a5e99c99d406a24242ca33a18436b2824d04d1bd3220c79d77.
    python3 run.py  -> results.json, run.log (stdout)"""
import json, re, unicodedata, pathlib
H = pathlib.Path(__file__).resolve().parent
PLAN = "87f81394aa4152a5e99c99d406a24242ca33a18436b2824d04d1bd3220c79d77"
L = (H.parents[2] / "data/corpora/diogenes-laertius/text/tlg001.txt").read_text(encoding="utf-8").split("\n")
RUNS = {"Speusippus": [(1374, 1391)], "Xenocrates": [(1420, 1495)], "Aristotle": [(1799, 1952)], "Theophrastus": [(1988, 2210)],
        "Demetrius": [(2331, 2375)], "Heraclides": [(2407, 2434)], "Chrysippus": [(3489, 3581), (3586, 3680)]}
NUM = re.compile(r"[α-ωϛ]′\.?")
STOP = set("περι των του της τα το τον την τους τοις ταις τας και η προς εκ εν υπερ κατα απο επι καθ μετα αλλο ψευδεπιγραφον".split())
def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("ς", "σ").replace("ʼ", " ").replace("᾽", " ").replace("’", " ")
    return re.findall(r"[α-ω]+", s)
def content(s): return [w for w in norm(s) if w not in STOP and len(w) >= 4]
def stems(s): return [w[:5] for w in content(s)]
def titles(name):
    out = []
    for a, b in RUNS[name]:
        for l in L[a - 1:b]:
            l = l.strip()
            if not NUM.search(l) or len(l) > 140: continue
            t = NUM.sub(" ", l); t = re.sub(r"[\[\]\.·,;]", " ", t); t = re.sub(r"\s+", " ", t).strip()
            if content(t): out.append(t)
    return out
EXT_A = ["Κατηγορίαι", "Περὶ ἑρμηνείας", "Ἀναλυτικὰ πρότερα", "Ἀναλυτικὰ ὕστερα", "Τοπικά", "Περὶ σοφιστικῶν ἐλέγχων", "Φυσικὴ ἀκρόασις", "Περὶ οὐρανοῦ",
         "Περὶ γενέσεως καὶ φθορᾶς", "Μετεωρολογικά", "Περὶ ψυχῆς", "Περὶ αἰσθήσεως καὶ αἰσθητῶν", "Περὶ μνήμης καὶ ἀναμνήσεως", "Περὶ ὕπνου καὶ ἐγρηγόρσεως",
         "Περὶ ἐνυπνίων", "Περὶ τῆς καθ᾽ ὕπνον μαντικῆς", "Περὶ μακροβιότητος καὶ βραχυβιότητος", "Περὶ νεότητος καὶ γήρως", "Περὶ ζωῆς καὶ θανάτου",
         "Περὶ ἀναπνοῆς", "Περὶ τὰ ζῷα ἱστορίαι", "Περὶ ζῴων μορίων", "Περὶ ζῴων κινήσεως", "Περὶ ζῴων πορείας", "Περὶ ζῴων γενέσεως", "Τὰ μετὰ τὰ φυσικά",
         "Ἠθικὰ Νικομάχεια", "Ἠθικὰ Εὐδήμεια", "Ἠθικὰ μεγάλα", "Πολιτικά", "Οἰκονομικά", "Τέχνη ῥητορική", "Περὶ ποιητικῆς", "Ἀθηναίων πολιτεία"]
SPUR_A = ["Περὶ κόσμου", "Περὶ χρωμάτων", "Περὶ ἀκουστῶν", "Φυσιογνωμονικά", "Περὶ φυτῶν", "Περὶ θαυμασίων ἀκουσμάτων", "Μηχανικά", "Προβλήματα",
          "Περὶ ἀτόμων γραμμῶν", "Ἀνέμων θέσεις καὶ προσηγορίαι", "Περὶ Ξενοφάνους, Ζήνωνος, Γοργίου", "Περὶ ἀρετῶν καὶ κακιῶν", "Ῥητορικὴ πρὸς Ἀλέξανδρον", "Περὶ πνεύματος"]
EXT_T = ["Περὶ φυτῶν ἱστορίας", "Περὶ φυτῶν αἰτιῶν", "Χαρακτῆρες", "Τὰ μετὰ τὰ φυσικά", "Περὶ αἰσθήσεων", "Περὶ λίθων", "Περὶ πυρός", "Περὶ ὀσμῶν", "Περὶ ἀνέμων",
         "Περὶ σημείων", "Περὶ κόπων", "Περὶ ἰλίγγων", "Περὶ ἱδρώτων", "Περὶ λιποψυχίας", "Περὶ παραλύσεως", "Περὶ τῶν ἐν ξηρῷ διαιτωμένων ἰχθύων"]
def run(cat, ext):
    S = {s: t for t in ext for s in stems(t)}; T = titles(cat); hits = []
    for t in T:
        f = stems(t)[0]
        if f in S: hits.append([t, S[f]])
    return {"catalogue": cat, "n": len(T), "matched": len(hits), "rate": round(len(hits) / len(T), 3), "hits": hits}
CONTROLS = ["Speusippus", "Xenocrates", "Demetrius", "Heraclides", "Chrysippus"]
res = {"plan_sha256": PLAN,
       "A_against_Aristotle_extant": [run(c, EXT_A) for c in ["Theophrastus"] + CONTROLS + ["Aristotle"]],
       "A2_against_Aristotle_spuria": [run(c, SPUR_A) for c in ["Theophrastus"] + CONTROLS + ["Aristotle"]],
       "B_against_Theophrastus_extant": [run(c, EXT_T) for c in ["Aristotle"] + CONTROLS + ["Theophrastus"]]}
json.dump(res, open(H / "results.json", "w"), ensure_ascii=False, indent=1)
for k in ("A_against_Aristotle_extant", "A2_against_Aristotle_spuria", "B_against_Theophrastus_extant"):
    print("==", k)
    for r in res[k]: print(f"  {r['catalogue']:<13} {r['matched']:>3}/{r['n']:<4} {100 * r['rate']:5.1f}%")
for k, c in (("A_against_Aristotle_extant", "Theophrastus"), ("B_against_Theophrastus_extant", "Aristotle")):
    r = [x for x in res[k] if x["catalogue"] == c][0]
    print("--", k, c, "hits:"); [print("    ", a, "<-", b) for a, b in r["hits"]]
