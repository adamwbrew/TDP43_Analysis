"""Frozen display replay from Bio_Data_Analysis, never a registration fitter.

The former outline renderer is retained to reproduce its inspection figure.
Its occupancy-derived outline is a DISPLAY PROXY, never a tissue-validity mask.
See outputs/comet_core/alignment_replay_validation.json for source hashes.
"""
import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt
ARMS = {"Hk1": "TDP43–HK1", "Pfkp": "TDP43–PFKP"}
ANIMAL_ORDER = ["21F", "23M", "24M", "22F", "21M", "22M"]
ANIMAL_COLORS = dict(zip(ANIMAL_ORDER, ["#0072B2", "#009E73", "#7C52A1", "#D55E00", "#E69F00", "#CC79A7"]))
INK = "#173447"

def boundary_points(grid):
    occupied = grid['n_all'] > 0
    # One-bin closing connects small sampling gaps; never fill large cavities.
    mask = ndi.binary_closing(np.pad(occupied, 2), iterations=1)[2:-2, 2:-2]
    labels, _ = ndi.label(mask)
    sizes = np.bincount(labels.ravel()); sizes[0] = 0
    mask = labels == sizes.argmax() if sizes.max() else occupied
    boundary = mask & ~ndi.binary_erosion(mask)
    y, x = np.where(boundary)
    return np.column_stack(((grid['x_edges'][x] + grid['x_edges'][x + 1]) / 2,
                            (grid['y_edges'][y] + grid['y_edges'][y + 1]) / 2))

def transform_xy(xy,centroid,orientation='none'):
    """Reflect about native origin, then translate the reflected landmark."""
    if orientation not in ('none','horizontal','vertical','both'):
        raise ValueError('Only none, horizontal, vertical, both allowed')
    signs=np.array([-1 if orientation in ('horizontal','both') else 1,
                    -1 if orientation in ('vertical','both') else 1])
    oriented=np.asarray(xy,float)*signs
    center=np.asarray(centroid,float)*signs
    return oriented,oriented-center

def style():
    plt.rcParams.update({'figure.facecolor':'white','axes.facecolor':'white','axes.edgecolor':'#bccbd1',
                         'axes.labelcolor':INK,'text.color':INK,'xtick.color':INK,'ytick.color':INK,
                         'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':12,
                         'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False,
                         'savefig.facecolor':'white','svg.fonttype':'none','figure.dpi':110})

def alignment_figure(geometry, proposals):
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 3, figsize=(17, 12))
    for row, arm in enumerate(ARMS.values()):
        part = [p for p in proposals if p['pla_arm'] == arm]
        for col, mode in enumerate(['Native image coordinates', 'Cavity-centered only', 'Cavity + internal cue + discrete flip']):
            ax = axes[row, col]
            for p in part:
                points = boundary_points(geometry[p['job']])
                if col:
                    points = transform_xy(points, p['center'], p['flip'] if col == 2 else 'none')[1]
                ax.scatter(points[:,0], points[:,1], s=2, alpha=.5, color=ANIMAL_COLORS[p['animal_id']], label=p['animal_id'])
            ax.set_title(f'{arm}\n{mode}', fontsize=12)
            ax.set_aspect('equal'); ax.invert_yaxis(); ax.set_xlabel('x · export units'); ax.set_ylabel('y · export units')
            if col: ax.plot(0,0,'k+',ms=13,mew=2)
            if row == 0 and col == 0: ax.legend(ncol=3, fontsize=9, markerscale=3, loc='upper center')
    fig.suptitle('Align internal features first; keep missing tissue missing', fontsize=21, fontweight='bold', y=.99)
    fig.text(.05,.015,'All 12 sections have inspectable proposals. Cross = cavity anchor. Flips are geometric suggestions, not anatomical approvals.\nCropped edges do not move the anchor; remaining shape differences may reflect section level, tissue loss or imperfect landmarks.', fontsize=11)
    fig.tight_layout(rect=(0,.065,1,.95), h_pad=3.0)
    return fig
