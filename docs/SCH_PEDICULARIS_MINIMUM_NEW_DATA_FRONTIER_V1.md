# SCH Pedicularis minimum new-data frontier v1

## Purpose

After published-data recovery and method-precedent recovery, the unresolved
40-field F0 package should not be interpreted as requiring forty new
measurements or thirty-five separate experiments.

The minimum focal direct-data burden is smaller.

## Gate accounting

```text
40 total F0 gates

 5 already registered / no new data
27 empirical target gates requiring focal calibration measurements
 8 sample-size gates computed downstream by CAL-C
```

Thus only 27 gate targets require new focal empirical calibration.

Those 27 targets are supplied by exactly three calibration cohorts:

```text
CAL_P0   8 empirical targets
CAL_P1   8 empirical targets
CAL_G   11 empirical targets
        --
        27.
```

## Why repeatability is not a fourth cohort

The same-flower CAL-A repeatability flowers are deliberately a subset of the
P0 calibration flowers.

The P0 calibration cohort therefore supplies both:

```text
same-flower measurement-noise information
+
graded-z manipulation / off-target distributions.
```

Repeatability is a nested measurement component, not an independent field
cohort.

## Cohort 1 — CAL_P0

One P0 calibration cohort supplies the empirical basis for:

```text
minimum adjacent realized-z separation
opening-width change
tube-diameter change
bract-height change
lower-lip-angle change
water-depth change
flower-orientation change
mechanical-damage ceiling.
```

It also supplies variance information for the eight P0 CAL-C planning
criteria.

Same-flower repeats on a subset of these flowers supply measurement-noise
context used not only for P0 but also for compatible P1/G selectivity margins.

Published evidence already supplies focal natural trait scale, instrument
resolution, and a congeneric low-contamination non-destructive manipulation
precedent. It does not supply focal >=5-level manipulation or same-flower
repeatability.

## Cohort 2 — CAL_P1

One separate P1 calibration cohort supplies:

```text
minimum pollen-receipt increase
minimum initial-seed-set / pollen-limitation relief
maximum early-predator contamination
maximum z change
maximum bract-height change
maximum opening-width change
maximum water-depth change
maximum handling damage.
```

It also supplies the eight P1 CAL-C variance inputs.

Published evidence is unusually rich here: focal high outcrossing, focal
pollen/reward/ovule scales, and multiple congeneric supplementation studies
from null to large effects. These reduce design invention but do not replace
the missing focal registered supplementation effect.

## Cohort 3 — CAL_G

One separate G calibration cohort supplies:

```text
minimum early-attack reduction
minimum predation-fraction reduction
minimum final intact-seed gain
earliest usable barrier time
latest usable barrier time
maximum initial-seed-set contamination
maximum pollen contamination
maximum visitor contamination
maximum z change
maximum water-depth change
maximum handling-damage difference.
```

It also supplies nine G CAL-C variance inputs.

Published evidence already supplies focal oviposition timing, focal natural
predation variability, the wrong-axis water-defence causal experiment,
within-genus post-pollination timing, and within-genus barrier efficacy.

The missing quantity is narrower: focal barrier effectiveness/selectivity
under natural bumblebee pollination with water-y fixed.

## CAL-C is not a field cohort

After CAL-A/B target values are frozen, CAL-C computes the remaining eight
sample-size fields from:

```text
25 criterion variances
+
25 frozen boundaries
+
prospective assumed true values
+
familywise power / design-effect assumptions.
```

No fourth calibration field cohort is created.

## Independence rule

```text
P0 flowers != P1 flowers != G flowers.
```

Repeatability flowers may overlap P0 because repeatability is nested within
CAL_P0.

Plant-level overlap among calibration modules may be reported by the cohort
registry but must not be silently treated as independent. Where practical,
plant-level separation is cleaner.

## Machine state

Ledger:

```text
empirical/architecture/PEDICULARIS_MINIMUM_NEW_DATA_FRONTIER_V1.csv
```

Audit:

```bash
python scripts/audit_pedicularis_minimum_new_data_frontier.py
```

Current status:

```text
THREE_FIELD_CALIBRATION_COHORTS_ARE_THE_MINIMUM_DIRECT_DATA_FRONTIER
```

## Claim ceiling

This compression minimizes distinct calibration cohorts. It does not reduce
the requirement that each target be prospectively justified, and it does not
turn published external priors into direct focal gate values.
