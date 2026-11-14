"""Read and verify an immutable core spatial run for the three PDF views.

This module does not fit alignment, infer masks, derive centroids, rerun source
selection, or produce example experimental results. Missing inputs yield an
empty blocked payload. The only previews sampled here are object coordinates;
all selected objects contribute to verification of the saved count matrices.
"""
import csv
import gzip
import json
from pathlib import Path

import numpy as np
from shapely.geometry import mapping, shape
from shapely.errors import GEOSException

from .core import (
    FixedTransform, SectionResult, assign_centroid_bins, polygon_tissue_validity,
    raster_cell_footprints, shared_symmetric_limit, summarize_by_arm,
)
from .manifest import display_directions_from_manifest, grid_from_manifest, sha256_file


SCHEMA_VERSION = "comet-core-view-v1"
COLORBAR_LABEL = "Difference in mean PLA count per spatial bin (Running − Homecage)"
MATRIX_FIELDS = ("homecage_mean", "running_mean", "difference", "homecage_n", "running_n", "displayable")


def _read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _run_file(directory, filename):
    """Run artifacts must stay inside their explicitly selected run directory."""
    if not isinstance(filename, str) or not filename:
        raise ValueError("Run artifact filename is missing")
    path = (directory / filename).resolve()
    if directory != path and directory not in path.parents:
        raise ValueError("Run artifact escapes the run directory")
    if not path.is_file():
        raise ValueError("Saved run artifact is missing: " + filename)
    return path


def _json_matrix(values):
    array = np.asarray(values)
    if array.dtype == np.bool_ or np.issubdtype(array.dtype, np.integer):
        return array.tolist()
    return [[float(value) if np.isfinite(value) else None for value in row] for row in array]


def _blocked(reasons, preflight=None):
    reasons = list(dict.fromkeys(str(value) for value in reasons if value))
    if not reasons:
        reasons = ["No verified aligned core run has been supplied."]
    return {
        "schema_version": SCHEMA_VERSION, "status": "blocked", "blockers": reasons,
        "warnings": [], "grid": None, "color_scale": None, "arms": {}, "sections": [],
        "validation": {"core_payload_verified": False, "scientific_acceptance_passed": False,
                       "preflight": preflight},
        "views": {key: {"available": False, "fulfilled": False, "blockers": reasons}
                  for key in ("differences", "coverage", "alignment")},
        "alignment": {"status": "unavailable", "reference": None, "sections": [],
                      "blockers": reasons},
    }


def _load_arrays(path, grid, keys):
    with np.load(path, allow_pickle=False) as values:
        missing = (set(keys) | {"x_edges", "y_edges"}) - set(values.files)
        if missing:
            raise ValueError("Required matrix arrays absent: " + ", ".join(sorted(missing)))
        if not np.array_equal(values["x_edges"], grid.x_edges) or not np.array_equal(values["y_edges"], grid.y_edges):
            raise ValueError("Saved matrices do not use the one recorded shared grid")
        arrays = {key: values[key].copy() for key in keys}
    if any(value.shape != grid.shape for value in arrays.values()):
        raise ValueError("Saved matrix shape disagrees with recorded grid edges")
    return arrays


def _provenance_preview(path, section, grid, preview_limit):
    """Verify every saved object, count conservation, and unchanged transform."""
    total = section["selected_objects"]
    if not isinstance(total, int) or isinstance(total, bool) or total < 0:
        raise ValueError("Selected-object total is invalid")
    selected = set(np.linspace(0, total - 1, min(preview_limit, total), dtype=int).tolist())
    native_preview, aligned_preview, ids_preview, row_preview = [], [], [], []
    recounted = np.zeros(grid.shape, dtype=np.int64)
    transform = FixedTransform(section["fixed_transform"]["matrix"])
    expected_source = section["source"]["source_file_id"]
    seen_ids, seen_rows, buffered_native, buffered_aligned = set(), set(), [], []
    objects_seen, in_grid = 0, 0

    def verify_chunk():
        nonlocal in_grid
        if not buffered_native:
            return
        native = np.asarray(buffered_native, dtype=float)
        aligned = np.asarray(buffered_aligned, dtype=float)
        if not np.isfinite(native).all() or not np.isfinite(aligned).all():
            raise ValueError("Saved object coordinates contain nonfinite values")
        # Numeric round-trip tolerance applies only to verification of saved
        # floating point coordinates, never to strict tissue containment.
        if not np.allclose(transform.points(native), aligned, rtol=1e-13, atol=1e-12):
            raise ValueError("Saved aligned coordinates disagree with supplied unchanged transform")
        bins, inside = assign_centroid_bins(aligned, grid)
        np.add.at(recounted, (bins[inside, 0], bins[inside, 1]), 1)
        in_grid += int(inside.sum())
        buffered_native.clear()
        buffered_aligned.clear()

    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = {"source_file_id", "source_row_number", "object_id", "x_input", "y_input", "x_aligned", "y_aligned"}
        if not fields.issubset(reader.fieldnames or []):
            raise ValueError("Saved object provenance lacks required coordinate/identity columns")
        for row in reader:
            if row["source_file_id"] != expected_source:
                raise ValueError("Saved object provenance source identity disagrees with section metadata")
            identifier = row["object_id"]
            row_number = int(row["source_row_number"])
            if not identifier or identifier in seen_ids or row_number < 2 or row_number in seen_rows:
                raise ValueError("Saved object provenance has missing/repeated object or source-row identity")
            seen_ids.add(identifier)
            seen_rows.add(row_number)
            native = [float(row["x_input"]), float(row["y_input"])]
            aligned = [float(row["x_aligned"]), float(row["y_aligned"])]
            if objects_seen in selected:
                native_preview.append(native)
                aligned_preview.append(aligned)
                ids_preview.append(identifier)
                row_preview.append(row_number)
            buffered_native.append(native)
            buffered_aligned.append(aligned)
            objects_seen += 1
            if len(buffered_native) >= 8192:
                verify_chunk()
        verify_chunk()
    if objects_seen != total or in_grid != section["in_grid_objects"]:
        raise ValueError("Saved object provenance/count conservation disagrees with section index")
    if in_grid + section["outside_grid_objects"] != total:
        raise ValueError("Saved section has inconsistent in/out-grid object totals")
    return recounted, {
        "native_centroid_preview": native_preview, "aligned_centroid_preview": aligned_preview,
        "object_id_preview": ids_preview, "source_row_number_preview": row_preview,
        "preview_sampling": {"method": "evenly_spaced_selected_source_row_indices", "limit": preview_limit,
                             "shown_objects": len(native_preview), "total_selected_objects": total,
                             "sampled": len(native_preview) < total,
                             "counts_use_all_selected_objects": True},
    }


def _mask_geometry(specification, transform, manifest_base_dir):
    path = Path(specification["path"])
    if not path.is_absolute():
        if manifest_base_dir is None:
            raise ValueError("Relative existing-mask path requires its original manifest_base_dir")
        path = Path(manifest_base_dir) / path
    if not path.is_file() or sha256_file(path) != specification["sha256"]:
        raise ValueError("Existing mask is missing or its recorded SHA-256 does not match")
    if specification["format"] == "geojson":
        value = _read_json(path)
        original = shape(value["geometry"] if value.get("type") == "Feature" else value)
        # Identity application validates without repairing the supplied mask.
        original = FixedTransform(((1, 0, 0), (0, 1, 0), (0, 0, 1))).geometry(original)
    elif specification["format"] == "raster_npz":
        with np.load(path, allow_pickle=False) as arrays:
            original = raster_cell_footprints(arrays["mask"], arrays["x_edges"], arrays["y_edges"],
                                              FixedTransform(((1, 0, 0), (0, 1, 0), (0, 0, 1))))
    else:
        raise ValueError("Existing mask format is unsupported")
    if specification["coordinate_space"] == "native":
        return original, transform.geometry(original)
    if specification["coordinate_space"] == "aligned":
        return None, original
    raise ValueError("Existing mask coordinate space is unresolved")


def _alignment_geometry(directory, index, grid, manifest_base_dir):
    """Use recorded run geometry when supplied, otherwise the hashed existing mask."""
    if index.get("aligned_mask_file"):
        aligned_path = _run_file(directory, index["aligned_mask_file"])
        if index.get("aligned_mask_sha256") and sha256_file(aligned_path) != index["aligned_mask_sha256"]:
            raise ValueError("Recorded aligned mask artifact SHA-256 mismatch")
        aligned = shape(_read_json(aligned_path))
        native = None
        if index.get("native_mask_file"):
            native_path = _run_file(directory, index["native_mask_file"])
            if index.get("native_mask_sha256") and sha256_file(native_path) != index["native_mask_sha256"]:
                raise ValueError("Recorded native mask artifact SHA-256 mismatch")
            native = shape(_read_json(native_path))
        # Reject invalid geometry instead of automatic repair.
        identity = FixedTransform(((1, 0, 0), (0, 1, 0), (0, 0, 1)))
        aligned = identity.geometry(aligned)
        if native is not None:
            supplied = FixedTransform(index["fixed_transform"]["matrix"]).geometry(native)
            if not supplied.equals_exact(aligned, 0):
                raise ValueError("Recorded mask preview changed the fixed transform")
        return native, aligned
    return _mask_geometry(index["mask"], FixedTransform(index["fixed_transform"]["matrix"]), manifest_base_dir)


def build_core_view_payload(run_directory=None, *, manifest_base_dir=None, preflight=None, preview_limit=2000):
    """Build JSON-safe current core views from a verified immutable run.

    preflight, when supplied and blocked, takes precedence over any stale run.
    No run yields no arrays. Numerical availability does not imply that the
    prior alignment-check layout has been reproduced or visually confirmed.
    Exact original mask geometry is never inferred from detections or images.
    """
    if preflight is not None and preflight.get("status") != "ready":
        return _blocked(preflight.get("blockers", []), preflight)
    if run_directory is None:
        return _blocked(["No verified aligned core run has been supplied."], preflight)
    if not isinstance(preview_limit, int) or isinstance(preview_limit, bool) or preview_limit < 0:
        return _blocked(["preview_limit must be a nonnegative integer"], preflight)
    directory = Path(run_directory).expanduser().resolve()
    try:
        manifest = _read_json(_run_file(directory, "manifest_snapshot.json"))
        validation = _read_json(_run_file(directory, "validation.json"))
        index = _read_json(_run_file(directory, "section_index.json"))
        if validation.get("software_status") != "completed" or validation.get("count_conservation_passed") is not True:
            raise ValueError("Saved run did not complete count-conservation validation")
        grid = grid_from_manifest(manifest)
        directions = display_directions_from_manifest(manifest)
        specifications = {value["section_id"]: value for value in manifest["sections"]}
        if len(specifications) != len(manifest["sections"]) or len(index) != len(specifications):
            raise ValueError("Run section index and manifest do not have a unique one-to-one mapping")
        sections, payload_sections, previews, warnings, mask_blockers = [], [], [], [], []
        seen = set()
        for record in index:
            sid = record["section_id"]
            if sid in seen or sid not in specifications:
                raise ValueError("Run section index has repeated/unmapped section IDs")
            seen.add(sid)
            specification = specifications[sid]
            for field in ("animal_id", "physical_section_id", "condition", "pla_type", "source", "mask"):
                if record[field] != specification[field]:
                    raise ValueError("Saved section provenance disagrees with manifest: " + field)
            if record["fixed_transform"] != specification["transform"]:
                raise ValueError("Saved fixed transform disagrees with manifest")
            values = _load_arrays(_run_file(directory, record["matrix_file"]), grid, ("counts", "tissue_validity"))
            if values["tissue_validity"].dtype != np.bool_:
                raise ValueError("Saved tissue-validity matrix must be boolean")
            result = SectionResult(*(record[key] for key in (
                "section_id", "animal_id", "physical_section_id", "condition", "pla_type")),
                                   values["counts"], values["tissue_validity"])
            recounted, preview = _provenance_preview(_run_file(directory, record["object_provenance_file"]),
                                                    record, grid, preview_limit)
            if not np.array_equal(recounted, result.counts):
                raise ValueError("Saved section counts disagree with all saved object provenance")
            if int(result.tissue_validity.sum()) != record["valid_bins"]:
                raise ValueError("Saved valid-bin total disagrees with section index")
            geometry_preview = {"native_mask_geojson": None, "aligned_mask_geojson": None}
            try:
                native_mask, aligned_mask = _alignment_geometry(directory, record, grid, manifest_base_dir)
                if not np.array_equal(polygon_tissue_validity(aligned_mask, grid), result.tissue_validity):
                    raise ValueError("Saved tissue-validity matrix disagrees with supplied full-bin mask geometry")
                geometry_preview = {"native_mask_geojson": mapping(native_mask) if native_mask is not None else None,
                                    "aligned_mask_geojson": mapping(aligned_mask)}
            except (OSError, KeyError, TypeError, ValueError, GEOSException) as exc:
                # Missing external masks can leave a portable numerical snapshot
                # readable. A mask that exists but contradicts saved validity is
                # a numerical integrity failure, not just an unavailable preview.
                if "disagrees" in str(exc) or "changed the fixed transform" in str(exc) or "mismatch" in str(exc):
                    raise
                mask_blockers.append(sid + ": " + str(exc))
            sections.append(result)
            payload_sections.append({key: record[key] for key in (
                "section_id", "animal_id", "physical_section_id", "condition", "pla_type", "source", "mask",
                "fixed_transform", "selected_objects", "in_grid_objects", "outside_grid_objects", "matrix_file",
                "object_provenance_file")})
            payload_sections[-1].update(counts=values["counts"].tolist(),
                                        tissue_validity=values["tissue_validity"].tolist())
            previews.append({"section_id": sid, "pla_type": result.pla_type, "condition": result.condition,
                             **preview, **geometry_preview})
        summaries = summarize_by_arm(sections, grid)
        arms = {}
        for arm, expected in summaries.items():
            saved = _load_arrays(_run_file(directory, arm.lower() + "_matrices.npz"), grid, MATRIX_FIELDS)
            for key in MATRIX_FIELDS:
                if not np.array_equal(saved[key], getattr(expected, key), equal_nan=True):
                    raise ValueError("Saved %s %s does not equal section-derived values" % (arm, key))
            arms[arm] = {key: _json_matrix(saved[key]) for key in MATRIX_FIELDS}
            arms[arm]["section_ids"] = list(expected.section_ids)
            arms[arm]["eligible_section_totals"] = {
                condition: sum(s.pla_type == arm and s.condition == condition for s in sections)
                for condition in ("Homecage", "Running")}
        limit = shared_symmetric_limit(summaries)
        if validation.get("shared_symmetric_color_limit") != limit:
            raise ValueError("Saved shared symmetric color limit disagrees with verified differences")
        mask_geometry_rechecked = not mask_blockers
        reference_files = list(directory.glob("accepted_alignment_reference.*"))
        reference = None
        if len(reference_files) == 1 and sha256_file(reference_files[0]) == manifest["alignment_reference"]["sha256"]:
            reference = {**manifest["alignment_reference"], "run_file": reference_files[0].name,
                         "local_path": str(reference_files[0])}
        else:
            mask_blockers.append("Copied accepted alignment reference is missing or its hash does not match")
        alignment_available = reference is not None and not mask_blockers
        alignment_status = "inspection_pending" if alignment_available else "unavailable"
        alignment_notes = list(mask_blockers)
        # An arbitrary inspection overlay is not the requested same prior figure.
        if validation.get("alignment_reproduction_status") != "matches_previous_accepted_figure":
            alignment_notes.append("The regenerated fixed-coordinate view is an inspection aid. The prior figure's "
                                   "layout, layers, limits and sampling must be preserved and compared before claiming exact reproduction.")
        warnings.extend(validation.get("blockers", []))
        warnings.extend(mask_blockers)
        return {
            "schema_version": SCHEMA_VERSION, "status": "numerical_ready", "blockers": [],
            "warnings": warnings, "run_directory": str(directory),
            "grid": {**manifest["grid"], "matrix_order": "y_bin,x_bin",
                     "shape": list(grid.shape), "display_directions": {"x": directions[0], "y": directions[1]},
                     "boundary_convention": "Lower numeric edges inclusive; upper exclusive except outer maximum included"},
            "color_scale": {"cmin": -limit, "cmax": limit, "center": 0, "label": COLORBAR_LABEL,
                            "shared_across_arms": True, "missing_color": "#8b9098", "zero_color": "#ffffff"},
            "arms": arms, "sections": payload_sections,
            "views": {
                "differences": {"available": True, "fulfilled": True, "blockers": []},
                "coverage": {"available": True, "fulfilled": True, "blockers": []},
                "alignment": {"available": alignment_available,
                              "fulfilled": alignment_available and validation.get("alignment_reproduction_status") == "matches_previous_accepted_figure",
                              "status": alignment_status, "blockers": alignment_notes}},
            "alignment": {"status": alignment_status, "reference": reference, "sections": previews,
                          "blockers": alignment_notes, "transform_policy": "Apply recorded fixed transform only; never fit or update",
                          "preview_is_microscopy_pixels": False},
            "validation": {**validation, "core_payload_verified": True, "section_mean_arithmetic_verified": True,
                           "all_saved_objects_recounted": True,
                           "strict_mask_geometry_rechecked": mask_geometry_rechecked,
                           "scientific_acceptance_passed": validation.get("scientific_acceptance_passed") is True,
                           "preflight": preflight},
            "interpretation": {
                "unit": "PLA detections per spatial bin averaged equally over valid physical sections",
                "difference": "Running mean minus Homecage mean within each PLA type",
                "valid_zero": "A fully covered section with no PLA contributes 0",
                "missing": "A difference is null when either condition has no section fully covering the bin",
                "coverage": "N is the number of valid tissue sections, not animals or objects",
                "section_contributions": "For hover use only matching-arm/condition sections whose tissue_validity[y][x] is true",
                "limits": "Descriptive counts; no smoothing, interpolation, normalization or inferential tests"},
        }
    except (OSError, KeyError, TypeError, ValueError, IndexError, GEOSException) as exc:
        return _blocked(["Saved core run could not be verified: " + str(exc)], preflight)
