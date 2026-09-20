# SCH macroecology H2 modelability gate V1

## Question

H2 asks when the same canonical trait axis changes ecological state across contexts.

The current H2 layer contains ten materialized local cases, but the cases belong to two noncommensurate measurement families:

```text
plant-performance contexts
visitor-role behavior contexts
```

A combined regression across those layers would mix different estimands.

## Current local-case denominator

```text
TOTAL_LOCAL_CASES = 10
CANONICAL_AXES_WITH_CASES = 5
BIOLOGICAL_CLUSTERS_WITH_CASES = 4
AXES_WITH >=2 LOCAL_CASES = 4
```

Axes with at least two local contexts:

```text
Caryopteris_000330_corolla_tube
Blueberry_000076_corolla_access
Sesame_000336_corolla_tube
Sesame_000336_nectar_availability
```

Gentiana currently has one materialized local plant-performance context plus broader source-level evidence of spatial geometry change. Its additional population rows remain pending S3 extraction.

## Plant-performance layer

Current state:

```text
cases = 3
canonical axes = 2
clusters = 2
axes with >=2 local cases = 1
```

The single repeated plant-performance axis is *Caryopteris divaricata* corolla tube:

```text
natural robbery
-> short-tube realized advantage

robber exclusion
-> no detected tube-length effect
```

This is a valid within-axis ecological switch, but one axis is not a basis for a general H2 mixed model.

## Visitor-role behavior layer

Current state:

```text
cases = 7
canonical axes = 3
clusters = 2
axes with >=2 local cases = 3
```

The repeated axes are:

- blueberry corolla-access geometry;
- sesame corolla access;
- sesame nectar/resource state.

These cases resolve visitor role or foraging tactic, not local plant-fitness geometry.

They therefore cannot be pooled with the plant-performance layer.

## Project modelability gates

Before H2 model fitting, the following conservative project thresholds are frozen:

```text
minimum cases per layer             12
minimum canonical axes per layer     8
minimum independent clusters         8
minimum repeated axes                5
```

These are project safeguards, not universal statistical laws.

Current result:

```text
PLANT_PERFORMANCE_MODEL = FAIL
ROLE_BEHAVIOR_MODEL = FAIL
COMBINED_LAYER_MODEL = PROHIBITED_BY_ESTIMAND
```

## Why the combined model is prohibited

The two layers answer different questions.

### Plant-performance H2

```text
How does the realized fitness geometry of a trait change across contexts?
```

### Role-behavior H2

```text
How does the functional behavior of the visitor change across contexts?
```

A visitor can switch from legitimate use to robbing without producing a measurable fitness cost.

Sesame demonstrates exactly this distinction.

Therefore:

```text
consumer-role switch
!=
plant-fitness geometry switch
```

## Current mechanistic change classes

Seven change records are registered:

```text
GEOMETRY_CLASS_SWITCH                         1
GEOMETRY_DISAPPEARANCE                        1
COMPONENT_WEIGHT_SHIFT                        1
COMPONENT_WEIGHT_SHIFT_WITH_EVOLUTIONARY_RESPONSE 1
CONSUMER_ROLE_BEHAVIOR_SHIFT                  3
```

Five change records already contain two or more local materialized cases.

Two remain source-level only:

- *Pedicularis rex* component-weight shift;
- *Primula farinosa* component-weight shift with evolutionary response.

## What is licensed now

Primary H2 outputs currently licensed:

- source-resolved within-axis context descriptions;
- within-source treatment/cultivar contrasts;
- descriptive mechanistic change-type synthesis;
- source-object recovery and promotion audits.

Not licensed as primary analyses:

- mixed-effects context-switch regression;
- context-switch prevalence;
- one combined regression of plant-performance and role-behavior cases;
- counting unmaterialized reported contexts as observations.

## Scientific result that already survives the gate

Even without a general H2 model, the current evidence supports a stronger ecological statement:

> **Context dependence changes more than effect size. It can switch geometry class, erase a trait effect, change the relative weight of opposing components, alter evolutionary response, or change the behavioral role expressed by an interacting consumer.**

This is the H2 ecological contribution.

## Next data priorities

The largest gain now comes from fixed-role plant-performance source recovery:

1. *Gentiana lutea* S3 population selection table;
2. *Gymnadenia conopsea* Appendix A Table A2;
3. *Pedicularis rex* S1/S2/Appendix S1;
4. *Primula farinosa* population × experiment × time tables.

These sources can increase the plant-performance H2 layer rather than merely adding more role-behavior examples.

## Status

```text
H2_TOTAL_LOCAL_CASES = 10
H2_PLANT_PERFORMANCE_CASES = 3
H2_ROLE_BEHAVIOR_CASES = 7

H2_PLANT_PERFORMANCE_MODEL = FAIL_CLOSED
H2_ROLE_BEHAVIOR_MODEL = FAIL_CLOSED
H2_COMBINED_MODEL = NOT A VALID ESTIMAND

H2_PRIMARY_OUTPUT = DESCRIPTIVE_WITHIN_SOURCE_CONTRASTS
```
