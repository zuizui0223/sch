# SCH pure-function optimum upgrade v1

## Purpose

The default multi-level `z x P x G` experiment identifies state-specific reproductive optima:

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

These are sufficient for the default causal-compromise claim. They are not automatically the theory-level pure function optima `z_F1*` and `z_F2*` because direct/background trait consequences remain in every state surface.

A stronger identification is possible from the same randomized crossed experiment when the causal **component surfaces themselves** have stable optima across the other functional context.

Implementation:

```text
scripts/identify_sch_pure_function_optima.py
```

## Component surfaces

Define pollinator-mediated reproductive contribution at each antagonist state:

```text
M_G0(z) = W10(z) - W00(z)
M_G1(z) = W11(z) - W01(z).
```

Define antagonist-present reproductive contribution at each pollinator state:

```text
H_P0(z) = W01(z) - W00(z)
H_P1(z) = W11(z) - W10(z).
```

`H` is oriented on the common reproductive scale: larger is better. When antagonists only impose losses, `H` will usually be non-positive and its optimum is the state at which antagonist-mediated loss is least severe.

Because each component is a randomized-state difference, consumer-independent baseline effects cancel algebraically if the interventions are selective.

## Why context stability matters

A single theory-level function optimum is not identified merely because one component contrast has a maximum.

For function 1, SCH observes two conditional component surfaces:

```text
M_G0(z)
M_G1(z).
```

For function 2 it observes:

```text
H_P0(z)
H_P1(z).
```

If the optimum changes materially with the other function's state, the functional effect is context-dependent and there is no single empirical `z_F1*` or `z_F2*` to export.

Therefore the upgrade requires:

```text
optimum(M_G0) ~= optimum(M_G1)
optimum(H_P0) ~= optimum(H_P1)
```

within prospectively frozen equivalence bounds, with all four component optima supported as interior concave optima across a declared fraction of plant-cluster bootstrap replicates.

## Positive promotion

Only when both function pairs pass does the upgraded receipt contain:

```text
identified_pure_function_optima.z_F1
identified_pure_function_optima.z_F2
```

with semantics:

```text
CONTEXT_STABLE_CAUSAL_COMPONENT_OPTIMA_ON_COMMON_REPRODUCTIVE_SCALE.
```

The upgrade status is:

```text
CONTEXT_STABLE_COMPONENT_OPTIMA_IDENTIFIED.
```

If either pair is context-dependent, non-concave, boundary-limited, or too uncertain, status is:

```text
PURE_FUNCTION_OPTIMA_NOT_IDENTIFIED.
```

and no `identified_pure_function_optima` field is emitted.

## Claim ceiling

This upgrade does not weaken the default SCH result. A system may have a strong causal shared-trait compromise while its functional components remain context-dependent.

The hierarchy is therefore:

```text
state-specific causal compromise
    does not require pure-function optima

context-stable component optima
    -> optional empirical mapping to z_F1*, z_F2*

context-dependent component optima
    -> retain M_G0*, M_G1*, H_P0*, H_P1* separately.
```

The pure-function label additionally assumes the randomized interventions isolate the declared functional components on the chosen reproductive scale. Failed manipulation checks invalidate the upgrade even if the numerical surfaces align.

## BITA handoff

BITA defaults to state-specific release toward `z_P*`.

Only an upgraded SCH receipt may unlock:

```text
sch_reference_mode = pure_function
```

and the stricter Chapter-2 estimand:

```text
R_pure = |x0* - z_F1*| - |x1* - z_F1*|.
```

This prevents a state optimum from being silently relabeled as a pure functional optimum.
