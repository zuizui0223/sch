# SCH original-author context audit V2 (2026-11-15)

## Purpose: measure the original author's actual treatment × trait tests

This is a bounded source-level extension to the existing **137 matched treatment pairs from 26 published papers**. It adds no new field observations, no new independent biological programmes, and no inferred SCH conflict loss L. It joins the original author-fitted interaction results to immutable compiled row IDs, rather than mistaking a point sign crossing or a reconstructed two-SE contrast for the source author's fitted statistical test.

Primary sources:

- Beans & Roach (2015), *American Journal of Botany* 102:217–224, DOI 10.3732/ajb.1400355, original Table 2: https://bsapubs.onlinelibrary.wiley.com/doi/10.3732/ajb.1400355
- Stinchcombe et al. (2002), *The American Naturalist* 160:511–523, DOI 10.1086/342069, original Table 2: https://people.duke.edu/~mrausher/Stinchcombe_et_al_2002.pdf
- Compiled matching keys: data/SCH_2020_FUNCTIONAL_META_MATCHED_ORIGINAL_PAIRS_V1.csv, original published source IDs 204–219 and 495/496.

## Positive finding: opposite changes in selection strength across different traits

For Beans & Roach, we recovered the entire **8比較** original Table 2 matrix: four greenhouse interaction tests and four field manipulation tests. All eight match the stored source β/SE and individual row IDs in the existing 137-pair ledger.

| Study | Trait | Invasive absent β ± SE | Invasive present β ± SE | Original author interaction |
|---|---|---:|---:|---|
| Greenhouse | Number of internodes | +0.140 ± 0.010 | +0.360 ± 0.020 | F=82.74, P<0.0001 |
| Greenhouse | First internode length | +0.150 ± 0.020 | +0.040 ± 0.020 | F=8.35, P=0.005 |
| Greenhouse | Early growth rate | +0.090 ± 0.020 | +0.003 ± 0.002 | F=4.38, P=0.040 |
| Field removal | Early growth rate | +0.150 ± 0.030 | −0.090 ± 0.110 | F=3.93, P=0.049 |

The original eight-test p-value family has a conservative Bonferroni cutoff of 0.05/8 = **0.00625**. Exactly **2形質**, both greenhouse internode-related traits, pass:

- **Number of internodes:** Δβ (competitor present − absent) = **+0.220**. Positive selection becomes stronger.
- **First internode length:** Δβ = **−0.110**. Positive selection becomes weaker, not significantly negative.

These results demonstrate **trait-specific reweighting of phenotypic selection associations** under the same invasive competitor. It is not a uniform selection-strength increase and not proof of two functions in conflict on the same trait coordinate.

The other four original tests, including both nonsignificant greenhouse/field traits, remain in the source CSV. There are **4/8 nominal original author interactions**, **2/8** surviving this eight-test threshold and **1** under the exploratory 0.05/137 benchmark. Those ratios are *not* population prevalence or multiple independent species: these are eight dependent axes/context contrasts from **同一論文**.

The field early-growth direct interaction P=**0.049** is nominally detectable. It has a point sign crossing (+0.15 to −0.09) but the negative selection gradient is imprecise (SE 0.11), so it is **not a two-arm supported sign reversal**, and it fails the eight-test cutoff. In greenhouse, early-growth contrast is also nominally supported at P=0.040, but the two ecological settings are not exact replications of each other's sampling/treatments.

**Scientific ceiling:** the environment/competitor treatment is manipulated, not the trait itself. Original phenotypic gradients remain associations between traits and fruit number. The trait-specific response is genuine original-source evidence of changes in *realized selection associations*, not heritable change, separated functions, causal functional optima, or L.

## Critical primary-estimand guard: Stinchcombe is NOT a source direct insect × leaf-area test

The *Ipomoea hederacea* pair (source rows 495/496) has:

| Original 2002 Table 2 regime | Standardized phenotypic βp' ± SE | Standardized genotypic βg' ± SE | Original author's within-regime bias test P |
|---|---:|---:|---:|
| Insects absent | +0.790 ± 0.030 | +0.018 ± 0.060 | 0.052 |
| Insects present | +0.044 ± 0.050 | +0.020 ± 0.050 | 0.76 |

Stinchcombe's two published Table 2 P-values compare **phenotypic versus genotypic selection estimates within each insect regime**, testing environmentally induced bias. Neither is an original author-fitted treatment × leaf-area P-value. The 2002 source warns that separate trait standardizations can make even phenotypic-versus-genotypic slope differences misleading.

The earlier published compilation's phenotypic point difference −0.746 is an arithmetic difference. Its previously reconstructed marginal-SE Bonferroni P upper bound 1.52×10^−18 does **not** substitute for a verified original study-level insect × trait interaction, nor for heritable evolutionary selection. This is an **estimand mismatch**, not proof that the leaf-area difference was environmentally biased or that a true insect effect does not exist. The exact primary direct interaction remains unrecovered.

## Research consequence

The supportable SCH statement from the new original-author check is:

> A single experimentally changed competitor regime can strengthen selection on one vegetative trait and weaken it on another, without either response requiring sign reversal. Original author-fitted interaction testing and two independently supported opposing selection gradients are different evidential standards.

For publication, this remains a specific previously published biological study with a new source-validated evidence readout, **not** a new cross-study law. Only one original author interaction currently survives the 137-comparison sensitivity benchmark; the 26-paper general effect remains unresolved. It does not identify the same-coordinate functional conflict, 機能別最適値, or shared-trait compromise loss L.

No 137-pair classification, previous publication result receipt, NPH Viewpoint, or holdout denominator was changed.

## Reproduction

Run:

    python scripts/audit_sch_primary_fitted_context.py --output artifacts/sch_original_primary_context_v2.json
    python -m pytest -q tests/test_sch_primary_fitted_context.py

Source matrices: data/SCH_2020_BEANS_ROACH_AUTHOR_INTERACTIONS_V2.csv and data/SCH_2020_STINCHCOMBE_TABLE2_ESTIMAND_V1.csv. The auditor fails closed on altered primary F/P values, source row IDs, original β/SE, context labels, or mistaken primary test estimands.
