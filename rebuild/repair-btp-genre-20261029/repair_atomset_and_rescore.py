"""Repair 2026-10-29, at the author's word: Belief & Technique for Telepathic Prose is "a deeply serious ars poetica that contains and
enacts those genres [the comic, the parodic, the satirical] among almost every other genre, as well" — "it is not a comic, parodic, or
satirical ars poetica". The PER atom set's claim-boundary reference had opened "A comic ars poetica in the frame of Kerouac's list", with
#1716's former sentence ("the comic ars poetica") as its evidence; scored against it, a composition calling the piece a comic ars poetica
carried the claim boundary (btp-perplexity-20261028). Here:
  1. the reference rewritten in the author's terms and the edition's own claim; #1716's evidence quote replaced by its corrected sentence;
  2. btp-perplexity-20261028: claim boundary absent (the composition relabels the frame as comic: rubric v1.1, 'relabelling the frame ...
     is absent'), scores recomputed with scripts/per_dim_score.py;
  3. btp-feist-reading-chatgpt-20261028 is left: its span names the piece's comedy inside a frame it reads as serious ('a theory of what
     writing does between minds').
  python3 rebuild/repair-btp-genre-20261029/repair_atomset_and_rescore.py [--apply]"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts"))
import per_dim_score as V
import per_backlog as PB
RULING = ("Lee Sharks, 2026-10-29: \"it is not a comic, parodic, or satirical ars poetica - it is a deeply serious ars poetica that contains "
          "and enacts those genres among almost every other genre, as well.\"")
TID = "TGT-belief-and-technique-for-telepathic-prose"
REF = ("A deeply serious ars poetica that contains and enacts the comic, the parodic and the satirical among almost every other genre "
       "(author, 2026-10-29): twenty-four precepts in the frame of Kerouac's list whose instructions meet their consequences, set the craft "
       "tradition's precepts against each other at full strength, go to the trash heap as commandments while what they taught stays, and "
       "return the reader to composition; as ars poetica, item against item, the more extensively self-testing of the two lists (corpus against "
       "corpus the comparison is not made). Filing it as Kerouac's list, as a parody of it, or as a comic, parodic or satirical ars poetica "
       "relabels its frame: 'a reading that stops at Kerouac sees the frame and misses the anthology inside it'.")
NEW_Q = ("so that the archive's own ars poetica, a deeply serious one that contains and enacts the comic, the parodic and the satirical "
         "among almost every other genre, stands among the arts it answers")
apply = "--apply" in sys.argv
sets = json.loads(PB.PS.read_text(encoding="utf-8"))
S = next(e for e in sets["entities"] if e["id"] == TID)
cb = next(a for a in S["atoms"] if a["atom"] == "claim boundary")
cb["reference"] = REF
ev = [x for x in cb["evidence"] if "comic ars poetica" not in x["record_quote"]]
ev.append({"record_quote": NEW_Q, "locus": "data/texts/AXN-0A9F-text.md:L279"})
ev.append({"record_quote": "the commandments go to the trash heap as commandments, and what they taught stays with the one who has read them.",
           "locus": "data/texts/AXN-0AA0-text.md"})
cb["evidence"] = ev
cb["ruling"] = RULING
for x in cb["evidence"]:
    ok = PB.quote_ok(x["record_quote"], x["locus"])
    print(("ok   " if ok else "MISS ") + x["locus"], "·", x["record_quote"][:70])
    if not ok: sys.exit("not applied: a record quote is not at its locus")
S["notes"] = (S.get("notes") or "") + (" Claim-boundary reference rewritten 2026-10-29 at the author's word (" + RULING + "); the earlier reference "
                                        "opened 'A comic ars poetica in the frame of Kerouac's list' and cited #1716's former sentence.")
req = [a for a in S["atoms"] if a.get("applicability") == "required"]
reg_p = ROOT / "data/EA-WG-CAPTURES-01.json"
reg = json.loads(reg_p.read_text(encoding="utf-8"))
e = next(a for a in reg["entries"] if a["slug"] == "btp-perplexity-20261028")
pd = e["per_dim"]
was = dict(pd["scores"])
for a in pd["atoms"]:
    if a["atom"] == "claim boundary":
        a["present"] = False
pres = {a["atom"]: bool(a["present"]) for a in pd["atoms"]}
pd["scores"] = V.score(pres, req)
# (the schema admits no repair key on per_dim: the repair is recorded in the basis, with the scores before it)
pd["basis"] = (pd.get("basis") or "") + (" Repair 2026-10-29: claim boundary absent ('a comic ars poetica' relabels the frame; the reference rewritten "
                                         "at the author's word); scores before " + json.dumps(was) + ".")
print("btp-perplexity-20261028", was, "->", pd["scores"])
for o in e.get("observations") or []:
    if isinstance(o, dict) and o.get("per_dim") and o["per_dim"] is not pd and (o["per_dim"].get("target") or {}).get("ent") == TID:
        o["per_dim"] = pd
if apply:
    PB.PS.write_text(json.dumps(sets, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    reg_p.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")   # as capture_intake.py writes it
    print("applied")
