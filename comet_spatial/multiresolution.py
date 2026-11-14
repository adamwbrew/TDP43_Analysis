"""Fresh raw-object exploratory maps at several real spatial resolutions.

An internal greatest-common-divisor grid allows exact integer aggregation to
each requested width after one raw CSV pass. This does not interpolate counts,
average existing maps, infer tissue masks, or alter the recorded transforms.
"""
import csv
import gzip
import json
import math
import shutil
import tempfile
from datetime import datetime, timezone
from functools import reduce
from pathlib import Path

import numpy as np

from .core import GridSpec
from .exploratory import LIMITATIONS, count_raw_section, summarize_observed_sections
from .manifest import display_directions_from_manifest, grid_from_manifest, sha256_file


DEFAULT_WIDTHS = (1000, 500, 250, 100)
MATRIX_KEYS = ("homecage_mean", "running_mean", "difference", "homecage_n", "running_n", "displayable")
SECTION_KEYS = ("section_id", "physical_section_id", "animal_id", "condition", "pla_type", "source", "fixed_transform",
                "source_rows", "pla_objects", "chat_objects", "in_grid_objects", "outside_grid_objects",
                "pla_in_grid_objects", "pla_outside_grid_objects", "chat_in_grid_objects", "chat_outside_grid_objects")


def _save_json(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False) + "\n", encoding="utf-8")


def _matrix(value):
    array = np.asarray(value)
    if np.issubdtype(array.dtype, np.integer) or array.dtype == np.bool_:
        return array.tolist()
    return [[float(number) if np.isfinite(number) else None for number in row] for row in array]


def grid_at_width(reference_grid, width):
    """Same recorded extent and axis metadata, with explicit new numeric edges."""
    if not isinstance(width, int) or isinstance(width, bool) or width <= 0:
        raise ValueError("Bin width must be a positive integer in export units")
    edges = []
    for old in (reference_grid.x_edges, reference_grid.y_edges):
        count = (old[-1] - old[0]) / width
        if count != int(count):
            raise ValueError("Requested width must divide each common extent exactly")
        edges.append(tuple(old[0] + np.arange(int(count) + 1) * width))
    return GridSpec(edges[0], edges[1], reference_grid.coordinate_units, reference_grid.reference_space,
                    reference_grid.x_positive, reference_grid.y_positive)


def aggregate_counts(counts, factor):
    """Sum integer fine bins exactly; never aggregate support or section means."""
    array = np.asarray(counts)
    if (array.ndim != 2 or not np.issubdtype(array.dtype, np.integer) or (array < 0).any() or
            not isinstance(factor, int) or isinstance(factor, bool) or factor <= 0 or
            array.shape[0] % factor or array.shape[1] % factor):
        raise ValueError("Exact aggregation requires nonnegative integer counts and a dividing integer factor")
    return array.reshape(array.shape[0] // factor, factor, array.shape[1] // factor, factor).sum(axis=(1, 3))


def refinement_checks(resolution_sections, widths):
    checks = []
    for coarse in widths:
        for fine in widths:
            if coarse <= fine or coarse % fine:
                continue
            for original, refined in zip(resolution_sections[coarse], resolution_sections[fine]):
                if original["section_id"] != refined["section_id"]:
                    raise ValueError("Refinement section identities differ")
                for key in ("pla_counts", "chat_counts"):
                    if not np.array_equal(original[key], aggregate_counts(refined[key], coarse // fine)):
                        raise ValueError("Refinement conservation failed")
            checks.append({"coarse_width": coarse, "fine_width": fine, "all_section_pla_chat_counts_equal_exact_sum": True})
    return checks


def support_statistics(summary):
    result = {}
    for arm, arrays in summary.items():
        h, r, valid = arrays["homecage_n"], arrays["running_n"], arrays["displayable"]
        either = (h > 0) | (r > 0)
        result[arm] = {
            "total_grid_bins": int(valid.size), "displayable_bins": int(valid.sum()),
            "displayable_fraction_of_grid": float(valid.mean()), "either_condition_observed_bins": int(either.sum()),
            "displayable_fraction_of_either_observed": float(valid.sum() / either.sum()) if either.any() else 0,
            "both_conditions_n_ge_2_bins": int(((h >= 2) & (r >= 2)).sum()),
            "both_conditions_n_ge_3_bins": int(((h >= 3) & (r >= 3)).sum()),
            "zero_difference_bins": int((valid & (arrays["difference"] == 0)).sum()),
            "homecage_observed_n_distribution": {str(int(n)): int((h == n).sum()) for n in np.unique(h)},
            "running_observed_n_distribution": {str(int(n)): int((r == n).sum()) for n in np.unique(r)},
            "n_meaning": "Observed-object-supported physical sections; not full-bin tissue coverage"}
    return result


def _read_pla_points(path, section):
    values = {"section_id": section["section_id"], "animal_id": section["animal_id"],
              "condition": section["condition"], "pla_type": section["pla_type"],
              "source_file_id": section["source"]["source_file_id"], "source_sha256": section["source"]["sha256"],
              "x": [], "y": [], "native_x": [], "native_y": [], "object_id": [], "source_row": [],
              "sampled": False, "position_definition": "Bounding-box midpoint, fixed aligned; not measured centroid"}
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["source_file_id"] != values["source_file_id"]:
                raise ValueError("PLA point provenance source mismatch")
            for key, field in (("x", "x_fixed_aligned"), ("y", "y_fixed_aligned"),
                               ("native_x", "x_bbox_midpoint_native"), ("native_y", "y_bbox_midpoint_native")):
                values[key].append(float(row[field]))
            values["object_id"].append(row["object_id"])
            values["source_row"].append(int(row["source_row_number"]))
    if len(values["x"]) != section["pla_objects"] or len(set(values["object_id"])) != len(values["object_id"]):
        raise ValueError("Full PLA point cache does not conserve unique selected objects")
    values["point_count"] = len(values["x"])
    return values


def _compare_baseline(directory, reference_grid, sections, summaries):
    directory = Path(directory)
    old_sections = json.loads((directory / "section_index.json").read_text(encoding="utf-8"))
    previous = {s["section_id"]: s for s in old_sections}
    if set(previous) != {s["section_id"] for s in sections}:
        raise ValueError("Baseline cohort section identities differ")
    for section in sections:
        old = previous[section["section_id"]]
        if section["source"]["sha256"] != old["source"]["sha256"] or section["fixed_transform"] != old["fixed_transform"]:
            raise ValueError("Baseline raw source or unchanged transform differs")
        for key in ("pla_counts", "chat_counts", "all_counts", "observed_support"):
            if not np.array_equal(section[key], old[key]):
                raise ValueError("Fresh 1000-unit section counts/support differ from baseline: " + key)
    for arm, summary in summaries.items():
        with np.load(directory / (arm.lower() + "_matrices.npz"), allow_pickle=False) as arrays:
            if not np.array_equal(arrays["x_edges"], reference_grid.x_edges) or not np.array_equal(arrays["y_edges"], reference_grid.y_edges):
                raise ValueError("1000-unit baseline grid differs")
            for key in MATRIX_KEYS:
                if not np.array_equal(arrays[key], summary[key], equal_nan=True):
                    raise ValueError("Fresh 1000-unit arm values differ from baseline: " + key)
    return {"directory": str(directory.resolve()), "matched": True,
            "all_section_counts_support_and_arm_mean_difference_n_arrays_exactly_equal": True,
            "baseline_validation_sha256": sha256_file(directory / "validation.json")}


def build_multiresolution_maps(manifest_path, authorization_path, output_directory, *,
                              baseline_directory=None, widths=DEFAULT_WIDTHS):
    """Stream each raw CSV once; save fresh real bins and every PLA coordinate."""
    manifest_path, authorization_path, output_directory = map(Path, (manifest_path, authorization_path, output_directory))
    manifest_hash, auth_hash = sha256_file(manifest_path), sha256_file(authorization_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    authorization = json.loads(authorization_path.read_text(encoding="utf-8"))
    if authorization.get("status") != "authorized" or authorization.get("authorized_by") != "user":
        raise ValueError("Explicit user exploratory authorization is required")
    for key in ("sample_relationships", "existing_fixed_alignment", "duplicate_resolution", "grid_definition"):
        if manifest["confirmations"][key].get("confirmed") is not True:
            raise ValueError("Documented cohort, fixed transform or grid unresolved: " + key)
    widths = tuple(widths)
    if not widths or len(set(widths)) != len(widths) or any(not isinstance(w, int) or isinstance(w, bool) or w <= 0 for w in widths):
        raise ValueError("Distinct positive integer bin widths required")
    reference = grid_from_manifest(manifest)
    directions = display_directions_from_manifest(manifest)
    accumulator_width = reduce(math.gcd, widths)
    accumulator_grid = grid_at_width(reference, accumulator_width)
    grids = {width: grid_at_width(reference, width) for width in widths}
    output_directory.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "_" + manifest_hash[:12]
    with tempfile.TemporaryDirectory(prefix=".multires-stage-", dir=output_directory) as temporary:
        stage = Path(temporary)
        base_sections, point_sections, counts_by_resolution = [], [], {width: [] for width in widths}
        for number, specification in enumerate(manifest["sections"]):
            prefix = "section_%04d" % number
            provenance = stage / (prefix + "_all_pla_points.csv.gz")
            counted = count_raw_section(specification, accumulator_grid, manifest_path.parent, provenance)
            metadata = {key: counted[key] for key in SECTION_KEYS}
            metadata["pla_object_provenance_file"] = provenance.name
            base_sections.append(metadata)
            point_sections.append(_read_pla_points(provenance, counted))
            for width in widths:
                pla = aggregate_counts(counted["pla_counts"], width // accumulator_width)
                chat = aggregate_counts(counted["chat_counts"], width // accumulator_width)
                if int(pla.sum()) != counted["pla_in_grid_objects"] or int(chat.sum()) != counted["chat_in_grid_objects"]:
                    raise ValueError("Per-resolution known-object count conservation failed")
                counts_by_resolution[width].append({**metadata, "pla_counts": pla, "chat_counts": chat,
                                                    "all_counts": pla + chat, "observed_support": (pla + chat) > 0})
        summaries = {width: summarize_observed_sections(counts_by_resolution[width], grids[width]) for width in widths}
        refinement = refinement_checks(counts_by_resolution, widths)
        baseline = None
        if baseline_directory is not None:
            if 1000 not in summaries:
                raise ValueError("Baseline comparison requires the 1000-unit resolution")
            baseline = _compare_baseline(baseline_directory, grids[1000], counts_by_resolution[1000], summaries[1000])
        totals = {key: sum(s[key] for s in base_sections) for key in (
            "source_rows", "pla_objects", "chat_objects", "in_grid_objects", "outside_grid_objects")}
        # Verify all assets again after the full raw pass, beyond the individual
        # before/after checks inside the reused raw reader.
        for section in base_sections:
            source = section["source"]
            path = Path(source["path"])
            path = path if path.is_absolute() else manifest_path.parent / path
            if sha256_file(path) != source["sha256"]:
                raise ValueError("Raw input changed before multiresolution publication")
        if sha256_file(manifest_path) != manifest_hash or sha256_file(authorization_path) != auth_hash:
            raise ValueError("Manifest or authorization changed during multiresolution computation")
        validation = {
            "status": "completed_exploratory_multiresolution", "strict_pdf_results": False, "strict_pdf_results_pending": True,
            "source_totals": totals, "all_raw_objects_counted": True, "raw_csv_passes_per_section": 1,
            "no_point_sampling": True, "full_pla_point_count": sum(p["point_count"] for p in point_sections),
            "full_pla_point_count_matches_raw": sum(p["point_count"] for p in point_sections) == totals["pla_objects"],
            "count_conservation_all_resolutions": True, "exact_refinement_checks": refinement,
            "baseline_1000_comparison": baseline, "hashes_verified_before_after_and_before_publication": True,
            "fixed_transforms_unchanged": True, "masks_used": False, "measured_centroids_used": False,
            "manifest_sha256": manifest_hash, "authorization_sha256": auth_hash,
            "code_sha256": {"comet_spatial/multiresolution.py": sha256_file(Path(__file__)),
                            "comet_spatial/exploratory.py": sha256_file(Path(__file__).with_name("exploratory.py"))},
            "generated_utc": datetime.now(timezone.utc).isoformat()}
        statistics = {str(width): support_statistics(summaries[width]) for width in widths}
        parameters = {"widths_export_units": list(widths), "internal_integer_accumulator_width": accumulator_width,
                      "accumulator_purpose": "Exact integer sums from fresh raw objects; no interpolation or support aggregation",
                      "common_extent": {"x": [reference.x_edges[0], reference.x_edges[-1]],
                                        "y": [reference.y_edges[0], reference.y_edges[-1]]},
                      "position_definition": "Bounding-box midpoint, not measured centroid; unchanged fixed transform",
                      "support_definition": "Per resolution: (raw PLA count + raw ChAT count)>0 for each section/bin",
                      "n_meaning": "Observed-object-supported physical sections, not tissue coverage",
                      "mean_definition": "Equal-section mean PLA count over sections with observed objects in that bin",
                      "missing_definition": "Null difference when either condition has zero observed-object-supported sections",
                      "color_scale_policy": "Symmetric about zero, identical across arms within each resolution; recomputed for each width",
                      "boundary_convention": "Lower numeric edge inclusive; upper exclusive except outer maximum included",
                      "smoothing": False, "interpolation": False, "normalization": False, "inferential_tests": False,
                      "point_detail": "All raw PLA objects and exact object IDs/source rows, not sampled display points"}
        resolutions, resolution_index = {}, {}
        for width in widths:
            directory = stage / ("resolution_%s" % width)
            directory.mkdir()
            grid = grids[width]
            arrays_by_arm = summaries[width]
            finite = np.concatenate([np.abs(values["difference"][np.isfinite(values["difference"])]) for values in arrays_by_arm.values()])
            limit = float(finite.max()) if len(finite) and finite.max() > 0 else 1.0
            arms = {}
            for arm, arrays in arrays_by_arm.items():
                np.savez_compressed(directory / (arm.lower() + "_matrices.npz"), x_edges=grid.x_edges, y_edges=grid.y_edges,
                                    **{key: arrays[key] for key in MATRIX_KEYS})
                arms[arm] = {key: _matrix(value) if isinstance(value, np.ndarray) else value for key, value in arrays.items()}
                arms[arm].update(homecage_observed_section_n=arms[arm]["homecage_n"], running_observed_section_n=arms[arm]["running_n"])
            json_sections = []
            for number, section in enumerate(counts_by_resolution[width]):
                matrix_file = "section_%04d.npz" % number
                np.savez_compressed(directory / matrix_file, x_edges=grid.x_edges, y_edges=grid.y_edges,
                                    **{key: section[key] for key in ("pla_counts", "chat_counts", "all_counts", "observed_support")})
                json_sections.append({**{key: section[key] for key in SECTION_KEYS}, "matrix_file": matrix_file,
                                      **{key: _matrix(section[key]) for key in ("pla_counts", "chat_counts", "all_counts", "observed_support")}})
            payload = {
                "schema_version": "comet-exploratory-v1", "status": "exploratory_ready",
                "analysis_kind": "observed_object_support_exploratory", "strict_pdf_results": False, "strict_pdf_results_pending": True,
                "bin_width_export_units": width,
                "grid": {**manifest["grid"], "x_edges": list(grid.x_edges), "y_edges": list(grid.y_edges),
                         "shape": list(grid.shape), "bin_width_export_units": width, "matrix_order": "y_bin,x_bin",
                         "display_directions": {"x": directions[0], "y": directions[1]}},
                "color_scale": {"cmin": -limit, "cmax": limit, "center": 0, "shared_across_arms": True,
                                "label": "Exploratory difference in mean exported PLA count per bin (Running − Homecage)",
                                "missing_color": "#8b9098", "zero_color": "#ffffff"},
                "arms": arms, "sections": json_sections, "parameters": parameters, "limitations": LIMITATIONS,
                "validation": {**validation, "displayable_bins_by_arm": {arm: statistics[str(width)][arm]["displayable_bins"] for arm in arms}},
                "statistics": statistics[str(width)]}
            _save_json(directory / "view_payload.json", payload)
            resolutions[str(width)] = payload
            resolution_index[str(width)] = {"payload_file": "resolution_%s/view_payload.json" % width,
                                            "shape": list(grid.shape), "statistics": statistics[str(width)]}
        _save_json(stage / "pla_points.json", {"schema_version": "comet-pla-point-detail-v1", "sampled": False, "sections": point_sections})
        combined = {"schema_version": "comet-multiresolution-v1", "status": "exploratory_ready", "strict_pdf_results": False,
                    "strict_pdf_results_pending": True, "default_resolution": "250" if 250 in widths else str(widths[0]),
                    "resolutions": resolutions, "pla_points": point_sections, "sections": base_sections,
                    "statistics_by_resolution": statistics, "validation": validation, "parameters": parameters,
                    "limitations": LIMITATIONS, "authorization": authorization}
        _save_json(stage / "view_payload.json", combined)
        _save_json(stage / "index.json", {"schema_version": "comet-multiresolution-v1", "resolutions": resolution_index,
                                          "point_detail_file": "pla_points.json", "payload_file": "view_payload.json", "validation": validation})
        _save_json(stage / "validation.json", validation)
        _save_json(stage / "parameters.json", parameters)
        _save_json(stage / "statistics_by_resolution.json", statistics)
        _save_json(stage / "section_index.json", base_sections)
        _save_json(stage / "manifest_snapshot.json", manifest)
        _save_json(stage / "authorization_snapshot.json", authorization)
        destination = output_directory / run_id
        shutil.move(str(stage), str(destination))
    _save_json(output_directory / "latest_run.json", {"run_directory": str(destination.resolve()), "payload_file": "view_payload.json",
                                                    "index_file": "index.json", **validation})
    return destination
