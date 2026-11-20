"""Selected-measurement UI semantics against the real calculation module."""
import csv
import io
import json
from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


FIXTURE = r"""
const assert=require('assert'),fs=require('fs');
var window={};const engine=require(process.argv[1]);
window.COMET_MEASUREMENTS=engine;
let resolution='100',mode='exploratory';const exploratory=()=>mode==='exploratory';
const conditions=['Homecage','Running'],arms=['HK1','PFKP'];
const C={grid:{x_edges:[0,1,2],y_edges:[0,1,2]},sections:[],arms:{}};
const MR={pla_points:[]},DATA={measurement_features:{schema_version:'comet-measurement-features-v1',validation:{all_selected_pla_objects_retained:true},available_markers:[{id:'chat',label:'ChAT'}],sections:[]}};
for(const arm of arms){
 C.arms[arm]={homecage_mean:[[1,0],[0,null]],running_mean:[[2,1/3],[0,null]],difference:[[1,1/3],[0,null]],displayable:[[true,true],[true,false]],homecage_observed_section_n:[[3,0],[0,0]],running_observed_section_n:[[3,1],[0,0]]};
 for(const condition of conditions)for(let i=0;i<3;i++){
  const running=condition==='Running',section_id=arm+'_'+condition+'_'+i,extra=running&&i===0;
  const p={section_id,source_sha256:'same-source',x:running?[.2,.3]:[.2],y:running?[.2,.3]:[.2]};
  const f={section_id,source_sha256:'same-source',area_um2:running?[.3,.5]:[.2],intensity:running?[.4,.6]:[.2],markers:{chat:running?[1,0]:[1]}};
  if(extra){p.x.push(1.2);p.y.push(.2);f.area_um2.push(.4);f.intensity.push(.7);f.markers.chat.push(1);}
  const pla_counts=[[running?2:1,extra?1:0],[0,0]];
  C.sections.push({section_id,physical_section_id:section_id,animal_id:condition+i,condition,pla_type:arm,pla_counts,chat_counts:[[0,0],[0,0]],observed_support:pla_counts.map(row=>row.map(n=>n>0))});MR.pla_points.push(p);DATA.measurement_features.sections.push(f);
 }
}
const baseline=JSON.stringify(C),featuresBefore=JSON.stringify(DATA.measurement_features);
const num=n=>String(n),nMatrix=(d,c)=>d[c==='Running'?'running_observed_section_n':'homecage_observed_section_n'];
"""


class MeasurementUiTests(unittest.TestCase):
    def run_node(self, body):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node is needed for selected-measurement UI checks")
        script = FIXTURE + (ROOT / "scripts/comet_measurement_controls.js").read_text() + body
        result = subprocess.run([node, "-e", script, str(ROOT / "scripts/comet_measurements.js")],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def test_primary_mean_retains_defined_condition_when_comparison_is_undefined(self):
        self.run_node(r"""
measurementId='mean_pla_area';comparisonId='percent_change';
const active=measurementResult();
assert.equal(active.arms.HK1.homecage_mean[0][1],null);
assert.equal(active.arms.HK1.running_mean[0][1],.4);
assert.equal(active.arms.HK1.homecage_valid_section_n[0][1],0);
assert.equal(active.arms.HK1.running_valid_section_n[0][1],1);
assert.equal(shownMetricMatrix('HK1','difference')[0][1],null,'undefined comparison stays blank');
assert.equal(shownMetricMatrix('HK1','running_mean')[0][1],.4,'available mean must remain inspectable');
assert.equal(shownMetricMatrix('HK1','running_mean')[1][1],null,'outside recorded domain remains blank');
assert.equal(metricUnits(), 'µm² (exported)');assert.equal(metricUnits(true),'%');
assert.equal(JSON.stringify(C),baseline);assert.equal(JSON.stringify(DATA.measurement_features),featuresBefore);
""")

    def test_selection_changes_do_not_reuse_stale_statistics_or_coerce_undefined_to_zero(self):
        self.run_node(r"""
measurementId='large_pla_count';areaCutoff=.35;
assert.equal(measurementResult().arms.HK1.homecage_mean[0][0],0);
assert.equal(measurementResult().arms.HK1.running_mean[0][0],1);
areaCutoff=.6;assert.equal(measurementResult().arms.HK1.running_mean[0][0],0,'threshold is part of selection cache key');
measurementId='mean_pla_area';comparisonId='absolute_difference';
assert(Math.abs(shownMetricMatrix('HK1','difference')[0][0]-.2)<1e-14);
const intensive=metricSectionValues(C.sections[0]);assert.equal(intensive[0][1],null);
measurementId='pla_count';assert.equal(metricSectionValues(C.sections[0])[0][1],0,'count empty remains numeric zero');
assert.equal(shownMetricMatrix('HK1','difference')[0][0],1);
assert.equal(formatMeasurement(.000003),'0.000003','small area is not rounded to zero');
assert.equal(formatMeasurement(null),'undefined');assert.equal(JSON.stringify(C),baseline);
""")

    def test_missing_feature_cache_preserves_baseline_but_rejects_other_measurements(self):
        self.run_node(r"""
DATA.measurement_features={};
assert.equal(measurementFeaturesAvailable(),false);
assert.equal(measurementResult(),C,'existing PLA count baseline remains viewable');
measurementId='mean_pla_area';
assert.throws(()=>measurementResult(),/Validated object features are unavailable/);
assert.equal(JSON.stringify(C),baseline,'no substituted statistic or mutated count data');
""")

    def test_selected_csv_includes_units_valid_n_raw_support_and_missing_reason(self):
        output = self.run_node(r"""
measurementId='mean_pla_area';comparisonId='percent_change';let captured='',filename='';
global.Blob=class{constructor(parts){this.contents=parts.join('');}};
global.URL={createObjectURL(blob){captured=blob.contents;return 'blob:fixture';},revokeObjectURL(){}};
global.document={createElement(){return {href:'',download:'',click(){filename=this.download;}};}};
global.setTimeout=fn=>fn();downloadMeasurementTable('HK1');
console.log(JSON.stringify({csv:captured,filename,baselineIntact:JSON.stringify(C)===baseline}));
""")
        value = json.loads(output)
        self.assertTrue(value["baselineIntact"])
        self.assertIn("mean_pla_area_percent_change", value["filename"])
        rows = list(csv.DictReader(io.StringIO(value["csv"])))
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0]["measurement_units"], "µm² (exported)")
        self.assertEqual(rows[0]["comparison_units"], "%")
        self.assertEqual(rows[1]["homecage_defined_measurement_sections"], "0")
        self.assertEqual(rows[1]["running_defined_measurement_sections"], "1")
        self.assertEqual(rows[1]["homecage_observed_support_N"], "0")
        self.assertEqual(rows[1]["selected_comparison"], "")
        self.assertEqual(rows[1]["missing_reason"], "undefined_homecage_mean")
        self.assertEqual(rows[1]["tissue_coverage_verified"], "false")
        self.assertEqual(rows[1]["HK1_Homecage_0__measurement_value"], "")

    def test_actual_controls_cover_pdf_functions_and_bootstrap_engine_before_views(self):
        template = (ROOT / "scripts/comet_core_explorer.html").read_text()

        class Controls(HTMLParser):
            def __init__(self):
                super().__init__(); self.ids=[]; self.selection=None; self.options={}
            def handle_starttag(self, tag, attrs):
                attrs=dict(attrs)
                if "id" in attrs: self.ids.append(attrs["id"])
                if tag=="select": self.selection=attrs.get("id"); self.options[self.selection]=[]
                if tag=="option" and self.selection: self.options[self.selection].append(attrs.get("value"))
            def handle_endtag(self, tag):
                if tag=="select": self.selection=None
        parser=Controls(); parser.feed(template)
        self.assertEqual(len(parser.ids),len(set(parser.ids)))
        self.assertEqual(len(parser.options["measurement-function"]),13)
        self.assertEqual(parser.options["comparison-function"],["absolute_difference","percent_change","log2_fold_change"])
        self.assertEqual(parser.options["measurement-marker"],["chat"])
        self.assertEqual(parser.options["focus-bin-width"],["100","50","25","10"])
        self.assertNotIn("measurement-export-width",parser.ids)
        self.assertEqual(parser.options["measurement-export-region"],["whole","zoom","detail"])
        for identifier in ["area-cutoff","apply-area-cutoff","custom-color-limit","apply-color-limit","measurement-error",
                           "show-object-context","export-hk1-png","export-pfkp-png","export-hk1-svg","export-pfkp-svg",
                           "open-fine-detail"]:
            self.assertIn(identifier,parser.ids)
        self.assertIn('PNG: 8,000 pixels wide. SVG: scalable vector.', template)
        self.assertIn('Current map zoom · existing bins', template)
        self.assertIn('Fine detailed window · recomputed bins', template)
        self.assertIn('Spatial detail: calculated bin width', template)
        self.assertLess(template.index("__MEASUREMENT_ENGINE_JS__"),template.index("'use strict';const DATA="))
        self.assertLess(template.index("__MEASUREMENT_CONTROLS_JS__"),template.index("initializeMeasurements();"))

    def test_footprint_is_metric_independent_vector_boundary_and_does_not_fill_missing_values(self):
        self.run_node(r"""
const nodes={'show-object-context':{checked:true}},Q=id=>nodes[id];
DATA.context_geometry={HK1:{grid:C.grid,footprint:[[true,false],[true,true]],x:[0,1,1,0,0,null,1,2],y:[0,0,1,1,0,null,1,1]}};
const geometryBefore=JSON.stringify(DATA.context_geometry),first=observedFootprintTraces('HK1');
assert.equal(first.length,2);assert.equal(first[0].type,'heatmap');assert.equal(first[0].z[0][1],null,'footprint holes stay holes');
assert.equal(first[1].type,'scatter','outline stays vector, not WebGL or raster image');
assert.equal(first[1].connectgaps,false);assert.equal(first[1].line.simplify,false);
measurementId='mean_pla_area';const missing=shownMetricMatrix('HK1','difference')[0][1];assert.equal(missing,null);
assert.deepEqual(observedFootprintTraces('HK1'),first,'selected statistic cannot change observation context');
assert.equal(shownMetricMatrix('HK1','difference')[0][1],null,'context does not impute unavailable measurements');
nodes['show-object-context'].checked=false;assert.deepEqual(observedFootprintTraces('HK1','all',observedContextVisible()),[]);
assert.equal(JSON.stringify(DATA.context_geometry),geometryBefore);assert.equal(JSON.stringify(C),baseline);
""")

    def test_catalog_drives_all_nineteen_controls_and_section_share_uses_percentage_points(self):
        self.run_node(r"""
const nodes={},Q=id=>nodes[id]||(nodes[id]={value:'',disabled:false,options:[]});
const esc=v=>String(v);Q('measurement-function').value='pla_count';
window.COMET_VECTOR_EXPORT={download(){}};initializeMeasurements();
assert.equal((Q('measurement-function').innerHTML.match(/<option /g)||[]).length,19);
for(const metric of engine.MEASUREMENTS)assert(Q('measurement-function').innerHTML.includes('value="'+metric.id+'"'));
measurementId='section_pla_share';assert.equal(metricUnits(),'% of section PLA');assert.equal(metricUnits(true),'percentage points');
comparisonId='percent_change';assert.equal(metricUnits(true),'%');
assert.equal(Q('export-hk1-png').disabled,false);assert.equal(typeof Q('export-pfkp-svg').onclick,'function');
let scrolls=0,focuses=0;Q('focus-workspace').hidden=false;Q('focus-workspace').scrollIntoView=()=>scrolls++;
Q('focus-bin-width').value='50';Q('focus-bin-width').focus=()=>focuses++;
Q('open-fine-detail').onclick();assert.equal(scrolls,1);assert.equal(focuses,1);
assert.equal(Q('focus-bin-width').value,'50','opening detail preserves the selected scientific bin width');
assert.equal(measurementId,'section_pla_share','navigation does not change the selected statistic');
""")

    def test_detail_rebin_is_bounded_cached_and_exports_its_actual_grid_and_provenance(self):
        self.run_node(r"""
const nodes={'focus-bin-width':{value:'10'},'mean-view':{value:'difference'},'measurement-export-region':{value:'detail'},'signed-range':{value:'full'},'show-object-context':{checked:true}},Q=id=>nodes[id];
let focusWindow={xmin:0,xmax:8000,ymin:0,ymax:8000},sharedViewport=null,calls=[];
MR.resolutions={'100':C};DATA.measurement_feature_payload_sha256='features-hash';DATA.measurement_features.source_count_payload_sha256='count-hash';
window.COMET_DETAIL_GRID={calculate(options){calls.push(options);return {grid:{x_edges:[0,25,50],y_edges:[0,25,50]},calculation:measurementResult()};}};
const colorDisplayScale=()=>({zmin:-2,zmax:2});
let detail=detailAnalysis();assert.equal(detail.binWidth,25,'8k window needs automatic bound rather than huge10-unit allocation');
assert(detail.note.includes('adjusted'));assert.equal(nodes['focus-bin-width'].value,'25');
detailAnalysis();assert.equal(calls.length,1,'same region calculation reused');
measurementId='mean_pla_area';detailAnalysis();assert.equal(calls.length,2,'different statistic recalculates');
assert.equal(calls[0].base,C);assert.equal(calls[0].points,MR.pla_points);assert.equal(calls[0].binWidth,25);
const exported=selectedExportOptions('HK1');assert.deepEqual(exported.grid.x_edges,[0,25,50]);assert.equal(exported.binWidth,25);
assert.equal(exported.z[0][1],null,'export preserves undefined comparison');
assert.equal(exported.metadata.source_features_sha256,'features-hash');assert.equal(exported.metadata.source_count_payload_sha256,'count-hash');
assert.equal(exported.metadata.tissue_coverage_verified,false);assert.equal(exported.viewport.xmax,8000);
focusWindow={xmin:0,xmax:100000,ymin:0,ymax:100000};assert.throws(()=>detailAnalysis(),/too large/);
assert.equal(JSON.stringify(C),baseline);assert.equal(JSON.stringify(DATA.measurement_features.sections),JSON.stringify(JSON.parse(featuresBefore).sections));
""")

    def test_export_uses_explicit_eight_k_width_reports_errors_and_prevents_parallel_allocations(self):
        self.run_node(r"""
const nodes={},Q=id=>nodes[id]||(nodes[id]={value:'',dataset:{},disabled:false,textContent:''});
Q('mean-view').value='difference';Q('signed-range').value='full';Q('measurement-export-region').value='whole';
const focusWindow=null,sharedViewport=null,colorDisplayScale=()=>({zmin:-1,zmax:1});let calls=[],finish;
window.COMET_VECTOR_EXPORT={download(options){calls.push(options);options.onProgress('Drawing exact vector bins');return new Promise(resolve=>finish=()=>resolve({width:8000,height:8200}));}};
global.setTimeout=fn=>fn();
(async()=>{
 const first=exportMeasurementImage('HK1','png');await Promise.resolve();
 assert.equal(calls.length,1);assert.equal(calls[0].width,8000);assert.equal(calls[0].format,'png');assert(calls[0].filename.endsWith('_8000px'));assert(Q('export-hk1-png').disabled);
 await exportMeasurementImage('PFKP','png');assert.equal(calls.length,1,'one bitmap allocation at a time');
 finish();await first;assert.equal(Q('measurement-export-status').dataset.state,'ready');assert.equal(Q('export-hk1-png').disabled,false);
 window.COMET_VECTOR_EXPORT.download=async options=>{calls.push(options);return {width:8000,height:8200};};
 await exportMeasurementImage('HK1','png');assert.equal(calls[1].width,8000);assert(calls[1].filename.endsWith('_8000px'));
 assert.deepEqual(calls[1].z,calls[0].z,'fixed-size exports preserve the calculated values');
 assert.deepEqual(calls[1].grid,calls[0].grid,'fixed-size exports preserve the recorded grid');
 await exportMeasurementImage('HK1','svg');assert(calls[2].filename.endsWith('_vector'));
 window.COMET_VECTOR_EXPORT.download=async()=>{throw Error('Canvas memory limit');};await exportMeasurementImage('PFKP','png');
 assert.equal(Q('measurement-export-status').dataset.state,'error');assert(Q('measurement-export-status').textContent.includes('Canvas memory limit'));
 assert.equal(Q('export-pfkp-svg').disabled,false,'failed raster export does not strand controls');
})().catch(error=>{console.error(error);process.exitCode=1;});
""")


if __name__ == "__main__":
    unittest.main()
