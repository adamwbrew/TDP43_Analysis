"""Assemble the offline native-coordinate atlas from saved, verified payloads.

No raw analysis or metadata inference occurs here. The browser never requests a
network resource; both the Plotly runtime and saved measurements are embedded.
"""
from pathlib import Path
import json
import base64
from plotly.offline import get_plotlyjs

ROOT = Path(__file__).resolve().parents[1]


def build(root=ROOT):
    root = Path(root)
    source = root / "outputs/native_atlas/payload.json"
    payload = json.loads(source.read_text())
    if not payload.get("exports"):
        raise ValueError("Native atlas has no exports")
    context_path = root / "outputs/native_atlas/historical_context.json"
    historical = json.loads(context_path.read_text()) if context_path.exists() else {}
    for figure in historical.get("figures", []):
        relative = figure.get("path")
        if relative:
            image = root / relative
            if not image.is_file():
                raise FileNotFoundError("Historical figure missing: %s" % image)
            figure["embedded_data_url"] = "data:image/png;base64," + base64.b64encode(image.read_bytes()).decode("ascii")
    display = {
        "scope": "Display-only starting values for the saved native atlas; no effect on raw analysis or biological inclusion.",
        "default_export": "input_004",
        "default_metric": "PLA detections per bin",
        "default_view": "2D native map",
        "bin_width_native_units": 128,
        "count_colour_transform": "log(1 + raw count)",
        "count_colour_palette": "Magma-style sequential scale for PLA; amber for ChAT; shared class/bin limits; zero-count bins blank with unknown tissue status",
        "minimum_PLA_per_association_bin": 10,
        "minimum_support_interpretation": "Interactive display filter for a descriptive fraction; not a validated cutoff or transferred historical parameter.",
        "overlay_PLA_marker_size": 2.5,
        "overlay_ChAT_marker_size_multiplier": 0.68,
        "overlay_opacity": 0.65,
        "coordinate_display": "Native Y increases downward; units and anatomical orientation unverified.",
        "scale_policy": "Identical colour limits across all exports for each object class, bin width and transform.",
        "point_sampling": "Use the deterministic samples recorded in the native-atlas analysis payload; all eligible rows feed count maps.",
    }
    (root / "metadata/explorer_display_parameters.json").write_text(json.dumps(display, indent=2) + "\n")
    manifest = json.loads((root / "metadata/input_manifest.json").read_text())
    audit = json.loads((root / "outputs/inventory/file_audit.json").read_text())
    inventory = json.loads((root / "outputs/inventory/summary.json").read_text())
    data = {"atlas": payload, "historical": historical, "manifest": manifest,
            "audit": audit, "inventory": inventory}
    encoded = json.dumps(data, ensure_ascii=False, allow_nan=False,
                         separators=(",", ":")).replace("<", "\\u003c")
    template = (Path(__file__).parent / "spatial_explorer.html").read_text()
    result = template.replace("__PLOTLY__", get_plotlyjs()).replace("__PAYLOAD__", encoded)
    out = root / "outputs/app/native_explorer.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(result)
    return {"path": str(out), "bytes": out.stat().st_size,
            "exports": len(payload["exports"]), "network_required": False}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
