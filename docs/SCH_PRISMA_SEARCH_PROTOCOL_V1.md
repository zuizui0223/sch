# SCH PRISMA search protocol v1

## Purpose

This protocol creates a **new systematic-expansion lane** for the JBI submission target. It does not retroactively relabel the frozen BITA-derived coverage audit as systematic.

The systematic lane asks which published studies jointly measure floral attraction/display cues and the two consumer audiences needed by SCH, and it separately codes the geographical context needed to decide whether the evidence supports a Journal of Biogeography synthesis.

Version: `SCH_PRISMA_V1`

## Information sources

The automated identification pass uses two open bibliographic metadata services:

1. **OpenAlex** — broad scholarly metadata and full-text-index-assisted discovery where available;
2. **Crossref** — independent DOI/title metadata discovery.

These services are used for **identification**, not automatic scientific inclusion. Only bibliographic metadata are stored; publisher full text and reconstructed abstracts are not committed.

A later manual database supplement may add records from institutionally accessible Web of Science/Scopus or backward/forward citation chasing, but those additions must enter the same provenance ledger with a distinct `source_database`/`query_id`. They may not be silently mixed into the automated counts.

## Search date

Every Actions run records UTC retrieval time. The manuscript PRISMA flow must use a frozen release receipt, not a moving live query.

## Search concept blocks

The search deliberately avoids requiring the phrase `shared cue`, because many relevant primary studies were not framed with that terminology.

### Floral signal block

```text
floral scent
flower scent
floral odor / odour
floral volatile
floral color / colour
floral display
flower size
floral trait
floral signal
```

### Mutualist block

```text
pollinator / pollination
```

### Antagonist/exploiter block

```text
herbivore
florivore
seed predator
nectar robber
antagonist
non-pollinating wasp
```

## Registered query set

The automated V1 query registry is intentionally explicit rather than generated after results are seen.

| query_id | bibliographic search text |
|---|---|
| Q01 | `"floral scent" pollinator herbivore` |
| Q02 | `"floral scent" pollinator florivore` |
| Q03 | `"floral scent" pollinator "seed predator"` |
| Q04 | `"floral scent" pollinator "nectar robber"` |
| Q05 | `"floral volatile" pollinator herbivore` |
| Q06 | `"floral color" pollinator herbivore` |
| Q07 | `"floral colour" pollinator herbivore` |
| Q08 | `"floral display" pollinator herbivore` |
| Q09 | `"flower size" pollinator herbivore` |
| Q10 | `"floral trait" pollinator antagonist` |
| Q11 | `"floral signal" pollinator antagonist` |
| Q12 | `flower pollinator "seed predator" trait` |
| Q13 | `flower pollinator "nectar robber" trait` |
| Q14 | `fig scent pollinator "non-pollinating wasp"` |

The exact query text is version-controlled in `scripts/harvest_sch_prisma_candidates.py`; changing the query set creates a new protocol version rather than overwriting V1.

## Automated identification limits

Per query/database, the registered harvester requests a bounded number of records for reproducibility and service safety. The default cap is 200 records per query per database. If any query reaches its cap, the identification receipt marks it `TRUNCATED_AT_REGISTERED_CAP`; the systematic search is then **not complete** until that query is rerun with a predeclared expanded cap/version.

A truncated query cannot be treated as exhaustive merely because downstream screening yield is low.

## Deduplication

Records are deduplicated in this order:

1. normalized DOI when present;
2. otherwise normalized title + publication year.

The ledger retains all database/query provenance in semicolon-delimited source fields. Duplicate removal counts are generated from raw hit identity, not estimated manually.

## Identification output

The automated candidate CSV contains only bibliographic/provenance fields and blank screening fields:

```text
record_id
doi
title
year
venue
source_databases
query_ids
openalex_id
crossref_url
identification_status
screen_title_abstract
screen_title_abstract_reason
fulltext_status
screen_fulltext
screen_fulltext_reason
```

All records begin `UNSCREENED`.

## Title/abstract screening criteria

### Include for full-text screening if potentially relevant

The record must plausibly involve:

1. a flower/floral attraction, display, scent, colour, reward or related signal trait;
2. a pollinator/pollination response, service or selection component;
3. an antagonist/exploiter such as herbivore, florivore, seed predator, nectar robber, parasite/exploiter, or non-pollinating fig wasp;
4. enough primary-study information that a same-study or evolutionary-outcome lane might be evaluated.

Uncertainty is resolved toward **retain for full text**.

### Title/abstract exclusion reasons

Use exactly one primary reason:

```text
TA_NOT_FLORAL_SIGNAL
TA_NO_POLLINATOR_COMPONENT
TA_NO_ANTAGONIST_COMPONENT
TA_NOT_PRIMARY_OR_RELEVANT_SYNTHESIS
TA_NONBIOLOGICAL_OR_OFF_TOPIC
```

## Full-text screening lanes

A full text can enter more than one bounded evidence lane, but each lane has an independent claim ceiling.

### STRICT_LINKED_EXPERIMENT

Requires unchanged four-field gate:

```text
A manipulated
+ pollinator response measured
+ antagonist response measured
+ common plant reproductive outcome
```

### DIRECTIONAL_OR_NEAR_PASS

Biologically relevant but one or more strict fields missing. Missing fields and blockers are coded explicitly.

### EVOLUTIONARY_OUTCOME

Direct evidence for compromise, polymorphism maintenance, population differentiation/change, partial modularization, or historical transition. Evolutionary level and causal strength are coded separately.

### HISTORICAL_TRANSITION

Candidate for L3/L4 history. Strict L4 still requires reconstructed ancestral shared state, descendant private/separable architecture, both receiver channels, repeated transitions and alternatives.

## Full-text exclusion reasons

Primary exclusion codes:

```text
FT_NO_DECLARED_FLORAL_COORDINATE
FT_NO_POLLINATOR_EVIDENCE
FT_NO_ANTAGONIST_EVIDENCE
FT_NO_RELEVANT_OUTCOME_OR_EVOLUTIONARY_STATE
FT_REVIEW_ONLY_NO_PRIMARY_ROLE
FT_DUPLICATE_DATASET_OR_REPORT
FT_FULLTEXT_UNAVAILABLE
FT_OTHER_WITH_EXPLANATION
```

`FT_FULLTEXT_UNAVAILABLE` is preserved as a retrieval result, not treated as biological failure.

## Scientific coding fields for retained studies

The systematic screening ledger must include:

```text
A_trait
A_manipulated
pollinator_response_measured
antagonist_response_measured
common_reproductive_outcome
selection_form
cue_architecture
evolutionary_level
causal_strength
claim_ceiling
```

## JBI geography coding fields

Every full-text-retained study must also include:

```text
study_region
country_or_ocean_basin
latitude_reported
longitude_reported
spatial_grain
spatial_extent
single_site_vs_multisite
geographic_contrast
receiver_assemblage_contrast
biogeographic_context
historical_or_phylogenetic_context
```

Rules:

- use reported study geography, not author affiliation;
- do not geocode vague place names into false precision;
- `NOT_REPORTED` is a valid value;
- a study location is not itself a geographic contrast;
- `receiver_assemblage_contrast` requires evidence that pollinator/antagonist community or focal audience differs across the spatial comparison;
- a phylogeny without a spatial/historical biogeographic interpretation is not automatically a geographic contrast.

## JBI fit readout

After screening, produce a fail-closed journal-fit receipt with:

```text
strict linked experiments
multisite/spatial-contrast studies
studies with receiver-assemblage contrast
historical/phylogeographic transition candidates
number of studies supporting an analyzable geography x cue-overlap question
```

Possible decisions:

```text
JBI_SYNTHESIS_IDENTIFIED
JBI_CONCEPTUAL_FIT_ONLY
JBI_GEOGRAPHIC_EVIDENCE_INSUFFICIENT
PRISMA_NOT_COMPLETE
```

`JBI_CONCEPTUAL_FIT_ONLY` means geography is theoretically central but empirical geographic synthesis is too sparse; this should trigger reconsideration of the Ecology and Evolution fallback rather than forcing a weak geographic analysis.

## PRISMA artifacts

The final systematic package must contain:

1. query registry and search timestamp;
2. raw hit counts per database/query;
3. deduplication count;
4. identified-record candidate ledger;
5. title/abstract decisions and reasons;
6. full-text decisions and reasons;
7. final included counts by evidence lane;
8. machine-generated PRISMA flow table/diagram input.

Until title/abstract and full-text screening are complete, the flow status is `PRISMA_IDENTIFICATION_ONLY`.
