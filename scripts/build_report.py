"""Build saved input-audit figures and connect them to the spatial explorer.

This report never calculates biological comparisons from unresolved metadata.
It reads the reproducible inventory, not old scientific summary plots.
"""
from pathlib import Path
import html
import json
import os

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "tmp/matplotlib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import pandas as pd
from plotly.offline import get_plotlyjs


def save(fig, name):
    out = ROOT / "outputs/figures"
    out.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "svg"):
        fig.savefig(out / (name + "." + ext), dpi=300, bbox_inches="tight")
    plt.close(fig)


def build():
    manifest = json.loads((ROOT / "metadata/input_manifest.json").read_text())
    audit = json.loads((ROOT / "outputs/inventory/file_audit.json").read_text())
    summary = json.loads((ROOT / "outputs/inventory/summary.json").read_text())
    by_id = {m["file_id"]: m for m in manifest}
    plt.rcParams.update({"font.size": 11, "svg.fonttype": "none"})
    fig, ax = plt.subplots(figsize=(10, 5.6), layout="constrained")
    ys = np.arange(len(audit))
    pla = [a["pla_row_count_by_export_label"] for a in audit]
    chat = [a["chat_row_count_by_export_label"] for a in audit]
    labels = ["%s · job token %s" % (a["file_id"], by_id[a["file_id"]]["job_token_from_filename"]) for a in audit]
    ax.barh(ys, chat, color="#0072B2", label="ChAT-labelled detections")
    ax.barh(ys, pla, left=chat, color="#D55E00", label="PLA-labelled detections")
    ax.set(yticks=ys, yticklabels=labels, xlabel="Exported rows per file (possible repeat analyses included)",
           title="Input audit: counts describe exports, not biological replication")
    ax.invert_yaxis()
    ax.ticklabel_format(axis="x", style="plain")
    ax.set_title("Input audit: counts describe exports, not biological replication", pad=45)
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.01), ncol=2, frameon=False)
    ax.spines[["right", "top"]].set_visible(False)
    save(fig, "input_export_counts")

    overlap = pd.read_csv(ROOT / "outputs/inventory/within_input_overlap.csv")
    ids = [a["file_id"] for a in audit]
    mat = np.full((len(ids), len(ids)), np.nan)
    np.fill_diagonal(mat, 100)
    for row in overlap.to_dict("records"):
        i, j = ids.index(row["left_file_id"]), ids.index(row["right_file_id"])
        mat[i, j] = 100 * row["left_signature_shared_fraction"]
        mat[j, i] = 100 * row["right_signature_shared_fraction"]
    fig, ax = plt.subplots(figsize=(8, 7), layout="constrained")
    im = ax.imshow(mat, vmin=0, vmax=100, cmap="cividis", interpolation="none")
    for i in range(len(ids)):
        for j in range(len(ids)):
            ax.text(j, i, "%.1f" % mat[i, j], ha="center", va="center",
                    color="white" if mat[i, j] < 55 else "black", fontsize=9)
    ax.set(xticks=range(len(ids)), yticks=range(len(ids)), xticklabels=ids, yticklabels=ids,
           xlabel="Compared export", ylabel="Denominator export",
           title="Shared exported measurements: repeat-analysis review")
    ax.tick_params(axis="x", rotation=45)
    fig.colorbar(im, ax=ax, label="% of row export's distinct measurement signatures shared")
    fig.supxlabel("Excludes Analysis Region and Object Id. Agreement does not prove biological identity.", fontsize=10)
    save(fig, "input_measurement_overlap")

    fig, ax = plt.subplots(figsize=(11, 7), layout="constrained")
    ax.set(xlim=(0, 1), ylim=(0, 1)); ax.axis("off")
    nodes = [(0.03, .79, .42, .14, "Current inputs\nPDF + object CSV inventory"),
             (.55, .79, .42, .14, "Required existing assets\nMapping + masks + fixed alignment"),
             (.29, .56, .42, .14, "Validate provenance and coordinates\nOne shared aligned grid"),
             (.03, .32, .42, .14, "Per-section object counts\nCount each accepted centroid once"),
             (.55, .32, .42, .14, "Full-bin tissue validity\nValid empty = 0; missing = excluded"),
             (.29, .07, .42, .14, "Separate HK1 / PFKP section means\nRunning − Homecage + coverage")]
    for x, y, w, h, label in nodes:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=.01", facecolor="#E8F1F5", edgecolor="#536A77"))
        ax.text(x+w/2, y+h/2, label, ha="center", va="center", fontsize=11)
    for a, b in [((.24,.79),(.43,.70)),((.76,.79),(.57,.70)),((.43,.56),(.24,.46)),((.57,.56),(.76,.46)),((.24,.32),(.43,.21)),((.76,.32),(.57,.21))]:
        ax.add_patch(FancyArrowPatch(a,b,arrowstyle="->",mutation_scale=14,color="#536A77"))
    ax.set_title("Aligned COMET comparison: existing geometry required; native exploration is available separately", pad=12)
    save(fig, "workflow")

    app = ROOT / "outputs/app"; app.mkdir(parents=True, exist_ok=True)
    payload = [{**a, "manifest": by_id[a["file_id"]]} for a in audit]
    encoded = json.dumps(payload, ensure_ascii=False, allow_nan=False).replace("<", "\\u003c")
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>COMET input explorer</title>
<style>body{font:16px system-ui,sans-serif;color:#20323e;background:#f4f7f8;margin:0}main{max-width:1160px;margin:auto;padding:30px}h1{margin:0 0 10px;font-size:28px}h2{font-size:21px}p{line-height:1.55}.notice{background:#fff1da;border-left:5px solid #9b6100;padding:16px 20px;margin:22px 0}.card{background:white;border:1px solid #cbd5db;border-radius:8px;padding:20px;margin:18px 0}select{padding:10px;font:inherit;max-width:100%}#chart{height:440px}#details{display:grid;grid-template-columns:1fr 1fr;gap:12px}dt{font-weight:600;margin-top:12px}dd{margin:4px 0;overflow-wrap:anywhere}a{color:#005b90}code{overflow-wrap:anywhere}table{border-collapse:collapse;width:100%}td,th{padding:9px;text-align:left;border-bottom:1px solid #ddd}@media(max-width:700px){main{padding:16px}#details{display:block}}</style>
<script>__PLOTLY__</script></head><body><main><h1>COMET input explorer</h1>
<p>Saved inventory connected to the main notebook. Select an export to inspect its provenance, labels and coordinate fields.</p>
<div class="notice"><strong>Spatial comparison blocked.</strong> The instruction PDF refers to existing accepted alignment and tissue masks, but these assets and current sample relationships are not supplied. No Running − Homecage map has been calculated.</div>
<div class="card"><h2>Exported rows</h2><p>Each bar is a file, not an animal or independent section. Files overlap and must not be summed as independent samples. Colours indicate literal exported object classes, not experimental conditions.</p><div id="chart" aria-label="Export row count bar chart"></div><label for="file">Inspect export: </label><select id="file"></select></div>
<div class="card"><h2 id="detailTitle"></h2><div id="details"><dl id="left"></dl><dl id="right"></dl></div><h3>Observed coordinate bounds</h3><p>Bounding-box coordinates have unverified units. Midpoints are reconstructed proxies; the centroid definition needs clarification.</p><table><thead><tr><th>Field</th><th>Minimum</th><th>Maximum</th></tr></thead><tbody id="bounds"></tbody></table></div>
<div class="card"><h2>How to proceed</h2><p>Provide the existing accepted transformations and alignment-check source, tissue masks, centroid definition, shared reference/grid and authoritative section/animal/condition/arm mapping with repeat-export decisions. The workflow will then retain valid empty bins as zero and exclude any section-bin not fully contained in its mask.</p><p><a href="../../TDP43_COMET_analysis.ipynb">Main notebook</a> · <a href="../inventory/report.md">Inventory audit</a> · <a href="../../docs/project_brief.md">Scientific requirements</a></p><p>Opening the notebook requires a notebook viewer. This explorer reads saved audit values; changing a selection does not rerun analysis.</p></div></main>
<script>const records=__PAYLOAD__;const file=document.getElementById('file');
function add(dl,key,value){const dt=document.createElement('dt');dt.textContent=key;const dd=document.createElement('dd');dd.textContent=String(value);dl.append(dt,dd)}
records.forEach((r,i)=>{const o=document.createElement('option');o.value=i;o.textContent=r.file_id+' · job token '+r.manifest.job_token_from_filename;file.append(o)});
function show(){const r=records[Number(file.value)];document.getElementById('detailTitle').textContent=r.file_id;const l=document.getElementById('left'),q=document.getElementById('right');l.replaceChildren();q.replaceChildren();
add(l,'Exact source filename',r.filename);add(l,'SHA-256',r.sha256);add(l,'Source path recorded at inventory',r.path);add(l,'Rows',r.row_count.toLocaleString());
add(q,'Embedded Analysis Region text',Object.keys(r.analysis_region_counts).join('; '));add(q,'New-study assignment','Unconfirmed');add(q,'Historical byte-identical reference copies',r.manifest.historical_byte_identical_copy_count);add(q,'Centroid-named fields',r.true_centroid_fields_present.join(', ')||'None');add(q,'Malformed rows',r.malformed_row_count);
const b=document.getElementById('bounds');b.replaceChildren();Object.entries(r.bbox_field_ranges).forEach(([k,v])=>{const tr=document.createElement('tr');[k,...v].forEach(x=>{const td=document.createElement('td');td.textContent=x;tr.append(td)});b.append(tr)})}
file.addEventListener('change',show);show();Plotly.newPlot('chart',[
{type:'bar',name:'ChAT-labelled detections',x:records.map(r=>r.file_id),y:records.map(r=>r.chat_row_count_by_export_label),marker:{color:'#0072B2'}},
{type:'bar',name:'PLA-labelled detections',x:records.map(r=>r.file_id),y:records.map(r=>r.pla_row_count_by_export_label),marker:{color:'#D55E00'}}],
{barmode:'stack',margin:{t:25,b:60,l:80,r:15},yaxis:{title:{text:'Exported rows per file'}},legend:{orientation:'h',y:1.12},paper_bgcolor:'white',plot_bgcolor:'white'}, {responsive:true,displaylogo:false,displayModeBar:false});document.getElementById('chart').on('plotly_click',e=>{file.value=records.findIndex(r=>r.file_id===e.points[0].x);show()});
</script></body></html>'''
    page = page.replace("__PLOTLY__", get_plotlyjs()).replace("__PAYLOAD__", encoded)
    (app / "input_audit.html").write_text(page)
    # Keep inventory as a drill-down; the main view shows real spatial data.
    from scripts.build_spatial_explorer import build as build_spatial_explorer
    build_spatial_explorer()
    from scripts.build_comet_core_report import build as build_core_report
    build_core_report()
    return summary


if __name__ == "__main__":
    build()
