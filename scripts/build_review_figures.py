"""High-resolution review figures from validated saved arrays and PLA positions."""
from pathlib import Path
from hashlib import sha256
import json
import os

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "tmp/matplotlib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
import numpy as np

SUPPORT_COLORS = ["#eef2f6", "#c49a55", "#4c9b9b", "#143e68"]
ORDER = ["21F", "23M", "24M", "22F", "21M", "22M"]
COLORS = ["#2675ac", "#388d79", "#6472b5", "#bc8b32", "#a45d37", "#bd657e"]


def build(root=ROOT):
    root = Path(root)
    pointer_path = root / "outputs/section_means/latest_run.json"
    if not pointer_path.is_file():
        pointer_path = root / "outputs/exploratory_multiresolution/latest_run.json"
    pointer = json.loads(pointer_path.read_text())
    recorded = Path(pointer["run_directory"])
    local = pointer_path.parent / recorded.name
    run = local if local.is_dir() else recorded
    path = run / "view_payload.json"
    data = json.loads(path.read_text())
    checks = data["validation"]
    if not all(checks.get(k) is True for k in ("count_conservation_all_resolutions", "fixed_transforms_unchanged", "full_pla_point_count_matches_raw")):
        raise ValueError("Saved multiresolution validation is incomplete")
    if sum(len(p["x"]) for p in data["pla_points"]) != checks["full_pla_point_count"]:
        raise ValueError("PLA cache no longer matches validated source count")
    p = data["resolutions"]["100"]
    if p["strict_pdf_results"] is not False:
        raise ValueError("These review figures require the separate exploratory data")
    out = root / "outputs/comet_core/detailed_review"
    out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "svg.fonttype": "none"})
    xe, ye = np.asarray(p["grid"]["x_edges"]), np.asarray(p["grid"]["y_edges"])
    manifest = []
    note = ("RECONSTRUCTED OBJECT MAPS · unchanged saved alignment · tissue coverage uncertain\n"
            "Observed-object support is not a tissue mask. PLA dots are bounding-box midpoint proxies, not fluorescence pixels.")

    def axes(ax):
        ax.set(xlim=(xe[0], xe[-1]), ylim=(ye[-1], ye[0]))
        ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_visible(False)

    def frame(fig, title):
        fig.suptitle(title, x=.055, ha="left", y=.98, fontsize=19, weight="bold", color="#19354a")
        fig.text(.055, .93, "Full selected object data · separate sections and arms · no smoothing or refitting", fontsize=10, color="#567183")
        fig.text(.055, .025, note, fontsize=9, linespacing=1.6, color="#567183")

    def save(fig, name, caption):
        for ext in ("png", "svg"):
            fig.savefig(out / (name + "." + ext), dpi=600, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        from PIL import Image
        with Image.open(out / (name + '.png')) as image:
            dimensions = list(image.size)
        manifest.append({"id": name, "png": name + ".png", "svg": name + ".svg", "dpi": 600, "pixel_dimensions": dimensions, "caption": caption})

    cmap = ListedColormap(SUPPORT_COLORS); norm = BoundaryNorm(np.arange(-.5, 4.5), 4)
    fig, axs = plt.subplots(2, 2, figsize=(15, 14))
    fig.subplots_adjust(left=.07, right=.86, top=.86, bottom=.13, wspace=.22, hspace=.29)
    frame(fig, "Detailed observed-section support · 100-unit bins")
    for row, arm in enumerate(("HK1", "PFKP")):
        for col, condition in enumerate(("Homecage", "Running")):
            key = "homecage_n" if condition == "Homecage" else "running_n"
            n = np.asarray(p["arms"][arm][key])
            im = axs[row, col].pcolormesh(xe, ye, n, cmap=cmap, norm=norm, shading="flat", rasterized=True)
            axes(axs[row, col]); axs[row, col].set_title(f"TDP43–{arm} · {condition}\n{int((n == 3).sum()):,} bins with all three sections observed", fontsize=11, pad=10)
    cb = fig.add_axes([.91, .23, .014, .52])
    bar = fig.colorbar(im, cax=cb, ticks=range(4))
    bar.set_label("Sections with ≥1 exported PLA or ChAT object (N)")
    save(fig, "observed_support_detail_100", "Categorical N=0,1,2,3 with four discrete colors. N=0 means no exported object support; N=3 does not establish full-bin tissue coverage.")

    by_section = {s["section_id"]: s for s in p["sections"]}
    for arm in ("HK1", "PFKP"):
        points = sorted([r for r in data["pla_points"] if r["pla_type"] == arm], key=lambda r: ORDER.index(r["animal_id"]))
        fig, axs = plt.subplots(2, 3, figsize=(18, 13))
        fig.subplots_adjust(left=.06, right=.97, top=.86, bottom=.13, wspace=.25, hspace=.28)
        frame(fig, f"Saved alignment in detail · TDP43–{arm} · all PLA object locations")
        for ax, record in zip(axs.flat, points):
            section = by_section[record["section_id"]]
            support = np.asarray(section["observed_support"], int)
            ax.pcolormesh(xe, ye, support, cmap=ListedColormap(["#f4f6f8", "#dce6ed"]), vmin=0, vmax=1, shading="flat", rasterized=True)
            if len(record["x"]) != section["pla_objects"] or record.get("sampled") is not False:
                raise ValueError("Individual section points are incomplete or sampled")
            ax.scatter(record["x"], record["y"], s=.35, color=COLORS[ORDER.index(record["animal_id"])], linewidths=0, alpha=.8, rasterized=True)
            axes(ax); ax.set_title(f"{record['animal_id']} · {record['condition']}\n{len(record['x']):,} exact PLA midpoint proxies", fontsize=11, pad=10)
        save(fig, "alignment_detail_" + arm.lower(), "Six individual sections, Homecage above Running, in the unchanged saved frame. All selected PLA positions are drawn over faint observed PLA/ChAT-bin footprints. Footprints do not establish tissue boundaries.")

    result = {"source_payload": str(path), "source_payload_sha256": sha256(path.read_bytes()).hexdigest(),
              "source_objects": checks["source_totals"], "full_pla_point_count": checks["full_pla_point_count"],
              "strict_pdf_results": False, "presentation_only": True,
              "support_colors_N_0_1_2_3": SUPPORT_COLORS, "figures": manifest}
    (out / "manifest.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
