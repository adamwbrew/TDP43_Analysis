"""Synthetic acceptance cases, never results from experimental specimens."""
import unittest

import numpy as np
from shapely.geometry import Polygon, box

from comet_spatial.core import (
    FixedTransform, GridSpec, SectionResult, assign_centroid_bins, count_section,
    polygon_tissue_validity, raster_cell_footprints, shared_symmetric_limit,
    summarize_by_arm,
)


def grid(x=(0, 1, 2), y=(0, 1)):
    return GridSpec(x, y, "test_unit", "synthetic_reference", "test_right", "test_up")


class SpatialAcceptanceTests(unittest.TestCase):
    def test_internal_outer_and_corner_boundaries_assigned_once(self):
        g = grid(y=(0, 1, 2))
        xy = [[0, 0], [1, 0], [1, 1], [2, 2], [2, 1], [-1, 1], [2.00001, 1]]
        indices, inside = assign_centroid_bins(xy, g)
        self.assertEqual(indices.tolist(), [[0, 0], [0, 1], [1, 1], [1, 1], [1, 1], [-1, -1], [-1, -1]])
        result = count_section(xy, g, list(range(len(xy))))
        np.testing.assert_array_equal(result.counts, [[1, 1], [0, 3]])
        self.assertEqual((result.total_objects, result.in_grid_objects, result.outside_grid_objects), (7, 5, 2))
        self.assertEqual(int(result.counts.sum()), int(inside.sum()))

    def test_duplicate_object_ids_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            count_section([[0.2, 0.2], [0.3, 0.3]], grid(), ["same", "same"])

    def test_missing_object_id_cannot_be_a_new_detection(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            count_section([[0.2, 0.2]], grid(), [np.nan])

    def test_nonfinite_centroid_is_not_silently_discarded(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            count_section([[np.nan, 0.2]], grid(), ["bad"])

    def test_complete_boundary_inclusion_and_tiny_sliver_exclusion(self):
        g = grid()
        np.testing.assert_array_equal(polygon_tissue_validity(box(0, 0, 2, 1), g), [[True, True]])
        # Far below a typical area tolerance: the strict full-bin rule excludes it.
        sliver = 1e-13
        np.testing.assert_array_equal(polygon_tissue_validity(box(0, 0, 2 - sliver, 1), g), [[True, False]])

    def test_mask_hole_rejects_cell_even_with_center_inside_tissue(self):
        mask = Polygon([(0, 0), (2, 0), (2, 1), (0, 1)],
                       holes=[[(0.1, 0.1), (0.11, 0.1), (0.11, 0.11), (0.1, 0.11)]])
        np.testing.assert_array_equal(polygon_tissue_validity(mask, grid()), [[False, True]])

    def test_invalid_or_absent_mask_fails_instead_of_becoming_zero(self):
        with self.assertRaises(ValueError):
            polygon_tissue_validity(None, grid())
        with self.assertRaisesRegex(ValueError, "valid"):
            polygon_tissue_validity(Polygon([(0, 0), (1, 1), (1, 0), (0, 1)]), grid())

    def test_raster_uses_full_footprints_and_preserves_false_hole(self):
        identity = FixedTransform(((1, 0, 0), (0, 1, 0), (0, 0, 1)))
        pixels = np.ones((3, 3), dtype=bool)
        pixels[1, 1] = False
        geometry = raster_cell_footprints(pixels, [0, 1, 2, 3], [0, 1, 2, 3], identity)
        g = grid(x=(0, 1, 2, 3), y=(0, 1, 2, 3))
        np.testing.assert_array_equal(polygon_tissue_validity(geometry, g), pixels)
        shifted_grid = grid(x=(0.5, 1.5), y=(0.5, 1.5))
        self.assertFalse(polygon_tissue_validity(geometry, shifted_grid)[0, 0])

    def test_raster_no_center_resampling_of_partial_coverage(self):
        identity = FixedTransform(((1, 0, 0), (0, 1, 0), (0, 0, 1)))
        footprint = raster_cell_footprints(np.array([[True]], dtype=bool), [0, 1], [0, 1], identity)
        np.testing.assert_array_equal(polygon_tissue_validity(footprint, grid(x=(0, 1 + 1e-13))), [[False]])

    def test_supplied_transform_applies_identically_to_centroids_and_mask(self):
        transform = FixedTransform(((-1, 0, 3), (0, 1, 2), (0, 0, 1)))
        np.testing.assert_array_equal(transform.points([[0.5, 0.5], [1.5, 0.5]]), [[2.5, 2.5], [1.5, 2.5]])
        g = grid(x=(1, 2, 3), y=(2, 3))
        np.testing.assert_array_equal(polygon_tissue_validity(transform.geometry(box(0, 0, 2, 1)), g), [[True, True]])
        result = count_section(transform.points([[0.5, 0.5]]), g, ["one"])
        np.testing.assert_array_equal(result.counts, [[0, 1]])

    def section(self, label, condition, value, arm="HK1", valid=(True, True)):
        return SectionResult(label, "animal_" + label, "physical_" + label, condition, arm,
                             np.asarray([value], dtype=int), np.asarray([valid], dtype=bool))

    def test_pdf_example_equal_section_means_and_separate_arms(self):
        sections = [self.section("H%d" % i, "Homecage", [n, 0]) for i, n in enumerate((3, 5, 4))]
        sections += [self.section("R%d" % i, "Running", [n, 0]) for i, n in enumerate((7, 8, 9))]
        sections += [self.section("PH", "Homecage", [100, 0], "PFKP"),
                     self.section("PR", "Running", [10, 0], "PFKP")]
        results = summarize_by_arm(sections, grid())
        np.testing.assert_array_equal(results["HK1"].homecage_mean, [[4, 0]])
        np.testing.assert_array_equal(results["HK1"].running_mean, [[8, 0]])
        np.testing.assert_array_equal(results["HK1"].difference, [[4, 0]])
        np.testing.assert_array_equal(results["HK1"].homecage_n, [[3, 3]])
        np.testing.assert_array_equal(results["PFKP"].difference, [[-90, 0]])
        self.assertEqual(shared_symmetric_limit(results), 90)

    def test_valid_zero_is_included_and_missing_tissue_is_excluded(self):
        sections = [self.section("H0", "Homecage", [0, 999], valid=(True, False)),
                    self.section("H1", "Homecage", [10, 999], valid=(True, False)),
                    self.section("R0", "Running", [8, 10], valid=(True, True))]
        result = summarize_by_arm(sections, grid())["HK1"]
        self.assertEqual(result.homecage_mean[0, 0], 5)
        self.assertEqual(result.difference[0, 0], 3)
        np.testing.assert_array_equal(result.homecage_n, [[2, 0]])
        np.testing.assert_array_equal(result.running_n, [[1, 1]])
        self.assertTrue(np.isnan(result.homecage_mean[0, 1]))
        self.assertTrue(np.isnan(result.difference[0, 1]))
        self.assertFalse(result.displayable[0, 1])

    def test_no_opposite_group_support_stays_missing(self):
        result = summarize_by_arm([self.section("R", "Running", [8, 0])], grid())["HK1"]
        self.assertTrue(np.isnan(result.difference).all())
        np.testing.assert_array_equal(result.homecage_n, [[0, 0]])
        with self.assertRaisesRegex(ValueError, "No displayable"):
            shared_symmetric_limit({"HK1": result})

    def test_repeated_physical_section_cannot_be_extra_replication(self):
        first = self.section("A", "Homecage", [1, 0])
        repeat = SectionResult("A_rerun", first.animal_id, first.physical_section_id,
                               first.condition, first.pla_type, first.counts, first.tissue_validity)
        with self.assertRaisesRegex(ValueError, "physical section"):
            summarize_by_arm([first, repeat], grid())

    def test_invalid_grid_and_transform_rejected(self):
        with self.assertRaises(ValueError):
            grid(x=(0, 0, 1))
        with self.assertRaises(ValueError):
            FixedTransform(((1, 0, 0), (0, 1, 0), (0, 0.1, 1)))


if __name__ == "__main__":
    unittest.main()
