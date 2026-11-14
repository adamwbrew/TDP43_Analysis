"""Portable fixed-three derived runs from small fictional cached raw counts."""
import copy
import csv
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import numpy as np

from comet_spatial.exploratory import summarize_observed_sections
from comet_spatial.core import GridSpec
from scripts.build_section_mean_maps import build, locate_run


ROOT = Path(__file__).resolve().parents[1]


def json_matrix(value):
    array = np.asarray(value)
    if array.dtype.kind != "f":
        return array.tolist()
    return [[float(v) if np.isfinite(v) else None for v in row] for row in array]


class SectionMeanBuildAcceptanceTests(unittest.TestCase):
    def fixture(self, root, mode="mixed"):
        for relative in ("scripts/build_section_mean_maps.py", "comet_spatial/section_means.py"):
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        policy = {"empty_bin_policy": "zero", "sections_per_condition": 3,
                  "authority": "FICTIONAL SOFTWARE TEST; explicit scientist-directed zero assumption"}
        (root / "metadata").mkdir()
        (root / "metadata/scientist_directed_mean_policy.json").write_text(json.dumps(policy))
        source = root / "outputs/exploratory_multiresolution/fictional_immutable_source"
        source.mkdir(parents=True)
        sections, points = [], []
        for arm in ("HK1", "PFKP"):
            for condition, triple in (("Homecage", (3, 5, 4)), ("Running", (7, 8, 9))):
                for i, count in enumerate(triple):
                    sid = arm + "_" + condition + str(i)
                    if arm == "PFKP":
                        count = 10 if condition == "Homecage" else 1
                    pla = np.asarray([[count, 0 if condition == "Homecage" else (i + 1) * 2], [0, 0]])
                    chat = np.asarray([[0, 0], [1, 0]])
                    if mode == "zero_difference":
                        pla = np.asarray([[1, 0], [0, 0]])
                    if mode == "empty_arm" and arm == "PFKP":
                        pla[:] = 0
                        chat[:] = 0
                    matrix = [[-1, 0, 10], [0, 1, -20], [0, 0, 1]]
                    raw_count = int(pla.sum())
                    sections.append({"section_id": sid, "physical_section_id": "physical_" + sid,
                        "animal_id": condition + str(i), "condition": condition, "pla_type": arm,
                        "source": {"source_file_id": "source_" + sid, "sha256": "1" * 64},
                        "fixed_transform": {"matrix": matrix, "accepted": True},
                        "pla_counts": pla.tolist(), "chat_counts": chat.tolist(),
                        "all_counts": (pla + chat).tolist(), "observed_support": (pla + chat > 0).tolist(),
                        "pla_objects": raw_count, "chat_objects": int(chat.sum())})
                    # Full, unsampled coordinate identity is copied as source
                    # evidence. Derivation must not transform or resample it.
                    xy = [(ix + .5, iy + .5) for iy, ix in np.ndindex(pla.shape)
                          for _ in range(int(pla[iy, ix]))]
                    points.append({"section_id": sid, "x": [p[0] for p in xy], "y": [p[1] for p in xy],
                        "native_x": [10 - p[0] for p in xy], "native_y": [20 + p[1] for p in xy],
                        "object_id": ["000" + str(j) for j in range(raw_count)],
                        "source_row": list(range(2, raw_count + 2)), "sampled": False,
                        "point_count": raw_count})
        validation = {key: True for key in (
            "count_conservation_all_resolutions", "full_pla_point_count_matches_raw",
            "hashes_verified_before_after_and_before_publication", "fixed_transforms_unchanged")}
        validation.update(status="completed_exploratory_multiresolution", generated_utc="fictional_original_timestamp",
            baseline_1000_comparison={"matched": True,
                "all_section_counts_support_and_arm_mean_difference_n_arrays_exactly_equal": True},
            source_totals={"pla_objects": sum(s["pla_objects"] for s in sections),
                           "chat_objects": sum(s["chat_objects"] for s in sections)})
        resolutions = {}
        # Repeated small grids make the fixture lightweight while exercising
        # every saved resolution key and every section's identity independently.
        reference = GridSpec((0, 1, 2), (0, 1, 2), "fictional", "fictional", "right", "down")
        summaries = summarize_observed_sections(sections, reference)
        for width in ("1000", "500", "250", "100"):
            arms = {arm: {key: json_matrix(value) if isinstance(value, np.ndarray) else value
                          for key, value in summary.items()} for arm, summary in summaries.items()}
            resolutions[width] = {"sections": copy.deepcopy(sections), "arms": arms,
                "grid": {"x_edges": [0, 1, 2], "y_edges": [0, 1, 2], "shape": [2, 2]},
                "parameters": {"mean_definition": "old variable observed-support denominator"},
                "color_scale": {"cmin": -99, "cmax": 99}, "validation": copy.deepcopy(validation)}
        payload = {"resolutions": resolutions, "pla_points": points, "sections": sections,
                   "statistics_by_resolution": {}, "validation": validation}
        path = source / "view_payload.json"
        path.write_text(json.dumps(payload, allow_nan=False))
        pointer = source.parent / "latest_run.json"
        # The builder must prefer the portable local snapshot over a stale
        # absolute source-computer path containing the same run basename.
        pointer.write_text(json.dumps({"run_directory": "/old/computer/fictional_immutable_source",
                                       "payload_file": "view_payload.json"}))
        return path, payload

    def test_fixed_three_zero_condition_and_immutable_points_transforms_and_history(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_path, original = self.fixture(root)
            before = source_path.read_bytes()
            self.assertEqual(locate_run(root, "exploratory_multiresolution"), source_path)
            run = build(root)
            derived = json.loads((run / "view_payload.json").read_text())
            self.assertEqual(source_path.read_bytes(), before)
            self.assertEqual(derived["pla_points"], original["pla_points"])
            self.assertEqual(derived["sections"], original["sections"])
            by_section = {s["section_id"]: s for s in derived["sections"]}
            for points in derived["pla_points"]:
                counts = np.zeros((2, 2), dtype=int)
                for x, y, nx, ny in zip(points["x"], points["y"], points["native_x"], points["native_y"]):
                    counts[int(y), int(x)] += 1
                    self.assertEqual(-nx + 10, x)
                    self.assertEqual(ny - 20, y)
                np.testing.assert_array_equal(counts, by_section[points["section_id"]]["pla_counts"])
            self.assertEqual(derived["fixed_section_denominator"], 3)
            for width, payload in derived["resolutions"].items():
                self.assertEqual(payload["sections"], original["resolutions"][width]["sections"])
                hk1, pfkp = payload["arms"]["HK1"], payload["arms"]["PFKP"]
                self.assertEqual(hk1["homecage_mean"], [[4.0, 0.0], [0.0, None]])
                self.assertEqual(hk1["running_mean"], [[8.0, 4.0], [0.0, None]])
                self.assertEqual(hk1["difference"], [[4.0, 4.0], [0.0, None]])
                self.assertEqual(hk1["homecage_n"][0][1], 0)
                self.assertEqual(hk1["running_n"][0][1], 3)
                self.assertTrue(hk1["displayable"][0][1])
                self.assertEqual(hk1["homecage_assumed_zero_section_n"][0][1], 3)
                self.assertEqual(hk1["raw_arithmetic_difference"][1][1], 0)
                self.assertEqual(pfkp["difference"][0][0], -9)
                self.assertFalse(payload["coverage_verified"])
                self.assertFalse(np.asarray(hk1["tissue_coverage_known"]).any())
                for arm in ("HK1", "PFKP"):
                    for condition, key in (("Homecage", "homecage"), ("Running", "running")):
                        group = [s for s in payload["sections"] if s["pla_type"] == arm and s["condition"] == condition]
                        expected_total = sum(np.asarray(s["pla_counts"]) for s in group)
                        np.testing.assert_array_equal(payload["arms"][arm][key + "_count_sum"], expected_total)
                with np.load(run / ("resolution_" + width) / "hk1_matrices.npz", allow_pickle=False) as arrays:
                    np.testing.assert_array_equal(arrays["homecage_mean"], [[4, 0], [0, 0]])
                    np.testing.assert_array_equal(arrays["difference"], [[4, 4], [0, 0]])
                    self.assertTrue(np.isnan(arrays["display_difference"][1, 1]))
                with (run / ("resolution_" + width) / "hk1_bins.csv").open() as handle:
                    rows = list(csv.DictReader(handle))
                self.assertEqual(rows[1]["mean_denominator_each_condition"], "3")
                self.assertEqual(rows[1]["homecage_observed_N"], "0")
                self.assertEqual(float(rows[1]["running_minus_homecage"]), 4)
                self.assertEqual(rows[1]["coverage_verified"], "False")
                self.assertEqual(rows[3]["display_domain"], "False")
                self.assertNotIn("baseline_1000_comparison", payload["validation"])
                self.assertEqual(payload["validation"]["fixed_section_denominator"], 3)
                self.assertTrue(payload["validation"]["all_mean_difference_checks_passed"])
            self.assertNotIn("baseline_1000_comparison", derived["validation"])
            self.assertEqual(derived["validation"]["source_count_validation"], original["validation"])
            source_record = json.loads((run / "source_record.json").read_text())
            self.assertEqual(source_record["sha256"], hashlib.sha256(before).hexdigest())
            self.assertTrue(source_record["historical_payload_unchanged"])

    def test_derived_latest_pointer_resolves_portably(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root)
            run = build(root)
            pointer = root / "outputs/section_means/latest_run.json"
            record = json.loads(pointer.read_text())
            record["run_directory"] = "/old/computer/section_means/" + run.name
            pointer.write_text(json.dumps(record))
            self.assertEqual(locate_run(root, "section_means"), run / "view_payload.json")

    def test_all_zero_differences_keep_nonzero_colour_range(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root, mode="zero_difference")
            run = build(root)
            derived = json.loads((run / "view_payload.json").read_text())
            for payload in derived["resolutions"].values():
                self.assertEqual(payload["color_scale"]["cmin"], -1)
                self.assertEqual(payload["color_scale"]["cmax"], 1)
                self.assertEqual(payload["arms"]["HK1"]["difference"][0][0], 0)

    def test_empty_arm_stays_blank_with_explicit_zero_arithmetic_and_null_stats(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root, mode="empty_arm")
            run = build(root)
            derived = json.loads((run / "view_payload.json").read_text())
            for payload in derived["resolutions"].values():
                self.assertEqual(payload["arms"]["PFKP"]["difference"], [[None, None], [None, None]])
                self.assertEqual(payload["arms"]["PFKP"]["raw_arithmetic_difference"], [[0, 0], [0, 0]])
                self.assertEqual(payload["statistics"]["PFKP"]["displayable_bins"], 0)
                self.assertIsNone(payload["statistics"]["PFKP"]["minimum_difference"])
                self.assertIsNone(payload["statistics"]["PFKP"]["maximum_difference"])

    def test_incomplete_cached_source_validation_cannot_publish_derived_run(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, payload = self.fixture(root)
            payload["validation"]["count_conservation_all_resolutions"] = False
            source.write_text(json.dumps(payload))
            with self.assertRaisesRegex(ValueError, "validation incomplete"):
                build(root)
            self.assertFalse((root / "outputs/section_means/latest_run.json").exists())


if __name__ == "__main__":
    unittest.main()
