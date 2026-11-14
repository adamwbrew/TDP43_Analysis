#!/usr/bin/env python3
"""Run the specified raw-count workflow only after explicit input preflight.

Exit codes: 0 = preflight ready; 2 = blocked/invalid inputs; 3 = numerical run
completed but alignment reproduction/comparison still needs scientist review.
No alignment fitting, centroid derivation, mask inference or normalization is
performed. Every successful full run is retained in a separate output folder.
"""
import argparse
import csv
import gzip
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from shapely.geometry import shape, mapping

from comet_spatial.core import (
    FixedTransform, SectionResult, count_section, polygon_tissue_validity,
    raster_cell_footprints, shared_symmetric_limit, summarize_by_arm,
)
from comet_spatial.manifest import (
    display_directions_from_manifest, grid_from_manifest, load_manifest, preflight_manifest, sha256_file,
)


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
                    encoding="utf-8")


def asset_path(asset, base):
    path = Path(asset["path"])
    return path if path.is_absolute() else base / path


def display_directions(manifest):
    """Do not guess screen orientation from an anatomical axis description."""
    return display_directions_from_manifest(manifest)


def read_objects(source, base):
    """Read selected rows exactly; identifiers and selection values stay strings."""
    selection = source["object_selection"]
    predicates = selection.get("predicates", {}) if selection["mode"] == "column_equals" else {}
    if any(not isinstance(value, str) for value in predicates.values()):
        raise ValueError("column_equals predicate values must be exact exported strings")
    columns = [source["object_id_column"], source["centroid_x_column"], source["centroid_y_column"]]
    pla_definition = source["pla_object_type"]
    classification = (pla_definition.get("classification_column")
                      if pla_definition["kind"] == "classified_mixed_source" else None)
    ids, native, row_numbers = [], [], []
    seen_rows = 0
    with asset_path(source, base).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
            raise ValueError("Missing or duplicated CSV column headers")
        if "Object Type" in reader.fieldnames and classification is None:
            raise ValueError("CSV has an Object Type field: explicitly declare its accepted PLA classification values")
        missing = set(columns + list(predicates) + ([classification] if classification else [])) - set(reader.fieldnames)
        if missing:
            raise ValueError("Required exact CSV columns absent: " + ", ".join(sorted(missing)))
        for row_number, row in enumerate(reader, start=2):
            seen_rows += 1
            if None in row or any(value is None for value in row.values()):
                raise ValueError("Malformed CSV row %d; no rows silently dropped" % row_number)
            if any(row[column] != expected for column, expected in predicates.items()):
                continue
            if classification and row[classification] not in pla_definition["accepted_values"]:
                raise ValueError("Selected non-PLA object classification at CSV row %d; explicit object_selection "
                                 "must select only the declared PLA values" % row_number)
            try:
                xy = [float(row[columns[1]]), float(row[columns[2]])]
            except (ValueError, TypeError) as exc:
                raise ValueError("Non-numeric accepted centroid at CSV row %d" % row_number) from exc
            if not np.isfinite(xy).all():
                raise ValueError("Nonfinite accepted centroid at CSV row %d" % row_number)
            ids.append(row[columns[0]])
            native.append(xy)
            row_numbers.append(row_number)
    return ids, np.asarray(native, dtype=float).reshape((-1, 2)), row_numbers, seen_rows


def load_existing_mask(specification, transform, base):
    """Use existing polygon/raster footprints without repair or resampling."""
    supplied = transform if specification["coordinate_space"] == "native" else FixedTransform(
        ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    path = asset_path(specification, base)
    if specification["format"] == "geojson":
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("Existing GeoJSON must be an object")
        if value.get("type") == "Feature":
            value = value.get("geometry")
        if not isinstance(value, dict) or value.get("type") not in ("Polygon", "MultiPolygon"):
            raise ValueError("Existing GeoJSON must contain one Polygon/MultiPolygon or Feature")
        return supplied.geometry(shape(value))
    with np.load(path, allow_pickle=False) as value:
        if not {"mask", "x_edges", "y_edges"}.issubset(value.files):
            raise ValueError("Existing raster_npz requires boolean mask and explicit x_edges/y_edges")
        return raster_cell_footprints(value["mask"], value["x_edges"], value["y_edges"], supplied)


def write_objects(path, source, ids, native, aligned, row_numbers):
    with gzip.open(path, "wt", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source_file_id", "source_row_number", "object_id", "x_input", "y_input",
                         "x_aligned", "y_aligned"])
        for oid, xy, xy_aligned, row_number in zip(ids, native, aligned, row_numbers):
            writer.writerow([source["source_file_id"], row_number, oid, *xy, *xy_aligned])


def orient_axes(ax, grid, directions):
    ax.set_xlim(grid.x_edges[0], grid.x_edges[-1])
    ax.set_ylim(grid.y_edges[0], grid.y_edges[-1])
    if directions[0] == "left":
        ax.invert_xaxis()
    if directions[1] == "down":
        ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.set_xlabel("Aligned x (%s)" % grid.coordinate_units)
    ax.set_ylabel("Aligned y (%s)" % grid.coordinate_units)


def export_figures(directory, grid, summaries, sections, masks, samples, directions):
    os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "tdp43-matplotlib-cache"))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize
    from matplotlib.ticker import MaxNLocator

    plt.rcParams.update({"font.size": 10, "svg.fonttype": "none", "savefig.facecolor": "white"})
    limit = shared_symmetric_limit(summaries)
    # A white zero and darker missing gray must remain visibly distinct.
    diverging = plt.get_cmap("RdBu_r").with_extremes(bad="#8b9098")

    def save(fig, name):
        fig.savefig(directory / (name + ".png"), dpi=300, bbox_inches="tight")
        fig.savefig(directory / (name + ".svg"), bbox_inches="tight")
        plt.close(fig)

    for arm, summary in summaries.items():
        fig, ax = plt.subplots(figsize=(9, 7), layout="constrained")
        image = ax.pcolormesh(grid.x_edges, grid.y_edges, np.ma.masked_invalid(summary.difference),
                              cmap=diverging, norm=Normalize(-limit, limit), shading="flat", rasterized=True)
        orient_axes(ax, grid, directions)
        ax.set_title("TDP43-%s: Running − Homecage" % arm)
        fig.colorbar(image, ax=ax, label="Difference in mean PLA count per spatial bin (Running − Homecage)")
        fig.text(.02, -.01, "Gray: no fully covered section in one or both conditions. Zero is a valid difference.",
                 fontsize=9)
        save(fig, "difference_" + arm.lower())

    maximum_n = max(sum(s.pla_type == arm and s.condition == condition for s in sections)
                    for arm in summaries for condition in ("Homecage", "Running"))
    fig, axes = plt.subplots(2, 2, figsize=(13, 11), layout="constrained")
    for row, (arm, summary) in enumerate(summaries.items()):
        for col, condition in enumerate(("Homecage", "Running")):
            ax = axes[row, col]
            n = summary.homecage_n if condition == "Homecage" else summary.running_n
            image = ax.pcolormesh(grid.x_edges, grid.y_edges, n, cmap="viridis",
                                  vmin=0, vmax=max(1, maximum_n), shading="flat", rasterized=True)
            orient_axes(ax, grid, directions)
            ax.set_title("TDP43-%s · %s" % (arm, condition))
    bar = fig.colorbar(image, ax=axes.ravel().tolist(), label="Sections fully covering the entire bin")
    bar.locator = MaxNLocator(integer=True)
    bar.update_ticks()
    save(fig, "coverage_four_panels")

    fig, axes = plt.subplots(1, 2, figsize=(14, 7), layout="constrained")
    for ax, arm in zip(axes, ("HK1", "PFKP")):
        for index, section in enumerate(sections):
            if section.pla_type != arm:
                continue
            color = plt.get_cmap("tab10")(index % 10)
            geometry = masks[section.section_id]
            polygons = [geometry] if geometry.geom_type == "Polygon" else list(geometry.geoms)
            for polygon_index, polygon in enumerate(polygons):
                x, y = polygon.exterior.xy
                ax.plot(x, y, color=color, lw=1.2,
                        label=section.section_id if polygon_index == 0 else None)
                for hole in polygon.interiors:
                    ax.plot(*hole.xy, color=color, lw=.8, linestyle="--")
            points = samples[section.section_id]
            if len(points):
                ax.scatter(points[:, 0], points[:, 1], color=color, s=1, alpha=.2, rasterized=True)
        orient_axes(ax, grid, directions)
        ax.set_title("TDP43-%s: supplied fixed alignment" % arm)
        ax.legend(fontsize=7, loc="best")
    fig.suptitle("Regenerated mask/centroid inspection view · comparison with accepted reference pending")
    save(fig, "alignment_inspection_regenerated")
    return limit


def save_matrices(directory, summaries, grid):
    for arm, summary in summaries.items():
        values = {name: getattr(summary, name) for name in (
            "homecage_mean", "running_mean", "difference", "homecage_n", "running_n", "displayable")}
        np.savez_compressed(directory / (arm.lower() + "_matrices.npz"),
                            x_edges=grid.x_edges, y_edges=grid.y_edges, **values)
        with (directory / (arm.lower() + "_bins.csv")).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["y_bin", "x_bin", "x_min", "x_max", "y_min", "y_max",
                             "homecage_mean_count", "running_mean_count", "running_minus_homecage_mean_count",
                             "homecage_valid_section_count", "running_valid_section_count", "displayable"])
            for iy in range(grid.shape[0]):
                for ix in range(grid.shape[1]):
                    means = [values[key][iy, ix] for key in ("homecage_mean", "running_mean", "difference")]
                    writer.writerow([iy, ix, grid.x_edges[ix], grid.x_edges[ix + 1], grid.y_edges[iy],
                                     grid.y_edges[iy + 1], *[float(v) if np.isfinite(v) else "" for v in means],
                                     int(summary.homecage_n[iy, ix]), int(summary.running_n[iy, ix]),
                                     bool(summary.displayable[iy, ix])])


def execute(manifest, manifest_path, output_directory, directions):
    base = manifest_path.parent
    grid = grid_from_manifest(manifest)
    output_directory.mkdir(parents=True, exist_ok=True)
    sections, index, masks, samples = [], [], {}, {}
    manifest_hash = sha256_file(manifest_path)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    run_name = stamp + "_" + manifest_hash[:12]
    with tempfile.TemporaryDirectory(prefix=".analysis-stage-", dir=output_directory) as temporary:
        stage = Path(temporary)
        for number, specification in enumerate(manifest["sections"]):
            source = specification["source"]
            ids, native, row_numbers, total_source_rows = read_objects(source, base)
            transform = FixedTransform(specification["transform"]["matrix"])
            aligned = transform.points(native)
            mask = load_existing_mask(specification["mask"], transform, base)
            counts = count_section(aligned, grid, ids)
            validity = polygon_tissue_validity(mask, grid)
            result = SectionResult(*(specification[key] for key in (
                "section_id", "animal_id", "physical_section_id", "condition", "pla_type")),
                                   counts.counts, validity)
            sections.append(result)
            masks[result.section_id] = mask
            sample_indices = np.linspace(0, len(aligned) - 1, min(2000, len(aligned)), dtype=int)
            samples[result.section_id] = aligned[sample_indices]
            prefix = "section_%04d" % number
            np.savez_compressed(stage / (prefix + ".npz"), counts=counts.counts, tissue_validity=validity,
                                x_edges=grid.x_edges, y_edges=grid.y_edges)
            write_objects(stage / (prefix + "_objects.csv.gz"), source, ids, native, aligned, row_numbers)
            # Retain actual mask geometry for portable inspection, with no
            # inferred outline, repair, buffer, or resampling.
            aligned_mask_file = prefix + "_aligned_mask.geojson"
            save_json(stage / aligned_mask_file, mapping(mask))
            mask_artifacts = {"aligned_mask_file": aligned_mask_file,
                              "aligned_mask_sha256": sha256_file(stage / aligned_mask_file)}
            if specification["mask"]["coordinate_space"] == "native":
                native_mask = load_existing_mask(specification["mask"], FixedTransform(np.eye(3)), base)
                native_mask_file = prefix + "_native_mask.geojson"
                save_json(stage / native_mask_file, mapping(native_mask))
                mask_artifacts.update(native_mask_file=native_mask_file,
                                      native_mask_sha256=sha256_file(stage / native_mask_file))
            index.append({"section_id": result.section_id, "animal_id": result.animal_id,
                          "physical_section_id": result.physical_section_id, "condition": result.condition,
                          "pla_type": result.pla_type, "source": source, "mask": specification["mask"],
                          "fixed_transform": specification["transform"], "source_rows": total_source_rows,
                          "selected_objects": counts.total_objects, "in_grid_objects": counts.in_grid_objects,
                          "outside_grid_objects": counts.outside_grid_objects,
                          "valid_bins": int(validity.sum()), "matrix_file": prefix + ".npz",
                          "object_provenance_file": prefix + "_objects.csv.gz", **mask_artifacts})
        summaries = summarize_by_arm(sections, grid)
        for arm, summary in summaries.items():
            if not summary.displayable.any():
                raise ValueError("No bin has valid tissue in both conditions for " + arm)
            if not np.allclose(summary.difference[summary.displayable],
                               (summary.running_mean - summary.homecage_mean)[summary.displayable]):
                raise ValueError("Difference arithmetic validation failed for " + arm)
        # Detect input changes during CSV reading or geometry processing.
        checked = set()
        for specification in manifest["sections"]:
            for asset in (specification["source"], specification["mask"]):
                path = asset_path(asset, base)
                if path not in checked and sha256_file(path) != asset["sha256"]:
                    raise ValueError("Input changed during analysis: " + str(path))
                checked.add(path)
        save_matrices(stage, summaries, grid)
        limit = export_figures(stage, grid, summaries, sections, masks, samples, directions)
        reference = asset_path(manifest["alignment_reference"], base)
        if sha256_file(reference) != manifest["alignment_reference"]["sha256"]:
            raise ValueError("Accepted alignment reference changed during analysis")
        shutil.copyfile(reference, stage / ("accepted_alignment_reference" + reference.suffix))
        save_json(stage / "manifest_snapshot.json", manifest)
        save_json(stage / "section_index.json", index)
        acceptance = {"software_status": "completed", "scientific_acceptance": "pending",
                      "scientific_acceptance_passed": False,
                      "alignment_reproduction_status": "inspection_view_regenerated_unverified",
                      "blockers": ["Compare regenerated fixed-mask/centroid view with the accepted alignment reference. "
                                   "Exact reproduction of the prior alignment-check figure requires its layout, layers, "
                                   "limits and sampling parameters; these are not inferred from a summary image."],
                      "display_orientation": {"x_increases_to": directions[0], "y_increases_to": directions[1]},
                      "shared_symmetric_color_limit": limit, "matrix_order": "y_bin,x_bin",
                      "count_conservation_passed": all(r["in_grid_objects"] + r["outside_grid_objects"] ==
                                                       r["selected_objects"] for r in index),
                      "displayable_bins_by_arm": {arm: int(s.displayable.sum()) for arm, s in summaries.items()},
                      "alignment_preview_sampling": "At most 2000 evenly spaced source-row indices per section; no sampling in counts",
                      "manifest_sha256": manifest_hash,
                      "code_sha256": {str(path.relative_to(PROJECT_ROOT)): sha256_file(path) for path in (
                          Path(__file__), PROJECT_ROOT / "comet_spatial/core.py", PROJECT_ROOT / "comet_spatial/manifest.py")},
                      "generated_utc": datetime.now(timezone.utc).isoformat()}
        save_json(stage / "validation.json", acceptance)
        destination = output_directory / run_name
        shutil.move(str(stage), str(destination))
    save_json(output_directory / "latest_run.json", {"run_directory": str(destination), **acceptance})
    return destination


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=PROJECT_ROOT / "metadata/analysis_manifest.json")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--preflight-report", type=Path, default=PROJECT_ROOT / "outputs/preflight.json")
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "outputs/spatial")
    args = parser.parse_args(argv)
    manifest_path = args.manifest.expanduser().resolve()
    report = preflight_manifest(manifest_path)
    report.update(manifest_path=str(manifest_path), checked_utc=datetime.now(timezone.utc).isoformat())
    manifest, directions = None, None
    if report["status"] == "ready":
        try:
            manifest = load_manifest(manifest_path)
            directions = display_directions(manifest)
        except (OSError, KeyError, TypeError, ValueError) as exc:
            report["status"] = "blocked"
            report["blockers"].append(str(exc))
    save_json(args.preflight_report, report)
    if report["status"] != "ready":
        print("BLOCKED: %d unresolved input requirements; see %s" % (len(report["blockers"]), args.preflight_report))
        return 2
    if args.preflight_only:
        print("READY: supplied input attestations and file hashes pass preflight; scientific alignment inspection remains separate.")
        return 0
    try:
        destination = execute(manifest, manifest_path, args.output_dir.expanduser().resolve(), directions)
    except (OSError, KeyError, TypeError, ValueError, csv.Error) as exc:
        report["status"] = "blocked"
        report["blockers"].append("Execution stopped before publishing a run: " + str(exc))
        save_json(args.preflight_report, report)
        print("BLOCKED: " + str(exc))
        return 2
    print("NUMERICAL RUN COMPLETE: %s; final scientific acceptance pending alignment comparison." % destination)
    return 3


if __name__ == "__main__":
    sys.exit(main())
