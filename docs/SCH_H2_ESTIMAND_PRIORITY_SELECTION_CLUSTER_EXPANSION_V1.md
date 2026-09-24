# SCH H2 estimand-priority selection-cluster expansion V1

## Prospective screening step

PR #77 froze the review order for the 463 records that were title/abstract-unscreened at that time. The first six priority records were then adjudicated without changing the scientific admission rules.

All six were retained to full text in V21. Two records already expose exact, source-resolved standardized selection gradients and are formally included at full text in V22:

- SCHPRISMA-000659 — *Lobelia cardinalis* (Bartkowska & Johnston 2012)
- SCHPRISMA-000775 — *Brassica rapa* (Knauer & Schiestl 2017)

The other four remain full-text pending; they are not promoted by title alone.

## Exact numeric recovery

### Brassica rapa

Table 2 supplies nine floral traits across three consumer regimes:

- bumble bees;
- bumble bees + cabbage butterflies;
- cabbage butterflies.

Fitness is relative seed set. All 27 directional-selection beta +/- SE cells are frozen in:

`data/SCH_H2_BRASSICA_KNAUER_2017_SELECTION_GRADIENTS_V1.csv`

This is a repeated-context TOTAL_SELECTION_EFFECT family with numeric pooling family STANDARDIZED_SELECTION_GRADIENT.

### Lobelia cardinalis

Table 2 supplies six traits under:

- natural pollination;
- supplemental hand pollination.

Fitness is relative seed number. All 12 directional-selection beta +/- SE cells are frozen in:

`data/SCH_H2_LOBELIA_BARTKOWSKA_2012_SELECTION_GRADIENTS_V1.csv`

Herbivore-mediated paths are source-resolved in the same study, but herbivory was not experimentally toggled. The study is therefore retained as DIRECTIONAL_OR_NEAR_PASS rather than promoted to a strict causal crossed experiment.

## H2 consequence

A source-level recovery of the previously included Dalechampia study additionally freezes Table 4 mean-standardized net selection gradients. The upper-bract axis is explicitly decomposed into pollinator-positive and seed-predator-negative components on the same predicted seed-survival fitness surface. This adds a third independent biological cluster without changing PRISMA inclusion counts.\n\nThe V7 builder now adds:

~~~text
new exact cases                         39
new canonical trait axes               15
new independent biological clusters     2
~~~

For TOTAL_SELECTION_EFFECT:

~~~text
before: 30 cases / 8 axes / 3 clusters
after:  73 cases / 27 axes / 6 clusters
~~~

For the stricter numeric pooling family STANDARDIZED_SELECTION_GRADIENT:

~~~text
before: 12 cases / 4 axes / 2 clusters
after:  51 cases / 19 axes / 4 clusters
~~~

The registered independent-cluster minimum remains 8.

Therefore:

~~~text
H2_COMMENSURATE_ESTIMAND_GATE = FAIL
remaining TOTAL_SELECTION_EFFECT cluster deficit = 2
~~~

This is progress without retuning the gate.

## Biological interpretation

The important gain is independence, not raw row count.

Brassica shows that the same floral-signal coordinate can experience different net selection when consumer composition changes, including a pollinating herbivore whose functional sign depends on the surrounding pollinator regime.

Lobelia shows that pollinator-mediated selection on the same floral traits can be separated from weaker herbivore-mediated paths on seed fitness, while preserving the distinction between experimental pollination contrasts and observational herbivore mediation.

Together they strengthen the comparative claim that realized multifunctional selection is context-assembled rather than a fixed species-level property.

## Next target

Do not maximize cases per paper. Recover at least two additional independent biological clusters with commensurate standardized selection gradients.

Priority remains source-resolved, same-trait, repeated-context studies from the frozen V21 order.
