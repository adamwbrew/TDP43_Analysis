"""Temporary fictional numerical runs; no example experiment maps are exported."""
import csv
import gzip
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from shapely.geometry import box, mapping

from comet_spatial.core import (
    FixedTransform, SectionResult, count_section, polygon_tissue_validity,
    shared_symmetric_limit, summarize_by_arm,
)
from comet_spatial.core_view import build_core_view_payload
from comet_spatial.manifest import empty_manifest, grid_from_manifest, section_template, sha256_file


class CoreViewAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.run = self.base / "fictional_run"
        self.run.mkdir()
        self.manifest = empty_manifest()
        self.manifest["grid"] = {
            "x_edges": [0, 1, 3], "y_edges": [0, 1], "coordinate_units": "fictional_units",
            "reference_space": "fictional_reference", "orientation": {
                "x_positive": "fictional_anatomical_x", "y_positive": "fictional_anatomical_y",
                "display_x_increases_to": "left", "display_y_increases_to": "down"},
            "provenance": "EXPLICIT FICTIONAL NONUNIFORM SHARED GRID"}
        # Byte content is sufficient: this test validates provenance, not image rendering.
        (self.run / "accepted_alignment_reference.png").write_bytes(b"fictional_reference_bytes")
        self.manifest["alignment_reference"] = {
            "path": "reference.png", "sha256": sha256_file(self.run / "accepted_alignment_reference.png"),
            "figure_id": "FICTIONAL_REFERENCE"}
        self.grid = grid_from_manifest(self.manifest)
        self.index, self.sections = [], []
        for i, (arm, condition, n) in enumerate((
                ("HK1", "Homecage", 1), ("HK1", "Running", 3),
                ("PFKP", "Homecage", 4), ("PFKP", "Running", 1))):
            sid = arm + "_" + condition
            specification = section_template()
            specification.update(section_id=sid, physical_section_id="physical_" + sid,
                                 animal_id="animal_" + condition, condition=condition, pla_type=arm)
            specification["source"].update(path=sid + ".csv", sha256="1" * 64, source_file_id=sid,
                                            centroid_definition={"kind": "measured_centroid", "confirmed": True,
                                                                 "evidence": "FICTIONAL MEASUREMENT"})
            # A supplied translation is applied to native centroids and mask alike.
            specification["transform"].update(matrix=[[1, 0, -10], [0, 1, 0], [0, 0, 1]],
                                               accepted=True, reference_space="fictional_reference")
            native_mask = box(10, 0, 13, 1)
            transform = FixedTransform(specification["transform"]["matrix"])
            aligned_mask = transform.geometry(native_mask)
            prefix = "section_%04d" % i
            native_file, aligned_file = prefix + "_native_mask.geojson", prefix + "_aligned_mask.geojson"
            self.write_json(self.run / native_file, mapping(native_mask))
            self.write_json(self.run / aligned_file, mapping(aligned_mask))
            specification["mask"].update(path="original_mask.geojson", sha256="2" * 64,
                                        format="geojson", coordinate_space="native")
            self.manifest["sections"].append(specification)
            native = np.asarray([[10.5, .5]] * n)
            aligned = transform.points(native)
            counted = count_section(aligned, self.grid, ["000" + str(j) for j in range(n)])
            valid = polygon_tissue_validity(aligned_mask, self.grid)
            result = SectionResult(sid, specification["animal_id"], specification["physical_section_id"],
                                   condition, arm, counted.counts, valid)
            self.sections.append(result)
            np.savez_compressed(self.run / (prefix + ".npz"), counts=counted.counts, tissue_validity=valid,
                                x_edges=self.grid.x_edges, y_edges=self.grid.y_edges)
            object_file = prefix + "_objects.csv.gz"
            with gzip.open(self.run / object_file, "wt", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["source_file_id", "source_row_number", "object_id", "x_input", "y_input", "x_aligned", "y_aligned"])
                for j, (original, transformed) in enumerate(zip(native, aligned)):
                    writer.writerow([sid, j + 2, "000" + str(j), *original, *transformed])
            self.index.append({**{key: specification[key] for key in (
                "section_id", "physical_section_id", "animal_id", "condition", "pla_type", "source", "mask")},
                "fixed_transform": specification["transform"], "source_rows": n, "selected_objects": n,
                "in_grid_objects": n, "outside_grid_objects": 0, "valid_bins": int(valid.sum()),
                "matrix_file": prefix + ".npz", "object_provenance_file": object_file,
                "native_mask_file": native_file, "aligned_mask_file": aligned_file,
                "native_mask_sha256": sha256_file(self.run / native_file),
                "aligned_mask_sha256": sha256_file(self.run / aligned_file)})
        self.summaries = summarize_by_arm(self.sections, self.grid)
        self.save_summary()
        self.validation = {"software_status": "completed", "scientific_acceptance_passed": False,
                           "count_conservation_passed": True,
                           "shared_symmetric_color_limit": shared_symmetric_limit(self.summaries),
                           "alignment_reproduction_status": "inspection_view_regenerated_unverified",
                           "blockers": ["FICTIONAL TEST: prior layout comparison pending"]}
        self.write_snapshot()

    def tearDown(self):
        self.temporary.cleanup()

    @staticmethod
    def write_json(path, value):
        Path(path).write_text(json.dumps(value), encoding="utf-8")

    def write_snapshot(self):
        self.write_json(self.run / "manifest_snapshot.json", self.manifest)
        self.write_json(self.run / "section_index.json", self.index)
        self.write_json(self.run / "validation.json", self.validation)

    def save_summary(self):
        for arm, summary in self.summaries.items():
            np.savez_compressed(self.run / (arm.lower() + "_matrices.npz"),
                                x_edges=self.grid.x_edges, y_edges=self.grid.y_edges,
                                **{key: getattr(summary, key) for key in (
                                    "homecage_mean", "running_mean", "difference", "homecage_n", "running_n", "displayable")})

    def test_no_run_has_no_default_scientific_arrays(self):
        payload = build_core_view_payload()
        self.assertEqual(payload["status"], "blocked")
        self.assertEqual(payload["arms"], {})
        self.assertIsNone(payload["grid"])
        self.assertFalse(payload["views"]["differences"]["available"])
        json.dumps(payload, allow_nan=False)

    def test_current_blocked_preflight_prevents_stale_run_display(self):
        payload = build_core_view_payload(self.run, preflight={"status": "blocked", "blockers": ["Current mask unresolved"]})
        self.assertEqual(payload["arms"], {})
        self.assertIn("Current mask unresolved", payload["blockers"])

    def test_verified_numerics_preserve_zero_shared_grid_scale_and_pending_alignment(self):
        payload = build_core_view_payload(self.run, preview_limit=2)
        self.assertEqual(payload["status"], "numerical_ready", payload["blockers"])
        self.assertEqual(payload["arms"]["HK1"]["difference"], [[2.0, 0.0]])
        self.assertEqual(payload["arms"]["PFKP"]["difference"], [[-3.0, 0.0]])
        self.assertEqual(payload["grid"]["x_edges"], [0, 1, 3])  # no uniform-grid restriction
        self.assertEqual(payload["grid"]["display_directions"], {"x": "left", "y": "down"})
        self.assertEqual(payload["color_scale"]["cmin"], -3)
        self.assertEqual(payload["color_scale"]["cmax"], 3)
        self.assertTrue(payload["views"]["alignment"]["available"])
        self.assertFalse(payload["views"]["alignment"]["fulfilled"])
        self.assertFalse(payload["validation"]["scientific_acceptance_passed"])
        self.assertTrue(payload["validation"]["all_saved_objects_recounted"])
        preview = payload["alignment"]["sections"][1]
        self.assertEqual(preview["native_centroid_preview"], [[10.5, .5], [10.5, .5]])
        self.assertEqual(preview["aligned_centroid_preview"], [[.5, .5], [.5, .5]])
        self.assertEqual(preview["object_id_preview"], ["0000", "0002"])
        self.assertTrue(preview["preview_sampling"]["sampled"])
        self.assertEqual(payload["sections"][0]["animal_id"], "animal_Homecage")
        json.dumps(payload, allow_nan=False)

    def test_matrix_tampering_is_not_presented_as_a_result(self):
        path = self.run / "hk1_matrices.npz"
        with np.load(path) as arrays:
            changed = {key: arrays[key].copy() for key in arrays.files}
        changed["difference"][0, 0] = 99
        np.savez_compressed(path, **changed)
        payload = build_core_view_payload(self.run)
        self.assertEqual(payload["status"], "blocked")
        self.assertEqual(payload["arms"], {})
        self.assertIn("does not equal section-derived", payload["blockers"][0])

    def test_changed_fixed_transform_is_detected_from_saved_coordinates(self):
        self.index[0]["fixed_transform"]["matrix"][0][2] = -9
        # Both index and manifest change together; coordinate evidence still detects it.
        self.write_snapshot()
        payload = build_core_view_payload(self.run)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("unchanged transform", payload["blockers"][0])

    def test_missing_saved_outline_disables_alignment_without_filling_missing_geometry(self):
        for record in self.index:
            record.pop("native_mask_file")
            record.pop("aligned_mask_file")
        self.write_snapshot()
        payload = build_core_view_payload(self.run)
        self.assertEqual(payload["status"], "numerical_ready", payload["blockers"])
        self.assertFalse(payload["views"]["alignment"]["available"])
        self.assertIsNone(payload["alignment"]["sections"][0]["aligned_mask_geojson"])
        self.assertEqual(payload["arms"]["HK1"]["difference"][0][0], 2)

    def test_mask_artifact_hash_change_is_an_integrity_failure(self):
        (self.run / self.index[0]["aligned_mask_file"]).write_text(json.dumps(mapping(box(0, 0, 1, 1))))
        payload = build_core_view_payload(self.run)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("SHA-256 mismatch", payload["blockers"][0])

    def test_section_contributions_are_exact_valid_zero_counts(self):
        payload = build_core_view_payload(self.run)
        contributors = [s for s in payload["sections"] if s["pla_type"] == "HK1" and
                        s["condition"] == "Homecage" and s["tissue_validity"][0][1]]
        self.assertEqual([s["counts"][0][1] for s in contributors], [0])
        self.assertEqual(len(contributors), payload["arms"]["HK1"]["homecage_n"][0][1])

    def test_missing_opposite_condition_is_null_and_not_a_true_zero(self):
        record = self.index[0]
        native = box(10, 0, 11, 1)
        aligned = FixedTransform(record["fixed_transform"]["matrix"]).geometry(native)
        for prefix, geometry in (("native", native), ("aligned", aligned)):
            self.write_json(self.run / record[prefix + "_mask_file"], mapping(geometry))
            record[prefix + "_mask_sha256"] = sha256_file(self.run / record[prefix + "_mask_file"])
        valid = polygon_tissue_validity(aligned, self.grid)
        first = self.sections[0]
        self.sections[0] = SectionResult(first.section_id, first.animal_id, first.physical_section_id,
                                         first.condition, first.pla_type, first.counts, valid)
        record["valid_bins"] = int(valid.sum())
        np.savez_compressed(self.run / record["matrix_file"], counts=first.counts, tissue_validity=valid,
                            x_edges=self.grid.x_edges, y_edges=self.grid.y_edges)
        self.summaries = summarize_by_arm(self.sections, self.grid)
        self.save_summary()
        self.write_snapshot()
        payload = build_core_view_payload(self.run)
        self.assertEqual(payload["status"], "numerical_ready", payload["blockers"])
        self.assertIsNone(payload["arms"]["HK1"]["difference"][0][1])
        self.assertIsNone(payload["arms"]["HK1"]["homecage_mean"][0][1])
        self.assertEqual(payload["arms"]["HK1"]["running_mean"][0][1], 0)
        self.assertEqual(payload["arms"]["HK1"]["homecage_n"][0][1], 0)
        self.assertEqual(payload["arms"]["HK1"]["running_n"][0][1], 1)
        self.assertFalse(payload["arms"]["HK1"]["displayable"][0][1])
        json.dumps(payload, allow_nan=False)


if __name__ == "__main__":
    unittest.main()
