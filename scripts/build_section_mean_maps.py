"""Derive scientist-directed fixed-three means from validated, saved raw counts.

No CSV recount, point interpolation, registration fitting, or tissue mask is
performed. Earlier variable-denominator runs remain immutable historical inputs.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import copy
import csv
import json
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from comet_spatial.section_means import summarize_section_means


def locate_run(root, family):
    pointer = root / 'outputs' / family / 'latest_run.json'
    record = json.loads(pointer.read_text())
    recorded = Path(record['run_directory'])
    local = pointer.parent / recorded.name
    run = local if local.is_dir() else recorded
    return run / record.get('payload_file', 'view_payload.json')


def json_array(array):
    values = np.asarray(array)
    if values.dtype.kind == 'f':
        return [[float(v) if np.isfinite(v) else None for v in row] for row in values]
    return values.tolist()


def build(root=ROOT):
    root = Path(root)
    source = locate_run(root, 'exploratory_multiresolution')
    source_bytes = source.read_bytes()
    original = json.loads(source_bytes)
    for key in ('count_conservation_all_resolutions', 'full_pla_point_count_matches_raw',
                'hashes_verified_before_after_and_before_publication', 'fixed_transforms_unchanged'):
        if original['validation'].get(key) is not True:
            raise ValueError('Saved raw count validation incomplete: ' + key)
    authority_path = root / 'metadata/scientist_directed_mean_policy.json'
    authority = json.loads(authority_path.read_text())
    if authority.get('empty_bin_policy') != 'zero' or authority.get('sections_per_condition') != 3:
        raise ValueError('Explicit scientist-directed three-section zero policy required')
    output = copy.deepcopy(original)
    output['default_resolution'] = 100
    output['analysis_kind'] = 'fixed_three_section_mean_exploratory'
    output['fixed_section_denominator'] = 3
    output['authorization'] = authority
    output['limitations'] = [
        'Empty section-bins contribute assumed zero by the 14 November scientist-directed policy; tissue coverage is uncertain.',
        'The per-arm union of observed PLA/ChAT bins is a display domain, not a tissue boundary. Outside it, maps are blank.',
        'Positions are bounding-box midpoint proxies using the unchanged saved alignment.',
        'Raw count means are not tissue-area normalized; differences are descriptive, without inferential tests.',
        'Three animals per condition; the same six animals appear in both separate PLA arms.']
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    digest = sha256(source_bytes).hexdigest()
    run = root / 'outputs/section_means' / (stamp + '_' + digest[:12])
    run.mkdir(parents=True, exist_ok=False)
    validation = {'source_payload_sha256': digest, 'cached_raw_counts_reused': True,
                  'raw_csv_recomputed': False, 'fixed_section_denominator': 3,
                  'empty_bin_policy': 'zero', 'tissue_coverage_verified': False,
                  'all_mean_difference_checks_passed': True, 'all_counts_conserved': True,
                  'fixed_transforms_unchanged': True, 'resolutions': {}}
    for width, payload in output['resolutions'].items():
        summary = summarize_section_means(payload['sections'], empty_bin_policy='zero')
        payload['analysis_kind'] = output['analysis_kind']
        payload['fixed_section_denominator'] = 3
        payload['coverage_verified'] = False
        payload['limitations'] = output['limitations']
        payload['parameters'] = {**payload['parameters'],
            'empty_bin_policy': 'zero', 'sections_per_condition': 3,
            'mean_definition': 'Sum of raw PLA counts in all three sections / 3, including empty section-bins as assumed zero.',
            'missing_definition': 'Blank outside the per-arm union of observed PLA/ChAT support across all six sections. Coverage uncertain.',
            'n_meaning': 'Observed-object section count is diagnostic only; the mean denominator is always three.',
            'scientist_policy_record': 'metadata/scientist_directed_mean_policy.json'}
        all_differences = []
        dest = run / ('resolution_' + width); dest.mkdir()
        stats = {}
        for arm, values in summary['arms'].items():
            displayable = values['displayable']
            home = values['homecage_mean']; running = values['running_mean']
            # Independent identity checks, including bins with an entirely empty condition.
            groups = {c: [s for s in payload['sections'] if s['pla_type'] == arm and s['condition'] == c]
                      for c in ('Homecage', 'Running')}
            for c, mean in [('Homecage', home), ('Running', running)]:
                expected = sum(np.asarray(s['pla_counts'], dtype=np.int64) for s in groups[c]) / 3
                if not np.array_equal(mean, expected):
                    raise AssertionError('Fixed-three section mean failed')
            if not np.array_equal(values['difference'], running - home):
                raise AssertionError('Running minus Homecage check failed')
            n_h = values['homecage_observed_section_n']; n_r = values['running_observed_section_n']
            visible_difference = values['display_difference']
            old = payload['arms'][arm]
            payload['arms'][arm] = {**old, **{k: json_array(v) for k,v in values.items() if isinstance(v,np.ndarray)},
                'homecage_mean': json_array(np.where(displayable, home, np.nan)),
                'running_mean': json_array(np.where(displayable, running, np.nan)),
                'difference': json_array(visible_difference),
                'raw_arithmetic_difference': json_array(values['difference']),
                'homecage_n': json_array(n_h), 'running_n': json_array(n_r),
                'section_denominator': 3, 'section_ids': values['section_ids']}
            np.savez_compressed(dest / (arm.lower() + '_matrices.npz'),
                                **{k:v for k,v in values.items() if isinstance(v,np.ndarray)})
            xe, ye = payload['grid']['x_edges'], payload['grid']['y_edges']
            with (dest / (arm.lower() + '_bins.csv')).open('w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['arm','xmin','xmax','ymin','ymax','homecage_mean','running_mean','running_minus_homecage',
                                 'mean_denominator_each_condition','homecage_observed_N','running_observed_N',
                                 'homecage_assumed_zero_sections','running_assumed_zero_sections','display_domain','coverage_verified'])
                for iy, ix in np.ndindex(home.shape):
                    writer.writerow([arm,xe[ix],xe[ix+1],ye[iy],ye[iy+1],home[iy,ix],running[iy,ix],values['difference'][iy,ix],
                                     3,n_h[iy,ix],n_r[iy,ix],3-n_h[iy,ix],3-n_r[iy,ix],bool(displayable[iy,ix]),False])
            signed = values['difference'][displayable]
            all_differences.extend(signed.tolist())
            stats[arm] = {'displayable_bins': int(displayable.sum()), 'total_grid_bins': int(displayable.size),
                'negative_difference_bins': int((signed < 0).sum()), 'positive_difference_bins': int((signed > 0).sum()),
                'zero_difference_bins': int((signed == 0).sum()),
                'minimum_difference': float(signed.min()) if signed.size else None,
                'maximum_difference': float(signed.max()) if signed.size else None,
                'whole_condition_zero_bins_displayed': int((displayable & ((n_h==0) | (n_r==0))).sum()),
                'fixed_section_denominator': 3, 'tissue_coverage_verified': False}
        limit = max(1., float(np.max(np.abs(all_differences)))) if all_differences else 1.
        payload['color_scale'] = {**payload['color_scale'], 'cmin': -float(limit), 'cmax': float(limit),
            'label': 'Mean raw PLA count / three sections: Running − Homecage',
            'missing_color': '#e4e9ee'}
        payload['statistics'] = stats
        output['statistics_by_resolution'][width] = stats
        validation['resolutions'][width] = stats
        source_validation = copy.deepcopy(payload['validation'])
        payload['validation'] = {k:v for k,v in source_validation.items()
                                 if k not in ('baseline_1000_comparison', 'generated_utc', 'displayable_bins_by_arm')}
        payload['validation'].update(status='completed_fixed_three_section_means',
            source_count_validation=source_validation,
            fixed_section_denominator=3, empty_bin_policy='zero',
            tissue_coverage_verified=False, all_mean_difference_checks_passed=True,
            displayable_bins_by_arm={arm:s['displayable_bins'] for arm,s in stats.items()},
            generated_utc=datetime.now(timezone.utc).isoformat())
    if source.read_bytes() != source_bytes:
        raise RuntimeError('Historical count payload changed during derivation')
    output['parameters'] = {**output.get('parameters', {}), 'mean_policy': authority}
    inherited = {k:v for k,v in original['validation'].items()
                 if k not in ('baseline_1000_comparison', 'generated_utc')}
    output['validation'] = {**inherited, **validation}
    output['validation']['status'] = 'completed_fixed_three_section_means'
    output['validation']['source_count_validation'] = original['validation']
    output['validation']['generated_utc'] = datetime.now(timezone.utc).isoformat()
    (run / 'view_payload.json').write_text(json.dumps(output, allow_nan=False, separators=(',', ':')))
    (run / 'source_record.json').write_text(json.dumps({'path': str(source), 'sha256': digest,
        'scientist_policy': authority, 'policy_sha256': sha256(authority_path.read_bytes()).hexdigest(),
        'code_sha256': {name: sha256((root/name).read_bytes()).hexdigest() for name in
                        ['scripts/build_section_mean_maps.py', 'comet_spatial/section_means.py']},
        'historical_payload_unchanged': True}, indent=2)+'\n')
    (run / 'validation.json').write_text(json.dumps(validation, indent=2)+'\n')
    (run.parent / 'latest_run.json').write_text(json.dumps({'run_directory': str(run),
        'payload_file': 'view_payload.json', 'status': 'completed_fixed_three_section_means',
        'source_payload_sha256': digest}, indent=2)+'\n')
    return run


if __name__ == '__main__':
    print(build())
