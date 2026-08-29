# SCH PRISMA V1 identification readout

## Decision

The first registered automated identification pass ran successfully but **did not define a valid screening universe**.

Actions provenance:

```text
workflow: Harvest SCH PRISMA identification
run id:   33238145907
head:     98b62bd3fbcdf26bdb0263e7dff354281679a1b9
artifact: sch-prisma-identification-v1
```

Aggregate result:

```text
raw query/database hits:       5,406
deduplicated records:          2,684
duplicate query hits removed:  2,722
query x database combinations: 28
combinations truncated at cap: 25
status:                        PRISMA_IDENTIFICATION_TRUNCATED
```

The registered cap was 200 records per query per database.

## Why V1 failed as the screening universe

V1 used the same 14 biological queries against both OpenAlex and Crossref `query.bibliographic`.

OpenAlex reported totals ranged from 13 records for the fig-specific query to 2,050 for the broadest query. Crossref was dramatically broader because `query.bibliographic` is not a title/abstract-only ecological search coordinate. Example reported totals included:

```text
Q01 "floral scent" pollinator herbivore
  OpenAlex: 2,050
  Crossref: 35,218

Q11 "floral signal" pollinator antagonist
  OpenAlex: 346
  Crossref: 775,455

Q14 fig scent pollinator "non-pollinating wasp"
  OpenAlex: 13
  Crossref: 1,825,683
```

A successful API response therefore does not imply a successful systematic identification strategy.

## Fail-closed interpretation

The 2,684 V1 records are **not**:

- the PRISMA screening denominator;
- evidence that 2,684 biologically relevant studies exist;
- a prevalence denominator;
- a reason to begin manual screening.

The V1 artifact is retained as access/method provenance only.

## V2 correction

V2 changes the discovery architecture rather than merely increasing the cap:

1. use OpenAlex as the registered discovery source;
2. retrieve every result for each registered query up to a cap above the V1 maximum;
3. reconstruct OpenAlex title/abstract text **in memory only**;
4. require the floral-signal, pollinator and antagonist/exploiter concept blocks to all occur in title/abstract metadata before a record becomes an `UNSCREENED` candidate;
5. do not store abstract text in the repository/artifact;
6. deduplicate by DOI, then normalized title/year;
7. use Crossref only later for DOI/bibliographic metadata reconciliation, not broad discovery.

If any OpenAlex query still hits the V2 cap, V2 remains truncated and cannot become the PRISMA identification denominator.
