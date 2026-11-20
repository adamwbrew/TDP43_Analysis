"""Save all default calculation functions and high-resolution example maps.

The input is the unchanged spatial count snapshot plus source-verified PLA
attributes. Object statistics are calculated per section, then section means
are compared; objects are never pooled as independent biological samples.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import argparse
import csv
import json
import os
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'tmp/matplotlib'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import PolyCollection, LineCollection
from matplotlib.colors import Normalize
from comet_spatial.measurements import compute_measurement, compare_conditions, MEASUREMENTS, COMPARISONS
from comet_spatial.measurement_features import ensure_spatial_feature_cache
from comet_spatial.context_geometry import build_context_geometry
from scripts.build_section_mean_maps import locate_run


COMPARISON_EXAMPLES=[('marker_associated_pla_count','absolute_difference'),
    ('mean_pla_area','absolute_difference'),('large_pla_fraction','absolute_difference'),
    ('pla_count','percent_change'),('pla_count','log2_fold_change'),
    ('section_pla_share','absolute_difference'),('marker_associated_pla_area_fraction','absolute_difference'),
    ('median_pla_intensity','absolute_difference'),('pla_area_iqr','absolute_difference'),
    ('pla_area_cv','absolute_difference'),('mean_pla_nearest_neighbor_distance','absolute_difference')]


def save_figure(payload,calculation,out,identifier,display_cap=None):
    """Exact tiles and shared signed linear colours; no spatial interpolation."""
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    cmap=LinearSegmentedColormap.from_list('comet_signed',[(0,'#2166ac'),(.5,'#ffffff'),(1,'#b2182b')])
    cmap.set_bad((0,0,0,0))
    fig,axs=plt.subplots(1,2,figsize=(16,9))
    fig.subplots_adjust(left=.045,right=.88,top=.81,bottom=.15,wspace=.17)
    m,c=calculation['measurement'],calculation['comparison']
    title=m['label']+' · '+c['label']
    fig.suptitle(title,x=.045,ha='left',y=.98,fontsize=18,weight='bold',color='#19354a')
    width=payload['grid']['bin_width_export_units']
    fig.text(.045,.925,f'{width}-unit bins · per-section measurement → equal means of defined sections → selected comparison',fontsize=10,color='#567183')
    scope=[]
    if m['needsCutoff']:scope.append(f'Large ≥ {calculation["area_cutoff"]:g} µm² (exported)')
    if m['needsMarker']:scope.append('Marker '+('ChAT' if calculation['marker']=='chat' else calculation['marker']))
    if not scope:scope.append('All PLA detections; no size or marker filter')
    fig.text(.045,.887,' · '.join(scope)+' · no pseudocounts',fontsize=10,color='#567183')
    full=calculation['color_scale']['cmax'];limit=full if display_cap is None else display_cap
    if not np.isfinite(limit) or limit<=0:raise ValueError('Display cap must be positive and finite')
    grid=payload['grid'];xe,ye=grid['x_edges'],grid['y_edges']
    panels=[]
    for ax,arm in zip(axs,('HK1','PFKP')):
        arrays=calculation['arms'][arm];z=np.asarray(arrays['comparison_value'],float)
        saturated=int((np.abs(z[np.isfinite(z)])>limit).sum())
        ax.set_facecolor('#e4e9ee')
        context=payload.get('context_geometry',{}).get(arm)
        if context:
            cg=context['grid'];mask=context['footprint'];strips=[]
            for j,row in enumerate(mask):
                padded=np.pad(np.asarray(row,int),(1,1));change=np.diff(padded)
                for start,end in zip(np.flatnonzero(change==1),np.flatnonzero(change==-1)):
                    strips.append([(cg['x_edges'][start],cg['y_edges'][j]),(cg['x_edges'][end],cg['y_edges'][j]),(cg['x_edges'][end],cg['y_edges'][j+1]),(cg['x_edges'][start],cg['y_edges'][j+1])])
            ax.add_collection(PolyCollection(strips,facecolors='#f0f3f6',edgecolors='none',antialiaseds=False))
        # Only defined cells become true vector polygons; no raster/image layer
        # is hidden inside the SVG, and undefined cells cannot cover the context.
        iy,ix=np.where(np.isfinite(z));x=np.asarray(xe);y=np.asarray(ye)
        verts=np.stack([np.column_stack([x[ix],y[iy]]),np.column_stack([x[ix+1],y[iy]]),np.column_stack([x[ix+1],y[iy+1]]),np.column_stack([x[ix],y[iy+1]])],axis=1)
        im=PolyCollection(verts,array=z[iy,ix],cmap=cmap,norm=Normalize(-limit,limit),edgecolors='none',antialiaseds=False,rasterized=False)
        ax.add_collection(im)
        if context:
            segments=[[(context['x'][i],context['y'][i]),(context['x'][i+1],context['y'][i+1])] for i in range(0,len(context['x']),3)]
            ax.add_collection(LineCollection(segments,colors='#778b9b',linewidths=.25,antialiaseds=True))
        ax.set(xlim=(xe[0],xe[-1]),ylim=(ye[-1],ye[0]));ax.set_aspect('equal');ax.set_xticks([]);ax.set_yticks([])
        for spine in ax.spines.values():spine.set_visible(False)
        ax.set_title(f'TDP43–{arm}\n{int(np.isfinite(z).sum()):,} defined comparison bins'+
                     (f' · {saturated:,} saturated' if display_cap is not None else ''),fontsize=12,pad=10)
        panels.append({'arm':arm,'defined_bins':int(np.isfinite(z).sum()),'saturated_bins':saturated})
    cax=fig.add_axes([.915,.25,.014,.43]);bar=fig.colorbar(im,cax=cax,extend='both' if display_cap else 'neither')
    if bar.solids is not None:bar.solids.set_rasterized(False)
    bar.set_label(c['units'])
    rule='Extensive measurements/section shares: average three sections, including assumed empty-bin zeros.' if m['empty_bin_rule']=='assumed_zero' else 'Object statistics/fractions: average defined section values; unavailable values remain missing.'
    fig.text(.045,.09,rule,fontsize=10,color='#567183')
    if display_cap is not None:
        fig.text(.045,.125,f'DETAIL COLOR DISPLAY: ±{limit:.6g} {c["units"]}. Saturation affects color only; full-range companion and exact arrays are retained.',fontsize=9,color='#946f22')
    fig.text(.045,.035,'Fixed pale footprint + thin outline = detected-object context, not a tissue boundary; coverage uncertain.\nUndefined statistics remain blank within this context. Exact units, valid-section N and full-range values are saved.',fontsize=9,color='#567183',linespacing=1.6)
    for ext in ('png','svg'):fig.savefig(out/(identifier+'.'+ext),dpi=600,bbox_inches='tight',facecolor='white')
    plt.close(fig)
    return {'id':identifier,'png':'figures/'+identifier+'.png','svg':'figures/'+identifier+'.svg','dpi':600,
            'measurement':m['id'],'comparison':c['id'],'units':c['units'],'color_limit':float(limit),
            'display_cap':display_cap,'panels':panels,'svg_all_grid_tiles_vector':True,'observed_object_outline':bool(payload.get('context_geometry'))}


def build(root=ROOT,*,area_cutoff=.1,marker='chat'):
    root=Path(root);base_path=locate_run(root,'section_means');base_bytes=base_path.read_bytes();base=json.loads(base_bytes)
    if base.get('fixed_section_denominator')!=3:raise ValueError('Current approved fixed-three spatial predecessor required')
    features=ensure_spatial_feature_cache(root,base['pla_points'])
    if not features:raise ValueError('PLA attributes missing; run scripts/build_measurement_features.py with original CSVs first')
    out=root/'outputs/calculation_functions';out.mkdir(parents=True,exist_ok=True)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');source_sha=sha256(base_bytes).hexdigest()
    run=out/(stamp+'_'+source_sha[:12]);run.mkdir()
    stats=[];figures=[];count_matches=True;partitions=True
    context_geometry=build_context_geometry(base)
    for width in ('1000','500','250','100'):
        payload={**base['resolutions'][width],'pla_points':base['pla_points'],'context_geometry':context_geometry}
        destination=run/('resolution_'+width);destination.mkdir()
        counts={}
        for measurement in MEASUREMENTS:
            identifier=measurement['id']
            calc=compute_measurement(payload,features,identifier,area_cutoff=area_cutoff,marker=marker)
            arrays={'section_ids':np.asarray([s['section_id'] for s in calc['sections']]),
                    'section_values':np.stack([s['values'] for s in calc['sections']]),
                    'section_defined':np.stack([s['defined'] for s in calc['sections']]),
                    'x_edges':np.asarray(payload['grid']['x_edges']),'y_edges':np.asarray(payload['grid']['y_edges'])}
            if identifier in ('pla_count','large_pla_count','small_pla_count','marker_associated_pla_count','marker_associated_large_pla_count'):
                counts[identifier]=arrays['section_values']
            for arm,a in calc['arms'].items():
                prefix=arm.lower()+'_'
                for key in ('homecage_mean','running_mean','homecage_valid_section_n','running_valid_section_n','eligibility'):
                    arrays[prefix+key]=a[key]
                for comparison in COMPARISONS:
                    cid=comparison['id'];comparison_result=compare_conditions(a['running_mean'],a['homecage_mean'],cid)
                    valid=a['eligibility']&comparison_result['defined']
                    value=np.where(valid,comparison_result['values'],np.nan)
                    reasons=np.asarray(comparison_result['missing_reason'],object).copy()
                    reasons[~a['eligibility']]='outside_display_domain'
                    arrays[prefix+cid]=value
                    arrays[prefix+cid+'_missing_reason']=np.asarray(np.where(reasons==None,'',reasons),dtype='U48')
                    eligible=a['eligibility'];finite=value[np.isfinite(value)]
                    row={'bin_width':int(width),'measurement':identifier,'comparison':cid,'arm':arm,
                         'units':calc['comparison']['units'] if cid=='absolute_difference' else comparison['units'],
                         'area_cutoff':area_cutoff,'marker':marker,'eligible_bins':int(eligible.sum()),
                         'defined_comparison_bins':int(valid.sum()),'undefined_eligible_bins':int((eligible&~valid).sum()),
                         'negative_bins':int((finite<0).sum()),'positive_bins':int((finite>0).sum()),'equal_bins':int((finite==0).sum()),
                         'minimum':float(finite.min()) if finite.size else None,'maximum':float(finite.max()) if finite.size else None,
                         'homecage_metric_N_0':int(((a['homecage_valid_section_n']==0)&eligible).sum()),
                         'running_metric_N_0':int(((a['running_valid_section_n']==0)&eligible).sum())}
                    stats.append(row)
                    if width=='100' and (identifier,cid) in COMPARISON_EXAMPLES:
                        example={**calc,'comparison':dict(comparison)}
                        if cid=='absolute_difference':example['comparison']['units']=calc['comparison']['units']
                        example['arms']={}
                        for aa,bb in calc['arms'].items():
                            v=compare_conditions(bb['running_mean'],bb['homecage_mean'],cid)
                            example['arms'][aa]={**bb,'comparison_value':np.where(bb['eligibility']&v['defined'],v['values'],np.nan)}
                        all_finite=np.concatenate([z['comparison_value'][np.isfinite(z['comparison_value'])]for z in example['arms'].values()])
                        example['color_scale']={'cmax':float(np.max(np.abs(all_finite))) if all_finite.size and np.max(np.abs(all_finite))>0 else 1}
                        # Render once per example, after both arm arrays have been assembled.
                        if arm=='PFKP':
                            figures.append(save_figure(payload,example,run/'figures',identifier+'_'+cid+'_100'))
                            nonzero=np.abs(all_finite[all_finite!=0])
                            detail_cap=float(np.quantile(nonzero,.95,method='linear')) if nonzero.size else 1.
                            detail=save_figure(payload,example,run/'figures',identifier+'_'+cid+'_detail_100',display_cap=detail_cap)
                            detail['display_cap_basis']='95th percentile of nonzero absolute comparison values, shared across both arms; display only'
                            figures.append(detail)
            np.savez_compressed(destination/(identifier+'.npz'),**arrays)
            if identifier=='pla_count':
                for arm,a in calc['arms'].items():
                    for key in ('homecage_mean','running_mean','difference'):
                        if not np.array_equal(a[key],np.asarray(payload['arms'][arm][key],float),equal_nan=True):
                            raise ValueError('Existing PLA count means/difference changed')
        if not np.array_equal(counts['large_pla_count']+counts['small_pla_count'],counts['pla_count']):
            raise ValueError('Large/small PLA partition does not conserve original counts')
        if not ((counts['marker_associated_large_pla_count']<=counts['large_pla_count']).all() and
                (counts['marker_associated_large_pla_count']<=counts['marker_associated_pla_count']).all()):
            raise ValueError('Marker-associated subsets do not match parent counts')
    if base_path.read_bytes()!=base_bytes:raise RuntimeError('Original spatial predecessor changed during measurement derivation')
    with (run/'summary.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(stats[0]));writer.writeheader();writer.writerows(stats)
    validation={'all_19_measurements_saved':True,'measurement_count':len(MEASUREMENTS),'all_3_comparisons_saved':True,'all_4_resolutions_saved':True,
                'existing_PLA_count_results_unchanged':count_matches,'large_small_partition_conserved':partitions,
                'full_pla_point_count':features['validation']['point_count'],'geometry_and_coverage_unchanged':True,
                'pseudocounts_added':False,'raw_features_reused':True,'raw_sources_modified':False,
                'source_spatial_payload_sha256':source_sha}
    report={'schema_version':'comet-calculation-functions-v1','area_cutoff':area_cutoff,'marker':marker,
            'measurements':MEASUREMENTS,'comparisons':COMPARISONS,'statistics':stats,'figures':figures,
            'validation':validation,'source_spatial_payload':str(base_path),'source_spatial_payload_sha256':source_sha,
            'feature_source_count_sha256':features['source_count_payload_sha256'],
            'coverage_policy':'Current approved mask-free display domain preserved; coverage uncertain',
            'averaging':'Equal means of defined section values. Counts/sums include assumed empty-bin zeros; object statistics and fractions do not.',
            'quantile_method':'type7_linear','context_geometry':{arm:{k:g[k] for k in ['geometry_sha256','source_bin_width','occupied_bin_count','boundary_segments','tissue_coverage_verified']} for arm,g in context_geometry.items()},
            'spatial_features':features.get('spatial_features',{}),'generated_utc':datetime.now(timezone.utc).isoformat(),
            'code_sha256':{p:sha256((root/p).read_bytes()).hexdigest() for p in
                           ['comet_spatial/measurements.py','scripts/comet_measurements.js','scripts/build_measurement_report.py']}}
    (run/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    (run/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    (out/'latest_run.json').write_text(json.dumps({'run_directory':str(run),'report_file':'report.json'},indent=2)+'\n')
    return run


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--area-cutoff',type=float,default=.1);parser.add_argument('--marker',default='chat')
    args=parser.parse_args();print(build(area_cutoff=args.area_cutoff,marker=args.marker))
