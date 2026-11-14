"""Native reconstruction invariants; fixtures never stand in for tissue masks."""
import unittest
import numpy as np
import pandas as pd
from comet_spatial.native_atlas import (AREA, BOXES, CHAT_FLAG, CHAT_LABEL, MIN_DIAMETER,
    MAX_DIAMETER, PLA_LABEL, PARAMETERS, export_payload, midpoint_coordinates,
    morphology_summary, native_edges, raw_grid, sampled_indices, source_review_targets,
    morphology_object_review_targets)


class NativeAtlasTests(unittest.TestCase):
    def frame(self):
        return pd.DataFrame({"Object Id": [0, 1, 2, 3],
            "Object Type": [PLA_LABEL, PLA_LABEL, PLA_LABEL, CHAT_LABEL],
            "Analysis Region": ["unconfirmed text"] * 4,
            CHAT_FLAG: [1, 0, 1, 1], AREA: [.25, .5, 1, 2],
            MIN_DIAMETER: [0, 0, 1, 2], MAX_DIAMETER: [0, 2, 2, 4],
            "XMin": [0, 2, 4, 6], "XMax": [2, 4, 6, 8],
            "YMin": [0, 2, 4, 6], "YMax": [2, 4, 6, 8]})

    def payload(self):
        return export_payload(self.frame(), {"file_id": "synthetic"}, widths=[2, 4],
                              point_caps={"PLA": 2, "ChAT": 1})

    def test_all_source_rows_conserved_for_each_class_and_width(self):
        payload = self.payload()
        for grid in payload["grids"].values():
            self.assertEqual(np.asarray(grid["pla"]).sum(), 3)
            self.assertEqual(np.asarray(grid["chat"]).sum(), 1)
            self.assertEqual(np.asarray(grid["pla_chat_positive"]).sum(), 2)
            self.assertEqual(np.asarray(grid["pla_chat_negative"]).sum(), 1)
        self.assertEqual(payload["association"]["percent_chat_positive"], 100 * 2 / 3)

    def test_internal_edges_and_outer_max_are_counted_once(self):
        matrix = raw_grid(np.array([[0, 0], [2, 2], [4, 4]]), [0, 2, 4], [0, 2, 4])
        np.testing.assert_array_equal(matrix, [[1, 0], [0, 2]])
        with self.assertRaises(ValueError):
            raw_grid([[5, 0]], [0, 2, 4], [0, 2, 4])

    def test_class_balanced_samples_are_reproducible_unique_and_bounded(self):
        first = sampled_indices(1000, 20, "same source")
        np.testing.assert_array_equal(first, sampled_indices(1000, 20, "same source"))
        self.assertEqual(len(set(first)), 20)
        self.assertFalse(np.array_equal(first, sampled_indices(1000, 20, "other source")))
        self.assertEqual([len(self.payload()["points"][k]) for k in ["PLA", "ChAT"]], [2, 1])

    def test_bad_boxes_and_repeated_object_ids_fail_without_silent_drop(self):
        frame = self.frame()
        frame.loc[0, "XMax"] = -1
        with self.assertRaises(ValueError): midpoint_coordinates(frame)
        frame = self.frame()
        frame.loc[1, "Object Id"] = 0
        with self.assertRaises(ValueError): export_payload(frame, {"file_id": "synthetic"})

    def test_zero_diameter_exclusion_affects_ratio_only(self):
        payload = self.payload()
        morph = payload["morphology"]["PLA"]
        self.assertEqual(morph["ratio_excluded"], 1)
        self.assertEqual(morph["zero_min_retained_in_ratio"], 1)
        self.assertEqual(morph["area"]["n"], 3)
        self.assertEqual(payload["class_counts"]["PLA"], 3)
        self.assertEqual(morph["diameter_ratio"]["quantiles"][0], 0)

    def test_native_extent_is_full_envelope_and_never_supplies_anatomy(self):
        edges = native_edges(1, 7, 2)
        np.testing.assert_array_equal(edges, [0, 2, 4, 6, 8])
        payload = self.payload()
        self.assertEqual(payload["extent"], [0, 8, 0, 8])
        for absent in ["tissue_validity", "condition", "animal_id", "aligned_coordinates"]:
            self.assertNotIn(absent, payload)
        self.assertIn("not a tissue-valid zero", PARAMETERS["zero_semantics"])

    def test_selected_flag_extremes_require_recorded_full_count_support(self):
        export = export_payload(self.frame(), {"file_id": "synthetic"}, widths=[128])
        targets = source_review_targets([export])
        self.assertEqual(len(targets), 1)  # no fraction targets below 20 PLA
        self.assertEqual(targets[0]["PLA_count"], 3)
        self.assertEqual(targets[0]["PLA_ChAT_flag_positive"], 2)
        self.assertAlmostEqual(targets[0]["PLA_ChAT_flag_fraction"], 2 / 3)
        self.assertIn("no tissue mask", targets[0]["tissue_coverage_status"])

    def test_morphology_review_uses_full_source_records_and_keeps_count_denominator(self):
        frame = self.frame()
        record = {"file_id": "synthetic", "relative_path": "fixture.csv", "sha256": "fixture-only"}
        original = frame.copy(deep=True)
        export = export_payload(frame, record, widths=[128], point_caps={"PLA": 0, "ChAT": 0})
        targets = morphology_object_review_targets(frame, record)
        reasons = {row["review_reason"]: row for row in targets}
        invalid = reasons["diameter_ratio_ineligible_inspect_measurement_and_segmentation"]
        self.assertEqual(invalid["object_id"], 0)
        self.assertIsNone(invalid["diameter_ratio_minimum_over_maximum"])
        self.assertEqual(invalid["source_row_index_zero_based"], 0)
        self.assertEqual(invalid["source_csv_record_number_including_header"], 2)
        retained = reasons["zero_minimum_positive_maximum_retained_ratio_zero"]
        self.assertEqual(retained["object_id"], 1)
        self.assertEqual(retained["diameter_ratio_minimum_over_maximum"], 0)
        self.assertEqual(reasons["largest_positive_finite_exported_PLA_area"]["object_id"], 2)
        self.assertTrue(all(row["retained_in_raw_PLA_count"] for row in targets))
        self.assertEqual(export["class_counts"]["PLA"], 3)
        self.assertEqual(export["association"]["pla_total"], 3)
        self.assertEqual(export["points"]["PLA"], [])
        self.assertEqual(targets, morphology_object_review_targets(frame, record))
        pd.testing.assert_frame_equal(frame, original)


if __name__ == "__main__":
    unittest.main()
