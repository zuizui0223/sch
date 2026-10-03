from __future__ import annotations

import csv
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.adjudicate_pedicularis_primary_methods import (
    DEFAULT_LEDGER,
    build,
)


def _rows() -> list[dict[str, str]]:
    with DEFAULT_LEDGER.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write(tmp_path: Path, rows: list[dict[str, str]]) -> Path:
    path = tmp_path / "adjudication.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path


def _asset(rows: list[dict[str, str]], asset_id: str) -> dict[str, str]:
    return next(row for row in rows if row["asset_id"] == asset_id)


def test_current_primary_method_state_keeps_direct_p1_and_g_open() -> None:
    result = build()

    assert result["n_primary_assets"] == 3
    assert result["direct_focal_p1_effect_recovered"] is False
    assert result["registered_p1_estimand_recovered"] is False
    assert result["registered_p1_protocol_family_compatible"] is False
    assert result["direct_focal_independent_g_recovered"] is False
    assert result["registered_g_effect_estimand_recovered"] is False
    assert result["registered_g_protocol_family_compatible"] is False
    assert result["direct_f0_values_recovered"] == 0
    assert result["field_calibration_still_required"] is True
    assert result["status"] == (
        "PRIMARY_METHOD_ADJUDICATION_READY_DIRECT_P1_G_STILL_UNRECOVERED"
    )


def test_hand_pollination_wording_alone_never_promotes_jing2013(tmp_path: Path) -> None:
    rows = _rows()
    jing = _asset(rows, "PRIMARY_JING2013_METHODS")
    jing["primary_binary_retrieved"] = "YES"
    jing["methods_locator"] = "Methods p.4"
    jing["treatment_identity"] = "HAND_UNSPECIFIED"
    jing["sample_size_reported"] = "YES"

    result = build(_write(tmp_path, rows))
    adjudication = result["asset_results"]["PRIMARY_JING2013_METHODS"]

    assert adjudication["status"] == (
        "PRIMARY_METHODS_RECOVERED_NONREGISTERED_P1_TREATMENT"
    )
    assert adjudication["direct_focal_supplementation_effect_recovered"] is False


def test_open_focal_supplementation_can_recover_effect_without_protocol_equivalence(
    tmp_path: Path,
) -> None:
    rows = _rows()
    jing = _asset(rows, "PRIMARY_JING2013_METHODS")
    jing.update({
        "primary_binary_retrieved": "YES",
        "p_rex_methods_confirmed": "YES",
        "methods_locator": "Methods p.4 Table 2",
        "treatment_identity": "OPEN_SUPPLEMENTAL_OUTCROSS",
        "open_natural_control": "YES",
        "supplemental_cross_pollen": "YES",
        "flowers_open_to_natural_visitors": "YES",
        "standardized_multi_donor_cross_pollen": "NO",
        "sample_size_reported": "YES",
        "reproductive_outcome_reported": "YES",
        "pre_predation_reproductive_endpoint_reported": "YES",
    })

    result = build(_write(tmp_path, rows))
    adjudication = result["asset_results"]["PRIMARY_JING2013_METHODS"]

    assert adjudication["direct_focal_supplementation_effect_recovered"] is True
    assert adjudication["registered_p1_estimand_recovered"] is True
    assert adjudication["registered_protocol_family_compatible"] is False
    assert adjudication["status"] == (
        "DIRECT_FOCAL_P1_EFFECT_RECOVERED_PROTOCOL_NOT_FULLY_EQUIVALENT"
    )
    assert result["direct_f0_values_recovered"] == 0
    assert result["field_calibration_still_required"] is True


def test_full_registered_family_p1_requires_multi_donor_open_supplementation(
    tmp_path: Path,
) -> None:
    rows = _rows()
    wang = _asset(rows, "PRIMARY_WANG1998_PDF")
    wang.update({
        "primary_binary_retrieved": "YES",
        "p_rex_methods_confirmed": "YES",
        "methods_locator": "Methods p.782 Table 1",
        "treatment_identity": "OPEN_SUPPLEMENTAL_OUTCROSS",
        "open_natural_control": "YES",
        "supplemental_cross_pollen": "YES",
        "flowers_open_to_natural_visitors": "YES",
        "standardized_multi_donor_cross_pollen": "YES",
        "sample_size_reported": "YES",
        "reproductive_outcome_reported": "YES",
        "pre_predation_reproductive_endpoint_reported": "YES",
    })

    result = build(_write(tmp_path, rows))
    adjudication = result["asset_results"]["PRIMARY_WANG1998_PDF"]

    assert adjudication["registered_protocol_family_compatible"] is True
    assert adjudication["status"] == (
        "DIRECT_FOCAL_P1_REGISTERED_FAMILY_RECOVERED"
    )
    assert result["registered_p1_protocol_family_compatible"] is True
    assert result["direct_f0_values_recovered"] == 0


def test_bagged_cross_assay_is_not_registered_p1(tmp_path: Path) -> None:
    rows = _rows()
    jing = _asset(rows, "PRIMARY_JING2013_METHODS")
    jing.update({
        "primary_binary_retrieved": "YES",
        "p_rex_methods_confirmed": "YES",
        "methods_locator": "Methods p.4",
        "treatment_identity": "BAGGED_HAND_CROSS",
        "open_natural_control": "YES",
        "supplemental_cross_pollen": "YES",
        "flowers_open_to_natural_visitors": "NO",
        "standardized_multi_donor_cross_pollen": "YES",
        "sample_size_reported": "YES",
        "reproductive_outcome_reported": "YES",
        "pre_predation_reproductive_endpoint_reported": "YES",
    })

    result = build(_write(tmp_path, rows))
    assert result["direct_focal_p1_effect_recovered"] is False
    assert "bagged_breeding_system_assay_is_not_registered_P1" in (
        result["claim_ceiling"]
    )


def test_focal_predator_exclusion_effect_can_be_recovered_without_registered_selectivity(
    tmp_path: Path,
) -> None:
    rows = _rows()
    tang = _asset(rows, "PRIMARY_TANG2011_THESIS")
    tang.update({
        "primary_binary_retrieved": "YES",
        "p_rex_methods_confirmed": "YES",
        "methods_locator": "Chapter 4 Methods pp.88-90 Table 4.2",
        "treatment_identity": "PREDATOR_ACCESS_EXCLUSION",
        "sample_size_reported": "YES",
        "predator_exposed_control": "YES",
        "predator_exclusion_intervention": "YES",
        "water_y_held_fixed": "YES",
        "natural_pollination_preserved": "NO",
        "timing_or_localization_qualified": "YES",
        "pollinator_entry_preserved": "NO",
        "seed_predation_outcome_reported": "YES",
        "final_seed_outcome_reported": "YES",
    })

    result = build(_write(tmp_path, rows))
    adjudication = result["asset_results"]["PRIMARY_TANG2011_THESIS"]

    assert adjudication["direct_focal_independent_g_recovered"] is True
    assert adjudication["registered_g_effect_estimand_recovered"] is True
    assert adjudication["registered_g_protocol_family_compatible"] is False
    assert adjudication["status"] == (
        "DIRECT_FOCAL_INDEPENDENT_G_RECOVERED_SELECTIVITY_NOT_REGISTERED"
    )
    assert result["direct_f0_values_recovered"] == 0


def test_registered_g_family_requires_natural_pollination_and_entry_preservation(
    tmp_path: Path,
) -> None:
    rows = _rows()
    tang = _asset(rows, "PRIMARY_TANG2011_THESIS")
    tang.update({
        "primary_binary_retrieved": "YES",
        "p_rex_methods_confirmed": "YES",
        "methods_locator": "Chapter 4 Methods pp.88-90 Table 4.2",
        "treatment_identity": "PREDATOR_ACCESS_EXCLUSION",
        "sample_size_reported": "YES",
        "predator_exposed_control": "YES",
        "predator_exclusion_intervention": "YES",
        "water_y_held_fixed": "YES",
        "natural_pollination_preserved": "YES",
        "timing_or_localization_qualified": "YES",
        "pollinator_entry_preserved": "YES",
        "seed_predation_outcome_reported": "YES",
        "final_seed_outcome_reported": "YES",
    })

    result = build(_write(tmp_path, rows))
    adjudication = result["asset_results"]["PRIMARY_TANG2011_THESIS"]

    assert adjudication["registered_g_protocol_family_compatible"] is True
    assert adjudication["status"] == (
        "DIRECT_FOCAL_REGISTERED_G_FAMILY_RECOVERED"
    )
    assert result["registered_g_protocol_family_compatible"] is True
    assert result["field_calibration_still_required"] is True


def test_water_defence_manipulation_never_becomes_independent_g(tmp_path: Path) -> None:
    rows = _rows()
    tang = _asset(rows, "PRIMARY_TANG2011_THESIS")
    tang.update({
        "primary_binary_retrieved": "YES",
        "p_rex_methods_confirmed": "YES",
        "methods_locator": "Hypothetical primary Methods",
        "treatment_identity": "WATER_DEFENCE_MANIPULATION",
        "sample_size_reported": "YES",
        "predator_exposed_control": "YES",
        "predator_exclusion_intervention": "NO",
        "water_y_held_fixed": "NO",
        "natural_pollination_preserved": "YES",
        "timing_or_localization_qualified": "YES",
        "pollinator_entry_preserved": "YES",
        "seed_predation_outcome_reported": "YES",
        "final_seed_outcome_reported": "YES",
    })

    result = build(_write(tmp_path, rows))
    assert result["direct_focal_independent_g_recovered"] is False
    assert "water_defence_manipulation_is_not_independent_G" in (
        result["claim_ceiling"]
    )


def test_retrieved_binary_requires_concrete_methods_locator(tmp_path: Path) -> None:
    rows = deepcopy(_rows())
    jing = _asset(rows, "PRIMARY_JING2013_METHODS")
    jing["primary_binary_retrieved"] = "YES"
    jing["p_rex_methods_confirmed"] = "YES"

    with pytest.raises(ValueError, match="lacks a concrete primary Methods/Table locator"):
        build(_write(tmp_path, rows))
