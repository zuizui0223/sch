from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.classify_pedicularis_empirical_outcome import (
    DEFAULT_WORLDS,
    POSITIVE_SURFACE,
    _read_worlds,
    build as classify_world,
)


EVENT_STATUS = "G_EVENT_TIME_DESCRIPTORS_READY_NO_WINDOW_SELECTED"
PURE_STATUS = "CONTEXT_STABLE_COMPONENT_OPTIMA_IDENTIFIED"


def _load(path: Path | None) -> dict | None:
    if path is None:
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _context(payload: dict, label: str) -> tuple[str, str]:
    population = payload.get("population_id")
    season = payload.get("season_id")
    if not isinstance(population, str) or not population:
        raise ValueError(f"{label} population_id is missing")
    if not isinstance(season, str) or not season:
        raise ValueError(f"{label} season_id is missing")
    return population, season


def _require_same_context(
    surface: dict,
    event_time: dict | None,
    antagonist: dict | None,
    pure_function: dict | None,
) -> tuple[str, str]:
    named = [
        ("surface", surface),
        ("event_time", event_time),
        ("antagonist", antagonist),
        ("pure_function", pure_function),
    ]
    observed = [
        (label, _context(payload, label))
        for label, payload in named
        if payload is not None
    ]
    contexts = {context for _, context in observed}
    if len(contexts) != 1:
        detail = ", ".join(
            f"{label}={context[0]}/{context[1]}"
            for label, context in observed
        )
        raise ValueError(
            "Pedicularis outcome receipts must share one population/season: "
            + detail
        )
    return next(iter(contexts))


def _timing_state(event_time: dict | None) -> dict:
    if event_time is None:
        return {
            "status": "NOT_EVALUATED",
            "headline_role": "enabling_ecological_mechanism_only",
            "method_route": None,
        }
    if event_time.get("status") != EVENT_STATUS:
        raise ValueError("event-time receipt is not a valid descriptor receipt")
    if event_time.get("sampling_grid_prospectively_frozen") is not True:
        raise ValueError("event-time receipt lacks frozen sampling-grid provenance")
    descriptor = event_time.get("median_temporal_separability_descriptor")
    if not isinstance(descriptor, dict):
        raise ValueError("event-time receipt lacks Delta_T50 descriptor")
    ordering = descriptor.get("ordering_state")
    allowed = {
        "MEDIAN_TEMPORAL_SEPARATION_SUPPORTED_ON_SAMPLED_GRID",
        "MEDIAN_TEMPORAL_ENTANGLEMENT_SUPPORTED_ON_SAMPLED_GRID",
        "MEDIAN_TEMPORAL_ORDERING_UNRESOLVED_ON_SAMPLED_GRID",
    }
    if ordering not in allowed:
        raise ValueError("event-time receipt has an unregistered ordering state")
    return {
        "status": ordering,
        "headline_role": "enabling_ecological_mechanism_only",
        "method_route": descriptor.get("method_development_route_implication"),
        "delta_t50_lower_bound_hours": descriptor.get(
            "delta_t50_lower_bound_hours"
        ),
        "delta_t50_upper_bound_hours": descriptor.get(
            "delta_t50_upper_bound_hours"
        ),
    }


def _pure_function_state(
    pure_function: dict | None,
    surface: dict,
) -> dict:
    if pure_function is None:
        return {
            "status": "NOT_EVALUATED",
            "context_stable_component_optima_identified": False,
        }
    if surface.get("status") != POSITIVE_SURFACE:
        raise ValueError(
            "pure-function upgrade is not admissible after a negative primary surface"
        )
    if pure_function.get("surface_data_sha256") != surface.get(
        "surface_data_sha256"
    ):
        raise ValueError("pure-function receipt is not bound to the same surface")
    upgrade = pure_function.get("pure_function_upgrade")
    if not isinstance(upgrade, dict):
        raise ValueError("pure-function receipt lacks upgrade object")
    status = upgrade.get("status")
    if status not in {PURE_STATUS, "PURE_FUNCTION_OPTIMA_NOT_IDENTIFIED"}:
        raise ValueError("unregistered pure-function upgrade status")
    identified = status == PURE_STATUS
    if identified and not isinstance(
        pure_function.get("identified_pure_function_optima"), dict
    ):
        raise ValueError(
            "positive pure-function receipt lacks identified component optima"
        )
    return {
        "status": status,
        "context_stable_component_optima_identified": identified,
        "identified_pure_function_optima": (
            pure_function.get("identified_pure_function_optima")
            if identified
            else None
        ),
    }


def _permitted_claims(world: dict, pure: dict) -> list[str]:
    world_id = world.get("world_id")
    claims: list[str] = []
    if world_id in {"W1", "W2", "W3", "W4", "W5"}:
        claims.append(
            "causal_state_specific_multifunctional_compromise_in_tested_context"
        )
    if world_id in {"W1", "W2", "W3"}:
        claims.append(
            "seed_predator_exposure_causes_downward_reproductive_state_optimum_shift"
        )
    if world_id in {"W1", "W2"}:
        claims.append(
            "enemy_induced_optimum_shift_moves_away_from_higher_pollen_receipt"
        )
    if world_id == "W1":
        claims.append(
            "enemy_induced_optimum_shift_moves_away_from_higher_initial_seed_set"
        )
    if pure["context_stable_component_optima_identified"]:
        claims.append(
            "context_stable_pollinator_and_antagonist_component_optima_identified"
        )
    return claims


def _prohibited_claims(world: dict, pure: dict) -> list[str]:
    prohibited = [
        "do_not_claim_historical_adaptation",
        "do_not_claim_predator_cue_identity",
        "do_not_claim_adaptive_pollen_limitation",
        "do_not_claim_antagonists_maintain_population_pollen_limitation",
        "do_not_use_Delta_T50_as_confirmatory_barrier_hour",
    ]
    if not pure["context_stable_component_optima_identified"]:
        prohibited.append(
            "do_not_relabel_state_specific_optima_as_pure_function_optima"
        )
    if world.get("world_id") != "W1":
        prohibited.append(
            "do_not_claim_enemy_displacement_reduces_initial_seed_set"
        )
    if world.get("world_id") not in {"W1", "W2"}:
        prohibited.append(
            "do_not_claim_enemy_displacement_reduces_pollination_performance"
        )
    return prohibited


def build(
    *,
    surface: dict,
    antagonist: dict | None,
    event_time: dict | None,
    pure_function: dict | None,
    world_rows: list[dict[str, str]] | None = None,
) -> dict:
    population_id, season_id = _require_same_context(
        surface,
        event_time,
        antagonist,
        pure_function,
    )
    worlds = _read_worlds(DEFAULT_WORLDS) if world_rows is None else world_rows
    primary_world = classify_world(surface, antagonist, worlds)
    timing = _timing_state(event_time)
    pure = _pure_function_state(pure_function, surface)

    return {
        "analysis": "pedicularis_empirical_interpretation_bundle_v1",
        "population_id": population_id,
        "season_id": season_id,
        "primary_outcome_world": primary_world,
        "headline_result_code": (
            primary_world.get("biological_state")
            or primary_world.get("status")
        ),
        "headline_ecological_conclusion": (
            primary_world.get("allowed_headline")
            or "Positive primary surface recovered; secondary enemy-displacement "
            "diagnostic remains pending."
        ),
        "timing_mechanism": timing,
        "pure_function_upgrade": pure,
        "permitted_claims": _permitted_claims(primary_world, pure),
        "prohibited_claims": _prohibited_claims(primary_world, pure),
        "paper_spine": (
            "natural conflict -> temporal feasibility -> randomized z x P x G "
            "surface -> predeclared W0-W5 world -> optional component-optimum "
            "promotion"
        ),
        "status": "PEDICULARIS_EMPIRICAL_INTERPRETATION_BUNDLE_READY",
        "claim_ceiling": [
            "W0_W5_classifier_is_the_single_source_of_primary_outcome_assignment",
            "timing_is_enabling_mechanism_not_headline_outcome",
            "pure_function_promotion_is_separate_from_state_optimum_world",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Assemble the predeclared P. rex W0-W5 ecological outcome with "
            "optional temporal-separability and pure-function receipts"
        )
    )
    parser.add_argument("surface", type=Path)
    parser.add_argument("--antagonist", type=Path)
    parser.add_argument("--event-time", type=Path)
    parser.add_argument("--pure-function", type=Path)
    parser.add_argument("--worlds", type=Path, default=DEFAULT_WORLDS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(
        surface=_load(args.surface),
        antagonist=_load(args.antagonist),
        event_time=_load(args.event_time),
        pure_function=_load(args.pure_function),
        world_rows=_read_worlds(args.worlds),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
