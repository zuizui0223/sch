# Chapter 1 to Chapter 2 positioning

## Dissertation-level question

How do plants evolve floral signals when the same phenotype affects both mutualists and antagonists, and when can an additional defensive trait improve, release or reverse the resulting fitness constraint?

The two repositories now form one experimental identification programme:

```text
Chapter 1 — SCH
identify the one-trait dual-audience conflict

Chapter 2 — BITA
add defence and identify whether/how that conflict is released
```

The literature evidence in both chapters is retained as biological grounding and mechanism recurrence evidence. It does not substitute for the chapter-specific identifying experiment.

## Chapter 1 — SCH: identify why attraction becomes conflicted

SCH begins with one predeclared attraction/display coordinate `A` and crosses it with antagonist state `G` and pollinator state `P`:

```text
A x G x P
8 cells
```

For one common reproductive outcome,

```text
d[g,p] = W[1,g,p] - W[0,g,p].
```

The core channel contrasts are

```text
M_A(g) = d[g,1] - d[g,0]
         pollinator-mediated contribution

G_A(p) = d[0,p] - d[1,p]
         antagonist-mediated loss

B_A    = d[0,0]
         consumer-independent remainder

J_A    = d[1,1] - d[1,0] - d[0,1] + d[0,0]
         A x G x P channel-dependence diagnostic.
```

The biological shared-cue claim requires two layers.

1. **Informational overlap:** pollinators and antagonists use the same validated sensory/display coordinate of `A`.
2. **Functional conflict:** pollinator access makes the reproductive effect of `A` more positive while antagonist access makes it less positive.

Thus SCH does not stop at showing that both audiences visit the same flower phenotype. It asks whether the two audiences make opposing causal contributions to the fitness value of that same manipulated coordinate.

### Realized constraint

Under natural pollinator access,

```text
G_A(1) = d[0,1] - d[1,1].
```

If `G_A(1) > 0`, antagonist presence flattens the attraction-fitness effect relative to antagonist removal. Stronger functional levels are:

```text
attenuation:       0 < d[1,1] < d[0,1]
release:           d[1,1] <= 0 < d[0,1]
strict reversal:   d[1,1] < 0 < d[0,1].
```

The full contract is `docs/SCH_MECHANISM_IDENTIFICATION_DESIGN_V1.md`.

## What the SCH literature layer now does

The systematic review and targeted audits no longer define the identity of Chapter 1. Their role is to show that the mechanism is ecologically realistic and to locate missing identifying measurements.

The literature layer supplies:

- recurrent `A -> pollination` and `A -> antagonism` routes;
- same-code or same-display receiver responses in real systems;
- documented compromise, polymorphism, population-level evolutionary change and partial decoupling;
- evidence that complete same-coordinate manipulation + both consumer channels + common reproduction is rare;
- historical candidate systems, especially *Ficus*, for later shared-to-private reconstruction.

Through V20, the frozen systematic cohort has 868 records, 405 title/abstract decisions and 117 primary includes. Two studies satisfy the strict linked measurement architecture, but neither closes the central positive dual-audience chain. These results support **mechanism reality and design need**, not a substitute cross-study mechanism estimate.

The current SCH status is therefore:

```text
REAL_WORLD_MECHANISM_COMPONENTS_RECOVERED
COMPLETE_SCH_CHANNEL_IDENTIFICATION_NOT_YET_EXECUTED
```

## Chapter 2 — BITA: add a defence coordinate

BITA begins from the conflict identified by SCH and asks whether a distinct antagonist-reducing trait `D` changes the reproductive effect of attraction.

For the four trait states,

```text
A0 = W10 - W00
     attraction effect when defence is low

A1 = W11 - W01
     attraction effect when defence is high

Delta_AD W = W11 - W10 - W01 + W00
           = A1 - A0
           = rho_delta - iota_delta - kappa_delta.
```

The four-cell trait surface supports nested functional outcome claims:

```text
Level 1 — positive interaction relief
Delta_AD W > 0

Level 2 — constraint release
A0 <= 0 and A1 > 0

Level 3 — strict sign reversal
A0 < 0 and A1 > 0.
```

A positive total interaction decides the Level-1 escape inequality on the declared outcome scale, but it does not identify the mechanism allocation.

## BITA mechanism allocation

BITA extends the SCH design by crossing the two traits with both consumer states:

```text
A x D x antagonist x pollinator
16 cells.
```

Its mechanism problem is to allocate the `A x D` reproductive interaction among:

```text
rho_delta    antagonist relief
iota_delta   pollinator interference
kappa_delta  independently validated remaining joint channel.
```

Selective crossed interventions, pollinator-absent baseline handling and the `A x D x G x P` diagnostic are needed for point identification of the biotic channels. The remaining residual must not be called `kappa` by subtraction; a joint construction/allocation channel requires an independent assay.

## The chapter bridge

The experimental logic is now deliberately nested:

```text
SCH Stage 0
validate one A coordinate and receiver access
        ↓
SCH Stage 1-2
A x G x P
identify pollinator gain, antagonist loss and realized constraint
        ↓
SCH Stage 3-4
independent remainder assay + evolutionary extension
        ↓
BITA Stage 1
A x D reproductive surface
ask whether D improves/releases/reverses attraction
        ↓
BITA Stage 2-3
A x D x G x P + independent cost assay
identify why the escape outcome occurs.
```

This nesting is the main conceptual value of the sister projects. Chapter 2 is not merely a more complicated version of Chapter 1; it asks whether a new trait dimension changes the constraint that Chapter 1 has already identified.

## Informational versus functional escape

The programme distinguishes two different ways plants can escape dual-audience conflict.

| Escape form | What changes | SCH/BITA role |
|---|---|---|
| **Informational / architectural escape** | the floral signal becomes more receiver-specific through component partitioning, conditional expression, timing or private cues | SCH evolutionary extension |
| **Functional defence-mediated escape** | antagonists may still detect `A`, but a distinct `D` reduces the reproductive penalty while preserving attraction benefit | BITA core |

Therefore BITA can release the functional cost of cue sharing even if the antagonist continues to detect the attraction cue. Conversely, a private cue can reduce receiver overlap without implying any particular `A x D` interaction.

## Current empirical bridge

The broader *Nicotiana attenuata* programme remains the highest-information composite bridge because separate studies recover attraction effects on pollination and antagonism, an `A x D`-like reproductive factorial, and flower-specific defence biology. However, these papers cannot be treated as cells of one complete experiment.

The programme remains:

```text
PROGRAM_COMPOSITE_NEAR_COMPLETE
DIRECT_COMPLETE_CHAIN_NOT_ESTABLISHED.
```

The direct closure requires one invariant `A`, one independently validated flower-restricted `D`, both consumer channels, a common reproductive outcome and compatible uncertainty in the same experimental chain.

## Joint claim ceiling

Together SCH and BITA support a stronger research programme than either literature synthesis alone:

> Real floral traits operate under recurrent mutualist-antagonist conflict; SCH supplies a selective design to identify how that conflict constrains attraction on one coordinate, and BITA supplies the nested design to test whether an added defence coordinate releases the constraint and to identify the mechanism of that release.

Three intersections remain open before the full programme is empirically closed:

1. a complete SCH same-coordinate `A x antagonist x pollinator` mechanism experiment;
2. a BITA uncertainty-identified positive/releasing `A x D` outcome with clean trait scope;
3. a complete BITA channel allocation with an independent remaining-cost assay.

Historical shared-cue -> private-cue reconstruction is a later evolutionary extension, not a prerequisite for establishing the contemporary SCH -> BITA mechanism sequence.
