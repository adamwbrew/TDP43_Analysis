"""Local detail must recount source points, retaining biological denominators."""
import json
from pathlib import Path
import shutil
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


def fixture():
    grid = {"x_edges": [0, 100, 200], "y_edges": [0, 100, 200],
            "bin_width_export_units": 100, "coordinate_units": "unverified export units"}
    sections, points, attributes = [], [], []
    for arm in ("HK1", "PFKP"):
        for condition in ("Homecage", "Running"):
            for i in range(3):
                sid = arm + "_" + condition + str(i)
                xy = [(150, 150)]
                if arm == "HK1":
                    xy = ({("Homecage", 0): [(1, 1), (24, 24), (25, 25), (50, 50),
                                              (100, 100), (200, 200), (150, 150)],
                           ("Homecage", 1): [(10, 10), (26, 26)],
                           ("Homecage", 2): [(150, 150)],
                           ("Running", 0): [(1, 1), (2, 2)],
                           ("Running", 1): [(20, 20)],
                           ("Running", 2): [(175, 175)]})[(condition, i)]
                counts = [[0, 0], [0, 0]]
                for x, y in xy:
                    counts[min(int(y // 100), 1)][min(int(x // 100), 1)] += 1
                sections.append({"section_id": sid, "animal_id": condition + str(i),
                    "physical_section_id": sid, "condition": condition, "pla_type": arm,
                    "pla_objects": len(xy), "pla_counts": counts,
                    "chat_counts": [[1, 2], [3, 4]], "observed_support": [[True] * 2] * 2})
                points.append({"section_id": sid, "source_sha256": "sha_" + sid,
                    "x": [p[0] for p in xy], "y": [p[1] for p in xy],
                    "native_x": [p[0] + 1000 for p in xy], "native_y": [p[1] + 2000 for p in xy],
                    "object_id": list(range(100, 100 + len(xy))),
                    "source_row": list(range(2, 2 + len(xy))), "point_count": len(xy), "sampled": False})
                attributes.append({"section_id": sid, "source_sha256": "sha_" + sid,
                    "point_order_sha256": "full_order_" + sid,
                    "area_um2": [(j + 1) / 10 for j in range(len(xy))],
                    "intensity": [(j + 1) * 100 for j in range(len(xy))],
                    "nearest_neighbor_distance": [(j + 1) * (10 if i == 0 else 100) for j in range(len(xy))],
                    "markers": {"chat": [j % 2 for j in range(len(xy))]}})
    base = {"grid": grid, "sections": sections, "arms": {
        "HK1": {"displayable": [[True, False], [False, True]]},
        "PFKP": {"displayable": [[True, True], [True, True]]}}}
    return {"base": base, "points": points, "features": {
        "available_markers": [{"id": "chat", "label": "ChAT"}], "sections": attributes},
        "window": {"xmin": 0, "xmax": 50, "ymin": 0, "ymax": 50},
        "binWidth": 25, "id": "pla_count"}


@unittest.skipUnless(shutil.which("node"), "Node is needed for the browser detail-grid engine")
class ExactDetailGridTests(unittest.TestCase):
    def run_helper(self, request):
        program = ("const fs=require('fs'),D=require(" + json.dumps(str(ROOT / "scripts/comet_detail_grid.js")) +
                   ");const q=JSON.parse(fs.readFileSync(0,'utf8')),before=JSON.stringify(q);"
                   "try{const result=D.calculate(q);console.log(JSON.stringify({result,unchanged:before===JSON.stringify(q)}));}"
                   "catch(error){console.log(JSON.stringify({error:error.message,unchanged:before===JSON.stringify(q)}));}")
        completed = subprocess.run([shutil.which("node"), "-e", program], input=json.dumps(request),
                                   capture_output=True, text=True, check=True, timeout=20)
        return json.loads(completed.stdout)

    def calculated(self, request):
        result = self.run_helper(request)
        self.assertTrue(result["unchanged"], "Rebinning must not mutate cached inputs")
        self.assertNotIn("error", result)
        return result["result"]

    def test_exact_source_rebinning_keeps_boundary_points_and_three_animal_weights(self):
        result = self.calculated(fixture())
        self.assertEqual(result["grid"]["x_edges"], [0, 25, 50])
        self.assertEqual(result["grid"]["y_edges"], [0, 25, 50])
        calculation = result["calculation"]
        self.assertEqual(len(calculation["sections"]), 12)
        self.assertEqual(calculation["sections"][0]["values"], [[2, 0], [0, 2]])
        # The upper-edge object at (50,50) stays in the last bin. Re-rendering
        # a coarse count matrix could not recover this exact four-way split.
        arm = calculation["arms"]["HK1"]
        self.assertEqual(arm["homecage_mean"], [[1, 0], [0, 1]])
        self.assertEqual(arm["running_mean"], [[1, 0], [0, 0]])
        self.assertEqual(arm["difference"], [[0, 0], [0, -1]])
        self.assertEqual(arm["homecage_valid_section_n"], [[3, 3], [3, 3]])

    def test_section_share_uses_full_section_total_including_objects_outside_detail(self):
        request = fixture(); request["id"] = "section_pla_share"
        result = self.calculated(request)["calculation"]
        self.assertAlmostEqual(result["sections"][0]["values"][0][0], 200 / 7)
        self.assertAlmostEqual(result["sections"][1]["values"][0][0], 50)
        self.assertEqual(result["sections"][2]["values"][0][0], 0)
        self.assertAlmostEqual(result["arms"]["HK1"]["homecage_mean"][0][0], (200 / 7 + 50) / 3)
        self.assertEqual(result["comparison"]["units"], "percentage points")

    def test_cached_full_section_neighbor_distances_are_sliced_not_recomputed(self):
        request = fixture(); request["id"] = "mean_pla_nearest_neighbor_distance"
        result = self.calculated(request)["calculation"]
        self.assertEqual(result["sections"][0]["values"][0][0], 15)
        self.assertEqual(result["sections"][1]["values"][0][0], 100)
        self.assertIsNone(result["sections"][2]["values"][0][0])
        arm = result["arms"]["HK1"]
        self.assertEqual(arm["homecage_mean"][0][0], 57.5)
        self.assertEqual(arm["homecage_valid_section_n"][0][0], 2)

    def test_marker_flags_and_areas_keep_source_order_after_nonprefix_selection(self):
        request = fixture(); request["id"] = "marker_associated_pla_area_fraction"
        request["window"] = {"xmin": 100, "xmax": 150, "ymin": 100, "ymax": 150}
        request["features"]["sections"][0]["markers"]["chat"] = [0, 0, 0, 0, 1, 0, 0]
        result = self.calculated(request)["calculation"]
        # Only source objects at indices 4 and 6 enter. The first is associated,
        # the second is not; taking a prefix of the feature cache would be wrong.
        self.assertEqual(result["sections"][0]["values"], [[1, None], [None, 0]])

    def test_regular_grid_covers_requested_window_and_counts_its_entire_extent(self):
        request = fixture(); request["window"] = {"xmin": -5, "xmax": 35, "ymin": -5, "ymax": 35}
        fine = self.calculated(request)
        self.assertEqual(fine["grid"]["x_edges"], [-25, 0, 25, 50])
        self.assertEqual(sum(map(sum, fine["calculation"]["sections"][0]["values"])), 4)
        request["binWidth"] = 100
        coarse = self.calculated(request)
        self.assertEqual(coarse["grid"]["x_edges"], [-100, 0, 100])
        self.assertEqual(sum(map(sum, coarse["calculation"]["sections"][0]["values"])), 5)
        # Point (100,100) enters the expanded coarse extent, rather than being
        # silently lost by filtering to a different requested-window extent.

    def test_domain_projects_baseline_centers_and_does_not_fill_undefined_metrics(self):
        request = fixture(); request["id"] = "mean_pla_area"
        request["window"] = {"xmin": 80, "xmax": 120, "ymin": 80, "ymax": 120}
        result = self.calculated(request)
        self.assertEqual(result["grid"]["x_edges"], [75, 100, 125])
        arm = result["calculation"]["arms"]["HK1"]
        self.assertEqual(arm["eligibility"], [[True, False], [False, True]])
        self.assertFalse(arm["displayable"][0][0])
        self.assertEqual(arm["missing_reason"][0][1], "outside_display_domain")
        self.assertFalse(result["calculation"]["coverage_verified"])

    def test_large_grid_invalid_window_and_misaligned_features_are_rejected(self):
        cases = []
        too_large = fixture(); too_large["window"]["xmax"] = 10025; cases.append((too_large, "400"))
        invalid = fixture(); invalid["window"]["ymax"] = 0; cases.append((invalid, "bounds"))
        feature = fixture(); feature["features"]["sections"][0]["area_um2"].pop(); cases.append((feature, "every source PLA"))
        source = fixture(); source["features"]["sections"][0]["source_sha256"] = "other"; cases.append((source, "source hash"))
        for request, message in cases:
            with self.subTest(message=message):
                result = self.run_helper(request)
                self.assertIn(message, result["error"])
                self.assertTrue(result["unchanged"])


if __name__ == "__main__":
    unittest.main()
