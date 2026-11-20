"""Exact metric-independent detected-object footprints, never tissue masks."""
from hashlib import sha256
import json
import numpy as np


def footprint_geometry(grid, footprint):
    """Merge collinear grid-edge segments while preserving every gap and hole."""
    mask=np.asarray(footprint,bool)
    xe,ye=np.asarray(grid['x_edges'],float),np.asarray(grid['y_edges'],float)
    if mask.shape!=(len(ye)-1,len(xe)-1) or any(not np.isfinite(e).all() or not (np.diff(e)>0).all() for e in (xe,ye)):
        raise ValueError('Footprint must match finite increasing recorded grid edges')
    x,y=[],[]
    def runs(row):
        padded=np.pad(row.astype(int),(1,1))
        return zip(np.flatnonzero(np.diff(padded)==1),np.flatnonzero(np.diff(padded)==-1))
    horizontal=np.diff(np.pad(mask.astype(int),((1,1),(0,0))),axis=0)!=0
    vertical=np.diff(np.pad(mask.astype(int),((0,0),(1,1))),axis=1)!=0
    for j,row in enumerate(horizontal):
        for start,end in runs(row):
            x.extend([float(xe[start]),float(xe[end]),None]);y.extend([float(ye[j]),float(ye[j]),None])
    for i,col in enumerate(vertical.T):
        for start,end in runs(col):
            x.extend([float(xe[i]),float(xe[i]),None]);y.extend([float(ye[start]),float(ye[end]),None])
    return {'grid':{'x_edges':xe.tolist(),'y_edges':ye.tolist()},'footprint':mask.tolist(),
            'x':x,'y':y,'occupied_bin_count':int(mask.sum()),'boundary_segments':len(x)//3,
            'source_bin_width':float(grid.get('bin_width_export_units',np.min(np.diff(xe)))),
            'label':'Observed-object footprint; not a tissue boundary',
            'tissue_coverage_verified':False,'holes_filled':False,'smoothing':False,
            'geometry_sha256':sha256(json.dumps({'x':xe.tolist(),'y':ye.tolist(),'mask':mask.tolist()},separators=(',',':')).encode()).hexdigest()}


def build_context_geometry(multiresolution):
    resolutions=multiresolution.get('resolutions',{})
    if not resolutions:return {}
    finest=resolutions[min(resolutions,key=int)]
    if not finest.get('grid') or not finest.get('arms'):return {}
    return {arm:footprint_geometry(finest['grid'],values['displayable']) for arm,values in finest['arms'].items() if 'displayable' in values}
