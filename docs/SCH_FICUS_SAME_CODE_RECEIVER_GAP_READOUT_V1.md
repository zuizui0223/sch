# SCH Ficus same-code receiver gap readout v1

## Decision

The fixed 32-species *Ficus* screen has now reached a narrower question than generic pollinator specificity or generic non-pollinating-wasp use of fig scent:

> **When a pollinator-attractive chemical code is experimentally resolved, do non-pollinating wasps respond to that same code?**

Three systems define the current frontier.

```text
F. semicordata : pollinator code resolved; NPFW timing resolved; same-code NPFW behaviour missing
F. carica      : pollinator code resolved; NPFW host association resolved; same-code NPFW behaviour missing
F. hispida     : dual-audience whole-odour behaviour resolved; exact synthetic pollinator code missing
```

The machine-readable ledger is `empirical/one_trait_shared_cue/FICUS_SAME_CODE_RECEIVER_GAP_V1.csv`.

## Ficus semicordata: private chemical code plus temporal separation

Chen et al. (2009; doi:10.1111/j.1365-2435.2009.01622.x) directly established 4-methylanisole as the key pollinator-attractive compound in receptive *F. semicordata*.

Yan, Peng & Yang (2012; doi:10.1016/j.chnaes.2012.02.003) independently observed the oviposition sequence of fig wasps using *F. semicordata*. The pollinator enters first. Among the directly quantified NPFWs, *Platyneura cunia* oviposits about 10 days after the pollinator and *Sycoscapter trifemmensis* 14–32 days after the pollinator.

This changes the ecological interpretation in a useful but bounded way:

```text
resolved pollinator-private chemical code: YES
NPFW presence in same host system:         YES
NPFW temporal separation:                  DIRECTLY OBSERVED
NPFW response to 4-methylanisole itself:   NOT TESTED
```

The system therefore reaches **L1 temporal/ecological separation plus a resolved private pollinator code**. It still does not show that NPFWs fail to detect, avoid, or ignore 4-methylanisole. Temporal separation and chemical privatization are compatible mechanisms, but they are not the same estimand.

## Ficus carica: ratio code plus a documented non-pollinator

The pollinator *Blastophaga psenes* responds to a precise ratio of four common receptive-fig VOCs; small changes to that ratio abolish attraction. This is a resolved ratio-specific pollinator code rather than a single unusual-compound private channel.

Doğanlar (2012; doi:10.3906/zoo-1111-3) directly documents *Philotrypesis caricae* as a non-pollinating fig wasp associated with *F. carica*. This closes the NPFW-presence cell but not the chemical-interception cell:

```text
resolved pollinator four-VOC code:         YES
NPFW associated with F. carica:            YES
NPFW response to validated four-VOC code:  NOT TESTED
```

Host association cannot be promoted to evidence that *P. caricae* intercepts or avoids the pollinator code.

## Ficus hispida: direct dual-audience behaviour before code resolution

*F. hispida* supplies the complementary geometry. Pollinating and non-pollinating *Philotrypesis* wasps respond directly to receptive fig odour. Recent work supports species-specific recognition through blends, but the pollinator-attractive synthetic code has not been resolved to the same standard as the 4-methylanisole or four-VOC systems.

Thus:

```text
direct pollinator response to receptive odour: YES
direct NPFW response to receptive odour:       YES
exact synthetic pollinator code:               UNRESOLVED
same-code receiver test:                       NOT YET DEFINABLE
```

The highest-value experiment here is code resolution first, followed by both receiver guilds against that exact synthetic coordinate.

## What is now positive

The same-radiation evidence has advanced beyond a vague analogy. *Ficus* contains:

- multiple experimentally resolved pollinator recognition architectures;
- direct NPFW exploitation of receptive scent in other species;
- a directly observed temporal separation between pollinator and NPFW oviposition in the same species that has the narrowest private chemical code;
- molecular differentiation between pollinating and non-pollinating receivers.

These results support the biological plausibility of **chemical plus temporal receiver separation** as a route out of shared-cue exposure.

## What remains zero

The decisive matched cell remains empty:

```text
resolved pollinator code + direct NPFW behaviour to that same code = 0 species
```

Consequently neither of these inferences is allowed:

```text
temporal delay -> NPFW cannot perceive private code          NO
NPFW host association -> NPFW intercepts pollinator code     NO
whole-odour NPFW response -> response to unresolved key code NO
```

And strict historical L4 remains:

```text
DIRECT_L4 = 0
NOT_EVALUABLE for repeated shared -> private transitions under both audiences
```

## Next decisive experiments/searches

1. *F. semicordata*: test NPFWs directly against 4-methylanisole and relevant controls, while preserving their natural post-pollination timing.
2. *F. carica*: test *Philotrypesis caricae* against the validated four-VOC ratio and ratio perturbations.
3. *F. hispida*: first resolve the minimal synthetic pollinator-attractive blend; then test pollinator and *Philotrypesis* on that identical code.
4. Only after matched chemical-coordinate receiver states exist should shared/private states be reconstructed on the 32-species phylogeny.

This is now a small, experimentally interpretable missing intersection rather than a broad literature gap.
