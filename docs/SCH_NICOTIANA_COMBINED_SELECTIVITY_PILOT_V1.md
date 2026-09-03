# SCH Nicotiana combined-selectivity pilot v1

## Purpose

This pilot is the go/no-go experiment for using *Nicotiana attenuata* as the confirmatory SCH mechanism system.

Primary-source recovery already establishes the separate ingredients:

```text
BA manipulation -> pollinator-mediated seed production
BA manipulation -> M. sexta oviposition
standardized moth pollen loading -> mature seed outcome
post-oviposition egg removal -> downstream herbivore suppression
```

The unresolved question is whether those ingredients can be combined without destroying the meaning of the `P` and `G` channels.

This pilot is therefore **not powered to prove SCH**. It is powered/designed to reject unusable intervention architectures early.

## Core biological problem

The highest-information BA-responsive receiver, female *Manduca sexta*, can perform both roles during one foraging bout:

```text
flower visitation / pollen delivery
+
oviposition leading to future larval herbivory
```

Therefore `pollinator present/absent` and `antagonist present/absent` cannot simply be implemented by adding/removing the moth. The same receiver would move both pathways.

SCH requires pathway interventions rather than guild labels.

## Fixed A coordinate

Use the historically validated benzylacetone contrast as the first candidate:

```text
A1 = EV / BA-emitting
A0 = CHAL / BA-silenced
```

Before any receiver trial, verify in the actual material:

- nocturnal BA emission contrast;
- nectar volume and sugar concentration;
- flower morphology / opening time;
- flower number in the exposure window;
- plant size and developmental stage.

Promotion requires the BA contrast to remain large while non-target floral traits remain sufficiently similar for the intended claim.

## Pilot architecture A — same female receiver, pathway manipulation

This is the first-choice selectivity test because it keeps receiver identity constant across `P` and `G` states.

### P component

Use the established standardized pollen-loading method on the moth proboscis.

```text
P1 = standardized pollen load before release
P0 = matched sham manipulation without added pollen
```

The exact pollen source and load are fixed before the experiment. Recover pollen from the proboscis after the trial to quantify delivered/remaining load and to verify that loading does not differ by `A` or later `G` assignment.

### G component

Allow the female moth to make the oviposition decision before the `G` intervention.

```text
G1 = eggs retained through hatch / predeclared damage window
G0 = eggs counted, then removed before hatch
```

This ordering is essential. Removing or excluding the female before oviposition would erase the `A -> antagonist choice` pathway that SCH is trying to evaluate.

### Candidate factorial

```text
A x P x G

BA-  sham-pollen  eggs-removed
BA+  sham-pollen  eggs-removed
BA-  pollen-load  eggs-removed
BA+  pollen-load  eggs-removed
BA-  sham-pollen  eggs-retained
BA+  sham-pollen  eggs-retained
BA-  pollen-load  eggs-retained
BA+  pollen-load  eggs-retained
```

The `G` assignment should be randomized before moth exposure but implemented only after egg counts are recorded, so the moth cannot respond to the future treatment.

## Critical problem with architecture A

Pollen loading is not automatically equivalent to a clean `pollinator pathway on/off` intervention.

If sham-loaded moths still transfer enough endogenous or previously acquired pollen to generate substantial reproduction, `P0` is contaminated.

If sham-loaded flowers are effectively sterile, the `P0` reproductive cells may collapse near zero, making `B_A`, `G_A(0)` and the four-way bookkeeping uninformative.

Therefore architecture A is acceptable only if the pilot shows a useful intermediate separation:

```text
P1 materially increases the declared reproductive channel
while
P0 retains a measurable, biologically interpretable baseline W.
```

If this cannot be achieved, architecture A may still validate the pollination and antagonist tools but must not be promoted as the canonical SCH 8-cell experiment.

## Pilot architecture B — natural reproduction plus standardized pollen augmentation

If architecture A produces a degenerate `P0`, test a second pathway design on intact flowers/plants:

```text
P0 = natural/self reproduction under the standardized receiver exposure
P1 = the same exposure plus a fixed outcross-pollen augmentation
```

`G0/G1` remains egg removal versus retention after oviposition.

This preserves a non-zero reproductive baseline and can test whether added pollinator-mediated outcrossing changes the effect of `A`.

However the claim ceiling is narrower:

```text
P = augmented outcross-pollen channel
not
P = all pollinator-mediated reproduction
```

Architecture B is promoted only if that narrower estimand remains biologically aligned with the SCH question and the outcross augmentation does not alter moth oviposition behaviour.

## Contamination tests

The pilot must report these before any SCH mechanism contrast.

### C1 — P manipulation -> G behaviour

Test whether pollen loading/sham changes:

- probability of oviposition;
- egg number;
- time spent on the plant / flower;
- number of flowers probed.

A large effect means `P` manipulation changes `G` and is not selective.

### C2 — future G assignment -> pre-treatment behaviour

Because `G` is implemented only after oviposition, randomized future `G` labels should show no systematic difference in:

- visits;
- pollen delivery;
- egg number;
- BA exposure.

Any imbalance is a randomization/implementation problem.

### C3 — egg removal -> subsequent A/P biology

Verify that egg removal itself does not change:

- floral damage before removal;
- BA emission in later flowers used for outcome assessment;
- pollination treatment delivery;
- handling damage.

Use sham handling in `G1` plants if necessary so physical manipulation is balanced.

### C4 — G retention -> actual damage

`G1` must produce enough downstream antagonist exposure/damage to create a biologically meaningful contrast. Record:

- eggs;
- hatch success;
- larval establishment;
- leaf/floral damage through a fixed window;
- plant compensation / new flower production.

If eggs are retained but reproductive damage is negligible, `G` is biologically weak even if technically selective.

## Receiver and block structure

Use one female moth per experimental block where feasible so each moth encounters a balanced randomized set of `A` states. Do not treat flower visits from one moth as independent biological replicates.

Record at minimum:

```text
moth_id
plant_id
flower_id
block_id
night
time_order
A_state
P_state
future_G_state
BA_measure
nectar_measure
visit_count
probe_duration
pollen_load_pre
pollen_load_post
egg_count
egg_removed_or_retained
hatch_count
larval_damage
capsule
seed_count
seed_viability
```

The confirmatory analysis unit and random-effects structure must be chosen from the pilot's realized dependence, not from the nominal number of flowers.

## Common W decision

The preferred `W` is mature viable seed output, but the pilot must test whether this remains interpretable after antagonist damage that may act at whole-plant scale.

Two admissible allocation units are:

### Flower-level W

Use when damage can be linked to focal flowers without major spillover among flowers on the same plant.

```text
W = viable seeds per focal flower
secondary = capsule probability, seeds per capsule
```

### Plant-level W

Use when retained larvae alter resource allocation across the plant.

```text
W = viable seed output over a fixed post-exposure reproductive window
```

If `G` acts at plant level, do not pretend flowers on the same plant are independent replicates.

## Promotion rules

Promote *Nicotiana* to the confirmatory SCH 8-cell design only if all are satisfied:

```text
PSEL1  A remains stable under all handling
PSEL2  P contrast changes the intended reproductive pollination channel
PSEL3  P manipulation has acceptably small effect on oviposition behaviour
GSEL1  egg-removal contrast preserves the preceding A-dependent oviposition decision
GSEL2  G1 produces measurable antagonist damage/loss
GSEL3  egg removal/sham handling has acceptably small effect on A and P
W1     one common W remains measurable and non-degenerate across the design
DEP1   block/moth/plant dependence can be represented with feasible replication
```

No single p-value promotes the system. The decision is based on intervention validity and whether the resulting estimands still correspond to the SCH channel definitions.

## Stop rules

Stop *Nicotiana* as the canonical 8-cell system when any of the following remains after both reasonable pilot architectures:

- `P0` cannot be made interpretable without also suppressing the female moth's antagonist choice;
- pollen manipulation materially changes oviposition behaviour;
- egg removal/retention cannot create a selective damage contrast;
- the downstream larval effect operates at a scale that makes a common W infeasible with realistic replication;
- BA manipulation ceases to be the invariant coordinate under the combined handling.

If stopped, retain *Nicotiana* in SCH as strong real-world evidence for `L0` shared-coordinate conflict components and as a BITA programme bridge. Do not treat system rejection as hypothesis rejection.

## Method precedent outside Nicotiana

Theis & Adler 2012 independently manipulated fragrance, pollination and florivores in *Cucurbita pepo* var. *texana* and measured seed production. That system is a direct precedent that the three biological factors can be experimentally crossed. It does not itself close SCH because enhanced fragrance increased florivore attraction but not pollinator attraction.

Sánchez-Lafuente 2007 provides the complementary dissociation: corolla manipulation altered pollinator visitation and reproduction but not fruit-predator visitation.

These precedents justify the fail-closed rule:

```text
A real A x P x G architecture
!=
a demonstrated shared-cue conflict
```

Both `M_A > 0` and `G_A > 0` must be recovered on the declared A coordinate.

## Immediate execution decision

```text
1. run architecture-A manipulation/contamination checks at small scale
2. if P0 degenerates, run architecture-B feasibility
3. promote only if combined selectivity survives
4. otherwise freeze Nicotiana as L0 real-world evidence and move system
```

This combined-selectivity test is now the highest-information next validation for mechanism-first SCH.