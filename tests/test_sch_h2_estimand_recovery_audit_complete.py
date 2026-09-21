import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data" / "SCH_H2_ESTIMAND_RECOVERY_FULLTEXT_QUEUE_V1.csv"
AUDITS = [
    ROOT / "data" / "SCH_H2_ESTIMAND_RECOVERY_AUDIT_BATCH1_V1.csv",
    ROOT / "data" / "SCH_H2_ESTIMAND_RECOVERY_AUDIT_BATCH2_V1.csv",
    ROOT / "data" / "SCH_H2_ESTIMAND_RECOVERY_AUDIT_BATCH3_V1.csv",
]
READOUT = ROOT / "data" / "SCH_H2_ESTIMAND_RECOVERY_AUDIT_CUMULATIVE_V2.json"
SCRIPT = ROOT / "scripts" / "build_sch_h2_estimand_recovery_audit_cumulative_v2.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_h2_estimand_audit_complete", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(QUEUE, AUDITS)


def test_v20_fulltext_estimand_recovery_queue_is_fully_audited():
    built = _build()
    assert built["n_frozen_queue_records"] == 29
    assert built["n_audited_records"] == 29
    assert built["n_unaudited_queue_records"] == 0
    assert built["fulltext_queue_audit_complete"] is True
    assert built["audited_tier_counts"] == {
        "FT0_EXPLICIT_SELECTION": 2,
        "FT1_FINAL_PERFORMANCE": 3,
        "FT2_CONTEXT_RICH": 3,
        "FT3_OTHER_RETAINED": 21,
    }


def test_v20_fulltext_frontier_adds_zero_total_selection_clusters():
    built = _build()
    assert built["decision_counts"] == {"NOT_PROMOTED": 29}
    assert built["n_total_selection_effect_promotions"] == 0
    assert built["promotion_rate"] == 0.0
    assert built["promoted_record_ids"] == []
    assert built["status"] == "ESTIMAND_RECOVERY_FULLTEXT_QUEUE_COMPLETE_ZERO_TOTAL_SELECTION_PROMOTIONS"


def test_identification_failures_dominate_completed_frontier():
    built = _build()
    assert built["n_shared_trait_coordinate_failures"] == 8
    assert built["reason_counts"] == {
        "DUPLICATE_OR_SECONDARY_REPORT": 2,
        "NOT_PRIMARY_EMPIRICAL_STUDY": 7,
        "NO_ANIMAL_POLLINATOR_COMPONENT": 1,
        "NO_COMMON_FITNESS_SELECTION_ESTIMAND": 3,
        "NO_COMMON_REPRODUCTIVE_OUTCOME": 3,
        "NO_DIRECT_ANTAGONIST_RESPONSE_ON_SELECTED_TRAIT": 1,
        "NO_FOCAL_POLLINATOR_ANTAGONIST_TRAIT_ESTIMAND": 1,
        "NO_MEASURED_CONSUMER_COMPONENTS": 2,
        "NO_MEASURED_POLLINATOR_COMPONENT": 1,
        "NO_SHARED_TRAIT_COORDINATE": 8,
    }


def test_next_frontier_returns_to_frozen_unscreened_cohort():
    built = _build()
    assert built["next_screening_frontier"] == "463_TITLE_ABSTRACT_UNSCREENED_RECORDS"
    assert "next_expansion_must_return_to_frozen_unscreened_cohort_outcome_blind" in built["claim_ceiling"]


def test_complete_estimand_recovery_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))
