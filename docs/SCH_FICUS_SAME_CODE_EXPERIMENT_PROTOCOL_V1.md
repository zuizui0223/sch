# SCH Ficus same-code receiver experiment protocol v1

## Purpose

The current Ficus bottleneck is not generic scent specificity. It is the missing matched receiver test:

```text
resolved pollinator-attractive chemical code
+ direct NPFW behaviour to that identical chemical coordinate
```

The protocol below converts the three priority cells into one common experimental contract. It is deliberately fail-closed: a nonsignificant NPFW response is not called a private channel.

## Common estimand

For each receiver guild and stimulus contrast, estimate the probability of choosing the coded stimulus over its declared control among decisive choices, while retaining no-choice frequency as a separate diagnostic. Tree, collection batch, date/time and assay batch must be retained so uncertainty can reflect dependence rather than treating all wasps as exchangeable.

The analysis then passes uncertainty intervals to `scripts/classify_ficus_same_code_receiver.py`.

Default no-preference coordinate:

```text
p0 = 0.50
```

Default behavioural-equivalence zone:

```text
0.40 <= p_NPFW(code) <= 0.60
```

The ±0.10 margin is a predeclared biological tolerance, not a universal constant. A different margin is allowed only if justified before seeing the focal result.

A useful planning benchmark is that, under independent decisive choices and a true response of 0.50, roughly 68 decisive choices give a nominal 90% normal-approximation interval with half-width about 0.10. This is **not** the final sample size: clustering, no-choice rates, tree/batch heterogeneity and the desired power for positive controls must be added prospectively.

## Required controls

Every same-code NPFW test must contain all three gates:

1. **Pollinator code replication.** The known pollinator must respond positively to the exact code in the current assay batch or an explicitly linked validation batch.
2. **NPFW responsiveness positive control.** The NPFW must respond to a biologically relevant host/stage cue so that a focal nonresponse is interpretable.
3. **Matched code test.** The NPFW is tested against exactly the pollinator-validated chemical coordinate, not merely whole-host odour, a receptor-binding assay, or host association.

Classification is then:

```text
SAME_CODE_INTERCEPTION
SAME_CODE_AVOIDANCE
BEHAVIORAL_NONRESPONSE_EQUIVALENT
INCONCLUSIVE_SAME_CODE_RESPONSE
```

`BEHAVIORAL_NONRESPONSE_EQUIVALENT` supports behavioural privacy only at the declared assay scale. It does not prove chemical imperceptibility.

## Experiment A — Ficus semicordata

### Biological coordinate

```text
code = 4-methylanisole
pollinator = Ceratosolen gravelyi
NPFW targets = Platyneura cunia, Sycoscapter trifemmensis, plus other identified abundant NPFWs when feasible
```

The key addition is timing. Existing field observations place *P. cunia* oviposition about 10 days after pollinator entry and *S. trifemmensis* 14–32 days after pollinator entry. NPFW assays should therefore use individuals and host-stage controls corresponding to their natural post-pollination windows rather than forcing every receiver into the receptive-stage pollinator window.

Minimum stimulus panel:

```text
4-methylanisole at headspace-calibrated natural dose
solvent / carrier control
stage-matched whole-host odour positive control
nonhost or stage-mismatched odour control where feasible
```

Primary question:

> Does a responsive NPFW intercept, avoid, or show equivalence-supported behavioural nonresponse to 4-methylanisole itself?

The temporal result and chemical result are coded separately. Delayed oviposition does not count as chemical nonresponse.

## Experiment B — Ficus carica

### Biological coordinate

```text
code = validated four-VOC blend at the pollinator-attractive ratio
pollinator = Blastophaga psenes
NPFW target = Philotrypesis caricae, with additional identified exploiters if available
```

Minimum stimulus panel:

```text
validated four-VOC ratio
at least two ratio-perturbed blends that abolish/reduce pollinator attraction
whole receptive fig odour positive control
solvent / carrier control
```

The ratio-perturbation treatments are essential because the claim concerns a ratio code rather than generic detection of the same four compounds.

Primary questions:

1. Can the pollinator specificity of the ratio be replicated in the current assay?
2. Does the NPFW respond to the exact attractive ratio?
3. Does the NPFW discriminate the attractive ratio from the perturbed ratios in the same direction as the pollinator?

A response to all component compounds without ratio specificity is not the same-code result.

## Experiment C — Ficus hispida

This system requires two stages.

### Stage 1: resolve the pollinator code

Use the receptive bouquet as the positive reference and progressively test synthetic candidate blends, omission blends and ratio perturbations until a minimal pollinator-attractive code is identified with uncertainty. The code is not declared resolved merely because a whole bouquet is species specific.

### Stage 2: matched receiver assay

Once the pollinator code is frozen, test known *Philotrypesis* NPFWs against that identical code, its omission/perturbation controls, whole receptive odour and solvent control.

Primary question:

> Does the known whole-odour dual-audience response persist on the minimal pollinator-attractive chemical coordinate?

## Analysis hierarchy

The order of inference is fixed:

```text
receiver assay validity
-> pollinator code replication/resolution
-> NPFW same-code behavioural classification
-> species-level shared/private/code-interception state
-> only then phylogenetic state reconstruction
```

Do not reconstruct `shared` versus `private` states from host association, receptor binding, timing alone, or whole-odour response when the key code is unresolved.

## Promotion rule toward L4

One successful same-code assay closes a contemporary matched receiver cell but does not create L4. Historical promotion additionally requires:

- multiple independently coded shared/private/code-interception states on the same chemical definition;
- ancestral-state reconstruction;
- repeated transitions rather than one tip difference;
- pollinator and exploiter regime information on those branches;
- tests against section, reproductive system, phylogeny and available abiotic/geographic alternatives.

Until then the Ficus result remains `COMPOSITE_NEAR_L4`.
