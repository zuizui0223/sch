# One-trait shared-cue coverage protocol v1

## Question

This audit asks whether the committed evidence base contains an experiment that can support the original one-trait question without importing the canonical paper's two-trait estimand.

The strict coverage gate is:

```text
one focal attraction/display trait A is manipulated
+ the pollinator response to that same A contrast is measured
+ the antagonist response to that same A contrast is measured
+ a common plant reproductive outcome is measured in the linked experiment
```

`D`, an `A x D` interaction, a 16-cell design, selective consumer exclusion, and an independent joint-cost assay are **not** required for this coverage gate. Those requirements belong to the canonical two-trait mechanism-allocation problem.

## Estimand boundary

For a one-trait contrast, the general accounting identity is

```text
Delta_A W = Delta_A M - Delta_A G - Delta_A C.
```

If direct attraction cost is standardized away or measured independently, the biotic balance may be defined as

```text
S_A = Delta_A M - Delta_A G.
```

This simplification is not automatic. Observation of total `W(A)` alone does not allocate `M`, `G`, and `C`. Channel allocation still needs selective interventions or defensible channel-specific measurements. The one-trait problem is therefore **less demanding than the two-trait cross-curvature problem**, not identification-free.

## Source universe

The audit starts from a frozen export of BITA's canonical generated route table:

- `data/source_exports/BITA_TABLE_S3_MECHANISM_PATTERN_LEDGER.csv`

The export commit, declared UTF-8/LF normalization and canonical SHA-256 values are recorded in `data/source_exports/SOURCE_EXPORT_MANIFEST.json`. The builder fails closed if either frozen input drifts.

It groups records by `independence_cluster`, never by effect row. All clusters containing an `A_to_pollination` or `A_to_antagonism` route require an explicit source adjudication in `ONE_TRAIT_SOURCE_ADJUDICATION_V1.csv`. A new A-route cluster therefore fails closed until its manipulation, linkage and reproductive-outcome fields are adjudicated.

The separate 16-system identification matrix is re-screened only as a comparison. It was assembled to approach the two-trait identification target and is not assumed to be a complete one-trait source universe.

## Verdicts

- `PASS_DIRECTIONAL_ONLY`: the source-reported design passes the four coverage fields, but available committed/public data do not support a new uncertainty-bearing estimate.
- `FAIL`: at least one declared field fails.
- `NOT_EVALUABLE_NO_A_ROUTE`: the cluster is outside the current one-trait A-route candidate set.

A coverage pass establishes existence of a relevant design in the screened evidence base. It is not a meta-analytic effect, a prevalence estimate, proof of shared-cue evolution, or point identification of `Delta_A M` and `Delta_A G`.
