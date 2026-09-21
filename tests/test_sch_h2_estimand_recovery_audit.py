import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data" / "SCH_H2_ESTIMAND_RECOVERY_FULLTEXT_QUEUE_V1.csv"
AUDIT = ROOT / "data" / "SCH_H2_ESTIMAND_RECOVERY_AUDIT_BATCH1_V1.csv"
READOUT = ROOT / "data" / "SCH_H2_ESTIMAND_RECOVERY_AUDIT_BATCH1_READOUT_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_h2_estimand_recovery_audit.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_h2_estimand_audit", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(QUEUE, AUDIT)


def test_first_priority_batch_is_audited_without_priority_retuning():
    built = _build()
    assert built["n_frozen_queue_records"] == 29
    assert built["n_audited_records"] == 8
    assert built["n_unaudited_queue_records"] == 21
    assert built["audited_tier_counts"] == {
        "FT0_EXPLICIT_SELECTION": 2,
        "FT1_FINAL_PERFORMANCE": 3,
        "FT2_CONTEXT_RICH": 3,
    }


def test_first_priority_batch_adds_no_total_selection_family():
    built = _build()
    assert built["decision_counts"] == {"NOT_PROMOTED": 8}
    assert built["n_total_selection_effect_promotions"] == 0
    assert built["promoted_record_ids"] == []
    assert built["status"] == "ESTIMAND_RECOVERY_BATCH1_AUDITED_NO_TOTAL_SELECTION_PROMOTIONS"


def test_negative_yield_has_explicit_identification_reasons():
    built = _build()
    assert built["reason_counts"] == {
        "NOT_PRIMARY_EMPIRICAL_STUDY": 1,
        "NO_COMMON_FITNESS_SELECTION_ESTIMAND": 1,
        "NO_COMMON_REPRODUCTIVE_OUTCOME": 1,
        "NO_DIRECT_ANTAGONIST_RESPONSE_ON_SELECTED_TRAIT": 1,
        "NO_FOCAL_POLLINATOR_ANTAGONIST_TRAIT_ESTIMAND": 1,
        "NO_MEASURED_CONSUMER_COMPONENTS": 1,
        "NO_SHARED_TRAIT_COORDINATE": 2,
    }
    assert "do_not_retune_batch1_priority_rules_after_observing_zero_promotions" in built["claim_ceiling"]


def test_estimand_recovery_audit_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))
