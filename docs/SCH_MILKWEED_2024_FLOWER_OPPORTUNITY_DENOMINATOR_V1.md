# SCH: apparent milkweed fitness-stage selection divergence under unequal floral exposure — original-source reanalysis V1 (2026-11-16)

## Primary ecological finding and what was actually computed

**A previously promising source-computed association shrinks sharply when the original observation denominators are reconciled.** In García, Dow, Vézina & Parachnowitsch (2024), *Journal of Pollination Ecology* 36:73–84 (doi: [10.26786/1920-7603(2024)758](https://doi.org/10.26786/1920-7603(2024)758)), fruit initiation was counted **over the entire tagged stem**, while inserted pollinia were recorded from **10 sampled flowers per stem** (five on each of two umbels). Thus previous direct comparisons of relative *whole-plant fruit counts* with relative *ten-flower pollinium counts* compare different exposure opportunities.

The original complete-case 2024 Appendix II source **XLSX SHA-256** is pinned to \`d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb\` (38,955 bytes), DOI above, official publisher galley \`https://www.pollinationecology.org/index.php/jpe/article/download/758/478\`. The XLSX contains one CSV-like line per cell, giving **103 original observational source records** with **102 distinct plant ID labels** (source label \`68\` is duplicated; both original rows retained, ambiguous rows grouped during bootstrap and each dropped separately in source sensitivity). These are not 103 independently randomized plants or genetic individuals.

### Source-exposure definitions verified directly from 103 individual rows

The journal Methods describe reproductive effort as total inflorescence number and total **flowers plus buds estimated at peak bloom**, and define inflorescence size by total flowers divided by inflorescence number. The original dataset exactly verifies:

- \`tot.flws = flwrs + buds\` on **103/103** source rows.
- \`inflor.size = tot.flws/inflor.nu\` within recorded source rounding, maximum absolute difference **0.00429**.
- Flower opportunities per plant at peak: **33–268**, median **118**.
- **40/103 stems** have zero initiated fruits, compared with **27/103** with zero scored pollinia insertions.
- Mean \`fruit.init\` **2.068**, sample variance **7.142** (count overdispersion is plausible).
- No plant has more initiated fruits than the estimated total peak flowers (\`0/103\`), but **the seasonal flowers and traced flowers are not identified**, so this is *not* a directly measured per-pollinium fertilization rate.

This key source feature demonstrates why an inflorescence-number trait can correlate with all-plant fruit count but not with insertion count from exactly ten sampled flowers.

### Empirical relationships

Among the same 103 genuine published rows:

| Original observable | Pearson correlation with total flowers at peak |
|---|---:|
| **Initiated fruit count for whole plant** | **+0.42082** |
| **Inserted pollinia count in ten-flower sample** | **+0.03742** |

The source count-based same-plant two-female-stage comparison from PR #252 is recovered unchanged (ten jointly standardized trait predictors; within-record difference of mean-normalized responses, with HC3 robust SE):

| Inflorescence number as focal trait | β: fruit minus insertions | Nominal HC3 P | 95% source plant-ID-block bootstrap |
|---|---:|---:|---|
| Whole-plant fruit count relative to mean vs ten-flower pollinium count relative to mean | **+0.48358** | **0.00903** | **[+0.14184,+0.86261]** |
| **Fruit count divided by the plant's peak flower count**, then normalized to mean, vs pollinium count per fixed 10 flowers normalized to mean | **+0.10502** | **0.55018** | **[−0.23110,+0.44305]** |

The full original ten-trait fit is recomputed in both comparisons, not merely the bivariate correlation. The per-opportunity model retains all original individuals and source phenotypes; the 1,999 bootstrap replicates resample **102 source plant-ID labels** as groups (duplicate label 68 remains grouped). Dropping either duplicated-source ID68 row separately yields adjusted focal contrast **+0.1252 / +0.1211** under the fixed original phenotype standardization. The observed directional association from the original count-based outcome is **not robust to changing the denominator**.

### Do not turn this sensitivity into a spurious causal mediation fraction

**Important:** mean-normalized fruit *count* and mean-normalized fruit *per peak flower* are different response estimands. One cannot calculate a scientifically identified percentage of causal mediation by subtracting these coefficients. The per-peak-flower quantity is an **imperfect production-rate proxy**, not the probability that a tracked flower received a compatible pollinium and then initiated a fruit. The 10-flower insertion sample is not a random event-matched risk set of the fruit counts across the whole plant.

A separate conditional linear model adds **standardized \`log(tot.flws)\`** to the original ten-trait count-based model. For inflorescence-number's paired difference it returns **β=−1.0098** and source-label bootstrap 95% interval **[−2.4159,+0.4424]**. This unstable change of sign is a **sensitivity of correlated size and exposure covariates**, not proof of reversed ecological selection. The total flower count is **algebraically derived** from inflorescence number and inflorescence size, so including it can adjust away the very display pathway one might want to measure. Both exposure approaches require separate biological interpretation.

### Why the new result matters to SCH

Prior source-compiled 2005 *A. syriaca* experiment reported opposite *phenotypic* selection slopes on flowering duration when using female pollinia insertion versus fruit-initiation outcomes under resource supplementation (original source row IDs 29/35). The independent 2024 source revealed apparent trait-stage divergence, but **the strongest numerical candidate in 2024 (inflorescence number) is heavily sensitive to the unit of flower opportunity**. This establishes an **important failure mode of inferring postpollination filtering from different observed fitness-stage proxies**: a trait generating more flowers may increase the *number of opportunities* rather than the rate of effective pollen-to-fruit conversion.

The new evidence is therefore not a positive confirmation that a postpollination filter causes evolutionary conflict, nor a proof there is no such filter. It is a **negative control with an ecological consequence**: an apparently significant stage-dependent selection difference may disappear under an opportunity-matched descriptive analysis. SCH should require matching the risk set, stage, observation time, and fitness currency **before** promoting opposite coefficients to functional trade-offs.

## Robustness, preconditions and limitations

- This is a genuine source-data analysis of a previously published observational population, **not newly collected field or trait-manipulation data**.
- The count-based model is reproduced with the original source data; the matched denominator sensitivity is new. Both use 10-trait partial slopes, HC3 uncertainty and a 1,999-draw ID-label-block bootstrap.
- Peak-bloom flower count is a **proxy**: it is not season-total flowers, compatible pollinia received, pollen tube success or actual fruits from the ten measured flowers.
- Conditioning on total flowers may remove legitimate **causal selection on flower production** and should not be advertised as finding the one correct causal fitness measure.
- The fecundity count is overdispersed (variance 7.142 vs mean 2.068) with 40 zero fruits. HC3 and bootstrap do not prove linear-rate model is fully specified; a count-link / hurdle sensitivity is an appropriate **later** extension.
- The 2024 study's 103 rows carry 102 distinct plant labels; clustered ramets/genets and geographic dependence remain unmeasured. The source duplication is documented, not fixed silently.
- The 2024 author's published insertion–fruit correlation from a broader reported population may use a different N than the 103-row appendix; do not claim their printed estimate is wrong.
- Ten traits imply multiple comparisons; no confirmatory familywise stage-difference effect is claimed. No intervention on inflorescence number or fruit retention, no same-flower fate tracking, no function-specific optima and no SCH compromise loss \(\mathcal L\).

### How to reproduce exactly

    python -m scripts.ingest_sch_milkweed_2024_original_appendix --outdir artifacts/sch_milkweed_flower_opportunity
    python -m scripts.analyze_sch_milkweed_2024_flower_opportunity --source artifacts/sch_milkweed_flower_opportunity/original_2024_jpe_appendix_ii.xlsx --output artifacts/sch_milkweed_flower_opportunity/source_flower_opportunity_v1.json --boot 1999
    python -m pytest -q tests/test_sch_milkweed_2024_flower_opportunity.py

The ten-trait comparison values (original count-based, exposure-normalized and conditional log-flower variants) are in \`data/SCH_MILKWEED_2024_GENUINE_FLOWER_OPPORTUNITY_SENSITIVITY_V1.csv\`. The source and complete numeric JSON results are recorded in the dedicated GitHub Action source audit artifact; the original source XLSX remains external (not copied into Git history).

**Status: OBSERVED_FEMALE_STAGE_SELECTION_DIFFERENCE_NOT_ROBUST_TO_FLOWER_OPPORTUNITY_DENOMINATOR; MECHANISTIC_POSTPOLLINATION_CONVERSION_UNIDENTIFIED.**
