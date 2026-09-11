# SCH Pedicularis causal-compromise experiment v1

## Decision

`Pedicularis rex` remains a top-tier direct Chapter-1 execution candidate because the programme now contains four distinct ingredients:

```text
1  shared conflict on exsertion in P. rex
2  causal evidence that cupulate-bract water defence reduces seed-predator damage
3  non-destructive corolla-tube manipulation precedent in congeners
4  a corrected independent seed-predator intervention pathway for the SCH antagonist lane.
```

Key sources:

- Sun, Armbruster & Huang 2016, DOI `10.1093/aob/mcw097`
- Sun & Huang 2015, DOI `10.1093/aobpla/plv019`
- Huang, Wang & Sun 2016, DOI `10.1111/jipb.12460`

The studies remain separate evidence modules. No cross-study data merging is allowed.

> **Current execution rule.** For the same-species SCH -> BITA chain, water retained/drained is **not** the registered SCH antagonist `G`. Water defence is reserved as the later BITA `y` axis. The registered SCH V2 surface therefore holds water-y fixed and manipulates seed-predator exposure independently. See `SCH_PEDICULARIS_WATER_G_DEPRECATION_V1.md` and `SCH_PEDICULARIS_FULL_SURFACE_CONTRACT_V2.md`.

## Focal Chapter-1 coordinate

Primary coordinate:

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

Expected state geometry:

```text
pollination-facing optimum shifted toward greater exsertion
seed-protection-facing optimum shifted toward lower exsertion.
```

This remains an expectation until causal multi-level manipulation is completed.

## Stage P0 — non-destructive z-manipulation pilot

A congeneric Pedicularis field experiment shortened corolla tubes by bending the tube and fixing it with clear sticky tape rather than cutting tissue. This establishes a manipulation precedent, not validation in `P. rex`.

For `P. rex`, use the registered Stage-P0 contract:

```text
docs/SCH_PEDICULARIS_STAGE_P0_DATA_CONTRACT_V1.md
scripts/evaluate_pedicularis_stage_p0.py
```

Candidate manipulation family:

```text
natural / sham-tape control
mild shortening
intermediate shortening
strong shortening
additional graded level(s) as needed to recover >=5 informative realized z levels.
```

The final levels are defined by realized exsertion, not nominal treatment labels.

A valid z manipulation must move exsertion while keeping preregistered off-target coordinates inside tolerance, including:

```text
corolla opening
lower-lip angle / position
corolla tube diameter
flower orientation
cupulate-bract height
water depth / retention
mechanical damage.
```

Pollinator visits and pollen grains are measured as functional checks but are not equivalence targets because z is intended to alter the pollination-facing function.

## Stage P1 — pollination-weight manipulation

The registered preferred contrast is:

```text
P1 = open natural pollination
P0 = open + standardized saturating supplemental cross-pollen.
```

Do not default to pollinator exclusion: pollinators and seed predators overlap in the open-flower period, so bagging/caging can contaminate the antagonist lane.

Use:

```text
docs/SCH_PEDICULARIS_POLLINATION_WEIGHT_AND_4_STATE_MAPPING_V1.md
scripts/evaluate_pedicularis_pollination_weight.py
```

A positive receipt must show both effectiveness and selectivity:

```text
supplementation increases pollen receipt
supplementation changes the preregistered pollen-limitation endpoint
while early predator attack, realized z, bract geometry, water state,
and mechanical damage remain within tolerance.
```

If the natural population is already pollen-saturated, the P treatment is uninformative in that context and the full surface remains locked.

## Stage G — independent antagonist-weight manipulation

The 2015 bract-water experiment remains important causal evidence that water defence reduces seed-predator damage. It is now treated as a **BITA functional-y / preferential-loading precedent**, not as the definitive SCH `G` intervention.

For the same-species causal chain, SCH requires:

```text
G0 = seed predator independently excluded
G1 = seed predator exposed
water-y = held fixed.
```

The preferred first method-development route is a timed post-pollination lower-flower / fruit sleeve that leaves the pollinator-entry zone uncovered and is applied before the registered late cutoff / ovary-swelling stage.

Use:

```text
docs/SCH_PEDICULARIS_STAGE_G_FIELD_PILOT_V1.md
scripts/evaluate_pedicularis_predator_method_v3.py
```

The required receipt is:

```text
receipt_schema_version = SCH_PEDICULARIS_PREDATOR_METHOD_V3
status = PEDICULARIS_PREDATOR_METHOD_VALIDATED.
```

A positive Stage-G method must reduce early attack and later predation, improve final intact seed set, and preserve:

```text
initial seed set
pollen receipt
pollinator visitation
realized exsertion
water state
handling integrity.
```

If no independent predator method passes, Pedicularis is demoted as the first same-species causal chain. Do **not** rescue the design by returning to water retained/drained as SCH `G`.

## Readiness assembly

The corrected full surface is unlocked only when one population and season produce all three positive receipts:

```text
SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1
+ SCH_PEDICULARIS_POLLINATION_WEIGHT_V1
+ SCH_PEDICULARIS_PREDATOR_METHOD_V3
-> SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3.
```

Use:

```text
scripts/assemble_pedicularis_full_surface_readiness.py
```

The three receipts must share `population_id` and `season_id`.

## Stage P2 — corrected V2 causal compromise surface

Run only the registered V2 mapping:

```text
>=5 realized z levels
x P0/P1 pollination-weight state
x G0/G1 independent predator state

water-y held fixed across all cells.
```

Four-state mapping:

```text
W00 = supplemented + predator excluded
W10 = natural      + predator excluded
W01 = supplemented + predator exposed
W11 = natural      + predator exposed.
```

Primary common reproductive outcome:

```text
undamaged mature viable seeds per focal flower / capsule.
```

Secondary outcomes include:

```text
pollen receipt
initial seed set
early seed-predator attack
seed-predation fraction
pollinator visitation / handling
water depth
mechanical damage.
```

Run:

```text
scripts/analyze_pedicularis_full_surface_v2.py
```

The returned core SCH estimands are:

```text
z_P* = state-specific pollination-facing reproductive optimum
z_G* = state-specific antagonist-facing reproductive optimum
z_C* = combined reproductive optimum
state-optimum separation
opposing optimum shifts
functional-component gradients.
```

Do not call `z_P*` or `z_G*` pure-function optima by default.

## Stage P3 — optional pure-function promotion

If the V2 surface is positive and sufficiently selective, form component contrasts:

```text
M_G0(z) = W10(z) - W00(z)
M_G1(z) = W11(z) - W01(z)

H_P0(z) = W01(z) - W00(z)
H_P1(z) = W11(z) - W10(z).
```

Only if component optima are context-stable may the receipt be promoted to:

```text
identified_pure_function_optima.z_F1
identified_pure_function_optima.z_F2
status = CONTEXT_STABLE_COMPONENT_OPTIMA_IDENTIFIED.
```

Use `scripts/identify_sch_pure_function_optima.py`.

## Stage P4 — fitness-scale conflict budget

After the component-optimum gate, estimate the focal-component conflict budget on the common reproductive scale:

```text
F1_bar(z) = 0.5 * [(W10-W00) + (W11-W01)]
F2_bar(z) = 0.5 * [(W01-W00) + (W11-W10)]

L_S,component*
= max F1_bar
+ max F2_bar
- max(F1_bar + F2_bar).
```

Use:

```text
scripts/estimate_sch_conflict_budget.py
```

A valid receipt exports `L_S_component`, its 95% interval, and `fitness_scale_id`. SLK G2 is bounded-positive only when the lower 95% bound is above zero.

## Geographic replication

Pedicularis has a natural antagonist-weight gradient; the 2016 study reports seed predation from approximately:

```text
0.80% to 27.42%
```

across populations.

After the first causal population closes, replicate a reduced surface in at least one lower- and one higher-predation context.

Prediction:

```text
weaker antagonist weight
-> z_C* shifts toward z_P*
-> conflict load / compromise magnitude decreases.
```

This turns the geographic mosaic into a direct test rather than background variation.

## Stop rules

### Stop P0 — z manipulation invalid

If bending/tape changes orientation, corolla opening, water protection, or damage beyond tolerance, do not use it as z.

### Stop P1 — pollination intervention ineffective or contaminated

If supplementation does not change the pollen-limitation endpoint, or changes early predator attack / water state beyond tolerance, redesign or change context before the factorial.

### Stop G — independent predator method invalid

If the exclusion method alters pollination, realized z, water state, or handling damage beyond tolerance, reject it. If no independent method passes, demote Pedicularis and move primary causal execution to Dalechampia / the next qualified system.

### Stop surface — no opposing geometry

If z effects on the two functional components align rather than oppose, report multifunctionality without causal shared-coordinate conflict.

### Stop component upgrade — context instability

If component optima shift materially across the other ecological state, retain a valid state-specific conflict result but do not export theory-level pure-function optima or the registered component conflict budget.

## Current execution status

```text
shared conflict reality in P. rex:                      RECOVERED
water-defence causal function / BITA-y precedent:       RECOVERED
congeneric non-destructive z-manipulation precedent:    RECOVERED
P. rex multi-level z validation:                        NOT YET EXECUTED
P. rex pollination-weight validation:                   NOT YET EXECUTED
independent predator-method V3 validation:               NOT YET EXECUTED
corrected V2 full causal z x P x G surface:             NOT YET EXECUTED
biological fitness-scale L receipt:                     NOT YET EXECUTED.
```

## Bottom line

Pedicularis remains the highest-leverage same-system route because a successful V2 programme can connect SCH conflict identification to BALANCE/BITA without changing species. Its decisive uncertainty is now explicit: **can an independent seed-predator intervention be qualified while water defence remains fixed?** The published water experiment supports the biological plausibility of the downstream y axis but no longer substitutes for that gate.
