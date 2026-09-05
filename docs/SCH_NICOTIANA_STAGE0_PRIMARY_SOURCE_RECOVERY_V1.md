# SCH Nicotiana Stage-0 primary-source recovery v1

## Purpose

This audit asks how much of the *Nicotiana attenuata* Stage-0 promotion gate is already supported by primary literature, and which cells still require new work before the SCH `A x antagonist x pollinator` mechanism experiment can be interpreted.

The rule is fail-closed: programme-level coherence may establish biological reality and feasibility, but it cannot be assembled into the missing 8-cell causal table.

## Source set

### Kessler et al. 2015 — DOI 10.7554/eLife.07641

This experiment independently manipulated floral benzylacetone production and nectar production by RNAi and tested pollinator-mediated outcrossing and hawkmoth oviposition. In the native field experiment, CHAL scent-silenced plants produced only 22.9% of the outcrossed seeds produced by EV controls. In the same paper, CHAL plants received 43.1% of the *M. sexta* eggs received by EV plants in the field (`p=0.046`); the single-moth tent contrast was directionally weaker (`81.9%`, `p=0.096`). Nectar removal had an even larger oviposition effect.

Admitted SCH use:

```text
DIRECT_BA_TO_POLLINATOR_MEDIATED_OUTCROSSING
DIRECT_BA_TO_HAWKMOTH_OVIPOSITION_IN_FIELD
SAME_PROGRAMME_DUAL_AUDIENCE_RESPONSE
```

Important boundary: oviposition is an antagonist-response endpoint, not yet antagonist-mediated reproductive loss on the common `W` scale. The source supports a BA-associated antagonist response, but the effect is context-dependent in magnitude and should not be treated as a universal coefficient.

The same source also reports that the RNAi scent and nectar constructs targeted the intended pathways in an otherwise isogenic background and that transformed plants were morphologically indistinguishable from controls. This substantially strengthens `S0.1` feasibility, but the exact new execution manipulation still requires its own checks.

### Haverkamp et al. 2016 — DOI 10.7554/eLife.15039

This experiment provides a particularly useful SCH intervention component. Flowers were antherectomized, *M. sexta* proboscides were loaded with a standardized quantity of pollen using a fine brush, and mature capsules/seeds were measured after moth visitation. Pollen load was checked after trials and did not differ between EV and CHAL treatments.

Admitted SCH use:

```text
STANDARDIZED_MOTH_POLLEN_LOADING_FEASIBLE
ANTHERECTOMIZED_FLOWER_REPRODUCTIVE_ASSAY_FEASIBLE
BA_DEPENDENT_POLLINATION_SERVICE_TO_MATURE_SEED_RECOVERED
```

This is direct feasibility evidence for an experimentally controlled pollination pathway rather than a generic visitor-count proxy.

### Baldwin et al. / *N. attenuata* outcrossing work — field and tent pollination assays

Existing *N. attenuata* pollination experiments show that emasculation, hand pollination, pollinator exclusion and mature seed/viability scoring are all feasible. In free-flight moth arrays, females also laid eggs while visiting flowers; eggs were removed every afternoon while flower visitation and pollen transfer continued.

Admitted SCH use:

```text
POLLINATION_EXCLUSION_AND_HAND_POLLINATION_FEASIBLE
POST_OVIPOSITION_EGG_REMOVAL_FEASIBLE_DURING_MOTH_VISITATION
MATURE_SEED_AND_VIABILITY_ENDPOINT_FEASIBLE
```

The daily egg-removal precedent is especially important because it shows a practical route for preserving moth choice/oviposition behaviour while suppressing the downstream larval-damage pathway.

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
| `S0.1 stable A0/A1 chemical contrast` | **STRONG PARTIAL** | BA has been directly and selectively silenced in an otherwise isogenic background; scent and nectar were experimentally uncoupled and plants were morphologically indistinguishable | verify BA, nectar, floral timing/morphology and later `D` under the exact new intervention context |
| `S0.2 pollinator-side response to A` | **RECOVERED at programme level** | BA changes pollinator-mediated mature seed production; pollen-loading assays directly link BA to service quality | replicate only if execution context materially changes |
| `S0.3 antagonist-side response to same A` | **RECOVERED at programme level** | field BA silencing reduces *M. sexta* egg load; tent effect is weaker but directionally consistent | convert oviposition into antagonist-mediated loss on common `W` |
| `S0.4 workable P intervention` | **FEASIBILITY RECOVERED** | antherectomy, hand pollination, exclusion and standardized pollen loading of moth proboscides are established methods | combine a P manipulation with the G manipulation in the same registered design and verify no behavioural contamination |
| `S0.5 workable G intervention` | **FEASIBILITY RECOVERED** | eggs have been removed after natural moth oviposition while moth flower visitation continued; gentle egg removal before hatch is established in this system | validate that the chosen egg-removal schedule removes downstream damage without altering moth choice, A, or P |
| `S0.6 acceptable cross-channel contamination` | **PARTIAL / CRITICAL** | the component methods can be temporally separated: pollination exposure first, egg removal after oviposition | demonstrate in the combined pilot that pollen manipulation does not alter oviposition and egg removal does not alter pollination or subsequent A expression |
| `S0.7 one common W endpoint in all cells` | **STRONG PARTIAL** | mature capsules, seeds and seed viability are routinely recoverable | show that the combined P/G design produces interpretable variation in one identical `W` across all eight cells |

## Positive recovery

The Stage-0 audit therefore upgrades the system from a generic candidate to a source-grounded L0 candidate with both intervention components already demonstrated separately.

```text
BA -> pollinator-mediated mature reproduction: RECOVERED
BA -> antagonist oviposition response:          RECOVERED in field
standardized pollination manipulation:          FEASIBILITY RECOVERED
post-oviposition egg removal:                   FEASIBILITY RECOVERED
mature seed/capsule endpoint:                   FEASIBILITY RECOVERED
combined P/G selectivity:                       NOT YET TESTED
```

This is enough to justify the statement that the proposed shared-cue mechanism is biologically real in *N. attenuata*: an experimentally varied floral attraction coordinate affects both a mutualist-mediated reproductive route and an antagonist behavioural route.

It is not enough to claim functional SCH conflict, because the missing intersection is still:

```text
same A
x combined selective pollination manipulation
x combined selective antagonist-damage manipulation
-> one common reproductive W
```

## Main bottleneck after recovery

The dominant uncertainty is no longer whether benzylacetone is a plausible shared cue, nor whether the individual manipulation tools exist. The dominant uncertainty is **combined channel selectivity**.

A female *M. sexta* can pollinate and oviposit during the same foraging bout. Therefore the next experiment must manipulate pathways rather than assign the organism one permanent guild label.

A high-value candidate architecture is to use the established pollen-loading and egg-removal methods in the same experiment:

```text
A = EV/BA+ versus CHAL/BA-

P manipulation candidate
= standardized outcross-pollen availability / loading
  versus matched sham / suppressed focal pollination route

G manipulation candidate
= eggs retained through hatch and damage
  versus eggs counted then removed before hatch
```

The important feature is that `G=0` occurs **after** the moth has had the opportunity to use `A` for host/flower choice. Removing eggs before choice would erase the very antagonist-response pathway SCH is trying to measure.

The combined pilot must verify four contamination checks:

1. pollen loading/sham does not change oviposition probability or egg number;
2. egg-removal assignment cannot influence the moth's preceding flower choice or pollen delivery;
3. BA remains stable across P/G assignments before and during receiver exposure;
4. G retention changes damage enough to affect the declared reproductive scale.

If the P manipulation cannot be made without changing moth behaviour, a different pollinator receiver or a different biological system should be used rather than forcing the canonical decomposition.

## Reproductive endpoint decision

For SCH, the primary `W` should be a maternal reproductive endpoint that can be observed after all experimental routes have acted. The preferred order remains:

```text
1. mature viable seeds per standardized focal flower / plant allocation unit
2. capsule probability + seed number as decomposed secondary outcomes
3. earlier proxies only if mature reproduction is infeasible
```

The programme literature demonstrates that capsule and seed-related outcomes are feasible in this species. It does not yet demonstrate that BA-dependent oviposition has been causally translated into loss on that exact outcome under a selective egg-retention versus egg-removal contrast.

## Independent real-world method precedent

Theis & Adler 2012 (`10.1890/11-0825.1`) independently manipulated fragrance, pollination and florivores in *Cucurbita pepo* var. *texana* and measured seed production. Enhanced fragrance increased florivore attraction and reduced reproduction but did not increase pollinator attraction. This is useful as a real-world precedent that the three-factor ecological architecture is experimentally feasible, while also demonstrating why SCH must keep `M_A > 0` and `G_A > 0` as separate gates rather than assuming both from a total fitness effect.

Sánchez-Lafuente 2007 (`10.1093/aob/mcl267`) provides the complementary boundary: corolla manipulation altered pollinator visitation and fruit production but did not alter fruit-predator visitation. Together these studies show that the two channel responses can dissociate in nature.

## BITA consequence

The source recovery also sharpens the SCH -> BITA transition.

Kessler 2008 establishes that an attraction-by-nicotine-like reproductive surface exists, while Li 2017 shows that flower-specific defence biology is accessible. Li 2018 simultaneously warns that upstream JA manipulation can move attraction/reward traits. Therefore BITA should not add `D` until SCH has frozen the BA `A` coordinate and a downstream `D` candidate has passed orthogonality checks.

The ordering remains:

```text
SCH Stage 0/1
freeze BA A
combine validated P and G pathway manipulations
pilot A x G x P

then BITA
add one independently validated flower-associated D
A x D x G x P
```

## Updated status

```text
FIRST_CHOICE_SYSTEM: NICOTIANA_ATTENUATA
L0_SHARED_COORDINATE_REALITY: SUPPORTED_AT_PROGRAMME_LEVEL
S0.1_COORDINATE_STABILITY: STRONG_PARTIAL
S0.2_POLLINATOR_RESPONSE: RECOVERED
S0.3_ANTAGONIST_RESPONSE: RECOVERED_FIELD
S0.4_P_INTERVENTION: FEASIBILITY_RECOVERED
S0.5_G_INTERVENTION: FEASIBILITY_RECOVERED
S0.6_COMBINED_SELECTIVITY: OPEN_CRITICAL_GATE
S0.7_COMMON_W: STRONG_PARTIAL
COMPLETE_SCH_CHANNEL_IDENTIFICATION: NOT_YET_EXECUTED
```

## Next valid work

Do not spend the next cycle re-establishing that BA can affect both audiences or inventing new intervention classes from scratch. The high-information next work is a **combined selectivity pilot** using the already established manipulation components, with contamination checks registered before the full 8-cell analysis.

If combined selectivity passes, *Nicotiana* should be promoted immediately to the balanced 8-cell mechanism pilot. If it fails after a serious attempt, retain *Nicotiana* as real-world L0 evidence and move the confirmatory SCH decomposition to the next candidate system.