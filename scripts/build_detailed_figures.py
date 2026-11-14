"""Export unsmoothed multiresolution maps and exact object reconstructions."""
from pathlib import Path
import csv
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "tmp/matplotlib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
import numpy as np

ARMS = ("HK1", "PFKP")
CONDITIONS = ("Homecage", "Running")
NOTE = ("EXPLORATORY · bounding-box midpoints · unchanged fixed transforms · uncalibrated export units\n"
        "Observed PLA/ChAT support is data-dependent, not complete tissue coverage. No smoothing, interpolation or tests.")


def build(run_directory):
    run = Path(run_directory)
    index = json.loads((run / "index.json").read_text())
    results = {}
    for width, item in index["resolutions"].items():
        filename = item["payload_file"] if isinstance(item, dict) else item
        results[str(width)] = json.loads((run / filename).read_text())
    if any(p.get("strict_pdf_results") is not False for p in results.values()):
        raise ValueError("Detailed figures require explicitly exploratory payloads")
    out = run / "figures"
    out.mkdir(exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "svg.fonttype": "none"})
    signed = plt.get_cmap("RdBu_r").copy(); signed.set_bad("#d7dfe6")
    counts = plt.get_cmap("cividis").copy(); counts.set_bad("#d7dfe6")
    ns = ListedColormap(["#eff3f6", "#b8d5e7", "#5b9cc6", "#164f7c"])
    nnorm = BoundaryNorm(np.arange(-.5, 4.5), 4)
    manifest = []
    summary = []

    def frame(fig, title):
        fig.suptitle(title, x=.06, ha="left", y=.985, fontsize=19, weight="bold", color="#19354a")
        fig.text(.06, .94, "Actual raw objects · same recorded extent · linear scales", fontsize=10, color="#567183")
        fig.text(.06, .025, NOTE, fontsize=9, linespacing=1.6, color="#567183")

    def axes(ax, p):
        xe, ye = p["grid"]["x_edges"], p["grid"]["y_edges"]
        ax.set(xlim=(xe[0], xe[-1]), ylim=(ye[-1], ye[0]), xlabel="Aligned X · export units", ylabel="Aligned Y · export units")
        ax.set_aspect("equal"); ax.tick_params(labelsize=8)
        ax.ticklabel_format(style="plain", axis="both", useOffset=False)
        for spine in ax.spines.values(): spine.set_visible(False)

    def mesh(ax, p, values, **kw):
        result = ax.pcolormesh(p["grid"]["x_edges"], p["grid"]["y_edges"],
            np.ma.masked_invalid(np.asarray(values, float)), shading="flat", rasterized=True, **kw)
        axes(ax, p)
        return result

    def save(fig, name, caption):
        for ext in ("png", "svg"):
            fig.savefig(out / (name + "." + ext), dpi=300, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        manifest.append({"id": name, "path": "figures/" + name + ".png", "svg_path": "figures/" + name + ".svg", "dpi": 300,
                         "caption": caption, "strict_pdf_results": False})

    for width in ("1000", "500", "250", "100"):
        p = results[width]
        for arm in ARMS:
            a = p["arms"][arm]; z = np.asarray(a["difference"], float)
            hn, rn = np.asarray(a["homecage_n"]), np.asarray(a["running_n"])
            summary.append({"width_export_units": int(width), "arm": arm,
                "grid_rows": len(z), "grid_columns": len(z[0]), "grid_bins": z.size,
                "comparable_bins": int(np.isfinite(z).sum()),
                "both_conditions_observed_N3_bins": int(((hn == 3) & (rn == 3)).sum()),
                "signed_scale_limit": p["color_scale"]["cmax"],
                "minimum_difference": float(np.nanmin(z)), "maximum_difference": float(np.nanmax(z)),
                "scope": "Descriptive correlated bins, not biological replication or tissue coverage"})

    for width in ("250", "100"):
        p = results[width]; limit = p["color_scale"]["cmax"]
        fig, axs = plt.subplots(1, 2, figsize=(16, 10))
        fig.subplots_adjust(left=.065, right=.88, top=.87, bottom=.15, wspace=.25)
        frame(fig, f"Detailed PLA differences · {width}-unit bins")
        for ax, arm in zip(axs, ARMS):
            a = p["arms"][arm]; z = np.asarray(a["difference"], float)
            im = mesh(ax, p, z, cmap=signed, vmin=-limit, vmax=limit)
            ax.set_title(f"TDP43–{arm}\nRunning − Homecage · {np.isfinite(z).sum():,} comparable bins", fontsize=12, pad=12)
        cb = fig.add_axes([.91, .24, .015, .52])
        fig.colorbar(im, cax=cb, label="Difference in observed-support mean PLA count / bin")
        save(fig, "detailed_differences_" + width,
             f"Two separate arms on a shared symmetric linear scale at {width} export-unit resolution. Grey is unavailable support, white is a zero difference. No image pixels or physical calibration are claimed.")

    p = results["100"]; display_limit = 25
    fig, axs = plt.subplots(1, 2, figsize=(16, 10))
    fig.subplots_adjust(left=.065, right=.88, top=.84, bottom=.15, wspace=.25)
    frame(fig, "Fine-bin detail · fixed display range ±25 counts")
    fig.text(.06, .90, "100-unit bins · values beyond ±25 use endpoint colors · full-range figures and exact arrays retained", fontsize=10, color="#8a5927")
    for ax, arm in zip(axs, ARMS):
        z = np.asarray(p["arms"][arm]["difference"], float)
        clipped = int((np.abs(z[np.isfinite(z)]) > display_limit).sum())
        im = mesh(ax, p, z, cmap=signed, vmin=-display_limit, vmax=display_limit)
        ax.set_title(f"TDP43–{arm} · Running − Homecage\n{clipped:,} of {np.isfinite(z).sum():,} bins beyond displayed range", fontsize=11, pad=12)
    cb = fig.add_axes([.91, .24, .015, .52])
    fig.colorbar(im, cax=cb, extend="both", label="Difference in observed-support mean PLA count / bin")
    save(fig, "fine_detail_contrast_100",
         "Supplementary linear signed detail view, both arms fixed to ±25 counts; out-of-range values saturate at the endpoints. Counts, missingness and means are unchanged. Use full-range figures or numerical arrays for uncapped magnitudes.")

    fig, axs = plt.subplots(2, 4, figsize=(21, 13))
    fig.subplots_adjust(left=.05, right=.96, top=.87, bottom=.15, wspace=.4, hspace=.38)
    frame(fig, "Resolution sensitivity · finer bins change counts and observed support")
    for col, width in enumerate(("1000", "500", "250", "100")):
        p = results[width]; limit = p["color_scale"]["cmax"]
        for row, arm in enumerate(ARMS):
            im = mesh(axs[row, col], p, p["arms"][arm]["difference"], cmap=signed, vmin=-limit, vmax=limit)
            axs[row, col].set_title(f"{arm} · {width} units\nlinear scale ±{limit:,.2f}", fontsize=11)
            fig.colorbar(im, ax=axs[row, col], orientation="horizontal", shrink=.85, pad=.19, fraction=.035)
    save(fig, "resolution_sensitivity",
         "Each column uses freshly recounted raw objects. Both arms share a symmetric scale within each column; scale limits and bin areas differ between columns. Changes do not measure an effect at a fixed physical scale.")

    p = results["100"]
    commonmax = max(np.nanmax(np.asarray(p["arms"][arm][key], float)) for arm in ARMS for key in ("homecage_mean", "running_mean"))
    for kind in ("means", "support"):
        fig, axs = plt.subplots(2, 2, figsize=(14, 14))
        fig.subplots_adjust(left=.08, right=.85, top=.88, bottom=.13, wspace=.27, hspace=.28)
        frame(fig, "Detailed condition means · 100-unit bins" if kind == "means" else "Detailed observed-section support · 100-unit bins")
        for row, arm in enumerate(ARMS):
            for col, condition in enumerate(CONDITIONS):
                key = "running" if condition == "Running" else "homecage"
                values = p["arms"][arm][key + ("_mean" if kind == "means" else "_n")]
                im = mesh(axs[row, col], p, values, **({"cmap": counts, "vmin": 0, "vmax": commonmax} if kind == "means" else {"cmap": ns, "norm": nnorm}))
                axs[row, col].set_title(f"TDP43–{arm} · {condition}", fontsize=12)
        cb = fig.add_axes([.90, .23, .015, .52])
        fig.colorbar(im, cax=cb, **({"label": "Mean raw PLA count / observed-support bin"} if kind == "means" else {"label": "Sections with ≥1 PLA or ChAT object (N observed)", "ticks": range(4)}))
        save(fig, "detailed_" + kind + "_100",
             "100-export-unit raw means with one common linear sequential scale." if kind == "means" else "Four observed-object-support maps with identical integer N=0–3 scale; no tissue mask is available. Finer bins are sparser.")

    sectionmax = max(np.asarray(s["pla_counts"]).max() for s in p["sections"])
    for arm in ARMS:
        sections = sorted([s for s in p["sections"] if s["pla_type"] == arm], key=lambda s: (CONDITIONS.index(s["condition"]), s["animal_id"]))
        fig, axs = plt.subplots(2, 3, figsize=(17, 13))
        fig.subplots_adjust(left=.06, right=.89, top=.87, bottom=.13, wspace=.27, hspace=.28)
        frame(fig, f"Individual section PLA counts · TDP43–{arm} · 100-unit bins")
        for ax, s in zip(axs.flat, sections):
            values = np.where(np.asarray(s["observed_support"]), np.asarray(s["pla_counts"]), np.nan)
            im = mesh(ax, p, values, cmap=counts, vmin=0, vmax=sectionmax)
            ax.set_title(f"{s['animal_id']} · {s['condition']}\n{s['pla_objects']:,} PLA objects", fontsize=11)
        cb = fig.add_axes([.93, .23, .012, .52]); fig.colorbar(im, cax=cb, label="Raw PLA detections per section-bin")
        save(fig, "individual_sections_" + arm.lower() + "_100",
             "Six individual physical sections, not a pooled group. Both arm atlases share one raw-count scale. ChAT-only observed bins retain PLA=0; grey means no exported objects.")

    with (run / "resolution_summary.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary[0])); writer.writeheader(); writer.writerows(summary)
    result = {"figures": manifest, "strict_pdf_results": False,
              "resolution_summary": summary,
              "scale_policy": "Same symmetric linear signed scale across arms within each resolution; count magnitudes and limits are not comparable across resolutions."}
    (run / "detailed_figure_manifest.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/build_detailed_figures.py MULTIRESOLUTION_RUN_DIRECTORY")
    print(json.dumps(build(sys.argv[1]), indent=2))
