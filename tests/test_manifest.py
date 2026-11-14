"""Intake/preflight tests use tiny synthetic files and explicit fictional sign-off."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from comet_spatial.manifest import (
    display_directions_from_manifest, empty_manifest, preflight_manifest,
    section_template, sha256_file, validate_manifest,
)


class ManifestAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.manifest = empty_manifest()
        for label in ("signoff", "alignment_check", "alignment_approval", "mask"):
            (self.base / label).write_text("synthetic acceptance fixture " + label, encoding="utf-8")
        self.manifest["approval"] = {"status": "documented", "documented_by": "TEST_FIXTURE_ONLY",
                                     "documented_at": "2026-11-09T12:00:00-05:00", "evidence": self.asset("signoff")}
        for item in self.manifest["confirmations"].values():
            item.update(confirmed=True, evidence="Synthetic test only; explicit fictional source relationships")
        self.manifest["study"]["scientific_question"] = "Synthetic acceptance test"
        self.manifest["grid"] = {"x_edges": [0, 1], "y_edges": [0, 1], "coordinate_units": "test_unit",
                                 "reference_space": "test_space", "orientation": {"x_positive": "test_right", "y_positive": "test_up",
                                                                                   "display_x_increases_to": "right",
                                                                                   "display_y_increases_to": "up"},
                                 "provenance": "Explicit synthetic acceptance grid"}
        self.manifest["alignment_reference"] = dict(self.asset("alignment_check"), figure_id="test_figure")
        for arm in ("HK1", "PFKP"):
            for condition in ("Homecage", "Running"):
                label = arm + "_" + condition
                (self.base / label).write_text("id,x,y\n" + label + ",0.5,0.5\n", encoding="utf-8")
                section = section_template()
                section.update(section_id=label, physical_section_id="physical_" + label,
                               animal_id="animal_" + condition, condition=condition, pla_type=arm)
                section["source"].update(self.asset(label), source_file_id=label, coordinate_units="test_unit",
                                         object_id_column="id", centroid_x_column="x", centroid_y_column="y",
                                         pla_object_type={"kind": "documented_pla_only", "evidence": "Synthetic source contains PLA only"},
                                         centroid_definition={"kind": "measured_centroid", "confirmed": True,
                                                              "evidence": "Synthetic true centroid fixture"})
                section["mask"].update(self.asset("mask"), format="geojson", coordinate_space="native", coordinate_units="test_unit")
                section["transform"].update(matrix=[[1, 0, 0], [0, 1, 0], [0, 0, 1]], accepted=True,
                                            approved_by="TEST_FIXTURE_ONLY", native_units="test_unit", aligned_units="test_unit",
                                            reference_space="test_space",
                                            evidence=self.asset("alignment_approval"))
                self.manifest["sections"].append(section)
                self.manifest["source_relationships"].append({"source_file_id": label, "relationship": "independent",
                                                             "included": True, "evidence": "Synthetic test assignment"})

    def tearDown(self):
        self.temp.cleanup()

    def asset(self, name):
        return {"path": name, "sha256": sha256_file(self.base / name)}

    def report(self):
        return validate_manifest(self.manifest, self.base)

    def test_complete_signed_manifest_can_pass(self):
        self.assertEqual(self.report()["status"], "ready", self.report()["blockers"])

    def test_empty_template_is_honestly_blocked(self):
        report = validate_manifest(empty_manifest(), self.base)
        self.assertEqual(report["status"], "blocked")
        self.assertTrue(any("not documented" in text.lower() for text in report["blockers"]))
        self.assertTrue(any("No confirmed section" in text for text in report["blockers"]))

    def test_unconfirmed_relationships_are_not_inferred(self):
        self.manifest["confirmations"]["sample_relationships"]["confirmed"] = False
        self.assertIn("Confirmation missing: sample_relationships", self.report()["blockers"])

    def test_absent_accepted_transform_and_alignment_reference_block(self):
        self.manifest["sections"][0]["transform"]["accepted"] = False
        (self.base / "alignment_check").unlink()
        report = self.report()
        self.assertEqual(report["status"], "blocked")
        self.assertTrue(any("accepted fixed transform" in x for x in report["blockers"]))
        self.assertTrue(any("alignment_reference is missing" in x for x in report["blockers"]))

    def test_changed_input_hash_blocks(self):
        (self.base / "HK1_Homecage").write_text("modified", encoding="utf-8")
        self.assertTrue(any("SHA-256 mismatch" in x for x in self.report()["blockers"]))

    def test_missing_mask_and_centroid_definition_block(self):
        (self.base / "mask").unlink()
        self.manifest["sections"][0]["source"]["centroid_definition"]["confirmed"] = False
        report = self.report()
        self.assertTrue(any(".mask is missing" in x for x in report["blockers"]))
        self.assertTrue(any("centroid measurement definition is unconfirmed" in x for x in report["blockers"]))

    def test_unapproved_bounding_box_proxy_blocks(self):
        self.manifest["sections"][0]["source"]["centroid_definition"]["kind"] = "bounding_box_midpoint"
        self.assertTrue(any("explicitly amended approved proxy" in x for x in self.report()["blockers"]))

    def test_approved_proxy_still_needs_hashed_amendment(self):
        self.manifest["sections"][0]["source"]["centroid_definition"]["kind"] = "approved_proxy"
        self.assertTrue(any("approved_amendment" in x for x in self.report()["blockers"]))

    def test_coordinate_unit_mismatch_blocks(self):
        self.manifest["sections"][0]["mask"]["coordinate_units"] = "unconfirmed_pixel"
        self.assertTrue(any("mask units disagree" in x for x in self.report()["blockers"]))

    def test_reference_space_mismatch_blocks(self):
        self.manifest["sections"][0]["transform"]["reference_space"] = "different_reference"
        self.assertTrue(any("transform reference space disagrees" in x for x in self.report()["blockers"]))

    def test_anatomical_terms_without_explicit_display_direction_block(self):
        self.manifest["grid"]["orientation"] = {"x_positive": "anatomical_right", "y_positive": "ventral"}
        self.assertTrue(any("Display orientation is unresolved" in x for x in self.report()["blockers"]))

    def test_explicit_display_direction_does_not_guess_from_anatomy(self):
        self.manifest["grid"]["orientation"] = {"x_positive": "dorsal", "y_positive": "ventral",
                                                "display_x_increases_to": "left", "display_y_increases_to": "down"}
        self.assertEqual(display_directions_from_manifest(self.manifest), ("left", "down"))
        self.assertEqual(self.report()["status"], "ready", self.report()["blockers"])

    def test_literal_legacy_display_directions_are_unambiguous(self):
        self.manifest["grid"]["orientation"] = {"x_positive": "left", "y_positive": "down"}
        self.assertEqual(display_directions_from_manifest(self.manifest), ("left", "down"))
        self.assertEqual(self.report()["status"], "ready", self.report()["blockers"])

    def test_invalid_explicit_display_direction_blocks_despite_literal_fallback(self):
        self.manifest["grid"]["orientation"] = {"x_positive": "right", "y_positive": "up",
                                                "display_x_increases_to": "dorsal", "display_y_increases_to": "up"}
        self.assertTrue(any("Display orientation is unresolved" in x for x in self.report()["blockers"]))

    def test_pla_object_declaration_is_required_even_for_all_rows(self):
        del self.manifest["sections"][0]["source"]["pla_object_type"]
        self.assertTrue(any("source.pla_object_type must declare" in x for x in self.report()["blockers"]))

    def test_mixed_source_requires_class_column_and_exact_pla_labels(self):
        self.manifest["sections"][0]["source"]["pla_object_type"] = {
            "kind": "classified_mixed_source", "evidence": "Synthetic PLA and ChAT classification"}
        blockers = self.report()["blockers"]
        self.assertTrue(any("pla_object_type.classification_column" in x for x in blockers))
        self.assertTrue(any("pla_object_type.accepted_values" in x for x in blockers))

    def test_mixed_source_exact_class_definition_passes_metadata_only(self):
        self.manifest["sections"][0]["source"]["pla_object_type"] = {
            "kind": "classified_mixed_source", "classification_column": "Object Type", "accepted_values": ["PLA"],
            "evidence": "Synthetic source dictionary defines PLA detection class"}
        self.assertEqual(self.report()["status"], "ready", self.report()["blockers"])

    def test_pla_class_values_cannot_be_coerced_from_numbers(self):
        self.manifest["sections"][0]["source"]["pla_object_type"] = {
            "kind": "classified_mixed_source", "classification_column": "Class", "accepted_values": [1],
            "evidence": "Synthetic source dictionary"}
        self.assertTrue(any("exact PLA class strings" in x for x in self.report()["blockers"]))

    def test_repeated_source_selection_blocks(self):
        duplicate = copy.deepcopy(self.manifest["sections"][0])
        duplicate.update(section_id="rerun", physical_section_id="pretend_new_section")
        self.manifest["sections"].append(duplicate)
        self.assertTrue(any("identical source/selection" in x for x in self.report()["blockers"]))

    def test_included_superseded_source_blocks(self):
        self.manifest["source_relationships"][0].update(relationship="superseded", primary_source_file_id="other")
        self.assertTrue(any("superseded source cannot enter" in x for x in self.report()["blockers"]))

    def test_overlapping_selectors_on_consolidated_source_block(self):
        duplicate = copy.deepcopy(self.manifest["sections"][0])
        duplicate.update(section_id="subset", physical_section_id="subset_section")
        duplicate["source"]["object_selection"] = {"mode": "column_equals", "predicates": {"region": "one"}}
        self.manifest["sections"].append(duplicate)
        self.assertTrue(any("may overlap" in x for x in self.report()["blockers"]))

    def test_disjoint_selectors_on_consolidated_source_are_allowed(self):
        original = self.manifest["sections"][0]
        original["source"]["object_selection"] = {"mode": "column_equals", "predicates": {"region": "one"}}
        duplicate = copy.deepcopy(original)
        duplicate.update(section_id="other_region", physical_section_id="other_section")
        duplicate["source"]["object_selection"] = {"mode": "column_equals", "predicates": {"region": "two"}}
        self.manifest["sections"].append(duplicate)
        self.assertEqual(self.report()["status"], "ready", self.report()["blockers"])

    def test_malformed_or_missing_manifest_returns_blocker(self):
        path = self.base / "missing.json"
        self.assertEqual(preflight_manifest(path)["status"], "blocked")
        path.write_text("not valid JSON", encoding="utf-8")
        self.assertEqual(preflight_manifest(path)["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
