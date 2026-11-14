"""Scientific reading guide and figures for observed exports, not group inference."""
from pathlib import Path
import json
import os

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "tmp/matplotlib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def build(root=ROOT):
    root = Path(root)
    atlas = json.loads((root / "outputs/native_atlas/payload.json").read_text())
    audit = json.loads((root / "outputs/inventory/file_audit.json").read_text())
    manifest = {m["file_id"]: m for m in json.loads((root / "metadata/input_manifest.json").read_text())}
    exports = {e["file_id"]: e for e in atlas["exports"]}
    figures = root / "outputs/native_atlas/figures"
    figures.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 11, "svg.fonttype": "none"})
    rows = []
    for a in audit:
        e = exports[a["file_id"]]
        n, positive = a["pla_row_count_by_export_label"], a["pla_rows_with_chat_present_equal_1"]
        assert e["association"]["pla_total"] == n
        assert e["association"]["chat_positive"] == positive
        morphology = e["morphology"]["PLA"]
        rows.append({"file_id": a["file_id"], "job_token": str(manifest[a["file_id"]]["job_token_from_filename"]),
                     "exported_region_label": "; ".join(a["analysis_region_counts"]),
                     "pla_count": n, "chat_count": a["chat_row_count_by_export_label"],
                     "pla_with_chat_flag": positive, "pla_chat_flag_percent": 100 * positive/n,
                     "zero_minimum_diameter_pla": morphology["zero_min_diameter"],
                     "unusable_diameter_ratio_pla": morphology["ratio_excluded"],
                     "unusable_diameter_ratio_percent": 100 * morphology["ratio_excluded"]/n})
    frame = pd.DataFrame(rows)
    frame.to_csv(root / "outputs/native_atlas/export_findings.csv", index=False)

    def save(fig, name):
        for ext in ("png", "svg"):
            fig.savefig(figures / (name + "." + ext), dpi=300, bbox_inches="tight")
        plt.close(fig)

    y = np.arange(len(frame))
    labels = ["%s · job %s" % (r.file_id, r.job_token) for r in frame.itertuples()]
    fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True, layout="constrained")
    axes[0].barh(y, frame.pla_count, color="#167A87", height=.6)
    axes[0].set(yticks=y, yticklabels=labels, xlabel="PLA-labelled detections per export", title="Detected PLA count")
    axes[0].set_xlim(0, frame.pla_count.max()*1.25)
    for yy, count in zip(y, frame.pla_count):
        axes[0].text(count+frame.pla_count.max()*.02, yy, f"{count:,}", va="center", fontsize=10)
    axes[1].scatter(frame.pla_chat_flag_percent, y, s=60, color="#167A87", zorder=3)
    axes[1].set(xlim=(0, 100), xlabel="PLA with exported ChAT presence (%)", title="Association flag: denominator = all PLA")
    for yy, row in enumerate(frame.itertuples()):
        axes[1].text(row.pla_chat_flag_percent+1.8, yy, f"{row.pla_chat_flag_percent:.2f}%", va="center", fontsize=10)
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="x", alpha=.15)
    axes[0].invert_yaxis()
    fig.suptitle("Current export findings · files are overlapping analyses, not independent animals", fontsize=14)
    save(fig, "export_signal_profiles")

    overlap = pd.read_csv(root / "outputs/inventory/within_input_overlap.csv")
    paired = overlap[overlap["left_signature_shared_fraction"] > .8].copy()
    pair_rows = []
    indexed = frame.set_index("file_id")
    for o in paired.to_dict("records"):
        left, right = indexed.loc[o["left_file_id"]], indexed.loc[o["right_file_id"]]
        pair_rows.append({"left_file_id": o["left_file_id"], "right_file_id": o["right_file_id"],
                          "left_job_token": left.job_token, "right_job_token": right.job_token,
                          "left_pla": int(left.pla_count), "right_pla": int(right.pla_count),
                          "right_minus_left_pla_count": int(right.pla_count-left.pla_count),
                          "pla_count_relative_change_percent": 100*(right.pla_count-left.pla_count)/left.pla_count,
                          "left_chat_flag_percent": float(left.pla_chat_flag_percent),
                          "right_chat_flag_percent": float(right.pla_chat_flag_percent),
                          "right_minus_left_association_percentage_points": float(right.pla_chat_flag_percent-left.pla_chat_flag_percent),
                          "left_distinct_measurements_shared_percent": 100*o["left_signature_shared_fraction"],
                          "right_distinct_measurements_shared_percent": 100*o["right_signature_shared_fraction"],
                          "interpretation": "Pair selected by measurement agreement; section/ROI/rerun identity remains unresolved."})
    pair = pd.DataFrame(pair_rows)
    pair.to_csv(root / "outputs/native_atlas/overlapping_export_sensitivity.csv", index=False)
    if len(pair):
        fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True, layout="constrained")
        yy = np.arange(len(pair))
        lab = [f"job {r.left_job_token} → {r.right_job_token}" for r in pair.itertuples()]
        for ax, values, title, xlabel in [
            (axes[0], pair.pla_count_relative_change_percent, "PLA count changes across overlapping exports", "Relative count change (%) · denominator = left export"),
            (axes[1], pair.right_minus_left_association_percentage_points, "ChAT presence fraction changes", "Right − left association (percentage points)")]:
            ax.axvline(0, color="#788994", lw=.9)
            ax.hlines(yy, 0, values, color="#BCCCD2", lw=3)
            ax.scatter(values, yy, s=65, color="#167A87", zorder=3)
            padding=max(abs(values).max()*.24, .35)
            ax.set_xlim(min(0,values.min())-padding, max(0,values.max())+padding)
            for yvalue, value in zip(yy, values):
                ax.annotate(f"{value:+.2f}", (value,yvalue), xytext=(0,10), textcoords="offset points", ha="center", fontsize=10)
            ax.set(xlabel=xlabel, title=title, yticks=yy, yticklabels=lab)
            ax.spines[["top","right"]].set_visible(False)
            ax.grid(axis="x",alpha=.15)
        axes[0].invert_yaxis()
        fig.suptitle("Alternative-export review · paired by shared measurements, never a condition contrast", fontsize=14)
        save(fig, "overlapping_export_sensitivity")

    fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True, layout="constrained")
    for yy, row in enumerate(frame.itertuples()):
        area = exports[row.file_id]["morphology"]["PLA"]["area"]
        probabilities = np.asarray(area["quantile_probabilities"])
        quantiles = np.asarray(area["quantiles"])
        def q(p):
            matches=np.flatnonzero(np.isclose(probabilities,p))
            if not len(matches):
                raise ValueError(f"Required area quantile {p} absent")
            return float(quantiles[matches[0]])
        axes[0].hlines(yy,q(.01),q(.99),color="#BCCCD2",lw=1.2)
        axes[0].hlines(yy,q(.25),q(.75),color="#167A87",lw=5)
        axes[0].scatter([q(.5)],[yy],color="#152F40",s=26,zorder=3)
    axes[0].set_xscale("log")
    axes[0].set(yticks=y,yticklabels=labels,xlabel="PLA area (µm² in export header; calibration unverified)",title="PLA size: median, IQR and 1st–99th percentiles")
    axes[1].barh(y,frame.unusable_diameter_ratio_percent,color="#B1682B",height=.6)
    axes[1].set_xlim(0,max(5,frame.unusable_diameter_ratio_percent.max()*1.28))
    for yy,row in enumerate(frame.itertuples()):
        axes[1].text(row.unusable_diameter_ratio_percent+.35,yy,f"{row.unusable_diameter_ratio_percent:.1f}% · {row.unusable_diameter_ratio_pla:,}",va="center",fontsize=9)
    axes[1].set(xlabel="PLA excluded from diameter-ratio summaries (%)",title="Shape measurement quality, not signal exclusion")
    for ax in axes:
        ax.spines[["top","right"]].set_visible(False)
        ax.grid(axis="x",alpha=.15)
    axes[0].invert_yaxis()
    fig.suptitle("Morphology audit · distributions use all eligible export objects, not the displayed sample",fontsize=14)
    save(fig,"export_morphology_quality")

    facts={"scope":"Descriptive export-level findings only; no Running/Homecage inference or new alignment.",
           "exports":len(frame),"pla_rows_including_overlapping_analyses":int(frame.pla_count.sum()),
           "association_flag_percent_range":[float(frame.pla_chat_flag_percent.min()),float(frame.pla_chat_flag_percent.max())],
           "candidate_overlapping_export_pairs":len(pair),
           "pla_count_relative_change_percent_range": [float(pair.pla_count_relative_change_percent.min()),float(pair.pla_count_relative_change_percent.max())],
           "association_change_percentage_point_range":[float(pair.right_minus_left_association_percentage_points.min()),float(pair.right_minus_left_association_percentage_points.max())],
           "zero_minimum_diameter_pla_including_repeats":int(frame.zero_minimum_diameter_pla.sum()),
           "unusable_diameter_ratio_pla_including_repeats":int(frame.unusable_diameter_ratio_pla.sum()),
           "unusable_diameter_ratio_percent_range":[float(frame.unusable_diameter_ratio_percent.min()),float(frame.unusable_diameter_ratio_percent.max())]}
    (root/"outputs/native_atlas/findings.json").write_text(json.dumps(facts,indent=2)+"\n")
    parameters={"candidate_pair_display_rule":"left fraction of distinct shared exported measurement signatures > 0.8; selected for review, not proof of section identity",
                "area_distribution_intervals":[0.01,0.25,0.5,0.75,0.99],
                "area_intervals_meaning":"Object distribution quantiles, not confidence intervals or animal uncertainty",
                "count_change_denominator":"PLA count of left export in each displayed pair",
                "association_change_units":"Percentage points, right export minus left export",
                "association_denominator":"All PLA-labelled rows of each export; no morphology exclusions",
                "condition_aggregation":False,"new_clustering":False}
    (root/"metadata/descriptive_findings_parameters.json").write_text(json.dumps(parameters,indent=2)+"\n")
    lines=["# TDP43 COMET: results and visual guide","",
           "The revised report leads with real spatial reconstructions and descriptive export findings. It reuses the former project's overlays, shared scales, denominator-aware maps, source-coordinate review and scientific explanations. The eight supplied files are overlapping analyses; their labels are preserved without assigning new animals or conditions.","",
           "Open `outputs/app/index.html` for linked maps, layers, bin-size controls, 3D measurement surfaces, paired-export review and historical findings. The app is self-contained and works offline. The main notebook contains saved figures and the executed analysis.","",
           "## 1. Where are the exported PLA detections?","",
           "![Native PLA count atlas](../outputs/native_atlas/figures/native_pla_count_atlas.png)","",
           "**Question:** where do exported PLA detections concentrate within each source coordinate frame? **Read:** every panel is one export, with a shared raw-count scale at the recorded bin width. Coordinates are bounding-box midpoints in unverified native units, displayed with image y downward; no physical/anatomical orientation is inferred. **Evidence:** actual object positions and bin counts, without smoothing or mask reconstruction. **Limit:** zero detections in an export-grid bin do not establish that the bin contains tissue. **Next:** use the explorer's bin click and review targets to inspect the original fluorescence channels and segmentation.","",
           "![PLA/ChAT reconstructed layers](../outputs/native_atlas/figures/native_layer_overlay_atlas.png)","",
           "The overlay combines deterministically sampled object midpoints. The raw heatmap counts every eligible object; sample points are for display only. These are reconstructed detections, not microscopy pixels or validated tissue outlines.","",
           "## 2. What do the exports show about PLA and the ChAT presence flag?","",
           "![Signal profiles](../outputs/native_atlas/figures/export_signal_profiles.png)","",
           f"**Finding:** exported PLA ChAT-presence fractions span {facts['association_flag_percent_range'][0]:.2f}%–{facts['association_flag_percent_range'][1]:.2f}% across the eight files. Each fraction divides flagged PLA detections by all PLA detections in that export. This range spans multiple export labels/arms and repeated analyses; it is not a Running/Homecage comparison. Flagged PLA does not establish neuron identity, direct binding or enzyme activity.","",
           "## 3. Do overlapping exports produce the same measurements?","",
           "![Alternative-export review](../outputs/native_atlas/figures/overlapping_export_sensitivity.png)","",
           f"**Finding:** four pairs share roughly 91–95% of distinct measurement signatures. In the plotted right-minus-left ordering, PLA counts change {facts['pla_count_relative_change_percent_range'][0]:+.2f}% to {facts['pla_count_relative_change_percent_range'][1]:+.2f}%, while association fractions change {facts['association_change_percentage_point_range'][0]:+.2f} to {facts['association_change_percentage_point_range'][1]:+.2f} percentage points. These different denominators are labeled explicitly. **Limit:** pairing by shared measurements does not prove which exports are primary, alternative ROI analyses or reruns. **Next:** resolve those relationships before section or animal aggregation.","",
           "## 4. Which morphology measurements need image review?","",
           "![Morphology quality](../outputs/native_atlas/figures/export_morphology_quality.png)","",
           f"**Finding:** {facts['unusable_diameter_ratio_pla_including_repeats']:,} exported PLA rows have unusable minimum/maximum diameter ratios, including possible repeated detections. Per-export exclusion percentages span {facts['unusable_diameter_ratio_percent_range'][0]:.1f}%–{facts['unusable_diameter_ratio_percent_range'][1]:.1f}%. These objects remain in counts and ChAT-presence summaries. A zero minimum diameter with positive maximum remains a valid ratio of zero. The area intervals describe object distributions, not uncertainty in animals or confidence intervals. **Next:** inspect zero/invalid-diameter and extreme-area source objects before any shape modeling. No clustering is fitted in this report. [Full-source object review records](../outputs/native_atlas/morphology_object_review_targets.csv) and [native bin review windows](../outputs/native_atlas/review_targets.csv) provide source IDs/boxes and selection reasons; records can overlap across reasons.","",
           "## 5. What does the former project contribute?","",
           "The explorer and notebook retain verified historical animal-level findings and figures, explicitly labeled **historical expanded dataset**. That analysis used twelve retained sections, six animals and different expanded inputs; it is not a recomputation from these eight files. See [historical findings and visual transfer](historical_findings_and_visual_transfer.md) for exact sources, hashes, limitations and the methods actually reused.","",
           "## Requested condition difference maps","",
           "The supplied PDF still governs the final aligned Running − Homecage maps: separate PLA arms, unchanged accepted transforms, existing tissue masks, strict full-bin inclusion, valid zeros, equal-section means and coverage. Those specific outputs await the numerical accepted assets and current section relationships. Native exploration and historical context do not supply missing anatomical correspondence. See [project brief](project_brief.md) and `outputs/preflight.json` for exact unresolved fields.",""]
    (root/"docs/native_results_guide.md").write_text("\n".join(lines))
    return facts


if __name__=="__main__":
    print(json.dumps(build(),indent=2))
