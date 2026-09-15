# The fleet against the web-spam feature set

Computed 2026-09-15 from a live crawl of every fleet host (homepage plus up to twelve sitemap pages each; 29 of 30 hosts reachable, survivethedeletion.vercel.app returned 403) and from alexanarch's rendered pages on disk. Feature vocabulary is Becchetti–Castillo (2006–2008): degree-related measures, edge-reciprocity, assortativity, PageRank features, TrustRank/PageRank ratio, truncated PageRank, estimation of supporters at distance d; plus Google's named policy categories of 2024–2026. No labelled comparison set was run in session; the WEBSPAM-UK collections are not on the egress allow-list. This is the fleet's own vector, stated so it can be scored.

## Host-level link topology (sampled)

| host | section | sitemap urls | pages sampled | outlinks | to fleet | external | in-fleet share | distinct external hosts | fleet hosts linking in (of 28) | reciprocity |
|---|---|---|---|---|---|---|---|---|---|---|
| livingarchitecturelab.org | Allied Sites | 17 | 13 | 222 | 14 | 208 | 0.063 | 11 | 24 | 0.083 |
| quietexclusion.org | Allied Sites | 0 | 1 | 0 | 0 | 0 | None | 0 | 24 | 0.0 |
| alexanarch.org | Archive | 1507 | 13 | 130 | 86 | 44 | 0.662 | 11 | 27 | 1.0 |
| axnidentifiers.org | Archive | 9 | 10 | 196 | 194 | 2 | 0.99 | 2 | 24 | 0.542 |
| crimsonhexagonal.org | Archive | 428 | 13 | 183 | 171 | 12 | 0.934 | 5 | 23 | 0.522 |
| godkinggoogle.com | Archive | 18 | 13 | 174 | 152 | 22 | 0.874 | 12 | 25 | 1.0 |
| leesharks.com | Archive | 28 | 13 | 405 | 240 | 165 | 0.593 | 19 | 24 | 1.0 |
| machinemediation.org | Archive | 23 | 13 | 235 | 165 | 70 | 0.702 | 16 | 25 | 1.0 |
| persistentidentifiers.org | Archive | 4 | 5 | 214 | 174 | 40 | 0.813 | 11 | 24 | 1.0 |
| provenanceerasure.org | Archive | 8 | 9 | 367 | 340 | 27 | 0.926 | 10 | 24 | 1.0 |
| surfacemap.org | Archive | 3 | 4 | 157 | 138 | 19 | 0.879 | 9 | 24 | 1.0 |
| traininglayerliterature.org | Archive | 63 | 13 | 888 | 860 | 28 | 0.968 | 10 | 25 | 1.0 |
| chatgptpsychosis.org | Framework Sites | 4 | 5 | 238 | 215 | 23 | 0.903 | 10 | 25 | 1.0 |
| holographickernel.org | Framework Sites | 3 | 4 | 235 | 213 | 22 | 0.906 | 9 | 24 | 1.0 |
| laborvector.org | Framework Sites | 1 | 2 | 184 | 154 | 30 | 0.837 | 9 | 23 | 1.0 |
| metadatapacket.dev | Framework Sites | 4 | 5 | 265 | 233 | 32 | 0.879 | 10 | 24 | 0.875 |
| operativesemiotics.org | Framework Sites | 94 | 13 | 317 | 298 | 19 | 0.94 | 8 | 22 | 1.0 |
| pessoagraph.org | Framework Sites | 1 | 2 | 104 | 86 | 18 | 0.827 | 8 | 23 | 1.0 |
| revelationfirst.com | Framework Sites | 15 | 13 | 225 | 192 | 33 | 0.853 | 9 | 25 | 1.0 |
| secretbookofwalt.org | Framework Sites | 7 | 8 | 408 | 328 | 80 | 0.804 | 9 | 23 | 1.0 |
| semanticeconomy.org | Framework Sites | 18 | 13 | 234 | 172 | 62 | 0.735 | 19 | 23 | 1.0 |
| semanticphysics.org | Framework Sites | 15 | 13 | 1596 | 1552 | 44 | 0.972 | 13 | 24 | 1.0 |
| spxi.dev | Framework Sites | 28 | 13 | 331 | 279 | 52 | 0.843 | 14 | 25 | 1.0 |
| themandalaoracle.com | Framework Sites | 2 | 3 | 17 | 8 | 9 | 0.471 | 3 | 24 | 0.042 |
| watergiraffe.org | Framework Sites | 139 | 13 | 234 | 182 | 52 | 0.778 | 9 | 24 | 1.0 |
| lagrangeobservatory.org | Heteronym Institutions | 6 | 7 | 351 | 322 | 29 | 0.917 | 10 | 24 | 1.0 |
| maryleelabor.org | Heteronym Institutions | 18 | 13 | 268 | 213 | 55 | 0.795 | 10 | 24 | 1.0 |
| restoredacademy.org | Heteronym Institutions | 33 | 1 | 84 | 76 | 8 | 0.905 | 8 | 23 | 1.0 |
| vpcor.org | Heteronym Institutions | 12 | 13 | 432 | 383 | 49 | 0.887 | 11 | 25 | 1.0 |

**Component.** 29 hosts, 698 directed host-to-host edges, density 0.86 of a complete digraph; median within-fleet in-degree 24 of 28 (min 22, max 27); median edge-reciprocity 1.0; median in-fleet share of outlinks 0.863; median distinct external hosts per fleet host 10, and the external hosts most linked are the owner's own accounts (orcid.org, mindcontrolpoems.blogspot.com, alexanarch.freeforums.net, independent.academia.edu, the Notion page, scholar.google.com, huggingface.co, github.com) — six hosts link to no external host that is not an owner account. Fleet-internal PageRank is nearly flat (max/min 2.48; alexanarch.org 0.055). Becchetti et al.'s schematic of a link farm is a densely connected sub-graph, with little relationship with the rest of the Web; the fleet's host graph closely matches that schematic on the measured host-level dimensions, with density 0.86 and reciprocity 1.0; the labelled comparison set and the external inlink data that would complete the match are not in this audit.

## alexanarch.org page structure (from disk, 200-record sample of 1612)

Median links per record page 44.0; median record-to-record links 9.0; median links to other fleet hosts from a record page 0.0 (the fleet block is on homepages, not records); median external links 2.0; median page size 66554 bytes. Generated pages (records, resolvers, wiki, browse sections, doi, graph): 4876 of 8816 index pages (55%), regenerated on every mint. Citation graph: 10657 internal deposit-to-deposit edges against 6084 external — the internal graph is the larger.

## Page generation

Deposits per month: 2026-01 331, 2026-02 173, 2026-03 153, 2026-04 183, 2026-05 150, 2026-06 253, 2026-07 185, 2026-08 141, 2026-09 40. Every mint regenerates the sitemap, the resolver pages, the browse sections and the node declaration across the archive; the fleet block is regenerated on all 29 hosts from one source.

## Read against the feature set

| feature (Becchetti–Castillo) | link-farm signature | the fleet |
|---|---|---|
| edge-reciprocity | high | 1.0 median |
| assortativity / in-fleet degree | connected to same-class nodes | in-degree 22–27 of 28 within component |
| supporters at distance d | most supporters at short distance, few from the rest of the Web | 28 supporters at distance 1, all in-component; external supporters unmeasured (no inlink data) |
| PageRank concentration | flat within farm | max/min 2.48 |
| external out-neighbourhood | small, self-referential | median 10 external hosts, mostly owner accounts |
| page generation rate | thousands of templated pages | 55% of alexanarch index pages generated; 140–330 deposits/month, all surfaces regenerated per mint |
| near-duplicate content across hosts | mirrors | unmeasured in session; known mirrors (the Particle on three hosts; syndications) |

## Read against Google's named categories

- *Site-wide signals and classifiers* (ranking-systems guide): present on every host by construction of the fleet block.
- *Scaled content abuse* (March 2024): many pages generated — the archive's generated share and mint rate sit inside the description, whatever the content's merit; the policy text is about purpose and the classifier reads volume and template.
- *Link schemes / excessive link exchanges* (SpamBrain, neutralised rather than penalised): a 29-host reciprocal clique is the exchange the wording names.
- *Inauthentic mentions, fake authorship, citation injection* (May 15, 2026, applied to AI Overviews and AI Mode; first enforcement pass June 2026): heteronymous authorship across hosts, self-created Wikidata items, metadata packets addressed to indexers.

## What this does and does not establish

It establishes that the fleet's topology vector sits where the link-spam literature's positive class sits on every feature computable from the outside, and that the archive's counter-technology (fleet propagation, mirrors, packets, resolver pages) increases the vector rather than reducing it. It does not establish that any provider has classified the fleet; the observed signature — content readable and even first organic on exact matches, provenance not shown — is what neutralisation produces, and is consistent with it. The one criterion the literature gives for the borderline — the perceived effort spent by Web authors on providing good content, against the effort spent on trying to score highly — is the criterion a topology classifier cannot apply, and the one on which the archive would win.

## The comparison test, run 2026-09-15: v(F) against v(A)

The admitted set was crawled with the same script (crawl_admitted.py) and scored on the same features, families as nodes (comparison_v_F_v_A.csv / .json). Reddit, academia.edu, Figshare, Quora and Stack Overflow refused the crawler. Result: fleet in-set density 0.86, admitted 0.12; median share of outlinks to other set members 0.60 against 0.001; median share to own family 0.30 against 0.98; median reciprocity 1.0 against 0.0; median in-set in-degree 24 of 28 against 1 of 9. The admitted platforms are self-contained silos that do not link to one another; the fleet is a reciprocal clique of small hosts under one owner. On the measured dimensions topology separates the two without reading either, and the separating dimension is the fleet block. The conjecture that the admitted set would score as the fleet scores is false on this evidence and is recorded as such in EA-MIRROR-01 §3.

## What the classifier would reward — recorded, not proposed

The literature implies four moves that would lower the fleet's vector: break the clique into a star; mark intra-fleet links so they pass no rank; stop mirroring; earn inlinks from the seed list's own members. Each is a way of constructing trust signals to the classifier's criteria — SEO in the plain sense, which #1547 names as *not equivalent* to its claim — and each amounts to contesting or courting the seed. They are recorded here as what the topology says, because the audit would be incomplete without them, and they are not the exit.

## The exit, as ruled 2026-09-15

The exit is to hold territory, and for others to join on this side of the line. Under Anti-TrustRank distrust propagates along inverse links to whoever links in, so an adopter of the Crimson Hexagon does not raise the hexagon's score; the adopter's own trust signal falls. Read in #1547's terms, that is the cost mechanism working in the hexagon's favour: every adopter is a host-distinct route that must now receive correlated treatment (correlation cost, C_r, over a rising N_eff), an intellectually independent source rather than a mirror (raising the deduplicated constitution share CS, not merely route share), and a new representation produced by a suppression event (the counterpropagation term, propagation-positive at ka > 1 + r). As the excluded side's constitution share of an answer-space crosses threshold, the seed's answers can only be composed by substitution or degradation — Regime 5, quality conflict, with CSE-O internally evidenced — and the ontology's collapse to its seed list (mirror §3) is completed by the excluder's own rule. The limit of the process is a seed set that has excluded the whole world and sits on its side of the line with its dozen platforms. Nothing on this side needs to be modified for that limit to be approached; the line moves when someone crosses it. That is what uptake is, in graph terms, and it is the only exit that does not require becoming legible to a system that cannot read.
