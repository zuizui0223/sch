# Water level can change selection without changing mean enemy pressure in the same way

## Biological question

In *Pedicularis rex*, can loss of rainwater defence **increase average seed-predator
attack while decreasing the difference in attack risk between low and high
floral exsertion**? If so, a population with *greater average attack pressure* could experience
*weaker* selection against exsertion, not stronger selection.

This is a falsifiable **new prospective prediction**, not a result of the
2015 and 2016 papers. Do not merge the two publications into a fabricated
`exsertion x water` factorial dataset.

Sources:

- Sun & Huang 2015, doi:10.1093/aobpla/plv019, Methods (Seed predation;
  Effects of water removal on pollinators and nectar robbers), Tables 1–2.
- Sun, Armbruster & Huang 2016, doi:10.1093/aob/mcw097, Methods (Traits
  measured), and the observational exsertion-to-pollen and predation results.

## What the published evidence does and does not show

**2015**: Water drainage was achieved by **cutting a hole at the base of the
cupulate bract with scissors**. The treatment was applied to 20–30
inflorescences/individuals per population (40–60 tagged individuals from 20
dense subplots/population). Seed predation was scored from multiple capsules
within individuals. This identifies the effect of the *compound
puncture-plus-drainage treatment* in those populations. Without a separate
non-wounding water-removal arm or punctured-but-water-retaining control,
the publication does **not** experimentally isolate water presence from bract
damage/seal differences or other associated changes.

Across six populations the published seed-predation treatment coefficients
share the same negative **GLM coefficient sign** (under the original treatment
coding). In Zhongdian the published beta was -0.093 with SE 0.348 (P=0.789);
its point estimate was not opposite in sign to the other populations. The
median SE of the other five reported site effects was 0.017, so this
particular *nonsignificant* site has about 20.5 times their reported
uncertainty. **No effect detected** must not be narrated as **a biological
effect absent**, while the published site-by-treatment heterogeneity
test remains positive (chi-square=36.782, df=5, P<0.0001).

Pollinator and robber visitation was compared at **Shama only**, using ten
plots across 2010–2011, not in all six study populations. Its water-treatment
pollinator P=0.958 is a non-rejection of the null, **not** a prospective
equivalence demonstration or proof that water handling is neutral everywhere.

**2016**: Corolla exsertion
`(flower_length - bract_height) / flower_length` was observationally
associated with both greater stigmatic pollen receipt and greater seed
predation. That ratio is **not** a measured water-surface height or
individually randomized exsertion treatment.

The source-level check is machine-readable in the existing
`scripts/audit_pedicularis_published_empirical_priors.py` receipt field
`water_2015_site_evidence`, without any conversion of the paper's
coefficients into raw risk differences or prospective F0 values.

## Three non-equivalent biological explanations

**H1 — physical-waterline shielding.** The accessible location for insect
oviposition is determined by the amount of reproductive tissue above the
actual water surface, not simply by corolla length or bract depth. For a
given high-vs-low randomized exsertion contrast, retained water can protect
the lower treatment disproportionately, creating an exsertion-dependent
difference in predator attack. Drainage can expose *both* treatments, increasing
mean attack and sometimes reducing the remaining high-low difference.

**H2 — wound / handling / associated physiological cue.** Cutting a bract,
altering surface chemistry, causing microclimate changes, or changing
oviposition substrate might raise attack independently of water height.
If attack follows puncture or handling at matched measured water levels, the
original drainage treatment cannot be attributed to a physical liquid barrier.
The actual oviposition cue remains unknown; do not assert volatile induction.

**H3 — saturating attack probability with unchanged predator preference.**
A bounded risk-scale interaction can appear even if predators respond to
exsertion with the **same log-odds slope** in wet and dry plants. Under

```
p(attack | z, y) = logistic(alpha + beta * z + delta * I(dry))
```

the dry treatment increases risk if delta>0 but has *no* z-by-water
interaction on the logit scale. Yet a *risk-difference* contrast can shrink
or grow according to where the baseline risk lies. Illustrative values at
two z levels, with the same beta and delta in both scenarios:

| Scenario | Retained low/high risk | Drained low/high risk | High-minus-low: retained vs drained |
|---|---|---|---|
| Approaching saturation | 0.332 / 0.668 | 0.690 / 0.900 | 0.336 vs 0.210 |
| Starting at low risk | 0.047 / 0.168 | 0.182 / 0.475 | 0.121 vs 0.293 |

Those numbers are a **mathematical illustration, not observed P. rex
measurements**. A smaller risk difference is still ecologically meaningful
when predators actually destroy seeds, but it is **not itself proof**
that predators changed their trait-discrimination rule.

Thus the sign of the risk-scale interaction is a *contingent prediction*,
not a universal theorem about draining water. Both signs and null results
are biologically possible.

## Minimal causal intervention that discriminates H1 from H2

The 2015 intervention targeted **individual inflorescences/plants**,
not separately randomized flowers; water can be shared among flowers at a
whorl or along the inflorescence. Repeating water assignment independently
within a plant risks treatment spillover and pseudo-replication.

Use a conservative **plant-level water assignment** (stratified/randomized
within independent patches), with multiple exsertion `z` settings randomized
among distinct intact fruit-bearing flowers **within each plant**. When
feasible, apply at least five predeclared z levels for comparability with P0.
One plant contributes **one** independently water-randomized unit; several
capsules/flowers within it do not multiply water-arm replication.

The minimally identified water contrast requires:

- **WET_HANDLING_SHAM**: bracts remain intact and water is retained, with
  matched non-puncturing instrument contact.
- **DRY_NONPUNCTURE**: water is aspirated/wicked without cutting the bract,
  with *identical visit frequency, instrument contact and time* as the sham.
  Confirm retention of the treatment throughout the actual oviposition
  exposure interval despite rainfall/refill.
- Optional mechanistic comparison after the water-only contrast:
  `DRY_PUNCTURED` and a wound-control at matched water content. A direct
  water-vs-puncture decomposition is possible **only if the physical
  device/control combinations are successfully validated**; merely naming
  a third arm does not guarantee an identified wound effect.

If a non-wounding dry treatment is physically impossible or rewetting cannot
be controlled, report `WATER_ONLY_MECHANISM_NOT_IDENTIFIED` and do not call
the original scissors effect a water-only causal effect. Fix any alternative
sealed-puncture factorial **before** field collection.

A separate *negative-control* measurement of bract injury, microclimate and
handling must be recorded in every treatment. The exact manipulation
`setting_id` (not merely the label `dry`) must be pre-frozen.

## Exposure geometry, sampling and outcomes

Measure at the flower/whorl level **before and during predator access**:

```
assigned_z_rank, realized_corolla_exsertion_mm
flower_base_and_ovary_elevation_mm
bract_rim_elevation_mm
water_surface_elevation_mm
exposed_ovary_or_corolla_length_above_water_mm
rainfall_or_refilling_observation
bract_puncture_and_handling_damage
flower_age, stage, whorl_id, plant_id, patch_id
```

The relevant physical mediator is **actual exposure above the waterline**,
not `assigned_z_rank` and not `(flower length - bract height)/flower length`.
Use assignment for ITT causal inference. Do not condition the primary
assignment contrast on realized exposure as if it were randomized.

Independent primary biological endpoints:

1. **Early attack/oviposition** assessed with a prospectively validated,
   non-destructive observation method or a *separate* sacrificial diagnostic
   cohort where necessary.
2. **Final intact viable seeds per ovule or per flower**, recorded on intact
   mature-fruit flowers with explicitly observed fruit fate.

Predeclared fruit fates must distinguish absence of development from
complete destruction. A capsule with zero distinguishable damaged and
undamaged seeds is not automatically 100% predated. Initial seed set,
late larval survival and final viable seed production must never be conflated.

The PR #200 stigmatic-pollen sentinel assay can be a *separate*
pollination-facing endpoint but **does not** by itself provide the
water-by-z experiment, a pollinator pure-function optimum, or same-flower
pollen–seed covariance. Visitor-rate non-difference reported at Shama does
not prove the absence of water effects on pollen transfer at other sites.

## Ecological contrasts to estimate without invented data

For each water-assigned plant `i`, calculate the slope of early attack
probability across its preassigned z ranks, `b_Ai`. Compare wet vs dry
**plant-level slopes** within patches, and use patch-aware randomization or
resampling. The directional interaction is

```
Delta_attack = slope_A(WET) - slope_A(DRY)
baseline_effect = mean_A(DRY) - mean_A(WET)
```

The paradoxical ecological world occurs when both are positive on the
**risk scale**, conditional on adequate uncertainty support. A positive
`Delta_attack` is not by itself evidence of a changed log-odds preference:
inspect the standardized logit-scale z-by-water contrast and compare
measured waterline exposure.

The fitness counterpart compares z-by-water differences in **final viable
reproduction**, with patch/plant uncertainty and the correct outcome
denominator. Only if this also changes is there support for a change in
*realized reproductive selection*, rather than a change in attack alone.
An interaction in early attack and a null final-fitness interaction is a
scientifically meaningful outcome; avoid post-hoc compensation stories.

Do not estimate or claim a four-state SCH `W00-W11` surface,
`z_P*`, `z_G*`, pure function optima or `L` from this two-factor
BITA-y mechanism experiment.

## Repository boundary and next empirical fork

The primary SCH full-surface design **holds bract-water y fixed** and needs
a separate predator exposure/exclusion `G`. This secondary
waterline/access project is orthogonal to that registered G route and
cannot rescue failed P0/P1/G readiness, a blocked original W1/W2
same-flower assay or an unqualified pollen sentinel.

If a direct field programme is not available, this protocol remains an
evidence-bounded, preregistration-ready biological hypothesis, not a newly
observed result. External source data supply **zero** randomized
`z x water` observations at present.

Tracking: issue #201, PR #200 and the independent
`docs/SCH_PEDICULARIS_WATER_G_DEPRECATION_V1.md` boundary.
