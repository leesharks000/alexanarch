# Record repair — open questions for a ruling (2026-10-15)

Each question gives the case, what each option does, and a recommendation. Nothing below has been changed.

## 1. Day and Night: two editions in two records (#282, #324)
Both records seat the 2013 text ("Brief Preface…"). The current blog edition (December 2025: Publication History,
Translator's Preface, the fuller selection) is held only in each record's second store (data/deposits), which the
page does not show.
- a. Seat the current edition in #282, keep #324 as the 2013 text.
- b. Seat the current edition in both.
- c. Leave both as they are.

## 2. Six records whose AXN hashes the second store, not the text the page shows
#1204, #1250, #1344, #1382, #1383, #1521. On #1250 (The reward of love) the page shows the poem; the AXN is the hash
of a July restoration of the Ezra Pound post.
- a. Re-derive each AXN from the text the page shows (new glyph; the old one recorded, as for every repair today).
- b. Leave the identifiers as they are.
Recommendation: a — the identifier should name the bytes a reader sees.

## 3. "[pending]" DOIs inside 28 texts
Texts published with "DOI: [pending]" / "[to be minted]" where the DOI was assigned afterwards (and is recorded
elsewhere in the archive), e.g. #24, #47, #88, #335, #371, #381, #388, #518, #521, #528, #575, #605, #1327.
- a. Fill each with the DOI it was later assigned (a change to the published text).
- b. Leave the text as published; the record's metadata already carries the DOI.
Recommendation: b (repair standard: the text as published), unless you want citations inside texts completed.

## 4. Figures pointing at claude.ai chat files (#502, #507, #509)
The published posts carry the same broken figure links. The blog also hosts the images, uncaptioned, at the top of
the later post; which image is which figure cannot be read off the post.
- a. You name which image is which figure; the links are repointed to the Blogger images.
- b. Leave as published.

## 5. Record title names one version, the seated text is another (~15)
#72 (title v4.0, text v3.0), #161 (v1.1 / v1.2), #197, #543, #838, #872, #958 (v1.0 / v1.3), #1034, #1367
(v2.2 / v2.1), #1373 (v2.0 / v0.2), #1443 (v3.6 / v3.7) and others. The title came from the published deposit, so
either the wrong version's file was seated, or the title was mistyped.
- a. Search the blog and the archive for the version the title names; seat it where found (duplicate check
  first); where not found, record the mismatch on the page and leave both as they are.
- b. Retitle each record to the version actually seated.
- c. Leave as they are.
Recommendation: a.

## 6. Wrong bodies whose work is not on the blog
#1168 (Untitled), #1358 (Contributor License v3.0, Rhys Owens), #1393 (Jess Elgene certificate), #980/#981 (Alice
Thornburgh registry), #982 (pessoagraph visualization), #959 (Hexagonal OS build files), #962, #988, #1132, #1242,
#1347, #1371, #1376 (ChatGPT prospectus), #1021 (Pound canon node). Not on the blog; data-rhizome is not reachable
from this session (403).
- a. Grant this session access to data-rhizome, or attach the files; each is then seated with the duplicate check.
- b. Leave held: each keeps its current body, and its page states the body is a different work.

## Rulings (Lee Sharks, 2026-10-15 19:45)
1. "keep dates and posts synced." — #282 seated with the post of 2026-01-09, #324 with the post of 2026-01-17
   (kind other_edition; the 2013 text kept as appendix). Standing rule: a record's text, seated from the blog, is the
   post of the record's own date.
2. "recompute." — the six AXNs re-derived from the canonical text (scripts/repair_rulings_20261015.py).
3. "leave them." — in-text "[pending]" DOIs stay as published.
4. "only if you can inspect it, im not tracking down individual figures - why not link to the relevant blog post
   generally?" — the six figure links in #502/#507/#509 now link to the post of the record's date.
5. "the blog often holds only the most up to date version, it was often my practice to overpaste rapid updates."
   — version mismatches between a record's title and its text stay; the blog is not used to replace a record's text
   on the ground of version.
6. "whatever." — off-blog wrong bodies stay held.
Readers approved for the remaining reading: "yes im open to readers, long as they have provenance" — each reading
carries read ranges, verbatim quotes with lines (checked), and its transcript is audited for the lines it opened.
