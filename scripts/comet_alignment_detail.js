/* Exact high-detail alignment inspection. No fitting, sampling, masks or anatomy. */
(function (global) {
  'use strict';

  function inversePoint(matrix, point) {
    const a=matrix[0][0], b=matrix[0][1], c=matrix[1][0], d=matrix[1][1];
    const determinant=a*d-b*c;
    if (!Number.isFinite(determinant)||determinant===0) throw new Error('Non-invertible supplied transform');
    const x=point[0]-matrix[0][2], y=point[1]-matrix[1][2];
    return [(d*x-b*y)/determinant,(-c*x+a*y)/determinant];
  }
  function forwardPoint(matrix, point) {
    return [matrix[0][0]*point[0]+matrix[0][1]*point[1]+matrix[0][2],
            matrix[1][0]*point[0]+matrix[1][1]*point[1]+matrix[1][2]];
  }
  function binIndex(edges, value) {
    if (!Number.isFinite(value)||value<edges[0]||value>edges[edges.length-1]) return -1;
    if (value===edges[edges.length-1]) return edges.length-2;
    let lo=0, hi=edges.length-1;
    while (lo<hi) { const mid=Math.floor((lo+hi+1)/2); if(edges[mid]<=value)lo=mid;else hi=mid-1; }
    return lo;
  }
  function nativeTileGrid(section, grid, frame) {
    const matrix=section.fixed_transform.matrix;
    const native=frame==='native';
    if(native&&(matrix[0][1]!==0||matrix[1][0]!==0)) return null;
    let x=grid.x_edges.slice(),y=grid.y_edges.slice();
    if(native) { x=x.map(v=>inversePoint(matrix,[v,0])[0]); y=y.map(v=>inversePoint(matrix,[0,v])[1]); }
    const reverseX=x[0]>x[x.length-1],reverseY=y[0]>y[y.length-1];
    if(reverseX)x.reverse();if(reverseY)y.reverse();
    const ix=x.slice(0,-1).map((_,i)=>reverseX?x.length-2-i:i);
    const iy=y.slice(0,-1).map((_,i)=>reverseY?y.length-2-i:i);
    return {x_edges:x,y_edges:y,ix,iy,
      pla_counts:iy.map(j=>ix.map(i=>section.pla_counts[j][i])),
      chat_counts:iy.map(j=>ix.map(i=>section.chat_counts[j][i])),
      observed_support:iy.map(j=>ix.map(i=>section.observed_support[j][i])),
      frame,rectangles_are_exact_inverse_images:native};
  }
  function exactTileMesh(tile,z) {
    const mesh={x:[],y:[],z:[],i:[],j:[],k:[],intensity:[],text:[]};
    for(let iy=0;iy<tile.pla_counts.length;iy++)for(let ix=0;ix<tile.pla_counts[iy].length;ix++){
      if(!tile.observed_support[iy][ix])continue;
      const v=mesh.x.length,x0=tile.x_edges[ix],x1=tile.x_edges[ix+1],y0=tile.y_edges[iy],y1=tile.y_edges[iy+1];
      const pla=tile.pla_counts[iy][ix],chat=tile.chat_counts[iy][ix];
      mesh.x.push(x0,x1,x1,x0);mesh.y.push(y0,y0,y1,y1);mesh.z.push(z,z,z,z);
      mesh.i.push(v,v);mesh.j.push(v+1,v+2);mesh.k.push(v+2,v+3);mesh.intensity.push(pla,pla);
      const text='PLA='+pla+'; ChAT='+chat+'<br>Displayed bin ['+x0+', '+x1+'] × ['+y0+', '+y1+']';
      mesh.text.push(text,text,text,text);
    }
    return mesh;
  }
  function pointCoordinates(points,frame){
    if(frame==='native') {
      if(!Array.isArray(points.native_x)||!Array.isArray(points.native_y))return null;
      return {x:points.native_x,y:points.native_y};
    }
    return {x:points.x,y:points.y};
  }
  function sharedCountRange(allSections,selection){
    let maximum=1;
    for(const section of allSections)for(const row of section.pla_counts)for(const value of row)maximum=Math.max(maximum,value);
    return {maximum,limit:selection==='full'?maximum:Number(selection)};
  }
  const pure={inversePoint,forwardPoint,binIndex,nativeTileGrid,exactTileMesh,pointCoordinates,sharedCountRange};
  global.COMET_ALIGNMENT_DETAIL=pure;
  const app=global.COMET_CORE_EXPLORER;
  if(!app||!global.document||!app.multiresolution?.resolutions||!app.multiresolution?.pla_points?.length)return;

  const Q=id=>document.getElementById(id),H=app.helpers,AH=app.alignmentHelpers;
  const esc=H.esc,num=H.num,config=H.cfg;
  const animalOrder=['21F','23M','24M','22F','21M','22M'];
  const palette=['#0072B2','#009E73','#7C52A1','#D55E00','#E69F00','#CC79A7'];
  const densityScale='Cividis';
  let roi=null,cacheKey='',cache=new Map(),detailGeneration=0,lastRenderContext='',lastReviewBin='',mainGeneration=0;
  let renderTask=Promise.resolve();
  let pointSize=1.7;
  const pointById=new Map(app.multiresolution.pla_points.map(p=>[p.section_id,p]));
  const selectedByJob=new Map((app.data.cohort_selection?.sections||[]).map(s=>[String(s.job),s]));
  let detailSection='';

  const payload=()=>app.resolutions[String(app.resolution)];
  const color=s=>s.snapshot?.color||palette[Math.max(0,animalOrder.indexOf(s.section.animal_id))%palette.length];
  const sectionLabel=s=>s.section.animal_id+' · '+s.section.condition;
  function joinRows(state){
    const current=payload();if(!current)return [];
    const byId=new Map(current.sections.map(s=>[s.section_id,s]));
    return state.rows.map(snapshot=>{
      const chosen=selectedByJob.get(String(snapshot.job));
      const id=chosen?.section_id||snapshot.section_id;
      const section=byId.get(id)||current.sections.find(s=>s.source?.source_file_id==='historical_job_'+snapshot.job);
      return section?{section,snapshot,points:pointById.get(section.section_id)}:null;
    }).filter(Boolean);
  }
  function activeCache(entry,frame){
    const key=app.resolution+'|'+Q('align-arm').value+'|'+frame;
    if(cacheKey!==key){cacheKey=key;cache=new Map();}
    const sid=entry.section.section_id;
    if(!cache.has(sid))cache.set(sid,{tile:nativeTileGrid(entry.section,payload().grid,frame)});
    return cache.get(sid);
  }
  function customCounts(entry,frame){
    const item=activeCache(entry,frame),tile=item.tile;if(!tile)return null;
    if(!item.custom){const grid=payload().grid;
      item.custom=tile.iy.map((iy,j)=>tile.ix.map((ix,i)=>[
        tile.pla_counts[j][i],tile.chat_counts[j][i],grid.x_edges[ix],grid.x_edges[ix+1],grid.y_edges[iy],grid.y_edges[iy+1]]));
    }return item.custom;
  }
  function customPoints(entry,frame){
    const item=activeCache(entry,frame),p=entry.points,grid=payload().grid;
    if(!item.pointsCustom)item.pointsCustom=p.x.map((x,i)=>{
      const ix=binIndex(grid.x_edges,x),iy=binIndex(grid.y_edges,p.y[i]);
      return [p.object_id[i],p.source_row[i],p.native_x?.[i],p.native_y?.[i],
        iy<0||ix<0?null:entry.section.pla_counts[iy][ix],iy<0||ix<0?null:entry.section.chat_counts[iy][ix]];
    });return item.pointsCustom;
  }
  function countLimit(){
    const selected=Q('align-count-range')?.value||'full';
    return sharedCountRange(payload().sections,selected);
  }
  function ranges(entries,frame){
    const grid=payload().grid,points=[];
    // Crop the VIEW to actual exported-object bins, preserving coordinates and
    // every source point. Empty common-grid padding need not occupy the canvas.
    for(const entry of entries){
      const item=activeCache(entry,frame),tile=item.tile;
      if(tile){
        if(!item.observedExtent){let x0=Infinity,x1=-Infinity,y0=Infinity,y1=-Infinity;
          for(let iy=0;iy<tile.observed_support.length;iy++)for(let ix=0;ix<tile.observed_support[iy].length;ix++)if(tile.observed_support[iy][ix]){
            x0=Math.min(x0,tile.x_edges[ix]);x1=Math.max(x1,tile.x_edges[ix+1]);
            y0=Math.min(y0,tile.y_edges[iy]);y1=Math.max(y1,tile.y_edges[iy+1]);
          }item.observedExtent=Number.isFinite(x0)?[[x0,x1],[y0,y1]]:null;
        }
        if(item.observedExtent){points.push([item.observedExtent[0][0],item.observedExtent[1][0]],
          [item.observedExtent[0][1],item.observedExtent[1][1]]);continue;}
      }
      for(const x of [grid.x_edges[0],grid.x_edges.at(-1)])for(const y of [grid.y_edges[0],grid.y_edges.at(-1)])points.push(frame==='native'?inversePoint(entry.section.fixed_transform.matrix,[x,y]):[x,y]);
    }
    const x=[Math.min(...points.map(p=>p[0])),Math.max(...points.map(p=>p[0]))],y=[Math.min(...points.map(p=>p[1])),Math.max(...points.map(p=>p[1]))];
    const px=(x[1]-x[0])*.025,py=(y[1]-y[0])*.025;
    return [[x[0]-px,x[1]+px],[y[0]-py,y[1]+py]];
  }
  function axisPair(frame,range,xref){
    const grid=payload().grid,xd=grid.display_directions?.x||'right',yd=grid.display_directions?.y||'down';
    const xrange=frame==='native'||xd==='right'?range[0]:range[0].slice().reverse();
    const yrange=frame==='native'||yd==='down'?range[1].slice().reverse():range[1];
    return {x:{title:{text:''},range:xrange,showticklabels:false,showgrid:false,zeroline:false,constrain:'domain'},
      y:{title:{text:''},range:yrange,showticklabels:false,showgrid:false,zeroline:false,scaleanchor:xref,scaleratio:1,constrain:'domain'}};
  }
  function heatTrace(entry,frame,opacity,limit,support){
    const tile=activeCache(entry,frame).tile;if(!tile)return null;
    const z=tile.pla_counts.map((row,iy)=>row.map((n,ix)=>tile.observed_support[iy][ix]?(support?1:n):null));
    return {type:'heatmap',x:tile.x_edges,y:tile.y_edges,z,zmin:0,zmax:support?1:limit,
      colorscale:support?[[0,color(entry)],[1,color(entry)]]:densityScale,zsmooth:false,hoverongaps:false,
      opacity,showscale:false,customdata:customCounts(entry,frame),name:sectionLabel(entry),
      meta:{section_id:entry.section.section_id,kind:'counts'},
      hovertemplate:'<b>'+esc(sectionLabel(entry))+'</b><br>Raw PLA=%{customdata[0]:,}; ChAT=%{customdata[1]:,}<br>Aligned bin X=[%{customdata[2]:,.0f}, %{customdata[3]:,.0f}]<br>Aligned bin Y=[%{customdata[4]:,.0f}, %{customdata[5]:,.0f}]<br>Full-bin counts; observed support is not tissue coverage<extra>'+esc(entry.section.section_id)+'</extra>'};
  }
  function pointTrace(entry,frame,flat,z,opacity,indices){
    const p=entry.points,xy=pointCoordinates(p,frame);if(!xy)return null;
    const index=indices||p.x.map((_,i)=>i),custom=customPoints(entry,frame);
    const trace={type:flat?'scattergl':'scatter3d',mode:'markers',x:index.map(i=>xy.x[i]),y:index.map(i=>xy.y[i]),
      customdata:index.map(i=>custom[i]),showlegend:false,name:sectionLabel(entry),
      marker:{size:pointSize,color:color(entry),opacity:Math.max(.15,Math.min(.9,opacity))},
      meta:{section_id:entry.section.section_id,kind:'points'},
      hovertemplate:'<b>'+esc(sectionLabel(entry))+'</b><br>PLA Object Id=%{customdata[0]} · source row %{customdata[1]}<br>Native X=%{customdata[2]:,.1f}, Y=%{customdata[3]:,.1f}<br>Displayed X=%{x:,.1f}, Y=%{y:,.1f}<br>Current full bin: PLA=%{customdata[4]:,}, ChAT=%{customdata[5]:,}<br>Bounding-box midpoint proxy; not a measured centroid<extra>'+esc(entry.section.source.source_file_id)+'</extra>'};
    if(!flat)trace.z=index.map(()=>z);return trace;
  }
  function installWorkspace(){
    if(Q('alignment-detail-workspace'))return;
    const controls=Q('align-content').closest('.controls');
    const range=document.createElement('label');range.innerHTML='Linear PLA-count colour range<select id="align-count-range"><option value="full">Full observed section range</option><option value="100">0–100 counts</option><option value="50">0–50 counts</option><option value="25">0–25 counts</option><option value="10">0–10 counts</option></select>';
    controls.insertBefore(range,controls.querySelector('.buttons'));
    const points=document.createElement('label');points.innerHTML='Exact-point size<input id="align-point-size" type="range" min=".5" max="4" step=".25" value="1.7">';
    controls.insertBefore(points,controls.querySelector('.buttons'));
    const article=document.createElement('article');article.id='alignment-detail-workspace';article.className='card';article.style.marginTop='18px';
    article.innerHTML='<div class="padded" style="padding-bottom:0"><h2>Inspect each section in two dimensions.</h2><p style="font-size:12px;color:#61798b">The atlas separates the six animals. Click the overlay for a local window, or inspect one section in detail. Every exported PLA midpoint in the window is retained; fine-bin tiles show exact full-bin PLA counts. Original coordinates remain on hover; no physical scale bar is implied.</p></div><div class="controls" style="border-left:0;border-right:0;border-radius:0;margin:0"><label>Section view<select id="align-detail-layout"><option value="atlas">All six individual sections</option><option value="single">One section · larger view</option></select></label><label>Selected section<select id="align-detail-section"></select></label><label>Click window<select id="align-detail-width"><option value="2000">Close detail</option><option value="4000" selected>Local region</option><option value="8000">Broad region</option></select></label><label style="flex-direction:row;align-items:center;padding-bottom:7px"><input id="align-detail-tiles" type="checkbox" checked>Exact count tiles</label><label style="flex-direction:row;align-items:center;padding-bottom:7px"><input id="align-detail-points" type="checkbox" checked>All PLA midpoint points</label><button id="align-detail-viewport">Use overlay viewport</button><button id="align-detail-reset">Full field · six sections</button></div><div id="alignment-detail-summary" class="readout" style="margin:12px 18px"></div><div id="alignment-detail-plot" style="height:920px"></div><div id="alignment-detail-object" class="caption">Hover a point for its exact section, object ID and source row. Dots represent detections, not microscopy pixels or literal molecules.</div><div class="caption">All six panels share one linear raw-count colour scale and preserve the saved orientation. The view fits exported-object extents without fitting or changing alignment. Native tiles are exact inverse-mapped rectangles under saved translations/reflections. Coverage is uncertain; blank object bins are not proof of absent tissue. The frozen original alignment check remains unchanged.</div>';
    Q('alignment-content').querySelector('.alignment-layout').insertAdjacentElement('afterend',article);
    for(const id of ['align-count-range','align-point-size'])Q(id).oninput=()=>{pointSize=Number(Q('align-point-size').value);app.renderAlignment();};
    for(const id of ['align-detail-layout','align-detail-section','align-detail-width','align-detail-tiles','align-detail-points'])Q(id).oninput=()=>{detailSection=Q('align-detail-section').value;renderDetail();};
    Q('align-detail-reset').onclick=()=>{roi=null;Q('align-detail-layout').value='atlas';renderDetail();};
    Q('align-detail-viewport').onclick=()=>{
      const plot=Q('alignment-plot'),layout=plot.layout;
      if(Q('align-view').value!=='flat'||!layout?.xaxis?.range)return;
      const rect={xmin:Math.min(...layout.xaxis.range),xmax:Math.max(...layout.xaxis.range),ymin:Math.min(...layout.yaxis.range),ymax:Math.max(...layout.yaxis.range)};
      const entry=currentEntries().find(s=>s.section.section_id===detailSection)||currentEntries()[0];
      roi={...(Q('align-frame').value==='native'?forwardRect(entry,rect):rect),arm:Q('align-arm').value};renderDetail();
    };
    const sidebar=Q('alignment-content').querySelector('.sidebar > div');
    if(sidebar)sidebar.innerHTML='<h3>Two-dimensional section review</h3><p>Fine-grid raw counts and every exported PLA midpoint are shown in the saved orientation. All twelve sections share one count-colour range at each selected level of detail.</p><p><strong>Overlay is for comparison.</strong> Blending colours is not a condition mean. The separate section panels expose individual contributions; the comparison tab contains the calculated condition averages.</p><p><strong>Coverage is uncertain.</strong> Observed detections are not a tissue boundary. No serial-section or physical-depth reconstruction is used.</p>';
    const downloads=document.createElement('div');downloads.className='downloads';downloads.style.paddingTop='12px';
    for(const figure of app.data.review_figures||[])if(figure.id?.startsWith('alignment_detail_')&&figure.data_url){
      const link=document.createElement('a');link.href=figure.data_url;link.download=figure.filename||figure.id+'.png';link.textContent='Download full-point '+(figure.id.includes('pfkp')?'PFKP':'HK1')+' atlas · 600 DPI';downloads.appendChild(link);
    }if(downloads.children.length)article.appendChild(downloads);
  }
  function currentEntries(){return joinRows(app.getAlignmentState()).sort((a,b)=>animalOrder.indexOf(a.section.animal_id)-animalOrder.indexOf(b.section.animal_id));}
  function forwardRect(entry,rect){
    const matrix=entry.section.fixed_transform.matrix,corners=[];
    for(const x of [rect.xmin,rect.xmax])for(const y of [rect.ymin,rect.ymax])corners.push(forwardPoint(matrix,[x,y]));
    return {xmin:Math.min(...corners.map(p=>p[0])),xmax:Math.max(...corners.map(p=>p[0])),ymin:Math.min(...corners.map(p=>p[1])),ymax:Math.max(...corners.map(p=>p[1]))};
  }
  function localRange(entry,frame){
    if(!roi)return ranges([entry],frame);
    if(frame==='saved')return [[roi.xmin,roi.xmax],[roi.ymin,roi.ymax]];
    const matrix=entry.section.fixed_transform.matrix,points=[];
    for(const x of [roi.xmin,roi.xmax])for(const y of [roi.ymin,roi.ymax])points.push(inversePoint(matrix,[x,y]));
    return [[Math.min(...points.map(p=>p[0])),Math.max(...points.map(p=>p[0]))],[Math.min(...points.map(p=>p[1])),Math.max(...points.map(p=>p[1]))]];
  }
  function selectPoint(event){
    const point=event.points?.[0],id=point?.data?.meta?.section_id;if(!id)return;
    const entry=currentEntries().find(s=>s.section.section_id===id);if(!entry)return;
    let aligned=[point.x,point.y];if(Q('align-frame').value==='native')aligned=forwardPoint(entry.section.fixed_transform.matrix,aligned);
    const width=Number(Q('align-detail-width').value);
    roi={xmin:aligned[0]-width/2,xmax:aligned[0]+width/2,ymin:aligned[1]-width/2,ymax:aligned[1]+width/2,arm:Q('align-arm').value};
    detailSection=id;Q('align-detail-section').value=id;Q('align-detail-layout').value='single';renderDetail();
  }
  async function renderDetail(){
    const generation=++detailGeneration,entries=currentEntries();if(!entries.length)return;
    const options=Q('align-detail-section');
    if(!entries.some(e=>e.section.section_id===detailSection))detailSection=entries[0].section.section_id;
    const old=options.value;options.innerHTML=entries.map(e=>'<option value="'+esc(e.section.section_id)+'">'+esc(sectionLabel(e))+'</option>').join('');options.value=detailSection||old;
    const single=Q('align-detail-layout').value==='single',chosen=single?entries.filter(e=>e.section.section_id===detailSection):entries;
    const frame=Q('align-frame').value,limits=countLimit(),traces=[],annotations=[],layout={
      template:'plotly_white',paper_bgcolor:'white',plot_bgcolor:'#e7edf2',font:{family:'Arial',size:10,color:'#466a83'},
      margin:{l:20,r:85,b:20,t:48},showlegend:false,dragmode:'zoom',uirevision:'detail-'+app.resolution+'-'+Q('align-arm').value+'-'+frame+'-'+JSON.stringify(roi)+'-'+single};
    let shown=0,clipped=0;
    chosen.forEach((entry,index)=>{
      const axis=index===0?'':String(index+1),xref='x'+axis,yref='y'+axis;
      const col=single?0:index%3,row=single?0:Math.floor(index/3),dx=single?[0,1]:[col/3+.025,(col+1)/3-.055],dy=single?[0,1]:row===0?[.56,1]:[0,.44];
      const pair=axisPair(frame,localRange(entry,frame),xref);
      layout['xaxis'+axis]={...pair.x,domain:dx,anchor:yref};layout['yaxis'+axis]={...pair.y,domain:dy,anchor:xref};
      const count=Q('align-detail-tiles').checked?heatTrace(entry,frame,.7,limits.limit,false):null;
      if(count){count.xaxis=xref;count.yaxis=yref;count.showscale=index===0;count.colorbar={title:{text:'Raw PLA / section-bin'},thickness:12,len:.75,x:1.015};traces.push(count);}
      const point=entry.points,indexes=[];
      for(let i=0;i<point.x.length;i++)if(!roi||(point.x[i]>=roi.xmin&&point.x[i]<=roi.xmax&&point.y[i]>=roi.ymin&&point.y[i]<=roi.ymax))indexes.push(i);
      shown+=indexes.length;
      if(Q('align-detail-points').checked){const dots=pointTrace(entry,frame,true,0,.75,indexes);if(dots){dots.xaxis=xref;dots.yaxis=yref;traces.push(dots);}}
      if(Q('align-guides').checked){const guides=[];AH.appendSavedGuides(guides,entry.snapshot,true,0,color(entry));for(const guide of guides){guide.xaxis=xref;guide.yaxis=yref;traces.push(guide);}}
      for(const rowValues of entry.section.pla_counts)for(const value of rowValues)if(value>limits.limit)clipped++;
      annotations.push({xref:'paper',yref:'paper',x:(dx[0]+dx[1])/2,y:dy[1]+.045,text:'<b>'+esc(sectionLabel(entry))+'</b> · '+num(indexes.length)+' PLA points',showarrow:false,font:{size:11},xanchor:'center'});
    });
    layout.annotations=annotations;Q('alignment-detail-plot').style.height=single?'700px':'940px';
    Q('alignment-detail-summary').textContent=num(shown)+' exact PLA midpoint proxies in '+(roi?'the selected aligned window':'the full field')+' · '+(single?'one section':'six separate sections')+' · '+(Q('align-detail-tiles').checked&&limits.limit<limits.maximum?num(clipped)+' full-field section-bins beyond colour range; exact hover values retained':'full linear section-count range')+'. '+(roi?'Tiles retain their full-bin counts; points are selected by viewport.':'No point sampling.');
    await Plotly.react('alignment-detail-plot',traces,layout,config);
    if(generation!==detailGeneration)return;
    const plot=Q('alignment-detail-plot');plot.removeAllListeners?.('plotly_hover');
    plot.on('plotly_hover',event=>{const p=event.points?.[0];if(p?.data?.meta?.kind==='points')Q('alignment-detail-object').textContent=p.data.meta.section_id+' · Object Id '+p.customdata[0]+' · source row '+p.customdata[1]+' · native ('+num(p.customdata[2])+', '+num(p.customdata[3])+') · current bin PLA '+p.customdata[4]+', ChAT '+p.customdata[5]+'. Bounding-box midpoint proxy; not a measured centroid.';});
  }
  async function renderAlignmentNow(generation){
    const current=payload(),state=app.getAlignmentState(),entries=joinRows(state);
    if(!current||!entries.length||entries.length!==state.rows.length||entries.some(e=>!e.points))return false;
    installWorkspace();AH.layerControls();
    if(roi&&roi.arm!==Q('align-arm').value)roi=null;
    const reviewed=state.reviewBin,reviewKey=reviewed?JSON.stringify(reviewed):'';
    if(reviewed&&reviewed.arm===Q('align-arm').value&&reviewKey!==lastReviewBin){
      const width=Number(Q('align-detail-width').value),x=(reviewed.xmin+reviewed.xmax)/2,y=(reviewed.ymin+reviewed.ymax)/2;
      roi={xmin:x-width/2,xmax:x+width/2,ymin:y-width/2,ymax:y+width/2,arm:reviewed.arm};lastReviewBin=reviewKey;
    }
    const visibleIds=new Set(state.chosen.map(AH.sid)),chosen=entries.filter(e=>visibleIds.has(AH.sid(e.snapshot)));
    Q('align-view').value='flat';
    const flat=true,frame=Q('align-frame').value,content=Q('align-content').value;
    const dots=content==='points'||content==='both',tiles=content!=='points',support=content==='support';
    const opacity=Number(Q('align-opacity').value)/100,spacing=Number(Q('align-spacing').value)/100,extent=ranges(entries,frame);
    const span=Math.max(extent[0][1]-extent[0][0],extent[1][1]-extent[1][0]),limits=countLimit(),traces=[];
    let visiblePointCount=0,clipped=0;
    for(const entry of chosen){
      const index=animalOrder.indexOf(entry.section.animal_id),z=index*span*spacing/4;
      if(tiles){const tile=activeCache(entry,frame).tile;
        if(flat){const trace=heatTrace(entry,frame,content==='both'?opacity*.5:opacity,limits.limit,support);if(trace){trace.showscale=!support&&traces.length===0;trace.colorbar={title:{text:'Raw PLA / section-bin'},thickness:13,len:.8};traces.push(trace);}}
        else if(tile){const mesh=exactTileMesh(tile,z);traces.push({...mesh,type:'mesh3d',name:sectionLabel(entry),flatshading:true,intensitymode:'cell',
          ...(support?{color:color(entry),intensity:undefined}:{cmin:0,cmax:limits.limit,colorscale:densityScale}),
          opacity:content==='both'?opacity*.45:opacity,showscale:!support&&traces.length===0,
          colorbar:{title:{text:'Raw PLA / section-bin'},thickness:13,len:.8},
          meta:{section_id:entry.section.section_id,kind:'tiles'},hovertemplate:'<b>'+esc(sectionLabel(entry))+'</b><br>%{text}<br>Z is display separation only<extra>'+esc(entry.section.section_id)+'</extra>',
          lighting:{ambient:1,diffuse:0,specular:0}});}
      }
      if(dots){const trace=pointTrace(entry,frame,flat,z,content==='both'?opacity*.6:opacity);if(trace){visiblePointCount+=entry.points.x.length;traces.push(trace);}}
      for(const row of entry.section.pla_counts)for(const count of row)if(count>limits.limit)clipped++;
      AH.appendSavedGuides(traces,entry.snapshot,flat,z,color(entry));
    }
    const pair=axisPair(frame,extent,'x'),layout={template:'plotly_white',paper_bgcolor:'white',plot_bgcolor:'#e7edf2',font:{family:'Arial',size:11,color:'#446a84'},
      margin:{l:20,r:95,b:20,t:25},showlegend:false,dragmode:'zoom',
      xaxis:pair.x,yaxis:pair.y,uirevision:'alignment-detail-'+app.resolution+'-'+Q('align-arm').value+'-'+frame+'-'+flat+'-'+state.cameraRevision,
      scene:{xaxis:{title:{text:(frame==='native'?'Native':'Fixed aligned')+' X · export units'},range:pair.x.range,nticks:5},
        yaxis:{title:{text:(frame==='native'?'Native':'Fixed aligned')+' Y · preserved direction'},range:pair.y.range,nticks:5},
        zaxis:{title:{text:'Layer separation · display only'},showticklabels:false},aspectmode:'manual',
        aspectratio:{x:1,y:(extent[1][1]-extent[1][0])/(extent[0][1]-extent[0][0]),z:.62},camera:state.camera,dragmode:'orbit'}};
    const selected=state.reviewBin;
    if(selected&&selected.arm===Q('align-arm').value&&frame==='saved'&&flat)layout.shapes=[{type:'rect',xref:'x',yref:'y',x0:selected.xmin,x1:selected.xmax,y0:selected.ymin,y1:selected.ymax,line:{color:'#102f47',width:2,dash:'dash'},fillcolor:'rgba(255,255,255,.06)'}];
    if(!chosen.length)layout.annotations=[{xref:'paper',yref:'paper',x:.5,y:.5,text:'Select at least one section.',showarrow:false}];
    Q('alignment-plot').style.height=flat?'760px':'780px';
    Q('opacity-label').textContent=Math.round(opacity*100)+'%';Q('spacing-control').hidden=flat;
    Q('alignment-title').textContent='TDP43–'+Q('align-arm').value+' · detailed '+(frame==='native'?'native coordinates':'unchanged fixed frame');
    Q('alignment-subtitle').textContent=chosen.length+' / '+entries.length+' sections'+(dots?' · all '+num(visiblePointCount)+' visible-section PLA points':'')+' · two-dimensional view · no sampling';
    Q('alignment-tag').textContent='Fine grid + source objects';
    Q('alignment-caption').textContent=(dots?'Every PLA midpoint in the visible sections is shown. ':'')+(tiles?'Tiles retain exact section counts; ChAT-only bins contain PLA=0. ':'')+(support?'Section colours identify observed detections. ':'')+(limits.limit<limits.maximum&&tiles&&!support?num(clipped)+' visible-section bins exceed the linear display range 0–'+num(limits.limit)+'; hover values remain uncapped. ':'')+'Overlay blending is not a condition mean. Saved anchors and cues remain unchanged. The viewport fits exported objects without changing coordinates. Coverage is uncertain. Click for the linked section window below.';
    await Plotly.react('alignment-plot',traces,layout,config);
    if(generation!==mainGeneration)return true;
    const plot=Q('alignment-plot');plot.removeAllListeners?.('plotly_click');plot.on('plotly_click',selectPoint);
    lastRenderContext=app.mode+'|'+app.resolution+'|'+Q('align-arm').value;
    await renderDetail();return true;
  }
  function detailedAlignment(){
    const current=payload(),state=app.getAlignmentState(),entries=joinRows(state);
    if(!current||!entries.length||entries.length!==state.rows.length||entries.some(e=>!e.points))return false;
    const generation=++mainGeneration;
    // The lifecycle wrapper stages hidden panels at a nonzero size, snapshots
    // inactive WebGL views, and awaits this promise during the eager warm-up.
    // Do not purge its plots or short-circuit hidden panels here.
    const frameReady=new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
    renderTask=renderTask.catch(()=>{}).then(()=>frameReady).then(()=>generation===mainGeneration?renderAlignmentNow(generation):true);
    app.alignmentReady=renderTask;
    return true;
  }
  app.alignmentRenderer=detailedAlignment;
  Object.assign(pure,{render:detailedAlignment,renderDetail,get roi(){return roi;}});
  document.addEventListener('comet:viewchange',event=>{if(event.detail?.tab==='alignment'){
    const context=app.mode+'|'+app.resolution+'|'+Q('align-arm').value;
    if(context!==lastRenderContext||!Q('alignment-plot')?.data||!Q('alignment-detail-plot')?.data)app.renderAlignment();
    else Plotly.Plots.resize('alignment-detail-plot');
  }});
  if(app.activeView==='alignment'||!Q('panel-alignment').hidden)app.renderAlignment();
})(typeof window!=='undefined'?window:globalThis);
