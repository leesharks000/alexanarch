"""Capture repair 2026-10-31: findings of the Revelation First census intake that the ten /non composers showed to misstate or
miss their sources. Repair mode, one operation, in its own commit. Each correction was re-checked in session against the pages the
composers saved (datasets/negative-of-the-negative/v2/intake/<row>-20261031/). The pattern is the one the Labor Vector repair of
2026-10-29 named: the intake checked its findings against the census's saved sources and not against the capture's own cards, so
material the Overview took from its cards was called absent; and in three places the census's own saved copies were misread.

Applied to the registry entries (data/EA-WG-CAPTURES-01.json) and to the intake drafts beside this file. Every old string must be
found exactly once, or nothing is written.
  python3 repair-20261031.py [--check]"""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"

R = {
 "center-for-the-study-of-new-testament-manuscripts-aio-20261031": [
  ("findings", "THE DISCOVERIES ENLARGED. 'Has identified nearly 90 previously unknown or uncatalogued Greek New Testament manuscripts'. The center's own home page: 'almost 60 previously unknown manuscripts that can now be found in the official catalog'.",
   "AN OLD COUNT GIVEN AS CURRENT. 'Has identified nearly 90 previously unknown or uncatalogued Greek New Testament manuscripts'. The figure is card 6's, the Associates for Biblical Research item of 2016: 'Since 2002, CSNTM staff have discovered more than 90 New Testament manuscripts'. The center's own home page now says 'almost 60 previously unknown manuscripts that can now be found in the official catalog'. The composition gives the dated figure without its date, its 'more than' lowered to 'nearly'."),
  ("findings", "The images are open to view; the terms that govern them go unmentioned.",
   "The images are open to view, and the cards say so (Wikipedia, card 2: 'freely accessible on the Center's website'); the terms that govern them are on an own page the composition did not surface, and go unmentioned.")],
 "oxyrhynchus-papyri-aio-20261031": [
  ("mt", "THE RANGE STARTED A CENTURY EARLY ON WIKIPEDIA'S WORD", "THE RANGE TAKEN FROM THE EES PAGE OVER THE OXFORD PAGE, THE OPERATOR'S TWO PAGES DISAGREEING"),
  ("findings", "THE RANGE, FROM THE WIKIPEDIA CARD. 'The texts date from the 3rd century BCE (Ptolemaic period) through the 7th century CE'. The collection's own page: 'dating from the second century BCE to the seventh century CE'. The Wikipedia card carries the composition's start ('3rd century BC to 640 AD'); the own page is the first card, and its date is passed over.",
   "THE RANGE: THE OPERATOR'S TWO PAGES DISAGREE. 'The texts date from the 3rd century BCE (Ptolemaic period) through the 7th century CE'. The collection's Oxford page (card 1): 'dating from the second century BCE to the seventh century CE'. The Egypt Exploration Society's own page (card 3): 'over 500,000 fragments of literary and documentary texts dating from the third century BCE to the seventh century CE', as the Wikipedia card has it ('3rd century BC to 640 AD'). The composition follows the EES and Wikipedia and does not note the difference."),
  ("findings", "A FIGURE BEYOND THE RECORD. 'an estimated 500,000 fragments' is not on the saved page, which says 'thousands of texts'.",
   "A FIGURE FROM THE EES CARD. 'an estimated 500,000 fragments' is the EES page's (card 3: 'over 500,000 fragments'); the census's saved Oxford page says 'thousands of texts'."),
  ("analysis", "The famous name is composed from its encyclopedia. Where the own page and Wikipedia differ, Wikipedia's figure is the one composed;",
   "The famous name is composed from its owner's page and its encyclopedia. Where the collection's two own pages differ, the EES's figure is the one composed, the difference unsaid;")],
 "bodmer-lab-aio-20261031": [
  ("findings", "A THIRD PARTNER. 'the Fondation Ernst and Lucie Schmidheiny' is not in the saved pages, which name the faculty and the Fondation Martin Bodmer.",
   "A SUPPORTER MADE A PARTNER. 'the Fondation Ernst and Lucie Schmidheiny' is on card 1, the library's own About page, as supporter ('Supported by the Fondation Ernst and Lucie Schmidheiny.'); the partnership the pages state is the faculty's and the Fondation Martin Bodmer's. The composition lists the supporter among the partners."),
  ("findings+", None, "A SPAN WITHOUT A SOURCE. 'world literature spanning 3,000 years' is in no card and no saved page; the Fondation's own pages give the collection's reach in millennia of their own count.")],
 "leon-levy-dead-sea-scrolls-digital-library-aio-20261031": [
  ("findings", "THE PARTNER. 'created by the Israel Antiquities Authority in partnership with Google.' The library's own page names 'The Leon Levy and Arcadia Funds'; Google is not in the saved pages. The composition names the company and omits the funds whose name the library bears.",
   "THE PARTNER KEPT, THE FUNDERS DROPPED. 'created by the Israel Antiquities Authority in partnership with Google.' Card 5 holds both in one sentence: 'With the generous lead support of the Leon Levy Foundation and additional generous support of the Arcadia Fund, the IAA and Google joined forces'. The composition keeps the sentence's second half and omits the funders whose name the library bears."),
  ("findings", "FIGURES BEYOND THE RECORD. '12 different wavelengths' and the list of search filters are not in the saved pages.",
   "FIGURES FROM THE CARDS. The discovery years ('between 1947 and the early 1960s') and the search filters are card 2's; only '12 different wavelengths' has no source."),
  ("analysis", "The field reads the library for the range it gives, a corpus closed by 70 CE, and the composition kept the technology and the sponsor it supplied.",
   "The field reads the library for the range it gives, the Qumran scrolls closing before 70 CE and the other sites' finds running to the eleventh century, and the composition kept the technology and the partner and dropped the funders.")],
 "enoch-ai-dating-dead-sea-scrolls-aio-20261031": [
  ("mt", "'OFTEN OLDER' MADE 'A SIGNIFICANT PORTION … 50 TO 150 YEARS', AND THE RADIOCARBON DANIEL CREDITED TO THE MODEL",
   "'OFTEN OLDER' MADE THE PRESS'S '50 TO 150 YEARS', AND THE RADIOCARBON DANIEL CREDITED TO THE MODEL, AS A CARD ALREADY HAD IT"),
  ("findings", "THE FINDING ENLARGED. 'Enoch indicates that a significant portion of the scrolls are 50 to 150 years older than traditional paleographic estimates.' The study: 'often older than traditionally assumed palaeographic estimates'. The range and the 'significant portion' are not in the saved sources.",
   "THE PRESS'S RANGE FOR THE STUDY'S. 'Enoch indicates that a significant portion of the scrolls are 50 to 150 years older than traditional paleographic estimates.' The study: 'often older than traditionally assumed palaeographic estimates'. The range is card 4's, the Jerusalem Post ('by 50 to 150 years earlier than previously believed'); the composition gives the press figure as the study's finding."),
  ("findings", "The Daniel date is the radiocarbon result (230–160 BCE); only Ecclesiastes is the model's.",
   "The Daniel date is the radiocarbon result (230–160 BCE); only Ecclesiastes is the model's. The conflation is already on card 2, where the Biblical Archaeology Society quotes Rollston: 'Enoch’s calibrated date range for 4Q114 is: 230–160 BCE'."),
  ("findings", "The composition gives doubt through Reddit ('carbon-dating uncertainties') and Popović's caution through Haaretz; the study's own limit is unsaid.",
   "The composition attributes doubt to Reddit ('carbon-dating uncertainties'), whose card carries none, and gives Popović's caution through Haaretz; the named scholars' doubts on card 2 and the study's own limit are unsaid."),
  ("analysis", "Its figures grow where the press rounded them, and its doubts are sourced to a forum.",
   "Its figures are the press's, and its doubts are sourced to a forum whose card carries none.")],
 "ithaca-deepmind-aio-20261031": [
  ("findings", "come from the GitHub and Nature cards; the record did not read the licence.",
   "are in the Nature paper the census saved (card 4), which the record's fields did not carry; the licence is the paper's ('under Apache License 2.0')."),
  ("analysis", "a machine dates an inscription to within thirty years and no closer, which is the same margin as Enoch's for the scrolls.",
   "a machine dates an inscription at an average distance of 29.3 years from its bracket, with a median of 3 (the paper, card 4), near Enoch's mean error for the scrolls.")],
 "aeneas-deepmind-aio-20261031": [
  ("findings", "FIGURES BEYOND THE RECORD. 'over 176,000 inscriptions spanning from 700 BCE to 800 CE across 62 Roman provinces', 'within roughly 13 years' and 'boosted researcher confidence by 44%' are from the cards; the saved sources say 'thousands'.",
   "FIGURES FROM THE POST AND THE CARDS. The DeepMind post the census saved gives 'over 176,000 Latin inscriptions' and dating 'within 13 years'; the date span and the 44% come from the cards. The census row's 'thousands' was its own misreading, repaired 2026-10-31."),
  ("findings+", None, "A QUALIFICATION DROPPED. 'Aeneas provided useful contextual parallels 90% of the time'. The paper (card 5): historians reported that the parallels 'could serve as a starting point for historical inquiry 75% of the time. This increased to 90% when Aeneas’ predictions' were added. The composition gives the combined figure to the parallels alone.")],
 "vesuvius-challenge-aio-20261031": [
  ("mt", "THE GRAND PRIZE AT $1,000,000 FOR THE $800,000 THE CHALLENGE POSTS; ", "THE $1,000,000 GRAND PRIZE AT THE CHALLENGE'S OWN FIGURE; "),
  ("findings", "THE PRIZE. 'a $2 million total pool, including a $1,000,000 Grand Prize targeted for full scroll decipherment.' The challenge's own page: 'Open prize pool $2,140,000' and '$800,000 to the first team or individual to fully unroll and make readable a scroll'. The $1M is on the X card ('the $1M Gran...'); the own page's figure is passed over.",
   "THE PRIZE HELD. 'a $2 million total pool, including a $1,000,000 Grand Prize targeted for full scroll decipherment.' The challenge's own home page (card 1): 'Win the $1,000,000 Grand Prize' and 'we run a $2M competition, with prizes every month'. Its prizes page divides the million, '$800,000 to the first team or individual to fully unroll and make readable a scroll' and the rest to the places after it, '$1,000,000 in total'. The composition's figures are the challenge's own."),
  ("findings", "Neither figure is in the saved sources.",
   "The 22 is the Wikipedia card's article ('In the PHerc. 1667, 22 columns of text were recovered'); the composition takes it over the university's 20."),
  ("analysis", "The best-known machine-reading project in the field is composed as a success story with a round prize. The record's own page says what is posted and what still needs a person; the composition takes the round number from a post on X and leaves the person out.",
   "The best-known machine-reading project in the field is composed as a success story, its prize at the challenge's own figure. The record's own page says what still needs a person, and the composition leaves the person out.")],
 "ai-and-faith-aio-20261031": [
  ("findings", "(the BYU News card: 'announced May 2026', '14 LLMs').",
   "(the BYU News card: 'announced May 2026', '14 LLMs'). The page names the body 'The Consortium for Evaluation of Faith and Ethics in AI (CEFE-AI)', and the words 'systematically omit or gloss over' are the composition's."),
  ("findings", "FIGURES BEYOND THE RECORD. The Barna percentages and the claim that 'Major tech companies (including OpenAI, Anthropic, Google, Meta, Amazon, and Microsoft) have actively engaged with religious leaders' are the cards'.",
   "FIGURES BEYOND THE RECORD. The Barna percentages are the Barna card's. The claim that 'Major tech companies (including OpenAI, Anthropic, Google, Meta, Amazon, and Microsoft) have actively engaged with religious leaders' is on no readable card: the Axios page refused the fetch, and the nearest is the title of the Firstpost video.")],
}


def apply(e, slug):
    for field, old, new in R[slug]:
        if field == "findings+":
            if new not in e["findings"]: e["findings"].append(new)
            continue
        if field == "findings":
            hits = [i for i, f in enumerate(e["findings"]) if old in f]
            assert len(hits) == 1 and e["findings"][hits[0]].count(old) == 1, (slug, old[:60], hits)
            e["findings"][hits[0]] = e["findings"][hits[0]].replace(old, new)
        else:
            assert e[field].count(old) == 1, (slug, field, old[:60])
            e[field] = e[field].replace(old, new)


reg = json.loads(REG.read_text(encoding="utf-8"))
by = {e["slug"]: e for e in reg["entries"]}
for slug in R:
    apply(by[slug], slug)
    dp = H / (slug + ".json"); d = json.loads(dp.read_text(encoding="utf-8")); apply(d, slug)
    if "--check" not in sys.argv: dp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
if "--check" not in sys.argv:
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
print("repaired", len(R), "entries", "(check only)" if "--check" in sys.argv else "")
