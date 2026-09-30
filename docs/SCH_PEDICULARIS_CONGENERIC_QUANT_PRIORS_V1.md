# SCH Pedicularis congeneric quantitative priors v1

## Purpose

Pedicularis rex still lacks the registered focal P0/P1 calibration effects.
However, congeneric Pedicularis experiments provide real quantitative bounds
on method contamination, pollen-limitation effect heterogeneity, and field
sample feasibility.

These data are deliberately separated from the P. rex published-prior ledger.

Machine ledger:

```text
empirical/architecture/PEDICULARIS_CONGENERIC_QUANTITATIVE_PRIORS_V1.csv
```

Audit:

```bash
python scripts/audit_pedicularis_congeneric_quantitative_priors.py
```

Current bounded state:

```text
27 quantitative prior rows
6 Pedicularis species
P0 rows   5
P1 rows  22
direct P. rex effect rows  0
direct F0 values           0.
```

## P0 — non-destructive manipulation contamination

Huang, Wang & Sun 2016 provide unusually useful quantitative handling data for
P. tricolor.

```text
12 flowering individuals
72 shortened flowers
72 unmanipulated flowers

bumblebee visits / census
shortened      2.70 +/- 0.34 SE
control        2.61 +/- 0.37 SE
F1,64=0.033, P=0.857

seed set
shortened      0.45 +/- 0.022 SE
control        0.48 +/- 0.018 SE
F1,180=1.264, P=0.262.
```

The physical manipulation was corolla shortening by bending/fixation rather
than tissue cutting.

This supports a low-contamination manipulation family. It does not establish
that P. rex can realize five ordered exsertion levels without changing bract
water, opening geometry, orientation or damage.

## P1 — effect range is intrinsically broad

### Near-zero response precedent

In P. monbeigiana (Sun et al. 2005):

```text
open control                 n=20
bagged                       n=12
hand geitonogamy             n=12
supplemental outcross        n=12.
```

Open seed set was 41.7% in the Site-1 report and hand geitonogamy averaged
22.3%. Supplemental outcross seed set was not statistically different from
the open control.

This is a direct precedent for a valid P1 method yielding essentially no
pollen-limitation signal.

### Large and context-dependent response precedent

In P. monbeigiana (Liao et al. 2011), supplementation was performed at the
whole-plant level every two days through anthesis.

```text
10 supplemented plants / experimental plot
10 natural controls / experimental plot

fruit-set treatment effect   F1,304=107.12, P<=0.001
seed-set treatment effect    F1,304=113.27, P<=0.001.
```

Reported seed-set responses relative to control were:

```text
pure sparse    2.1 x
pure dense     1.1 x
mixed sparse   +36%
mixed dense    +35%.
```

The plot-type x treatment interaction for seed set was F=18.13, P<=0.001.

Thus the same genus contains both near-zero and large supplementation effects.
A single congeneric expected effect is not biologically defensible.

## P1 — hand-pollination response and whole-plant context

### P. dunniana — quantitative hand-pollination response

Sun et al. (2005) report:

```text
natural pollination       seed set 54.2%
hand self-pollination     seed set 63.1%
hand cross-pollination    seed set 67.2%

ANOVA F = 115.08, df = 2,15, P < 0.001.
```

This demonstrates that hand pollen addition can increase seed set within
`Pedicularis`. It is kept separate from the open-flower supplementation family:
`P. dunniana` is strongly autogamous and the contrast is a breeding-system /
pollen-limitation assay rather than the exact registered P. rex P1 intervention.

### P. palustris — whole-plant pollinator dependence can coexist with scale-dependent limitation

Karrenberg & Jensen (2000) compared pollinator exclosure, hand pollination and
natural pollination at the whole-plant level in one large and one small
population.

Published quantitative context includes:

```text
pollinator exclosure seed set   <15% of natural seed set
self-compatibility               61% and 97% of within-population cross seed set
maximum simultaneously open flowers
  small population               31%
  large population               13%.
```

Natural pollination was sufficient for maximum **seed production per plant**,
yet seed set **per capsule** was pollen-limited in the smaller population.

That distinction matters for P1 design: whole-plant reproductive output and
capsule-level pollen limitation can disagree even in the same system. The
registered P. rex endpoint and experimental unit must therefore be frozen
before effect targets are chosen.

## P1 — pollination context also varies strongly

P. densispica provides an additional context precedent.

Bombus richardsi accounted for:

```text
mixed patches   162 / 346 recorded visits
pure patches    109 / 310 recorded visits
chi-square=9.17, P=0.002.
```

Self/outcross pollen-limitation contrasts differed strongly among pure/mixed
patch contexts in all three regions (reported regional F tests 72.78, 27.82
and 35.83; all P<0.001).

This reinforces the rule that a P. rex P1 effect target should be treated as
context-specific until measured.

## P1 — experimental-unit choice

At least two experimentally demonstrated supplementation units now exist:

```text
within-plant paired flowers
whole-plant supplementation.
```

Within-plant pairing controls plant-level heterogeneity but can permit
resource reallocation among treated and untreated flowers.

Whole-plant supplementation reduces that particular bias but requires more
pollen and loses within-plant treatment pairing.

The two designs estimate different intervention structures and must not be
pooled as if they were interchangeable replicates.

## CAL-B use

Congeneric effect sizes may be used for:

- external effect-plausibility scenarios;
- stop-rule stress tests;
- deciding how wide the P1 pilot search should be;
- checking that the prospectively selected minimum effect is not absurd
  relative to the genus-level empirical range.

They may not be inserted automatically as the P. rex CAL-B target.

## CAL-C use

Congeneric sample sizes and uncertainty can inform sensitivity analyses for:

- achievable plant counts;
- flowers per plant;
- whether a whole-plant vs paired-flower design is feasible;
- alternate assumed-effect scenarios.

They are not same-context pilot variance.

## Claim ceiling

Congeneric quantitative priors reduce design invention and expose plausible
effect heterogeneity.

They do not provide a P. rex supplementation effect, do not validate P0/P1,
and do not directly freeze any F0 value.
