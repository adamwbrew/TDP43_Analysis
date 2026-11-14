#!/usr/bin/env python3
"""Read-only, streaming CSV audit; never infer specimen identity from file names.

Example:
    python scripts/inventory_data.py --data-dir '/path/to/Initial Data' \
        --reference-dir '/path/to/historical/Initial Data' \
        --reference-dir '/path/to/historical/entire Chat dataset'

Source files are opened read-only. SHA-256 establishes byte identity. Row
signatures establish agreement of exported text values, not biological identity.
This inventory intentionally cannot approve sample assignments or spatial data.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


NULL_TOKENS = {"", "nan", "na", "n/a", "null", "none"}
CATEGORICAL = {
    "Image Location", "Analysis Region", "Algorithm Name", "Object Type",
    "PLA - TRITC_E1 present", "ChAt-50 - FITC_E1 present",
}
BBOX_FIELDS = ("XMin", "XMax", "YMin", "YMax")
PLA_LABEL = "PLA - TRITC_E1"
CHAT_LABEL = "ChAt-50 - FITC_E1"
METHOD_VERSION = "1.1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not fieldnames:
        fieldnames = list(rows[0]) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def signature(values: list[str]) -> bytes:
    # Length prefixes prevent embedded separators from making distinct rows equal.
    digest = hashlib.blake2b(digest_size=16)
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.digest()


def empty_profile() -> dict:
    return {"missing_count": 0, "numeric_count": 0, "non_numeric_count": 0,
            "non_finite_count": 0, "integer_valued_count": 0, "zero_count": 0,
            "negative_count": 0, "numeric_min": None, "numeric_max": None,
            "examples": [], "categorical_counts": Counter()}


def profile_value(profile: dict, value: str, categorical: bool):
    if value.strip().lower() in NULL_TOKENS:
        profile["missing_count"] += 1
        return
    if categorical:
        profile["categorical_counts"][value] += 1
    if len(profile["examples"]) < 6 and value not in profile["examples"]:
        profile["examples"].append(value)
    try:
        number = float(value)
    except ValueError:
        profile["non_numeric_count"] += 1
        return
    if not math.isfinite(number):
        profile["non_finite_count"] += 1
        return
    profile["numeric_count"] += 1
    profile["integer_valued_count"] += int(number.is_integer())
    profile["zero_count"] += int(number == 0)
    profile["negative_count"] += int(number < 0)
    if profile["numeric_min"] is None or number < profile["numeric_min"]:
        profile["numeric_min"] = number
    if profile["numeric_max"] is None or number > profile["numeric_max"]:
        profile["numeric_max"] = number


def infer_type(profile: dict) -> str:
    if profile["non_finite_count"]:
        return "numeric_with_nonfinite" if not profile["non_numeric_count"] else "mixed"
    if profile["numeric_count"] and profile["non_numeric_count"]:
        return "mixed"
    if profile["non_numeric_count"]:
        return "string"
    if not profile["numeric_count"]:
        return "empty"
    return "integer_valued" if profile["numeric_count"] == profile["integer_valued_count"] else "numeric"


def audit_csv(path: Path, file_id: str, keep_signatures: bool) -> tuple[dict, set, set]:
    profiles = {}
    row_count = malformed = invalid_bbox = missing_bbox = 0
    exact_signatures, measurement_signatures, object_ids = set(), set(), set()
    duplicate_object_ids = 0
    exact_duplicate_rows = 0
    bbox_ranges = {key: [None, None] for key in BBOX_FIELDS}
    pla_count = chat_count = pla_chat_positive_count = 0
    object_types = Counter()
    regions = Counter()
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        if len(set(header)) != len(header):
            raise ValueError(f"Duplicate CSV column names: {path}")
        profiles = {name: empty_profile() for name in header}
        indices = {name: i for i, name in enumerate(header)}
        measurement_indices = [i for i, name in enumerate(header) if name not in {"Analysis Region", "Object Id"}]
        bbox_indices = [indices.get(key) for key in BBOX_FIELDS]
        for row in reader:
            row_count += 1
            if len(row) != len(header):
                malformed += 1
                continue
            for name, value in zip(header, row):
                profile_value(profiles[name], value, name in CATEGORICAL)
            object_type = row[indices["Object Type"]] if "Object Type" in indices else ""
            object_types[object_type] += 1
            region = row[indices["Analysis Region"]] if "Analysis Region" in indices else ""
            regions[region] += 1
            if "Object Id" in indices:
                object_id = row[indices["Object Id"]]
                duplicate_object_ids += int(object_id in object_ids)
                object_ids.add(object_id)
            if object_type == PLA_LABEL:
                pla_count += 1
                flag_index = indices.get("ChAt-50 - FITC_E1 present")
                if flag_index is not None:
                    try:
                        pla_chat_positive_count += int(float(row[flag_index]) == 1)
                    except ValueError:
                        pass
            elif object_type == CHAT_LABEL:
                chat_count += 1
            if all(index is not None for index in bbox_indices):
                try:
                    xmin, xmax, ymin, ymax = [float(row[index]) for index in bbox_indices]
                    if not all(math.isfinite(value) for value in (xmin, xmax, ymin, ymax)):
                        missing_bbox += 1
                    else:
                        invalid_bbox += int(xmax < xmin or ymax < ymin)
                        for key, value in zip(BBOX_FIELDS, (xmin, xmax, ymin, ymax)):
                            bounds = bbox_ranges[key]
                            bounds[0] = value if bounds[0] is None else min(bounds[0], value)
                            bounds[1] = value if bounds[1] is None else max(bounds[1], value)
                except ValueError:
                    missing_bbox += 1
            if keep_signatures:
                exact = signature(row)
                exact_duplicate_rows += int(exact in exact_signatures)
                exact_signatures.add(exact)
                measurement_signatures.add(signature([row[index] for index in measurement_indices]))
    result = {
        "file_id": file_id, "path": str(path.resolve()), "filename": path.name,
        "row_count": row_count, "column_count": len(header), "columns": header,
        "malformed_row_count": malformed, "column_profiles": profiles,
        "object_type_counts": dict(object_types), "analysis_region_counts": dict(regions),
        "pla_row_count_by_export_label": pla_count, "chat_row_count_by_export_label": chat_count,
        "pla_rows_with_chat_present_equal_1": pla_chat_positive_count,
        "object_id_unique_count": len(object_ids), "duplicate_object_id_occurrences": duplicate_object_ids,
        "bbox_field_ranges": bbox_ranges, "invalid_bbox_order_count": invalid_bbox,
        "missing_or_nonfinite_bbox_count": missing_bbox,
        "true_centroid_fields_present": [name for name in header if "centroid" in name.lower()],
        "exact_duplicate_row_occurrences": exact_duplicate_rows if keep_signatures else None,
        "measurement_signature_unique_count": len(measurement_signatures) if keep_signatures else None,
    }
    for profile in profiles.values():
        profile["observed_type"] = infer_type(profile)
        profile["categorical_counts"] = dict(profile["categorical_counts"])
    return result, exact_signatures, measurement_signatures


def dictionary_entry(name: str) -> tuple[str, str, str]:
    if name == "Image Location":
        return "Source image path text exported by HALO; image pixels are not included in the CSV.", "path text", "Path agreement alone does not establish acquisition/processing provenance."
    if name == "Analysis Region":
        return "Analysis-region label embedded in the export, preserved verbatim.", "label", "May suggest a sample/marker label; requires scientist confirmation for this study."
    if name == "Algorithm Name":
        return "Algorithm label/version exported by HALO.", "label", "Parameters and segmentation validation are not encoded completely."
    if name == "Object Id":
        return "Object identifier within one export.", "identifier", "Not a cross-export specimen/object correspondence key."
    if name == "Object Type":
        return "Detected-object class reported by the export.", "label", "A row is a detection, not an independent biological replicate or necessarily a cell/molecule."
    if name.endswith(" present"):
        return "Exported channel-presence indicator.", "exported indicator", "Interpretation depends on acquisition, detection and colocalization settings."
    if name in BBOX_FIELDS:
        return "Native-axis bounding-box boundary reported by the export.", "unverified coordinate units", "No centroid fields are supplied; the requested centroid definition is unresolved. Historical midpoint proxies require explicit scientific clarification before use."
    if "µm²" in name:
        return "Exported area measurement with a header-labelled unit.", "µm² (export header; calibration unverified)", "Header units do not independently validate X/Y calibration."
    if "µm" in name:
        return "Exported diameter measurement with a header-labelled unit.", "µm (export header; calibration unverified)", "Header units do not independently validate X/Y calibration."
    if name.startswith("% Area"):
        return "Exported percent-area colocalization measurement.", "% (export header)", "Algorithm denominator must be confirmed; not the requested section-normalized spatial count fraction."
    if name.startswith("Area in"):
        return "Exported colocalized area measurement.", "not explicitly stated in this header", "Do not assign calibration from related column labels."
    if name == "Average Intensity":
        return "Exported average object intensity.", "not documented", "Do not compare as calibrated fluorescence without acquisition/processing information."
    return "Exported measurement; see source technical specification.", "not documented", "Scientific meaning needs confirmation."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", required=True, type=Path)
    parser.add_argument("--reference-dir", action="append", type=Path, default=[])
    parser.add_argument("--output-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--skip-row-overlap", action="store_true", help="Skip in-memory row-signature comparisons.")
    args = parser.parse_args()
    data_dir, root = args.data_dir.resolve(), args.output_root.resolve()
    if not data_dir.is_dir():
        parser.error(f"Missing data directory: {data_dir}")
    for directory in args.reference_dir:
        if not directory.is_dir():
            parser.error(f"Missing reference directory: {directory}")
    source_files = sorted(path for path in data_dir.rglob("*") if path.is_file())
    if not source_files:
        parser.error(f"No files found in data directory: {data_dir}")
    reference_files = sorted({path.resolve() for directory in args.reference_dir for path in directory.rglob("*") if path.is_file()})
    inventory_dir = root / "outputs" / "inventory"
    inventory_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir = root / "metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    reference_manifest = []
    refs_by_hash = {}
    for path in reference_files:
        if path.suffix.lower() != ".csv":
            continue
        record = {"path": str(path), "filename": path.name, "size_bytes": path.stat().st_size, "sha256": sha256(path)}
        reference_manifest.append(record)
        refs_by_hash.setdefault(record["sha256"], []).append(record)
    print(f"Hashed {len(reference_manifest)} reference CSVs.", flush=True)
    manifests, audits, signatures = [], [], {}
    for number, path in enumerate(source_files, 1):
        file_id = f"input_{number:03d}"
        digest = sha256(path)
        match = re.search(r"_job(\d+)", path.name)
        manifest = {"file_id": file_id, "source_path": str(path), "relative_path": str(path.relative_to(data_dir)),
                    "format": path.suffix.lower().lstrip("."), "size_bytes": path.stat().st_size,
                    "sha256": digest, "job_token_from_filename": match.group(1) if match else "",
                    "historical_byte_identical_copy_count": len(refs_by_hash.get(digest, [])),
                    "historical_byte_identical_paths": json.dumps([record["path"] for record in refs_by_hash.get(digest, [])]),
                    "sample_assignment_status": "unconfirmed_for_new_project"}
        if path.suffix.lower() == ".csv":
            audit, exact, measurement = audit_csv(path, file_id, not args.skip_row_overlap)
            if sha256(path) != digest:
                raise RuntimeError(f"Source changed during audit; outputs are not valid: {path}")
            audit["sha256"] = digest
            audit["source_sha256_unchanged_during_audit"] = True
            audits.append(audit)
            signatures[file_id] = (exact, measurement)
            manifest.update({"row_count": audit["row_count"], "column_count": audit["column_count"],
                             "exported_analysis_regions": json.dumps(list(audit["analysis_region_counts"])),
                             "true_centroid_fields_present": json.dumps(audit["true_centroid_fields_present"])})
            print(f"Audited {file_id}: {audit['row_count']:,} rows ({path.name}).", flush=True)
        else:
            manifest.update({"row_count": "", "column_count": "", "exported_analysis_regions": "", "true_centroid_fields_present": ""})
        manifests.append(manifest)
    write_csv(metadata_dir / "input_manifest.csv", manifests)
    write_json(metadata_dir / "input_manifest.json", manifests)
    write_csv(inventory_dir / "reference_manifest.csv", reference_manifest)
    overlap = []
    if not args.skip_row_overlap:
        for i, left in enumerate(audits):
            for right in audits[i + 1:]:
                left_exact, left_measure = signatures[left["file_id"]]
                right_exact, right_measure = signatures[right["file_id"]]
                same_measure = len(left_measure & right_measure)
                overlap.append({"left_file_id": left["file_id"], "right_file_id": right["file_id"],
                                "byte_identical": left["sha256"] == right["sha256"],
                                "exact_exported_row_signatures_shared": len(left_exact & right_exact),
                                "measurement_signatures_shared_excluding_region_and_object_id": same_measure,
                                "left_unique_measurement_signature_count": len(left_measure),
                                "right_unique_measurement_signature_count": len(right_measure),
                                "left_signature_shared_fraction": same_measure / len(left_measure) if left_measure else None,
                                "right_signature_shared_fraction": same_measure / len(right_measure) if right_measure else None,
                                "interpretation": "Exact exported-value agreement; not proof of biological identity or approved sample correspondence."})
    write_csv(inventory_dir / "within_input_overlap.csv", overlap,
              list(overlap[0]) if overlap else ["left_file_id", "right_file_id", "measurement_signatures_shared_excluding_region_and_object_id"])
    column_rows = []
    sample_rows = []
    for audit in audits:
        for column, profile in audit["column_profiles"].items():
            column_rows.append({"file_id": audit["file_id"], "column": column,
                                **{key: json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict)) else value
                                   for key, value in profile.items()}})
        for region, count in audit["analysis_region_counts"].items():
            sample_rows.append({"file_id": audit["file_id"], "exported_analysis_region": region,
                                "rows_in_export_region": count, "animal_id": "", "condition": "",
                                "pla_arm": "", "physical_section_id": "", "roi_id": "",
                                "biological_replicate_id": "", "technical_repeat_of": "",
                                "include_in_primary_analysis": "pending",
                                "approved_alignment_id": "", "aligned_centroid_source": "",
                                "tissue_mask_source": "", "coordinate_units": "unverified",
                                "assignment_status": "unconfirmed_for_new_project",
                                "evidence": "Analysis Region text observed in CSV; no transfer of historical assignments."})
    write_csv(inventory_dir / "column_profiles.csv", column_rows)
    # Generated suggestions are separate from human-curated assignments, so reruns
    # cannot erase scientist approvals in an existing sample_metadata.csv.
    sample_path = metadata_dir / "sample_metadata.csv"
    if sample_path.exists():
        write_csv(inventory_dir / "sample_metadata_observed.csv", sample_rows)
    else:
        write_csv(sample_path, sample_rows)
    dictionary = []
    for column in dict.fromkeys(column for audit in audits for column in audit["columns"]):
        description, units, caution = dictionary_entry(column)
        profiles = [audit["column_profiles"][column] for audit in audits if column in audit["column_profiles"]]
        minima = [profile["numeric_min"] for profile in profiles if profile["numeric_min"] is not None]
        maxima = [profile["numeric_max"] for profile in profiles if profile["numeric_max"] is not None]
        dictionary.append({"column": column, "description": description, "units_or_representation": units,
                           "observed_types": ";".join(sorted({profile["observed_type"] for profile in profiles})),
                           "missing_count_all_files": sum(profile["missing_count"] for profile in profiles),
                           "nonfinite_count_all_files": sum(profile["non_finite_count"] for profile in profiles),
                           "numeric_min_all_files": min(minima) if minima else "",
                           "numeric_max_all_files": max(maxima) if maxima else "", "limitations": caution})
    write_csv(metadata_dir / "data_dictionary.csv", dictionary)
    write_json(metadata_dir / "data_dictionary.json", dictionary)
    manifest_by_id = {record["file_id"]: record for record in manifests}
    summary = {
        "method_version": METHOD_VERSION, "started_utc": started,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "data_directory": str(data_dir), "reference_directories": [str(path.resolve()) for path in args.reference_dir],
        "source_file_count": len(source_files), "source_csv_count": len(audits),
        "source_bytes": sum(record["size_bytes"] for record in manifests),
        "total_exported_rows_including_possible_repeats": sum(audit["row_count"] for audit in audits),
        "total_pla_rows_by_export_label_including_possible_repeats": sum(audit["pla_row_count_by_export_label"] for audit in audits),
        "total_chat_rows_by_export_label_including_possible_repeats": sum(audit["chat_row_count_by_export_label"] for audit in audits),
        "source_files_identical_to_historical_reference": sum(record["historical_byte_identical_copy_count"] > 0 for record in manifests),
        "all_csvs_missing_true_centroid_fields": all(not audit["true_centroid_fields_present"] for audit in audits),
        "malformed_rows": sum(audit["malformed_row_count"] for audit in audits),
        "invalid_bbox_rows": sum(audit["invalid_bbox_order_count"] for audit in audits),
        "row_overlap_audited": not args.skip_row_overlap,
        "row_signature_algorithm": "BLAKE2b-128 over length-prefixed UTF-8 exported values; possible cryptographic collision is not a biological identity test.",
        "measurement_signature_excluded_columns": ["Analysis Region", "Object Id"],
        "sample_metadata_policy": "No assignments inferred from filename tokens, embedded labels, historical findings or duplicate status; generated observations do not overwrite curated metadata.",
        "blockers": [
            "No scientist-approved mapping of these exports to the new experiment, animals, conditions, PLA arms, physical sections and repeated analyses.",
            "No centroid fields are supplied; the requested aligned-centroid definition is unresolved. Historical bounding-box midpoint proxies require explicit scientific clarification before use.",
            "No approved alignment transforms/reference anatomy, aligned tissue masks, coordinate calibration or verified common grid supplied in the inventoried data directory.",
            "Byte-identical historical copies and overlapping analyses are documented; current section mapping and ROI/rerun inclusion resolution remain needed."
        ],
        "files": [{"file_id": audit["file_id"], "filename": audit["filename"], "row_count": audit["row_count"],
                   "object_type_counts": audit["object_type_counts"], "analysis_region_counts": audit["analysis_region_counts"],
                   "pla_rows_with_chat_present_equal_1": audit["pla_rows_with_chat_present_equal_1"],
                   "historical_byte_identical_copy_count": manifest_by_id[audit["file_id"]]["historical_byte_identical_copy_count"]} for audit in audits],
    }
    write_json(inventory_dir / "file_audit.json", audits)
    write_json(inventory_dir / "summary.json", summary)
    reconciliation_failures = []
    for audit in audits:
        valid_rows = audit["row_count"] - audit["malformed_row_count"]
        if sum(audit["object_type_counts"].values()) != valid_rows:
            reconciliation_failures.append(f"{audit['file_id']}: object-type counts do not reconcile")
        for name, profile in audit["column_profiles"].items():
            parsed = sum(profile[key] for key in ("missing_count", "numeric_count", "non_numeric_count", "non_finite_count"))
            if parsed != valid_rows:
                reconciliation_failures.append(f"{audit['file_id']}: {name} profile does not reconcile")
    validation = {
        "completed_utc": summary["completed_utc"], "method_version": METHOD_VERSION,
        "status": "passed" if not reconciliation_failures else "failed",
        "source_sha256_verified_before_and_after_csv_scan": all(audit["source_sha256_unchanged_during_audit"] for audit in audits),
        "file_count": len(audits), "column_profile_count": len(column_rows),
        "profile_and_object_type_row_counts_reconcile": not reconciliation_failures,
        "failures": reconciliation_failures,
        "scope": "Input audit consistency only; does not validate biological assignments, spatial alignment, calibration or analysis readiness."
    }
    write_json(inventory_dir / "validation.json", validation)
    report = ["# Read-only input inventory", "", "This is an input audit, not a biological result.", "",
              f"- CSV files: {len(audits)}; bytes: {summary['source_bytes']:,}.",
              f"- Exported rows, including possible repeated analyses: {summary['total_exported_rows_including_possible_repeats']:,}.",
              f"- Files byte-identical to historical reference CSVs (SHA-256): {summary['source_files_identical_to_historical_reference']}/{len(audits)}.",
              "- Filenames and embedded region labels are observations, not approved new-study metadata.",
              "- Full column counts, types, missingness, categorical counts and numeric ranges are in column_profiles.csv and file_audit.json.", "",
              "| File | Job token | Exported region text | Rows | PLA-label rows | ChAT-label rows |", "|---|---|---|---:|---:|---:|"]
    for audit in audits:
        report.append(f"| {audit['file_id']} | {manifest_by_id[audit['file_id']]['job_token_from_filename']} | {'; '.join(audit['analysis_region_counts'])} | {audit['row_count']:,} | {audit['pla_row_count_by_export_label']:,} | {audit['chat_row_count_by_export_label']:,} |")
    report += ["", "## What the evidence demonstrates", "", "SHA-256 agreement establishes byte-identical copies of the files in the reference locations. It does not establish that the new experiment has the same scientific assignments or that the instructions authorize reusing those assignments. Embedded label text and object class labels are preserved without upgrading them to validated biological identity.", "", "Within-input overlap compares full exported rows and, separately, all exported values except Analysis Region and Object Id. Shared measurement signatures show exact agreement of exported image path, algorithm, type, measurements and boxes. Repeated measurement values can occur; these signatures are evidence of overlap, not a validated biological-object matching procedure. Fractions use distinct signatures, not row multiplicities. Do not pool candidate reruns as independent sections/animals.", "", "## Analysis blockers", ""]
    report += [f"- {blocker}" for blocker in summary["blockers"]]
    report += ["", "## Provenance and reruns", "", "Source files were opened read-only. No source files were moved or edited. The command records complete SHA-256 hashes; row parsing uses Python's CSV reader with UTF-8 BOM handling. Numeric ranges describe exported values; header units are not calibration validation. UTC timestamps are execution provenance. Existing metadata/sample_metadata.csv is preserved on rerun; refreshed observed suggestions are written to outputs/inventory/sample_metadata_observed.csv.", ""]
    (inventory_dir / "report.md").write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({key: value for key, value in summary.items() if key != "files"}, indent=2), flush=True)
    return int(bool(reconciliation_failures))


if __name__ == "__main__":
    raise SystemExit(main())
