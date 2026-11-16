# SCH: a properly normalized zero-truncated NB2 test of milkweed fruit-count selection (2026-11-17)

## Source-verified quantitative result

The original published García et al. (2024), *Journal of Pollination Ecology*, DOI **10.26786/1920-7603(2024)758**, Appendix II source XLSX has **103 authentic rows, 102 distinct source plant labels**, one duplicated ID 68. Publisher source binary is exactly **38,955 bytes, SHA256 d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb**. The source was recovered from this repository's previous signed original-source GitHub Actions artifact rather than re-scraping a publisher endpoint that temporarily returned HTTP 500. The analysis specifically targets the **63 fruit-positive rows (62 source plant labels)**, with all ten original standardized predictors and the source peak-flower opportunity \(T_i=\mathrm{open\ flowers}+\mathrm{buds}\).

The previous PR #255 found a nominal negative association between **inflorescence number** and fruit count *per peak flower* in the 63 positive fruit records. However, it fit an **ordinary NB2 GLM after deleting all zero-fruit outcomes**, an invalid likelihood for a deliberately zero-truncated outcome. This source audit implements the mathematically correct conditional probability instead:

\[
 \Pr(F_i=y\mid F_i>0,\boldsymbol z_i,T_i)
 = \frac{\operatorname{NB2}(y;\mu_i,\alpha)}{
 1-\operatorname{NB2}(0;\mu_i,\alpha)},\qquad y=1,2,\ldots,
\quad \log\mu_i=\log T_i+\beta_0+\sum_{k=1}^{10}\beta_k z_{ik}.
\]

The source fixed dispersion \(\alpha=0.43988\) is derived from the entire 103-row sample's source Poisson residual moment diagnostic and is **NOT claimed to be jointly estimated by the 63-row truncated likelihood**. Analytical scores were checked against numerical finite differences; expected-information Fisher scoring refines the nonlinear source optimizer and a sandwich estimator groups both source rows with duplicated ID 68 under the same plant label.

### Comparison: positive counts versus per-opportunity positive rates

| Model on the original 63 fruit-positive source rows | Focal inflorescence-number coefficient | Robust nominal P | 95% source-label cluster confidence interval |
|---|---:|---:|---|
| Ordinary **non-truncated** NB2 on positive rows only; fruit count per peak flower (PR #255) | **−0.32906** | **0.000269** | [−0.50607,−0.15204] |
| Properly **zero-truncated** NB2, whole-stem positive fruit counts, **no flower offset** | **+0.06224** | **0.60152** | [−0.17136,+0.29583] |
| Properly **zero-truncated** NB2, positive fruit counts with peak-flower exposure offset | **−0.30104** | **0.01139** | **[−0.53421,−0.06787]** |

**What is genuinely new:** Correctly accounting for source zero truncation reduces the apparent strength of the negative statistical evidence (P≈0.00027 → **0.0114**) but does **not** remove the negative association from the original positive-only per-peak-flower model. A **different target**, the whole-stem number of fruits among the same positive stems, has no detected focal association. This divergence is driven materially by exposure normalization and the selected fruit-positive subgroup; it does not imply that plants biologically allocate fewer resources to each flower when they have more inflorescences.

The proper likelihood's original focal estimate changes to \(e^{-0.30104}\approx0.740\) on the latent *untruncated* mean fruit rate per +1 SD of inflorescence number, under the model. It does **not** directly equal the change in *observed conditional positive* mean, which is \(\mu/(1-P_0)\) and varies with intercept and plant exposure.

### Fixed alpha grid and duplicate-label source sensitivity

An explicitly prespecified grid of NB2 fixed alpha values \(\{0.25,0.5,1,2\}\) gives proper truncated per-peak-flower log-coefficients approximately **−0.306, −0.300, −0.294, −0.288** and nominal two-sided cluster-robust P values **0.0071, 0.0128, 0.0241, 0.0403**. This direction survives different dispersion *working assumptions*, but **all are nominal exploratory P values over ten simultaneous source traits**; none is evidence of familywise support under 0.05/10 = **0.005**.

The source ambiguity \`plant_id=68\` was handled without inventing an original correction. Excluding either source row separately gives the proper zero-truncated, peak-flower-offset focal slope **−0.29845** (P=.0123) or **−0.30077** (P=.0118). The 62 labelled positive source plants are not independently genotyped or a random sample of the world's milkweed.

### Important reliability boundary: the direct source-ID bootstrap is unstable

A 199-replicate bootstrap resampled the **62 labelled positive plants**, keeping duplicate ID68 together. Only **101/199** optimized replicates met the pre-specified analytic score criterion, while **98/199** failed it. The simulation failure source receipt records **98 unsettled optimizer gradients**, not a missing source workbook or failed probability normalization. Consequently **NO bootstrap percentile 95% interval is reported** for this model: the resulting 101 fits must not be treated as an unbiased or automatically representative subset of all resamples.

The full-source properly truncated point model, fixed-alpha grid and both original ID68 exclusions had converged source analytic scores. Its cluster sandwich 95% interval is conditional on fixed NB2 alpha and correctly specified zero-truncated mean form, *without* dispersion-parameter uncertainty. The bootstrap instability raises a substantial warning about high-dimensional positive-only inference with only 63 source rows and ten correlated traits, even though the optimized original source estimate itself is numerically well-defined.

### Why the result is not biological proof of a trade-off

1. **Selection on a post-outcome subset.** Only stems with \(F>0\) contribute to the count component. Conditioning on fruit presence can select on plant condition, phenology, unobserved visitors and resource state. A true two-part hurdle representation needs a full coherent zero model and properly normalized conditional count; the separate whole-sample any-fruit logistic models from PR #255 are observational associations, and no direct flower-level transition was tracked.
2. **Outcome denominator and exposure link.** Peak count of open flowers plus buds is mathematically related to inflorescence number and inflorescence size. Adding \(\log T_i\) as an offset models per-peak-flower fruit **rate** rather than whole-stem fruit **count**. The negative coefficient appears in the former but not the latter, so it cannot be interpreted as causal reproductive allocation.
3. **Source fitness stage mismatch.** The 2024 pollinia-insertion endpoint consists of events in ten sampled flowers, while fruits were initiated across the whole plant. The original source does not follow the actual compatible inserted pollinium through fertilization, abortion and mature fruit fate on a named flower. No per-flower reproductive conversion probability exists in this table.
4. **Inference and multiplicity.** The fixed-alpha source likelihood is not equivalent to a dispersion-profiled joint maximum-likelihood model. The 63 source positive records are one biological programme, not 63 independent experiments. Robust P=.0114 does not survive the ten-trait familywise threshold 0.005; no original genetic effects or causal optima are recovered.

### Source and reproducibility contract

Script \`scripts/analyze_sch_milkweed_2024_zero_truncated_nb.py\` implements and separately tests the *actual* zero-truncated NB2 log-likelihood and analytic score. The source model result, fixed-alpha grid and complete-case/ID68 validity are saved as a JSON in the \`SCH original 2024 milkweed proper zero-truncated NB2\` GitHub Action. Original source bytes are checked against the publisher SHA256 before modeling. The directly inspectable source-derived comparison is recorded in \`data/SCH_MILKWEED_2024_ZERO_TRUNCATED_NB_SENSITIVITY_V1.csv\`.

This is an original **real public-data source reanalysis**, not a new field collection, and it does not enlarge the previous 137 treatment-gradient pairs or 572-original-row master dataset. **SCH pure-function optima and compromise loss \(L\) remain unidentified.**

**Current claim ceiling:** properly source-normalized count likelihood retains a negative *conditional and denominator-dependent association*, **not** confirmed independent evolutionary conflict or a causal resource allocation effect; direct bootstrap interval is unavailable due to failed original source resample convergence.
