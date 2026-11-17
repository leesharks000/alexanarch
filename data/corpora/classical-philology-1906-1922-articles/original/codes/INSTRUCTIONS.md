# Dead Letters: coding Classical Philology 1906–1922 on the page

You are one reader of ten. Your chunk file holds about 90 articles and notes from Classical Philology (1906–1922), as JSTOR's Early Journal Content served them, each with its catalogued title. Each item has an OPENING (the first ~450 words of the page after JSTOR's boilerplate), up to four WINDOWS (~600 characters around text-question vocabulary later in the item), and a CLOSING (the last ~250 words). Read every item's extract in full before coding it. Code what the item does, from the page, not from its title alone.

## The codebook (one primary code; an optional secondary)
- A, locus: re-reads a passage for its sense.
- B, repair: resolves an apparent inconsistency or problem inside an author.
- C, reconstruction: reconstructs a doctrine, institution, practice, event or context from texts.
- D1, text at the locus: emendation, conjecture, crux, reading of a manuscript at a passage, lacuna, colometry, interpolation of a line or passage.
- D2, text at the work: authenticity, authorship, date, unity or composition of a work; its manuscript tradition or recension; an edition.
- D3, text at the corpus: the partition of a corpus among composing persons. Whether names in a corpus are one maker or several (e.g. whether the Iliad and Odyssey are one poet's; whether works under one name are by several; whether two names are one maker), and whether the author is the right unit.
- E, relation: sources, imitation, allusion, influence, intertext between authors.
- F, after antiquity: reception and transmission beyond antiquity, as an object of study.
- G, position: argues a thesis not anchored to an author or text: method, theory, a general claim; also editorial notices, programmes, obituaries, announcements.
- L, language: grammar, lexicon, metre, accent, dialect, style as language.
- M, document: publishes or reads an inscription, papyrus or object as a document.

## Fields (one JSON object per item, one per line, in your output file)
- "id": the item id exactly as given.
- "kind": "article" (a signed study), "note" (a short signed note, under ~4 pages), "review" (a review of a book or books), or "notice" (obituary, announcement, list, editorial, books received).
- "title": the item's title as the page prints it (for a review: the book reviewed, short).
- "reach": the primary code. "reach2": a secondary code or null.
- "span": 6–30 words copied EXACTLY, character for character, from the extract, that show the primary code. Copy, do not paraphrase. Keep OCR errors as they stand.
- "d_direction": for any D1/D2/D3 code (primary or secondary): "confirm" if the item settles toward the received text, standing or attribution, "open" if it puts the received text, standing or attribution in question, "both" if it does each for different things; null otherwise. Decide from what the item concludes (read the CLOSING and WINDOWS), not from its title.
- "d_span": for a D code, 6–30 words copied exactly from the extract that show the direction; else null.
- "evidence": for D and B codes: "locus" (the argument rests on readings at particular passages), "relation" (it rests on a relation among parts: order, form, structure, style across a whole, convergence of several indications), "find" (a manuscript, papyrus or inscription newly brought in), or "mixed"; null otherwise.
- "relation_decides_locus": for D and B codes: true if a relation among parts (form, order, structure, convergence) is allowed to decide a question at a particular passage or attribution; false if each locus is decided on its own; null otherwise.
- "sense_method": for items arguing a word's sense (usually L or A): "parallels" (occurrences cited one by one, sorted into senses), "passage" (the word read in its passage and the form of the work), or "both"; null otherwise.
- "note": up to 25 words of your own, only where a code needs a reason (especially any D3, and any D code in a review).

## Rules
- D3 is rare. Code it only where the item takes up the partition of a corpus among persons. Scribes' hands in a manuscript, vase-painters, "the same author's" other book, are not D3.
- A review that reports and judges a book's argument on a work's authenticity, date or a corpus partition gets that D code, with kind "review".
- Every span and d_span must be a verbatim substring of the extract. They will be checked by machine against the full page; a span that does not match is discarded.
- Write your output as JSON Lines to the output path you are given, one line per item, every item in your chunk, in order. Then reply with only: the number of items coded, and the count of each primary code.
