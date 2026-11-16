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

## New original-data quantitative results — CI source verified

The exact official 2024 source XLSX was ingested, decoded and fitted with **103 original source rows / 102 observed plant labels** in [GitHub Actions #43892182850](https://github.com/zuizui0223/sch/actions/runs/43892182850). Both stages use the same ten original standardized plant traits and are estimated in a **joint stacked Poisson model** with robust standard errors clustered by original plant label (including both records bearing ID 68). A *no-offset* model acts as a direct count-denominator negative control.

| Inflorescence number: fruits − pollinium insertions in log-rate slopes | No exposure offset | Offsets log(peak flowers) for fruits and log(10) for sampled insertions |
|---|---:|---:|
| Original source estimated log slope difference | **+0.45862** | **+0.08315** |
| 102-label-cluster robust SE | 0.17606 | 0.17432 |
| Asymptotic two-sided normal P | **0.00919** | **0.63335** |
| Source cluster-robust 95% CI | [+0.11354,+0.80370] | **[−0.25852,+0.42482]** |
| Ten-trait joint Wald χ²(10) | 15.976 | 10.819 |
| Ten-trait joint P | 0.1003 | **0.3718** |
| Ten individual traits passing exploratory Bonferroni P<0.005 | **0/10** | **0/10** |

Leaving out the first original ID 68 record gives exposure-offset inflorescence slope difference **+0.10191, P=0.56079**; leaving out the second gives **+0.09930, P=0.57192**. This guards against silently treating the two differently observed fruit counts with the same identifier as two independent genetic plants.

The fitted Poisson-mean model has residual Pearson dispersion diagnostics of **2.27 for fruit count** and **2.58 for pollinia insertion count** after exposure offsets, illustrating extra-Poisson variability. Plant-label clustered sandwich SEs are used rather than uncorrected Poisson model SEs; these do not guarantee that the conditional log-mean function is fully correct. A zero-inflated or negative binomial sensitivity would be useful for future independent confirmation but cannot, by itself, make the unmatched sampled-flower risk sets identical.

### Scientific consequence

Two statistical families now agree directionally on a **measurement-denominator sensitivity**:

- Paired relative-fitness OLS: source original stage contrast **+0.48358, P=0.0090**, after exposure-normalized proxy **+0.10502, P=0.5502**.
- Original count-link Poisson: source original contrast **+0.45862, P=0.0092**, after flower-opportunity offsets **+0.08315, P=0.6334**.

Because the *outcome* and hence the biological estimand changes when we normalize by flower exposure, this is **not a causal decomposition nor evidence that 82% of natural selection is caused by counting bias**. It establishes that the nominal positive focal gradient difference is not robust across defensible observed opportunity definitions. In particular, source peaks of open flowers and buds are only snapshots, while inserted pollinia refer to ten selected flowers; no observed marked-flower-level transition \(P(\mathrm{fruit}\mid\mathrm{compatible\ pollen\ inserted})\) can be identified from these aggregate columns.

The original ten-trait source model result values are in \`data/SCH_MILKWEED_2024_GENUINE_POISSON_STAGE_EXPOSURE_RESULTS_V1.csv\`; full statistics, source quality checks and the original source appendix are retained in artifact **#14236463601** (ZIP SHA-256 \`d1c31bdfa73f20c06256e3e7b670383105abb14f9c4df0d43c9e02584f6d565c\`).

## Status and ceilings

The actual source-count calculation is reproducibly specified in \`scripts/analyze_sch_milkweed_2024_poisson_exposure.py\`; numerical conclusions must be taken from a **successful GitHub Actions original-data run** and recorded here only after the CI receipt is inspected.

A null exposed-rate coefficient does not prove that compatible deposited pollinia fail to yield fruits; a non-null coefficient is not a causal postpollination effect. The ten sampled flowers for pollinia and the whole-stem fruit outcomes do not correspond to the same tracked flowers. Observational floral display, total peak flowers and plant resources are not independently randomized.

Neither same-trait stage slope differences nor a Poisson contrast can identify pure-function fitness optima or SCH conflict loss \(\mathcal L\). The source 137 original environmental gradient pairs and main New Phytologist Viewpoint remain unchanged.
