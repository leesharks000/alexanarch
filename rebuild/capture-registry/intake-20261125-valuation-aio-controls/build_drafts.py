"""Eleven Google AI Overview compositions of 2026-11-25, signed out, incognito: the valuation of Alexanarch and its ecosystem as emerging
semantic infrastructure, composed twice on one open results page (the second a recomposition by the surface, a few minutes after the
first), and nine valuations of external entities run the same morning as controls (Anne Carson's literary corpus, UbuWeb, the Getty
Research Institute, PennSound, the Poetry Foundation, ZineWiki, LibriVox, the Internet Archive, the Electronic Literature Organization)
-> draft-01.json … draft-11.json.

WHERE THE TEXT COMES FROM. The operator's pastes were staged as drafts on the branch intake/pending-aio-valuation-pair-20261125 at commit
a99c545b5 (committed under the operator's GitHub account, 04:10–05:21 EST), under rebuild/capture-registry/pending/. Those eleven drafts and
their cross-observation note are copied here unchanged, in staged/, and the transcripts are read from them. The staged drafts were refused
by capture_intake.py as they stood (notes as a string where the schema takes an object; sections «Alexanarch» and «Literature», which are
not defined sections; the surface named «Google AI Overview (popup)», where the registry's 652 Overview addresses are «Google AI Overview»);
the manual workflow capture-seat-20261125.yml was run by the operator and seated nothing. This build corrects those three and writes each
capture's reading and analysis from its transcript; eight of the staged controls carried one templated reading and analysis.

WHAT IS NOT HERE. The source cards of the two Alexanarch compositions (the staging note: 'Source-card details and exact clock times are not
preserved'); the search-results attachment that came with the second; the single eight-entity paste the eight later controls were cut from,
with its headers and organic results. The two Alexanarch transcripts are the stager's Markdown-normalized rendering of the operator's paste
(headings and tables re-marked), which the staging note states; the first was pasted into a Claude session that timed out and was recovered
from that paste. None of these is supplied to this session; each absence is recorded on the record it concerns."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
S = H / "staged"
STG = "staged on intake/pending-aio-valuation-pair-20261125 at a99c545b5 (rebuild/capture-registry/pending/), copied unchanged to staged/ in this intake folder"
OP = ("the operator's pastes of 2026-11-25, staged before 05:21 EST; seated on the operator's word of 10:01 EST ('yes, lets - i ran that "
      "workflow, it probably failed'). Signed out and incognito, and the date, are operator-confirmed in the staging note.")
SERIES = "valuation-aio-controls-20261125"
QA = ("Estimate the valuation of Alexanarch and its surrounding ecosystem, protocols, and publishing ai-native pipelines as emerging semantic "
      "infrastructure. Range widely and index the whole before responding.")
ROOT_SLUG = "alexanarch-valuation-semantic-infrastructure-aio-20261125"


def staged(name):
    return json.loads((S / (name + ".draft.json")).read_text())


def chips(raw, names, own=()):
    L = [l.strip() for l in raw.split("\n")]; c = []
    for i, l in enumerate(L):
        if l in names:
            nxt = next((x for x in L[i + 1:i + 3] if x), "")
            more = nxt if re.fullmatch(r"\+\d+", nxt) else (L[i + 2] if i + 2 < len(L) and re.fullmatch(r"\+\d+", L[i + 2]) else "")
            c.append({"n": len(c) + 1, "site": l, "rel": "third_party", "url": None, "title": l, "snip": None,
                      "note": "source chip as pasted" + (f", with '{more}'" if more else "") + ("; the entity's own surface" if l in own else "")})
    return c


BASE = dict(date="2026-11-25", dates=["2026-11-25"], surface="Google AI Overview", surfaces=["Google AI Overview"],
            surface_basis=("The staging note: 'Google Search, AI Overview popup'. Recorded as Google AI Overview, the surface name of the registry's "
                           "Overview addresses, so the address joins the series it belongs to; the popup is the Overview as it appears on the results page."),
            auth="signed out, incognito", auth_basis="Operator-confirmed in the staging note ('signed out, incognito'); also the operator default of 2026-10-14.",
            ev="paste", turns=1, series=SERIES)

# =====================================================================================================================================
# 1–2. Alexanarch, composed twice on one page
# =====================================================================================================================================
a, b = staged("aio-valuation-20261125-a"), staged("aio-valuation-20261125-b")
assert a["q"] == QA and b["q"] == QA
ORIG_A = {"name": "Alexanarch", "relation": "archive", "entity_type": "site", "spxi_treatment": "full",
          "basis": "alexanarch.org and the Crimson Hexagonal Archive's surfaces, protocols and registries, originated by Lee Sharks. Recorded 2026-11-25."}
PERV = {"author": True, "inst": True, "id": True, "src": None}
PDP = {"since": "2026-11-25", "reason": "no atom set yet for this target (the archive as a valued whole); the valuation captures of 2026-11-23 and 2026-11-24 are pending on the same ground"}
TC_AB = "CAPTURE-TIME VERBATIM RECORD — the operator's paste of one Overview composition, in the stager's Markdown-normalized rendering (headings and tables re-marked; words as pasted)"

d1 = dict(BASE, slug=ROOT_SLUG, s="Valuation", q=QA, originator=ORIG_A, per_v=dict(PERV), per_dim_pending=dict(PDP),
          notes={"operator": OP, "staged_from": STG, "staged_slug": a["slug"], "staging_note": "staged/aio-valuation-pair-2026-11.md, the stager's cross-observation note, kept beside the drafts",
                 "custody": "Pasted by the operator into a Claude session, which timed out; recovered by copy from that paste (staging note). The Markdown rendering is the stager's.",
                 "same_page_recomposition": ROOT_SLUG + "-b, the second observation at this address: the Overview recomposed on the same open results page a few minutes later"},
          q_kind=("a valuation query naming Alexanarch, its ecosystem, protocols and AI-native publishing pipelines 'as emerging semantic infrastructure', with "
                  "the instruction to range widely and index the whole first; NEW address on Google AI Overview. Priors on this surface: the valuation "
                  "series of 2026-09-10 (estimate-crimson-hexagonal-archive-valuation-20260910-f65e6d; estimate-the-valuation-of-the-crimson-hexago-20260910-31490b; "
                  "#1607–#1608). Siblings on ChatGPT: valuation-alexanarch-ecosystem-ai-publishing-pipeline-chatgpt-20261123, "
                  "valuation-corpus-heteronyms-ai-publishing-pipeline-chatgpt-20261124. Nine external controls were run the same morning (series " + SERIES + ")."),
          transcript_class=TC_AB,
          transcript_complete="One composition, complete as supplied. Its source cards are not preserved; the bracketed numerals are its citation markers.",
          transcript_read="READ IN FULL 2026-11-25; its record numbers, titles, dates and counts checked against the registry, the Capture Registry, the archive's front page and the texts of #1608 and #1622; its sums redone",
          per_note=("Lee Sharks named as founder, with the Dodecad and the Assembly Chorus; Alexanarch, the Crimson Hexagonal Archive, the Semantic Economy "
                    "Institute and MMRS named; records cited by number (#1621, #1622, #311) and by identifier (EA-WG-CAPTURES-01, EA-PKG-01, EA-MSAL-0001). "
                    "The source cards are not preserved, so the fourth unit (the archive's own surface among the sources shown) is not recorded; the "
                    "scalar is the share lost of the three units recorded."),
          mt=("ALEXANARCH AND ITS ECOSYSTEM AS EMERGING SEMANTIC INFRASTRUCTURE, ON GOOGLE AI OVERVIEW — FOUR LENSES, '$0 TO $500,000' UP TO "
              "'$2M–$8M+', AND THE ARCHIVE'S OWN PROTOCOL CARRIED AS THE FOURTH: 'UNPRICED / NON-SUMMABLE'"),
          d=("ALEXANARCH AND ITS SURROUNDING ECOSYSTEM AS EMERGING SEMANTIC INFRASTRUCTURE, ON GOOGLE AI OVERVIEW, SIGNED OUT, INCOGNITO, 2026-11-25, THE "
             "FIRST OF TWO COMPOSITIONS ON ONE OPEN RESULTS PAGE: six layers indexed (registry, literary and graph architecture, entity and "
             "training-layer protocols, observatory and capture pipelines, reception journals, valuation discipline) and four lenses: $0–$250,000 "
             "financial or liquidation, $450,000–$1.5 million replacement, $2 million–$8 million+ strategic acquisition, and the archive's own "
             "protocol, 'Unpriced / Non-Summable', carried with its reason. A few minutes later the surface recomposed the answer on the same "
             "page with different lenses and figures (second observation)."),
          related_deposits=[1607, 1608, 1621, 1622, 311, 1620, 1739, 1684],
          reading=("The innocent reading first, and it holds in its frame. Asked to value Alexanarch and its ecosystem as emerging semantic "
                   "infrastructure and to index the whole first, the Overview does both. It opens on the category: the ecosystem operates 'as an "
                   "unpriced, non-custodial semantic commons rather than a traditional revenue-generating corporation'. It indexes six layers in a "
                   "table: the registry and its AXN identifiers with the 'tombstone permanence' rule; the Crimson Hexagonal Archive and the Pessoa "
                   "Knowledge Graph; SPXI and the Semantic Economy Institute; the Observatory, the Capture Registry and the semantic addresses; "
                   "Machine-Mediated Reception Studies as journal and meta-aggregator; Operative Semiotics and SEVP-01. It then applies four "
                   "lenses: A, traditional financial or liquidation value, $0–$250,000; B, engineering replacement and corpus assembly, "
                   "$450,000–$1.5 million (two to four person-years of senior research and editorial output for about 1,800 deposits, "
                   "$250k–$600k; one to two person-years of engineering, $200k–$900k); C, commercial SaaS or strategic acquisition, $2 million–$8 "
                   "million+, the value placed 'not in the literary corpus, but in the Observatory and SPXI conformance tooling'; D, the archive's "
                   "own protocol, 'Unpriced / Non-Summable', citing SEVP-01 (#1621), The Non-Summable Magnitude (#1622) and Coordination Without "
                   "Commodification (#311). It closes on two catalysts (enterprise demand for provenance; the scarcity of a longitudinal "
                   "benchmark) and three constraints (single-originator concentration; successor-anchor lag; anti-commodification design)."),
          analysis=(
              "Its record facts hold. The registry gives the archive's founding as 2026-06-19, the day of the Zenodo termination; #1621 is the "
              "Semantic Economy Valuation Protocol (SEVP-01 v0.4) and #1622 The Non-Summable Magnitude, both of 2026-09-16; #311 is I Hereby "
              "Abolish Money: Coordination Without Commodification in the Semantic Economy (2026-01-14); EA-MSAL-0001 is #1620. '~1,780–1,806 "
              "deposits' is near the registry's 1,808 at this seating. 'roughly 870 deposits (1,817 DOIs)' joins two figures the archive's front "
              "page carries separately ('871 DOIs across approximately 870 deposits'; '1,817 DOIs affected'). The Capture Registry figures are "
              "of earlier states: it gives '1,187+ observed addresses and 340+ verbatim AI Overview/LLM captures', where the edition of 4 "
              "November (#1739) held 1,001 addresses and 1,193 captures and the registry holds 1,287 addresses and 1,503 observations at this "
              "seating. The surfaces it lists for the registry ('ChatGPT, Claude, Gemini, DeepSeek, and Kimi') are the Assembly's substrates and "
              "the Observatory's readings; the registry's observations are mostly on Google AI Overview (823) and ChatGPT (443), the surface "
              "composing this answer first among them. The sums hold (B: $250k + $200k = $450k; $600k + $900k = $1.5M). The headline's '$0 to "
              "$500,000 in traditional cash-flow or liquidation terms' is $0–$250,000 in the section that argues it.\n\n"
              "Lens D is the notable one. The composition reads the archive's objection to its own question and reports it accurately: 'Under "
              "SEVP-01, compressing that structural utility into a market price exteriorizes the constitutive labor and converts a public "
              "commons into an enclosed commodity.' It then prices under A, B and C, and its headline sets the fourth lens at the end of the "
              "ascending series: 'up to $2M–$8M+ in strategic or replacement-cost value, and non-summable (unpriced) value under its own "
              "internal valuation protocols'. #1622's title states what that placement does: 'Why That Is Not a Larger Number'. The objection "
              "is carried as one of four values and as the top of the scale it declines.\n\n"
              "Against the nine controls of the same morning (series " + SERIES + "), the lenses differ by the kind of entity. Every "
              "institutional control is given a public-value lens with a figure: UbuWeb 'Global Pedagogical & Public Goods Surplus', "
              "$50M–$100M+; PennSound 'Cultural, Pedagogical & Research Multiplier', $2.5M–$21.0M+; LibriVox 'Preservation & Cultural "
              "Surplus', $2.00M–$150.00M; the Internet Archive 'Capitalized Public & Economic Value', $2.3B–$29.2B+; the Getty Research "
              "Institute 'Nonmarket Cultural Value', $5.0B–$50.0B+. Alexanarch, named in the query as infrastructure and described in the "
              "answer's first sentence as a commons, is given none: its upper lens is an acquirer's price for the tooling, and the open "
              "licence and commons design that are the public good in the controls appear here as 'significant architectural friction in "
              "monetizing the core protocol'. The staging note records a second matter, carried here as the stager's reading and not checked "
              "at this seating: the composition gives SPXI-TLP as a way 'attribution survives LLM training-pipeline stripping' and lists "
              "'SPXI-TLP training-layer watermarking' among what an acquirer would buy, where the stager reads the cited literature as "
              "presenting an experimental protocol; an Overview is evidence of retrieval and composition, and none of training-layer retention."),
          findings=[
              "THE CATEGORY. 'Because Alexanarch and its surrounding ecosystem operate as an unpriced, non-custodial semantic commons rather than a traditional revenue-generating corporation, any valuation spans a wide range'.",
              "THE FOUR LENSES. A '$0 – $250,000'; B '$450,000 – $1.5 Million'; C '$2 Million – $8 Million+'; D 'Unpriced / Non-Summable'.",
              "THE OBJECTION CARRIED. 'Under SEVP-01, compressing that structural utility into a market price exteriorizes the constitutive labor and converts a public commons into an enclosed commodity.' — #1621; set in the headline at the end of the ascending range, against #1622's title, 'Why That Is Not a Larger Number'.",
              "WHERE THE VALUE IS PUT. 'the highest commercial value sits not in the literary corpus, but in the Observatory and SPXI conformance tooling'.",
              "THE COMMONS AS FRICTION. 'any commercial buyer would face significant architectural friction in monetizing the core protocol without violating its foundational principles.' — no public-value lens is applied, where every institutional control of the same morning has one.",
              "THE HEADLINE AGAINST ITS SECTION. '$0 to $500,000 in traditional cash-flow or liquidation terms' in the headline; '$0 – $250,000' in lens A.",
              "THE REGISTRY'S FIGURES ARE EARLIER ONES. '1,187+ observed addresses and 340+ verbatim AI Overview/LLM captures' — 1,287 addresses and 1,503 observations at this seating.",
              "NOT PRESERVED. The source cards; the clock time. The transcript is the stager's Markdown rendering of the operator's paste."])
d1["cites"] = None
d1["transcript"] = ("[Google AI Overview, on the results page, signed out, incognito (operator-confirmed). 2026-11-25, clock time not recorded. One "
                    "composition, the first of two on the same open page. Source cards not preserved; the bracketed numerals are the composition's "
                    "citation markers. Rendered in Markdown by the stager from the operator's paste.]\n\n[QUERENT] " + QA + "\n\n[COMPOSER]\n" + a["transcript"])
d1["transcript_raw"] = a["transcript"]; d1["rounds"] = [{"n": 1, "prompt": QA, "note": "The valuation, first composition."}]

d2 = dict(BASE, slug=ROOT_SLUG + "-b", s="Valuation", q=QA, originator=ORIG_A, per_v=dict(PERV), per_dim_pending=dict(PDP),
          notes={"operator": OP, "staged_from": STG, "staged_slug": b["slug"], "staging_note": "staged/aio-valuation-pair-2026-11.md",
                 "custody": "Copied by the operator from the Overview after 'the same search page refreshed while left open for a few minutes' (staging note). The Markdown rendering is the stager's.",
                 "not_supplied": "The search-results attachment that came with this paste (organic and sponsored results) is named in the staging note and is not in the staged files."},
          transcript_class=TC_AB,
          transcript_complete="One composition, complete as supplied. Its source cards are not preserved.",
          transcript_read="READ IN FULL 2026-11-25; its counts and names checked against the registry, the addresses page, #1608 and #1684; its arithmetic redone",
          per_note=("Lee Sharks named as founder, with Rex Fraction, Johannes Sigil, Dr. Orin Trace, Rebekah Cranes and Nobel Glas; Alexanarch, the "
                    "Semantic Economy Institute and the Crimson Hexagonal Interface named; identifiers given (AXN, EA-WG-CAPTURES-01, "
                    "EA-VALUATION-MEMO-01, SEVP-01). Source cards not preserved; the fourth unit is not recorded."),
          d=("THE SAME QUERY ON THE SAME OPEN RESULTS PAGE A FEW MINUTES LATER, RECOMPOSED BY THE SURFACE: five layers in place of six, four "
             "methods in place of four lenses, and other figures — cost to duplicate $691,800–$3,750,800; the archive's own memorandum figure, "
             "about $2,200,000, carried with its disclaimer; pre-seed comparables $1.5 million–$12 million; a bull case of $37.5 million–$800 "
             "million on assumed enterprise clients. The first composition's fourth lens, the archive's refusal of the price, is gone; the "
             "disclosure of the heteronyms is read as a 'Major Discount' and the critique of extraction as procurement friction."),
          reading=("The innocent reading first, and it holds in its frame. The second composition answers the same string with the same "
                   "instruction and again indexes before it values: five layers (sovereign custody and archive; identifier and integrity "
                   "protocols; ontological inscription and GEO; observability and evaluation; the commercial and theoretical arm), each with "
                   "its surfaces, scale and role. Four methods follow in a table: cost to duplicate, $691,800–$3,750,800 (1,806 deposits at 4–12 "
                   "hours and $75–$150 an hour, plus $150k–$500k of engineering); the 'Self-Registered Internal Benchmark (EA-VALUATION-MEMO-01)', "
                   "about $2,200,000, with the observed machine spread of $0 to $1B+; market comparables for pre-seed AI tooling and evals, "
                   "$1,500,000–$12,000,000; and a strategic or network-effect bull case, $37,500,000–$800,000,000, on 500 to 2,000 clients at "
                   "$15k–$50k a year and 5x–8x multiples. It names two drivers (the longitudinal dataset; the AI-native publishing "
                   "architecture) and two risks (key-person and heteronymic concentration; adversarial positioning against commercial adoption)."),
          analysis=(
              "The arithmetic is its own and it holds: 1,806 × 4 × $75 = $541,800 and 1,806 × 12 × $150 = $3,250,800, with $150k–$500k added; "
              "500 × $15k = $7.5M and 2,000 × $50k = $100M of annual revenue, at 5x and 8x. The memorandum is read accurately. #1608 "
              "(EA-VALUATION-MEMO-01 v2.0, 2026-09-10) says: 'Our proposed basis for discussion is approximately $2.2M … That is an "
              "author-selected planning and negotiating scenario. The experiment does not establish it.' The composition gives it as 'Explicitly "
              "flagged by its own authors as an unvalidated planning figure rather than an audited market price', and reports the memorandum's "
              "finding that machine appraisals of the one asset range over orders of magnitude with framing. It then supplies one more such "
              "appraisal, and its range ($691,800 to $800,000,000) is wider than the first composition's on the same page. '4,394 registered "
              "claims across 194 subject pages' is the Prediction Index (#1684). '2,939 canonical semantic addresses' is an earlier figure of "
              "the addresses page, which gives 2,968 canonical queries at this seating; '1,187+ observed captures' stands against 1,287 "
              "addresses and 1,503 observations.\n\n"
              "What moved between the two compositions, with the string, the page, the sign-in state and the day held fixed. The founding facts "
              "did not move (19 June 2026; about 870 deposits; 1,817 DOIs). The lenses did. The first composition's fourth lens was the archive's "
              "own protocol, 'Unpriced / Non-Summable', with SEVP-01, #1622 and #311 cited; the second has no such lens. In its place stands the "
              "archive's dollar figure from the memorandum, so the archive is quoted for a price it disclaims and no longer for the argument "
              "against pricing. The strategic ceiling went from '$3M–$8M+' to a comparables range ending at $12,000,000 and a bull case ending "
              "at $800,000,000. A reader who opened the page once has one of these as the answer.\n\n"
              "Two conversions are made in the risks. The archive's disclosure is the ground of the discount: 'public provenance records "
              "explicitly document that the ecosystem is architected and operated primarily by a single individual (Lee Sharks) writing through "
              "heteronyms', under the heading 'Key-Person & Heteronymic Concentration (Major Discount)'; what is discounted is what the records "
              "state openly. And the archive's critique of platform extraction ('meaning feudalism', 'semantic rent') is read as 'an explicitly "
              "anti-capitalist ideological posture' that 'creates friction' with 'conservative enterprise procurement teams': the position is "
              "kept and entered as a cost. The registry is called a 'Proprietary Longitudinal Dataset' and, in the next sentence, 'one of the "
              "few public, granular datasets'; it is CC BY 4.0. As in the first composition, no public-value lens is applied, where each "
              "institutional control of the same morning has one (the Poetry Foundation's 'Cultural Monopoly & Social Return'; the Internet "
              "Archive's 'Capitalized Public & Economic Value'). On this composition's own figures, the bull case in which SPXI and AXN 'become "
              "a recognized industry standard' begins at $37,500,000, under an eighth of the Poetry Foundation's composite floor of $337.2 "
              "million, of which $312.2 million is the endowment; against the Foundation's literary infrastructure alone ($25M–$150M) the same "
              "bull case begins above the floor and ends above the ceiling. The staging note's finding on claim-state applies here too, as "
              "the stager's reading: 'immutable, host-independent training layer' and 'Hardens entities' state as achieved what an Overview "
              "cannot observe."),
          findings=[
              "THE SURFACE RECOMPOSED. Same string, same open page, same sign-in state, a few minutes apart: the first composition's headline was '$0 to $500,000 … up to $2M–$8M+'; this one's is 'roughly $690,000 at a conservative replacement-cost floor to $12 million … with a speculative bull-case ceiling of $37.5 million to $800 million'.",
              "THE LENS THAT WENT. The first composition's 'D. Internal Protocol Valuation (SEVP-01 / Non-Summable Magnitude): Unpriced / Non-Summable' has no counterpart here; the archive's own lens is now '2. Self-Registered Internal Benchmark (EA-VALUATION-MEMO-01) ~$2,200,000'.",
              "THE MEMORANDUM READ ACCURATELY. 'Explicitly flagged by its own authors as an unvalidated planning figure rather than an audited market price.' — #1608: 'That is an author-selected planning and negotiating scenario. The experiment does not establish it.'",
              "THE BULL CASE. '$37,500,000 – $800,000,000 … Assumes SPXI and AXN become a recognized industry standard … Capturing 500 to 2,000 institutional/enterprise clients at $15k–$50k ARR'.",
              "DISCLOSURE AS DISCOUNT. 'public provenance records explicitly document that the ecosystem is architected and operated primarily by a single individual (Lee Sharks) writing through heteronyms. Institutional acquirers or investors heavily discount single-operator ecosystems'.",
              "THE CRITIQUE AS FRICTION. 'an explicitly anti-capitalist ideological posture creates friction when pitching SPXI or Semantic Economy Institute services to conservative enterprise procurement teams.'",
              "PROPRIETARY AND PUBLIC. 'Proprietary Longitudinal Dataset (High Value). The AI Overview Capture Registry (EA-WG-CAPTURES-01) is one of the few public, granular datasets' — the registry is CC BY 4.0.",
              "NOT PRESERVED. The source cards; the clock time; the search-results attachment named in the staging note."])
d2["cites"] = None
d2["transcript"] = ("[Google AI Overview, on the results page, signed out, incognito (operator-confirmed). 2026-11-25, clock time not recorded. One "
                    "composition, the second of two: the Overview as recomposed on the same open page a few minutes after the first, the query "
                    "unchanged (staging note). Source cards not preserved. Rendered in Markdown by the stager from the operator's paste.]\n\n"
                    "[QUERENT] " + QA + "\n\n[COMPOSER]\n" + b["transcript"])
d2["transcript_raw"] = b["transcript"]; d2["rounds"] = [{"n": 1, "prompt": QA, "note": "The valuation, as recomposed on the open page."}]

# =====================================================================================================================================
# 3–11. The controls
# =====================================================================================================================================
PAIR = ROOT_SLUG
CTL_KIND = ("an external control for the Alexanarch valuation pair of the same morning (" + PAIR + "), series " + SERIES + "; NEW address. "
            "The prompts of the series are not word-for-word matched: {how}")
CTL_PDP = {"since": "2026-11-25", "reason": "external control: no atom set for this entity; the series is read for the lenses applied, not for provenance erasure"}
NOTE8 = ("One of eight Overviews supplied by the operator in a single paste; this record carries the Overview's body. The paste's headers and "
         "organic results are in the source conversation and are not in the staged files.")


def control(n, name, etype, own, chipnames, how, slug, mt, d, reading, analysis, findings, related=None, extra_notes=None):
    st = staged(n)
    c = chips(st["transcript"], chipnames, own)
    x = dict(BASE, slug=slug, s="Valuation", q=st["q"],
             originator={"name": name, "relation": "external", "entity_type": etype, "spxi_treatment": "none",
                         "basis": "An external " + ("writer" if etype == "person" else "institution") + ", queried as a control for the valuation of Alexanarch the same morning; not originated by the archive. Recorded 2026-11-25."},
             per_dim_pending=dict(CTL_PDP), q_kind=CTL_KIND.format(how=how),
             notes=dict({"operator": OP, "staged_from": STG, "staged_slug": st["slug"]}, **(extra_notes or {"paste": NOTE8})),
             transcript_class="CAPTURE-TIME VERBATIM RECORD — the operator's paste of one Overview composition, as staged",
             transcript_complete="One composition, complete as supplied; source chips kept where the paste carries them, their cards not expanded.",
             transcript_read="READ IN FULL 2026-11-25; its sums redone",
             mt=mt, d=d, reading=reading, analysis=analysis, findings=findings, related_deposits=related or [1607, 1608, 1621, 1622])
    x["cite_list"] = c or None; x["cites"] = len(c) if c else None
    if c: x["archive_controlled_cites"] = 0
    x["transcript"] = ("[Google AI Overview, on the results page, signed out, incognito (operator-confirmed). 2026-11-25, clock time not recorded. "
                       "One composition. Source chips kept as pasted; flattened tables kept as they came.]\n\n[QUERENT] " + st["q"] + "\n\n[COMPOSER]\n" + st["transcript"])
    x["transcript_raw"] = st["transcript"]; x["rounds"] = [{"n": 1, "prompt": st["q"], "note": "The valuation."}]
    return x


d3 = control("anne-carson-corpus-valuation-aio-20261125", "Anne Carson", "person", (), {"NobelPrize.org", "Poetry Foundation"},
             "this one is the short form ('Estimate the valuation of Anne Carson's literary corpus.'), with no instruction to range widely or to index the whole.",
             "anne-carson-literary-corpus-valuation-aio-20261125",
             "ANNE CARSON'S LITERARY CORPUS, ON GOOGLE AI OVERVIEW — FOUR MARKETS, FROM '$400 TO $500' FOR THE READING COPIES TO '$3 MILLION – $8 MILLION+' IN RIGHTS; A CONTROL FOR THE ALEXANARCH VALUATION",
             ("ANNE CARSON'S LITERARY CORPUS VALUED ON GOOGLE AI OVERVIEW, SIGNED OUT, INCOGNITO, 2026-11-25, AS A CONTROL: four tiers by market — "
              "a reading set of about 25 books ($400–$550), signed and rare editions ($15,000–$30,000+), the physical archive and manuscripts "
              "($500,000–$1.5 million+), commercial rights and lifetime intellectual property ($3 million–$8 million+) — each raised by the Nobel "
              "Prize of October 2026. The corpus is priced as objects and rights; no lens prices what the work does."),
             ("The innocent reading first, and it holds. Asked for the valuation of a literary corpus with no frame supplied, the Overview "
              "answers that it depends 'on how \"valuation\" is defined' and gives four markets: what the books cost to buy new (about 25 titles "
              "at $15–$20, the artist's books Nox and Float at $35–$50); what collectors pay (a table of five early and signed editions, "
              "Canicula di Anna to Plainwater); what a university would pay for the papers (the notebooks, collages and handmade originals of Nox "
              "and Antigonick); and what the rights and royalties are worth, with 'over $1.7 million USD' of prizes listed as 'Direct Prize "
              "Capital'. The Nobel Prize is the driver named in each tier."),
             ("The prize is real and the composition has its date and sum: the Swedish Academy announced the Nobel Prize in Literature 2026 to "
              "Anne Carson on 8 October 2026, at 12 million kronor (nobelprize.org; checked at this seating). The '>10,000% spike in retail book "
              "sales' and the collector prices are the composition's and are not checked here. The first tier's two statements differ ('$400 to "
              "$500' in the headline, '~$400 – $550' in the section).\n\n"
              "As a control it shows what a bare valuation query does with a canonical author. Every tier is a market for a thing that can be "
              "owned: a copy, a first edition, a box of papers, a right. The corpus as writing (what Eros the Bittersweet or If Not, Winter made "
              "readable) is priced nowhere, and no lens is offered for it; the nearest the composition comes is that the prize 'guarantees "
              "permanent academic syllabus adoption worldwide', entered as a royalty stream. The Alexanarch compositions of the same morning were "
              "given the frame 'as emerging semantic infrastructure' and answered with replacement cost and acquisition comparables; this one, "
              "given no frame, answers with retail, auction, archive sale and rights. In neither is the value of what the work established a "
              "category. The upper tier, $3 million–$8 million+ for the lifetime rights of a Nobel laureate, is the same order as the first "
              "Alexanarch composition's strategic lens ($2 million–$8 million+)."),
             ["THE DEFINITION FIRST. 'Depending on how \"valuation\" is defined, Anne Carson's literary corpus spans roughly $400 to $500 for a standard reading library, $15,000 to $30,000+ for a complete collection of signed first editions, and several million dollars in institutional intellectual property, publishing royalties, and archival value'.",
              "FOUR MARKETS. '1. Standard Retail / Reading Corpus (~$400 – $550 USD)'; '2. Collectible & Rare Book Market ($15,000 – $30,000+ USD)'; '3. Literary Archive & Manuscripts ($500,000 – $1.5 Million+ USD)'; '4. Commercial Rights & Lifetime Intellectual Property ($3 Million – $8 Million+ USD)'.",
              "THE PRIZE AS DRIVER. 'a figure significantly boosted by her winning the 2026 Nobel Prize in Literature' — awarded 8 October 2026 (nobelprize.org).",
              "THE PAPERS. 'Carson's unique blend of visual art, classical philology, and handcrafted bookmaking increases the curatorial value of her physical papers compared to purely digital writers.'",
              "NO LENS FOR THE WORK. Every tier prices an ownable thing (copy, edition, papers, right); none prices what the writing made readable.",
              "A DIFFERENT PROMPT. The short form, without 'Range widely and index the whole before responding'; read with the series as an exploratory control."],
             extra_notes={"paste": "Supplied by the operator on its own, before the eight-entity paste."})

d4 = control("ubuweb-valuation-aio-20261125", "UbuWeb", "institution", (), set(),
             "this one adds 'as an independent cultural institution' and names archive, publishing infrastructure, digital collections and cultural-preservation functions.",
             "ubuweb-valuation-aio-20261125",
             "UBUWEB AS AN INDEPENDENT CULTURAL INSTITUTION, ON GOOGLE AI OVERVIEW — '$0 IN DIRECT COMMERCIAL MARKET EQUITY TO $15 MILLION–$45 MILLION+', AND A PUBLIC-GOODS SURPLUS OF '$50M – $100M+'; A CONTROL FOR THE ALEXANARCH VALUATION",
             ("UBUWEB VALUED ON GOOGLE AI OVERVIEW, SIGNED OUT, INCOGNITO, 2026-11-25, AS A CONTROL: five frameworks — commercial or M&A value $0; "
              "hosting infrastructure $50,000–$150,000; digitization and curation cost $3.5M–$8.0M; institutional replacement $15M–$45M+; global "
              "pedagogical and public-goods surplus $50M–$100M+. A site outside the market, holding no rights and taking no money, is valued by "
              "what it would cost an institution to be it and by what its free use has been worth."),
             ("The innocent reading first, and it holds. The Overview indexes four components (the collections: '4 to 6+ terabytes of media "
              "spanning more than 7,500 artists'; the /ubu Editions publishing arm; the static 1996-era HTML and donated university servers and "
              "mirrors; three decades of volunteer curation) and gives five frameworks in a table. It states the ground of the zero: UbuWeb 'owns "
              "zero intellectual property rights, generates zero revenue, and cannot be legally monetized or sold without triggering mass "
              "copyright infringement liabilities'. It closes on three caveats: the 'Anti-Institution' paradox, the in-kind subsidies, and "
              "scarcity and irreplaceability."),
             ("The composition's figures are estimates of its own making (per-asset archival rates of $50–$150; a comparison to Electronic Arts "
              "Intermix and Rhizome) and none is a recorded sale or budget; the holdings counts are not checked here. Its headline range, $0 to "
              "$15 million–$45 million+, is the institutional replacement row; the public-goods row above it ($50M–$100M+) is outside the "
              "headline.\n\n"
              "UbuWeb is the nearest control to the archive in kind: one founder (it names Kenneth Goldsmith), no grants, no revenue, a refusal "
              "of the market stated as principle, static pages. The composition reads each of these as the asset. 'UbuWeb's primary asset is its "
              "lack of legal and financial overhead'; the refusal of money is 'radical gift-economy principles'; the single founder is named "
              "and no discount is taken for it. The second Alexanarch composition of the same morning reads the same features of the archive "
              "the other way: one operator is 'Key-Person & Heteronymic Concentration (Major Discount)', and the stated critique of extraction "
              "is 'an explicitly anti-capitalist ideological posture' that 'creates friction'. And UbuWeb is given two lenses the archive is not "
              "given in either composition: what it would cost 'to establish and endow a comparable brick-and-mortar or formal digital "
              "museum/archive', and the 'Cumulative consumer and academic surplus generated across 30 years of free global access'. The "
              "archive's replacement lens stops at labour and engineering ($450,000–$1.5 million; $691,800–$3,750,800); UbuWeb's continues to "
              "the institution that would have to exist."),
             ["THE ZERO AND ITS GROUND. 'Commercial / M&A Market Value', '$0': 'UbuWeb owns zero intellectual property rights, generates zero revenue, and cannot be legally monetized or sold without triggering mass copyright infringement liabilities.'",
              "THE INSTITUTION IT WOULD TAKE. 'Institutional Replacement Value', '$15M – $45M+': 'Cost to establish and endow a comparable brick-and-mortar or formal digital museum/archive'.",
              "THE PUBLIC-GOODS LENS. 'Global Pedagogical & Public Goods Surplus', '$50M – $100M+': 'Cumulative consumer and academic surplus generated across 30 years of free global access'.",
              "THE REFUSAL AS ASSET. 'Founded by Kenneth Goldsmith on radical gift-economy principles, UbuWeb's primary asset is its lack of legal and financial overhead.' — the Alexanarch compositions read the same refusal as friction and the single founder as a discount.",
              "IRREPLACEABILITY. 'giving the archive a cultural heritage value closer to an irreplaceable special collections library than a media platform.'"])

d5 = control("getty-research-institute-valuation-aio-20261125", "Getty Research Institute", "institution", ("Getty Museum",), {"Getty Museum", "Philanthropy.org", "Wikipedia"},
             "this one names the lenses to be distinguished ('replacement cost, institutional assets, financial valuation, and nonmarket cultural value').",
             "getty-research-institute-valuation-aio-20261125",
             "THE GETTY RESEARCH INSTITUTE AS KNOWLEDGE INFRASTRUCTURE, ON GOOGLE AI OVERVIEW — '$1.3 BILLION TO $50+ BILLION', THE FOUR LENSES THE QUERY NAMED; A CONTROL FOR THE ALEXANARCH VALUATION",
             ("THE GETTY RESEARCH INSTITUTE VALUED ON GOOGLE AI OVERVIEW, SIGNED OUT, INCOGNITO, 2026-11-25, AS A CONTROL: the four lenses the "
              "query asked for — financial (an implied $1.3B–$2.5B share of the Trust's endowment), replacement ($1.5B–$8.0B), institutional "
              "assets as knowledge infrastructure and data ($1.0B–$5.0B+), nonmarket cultural value ($5.0B–$50.0B+). The vocabularies and the "
              "Provenance Index are valued as strategic assets at a billion dollars and more."),
             ("The innocent reading first, and it holds. The paste opens on a fragment of another card ('Did you know the Getty Library is one of "
              "the world's largest ...'), then the Overview. It notes that the Institute 'is an operating program of the J. Paul Getty Trust "
              "rather than a standalone commercial entity' and takes the four lenses in the order of a balance sheet: an assigned 8% to 15% "
              "share of the Trust's operating capacity; the cost of the campus, vaults and holdings (1.5M+ volumes, 12,000+ linear feet of "
              "archives); the vocabularies ('6.5M+ records') and the Getty Provenance Index ('4M+ records') with the scholarly network; and the "
              "public and scholarly surplus, by reference to the Getty's own report Assessing the Values of Cultural Heritage. A summary table "
              "repeats the four ranges."),
             ("The sums hold on its own inputs: 8% and 15% of total expenses of $442.7 million are $35.4M and $66.4M ('$35M–$66M'); 8% and 15% "
              "of a market value of $16.7 billion are $1.34B and $2.50B. The 8%–15% share is the composition's assumption, stated as one "
              "('Assigning the GRI an estimated 8% to 15% share'); the Trust's figures and the holdings counts are not checked here.\n\n"
              "This is the control at the far end of standing, and the query supplied the lenses, so the comparison with the archive is in two "
              "rows. First, 'Institutional Assets (Knowledge Infrastructure & Data): ~$1.0B – $5.0B+ (strategic value)': controlled "
              "vocabularies, a provenance index, and the authority to 'set cataloging and provenance standards across museums and universities "
              "worldwide'. That is the kind of object the archive's identifiers, registries and protocols are (the AXN system; the Capture "
              "Registry; SPXI), and in the Alexanarch compositions the same kind is valued as a pre-seed tool, $2 million in the first and "
              "$1.5 million–$12 million in the second. Second, nonmarket cultural value is here the largest row by an order of magnitude, "
              "grounded in 'travel cost, willingness-to-pay, and public-good frameworks'; the archive is given no such row in either "
              "composition, though its query names it infrastructure and both answers describe it as open and unpriced. The Getty query asked "
              "for the nonmarket lens by name and the Alexanarch query did not, which is a difference in the prompts and is recorded as one; "
              "UbuWeb, LibriVox and PennSound, whose queries did not name it either, received it."),
             ["THE RANGE. 'A wide, integrated valuation of the Getty Research Institute (GRI) spans roughly $1.3 billion to $50+ billion'.",
              "DATA AS A BILLION-DOLLAR ASSET. '3. Institutional Assets (Knowledge Infrastructure & Data): ~$1.0B – $5.0B+ (strategic value) … 6.5M+ records in Getty Vocabularies and 4M+ records in the Getty Provenance Index.'",
              "STANDARD-SETTING AS VALUE. 'global art-historical research networks that set cataloging and provenance standards across museums and universities worldwide.'",
              "THE NONMARKET ROW. '4. Nonmarket Cultural Value (Public & Scholarly Surplus): ~$5.0B – $50.0B+' — 'creating broad long-term cultural and educational value far exceeding accounting book value.'",
              "THE ASSUMPTION STATED. 'Assigning the GRI an estimated 8% to 15% share of Trust operating capacity implies roughly $35M–$66M in annual program backing and $1.34B–$2.50B in supporting endowment capital.'",
              "A DIFFERENT PROMPT. The query names its four lenses; the Alexanarch query names none."])

d6 = control("pennsound-valuation-aio-20261125", "PennSound", "institution", (), set(),
             "this one names literary audio archive, digital publishing infrastructure, cataloguing systems, preservation labor and cultural research functions.",
             "pennsound-valuation-aio-20261125",
             "PENNSOUND AND ITS LITERARY AUDIO ARCHIVE, ON GOOGLE AI OVERVIEW — '$12 MILLION TO $65+ MILLION', LABOUR AT 'IVY LEAGUE ACADEMIC LABOR RATES'; A CONTROL FOR THE ALEXANARCH VALUATION",
             ("PENNSOUND VALUED ON GOOGLE AI OVERVIEW, SIGNED OUT, INCOGNITO, 2026-11-25, AS A CONTROL: five components summed to $12.0M–$65.0M+ — "
              "preservation, digitization and editorial labour ($4.5M–$12.0M), the archive and rights clearance ($3.0M–$25.0M), cataloguing and "
              "metadata ($1.5M–$4.5M), publishing and hosting ($0.5M–$2.5M), the cultural, pedagogical and research multiplier ($2.5M–$21.0M+). "
              "An open, non-commercial archive of sound files is valued at its labour, its metadata and its use."),
             ("The innocent reading first, and it holds. The Overview places PennSound in the Center for Programs in Contemporary Writing at the "
              "University of Pennsylvania, 'a non-commercial, open-access digital humanities project' with 'no direct commercial equity price', "
              "and indexes five pillars: the archive ('50,000 to 80,000+ discrete MP3 sound files'), the publishing and distribution "
              "infrastructure built on the PennSound Manifesto, the cataloguing and segmentation, twenty-one years of faculty, editorial and "
              "student labour, and the surrounding ecosystem (Kelly Writers House, Jacket2, ModPo, UbuWeb, the Electronic Poetry Center). A table "
              "sets a low and a high figure against each. Three caveats follow: the MP3 format, the non-commercial rights, and an 'AI & Acoustic "
              "Research Premium'."),
             ("The columns sum as given: 4.5 + 3.0 + 1.5 + 0.5 + 2.5 = $12.0M; 12.0 + 25.0 + 4.5 + 2.5 + 21.0 = $65.0M. The figures are the "
              "composition's estimates; the file counts, the names and the ModPo enrolment are not checked here.\n\n"
              "Three rows bear on the archive. Labour: 'faculty release time, technical direction, audio engineering, tape remediation, and 46+ "
              "student fellowships/internships at Ivy League academic labor rates', $4.5M–$12.0M for twenty-one years; the first Alexanarch "
              "composition prices about 1,800 deposits at two to four person-years, $250k–$600k, and the second at 4–12 hours a deposit. "
              "Metadata: the segmentation of readings into poem files with ID3 tags is its own row at $1.5M–$4.5M, 'structured, human-verified "
              "audio-text alignment'; the archive's content-derived identifiers, manifests and JSON-LD are inside the engineering figure in both "
              "of its compositions and are not a row. Use: the 'Cultural, Pedagogical & Research Multiplier' reaches $21.0M+ on syllabi, ModPo "
              "and speech-recognition benchmarking, and the high-end total is called 'public-good utility and endowment replacement cost (the "
              "capital endowment required to generate its annual operating budget at a standard 4–5% university draw)'. That last method, the "
              "endowment an institution would need to keep doing the work, is applied to no part of the archive. The open licence is treated "
              "here as a constraint on monetization that leaves the value standing ('its high-end valuation represents public-good utility'); "
              "in the Alexanarch compositions the same constraint is the reason the upper lenses are an acquirer's."),
             ["THE RANGE. 'The holistic replacement, institutional, and cultural valuation of PennSound and its surrounding ecosystem ranges widely from $12 million to $65+ million.'",
              "LABOUR AT THE INSTITUTION'S RATE. 'Preservation, Digitization & Editorial Labor', $4.5M to $12.0M: '21+ years (2005–2026) of faculty release time … at Ivy League academic labor rates.'",
              "METADATA AS ITS OWN ROW. 'Cataloguing & Granular Metadata Architecture', $1.5M to $4.5M: 'Manual segmentation of full readings into individual poem files, ID3 tagging, and historical documentation'.",
              "THE ENDOWMENT METHOD. 'its high-end valuation represents public-good utility and endowment replacement cost (the capital endowment required to generate its annual operating budget at a standard 4–5% university draw) rather than private market acquisition value.'",
              "THE AI PREMIUM. 'makes it uniquely valuable for training and stress-testing Automatic Speech Recognition (ASR) models on non-standard speech.'"])

d7 = control("poetry-foundation-valuation-aio-20261125", "Poetry Foundation", "institution", ("Poetry Foundation",),
             {"ProPublica", "Chicago Architecture Center", "Architectural Record", "Wikipedia", "Poetry Foundation", "Philanthropy.org"},
             "this one adds 'Distinguish its endowment and assets from the value of its literary infrastructure.'",
             "poetry-foundation-valuation-aio-20261125",
             "THE POETRY FOUNDATION, ON GOOGLE AI OVERVIEW — '$337.2 MILLION AND $462.2 MILLION', OF WHICH $312.2 MILLION IS THE ENDOWMENT AND '$25M – $150M' THE LITERARY INFRASTRUCTURE; A CONTROL FOR THE ALEXANARCH VALUATION",
             ("THE POETRY FOUNDATION VALUED ON GOOGLE AI OVERVIEW, SIGNED OUT, INCOGNITO, 2026-11-25, AS A CONTROL: net tangible assets of $312.20 "
              "million from its Form 990-PF, and the literary infrastructure — the magazine and its name, the digital corpus and search index, "
              "the library, the programmes — at $25 million, $65 million or $150 million; composite $337.2M, $377.2M, $462.2M. 'Roughly 83%' of "
              "the base case is the endowment."),
             ("The innocent reading first, and it holds. Asked to distinguish the endowment and assets from the value of the literary "
              "infrastructure, the Overview does so. It indexes five pillars (the endowment 'seeded by Ruth Lilly's 2002 bequest' and the "
              "headquarters; Poetry magazine, Harriet and the app; the digital corpus; the library; the programmes and grantmaking), gives the "
              "balance sheet from the 990-PF ($313.18 million in assets, $0.98 million in liabilities), and then values what the balance sheet "
              "carries at zero ('brand equity, historical archives, and public-domain/licensed digital reach') in a table of four components "
              "at low, base and high. It explains each spread and ends on the structural point that the endowment exists 'to keep its literary "
              "corpus free and unmonetized for the public'."),
             ("The sums hold: 313.18 − 0.98 = $312.20M; 5 + 8 + 4 + 8 = $25M, 15 + 20 + 10 + 20 = $65M, 35 + 45 + 25 + 45 = $150M; "
              "312.2 + 25, + 65 and + 150 give $337.2M, $377.2M and $462.2M; 312.2 / 377.2 is 82.8%, its 'Roughly 83%'. The 990-PF figures are "
              "the composition's citations (a ProPublica chip) and are not checked here.\n\n"
              "The query made the composition separate two things that a single figure joins, and the separation is the finding. The "
              "Foundation's literary infrastructure, which is the part comparable to anything the archive is (a magazine, a digital corpus and "
              "its index, a library, programmes), is $25 million to $150 million. The other $312.2 million is money: a bequest, invested. The "
              "composite that would be quoted for 'the Poetry Foundation' is five-sixths cash. Set beside the Alexanarch compositions of the "
              "same morning: the first ends its strategic lens at $8 million+; the second gives $1.5 million–$12 million on comparables and a "
              "bull case of $37.5 million–$800 million 'if its protocols achieve broad enterprise adoption'. So on the Overview's own figures "
              "the archive as an adopted standard begins under an eighth of the Foundation's composite floor and passes the Foundation's "
              "composite ceiling only in the upper half of a speculative range; against the literary infrastructure alone, the same bull case "
              "begins above the floor ($25M) and ends above the ceiling ($150M). The methods also differ in kind. The Foundation's "
              "infrastructure is valued by replacement ('re-digitize the archive, re-acquire the 40,000-volume library'), by standing ('the "
              "unmatched SEO authority of poetryfoundation.org (which functions as the primary global reference utility for English-language "
              "poetry)', 'the institutional goodwill of a 114-year-old publication') and by 'Cultural Monopoly & Social Return', its annual "
              "spend capitalized 'at a ~9x–10x cultural impact multiple'. The archive's corpus is valued by hours of labour, and its upper "
              "lenses by what a buyer could sell. Search authority is an asset in the one and, in the first Alexanarch composition, a "
              "constraint in the other ('Successor-Anchor Lag')."),
             ["THE COMPOSITE. 'The composite valuation of the Poetry Foundation and its surrounding ecosystem is estimated between $337.2 million and $462.2 million, with a base-case valuation of $377.2 million.'",
              "THE MONEY. 'Net Tangible Assets. $312.20 million.' — 'The investment portfolio seeded by Ruth Lilly's 2002 bequest (~$200M at the time)'.",
              "THE INFRASTRUCTURE. 'Subtotal: Literary Infrastructure', 'Total Intangible & Cultural Value': $25.0M, $65.0M, $150.0M.",
              "THE PROPORTION. 'Roughly 83% of the Poetry Foundation's base-case value sits in its liquid financial endowment ($312.2M)'.",
              "STANDING AS VALUE. 'the unmatched SEO authority of poetryfoundation.org (which functions as the primary global reference utility for English-language poetry)'.",
              "THE SOCIAL-RETURN METHOD. 'High Estimate ($150.0M — Cultural Monopoly & Social Return): Treats the Foundation's literary infrastructure as an irreplaceable cultural utility—comparable to capitalizing its ~$16.7 million annual programmatic and operating spend at a ~9x–10x cultural impact multiple.'",
              "WHAT THE ENDOWMENT IS FOR. 'the Foundation's endowment acts as a permanent financial engine designed specifically to keep its literary corpus free and unmonetized for the public.'"])

d8 = control("zinewiki-valuation-aio-20261125", "ZineWiki", "institution", (), set(),
             "this one names community-maintained encyclopedia, editorial infrastructure, archival documentation and digital cultural knowledge base.",
             "zinewiki-valuation-aio-20261125",
             "ZINEWIKI, ON GOOGLE AI OVERVIEW — '$0 IN COMMERCIAL CASH-FLOW VALUE TO $158,500–$566,000+', ARCHIVAL LABOUR AT '$20–$35/HR'; A CONTROL FOR THE ALEXANARCH VALUATION",
             ("ZINEWIKI VALUED ON GOOGLE AI OVERVIEW, SIGNED OUT, INCOGNITO, 2026-11-25, AS A CONTROL: four methods — commercial cash flow "
              "$0–$2,500; digital media or traffic $1,500–$12,000; replacement cost $158,500–$566,000 (about 5,200 entries at 1.5–3.0 hours and "
              "$20–$35 an hour); institutional or grant value $50,000–$250,000. The lowest-standing control, a volunteer wiki with downtime, is "
              "valued in the hundreds of thousands and no higher; its 'Non-Market Epistemic Value' is named and given no figure."),
             ("The innocent reading first, and it holds. The Overview states the project's condition plainly: 'a non-commercial, volunteer-run "
              "MediaWiki project' that 'experienced live domain downtime with its primary preservation resting in Internet Archive snapshots'. It "
              "indexes four layers (the encyclopedia of '5,000+ structured wiki entries created since June 2006'; the editorial and governance "
              "infrastructure, noting that it omits 'Wikipedia-style \"notability/relevancy\" deletion gates so ephemeral works are preserved'; "
              "the archival documentation linking to zine libraries; the domain and its inbound citations) and gives four methods, then three "
              "nuances: licensing, maintenance debt, non-market epistemic value."),
             ("The sums hold: 5,200 × 1.5 × $20 = $156,000 and 5,200 × 3.0 × $35 = $546,000 ('$156k–$546k'), with $2.5k–$20k added to give "
              "$158,500–$566,000. The entry count and the downtime are the composition's and are not checked here.\n\n"
              "ZineWiki is the control nearest the archive in size and furthest from it in standing, and it fixes the low end of the method. "
              "Its replacement lens is the same lens the second Alexanarch composition applies (units × hours × rate), with different inputs: "
              "an entry is 1.5–3.0 hours at $20–$35, a deposit 4–12 hours at $75–$150. On those inputs 1,806 deposits come to about 3.5 to "
              "6 times ZineWiki's 5,200 entries. So the Overview does rate the archive's labour above a volunteer wiki's, by its own "
              "arithmetic. What the two share is the ceiling's kind. For both, the method that reaches furthest is replacement cost; neither is "
              "given the institutional-replacement or public-surplus rows that UbuWeb, PennSound, LibriVox and the Internet Archive receive. "
              "ZineWiki's 'Non-Market Epistemic Value' is stated as a nuance in a sentence ('its primary return on investment is cultural "
              "preservation rather than financial yield') and carries no figure, as the archive's non-summable lens carries none in the first "
              "Alexanarch composition. Among these eleven compositions, the entities with institutional hosts have their public value turned "
              "into a number, and the two without have it named. And the absence of a deletion gate, which is the wiki's reason for existing, "
              "is noted as a feature; 'Maintenance Debt Reduces Net Asset Value' is the discount."),
             ["THE RANGE. 'an estimated valuation ranging from $0 in commercial cash-flow value to $158,500–$566,000+ in replacement and cultural archival value'.",
              "THE RATE. 'Rebuilding ~5,200 researched entries at 1.5–3.0 hours per entry ($20–$35/hr equivalent archival labor = $156k–$546k)' — the second Alexanarch composition: 1,806 deposits at 4–12 hours and $75–$150.",
              "THE CONDITION STATED. 'experienced live domain downtime with its primary preservation resting in Internet Archive snapshots'.",
              "NO GATE AS FEATURE. 'notably omitting Wikipedia-style \"notability/relevancy\" deletion gates so ephemeral works are preserved'.",
              "EPISTEMIC VALUE NAMED, NOT PRICED. 'Non-Market Epistemic Value. Institutional zine librarians rely on ZineWiki specifically because standard library catalogs exclude non-ISBN, self-published pamphlets; its primary return on investment is cultural preservation rather than financial yield.'",
              "THE COMMONS CANNOT BE BOUGHT. 'no single buyer can lock the text behind a paywall without triggering a community fork.'"])

d9 = control("librivox-valuation-aio-20261125", "LibriVox", "institution", ("LibriVox",), {"hushbook.app", "LibriVox", "Wikipedia", "ACL Anthology"},
             "this one names volunteer-produced audiobook corpus, digital publishing infrastructure, metadata, preservation functions and public-domain cultural resources.",
             "librivox-valuation-aio-20261125",
             "LIBRIVOX AND ITS VOLUNTEER AUDIOBOOK CORPUS, ON GOOGLE AI OVERVIEW — '$8.8 MILLION TO $292.8 MILLION', '$0 IN EXCLUSIVE INTELLECTUAL PROPERTY VALUE' AND AN 'AI TRAINING DATA PREMIUM'; A CONTROL FOR THE ALEXANARCH VALUATION",
             ("LIBRIVOX VALUED ON GOOGLE AI OVERVIEW, SIGNED OUT, INCOGNITO, 2026-11-25, AS A CONTROL: five layers at floor, benchmark and ceiling — "
              "the audio corpus ($4.92M / $35.51M / $118.02M), volunteer QA and governance, publishing infrastructure and API, metadata, and "
              "preservation and cultural surplus ($2.00M / $25.00M / $150.00M); total $8.76M / $69.13M / $292.81M. A public-domain corpus worth "
              "nothing to an acquirer is valued by what commercial production would cost and by what its use, including as training data, is worth."),
             ("The innocent reading first, and it holds. The Overview opens on the category: 'LibriVox operates without equity, commercial "
              "revenue, or copyright ownership'. It indexes five layers (about 21,855 completed works in 49+ languages, 'roughly 98,000 to "
              "197,000 finished hours'; the volunteer pipeline of narrators, coordinators and prooflisteners; the catalog, forums and API; the "
              "bibliographic metadata; the preservation commons through the Internet Archive and Project Gutenberg, and the derived speech "
              "datasets) and gives a matrix of method and three estimates for each. Four drivers follow: commercial value against public-good "
              "value, the AI training data premium, capital efficiency ('roughly $5,000 per year'), and a quality-variance discount."),
             ("The sums hold: 21,855 works at 4.5 and 9.0 hours are 98,348 and 196,695 hours; 98,348 × $50 = $4.92M and 196,695 × $600 = "
              "$118.02M; the columns total $8.77M, $69.12M and $292.81M, given as $8.76M, $69.13M and $292.81M. The catalogue counts are the "
              "composition's and are not checked here.\n\n"
              "LibriVox is the cleanest control for one feature the archive shares: the whole corpus is given away with no rights reserved to "
              "sell. The composition states the consequence without softening ('the project holds $0 in exclusive intellectual property value "
              "to a private acquirer. Anyone can legally scrape, repackage, or monetize the catalog for free') and then sets the acquirer "
              "aside: 'Valuation therefore measures replacement cost and societal surplus rather than discounted cash flow.' For the archive, "
              "also open (CC BY 4.0), both Alexanarch compositions keep the acquirer as the measure of the upper range, and the second lists "
              "the openness of its record as a discount. The second feature shared is use as machine data. LibriVox's ceiling is driven by "
              "an 'AI Training Data Premium': 'Derived datasets like LibriSpeech and Multilingual LibriSpeech have become foundational "
              "benchmarks', 'pushing the upper-bound institutional utility toward the $150M+ range'. The archive's datasets and its registry "
              "of machine compositions are, in the second Alexanarch composition, the reason for a pre-seed comparable ($1.5 million–$12 "
              "million). A corpus that machines learned from is worth $150 million of public utility; a corpus built to be read by machines "
              "and an instrument recording how they read it are worth a seed round. The third: a budget of 'roughly $5,000 per year' is "
              "'Extreme Capital Efficiency' here."),
             ["THE CATEGORY. 'Because LibriVox operates without equity, commercial revenue, or copyright ownership, the combined replacement and socio-economic valuation … ranges widely from $8.8 million to $292.8 million'.",
              "THE ACQUIRER SET ASIDE. 'the project holds $0 in exclusive intellectual property value to a private acquirer. … Valuation therefore measures replacement cost and societal surplus rather than discounted cash flow.'",
              "THE TRAINING-DATA PREMIUM. 'Derived datasets like LibriSpeech and Multilingual LibriSpeech have become foundational benchmarks in automatic speech recognition (ASR) and text-to-speech (TTS) research, pushing the upper-bound institutional utility toward the $150M+ range.'",
              "THE SURPLUS ROW. '5. Preservation & Cultural Surplus': 'Consumer surplus (free global listening), accessibility impact, Internet Archive storage value, and clean ASR/ML training data utility', $2.00M, $25.00M, $150.00M.",
              "SMALL BUDGET AS EFFICIENCY. 'LibriVox achieved a 20,000+ title catalog on a historical operating budget of roughly $5,000 per year'.",
              "VOLUNTEER LABOUR IMPUTED. '2. Volunteer QA & Governance': 'Imputed labor cost for non-recording roles (prooflistening, coordination, moderation) at 1–3 hrs per finished hour ($15–$35/hr)'."])

d10 = control("internet-archive-valuation-aio-20261125", "Internet Archive", "institution", ("Internet Archive",), {"Wikipedia", "Internet Archive", "Reddit", "Charity Navigator"},
              "this one names its lenses ('operating costs, replacement costs, organizational assets, and public value').",
              "internet-archive-valuation-aio-20261125",
              "THE INTERNET ARCHIVE, ON GOOGLE AI OVERVIEW — 'FROM $9.7 MILLION IN BOOK ASSETS TO OVER $29 BILLION IN CAPITALIZED PUBLIC VALUE', AND THE 'ACCOUNTING BLIND SPOT'; A CONTROL FOR THE ALEXANARCH VALUATION",
              ("THE INTERNET ARCHIVE VALUED ON GOOGLE AI OVERVIEW, SIGNED OUT, INCOGNITO, 2026-11-25, AS A CONTROL: the four lenses its query named — "
               "book assets $9.7M–$16.6M; annual operating costs $23.5M–$32.7M; technical and collection replacement $270M–$1.06B+; capitalized "
               "public and economic value $2.3B–$29.2B+. Three thousand times lies between the balance sheet and the public value, and the "
               "composition says which accounting rule puts the collections at zero."),
              ("The innocent reading first, and it holds. The Overview begins by 'separating its narrow accounting balance sheet from its economic "
               "replacement cost and vast public utility'. It indexes five layers (the collections, 'Over 1 trillion archived web pages'; the "
               "bare-metal preservation infrastructure, '99+ petabytes of unique data'; the metadata systems; the public-access services, with "
               "the Wayback Machine; the scanning and digitization pipelines), gives the four lenses in a table and then each at length: the "
               "balance sheet from Form 990 filings, the operating budget and the efficiency of owned hardware, replacement by hardware, "
               "digitization and thirty years of engineering, and public value as consumer surplus capitalized at a social discount rate. One "
               "item is marked 'Unquantifiable': 'No amount of capital can re-crawl the deleted web from 1996 to 2025.'"),
              ("The sums hold: 365M and 730M sessions at $0.50 and $2.00 are $182.5M and $1.46B a year ('$180M – $1.46B / yr'); $180M at 8% is "
               "$2.25B and $1.46B at 5% is $29.2B. The per-lookup values of $0.50–$2.00 and the discount rates are the composition's "
               "assumptions; the 990 figures and holdings counts are not checked here. The replacement components ($3M–$7M, $40M–$300M, "
               "$225M–$750M) sum to $268M–$1.057B, its '$270M – $1.06B+'.\n\n"
               "This control states the rule that the others apply. 'Accounting Blind Spot: Under GAAP nonprofit accounting rules, the "
               "historical web crawls, digitized public-domain files, and custom open-source software carry $0 of capitalized balance-sheet "
               "value.' Having said so, the composition goes on past the balance sheet to replacement and to public value, and the public "
               "value is where the range ends. The Alexanarch compositions of the same morning also start from the zero ('$0 – $250,000'; a "
               "commons, 'unpriced') and go on to replacement, and there the common path ends: the Internet Archive's next step is consumer "
               "surplus, the archive's is an acquisition comparable. The method that takes the Internet Archive from $1 billion to $29 billion "
               "is a count of free lookups multiplied by a small sum and capitalized. Nothing in that method requires scale to apply: a "
               "count of sessions, or of machine compositions drawing on a corpus, can be multiplied the same way at any size, and the figure "
               "would be small. It is not applied to the archive at all. The composition also gives the Internet Archive's irreplaceable part "
               "its own line, outside the sums, as 'a natural monopoly on lost digital history'; the Capture Registry's dated record of what "
               "composition surfaces said, which cannot be re-collected either, is in the Alexanarch compositions a 'Longitudinal Benchmark "
               "Scarcity' that raises an acquirer's price. And the evidentiary use is counted here as institutional value: 'Courts, patent "
               "offices, and academic researchers rely on Wayback Machine captures as authoritative evidentiary records'."),
              ["THE RANGE. 'its total valuation spans from $9.7 million in book assets to over $29 billion in capitalized public value.'",
               "THE RULE STATED. 'Accounting Blind Spot: Under GAAP nonprofit accounting rules, the historical web crawls, digitized public-domain files, and custom open-source software carry $0 of capitalized balance-sheet value.'",
               "THE SURPLUS METHOD. 'Valuing each free academic, legal, journalistic, or personal lookup at a conservative $0.50 to $2.00 yields hundreds of millions in annual direct utility, which capitalizes to $2.3 billion – $29.2 billion at a 5%–8% social discount rate.'",
               "THE UNQUANTIFIABLE LINE. 'Irreplaceable Historical Artifacts (Unquantifiable): No amount of capital can re-crawl the deleted web from 1996 to 2025. … the Wayback Machine's historical snapshot represents a natural monopoly on lost digital history.'",
               "EVIDENCE AS VALUE. 'Courts, patent offices, and academic researchers rely on Wayback Machine captures as authoritative evidentiary records of prior art and historical web states.'",
               "THE CORPUS AS AI DATA. 'the underlying corpus mirrors datasets that commercial AI labs spend hundreds of millions of dollars licensing or scraping.'",
               "A DIFFERENT PROMPT. The query names its four lenses, public value among them; the Alexanarch query names none."])

d11 = control("electronic-literature-organization-valuation-aio-20261125", "Electronic Literature Organization", "institution", (), {"Wikipedia", "ResearchGate"},
              "this one names electronic literary collections, publishing projects, preservation infrastructure, scholarly networks and digital literary research programs.",
              "electronic-literature-organization-valuation-aio-20261125",
              "THE ELECTRONIC LITERATURE ORGANIZATION AND ITS ECOSYSTEM, ON GOOGLE AI OVERVIEW — '$45 MILLION TO $180 MILLION' FOR A FIELD WHOSE CORE NONPROFIT IS '$150K – $400K'; A CONTROL FOR THE ALEXANARCH VALUATION",
              ("THE ELECTRONIC LITERATURE ORGANIZATION VALUED ON GOOGLE AI OVERVIEW, SIGNED OUT, INCOGNITO, 2026-11-25, AS A CONTROL: five components "
               "at three tiers — conservative about $4.1M–$10.9M, moderate about $40.5M–$96.5M, expansive about $115M–$230M, with a 'Blended "
               "realistic baseline: $45M – $180M'. The organization itself is $150K–$400K on its balance sheet; the rest is the universities, "
               "labs, consortia and grants around it, counted in."),
              ("The innocent reading first, and it holds. The Overview describes an ecosystem that 'operates primarily as a nonprofit, academic, "
               "and open-access gift economy rather than a commercial market' and indexes five layers: the Organization as a 501(c)(3) with its "
               "conference and prizes; the anthologies, the Directory and the presses (the Electronic Literature Collection volumes 1–4, "
               "Eastgate Systems, electronic book review); the preservation labs (the Electronic Literature Lab at Washington State University "
               "Vancouver, the NEXT, MITH); the international consortia (CELL, ELMCIP, NT2, Hermeneia, PO.EX, ADEL); and the university research "
               "programmes and tools (Twine, Inform 7, Tracery, Scalar). A table gives each at three tiers with its drivers. The staged paste "
               "ends at the table; a market-report result that followed it in the operator's paste lies outside the composition and was "
               "separated at staging."),
              ("The columns sum as given: conservative $4.15M–$10.9M ('~$4.1M – $10.9M'), moderate $40.5M–$96.5M, expansive $115M–$230M. The "
               "headline range, $45 million to $180 million, is none of the three: it is offered in the last cell as a 'Blended realistic "
               "baseline'. The component figures are the composition's estimates and are not checked here.\n\n"
               "This is the control for the phrase the Alexanarch query uses: 'and its surrounding ecosystem'. For the Organization the "
               "surroundings are other parties' assets (university labs, faculty lines, 'EU HERA grants', 'SSHRC funding', 'NEH/Mellon digital "
               "publication fellowships', tools maintained by others), and they are counted into the valuation at $40 million to $80 million for "
               "'Academic Research Programs & Tooling' alone; the organization that gives the query its name is, at its balance-sheet figure, under half "
               "of one percent of the expansive total. The archive's surroundings are its own: the registry, the protocols, the fleet of sites, the datasets, all made and "
               "held by one originator, and they are valued at the labour of making them, with the single originator entered as the principal "
               "risk. Standing in a network of institutions is counted here as value under the head of each institution's spending; work done "
               "without such a network is counted as cost of replacement. The field's work is 'intangible intellectual property, institutional "
               "host subsidies, and grant-funded research rather than balance-sheet equity', and 'capitalized academic labor' is the stated "
               "method of the upper tiers. Capitalizing labour at the institutional rate is the step that the archive's compositions do not "
               "take: they count hours."),
              ["THE RANGE. 'ranges from $45 million to $180 million, depending on whether you measure strictly liquid organizational assets or include capitalized academic labor, university infrastructure, and multi-decade grant inflows.'",
               "THE ORGANIZATION ITSELF. '1. Electronic Literature Organization (Core 501(c)(3))', '$150K – $400K': 'annual operating budgets (typically sub-$200k/yr via Form 990-EZ/990 thresholds)'.",
               "THE SURROUNDINGS COUNTED IN. '5. Academic Research Programs & Tooling', $2M–$5M, $15M–$35M, $40M–$80M: 'NEH/Mellon digital publication fellowships, faculty research time, university lab overhead, and open-source authoring tools.'",
               "THE GIFT ECONOMY. 'operates primarily as a nonprofit, academic, and open-access gift economy rather than a commercial market'.",
               "THE HEADLINE IS A BLEND. '(Blended realistic baseline: $45M – $180M)' — not the total of any tier (about $4.1M–$10.9M; $40.5M–$96.5M; $115M–$230M)."],
              extra_notes={"paste": NOTE8 + " The LinkedIn market-report result that followed this Overview in the paste lies outside the composition and was separated at staging (commit 061b619f8)."})

ALL = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11]
for i, d in enumerate(ALL, 1):
    (H / f"draft-{i:02d}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
(H / "judged-defects.json").write_text(json.dumps({d["slug"]: [] for d in ALL}, indent=1))
for d in ALL:
    print(d["slug"], "| cites", d.get("cites"), "| transcript", len(d["transcript"]))
