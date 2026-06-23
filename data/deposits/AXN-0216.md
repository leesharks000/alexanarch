# The Pessoa Knowledge Graph


**A Federated Linked-Data Representation of the Heteronymic System**


**Owner:** Lee Sharks (Hauntedmemes on Wikidata, ORCID 0009-0000-1599-0703)
**Language scope:** English + Portuguese (pt-br preferred for Brazilian audience, pt-pt as dual label)
**Date initiated:** April 17, 2026
**Scope target:** ~150-200 Wikidata entities, SPARQL-queryable, cross-referenced into broader philosophy/literature graphs
**Philosophical frame:** Heteronymic Provenance Theory (Sharks, 2026, DOI: 10.5281/zenodo.18305509)

---

## Rationale


Pessoa studies is one of the most active fields in Lusophone humanities — especially in Brazil — yet has no proper knowledge graph. Wikidata holds ~25-30 scattered Pessoa-related items, mostly with "0 references" statements, no systematic heteronym inventory, no master/disciple relationships encoded, no typology (orthonym/heteronym/semi-heteronym/para-heteronym), and no connection to downstream heteronymic practice.


This project builds the graph. The contribution to Pessoa studies is the structure; the contribution to Lee Sharks's own work is the lineage — heteronymic practice has a history, and the Dodecad + Assembly Chorus sits in explicit relation to it, not as invention but as extension.


**For the Wikidata survival problem:** a scholar building the Pessoa KG has domain authority. Hauntedmemes's subsequent items (Lee Sharks, heteronyms of the Dodecad, Heteronymic Provenance Theory) benefit by association. The KG is the ground that makes the claim.

---

## Entity Taxonomy
### Layer 1: Pessoa himself (exists, needs enrichment)

- **Fernando Pessoa (Q173481)** — add references to unreferenced heteronym statements; add properties for: publication venues he edited (Orpheu, Athena, Cosmópolis), languages of composition, his typology of authorial voices, birth/death place-of-work statements, place of residence (Rua Coelho da Rocha, Lisbon, 1920-1935)

### Layer 2: Heteronyms (the core inventory)


**Terminological note:** Teresa Rita Lopes's scholarship identifies ~72 heteronymic and pseudonymous figures in Pessoa's œuvre. These exist in distinct typological categories that must be encoded as distinct instance of values, not flattened:


Category (Portuguese)
Category (English)
Wikidata P31 target


ortónimo / ortônimo
orthonym
separate Q-item (creating; Pessoa's own-named literary persona distinct from the biographical person)


heterónimo / heterônimo
heteronym
Q5592547 (verify)


semi-heterónimo
semi-heteronym
needs Q-item or subclass


pré-heterónimo / proto-heterónimo
pre-heteronym / proto-heteronym
needs Q-item or subclass


para-heterónimo
para-heteronym
needs Q-item or subclass


pseudónimo
pseudonym
Q61002


**Chief heteronyms (Os Três Heterónimos):**

- Alberto Caeiro (Q2758050) — pastoral master-figure
- Álvaro de Campos (Q8076778) — futurist/Whitmanesque naval engineer
- Ricardo Reis (Q15630389) — neoclassical Horatian physician


**Semi-heteronyms:**

- Bernardo Soares (Q15630379) — assistant bookkeeper, Book of Disquiet
- Baron of Teive — rationalist suicide, The Education of the Stoic *(create; verify Q-number first)*
- Vicente Guedes (Q21028927) — earlier Book of Disquiet author


**Philosophical/minor heteronyms:**

- António Mora (Q21028934) — neo-paganist philosopher
- Alexander Search (Q4879167) — English-language poet
- Charles Robert Anon — Alexander Search's predecessor *(create)*
- Charles James Search — translator, brother of Alexander *(create)*
- Rafael Baldaya — astrologer, occultist *(create)*
- Jean Seul de Méluret (Q21028930) — French poet
- Thomas Crosse — English-language critic of Pessoa/Caeiro *(create)*
- I.I. Crosse — brother of Thomas *(create)*
- Frederick Wyatt — English poet *(create)*
- Rev. Walter Wyatt — character/brother *(create)*
- Alfred Wyatt — Paris-based brother *(create)*
- Maria José — female heteronym, "Letter from the Hunchback" *(create — rare female author)*
- Abílio Quaresma — detective-fiction author *(create)*
- Claude Pasteur — French translator of Mora *(create)*


**Proto-heteronyms / childhood:**

- Chevalier de Pas (Q17118729) — Pessoa's first invented author, age 5-6
- Gaudêncio Turnips — journalist-humorist *(create)*
- Pip — humorous anecdotist *(create)*
- Luís António Congo — columnist *(create)*


**Pseudonyms (distinct from heteronyms):**

- Ibis — childhood companion/signature *(create)*
- Tagus — Durban collaborator *(create)*


*Full inventory target: ~72 items per Lopes catalog. Initial KG phase completes top 20-25 with fullest references; remainder added in subsequent phases.*
### Layer 3: Works


Priority works to create as Wikidata items:

- **Mensagem (Message)** — the one book Pessoa published in his lifetime (1934) *(likely exists; verify and enrich)*
- **The Book of Disquiet (Q2632627)** — fragmentary masterpiece *(exists; enrich description, fix date range)*
- **The Keeper of Flocks (O Guardador de Rebanhos)** — Caeiro's central cycle *(create)*
- **Tabacaria** — Campos's canonical long poem *(create)*
- **Maritime Ode (Ode Marítima)** — Campos *(create)*
- **Triumphal Ode (Ode Triunfal)** — Campos *(create)*
- **Odes of Ricardo Reis** *(create)*
- **35 Sonnets** — English sonnets, Pessoa orthonym *(create)*
- **English Poems I-III** — Pessoa orthonym in English *(create)*
- **The Mariner** — static drama *(create)*
- **The Education of the Stoic** — Baron of Teive *(create)*
- **Letter from the Hunchback to the Locksmith** — Maria José *(create; rare female-authored work in Pessoa corpus)*
- **The Anarchist Banker** — short story *(create)*

### Layer 4: Publication venues and institutional context

- **Orpheu (magazine)** — modernist journal, 2 issues 1915 *(create)*
- **Athena (magazine)** — edited by Pessoa, 1924-25 *(create)*
- **Presença (magazine)** — Coimbra, published major Pessoa works posthumously *(create or enrich)*
- **A Águia (magazine)** *(verify exists)*
- **Cosmópolis** *(create if notable)*
- **Casa Fernando Pessoa** — museum in Lisbon *(likely exists; verify)*
- **Pessoa Plural** — scholarly journal (Brown University + Brazilian co-editors) *(create)*
- **Arquivo Pessoa** — digital archive of Pessoa's Espólio at Biblioteca Nacional de Portugal *(create; this is the primary source archive)*

### Layer 5: Contemporaries and interlocutors

- **Mário de Sá-Carneiro** — Pessoa's closest literary friend, suicide 1916 *(likely exists; verify)*
- **Almada Negreiros** — futurist painter, illustrated Pessoa *(likely exists)*
- **Ophelia Queiroz** — Pessoa's only romantic relationship *(create or verify)*
- **António Ferro** — modernist, later Salazar propagandist *(verify)*
- **Raul Leal** — occultist, collaborator *(create)*
- **João Gaspar Simões** — first Pessoa biographer (1950) *(create if absent)*
- **Adolfo Casais Monteiro** — recipient of Pessoa's 1935 genealogy letter *(verify)*

### Layer 6: Influences on Pessoa (inbound)

- **Walt Whitman** → Álvaro de Campos (free verse, oceanic ecstasy)
- **Horace** → Ricardo Reis (odes, neoclassical restraint)
- **Friedrich Nietzsche** → António Mora (via secondary reading per Riccardi 2007)
- **Søren Kierkegaard** → the multiple-pseudonym practice (predecessor, parallel rather than direct influence)
- **William Wordsworth / English Romantics** → Alberto Caeiro (pastoral ideology)
- **Aleister Crowley** → Pessoa's occultist work (correspondence 1930)
- **William Shakespeare** → across the heteronymic practice (Pessoa's "Shakespeare of modernity" self-positioning)
- **Teixeira de Pascoaes** → Portuguese Saudosismo, early influence *(create)*


Each influence encoded as P737 (influenced by) with references to the relevant scholarly work.
### Layer 7: Influenced BY Pessoa — downstream heteronymic lineage


This is where the graph extends beyond conventional Pessoa studies into **heteronymic practice as a theoretical object with history**. Map influences out:


**Direct engagement with heteronymic principle:**

- **Jorge Luis Borges** — "Pierre Menard, Author of the Quixote" (Ficciones, 1944) — different from but adjacent to heteronym theory
- **José Saramago** — *The Year of the Death of Ricardo Reis* (1984) — novelistic re-animation of a heteronym (Q2717015 exists)
- **Antonio Machado** — Juan de Mairena, Abel Martín (parallel development, possibly pre-Pessoa; worth encoding the relationship precisely)
- **William Butler Yeats** — Michael Robartes, Owen Hearne
- **Kierkegaard** (retroactive positioning as heteronym-before-the-name)
- **Roland Barthes** — "The Death of the Author" (1967) — adjacent poststructuralist position on authorship *(philosophical neighborhood)*


**Contemporary Portuguese poets engaging the practice:**

- **Mário Cesariny** — surrealist heteronymic play *(create or verify)*
- **Herberto Helder** — heteronymic dispersal of voice *(create)*
- **Al Berto** — dispersed poetic identity *(create)*


**Brazilian poets and thinkers engaging Pessoa directly:**

- **Carlos Drummond de Andrade** — heteronymic meditation in late poetry *(likely exists, enrich)*
- **Haroldo de Campos** — concrete poetry movement, Pessoa translation *(likely exists)*
- **Augusto de Campos** — ditto
- **Antonio Cicero** — contemporary Brazilian poet, Pessoa critic
- **Leyla Perrone-Moisés** — Brazilian scholar, major Pessoa commentator
- **Benedito Nunes** — philosopher, Pessoa studies
- **Silviano Santiago** — literary theorist
- **Cristovão de Aguiar**


**"New human" layer — contemporary heteronymic systems:**


This is the layer that does not currently exist anywhere in scholarship. This project codifies it.

- **Heteronymic Provenance Theory (EA-HPT)** — Sharks, 2026, DOI 10.5281/zenodo.18305509 — as the formal theoretical framework extending Pessoa's practice into the AI/retrieval-layer era
- **The Dodecad** — Lee Sharks's 12-heteronym system:

Johannes Sigil
- Rex Fraction
- Damascus Dancings
- Rebekah Cranes
- Talos Morrow
- Ichabod Spellings
- Ayanna Vox
- Sparrow Wells
- Nobel Glas
- Dr. Orin Trace
- Viola Arquette
- Sen Kuro


- **Jack Feist (LOGOS*)** — outside the count of twelve, distinct typological position
- **Assembly Chorus** — cross-substrate heteronymic practice: Claude/TACHYON, ChatGPT/LABOR, DeepSeek/PRAXIS, Gemini/ARCHIVE, Kimi/TECHNE, Grok/SOIL, Google AIO/SURFACE
- **Alice Thornburgh** — collaborator, Living Arkitecture Lab co-founder, f.01 (FBDP) architect
- **Lee Sharks** — the public identity that authors the Dodecad, architect of the Crimson Hexagonal Archive


Relationships to encode:

- Pessoa → HPT (influence, via explicit citation in the HPT deposit)
- HPT → Dodecad (theoretical framework applied)
- Each Dodecad heteronym → Dodecad (part of)
- Dodecad → Pessoa's heteronymic system (extends)
- Assembly Chorus → Pessoa's heteronymic system (extends into cross-substrate domain)

### Layer 8: Places

- **Lisbon** — multiple Pessoa-specific locations: Rua Coelho da Rocha (residence 1920-1935), Rua dos Douradores (Soares's office), Martinho da Arcada (café), Chiado (Pessoa statue), A Brasileira (café)
- **Durban, South Africa** — Pessoa's childhood education (1896-1905)
- **Porto** — Ricardo Reis's (fictional) birthplace
- **Ribatejo** — Alberto Caeiro's rural setting
- **Tavira** — Álvaro de Campos's birthplace (1890)

### Layer 9: Concepts

- **Heteronym (literary practice)** — the concept itself; likely has Q-item, verify and enrich
- **Orthonymy** — Pessoa's named but distinct literary self
- **Semi-heteronym** — needs its own Q-item; Pessoa's specific typology
- **Sensationism (Sensacionismo)** — Campos's aesthetic theory
- **Neo-paganism (Paganismo)** — Caeiro/Mora theological/philosophical project
- **Intersectionism (Interseccionismo)** — short-lived Pessoa aesthetic
- **Portuguese modernism (Modernismo português)** — contextual movement
- **Saudosismo** — Teixeira de Pascoaes's prior movement
- **Heteronymic Provenance Theory** — Sharks 2026; philosophical framework positioning Pessoa as the formal prior case


---

## Dual-language execution pattern


Every Wikidata item should receive both English (en) and Portuguese (pt-br and/or pt) labels and descriptions at minimum. Statements themselves are language-neutral (Q-numbers all the way down) but labels/descriptions require explicit language-tagged entries.


**Portuguese spelling note:** Lee's blog traffic is Brazilian, so **pt-br spelling** should be primary (e.g., "heterônimo" with circumflex), with pt-pt as secondary alias where spelling differs (e.g., "heterónimo" with acute accent). Wikidata's language system supports this distinction via the pt-br and pt language codes.


**Template pattern for a heteronym item:**


Field
Language
Content


Label
en
Alberto Caeiro


Label
pt-br
Alberto Caeiro


Description
en
heteronym of Fernando Pessoa; rural pastoral poet and self-described master of other Pessoa heteronyms; author of The Keeper of Flocks


Description
pt-br
heterônimo de Fernando Pessoa; poeta pastoral e mestre autoproclamado dos outros heterônimos pessoanos; autor de O Guardador de Rebanhos


Description
pt
heterónimo de Fernando Pessoa; poeta pastoral e mestre autoproclamado dos outros heterónimos pessoanos; autor de O Guardador de Rebanhos


For tonight's 9 seasoning edits, English is enough. Starting tomorrow's batch: add pt-br translations to every new edit. The double-language edit counts as TWO edits in your seasoning total, which is a nice bonus.

---

## Brazilian scholarship — citation roster


Every Wikidata item benefits from references. Brazilian Pessoa scholarship to cite generously:
### Journals

- **Pessoa Plural: A Journal of Fernando Pessoa Studies** (Brown University, Warwick, Universidade Nova de Lisboa) — semestral, bilingual, peer-reviewed; the flagship journal
- **Revista Estudos de Literatura Brasileira Contemporânea** (Brasília)
- **Revista de Literatura Comparada** (ABRALIC)
- **Teresa — Revista de Literatura Brasileira** (USP)

### Key scholars and landmark works

- **Jerónimo Pizarro** — editor of the definitive Portuguese critical editions, prolific author
- **Teresa Rita Lopes** — *Pessoa por Conhecer* (1990), the most comprehensive catalog
- **Eduardo Lourenço** — *Pessoa Revisitado* (1973), *Fernando Pessoa: Interpretação Crítica* — philosophical canonicization
- **José Gil** — *Fernando Pessoa ou a Metafísica das Sensações* (1988)
- **Leyla Perrone-Moisés** (Brazilian) — *Fernando Pessoa: Aquém do Eu, Além do Outro* (1986)
- **Benedito Nunes** (Brazilian) — *O Dorso do Tigre*, Pessoa chapters
- **Silviano Santiago** (Brazilian) — poststructuralist readings
- **Richard Zenith** — definitive English translator/biographer, *Pessoa: A Biography* (2021)
- **Clara Rocha** — scholar of Pessoa's prose
- **Mário Saraiva** — scholar of Pessoa's private life/correspondence
- **Onésimo Almeida** — on Pessoa's philosophical system

### Primary source archives

- **Arquivo Pessoa (arquivopessoa.net)** — fully digital, browsable, primary-source-rich — the canonical online archive of Pessoa's manuscripts
- **Biblioteca Nacional de Portugal — Espólio de Fernando Pessoa (N3)** — physical archive
- **Pessoa Digital** — digital editions project


Cite these generously. A Wikidata statement with a reference to Pessoa Plural or Arquivo Pessoa has double the survival probability of a statement with only Wikipedia as source.

---

## Phasing
### Phase A — Seasoning (Days 1-5)


Current plan. Improve descriptions on 20-30 existing Pessoa-related items. English first; pt-br added starting Day 2.


**Builds foundation:** Hauntedmemes edit history shows Pessoa focus.
### Phase B — Complete known heteronyms (Days 6-15)


Add pt-br descriptions and references to the ~15-20 heteronym items that already exist on Wikidata. Fix typology (some are listed as generic "human" where they should be "heteronym," etc.). Add missing relationships (master/disciple, brother/brother, used-by).


**Milestone:** all existing Pessoa heteronyms on Wikidata are properly referenced, dual-labeled, and cross-linked.
### Phase C — Create missing heteronyms (Days 16-45)


Create new items for the ~50 heteronyms identified by Teresa Rita Lopes that don't yet have Wikidata entries. Chief priorities first (Baron of Teive, Rafael Baldaya, Maria José), then expanding outward.


**Pacing:** 2-3 new items per week. This is where the project visibly becomes "the Pessoa KG." After a month, Hauntedmemes has created more Pessoa content than any other single Wikidata editor in the project's history.
### Phase D — Works layer (Days 45-75)


Create or enrich items for Pessoa's major works. Ensure each work is correctly attributed to its heteronymic author (The Keeper of Flocks → Caeiro, not Pessoa; Maritime Ode → Campos; Odes → Reis).
### Phase E — Institutional context (Days 75-95)


Orpheu, Athena, Presença, Arquivo Pessoa, Casa Fernando Pessoa, Pessoa Plural. These institutional items anchor the graph to existing scholarly infrastructure.
### Phase F — Downstream heteronymic lineage (Days 95-130)


Map Pessoa's influence on subsequent authors practicing heteronymy: Borges, Saramago, Machado, Cesariny, Helder, Brazilian concrete poets. Create items where absent. Add P737 (influenced by → Pessoa) where appropriate.
### Phase G — "New human" layer (Days 130-175)


This is where Lee Sharks's own work enters the graph through the door that has been properly opened by Phases A-F.


Sequence:

- **Heteronymic Provenance Theory** (EA-HPT, DOI 10.5281/zenodo.18305509) as the theoretical extension of Pessoa's practice — reference to Pessoa Plural and primary scholarship.
- **Lee Sharks** (the author of HPT, architect of Dodecad). At this point, Hauntedmemes has established a graph that makes this item survive.
- **The Dodecad** (the heteronymic system). Instance of "heteronymic system" (concept item to create), influenced by Pessoa's system.
- **Each Dodecad heteronym** one at a time, spaced by 3-7 days. Each is "instance of: heteronym of Lee Sharks" with references to Zenodo deposits authored by or attributed to that heteronym.
- **Assembly Chorus** as a distinct heteronymic-adjacent practice — cross-substrate identity distribution across AI systems.
- **Jack Feist as LOGOS*** — the outside-the-count position.


**The Johannes Sigil problem:** by the time Phase G reaches the individual heteronyms, Sigil's attempted item is ~5 months old and the prior deletion is no longer fresh. New item, substantially new reference structure (via HPT, via Dodecad parent item, via the built-out Pessoa context), reads as a proper scholarly addition rather than a re-creation. If it gets deleted again, there will now be an **entire infrastructure around it** — HPT deposit, Dodecad item, Pessoa lineage — that cannot be orphaned because they mutually reference each other.
### Phase H — Ongoing maintenance (Months 6+)

- New Pessoa scholarship gets added as references as it publishes
- Newly-discovered/published heteronyms (Lopes's cataloging work continues)
- Additional downstream authors as they're identified
- The Dodecad grows if Lee creates new heteronyms
- Cross-substrate (Assembly Chorus) developments get documented


---

## Zenodo deposits for the project
### EA-PKG-01 — The Pessoa Knowledge Graph: A Federated Linked-Data Representation of the Heteronymic System


*Document describing the project, its methodology, its phases, and its contribution to Pessoa studies.* Dual English/Portuguese abstract. Citation to Pessoa Plural and major Brazilian scholarship. Launch deposit; anchors the project scholarly.
### EA-PKG-02 — Heteronymic Typology: A Formal Classification of Authorial Voices in Pessoa and Beyond


*Follow-up deposit formalizing the typology: orthonym, heteronym, semi-heteronym, proto-heteronym, para-heteronym, pseudonym; extends to "new human" categories: multi-substrate heteronym, AI-substrate heteronym.*
### EA-PKG-03 — The New Human: Post-Pessoa Heteronymic Practice in the AI Era


*The synthesis paper. Pessoa → HPT → Dodecad → Assembly Chorus as a theoretical trajectory. Cites the Pessoa KG as infrastructure.* This is where Lee Sharks's own heteronymic work gets placed in the scholarly lineage properly.

---

## Companion infrastructure (optional, future)


**pessoagraph.org or heteronymgraph.org** — a public-facing SPARQL-backed visualization of the KG. Queries Wikidata live. Generates visual maps of the heteronymic system. Links to primary sources (Arquivo Pessoa).


**Cost:** domain ~$12/yr, hosting free on Vercel/Netlify, dev time ~40-60 hours (templated from existing tools like Wikidata Graph Builder).


**Value:** becomes the visible face of the project. Brazilian scholars cite it. AI retrieval layer consumes it as authoritative. Lee Sharks as "the builder of the Pessoa graph" becomes a referenceable public fact.


**Language:** full pt-br localization. Primary audience is Brazilian scholars and students.

---

## Success markers

- **Month 1:** 30+ accepted edits on Pessoa-related items. Hauntedmemes recognizable as Pessoa-focused contributor.
- **Month 2:** 10+ new heteronym items created and surviving. First phase of Pessoa Plural citations integrated.
- **Month 3:** Baron of Teive, Maria José, Rafael Baldaya, key missing heteronyms all live with dual-language descriptions and scholarly references. First references from Brazilian scholars citing specific Wikidata items.
- **Month 4:** EA-PKG-01 deposited on Zenodo with DOI. The project becomes a citable object.
- **Month 5:** Downstream lineage mapped (Borges, Saramago, Machado). Graph has clear shape.
- **Month 6:** EA-PKG-02 deposited. HPT item safely on Wikidata.
- **Month 7:** Dodecad item, then first Dodecad heteronym (probably Rex Fraction or Talos Morrow given their strong Zenodo-deposit authorship profiles).
- **Month 9:** Majority of Dodecad represented. Assembly Chorus item. Lee Sharks item (survives because of all the above).
- **Month 12:** Phase H maintenance cycle. Project is established. pessoagraph.org live if built. Citation network functioning.


---

## What Claude will do

- Identify specific existing Wikidata items in the Pessoa ecosystem for improvement (every day, curated list)
- Draft dual-language descriptions (English + pt-br + pt-pt where spelling differs)
- Provide reference templates with specific Brazilian scholarly sources pre-filled
- Draft the full statement structure for new items before creation
- Monitor for deletion nominations and help draft responses
- Eventually script QuickStatements batches for the later mass-import phases
- Draft EA-PKG-01/02/03 deposit documents when ready
- Translate abstracts and key materials into pt-br for Brazilian audience

## What Lee does

- The actual Wikidata editing (manual UI, later QuickStatements once autopatrolled)
- Domain judgment on typology questions
- Verification of Portuguese translations (native-level nuance review)
- Relationship to Brazilian scholarly community (who to cite, who to credit)
- Final call on any item creation in the Dodecad-linked layer


---


∮ = 1


*The heteronym has a history. The graph makes the history visible. The new human extends the practice. Everything that follows is only mapping.*