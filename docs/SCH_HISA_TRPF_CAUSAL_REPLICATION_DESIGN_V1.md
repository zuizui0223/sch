# SCH HisA/TrpF causal replication design v1

## Goal

Convert the HisA/TrpF cross-domain adaptive-conflict anchor into a genuine SCH-style causal test without pretending that multidimensional sequence space is automatically one shared trait axis.

## Shared coordinate

Construct an **isogenic single-copy allele panel** of at least five preselected HisA-derived variants spanning a one-dimensional biochemical activity-allocation coordinate.

Freeze `z` before the growth experiment using an independent biochemical assay, for example a monotone transform of the ratio of HisA and TrpF catalytic performance:

```text
z = log[(HisA catalytic-performance proxy + epsilon)
        /(TrpF catalytic-performance proxy + epsilon)].
```

The exact transform and `epsilon` must be frozen before growth outcomes are inspected.

To support a one-axis interpretation, the panel must use:

```text
same chromosomal locus
same copy number = 1
same promoter/regulatory context
bounded protein-abundance variation
no secondary adaptive mutations outside the engineered allele.
```

If abundance/stability differences are too large, the strong scalar-`z` interpretation fails and the panel remains only a multidimensional adaptive-conflict system.

## Functional-weight interventions

Use amino-acid supplementation to toggle biosynthetic demand while keeping the engineered allele panel unchanged.

Conceptual factorial:

```text
H0 = histidine supplied       -> HisA demand neutralized
H1 = histidine not supplied   -> HisA demand active
T0 = tryptophan supplied      -> TrpF demand neutralized
T1 = tryptophan not supplied  -> TrpF demand active.
```

This gives:

```text
z x H x T
```

with four demand states.

## Common fitness outcome

Primary outcome:

```text
exponential growth rate / Malthusian fitness
```

measured in otherwise matched media and normalized only by a preregistered procedure.

Secondary checks:

```text
lag time
stationary yield
protein abundance
HisA-specific activity proxy
TrpF-specific activity proxy.
```

## SCH estimands

Fit the same allele panel in all four demand states and recover:

```text
z_H*   = H1 T0 function-1-facing optimum
z_T*   = H0 T1 function-2-facing optimum
z_C*   = H1 T1 combined optimum
z_00*  = H0 T0 baseline optimum / nuisance reference.
```

Primary causal SCH signatures:

```text
z_H* and z_T* meaningfully separated;
z_C* supported inside their interval when an interior compromise is predicted;
neutralizing T shifts the optimum toward z_H*;
neutralizing H shifts the optimum toward z_T*;
component gradients at z_C* oppose one another;
positive fitness-scale shared conflict budget L.
```

The existing generic SCH multilevel causal-surface and conflict-budget logic can be reused after the microbial adapter preserves these state semantics.

## Strong falsifiers

- the single-copy allele panel cannot be represented by one preregistered biochemical allocation axis;
- H/T supplementation changes allele abundance or unrelated physiology in a variant-specific way large enough to destroy the weight interpretation;
- state optima are aligned rather than opposed;
- optimum shifts under H/T toggles do not move in opposite predicted directions;
- the bounded conflict budget includes zero.

## Why this is independent of BITA and PAYOFF

No duplicated copy is required for the SCH test. The test asks only whether one multifunctional molecular coordinate has opposed function-specific optima.

No architecture-frequency manipulation or `eta` is involved.

## Promotion

A positive experiment can promote HisA/TrpF from:

```text
G2 cross-domain adaptive-conflict anchor
```

to:

```text
G2 cross-domain causal SCH replication
```

only if the scalar-axis and selective-demand gates pass.
