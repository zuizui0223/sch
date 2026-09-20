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
same-individual trait/pollination/seed linkage: 7 populations
  population IDs: 1, 3, 5, 8, 9, 10, 11
pressure-only seed outcomes after label loss: 5 populations
  population IDs: 2, 4, 6, 7, 12
population-specific trait geometry: not estimated as 12 or 14 independent coefficients
```

The primary article explicitly states that labels were lost in populations 2, 4, 6, 7 and 12, so seed production/predation there cannot be related back to individual mean floral morphology. These populations can support local antagonist pressure, not local shared-trait geometry.

Resolved supplementary objects:

```text
supp_118_2_227__index.html
supp_mcw097_aob-16074-s01.doc   66.5 KB
supp_mcw097_aob-16074-s02.xls   48.5 KB
```

Table S1 contains population location/altitude; Table S2 contains initial/final seed set and seed predation for 12 populations; Appendix S1 contains trait means/SE and pollination success for 14 populations.

Do not create 14 equal model cases from the population count alone. Even after supplement recovery, population-specific antagonist pressure is not automatically population-specific two-function geometry.

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


## Measurement-layer gate

H2 now distinguishes the highest biological quantity supported by a source from the highest quantity actually materialized as a model row.

```text
LOCAL_GEOMETRY
  both local functional routes + common outcome identify a local geometry

LOCAL_NET_SELECTION
  local realized/net trait effect is identified, but two functional components are not

LOCAL_ANTAGONIST_PRESSURE
  local antagonist intensity/outcome is identified, but local shared-trait geometry is not

CONTEXT_STRUCTURE_ONLY
  contexts are known, but local outcome values are not materialized
```

These layers are ordered by information content, not by biological importance.

A source may support a higher layer while the repository remains at a lower materialized layer until the relevant table/object is inspected.

Current examples:

```text
Gentiana focal population:
  source supported = LOCAL_GEOMETRY
  materialized     = LOCAL_GEOMETRY

Gentiana 12-population source:
  source supported = LOCAL_NET_SELECTION
  materialized     = CONTEXT_STRUCTURE_ONLY

Gymnadenia 2x2 factorial:
  source supported = LOCAL_NET_SELECTION
  materialized     = CONTEXT_STRUCTURE_ONLY

Pedicularis geographic mosaic:
  source supported = LOCAL_ANTAGONIST_PRESSURE
  materialized     = CONTEXT_STRUCTURE_ONLY

Primula farinosa programme:
  source supported = LOCAL_GEOMETRY
  materialized     = CONTEXT_STRUCTURE_ONLY

Caryopteris natural robbery:
  source supported = LOCAL_GEOMETRY
  materialized     = LOCAL_GEOMETRY

Caryopteris robber exclusion:
  source supported = LOCAL_NET_SELECTION
  materialized     = LOCAL_NET_SELECTION
```

This prevents local pressure, local net selection and local two-function geometry from being treated as interchangeable H2 observations.
