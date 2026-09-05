# Shared Trait Compromise / SCH

SCH is **Chapter 1** of a three-world trait-architecture programme with [BALANCE](https://github.com/zuizui0223/balance) as Chapter 2 and [BITA](https://github.com/zuizui0223/bita) as Chapter 3.

```text
Chapter 1 / SCH — shared-coordinate world
function 1 ---\
               >--- shared trait z ---> compromise
function 2 ---/
-> where does compromise settle?

Chapter 2 / BALANCE — middle world
shared-axis conflict is real
but differentiated architecture still does not pay
-> why does compromise persist, and how deep/wide is that domain?

Chapter 3 / BITA — differentiated-coordinate world
shared compromise
      ↓
function 1 ---> trait x
function 2 ---> trait y
      ↓
functional differentiation / modularization
-> when does differentiation win, and through which mechanism?
```

The general SCH question is:

> **What happens when two fitness-relevant functions are forced to use the same phenotypic coordinate?**

The pollinator-antagonist shared-cue problem is the first floral implementation, not the definition of the chapter.

## Theory target

At the theory level, let one trait `z` contribute to two functions:

```text
W_shared(z) = w1 F1(z) + w2 F2(z) - C(z).
```

Pure function-specific optima are:

```text
z_F1* = argmax F1(z)
z_F2* = argmax F2(z).
```

The older shorthand `z1* != z2*` refers to this theory-level conflict.

Under the ideal local quadratic benchmark:

```text
L_shared(z)
  = a (z - z_F1*)^2
  + b (z - z_F2*)^2
```

with theory-level mismatch penalty:

```text
L_compromise,theory*
  = [a b / (a + b)] (z_F1* - z_F2*)^2.
```

This is a theory benchmark, not an instruction to relabel experimental state optima as pure function optima.

## What the experiment directly identifies

The multi-level crossed experiment fits:

```text
W00(z) = P0G0
W10(z) = P1G0
W01(z) = P0G1
W11(z) = P1G1
```

and directly identifies:

```text
z_P* = argmax W10(z) = z_pollinator_context
z_G* = argmax W01(z) = z_antagonist_context
z_C* = argmax W11(z) = z_combined.
```

These are state-specific reproductive optima. Because direct/background trait effects can remain:

```text
z_P* != automatically z_F1*
z_G* != automatically z_F2*.
```

The default Chapter-1 result therefore remains state-specific.

A stronger optional promotion uses the causal component contrasts from the same selective `z x P x G` experiment:

```text
M_G0(z) = W10(z) - W00(z)
M_G1(z) = W11(z) - W01(z)
H_P0(z) = W01(z) - W00(z)
H_P1(z) = W11(z) - W10(z).
```

If the two pollinator-component optima agree across antagonist states and the two antagonist-component optima agree across pollinator states, with interior-optimum and bootstrap support inside a prospectively frozen equivalence bound, SCH may promote them to context-stable empirical `z_F1*` and `z_F2*`. If they differ by context, retain conditional component optima and do not use the pure-function label.

This optional gate is implemented in `scripts/identify_sch_pure_function_optima.py` and documented in `docs/SCH_PURE_FUNCTION_OPTIMA_UPGRADE_V1.md`.

## Identification programme

```text
L0  multifunctionality
L1  local functional conflict
L2  state-specific compromise geometry
L3  mechanism-resolved balance
L4  evolutionary maintenance
L5  historical architecture.
```

The decisive empirical compromise result requires:

```text
z_P* != z_G*
combined W11(z) has a supported interior z_C*
G off -> z_C* shifts toward z_P*
P off -> z_C* shifts toward z_G*
opposing functional-component gradients near z_C*.
```

The zero derivative of an interior fitted quadratic at its own vertex is not counted as independent evidence.

## Floral implementation

For one binary attraction/display contrast `A`, SCH crosses:

```text
A x antagonist x pollinator
```

in eight cells on one common reproductive outcome.

```text
d[g,p] = W[1,g,p] - W[0,g,p]
M_A(g) = d[g,1] - d[g,0]
G_A(p) = d[0,p] - d[1,p]
B_A    = d[0,0]
J_A    = d[1,1] - d[1,0] - d[0,1] + d[0,0].
```

A positive `M_A` and positive `G_A` establish local functional conflict. The multi-level extension locates `z_P*`, `z_G*`, and `z_C*`.

## Critical negative-control principle

```text
multifunctionality != conflict.
```

A trait can serve two functions while both functions favor the same state. Positive SCH inference therefore requires opposing causal geometry, not merely two functions.

## Real-world evidence role

The PRISMA programme and targeted primary-source audits remain a **real-world evidence spine**. They show that shared traits affect multiple functions, opposing selection and compromise occur, interaction weights redirect evolution, and partial decoupling occurs. They do not define the SCH estimand.

Current bounded status:

```text
REAL_WORLD_MULTIFUNCTIONALITY_RECOVERED
CASE_LEVEL_COMPROMISE_RECOVERED
STATE_SPECIFIC_CAUSAL_COMPROMISE_ANALYZER_READY
OPTIONAL_CONTEXT_STABLE_COMPONENT_OPTIMUM_UPGRADE_READY
PURE_FUNCTION_OPTIMA_NOT_IDENTIFIED_BY_DEFAULT
COMPLETE_CAUSAL_COMPROMISE_EXPERIMENT_NOT_YET_EXECUTED
HISTORICAL_INTEGRATION_TO_MODULARIZATION_NOT_YET_IDENTIFIED.
```

## Current execution strategy

```text
Dalechampia
-> conditional first-choice causal compromise-surface system
-> Mexican case-level conflict recovered
-> Costa Rica shows conflict is not species-wide
-> qualify a conflict-active population / season first
-> validate reversible z manipulation and selective G0/G1

Nicotiana attenuata
-> first-choice local shared-cue mechanism system
-> strong hand-off into the later architecture chapters once a common fitness-scale receipt exists

Castilleja linariaefolia
-> high-value fallback, but its focal manipulation and selective antagonist control still require Stage 0

Platycodon / aligned-orientation systems
-> negative controls.
```

The Dalechampia execution chain is:

```text
population qualification
-> reversible multi-level z validation
-> controlled adult-weevil exposure
-> selective G0/G1 validation
-> 5 z x 2 P x 2 G
-> causal compromise receipt
-> optional context-stable component-optimum upgrade.
```

## SCH -> BALANCE -> BITA

SCH defines the **left-hand boundary** of the middle world.

Default empirical handoff:

```text
SCH
z_P*, z_G*, z_C*
+ causal compromise geometry
+ fitness-scale conflict budget L when identified
        ↓
BALANCE
requires L > 0
combines L with the BITA-facing architecture margin Phi=sL-K
studies L > 0 and Phi < 0
-> middle-world position, two-sided depth, reserve, topology, persistence
        ↓
BITA
studies Phi = 0 and Phi > 0
-> dimensional release
-> preferential functional loading
-> joint fitness improvement
-> mechanism allocation.
```

Optional stricter lane:

```text
SCH component contrasts identify context-stable z_F1*
-> upgraded receipt exports identified_pure_function_optima.z_F1
-> BALANCE retains the same distinction between state-specific and pure-function reference lanes
-> BITA may additionally test release toward pure z_F1*.
```

State-specific and pure-function release remain separate.

The key programme rule is:

```text
SCH says whether conflict exists and where the one-coordinate compromise lies.
BALANCE asks what ecological world exists while conflict exists but differentiation still loses.
BITA asks what happens at and beyond the architecture crossing.
```

See `docs/THREE_WORLD_PROGRAMME_V1.md`.

## Canonical reader path

- `manuscript/MANUSCRIPT_SHARED_TRAIT_COMPROMISE.md` — canonical Chapter-1 manuscript
- `docs/THREE_WORLD_PROGRAMME_V1.md` — Chapter 1 -> Chapter 2 -> Chapter 3 interface
- `docs/SCH_CAUSAL_COMPROMISE_SURFACE_ANALYSIS_V1.md` — state-specific optimum analyzer contract
- `docs/SCH_PURE_FUNCTION_OPTIMA_UPGRADE_V1.md` — optional context-stable component-optimum promotion
- `docs/SCH_MULTI_LEVEL_COMPROMISE_IDENTIFICATION_V1.md` — multi-level causal design
- `docs/SHARED_TO_DIFFERENTIATED_QUADRATIC_BRIDGE_V1.md` — theory/empirical bridge
- `docs/SCH_EXECUTION_SPINE_V1.md` — end-to-end execution
- `scripts/analyze_sch_compromise_surface.py` — full compromise analyzer
- `scripts/identify_sch_pure_function_optima.py` — optional pure-function upgrade
- `scripts/evaluate_dalechampia_stage0.py` — Stage-0 qualification
- `docs/CHAPTER_1_TO_BITA_CHAPTER_2_POSITIONING.md` — retained legacy two-chapter positioning/provenance
- `empirical/architecture/SCH_COMPROMISE_PREDICTION_LEDGER_V1.csv` — prediction contract
- `empirical/one_trait_shared_cue/` and `empirical/prisma/` — real-world evidence.

## Immediate empirical programme

```text
Stage 0  qualify one conflict-active context
Stage 1  validate multi-level z and selective functional interventions
Stage 2  recover z_P*, z_G*, z_C*
Stage 3  test causal optimum shifts and component gradients
Stage 3b optionally test context-stable component optima -> z_F1*, z_F2*
Stage 4  test evolutionary maintenance / movement
Stage 5  export the compromise geometry and fitness-scale conflict budget to BALANCE
Stage 6  retain matched contexts for later BITA architecture tests.
```

SCH is organized around **the ecology and evolution of compromise under multifunctional trait integration**. The literature establishes that the mechanism is biologically real; the decisive chapter result is the causal reconstruction of how competing functional demands shape one shared coordinate. BALANCE and BITA then ask what happens between, at, and beyond the architecture boundary without retroactively changing the SCH estimand.
