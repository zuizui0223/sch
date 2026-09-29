# SCH Pedicularis Stage-G field pilot v1

## Goal

Identify one **independent seed-predator intervention** for `Pedicularis rex` that reduces pre-dispersal seed-predator attack while preserving the pollination lane and keeping the Chapter-2 water-defence axis fixed.

This is a method-development experiment. It is not yet the SCH causal compromise experiment.

## Natural-history constraints

Primary-source natural history places seed-predator oviposition:

```text
after flowers open
before ovaries swell
from outside the flower
through sepals or corolla tube.
```

`P. rex` reproduction depends strongly on bumblebee pollination, so any method that blocks the pollinator-entry zone during the relevant open-flower period is invalid for SCH.

A within-genus timing precedent now strengthens the sequence assumption. In
`P. furbishiae`, immature scapes were enclosed by mesh and the cages were
removed before flowers opened; later lepidopteran seed predation was unchanged,
which the authors interpreted as attack occurring after pollination. This
supports a Pedicularis post-pollination attack window, but does **not** show
that leaving a barrier in place after pollination is effective or selective.

## Candidate methods

### Method A — post-pollination lower-flower / fruit sleeve

First choice.

```text
natural pollination window
-> confirm pollen receipt on matched flowers
-> apply a small porous sleeve around the lower corolla / ovary region
-> leave upper corolla, stigma and pollinator-entry geometry exposed
-> maintain normal cupulate-bract water state.
```

Candidate materials:

```text
fine inert mesh
soft porous / dialysis-like tubing
custom lower-flower sleeve.
```

The exact material is not preregistered as successful. It must be selected by this pilot.

### Method B — local lower-corolla ovipositor barrier

Second choice if Method A cannot be applied early enough before oviposition.

Cover only the known lower attack region while preserving the visitor entrance and stigma/anther interaction zone.

This is biologically motivated but has no direct `P. rex` validation.

## Experimental unit

Use paired flowers within the same plant whenever feasible.

For each plant assign at least:

```text
EXPOSED + sham handling
EXCLUDED + Method A
```

If material is sufficient, add:

```text
EXCLUDED + Method B
```

Method comparison is exploratory. The confirmatory Stage-G V4 receipt must use a single prospectively chosen method.

## Timing records

For every focal flower record:

```text
anthesis time
first observed legitimate pollinator visit when available
barrier application time
whether the preregistered natural-pollination window was completed
whether ovary swelling had begun at barrier application
whether the barrier covered the pollinator-entry zone
whether attack / puncture / oviposition evidence was already present before barrier placement
whether the barrier later showed an integrity/access failure
barrier removal time if removed
exclusion_method identifier.
```

Do not infer an hour-scale window from the congeneric timing precedent. It supports the ordering of events only. Estimate the earliest post-pollination application time and latest effective pre-swelling application time in focal P. rex, then freeze those bounds before confirmatory Stage G.

## Barrier timing and integrity checks

The recovered external barrier literature adds two hard method-validity checks
that are not biological effect-size thresholds:

```text
pre_barrier_attack_present = 0
barrier_integrity_failure_present = 0
```

for every EXCLUDED focal flower entering a positive method receipt.

Why:

- a barrier applied after attack has already begun cannot identify the full
  predator-exclusion contrast;
- a sleeve with a pore / seal / placement failure may look like a biological
  non-response even when the material class itself could work.

Record these observations independently of the later
`early_predator_attack_present` endpoint. The former describes the state at
treatment start / barrier integrity; the latter is a post-treatment antagonist
outcome.

## Pollination checks

Record:

```text
legitimate pollinator visits
stigmatic pollen receipt / pollen grains on a matched or sacrificial flower
initial seed set
```

The barrier method fails if it materially changes the pollination lane beyond the prospectively frozen tolerance.

## Antagonist checks

Record:

```text
early external attack / oviposition evidence when visible
later seed-predation fraction
final intact seed set.
```

The method must lower attack/predation and improve final intact seed set by the registered minimum.

## Water-y checks

Because water defence is reserved for BITA Chapter 2, SCH Stage G must keep it fixed.

Record:

```text
water depth / water presence
bract integrity
realized exsertion
mechanical damage.
```

If exclusion changes water retention, that method is rejected even if predation falls.

## Prospective threshold freeze

Method-development information may be used to choose the final method and
support threshold rationale, but the confirmatory G decision rules must be
frozen before the confirmatory outcome data are read. Use
`SCH_PEDICULARIS_THRESHOLD_FREEZE_CONTRACT_V1.md`, including one basis note
for every timing, sample-size, effectiveness, and selectivity gate.

## Machine evaluation

Use:

```text
empirical/architecture/PEDICULARIS_PREDATOR_METHOD_TEMPLATE_V4.csv
empirical/architecture/PEDICULARIS_PREDATOR_METHOD_CONFIG_V4.json
scripts/evaluate_pedicularis_predator_method.py
```

The output must be:

```text
receipt_schema_version = SCH_PEDICULARIS_PREDATOR_METHOD_V4
status = PEDICULARIS_PREDATOR_METHOD_VALIDATED.
```

Only this method-qualified V3 receipt can enter:

```text
SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3.
```

## Fail-closed gates

A method is not promoted if any of the following fails:

```text
single method identity
minimum paired plants
minimum flowers per treatment
barrier applied after the registered pollination window
barrier applied before the registered late cutoff
pollination window complete
ovary not yet swollen
pollinator-entry zone not covered
no attack already present before EXCLUDED barrier application
barrier integrity maintained / no visible access failure
EXPOSED control receives matched sham handling
predator attack reduced
seed predation reduced
final seed set improved
initial seed set stable
pollen receipt stable
pollinator visitation stable
realized z stable
water state stable
handling damage stable.
```

## Decision rule

```text
one method passes V3
-> freeze method + timing + tolerances
-> run same-context P0 / P1 / G3 readiness
-> only then unlock the full z x P x G surface.

no method passes V3
-> the failure is specifically barrier effectiveness/selectivity or focal timing qualification, not generic post-pollination timing plausibility
-> Pedicularis is demoted as first-choice causal SCH system
-> move to Dalechampia / Castilleja rather than reusing water as G.
```

## Claim ceiling

A positive Stage-G result establishes only:

```text
a method-qualified independent antagonist intervention.
```

It does not establish compromise, dimensional release, structural modularity, or historical differentiation.
