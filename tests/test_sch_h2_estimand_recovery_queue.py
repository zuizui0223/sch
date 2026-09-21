import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "empirical" / "prisma" / "frozen_v2" / "SCH_PRISMA_V2_IDENTIFIED_CANDIDATES_FROZEN_2026-08-29.csv"
V20 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V20_BATCH4_REMAINDER_TITLE_ABSTRACT.csv"
QUEUE = ROOT / "data" / "SCH_H2_ESTIMAND_RECOVERY_FULLTEXT_QUEUE_V1.csv"
READOUT = ROOT / "data" / "SCH_H2_ESTIMAND_RECOVERY_FULLTEXT_READOUT_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_h2_estimand_recovery_fulltext_queue.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_h2_estimand_recovery_queue", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(FROZEN, V20)


def test_estimand_recovery_queue_covers_all_v20_fulltext_pending():
    rows, receipt = _build()
    assert len(rows) == 29
    assert receipt["n_fulltext_pending"] == 29
    assert receipt["tier_counts"] == {
        "FT0_EXPLICIT_SELECTION": 2,
        "FT1_FINAL_PERFORMANCE": 3,
        "FT2_CONTEXT_RICH": 3,
        "FT3_OTHER_RETAINED": 21,
    }


def test_estimand_priority_is_outcome_blind_and_frozen():
    rows, receipt = _build()
    assert receipt["n_selection_or_performance_priority"] == 5
    assert receipt["n_context_rich_priority"] == 3
    assert receipt["priority_record_ids"] == [
        "SCHPRISMA-000317",
        "SCHPRISMA-000400",
        "SCHPRISMA-000309",
        "SCHPRISMA-000310",
        "SCHPRISMA-000386",
        "SCHPRISMA-000370",
        "SCHPRISMA-000372",
        "SCHPRISMA-000378",
    ]
    assert all(row["outcome_blind_priority"] == "YES" for row in rows)
    assert "no_ecological_outcome_sign_used_for_priority" in receipt["claim_ceiling"]


def test_queue_order_starts_with_explicit_selection_then_final_performance():
    rows, _ = _build()
    assert [row["record_id"] for row in rows[:5]] == [
        "SCHPRISMA-000317",
        "SCHPRISMA-000400",
        "SCHPRISMA-000309",
        "SCHPRISMA-000310",
        "SCHPRISMA-000386",
    ]
    assert [row["recovery_tier"] for row in rows[:5]] == [
        "FT0_EXPLICIT_SELECTION",
        "FT0_EXPLICIT_SELECTION",
        "FT1_FINAL_PERFORMANCE",
        "FT1_FINAL_PERFORMANCE",
        "FT1_FINAL_PERFORMANCE",
    ]


def test_frozen_queue_readout_is_reproducible():
    _, receipt = _build()
    assert receipt == json.loads(READOUT.read_text(encoding="utf-8"))
