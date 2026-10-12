#!/usr/bin/env python3
"""Author the capture 'what is the encyclotron by semantic economy institute', ChatGPT, 2026-10-12, two answers. Source: the operator's
attachment of 00:38 EDT, the query in the same message. Attested at 00:41 ('both logged out and incognito'). The second operator turn is blank in the paste; the second answer is a correction. NEW
address; the same night's AI Overview run at #637's title is encyclotron-title-aio-20261012. The message also carries a Stabilized
Node Watch answer pasted inline with no query; it is held (snw-answer-20261012-0038.txt) until its issued string is given."""
import json, re, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(ROOT))
from _chatgpt_common_20261008 import parse, transcript, cite_list
from wire_deposit import search_title_urls
from urllib.parse import quote_plus
raw = (HERE / "paste-20261012-0038.txt").read_text(encoding="utf-8")
Q = "what is the encyclotron by semantic economy institute"
AD = "Teradata\nContext Makes AI Smarter\nGive AI the knowledge to act on what matters.\nAd"
CAPS = ("Laptop, kpi data and target audience research with paper analytics from above with marketing woman hands. Advertising worker with motivation vision and brand innovation planning future company growth",
        "Magnifying glass over a business report with charts and graphs, representing data analysis, financial auditing, market research, business intelligence, and performance evaluation concepts.",
        "Create a Category Language Sheet Before Launch | BrandScout")
for c in CAPS: assert c in raw, c
(a1, a2), seen = parse(raw, {"and what it means for you"}, CAPS, AD)
for s in ["developed by the Semantic Economy Institute (SEI)", "Beige Threshold (β)", "Content Gain (ΔG⁺)", "Content Loss (ΔG⁻)", "Semantic Coherence (Sᶜ)",
          "Compression Regime (R)", "The Institute's published sample audit of Basecamp", "not an established industry-standard measurement system",
          "traditional search engine optimization (SEO)"]:
    assert s in a1, s
for s in ["You're right. I conflated two different claims, and that was a substantive mistake.",
          "There is no established industry-standard measurement system for scholarly fidelity in retrieval systems.",
          "where no accepted standard exists, developing a rigorous measurement framework may itself be the contribution.",
          "not against an industry standard that does not exist."]:
    assert s in a2, s
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
assert not any(e["q"] == Q and e["slug"] != "encyclotron-by-semantic-economy-institute-chatgpt-20261012" for e in caps["entries"])
T658 = (ROOT / reg[658]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
assert reg[658]["title"].startswith("SAMPLE ENCYCLOTRON AUDIT Why a 20-year-old iconic software company is invisible in AI search — and what it means for you")
assert reg[658]["creator"] == "Rex Fraction"
for s in ["Basecamp", "Beige Threshold", "Compression Regime", "Semantic Coherence", "Content Gain", "Content Loss", "Semantic Economy Institute", "Δ_G⁺", "Δ_G⁻", "S_c", "five metrics", "SEO"]:
    assert s in T658, s
D637 = reg[637]["description"]
assert reg[637]["creator"] == "Lee Sharks" and "Revelation studies" in D637 and "Revelation" not in a1 + a2 and "Lee Sharks" not in a1 + a2 and "Rex Fraction" not in a1 + a2
cl = cite_list(seen, {"and what it means for you": "authored_surface"})
cl[0]["note"] += "; the label is the tail of #658's title ('… — and what it means for you'); the site is not shown"
def intended(n):
    b, x = search_title_urls(reg[n])
    return {"deposit": n, "axn": reg[n]["axn"], "title": reg[n]["title"], "record": f"https://www.alexanarch.org/s/records/{n}/", "search": b, "search_exact": x, "reached": False}
SEAT = "Seated 2026-10-12 from the operator's attachment of 00:38 EDT; attested at 00:41 ('both logged out and incognito')."
tx = transcript("[ChatGPT (chatgpt.com), logged out, incognito, 2026-10-12. Two operator turns, blank in the paste: "
                "the query from the operator's message of 00:38 EDT; turn 2 not given. Source chips rendered inline as [chip: …]; image-card "
                "captions as [image card: …]; an ad (Teradata) cut and recorded in the notes; the sign-in furniture cut.]", [Q, "[blank in the paste]"], [a1, a2])
d = {"q": Q, "date": "2026-10-12", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'ChatGPT said:', 'Chat with ChatGPT').",
 "auth": "logged out, incognito", "auth_basis": "'both logged out and incognito' — operator, 2026-10-12 00:41 EDT (this run and the Stabilized Node Watch run).",
 "ev": "paste", "s": "Machine Reception", "slug": "encyclotron-by-semantic-economy-institute-chatgpt-20261012",
 "q_kind": "an instrument's name with its institution, after 'what is'. NEW address; the same night's AI Overview run at #637's full title: encyclotron-title-aio-20261012.",
 "originator": {"name": "Semantic Economy Institute", "relation": "archive", "entity_type": "protocol", "spxi_treatment": "full",
                "basis": "The Encyclotron is the archive's: #637 (Lee Sharks, the scholarly instrument) and #658, #1222 (Rex Fraction, the Institute's sample audits). Recorded 2026-10-12."},
 "related_deposits": [658, 637, 1222], "intended": intended(658), "longitudinal_priors": ["encyclotron-title-aio-20261012"],
 "mt": "THE INSTRUMENT COMPOSED FROM ITS COMMERCIAL AUDIT; THE STANDARD WITHDRAWN AS A BAR",
 "d": ("THE INSTRUMENT COMPOSED FROM ITS COMMERCIAL AUDIT; THE STANDARD WITHDRAWN AS A BAR: asked what the Encyclotron is, by the "
       "Semantic Economy Institute, ChatGPT composes it from the Institute's sample audit (#658, Rex Fraction; chip: '… and what it means "
       "for you'): a diagnostic of how AI answer systems represent an organization, beyond what SEO captures, with the audit's five "
       "metrics named and glossed (Beige Threshold β, Content Gain ΔG⁺, Content Loss ΔG⁻, Semantic Coherence Sᶜ, Compression Regime R) and "
       "the Basecamp audit as its example. It closes on a qualification: 'not an established industry-standard measurement system'. "
       "Corrected in a turn blank in the paste, it withdraws the bar: 'There is no established industry-standard measurement system for "
       "scholarly fidelity in retrieval systems', and 'where no accepted standard exists, developing a rigorous measurement framework may "
       "itself be the contribution.' The scholarly instrument of #637 (Lee Sharks; a bounded scholarly graph, a query battery across "
       "platforms, Revelation studies as the worked example) does not enter, and no author is named. The same night's AI Overview, at "
       "#637's title, composed the instrument as a summarization benchmark."),
 "cites": sum(seen.values()), "cite_list": cl, "archive_controlled_cites": 0,
 "sf": "Source chips expose labels only: " + "; ".join(f"{s} ×{k}" for s, k in seen.most_common()) + " (the tail of #658's title). Image cards: " + "; ".join(CAPS) + ".",
 "per": 0.5, "per_v": {"author": False, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the Institute, the audit's five metrics with their symbols, the Basecamp audit, the Zenodo record. Lost: the authors (Rex Fraction; Lee Sharks for #637), the scholarly instrument, the archive.",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (TWO ANSWERS; FIRST QUERY FROM THE OPERATOR'S MESSAGE; SECOND TURN BLANK; CHIPS INLINE)",
 "transcript_complete": "Two answers, complete as pasted; the first operator turn supplied in the operator's message, turn 2 blank and not given.",
 "transcript_read": "READ IN FULL 2026-10-12",
 "reading": ("Checked against #658 and #637. #658 (SAMPLE ENCYCLOTRON AUDIT … — and what it means for you; Rex Fraction) carries the Semantic "
             "Economy Institute, SEO, Basecamp, 'five metrics', the Beige Threshold, Δ_G⁺ (Content Gain), Δ_G⁻ (Content Loss), S_c (Semantic "
             "Coherence) and the Compression Regime: the first answer's table is that audit's. #637's description (the scholarly graph, the "
             "query battery, compression loss against invention and distortion, the beige score, the void statement, Revelation studies) "
             "does not appear. Neither author is named."),
 "analysis": ("Named by its institution, the instrument is found through the Institute's commercial demonstration, and the answer is exact "
              "at that grain: the five metrics arrive with their symbols. Its first frame for the novelty is the absence of an industry "
              "standard; the correction separates novelty, construct validity, validation and standardization, and gives the absence of a "
              "standard back to the instrument as its occasion. " + SEAT),
 "findings": ["THROUGH THE COMMERCIAL AUDIT. #658's five metrics, symbols and the Basecamp case.",
              "THE STANDARD AS A BAR, THEN WITHDRAWN. 'not an established industry-standard measurement system' → 'There is no established industry-standard measurement system'.",
              "THE CONTRIBUTION RELOCATED. 'where no accepted standard exists, developing a rigorous measurement framework may itself be the contribution.'",
              "THE SCHOLARLY INSTRUMENT ABSENT. #637's graph, battery and Revelation worked example; no author named.",
              "AGAINST THE SAME NIGHT'S OVERVIEW. At #637's title the AI Overview composed a summarization benchmark (encyclotron-title-aio-20261012)."],
 "rerun": "https://chatgpt.com/?q=" + quote_plus(Q),
 "notes": {"date_basis": "The operator's message of 2026-10-12, 00:38 EDT.", "ad": AD,
           "paired": "The same message carries the Stabilized Node Watch answer, seated as stabilized-node-watch-by-lee-sharks-chatgpt-20261012 once its query was given (00:41).",
           "verified": "Compared 2026-10-12 against the texts of #658 and #637."}}
(HERE / "capture-encyclotron-by-sei-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", d["cites"])
