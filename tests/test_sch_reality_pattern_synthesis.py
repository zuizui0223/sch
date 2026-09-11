import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "SCH_PATTERN_LEDGER_V1.csv"
READOUT = ROOT / "data" / "SCH_PATTERN_READOUT_V1.json"
QUANT = ROOT / "data" / "SCH_QUANTITATIVE_READOUT_V1.json"
PROMOTION = ROOT / "docs" / "SCH_META_ANALYSIS_PROMOTION_RULE_V1.md"
STATUS = ROOT / "docs" / "PUBLICATION_STATUS.md"
SCRIPT = ROOT / "scripts" / "build_sch_pattern_readout.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_pattern", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(LEDGER)


def test_pattern_ledger_has_frozen_independent_cluster_structure():
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 16
    assert len({r["cluster_id"] for r in rows}) == 16
    counts = {}
    for row in rows:
        counts[row["pattern_class"]] = counts.get(row["pattern_class"], 0) + 1
    assert counts["OPPOSING_DIRECTION"] == 4
    assert counts["CONTEXT_WEIGHT_SHIFT"] == 7
    assert counts["SHARED_TRACKING_NO_CONFLICT"] == 2
    assert counts["COMBINED_INTERMEDIATE_OR_COMPROMISE"] == 1
    assert counts["SEQUENTIAL_FILTER_COMBINATION"] == 1


def test_machine_readout_matches_committed_core_counts():
    built = _build()
    frozen = json.loads(READOUT.read_text(encoding="utf-8"))
    for key in (
        "n_records",
        "n_independent_clusters",
        "pattern_class_counts",
        "confidence_counts",
        "n_high_confidence_clusters",
        "n_conflict_signature_clusters",
        "n_context_shift_clusters",
        "n_negative_control_clusters",
        "n_shared_tracking_conflict_candidate_clusters",
        "n_quantitative_pool_eligible_clusters",
    ):
        assert built[key] == frozen[key]
    assert frozen["n_quantitative_pool_eligible_clusters"] == 0
    assert "not_natural_prevalence" in frozen["claim_ceiling"]
    assert "direct_L_identification" in frozen["claim_ceiling"]


def test_quantitative_lane_remains_fail_closed():
    q = json.loads(QUANT.read_text(encoding="utf-8"))
    assert q["n_within_study_conflict_component_candidates"] == 4
    assert q["n_within_study_conflict_component_clusters_with_exact_numeric_values"] == 2
    assert q["n_strata_with_at_least_3_compatible_independent_clusters"] == 0
    assert "NO_RANDOM_EFFECTS_POOL_YET" in q["status"]


def test_positive_selected_pool_cannot_be_misread_as_general_meta_analysis():
    text = PROMOTION.read_text(encoding="utf-8")
    assert "conditional on positive admission" in text
    assert "not an unbiased mean across all design-eligible systems" in text
    assert "Design-matched aligned/no-conflict systems must remain visible" in text
    assert "State-specific reproductive optima remain distinct from pure-function optima" in text


def test_publication_order_puts_literature_synthesis_before_focal_experiment():
    text = STATUS.read_text(encoding="utf-8")
    assert "PRIMARY_EMPIRICAL_LAYER = LITERATURE_PATTERN_RECOVERY" in text
    assert "FOCAL_EXPERIMENT_POSITION = FINAL_IDENTIFICATION_UPGRADE" in text
    assert text.index("source-adjudicated literature pattern recovery") < text.index("focal causal experiment last")
