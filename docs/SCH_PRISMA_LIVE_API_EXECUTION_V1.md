# SCH PRISMA live API execution v1

## Purpose

This document separates the registered scientific search protocol from the operational availability of external bibliographic APIs in GitHub Actions.

The registered query set and fail-closed scientific interpretation remain in:

```text
docs/SCH_PRISMA_SEARCH_PROTOCOL_V1.md
scripts/harvest_sch_prisma_candidates.py
```

The Actions orchestration layer is:

```text
scripts/harvest_sch_prisma_ci.py
.github/workflows/harvest-sch-prisma-identification.yml
```

## OpenAlex authentication

Current OpenAlex API documentation provides substantially larger free daily usage with a free API key and instructs scaled API users to supply:

```text
api_key=YOUR_KEY
```

The Actions workflow therefore reads an optional repository secret:

```text
OPENALEX_API_KEY
```

and passes it only through the process environment. The key is never written to an artifact or receipt.

## No-key or rate-limited execution

External API unavailability must not be confused with a scientific negative result.

If OpenAlex is unavailable, unconfigured, or rate-limited, the Actions wrapper may still retrieve available Crossref records, but its receipt must report:

```text
systematic_completion_status = PRISMA_IDENTIFICATION_BLOCKED_EXTERNAL_SOURCE
registered_source_retrieval_complete = false
```

and list a machine-readable external-source failure code.

A green Actions workflow in this condition means only:

```text
code + receipt machinery executed successfully.
```

It does **not** mean the registered two-database search is complete.

## Complete identification execution

A registered-source completeness statement requires all of:

```text
all registered OpenAlex query calls succeeded
all registered Crossref query calls succeeded
no query was truncated at its registered cap.
```

Only then can the live execution avoid the `BLOCKED_EXTERNAL_SOURCE` or `TRUNCATED` status.

## Why the registered harvester remains fail-closed

`scripts/harvest_sch_prisma_candidates.py` continues to abort on a retrieval failure. This is deliberate: it is the registered scientific harvester.

The CI wrapper catches availability failures only so that transient third-party API state does not make unrelated mechanism-development PRs appear computationally broken. It preserves the failure in the receipt and never upgrades a partial retrieval to a complete search.

## Current role in SCH

The PRISMA lane is now a secondary real-world evidence product. The main SCH Chapter-1 contribution is the causal compromise experiment. Therefore external bibliographic API availability is not a valid blocking criterion for the mechanism code, while systematic-review completeness remains independently fail-closed.
