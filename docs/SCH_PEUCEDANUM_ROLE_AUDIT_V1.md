# Peucedanum multivittatum role audit v1

## Decision

`Peucedanum multivittatum` is **not** promoted to the first causal SCH execution system.

Its strongest current value is different:

```text
SCH: real-world evidence that functional weights and selection on floral allocation shift with seed-predator pressure
BITA: unusually strong natural example of partial functional differentiation between perfect and male flowers
```

This distinction matters because the extant architecture is already andromonoecious. It is therefore not a clean example of a single undifferentiated trait `z` whose compromise is subsequently split experimentally.

## Primary sources

- Kudo & Shibata 2021, *Ecology and Evolution*, DOI `10.1002/ece3.7468`
- Kudo & Shibata 2025, *Journal of Ecology*, DOI `10.1111/1365-2745.70130`
- Dryad 2021-study data: DOI `10.5061/dryad.b5mkkwhcq`
- Dryad later-study data: DOI `10.5061/dryad.w3r2280v5`

## Recovered architecture

`P. multivittatum` is andromonoecious. Terminal umbels contain perfect and male flowers. During the male phase, perfect and male flowers are similar in form and pollen output, but only perfect flowers subsequently carry female/seed function.

The main natural pathways are therefore:

```text
perfect flowers
  -> pollen donation
  -> female fruit/seed production
  -> seed-predator target

male flowers
  -> pollen/display function
  -> no direct seed target
```

This is already a partially differentiated architecture.

## 2021 evidence: geographic functional-weight mosaic

Across nine Taisetsu populations over 2017-2019:

```text
early flowering / early snowmelt
-> intense predispersal seed predation
-> more male-biased sex allocation

late flowering / late snowmelt
-> negligible predation
-> more perfect flowers.
```

Fruit-set success increased with perfect-flower number, whereas male-flower number was not associated with fruit-set success. Predation damage ranged from strong in early populations to absent in late populations.

This is useful SCH evidence that the ecological weight on reproductive allocation changes sharply across local environments. It is not a causal `z x P x G` compromise experiment.

## 2025 evidence: opposing selection and partial differentiation

The later four-year study strengthens the interpretation:

```text
more perfect flowers
-> more moth oviposition / seed predation
-> lower female fitness under strong predation

more total flowers
-> greater siring success

more male flowers
-> reduced predation damage
```

The study reports that male-flower production reduced predation damage but that this effect was independent of measured male fitness as a pollen donor. Selection on perfect-flower production shifted from negative in high-predation early-flowering populations to positive in low-predation late-flowering populations.

This is strong real-world evidence for context-dependent allocation and for a differentiated male-only flower class preserving display/pollen function while avoiding seed-bearing exposure.

## Why this is not the main SCH causal system

The canonical Chapter-1 result requires a manipulable shared coordinate and selective functional interventions that recover state-specific optima:

```text
z_P*
z_G*
z_C*.
```

Current Peucedanum evidence is observational/selection-based and the extant architecture already contains distinct male and perfect flower classes. Therefore:

```text
SHARED_FUNCTIONAL_WEIGHT_MOSAIC: RECOVERED
OPPOSING_SELECTION_ON_ALLOCATION: RECOVERED
CAUSAL_SHARED_TRAIT_COMPROMISE: NOT IDENTIFIED
```

## Best experimental use

If used experimentally, Peucedanum is better treated as a BITA-style allocation system than as the first SCH surface.

A useful manipulation would hold total terminal-umbel display approximately constant while altering male:perfect flower composition, then measure:

```text
paternity / siring success
female intact-fruit production
moth oviposition
predation damage
```

Selective flower removal could create composition contrasts, but it changes potential ovule number by design and therefore requires separate male and female fitness accounting. It should not be forced into the current single-fitness SCH receipt without a new preregistered estimand.

## Data availability boundary

The relevant Dryad datasets are public and list the raw Excel files used by the published analyses. They have not yet been imported into this repository, so no repository-level reanalysis result is claimed here.

## Current role

```text
Pedicularis rex       -> best causal-method benchmark for shared compromise -> water-y release, subject to field access
Peucedanum multivittatum -> best Japan-accessible natural partial-differentiation / selection-mosaic system
Dalechampia           -> strongest published stabilizing-compromise case
Nicotiana attenuata   -> strongest local same-cue mechanism bridge
```

## Claim ceiling

Peucedanum currently supports:

```text
real-world functional-weight mosaic
context-dependent selection on floral allocation
partial functional differentiation of flower classes
```

It does not yet establish:

```text
causal SCH state optima
experimental dimensional release
ancestral shared -> differentiated historical transition
complete structural/developmental modularity.
```
