# SCH Pedicularis experimental method precedents v1

## Purpose

The absence of project-owned P. rex calibration data does not mean the P0/P1
manipulation methods need to be invented from scratch.

This ledger records experimentally demonstrated Pedicularis methods while
keeping method feasibility separate from focal-species effect estimation.

Machine ledger:

```text
empirical/architecture/PEDICULARIS_METHOD_PRECEDENTS_V1.csv
```

Audit:

```bash
python scripts/audit_pedicularis_method_precedents.py
```

## P0 floral-dimension manipulation

Huang, Wang & Sun 2016 manipulated corolla tube length in field Pedicularis.

For P. tricolor, the tube was shortened by bending it and fixing it with clear
sticky tape rather than cutting tissue.

Published quantitative results include:

```text
12 flowering individuals
72 shortened flowers
72 unmanipulated flowers

bumblebee visits / census
shortened       2.70 +/- 0.34 SE
unmanipulated   2.61 +/- 0.37 SE
F1,64=0.033, P=0.857

seed set / capsule
shortened       0.45 +/- 0.022 SE
unmanipulated   0.48 +/- 0.018 SE
F1,180=1.264, P=0.262.
```

This is a strong congeneric precedent for a reversible/non-destructive floral
dimension manipulation plus a visitor-response contamination check.

It is not validation that the registered P. rex exsertion manipulation can
produce five ordered realized-z levels without off-target effects.

## P1 pollen-supplementation precedents

### Yang, Sun & Guo 2005

Two Pedicularis species, P. siphonantha and P. longiflora, were subjected to:

```text
open pollination
open + supplemental self pollen
open + supplemental outcross pollen
bagged hand self-pollination
bagged hand outcross-pollination.
```

The open-pollination supplementation experiment did not increase seed
production, while hand self/outcross treatments differed in seed production.

This demonstrates that supplemental-pollen and bagged hand-pollination
treatments are established field methods in the genus.

### Dai et al. 2017 — two distinct studies

Keep two same-year papers separate.

The Journal of Systematics and Evolution paper (doi
`10.1111/jse.12240`) studied four large P. siphonantha populations spanning
3200-4300 m. Outcross supplementation significantly increased seed production
per capsule in high-altitude populations but not lower-altitude populations.
This is the **effect-heterogeneity precedent**.

The Journal of Mountain Science paper (doi
`10.1007/s11629-017-4481-1`) provides the detailed **protocol precedent**:
three natural plus two transplanted populations; 20 randomly selected
individuals per population; three marked flowers per individual assigned to
supplemental self pollen, supplemental outcross pollen, or open pollination.
It defines

```text
PL_S = (F_IS - F_IN) / F_IN
PL_X = (F_IX - F_IN) / F_IN
```

using seed production per capsule and harvests treated flowers at fruit
maturity.

Together these demonstrate:

```text
paired/within-plant supplementation is feasible in Pedicularis
the supplementation effect itself can be strongly context-dependent.
```

The protocol may transfer, but neither published effect may be treated as a
P. rex effect.

### Sun et al. 2005 — P. monbeigiana

A separate congeneric experiment included:

```text
open control                     n=20
bagged flowers                   n=12
bagged hand-geitonogamy          n=12
supplemental outcross pollen     n=12.
```

Supplemental outcross seed set was not statistically different from open
control, whereas hand geitonogamy reduced seed production. In three open field
sites, fruit set was 94.7±3.2%, 96.2±3.0% and 94.2±4.3%, and seed set was
41.7±9.3%, 38.2±8.4% and 37.6±9.0% (N>20 per site; the indexed full text does
not make the SD/SE label of the ± values sufficiently clear for reuse as a
variance estimate).

This is a useful precedent for a **true near-zero supplementation response**:
supplementation can be methodologically valid yet biologically uninformative
when natural pollen delivery is already sufficient.

### Liao et al. 2011 — whole-plant supplementation

P. monbeigiana was supplemented at the **whole-plant** level rather than by
supplementing one focal flower only.

Within each experimental plot:

```text
10 plants  supplemental outcross pollen
10 plants  natural-pollination controls
```

Supplemental pollen was applied to all flowers every two days through anthesis.
Pollen was pooled from 20 flowers on five non-focal donors about 100 m away.

The design explicitly reduced the risk that a supplemented flower would draw
resources away from untreated flowers on the same plant.

Published quantitative results included:

```text
fruit-set treatment effect   F1,304 = 107.12, P <= 0.001
seed-set treatment effect    F1,304 = 113.27, P <= 0.001

seed set relative to control
pure sparse plot             2.1 x
pure dense plot              1.1 x
mixed sparse plot            +36%
mixed dense plot             +35%

plot-type x treatment
seed set                     F = 18.13, P <= 0.001.
```

This is both an effect-scale precedent and a warning: the supplementation
effect can vary strongly with ecological context.

### Two legitimate P1 experimental units now exist

The literature therefore supports at least two distinct P1 designs:

```text
A. within-plant paired flowers
   + controls individual heterogeneity strongly
   - can permit within-plant resource reallocation among treated/control flowers

B. whole-plant supplementation
   + minimizes within-plant resource-reallocation bias
   - sacrifices within-plant treatment pairing and requires more donor pollen.
```

These are alternative experimental estimands, not interchangeable
implementations. The P. rex calibration basis document should state which
experimental unit is selected and why.

## Handling and exclusion precedent

Huang & Shi 2013 manipulated eight nectarless Pedicularis species.

On each of 10 plants per species, three flowers were assigned to:

```text
gap blocked + open pollination
tip blocked + open pollination
tip blocked + pollinator exclusion with a small nylon net.
```

A pilot tested glue brands and reported no bumblebee discrimination against
the manipulated flowers.

This is a strong handling-control and exclusion-method precedent, but it is
neither P1 supplementation nor independent seed-predator G.

## Same-species antagonist-related precedent

Sun & Huang 2015 manipulated bract water in P. rex and jointly measured visitor
rates and seed outcomes.

This remains useful evidence that an intervention can be audited for
pollinator contamination and antagonist-related reproductive effects in the
focal species.

However, water drainage is not the registered independent predator-exclusion G
and remains deprecated for the SCH-to-BITA reference surface.

## What is now resolved

Method-family uncertainty is substantially reduced:

```text
P0 non-destructive floral manipulation   CONGENERIC FIELD PRECEDENT
P1 supplemental hand pollination         >=5 CONGENERIC PRECEDENTS
flower handling / bagging controls       MULTI-SPECIES PEDICULARIS PRECEDENT
visitor contamination auditing           CONGENERIC + P. rex PRECEDENT.
```

## What remains focal empirical work

```text
P. rex multi-level realized-exsertion manipulation
P. rex same-flower repeatability
P. rex pollen-supplementation effect
P. rex independent seed-predator exclusion
P. rex independent-G timing qualification.
```

## Claim ceiling

These studies support method feasibility and design choice.

They do not provide direct P. rex effect estimates for the registered
interventions and do not freeze any F0 value.
