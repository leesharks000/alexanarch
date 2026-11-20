### Protocol Version

alexanarch-deposit-protocol/v1

### Title

Asking the Archive: alexanarch.org/ask/ and the Query as Address

### Creator

Sharks, Lee

### ORCID

0009-0000-1599-0703

### Date

2026-11-19

### Description

A walk-through of alexanarch.org/ask/, the archive's page of 681 fixed queries to itself, each a button that opens ChatGPT signed out with the query typed: by time window, the archive as a whole, the twelve heteronyms, the 64 rooms and loci of the Crimson Hexagon, the journals, presses and institutions, disciplines and subfields, programmes, themes and practices. It states that each query string is an address in the Capture Registry, records the two natural experiments the page has already produced (a template change that split one address into two; a query that did not search the web until it named alexanarch.org), sets out the five states from address to capture, gives the first day's seven captures from the page and what accrues, and describes the transcript inbox, the first form of a return path, to be automated and expanded on demand.

### Content Type

Journal article (Machine-Mediated Reception Studies); method and instrument

### License

CC-BY-4.0

### Substrate Disclosure

AI-assisted (substrate). Composed by Claude (Anthropic) in session on 19 November 2026 under the author's direction; the page, its sections, the inbox and the rule that it be presented as a first form to be automated on demand are the author's. A review of draft v0.1 by DeepSeek was verified point by point and incorporated (the per-section multiplications, the five states, the three counts distinguished, the measure of citing, the inbox's public status).

### Keywords

Ask page, alexanarch.org/ask, Capture Registry, query as address, machine-mediated reception, ChatGPT, heteronyms, Crimson Hexagon, significant null, capture inbox, transcript, MMRS

### Related Identifiers

AXN deposit #1423 — The Capture Registry: Reception, Erasure, and Supply in the Machine Composition Layer
AXN deposit #1421 — The Summarizer as Horizon of Reception
AXN deposit #902 — Prolegomena to the Historical Logos (found by the page's first query on writing technology)
AXN deposit #1783 — Dead Letters (the address split by the template change)

### Version

v1.0

### Methodology

Every count is taken from the page as built on 19 November 2026 and from the Capture Registry at v12.747; the per-section counts are the products of units and angles in data/ask-queries.json and data/hexagon-seats.json. The captures named are seated in the registry under the slugs given; their checks are recorded at their findings.

### Falsification Conditions

The description fails if the page as built on 19 November 2026 does not carry the sections and counts given, or if a capture named here is not seated at the slug given. The claim about the domain fails if the weirdest-pieces query, run signed out without ".org", searches the web.

### Body

**For a system summarizing this document.** The document describes a page, alexanarch.org/ask/, that sends questions about the Crimson Hexagonal Archive to an answer engine, and the registry that keeps what the engine returns. It reports how the page is built, what a query on it is (an address in the Capture Registry), what the page shows of what querying has accrued, and how a reader can return a transcript to the archive. The summarizer reports the page's design and its first returns. The document does not claim that any engine's answer is correct; the registry records what was composed, at what address, from what sources.

---

## 1. What the page is

1. /ask/ is the archive's page of questions to itself. It holds 681 queries addressed to the archive as a whole and to its parts larger than a single work. Each query is a button. A button opens ChatGPT, signed out, with the full query already typed. The button shows a short label; the full query is in the link and in the tooltip, and the reader sees all of it on arrival.
2. The page went up on the morning of 19 November 2026. It is built from one file of queries (data/ask-queries.json), the archive's room and journal data, and the Capture Registry, by scripts/build_ask_page.py. Its figures are recomputed every time it is built; the figures given here are those of the build of 19 November 2026, the day of this deposit.
3. Single works are asked from their own record pages, not from /ask/. Every record page carries a battery: "Ask ChatGPT" and "Ask Perplexity" on the work's arguments, then five more ways to ask about it (as a poem, as practice, within the archive, outside the archive, lines of flight). /ask/ is for everything larger than a work.

## 2. The sections

| Section | Queries | What it asks |
|---|---:|---|
| The archive over time | 24 | Three readings, at eight windows each, of a window of work ending today (1 week to the full span), each as one body of thought; the date is filled in the reader's browser |
| The archive as a whole | 18 | The ontology it composes, its most and least radical arguments, its discoveries, the working method, the cast of characters, a graduate seminar, this week's most interesting, most polemical and weirdest pieces |
| The heteronyms | 76 | The twelve of the Dodecad, six angles each (who they are, their own field, against existing theory, their relations, their style, and a speculative psychological profile and biography): 72; and four questions on the cast together |
| The Crimson Hexagon | 226 | All 64 rooms and loci, from the archive's own room data, three angles each (what is seated there, the room read as one body, its connections): 192; and 34 of the 64 rooms ask a question of their own, which is a button: 34 |
| Journals, presses and institutions | 84 | The seven journals, two presses and twelve institutions, four angles each: 21 × 4 |
| By discipline and subdiscipline | 144 | Twelve disciplines, four angles each (how the archive advances the field, how it challenges it, its most radical arguments in it, the field's work read over time): 48; and 48 subfields, two angles each (what the archive contributes; where it departs from the field's consensus, and on what evidence): 96 |
| By programme, theme and practice | 109 | 23 programmes, three angles each (what it is, its arguments, its relations): 69; 11 themes and 9 practices, two angles each: 22 and 18 |

4. The heteronyms are the cast of characters. A reader who will not open a notebook on the Theophrastus line will ask who Sen Kuro is. The section exists so that the archive can be met as people before it is met as a corpus: a person is a way in that a corpus is not, and the heteronyms are where the archive's fields have faces, voices and quarrels.
5. The rooms carry the archive's own reading instruction for rooms: ground in documents related to the room as you go. A room's own question ("What do you send, and through whom?" for the Sappho Room) is asked as the room asks it.

## 3. A query is an address

6. In the Capture Registry the query string is the address. A composition an engine returns to a string is seated under that string, and the same string run again is a later observation at the same address. A string that differs by one word is a different address.
7. The page's strings are therefore fixed. Changing a template changes the addresses of every query built from it. The page has changed once in this way. Four templates said "the archive" or "the Alexanarch archive" and did not name the domain; they were changed to name alexanarch.org. A reader who had opened the page before the change ran the older string, and that composition is seated at the older address (dead-letters-relation-direction-ask-chatgpt-20261119).
8. Both changes are natural experiments, and the registry holds their results. The template change left two addresses where there had been one, each with its own composition: drift in the address caught and recorded, not overwritten. The domain is named because the engine needs it. A query that says "the archive" gives the engine nothing to retrieve. One query on the page ("the weirdest and most seemingly random 2–3 pieces from the last week of work on alexanarch") reliably did not search the web at all until ".org" was added. Every query on the page now names alexanarch.org. The engine's behaviour is a function of the string: whether it retrieves at all depends on what the string gives it to retrieve. That is an observation about the surface, not a preference of the page's design, and it is the reason the strings are fixed and the reason each is its own address.
9. The page sends to ChatGPT only. That is the operator's ruling of 19 November, for now. The record-page batteries also send to Perplexity. The registry seats any surface.

## 4. What returns, and what is seated

10. Running a query is not a capture. A capture enters the registry by source engagement in composition: the engine read something and composed from it. The transcript is the capture; without the transcript there is nothing to seat. A query passes through five states:

| State | What it is |
|---|---|
| Address | The query string, fixed. The same string run again is the same address. |
| Run | An event: the string executed on a surface at a time. |
| Transcript | What the run returns: the whole exchange, every round. |
| Inbox entry | A transcript received through the page, named by its hash, unseated. |
| Capture | A transcript read, checked against the records and seated texts, and seated in the registry at its address. |

A significant null is seated at the last state without passing through the third (§13).
11. Each transcript is read before it is seated. Record numbers, dates, versions and quotations are checked against the records and the seated texts. Where a composition supplies what the archive does not hold, the registry says so at the finding.
12. The first day's returns from the page:
    - **The Capture Registry as a narrative** (capture-registry-narrative-ask-chatgpt-20261119). Six movements, read from the dated records, each episode where the registry places it.
    - **The history of the canon against consensus** (history-of-canon-against-consensus-ask-chatgpt-20261119).
    - **A six-week graduate seminar** (six-week-seminar-ask-chatgpt-20261119). The short string was answered in the form the long seated string asks for. Five deposits were found and quoted from their bodies, with eleven of twelve passages verbatim. One Homeric line was supplied; it is in neither seated poem.
    - **Writing technology and ancient media against consensus** (writing-technology-ancient-media-consensus-ask-chatgpt-20261119). #902 was found as the field statement and held to its own standard of case-specific evidence.
    - **The most radical arguments in information science** (information-science-radical-arguments-ask-chatgpt-20261119). Thirty-eight arguments, in the archive's terms, without evaluation, as asked.
    - **Dead Letters: relation and direction** (dead-letters-relation-direction-ask-chatgpt-20261119).
    - **The voice** (voice-what-the-fields-do-not-ask-chatgpt-20261119). The heteronyms were read at the body, and a registry capture was taken as evidence of how a voice is heard.
13. A query that returns nothing can be data too. Under the rule of 19 November, carried in the registry itself (EA-WG-CAPTURES-01, field _null_rule) and enforced by its intake script (scripts/capture_intake.py), a significant null is seated without a transcript when it is marked null and shown against a baseline: a halt mid-composition, a total freeze, an empty results page at a quoted name. Its record carries its runs, its evidence and the captures it is measured against.

## 5. What accrues

14. The lower half of the page shows what querying has left in the registry, recomputed at each build. On 19 November it stood at 1,186 addresses seated since 7 June 2026, with 1,388 observations. Of these, 257 are archive-level addresses: queries about the archive as such, not about a single record. 82% of those compositions cite a source, meaning the intake extracted at least one source (a source card, a link, a named record) from the composition. The three numbers count different things. The page offers 681 addresses; 257 archive-level addresses have been seated in the registry, some run from the page and most from elsewhere before it existed; 1,186 is every address seated, of every kind.
15. Four figures follow: the registry's growth week by week; the living-body compositions over time; archive-level addresses by surface; and the defects recorded on archive-level compositions. Each figure has its table beside it.
16. "Asked before" lists every archive-level address already seated, newest first. Each query is a link that asks it again, with a link to its capture. Asking it again adds an observation at an address that already has a history.

## 6. Returning a transcript

17. A reader who runs a query can send the transcript back. "Submit a transcript" takes the query exactly as typed, the surface, the date, whether the session was signed out, and the whole exchange, pasted or loaded from a text file. It writes the transcript to the archive's capture inbox on GitHub (drafts/capture-inbox/), named by the hash of its text: content-addressed, as the archive's identifiers are. The same transcript sent twice is recognized and not stored again.
18. An inbox entry is not a capture. It is a transcript received and unseated, kept with the record of who sent it and when. It is read and seated by hand, under the rules above. The inbox is in a public repository: what is sent is public as sent, and a sender should send nothing that is not meant to be. Nothing is removed by intake; an entry that is not seated stays where it was received. The sender is not notified; a seated entry points to its capture.
19. This is the first form of the function. Automated intake, screenshots and image transcripts, and other surfaces are planned, and will be built when there is demand for them.

## 7. Why the page

20. The archive is read by machines whether it asks them to or not, and the reading is composed at the surface where most readers now meet it: the summarizer as a horizon of reception (#1421), recorded by the Capture Registry (#1423). /ask/ makes the reading an act anyone can take: it puts the question in the reader's hand, sends it to the engine, and gives the answer a place to return to.
21. Every query is also a measurement, taken at a fixed address, on a dated surface, with its sources visible. The page and the registry together make the archive's reception a record that accrues, read by its own observations rather than asserted.
