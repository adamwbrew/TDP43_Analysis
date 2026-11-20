"""Extract full-precision PLA attributes, bound to the unchanged object cache.

This adds measurements to existing object identities. It never changes their
coordinates, section assignments, transforms, bins or coverage convention.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import csv
import json
import math
import tempfile
import shutil

import numpy as np

from .core import FixedTransform
from .manifest import sha256_file
from .exploratory import PLA_CLASS, CHAT_CLASS


AREA_COLUMN = 'Area (µm²)'
INTENSITY_COLUMN = 'Average Intensity'
MARKERS = [{'id':'chat', 'label':'ChAT', 'source_column':'ChAt-50 - FITC_E1 present'}]


def nearest_neighbor_distances(points):
    """Exact within-section Euclidean spacing, retaining every midpoint proxy.

    The second returned neighbour excludes the query point itself. Distinct
    objects sharing a coordinate correctly have zero spacing. No section edge
    correction, physical calibration, filtering or cross-section pooling occurs.
    """
    from scipy.spatial import cKDTree
    xy=np.column_stack([points['x'],points['y']]).astype(float)
    if not np.isfinite(xy).all():
        raise ValueError('Nearest-neighbor coordinates must all be finite')
    if len(xy)<2:
        return [None]*len(xy)
    distances=cKDTree(xy).query(xy,k=2,eps=0,p=2,workers=1)[0][:,1]
    return distances.tolist()


def spatial_feature_policy():
    return {'field':'nearest_neighbor_distance','method':'scipy.spatial.cKDTree.query',
            'k':2,'eps':0,'p':2,'workers':1,'exclude_self':True,
            'population':'All PLA midpoint proxies within the same physical section',
            'units':'exported coordinate units; physical calibration unverified',
            'duplicate_coordinates':'Distinct objects at identical positions have zero distance',
            'singleton_section':'Undefined distance', 'edge_correction':False,
            'limitations':'Descriptive detected-object spacing; affected by detection density and unobserved objects outside the exported section. Not a calibrated cell distance or a point-process inference.'}


def point_order_hash(points):
    """Fingerprint identities and exact ordered coordinates without resampling."""
    values = {key:points[key] for key in ('object_id','source_row','x','y','native_x','native_y')}
    return sha256(json.dumps(values,allow_nan=False,separators=(',',':')).encode()).hexdigest()


def feature_number(value):
    """Keep valid exported nonnegative measurements; unavailable values stay null."""
    try:
        number=float(value)
    except (ValueError,TypeError):
        return None
    return number if math.isfinite(number) and number>=0 else None


def extract_section_features(specification, points, base_dir):
    source=specification['source']
    path=Path(source['path'])
    if not path.is_absolute(): path=Path(base_dir)/path
    expected=source['sha256']
    if sha256_file(path)!=expected:
        raise ValueError('Raw source SHA-256 mismatch: '+str(path))
    if source['sha256']!=points['source_sha256'] or specification['section_id']!=points['section_id']:
        raise ValueError('Point cache and raw source identity disagree')
    record={'section_id':specification['section_id'], 'source_sha256':expected,
            'point_order_sha256':point_order_hash(points),
            'area_um2':[], 'intensity':[], 'markers':{marker['id']:[] for marker in MARKERS}}
    native=[];index=0;counts={PLA_CLASS:0,CHAT_CLASS:0};invalid={'area_um2':0,'intensity':0,'chat':0}
    with path.open(encoding='utf-8-sig',newline='') as handle:
        reader=csv.DictReader(handle)
        required={'Object Id','Object Type',AREA_COLUMN,INTENSITY_COLUMN,'XMin','XMax','YMin','YMax',
                  *(marker['source_column'] for marker in MARKERS)}
        if not reader.fieldnames or len(reader.fieldnames)!=len(set(reader.fieldnames)) or not required.issubset(reader.fieldnames):
            raise ValueError('Required PLA attribute fields are absent or duplicated')
        for row_number,row in enumerate(reader,2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError('Malformed CSV row '+str(row_number))
            kind=row['Object Type']
            if kind not in counts: raise ValueError('Unrecognized object class at row '+str(row_number))
            counts[kind]+=1
            if kind!=PLA_CLASS: continue
            if index>=len(points['object_id']) or row['Object Id']!=str(points['object_id'][index]) or row_number!=points['source_row'][index]:
                raise ValueError('PLA attribute/object identity or source-row order mismatch at row '+str(row_number))
            native.append([(float(row['XMin'])+float(row['XMax']))/2,
                           (float(row['YMin'])+float(row['YMax']))/2])
            for field,column in [('area_um2',AREA_COLUMN),('intensity',INTENSITY_COLUMN)]:
                value=feature_number(row[column]);record[field].append(value)
                invalid[field]+=value is None
            for marker in MARKERS:
                number=feature_number(row[marker['source_column']])
                value=int(number) if number in (0,1) else None
                record['markers'][marker['id']].append(value)
                invalid[marker['id']]+=value is None
            index+=1
    if index!=len(points['x']): raise ValueError('PLA feature extraction lost or added objects')
    native=np.asarray(native,dtype=float).reshape(-1,2)
    expected_native=np.column_stack([points['native_x'],points['native_y']])
    if not np.array_equal(native,expected_native): raise ValueError('Native midpoint cache mismatch')
    aligned=FixedTransform(specification['transform']['matrix']).points(native)
    if not np.array_equal(aligned,np.column_stack([points['x'],points['y']])):
        raise ValueError('Saved alignment/point cache mismatch; no coordinate changes permitted')
    if sha256_file(path)!=expected: raise ValueError('Raw source changed during feature extraction')
    record['point_count']=index
    record['invalid_attribute_counts']=invalid
    record['source_class_counts']={'pla':counts[PLA_CLASS],'chat':counts[CHAT_CLASS]}
    record['nearest_neighbor_distance']=nearest_neighbor_distances(points)
    return record


def locate_saved_counts(root):
    pointer=Path(root)/'outputs/exploratory_multiresolution/latest_run.json'
    data=json.loads(pointer.read_text())
    recorded=Path(data['run_directory'])
    local=pointer.parent/recorded.name/data.get('payload_file','view_payload.json')
    return local if local.is_file() else recorded/data.get('payload_file','view_payload.json')


def build_feature_cache(root):
    """Read the twelve selected CSVs; save a separate immutable attribute cache."""
    root=Path(root)
    source_path=locate_saved_counts(root)
    source_bytes=source_path.read_bytes();source=json.loads(source_bytes)
    if not all(source['validation'].get(key) is True for key in
               ('count_conservation_all_resolutions','full_pla_point_count_matches_raw','fixed_transforms_unchanged')):
        raise ValueError('Raw-count predecessor validation is incomplete')
    manifest_path=root/'metadata/analysis_manifest.json'
    manifest_bytes=manifest_path.read_bytes();manifest=json.loads(manifest_bytes)
    points={p['section_id']:p for p in source['pla_points']}
    if len(points)!=12 or len(manifest['sections'])!=12 or len({s['section_id']for s in manifest['sections']})!=12:
        raise ValueError('Exactly twelve distinct selected completed sections required')
    output=root/'outputs/measurement_features';output.mkdir(parents=True,exist_ok=True)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    source_hash=sha256(source_bytes).hexdigest()
    with tempfile.TemporaryDirectory(prefix='.features-',dir=output) as temporary:
        stage=Path(temporary)
        records=[extract_section_features(s,points[s['section_id']],manifest_path.parent) for s in manifest['sections']]
        if sum(r['point_count']for r in records)!=source['validation']['full_pla_point_count']:
            raise ValueError('PLA feature count does not match the full object cache')
        totals={key:sum(r['source_class_counts'][key]for r in records) for key in ('pla','chat')}
        if totals!={'pla':source['validation']['source_totals']['pla_objects'],
                    'chat':source['validation']['source_totals']['chat_objects']}:
            raise ValueError('Source class counts changed from the saved raw count run')
        if source_path.read_bytes()!=source_bytes or manifest_path.read_bytes()!=manifest_bytes:
            raise RuntimeError('Input metadata changed during extraction')
        validation={'status':'completed', 'source_hashes_verified_before_after':True,
                    'all_pla_object_ids_and_source_rows_matched':True,'native_and_aligned_coordinates_unchanged':True,
                    'all_selected_pla_objects_retained':True,'point_count':sum(r['point_count']for r in records),
                    'source_class_counts':totals,'raw_sources_modified':False,
                    'invalid_attribute_counts':{key:sum(r['invalid_attribute_counts'][key]for r in records)
                                                for key in ('area_um2','intensity','chat')}}
        payload={'schema_version':'comet-measurement-features-v1','default_area_cutoff':0.1,
                 'available_markers':MARKERS,'sections':records,'validation':validation,
                 'source_count_payload':str(source_path),'source_count_payload_sha256':source_hash,
                 'manifest_sha256':sha256(manifest_bytes).hexdigest(),
                 'attribute_columns':{'area_um2':AREA_COLUMN,'intensity':INTENSITY_COLUMN},
                 'spatial_features':spatial_feature_policy(),
                 'units':{'area_um2':'µm² as labeled in the export; calibration not independently verified',
                          'intensity':'exported intensity units; physical/normalization scale undocumented'},
                 'invalid_value_policy':'Nonfinite, negative, absent or malformed measurements remain null. Affected dependent bin metrics are undefined; no silent object exclusion.',
                 'source_code_sha256':sha256_file(Path(__file__)),
                 'generated_utc':datetime.now(timezone.utc).isoformat()}
        (stage/'features.json').write_text(json.dumps(payload,separators=(',',':'),allow_nan=False))
        (stage/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
        destination=output/(stamp+'_'+source_hash[:12]);shutil.move(str(stage),str(destination))
    pointer={'run_directory':str(destination),'payload_file':'features.json','schema_version':payload['schema_version'],
             'payload_sha256':sha256_file(destination/'features.json'),'point_count':validation['point_count']}
    (output/'latest_run.json').write_text(json.dumps(pointer,indent=2)+'\n')
    return destination


def load_feature_cache(root, points):
    """Validate the portable cached attributes before embedding them in the app."""
    root=Path(root);pointer=root/'outputs/measurement_features/latest_run.json'
    if not pointer.is_file(): return {}
    latest=json.loads(pointer.read_text());recorded=Path(latest['run_directory'])
    local=pointer.parent/recorded.name/latest.get('payload_file','features.json')
    path=local if local.is_file() else recorded/latest.get('payload_file','features.json')
    if sha256_file(path)!=latest['payload_sha256']: raise ValueError('PLA attribute cache hash mismatch')
    data=json.loads(path.read_text())
    if data.get('schema_version')!='comet-measurement-features-v1': raise ValueError('Unknown attribute-cache schema')
    by_section={p['section_id']:p for p in points}
    if len(data['sections'])!=len(by_section): raise ValueError('Attribute/coordinate cohort mismatch')
    for record in data['sections']:
        p=by_section[record['section_id']];n=len(p['x'])
        if record['source_sha256']!=p['source_sha256'] or record['point_order_sha256']!=point_order_hash(p):
            raise ValueError('Attribute cache no longer matches ordered source objects')
        if any(len(a)!=n for a in [record['area_um2'],record['intensity'],*record['markers'].values()]):
            raise ValueError('Attribute vector length mismatch')
        if 'nearest_neighbor_distance' in record:
            distances=record['nearest_neighbor_distance']
            if len(distances)!=n or any(v is not None and (isinstance(v,(bool,np.bool_)) or not isinstance(v,(float,int)) or not math.isfinite(v) or v<0) for v in distances):
                raise ValueError('Invalid nearest-neighbor distance vector')
    if not all(data['validation'].get(k) is True for k in
               ('source_hashes_verified_before_after','all_pla_object_ids_and_source_rows_matched',
                'native_and_aligned_coordinates_unchanged','all_selected_pla_objects_retained')):
        raise ValueError('Attribute cache validation incomplete')
    return data


def ensure_spatial_feature_cache(root, points):
    """Extend a validated old cache immutably, without rereading or changing CSVs."""
    root=Path(root)
    data=load_feature_cache(root,points)
    if not data or all('nearest_neighbor_distance' in s for s in data['sections']):
        return data
    pointer_path=root/'outputs/measurement_features/latest_run.json'
    previous=json.loads(pointer_path.read_text())
    point_map={p['section_id']:p for p in points}
    for section in data['sections']:
        section['nearest_neighbor_distance']=nearest_neighbor_distances(point_map[section['section_id']])
    data['spatial_features']=spatial_feature_policy()
    data['predecessor_feature_payload_sha256']=previous['payload_sha256']
    data['spatial_extension_utc']=datetime.now(timezone.utc).isoformat()
    data['spatial_extension_source_code_sha256']=sha256_file(Path(__file__))
    data['validation']['within_section_nearest_neighbors_exact']=True
    data['validation']['spatial_extension_coordinates_unchanged']=True
    output=pointer_path.parent
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    with tempfile.TemporaryDirectory(prefix='.spatial-features-',dir=output) as temporary:
        stage=Path(temporary)
        (stage/'features.json').write_text(json.dumps(data,separators=(',',':'),allow_nan=False))
        (stage/'validation.json').write_text(json.dumps(data['validation'],indent=2)+'\n')
        destination=output/(stamp+'_'+data['source_count_payload_sha256'][:12])
        shutil.move(str(stage),str(destination))
    pointer={'run_directory':str(destination),'payload_file':'features.json',
             'schema_version':data['schema_version'],'payload_sha256':sha256_file(destination/'features.json'),
             'point_count':data['validation']['point_count']}
    pointer_path.write_text(json.dumps(pointer,indent=2)+'\n')
    return load_feature_cache(root,points)
