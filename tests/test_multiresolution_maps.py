"""Exact fresh-bin refinement and portable detail tests on fictional sources."""
import csv
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from comet_spatial.core import GridSpec, count_section
from comet_spatial.exploratory import CHAT_CLASS, PLA_CLASS
from comet_spatial.manifest import empty_manifest, sha256_file
from comet_spatial.multiresolution import aggregate_counts, build_multiresolution_maps, grid_at_width


def reference_grid():
    return GridSpec((0, 1000), (0, 1000), "fictional_units", "fictional_frame", "x", "y")


class MultiresolutionAcceptanceTests(unittest.TestCase):
    def test_raw_boundaries_refine_exactly_to_every_requested_grid(self):
        reference = reference_grid()
        xy = [[0, 0], [100, 100], [250, 250], [500, 500], [999.99, 999.99], [1000, 1000], [-1, 0]]
        ids = list(range(len(xy)))
        fine = count_section(xy, grid_at_width(reference, 50), ids)
        self.assertEqual(fine.in_grid_objects, 6)
        self.assertEqual(fine.outside_grid_objects, 1)
        for width in (1000, 500, 250, 100):
            with self.subTest(width=width):
                direct = count_section(xy, grid_at_width(reference, width), ids)
                rebinned = aggregate_counts(fine.counts, width // 50)
                np.testing.assert_array_equal(rebinned, direct.counts)
                self.assertEqual(int(rebinned.sum()), 6)
        self.assertEqual(count_section([[250, 250]], grid_at_width(reference, 250), ["edge"]).counts[1, 1], 1)

    def test_aggregation_rejects_partial_or_noninteger_factors(self):
        for factor in (0, 2.5, 3):
            with self.subTest(factor=factor):
                with self.assertRaises(ValueError):
                    aggregate_counts(np.ones((4, 4), dtype=int), factor)
        with self.assertRaises(ValueError):
            grid_at_width(reference_grid(), 300)

    def make_case(self, base):
        manifest = empty_manifest()
        manifest["grid"] = {"x_edges": [0, 1000], "y_edges": [0, 1000], "coordinate_units": "fictional_units",
                            "reference_space": "fictional_frame", "orientation": {"x_positive": "right", "y_positive": "up"}}
        for item in manifest["confirmations"].values():
            item["confirmed"] = True
        for arm in ("HK1", "PFKP"):
            for condition in ("Homecage", "Running"):
                sid = arm + "_" + condition
                path = base / (sid + ".csv")
                # Exact point bounds make grid-edge ownership testable. The
                # 750/750 bin is ChAT-only and therefore a measured PLA zero.
                x = 0 if condition == "Homecage" else 250
                with path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.writer(handle)
                    writer.writerow(["Object Id", "Object Type", "XMin", "XMax", "YMin", "YMax", "source_label"])
                    writer.writerow(["0001", PLA_CLASS, x + 100, x + 100, 200, 200, sid])
                    writer.writerow(["0002", CHAT_CLASS, 850, 850, 950, 950, sid])
                manifest["sections"].append({"section_id": sid, "physical_section_id": "physical_" + sid,
                    "animal_id": "animal_" + condition, "condition": condition, "pla_type": arm,
                    "source": {"path": path.name, "sha256": sha256_file(path), "source_file_id": "source_" + sid,
                               "object_id_column": "Object Id"},
                    "transform": {"accepted": True, "matrix": [[1, 0, -100], [0, 1, -200], [0, 0, 1]]}})
        manifest_path, auth_path = base / "manifest.json", base / "authorization.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        auth_path.write_text(json.dumps({"status": "authorized", "authorized_by": "user",
                                        "authorization_text": "FICTIONAL EXPLORATORY SOFTWARE TEST"}), encoding="utf-8")
        return manifest, manifest_path, auth_path

    def test_fresh_run_preserves_all_points_and_recomputes_finer_support(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            _, manifest_path, auth_path = self.make_case(base)
            run = build_multiresolution_maps(manifest_path, auth_path, base / "outputs")
            payload = json.loads((run / "view_payload.json").read_text())
            self.assertFalse(payload["strict_pdf_results"])
            self.assertTrue(payload["strict_pdf_results_pending"])
            self.assertEqual(payload["default_resolution"], "250")
            self.assertEqual(payload["validation"]["source_totals"]["source_rows"], 8)
            self.assertEqual(payload["validation"]["full_pla_point_count"], 4)
            self.assertEqual(payload["parameters"]["internal_integer_accumulator_width"], 50)
            self.assertEqual(len(payload["validation"]["exact_refinement_checks"]), 5)
            coarse = payload["resolutions"]["1000"]
            detailed = payload["resolutions"]["250"]
            self.assertEqual(coarse["arms"]["HK1"]["difference"], [[0.0]])
            self.assertIsNone(detailed["arms"]["HK1"]["difference"][0][0])
            self.assertIsNone(detailed["arms"]["HK1"]["difference"][0][1])
            self.assertEqual(detailed["arms"]["HK1"]["difference"][3][3], 0)
            self.assertEqual(detailed["arms"]["HK1"]["homecage_n"][3][3], 1)
            self.assertEqual(detailed["arms"]["HK1"]["running_n"][3][3], 1)
            for width, resolution in payload["resolutions"].items():
                for section in resolution["sections"]:
                    self.assertEqual(int(np.asarray(section["pla_counts"]).sum()), 1)
                    self.assertEqual(int(np.asarray(section["chat_counts"]).sum()), 1)
                    np.testing.assert_array_equal(np.asarray(section["observed_support"]),
                                                  (np.asarray(section["pla_counts"]) + np.asarray(section["chat_counts"])) > 0)
                self.assertTrue((run / ("resolution_" + width) / "hk1_matrices.npz").is_file())
            for point in payload["pla_points"]:
                self.assertFalse(point["sampled"])
                self.assertEqual(point["object_id"], ["0001"])
                self.assertEqual(point["source_row"], [2])
                self.assertEqual(point["native_x"][0] - point["x"][0], 100)
                self.assertEqual(point["native_y"][0] - point["y"][0], 200)
            self.assertTrue(payload["validation"]["full_pla_point_count_matches_raw"])

    def test_hash_failure_leaves_no_published_payload(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            manifest, manifest_path, auth_path = self.make_case(base)
            (base / manifest["sections"][0]["source"]["path"]).write_text("changed", encoding="utf-8")
            output = base / "outputs"
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                build_multiresolution_maps(manifest_path, auth_path, output)
            self.assertFalse((output / "latest_run.json").exists())
            self.assertEqual(list(output.rglob("view_payload.json")), [])


if __name__ == "__main__":
    unittest.main()
