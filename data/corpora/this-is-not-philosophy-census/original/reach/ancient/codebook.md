# Reach codebook (one code per abstract)

Code what the article DOES with its object, as its abstract states it. Code the article's main move, not side remarks. One primary code; an optional secondary only if the abstract plainly makes two moves of equal weight.

- **A — passage, term or argument re-read.** The unit is a passage, a term, a single argument or a line: "a new reading of X 1017a7–30", "the meaning of 'Y' in Z", "the argument at Phaedo 74".
- **B — an apparent inconsistency resolved.** The abstract sets up a tension, puzzle, contradiction, problem or apparent conflict *in or between the author's texts or doctrines* and shows it is resolved, dissolved, or only apparent ("reconcile", "consistent", "despite appearances", "seems to conflict"). If it resolves a puzzle by re-reading one passage, B wins over A. If it argues the tension is REAL and left standing, that is not B (code C or D by what it does with it).
- **C — a doctrine reconstructed inside one author.** A view, theory or position of one author (or one school treated as one author) is reconstructed, explained, defended or systematized from across that author's works ("Aristotle's theory of X", "the Stoic account of Y").
- **D — a claim about the text itself.** Authenticity, authorship, dating, unity or disunity, redaction, transmission, textual criticism, place within a corpus, the status of a work or fragment as evidence. Includes defences of unity/authenticity. Note in `dir` whether the claim CONFIRMS the received standing of the text ("confirm") or OPENS it — inauthentic, composite, misattributed, redated against consensus, emended against the vulgate ("open"), or "neutral".
- **E — relations across authors or receptions within antiquity.** The article's main object is a relation: influence, polemic, comparison, reception, between two or more ancient authors/schools (incl. late antique commentators on Aristotle, Plato in Plotinus, etc.).
- **F — engagement past antiquity.** Main move brings the ancient material into relation with post-antique philosophy, science, or present debates (medieval, early modern, modern philosophers; contemporary metaethics; "relevance today") as a central claim, not a passing nod.

Non-scholarly items (editorial notes, obituaries, book notes, corrigenda, reports) → code **X**.

Decision order when torn: D > B > E > F > C > A (pick the earliest that genuinely describes the MAIN move).

## Output: one JSON object per line
{"id": "...", "code": "A|B|C|D|E|F|X", "code2": "" or a letter, "dir": "confirm|open|neutral" (D only, else ""), "quote": "<verbatim span of 6–30 words copied EXACTLY from the abstract that warrants the code>"}

The quote must be an exact substring of the abstract (same characters, same punctuation). It will be machine-checked; a non-matching quote invalidates the row.
