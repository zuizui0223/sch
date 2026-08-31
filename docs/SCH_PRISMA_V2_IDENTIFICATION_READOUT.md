# SCH PRISMA V2 identification readout

## Decision

The registered V2 OpenAlex identification pass is **complete on its declared search coordinate** and can serve as the title/abstract screening denominator.

Actions provenance:

```text
workflow: Harvest SCH PRISMA identification V2
run id:   33238702090
head:     06621da843ddc9b013030134e9689b11f0d7adf1
artifact: sch-prisma-identification-v2
artifact id: 9710707247
artifact sha256: 70fbe6d28d577082a35c35f2a8d7bf0b8cf47706d7a4f117c047c884099af89f
```

Aggregate result:

```text
OpenAlex records fully retrieved across 14 queries: 10,953
query-hits passing the registered title/abstract concept filter: 2,107
query-hits failing the concept filter: 8,846
duplicate concept-pass query-hits removed: 1,239
deduplicated UNSCREENED candidates: 868
queries truncated at cap 2,500: 0
stored reconstructed abstracts: NO
Crossref used for V2 discovery: NO
status: PRISMA_V2_IDENTIFICATION_COMPLETE
```

`COMPLETE` applies only to the registered OpenAlex identification coordinate. It does not mean title/abstract screening, full-text screening, inclusion, prevalence estimation or JBI geographic-fit coding is complete.

## Query-level retrieval

| query | OpenAlex total/retrieved | concept-pass hits |
|---|---:|---:|
| Q01 | 2,050 / 2,050 | 288 |
| Q02 | 263 / 263 | 97 |
| Q03 | 236 / 236 | 66 |
| Q04 | 193 / 193 | 60 |
| Q05 | 1,385 / 1,385 | 230 |
| Q06 | 375 / 375 | 63 |
| Q07 | 298 / 298 | 51 |
| Q08 | 1,078 / 1,078 | 231 |
| Q09 | 1,023 / 1,023 | 186 |
| Q10 | 1,297 / 1,297 | 315 |
| Q11 | 346 / 346 | 91 |
| Q12 | 1,677 / 1,677 | 219 |
| Q13 | 719 / 719 | 208 |
| Q14 | 13 / 13 | 2 |

The sum of concept-pass hits is intentionally larger than 868 because the same publication can be retrieved by several registered queries.

## Known-anchor sensitivity check

Before using the 868-record ledger as a screening denominator, the V2 candidate set was checked against the eight source-adjudicated anchors already frozen in `evidence/EVIDENCE_ROLE_REGISTRY_V1.csv`.

| anchor | DOI | V2 recovery |
|---|---|---|
| Sasidharan et al. 2023 | `10.1093/aob/mcad064` | RECOVERED |
| Theis & Adler 2012 | `10.1890/11-0825.1` | RECOVERED |
| Page et al. 2014 | `10.1371/journal.pone.0098755` | RECOVERED |
| Junker & Blüthgen 2010 | `10.1093/aob/mcq045` | RECOVERED |
| Knauer et al. 2018 | `10.1038/s41467-018-03792-x` | RECOVERED |
| Kessler et al. 2015 | `10.7554/eLife.07641` | RECOVERED |
| Pérez-Barrales et al. 2013 | `10.1111/j.1600-0706.2013.20780.x` | RECOVERED |
| Theis et al. 2014 | `10.3732/ajb.1400171` | RECOVERED |

```text
known anchors recovered: 8 / 8
```

This is a positive-control sensitivity check, not an estimate of search recall for unknown relevant studies.

## Relationship to V1

V1 returned 5,406 query/database hits and 2,684 deduplicated records but was truncated in 25 of 28 query × database combinations, primarily because Crossref `query.bibliographic` was far broader than the intended ecological title/abstract coordinate. V1 remains provenance for a rejected search implementation and is not added to the PRISMA screening denominator.

V2 therefore supplies the first valid automated identification denominator:

```text
identified for title/abstract screening = 868
```

## Next gate

Screen all 868 records under the frozen V1 screening reasons, resolving uncertainty toward full-text retention. Every record retains its identification provenance. After title/abstract screening, full-text decisions must add the scientific evidence lane and JBI geography fields before any prevalence or biogeographic synthesis claim is allowed.
