# Pedicularis rex: geographic heterogeneity may enter when interactions become reproductive fitness

## Biological question

Must the geographic mosaic of floral selection in *Pedicularis rex* mean
that pollinators or seed predators change their **trait preferences** among
populations? Or can a common trait-response pattern yield different final
reproductive consequences because the biological conversion from pollen and
attack to surviving seeds changes with local context?

The second mechanism matters for SCH: heterogeneity in realized conflict
does not imply different functional optima or different animal preferences.

**Source**: Sun, Armbruster & Huang (2016), *Annals of Botany* 118:227–237,
doi:10.1093/aob/mcw097, original **Table 1 and Model 1–4 interpretation**.
The source reports observational within-population/plant-level trait–response
fits, not randomized exsertion. This readout is an original-table model-support
audit, not a refit to raw pollen/seed records.

## Actual source data: how the four stages differ

| Response | Best listed AICc | Model with population × response/trait term AICc | ΔAICc | Table-derived relative likelihood |
|---|---:|---:|---:|---:|
| Stigma pollen receipt (14 populations) | 1700.10 | 1714.83 | 14.73 | 0.000633 |
| Seed predation (7 linked populations) | −156.11 | −151.03 | 5.08 | 0.078866 |
| Initial seed set (14 populations) | −493.44 | −480.30 | 13.14 | 0.001402 |

All three reported **best models** omit the shown population × trait or
pollen-response interaction, while retaining additive population variation.

**Different observation:** final viable seed production (7 linked populations)
has a published *best interactive model* AICc = **−1000.03** and a more
complex full model AICc = **−971.091**. Its selected model contains
population-specific interactions involving initial seed set, predation,
exsertion and their combinations.

**Critical statistical boundary:** both final-seed models shown in Table 1
contain population interactions. Their ΔAICc of **28.939** favors the
*particular reduced interactive candidate*, **not** an interactive model
over a no-interaction baseline. The paper explains that its interaction
model beat the no-interaction alternative, but does not list the latter's
AICc in Table 1. We cannot calculate that unreported contrast.

The original article prose also gives approximate relative-likelihood
figures (0.0068, 0.3450, 0.0120) that do **not** equal
`exp(-ΔAICc/2)` using its printed Table 1 AICc contrasts
(0.000633, 0.078866, 0.001402). This reproducible arithmetic discrepancy
does not overturn the ranking of any of the listed candidates; it does mean
the prose ratios should not be reused as if directly derived from Table 1.
The calculation is machine-checked in
`scripts/audit_pedicularis_2016_selection_model_support.py`.

**Crucial scope:** 14 populations contributed the published pollen-receipt
and initial-seed fits; only seven individually linked populations
(1, 3, 5, 8, 9, 10, 11) contributed predation and final-seed fits.
Population numbers or model AICc cannot be pooled across endpoints. Failure
to select a population × exsertion effect is **not** statistical proof
of identical consumer-preference slopes across populations.

## Two distinct ecological mechanisms

### H1 — context-dependent enemy preference

The response of early seed-predator oviposition to exsertion changes
among populations or patches. If this is true, randomized exsertion
within each independently replicated local context should reveal
different **attack-risk slopes** at a valid common predator-exposure
reference, even when initial reproductive potential and bract water are
matched.

The source 2016 selected predation model does not require such an
interaction among its seven linked populations, but the sample/selection
procedure cannot rule it out. The 2013 patch-size/density study supplies
context-specific *mean* predation, not a local exsertion-response estimate.

### H2 — context-dependent fitness translation (distinct prediction)

Predator attack–trait relationships may be similar, yet their impact on
surviving seed production differs because *seed initiation, baseline
predation, attack-induced survival, and/or capsule-level success–risk
covariance* vary among local contexts.

For an individual capsule with **distinguishable initiated seeds**
(`I > 0`), define `I` = (intact + damaged seeds) / ovules,
`q` = damaged / (intact + damaged seeds), and
`F` = intact seeds / ovules. If all relevant damaged seeds are counted:

```
F = I (1 - q)

E[F | context, z, G]
  = E[I] * (1 - E[q]) - Cov(I, q).
```

This is an algebraic identity, **not evidence** that covariance differs
in the 2016 data. Similar `q` slopes need not imply similar final
fitness gradients, because `I` and its association with `q` may differ.

The 2013 paper separately reports density × patch-size interactions
in initial seed set and predation but no detected interaction in final
seed set. The 11 patches and their nested capsules make the printed
large-denominator ANOVA significance inappropriate as a robust
patch-level causal answer. Compensation/covariance remains a prediction,
not an established explanation of the apparently weak final interaction.

## Experimental discrimination, using the existing two-cohort bridge

The *separate pollen sentinel cohort* can map randomized marginal pollen
receipt `M(z)`. The *intact fruit cohort*, already registered on the
same physical z grid with independent predator G and water-y fixed,
can also record the **three distinct seed fractions** on each matched
fruit-bearing flower:

- initiated/distinguishable seed fraction `I`;
- predation among identifiable initiated seeds `q`;
- final intact viable seed fraction `F`.

For each `z × G` cell, quantify the three terms in the identity and
compare component profiles, preserving plant/patch clustering and
fruit-fate/censoring records. Decomposing a mean response is not enough
to identify causal mediation or animal preferences, but it is more
biologically informative than comparing only the final `F` maxima.

**Fail closed on seed ambiguity:** a fruit with intact = damaged = 0
may have initiated zero seeds or lost all distinguishable tissues. Its
`q` is undefined under these raw columns, so it cannot silently be
excluded from covariance estimation or arbitrarily assigned `q=1`.
Keep its observed final intact seed count for the fitness profile and
report the decomposition as not identified until flower-fate data
resolve it. The existing Xia2013 patch-unit audit already enforces
this measurement distinction.

New field comparisons must pre-freeze cohort sampling and evaluate
interference: predator barriers on one flower may displace enemy
attack onto others, and fruit resources can be reallocated among
sibling flowers.

## What this observation changes for SCH

The original biological claim can be sharpened from

> predator selection varies in space, so shared-flower conflict varies

to a more discriminating *testable explanation*:

> Even when the floral trait–consumer response is approximately portable
> across populations, **its reproductive consequences need not be**.
> Spatially varying seed initiation, predator pressure and coupling
> between them may create a mosaic of realized fitness constraints.

This is still an **alternative mechanism** rather than a verified causal
process. No original 2016 raw linked flower–seed dataset, 2013 Dryad
workbook, or new focal `z × G` field experiment was obtained in this
audit. Table 1 AICc values are real published aggregate results; any
numerical demonstration using arbitrary raw flowers must be labeled
synthetic.

## Machine files

```text
data/PEDICULARIS_2016_SELECTION_MODEL_AICC_V1.csv
scripts/audit_pedicularis_2016_selection_model_support.py
tests/test_pedicularis_2016_selection_model_support.py
```

Run `python scripts/audit_pedicularis_2016_selection_model_support.py`.
This produces source-comparison receipts and deliberately reports
`hypothesis_directly_identified_by_table_only = false`.

Related: `SCH_PEDICULARIS_XIA2013_PATCH_UNIT_AUDIT_V1.md`,
`SCH_PEDICULARIS_TWO_COHORT_ECOLOGICAL_ALIGNMENT_V1.md`.
