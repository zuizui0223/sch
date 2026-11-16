# SCH 2024 milkweed count-link exposure sensitivity (2026-11-16)

## Primary question

Does the source-verified 2024 *Asclepias syriaca* discrepancy between selection via **initiated fruits per whole stem** and **pollinia inserted in ten sampled flowers** survive when both outcomes are modeled as counts relative to the appropriate observable flower exposures?

Source paper: García et al. (2024), *Journal of Pollination Ecology*, DOI \`10.26786/1920-7603(2024)758\`.
Official original source Appendix II: \`https://www.pollinationecology.org/index.php/jpe/article/download/758/478\`, SHA-256 \`d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb\`.

The previous paired normalized-OLS original-source result (PR #253) estimated a stage difference on **inflorescence number** of **+0.48358**, P=0.0090, for whole-stem fruit count compared with ten-flower insertion counts. When fruits were divided by \`tot.flws=flwrs+buds\` at peak bloom, the stage difference changed to **+0.10502**, P=0.550, 95% ID-block bootstrap **[−0.2311,+0.4431]**. Those are **different response definitions**, not an identified proportion of causal mediation.

## New count-link model (sensitivity, not confirmatory identification)

Using the same verified 103 published source rows, **102 original plant labels**, including the duplicated \`plant_id=68\` source rows retained as one cluster:

\[
\log \mathrm E[F_i]
  = \log(T_i) + a_F + \sum_{k=1}^{10}\beta_{F,k}z_{i,k},
\qquad
\log \mathrm E[I_i]
  = \log(10) + a_I + \sum_{k=1}^{10}\beta_{I,k}z_{i,k}.
\]

Here \(F_i\) denotes *initiated fruits over the whole plant*, \(I_i\) denotes pollinia inserted in ten observed flowers, and \(T_i\) denotes **open flowers plus buds estimated at peak bloom**, not a true longitudinal count of compatible pollen-receiving flowers. A jointly stacked count-GLM with two stage-specific intercepts and trait slopes produces contrasts \(\beta_{F,k}-\beta_{I,k}\). It uses a **single cluster-robust sandwich covariance** across 102 original plant labels and both outcomes; individual and 10-trait joint tests are asymptotic and exploratory.

A parallel no-offset Poisson count model checks how much estimated rate-stage patterns depend on the exposure adjustment. The duplicated source ID68 rows are each excluded in a separate source sensitivity. Source outcome overdispersion and zero counts are reported; Poisson with sandwich uncertainty does **not** automatically validate the log-mean model when responses are zero-heavy.

## Status and ceilings

The actual source-count calculation is reproducibly specified in \`scripts/analyze_sch_milkweed_2024_poisson_exposure.py\`; numerical conclusions must be taken from a **successful GitHub Actions original-data run** and recorded here only after the CI receipt is inspected.

A null exposed-rate coefficient does not prove that compatible deposited pollinia fail to yield fruits; a non-null coefficient is not a causal postpollination effect. The ten sampled flowers for pollinia and the whole-stem fruit outcomes do not correspond to the same tracked flowers. Observational floral display, total peak flowers and plant resources are not independently randomized.

Neither same-trait stage slope differences nor a Poisson contrast can identify pure-function fitness optima or SCH conflict loss \(\mathcal L\). The source 137 original environmental gradient pairs and main New Phytologist Viewpoint remain unchanged.
