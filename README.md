# Shared Trait Compromise / SCH

SCH is the **functional-conflict identification paper** in the SCH–SLK–BITA programme.

Its central claim boundary is:

```text
multifunctionality != identified functional conflict
```

A second, stricter boundary is:

```text
state-specific reproductive optimum != pure-function optimum
```

The active paper asks what evidence is required before a multifunctional trait may legitimately be described as causally constrained by opposing functional demands.

## Canonical question

> **When multiple functions use one phenotypic coordinate, when has true functional conflict been identified rather than merely multifunctionality or context dependence?**

## Theory target

At the theory level, one shared coordinate `z` contributes to two functions:

```text
W_shared(z) = w1 F1(z) + w2 F2(z) - C(z)
```

with pure function-specific optima

```text
z_F1* = argmax F1(z)
z_F2* = argmax F2(z).
```

Theory-level conflict is

```text
z_F1* != z_F2*.
```

Under the local quadratic benchmark,

```text
L_compromise,theory*
  = [a b / (a + b)] (z_F1* - z_F2*)^2.
```

This is a theory benchmark and an optional downstream handoff quantity. It is not an instruction to relabel experimental state optima as pure-function optima.

## What the experiment directly identifies

The multi-level crossed experiment fits

```text
W00(z) = P0 G0
W10(z) = P1 G0
W01(z) = P0 G1
W11(z) = P1 G1.
```

It directly identifies state-specific reproductive optima

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

In general,

```text
z_P* != automatically z_F1*
z_G* != automatically z_F2*.
```

Direct/background effects of `z` can remain in every consumer state.

## Promotion ladder

SCH uses an explicit evidence ladder:

```text
L0  multifunctionality
L1  local functional conflict
L2  state-specific compromise geometry
L3  causal compromise
L4  context-stable component-optimum promotion
```

A strong causal compromise result requires:

```text
z_P* != z_G*
combined W11(z) has a supported interior z_C*
G off -> optimum shifts toward z_P*
P off -> optimum shifts toward z_G*
opposing functional-component gradients near z_C*.
```

The zero derivative of a fitted interior optimum at its own vertex is not independent evidence of balance.

## Pure-function promotion gate

Use component contrasts from the same selective `z x P x G` experiment:

```text
M_G0(z) = W10(z) - W00(z)
M_G1(z) = W11(z) - W01(z)
H_P0(z) = W01(z) - W00(z)
H_P1(z) = W11(z) - W10(z).
```

Only if the pollinator-component optima agree across antagonist states and the antagonist-component optima agree across pollinator states, inside a prospectively frozen equivalence bound with uncertainty support, may SCH promote them to context-stable empirical `z_F1*` and `z_F2*`.

If they differ by context, retain conditional component optima. Do not force the pure-function label.

## Critical negative control

```text
multifunctionality = true
functional conflict = false
```

is a valid and important outcome when both functions favor the same trait state. Aligned-optimum systems are therefore part of the SCH test, not inconvenient exceptions.

## Real-world evidence role

The literature and PRISMA programme provide ecological grounding. They show that shared traits affect multiple functions, opposing demands and compromise-like outcomes occur, and changing interaction regimes can redirect evolution.

They do **not** by themselves identify the SCH estimands in one biological system.

Current bounded status:

```text
REAL_WORLD_MULTIFUNCTIONALITY_RECOVERED
CASE_LEVEL_OPPOSING_DEMANDS_RECOVERED
CASE_LEVEL_COMPROMISE_RECOVERED
STATE_SPECIFIC_CAUSAL_COMPROMISE_ANALYZER_READY
PURE_FUNCTION_PROMOTION_GATE_READY
COMPLETE_CAUSAL_COMPROMISE_EXPERIMENT_NOT_YET_EXECUTED
PURE_FUNCTION_OPTIMA_NOT_IDENTIFIED_BY_DEFAULT
```

## Comparative macroecology extension

SCH now also carries an active comparative ecological layer built from the same identification rules.

Current bounded state:

~~~text
current primary-study inclusions         153
canonical biological trait axes           50

static fixed-role resolved axes            19
  conflict                                  9
  reinforcement                             2
  one-sided / null                          8

broad materialized H2 local cases          49

TOTAL_SELECTION_EFFECT family
  cases                                    81
  trait axes                               31
  independent programmes                    8
  registered estimand-family gate        PASS

strict STANDARDIZED_SELECTION_GRADIENT family
  cases                                    61
  trait axes                               26
  independent programmes                    6
  strict numeric pooling gate            FAIL

repeated TOTAL_SELECTION_EFFECT axes        27
  no point reversal                         13
  point-estimate sign switch                14
    bidirectional uncertainty-supported      3
    one-side supported                       5
    both-sides unsupported                   5
    uncertainty unresolved                   1

H1 modelability = FAIL_CLOSED
H2 breadth gate = PASS
H2 estimand-family breadth gate = PASS
H2 strict numeric-pooling gate = FAIL_CLOSED

H2M1-V3 prospective reversal holdout
  development programmes excluded             8
  frozen active source pool                  456
  held-out programmes registered              4
  complete primary outcomes                    3
    single modifier                            3
    multi-component                            0 complete
  single-modifier q_j                    0, 0, 2/3
  primary test                              CLOSED
  spatial mosaics             EXTERNAL_REPLICATION
  opening gate                 DESIGN_BREADTH_ONLY
~~~

All four V26 studies now have source-axis coverage; three have V27 numeric outcome adjudication. The four new coverage rows remain composite, so the canonical geometry ledger stays at 50 axes until individual-axis canonicalization.

V28 adds four more formal primary studies from the frozen TA1 tier. Design-only recoding yields 57 P1 records, 39 H1 record-level candidates and 64 source-axis evidence rows; only Vaccinium 000429 adds a new same-coordinate H1 source axis. The canonical ledger remains at 50 axes.

V29 adds three more primary studies but no new H1 trait geometry. Lonicera 000540 becomes a second BENEFIT_COST_COUPLED role-boundary case because the same nectar robber both cross-pollinates and reduces legitimate visitation.

V30 adds four more primary studies without adding an H1 trait geometry. Sesamum 000546 becomes a third BENEFIT_COST_COUPLED / role-dependent case, while Clinopodium 000549 adds joint elevational geographic and receiver-assemblage context. P1 rises to 64, but the H1 record frontier remains 39.

V31 adds three primary studies plus one explicit duplicate-report exclusion. P1 rises to 67 while the H1 record frontier remains 39: Digitalis robbery, Lonicera aphid herbivory and Brassica ontogeny × herbivore treatments are interaction-context experiments rather than matched two-function response surfaces on one floral trait coordinate.

V32 completes the TA1 full-text tier. Four more primary studies raise P1 to 71, but the H1 record frontier remains 39. Iris 000663 and Primula 000729 expand benefit-cost/role-boundary evidence, Salvia 000736 adds spatiotemporal robbery context, and Brassica incana 000839 adds a 15-population urbanization context without a matched same-trait two-function geometry.

V33 closes the complete frozen TA2 repeated-context title/abstract tier: 20 records screened, 14 retained for full text and 6 excluded. Formal title/abstract screening now covers 483/868 records; 385 remain unscreened.

V34 closes the first TA2 full-text batch: Isoplexis enters broad P1 but not H1, Tribulus enters EVOLUTIONARY_OUTCOME, the Solanum preprint is removed as a duplicate, and the published Solanum study becomes a P2 pollination-service/pollen-consumption boundary. Primary studies rise to 145 while the H1 frontier remains 39.

V35 closes the second TA2 full-text batch. Sabatia becomes a P2 both-response/no-common-fitness case, Hakea enters EVOLUTIONARY_OUTCOME, Silene-Hadena is antagonist-side only in the focal source, and the scent synthesis is excluded from the primary count. Primary studies reach 148 while H1 remains 39.

V36 closes the third TA2 full-text batch. Anemone adds a benefit-cost role boundary, the leafflower study adds a 16-population pollinator-cheater mosaic, and Camissoniopsis adds spatial context to an already represented biological programme. Primary studies reach 152, P1=74 and H2-context=31 while H1 remains 39.

V37 completes the TA2 full-text tier. The Mimulus dissertation is retained as composite P2 evidence because its pollinator and herbivore responses occur in separate experiments without a common reproductive endpoint; the BioScience synthesis is excluded from the primary count. Primary studies reach 153, P2=20, and H1 remains 39.

V38 begins the deterministic TA3 remainder with review orders 78–102: 25 records screened, 14 retained and 11 excluded. Formal title/abstract screening now covers 508/868 records; 360 remain unscreened.

V39 closes the second deterministic TA3 batch, review orders 103–127: 25 records screened, 10 retained and 15 excluded. Formal title/abstract screening reaches 533/868; 335 remain unscreened.

V40 closes the third deterministic TA3 batch, review orders 128–152: 25 records screened, 13 retained and 12 excluded. Formal title/abstract screening reaches 558/868; 310 remain unscreened. The retained set includes nursery-pollinator, pollinator-exploiter, herbivory-mediated fitness and pollination–seed-predation boundary systems.

V41 closes the fourth deterministic TA3 batch, review orders 153–177: 25 records screened, 7 retained and 18 excluded. Formal title/abstract screening reaches 583/868; 285 remain unscreened. The retained set includes a two-factor pollinator × herbivore common-fitness experiment, trait-dependent legitimate/robbing hummingbird behaviour, fig mutualism top-down control and nectar-chemistry multi-consumer systems.

V42 closes the fifth deterministic TA3 batch, review orders 178–202: 25 records screened, 19 retained and 6 excluded. Formal title/abstract screening reaches 608/868; 260 remain unscreened. The retained set is enriched for nectar chemistry, role-coupled pollinators, robbery systems and comparative pollination-herbivory studies.

V43 closes the sixth deterministic TA3 batch, review orders 203–227: 25 records screened, 10 retained and 15 excluded. Formal title/abstract screening reaches 633/868; 235 remain unscreened. Negative controls such as Dalechampia seed-predator non-constraint and Erythronium pollen-colour one-sided effects remain in the retained set.

The current biological synthesis is:

> realized multifunctional geometry depends on trait axis × ecological context × consumer functional role.

V3 corrects the prospective source boundary to the 456 records still formally unscreened at V24 close; seven records already screened in V21/V23 remain in the PRISMA denominator but are excluded from the prospective source pool.

The macroecology layer is an **active upgrade path**, not a reason to delay the frozen New Phytologist Viewpoint. It becomes a candidate full comparative paper only after the systematic denominator is completed and an H1 or plant-performance H2 modelability gate passes.

See:

- `docs/SCH_MACROECOLOGY_ECOLOGICAL_SYNTHESIS_V1.md`
- `data/SCH_MACROECOLOGY_CANONICAL_TRAIT_AXIS_LEDGER_V1.csv`
- `docs/SCH_MACROECOLOGY_H2_MODELABILITY_V6.md`
- `docs/SCH_H2_GYMNADENIA_A2_RECOVERY_V1.md`
- `docs/SCH_H2_TRIFOLIUM_RECOVERY_V1.md`
- `docs/SCH_H2_ERYSIMUM_TABLE5_RECOVERY_V1.md`\n- `docs/SCH_H2_POLYGALA_TANACETUM_RECOVERY_V1.md`
- `docs/SCH_H2_ESTIMAND_GATE_PASS_V9.md`
- `docs/SCH_H2_DIRECTIONAL_CONTEXT_ANALYSIS_V10.md`
- `docs/SCH_H2_SWITCH_MECHANISM_TAXONOMY_V11.md`
- `docs/SCH_H2_REVERSAL_HOLDOUT_PROTOCOL_V1.md` — superseded pre-data protocol provenance
- `docs/SCH_H2_REVERSAL_HOLDOUT_PROTOCOL_V2.md` — superseded source-pool boundary
- `docs/SCH_H2_REVERSAL_HOLDOUT_PROTOCOL_V3.md` — active prospective contract
- `docs/SCH_H2_HOLDOUT_V26_DESIGN_FREEZE.md` — first four held-out programmes, design-only
- `docs/SCH_H2_HOLDOUT_V27_OUTCOME_READOUT.md` — first three held-out outcomes
- `docs/SCH_PRISMA_V28_TA1_FULLTEXT_BATCH_A_READOUT.md` — first TA1 full-text batch
- `docs/SCH_PRISMA_V29_TA1_FULLTEXT_BATCH_B_READOUT.md` — second TA1 full-text batch
- `docs/SCH_PRISMA_V30_TA1_FULLTEXT_BATCH_C_READOUT.md` — third TA1 full-text batch
- `docs/SCH_PRISMA_V31_TA1_FULLTEXT_BATCH_D_READOUT.md` — fourth TA1 full-text batch
- `docs/SCH_PRISMA_V32_TA1_FULLTEXT_CLOSURE_READOUT.md` — final TA1 full-text closure
- `docs/SCH_PRISMA_V33_TA2_HOLDOUT_READOUT.md` — complete TA2 title/abstract screening
- `docs/SCH_PRISMA_V34_TA2_FULLTEXT_BATCH_A_READOUT.md` — first TA2 full-text batch
- `docs/SCH_PRISMA_V35_TA2_FULLTEXT_BATCH_B_READOUT.md` — second TA2 full-text batch
- `docs/SCH_PRISMA_V36_TA2_FULLTEXT_BATCH_C_READOUT.md` — third TA2 full-text batch
- `docs/SCH_PRISMA_V37_TA2_FULLTEXT_CLOSURE_READOUT.md` — complete TA2 full-text closure
- `docs/SCH_PRISMA_V38_TA3_BATCH_A_READOUT.md` — first deterministic TA3 batch
- `docs/SCH_PRISMA_V39_TA3_BATCH_B_READOUT.md` — second deterministic TA3 batch
- `docs/SCH_PRISMA_V40_TA3_BATCH_C_READOUT.md` — third deterministic TA3 batch
- `docs/SCH_PRISMA_V41_TA3_BATCH_D_READOUT.md` — fourth deterministic TA3 batch
- `docs/SCH_PRISMA_V42_TA3_BATCH_E_READOUT.md` — fifth deterministic TA3 batch
- `docs/SCH_PRISMA_V43_TA3_BATCH_F_READOUT.md` — sixth deterministic TA3 batch

## Empirical execution strategy

```text
qualify conflict-active context
-> validate reversible multi-level z manipulation
-> validate selective consumer interventions
-> fit W00(z), W10(z), W01(z), W11(z)
-> recover z_P*, z_G*, z_C*
-> test optimum shifts and opposing component gradients
-> optionally test context-stable component optima
-> export only justified quantities downstream
```

Current high-value systems remain:

- **Dalechampia** — conditional first-choice compromise-surface system; conflict must be population/season qualified first.
- **Nicotiana attenuata** — strong local shared-cue mechanism system and downstream bridge candidate.
- **Castilleja linariaefolia** — high-value fallback requiring Stage-0 trait/intervention validation.
- aligned-optimum orientation systems — negative controls.

## Programme ownership

```text
SCH
multifunctionality != conflict
state-specific optimum != pure-function optimum
        |
        v
identified conflict / L when justified
        |
        v
SLK
L -> R -> Phi -> accessibility -> invasion -> fixation -> occupancy
        |
        v
multiple trait axes / observed interaction
        |
        v
BITA
trait interaction != mechanism
```

### SCH owns

- causal identification of opposing functional geometry on one shared coordinate;
- state-specific compromise geometry;
- the promotion gate from state-specific to context-stable function-specific optima;
- empirical qualification and negative-control logic.

### SLK owns

- the cross-repository architecture-value and population-realization spine;
- `R`, `K`, `Phi = R-K`, the minimum `R=sL` bridge where applicable;
- accessibility, invasion, fixation, occupancy, and INV1.

### BITA owns

- interaction-versus-mechanism inference once multiple trait axes exist;
- identified sets, partial identification, selective crossed consumer interventions, separability diagnostics, and remaining-channel assays.

### BALANCE

The BALANCE repository is now a DOI-oriented technical module for middle-world certification, worldline comparison, depth/reserve geometry, and hysteresis. It is not an active standalone paper in the current publication queue.

## Canonical reader path

- `manuscript/MANUSCRIPT_SHARED_TRAIT_COMPROMISE.md` — canonical active SCH manuscript
- `docs/PUBLICATION_STATUS.md` — active publication status and ownership boundary
- `docs/SCH_CAUSAL_COMPROMISE_SURFACE_ANALYSIS_V1.md` — state-specific optimum analyzer contract
- `docs/SCH_PURE_FUNCTION_OPTIMA_UPGRADE_V1.md` — context-stable component-optimum promotion gate
- `docs/SCH_MULTI_LEVEL_COMPROMISE_IDENTIFICATION_V1.md` — multi-level causal design
- `docs/SCH_EXECUTION_SPINE_V1.md` — end-to-end empirical execution
- `scripts/analyze_sch_compromise_surface.py` — compromise-surface analyzer
- `scripts/identify_sch_pure_function_optima.py` — optional pure-function promotion implementation
- `empirical/one_trait_shared_cue/` and `empirical/prisma/` — real-world evidence spine

Legacy chapter-programme documents remain versioned as provenance but are not the active publication architecture.

## Active paper thesis

SCH is not a paper about calculating `L` for its own sake. Its contribution is the inference gate before `L` is allowed to enter the SLK flagship:

> a trait serving two functions is not yet a conflicted trait, and a consumer-specific reproductive optimum is not yet a pure functional optimum.

That narrower ownership keeps SCH independent from SLK and complementary to BITA.
