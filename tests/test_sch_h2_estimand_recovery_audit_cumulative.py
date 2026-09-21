import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data" / "SCH_H2_ESTIMAND_RECOVERY_FULLTEXT_QUEUE_V1.csv"
AUDITS = [
    ROOT / "data" / "SCH_H2_ESTIMAND_RECOVERY_AUDIT_BATCH1_V1.csv",
    ROOT / "data" / "SCH_H2_ESTIMAND_RECOVERY_AUDIT_BATCH2_V1.csv",
]
READOUT = ROOT / "data" / "SCH_H2_ESTIMAND_RECOVERY_AUDIT_CUMULATIVE_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_h2_estimand_recovery_audit_cumulative.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_h2_estimand_audit_cumulative", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(QUEUE, AUDITS)


def test_cumulative_estimand_recovery_audits_13_queue_records():
    built = _build()
    assert built["n_audit_batches"] == 2
    assert built["n_audited_records"] == 13
    assert built["n_unaudited_queue_records"] == 16
    assert built["audited_tier_counts"] == {
        "FT0_EXPLICIT_SELECTION": 2,
        "FT1_FINAL_PERFORMANCE": 3,
        "FT2_CONTEXT_RICH": 3,
        "FT3_OTHER_RETAINED": 5,
    }


def test_cumulative_estimand_recovery_has_zero_total_selection_promotions():
    built = _build()
    assert built["decision_counts"] == {"NOT_PROMOTED": 13}
    assert built["n_total_selection_effect_promotions"] == 0
    assert built["promotion_rate"] == 0.0
    assert built["n_shared_trait_coordinate_failures"] == 6


def test_cumulative_negative_yield_is_identification_not_null_effect():
    built = _build()
    assert built["reason_counts"]["NO_SHARED_TRAIT_COORDINATE"] == 6
    assert "shared_trait_coordinate_failure_is_distinct_from_null_ecological_effect" in built["claim_ceiling"]
    assert "estimand_family_bottleneck_is_identification_not_raw_case_count" in built["claim_ceiling"]


def test_cumulative_estimand_recovery_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))
