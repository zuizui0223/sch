from __future__ import annotations

import pytest

from scripts.map_pedicularis_empirical_outcomes import build


FP = "a" * 64


def _event(ordering: str = "MEDIAN_TEMPORAL_SEPARATION_SUPPORTED_ON_SAMPLED_GRID") -> dict:
    return {
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "status": "G_EVENT_TIME_DESCRIPTORS_READY_NO_WINDOW_SELECTED",
        "sampling_grid_prospectively_frozen": True,
        "median_temporal_separability_descriptor": {
            "ordering_state": ordering,
            "method_development_route_implication": "ROUTE",
            "delta_t50_lower_bound_hours": 1.0,
            "delta_t50_upper_bound_hours": 5.0,
        },
    }


def _surface(status: str = "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE") -> dict:
    return {
        "receipt_schema_version": "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1",
        "system_wrapper_schema_version": "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2",
        "system": "Pedicularis rex",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "status": status,
        "surface_data_sha256": FP,
        "surface_data_n_rows": 100,
    }


def _antagonist(
    *,
    shift: bool = True,
    pollen: bool = True,
    seed: bool = True,
) -> dict:
    return {
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "surface_status": "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE",
        "surface_data_sha256": FP,
        "surface_data_fingerprint_match": True,
        "status": "SYNTHETIC_TEST_STATUS",
        "predator_removal_shifts_optimum_upward": shift,
        "antagonist_shift_away_from_higher_pollen_receipt_supported": pollen,
        "antagonist_shift_away_from_higher_initial_seed_set_supported": seed,
        "z_predator_free_natural_pollination_state_optimum": 0.8,
        "z_predator_exposed_natural_pollination_state_optimum": 0.5,
        "pollinator_favored_optimum_identified": False,
        "antagonist_contribution_to_pollen_limitation_identified": False,
    }


def _pure(identified: bool = True) -> dict:
    payload = {
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "surface_data_sha256": FP,
        "pure_function_upgrade": {
            "status": (
                "CONTEXT_STABLE_COMPONENT_OPTIMA_IDENTIFIED"
                if identified
                else "PURE_FUNCTION_OPTIMA_NOT_IDENTIFIED"
            )
        },
    }
    if identified:
        payload["identified_pure_function_optima"] = {
            "z_F1": 0.9,
            "z_F2": 0.2,
        }
    return payload


def test_strongest_empirical_tier_is_enemy_shift_with_pollen_and_seed_cost() -> None:
    result = build(
        event_time=_event(),
        surface=_surface(),
        antagonist=_antagonist(),
        pure_function=None,
    )

    assert result["headline_result_code"] == (
        "ENEMY_INDUCED_OPTIMUM_DISPLACEMENT_WITH_POLLEN_AND_INITIAL_SEED_COST"
    )
    assert "greater pollen receipt" in result["headline_ecological_conclusion"]
    assert "greater initial seed set" in result["headline_ecological_conclusion"]
    assert (
        "seed_predator_exposure_causes_downward_reproductive_state_optimum_shift"
        in result["permitted_claims"]
    )
    assert (
        "do_not_relabel_state_specific_optima_as_pure_function_optima"
        in result["prohibited_claims"]
    )
    assert (
        "do_not_claim_antagonists_maintain_population_pollen_limitation"
        in result["prohibited_claims"]
    )


def test_pollen_only_tier_does_not_promote_initial_seed_cost() -> None:
    result = build(
        event_time=_event(),
        surface=_surface(),
        antagonist=_antagonist(seed=False),
        pure_function=None,
    )

    assert result["headline_result_code"] == (
        "ENEMY_INDUCED_OPTIMUM_DISPLACEMENT_WITH_POLLEN_COST"
    )
    assert (
        "enemy_induced_optimum_shift_moves_away_from_higher_initial_seed_set"
        not in result["permitted_claims"]
    )
    assert (
        "do_not_claim_enemy_displacement_reduces_initial_seed_set"
        in result["prohibited_claims"]
    )


def test_optimum_shift_without_pollination_cost_stays_biologically_distinct() -> None:
    result = build(
        event_time=_event(),
        surface=_surface(),
        antagonist=_antagonist(pollen=False, seed=False),
        pure_function=None,
    )

    assert result["headline_result_code"] == (
        "ENEMY_INDUCED_OPTIMUM_DISPLACEMENT_WITHOUT_POLLINATION_COST"
    )
    assert (
        "enemy_induced_optimum_shift_moves_away_from_higher_pollen_receipt"
        not in result["permitted_claims"]
    )


def test_negative_primary_surface_blocks_enemy_shift_interpretation() -> None:
    result = build(
        event_time=_event(),
        surface=_surface("COMPROMISE_CRITERIA_NOT_ALL_RECOVERED"),
        antagonist=None,
        pure_function=None,
    )

    assert result["headline_result_code"] == (
        "CAUSAL_COMPROMISE_NOT_RECOVERED_IN_TESTED_CONTEXT"
    )
    assert result["primary_surface"]["causal_compromise_supported"] is False
    assert result["permitted_claims"] == []


def test_temporal_entanglement_changes_method_route_not_headline_tier() -> None:
    result = build(
        event_time=_event(
            "MEDIAN_TEMPORAL_ENTANGLEMENT_SUPPORTED_ON_SAMPLED_GRID"
        ),
        surface=_surface(),
        antagonist=_antagonist(),
        pure_function=None,
    )

    assert result["timing_mechanism"]["status"] == (
        "MEDIAN_TEMPORAL_ENTANGLEMENT_SUPPORTED_ON_SAMPLED_GRID"
    )
    assert result["timing_mechanism"]["headline_role"] == (
        "enabling_ecological_mechanism_only"
    )
    assert result["headline_result_code"].startswith(
        "ENEMY_INDUCED_OPTIMUM_DISPLACEMENT"
    )


def test_pure_function_upgrade_is_separate_and_optional() -> None:
    result = build(
        event_time=_event(),
        surface=_surface(),
        antagonist=_antagonist(),
        pure_function=_pure(True),
    )

    assert result["pure_function_upgrade"][
        "context_stable_component_optima_identified"
    ] is True
    assert (
        "context_stable_pollinator_and_antagonist_component_optima_identified"
        in result["permitted_claims"]
    )
    assert (
        "do_not_relabel_state_specific_optima_as_pure_function_optima"
        not in result["prohibited_claims"]
    )


def test_pure_function_receipt_must_share_surface_fingerprint() -> None:
    pure = _pure(True)
    pure["surface_data_sha256"] = "b" * 64

    with pytest.raises(ValueError, match="same surface"):
        build(
            event_time=_event(),
            surface=_surface(),
            antagonist=_antagonist(),
            pure_function=pure,
        )


def test_antagonist_receipt_must_share_surface_fingerprint() -> None:
    ant = _antagonist()
    ant["surface_data_sha256"] = "b" * 64

    with pytest.raises(ValueError, match="different raw data"):
        build(
            event_time=_event(),
            surface=_surface(),
            antagonist=ant,
            pure_function=None,
        )


def test_all_receipts_must_share_population_and_season() -> None:
    event = _event()
    event["season_id"] = "S2"

    with pytest.raises(ValueError, match="share one population/season"):
        build(
            event_time=event,
            surface=_surface(),
            antagonist=_antagonist(),
            pure_function=None,
        )


def test_impossible_secondary_boolean_hierarchy_fails_closed() -> None:
    with pytest.raises(ValueError, match="cannot pass without optimum shift"):
        build(
            event_time=_event(),
            surface=_surface(),
            antagonist=_antagonist(shift=False, pollen=True, seed=False),
            pure_function=None,
        )

    with pytest.raises(ValueError, match="cannot pass without pollen tier"):
        build(
            event_time=_event(),
            surface=_surface(),
            antagonist=_antagonist(shift=True, pollen=False, seed=True),
            pure_function=None,
        )
