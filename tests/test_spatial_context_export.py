"""Exact detected-object context and genuine SVG tile exports, not pixel replicas."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import unittest
import xml.etree.ElementTree as ET

import numpy as np

from comet_spatial.context_geometry import footprint_geometry, build_context_geometry


ROOT = Path(__file__).resolve().parents[1]
SVG = '{http://www.w3.org/2000/svg}'


def ring():
    return {'x_edges':[-2,0,3,7], 'y_edges':[1,2,5,9]}, [[True]*3,[True,False,True],[True]*3]


def segments(context):
    return {tuple(sorted(((context['x'][i],context['y'][i]),(context['x'][i+1],context['y'][i+1]))))
            for i in range(0,len(context['x']),3)}


class DetectedObjectContextTests(unittest.TestCase):
    def test_exact_nonuniform_edges_preserve_inner_hole_and_do_not_mutate_inputs(self):
        grid,mask=ring();before=copy.deepcopy((grid,mask));context=footprint_geometry(grid,mask)
        expected={((-2,1),(7,1)),((-2,9),(7,9)),((-2,1),(-2,9)),((7,1),(7,9)),
                  ((0,2),(3,2)),((0,5),(3,5)),((0,2),(0,5)),((3,2),(3,5))}
        self.assertEqual(segments(context),expected)
        self.assertEqual(context['occupied_bin_count'],8)
        self.assertEqual(context['boundary_segments'],8)
        self.assertFalse(context['footprint'][1][1])
        self.assertFalse(context['holes_filled']);self.assertFalse(context['smoothing'])
        self.assertFalse(context['tissue_coverage_verified'])
        self.assertEqual((grid,mask),before)

    def test_disconnected_components_keep_their_gap_and_empty_context_stays_empty(self):
        grid={'x_edges':[0,2,5,9],'y_edges':[-3,1]}
        context=footprint_geometry(grid,[[True,False,True]])
        self.assertEqual(context['occupied_bin_count'],2)
        self.assertEqual(context['boundary_segments'],8)
        for (x0,y0),(x1,y1) in segments(context):
            self.assertFalse(x0==0 and x1==9)  # No boundary bridges the empty middle bin.
        empty=footprint_geometry(grid,[[False,False,False]])
        self.assertEqual(empty['x'],[]);self.assertEqual(empty['y'],[])
        self.assertEqual(empty['boundary_segments'],0)

    def test_context_source_fingerprint_ignores_selected_metric_values_and_uses_finest_grid(self):
        fine={'x_edges':[0,1,2,3],'y_edges':[0,1,2,3],'bin_width_export_units':1}
        mask=[[True]*3,[True,False,True],[True]*3]
        payload={'resolutions':{'3':{'grid':{'x_edges':[0,3],'y_edges':[0,3],'bin_width_export_units':3},
              'arms':{'HK1':{'displayable':[[True]]}}},
              '1':{'grid':fine,'arms':{'HK1':{'displayable':mask,'difference':[[1]*3 for _ in range(3)]}}}}}
        changed=copy.deepcopy(payload)
        changed['resolutions']['1']['arms']['HK1']['difference']=[[None]*3 for _ in range(3)]
        changed['resolutions']['1']['arms']['HK1']['running_mean']=[[None]*3 for _ in range(3)]
        changed['measurement']='An unrelated missing-valued object metric'
        one,two=build_context_geometry(payload)['HK1'],build_context_geometry(changed)['HK1']
        self.assertEqual(one['geometry_sha256'],two['geometry_sha256'])
        self.assertEqual(one['x'],two['x']);self.assertEqual(one['y'],two['y'])
        self.assertEqual(one['source_bin_width'],1)
        self.assertFalse(one['footprint'][1][1])

    def test_context_rejects_mismatched_or_nonincreasing_geometry(self):
        grid,mask=ring()
        with self.assertRaises(ValueError):footprint_geometry(grid,[[True]])
        grid['x_edges']=[0,2,1,3]
        with self.assertRaises(ValueError):footprint_geometry(grid,mask)


@unittest.skipUnless(shutil.which('node'),'Node is needed for the exact SVG exporter checks')
class VectorExportTests(unittest.TestCase):
    def export(self,options,extra=''):
        program="const fs=require('fs'),E=require("+json.dumps(str(ROOT/'scripts/comet_vector_export.js'))+");const o=JSON.parse(fs.readFileSync(0,'utf8'));"+extra+"const before=JSON.stringify(o);const source=E.svg(o);console.log(JSON.stringify({source,unchanged:before===JSON.stringify(o),nanRetained:Number.isNaN(o.z[1]?.[1]),infinityRetained:o.z[1]?.[2]===Infinity}));"
        result=subprocess.run([shutil.which('node'),'-e',program],input=json.dumps(options),capture_output=True,text=True,check=True,timeout=10)
        value=json.loads(result.stdout);return value,ET.fromstring(value['source'])

    def options(self,z=None):
        grid={'x_edges':[0,1,3,6],'y_edges':[0,2,5]}
        context=footprint_geometry(grid,[[True,True,False],[False,True,True]])
        return {'arm':'HK1','grid':grid,'z':z if z is not None else [[None,0,2],[-1,None,None]],
                'contextGeometry':context,'contextVisible':True,'measurementLabel':'Area <& "quoted" \'single\'',
                'comparisonLabel':'Running − Homecage','units':'µm² (exported)','binWidth':100,
                'zmin':-1,'zmax':1,'metadata':{'cutoff':.1,'marker':'chat','coverage_verified':True}}

    def test_svg_is_real_vector_with_exact_finite_tile_count_zero_values_and_safe_text(self):
        result,svg=self.export(self.options(),'o.z[1][1]=NaN;o.z[1][2]=Infinity;')
        self.assertTrue(result['unchanged']);self.assertTrue(result['nanRetained']);self.assertTrue(result['infinityRetained'])
        self.assertEqual(svg.findall('.//'+SVG+'image'),[])
        tiles=svg.find(".//"+SVG+"g[@id='calculated-tiles']")
        self.assertEqual(len(tiles.findall(SVG+'rect')),3)  # Includes the finite numerical zero.
        self.assertIn('#ffffff',[r.attrib['fill'] for r in tiles.findall(SVG+'rect')])
        self.assertIn('3 defined tiles', ''.join(svg.itertext()))
        self.assertIn('1 display-saturated', ''.join(svg.itertext()))
        metadata=json.loads(svg.find(SVG+'metadata').text)
        self.assertEqual(metadata['units'],'µm² (exported)')
        self.assertEqual(metadata['measurementLabel'],self.options()['measurementLabel'])
        self.assertTrue(metadata['vector_tiles']);self.assertFalse(metadata['coverage_verified'])
        self.assertEqual(svg.findall('.//'+SVG+'script'),[])
        self.assertIn('Area <& "quoted" \'single\'',svg.find(SVG+'title').text)

    def test_all_undefined_metric_still_draws_context_without_filling_its_hole(self):
        grid,mask=ring();context=footprint_geometry(grid,mask)
        options=self.options([[None]*3 for _ in range(3)])
        options.update(grid=grid,contextGeometry=context)
        result,svg=self.export(options)
        self.assertTrue(result['unchanged'])
        self.assertEqual(len(svg.find(".//"+SVG+"g[@id='calculated-tiles']")),0)
        footprints=svg.find(".//"+SVG+"g[@id='observed-object-footprint']").findall(SVG+'rect')
        self.assertEqual(len(footprints),4)  # Top, two side strips and bottom; no hole cell.
        # Source hole midpoint (1.5,3.5), transformed using the documented map projection.
        px,py=70+(1.5+2)*190,210+(3.5-1)*190
        self.assertFalse(any(float(r.attrib['x'])<px<float(r.attrib['x'])+float(r.attrib['width']) and
                             float(r.attrib['y'])<py<float(r.attrib['y'])+float(r.attrib['height']) for r in footprints))
        outline=svg.find(".//"+SVG+"path[@id='observed-object-outline']")
        self.assertIsNotNone(outline);self.assertEqual(outline.attrib['fill'],'none')
        self.assertEqual(outline.attrib['d'].count('M'),8)

    def test_context_can_be_hidden_without_changing_numerical_tiles(self):
        options=self.options();_,visible=self.export(options)
        options['contextVisible']=False;_,hidden=self.export(options)
        self.assertIsNone(hidden.find(".//"+SVG+"g[@id='observed-object-footprint']"))
        self.assertIsNone(hidden.find(".//"+SVG+"path[@id='observed-object-outline']"))
        a=visible.find(".//"+SVG+"g[@id='calculated-tiles']");b=hidden.find(".//"+SVG+"g[@id='calculated-tiles']")
        self.assertEqual([r.attrib for r in a],[r.attrib for r in b])

    def test_color_clamps_only_display_endpoints_and_rejects_invalid_limits(self):
        program="const E=require("+json.dumps(str(ROOT/'scripts/comet_vector_export.js'))+");console.log(JSON.stringify([-9,0,9].map(v=>E.color(v,-1,1,[[0,'#000000'],[1,'#ffffff']]))));"
        result=subprocess.run([shutil.which('node'),'-e',program],capture_output=True,text=True,check=True,timeout=10)
        self.assertEqual(json.loads(result.stdout),['#000000','#808080','#ffffff'])
        options=self.options();options['zmax']=options['zmin']
        with self.assertRaises(subprocess.CalledProcessError):self.export(options)

    def test_extreme_png_window_is_rejected_before_allocating_canvas_or_object_urls(self):
        options=self.options();options.update(format='png',width=12000,
            viewport={'xmin':0,'xmax':1,'ymin':0,'ymax':1000})
        program="""const fs=require('fs'),E=require(ENGINE);
const o=JSON.parse(fs.readFileSync(0,'utf8'));let allocated=false;
global.Blob=class {constructor(parts,options){this.parts=parts;this.type=options.type;}};
global.URL={createObjectURL(){allocated=true;throw Error('Unexpected resource allocation');}};
global.Image=class {constructor(){allocated=true;throw Error('Unexpected image allocation');}};
global.document={createElement(){allocated=true;throw Error('Unexpected canvas allocation');}};
(async()=>{try{await E.download(o);console.log(JSON.stringify({rejected:false,allocated}));}
catch(error){console.log(JSON.stringify({rejected:true,message:error.message,allocated}));}})();
""".replace('ENGINE',json.dumps(str(ROOT/'scripts/comet_vector_export.js')))
        result=subprocess.run([shutil.which('node'),'-e',program],input=json.dumps(options),capture_output=True,text=True,check=True,timeout=10)
        audit=json.loads(result.stdout)
        self.assertTrue(audit['rejected']);self.assertIn('too tall',audit['message'])
        self.assertFalse(audit['allocated'])


if __name__=='__main__':unittest.main()
