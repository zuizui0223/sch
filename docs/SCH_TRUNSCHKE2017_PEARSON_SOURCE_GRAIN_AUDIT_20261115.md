# SCH original published correlation audit: independent 12 orchid populations versus printed P-values (2026-11-15)

## Executable new *published-number* calculation, not a raw-data refit

Trunschke, Sletvold & Ågren (2017), *New Phytologist* 214:1381–1389, DOI [10.1111/nph.14479](https://doi.org/10.1111/nph.14479), state that the species/population-level sample contains **12 orchid populations** (one studied population for each of 12 species). The main article's section *Variation in phenotypic traits, pollen limitation and opportunity for selection* prints correlations between population mean traits and population pollen limitation (PL). The flowering-start correlation explicitly says **n=12**; other four trait comparisons are in the same 12-population paragraph. **Those are original reported source r and P, not a new regression of underlying 2013 plant observations.**

Independent arithmetic tests the exact two-sided Pearson t distribution from the printed three-decimal r:
`t = |r| sqrt((n−2)/(1−r²))`, `P = 2*Pr(T_(n−2) >= t)`.

| Trait | Original printed r | Original printed P | Independent n=12 two-sided Pearson P | n=24 diagnostic P (NOT established original n) |
|---|---:|---:|---:|---:|
| Flowering start | −0.763 | <0.001 | **0.003893** | 0.0000145 |
| Plant height | −0.784 | <0.001 | **0.002543** | 0.00000582 |
| Flower size | −0.428 | 0.040 | **0.165133** | 0.036939 |
| Number of flowers | −0.325 | 0.116 | **0.302654** | 0.121241 |
| Spur length | −0.337 | 0.111 | **0.284089** | 0.107325 |

This is a **source-provenance discrepancy**: the five P labels are not reproducible under the conventional two-sided Pearson test of 12 independent populations and the reported rounded r. The n=24 diagnostic column is numerically closer, compatible with a possible use of two pollination-treatment means per species, but **this audit does not prove that the authors used 24 observations, duplicated population PL or committed pseudoreplication**. Original calculation code or raw input grain would be needed for causal attribution of the discrepancy. The independent n=12 result for flower size is P≈**0.165**, not a nominally significant P=.040. The r ±0.0005 rounding envelope does not bridge the difference.

## Internal negative control: not every original PL P-value is incompatible

The same published Figure 2 reports across **12 populations** a relation of PL to open-pollinated opportunity for selection with **R²=0.63, P=0.002**. Taking `|r|=sqrt(0.63)` gives a two-sided Pearson P≈**0.00206** for n=12, which is consistent with its printed P. This does **not** show an article-wide testing error; the discrepancy is currently limited to the five published morphological-trait correlations audited above.

The published **PL versus pollinator-mediated selection** source ANCOVA (Table 4, F=18.79, P<0.001) is **not the same analysis as these five Pearson tests**. It remains one original published result, not recalculated or automatically invalidated here. However, it uses 12 biological species repeatedly across five trait axes (df residual 50), and a species-cluster robust re-estimation is still an outstanding issue.

## Additional source-observed ecological contrast: reward strategy and the high-PL tail

The original 2017 article describes **six rewarding and six deceptive species**. Its Results/Discussion partitions the 12 populations as:

| Population group | PL above 0.8 | PL below 0.4 |
|---|---:|---:|
| Deceptive / rewardless orchid species | **5** | **1** |
| Rewarding orchid species | **0** | **6** |

There are **zero** studied species in the intermediate PL interval (0.4–0.8). A conditional 2×2 exact Fisher calculation on this **post hoc published partition** gives two-sided **P = 0.01515**. This is an exploratory calculation on **12 published categories**, not a newly collected biological outcome, a species-wide evolutionary causal effect, or a preregistered threshold. It supports the descriptive fact that the studied high-PL extreme co-occurs with rewardlessness. It does not show how selection varies *within* either strategy, which would require Table S5/S6 individual population values.

The large gap in PL implies that **intermediate response geometry is not empirically sampled in this 2017 system**. A near-linear across-species relationship between PL and selection intensity cannot, from these two distinct PL regimes alone, distinguish a continuous PL effect from strategy, phylogeny, phenology or community context differences.

## Claim ceiling and follow-on

- **New calculation now reproducible**: conventional two-sided Pearson P for five originally published r at n=12, alternate n=24 diagnostic P, and exact published reward×PL 2×2 Fisher under post hoc group definitions.
- **Not recovered**: actual original observational units/covariance for those r; full species×trait gradients; true regression model and degree-of-freedom selection in the source; any species-level leave-one-out PL-selection association.
- **Not changed**: original 2017 source author ANCOVA, 2014/2016 experimental ecology, SCH 137-pair mega compilation, New Phytologist Viewpoint, `L` and functional optima.

Source original supplement S5/S6 is officially listed but CI publisher requests produced HTTP 403 (recorded in `docs/SCH_TRUNSCHKE2017_S5S6_ACCESS_BOUNDARY_20261115.md`). The original Dryad XLS is similarly restricted in CI, with exact file MD5 pinned (see `docs/SCH_ORCHID_2017_RAW_ORIGINAL_ACCESS_BOUNDARY_20261115.md`). Do not re-label source-correlation calculations as a completed independent raw-data refit.

Run:

    python scripts/audit_sch_trunschke2017_pearson_grain.py --output artifacts/sch_trunschke2017_pearson_grain_v1.json
    python -m pytest -q tests/test_sch_trunschke2017_pearson_grain.py

**Status: CONDITIONAL_PEARSON_P_DISCREPANCY_IDENTIFIED; FISHER_REWARD_PL_ASSOCIATION_DESCRIPTIVE; 12_SPECIES_RAW_DATA_NEEDED_FOR_CAUSAL_GRANULARITY.**
