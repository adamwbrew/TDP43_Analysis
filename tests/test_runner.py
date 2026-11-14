"""Temporary fictional inputs exercise the runner; no experiment maps are made."""
import copy
import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from comet_spatial.manifest import empty_manifest, section_template, sha256_file

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("spatial_runner", ROOT / "scripts/run_analysis.py")
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class RunnerIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.output = self.base / "generated"
        self.report = self.base / "preflight.json"
        self.manifest_path = self.base / "manifest.json"
        # A genuine tiny source image serves only as a fictional reference file.
        from PIL import Image
        Image.new("RGB", (20, 20), "white").save(self.base / "reference.png")
        (self.base / "evidence.txt").write_text("FICTIONAL SOFTWARE TEST ONLY", encoding="utf-8")
        (self.base / "mask.geojson").write_text(json.dumps({"type": "Feature", "properties": {},
            "geometry": {"type": "Polygon", "coordinates": [[[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]]}}))
        self.manifest = empty_manifest()
        self.manifest["approval"] = {"status": "scientist_approved", "approved_by": "FICTIONAL_TEST",
            "approved_at": "2026-11-09T12:00:00-05:00", "evidence": self.asset("evidence.txt")}
        for confirmation in self.manifest["confirmations"].values():
            confirmation.update(confirmed=True, evidence="Explicit fictional software acceptance fixture")
        self.manifest["study"]["scientific_question"] = "Fictional count-map arithmetic test"
        self.manifest["grid"] = {"x_edges": [0, 1, 2], "y_edges": [0, 1, 2],
            "coordinate_units": "test_units", "reference_space": "fictional_space",
            "orientation": {"x_positive": "test_right", "y_positive": "test_down",
                            "display_x_increases_to": "right", "display_y_increases_to": "down"},
            "provenance": "Explicit 2 by 2 fictional grid"}
        self.manifest["alignment_reference"] = dict(self.asset("reference.png"), figure_id="fictional_reference")
        for arm in ("HK1", "PFKP"):
            for condition in ("Homecage", "Running"):
                label = arm + "_" + condition
                # True centroid fields; no centroids are synthesized from boxes by the runner.
                n = (1 if condition == "Homecage" else 3) if arm == "HK1" else (4 if condition == "Homecage" else 1)
                with (self.base / (label + ".csv")).open("w", newline="", encoding="utf-8") as handle:
                    writer = csv.writer(handle)
                    writer.writerow(["id", "cx", "cy", "Object Type", "source_label"])
                    for index in range(n):
                        writer.writerow(["000" + str(index), .5, .5, "test_PLA", label])
                    writer.writerow(["marker", 1.5, 1.5, "test_marker", label])
                section = section_template()
                section.update(section_id=label, physical_section_id="physical_" + label,
                    animal_id="animal_" + condition, condition=condition, pla_type=arm)
                section["source"].update(self.asset(label + ".csv"), source_file_id=label,
                    coordinate_units="test_units", object_id_column="id", centroid_x_column="cx", centroid_y_column="cy",
                    centroid_definition={"kind": "measured_centroid", "confirmed": True, "evidence": "Explicit test centroids"},
                    object_selection={"mode": "column_equals", "predicates": {"Object Type": "test_PLA"}},
                    pla_object_type={"kind": "classified_mixed_source", "classification_column": "Object Type",
                                     "accepted_values": ["test_PLA"], "evidence": "Fictional class definition"})
                section["mask"].update(self.asset("mask.geojson"), format="geojson", coordinate_space="native",
                                       coordinate_units="test_units")
                section["transform"].update(matrix=[[1, 0, 0], [0, 1, 0], [0, 0, 1]], accepted=True,
                    approved_by="FICTIONAL_TEST", native_units="test_units", aligned_units="test_units",
                    reference_space="fictional_space",
                    evidence=self.asset("evidence.txt"))
                self.manifest["sections"].append(section)
                self.manifest["source_relationships"].append({"source_file_id": label, "relationship": "independent",
                    "included": True, "evidence": "Independent fictional source"})

    def tearDown(self):
        self.temporary.cleanup()

    def asset(self, name):
        return {"path": name, "sha256": sha256_file(self.base / name)}

    def run_cli(self, manifest=None, preflight_only=False):
        self.manifest_path.write_text(json.dumps(self.manifest if manifest is None else manifest), encoding="utf-8")
        arguments = ["--manifest", str(self.manifest_path), "--preflight-report", str(self.report),
                     "--output-dir", str(self.output)]
        if preflight_only:
            arguments.append("--preflight-only")
        return runner.main(arguments)

    def test_blocked_manifest_saves_blockers_and_no_maps(self):
        self.assertEqual(self.run_cli(empty_manifest()), 2)
        self.assertEqual(json.loads(self.report.read_text())["status"], "blocked")
        self.assertFalse(self.output.exists())
        self.assertEqual(list(self.base.rglob("difference*.png")), [])

    def test_ready_preflight_does_not_run_analysis(self):
        self.assertEqual(self.run_cli(preflight_only=True), 0)
        self.assertEqual(json.loads(self.report.read_text())["status"], "ready")
        self.assertFalse(self.output.exists())

    def test_full_run_saves_correct_separate_counts_shared_limits_and_pending_review(self):
        self.assertEqual(self.run_cli(), 3)
        latest = json.loads((self.output / "latest_run.json").read_text())
        directory = Path(latest["run_directory"])
        self.assertFalse(latest["scientific_acceptance_passed"])
        self.assertEqual(latest["alignment_reproduction_status"], "inspection_view_regenerated_unverified")
        self.assertEqual(latest["shared_symmetric_color_limit"], 3)
        self.assertEqual(latest["display_orientation"], {"x_increases_to": "right", "y_increases_to": "down"})
        for arm, difference in (("hk1", 2), ("pfkp", -3)):
            with np.load(directory / (arm + "_matrices.npz")) as arrays:
                self.assertEqual(arrays["difference"][0, 0], difference)
                self.assertEqual(arrays["difference"][1, 1], 0)  # measured, fully covered zero
                np.testing.assert_array_equal(arrays["homecage_n"], np.ones((2, 2)))
                np.testing.assert_array_equal(arrays["running_n"], np.ones((2, 2)))
                self.assertTrue(arrays["displayable"].all())
            self.assertTrue((directory / ("difference_" + arm + ".svg")).is_file())
            from PIL import Image
            with Image.open(directory / ("difference_" + arm + ".png")) as figure:
                self.assertAlmostEqual(figure.info["dpi"][0], 300, places=1)
        self.assertTrue((directory / "coverage_four_panels.png").is_file())
        self.assertTrue((directory / "alignment_inspection_regenerated.png").is_file())
        self.assertEqual(sha256_file(directory / "accepted_alignment_reference.png"),
                         self.manifest["alignment_reference"]["sha256"])
        import gzip
        with gzip.open(directory / "section_0000_objects.csv.gz", "rt", encoding="utf-8") as handle:
            row = next(csv.DictReader(handle))
        self.assertEqual(row["object_id"], "0000")

    def test_mixed_object_rows_are_not_silently_counted_as_pla(self):
        self.manifest["sections"][0]["source"]["object_selection"] = {"mode": "all_rows"}
        self.assertEqual(self.run_cli(), 2)
        self.assertIn("non-PLA", " ".join(json.loads(self.report.read_text())["blockers"]))
        self.assertFalse((self.output / "latest_run.json").exists())
        self.assertEqual(list(self.output.rglob("difference*.png")), [])

    def test_partial_mask_remains_invalid_while_valid_empty_bins_stay_zero(self):
        partial = {"type": "Polygon", "coordinates": [[[0, 0], [1.999999999, 0], [1.999999999, 2], [0, 2], [0, 0]]]}
        (self.base / "partial.geojson").write_text(json.dumps(partial))
        self.manifest["sections"][0]["mask"].update(self.asset("partial.geojson"))
        self.assertEqual(self.run_cli(), 3)
        latest = json.loads((self.output / "latest_run.json").read_text())
        with np.load(Path(latest["run_directory"]) / "hk1_matrices.npz") as arrays:
            self.assertEqual(arrays["homecage_n"][0, 1], 0)
            self.assertTrue(np.isnan(arrays["difference"][0, 1]))
            self.assertEqual(arrays["difference"][1, 0], 0)


if __name__ == "__main__":
    unittest.main()
