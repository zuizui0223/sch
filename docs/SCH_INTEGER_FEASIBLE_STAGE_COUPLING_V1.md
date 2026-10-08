# Integer seed-count constraints can identify reproductive selection from unpaired stage margins

## Biological identification question

SCH now distinguishes three different data situations:

1. **Matched fruit data:** initiated, damaged and viable seeds are
   observed on the same fully resolved fruit. Reproductive fitness
   and within-fruit covariance are directly reconstructible.
2. **Unpaired stage marginal data:** complete fractions of initiation
   and predation exist within the same trait-setting cohort, but the
   underlying fruit identity joining them is lost. A rearrangement
   inequality gives sharp *fractional relaxation* bounds.
3. **Unpaired margins with known seed counts:** initiated seed counts
   and countable per-fruit ovule numbers are measured, plus exact
   rational predation fractions, but pairing to those predation
   observations is lost. Integer-feasible matching can sharpen
   the interval and sometimes identify its *sign*.

The third situation is new here. A fruit cannot lose 0.5 of a seed.
For a candidate initiation count k, a predation fraction q is
biologically admissible only if k×q is an integer number of
damaged, distinguishable seeds.

## A sharp, reproducible selection-sign example

**Synthetic, not a Pedicularis rex dataset.** Each of two fruits
at either floral-trait setting has exactly 12 ovules:

| Observed unpaired stage sample | LOW floral rank | HIGH floral rank |
|---|---:|---:|
| Multiset of initiated seed counts | 1, 2 | 1, 4 |
| Multiset of countable predation fractions | 1/2, 1 | 1/2, 1 |
| Mean initiation fraction | 0.125 | 0.208333 |
| Mean predation fraction | 0.75 | 0.75 |

The full **continuous-fraction** rearrangement bounds permit:

| Quantity | Continuous relaxation |
|---|---:|
| LOW mean viable seed fraction | [1/48, 1/24] |
| HIGH mean viable seed fraction | [1/48, 1/12] |
| HIGH minus LOW | [−1/48, +1/16] |

Thus the relaxed interval crosses zero, so the unconstrained
marginal information alone does not identify a selection sign.

The biologically exact integer constraints change the answer.
A q=1/2 observation **cannot** pair with a fruit containing only
one initiated seed; it must pair with the count-2 (LOW) or
count-4 (HIGH) fruit. The other fruit has q=1:

- LOW viable counts: 0/12 and 1/12 -> mean **1/24**.
- HIGH viable counts: 0/12 and 2/12 -> mean **1/12**.
- HIGH minus LOW = **+1/24 = 0.041667**.

Only these pairings are integer-feasible; therefore a positive
finite-sample floral-fitness difference follows **without
recovering the actual fruit ID linkage**, under the complete
biological measurement assumptions.

The earlier 40-ovule two-world witness is retained as an
important *negative control*: its q×initiated values are
integer-feasible in either arrangement, so the integer-aware
procedure **still cannot identify the selection sign**.
Integer constraints help in some cases, not automatically.

## Ovule count need not be constant across fruits

In nature, ovule counts vary across flowers. The focal
*P. rex* 2016 source reports an average of **25.96 ovules,
SD 6.33** for its measured ovule sample. A method requiring
identical ovule numbers for all experimental fruits would have
limited field value.

The upgraded exact solver therefore also accepts **paired
ovule-and-initiated-seed counts per fruit**, with different
ovule counts on different fruits, while keeping the separate
predation fractions unpaired. It uses the integer check for
each candidate pairing and optimizes the **mean of individual
fruit's viable fractions**, rather than incorrectly pooling
viable counts over unequal ovule denominators.

Second synthetic demonstration:

- LOW initiation tuples (ovules, initiated): (12,1), (8,2)
- HIGH tuples: (15,1), (10,4)
- q margins both contexts: [1/2,1]

The only feasible assignments yield mean intact fraction
LOW = 1/16 = 0.0625 and HIGH = 1/10 = 0.10.
Thus HIGH−LOW = 3/80 = **+0.0375** while the relaxed
continuous matching interval still includes zero.

## Exact algorithm

For each setting and its set of n initiation fruits,
construct a bipartite graph:

- Left vertex: one real measured **(ovules, initiated)** pair.
- Right vertex: one unpaired exact **q fraction**.
- Allowed edge: initiated×q is an integer in [0,initiated].
- Edge payoff: (initiated−damaged)/ovules.

Enumerate all feasible perfect matchings by a memoized
bitmask dynamic programme. Retain the matching with the
**lowest** and the one with the **highest** sum of per-fruit
payoff fractions; divide by n. All calculations along each
edge and through the matching sums use Python's exact
rational-number arithmetic. The reported decimal interval
is the exact rational interval converted for presentation.

For n fruits the implementation is worst-case
O(n²2^n) time and O(n2^n) state-related memory.
We deliberately reject >14 fruits per setting until
a scalable flow/assignment optimization is implemented,
so there is no accidental exponential job in field production.

The algorithm returns explicit integer damaged/viable seed
counts for one attaining matching at each extreme. This is
an **existence witness**, not a reconstruction of which
natural fruit actually sustained that damage.

Brute-force enumeration over all permutations of a separate
four-fruit fixture is included in regression tests and must
recover exactly the same extrema. Impossible complete
matchings fail closed rather than silently rounding q.

## Exact rational recording is essential

The value q=1/3 should be supplied as the string "1/3".
A rounded decimal "0.3333333333333333" is **not** silently
replaced by 1/3, because doing so can change which
seed-count pairings are feasible.

This is a methodological consequence for future P. rex
field sheets: record the *number of damaged seeds and
the number of distinguishably initiated seeds*, not just
rounded predation percentages, and keep the fruit ID
and ovule count. If the fruit is fully eaten and initial
seed number is unknowable, q is not identified; such
records require a separate missingness/censoring analysis,
not integer matching by assumption.

## Use and examples

Existing equal-ovule benchmark:

    python scripts/bound_sch_integer_feasible_seed_stage_selection.py \
      data/SCH_INTEGER_SEED_COUPLING_SYNTHETIC_WITNESS_V1.json

Variable-ovule benchmark:

    python scripts/bound_sch_integer_feasible_seed_stage_selection.py \
      data/SCH_VARIABLE_OVULE_SEED_COUPLING_SYNTHETIC_WITNESS_V1.json

Tests:

    python -m pytest -q tests/test_sch_integer_feasible_seed_coupling.py

The JSON data_kind is SYNTHETIC_DEMONSTRATION for these
examples. If another dataset is labeled as observed,
positive field/season provenance and full-fate declarations
are required, but **those fields do not independently
authenticate the underlying measurements**. The machine
receipt explicitly carries a false
observed_field_data_independently_verified flag.

## Inference boundary

These are **sharp bounds on a finite set of empirically
possible observed-fraction pairings**, under the explicit
count and source assumptions. They are not confidence
intervals for the population, causal selection without
a randomized trait setting, or identified SCH pure
pollinator and antagonist function optima.

The method does not yet handle >14 fruit observations
per setting, unequal fruit weights, unrecognized predation
that destroys all seed coats, missing ovule counts, q
measured imprecisely, or partly overlapping rather
than full known marginal sets. A positive mathematical
sign is not evidence that P. rex itself exhibits the
particular predicted selection direction.

**Main ecological lesson:** absence of individual
fruit matching is sometimes *recoverable as a bounded
identification problem*. Biological count constraints
can materially change what is identifiable, so preserving
raw count granularity is informative even if some
record linkage fails.
