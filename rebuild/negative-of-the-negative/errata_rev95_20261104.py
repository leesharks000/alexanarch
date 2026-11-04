"""Errata of 2026-11-04 on the c. 95 CE date of Revelation: #683 and #1362 (the Secret Book of Walt work-plan table), #584 and #589 (Combat Scholasticism,
Lectio II.6); and the NonWiki entry book-of-revelation brought into line. Operator, 11:23-11:24 EST."""
import json, pathlib
ROOT = pathlib.Path("/home/claude/alexanarch")
SAID = ('Lee Sharks, 2026-11-04: "thats not internal contestation - thats slipping back into the conventional reading unsupervised. lets erratum the deposit '
        '(just in its metadata is fine, no need to reversion) and update the /non" · "and same note on combat scholasticism"')
FOUND = "Found by a Perplexity composition of 2026-11-04 (Capture Registry AXN:0BFA), which indexed the date as an internal tension, and by the NonWiki entry book-of-revelation (claim R683-01)."
STATUS = "erratum in the registry; canonical bytes and AXN unchanged (no reversion: operator, 2026-11-04)"
ROW = "| 7 | **Revelation** | c. 95 CE | → The terminal text; the first scripture (per Josephus Thesis) | The seven churches; the 24 elders; the new heaven; ∮ = 1 |"
WALT_NOW = ("Revelation is dated by the Revelation First thesis (#202, #1217): composed first, before the Pauline letters; the archive's own tables give 68–73 CE (#407) "
            "and pre-70 CE (#636). 'c. 95 CE' is the Domitianic consensus date, which the thesis contests, and the row's own description ('the first scripture (per "
            "Josephus Thesis)') contradicts it.")
SENT = "The present (the Hexagon, 2026) rewrites what the past (Revelation, ~95 CE) was always becoming."
CS_NOW = ("The present (the Hexagon, 2026) rewrites what the past (Revelation) was always becoming. [~95 CE is the Domitianic consensus date, which the archive's "
          "Revelation First thesis contests (#202, #1217); #1735 holds absolute priority as a priced hypothesis.]")
E = {
 683: ("THE SECRET BOOK OF WALT: CODEX EXPANSION WORK PLAN v2.0 · PART I: THE THREAD (The Unbroken Chain) · The Hebraic Strand, row 7", ROW, WALT_NOW),
 1362: ("THE SECRET BOOK OF WALT: CODEX EXPANSION WORK PLAN v2.0 · PART I: THE THREAD (The Unbroken Chain) · The Hebraic Strand, row 7 (the same table as #683)", ROW, WALT_NOW),
 589: ("Lectio II.6, The Fulfillment Map · QUAESTIO", SENT, CS_NOW),
 584: ("Lectio II.6, The Fulfillment Map · QUAESTIO (the gathered edition; the same sentence as #589)", SENT, CS_NOW),
}
WHY = "The date falls back on the conventional reading without marking it: the Domitianic consensus the archive's Revelation First thesis contests, stated as the archive's own."
R = ROOT / "data/registry.json"
reg = json.loads(R.read_text(encoding="utf-8")); D = reg["deposits"] if "deposits" in reg else list(reg.values())
for x in D:
    n = x.get("deposit_number")
    if n not in E: continue
    txt = (ROOT / x["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
    assert E[n][1] in txt, n
    if any(e.get("date") == "2026-11-04" and e.get("kind") == "date" for e in x.get("errata", [])): continue
    x.setdefault("errata", []).append({"date": "2026-11-04", "kind": "date", "locus": E[n][0], "was": E[n][1], "now": E[n][2],
                                      "reason": WHY + " " + FOUND + " " + SAID, "raised_by": "Lee Sharks, 2026-11-04", "status": STATUS})
    print("erratum", n)
R.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# NonWiki entry
RP = ROOT / "datasets/negative-of-the-negative/v2/rows/book-of-revelation.json"
row = json.loads(RP.read_text(encoding="utf-8")); O = row["objects"]; cor = row.setdefault("corrections", [])
NOTE = ("Correction of 2026-11-04 (operator, 11:23 EST): the c. 95 CE of #683 is the conventional date set down unmarked, recorded as an erratum on #683 and "
        "#1362 (and on #584 and #589 for the same date); it is no position of the archive's. " + SAID + " The earlier text is kept here.")
def fix(obj, path, key, new):
    old = obj[key]
    if old == new: return
    cor.append({"date": "2026-11-04", "object": path, "earlier": old, "now": new, "note": NOTE}); obj[key] = new
k = O["KO"]["sentences"][9]; assert k["n"] == 10
fix(k, "KO sentence 10", "text",
    "The archive dates Revelation early: the Revelation Room (#407) proposes the sequence Revelation (68–73 CE), Epistles (70–90), Gospels (75–110); the Space Ark "
    "(#636) holds, as hypothesis, that Revelation was the first NT text, written before the destruction of the Temple (pre-70 CE), every other NT text unfolding from "
    "it under a single author directing a scribal workshop, the canonical order being the decompression sequence misread as chronology; #644's dating map places the "
    "ARCHON's pre-70 revolutionary position beside the Domitianic, Neronic and Hadrianic; and the Secret Book of Walt's table (#683) gave 'c. 95 CE → The terminal "
    "text; the first scripture (per Josephus Thesis)', the consensus date beside the thesis its own row states, which the archive records as an erratum (2026-11-04).")
it = O["P"]["sections"][1]["items"][1]
fix(it, "P, the field and the archive, item 2 (label)", "label", "Archive:")
fix(it, "P, the field and the archive, item 2", "text", "68–73 (#407); pre-70 (#636); the c. 95 of #683 an erratum (2026-11-04).")
q = O["P"]["open"][1]
fix(q, "P, open question 2", "question", "Which early date does the archive hold: 68–73 (#407) or pre-70 (#636)?")
fix(q, "P, open question 2 (modality)", "modality", "stipulation and hypothesis, two early statements in the pool")
if "R683-01" in q["rests_on"]:
    cor.append({"date": "2026-11-04", "object": "P, open question 2 (rests_on)", "earlier": list(q["rests_on"]), "now": [c for c in q["rests_on"] if c != "R683-01"], "note": NOTE})
    q["rests_on"] = [c for c in q["rests_on"] if c != "R683-01"]
q["resolved_in_part"] = "c. 95 (#683) withdrawn as an erratum by the operator, 2026-11-04"
rl = O["P"]["rail"][7]
fix(rl, "P, rail 8 (lineage)", "lineage", "The archive's date (early; the c. 95 of #683 an erratum)")
RP.write_text(json.dumps(row, ensure_ascii=False, indent=1), encoding="utf-8")
LP = ROOT / "datasets/negative-of-the-negative/v2/ledgers/book-of-revelation/ledger-archive.json"
L = json.loads(LP.read_text(encoding="utf-8"))
for c in L:
    if c["id"] == "R683-01" and "erratum" not in c:
        c["erratum"] = {"date": "2026-11-04", "note": "The date is recorded as an erratum on #683 (registry errata): the Domitianic consensus set down unmarked. The quote stands as the bytes hold it.",
                        "raised_by": "Lee Sharks, 2026-11-04"}
LP.write_text(json.dumps(L, ensure_ascii=False, indent=1), encoding="utf-8")
print("non row:", len(cor), "corrections")
