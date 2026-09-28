# SCH Pedicularis focal direct-evidence search audit v1

## Purpose

This audit records what was actually recovered for the remaining focal
`Pedicularis rex` empirical gaps and, equally importantly, what was **not**
qualified from the searched literature.

Machine ledger:

```text
empirical/architecture/PEDICULARIS_FOCAL_DIRECT_EVIDENCE_SEARCH_V1.csv
```

Audit:

```bash
python scripts/audit_pedicularis_focal_direct_evidence_search.py
```

## Current direct-gap state

```text
registered P1 supplementation effect       NOT RECOVERED
Pedicularis post-pollination attack timing  RECOVERED
P. rex post-pollination barrier validation  NOT RECOVERED
registered independent G                    NOT RECOVERED
same-flower CAL-A repeatability             NOT RECOVERED
focal >=5-level P0 manipulation             NOT RECOVERED.
```

`NOT RECOVERED` means no qualifying estimand was recovered from the searched
record set. It is not a proof that no unpublished or inaccessible dataset
exists.

## P1 — what is focal and what remains unresolved

### Wang 1998

Focal pollination biology at Zhongdian and Kunming shows that seed production
depends on bumblebee pollination.

This establishes focal pollinator dependence but does not expose a natural vs
supplemental-pollen contrast in the searchable text.

### Tang, Xie & Sun 2007

Focal natural pollination ecology and nectar reward are recovered. P. rex
subsp. rex nectar sugar was reported as 22%.

No registered pollen-supplementation contrast was recovered from the accessible
abstract/index.

### Jing, Xia, Liu & Qin 2013

The primary abstract explicitly says that reproductive outputs were measured
under **hand and natural pollination** and reports high multilocus outcrossing
in sparse and dense patches.

However, the accessible primary abstract does not specify whether the hand
treatment was:

```text
open + supplemental outcross pollen
bagged self/outcross breeding-system assay
or another hand-pollination treatment.
```

Therefore the study is deliberately classified as:

```text
FOCAL_HAND_VS_NATURAL_REPORTED_TREATMENT_IDENTITY_UNRESOLVED
```

and is not promoted to registered P1 until the primary methods are recovered.

## G — what is focal and what remains unresolved

### Xia, Sun & Liu 2013

Provides focal density-associated pollination, reproduction and predispersal
seed-predation data with a public Dryad workbook.

This is observational G baseline, not randomized predator exclusion.

### Sun & Huang 2015

Provides a real focal causal experiment with visitor and seed outcomes.

But the intervention manipulates bract water defence. It remains the wrong
SCH-G axis and is retained only as an antagonist/selectivity precedent and
BITA-y evidence.

### Sun, Armbruster & Huang 2016

Provides focal plant-level and geographic seed-predation variation linked to
floral traits.

This is conflict reality / external variance, not predator exclusion.

### Tang 2011 thesis

Later focal papers cite the thesis for predator natural history and oviposition
timing. The full text has not been ingested, so no predator-exclusion
experiment is currently verified from it.

### Menges, Waller & Gawler 1986 — P. furbishiae timing precedent

A within-genus timing experiment now narrows the G gap further. Immature
`P. furbishiae` scapes were covered with aluminum mesh and the cages were
removed before flowers opened so pollination could proceed. Previously caged
scapes later suffered the same lepidopteran seed predation as other plants, and
the authors inferred that seed-predator attack occurred after pollination.

This changes the evidence frontier:

```text
Pedicularis post-pollination attack timing      RECOVERED
P. rex barrier effectiveness/selectivity        NOT RECOVERED
P. rex timing qualification for the chosen barrier  NOT RECOVERED
registered independent G                        NOT RECOVERED
```

The precedent supports temporal plausibility only. Because the mesh was removed
before flowering, it did not test whether leaving a barrier on after pollination
would selectively exclude the predator.

## CAL-A repeatability

Sun et al. 2016 measured two different flowers from different whorls on each
plant with 0.1-mm digital-caliper precision and then averaged the two floral
measurements.

That provides instrument-resolution and biological-replicate context.

It is **not** same-flower repeatability.

## P0 manipulation

Focal observational exsertion conflict is well recovered and a congeneric
non-destructive bending/fixation manipulation is quantitatively demonstrated.

No focal P. rex experiment with >=5 realized exsertion levels plus the current
off-target checks was recovered.

## Remaining highest-value retrievals

1. Primary full methods for Jing et al. 2013 to classify the hand-pollination
   treatment exactly.
2. Tang 2011 thesis full text to check for any focal predator-access
   manipulation beyond the already recovered timing natural history.
3. A focal P. rex post-pollination barrier pilot: the literature now supports
   timing plausibility more strongly than barrier effectiveness.
4. Dryad `10.5061/dryad.6cv06/raw data.xlsx` for raw focal seed-outcome
   distributions.
5. 2016 `mcw097` supplements and Wang 1998 PDF for remaining focal context
   and any treatment details unavailable in searchable abstracts.

## Claim ceiling

This audit narrows the unresolved focal work. It does not establish that the
missing experiments do not exist elsewhere, and it does not convert
nonqualifying historical evidence into a positive SCH receipt.
