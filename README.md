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
