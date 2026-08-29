# SCH Ficus same-code trial data contract v1

## Purpose

This contract is the bridge between the source-anchored Y-tube protocol and the registered same-code classifier. One CSV is one matched analysis package:

```text
one Ficus species
+ one frozen pollinator chemical code
+ one pollinator taxon
+ one focal NPFW taxon
+ pollinator code validation
+ NPFW host/stage positive control
+ NPFW same-code test
```

The analysis entry point is `scripts/analyze_ficus_same_code_trials.py`.

## Required columns

| column | meaning |
|---|---|
| `trial_id` | globally unique introduced-wasp record within the file |
| `species` | focal *Ficus* species; exactly one value per package |
| `receiver_taxon` | pollinator or focal NPFW taxon |
| `receiver_guild` | `POLLINATOR` or `NPFW` |
| `assay_role` | `POLLINATOR_CODE`, `NPFW_POSITIVE_CONTROL`, or `NPFW_SAME_CODE` |
| `code_id` | frozen versioned identity of the focal pollinator code; must be identical across all three roles |
| `cluster_id` | predeclared independent resampling cluster, e.g. source-tree/day block |
| `assay_day` | assay date or registered day identifier |
| `assay_batch` | assay batch identifier |
| `fig_stage` | host developmental stage used for the trial |
| `apparatus_id` | versioned receiver-specific apparatus/protocol identifier |
| `stimulus_id` | exact stimulus preparation/version used in that role |
| `control_id` | exact paired control preparation/version |
| `choice` | `CODE`, `CONTROL`, or `NO_CHOICE` |

`CODE` always means the focal stimulus side for that assay role. Thus in `NPFW_POSITIVE_CONTROL`, `CODE` is the biologically relevant host/stage cue; in `NPFW_SAME_CODE`, `CODE` is the exact frozen pollinator chemical code.

## Fail-closed structural gates

The analyzer rejects the package before inference if any of the following occurs:

- duplicate or blank `trial_id`;
- any required provenance field is blank;
- any role is missing;
- pollinator rows are not labelled `POLLINATOR` or NPFW rows are not labelled `NPFW`;
- more than one plant species occurs in the package;
- pollinator and NPFW assays use different `code_id` values;
- the NPFW positive-control and same-code assays use different NPFW taxa;
- a role has zero decisive choices;
- fewer than the predeclared minimum number of decisive `cluster_id` values are available.

A failed structural gate is `NOT_EVALUABLE`, not evidence of no response.

## Uncertainty contract

The first-pass registered analysis resamples the declared `cluster_id` rather than treating introduced wasps as exchangeable.

```text
pollinator code validation      -> 95% cluster-bootstrap interval
NPFW positive control           -> 95% cluster-bootstrap interval
NPFW same-code direction        -> 95% cluster-bootstrap interval
NPFW same-code equivalence      -> 90% cluster-bootstrap interval
```

The two NPFW intervals are intentionally separate. Directional attraction/avoidance and equivalence to no preference are different inferential questions. The default behavioral-equivalence zone remains `[0.40, 0.60]` around `p=0.50`.

The bootstrap is a prespecified first-pass dependence adjustment. A richer hierarchical model may replace it when the final field design contains nested tree/day/batch structure, but the replacement must preserve the same estimand and feed the same 95% directional / 90% equivalence contract into the classifier.

## No-choice rule

`NO_CHOICE` is never silently discarded from the dataset. Choice probability is estimated among decisive choices, while introduced, decisive and no-choice counts/fractions are all reported in the receipt.

Historical source-style analyses that exclude no-choice individuals may be reproduced only as a sensitivity lane when replicating a published pollinator result. They do not replace the primary registered receipt.

## Planning versus realized inference

The current prospective privacy benchmark is:

```text
206 decisive NPFW same-code choices -> about 80% probability of satisfying the 90% Wilson equivalence rule when true p=0.50
260 decisive choices                -> about 90%
```

These are planning targets, not post hoc eligibility thresholds. A realized interval can satisfy the preregistered equivalence rule with fewer observations, but the receipt will explicitly show whether the 206/260 planning benchmarks were reached.

## Output claim ceiling

The output may classify a contemporary receiver state as:

```text
SAME_CODE_INTERCEPTION
SAME_CODE_AVOIDANCE
BEHAVIORAL_NONRESPONSE_EQUIVALENT
INCONCLUSIVE_SAME_CODE_RESPONSE
```

or fail an upstream assay gate. None of those states alone is `DIRECT_L4`. Historical promotion still requires multiple matched states, ancestral reconstruction, repeated transitions and alternative-history tests.
