# SCH: selection can change strongly without reversing its direction

## Biological question

Does the scarcity of **bidirectionally supported sign reversals** imply that pollination changes have little evolutionary impact on floral traits? The three independently published and prospectively design-classified programmes already frozen in SCH's V26/V27 outcome set allow a stronger source-defined secondary test: is **the magnitude of within-year, same-trait selection** different under open versus hand-supplemented pollination?

This is an **exploratory cross-programme contrast analysis**, not a refit of individual plants, not a new literature search, and NOT the preregistered H2M1 class comparison. No new programme has been added; the fourth registered Impatiens programme still lacks the requisite numerical uncertainties and is not silently treated as a negative outcome.

## Complete study-defined comparator family

The full source-eligible same-year *open versus supplemented* selection-gradient family has 14 contrasts in **three independent studies**, not 14 independent biological experiments:

| Programme and source | Independent same-year floral contrasts | Source response family |
|---|---:|---|
| Dactylorhiza lapponica, Sletvold, Grindeland & Ågren (2010), doi:10.1111/j.1469-8137.2010.03296.x, original Table 3 | 5 | Standardized linear selection |
| Primula alpicola, Chen, Zhang & Li (2017), doi:10.1038/s41598-017-13340-0, original Table 2 | 4 | Standardized linear selection |
| Trillium discolor, doi:10.1002/ajb2.16101, original 2020 Table 1 and 2021 Table 2 | 5 (2 from 2020, 3 from 2021) | Conditional Poisson-model linear selection |

The selection contrast is **beta(open) minus beta(supplemented)**, within the same trait, same study, and (where necessary) the same year. Poisson-model values from Trillium are never pooled with selection-gradient values from the other two programmes. The registered V27 holdout classification and original 0, 0, and 2/3 supported all-context reversal rates **remain unchanged**.

## Independent-uncertainty and multiple-comparison bound

For a contrast of two source estimates, the unknown covariance cannot make its SE exceed the sum of the two reported SEs:

    Delta = beta_open - beta_supplemented
    SE(Delta) <= SE_open + SE_supplemented

For each of **all 14** matched source-eligible edges, compute the standard-normal approximation with this worst-case SE; use a two-sided simultaneous Bonferroni threshold alpha/14. Its critical normal quantile is approximately **2.913726** at familywise alpha=.05. This is a conditional asymptotic interval: the source coefficients and their reported SEs must refer to comparable parameters and be valid. Nothing here reproduces the original authors' treatment-interaction ANCOVA or Poisson model.

### Results from published numeric coefficients

| One treated trait and source year | Open beta (SE) | Supplemented beta (SE) | Open minus supplemented | Worst SE | 14-edge adjusted P upper bound | 95% familywise normal interval |
|---|---|---|---:|---:|---:|---|
| Dactylorhiza spur length (2010) | +0.300 (0.068) | −0.024 (0.037) | +0.324 | 0.105 | 0.0284 | [+0.0181,+0.6299] |
| Primula flowering start (2016 field season, 2017 paper) | +0.194 (0.035) | −0.012 (0.031) | +0.206 | 0.066 | 0.0252 | [+0.0137,+0.3983] |
| Trillium petal size (2020 field season) | −3.94 (1.2) | +0.47 (0.29) | −4.41 | 1.49 | 0.0431 | [−8.7515,−0.0685] |

The first two are stable to independently bounded decimal rounding of original source beta and SE values. The Trillium printed-data-only familywise confidence interval barely excludes zero, but the original 2020 published SE=1.2 is printed to **one decimal**, and the conservative source rounding envelope raises its worst possible SE to **1.545**, reducing the least possible absolute point contrast to **4.40**. Under that more adversarial envelope, the recreated 14-edge bound **does not certify** Trillium. This sensitivity must NOT be hidden. Independently, the Trillium authors publish an original 2020 petal-size pollination-treatment contrast of **−4.41 (SE 1.23, P < 0.0001)** in Table 1. That directly fitted source result strongly supports a treatment contrast even under 14-test Bonferroni, *conditional on the published model test*, but it is not a result derived from our unknown-covariance reconstruction.

The 2020 Trillium **display-height** row also has an internal source-table warning: printed beta(open)=2.96 and beta(supplemented)=−0.13 imply arithmetic open-minus-supplemented **3.09**, whereas the same table's displayed pollinator-mediated Delta value reads **−2.83**. No attempt is made to silently repair the authors' published model using guessed missing quantities. This axis is **not** one of the positive 14-edge conservative results.

## What is new to SCH

The important comparative ecological distinction is between **selection-gradient modification** and **complete supported sign reversal**.

In the original V27 holdout, none of Dactylorhiza's five or Primula's four axes has opposite statistically supported treatment-cell gradient signs. Trillium's two all-context supported reversals occur across year/context combinations, not within a single-year pollination-treatment pair (within-year diagnostic 0/3). Nevertheless, across all fourteen within-year comparisons, treatment-associated differences in *selection magnitude* are identifiable in each of the three programmes based on the printed source coefficients plus conservative covariance bounds (with the rounding limitation above).

Thus the empirical conclusion is **not** “pollination produces universal selection reversals” or “3/3 implies 100% natural prevalence.” It is narrower and biologically consequential:

> Meaningful changes in floral selection can be detected across independent pollination-manipulation programmes even when the sign-reversal criterion remains unmet. A weak or nonsignificant supplemented-cell gradient is not evidence of unchanged selection relative to open pollination.

The results are supported within each study's own fitted scale; a numerical pooled treatment effect, independent study selection probability, universal direction, shared trait optimum, SCH conflict loss L, and SLK architecture value remain **not identified**.

## Design caveats that change how far to interpret the three systems

- **Dactylorhiza:** The published source estimates a strong pollinator-mediated spur-length effect and finds fruit herbivory contributed little to floral selection at that study site. It is NOT an example of independently manipulated pollinator versus herbivore conflict. Original trait-by-treatment P for spur length is <0.0001.
- **Primula:** The experiment randomly assigned both long- and short-styled plants to open pollination, but only long-styled plants could receive supplemental pollen without damage. Its analyzed open group contains **both morphs** (182 long-styled and 169 short-styled after losses), while the supplemented group contains **165 long-styled plants only**. The authors report no detected morph differences for most traits, but this does not demonstrate equivalence of all morph-specific trait–fitness slopes. The contrast is therefore a strong *published treatment-associated selection* signature, with a residual morph-composition identification caveat. Source article reported an original interaction indicating pollinator-mediated flowering-start selection (Delta beta=+0.206, P<0.05).
- **Trillium:** The 2020 petal result uses the conditional Poisson model of seed number (not a common cross-species Gaussian selection coefficient), and **2020 and 2021 do not count as separate independent study programmes**. Original paper reports P<0.0001 for the 2020 petal selection contrast. The 2020 display-height printed-value inconsistency and one-decimal petal-size SE must remain visible.
- **2019 Primula correction:** doi:10.1038/s41598-019-43381-6 corrects Figure 1 line styling and a Table 3 pollinator-mediated correlational-selection symbol, NOT the Table 2 flowering-start linear beta/SE that is used here. The corrective notice was checked before promotion.

For all three, treatment assignment changes ecological conditions, but **flowering time, spur length, and petal size were not experimentally set to random values**. The selection gradient within a treatment remains a phenotype–fitness association. These comparisons do not identify pure-function optima, do(z) trait effects, individual evolutionary responses or an adaptive time trend.

## Reproducible boundaries

Code: scripts/audit_sch_h2_cross_programme_pollination_edges.py

Frozen primary data: data/SCH_H2_HOLDOUT_V27_NUMERIC_SOURCE_FREEZE.csv

Untouched V27 readout: data/SCH_H2_HOLDOUT_V27_OUTCOME_READOUT.json

Regression: tests/test_sch_h2_cross_programme_pollination_edges.py

To calculate all 14 cases:

    python scripts/audit_sch_h2_cross_programme_pollination_edges.py

This creates a secondary reporting object only. There are no additional independent biological clusters, no changed original H2M1 classes, and no newly collected field data.
