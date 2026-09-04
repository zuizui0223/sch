# Shared Trait Compromise / SCH

SCH is Chapter 1 of a trait-architecture programme paired with [BITA](https://github.com/zuizui0223/bita).

```text
Chapter 1 / SCH
function 1 ---\
               >--- shared trait z ---> compromise / balance
function 2 ---/

Chapter 2 / BITA
shared compromise
      ↓
function 1 ---> trait x
function 2 ---> trait y
      ↓
functional differentiation / modularization
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

Pure `z_F1*` / `z_F2*` require an additional identifying assay.

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
-> strongest direct hand-off into BITA

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
-> causal compromise receipt.
```

## SCH -> BITA

Default empirical handoff:

```text
SCH
z_P*, z_G*, z_C*
-> causal compromise

BITA
x,y
-> preferential functional loading
-> x* moves toward z_P* by default
-> joint fitness improvement
-> 16-cell mechanism allocation.
```

Optional stricter lane:

```text
SCH independently identifies z_F1*
-> BITA additionally tests release toward pure z_F1*.
```

State-specific and pure-function release are kept separate.

## Canonical reader path

- `manuscript/MANUSCRIPT_SHARED_TRAIT_COMPROMISE.md` — canonical Chapter-1 manuscript
- `docs/SCH_CAUSAL_COMPROMISE_SURFACE_ANALYSIS_V1.md` — state-specific optimum analyzer contract
- `docs/SCH_MULTI_LEVEL_COMPROMISE_IDENTIFICATION_V1.md` — multi-level causal design
- `docs/SHARED_TO_DIFFERENTIATED_QUADRATIC_BRIDGE_V1.md` — theory/empirical bridge
- `docs/SCH_EXECUTION_SPINE_V1.md` — end-to-end execution
- `scripts/analyze_sch_compromise_surface.py` — full compromise analyzer
- `scripts/evaluate_dalechampia_stage0.py` — Stage-0 qualification
- `docs/CHAPTER_1_TO_BITA_CHAPTER_2_POSITIONING.md` — chapter bridge
- `empirical/architecture/SCH_COMPROMISE_PREDICTION_LEDGER_V1.csv` — prediction contract
- `empirical/one_trait_shared_cue/` and `empirical/prisma/` — real-world evidence.

## Immediate empirical programme

```text
Stage 0  qualify one conflict-active context
Stage 1  validate multi-level z and selective functional interventions
Stage 2  recover z_P*, z_G*, z_C*
Stage 3  test causal optimum shifts and component gradients
Stage 4  test evolutionary maintenance / movement
Stage 5  hand the identified compromise to BITA.
```

SCH is organized around **the ecology and evolution of compromise under multifunctional trait integration**. The literature establishes that the mechanism is biologically real; the decisive chapter result is the causal reconstruction of how competing functional demands shape one shared coordinate.
