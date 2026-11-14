"""Export actual authorized exploratory count maps, never strict tissue maps."""
import csv
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "tmp/matplotlib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
import numpy as np

ARMS = ("HK1", "PFKP")
CONDITIONS = ("Homecage", "Running")
NOTE = ("EXPLORATORY: positions are bounding-box midpoints; observed support means ≥1 exported PLA or ChAT object in a bin.\n"
        "Support is data-dependent and does not establish full tissue coverage. Coordinate units are not physically calibrated.")


def build(run_directory):
    run = Path(run_directory)
    payload = json.loads((run / "view_payload.json").read_text())
    if payload.get("strict_pdf_results") is not False:
        raise ValueError("Exploratory figure builder requires explicit non-strict result status")
    grid, arms = payload["grid"], payload["arms"]
    xe, ye = np.asarray(grid["x_edges"]), np.asarray(grid["y_edges"])
    limit = max(abs(payload["color_scale"]["cmin"]), abs(payload["color_scale"]["cmax"]))
    out = run / "figures"; out.mkdir(exist_ok=True)
    manifest = []
    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":11, "svg.fonttype":"none",
                         "axes.spines.top":False, "axes.spines.right":False})
    cmap = plt.get_cmap("RdBu_r").copy(); cmap.set_bad("#d6dde5")
    support_cmap = ListedColormap(["#f1f4f7", "#b8d5e7", "#5b9cc6", "#164f7c"])
    support_norm = BoundaryNorm(np.arange(-.5, 4.5), support_cmap.N)
    findings = {"scientific_status":"authorized_exploratory", "strict_pdf_results":False,
                "denominator":"Sections with ≥1 observed exported PLA or ChAT object in a bin; no full-bin tissue guarantee",
                "grid_shape_y_x":[len(ye)-1,len(xe)-1], "bin_width_export_units":1000,
                "shared_symmetric_difference_limit":limit, "arms":{}}

    def axes(ax):
        ax.set(xlim=(xe[0], xe[-1]), ylim=(ye[-1], ye[0]),
               xlabel="Aligned X · export units", ylabel="Aligned Y · export units")
        ax.set_aspect("equal")
        ax.ticklabel_format(style="plain", axis="both", useOffset=False)
        ax.tick_params(labelsize=9)

    def export(fig, name, title, caption):
        for ext in ("png", "svg"):
            fig.savefig(out / (name+"."+ext), dpi=300, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        manifest.append({"id":name, "title":title, "path":"figures/"+name+".png",
                         "svg_path":"figures/"+name+".svg", "dpi":300, "caption":caption,
                         "scientific_status":"exploratory; strict tissue-mask results pending"})

    def frame(fig, title, bottom=.20, top=.83):
        fig.subplots_adjust(left=.08, right=.96, bottom=bottom, top=top, wspace=.25, hspace=.35)
        fig.suptitle(title, fontsize=18, fontweight="bold", y=.98, color="#19354a")
        fig.text(.5,.92,"User-authorized exploration · same fixed alignment · unsmoothed raw counts", ha="center", fontsize=10, color="#80642c")
        fig.text(.055,.025,NOTE, fontsize=9, color="#5f7181", linespacing=1.5)

    def diff(ax, arm, minimum_observed=1):
        a = arms[arm]
        z = np.asarray(a["difference"],dtype=float)
        keep = (np.asarray(a["homecage_n"]) >= minimum_observed) & (np.asarray(a["running_n"]) >= minimum_observed)
        z = np.where(keep, z, np.nan)
        mesh = ax.pcolormesh(xe,ye,np.ma.masked_invalid(z),cmap=cmap,vmin=-limit,vmax=limit,shading="flat",rasterized=False)
        axes(ax); ax.set_title("TDP43–"+arm+" · Running − Homecage",pad=10,fontsize=12)
        return mesh

    def support(ax, arm, condition):
        key = "running_n" if condition=="Running" else "homecage_n"
        z = np.asarray(arms[arm][key],dtype=int)
        mesh = ax.pcolormesh(xe,ye,z,cmap=support_cmap,norm=support_norm,shading="flat",rasterized=False)
        axes(ax); ax.set_title("TDP43–"+arm+" · "+condition,pad=10,fontsize=12)
        return mesh

    difference_label = "Difference in observed-support mean PLA count per spatial bin\n(Running − Homecage)"
    for arm in ARMS:
        a=arms[arm]; z=np.asarray(a["difference"],float); finite=np.isfinite(z)
        hn,rn=np.asarray(a["homecage_n"]),np.asarray(a["running_n"])
        vals=z[finite]
        findings["arms"][arm]={"displayable_bins":int(finite.sum()), "grid_bins":int(z.size),
            "all_three_sections_per_condition_bins":int(((hn==3)&(rn==3)).sum()),
            "lower_observed_support_comparison_bins":int((finite & ((hn<3)|(rn<3))).sum()),
            "positive_difference_bins":int((vals>0).sum()),"negative_difference_bins":int((vals<0).sum()),
            "zero_difference_bins":int((vals==0).sum()),
            "minimum_difference":float(vals.min()) if len(vals) else None,
            "maximum_difference":float(vals.max()) if len(vals) else None,
            "observed_support_sensitivity":[{
                "minimum_observed_sections_each_condition":n,
                "retained_bins":int((finite & (hn>=n) & (rn>=n)).sum()),
                "negative_bins":int(((z<0) & (hn>=n) & (rn>=n)).sum()),
                "positive_bins":int(((z>0) & (hn>=n) & (rn>=n)).sum()),
                "zero_bins":int(((z==0) & (hn>=n) & (rn>=n)).sum())} for n in (1,2,3)],
            "interpretation":"Bin counts are descriptive spatial summaries, not independent biological replicates or significance tests."}
        fig,ax=plt.subplots(figsize=(8.5,8));frame(fig,"Exploratory spatial PLA difference · "+arm)
        im=diff(ax,arm); fig.colorbar(im,ax=ax,shrink=.75,pad=.035,label=difference_label)
        export(fig,"exploratory_difference_"+arm.lower(),"Exploratory "+arm+" difference",
               "Running minus Homecage mean raw PLA count among sections with observed PLA/ChAT support; grey bins lack support in either condition, white is zero observed-count difference.")

    fig, axs = plt.subplots(1,2,figsize=(14,8));frame(fig,"Two exploratory spatial PLA differences",bottom=.20,top=.83)
    for ax,arm in zip(axs,ARMS): im=diff(ax,arm)
    fig.colorbar(im,ax=list(axs),shrink=.75,pad=.035,label=difference_label)
    export(fig,"exploratory_differences_two_arms","Two exploratory difference maps",
           "Separate arms use one symmetric linear scale centered at zero; grey is unavailable observed support, not verified absent tissue.")

    fig, axs = plt.subplots(1,2,figsize=(14,8));frame(fig,"Observed-support sensitivity: all three sections per condition",bottom=.20,top=.83)
    for ax,arm in zip(axs,ARMS): im=diff(ax,arm,minimum_observed=3)
    fig.colorbar(im,ax=list(axs),shrink=.75,pad=.035,label=difference_label)
    export(fig,"exploratory_differences_all_three_observed","All-three-observed support sensitivity",
           "Display only bins with observed objects in all three sections in each condition. Means and shared color limits are unchanged; this still does not verify entire-bin tissue coverage.")

    fig,axs=plt.subplots(2,2,figsize=(13,12));frame(fig,"Four observed-object support maps",bottom=.13,top=.87)
    for row,arm in enumerate(ARMS):
        for col,condition in enumerate(CONDITIONS): im=support(axs[row,col],arm,condition)
    fig.colorbar(im,ax=list(axs.flat),ticks=range(4),shrink=.8,pad=.025,
                 label="Sections with ≥1 observed PLA or ChAT object (N observed)")
    export(fig,"observed_support_four_panels","Four observed-object support maps",
           "Number of sections with exported objects per bin, separately for condition and arm. N=0 means no exported detections, not established missing tissue. No strict coverage is claimed.")
    for arm in ARMS:
        for condition in CONDITIONS:
            fig,ax=plt.subplots(figsize=(8,8));frame(fig,"Observed-object support · "+arm+" · "+condition)
            im=support(ax,arm,condition);fig.colorbar(im,ax=ax,ticks=range(4),shrink=.75,pad=.035,label="Sections with observed objects (N)")
            export(fig,"observed_support_"+arm.lower()+"_"+condition.lower(),arm+" "+condition+" observed support",
                   "Detection-supported section N, not full-bin tissue-mask coverage.")

    means=[np.asarray(arms[a][k],float) for a in ARMS for k in ("homecage_mean","running_mean")]
    maximum=max(float(np.nanmax(z)) for z in means)
    mean_cmap=plt.get_cmap("cividis").copy();mean_cmap.set_bad("#d6dde5")
    fig,axs=plt.subplots(2,2,figsize=(13,12));frame(fig,"Condition means behind the exploratory differences",bottom=.13,top=.87)
    for row,arm in enumerate(ARMS):
        for col,condition in enumerate(CONDITIONS):
            ax=axs[row,col];z=np.asarray(arms[arm]["running_mean" if condition=="Running" else "homecage_mean"],float)
            im=ax.pcolormesh(xe,ye,np.ma.masked_invalid(z),cmap=mean_cmap,vmin=0,vmax=maximum,shading="flat")
            axes(ax);ax.set_title("TDP43–"+arm+" · "+condition,fontsize=12,pad=10)
    fig.colorbar(im,ax=list(axs.flat),shrink=.8,pad=.025,label="Mean PLA count per bin among observed-support sections")
    export(fig,"exploratory_condition_means","Exploratory condition means",
           "The raw section means used in the differences, shown with one common linear sequential scale. Denominators are observed-section N and may vary across bins.")

    targets=[]
    for arm in ARMS:
        z=np.asarray(arms[arm]["difference"],float)
        for reason, flat in (("most_negative_difference",np.nanargmin(z)),("most_positive_difference",np.nanargmax(z))):
            iy,ix=np.unravel_index(flat,z.shape)
            corners=np.array([[x,y,1.] for x in (xe[ix],xe[ix+1]) for y in (ye[iy],ye[iy+1])])
            for s in payload["sections"]:
                if s["pla_type"]!=arm: continue
                native=corners@np.linalg.inv(np.asarray(s["fixed_transform"]["matrix"])).T
                targets.append({"arm":arm,"review_reason":reason,"section_id":s["section_id"],
                    "animal_id":s["animal_id"],"condition":s["condition"],"y_bin":int(iy),"x_bin":int(ix),
                    "aligned_x_min":float(xe[ix]),"aligned_x_max":float(xe[ix+1]),
                    "aligned_y_min":float(ye[iy]),"aligned_y_max":float(ye[iy+1]),
                    "native_x_min":float(native[:,0].min()),"native_x_max":float(native[:,0].max()),
                    "native_y_min":float(native[:,1].min()),"native_y_max":float(native[:,1].max()),
                    "section_pla_count":int(s["pla_counts"][iy][ix]),
                    "section_chat_count":int(s["chat_counts"][iy][ix]),
                    "observed_support":bool(s["observed_support"][iy][ix]),
                    "running_minus_homecage":float(z[iy,ix]),
                    "source_file_id":s["source"]["source_file_id"],"source_path":s["source"]["path"],
                    "scope":"Selected extreme-bin review target, not a representative sample; native coordinates are not calibrated physical units."})
    with (run/"selected_bin_review_windows.csv").open("w",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(targets[0]));writer.writeheader();writer.writerows(targets)

    (run/"figure_manifest.json").write_text(json.dumps({"figures":manifest,"strict_pdf_results":False},indent=2,ensure_ascii=False)+"\n")
    (run/"findings.json").write_text(json.dumps(findings,indent=2,ensure_ascii=False)+"\n")
    return {"run_directory":str(run),"figures":len(manifest),"findings":findings}


if __name__ == "__main__":
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python scripts/build_exploratory_figures.py RUN_DIRECTORY")
    print(json.dumps(build(sys.argv[1]),indent=2))
