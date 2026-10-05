from __future__ import annotations

import argparse
import json
from pathlib import Path


SURFACE_SCHEMA = "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1"
SURFACE_WRAPPER = "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2"
POSITIVE_SURFACE = "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE"
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


def _validate_same_context(
    named_payloads: list[tuple[str, dict | None]],
) -> tuple[str, str]:
    observed = [
        (label, _context(payload, label))
        for label, payload in named_payloads
        if payload is not None
    ]
    if not observed:
        raise ValueError("at least one Pedicularis result receipt is required")
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


def _surface_state(surface: dict | None) -> dict:
    if surface is None:
        return {
            "status": "NOT_EVALUATED",
            "causal_compromise_supported": False,
        }
    if surface.get("receipt_schema_version") != SURFACE_SCHEMA:
        raise ValueError("surface receipt schema mismatch")
    if surface.get("system_wrapper_schema_version") != SURFACE_WRAPPER:
        raise ValueError("surface receipt is not the active Pedicularis wrapper")
    if surface.get("system") != "Pedicularis rex":
        raise ValueError("surface receipt is not Pedicularis rex")
    return {
        "status": surface.get("status"),
        "causal_compromise_supported": (
            surface.get("status") == POSITIVE_SURFACE
        ),
        "surface_data_sha256": surface.get("surface_data_sha256"),
        "surface_data_n_rows": surface.get("surface_data_n_rows"),
    }


def _antagonist_state(
    antagonist: dict | None,
    surface: dict | None,
) -> dict:
    if antagonist is None:
        return {
            "status": "NOT_EVALUATED",
            "enemy_induced_optimum_displacement_supported": False,
            "pollen_performance_cost_supported": False,
            "initial_seed_cost_supported": False,
        }
    if surface is None or surface.get("status") != POSITIVE_SURFACE:
        raise ValueError(
            "antagonist diagnostic requires a positive full-surface receipt"
        )
    if antagonist.get("surface_status") != POSITIVE_SURFACE:
        raise ValueError(
            "antagonist diagnostic is not downstream of a positive surface"
        )
    if antagonist.get("surface_data_fingerprint_match") is not True:
        raise ValueError("antagonist diagnostic lacks positive fingerprint match")
    if antagonist.get("surface_data_sha256") != surface.get(
        "surface_data_sha256"
    ):
        raise ValueError(
            "antagonist diagnostic and full surface use different raw data"
        )
    if antagonist.get("pollinator_favored_optimum_identified") is not False:
        raise ValueError(
            "state-specific antagonist diagnostic must not promote a pure "
            "pollinator optimum"
        )

    shift = antagonist.get("predator_removal_shifts_optimum_upward")
    pollen = antagonist.get(
        "antagonist_shift_away_from_higher_pollen_receipt_supported"
    )
    seed = antagonist.get(
        "antagonist_shift_away_from_higher_initial_seed_set_supported"
    )
    if not all(isinstance(value, bool) for value in (shift, pollen, seed)):
        raise ValueError("antagonist diagnostic lacks registered boolean results")
    if pollen and not shift:
        raise ValueError("pollen-cost chain cannot pass without optimum shift")
    if seed and not pollen:
        raise ValueError("initial-seed tier cannot pass without pollen tier")

    return {
        "status": antagonist.get("status"),
        "enemy_induced_optimum_displacement_supported": shift,
        "pollen_performance_cost_supported": pollen,
        "initial_seed_cost_supported": seed,
        "z_predator_free_state": antagonist.get(
            "z_predator_free_natural_pollination_state_optimum"
        ),
        "z_predator_exposed_state": antagonist.get(
            "z_predator_exposed_natural_pollination_state_optimum"
        ),
        "pollinator_favored_optimum_identified": False,
        "antagonist_contribution_to_pollen_limitation_identified": False,
    }


def _pure_function_state(
    pure_function: dict | None,
    surface: dict | None,
) -> dict:
    if pure_function is None:
        return {
            "status": "NOT_EVALUATED",
            "context_stable_component_optima_identified": False,
        }
    if surface is None:
        raise ValueError("pure-function upgrade requires a surface receipt")
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


def _headline(
    surface_state: dict,
    antagonist_state: dict,
) -> tuple[str, str]:
    if surface_state["status"] == "NOT_EVALUATED":
        return (
            "EMPIRICAL_SURFACE_NOT_YET_RUN",
            "No causal Pedicularis ecological headline is licensed yet.",
        )
    if not surface_state["causal_compromise_supported"]:
        return (
            "CAUSAL_COMPROMISE_NOT_RECOVERED_IN_TESTED_CONTEXT",
            "The tested population/season does not recover the registered "
            "causal compromise geometry.",
        )
    if antagonist_state["status"] == "NOT_EVALUATED":
        return (
            "CAUSAL_COMPROMISE_RECOVERED_SECONDARY_ENEMY_SHIFT_NOT_YET_TESTED",
            "Causal compromise is recovered, but the enemy-induced optimum "
            "displacement hypothesis has not yet been evaluated.",
        )
    if antagonist_state["initial_seed_cost_supported"]:
        return (
            "ENEMY_INDUCED_OPTIMUM_DISPLACEMENT_WITH_POLLEN_AND_INITIAL_SEED_COST",
            "Seed-predator exposure shifts the reproductive state optimum "
            "toward lower exsertion, away from trait states with greater pollen "
            "receipt and greater initial seed set.",
        )
    if antagonist_state["pollen_performance_cost_supported"]:
        return (
            "ENEMY_INDUCED_OPTIMUM_DISPLACEMENT_WITH_POLLEN_COST",
            "Seed-predator exposure shifts the reproductive state optimum "
            "toward lower exsertion, away from trait states with greater pollen "
            "receipt.",
        )
    if antagonist_state["enemy_induced_optimum_displacement_supported"]:
        return (
            "ENEMY_INDUCED_OPTIMUM_DISPLACEMENT_WITHOUT_POLLINATION_COST",
            "Seed-predator exposure shifts the reproductive state optimum, "
            "but the shift is not supported as a cost to the registered "
            "pollination-performance responses.",
        )
    return (
        "CAUSAL_COMPROMISE_WITHOUT_DIRECTIONAL_ENEMY_DISPLACEMENT",
        "Causal compromise is recovered, but predator removal does not support "
        "the preregistered upward optimum shift.",
    )


def build(
    *,
    event_time: dict | None,
    surface: dict | None,
    antagonist: dict | None,
    pure_function: dict | None,
) -> dict:
    population_id, season_id = _validate_same_context(
        [
            ("event_time", event_time),
            ("surface", surface),
            ("antagonist", antagonist),
            ("pure_function", pure_function),
        ]
    )

    timing = _timing_state(event_time)
    surface_result = _surface_state(surface)
    antagonist_result = _antagonist_state(antagonist, surface)
    pure_result = _pure_function_state(pure_function, surface)
    headline_code, headline = _headline(surface_result, antagonist_result)

    permitted_claims = []
    if surface_result["causal_compromise_supported"]:
        permitted_claims.append(
            "causal_state_specific_multifunctional_compromise_in_tested_context"
        )
    if antagonist_result["enemy_induced_optimum_displacement_supported"]:
        permitted_claims.append(
            "seed_predator_exposure_causes_downward_reproductive_state_optimum_shift"
        )
    if antagonist_result["pollen_performance_cost_supported"]:
        permitted_claims.append(
            "enemy_induced_optimum_shift_moves_away_from_higher_pollen_receipt"
        )
    if antagonist_result["initial_seed_cost_supported"]:
        permitted_claims.append(
            "enemy_induced_optimum_shift_moves_away_from_higher_initial_seed_set"
        )
    if pure_result["context_stable_component_optima_identified"]:
        permitted_claims.append(
            "context_stable_pollinator_and_antagonist_component_optima_identified"
        )

    prohibited_claims = [
        "do_not_claim_historical_adaptation",
        "do_not_claim_predator_cue_identity",
        "do_not_claim_adaptive_pollen_limitation",
        "do_not_use_Delta_T50_as_confirmatory_barrier_hour",
    ]
    if not pure_result["context_stable_component_optima_identified"]:
        prohibited_claims.append(
            "do_not_relabel_state_specific_optima_as_pure_function_optima"
        )
    if not antagonist_result["initial_seed_cost_supported"]:
        prohibited_claims.append(
            "do_not_claim_enemy_displacement_reduces_initial_seed_set"
        )
    prohibited_claims.append(
        "do_not_claim_antagonists_maintain_population_pollen_limitation"
    )

    return {
        "analysis": "pedicularis_empirical_outcome_map_v1",
        "population_id": population_id,
        "season_id": season_id,
        "headline_result_code": headline_code,
        "headline_ecological_conclusion": headline,
        "timing_mechanism": timing,
        "primary_surface": surface_result,
        "enemy_displacement_secondary": antagonist_result,
        "pure_function_upgrade": pure_result,
        "permitted_claims": permitted_claims,
        "prohibited_claims": prohibited_claims,
        "paper_spine": (
            "natural conflict -> temporal feasibility -> randomized z x P x G "
            "surface -> enemy-induced state-optimum displacement -> "
            "pollination-performance consequence"
        ),
        "status": "PEDICULARIS_EMPIRICAL_OUTCOME_INTERPRETATION_READY",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Map completed P. rex receipts to prospectively bounded ecological "
            "conclusions without promoting state optima or calibration outputs"
        )
    )
    parser.add_argument("--event-time", type=Path)
    parser.add_argument("--surface", type=Path)
    parser.add_argument("--antagonist", type=Path)
    parser.add_argument("--pure-function", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(
        event_time=_load(args.event_time),
        surface=_load(args.surface),
        antagonist=_load(args.antagonist),
        pure_function=_load(args.pure_function),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
