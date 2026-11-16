# The census of *This Is Not Philosophy*

This seat holds what the notebook's tables are built from. The publishers' abstracts are not here: each coded article is reached by its DOI, and every reach code carries the 6–30-word span of the abstract it rests on, verbatim, so that a reader can check the code against the abstract at its source.

## original/census/
One `<journal>.jsonl` per journal: n, DOI, year, type, title (with the Crossref subtitle joined as `title: subtitle`), authors, volume, issue, pages, whether Crossref holds an abstract, the number of references, cited-by. `<journal>.source.json` records the query, the date read and the hash of the raw pull. `persee-<series>.jsonl` holds the Persée OAI records (title, date, identifier, creator, type) for the *Revue philosophique de Louvain* (phlou) and the *Revue des Études Grecques* (reg).

Journals: Ancient Philosophy, Phronesis, Apeiron, Elenchos, Rhizomata, Archiv für Geschichte der Philosophie; Continental Philosophy Review, Man and World / Husserl Studies line (manworld), Research in Phenomenology, Journal of the British Society for Phenomenology, Philosophy Today, Angelaki; Noûs, Mind, Philosophy and Phenomenological Research; Philologus, Classical Quarterly, Rivista di storia della filosofia, Peitho, Revue de philosophie ancienne; and the two Persée series.

## original/codes/
The object codes: for each title, the group (Plato, Aristotle, Presocratics, …, or for the continental arm the names of the apparatus) as `code2.py` and `code_cont.py` assign them.

## original/reach/
`ancient/`, `continental/`, `analytic/`: the readers' output files (one row per abstract: DOI, code, direction where D, the span), the codebooks, the calibration codes, the adjudication logs (each ruling with its reason), and the tallies. The readers were Claude instances working in parallel, each code machine-checked for its span; the lead coder adjudicated (notebook §0.5b).

## original/standing/
The lexicon pulls (`dpull*.tsv`, `pull-*.tsv`) and the hand rulings S (a work's standing: authenticity, date, order, composition, unity, authorship) and T (text, fragment, transmission) that build §4.12.

## original/stylometry/
The script and its output (§4.15). The corpus of abstracts it reads is rebuilt by `build.py` from the DOIs; it is not seated.

## original/scripts/
Every script that built the above.
