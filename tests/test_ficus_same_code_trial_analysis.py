from __future__ import annotations

import pytest

from scripts.analyze_ficus_same_code_trials import analyze_trials


BASE = {
    "species": "Ficus_semicordata",
    "code_id": "4_METHYLANISOLE_V1",
    "assay_day": "2026-08-29",
    "assay_batch": "B1",
    "fig_stage": "STAGE_MATCHED",
    "apparatus_id": "Y_TUBE_REGISTERED",
    "stimulus_id": "FOCAL",
    "control_id": "CONTROL",
}


def _rows(*, npfw_code_successes: int = 5, clusters: int = 6, no_choices_per_cluster: int = 2):
    rows = []
    trial = 0
    for cluster in range(clusters):
        cluster_id = f"C{cluster:02d}"
        roles = (
            ("POLLINATOR_CODE", "POLLINATOR", "Ceratosolen_gravelyi", 8),
            ("NPFW_POSITIVE_CONTROL", "NPFW", "Platyneura_cunia", 8),
            ("NPFW_SAME_CODE", "NPFW", "Platyneura_cunia", npfw_code_successes),
        )
        for role, guild, taxon, successes in roles:
            for i in range(10):
                trial += 1
                rows.append(
                    {
                        **BASE,
                        "trial_id": f"T{trial:04d}",
                        "receiver_taxon": taxon,
                        "receiver_guild": guild,
                        "assay_role": role,
                        "cluster_id": cluster_id,
                        "choice": "CODE" if i < successes else "CONTROL",
                    }
                )
            for _ in range(no_choices_per_cluster):
                trial += 1
                rows.append(
                    {
                        **BASE,
                        "trial_id": f"T{trial:04d}",
                        "receiver_taxon": taxon,
                        "receiver_guild": guild,
                        "assay_role": role,
                        "cluster_id": cluster_id,
                        "choice": "NO_CHOICE",
                    }
                )
    return rows


def test_balanced_npfw_choices_support_behavioral_equivalence_when_controls_work() -> None:
    result = analyze_trials(_rows(npfw_code_successes=5), iterations=1000)
    assert result["decision"]["status"] == "BEHAVIORAL_NONRESPONSE_EQUIVALENT"
    assert result["roles"]["NPFW_SAME_CODE"]["choice_probability"] == 0.5
    assert result["roles"]["NPFW_SAME_CODE"]["no_choice"] == 12
    assert result["roles"]["NPFW_SAME_CODE"]["decisive_cluster_count"] == 6
    assert result["roles"]["NPFW_SAME_CODE"]["directional_95pct_cluster_bootstrap"] == {
        "low": 0.5,
        "high": 0.5,
    }
    assert result["roles"]["NPFW_SAME_CODE"]["equivalence_90pct_cluster_bootstrap"] == {
        "low": 0.5,
        "high": 0.5,
    }
    assert not result["planning_benchmarks"]["meets_privacy_80pct_planning_benchmark"]


def test_strong_npfw_same_code_choice_is_interception() -> None:
    result = analyze_trials(_rows(npfw_code_successes=7), iterations=1000)
    assert result["decision"]["status"] == "SAME_CODE_INTERCEPTION"
    assert result["roles"]["NPFW_SAME_CODE"]["choice_probability"] == 0.7


def test_frozen_code_mismatch_fails_closed() -> None:
    rows = _rows()
    for row in rows:
        if row["assay_role"] == "NPFW_SAME_CODE":
            row["code_id"] = "DIFFERENT_CODE"
    with pytest.raises(ValueError, match="one frozen code_id"):
        analyze_trials(rows, iterations=1000)


def test_npfw_taxon_must_match_between_positive_control_and_same_code() -> None:
    rows = _rows()
    for row in rows:
        if row["assay_role"] == "NPFW_SAME_CODE":
            row["receiver_taxon"] = "Sycoscapter_trifemmensis"
    with pytest.raises(ValueError, match="same focal NPFW taxon"):
        analyze_trials(rows, iterations=1000)


def test_too_few_decisive_clusters_is_not_analyzable() -> None:
    with pytest.raises(ValueError, match="need at least 4 decisive clusters"):
        analyze_trials(_rows(clusters=3), iterations=1000)
