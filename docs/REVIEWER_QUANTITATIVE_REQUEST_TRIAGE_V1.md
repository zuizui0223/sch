# SCH reviewer quantitative request triage V1

## Purpose

This document classifies likely reviewer requests by whether they improve estimand compatibility or evidence adjudication. `DO_NOW` means the request can strengthen the present Viewpoint without inventing a common effect size; `DO_IF_REQUESTED` means it is useful only if a reviewer challenges classification robustness; `DECLINE` means the requested analysis would pool incompatible quantities or misread the screened evidence universe as a prevalence sample.

| Reviewer request | Decision | Quantitative value gained | Trigger / boundary |
|---|---|---|---|
| Add an explicit compatibility matrix for the strongest numerical studies. | `DO_NOW` | Makes the pooling gate inspectable by listing estimand family, orientation, uncertainty, and covariance availability for the `four strong same-coordinate designs`. | The matrix should explain why compatibility fails; it must not manufacture a common scale. |
| Show within-study numerical estimates side by side without pooling. | `DO_NOW` | Preserves useful quantitative information while keeping native estimands distinct. | Display native units or clearly defined standardized quantities only when the transformation is biologically valid. |
| Run classification sensitivity with a second-adjudicator check. | `DO_IF_REQUESTED` | Tests whether the assignment to direct conflict, context-dependent, aligned/no-conflict, and other evidence classes is stable to independent adjudication. | Use if a reviewer challenges coding subjectivity; this is a robustness check on evidence classification, not a new prevalence estimator. |
| Repeat the classification under one prospectively stated alternative threshold. | `DO_IF_REQUESTED` | Quantifies whether borderline systems drive the qualitative evidence pattern. | Keep the alternative rule biologically interpretable and frozen before reclassification; do not search thresholds for a desired result. |
| Compute a pooled conflict effect from the current heterogeneous numerical studies. | `DECLINE` | No defensible gain because the current set lacks a common estimand, orientation, uncertainty, and covariance structure. | `POOLED_CONFLICT_EFFECT = NOT_ESTIMATED`; the paper quantifies evidence structure, **not a universal mean trade-off**. |
| convert 16/5/7/2 into prevalence of conflict, context dependence, or alignment in nature. | `DECLINE` | None: the targeted source-adjudicated universe is not a probability sample. | `NATURAL_PREVALENCE = NOT_ESTIMATED`; proportions inside the screened set are descriptive only. |
| Add more examples simply to raise n until a meta-analysis threshold is reached. | `DECLINE` | Sample count alone does not create estimand compatibility. | New studies matter only if they add independent, compatible quantitative information under the registered gate. |
| Meta-estimate a conflict budget from directional gradients, treatment contrasts, and optimum separations together. | `DECLINE` | These quantities are not interchangeable measurements of one latent scalar without an explicit measurement model. | `META_ESTIMATED_CONFLICT_BUDGET = NOT_ESTIMATED`. |

## Revision rule

Prefer transparency about compatibility over forced synthesis. A reviewer request for “more quantitative analysis” should be translated first into the estimand being requested. If the requested quantity does not have a common measurement scale across the evidence set, the correct quantitative response is a compatibility matrix, within-study display, or fail-closed bound—not a pooled mean.

```text
POOLED_CONFLICT_EFFECT = NOT_ESTIMATED
NATURAL_PREVALENCE = NOT_ESTIMATED
META_ESTIMATED_CONFLICT_BUDGET = NOT_ESTIMATED
```

The active Viewpoint remains a quantitative identification framework and source-adjudicated evidence synthesis, **not a universal mean trade-off** estimate.
