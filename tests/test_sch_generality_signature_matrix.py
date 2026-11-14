import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "SCH_GENERALITY_SIGNATURE_MATRIX_V1.csv"


def _rows():
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        return {row["system"]: row for row in csv.DictReader(handle)}


def test_primary_causal_route_is_not_marked_executed():
    rows = _rows()
    assert rows["Pedicularis_rex"]["causal_status"] == "FULL_CAUSAL_SURFACE_NOT_YET_EXECUTED"


def test_negative_and_aligned_controls_remain_controls():
    rows = _rows()
    assert rows["Ipomopsis_aggregata"]["program_role"] == "NEGATIVE_CONTROL"
    assert rows["Platycodon_grandiflorus"]["program_role"] == "ALIGNED_OPTIMUM_CONTROL"


def test_dalechampia_is_not_promoted_to_complete_causal_replication():
    rows = _rows()
    assert "INCOMPLETE" in rows["Dalechampia"]["causal_status"]


def test_darwin_finches_are_cross_domain_observational_not_causal_replication():
    rows = _rows()
    item = rows["Darwin_finches_beak_jaw"]
    assert item["program_role"] == "G2_CROSS_DOMAIN_OBSERVATIONAL_CONSTRAINT_CANDIDATE"
    assert item["causal_status"] == "NO_REGISTERED_SCH_OPTIMUM_SHIFT_CAUSAL_SURFACE"


def test_hisa_trpf_is_experimental_conflict_anchor_not_registered_sch_surface():
    rows = _rows()
    item = rows["Salmonella_HisA_TrpF"]
    assert item["program_role"] == "G2_CROSS_DOMAIN_ADAPTIVE_CONFLICT_EXPERIMENTAL_ANCHOR"
    assert item["causal_status"] == "NO_REGISTERED_ONE_AXIS_WEIGHT_MANIPULATION_SURFACE"
