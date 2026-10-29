"""Capture repair 2026-10-29 (fourth): findings of the Labor Vector intake that the fifteen /non composers showed to misstate
or miss their sources. Repair mode, one operation, in its own commit. Each correction was re-checked in session against the pages
the composers saved (datasets/negative-of-the-negative/v2/intake/<row>-20261029/). The pattern behind most of them: the intake
checked its findings against the census's saved sources and not against the capture's own cards, so material the Overview took
from its cards was called absent from every source.

Applied to the registry entries (data/EA-WG-CAPTURES-01.json) and to the intake drafts beside this file. Every old string must be
found exactly once, or nothing is written.
  python3 repair-20261029.py [--check]"""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"

R = {  # slug -> list of (field, old, new); field "findings+" appends a finding
 "negotiating-tech-aio-20261029": [
  ("findings", "from LinkedIn, YouTube, Medium, the Tech Interview Handbook, Reddit and Goldman Sachs: thirteen cards.",
   "from LinkedIn, YouTube, Medium, next play, the Tech Interview Handbook, Reddit, Goldman Sachs and Instagram: thirteen cards.")],
 "microsoft-working-with-ai-aio-20261029": [
  ("findings", "its blog (card 4) and the press (cards 5, 7).", "its blog (card 4), a news video (card 5) and a Facebook post of unnamed authorship (card 7).")],
 "yale-budget-lab-ai-labor-market-aio-20261029": [
  ("findings", "BEYOND THE RECORD. 'wage trends' are in no saved source; the 'Capital vs. Labor' line (companies cutting jobs 'for broader macro or capital-investment reasons rather than direct workforce replacement by AI agents') and the 'slight volatility' in high-exposure unemployment rest on the Lab's other pages (cards 3 and 4), which the record did not read.",
   "BEYOND THE CARDS IT CITES. Wages are on card 4, the Lab's May 2026 note (its estimate for inflation-adjusted hourly wages is close to zero); the Overview cites its wage line to cards 1 and 2, which do not carry it. The 'Capital vs. Labor' line (companies cutting jobs 'for broader macro or capital-investment reasons rather than direct workforce replacement by AI agents') and the 'slight volatility' in high-exposure unemployment are on no card."),
  ("findings+", None, "THE USAGE FINDING DROPPED. The tracker's own takeaway that measures of AI usage show no connection to changes in employment or unemployment is on card 2's snippet and is not composed.")],
 "luddite-lab-aio-20261029": [
  ("findings", "is the record's quote, composed at its own grain;",
   "is the home page's form (card 1's snippet; the record quotes the About page's 'organizers'), composed more loosely;"),
  ("findings", "THE LEADERSHIP RAISED. 'Founded and co-led by figures including sociologist and DAIR director Alex Hanna': the hub's About page, saved with the record, lists her on the team as 'Director of Research, DAIR Institute' and names no founder; the founding is the composition's, on the LinkedIn card of her launch post. The primer's reframing of displacement as 'a management choice' rests on the AI Weekly card; the record does not carry it.",
   "THE LEADERSHIP RAISED. 'Founded and co-led by figures including sociologist and DAIR director Alex Hanna': 'co-led' is AI Weekly's (card 2: 'The team is led by Alex Hanna, Director of Research at DAIR, and Hannah Lipstein, Research Associate there'); 'founded', 'sociologist' and 'DAIR director' are in no source, and the LinkedIn card's 'as we launch' is a launch. The composition leaves out Hannah Lipstein. The primer's reframing of displacement as 'a management choice' rests on the AI Weekly card, given as the hub's 'Core Philosophy' without AI Weekly's own caveat ('advocacy-oriented research')."),
  ("findings+", None, "THE LAB AND THE HUB MADE ONE. 'formally known as the Luddite Lab Resource Hub' gives the Lab and its hub as one name; the Lab's newsletter (card 5) gives the hub as one of the Lab's 'two different offerings', beside its trainings for unions and organizers."),
  ("analysis", "The composition gives a team member as its founder, from her launch post.",
   "The composition gives one of its two leads as its founder, a title no source gives, and leaves out the other.")],
 "worker-info-exchange-aio-20261029": [
  ("mt", "AN OXFORD PARTNERSHIP THE RECORD DOES NOT HOLD", "THE OXFORD RESEARCH FROM ITS OWN CARDS, ABSENT FROM THE RECORD"),
  ("findings", "THE OXFORD PARTNERSHIP NOT IN THE RECORD. The TUC report is in a card (29 April 2026); the University of Oxford appears in no saved source.",
   "THE OXFORD RESEARCH, FROM THE CARDS. The TUC report is in a card (29 April 2026). The University of Oxford is absent from the census's saved sources and present in the Overview's own cards: card 2 ('Research by Oxford University and Worker Info Exchange, based on 1.5 million trips, shows falling driver pay') and card 3 (the 'participatory audit with Oxford University, built from drivers' own data subject access requests'). The composition's alliance is the cards' research."),
  ("analysis", "the composition joins it to its foundation and adds an academic partner the record cannot place.",
   "the composition joins it to its foundation and carries its Oxford research from its own cards, which the record has not read.")],
 "ilo-digital-labour-platform-policy-tracker-aio-20261029": [
  ("findings", "JUDICIAL DECISIONS AHEAD OF THE TRACKER. The ILO's own page says 'the next phase of the project will focus on ... integrating judicial decisions related to the platform economy'; the composition gives them as tracked now.",
   "JUDICIAL DECISIONS AHEAD OF THE TRACKER. The tracker's home page (card 1) states the aim, 'a comprehensive overview of global policies, legislation, collective bargaining agreements, and judicial decisions', and in the next sentences its limit: 'Currently, the tracker focuses on legislative developments worldwide, and includes collective bargaining agreements which are publicly available in Europe. The tracker will further develop ... the judicial decisions.' The composition turns the aim into the present and drops the limit; the ILO's expansion page gives the decisions as the next phase."),
  ("findings", "'MORE THAN 30 COUNTRIES'. The record states no count; the figure is in no saved source.",
   "'MORE THAN 30 COUNTRIES'. Held at the card's grain: the tracker's home page (card 1) lists 33 countries, with 58 legislation records, 15 collective bargaining agreements and 11 other initiatives (counted in session from its grid). The record states no count."),
  ("findings+", None, "TWO ISSUES ADDED. 'Remuneration and fair pay' and 'Contract termination and account deactivation' carry 'fair pay' and 'account deactivation', which no field source gives among the tracked issues.")],
 "fairwork-cloudwork-ratings-aio-20261029": [
  ("findings", "'spun out of' is the composition's word for an operator the record gives as based at both.",
   "'spun out of' is Fairwork's own wording on card 8 ('A non-profit spun out of the Oxford Internet Institute (OII) & Berlin Social Science Center (WZB)'); the record gives the project as based at both."),
  ("findings+", None, "THE AI ABSENT. The 2025 report's title is about 'Digital Labour and AI Supply Chain Governance', it has a section on data work, and two cards concern the labour behind AI; the composition mentions no AI."),
  ("findings+", None, "FINDINGS GIVEN AS DEFINITIONS. 'after costs', 'blanket liability clauses or vague job descriptions' and 'burnout, back pain' are findings of the 2025 ratings as the trade press reported them (card 6, The Global Recruiter: platforms with 'blanket liability clauses', workers earning the minimum wage 'after costs', policies on 'burnout or back pain'), composed as the definitions of the principles.")],
 "partnership-on-ai-responsible-sourcing-aio-20261029": [
  ("findings", "the vendor engagement guidance and transparency template are its August 2024 additions.",
   "the vendor engagement guidance and transparency template were introduced in August 2024 and finalized in PAI's post of 29 April 2026 (card 3), which the composition follows."),
  ("findings", "The composition calls the template 'a standard'; PAI's own pages give it as a template for reporting.",
   "The composition's template sentence is card 3's nearly word for word ('outlines what companies should be monitoring and publicly reporting'), with its force raised to 'A standard'."),
  ("findings+", None, "WORDS FROM OTHER HANDS. 'ethical supply chain' is the vendor Sama's phrase for its own effort (card 5), given as what the white paper outlines.")],
 "data-workers-inquiry-aio-20261029": [
  ("findings", "FIGURES BEYOND THE RECORD. 'low pay (sometimes under $1–$2 an hour)' and the extraction of 'voice recordings, facial scans, and photos of family members' are not in the saved sources; the record's own findings are the repository's range 'from psychological, physical and sexual abuse to resistance strategies and efforts to unionize' and the gift-card payment on Mechanical Turk.",
   "ONE INQUIRY'S FINDINGS GIVEN AS THE PROJECT'S. The personal-data list is card 6's, one inquirer's finding ('why are data workers asked to share their faces, voices, and even photos of their children'), composed at his detail, credited to the project, and 'children' changed to 'family members'. NDAs are on cards 5, 8 and 9, rejections on card 8. Only 'low pay (sometimes under $1–$2 an hour)' has no source. The record's own findings are the repository's range 'from psychological, physical and sexual abuse to resistance strategies and efforts to unionize' and the gift-card payment on Mechanical Turk."),
  ("findings", "and its 'nine countries' rests on the cards.", "and it lists nine country names, which the cards give as 'nine countries'."),
  ("findings+", None, "THE LIMIT DROPPED. One of the project's researchers writes on card 8 that the efforts it accompanied, 'such as efforts to build workers' councils, advocacy groups, or non-institutionalized solidarity structures', 'were largely forced to remain on a localized level'; the composition gives the collective action without the limit."),
  ("analysis", "The composition adds two vivid figures the record cannot source and leaves the inquiries' scale unstated;",
   "The composition carries one inquirer's findings as the project's, adds one figure no source holds, and leaves the inquiries' scale unstated;")],
 "ilo-generative-ai-and-jobs-index-aio-20261029": [
  ("findings", "the paper's 29.2% is the 2023 index's combined share of augmentation and 'the big unknown'.",
   "both numbers are in the paper as 2023 category shares: 29.2% is the 2023 index's combined share of augmentation and 'the big unknown', and 16.2% the share of 'the big unknown' alone (the same paragraph)."),
  ("findings", "the record keeps them as two measures.", "the record keeps them as two measures, and so does The People Space's card, which gives both in one sentence; the join into one range is the composition's.")],
 "turkopticon-aio-20261029": [
  ("findings", "its ratings are of requesters on Mechanical Turk, and it rates no platform.", "it rates requesters on Mechanical Turk, and no platform."),
  ("findings", "THE PRESENT WORK ABSENT. The working relationship with Amazon, the reinstatement system for suspended accounts and the mass-rejection campaign, the record's current findings, are not composed.",
   "THE PLATFORM'S CLOSURE ABSENT. Turkopticon's own article of 4 September 2026 (card 6): 'With Amazon announcing that MTurk will close on September 30, 2026'. The composition takes its list of data work from that card and leaves out the closure, and the record, in the present tense, has not recorded it. The working relationship with Amazon, the reinstatement system and the mass-rejection campaign, the record's current findings, are work on a platform that closed on 30 September."),
  ("findings+", None, "THE PURPOSE REVERSED. The composition's purpose for the tool, to make relations 'transparent', is the one the founders set themselves against in their CHI 2013 paper (card 5): others had 'promised to remedy the information asymmetry between workers and employers, repairing Mechanical Turk into a more \"transparent\" marketplace. Our team, by contrast, built Turkopticon in part to draw attention to commodification and exploitation'.")],
 "gdpval-aio-20261029": [
  ("findings", "Every figure is the record's: 1,320 tasks, 30 per occupation, 44 occupations, 9 sectors, the 220-task gold subset, experts averaging 14 years.",
   "Every figure the composition gives is the record's: 1,320 tasks, 44 occupations, 9 sectors, the 220-task gold subset, experts averaging 14 years.")],
 "bossware-and-employment-tech-database-aio-20261029": [
  ("d", "eleven named products in three groups", "thirteen named products in three groups"),
  ("findings+", None, "DISCONTINUED PRODUCTS GIVEN AS CURRENT. Two of the composition's examples are marked Discontinued in the table itself: Amazon's WiFi Tracking and HireVue AI Facial Recognition. 'Industry-Specific & Logistics Tracking' is not one of the table's categories; the Amazon tools and Netradyne are Workplace Safety rows.")],
}
# the turkopticon requester finding, corrected separately (its text was added in session before seating)
R["turkopticon-aio-20261029"].append((
  "findings", "REQUESTERS AS EMPLOYERS. The composition's 'review and rate employers (\"requesters\")' gives requesters a standing Turkopticon's FAQ withholds: 'While requesters are not employers in the legal sense, requesters are in a position of power over workers by virtue of making payment decisions'.",
  "REQUESTERS AS EMPLOYERS. The composition's 'review and rate employers (\"requesters\")' is the founders' own usage: their CHI 2013 paper (card 5) has workers 'create and use reviews of employers when choosing employers on AMT', and card 3 is titled an 'Employer Reputation System'. The FAQ, an own page the composition did not surface, adds the qualification: 'While requesters are not employers in the legal sense, requesters are in a position of power over workers by virtue of making payment decisions'."))


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
