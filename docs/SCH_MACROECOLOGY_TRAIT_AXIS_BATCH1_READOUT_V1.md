# SCH macroecology trait-axis outcome readout — Batch 1

## Status

Batch 1 is the first ecological-outcome recode performed **after** the design-only eligibility gate was frozen.

```text
source records                    8
independent biological clusters  7
trait axes                       15
fixed-role geometry resolved      7 axes / 5 clusters
role-dependent boundary           1 axis
remaining unresolved/partial      7 axes
```

The batch is deliberately small and non-random. It is an early descriptive result, not the final H1-H3 macroecology sample.

## First ecological result: pollinator-antagonist systems do not have one geometry

Among the seven fixed-role trait axes for which the present sources resolve the ecological geometry:

```text
CONFLICT / OPPOSITION             3
ALIGNMENT / REINFORCEMENT         2
ONE-SIDED OR NULL                 2
```

This is not a prevalence estimate. Its value is qualitative specificity: even inside the antagonist-enriched SCH sampling frame, the same broad interaction label does not imply opposing selection.

### Conflict

- *Gymnadenia conopsea*, flowering phenology: pollinators favor later flowering while herbivores favor earlier flowering.
- *Primula farinosa*, scape-height morph: pollinators favor long scapes while grazers favor short scapes.
- *Dalechampia scandens*, upper bract area: published component gradients have opposite signs.

### Alignment / reinforcement

- *Gymnadenia conopsea*, spur length: both pollinators and herbivores select longer spurs.
- *Gentiana lutea*, flower colour in the focal population: pollinator- and seed-predator-mediated paths both favor yellow flowers.

### One-sided or null

- *Cucurbita pepo* var. *texana*, enhanced fragrance: florivore attraction and reproductive cost increase while pollinator attraction does not.
- *Gentiana lutea*, flower colour across 12 populations: pollinator response varies spatially, while seed predators are not detected as selective agents on colour in the multi-population analysis.

The immediate ecological implication is therefore:

> **antagonist presence is not equivalent to functional conflict.**

What matters is the sign and strength of the antagonist-mediated contribution on the declared trait axis.

## Second ecological result: geometry is trait-axis specific

The strongest within-system demonstration is *Gymnadenia conopsea*.

```text
flowering phenology:
pollinator -> later
herbivore  -> earlier
=> conflict + near cancellation

spur length:
pollinator -> longer
herbivore  -> longer
=> reinforcement
```

Thus a plant-pollinator-herbivore **system** is not correctly labeled as conflicted or aligned without specifying the trait coordinate.

This directly supports the three-level macroecology architecture:

```text
context case -> trait axis -> biological cluster
```

## Third ecological result: conflict can be hidden by cancellation

The flowering-phenology axis in *Gymnadenia* supplies the first explicit H3 case.

Pollinator- and herbivore-mediated selection act in opposite directions with similar additive strength, yielding little or no net selection on phenology.

The ecological reading is:

```text
weak net selection
!=
weak ecological selection
```

Strong opposing selective components can cancel.

Exact cancellation magnitude remains pending the registered Appendix A numeric/covariance reconstruction. The current result is directional.

## Fourth ecological result: geometry can change across space without changing the trait

Four of the seven resolved fixed-role axes already have a source-supported context-shift signal.

The clearest examples are:

- *Primula farinosa*: the pollinator-grazer balance changes among populations and predicts changes in scape-morph frequency.
- *Gentiana lutea*: pollinator preferences for the same yellow-orange colour coordinate vary among populations; the multi-population study does not recover seed-predator colour selection.
- *Gymnadenia conopsea*: changing pollination/herbivory regimes changes the component selection acting on the same floral axes.

The two *Gentiana* records are assigned to one biological cluster rather than counted as independent replication. Their value is within-program context contrast.

## Fifth ecological result: consumer roles themselves can be context dependent

The *Primula secundiflora* axis is retained as a boundary rather than forced into H1.

Nectar-robbing bumblebees can also transfer pollen, and their reproductive contribution depends on floral morph. Therefore:

```text
consumer label = "nectar robber"
does not guarantee
functional role = antagonist
```

SCH macroecology records this as `ROLE_DEPENDENT`. Fixed-role H1 excludes such cases, while a later role-switch analysis can retain them as biologically informative.

## Unresolved axes are retained

Six *Erysimum mediohispanicum* trait axes are already resolved as spatially stable or context-variable at the total-selection level, but the exact pollinator-versus-herbivore component sign is not yet frozen trait by trait. They remain in the ledger as `UNRESOLVED` rather than being inferred from the paper-level statement that the geographic mosaic reflects a balance of mutualistic and antagonistic selection.

Likewise, the *Gymnadenia* floral-display axis is retained while its agent-specific direction awaits table-level recoding.

## What this changes in the SCH story

The macroecology layer is no longer only a plan. Batch 1 supports a bounded ecological statement:

> **Realized multifunctional geometry is axis- and context-specific: the same broad mutualist-antagonist setting can generate opposition, reinforcement, one-sided costs, cancellation, or role switching.**

This statement is stronger than "multifunctionality is not conflict" but remains below a population-frequency claim.

## Claim ceiling

```text
BATCH1_TRAIT_AXIS_RESULT = DESCRIPTIVE_ECOLOGICAL_PATTERN_RECOVERED
FIXED_ROLE_RESOLVED_AXES = 7
INDEPENDENT_CLUSTERS_WITH_RESOLVED_AXES = 5
CONFLICT_PREVALENCE = NOT_ESTIMATED
H1_MODERATOR_EFFECTS = NOT_ESTIMATED
H2_POPULATION_FREQUENCY = NOT_ESTIMATED
CANCELLATION_MAGNITUDE = NOT_ESTIMATED
FULL_MACRO_INFERENCE = CLOSED
```

Next: expand the same outcome-blind design recode to the remaining primary-study queue, freeze cluster/program dependence, and only then fit the registered macro models.
