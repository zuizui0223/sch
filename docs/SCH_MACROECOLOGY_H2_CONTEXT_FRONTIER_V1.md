# SCH macroecology H2 context frontier V1

## Objective

H1 asks which ecological geometries occur on canonical trait axes.

H2 asks a different question:

> **When does the same canonical trait axis change ecological geometry across populations, years, treatments, or consumer regimes?**

A source-level `context_shift_detected = YES` flag is not yet a context case. H2 therefore requires explicit expansion into repeated ecological observations nested inside one canonical trait axis.

## Current H2 frontier

The canonical ledger contains 48 biological trait axes.

Thirty currently have source-supported context variation and enter the H2 extraction queue:

```text
H2 queue axes                      30
independent biological clusters   13
```

The 30 axes split into four biologically distinct lanes.

### H2A — geometry switch already confirmed

```text
axes = 1
```

Current case:

- *Gentiana lutea* yellow-orange flower-colour axis.

The focal-population source supports reinforcement, whereas the broader multi-population source supports a one-sided/context-dependent pattern.

This is already a cross-source geometry switch and should be decomposed into explicit population/source contexts rather than counted twice.

### H2B — geometry resolved, context dependence reported

```text
axes = 8
```

Examples include:

- *Gymnadenia conopsea* flowering phenology;
- *Gymnadenia conopsea* spur length;
- *Pedicularis rex* corolla exsertion;
- *Primula farinosa* scape-height morph;
- *Tanacetum vulgare* individual chemotype;
- *Tanacetum vulgare* plot-level chemodiversity;
- *Trifolium repens* flower size;
- *Trifolium repens* inflorescence production.

These axes have a resolved canonical geometry but also a source-supported context effect. H2 must determine whether context changes:

- component strength only;
- one component from present to null;
- the sign of a component;
- or the complete geometry class.

### H2C — context present, geometry still unresolved

```text
axes = 10
```

These are especially valuable because context-case extraction may solve an H1 ambiguity rather than merely describe heterogeneity.

Current examples include:

- four *Erysimum mediohispanicum* corolla axes;
- *Polygala vayredae* flower size and nectar reward;
- three *Primula farinosa* floral-trait axes;
- *Trifolium repens* flowering time.

These are P1 extraction targets.

### H2D — consumer role changes with context

```text
axes = 11
```

These axes are not part of fixed-role H1, but they contain a separate ecological phenomenon:

> the functional role of the visitor itself changes with morphology or context.

Current systems include:

- blueberry corolla access and legitimate-versus-robbing behavior;
- *Caryopteris divaricata* floral access/reward;
- *Lithophragma bolanderi* brood-pollination architecture;
- *Primula secundiflora* morph-dependent nectar robbing/pollination;
- sesame corolla/reward axes.

This lane should remain separate from fixed-role geometry switching.

## Priority

The frozen extraction order is:

```text
P1
  H2A confirmed geometry switches
  H2C unresolved fixed-role axes with repeated context
  H2D consumer-role context

P2
  H2B resolved fixed-role axes with context dependence
```

Why H2C outranks H2B:

- H2C can convert unresolved canonical axes into identified ecological geometry;
- H2B already has an H1 classification and mainly refines heterogeneity.

## Current trait-domain composition

Across the H2 queue:

```text
MORPHOLOGY        19
REWARD             4
CHEMICAL_SIGNAL    3
DISPLAY_STATE      2
PHENOLOGY          2
```

This concentration in morphology is descriptive only and cannot be interpreted as a biological prevalence pattern because the systematic screen and context-case extraction are incomplete.

## Consumer-role composition

```text
NET_ANTAGONISTIC       19
ROLE_DEPENDENT          7
BENEFIT_COST_COUPLED    4
```

Thus over one third of the current H2 queue is not a simple fixed mutualist-versus-antagonist comparison.

This is itself a reason to separate:

```text
geometry switching
!=
consumer-role switching
```

## Context-case unit

Every H2 case must be materialized as:

```text
canonical trait axis
  -> population / site
  -> year / season
  -> treatment / consumer regime
  -> local function-1 direction
  -> local function-2 direction
  -> local geometry
```

A study with only one usable context is never coded as a negative context-switch case.

## What is not licensed yet

Current H2 status:

```text
canonical context-shift queue = READY
context cases                  = 0
H2 model                       = NOT READY
```

Therefore the following remain prohibited:

- treating `context_shift_detected` as a replicated observation;
- estimating the frequency of context switching;
- mixed models on the 30 queue axes;
- pooling role-dependent and fixed-role contexts into one outcome.

## Next extraction targets

Highest-value first systems:

1. *Gentiana lutea* colour — already known cross-source geometry switch;
2. *Erysimum mediohispanicum* — eight-population selection mosaic and four unresolved corolla axes;
3. *Primula farinosa* — multi-population floral-trait selection with existing scape conflict anchor;
4. *Pedicularis rex* — 14-population pollinator/seed-predator component data;
5. *Gymnadenia conopsea* — factorial pollination × herbivory context;
6. role-switch systems such as *Caryopteris*, blueberry and sesame.

## Claim ceiling

```text
H2_QUEUE_AXES = 30
H2_QUEUE_CLUSTERS = 13

GEOMETRY_SWITCH_CONFIRMED = 1
RESOLVED_FIXED_ROLE_CONTEXT_AXES = 8
UNRESOLVED_FIXED_ROLE_CONTEXT_AXES = 10
CONSUMER_ROLE_CONTEXT_AXES = 11

CONTEXT_CASES_MATERIALIZED = 0
H2_MODEL = NOT_READY
H2_PREVALENCE = NOT_ESTIMATED
```
