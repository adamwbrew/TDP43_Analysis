"""Independent fictional section/bin examples and Python/browser-engine parity."""
import copy
import json
import math
from pathlib import Path
import shutil
import subprocess
import unittest

import numpy as np

from comet_spatial.measurements import MEASUREMENTS, COMPARISONS, compute_measurement, compare_conditions


ROOT = Path(__file__).resolve().parents[1]


def fixture():
    grid = {"x_edges": [0, 1, 2, 3, 4, 5], "y_edges": [0, 1]}
    sections, points, features = [], [], []
    for arm in ("HK1", "PFKP"):
        for condition in ("Homecage", "Running"):
            for i in range(3):
                sid = arm+"_"+condition+str(i)
                # Tuples: bin index, area, intensity, ChAT flag. Object numbers
                # differ by section deliberately, so pooling is detectably wrong.
                records = []
                if arm == "HK1" and condition == "Homecage":
                    if i == 0:
                        records = [(0,.05,1,0),(0,.1,2,1),(0,.2,3,1),(0,.4,4,0),(2,.2,2,1)]
                    elif i == 1:
                        records = [(0,.8,8,0)]
                elif arm == "HK1" and condition == "Running":
                    if i == 0:
                        records = [(0,.1,10,1),(0,.3,30,1),(3,.4,4,0)]
                    elif i == 2:
                        records = [(0,.9,90,0)]
                elif i == 0:
                    records = [(0,1 if condition == "Homecage" else 3,1,1)]
                count = [[sum(b == j for b,a,v,m in records) for j in range(5)]]
                sections.append({"section_id":sid,"animal_id":condition+str(i),"pla_type":arm,
                    "condition":condition,"pla_counts":count,"chat_counts":[[0,1,0,0,0]],
                    "observed_support":[[bool(n or j == 1) for j,n in enumerate(count[0])]]})
                points.append({"section_id":sid,"source_sha256":"hash_"+sid,
                               "x":[b+.5 for b,a,v,m in records],"y":[.5]*len(records)})
                xy=[(b+.5,.5) for b,a,v,m in records]
                # Independent brute-force nearest distances for these tiny
                # fictional sections; production caches use a same-section tree.
                nearest=[min(math.dist(point,other) for j,other in enumerate(xy) if j!=k)
                         if len(xy)>1 else None for k,point in enumerate(xy)]
                features.append({"section_id":sid,"source_sha256":"hash_"+sid,
                    "area_um2":[a for b,a,v,m in records],"intensity":[v for b,a,v,m in records],
                    "nearest_neighbor_distance":nearest,
                    "markers":{"chat":[m for b,a,v,m in records]}})
    payload = {"grid":grid,"sections":sections,"pla_points":points,
               "arms":{arm:{"displayable":[[True,True,True,True,False]]} for arm in ("HK1","PFKP")}}
    cache = {"schema_version":"comet-measurement-features-v1","available_markers":[{"id":"chat","label":"ChAT","source_column":"ChAt-50 - FITC_E1 present"}],
             "sections":features,"default_area_cutoff":.1}
    return payload, cache


def clean(value):
    if isinstance(value,np.ndarray):
        return clean(value.tolist())
    if isinstance(value,dict):
        return {k:clean(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):
        return [clean(v) for v in value]
    if isinstance(value,(float,np.floating)):
        return float(value) if np.isfinite(value) else None
    if isinstance(value,(np.integer,np.bool_)):
        return value.item()
    return value


class MeasurementArithmeticTests(unittest.TestCase):
    def test_all_nineteen_section_measurements_from_hand_calculated_objects(self):
        payload, features = fixture()
        expected = {"pla_count":4,"large_pla_count":3,"small_pla_count":1,"large_pla_fraction":.75,
                    "mean_pla_area":.1875,"median_pla_area":.15,"p90_pla_area":.34,"total_pla_area":.75,
                    "mean_pla_intensity":2.5,"marker_associated_pla_count":2,
                    "marker_associated_pla_fraction":.5,"marker_associated_large_pla_count":2,
                    "marker_associated_pla_mean_area":.15,"section_pla_share":80,
                    "marker_associated_pla_area_fraction":.4,"median_pla_intensity":2.5,
                    "pla_area_iqr":.1625,"pla_area_cv":math.sqrt(115)/15,
                    "mean_pla_nearest_neighbor_distance":0}
        self.assertEqual(set(expected),{m["id"] for m in MEASUREMENTS})
        for metric,value in expected.items():
            with self.subTest(metric=metric):
                result = compute_measurement(payload,features,metric)
                section = next(s for s in result["sections"] if s["section_id"] == "HK1_Homecage0")
                self.assertAlmostEqual(section["values"][0,0],value)

    def test_section_weighting_does_not_pool_objects_or_replace_missing_means_with_zero(self):
        payload,features = fixture()
        count = compute_measurement(payload,features,"pla_count")["arms"]["HK1"]
        area = compute_measurement(payload,features,"mean_pla_area")["arms"]["HK1"]
        self.assertAlmostEqual(count["homecage_mean"][0,0],5/3)
        self.assertEqual(count["homecage_valid_section_n"][0,0],3)
        self.assertAlmostEqual(area["homecage_mean"][0,0],(.1875+.8)/2)
        self.assertNotAlmostEqual(area["homecage_mean"][0,0],1.55/5)  # Pooled-object mean.
        self.assertEqual(area["homecage_valid_section_n"][0,0],2)
        self.assertAlmostEqual(area["running_mean"][0,0],(.2+.9)/2)
        associated = compute_measurement(payload,features,"marker_associated_pla_mean_area")["arms"]["HK1"]
        self.assertEqual(associated["homecage_valid_section_n"][0,0],1)
        self.assertAlmostEqual(associated["homecage_mean"][0,0],.15)

    def test_empty_bin_counts_and_sums_zero_but_fractions_and_intensives_undefined(self):
        payload,features=fixture()
        for metric in MEASUREMENTS:
            with self.subTest(metric=metric["id"]):
                arm=compute_measurement(payload,features,metric["id"])["arms"]["HK1"]
                if metric["empty_bin_rule"]=="assumed_zero":
                    self.assertEqual(arm["homecage_mean"][0,1],0)
                    self.assertEqual(arm["homecage_valid_section_n"][0,1],2 if metric["id"]=="section_pla_share" else 3)
                    self.assertEqual(arm["difference"][0,1],0)
                else:
                    self.assertTrue(np.isnan(arm["homecage_mean"][0,1]))
                    self.assertEqual(arm["homecage_valid_section_n"][0,1],0)
                    self.assertFalse(arm["displayable"][0,1])
                self.assertFalse(arm["displayable"][0,4])
                self.assertEqual(arm["missing_reason"][0,4],"outside_display_domain")

    def test_cutoff_boundary_is_inclusive_and_configurable(self):
        payload,features=fixture()
        large=compute_measurement(payload,features,"large_pla_count",area_cutoff=.1)
        small=compute_measurement(payload,features,"small_pla_count",area_cutoff=.1)
        self.assertEqual(large["sections"][0]["values"][0,0],3)  # Includes area exactly .1.
        self.assertEqual(small["sections"][0]["values"][0,0],1)
        for cutoff in [0,.1,.2,1]:
            ll=compute_measurement(payload,features,"large_pla_count",area_cutoff=cutoff)
            ss=compute_measurement(payload,features,"small_pla_count",area_cutoff=cutoff)
            for original,l,s in zip(payload["sections"],ll["sections"],ss["sections"]):
                np.testing.assert_array_equal(l["values"]+s["values"],original["pla_counts"])
        with self.assertRaisesRegex(ValueError,"cutoff"):
            compute_measurement(payload,features,"large_pla_count",area_cutoff=-1)

    def test_comparisons_follow_condition_means_and_mask_zeros_without_pseudocounts(self):
        payload,features=fixture()
        percent=compute_measurement(payload,features,"pla_count",comparison="percent_change")
        log=compute_measurement(payload,features,"pla_count",comparison="log2_fold_change")
        arm=percent["arms"]["HK1"]
        self.assertAlmostEqual(arm["difference"][0,0],-40)
        self.assertAlmostEqual(arm["difference"][0,2],-100)  # R=0, H>0 is a valid percent loss.
        for index in [1,3]:
            self.assertTrue(np.isnan(arm["difference"][0,index]))
            self.assertEqual(arm["missing_reason"][0,index],"zero_homecage_mean")
        self.assertAlmostEqual(log["arms"]["HK1"]["difference"][0,0],np.log2(3/5))
        self.assertTrue(np.isnan(log["arms"]["HK1"]["difference"][0,2]))
        self.assertIsNone(log["pseudocount"])
        pure=compare_conditions([[2,0,3,np.nan]],[[1,1,0,2]],"percent_change")
        np.testing.assert_allclose(pure["values"],[[100,-100,np.nan,np.nan]],equal_nan=True)

    def test_invalid_features_contaminate_only_relevant_metric_bins(self):
        payload,features=fixture()
        features["sections"][0]["area_um2"][0]=None  # Non-associated PLA object.
        mean=compute_measurement(payload,features,"mean_pla_area")
        associated=compute_measurement(payload,features,"marker_associated_pla_mean_area")
        count=compute_measurement(payload,features,"pla_count")
        self.assertFalse(mean["sections"][0]["defined"][0,0])
        self.assertAlmostEqual(associated["sections"][0]["values"][0,0],.15)
        self.assertEqual(count["sections"][0]["values"][0,0],4)
        features["sections"][0]["markers"]["chat"][0]=None
        self.assertFalse(compute_measurement(payload,features,"marker_associated_pla_count")["sections"][0]["defined"][0,0])
        features["sections"][0]["intensity"][1]=None
        self.assertFalse(compute_measurement(payload,features,"mean_pla_intensity")["sections"][0]["defined"][0,0])

    def test_arms_eligibility_and_inputs_stay_separate_and_unchanged(self):
        payload,features=fixture();before=copy.deepcopy((payload,features))
        result=compute_measurement(payload,features,"mean_pla_area")
        self.assertEqual(result["arms"]["PFKP"]["difference"][0,0],2)
        self.assertAlmostEqual(result["arms"]["HK1"]["difference"][0,0],.05625)
        self.assertEqual(result["color_scale"]["cmax"],2)
        self.assertEqual((payload,features),before)
        self.assertFalse(result["coverage_verified"])
        np.testing.assert_array_equal(result["arms"]["HK1"]["eligibility"],payload["arms"]["HK1"]["displayable"])
        with self.assertRaisesRegex(ValueError,"marker"):
            compute_measurement(payload,features,"marker_associated_pla_count",marker="not_exported")

    def test_misaligned_points_feature_lengths_hashes_and_duplicate_specimens_are_rejected(self):
        for corrupt in ['point','length','hash','animal','duplicate_features']:
            payload,features=fixture()
            if corrupt=='point':payload['pla_points'][0]['x'][0]=1.5
            elif corrupt=='length':features['sections'][0]['area_um2'].pop()
            elif corrupt=='hash':features['sections'][0]['source_sha256']='wrong'
            elif corrupt=='animal':payload['sections'][1]['animal_id']=payload['sections'][0]['animal_id']
            else:features['sections'].append(features['sections'][0])
            with self.subTest(corrupt=corrupt),self.assertRaises(ValueError):
                compute_measurement(payload,features,'mean_pla_area')

    def test_section_share_uses_its_own_full_section_total_and_keeps_zero_total_missing(self):
        payload,features=fixture()
        result=compute_measurement(payload,features,'section_pla_share')
        first,second,empty=result['sections'][:3]
        np.testing.assert_allclose(first['values'],[[80,0,20,0,0]])
        self.assertEqual(np.nansum(first['values']),100)
        self.assertEqual(np.nansum(second['values']),100)
        self.assertFalse(empty['defined'].any())
        self.assertEqual(result['arms']['HK1']['homecage_mean'][0,0],90)
        self.assertEqual(result['comparison']['units'],'percentage points')
        self.assertEqual(result['measurement']['units'],'% of section PLA')
        # A recorded full-section total remains the denominator even if a
        # displayed/counted field contains only part of those detections.
        payload['sections'][0]['pla_objects']=10
        partial=compute_measurement(payload,features,'section_pla_share')['sections'][0]
        self.assertEqual(partial['values'][0,0],40)
        payload['sections'][0]['pla_objects']=1
        with self.assertRaisesRegex(ValueError,'Section PLA total'):
            compute_measurement(payload,features,'section_pla_share')

    def test_marker_area_fraction_is_area_weighted_and_unknown_denominators_stay_missing(self):
        payload,features=fixture()
        result=compute_measurement(payload,features,'marker_associated_pla_area_fraction')
        self.assertAlmostEqual(result['sections'][0]['values'][0,0],.3/.75)
        self.assertEqual(result['sections'][1]['values'][0,0],0)
        self.assertAlmostEqual(result['arms']['HK1']['homecage_mean'][0,0],.2)
        self.assertNotAlmostEqual(result['arms']['HK1']['homecage_mean'][0,0],.3/1.55)
        features['sections'][0]['area_um2'][0]=None  # Non-associated area still affects total area.
        self.assertFalse(compute_measurement(payload,features,'marker_associated_pla_area_fraction')['sections'][0]['defined'][0,0])
        payload,features=fixture()
        features['sections'][0]['area_um2'][:4]=[0,0,0,0]
        self.assertFalse(compute_measurement(payload,features,'marker_associated_pla_area_fraction')['sections'][0]['defined'][0,0])

    def test_median_intensity_and_iqr_use_within_section_type7_quantiles(self):
        payload,features=fixture()
        features['sections'][0]['intensity'][:4]=[0,1,2,100]
        median=compute_measurement(payload,features,'median_pla_intensity')
        self.assertEqual(median['sections'][0]['values'][0,0],1.5)
        self.assertEqual(median['arms']['HK1']['homecage_mean'][0,0],(1.5+8)/2)
        iqr=compute_measurement(payload,features,'pla_area_iqr')
        self.assertAlmostEqual(iqr['sections'][0]['values'][0,0],.25-.0875)
        self.assertEqual(iqr['sections'][1]['values'][0,0],0)  # Singleton IQR is zero, not missing.
        self.assertFalse(iqr['sections'][0]['defined'][0,1])
        features['sections'][0]['intensity'][0]=None
        self.assertFalse(compute_measurement(payload,features,'median_pla_intensity')['sections'][0]['defined'][0,0])

    def test_area_cv_is_population_requires_two_positive_mean_and_is_numerically_stable(self):
        payload,features=fixture()
        result=compute_measurement(payload,features,'pla_area_cv')
        self.assertAlmostEqual(result['sections'][0]['values'][0,0],math.sqrt(115)/15)
        self.assertFalse(result['sections'][1]['defined'][0,0])  # One object.
        features['sections'][0]['area_um2'][:4]=[1,1,1,1]
        self.assertEqual(compute_measurement(payload,features,'pla_area_cv')['sections'][0]['values'][0,0],0)
        features['sections'][0]['area_um2'][:4]=[0,0,0,0]
        self.assertFalse(compute_measurement(payload,features,'pla_area_cv')['sections'][0]['defined'][0,0])
        features['sections'][0]['area_um2'][:4]=[1e12,1e12+1,1e12,1e12+1]
        self.assertAlmostEqual(compute_measurement(payload,features,'pla_area_cv')['sections'][0]['values'][0,0],.5/(1e12+.5),places=24)
        features['sections'][0]['area_um2'][0]=None
        self.assertFalse(compute_measurement(payload,features,'pla_area_cv')['sections'][0]['defined'][0,0])

    def test_nearest_neighbor_uses_precomputed_full_section_values_and_accepts_duplicate_zeros(self):
        payload,features=fixture()
        result=compute_measurement(payload,features,'mean_pla_nearest_neighbor_distance')
        first,one=result['sections'][:2]
        self.assertEqual(first['values'][0,0],0)  # Four duplicate positions; distinct objects.
        self.assertEqual(first['values'][0,2],2)  # One local object, neighbor lies in another bin.
        self.assertFalse(one['defined'][0,0])  # Whole-section singleton has no other object.
        self.assertEqual(result['measurement']['units'],'exported coordinate units')
        features['sections'][0]['nearest_neighbor_distance'][0]=-1
        self.assertFalse(compute_measurement(payload,features,'mean_pla_nearest_neighbor_distance')['sections'][0]['defined'][0,0])
        features['sections'][0]['nearest_neighbor_distance'].pop()
        with self.assertRaisesRegex(ValueError,'Nearest-neighbor distances'):
            compute_measurement(payload,features,'mean_pla_nearest_neighbor_distance')


@unittest.skipUnless(shutil.which("node"),"Node is needed for browser-engine parity checks")
class BrowserMeasurementParityTests(unittest.TestCase):
    def test_every_measurement_comparison_and_edge_case_matches_python(self):
        payload,features=fixture()
        # Include a contaminated non-associated area to check dependency-specific
        # invalidation, not just finite happy-path numerical agreement.
        features['sections'][0]['area_um2'][0]=None
        request={'payload':payload,'features':features,'metrics':[m['id']for m in MEASUREMENTS],
                 'comparisons':[c['id']for c in COMPARISONS]}
        program="const fs=require('fs'),M=require("+json.dumps(str(ROOT/'scripts/comet_measurements.js'))+");const q=JSON.parse(fs.readFileSync(0,'utf8'));console.log(JSON.stringify(q.metrics.flatMap(id=>q.comparisons.map(comparison=>M.calculate(q.payload,q.features,id,{areaCutoff:.1,marker:'chat',comparison})))));"
        completed=subprocess.run([shutil.which('node'),'-e',program],input=json.dumps(request),capture_output=True,text=True,check=True,timeout=20)
        actual=json.loads(completed.stdout)
        expected=[clean(compute_measurement(payload,features,metric,comparison=comparison))for metric in request['metrics']for comparison in request['comparisons']]
        self.assertEqual(len(actual),57)
        for one,two in zip(actual,expected):
            with self.subTest(metric=one['measurement']['id'],comparison=one['comparison']['id']):
                self.assertEqual(one['measurement'],two['measurement']);self.assertEqual(one['comparison'],two['comparison'])
                for a,b in zip(one['sections'],two['sections']):
                    np.testing.assert_allclose(np.asarray(a['values'],float),np.asarray(b['values'],float),rtol=1e-13,atol=1e-13,equal_nan=True)
                    self.assertEqual(a['defined'],b['defined'])
                for arm in ['HK1','PFKP']:
                    for key in ['homecage_mean','running_mean','difference','absolute_difference','homecage_valid_section_n','running_valid_section_n']:
                        np.testing.assert_allclose(np.asarray(one['arms'][arm][key],float),np.asarray(two['arms'][arm][key],float),rtol=1e-13,atol=1e-13,equal_nan=True)
                    for key in ['displayable','eligibility','missing_reason']:
                        self.assertEqual(one['arms'][arm][key],two['arms'][arm][key])

    def test_browser_helpers_cover_boundary_and_zero_log_cases(self):
        program="const M=require("+json.dumps(str(ROOT/'scripts/comet_measurements.js'))+");console.log(JSON.stringify({bins:[0,1,2,-.01,2.01].map(v=>M.binIndex([0,1,2],v)),q:M.quantile([.05,.1,.2,.4],.9),percent:M.compareConditions([[2,0,3,null]],[[1,1,0,2]],'percent_change'),log:M.compareConditions([[0,2,0]],[[1,1,0]],'log2_fold_change')}));"
        result=json.loads(subprocess.run([shutil.which('node'),'-e',program],capture_output=True,text=True,check=True,timeout=10).stdout)
        self.assertEqual(result['bins'],[0,1,1,-1,-1]);self.assertAlmostEqual(result['q'],.34)
        self.assertEqual(result['percent']['values'],[[100,-100,None,None]])
        self.assertEqual(result['log']['values'],[[None,1,None]])


if __name__=='__main__':
    unittest.main()
