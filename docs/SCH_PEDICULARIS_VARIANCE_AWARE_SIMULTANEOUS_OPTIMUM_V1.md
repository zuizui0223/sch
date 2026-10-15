# SCH: variance-aware simultaneous rank inference for Pedicularis rex

## Biological question and scope

Does excluding seed predators change the best floral-exsertion setting across **all five** prospectively assigned z ranks when intact viable mature seeds per flower are the response? Rejecting a sharp no-predator-effect Fisher null or finding a z4-versus-z2 response is **not** proof that the full five-rank optimum moved.

This is a non-gating, source-locked companion to SCH_PEDICULARIS_FIVE_RANK_SIMULTANEOUS_OPTIMUM_CONFIDENCE_V1.md. **No newly randomized P. rex field data exist here.** Results below come from fully synthetic examples, not measurements, population sample-size requirements, estimated field power or an SCH/SLK architecture result.

## Preserved source structure

One independent patch-stage batch is ten DISTINCT mothers and twenty assigned flowers, with two different plants contributing to each G-by-z cell. Predator treatment G is assigned to WHOLE MOTHER PLANTS. Reuse the existing fruit-fate receipt: exact counts, source-verified zeros, partially censored outcomes and unobserved maturity remain lower/upper seed intervals; no unknown count is imputed as zero.

For each of 20 within-G unordered pairs of z ranks a,b, the source-valid batch difference lies within [L_b,U_b], where L_b=cell_lower(a)-cell_upper(b) and U_b=cell_upper(a)-cell_lower(b). A prospectively established GLOBAL physical intact-seed cap K must bound ALL eligible potential outcomes, not only the observed maximum or a historical mean ovule count. Each contrast endpoint is in [-K,K].

For B>=2 independent batches, use the unbiased between-batch variance (B-1 denominator), computed separately for lower and upper endpoints. The Maurer-Pontil one-sided empirical Bernstein radius for bounded independent batch contrasts is:

    r(x) = sqrt(2 * s² * log(2/delta) / B)
           + 7 * (2K) * log(2/delta) / (3 * (B-1)).

For the 20 lower and 20 upper endpoints, set delta=alpha/40. The simultaneous interval for each mean difference is:

    [mean(L)-r(L), mean(U)+r(U)] intersect [-K,K].

The 40 protected one-sided inequalities give conditional joint coverage at least 1-alpha. A candidate rank is removed only when a competitor is strictly better throughout its simultaneous band. The resulting two sets of possible G-specific optimal ranks bound the optimal exsertion shift (EXCLUDED minus EXPOSED).

The covered target is the **average of enrolled independent-patch assignment expectations**. Population transport requires representative sampling, target comparability, real randomization and absence of interference. Dependence between flowers and G-by-z cells WITHIN patch is allowed; flowers are not independent replicates.

The new nominal-95% empirical Bernstein and existing nominal-95% Hoeffding outputs are strictly ALTERNATIVE procedures. Intersecting two independent 95% interval families without splitting alpha has no justified joint 95% guarantee.

Methodological reference: Maurer A, Pontil M (2009), Empirical Bernstein Bounds and Sample Variance Penalization, arXiv:0907.3740, Theorem 11 (bounded independent observations and one-sided tails).

## Synthetic method-efficiency comparison

Invented fully observed, identical-patch seed response means: predator EXCLUDED = [5,7,10,14,19] with unique z4 maximum; predator EXPOSED = [5,8,13,8,5] with unique z2 maximum. Set K=40 and alpha=.05. Each peak exceeds its nearest competitor by five intact seeds per flower.

| Independent synthetic patches | Synthetic mothers | Hoeffding radius | Empirical Bernstein radius (variance zero) | Full z maxima certified? |
|---:|---:|---:|---:|---|
| 32 | 320 | 25.85 | 44.43 | neither |
| 100 | 1,000 | 14.63 | 13.91 | neither |
| 276 | 2,760 | 8.80 | 5.008 | neither |
| **277** | **2,770** | **8.79** | **4.990** | empirical Bernstein only |
| 855 | 8,550 | 5.002 | 1.613 | empirical Bernstein only |
| **856** | **8,560** | **4.999** | **1.611** | both |

277 versus 856 is a SYNTHETIC NOISELESS MATHEMATICAL DETECTABILITY THRESHOLD, not empirical recruitment advice, a field power estimate or evidence of actual P. rex selection. For small numbers of patches or substantial trait-specific patch heterogeneity, empirical Bernstein can be wider than Hoeffding; unknown fruit fates can also eliminate the rank-shift certificate.

### Ecological design implication

When patch productivity is an additive shared baseline for all exsertion ranks, the paired rank difference removes that baseline: patch-level absolute fitness may vary while within-patch trait contrast variance remains small. Preserve source-linked paired G-by-z responses within each independent patch, rather than pooling unpaired flowers across heterogeneous locations. If patch environment modifies the trait-specific response, this cancellation fails; the method will use the increased contrast variance.

This is a design implication, not observed seed-predator-mediated natural selection.

## Tests and inferential ceiling

The implementation uses the existing frozen flower/fate CSV and allocation receipt, preserves G treatment and z assignment identity, prevents reusing a patch under another stage, requires the precommitted cap and retains missing mature seed intervals. Tests cover all 40 endpoints, unbiased variance, null shift, heterogeneity, missing-fate sensitivity and explicit source tampering.

Unverified: water state, physical z manipulation, seed-predator exclusion selectivity, pollen-mediated fitness, fruit maturity follow-up, no interference and a valid globally precommitted field K. Even if a true G-dependent reproductive optimum shift were confirmed, it would not by itself identify pure pollination-versus-antagonist function optima, SCH conflict loss L, or SLK architecture value.
