# SCH PRISMA V13 — Batch-2 full-text closure

## Machine-audited cumulative state

```text
frozen denominator:                    868
title/abstract screened:               208
retained for full text:                130
title/abstract excluded:                78
TA unscreened:                         660

reports sought for retrieval:          130
reports not retrieved:                   1
reports assessed for eligibility:      129
primary studies included:               53
assessed full-text exclusions:          76
formal EXCLUDE decisions:               77
current full-text undecided:             0

STRICT_LINKED_EXPERIMENT:                2
DIRECTIONAL_OR_NEAR_PASS:               46
EVOLUTIONARY_OUTCOME:                   15

positive geographic records:           11
positive receiver records:              11
joint geography + receiver records:     10
obvious independent joint systems:    <= 9
```

`FT_FULLTEXT_UNAVAILABLE` is now separated from reports assessed for eligibility. `SCHPRISMA-000194` is the single not-retrieved report; it is a formal retrieval/exclusion state, not a biological full-text failure.

## Scientific update

V13 closes the 35-report queue opened by V12 with nine inclusions, twenty-five assessed exclusions and one not-retrieved report. No new strict experiment is admitted. The strict linked measurement architecture therefore remains two studies, and the positive dual-audience chain remains unrecovered.

Two additions sharpen lower evidence layers. Junker & Blüthgen 2010 places opposite receiver responses on the same synthetic scent coordinate: bumblebees are attracted and ants are repelled, but there is no common plant reproductive outcome. Kleinschmidt et al. 2023 adds a two-population *Lithophragma bolanderi*–*Greya* coevolutionary mosaic with floral morphology, pollinator-community turnover, local pollination efficacy and oviposition differences, but `A` is observational.

The raw JBI counters rise to 10 joint-positive records. `SCHPRISMA-000167` and `SCHPRISMA-000523` are the same *Primula farinosa* research program, so record count is not independent-system count; the obvious current upper bound is nine independent biological systems pending the full independence audit.

## Provenance boundary

`decision_source` is provenance for an individual versioned sparse overlay. It is not a cumulative history field. V12 retains its 70 title/abstract provenance rows and V13 retains its 35 full-text provenance rows; a merged latest-state view may show the V13 source for records adjudicated at both stages and must not be used to reconstruct stage history.

No pooled effect is authorized by Batch-2 closure alone.
