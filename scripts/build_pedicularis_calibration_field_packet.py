from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts import validate_pedicularis_cohort_registry as cohort
from scripts.build_pedicularis_calibration_package import (
    _write_json,
    build_package,
)
from scripts.materialize_pedicularis_g_field_rows import (
    PROXY_REQUIRED_FIELDS,
    _read as read_g_table,
    _write_csv as write_g_csv,
    build as materialize_g,
)


def _registry_by_flower(
    rows: list[dict[str, str]],
) -> dict[str, dict[str, str]]:
    return {
        row["flower_id"]: row
        for row in rows
    }


def _validate_proxy_registry(
    *,
    registry_rows: list[dict[str, str]],
    proxy_path: Path,
) -> dict:
    registry = _registry_by_flower(registry_rows)
    proxy_rows = read_g_table(
        proxy_path,
        PROXY_REQUIRED_FIELDS,
        label="pollen proxy",
    )

    proxy_ids = {
        row["proxy_flower_id"]
        for row in proxy_rows
    }

    missing = sorted(proxy_ids - set(registry))
    if missing:
        raise ValueError(
            "G pollen proxy flower IDs missing from cohort registry: "
            + ", ".join(missing)
        )

    wrong_role = sorted(
        proxy_id
        for proxy_id in proxy_ids
        if registry[proxy_id]["cohort_role"] != "CAL_B_G"
    )
    if wrong_role:
        raise ValueError(
            "G pollen proxy flowers must be registered as CAL_B_G: "
            + ", ".join(wrong_role)
        )

    ineligible = sorted(
        proxy_id
        for proxy_id in proxy_ids
        if (
            registry[proxy_id]["threshold_basis_eligible"] != "YES"
            or registry[proxy_id]["confirmatory_eligible"] != "NO"
        )
    )
    if ineligible:
        raise ValueError(
            "G pollen proxy flowers must be threshold-basis-only: "
            + ", ".join(ineligible)
        )

    mismatch = []
    for row in proxy_rows:
        registered = registry[row["proxy_flower_id"]]
        for field in (
            "population_id",
            "season_id",
            "plant_id",
        ):
            if registered[field] != row[field]:
                mismatch.append(
                    f"{row['proxy_flower_id']}:{field}"
                )
    if mismatch:
        raise ValueError(
            "G pollen proxy registry/data identity mismatch: "
            + ", ".join(sorted(mismatch))
        )

    return {
        "n_proxy_rows": len(proxy_rows),
        "n_proxy_flowers": len(proxy_ids),
        "proxy_flower_ids": sorted(proxy_ids),
        "all_proxy_flowers_registered_as_CAL_B_G": True,
        "all_proxy_flowers_threshold_basis_only": True,
    }


def build_field_packet(
    *,
    registry_path: Path,
    repeatability_path: Path,
    p0_path: Path,
    p1_path: Path,
    g_focal_path: Path,
    g_proxy_path: Path,
    g_materialized_out: Path,
) -> tuple[dict, dict, dict, dict]:
    registry_rows = cohort._read(registry_path)
    cohort_receipt = cohort.validate(registry_rows)

    proxy_registration = _validate_proxy_registry(
        registry_rows=registry_rows,
        proxy_path=g_proxy_path,
    )

    g_rows, g_materialization_receipt = materialize_g(
        g_focal_path,
        g_proxy_path,
    )
    write_g_csv(
        g_materialized_out,
        g_rows,
    )

    repeatability_summary, calibration_summary, package_receipt = (
        build_package(
            registry_path=registry_path,
            repeatability_path=repeatability_path,
            p0_path=p0_path,
            p1_path=p1_path,
            g_path=g_materialized_out,
        )
    )

    if (
        package_receipt["population_id"],
        package_receipt["season_id"],
    ) != (
        g_materialization_receipt["population_id"],
        g_materialization_receipt["season_id"],
    ):
        raise ValueError(
            "G materialization context differs from calibration package"
        )

    field_receipt = {
        "receipt_schema_version": (
            "SCH_PEDICULARIS_CALIBRATION_FIELD_PACKET_V1"
        ),
        "analysis": "pedicularis_calibration_field_packet",
        "population_id": package_receipt["population_id"],
        "season_id": package_receipt["season_id"],
        "cohort_registry_status": cohort_receipt["status"],
        "g_proxy_registration": proxy_registration,
        "g_materialization_status": (
            g_materialization_receipt["status"]
        ),
        "calibration_package_status": package_receipt["status"],
        "n_g_endpoint_rows": g_materialization_receipt[
            "n_focal_endpoint_rows"
        ],
        "n_g_pollen_proxy_rows": g_materialization_receipt[
            "n_pollen_proxy_rows"
        ],
        "status": (
            "PEDICULARIS_CALIBRATION_FIELD_PACKET_"
            "READY_FOR_TARGET_FREEZE"
        ),
        "unlocked_next_steps": package_receipt[
            "unlocked_next_steps"
        ],
        "claim_ceiling": [
            "field_packet_integrity_and_materialization_only",
            "pollen_proxy_flowers_are_calibration_only",
            "does_not_select_thresholds",
            "does_not_validate_P0_P1_or_G",
        ],
    }

    return (
        repeatability_summary,
        calibration_summary,
        g_materialization_receipt,
        field_receipt,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build the complete Pedicularis calibration field packet "
            "from registry, repeatability, P0/P1, G endpoint flowers, "
            "and matched destructive G pollen proxies"
        )
    )
    parser.add_argument("cohort_registry", type=Path)
    parser.add_argument("repeatability_csv", type=Path)
    parser.add_argument("p0_csv", type=Path)
    parser.add_argument("p1_csv", type=Path)
    parser.add_argument("g_focal_csv", type=Path)
    parser.add_argument("g_pollen_proxy_csv", type=Path)
    parser.add_argument(
        "--g-materialized-out",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--repeatability-out",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--calibration-out",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--g-materialization-receipt-out",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--field-packet-receipt-out",
        type=Path,
        required=True,
    )
    args = parser.parse_args()

    (
        repeatability_summary,
        calibration_summary,
        g_materialization_receipt,
        field_receipt,
    ) = build_field_packet(
        registry_path=args.cohort_registry,
        repeatability_path=args.repeatability_csv,
        p0_path=args.p0_csv,
        p1_path=args.p1_csv,
        g_focal_path=args.g_focal_csv,
        g_proxy_path=args.g_pollen_proxy_csv,
        g_materialized_out=args.g_materialized_out,
    )

    _write_json(
        args.repeatability_out,
        repeatability_summary,
    )
    _write_json(
        args.calibration_out,
        calibration_summary,
    )
    _write_json(
        args.g_materialization_receipt_out,
        g_materialization_receipt,
    )
    _write_json(
        args.field_packet_receipt_out,
        field_receipt,
    )

    print(
        json.dumps(
            field_receipt,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
