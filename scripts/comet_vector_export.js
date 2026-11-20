/* Exact vector grid tiles and context. No screenshot upscaling or interpolation. */
(function(scope){
'use strict';
const finite=v=>typeof v==='number'&&Number.isFinite(v);
const xml=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
const number=v=>Number(v.toPrecision(12)).toString();
function color(value,minimum,maximum,palette){
 const t=Math.max(0,Math.min(1,(value-minimum)/(maximum-minimum)));
 let i=1;while(i<palette.length-1&&t>palette[i][0])i++;
 const [a,ca]=palette[i-1],[b,cb]=palette[i],f=(t-a)/(b-a);
 const rgb=c=>{if(!/^#[0-9a-f]{6}$/i.test(c))throw Error('Export colors must be six-digit hex values');return [1,3,5].map(j=>parseInt(c.slice(j,j+2),16));};
 const x=rgb(ca),y=rgb(cb);return '#'+x.map((v,j)=>Math.round(v+(y[j]-v)*f).toString(16).padStart(2,'0')).join('');
}
function svg(options){
 const {arm,grid,z,contextGeometry:context,contextVisible=true,measurementLabel='',comparisonLabel='',units='',zmin,zmax}=options;
 const palette=options.colorScale||[[0,'#2166ac'],[.5,'#ffffff'],[1,'#b2182b']];
 const xe=grid.x_edges,ye=grid.y_edges;
 if(!finite(zmin)||!finite(zmax)||zmax<=zmin)throw Error('Finite increasing color limits are required');
 if(z.length!==ye.length-1||z.some(row=>row.length!==xe.length-1))throw Error('Export matrix/grid dimensions disagree');
 const v=options.viewport||{xmin:xe[0],xmax:xe[xe.length-1],ymin:ye[0],ymax:ye[ye.length-1]};
 if(![v.xmin,v.xmax,v.ymin,v.ymax].every(finite)||v.xmax<=v.xmin||v.ymax<=v.ymin)throw Error('Export window must have finite increasing bounds');
 const W=2000,left=70,top=210,plotWidth=1710,rawHeight=plotWidth*(v.ymax-v.ymin)/(v.xmax-v.xmin);
 // Highly elongated selections retain a proportional map in a bounded document.
 const plotHeight=Math.max(100,Math.min(5000,rawHeight)),scale=Math.min(plotWidth/(v.xmax-v.xmin),plotHeight/(v.ymax-v.ymin));
 const mapWidth=(v.xmax-v.xmin)*scale,mapHeight=(v.ymax-v.ymin)*scale,H=top+mapHeight+180;
 const X=x=>left+(x-v.xmin)*scale,Y=y=>top+(y-v.ymin)*scale;
 const parts=[`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${number(H)}" viewBox="0 0 ${W} ${number(H)}" role="img" aria-label="${xml(measurementLabel+' '+comparisonLabel+' '+arm)}">`,
 `<title>${xml(measurementLabel+' · '+comparisonLabel+' · TDP43–'+arm)}</title>`,
 `<desc>Exact calculated grid tiles. Undefined bins remain undefined. The optional outline follows detected-object bins, not verified tissue. No smoothing, resampling or physical calibration.</desc>`,
 `<metadata>${xml(JSON.stringify({...options.metadata,arm,measurementLabel,comparisonLabel,units,bin_width:options.binWidth,viewport:v,color_limits:[zmin,zmax],context_visible:contextVisible,coverage_verified:false,vector_tiles:true}))}</metadata>`,
 `<rect width="100%" height="100%" fill="#ffffff"/>`,
 `<g font-family="Arial, sans-serif" fill="#19354a"><text x="70" y="55" font-size="32" font-weight="bold">${xml(measurementLabel)}</text><text x="70" y="99" font-size="25">${xml('TDP43–'+arm+' · '+comparisonLabel)}</text><text x="70" y="138" font-size="20" fill="#567183">${xml((options.binWidth?options.binWidth+'-unit bins · ':'')+'equal section-level means · '+units)}</text><text x="70" y="172" font-size="19" fill="#567183">${xml(options.metadata?.averaging_policy||'Defined-section N and exact values are retained in the bin CSV.')}</text></g>`,
 `<defs><clipPath id="map-window"><rect x="${left}" y="${top}" width="${number(mapWidth)}" height="${number(mapHeight)}"/></clipPath><linearGradient id="colorbar" x1="0" y1="1" x2="0" y2="0">${palette.map(([p,c])=>`<stop offset="${p}" stop-color="${xml(c)}"/>`).join('')}</linearGradient></defs>`,
 `<rect x="${left}" y="${top}" width="${number(mapWidth)}" height="${number(mapHeight)}" fill="#e4e9ee"/>`,
 `<g clip-path="url(#map-window)">`];
 const rect=(x0,x1,y0,y1,fill)=>`<rect x="${number(X(x0))}" y="${number(Y(y0))}" width="${number((x1-x0)*scale)}" height="${number((y1-y0)*scale)}" fill="${fill}"/>`;
 if(contextVisible&&context?.footprint&&context.grid){
  const g=context.grid;parts.push('<g id="observed-object-footprint" shape-rendering="crispEdges">');
  for(let y=0;y<context.footprint.length;y++){
   if(g.y_edges[y+1]<=v.ymin||g.y_edges[y]>=v.ymax)continue;
   let start=-1;for(let x=0;x<=context.footprint[y].length;x++){
    const on=x<context.footprint[y].length&&context.footprint[y][x];
    if(on&&start<0)start=x;
    if(!on&&start>=0){if(g.x_edges[x]>v.xmin&&g.x_edges[start]<v.xmax)parts.push(rect(g.x_edges[start],g.x_edges[x],g.y_edges[y],g.y_edges[y+1],'#f0f3f6'));start=-1;}
   }
  }parts.push('</g>');
 }
 let defined=0,saturated=0;
 parts.push('<g id="calculated-tiles" shape-rendering="crispEdges">');
 for(let y=0;y<z.length;y++){
  if(ye[y+1]<=v.ymin||ye[y]>=v.ymax)continue;
  for(let x=0;x<z[y].length;x++){
   const value=z[y][x];if(!finite(value)||xe[x+1]<=v.xmin||xe[x]>=v.xmax)continue;
   defined++;if(value<zmin||value>zmax)saturated++;
   parts.push(rect(xe[x],xe[x+1],ye[y],ye[y+1],color(value,zmin,zmax,palette)));
  }
 }parts.push('</g>');
 if(contextVisible&&context?.x?.length){
  let path='',move=true;for(let i=0;i<context.x.length;i++){
   if(!finite(context.x[i])||!finite(context.y[i])){move=true;continue;}
   path+=(move?'M':'L')+number(X(context.x[i]))+' '+number(Y(context.y[i]));move=false;
  }
  parts.push(`<path id="observed-object-outline" d="${path}" fill="none" stroke="#778b9b" stroke-width="0.9" stroke-linecap="square"/>`);
 }
 parts.push('</g>');
 const barX=left+mapWidth+50,barY=top+mapHeight*.18,barH=mapHeight*.63;
 parts.push(`<rect x="${number(barX)}" y="${number(barY)}" width="28" height="${number(barH)}" fill="url(#colorbar)"/>`);
 for(const t of [0,.25,.5,.75,1])parts.push(`<text x="${number(barX+40)}" y="${number(barY+barH*(1-t)+7)}" font-family="Arial" font-size="20" fill="#466a83">${xml(Number((zmin+t*(zmax-zmin)).toPrecision(5)))}</text>`);
 parts.push(`<text x="70" y="${number(top+mapHeight+46)}" font-family="Arial" font-size="20" fill="#567183">${xml(defined.toLocaleString('en-US')+' defined tiles in this view · '+saturated.toLocaleString('en-US')+' display-saturated; exact values unchanged')}</text>`,
 `<text x="70" y="${number(top+mapHeight+82)}" font-family="Arial" font-size="19" fill="#567183">${xml(contextVisible?'Pale footprint + outline = detected-object context; not a tissue boundary.':'Object-footprint context hidden. Gray = undefined or outside the observed domain.')}</text>`,
 `<text x="70" y="${number(top+mapHeight+118)}" font-family="Arial" font-size="19" fill="#567183">Tissue coverage uncertain · spacing uses exported coordinate units · no spatial interpolation</text></svg>`);
 return parts.join('');
}
async function download(options){
 const progress=options.onProgress||(()=>{}),format=options.format||'svg',width=options.width||8000;
 if(!['svg','png'].includes(format))throw Error('Choose SVG or PNG');
 if(![8000,12000].includes(width))throw Error('PNG width must be 8000 or 12000 pixels');
 progress('Building exact vector tiles and object-footprint outline…');
 const source=svg(options),blob=new Blob([source],{type:'image/svg+xml;charset=utf-8'});
 const save=(value,name)=>{const url=URL.createObjectURL(value),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),30000);};
 const match=source.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/),height=Math.round(width*Number(match[2])/Number(match[1]));
 const filename=(options.filename||'COMET_spatial_map')+'.'+format;
 if(format==='svg'){save(blob,filename);return {filename,width:Number(match[1]),height:Number(match[2]),vector:true};}
 if(height>16000)throw Error('This selection is too tall for a safe PNG export. Choose vector SVG or a wider window.');
 progress('Rendering '+width.toLocaleString()+' × '+height.toLocaleString()+' pixels from vector tiles…');
 const url=URL.createObjectURL(blob),img=new Image();
 try{
  await new Promise((resolve,reject)=>{img.onload=resolve;img.onerror=()=>reject(Error('Could not decode the vector export'));img.src=url;});
  const canvas=document.createElement('canvas');canvas.width=width;canvas.height=height;
  try{
   const ctx=canvas.getContext('2d');if(!ctx)throw Error('This browser cannot allocate the export canvas; choose SVG.');
   ctx.fillStyle='#ffffff';ctx.fillRect(0,0,width,height);ctx.drawImage(img,0,0,width,height);
   progress('Encoding the high-resolution PNG…');
   const png=await new Promise(resolve=>canvas.toBlob(resolve,'image/png'));
   if(!png)throw Error('The browser could not encode this PNG; choose 8000 pixels or vector SVG.');
   save(png,filename);
  }finally{canvas.width=1;canvas.height=1;}
 }finally{URL.revokeObjectURL(url);img.src='';}
 return {filename,width,height,vector:false};
}
const api={svg,download,color};scope.COMET_VECTOR_EXPORT=api;if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
