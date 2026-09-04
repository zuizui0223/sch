from __future__ import annotations

from scripts.analyze_sch_compromise_surface import analyze
from scripts.identify_sch_pure_function_optima import identify


def _base_config() -> dict:
    return {
        "bootstrap_reps": 300,
        "random_seed": 17,
        "min_z_levels": 5,
        "min_valid_bootstrap_fraction": 0.8,
        "min_interior_bootstrap_fraction": 0.9,
        "min_optimum_separation": 0.5,
        "min_optimum_shift": 0.25,
        "min_abs_component_gradient": 0.25,
    }


def _pure_config() -> dict:
    return {
        "bootstrap_reps": 300,
        "random_seed": 19,
        "min_z_levels": 5,
        "min_valid_bootstrap_fraction": 0.8,
        "min_component_interior_bootstrap_fraction": 0.9,
        "max_context_optimum_difference": 0.2,
    }


def _stable_rows() -> list[dict[str, str]]:
    rows = []
    for plant in range(18):
        plant_effect = (plant % 3) * 0.05
        for z in (-2, -1, 0, 1, 2):
            baseline = 30.0 + plant_effect
            m = 10.0 - (z - 1.5) ** 2
            h = -(z + 1.5) ** 2
            for p, g in ((0, 0), (1, 0), (0, 1), (1, 1)):
                fitness = baseline + (m if p else 0.0) + (h if g else 0.0)
                rows.append(
                    {
                        "plant_id": f"P{plant:02d}",
                        "blossom_id": f"P{plant:02d}_Z{z:+d}_P{p}G{g}",
                        "z_level": f"Z{z:+d}",
                        "z_measured": str(float(z)),
                        "pollinator_state": str(p),
                        "antagonist_state": str(g),
                        "fitness_value": f"{fitness:.5f}",
                    }
                )
    return rows


def _context_dependent_rows() -> list[dict[str, str]]:
    rows = _stable_rows()
    for row in rows:
        if row["pollinator_state"] == "1" and row["antagonist_state"] == "1":
            z = float(row["z_measured"])
            # Shift the pollinator component strongly in the G1 context while
            # retaining an overall interior combined surface.
            row["fitness_value"] = str(float(row["fitness_value"]) + 2.5 * z)
    return rows


def test_context_stable_components_promote_pure_function_optima() -> None:
    rows = _stable_rows()
    base = analyze(rows, _base_config())
    assert base["status"] == "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE"
    upgraded = identify(rows, base, _pure_config())
    assert upgraded["pure_function_upgrade"]["status"] == "CONTEXT_STABLE_COMPONENT_OPTIMA_IDENTIFIED"
    pure = upgraded["identified_pure_function_optima"]
    assert abs(pure["z_F1"] - 1.5) < 1e-8
    assert abs(pure["z_F2"] + 1.5) < 1e-8
    assert pure["semantics"] == "CONTEXT_STABLE_CAUSAL_COMPONENT_OPTIMA_ON_COMMON_REPRODUCTIVE_SCALE"


def test_context_dependent_components_do_not_get_relabelled_as_pure_optima() -> None:
    rows = _context_dependent_rows()
    base = analyze(rows, _base_config())
    assert base["status"] == "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE"
    upgraded = identify(rows, base, _pure_config())
    assert upgraded["pure_function_upgrade"]["status"] == "PURE_FUNCTION_OPTIMA_NOT_IDENTIFIED"
    assert "identified_pure_function_optima" not in upgraded
