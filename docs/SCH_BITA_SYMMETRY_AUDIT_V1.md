# SCH–BITA symmetry audit v1

## Decision

The chapter pair is now conceptually symmetric at the trait-architecture level, but not yet symmetric in empirical depth or submission readiness.

```text
mathematical interface:          PASS
programme-level scope:           PASS
worked-case separation:          PASS
historical claim ceiling:        PASS
figure-argument symmetry:        PASS at plan level
empirical parameter symmetry:    PARTIAL
submission-package symmetry:     NOT YET
```

## 1. Programme-level question

### SCH / Chapter 1

> How do conflicting functions resolve selection while they remain coupled on one trait, and what residual conflict remains after the best one-axis phenotype is chosen?

### BITA / Chapter 2

> When does relaxing that shared-axis constraint by trait differentiation pay, and how can the mechanism of the resulting multi-trait phenotype be identified?

**Assessment: PASS.** The questions are complementary rather than redundant.

## 2. Shared mathematical objects

Chapter 1:

```text
L_S(z) = l1(z) + l2(z)
z*     = argmin L_S(z)
L_S*   = L_S(z*)
```

Chapter 2:

```text
R >= 0
Delta_arch = R-K
Delta_arch > 0 <=> K<R
```

Quadratic handoff:

```text
SCH:
z* = (w1 theta1 + w2 theta2)/(w1+w2)
L_S* = [w1w2/(w1+w2)](theta1-theta2)^2

BITA:
R = s L_S*
Delta_arch = s L_S* - K
```

**Assessment: PASS.** `L_S*` is the exact cross-chapter interface.

## 3. What each chapter holds fixed

### SCH

Architecture is fixed to one shared coordinate. Selection can alter position, functional weights, context, frequencies or population means, but the general Chapter 1 comparison does not require a new axis.

### BITA

The shared architecture is the baseline. The phenotype space is enlarged to allow partial separation, residual coupling and additional architecture cost.

**Assessment: PASS.** The chapters differ by one controlled modelling operation: relaxing the shared-axis constraint.

## 4. Floral worked cases

### SCH floral case

```text
z = A
W(A)=M(A)-G(A)-C(A)
```

Cue overlap makes one floral coordinate affect pollinator and antagonist channels.

### BITA floral case

```text
Delta_AD W = W11-W10-W01+W00
```

A second focal axis plus consumer interventions is used to ask why the multi-trait interaction occurs.

**Assessment: PASS with deliberate biological asymmetry.** The two floral cases are not supposed to be the same experiment. SCH measures conflict while one signal axis is shared; BITA studies function after multiple axes exist.

## 5. Main results

### SCH current result class

Current evidence supports bounded examples of:

- integrated stabilizing compromise;
- context-dependent polymorphism maintenance;
- population evolutionary redirection;
- partial cue/component decoupling.

### BITA current result class

Current theory supports:

- general nested-architecture weak dominance before extra fixed cost;
- `Delta_arch=R-K`;
- quadratic `R=sL_S*`;
- finite nonlinear robustness;
- mechanism-identification design after multiple axes exist.

**Assessment: PARTIAL symmetry.** SCH is currently stronger on heterogeneous real evolutionary outcomes; BITA is stronger on general formal architecture comparison. This is an evidence asymmetry, not a logical mismatch.

## 6. Parameter recoverability

### SCH

The general Chapter 1 model defines `z*` and `L_S*`, but the current cross-system evidence does not estimate them on one common quantitative scale. Pérez-Barrales supplies a direct observational compromise surface, while other cases support different outcome classes.

### BITA

The architecture model computes `R`, `s` and `Delta_arch` within the declared theoretical model, but empirical systems do not directly estimate the full parameter set or historical transition.

**Assessment: PARTIAL on both sides.** Neither chapter currently closes the complete within-system empirical bridge:

```text
measure z*, L_S*
-> observe/manipulate partial differentiation
-> estimate R, s, K
-> identify the ecological mechanism
```

This is the strongest future programme-level experiment.

## 7. Historical causation

### SCH ceiling

No replicated direct shared-cue -> private-cue historical transition is established. *Ficus* is `COMPOSITE_NEAR_L4`, not direct L4.

### BITA ceiling

A higher optimized value of a differentiated architecture does not establish that the lineage historically evolved by splitting one shared trait into two axes.

**Assessment: PASS.** Both chapters fail closed at the same historical boundary.

## 8. Figures

### SCH planned Main figures

1. one shared axis / two functional optima;
2. context shifts `z*` without changing architecture;
3. floral shared-cue mapping;
4. observed one-trait evolutionary outcomes and historical stop line;
5. `z*, L_S* -> BITA` handoff.

### BITA canonical Main figures

1. balance -> differentiated architecture;
2. architecture-cost boundary;
3. nonlinear robustness + real partial-differentiation anchors;
4. mechanism identification after multiple axes exist;
5. fragmented empirical identification frontier.

**Assessment: PASS at argument-structure level.** Chapter 1 Figures 1–3 explain the shared architecture; Chapter 2 Figures 1–3 explain relaxation of that architecture. Both end by connecting theory to evidence and the next inference gate.

## 9. Manuscript titles

Current pair:

```text
SCH:
How do conflicting functions balance on one trait?
Linking shared-trait compromise to evolutionary response

BITA:
When does a trait trade-off resolve by differentiation rather than compromise?
Linking trait architecture to mechanism identification
```

**Assessment: PASS, but not mechanically parallel.** This is preferable to forcing identical syntax because Chapter 1 emphasizes the location/maintenance of the shared solution whereas Chapter 2 emphasizes an architectural choice.

## 10. Submission readiness

### SCH

General trait-balance manuscript is an integration candidate. It does not yet have a focused reference audit, rendered submission package, final figures or page QA.

### BITA

Canonical Chapter 2 package is already built and visually validated at the pre-metadata stage.

**Assessment: NOT YET symmetric.** This is now the main practical difference between the two papers.

## 11. Highest-value next SCH work

Do not add another general hypothesis. The next paperization steps are:

1. map every admitted SCH evidence item to `shared-axis balance`, `context shift`, `one-axis alternative`, `partial decoupling`, or `historical transition`;
2. identify which sources actually contain enough information to estimate or bound a fitness-surface optimum, rather than merely a directional response;
3. build Figures 1–5 from the approved symmetry plan;
4. create a focused Chapter 1 reference spine and replace the current source-placeholder language;
5. build a review package and run page-by-page QA;
6. keep the targeted *Ficus* same-code experiment as a separate high-value historical gate rather than letting it dominate the general Chapter 1 paper.

## Bottom line

The chapter programme is now genuinely symmetric in logic:

```text
SCH = optimize within one architecture
BITA = test whether changing that architecture pays
```

The remaining asymmetry is empirical and editorial, not conceptual. SCH now needs the same paperization discipline that BITA has already received.
