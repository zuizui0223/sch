# SCH Nicotiana Stage 0-1 pilot contract v1

## Decision

*Nicotiana attenuata* is the first-choice current biological system for attempting direct SCH mechanism closure because the existing programme already contains the closest combination of a manipulable attraction coordinate, same-system pollinator and antagonist responses, reproductive outcomes, and a direct bridge to BITA.

This is a **candidate execution decision**, not a claim that the existing literature already supplies the SCH 8-cell estimate.

```text
FIRST_CHOICE_SCH_EXECUTION_SYSTEM: NICOTIANA_ATTENUATA
CURRENT_STATUS: L0_PROGRAMME_SUPPORT_RECOVERED; SELECTIVITY_GATE_OPEN
```

A dedicated primary-source recovery (`docs/SCH_NICOTIANA_STAGE0_PRIMARY_SOURCE_RECOVERY_V1.md`) now closes two Stage-0 biological-reality cells at programme level: the benzylacetone axis affects pollinator-mediated reproduction and the same manipulated scent axis affects hawkmoth oviposition. The next work should therefore not repeat generic same-cue discovery. It should close the selective `P/G` intervention and antagonist-response-to-reproductive-loss cells.

## Current Stage-0 recovery state

```text
S0.1  stable A0/A1 chemical contrast                  PARTIAL
S0.2  pollinator-side response to A                   RECOVERED at programme level
S0.3  antagonist-side response to same A              RECOVERED at programme level
S0.4  workable P intervention                         PARTIAL FEASIBILITY
S0.5  workable G intervention                         OPEN
S0.6  acceptable cross-channel contamination         OPEN / CRITICAL
S0.7  one common reproductive endpoint in all cells  PARTIAL FEASIBILITY
```

Thus *Nicotiana* is already a source-grounded **L0 informational-overlap candidate**. It is not yet an L1 functional-conflict result because oviposition has not been converted into antagonist-mediated reproductive loss under a selective `G` intervention on the common `W` scale.

## Why this system ranks first

The programme already supplies four unusually valuable ingredients:

1. floral benzylacetone provides a biologically interpretable attraction/scent coordinate;
2. the same programme contains pollinator-mediated reproduction and hawkmoth oviposition responses to attraction/reward manipulations;
3. a manipulated attraction-by-defence-like reproductive surface already exists at programme level;
4. the system can extend directly into BITA once a distinct, stable defence coordinate is validated.

The decisive weakness is also clear: hawkmoths can occupy both pollinator and antagonist roles, so role labels alone do not supply selective `P` and `G` interventions. SCH therefore begins with a selectivity pilot rather than immediately committing to the full confirmatory 8-cell design.

## Declared Stage-0 attraction coordinate

The preferred initial `A` candidate is floral benzylacetone emission.

The operational requirement is not merely `BA present` versus `BA absent`. The experiment must verify a stable quantitative contrast across all consumer treatments:

```text
A0 = low / suppressed benzylacetone
A1 = natural or restored benzylacetone
```

Before promotion to Stage 1, measure or verify that the manipulation does not materially alter at least:

- nectar amount / sugar reward;
- flower opening and longevity;
- corolla morphology and presentation;
- flowering time within the trial;
- the later candidate `D` coordinate used by BITA.

Existing source evidence shows that benzylacetone and nectar can be experimentally uncoupled, which supports axis feasibility, but the exact new Stage-0 manipulation still requires its own manipulation checks. If the attraction manipulation shifts multiple receiver-facing coordinates, the declared estimand becomes a composite floral-attraction package and must be labelled as such rather than benzylacetone-specific.

## Stage 0A — same-coordinate receiver validation

The first biological question is informational:

> Do the focal pollinating and antagonistic receiver states respond to the same declared benzylacetone contrast?

Primary-source recovery already supports this at programme level: benzylacetone manipulation affects pollinator-mediated outcrossing and hawkmoth oviposition on the same experimentally varied scent axis. Therefore `S0.2` and `S0.3` are no longer generic discovery tasks.

The execution experiment should still verify the chosen `A0/A1` contrast if the manipulation, receiver context or exposure protocol differs materially from the historical experiments. A nonsignificant antagonist test is not evidence of privacy.

## Stage 0B — selective intervention audit

This is now the dominant Stage-0 bottleneck. Before the 8-cell reproductive experiment, test candidate intervention routes for `P` and `G`.

Candidate strategies include:

```text
P manipulation
- controlled hand-pollination versus pollinator access
- temporal access windows that isolate pollination
- access geometry that preserves oviposition exclusion if biologically valid

G manipulation
- egg/oviposition exclusion after standardized pollination
- removal of eggs or early antagonist stages before reproductive damage
- temporal exclusion targeted to the oviposition window
- focal-antagonist access cages only if they leave pollinator service unchanged
```

Each proposed intervention must be tested against two selectivity criteria:

1. the intended route changes strongly enough to be biologically useful;
2. the non-target route and the `A` coordinate remain sufficiently stable.

There is no requirement that the exact natural receiver individual be assigned permanently to one role. The intervention must isolate causal pathways, not anthropomorphic guild labels.

A broad jasmonate or defence genotype is not sufficient as `G=0` if it also changes benzylacetone, nectar or other receiver-facing traits. The `G` manipulation should target antagonist exposure, establishment or damage as directly as feasible.

## Stage-0 promotion rule

Promote *Nicotiana* to the SCH 8-cell pilot only when all of the following are supported:

```text
S0.1  stable A0/A1 chemical contrast
S0.2  pollinator-side response to A demonstrated
S0.3  antagonist-side response to same A demonstrated
S0.4  workable P intervention identified
S0.5  workable G intervention identified
S0.6  intervention checks show acceptable cross-channel contamination
S0.7  one common reproductive endpoint can be followed in every cell
```

Current recovery means `S0.2` and `S0.3` are already supported at programme level, while `S0.4-S0.6` define the main experimental go/no-go decision.

If `S0.4-S0.6` fail because pollination and oviposition cannot be selectively separated, do not force the canonical decomposition. Retain *Nicotiana* as a coupled-receiver real-world L0 system and move the confirmatory SCH mechanism test to the next candidate system.

## Stage 1 — 8-cell mechanism pilot

After Stage 0 passes, cross:

```text
A x G x P

A0 G0 P0
A1 G0 P0
A0 G0 P1
A1 G0 P1
A0 G1 P0
A1 G1 P0
A0 G1 P1
A1 G1 P1
```

Use matched blocks and randomize `A` within the highest feasible level of replication. Preserve plant identity, block, date/night, flower position, receiver exposure and repeated measurements in the raw data.

The preferred common reproductive endpoint is one that can be measured identically in all eight cells. Candidate endpoints should be ranked in this order:

1. mature viable seed production per standardized flower;
2. mature capsule probability plus seed number as separate secondary components;
3. an earlier reproductive proxy only if mature reproduction is infeasible and the limitation is explicit.

Historical experiments establish feasibility of capsule- and seed-related outcomes in this system, but they do not close the required antagonist-response-to-reproductive-loss link under a selective `G` intervention. Raw visitation or oviposition is a mechanism mediator, not the primary common `W` endpoint.

## Stage-1 quantities to estimate

For every cell estimate

```text
W[a,g,p]
d[g,p] = W[1,g,p] - W[0,g,p]
```

and then

```text
M_A(g) = d[g,1] - d[g,0]
G_A(p) = d[0,p] - d[1,p]
B_A    = d[0,0]
J_A    = d[1,1] - d[1,0] - d[0,1] + d[0,0]
```

The pilot is not intended to make the final confirmatory claim. Its job is to estimate:

- cell means / probabilities;
- variance and overdispersion;
- plant/block/night clustering;
- retention and missingness;
- achievable intervention selectivity;
- plausible magnitudes of `M_A`, `G_A` and `J_A`.

Those estimates, not literature visitor effects, determine the confirmatory Stage-2 power calculation.

## Mechanism-success hierarchy

The result ladder is predeclared as:

```text
L0 informational overlap:
    both receiver states respond to the same A coordinate
    -> programme-level support now recovered for Nicotiana BA

L1 functional dual-audience conflict:
    M_A(g) > 0 and G_A(p) > 0 for predeclared states

L2 realized attraction constraint:
    G_A(1) > 0 under natural pollinator access

L2+ attenuation:
    0 < d[1,1] < d[0,1]

L2++ release under antagonist removal:
    d[1,1] <= 0 < d[0,1]

L2+++ strict reversal:
    d[1,1] < 0 < d[0,1]

L3 mechanism-resolved SCH:
    confirmatory 8-cell estimates + B_A + J_A + intervention validation
```

Do not make Stage-2/Stage-3 claims from visitor counts alone.

## Bridge to BITA

If *Nicotiana* passes SCH Stage 1/2, preserve exactly the same `A` coordinate for BITA. BITA then adds a separately validated `D` coordinate:

```text
SCH:   A x G x P
BITA:  A x D x G x P
```

The high-value programme-level outcome is therefore not two disconnected experiments. It is a nested design in which Chapter 2 adds one defence coordinate to a one-trait conflict already identified in Chapter 1.

Flower-specific jasmonate biology makes a downstream `D` search realistic, but broad upstream JA perturbation is disallowed as an orthogonal `D` when it also changes benzylacetone or nectar.

## Stop rules

Stop *Nicotiana* as the primary SCH mechanism system if any of the following holds after a serious Stage-0 attempt:

- benzylacetone cannot be manipulated without materially moving other declared attraction/reward coordinates;
- pollinator and antagonist pathways cannot be selectively perturbed enough to interpret `M_A` and `G_A`;
- antagonist response cannot be linked to reproductive loss on the common outcome scale;
- the required common reproductive endpoint is not feasible in all eight cells.

The prior stop rule based on generic failure to show antagonist response to BA is now lower priority because programme-level directional evidence for BA-associated oviposition is already recovered. It remains relevant only if the new execution context materially changes the `A` or receiver state.

A failed Stage 0 is informative system selection, not a falsification of SCH across nature.

## Current execution priority

```text
Priority 1  freeze the exact BA A coordinate and manipulation-check panel
Priority 2  close S0.4-S0.6 with selective P/G intervention tests
Priority 3  demonstrate antagonist response -> loss on one common W endpoint
Priority 4  run a small balanced 8-cell pilot only after selectivity passes
Priority 5  estimate mechanism-scale variance and power Stage 2
```

This ordering intentionally outranks additional broad literature screening for the mechanism-first SCH programme.