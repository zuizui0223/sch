# A single ecological intervention can reverse net floral selection without a large factorial interaction

## Biological question

Must a supported reversal of natural selection on a multifunctional floral trait
require simultaneous turnover in multiple interacting agents? **No, not even
within the existing SCH empirical catalogue.**

The source-verified *Gymnadenia conopsea* experiment of Sletvold, Moritz &
Ågren (2015; *Ecology* 96:214–221, DOI `10.1890/14-0119.1`) is a four-arm,
factorial **pollination supplementation × herbivore exclusion** field
experiment. The exact five-trait × four-treatment phenotypic selection-gradient
table was previously recovered from Ecological Archives E096-022, Appendix A,
Table A2.

### Direct experimental contrast: one factor varies, the other does not

| Floral trait | Herbivory state | Open pollination β ± SE | Hand-supplemented β ± SE | Selection directions |
|---|---|---|---|---|
| Flowering start | Herbivores excluded in BOTH arms | **+0.094 ± 0.031** (source P<0.01) | **−0.066 ± 0.028** (source P<0.05) | Later versus earlier flowering |
| Flowering start | Natural herbivory in BOTH arms | −0.0042 ± 0.054 (NS) | −0.160 ± 0.056 (source P<0.01) | Near zero versus earlier |
| Spur length | Herbivores excluded in BOTH arms | +0.077 ± 0.035 (source P<0.05) | −0.042 ± 0.029 (NS) | Significant positive versus unsupported negative |
| Spur length | Natural herbivory in BOTH arms | +0.180 ± 0.057 (source P<0.01) | +0.083 ± 0.053 (NS) | Significant positive versus unsupported positive |

**Positive and negative flowering-start selection estimates, each individually
supported in the original table, occur with herbivore exclusion held fixed.**
Only pollen supplementation differs. The corresponding contrast in point
estimates is **−0.160 selection-gradient units**. The source table does **not** provide the covariance, so its **exact**
contrast SE and original factorial ANCOVA p remain unknown. However,
a sharp covariance-worst-case bound `SE(delta beta) <= 0.031+0.028
= 0.059` gives a **conditional conservative normal-Wald p upper bound
of approximately 0.0067**, with 95% interval [−0.276,−0.044].
This is a nominal single-edge result; it does not certify a
5%-family-wide finding for the **20 exploratory source-table edges**.
See `SCH_GYMNADENIA_COVARIANCE_ROBUST_GRADIENT_CONTRAST_V1.md`.

Importantly, floral phenotypes were **not themselves randomized**. The
factorially randomized manipulation changes the ecological fitness
environment, and the resulting selection coefficients are still
trait–fitness associations within treatment cells. This is direct
experimental context manipulation, **not** direct `do(z)` identification
of pure-function optima.

### Nonadditivity is not required for this directional reversal

Use the source's four treatment values for flowering start:

```text
C+H    open pollen, natural herbivory      β = −0.0042
C+E    open pollen, herbivore excluded     β = +0.094
HP+H   supplemented, natural herbivory    β = −0.160
HP+E   supplemented, herbivore excluded   β = −0.066
```

If the two environmental effects add to the background selection gradient,
the predicted natural combination is

```text
β_additive(C+H) = β(C+E) + β(HP+H) − β(HP+E)
                =  0.094 − 0.160 + 0.066
                =  0.000

β_observed(C+H) = −0.0042
factorial difference-in-differences = −0.0042
```

This is a **point-estimate decomposition**, not a statistical equivalence
test for exact additivity. Although the SE of a four-coefficient contrast
can be **upper bounded** by the sum of the four cell SEs, that bound is
too wide to establish either a nonzero factorial interaction or
equivalence to zero. The exact interaction SE and source ANCOVA p
remain unrecovered.

Under natural pollination with herbivory, the observed net gradient is
close to zero. Under herbivore exclusion, pollen delivery yields selection
for **later** flowering; relieving pollen limitation in that same
herbivore-excluded background reveals a gradient toward **earlier**
flowering. Therefore, "weak net selection" cannot be interpreted as
weak underlying selective pressures.

For spur length, the same additive reconstruction predicts `+0.202`
versus an observed `+0.180`, a double difference `−0.022`. There is
a **point** sign change between the two herbivore-excluded pollination
arms, but the negative estimate is unsupported in the source; it must not
be promoted to another bidirectionally supported reversal.

Across all five traits, the raw point differences-in-differences are:

```text
plant height      +0.011
number of flowers +0.060
corolla size      +0.043
spur length       −0.022
flowering start   −0.0042
```

Those magnitudes are on each trait's original standardized-selection
scale. None has a covariance-aware interaction CI and none proves
additive or nonadditive selection statistically.

## What this corrects in SCH

The previous H2 V11 *discovery-set* conjecture that robust directional
reversal might **require** simultaneous changes in multiple ecological
weights was too strong. The same factorial source contains a
**within-one-factor supported sign contrast**: one pollination
manipulation with herbivory status constant. This does not establish that
single-factor interventions are *usually* more effective; no independent
programme-level reversal-rate denominator supports that comparison.

Revised ecological statement:

> Opposing selective contributions can create a near-zero realized
> gradient, while changing a single ecological input can reveal a
> positive or negative net gradient, **without any demonstrated
> change in pollinator/herbivore preference or nonadditive effect.**

This is stronger than simply noting a statistical sign reversal because
the single intervention responsible for the matched comparison is
identified by experimental design. The mechanism of the background
negative selection is **not** established as a pure herbivore or
resource-allocation function: `HP+E` combines supplemented pollination
and exclusion and is not a hypothetical no-interaction/zero-cost state.

The specific conditional reversal is a reanalysis of an *already
published* source, **not** a novel empirical discovery of a new biological
system. Its value is to **falsify an overly narrow SCH prediction** and
align the emerging theory with real experimental ecology.

## Prospective programme boundary

Do not relabel the historical H2M1 V26 outcome-blind programme classes
based on this post hoc source reinterpretation; all existing held-out
success/failure denominators remain intact. The V11 source programme
continues to be classified as a **2×2 factorial experiment**. The new
conditional comparison is an **edge inside that programme**, not an
additional independent study, trait axis or replication.

This distinction also applies to *Pedicularis rex*: the 2015 site-specific
water-treatment effects do not by themselves demonstrate exsertion
selection reversal, and the 2016 observational correlations cannot
identify exsertion-specific causal functional optima. The positive
`Gymnadenia` counterexample helps constrain what SCH should seek,
without substituting for the blocked focal `P. rex` experiment.

## Reproduction

```sh
python scripts/audit_sch_gymnadenia_factorial_reversal.py \
  --output data/SCH_GYMNADENIA_SINGLE_FACTOR_REVERSAL_V1.json
python -m pytest -q tests/test_sch_gymnadenia_factorial_reversal.py
```

The audit reads the frozen original 20 treatment cells and checks all
five trait axes, four one-factor comparisons per axis, same-treatment
sample sizes, point additive residuals, and original cell-support
codes. It explicitly never turns selected cell p-values into a
covariance-aware test of between-treatment effects.
