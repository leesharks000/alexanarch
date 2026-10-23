---
annotations_creators:
- expert-generated
license: cc-by-sa-4.0
task_categories:
- translation
- token-classification
language:
- egy
- de
multilinguality:
- multilingual
pretty_name: Thesaurus Linguae Aegyptiae, Original Earlier Egyptian sentences, corpus v18, premium
size_categories:
- 10K<n<100K
dataset_info:
  features:
  - name: hieroglyphs
    dtype: string
  - name: transliteration
    dtype: string
  - name: lemmatization
    dtype: string
  - name: UPOS
    dtype: string
  - name: glossing
    dtype: string
  - name: translation
    dtype: string
  - name: dateNotBefore
    dtype: string
  - name: dateNotAfter
    dtype: string
splits:
  - name: train
    num_examples: 12773
---
# Dataset Card for Dataset _tla-Earlier_Egyptian_original-v18-premium_

<!-- Provide a quick summary of the dataset. -->
This data set contains Earlier Egyptian, i.e., ancient Old Egyptian and ancient Middle Egyptian, sentences in `hieroglyphs` and `transliteration`, with `lemmatization`, with POS `glossing` and with a German `translation`. 
This set of _original_ Earlier Egyptian sentences only contains text witnesses from before the start of the New Kingdom (late 16th century BCE).
The data comes from the database of the [Thesaurus Linguae Aegyptiae](https://thesaurus-linguae-aegyptiae.de), corpus version 18, and contains only fully intact, 
unambiguously readable sentences (12,773 of 55,026 sentences), adjusted for philological and editorial markup.

## Dataset Details

### Dataset Description

<!-- Provide a longer summary of what this dataset is. -->

- **Homepage:** https://thesaurus-linguae-aegyptiae.de.
- **Curated by:**
German Academies’ project “Strukturen und Transformationen des Wortschatzes der ägyptischen Sprache. Text- und Wissenskultur im alten Ägypten”,
Executive Editor: [Daniel A. Werning](https://www.bbaw.de/die-akademie/mitarbeiterinnen-mitarbeiter/werning-daniel).
- **Funded by:**
The Academies’ project “Strukturen und Transformationen des Wortschatzes der ägyptischen Sprache. Text- und Wissenskultur im alten Ägypten” of the Berlin-Brandenburg Academy of Sciences and Humanities and the Saxon Academy of Sciences and Humanities in Leipzig is co-financed by the German federal government and the federal states Berlin and Saxony.
The Saxon Academy of Sciences and Humanities in Leipzig is co-financed by the Saxon State government out of the State budget approved by the Saxon State Parliament.
- **Language(s) (NLP):** egy-Egyp, egy-Egyh, de-DE.
- **License:** [CC BY-SA 4.0 Int.](https://creativecommons.org/licenses/by-sa/4.0/); for required attribution, see citation recommendations below.
- **Point of Contact:** [Daniel A. Werning](https://www.bbaw.de/die-akademie/mitarbeiterinnen-mitarbeiter/werning-daniel)

## Uses

<!-- Address questions around how the dataset is intended to be used. -->

### Direct Use

<!-- This section describes suitable use cases for the dataset. -->

This data set may be used
- to train translation models Egyptian hieroglyphs => Egyptological transliteration,
- to create lemmatizers Earlier Egyptian transliteration => [TLA lemma ID](https://thesaurus-linguae-aegyptiae.de/info/lemma-lists),
- to train translation models Earlier Egyptian transliteration => German.

### Out-of-Scope Use

<!-- This section addresses misuse, malicious use, and uses that the dataset will not work well for. -->

This data set of selected intact sentences is not suitable for reconstructing entire ancient source texts. 

## Dataset

## Dataset Structure

<!-- This section provides a description of the dataset fields, and additional information about the dataset structure such as criteria used to create the splits, relationships between data points, etc. -->

The dataset is not divided. Please create your own random splits.

The dataset comes as a _JSON lines_ file.

### Data Fields

#### plain_text
- `hieroglyphs`: a `string`, sequence of Egyptian hieroglyphs (Unicode v15), individual sentence elements separated by space.
- `transliteration`: a `string`, Egyptological transliteration, following the [_Leiden Unified Transliteration_](https://www.iae-egyptology.org/the-leiden-unified-transliteration), individual sentence elements separated by space.
- `lemmatization`: a `string`, individual [TLA Lemma IDs](https://thesaurus-linguae-aegyptiae.de/info/lemma-lists)+"`|`"+lemma transliteration, separated by space.
- `UPOS`: a `string`, Part of Speech according to [Universal POS tag set](https://universaldependencies.org/u/pos/).
- `glossing`: a `string`, individual glosses of the inflected forms, separated by space (for information, see the comments below).
- `translation`:  a `string`, German translation.
- `dateNotBefore`, `dateNotAfter`: two `strings` containing an integer or empty, _terminus ante quem non_ and _terminus post quem non_ for the text witness.

### Data instances

Example of an dataset instance:
```
{
  "hieroglyphs": "𓆓𓂧𓇋𓈖 𓅈𓏏𓏭𓀜𓀀 𓊪𓈖 𓈖 𓌞𓏲𓀀 𓆑",
  "transliteration": "ḏd.ꞽn nm.tꞽ-nḫt pn n šms.w =f",
  "lemmatization": "185810|ḏd 851865|Nmt.j-nḫt.w 59920|pn 400055|n 155030|šms.w 10050|=f",
  "UPOS": "VERB PROPN PRON ADP NOUN PRON",
  "glossing": "V\\tam.act-cnsv PERSN dem.m.sg PREP N.m:stpr -3sg.m",
  "translation": "Nun sagte dieser Nemti-nacht zu seinem Diener:",
  "dateNotBefore": "-1939",
  "dateNotAfter": "-1630"
}
```

## Dataset Creation

### Curation Rationale

<!-- Motivation for the creation of this dataset. -->

ML projects have requested raw data from the TLA. 
At the same time, the raw data is riddled with philological markers that make it difficult for non-Egyptological users. 
This is a strictly filtered data set that only contains intact, unquestionable, fully lemmatized sentences. 

### Source Data

<!-- This section describes the source data (e.g. news text and headlines, social media posts, translated sentences, ...). -->

For the corpus of Earlier Egyptian texts in the _TLA_, cf. the information on the [TLA text corpus](https://thesaurus-linguae-aegyptiae.de/info/text-corpus), 
notably the [PDF overview](https://nubes.bbaw.de/s/xD7MYJrmE8xNBNt).

#### Data Collection and Processing

<!-- This section describes the data collection and processing process such as data selection criteria, filtering and normalization methods, tools and libraries used, etc. -->

This dataset contains all Earlier Egyptian sentences of the TLA corpus v18 (2023) that 
- show no destruction,
- have no questionable readings,
- have hieroglyphs encoded,
- are fully lemmatized (and lemmata have a transliteration and a POS),
- have a German translation.

#### Who are the source data producers?

AV [Altägyptisches Wörterbuch](https://www.bbaw.de/forschung/altaegyptisches-woerterbuch),
AV [Wortschatz der ägyptischen Sprache](https://www.bbaw.de/en/research/vocabulary-of-the-egyptian-language);
Susanne Beck, R. Dominik Blöse, Marc Brose, Billy Böhm, Svenja Damm, Sophie Diepold, Charlotte Dietrich, Peter Dils, Frank Feder, Heinz Felber, Stefan Grunert, 
Ingelore Hafemann, Jakob Höper, Samuel Huster, Johannes Jüngling, Kay Christine Klinger, Ines Köhler, Carina Kühne-Wespi, Renata Landgráfová, Florence Langermann, 
Verena Lepper, Antonie Loeschner, Franka Milde, Lutz Popko, Miriam Rathenow, Elio Nicolas Rossetti, Jakob Schneider, Simon D. Schweitzer, Alexander Schütze, 
Lisa Seelau, Gunnar Sperveslage, Katharina Stegbauer, Doris Topmann, Günter Vittmann, Anja Weber, Daniel A. Werning.

### Annotations

<!-- If the dataset contains annotations which are not part of the initial data collection, use this section to describe them. -->

#### Annotation process

<!-- This section describes the annotation process such as annotation tools used in the process, the amount of data annotated, annotation guidelines provided to the annotators, interannotator statistics, annotation validation, etc. -->

The transliteration sometimes contains round brackets (`( )`), 
which mark phonemes added by the editor without the addition being regarded as an incorrect omission. 
For model training, the brackets, but not their content, may optionally be removed.

The hieroglyphs sometimes contain glyphs that are not yet part of Unicode (notably v15). 
These are indicated by their [code in JSesh](https://doi.org/10.5281/zenodo.5849135), with additional [codes/signs generated by the TLA project](https://github.com/thesaurus-linguae-aegyptiae/tla-jsesh-glyphs) and marked by tags `<g>`...`</g>`.

#### Who are the annotators?

<!-- This section describes the people or systems who created the annotations. -->

Susanne Beck, Marc Brose, Billy Böhm, Svenja Damm, Sophie Diepold, Charlotte Dietrich, Peter Dils, Frank Feder, Heinz Felber, Stefan Grunert, Ingelore Hafemann, 
Samuel Huster, Johannes Jüngling, Kay Christine Klinger, Ines Köhler, Carina Kühne-Wespi, Renata Landgráfová, Florence Langermann, Verena Lepper, Antonie Loeschner, 
Franka Milde, Lutz Popko, Miriam Rathenow, Elio Nicolas Rossetti, Jakob Schneider, Simon D. Schweitzer, Alexander Schütze, Lisa Seelau, Gunnar Sperveslage, 
Katharina Stegbauer, Doris Topmann, Günter Vittmann, Anja Weber, Daniel A. Werning.

#### Personal and Sensitive Information

<!-- State whether the dataset contains data that might be considered personal, sensitive, or private (e.g., data that reveals addresses, uniquely identifiable names or aliases, racial or ethnic origins, sexual orientations, religious beliefs, political opinions, financial or health data, etc.). If efforts were made to anonymize the data, describe the anonymization process. -->

No personal, sensitive, or private data.

## Bias, Risks, and Limitations

<!-- This section is meant to convey both technical and sociotechnical limitations. -->

<!-- This section is meant to convey recommendations with respect to the bias, risk, and technical limitations. -->

This is not a carefully balanced data set.

Note that the lemmatization is done via lemma IDs, since the lemma transliteration contains many consonantal homonyms due to the vowel-less nature of hieroglyphic writing. 

<!-- Users should be made aware of the risks, biases and limitations of the dataset. More information needed for further recommendations. -->

## Citation of this dataset

<!-- If there is a paper or blog post introducing the dataset, the APA and Bibtex information for that should go in this section. -->

Thesaurus Linguae Aegyptiae, Original Earlier Egyptian sentences, corpus v18, premium, https://huggingface.co/datasets/thesaurus-linguae-aegyptiae/tla-Earlier_Egyptian_original-v18-premium, 
v1.1, 2/16/2024 
ed. by Tonio Sebastian Richter & Daniel A. Werning on behalf of the Berlin-Brandenburgische Akademie der Wissenschaften and Hans-Werner Fischer-Elfert & Peter Dils on behalf of the Sächsische Akademie der Wissenschaften zu Leipzig. 

**BibTeX:**

```
@misc{tlaEarlierEgyptianOriginalV18premium,
 editor = {{Berlin-Brandenburgische Akademie der Wissenschaften} and {Sächsische Akademie der Wissenschaften zu Leipzig} and Richter, Tonio Sebastian and Werning, Daniel A. and Hans-Werner Fischer-Elfert and Peter Dils},
 year = {2024},
 title = {Thesaurus Linguae Aegyptiae, Original Earlier Egyptian sentences, corpus v18, premium},
 url = {https://huggingface.co/datasets/thesaurus-linguae-aegyptiae/tla-Earlier_Egyptian_original-v18-premium},
 location = {Berlin},
 organization = {{Berlin-Brandenburgische Akademie der Wissenschaften} and {Sächsische Akademie der Wissenschaften zu Leipzig}},
}
```

**RIS:**

```
TY  - DATA
T1  - Thesaurus Linguae Aegyptiae, Original Earlier Egyptian sentences, corpus v18, premium
PY  - 2024
Y1  - 2024
CY  - Berlin
ED  - Berlin-Brandenburgische Akademie der Wissenschaften
ED  - Richter, Tonio Sebastian
ED  - Werning, Daniel A.
ED  - Sächsische Akademie der Wissenschaften zu Leipzig
ED  - Fischer-Elfert, Hans-Werner
ED  - Dils, Peter
IN  - Berlin-Brandenburgische Akademie der Wissenschaften
IN  - Sächsische Akademie der Wissenschaften zu Leipzig
UR  - https://huggingface.co/datasets/thesaurus-linguae-aegyptiae/tla-Earlier_Egyptian_original-v18-premium
DB  - Thesaurus Linguae Aegyptiae
DP  - Akademienvorhaben "Strukturen und Transformationen des Wortschatzes der ägyptischen Sprache", Berlin-Berlin-Brandenburgischen Akademie der Wissenschaften
ER  -
```

## Glossary

<!-- If relevant, include terms and calculations in this section that can help readers understand the dataset or dataset card. -->

**Lemma IDs**

For the stable lemma IDs, see https://thesaurus-linguae-aegyptiae.de/info/lemma-lists.

**Glossing**

For the glossing abbreviations, see https://thesaurus-linguae-aegyptiae.de/listings/ling-glossings. 

_Note:_ The glosses correspond to the _inflected grammatical forms_ in the very sentence.

## Dataset Card Authors

[Daniel A. Werning](https://www.bbaw.de/die-akademie/mitarbeiterinnen-mitarbeiter/werning-daniel)

## Dataset Card Contact

[Daniel A. Werning](https://www.bbaw.de/die-akademie/mitarbeiterinnen-mitarbeiter/werning-daniel)