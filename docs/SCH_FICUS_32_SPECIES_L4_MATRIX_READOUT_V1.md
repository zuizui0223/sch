# SCH Ficus 32-species L4 candidate matrix readout v1

## Result

The Cao et al. 32-species receptive-scent comparison has been converted from a generic phylogenetic scaffold into a species-level L4 candidate matrix and overlaid with direct behavioural, electrophysiological and receiver-mechanism evidence.

A fixed-universe follow-up changed the diagnosis in an important way. The pollinator side is not limited to a single resolved chemical code: within the 32 Cao species, both *Ficus semicordata* and *F. carica* have key attractive chemical codes resolved by behavioural experiments. They represent different coding architectures. *F. semicordata* uses a single unusual compound, whereas *F. carica* uses a specific ratio of four common VOCs. The narrow `private channel` label remains directly demonstrated only for *F. semicordata*.

A second focused pass now also separates **chemical-coordinate evidence** from **temporal receiver separation**. In *F. semicordata*, non-pollinating wasps are directly observed to oviposit after the pollinator — *Platyneura cunia* at about 10 days and *Sycoscapter trifemmensis* at 14–32 days after pollinator entry — but neither species has been tested behaviourally against 4-methylanisole itself. This is positive L1 temporal/ecological separation, not closure of the same-code receiver cell.

The 32-species matrix is `empirical/one_trait_shared_cue/FICUS_32_SPECIES_L4_CANDIDATE_MATRIX_V1.csv`. The matched receiver-gap extension is `empirical/one_trait_shared_cue/FICUS_SAME_CODE_RECEIVER_GAP_V1.csv`, with its bounded interpretation in `docs/SCH_FICUS_SAME_CODE_RECEIVER_GAP_READOUT_V1.md`.

## Coverage

```text
Ficus species on scent phylogenetic scaffold:                    32 / 32
sampled individuals represented in Cao et al.:                  242
monoecious species:                                              15
functionally dioecious species:                                  17
narrow single-compound private-channel species:                   1  (F. semicordata)
resolved pollinator attractive chemical codes:                    2  (F. semicordata, F. carica)
direct own-host NPFW scent-behaviour species:                     2  (F. hispida, F. racemosa)
pollinator + NPFW molecular-panel species:                        2  (F. semicordata, F. hispida)
private-code species with direct NPFW temporal separation:        1  (F. semicordata)
direct leaky/shared pollinator-filter comparator:                 1  (F. auriculata)
resolved pollinator code + direct same-code NPFW behaviour:       0
DIRECT_L4 species/transitions:                                    0
```

The three complementary P1 systems are now:

- **Ficus semicordata — resolved single-compound code plus temporal separation.** 4-methylanisole is sufficient for attraction of its pollinator and is the narrowest private-channel result in the fixed matrix. Pollinating and non-pollinating wasp odorant-binding evidence exists in the host system, and direct field observations place at least two NPFW oviposition windows after pollinator entry. What is still missing is direct NPFW attraction, avoidance or indifference to 4-methylanisole itself.
- **Ficus carica — resolved ratio-specific code.** A synthetic four-VOC blend in the correct proportions reproduces attraction of *Blastophaga psenes*, while small changes in the proportions abolish attraction. *Philotrypesis caricae* is directly documented from the host system, but no matched behavioural test has been recovered for that NPFW against the validated four-VOC ratio or its perturbations.
- **Ficus hispida — direct dual-audience system.** Pollinator and non-pollinating *Philotrypesis* respond to receptive fig odour, and molecular receiver data cover both guilds. Recent behavioural/electrophysiological work supports species-specific host recognition through VOC blends, but the key attractive synthetic code has not been resolved to the same standard as *F. semicordata* or *F. carica*.

Two P2 systems sharpen the contrast. *F. auriculata* is a directly tested leaky/shared-filter case: its pollinator prefers its usual host but is also attracted to a sympatric alternative host whose scent shares semiochemicals. *F. racemosa* contributes direct non-pollinating-wasp response to stage-specific fig odour.

## The new bottleneck

The previous bottleneck — “find a second pollinator-specific chemical-code tip” — is closed. The fixed-universe search recovered *F. carica* as a second resolved code. The *F. semicordata* timing result also closes a different ecological cell: a private-code host can show direct temporal separation of pollinator and NPFW use.

What remains is still the **same-code dual-audience intersection**.

```text
resolved single-compound pollinator code -> F. semicordata
  + direct delayed NPFW oviposition      -> F. semicordata
  + direct NPFW response to same code    -> missing

resolved ratio-specific pollinator code  -> F. carica
  + documented NPFW host association     -> F. carica
  + direct NPFW response to same code    -> missing

direct shared pollinator/NPFW behaviour  -> F. hispida
  + exact synthetic pollinator code      -> missing

resolved code + direct NPFW same-code response -> no species yet
historical shared -> private transition        -> no species/branch yet
```

This matters because **temporal separation is not chemical privatization**. A delayed NPFW can still detect the pollinator cue, and an NPFW host association does not show that it intercepts the pollinator's chemical code. Conversely, showing that an exploiter tracks a receptive bouquet does not identify which pollinator-attractive code it intercepts. The strict historical hypothesis needs the receiver measurements on the same chemical coordinate before ancestral-state or transition reconstruction becomes biologically interpretable.

The matrix therefore does **not** infer L4 by multiplying the *F. semicordata* temporal separation, the *F. carica* pollinator code, or the *F. hispida* antagonist result across species.

## Priority tests generated by the matrix

The next pass should remain inside the fixed *Ficus* system and close three explicit cells rather than broaden the literature again.

1. **F. semicordata:** test non-pollinating wasp attraction/avoidance to 4-methylanisole itself, while preserving the natural post-pollination windows now documented for *P. cunia* and *S. trifemmensis*.
2. **F. carica:** test *Philotrypesis caricae* and other relevant exploiters against the validated four-VOC ratio code and perturbed ratios.
3. **F. hispida:** resolve the pollinator-attractive blend to a synthetic code and test *Philotrypesis* against that same code.
4. Use *F. auriculata* as a shared/leaky comparator rather than forcing it into a private-state class.
5. Only after shared/private or code-interception states are available on matched chemical coordinates should they be reconstructed on the 32-species phylogeny and tested against section, reproductive system, phylogenetic and abiotic/geographic alternatives.

If the same-code exploiter intersection remains empty, repeated L4 remains `NOT_EVALUABLE` even though multiple pollinator recognition architectures and one direct temporal-separation case are now empirically resolved.

## Claim ceiling

The current strongest statement is:

> A fixed 32-species fig scent scaffold contains at least two directly resolved pollinator chemical-code architectures — a single-compound code in *F. semicordata* and a ratio-specific four-VOC code in *F. carica* — together with direct dual-audience scent tracking in *F. hispida*, a leaky shared-filter comparator in *F. auriculata*, and direct temporal separation of pollinator and NPFW oviposition in the private-code *F. semicordata* system. The missing historical intersection is narrower but still decisive: no coded species combines a resolved pollinator-attractive chemical code with direct non-pollinating-wasp response to that same code and a reconstructed transition. Repeated shared-to-private evolution under dual-audience selection therefore remains `NOT_EVALUABLE`, not supported or rejected.
