"""Relocation preserves scientific identity and refuses incomplete raw inputs."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.configure_local_inputs import configure


class ConfigureLocalInputsTests(unittest.TestCase):
    def fixture(self, directory):
        root = Path(directory) / "copied project"
        metadata = root / "metadata"
        metadata.mkdir(parents=True)
        data = root / "entire Chat dataset"
        data.mkdir()
        jobs = ["4998", "5006", "4997", "5001", "5007", "5002",
                "5020", "5003", "5403", "4999", "5005", "5000"]
        files, sections, relationships = [], [], []
        for index, job in enumerate(jobs + ["4978"]):
            filename = "recorded source " + job + ".csv"
            raw = ("Object Id,XMin,YMin\n" + str(index) + ",1,2\n").encode()
            (data / filename).write_bytes(raw)
            digest = hashlib.sha256(raw).hexdigest()
            source = {"path": "/unavailable/old computer/" + filename,
                      "source_file_id": "historical_job_" + job, "sha256": digest}
            files.append({"job": job, "relative_path": filename, "sha256": digest})
            relationships.append({**source, "job": job, "included": job != "4978",
                                  "relationship": "superseded" if job == "4978" else "primary"})
            if job == "4978":
                relationships[-1]["primary_source_file_id"] = "historical_job_5403"
            else:
                sections.append({"job": job, "source": source, "section_id": "section_" + job,
                                 "animal_id": "animal_" + str(index % 6),
                                 "condition": "Homecage" if index % 6 < 3 else "Running",
                                 "pla_type": "HK1" if index < 6 else "PFKP",
                                 "transform": {"matrix": [[-1, 0, index], [0, 1, -index], [0, 0, 1]]}})
        cohort = {"fresh_folder_inventory": {"files": files},
                  "exclusion_policy": {"primary_jobs": jobs, "excluded_jobs": [{"job": "4978"}]}}
        cohort_path = metadata / "cohort_selection.json"
        cohort_path.write_text(json.dumps(cohort))
        manifest = {"sections": sections, "source_relationships": relationships,
                    "cohort_selection": {"path": cohort_path.name,
                                         "sha256": hashlib.sha256(cohort_path.read_bytes()).hexdigest()},
                    "scientific_policy": {"empty_bins": "zero", "coverage": "uncertain"}}
        manifest_path = metadata / "analysis_manifest.json"
        manifest_path.write_text(json.dumps(manifest))
        return root, data, manifest_path, manifest

    def without_paths(self, manifest):
        result = copy.deepcopy(manifest)
        for section in result["sections"]:
            section["source"].pop("path")
        for relation in result["source_relationships"]:
            relation.pop("path")
        return result

    def test_default_folder_relocates_all_thirteen_hash_verified_sources_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root, data, path, before = self.fixture(directory)
            result = configure(root)
            after = json.loads(path.read_text())
            self.assertEqual(self.without_paths(before), self.without_paths(after))
            self.assertEqual(result["verified_csv_files"], 13)
            self.assertTrue(result["manifest_updated"])
            for section in after["sections"]:
                self.assertEqual(Path(section["source"]["path"]).parent, data.resolve())
            for relation in after["source_relationships"]:
                self.assertEqual(Path(relation["path"]).parent, data.resolve())
            self.assertFalse(after["source_relationships"][-1]["included"])
            self.assertEqual(after["source_relationships"][-1]["primary_source_file_id"], "historical_job_5403")

    def test_explicit_data_directory_and_check_only_leave_manifest_byte_identical(self):
        with tempfile.TemporaryDirectory() as directory:
            root, data, path, _ = self.fixture(directory)
            moved = Path(directory) / "separate private CSVs"
            data.rename(moved)
            before, modified = path.read_bytes(), path.stat().st_mtime_ns
            result = configure(root, data_dir=moved, check_only=True)
            self.assertTrue(result["paths_differ"])
            self.assertFalse(result["manifest_updated"])
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(path.stat().st_mtime_ns, modified)

    def test_interrupted_export_hash_mismatch_aborts_without_partial_manifest_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root, data, path, _ = self.fixture(directory)
            before = path.read_bytes()
            (data / "recorded source 4978.csv").write_text("incomplete replacement bytes")
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch for job 4978"):
                configure(root)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(list(path.parent.glob(".analysis_manifest.*.tmp")), [])

    def test_missing_completed_export_aborts_without_changing_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root, data, path, _ = self.fixture(directory)
            before = path.read_bytes()
            (data / "recorded source 5403.csv").unlink()
            with self.assertRaisesRegex(ValueError, "Missing recorded source for job 5403"):
                configure(root)
            self.assertEqual(path.read_bytes(), before)

    def test_changed_cohort_authority_is_rejected_before_relocation(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _, path, _ = self.fixture(directory)
            before = path.read_bytes()
            cohort = path.parent / "cohort_selection.json"
            cohort.write_bytes(cohort.read_bytes() + b" ")
            with self.assertRaisesRegex(ValueError, "cohort metadata SHA-256 mismatch"):
                configure(root)
            self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
