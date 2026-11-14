#!/usr/bin/env python3
"""Verify the selected thirteen CSVs and relocate local raw-input paths.

Only source paths in analysis_manifest.json are changed. The twelve completed
sections, interrupted-export exclusion, hashes, assignments, fixed transforms
and all scientific policy records remain unchanged. Raw files are never copied.
Viewing the app and rerunning from saved counts do not require this step.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def configure(root=ROOT, data_dir=None, check_only=False):
    root = Path(root).resolve()
    data_dir = Path(data_dir).expanduser().resolve() if data_dir is not None else root / "entire Chat dataset"
    manifest_path = root / "metadata/analysis_manifest.json"
    original = manifest_path.read_bytes()
    manifest = json.loads(original)
    authority = manifest["cohort_selection"]
    cohort_path = Path(authority["path"])
    if not cohort_path.is_absolute():
        cohort_path = manifest_path.parent / cohort_path
    if digest(cohort_path) != authority["sha256"]:
        raise ValueError("Recorded cohort metadata SHA-256 mismatch; no paths changed")
    cohort = json.loads(cohort_path.read_text())
    inventory = cohort["fresh_folder_inventory"]["files"]
    expected = {str(record["job"]): record for record in inventory}
    if len(inventory) != 13 or len(expected) != 13:
        raise ValueError("Expected thirteen distinct recorded source exports")
    sections = manifest["sections"]
    relationships = manifest["source_relationships"]
    primary = {str(value) for value in cohort["exclusion_policy"]["primary_jobs"]}
    excluded = {str(record["job"]) for record in cohort["exclusion_policy"]["excluded_jobs"]}
    if len(sections) != 12 or len(primary) != 12 or excluded != {"4978"} or "5403" not in primary:
        raise ValueError("Expected the twelve completed sections with 4978 superseded by 5403")
    by_job = {str(record["job"]): record for record in relationships}
    if len(relationships) != 13 or len(by_job) != 13 or set(by_job) != primary | excluded or set(expected) != set(by_job):
        raise ValueError("Source relationships do not match the recorded thirteen-export cohort")
    if {str(record["job"]) for record in sections} != primary:
        raise ValueError("Section jobs do not match the twelve recorded completed exports")
    for job, relation in by_job.items():
        if relation["included"] is not (job in primary):
            raise ValueError("Included/excluded source status changed for job " + job)
    interrupted = by_job["4978"]
    if interrupted.get("relationship") != "superseded" or interrupted.get("primary_source_file_id") != by_job["5403"]["source_file_id"]:
        raise ValueError("The interrupted job 4978 must remain superseded by 5403")
    for section in sections:
        source, relation = section["source"], by_job[str(section["job"])]
        if source["source_file_id"] != relation["source_file_id"] or source["sha256"] != relation["sha256"]:
            raise ValueError("Section source identity disagrees with its recorded relationship")
    verified = {}
    for job, relation in by_job.items():
        record = expected[job]
        filename = record.get("relative_path") or Path(record["path"]).name
        if not filename or Path(filename).name != filename:
            raise ValueError("Recorded input filename must be a single filename: " + str(filename))
        if relation["sha256"] != record["sha256"]:
            raise ValueError("Manifest/cohort source hashes disagree for job " + job)
        path = data_dir / filename
        if not path.is_file():
            raise ValueError("Missing recorded source for job " + job + ": " + str(path))
        if digest(path) != record["sha256"]:
            raise ValueError("Raw source SHA-256 mismatch for job " + job + ": " + str(path))
        verified[job] = str(path)
    updated = copy.deepcopy(manifest)
    for section in updated["sections"]:
        section["source"]["path"] = verified[str(section["job"])]
    for relation in updated["source_relationships"]:
        relation["path"] = verified[str(relation["job"])]
    changed = updated != manifest
    if not check_only and changed:
        # Verify everything before replacing the one mutable configuration file.
        # Reject concurrent edits instead of losing another person's changes.
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=manifest_path.parent,
                                             prefix=".analysis_manifest.", suffix=".tmp", delete=False) as handle:
                temporary = Path(handle.name)
                json.dump(updated, handle, indent=2, ensure_ascii=False)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            if manifest_path.read_bytes() != original:
                raise RuntimeError("Manifest changed during verification; no paths replaced")
            temporary.replace(manifest_path)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()
    return {"verified_csv_files": len(verified), "completed_sections": 12,
            "interrupted_export": "4978 verified and still excluded; replacement 5403",
            "data_directory": str(data_dir), "manifest": str(manifest_path),
            "check_only": check_only, "paths_differ": changed,
            "manifest_updated": changed and not check_only}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path,
                        help="Folder containing the thirteen original CSV exports (default: repository/entire Chat dataset)")
    parser.add_argument("--check-only", action="store_true", help="Verify every hash without changing the manifest")
    args = parser.parse_args(argv)
    try:
        result = configure(data_dir=args.data_dir, check_only=args.check_only)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as exc:
        parser.exit(2, "INPUT CONFIGURATION STOPPED: " + str(exc) + "\n")
    print(json.dumps(result, indent=2))
    print("Current comparison: three-section means, empty section-bins assumed zero, coverage uncertain.")
    print("The historical strict tissue-mask method remains separate; no mask requirement is added to this comparison.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
