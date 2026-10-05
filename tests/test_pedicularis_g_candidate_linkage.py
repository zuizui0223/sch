from __future__ import annotations

from pathlib import Path

import pytest

from scripts.screen_pedicularis_g_candidates import (
    DEFAULT_CANDIDATES,
    _read_candidates,
    build,
)


def _row(
    plant: int,
    *,
    treatment: str,
    method: str,
    suffix: str,
    integrity_failure: bool = False,
) -> dict[str, str]:
    excluded = treatment == "EXCLUDED"
    return {
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "plant_id": f"P{plant:02d}",
        "flower_id": f"P{plant:02d}_{suffix}",
        "predator_treatment": treatment,
        "exclusion_method": method,
        "sham_device_applied": "0" if excluded else "1",
        "anthesis_time_hours": "0",
        "barrier_application_time_hours": "12",
        "pollination_window_complete_before_barrier": "1",
        "ovary_swollen_at_barrier": "0",
        "barrier_covers_pollinator_entry": "0",
        "pre_barrier_attack_present": "0",
        "barrier_integrity_failure_present": (
            "1" if integrity_failure else "0"
        ),
        "realized_exsertion": "0.50",
        "water_depth": "10.0",
        "pollen_grains": "100",
        "pollinator_visits": "10",
        "early_predator_attack_present": "0" if excluded else "1",
        "ovule_count": "100",
        "undamaged_seed_count": "68" if excluded else "50",
        "damaged_seed_count": "2" if excluded else "20",
        "mechanical_damage": "0",
    }


def _rows(*, porous_fails: bool = True) -> list[dict[str, str]]:
    rows = []
    for plant in range(6):
        rows.append(
            _row(
                plant,
                treatment="EXPOSED",
                method="SHAM_SLEEVE",
                suffix="EXPOSED",
            )
        )
        rows.append(
            _row(
                plant,
                treatment="EXCLUDED",
                method="FINE_MESH_LOWER_FRUIT_SLEEVE",
                suffix="MESH",
            )
        )
        rows.append(
            _row(
                plant,
                treatment="EXCLUDED",
                method="POROUS_TUBING_LOWER_FRUIT_SLEEVE",
                suffix="POROUS",
                integrity_failure=porous_fails,
            )
        )
    return rows


def test_canonical_field_codes_link_v4_rows_to_candidate_ids() -> None:
    result = build(_rows(), _read_candidates(DEFAULT_CANDIDATES))

    assert result["status"] == "G_CANDIDATE_LINKED_EXPLORATORY_SCREEN_ONLY"
    assert result["tested_candidate_ids"] == [
        "G_A1_FINE_MESH",
        "G_A2_POROUS_TUBING",
    ]
    assert result["hard_validity_pass_candidate_ids"] == [
        "G_A1_FINE_MESH"
    ]
    assert result["retired_candidate_ids"] == ["G_A2_POROUS_TUBING"]
    assert result["candidate_selected"] is False


def test_unknown_field_method_code_fails_closed() -> None:
    rows = _rows()
    for row in rows:
        if row["predator_treatment"] == "EXCLUDED":
            row["exclusion_method"] = "AD_HOC_BARRIER"
            break

    with pytest.raises(ValueError, match="unregistered G field method codes"):
        build(rows, _read_candidates(DEFAULT_CANDIDATES))


def test_multiple_hard_pass_candidates_are_not_ranked_posthoc() -> None:
    result = build(
        _rows(porous_fails=False),
        _read_candidates(DEFAULT_CANDIDATES),
    )

    assert result["hard_validity_pass_candidate_ids"] == [
        "G_A1_FINE_MESH",
        "G_A2_POROUS_TUBING",
    ]
    assert result["current_frontier"] == (
        "MULTIPLE_TESTED_CANDIDATES_PASS_HARD_VALIDITY_"
        "NO_AUTOMATIC_SELECTION"
    )
    assert result["candidate_selected"] is False
    assert "multiple_pass_candidates_are_not_ranked_by_posthoc_effect_size" in (
        result["claim_ceiling"]
    )


def test_candidate_screen_preserves_priority_and_precedent_provenance() -> None:
    result = build(_rows(), _read_candidates(DEFAULT_CANDIDATES))
    mesh = result["candidate_screens"]["G_A1_FINE_MESH"]

    assert mesh["field_exclusion_method"] == (
        "FINE_MESH_LOWER_FRUIT_SLEEVE"
    )
    assert mesh["exploratory_priority"] == 1
    assert "Pedicularis" in mesh["precedent_basis"]
    assert mesh["n_paired_plants"] == 6


def test_candidate_matrix_has_unique_nonempty_field_codes() -> None:
    rows = _read_candidates(DEFAULT_CANDIDATES)
    codes = [row["field_exclusion_method"] for row in rows]

    assert len(codes) == 5
    assert all(codes)
    assert len(codes) == len(set(codes))
