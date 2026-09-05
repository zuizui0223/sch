# SCH Pedicularis causal-compromise experiment v1

## Decision

`Pedicularis rex` is now a serious direct Chapter-1 execution candidate because three otherwise difficult pieces are available in the same genus/programme:

```text
1  shared conflict on exsertion in P. rex
2  selective antagonist-weight manipulation via bract water in P. rex
3  non-destructive corolla-tube manipulation precedent in congeners.
```

Key sources:

- Sun, Armbruster & Huang 2016, DOI `10.1093/aob/mcw097`
- Sun & Huang 2015, DOI `10.1093/aobpla/plv019`
- Huang, Wang & Sun 2016, DOI `10.1111/jipb.12460`

The three studies remain separate evidence modules. No cross-study data merging is allowed.

## Focal Chapter-1 coordinate

Primary candidate:

```text
z = realized corolla exsertion above the cupulate bract
  = (flower length - bract height) / flower length.
```

Observed biological geometry in `P. rex`:

```text
higher z -> more pollen arrival
higher z -> more seed predation
seed predation -> fewer final viable seeds.
```

Thus the expected state geometry is:

```text
pollination-facing optimum shifted toward greater exsertion
seed-protection-facing optimum shifted toward lower exsertion.
```

This remains an expectation until causal multi-level manipulation is completed.

## Stage P0 — non-destructive z-manipulation pilot

A congeneric Pedicularis field experiment shortened corolla tubes by **bending the tube and fixing it with clear sticky tape**, rather than cutting tissue. This establishes a manipulation precedent for changing exposed corolla length without tissue removal.

For `P. rex`, test an adapted version only as a pilot.

Candidate manipulation family:

```text
natural / sham-tape control
mild shortening
intermediate shortening
strong shortening
```

The final number and spacing of levels are set from realized exsertion, not from nominal treatment labels. Confirmatory SCH still targets >=5 informative realized z values if feasible.

Do not use permanent cutting as the default manipulation.

## Stage P0 manipulation checks

A z level is valid only if the manipulation changes exsertion while keeping other relevant coordinates inside preregistered tolerances.

Measure at least:

```text
realized exsertion
corolla opening
lower-lip angle / position
stigma position
corolla tube diameter
flower orientation
cupulate-bract height
water depth / retention
nectar accessibility where relevant
handling time of legitimate pollinators
mechanical damage / wilting.
```

Critical rule:

```text
z manipulation must not silently become a pollinator-handling or water-defence manipulation.
```

If transparent tape itself changes visitor behavior, run sham tape at every nominal z family or reject the method.

## Stage P1 — functional-weight manipulations

### Pollination-facing weight

The cleanest final implementation remains unresolved and should be pilot-tested rather than assumed.

Candidate approaches:

```text
natural pollination vs standardized pollen supplementation
or
controlled Bombus exposure vs matched no-exposure / standardized-pollen baseline.
```

The chosen P intervention must change pollinator-mediated reproductive limitation while avoiding simultaneous changes in antagonist exposure.

### Antagonist-facing weight

The 2015 experiment already supplies a strong validated intervention precedent:

```text
water retained in cupulate bract
vs
bract drained before anthesis.
```

Observed selectivity:

```text
pollinator visitation: treatment P = 0.958
initial seed set:       treatment P = 0.906
seed predation:         treatment P < 0.0001
final seed set:         treatment P < 0.0001.
```

Therefore this is the first-choice antagonist-weight intervention for Stage P1, subject to replication in the focal population / season.

## Stage P2 — causal compromise surface

Once z and both functional interventions pass selectivity checks, run a randomized multi-level surface.

Conceptual design:

```text
>=5 realized z levels
x pollination-weight state
x antagonist-weight state.
```

Use one common reproductive outcome across all cells.

Primary candidate endpoint:

```text
mature intact viable seeds per focal flower / capsule
```

with initial seed set and seed-predation fraction retained as mechanism-resolving secondary outcomes.

The registered SCH analyzer then estimates:

```text
z_P* = state-specific pollination-facing reproductive optimum
z_G* = state-specific antagonist-facing reproductive optimum
z_C* = combined reproductive optimum
state-optimum separation
opposing optimum shifts
functional-component gradients.
```

Do not call `z_P*` or `z_G*` pure function optima by default.

## Stage P3 — optional pure-function promotion

If the full crossed surface is sufficiently selective, form component contrasts:

```text
M_G0(z) = W10(z) - W00(z)
M_G1(z) = W11(z) - W01(z)

H_P0(z) = W01(z) - W00(z)
H_P1(z) = W11(z) - W10(z).
```

Only if the component optima are context-stable may the receipt be promoted to:

```text
identified_pure_function_optima.z_F1
identified_pure_function_optima.z_F2.
```

Use `scripts/identify_sch_pure_function_optima.py` for the registered upgrade gate.

## Geographic replication

Pedicularis has an unusually useful natural gradient in antagonist weight.

The 2016 study reports seed predation from:

```text
0.80% to 27.42%
```

across populations, while the pollinator-facing direction is comparatively consistent.

After the first causal population closes, replicate a reduced surface in at least one low-predation and one high-predation context.

Prediction:

```text
weaker antagonist weight
-> z_C* shifts toward z_P*
-> compromise magnitude decreases.
```

This would turn the geographic mosaic from background variation into a direct SCH test.

## Stop rules

### Stop P0 — manipulation invalid

If bending/tape changes orientation, corolla opening, handling mechanics or water protection beyond tolerance, do not use it as z.

### Stop P1 — pollination intervention not selective

If the P intervention changes seed-predator access or water state, redesign before the factorial.

### Stop P2 — water manipulation loses selectivity

If the intact/drained contrast changes pollinator visitation or initial seed set materially in the focal context, it cannot serve as a clean antagonist-weight intervention there.

### Stop P3 — no opposing geometry

If z effects on pollination and antagonist loss align rather than oppose, report multifunctionality without compromise.

## Current execution status

```text
shared conflict reality in P. rex:                 RECOVERED
selective antagonist-weight manipulation:          RECOVERED
congeneric non-destructive z-manipulation method:  RECOVERED
P. rex multi-level z validation:                   NOT YET EXECUTED
selective pollination-weight intervention:          NOT YET CLOSED
full causal z x P x G surface:                     NOT YET EXECUTED.
```

## Bottom line

Pedicularis has moved from an external validation system to a **top-tier causal SCH candidate**. Its key advantage over Dalechampia is that a selective antagonist-facing intervention is already experimentally demonstrated. Its remaining decisive gate is whether exsertion can be manipulated over several levels in `P. rex` without changing the other floral coordinates that make the system interpretable.
