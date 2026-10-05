#!/usr/bin/env python3
"""Author the capture 'revelationfirst.com', Google AI Overview, signed out, incognito, 2026-10-05.

Source: the operator's message of 2026-10-05 01:50 EDT (paste-20261005-0150.txt), re-sent after the 01:19 message's inline paste
was lost from the session. Attestation and workaround from the 01:19 message: "all logged out, incognito"; "the revelation first
was achieved by a workaround. i typed revelationfirst.com in, it said displaying results for revelation first, i clicked show
results for revelation first and it stayed the same - but those are in no way the results it would normally show for unquoted
revelation first, even tho it is composing as if for the entity revelation first." Surface recorded as Google AI Overview by the
operator's default of 2026-10-01; the 'AI Mode Conversation' header is not evidence of surface. The address is the string typed,
'revelationfirst.com'; the page rewrote it to 'revelation first' (the paste's echo, doubled). NEW address.
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261005-0150.txt").read_text(encoding="utf-8")
Q = "revelationfirst.com"
head = "AI Mode Conversation\nYou said: revelation firstrevelation first\n"
assert raw.startswith(head)
body = raw[len(head):]
k = body.index("\nrevelationfirst.com\n")
ans, rail = body[:k].strip(), body[k:]
ANS = re.sub(r" ?\[\[1\]\(https://www\.google\.com/goto\?url=[^)]*\)\]", "", ans)
assert "google.com" not in ANS

C = [("revelationfirst.com", "Revelation First — The Apocalypse as the Earliest New Testament Document",
      "The Revelation First thesis argues the Apocalypse of John was the first book composed in the New Testament — preceding Paul's letters and the Synoptic Gospels."),
     ("revelationfirst.com", "Revelation First — The Apocalypse as the Earliest New Testament Document",
      "reception measured via MMRS Capture Registry. Author: Lee Sharks (ORCID 0009-0000-1599-0703). ∮ = 1")]
cards = [{"n": i, "site": s, "rel": "authored_surface", "url": None, "title": t, "snip": sn,
          "note": "revelationfirst.com, the thesis site; title verified 2026-10-05"} for i, (s, t, sn) in enumerate(C, 1)]
for c in cards:
    for f in ("site", "title", "snip"):
        assert c[f] in rail, (c["n"], f)
assert rail.count("\nrevelationfirst.com\n") == 2

QUOTES = ["The Revelation First thesis argues that the Apocalypse of John was written before any other New Testament book, predating both Paul's letters and the Synoptic Gospels.",
          "Early Dating: It proposes a composition date before 70 CE during the Neronian or Galban era, rather than the traditional late first-century Domitianic date.",
          "The First Corpus: Revelation establishes a seven-church letter structure before any similar closed Pauline corpus circulated.",
          "Distinct from Myth: The thesis maintains that the Logos is real and rejects the Jesus Myth perspective.",
          "Research Program: Authored by Lee Sharks as an open scholarly framework with defined falsification criteria.",
          "Conditional Rungs: Advanced extensions explore author-functions and textual formatting under Roman historical context."]
for q in QUOTES:
    assert q in ANS, q

ROOT = HERE.parents[2]
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
def text(n):
    return (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8", errors="ignore")
t202, t1217 = text(202), text(1217)
assert "favors, a pre-70 CE reading" in t202 and "Claim 4: Revelation as seed." in t202 and "The seven letters (Rev 2–3) become the epistolary form." in t202
assert "the Josephus Thesis is NOT the Jesus Myth thesis" in t1217 and "The Logos is real." in t1217
assert "Falsification Conditions." in text(832)
assert "Galba" not in t202 and "Galba" not in t1217
assert "during the reign of Emperor Nero or Galba" in text(830) and "during the reign of Emperor Nero or Galba" in text(1025)
SEATED = [text(n) for n, x in reg.items() if (x.get("full_text_path") or "").startswith("/data/texts/") and (ROOT / x["full_text_path"].lstrip("/")).exists()]
assert not any("closed Pauline corpus" in s or "Conditional Rung" in s for s in SEATED)

SITE = {"title": "Revelation First — The Apocalypse as the Earliest New Testament Document",
        "lines": ["A Neronian or Galban date persists as a serious minority position.",
                  "The sevenfold address preceded and helped generate the later construal of Paul's letters as a closed corpus to seven churches.",
                  "Each rung stands without the ones above it.", "This rung is contingent by construction.",
                  "Not the Jesus Myth thesis. The Logos is real.", "The residue is published as the falsification surface.",
                  "reception measured via MMRS Capture Registry"]}

WORKAROUND = ("\"the revelation first was achieved by a workaround. i typed revelationfirst.com in, it said displaying results for revelation "
              "first, i clicked show results for revelation first and it stayed the same - but those are in no way the results it would "
              "normally show for unquoted revelation first, even tho it is composing as if for the entity revelation first.\" — operator, 2026-10-05 01:19 EDT.")
tx = ("[Google AI Overview (operator default of 2026-10-01), incognito, signed out; the paste carries the header 'AI Mode Conversation', "
      "which is not evidence of surface. Typed: 'revelationfirst.com'; the page rewrote it to 'revelation first' (the paste's echo, "
      "doubled: 'revelation firstrevelation first'). Inline citation links ([1]) cut.]\n\n" + ANS + "\n\n"
      + "\n".join(f"[source card] {c['site']} — \"{c['title']}\" — {c['snip']}" for c in cards))

SEAT = "Seated 2026-10-05 from the operator's message of 01:50 EDT, on the attestation and account of the workaround in the message of 01:19 EDT (\"all logged out, incognito\")."
d = {
 "q": Q, "date": "2026-10-05", "surface": "Google AI Overview",
 "surface_basis": "Operator default of 2026-10-01; no AI Mode stated. The 'AI Mode Conversation' header is not evidence of surface.",
 "auth": "signed out, incognito", "auth_basis": "'all logged out, incognito' — operator, 2026-10-05 01:19 EDT, for the batch.",
 "ev": "paste", "s": "Revelation & Theology",
 "slug": "revelationfirst-com-aio-20261005",
 "q_kind": ("a domain name typed as the query, rewritten by the page to 'revelation first' ('displaying results for revelation first'); "
            "'show results for revelation first' clicked, unchanged. NEW address; the composition is the entity's, and on the operator's "
            "account the results differ from those for unquoted 'revelation first' (seated 2026-06-24)."),
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "site", "spxi_treatment": "full",
                "basis": "revelationfirst.com is the archive's thesis site; the Revelation First thesis is Lee Sharks's (#202, #832, #1217). Recorded 2026-10-05."},
 "related_deposits": [202, 832, 1217, 1211, 830, 1025],
 "mt": "THE DOMAIN READ AS THE ENTITY, FROM ITS OWN SITE",
 "d": ("THE DOMAIN READ AS THE ENTITY, FROM ITS OWN SITE: typed as a domain and rewritten to 'revelation first', the query gets an Overview "
       "of the Revelation First thesis composed from two revelationfirst.com cards. It covers Revelation before Paul and the Synoptics, the "
       "seed, the midrashim transform, a pre-70 date, the sevenfold address ahead of a closed Pauline corpus, 'the Logos is real' against "
       "the Jesus Myth thesis, falsification criteria, and 'Conditional Rungs'. It is attributed to Lee Sharks. Every element matches the "
       "site. 'Galban' and the ladder of rungs come from the site's wording and are not in the deposits; there the pre-70 date is Nero's."),
 "cites": 2, "cite_list": cards, "archive_controlled_cites": 2,
 "sf": "2 source cards, both revelationfirst.com (the same page, two snippets: the thesis line and the MMRS/author/ORCID line).",
 "per": 0.25, "per_v": {"author": True, "inst": False, "id": True, "src": True},
 "per_note": "Retained: the author (Lee Sharks), the identifier (ORCID 0009-0000-1599-0703, on the second card) and the source (revelationfirst.com). Lost: the institution (no Crimson Hexagonal Archive; the card's 'MMRS Capture Registry' only).",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
 "transcript_complete": "Complete as supplied: one answer with its card rail. Re-sent by the operator at 01:50 EDT after the 01:19 paste was lost from the session.",
 "transcript_read": "READ IN FULL 2026-10-05",
 "reading": (
   "The operator typed the domain. Google answered 'displaying results for revelation first', and the offered 'show results for "
   "revelation first' left the page unchanged. The Overview composes the entity, with the site as its only source. Checked against the "
   "deposits and the site (fetched 2026-10-05): the priority claim, the seed and the midrashim transform are #202's (Claim 4: 'The seven "
   "letters (Rev 2–3) become the epistolary form'). 'The Logos is real' and the separation from the Jesus Myth thesis are #1217's, and the "
   "falsification criteria are #832's 'Falsification Conditions'. Three phrasings are the site's and not the deposits'. The site has 'A "
   "Neronian or Galban date persists as a serious minority position'; in the deposits the pre-70 date is argued from Nero (666/616), and "
   "Galba appears only inside the baseline's quotation of an earlier Google composition (#830, #1025). The site has 'the later construal "
   "of Paul's letters as a closed corpus to seven churches', which the answer gives as 'closed Pauline corpus'. And the site's ladder ('Each "
   "rung stands without the ones above it') becomes 'Conditional Rungs'. The composition follows the site at its own resolution, with "
   "attribution and the ORCID on the rail. " + WORKAROUND),
 "analysis": ("A domain query turned into the entity's Overview; the site's own wording carried at the site's resolution. Companion to "
              "'\"revelation first thesis\"' (2026-10-02) and 'revelation first crimson hexagonal' (2026-09-22). " + SEAT),
 "findings": [
   "THE DOMAIN REWRITTEN TO THE ENTITY. 'revelationfirst.com' → 'revelation first'; 'show results for' unchanged; composed as the thesis.",
   "ONE SITE, TWO CARDS. Both cards revelationfirst.com; the second carries 'Author: Lee Sharks (ORCID 0009-0000-1599-0703)'.",
   "THE THESIS ACCURATE. Priority, seed, midrashim transform, pre-70, 'the Logos is real' against the Jesus Myth, falsification — as #202, #832, #1217.",
   "THE SITE'S WORDING, NOT THE DEPOSITS'. 'Galban', the closed Pauline corpus, the rungs: on the site; Galba in the deposits only inside a quoted Google composition (#830, #1025).",
   "ATTRIBUTED. 'Authored by Lee Sharks as an open scholarly framework'.",
 ],
 "longitudinal_priors": ["revelation-first-adoption", "revelation-first-overview", "revelation-first-crimson-hexagonal-aio-20260922", "revelation-first-thesis-aio-20261002"],
 "rerun": "https://www.google.com/search?q=revelationfirst.com",
 "notes": {"date_basis": "The operator's messages of 2026-10-05, 01:19 and 01:50 EDT.",
           "workaround": WORKAROUND,
           "site_checked": "revelationfirst.com fetched 2026-10-05: title '" + SITE["title"] + "'; lines: " + " | ".join(SITE["lines"]),
           "verified": ("Compared 2026-10-05 against #202 (pre-70, Claim 4, the seven letters), #1217 (Jesus Myth; 'The Logos is real.'), #832 "
                        "(Falsification Conditions), #830/#1025 (Galba inside a quoted Google composition) and the site. 'closed Pauline corpus' and "
                        "'Conditional Rung' absent from every seated deposit text.")},
}
(HERE / "capture-01-revelationfirst-com-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx))
