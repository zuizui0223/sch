from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ALLOWED_VERSIONED_RUNTIME = {
    "evaluate_sch_h2_reversal_holdout_v1.py",
    "evaluate_sch_h2_reversal_holdout_v2.py",
    "evaluate_sch_h2_reversal_holdout_v3.py",
    "harvest_sch_prisma_candidates_v2.py",
}

REMOVED_RUNTIME_NAMES = {
    "build_sch_h2_selection_cluster_expansion_v7.py",
    "build_sch_h2_selection_cluster_expansion_v8.py",
    "build_sch_h2_selection_cluster_expansion_v9.py",
    "build_sch_macroecology_h2_context_cases_cumulative_v2.py",
    "build_sch_macroecology_h2_context_cases_cumulative_v3.py",
    "build_sch_macroecology_h2_context_cases_cumulative_v4.py",
    "build_sch_macroecology_h2_context_cases_cumulative_v5.py",
    "build_sch_macroecology_h2_context_cases_cumulative_v6.py",
    "build_sch_macroecology_h2_context_cases_cumulative_v7.py",
    "build_sch_macroecology_h2_measurement_layer_v3.py",
    "build_sch_macroecology_h2_measurement_layer_v4.py",
    "build_sch_macroecology_h2_measurement_layer_v5.py",
    "build_sch_macroecology_h2_measurement_layer_v6.py",
    "build_sch_macroecology_h2_measurement_layer_v7.py",
    "build_sch_macroecology_h2_change_type_seed_v3.py",
    "build_sch_macroecology_h2_change_type_seed_v4.py",
    "build_sch_macroecology_h2_change_type_seed_v5.py",
    "build_sch_macroecology_h2_change_type_seed_v6.py",
    "build_sch_macroecology_h2_change_type_seed_v7.py",
    "diagnose_sch_macroecology_h2_modelability_v2.py",
    "diagnose_sch_macroecology_h2_modelability_v3.py",
    "diagnose_sch_macroecology_h2_modelability_v4.py",
    "diagnose_sch_macroecology_h2_modelability_v5.py",
    "diagnose_sch_macroecology_h2_modelability_v6.py",
    "analyze_pedicularis_full_surface_v2.py",
    "evaluate_pedicularis_predator_method_v3.py",
    "analyze_sch_h2_total_selection_direction_v10.py",
    "analyze_sch_h2_switch_mechanisms_v11.py",
    "build_sch_h2_estimand_recovery_audit_cumulative_v2.py",
}


def test_versioned_runtime_files_are_protocol_exceptions_only():
    actual = {
        path.name
        for path in (ROOT / "scripts").glob("*_v*.py")
        if path.stem.rsplit("_v", 1)[-1].isdigit()
    }
    assert actual == ALLOWED_VERSIONED_RUNTIME


def test_removed_runtime_names_are_not_referenced_by_active_code_or_docs():
    roots = [
        ROOT / "scripts",
        ROOT / "tests",
        ROOT / "docs",
        ROOT / ".github",
        ROOT / "README.md",
    ]
    hits = []
    for root in roots:
        paths = [root] if root.is_file() else [
            path for path in root.rglob("*") if path.is_file()
        ]
        for path in paths:
            if path == Path(__file__):
                continue
            if path.suffix not in {".py", ".md", ".yml", ".yaml", ".txt"}:
                continue
            text = path.read_text(encoding="utf-8")
            for removed in REMOVED_RUNTIME_NAMES:
                if removed in text:
                    hits.append(f"{path.relative_to(ROOT)} -> {removed}")
    assert hits == []
