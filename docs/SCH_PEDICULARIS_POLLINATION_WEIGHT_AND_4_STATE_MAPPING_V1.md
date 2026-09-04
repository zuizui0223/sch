# SCH Pedicularis pollination-weight intervention and four-state mapping v1

## Decision

For `Pedicularis rex`, do **not** make pollinator exclusion the default P manipulation. Pollinators and seed predators both act after flowers open, so bagging / caging risks changing the antagonist lane at the same time.

The preferred first pilot is instead:

```text
P1 = open natural pollination
P0 = open + standardized saturating supplemental cross-pollen
```

Both treatments remain open to the same visitor and seed-predator environment.

The P manipulation therefore changes **dependence on pollinator-mediated pollen delivery**, not physical pollinator access.

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

If natural pollination is already saturating in the focal context, supplementation is biologically uninformative as a P-weight manipulation. That is a valid stop result.

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

## Antagonist-weight states

Use the existing water-defence manipulation as the starting G intervention.

```text
G0 = water-retention protection active / antagonist weight reduced
G1 = bract drained / antagonist weight increased.
```

The 2015 experiment showed that draining increased seed predation while pollinator visitation and initial seed set were not detectably changed in that study.

This selectivity must still be replicated / prospectively bounded in the focal SCH population and season.

## Four-state mapping

With the two weight interventions, the SCH state surfaces become:

```text
W00(z)
= P0 supplemental pollen
+ G0 water protection active
= both focal functional constraints strongly reduced

W10(z)
= P1 natural pollination
+ G0 water protection active
= pollination-facing state

W01(z)
= P0 supplemental pollen
+ G1 water defence disabled
= antagonist-facing state

W11(z)
= P1 natural pollination
+ G1 water defence disabled
= both functional demands active / combined state.
```

The default empirical state optima retain the registered meaning:

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

They are **state-specific reproductive optima**, not automatically pure `z_F1*` or `z_F2*`.

## Why this mapping is useful

The two manipulations attack different bottlenecks without requiring different physical visitor-exclusion regimes:

```text
P manipulation
-> changes pollen-limitation weight while leaving flowers open

G manipulation
-> changes water-based antagonist protection while leaving pollination access open.
```

This reduces cage / bag / access artefacts and makes the four reproductive surfaces much easier to compare on one common seed-fitness endpoint.

## Sham controls

### P sham

Natural-pollination flowers receive the same handling duration and stigma-contact procedure without the standardized pollen addition.

### G sham / handling control

The final confirmatory experiment should distinguish the intended water-state difference from cutting / puncture artefacts. A reversible drain/refill or matched sham-hole treatment is preferable if Stage G validation shows it can reproduce the original water effect without persistent tissue damage.

The historical 2015 hole-at-bract-base method is evidence that the function is manipulable, not automatically the final confirmatory implementation.

## Full experiment

Once z, P and G all pass their own validation gates:

```text
>=5 realized z levels
x P0/P1 pollination-weight state
x G0/G1 antagonist-weight state
```

Primary outcome:

```text
mature intact viable seeds / ovules or the frozen common reproductive scale.
```

Secondary mechanism outcomes:

```text
pollen receipt
initial seed set
early seed-predator attack
seed-predation fraction
pollinator visitation / handling
water retention.
```

Run the registered SCH state-surface analyzer, then the optional context-stable component-optimum upgrade.

## Stop rules

```text
P supplementation does not improve the pollen-limitation endpoint
-> P intervention ineffective in this context

P supplementation changes early predator attack
-> P intervention not selective

G manipulation changes pollination beyond tolerance
-> G intervention not selective

z manipulation changes water-defence state
-> z intervention invalid.
```

Any failed gate blocks the full factorial rather than being statistically adjusted away later.

## Claim ceiling

A successful P and G validation establishes only that the two functional weights can be manipulated selectively enough for the main experiment.

It does not itself establish compromise, dimensional release, or historical modularization.
