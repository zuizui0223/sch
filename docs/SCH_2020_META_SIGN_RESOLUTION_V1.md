# The missing inferential step in 137 paired plant-selection gradients

## Scientific question and source

**How much of the reported environmental sign-switching in directional plant selection is itself statistically resolved?** This is a direct new calculation on the **137 source-matched original published trait/treatment pairs** in the Caruso, Maherali & Martin (2020) experimental plant-functional-trait database (dataset DOI **10.5061/dryad.sn02v6x0q**, original master MD5 **7f680c344c0a418a3d8742649de24d52**). The master comprises 572 source rows, 43 original paper IDs and 46 named species; the eligible 137 paired gradients originate from 26 independent original papers and 34 species.

These exact 137 records, original article/trait identity and DOI are retained in \`data/SCH_2020_FUNCTIONAL_META_MATCHED_ORIGINAL_PAIRS_V1.csv\`. The author's deliberately duplicated 1,014-row analysis table and separate 815-row observational table are NOT appended. This work uses **published individual slope-and-SE estimates**, not new experimental plant-level measurements.

## Result 1 — Point sign changes do not imply two confirmed opposed slopes

Across **137** matched treatment pairs, **41** original fitted selection gradients change sign. These 41 occur across **15 of 26 original papers**, not 41 independent species or experiments.

Individual two-sided source-SE normal-Wald diagnostics at **|beta|/SE > 1.96** show:

| Status of opposite-sign source point slopes | Matched source comparisons |
|---|---:|
| BOTH original treatment slopes nominally nonzero and opposite | **0** |
| Exactly ONE original treatment slope nominally nonzero | **13** |
| NEITHER original treatment slope nominally nonzero | **28** |
| **Total point sign changes** | **41** |

The distinction matters biologically. A fit β₁>0 and β₂<0 can occur when one or both source slopes have broad uncertainty overlapping zero; the source alone then does **not establish two different directional selective regimes**. These are original source marginal-SE checks; they are **not direct author fitted treatment×trait interaction P tests**, do not account for within-study coefficient covariance, and have not been certified for simultaneous familywise multiple comparisons. The complementary direct-interaction QA remains documented separately in \`docs/SCH_GLOBAL_FUNCTIONAL_TRAIT_META_EMPIRICAL_V1.md\`.

No source-supported two-arm reversal is detected in this selected compilation. That is **not a claim of absence of real reversals or an ecological frequency estimate**. It is not a prevalence estimate for natural plant systems: **one source paper can contribute multiple correlated trait comparisons**, which do not create independent experimental replications.

## Result 2 — What precision would be needed if source betas did not change?

For each of the 41 strictly opposite sign beta pairs, calculate each treatment's absolute source z-score \`zᵢ=|βᵢ|/SEᵢ\`. A source-value-only **counterfactual information multiplier** needed for both arm slopes to exceed 1.96 is:

    m_min = [1.96 / min(|β₁|/SE₁, |β₂|/SE₂)]².

This exact algebra holds **only if the original fitted beta point values remain fixed** and their SEs shrink like 1/sqrt(n). It is deliberately **not a power analysis**, a field sample-size recommendation, an ecological prediction, a causal result, an estimate of trait variance, or a biologically meaningful effect ratio. The original source models often contain highly unequal fitness scales and correlated source estimates; future effect-size estimates could move.

**Actual numerical source receipt (41 sign-crossing pairs):**

- Lower quartile m_min ≈ **8.64**; median ≈ **15.37**; upper quartile ≈ **158.76**.
- Only **3/41** would clear individual two-arm nominal sign support with at most 2× hypothetical information, **6/41** with ≤4×, **21/41** with ≤16×.
- **12/41** need more than a hypothetical 100-fold information multiplier under this frozen-beta algebra.
- The source point β's were not obtained by randomly assigning trait coordinates, and one paper may contribute several trait axes. Neither these ratios nor 41/137 are a study-independent natural prevalence.

The large and heterogeneous precision demands show **why the sign-crossing total alone is not convincing evidence of frequent conflict**. They do not establish whether the problem in any original study is low effective sample size, inaccurate point estimates, unmeasured fitness pathways, missing source covariance, differing phenological windows or genuine biologically small antagonistic selection.

## Result 3 — Specificity requires studies that overlap in trait class and manipulation

The original source meta has five defined trait domains. The 137 pairs include **physiology 22 (11 point sign changes), plant size 39 (7), and phenology 53 (16)**. The apparent greater rate in physiology than in size cannot be promoted to a macroecological causal trait-class effect: study taxa, publication, experimental setting and environmental driver differ, and only a subset of original papers tested both domains. Analysis must compare within-original-paper domains or obtain a broader source-confirmed meta sample before any cross-trait biological generality claim.

The prior 26-paper source-agent comparison also failed its registered macro claim: paper-level biotic-vs-abiotic sign-crossing fraction contrast **−0.101** with whole-paper conditional permutation **p=0.3996**, and abiotic studies lacked in-situ controls entirely. Those results remain unchanged.

## Consequence for SCH's empirical paper

This is an **original, reproducible quantitative uncertainty/precision audit of published study data**, not an original field-selection experiment, a systematic comprehensive 2026 meta-analysis, a null proof, or an experimentally identified SCH conflict L.

The solid conclusion is methodological and ecological in scope:

> Across 26 original experimental publications, observed sign-crossing of total selection gradients is common in point estimates but never doubly source-SE-supported as two opposed slopes; most crossings involve *two* statistically unresolved arm slopes. The inferential gap is not closed by counting trait coordinates or by a study's interaction P alone.

A publishable stronger empirical answer requires **direct author-fitted trait×intervention gradients and covariance structures** across a defined biological manipulation/fitness class; the pilot's original Beans & Roach direct contrast QA already demonstrates why subtracting marginal source SEs cannot replace primary study interaction tests.

### Reproduction

Code: \`scripts/audit_sch_2020_meta_sign_resolution.py\`

Original verified 137 records: \`data/SCH_2020_FUNCTIONAL_META_MATCHED_ORIGINAL_PAIRS_V1.csv\`

Prior source receipt: \`data/SCH_2020_FUNCTIONAL_META_EXPERIMENTAL_READOUT_V1.json\`

New output: \`data/SCH_2020_META_SIGN_RESOLUTION_V1.json\`

Tests: \`tests/test_sch_2020_meta_sign_resolution.py\`

This analysis does not alter the SCH New Phytologist Viewpoint, earlier H2 frozen holdouts, or down-stream SLK and BITA theoretical estimands.
