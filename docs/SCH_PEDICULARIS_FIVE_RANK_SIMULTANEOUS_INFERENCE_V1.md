# All-five-rank simultaneous uncertainty for the P. rex two-flower experiment

## One biological question; ten treatment-cell means

SCH's core ecological question is whether independent predator exclusion
changes which of five physical floral-exsertion settings yields the
most **intact mature seeds per flower**.

Two earlier inferential objects are useful but not sufficient:

1. PR #221 has a **high-sensitivity matched-mother Fisher sharp test**
   of whether predator G affects a prespecified *relative*
   z4-versus-z2 seed-fitness response. Rejection can indicate
   a shape-dependent response, but is **not** a direct test
   of the full population optimum-rank shift.
2. The two-flower fruit-fate estimator computes **descriptive
   finite-source possible optima** under predator excluded/exposed
   G, retaining verified zero and unknown maturity outcomes.
   It has no sampling/randomization simultaneous confidence
   guarantee for the ten z×G means.

This addition supplies a deliberately **distribution-free,
finite-sample, design-conditional benchmark** protecting
*all ten* z×G treatment-cell mean fitness values simultaneously.
The confidence set for the optimum-rank shift is an outer
projection of those ten joint bands.

Its large-sample conservatism is itself an important design
result. This is NOT a practical-powered final field method
or new measured P. rex biology.

## Correct independent unit: the randomized patch-stage batch

The connected cyclic candidate assigns ten **eligible parent
plants**, with two individually tagged fruit-bearing flowers
on each plant, into one patch × developmental-stage batch.
G is randomized to **the plant**, while each plant's
two flower exsertion settings form one of the five
cycle edges.

Each z×G cell contains two flowers from two distinct
plants **inside the same batch**. The batch-level
sampled cell outcome is

    X_b(g,z) = 1/2 * [Y_(b,plant1)(g,z) + Y_(b,plant2)(g,z)]

with intact mature seed counts for two tagged flowers.
Under the prospective randomization, X_b(g,z) has
a design-conditional expectation mu_b(g,z), whose
value is not observed because the source eligible
flowers do not simultaneously receive all G×z
potential treatments.

Define the target for B already enrolled batches as

    mu(g,z) = (1/B) * sum_b E_randomization[X_b(g,z)].

This is an **average over the assignment distributions
of the fixed enrolled batch identities**. Under
genuine randomized z/plant assignments, stable
potential outcomes and no interference, it can
represent a finite-enrollment treatment response.
It is **not** automatically an optimal phenotype
for a random natural P. rex population.

Independence of these B random assignments,
CONDITIONAL ON the enrolled potential-outcome
schedule, is the crucial concentration assumption.
Flowers inside one batch are NOT independent
sampling units, and the ten treatment-cell means
are not required to be mutually independent.
True ecological independence of patches is
not required for the **conditional** randomization
argument if the entire potential-outcome schedule
is fixed and no cross-batch interference exists,
but population transport still requires a
representative patch sampling design.

The source uses salted SHA256 deterministic
assignment reconstruction. Its hash and
frozen IDs **do not prove** the actual field
assignment was genuinely random or mutually
independent across batches. That execution
must be verified prospectively.

## Finite-sample Hoeffding plus simultaneous union guarantee

Assume, BEFORE randomization, a verified **global
integer physical upper bound** K on the number of
intact seeds in *any* potential flower under *any*
assigned G and z:

    0 <= Y_i(g,z) <= K  for every study flower, g and z.

The within-batch mean X_b(g,z) therefore also
lies in [0,K], even with arbitrary correlation
between its two contributing mother plants.

Hoeffding's concentration inequality for
independent, not necessarily identical,
bounded random variables yields

    P(|mean_b X_b(g,z) - mu(g,z)| > r)
        <= 2 exp(-2 B r^2/K^2).

There are **m=10** treatment-cell means (two G
arms × five exsertion ranks). The union bound
over all ten cells yields simultaneous
probability **at least 1-alpha** that
every mean is inside its band when

    r = K * sqrt(log(2*m/alpha)/(2*B)).

No flower-level variance is substituted for
B. No Gaussian fitness distribution, unverified
maternal ICC, bootstrap asymptotic approximation
or Fisher sharp-null model is needed for this
conservative finite-source confidence statement.

### Retain missing mature seed fates

If actual per-flower maturity data have
documented deterministic bounds [l_i,u_i],
the two flowers in each patch-stage × z×G
cell give batch-mean bounds

    L_b(g,z) <= X_b(g,z) <= U_b(g,z).

The joint Hoeffding event for the *unseen
true X_b* remains valid. Thus conservative
bands on the original design expectation are

    [ max(0, mean_b L_b(g,z)-r),
      min(K, mean_b U_b(g,z)+r) ].

This is valid even when a flower is lost
**because it was heavily predated**, provided
the source outcomes really lie within
the recorded caps and the randomization
assumptions hold.

A confirmed pre-dispersal zero mature viable
yield enters [0,0], without pretending to
know its original initiated-seed or predator
stage q. An entirely unobserved fruit enters
[0,cap] with authentic prospective source
cap, not a fabricated zero.

The tool rejects a source cap greater than the
predeclared global K and keeps **all**
original allocated flower IDs, patch/stage,
plant G and flower z assignment through the
existing fruit-fate source validator.

## From simultaneous mean bands to optimum-rank inference

Let the simultaneous interval for each
arm and rank be [L_(g,z),U_(g,z)].

A rank k is **possibly optimal** within
one predator state if its upper bound
could be at least the largest lower bound
among all five ranks:

    U_(g,k) >= max_z L_(g,z).

It is a **guaranteed unique optimal
rank** only when

    L_(g,k) > max_(z != k) U_(g,z).

The true population (more precisely the
conditional enrolled-batch assignment-marginal)
argmax set is covered by these **outer**
possible-rank sets whenever all 10
confidence bands simultaneously cover.

Taking the most extreme ranks in the
excluded and exposed possible sets yields
an **outer interval for their rank shift**:

    [min(opt_E) - max(opt_X),
     max(opt_E) - min(opt_X)].

If this outer shift interval lies strictly
above zero, a **positive shift** is certified
with coverage/error guarantee conditional
on all assumptions. The same logic applies
to strictly negative shifts. If it
contains zero, the result is unresolved
without further assumptions.

This is a *sufficient condition*: confidence
bounds can be too broad even when a real
shift exists. It does not test Fisher's
sharp no-G-effect null and does not
identify the pure pollinator/predator
component fitness optima of SCH/SLK.

## An unexpectedly stringent sample-size ceiling

Take the **invented** ideal response curves
used in PR #218:

    F_excluded(z0..z4) = [4,6,8,10,14]
    F_exposed(z0..z4)  = [5,9,11,9,6]

Their designated peaks are z4 and z2,
a rank shift of +2. Assume perfect maturity
ascertainment, completely uniform batch
means equal to their true intended means,
alpha=0.05 and a **hypothetical** universal
potential viable seed bound K=25.

| Independent ten-plant batches B | Enrolled plants | Hoeffding joint radius r, seeds/flower |
|---:|---:|---:|
| 1 | 10 | 43.27 (band clips at [0,25]) |
| 4 | 40 | 21.64 (clips) |
| 16 | 160 | 10.82 |
| 32 | 320 | **7.65** |
| 469 | 4,690 | 2.00 |
| 1,873 | 18,730 | **1.00** (slightly below) |

At **B=32 (320 enrolled plants)**, all five
ranks remain possible for both predator
states, yielding outer shift interval
**[-4,+4]**. That means no rank movement
can be certified using these maximally
distribution-free bands, **even though
the hypothetical sample means exactly
match the true preferred curves**.

For the exposed state, its top mean
at z2=11 exceeds the runner-up
z1/z3=9 by Delta=2 seeds/flower.
To certify their strict separation
using two non-overlapping bands of
radius r needs 2r < Delta.

Algebraically, a necessary radius-only
feasibility condition is

    B > 2 K^2 log(2m/alpha) / Delta^2.

With K=25, m=10, alpha=.05 and
hypothetical Delta=2, the smallest
integer meeting that inequality is
**1,873 independent batches = 18,730
eligible plants**, even under perfect
noiseless mean curves.

### A subtle ecological distinction: direction versus exact optimum

The synthetic test now *exactly searches* the
smallest whole-batch B satisfying either
(i) a **strictly positive excluded-minus-exposed
shift** or (ii) identification of **both**
state-specific optimal ranks individually,
under the entirely hypothetical perfect
mean curves above.

At B=468, a positive shift is **not yet
certified**. At B=469 (4,690 plants),
the possible EXCLUDED optimum is **only
z4**, while the EXPOSED optimum might
still be **z1, z2 or z3**. Nonetheless,
**every** compatible excluded optimum
is greater than **every** compatible
exposed optimum: the shift interval
is **[+1,+3]**. The **direction of
optimum displacement** is therefore
already conservatively certified.

To identify both exact state-specific
optima z4 and z2, B=1,873
(18,730 plants) is necessary under
the same artificial radius-only
condition.

This distinguishes a **scientifically
weaker but directly relevant ecological
claim** (the fitness optimum moves
toward higher exsertion) from the
stronger claim that both optimal z
settings are individually recovered.
Both thresholds are extreme because
the chosen distribution-free confidence
method ignores realized seed-fitness
variance and plant/patch covariance.

The earliest batch horizons are computed
by `hypothetical_perfect_curve_horizon()`
and are protected by deterministic
tests at their **B−1/B** boundaries.
They are **not** an empirical sample-
size or 80%-power recommendation.

This is **NOT a biological sample-size
recommendation, minimum powered design,
or evidence about P. rex population size**.
It measures the high price of distribution-free
worst-case coverage. If actual randomized
batch means fluctuate, still more batches
may be needed for this method. If maturity
remains missing at a persistent fraction,
even arbitrarily many batches may leave
an unidentified rank, because the
unobserved counts retain nonzero bounds.

A variance-calibrated but well-justified
plant/patch-aware simultaneous procedure
could be much more informative; it requires
pilot seed-count distributions and
randomization metadata to establish coverage.
The existing high-sensitivity within-mother
Fisher contrast is a **different null and
target**; its synthetic success does not
make this full-peak inference unnecessary.

## Input contract, scientific limits and testing

CLI:

    python -m scripts.bound_pedicularis_simultaneous_five_rank_optima \
      qualified_candidate_fruit_fates.csv \
      original_two_flower_design_receipt.json \
      original_prospective_global_bound_config.json \
      --output simultaneous_peak_outer_confidence.json

The inference config must explicitly name
\`cap_assumption_kind\` as either a
**SYNTHETIC_NOT_FIELD_VERIFIED** benchmark or
a **PROSPECTIVE_FIELD_CAP_CLAIM_NOT_EXTERNALLY_VERIFIED**
declaration, and the cap status must state
\`PRE_TREATMENT_REGISTERED_GLOBAL_POTENTIAL_SEED_CAP\`.
These strings do **not authenticate source facts**.

Regression tests check:

- B=32, K=25 gives exact Hoeffding radius ~7.65;
- structural B≥1873 radius condition for
  a 2-seed ideal gap;
- the full five-rank outer peak sets remain
  nonidentified at 320 plants;
- under 1,873 synthetic perfect batches,
  z4 and z2 become independently uniquely
  ordered, with shift +2, **conditional**;
- missing exposed high-rank fruit outcomes
  remain unidentifiable even at B=1,873;
- all original flower IDs and treatment
  assignments must be source-locked;
- unregistered/global seed caps and invalid
  Hoeffding α values fail closed;
- a separate simulation with arbitrary
  correlation across the ten cells
  checks joint concentration under
  independent batch randomizations.

Causal and ecological qualifications remain
unchanged. There are **no actual measured
P. rex mature seed outcomes** to run through
this inference pipeline, no independent
proof of G exclusion effectiveness, no
confirmed physical z first-stage, no
source-verified universal seed cap, and
no observed W00–W11 architecture value.

The result is a conservative **methodological
baseline for simultaneous full-surface
inference**, not a new empirical positive
optimum-shift result. This module must
remain **non-gating** for SCH/SLK.

Reference:
T. Freidling (2026), *Randomization Inference
with Concentration Inequalities*,
arXiv:2609.18586, a current methodological
preprint extending concentration methods
to clustered/matched randomized settings.
Our construction here uses the much simpler
classical bounded-variable Hoeffding
inequality plus a Bonferroni union bound;
it is not an implementation of the preprint's
more efficient bounds.
