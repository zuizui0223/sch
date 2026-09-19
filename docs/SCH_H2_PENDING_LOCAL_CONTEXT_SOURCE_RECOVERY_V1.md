# SCH H2 pending local-context source recovery V1

## Decision

```text
H2_LOCAL_CONTEXT_EXTRACTION = FAIL_CLOSED
GENTIANA_S3_ROUTE = RESOLVED_BINARY_NOT_MATERIALIZED
GYMNADENIA_A2_ROUTE = RESOLVED_BINARY_NOT_MATERIALIZED
PEDICULARIS_POPULATION_SUPPLEMENT = IDENTIFIED_EXTRACTION_PENDING
PRIMULA_POPULATION_EXPERIMENT_TABLES = PROGRAMME_SOURCE_EXTRACTION_PENDING
```

A context structure is not promoted to local model cases until the source object containing the local outcome is inspected.

## Gentiana lutea

Canonical axis:

`Gentiana_lutea_color_axis`

Primary broad source:

- Sobral et al. 2015, PLOS ONE
- DOI: `10.1371/journal.pone.0132522`

Published supporting object:

```text
S3 Table
Population traits and coefficients of selection on flower color
DOI object: 10.1371/journal.pone.0132522.s004
format: DOC
route: PLOS supporting-information file endpoint
binary materialized in repo workflow: false
```

The article establishes that flower-colour effects on pollinator visitation differ among populations, while the colour × population interaction for escape from seed predation is not supported. Population-specific selection coefficients are explicitly delegated to S3 Table.

Do not reconstruct the S3 coefficients from Fig. 4.

## Gymnadenia conopsea

Canonical axes:

- `Gymnadenia_000030_phenology`
- `Gymnadenia_000030_spur_length`

Source object:

```text
Ecological Archives E096-022
Appendix A Table A2
reported content: treatment-group selection gradients beta +/- SE
local factorial cells: 4
binary materialized: false
```

The 2 × 2 design structure is known, but treatment-specific H2 cases remain blocked until the table bytes are inspected.

## Pedicularis rex

Canonical axis:

`Pedicularis_000376_corolla_exsertion`

Source programme:

- Sun, Armbruster & Huang 2016
- DOI: `10.1093/aob/mcw097`

Source structure:

```text
floral / pollen information: 14 populations
seed predation / seed production: 12 populations
supplement contains population/locality tables
local component geometry extraction: pending
```

Do not create 14 equal model cases from the population count alone.

## Primula farinosa

Canonical axis:

`Primula_farinosa_000523_scape`

The programme spans a broad population survey plus smaller experimental subsets and long-term follow-up.

The correct H2 unit is the source-specific population × manipulation × time observation, not all populations in the programme.

Population subset identities, treatment assignment and local selection/morph-frequency outcomes must be recovered from the individual primary sources before materialization.

## Promotion gate

A local context case can be promoted only when all of the following are source-resolved:

1. canonical trait axis;
2. local context identity;
3. context timing or treatment state when applicable;
4. function-1 direction/effect for that local context, or an explicit local null;
5. function-2 direction/effect for that local context, or an explicit local null;
6. common outcome / geometry basis;
7. source provenance.

Until then:

```text
reported context count != H2 model N
```
