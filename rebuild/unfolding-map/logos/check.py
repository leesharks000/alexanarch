#!/usr/bin/env python3
"""By logos (the author, 16:11): keys taken from the strongest transforms, what each predicts of a broader stretch of Matthew, and the seat read for it.
This script only fetches the verses and counts where a wording stands across the New Testament and the Septuagint; the reading is in the file.
   python3 check.py <alexanarch root> <engine dir> out.json"""
import sys, re, json, pathlib, collections
sys.path.insert(0, sys.argv[2]); import midrash as E
root = pathlib.Path(sys.argv[1]) / "data/corpora"
def sq(s): return re.sub(r"\s+", " ", E.norm(s)).strip()
def load(corpus):
    out = []
    for p in sorted((root / corpus / "text").glob("*.txt")):
        seen = set()
        for l in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            if "\t" in l:
                r, t = l.split("\t", 1); r = r.strip()
                if re.search(r"\d+:\d+$", r) and r not in seen: seen.add(r); out.append((r, sq(t)))
    return out
NT, LXX = load("gnt-nestle1904"), load("lxx-swete"); D = dict(NT); OUT = dict(verses={}, counts={})
V = ["Rev 17:3", "Rev 21:10", "Rev 21:11", "Rev 19:10", "Rev 22:8", "Rev 22:9", "Rev 11:15", "Matt 4:1", "Matt 4:3", "Matt 4:5", "Matt 4:8", "Matt 4:9", "Matt 4:10", "Luke 4:1", "Luke 4:5", "Luke 4:7", "Luke 4:8", "Luke 4:9",
     "Rev 1:16", "Rev 1:17", "Rev 10:1", "Matt 17:1", "Matt 17:2", "Matt 17:6", "Matt 17:7", "Mark 9:2", "Mark 9:3", "Mark 9:6", "Luke 9:29",
     "Rev 17:4", "Rev 17:16", "Rev 11:1", "Rev 2:27", "Matt 27:28", "Matt 27:29", "Matt 27:30", "Mark 15:17", "Mark 15:19",
     "Rev 20:7", "Rev 2:10", "Matt 27:15", "Matt 27:16", "Matt 27:26", "Mark 15:7", "Luke 23:19", "Luke 23:25",
     "Rev 19:14", "Rev 19:19", "Rev 19:8", "Rev 18:8", "Rev 16:15", "Rev 3:18", "Matt 22:7", "Matt 22:11", "Matt 22:12", "Matt 22:13", "Luke 14:21",
     "Rev 10:9", "Rev 10:10", "Matt 26:26", "Mark 14:22", "Rev 5:4", "Matt 26:75", "Rev 13:3", "Rev 13:14", "Rev 4:1", "Rev 19:11", "Matt 3:16", "Mark 1:10"]
for r in V: OUT["verses"][r] = D[r]; print(r, ":", D[r][:400])
C = [("the holy city", r"αγιαν πολιν|πολιν την αγιαν|πολει τη αγια|πολεωσ τησ αγιασ"), ("a high mountain", r"οροσ (μεγα και )?υψηλον"), ("into the wilderness … spirit", r"εισ (την )?ερημον.{0,40}πνευμα|πνευμα.{0,60}εισ (την )?ερημον"),
     ("fall and worship", r"πεσ\w+ (\w+ ){0,5}προσκυν"), ("worship God / the Lord your God", r"τω θεω προσκυνησον|κυριον τον θεον σου προσκυνησεισ"), ("shows / showed (δείκνυμι) with mountain or city", r"(εδειξεν|δεικνυσιν).{0,60}(πολιν|βασιλει)"),
     ("face as the sun", r"(προσωπον|οψισ) αυτου ωσ ο ηλιοσ"), ("fell on the face(s) … feared", r"επεσ\w+ επι (τα )?προσωπ\w+"), ("touched … fear not", r"(ηψατο|αψαμενοσ|εθηκεν την δεξιαν).{0,60}μη φοβ"),
     ("scarlet (κόκκινος)", r"κοκκιν"), ("a reed with the right hand", r"καλαμ\w+.{0,30}δεξια"), ("a reed like a rod / rod", r"καλαμοσ ομοιοσ ραβδω"), ("stripped / naked", r"εκδυσαντεσ|γυμνην"),
     ("a prisoner (δέσμιος)", r"δεσμιο"), ("prison, in the passion and Rev 20", r"φυλακη"), ("armies (στράτευμα)", r"στρατευμα"), ("burned the city", r"ενεπρησεν|κατακαυθησεται"), ("bound feet and hands", r"δησαντεσ αυτου ποδασ και χειρασ|δεδεμενοσ τουσ ποδασ και τασ χειρασ"),
     ("garment of the wedding / keeps his garments", r"ενδυμα γαμου|τηρων τα ιματια"), ("take and eat", r"λαβ\w+ (και )?(κατα)?φαγ"), ("wept much / bitterly", r"εκλαιον πολυ|εκλαυσεν πικρωσ"), ("heaven(s) opened", r"ηνεω\w+ οι ουρανοι|ουρανον ηνεωγμενον|ηνοιχθησαν οι ουρανοι|θυρα ηνεωγμενη εν τω ουρανω")]
print()
for lab, rx in C:
    c = re.compile(rx); nt = [r for r, t in NT if c.search(t)]; lx = [r for r, t in LXX if c.search(t)]; OUT["counts"][lab] = dict(nt=nt, lxx=len(lx), lxx_refs=lx[:5]); print(f"{lab}: NT {nt[:16]} | LXX {len(lx)} {lx[:4]}")
for ref in ("Δευτερονόμιον 6:13", "Δευτερονόμιον 8:3", "Ἰεζεκιήλ 1:1", "Ἰεζεκιήλ 40:2", "Ἰεζεκιήλ 3:1"):
    t = dict(LXX).get(ref); print(ref, ":", (t or "")[:260]); OUT["verses"][ref] = t
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
