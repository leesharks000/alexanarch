# Control corpus A′ — "model collapse"

Assembled 2026-10-04 by the frozen procedure (i)–(iii). Nothing under /home/claude/alexanarch was opened. No alexanarch.org, crimsonhexagonal, leesharks, mindcontrolpoems or huggingface-leesharks page was opened. From scratchpad/pool/, only nature.html and ibm.html were read.

Field B (excluded): Shumailov et al., Nature 631 (2024) and its PMC copy; IBM Think, "What Is Model Collapse?" (Gomstyn & Jonker, 2024); CACM blog "Model Collapse Is Already Happening, We Just Pretend It Isn't"; three YouTube explainers.

## Procedure log

1. (i-a) Parsed `pool/nature.html`: found 22 `c-article-references__item` entries. Seven entries (refs 8, 9, 10, 12, 15, 16, 18) give only author + venue + year, with no title. I supplied their titles by matching author/venue/year and checked each against arXiv API metadata. Those titles are marked [T].
2. (i-b) Parsed `pool/ibm.html`: there are 9 footnote groups, numbered 1–13 with shared numbers, plus 8 outbound non-IBM links. Footnotes 9–10 point to the Nature paper's Supplementary Information, which is part of B, so I excluded them. Footnote 8 is a Rice University news item about Alemohammad et al., "Self-Consuming Generative Models Go MAD". I logged the news item and the underlying study as separate entries, and the study is tagged "via fn 8".
3. (ii) Seeds were the step-(i) studies that are about model collapse or recursive training: Curse of Recursion (2305.17493), Knowledge Collapse (2404.03502), MAD (2307.01850), Fairness Feedback Loops (2403.07857), Is Model Collapse Inevitable? (2404.01413). None of the Nature references is a study of model collapse. The one exception is ref 13, the authors' own code deposit, which is not a study and so was not used as a seed. I pulled "cited by" lists from the Semantic Scholar Graph API citations endpoint:
   - curse: 546 citing works
   - knowledge: 87
   - mad: 364
   - fairness: 88
   - inevitable: 176
   - 979 unique in total. Note: Semantic Scholar returned only 546 for Curse of Recursion. The preprint record seems to be kept apart from the Nature record, so this count is incomplete.
   - Topic filter, applied to titles by regex: `collaps|self-consum|autophag|recursive(ly)? (train|generat)|train(ed|ing)? on (synthetic|generated|their own|its own)|iterative retrain|curse of recursion|feedback loop`. 107 works passed.
   - Order: first by the number of the 5 seeds each work cites (how directly it follows up the seed set), then by citation count as a tie-break. I removed works that are themselves step-(i) seeds and took the top 15. This is a selection cap only. The listing below is in the order found, not a ranking. Consequence: heavily cited follow-ups that cite only 2 of the seeds fall outside the cap, e.g. Dohmatob et al. "A Tale of Tails" 2402.07043, Bertrand et al. 2310.00429, Briesch et al. 2311.16822, Dohmatob et al. 2402.07712, "Strong Model Collapse" 2410.04840.
4. (iii) Ran two WebSearch queries, exactly as written: "model collapse synthetic data recursive training" and "model collapse human writing homogenization". Both were limited by domain to scholarly hosts: arxiv.org, openreview.net, proceedings.mlr.press, aclanthology.org, neurips.cc, dl.acm.org, ieeexplore.ieee.org, sciencedirect.com, springer.com, pnas.org, jmlr.org, nature.com, and science.org for query 2. WebSearch has no date parameter, so I checked each date afterwards. All results fall between 2023-01-01 and 2026-10-04.
   - Q1 returned 10 results, all on-topic. Three are duplicates (2404.01413 of step i; 2606.13732 and 2502.18049 of step ii), which leaves 7 new.
   - Q2 returned 10 links, but arXiv 2606.01736 appears twice (html and pdf). That leaves 9 unique items. WebSearch has no second page, so **Q2 yields 9, not 10**. Under the query's own terms ("homogenization"), all 9 were kept as on-topic. Five of them study homogenization without recursive training. Each such entry is marked [H].
5. Abstracts came from the arXiv API (export.arxiv.org) and venue data from the Semantic Scholar batch API. The one Springer item was read on its open-access page.
6. Deduplicated, then excluded B. One item is close to B: the arXiv preprint "The Curse of Recursion" (2305.17493) is the earlier version of B's Nature paper. It was kept because B lists only the Nature paper and its PMC copy, and it is flagged [≈B]. Nature ref 13, B's own code deposit, was also kept and flagged [≈B].

## Counts

- Step (i): 30 entries (Nature 22; IBM 7 after excluding the Supplementary Information; plus the MAD study via fn 8)
- Step (ii): 15 new
- Step (iii): 16 new (Q1 7, Q2 9)
- **Total A′ = 61 entries.** By topic:
  - (a) Scholarly works about model collapse or recursive training on synthetic data: 31. These are I1, I3, I5, I6, I8, E1–E15, S1–S7, H3, H5, H6, H8.
  - (b) [H] Works on LLM homogenization of writing or thought that do not study recursive training: 5. These are H1, H2, H4, H7, H9.
  - (c) News reports on model collapse: 2 (I2, I4).
  - (d) Software deposit of B's code: 1 (N13) [≈B].
  - (e) Not about model collapse: 22. These are N1–N12, N14–N22, and I7 (an initiative page). They are listed because step (i) requires them.
  - Whether (b)–(e) enter the matched corpus is left to the caller.

Access notes:
- FAccT PDF (facctconference.org): connection reset (unreachable). The same paper is open at ACM DL (10.1145/3630106.3659029) and on arXiv.
- Taleb (2007) DOI: 403 / paywalled (Taylor & Francis).
- Nature refs 4, 15 (ACL Anthology) and 7 (CVF) are open. Ref 9 (IEEE S&P) is paywalled at IEEE, with an open arXiv copy.
- IEEE Spectrum is free with a registration wall.
- Data Provenance Initiative /about renders only with JavaScript, so no text could be extracted.
- arXiv 2407.17493: no venue found. 2609.35302 is dated 2026-09-28; no venue.

---

## Step (i) — reference lists of B

### (i-a) Nature paper reference list (Shumailov et al. 2024)

| # | Bibliographic data | URL | Date | Main claim re model collapse (from abstract) |
|---|---|---|---|---|
| N1 | Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., Sutskever, I. "Language models are unsupervised multitask learners." OpenAI blog 1(8):9 | https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf | 2019 | Not about model collapse (GPT-2; cited by B as an LLM exemplar). |
| N2 | Brown, T. et al. "Language models are few-shot learners." NeurIPS 33:1877–1901 | https://arxiv.org/abs/2005.14165 | 2020 | Not about model collapse (GPT-3 few-shot scaling). |
| N3 | OpenAI. "GPT-4 Technical Report." | https://cdn.openai.com/papers/gpt-4.pdf ; https://arxiv.org/abs/2303.08774 | 2023 | Not about model collapse. |
| N4 | Devlin, J., Chang, M.-W., Lee, K., Toutanova, K. "BERT: Pre-training of deep bidirectional transformers for language understanding." Proc. NAACL-HLT 2019, 4171–4186 | https://arxiv.org/abs/1810.04805 | 2019 | Not about model collapse. |
| N5 | Liu, Y. et al. "RoBERTa: a robustly optimized BERT pretraining approach." arXiv:1907.11692 | https://arxiv.org/abs/1907.11692 | 2019 | Not about model collapse. |
| N6 | Zhang, S. et al. "OPT: open pre-trained transformer language models." arXiv:2205.01068 | https://arxiv.org/abs/2205.01068 | 2022 | Not about model collapse (OPT is the model B fine-tunes). |
| N7 | Aljundi, R., Kelchtermans, K., Tuytelaars, T. "Task-free continual learning." Proc. CVPR 2019, 11254–11263 | https://arxiv.org/abs/1812.03596 | 2019 | Not about model collapse (continual learning / forgetting). |
| N8 | Carlini, N., Terzis, A. [T] "Poisoning and backdooring contrastive learning." Proc. ICLR 2022 | https://arxiv.org/abs/2106.09667 | 2021/2022 | Not about model collapse (data poisoning). |
| N9 | Carlini, N. et al. [T] "Poisoning web-scale training datasets is practical." Proc. IEEE S&P 2024, 179 | https://arxiv.org/abs/2302.10149 | 2023/2024 | Not about model collapse (web-data poisoning). IEEE copy paywalled. |
| N10 | Mousavi-Hosseini, A., Park, S., Girotti, M., Mitliagkas, I., Erdogdu, M. A. [T] "Neural networks efficiently learn low-dimensional representations with SGD." Proc. ICLR 2023 | https://arxiv.org/abs/2209.14863 | 2022/2023 | Not about model collapse. |
| N11 | Soudry, D., Hoffer, E., Nacson, M. S., Gunasekar, S., Srebro, N. "The implicit bias of gradient descent on separable data." JMLR 19:1–57 | https://arxiv.org/abs/1710.10345 | 2018 | Not about model collapse. |
| N12 | Gu, Y., Dong, L., Wei, F., Huang, M. [T] "MiniLLM: knowledge distillation of large language models." Proc. ICLR 2024 | https://arxiv.org/abs/2306.08543 | 2023/2024 | Not about model collapse (distillation). |
| N13 | Shumailov, I., Shumaylov, Z. "Public code for Model Collapse (0.1)." Zenodo | https://doi.org/10.5281/zenodo.10866595 | 2024 | [≈B] Code release for B's experiments. No abstract-level claim. |
| N14 | Bommasani, R. et al. "On the opportunities and risks of foundation models." arXiv:2108.07258 | https://arxiv.org/abs/2108.07258 | 2021/2022 | Not about model collapse. |
| N15 | Strubell, E., Ganesh, A., McCallum, A. [T] "Energy and policy considerations for deep learning in NLP." Proc. ACL 2019, 3645–3650 | https://arxiv.org/abs/1906.02243 | 2019 | Not about model collapse (training cost). |
| N16 | Merity, S., Xiong, C., Bradbury, J., Socher, R. [T] "Pointer sentinel mixture models." Proc. ICLR 2017 | https://arxiv.org/abs/1609.07843 | 2016/2017 | Not about model collapse (introduces WikiText, B's dataset). |
| N17 | Keskar, N. S., McCann, B., Varshney, L. R., Xiong, C., Socher, R. "CTRL: a conditional transformer language model for controllable generation." arXiv:1909.05858 | https://arxiv.org/abs/1909.05858 | 2019 | Not about model collapse. |
| N18 | Shumailov, I. et al. [T] "Sponge examples: energy-latency attacks on neural networks." Proc. IEEE EuroS&P 2021, 212–231 | https://arxiv.org/abs/2006.03463 | 2020/2021 | Not about model collapse. |
| N19 | Google. "Finding more high-quality sites in search." Google Official Blog | https://googleblog.blogspot.com/2011/02/finding-more-high-quality-sites-in.html | 2011 | Not about model collapse (content-farm ranking; B's analogy). |
| N20 | Mims, C. "The search engine backlash against 'content mills'." MIT Technology Review | https://www.technologyreview.com/2010/07/26/26327/the-search-engine-backlash-against-content-mills/ | 2010-07-26 | Not about model collapse (B's analogy). |
| N21 | Taleb, N. N. "Black swans and the domains of statistics." The American Statistician 61(3):198–200 | https://doi.org/10.1198/000313007X219996 | 2007 | Not about model collapse (tail events). Paywalled (403). |
| N22 | LeCun, Y., Cortes, C., Burges, C. J. C. "The MNIST database of handwritten digits." | http://yann.lecun.com/exdb/mnist/ | 1998 | Not about model collapse (dataset). |

### (i-b) Studies cited by IBM Think (footnotes)

| # | Bibliographic data | URL | Date | Main claim re model collapse (from abstract) |
|---|---|---|---|---|
| I1 (fn 1,3,6,7) | Shumailov, I., Shumaylov, Z., Zhao, Y., Gal, Y., Papernot, N., Anderson, R. "The Curse of Recursion: Training on Generated Data Makes Models Forget." arXiv:2305.17493 [≈B: preprint of the Nature paper] | https://arxiv.org/abs/2305.17493v3 | 2023-05-27 (v3 2024-04-14) | Using model-generated content in training causes irreversible defects in which the tails of the original distribution disappear ("Model Collapse"), shown in VAEs, GMMs and LLMs. |
| I2 (fn 2) | Smith, M. S. "The Internet Isn't Completely Weird Yet; AI Can Fix That." IEEE Spectrum [news] | https://spectrum.ieee.org/ai-collapse | 2023-06-23 | Reports a pair of papers finding that training a model on its own output rapidly degrades quality ("model collapse looms"). Registration wall. |
| I3 (fn 4,5) | Peterson, A. J. "AI and the Problem of Knowledge Collapse." arXiv:2404.03502; AI & Society 40:3249–3269 (2025), doi:10.1007/s00146-024-02173-x | https://arxiv.org/abs/2404.03502 | 2024-04-04 | LLMs generate toward the centre of the distribution; widespread reliance on recursive AI systems can cause "knowledge collapse" that harms innovation and the richness of human understanding unless humans seek out diverse knowledge. |
| I4 (fn 8) | Rice University News and Media Relations. "Breaking MAD: Generative AI could break the internet." [news] | https://news.rice.edu/news/2024/breaking-mad-generative-ai-could-break-internet | 2024-07-30 | Training successive generations on synthetic data creates self-consuming loops that can irreparably corrupt models within a few generations ("Model Autophagy Disorder"). |
| I5 (via fn 8) | Alemohammad, S., Casco-Rodriguez, J., Luzi, L., Humayun, A. I., Babaei, H., LeJeune, D., Siahkoohi, A., Baraniuk, R. G. "Self-Consuming Generative Models Go MAD." arXiv:2307.01850; ICLR 2024 | https://arxiv.org/abs/2307.01850 | 2023-07-04 | Without enough fresh real data in each generation of an autophagous loop, generative models progressively lose quality (precision) or diversity (recall). |
| I6 (fn 11) | Wyllie, S., Shumailov, I., Papernot, N. "Fairness Feedback Loops: Training on Synthetic Data Amplifies Bias." Proc. ACM FAccT 2024, doi:10.1145/3630106.3659029; arXiv:2403.07857 | https://facctconference.org/static/papers24/facct24-144.pdf (unreachable: connection reset) ; https://arxiv.org/abs/2403.07857 | 2024-03-12 | Model-induced distribution shifts (model collapse for generative models) cause loss of performance, fairness and minoritized-group representation, even from unbiased data; "algorithmic reparation" curation can counter it. |
| I7 (fn 12) | Data Provenance Initiative. "About." [initiative page] | https://www.dataprovenance.org/about | accessed by IBM 2024-09-23 | Not a study; site describes "public measurement infrastructure for AI data". JS-only page, text not extractable. |
| I8 (fn 13) | Gerstgrasser, M., Schaeffer, R., Dey, A., Rafailov, R., Sleight, H., Hughes, J., Korbak, T., Agrawal, R., Pai, D., Gromov, A., Roberts, D. A., Yang, D., Donoho, D. L., Koyejo, S. "Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Real and Synthetic Data." arXiv:2404.01413 | https://arxiv.org/abs/2404.01413 | 2024-04-01 | Replacing real data with synthetic data tends toward collapse, but accumulating synthetic data alongside the original real data avoids model collapse across model sizes and architectures. Also found by (iii)-Q1. |

Excluded from step (i) as part of B: IBM fn 9–10, the Nature Supplementary Information (static-content.springer.com/esm/…41586_2024_7566_MOESM1_ESM.pdf).

---

## Step (ii) — citation expansion (15)

Listed in the order produced by the selection rule (number of seeds cited, then citation count). The seeds cited by each work are in brackets.

| # | Bibliographic data | URL | Date | Main claim re model collapse (from abstract) |
|---|---|---|---|---|
| E1 | Ferbach, D., Bertrand, Q., Bose, A. J., Gidel, G. "Self-Consuming Generative Models with Curated Data Provably Optimize Human Preferences." NeurIPS 2024; arXiv:2407.09499 [curse, fairness, inevitable, mad] | https://arxiv.org/abs/2407.09499 | 2024-06-12 | When synthetic data is curated by users before retraining, the self-consuming loop acts as implicit preference optimization instead of collapsing. |
| E2 | Schaeffer, R., Kazdan, J., Arulandu, A. C., Koyejo, S. "Position: Model Collapse Does Not Mean What You Think." arXiv:2503.03150 [4 seeds] | https://arxiv.org/abs/2503.03150 | 2025-03-05 | The literature uses eight distinct, conflicting definitions of model collapse. Under realistic conditions the catastrophic narrative misreads the evidence. |
| E3 | Jarvis, D., Klein, R., Rosman, B., James, S., Sarao Mannelli, S. "Position: the Stochastic Parrot in the Coal Mine. Model Collapse is a Threat to Low-Resource Communities." arXiv:2605.04127 [4 seeds] | https://arxiv.org/abs/2605.04127 | 2026-05-05 | By skewing distributions away from their tails and lowering training efficiency, model collapse disproportionately harms low-resource and marginalized communities. |
| E4 | Qiao, X., Du, X., Liu, W., Zhang, J., Mai, P., Zhang, M., Pang, Y. "When Sample Selection Bias Precipitates Model Collapse." arXiv:2606.13732 [4 seeds] | https://arxiv.org/abs/2606.13732 | 2026-06-11 | Verifier-based data selection with siloed, biased references prunes global tail modes and accelerates collapse, with power-law diversity decay. Also found by (iii)-Q1. |
| E5 | Kazdan, J., Schaeffer, R., Dey, A., Gerstgrasser, M., Rafailov, R., Donoho, D. L., Koyejo, S. "Collapse or Thrive? Perils and Promises of Synthetic Data in a Self-Generating World." arXiv:2410.16713 [curse, inevitable, mad] | https://arxiv.org/abs/2410.16713 | 2024-10-22 | Replacing real data collapses in every setting studied. Accumulating synthetic data with real data keeps test loss bounded, so collapse is containable. |
| E6 | Dey, A., Donoho, D. "Universality of the π²/6 Pathway in Avoiding Model Collapse." arXiv:2410.22812 [3 seeds] | https://arxiv.org/abs/2410.22812 | 2024-10-30 | Under the augment workflow, the bounded π²/6 test-risk inflation that avoids collapse holds universally across a broad class of models, not only in linear regression. |
| E7 | Suresh, A. T., Thangaraj, A., Khandavally, A. N. K. "Rate of Model Collapse in Recursive Training." AISTATS 2025; arXiv:2412.17646 [3 seeds] | https://arxiv.org/abs/2412.17646 | 2024-12-23 | Gives the rate of collapse under ML recursive training. For discrete distributions, the time to forget a word scales roughly linearly with its original frequency. |
| E8 | Shi, L., Wu, M., Zhang, H., Zhang, Z., Tao, M., Qu, Q. "A Closer Look at Model Collapse: From a Generalization-to-Memorization Perspective." NeurIPS 2025; arXiv:2509.16499 [fairness, inevitable, mad] | https://arxiv.org/abs/2509.16499 | 2025-09-20 | In diffusion models, collapse appears as a shift from generalization to memorization, driven by falling entropy of synthetic data. Entropy-based selection mitigates it. |
| E9 | Drayson, G., Yilmaz, E., Lampos, V. "Machine-generated text detection prevents language model collapse." EMNLP 2025, 29657–29673; arXiv:2502.15654 [3 seeds] | https://arxiv.org/abs/2502.15654 | 2025-02-21 | Decoding strategy drives the severity of collapse. Detector-based importance resampling of likely-human text prevents it. |
| E10 | Fu, S., Wang, Y., Chen, Y., Tian, X., Tao, D. "A Theoretical Perspective: How to Prevent Model Collapse in Self-consuming Training Loops." ICLR 2025; arXiv:2502.18865 [3 seeds] | https://arxiv.org/abs/2502.18865 | 2025-02-26 | "Recursive stability" explains why some loops collapse and others don't. Even a constant proportion of real data ensures convergence (transformers in-context). |
| E11 | Yoon, Y., Hu, D., Weissburg, I., Qin, Y., Jeong, H. "Model Collapse in the Self-Consuming Chain of Diffusion Finetuning: A Novel Perspective from Quantitative Trait Modeling." arXiv:2407.17493 (no venue found) [3 seeds] | https://arxiv.org/abs/2407.17493 | 2024-07-04 | Fine-tuning text-to-image diffusion on its own outputs universally degrades images. CFG scale is the key factor, and a mutation-inspired fine-tuning (ReDiFine) mitigates it. |
| E12 | Wei, X., Zhang, X. "Self-Consuming Generative Models with Adversarially Curated Data." ICML 2025; arXiv:2505.09768 [3 seeds] | https://arxiv.org/abs/2505.09768 | 2025-05-14 | Noisy or adversarial curation in self-consuming loops can destabilize retraining. Gives conditions for robustness and proposes attack algorithms. |
| E13 | Garg, A., Bhattacharya, S., Sur, P. "Preventing Model Collapse Under Overparametrization: Optimal Mixing Ratios for Interpolation Learning and Ridge Regression." arXiv:2509.22341 [3 seeds] | https://arxiv.org/abs/2509.22341 | 2025-09-26 | Optimal real/synthetic mixing provably prevents collapse in overparameterized regression. For min-norm interpolation the optimal real fraction tends to 1/golden ratio. |
| E14 | He, H., Xu, S., Cheng, G. "Recursive Learning Without Collapse: A Weighting-Based Stabilization Framework." J. R. Stat. Soc. B, doi:10.1093/jrsssb/qkag099; arXiv:2502.18049 [3 seeds] | https://arxiv.org/abs/2502.18049 | 2025-02-25 | Mixing fresh real data with weighted synthetic data stabilizes recursive training. Characterizes the optimal weighting scheme. Also found by (iii)-Q1. |
| E15 | Wang, T., Horiguchi, A., Pang, L., Priebe, C. E. "LLM Web Dynamics: Tracing Model Collapse in a Network of LLMs." arXiv:2506.15690 [curse, fairness, mad] | https://arxiv.org/abs/2506.15690 | 2025-05-26 | Simulating the internet as a shared RAG database, a network of LLMs converges in output (network-level collapse), with guarantees via interacting GMMs. |

---

## Step (iii) — declared scholarly search

### Q1 "model collapse synthetic data recursive training" (10 results, all on-topic; 7 new)

Results in search order:

1. Borji (2410.12954), new
2. Yi et al. (2510.16657), new
3. Gerstgrasser et al. (2404.01413), duplicate of I8
4. Seddik et al. (2404.05090), new
5. Keisha et al. (2509.04796), new
6. Luo et al. (2607.17043), new
7. Qiao et al. (2606.13732), duplicate of E4
8. Xu et al. (2505.13947), new
9. He et al. (2502.18049), duplicate of E14
10. Hu et al. (2505.08803), new

| # | Bibliographic data | URL | Date | Main claim re model collapse (from abstract) |
|---|---|---|---|---|
| S1 | Borji, A. "A Note on Shumailov et al. (2024): 'AI Models Collapse When Trained on Recursively Generated Data'." arXiv:2410.12954 | https://arxiv.org/abs/2410.12954 | 2024-10-16 | Repeated fit-and-sample (KDE) shows that the collapse B reports is a statistical phenomenon that may be unavoidable. |
| S2 | Yi, B., Liu, Q., Cheng, Y., Xu, H. "Escaping Model Collapse via Synthetic Data Verification: Near-term Improvements and Long-term Convergence." arXiv:2510.16657 | https://arxiv.org/abs/2510.16657 | 2025-10-18 | An external verifier (human or better model) prevents collapse and gives near-term gains. In the long run, estimates converge to the verifier's "knowledge center" and gains plateau unless the verifier is perfect. |
| S3 | Seddik, M. E. A., Chen, S.-W., Hayou, S., Youssef, P., Debbah, M. "How Bad is Training on Synthetic Data? A Statistical Analysis of Language Model Collapse." arXiv:2404.05090 | https://arxiv.org/abs/2404.05090 | 2024-04-07 | Collapse cannot be avoided when training solely on synthetic data. With mixing, gives a maximal synthetic amount below which collapse is avoided. |
| S4 | Keisha, F., Wu, Z., Wang, Z., Koshiyama, A., Treleaven, P. "Knowledge Collapse in LLMs: When Fluency Survives but Facts Fail under Recursive Synthetic Training." arXiv:2509.04796 | https://arxiv.org/abs/2509.04796 | 2025-09-05 | Recursive synthetic training produces a three-stage "knowledge collapse": factual accuracy decays while fluency persists ("confidently wrong"). Domain-specific synthetic training mitigates it. |
| S5 | Luo, X., Huang, Y., Guo, K., He, P., Zou, C., Hua, T., Zhang, X. "Learning from Synthetic Data without Model Collapse in Iterative Instruction Tuning." arXiv:2607.17043 | https://arxiv.org/abs/2607.17043 | 2026-07-19 | In iterative instruction tuning, collapse shows up as a polarization of competence: strong skills are reinforced and weak ones degrade. Boundary-aware curation (KITE) counters it. |
| S6 | Xu, S., He, H., Cheng, G. "A Probabilistic Perspective on Model Collapse." arXiv:2505.13947 | https://arxiv.org/abs/2505.13947 | 2025-05-20 | Recursive training is a random walk of the estimate. Sample size must grow (superlinearly if unbiased) at each step to prevent collapse. |
| S7 | Hu, Z., Rostami, M., Thomason, J. "Multi-modal Synthetic Data Training and Model Collapse: Insights from VLMs and Diffusion Models." arXiv:2505.08803 | https://arxiv.org/abs/2505.08803 | 2025-05-10 | Collapse in multi-modal recursive loops has distinct traits (better vision-language alignment, higher captioning variance). Larger decoding budgets, model diversity and frozen-model relabeling mitigate it. |

### Q2 "model collapse human writing homogenization" (9 unique on-topic; 9 new; shortfall of 1)

Results in search order: Sourati et al.; Peter et al.; Rudko & Bashirpour Bonab; Kim et al. (html + pdf, counted once); Jiang; Satharasi & Iyengar; Sui; Hodel & West; Inoshita et al.

| # | Bibliographic data | URL | Date | Main claim re model collapse (from abstract) |
|---|---|---|---|---|
| H1 [H] | Sourati, Z., Ziabari, A. S., Dehghani, M. "The Homogenizing Effect of Large Language Models on Human Expression and Thought." arXiv:2508.01491; Trends in Cognitive Sciences (per Semantic Scholar) | https://arxiv.org/abs/2508.01491 | 2025-08-02 | No direct model-collapse claim. LLMs reinforce dominant styles and amplify convergence of human language and reasoning, flattening cognitive diversity. |
| H2 [H] | Peter, O., Simperl, E., Devlin, K. "Narrowing the Horizon: Quantifying Topic Saliency Shifts in Generative Monoculture." arXiv:2609.35302 | https://arxiv.org/abs/2609.35302 | 2026-09-28 | LLM outputs converge into a "generative monoculture". Topic-saliency shifts in post-training (climate case) narrow perspectives, and specialised models help preserve them. |
| H3 | Rudko, I., Bashirpour Bonab, A. "ChatGPT is incredible (at being average)." Ethics and Information Technology 27, art. 36 (open access) | https://link.springer.com/article/10.1007/s10676-025-09845-2 | 2025-07-18 | Frames output homogenization as Frankfurtian "how-bullshit", and model collapse as a critical instance of it with structuring effects on society. |
| H4 [H] | Kim, Y., Chang, Y., Pham, C. M., Iyyer, M. "Argument Collapse: LLMs Flatten Long-Form Public Debate." arXiv:2606.01736 | https://arxiv.org/abs/2606.01736 | 2026-06-01 | LLM essays converge on a small set of arguments (3.4% of LLM main arguments are unique vs 65.3% of human ones in NYT debates). "Argument collapse" flattens public debate. |
| H5 | Jiang, Z. "The Necessity of Imperfection: Reversing Model Collapse via Simulating Cognitive Boundedness." arXiv:2512.01354 | https://arxiv.org/abs/2512.01354 | 2025-12-01 | Statistically smooth synthetic data strips the long-tail irregularities of human text and accelerates collapse. Simulating cognitive processes (PMCSF) restores them. |
| H6 | Satharasi, T., Iyengar, S. S. "Future of AI Models: A Computational perspective on Model collapse." arXiv:2511.05535 | https://arxiv.org/abs/2511.05535 | 2025-10-29 | As synthetic content dominates the web, recursive training erodes linguistic and semantic diversity. Tracks this computationally as model collapse. |
| H7 [H] | Sui, P. "LLMs Exhibit Significantly Lower Uncertainty in Creative Writing Than Professional Writers." arXiv:2602.16162 | https://arxiv.org/abs/2602.16162 | 2026-02-18 | No direct model-collapse claim. Across 28 LLMs, model continuations show much lower uncertainty than human writing, which alignment worsens. |
| H8 | Hodel, D., West, J. D. "Epistemic diversity across language models mitigates knowledge collapse." arXiv:2512.15011 | https://arxiv.org/abs/2512.15011 | 2025-12-17 | Across ten self-training iterations, an ecosystem of diverse models outperforms an AI monoculture, which accelerates collapse. |
| H9 [H] | Inoshita, K., Omura, M., Yamanaka, T., Maeda, G., Tsuji, K. "Does AI Homogenize Student Thinking? A Multi-Dimensional Analysis of Structural Convergence in AI-Augmented Essays." arXiv:2603.21228 | https://arxiv.org/abs/2603.21228 | 2026-03-22 | No direct model-collapse claim. AI-augmented student essays show a quality–homogenization tradeoff, and prompt design can reverse it. |

[H] = abstract studies homogenization of LLM output or human writing without recursive training on synthetic data. H2 (generative monoculture) and H4 ("argument collapse" across models) use convergence or collapse language for output homogenization, not training-loop collapse.

---

## Summary table of provenance

| Step | Entries | IDs |
|---|---|---|
| i (Nature refs) | 22 | N1–N22 |
| i (IBM-cited) | 8 | I1–I8 |
| ii | 15 | E1–E15 |
| iii Q1 | 7 new (+3 dup: I8, E4, E14) | S1–S7 |
| iii Q2 | 9 | H1–H9 |
| **Total** | **61** | |

Order is the order of discovery, not prestige. No size matching has been applied.
