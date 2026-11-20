"""Section-level spatial measurements and comparisons on the preserved grid.

Counts/sums retain the explicit assumed-zero policy. Intensive measurements and
fractions are undefined without their requisite objects, and conditions average
defined section values equally rather than pooling objects. These functions do
not infer tissue validity, refit alignment, or add pseudocounts.
"""
from numbers import Real
import numpy as np


MEASUREMENTS = [
    {"id": "pla_count", "label": "PLA count", "units": "PLA count / bin"},
    {"id": "large_pla_count", "label": "Large PLA count", "units": "PLA count / bin", "needsCutoff": True},
    {"id": "small_pla_count", "label": "Small PLA count", "units": "PLA count / bin", "needsCutoff": True},
    {"id": "large_pla_fraction", "label": "Large PLA fraction", "units": "fraction", "needsCutoff": True},
    {"id": "mean_pla_area", "label": "Mean PLA area", "units": "µm² (exported)"},
    {"id": "median_pla_area", "label": "Median PLA area", "units": "µm² (exported)"},
    {"id": "p90_pla_area", "label": "90th-percentile PLA area", "units": "µm² (exported)"},
    {"id": "total_pla_area", "label": "Total PLA area", "units": "µm² (exported)"},
    {"id": "mean_pla_intensity", "label": "Mean PLA intensity", "units": "exported intensity units"},
    {"id": "marker_associated_pla_count", "label": "Marker-associated PLA count", "units": "PLA count / bin", "needsMarker": True},
    {"id": "marker_associated_pla_fraction", "label": "Marker-associated PLA fraction", "units": "fraction", "needsMarker": True},
    {"id": "marker_associated_large_pla_count", "label": "Marker-associated large PLA count", "units": "PLA count / bin", "needsMarker": True, "needsCutoff": True},
    {"id": "marker_associated_pla_mean_area", "label": "Marker-associated PLA mean area", "units": "µm² (exported)", "needsMarker": True},
    {"id": "section_pla_share", "label": "Section PLA share", "units": "% of section PLA", "difference_units": "percentage points"},
    {"id": "marker_associated_pla_area_fraction", "label": "Marker-associated PLA area fraction", "units": "fraction", "needsMarker": True},
    {"id": "median_pla_intensity", "label": "Median PLA intensity", "units": "exported intensity units"},
    {"id": "pla_area_iqr", "label": "PLA area interquartile range", "units": "µm² (exported)"},
    {"id": "pla_area_cv", "label": "PLA area coefficient of variation", "units": "dimensionless CV"},
    {"id": "mean_pla_nearest_neighbor_distance", "label": "Mean PLA nearest-neighbor distance", "units": "exported coordinate units"},
]
ZERO_METRICS = {"pla_count", "large_pla_count", "small_pla_count", "total_pla_area",
                "marker_associated_pla_count", "marker_associated_large_pla_count", "section_pla_share"}
for _measurement in MEASUREMENTS:
    _measurement.update(needsMarker=_measurement.get("needsMarker", False),
                        needsCutoff=_measurement.get("needsCutoff", False),
                        empty_bin_rule="assumed_zero" if _measurement["id"] in ZERO_METRICS else "undefined")
COMPARISONS = [
    {"id": "absolute_difference", "label": "Running − Homecage", "units": "measurement units"},
    {"id": "percent_change", "label": "Percent change relative to Homecage", "units": "%"},
    {"id": "log2_fold_change", "label": "Log2 fold change (Running / Homecage)", "units": "log2 ratio"},
]


def _numbers(values):
    return np.asarray([float(v) if isinstance(v, Real) and not isinstance(v, (bool, np.bool_)) else np.nan
                       for v in values], dtype=float)


def _selected_payload(payload):
    if "grid" in payload:
        return payload, payload.get("pla_points", [])
    width = str(payload.get("default_resolution", "100"))
    return payload["resolutions"][width], payload.get("pla_points", [])


def compare_conditions(running, homecage, comparison="absolute_difference"):
    """Compare condition means; undefined ratios remain missing, without offsets.

    Returns numerical ``values``, boolean ``defined`` and ``missing_reason``
    arrays. Eligibility is a separate caller-owned mask, never inferred here.
    """
    if comparison not in {c["id"] for c in COMPARISONS}:
        raise ValueError("Unknown condition comparison")
    running, homecage = np.asarray(running, float), np.asarray(homecage, float)
    if running.shape != homecage.shape:
        raise ValueError("Condition means must have the same shape")
    valid = np.isfinite(running) & np.isfinite(homecage)
    reasons = np.full(running.shape, None, dtype=object)
    reasons[~np.isfinite(homecage) & ~np.isfinite(running)] = "undefined_both_condition_means"
    reasons[~np.isfinite(homecage) & np.isfinite(running)] = "undefined_homecage_mean"
    reasons[np.isfinite(homecage) & ~np.isfinite(running)] = "undefined_running_mean"
    values = running-homecage
    if comparison == "percent_change":
        reasons[valid & (homecage == 0)] = "zero_homecage_mean"
        valid &= homecage != 0
        values = np.divide(100*values, homecage, out=np.full(running.shape, np.nan), where=valid)
    elif comparison == "log2_fold_change":
        reasons[valid & (homecage <= 0)] = "nonpositive_homecage_mean"
        reasons[valid & (homecage > 0) & (running <= 0)] = "nonpositive_running_mean"
        valid &= (homecage > 0) & (running > 0)
        with np.errstate(divide="ignore", invalid="ignore"):
            values = np.log2(np.divide(running, homecage, out=np.full(running.shape, np.nan), where=valid))
    finite = valid & np.isfinite(values)
    reasons[valid & ~finite] = "nonfinite_comparison"
    return {"values": np.where(finite, values, np.nan), "defined": finite, "missing_reason": reasons}


def _bins(points, grid):
    x, y = _numbers(points["x"]), _numbers(points["y"])
    xe, ye = np.asarray(grid["x_edges"], float), np.asarray(grid["y_edges"], float)
    if len(x) != len(y) or any(a.ndim != 1 or len(a) < 2 or not np.isfinite(a).all() or not (np.diff(a) > 0).all() for a in (xe, ye)):
        raise ValueError("Finite coordinates and strictly increasing recorded bin edges are required")
    ix, iy = np.searchsorted(xe, x, side="right")-1, np.searchsorted(ye, y, side="right")-1
    ix[x == xe[-1]] = len(xe)-2
    iy[y == ye[-1]] = len(ye)-2
    if not np.isfinite(x).all() or not np.isfinite(y).all() or ((ix < 0) | (ix >= len(xe)-1) | (iy < 0) | (iy >= len(ye)-1)).any():
        raise ValueError("Every cached point must lie within the recorded shared grid")
    return iy*(len(xe)-1)+ix, (len(ye)-1, len(xe)-1)


def _section_values(section, points, feature, grid, measurement_id, cutoff, marker):
    shape = (len(grid["y_edges"])-1, len(grid["x_edges"])-1)
    if measurement_id in ("pla_count", "section_pla_share"):
        values = np.asarray(section["pla_counts"], float)
        if values.shape != shape or not np.isfinite(values).all() or (values < 0).any() or not np.equal(values, np.floor(values)).all():
            raise ValueError("PLA counts must be finite nonnegative integer matrices on the recorded grid")
        if measurement_id == "section_pla_share":
            # The denominator is the whole physical section, never just this bin,
            # the condition, the current viewport or a selected-object subset.
            total = section.get("pla_objects", float(values.sum()))
            if isinstance(total, (bool, np.bool_)) or not isinstance(total, Real) or not np.isfinite(total) or total < values.sum() or total != int(total):
                raise ValueError("Section PLA total must be a nonnegative integer at least as large as its grid count")
            return values / total * 100 if total > 0 else np.full(shape, np.nan)
        return values.copy()
    if points is None or feature is None:
        raise ValueError("Complete indexed PLA points and measurement features are required")
    if points.get("source_sha256") and feature.get("source_sha256") != points["source_sha256"]:
        raise ValueError("Measurement feature source hash differs from the point cache")
    flat, shape = _bins(points, grid)
    length, size = len(flat), int(np.prod(shape))
    if len(feature.get("area_um2", [])) != length or len(feature.get("intensity", [])) != length:
        raise ValueError("Feature arrays must index every point exactly once")
    area, intensity = _numbers(feature["area_um2"]), _numbers(feature["intensity"])
    marker_values = feature.get("markers", {}).get(marker, [])
    marker_metric = measurement_id.startswith("marker_associated")
    if marker_metric and len(marker_values) != length:
        raise ValueError("Selected marker flags must index every point exactly once")
    flags = _numbers(marker_values) if len(marker_values) == length else np.full(length, np.nan)
    count = lambda select: np.bincount(flat[select], minlength=size).astype(float)
    n = np.bincount(flat, minlength=size).astype(float)
    if not np.array_equal(n.reshape(shape), np.asarray(section["pla_counts"])):
        raise ValueError("Cached point membership disagrees with saved per-section PLA counts")
    good_area = np.isfinite(area) & (area >= 0)
    bad_area, bad_intensity = count(~good_area), count(~np.isfinite(intensity))
    good_marker = np.isfinite(flags) & np.isin(flags, [0, 1])
    associated = good_marker & (flags == 1)
    bad_marker, n_marker = count(~good_marker), count(associated)
    area_sum = np.bincount(flat[good_area], weights=area[good_area], minlength=size).astype(float)
    large = count(good_area & (area >= cutoff))
    values = np.full(size, np.nan)
    with np.errstate(divide="ignore", invalid="ignore"):
        if measurement_id == "large_pla_count":
            values = large
        elif measurement_id == "small_pla_count":
            values = n-large
        elif measurement_id == "large_pla_fraction":
            values = large/n
        elif measurement_id == "total_pla_area":
            values = area_sum
        elif measurement_id == "mean_pla_area":
            values = area_sum/n
        elif measurement_id in ("median_pla_area", "p90_pla_area", "pla_area_iqr", "median_pla_intensity"):
            # Type-7 linear quantile within each section/bin, never a spatial interpolation.
            selected_values = intensity if measurement_id == "median_pla_intensity" else area
            good = np.isfinite(intensity) if measurement_id == "median_pla_intensity" else good_area
            order = np.lexsort((selected_values[good], flat[good]))
            sorted_bins, sorted_values = flat[good][order], selected_values[good][order]
            occupied, starts, counts = np.unique(sorted_bins, return_index=True, return_counts=True)
            def quantile(q):
                position = (counts-1)*q
                lower, upper = np.floor(position).astype(int), np.ceil(position).astype(int)
                return sorted_values[starts+lower] + (position-lower)*(sorted_values[starts+upper]-sorted_values[starts+lower])
            values[occupied] = quantile(.75)-quantile(.25) if measurement_id == "pla_area_iqr" else quantile(.9 if measurement_id == "p90_pla_area" else .5)
            if measurement_id == "median_pla_intensity":
                values[bad_intensity > 0] = np.nan
        elif measurement_id == "pla_area_cv":
            # Centered two-pass population variance avoids cancellation of E[x²]-E[x]².
            mean = area_sum/n
            deviations = area[good_area]-mean[flat[good_area]]
            variance = np.bincount(flat[good_area], weights=deviations*deviations, minlength=size).astype(float)/n
            values = np.sqrt(variance)/mean
            values[(n < 2) | (mean <= 0)] = np.nan
        elif measurement_id == "mean_pla_intensity":
            good = np.isfinite(intensity)
            values = np.bincount(flat[good], weights=intensity[good], minlength=size)/n
            values[bad_intensity > 0] = np.nan
        elif measurement_id == "mean_pla_nearest_neighbor_distance":
            distances = feature.get("nearest_neighbor_distance", [])
            if len(distances) != length:
                raise ValueError("Nearest-neighbor distances must index every point exactly once")
            distances = _numbers(distances)
            good = np.isfinite(distances) & (distances >= 0)
            values = np.bincount(flat[good], weights=distances[good], minlength=size).astype(float)/n
            values[count(~good) > 0] = np.nan
        elif measurement_id == "marker_associated_pla_count":
            values = n_marker
        elif measurement_id == "marker_associated_pla_fraction":
            values = n_marker/n
        elif measurement_id == "marker_associated_large_pla_count":
            values = count(associated & good_area & (area >= cutoff))
        elif measurement_id == "marker_associated_pla_mean_area":
            good = associated & good_area
            values = np.bincount(flat[good], weights=area[good], minlength=size)/n_marker
        elif measurement_id == "marker_associated_pla_area_fraction":
            good = associated & good_area
            values = np.bincount(flat[good], weights=area[good], minlength=size).astype(float)/area_sum
            values[bad_area > 0] = np.nan
    if measurement_id in ("large_pla_count", "small_pla_count", "large_pla_fraction", "total_pla_area", "mean_pla_area", "median_pla_area", "p90_pla_area", "pla_area_iqr", "pla_area_cv"):
        values[bad_area > 0] = np.nan
    if marker_metric:
        values[bad_marker > 0] = np.nan
        if measurement_id in ("marker_associated_large_pla_count", "marker_associated_pla_mean_area"):
            values[count(associated & ~good_area) > 0] = np.nan
    values[~np.isfinite(values)] = np.nan
    return values.reshape(shape)


def compute_measurement(payload, features, measurement_id, *, area_cutoff=.1, marker="chat", comparison="absolute_difference"):
    """Compute one metric per section/bin, equal-section means, then comparison.

    ``payload`` is the selected resolution with ``pla_points`` attached, or a
    combined multiresolution payload. Eligibility is copied from its arms and
    remains distinct from metric-defined section N. No array is modified.
    """
    catalog = {m["id"]: m for m in MEASUREMENTS}
    comparisons = {c["id"]: c for c in COMPARISONS}
    if measurement_id not in catalog or comparison not in comparisons:
        raise ValueError("Unknown spatial measurement or comparison")
    if isinstance(area_cutoff, (bool, np.bool_)) or not isinstance(area_cutoff, Real) or not np.isfinite(area_cutoff) or area_cutoff < 0:
        raise ValueError("The area cutoff must be a finite nonnegative number")
    selected, points = _selected_payload(payload)
    meta = dict(catalog[measurement_id])
    markers = {m["id"]: m for m in features.get("available_markers", [])}
    if meta["needsMarker"] and marker not in markers:
        raise ValueError("Selected marker is not present in the feature cache")
    if meta["needsMarker"]:
        meta["label"] = meta["label"].replace("Marker-associated", markers[marker]["label"]+"-associated")
    comparison_meta = dict(comparisons[comparison])
    if comparison == "absolute_difference":
        comparison_meta["units"] = meta.get("difference_units", meta["units"])
    point_map = {p["section_id"]: p for p in points}
    feature_map = {f["section_id"]: f for f in features.get("sections", [])}
    if len(point_map) != len(points) or len(feature_map) != len(features.get("sections", [])):
        raise ValueError("Repeated point or feature section identities")
    sections = selected["sections"]
    if len({s["section_id"] for s in sections}) != len(sections):
        raise ValueError("Repeated section identities cannot increase replication")
    computed = []
    for section in sections:
        values = _section_values(section, point_map.get(section["section_id"]), feature_map.get(section["section_id"]), selected["grid"], measurement_id, area_cutoff, marker)
        computed.append({"section_id": section["section_id"], "values": values, "defined": np.isfinite(values)})
    by_id = {s["section_id"]: s for s in computed}
    arms, finite_values = {}, []
    for arm in ("HK1", "PFKP"):
        source_arm = selected["arms"][arm]
        eligible = np.asarray(source_arm["displayable"], bool).copy()
        means, ns = {}, {}
        for condition in ("Homecage", "Running"):
            group = [s for s in sections if s["pla_type"] == arm and s["condition"] == condition]
            if len(group) != 3 or len({s.get("animal_id", s["section_id"]) for s in group}) != 3:
                raise ValueError("Each arm/condition requires three distinct animal sections")
            stack = np.stack([by_id[s["section_id"]]["values"] for s in group])
            valid = np.isfinite(stack)
            ns[condition] = valid.sum(axis=0)
            means[condition] = np.divide(np.where(valid, stack, 0).sum(axis=0), ns[condition],
                out=np.full(eligible.shape, np.nan), where=ns[condition] > 0)
        home, running = means["Homecage"], means["Running"]
        absolute = running-home
        compared = compare_conditions(running, home, comparison)
        reasons = compared["missing_reason"]
        reasons[~eligible] = "outside_display_domain"
        valid = eligible & compared["defined"]
        result = np.where(valid, compared["values"], np.nan)
        finite_values.extend(result[np.isfinite(result)].tolist())
        arms[arm] = {"homecage_mean": np.where(eligible, home, np.nan), "running_mean": np.where(eligible, running, np.nan),
            "homecage_valid_section_n": ns["Homecage"], "running_valid_section_n": ns["Running"],
            "comparison_value": result, "difference": result.copy(), "absolute_difference": np.where(eligible, absolute, np.nan),
            "displayable": valid, "eligibility": eligible, "missing_reason": reasons}
    limit = max((abs(v) for v in finite_values), default=0) or 1.
    return {"measurement": meta, "comparison": comparison_meta, "area_cutoff": float(area_cutoff), "marker": marker,
        "sections": computed, "arms": arms, "coverage_verified": False,
        "eligibility_policy": "Preserved current per-arm display domain; no tissue mask inferred",
        "quantile_method": "type7_linear", "pseudocount": None,
        "color_scale": {"cmin": -limit, "cmax": limit, "center": 0, "shared_across_arms": True,
                        "label": comparison_meta["label"]+" · "+meta["label"], "units": comparison_meta["units"]}}
