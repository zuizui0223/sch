# Evidence spine

`EVIDENCE_ROLE_REGISTRY_V1.csv` assigns the current paper-facing role and claim ceiling for each named evidence anchor. Paths in `bita_source` are relative to the frozen BITA source repository and commit declared in `data/source_exports/SOURCE_EXPORT_MANIFEST.json`.

The registry does not promote every source to the strict four-field coverage gate. It deliberately separates:

- linked experimental coverage;
- cross-study cue-response synthesis;
- antagonist cue-discrimination evidence;
- consumer-dependency synthesis; and
- ecological context/selection mechanisms.

It also retains a supporting ring of source-adjudicated near passes: an experimental split-outcome system, an observational shared-tracking system, and a comparative shared-tracking system. These sources explain why studies fail the strict gate and help design the next search; they do not increase the strict pass count.

This prevents mechanistically useful studies from being discarded while also preventing them from being counted as same-experiment estimates of `M_A`, `G_A`, or `S_A`.
