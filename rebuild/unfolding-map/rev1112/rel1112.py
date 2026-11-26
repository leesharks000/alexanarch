#!/usr/bin/env python3
"""The shared members of Revelation 11-12 as relations (the form and rules of relations/relations.py, unchanged). Each pair: Revelation's clause and the
clause of the Gospel (or Acts) that holds the member. Forms are checked in the seat; the differences and operators are computed by DERIVE.
   python3 rel1112.py <alexanarch root> <engine dir> out.json"""
import sys, re, json, collections
root, eng, outp = sys.argv[1:4]; sys.path.insert(0, "../relations"); sys.argv = [sys.argv[0], root, eng, outp]
import relations as R
r, SIDE = R.r, R.SIDE
P = [
# the witnesses and the cross and tomb
("watchers / Mark", "gnt:Rev 11:12", "gnt:Mark 15:40", r(("ADVERSARY","εχθροι"),("θεωρεω","εθεωρησαν"),("FAITHFUL","αυτοσ","αυτουσ"),mode="VISION-EVENT"), r(("FAITHFUL","γυναικεσ"),("θεωρεω","θεωρουσαι"),mode="NARRATIVE-EVENT")),
("watchers / Matthew", "gnt:Rev 11:12", "gnt:Matt 27:55", r(("ADVERSARY","εχθροι"),("θεωρεω","εθεωρησαν"),("FAITHFUL","αυτοσ","αυτουσ"),mode="VISION-EVENT"), r(("FAITHFUL","γυναικεσ"),("θεωρεω","θεωρουσαι"),mode="NARRATIVE-EVENT")),
("watchers / Luke", "gnt:Rev 11:12", "gnt:Luke 23:35", r(("ADVERSARY","εχθροι"),("θεωρεω","εθεωρησαν"),("FAITHFUL","αυτοσ","αυτουσ"),mode="VISION-EVENT"), r(("ALL","λαοσ"),("θεωρεω","θεωρων"),mode="NARRATIVE-EVENT")),
("watchers / John", "gnt:Rev 11:12", "gnt:John 20:6", r(("ADVERSARY","εχθροι"),("θεωρεω","εθεωρησαν"),("FAITHFUL","αυτοσ","αυτουσ"),mode="VISION-EVENT"), r(("FAITHFUL","πετροσ"),("θεωρεω","θεωρει"),(None,"οθονιον","οθονια"),mode="NARRATIVE-EVENT")),
("great fear / Matthew", "gnt:Rev 11:11", "gnt:Matt 27:54", r(("ALL","θεωρουντασ"),("φοβοσ","φοβοσ μεγασ"),mode="VISION-EVENT"), r(("GUARD","εκατονταρχοσ"),("φοβοσ","εφοβηθησαν σφοδρα"),mode="NARRATIVE-EVENT")),
("great voice / Mark", "gnt:Rev 11:12", "gnt:Mark 15:34", r(("THING","εκ του ουρανου"),("λεγω","λεγουσησ"),(None,"φωνη μεγαλη","φωνησ μεγαλησ"),[("FAITHFUL","αυτοισ")],mode="VISION-EVENT"), r(("CHRIST","ιησουσ"),("βοαω","εβοησεν"),(None,"φωνη μεγαλη","φωνη μεγαλη"),[("GOD","ο θεοσ μου")],mode="NARRATIVE-EVENT")),
("great voice / Luke", "gnt:Rev 11:12", "gnt:Luke 23:46", r(("THING","εκ του ουρανου"),("λεγω","λεγουσησ"),(None,"φωνη μεγαλη","φωνησ μεγαλησ"),[("FAITHFUL","αυτοισ")],mode="VISION-EVENT"), r(("CHRIST","ιησουσ"),("λεγω","ειπεν"),(None,"φωνη μεγαλη","φωνη μεγαλη"),[("GOD","πατερ")],mode="NARRATIVE-EVENT")),
("the tomb / Mark", "gnt:Rev 11:9", "gnt:Mark 15:45-46", r(("ALL","ουκ αφιουσιν"),("τιθημι","τεθηναι"),("FAITHFUL","πτωμα","πτωματα αυτων"),[("THING","εισ μνημα")],pol="-",mode="VISION-EVENT"), r(("FAITHFUL","ιωσηφ"),("τιθημι","κατεθηκεν"),("CHRIST","πτωμα","πτωμα"),[("THING","εν μνηματι")],mode="NARRATIVE-EVENT")),
("the tomb / Luke", "gnt:Rev 11:9", "gnt:Luke 23:52-53", r(("ALL","ουκ αφιουσιν"),("τιθημι","τεθηναι"),("FAITHFUL","πτωμα","πτωματα αυτων"),[("THING","εισ μνημα")],pol="-",mode="VISION-EVENT"), r(("FAITHFUL",None),("τιθημι","εθηκεν"),("CHRIST","σωμα","σωμα του ιησου"),[("THING","εν μνηματι")],mode="NARRATIVE-EVENT")),
("after three days / Matthew", "gnt:Rev 11:11", "gnt:Matt 27:63", r(("FAITHFUL",None),("ιστημι","εστησαν"),(None,"μετα τρεισ ημερασ","μετα τασ τρεισ ημερασ"),mode="VISION-EVENT"), r(("CHRIST",None),("εγειρω","εγειρομαι"),(None,"μετα τρεισ ημερασ","μετα τρεισ ημερασ"),mode="PROPHECY")),
("three days / Mark", "gnt:Rev 11:11", "gnt:Mark 15:29", r(("FAITHFUL",None),("ιστημι","εστησαν"),(None,"τρεισ ημεραι","τρεισ ημερασ"),mode="VISION-EVENT"), r(("CHRIST","οικοδομων"),("οικοδομεω","οικοδομων"),(None,"τρεισ ημεραι","τρισιν ημεραισ"),mode="STATEMENT")),
("the earthquake / Matthew", "gnt:Rev 11:13", "gnt:Matt 28:2", r(("THING","σεισμοσ μεγασ"),("γινομαι","εγενετο"),mode="VISION-EVENT"), r(("THING","σεισμοσ"),("γινομαι","εγενετο"),mode="NARRATIVE-EVENT")),
("the holy city / Matthew", "gnt:Rev 11:2", "gnt:Matt 27:53", r(("ADVERSARY","εθνεσιν"),("πατεω","πατησουσιν"),(None,"αγια πολισ","πολιν την αγιαν"),mode="PROPHECY"), r(("FAITHFUL",None),("εισερχομαι","εισηλθον"),(None,"αγια πολισ","αγιαν πολιν"),mode="NARRATIVE-EVENT")),
("the glory / Luke", "gnt:Rev 11:13", "gnt:Luke 23:47", r(("ALL","οι λοιποι"),("διδωμι δοξαν","εδωκαν δοξαν"),None,[("GOD","τω θεω")],mode="VISION-EVENT"), r(("GUARD","εκατονταρχησ"),("δοξαζω","εδοξαζεν"),None,[("GOD","τον θεον")],mode="NARRATIVE-EVENT")),
("afraid / Luke", "gnt:Rev 11:13", "gnt:Luke 24:5", r(("ALL","οι λοιποι"),("εμφοβοσ","εμφοβοι εγενοντο"),mode="VISION-EVENT"), r(("FAITHFUL",None),("εμφοβοσ","εμφοβων δε γενομενων"),mode="NARRATIVE-EVENT")),
("the reed / Mark", "gnt:Rev 11:1", "gnt:Mark 15:36", r(None,("διδωμι","εδοθη"),(None,"καλαμοσ","καλαμοσ"),[("SEER","μοι")],mode="VISION-EVENT"), r(("ALL","τισ"),("ποτιζω","εποτιζεν"),(None,"καλαμοσ","καλαμω"),[("CHRIST","αυτον")],mode="NARRATIVE-EVENT")),
("where crucified / John", "gnt:Rev 11:8", "gnt:John 19:20", r(None,("σταυροω","εσταυρωθη"),("CHRIST","κυριοσ","κυριοσ αυτων"),mode="VISION-EVENT"), r(None,("σταυροω","εσταυρωθη"),("CHRIST","κυριοσ","ιησουσ"),mode="NARRATIVE-EVENT")),
("into heaven in the cloud / Acts", "gnt:Rev 11:12", "gnt:Acts 1:9", r(("FAITHFUL",None),("αναβαινω","ανεβησαν"),(None,"νεφελη","εν τη νεφελη"),mode="VISION-EVENT"), r(("CHRIST",None),("επαιρω","επηρθη"),(None,"νεφελη","νεφελη"),mode="NARRATIVE-EVENT")),
("the earth rejoices / John", "gnt:Rev 11:10", "gnt:John 16:20", r(("ADVERSARY","κατοικουντεσ επι τησ γησ"),("χαιρω","χαιρουσιν"),("FAITHFUL","αυτοσ","επ αυτοισ"),mode="VISION-EVENT"), r(("ADVERSARY","κοσμοσ"),("χαιρω","χαρησεται"),mode="PROPHECY")),
# the joint
("the kingdom of the world / Matthew", "gnt:Rev 11:15", "gnt:Matt 4:8", r(None,("γινομαι","εγενετο"),(None,"βασιλεια του κοσμου","βασιλεια του κοσμου"),[("GOD","του κυριου ημων")],mode="VISION-EVENT"), r(("ADVERSARY","διαβολοσ"),("δεικνυμι","δεικνυσιν"),(None,"βασιλεια του κοσμου","βασιλειασ του κοσμου"),[("CHRIST","αυτω")],mode="NARRATIVE-EVENT")),
("the trumpet / Matthew", "gnt:Rev 11:15", "gnt:Matt 24:31", r(("ANGEL","αγγελοσ"),("σαλπιζω","εσαλπισεν"),mode="VISION-EVENT"), r(("ANGEL","αγγελουσ"),("σαλπιζω","σαλπιγγοσ"),mode="PROPHECY")),
("great power / Matthew", "gnt:Rev 11:17", "gnt:Matt 24:30", r(("GOD","κυριε ο θεοσ"),("λαμβανω","ειληφασ"),(None,"δυναμισ","δυναμιν"),mode="STATEMENT"), r(("CHRIST","υιον του ανθρωπου"),("ερχομαι","ερχομενον"),(None,"δυναμισ","δυναμεωσ"),mode="PROPHECY")),
# the sign
("the sign in heaven / Matthew", "gnt:Rev 12:1", "gnt:Matt 24:30", r(("THING","σημειον"),("οραω","ωφθη"),(None,"ουρανοσ","εν τω ουρανω"),mode="VISION-EVENT"), r(("THING","σημειον"),("φαινω","φανησεται"),(None,"ουρανοσ","εν ουρανω"),mode="PROPHECY")),
("with child / Matthew 24", "gnt:Rev 12:2", "gnt:Matt 24:19", r(("FIGURE",None),("εν γαστρι εχω","εν γαστρι εχουσα"),mode="VISION-EVENT"), r(("ALL",None),("εν γαστρι εχω","εν γαστρι εχουσαισ"),mode="THREAT")),
("with child / Matthew 1", "gnt:Rev 12:2", "gnt:Matt 1:18", r(("FIGURE",None),("εν γαστρι εχω","εν γαστρι εχουσα"),mode="VISION-EVENT"), r(("FAITHFUL","μαριασ"),("εν γαστρι εχω","εν γαστρι εχουσα"),mode="NARRATIVE-EVENT")),
("she bore a son / Matthew", "gnt:Rev 12:5", "gnt:Matt 1:25", r(("FIGURE",None),("τικτω","ετεκεν"),(None,"υιοσ","υιον"),mode="VISION-EVENT"), r(("FAITHFUL",None),("τικτω","ετεκεν"),(None,"υιοσ","υιον"),mode="NARRATIVE-EVENT")),
("to shepherd / Matthew", "gnt:Rev 12:5", "gnt:Matt 2:6", r(("CHRIST","υιον"),("ποιμαινω","ποιμαινειν"),("ALL","εθνοσ","παντα τα εθνη"),mode="VISION-EVENT"), r(("CHRIST","ηγουμενοσ"),("ποιμαινω","ποιμανει"),("FAITHFUL","λαοσ","τον λαον μου"),mode="CITATION")),
("the flight / Matthew 2", "gnt:Rev 12:6", "gnt:Matt 2:13", r(("FIGURE","γυνη"),("φευγω","εφυγεν"),(None,"ερημοσ","εισ την ερημον"),mode="VISION-EVENT"), r(("FAITHFUL","ιωσηφ"),("φευγω","φευγε"),(None,"αιγυπτοσ","εισ αιγυπτον"),mode="COMMAND")),
("the flight / Matthew 24", "gnt:Rev 12:6", "gnt:Matt 24:16", r(("FIGURE","γυνη"),("φευγω","εφυγεν"),(None,"ερημοσ","εισ την ερημον"),mode="VISION-EVENT"), r(("FAITHFUL","οι εν τη ιουδαια"),("φευγω","φευγετωσαν"),(None,"οροσ","εισ τα ορη"),mode="COMMAND")),
("the stars / Matthew", "gnt:Rev 12:4", "gnt:Matt 24:29", r(("ADVERSARY","ουρα αυτου"),("βαλλω","εβαλεν"),(None,"αστηρ","αστερων"),mode="VISION-EVENT"), r(None,("πιπτω","πεσουνται"),(None,"αστηρ","αστερεσ"),mode="PROPHECY")),
("a woman when she bears / John", "gnt:Rev 12:4", "gnt:John 16:21", r(("FIGURE","γυναικοσ"),("τικτω","τεκη"),(None,"τεκνον","τεκνον"),mode="VISION-EVENT"), r(("FIGURE","γυνη"),("τικτω","τικτη"),(None,"παιδιον","παιδιον"),mode="PARABLE")),
("a place prepared / John", "gnt:Rev 12:6", "gnt:John 14:2", r(("GOD","απο του θεου"),("ετοιμαζω","ητοιμασμενον"),(None,"τοποσ","τοπον"),[("FIGURE","γυνη")],mode="VISION-EVENT"), r(("CHRIST","πορευομαι"),("ετοιμαζω","ετοιμασαι"),(None,"τοποσ","τοπον"),[("FAITHFUL","υμιν")],mode="PROMISE")),
("cast down / John", "gnt:Rev 12:9", "gnt:John 12:31", r(None,("βαλλω","εβληθη"),("ADVERSARY","δρακων","δρακων"),mode="VISION-EVENT"), r(None,("εκβαλλω","εκβληθησεται"),("ADVERSARY","αρχων","αρχων του κοσμου τουτου"),mode="PROPHECY")),
("cast down / Luke", "gnt:Rev 12:9", "gnt:Luke 10:18", r(None,("βαλλω","εβληθη"),("ADVERSARY","σατανασ","σατανασ"),mode="VISION-EVENT"), r(None,("πιπτω","πεσοντα"),("ADVERSARY","σατανασ","σαταναν"),mode="STATEMENT")),
("not loving the life / John", "gnt:Rev 12:11", "gnt:John 12:25", r(("FAITHFUL","αυτοι"),("αγαπαω","ηγαπησαν"),(None,"ψυχη","την ψυχην αυτων"),pol="-",mode="STATEMENT"), r(("ALL","ο μισων"),("μισεω","μισων"),(None,"ψυχη","την ψυχην αυτου"),mode="STATEMENT")),
("keeping the commandments / John", "gnt:Rev 12:17", "gnt:John 15:10", r(("FAITHFUL","τηρουντων"),("τηρεω","τηρουντων"),("GOD","εντολη","εντολασ του θεου"),mode="VISION-EVENT"), r(("FAITHFUL",None),("τηρεω","τηρησητε"),("CHRIST","εντολη","εντολασ μου"),mode="CONDITION")),
("snatched up / 1 Thessalonians", "gnt:Rev 12:5", "gnt:1Thess 4:17", r(None,("αρπαζω","ηρπασθη"),("CHRIST","τεκνον","τεκνον αυτησ"),[("GOD","προσ τον θεον")],mode="VISION-EVENT"), r(None,("αρπαζω","αρπαγησομεθα"),("FAITHFUL","ημεισ","ημεισ οι ζωντεσ"),[("CHRIST","του κυριου")],mode="PROPHECY")),
]
S = R.M.Seats(root); rows, bad = [], []
for name, sl, tl, s, t in P:
    st, tt = R.sq(S.get(sl)), R.sq(S.get(tl))
    for rel, txt, wh in ((s, st, "seed"), (t, tt, "target")):
        for f in R.forms(rel):
            if f not in txt: bad.append((name, wh, f))
        if rel["pol"] == "-" and not R.NEG.search(txt): bad.append((name, wh, "minus without a particle"))
    F, O = R.DERIVE(s, t); rows.append(dict(name=name, seed=sl, target=tl, features=sorted(F), operators=sorted(O)))
print("pairs:", len(rows), "| forms not found in the seat:", bad or "none")
for x in rows: print(f"  {x['name']:36} {x['seed'][4:]:11} → {x['target'][4:]:16} {x['features']}  ⇒ {x['operators']}")
cf, co = collections.Counter(f for x in rows for f in x["features"]), collections.Counter(o for x in rows for o in x["operators"])
print("\nfeatures:", dict(cf)); print("operators:", dict(co))
B = json.load(open("../relations/relations.json", encoding="utf-8"))["rows"]
bf = collections.Counter(f for x in B for f in x["features"])
print("\nshare of pairs/loci showing each difference: here (n=%d) | the 34 loci of 2J" % len(rows))
for f in sorted(set(cf) | set(bf)): print(f"  {f:36} {cf[f]/len(rows):.2f} | {bf[f]/len(B):.2f}")
json.dump(dict(rows=rows, features=cf, operators=co, bad=bad), open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
