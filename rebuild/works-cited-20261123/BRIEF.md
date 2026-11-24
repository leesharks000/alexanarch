# Reader brief: the works each deposit cites, as a standard list

You are one of several readers. For each record assigned to you, read its full text file (path given) from start to end, in chunks, and list every OUTSIDE work the text cites, quotes, or names as a source it read or relies on. Outside work = anything that is NOT an alexanarch.org record (records cited as #N are handled separately; do not list them). Include: books, articles, editions of ancient texts, translations, web pages, datasets, reports, news articles, software/repositories, standards, letters/emails quoted, Wikipedia pages, public statements.

Rules (provenance is the point; nothing is invented):
1. Only what the text itself cites. Do not add works it does not cite. Do not look anything up on the web. Do not supply a year, publisher, URL or page range the text does not give, EXCEPT you may copy details given elsewhere in the same text (e.g. a footnote gives the year, a later section the URL).
2. Each entry in standard bibliographic form, Chicago author-date style, one line:
   Surname, Forename (or initials as given). Year. "Article Title." *Journal* Vol (Issue): pages. https://doi.org/… or URL.
   Surname, Forename. Year. *Book Title*. Place: Publisher.
   Ancient texts: Author. *Work*. Ed./trans. Editor. Place, Year (as given). Seat or URL if given.
   Web page: Author or Organization. Year. "Title." Site. Date if given. URL.
   If the text gives no year, write n.d. in the year slot. If no author, start with the organization or the title.
   Use markdown italics (*…*) for book/journal/site titles, straight double quotes for article titles.
3. One entry per distinct work (merge repeated citations; separate editions = separate entries).
4. Provenance for every entry: the 1-based line numbers in the file where the text cites it (at least one, up to five), and a short verbatim snippet (under 120 characters) copied from one of those lines that shows the citation.
5. Do not change anything in the repository. Write only your output files.

Output: for each record N, write /tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/refs/N.json exactly as:
{"n": N, "file": "<path>", "lines_read": <total line count of the file>, "read_in_full": true,
 "entries": [{"ref": "<the one-line entry>", "lines": [<ints>], "snippet": "<verbatim from the file>"}],
 "notes": "<anything uncertain, e.g. a work named too vaguely to cite>"}
Sort entries alphabetically by their first word. If a record cites no outside works, write entries: [] and say so in notes.
At the end, reply with one line per record: N, entry count, and anything uncertain.
