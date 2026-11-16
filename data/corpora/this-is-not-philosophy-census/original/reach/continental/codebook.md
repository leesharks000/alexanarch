# Reach codebook, continental (one primary code per abstract)

Code what the article DOES, as its abstract states it: its main move, not side remarks. Give one primary code, and an optional code2 only when the abstract plainly makes two moves of equal weight. Codes A–E match the codebook used for the ancient-philosophy journals. F is redefined here, and G is new.

- **A — A passage, term, single text or argument re-read.** The unit is one text or one term: "a reading of §44 of Being and Time", "the word Walten in Beast & Sovereign II".
- **B — An apparent inconsistency resolved.** The abstract sets up a tension, contradiction or apparent defect in the author's own texts or doctrine, and shows it is resolved, dissolved or only apparent. If the tension is argued to be real and left standing, it is not B.
- **C — A doctrine reconstructed inside one author.** One author's view, concept or position is reconstructed, explained, defended or systematized, including against other interpreters of that author ("Husserl's critique of liberalism", "Arendt on truthfulness").
- **D — A claim about the text itself.** Editions, the Nachlass, newly published or unpublished material treated as the article's object, dating, compilation (e.g. Der Wille zur Macht), translation as the object, authenticity, the status of a text. Record dir: "confirm", "open" or "neutral".
- **E — Relations across authors.** The main object is a relation between two or more named thinkers: X's reading of Y, X and Y on Z, influence, debate, reception.
- **F — An author's apparatus applied.** A named author's concepts are applied to a phenomenon, case, present problem or another domain: "Arendt and architecture", "Heidegger and AI", "a Derridean reading of the constitution".
- **G — Independent thesis.** The article argues its own thesis about a phenomenon or problem. It is not anchored in reconstructing or applying a named author, though it may cite authors along the way: a phenomenological description, a conceptual argument, a position in a contemporary debate.

Non-scholarly items (editorials, introductions to an issue, interviews, review essays that mainly summarize, obituaries) → **X**.

When torn, decide in this order: D > B > E > F > C > A > G. Pick the earliest code that genuinely describes the MAIN move. Code G only when no named author's corpus is the object.

## Output: one JSON object per line
{"id": "...", "code": "A|B|C|D|E|F|G|X", "code2": "" or a letter, "dir": "confirm|open|neutral" (D only, else ""), "quote": "<verbatim span of 6–30 words copied EXACTLY from the abstract that warrants the code>"}

The quote must be an exact substring of the abstract (same characters, same punctuation). It is machine-checked, and a row whose quote does not match is invalid.
