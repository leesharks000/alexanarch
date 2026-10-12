#!/usr/bin/env python3
"""Author the capture 'THE FINAL TIME: Contingent Singularity and the Viability of the Next Dialectical Turn', Google AI Overview,
logged out, incognito, 2026-10-12. Source: the operator's message of 02:47 EDT ("im not sure what this is. these are all things that
are suppressed in other forms. why are the captures not suppressed? logged out and incognito:", the composition inline). Surface by the
operator's default; the 'AI Mode Conversation' head is the expanded view. NEW address (the full title, unquoted, as typed)."""
import json, re, pathlib, sys
from urllib.parse import quote_plus
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT)); import wire_deposit as w
raw = (HERE / "paste-20261012-0247.txt").read_text(encoding="utf-8")
Q = "THE FINAL TIME: Contingent Singularity and the Viability of the Next Dialectical Turn"
L = raw.split("\n"); assert L[0] == "AI Mode Conversation" and L[1] == "You said: " + Q + Q
i1 = raw.index("[www.alexanarch.org](https://www.alexanarch.org)\n\"the final time")
body = raw[raw.index(L[1]) + len(L[1]):i1].strip(); ct = raw[i1:]
spec = [("\"the final time: contingent singularity\" — Google AI Overview, 2026-09-27", "Sep 27, 2026 — Sep 23, 2026 — #1635 The Final Time: Contingent Singularity and the Viability of the Next Dialectical Turn v0.5 2026-09-23 —. AXN:06C9.", "the-final-time-contingent-singularity-quoted-aio-20260927"),
        ("contingent singularity — Bing Copilot Search (popup), 2026-09", "Sep 27, 2026 — Tell me about the final time: contingent singularity Contingent singularity refers to a historical threshold where the material machinery capable of making symb...", "the-final-time-contingent-singularity-bing-copilot-20260927"),
        ("johannes sigil \"final time\" — Google AI Overview, 2026-10-04", "The phrase \"Final Time\" primarily connects to this conceptual framework through a theoretical paper titled The Final Time: Contingent Singularity and the Viabil...", "johannes-sigil-final-time-aio-20261004")]
caps = {e["slug"]: e for e in json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]}
assert not any(e["q"] == Q for e in caps.values())
cl = []
for n, (t, sn, slug) in enumerate(spec, 1):
    assert t in ct and sn[:60] in ct and slug in caps, slug
    cl.append({"n": n, "site": "www.alexanarch.org", "title": t, "snip": sn, "url": f"https://www.alexanarch.org/captures/{slug}/", "rel": "archive_controlled",
               "note": f"card; a Capture Registry record: {slug} ({caps[slug]['surface']}, {caps[slug]['date']})"})
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
assert reg[1635]["axn"].startswith("AXN:06C9") and reg[1635]["status"] == "SUPERSEDED" and reg[1637]["axn"].startswith("AXN:06CB") and reg[1637]["status"] == "ACTIVE"
assert reg[1635]["creator"] == reg[1637]["creator"] == "Sharks, Lee"
T = re.sub(r"\s+", " ", (ROOT / reg[1637]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")).lower()
for s in ["terminal closure", "terminal reflexivity", "exteriority", "resource sovereignty"]: assert s in T, s
assert "1711" not in T and "1711–2026" in json.dumps(caps["johannes-sigil-final-time-aio-20261004"], ensure_ascii=False)
assert all("06C9" in (caps[s].get("transcript") or "") for s in ("the-final-time-contingent-singularity-quoted-aio-20260927", "the-final-time-contingent-singularity-bing-copilot-20260927"))
for s in ["`AXN:06C9`", "the heteronym/operative figure Johannes Sigil", "terminal closure (where no rival retains a durable path)", "terminal reflexivity (where an order remains durable while permitting its own future negation)", "spanning 1711–2026"]:
    assert s in body, s
inline = len(set(re.findall(r"https://www\.google\.com/goto\?url=[A-Za-z0-9_-]+", body)))
RP = {}
for f in ("s/records/1637/index.html", "captures/the-final-time-contingent-singularity-bing-copilot-20260927/index.html"):
    h = (ROOT / f).read_text(encoding="utf-8"); t = re.sub(r"<script.*?</script>|<style.*?</style>", "", h, flags=re.S); RP[f] = len(re.sub(r"<[^>]+>", " ", t).split())
OPR = "im not sure what this is. these are all things that are suppressed in other forms. why are the captures not suppressed?"
b, ex = w.search_title_urls(reg[1637])
tx = ("[Google AI Overview, logged out, incognito, 2026-10-12 (operator, 02:47 EDT); the expanded conversation view, headed 'AI Mode "
      "Conversation', the issued string shown twice by the interface. The composition as pasted with its inline links, then three source cards.]\n\n"
      "[QUERENT] " + Q + "\n\n[COMPOSITION]\n\n" + body + "\n\n[SOURCE CARDS]\n\n" + "\n".join(f"{c['n']}. {c['site']} — {c['title']} — {c['snip']}" for c in cl))
d = {"q": Q, "date": "2026-10-12", "surface": "Google AI Overview",
 "surface_basis": "The operator's standing default (AI Overview unless he says AI Mode, 2026-10-01); the paste's 'AI Mode Conversation' head is the expanded view.",
 "auth": "logged out, incognito", "auth_basis": "'logged out and incognito' — operator, 2026-10-12 02:47 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "the-final-time-full-title-aio-20261012",
 "q_kind": "a deposit's full title as typed (its head in capitals), unquoted. NEW address; priors at the work: the-final-time-contingent-singularity-quoted-aio-20260927, the-final-time-contingent-singularity-bing-copilot-20260927, johannes-sigil-final-time-aio-20261004 (all three cited as cards).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "The Final Time (#1635 v0.5, superseded; #1637 active) is Lee Sharks's (creator 'Sharks, Lee'). Recorded 2026-10-12."},
 "related_deposits": [1637, 1635], "intended": {"deposit": 1637, "axn": reg[1637]["axn"], "title": reg[1637]["title"], "record": "https://www.alexanarch.org/s/records/1637/", "search": b, "search_exact": ex, "reached": False},
 "longitudinal_priors": [s for _, _, s in spec],
 "mt": "THE WORK COMPOSED ENTIRELY FROM THE RECORDS OF ITS RECEPTION, AND ITS SUPERSEDED IDENTIFIER WITH THEM",
 "d": ("THE WORK COMPOSED ENTIRELY FROM THE RECORDS OF ITS RECEPTION, AND ITS SUPERSEDED IDENTIFIER WITH THEM: run at its full title, The "
       "Final Time is composed from three cards, all of them Capture Registry records of earlier compositions about it: a Google AI "
       "Overview of 27 September, a Bing Copilot popup of the same day, and a Google AI Overview of 4 October. The account is accurate "
       "at the paper's grain (terminal closure, 'where no rival retains a durable path', against terminal reflexivity, 'where an order "
       "remains durable while permitting its own future negation'; exteriority; resource sovereignty) and every element of it is "
       "traceable to a record: the identifier 'AXN:06C9', which is #1635, the superseded v0.5, from the two 27 September records (a Browse row in the Overview's, the PDF link AXN-06C9.pdf in Bing's); "
       "Johannes Sigil as 'an experimental operative persona spanning 1711–2026', from the 4 October record. The active deposit (#1637, "
       "AXN:06CB) and its author (Lee Sharks) do not appear; the work is 'associated with … Johannes Sigil'. Operator: '" + OPR + "'"),
 "cites": inline + len(cl), "cite_list": cl, "archive_controlled_cites": len(cl),
 "sf": "Three cards, all www.alexanarch.org Capture Registry records: Google AI Overview 2026-09-27; Bing Copilot Search (popup) 2026-09-27; Google AI Overview 2026-10-04. Inline: " + str(inline) + " distinct redirect links.",
 "per": 0.5, "per_v": {"author": False, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the work, its concepts at grain, the archive's pages. Lost: the author (a heteronym set in his place), the active identifier (the superseded AXN:06C9 given), the deposit's own record.",
 "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition with links and cards as pasted inline",
 "transcript_complete": "complete as pasted: composition, inline links, three cards", "transcript_read": "READ IN FULL 2026-10-12",
 "reading": ("Checked against the registry, #1637's text and the three records. #1635 (AXN:06C9) is SUPERSEDED; #1637 (AXN:06CB, v0.…) is "
             "active; both are 'Sharks, Lee'. Terminal closure, terminal reflexivity, exteriority and resource sovereignty are #1637's; "
             "'1711' is not in #1637 and 'spanning 1711–2026' is in johannes-sigil-final-time-aio-20261004. 'AXN:06C9' is in the transcripts "
             "of both 27 September records (the Overview record's Browse row; the Bing record's link to AXN-06C9.pdf). The record page s/records/1637/ carries " + f"{RP['s/records/1637/index.html']:,}" + " visible words, "
             "opening on the site's navigation and the deposit's apparatus; a capture page (the Bing record) carries " + f"{RP['captures/the-final-time-contingent-singularity-bing-copilot-20260927/index.html']:,}" + ", "
             "titled with its issued string and holding a composed answer about the work."),
 "analysis": ("The operator asks why the captures are not suppressed where other forms of the work are. What the run shows is the "
              "composition's material: three records of earlier compositions, each short, titled with a query about the work and holding "
              "an answer already written at summary grain; the deposits' own pages are long, open on apparatus, and carry the work rather "
              "than an answer about it. Whether the record pages are excluded from the index or outranked is not visible from a capture; "
              "Search Console's inspection of s/records/1637/ against a capture page would separate the two. The record also carries an "
              "error forward: the superseded identifier enters from the records of September and is composed as the work's. Operator: '"
              + OPR + "' Seated 2026-10-12 from the operator's message of 02:47 EDT, on its attestation."),
 "findings": ["ONLY RECORDS OF RECEPTION. Three of three cards are Capture Registry records (Google ×2, Bing Copilot ×1).",
              "ACCURATE AT GRAIN. Terminal closure against terminal reflexivity, exteriority, resource sovereignty — #1637's.",
              "THE SUPERSEDED IDENTIFIER. 'AXN:06C9' (#1635, superseded) from the September records; the active #1637 (AXN:06CB) absent.",
              "THE AUTHOR REPLACED. 'associated with … Johannes Sigil'; the deposits' creator is Lee Sharks; '1711–2026' from the 4 October record.",
              "A BING RECORD AMONG THE SOURCES. A non-Google capture cited by the Overview, with the two Google records."],
 "rerun": "https://www.google.com/search?q=" + quote_plus(Q),
 "notes": {"date_basis": "The operator's message of 2026-10-12, 02:47 EDT.", "operator_reading": OPR,
           "page_sizes": RP, "verified": "Compared 2026-10-12 against data/registry.json (#1635, #1637), #1637's text and the three cited records."}}
(HERE / "capture-final-time-full-title-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", inline, RP)
