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

## Independent patch-context evidence boundary

Xia, Sun & Liu (2013; doi:10.1098/rsbl.2013.0387) report that
the sign of the patch-size association with P. rex seed predation reverses
between sparse and dense patches. This is a useful biological lead, but the
2011 density/patch-size predictors span **11 independent patches**, while
the published capsule-level ANOVAs use residual df 2047/2345. Neither
patch-robust significance nor a compensation explanation for the
nonsignificant final-seed interaction is recovered. A separate
`audit_pedicularis_xia2013_patch_units.py` keeps those claims below their
evidence ceiling and defines a matched-capsule covariance test that could
be run on the verified historical Dryad workbook. No direct F0/G inference
is promoted.

## Execution priority

The repository is now **empirical-gate limited, not literature-screen limited**.

The machine-readable current Pedicularis blocker is
`PROSPECTIVE_THRESHOLD_FREEZE_REQUIRED`; run
`python scripts/audit_pedicularis_execution_frontier.py` to verify it.

Published-data recovery now tracks 10 Pedicularis sources and 77 quantitative
measurement/design rows. The strongest external resources are the public Dryad
dataset `10.5061/dryad.6cv06` (`raw data.xlsx`) and the 2016 `mcw097`
supplements. These historical data can inform variance, effect scale and field
feasibility, but recover **0 direct F0 gate values** because they are not the
same prospectively registered population/season/intervention package. Run
`python scripts/audit_pedicularis_published_empirical_priors.py` for the
bounded recovery state. Directly reported 2016 plant-level SDs now also
support external paired-difference sensitivity envelopes for P1 pollen and G
seed predation across explicit within-pair correlation assumptions; these
remain scenario priors, not observed CAL-C pilot SDs.

Focal reward-context recovery now also includes P. rex nectar dynamics across
Kunming, Lijiang and Daocheng. Across 13 stage/population rows, reported nectar
volume is 1.13±0.68 uL SD and sugar concentration 33±5% SD, with individual
table rows spanning 0.23–2.50 uL and 26–41% sugar. A separate 2007 study reports
a P. rex subsp. rex pollen–ovule ratio of 11222.04±4887.18 SD. These are focal
natural-state measurements, not supplementation effects.

A separate focal morphology dataset provides exact P. rex natural-scale means
(±SEM): corolla tube 23.43±0.498 mm, lower-lip width 12.71±0.382 mm, and
pollen-grain volume 4448±89.28 um3. These help bound natural P0/P1 trait scale
but are not same-flower repeatability estimates.

A focal P. rex mating-system study adds another strong natural-state constraint:
multilocus outcrossing was high in both sparse and dense patches
(`t_m=1.151` and `0.924`, respectively). Secondary citation reproduces
uncertainties of ±0.108 and ±0.042, but their SD/SE interpretation remains
unverified in the primary full text, so they are not used as CAL-C variance.

A separate 2005 five-population RAPD study reports strong population
differentiation (`Gst=0.747`) and interprets the pattern as compatible with
mixed mating and relatively high selfing. Gst is **not** treated as a selfing
rate. Together with the high-outcrossing 2013 result, this is evidence that
mating context varies strongly among P. rex populations rather than evidence
for one portable species-wide P1 expectation.

Method recovery also shows that the P0/P1 treatment families do not need to be
invented from scratch. Pedicularis field studies already demonstrate
non-destructive corolla shortening by bending + clear tape, flower-level
blocking/bagging controls, and self/outcross pollen supplementation. The P1
recovery includes five supplementation precedents, including a whole-plant
P. monbeigiana experiment with an exact treatment effect (F1,304=113.27 for
seed set). A ninth method precedent now adds within-genus G timing evidence:
P. furbishiae scapes covered before flowering but uncovered for pollination
later showed normal lepidopteran seed predation, supporting post-pollination
attack timing. These remain method/timing precedents only: focal P. rex
manipulation, repeatability, supplementation and independent-G effects remain
unmeasured in the registered form. Run
`python scripts/audit_pedicularis_method_precedents.py`.

A separate congeneric quantitative ledger now contains 27 numerical/design
rows from six Pedicularis species. It makes the P1 uncertainty concrete:
published supplementation spans an effectively null response in P. monbeigiana
to a reported 2.1x seed-set response in another ecological context. The
expanded range also includes P. dunniana natural/hand-self/hand-cross seed set
(54.2%, 63.1%, 67.2%; F=115.08, df=2,15, P<0.001) and P. palustris
whole-plant pollinator exclosure (<15% of natural seed set) plus
population-dependent pollen-limitation context. These are external CAL-B/C
sensitivity priors, not portable P. rex targets, and the different intervention
families are not pooled as one effect. Run
`python scripts/audit_pedicularis_congeneric_quantitative_priors.py`.

A focal direct-evidence search audit is also frozen. It currently recovers
natural pollinator dependence, high outcrossing, reward variation, seed-
predation baselines, a wrong-axis focal antagonist experiment, and congeneric
method precedents. A within-genus P. furbishiae experiment now also establishes
that a Pedicularis lepidopteran seed predator can attack after pollination.
External G-method recovery now separates four claims: within-genus
post-pollination attack timing, within-genus barrier efficacy with natural
pollination replaced by hand crossing, fruit-development compatibility of a
post-pollination porous barrier, and external fruit-local barrier efficacy.
All four precedent classes are now recovered. What remains unresolved is
**barrier effectiveness under the focal P. rex device, preservation of natural
bumblebee pollination, and numeric timing qualification in focal P. rex**, plus
the registered focal P1 supplementation effect, same-flower repeatability, and
>=5-level P0 manipulation. The 2013
focal mating-system paper explicitly reports hand versus natural pollination,
but the accessible primary abstract does not identify the hand treatment
precisely enough to promote it to P1. Run
`python scripts/audit_pedicularis_focal_direct_evidence_search.py`.
The barrier-class evidence itself is audited separately with
`python scripts/audit_pedicularis_g_barrier_precedents.py`; none of those
external precedents is promoted to focal P. rex validation or a direct F0
value.

Broad literature expansion is now explicitly stopped. Only five named primary
assets remain worth retrieving: Jing 2013 Methods, Tang 2011 thesis, Wang 1998
PDF, Xia 2013 Dryad raw workbook, and the 2016 mcw097 supplements. Only the
first three could plausibly change a direct P1/G gap; the last two can sharpen
external priors only. Until one of those primary binaries is retrieved, focal
field calibration is the primary path. Run
`python scripts/audit_pedicularis_primary_binary_frontier.py`.

Concrete retrieval attempts are now frozen separately. Jing2013 remains
treatment-identity unresolved after Springer/author-copy/index routes; the live
Springer primary page exposes the abstract but not Methods. Wang1998 has now
advanced from a generic "611-KB PDF listed" state to an exact publisher PDF URL:

```text
https://www.jipb.net/EN/article/downloadArticleFile.do?attachType=PDF&id=25287
```

but direct public GET still returns HTTP 403 in the current fetch environment.
The same article-id endpoint was also tested through JIPB CN,
chinbullbotany CN and plant-ecology CN legacy mirrors; all four known variants
returned HTTP 403. Public URL-variant probing for Wang1998 is therefore closed.
Tang2011's live Globethesis URL now redirects to a suspended-account page with
no binary links; its full English abstract remains the strongest accessible
content and describes no predator exclusion. Dryad file `46101` is publicly
identified but the current file-download API requires authentication.

Accordingly, abstract/index search is stopped for Jing2013, PDF-URL discovery is
stopped for Wang1998, and Globethesis retries are stopped for Tang2011. Only
legitimate primary/library/repository binary access can change those states.
Run `python scripts/audit_pedicularis_primary_binary_retrieval_attempts.py`.

Primary-binary interpretation is now fail-closed as well. If Jing2013,
Wang1998 or Tang2011 is ever retrieved, its Methods/Table facts must be entered
in `PEDICULARIS_PRIMARY_METHOD_ADJUDICATION_V1.csv` and passed through
`scripts/adjudicate_pedicularis_primary_methods.py`. The adjudicator separates
a historical focal effect from the stricter registered estimand/protocol
family, so terms such as "hand pollination" or "predator exclusion" cannot be
promoted by wording alone. Even a positive historical adjudication recovers
zero direct F0 values; same-context prospective calibration remains required.
The threshold-basis ledger currently resolves 5/40 gate values directly from
registered contracts. The remaining 35 are now organized into three
nonconfirmatory modules:

```text
CAL-A  measurement / equivalence / handling calibration   20 gates
CAL-B  exploratory P/G effects + G timing                  7 gates
CAL-C  prospective power / precision planning              8 gates
```

CAL-A repeatability and target-freeze infrastructure is implemented: 20
separation/equivalence decisions can be materialized with pilot context and
13 matched measurement-noise q95 values, then frozen prospectively and
transferred into CAL-C. Its calibration data are not yet collected. CAL-B target-freeze infrastructure is implemented:
pilot mean/q05/q95 can be materialized separately from the seven manually
justified effect/timing targets, and the five effect targets can be transferred
into CAL-C without filling assumed true effects. CAL-C planning infrastructure is also implemented:
pilot SD provenance can be materialized separately from biological targets,
then a familywise P0/P1/G plan can generate the eight sample-size gates once
CAL-A/B targets and planning assumptions are prospectively frozen.

F0 assembly infrastructure is also implemented. A positive CAL-A receipt,
positive CAL-B receipt and positive CAL-C plan are combined with the five
registered contract values as an exact 5 + 20 + 7 + 8 = 40 source partition;
all three output configs are revalidated by the shared prospective-freeze
validator before confirmatory collection is unlocked.

Use `scripts/build_pedicularis_calibration_package.py` to validate the
cohort registry against the four nonconfirmatory data bundles and generate the
repeatability + threshold-free calibration summaries together. The package
allows same-flower repeatability within CAL-A P0 but rejects other cross-lane
flower reuse. Lower-level summarizer/registry tools remain available for audit.

Field-effort priority is now explicit without inventing sample sizes:
`G exploratory > P0 + nested repeatability > P1 exploratory`. This is a
structural-risk / information-yield order, not a strict chronological sequence
or an informal stop rule. The derived bundle yields are G=20, P0=16,
repeatability=13 measurement-noise floors, and P1=16 calibration-support
outputs. Run
`python scripts/audit_pedicularis_calibration_collection_yield.py`.

G exploratory now also has a threshold-free fail-fast screen. Multiple V4
candidate barriers can be compared on the already-registered hard validity
requirements first; attack/predation, reproductive gain and contamination are
summarized descriptively, with no automatic method selection or effect
threshold. This allows mechanically invalid barrier designs to be retired
before confirmatory G planning. Run
`python scripts/screen_pedicularis_g_exploratory_methods.py <g_v4.csv>`.

The exploratory device space is bounded before field data. First-tier candidates
are a post-pollination fine-mesh lower-fruit sleeve and a soft porous/dialysis-
style sleeve; a lower-corolla local sleeve is second-tier when pollination and
oviposition timing overlap. Whole-flower mesh and chemical routes are fallbacks.
This is a candidate-priority matrix only: the two first-tier methods remain tied
until focal V4 rows pass the hard-validity screen. Run
`python scripts/audit_pedicularis_g_exploratory_candidates.py`.

Candidate identity is now carried into the field data through canonical
`exclusion_method` codes (for example
`FINE_MESH_LOWER_FRUIT_SLEEVE` and
`POROUS_TUBING_LOWER_FRUIT_SLEEVE`). Run
`python scripts/screen_pedicularis_g_candidates.py <g_v4.csv>` to require an
exact candidate-to-field-code match before the fail-fast hard-validity screen.
Unknown ad-hoc method labels fail closed; a hard-validity failure can retire the
tested candidate as implemented, while multiple hard-validity passes remain
unselected until prospective effect/selectivity targets exist.

For field execution, populate
`PEDICULARIS_G_FIRST_TIER_PILOT_PLANTS_TEMPLATE_V1.csv` with the focal
population/season, plant IDs and three treatment-blind flower IDs per plant.
Then run `build_pedicularis_g_first_tier_pilot_manifest.py` with a
precommitted neutral `--allocation-seed`. The builder deterministically
randomizes those three flowers within each plant to sham, fine-mesh and
porous-tubing arms using SHA-256 ranking and records the seed/algorithm in the
receipt. The script does not choose the number of plants and does not generate
V4 outcomes before they are measured.

Before field scoring, bind that randomized allocation to the canonical V4
schema with `prepare_pedicularis_g_v4_field_sheet.py prepare`. The command
prefills only the frozen plant/flower/treatment/method identity columns and
writes an identity lock tied to the allocation receipt and seed digest. After
field scoring, run the same tool in `verify --require-complete` mode before
`screen_pedicularis_g_candidates.py`; any flower substitution, treatment or
method-code drift, missing/extra row, or incomplete V4 cell fails closed.

Primary biological timing is now audited separately in
`PEDICULARIS_G_TIMING_PRIMARY_EVIDENCE_V1.csv`. Focal P. rex sources recover
the open-flower/pre-swelling oviposition order, bumblebee dependence,
approximately three-week capsule maturation, and strong geographic variation in
seed predation, but recover **no hour-scale safe barrier window**. The registered
timing bounds therefore remain focal event-time estimands rather than literature
constants; natural predation prevalence is explicitly ineligible as a device
hard-failure tolerance. Run
`python scripts/audit_pedicularis_g_timing_primary_evidence.py`.

The separate natural-state `CAL_B_G_TIMING` pilot now tests temporal
separability directly. Destructive pollen sentinels estimate the pollination
completion trajectory, while one repeated attack/swelling sentinel per plant
tracks the first antagonist/developmental constraint. The nominal elapsed-hour
grids and maximum allowed field-timing deviation are frozen in the config before
data; every plant must cover every scheduled time, and both sentinel lanes use
the same plant blocks. The summarizer reports interval-censored event timing and
the exploratory median `Delta_T50` ordering without selecting a confirmatory
barrier hour. Run
`python scripts/summarize_pedicularis_g_event_time_pilot.py <config.json> <timing.csv>`.

Exploratory G method reliability also has a prospective sample-size planner.
Given a frozen maximum acceptable per-plant hard-failure probability, it
computes the minimum plants required for zero observed hard failures using the
one-sided exact binomial upper bound. At 95% confidence, a 10% tolerance implies
29 plants/candidate and a 5% tolerance implies 59; neither is a default.
Because the current three-arm manifest puts both first-tier candidates plus one
shared sham on every plant, those examples correspond to 29 or 59 distinct
plants (87 or 177 total flowers), not 58 or 118 distinct plants. Run
`python scripts/plan_pedicularis_g_hard_validity_pilot.py`.

Before field collection starts, bind the hard-validity plan, randomized
allocation, allocation receipt and V4 identity lock with
`audit_pedicularis_g_pilot_preflight.py`. The preflight requires one
population/season, verifies the allocation/receipt/seed/identity digests, and
checks that the actual number of distinct plants meets the prospectively frozen
hard-validity plan. An under-sized packet remains explicitly not field-ready.

Stage-P0 uses the same treatment-blind allocation discipline. Freeze the
ordered z-level/sham plan separately, register flower IDs without treatment
labels, then run `build_pedicularis_p0_randomized_assignment.py` with a
precommitted seed. Every plant supplies one flower per planned z level; the
builder randomizes flower-to-level assignment within plant but does not choose
manipulation strengths, plant count or thresholds. This makes the implemented
field allocation match the registered P0 design.

A second focal biological prediction is now registered from the 2016 P. rex
selection study. In the seven populations with linked plant-level data, the
best seed-predation model retained positive effects of exsertion, lower-lip
width and stigmatic pollen load plus population; the source itself highlights
the unexpectedly higher predation of better-pollinated flowers. This is treated
as observational pollination-success/antagonist-risk coupling, not evidence that
pollen is the predator cue. Combined with focal pollen limitation, it motivates
a post-surface test of whether seed predators shift the NATURAL-pollination
reproductive optimum toward lower exsertion, away from trait states with higher
pollen receipt. That is a state-optimum/pollination-performance result, not a
pure pollinator optimum and not yet evidence that antagonists maintain pollen
limitation. The four-criterion adaptive-pollen-limitation map remains fail-closed
at 1/4 fully supported criteria.
See `SCH_PEDICULARIS_ANTAGONIST_CONSTRAINED_POLLEN_LIMITATION_V1.md`.
The biological paper spine is now frozen separately in
`docs/SCH_PEDICULARIS_EMPIRICAL_STORY_V1.md`: the headline test is
enemy-induced displacement of the natural-pollination reproductive optimum
away from trait states with greater pollination performance; timing and
threshold machinery remain enabling methods rather than the paper's subject.
The six predeclared empirical outcome worlds (W0-W5) are machine-readable in
`PEDICULARIS_EMPIRICAL_OUTCOME_WORLDS_V1.csv` and classified with
`classify_pedicularis_empirical_outcome.py`, so null and partial outcomes have
their own biological interpretations rather than being post-hoc relabelled.
The close-precedent novelty audit is frozen in
`PEDICULARIS_EMPIRICAL_NOVELTY_MATRIX_V1.csv`. Existing studies already cover
factorial pollination x antagonism, multi-level floral-display optima, and
enemy-associated floral optimum shifts. The bounded P. rex gap is therefore
the joint randomized multi-level shared-z x selective-P x selective-G design
that recovers four reproductive state surfaces and directly tests
antagonist-removal optimum displacement.

The next primary objective is to close one same-system causal chain. The active
Pedicularis route is:

```text
same population + same season
CAL-A      measurement/equivalence/handling calibration
CAL-B      exploratory P/G effects + G timing pilot
CAL-C      intervention-validity/selectivity power planning
Stage F0   freeze P0/P1/G thresholds + one basis note per gate before confirmatory outcomes
G select   freeze one exploratory hard-pass G method before confirmatory outcomes
P2 bind    bind frozen P0 z labels + physical manipulation settings + full
           P0 plan SHA + P0/P1/G configs + selected G method to geometry
           |
           +-----------------------------+
           |                             |
P0/P1/G confirmatory                 POWER_GEOMETRY_PILOT
randomized collection               separate-cohort collection
           |                             |
           v                             |  not yet admissible
readiness V3 when randomized             |
P0/P1/G all pass                         |
           +---------- exact plan SHA ---+
                           |
P2 geometry              only now summarize / precision-qualify geometry;
                         failed readiness or plan mismatch discards it for power basis
P2 basis                 resolve 18/21 blockers from qualified geometry
P2 final3                materialize numeric z grid + within-level z SD from locked
                         positive P0; use a pre-geometry full-surface threshold freeze
                         to move 3 -> 0 blockers
P2 bind                  require BOTH exact 18-path geometry binding and exact
                         3-path P0/F0 binding to the same frozen power config
P2 power                 only then run registered production W0-W5 power
P2 alloc                 require exact positive readiness V3 + passing powered design,
                         then bind treatment-blind flower IDs
P2 lock                  verify exact z/P/G/method identity + surface SHA-256
Stage P2                 run verified z x P x G surface
Stage P3                 test context-stable component optima
Stage P4                 export fitness-scale conflict budget L
```

Current P1 V1 is explicitly `WITHIN_PLANT_PAIRED_FLOWERS`, matching the
registered CAL-C paired-plant sample-size fields and paired bootstrap estimator.
Whole-plant supplementation remains a literature-supported alternative, but
cannot be substituted into V1 without a separate prospective protocol/evaluator.
For confirmatory P1, `build_pedicularis_p1_randomized_assignment.py` binds
treatment-blind flower IDs to equal NATURAL sham-handling and SUPPLEMENTED
donor-mixed-cross-pollen arms within each plant using a precommitted SHA-256
seed. The production P1 CLI requires that allocation receipt and rejects
flower/treatment/handling or frozen-config drift.

The final P2 replication now has a second prospective power layer in addition
to CAL-C, but its evidence basis is audited first. The current basis ledger has
30 rows, with 21 blocking inputs and 0/12 causal-geometry rows ready for a
registered single-scenario n. `audit_pedicularis_w1_w2_power_basis.py`
therefore keeps the registered n fail-closed until either an independent
nonconfirmatory geometry pilot or a prospectively frozen robust scenario
envelope supplies the missing basis. Blocked-basis simulations are explicitly
sensitivity-only and cannot feed P2 allocation. Before spending a separate
geometry-pilot cohort, `evaluate_pedicularis_w1_w2_power_envelope.py` can run
multiple prospectively declared sensitivity worlds and report worst-case power
plus the scenario-specific minimum-n range. The envelope is a
value-of-information diagnostic only: it cannot register n or unlock P2.
The current-evidence boundability audit shows why this remains a diagnostic:
among the 18 blocking geometry/variance inputs there are currently 0 direct
same-estimand numeric bounds, 3 direction-only constraints, 4 endpoint
scale/range constraints and 11 inputs with no numerical bound. Thus a narrow
Route-B scenario set cannot be attributed to the current focal evidence alone;
see `docs/SCH_PEDICULARIS_W1_W2_ENVELOPE_BOUNDABILITY_V1.md`.
If geometry uncertainty materially changes the field decision, Route A is now
executable without placing an unnecessary second fruit-maturation wait on the
critical path. After F0 and pre-outcome G-method selection,
`bind_pedicularis_geometry_intervention_plan.py` freezes the exact P0 z plan,
P0/P1/G configs, selected G method and geometry config. A disjoint
`POWER_GEOMETRY_PILOT` cohort may then be **collected in parallel** with
randomized confirmatory P0/P1/G. Its data remain inadmissible until later
readiness V3 is positive and all bound plan hashes match exactly.
`summarize_pedicularis_p2_geometry_pilot.py` therefore requires that later
readiness receipt before any point estimate is exposed for power basis. See
`docs/SCH_PEDICULARIS_PARALLEL_GEOMETRY_COLLECTION_V1.md`.

The precision gate remains frozen before pilot outcomes; point-estimable geometry
alone cannot promote the 18 power-basis paths. Geometry-pilot n is also
prospective: `candidate_cumulative_plants` freezes exact-balanced cumulative
looks and `adjudicate_pedicularis_p2_geometry_accrual.py` stops at the first
precision pass; later looks require every earlier look to have formally failed
precision.
After precision qualifies, the separate
`POWER_GEOMETRY_PILOT` can materialize 18 same-estimand geometry/variance
basis rows, reducing 21 blockers to three. Those final three are now
machine-resolvable without another experiment:
`materialize_pedicularis_w1_w2_final_p0_f0_basis.py` uses the positive locked
P0 experiment to define the numeric z grid as the mean realized exsertion of
each validated physical setting and estimates `realized_z_sd` as the pooled
within-setting residual SD; the primary `sch_surface` rules come from
`freeze_pedicularis_full_surface_thresholds.py`, which must be frozen before
geometry/P2 outcomes are used. A zero-blocker basis then requires **two**
exact config bindings:
`bind_pedicularis_w1_w2_geometry_config.py` for the 18 qualified geometry
paths and `bind_pedicularis_w1_w2_p0_f0_config.py` for the final three.
See `docs/SCH_PEDICULARIS_P2_GEOMETRY_PILOT_V1.md` and
`docs/SCH_PEDICULARIS_FINAL_W1_W2_BASIS_V1.md`.
`simulate_pedicularis_w1_w2_power.py` then powers the actual production
full-surface -> enemy-displacement -> W0-W5 pipeline. The powered z grid,
plants and flowers-per-plant design are then bound to treatment-blind flower
IDs by `build_pedicularis_full_surface_allocation.py`. Allocation now also
requires the exact positive readiness V3 receipt that validated the P0 physical
z settings, G0 exclusion method and G1 exposed-sham handling; that readiness
SHA-256 is carried through the field packet. The completed P2 field
packet must pass
`prepare_pedicularis_full_surface_field_sheet.py verify --require-complete`;
the production analyzer rejects a CSV whose SHA-256 differs from that verified
packet **or whose primary surface/system-check config differs from the exact
config used in registered power**. See
`docs/SCH_PEDICULARIS_W1_W2_POWER_V1.md` and
`docs/SCH_PEDICULARIS_FULL_SURFACE_ALLOCATION_V1.md`.

Until that chain produces a valid full-surface receipt (or fails a preregistered
stop rule), additional TA3 remainder screening is secondary. Screening records
already recovered remain part of the systematic denominator, but adding further
screening batches does not substitute for executing the missing SCH estimands.

For implementation files, Git history is the version record. New runtime code
should use canonical unversioned entrypoints; version suffixes are reserved for
scientifically distinct frozen protocols, schemas, and provenance snapshots.

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
interaction-timing moderator = FAIL_CLOSED (34/35 fixed-role axes simultaneous/overlapping)
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

V44 closes the seventh deterministic TA3 batch, review orders 228–252: 25 records screened, 10 retained and 15 excluded. Formal title/abstract screening reaches 658/868; 210 remain unscreened. The retained set includes tripartite selection, brood-pollination, ozone-mediated biotic context and herbivory-dependent pollinator selection.

V45 closes the eighth deterministic TA3 batch, review orders 253–277: 25 records screened, 11 retained and 14 excluded. Formal title/abstract screening reaches 683/868; 185 remain unscreened. Strong retains include Primula farinosa scape length, nursery-pollination systems, orchid ant-protection, and Cucurbita shared floral volatiles.

V46 closes the ninth deterministic TA3 batch: 25 records screened, 6 retained and 19 excluded. Formal title/abstract screening reaches 708/868; 160 remain unscreened. Retains include Impatiens, Arabidopsis lyrata, Geranium, Silene–Hadena and Pedicularis rex multi-agent systems.

V47 closes the tenth deterministic TA3 batch, review orders 304–328: 25 records screened, 6 retained and 19 excluded. Formal title/abstract screening reaches 733/868; 135 remain unscreened.

V48 closes the eleventh deterministic TA3 batch, review orders 329–353: 25 records screened, 9 retained and 16 excluded. Formal title/abstract screening reaches 758/868; 110 remain unscreened. Retains include fig chemical conflict, sequential conflicting selection, nursery-pollinator systems and slippery-flower ant defence.

V49 closes the twelfth deterministic TA3 batch, review orders 354–378: 25 records screened, 9 retained and 16 excluded. Formal title/abstract screening reaches 783/868; only 85 remain unscreened. Retains include ant–pollinator conflict, nursery-pollinator selection, shared floral volatile attraction/defence and Thunia bract defence.

V50 closes the thirteenth deterministic TA3 batch: 25 records screened, 15 retained and 10 excluded. Formal title/abstract screening reaches 808/868; only 60 remain unscreened.

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
- `docs/SCH_PRISMA_V44_TA3_BATCH_G_READOUT.md` — seventh deterministic TA3 batch
- `docs/SCH_PRISMA_V45_TA3_BATCH_H_READOUT.md` — eighth deterministic TA3 batch
- `docs/SCH_PRISMA_V46_TA3_BATCH_I_READOUT.md` — ninth deterministic TA3 batch
- `docs/SCH_PRISMA_V47_TA3_BATCH_J_READOUT.md` — tenth deterministic TA3 batch
- `docs/SCH_PRISMA_V48_TA3_BATCH_K_READOUT.md` — eleventh deterministic TA3 batch
- `docs/SCH_PRISMA_V49_TA3_BATCH_L_READOUT.md` — twelfth deterministic TA3 batch
- `docs/SCH_PRISMA_V50_TA3_BATCH_M_READOUT.md` — thirteenth deterministic TA3 batch

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
