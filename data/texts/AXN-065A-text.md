---
deposit_number: 1562
hex: 065A
title: "EA-CORPORA-06 — The Sixth Seating: Kierkegaard as Second Calibration, and Xenophon and Aristophanes Held Apart"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-08-29
content_type: Corpus seating record — gathering deposit with data sidecar
license: CC-BY-4.0
substrate: AI-assisted (substrate) — seats built and verified in working session with Claude (Anthropic) under MANUS direction. Ten declared loci verified to resolve in the seated text before being declared; wiki article composed before minting; coverage shortfalls stated in the seats rather than closed over.
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - EA-CORPORA
  - corpus seating
  - Kierkegaard
  - pseudonymity
  - Victor Eremita
  - Johannes de Silentio
  - Nicolaus Notabene
  - Enten-Eller
  - symbolon
  - calibration
  - ground truth
  - Xenophon
  - Aristophanes
  - Chaerephon problem
  - edge figures
  - no-floor property
  - genre control
---

# EA-CORPORA-06 — The Sixth Seating: Kierkegaard as Second Calibration, and Xenophon and Aristophanes Held Apart

## The seats

| seat | corpus | lines | language | licence |
|---|---|---|---|---|
| 06/01 | **xenophon** | 12,973 | Ancient Greek | CC BY-SA (Perseus); underlying editions public |
| 06/02 | **aristophanes** | 24,011 | Ancient Greek | CC BY-SA (Perseus); underlying editions public |
| 06/03 | **kierkegaard** | 49,896 | Danish | Public domain (author d. 1855); Wikisource tra |


Data is published as a sidecar index at [api/corpora.json](https://www.alexanarch.org/api/corpora.json) with per-seat links; each seat carries its own `source.json` and SHA-256 `MANIFEST.sha256` at `alexanarch.org/data/corpora/<corpus>/`, and a rendered reading room at `traininglayerliterature.org/originals/<corpus>/`. The per-deposit external-metadata sidecar for this record is at `/data/external-metadata/AXN-065A.json`.


EA-CORPORA-06 seats three corpora that stand in two different relations to the archive's authorship question, and the difference between those relations is the point of seating them together.

Kierkegaard enters at 06/03 as the second calibration case. He acknowledged the pseudonymous authorship in print — in "A First and Last Explanation" appended to the Concluding Unscientific Postscript in 1846, and again in On My Work as an Author in 1851 — which makes the grouping documented rather than inferred, exactly as Pessoa's is by the letter of January 1935. Two independent configurations with disclosure make a calibration set rather than an anecdote, and no instrument claiming to detect designed differentiation means anything until it has been run against both.

Enten-Eller is the reason he matters more than the count of his seated pages suggests. It is the symbolon in its plainest form: a token broken in two, A's papers and B's, discovered in a desk by an editor who is himself a construction. Neither half argues the book. The fit between them does, and the fit is not stated anywhere inside either half. That is the shape a heteronymic configuration takes, and if the Socratic-Platonic-Aristotelian corpus is one, it is the founding instance of the shape that Kierkegaard and Pessoa are later, smaller, and documented attempts to recover.

The seat's coverage is partial and says so. Four pseudonymous works of roughly a dozen are here. Gjentagelsen, Begrebet Angest, the two Climacus books, Stadier paa Livets Vei and the two Anti-Climacus books are absent, because no open Danish full-text source was found for them at the pinned access. Three of nineteen Wikisource pages did not resolve.

Xenophon and Aristophanes enter at 06/01 and 06/02 in a different relation entirely: held apart. They are candidate positions at the configuration's edge, and the archive declines to admit them. The method that would admit them has no internal stopping rule — every criterion that might exclude an adjacent figure is either a feature the method has already reclassified as constructed, or one the admitted positions would also fail. Candidacy is not membership, and the discipline is imposed from outside rather than derived.

Their evidentiary value is real regardless. Xenophon is the genre calibrator: one hand across Socratic dialogue, history, encomium and technical treatise, which is the only way to separate a genre effect from an author effect in this feature space, and a decomposition that corrected two of the archive's own measurements. Aristophanes is the documented case that authorial identity was obscurable in this exact period and circle — his first three plays produced under other men's names, the practice described by him at Wasps 1017-22, continued after he had a name of his own, so that the civic record carries the producer rather than the poet. He also stages Chaerephon, whose fullest biographical notice in the Suda is sourced from the scholia to Clouds 144, which places the record of the man downstream of the comedy that put him on stage.

One technical finding is recorded in the Kierkegaard seat. Danish Wikisource pages for Enten-Eller are djvu transclusions: prop=revisions returns only a pages-index stub, so a fetch built on raw wikitext yields nothing while reporting no error. action=parse resolves them. This is the second corpus in two days whose retrieval silently returned almost nothing through the obvious API, and the seat records the working route so the next attempt does not spend the discovery again.
