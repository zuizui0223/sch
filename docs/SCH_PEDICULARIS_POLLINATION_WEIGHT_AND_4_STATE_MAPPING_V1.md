# SCH Pedicularis pollination-weight intervention and four-state mapping v1

## Decision

For `Pedicularis rex`, do **not** make pollinator exclusion the default P manipulation. Pollinators and seed predators both act after flowers open, so bagging / caging risks changing the antagonist lane at the same time.

The preferred P pilot is:

```text
P1 = open natural pollination
P0 = open + standardized saturating supplemental cross-pollen
```

Both treatments remain open to the same visitor and seed-predator environment.

The P manipulation therefore changes **dependence on pollinator-mediated pollen delivery**, not physical pollinator access.

> **Important V2 correction.** The earlier prototype in this document paired P with water retained/drained as SCH antagonist `G`. That mapping is deprecated for the same-species SCH -> BITA chain. The registered V2 surface uses an **independent seed-predator exposure/exclusion intervention as G while water defence is held fixed**. See `SCH_PEDICULARIS_WATER_G_DEPRECATION_V1.md` and `SCH_PEDICULARIS_FULL_SURFACE_CONTRACT_V2.md`.

## Biological basis

`P. rex` is self-compatible but has little or no automatic self-pollination and seed production depends strongly on bumblebee pollination. The focal flowers are therefore suitable for a pollen-limitation manipulation.

The seed-predator natural-history window overlaps open flowering: eggs are laid on ovaries after flowers open and before ovaries swell. This makes temporal pollinator exclusion a potentially contaminated default intervention.

## Pollination-weight states

### P1 — natural pollination weight active

```text
flower remains open
sham handling matches the supplemental treatment
no added pollen beyond the standardized sham procedure.
```

### P0 — pollination limitation suppressed

```text
flower remains open
standardized donor-mixed cross-pollen is applied to the receptive stigma
treatment is repeated prospectively if needed to reach the frozen saturation criterion.
```

The donor protocol should avoid repeated use of one pollen donor and should be blocked by plant / date.

## P-pilot effectiveness gate

The supplementation treatment is useful only if it changes the reproductive consequence of pollen delivery enough to alter the functional weight.

Primary pilot effect:

```text
initial seed set
= (undamaged + later-damaged initiated seeds) / ovules
```

or an equivalent predeclared pre-predation reproductive endpoint.

The supplementation lane should exceed a preregistered minimum improvement in initial seed set or other validated pollen-limitation endpoint.

If natural pollination is already saturating in the focal context, supplementation is biologically uninformative as a P-weight manipulation. That is a valid stop result, not evidence that pollination is unimportant.

## P-pilot selectivity gate

Supplemental pollination must not silently alter the antagonist or defence lanes.

Measure at least:

```text
realized exsertion
cupulate-bract water depth
bract height / relevant geometry
mechanical damage from handling
seed-predator attack / oviposition proxy before downstream seed consumption.
```

Critical point:

```text
later predation fraction is not the only selectivity check
```

because supplementation can change the number of initiated seeds and therefore the denominator / resource landscape for later larvae.

Prefer a proximate antagonist-access measure such as:

```text
oviposition scar / puncture
adult attack incidence
or another preregistered early attack indicator.
```

If the P treatment changes early antagonist attack beyond tolerance, it is not selective enough for the SCH crossed design.

## Corrected antagonist-weight states for the V2 chain

The registered same-species SCH -> BITA route uses an antagonist manipulation independent of the Chapter-2 water-defence axis:

```text
G0 = PREDATOR_EXCLUDED
     seed-predator exposure selectively suppressed by a method-qualified
     independent exclusion intervention

G1 = PREDATOR_EXPOSED
     matched exposed / sham condition.
```

Required method receipt:

```text
SCH_PEDICULARIS_PREDATOR_METHOD_V3
status = PEDICULARIS_PREDATOR_METHOD_VALIDATED.
```

During the SCH V2 surface:

```text
water_y = HELD_FIXED_ACROSS_ALL_SCH_CELLS.
```

The historical water retained/drained experiment remains important as causal evidence that water defence reduces antagonist damage, but it belongs to the BITA `y` lane / functional-y selectivity precedent, not the definitive SCH `G` lane.

## Corrected four-state mapping

With open-flower P manipulation and independent predator G, the registered V2 state surfaces are:

```text
W00(z)
= P0 supplemental pollen
+ G0 predator excluded

W10(z)
= P1 natural pollination
+ G0 predator excluded

W01(z)
= P0 supplemental pollen
+ G1 predator exposed

W11(z)
= P1 natural pollination
+ G1 predator exposed.
```

Water defence is held fixed in every cell.

The default empirical state optima retain the registered meaning:

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

They are **state-specific reproductive optima**, not automatically pure `z_F1*` or `z_F2*`.

## Why the corrected mapping matters

The two Chapter-1 interventions now alter distinct ecological weights while preserving the Chapter-2 axis for an independent downstream test:

```text
P manipulation
-> changes pollen-limitation weight while leaving flowers open

G manipulation
-> changes seed-predator exposure independently

water-y
-> held fixed in SCH
-> manipulated later in BITA.
```

This prevents the protected water state from helping define the Chapter-1 reference and then being asked in Chapter 2 to move the optimum toward that same reference.

## Sham controls

### P sham

Natural-pollination flowers receive the same handling duration and stigma-contact procedure without the standardized pollen addition.

### G sham

The exposed control receives handling matched to the selected exclusion device. The method-qualified G intervention must preserve pollinator-entry geometry, pollen receipt, water state, realized exsertion and handling integrity within prospectively frozen tolerances.

## Full experiment

Once z, P and independent G all pass their own validation gates:

```text
>=5 realized z levels
x P0/P1 pollination-weight state
x G0/G1 independent predator state

water-y held fixed.
```

Primary outcome:

```text
undamaged mature viable seeds per focal flower / capsule
```

or the prospectively frozen common reproductive scale used by the V2 contract.

Secondary mechanism outcomes include:

```text
pollen receipt
initial seed set
early seed-predator attack
seed-predation fraction
pollinator visitation / handling
water retention.
```

Run `SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2`, then the registered SCH state-surface analyzer, then the optional context-stable component-optimum upgrade.

## Stop rules

```text
P supplementation does not improve the pollen-limitation endpoint
-> P intervention ineffective in this context

P supplementation changes early predator attack
-> P intervention not selective

independent G changes pollination, realized z, or water state beyond tolerance
-> G intervention not selective

z manipulation changes water-defence state
-> z intervention invalid

only water retained/drained is available as G
-> same-species SCH -> BITA chain remains unqualified; do not revert to the deprecated mapping.
```

Any failed gate blocks the full factorial rather than being statistically adjusted away later.

## Machine implementation

Pollination-weight pilot:

```text
scripts/evaluate_pedicularis_pollination_weight.py
receipt = SCH_PEDICULARIS_POLLINATION_WEIGHT_V1.
```

Independent antagonist method:

```text
scripts/evaluate_pedicularis_predator_method_v3.py
receipt = SCH_PEDICULARIS_PREDATOR_METHOD_V3.
```

Readiness assembly:

```text
scripts/assemble_pedicularis_full_surface_readiness.py
receipt = SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3.
```

## Claim ceiling

Successful P and G validation establishes only that the two functional weights can be manipulated selectively enough for the main V2 experiment.

It does not itself establish compromise, conflict budget `L`, dimensional release, architecture value, or historical modularization.
