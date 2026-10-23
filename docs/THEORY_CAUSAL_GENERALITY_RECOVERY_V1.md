# SCH theory -> causal -> generality recovery spine v1

## Independent question

SCH asks whether competing functions forced onto **one shared trait coordinate** generate a real compromise geometry and where that compromise settles.

PAYOFF population frequency, invasion, coexistence and `eta` are explicitly outside this spine.

---

# T — Theory

## T1. Shared-coordinate optimum

For two functions with distinct preferred states on one coordinate `z`, the quadratic baseline is

```text
z* = (w1 theta1 + w2 theta2)/(w1+w2)
L  = [w1 w2/(w1+w2)](theta1-theta2)^2.
```

The result is now generalized beyond two functions and beyond quadratic loss. For strictly convex function losses `ell_i(z)` with positive weights,

```text
J(z) = sum_i w_i ell_i(z)
```

has one shared optimum inside the convex hull of the function-specific optima. Its exact log-weight sensitivity is

```text
d z*/d log(w_j)
= - w_j ell_j'(z*) / sum_i w_i ell_i''(z*).
```

Therefore increasing one function's relative weight moves the shared optimum toward that function's own optimum. A common positive rescaling of all function weights leaves `z*` unchanged.

Status: `GENERAL_N_FUNCTION_STRICT_CONVEX_THEORY_PROVED_UNDER_DECLARED_ASSUMPTIONS`.

## T2. Operational conflict budget

Map the theoretical loss to a measurable fitness-scale component budget using the factorial causal surfaces while preserving the distinction between state-specific and pure-function optima.

Status: `IMPLEMENTED_THEORY_TO_ESTIMAND_BRIDGE`.

## T3. Falsifiable signatures

A real one-axis conflict predicts, under selective functional interventions:

```text
function-facing state optima differ;
removing / weakening one functional demand moves the optimum toward the other;
the combined optimum can occupy an interior compromise;
component gradients around the combined optimum oppose one another.
```

The n-function theorem adds a stronger comparative-static signature: each selectively increased functional weight must shift the common optimum toward that function's own preferred state while all else remains fixed.

Status: `REGISTERED`.

### Theory claim ceiling

The mathematics establishes existence/geometry **conditional on the model assumptions**. It does not establish that any natural system actually has conflicting function-specific optima or that changing environment alters only one weight while leaving the loss family fixed.

---

# C — Causal validation

## C0. Trait-manipulation qualification

Validate that the shared coordinate can be moved over multiple levels without silently moving the reserved second axis or unrelated morphology.

Primary Pedicularis gate: `SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1`.

Status: `ANALYZER_IMPLEMENTED_EMPIRICAL_EXECUTION_PENDING`.

## C1. Selective functional interventions

Validate independent perturbations for the two functional demands.

For the current Pedicularis route:

```text
P = pollination-weight intervention
G = independent seed-predator intervention
water-y = fixed
```

Status: `METHOD_CONTRACTS_IMPLEMENTED_EMPIRICAL_EXECUTION_PENDING`.

## C2. Full causal surface

Run the multi-level:

```text
z x P x G
```

surface in one frozen population x season x fitness scale and recover `z_P*`, `z_G*`, `z_C*` with uncertainty.

Status: `ANALYZER_IMPLEMENTED_NOT_YET_EXECUTED`.

## C3. Fitness-scale conflict receipt

Require a positive bounded conflict budget `L` on the registered reproductive-fitness scale, then export the context-locked handoff to later chapters.

Status: `ANALYZER_AND_INTERFACE_IMPLEMENTED_NOT_YET_EXECUTED`.

### Causal success criterion

SCH is causally supported in a focal system only when **selective interventions move the optimum of the same trait coordinate in the predicted opposed directions and a positive conflict budget is recovered on the same causal surface**.

---

# G — Generality

## G0. Same-system causal existence proof

Primary current route: `Pedicularis rex`.

A positive Pedicularis result establishes that the mechanism can exist in nature. It does not establish universality.

Status: `PREFERRED_ROUTE_NOT_YET_EXECUTED`.

## G1. Independent floral replications

Test recurrence of the **shared-coordinate conflict geometry**, not recurrence of one pollination-defence mechanism.

Current complementary candidates / roles:

```text
Dalechampia              strong existing compromise geometry; causal selectivity still incomplete
Castilleja linariaefolia short antagonist-to-fitness fallback; manipulations incomplete
Nicotiana attenuata      high-information shared-cue mechanism bridge; clean optimum surface incomplete
Polemonium viscosum      broader pollination-physiology conflict candidate
```

Negative / boundary controls are required:

```text
Ipomopsis aggregata      near-monotonic / negative control role
Platycodon grandiflorus  aligned-function optimum control
```

Status: `CANDIDATE_SET_REGISTERED_REPLICATION_INCOMPLETE`.

## G2. Cross-domain generality

Cross-domain candidates now include Darwin finch beak/jaw performance constraints and the Salmonella HisA/TrpF adaptive-conflict system. These support biological reality of shared multifunctional constraints, but neither is currently a registered SCH optimum-shift causal replication on the same scalar coordinate.

Status: `CROSS_DOMAIN_CANDIDATES_RECOVERED_CAUSAL_REPLICATION_NOT_YET_CLOSED`.

### Generality promotion rule

Do not use literature count alone. Promotion requires recurrence of the defining geometry under appropriately matched estimands, explicit negative/boundary systems, and clear separation of causal experiments from observational anchors.

---

# Current bottleneck

```text
theory                         n-function convex comparative statics now proved
causal analysis machinery      implemented
same-system causal biology     NOT YET EXECUTED
cross-system generality        candidate map expanded; causal replication incomplete
```

The next scientific gate is empirical Pedicularis method qualification and the same-context `z x P x G` surface, not additional PAYOFF game theory.
