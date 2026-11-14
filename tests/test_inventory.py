"""Synthetic input-audit fixtures; no scientific assignments are inferred."""

import csv
from pathlib import Path
import tempfile
import unittest

from scripts.inventory_data import audit_csv, sha256, signature


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="tdp43-inventory-test-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.header = [
            "Image Location", "Analysis Region", "Algorithm Name", "Object Id",
            "Object Type", "ChAt-50 - FITC_E1 present", "XMin", "XMax",
            "YMin", "YMax", "Area (µm²)",
        ]
        self.base = [
            "image,with comma", "unassigned export label", "fixture algorithm", "1",
            "PLA - TRITC_E1", "1", "0", "1", "0", "1", "0.25",
        ]

    def write_fixture(self, name, rows, bom=False):
        path = self.directory / name
        with path.open("w", newline="", encoding="utf-8-sig" if bom else "utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(self.header)
            writer.writerows(rows)
        return path

    def test_bom_and_quoted_fields_preserve_exported_text(self):
        row = self.base.copy()
        row[1] = 'region with "quotes", comma\nand a line break'
        path = self.write_fixture("quoted.csv", [row], bom=True)
        audit, _, _ = audit_csv(path, "synthetic", True)
        self.assertEqual(audit["columns"], self.header)
        self.assertEqual(audit["row_count"], 1)
        self.assertEqual(audit["analysis_region_counts"], {row[1]: 1})
        self.assertEqual(audit["column_profiles"]["Image Location"]["examples"], [row[0]])
        self.assertEqual(audit["pla_rows_with_chat_present_equal_1"], 1)
        self.assertEqual(audit["true_centroid_fields_present"], [])

    def test_malformed_rows_are_counted_without_entering_measurement_profiles(self):
        path = self.write_fixture("malformed.csv", [self.base, ["too", "short"], self.base + ["extra"]])
        audit, exact, measured = audit_csv(path, "synthetic", True)
        self.assertEqual(audit["row_count"], 3)
        self.assertEqual(audit["malformed_row_count"], 2)
        self.assertEqual(audit["object_type_counts"], {"PLA - TRITC_E1": 1})
        self.assertEqual(audit["column_profiles"]["Area (µm²)"]["numeric_count"], 1)
        self.assertEqual((len(exact), len(measured)), (1, 1))

    def test_missing_nonfinite_and_reversed_boxes_remain_auditable(self):
        rows = []
        for number, (xmin, xmax, area) in enumerate([("", "1", ""), ("inf", "4", "0.5"), ("3", "2", "0")]):
            row = self.base.copy()
            row[3], row[6], row[7], row[10] = str(number), xmin, xmax, area
            rows.append(row)
        audit, _, _ = audit_csv(self.write_fixture("invalid.csv", rows), "synthetic", True)
        self.assertEqual(audit["row_count"], 3)
        self.assertEqual(audit["missing_or_nonfinite_bbox_count"], 2)
        self.assertEqual(audit["invalid_bbox_order_count"], 1)
        self.assertEqual(audit["column_profiles"]["XMin"]["missing_count"], 1)
        self.assertEqual(audit["column_profiles"]["XMin"]["non_finite_count"], 1)
        self.assertEqual(audit["column_profiles"]["Area (µm²)"]["missing_count"], 1)
        self.assertEqual(audit["column_profiles"]["Area (µm²)"]["zero_count"], 1)

    def test_repeat_rows_keep_multiplicity_while_region_and_id_exclusions_are_explicit(self):
        changed = self.base.copy()
        changed[1], changed[3] = "different exported region", "99"
        first, exact_first, measured_first = audit_csv(
            self.write_fixture("first.csv", [self.base, self.base]), "first", True
        )
        second, exact_second, measured_second = audit_csv(
            self.write_fixture("second.csv", [changed]), "second", True
        )
        self.assertEqual(first["row_count"], 2)
        self.assertEqual(first["pla_row_count_by_export_label"], 2)
        self.assertEqual(first["duplicate_object_id_occurrences"], 1)
        self.assertEqual(first["exact_duplicate_row_occurrences"], 1)
        self.assertEqual(first["measurement_signature_unique_count"], 1)
        self.assertEqual(len(exact_first & exact_second), 0)
        self.assertEqual(len(measured_first & measured_second), 1)
        self.assertEqual(second["row_count"], 1)
        # Serialized values must distinguish different field boundaries.
        self.assertNotEqual(signature(["ab", "c"]), signature(["a", "bc"]))

    def test_hash_and_audit_do_not_modify_source_bytes_or_mtime(self):
        known = self.directory / "known.txt"
        known.write_bytes(b"abc")
        self.assertEqual(sha256(known), "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
        path = self.write_fixture("source.csv", [self.base])
        original_bytes, original_mtime = path.read_bytes(), path.stat().st_mtime_ns
        original_hash = sha256(path)
        audit_csv(path, "synthetic", True)
        self.assertEqual(path.read_bytes(), original_bytes)
        self.assertEqual(path.stat().st_mtime_ns, original_mtime)
        self.assertEqual(sha256(path), original_hash)


if __name__ == "__main__":
    unittest.main()
