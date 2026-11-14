"""Connect a verified numerical run and the frozen alignment review to the app.

This presentation build never fits transforms or fabricates missing matrices.
Use --run to select a completed numerical snapshot after resolving its inputs.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from comet_spatial.core_view import build_core_view_payload
from comet_spatial.manifest import preflight_manifest


def build(root=ROOT, run_directory=None):
    root = Path(root)
    from scripts.build_comet_workflow import build as build_workflow
    build_workflow(root)
    manifest = root / "metadata/analysis_manifest.json"
    preflight = preflight_manifest(manifest)
    (root / "outputs/preflight.json").write_text(json.dumps(preflight, indent=2) + "\n")
    intake = json.loads(manifest.read_text())
    # Preserve every field diagnostic on disk; present the scientific causes
    # once rather than repeating missing columns/masks for all twelve sections.
    viewer_preflight = preflight
    if preflight["status"] != "ready" and intake.get("pending_inputs"):
        viewer_preflight = {**preflight, "blockers": [
            item["required"] + " " + item["why"] for item in intake["pending_inputs"]],
            "detailed_diagnostics_file": "outputs/preflight.json"}
    payload = build_core_view_payload(run_directory, manifest_base_dir=manifest.parent,
                                      preflight=viewer_preflight)
    out = root / "outputs/core_view"
    out.mkdir(parents=True, exist_ok=True)
    (out / "payload.json").write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    from scripts.build_comet_core_explorer import build as build_viewer
    viewer = build_viewer(root)
    return {"status": viewer["status"], "strict_pdf_status": payload["status"],
            "core_status": payload["status"], "viewer": viewer}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, help="Explicit immutable outputs/spatial run folder")
    args = parser.parse_args()
    print(json.dumps(build(run_directory=args.run), indent=2))
