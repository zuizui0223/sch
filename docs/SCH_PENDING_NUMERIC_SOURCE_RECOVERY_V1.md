# SCH pending numeric source recovery V1

## Decision

```text
SOURCE_ROUTE_RESOLVED_EXTRACTION_FAIL_CLOSED
Fragaria_inflorescence_density = NUMERIC_EXTRACTION_PENDING
Gymnadenia_flowering_phenology = NUMERIC_EXTRACTION_PENDING
RANDOM_EFFECTS_GATE = FAIL_CLOSED
POOLED_CONFLICT_EFFECT = NOT_ESTIMATED
```

Both remaining strict same-coordinate designs have a specific source object identified. In addition, the Fragaria supporting-information download route has been resolved to the published Oxford Academic CDN object, and the Gymnadenia Ecological Archives object has been resolved at the archive level. Neither result is the same as having materialized and inspected the source table bytes.

## Fragaria vesca

```text
cluster:                Fragaria_inflorescence_density
DOI:                    10.1002/evl3.262
source object:          Table S2
source file:            evl3262-sup-0001-suppmat.docx
published analysis:     emtrends differences in beta
download route status:  SIGNED_OUP_CDN_ROUTE_RESOLVED
binary materialized:    false
numeric promotion:      BLOCKED_UNTIL_SOURCE_TABLE_BYTES_ARE_INSPECTED
```

Oxford Academic exposes the article's supporting-information link, and that link resolves to the signed CDN object named `evl3262-sup-0001-suppmat.docx`. The article states that Table S2 contains the exact treatment combinations used for the selection-gradient contrasts and that differences in beta were calculated with `emtrends`.

The current execution environment still has not materialized the DOCX bytes for table-level inspection. **do not digitize Figure 1 as if it were Table S2.** Plot reading would replace a published coefficient table with a lower-precision reconstruction and would not recover the uncertainty or covariance needed by the registered pooling gate.

## Gymnadenia conopsea

```text
cluster:                Gymnadenia_flowering_phenology
DOI:                    10.1890/14-0119.1
source object:          Appendix A Table A2
archive:                Ecological Archives E096-022
archive object:         E096-022-A1
archive route status:   ECOLOGICAL_ARCHIVES_OBJECT_RESOLVED
reported content:       phenotypic linear selection gradients (beta +/- SE) for all four treatment groups
binary materialized:    false
numeric promotion:      BLOCKED_UNTIL_SOURCE_TABLE_BYTES_ARE_INSPECTED
```

The Ecological Archives record identifies Appendix A Table A2 as the table containing the linear selection gradients and standard errors for all four experimental treatment groups. This is the correct object for reconstructing the mediated phenology contrasts. The archive object is resolved, but the table bytes have not been materialized in the present execution environment.

Even when the four beta +/- SE entries are recovered, **do not infer missing covariance**. A difference of treatment-specific gradients needs a valid variance for the registered contrast; marginal standard errors alone do not license an independence assumption.

## Provenance state is not numeric state

```text
SOURCE_LOCATIONS_CONFIRMED = 2
DOWNLOAD_ROUTES_RESOLVED = 1
BINARY_MATERIALIZATIONS_COMPLETED = 0
EXACT_NUMERIC_EXTRACTIONS_COMPLETED = 0
```

Resolving a web route is useful provenance, but it does not promote a biological coefficient. No numeric field in `SCH_CONFLICT_COMPONENT_EFFECTS_V1.csv` changes in this step.

## Promotion gate

A pending design can move from `NUMERIC_EXTRACTION_PENDING` only when all relevant items below are source-verified:

1. the exact coefficient or treatment-specific coefficients defining the registered contrast;
2. the effect-scale definition and orientation;
3. uncertainty for the target contrast or enough source information to derive it validly;
4. covariance information when the contrast combines estimates from the same experiment, or an explicitly justified design-based alternative;
5. the resulting contrast is commensurable with an already registered estimand family.

Until then, the compatibility state remains:

```text
REGISTERED_DESIGNS = 4
EXACT_COMPONENT_NUMERIC_DESIGNS = 2
VALID_CONTRAST_VARIANCE_DESIGNS = 0
CURRENTLY_POOLABLE_DESIGNS = 0
RANDOM_EFFECTS_GATE = FAIL_CLOSED
```

This is a provenance result, not evidence that the underlying biological effects are absent or zero.
