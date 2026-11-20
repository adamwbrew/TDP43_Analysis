"""Audit Python/browser calculations on every real 100-unit bin without recounting.

The selected immutable count/feature snapshots are read only. Node writes small
binary arrays to a temporary directory; Python checks full numerical arrays and
undefined masks, then saves a compact provenance/validation record.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse
import json
import shutil
import subprocess
import sys
import tempfile

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from comet_spatial.measurements import MEASUREMENTS, COMPARISONS, compute_measurement


def digest(path):
    h = sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def selected_path(root, family, default_name):
    pointer = root / 'outputs' / family / 'latest_run.json'
    value = json.loads(pointer.read_text())
    directory = Path(value['run_directory'])
    local = pointer.parent / directory.name
    if local.is_dir():
        directory = local
    return directory / value.get('payload_file', value.get('features_file', default_name))


def geometry_digest(data):
    geometry = {'points': data['pla_points'], 'resolutions': {}}
    for width, payload in data['resolutions'].items():
        geometry['resolutions'][width] = {
            'grid': payload['grid'],
            'sections': [{key: section[key] for key in ('section_id', 'fixed_transform', 'pla_counts', 'chat_counts', 'observed_support')}
                         for section in payload['sections']],
            'observed_n': {arm: {key: arrays[key] for key in ('homecage_observed_section_n', 'running_observed_section_n')}
                           for arm, arrays in payload['arms'].items()}}
    return sha256(json.dumps(geometry, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


NODE_PROGRAM = r'''
const fs=require('fs'),path=require('path');
const [payloadPath,featuresPath,enginePath,out]=process.argv.slice(2);
const all=JSON.parse(fs.readFileSync(payloadPath,'utf8'));
const features=JSON.parse(fs.readFileSync(featuresPath,'utf8'));
const M=require(enginePath),payload={...all.resolutions['100'],pla_points:all.pla_points};
const descriptors=M.MEASUREMENTS.map(m=>({measurement:m.id,cutoff:.1}));
descriptors.push({measurement:'large_pla_count',cutoff:.2});
function save(name,matrix,type='float'){
 const flat=matrix.flat(Infinity),values=type==='byte'?Uint8Array.from(flat,v=>v?1:0):Float64Array.from(flat,v=>v===null?NaN:v);
 fs.writeFileSync(path.join(out,name+'.bin'),Buffer.from(values.buffer,values.byteOffset,values.byteLength));
}
const index=[];
for(let i=0;i<descriptors.length;i++){
 const descriptor=descriptors[i],base='metric_'+i;
 for(const comparison of M.COMPARISONS){
  const result=M.calculate(payload,features,descriptor.measurement,{areaCutoff:descriptor.cutoff,marker:'chat',comparison:comparison.id});
  for(const arm of ['HK1','PFKP']){
   const values=result.arms[arm],prefix=base+'_'+arm;
   save(prefix+'_'+comparison.id,values.comparison_value);
   save(prefix+'_'+comparison.id+'_defined',values.displayable,'byte');
   if(comparison.id==='absolute_difference'){
    for(const key of ['homecage_mean','running_mean','homecage_valid_section_n','running_valid_section_n'])save(prefix+'_'+key,values[key]);
   }
  }
  if(comparison.id==='absolute_difference')for(let j=0;j<result.sections.length;j++){
   save(base+'_section_'+j,result.sections[j].values);
   save(base+'_section_'+j+'_defined',result.sections[j].defined,'byte');
  }
 }
 index.push(descriptor);
}
fs.writeFileSync(path.join(out,'index.json'),JSON.stringify(index));
console.log(JSON.stringify({measurements:descriptors.length,comparison_cases:descriptors.length*3,sections:payload.sections.length,grid:payload.grid.shape}));
'''


def validate(root=ROOT, output=None):
    root = Path(root)
    node = shutil.which('node')
    if not node:
        raise RuntimeError('Node.js is required for the independent browser-engine audit')
    payload_path = selected_path(root, 'section_means', 'view_payload.json')
    feature_path = selected_path(root, 'measurement_features', 'features.json')
    legacy_path = root / 'outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/view_payload.json'
    if not legacy_path.is_file():
        raise FileNotFoundError('Original published fixed-three snapshot is required for baseline preservation check')
    paths = [payload_path, feature_path, legacy_path,
             root / 'outputs/comet_core/alignment_snapshot.json',
             root / 'outputs/comet_core/figures/alignment_check_reference.png',
             root / 'scripts/comet_measurements.js', root / 'comet_spatial/measurements.py']
    before = {str(p.relative_to(root)): digest(p) for p in paths}
    all_data = json.loads(payload_path.read_text())
    features = json.loads(feature_path.read_text())
    legacy = json.loads(legacy_path.read_text())
    geometry_before = geometry_digest(all_data)
    baseline_checks = []
    for width, payload in all_data['resolutions'].items():
        result = compute_measurement({**payload, 'pla_points': all_data['pla_points']}, features, 'pla_count')
        for arm in ('HK1', 'PFKP'):
            for key in ('homecage_mean', 'running_mean', 'difference', 'displayable'):
                expected = np.asarray(legacy['resolutions'][width]['arms'][arm][key], dtype=bool if key == 'displayable' else float)
                actual = np.asarray(result['arms'][arm][key])
                if not np.array_equal(actual, expected, equal_nan=True):
                    raise AssertionError('Published PLA count baseline changed: '+width+'/'+arm+'/'+key)
        baseline_checks.append({'bin_width':int(width),'both_arms_mean_difference_eligibility_exactly_equal':True})
    payload = {**all_data['resolutions']['100'], 'pla_points': all_data['pla_points']}
    descriptors = [{'measurement': m['id'], 'cutoff': .1} for m in MEASUREMENTS]
    descriptors.append({'measurement': 'large_pla_count', 'cutoff': .2})
    atol = rtol = 1e-12
    records, arrays_checked, numbers_checked, global_maximum = [], 0, 0, 0.
    with tempfile.TemporaryDirectory(prefix='tdp43-engine-parity-') as temporary:
        directory = Path(temporary)
        program = directory / 'audit.cjs'
        program.write_text(NODE_PROGRAM)
        completed = subprocess.run([node,str(program),str(payload_path),str(feature_path),
                                    str(root/'scripts/comet_measurements.js'),str(directory)],
                                   text=True,capture_output=True,check=True,timeout=180)
        node_summary = json.loads(completed.stdout)
        for i, descriptor in enumerate(descriptors):
            for comparison in COMPARISONS:
                result = compute_measurement(payload,features,descriptor['measurement'],
                    area_cutoff=descriptor['cutoff'],comparison=comparison['id'])
                maximum, checked = 0., 0

                def check(name, expected, byte=False):
                    nonlocal arrays_checked,numbers_checked,maximum,checked
                    original = np.asarray(expected)
                    actual = np.fromfile(directory/(name+'.bin'),dtype=np.uint8 if byte else np.float64).reshape(original.shape)
                    if byte:
                        np.testing.assert_array_equal(actual.astype(bool), original)
                    else:
                        np.testing.assert_array_equal(np.isfinite(actual),np.isfinite(original))
                        np.testing.assert_allclose(actual,original,atol=atol,rtol=rtol,equal_nan=True)
                        good = np.isfinite(original)
                        if good.any():
                            maximum = max(maximum,float(np.max(np.abs(actual[good]-original[good]))))
                    checked += 1;arrays_checked += 1;numbers_checked += original.size

                base='metric_'+str(i)
                for arm in ('HK1','PFKP'):
                    arrays=result['arms'][arm];prefix=base+'_'+arm
                    check(prefix+'_'+comparison['id'],arrays['comparison_value'])
                    check(prefix+'_'+comparison['id']+'_defined',arrays['displayable'],True)
                    if comparison['id']=='absolute_difference':
                        for key in ('homecage_mean','running_mean','homecage_valid_section_n','running_valid_section_n'):
                            check(prefix+'_'+key,arrays[key])
                if comparison['id']=='absolute_difference':
                    for j,section in enumerate(result['sections']):
                        check(base+'_section_'+str(j),section['values'])
                        check(base+'_section_'+str(j)+'_defined',section['defined'],True)
                global_maximum=max(global_maximum,maximum)
                records.append({**descriptor,'comparison':comparison['id'],'arrays_checked':checked,
                                'maximum_absolute_error':maximum,'finite_and_undefined_masks_exact':True,'passed':True})
    after = {str(p.relative_to(root)): digest(p) for p in paths}
    if before != after or geometry_digest(all_data) != geometry_before:
        raise AssertionError('An immutable input or in-memory geometry/support changed during the audit')
    record={'recorded_utc':datetime.now(timezone.utc).isoformat(),'local_scientific_date':'2026-11-19',
        'status':'passed','raw_inputs_recounted':False,'point_objects':sum(len(p['x']) for p in all_data['pla_points']),
        'physical_sections':12,'bin_width_export_units':100,'bins_per_arm':60000,'measurement_variants':len(MEASUREMENTS)+1,
        'comparison_cases':len(records),'arrays_checked':arrays_checked,'scalar_entries_checked':numbers_checked,
        'absolute_tolerance':atol,'relative_tolerance':rtol,'maximum_absolute_error':global_maximum,
        'node_execution':node_summary,'all_finite_and_undefined_masks_exact':True,
        'published_pla_count_baselines':baseline_checks,'geometry_and_observed_support_sha256':geometry_before,
        'all_input_files_unchanged_before_after':True,'input_sha256':before,
        'validator_sha256':digest(Path(__file__)),'cases':records}
    output=Path(output) if output else root/'outputs/protocols/calculation_engine_parity_2026-11-19.json'
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(record,indent=2)+'\n')
    return record


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=validate(output=args.output)
    print(json.dumps({key:result[key] for key in ('status','comparison_cases','arrays_checked','scalar_entries_checked','maximum_absolute_error','all_input_files_unchanged_before_after')},indent=2))
