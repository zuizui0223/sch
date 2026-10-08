# Stage coupling can reverse selection without changing either functional marginal

## Core ecological question

Suppose two environments or two plant populations show the same
trait-specific average seed initiation and the same trait-specific
seed-predation rate. Does that determine whether a larger floral
trait value has higher final viable seed reproduction?

**No.** It may not even determine the *direction* of the viable-seed
gradient, because successful ovule development and predation need
not be statistically independent **within a fruit**.

A closely related sequential-fitness approach is established
empirically in *Ipomopsis* (American Naturalist 2022,
doi:10.1086/716740; source Dryad doi:10.7280/D1KM49):
seed initiation and escape from seed predation are separate
life-stage reproductive filters. That precedent does **not**
verify any stage-coupling reversal in the focal *Pedicularis rex*.

## Exact identity, and what the means omit

Within a fixed trait setting `z`, for each fully observed fruit:

```text
I = initiated / ovules                  0 < I <= 1
q = damaged / initiated                0 <= q <= 1
F = undamaged / ovules = I*(1-q)
```

Assume the damaged-seed counts genuinely recover all initiated
seeds and do not include completely destroyed seed material with
unrecognizable fates. Then:

```text
E[F | z] = E[I | z]*(1-E[q | z]) - Cov(I,q | z).
```

Both marginal curves `E[I | z]` and `E[q | z]` can therefore be
unchanged while their **coupling structure** shifts the location
or direction of reproductive selection.

The difference between two trait settings L and H also obeys
the exact midpoint decomposition:

```text
DeltaF =
    (1 - midpoint(mean_q)) * Delta(mean_I)
    - midpoint(mean_I) * Delta(mean_q)
    - Delta Cov(I,q).
```

Here the covariance is within a trait-setting cell, not a
pollen–seed covariance between distinct sacrificial sentinel
flowers and intact mature fruits.

## Synthetic two-world counterexample, with valid seed counts

Assume each fruit has **40 ovules**, and each trait setting
has two equal-weight capsules. The separate initiation and
predation marginal distributions are identical across World A
and World B:

| Trait rank | Initiation I values | Predation q values | Mean I | Mean q |
|---|---|---|---:|---:|
| LOW | 0.05, 0.75 | 0, 0.50 | 0.40 | 0.25 |
| HIGH | 0.20, 1.00 | 0, 0.50 | 0.60 | 0.25 |

All fractions can be realized with integer initiated/damaged
seeds at 40 ovules. Thus the trait shows a positive mean
initiation benefit (+0.20) and **no average predation
difference** whatsoever.

**World A — predation falls on the high-initiation fruit in
the HIGH trait cell:**

```text
LOW:  (I=.05,q=.50), (I=.75,q=0)
      mean viable F = (.025 + .750)/2 = 0.3875
HIGH: (I=.20,q=0),   (I=1.0,q=.50)
      mean viable F = (.200 + .500)/2 = 0.3500
HIGH minus LOW = -0.0375
```

**World B — swap predation between fruits without changing
a single marginal observation:**

```text
LOW:  (I=.05,q=0),   (I=.75,q=.50)
      mean viable F = (.050 + .375)/2 = 0.2125
HIGH: (I=.20,q=.50), (I=1.0,q=0)
      mean viable F = (.100 + 1.00)/2 = 0.5500
HIGH minus LOW = +0.3375
```

The same trait-specific input means, the same entire
**unpaired I and q marginal distributions** and the same
presumed sampling frame are compatible with selection
**against** higher z or selection **for** higher z.

These are **constructed mathematical worlds**, not observed
*Pedicularis* populations or estimated population effects.
The example shows the precise unobserved ecological degree
of freedom: **which initiated-seed outcomes are attacked**.

## Sharp bounds without inventing fruit matching

A stronger result than "covariance is missing" is available
if the **complete marginal empirical distributions** are
measured but their fruit pairing is lost.

For equal-weight positive-I fractions, sort `I` and `q`
in each trait cell. By the **rearrangement inequality**:

- sorting both in the same order **maximizes**
  `mean(I*q)` and **minimizes** viable fitness;
- sorting in opposite order **minimizes**
  `mean(I*q)` and **maximizes** viable fitness.

This yields exact sharp bounds on the empirical mean viable
seed fraction over all unknown one-to-one pairings, without
assuming an unmeasured independence model:

```text
F_min(z) = mean(I_z) - mean(sort(I_z) * sort(q_z))
F_max(z) = mean(I_z) - mean(sort(I_z) * reverse(sort(q_z)))

DeltaF = F(H)-F(L)
lies in [F_min(H)-F_max(L), F_max(H)-F_min(L)].
```

For the example:

```text
LOW viable range   [0.2125, 0.3875]
HIGH viable range  [0.3500, 0.5500]
HIGH−LOW range     [-0.0375, +0.3375].
```

Zero lies inside the sharp interval, so **sign not identified**.
In a distinct scenario with non-overlapping tight bounds,
sign **can** be identified despite missing matching; the tests
verify this positive and negative case. The inference target
remains a bounded **finite empirical sample**, not a population
confidence interval or proof of randomized causal selection.

**Sharpness is relative to the stated fractional model.**
If each fruit has a verified finite number of ovules and
damaged/initiated seed counts must be *integers*, some
continuous-fraction q–I matches may be biologically
impossible. Additional integer or fate constraints can then
tighten these conservative fractional bounds. The two-world
40-ovule witness above was checked to have integer counts
under **every specific matching shown**. With general source
data, a physical integer-feasibility audit is needed
before calling the unrestricted rearrangement extrema
biologically attainable.

This procedure needs **full within-setting marginal samples
of equal size and equal weight**. It cannot be run on
published means alone, unequal sample sets without a
registered weighting/optimal-transport extension, or fruit
predation rates reported after selectively excluding
completely consumed capsules.

## Relevance to SCH–SLK–BITA

This is a *non-identification of fitness selection from
unpaired reproductive-stage margins* at the ecological level.

It sharpens the previous 2014–2015 orchid result:

```text
interaction intensity                  not sufficient
trait-conditioned mean stage response  may still be insufficient
stage coupling + individual fate       can determine final fitness direction.
```

The 2016 *P. rex* observational source reports fruit outcomes
at a different grain than the stigma-pollen observations and
has completely consumed fruit-fate ambiguities; do not apply
this witness as if its empirical covariance has been measured.

The already coded separate *P. rex* fruit cohort, if executed,
records initiation and predation on **the same intact fruit**
and estimates their coupling; separate pollen sentinels are
used only for the upstream marginal pollen response. If
complete destruction or 0/0 seed fate is ambiguous, even
within-fruit q can remain unidentified. In that case
pre-register a censoring or missingness sensitivity route;
do not substitute the abstract sharp matching bound for
missing biological fractions.

**No** pure F1/F2 optima, four-state SCH compromise penalty
L, SLK R/K/Phi or historical trait architecture can be
promoted by this mathematical construction.

## Machine reproduction

```sh
python scripts/bound_sch_unpaired_seed_stage_selection.py \
  data/SCH_STAGE_COUPLING_SYNTHETIC_MARGINS_V1.csv
python -m pytest -q tests/test_sch_unpaired_seed_stage_selection.py
```

The CSV is **synthetic and illustrative**. It encodes
`setting,channel,value` without putting fictitious
I and q together in a fruit row. The script outputs sharp
bounds and an explicit unresolved/positive/negative
finite-sample sign status, without imputed matching.
