# SCH: trait identity and selection-direction persistence in original experimental gradients — V1

*2026-11-15. New numerical reanalysis of published selection gradients; not new field observations.*

## Concrete ecological question

When the environment is experimentally modified, does selection on an individual plant trait **tend to retain its sign**, even when the magnitude of the selection gradient changes?

The previous 26-paper, 137 matched-pair original Caruso–Maherali–Martin (2020) reanalysis (doi: 10.1086/706199; exact original experimental archive doi: **10.5061/dryad.sn02v6x0q**) found **41/137 source point sign crossings**, but **zero** pairs with two nominally nonzero, opposite signed arm gradients. That result alone did not establish whether trait identity contained stable directional information beyond paper-level sign composition.

**New directly computed diagnostic:** conditional on each original study's distinct-trait gradient sign margins, compare observed SAME-trait signs across the two treatment arms against *randomly re-pairing treatment-arm 2's trait labels among the matched trait axes*. This is a conditional **trait-label re-pairing reference**, **not** actual randomized trait or treatment reassignment, and does not measure causal evolutionary persistence or the shared-function conflict loss L.

## Eligibility and independent unit

The frozen **137 actual experimental matched pairs** contain 26 original study papers. Every retained new analysis block is identical in:

- original paper ID and species,
- reported experimental context and fitness component **and identical fitness measure**,
- source ecological agent and **both exact treatment names**.

A block is eligible only if it contains **at least two different traits** with **exactly one pair per trait**. Blocks with repeated same-trait rows (potentially multiple cohorts/site-years) are excluded, not shuffled across their possibly incompatible populations. Singleton blocks cannot inform trait re-pairing. No 2017 Trunschke 12-species study is converted into a 12-article replicated trait block, because each species supplies only one original matched flowering-start trait.

**Selected: 11 treatment/fitness blocks, 43 original matched pairs, from 10 separate original papers but only 8 distinct original species** (including two different controlled/field blocks in the single Beans & Roach paper). Two papers each share *Avena barbata*, and two share *Arabidopsis thaliana*; therefore, ten original publications must NOT be promoted to ten independent taxa. The remaining **94/137 pairs** have no qualifying multiple unique-trait block under these strict rules. They are **not null results or discarded from the primary meta dataset**.

## Genuine additional quantitative result

| Same-sign across experimental treatment arms | Observed | Conditional within-source re-pairing expectation |
|---|---:|---:|
| Original eligible matched trait pairs | **35/43 = 81.40%** | **24.22/43 = 56.33%** |
| Equal-weight across original papers (10 papers) | **81.53%** | **59.99%** |
| Equal-weight across original biological species (8 species) | **84.25%** | **60.39%** |

The exact fixed-marginal distribution of matched positive/negative signs is calculated by a within-block hypergeometric law: if the original treatment 1 has `n1` positive slopes, treatment 2 has `n2` positive slopes, and the block has `n` distinct traits, reassigning treatment-2 trait positions yields the count of same signs as `n - n1 - n2 + 2K`, with `K ~ Hypergeometric(n,n1,n2)`. The exact distribution is convolved across the 11 blocks; the paper-equal distribution is separately convolved with **one weight per original paper**, not 43 independent paper weights.

**Exploratory conditional exact tail probabilities:**

- Matched 43-pair total, 35 observed versus 24.22 conditional expectation: **P = 0.00024113** (upper tail; in this discrete distribution the absolute-deviation two-sided tail is the same).
- Paper-equal matched same-sign fraction: **P = 0.00014468**, with 10 original papers.
- When original paper duplications of *Avena barbata* and *Arabidopsis thaliana* are counted as **one biological species each**, the 8-species-equal estimate is **84.25%** observed versus **60.39%** expected; exact conditional **P = 0.00014468**. Entire original-species leave-one-out sensitivity (dropping all its publications) retains P≤**0.00171**.
- Within the SAME 43 pairs, if treatment-2 signs may be shuffled **only among traits of the same original functional trait class**, the expectation rises to **28.74/43**, but observed **35/43** remains higher: **P = 0.01190476**.
- Leave **one entire paper out** (both contexts of paper 13 excluded together, never singly): the unweighted exact conditional tail remains at or below **P = 0.00171** for every excluded original paper.

Among the selected 43 paired gradients, 8 have point sign crossings; **13 pairs** have both separately reported nominal 95%-supported source gradients and **all 13 retain the same sign**. These are source-marginal β±SE diagnostics, *not* original-author fitted treatment×trait P-values. No new effect-size model combining original paper fitted interactions has been estimated.

The computed result is a **positive ecological pattern in the selected original experiments**: the original biological trait identity predicts which selection direction remains after experimentally changing environmental context more strongly than is captured by the sign composition within matched original experiment blocks. Conditions can reweight selection strength without uniformly scrambling its direction.

## Why this is NOT a new causal generality test

These exact probabilities **only answer the conditional re-pairing question**. Experimental trait identities are never randomly permuted in nature, and the 10 original publications are selected from a previously published nonrandom meta-compilation. P values therefore do **not** mean that an evolutionary trait-specific constraint has been experimentally identified, that treatment regimes could not alter fitness optima, or that 81% of the world's plant traits universally retain their selection direction. The exercise was exploratory, selected using the available data, and subject to unmeasured original trait and gradient sampling covariance.

A same-sign pair includes two nonsignificant coefficients as well as two individually supported coefficients. The 13 supported same-sign cases do not prove their **treatment interactions** differ significantly; nor do point crosses among the 8 cases confirm true reversals. The 43 pairs share study effects and sometimes trait-family covariance; our paper-equal sensitivity and within-class null are controls for some—but not all—sources of this dependence.

The paper's main previous agent hypothesis remains **not supported**: biotic manipulations did not produce more inferred direction reversals than abiotic manipulations (paper-label P=0.3996), and that result is source-design-confounded. **No SCH same-coordinate function-specific causal optima, predator–pollinator compromise, or empirical L** are established by sign identities. Nothing in this new result changes the existing New Phytologist Viewpoint's generality claims or the primary 137-pair denominator.

## Reproduction

Run from repository root:

    python scripts/analyze_sch_2020_trait_direction_persistence.py --output artifacts/sch_2020_trait_sign_persistence_v1.json
    python -m pytest -q tests/test_sch_2020_trait_direction_persistence.py

All numerical probabilities use **Python standard-library exact rational arithmetic** (hypergeometric combination counts + convolution; no SciPy, Monte Carlo, or floating-point P simulation). Study grouping, 137-row source consistency, exact 10-paper sample and leave-one-original-paper-out diagnostics are fail-closed. The GitHub Action stores the signed source-derived JSON receipt.

**Manuscript interpretation:** *Published environmental manipulations often alter the magnitude of plant trait–fitness associations while preserving trait-specific directional information, but observed directional persistence alone does not diagnose antagonistic functional optima or an adaptive compromise.*
