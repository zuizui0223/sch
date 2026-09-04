# SCH causal compromise surface analysis v1

## Purpose

This is the registered first-pass analyzer for the confirmatory Chapter-1 experiment after Stage 0 has identified:

```text
one conflict-active context
+ one manipulable shared z coordinate
+ selective pollinator state P
+ selective antagonist state G.
```

The analysis turns a randomized multi-level

```text
z x P x G
```

experiment into explicit estimates of intervention-defined state optima, optimum shifts, functional-component gradients, and residual P x G interaction.

Implementation:

```text
scripts/analyze_sch_compromise_surface.py
```

## Critical notation boundary

SCH distinguishes **theoretical pure function optima** from **experimentally identified state optima**.

The theoretical framework may define

```text
z_F1* = argmax F1(z)
z_F2* = argmax F2(z)
```

for isolated function-specific objectives. These are useful theoretical quantities, but the crossed reproductive experiment does not generally identify them because consumer-independent/direct consequences `C(z)` remain in every reproductive state unless they are separately measured.

The experiment directly identifies:

```text
z_P* = argmax W10(z)  = z_pollinator_context
z_G* = argmax W01(z)  = z_antagonist_context
z_C* = argmax W11(z)  = z_combined.
```

Therefore:

```text
z_P* != automatically z_F1*
z_G* != automatically z_F2*.
```

Equality requires an additional identifying argument or independent direct-cost / baseline assay. The analyzer never infers pure function optima by subtraction.

## Required data

Template:

```text
empirical/architecture/SCH_CAUSAL_COMPROMISE_SURFACE_TEMPLATE_V1.csv
```

Required columns:

| column | meaning |
|---|---|
| `plant_id` | biological cluster / randomization block |
| `blossom_id` | unique experimental unit |
| `z_level` | preregistered assigned trait level |
| `z_measured` | measured realized value of the declared shared coordinate |
| `pollinator_state` | `0` or `1` |
| `antagonist_state` | `0` or `1` |
| `fitness_value` | common primary reproductive outcome on one declared scale |

For Dalechampia the intended primary `fitness_value` is mature intact viable seeds per focal blossom. Other systems may use another predeclared common fitness outcome, but the scale must be identical across all cells.

## Four state surfaces

The analyzer fits a local quadratic to the mean response across z levels in each causal state:

```text
W00(z) = P0 G0
W10(z) = P1 G0
W01(z) = P0 G1
W11(z) = P1 G1.
```

The quadratic is a **local benchmark**, not a biological law. At least three distinct z levels are mathematically required; the confirmatory default is five or more.

For each state the analyzer returns:

```text
quadratic coefficients
observed z range
discrete best observed z
interior concave vertex when supported
primary optimum
optimum classification.
```

If the fitted curve is not concave with a vertex inside the observed z range, the state is classified:

```text
BOUNDARY_OR_NONCONCAVE
```

and the best observed z level is used as the bounded primary optimum. Such a state cannot by itself support an interior-compromise claim.

## Experimentally identified optima

The principal experimental optima are:

```text
z_P* = z_pollinator_context = argmax W10(z)
z_G* = z_antagonist_context = argmax W01(z)
z_C* = z_combined           = argmax W11(z).
```

These are **intervention-defined state optima**. They deliberately retain consumer-independent/direct trait consequences rather than silently allocating them to a physiological `C(z)` term.

The corresponding causal shifts are:

```text
shift_remove_antagonist
  = z_P* - z_C*

shift_remove_pollinator
  = z_G* - z_C*.
```

Under a positive shared-compromise result these shifts should point in opposite directions and exceed a prospectively declared biologically meaningful displacement.

This establishes that changing functional weights moves the realized optimum. It does not require pretending that `z_P*` or `z_G*` are pure isolated-function optima.

## Component decomposition

The analyzer derives quadratic component curves algebraically:

```text
baseline(z)
  = W00(z)

pollinator_component_G0(z)
  = W10(z) - W00(z)

antagonist_component_P1(z)
  = W11(z) - W10(z)

antagonist_component_P0(z)
  = W01(z) - W00(z)

PxG_interaction(z)
  = W11(z) - W10(z) - W01(z) + W00(z).
```

At the combined optimum it reports the derivative of every component. The primary functional-conflict diagnostic compares:

```text
pollinator_component_G0 gradient
vs
antagonist_component_P1 gradient.
```

Opposite non-zero gradients are evidence that the two functions pull the shared coordinate in different directions near the combined state.

The `PxG_interaction` term remains explicit. If it is large, the consumer pathways are context-dependent and the two functional contributions should not be narrated as strictly separable.

## Critical non-tautology rule

For an interior fitted quadratic, the derivative of `W11(z)` at its own fitted vertex is zero by construction.

Therefore:

```text
W11'(z_C*) = 0
```

is **not** counted as an independent test of gradient cancellation.

The Chapter-1 balance claim instead requires convergent evidence from:

1. an interior combined optimum;
2. distinct intervention-defined state optima;
3. causal optimum shifts in opposite directions when P or G is removed;
4. opposing functional-component gradients near the combined optimum.

This avoids turning a fitted parabola into circular proof of compromise.

## Bootstrap

Uncertainty is estimated by resampling whole `plant_id` clusters.

Each bootstrap replicate:

```text
resamples plants with replacement
-> refits all four state surfaces
-> recomputes state optima
-> recomputes optimum shifts
-> recomputes component gradients.
```

The output reports 95% percentile intervals and the fraction of valid bootstrap replicates with an interior combined optimum.

A package fails closed if too few bootstrap replicates retain enough state/z coverage to fit the registered surfaces.

## Decision thresholds

Thresholds are not hard-coded. A deliberately non-runnable template is:

```text
empirical/architecture/SCH_CAUSAL_COMPROMISE_SURFACE_CONFIG_TEMPLATE_V1.json
```

Before confirmatory analysis, freeze numeric values for:

```text
min_optimum_separation
min_optimum_shift
min_abs_component_gradient
min_interior_bootstrap_fraction.
```

These define biological relevance, not merely statistical non-zero values.

## Machine decisions

### C2 — distinct state optima

The 95% bootstrap interval for

```text
z_P* - z_G*
```

must lie outside the predeclared equivalence region around zero.

### C3 — interior combined optimum

The observed `W11` surface must be concave with an interior vertex and the fraction of bootstrap fits retaining an interior combined optimum must exceed the predeclared threshold.

### C4 — opposing causal optimum shifts

The bootstrap intervals for:

```text
z_P* - z_C*
z_G* - z_C*
```

must exceed the minimum meaningful displacement in opposite directions.

### C5 — opposed functional gradients

The bootstrap intervals for the pollinator and antagonist component gradients at `z_C*` must exceed the predeclared minimum magnitude with opposite signs.

If all four pass, status is:

```text
MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE
```

Otherwise:

```text
COMPROMISE_CRITERIA_NOT_ALL_RECOVERED.
```

The word `CANDIDATE` is intentional: this first-pass analysis assumes the randomized intervention contract is valid and uses a local quadratic approximation. Confirmatory reporting must include raw cell summaries, sensitivity to alternative smoothers / bounded models, manipulation checks, and the direct-cost lane.

## Claim ceiling

A positive output licenses a contemporary causal statement that selective functional demands generate an interior reproductive optimum and move that optimum predictably when either demand is weakened.

It does **not** by itself identify:

```text
pure z_F1* or z_F2* unless direct/background costs are independently separated
construction / physiological cost by subtraction
historical origin of the shared trait
ancestral integration -> modularization
long-term response to selection.
```

Those remain separate estimands.

## Cross-chapter handoff

The default SCH -> BITA handoff is therefore:

```text
z_P* / z_pollinator_context   state-specific function-1-facing reference
z_G* / z_antagonist_context   state-specific function-2-facing reference
z_C* / z_combined             combined compromise reference
optimum separation
compromise shifts
functional gradient geometry.
```

BITA should test release toward the **identified state-specific reference** by default. Only when SCH has an independent assay that identifies `z_F1*` should BITA relabel that reference as a pure function-1 optimum.
