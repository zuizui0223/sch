# How many P. rex plants are needed for the two-flower experiment?

## The question must be divided in two

The new cyclic fruit experiment assigns only **two flowers per plant**
across five physical floral exsertion settings and two predator G states.
Within each patch × flower-stage batch it requires ten plants, each
having two eligible flowers. Five plants are assigned to each G arm,
and within an arm the z-pairs follow a connected five-edge cycle.
Therefore **each z×G cell receives two flowers from distinct plants
per ten-plant batch**. The G manipulation is between plants.

This has two entirely different practical unknowns:

1. **Plant supply:** How many plants must be screened to recruit
   enough plants with two suitable flowers?
2. **Biological detectability:** After enrolling those plants,
   how often can an analysis distinguish a predator-induced shift
   in the finite-grid *intact mature seed count* optimum, given
   plant-level variance and loss of maturity outcomes?

Neither may be inferred solely from mean published mature
capsules per plant. The 2016 Sun, Armbruster & Huang paper
(DOI 10.1093/aob/mcw097) reports a mean 12.51 ± 5.60 SD
mature capsules per sampled plant. That is **not** the
fraction of plants with two stage-matched flowers and
does **not** measure viable seed-count variance or
the treatment-response variance needed for this study.

## Part I: hypothetical plant eligibility and screening

Let p be the **assumed probability** that an independently
screened plant in a precommitted patch-stage stratum
has two eligible flowers. For s screened plants, the
number eligible has binomial distribution Binomial(s,p)
under the *additional unverified* independent eligibility
assumption.

To recruit ten eligible plants in one stratum with
probability at least 95%, the minimum s values are:

| Assumed p(two eligible flowers) | Screened plants per stratum | Required eligible plants |
|---:|---:|---:|
| 0.30 | 49 | 10 |
| 0.50 | 28 | 10 |
| 0.80 | 16 | 10 |

These are **conditional sample-supply calculations**,
not field-estimated eligibility probabilities.

For B independently recruited patch-stage strata,
the chance all B can fill is
[P(Binomial(s,p) ≥ 10)]^B. Therefore the 95% *joint*
screening count **per stratum increases with B**.
For example, at p=0.50:

| Number of strata B | Required eligible plants | Screened per stratum | Total screened |
|---:|---:|---:|---:|
| 1 | 10 | 28 | 28 |
| 4 | 40 | 32 | 128 |
| 16 | 160 | 35 | 560 |
| 32 | 320 | 37 | 1184 |

These values require that plants and stratum eligibility
events be independent and share the same p. In reality,
flower production can be spatially correlated and vary
by season, plant size, developmental stage and patch.
A real **treatment-blind eligibility census** is needed
before the numbers can inform recruitment.

A positive pilot eligibility rate is not evidence that
eligible plants are representative of the overall
population, or that plant treatment interference is absent.

## Part II: scenario-specific optimum shift detectability

The new analysis script
`scripts/simulate_pedicularis_two_flower_detectability.py`
calls the **actual frozen design algorithm** for each
synthetic replicate rather than treating 20 fruit flowers
as independently assigned to ten treatment cells.

One synthetic mother plant contributes **two** flowers,
sharing a maternal effect; G is assigned once per plant.
Each patch-stage batch receives a common environmental
effect, and flowers receive additional independent noise.

The synthetic plant-specific seed count is:

    Y = round_clip(mu[G,z] + patch_effect
                   + maternal_plant_effect + flower_residual,
                   0, prospective_seed_cap)

The patch, maternal and flower effects are independent
zero-mean Gaussian **illustrative generator choices**,
not verified reproductive biology of P. rex. They
are specified in seed-count units, and nothing in
this source justifies interpreting them as
measured standard deviations.

The included scenario set (each profile lists mean
seed counts at assigned z ranks 0–4):

- **Low-variance, complete maturity:**
  EXCLUDED [4,6,8,10,14], EXPOSED [5,9,11,9,6],
  patch SD 1, plant SD 2, flower SD 2.
- **High maternal heterogeneity:** same profiles,
  plant SD 6 instead of 2, no missing outcomes.
- **5% MCAR maturity loss:** low-variance profile,
  but unknown fruits contribute [0,25] viable seeds,
  not an imputed zero.
- **Outcome-dependent maturity loss:** an illustrative
  baseline 12% missing rate modified so low intact
  seed counts are more likely to be unobserved.
- **No true optimum displacement (null):**
  the two G states have the SAME profile
  [5,9,11,9,6]. Positive shifts that occur
  purely because of simulated noise here are
  **descriptive false signals**, NOT an estimated
  statistical Type I error for a formal test.

The output compares, over independent synthetic
assignments, three fractions:

1. Positive optimum shift on simulated fully
   observed (latent) seed counts.
2. **Guaranteed positive shift** when unknown
   maturity outcomes retain their prospective
   [0,25] seed-count intervals.
3. Guaranteed positive shift that survives
   deleting every one parent plant's entire
   two-flower assignment block.

Each numerator is a count of synthetic data
realizations satisfying a finite-grid statement.
**These are NOT nominal-α hypothesis tests or
calibrated frequentist power.** The fraction
cannot be used to promise 80% "power" for
a Nature/Am Nat ecological claim. Nor does
a plant-delete-stable sample replace a
plant-level randomization-based confidence
interval.

The default configuration explores 10, 20, 40,
80, 160 and 320 eligible enrolled plants, with
two fruit flowers per plant and 2, 4, 8, 16,
32 and 64 fruit observations per z×G cell.
All source profiles, variances, missingness
mechanisms, seed cap and the Monte Carlo seed
are frozen in a synthetic JSON input.

## The crucial ecological limit: more plants may NOT rescue unobserved fruits

If the fraction m of flowers whose maturity output
remains entirely unobserved does not decrease
with sample size, and each missing fruit contributes
a worst-case [0,K] intact seed interval, the bound
on a z×G mean is asymptotically (in an idealized
uniform-MCAR model):

    [(1-m)*mu(z,G),
     (1-m)*mu(z,G) + m*K].

The **width m*K does not shrink** with the
number of plants. Better recruitment reduces
sampling variation but cannot make adversarial
missing seed counts become observed.

For an optimum at a rank with true mean mu*
to remain guaranteed above a competitor
with mean mu*−Delta under this uniform m
assumption, the necessary strict inequality is

    (1-m)*Delta > m*K
    i.e.  m < Delta/(K+Delta).

**Illustrative comparison:**
if the true gap is 4 intact seeds per flower
and potential seed cap K=25, that
*pairwise unique-optimum* requirement is
m less than 4/29 = 13.8%. With m=15%,
it is impossible to guarantee that
pairwise ordering using only these
worst-case maturity intervals, however
many synthetic plants are recruited.

This is a deterministic missing-information
bound under the stated uniform-fate model,
not a claimed 13.8% threshold for P. rex.
The required m for just **the direction of
optimum shift** can differ from the rate
needed to identify both optima uniquely;
the script computes whole-grid possible
optimum sets. Under outcome-dependent
missingness, the uniform-MCAR limiting
formula is an *illustrative comparison only*,
not the true limiting rate.

Thus this project must invest in **pre-dispersal
maturity tracking** and defensible
per-flower seed caps, not only more plants.

## Key missing biological calibrations before a defensible n

- A treatment-blind field census of two
  eligible flowers per plant by patch/stage.
- A small separately qualified G exclusion
  and physical z pilot, including G spillover
  across plants and unintended z effects.
- **Plant**, flower and patch variance of
  intact mature seed counts in real P. rex.
- Source-specific rates and mechanisms of
  unobservable mature fruit fate, including
  total seed destruction.
- The expected minimum meaningful **optimum
  gap** between adjacent physical z settings
  (not just a presumed direction of the peak).
- Independent patch replication and prospective
  plant-level randomization-based hypothesis
  testing, with control of falsely
  detecting shifts under no true shift.
- A separate pollen-sentinel sampling/power
  plan to tie ecological fertility optima
  to floral pollination performance.

Only after these empirical inputs and a
calibrated confirmatory estimator can a
single final recruitment n be recommended
for SCH's core W1/W2 claims.

## Reproduce the synthetic grid

    python scripts/simulate_pedicularis_two_flower_detectability.py \
      data/SCH_TWO_FLOWER_SYNTHETIC_DETECTABILITY_SCENARIOS_V1.json \
      --output scenario_detectability.json

Focused tests:

    python -m pytest -q \
      tests/test_pedicularis_two_flower_design_detectability.py

No new P. rex field individual was sampled. The
independently randomized plant-level G method is
still a **candidate**, and neither P0, G, P2,
W1/W2, true pure-function optima, SCH L nor
SLK architecture value is authorized by
these synthetic calculations.

Background methodology: Donner et al. and
subsequent reviews of cluster randomized
trial sample size estimation emphasize the
impact of within-cluster correlation on the
number of *independent clusters* rather
than counting subunits as independent
observations. Here the cluster is a
parent plant for G, with patch-stage strata
above it; the actual biological endpoint
is intact seeds per flower.
