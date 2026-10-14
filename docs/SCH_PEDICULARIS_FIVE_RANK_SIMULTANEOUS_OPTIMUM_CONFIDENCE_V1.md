# Simultaneous five-rank confidence sets for the P. rex reproductive optimum

## Ecological question

The SCH hypothesis is not merely "seed-predator exclusion improves seed
production" or "predator treatment changes selection on one selected
exsertion contrast." The mechanistic ecological claim is that
**the floral exsertion rank that maximizes viable mature seed production
differs between predator excluded and predator exposed environments**.

The existing two-flower cyclic experiment randomizes predator G at the
MOTHER PLANT level, and two floral z settings within each plant.
It has five z values and ten z×G treatment cells, with two
different mother plants per cell in each patch×flower-stage batch.

PR #221 established a much more responsive within-mother seed-fitness
contrast test than the discrete sample peak-midrank Fisher statistic.
But that contrast tests a different sharp null, allows arbitrary
mother-specific constant additive seed gains, and still does not
prove that the *whole five-rank* fitness optimum moved.

The next necessary inferential object is a **confidence set of optimal
ranks** that accounts for uncertainty in ALL five levels
SIMULTANEOUSLY for both G states, rather than picking the
observed maximum and comparing it only after selection.

This is the classical statistical **multiple comparisons with the best**
problem (Hsu 1982; Chang & Hsu 1992). The implementation here
takes a deliberately conservative, transparent and source-specific
route: **distribution-free Hoeffding concentration over truly
independent patch-stage batch vectors**, with Bonferroni
simultaneous protection for the entire rank-comparison family.

## Registered sampling and bounded outcomes

Before any analysis, require the original
source-locked two-flower allocation receipt and the
complete enrolled mature-fruit outcome rows; every
flower/plant/z/G identity must pass the same validation
as in PR #217 and the fruit-fate bounds of PR #213.

Each fruit is either exactly counted, pre-dispersal
verified zero, or has a prospective, source-justified
unknown mature seed yield [0,U] / partial [L,U].
**Missing mature fruits are not imputed as zero or deleted**.

An additional **prospectively registered population-wide
mature viable seed-count upper cap K** is required.
It is NOT inferred from the observed maximal seed count
or the 2016 source's mean ovule number.

Treat every unique patch×flower-stage batch as one
statistically independent sampled/assigned block
of **ten whole mother plants and twenty flowers**.
The two mother plants contributing a treatment
cell are averaged *within* each block, preserving
possible within-plant, within-patch and between-
treatment correlations. No pseudoreplication
from the twenty flowers in that patch is allowed.

The same geographical patch observed in two flower
stages must not be entered as two independent blocks.
Patch-to-patch stochastic independence, selection
of representative patches from a coherent target
population, correct randomization at the plant
level, valid physical z settings, source
selectivity of predator exclusion, no spillover
and a genuine global K require FIELD verification.
Without them, a nominal 95% guarantee is conditional
mathematics rather than an externally supported
ecological claim.

## Simultaneous inequality and confidence construction

For every predator treatment g and unordered z
pair a,b (with a<b), there are
2×binomial(5,2)=**20** possible pairwise z
comparisons across the two G states.

Let [L_(g,z,b), U_(g,z,b)] be the within-batch
interval for mean intact seeds/flower at
treatment (g,z) in independently sampled batch b.

The unknown mature-seed mean rank difference
within a given batch is bounded by

    d_lower_(g,a,batch,b_rank)
       = L_(g,a,batch) - U_(g,b_rank,batch)
    d_upper_(g,a,batch,b_rank)
       = U_(g,a,batch) - L_(g,b_rank,batch).

For each comparison, average both endpoints
over the B independent patch-stage batches,
getting [D_lower,D_upper].

If **every conceivable intact seed outcome is
between 0 and the precommitted K**, every batch
comparison endpoint is bounded in [-K,+K].
Hoeffding's inequality and the union bound
over **40 one-sided tail events** (lower
endpoint of 20 differences, upper endpoint
of 20 differences) give the common
simultaneous error radius

    epsilon = K * sqrt(2 * log(40/alpha) / B).

For every g,a,b simultaneously, the population
mean difference mu_g(a)-mu_g(b) is enclosed in

    [ D_lower - epsilon, D_upper + epsilon ],

intersected with the physically possible [-K,K].

Conditional on the stated independent batch
sampling/assignment design, registered K and
source outcome fates, the simultaneous
family has confidence at least **1-alpha**.
It does NOT require normal seed counts, does
not choose a maximum before adjustment,
and remains valid against informative fruit
missingness because its worst-case unknown
outcomes are still bounded, **not estimated**.

There are 20 DIFFERENCES protected (40 one-sided
endpoints), not 10 simple cell means and not
individual fruit replicates.

### Selection-safe elimination of non-optimal ranks

A rank z is rejected as a possible best in
one predator state ONLY when another rank j
has a simultaneous lower confidence bound
on mu_g(j)-mu_g(z) strictly greater than zero.

On the event that all twenty pair intervals
cover their true values, a truly maximizing
rank can never be discarded. Thus the
remaining set S_E (G excluded) or
S_X (G exposed) simultaneously includes
every genuine best rank.

For the outer shift in optimum rank:

    shift_min = min(S_E) - max(S_X)
    shift_max = max(S_E) - min(S_X).

**If shift_min > 0**, predator exclusion
has a strictly higher rank optimum in all
allowed confidence completions. **If
shift_max < 0**, it has a strictly lower
rank optimum. Otherwise the weak-null
direction is **not identified by this
confidence procedure**.

This is a conservative *simultaneous confidence
set* approach to the weak ecological direction
of optimum shift under independent patch-sampling
and a qualified experiment — unlike
the previous Fisher SHARP-null p tests.
It is NOT itself a plant-label conditional
randomization test or evidence of any
qualified actual predator treatment.

## A new and important negative result: a rigorous guarantee may be unusable at field scale

Use the frozen strong-effect synthetic
potential curves (NOT measured P. rex):

    excluded seed means = [5, 7, 10, 14, 19]
    exposed seed means  = [5, 8, 13,  8,  5],
    K = 40 intact viable seeds per flower,
    alpha = .05.

At each patch batch the underlying mean
curves are exactly these values, with
no noise and no maturity missingness.
The sample winner is ALWAYS excluded z4
versus exposed z2: the descriptive
optimum displacement is +2 ranks.

But a nonparametric worst-case confidence
guarantee must protect all 20 comparisons
against every bounded batch outcome
distribution. The radius is:

| Independent patch-stage batches B | Enrolled mothers (10B) | epsilon, intact seeds/flower |
|---:|---:|---:|
| 2 | 20 | 103.4 (clip to physical range) |
| 8 | 80 | 51.7 |
| 32 | 320 | 25.9 |
| 100 | 1000 | 14.6 |
| 855 | 8550 | 5.0018 |
| **856** | **8560** | **4.9989** |

The closest competitor to both
the excluded z4 optimum and the exposed
z2 optimum is just **5 intact seeds
per flower worse** in these synthetic
profiles. Therefore, in the noiseless
identical-patch fixture, at B=855
the strict simultaneous guarantee still
cannot uniquely separate the two optima;
at B=856, it can certify both unique
optima (z4, z2), giving a positive
rank displacement of +2.

**856 batches / 8,560 plants is NOT
an empirical sample-size recommendation.**
It is the cost of an exceptionally conservative
distribution-free familywise guarantee
for the pre-specified worst-case K and
effect margins. The unrealistic requirement
is an informative *negative result* about
using such universal bounds as a primary
field-study inferential procedure.

This motivates calibrated, variance-aware
plant/patch covariance estimation and
simultaneous comparison methods (e.g.,
multiple-comparisons-with-best or valid
patch-resampling and randomization-based
bands) rather than falsely suggesting
that existing 10–40-plant simulation
frequencies deliver 95% statistical
confidence of optimum displacement.

## Missing maturity information cannot be solved simply by B→∞

The outcome-fate error interval [L,U]
is kept *inside* every patch contrast
before sampling uncertainty is added.
If a non-vanishing fraction of source
final seed counts stays completely
unobserved, even the sample-level
fitness contrast may remain ambiguous
as independent patch replication increases.

In that case a smaller statistical
radius cannot restore an ordering
not identified from the observed
seed-fate intervals. Source recovery
and independently justified individual
upper seed-potential bounds are
therefore biologically necessary.

## Exact implementation and adversarial tests

The module
\`scripts/certify_pedicularis_simultaneous_optimum_rank.py\`
first executes the original complete
two-flower fate/assignment validator
and requires the explicit population-
wide viable seed cap K. It rejects:

- fewer than two independently sourced
  patches, duplicate patch IDs across
  flowering stages, malformed or missing
  z×G treatment cells;
- altered source z/G or flower IDs,
  unregistered physical method labels;
- per-flower seed caps exceeding the
  registered population-wide K;
- negative, inverted, infinite or
  otherwise impossible seed-outcome
  intervals and invalid alpha.

Source rows may have genuine unknown
fruit fates, which widen the bounds
without being mislabeled as observed
zero mature seed count.

Regression tests verify the exact
20-comparison/40-endpoint arithmetic,
source identity, synthetic 855/856
threshold, full sample versus
confidence optimum rank sets,
a no-treatment-difference true-null
control, and honest fail-closed
behaviour with patch reuse.

Reproduce on **prospectively qualified** data:

    python -m scripts.certify_pedicularis_simultaneous_optimum_rank \
      all_allocated_fruit_fates.csv frozen_two_flower_receipt.json \
      --registered-seed-cap REGISTERED_GLOBAL_K \
      --alpha 0.05 --output simultaneous_rank_confidence.json

Focused tests:

    python -m pytest -q tests/test_pedicularis_simultaneous_optimum_rank.py

## Main claim ceiling and next research step

This is a **formal conditional confidence-set
construction**, but not a new empirical P. rex
field result. Neither patch independence,
eligible-plant representativeness, treatment
G selectivity, flowering-stage comparability,
physical exsertion first stage, nor
interference-free seed predation is
verified by the repository.

If these field conditions fail, the
1-alpha statement cannot be used
for publication-grade causal inference.

A powerful future method would use
**plant- and patch-aware variance estimates
for all twenty within-G rank comparisons
and an efficient simultaneous best-treatment
procedure**, with simulation-calibrated
coverage across null and alternative
ecological fitness surfaces. The
current strict method provides a safe
reference or fallback benchmark.

No SCH pure mutualist/antagonist
function optimum, architecture compromise
L, full four-state W1/W2 or SLK payoff
is established.

### Literature foundations

Hsu, J. C. (1982).
*Simultaneous Inference with Respect to the Best Treatment in Block Designs*.
JASA 77:461–467. doi:10.1080/01621459.1982.10477833.

Chang, J. Y. & Hsu, J. C. (1992).
*Optimal Designs for Multiple Comparisons with the Best*.
J. Statistical Planning and Inference 30:45–62.
doi:10.1016/0378-3758(92)90106-3.

The implementation here is **not** a
verbatim MCB procedure from either paper.
It uses a self-contained, conservative
Hoeffding/union-bound simultaneous
rank-elimination certificate.
