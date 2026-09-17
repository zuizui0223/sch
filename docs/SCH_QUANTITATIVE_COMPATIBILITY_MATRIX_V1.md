# SCH quantitative compatibility matrix V1

## Purpose

This matrix separates **estimand family**, **orientation**, numerical completeness, **uncertainty**, and **covariance** handling for the four registered strict same-coordinate conflict designs. It is a pooling gate, not a meta-analysis.

```text
REGISTERED_DESIGNS = 4
EXACT_COMPONENT_NUMERIC_DESIGNS = 2
VALID_CONTRAST_VARIANCE_DESIGNS = 0
CURRENTLY_POOLABLE_DESIGNS = 0
RANDOM_EFFECTS_GATE = FAIL_CLOSED
POOLED_CONFLICT_EFFECT = NOT_ESTIMATED
```

## Compatibility matrix

| cluster | coordinate | estimand family | orientation | numeric status | uncertainty | covariance | poolable now? | blocker |
|---|---|---|---|---|---|---|---|---|
| Dalechampia_shared_bract | upper bract area | mean-standardized selection gradient | OPPOSING_SIGNS_NUMERIC | EXACT_COMPONENT_COEFFICIENTS | COMPONENT_INTERVALS_AVAILABLE_CONTRAST_VARIANCE_MISSING | NOT_REPORTED | NO | covariance between component estimates not reported; valid contrast variance unavailable |
| Silene_petals_sexual_function | petal length | variance-standardized selection gradient | OPPOSING_SIGNS_NUMERIC | EXACT_COMPONENT_COEFFICIENTS | COMPONENT_UNCERTAINTY_MISSING | NOT_AVAILABLE_WITH_CURRENT_COMPONENT_UNCERTAINTY | NO | component SE or CI not reported in table text; valid contrast variance unavailable |
| Fragaria_inflorescence_density | inflorescence density | variance-standardized selection gradient | OPPOSING_DIRECTION_SOURCE_ADJUDICATED | NUMERIC_EXTRACTION_PENDING | SUPPLEMENT_EXTRACTION_PENDING | PENDING_TABLE_S2_EXTRACTION | NO | exact beta and CI reside in Table S2; numeric extraction and contrast uncertainty pending |
| Gymnadenia_flowering_phenology | flowering phenology | variance-standardized selection gradient | OPPOSING_DIRECTION_SOURCE_ADJUDICATED | NUMERIC_EXTRACTION_PENDING | TREATMENT_GROUP_UNCERTAINTY_AVAILABLE_CONTRAST_RECONSTRUCTION_PENDING | PENDING_MEDIATED_CONTRAST_RECONSTRUCTION | NO | Appendix A treatment-group beta plus SE require mediated-contrast reconstruction with covariance retained |

## Native within-study numbers, deliberately not pooled

| cluster | component 1 | estimate | component 2 | estimate | direct within-study contrast | native scale |
|---|---|---:|---|---:|---:|---|
| Dalechampia_shared_bract | pollinator-mediated selection | +0.6938 | seed-predator-mediated selection | -0.3093 | +1.0031 | mean-standardized selection gradient |
| Silene_petals_sexual_function | male-function selection | +0.6450 | female-function selection | -0.2670 | +0.9120 | variance-standardized selection gradient |
| Fragaria_inflorescence_density | pollinator-mediated selection | pending | herbivore-mediated selection | pending | pending | variance-standardized selection gradient |
| Gymnadenia_flowering_phenology | pollinator-mediated selection | pending | herbivore-mediated selection | pending | pending | variance-standardized selection gradient |

## Why the random-effects gate remains closed

The largest registered estimand family contains three variance-standardized selection-gradient designs, but this is not a three-study meta-analytic stratum: Silene lacks the component uncertainty needed for a valid contrast variance, Fragaria still requires exact Table S2 extraction, and Gymnadenia requires Appendix A mediated-contrast reconstruction with covariance retained. Dalechampia additionally sits on a mean-standardized rather than variance-standardized selection-gradient scale and lacks the covariance needed to propagate the difference of its two component gradients.

Therefore the current result is **quantitative incompatibility, not quantitative absence**. `RANDOM_EFFECTS_GATE = FAIL_CLOSED` is not evidence that the true cross-system effect is zero. It means the present evidence cannot support a defensible pooled effect without inventing a common scale or missing covariance.

Promotion requires at least three independent biological clusters with a common estimand family and orientation, exact effect extraction, valid uncertainty for the pooled contrast, and correct within-study covariance handling.

```text
POOLED_CONFLICT_EFFECT = NOT_ESTIMATED
NATURAL_PREVALENCE = NOT_ESTIMATED
META_ESTIMATED_CONFLICT_BUDGET = NOT_ESTIMATED
```

## Claim ceiling

The matrix diagnoses current compatibility and missing information. It does not estimate a grand conflict effect, prevalence, or bounded function-specific optima.
