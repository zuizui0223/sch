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

## Source-anchored bioassay contract

The matched historical question requires the **same chemical coordinate**, not necessarily one universal apparatus for every receiver. The best design is therefore to preserve the established assay logic for each receiver class and add the missing same-code treatment.

### Pollinator benchmark: F. semicordata / Chen et al. 2009

The published *Ceratosolen gravelyi* assay used a glass Y-tube with an 8-cm stem, 9-cm arms at 55 degrees and 1.5-cm internal diameter. Cleaned and humidified charcoal-filtered air was supplied at 200 mL/min to each arm. Assays were run at approximately 26 C. Each wasp had 5 min; a choice required crossing 1 cm beyond the junction and remaining there for more than 1 min. Individuals failing to reach the decision line within 5 min were retained as `no choice`. Treatment sides were switched every four assays and the olfactometer was rinsed with ethanol after each assay.

This geometry/decision rule is the **source-faithful pollinator validation lane** for 4-methylanisole. The new NPFW assay does not have to force larger parasitoid species into this narrower apparatus if their established behavioural assay requires different geometry.

### NPFW benchmark: F. hispida / F. racemosa / Proffit et al. 2007

The established NPFW odour-choice assay used a larger glass Y-tube: 4-cm diameter, 14-cm lateral arms and an 8-cm basal stem. Humidified activated-charcoal-purified air entered each arm at 75 mL/min and was extracted from the basal stem at 95 mL/min. Figs were held in odour-free bags; visual cues were blocked. Y-tubes were cleaned with acetone before trials, control/odour position was reversed on each successive trial, and air-vs-air controls were interleaved. Crucially, NPFW species were tested against fig odours corresponding to the phenological stage they naturally exploit.

This is the **source-faithful NPFW validation lane**. For *F. semicordata*, the stage-matched whole-host positive control should therefore follow the natural delayed oviposition window of each target NPFW. The novel manipulation is addition of 4-methylanisole itself at a calibrated dose, not replacement of the NPFW assay by the pollinator apparatus.

### Ratio-code benchmark: F. carica / Proffit et al. 2020

The published *Blastophaga psenes* tests used a glass Y-tube 40 mm in diameter with 200-mm lateral arms and a 150-mm central arm. Odour sources were placed in 500-mL glass containers; charcoal-purified, humidified air entered at 200 mL/min per arm. Source position was inverted on each successive trial. Air was allowed to flow for 1 min before introduction, each individual was observed for 10 min, and individuals remaining in the departure/central section after 10 min were classified as no-choice and excluded from the paper's exact-binomial choice test. Between 42 and 60 wasps were tested per treatment and no more than 25 individuals per treatment were tested per day.

The key chemical control is not simply component presence. Four antennally active compounds — benzyl alcohol, (S)-linalool, (Z)-linalool-oxide (furanoid), and (E)-linalool-oxide (furanoid) — were delivered in a source-calibrated blend. The attractive B1 blend approximated receptive-fig proportions; proportion perturbations altered attraction. Synthetic dispensers were calibrated to release rates comparable to one receptive fig.

For the new NPFW experiment, the **exact frozen B1-style ratio and release-rate calibration** must be copied from the source preparation record used in the replication. A generic four-compound mixture is not the same code.

## Cross-assay harmonization

Apparatus-specific choice definitions remain recorded rather than silently pooled. The common analysis variable is a behavioural choice probability on a declared two-source contrast plus a separately retained no-choice rate. Primary reports must therefore provide, for each receiver and assay block:

```text
species / receiver guild
source tree and collection batch
fig developmental stage
Y-tube geometry / flow regime
stimulus identity and calibrated release rate
left/right assignment sequence
number introduced
number choosing code
number choosing control
number no-choice
assay day / block
```

A source-faithful assay can be analyzed with a modern hierarchical/binomial model, but historical no-choice exclusion must be reproduced as a sensitivity lane if direct replication of the published pollinator result is being claimed. The main new same-code inference should retain no-choice information rather than make the result depend on post-choice filtering.

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

The source pollinator assay demonstrated attraction to 4-methylanisole over a broad concentration range and showed that blends lacking the compound were unattractive. The replication should nevertheless center the NPFW test on measured stage-/system-relevant headspace release rather than choosing a favourable dose after observing NPFW behaviour.

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
validated four-VOC ratio at source-calibrated release rates
at least two predeclared ratio-perturbed blends from the validated perturbation family
whole receptive fig odour positive control
solvent / empty-source control
```

The ratio-perturbation treatments are essential because the claim concerns a ratio code rather than generic detection of the same four compounds. The published pollinator work showed B1 attraction comparable to receptive fig odour and loss/reduction of attraction for several altered proportions; those source-defined perturbations should be preferred to post hoc newly invented ratios.

Primary questions:

1. Can the pollinator specificity of the ratio be replicated in the current assay?
2. Does the NPFW respond to the exact attractive ratio?
3. Does the NPFW discriminate the attractive ratio from the perturbed ratios in the same direction as the pollinator?

A response to all component compounds without ratio specificity is not the same-code result.

## Experiment C — Ficus hispida

This system requires two stages.

### Stage 1: resolve the pollinator code

Use the receptive bouquet as the positive reference and progressively test synthetic candidate blends, omission blends and ratio perturbations until a minimal pollinator-attractive code is identified with uncertainty. The code is not declared resolved merely because a whole bouquet is species specific.

Use the established NPFW stage-sensitive Y-tube logic as the behavioural benchmark, while calibrating synthetic dispensers using the release-rate logic demonstrated in the *F. carica* study. Freeze the candidate code before testing *Philotrypesis* on it.

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

## Primary method provenance

- Chen et al. 2009, Functional Ecology, doi:10.1111/j.1365-2435.2009.01622.x — *F. semicordata* pollinator Y-tube assay and 4-methylanisole validation.
- Proffit et al. 2007, Journal of Animal Ecology, doi:10.1111/j.1365-2656.2007.01213.x — NPFW stage-sensitive Y-tube assay architecture.
- Proffit et al. 2020, Scientific Reports, doi:10.1038/s41598-020-66655-w — *F. carica* pollinator Y-tube assay, four-VOC ratio perturbation and calibrated synthetic dispensers.
