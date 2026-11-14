"""600-DPI scientific exports of the fixed-three means and exact differences."""
from pathlib import Path
from hashlib import sha256
import json
import os
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'tmp/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scripts.build_section_mean_maps import locate_run


def build(root=ROOT):
    root = Path(root)
    path = locate_run(root, 'section_means')
    data = json.loads(path.read_text())
    if data.get('fixed_section_denominator') != 3 or not data['validation']['all_mean_difference_checks_passed']:
        raise ValueError('Validated fixed-three mean run required')
    out = path.parent / 'figures'; out.mkdir(exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10, 'svg.fonttype':'none'})
    figures = []
    sequential = LinearSegmentedColormap.from_list('comet_mean',[(0,'#ffffff'),(.3,'#c1daed'),(.7,'#5896c4'),(1,'#174e79')])
    sequential.set_bad('#edf0f3')
    signed = LinearSegmentedColormap.from_list('comet_signed',[(0,'#2166ac'),(.5,'#ffffff'),(1,'#b2182b')])
    signed.set_bad('#edf0f3')

    def decorate(ax, grid):
        ax.set(xlim=(grid['x_edges'][0],grid['x_edges'][-1]), ylim=(grid['y_edges'][-1],grid['y_edges'][0]))
        ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values(): spine.set_visible(False)

    def header(fig, title, subtitle):
        fig.suptitle(title, x=.045, ha='left', y=.98, fontsize=20, weight='bold', color='#19354a')
        fig.text(.045,.928,subtitle,fontsize=10,color='#567183')
        fig.text(.045,.025,'All three sections per condition · empty section-bins = assumed zero · coverage uncertain\n'
                 'Unchanged saved alignment · midpoint proxies · exact bin counts · no smoothing, normalization or statistical tests',
                 fontsize=9,color='#567183',linespacing=1.6)

    def save(fig, identifier, title, caption):
        name = identifier+'.png'
        fig.savefig(out/name,dpi=600,bbox_inches='tight',facecolor='white')
        fig.savefig(out/(identifier+'.svg'),dpi=600,bbox_inches='tight',facecolor='white')
        plt.close(fig)
        from PIL import Image
        with Image.open(out/name) as im: dimensions=list(im.size)
        figures.append({'id':identifier,'path':'figures/'+name,'svg':'figures/'+identifier+'.svg',
                        'title':title,'caption':caption,'dpi':600,'pixel_dimensions':dimensions,
                        'sha256':sha256((out/name).read_bytes()).hexdigest()})

    for width in ('250','100'):
        p=data['resolutions'][width];grid=p['grid'];xe,ye=grid['x_edges'],grid['y_edges']
        limit=p['color_scale']['cmax']
        for cap, suffix in [(limit,''),(min(25.,limit),'_contrast')]:
            fig,axs=plt.subplots(1,2,figsize=(16,9))
            fig.subplots_adjust(left=.045,right=.88,top=.84,bottom=.13,wspace=.15)
            header(fig,'Running − Homecage · mean PLA count across all three sections',
                   f'TDP43–HK1 and TDP43–PFKP · {width}-unit bins · shared linear colours, −{cap:g} to +{cap:g}')
            clips=[]
            for ax,arm in zip(axs,('HK1','PFKP')):
                v=np.asarray(p['arms'][arm]['difference'],float)
                clipped=int((np.abs(v[np.isfinite(v)])>cap).sum());clips.append(f'{arm}: {clipped:,}')
                im=ax.pcolormesh(xe,ye,v,cmap=signed,vmin=-cap,vmax=cap,shading='flat',rasterized=True)
                decorate(ax,grid);ax.set_title('TDP43–'+arm,fontsize=14,pad=14)
            cax=fig.add_axes([.915,.24,.014,.47]);cb=fig.colorbar(im,cax=cax,extend='both' if suffix else 'neither')
            cb.set_label('Running − Homecage · mean raw PLA / bin')
            if suffix:fig.text(.045,.09,'Display contrast only: saturated bins '+', '.join(clips)+'. Exact uncapped values remain in tables and app hover.',fontsize=9,color='#946f22')
            save(fig,'section_mean_differences'+suffix+'_'+width,'Three-section differences · '+width+suffix.replace('_',' '),
                 'Fixed denominator three; blank outside all-six-section object-support union. Coverage uncertain. '+('Display range ±25; uncapped numerical values retained.' if suffix else 'Shared full symmetric linear range.'))
        vmax=max(np.nanmax(np.asarray(p['arms'][a][key],float)) for a in ('HK1','PFKP') for key in ('homecage_mean','running_mean'))
        for contrast in (False,True):
            mean_limit=min(25.,vmax) if contrast else vmax
            diff_limit=min(25.,limit) if contrast else limit
            fig,axs=plt.subplots(2,3,figsize=(20,15))
            fig.subplots_adjust(left=.045,right=.94,top=.86,bottom=.13,wspace=.23,hspace=.23)
            header(fig,'Condition averages and the difference they produce',f'{width}-unit bins · each condition is the sum of three section counts / 3 · '+
                   (f'DETAIL DISPLAY: means 0–{mean_limit:g}, differences ±{diff_limit:g}' if contrast else 'shared full linear ranges'))
            for row,arm in enumerate(('HK1','PFKP')):
                for col,(key,title) in enumerate([('homecage_mean','Homecage mean'),('running_mean','Running mean'),('difference','Running − Homecage')]):
                    arr=np.asarray(p['arms'][arm][key],float)
                    capped=int((np.abs(arr[np.isfinite(arr)])>(diff_limit if col==2 else mean_limit)).sum())
                    image=axs[row,col].pcolormesh(xe,ye,arr,cmap=signed if col==2 else sequential,
                        vmin=-diff_limit if col==2 else 0,vmax=diff_limit if col==2 else mean_limit,shading='flat',rasterized=True)
                    decorate(axs[row,col],grid);axs[row,col].set_title(f'TDP43–{arm} · {title}'+
                        (f'\n{capped:,} bins use saturated endpoint colours' if contrast else ''),fontsize=12,pad=12)
                    bar=fig.colorbar(image,ax=axs[row,col],fraction=.034,pad=.025,shrink=.8,
                                    extend=('both' if col==2 else 'max') if contrast else 'neither')
                    bar.set_label('Mean raw PLA / bin' if col<2 else 'Difference',fontsize=9)
            if contrast:fig.text(.045,.09,'Colour contrast only: exact uncapped values remain in matrices, tables and app hover. Full-range companion figures are retained.',fontsize=10,color='#946f22')
            save(fig,'section_means_and_difference_'+('contrast_' if contrast else '')+width,
                 'Condition means and differences · '+width+(' detail contrast' if contrast else ' full range'),
                 'Means share one sequential range across both conditions and both arms; differences share one symmetric range. '+
                 ('Endpoint saturation is labeled and counted; exact values unchanged. ' if contrast else '')+'No interpolation. Coverage uncertain.')
    result={'source_payload':str(path),'source_payload_sha256':sha256(path.read_bytes()).hexdigest(),
            'fixed_section_denominator':3,'empty_bin_policy':'zero','coverage_verified':False,'figures':figures}
    (path.parent/'detailed_figure_manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    print(json.dumps(build(),indent=2))
