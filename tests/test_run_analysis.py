"""Full temporary fictional run verifies portable saved masks and core views.

All figures and numerical files are created inside TemporaryDirectory. These
inputs do not represent specimens and never become project scientific outputs.
"""
import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image
from shapely.geometry import box, mapping, shape

from comet_spatial.core import FixedTransform, polygon_tissue_validity
from comet_spatial.core_view import build_core_view_payload
from comet_spatial.manifest import (
    empty_manifest, grid_from_manifest, preflight_manifest, section_template, sha256_file,
)


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("portable_core_runner_test", ROOT / "scripts/run_analysis.py")
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class PortableFullRunAcceptanceTests(unittest.TestCase):
    def test_real_runner_saves_geometry_and_self_contained_exact_core_views(self):
        with tempfile.TemporaryDirectory(prefix="comet-fictional-acceptance-") as temporary:
            base = Path(temporary)
            inputs = base / "fictional_inputs"
            inputs.mkdir()
            evidence = inputs / "evidence.txt"
            evidence.write_text("FICTIONAL SOFTWARE ACCEPTANCE INPUTS; NO EXPERIMENTAL SPECIMENS", encoding="utf-8")
            reference = inputs / "reference.png"
            Image.new("RGB", (10, 10), "white").save(reference)

            def asset(path):
                return {"path": str(path.relative_to(base)), "sha256": sha256_file(path)}

            manifest = empty_manifest()
            manifest["approval"] = {
                "status": "documented", "documented_by": "FICTIONAL_TEST_TRANSCRIPTION",
                "documented_at": "2026-11-11T12:00:00-05:00", "evidence": asset(evidence)}
            for confirmation in manifest["confirmations"].values():
                confirmation.update(confirmed=True, evidence="Explicit fictional acceptance fixture")
            manifest["study"]["scientific_question"] = "FICTIONAL portable raw-count acceptance check"
            manifest["grid"] = {
                "x_edges": [0, 1, 2], "y_edges": [0, 1], "coordinate_units": "fictional_units",
                "reference_space": "fictional_fixed_frame", "orientation": {
                    "x_positive": "fictional_horizontal_axis", "y_positive": "fictional_vertical_axis",
                    "display_x_increases_to": "right", "display_y_increases_to": "down"},
                "provenance": "Explicit shared two-by-one fictional grid"}
            manifest["alignment_reference"] = {**asset(reference), "figure_id": "FICTIONAL_TEST_REFERENCE"}
            native_masks = {}
            conditions = (("HK1", "Homecage", 1), ("HK1", "Running", 3),
                          ("PFKP", "Homecage", 4), ("PFKP", "Running", 1))
            for arm, condition, n in conditions:
                sid = arm + "_" + condition
                source_path = inputs / (sid + ".csv")
                with source_path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.writer(handle)
                    writer.writerow(["Object Id", "cx", "cy", "Object Type", "section_label"])
                    for index in range(n):
                        writer.writerow(["000" + str(index), 10.5, 20.5, "fixture_PLA", sid])
                    # An unselected marker at the second bin must never become PLA.
                    writer.writerow(["marker", 11.5, 20.5, "fixture_marker", sid])
                # Only HK1/Homecage lacks full coverage of the second bin. A
                # tiny exterior sliver suffices; the zero is then missing tissue.
                maximum_x = 12 - 1e-10 if (arm, condition) == ("HK1", "Homecage") else 12
                native_mask = box(10, 20, maximum_x, 21)
                native_masks[sid] = native_mask
                mask_path = inputs / (sid + "_mask.geojson")
                mask_path.write_text(json.dumps(mapping(native_mask)), encoding="utf-8")
                section = section_template()
                section.update(section_id=sid, physical_section_id="physical_" + sid,
                               animal_id="animal_" + condition, condition=condition, pla_type=arm)
                section["source"].update(
                    asset(source_path), source_file_id="source_" + sid, coordinate_units="fictional_units",
                    object_id_column="Object Id", centroid_x_column="cx", centroid_y_column="cy",
                    centroid_definition={"kind": "measured_centroid", "confirmed": True,
                                         "evidence": "Explicit fictional measured-centroid columns"},
                    pla_object_type={"kind": "classified_mixed_source", "classification_column": "Object Type",
                                     "accepted_values": ["fixture_PLA"], "evidence": "Fictional source dictionary"},
                    object_selection={"mode": "column_equals", "predicates": {"Object Type": "fixture_PLA"}})
                section["mask"].update(asset(mask_path), format="geojson", coordinate_space="native",
                                       coordinate_units="fictional_units")
                section["transform"].update(
                    matrix=[[1, 0, -10], [0, 1, -20], [0, 0, 1]], accepted=True,
                    approved_by="FICTIONAL_FIXED_TRANSFORM_SOURCE", native_units="fictional_units",
                    aligned_units="fictional_units", reference_space="fictional_fixed_frame", evidence=asset(evidence))
                manifest["sections"].append(section)
                manifest["source_relationships"].append({
                    "source_file_id": "source_" + sid, "relationship": "independent", "included": True,
                    "evidence": "Independent fictional source for each section/arm"})
            manifest_path = base / "fictional_manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            report = preflight_manifest(manifest_path)
            self.assertEqual(report["status"], "ready", report["blockers"])

            # Exercise actual readers, strict geometry, all numerical saves and
            # real 300-DPI/SVG exports; no renderer or measurement is mocked.
            destination = runner.execute(manifest, manifest_path, base / "temporary_results", ("right", "down"))
            section_index = json.loads((destination / "section_index.json").read_text())
            grid = grid_from_manifest(manifest)
            for record in section_index:
                sid = record["section_id"]
                for frame in ("native", "aligned"):
                    path = destination / record[frame + "_mask_file"]
                    self.assertEqual(sha256_file(path), record[frame + "_mask_sha256"])
                native = shape(json.loads((destination / record["native_mask_file"]).read_text()))
                aligned = shape(json.loads((destination / record["aligned_mask_file"]).read_text()))
                self.assertTrue(native.equals_exact(native_masks[sid], 0))
                transform = FixedTransform(record["fixed_transform"]["matrix"])
                self.assertTrue(transform.geometry(native).equals_exact(aligned, 0))
                with np.load(destination / record["matrix_file"], allow_pickle=False) as arrays:
                    np.testing.assert_array_equal(arrays["tissue_validity"], polygon_tissue_validity(aligned, grid))
                    expected_n = next(n for arm, condition, n in conditions if sid == arm + "_" + condition)
                    np.testing.assert_array_equal(arrays["counts"], [[expected_n, 0]])
                self.assertEqual(record["source_rows"], record["selected_objects"] + 1)
            for filename in ("difference_hk1.png", "difference_pfkp.png", "coverage_four_panels.png",
                             "alignment_inspection_regenerated.png"):
                self.assertTrue((destination / filename).is_file())
                with Image.open(destination / filename) as figure:
                    self.assertAlmostEqual(figure.info["dpi"][0], 300, places=1)
            self.assertTrue((destination / "difference_hk1.svg").is_file())

            # Remove the originals to prove the viewer uses recorded mask
            # geometry and saved object provenance, not inaccessible old paths.
            for original_mask in inputs.glob("*_mask.geojson"):
                original_mask.unlink()
            payload = build_core_view_payload(destination, preview_limit=2)
            self.assertEqual(payload["status"], "numerical_ready", payload["blockers"])
            self.assertTrue(payload["views"]["alignment"]["available"])
            self.assertFalse(payload["views"]["alignment"]["fulfilled"])
            self.assertTrue(payload["validation"]["strict_mask_geometry_rechecked"])
            self.assertTrue(payload["validation"]["all_saved_objects_recounted"])
            self.assertFalse(payload["validation"]["scientific_acceptance_passed"])
            hk1, pfkp = payload["arms"]["HK1"], payload["arms"]["PFKP"]
            self.assertEqual(hk1["homecage_mean"], [[1.0, None]])
            self.assertEqual(hk1["running_mean"], [[3.0, 0.0]])
            self.assertEqual(hk1["difference"], [[2.0, None]])
            self.assertEqual(hk1["homecage_n"], [[1, 0]])
            self.assertEqual(hk1["running_n"], [[1, 1]])
            self.assertEqual(pfkp["homecage_mean"], [[4.0, 0.0]])
            self.assertEqual(pfkp["running_mean"], [[1.0, 0.0]])
            self.assertEqual(pfkp["difference"], [[-3.0, 0.0]])
            self.assertEqual(pfkp["homecage_n"], [[1, 1]])
            self.assertEqual(pfkp["running_n"], [[1, 1]])
            self.assertEqual(payload["color_scale"]["cmin"], -3)
            self.assertEqual(payload["color_scale"]["cmax"], 3)
            json.dumps(payload, allow_nan=False)


if __name__ == "__main__":
    unittest.main()
