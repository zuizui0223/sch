# Calibration of a plant-level Fisher test is not power for optimum displacement

## Which statistical problem was unresolved?

The two-flower *Pedicularis rex* cyclic design assigns **predator G to
whole mother plants** and two different experimentally specified floral
exsertion z settings to their two flowers. A given patch × developmental
stage × cyclic z-edge has **one excluded and one exposed plant**.
Consequently, exact Fisher randomization inference swaps the whole
plant's G label with its edge-matched counterpart, keeping **both flowers
together**. No separate permutations of flowers are legitimate.

PR #218 simulated 3,000 candidate datasets and classified whether the
observed *finite-sample* excluded-versus-exposed optimum-rank shift was
positive. Its **no-shift** control sometimes classified positive simply
because small-cell means fluctuate. A classification frequency is not
nominal-alpha inferential power.

PR #219 subsequently implemented a conditional Fisher test using the
peak-midrank difference

    T = peak_midrank(EXCLUDED) - peak_midrank(EXPOSED)

over all five experimentally assigned z settings. This addition uses
that **actual implementation** to examine sharp-null calibration and
rejection under different causal alternatives.

## The five deliberately distinct worlds

All distributions below are **synthetic assumptions**, not measured
*P. rex* means, P0 pilot evidence, G method success or estimated
maternal variance. Each run regenerates the complete source-equivalent
10-plant cyclic assignment for each patch-stage batch.

| Assumed data-generating condition | G difference in seed output | Specified top-ranked z |
|---|---|---|
| SHARP_NO_G_EFFECT | Every flower has the *same* potential seed count under G excluded/exposed | z2 in both arms |
| COMMON_ADDITIVE_G_GAIN | +3 intact seeds per flower at every z | z2 in both arms |
| HETEROGENEOUS_PLANT_G_GAIN | Mean +3, but effect varies among plants rather than being an imposed G×z term | z2 in both intended mean curves |
| CHANGED_G_BY_Z_SAME_PEAK | Seed-count differences vary with z | z2 remains best in both intended mean curves |
| PREDATOR_EXCLUSION_SHIFTS_PEAK | Seed-count response changes with z | Excluded z4; exposed z2 |

The exposed mean curve is [5, 8, 13, 8, 5]. The
**excluded** curve is the same for sharp-null, +3 at
every setting for additive conditions (heterogeneous
plant gains further vary by plant), [8,10,17,12,9] for
the same-peak shape change, and [5,7,10,14,19] for the
assumed peak displacement.

Potential seed counts are generated **before choosing
the observed G result**, using an independent deterministic
random-number substream from the hashed plant G
randomization seed, with a shared patch effect,
a mother-plant effect shared by both flowers and
independent flower noise. Counts are rounded and
clipped to a synthetic finite upper seed cap. Such
clipping can slightly change the realized potential
mean curve, especially under large variance; it must
not be described as an exact, unqualified
constant-additive effect in every random world.

No field source population variance is inferred from
these hypothetical parameters.

## Which rejection fraction can be interpreted as what?

The **Fisher sharp null** is

    H0: Y_i(EXCLUDED,z) = Y_i(EXPOSED,z)
        for EVERY allocated flower i at its fixed assigned z.

Under this particular world, the matched whole-plant
assignment permutation is exact, conditional on the
registered z-edge and flower positions. The empirical
fraction with one-sided p ≤0.05 is a Monte Carlo check
of **sharp-null Type-I error**, with simulation
uncertainty. Its nominal validity is determined by
the actual randomization, not by fitting a regression
to the simulated means.

For each NONSHARP world, the same fraction estimates
the probability of **rejecting this strong sharp
no-effect null** under the invented data generator.
It is **not** a test of the weak null of no change
in population optimal z. In particular:

- Uniform additive predator benefit **does not**
  move the true peak in the specified mean curves,
  but violates the no-G-effect sharp null.
- Plant-specific effects can violate sharp
  no-effect and universal constant-additive
  nulls even without a designed z-dependence.
- A z-dependent predator effect may change
  the response surface **without** moving
  the maximizing rank.
- A true optimum shift in the generator may
  nevertheless have low rejection probability
  for a coarse or noisy peak-midrank statistic.

The output deliberately reports both

    fraction_descriptive_positive_peak_shift
    fraction_Fisher_sharp_no-effect_rejection

**separately**. It additionally reports their
joint fraction and an approximate Wilson 95%
simulation-proportion interval for the *rejection
frequency* (not a field-treatment confidence
interval). With 60 simulated datasets per
scenario/size condition, those percentages have
considerable Monte Carlo uncertainty.

The matched plant-pair Fisher test has only
2^5=32 possible assignments with one ten-plant
batch (minimum nonzero exact p=1/32). The test
enumerates exactly at 10 and 20 enrolled plants
(5 and 10 edge pairs) and uses plus-one Monte
Carlo tail inference at 40 enrolled plants
(20 edge pairs; 999 random assignments per
simulated dataset). This distinction is explicit
in the output.

## Executed synthetic calibration — negative sensitivity finding

After fixing the random-seed range bug, the dedicated
[GitHub Actions run 38403310656](https://github.com/zuizui0223/sch/actions/runs/38403310656)
completed the entire **900 dataset** frozen study
(5 scenarios × 3 independent-plant counts × 60
realizations), including source-consistent whole-plant
assignments and exact or plus-one Fisher permutations.

The numbers below report two **different** simulation
frequencies, each out of 60 replicates. Cells read
**positive sample-peak shift / p≤0.05 sharp-null
rejection**, in percent:

| Synthetic potential-outcome world | 10 plants | 20 plants | 40 plants |
|---|---:|---:|---:|
| Sharp no-G-effect null | 0 / 0 | 0 / 0 | 0 / 0 |
| Constant additive G gain | 1.7 / 0 | 0 / 0 | 0 / 0 |
| G gain heterogeneous by plant | 5.0 / 0 | 0 / 0 | 0 / 0 |
| G changes z-response but optimum still z2 | 0 / 0 | 0 / 0 | 0 / 0 |
| **Excluded peak z4, exposed peak z2** | **100 / 0** | **100 / 0** | **100 / 1.7** |

The **unexpected central result** is that under this
very favorable large peak-shift alternative,
the peak-midrank Fisher test rejected the sharp
null in **only 1 of 180 true-shift synthetic
allocations** across all tested sizes.
At 40 plants, the estimated rejection
frequency is 1/60=1.7%, Wilson Monte Carlo
95% interval approximately **0.3%–8.9%**;
at 10 and 20 plants, 0/60 each permits
rejection frequencies up to ~6.0% at 95%
Wilson confidence under repeated simulation.

This is **not evidence that predator selection
is absent in P. rex**. It shows this bounded,
coarse **peak-midrank statistic has very
low sensitivity under our synthetic design
and effect curves**, even when the sample
peak ranks differ in the expected direction
in every replicate.

Likewise, 0/60 rejections under the true
sharp null does not establish exact Type-I
error = 0; exact Fisher superuniformity
is a *theorem conditional on assignment*,
while 60 synthetic draws are an imprecise
empirical diagnostic. No null or non-null
simulation rate is a confidence interval
for an actual P. rex experimental effect.

**Protocol consequence:** do not register
peak-midrank Fisher p alone as the
primary powered test of predator-mediated
optimum displacement. The next method
should compare **prospectively specified
quantitative cross-z G-response contrasts**
against the original peak-midrank test,
then separately establish simultaneous
peak identification and a valid test of
the *weak hypothesis* of unchanged
population optimum. Rejecting a targeted
interaction contrast is not itself proof
of an optimum shift.

## Critical formal-null distinction

The existing optional PR #219 sensitivity test
also considers the **union of sharp constant
integer seed-gain effects**. This can rule out
a *universally common* additive gain while
remaining conservative over plausible τ, but
still does not directly test the weak hypothesis
that predator exclusion leaves the population
optimum unchanged.

No amount of sharp-null calibration alone
supplies a valid test of that weak null. A
formal weak-null optimum-rank test needs a
separate estimator, simultaneous uncertainty
over the five response-curve means, plant-
and patch-aware randomization inference,
careful nonregular argmax handling and
prospective multiplicity control.

The present simulation therefore **does
not output a recommended empirical n for
an 80% powered weak-null optimum-shift test.**

## Unknown maturity outcomes remain a hard boundary

All generated flowers have complete intact
mature seed counts so the Fisher method
can be applied. This is intentional; the
current Fisher routine **refuses** to
recode completely consumed or missing
mature fruits as zero, or to drop them
post-treatment and rerandomize only
observed outcomes. Conditional on informative
maturity loss, actual field selection
may remain partly identified and this
calibration does not solve it.

The complementary bounded fruit-fate,
integer-count coupling, and two-flower
missingness tools remain separate.

## Reproduction

Frozen synthetic scenario configuration:

    data/SCH_P_REX_MATCHED_PLANT_FISHER_CALIBRATION_SCENARIOS_V1.json

Run:

    python -m scripts.simulate_pedicularis_plant_pair_fisher_calibration \
      data/SCH_P_REX_MATCHED_PLANT_FISHER_CALIBRATION_SCENARIOS_V1.json \
      --output fisher_synthetic_calibration.json

Tests:

    python -m pytest -q \
      tests/test_pedicularis_plant_pair_fisher_calibration.py

The dedicated GitHub workflow prints the
simulation-proportion table and publishes a
machine-readable JSON artifact. Tests include
an **independent exhaustive 32-assignment
super-uniformity check** under sharp no-G-effect.

Results remain non-gating. No actual *P. rex*
source raw seed data, exact G exclusion
selectivity, observed field effect, or pure
functional optimum is established, and
SCH P0/P1/G/P2/W1/W2 and SLK architecture
value remain blocked.
