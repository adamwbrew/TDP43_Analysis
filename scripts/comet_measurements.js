/* Pure section/bin measurements. No registration, tissue inference or pseudocounts. */
(function(scope){
'use strict';
const ZERO_METRICS=new Set(['pla_count','large_pla_count','small_pla_count','total_pla_area','marker_associated_pla_count','marker_associated_large_pla_count','section_pla_share']);
const MEASUREMENTS=[
 {id:'pla_count',label:'PLA count',units:'PLA count / bin'},
 {id:'large_pla_count',label:'Large PLA count',units:'PLA count / bin',needsCutoff:true},
 {id:'small_pla_count',label:'Small PLA count',units:'PLA count / bin',needsCutoff:true},
 {id:'large_pla_fraction',label:'Large PLA fraction',units:'fraction',needsCutoff:true},
 {id:'mean_pla_area',label:'Mean PLA area',units:'µm² (exported)'},
 {id:'median_pla_area',label:'Median PLA area',units:'µm² (exported)'},
 {id:'p90_pla_area',label:'90th-percentile PLA area',units:'µm² (exported)'},
 {id:'total_pla_area',label:'Total PLA area',units:'µm² (exported)'},
 {id:'mean_pla_intensity',label:'Mean PLA intensity',units:'exported intensity units'},
 {id:'marker_associated_pla_count',label:'Marker-associated PLA count',units:'PLA count / bin',needsMarker:true},
 {id:'marker_associated_pla_fraction',label:'Marker-associated PLA fraction',units:'fraction',needsMarker:true},
 {id:'marker_associated_large_pla_count',label:'Marker-associated large PLA count',units:'PLA count / bin',needsMarker:true,needsCutoff:true},
 {id:'marker_associated_pla_mean_area',label:'Marker-associated PLA mean area',units:'µm² (exported)',needsMarker:true},
 {id:'section_pla_share',label:'Section PLA share',units:'% of section PLA',difference_units:'percentage points'},
 {id:'marker_associated_pla_area_fraction',label:'Marker-associated PLA area fraction',units:'fraction',needsMarker:true},
 {id:'median_pla_intensity',label:'Median PLA intensity',units:'exported intensity units'},
 {id:'pla_area_iqr',label:'PLA area interquartile range',units:'µm² (exported)'},
 {id:'pla_area_cv',label:'PLA area coefficient of variation',units:'dimensionless CV'},
 {id:'mean_pla_nearest_neighbor_distance',label:'Mean PLA nearest-neighbor distance',units:'exported coordinate units'}
].map(m=>({...m,needsMarker:!!m.needsMarker,needsCutoff:!!m.needsCutoff,empty_bin_rule:ZERO_METRICS.has(m.id)?'assumed_zero':'undefined'}));
const COMPARISONS=[
 {id:'absolute_difference',label:'Running − Homecage',units:'measurement units'},
 {id:'percent_change',label:'Percent change relative to Homecage',units:'%'},
 {id:'log2_fold_change',label:'Log2 fold change (Running / Homecage)',units:'log2 ratio'}
];
const finite=v=>typeof v==='number'&&Number.isFinite(v), preparedCache=[];
function binIndex(edges,value){
 if(!finite(value)||value<edges[0]||value>edges[edges.length-1])return -1;
 if(value===edges[edges.length-1])return edges.length-2;
 let lo=0,hi=edges.length-1;while(lo+1<hi){const mid=(lo+hi)>>1;if(value<edges[mid])hi=mid;else lo=mid;}return lo;
}
function rows(values,nx,boolean=false){const out=[];for(let i=0;i<values.length;i+=nx){const row=[];for(let j=i;j<i+nx;j++)row.push(boolean?!!values[j]:finite(values[j])?values[j]:null);out.push(row);}return out;}
function objectRows(values,nx){const out=[];for(let i=0;i<values.length;i+=nx)out.push(values.slice(i,i+nx));return out;}
function quantile(sorted,q){if(!sorted.length)return NaN;const position=(sorted.length-1)*q,lower=Math.floor(position),upper=Math.ceil(position);return sorted[lower]+(position-lower)*(sorted[upper]-sorted[lower]);}
function compareConditions(running,homecage,comparison='absolute_difference'){
 if(!COMPARISONS.some(c=>c.id===comparison))throw Error('Unknown condition comparison');
 const array=Array.isArray(running)||ArrayBuffer.isView(running);
 if(array){if(!(Array.isArray(homecage)||ArrayBuffer.isView(homecage))||running.length!==homecage.length)throw Error('Condition means must have the same shape');const children=Array.from(running,(value,i)=>compareConditions(value,homecage[i],comparison));return {values:children.map(c=>c.values),defined:children.map(c=>c.defined),missing_reason:children.map(c=>c.missing_reason)};}
 let reason=null,value=NaN;
 if(!finite(homecage)&&!finite(running))reason='undefined_both_condition_means';
 else if(!finite(homecage))reason='undefined_homecage_mean';else if(!finite(running))reason='undefined_running_mean';
 else if(comparison==='percent_change'&&homecage===0)reason='zero_homecage_mean';
 else if(comparison==='log2_fold_change'&&homecage<=0)reason='nonpositive_homecage_mean';
 else if(comparison==='log2_fold_change'&&running<=0)reason='nonpositive_running_mean';
 else value=comparison==='absolute_difference'?running-homecage:comparison==='percent_change'?100*(running-homecage)/homecage:Math.log2(running/homecage);
 if(!reason&&!finite(value))reason='nonfinite_comparison';return {values:finite(value)?value:null,defined:finite(value),missing_reason:reason};
}
function select(payload){if(payload.grid)return {payload,points:payload.pla_points||[]};return {payload:payload.resolutions[String(payload.default_resolution||'100')],points:payload.pla_points||[]};}
function validateGrid(grid){for(const edges of [grid.x_edges,grid.y_edges])if(!Array.isArray(edges)||edges.length<2||edges.some((v,i)=>!finite(v)||(i&&v<=edges[i-1])))throw Error('Finite strictly increasing recorded bin edges are required');}
function prepare(payload,features,points){
 const old=preparedCache.find(p=>p.grid===payload.grid&&p.sections===payload.sections&&p.features===features&&p.points===points);if(old)return old.records;
 validateGrid(payload.grid);const nx=payload.grid.x_edges.length-1,ny=payload.grid.y_edges.length-1,size=nx*ny;
 const pointMap=new Map(points.map(p=>[p.section_id,p])),featureMap=new Map((features.sections||[]).map(f=>[f.section_id,f]));
 if(pointMap.size!==points.length||featureMap.size!==(features.sections||[]).length)throw Error('Repeated point or feature section identities');
 const records=new Map();
 for(const section of payload.sections){
  const p=pointMap.get(section.section_id),f=featureMap.get(section.section_id);if(!p||!f)throw Error('Complete indexed PLA points and measurement features are required');
  if(p.source_sha256&&p.source_sha256!==f.source_sha256)throw Error('Measurement feature source hash differs from the point cache');
  const length=p.x.length;if(p.y.length!==length||!Array.isArray(f.area_um2)||!Array.isArray(f.intensity)||f.area_um2.length!==length||f.intensity.length!==length)throw Error('Feature arrays must index every point exactly once');
  const bins=new Int32Array(length),n=new Float64Array(size);
  for(let i=0;i<length;i++){const x=binIndex(payload.grid.x_edges,p.x[i]),y=binIndex(payload.grid.y_edges,p.y[i]);if(x<0||y<0)throw Error('Every cached point must lie within the recorded shared grid');const b=y*nx+x;bins[i]=b;n[b]++;}
  if(section.pla_counts.length!==ny)throw Error('Saved per-section count shape differs from grid');
  for(let y=0;y<ny;y++){if(section.pla_counts[y].length!==nx)throw Error('Saved per-section count shape differs from grid');for(let x=0;x<nx;x++)if(n[y*nx+x]!==section.pla_counts[y][x])throw Error('Cached point membership disagrees with saved per-section PLA counts');}
  records.set(section.section_id,{section,points:p,feature:f,bins,n,nx,ny,size});
 }
 preparedCache.unshift({grid:payload.grid,sections:payload.sections,features,points,records});if(preparedCache.length>2)preparedCache.pop();return records;
}
function sectionValues(record,id,cutoff,marker){
 const {feature:f,bins,n,size}=record,area=f.area_um2,intensity=f.intensity,flags=(f.markers||{})[marker]||[],markerMetric=id.startsWith('marker_associated');
 if(markerMetric&&flags.length!==bins.length)throw Error('Selected marker flags must index every point exactly once');
 const nearest=f.nearest_neighbor_distance||[];if(id==='mean_pla_nearest_neighbor_distance'&&nearest.length!==bins.length)throw Error('Nearest-neighbor distances must index every point exactly once');
 const sums=new Float64Array(size),bad=new Uint32Array(size),large=new Float64Array(size),markerN=new Float64Array(size),markerBad=new Uint32Array(size),markerAreaBad=new Uint32Array(size),bucket=['median_pla_area','p90_pla_area','pla_area_iqr','median_pla_intensity'].includes(id)?new Map():null;
 const totalArea=id==='marker_associated_pla_area_fraction'?new Float64Array(size):null;
 for(let i=0;i<bins.length;i++){
  const b=bins[i],a=area[i],aGood=finite(a)&&a>=0;
  if(id==='mean_pla_intensity'||id==='median_pla_intensity'){if(finite(intensity[i])){sums[b]+=intensity[i];if(bucket){if(!bucket.has(b))bucket.set(b,[]);bucket.get(b).push(intensity[i]);}}else bad[b]++;continue;}
  if(id==='mean_pla_nearest_neighbor_distance'){if(finite(nearest[i])&&nearest[i]>=0)sums[b]+=nearest[i];else bad[b]++;continue;}
  if(totalArea){if(aGood)totalArea[b]+=a;else bad[b]++;}
  if(markerMetric){const flag=flags[i];if(!finite(flag)||(flag!==0&&flag!==1)){markerBad[b]++;continue;}if(flag!==1)continue;markerN[b]++;if(!aGood){markerAreaBad[b]++;continue;}sums[b]+=a;if(a>=cutoff)large[b]++;continue;}
  if(!aGood){bad[b]++;continue;}sums[b]+=a;if(a>=cutoff)large[b]++;
  if(bucket){if(!bucket.has(b))bucket.set(b,[]);bucket.get(b).push(a);}
 }
 // Centered two-pass population variance; never E[x²]-E[x]² cancellation.
 const squared=id==='pla_area_cv'?new Float64Array(size):null;
 if(squared)for(let i=0;i<bins.length;i++)if(finite(area[i])&&area[i]>=0){const b=bins[i],delta=area[i]-sums[b]/n[b];squared[b]+=delta*delta;}
 const values=new Float64Array(size);values.fill(NaN);
 for(let b=0;b<size;b++){
  if(markerMetric){
   if(markerBad[b])continue;
   if(id==='marker_associated_pla_count')values[b]=markerN[b];
   else if(id==='marker_associated_pla_fraction'){if(n[b])values[b]=markerN[b]/n[b];}
   else if(id==='marker_associated_large_pla_count'){if(!markerAreaBad[b])values[b]=large[b];}
   else if(id==='marker_associated_pla_mean_area'){if(markerN[b]&&!markerAreaBad[b])values[b]=sums[b]/markerN[b];}
   else if(id==='marker_associated_pla_area_fraction'){if(!bad[b]&&totalArea[b]>0)values[b]=sums[b]/totalArea[b];}
  }else{
   if(bad[b])continue;
   if(id==='large_pla_count')values[b]=large[b];
   else if(id==='small_pla_count')values[b]=n[b]-large[b];
   else if(id==='large_pla_fraction'){if(n[b])values[b]=large[b]/n[b];}
   else if(id==='total_pla_area')values[b]=sums[b];
   else if(id==='mean_pla_area'||id==='mean_pla_intensity'||id==='mean_pla_nearest_neighbor_distance'){if(n[b])values[b]=sums[b]/n[b];}
   else if(id==='pla_area_cv'){if(n[b]>=2&&sums[b]>0)values[b]=Math.sqrt(squared[b]/n[b])/(sums[b]/n[b]);}
   else if(bucket&&n[b]){const sorted=bucket.get(b).sort((a,c)=>a-c);values[b]=id==='pla_area_iqr'?quantile(sorted,.75)-quantile(sorted,.25):quantile(sorted,id==='p90_pla_area' ? .9 : .5);}
  }
 }
 return values;
}
function calculate(input,features,measurementId,options={}){
 const areaCutoff=options.areaCutoff===undefined?.1:options.areaCutoff,marker=options.marker||'chat',comparisonId=options.comparison||'absolute_difference';
 const sourceMeta=MEASUREMENTS.find(m=>m.id===measurementId),sourceComparison=COMPARISONS.find(c=>c.id===comparisonId);if(!sourceMeta||!sourceComparison)throw Error('Unknown spatial measurement or comparison');
 if(!finite(areaCutoff)||areaCutoff<0)throw Error('The area cutoff must be a finite nonnegative number');
 const chosen=select(input),payload=chosen.payload,points=chosen.points;validateGrid(payload.grid);const nx=payload.grid.x_edges.length-1,ny=payload.grid.y_edges.length-1,size=nx*ny;
 const markerMeta=(features.available_markers||[]).find(m=>m.id===marker);if(sourceMeta.needsMarker&&!markerMeta)throw Error('Selected marker is not present in the feature cache');
 const measurement={...sourceMeta};if(measurement.needsMarker)measurement.label=measurement.label.replace('Marker-associated',markerMeta.label+'-associated');
 const comparison={...sourceComparison};if(comparisonId==='absolute_difference')comparison.units=measurement.difference_units||measurement.units;
 if(new Set(payload.sections.map(s=>s.section_id)).size!==payload.sections.length)throw Error('Repeated section identities cannot increase replication');
 const countOnly=measurementId==='pla_count'||measurementId==='section_pla_share',prepared=countOnly?null:prepare(payload,features,points),computed=[],computedMap=new Map();
 for(const section of payload.sections){let values;
  if(countOnly){if(section.pla_counts.length!==ny||section.pla_counts.some(r=>r.length!==nx))throw Error('PLA count matrix shape differs from grid');values=Float64Array.from(section.pla_counts.flat());if(values.some(v=>!finite(v)||v<0||!Number.isInteger(v)))throw Error('PLA counts must be finite nonnegative integer matrices');
   if(measurementId==='section_pla_share'){const inGrid=values.reduce((a,b)=>a+b,0),total=section.pla_objects===undefined?inGrid:section.pla_objects;if(!finite(total)||!Number.isInteger(total)||total<inGrid)throw Error('Section PLA total must be a nonnegative integer at least as large as its grid count');if(total>0)for(let b=0;b<size;b++)values[b]=values[b]/total*100;else values.fill(NaN);}
  }
  else values=sectionValues(prepared.get(section.section_id),measurementId,areaCutoff,marker);
  computedMap.set(section.section_id,values);computed.push({section_id:section.section_id,values:rows(values,nx),defined:rows(Array.from(values,finite),nx,true)});
 }
 const arms={};let limit=0;
 for(const arm of ['HK1','PFKP']){
  const eligibility=payload.arms[arm].displayable;if(eligibility.length!==ny||eligibility.some(r=>r.length!==nx))throw Error('Eligibility shape differs from grid');
  const eligible=eligibility.flat(),means={},counts={};
  for(const condition of ['Homecage','Running']){
   const group=payload.sections.filter(s=>s.pla_type===arm&&s.condition===condition);if(group.length!==3||new Set(group.map(s=>s.animal_id||s.section_id)).size!==3)throw Error('Each arm/condition requires three distinct animal sections');
   const totals=new Float64Array(size),n=new Uint8Array(size);for(const s of group){const values=computedMap.get(s.section_id);for(let b=0;b<size;b++)if(finite(values[b])){totals[b]+=values[b];n[b]++;}}
   const mean=new Float64Array(size);for(let b=0;b<size;b++)mean[b]=n[b]?totals[b]/n[b]:NaN;means[condition]=mean;counts[condition]=n;
  }
  const h=means.Homecage,r=means.Running,hm=new Float64Array(size),rm=new Float64Array(size),absolute=new Float64Array(size),value=new Float64Array(size),displayable=Array(size),reasons=Array(size).fill(null);hm.fill(NaN);rm.fill(NaN);absolute.fill(NaN);value.fill(NaN);
  for(let b=0;b<size;b++){
   displayable[b]=false;if(!eligible[b]){reasons[b]='outside_display_domain';continue;}
   hm[b]=h[b];rm[b]=r[b];absolute[b]=r[b]-h[b];
   const compared=compareConditions(r[b],h[b],comparisonId);reasons[b]=compared.missing_reason;
   if(compared.defined){value[b]=compared.values;displayable[b]=true;limit=Math.max(limit,Math.abs(compared.values));}
  }
  arms[arm]={homecage_mean:rows(hm,nx),running_mean:rows(rm,nx),homecage_valid_section_n:rows(counts.Homecage,nx),running_valid_section_n:rows(counts.Running,nx),comparison_value:rows(value,nx),difference:rows(value,nx),absolute_difference:rows(absolute,nx),displayable:rows(displayable,nx,true),eligibility:eligibility.map(row=>row.map(Boolean)),missing_reason:objectRows(reasons,nx)};
 }
 limit=limit||1;
 return {measurement,comparison,area_cutoff:areaCutoff,marker,sections:computed,arms,coverage_verified:false,eligibility_policy:'Preserved current per-arm display domain; no tissue mask inferred',quantile_method:'type7_linear',pseudocount:null,color_scale:{cmin:-limit,cmax:limit,center:0,shared_across_arms:true,label:comparison.label+' · '+measurement.label,units:comparison.units}};
}
const api={MEASUREMENTS,COMPARISONS,calculate,compareConditions,binIndex,quantile,clearCache:()=>{preparedCache.length=0;}};
if(typeof module==='object'&&module.exports)module.exports=api;
scope.COMET_MEASUREMENTS=api;
})(typeof window!=='undefined'?window:globalThis);
