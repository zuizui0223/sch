# SCH Castilleja linariaefolia source audit v1

## Decision

*Castilleja linariaefolia* is promoted to the highest-priority **short-path candidate** for complete SCH mechanism closure, but it is not yet execution-ready.

Its value is complementary to *Nicotiana attenuata*:

```text
Nicotiana  -> strongest experimentally manipulated same-coordinate evidence
Castilleja -> strongest direct pollination-vs-seed-predation conflict on seed fitness
```

## Primary evidence

### Cariveau et al. 2004 — Oikos

DOI: `10.1111/j.0030-1299.2004.12641.x`

The study examined hummingbird pollination and pre-dispersal seed predation by plume moth/fly larvae through female reproductive success. Supplemental pollination only marginally increased reproduction, with the authors interpreting seed predation as masking part of the pollination benefit. In observational trait-path analyses, calyx length experienced opposing selection via pollination and seed-predation routes.

Recovered SCH components:

```text
POLLINATOR_ROUTE_TO_W: RECOVERED
ANTAGONIST_ROUTE_TO_W: RECOVERED
COMMON_W_SEED_SET: RECOVERED
OPPOSING_SELECTION_ON_SAME_FLORAL_TRAIT: RECOVERED_OBSERVATIONALLY
ROLES_SEPARABLE_BY_TAXON/ROUTE: YES
```

Missing:

```text
RANDOMIZED_do(A): NOT RECOVERED FOR CALYX LENGTH
SELECTIVE_G_INTERVENTION: NOT RECOVERED
FULL_AxGxP: NOT RECOVERED
```

### Hixon, Carpenter & Paton 1983 — American Naturalist

DOI: `10.1086/284141`

This work experimentally changed *C. linariaefolia* flower density by controlled flower removals/additions and measured hummingbird territorial/foraging responses. It establishes that an experimentally manipulable floral-display coordinate is feasible in this species and that hummingbirds respond rapidly to that manipulation.

Recovered SCH feasibility:

```text
MANIPULATED_DISPLAY_A: YES
POLLINATOR_BEHAVIOURAL_RESPONSE_TO_DISPLAY: YES
```

Boundary:

- this is flower density/display, not calyx length;
- seed-predator response and common plant W were not tested in that experiment.

## What this changes

Before this audit, Castilleja's main weakness was the apparent lack of any practical `do(A)` precedent. The flower-density experiment removes that concern at the **display-coordinate** level, though not yet for the specific calyx-length coordinate showing opposing selection in Cariveau et al.

The system therefore has two candidate `A` strategies:

### Strategy A — display coordinate

```text
A = experimentally controlled flower number / display size
```

Advantages:

- directly manipulable with published precedent;
- hummingbird behavioural sensitivity is established;
- flower production/display enters the natural selection system studied by Cariveau et al.

Required recovery/new test:

- determine whether pre-dispersal seed predators respond positively to the same display contrast;
- ensure removal/addition does not mechanically alter the denominator of W; use standardized focal flowers or per-flower mature seed output rather than total plant seed count without adjustment.

### Strategy B — calyx-length coordinate

```text
A = calyx length / floral structural coordinate
```

Advantages:

- strongest existing evidence for opposing pollinator-vs-seed-predator selection on the same trait.

Required development:

- design a reversible/physical manipulation or select naturally matched flowers with a validated manipulation instrument;
- show the manipulation changes receiver-facing calyx geometry without damaging reproductive organs, nectar access or other flower traits.

Current recommendation: **test display first for manipulatability and seed-predator response; retain calyx length as the stronger evolutionary coordinate if a clean manipulation can be developed.**

## P intervention

The pollination route is comparatively tractable.

Existing work already uses pollen supplementation in this species. A confirmatory SCH design could use:

```text
P0 = standardized pollen-limited / visitor-excluded condition
P1 = standardized supplemental cross-pollination or validated natural pollinator access
```

However, the final contrast must represent a biologically interpretable pollinator-mediated contribution rather than simply pollen quantity. The exact P design should be chosen after pilot work on self-compatibility, autonomous fruit set and pollen limitation in the execution population.

Status:

```text
P_INTERVENTION_FEASIBILITY: STRONG_PARTIAL
```

## G intervention

This remains the main unresolved methodological cell for Castilleja.

The ideal G manipulation would suppress plume moth/fly pre-dispersal seed predation after pollination while leaving flower display, hummingbird access and seed development otherwise unchanged.

Candidate routes for source recovery/pilot:

- post-pollination fine-mesh fruit/ovary exclusion;
- targeted removal of eggs/larvae from focal fruits;
- selective insecticide applied only after flowers cease functioning, if a treatment can be validated as pollinator-neutral and development-neutral;
- bagging or sleeve treatment timed after the pollination window but before seed-predator oviposition.

Promotion requires a manipulation check showing:

```text
G1 -> higher seed-predator incidence
G0 -> substantially lower seed-predator incidence
no material change in P treatment or A coordinate
```

Status:

```text
G_INTERVENTION: OPEN_HIGH_PRIORITY
```

## Common W

Castilleja has an important advantage over Nicotiana: the antagonist is a pre-dispersal seed predator, so the causal endpoint is naturally close to maternal reproductive fitness.

Preferred W:

```text
mature intact viable seeds per standardized focal flower/fruit
```

Secondary outcomes:

```text
fruit set
seed number before predator loss
predator incidence
intact mature seed number
germination/viability if feasible
```

This allows the antagonist-mediated loss to be defined directly on the same scale as the pollinator-mediated gain.

## Current gate state

```text
same-coordinate natural opposing selection:   RECOVERED
P -> reproductive W:                          RECOVERED
G -> reproductive W:                          RECOVERED
common mature W:                              RECOVERED
roles biologically separable:                 RECOVERED
manipulated floral display A:                 RECOVERED_FEASIBILITY
same manipulated A -> antagonist response:    OPEN
selective P intervention:                     PARTIAL_STRONG
selective G intervention:                     OPEN_CRITICAL
clean manipulated calyx A:                    OPEN
complete A x G x P:                           NOT_EXECUTED
```

## Comparison with Nicotiana

### Nicotiana wins on

- direct manipulation of a chemically explicit attraction coordinate;
- experimentally demonstrated same-coordinate response by both audience routes;
- direct BITA defence extension.

### Castilleja wins on

- distinct mutualist and antagonist guilds;
- very short antagonist -> seed-fitness path;
- natural opposing selection already identified on a floral trait;
- common W is immediately interpretable as seed fitness.

Therefore the programme should not choose between them prematurely.

## Next decisive test

For Castilleja, the highest-information pilot is not yet the full 8-cell design. It is a two-part feasibility test:

```text
Pilot C1
A(display low/high)
-> hummingbird response
-> seed-predator oviposition/incidence

Pilot C2
post-pollination G suppression
-> predator incidence
-> mature intact seeds
with A and P held fixed
```

If C1 shows that seed predators track the same manipulated display coordinate and C2 shows a selective, strong G intervention, Castilleja becomes the leading complete SCH system.

If C1 fails, retain Castilleja as real-world opposing-selection evidence but not as the primary shared-cue experiment. If C2 fails, its short-path advantage cannot be exploited experimentally.

## Programme status after audit

```text
NICOTIANA:
L0/shared-coordinate strength = highest
complete mechanism identifiability = uncertain

CASTILLEJA:
functional conflict / G->W strength = highest current candidate
same manipulated A intersection = still missing
```

The next recovery should search primary studies on Castilleja seed-predator phenology and exclusion methods before designing C2 from scratch.