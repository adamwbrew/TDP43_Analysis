/* Scientific plot lifecycle: measurable initialization, loaded previews and finite GL use.
 * No measurements, coordinates, matrices or colour values are recalculated here. */
(function (scope) {
'use strict';
function createPlotLifecycle(env) {
 const doc=env.document, P=env.Plotly, records=new Map(), pending=new Set(), stages=new Map();
 const original={newPlot:P.newPlot.bind(P),react:P.react.bind(P),relayout:P.relayout.bind(P),purge:P.purge.bind(P),resize:P.Plots.resize.bind(P.Plots)};
 let installed=false, warming=false, booted=false, work=Promise.resolve(), errors=[], observed=null;
 const frame=()=>new Promise(resolve=>(env.requestAnimationFrame||((f)=>env.setTimeout(f,0)))(resolve));
 const frames=async()=>{await frame();await frame();};
 const target=v=>typeof v==='string'?doc.getElementById(v):v;
 const inMain=el=>!!el?.closest?.('main');
 const panelOf=el=>el?.closest?.('[role="tabpanel"]');
 const isVisible=el=>!!el?.isConnected&&!el.closest?.('[hidden]')&&!panelOf(el)?.dataset?.cometStaging;
 function track(promise){const p=Promise.resolve(promise);pending.add(p);p.then(()=>pending.delete(p),error=>{pending.delete(p);errors.push(String(error?.message||error));status('A plot could not finish loading. Reload the viewer to retry.','error');});return p;}
 function status(message,state){const el=doc.getElementById('plot-readiness');if(el){el.textContent=message;el.dataset.state=state;el.setAttribute('aria-busy',state==='loading'?'true':'false');}}
 function mainWidth(){const main=doc.querySelector('main'),rect=main?.getBoundingClientRect(),css=main&&env.getComputedStyle?env.getComputedStyle(main):{};return Math.max(280,(rect?.width||env.innerWidth||1200)-parseFloat(css.paddingLeft||0)-parseFloat(css.paddingRight||0));}
 async function withPanel(name,callback){
  const panel=typeof name==='string'?doc.getElementById('panel-'+name):name;
  if(!panel||(!panel.hidden&&!stages.has(panel)))return callback();
  let stage=stages.get(panel);
  if(!stage){stage={n:0,style:panel.getAttribute('style'),hidden:panel.hidden};stages.set(panel,stage);panel.dataset.cometStaging='true';panel.hidden=false;panel.style.cssText+=';position:absolute;left:-30000px;top:0;visibility:hidden;pointer-events:none;width:'+mainWidth()+'px;';}
  stage.n++;
  try{await frames();return await callback();}
  finally{if(--stage.n===0){delete panel.dataset.cometStaging;if(stage.style===null)panel.removeAttribute('style');else panel.setAttribute('style',stage.style);const tab=doc.getElementById(panel.getAttribute('aria-labelledby'));panel.hidden=tab?tab.getAttribute('aria-selected')!=='true':stage.hidden;stages.delete(panel);}}
 }
 function dimensions(el){const r=el.getBoundingClientRect();if(!(r.width>0&&r.height>0))throw Error('Plot '+(el.id||'(unnamed)')+' has no measurable drawing area');return {width:Math.max(1,Math.round(r.width)),height:Math.max(1,Math.round(r.height))};}
 function axisRanges(layout){const out={};for(const key of Object.keys(layout||{}))if(/^[xy]axis\d*$/.test(key)&&Array.isArray(layout[key]?.range))out[key]=layout[key].range.slice();return out;}
 function saveEvents(r){const el=r.el;if(el.__cometEventsWrapped||typeof el.on!=='function')return;el.__cometEventsWrapped=true;const on=el.on,remove=el.removeAllListeners;
  el.on=function(name,fn){if(!r.restoring){if(!r.events.has(name))r.events.set(name,[]);if(!r.events.get(name).includes(fn))r.events.get(name).push(fn);}return on.call(this,name,fn);};
  if(remove)el.removeAllListeners=function(name){if(!r.restoring){if(name)r.events.delete(name);else r.events.clear();}return remove.call(this,name);};
 }
 async function fit(r,initial){if(r.suspended||!r.el.isConnected||!r.el.data||!r.el.layout)return;const dims=dimensions(r.el),update={width:dims.width,height:dims.height,autosize:false};
  const ranges=initial?r.ranges:axisRanges(r.el.layout||r.layout);for(const [axis,value]of Object.entries(ranges)){update[axis+'.range']=value.slice();update[axis+'.autorange']=false;}
  r.fitting=true;try{await original.relayout(r.el,update);}finally{r.fitting=false;}r.lastWidth=dims.width;r.lastHeight=dims.height;
 }
 function record(el){let r=records.get(el);if(!r){r={el,events:new Map(),chain:Promise.resolve(),suspended:false,preview:null,shell:null,ranges:{},version:0};records.set(el,r);observed?.observe(el);}return r;}
 function render(kind,value,data,layout,config){const el=target(value);if(!inMain(el))return original[kind](value,data,layout,config);const r=record(el),version=++r.version;
  r.data=data;r.layout=layout||{};r.config=config||{};r.ranges=axisRanges(layout);r.suspended=false;
  const job=r.chain.catch(()=>{}).then(()=>withPanel(panelOf(el),async()=>{if(!el.isConnected||version!==r.version)return el;const dims=dimensions(el),next={...(layout||{}),...dims,autosize:false};
   if(kind==='newPlot'){r.events.clear();delete el.__cometEventsWrapped;}
   await original[kind](el,data,next,config);if(!el.isConnected||version!==r.version)return el;r.suspended=false;saveEvents(r);await frames();await fit(r,true);if(r.preview)r.preview.hidden=true;return el;
  }));r.chain=job;return track(job);
 }
 function removePreview(r){if(r.preview)r.preview.remove();r.preview=null;}
 function purge(el,forget=true){const r=records.get(el);if(r){r.version++;observed?.unobserve(el);removePreview(r);if(forget)records.delete(el);}original.purge(el);}
 function purgeTree(root){if(!root?.contains)return;for(const el of [...records.keys()])if(el!==root&&root.contains(el))purge(el);}
 async function suspend(r){if(r.hydrationPromise)await r.hydrationPromise;if(r.suspended||!r.el.isConnected||!r.el.data?.some(t=>/gl$|^surface$|^mesh3d$|^scatter3d$/.test(t.type||'')))return;
  const version=r.version;try{const url=await P.toImage(r.el,{format:'png',width:r.lastWidth,height:r.lastHeight,scale:1});if(version!==r.version||!r.el.isConnected)return;
   if(!r.shell){const shell=doc.createElement('div');shell.className='comet-plot-shell';r.el.parentNode.insertBefore(shell,r.el);shell.appendChild(r.el);r.shell=shell;}
   if(!r.preview){r.preview=doc.createElement('img');r.preview.className='comet-loaded-preview';r.preview.alt='Loaded scientific plot preview; interactive controls become available when this view opens.';r.preview.setAttribute('aria-hidden','true');r.shell.appendChild(r.preview);}
   r.preview.src=url;r.preview.hidden=false;if(r.preview.decode)await r.preview.decode();r.data=r.el.data;r.layout=r.el.layout;r.ranges=axisRanges(r.el.layout);r.suspended=true;r.restoring=true;try{original.purge(r.el);}finally{r.restoring=false;}delete r.el.__cometEventsWrapped;
  }catch(error){errors.push('Preview '+r.el.id+': '+String(error?.message||error));}
 }
 function hydrate(r){if(r.hydrationPromise)return r.hydrationPromise;if(!r.suspended||!r.el.isConnected)return Promise.resolve();
  const version=r.version,job=r.chain.catch(()=>{}).then(()=>withPanel(panelOf(r.el),async()=>{if(!r.el.isConnected||version!==r.version)return;r.suspended=false;
   await original.newPlot(r.el,r.data,{...r.layout,...dimensions(r.el),autosize:false},r.config);saveEvents(r);r.restoring=true;try{for(const [name,callbacks]of r.events)for(const callback of callbacks)r.el.on(name,callback);}finally{r.restoring=false;}await frames();await fit(r,true);if(r.preview)r.preview.hidden=true;
  }));r.chain=job;r.hydrationPromise=job;job.then(()=>{r.hydrationPromise=null;},()=>{r.hydrationPromise=null;});return job;
 }
 async function whenIdle(){for(let pass=0;pass<30;pass++){const batch=[...pending];if(batch.length)await Promise.allSettled(batch);await frames();if(!pending.size)return;}throw Error('Plots did not reach a settled state');}
 async function imagesReady(){const images=[...doc.querySelectorAll('img[src]')];await Promise.all(images.map(image=>image.decode?image.decode().catch(()=>{}):image.complete?Promise.resolve():new Promise(resolve=>{image.addEventListener('load',resolve,{once:true});image.addEventListener('error',resolve,{once:true});})));}
 async function activate(){const active=doc.querySelector('[role="tabpanel"]:not([hidden])');if(!active)return;
  await whenIdle();for(const r of records.values())if(r.el.isConnected&&panelOf(r.el)!==active)await suspend(r);
  await withPanel(active,async()=>{for(const r of records.values())if(r.el.isConnected&&panelOf(r.el)===active){await hydrate(r);if(r.el.data)await fit(r,false);}});
 }
 async function boot(){if(booted)return;booted=true;warming=true;status('Loading every 2D view…','loading');
  try{if(doc.fonts?.ready)await doc.fonts.ready;await imagesReady();await whenIdle();const app=env.COMET_CORE_EXPLORER;
   if(app){for(const [name,render]of [['alignment',app.renderAlignment],['coverage',app.renderCoverage]]){
    for(const r of records.values())await suspend(r);
    await withPanel(name,async()=>{render();await app.alignmentReady;await whenIdle();});app.markViewLoaded?.(name);
   }}
   await imagesReady();warming=false;await activate();await whenIdle();status(errors.length?'Views loaded; '+errors.length+' optional preview warning(s).':'All 2D views loaded · ready to inspect','ready');
   doc.dispatchEvent(new env.CustomEvent('comet:plotsready',{detail:{plots:records.size,warnings:errors.slice()}}));
  }catch(error){warming=false;errors.push(String(error?.message||error));status('A view could not finish loading: '+String(error?.message||error),'error');throw error;}
 }
 function install(){if(installed)return api;installed=true;
  P.newPlot=(...args)=>render('newPlot',...args);P.react=(...args)=>render('react',...args);
  P.purge=value=>{const el=target(value);if(el&&records.has(el))purge(el);else original.purge(value);};
  P.Plots.resize=value=>{const el=target(value),r=records.get(el);if(!r)return original.resize(value);if(!isVisible(el))return Promise.resolve();return track(r.chain.catch(()=>{}).then(()=>hydrate(r)).then(()=>fit(r,false)));};
  if(env.Element){const descriptor=Object.getOwnPropertyDescriptor(env.Element.prototype,'innerHTML');if(descriptor?.set&&descriptor.configurable)Object.defineProperty(env.Element.prototype,'innerHTML',{...descriptor,set(value){if(inMain(this))purgeTree(this);descriptor.set.call(this,value);}});}
  if(env.ResizeObserver){observed=new env.ResizeObserver(entries=>{for(const entry of entries){const r=records.get(entry.target);if(!r||r.fitting||r.suspended||!isVisible(r.el))continue;const rect=r.el.getBoundingClientRect();if(rect.width>0&&rect.height>0&&(Math.round(rect.width)!==r.lastWidth||Math.round(rect.height)!==r.lastHeight))track(r.chain.catch(()=>{}).then(()=>fit(r,false)));}});for(const r of records.values())observed.observe(r.el);}
  doc.addEventListener('comet:viewchange',()=>{if(!booted||warming)return;work=work.catch(()=>{}).then(activate);work.catch(error=>{errors.push(String(error?.message||error));});});
  const start=()=>{api.ready=boot();api.ready.catch(()=>{});};if(doc.readyState==='loading')doc.addEventListener('DOMContentLoaded',start,{once:true});else env.setTimeout(start,0);
  return api;
 }
 const api={install,withPanel,whenIdle,activate,boot,dimensions,purgeTree,records,errors,get pendingCount(){return pending.size;},ready:Promise.resolve()};return api;
}
if(typeof module==='object'&&module.exports)module.exports={createPlotLifecycle};
if(scope?.document&&scope.Plotly)scope.COMET_PLOT_LIFECYCLE=createPlotLifecycle(scope).install();
})(typeof window!=='undefined'?window:null);
