# SCH Nicotiana Stage-0 primary-source recovery v1

## Purpose

This audit asks how much of the *Nicotiana attenuata* Stage-0 promotion gate is already supported by primary literature, and which cells still require new work before the SCH `A x antagonist x pollinator` mechanism experiment can be interpreted.

The rule is fail-closed: programme-level coherence may establish biological reality and feasibility, but it cannot be assembled into the missing 8-cell causal table.

## Source set

### Kessler et al. 2015 — DOI 10.7554/eLife.07641

This experiment independently manipulated floral benzylacetone production and nectar production by RNAi and tested pollinator-mediated outcrossing and hawkmoth oviposition. The paper reports that both scent and nectar increased outcrossing across separately tested pollinators and both increased hawkmoth oviposition, with nectar contributing more strongly to oviposition.

Admitted SCH use:

```text
DIRECT_BA_TO_POLLINATOR_MEDIATED_OUTCROSSING
DIRECT_BA_TO_HAWKMOTH_OVIPOSITION
SAME_PROGRAMME_DUAL_AUDIENCE_RESPONSE
```

Important boundary: oviposition is an antagonist-response endpoint, not yet antagonist-mediated reproductive loss on the common `W` scale.

### Kessler, Gase & Baldwin 2008 — DOI 10.1126/science.1160072

This field experiment blocked the dominant floral attractant benzylacetone and nectar nicotine in all four combinations. The study measured floral visitation, florivory, nectar robbing, outcrossing-related reproductive outcomes and plant reproduction. Both floral attractant and nicotine were required for maximal capsule production and seed siring in emasculated flowers, while nicotine reduced florivory and nectar robbing.

Admitted SCH/BITA use:

```text
DIRECT_MANIPULATED_BA_AXIS
COMMON_REPRODUCTIVE_ENDPOINT_FEASIBILITY
DIRECT_AxD_LIKE_FIELD_SURFACE
ANTAGONIST_DAMAGE_ROUTE_EXISTS
```

Important boundary: this is an `A x D`-like reproductive surface, not a selective `A x G x P` decomposition. Nicotine suppression is also systemic rather than a clean consumer exclusion.

### Li et al. 2017 — DOI 10.1073/pnas.1703463114

This study identifies a flower-specific jasmonate sector controlling constitutive floral defence. A flower-specific JAZ regulator affects defensive compounds, and altered floral defence changes resistance to tobacco budworm attack.

Admitted programme use:

```text
FLOWER_SPECIFIC_DEFENCE_BIOLOGY_REAL
FLORIVORE_DAMAGE_CAN_BE_EXPERIMENTALLY_MODIFIED
BITA_D_CANDIDATE_SEARCH_SPACE
```

Boundary: the signalling sector is not itself an orthogonal `D` coordinate, and it does not supply a SCH `G` intervention.

### Li et al. 2018 — DOI 10.1111/jipb.12607

Field manipulation of jasmonate signalling shows that weakening JA signalling changes floral advertisement/reward traits, including benzylacetone and nectar, while also increasing florivore attack and floral damage.

Admitted use:

```text
PLEIOTROPY_WARNING
A_COORDINATE_STABILITY_WARNING
REAL_WORLD_FLORAL_DAMAGE_ROUTE
```

This source blocks the use of broad upstream JA perturbation as a clean independent `D` or `G` intervention when the intervention also moves `A`.

## Stage-0 gate recovery

The current evidence state is:

| Gate | Status | What is recovered | What remains |
|---|---|---|---|
| `S0.1 stable A0/A1 chemical contrast` | **PARTIAL** | BA has been directly manipulated, including independently from nectar in Kessler 2015 | verify the exact chosen BA manipulation leaves nectar, floral morphology, timing and later `D` invariant in the new experiment |
| `S0.2 pollinator-side response to A` | **RECOVERED at programme level** | BA manipulation changes pollinator-mediated outcrossing | replicate/validate under the exact Stage-0 execution context if the new intervention differs |
| `S0.3 antagonist-side response to same A` | **RECOVERED at programme level** | the same BA axis changes hawkmoth oviposition | convert antagonist response into a reproductive-loss pathway rather than stopping at oviposition |
| `S0.4 workable P intervention` | **PARTIAL FEASIBILITY** | separate pollinator assays and emasculated/controlled reproductive work show pollination can be experimentally handled | demonstrate a selective P on/off intervention while leaving G and A acceptably unchanged |
| `S0.5 workable G intervention` | **OPEN** | florivory/oviposition routes and defensive control are biologically tractable | identify a true antagonist-pathway intervention rather than using defence genotype as a proxy for G absence |
| `S0.6 acceptable cross-channel contamination` | **OPEN** | source literature exposes the problem explicitly | run intervention checks; hawkmoth dual roles make this the main bottleneck |
| `S0.7 one common W endpoint in all cells` | **PARTIAL FEASIBILITY** | capsule production, seed siring and outcrossing-related endpoints have been measured experimentally | select one outcome measurable identically across all eight SCH cells and link G exposure to loss on that scale |

## Positive recovery

The Stage-0 audit therefore upgrades the system from a generic candidate to a source-grounded L0 candidate.

```text
BA -> pollinator-mediated reproduction: RECOVERED
BA -> antagonist oviposition response:   RECOVERED
same manipulated attraction axis:        RECOVERED at programme level
floral antagonist damage route:          RECOVERED
common reproductive outcomes feasible:   RECOVERED as feasibility
```

This is enough to justify the statement that the proposed shared-cue mechanism is biologically real in *N. attenuata*: an experimentally varied floral attraction coordinate affects both a mutualist-mediated reproductive route and an antagonist behavioural route.

It is not enough to claim functional SCH conflict, because the missing intersection is still:

```text
same A
x selective pollinator pathway
x selective antagonist pathway
-> one common reproductive W
```

## Main bottleneck after recovery

The dominant uncertainty is no longer whether benzylacetone is a plausible shared cue. The dominant uncertainty is **channel selectivity**.

A hawkmoth can act as both pollinator and ovipositing antagonist. Therefore the next experiment must manipulate pathways rather than assign the organism one permanent guild label.

The preferred Stage-0B ordering is:

1. standardize or experimentally set pollination independently of natural visitor identity;
2. alter oviposition/egg establishment or subsequent antagonist damage after the pollination state is fixed;
3. verify that the G intervention does not alter BA emission, nectar or the standardized P treatment;
4. verify that the P treatment does not itself change antagonist exposure except through the predeclared biological pathway.

Candidate G interventions should be judged by their causal target:

```text
GOOD TARGET
oviposition / egg establishment / early antagonist damage pathway

NOT SUFFICIENT AS G=0
upstream plant defence genotype that changes A or multiple visitor-facing traits
```

## Reproductive endpoint decision

For SCH, the primary `W` should be a maternal reproductive endpoint that can be observed after all experimental routes have acted. The preferred order remains:

```text
1. mature viable seeds per standardized focal flower
2. capsule probability + seed number as decomposed secondary outcomes
3. earlier proxies only if mature reproduction is infeasible
```

The programme literature demonstrates that capsule and seed-related outcomes are feasible in this species. It does not demonstrate that antagonist oviposition has already been causally translated into loss on that exact outcome under a selective G intervention.

## BITA consequence

The source recovery also sharpens the SCH -> BITA transition.

Kessler 2008 establishes that an attraction-by-nicotine-like reproductive surface exists, while Li 2017 shows that flower-specific defence biology is accessible. Li 2018 simultaneously warns that upstream JA manipulation can move attraction/reward traits. Therefore BITA should not add `D` until SCH has frozen the BA `A` coordinate and a downstream `D` candidate has passed orthogonality checks.

The ordering remains:

```text
SCH Stage 0/1
freeze BA A
identify P and G pathways
pilot A x G x P

then BITA
add one independently validated flower-associated D
A x D x G x P
```

## Updated status

```text
FIRST_CHOICE_SYSTEM: NICOTIANA_ATTENUATA
L0_SHARED_COORDINATE_REALITY: SUPPORTED_AT_PROGRAMME_LEVEL
S0.2_POLLINATOR_RESPONSE: RECOVERED
S0.3_ANTAGONIST_RESPONSE: RECOVERED
S0.1_COORDINATE_STABILITY: PARTIAL
S0.4_P_INTERVENTION: PARTIAL_FEASIBILITY
S0.5_G_INTERVENTION: OPEN
S0.6_SELECTIVITY: OPEN_CRITICAL_GATE
S0.7_COMMON_W: PARTIAL_FEASIBILITY
COMPLETE_SCH_CHANNEL_IDENTIFICATION: NOT_YET_EXECUTED
```

## Next valid work

Do not spend the next cycle re-establishing that BA can affect both audiences. The high-information next work is to close `S0.4-S0.6` and the antagonist-response-to-reproductive-loss link.

If those gates pass, *Nicotiana* should be promoted immediately to a small balanced 8-cell mechanism pilot. If they fail after a serious selectivity test, retain *Nicotiana* as real-world L0 evidence and move the confirmatory SCH decomposition to the next candidate system.