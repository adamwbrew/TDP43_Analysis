"""Replay the former six-panel check using saved geometry and fixed transforms.

This renders the old occupancy-outline display; it never supplies a tissue mask,
fits alignment, or assigns the historical cohort to the new experiment.
"""
import hashlib
import importlib.metadata
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "tmp/matplotlib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from comet_spatial.alignment_replay import alignment_figure, style, transform_xy


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build(root=ROOT):
    root = Path(root)
    snapshot_path = root / "outputs/comet_core/alignment_snapshot.json"
    snapshot = json.loads(snapshot_path.read_text())
    sections = snapshot["sections"]
    geometry = {s["job"]: {k: np.asarray(v) if isinstance(v, list) else v
                           for k, v in s["alignment_figure_geometry_grid"].items()}
                for s in sections}
    # Check both independent implementations of every saved transformation.
    for section in sections:
        g = geometry[section["job"]]
        points = np.array([[g["x_edges"][0], g["y_edges"][0]],
                           [g["x_edges"][-1], g["y_edges"][-1]],
                           section["saved_center"]])
        direct = transform_xy(points, section["saved_center"], section["saved_flip"])[1]
        affine = np.c_[points, np.ones(len(points))] @ np.asarray(section["fixed_transform_matrix"]).T
        if not np.allclose(direct, affine[:, :2], rtol=0, atol=1e-10):
            raise ValueError("Saved transformation replay differs: " + section["job"])
    out = root / "outputs/comet_core/figures"
    out.mkdir(parents=True, exist_ok=True)
    reference = Path(snapshot["alignment_check"]["source_path"])
    target_reference = out / "alignment_check_reference.png"
    if reference.exists():
        if sha(reference) != snapshot["alignment_check"]["sha256"]:
            raise ValueError("Historical alignment reference changed")
        shutil.copy2(reference, target_reference)
    elif not target_reference.exists() or sha(target_reference) != snapshot["alignment_check"]["sha256"]:
        raise FileNotFoundError("Original alignment-check reference unavailable")
    plt.rcdefaults()
    style()
    fig = alignment_figure(geometry, [s["proposed"] for s in sections])
    for ext in ("png", "svg"):
        fig.savefig(out / ("alignment_check_reproduced." + ext), dpi=300, bbox_inches="tight")
    plt.close(fig)
    original = np.asarray(Image.open(target_reference).convert("RGBA"))
    replay = np.asarray(Image.open(out / "alignment_check_reproduced.png").convert("RGBA"))
    same_shape = original.shape == replay.shape
    validation = {
        "status": "saved_alignment_replayed_without_refitting",
        "sections": len(sections), "transforms_unchanged": True,
        "all_fixed_matrices_match_former_transform_formula": True,
        "geometry": "Original saved 250-unit object-occupancy grids; identical former boundary display renderer. Not a tissue mask.",
        "scientific_scope": "Former 12-section alignment snapshot. Four current inputs match its source bytes; current cohort is not inferred.",
        "anatomical_acceptance": "PDF says reuse accepted alignment; former snapshot metadata still label these transforms proposed. This replay does not change either record.",
        "snapshot_sha256": sha(snapshot_path),
        "reference_sha256": sha(target_reference),
        "reproduced_png_sha256": sha(out / "alignment_check_reproduced.png"),
        "renderer_sha256": sha(root / "comet_spatial/alignment_replay.py"),
        "reference_pixel_shape": list(original.shape),
        "reproduced_pixel_shape": list(replay.shape),
        "pixel_identical_to_saved_reference": bool(same_shape and np.array_equal(original, replay)),
        "pixel_comparison_note": "Rendering-library/font versions can change pixels without changing saved geometry or transforms.",
        "versions": {p: importlib.metadata.version(p) for p in ("numpy", "matplotlib", "scipy", "Pillow")},
        "figure_files": ["figures/alignment_check_reference.png", "figures/alignment_check_reproduced.png", "figures/alignment_check_reproduced.svg"],
    }
    cohort_path = root / "metadata/cohort_selection.json"
    if cohort_path.is_file():
        cohort = json.loads(cohort_path.read_text())
        validation.update(
            cohort_selection_sha256=sha(cohort_path),
            selected_current_sections=len(cohort["sections"]),
            scientific_scope="The user selected these twelve completed former-app sections. "
                             "Current expanded copies match their saved source hashes; "
                             "initial eight-file audit matches remain separate provenance. "
                             "No new count contrast or mask is inferred by this replay.",
        )
    (root / "outputs/comet_core/alignment_replay_validation.json").write_text(json.dumps(validation, indent=2) + "\n")
    return validation


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
