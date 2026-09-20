# SCH H2 pending local-context source recovery V1

## Decision

```text
H2_LOCAL_CONTEXT_EXTRACTION = FAIL_CLOSED
GENTIANA_S3_ROUTE = RESOLVED_BINARY_NOT_MATERIALIZED
GYMNADENIA_A2_ROUTE = TABLE_VALUES_EXTRACTED
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
exact table values extracted from source HTML: true
```

All eight treatment-cell net-selection cases are now materialized for phenology and spur length. Mediated contrast point estimates are also recorded, but their contrast SE/covariance is not supplied in Table A2, so covariance-aware local agent geometry remains blocked.

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

The primary article states that plant labels were lost in populations 2, 4, 6, 7 and 12. Those populations can support population-level antagonist pressure but cannot be related back to individual floral morphology.

Resolved supplementary object identities:

```text
Pedicularis_S1
  supp_mcw097_aob-16074-s01.doc
  population location / altitude

Pedicularis_S2
  supp_mcw097_aob-16074-s02.xls
  initial/final seed set + seed predation for 12 populations

Pedicularis_AppendixS1
  supp_118_2_227__index.html
  trait means / SE + pollination success for 14 populations
```

Do not create 14 equal model cases from the population count alone. Local antagonist pressure is not equivalent to local two-function trait geometry.

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

H2 now separates two parallel information layers.

### Plant-performance layer

```text
LOCAL_GEOMETRY
  both local functional routes + common outcome resolve a local geometry

LOCAL_NET_SELECTION
  local realized/net trait effect is resolved,
  but the two functional components are not

LOCAL_ANTAGONIST_PRESSURE
  local antagonist intensity/outcome is resolved,
  but local trait geometry is not

CONTEXT_STRUCTURE_ONLY
  local contexts are known,
  but outcome values have not been materialized
```

### Visitor-role behavior layer

Blueberry and sesame provide fully source-resolved local contexts for visitor tactics, but do not provide a local plant-fitness geometry for those manipulations.

Those cases are retained as:

```text
ROLE_BEHAVIOR_CONTEXT
```

and remain separate from the ordered plant-performance measurement layer.

Current reconciliation:

```text
total H2 local cases                         18
plant-performance cases                      11
visitor-role behavior cases                   7

plant-performance LOCAL_GEOMETRY              2
plant-performance LOCAL_NET_SELECTION         9
plant-performance LOCAL_ANTAGONIST_PRESSURE   0
```

The seven role-behavior cases come from blueberry cultivar morphology and sesame corolla/resource manipulations. They are real H2 local cases, but they do not count as plant-performance geometry cases.

## Source-object registry

Pending plant-performance promotions are registered in:

`data/SCH_H2_LOCAL_CONTEXT_SOURCE_OBJECTS_V1.csv`

Current registered objects:

```text
Gentiana_S3
  DOI object 10.1371/journal.pone.0132522.s004
  target = LOCAL_NET_SELECTION

Gymnadenia_A2
  Ecological Archives E096-022-A1
  target = LOCAL_NET_SELECTION

Pedicularis_S1
Pedicularis_S2
Pedicularis_AppendixS1
  target = context structure / local antagonist pressure

Primula_program_sources
  target = LOCAL_GEOMETRY
```

At the current runtime state:

```text
registered source objects                 6
binary objects materialized               0
exact local values extracted              1
```

Pending objects therefore do not create pseudo-cases.

## Revised promotion rule

A plant-performance local case is promoted only when all required local quantities for its declared measurement layer are source-resolved.

A role-behavior local case may be promoted without a local reproductive endpoint only when the source directly resolves the visitor-role contrast. Such a case remains explicitly outside plant-fitness geometry.

Therefore:

```text
reported context count
!=
plant-performance model N
!=
visitor-role behavior case count
```
