# SCH: simultaneous confidence sets for all five floral optima

## Ecological target

The two-flower *Pedicularis rex* experiment allocates ten eligible
parent plants in each patch × developmental-stage batch: G (predator
exposure or exclusion) is assigned to the **entire plant**, and two
distinct z settings are assigned to its two flowers. Each batch
contributes exactly two flowers from different mothers to each of the
ten G×z treatment cells.

Earlier SCH results test **different biological claims**: PR #215
identifies *descriptive sample* optimum ranks despite censored fruit
fates; PR #219 tests a Fisher sharp no-G-effect null; PR #221 tests a
much more sensitive *within-mother z-dependent G response* under a
sharp null allowing maternal additive gains. None supplies a
simultaneous population-level uncertainty set for all five
reproductive optima.

This method constructs a rigorous, though extremely conservative,
simultaneous **design-randomization expectation** interval for the
eligible enrolled cohort, NOT for every natural P. rex population.

## Assumptions necessary for genuine coverage

1. **B genuinely independently randomized patch-stage batches**;
   each has the complete ten-plant, 20-flower cyclic design. Within a
   batch the mothers, flowers and G×z cell means are **dependent**;
   only different batch assignments are assumed independent.
2. A prospective, biologically defensible, uniform integer cap K
   on **every potential** mature intact-seed outcome under all G/z
   assignments, not merely the maximum observed count or historical
   average ovule number.
3. Stable potential outcomes and no material interference between
   neighboring study mothers or manipulated flowers. The original
   SHA-256 allocation receipt **cannot authenticate** actual
   independent randomization or G selectivity.
4. The complete originally assigned cohort is accounted for.
   Unascertainable mature-seed outcomes are bounded [l_i,u_i] from
   genuinely documented flower-specific potential upper caps, rather
   than discarded or treated as zero.

The target at G,z is

    mu(G,z) = (1/B) sum_b E_randomization[X(b,G,z)],

where X is that particular patch-stage batch's **mean of its two
assigned flower outcomes** under G,z and lies in [0,K]. Different
batches may have different potential-outcome baselines. Without
representative population sampling, mu is **not** the average fitness
of every plant in the wider ecosystem.

## Exact nonasymptotic union-bound derivation

The two-sided Hoeffding bound for B independent bounded batch means
implies

    Pr(|mean(X)-mu(G,z)| > eps) <= 2 exp(-2 B eps² / K²).

A familywise union bound across all ten G×z cells gives

    Pr(any cell misses its band) <= 20 exp(-2 B eps² / K²).

Choose

    eps = K sqrt(log(20/alpha) / (2 B)).

Then with simultaneous probability at least 1-alpha, all ten target
means lie within eps of their *fully observed* randomization means.
If censoring remains, each actual realized sample mean lies in the
source-validated interval [L(G,z),U(G,z)]; thus the joint confidence
interval for mu is

    [max(0,L(G,z)-eps), min(K,U(G,z)+eps)].

**No assumption that the ten treatment cell means are independent
or that the two flowers on each plant are independent is used.**

An optimal rank is possible if its upper interval endpoint meets the
maximum of the five lower endpoints. A uniquely guaranteed optimum
rank requires its lower endpoint to exceed every other upper endpoint.
The possible EXCLUDED and EXPOSED rank sets give a confidence interval
for excluded−exposed optimal-rank difference, covering all maximizing
rank pairs on the simultaneous confidence event. A strictly positive
interval certifies a positive displacement only if every field
randomization, cap and interference assumption is valid.

## A negative but useful quantitative discovery

Reuse the previously frozen **synthetic** expected intact seed count
curves (ranks 0,1,2,3,4):

    EXCLUDED = [4,6,8,10,14]
    EXPOSED  = [5,9,11,9,6]

with *hypothetical* maximum possible seeds/flower K=25 and alpha=.05.

| Eligible plants | Independent 10-plant batches B | eps seeds/flower | Positive optimum displacement certified? |
|---:|---:|---:|---|
| 10 | 1 | 43.27, clipped | No |
| 80 | 8 | 15.30, clipped | No |
| 320 | 32 | 7.65 | No |
| 1,000 | 100 | 4.33 | No |
| 4,680 | 468 | 2.0002 | No |
| **4,690** | **469** | **1.9980** | **Yes: ideal oracle** |
| 18,720 | 1,872 | 1.0001 | Peak EXCLUDED uniquely z4, EXPOSED still z1–3 |
| **18,730** | **1,873** | **0.9998** | **Both state-specific peaks unique** |

The table assumes *oracle-perfect equality* between the observed
cell means and the hypothetical true expected means. This is **not**
a real-data estimate or a detection guarantee. At B=32, the joint
bounds leave **all five z ranks possible in both predator states**,
despite the visibly different synthetic peaks.

To incorporate actual sampling fluctuations, on the same 1-alpha
Hoeffding event each realized cell mean can differ from its expectation
by eps. Consequently its random confidence interval is contained in
a wider centered envelope [mu-2eps,mu+2eps]. If that wider envelope
certifies a positive shift, the observed interval will do so with
probability at least 1-alpha. The following are therefore more
conservative sufficient **oracle-model** calculations with *no
fruit fate censoring*:

| Desired classification | Optimistic oracle batches | Sufficient B with >=95% assignment probability, assuming the synthetic true means |
|---|---:|---:|
| Strict positive EXCLUDED-minus-EXPOSED optimum shift | 469 | **1,873** = 18,730 plants |
| Both state peaks each uniquely identified | 1,873 | **7,490** = 74,900 plants |

These very large numbers are **not instructions to sample tens of
thousands of plants**. They illustrate how uninformative a worst-case,
no-model bounded-outcome guarantee can be for a subtle phenotypic
optimum. In reality the cap K=25 might itself be too low to cover
every potential P. rex fruit; larger K increases the required sample
size quadratically.

The previous PR #218 descriptive 320-plant success scenarios and
PR #221 positive within-plant Fisher effects do **not** contradict
these results: they measure different quantities and make different
inferential claims.

## Next biologically productive step

Record real maternal, patch and flower variation in mature intact
seed production, actual prospective upper seed counts, fruit loss
and valid randomization. Then compare a **predeclared simultaneous,
variance-adaptive or biologically smooth model** with the present
worst-case bound, using synthetic null calibration and a defensible
assumption check. A sharper model can be practical, but will give up
some of this unrestricted nonasymptotic generality.

The targeted mother-internal z4-versus-z2 contrast remains a useful
*trait-conditioned predator selection* question, not a surrogate
for identifying the full five-rank argmax.

## Reproducibility

Synthetic oracle:

    python -m scripts.infer_pedicularis_simultaneous_design_peaks \
      --synthetic-oracle \
      data/SCH_P_REX_SYNTHETIC_ORACLE_SIMULTANEOUS_PEAK_V1.json \
      --output synthetic_joint_peaks.json

Future fully source-locked outcome analysis:

    python -m scripts.infer_pedicularis_simultaneous_design_peaks \
      complete_fruit_fate.csv candidate_design_receipt.json \
      --seed-cap 25 --alpha 0.05 --output joint_peaks.json

The number 25 on the latter command is ONLY an illustration; a field
study must replace it with a registered validated potential-outcome
upper cap. Source fate/original allocation checks are reused from
the existing two-flower cyclic analyzer.

Relevant theory: classical Hoeffding concentration and the Boole
union bound, e.g. J. Duchi, *Probability Bounds* notes
(https://web.stanford.edu/~jduchi/projects/probability_bounds.pdf).
Related recent methodological work: Freidling (2026),
*Randomization Inference with Concentration Inequalities*,
arXiv:2609.18586. Neither independently validates SCH's G barrier
or the original P. rex source data.

No measured P. rex optimal-rank displacement, independent G
qualification, P0/P2/W1/W2 causal chain, SCH loss L or SLK
architecture payoff is unlocked by this synthetic negative result.
