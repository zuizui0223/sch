# Nicotiana programme composite bridge v1

## Decision

The *Nicotiana attenuata* literature is the strongest current programme-level bridge between SCH's one-trait shared-cue question and BITA's second-trait outcome question.

```text
PROGRAM_COMPOSITE_NEAR_COMPLETE
DIRECT_COMPLETE_CHAIN_NOT_ESTABLISHED
```

The word **programme** is essential. The required links occur in different primary studies and cannot be combined as though they were one experimental table.

## Source roles

### Kessler et al. 2015 — receiver overlap on attraction coordinates

Kessler et al. (2015; DOI `10.7554/eLife.07641`) experimentally uncoupled floral benzylacetone and nectar production. It provides direct same-system evidence that manipulated attraction/reward coordinates affect pollinator-mediated outcrossing and hawkmoth oviposition.

Admitted SCH role:

```text
DIRECT_A_TO_POLLINATOR_RESPONSE
DIRECT_A_TO_ANTAGONIST_RESPONSE
PROGRAM_LEVEL_SHARED_RECEIVER_TRACKING
```

Claim ceiling:

- oviposition is not itself antagonist-mediated reproductive loss on the same scale as outcrossing;
- the study does not supply one common decomposed `W(A)` for both channels;
- it does not contain a second antagonist-reducing trait crossed with the same `A`.

### Kessler, Gase & Baldwin 2008 — second-trait reproductive surface

Kessler et al. (2008; DOI `10.1126/science.1160072`) crossed benzylacetone and nicotine production in all four combinations and measured reproductive and visitor outcomes.

Admitted bridge role:

```text
DIRECT_AxD_LIKE_REPRODUCTIVE_SURFACE
POSITIVE_AGGREGATE_INTERACTION_SIGN_ANCHOR
```

Claim ceiling:

- exact source/design-based interaction uncertainty is not recovered;
- systemic nicotine suppression does not establish a flower-restricted `D`;
- the published rounded surface gives a positive interaction pattern but does not by itself establish that attraction changed from non-beneficial or negative to positive;
- the design does not allocate antagonist relief, pollinator interference or an independent joint cost.

### Li et al. 2017 — flower-specific defence candidate

Li et al. (2017; DOI `10.1073/pnas.1703463114`) identifies flower-specific jasmonate-regulated constitutive defence biology.

Admitted bridge role:

```text
FLOWER_SPECIFIC_DEFENCE_TOOL_CANDIDATE
```

Claim ceiling:

- a signalling sector is not one declared `D` coordinate;
- one downstream output must be validated as antagonist-reducing;
- that intervention must preserve benzylacetone, nectar, vegetative defence and floral development sufficiently to keep `A` invariant.

### Li et al. 2018 — coordinate-stability warning

Li et al. (2018; DOI `10.1111/jipb.12607`) shows that upstream jasmonate perturbation changes attraction/reward outputs together with florivore attack or damage.

Admitted bridge role:

```text
PLEIOTROPY_AND_COORDINATE_STABILITY_WARNING
```

It cannot be treated as an independently crossed `D` manipulation when the intervention also changes `A`.

## What the programme currently answers

The programme supports all of the following existence statements:

1. an experimentally varied attraction coordinate can affect pollinator service;
2. the same plant system contains antagonist tracking of attraction/reward coordinates;
3. a manipulated attraction-by-defence-like reproductive surface exists;
4. flower-specific defence biology is experimentally accessible.

These statements make the chain biologically and experimentally plausible. They do not close the chain.

## Missing same-experiment intersection

A direct SCH-to-BITA bridge still requires one experiment containing:

```text
one invariant manipulated A
+ one independently validated flower-specific D
+ pollinator response to the same A contrast
+ antagonist response and antagonist-mediated loss
+ one common plant reproductive outcome in all four A×D cells
+ A0, A1 and Delta_AD W with compatible uncertainty
```

For the four reproductive cells,

```text
A0 = W10 - W00
A1 = W11 - W01
Delta_AD W = A1 - A0
```

The outcome hierarchy is:

```text
Delta_AD W > 0       positive interaction relief
A0 <= 0 and A1 > 0   constraint release
A0 < 0 and A1 > 0    strict negative-to-positive reversal
```

Only the first inequality is implied by a positive total interaction. Neither it nor a zero crossing demonstrates cue privacy.

## Minimum chain-closing experiment

Use a benzylacetone manipulation as the declared `A` only after confirming that its contrast is stable across `D` states. Select one downstream flower-specific defence output as `D` only after showing that it reduces the focal antagonist route and does not materially move the `A` coordinate.

Within matched blocks, cross:

```text
A0D0  A1D0  A0D1  A1D1
```

Record in the same trial:

- pollinator approach, visitation and pollen-transfer/service proxy;
- hawkmoth or other focal antagonist approach, oviposition, robbing or florivory;
- damage or loss linking antagonist response to the declared reproductive outcome;
- the common reproductive endpoint.

This first four-cell experiment can close:

1. the SCH linked shared-coordinate test;
2. the BITA interaction-relief test;
3. the stronger constraint-release or strict-reversal test if `A0` and `A1` cross the registered boundaries.

It does not yet allocate the mechanism.

## Selectivity warning

In this system a hawkmoth can contribute both pollination and oviposition. Role labels therefore cannot be converted automatically into selective pollinator and antagonist interventions.

Before a full crossed consumer design, pilot whether guild, timing, access route, hand-pollination standardization or focal oviposition exclusion can alter one channel without changing the other channel or the declared `A` and `D` coordinates. If selectivity fails, retain a coupled receiver-role model rather than forcing a separable BITA decomposition.

## No-pooling contract

Do not:

- combine Kessler 2015 response estimates with Kessler 2008 reproductive cells as one effect estimate;
- treat Li 2017 defence biology as the `D` level of either Kessler experiment;
- use Li 2018 upstream JA manipulation as an orthogonal `D` when it changes attraction/reward outputs;
- infer antagonist-mediated reproductive loss from oviposition alone;
- infer constraint release from `Delta_AD W > 0` alone.

## Relationship to the two repositories

SCH uses this programme as a bounded candidate for a direct shared-coordinate conflict experiment. BITA uses it as the leading candidate for a four-cell outcome surface and later channel-allocation programme.

The detailed BITA design is maintained in:

```text
docs/NICOTIANA_SCH_BITA_CHAIN_CLOSURE_V1.md
```

The two records must retain the same status:

```text
PROGRAM_COMPOSITE_NEAR_COMPLETE
DIRECT_COMPLETE_CHAIN_NOT_ESTABLISHED
```
