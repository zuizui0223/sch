# SCH post-pollination fitness-stage gate: actual original 103-row milkweed reanalysis — 2026-11-15

## New result: a genuine individual-record reanalysis, not a literature review

The 2024 *Asclepias syriaca* study, García, Dow, Vézina & Parachnowitsch, *Journal of Pollination Ecology* 36:73–84, DOI **10.26786/1920-7603(2024)758**, published the original selected data as **Appendix II**, official journal OJS galley **#478**:

https://www.pollinationecology.org/index.php/jpe/article/download/758/478

The actual publisher XLSX was recovered from the official public origin: **38,955 bytes**, **SHA-256 d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb**. Unusually, its sheet \`milkweed.selectiondata\` contains **104 Excel rows in one column**, one *comma-separated line per cell*, not 28 Excel columns; after correctly decoding these lines there are **103 original plant records and 28 variables**. All ten original phenotypic trait measures and all three fitness proxies are complete for 103 records.

**Source-data grain problem:** The 103 original rows have only **102 distinct \`plant_id\` labels**: ID \`68\` occurs twice with identical values on every source field *except \`fruit.init\`*. The authentic 2024 authors reported 103 plants, and the two source records have not been disambiguated by their original investigators. Do **NOT** invent a repaired plant ID or automatically discard one outcome. The primary regression retains all 103 author-published rows (for provenance); the confidence interval resamples all rows **in blocks of 102 observed plant-ID labels**. As a separate sensitivity, either ID 68 row is removed and the model re-estimated on 102 records, preserving the original 103-record trait scaling; the inflorescence-number stage difference changes from **+0.484** to **+0.507 or +0.501**.

This is **one field population**, not 103 independent studies, and source labels do not establish independently genotyped ramets or genetic individuals.

## Exact outcome mismatch: do not compute fruit/insertions as a conversion rate

The 2024 authors scored pollinium removals and insertions in **10 sampled flowers per plant** (5 flowers from each of two inflorescences) while counting initiated fruits **across the whole plant** after flowering. Those original variables do **not** share a one-flower or one-inflorescence risk set; the ratio \`fruit.init/insertions_t\` is **NOT** a valid observed conversion probability.

The paper's original correlation r=**−0.12** for pollinium insertion versus fruits was based on its broader observation stage (original reporting N=**119** pollinium-scored plants). The published ten-trait selection analysis is N=**103**, the 103-row source archive available here. At that latter complete-case source grain, our calculated source Pearson correlation is **r=+0.0114** between fruit count and ten-flower insertion, and **r=+0.4494** between insertion and removal. These are different *sample bases*, not evidence that either printed original-paper correlation is false.

## New actual same-row paired multiple regression

All **ten** original Table 1 traits are fitted simultaneously to (i) fruits initiated, (ii) pollinia inserted and (iii) pollinaria removed, as in the authors' phenotypic selection-gradient method. Predictors are zero-mean/unit sample-SD standardized; each fitness endpoint is divided by the corresponding complete-sample mean. **Nectar concentration uses \`nec.resid\` (the original humidity-adjusted concentration)**, not the uncorrected \`nectar.conc\`, as specified in the original Methods.

Because the **same original rows** supply both female fitness proxies, their difference is modeled as

\[
   w_{\mathrm{fruit},i}-w_{\mathrm{insertions},i}
    = a+\boldsymbol{\delta}^{\mathsf{T}}\mathbf z_i+\epsilon_i,
    \qquad \boldsymbol{\delta}=\boldsymbol{\beta}_{\mathrm{fruit}}-
        \boldsymbol{\beta}_{\mathrm{insertions}} .
\]

This paired response approach preserves the within-row covariance in the sampling uncertainty of \(\delta\), unlike treating the two original marginal SEs as if the sampling processes were independent. HC3 heteroskedasticity-robust SEs and **1,999 paired 102-ID-label-block bootstrap replicates** are reported, with fixed seed 20261115.

The recomputed source inflorescence-number fruit β=**+0.46366** closely reproduces the authors' Table 1 **+0.464**. Its pollinia-insertion β=**−0.01992** is similarly close to the source **−0.016**. This is a useful numerical source-reproduction check, though exact equality for all printed Table 1 coefficients is not asserted.

| Original plant trait | Fruit β | Insertion β | Paired Δβ (fruit − insertion) | HC3 P (unadjusted) | 95% plant-label bootstrap interval |
|---|---:|---:|---:|---:|---|
| **Inflorescence number** | **+0.4637** | **−0.0199** | **+0.4836** | **0.0090** | **[+0.1418,+0.8626]** |
| Inflorescence size | +0.3107 | −0.0109 | +0.3217 | 0.146 | [−0.0661,+0.7583] |
| Petal width | +0.1023 | −0.2503 | +0.3525 | 0.108 | [−0.0035,+0.7854] |
| Floral wet latex | +0.0423 | +0.3326 | −0.2903 | 0.0695 | [−0.6564,−0.0012] |

The remaining six original traits, their full original source-recomputed coefficients, HC3 SEs, original author Table 1 comparison and 1,999-bootstrap intervals are in \`data/SCH_2024_ASCLEPIAS_REAL_103_ROW_PAIRED_STAGE_RESULTS_V1.csv\` and the Actions JSON result.

**Formal inference ceiling matters:**

- The **joint ten-trait difference** (HC3 Wald χ²(10)=**13.258**) has **asymptotic P=0.2096**. It does **not** establish overall stage-level selection divergence.
- Inflorescence number has a **nominal** stage difference P≈**0.0090**, with a positive marginal bootstrap 95% interval, but **none of ten traits** passes a *post hoc ten-test Bonferroni* threshold P<0.005. The exploratory inflorescence result is a **candidate**, not a multiple-comparison-protected general ecological effect.
- The floral-latex bootstrap percentile interval marginally excludes zero but its HC3 P≈0.0695 does not; this is sensitivity to estimation method, especially in a single observational cohort. Do not count it as familywise-confirmed without a predeclared inference rule.
- Including all original plant traits and pollinia insertions, the source same-plant **partial association of relative fruit count with relative insertions** is **β=−0.0779, HC3 SE=0.1369, two-sided normal P=0.5694**. It is neither a causal insertion→fruit effect nor proof of equivalence/no conversion.
- The high-dimensional global Wald test is asymptotic with 103 records, and the ID68 label duplication, potential milkweed clonal structure, possible overdispersion and multiple comparisons limit strong general inference.

## Three independent original programmes: scope of the synthesis

| Primary published programme | Actual biological units | Key source observations | Evidence ceiling |
|---|---|---|---|
| **Caruso, Remington & Ostergren 2005** (doi:10.1007/s00442-005-0183-4) | *A. syriaca*, **one paper, three manipulation regimes** | Published-source flowering-duration β on female pollinia insertion versus fruits initiated has opposite *point signs* in all three regimes; **both slopes nominally supported only under resource supplementation** (−0.533±0.173 vs +0.362±0.113) | No original stage difference fitted interaction or raw plant-level covariance recovered; source treatment manipulation, not trait manipulation |
| **La Rosa & Conner 2017** (doi:10.3732/ajb.1600328) | Three Asclepias species, **one paper**, sample sizes species-dependent | No significantly **positive** pollinia-insertion→fruit-number path was detected in any species; the source's *A. viridiflora* path was negative | Original SEM path is observational; no cross-study common matched trait effect or trial-level raw refit; three species are not three papers |
| **García et al. 2024** (doi:10.26786/1920-7603(2024)758) | *A. syriaca*, **one additional field population, 103 archive records / 102 source IDs** | Genuine original same-row female-stage selection regression obtained; nominal inflorescence difference but **joint ten-trait P=0.210**, **0/10 familywise individual tests**; no positive insertion–fruit partial association detected (P=0.569) | Independent raw-data reanalysis but no randomized trait or pollen compatibility/resource mechanism |

This combined evidence is a **stage-filter hypothesis**, not evidence for one shared causal "conversion probability" or an average meta-analytic stage effect across three papers. Critically, source outcome scales vary (10 sampled flowers vs all-plant fruits, initiated vs matured fruits, per-ramet outcomes, experiment vs observational field settings); no inverse-variance meta-analytic pooling is appropriate.

## Biology: which downstream process might decouple pollinia insertion from fruit initiation?

Separate mechanisms are plausibly involved:

1. **Pollen compatibility / within-clone geitonogamy**: deposited pollinia may be self or incompatible and therefore not produce viable fertilization, even if an insertion was scored.
2. **Insertion effectiveness**: pollen deposited in a stigmatic slit is not proof of pollen-tube germination and effective fertilization.
3. **Resource-dependent fruit retention**: plants may initiate/retain only a small number of fruits relative to receipt due to carbon, nutrient and developmental limitation; the 2005 experimental resource-supplementation result provides a mechanistic motivation but not directly measured trait-specific mediation.
4. **Scale mismatch/phenology/plant condition**: insertion in a ten-flower subset is imperfectly linked to the fate of flowers on the whole plant, and phenotypic plant-vigor covariance can affect both trait and fruit output.

Future identification must mark **individual flowers**, follow their *compatible* deposited pollinia, germination and actual fruit initiation/abortion, ideally in a factorial **pollinator access × resource availability** experiment across a manipulable common trait gradient \(z\). The target is a causal conditional transition \(P(\text{fruit initiation on a tracked flower}\mid\text{effective compatible pollen},z,\text{resources})\), which is NOT in the present archival variables. Quantifying causal conditional mediation requires justified intervention or stronger sequential-exchangeability assumptions and correct denominators.

**Neither this signed-stage analysis nor the original 2005 reproductive-stage differences identify pure pollinator/antagonist optima or SCH's conflict loss \(\mathcal L\).** Keep the present New Phytologist Viewpoint's causal-claim boundaries unchanged.

## Reproducibility

Official published source XLSX is downloaded from galley #478 and checked against frozen SHA-256. The source text-like rows are parsed into 28 variables; no synthetic records are substituted. Main script: \`scripts/analyze_sch_milkweed_2024_paired_stage.py\`. Tests and reproducible source + model artifact: \`.github/workflows/sch_milkweed_2024_paired_stage.yml\`. Evidence receipt from source run ID **43692887512**, artifact **14152339217**, SHA256 of zip \`5491361b34bb21b9ff7cde198fc2e1bf7506b0cac0b9682f794e6dff6c89b063\`.

The original 2020 compiled 137 environmental matched β pairs, 572 master original source rows, and preexisting SCH manuscript claim bounds remain untouched.

**Status: REAL_2024_103_PUBLISHED_PLANT_ROWS_REANALYZED; TWO_FEMALE_OUTCOME_DESCRIPTIVE_DIVERGENCE; OMNIBUS_STAGE_TEST_NOT_SIGNIFICANT; CAUSAL_CONVERSION_NOT_IDENTIFIED.**
