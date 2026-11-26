#!/usr/bin/env python3
"""The loci of the pair scan as relations, and the rule owed since 2O.2: OPPOSE, the opposite deed (action lemmas in a declared table of opposites).
   python3 pairs_rel.py <alexanarch root> <engine dir> out.json"""
import sys, json, io, contextlib
root, eng, outp = sys.argv[1:4]; sys.argv = [sys.argv[0], root, eng, outp]
import relations as R
r = R.r
ANT = {frozenset(x) for x in (("κλειω", "ανοιγω"), ("κλειω", "αποκυλιω"), ("δεω", "λυω"), ("αποκτεινω", "εγειρω"), ("καταβαινω", "αναβαινω"), ("κρυπτω", "αποκαλυπτω"), ("κλαιω", "χαιρω"), ("διδωμι", "αιρω"), ("βαλλω", "αιρω"))}
def derive2(s, t):
    F, O = R.DERIVE(s, t)
    if frozenset((s["act"][0], t["act"][0])) in ANT: O.add("OPPOSE"); O.discard("SUBSTITUTE")
    return F, O
P = [
("bound by Satan / Luke 13", "gnt:Rev 20:2", "gnt:Luke 13:16", r(("ANGEL",None),("δεω","εδησεν"),("ADVERSARY","σατανασ","σατανασ"),mode="VISION-EVENT"), r(("ADVERSARY","σατανασ"),("δεω","εδησεν"),("FAITHFUL","θυγατηρ","θυγατερα αβρααμ"),mode="QUESTION")),
("must be loosed / Luke 13", "gnt:Rev 20:3", "gnt:Luke 13:16", r(None,("λυω","δει λυθηναι"),("ADVERSARY","αυτοσ","αυτον"),mode="VISION-EVENT"), r(None,("λυω","εδει λυθηναι"),("FAITHFUL","αυτοσ","ταυτην"),mode="QUESTION")),
("into the abyss / Luke 8", "gnt:Rev 20:3", "gnt:Luke 8:31", r(("ANGEL",None),("βαλλω","εβαλεν"),("ADVERSARY","αυτοσ","αυτον"),[("THING","εισ την αβυσσον")],mode="VISION-EVENT"), r(("CHRIST",None),("επιτασσω","επιταξη"),("ADVERSARY","αυτοσ","αυτοισ"),[("THING","εισ την αβυσσον")],pol="-",mode="NARRATIVE-EVENT")),
("authority received / Luke 19", "gnt:Rev 17:12", "gnt:Luke 19:17", r(("ADVERSARY","βασιλεισ"),("λαμβανω","λαμβανουσιν"),(None,"εξουσια","εξουσιαν"),mode="VISION-EVENT"), r(("FAITHFUL","δουλε"),("εχω","εχων"),(None,"εξουσια","εξουσιαν"),mode="PARABLE")),
("seated / Mark 14", "gnt:Rev 14:14", "gnt:Mark 14:62", r(("CHRIST","υιον ανθρωπου"),("καθημαι","καθημενον"),(None,"νεφελη","επι την νεφελην"),mode="VISION-EVENT"), r(("CHRIST","υιον του ανθρωπου"),("καθημαι","καθημενον"),(None,"δεξια","εκ δεξιων"),mode="PROPHECY")),
("to buy / Luke 22", "gnt:Rev 13:17", "gnt:Luke 22:36", r(("ALL","τισ"),("αγοραζω","αγορασαι"),None,pol="-",mode="VISION-EVENT"), r(("FAITHFUL","ο μη εχων"),("αγοραζω","αγορασατω"),(None,"μαχαιρα","μαχαιραν"),mode="COMMAND")),
("what the angel does at the closure / Matthew 28", "gnt:Rev 20:3", "gnt:Matt 28:2", r(("ANGEL",None),("κλειω","εκλεισεν"),(None,"επανω αυτου","επανω αυτου"),mode="VISION-EVENT"), r(("ANGEL","αγγελοσ"),("αποκυλιω","απεκυλισεν"),(None,"επανω αυτου","επανω αυτου"),mode="NARRATIVE-EVENT")),
]
S = R.M.Seats(root); rows, bad = [], []
for name, sl, tl, s, t in P:
    st, tt = R.sq(S.get(sl)), R.sq(S.get(tl))
    for rel, txt, wh in ((s, st, "seed"), (t, tt, "target")):
        for f in R.forms(rel):
            if f not in txt: bad.append((name, wh, f))
        if rel["pol"] == "-" and not R.NEG.search(txt): bad.append((name, wh, "minus without a particle"))
    F, O = derive2(s, t); rows.append(dict(name=name, seed=sl, target=tl, features=sorted(F), operators=sorted(O))); print(f"{name:48} {sorted(F)} => {sorted(O)}")
print("forms not found:", bad or "none")
# OPPOSE over everything entered so far
n = sum(1 for prs in R.L.values() for s, t in prs if frozenset((s["act"][0], t["act"][0])) in ANT); tot = sum(len(v) for v in R.L.values())
sys.path.insert(0, "../rev1112")
with contextlib.redirect_stdout(io.StringIO()):
    import os; os.chdir("../rev1112"); sys.argv = [sys.argv[0], root, eng, "/tmp/_x.json"]; import rel1112
n2 = sum(1 for _, _, _, s, t in rel1112.P if frozenset((s["act"][0], t["act"][0])) in ANT)
print(f"OPPOSE fires: {n} of the {tot} pairs of 2J; {n2} of the {len(rel1112.P)} of 2M; {sum(1 for x in rows if 'OPPOSE' in x['operators'])} of these {len(rows)}")
os.chdir("../relations"); json.dump(dict(rows=rows, bad=bad, oppose=dict(two_j=n, two_m=n2)), open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
