"""Authorized exploratory object-support maps, separate from strict PDF results.

Object occupancy is data-dependent support, never a tissue mask. A ChAT-only
bin contributes a PLA count of zero; a bin with no known objects contributes no
section. Every object is counted from the selected raw CSV with fixed supplied
transforms and an explicit bounding-box midpoint proxy.
"""
import csv
import gzip
import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from .core import FixedTransform, assign_centroid_bins
from .manifest import display_directions_from_manifest, grid_from_manifest, sha256_file


PLA_CLASS = "PLA - TRITC_E1"
CHAT_CLASS = "ChAt-50 - FITC_E1"
LIMITATIONS = [
    "Exploratory bounding-box midpoints are not measured object centroids.",
    "Observed-object support is data-dependent and is not verified tissue coverage, a tissue mask, or a full-bin containment test.",
    "A section with no exported PLA or ChAT in a bin is excluded; tissue with no detected objects may therefore be omitted.",
    "Partial edge bins and holes have unknown coverage; object support can bias condition means and differences.",
    "Counts are unnormalized descriptive section means, with no smoothing, interpolation or inferential tests.",
    "Fixed alignment is preserved; this analysis does not validate anatomical correspondence or physical calibration.",
    "The strict PDF results remain pending existing masks and an applicable centroid definition.",
]


def _json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def _matrix(values):
    array = np.asarray(values)
    if array.dtype == np.bool_ or np.issubdtype(array.dtype, np.integer):
        return array.tolist()
    return [[float(v) if np.isfinite(v) else None for v in row] for row in array]


def summarize_observed_sections(sections, grid):
    """Equal-section raw PLA means among sections having any known object."""
    if len({s["section_id"] for s in sections}) != len(sections):
        raise ValueError("Repeated exploratory section IDs")
    physical_keys = [(s["physical_section_id"], s["pla_type"]) for s in sections]
    if len(set(physical_keys)) != len(physical_keys):
        raise ValueError("Repeated physical section/PLA type cannot be extra replication")
    for section in sections:
        if section["pla_type"] not in ("HK1", "PFKP") or section["condition"] not in ("Homecage", "Running"):
            raise ValueError("Explicit separate arm and condition required")
        for key in ("pla_counts", "chat_counts"):
            count = np.asarray(section[key])
            if count.shape != grid.shape or not np.isfinite(count).all() or (count < 0).any() or not np.equal(count, np.floor(count)).all():
                raise ValueError("Exploratory counts must be finite nonnegative integer matrices on the shared grid")
    results = {}
    for arm in ("HK1", "PFKP"):
        means, ns = {}, {}
        part = [s for s in sections if s["pla_type"] == arm]
        for condition in ("Homecage", "Running"):
            n = np.zeros(grid.shape, dtype=np.int64)
            total = np.zeros(grid.shape, dtype=np.int64)
            for section in part:
                if section["condition"] != condition:
                    continue
                pla, chat = np.asarray(section["pla_counts"]), np.asarray(section["chat_counts"])
                observed = (pla + chat) > 0
                n += observed
                total += np.where(observed, pla, 0)
            means[condition] = np.divide(total, n, out=np.full(grid.shape, np.nan), where=n > 0)
            ns[condition] = n
        displayable = (ns["Homecage"] > 0) & (ns["Running"] > 0)
        results[arm] = {"homecage_mean": means["Homecage"], "running_mean": means["Running"],
                       "difference": np.where(displayable, means["Running"] - means["Homecage"], np.nan),
                       "homecage_n": ns["Homecage"], "running_n": ns["Running"], "displayable": displayable,
                       "section_ids": [s["section_id"] for s in part]}
    return results


def count_raw_section(specification, grid, base_dir, pla_provenance_path=None):
    """Count every known raw object, preserving full selected PLA provenance."""
    source = specification["source"]
    source_path = Path(source["path"])
    if not source_path.is_absolute():
        source_path = Path(base_dir) / source_path
    if sha256_file(source_path) != source["sha256"]:
        raise ValueError("Raw source SHA-256 mismatch: " + str(source_path))
    transform = FixedTransform(specification["transform"]["matrix"])
    if specification["transform"].get("accepted") is not True:
        raise ValueError("Exploratory run requires the documented unchanged fixed transform")
    object_id_column = source["object_id_column"]
    counts = {PLA_CLASS: np.zeros(grid.shape, dtype=np.int64), CHAT_CLASS: np.zeros(grid.shape, dtype=np.int64)}
    totals = {PLA_CLASS: 0, CHAT_CLASS: 0}
    outside = {PLA_CLASS: 0, CHAT_CLASS: 0}
    seen, buffer, source_rows = set(), [], 0
    output_handle = (gzip.open(pla_provenance_path, "wt", encoding="utf-8", newline="")
                     if pla_provenance_path is not None else None)
    writer = csv.writer(output_handle) if output_handle is not None else None
    if writer:
        writer.writerow(["source_file_id", "source_row_number", "object_id", "x_bbox_midpoint_native", "y_bbox_midpoint_native",
                         "x_fixed_aligned", "y_fixed_aligned"])

    def consume():
        if not buffer:
            return
        native = np.asarray([row[3] for row in buffer], dtype=float)
        aligned = transform.points(native)
        if not np.isfinite(aligned).all():
            raise ValueError("Fixed transformation generated nonfinite coordinates")
        bins, inside = assign_centroid_bins(aligned, grid)
        for object_type in (PLA_CLASS, CHAT_CLASS):
            selected = np.asarray([row[2] == object_type for row in buffer], dtype=bool)
            eligible = selected & inside
            np.add.at(counts[object_type], (bins[eligible, 0], bins[eligible, 1]), 1)
            outside[object_type] += int((selected & ~inside).sum())
        if writer:
            for record, xy in zip(buffer, aligned):
                row_number, oid, object_type, midpoint = record
                if object_type == PLA_CLASS:
                    writer.writerow([source["source_file_id"], row_number, oid, *midpoint, *xy])
        buffer.clear()

    try:
        with source_path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            required = {object_id_column, "Object Type", "XMin", "XMax", "YMin", "YMax"}
            if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)) or not required.issubset(reader.fieldnames):
                raise ValueError("Raw source lacks exact required fields or has duplicate headers")
            for row_number, row in enumerate(reader, start=2):
                if None in row or any(value is None for value in row.values()):
                    raise ValueError("Malformed raw CSV row %d" % row_number)
                oid, object_type = row[object_id_column], row["Object Type"]
                if not oid.strip() or oid in seen:
                    raise ValueError("Missing/repeated object ID at raw source row %d" % row_number)
                seen.add(oid)
                if object_type not in counts:
                    raise ValueError("Unknown raw Object Type at source row %d: %s" % (row_number, object_type))
                xmin, xmax, ymin, ymax = [float(row[key]) for key in ("XMin", "XMax", "YMin", "YMax")]
                if not np.isfinite([xmin, xmax, ymin, ymax]).all() or xmin > xmax or ymin > ymax:
                    raise ValueError("Nonfinite or reversed bounding box at source row %d" % row_number)
                midpoint = [(xmin + xmax) / 2, (ymin + ymax) / 2]
                buffer.append((row_number, oid, object_type, midpoint))
                totals[object_type] += 1
                source_rows += 1
                if len(buffer) >= 8192:
                    consume()
            consume()
    finally:
        if output_handle is not None:
            output_handle.close()
    if sha256_file(source_path) != source["sha256"]:
        raise ValueError("Raw source changed during exploratory counting")
    for object_type in counts:
        if int(counts[object_type].sum()) + outside[object_type] != totals[object_type]:
            raise ValueError("Exploratory object count conservation failed")
    pla, chat = counts[PLA_CLASS], counts[CHAT_CLASS]
    return {**{key: specification[key] for key in ("section_id", "physical_section_id", "animal_id", "condition", "pla_type")},
            "source": source, "fixed_transform": specification["transform"],
            "pla_counts": pla, "chat_counts": chat, "all_counts": pla + chat, "observed_support": (pla + chat) > 0,
            "source_rows": source_rows, "pla_objects": totals[PLA_CLASS], "chat_objects": totals[CHAT_CLASS],
            "in_grid_objects": int(pla.sum() + chat.sum()), "outside_grid_objects": sum(outside.values()),
            "pla_in_grid_objects": int(pla.sum()), "pla_outside_grid_objects": outside[PLA_CLASS],
            "chat_in_grid_objects": int(chat.sum()), "chat_outside_grid_objects": outside[CHAT_CLASS]}


def run_exploratory_maps(manifest_path, authorization_path, output_directory):
    """Publish one immutable local exploratory run only after full validation."""
    manifest_path, authorization_path, output_directory = map(Path, (manifest_path, authorization_path, output_directory))
    manifest_hash, authorization_hash = sha256_file(manifest_path), sha256_file(authorization_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    authorization = json.loads(authorization_path.read_text(encoding="utf-8"))
    if authorization.get("status") != "authorized" or authorization.get("authorized_by") != "user" or not authorization.get("authorization_text"):
        raise ValueError("Explicit user exploratory authorization is required")
    for key in ("sample_relationships", "existing_fixed_alignment", "duplicate_resolution", "grid_definition"):
        if manifest["confirmations"][key].get("confirmed") is not True:
            raise ValueError("Documented selected cohort/fixed transform/grid is unresolved: " + key)
    grid = grid_from_manifest(manifest)
    directions = display_directions_from_manifest(manifest)
    output_directory.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "_" + manifest_hash[:12]
    with tempfile.TemporaryDirectory(prefix=".exploratory-stage-", dir=output_directory) as temporary:
        stage = Path(temporary)
        sections = []
        for number, specification in enumerate(manifest["sections"]):
            prefix = "section_%04d" % number
            section = count_raw_section(specification, grid, manifest_path.parent, stage / (prefix + "_pla_objects.csv.gz"))
            np.savez_compressed(stage / (prefix + ".npz"), x_edges=grid.x_edges, y_edges=grid.y_edges,
                                **{key: section[key] for key in ("pla_counts", "chat_counts", "all_counts", "observed_support")})
            section.update(matrix_file=prefix + ".npz", pla_object_provenance_file=prefix + "_pla_objects.csv.gz")
            sections.append(section)
        summaries = summarize_observed_sections(sections, grid)
        finite = [np.abs(s["difference"][np.isfinite(s["difference"])]) for s in summaries.values()]
        finite = np.concatenate(finite)
        if len(finite) == 0:
            raise ValueError("No bin has observed-object support in both conditions")
        limit = float(finite.max()) or 1.0
        arms = {}
        for arm, summary in summaries.items():
            arrays = {key: value for key, value in summary.items() if isinstance(value, np.ndarray)}
            np.savez_compressed(stage / (arm.lower() + "_matrices.npz"), x_edges=grid.x_edges, y_edges=grid.y_edges, **arrays)
            arms[arm] = {key: _matrix(value) if isinstance(value, np.ndarray) else value for key, value in summary.items()}
            arms[arm].update(homecage_observed_section_n=arms[arm]["homecage_n"],
                             running_observed_section_n=arms[arm]["running_n"])
            with (stage / (arm.lower() + "_bins.csv")).open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["y_bin", "x_bin", "x_min", "x_max", "y_min", "y_max", "homecage_mean_pla_count",
                                 "running_mean_pla_count", "running_minus_homecage", "homecage_observed_section_n", "running_observed_section_n", "displayable"])
                for iy in range(grid.shape[0]):
                    for ix in range(grid.shape[1]):
                        writer.writerow([iy, ix, grid.x_edges[ix], grid.x_edges[ix+1], grid.y_edges[iy], grid.y_edges[iy+1],
                                         *[float(summary[key][iy, ix]) if np.isfinite(summary[key][iy, ix]) else "" for key in ("homecage_mean", "running_mean", "difference")],
                                         int(summary["homecage_n"][iy, ix]), int(summary["running_n"][iy, ix]), bool(summary["displayable"][iy, ix])])
        if sha256_file(manifest_path) != manifest_hash or sha256_file(authorization_path) != authorization_hash:
            raise ValueError("Manifest or exploratory authorization changed during analysis")
        totals = {key: sum(s[key] for s in sections) for key in ("source_rows", "pla_objects", "chat_objects", "in_grid_objects", "outside_grid_objects")}
        validation = {"status": "completed_exploratory", "strict_pdf_results": False, "strict_pdf_results_pending": True,
                      "all_raw_objects_counted": True, "object_sampling_used_for_counts": False,
                      "count_conservation_passed": totals["source_rows"] == totals["in_grid_objects"] + totals["outside_grid_objects"],
                      "input_hashes_verified_before_and_after": True, "fixed_transforms_unchanged": True,
                      "unknown_classes_rejected": True, "unique_object_ids_within_each_source_verified": True,
                      "masks_used": False, "measured_centroids_used": False,
                      "manifest_sha256": manifest_hash, "authorization_sha256": authorization_hash,
                      "source_totals": totals, "sections": len(sections),
                      "displayable_bins_by_arm": {arm: int(summary["displayable"].sum()) for arm, summary in summaries.items()},
                      "generated_utc": datetime.now(timezone.utc).isoformat()}
        parameters = {"position_definition": "Bounding-box midpoint x=(XMin+XMax)/2, y=(YMin+YMax)/2; exploratory only",
                      "support_definition": "Observed(s,b)=(PLA count + ChAT count)>0; not verified tissue coverage",
                      "mean_definition": "Sum of section PLA counts among observed-object-supported sections / observed-object-supported section N",
                      "difference_definition": "Running mean minus Homecage mean separately per PLA type",
                      "n_meaning": "Number of sections with one or more exported known PLA/ChAT objects in the bin; not full-bin tissue coverage",
                      "missing_definition": "Null mean at own-condition N=0; null difference when either condition N=0",
                      "valid_zero_definition": "PLA=0 and ChAT>0 contributes PLA count0 and increases observed-section N",
                      "boundary_convention": "Lower numeric edges inclusive; upper exclusive except outer maximum included",
                      "smoothing": False, "normalization": False, "inferential_tests": False,
                      "known_object_types": {PLA_CLASS: "PLA", CHAT_CLASS: "ChAT"}, "grid": manifest["grid"], "limitations": LIMITATIONS}
        json_sections = [{key: _matrix(value) if isinstance(value, np.ndarray) else value for key, value in section.items()} for section in sections]
        payload = {"schema_version": "comet-exploratory-v1", "status": "exploratory_ready",
                   "analysis_kind": "observed_object_support_exploratory", "strict_pdf_results": False,
                   "strict_pdf_results_pending": True, "title": "Exploratory observed-object-supported PLA count differences",
                   "grid": {**manifest["grid"], "shape": list(grid.shape), "matrix_order": "y_bin,x_bin",
                            "display_directions": {"x": directions[0], "y": directions[1]}},
                   "color_scale": {"cmin": -limit, "cmax": limit, "center": 0, "shared_across_arms": True,
                                   "label": "Exploratory difference in mean exported PLA count per bin (Running − Homecage)",
                                   "missing_color": "#8b9098", "zero_color": "#ffffff"},
                   "arms": arms, "sections": json_sections, "parameters": parameters, "limitations": LIMITATIONS,
                   "authorization": authorization, "validation": validation}
        _json(stage / "view_payload.json", payload)
        _json(stage / "section_index.json", json_sections)
        _json(stage / "parameters.json", parameters)
        _json(stage / "validation.json", validation)
        _json(stage / "manifest_snapshot.json", manifest)
        _json(stage / "authorization_snapshot.json", authorization)
        destination = output_directory / run_id
        shutil.move(str(stage), str(destination))
    _json(output_directory / "latest_run.json", {"run_directory": str(destination.resolve()), "payload_file": "view_payload.json", **validation})
    return destination
