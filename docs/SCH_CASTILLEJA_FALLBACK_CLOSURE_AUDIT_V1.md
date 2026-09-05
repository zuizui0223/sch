# SCH Castilleja fallback closure audit v1

## Decision

`Castilleja linariaefolia` remains a strong **short-path biological fallback** for Chapter 1, but it is not yet an immediately executable causal-compromise system.

The primary source recovers the right natural-selection geometry:

```text
longer / showier calyx
-> pollination pathway benefit
-> greater predispersal seed-predator pathway cost
-> common female seed fitness.
```

However, the key calyx axis was observational, not experimentally manipulated, and a selective predator-removal intervention was not recovered from the focal study.

Current status:

```text
REAL_WORLD_OPPOSING_SELECTION: RECOVERED
COMMON_SEED_FITNESS: RECOVERED
DIRECT_MULTI_LEVEL_CALYX_MANIPULATION: NOT RECOVERED
SELECTIVE_SEED_PREDATOR_INTERVENTION: NOT RECOVERED
CAUSAL_COMPROMISE_GEOMETRY: NOT YET IDENTIFIED.
```

## Primary source

Cariveau et al. 2004, Oikos, DOI `10.1111/j.0030-1299.2004.12641.x`.

The study system is hummingbird-pollinated `C. linariaefolia` in the Rocky Mountains of Colorado. Predispersal seed predators include plume-moth and fly larvae.

The study first tested pollen limitation with supplemental pollination. Supplemental pollen only marginally increased female reproductive components, with the authors arguing that seed predation may mask part of the benefit.

The main trait-selection analysis then used natural variation in:

```text
calyx length
flower production
plant height
```

and decomposed their relationships with relative seed set through pollination and seed-predation pathways.

The central positive result for SCH is that calyx length experienced opposing selection through the two pathways.

## Why this is a strong fallback

Compared with the `Nicotiana` oviposition lane, the antagonist-to-fitness path is short:

```text
predispersal larval attack
-> seed destruction
-> relative seed set.
```

The pollinator and antagonist guilds are also biologically distinct:

```text
pollinator = hummingbirds
antagonists = plume-moth / fly seed predators.
```

This avoids the same-individual dual-role complication of `Manduca sexta` in `Nicotiana`.

## What the 2004 source does not identify

### C0.1 — no randomized calyx coordinate

The focal selection analysis measured natural calyx length. It did not randomly assign plants or flowers to multiple calyx-length states.

Therefore:

```text
opposing selection on observed calyx length
!= causal response surface under do(calyx length).
```

A Chapter-1 compromise experiment still needs an intervention on the same declared `z` coordinate.

### C0.2 — supplemental pollination is not a pollinator-choice manipulation

Pollen supplementation tests pollen limitation / seed response to additional pollen. It does not show how hummingbirds change their behavior across experimentally assigned calyx values.

A causal calyx experiment must separately measure:

```text
calyx manipulation
-> hummingbird visitation / contact / pollen transfer.
```

### C0.3 — selective predator manipulation not recovered

The focal study quantified natural pre-dispersal predation and its path to seed fitness. A validated intervention that removes plume-moth / fly seed predators while leaving hummingbird pollination and calyx state unchanged was not recovered.

Thus the most important fallback gate is still:

```text
G0/G1 selectivity.
```

### C0.4 — mixed antagonist guild

Plume-moth and fly larvae are not automatically one mechanistic antagonist. If both are common, the causal experiment must either:

1. manipulate a declared combined `predispersal seed-predator` state and show that the intervention acts consistently on both; or
2. identify and manipulate one focal antagonist taxon/channel.

Do not pool taxa solely because both damage seeds.

## Stage-0 manipulation development

### Trait lane

The first manipulation problem is to create a reversible or low-damage calyx/display perturbation that changes the visual/structural coordinate without changing nectar, corolla tube, floral access, or ovary development.

Candidate routes to pilot:

```text
reversible visual extension / masking of the exposed calyx display
mechanically supported but tissue-preserving apparent-length manipulation
bounded lower-side perturbation if biologically credible upward extension fails.
```

A permanent tissue cut should not be assumed neutral. Direct floral damage can itself alter visitation, fruit set, or predator access.

Promotion requires manipulation checks for:

```text
measured apparent z
corolla access
nectar / floral reward
flower posture
hummingbird contact geometry
fruit / capsule development under standardized hand pollination and predator suppression.
```

### Pollinator lane

Measure the same manipulated calyx values against:

```text
hummingbird approach / visit probability
legitimate floral contact
pollen deposition
later seed set under predator-suppressed conditions.
```

### Predator lane

Recover antagonist natural history before declaring an exclusion treatment:

```text
adult oviposition timing / target tissue
larval entry timing
whether damage can be blocked after pollination
which predator taxa dominate the focal population.
```

Potential G interventions must be piloted with sham controls and tested for effects on hummingbird access and floral condition.

## Promotion rule

Castilleja becomes the preferred causal fallback only if all are recovered:

```text
C1 >=3 manipulable values on one calyx/display z
C2 manipulated z changes pollinator-mediated reproduction
C3 manipulated z changes predator exposure / loss in the opposing direction
C4 selective predator intervention exists
C5 one common mature-seed outcome remains interpretable.
```

Until then its role is:

```text
HIGH_VALUE_REAL_WORLD_OPPOSING_SELECTION_ANCHOR
+
SHORT_PATH_FALLBACK_REQUIRING_MANIPULATION_DEVELOPMENT.
```

## Comparison with Dalechampia

```text
Dalechampia
+ experimental display manipulability exists at genus-program level
+ strong positive conflict case exists
- conflict is geographically/contextually variable
- selective adult-weevil G intervention must be developed

Castilleja linariaefolia
+ distinct pollinator and seed-predator guilds
+ short predator -> seed-fitness path
+ opposing calyx selection already recovered
- focal calyx axis is observational
- selective predator intervention not recovered.
```

Therefore a failed Dalechampia population screen does not automatically make Castilleja ready for the confirmatory experiment. It moves Castilleja to the front of the **manipulation-development queue**.

## Claim ceiling

The positive statement currently allowed is:

> A natural `C. linariaefolia` system shows opposing pollination- and seed-predation-mediated selection on calyx length on a common seed-fitness scale, making it a strong short-path reality anchor and fallback candidate. It does not yet provide randomized multi-level calyx manipulation or selective antagonist intervention sufficient to identify the Chapter-1 causal compromise surface.
