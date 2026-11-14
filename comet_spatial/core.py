"""Separate, deterministic spatial steps specified by the new COMET instructions.

All matrices use [y_bin, x_bin]. Counts are object counts per section, never
normalized, smoothed, pooled across PLA types, or treated as animal inference.
Geometry predicates use the supplied mask exactly: no buffer or area tolerance.
"""
from dataclasses import dataclass
from typing import Tuple

import numpy as np
from shapely import affinity
from shapely.geometry import box
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union


@dataclass(frozen=True)
class GridSpec:
    """One explicit aligned grid shared by all sections, conditions and PLA types.

    Numerically lower x/y edges are inclusive and upper edges are exclusive,
    except that the outermost maximum edges are included in the last bin. An
    internal edge belongs to the interval beginning at that edge. A corner is
    assigned once; preserved display flips do not change numeric membership.
    """
    x_edges: Tuple[float, ...]
    y_edges: Tuple[float, ...]
    coordinate_units: str
    reference_space: str
    x_positive: str
    y_positive: str

    def __post_init__(self):
        for name in ("x_edges", "y_edges"):
            values = np.asarray(getattr(self, name), dtype=float)
            if values.ndim != 1 or len(values) < 2:
                raise ValueError("%s needs at least two edges" % name)
            if not np.isfinite(values).all() or not (np.diff(values) > 0).all():
                raise ValueError("%s must be finite and strictly increasing" % name)
            object.__setattr__(self, name, tuple(values.tolist()))
        for name in ("coordinate_units", "reference_space", "x_positive", "y_positive"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip():
                raise ValueError("%s must be explicitly documented" % name)

    @property
    def shape(self):
        return (len(self.y_edges) - 1, len(self.x_edges) - 1)

    def cells(self):
        for iy in range(self.shape[0]):
            for ix in range(self.shape[1]):
                yield iy, ix, box(self.x_edges[ix], self.y_edges[iy],
                                  self.x_edges[ix + 1], self.y_edges[iy + 1])


@dataclass(frozen=True)
class FixedTransform:
    """Apply a supplied accepted affine transform; this class never fits one.

    Column-vector convention: [aligned_x, aligned_y, 1] = matrix @ [x,y,1].
    Identity must be explicitly supplied when coordinates already are aligned.
    Approval is checked by the manifest gate, not inferred from matrix values.
    """
    matrix: Tuple[Tuple[float, ...], ...]

    def __post_init__(self):
        mat = np.asarray(self.matrix, dtype=float)
        if mat.shape != (3, 3) or not np.isfinite(mat).all():
            raise ValueError("Fixed transform must be a finite 3x3 matrix")
        if not np.array_equal(mat[2], [0.0, 0.0, 1.0]):
            raise ValueError("Only explicit affine transforms are supported")
        if np.linalg.det(mat[:2, :2]) == 0:
            raise ValueError("Fixed transform must be invertible")
        object.__setattr__(self, "matrix", tuple(tuple(row) for row in mat.tolist()))

    def points(self, xy):
        coords = _points(xy)
        mat = np.asarray(self.matrix)
        return coords @ mat[:2, :2].T + mat[:2, 2]

    def geometry(self, geometry):
        _valid_mask(geometry)
        m = self.matrix
        result = affinity.affine_transform(geometry, [m[0][0], m[0][1], m[1][0],
                                                       m[1][1], m[0][2], m[1][2]])
        _valid_mask(result)
        return result


def _points(xy):
    values = np.asarray(xy, dtype=float)
    if values.size == 0:
        values = np.empty((0, 2), dtype=float)
    if values.ndim != 2 or values.shape[1] != 2 or not np.isfinite(values).all():
        raise ValueError("Centroids must be finite n-by-2 coordinates; no silent dropping")
    return values


def assign_centroid_bins(aligned_centroids, grid):
    """Return [y,x] integer indices and in-grid flag for each supplied centroid."""
    coords = _points(aligned_centroids)
    ix = np.searchsorted(grid.x_edges, coords[:, 0], side="right") - 1
    iy = np.searchsorted(grid.y_edges, coords[:, 1], side="right") - 1
    ix[coords[:, 0] == grid.x_edges[-1]] = grid.shape[1] - 1
    iy[coords[:, 1] == grid.y_edges[-1]] = grid.shape[0] - 1
    inside = ((coords[:, 0] >= grid.x_edges[0]) & (coords[:, 0] <= grid.x_edges[-1]) &
              (coords[:, 1] >= grid.y_edges[0]) & (coords[:, 1] <= grid.y_edges[-1]))
    indices = np.column_stack([iy, ix]).astype(np.int64)
    indices[~inside] = -1
    return indices, inside


def count_section(aligned_centroids, grid, object_ids):
    """Count unique centroid objects once; retain explicit out-of-grid count.

    Call separately for each physical section and PLA type. Duplicate IDs cause
    an error, since repeat/rerun resolution is a scientific metadata decision.
    """
    coords = _points(aligned_centroids)
    ids = list(object_ids)
    if len(ids) != len(coords):
        raise ValueError("One explicit object ID is required per centroid")
    if any(v is None or str(v).strip() == "" or
           (isinstance(v, (float, np.floating)) and not np.isfinite(v)) for v in ids):
        raise ValueError("Object IDs cannot be missing")
    try:
        unique_count = len(set(ids))
    except TypeError as exc:
        raise ValueError("Object IDs must be scalar identifiers") from exc
    if unique_count != len(ids):
        raise ValueError("Duplicate object IDs: resolve source relationships before counting")
    bins, inside = assign_centroid_bins(coords, grid)
    counts = np.zeros(grid.shape, dtype=np.int64)
    np.add.at(counts, (bins[inside, 0], bins[inside, 1]), 1)
    return SectionCounts(counts=counts, total_objects=len(coords),
                         in_grid_objects=int(inside.sum()),
                         outside_grid_objects=int((~inside).sum()))


@dataclass(frozen=True)
class SectionCounts:
    counts: np.ndarray
    total_objects: int
    in_grid_objects: int
    outside_grid_objects: int


def _valid_mask(mask):
    if not isinstance(mask, BaseGeometry):
        raise ValueError("An explicit existing polygonal mask is required")
    if mask.geom_type not in ("Polygon", "MultiPolygon") or not mask.is_valid:
        raise ValueError("Mask must be valid Polygon/MultiPolygon; no automatic repair")
    if mask.is_empty:
        raise ValueError("Empty mask is unavailable tissue, not a valid zero mask")


def polygon_tissue_validity(aligned_mask, grid):
    """True only when the complete bin is covered by the supplied mask.

    Shapely covers includes a coincident boundary and rejects any exterior bin
    area, however small. Holes remain holes. No rounding, center-point shortcut,
    positive buffer, or approximate area ratio is used.
    """
    _valid_mask(aligned_mask)
    valid = np.zeros(grid.shape, dtype=bool)
    for iy, ix, cell in grid.cells():
        valid[iy, ix] = aligned_mask.covers(cell)
    return valid


def raster_cell_footprints(mask, x_edges, y_edges, supplied_transform):
    """Geometry of true raster cells with explicitly defined full footprints.

    mask[row,column] corresponds to the rectangle bounded by its supplied
    native x/y edges. Edges, not pixel centers, define coverage. No interpolation
    or resampling occurs: union full true-cell polygons, then apply the supplied
    fixed transform. False cells and holes therefore remain excluded.
    """
    raster = np.asarray(mask)
    if raster.dtype != np.bool_ or raster.ndim != 2:
        raise ValueError("Raster mask must be an explicit 2-D boolean array")
    native_grid = GridSpec(tuple(x_edges), tuple(y_edges), "native", "raster", "x", "y")
    if raster.shape != native_grid.shape:
        raise ValueError("Raster shape and explicit cell edges disagree")
    cells = [cell for iy, ix, cell in native_grid.cells() if raster[iy, ix]]
    if not cells:
        raise ValueError("Empty raster mask cannot establish covered tissue")
    return supplied_transform.geometry(unary_union(cells))


@dataclass(frozen=True)
class SectionResult:
    section_id: str
    animal_id: str
    physical_section_id: str
    condition: str
    pla_type: str
    counts: np.ndarray
    tissue_validity: np.ndarray


@dataclass(frozen=True)
class ArmSummary:
    homecage_mean: np.ndarray
    running_mean: np.ndarray
    difference: np.ndarray
    homecage_n: np.ndarray
    running_n: np.ndarray
    displayable: np.ndarray
    section_ids: Tuple[str, ...]


def summarize_by_arm(sections, grid):
    """Equal section means of raw counts with valid zeros and missing support.

    Each section contributes one raw bin count if its own mask fully covers the
    bin. Both means remain missing when their own N=0; a difference additionally
    requires N>=1 independently in each condition. This is descriptive section
    averaging specified by the PDF, not animal-level inferential statistics.
    """
    sections = list(sections)
    if len({s.section_id for s in sections}) != len(sections):
        raise ValueError("Section IDs must be unique")
    keys = [(s.physical_section_id, s.pla_type) for s in sections]
    if len(set(keys)) != len(keys):
        raise ValueError("A physical section/PLA type occurs more than once")
    for s in sections:
        if s.condition not in ("Homecage", "Running") or s.pla_type not in ("HK1", "PFKP"):
            raise ValueError("Explicit supported condition and separate PLA type required")
        count = np.asarray(s.counts)
        valid = np.asarray(s.tissue_validity)
        if count.shape != grid.shape or valid.shape != grid.shape:
            raise ValueError("All section matrices must use the one shared grid")
        if valid.dtype != np.bool_:
            raise ValueError("Tissue validity must be boolean")
        if not np.isfinite(count).all() or (count < 0).any() or not np.equal(count, np.floor(count)).all():
            raise ValueError("Per-section counts must be nonnegative finite integers")
    results = {}
    for arm in ("HK1", "PFKP"):
        group = [s for s in sections if s.pla_type == arm]
        means, ns = {}, {}
        for condition in ("Homecage", "Running"):
            eligible = [s for s in group if s.condition == condition]
            n = np.zeros(grid.shape, dtype=np.int64)
            total = np.zeros(grid.shape, dtype=float)
            for s in eligible:
                n += s.tissue_validity
                total += np.where(s.tissue_validity, s.counts, 0)
            means[condition] = np.divide(total, n, out=np.full(grid.shape, np.nan), where=n > 0)
            ns[condition] = n
        displayable = (ns["Homecage"] >= 1) & (ns["Running"] >= 1)
        difference = np.where(displayable, means["Running"] - means["Homecage"], np.nan)
        results[arm] = ArmSummary(means["Homecage"], means["Running"], difference,
                                  ns["Homecage"], ns["Running"], displayable,
                                  tuple(s.section_id for s in group))
    return results


def shared_symmetric_limit(summaries):
    """One absolute color limit across both arms; 1 only for an all-zero scale."""
    values = [np.abs(s.difference[np.isfinite(s.difference)]) for s in summaries.values()]
    finite = np.concatenate(values) if values else np.empty(0)
    if len(finite) == 0:
        raise ValueError("No displayable differences; cannot create a scientific heatmap")
    maximum = float(finite.max())
    return maximum if maximum > 0 else 1.0
