# Four independent plant programmes: a full spectrum of pollination-dependent selection

## Central ecological question

When pollination conditions change, **how often do the published estimates simply change sign, exhibit individually well-supported opposite directions, or demonstrate an actual between-regime difference on the same trait?** These are biologically different quantities and must be distinguished before attributing any "trade-off" to pollinators.

This is a transparent **secondary exploration on sources already frozen** in SCH, not a newly registered primary test, fresh raw field measurements, ecological prevalence estimate, or replacement of the earlier V26/V27 H2M1 heldout class analysis.

## Original sources and source-grain

Two source objects are used, each strictly tied to original published coefficients:

1. Frozen V27 pollination programmes: Dactylorhiza lapponica (doi:10.1111/j.1469-8137.2010.03296.x, five floral traits, source 2010), Primula alpicola (doi:10.1038/s41598-017-13340-0, four traits, source 2016 year), and Trillium discolor (doi:10.1002/ajb2.16101, two 2020 and three 2021 trait-year pairs). These remain **14 complete within-year trait contrasts** and **three biological studies**.
2. Original four-treatment 2015 Gymnadenia conopsea factorial table (Sletvold, Moritz & Ågren, doi:10.1890/14-0119.1, Ecological Archives Table A2): five phenotypic traits × TWO fixed-herbivory backgrounds = **ten open versus hand-supplemented pollination pairs** in **one** independent experiment. The two herbivory backgrounds are NOT two studies and the ten pairs are NOT ten independent traits.

Hence there are **24 within-trait, within-source, fixed-herbivory/year treatment edges in four independent programmes**. No contrasts are selected by source sign or P; all source-eligible cases stay in the family. The study programmes differ in relative fitness definition and sometimes model-link scale, so their beta magnitudes are not pooled.

## Three separate tests of ecological response

For each matched pair:

- **POINT SIGN CHANGE**: beta_open × beta_hand < 0, regardless of statistical precision. This is descriptive only.
- **BOTH DIRECTIONS SUPPORTED**: beta_open and beta_hand have opposite signs and each exceeds |beta/SE| > 1.96 in its own original treatment cell. This is a *nominal, individually cell-supported diagnostic*, NOT a 24-edge familywise reversal test.
- **TREATMENT-ASSOCIATED DIFFERENCE**: beta_open − beta_hand has a conservative 24-edge Bonferroni normal-Wald interval that excludes zero when using its maximum possible SE, SE_open + SE_hand. The SE bound holds under arbitrary covariance, but still needs valid original SEs and a normal approximation. For alpha=0.05, the 24-edge two-sided critical normal quantile is **3.07809**.

**Separate source-precision sensitivity:** every printed original coefficient and SE may vary by half its last printed decimal unit; for Dactylorhiza spur beta_open the 0.30 source precision is retained even though the frozen machine CSV abbreviates it as 0.3. A familywise difference is **decimal-rounding robust** only if the smallest compatible absolute difference exceeds 3.07809 times the largest compatible worst-case SE. This particularly matters near a multiple-comparison cutoff.

All three tests describe reported **phenotype–fitness selection gradients in manipulated pollen regimes**. None constitutes randomization of the floral phenotype itself.

## Quantitative results

| Independent biological programme | Complete matched pairs | Point signs differ | Both cell directions nominally supported | Printed-value 24-edge familywise differences | Decimal-rounding robust familywise differences |
|---|---:|---:|---:|---:|---:|
| Dactylorhiza lapponica | 5 | 3 | 0 | 1 | 0 |
| Primula alpicola | 4 | 2 | 0 | 1 | 0 |
| Trillium discolor (2020–2021) | 5 | 3 | 0 | 0 | 0 |
| Gymnadenia conopsea (natural and excluded herbivory strata) | 10 | 3 | 1 | 0 | 0 |
| **Total** | **24** | **11** | **1** | **2** | **0** |

The **sole individually bidirectionally supported reversal** is Gymnadenia flowering-start phenology under herbivore exclusion: beta_open = +0.094 (SE .031), beta_supplemented = −0.066 (SE .028), source significance P<0.01 and P<0.05, respectively. Its difference is +.160 with maximum possible SE .059, yielding nominal normal P upper approximately **.00669**. This does NOT clear the new full 24-edge 5% Bonferroni bound (upper adjusted P approximately **.1606**). The previously reported conditional single-edge result and 20-edge source-family caveat remain unchanged.

Under the *exact numbers as printed*, two other contrasts narrowly clear the complete 24-edge family:

- Dactylorhiza **spur length**: open − supplemental beta **+.324**, worst SE **.105**, nominal Bonferroni 24-edge P upper approximately **.0487**.
- Primula **flowering start**: open − supplemental beta **+.206**, worst SE **.066**, nominal Bonferroni 24-edge P upper approximately **.0432**.

**Neither is certified under the stronger source-decimal-rounding envelope for the expanded 24-edge family.** This differs from the previously published 14-edge sensitivity, under which both were robust to source rounding. That difference is a consequence of *adding ten comparisons to the multiple-testing family*; it is not a biological change or contradictory field observation.

Trillium 2020 petal-size printed pairwise difference **−4.41** (SE upper 1.49) no longer clears the 24-edge worst-covariance reconstruction; source Table 1 nonetheless directly reports an independently fitted treatment contrast with SE **1.23**, P<0.0001. This remains authentic original source evidence, but is a different method from our conservative interval constructed from printed separate-cell SEs. The source's 2020 display-height delta/arm coefficient inconsistency remains uncorrected and explicitly documented in the preceding V27 audit. Trillium's 2020/2021 pair rows are not counted as independent experiments.

## Ecological meaning: a response spectrum, not one prevalence number

The source-based evidence supports two *complementary* propositions:

**1. Sign change is not the same as a demonstrated reversal.** Eleven of 24 **point-estimate** pairs change sign, but only one pair has significant opposite directions in both original cells at an ordinary nominal threshold; even that is not a 24-edge familywise reversal certificate. This pattern illustrates that simply comparing the signs of estimated selection coefficients exaggerates what the source actually identifies.

**2. A change in the selection gradient can matter without a bidirectionally supported reversal.** Dactylorhiza spur length and Primula flowering time have strongly different open-versus-supplemented source values and original-study pollinator-mediated selection findings, although their supplemented-treatment signs are individually unsupported. Full 24-edge simultaneously protected inference becomes sensitive to how precisely their original standard errors were printed. Trillium supplies a distinct original source-reported treatment contrast on a different model scale. A nondetected or near-zero gradient in one arm should therefore NOT be treated as evidence that the ecological interaction made no difference.

This is *not* a sample of four randomly chosen natural systems. The 11/24 and 1/24 counts are not species-level or evolutionary prevalence rates, and even the 24 comparisons are dependent within studies. Adding many repeated axes does not create more independent ecological programmes.

## Relation to SCH's causal ladder

The source papers manipulated **pollination regime**, and Gymnadenia also manipulated **herbivory regime**. All focal floral traits were observed natural phenotypic variation; their realized exsertion, spur length, petal size or flowering time were NOT randomized directly. Hence no study here identifies a complete z × P × G causal fitness surface, pure function-specific optima, SCH conflict budget L or SLK architecture value.

The original sources are heterogeneous:

- **Gymnadenia** is the valid two-factor ecological regime study; the same system has opposite responses on phenology and reinforcing contributions on spur length. Those five axes are repeatedly measured within ONE experiment.
- **Dactylorhiza** supplies a pollination-modified selection gradient without established two-agent conflict.
- **Primula** compares open plants including two style morphs to supplemented long-styled plants only; selection differences retain a morph-composition identification caveat.
- **Trillium** uses source conditional Poisson gradients across two years. Those values cannot be numerically pooled with linear selection coefficients.

Consequently the biological contribution is a **trait-axis-specific interaction-sensitivity spectrum** across real independently executed studies, while the inferential conclusion is correspondingly narrow: different definitions of "selection changed" yield different counts, and claims of generic functional trade-offs demand direct, synchronized consumer and trait manipulations.

## Reproducibility

Canonical frozen source files:

- data/SCH_H2_HOLDOUT_V27_NUMERIC_SOURCE_FREEZE.csv
- data/SCH_H2_HOLDOUT_V27_OUTCOME_READOUT.json (unaltered)
- data/SCH_H2_GYMNADENIA_A2_SELECTION_GRADIENTS_V1.csv

New script:

- scripts/audit_sch_four_programme_selection_spectrum.py

Verification:

- tests/test_sch_four_programme_selection_spectrum.py

Run from repository root:

    python scripts/audit_sch_four_programme_selection_spectrum.py

This outputs all 24 source-identified contrasts, per-programme counts, unadjusted conservative P upper bounds, full 24-edge Bonferroni bounds, decimal-rounding robustness, and explicit limits. The original 14-edge V27 secondary result, heldout H2M1 classes, quantitative pooling gates and SCH L promotion gates remain untouched.
