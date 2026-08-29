# SCH PRISMA search protocol v2

## Purpose

V2 replaces the overbroad V1 discovery implementation while preserving the same biological question and 14 registered query IDs. It creates the candidate universe for title/abstract screening; it does not perform scientific inclusion.

Version: `SCH_PRISMA_V2`

## Why a new version is necessary

V1 combined OpenAlex and Crossref broad bibliographic discovery. Twenty-five of 28 query × database combinations hit the 200-record cap, and Crossref returned bibliographic totals as high as 1.8 million for a fig-specific query. The V1 result is therefore `PRISMA_IDENTIFICATION_TRUNCATED` and is not used as a screening denominator.

V2 changes the retrieval coordinate rather than post hoc deleting inconvenient V1 records.

## Discovery source

**OpenAlex only** for automated discovery.

The same V1 query strings remain frozen:

| query_id | query |
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

## Retrieval cap

V2 retrieves up to **2,500 OpenAlex records per query**. This is above the largest V1 OpenAlex reported total (2,050).

If any query reports more records than are retrieved at this cap:

```text
status = PRISMA_V2_IDENTIFICATION_TRUNCATED
```

and the candidate universe is not declared complete.

## Registered title/abstract concept filter

OpenAlex abstracts are reconstructed transiently from `abstract_inverted_index` for filtering only and are never written to output.

A retrieved record becomes an `UNSCREENED` V2 candidate only when its title + abstract metadata contain all three concept blocks.

### Floral-signal block

At least one of:

```text
floral
flower / flowers
blossom
fig / syconium
```

### Pollinator block

At least one of:

```text
pollinat*
flower visitor*
floral visitor*
```

### Antagonist/exploiter block

At least one of:

```text
herbiv*
floriv*
seed predator / seed-eating / seed eater
nectar robber / robbing / thief / thieving
antagon*
non-pollinating
parasitoid / parasite
exploit*
oviposit*
```

This filter is deliberately broad enough to retain near-pass and evolutionary studies. It does **not** require an A manipulation, reproductive outcome, or same-study paired response; those remain human full-text coding decisions.

## Missing abstract handling

A record without an OpenAlex abstract may still pass if its **title alone** contains all three registered concept blocks.

A record failing the concept filter is not a biological exclusion decision. It is outside the V2 bibliographic title/abstract search coordinate and is counted as `AUTOMATED_CONCEPT_FILTER_FAIL` in the identification receipt.

## Stored candidate fields

Only bibliographic/provenance and blank screening fields are stored:

```text
record_id
doi
title
year
venue
query_ids
openalex_id
identification_status
screen_title_abstract
screen_title_abstract_reason
fulltext_status
screen_fulltext
screen_fulltext_reason
...
JBI geography fields
```

No reconstructed abstract or publisher full text is saved.

## Abstract-free machine screening assistance

Before human title/abstract adjudication, a separate assistance packet may be generated for a frozen screening batch. The packet refetches each OpenAlex work, reconstructs the abstract only in memory, and records only:

```text
which registered concept blocks occur in the title
which registered concept blocks occur in the abstract
matched registered term strings
OpenAlex work type
known-anchor status
machine review priority
```

The abstract itself is not stored.

Machine review priority has **no PRISMA decision meaning**. It is used only to order human review:

```text
KNOWN_ANCHOR
HIGH_TITLE_TRIPLE
HIGH_TITLE_PAIR
MEDIUM_TITLE_ONE
ABSTRACT_ONLY
```

The assistance packet contains separate blank fields for any later formal decision, but the generator is prohibited from populating them. It therefore cannot increment screened, excluded, retained or included counts.

Known frozen anchors are promoted only as sensitivity controls so that a screening packet can be checked against studies already known to be biologically relevant. Their presence never auto-includes them in the systematic review.

## Formal screening audit

The deterministic batch workspace is audited independently of the machine-assistance packet. Only the registered formal fields in `SCH_PRISMA_V2_SCREEN_BATCH_*.csv` can change PRISMA counts.

Allowed title/abstract decisions are:

```text
RETAIN_FULLTEXT
EXCLUDE + exactly one registered TA exclusion reason
blank = UNSCREENED
```

`UNSCREENED` is never interpreted as exclusion. Full-text fields are rejected unless the record first passed title/abstract screening as `RETAIN_FULLTEXT`. Included full texts must be available and carry at least one registered evidence lane.

The screening audit regenerates title/abstract, full-text, evidence-lane and geography counts from the batch files. Completion of screening does **not** by itself authorize a pooled effect; outcome-scale compatibility and independence remain separate gates.

## Deduplication

1. normalized DOI;
2. otherwise normalized title + year.

All query IDs contributing the same record are retained.

## Crossref role after V2 discovery

Crossref may be used later to reconcile DOI/title/year/venue metadata for the deduplicated OpenAlex candidates. It is **not** part of the V2 discovery denominator and may not add new records silently.

Any records added by backward/forward citation chasing or manually accessible databases enter a separately labelled identification lane and are incorporated into the final PRISMA diagram with explicit provenance.

## V2 completion states

```text
PRISMA_V2_IDENTIFICATION_COMPLETE
PRISMA_V2_IDENTIFICATION_TRUNCATED
PRISMA_V2_RETRIEVAL_FAILED
```

`COMPLETE` means the registered OpenAlex queries were fully retrieved and the predeclared concept filter/deduplication completed. It does **not** mean title/abstract or full-text screening is complete.

## Next gate

Only a `PRISMA_V2_IDENTIFICATION_COMPLETE` candidate ledger proceeds to human title/abstract screening under `SCH_PRISMA_SEARCH_PROTOCOL_V1.md` exclusion codes and the unchanged SCH scientific admission rules. Machine triage may order that work but cannot replace the human decision fields.
