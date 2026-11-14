"""Current scientist-directed workflow; original PDF contract remains historical."""
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "tmp/matplotlib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


def build(root=ROOT):
    out = Path(root) / "outputs/figures"
    out.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(13, 8))
    fig.subplots_adjust(left=.015, right=.985, bottom=.025, top=.89)
    ax.set(xlim=(0, 1), ylim=(0, 1)); ax.axis("off")
    def box(x, y, w, h, text, face="#edf3f7", edge="#658097", size=11):
        ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
                     boxstyle="round,pad=.012", facecolor=face, edgecolor=edge, linewidth=1.1))
        ax.text(x, y, text, ha="center", va="center", fontsize=size, color="#19354a", linespacing=1.45)
    def arrow(a, b):
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=14,
                                    color="#698298", linewidth=1.2))
    box(.5,.93,.92,.09,"Selected cohort: six animals, twelve completed sections, two separate PLA arms\nExpanded source CSVs + exact hashes; interrupted 4978 excluded for 5403",size=12)
    box(.16,.73,.27,.15,"Saved fixed alignment\nAll 12 transforms recovered\nNo refitting",face="#e8f3ef")
    box(.50,.73,.27,.15,"Individual PLA positions\nAll 310,024 objects retained\nBounding-box midpoint proxies",face="#e8f3ef")
    box(.84,.73,.27,.15,"Scientist-directed policy\nAll three sections per condition\nEmpty section-bins assumed zero",face="#e8f3ef")
    for x in (.16,.50,.84): arrow((x,.885),(x,.82))
    box(.67,.48,.58,.15,"Shared aligned grids; default 100 export units\nCount each PLA once per section; preserve arm separation\nCondition mean = sum of all three section counts / 3\nTissue coverage remains uncertain",size=10.5)
    for a in ((.26,.65),(.5,.64),(.84,.64)): arrow(a,(.67,.57))
    box(.16,.30,.27,.27,"2 · Alignment review\nOriginal check preserved\nAll-object 2D inspection\nNo serial reconstruction",face="#e8f3ef",edge="#578f7b",size=12)
    arrow((.16,.64),(.16,.45))
    box(.51,.16,.27,.25,"1 · Means and differences\nHK1 and PFKP separately\nRunning − Homecage\n600-DPI figures and tables",face="#e8f3ef",edge="#578f7b",size=12)
    box(.84,.16,.27,.25,"3 · Four support maps\nSections with detections: N\nDiagnostic; denominator stays 3\nNo tissue mask inferred",face="#e8f3ef",edge="#578f7b",size=11)
    arrow((.59,.39),(.51,.30)); arrow((.76,.39),(.84,.30))
    fig.suptitle("Experiment to results: the three current visual families",fontsize=19,color="#19354a",y=.97)
    fig.text(.5,.905,"Scientist/user clarification · 14 November 2026 · raw counts · unchanged alignment · coverage uncertain",
             ha="center",fontsize=11,color="#62798c")
    for ext in ("png","svg"):
        fig.savefig(out/("workflow."+ext),dpi=600,bbox_inches="tight",facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    build()
