from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.summarize_pedicularis_g_event_time_pilot import (
    FREEZE_STATUS,
    SCHEMA,
    build,
)


def _config() -> dict:
    return {
        "schema": SCHEMA,
        "status": FREEZE_STATUS,
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "pollination_completion_definition": (
            "predefined focal stigma pollen-receipt criterion"
        ),
        "pollination_completion_measurement": (
            "single destructive stigma pollen count on matched sentinel flower"
        ),
        "attack_event_definition": "visible egg or oviposition puncture",
        "ovary_swelling_definition": "prospectively defined visible swelling",
        "sampling_schedule_basis_note": "fixed before event-time observations",
        "frozen_before_event_time_data": True,
        "frozen_at_utc": "2026-10-05T00:00:00Z",
    }


def _pollen(
    flower_id: str,
    plant_id: str,
    hours: float,
    pollen: int,
    complete: int,
) -> dict[str, str]:
    return {
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "plant_id": plant_id,
        "flower_id": flower_id,
        "flower_role": "POLLINATION_SENTINEL",
        "anthesis_time_hours": "0",
        "observation_time_hours": str(hours),
        "pollen_grains": str(pollen),
        "pollination_complete": str(complete),
        "attack_present": "",
        "ovary_swollen": "",
    }


def _natural(
    flower_id: str,
    plant_id: str,
    hours: float,
    attack: int,
    swollen: int,
) -> dict[str, str]:
    return {
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "plant_id": plant_id,
        "flower_id": flower_id,
        "flower_role": "ATTACK_SWELL_SENTINEL",
        "anthesis_time_hours": "0",
        "observation_time_hours": str(hours),
        "pollen_grains": "",
        "pollination_complete": "",
        "attack_present": str(attack),
        "ovary_swollen": str(swollen),
    }


def _rows() -> list[dict[str, str]]:
    rows = [
        _pollen("P01_P4", "P01", 4, 12, 0),
        _pollen("P02_P4", "P02", 4, 15, 0),
        _pollen("P01_P8", "P01", 8, 38, 1),
        _pollen("P02_P8", "P02", 8, 31, 0),
        _pollen("P01_P12", "P01", 12, 51, 1),
        _pollen("P02_P12", "P02", 12, 55, 1),
    ]
    for flower, plant, states in (
        (
            "P01_N",
            "P01",
            [(4, 0, 0), (8, 0, 0), (12, 1, 0)],
        ),
        (
            "P02_N",
            "P02",
            [(4, 0, 0), (8, 0, 0), (12, 0, 1)],
        ),
    ):
        for hours, attack, swollen in states:
            rows.append(_natural(flower, plant, hours, attack, swollen))
    return rows


def test_event_time_pilot_describes_biology_without_selecting_window() -> None:
    result = build(_config(), _rows())

    assert result["status"] == "G_EVENT_TIME_DESCRIPTORS_READY_NO_WINDOW_SELECTED"
    assert result["n_pollination_sentinel_flowers"] == 6
    assert result["n_attack_swelling_sentinel_flowers"] == 2
    assert result["timing_window_selected"] is False
    assert result["temporal_separability_inferred"] is False

    profile = {
        row["elapsed_hours"]: row
        for row in result["joint_time_profiles"]
    }
    assert profile[4.0]["pollination_complete_rate"] == pytest.approx(0.0)
    assert profile[8.0]["pollination_complete_rate"] == pytest.approx(0.5)
    assert profile[12.0]["pollination_complete_rate"] == pytest.approx(1.0)
    assert profile[12.0]["attack_free_rate"] == pytest.approx(0.5)
    assert profile[12.0]["ovary_not_swollen_rate"] == pytest.approx(0.5)
    assert profile[12.0]["constraint_present_rate"] == pytest.approx(1.0)

    poll = result["median_pollination_completion_interval_hours"]
    constraint = result["median_constraint_onset_interval_hours"]
    gap = result["median_temporal_separability_descriptor"]
    assert poll["lower_bound_hours"] == pytest.approx(4.0)
    assert poll["upper_bound_hours"] == pytest.approx(8.0)
    assert constraint["lower_bound_hours"] == pytest.approx(8.0)
    assert constraint["upper_bound_hours"] == pytest.approx(12.0)
    assert gap["delta_t50_lower_bound_hours"] == pytest.approx(0.0)
    assert gap["delta_t50_upper_bound_hours"] == pytest.approx(8.0)
    assert gap["ordering_state"] == (
        "MEDIAN_TEMPORAL_SEPARATION_SUPPORTED_ON_SAMPLED_GRID"
    )
    assert gap["method_development_route_implication"] == (
        "POSTPOLLINATION_BARRIER_ROUTE_BIOLOGICALLY_PLAUSIBLE_"
        "AT_MEDIAN_SCALE"
    )
    assert gap["candidate_selected"] is False
    assert gap["exact_individual_delta_t_estimated"] is False


def test_event_onsets_are_interval_censored_not_exact_event_times() -> None:
    result = build(_config(), _rows())
    by_flower = {
        row["flower_id"]: row
        for row in result["event_intervals_by_flower"]
    }

    p01 = by_flower["P01_N"]
    assert p01["attack_interval"]["last_negative_hours"] == pytest.approx(8.0)
    assert p01["attack_interval"]["first_positive_hours"] == pytest.approx(12.0)
    assert p01["swelling_interval"]["right_censored"] is True
    assert p01["first_constraint_positive_hours"] == pytest.approx(12.0)

    assert "attack_and_swelling_onsets_are_interval_censored" in (
        result["claim_ceiling"]
    )


def test_barrier_application_time_is_not_an_input_or_window_estimator() -> None:
    result = build(_config(), _rows())
    assert "barrier_application_time_hours" not in str(result)
    assert "does_not_use_barrier_application_time_as_natural_window" in (
        result["claim_ceiling"]
    )


def test_pollination_sentinel_is_single_destructive_observation() -> None:
    rows = _rows()
    rows.append(dict(rows[0]))
    with pytest.raises(ValueError, match="must be sampled once"):
        build(_config(), rows)


def test_attack_and_swelling_events_must_be_absorbing() -> None:
    rows = _rows()
    target = [
        row
        for row in rows
        if row["flower_id"] == "P01_N"
    ]
    target[1]["attack_present"] = "1"
    target[2]["attack_present"] = "0"
    with pytest.raises(ValueError, match="must be absorbing"):
        build(_config(), rows)


def test_roles_cannot_mix_measurement_fields() -> None:
    rows = _rows()
    pollen = next(
        row for row in rows
        if row["flower_role"] == "POLLINATION_SENTINEL"
    )
    pollen["attack_present"] = "0"
    with pytest.raises(ValueError, match="leave attack/swelling blank"):
        build(_config(), rows)

    rows = _rows()
    natural = next(
        row for row in rows
        if row["flower_role"] == "ATTACK_SWELL_SENTINEL"
    )
    natural["pollen_grains"] = "10"
    with pytest.raises(ValueError, match="leave pollen fields blank"):
        build(_config(), rows)


def test_config_definitions_must_be_frozen_before_data() -> None:
    config = _config()
    config["status"] = "REQUIRED_BEFORE_USE"
    with pytest.raises(ValueError, match="not prospectively frozen"):
        build(config, _rows())

    config = _config()
    config["pollination_completion_definition"] = "REQUIRED_BEFORE_USE"
    with pytest.raises(ValueError, match="pollination_completion_definition"):
        build(config, _rows())

    config = _config()
    config["frozen_before_event_time_data"] = False
    with pytest.raises(ValueError, match="before data"):
        build(config, _rows())


def test_context_and_minimum_time_coverage_fail_closed() -> None:
    rows = _rows()
    rows[0]["season_id"] = "S2"
    with pytest.raises(ValueError, match="population/season"):
        build(_config(), rows)

    rows = [
        row
        for row in _rows()
        if not (
            row["flower_role"] == "POLLINATION_SENTINEL"
            and row["observation_time_hours"] != "4"
        )
    ]
    with pytest.raises(ValueError, match=">=2 pollination sentinel time points"):
        build(_config(), rows)


def test_median_gap_descriptor_can_detect_temporal_entanglement_on_grid() -> None:
    rows = _rows()

    for row in rows:
        if (
            row["flower_role"] == "POLLINATION_SENTINEL"
            and row["observation_time_hours"] == "8"
        ):
            row["pollination_complete"] = "0"

    p01_at_8 = next(
        row
        for row in rows
        if row["flower_id"] == "P01_N"
        and row["observation_time_hours"] == "8"
    )
    p01_at_8["attack_present"] = "1"

    result = build(_config(), rows)
    gap = result["median_temporal_separability_descriptor"]

    assert result["median_pollination_completion_interval_hours"][
        "lower_bound_hours"
    ] == pytest.approx(8.0)
    assert result["median_pollination_completion_interval_hours"][
        "upper_bound_hours"
    ] == pytest.approx(12.0)
    assert result["median_constraint_onset_interval_hours"][
        "lower_bound_hours"
    ] == pytest.approx(4.0)
    assert result["median_constraint_onset_interval_hours"][
        "upper_bound_hours"
    ] == pytest.approx(8.0)
    assert gap["delta_t50_upper_bound_hours"] == pytest.approx(0.0)
    assert gap["ordering_state"] == (
        "MEDIAN_TEMPORAL_ENTANGLEMENT_SUPPORTED_ON_SAMPLED_GRID"
    )
    assert gap["method_development_route_implication"] == (
        "LATE_BARRIER_ROUTE_NOT_SUPPORTED_AT_MEDIAN_SCALE_"
        "TEST_OVERLAP_COMPATIBLE_LOCAL_BARRIER"
    )
    assert gap["candidate_selected"] is False


def test_delta_t50_remains_exploratory_and_does_not_select_barrier_hours() -> None:
    result = build(_config(), _rows())
    assert result["temporal_separability_inferred"] is False
    assert result["timing_window_selected"] is False
    assert (
        "delta_t50_is_a_schedule_grid_median_descriptor_not_an_exact_individual_gap"
        in result["claim_ceiling"]
    )
