"""Build the exploratory maps and separately retained strict PDF views.

The numerical core payload supplies differences and tissue-valid section counts.
A separately traced historical snapshot may reproduce saved transforms for review;
its approval and study scope stay visible and it never supplies a tissue mask.
"""
from pathlib import Path
import base64
import hashlib
import json
from plotly.offline import get_plotlyjs
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from comet_spatial.measurement_features import ensure_spatial_feature_cache
from comet_spatial.context_geometry import build_context_geometry


def load_exploratory(root):
    """Read only the explicitly selected immutable exploratory run, if supplied."""
    root = Path(root)
    pointer = root / "outputs/exploratory/latest_run.json"
    if not pointer.is_file():
        return {}
    latest = json.loads(pointer.read_text())
    value = latest.get("view_payload_path") or latest.get("view_payload") or latest.get("payload_path") or latest.get("payload_file")
    run_value = latest.get("run_directory") or latest.get("path") or latest.get("run_path")
    recorded_directory = Path(run_value) if run_value else (Path(value).parent if value else None)
    local_candidate = None
    if recorded_directory is not None:
        local_candidate = root / "outputs/exploratory" / recorded_directory.name / (Path(value).name if value else "view_payload.json")
    # A copied project owns its copied immutable run, even when the pointer still
    # records the original machine/workspace's absolute location.
    if local_candidate is not None and local_candidate.is_file():
        candidate = local_candidate
    elif value:
        candidate = Path(value)
        if not candidate.is_absolute():
            choices = [root / candidate, pointer.parent / candidate]
            if run_value:
                run_dir = Path(run_value)
                if not run_dir.is_absolute():
                    run_dir = root / run_dir
                choices.insert(0, run_dir / candidate)
            candidate = next((path for path in choices if path.is_file()), choices[0])
    elif run_value:
        directory = Path(run_value)
        if not directory.is_absolute():
            directory = root / directory
        candidate = directory / "view_payload.json"
    else:
        raise ValueError("Exploratory latest_run.json does not identify its saved view payload")
    payload = json.loads(candidate.read_text())
    if payload.get("status") != "exploratory_ready" or payload.get("strict_pdf_results") is not False:
        raise ValueError("Exploratory payload must be ready and explicitly separate from strict PDF results")
    checks = payload.get("validation", {})
    required_checks = ("count_conservation_passed", "input_hashes_verified_before_and_after", "fixed_transforms_unchanged", "all_raw_objects_counted")
    if not all(checks.get(key) is True for key in required_checks):
        raise ValueError("Exploratory payload lacks completed count/source/transform validation")
    payload["saved_payload_path"] = str(candidate)
    payload["inline_figures"] = []
    figure_manifest = candidate.parent / "figure_manifest.json"
    figure_metadata = json.loads(figure_manifest.read_text()).get("figures", []) if figure_manifest.is_file() else []
    by_filename = {Path(figure["path"]).name: figure for figure in figure_metadata}
    primary_figures = {"exploratory_difference_hk1.png", "exploratory_difference_pfkp.png",
                       "observed_support_four_panels.png", "exploratory_condition_means.png"}
    for image in sorted((candidate.parent / "figures").glob("*.png")):
        if image.name not in primary_figures:
            continue
        raw = image.read_bytes()
        payload["inline_figures"].append({"filename": image.name,
            "title": by_filename.get(image.name, {}).get("title", image.stem.replace("_", " ")),
            "caption": by_filename.get(image.name, {}).get("caption", ""), "sha256": hashlib.sha256(raw).hexdigest(),
            "data_url": "data:image/png;base64," + base64.b64encode(raw).decode("ascii")})
    return payload


def load_multiresolution(root):
    """Embed the selected genuine raw-count resolutions and complete PLA cache."""
    root = Path(root)
    # The dated scientist clarification selects a separate immutable fixed-three
    # derivation. Never overwrite or silently reinterpret the older support mean.
    pointer = root / "outputs/section_means/latest_run.json"
    if not pointer.is_file():
        pointer = root / "outputs/exploratory_multiresolution/latest_run.json"
    if not pointer.is_file():
        return {}
    latest = json.loads(pointer.read_text())
    run = Path(latest["run_directory"])
    filename = latest.get("payload_file", "view_payload.json")
    local = pointer.parent / run.name / Path(filename).name
    if local.is_file():
        path = local
    else:
        path = (run if run.is_absolute() else root / run) / filename
    payload = json.loads(path.read_text())
    if payload.get("schema_version") != "comet-multiresolution-v1":
        raise ValueError("Unrecognized multiresolution payload")
    resolutions = payload.get("resolutions", {})
    if set(resolutions) != {"1000", "500", "250", "100"}:
        raise ValueError("Multiresolution payload must retain all four calculated grids")
    checks = payload.get("validation", {})
    if not all(checks.get(key) is True for key in ("count_conservation_all_resolutions", "full_pla_point_count_matches_raw", "hashes_verified_before_after_and_before_publication", "fixed_transforms_unchanged")):
        raise ValueError("Multiresolution conservation, point-cache or provenance validation is incomplete")
    point_total = 0
    for record in payload.get("pla_points", []):
        lengths = [len(record[key]) for key in ("x", "y", "object_id", "source_row")]
        if record.get("sampled") is not False or len(set(lengths)) != 1:
            raise ValueError("Detailed PLA point cache must be complete and unsampled")
        point_total += lengths[0]
    if point_total != checks.get("full_pla_point_count"):
        raise ValueError("Detailed PLA point cache does not match recorded source count")
    manifest_path = path.parent / "detailed_figure_manifest.json"
    figures = json.loads(manifest_path.read_text()).get("figures", []) if manifest_path.is_file() else []
    for width, values in resolutions.items():
        if values.get("strict_pdf_results") is not False:
            raise ValueError("Multiresolution maps must remain explicitly exploratory")
        values["inline_figures"] = []
        for figure in figures:
            identifier = figure.get("id", "")
            if not (identifier.endswith("_" + width) or (width == "250" and identifier == "resolution_sensitivity")):
                continue
            image = path.parent / figure["path"]
            raw = image.read_bytes()
            values["inline_figures"].append({"filename": image.name,
                "title": figure.get("title", identifier.replace("_", " ")),
                "caption": figure.get("caption", ""),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "data_url": "data:image/png;base64," + base64.b64encode(raw).decode("ascii")})
    payload["saved_payload_path"] = str(path)
    return payload


def build(root=ROOT):
    root = Path(root)
    payload_path = root / "outputs/core_view/payload.json"
    if payload_path.is_file():
        core = json.loads(payload_path.read_text())
    else:
        core = {"schema_version": "comet-core-view-v1", "status": "blocked",
                "blockers": ["Validated COMET core payload has not yet been generated."],
                "arms": {}, "grid": None, "views": {}}
    audit_path = root / "outputs/comet_core/asset_audit.json"
    audit = json.loads(audit_path.read_text()) if audit_path.is_file() else {}
    snapshot = audit.get("saved_app_snapshot", {})
    check = snapshot.get("alignment_check", {})
    source = check.get("source_path") or check.get("path")
    if source:
        # The copied reference belongs to this project. The recorded original
        # path remains provenance and may refer to a different computer. Prefer
        # the local copy, but reject changed pixels rather than silently falling
        # back to an available historical file.
        local_reference = root / "outputs/comet_core/figures/alignment_check_reference.png"
        image_path = local_reference if local_reference.is_file() else Path(source)
        if not image_path.is_absolute():
            image_path = root / image_path
        raw = image_path.read_bytes()
        expected = check.get("sha256")
        digest = hashlib.sha256(raw).hexdigest()
        if expected and expected != digest:
            raise ValueError("Saved alignment-check image hash changed")
        check["sha256"] = digest
        check["embedded_data_url"] = "data:image/png;base64," + base64.b64encode(raw).decode("ascii")
    for kind in ("reference", "reproduced"):
        figure = root / ("outputs/comet_core/figures/alignment_check_%s.png" % kind)
        if figure.is_file():
            raw_figure = figure.read_bytes()
            if hashlib.sha256(raw_figure).hexdigest() == check.get("sha256"):
                check[kind + "_matches_reference"] = True
            else:
                check[kind + "_data_url"] = "data:image/png;base64," + base64.b64encode(raw_figure).decode("ascii")
            check[kind + "_sha256"] = hashlib.sha256(raw_figure).hexdigest()
    svg_path = root / "outputs/comet_core/figures/alignment_check_reproduced.svg"
    if svg_path.is_file():
        check["reproduced_svg_data_url"] = "data:image/svg+xml;base64," + base64.b64encode(svg_path.read_bytes()).decode("ascii")
    validation_path = root / "outputs/comet_core/alignment_replay_validation.json"
    replay_validation = json.loads(validation_path.read_text()) if validation_path.is_file() else {}
    replay_verified = (
        replay_validation.get("pixel_identical_to_saved_reference") is True
        and replay_validation.get("transforms_unchanged") is True
        and replay_validation.get("reference_sha256") == check.get("sha256")
        and replay_validation.get("reproduced_png_sha256") == check.get("reproduced_sha256")
        and check.get("reproduced_matches_reference") is True
    )
    cohort_path = root / "metadata/cohort_selection.json"
    cohort = json.loads(cohort_path.read_text()) if cohort_path.is_file() else {}
    questions_path = root / "docs/scientist_questions.md"
    questions = questions_path.read_text() if questions_path.is_file() else ""
    selected_by_job = {str(section.get("job")): section for section in cohort.get("sections", [])}
    matched_sections = [section for section in snapshot.get("sections", [])
                        if selected_by_job.get(str(section.get("job")), {}).get("source", {}).get("sha256")
                        == section.get("source_sha256") and section.get("source_sha256")]
    selected_cohort_verified = (
        len(cohort.get("sections", [])) == 12
        and len(matched_sections) == 12
        and cohort.get("fresh_folder_inventory", {}).get("all13csv_hashes_match_historical_manifest") is True
    )
    exploratory = load_exploratory(root)
    multiresolution = load_multiresolution(root)
    measurement_features = ensure_spatial_feature_cache(root, multiresolution.get("pla_points", []))
    feature_pointer=root/'outputs/measurement_features/latest_run.json'
    feature_payload_sha256=json.loads(feature_pointer.read_text()).get('payload_sha256') if measurement_features else None
    context_geometry = build_context_geometry(multiresolution)
    if context_geometry:
        context_path=root/'outputs/comet_core/context_geometry.json'
        context_path.parent.mkdir(parents=True,exist_ok=True)
        context_path.write_text(json.dumps(context_geometry,separators=(',',':'),allow_nan=False))
    review_figures = []
    review_directory = root / "outputs/comet_core/detailed_review"
    review_manifest = review_directory / "manifest.json"
    if review_manifest.is_file() and multiresolution.get("saved_payload_path"):
        review = json.loads(review_manifest.read_text())
        current_hash = hashlib.sha256(Path(multiresolution["saved_payload_path"]).read_bytes()).hexdigest()
        if review.get("source_payload_sha256") == current_hash:
            for figure in review.get("figures", []):
                image = review_directory / figure["png"]
                raw = image.read_bytes()
                review_figures.append({**figure, "filename": image.name,
                    "data_url": "data:image/png;base64," + base64.b64encode(raw).decode("ascii"),
                    "sha256": hashlib.sha256(raw).hexdigest()})
    data = {"core": core, "exploratory": exploratory, "multiresolution": multiresolution, "saved_alignment": snapshot,
            "cohort_selection": cohort, "selected_cohort_verified": selected_cohort_verified,
            "scientist_questions": questions, "review_figures": review_figures,
            "measurement_features": measurement_features,
            "measurement_feature_payload_sha256": feature_payload_sha256,
            "context_geometry": context_geometry,
            "alignment_replay_validation": {**replay_validation, "display_claim_verified": replay_verified},
            "asset_audit": {k: v for k, v in audit.items() if k != "saved_app_snapshot"}}
    encoded = json.dumps(data, ensure_ascii=False, allow_nan=False,
                         separators=(",", ":")).replace("<", "\\u003c")
    source = (Path(__file__).parent / "comet_core_explorer.html").read_text()
    # Independent modules are embedded before the core script and need no network.
    source=source.replace('<script id="comet-measurement-engine-js">__MEASUREMENT_ENGINE_JS__</script>',
        '<script id="comet-measurement-engine-js">__MEASUREMENT_ENGINE_JS__</script><script id="comet-vector-export-js">__VECTOR_EXPORT_JS__</script><script id="comet-detail-grid-js">__DETAIL_GRID_JS__</script>')
    page = source.replace("__PLOTLY__", get_plotlyjs()).replace("__PAYLOAD__", encoded)
    # Embed the local review renderers so the exported app remains fully offline.
    # These modules reuse saved numerical payloads; they never recalculate counts
    # or change the frozen section transforms.
    for token, filename in (("__MEASUREMENT_ENGINE_JS__", "comet_measurements.js"),
                            ("__VECTOR_EXPORT_JS__", "comet_vector_export.js"),
                            ("__DETAIL_GRID_JS__", "comet_detail_grid.js"),
                            ("__MEASUREMENT_CONTROLS_JS__", "comet_measurement_controls.js"),
                            ("__PLOT_LIFECYCLE_JS__", "comet_plot_lifecycle.js"),
                            ("__SUPPORT_DETAIL_JS__", "comet_support_detail.js"),
                            ("__ALIGNMENT_DETAIL_JS__", "comet_alignment_detail.js")):
        if token in page:
            page = page.replace(token, (Path(__file__).parent / filename).read_text())
    output = root / "outputs/app/index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page)
    current_resolution = multiresolution.get("resolutions", {}).get(str(multiresolution.get("default_resolution", 100)), {})
    current_status = current_resolution.get("status") or exploratory.get("status") or core["status"]
    return {"path": str(output), "bytes": output.stat().st_size,
            "status": current_status, "strict_pdf_status": core["status"], "saved_alignment_sections": len(snapshot.get("sections", [])),
            "resolutions": sorted(multiresolution.get("resolutions", {}), key=int)}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
