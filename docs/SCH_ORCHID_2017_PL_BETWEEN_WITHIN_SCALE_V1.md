# SCH: pollen-limitation / selection across ecological scales — direct source audit (2026-11-15)

## New source-verified quantitative ecological conclusion

A high-value **positive within-study, between-species** result is recoverable from Trunschke, Sletvold & Ågren (2017), *New Phytologist* 214:1381–1389, DOI **10.1111/nph.14479**, original ANCOVA Tables 2 and 4: https://nph.onlinelibrary.wiley.com/doi/10.1111/nph.14479.

The source compared **12 orchid species** (one sampled population per species, Öland, Sweden) under open versus supplemental hand pollination, with five plant/floral trait axes each. For each species and treatment the traits were standardized to mean 0 and variance 1 and relative female fitness was calculated from individual fitness divided by mean fitness. The authors fitted original trait × pollination treatment and trait × species × treatment ANCOVAs; the response family must remain separate from the original Caruso experimental-meta source paper ID 33 flowering-start pairs.

**Published Table 4 PL association F statistics (source model df=1,50):**

| Selection strength definition | Direct author F for pollen limitation | Published P | Interpretation |
|---|---:|---:|---|
| ABS net selection magnitude abs(beta open) | **6.374** | **0.015** | Within 12 species, higher PL associated with stronger net selection |
| ABS pollinator-mediated selection abs(beta open − beta supplemented) | **18.79** | **<0.001** | Within 12 species, higher PL associated with stronger pollinator-mediated selection |
| ABS nonpollinator selection abs(beta supplemented) | 0.0045 | 0.947 | No detected association (NOT equivalence to zero) |

Assuming the original ANCOVA P-values are valid, the first two associations also pass a *post hoc transparent three-component* Bonferroni sensitivity (alpha 0.0167). **This does not resolve nonindependence across the five traits per species in the original 60 species-trait data points**. The primary analysis error df=50 is not 50 independent species: there are 12 species, all sampled in the same published programme. A true species-cluster sensitivity is not computed yet and is required before a strong cross-species generality claim.

**Published Table 2 direct treatment × trait terms** also establish experimental pollination-context selection effects. The original flowering-start × treatment effect is F=6.62, P=0.010. More notably, plant height × species × pollination treatment is F=2.55, P=0.003, and number of flowers × species × treatment F=2.37, P=0.007. At the explicitly *post hoc* ten-test family cutoff 0.005, only the height × species × treatment interaction passes. These original ANOVA interaction terms establish context sensitivity of phenotypic selection associations, not two function-specific experimental optimum surfaces.

## Why the 2014 result is not contradicted

Sletvold & Ågren (2014), *Evolution* 68:1907–1918, DOI **10.1111/evo.12405** (https://onlinelibrary.wiley.com/doi/10.1111/evo.12405), sampled **two orchid species** across **14 population × year estimates**: *Gymnadenia conopsea* (9) and *Dactylorhiza lapponica* (5). Within each species, PL did **not** explain variation in pollinator-mediated selection on the individual traits in that original study. The authors did find a relationship in cross-species contrasts and noted that local trait–pollination-success covariance can vary independently from the mean PL.

The 2017 finding is a **between-species comparison of different populations**, whereas the 2014 nonassociation is **within-species across populations and years**. These are different conditioning sets, scales, populations, year periods, and trait arrays: their effects cannot be pooled as if contradictory estimates of one fixed slope. Both studies share some orchid taxa but not an identical independent population-year. A new hierarchical mixed-scale analysis would require original population-level raw PL and trait-selection estimates across both programmes, common trait definitions, proper covariance and study separation. One study cannot supply 12 independent studies, and 14 population years cannot become 14 species.

A viable SCH biology-first hypothesis is that **interaction intensity sets opportunity for selection at the among-species scale, while the mapping from trait to realized pollination success dominates within-species fluctuations**. This is **hypothesis generating**, not a causal mediation result or a demonstrated scale interaction. Selection is computed from phenotypic fitness associations under experimentally changed pollen supplementation, not randomized phenotype assignments.

## Evidence-grain integration, not 12 new independent programmes

The Caruso et al. 2020 published compilation contains 12 matched coefficient pairs for paper ID **33**, representing **12 species but only the flowering-start trait** (source author's original study has five trait axes). The current 137-pair total is retained. The Table 2 source-author tests and Table 4 PL regressions are separate denominators and cannot become +10 or +9 independent treatment pairs. Test family denominators (10 interactions / 3 selection components) are source-defined sensitivity boundaries, not new prospective registrations.

The original full individual-plant dataset is publicly listed at **Dryad DOI 10.5061/dryad.28n72**, as an original XLS plus DOCX dictionary. The original raw workbook has **not been retrieved, independently checksum-verified, or refitted in this audit**. Until then, species-cluster permutation/bootstrapping and leave-one-species-out sensitivity remain planned and must **not be reported as empirical results**.

### Current claim ceiling

- **Positive:** One original 12-species study reports stronger pollinator-mediated selection at higher PL, with strong original source ANCOVA associations; one original fitted trait-by-species treatment effect is robust to a ten-test Bonferroni sensitivity.
- **Separate negative/nondetection:** Across 14 conspecific population-years in two species, PL did not explain trait-mediated selection within species; in the 2017 study PL was not detectably associated with the nonpollinator gradient.
- **Unidentified:** a formal cross-level moderation coefficient, repeated independent multi-study universality, causal selection on experimentally randomized trait values, pure-function optima or fitness-scale compromise L.

Reproduce the pinned source-provenance and aggregation audit:

    python scripts/audit_sch_orchid_2017_selection_scale.py --output artifacts/sch_orchid_2017_source_scale_v1.json
    python -m pytest -q tests/test_sch_orchid_2017_selection_scale.py

## 日本語での主張境界

**種間**（2017年、12種×各1集団）では花粉制限と送粉者媒介選択強度の正の関連が原著で報告された。一方、**種内**（2014年、2種・計14集団×年）では同じ種類の関連が検出されなかった。生物学的スケール、時空間、モデル・標準化が違うので、両者は**共通**の推定量を扱う独立レプリケートではない。現状で種間・種内の差そのものを検定できたとは主張しない。
