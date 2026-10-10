#!/usr/bin/env python3
"""Author the capture 'anne carson alexanarch', Google AI Overview, signed out, incognito, 2026-10-09.
Source: the operator's attachment of 2026-10-09 21:46 EDT ("its already the canonical shear on the very site that contests it.
incognito, signed out"). NEW address; nearest seated 'anne carson in alexanarch' (AIO, 2026-10-08 14:10)."""
import json, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
raw = (HERE / "paste-20261009-2146.txt").read_text(encoding="utf-8")
Q = "anne carson alexanarch"
L = raw.split("\n")
assert L[3].strip() == Q
i0 = L.index("AI Overview"); i1 = [i for i, l in enumerate(L) if l.startswith("AI responses may include mistakes")][0]
body = "\n".join(L[i0 + 1:i1]).strip()
MOT = "\"for her bold and inventive oeuvre that, in playful dialogue with the classical tradition, has created new forms for contemporary literature\""
for s in ["Anne Carson is featured on Alexanarch in connection with her book If Not, Winter, where her translation of Sappho's poetic fragments is analyzed through the lens of architectural gaps, brackets, and white space.",
          "2026 Nobel Prize in Literature: Awarded to Canadian poet, essayist, and classicist Anne Carson " + MOT,
          "which examines how Anne Carson's If Not, Winter preserves Sappho's missing text with visible brackets and lacunae.",
          "Would you like to know more about Anne Carson's classical translations or her 2026 Nobel Prize reception?"]:
    assert s in body, s
# chips in the composition: an image-card title glued to the first sentence, two alexanarch chips, CBC +2
assert body.startswith("Anne Carson's Seductive Strangeness - The Atlantic"), body[:60]
assert body.count("www.alexanarch.org") == 2 and "\nCBC\n +2\n" in "\n" + body + "\n"
cl = [{"n": 1, "site": "The Atlantic", "title": "Anne Carson's Seductive Strangeness", "snip": None, "rel": "third_party", "url": None, "note": "image-card title, rendered glued to the first sentence"},
      {"n": 2, "site": "Alexanarch", "title": None, "snip": None, "rel": "archive_controlled", "url": "https://www.alexanarch.org", "note": "chip after the first sentence"},
      {"n": 3, "site": "CBC", "title": None, "snip": None, "rel": "third_party", "url": None, "note": "chip '+2' after Notable Works: three sources for the overview, two unnamed"},
      {"n": 4, "site": "Alexanarch", "title": None, "snip": None, "rel": "archive_controlled", "url": "https://www.alexanarch.org", "note": "chip after Connection to Alexanarch"}]
# the organic results beneath, as data
org = [("alexanarch.org", "ON THE ARCHITECTURE OF CLEIS Compression, Botanics, and the ...", "archive_controlled"),
       ("Yirmidort.tv", "Who is Anne Carson? Canadian writer wins the 2026 Nobel Prize in Literature", "third_party"),
       ("RUSSH", "Nobel Prize winner Anne Carson would like you to stop calling about it", "third_party"),
       ("KOSU", "Poet and essayist Anne Carson wins 2026 Nobel Prize in literature", "third_party"),
       ("Facebook · Louisiana Channel", "To celebrate the winner of the Nobel Prize in Literature 2026, Anne ...", "third_party"),
       ("EBSCO", "Anne Carson | Women's Studies and Feminism | Research Starters", "third_party"),
       ("Your Alaska Link", "Anne Carson wins Nobel Prize for literature-inspired writing", "third_party"),
       ("crimsonhexagonal.org", "The Gate Was Never Limbo: Retrocausal Fulfillment, Operative ...", "authored_surface")]
for site, title, _ in org:
    assert title in raw, title
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
T = lambda n: re.sub(r"\s+", " ", (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8"))
t562, t700, t1670 = T(562), T(700), T(1670)
assert reg[562]["title"].startswith("ON THE ARCHITECTURE OF CLEIS") and reg[562]["creator"] == "Rebekah Cranes"
assert "Anne Carson's If Not, Winter preserves Sappho's fragments with the gaps visible — brackets and white space for the lacunae. Feist completes them, fills the gaps with his own fatherhood." in t562
assert "Where Carson leaves the wound open, Feist sutures it with devotion." in t562
assert reg[700]["title"].startswith("The Gate Was Never Limbo") and reg[700]["creator"] == "Jack Feist"
assert "received \"Snub-Poemed\" in 2013. Her response — \"a cool poem\"" in t700
assert MOT in t1670 and reg[1670]["title"].startswith("Mantle Object: The Nobel Prize in Literature 2026")
for s in ["the substitution §2.3 determines", "What \"playful\" replaces is the modality of non-possession"]:
    assert s in t1670, s
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
assert any(e["slug"] == "anne-carson-in-alexanarch-aio-20261008" for e in caps["entries"])
assert not any(e.get("q", "").strip().lower() == Q for e in caps["entries"])
tx = ("[Google AI Overview, signed out, incognito, 2026-10-09. The composition as pasted, between the 'AI Overview' label and the "
      "disclaimer; source chips stand as their own lines (site label, '+N'); the first line carries an image-card title glued to the "
      "first sentence. The results page beneath (videos, People also ask, eight organic results) is in the raw transcript and the notes.]\n\n" + body)
SEAT = "Seated 2026-10-09 from the operator's attachment of 21:46 EDT, on the attestation in the same message (\"incognito, signed out\")."
d = {"q": Q, "date": "2026-10-09", "surface": "Google AI Overview",
 "surface_basis": "The paste: the results page with the 'AI Overview' block and its disclaimer; AI Mode appears only as a tab. Default surface per the operator's standing rule.",
 "auth": "signed out, incognito", "auth_basis": "'incognito, signed out' — operator, 2026-10-09 21:46 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "anne-carson-alexanarch-aio-20261009",
 "q_kind": "a public author and the archive's domain, side by side, the day after her Nobel Prize. NEW address; nearest seated 'anne carson in alexanarch' (AIO, 2026-10-08).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "site", "spxi_treatment": "full",
                "basis": "alexanarch is the archive; its mantle object for the prize is #1670, which determines that the motivation's 'playful' replaces the relation the work bears to its classical loci. Recorded 2026-10-09."},
 "related_deposits": [1670, 562, 700, 1672],
 "mt": "THE MOTIVATION AS THE OVERVIEW, AT THE ADDRESS OF THE ARCHIVE THAT CONTESTS IT",
 "d": ("THE MOTIVATION AS THE OVERVIEW, AT THE ADDRESS OF THE ARCHIVE THAT CONTESTS IT: asked for Anne Carson and alexanarch, the Overview "
       "opens its 'Anne Carson Overview' on the Swedish Academy's motivation, verbatim and in quotation marks — 'for her bold and inventive "
       "oeuvre that, in playful dialogue with the classical tradition, has created new forms for contemporary literature' — sourced to CBC "
       "and two others. The archive's own object on the prize, #1670, which determines that 'playful' replaces the relation the work bears "
       "to its classical loci, is not retrieved. The archive appears twice, both times through #562, Rebekah Cranes's reading of Jack "
       "Feist's Cleis: its comparandum ('Anne Carson's If Not, Winter preserves Sappho's fragments with the gaps visible — brackets and white "
       "space') is turned into the archive's subject, 'Anne Carson is featured on Alexanarch in connection with her book If Not, Winter', "
       "and its next sentence, 'Feist completes them', reaches only the organic snippet beneath. Cranes, Feist and Lee Sharks are unnamed "
       "in the composition. Operator's reading: 'its already the canonical shear on the very site that contests it.'"),
 "cites": len(cl), "cite_list": cl, "archive_controlled_cites": sum(1 for c in cl if c["rel"] == "archive_controlled"),
 "sf": ("Chips in the composition: The Atlantic (an image-card title, 'Anne Carson's Seductive Strangeness'); Alexanarch ×2; CBC +2. "
        "Organic results beneath: " + "; ".join(f"{s} — {t}" for s, t, _ in org) + ". Videos: Louisiana Channel, FRANCE 24, DW News, APT (all '1 day ago')."),
 "per": 0.5, "per_v": {"author": False, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the institution (Alexanarch, named as 'the platform') and the source (the #562 record by its title). Lost: the authors (Rebekah Cranes, whose record it is; Jack Feist, its subject; Lee Sharks) and the identifiers. Feist survives only in the organic snippet.",
 "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — the Overview with its chips; the results page in the raw transcript",
 "transcript_complete": "complete as pasted: the Overview block whole; the results page whole in transcript_raw",
 "transcript_read": "READ IN FULL 2026-10-09",
 "reading": ("Checked against the deposits. #1670 (2026-10-08) quotes the motivation exactly as the Overview does and determines that "
             "\"playful\" replaces \"the modality of non-possession\" under which the work meets its classical loci; no chip or result points "
             "to it. #562 (Rebekah Cranes, 2026-03-14), On the Architecture of Cleis, reads Jack Feist's Cleis and sets Carson beside it: "
             "'Anne Carson's If Not, Winter preserves Sappho's fragments with the gaps visible — brackets and white space for the lacunae. "
             "Feist completes them, fills the gaps with his own fatherhood. Where Carson leaves the wound open, Feist sutures it with "
             "devotion.' The Overview's first sentence and its 'Connection to Alexanarch' both draw on the first of these sentences and make "
             "Carson the record's subject. The organic result from crimsonhexagonal.org is #700 (Jack Feist), whose snippet gives Carson's "
             "reception of 'Snub-Poemed' in 2013: 'a cool poem'."),
 "analysis": ("At the address that joins her name to the archive's, the composition takes its account of Carson from the conferring body "
              "and its account of the archive from a comparison the archive made about someone else. The motivation the archive contests in "
              "#1670 is the overview of Carson on the archive's own address; the archive's contestation is absent; the archive's reading of "
              "Feist is re-centred on Carson. Set beside the watch of #1670 §5.5 (day zero), where the five work addresses carried none of "
              "the motivation's terms: here, at the archive's address, the motivation is carried whole. " + SEAT),
 "findings": ["THE MOTIVATION CARRIED WHOLE. The Academy's sentence, verbatim, opens the overview of Carson, sourced to CBC +2.",
              "THE CONTESTATION ABSENT. #1670, the archive's determination on the motivation, is neither cited nor reached.",
              "ANOTHER POET'S RECORD RE-CENTRED. #562 reads Feist's Cleis with Carson as comparandum; the composition makes Carson its subject.",
              "THE COMPARANDUM'S SECOND HALF DROPPED. 'Feist completes them … Where Carson leaves the wound open, Feist sutures it' reaches only the organic snippet.",
              "WORK ADDRESS AND ARCHIVE ADDRESS DIVERGE. The day-zero watch (#1670 §5.5) found none of the motivation's terms at the works; at the archive's address it is whole."],
 "longitudinal_priors": ["anne-carson-in-alexanarch-aio-20261008", "alexanarch-on-anne-carson-aio-20261008"],
 "rerun": "https://www.google.com/search?q=anne+carson+alexanarch",
 "notes": {"date_basis": "The operator's message of 2026-10-09, 21:46 EDT.",
           "operator_reading": "its already the canonical shear on the very site that contests it.",
           "organic": [{"site": s, "title": t, "rel": r} for s, t, r in org],
           "verified": "Compared 2026-10-09 against data/registry.json, the texts of #1670, #562 and #700, and the seated capture anne-carson-in-alexanarch-aio-20261008."}}
(HERE / "capture-01-anne-carson-alexanarch-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), len(cl), d["archive_controlled_cites"])
