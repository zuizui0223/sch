# SCH: genuine original 572-row multi-fitness source search and temporal identification audit (2026-11-15)

## Action completed: original archive re-ingested, not a literature-only review

This is a **new quantitative reanalysis of a real previously published source database**. The unduplicated original Caruso, Maherali & Martin (2020) experimental-selection master, DOI [10.5061/dryad.sn02v6x0q](https://doi.org/10.5061/dryad.sn02v6x0q), was recovered from Zenodo record 5000217, **83,973 bytes, MD5 `7f680c344c0a418a3d8742649de24d52`, SHA-256 `b03dc481874655d747f59ea41cc4c558b0a1fe5fcf6cebf6f942e6b65b9c6b73`**. The archived source dictionary was separately downloaded and checked, MD5 `0e9a28b40290a3f07ba3c7d7dd2b5a3d`.

This time the target is NOT a difference between environmental treatment arms, and therefore not the earlier 137 matched source pairs. The new question is: **within one reported original treatment/trait/population, do source studies report selection on the same trait through different reproductive/fitness outcome stages?**

An exact original-paper/year/species/population/trait/sex/treatment/agent/context join finds:

| Source processing grain | Recovered count |
|---|---:|
| Original experimental coefficients | **572** |
| Original source papers | **43** |
| Original species in the master | **46** |
| Context strata after full source matching | **514** |
| Strata with at least two different fitness codes | **44** |
| Candidate comparisons of two distinct reported fitness measures | **75** |
| Papers contributing comparisons | **3** |
| Species contributing comparisons | **5** |
| Candidate outcome pairs with both beta and SE reported | **50** |
| Two-outcome point sign differences | **16/75** |
| Two-outcome point sign differences with each independently nominal `|β/SE|>1.96` | **1/75** |

A stricter join additionally requiring identical `within.study.id` yields **0** pairs. That source field identifies different original compiled coefficients here and **has not been demonstrated to be a reliable identifier of the underlying individual plants or their cohort**. Consequently, the zero strict match is a provenance warning, NOT evidence that no two outcomes were measured on the same plant. It is crucial to check primary methods and source raw data.

The 75 comparisons are NOT 75 independent papers or 75 distinct taxa. They are repeated combinations clustered within just three author studies: Caruso et al. 2005 (*Asclepias syriaca*, 18 outcome-pair combinations), Sherrard et al. (*Panicum virgatum*, 32 combinations), and a source study including *Helianthemum marifolium*, *Cistus albidus* and *Ulex parviflorus* (25 combinations). The two last groups mainly compare biomass/performance versus fecundity and growth versus fecundity. Stage/fitness labels cannot be assigned the same causal currency without original adjudication.

## One new genuine same-trait opposite female-stage signature

A *single original source pair* survives marginal opposite-sign screening. It comes from Caruso, Remington & Ostergren (2005), *Oecologia* 146:68–76, DOI [10.1007/s00442-005-0183-4](https://doi.org/10.1007/s00442-005-0183-4), whose original published abstract verifies that each treatment studied **one male and two separate female fitness components** and that resource supplementation experimentally increased fruit set.

**Source experiment and exact original row identities**:
- Species: ***Asclepias syriaca*** (common milkweed)
- Same source trait: **length of flowering period**
- Same reported original regime: **resource supplementation**
- Female stage 1, **number of pollinia inserted** (pollen receipt; original source row **29**): β = **−0.533 ± 0.173**
- Female stage 2, **number of fruits initiated** (fruit-stage fecundity; original source row **35**): β = **+0.362 ± 0.113**

Both β/SE ratios separately exceed |1.96| and have **opposite signs**, even though the same trait and treatment are identified in the original meta master. This is a stronger source signature of **intra-female-stage selection discordance** than a single nonzero-vs-nonsignificant coefficient. It is **NOT male versus female antagonism**: pollinia insertion and fruit initiation are both female fitness proxies; pollinia removal is the male proxy in this system.

The source beta contrast is Δβ (fruits initiated minus inserted pollinia) = **+0.895**. A *conditional* Cauchy–Schwarz upper bound on its comparison SE is SE₁+SE₂=**0.286**, yielding conditional normal z≥**3.1294** and single-comparison P≤**0.001752**. This is **not** a source author-fitted interaction P, requires comparable marginal estimands, and does not use the unknown two-stage covariance. The exploratory family of **75 source outcome pairs** yields a conservative adjusted upper bound of about **0.1314**, so this result cannot be advertised as a universal familywise discovery. A direct same-plant stage-contrast model, source authors' actual treatment-stage interaction, and replication in independent species remain unverified.

*Biological implication (hypothesis, not a measured mechanism):* resource supply may alter the translation from pollen deposition/receipt to fruit initiation, changing how flowering duration maps to effective female fitness. An additional post-pollination conversion term is a natural explanation, but its gradient has **not been measured**; do not subtract those published standardized betas and label the result a causal conversion probability.

## Critical audit of previous Marchantia fitness-component conflict signature

Fuselier & McLetchie (2002), *American Journal of Botany* 89:592–601, DOI [10.3732/ajb.89.4.592](https://doi.org/10.3732/ajb.89.4.592), explicitly specifies three distinct observation times in female *Marchantia inflexa* exposed to 55% shade:

| Published original quantity | Source observation |
|---|---|
| Asexual cup count (asexual fitness proxy) | **Day 120** of experiment |
| Number of sexual structures (sexual fitness proxy) | **Day 150** |
| Age of first sexual expression, mean among 40 original high-light females (Table 1) | **132.9 days** |
| Complete-case sexual/alternative asexual selection models (Table 6 and Results) | **31 females**, not the same denominator as 40 |
| Same-trait direct phenotypic β on sexual structure number | **−0.915** |
| Same-trait direct phenotypic β on day-120 asexual cup number | **+0.496** |

**Temporal identification warning:** for any individual whose sexual expression began *after* day 120, sex expression timing cannot be a prior causal driver of the earlier day-120 cup count. Since the original 40-female average is 132.9 days, at least one of those 40 expressed sex after day 120, but **the fraction among the selected 31 females is not known**. Thus regressions using sexual-onset age as a predictor of asexual fitness can be phenotypic associations with past plant vigor/allocation and cannot identify the causal effect of manipulating later sexual onset on earlier asexual cups. Selecting the 31 females who expressed sex can additionally affect representation of plants.

**Separate source-provenance warning:** original Table 6 prints a total selection differential **`s=+0.243`** for sexual-onset age on the sexual-structure fitness outcome, while Table 7 prints a Pearson correlation between the SAME trait and outcome of **`r=−0.56`** (both marked N=31). These original table numbers are also reproduced in the author's 2004 University of Kentucky dissertation [UKnowledge](https://uknowledge.uky.edu/gradschool_diss/267/), Tables 6.6/6.7. Under identical 31 observations and positively oriented variables, a conventional univariate selection differential and Pearson r both have the sign of the same covariance and **cannot have opposite signs**. This is a **source estimand, transcription, or sample alignment discrepancy needing the original individual records**, not permission to silently change the published s sign and not proof of misconduct or original paper error. The sign inconsistency does NOT, by itself, refute the separately reported multivariate β=−0.915 or +0.496.

**Defensible Marchantia conclusion remains:** one original study reports opposite phenotypic *multivariate* selection gradients through sexual and asexual reproductive proxies on the same declared trait. It does NOT demonstrate genetic selection on sexual onset, a randomized common trait manipulation, a standardized cross-component direct difference, experimentally separated pure-function optima, or empirical SCH loss **L**.

## What this result changes and what it does not

SCH can now report two distinct original source systems with **same shared trait coordinate and two reproductive/fitness stages whose fitted phenotypic selection coefficients have opposite signs**: one independent 2002 liverwort system across sexual versus asexual fitness pathways and one independent 2005 milkweed system **within female reproductive stages**. This is a biological *phenotypic-signature evidence map with new original database-derived quantitative comparisons*, NOT an inverse-variance meta-estimate of a common effect and not causal proof of trait-function conflict. In the milkweed case both reported slopes individually have standard errors; in Marchantia the two component gradients have original nominal tests but no reported matched covariance or raw genotypic confirmation.

The earlier 137 context matched pairs, 41 point context flips, 2020 43-pair sign-persistence evidence, all 26 originally paired studies, and SCH's paper-ready Viewpoint remain unchanged. None of the 75 multi-fitness source combinations is added to the pre-existing **137 environmental contrast pairs**.

### Reproducible execution

    python -m scripts.audit_sch_2020_original_multi_fitness_components --outdir artifacts/sch_2020_fitness_components --output artifacts/sch_2020_fitness_components/real_fitness_grain_receipt.json
    python -m scripts.audit_sch_marchantia_2002_temporal_component --output artifacts/sch_marchantia2002_temporal_source.json
    python -m pytest -q tests/test_sch_2020_original_multi_fitness_components.py tests/test_sch_marchantia_2002_temporal_component.py

Authentic original sources are verified by source MD5 before opening the 572-row XLSX. Test fixtures check no numeric/trait/source drift and no causal overpromotion. The GitHub Action retains the original master workbook and source readme for short-term independent audit; derived receipts are source-documenting, not newly observed biological replicates.

**Next identification gate:** for the 2005 milkweed comparison, find the exact original 2005 fitted stage-comparison and raw within-plant joint measurements (pollinia insertion, fruit initiation, flowering duration and treatment), then test reproduction-stage conversion under the resource supplementation manipulation while preserving plant and family structure. The temporality issue in 2002 Marchantia must be explicitly resolved before causal fitness-component claims are considered.
