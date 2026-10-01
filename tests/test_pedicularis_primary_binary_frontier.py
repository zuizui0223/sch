from copy import deepcopy
import csv
from pathlib import Path

from scripts.audit_pedicularis_primary_binary_frontier import (
    DEFAULT_FRONTIER,
    EXPECTED_PRIORITY,
    build,
)


def _rows() -> list[dict[str, str]]:
    with DEFAULT_FRONTIER.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write(tmp_path: Path, rows: list[dict[str, str]]) -> Path:
    path = tmp_path / "frontier.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path


def test_current_frontier_stops_general_literature_expansion() -> None:
    result = build()

    assert result["n_primary_assets"] == 5
    assert result["priority_order"] == EXPECTED_PRIORITY
    assert result["n_assets_that_could_change_direct_gap"] == 3
    assert result["direct_gap_candidate_assets"] == [
        "PRIMARY_JING2013_METHODS",
        "PRIMARY_TANG2011_THESIS",
        "PRIMARY_WANG1998_PDF",
    ]
    assert result["n_external_prior_only_assets"] == 2
    assert result["n_retrieved_assets"] == 0
    assert result["general_literature_expansion_permitted"] is False
    assert result["congeneric_prior_expansion_permitted"] is False
    assert result["field_calibration_is_primary_path"] is True
    assert result["status"] == (
        "LITERATURE_EXPANSION_STOPPED_PENDING_PRIMARY_BINARY_OR_FIELD_DATA"
    )


def test_retrieved_jing_methods_unlock_only_targeted_reaudit(tmp_path: Path) -> None:
    rows = _rows()
    target = next(
        row for row in rows
        if row["asset_id"] == "PRIMARY_JING2013_METHODS"
    )
    target["current_access_state"] = (
        "PRIMARY_METHODS_FULL_TEXT_INGESTED"
    )
    result = build(_write(tmp_path, rows))

    assert result["retrieved_direct_gap_candidates"] == [
        "PRIMARY_JING2013_METHODS"
    ]
    assert result["status"] == (
        "PRIMARY_DIRECT_GAP_BINARY_AVAILABLE_REAUDIT_REQUIRED"
    )
    assert result["field_calibration_is_primary_path"] is False
    assert result["general_literature_expansion_permitted"] is False


def test_retrieved_dryad_raw_does_not_unlock_direct_gap(tmp_path: Path) -> None:
    rows = _rows()
    target = next(
        row for row in rows
        if row["asset_id"] == "RAW_XIA2013_DRYAD"
    )
    target["current_access_state"] = "WORKBOOK_INGESTED"
    result = build(_write(tmp_path, rows))

    assert result["retrieved_assets"] == ["RAW_XIA2013_DRYAD"]
    assert result["retrieved_direct_gap_candidates"] == []
    assert result["status"] == (
        "PRIMARY_NON_DIRECT_BINARY_AVAILABLE_PRIOR_REANALYSIS_REQUIRED"
    )
    assert result["field_calibration_is_primary_path"] is True


def test_priority_order_is_frozen() -> None:
    result = build()
    assert result["priority_order"] == [
        "PRIMARY_JING2013_METHODS",
        "PRIMARY_TANG2011_THESIS",
        "PRIMARY_WANG1998_PDF",
        "RAW_XIA2013_DRYAD",
        "SUPP_SUN2016_MCW097",
    ]


def test_stop_rule_preserves_key_claim_boundaries() -> None:
    result = build()
    ceiling = set(result["claim_ceiling"])
    assert "only_primary_method_text_can_resolve_Jing2013_treatment_identity" in ceiling
    assert "observational_raw_data_cannot_create_randomized_G" in ceiling
    assert "aggregate_supplements_cannot_create_missing_interventions" in ceiling
    assert "no_further_congeneric_screening_without_new_direct_gap_rationale" in ceiling
