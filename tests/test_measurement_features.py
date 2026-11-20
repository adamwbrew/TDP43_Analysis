"""Raw attributes must remain paired to the same measured objects and positions."""
import csv
import copy
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest

from comet_spatial.measurement_features import extract_section_features, load_feature_cache, point_order_hash, nearest_neighbor_distances


class MeasurementFeatureTests(unittest.TestCase):
    def fixture(self,root):
        path=root/'objects.csv'
        fields=['Object Id','Object Type','Area (µm²)','Average Intensity','ChAt-50 - FITC_E1 present','XMin','XMax','YMin','YMax']
        rows=[['01','PLA - TRITC_E1','.1','.25','1',1,3,2,4],
              ['02','ChAt-50 - FITC_E1','2','.5','1',1,3,2,4],
              ['03','PLA - TRITC_E1','.05','.125','0',3,5,4,6]]
        with path.open('w',newline='') as f:
            writer=csv.writer(f);writer.writerow(fields);writer.writerows(rows)
        digest=sha256(path.read_bytes()).hexdigest()
        spec={'section_id':'one','source':{'path':str(path),'sha256':digest},
              'transform':{'matrix':[[-1,0,10],[0,1,-2],[0,0,1]]}}
        points={'section_id':'one','source_sha256':digest,'object_id':['01','03'],'source_row':[2,4],
                'native_x':[2.,4.],'native_y':[3.,5.],'x':[8.,6.],'y':[1.,3.]}
        return path,spec,points

    def test_full_precision_attributes_preserve_identity_order_and_reflection(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);path,spec,points=self.fixture(root);before=path.read_bytes()
            result=extract_section_features(spec,points,root)
            self.assertEqual(result['area_um2'],[.1,.05]);self.assertEqual(result['intensity'],[.25,.125])
            self.assertEqual(result['markers'],{'chat':[1,0]})
            self.assertEqual(result['point_order_sha256'],point_order_hash(points))
            self.assertEqual(result['source_class_counts'],{'pla':2,'chat':1})
            # The overlapping ChAT-class row is excluded from PLA spacing.
            self.assertEqual(result['nearest_neighbor_distance'],[8**.5,8**.5])
            self.assertEqual(path.read_bytes(),before)

    def test_same_length_reordered_objects_and_changed_coordinates_are_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);_,spec,points=self.fixture(root)
            points['object_id'].reverse()
            with self.assertRaisesRegex(ValueError,'identity or source-row'):extract_section_features(spec,points,root)
            points['object_id'].reverse();points['x'][0]+=1
            with self.assertRaisesRegex(ValueError,'alignment/point cache'):extract_section_features(spec,points,root)

    def test_changed_raw_source_is_rejected_before_attributes_are_reused(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);path,spec,points=self.fixture(root);path.write_text(path.read_text()+'\n')
            with self.assertRaisesRegex(ValueError,'SHA-256 mismatch'):extract_section_features(spec,points,root)

    def test_portable_cache_rejects_corrupt_bytes_and_identity_vector(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);_,spec,points=self.fixture(root);record=extract_section_features(spec,points,root)
            run=root/'outputs/measurement_features/test-run';run.mkdir(parents=True)
            payload={'schema_version':'comet-measurement-features-v1','sections':[record],
                     'validation':{k:True for k in ['source_hashes_verified_before_after','all_pla_object_ids_and_source_rows_matched',
                       'native_and_aligned_coordinates_unchanged','all_selected_pla_objects_retained']}}
            path=run/'features.json';path.write_text(json.dumps(payload))
            pointer=run.parent/'latest_run.json';pointer.write_text(json.dumps({'run_directory':'/unavailable/test-run',
                'payload_file':'features.json','payload_sha256':sha256(path.read_bytes()).hexdigest()}))
            self.assertEqual(load_feature_cache(root,[points])['sections'][0]['area_um2'],[.1,.05])
            points['source_row'][0]=999
            with self.assertRaisesRegex(ValueError,'ordered source objects'):load_feature_cache(root,[points])
            path.write_text(path.read_text()+' ')
            with self.assertRaisesRegex(ValueError,'cache hash mismatch'):load_feature_cache(root,[points])

    def test_nearest_neighbors_are_exact_same_section_distances_without_point_mutation(self):
        points={'x':[0,3],'y':[0,4],'object_id':['a','b']};before=copy.deepcopy(points)
        self.assertEqual(nearest_neighbor_distances(points),[5,5])
        self.assertEqual(points,before)
        self.assertEqual(nearest_neighbor_distances({'x':[0,3,0],'y':[0,0,4]}),[3,3,4])
        # A separate section remains a separate population, not a pooled tree.
        self.assertEqual(nearest_neighbor_distances({'x':[1,2],'y':[0,0]}),[1,1])
        self.assertEqual(nearest_neighbor_distances({'x':[0,10],'y':[0,0]}),[10,10])

    def test_duplicate_positions_keep_zero_spacing_and_singletons_are_undefined(self):
        self.assertEqual(nearest_neighbor_distances({'x':[0,0,3],'y':[0,0,4]}),[0,0,5])
        self.assertEqual(nearest_neighbor_distances({'x':[2],'y':[4]}),[None])
        self.assertEqual(nearest_neighbor_distances({'x':[],'y':[]}),[])
        with self.assertRaisesRegex(ValueError,'finite'):
            nearest_neighbor_distances({'x':[0,float('nan')],'y':[0,1]})

    def test_optional_spacing_vector_is_validated_when_present_and_old_cache_stays_readable(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);_,spec,points=self.fixture(root);record=extract_section_features(spec,points,root)
            run=root/'outputs/measurement_features/test-run';run.mkdir(parents=True)
            payload={'schema_version':'comet-measurement-features-v1','sections':[record],
                     'validation':{k:True for k in ['source_hashes_verified_before_after','all_pla_object_ids_and_source_rows_matched',
                       'native_and_aligned_coordinates_unchanged','all_selected_pla_objects_retained']}}
            path=run/'features.json';pointer=run.parent/'latest_run.json'
            def write():
                path.write_text(json.dumps(payload))
                pointer.write_text(json.dumps({'run_directory':'/unavailable/test-run','payload_file':'features.json',
                                               'payload_sha256':sha256(path.read_bytes()).hexdigest()}))
            record.pop('nearest_neighbor_distance');write()
            self.assertNotIn('nearest_neighbor_distance',load_feature_cache(root,[points])['sections'][0])
            record['nearest_neighbor_distance']=[0,0];write()
            self.assertEqual(load_feature_cache(root,[points])['sections'][0]['nearest_neighbor_distance'],[0,0])
            for bad in [[0],[-1,0],[float('inf'),0],['1',0],[True,0]]:
                record['nearest_neighbor_distance']=bad;write()
                with self.subTest(vector=bad),self.assertRaisesRegex(ValueError,'nearest-neighbor'):
                    load_feature_cache(root,[points])


if __name__=='__main__':unittest.main()
