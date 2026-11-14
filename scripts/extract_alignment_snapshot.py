#!/usr/bin/env python3
"""Extract the old app's saved display alignment exactly, without refitting.

This preserves historical labels, fixed centers/flips and native binned display
counts. It does not construct tissue masks, derive new object centroids, choose
flips, or calculate current biological condition differences.
"""
import argparse
import csv
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def asset(path):
    return {"path": str(path), "sha256": sha256(path), "bytes": path.stat().st_size}


def extract(old_root, input_manifest, output_directory):
    app = old_root / "outputs/spatial_handoff/app/index.html"
    text = app.read_text(encoding="utf-8")
    marker = re.search(r"const root=document.getElementById\('[^']+'\), DATA=", text)
    if marker is None:
        raise ValueError("Original explorer DATA marker was not found; do not guess another payload")
    data, length = json.JSONDecoder().raw_decode(text[marker.end():])
    git = Path("/Users/adambrewer/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/fallback/git")
    try:
        revision = subprocess.run([str(git) if git.exists() else "git", "-C", str(old_root), "rev-parse", "HEAD"],
                                  capture_output=True, text=True, timeout=10, check=False)
        source_revision = revision.stdout.strip() if revision.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        source_revision = None
    proposals_path = old_root / "outputs/spatial_handoff/tables/alignment_proposals.json"
    proposals = {p["job"]: p for p in json.loads(proposals_path.read_text(encoding="utf-8"))}
    if len(data["sections"]) != 12 or len(proposals) != 12:
        raise ValueError("This historical snapshot expects the recorded 12-section app")
    current_hashes, input_checks = {}, []
    with input_manifest.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            path = Path(row["source_path"])
            digest = sha256(path)
            if digest != row["sha256"]:
                raise ValueError("Current input changed since inventory: " + str(path))
            current_hashes.setdefault(digest, []).append(row["file_id"])
            input_checks.append({"file_id": row["file_id"], "path": str(path), "sha256": digest,
                                 "matches_recorded_manifest": True})
    reference = old_root / "outputs/spatial_handoff/figures/19_feature_alignment_before_after.png"
    check = {**asset(reference), "source_path": str(reference), "figure_id": "19_feature_alignment_before_after",
             "caption": "All 12 sections have inspectable proposals. Cross = cavity anchor. Flips are geometric suggestions, "
                        "not anatomical approvals. Cropped edges do not move the anchor; remaining shape differences may "
                        "reflect section level, tissue loss or imperfect landmarks.",
             "source_function": "bio_visuals.feature_alignment.alignment_figure(geometry_250, stored_proposals)",
             "replay_without_refit": True}
    sections, compact, numeric_checks = [], [], []
    for source in data["sections"]:
        saved = source["proposed"]
        if saved != proposals[source["job"]]:
            raise ValueError("Embedded and saved transform records differ for " + source["job"])
        sx = -1 if saved["flip"] in ("horizontal", "both") else 1
        sy = -1 if saved["flip"] in ("vertical", "both") else 1
        cx, cy = saved["center"]
        matrix = [[sx, 0, -sx * cx], [0, sy, -sy * cy], [0, 0, 1]]
        grid = source["grids"]["250"]
        width = grid["width"]
        # Recover the already fixed native cell edges from saved bin centers.
        # This is exact grid bookkeeping, not tissue/landmark estimation.
        geometry = {"x_edges": [x - width / 2 for x in grid["x"]] + [grid["x"][-1] + width / 2],
                    "y_edges": [y - width / 2 for y in grid["y"]] + [grid["y"][-1] + width / 2],
                    "width": width, "n_all": grid["n_all"]}
        section = {key: source[key] for key in ("job", "animal", "group", "arm", "order", "color", "ready", "proposed")}
        section.update(filename=source["source"], source=source["source"], source_sha256=saved["source_sha256"],
                       current_input_file_ids=current_hashes.get(saved["source_sha256"], []), historical_assignments_only=True,
                       saved_center=saved["center"], saved_flip=saved["flip"], fixed_transform_matrix=matrix,
                       candidate_polygon_native=saved["polygon_native"],
                       candidate_polygon_role="Internal cavity anchor only; NOT outer tissue boundary or tissue mask",
                       reference_job=saved["reference_job"],
                       reference_frame="Independent per-arm cavity-origin / historical 21F orientation frame; not a validated global anatomical registration",
                       grids={"250": source["grids"]["250"], "500": source["grids"]["500"]},
                       alignment_figure_geometry_grid=geometry)
        sections.append(section)
        compact.append({key: value for key, value in section.items()
                        if key not in ("grids", "alignment_figure_geometry_grid", "candidate_polygon_native")})
        compact[-1]["grids"] = {"500": source["grids"]["500"]}
        with np.load(old_root / ("outputs/spatial_handoff/spatial_arrays/job_%s_metrics.npz" % source["job"]),
                     allow_pickle=False) as arrays:
            equal = all(np.array_equal(source["grids"]["1000"][key], arrays[key])
                        for key in ("n_pla", "n_chat", "n_all", "n_positive"))
            support_proxy = bool(np.array_equal(arrays["support"], arrays["n_all"] > 0))
        if not equal or not support_proxy:
            raise ValueError("Saved app/NPZ provenance changed for " + source["job"])
        numeric_checks.append({"job": source["job"], "embedded_proposal_equals_saved_json": True,
                               "metric_counts_equal_saved_npz": equal,
                               "saved_npz_support_equals_n_all_gt_zero": support_proxy})
    shared = {"schema_version": 1, "source_app_path": str(app), "source_app_sha256": sha256(app),
              "source_revision": source_revision,
              "remote_main_revision": "4631e1517f85de2c4bfb59879bf44f406770a903",
              "remote_main_verification_date": "2026-11-11",
              "scope": "Exact saved historical alignment display replay. No fitting, no new mask construction, "
                       "no condition-result recomputation. Historical identifiers and groups remain historical context.",
              "historical_assignments_only": True, "anatomical_approvals": sum(s["ready"] for s in data["sections"]),
              "coordinate_formula": "x_aligned = sign_x * (x_native - saved_center_x); y_aligned = sign_y * (y_native - saved_center_y)",
              "coordinate_units": data["units"],
              "display_grid_semantics": "Saved native positions are bin centers, not individual object centroids. "
                                        "Counts are unchanged. n_all>0 is object occupancy, not strict tissue coverage.",
              "display_orientation": {"x_increases_to": "right", "y_increases_to": "down"},
              "layer_order": data["animal_order"], "layer_order_meaning": data["order_meaning"],
              "alignment_check": check, "current_exact_byte_matches": sum(bool(s["current_input_file_ids"]) for s in sections),
              "extraction": {"method": "JSONDecoder.raw_decode after the original explorer const root / DATA marker",
                             "marker_character_offset": marker.start(), "payload_characters": length,
                             "default_original_frame": "proposed", "all_12_saved_transforms_preserved": True,
                             "script_sha256": sha256(Path(__file__))}}
    output_directory.mkdir(parents=True, exist_ok=True)
    snapshot_path = output_directory / "alignment_snapshot.json"
    snapshot_path.write_text(json.dumps({**shared, "sections": sections}, ensure_ascii=False, separators=(",", ":")) + "\n",
                             encoding="utf-8")
    audit_path = output_directory / "asset_audit.json"
    audit = json.loads(audit_path.read_text(encoding="utf-8")) if audit_path.exists() else {"schema_version": 1}
    audit.update(saved_app_snapshot={**shared, "sections": compact}, snapshot_asset=asset(snapshot_path),
                 saved_app_numeric_checks=numeric_checks, current_input_hash_verification=input_checks,
                 snapshot_extraction_utc=datetime.now(timezone.utc).isoformat())
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return snapshot_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old-root", type=Path, default=Path("/Users/adambrewer/Desktop/Coding/Bio_Data_Analysis"))
    parser.add_argument("--input-manifest", type=Path, default=ROOT / "metadata/input_manifest.csv")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs/comet_core")
    args = parser.parse_args()
    path = extract(args.old_root.expanduser().resolve(), args.input_manifest.expanduser().resolve(),
                   args.output_dir.expanduser().resolve())
    print("Saved exact 12-section historical alignment snapshot: " + str(path))


if __name__ == "__main__":
    main()
