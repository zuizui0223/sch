#!/usr/bin/env python3
"""Download and fingerprint *actual* public individual-level Ipomopsis data.

A discovery-only raw-data ingress step. It deliberately prints NO scientific
hypothesis test, selection coefficient, newly fitted effect, or claims about
SCH loss. The next scientific step must read column definitions before
declaring a unit/fitness estimand.

Source: Campbell, Bischoff, Raguso, Briggs & Sosenski 2021 Dryad dataset,
https://doi.org/10.7280/D1KM49 ; archived Zenodo record 5083399.
Expected checksums and file sizes come from Zenodo's archived record.
Any disagreement FAILS rather than continuing with a mutable file.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
from collections import Counter
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

RECORD = 5083399
DOI = "10.7280/D1KM49"
FILES = {
    "ReadMe_Selection_by_pollinators_and_predators.csv": "e681a5a0885271c4797730b5a30574d8",
    "Selection_by_pollinators_and_predators.csv": "12ed3dbe6d269c5f808f9c6b230d468c",
}
MAX_DOWNLOAD = 256 * 1024
MISSING = {"", ".", "NA", "NaN", "nan", "N/A", "null"}
USER_AGENT = "SCH-public-data-raw-ingress/1.0 (citable Dryad/Zenodo open research)"


def source_urls(filename: str) -> tuple[str, ...]:
    if filename not in FILES:
        raise ValueError("filename outside pinned public primary-data receipt")
    return (
        f"https://zenodo.org/api/records/{RECORD}/files/{filename}/content",
        f"https://zenodo.org/records/{RECORD}/files/{filename}?download=1",
        f"https://zenodo.org/records/{RECORD}/files/{filename}",
    )


def verified_bytes(raw: bytes, filename: str) -> bytes:
    if filename not in FILES:
        raise ValueError("unregistered source filename")
    if len(raw) == 0 or len(raw) > MAX_DOWNLOAD:
        raise ValueError("source file missing or unexpectedly large")
    digest = hashlib.md5(raw).hexdigest()  # archival identity only, not security
    if digest != FILES[filename]:
        raise ValueError(f"source DOI archive checksum mismatch for {filename}: {digest}")
    return raw


def acquire(filename: str, timeout: int = 25) -> tuple[bytes, str]:
    failures = []
    for url in source_urls(filename):
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT, "Accept":"text/csv,*/*"})
            with urlopen(request, timeout=timeout) as response:
                raw = response.read(MAX_DOWNLOAD + 1)
            return verified_bytes(raw, filename), url
        except (ValueError, TimeoutError, HTTPError, URLError) as exc:
            failures.append(f"{url}: {type(exc).__name__}: {exc}")
    raise ConnectionError("Cannot recover the required exact archive bytes:\n"
                          +"\n".join(failures))


def is_numeric(values: list[str]) -> bool:
    if not values:
        return False
    try:
        return all(math.isfinite(float(x)) for x in values)
    except (ValueError, OverflowError):
        return False


def schema_report(raw: bytes, readme: bytes) -> dict:
    text = raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)):
        raise ValueError("source has missing or duplicated column headings")
    rows = list(reader)
    if not rows:
        raise ValueError("source has no plant rows")
    if len(rows)>100_000:
        raise ValueError("unexpected row population: check raw original")
    if any(None in row for row in rows):
        raise ValueError("source CSV record wider than stated header")
    per = []
    for col in reader.fieldnames:
        x = [r.get(col, "") or "" for r in rows]
        nonmissing = [v for v in x if v.strip() not in MISSING]
        counts = Counter(nonmissing)
        numeric = is_numeric(nonmissing)
        item = {
            "column": col,
            "not_missing": len(nonmissing),
            "missing": len(rows)-len(nonmissing),
            "distinct_nonmissing": len(counts),
            "is_numeric_coercible": numeric,
        }
        if numeric:
            v = [float(z) for z in nonmissing]
            item.update({"min":min(v), "max":max(v),
                         "n_zero":sum(z==0 for z in v),
                         "n_negative":sum(z<0 for z in v)})
        elif len(counts)<=15:
            item["categorical_distribution"] = dict(sorted(counts.items()))
        else:
            item["sample_5_distinct_labels"] = sorted(counts)[:5]
        per.append(item)
    return {
        "status":"REAL_DATA_INGRESS_SCHEMA_ONLY_NO_BIOLOGICAL_INFERENCE",
        "data_doi": DOI,
        "archive_record": RECORD,
        "expected_data_md5": FILES["Selection_by_pollinators_and_predators.csv"],
        "expected_readme_md5": FILES["ReadMe_Selection_by_pollinators_and_predators.csv"],
        "n_original_data_rows":len(rows),
        "n_columns":len(reader.fieldnames),
        "columns":per,
        "original_variable_dictionary_utf8":readme.decode("utf-8-sig", errors="replace"),
        "positive_scientific_effect_estimated":False,
        "sample_weighting_or_cluster_independence_assumed":False,
        "primary_future_question":(
            "Does individual-level coupling between initiation and predator "
            "escape explain changes in realized floral selection, after "
            "study-site and taxon/genotype structure are respected?"
        ),
        "next_gate":"SCHEMA_DICTIONARY_REVIEW_AND_FITNESS_UNIT_ADJUDICATION",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--outdir", type=Path,
                    default=Path("artifacts/ipomopsis_original_ingress"))
    args = ap.parse_args()
    output = args.outdir
    output.mkdir(parents=True, exist_ok=True)
    source_urls_used = {}
    files = {}
    for name in FILES:
        raw, url = acquire(name)
        path = output / name
        path.write_bytes(raw)
        source_urls_used[name] = url
        files[name] = raw
    report = schema_report(
        files["Selection_by_pollinators_and_predators.csv"],
        files["ReadMe_Selection_by_pollinators_and_predators.csv"],
    )
    report["archive_file_urls_used"] = source_urls_used
    report_file = output / "schema_and_md5_verified.json"
    report_file.write_text(json.dumps(report, sort_keys=True, indent=2)
                           + "\n", encoding="utf-8")
    print("BEGIN_SCH_REAL_IPOMOPSIS_SOURCE_RECEIPT")
    print(report_file.read_text(encoding="utf-8"))
    print("END_SCH_REAL_IPOMOPSIS_SOURCE_RECEIPT")


if __name__ == "__main__":
    main()
