#!/usr/bin/env python3
"""Members as relations. Each read locus with a Gospel for target is restated as one or more pairs of relations, seed and target, in six slots:
agent, action, object, recipient, polarity, mode. Every slot that names wording gives the form as it stands in the seated verse, and the run checks it there.
The operators are then not assigned: they are computed from the difference of the two relations by the rules in DERIVE, written before the run.
Rules of entry: (1) the relation is the clause that holds the shared wording; (2) classes are given from the cited verses alone, not from their context;
(3) polarity is that of the clause as it states the deed; a minus must show a negative particle in the verse.
   python3 relations.py <alexanarch root> <engine dir> <out.json>"""
import sys, re, json, math, random, collections, pathlib
sys.path.insert(0, sys.argv[2]); import midrash as M
SIDE = dict(CHRIST="own", GOD="own", ANGEL="own", FAITHFUL="own", SEER="own", BAPTIST="own", YOUTH="own",
            ADVERSARY="against", RULER="against", GUARD="against", ALL="neutral", THING="neutral", FIGURE="neutral", CREATURE="neutral", OPEN="neutral")
EVENTLIKE = {"VISION-EVENT", "NARRATIVE-EVENT"}
def r(ag=None, act=None, obj=None, rec=None, pol="+", mode=None): return dict(ag=ag, act=act, obj=obj, rec=rec, pol=pol, mode=mode)
# ag, rec: (class, form) or (class, None) when the verb alone carries it;  act: (lemma, form);  obj: (class or None, lemma, form);  rec may be a list
L = {
"rev1.7→matt24.30": [(r(("ALL","φυλαι"),("κοπτω","κοψονται"),("CHRIST","αυτοσ","επ αυτον"),mode="PROPHECY"), r(("ALL","φυλαι"),("κοπτω","κοψονται"),mode="PROPHECY"))],
"rev1.7→john19.37": [(r(("ALL","οφθαλμοσ"),("οραω","οψεται"),("CHRIST","αυτοσ","αυτον"),mode="PROPHECY"), r(("ALL",None),("οραω","οψονται"),("CHRIST","αυτοσ","εισ ον"),mode="CITATION"))],
"rev3.5→matt10.32": [(r(("CHRIST",None),("ομολογεω","ομολογησω"),("FAITHFUL","αυτοσ","ονομα αυτου"),[("GOD","πατροσ μου"),("ANGEL","αγγελων")],mode="PROMISE"), r(("CHRIST","καγω"),("ομολογεω","ομολογησω"),("FAITHFUL","αυτοσ","εν αυτω"),[("GOD","πατροσ μου")],mode="PROMISE"))],
"rev3.5→luke12.8": [(r(("CHRIST",None),("ομολογεω","ομολογησω"),("FAITHFUL","αυτοσ","ονομα αυτου"),[("GOD","πατροσ μου"),("ANGEL","αγγελων")],mode="PROMISE"), r(("CHRIST","υιοσ του ανθρωπου"),("ομολογεω","ομολογησει"),("FAITHFUL","αυτοσ","εν αυτω"),[("ANGEL","αγγελων")],mode="PROMISE"))],
"rev19.9→matt22.3": [(r(None,("καλεω","κεκλημενοι"),(None,"γαμοσ","γαμου"),[("FAITHFUL","μακαριοι")],mode="BEATITUDE"), r(None,("καλεω","κεκλημενουσ"),(None,"γαμοσ","γαμουσ"),[("ADVERSARY","ουκ ηθελον")],mode="PARABLE"))],
"rev19.9→luke14.17": [(r(None,("καλεω","κεκλημενοι"),(None,"δειπνον","δειπνον"),[("FAITHFUL","μακαριοι")],mode="BEATITUDE"), r(None,("καλεω","κεκλημενοισ"),(None,"δειπνον","δειπνου"),[("ALL","κεκλημενοισ")],mode="PARABLE"))],
"rev5.2→mark1.7": [(r(("OPEN","τισ αξιοσ"),("λυω","λυσαι"),(None,"σφραγισ","σφραγιδασ"),mode="QUESTION"), r(("BAPTIST","ουκ ειμι"),("λυω","λυσαι"),(None,"ιμασ","ιμαντα"),pol="-",mode="STATEMENT"))],
"rev5.2→john1.27": [(r(("OPEN","τισ αξιοσ"),("λυω","λυσαι"),(None,"σφραγισ","σφραγιδασ"),mode="QUESTION"), r(("BAPTIST","ουκ ειμι εγω"),("λυω","λυσω"),(None,"ιμασ","ιμαντα"),pol="-",mode="STATEMENT"))],
"rev3.3→matt24.43": [(r(("CHRIST",None),("ηκω","ηξω"),(None,"κλεπτησ","κλεπτησ"),[("FAITHFUL","επι σε")],mode="THREAT"), r(("FIGURE","κλεπτησ"),("ερχομαι","ερχεται"),(None,"κλεπτησ","κλεπτησ"),[("FIGURE","οικοδεσποτησ")],mode="PARABLE"))],
"rev3.3→luke12.39": [(r(("CHRIST",None),("ηκω","ηξω"),(None,"κλεπτησ","κλεπτησ"),[("FAITHFUL","επι σε")],mode="THREAT"), r(("FIGURE","κλεπτησ"),("ερχομαι","ερχεται"),(None,"κλεπτησ","κλεπτησ"),[("FIGURE","οικοδεσποτησ")],mode="PARABLE"))],
"rev16.18+1.14→matt28.2-3": [(r(("THING","σεισμοσ"),("γινομαι","εγενετο"),mode="VISION-EVENT"), r(("THING","σεισμοσ"),("γινομαι","εγενετο"),mode="NARRATIVE-EVENT")),
                             (r(("CHRIST","κεφαλη αυτου"),("λευκοσ","λευκαι"),(None,"χιων","χιων"),mode="VISION-EVENT"), r(("ANGEL","ενδυμα αυτου"),("λευκοσ","λευκον"),(None,"χιων","χιων"),mode="NARRATIVE-EVENT"))],
"rev6.12→matt8.24": [(r(("THING","σεισμοσ"),("γινομαι","εγενετο"),mode="VISION-EVENT"), r(("THING","σεισμοσ"),("γινομαι","εγενετο"),mode="NARRATIVE-EVENT"))],
"rev13.13-14→john2.11": [(r(("ADVERSARY",None),("ποιεω","ποιει"),(None,"σημειον","σημεια"),[("ALL","ανθρωπων")],mode="VISION-EVENT"), r(("CHRIST","ιησουσ"),("ποιεω","εποιησεν"),(None,"σημειον","σημειων"),[("FAITHFUL","μαθηται")],mode="NARRATIVE-EVENT"))],
"rev18.23→john3.29": [(r(None,("ακουω","ακουσθη"),(None,"φωνη νυμφιου","φωνη νυμφιου"),[("ADVERSARY","εν σοι")],pol="-",mode="DOOM"), r(("BAPTIST","φιλοσ του νυμφιου"),("ακουω","ακουων"),(None,"φωνη νυμφιου","φωνην του νυμφιου"),mode="STATEMENT"))],
"rev18.23→john5.35": [(r(None,("φαινω","φανη"),(None,"λυχνοσ","λυχνου"),[("ADVERSARY","εν σοι")],pol="-",mode="DOOM"), r(("BAPTIST","εκεινοσ"),("φαινω","φαινων"),(None,"λυχνοσ","λυχνοσ"),mode="STATEMENT"))],
"rev18.21→john11.41": [(r(("ANGEL","αγγελοσ"),("αιρω","ηρεν"),(None,"λιθοσ","λιθον"),mode="VISION-EVENT"), r(("ALL",None),("αιρω","ηραν"),(None,"λιθοσ","λιθον"),mode="NARRATIVE-EVENT"))],
"rev19.18→john6.53": [(r(("CREATURE",None),("εσθιω","φαγητε"),("RULER","σαρξ","σαρκασ βασιλεων"),mode="COMMAND"), r(("ALL",None),("εσθιω","φαγητε"),("CHRIST","σαρξ","σαρκα του υιου"),mode="CONDITION"))],
"rev16.4→john2.9": [(r(("THING","υδατων"),("γινομαι","εγενετο"),(None,"αιμα","αιμα"),mode="VISION-EVENT"), r(("THING","υδωρ"),("γινομαι","γεγενημενον"),(None,"οινοσ","οινον"),mode="NARRATIVE-EVENT"))],
"rev1.17→matt28.4-5": [(r(("SEER",None),("πιπτω","επεσα"),(None,"νεκροσ","ωσ νεκροσ"),mode="VISION-EVENT"), r(("GUARD","τηρουντεσ"),("γινομαι","εγενηθησαν"),(None,"νεκροσ","ωσ νεκροι"),mode="NARRATIVE-EVENT")),
                       (r(("CHRIST",None),("φοβεομαι","μη φοβου"),None,[("SEER","επ εμε")],mode="VISION-EVENT"), r(("ANGEL","αγγελοσ"),("φοβεομαι","μη φοβεισθε"),None,[("FAITHFUL","γυναιξιν")],mode="NARRATIVE-EVENT"))],
"rev19.9+19.21+17.14→matt22.3-14": [(r(None,("καλεω","κεκλημενοι"),(None,"γαμοσ","γαμου"),[("FAITHFUL","μακαριοι")],mode="BEATITUDE"), r(None,("καλεω","κεκλημενουσ"),(None,"γαμοσ","γαμουσ"),[("ADVERSARY","ουκ ηθελον")],mode="PARABLE")),
                       (r(("CHRIST","καθημενου επι του ιππου"),("αποκτεινω","απεκτανθησαν"),("ADVERSARY","λοιποσ","οι λοιποι"),mode="VISION-EVENT"), r(("ADVERSARY","οι δε λοιποι"),("αποκτεινω","απεκτειναν"),("FAITHFUL","δουλοσ","δουλουσ"),mode="PARABLE")),
                       (r(("FAITHFUL","οι μετ αυτου"),("κλητοσ","κλητοι"),(None,"εκλεκτοσ","εκλεκτοι"),mode="STATEMENT"), r(("ALL","πολλοι"),("κλητοσ","κλητοι"),(None,"εκλεκτοσ","εκλεκτοι"),mode="STATEMENT"))],
"rev14.19→matt21.33": [(r(("ANGEL","αγγελοσ"),("τρυγαω","ετρυγησεν"),(None,"αμπελ","αμπελον"),mode="VISION-EVENT"), r(("FIGURE","οικοδεσποτησ"),("φυτευω","εφυτευσεν"),(None,"αμπελ","αμπελωνα"),mode="PARABLE"))],
"rev2.10→matt17.12": [(r(("FAITHFUL",None),("πασχω","μελλεισ πασχειν"),mode="COMMAND"), r(("CHRIST","υιοσ του ανθρωπου"),("πασχω","μελλει πασχειν"),mode="PROPHECY"))],
"rev1.3→matt26.18": [(r(("THING","καιροσ"),("εγγυσ","εγγυσ"),mode="STATEMENT"), r(("THING","καιροσ"),("εγγυσ","εγγυσ"),mode="STATEMENT"))],
"rev7.9→mark16.5": [(r(("FAITHFUL","οχλοσ"),("περιβαλλω","περιβεβλημενουσ"),(None,"στολη λευκη","στολασ λευκασ"),mode="VISION-EVENT"), r(("YOUTH","νεανισκον"),("περιβαλλω","περιβεβλημενον"),(None,"στολη λευκη","στολην λευκην"),mode="NARRATIVE-EVENT"))],
"rev6.15+19.17→mark6.21": [(r(("GOD","του θεου"),("δειπνον","δειπνον"),("RULER","μεγισταν","μεγιστανεσ"),[("CREATURE","ορνεοισ")],mode="VISION-EVENT"), r(("RULER","ηρωδησ"),("δειπνον","δειπνον"),("RULER","μεγισταν","μεγιστασιν"),[("RULER","μεγιστασιν")],mode="NARRATIVE-EVENT"))],
"rev9.3-4→luke10.19": [(r(None,("διδωμι","εδοθη"),(None,"εξουσια","εξουσια"),[("ADVERSARY","ακριδεσ")],mode="VISION-EVENT"), r(("CHRIST",None),("διδωμι","δεδωκα"),(None,"εξουσια","εξουσιαν"),[("FAITHFUL","υμιν")],mode="STATEMENT")),
                       (r(("ADVERSARY",None),("αδικεω","αδικησουσιν"),("ALL","ανθρωποσ","ανθρωπουσ"),mode="VISION-EVENT"), r(("THING","ουδεν"),("αδικεω","αδικησει"),("FAITHFUL","συ","υμασ"),pol="-",mode="STATEMENT"))],
"rev5.4→luke4.17": [(r(("ALL","ουδεισ"),("ανοιγω","ανοιξαι"),(None,"βιβλιον","βιβλιον"),pol="-",mode="VISION-EVENT"), r(("CHRIST",None),("ανοιγω","ανοιξασ"),(None,"βιβλιον","βιβλιον"),mode="NARRATIVE-EVENT"))],
"rev19.8+19.14→luke23.11": [(r(None,("περιβαλλω","περιβαληται"),(None,"λαμπροσ","λαμπρον"),[("FAITHFUL","αυτη")],mode="VISION-EVENT"), r(("RULER","ηρωδησ"),("περιβαλλω","περιβαλων"),(None,"λαμπροσ","λαμπραν"),[("CHRIST","αυτον")],mode="NARRATIVE-EVENT")),
                       (r(("FAITHFUL","στρατευματα"),("ακολουθεω","ηκολουθει"),("CHRIST","αυτοσ","αυτω"),mode="VISION-EVENT"), r(("RULER","στρατευμασιν"),("εμπαιζω","εμπαιξασ"),("CHRIST","αυτοσ","αυτον"),mode="NARRATIVE-EVENT"))],
"rev16.16→luke23.33": [(r(("THING","τοπον"),("καλεω","καλουμενον"),(None,"αρμαγεδων","αρμαγεδων"),mode="VISION-EVENT"), r(("THING","τοπον"),("καλεω","καλουμενον"),(None,"κρανιον","κρανιον"),mode="NARRATIVE-EVENT"))],
"rev16.16→john19.17": [(r(("THING","τοπον"),("καλεω","καλουμενον"),(None,"αρμαγεδων","αρμαγεδων"),mode="VISION-EVENT"), r(("THING","τοπον"),("λεγω","λεγεται εβραιστι"),(None,"γολγοθα","γολγοθα"),mode="NARRATIVE-EVENT"))],
"rev11.8→john19.20": [(r(None,("σταυροω","εσταυρωθη"),("CHRIST","κυριοσ","κυριοσ αυτων"),mode="VISION-EVENT"), r(None,("σταυροω","εσταυρωθη"),("CHRIST","ιησουσ","ιησουσ"),mode="NARRATIVE-EVENT"))],
"rev2.10→john20.27": [(r(("FAITHFUL",None),("γινομαι","γινου"),(None,"πιστοσ","πιστοσ"),mode="COMMAND"), r(("FAITHFUL","θωμα"),("γινομαι","γινου"),(None,"πιστοσ","πιστοσ"),mode="COMMAND"))],
"rev3.10→john17.15": [(r(("CHRIST","καγω"),("τηρεω","τηρησω"),(None,"πειρασμοσ","εκ τησ ωρασ του πειρασμου"),[("FAITHFUL","σε")],mode="PROMISE"), r(("GOD",None),("τηρεω","τηρησησ"),(None,"πονηροσ","εκ του πονηρου"),[("FAITHFUL","αυτουσ")],mode="PRAYER"))],
"rev9.11→john19.20": [(r(("ADVERSARY","αγγελον τησ αβυσσου"),("ονομα","ονομα"),(None,"εβραιστι","εβραιστι"),mode="VISION-EVENT"), r(("THING","τιτλον"),("γραφω","γεγραμμενον"),(None,"εβραιστι","εβραιστι"),mode="NARRATIVE-EVENT"))],
}
NEG = re.compile(r"\b(ου|ουκ|ουχ|μη|ουδε|ουδεισ|ουδεν|ουτε)\b")
def sq(s): return re.sub(r"\s+", " ", M.norm(s)).strip()
def forms(rel):
    out = []
    for k in ("ag", "rec"):
        v = rel[k]
        for c, f in (v if isinstance(v, list) else [v] if v else []):
            assert c in SIDE, c
            if f: out.append(f)
    if rel["act"]: out.append(rel["act"][1])
    if rel["obj"]: out.append(rel["obj"][2])
    return out
def side(c): return SIDE[c] if c else None
def DERIVE(s, t):
    """The rules, fixed before the run. Returns the set of features and of operators one pair of relations shows."""
    F, O = set(), set()
    sa, ta = (s["ag"] or (None,))[0], (t["ag"] or (None,))[0]
    same_act = s["act"][0] == t["act"][0]
    if not same_act: F.add("action changed")
    if sa and ta and sa != ta:
        flip = {side(sa), side(ta)} == {"own", "against"}; F.add("agent changed, side reversed" if flip else "agent changed, side kept")
    if bool(sa) != bool(ta): F.add("agent supplied" if ta else "agent removed")
    so, to = s["obj"], t["obj"]
    if so and to:
        if so[1] != to[1]: F.add("object changed")
        if so[0] and to[0] and so[0] != to[0]: F.add("object's party changed")
    elif so or to: F.add("object dropped" if so else "object supplied")
    sr = {c for c, _ in (s["rec"] or [])}; tr = {c for c, _ in (t["rec"] or [])}
    if sr and tr and sr != tr:
        if tr < sr: F.add("recipient narrowed")
        elif {side(c) for c in sr} == {"own"} and "against" in {side(c) for c in tr} or {side(c) for c in sr} == {"against"} and "own" in {side(c) for c in tr}: F.add("recipient changed, side reversed")
        else: F.add("recipient changed, side kept")
    if s["pol"] != t["pol"]: F.add("negative removed" if s["pol"] == "-" else "negative set")
    if s["mode"] != t["mode"] and not (s["mode"] in EVENTLIKE and t["mode"] in EVENTLIKE): F.add("mode changed")
    # operators as differences
    if s["mode"] == "VISION-EVENT" and t["mode"] == "NARRATIVE-EVENT" and same_act and s["pol"] == t["pol"] and "agent changed, side reversed" not in F: O.add("EVENT")
    if same_act and "agent changed, side reversed" in F: O.add("REVERSE-DOER")
    if "recipient changed, side reversed" in F and same_act: O.add("REVERSE-RECIPIENT")
    if "negative removed" in F: O.add("UNDO")
    if "negative set" in F: O.add("NEGATE")
    if same_act and "object changed" in F: O.add("SUBSTITUTE-OBJECT")
    if not same_act and so and to and so[1] == to[1]: O.add("SUBSTITUTE")
    if same_act and "agent changed, side kept" in F: O.add("TRANSFER-ATTRIBUTE")
    if t["mode"] == "CITATION": O.add("CITE-AS-SCRIPTURE")
    return F, O
def nb(X, y, G):
    V = sorted({f for x in X for f in x}); ok = 0; conf = collections.Counter()
    for i in range(len(X)):
        idx = [j for j in range(len(X)) if j != i]; prior = collections.Counter(y[j] for j in idx); best, bs = None, -1e9
        for g in G:
            if not prior[g]: continue
            sc = math.log(prior[g] / len(idx))
            for f in V:
                c = sum(1 for j in idx if y[j] == g and f in X[j]); p = (c + 1) / (prior[g] + 2); sc += math.log(p if f in X[i] else 1 - p)
            if sc > bs: best, bs = g, sc
        ok += best == y[i]; conf[(y[i], best)] += 1
    return ok / len(X), conf
if __name__ == "__main__":
    S = M.Seats(sys.argv[1]); DS = {d["id"]: d for d in json.loads((pathlib.Path(sys.argv[2]) / "derivations.json").read_text(encoding="utf-8"))["derivations"]}
    rows, bad = [], []
    for i, pairs in L.items():
        D = DS[i]; st, tt = sq(S.get(D["seed"])), sq(S.get(D["target"])); F, O = set(), set(); modes = set()
        for s, t in pairs:
            for rel, txt, wh in ((s, st, "seed"), (t, tt, "target")):
                for f in forms(rel):
                    if f not in txt: bad.append((i, wh, f))
                if rel["pol"] == "-" and not NEG.search(txt): bad.append((i, wh, "minus without a particle"))
            f, o = DERIVE(s, t); F |= f; O |= o; modes |= {"seed is " + s["mode"], "target is " + t["mode"]}
        hand = {x["op"] for x in D["steps"]}; g = D["target"].split(":", 1)[1].split()[0]
        rows.append(dict(id=i, gospel=g, relations=len(pairs), features=sorted(F), modes=sorted(modes), derived=sorted(O), hand=sorted(hand)))
    print("loci:", len(rows), "| relation pairs:", sum(r_["relations"] for r_ in rows), "| forms not found in the seat:", bad or "none")
    G = ["Matt", "Mark", "Luke", "John"]; y = [r_["gospel"] for r_ in rows]; print(dict(collections.Counter(y)))
    COMMON = ["EVENT", "REVERSE-DOER", "UNDO", "NEGATE", "SUBSTITUTE-OBJECT", "SUBSTITUTE", "TRANSFER-ATTRIBUTE", "CITE-AS-SCRIPTURE"]; agree = {}
    print("\nthe operators computed against the operators assigned (computed&assigned / computed only / assigned only):")
    for o in COMMON:
        a = sum(1 for r_ in rows if o in r_["derived"] and o in r_["hand"]); b = sum(1 for r_ in rows if o in r_["derived"] and o not in r_["hand"]); c = sum(1 for r_ in rows if o not in r_["derived"] and o in r_["hand"])
        agree[o] = (a, b, c); print(f"  {o:20} {a:2} / {b:2} / {c:2}")
    res = {}
    for name, X in (("differences of slots", [set(r_["features"]) for r_ in rows]), ("differences and modes", [set(r_["features"]) | set(r_["modes"]) for r_ in rows]),
                    ("operators computed", [set(r_["derived"]) for r_ in rows]), ("operators assigned (same 34)", [set(r_["hand"]) for r_ in rows])):
        acc, conf = nb(X, y, G); random.seed(1126); sh = []
        for _ in range(5000):
            yy = y[:]; random.shuffle(yy); sh.append(nb(X, yy, G)[0])
        p = sum(1 for a in sh if a >= acc) / len(sh); rec = {g: f"{conf[(g,g)]}/{y.count(g)}" for g in G}
        res[name] = dict(accuracy=round(acc, 3), commonest=round(max(collections.Counter(y).values()) / len(y), 3), shuffled_mean=round(sum(sh) / len(sh), 3), shuffled_95=round(sorted(sh)[int(.95 * len(sh))], 3), p=p, recall=rec)
        print(f"\n{name}: accuracy {acc:.3f} | commonest {res[name]['commonest']} | shuffled {res[name]['shuffled_mean']} (95th {res[name]['shuffled_95']}) | p={p:.4f} | recall {rec}")
    print("\nuse by Gospel:")
    allf = sorted({f for r_ in rows for f in r_["features"] + r_["derived"]})
    use = {f: {g: sum(1 for r_ in rows if r_["gospel"] == g and f in r_["features"] + r_["derived"]) for g in G} for f in allf}
    for f in allf: print(f"  {f:36}" + "  ".join(f"{g} {use[f][g]}/{y.count(g)}" for g in G))
    print("\nper locus:")
    for r_ in rows: print(f"  {r_['id']:34} computed {r_['derived']} | assigned {r_['hand']}")
    json.dump(dict(rows=rows, agreement=agree, naming=res, use=use, bad=bad), open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
