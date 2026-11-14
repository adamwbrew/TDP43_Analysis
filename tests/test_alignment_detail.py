"""Execute the JS coordinate/tile semantics without a browser or real specimens."""
import json
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts/comet_alignment_detail.js"


@unittest.skipUnless(shutil.which("node"), "Node is needed for the alignment JS acceptance checks")
class AlignmentDetailAcceptanceTests(unittest.TestCase):
    def evaluate(self, expression):
        program = SOURCE.read_text(encoding="utf-8") + "\nconst T=globalThis.COMET_ALIGNMENT_DETAIL;\n" + expression
        result = subprocess.run([shutil.which("node")], input=program, text=True,
                                capture_output=True, check=True, timeout=15)
        return json.loads(result.stdout)

    def test_native_reflection_reorders_rectangles_counts_and_support_exactly(self):
        result = self.evaluate("""
const section={fixed_transform:{matrix:[[-1,0,10],[0,1,-3],[0,0,1]]},
 pla_counts:[[3,0]],chat_counts:[[0,4]],observed_support:[[true,true]]};
const grid={x_edges:[0,1,2],y_edges:[0,1]};
const tile=T.nativeTileGrid(section,grid,'native');
const native=T.inversePoint(section.fixed_transform.matrix,[.5,.5]);
console.log(JSON.stringify({tile,native,recovered:T.forwardPoint(section.fixed_transform.matrix,native)}));
""")
        self.assertEqual(result["tile"]["x_edges"], [8, 9, 10])
        self.assertEqual(result["tile"]["y_edges"], [3, 4])
        self.assertEqual(result["tile"]["pla_counts"], [[0, 3]])
        self.assertEqual(result["tile"]["chat_counts"], [[4, 0]])
        self.assertEqual(result["tile"]["observed_support"], [[True, True]])
        self.assertEqual(result["tile"]["ix"], [1, 0])
        self.assertEqual(result["native"], [9.5, 3.5])
        self.assertEqual(result["recovered"], [.5, .5])

    def test_three_dimensional_tiles_are_constant_count_faces_and_leave_gaps(self):
        result = self.evaluate("""
const tile={x_edges:[0,1,2,3],y_edges:[0,1],pla_counts:[[3,0,0]],chat_counts:[[0,4,0]],observed_support:[[true,true,false]]};
console.log(JSON.stringify(T.exactTileMesh(tile,17)));
""")
        self.assertEqual(len(result["x"]), 8)
        self.assertEqual(len(result["i"]), 4)
        self.assertEqual(result["intensity"], [3, 3, 0, 0])
        self.assertEqual(result["z"], [17] * 8)
        self.assertNotIn(3, result["x"])  # The unobserved third bin has no tile.
        self.assertIn("PLA=0; ChAT=4", result["text"][4])
        source = SOURCE.read_text(encoding="utf-8")
        self.assertIn("intensitymode:'cell'", source)
        self.assertIn("zsmooth:false", source)

    def test_numeric_boundary_membership_is_single_and_outer_maximum_included(self):
        result = self.evaluate("console.log(JSON.stringify([0,1,2,-.01,2.01].map(v=>T.binIndex([0,1,2],v))));")
        self.assertEqual(result, [0, 1, 1, -1, -1])

    def test_native_points_use_every_stored_raw_coordinate_without_sampling(self):
        result = self.evaluate("""
const points={x:Array.from({length:5000},(_,i)=>i),y:Array(5000).fill(1),
 native_x:Array.from({length:5000},(_,i)=>i+123),native_y:Array(5000).fill(456)};
const p=T.pointCoordinates(points,'native');
console.log(JSON.stringify({length:p.x.length,first:p.x[0],last:p.x[4999],same:p.x===points.native_x,y:p.y[4999]}));
""")
        self.assertEqual(result, {"length": 5000, "first": 123, "last": 5122, "same": True, "y": 456})

    def test_rotated_native_bins_are_not_replaced_by_approximate_rectangles(self):
        result = self.evaluate("""
const section={fixed_transform:{matrix:[[0,-1,10],[1,0,20],[0,0,1]]},
 pla_counts:[[1]],chat_counts:[[0]],observed_support:[[true]]};
const grid={x_edges:[0,1],y_edges:[0,1]};
console.log(JSON.stringify({tile:T.nativeTileGrid(section,grid,'native'),point:T.inversePoint(section.fixed_transform.matrix,[7,22])}));
""")
        self.assertIsNone(result["tile"])
        self.assertEqual(result["point"], [2, 3])

    def test_no_app_or_multiresolution_does_not_require_dom_or_change_saved_renderer(self):
        result = self.evaluate("console.log(JSON.stringify({api:typeof T.exactTileMesh,app:typeof globalThis.COMET_CORE_EXPLORER}));")
        self.assertEqual(result, {"api": "function", "app": "undefined"})

    def test_shared_count_range_includes_larger_other_arm_and_preserves_values(self):
        result = self.evaluate("""
const sections=[{pla_type:'HK1',pla_counts:[[2,4]]},{pla_type:'PFKP',pla_counts:[[61,3]]}];
console.log(JSON.stringify({full:T.sharedCountRange(sections,'full'),capped:T.sharedCountRange(sections,'25'),raw:sections[1].pla_counts}));
""")
        self.assertEqual(result["full"], {"maximum": 61, "limit": 61})
        self.assertEqual(result["capped"], {"maximum": 61, "limit": 25})
        self.assertEqual(result["raw"], [[61, 3]])
        # The renderer must pass all current-resolution sections, rather than
        # the current arm or only visible/selected layers, into the tested helper.
        source = SOURCE.read_text(encoding="utf-8")
        self.assertIn("sharedCountRange(payload().sections,selected)", source)
        self.assertNotIn("countLimit(entries)", source)


if __name__ == "__main__":
    unittest.main()
