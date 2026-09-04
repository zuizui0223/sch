# SCH Dalechampia causal compromise experiment v1

## Decision

`Dalechampia` is a **conditional first-choice** system for a direct Chapter-1 test of shared-trait compromise geometry.

The positive anchor is the Mexican `D. scandens` population studied by Pérez-Barrales et al. (2013), where larger showy bracts increased bee visitation and pollen arrival and were also associated with greater seed predation, producing opposing selection and a stabilizing net tendency. The important boundary is that this is not species-wide: Opedal et al. (2019) found little relationship between floral advertisement and seed predation across focal and 20-population samples in northern Costa Rica.

Therefore the experiment begins by identifying a **conflict-active focal population / season**. It does not assume that any `D. scandens` population has the required geometry.

The target quantities remain:

```text
z1*   function-1 / pollination optimum
z2*   function-2 / predator-avoidance optimum
zc*   combined shared-trait optimum
```

and the decisive causal prediction remains:

```text
weaken one functional demand
-> zc* moves toward the optimum favored by the remaining function.
```

## Trait and functions

Primary shared trait:

```text
z = apparent involucral-bract display area during the receptive / receiver-choice window
```

Primary functions:

```text
F1 = pollinator-mediated pollen transfer / reproductive gain
F2 = avoidance of predispersal seed-predator loss
```

Primary common fitness endpoint:

```text
mature intact viable seeds per focal blossom
```

The common outcome is downstream of both functions; visitation and predator occurrence are mediators, not substitutes for `W`.

## Source-defined boundary before experimentation

### Positive case

Pérez-Barrales et al. (2013; DOI `10.1111/j.1600-0706.2013.20780.x`) studied one Mexican population. Blossoms with larger bracts received more bee visits and pollen, and seed-predation probability increased with bract size and seed production. The integrated female-fitness surface tended toward stabilizing selection.

The paper explicitly states that interpreting the predation pattern as adult curculionid oviposition choice assumes the pattern was not generated instead by differential larval success or inter-inflorescence larval movement. Thus the natural selection result is direct, but the exact adult oviposition window is not yet a directly recovered SCH intervention coordinate.

### Geographic negative / boundary case

Opedal et al. (2019; DOI `10.1002/ajb2.1209`) studied northern Costa Rica and found seed-predation probability largely unrelated to floral advertisement within focal populations and across a broader 20-population sample. This makes antagonist weight a context-dependent property rather than a fixed species trait.

Updated status:

```text
REAL_WORLD_DALECHAMPIA_CONFLICT:       RECOVERED_CASE_LEVEL
SPECIES_WIDE_CONFLICT:                 NOT SUPPORTED
GEOGRAPHIC_TURNOVER_IN_CONFLICT:       RECOVERED
DIRECT_OVIPOSITION_WINDOW:             NOT RECOVERED
```

## Critical manipulation problem: do not permanently clip bracts

Permanent bract clipping is not the preferred confirmatory manipulation when mature seeds are the common outcome.

During fruit maturation, `D. scandens` bracts turn green and contribute photosynthate to developing seeds. Permanent removal or shading can therefore create a direct carbon / development effect on seed outcome that is not part of the pollinator-versus-seed-predator conflict.

The confirmatory manipulation must alter the **apparent display coordinate during the ecological decision window** while preserving post-pollination bract tissue and function.

## Stage 0P — qualify a conflict-active population

Before constructing a factorial experiment, screen candidate populations / seasons with natural blossoms.

Record:

```text
apparent bract area
pollinator visitation
stigmatic pollen receipt
seed-predator incidence / damaged seeds
seeds initiated
mature intact seeds
plant / patch / date / phase
```

Promotion requires:

```text
P0.1 enough seed-predator incidence to estimate a G contrast
P0.2 pollination responds to the declared bract-display coordinate
P0.3 predation also responds to that coordinate or a tightly linked same-blossom state
P0.4 the two functions imply non-aligned preferred states over an experimentally reachable range.
```

If these conditions are not recovered, the focal population is not used for the positive compromise experiment. That outcome is biologically informative because SCH predicts that a weak antagonist weight can erase the compromise.

## Stage 0A — reversible multi-level z manipulation

Preferred manipulation:

```text
natural bract tissue remains intact
+
removable spectrally matched occluders for downward display shifts
+
removable spectrally matched artificial extensions for upward display shifts.
```

Initial planning levels:

```text
z = 0.60, 0.80, 1.00, 1.20, 1.40 x a standardized reference apparent area
```

These are not frozen doses. Stage 0 narrows them to the locally natural / behaviourally relevant range.

Promotion checks:

```text
Z0.1 measured apparent area changes as intended
Z0.2 visible and UV state is close enough that area is the main changed coordinate
Z0.3 gland visibility and access are unchanged
Z0.4 resin amount / gland size are unchanged
Z0.5 posture and blossom geometry are not mechanically distorted
Z0.6 material can be removed without lasting tissue damage
Z0.7 sham material does not alter visitation, predator response or seed development.
```

If credible upward extension cannot be built, use a bounded lower-side intervention plus a separately labelled natural-trait surface rather than pretending that a symmetric five-level causal axis exists.

## Stage 0B — pollinator intervention

Candidate pollinator states:

```text
P1 = natural pollinator access during the receptive window
P0 = pollinator exclusion during a matched window
```

Because `D. scandens` is self-compatible and can produce seeds by autonomous self-pollination, `P0` is not assumed to imply zero reproduction. A hand-pollination calibration arm maps pollen receipt to seed production independently of pollinator choice.

Promotion requires the P manipulation to change pollen delivery strongly while leaving antagonist exposure, `z`, resin reward and blossom development unchanged except through the declared pollination pathway.

## Stage 0G — recover the antagonist intervention instead of assuming it

The exact adult seed-weevil oviposition window is not currently frozen from primary-source recovery. Therefore broad passive exclusion is not the first-choice strategy.

The preferred pilot is **controlled sequential adult-weevil exposure**.

### Exposure-window pilot

Use blossoms with matched `z` and pollination status, and assign controlled adult-weevil access to sequential phenological windows:

```text
E0 no adult-weevil exposure
E1 female-phase exposure
E2 early bisexual-phase exposure
E3 late bisexual-phase exposure
E4 post-receptive / early fruit-development exposure.
```

The Mexican study reports receptive blossoms for up to roughly 10–12 days, with an initial female phase followed by a bisexual phase. The exact exposure windows are updated from local phenology; the categories above define the identification logic rather than fixed days.

For each exposure:

```text
standardize adult number and sex where possible
standardize exposure duration
use a chamber / mesh that does not alter the display outside the exposure period
record adult contact, probing or feeding when observable
retain a handling / chamber sham
track blossoms to developing and mature seeds
score damaged seeds, larvae / emergence where possible, and intact viable seeds.
```

The primary antagonist chain is deliberately bounded:

```text
controlled adult-weevil exposure
-> later seed-predator establishment / seed damage
-> mature intact seed loss.
```

Do not call this direct oviposition unless eggs, oviposition scars or equivalent direct markers are independently observed.

### G0/G1 promotion rule

A seed-predator intervention is admitted only if:

```text
G1 controlled exposure materially increases later seed loss
G0 no-exposure / validated exclusion keeps later seed loss low
pollination / pollen receipt is preserved across G states conditional on P
z, resin reward, bract posture and post-pollination bract integrity are preserved
sham chamber / handling effects are acceptably small.
```

Broad insecticide is not admitted by default. Broad bagging is not admitted unless it passes the same selectivity checks.

If controlled exposure cannot generate a reproducible antagonist contrast, Dalechampia remains a real-world compromise anchor but is not promoted to a mechanism-resolved L3 system.

## Stage 1 — local multi-level surface pilot

Only after Stage 0P, 0A, 0B and 0G pass, use:

```text
5 z levels x 2 pollinator states x 2 seed-predator states
= 20 cells.
```

Randomize within plant / patch where biology permits. Preserve at minimum:

```text
plant / genotype
patch
blossom
calendar date
phenological phase
z target and measured apparent area
pollinator treatment
seed-predator treatment / exposure window
sham / manipulation batch.
```

Primary endpoint:

```text
mature intact viable seeds per focal blossom.
```

Secondary decomposition:

```text
bee visitation / visit probability
stigmatic pollen load
fruit set / seed initiation
predator contact or direct oviposition marker if available
predated seed count
intact seed count
seed mass / viability.
```

## Function-specific surfaces

At each `z`, estimate:

```text
W(z,G,P)
```

and recover the multi-level analogues of pollinator-mediated contribution and predator-mediated loss.

Target surfaces:

```text
F1(z)  pollinator-mediated reproductive contribution
F2(z)  predator-avoidance / surviving-seed contribution
W(z)   combined mature-intact-seed fitness.
```

Use flexible smooth or low-order polynomial models only if the data support their shape. The quadratic SCH -> BITA bridge is a local benchmark, not a compulsory global fit.

## Primary Chapter-1 decisions

### C1 — multifunctionality

```text
z changes both functional routes.
```

### C2 — functional conflict

```text
z1* != z2*.
```

### C3 — shared compromise

```text
zc* lies away from both function-specific optima in the predicted direction
and the combined surface contains an interior optimum or bounded balance region.
```

### C4 — causal optimum shift

```text
weaken / remove seed-predator function
-> zc* moves toward z1*

weaken / remove pollinator function
-> zc* moves toward z2*.
```

Report optimum displacement with uncertainty rather than only a treatment p-value.

### C5 — gradient cancellation

Near `zc*`, the total gradient is approximately zero while function-specific marginal gradients remain non-zero and oppose one another.

This distinguishes balance from an uninformative flat surface.

## Direct-cost control

After temporary display materials are removed, compare sham and manipulated blossoms under standardized hand pollination and predator exclusion. Persistent effects on seed number, seed mass or viability are treated as a direct manipulation / bract-function pathway, not silently assigned to pollination or predation.

## Power policy

Do not power the final experiment from the published observational stabilizing-selection coefficient or from a bract-reduction pollen effect in another `Dalechampia` species.

Stage 1 estimates:

```text
within-plant / patch variance
cell retention
visit probability
pollen-load dispersion
predator incidence under controlled exposure
mature-intact-seed variance
curvature / optimum uncertainty
cross-route contamination of P and G interventions.
```

Confirmatory sample size is then determined by simulation for C2-C5, especially optimum separation and optimum displacement.

## Negative-control logic

A multifunctional trait is not automatically a compromise. Aligned-optimum systems remain deliberate negative controls. Dalechampia itself also supplies a context-level boundary: Costa Rican populations with weak predator coupling may behave like a low-`w2` state in which the compromise is absent or small.

Thus a failed Dalechampia population screen is not a nuisance result. It directly supports the prediction that changing functional weights can move or erase the shared optimum.

## Handoff to BITA

If C2-C5 are recovered, Chapter 1 delivers:

```text
z1*, z2*, zc*, compromise penalty / optimum displacement.
```

BITA then asks whether a second functional coordinate reduces that one-dimensional penalty and releases the first trait toward its function-specific optimum.

## Current status

```text
MEXICO_CASE_LEVEL_OPPOSING_SELECTION:      RECOVERED
OBSERVATIONAL_STABILIZING_COMPROMISE:      RECOVERED_CASE_LEVEL
COSTA_RICA_SPECIES_WIDE_GENERALIZATION:    NEGATIVE / GEOGRAPHICALLY_VARIABLE
BRact_ADVERTISEMENT_MANIPULABILITY:        RECOVERED_IN_GENUS
PERMANENT_BRact_REMOVAL_COMMON_W_CONFOUND: RECOVERED
CONFLICT_ACTIVE_FOCAL_POPULATION:          TO SCREEN
REVERSIBLE_MULTI_LEVEL_Z:                  TO VALIDATE
SELECTIVE_P:                               TO VALIDATE
DIRECT_OVIPOSITION_WINDOW:                 NOT RECOVERED
CONTROLLED_WEevil_EXPOSURE:                TO PILOT
SELECTIVE_G0_G1:                           MAIN BOTTLENECK
CAUSAL_Z1_Z2_ZC_RECOVERY:                  NOT YET EXECUTED
```

The companion recovery note is `docs/SCH_DALECHAMPIA_GEOGRAPHIC_CONFLICT_AND_G0_RECOVERY_V1.md`.
