# SCH Pedicularis independent-predator exclusion method audit v1

## Question

Can `Pedicularis rex` support a Chapter-1 antagonist intervention that changes pre-dispersal seed-predator pressure while leaving pollination and the proposed Chapter-2 water-defence axis unchanged?

The answer is not yet `yes`, but the natural history narrows the pilot substantially.

## Primary-source constraints

Sun, Armbruster & Huang (2016; DOI `10.1093/aob/mcw097`) report that the pre-dispersal seed predators are larvae of Diptera and Lepidoptera whose adults lay eggs on ovaries after flowers open but before ovaries swell. Oviposition is achieved from outside the flower by piercing the sepals or corolla tube. The insects were identified only to order because larvae were difficult to rear.

This yields three design constraints:

```text
C1  the antagonist-access window overlaps the post-opening floral period;
C2  the attack route is from outside the lower flower / ovary region;
C3  whole-flower bagging would also perturb bumblebee access and therefore is not a selective G intervention.
```

`P. rex` is almost entirely dependent on bumblebees for reproduction, so preserving the pollination lane is not optional.

## Pedicularis timing precedent

A direct P. rex seed-predator exclusion protocol was not recovered.

However, Menges, Waller & Gawler (1986; doi `10.2307/2443796`) provide a
within-genus timing precedent in `Pedicularis furbishiae`. Aluminum-mesh cages
were placed over groups of 3-6 immature scapes for an unrelated spittlebug
experiment and removed **before flowers opened** so pollination could proceed.
Those previously caged scapes later experienced the same lepidopteran seed
predation as other plants. The authors therefore inferred that the plume-moth
seed predator `Amblyptilia pica` attacked after pollination.

Across that study, `Amblyptilia` infested 39% of maturable capsules and seed
predation reduced mean seed yield from 25.4 to 2.8 seeds per capsule
(`N=224`, `P<0.001`).

This does **not** demonstrate that a post-pollination mesh sleeve excludes a
Pedicularis seed predator: the cages had already been removed. It does,
however, strengthen the temporal premise of G-A by showing within the genus
that a lepidopteran seed predator can arrive after the pollination phase.

## External barrier precedents: three separate evidence axes

The external evidence is now split deliberately into **timing**, **fruit-development compatibility**, and **barrier efficacy**. These are not interchangeable claims.

### 1. Within-genus timing — `Pedicularis furbishiae`

The Menges et al. precedent above supports only the event ordering:

```text
pollination can finish
-> a Pedicularis seed predator can attack later.
```

It does not test a barrier left in place during the predator-access period.

### 2. Fruit-local barrier compatibility — `Cypripedium candidum`

Walsh et al. (2014; doi `10.1093/aobpla/plu031`) used a fruit-local porous barrier after pollination.

In the 2011 experiment:

```text
N = 30 plants
initial fruit set scored 2 weeks after floral dehiscence
all fruits then enclosed in dialysis tubing
final fruit maturation and seed mass measured afterward.
```

Final maturation remained measurable:

```text
self     0.466 ± 0.08 SE
outcross 0.400 ± 0.08 SE
open     0.100 ± 0.08 SE.
```

Seed mass was measured in 29 fruits; outcross/open fruits averaged about 0.027 g and selfed fruits about 0.017 g.

This is strong evidence that a **post-pollination fruit-local porous barrier can coexist with continued fruit development and seed measurement**.

It is **not** a same-year efficacy contrast: all 2011 fruits were shielded, so there is no contemporaneous unshielded predator-control from which to estimate the causal reduction in predation. An earlier 2009 cohort had 73% fruit predation and an 89% seed-mass reduction, but year/site differ.

### 3. Fruit-local barrier efficacy — `Chamaecrista desvauxii`

Baker-Méio & Marquis (2012; doi `10.1111/j.1365-2745.2011.01892.x`) provide a closer efficacy-class precedent.

As developing fruits matured, treated individuals had each fruit enclosed in a mesh bag. Control fruits received brief sham bagging initially and were enclosed only near ripeness for collection.

The experiment showed that fruit-local exclusion could reduce attack without a detectable seed-mass penalty:

```text
var. 1 sucking attack      LRT = 9.62, P = 0.002
var. 1 chewing attack      LRT = 7.07, P = 0.008
var. modesta fruit set     LRT = 19.7, P < 0.001
seed mass                  no treatment difference, all P > 0.12.
```

The authors also report that early reproductive investment / pollination rates were not changed by the exclusion treatments.

But the efficacy was imperfect and context-dependent. Two failure modes are directly relevant to P. rex:

```text
1. some fruits were attacked before they were large enough to bag;
2. some sucking insects attacked through mesh holes.
```

Therefore this is a strong **barrier-class efficacy/selectivity precedent**, not a portable effect size or a validated P. rex device.

Machine audit:

```text
empirical/architecture/PEDICULARIS_G_BARRIER_PRECEDENTS_V1.csv
scripts/audit_pedicularis_g_barrier_precedents.py
```

The current three-axis evidence state is:

```text
Pedicularis post-pollination attack timing       RECOVERED
fruit-development compatibility of porous barrier RECOVERED OUTSIDE PEDICULARIS
fruit-local barrier efficacy/selectivity class    RECOVERED OUTSIDE PEDICULARIS
focal P. rex barrier effectiveness                NOT RECOVERED
focal P. rex barrier selectivity                   NOT RECOVERED
focal P. rex timing bounds                         NOT RECOVERED.
```

## Candidate methods ranked

### G-A — post-pollination lower-flower / fruit shielding

Preferred first pilot.

```text
1  allow a defined natural-pollination window;
2  verify pollen receipt before shielding on a paired / sacrificial sample;
3  before ovary swelling, apply a small barrier around the lower corolla / ovary region;
4  leave the stigma / upper corolla geometry and water-filled bract function unchanged;
5  compare later early-attack evidence, seed predation and final intact seed set.
```

Potential materials to pilot:

```text
fine inert mesh sleeve with pore size explicitly matched to focal predator access
soft dialysis / porous tubing
custom lower-flower sleeve fixed below the pollinator-contact zone.
```

The external precedents add three mandatory design checks:

```text
PRE-ATTACK CHECK
  score whether eggs / punctures are already present before barrier placement;

PORE-SIZE CHECK
  reject a mesh that still permits ovipositor / sucking access through openings;

DEVELOPMENT-COMPATIBILITY CHECK
  compare sham versus barrier for swelling, fruit retention, seed mass and
  mechanical damage rather than assuming porous material is inert.
```

This is the strongest route because it exploits sequence rather than trying to make one barrier simultaneously transparent to pollinators and opaque to predators.

### G-B — lower-corolla local ovipositor barrier during anthesis

Second choice if the pollination and oviposition windows cannot be temporally separated enough.

The barrier covers only the lower sepals / corolla-tube attack region and leaves the stigma, galea and visitor entrance exposed.

This is biologically plausible from the known attack route but has **no direct Pedicularis validation**. It requires a sham-device treatment and particularly strict checks of:

```text
pollinator visits
pollen receipt
realized exsertion
corolla opening
flower orientation
water depth / retention
mechanical damage.
```

### G-C — whole-flower or whole-inflorescence mesh

Not preferred for SCH.

It can exclude insects, but during the open-flower phase it also excludes or alters bumblebees and therefore cannot identify the antagonist lane independently.

Use only after pollination is demonstrably complete for the focal flowers.

### G-D — chemical exclusion

Not preferred.

Localized insecticide / repellent would require independent evidence that it leaves pollinator behaviour, floral physiology, water chemistry and seed development unaffected. This adds more assumptions than a physical barrier.

## Stage-G pilot design

Within the same focal population and season, randomize flowers within plants to:

```text
EXPOSED + sham handling
EXCLUDED + candidate physical barrier
```

The existing registered evaluator remains:

```text
scripts/evaluate_pedicularis_predator_weight.py
```

The pilot must recover:

```text
early predator attack: lower under EXCLUDED
seed-predation fraction: lower under EXCLUDED
final intact seed set: higher under EXCLUDED
```

while simultaneously satisfying prospective equivalence / tolerance gates for:

```text
initial seed set
pollen receipt
pollinator visitation
realized exsertion
water depth / state
mechanical damage.
```

## Additional timing records required

For each focal flower record:

```text
anthesis date/time
first natural pollinator visit if observed
barrier application date/time
stigma pollen check timing on paired flowers
ovary-swelling onset date/time
barrier removal date/time if removed
exclusion_method identifier.
```

These timing data are necessary because a method that works only after pollination is already saturated may still be valid, whereas a method applied too early would contaminate the P lane.

## Go / no-go

### GO

Proceed to the SCH V2 full surface only if one barrier method passes the registered predator-weight selectivity receipt in the same population and season as the z and P pilots.

### NO-GO

Pedicularis should be demoted as the first causal SCH system if no practical exclusion method can substantially reduce attack / predation without materially changing pollen receipt, visitor access or water defence.

Do not rescue the system by reusing water drainage as `G`; that would restore the SCH->BITA circularity already identified.

## Current status

```text
predator natural-history route:          RECOVERED
Pedicularis post-pollination attack timing: RECOVERED
whole-flower exclusion as selective G:   REJECTED
post-pollination attack timing:          RECOVERED WITHIN PEDICULARIS
fruit-local barrier compatibility:       RECOVERED OUTSIDE PEDICULARIS
fruit-local barrier efficacy class:      RECOVERED OUTSIDE PEDICULARIS
P. rex barrier effectiveness/selectivity: NOT YET EXECUTED
P. rex numeric timing bounds:             NOT YET EXECUTED
lower-corolla local barrier:              BIOLOGICALLY PLAUSIBLE, UNVALIDATED
P. rex selective independent G:           NOT YET EXECUTED
```

## Bottom line

The independent-G problem is narrower than before but not solved. The within-genus timing evidence makes a **small post-pollination shielding pilot** more defensible than before, but shielding effectiveness and selectivity still require focal P. rex validation before the full `z x P x G` factorial.