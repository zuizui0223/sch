# SCH quantitative Results/Discussion audit V1

## Purpose

This audit translates the source-adjudicated evidence structure into Results/Discussion language. It keeps literature counts, within-study quantities, theoretical identification gates, and unpooled cross-system quantities separate.

| Qualitative claim | Quantitative claim licensed | Ceiling / not licensed |
|---|---|---|
| The screened literature contains multiple evidence classes rather than one universal trade-off pattern. | The targeted evidence universe contains `16 clusters`. | This is a source-adjudicated evidence universe, not a probability sample from which natural prevalence can be estimated. |
| Direct conflict-compatible evidence exists in a minority of the screened systems. | `Five clusters` provide the strongest direct conflict signatures. | The count supports existence and recurrence inside the screened set; it is not a prevalence estimate and does not define a pooled conflict magnitude. |
| Functional weighting is often context dependent. | `Seven additional clusters` show context-dependent shifts in weighting or effective selection. | These heterogeneous shifts cannot be pooled into a single universal conflict effect without a common estimand. |
| A genuine negative class exists. | `Two clusters are aligned/no-conflict controls`. | The framework must accommodate alignment as well as conflict; multifunctionality alone cannot be interpreted as opposition. |
| Some studies are numerically strong enough for within-system analysis. | The strict numerical inventory contains `four strong same-coordinate designs`; two have exact component coefficients, zero have a valid contrast variance for the registered cross-component contrast, and zero are currently poolable. | Native within-study numbers can be displayed, but they cannot be promoted to a pooled cross-system effect. The inspectable gate is frozen in `docs/SCH_QUANTITATIVE_COMPATIBILITY_MATRIX_V1.md`. |
| The present literature does not support a defensible pooled cross-system conflict estimate. | `fewer than three independent clusters` share a compatible estimand family, orientation, uncertainty, and covariance treatment; the current compatibility matrix has `CURRENTLY_POOLABLE_DESIGNS = 0`. | `POOLED_CONFLICT_EFFECT = NOT_ESTIMATED`; this Viewpoint quantifies evidence structure and identifiability, **not a universal mean trade-off**. |
| A focal crossed experiment could estimate optima on a common trait coordinate. | Under the declared design, fitting `W00(z), W10(z), W01(z), W11(z)` across multiple trait levels can estimate `z_P*`, `z_G*`, `z_C*` and selective-removal shifts. | This is a prospective model/design prediction, not a completed empirical end-to-end result. |

## Quantitative compatibility receipt

The four-design inventory is now machine-audited from `data/SCH_CONFLICT_COMPONENT_EFFECTS_V1.csv`. Dalechampia and Silene retain their native within-study contrasts, while Fragaria Table S2 and Gymnadenia Appendix A remain extraction/reconstruction targets rather than guessed values. Missing covariance is not replaced by an independence assumption.

```text
REGISTERED_DESIGNS = 4
EXACT_COMPONENT_NUMERIC_DESIGNS = 2
VALID_CONTRAST_VARIANCE_DESIGNS = 0
CURRENTLY_POOLABLE_DESIGNS = 0
RANDOM_EFFECTS_GATE = FAIL_CLOSED
```

This fail-closed state is not evidence that the cross-system conflict effect is zero. It records that a common estimand with valid uncertainty and covariance handling is not yet available in at least three independent clusters.

## Discussion ceiling

```text
POOLED_CONFLICT_EFFECT = NOT_ESTIMATED
NATURAL_PREVALENCE = NOT_ESTIMATED
META_ESTIMATED_OPTIMUM_SEPARATION = NOT_ESTIMATED
META_ESTIMATED_CONFLICT_BUDGET = NOT_ESTIMATED
PURE_FUNCTION_OPTIMUM_DISTRIBUTION = NOT_ESTIMATED
```

Results may therefore state that direct conflict, context dependence, and aligned/no-conflict outcomes all occur in the source-adjudicated literature. Discussion may use this heterogeneity to motivate stronger same-coordinate experiments, but may not convert the `16/5/7/2` structure into natural frequencies or manufacture a pooled effect from incompatible estimands.
