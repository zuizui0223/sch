from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from copy import deepcopy
from datetime import datetime
from pathlib import Path


from scripts.freeze_pedicularis_p1_design import (
    validate as validate_p1_design,
)
from scripts.pedicularis_config_freeze import (
    FREEZE_SCHEMA,
    FREEZE_STATUS,
    required_gate_paths,
    validate_prospective_freeze,
)


ROOT = Path(__file__).resolve().parents[1]

ASSEMBLY_SCHEMA = "SCH_PEDICULARIS_F0_CONFIG_ASSEMBLY_V1"
ASSEMBLY_INPUT_STATUS = "PEDICULARIS_F0_ASSEMBLY_INPUTS_PROSPECTIVELY_FROZEN"
ASSEMBLY_STATUS = "PEDICULARIS_F0_CONFIGS_ASSEMBLED_AND_FROZEN"

DEFAULT_TEMPLATES = {
    "P0": ROOT / "empirical" / "architecture" / "PEDICULARIS_STAGE_P0_CONFIG_TEMPLATE_V1.json",
    "P1": ROOT / "empirical" / "architecture" / "PEDICULARIS_POLLINATION_WEIGHT_CONFIG_TEMPLATE_V1.json",
    "G": ROOT / "empirical" / "architecture" / "PEDICULARIS_PREDATOR_METHOD_CONFIG_V3.json",
}

REGISTERED_VALUES = {
    "stage_p0.min_z_levels": 5,
    "method_gate.require_pollination_window_complete": True,
    "method_gate.require_ovary_not_swollen": True,
    "method_gate.require_barrier_not_cover_pollinator_entry": True,
    "method_gate.require_sham_on_exposed": True,
}

CAL_A_SCHEMA = "SCH_PEDICULARIS_CAL_A_TARGET_FREEZE_V1"
CAL_A_STATUS = "PEDICULARIS_CAL_A_TARGETS_FROZEN"
CAL_B_SCHEMA = "SCH_PEDICULARIS_CAL_B_TARGET_FREEZE_V1"
CAL_B_STATUS = "PEDICULARIS_CAL_B_TARGETS_FROZEN"
CAL_C_ANALYSIS = "pedicularis_cal_c_sample_size_plan_v1"
CAL_C_STATUS = "PEDICULARIS_CAL_C_SAMPLE_SIZE_PLAN_READY"


def _load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a JSON object")
    return payload


def _valid_timestamp(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _positive_number(value: object, label: str) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(out) or out <= 0:
        raise ValueError(f"{label} must be finite and > 0")
    return out


def _positive_int(value: object, label: str) -> int:
    out = _positive_number(value, label)
    if not out.is_integer():
        raise ValueError(f"{label} must be an integer")
    return int(out)


def _context(payload: dict, label: str) -> tuple[str, str]:
    population = payload.get("population_id")
    season = payload.get("season_id")
    if not isinstance(population, str) or not population:
        raise ValueError(f"{label} population_id is missing")
    if not isinstance(season, str) or not season:
        raise ValueError(f"{label} season_id is missing")
    return population, season


def _decision_basis(receipt: dict, label: str) -> dict[str, str]:
    rows = receipt.get("decision_rows")
    if not isinstance(rows, list):
        raise ValueError(f"{label} decision_rows are missing")
    out = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError(f"{label} decision row is not an object")
        gate = row.get("gate_path")
        note = row.get("target_basis_note")
        if not isinstance(gate, str) or not gate:
            raise ValueError(f"{label} decision gate_path is missing")
        if not isinstance(note, str) or not note.strip():
            raise ValueError(f"{label} basis note is missing for {gate}")
        if gate in out:
            raise ValueError(f"{label} duplicate decision gate: {gate}")
        out[gate] = note.strip()
    return out


def _validate_target_receipt(
    receipt: dict,
    *,
    schema: str,
    status: str,
    label: str,
) -> tuple[dict[str, float], dict[str, str], tuple[str, str]]:
    if receipt.get("receipt_schema_version") != schema:
        raise ValueError(f"{label} receipt schema mismatch")
    if receipt.get("status") != status:
        raise ValueError(f"{label} receipt status is not positive")
    targets = receipt.get("targets")
    if not isinstance(targets, dict):
        raise ValueError(f"{label} targets are missing")
    normalized = {
        gate: _positive_number(value, f"{label}.{gate}")
        for gate, value in targets.items()
    }
    basis = _decision_basis(receipt, label)
    if set(normalized) != set(basis):
        raise ValueError(f"{label} target/basis gate coverage mismatch")
    return normalized, basis, _context(receipt, label)


def _validate_cal_c(plan: dict) -> tuple[dict[str, int], dict[str, str], tuple[str, str]]:
    if plan.get("analysis") != CAL_C_ANALYSIS:
        raise ValueError("CAL-C analysis id mismatch")
    if plan.get("status") != CAL_C_STATUS:
        raise ValueError("CAL-C plan status is not positive")

    sample_values = plan.get("sample_size_gate_values")
    if not isinstance(sample_values, dict):
        raise ValueError("CAL-C sample_size_gate_values are missing")
    normalized = {
        gate: _positive_int(value, f"CAL-C.{gate}")
        for gate, value in sample_values.items()
    }

    provenance = plan.get("planning_provenance")
    if not isinstance(provenance, dict):
        raise ValueError("CAL-C planning_provenance is missing")
    context = _context(provenance, "CAL-C planning provenance")
    basis_document = provenance.get("basis_document")
    if not isinstance(basis_document, str) or not basis_document.strip():
        raise ValueError("CAL-C planning basis_document is missing")

    familywise_power = plan.get("familywise_target_power")
    familywise_basis = plan.get("familywise_target_power_basis")
    if not isinstance(familywise_basis, str) or not familywise_basis.strip():
        raise ValueError("CAL-C familywise_target_power_basis is missing")

    lane_plans = plan.get("lane_plans")
    if not isinstance(lane_plans, dict):
        raise ValueError("CAL-C lane_plans are missing")

    gate_lane = {
        "stage_p0.min_plants": "P0",
        "stage_p0.min_flowers_per_level": "P0",
        "pollination_weight.min_plant_units_per_treatment": "P1",
        "pollination_weight.min_flowers_per_treatment": "P1",
        "method_gate.min_paired_plants": "G",
        "method_gate.min_flowers_per_treatment": "G",
        "predator_weight.min_paired_plants": "G",
        "predator_weight.min_flowers_per_treatment": "G",
    }

    if set(normalized) != set(gate_lane):
        raise ValueError(
            "CAL-C sample-size gate coverage mismatch: "
            f"missing={sorted(set(gate_lane) - set(normalized))}, "
            f"extra={sorted(set(normalized) - set(gate_lane))}"
        )

    basis = {}
    for gate, lane in gate_lane.items():
        row = lane_plans.get(lane)
        if not isinstance(row, dict):
            raise ValueError(f"CAL-C lane plan missing for {lane}")
        driving = row.get("driving_criteria")
        if not isinstance(driving, list) or not driving:
            raise ValueError(f"CAL-C driving criteria missing for {lane}")
        design_effect_basis = row.get("design_effect_basis")
        flowers_basis = row.get("flowers_per_plant_per_cell_basis")
        if not isinstance(design_effect_basis, str) or not design_effect_basis.strip():
            raise ValueError(f"CAL-C design-effect basis missing for {lane}")
        if not isinstance(flowers_basis, str) or not flowers_basis.strip():
            raise ValueError(f"CAL-C flowers-per-plant basis missing for {lane}")

        basis[gate] = (
            "CAL_C_SAMPLE_SIZE_PLAN: "
            f"familywise_target_power={familywise_power}; "
            f"familywise_basis={familywise_basis}; "
            f"lane={lane}; "
            f"required_plants={row.get('required_plants')}; "
            f"required_flowers_per_cell={row.get('required_flowers_per_cell')}; "
            f"driving_criteria={';'.join(str(x) for x in driving)}; "
            f"design_effect={row.get('design_effect')}; "
            f"design_effect_basis={design_effect_basis}; "
            f"flowers_per_plant_per_cell={row.get('flowers_per_plant_per_cell')}; "
            f"flowers_per_plant_per_cell_basis={flowers_basis}; "
            f"basis_document={basis_document}"
        )

    return normalized, basis, context


def _validate_assembly_config(config: dict) -> tuple[str, str]:
    if config.get("receipt_schema_version") != ASSEMBLY_SCHEMA:
        raise ValueError("F0 assembly schema mismatch")
    if config.get("status") != ASSEMBLY_INPUT_STATUS:
        raise ValueError("F0 assembly input status is not positive")
    if config.get("frozen_before_confirmatory_data") is not True:
        raise ValueError("F0 assembly must be frozen before confirmatory data")
    if not _valid_timestamp(config.get("frozen_at_utc")):
        raise ValueError("F0 assembly frozen_at_utc must be timezone-aware")
    basis_document = config.get("basis_document")
    if not isinstance(basis_document, str) or not basis_document.strip():
        raise ValueError("F0 assembly basis_document is missing")
    return _context(config, "F0 assembly config")


def _set_gate(config: dict, gate_path: str, value: object) -> None:
    section, field = gate_path.split(".", 1)
    block = config.get(section)
    if not isinstance(block, dict):
        raise ValueError(f"config section missing: {section}")
    if field not in block:
        raise ValueError(f"config gate missing: {gate_path}")
    block[field] = value


def assemble(
    *,
    cal_a_receipt: dict,
    cal_b_receipt: dict,
    cal_c_plan: dict,
    p1_design_receipt: dict,
    assembly_config: dict,
    templates: dict[str, dict],
) -> tuple[dict[str, dict], dict]:
    cal_a_values, cal_a_basis, cal_a_context = _validate_target_receipt(
        cal_a_receipt,
        schema=CAL_A_SCHEMA,
        status=CAL_A_STATUS,
        label="CAL-A",
    )
    cal_b_values, cal_b_basis, cal_b_context = _validate_target_receipt(
        cal_b_receipt,
        schema=CAL_B_SCHEMA,
        status=CAL_B_STATUS,
        label="CAL-B",
    )
    cal_c_values, cal_c_basis, cal_c_context = _validate_cal_c(cal_c_plan)
    p1_design = validate_p1_design(p1_design_receipt)
    p1_design_context = (
        p1_design["population_id"],
        p1_design["season_id"],
    )
    assembly_context = _validate_assembly_config(assembly_config)

    contexts = {
        cal_a_context,
        cal_b_context,
        cal_c_context,
        p1_design_context,
        assembly_context,
    }
    if len(contexts) != 1:
        raise ValueError(
            "CAL-A, CAL-B, CAL-C, P1 design and F0 assembly contexts "
            "must match exactly"
        )
    population_id, season_id = next(iter(contexts))

    cal_c_p1_design = cal_c_plan.get("p1_design_unit")
    if cal_c_p1_design != p1_design["design_unit"]:
        raise ValueError(
            "CAL-C P1 design_unit does not match the prospectively frozen "
            "P1 design receipt"
        )
    cal_c_lane_p1 = (
        cal_c_plan.get("lane_plans", {})
        .get("P1", {})
        .get("design_unit")
    )
    if cal_c_lane_p1 != p1_design["design_unit"]:
        raise ValueError(
            "CAL-C P1 lane plan design_unit does not match the frozen "
            "P1 design receipt"
        )

    registered_basis = {
        gate: "REGISTERED_CONTRACT_VALUE: "
        + (
            "minimum five realized z levels"
            if gate == "stage_p0.min_z_levels"
            else "registered G method/natural-history boolean requirement"
        )
        for gate in REGISTERED_VALUES
    }

    sources = {
        "REGISTERED_CONTRACT": (REGISTERED_VALUES, registered_basis),
        "CAL_A": (cal_a_values, cal_a_basis),
        "CAL_B": (cal_b_values, cal_b_basis),
        "CAL_C": (cal_c_values, cal_c_basis),
    }

    all_values: dict[str, object] = {}
    all_basis: dict[str, str] = {}
    source_by_gate: dict[str, str] = {}

    for source_name, (values, basis) in sources.items():
        if set(values) != set(basis):
            raise ValueError(f"{source_name} value/basis coverage mismatch")
        overlap = set(all_values) & set(values)
        if overlap:
            raise ValueError(
                f"F0 gate source overlap detected for {sorted(overlap)}"
            )
        for gate, value in values.items():
            all_values[gate] = value
            all_basis[gate] = basis[gate]
            source_by_gate[gate] = source_name

    expected = {
        gate
        for lane in ("P0", "P1", "G")
        for gate in required_gate_paths(lane)
    }
    if set(all_values) != expected:
        raise ValueError(
            "F0 40-gate coverage mismatch: "
            f"missing={sorted(expected - set(all_values))}, "
            f"extra={sorted(set(all_values) - expected)}"
        )
    if len(all_values) != 40:
        raise ValueError(f"F0 must contain exactly 40 gates, found {len(all_values)}")

    outputs: dict[str, dict] = {}
    lane_status = {
        "P0": "PEDICULARIS_P0_FIELD_CONFIG_FROZEN",
        "P1": "PEDICULARIS_P1_FIELD_CONFIG_FROZEN",
        "G": "PEDICULARIS_G_FIELD_CONFIG_FROZEN",
    }

    for lane in ("P0", "P1", "G"):
        if lane not in templates or not isinstance(templates[lane], dict):
            raise ValueError(f"F0 template missing for {lane}")
        config = deepcopy(templates[lane])
        lane_gates = required_gate_paths(lane)

        for gate in lane_gates:
            _set_gate(config, gate, all_values[gate])

        config["prospective_freeze"] = {
            "schema": FREEZE_SCHEMA,
            "status": FREEZE_STATUS,
            "lane": lane,
            "population_id": population_id,
            "season_id": season_id,
            "frozen_before_confirmatory_data": True,
            "frozen_at_utc": assembly_config["frozen_at_utc"],
            "basis_document": assembly_config["basis_document"],
            "threshold_basis": {
                gate: (
                    f"{source_by_gate[gate]}: {all_basis[gate]}"
                )
                for gate in lane_gates
            },
        }
        if lane == "P1":
            config["pollination_design"] = deepcopy(p1_design)
        config["status"] = lane_status[lane]

        freeze_receipt = validate_prospective_freeze(config, lane)
        if freeze_receipt["status"] != FREEZE_STATUS:
            raise ValueError(f"assembled {lane} config did not pass freeze validation")
        outputs[lane] = config

    source_counts = Counter(source_by_gate.values())
    expected_counts = {
        "REGISTERED_CONTRACT": 5,
        "CAL_A": 20,
        "CAL_B": 7,
        "CAL_C": 8,
    }
    if dict(source_counts) != expected_counts:
        raise ValueError(
            f"F0 source counts mismatch: {dict(source_counts)}"
        )

    receipt = {
        "receipt_schema_version": ASSEMBLY_SCHEMA,
        "analysis": "pedicularis_f0_config_assembly",
        "population_id": population_id,
        "season_id": season_id,
        "n_gate_values": len(all_values),
        "source_counts": expected_counts,
        "lane_gate_counts": {
            lane: len(required_gate_paths(lane))
            for lane in ("P0", "P1", "G")
        },
        "gate_sources": dict(sorted(source_by_gate.items())),
        "p1_design_unit": p1_design["design_unit"],
        "p1_estimand_family": p1_design["estimand_family"],
        "p1_design_basis_document": p1_design["basis_document"],
        "assembled_config_status": {
            lane: outputs[lane]["status"]
            for lane in ("P0", "P1", "G")
        },
        "status": ASSEMBLY_STATUS,
        "unlocked_next_step": (
            "collect same-context confirmatory P0/P1/G data using these frozen configs"
        ),
        "claim_ceiling": [
            "decision_rule_assembly_only",
            "does_not_generate_empirical_validation",
            "does_not_use_confirmatory_outcomes",
            "all_40_gate_values_have_explicit_source_provenance",
        ],
    }
    return outputs, receipt


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Assemble the 40-field Pedicularis F0 P0/P1/G configs from registered "
            "contract values plus positive CAL-A, CAL-B and CAL-C receipts"
        )
    )
    parser.add_argument("cal_a_receipt", type=Path)
    parser.add_argument("cal_b_receipt", type=Path)
    parser.add_argument("cal_c_plan", type=Path)
    parser.add_argument("p1_design_receipt", type=Path)
    parser.add_argument("assembly_config", type=Path)
    parser.add_argument("--p0-template", type=Path, default=DEFAULT_TEMPLATES["P0"])
    parser.add_argument("--p1-template", type=Path, default=DEFAULT_TEMPLATES["P1"])
    parser.add_argument("--g-template", type=Path, default=DEFAULT_TEMPLATES["G"])
    parser.add_argument("--p0-out", type=Path, required=True)
    parser.add_argument("--p1-out", type=Path, required=True)
    parser.add_argument("--g-out", type=Path, required=True)
    parser.add_argument("--receipt-out", type=Path, required=True)
    args = parser.parse_args()

    outputs, receipt = assemble(
        cal_a_receipt=_load_json(args.cal_a_receipt),
        cal_b_receipt=_load_json(args.cal_b_receipt),
        cal_c_plan=_load_json(args.cal_c_plan),
        p1_design_receipt=_load_json(args.p1_design_receipt),
        assembly_config=_load_json(args.assembly_config),
        templates={
            "P0": _load_json(args.p0_template),
            "P1": _load_json(args.p1_template),
            "G": _load_json(args.g_template),
        },
    )
    _write_json(args.p0_out, outputs["P0"])
    _write_json(args.p1_out, outputs["P1"])
    _write_json(args.g_out, outputs["G"])
    _write_json(args.receipt_out, receipt)
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
