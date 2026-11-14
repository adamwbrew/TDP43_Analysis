"""Exploratory reconstruction of supplied HALO exports in their native frame.

This module deliberately does not enter the accepted COMET analysis pipeline.
Bounding-box midpoints are display proxies, not measured centroids. Every map
uses one export independently; no tissue validity, registration, condition,
animal assignment or primary biological estimand is inferred.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


PLA_LABEL = "PLA - TRITC_E1"
CHAT_LABEL = "ChAt-50 - FITC_E1"
CHAT_FLAG = "ChAt-50 - FITC_E1 present"
AREA = "Area (µm²)"
MIN_DIAMETER = "Minimum Diameter (µm)"
MAX_DIAMETER = "Maximum Diameter (µm)"
BOXES = ["XMin", "XMax", "YMin", "YMax"]
POINT_COLUMNS = ["id", "x", "y", "xmin", "xmax", "ymin", "ymax", "area",
                 "min_diameter", "max_diameter", "chat_present"]
PARAMETERS = {
    "version": "1.0.0", "bin_widths": [64, 128, 256],
    "bin_width_selection": "Exploratory display choices in unverified native units; not transferred physical calibration or the accepted COMET grid.",
    "grid_origin": "Integer multiples of each width enclosing all exported bounding boxes; each export has independent native extents.",
    "point_caps": {"PLA": 4000, "ChAT": 3000},
    "sampling": "Fixed seeded uniform sample without replacement within each export/class, sorted back to source row order. Class caps avoid overwhelming PLA by the much larger ChAT class; samples are not prevalence estimates.",
    "area_hist_log10_edges": np.linspace(-3, 4, 57).tolist(),
    "ratio_hist_edges": np.linspace(0, 1, 41).tolist(),
    "review_targets": {"bin_width": 128, "top_count_bins_per_export": 5,
                       "low_high_flag_bins_per_export": 3, "minimum_PLA_per_flag_bin": 20,
                       "meaning": "Native windows for manual source-image review only; selected extremes are not prevalence estimates or spatial inference."},
    "morphology_object_review_targets": {
        "invalid_ratio_per_export": 4, "valid_zero_minimum_per_export": 2,
        "minimum_positive_area_per_export": 1, "maximum_area_per_export": 1,
        "selection": "Select PLA source records from the full parsed export before display downsampling. Preserve source order within diameter-QC categories; stable source-order ties for minimum/maximum positive finite area. An object may appear under several review reasons.",
        "meaning": "At most eight targeted selection records per export, not representative samples or unique-object counts. Every reviewed object remains in the raw PLA and ChAT-flag denominators. Ratio-ineligible objects remain eligible for area review when area is finite and positive."
    },
    "diameter_ratio": "minimum / maximum, finite min>=0 and max>0 and min<=max; zero minimum with positive maximum retained.",
    "orientation": "Native screen convention: x increases right and y increases down; no anatomical labels.",
    "boundary_rule": "Lower inclusive, upper exclusive except final maximum edge inclusive; internal boundaries enter the next bin.",
    "zero_semantics": "0 means no selected exported detection midpoint in this rectangular search bin. It is not a tissue-valid zero or evidence of absent tissue.",
    "raw_counts": "All finite ordered boxes contribute once per source row. No smoothing, tissue-area normalization, registration or cross-export pooling.",
    "scientific_status": "Exploratory export QC; not accepted aligned COMET condition-difference maps.",
}


def native_edges(lower, upper, width):
    """Deterministically enclose the full box envelope in width-sized bins."""
    if not all(np.isfinite([lower, upper, width])) or width <= 0 or upper < lower:
        raise ValueError("Finite ordered extents and positive bin width required")
    lo, hi = math.floor(lower / width) * width, math.ceil(upper / width) * width
    if hi <= lo:
        hi = lo + width
    return np.arange(lo, hi + width * 0.5, width, dtype=float)


def midpoint_coordinates(frame):
    """Validate every source box; do not silently discard malformed records."""
    boxes = frame[BOXES].to_numpy(dtype=float)
    if not np.isfinite(boxes).all():
        raise ValueError("Nonfinite native box; explicit QC resolution required")
    if ((boxes[:, 1] < boxes[:, 0]) | (boxes[:, 3] < boxes[:, 2])).any():
        raise ValueError("Reversed native box; explicit QC resolution required")
    return np.column_stack(((boxes[:, 0] + boxes[:, 1]) / 2,
                            (boxes[:, 2] + boxes[:, 3]) / 2))


def raw_grid(xy, x_edges, y_edges):
    """Count a row once; conserve the count including outer-edge detections."""
    xy = np.asarray(xy, dtype=float).reshape((-1, 2))
    if not np.isfinite(xy).all():
        raise ValueError("Finite coordinates required")
    if len(xy) and (((xy[:, 0] < x_edges[0]) | (xy[:, 0] > x_edges[-1]) |
                     (xy[:, 1] < y_edges[0]) | (xy[:, 1] > y_edges[-1])).any()):
        raise ValueError("Native display grid must enclose every selected midpoint")
    counts, _, _ = np.histogram2d(xy[:, 1], xy[:, 0], bins=[y_edges, x_edges])
    if counts.sum() != len(xy):
        raise AssertionError("Grid count conservation failed")
    return counts.astype(np.int64)


def sampled_indices(total, cap, source_key):
    """Stable independent class sample, without replacement or reweighting."""
    if cap < 0 or total < 0:
        raise ValueError("Nonnegative total and cap required")
    seed = int.from_bytes(hashlib.sha256(source_key.encode("utf-8")).digest()[:8], "big")
    return np.sort(np.random.default_rng(seed).choice(total, min(total, cap), replace=False))


def distribution(values, edges, log10=False):
    values = np.asarray(values, dtype=float)
    eligible = np.isfinite(values) & ((values > 0) if log10 else True)
    valid = values[eligible]
    transformed = np.log10(valid) if log10 else valid
    hist, _ = np.histogram(transformed, bins=edges)
    quantiles = np.quantile(valid, [0, .01, .25, .5, .75, .99, 1]).tolist() if len(valid) else [None] * 7
    return {"n": int(len(valid)), "excluded": int((~eligible).sum()),
            "quantile_probabilities": [0, .01, .25, .5, .75, .99, 1],
            "quantiles": quantiles, "hist_edges": list(edges),
            "quantiles_named": {k: float(v) for k, v in zip(["q05", "q25", "q50", "q75", "q95"], np.quantile(valid, [.05,.25,.5,.75,.95]))} if len(valid) else {k: None for k in ["q05", "q25", "q50", "q75", "q95"]},
            "hist_counts": hist.tolist(), "hist_underflow": int((transformed < edges[0]).sum()),
            "hist_overflow": int((transformed > edges[-1]).sum()),
            "hist_axis": "log10(exported area)" if log10 else "minimum / maximum diameter"}


def morphology_summary(frame):
    minimum = frame[MIN_DIAMETER].to_numpy(dtype=float)
    maximum = frame[MAX_DIAMETER].to_numpy(dtype=float)
    eligible = (np.isfinite(minimum) & np.isfinite(maximum) & (minimum >= 0) &
                (maximum > 0) & (minimum <= maximum))
    ratio = minimum[eligible] / maximum[eligible]
    shape = distribution(ratio, PARAMETERS["ratio_hist_edges"])
    shape["excluded"] = int((~eligible).sum())
    return {"area": distribution(frame[AREA], PARAMETERS["area_hist_log10_edges"], log10=True),
            "diameter_ratio": shape, "ratio_eligible": int(eligible.sum()),
            "ratio_excluded": int((~eligible).sum()),
            "zero_min_diameter": int((minimum == 0).sum()),
            "nonpositive_max_diameter": int((maximum <= 0).sum()),
            "both_zero_diameters": int(((minimum == 0) & (maximum == 0)).sum()),
            "zero_min_retained_in_ratio": int(((minimum == 0) & eligible).sum()),
            "scope": "Descriptive exported measurements only; exclusions apply to the diameter ratio, never counts or ChAT flag summaries."}


def _json_rows(values):
    result = np.asarray(values, dtype=object).tolist()
    for row in result:
        for i, value in enumerate(row):
            if isinstance(value, (float, np.floating)) and not np.isfinite(value):
                row[i] = None
            elif isinstance(value, np.generic):
                row[i] = value.item()
    return result


def export_payload(frame, record, widths=None, point_caps=None):
    """Create full-count matrices and separate, explicitly sampled overlays."""
    widths = PARAMETERS["bin_widths"] if widths is None else list(widths)
    point_caps = PARAMETERS["point_caps"] if point_caps is None else point_caps
    xy = midpoint_coordinates(frame)
    labels = frame["Object Type"].to_numpy()
    unknown = sorted(set(labels) - {PLA_LABEL, CHAT_LABEL})
    if unknown:
        raise ValueError("Unexpected object classes need an explicit adapter: %s" % unknown)
    classes = {"PLA": labels == PLA_LABEL, "ChAT": labels == CHAT_LABEL}
    flags = frame[CHAT_FLAG].to_numpy(dtype=float)
    positive = classes["PLA"] & (flags == 1)
    negative = classes["PLA"] & (flags == 0)
    pla_n = int(classes["PLA"].sum())
    if frame["Object Id"].duplicated().any():
        raise ValueError("Object IDs repeat within this export; resolve before display sampling")
    boxes = frame[BOXES].to_numpy(dtype=float)
    extent = [float(boxes[:, 0].min()), float(boxes[:, 1].max()),
              float(boxes[:, 2].min()), float(boxes[:, 3].max())]
    result = {"file_id": record["file_id"], "job_id": record.get("job_token_from_filename", ""),
              "filename": record.get("relative_path", ""), "source_sha256": record.get("sha256", ""),
              "row_count": len(frame), "analysis_regions": sorted(frame["Analysis Region"].unique().tolist()),
              "class_counts": {key: int(mask.sum()) for key, mask in classes.items()}, "extent": extent,
              "association": {"pla_total": pla_n, "chat_positive": int(positive.sum()),
                              "chat_negative": int(negative.sum()),
                              "chat_other": pla_n - int(positive.sum()) - int(negative.sum()),
                              "percent_chat_positive": 100 * int(positive.sum()) / pla_n if pla_n else None,
                              "definition": "100 × PLA-labeled rows with exported ChAT flag=1 / all PLA-labeled rows in this export; descriptive export QC, no group contrast."},
              "morphology": {}, "grids": {}, "points": {"columns": POINT_COLUMNS}}
    for width in widths:
        ex = native_edges(extent[0], extent[1], width)
        ey = native_edges(extent[2], extent[3], width)
        grids = {"pla": classes["PLA"], "chat": classes["ChAT"],
                 "pla_chat_positive": positive, "pla_chat_negative": negative}
        result["grids"][str(width)] = {"x_edges": ex.tolist(), "y_edges": ey.tolist(),
                                        **{key: raw_grid(xy[mask], ex, ey).tolist() for key, mask in grids.items()}}
    for key, mask in classes.items():
        subset = frame.loc[mask]
        result["morphology"][key] = morphology_summary(subset)
        idx = sampled_indices(len(subset), point_caps[key], record["file_id"] + ":" + key)
        displayed = subset.iloc[idx]
        coords = xy[mask][idx]
        values = np.column_stack([displayed["Object Id"].to_numpy(), coords,
                                  displayed[BOXES + [AREA, MIN_DIAMETER, MAX_DIAMETER, CHAT_FLAG]].to_numpy()])
        rows = _json_rows(values)
        for row in rows:
            row[0] = int(row[0])
        result["points"][key] = rows
    return result


def duplicate_review(root, exports):
    path = root / "outputs/inventory/within_input_overlap.csv"
    if not path.exists():
        return []
    overlaps = pd.read_csv(path)
    lookup = {e["file_id"]: e for e in exports}
    reviews = []
    for row in overlaps.to_dict("records"):
        if not row["measurement_signatures_shared_excluding_region_and_object_id"]:
            continue
        left, right = lookup[row["left_file_id"]], lookup[row["right_file_id"]]
        reviews.append({**row,
            "left_job_id": left["job_id"], "right_job_id": right["job_id"],
            "left_pla_count": left["class_counts"]["PLA"], "right_pla_count": right["class_counts"]["PLA"],
            "pla_count_right_minus_left": right["class_counts"]["PLA"] - left["class_counts"]["PLA"],
            "left_chat_positive_percent": left["association"]["percent_chat_positive"],
            "right_chat_positive_percent": right["association"]["percent_chat_positive"],
            "interpretation": "Candidate overlapping export analyses established by exact exported measurement-signature overlap. Count/flag differences describe exports and may reflect analysis extent or detection differences; not independent samples, treatment effects or accepted object matches.",
            "evidence_source": "outputs/inventory/within_input_overlap.csv",
            "identity_status": "Unapproved source relationship; do not pool or deduplicate biological objects automatically."})
    return reviews


def save_figures(payload, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm
    from matplotlib.lines import Line2D
    from matplotlib.ticker import FuncFormatter, MaxNLocator
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False})
    output = output / "figures"
    output.mkdir(parents=True, exist_ok=True)
    maps = payload["exports"]
    formatter = FuncFormatter(lambda value, pos: "%gk" % (value / 1000))
    maximum = max(np.max(e["grids"]["128"]["pla"]) for e in maps)
    cm = plt.get_cmap("magma").copy()
    cm.set_bad("#eef1f4")
    norm = LogNorm(vmin=1, vmax=max(2, maximum))
    fig, axes = plt.subplots(2, 4, figsize=(18, 10.7))
    fig.subplots_adjust(top=.86, bottom=.16, left=.055, right=.91, hspace=.35, wspace=.28)
    for ax, export in zip(axes.flat, maps):
        grid = export["grids"]["128"]
        mat = np.asarray(grid["pla"])
        display = np.ma.masked_equal(mat, 0)
        picture = ax.imshow(display, extent=[grid["x_edges"][0], grid["x_edges"][-1], grid["y_edges"][-1], grid["y_edges"][0]],
                            cmap=cm, norm=norm, interpolation="nearest", aspect="equal")
        ax.set_title("%s · job %s\n%s PLA detections" % (export["file_id"], export["job_id"], format(export["class_counts"]["PLA"], ",")), loc="left", fontsize=10)
        ax.xaxis.set_major_formatter(formatter)
        ax.yaxis.set_major_formatter(formatter)
        ax.xaxis.set_major_locator(MaxNLocator(3))
        ax.yaxis.set_major_locator(MaxNLocator(4))
        ax.set_xlabel("native X (unverified units)", fontsize=9)
        ax.set_ylabel("native Y ↓", fontsize=9)
        ax.tick_params(labelsize=8)
    cax = fig.add_axes([.93, .29, .012, .4])
    fig.colorbar(picture, cax=cax, label="PLA detections / 128 × 128 native-unit bin\nShared logarithmic display scale; raw unsmoothed counts")
    fig.suptitle("Where are the exported PLA detections?", x=.055, y=.97, ha="left", fontsize=22, fontweight="bold")
    fig.text(.055, .91, "Eight separately reconstructed exports · all rows counted · bounding-box midpoints, not microscopy pixels or measured centroids", fontsize=11)
    fig.text(.055, .075, "Read the color as detection count at a fixed bin width. Native aspect and source offsets are preserved; x→ / y↓ are screen axes.\nPale gray = zero exported midpoints in that search bin, NOT a tissue mask or a tissue-valid zero. No alignment or group comparison.\nNext: compare candidate export repeats and inspect original images; accepted masks, transforms and sample metadata are still required for COMET differences.", fontsize=10, linespacing=1.55)
    for ext in ["png", "svg"]:
        fig.savefig(output / ("native_pla_count_atlas." + ext), dpi=300, facecolor="white")
    plt.close(fig)
    fig, axes = plt.subplots(2, 4, figsize=(18, 10.7))
    fig.subplots_adjust(top=.84, bottom=.16, left=.055, right=.98, hspace=.35, wspace=.28)
    for ax, export in zip(axes.flat, maps):
        chat = np.asarray(export["points"]["ChAT"], dtype=float)
        pla = np.asarray(export["points"]["PLA"], dtype=float)
        ax.scatter(chat[:, 1], chat[:, 2], s=.9, color="#b5c4d1", alpha=.45, rasterized=True, linewidths=0)
        flag = pla[:, -1] == 1
        ax.scatter(pla[~flag, 1], pla[~flag, 2], s=1.6, color="#009eac", alpha=.7, rasterized=True, linewidths=0)
        ax.scatter(pla[flag, 1], pla[flag, 2], s=1.6, color="#bc427a", alpha=.7, rasterized=True, linewidths=0)
        ax.set_xlim(export["extent"][:2]); ax.set_ylim(export["extent"][3], export["extent"][2]); ax.set_aspect("equal")
        ax.set_title("%s · job %s\n%.1f%% of all PLA have ChAT flag=1" % (export["file_id"], export["job_id"], export["association"]["percent_chat_positive"]), loc="left", fontsize=10)
        ax.xaxis.set_major_formatter(formatter); ax.yaxis.set_major_formatter(formatter)
        ax.xaxis.set_major_locator(MaxNLocator(3)); ax.yaxis.set_major_locator(MaxNLocator(4))
        ax.set_xlabel("native X (unverified units)", fontsize=9); ax.set_ylabel("native Y ↓", fontsize=9); ax.tick_params(labelsize=8)
    fig.suptitle("PLA and ChAT detections in their native coordinate frame", x=.055, y=.97, ha="left", fontsize=20, fontweight="bold")
    fig.text(.055, .91, "Deterministic per-class display samples · source boxes retained for review · summaries use every exported PLA row", fontsize=11)
    legends = [Line2D([], [], marker="o", linestyle="", markersize=6, color=c, label=l) for c,l in [("#b5c4d1", "ChAT-labeled detections"), ("#009eac", "PLA: ChAT flag=0"), ("#bc427a", "PLA: ChAT flag=1")]]
    fig.legend(handles=legends, loc="upper left", bbox_to_anchor=(.05,.89), ncol=3, frameon=False)
    fig.text(.055, .075, "Up to 4,000 PLA and 3,000 ChAT points are shown per export. Class-balanced display sampling is not a prevalence estimate.\nMidpoint overlap is not physical colocalization or neuronal identity; exported ChAT flags depend on the HALO algorithm and acquisition.\nCandidate repeat analyses remain separate. Native views require no registration, but cannot establish anatomical correspondence or condition differences.", fontsize=10, linespacing=1.55)
    for ext in ["png", "svg"]:
        fig.savefig(output / ("native_layer_overlay_atlas." + ext), dpi=300, facecolor="white")
    plt.close(fig)


def source_review_targets(exports):
    """Select explicit high-count/flag-extreme windows for scientist review.

    A rectangular exported-search window is not asserted to contain valid
    tissue. Selection is intentionally extreme and supplies no p-value or CI.
    """
    records = []
    settings = PARAMETERS["review_targets"]
    for export in exports:
        grid = export["grids"][str(settings["bin_width"])]
        counts = np.asarray(grid["pla"], dtype=int)
        positive = np.asarray(grid["pla_chat_positive"], dtype=int)
        eligible = np.flatnonzero(counts.ravel() >= settings["minimum_PLA_per_flag_bin"])
        rate = np.divide(positive, counts, out=np.full(counts.shape, np.nan), where=counts > 0)
        nonzero = np.flatnonzero(counts.ravel() > 0)
        top = sorted(nonzero.tolist(), key=lambda i: (-counts.ravel()[i], i))[:settings["top_count_bins_per_export"]]
        lows = sorted(eligible.tolist(), key=lambda i: (rate.ravel()[i], -counts.ravel()[i], i))[:settings["low_high_flag_bins_per_export"]]
        highs = sorted(eligible.tolist(), key=lambda i: (-rate.ravel()[i], -counts.ravel()[i], i))[:settings["low_high_flag_bins_per_export"]]
        for category, selected in [("high_raw_PLA_count", top), ("low_ChAT_flag_fraction_min20_PLA", lows), ("high_ChAT_flag_fraction_min20_PLA", highs)]:
            for rank, flat in enumerate(selected, 1):
                iy, ix = np.unravel_index(flat, counts.shape)
                records.append({"file_id": export["file_id"], "job_id": export["job_id"],
                    "source_filename": export["filename"], "source_sha256": export["source_sha256"],
                    "review_reason": category, "rank_within_reason": rank, "x_bin": int(ix), "y_bin": int(iy),
                    "xmin": grid["x_edges"][ix], "xmax": grid["x_edges"][ix+1],
                    "ymin": grid["y_edges"][iy], "ymax": grid["y_edges"][iy+1],
                    "PLA_count": int(counts[iy, ix]), "PLA_ChAT_flag_positive": int(positive[iy, ix]),
                    "PLA_ChAT_flag_fraction": float(rate[iy, ix]), "ChAT_count": int(grid["chat"][iy][ix]),
                    "coordinate_units": "unverified native export units", "coordinate_proxy": "bounding-box midpoint",
                    "tissue_coverage_status": "unknown; rectangular exported-search bin, no tissue mask supplied",
                    "scientific_status": "Selected extreme for manual image/segmentation review, not a biological inference or representative sample"})
    return records


def morphology_object_review_targets(frame, record):
    """Select actual PLA records for microscopy review from the FULL export.

    Returned rows are review selections: the same source object can carry more
    than one reason. No counts, morphology values or eligibility are modified.
    Source row indices are zero-based data-record positions; CSV record numbers
    include the single header record, and are not necessarily text line numbers.
    """
    xy = midpoint_coordinates(frame)
    is_pla = frame["Object Type"].eq(PLA_LABEL).to_numpy()
    minimum = frame[MIN_DIAMETER].to_numpy(dtype=float)
    maximum = frame[MAX_DIAMETER].to_numpy(dtype=float)
    area = frame[AREA].to_numpy(dtype=float)
    eligible = (np.isfinite(minimum) & np.isfinite(maximum) & (minimum >= 0) &
                (maximum > 0) & (minimum <= maximum))
    source_positions = np.flatnonzero(is_pla)
    usable_area = source_positions[np.isfinite(area[source_positions]) & (area[source_positions] > 0)]
    settings = PARAMETERS["morphology_object_review_targets"]
    invalid = np.flatnonzero(is_pla & ~eligible)[:settings["invalid_ratio_per_export"]]
    zero_minimum = np.flatnonzero(is_pla & eligible & (minimum == 0))[:settings["valid_zero_minimum_per_export"]]
    area_low = sorted(usable_area.tolist(), key=lambda i: (area[i], i))[:settings["minimum_positive_area_per_export"]]
    area_high = sorted(usable_area.tolist(), key=lambda i: (-area[i], i))[:settings["maximum_area_per_export"]]
    selections = [
        ("diameter_ratio_ineligible_inspect_measurement_and_segmentation", invalid),
        ("zero_minimum_positive_maximum_retained_ratio_zero", zero_minimum),
        ("smallest_positive_finite_exported_PLA_area", area_low),
        ("largest_positive_finite_exported_PLA_area", area_high),
    ]

    def finite_or_none(value):
        return float(value) if np.isfinite(value) else None

    result = []
    for reason, positions in selections:
        for rank, position in enumerate(positions, 1):
            source = frame.iloc[position]
            result.append({
                "file_id": record["file_id"], "job_id": record.get("job_token_from_filename", ""),
                "source_filename": record.get("relative_path", ""), "source_sha256": record.get("sha256", ""),
                "source_row_index_zero_based": int(position),
                "source_csv_record_number_including_header": int(position) + 2,
                "object_id": int(source["Object Id"]), "object_type": str(source["Object Type"]),
                "exported_analysis_region": str(source["Analysis Region"]),
                "review_reason": reason, "rank_within_reason": rank,
                "xmin": float(source["XMin"]), "xmax": float(source["XMax"]),
                "ymin": float(source["YMin"]), "ymax": float(source["YMax"]),
                "x_midpoint": float(xy[position, 0]), "y_midpoint": float(xy[position, 1]),
                "exported_area": finite_or_none(area[position]),
                "minimum_diameter": finite_or_none(minimum[position]),
                "maximum_diameter": finite_or_none(maximum[position]),
                "diameter_ratio_minimum_over_maximum": float(minimum[position] / maximum[position]) if eligible[position] else None,
                "diameter_ratio_eligible": bool(eligible[position]),
                "exported_ChAT_flag": finite_or_none(float(source[CHAT_FLAG])),
                "retained_in_raw_PLA_count": True,
                "coordinate_units": "unverified native export units",
                "area_units": "µm² in export header; calibration unverified",
                "diameter_units": "µm in export header; calibration unverified",
                "coordinate_proxy": "bounding-box midpoint, not a measured centroid",
                "selection_scope": "Full export PLA records, not the displayed point sample. Selection records may repeat one source object under several reasons.",
                "scientific_status": "Targeted original-image/segmentation QC; not representative sampling or biological inference",
            })
    return result


def build(root=None, figures=True):
    root = Path(__file__).resolve().parents[1] if root is None else root
    root = Path(root).resolve()
    records = json.loads((root / "metadata/input_manifest.json").read_text())
    exports = []
    morphology_targets = []
    usecols = ["Object Id", "Object Type", "Analysis Region", CHAT_FLAG, AREA, MIN_DIAMETER, MAX_DIAMETER] + BOXES
    for record in records:
        path = Path(record["source_path"])
        if not path.is_file():
            path = root / "Initial Data" / record["relative_path"]
        if path.stat().st_size != record["size_bytes"]:
            raise ValueError("Input size differs from hashed inventory: " + str(path))
        frame = pd.read_csv(path, usecols=usecols, encoding="utf-8-sig")
        if len(frame) != record["row_count"]:
            raise ValueError("Input row count differs from inventory")
        exports.append(export_payload(frame, record))
        morphology_targets.extend(morphology_object_review_targets(frame, record))
        print("Reconstructed %s: %s rows" % (record["file_id"], format(len(frame), ",")), flush=True)
    output = root / "outputs/native_atlas"
    output.mkdir(parents=True, exist_ok=True)
    payload = {"schema_version": "1.0", "analysis_scope": PARAMETERS["scientific_status"],
        "coordinate_definition": "[(XMin+XMax)/2,(YMin+YMax)/2], bbox midpoint proxy. Native x-right/y-down screen convention; units unverified; no alignment.",
        "grid_semantics": PARAMETERS["zero_semantics"], "parameters": PARAMETERS,
        "summary": {"export_count": len(exports), "rows_including_possible_repeats": sum(e["row_count"] for e in exports),
                    "pla_rows_including_possible_repeats": sum(e["class_counts"]["PLA"] for e in exports),
                    "biological_sample_size": None, "biological_sample_size_status": "Unconfirmed for this study; exports are not biological replicates.",
                    "scientific_condition_maps_generated": False}, "exports": exports,
        "duplicate_review": duplicate_review(root, exports)}
    payload["review_targets"] = source_review_targets(exports)
    payload["morphology_object_review_targets"] = morphology_targets
    (output / "payload.json").write_text(json.dumps(payload, separators=(",", ":"), allow_nan=False))
    (root / "metadata/native_atlas_parameters.json").write_text(json.dumps(PARAMETERS, indent=2) + "\n")
    summaries = [{"file_id": e["file_id"], "job_id": e["job_id"], "rows": e["row_count"],
        "PLA": e["class_counts"]["PLA"], "ChAT": e["class_counts"]["ChAT"],
        "PLA_ChAT_flag_positive": e["association"]["chat_positive"],
        "PLA_ChAT_flag_percent": e["association"]["percent_chat_positive"],
        "PLA_area_median_header_um2_calibration_unverified": e["morphology"]["PLA"]["area"]["quantiles"][3],
        "PLA_ratio_excluded": e["morphology"]["PLA"]["ratio_excluded"],
        "PLA_zero_min_diameter": e["morphology"]["PLA"]["zero_min_diameter"],
        "PLA_both_zero_diameters": e["morphology"]["PLA"]["both_zero_diameters"]} for e in exports]
    pd.DataFrame(summaries).to_csv(output / "export_summary.csv", index=False)
    pd.DataFrame(payload["duplicate_review"]).to_csv(output / "candidate_repeat_review.csv", index=False)
    pd.DataFrame(payload["review_targets"]).to_csv(output / "review_targets.csv", index=False)
    pd.DataFrame(payload["morphology_object_review_targets"]).to_csv(output / "morphology_object_review_targets.csv", index=False)
    if figures:
        save_figures(payload, output)
    validation = {"schema_version": "1.0", "all_export_rows_reconciled_to_inventory": True,
        "all_grids_count_conserved": all(sum(sum(row) for row in g["pla"]) == e["class_counts"]["PLA"] and sum(sum(row) for row in g["chat"]) == e["class_counts"]["ChAT"] for e in exports for g in e["grids"].values()),
        "inputs_opened_read_only": True, "raw_hashes": "Reused full SHA-256 inventory records; this run checked sizes and row counts without redundant input rehash.",
        "tissue_masks_generated": False, "transforms_fitted": False, "conditions_assigned": False,
        "biological_comparisons_performed": False, "all_morphology_exclusions_retained_in_counts": True,
        "morphology_review_selected_from_full_exports": True,
        "morphology_review_selection_records": len(morphology_targets),
        "payload_bytes": (output / "payload.json").stat().st_size}
    (output / "validation.json").write_text(json.dumps(validation, indent=2) + "\n")
    print(json.dumps(validation, indent=2))
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--no-figures", action="store_true")
    args = parser.parse_args()
    build(args.root, figures=not args.no_figures)


if __name__ == "__main__":
    main()
