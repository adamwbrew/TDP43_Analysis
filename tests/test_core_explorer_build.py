"""Offline core-view assembly must preserve source pixels and blocked states."""
import base64
import hashlib
import json
import re
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.build_comet_core_explorer import build, load_exploratory, load_multiresolution


class CoreExplorerBuildTests(unittest.TestCase):
    def fixture(self, directory, changed=False):
        root = Path(directory)
        image = root / "saved-reference.png"
        image.write_bytes(b"unchanged-original-alignment-image")
        audit = {"saved_app_snapshot": {
            "sections": [{"job": "source-only"}],
            "alignment_check": {"source_path": str(image),
                                "sha256": "wrong" if changed else hashlib.sha256(image.read_bytes()).hexdigest()},
        }}
        path = root / "outputs/comet_core/asset_audit.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(audit))
        return root, image

    def test_missing_core_stays_blocked_and_reference_pixels_are_embedded(self):
        with tempfile.TemporaryDirectory() as directory:
            root, image = self.fixture(directory)
            with patch("scripts.build_comet_core_explorer.get_plotlyjs", return_value="/* inline Plotly */"):
                result = build(root)
            self.assertEqual(result["status"], "blocked")
            self.assertEqual(result["saved_alignment_sections"], 1)
            html = Path(result["path"]).read_text()
            self.assertIn(base64.b64encode(image.read_bytes()).decode(), html)
            self.assertIn('"arms":{}', html)
            self.assertNotIn("__PAYLOAD__", html)
            self.assertNotIn("__PLOTLY__", html)
            self.assertNotRegex(html, r'<script[^>]+src=["\']https?://')

    def test_identical_replay_is_verified_without_embedding_duplicate_pixels(self):
        with tempfile.TemporaryDirectory() as directory:
            root, image = self.fixture(directory)
            figure_dir = root / "outputs/comet_core/figures"
            figure_dir.mkdir()
            for kind in ("reference", "reproduced"):
                (figure_dir / ("alignment_check_%s.png" % kind)).write_bytes(image.read_bytes())
            digest = hashlib.sha256(image.read_bytes()).hexdigest()
            (root / "outputs/comet_core/alignment_replay_validation.json").write_text(json.dumps({
                "pixel_identical_to_saved_reference": True, "transforms_unchanged": True,
                "reference_sha256": digest, "reproduced_png_sha256": digest,
            }))
            with patch("scripts.build_comet_core_explorer.get_plotlyjs", return_value="/* inline Plotly */"):
                result = build(root)
            html = Path(result["path"]).read_text()
            self.assertIn('"display_claim_verified":true', html)
            self.assertEqual(html.count("data:image/png;base64,"), 1)

    def test_fresh_clone_embeds_local_reference_when_original_machine_is_unavailable(self):
        with tempfile.TemporaryDirectory() as directory:
            root, original = self.fixture(directory)
            local = root / "outputs/comet_core/figures/alignment_check_reference.png"
            local.parent.mkdir()
            local.write_bytes(original.read_bytes())
            original.unlink()
            with patch("scripts.build_comet_core_explorer.get_plotlyjs", return_value="/* inline Plotly */"):
                result = build(root)
            self.assertIn(base64.b64encode(local.read_bytes()).decode(), Path(result["path"]).read_text())

    def test_changed_local_reference_is_rejected_even_when_original_pixels_are_available(self):
        with tempfile.TemporaryDirectory() as directory:
            root, original = self.fixture(directory)
            local = root / "outputs/comet_core/figures/alignment_check_reference.png"
            local.parent.mkdir()
            local.write_bytes(b"changed local pixels")
            self.assertTrue(original.is_file())
            with self.assertRaisesRegex(ValueError, "image hash changed"):
                build(root)

    def exploratory_fixture(self, root, strict_result=False):
        directory = root / "outputs/exploratory/immutable-test-run"
        directory.mkdir(parents=True)
        payload = {"status": "exploratory_ready", "strict_pdf_results": strict_result,
                   "analysis_kind": "observed_object_support_exploratory", "arms": {},
                   "validation": {key: True for key in ("count_conservation_passed",
                       "input_hashes_verified_before_and_after", "fixed_transforms_unchanged", "all_raw_objects_counted")}}
        (directory / "view_payload.json").write_text(json.dumps(payload))
        (directory.parent / "latest_run.json").write_text(json.dumps({
            "run_directory": str(directory), "payload_file": "view_payload.json"}))

    def test_exploratory_payload_remains_separate_from_blocked_strict_results(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self.fixture(directory)
            self.exploratory_fixture(root)
            with patch("scripts.build_comet_core_explorer.get_plotlyjs", return_value="/* inline Plotly */"):
                result = build(root)
            self.assertEqual(result["status"], "exploratory_ready")
            self.assertEqual(result["strict_pdf_status"], "blocked")
            html = Path(result["path"]).read_text()
            self.assertIn('"strict_pdf_results":false', html)
            self.assertIn('"analysis_kind":"observed_object_support_exploratory"', html)

    def test_portable_copy_loads_local_run_when_recorded_absolute_location_is_gone(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self.fixture(directory)
            self.exploratory_fixture(root)
            pointer = root / "outputs/exploratory/latest_run.json"
            latest = json.loads(pointer.read_text())
            local_run = Path(latest["run_directory"])
            missing_original = root / "unavailable-original-workspace" / local_run.name
            self.assertFalse(missing_original.exists())
            latest["run_directory"] = str(missing_original)
            pointer.write_text(json.dumps(latest))
            payload = load_exploratory(root)
            self.assertEqual(payload["status"], "exploratory_ready")
            self.assertEqual(Path(payload["saved_payload_path"]), local_run / "view_payload.json")
            # The copied run also takes precedence if the former location later
            # returns, so a presentation refresh cannot silently use another copy.
            missing_original.mkdir(parents=True)
            alternate = json.loads((local_run / "view_payload.json").read_text())
            alternate["analysis_kind"] = "other_original_copy"
            (missing_original / "view_payload.json").write_text(json.dumps(alternate))
            self.assertEqual(load_exploratory(root)["analysis_kind"], "observed_object_support_exploratory")

    def test_exploratory_payload_cannot_claim_to_be_strict_pdf_result(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self.fixture(directory)
            self.exploratory_fixture(root, strict_result=True)
            with self.assertRaisesRegex(ValueError, "separate from strict PDF"):
                load_exploratory(root)

    def test_mode_bootstrap_targets_exist_in_real_initial_html_or_earlier_markup(self):
        # Inspect the real template's DOM, not a getElementById stub that invents
        # missing elements. This catches null textContent assignments on startup.
        from scripts.build_comet_core_explorer import ROOT
        template = (ROOT / "scripts/comet_core_explorer.html").read_text()
        initial_html = template[:template.rfind("<script>")]

        class IdParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.ids = []

            def handle_starttag(self, tag, attrs):
                self.ids.extend(value for key, value in attrs if key == "id")

        parser = IdParser()
        parser.feed(initial_html)
        self.assertEqual(len(parser.ids), len(set(parser.ids)), "Duplicate initial DOM IDs")
        initial_ids = set(parser.ids)
        start = template.index("function applyModeText()")
        stop = template.index("function downloadArmTable(", start)
        bootstrap = template[start:stop]
        created = {}
        for match in re.finditer(r'id=["\']([^"\']+)["\']', bootstrap):
            created.setdefault(match.group(1), []).append(match.start())
        for lookup in re.finditer(r"Q\('([^']+)'\)", bootstrap):
            identifier = lookup.group(1)
            self.assertTrue(identifier in initial_ids or any(
                position < lookup.start() for position in created.get(identifier, [])
            ), "Mode bootstrap queries missing DOM target: " + identifier)

    def multiresolution_fixture(self, root):
        directory = root / "outputs/exploratory_multiresolution/immutable-four-grid-run"
        directory.mkdir(parents=True)
        payload = {"schema_version": "comet-multiresolution-v1",
                   "resolutions": {width: {"strict_pdf_results": False} for width in ("1000", "500", "250", "100")},
                   "validation": {key: True for key in ("count_conservation_all_resolutions",
                       "full_pla_point_count_matches_raw", "hashes_verified_before_after_and_before_publication", "fixed_transforms_unchanged")},
                   "pla_points": [{"section_id": "source_section", "sampled": False,
                       "x": [1.25], "y": [-2.5], "object_id": ["object_7"], "source_row": [8]}]}
        payload["validation"]["full_pla_point_count"] = 1
        path = directory / "view_payload.json"
        path.write_text(json.dumps(payload))
        (directory.parent / "latest_run.json").write_text(json.dumps({
            "run_directory": str(directory), "payload_file": path.name}))
        return path, payload

    def test_multiresolution_loader_preserves_complete_points_and_uses_portable_run(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self.fixture(directory)
            path, expected = self.multiresolution_fixture(root)
            pointer = path.parent.parent / "latest_run.json"
            pointer.write_text(json.dumps({"run_directory": "/unavailable/original/" + path.parent.name,
                                           "payload_file": path.name}))
            payload = load_multiresolution(root)
            self.assertEqual(payload["pla_points"], expected["pla_points"])
            self.assertEqual(Path(payload["saved_payload_path"]), path)
            self.assertEqual(set(payload["resolutions"]), {"1000", "500", "250", "100"})

    def test_current_maps_report_ready_without_historical_exploratory_run(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self.fixture(directory)
            path, payload = self.multiresolution_fixture(root)
            payload["default_resolution"] = 100
            payload["resolutions"]["100"]["status"] = "exploratory_ready"
            path.write_text(json.dumps(payload))
            self.assertFalse((root / "outputs/exploratory/latest_run.json").exists())
            with patch("scripts.build_comet_core_explorer.get_plotlyjs", return_value="/* inline Plotly */"):
                result = build(root)
            self.assertEqual(result["status"], "exploratory_ready")
            self.assertEqual(result["strict_pdf_status"], "blocked")

    def test_multiresolution_loader_rejects_failed_validation_and_incomplete_points(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self.fixture(directory)
            path, payload = self.multiresolution_fixture(root)
            for flag in ("count_conservation_all_resolutions", "full_pla_point_count_matches_raw",
                         "hashes_verified_before_after_and_before_publication", "fixed_transforms_unchanged"):
                with self.subTest(flag=flag):
                    payload["validation"][flag] = False
                    path.write_text(json.dumps(payload))
                    with self.assertRaisesRegex(ValueError, "validation is incomplete"):
                        load_multiresolution(root)
                    payload["validation"][flag] = True
            payload["validation"]["full_pla_point_count"] = 2
            path.write_text(json.dumps(payload))
            with self.assertRaisesRegex(ValueError, "does not match recorded source count"):
                load_multiresolution(root)
            payload["validation"]["full_pla_point_count"] = 1
            payload["pla_points"][0]["sampled"] = True
            path.write_text(json.dumps(payload))
            with self.assertRaisesRegex(ValueError, "complete and unsampled"):
                load_multiresolution(root)

    def test_support_module_dom_targets_and_namespace_match_real_markup(self):
        from scripts.build_comet_core_explorer import ROOT
        template = (ROOT / "scripts/comet_core_explorer.html").read_text()
        module = (ROOT / "scripts/comet_support_detail.js").read_text()

        class IdParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.ids = []

            def handle_starttag(self, tag, attrs):
                self.ids.extend(value for key, value in attrs if key == "id")

        initial = IdParser()
        initial.feed(template[:template.index("'use strict';const DATA=")])
        start = module.index("root.innerHTML=`") + len("root.innerHTML=`")
        stop = module.index("`;", start)
        markup = IdParser()
        markup.feed(module[start:stop])
        self.assertEqual(len(markup.ids), len(set(markup.ids)), "Duplicate support-module IDs")
        self.assertFalse(set(markup.ids) & set(initial.ids), "Support controls collide with core controls")
        known = set(initial.ids) | set(markup.ids) | {"comet-support-detail"}
        targets = set(re.findall(r"Q\('([^']+)'\)", module))
        self.assertTrue(targets <= known, "Unknown real DOM targets: " + str(targets - known))
        self.assertIn("__SUPPORT_DETAIL_JS__", template)
        self.assertIn("__ALIGNMENT_DETAIL_JS__", template)

    def test_plot_lifecycle_measures_hidden_views_refits_and_releases_contexts(self):
        # This fixture models real ancestor-hidden geometry: an unstaged hidden
        # graph has zero width/height and native Plotly refuses to draw it. It
        # does not invent DOM IDs or return a fabricated element for lookups.
        node = shutil.which("node")
        if not node:
            self.skipTest("Node is needed for the injected plot/DOM lifecycle check")
        from scripts.build_comet_core_explorer import ROOT
        fixture = r"""const assert=require('assert');
const {createPlotLifecycle}=require(process.argv[1]);
const events=[], ids=new Map();
class Element {
 constructor(tag,id=''){this.tagName=tag.toUpperCase();this.id=id;this.children=[];this.parentNode=null;this.hidden=false;this.dataset={};this.attributes={};this.style={cssText:''};this.width=1100;this.height=500;this._html='';if(id)ids.set(id,this);}
 get isConnected(){return this.tagName==='MAIN'||!!this.parentNode?.isConnected;}
 appendChild(child){if(child.parentNode)child.parentNode.children=child.parentNode.children.filter(x=>x!==child);child.parentNode=this;this.children.push(child);return child;}
 insertBefore(child,before){if(child.parentNode)child.parentNode.children=child.parentNode.children.filter(x=>x!==child);child.parentNode=this;this.children.splice(this.children.indexOf(before),0,child);}
 remove(){if(this.parentNode)this.parentNode.children=this.parentNode.children.filter(x=>x!==this);this.parentNode=null;}
 contains(child){return child===this||this.children.some(x=>x.contains(child));}
 closest(selector){for(let x=this;x;x=x.parentNode){if(selector==='main'&&x.tagName==='MAIN')return x;if(selector==='[role="tabpanel"]'&&x.attributes.role==='tabpanel')return x;if(selector==='[hidden]'&&x.hidden)return x;}return null;}
 getAttribute(name){if(name==='style')return this.style.cssText||null;return this.attributes[name]??null;}
 setAttribute(name,value){if(name==='style')this.style.cssText=value;else this.attributes[name]=String(value);}
 removeAttribute(name){if(name==='style')this.style.cssText='';else delete this.attributes[name];}
 getBoundingClientRect(){if(!this.isConnected||this.closest('[hidden]'))return {width:0,height:0};const p=this.closest('[role="tabpanel"]');let width=this.width;if(p?.dataset.cometStaging){const m=p.style.cssText.match(/width:([\d.]+)px/);width=m?+m[1]:0;}return {width,height:this.height};}
 querySelectorAll(selector){let children=this.children.flatMap(c=>[c,...c.querySelectorAll(selector)]);if(selector==='img[src]')return children.filter(x=>x.tagName==='IMG'&&x.src);return children;}
 addEventListener(){}
 async decode(){events.push('decode:'+this.id);}
}
Object.defineProperty(Element.prototype,'innerHTML',{configurable:true,get(){return this._html;},set(value){events.push('replace:'+this.id);for(const child of this.children)child.parentNode=null;this.children=[];this._html=value;}});
const main=new Element('main','main');main.width=1200;
const listeners=new Map(),status=new Element('div','plot-readiness');main.appendChild(status);
const doc={readyState:'loading',fonts:{ready:Promise.resolve().then(()=>events.push('fonts'))},getElementById:id=>ids.get(id)||null,querySelector(selector){if(selector==='main')return main;if(selector==='[role="tabpanel"]:not([hidden])')return main.children.find(x=>x.attributes.role==='tabpanel'&&!x.hidden)||null;return null;},querySelectorAll:selector=>main.querySelectorAll(selector),createElement:tag=>new Element(tag),addEventListener(name,fn){if(!listeners.has(name))listeners.set(name,[]);listeners.get(name).push(fn);},dispatchEvent(event){for(const fn of listeners.get(event.type)||[])fn(event);}};
function makePanel(name,hidden){const panel=new Element('section','panel-'+name);panel.attributes.role='tabpanel';panel.attributes['aria-labelledby']='tab-'+name;panel.hidden=hidden;const tab=new Element('button','tab-'+name);tab.attributes['aria-selected']=hidden?'false':'true';main.appendChild(tab);main.appendChild(panel);const plot=new Element('div',name+'-plot');panel.appendChild(plot);return {panel,plot,tab};}
const dif=makePanel('differences',false),ali=makePanel('alignment',true),cov=makePanel('coverage',true);
const nativeRenders=[];
function nativePlot(value,data,layout,config){const el=typeof value==='string'?ids.get(value):value;const r=el.getBoundingClientRect();assert(r.width>0&&r.height>0,'native Plotly must never initialize at zero size');nativeRenders.push({id:el.id,width:layout.width,height:layout.height});el.data=data;el.layout=JSON.parse(JSON.stringify(layout));el.config=config;el.handlers={};el.on=function(name,fn){if(!this.handlers[name])this.handlers[name]=[];this.handlers[name].push(fn);return this;};el.removeAllListeners=function(name){if(name)delete this.handlers[name];else this.handlers={};return this;};return Promise.resolve(el);}
const P={newPlot:nativePlot,react:nativePlot,relayout(el,update){if(typeof el==='string')el=ids.get(el);for(const [key,value]of Object.entries(update)){const [a,b]=key.split('.');if(b){el.layout[a]||={};el.layout[a][b]=value;}else el.layout[a]=value;}events.push('fit:'+el.id);return Promise.resolve(el);},purge(el){events.push('purge:'+el.id);el.removeAllListeners?.();delete el.data;delete el.layout;delete el.on;delete el.removeAllListeners;},toImage:async el=>'data:image/png;base64,'+el.id,Plots:{resize:async()=>{throw Error('Uncontrolled Plotly resize');}}};
let resizeObserver;
const env={document:doc,Plotly:P,Element,innerWidth:1200,getComputedStyle:()=>({paddingLeft:'34',paddingRight:'34'}),requestAnimationFrame:fn=>setImmediate(fn),setTimeout,CustomEvent:class{constructor(type,options={}){this.type=type;this.detail=options.detail;}},ResizeObserver:class{constructor(callback){this.callback=callback;resizeObserver=this;}observe(){}unobserve(){}}};
const life=createPlotLifecycle(env).install();
const layout=()=>({xaxis:{range:[-8,17]},yaxis:{range:[12,-12],scaleanchor:'x'}});
(async()=>{
 await P.newPlot(ali.plot,[{type:'heatmap',z:[[1]]}],layout(),{});
 assert(ali.panel.hidden,'hidden panel restored after staged initialization');assert(!ali.panel.dataset.cometStaging);assert(nativeRenders[0].width===1132,'hidden staging uses actual content width');assert.deepStrictEqual(ali.plot.layout.yaxis.range,[12,-12]);
 ali.panel.hidden=false;ali.tab.attributes['aria-selected']='true';ali.plot.width=820;resizeObserver.callback([{target:ali.plot}]);await life.whenIdle();assert.equal(ali.plot.layout.width,820);assert.deepStrictEqual(ali.plot.layout.xaxis.range,[-8,17]);
 ali.panel.innerHTML='replacement';assert(events.indexOf('purge:alignment-plot')<events.indexOf('replace:panel-alignment'),'purge happens BEFORE chart DOM is detached');assert(!life.records.has(ali.plot));
 // A hidden empty drawing area is rejected, rather than silently creating a blank chart.
 const zero=new Element('div','zero');cov.panel.appendChild(zero);zero.height=0;await assert.rejects(P.newPlot(zero,[],layout(),{}),/no measurable drawing area/);life.errors.length=0;zero.remove();
 // Warm all tabs with real geometry and keep ready PNG previews of inactive GL views.
 const replacement=new Element('div','alignment-plot');ali.panel.appendChild(replacement);ali.plot=replacement;ali.panel.hidden=true;ali.tab.attributes['aria-selected']='false';
 await P.newPlot(dif.plot,[{type:'scattergl',x:[1],y:[2]}],layout(),{});const click=()=>{};dif.plot.on('plotly_click',click);
 const warmed=[];env.COMET_CORE_EXPLORER={markViewLoaded(name){warmed.push(name);},renderAlignment(){env.COMET_CORE_EXPLORER.alignmentReady=new Promise(resolve=>setImmediate(()=>setImmediate(resolve))).then(()=>P.react(ali.plot,[{type:'scattergl',x:[3],y:[4]}],layout(),{}));},renderCoverage(){return P.newPlot(cov.plot,[{type:'scattergl',x:[5],y:[6]}],layout(),{});}};
 const image=new Element('img','saved-figure');image.src='data:image/png;base64,example';main.appendChild(image);
 await life.boot();assert.deepStrictEqual(warmed,['alignment','coverage'],'eager views marked loaded before first tab opening');
 assert(nativeRenders.some(r=>r.id==='coverage-plot'),'coverage loaded before user opens the tab');assert(life.records.get(ali.plot).suspended&&life.records.get(cov.plot).suspended,'inactive GL views released after loaded previews');assert(dif.plot.data,'visible chart hydrated');assert.equal(dif.plot.handlers.plotly_click.length,1,'one existing click handler restored');assert.equal(dif.plot.handlers.plotly_click[0],click);assert.equal(status.dataset.state,'ready');assert(events.includes('decode:saved-figure'));assert(events.includes('fonts'));
 // Activate an already-loaded hidden view: hydrate and fit before removing its preview.
 dif.panel.hidden=true;dif.tab.attributes['aria-selected']='false';cov.panel.hidden=false;cov.tab.attributes['aria-selected']='true';const supportBefore=nativeRenders.filter(r=>r.id==='coverage-plot').length;await Promise.all([life.activate(),P.Plots.resize(cov.plot),P.Plots.resize(cov.plot)]);assert.equal(nativeRenders.filter(r=>r.id==='coverage-plot').length,supportBefore+1,'concurrent resize/activation hydrate exactly once');assert(cov.plot.data);assert(life.records.get(cov.plot).preview.hidden);assert(life.records.get(dif.plot).suspended);
 // Replacing a suspended graph also discards its retained records and PNG preview.
 dif.panel.innerHTML='new content';assert(!life.records.has(dif.plot));
 console.log(JSON.stringify({hidden_measured:true,resize_refit:true,purge_before_detach:true,eager_views:true,images_decoded:true,context_release_and_hydration:true,handlers_preserved:true}));
})().catch(error=>{console.error(error);process.exitCode=1;});
"""
        result = subprocess.run([node, "-e", fixture,
            str(ROOT / "scripts/comet_plot_lifecycle.js")], capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        checks = json.loads(result.stdout.strip())
        self.assertTrue(all(checks.values()), checks)
        self.assertEqual(set(checks), {"hidden_measured", "resize_refit", "purge_before_detach",
            "eager_views", "images_decoded", "context_release_and_hydration", "handlers_preserved"})

    def test_lifecycle_is_installed_before_core_initializes_and_has_accessible_status(self):
        from scripts.build_comet_core_explorer import ROOT
        template = (ROOT / "scripts/comet_core_explorer.html").read_text()
        self.assertLess(template.index("__PLOT_LIFECYCLE_JS__"),
                        template.index("'use strict';const DATA="))
        class StatusParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.status = None
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if attrs.get("id") == "plot-readiness":
                    self.status = attrs
        parser = StatusParser()
        parser.feed(template)
        self.assertIsNotNone(parser.status)
        self.assertEqual(parser.status.get("role"), "status")
        self.assertEqual(parser.status.get("aria-live"), "polite")
        self.assertEqual(parser.status.get("aria-busy"), "true")

    def test_shared_display_range_preserves_values_and_compares_both_condition_means(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node is needed for the colour-control behavior check")
        from scripts.build_comet_core_explorer import ROOT
        template = (ROOT / "scripts/comet_core_explorer.html").read_text()
        start = template.index("function colorDisplayScale(")
        stop = template.index("function renderDifferences()", start)
        script = template[start:stop] + r"""
const assert=require('assert');
const payload={color_scale:{cmin:-27,cmax:27},arms:{
 HK1:{homecage_mean:[[2,3]],running_mean:[[1,0]]},
 PFKP:{homecage_mean:[[196,null]],running_mean:[[9,12]]}}};
const before=JSON.stringify(payload),matrix=[[0,25,26,196,null]],raw=JSON.stringify(matrix);
const running=colorDisplayScale(payload,'running_mean','25');
const home=colorDisplayScale(payload,'homecage_mean','25');
assert.equal(running.fullLimit,196,'the unselected Homecage/PFKP maximum still sets the shared full range');
assert.equal(home.fullLimit,running.fullLimit);assert.equal(running.zmin,0);assert.equal(running.zmax,25);
assert.equal(running.optionLabel('25'),'0–25 counts');assert.equal(running.rangeLabel,'0–25 counts');
assert.equal(running.countClipped(matrix),2,'only above-range values saturate; zero and null are retained');
const full=colorDisplayScale(payload,'running_mean','full');assert.equal(full.zmax,196);assert.equal(full.countClipped(matrix),0);
const signed=colorDisplayScale(payload,'difference','25');assert.equal(signed.zmin,-25);assert.equal(signed.zmax,25);
assert.equal(signed.optionLabel('25'),'±25 counts');assert.equal(signed.countClipped([[-27,-25,0,25,26,null]]),2);
assert.equal(JSON.stringify(payload),before,'display selection must not mutate any scientific matrix');
assert.equal(JSON.stringify(matrix),raw,'saturation must not cap exact hover/table values');
console.log('shared display ranges verified');
"""
        result = subprocess.run([node, "-e", script], capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("shared display ranges verified", result.stdout)

    def test_changed_saved_reference_pixels_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self.fixture(directory, changed=True)
            with self.assertRaisesRegex(ValueError, "hash changed"):
                build(root)


if __name__ == "__main__":
    unittest.main()
