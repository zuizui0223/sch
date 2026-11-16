# SCH: original 2024 milkweed extra-Poisson and two-part source outcome audit (2026-11-17)

## Verified quantitative result — same original plants, new model

The correct source consists of 103 published original rows, 102 distinct labelled plant IDs (original ID 68 appears twice), from García, Dow, Vézina & Parachnowitsch (2024), *Journal of Pollination Ecology*, DOI **10.26786/1920-7603(2024)758**. Publisher Appendix II XLSX identity: **38,955 bytes, SHA256 \`d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb\`**.

The source publisher's official download returned HTTP 500 during this CI; the exact verified XLSX was recovered from this repository's earlier successful source run **#43893168280**, artifact \`sch-milkweed-2024-original-poisson-exposure-v1\`, and checked **again** against the identical original SHA256 before any model ran. There is no synthetic or substituted plant record. The new full source audit run **#43898620526** succeeded, preserving the original XLSX and JSON model receipt as artifact **#14241245787**, artifact ZIP SHA256 **\`c557a3b6abf5b38bf46910a1df709b7ce7cbf1c231e1e9940c111d3ad2d514a9\`**.

The previous authentic-source results (merged PR #253/#254) showed that the source 103-row *inflorescence-number* selection gradient difference between **whole-plant fruit initiation counts** and **pollinia insertions measured on ten sampled flowers per plant** changes dramatically when fruit counts are adjusted for the flower opportunity denominator. The Poisson-offset analysis gave β_delta=+0.08315 (P=0.6334), versus β_delta=+0.45862 (P=.0092) without an exposure offset.

## New NB2 test: the post-offset non-detection is not explained by assuming Poisson variance

The new procedure uses two independent NB2 **working conditional mean** models on standardized 10-trait covariates with offsets \(\log(\mathrm{tot.flws})\) for whole-stem initiated fruits and \(\log(10)\) for scored pollinia insertions. It joins both estimates via a **single 102-plant-label-cluster sandwich matrix**, with source-specific model residual moment dispersions (fruit α **0.43988**, insertion α **0.37809**) and a 499-replicate plant-ID block bootstrap. This is not a formal independent author-fitted model and not a causal effect.

| Original outcome model / question | Inflorescence-number stage log-rate coefficient difference | Nominal robust P | 95% interval |
|---|---:|---:|---|
| Previously merged Poisson + flower offset | **+0.08315** | 0.63335 | [−0.25852,+0.42482] |
| New NB2 with flower offset and same source plant labels | **+0.08906** | **0.61281** | **[−0.25588,+0.43401]** |

The new stage-specific NB2 Wald omnibus test for **all ten trait gradients** is χ²(10)=**10.19096**, **P=0.42390**, with **zero of ten** nominal individual P values surviving an exploratory Bonferroni P<0.005 family. The paired 499 original-label bootstrap for the focal coefficient gives **[−0.27063,+0.45448]**, also including zero. The two source ID68 rows were each excluded separately, yielding β_delta **+0.10681** (P=.5452) and **+0.10339** (P=.5595). Both cases preserve the conclusion.

A predeclared NB2 common-dispersion alpha grid **0.25, 0.5, 1, 2** produces respective focal β_deltas **+0.08399, +0.08987, +0.09807, +0.10741**, all with **P≥0.560**; none of these models produces a significant ten-trait joint test or an individually Bonferroni-passing trait. The alpha values are source-residual-moment estimates / fixed sensitivity grid, **not fully likelihood-estimated NB2 dispersion parameters**. Cluster-sandwich inference can account for some variance misspecification, not arbitrary errors in the log-mean functional form.

**Strongest warranted conclusion:** the earlier *numerical* stage contrast for inflorescence number is **not robust to the observed flower opportunity denominator**, and the attenuation remains across relative-fitness OLS, Poisson log-mean, and NB2 log-mean sensitivity analyses. Failure to reject is **not equivalence** or proof of no resource/pollen limitation.

## Additional new two-part insight: outcome definition determines the apparent flower-display selection

The original 103 source rows include **40 stems with zero initiated fruits** and **63 stems with one or more**. An observational *fruit-present* logistic regression with the ten standardized traits gives:

| Same focal trait: inflorescence number | Log-odds coefficient β | Robust P | 95% confidence interval |
|---|---:|---:|---|
| Probability of one or more fruits on the whole tagged stem | **+1.38204** | **0.0000111** | [+0.76573,+1.99836] |
| Same binary outcome, also conditioning on standardized log peak flower count | **+0.23324** | **0.85279** | [−2.23037,+2.69685] |

This large shift supports **flower-opportunity / display as a plausible explanation for the unadjusted association**, but the post-conditioning coefficient is extremely imprecise. Total flowers are themselves produced by inflorescence number and size; conditioning on the mediator and on correlated predictors may remove legitimate trait effects. Therefore neither the loss of significance nor the coefficient difference estimates a causal mediated fraction. The nominal tiny P for the unadjusted binary model is an *exploratory source-model association*, not a new independent population study.

Among the **63 fruit-positive records (62 distinct plant-ID labels)**, the conditional *working NB mean* regression shows a particularly instructive denominator effect:

| Fruit-positive stems only | Focal inflorescence-number log mean slope | Robust P | 95% interval |
|---|---:|---:|---|
| **Total initiated fruit count** on whole stem | **+0.03925** | **0.67228** | [−0.14260,+0.22109] |
| **Fruit count per peak flower proxy** | **−0.32906** | **0.000269** | [−0.50607,−0.15204] |

The latter negative source association is stable in a *working NB2 alpha grid* 0.25–2 (approximately β −0.329 to −0.331), but **does NOT establish an allocation trade-off**. The sign and magnitude shift when dividing by a flower count that is algebraically linked to the focal inflorescence-number predictor. Selecting only positive-fruit stems can induce selection/collider bias, and the reported NB conditional mean regression is **not a properly normalized zero-truncated negative-binomial hurdle likelihood**. It is **not** a confirmatory familywise result or a population-level zero-truncation-corrected effect.

This distinction is substantive biology: even on the same original plants, the following are **different observables**:

1. Whole-plant probability of at least one initiated fruit.
2. Number of initiated fruits conditional on being in a fruit-positive stem.
3. Initiated fruit count relative to an approximate peak-bloom flower opportunity.
4. Pollinium insertions in a distinct sample of exactly ten flowers.

None on its own measures true compatibility, viable pollen germination, pollination-to-fruit transition, matured seed output or descendant fitness.

## Implication for SCH's causal identification framework

These genuine analyses reinforce a *negative control / denominator failure mode*: an apparently strong contrast between two reproductive-stage selection gradients may appear or disappear because the **fitness endpoints have different sampling opportunities and stage definitions**, rather than because a shared trait has demonstrably different causal functional optima. The original 2024 sample was not a factorial trait-manipulation experiment. The 2005 Caruso resource-supplementation paper is a different biological programme; its original treatment-by-reproductive-stage coefficients cannot be assigned the 2024 population-level covariance or combined as one common effect size.

**Do not promote** any of these stage associations, negative conditional rate coefficients, alpha-grid P values or source-model nulls to independently identified evolutionary conflict, a reproductive resource constraint, or SCH loss \(L\).

A genuine causal transition study would trace the fate of each **marked flower** under compatible pollinium insertion versus no effective insertion, its actual fruit initiation and abortion under independently varied resource availability, and controlled variation of the same focal trait. A selection opportunity defined at the level of **the same individual flower and same time window** is the missing source unit.

### Reproduction and scope

- \`scripts/analyze_sch_milkweed_2024_nb2_two_part.py\`: original source checksum, NB2 stage-specific working means, manual block-cluster cross-stage sandwich, predeclared alpha sensitivity, fruit-presence/positive-only regressions and 499 exact-ID bootstrap.
- \`data/SCH_MILKWEED_2024_NB2_TWO_PART_RESULTS_V1.csv\`: ten original trait-specific source coefficients and independent-outcome uncertainty.
- \`.github/workflows/sch_milkweed_2024_nb2_two_part.yml\`: exact original publisher-source checksum verifications using a prior repository source artifact when publisher temporarily returns HTTP 500. Numeric source JSON and original XLSX are retained as CI artifacts.
- 137 earlier environment-matched selection pairs, 572 original meta master coefficients, and canonical SCH *New Phytologist* Viewpoint content are unchanged.

**Status:** \`NB2_POST_FLORAL_EXPOSURE_STAGE_DIFFERENCE_UNDETECTED; LOGISTIC_ANY_FRUIT_TRACKS_DISPLAY_IN_UNADJUSTED_ANALYSIS; NEGATIVE_POSITIVE_SUBSET_PER_FLOWER_SLOPE_EXPLORATORY_CONDITIONING_SENSITIVE; CAUSAL_COMPONENT_CONFLICT_NOT_IDENTIFIED\`.
