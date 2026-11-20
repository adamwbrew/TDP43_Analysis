/* Exact local rebinning of saved PLA midpoint proxies. No interpolation,
 * alignment fitting, neighbor recomputation or tissue-coverage inference. */
(function(scope){
'use strict';
const Measurements=(typeof module==='object'&&module.exports)?require('./comet_measurements.js'):scope.COMET_MEASUREMENTS;
const WIDTHS=[10,25,50,100],MAX_SIDE=400;
const finite=value=>typeof value==='number'&&Number.isFinite(value);

function uniqueBySection(records,label){
 if(!Array.isArray(records))throw Error(label+' must be an array');
 const result=new Map();
 for(const record of records){
  if(!record||typeof record.section_id!=='string'||result.has(record.section_id))throw Error('Missing or repeated '+label+' section identity');
  result.set(record.section_id,record);
 }
 return result;
}

function detailGrid(base,window,width){
 if(!WIDTHS.includes(width))throw Error('Detail bin width must be 10, 25, 50 or 100 export units');
 if(!window||!['xmin','xmax','ymin','ymax'].every(key=>finite(window[key]))||window.xmax<=window.xmin||window.ymax<=window.ymin)
  throw Error('The detailed window must have finite, increasing X and Y bounds');
 const x0=Math.floor(window.xmin/width)*width,x1=Math.ceil(window.xmax/width)*width;
 const y0=Math.floor(window.ymin/width)*width,y1=Math.ceil(window.ymax/width)*width;
 const nx=Math.round((x1-x0)/width),ny=Math.round((y1-y0)/width);
 if(!Number.isSafeInteger(nx)||!Number.isSafeInteger(ny)||nx<1||ny<1||nx>MAX_SIDE||ny>MAX_SIDE)
  throw Error('This detailed grid exceeds 400 rows or columns; choose a coarser detail bin width or a smaller window');
 return {...base.grid,x_edges:Array.from({length:nx+1},(_,i)=>x0+i*width),
  y_edges:Array.from({length:ny+1},(_,i)=>y0+i*width),shape:[ny,nx],bin_width_export_units:width,
  matrix_order:'y_bin,x_bin',requested_window:{...window},
  provenance:'Exact reassignment of saved PLA midpoint proxies on a regular local grid; no interpolation. Display domain projects the unchanged 100-unit observed domain by bin center; coverage uncertain.'};
}

function projectedDomain(base,grid,arm){
 const source=base.arms?.[arm]?.displayable;
 if(!Array.isArray(source)||source.length!==base.grid.y_edges.length-1||source.some(row=>!Array.isArray(row)||row.length!==base.grid.x_edges.length-1))
  throw Error('The baseline observed display domain does not match its grid');
 const xs=grid.x_edges,ys=grid.y_edges;
 return ys.slice(0,-1).map((y,iy)=>xs.slice(0,-1).map((x,ix)=>{
  const parentX=Measurements.binIndex(base.grid.x_edges,(x+xs[ix+1])/2);
  const parentY=Measurements.binIndex(base.grid.y_edges,(y+ys[iy+1])/2);
  return parentX>=0&&parentY>=0&&!!source[parentY][parentX];
 }));
}

function selectedRecord(record,indices,length,label){
 const result={...record};
 for(const [key,value] of Object.entries(record)){
  if(Array.isArray(value)||ArrayBuffer.isView(value)){
   if(value.length!==length)throw Error(label+' vector '+key+' must index every source PLA object');
   result[key]=indices.map(index=>value[index]);
  }
 }
 return result;
}

function calculate(options){
 if(!Measurements?.calculate)throw Error('The spatial measurement engine must load before detailed rebinning');
 const {base,points,window,binWidth,id='pla_count',areaCutoff=.1,marker='chat',comparison='absolute_difference'}=options||{};
 const features=options?.features||{sections:[],available_markers:[]};
 if(!base?.grid||!Array.isArray(base.sections)||!Array.isArray(base.grid.x_edges)||!Array.isArray(base.grid.y_edges))
  throw Error('The preserved baseline grid and section metadata are required');
 for(const edges of [base.grid.x_edges,base.grid.y_edges])if(edges.length<2||edges.some((value,i)=>!finite(value)||(i&&value<=edges[i-1])))
  throw Error('The baseline grid must have finite, increasing edges');
 const grid=detailGrid(base,window,binWidth),nx=grid.shape[1],ny=grid.shape[0];
 const pointMap=uniqueBySection(points,'point cache'),featureMap=uniqueBySection(features.sections||[],'feature cache');
 const sectionMap=uniqueBySection(base.sections,'baseline');
 if(pointMap.size!==sectionMap.size||[...pointMap.keys()].some(key=>!sectionMap.has(key)))throw Error('Detailed point cache and baseline section cohort disagree');
 if(featureMap.size&& (featureMap.size!==sectionMap.size||[...featureMap.keys()].some(key=>!sectionMap.has(key))))throw Error('Detailed feature cache and baseline section cohort disagree');
 const localPoints=[],localFeatures=[],sections=[];
 for(const section of base.sections){
  const point=pointMap.get(section.section_id),feature=featureMap.get(section.section_id);
  if(!point||!Array.isArray(point.x)||!Array.isArray(point.y)||point.x.length!==point.y.length)throw Error('Complete indexed PLA midpoint coordinates are required');
  const length=point.x.length,indices=[];
  for(let i=0;i<length;i++){
   const x=point.x[i],y=point.y[i];
   if(!finite(x)||!finite(y))throw Error('Every source PLA midpoint must have finite coordinates');
   if(x>=grid.x_edges[0]&&x<=grid.x_edges[nx]&&y>=grid.y_edges[0]&&y<=grid.y_edges[ny])indices.push(i);
  }
  const selected=selectedRecord(point,indices,length,'Point cache');
  selected.point_count=indices.length;selected.full_section_point_count=length;selected.roi_filtered=true;
  localPoints.push(selected);
  if(feature){
   if(point.source_sha256&&feature.source_sha256!==point.source_sha256)throw Error('Measurement feature source hash differs from the point cache');
   const selectedFeature=selectedRecord(feature,indices,length,'Feature cache');
   selectedFeature.markers={};
   for(const [key,values] of Object.entries(feature.markers||{})){
    if(!Array.isArray(values)||values.length!==length)throw Error('Marker flags must index every source PLA object');
    selectedFeature.markers[key]=indices.map(index=>values[index]);
   }
   // The source fingerprint describes the complete cache, not this local slice.
   if(feature.point_order_sha256){selectedFeature.source_point_order_sha256=feature.point_order_sha256;delete selectedFeature.point_order_sha256;}
   selectedFeature.point_count=indices.length;selectedFeature.roi_filtered=true;localFeatures.push(selectedFeature);
  }
  const counts=Array.from({length:ny},()=>Array(nx).fill(0));
  for(let i=0;i<selected.x.length;i++)counts[Measurements.binIndex(grid.y_edges,selected.y[i])][Measurements.binIndex(grid.x_edges,selected.x[i])]++;
  // The original section total remains the share denominator. Never reuse
  // coarse ChAT/support matrices as though they were measurements on this grid.
  const {pla_counts,chat_counts,all_counts,observed_support,tissue_validity,...metadata}=section;
  sections.push({...metadata,pla_counts:counts,pla_objects:section.pla_objects===undefined?length:section.pla_objects});
 }
 const payload={...base,grid,sections,pla_points:localPoints,arms:{}};
 for(const arm of ['HK1','PFKP'])payload.arms[arm]={displayable:projectedDomain(base,grid,arm)};
 const localCache={...features,sections:localFeatures};
 const calculation=Measurements.calculate(payload,localCache,id,{areaCutoff,marker,comparison});
 calculation.eligibility_policy='Fine-bin centers project the unchanged 100-unit observed-object domain; this is context, not verified tissue coverage';
 return {grid,calculation};
}

const api={calculate,WIDTHS:WIDTHS.slice(),MAX_SIDE};
if(typeof module==='object'&&module.exports)module.exports=api;
scope.COMET_DETAIL_GRID=api;
})(typeof window!=='undefined'?window:globalThis);
