/* Embedded inside the existing core script after its immutable source globals.
 * Selected statistics never replace C, the saved baseline used by alignment and
 * observed-support diagnostics. Rendered values are never capped numerically. */
let measurementId='pla_count',comparisonId='absolute_difference',areaCutoff=.1,markerId='chat';
const measurementCache=new Map(),sectionMetricMaps=new WeakMap(),mainHoverMatrices=new Map();
const measurementFeaturesBySection=new Map((DATA.measurement_features?.sections||[]).map(s=>[s.section_id,s]));
const measurementNumberFormatter=new Intl.NumberFormat(undefined,{maximumSignificantDigits:6});
const observedContextCache=new Map(),detailCalculationCache=new Map();
let measurementExportBusy=false;
const PNG_EXPORT_WIDTH=8000;
function observedContextVisible(){return Q('show-object-context')?.checked!==false;}
function observedFootprintTraces(arm,layer='all',visible=true){
 if(!visible)return [];const geometry=DATA.context_geometry?.[arm];if(!geometry)return [];
 const traces=[];if(layer!=='outline'&&geometry.grid&&Array.isArray(geometry.footprint)){
  let cached=observedContextCache.get(arm);if(cached?.geometry!==geometry){cached={geometry,z:geometry.footprint.map(row=>row.map(v=>v?1:null))};observedContextCache.set(arm,cached);}
  traces.push({type:'heatmap',name:'Detected-object footprint context',x:geometry.grid.x_edges,y:geometry.grid.y_edges,z:cached.z,zmin:0,zmax:1,colorscale:[[0,'#f1f3f5'],[1,'#f1f3f5']],showscale:false,zsmooth:false,hoverinfo:'skip',hoverongaps:false,meta:{kind:'detected-object-context',not_tissue_boundary:true}});
 }
 if(layer!=='background'&&Array.isArray(geometry.x)&&Array.isArray(geometry.y))traces.push({type:'scatter',mode:'lines',name:'Detected-object footprint boundary',x:geometry.x,y:geometry.y,line:{color:'#75838e',width:1,simplify:false},showlegend:false,hoverinfo:'skip',connectgaps:false,cliponaxis:true,meta:{kind:'detected-object-outline',not_tissue_boundary:true}});
 return traces;
}
function detailAnalysis(){
 if(!window.COMET_DETAIL_GRID?.calculate||!measurementFeaturesAvailable())return {grid:C.grid,calculation:measurementResult(),binWidth:Number(resolution),note:'Using the selected global bin grid.'};
 const requested=Number(Q('focus-bin-width').value),choices=[10,25,50,100],fits=width=>Math.ceil(focusWindow.xmax/width)-Math.floor(focusWindow.xmin/width)<=400&&Math.ceil(focusWindow.ymax/width)-Math.floor(focusWindow.ymin/width)<=400;
 let width=requested,note='';if(!fits(width)){width=choices.find(fits);if(!width)throw Error('The detail window is too large for a 400 × 400 grid. Select a smaller window.');Q('focus-bin-width').value=String(width);note='Detail bins adjusted to '+width+' export units to keep the grid at or below 400 × 400.';}
 const key=[measurementId,comparisonId,areaCutoff,markerId,width,focusWindow.xmin,focusWindow.xmax,focusWindow.ymin,focusWindow.ymax].join('|');if(detailCalculationCache.has(key))return {...detailCalculationCache.get(key),note};
 const result=window.COMET_DETAIL_GRID.calculate({base:MR.resolutions['100'],points:MR.pla_points,features:DATA.measurement_features,window:{...focusWindow},binWidth:width,id:measurementId,areaCutoff,marker:markerId,comparison:comparisonId});
 const record={...result,binWidth:width,note};detailCalculationCache.set(key,record);while(detailCalculationCache.size>2)detailCalculationCache.delete(detailCalculationCache.keys().next().value);return record;
}
function selectedExportOptions(arm){
 const key=Q('mean-view').value,comparison=key==='difference',scope=Q('measurement-export-region').value;
 let calculation=measurementResult(),grid=C.grid,z=shownMetricMatrix(arm,key),binWidth=Number(resolution),viewport;
 if(scope==='detail'){
  if(!focusWindow)selectDefaultFocus();const detail=detailAnalysis();calculation=detail.calculation;grid=detail.grid;z=metricDomainMatrix(calculation.arms[arm],calculation.arms[arm][key],comparison);binWidth=detail.binWidth;viewport={...focusWindow};
 }else if(scope==='zoom'&&sharedViewport)viewport={xmin:Math.min(...sharedViewport.x),xmax:Math.max(...sharedViewport.x),ymin:Math.min(...sharedViewport.y),ymax:Math.max(...sharedViewport.y)};
 const units=metricUnits(comparison),scale=colorDisplayScale(calculation,key,Q('signed-range').value,units),meta=measurementMeta();
 return {arm,grid,z,measurementLabel:meta.label+(meta.needsCutoff?' ('+(measurementId==='small_pla_count'?'small < ':'large ≥ ')+String(areaCutoff)+' exported µm²)':''),comparisonLabel:comparison?comparisonLabel():key==='running_mean'?'Running mean':'Homecage mean',units,colorScale:comparison?[[0,'#2166ac'],[.5,'#ffffff'],[1,'#b2182b']]:[[0,'#ffffff'],[.3,'#c1daed'],[.7,'#5896c4'],[1,'#174e79']],zmin:scale.zmin,zmax:scale.zmax,contextGeometry:DATA.context_geometry?.[arm],contextVisible:observedContextVisible(),viewport,binWidth,metadata:{measurement_id:measurementId,comparison_function:comparisonId,display:key,region:scope,marker:markerId,area_cutoff_exported_um2:areaCutoff,area_cutoff_applies:!!meta.needsCutoff,marker_applies:!!meta.needsMarker,bin_width_export_units:binWidth,averaging_policy:intensiveMeasurement()?'Equal mean of defined section values':'Equal mean of three section values; empty bins zero where defined',tissue_coverage_verified:false,context:'Metric-independent observed-object footprint, not a tissue boundary. No missing metric values are imputed.',source_features_sha256:DATA.measurement_feature_payload_sha256||null,source_count_payload_sha256:DATA.measurement_features?.source_count_payload_sha256||null}};
}
async function exportMeasurementImage(arm,format){
 if(measurementExportBusy)return;const status=Q('measurement-export-status'),buttons=['export-hk1-png','export-pfkp-png','export-hk1-svg','export-pfkp-svg'];
 measurementExportBusy=true;for(const id of buttons)Q(id).disabled=true;status.dataset.state='loading';status.textContent='Preparing '+arm+' '+format.toUpperCase()+'…';
 try{
  if(!window.COMET_VECTOR_EXPORT?.download)throw Error('The high-resolution export module is unavailable.');
  await new Promise(resolve=>setTimeout(resolve,0));const width=PNG_EXPORT_WIDTH;
  const options=selectedExportOptions(arm),filename='COMET_'+arm+'_'+measurementId+'_'+(Q('mean-view').value==='difference'?comparisonId:Q('mean-view').value)+'_'+options.binWidth+'_units_'+Q('measurement-export-region').value+'_cutoff_'+areaCutoff+'_marker_'+markerId+(format==='png'?'_'+width+'px':'_vector');
  const result=await window.COMET_VECTOR_EXPORT.download({...options,format,width,filename,onProgress:message=>{status.textContent=arm+': '+String(message);}});
  status.dataset.state='ready';status.textContent=arm+' '+format.toUpperCase()+' downloaded'+(result?.vector?' · resolution-independent vector tiles':result?.width?' · '+num(result.width)+' × '+num(result.height)+' pixels':'')+'. Same measured bins and coordinates; undefined values stay undefined.';
 }catch(error){status.dataset.state='error';status.textContent='Export failed: '+String(error?.message||error)+'. Try the scalable SVG export.';}
 finally{measurementExportBusy=false;for(const id of buttons)Q(id).disabled=!window.COMET_VECTOR_EXPORT?.download;}
}
function measurementMeta(){const meta=window.COMET_MEASUREMENTS?.MEASUREMENTS.find(m=>m.id===measurementId)||{id:'pla_count',label:'PLA count',units:'counts',empty_bin_rule:'assumed_zero',needsCutoff:false,needsMarker:false};if(!meta.needsMarker)return meta;const marker=(DATA.measurement_features?.available_markers||[]).find(m=>m.id===markerId)?.label||'ChAT';return {...meta,label:meta.label.replace('Marker-associated',marker+'-associated')};}
function measurementKey(){return [mode,resolution,measurementId,comparisonId,areaCutoff,markerId].join('|');}
function formatMeasurement(value){return value===null||value===undefined||!Number.isFinite(value)?'undefined':value===0?'0':measurementNumberFormatter.format(value);}
function comparisonLabel(){return comparisonId==='percent_change'?'100 × (Running − Homecage) / Homecage':comparisonId==='log2_fold_change'?'log₂(Running / Homecage)':'Running − Homecage';}
function metricUnits(comparison=false){if(comparison&&comparisonId==='percent_change')return '%';if(comparison&&comparisonId==='log2_fold_change')return 'log₂ fold change';const meta=measurementMeta();return comparison?(meta.difference_units||meta.units):meta.units;}
function intensiveMeasurement(){return measurementMeta().empty_bin_rule==='undefined';}
function measurementFeaturesAvailable(){const f=DATA.measurement_features;return !!(window.COMET_MEASUREMENTS?.calculate&&f?.schema_version==='comet-measurement-features-v1'&&Array.isArray(f.sections)&&f.sections.length>0&&f.validation?.all_selected_pla_objects_retained===true);}
function measurementResult(){
 if(!exploratory())return C;
 if(!measurementFeaturesAvailable()){if(measurementId!=='pla_count'||comparisonId!=='absolute_difference')throw Error('Validated object features are unavailable for this measurement');return C;}
 const key=measurementKey();if(measurementCache.has(key))return measurementCache.get(key);
 const result=window.COMET_MEASUREMENTS.calculate({...C,pla_points:MR.pla_points},DATA.measurement_features,measurementId,{areaCutoff,marker:markerId,comparison:comparisonId});
 measurementCache.set(key,result);while(measurementCache.size>2)measurementCache.delete(measurementCache.keys().next().value);return result;
}
function metricSectionMap(){const result=measurementResult();if(!sectionMetricMaps.has(result))sectionMetricMaps.set(result,new Map((result.sections||[]).map(s=>[s.section_id,s])));return sectionMetricMaps.get(result);}
function metricSectionValues(section){return metricSectionMap().get(section.section_id)?.values||section.pla_counts;}
function validMetricN(d,condition){return d[condition==='Running'?'running_valid_section_n':'homecage_valid_section_n']||d.homecage_mean.map(row=>row.map(v=>v===null?0:3));}
function metricDomainMatrix(d,matrix,comparison=false,domain=d.eligibility||d.displayable){return matrix.map((row,iy)=>row.map((value,ix)=>domain?.[iy]?.[ix]&&value!==null&&Number.isFinite(value)&&(!comparison||d.displayable?.[iy]?.[ix]!==false)?value:null));}
function shownMetricMatrix(arm,key){const d=measurementResult().arms[arm];return metricDomainMatrix(d,d[key],key==='difference',C.arms[arm].displayable);}
function contribution(arm,condition,iy,ix){return (C.sections||[]).filter(s=>String(s.pla_type).toUpperCase().includes(arm)&&String(s.condition).replace(/\s/g,'').toLowerCase()===condition.toLowerCase()&&(exploratory()||s.tissue_validity?.[iy]?.[ix])).map(s=>{
 if(!exploratory())return s.section_id+': PLA '+String(s.counts?.[iy]?.[ix]??'not supplied');
 return s.section_id+': '+measurementMeta().label+' '+formatMeasurement(metricSectionValues(s)?.[iy]?.[ix])+'; raw PLA '+String(s.pla_counts[iy][ix])+'; ChAT '+String(s.chat_counts[iy][ix])+'; observed support '+(s.observed_support[iy][ix]?'yes':'no, coverage uncertain');
 }).join(' | ')||'None';}
function hoverMatrix(a,d,hn,rn){
 const key=measurementKey()+'|'+a;if(mainHoverMatrices.has(key))return mainHoverMatrices.get(key);
 const hv=validMetricN(d,'Homecage'),rv=validMetricN(d,'Running'),metricMap=metricSectionMap(),domain=C.arms[a].displayable;
 // Resolve section/metric lookups once, rather than filtering the cohort and
 // rebuilding the request key six times for every one of 60,000 grid bins.
 const prepared=condition=>(C.sections||[]).filter(s=>s.pla_type===a&&s.condition===condition).map(s=>({id:s.section_id,values:metricMap.get(s.section_id)?.values||s.pla_counts,pla:s.pla_counts,chat:s.chat_counts,observed:s.observed_support}));
 const running=prepared('Running'),home=prepared('Homecage');
 const valuesAt=(entries,iy,ix)=>{let text='';for(const s of entries){if(text)text+=' | ';text+=s.id+': '+formatMeasurement(s.values[iy][ix])+' (raw PLA '+s.pla[iy][ix]+', ChAT '+s.chat[iy][ix]+'; observed '+(s.observed[iy][ix]?'yes':'no')+')';}return text||'None';};
 const outside='Outside the observed display domain; no exported objects in this bin. Coverage uncertain.';
 const matrix=d.difference.map((r,iy)=>r.map((v,ix)=>[d.homecage_mean[iy][ix],d.running_mean[iy][ix],hn[iy][ix],rn[iy][ix],iy,ix,domain[iy][ix]?valuesAt(running,iy,ix):outside,domain[iy][ix]?valuesAt(home,iy,ix):outside,hv[iy][ix],rv[iy][ix],d.missing_reason?.[iy]?.[ix]?.replace?.(/_/g,' ')||(!domain[iy][ix]?'outside observed display domain':'defined'),d.absolute_difference?.[iy]?.[ix]??v]));mainHoverMatrices.set(key,matrix);return matrix;
}
function applyMeasurementText(){
 const available=measurementFeaturesAvailable(),obs=exploratory();Q('measurement-function').disabled=!obs;Q('comparison-function').disabled=!obs||!available;
 for(const option of Q('measurement-function').options)option.disabled=!available&&option.value!=='pla_count';if(!obs)return;
 const meta=measurementMeta(),intensive=intensiveMeasurement(),context=meta.needsCutoff?' · '+(measurementId==='small_pla_count'?'small < ':'large ≥ ')+String(areaCutoff)+' exported µm²':'';
 Q('area-cutoff-control').hidden=!meta.needsCutoff;Q('marker-control').hidden=!meta.needsMarker;
 Q('custom-color-units').textContent=metricUnits(Q('mean-view').value==='difference');
 for(const link of Q('exploratory-downloads').querySelectorAll('a[download]'))link.hidden=measurementId!=='pla_count'||comparisonId!=='absolute_difference';
 Q('mean-view').options[0].textContent=comparisonLabel();Q('mean-view').options[1].textContent='Running mean · '+meta.label;Q('mean-view').options[2].textContent='Homecage mean · '+meta.label;
 Q('page-description').textContent='Select a section-level spatial measurement, average its defined values within each condition, then compare Running with Homecage. The saved alignment, grids and observed-support maps stay unchanged; tissue coverage remains uncertain.';
 Q('page-heading').textContent='Spatial measurements. Condition comparisons. 2D review.';
 Q('difference-intro').textContent=meta.label+context+'. Compute this measurement per section and bin, average section values within each condition, then apply '+comparisonLabel()+'. Arms remain separate. No spatial smoothing, tissue-area/acquisition normalization or statistical test.';
 Q('method-banner').textContent='Selected measurement: '+meta.label+context+'. '+(intensive?'A section-bin without the objects needed for this statistic is undefined, not zero. Each condition averages only its defined section values; measurement N is shown.':'Each condition averages three section values, including the formula-defined empty-bin zeros.')+' '+(comparisonId==='percent_change'?'Percent change is undefined when Homecage mean is zero.':comparisonId==='log2_fold_change'?'Log₂ fold change requires positive means in both conditions.':'Absolute comparison is Running mean − Homecage mean.')+' No pseudocounts are added. Current exploratory eligibility is preserved; coverage is uncertain.';
 Q('mode-status').textContent=intensive?'Defined-section average · coverage uncertain':'All 3 sections / condition · coverage uncertain';
 Q('current-policy-summary').textContent=intensive?'Current comparison is ready. Empty object statistics remain undefined; tissue coverage is uncertain.':'Current comparison is ready. Formula-defined empty section-bin values are zero; tissue coverage is uncertain.';
 Q('measurement-summary').textContent=meta.label+' ['+metricUnits()+']'+context+' · '+comparisonLabel()+' · '+(intensive?'empty object statistics/fractions remain undefined':'empty section-bins count as zero')+'.';
 Q('mean-view-note').textContent='Condition means average section-level '+meta.label.toLowerCase()+'. '+(intensive?'Defined measurement N may range from 0 to 3.':'Mean denominator = 3 per condition.')+' Observed-object N is a separate diagnostic.';
 Q('difference-guide').innerHTML=guideCard('How to read this selected comparison','<p><strong>Measurement.</strong> '+esc(meta.label+context)+'. Units: '+esc(metricUnits())+'.</p><p><strong>Calculation.</strong> Compute one value per section and bin, average those section values by condition, then apply '+esc(comparisonLabel())+'. '+(intensive?'Undefined section values are omitted; defined-measurement N is explicit.':'All three section values enter, including assumed zeros.')+'</p><p><strong>Colors.</strong> Positive values are higher in Running; negative values are lower. White is a defined zero comparison. Gray includes unavailable measurements or undefined comparisons as well as locations outside the saved observed domain.</p>')+guideCard('Limits and next inspection','<p><strong>Missing values.</strong> '+(intensive?'No qualifying objects means an undefined mean, percentile or fraction.':'Empty section-bins contribute zero by the agreed exploratory rule.')+' Percent change requires nonzero Homecage mean; log₂ fold change requires positive means in both conditions. No pseudocount is added.</p><p><strong>Inspect.</strong> Read both means, measurement-specific N, raw observed-support diagnostics and individual section values. Area uses exported µm² labels; intensity is an exported measurement, not calibrated fluorescence. Object maps do not establish full tissue coverage.</p><div id="difference-readout" class="readout" hidden></div><button id="inspect-aligned-bin" hidden style="margin-top:10px">Inspect selected bin in alignment</button>');
 Q('inspect-aligned-bin').onclick=()=>{if(!reviewBin)return;Q('align-arm').value=reviewBin.arm;Q('align-frame').value='saved';Q('align-view').value='flat';camera='top';cameraRevision++;layerControls(true);showTab('alignment');renderAlignment();};
 Q('coverage-intro').textContent='Four unchanged observed-support maps count sections containing exported PLA or ChAT detections. This baseline diagnostic stays independent of the selected measurement; defined measurement N appears in comparison hover and section detail.';
 Q('focus-global-caption').textContent='Every cached PLA point inside the selected window is shown as source-location context, including points outside a selected size or marker numerator. The background shows the selected section-level measurement or its condition mean. '+(intensive?'Undefined section measurements are omitted; defined N is shown.':'All three section values enter, including assumed zeros.')+' Observed support remains a separate baseline diagnostic; tissue coverage is uncertain.';
}
function resetMeasurementRange(){
 const units=metricUnits(Q('mean-view').value==='difference'),count=units.includes('count'),fraction=units.includes('fraction');
 const options=count?[100,50,25,10]:units==='%'?[500,200,100,50,25,10]:units==='log₂ fold change'?[8,4,2,1,.5]:fraction?[1,.5,.25,.1,.05]:[10,1,.5,.25,.1,.05,.025,.01];
 Q('signed-range').innerHTML='<option value="full">Full observed range</option>'+options.map(v=>'<option value="'+v+'">'+v+'</option>').join('');Q('signed-range').value=measurementId==='pla_count'&&comparisonId==='absolute_difference'?'25':'full';
 Q('custom-color-limit').value='';
}
function refreshMeasurementSelection(){
 Q('measurement-error').hidden=true;measurementCache.clear();mainHoverMatrices.clear();focusMaxima.clear();
 try{measurementResult();applyMeasurementText();renderDifferences();renderFocus();notifyView();}
 catch(error){Q('measurement-error').hidden=false;Q('measurement-error').textContent='This measurement could not be calculated: '+String(error?.message||error)+'. Saved alignment and support diagnostics are unchanged.';}
}
function initializeMeasurements(){
 const catalog=window.COMET_MEASUREMENTS?.MEASUREMENTS;if(catalog?.length){const old=Q('measurement-function').value;Q('measurement-function').innerHTML=catalog.map(m=>'<option value="'+esc(m.id)+'">'+esc(m.label)+'</option>').join('');Q('measurement-function').value=catalog.some(m=>m.id===old)?old:'pla_count';}
 Q('measurement-function').onchange=()=>{measurementId=Q('measurement-function').value;resetMeasurementRange();refreshMeasurementSelection();};
 Q('comparison-function').onchange=()=>{comparisonId=Q('comparison-function').value;resetMeasurementRange();refreshMeasurementSelection();};
 const applyCutoff=()=>{const raw=Q('area-cutoff').value,value=Number(raw);if(raw.trim()===''||!Number.isFinite(value)||value<0){Q('measurement-error').hidden=false;Q('measurement-error').textContent='Enter a finite, nonnegative area cutoff in exported µm².';return;}areaCutoff=value;resetMeasurementRange();refreshMeasurementSelection();};
 Q('apply-area-cutoff').onclick=applyCutoff;Q('area-cutoff').onchange=applyCutoff;Q('measurement-marker').onchange=()=>{markerId=Q('measurement-marker').value;refreshMeasurementSelection();};
 const applyColorLimit=()=>{const raw=Q('custom-color-limit').value,value=Number(raw);if(raw.trim()===''||!Number.isFinite(value)||value<=0){Q('measurement-error').hidden=false;Q('measurement-error').textContent='Enter a finite color-display limit greater than zero. Scientific values are never capped.';return;}Q('measurement-error').hidden=true;const choice=String(value),select=Q('signed-range');if(!Array.from(select.options).some(option=>option.value===choice)){const option=document.createElement('option');option.value=choice;option.textContent=choice;select.appendChild(option);}select.value=choice;renderDifferences();};
 Q('apply-color-limit').onclick=applyColorLimit;Q('custom-color-limit').onchange=applyColorLimit;
 Q('show-object-context').onchange=()=>{renderDifferences();renderFocus();if(!Q('panel-coverage').hidden)renderCoverage();notifyView();};
 Q('open-fine-detail').onclick=()=>{const workspace=Q('focus-workspace');if(workspace.hidden)renderFocus();workspace.scrollIntoView({behavior:'smooth',block:'start'});Q('focus-bin-width').focus({preventScroll:true});};
 for(const arm of ['HK1','PFKP'])for(const format of ['png','svg']){const button=Q('export-'+arm.toLowerCase()+'-'+format);button.disabled=!window.COMET_VECTOR_EXPORT?.download;button.onclick=()=>exportMeasurementImage(arm,format);}
}
function renderMeasurementDifferences(){
 const generation=++mapGeneration,ready=available('differences'),key=Q('mean-view').value,difference=key==='difference',which=key==='running_mean'?'Running':'Homecage',analysis=measurementResult(),meta=measurementMeta(),units=metricUnits(difference),scale=colorDisplayScale(analysis,key,Q('signed-range').value,units);
 Q('minimum-observed').disabled=true;Q('signed-range').disabled=false;for(const option of Q('signed-range').options)option.textContent=scale.optionLabel(option.value);applyMeasurementText();
 Q('difference-panels').innerHTML=arms.map(a=>'<article class="card"><div class="card-head"><div><h3>TDP43–'+a+'</h3><p>'+esc(meta.label)+' · '+esc(difference?comparisonLabel():which+' section mean')+'</p></div><span class="tag">'+(intensiveMeasurement()?'Defined-section mean':'Mean of all 3 sections')+'</span></div>'+(ready?'<div id="difference-'+a+'" class="plot"></div><div class="legend">'+(difference?'<span>Defined zero comparison</span>':'')+'<span class="missing">Undefined or outside observed domain</span><span class="context">Detected-object footprint · not tissue</span></div><div id="clip-status-'+a+'" class="caption"></div><div class="caption">'+(difference?'Identical symmetric linear colour limits across both PLA types.':'Identical sequential linear colour limits across both conditions and both PLA types.')+' Exact values are retained. The fixed observed-object footprint remains visible beneath undefined statistics; it does not establish tissue coverage.</div>':empty('Selected measurement is unavailable.','See the documented current inputs and calculation policy.'))+'</article>').join('');
 requirements('difference-blockers','differences');updateResolutionNotice();if(!ready)return;
 const gr=C.grid,supportSummary=[];
 for(const a of arms){const d=analysis.arms[a],base=C.arms[a],hn=nMatrix(base,'Homecage'),rn=nMatrix(base,'Running'),shownZ=shownMetricMatrix(a,key),shown=shownZ.reduce((n,r)=>n+r.filter(v=>v!==null).length,0),clipped=scale.countClipped(shownZ),custom=hoverMatrix(a,d,hn,rn);
 Q('clip-status-'+a).textContent=(meta.needsCutoff?'Large-PLA cutoff = '+String(areaCutoff)+' exported µm². ':'')+(Q('signed-range').value==='full'?'Full shared linear range '+scale.rangeLabel+'. No values saturated.':clipped+' shown bins beyond display range '+scale.rangeLabel+' use endpoint color. Exact values remain in hover and CSV; no numerical value is changed.');
 supportSummary.push(a+': '+num(shown)+' defined '+(difference?'comparisons':'means'));
 const plotLayout=mapLayout();if(sharedViewport){plotLayout.xaxis.range=sharedViewport.x.slice();plotLayout.yaxis.range=sharedViewport.y.slice();}if(focusWindow&&Q('focus-arm').value===a)plotLayout.shapes=[focusRectangle()];plotLayout.margin.t=87;
 plotLayout.title={text:a+' · '+esc(meta.label)+'<br><sup>'+esc(difference?comparisonLabel():which+' mean')+' · '+resolution+'-unit bins · display '+esc(scale.rangeLabel)+'</sup><br><sup>'+(meta.needsCutoff?(measurementId==='small_pla_count'?'small < ':'large ≥ ')+esc(String(areaCutoff))+' exported µm² · ':'')+(intensiveMeasurement()?'defined N varies':'N = 3; empty = 0')+' · coverage uncertain'+(clipped?' · '+num(clipped)+' saturated':'')+'</sup>',x:.025,font:{size:12}};
 // The full measurement and formula remain in the panel heading and hover.
 // Keep the vertical colorbar concise so long marker/statistic names fit.
 const labelText=(difference?(comparisonId==='percent_change'?'Percent change':comparisonId==='log2_fold_change'?'log₂(R/H)':'R − H'):which+' mean')+'<br>['+units+']';
 Plotly.newPlot('difference-'+a,[...observedFootprintTraces(a,'background',observedContextVisible()),{type:'heatmap',x:gr.x_edges,y:gr.y_edges,z:shownZ,customdata:custom,zmin:scale.zmin,zmax:scale.zmax,zmid:difference?0:undefined,colorscale:difference?[[0,'#2166ac'],[.5,'#ffffff'],[1,'#b2182b']]:[[0,'#ffffff'],[.3,'#c1daed'],[.7,'#5896c4'],[1,'#174e79']],zsmooth:false,hoverongaps:true,colorbar:{title:{text:labelText,side:'right',font:{size:10}},thickness:13,len:.82},hovertemplate:'<b>'+esc(meta.label)+'</b><br>Running mean=%{customdata[1]:.6g}<br>Homecage mean=%{customdata[0]:.6g}<br>Defined measurement sections: Running %{customdata[9]}, Homecage %{customdata[8]}<br><b>'+esc(difference?comparisonLabel():which+' mean')+'=%{z:.6g} ['+esc(units)+']</b><br>Status: %{customdata[10]}<br>Observed-object sections (diagnostic): Running %{customdata[3]}, Homecage %{customdata[2]}<br>Running section values — %{customdata[6]}<br>Homecage section values — %{customdata[7]}<extra>TDP43–'+a+'</extra>'},...observedFootprintTraces(a,'outline',observedContextVisible())],plotLayout,{...cfg,toImageButtonOptions:{format:'png',scale:4,filename:'COMET_'+a+'_'+measurementId+'_'+(difference?comparisonId:key)+'_'+resolution+'_cutoff_'+areaCutoff+'_marker_'+markerId}}).then(()=>{if(generation!==mapGeneration)return;bindMainZoom(a);Q('difference-'+a).on('plotly_click',ev=>{
 const p=ev.points[0],v=p.customdata;if(!v)return;reviewBin={arm:a,xmin:gr.x_edges[v[5]],xmax:gr.x_edges[v[5]+1],ymin:gr.y_edges[v[4]],ymax:gr.y_edges[v[4]+1]};Q('difference-readout').hidden=false;Q('difference-readout').textContent=meta.label+' · '+comparisonLabel()+' · TDP43–'+a+'\nX ['+num(reviewBin.xmin)+', '+num(reviewBin.xmax)+') · Y ['+num(reviewBin.ymin)+', '+num(reviewBin.ymax)+')\nRunning mean '+formatMeasurement(v[1])+' (defined N='+v[9]+'); Homecage mean '+formatMeasurement(v[0])+' (defined N='+v[8]+')\nStatus: '+v[10]+'\nRunning: '+v[6]+'\nHomecage: '+v[7];Q('inspect-aligned-bin').hidden=false;if(exploratory()&&pointRecords().length){Q('focus-arm').value=a;setFocusAt((reviewBin.xmin+reviewBin.xmax)/2,(reviewBin.ymin+reviewBin.ymax)/2);renderFocus();}
 });});
 }
 Q('filter-note').hidden=!exploratory();Q('filter-note').textContent=supportSummary.join(' · ')+'. '+(intensiveMeasurement()?'Condition means average defined section-level values; N may differ across locations.':'Condition means include all three section-level values, including formula-defined empty-bin zeros.')+' Undefined comparisons are masked. Observed support remains diagnostic; coverage uncertain.';
}
function downloadMeasurementTable(arm){
 const d=measurementResult().arms[arm],base=C.arms[arm],ss=(C.sections||[]).filter(s=>s.pla_type===arm),hn=nMatrix(base,'Homecage'),rn=nMatrix(base,'Running'),hv=validMetricN(d,'Homecage'),rv=validMetricN(d,'Running');
 const rows=[['measurement_id','measurement_label','measurement_units','comparison_function','comparison_units','area_cutoff_exported_um2','marker','arm','bin_width_export_units','xmin','xmax','ymin','ymax','homecage_mean','running_mean','absolute_difference','selected_comparison','homecage_defined_measurement_sections','running_defined_measurement_sections','homecage_observed_support_N','running_observed_support_N','inside_observed_display_domain','comparison_defined','missing_reason','averaging_policy','tissue_coverage_verified',...ss.map(s=>s.section_id+'__measurement_value')]];
 for(let iy=0;iy<d.difference.length;iy++)for(let ix=0;ix<d.difference[iy].length;ix++)rows.push([measurementId,measurementMeta().label,metricUnits(),comparisonId,metricUnits(true),areaCutoff,markerId,arm,resolution,C.grid.x_edges[ix],C.grid.x_edges[ix+1],C.grid.y_edges[iy],C.grid.y_edges[iy+1],d.homecage_mean[iy][ix],d.running_mean[iy][ix],d.absolute_difference?.[iy]?.[ix]??(comparisonId==='absolute_difference'?d.difference[iy][ix]:null),d.difference[iy][ix],hv[iy][ix],rv[iy][ix],hn[iy][ix],rn[iy][ix],base.displayable[iy][ix],d.displayable[iy][ix],d.missing_reason?.[iy]?.[ix]||'',intensiveMeasurement()?'equal mean of defined section statistics':'sum of all three section values / 3; empty bins assumed zero',false,...ss.map(s=>metricSectionValues(s)?.[iy]?.[ix])]);
 const q=v=>'"'+String(v??'').replace(/"/g,'""')+'"',blob=new Blob([rows.map(r=>r.map(q).join(',')).join('\n')+'\n'],{type:'text/csv;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='COMET_'+arm+'_'+measurementId+'_'+comparisonId+'_'+resolution+'_cutoff_'+areaCutoff+'_marker_'+markerId+'.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),500);
}
