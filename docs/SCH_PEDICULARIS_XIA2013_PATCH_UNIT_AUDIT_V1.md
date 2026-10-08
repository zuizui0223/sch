# Xia et al. (2013): patch-level inference and ecological context reversal

## Biological question

**Does the enemy side of a multifunctional conflict reorganize across patch
density and size, and can that reorganization be hidden in final seed output?**

Xia, Sun & Liu (2013), *Biology Letters*, doi:10.1098/rsbl.2013.0387,
is a compelling **observational motivation** for the question in *Pedicularis
rex*. It is not yet a patch-replicated estimate of a changed floral optimum.

This audit re-reads the primary Methods, Results and Tables 1–2 instead of
promoting reported F statistics directly into robust ecological effect sizes.

## What the focal data actually contain

The 2011 study sampled:

- 11 spatial patches: five sparse, six dense;
- 58 sampled spikes: 26 sparse, 32 dense;
- numerous nested fruits/capsules scored for seed traits.

Patch density and patch size are **patch-level attributes**. In contrast,
the published two-way ANOVA tests report:

| 2011 density × patch-size interaction | F | reported df |
|---|---:|---:|
| Fruit set | 3.060 | 1,54 |
| Initial seed set | 44.556 | 1,2047 |
| Final seed set | 0.023 | 1,2345 |
| Fruit predation | 10.605 | 1,54 |
| Seed predation | 106.270 | 1,2345 |

These are original paper statistics, not newly fitted model results.
The thousands of capsule-level denominator degrees of freedom are **not
thousands of independent patches**. The original Methods describe two-way
ANOVAs, not an explicit patch-random-intercept model.

The risk is pseudoreplication for a patch-level interaction: individual
capsules may be numerous while the environmental contrast has only 11
spatial replicates. The high F values may remain persuasive under an
appropriate hierarchical analysis, but that has **not** been shown by the
currently recovered primary material.

The earlier 2005 density comparison contains one sparse and one dense patch,
so it cannot independently replicate the patch-level density contrast in
that year either.

## The ecologically interesting pattern

The authors report a **sign reversal in the patch-size association with seed
predation**:

```text
sparse patches:
  small > large in seed predation

dense patches:
  large > small in seed predation.
```

This is biologically more discriminating than saying only "enemy pressure
varies." A context-independent, monotone patch-size effect cannot by itself
explain both observed directions. Possible mechanisms include local enemy
aggregation, dilution/satiation, or patch-network placement, but none is
identified from these observational contrasts alone.

The manuscript also reports density × size interactions in initial seed set
and seed predation but not in final seed set. This is an important **difference
among reported response-specific tests**, not proof that two significant
components cancelled or that the final interaction is equivalent to zero.
Their residual variances, data subsets and observational grains differ.

## A nontrivial reproductive mechanism to test

Let each *matched capsule* have:

```text
I = (intact seeds + damaged seeds) / ovules
q = damaged seeds / (intact seeds + damaged seeds)
F = intact seeds / ovules = I (1 - q).
```

For any fixed patch-context group, with q defined for the included capsules,

```text
E[F] = E[I] (1 - E[q]) - Cov(I, q).
```

The final term is a biologically important **success–risk coupling**.
If capsules with high initial reproductive output are preferentially
attacked, positive covariance reduces the realized output below the
prediction based on average predation alone. If predation concentrates on
initially low-output capsules, negative covariance can raise output relative
to that mean-only prediction.

Synthetic illustration, NOT P. rex observations:

| Two capsules | Initial I | Predation q | Mean final F |
|---|---|---|---|
| Positive coupling | 0.2, 0.8 | 0.0, 0.5 | 0.30 |
| Negative coupling | 0.2, 0.8 | 0.5, 0.0 | 0.45 |

Both examples have mean initial seed fraction 0.5 and mean predation 0.25.
The realized mean changes because the covariance changes. This is why the
missing raw-data linkage is potentially biologically informative, rather
than merely a variance-estimation detail.

A related 2016 P. rex paper reports pollen receipt and seed-predation risk
associated at the plant level. That **does not demonstrate** the capsule-level
`Cov(I, q)` in the 2013 data. The distinction should stay explicit.

## What to do if the Dryad workbook is obtained

The exact public file identity is already pinned in the repository:

```text
doi:10.5061/dryad.6cv06
dataset 11150 / version 11193 / file 46101
raw data.xlsx
size 89,597 bytes
MD5 10a98383677bbd2a01e19a86c350fdd3.
```

The binary remains unavailable via anonymous download in the current
retrieval environment; do not fabricate its contents.

After a legitimate download and checksum validation:

1. identify the data grain (patch → plant/spike → capsule) and check whether
   initial, final, ovules, and predation share the same capsule identifier;
2. reproduce the reported descriptive density/size means and their units;
3. estimate density × size on independently replicated patch contexts,
   using patch-level summaries and hierarchical models; with only 11 patches,
   report uncertainty and leave-one-patch-out sensitivity rather than relying
   on large-capsule asymptotic degrees of freedom;
4. calculate `Cov(I,q)` within each patch/context only where pairs really match,
   and check how the mean and covariance terms contribute to final seed set;
5. test whether the sign reversal in the patch-size effect survives
   patch-respecting uncertainty. A retained reversal is a local
   antagonist-context result, **not** an identified displacement of the
   floral-exsertion optimum.

No causal density or patch-size effect can be inferred merely by refitting
the observational data.

## SCH interpretation boundary

**Recoverable now**: reported observational patch-size direction reversal in
seed predation; the contrast among reported initial, predation and final
seed-set ANOVAs; a concrete hypothesis for covariance-mediated integration.

**Not recovered**: a patch-level robust interaction CI, a demonstrated
compensatory process, exsertion-dependent enemy selection within those 11
patches, causal G intervention, or changed reproductive trait optima.

These local observations can motivate a future experiment that randomizes
predator removal and floral exsertion **within independently replicated
patch contexts**. That is a biological test of when enemy pressure displaces
the floral optimum, beyond the focal same-population causal identification
study. It must not be smuggled into the registered primary P2 outcome worlds
after results have been observed.

Machine audit:

```text
data/PEDICULARIS_XIA2013_PATCH_UNIT_AUDIT_V1.csv
scripts/audit_pedicularis_xia2013_patch_units.py
tests/test_pedicularis_xia2013_patch_units.py
```

Run `python scripts/audit_pedicularis_xia2013_patch_units.py`.
