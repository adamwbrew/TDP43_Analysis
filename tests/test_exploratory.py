"""Fictional acceptance cases for explicitly limited exploratory support."""
import csv
import gzip
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from comet_spatial.core import GridSpec
from comet_spatial.exploratory import CHAT_CLASS, PLA_CLASS, count_raw_section, summarize_observed_sections
from comet_spatial.manifest import sha256_file


def grid():
    return GridSpec((0, 1, 2), (0, 1), "fictional_units", "fictional_frame", "x", "y")


def section(sid, condition, pla, chat, arm="HK1"):
    return {"section_id": sid, "physical_section_id": "physical_" + sid, "animal_id": "animal_" + sid,
            "condition": condition, "pla_type": arm, "pla_counts": np.asarray([pla], dtype=int),
            "chat_counts": np.asarray([chat], dtype=int)}


class ExploratoryAcceptanceTests(unittest.TestCase):
    def test_chat_only_zero_increases_support_but_empty_bin_stays_missing(self):
        rows = [section("H", "Homecage", [0, 0], [5, 0]), section("R", "Running", [2, 3], [0, 0])]
        hk1 = summarize_observed_sections(rows, grid())["HK1"]
        self.assertEqual(hk1["homecage_mean"][0, 0], 0)
        self.assertEqual(hk1["homecage_n"][0, 0], 1)
        self.assertEqual(hk1["difference"][0, 0], 2)
        self.assertEqual(hk1["homecage_n"][0, 1], 0)
        self.assertTrue(np.isnan(hk1["difference"][0, 1]))
        self.assertFalse(hk1["displayable"][0, 1])

    def test_equal_section_means_pdf_arithmetic_and_arms_separate(self):
        rows = [section("H%d" % i, "Homecage", [n, 0], [0, 1]) for i, n in enumerate((3, 5, 4))]
        rows += [section("R%d" % i, "Running", [n, 0], [0, 1]) for i, n in enumerate((7, 8, 9))]
        rows += [section("PH", "Homecage", [100, 0], [0, 1], "PFKP"),
                 section("PR", "Running", [10, 0], [0, 1], "PFKP")]
        result = summarize_observed_sections(rows, grid())
        np.testing.assert_array_equal(result["HK1"]["difference"], [[4, 0]])
        np.testing.assert_array_equal(result["HK1"]["homecage_n"], [[3, 3]])
        np.testing.assert_array_equal(result["PFKP"]["difference"], [[-90, 0]])

    def test_repeated_physical_section_rejected(self):
        first = section("one", "Homecage", [1, 0], [0, 0])
        other = section("rerun", "Homecage", [2, 0], [0, 0])
        other["physical_section_id"] = first["physical_section_id"]
        with self.assertRaisesRegex(ValueError, "physical section"):
            summarize_observed_sections([first, other], grid())

    def source_case(self, rows, change=None):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source = base / "fictional.csv"
            with source.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["Object Id", "Object Type", "XMin", "XMax", "YMin", "YMax"])
                writer.writerows(rows)
            specification = {"section_id": "fictional", "physical_section_id": "physical_fictional",
                             "animal_id": "animal_fictional", "condition": "Homecage", "pla_type": "HK1",
                             "source": {"path": source.name, "sha256": sha256_file(source),
                                        "source_file_id": "fictional_raw_source", "object_id_column": "Object Id"},
                             "transform": {"accepted": True, "matrix": [[1, 0, -10], [0, 1, -20], [0, 0, 1]]}}
            if change:
                change(specification)
            provenance = base / "pla.csv.gz"
            result = count_raw_section(specification, grid(), base, provenance)
            with gzip.open(provenance, "rt", encoding="utf-8") as handle:
                records = list(csv.DictReader(handle))
            return result, records

    def test_fixed_transform_midpoints_all_counts_and_pla_row_provenance(self):
        rows = [["0001", PLA_CLASS, 10, 11, 20, 21], ["0002", CHAT_CLASS, 11, 12, 20, 21],
                ["0003", PLA_CLASS, 14, 15, 20, 21]]
        result, records = self.source_case(rows)
        np.testing.assert_array_equal(result["pla_counts"], [[1, 0]])
        np.testing.assert_array_equal(result["chat_counts"], [[0, 1]])
        np.testing.assert_array_equal(result["observed_support"], [[True, True]])
        self.assertEqual(result["source_rows"], 3)
        self.assertEqual(result["pla_objects"], 2)
        self.assertEqual(result["chat_objects"], 1)
        self.assertEqual(result["in_grid_objects"] + result["outside_grid_objects"], 3)
        self.assertEqual(result["outside_grid_objects"], 1)
        self.assertEqual([r["object_id"] for r in records], ["0001", "0003"])
        self.assertEqual([r["source_row_number"] for r in records], ["2", "4"])
        self.assertEqual(float(records[0]["x_fixed_aligned"]), .5)
        self.assertEqual(float(records[0]["y_fixed_aligned"]), .5)

    def test_unknown_object_class_fails(self):
        with self.assertRaisesRegex(ValueError, "Unknown"):
            self.source_case([["1", "unrecognized", 10, 11, 20, 21]])

    def test_reversed_and_nonfinite_boxes_fail(self):
        for box in ((11, 10, 20, 21), (10, 11, "nan", 21), (10, "inf", 20, 21)):
            with self.subTest(box=box):
                with self.assertRaisesRegex(ValueError, "Nonfinite or reversed"):
                    self.source_case([["1", PLA_CLASS, *box]])

    def test_duplicate_id_across_known_classes_fails(self):
        with self.assertRaisesRegex(ValueError, "repeated object ID"):
            self.source_case([["1", PLA_CLASS, 10, 11, 20, 21], ["1", CHAT_CLASS, 10, 11, 20, 21]])

    def test_source_hash_mismatch_fails_before_counting(self):
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            self.source_case([["1", PLA_CLASS, 10, 11, 20, 21]], lambda s: s["source"].update(sha256="0" * 64))


if __name__ == "__main__":
    unittest.main()
