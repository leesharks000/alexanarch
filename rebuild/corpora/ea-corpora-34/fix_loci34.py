#!/usr/bin/env python3
"""Rewrite each Greek locus of the EA-CORPORA-34 specs into the code points of the seated text. The First1KGreek TEI is not in NFC
(it carries the oxia forms, U+1F71 and kin, where NFC has the tonos forms); the loci were written in NFC. Each find string is matched
against the seated text character by character under NFC equivalence and replaced by the text's own characters; the NFC form is kept
in the locus note. The texts themselves are not changed.   python3 fix_loci34.py   (after the first build)"""
import json, pathlib, re, unicodedata as U
H = pathlib.Path(__file__).resolve().parent; A = H.parents[2] / "data/corpora"
for sp in sorted(H.glob("spec34-*.json")):
    s = json.loads(sp.read_text(encoding="utf-8")); ch = False
    for lo in s.get("loci", []):
        t = " ".join((A / s["corpus"] / lo["text"]).read_text(encoding="utf-8").split())
        if " ".join(lo["find"].split()) in t: continue
        cls = {}
        for c in set(t): cls.setdefault(U.normalize("NFC", c), set()).add(c)
        pat = "".join("(?:" + "|".join(sorted(map(re.escape, cls.get(U.normalize("NFC", c), set()) | {c}))) + ")" for c in U.normalize("NFC", lo["find"]))
        m = re.search(pat, t)
        if m:
            nfc = lo["find"]; lo["find"] = m.group(0); ch = True
            lo["note"] = ((lo.get("note") + "; ") if lo.get("note") else "") + f"written in NFC as '{nfc}'; the seated TEI carries the oxia forms, so the locus is given in the text's own code points"
            print("fixed", s["corpus"], lo["label"][:50])
        else:
            print("STILL MISSING", s["corpus"], lo["label"][:60])
    if ch: sp.write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
