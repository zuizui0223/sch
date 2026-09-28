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
P1 supplemental hand pollination         >=2 CONGENERIC PRECEDENTS
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
