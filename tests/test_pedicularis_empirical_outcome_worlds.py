from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.classify_pedicularis_empirical_outcome import (
    DEFAULT_WORLDS,
    NEGATIVE_SURFACE,
    POSITIVE_SURFACE,
    _read_worlds,
    build,
)


def _surface(status: str = POSITIVE_SURFACE) -> dict:
    return {
        "status": status,
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "surface_data_sha256": "a" * 64,
    }


def _secondary(
    *,
    shift: bool,
    pollen: bool,
    seed: bool,
) -> dict:
    return {
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "surface_data_sha256": "a" * 64,
        "surface_data_fingerprint_match": True,
        "predator_removal_shifts_optimum_upward": shift,
        "higher_z_increases_pollen_receipt_in_both_G_states": pollen,
        "higher_z_increases_initial_seed_set_in_both_G_states": seed,
        "pollinator_favored_optimum_identified": False,
        "antagonist_contribution_to_pollen_limitation_identified": False,
    }


def _build(status: str, secondary: dict | None) -> dict:
    return build(_surface(status), secondary, _read_worlds(DEFAULT_WORLDS))


def test_negative_primary_surface_is_world_zero() -> None:
    result = _build(NEGATIVE_SURFACE, None)
    assert result["world_id"] == "W0"
    assert result["biological_state"] == "NO_CAUSAL_COMPROMISE_SURFACE"
    assert "secondary enemy-displacement story" in result["claim_ceiling"]


@pytest.mark.parametrize(
    ("shift", "pollen", "seed", "world_id"),
    [
        (True, True, True, "W1"),
        (True, True, False, "W2"),
        (True, False, True, "W3"),
        (True, False, False, "W3"),
        (False, True, True, "W4"),
        (False, True, False, "W4"),
        (False, False, True, "W5"),
        (False, False, False, "W5"),
    ],
)
def test_positive_surface_worlds_are_exhaustive(
    shift: bool,
    pollen: bool,
    seed: bool,
    world_id: str,
) -> None:
    result = _build(
        POSITIVE_SURFACE,
        _secondary(shift=shift, pollen=pollen, seed=seed),
    )
    assert result["world_id"] == world_id
    assert result["status"] == f"PEDICULARIS_EMPIRICAL_OUTCOME_{world_id}_ASSIGNED"


def test_positive_surface_waits_for_secondary_without_assigning_a_world() -> None:
    result = _build(POSITIVE_SURFACE, None)
    assert result["world_id"] is None
    assert result["status"] == (
        "POSITIVE_PRIMARY_SURFACE_SECONDARY_DIAGNOSTIC_PENDING"
    )


def test_world_map_never_promotes_pure_optimum_or_pollen_limitation_maintenance() -> None:
    for shift, pollen, seed in (
        (True, True, True),
        (True, True, False),
        (True, False, True),
        (False, True, True),
        (False, False, False),
    ):
        result = _build(
            POSITIVE_SURFACE,
            _secondary(shift=shift, pollen=pollen, seed=seed),
        )
        assert result["pure_pollinator_optimum_identified_by_world_map"] is False
        assert (
            result[
                "antagonist_maintenance_of_pollen_limitation_identified_by_world_map"
            ]
            is False
        )
        assert result["historical_adaptation_identified_by_world_map"] is False


def test_secondary_must_match_the_exact_surface_receipt_context_and_fingerprint() -> None:
    secondary = _secondary(shift=True, pollen=True, seed=True)
    secondary["surface_data_sha256"] = "b" * 64
    with pytest.raises(ValueError, match="surface_data_sha256"):
        _build(POSITIVE_SURFACE, secondary)

    secondary = _secondary(shift=True, pollen=True, seed=True)
    secondary["season_id"] = "S2"
    with pytest.raises(ValueError, match="season_id"):
        _build(POSITIVE_SURFACE, secondary)


def test_secondary_is_not_admissible_after_negative_primary_surface() -> None:
    with pytest.raises(ValueError, match="not admissible"):
        _build(
            NEGATIVE_SURFACE,
            _secondary(shift=False, pollen=False, seed=False),
        )


def test_secondary_cannot_promote_forbidden_claims() -> None:
    secondary = _secondary(shift=True, pollen=True, seed=True)
    secondary["pollinator_favored_optimum_identified"] = True
    with pytest.raises(ValueError, match="pure pollinator optimum"):
        _build(POSITIVE_SURFACE, secondary)

    secondary = _secondary(shift=True, pollen=True, seed=True)
    secondary["antagonist_contribution_to_pollen_limitation_identified"] = True
    with pytest.raises(ValueError, match="pollen limitation"):
        _build(POSITIVE_SURFACE, secondary)


def test_world_ledger_contains_exactly_six_predeclared_worlds() -> None:
    rows = _read_worlds(DEFAULT_WORLDS)
    assert [row["world_id"] for row in rows] == [
        "W0",
        "W1",
        "W2",
        "W3",
        "W4",
        "W5",
    ]
