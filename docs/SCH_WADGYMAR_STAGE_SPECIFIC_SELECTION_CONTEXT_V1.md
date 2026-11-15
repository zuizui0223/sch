# Independent original-source audit: temperature reweights fitness stages (2026-11-15)

## Primary evidence recovered

Wadgymar, Cumming & Weis (2015), *Global Change Biology* 21:3786–3799, DOI **10.1111/gcb.12988**, original Tables **3–4**, https://weis.eeb.utoronto.ca/weis/files/2014/01/Wadgymar_et_al-2015-Global_Change_Biology.pdf.

This is an independent biological programme from the Beans & Roach 2015 invasive-competition experiment. 原著の2段階モデルを独立の推定対象として保存する。 The study imposed ambient versus infrared warming on *Chamaecrista fasciculata* and analyzed two distinct fitness stages, survival to reproduction (logit) and seed production conditional on reproduction (negative-binomial log link). Its published Table 3 gives **original directly fitted trait × temperature interactions**, rather than a reconstructed p from independently reported β/SE values.

| Trait × warming | Survival to reproduction | Seed count conditional on reproduction |
|---|---|---|
| Flowering onset | NS (χ² not supplied) | **χ²=6.99, df=1, P<0.01** |
| Fruiting onset | Not fit in survival model | NS (χ² not supplied) |
| Vegetative biomass | **χ²=6.77, df=1, P<0.01** | NS (χ² not supplied) |

**Positive ecological result:** changing thermal context alters how *flowering onset* translates to **seed production**, while changing how *biomass* translates to **survival to reproduction**. In this published experiment, contextual selection response depends on **trait axis × fitness stage**, not just temperature or a single total-fitness slope.

Original Table 4 direct source coefficient examples:

- Flowering onset, conditional seed count: ambient **−0.45 ± 0.23**, heated **−0.19 ± 0.21**. The source-author interaction χ²=6.99 comes from the fitted hurdle count model, not from subtracting these marginal SEs.
- Vegetative biomass, survival: ambient **+0.25 ± 0.33**, heated **+1.72 ± 0.64**. The source-author interaction χ²=6.77 comes from the logit stage model.
- Remaining stage-cell values are preserved in the stage CSV. No unsupported χ² values are fabricated for the original NS cells.

## Model-family reconciliation to the 137-pair compilation

The earlier Caruso 2020 compilation provides **three pairs of standardized, Lande–Arnold relative-total-seed linear gradients** from this paper, with original source rows:

| Trait | Source row IDs | Ambient total-seed β ± SE | Heated total-seed β ± SE |
|---|---|---|---|
| Flowering onset | 351 / 354 | −0.89 ± 0.19 | −0.13 ± 0.21 |
| Fruiting onset | 352 / 355 | −0.45 ± 0.15 | −0.58 ± 0.18 |
| Biomass | 353 / 356 | +1.21 ± 0.18 | +0.81 ± 0.10 |

Those three pairs are correctly matched, but **the author-fit χ² tests in Table 3 are not directly fitted interactions for this exact linear total-seed β family**. Table 4 explicitly calls the latter *comparison/reference* gradients. It is invalid to assign the hurdle seed-count P value to the linear total-seed coefficient difference or to pool the survival-logit and seed-count-log effects as one common β. All three compiled pairs preserve sign; their point magnitude changes alone are not direct author-certified differences on that compiled scale.

The source's actual outcome construction matters: when survival is modeled as whether any seed was produced, fruiting-onset is not a covariate of the survival stage. An unfit interaction is not an estimated zero. A nonsignificant interaction is not equivalence to no contextual selection.

## Evidence ceiling

This **one independent original paper** expands real-world evidence for context-dependent **fitness-stage-specific selection associations**. It does **not** show that a particular animal function conflicts with another, that the original phenotype itself was randomized, that warming causes adaptive evolutionary change, or that two selective demands have different *pure-function* optima. It does not identify SCH conflict loss L. It is a study-specific original-author audit, not a new independent cross-species random-effects meta-analysis and not a population-frequency claim.

Combined with Beans & Roach (2015), two original **different** published programmes support a bounded qualitative insight: contexts can change the strength of selection associations without requiring a strongly supported point sign reversal. One acts across vegetative traits under invasive competition; the other acts across distinct fitness stages under warming. Their treatment types, model links and fitness endpoints differ, so **they must not be pooled into a numeric common ecological effect**.

## Reproduction

    python scripts/audit_sch_wadgymar_stage_context.py --output artifacts/sch_wadgymar_stage_context_v1.json
    python -m pytest -q tests/test_sch_wadgymar_stage_context.py

The script fails closed on changes to original article/model family, source-ID pairing, author χ² thresholds, 137-pair baseline, or the five applicable stage model tests.
