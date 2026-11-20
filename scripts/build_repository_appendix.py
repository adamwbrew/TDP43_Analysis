"""Inventory the selected Git project and rebuild its explanatory file catalog.

This documentation utility never executes analysis, modifies inputs, or reads
Git credentials/object contents. In a ZIP without Git metadata it can reuse the
published inventory. --check verifies file coverage and local documentation links.
"""
from pathlib import Path
import argparse
import ast
import csv
import html
from hashlib import sha256
import json
import re
import struct
import subprocess
from urllib.parse import unquote, quote
import zipfile

ROOT=Path(__file__).resolve().parents[1]
APPENDIX=Path('docs/appendix')

PURPOSES={
 '.DS_Store':'Existing tracked macOS Finder display metadata. It contains no analysis code; unrelated local changes are excluded from this update.',
 '.gitignore':'Selects publishable code/results while excluding raw inputs, instruction PDFs, environments and unselected generated runs.',
 '.gitattributes':'Preserves scientific CSV bytes, marks binary artifacts and identifies generated output files for Git review.',
 'README.md':'The starting instructions for viewing, rerunning and understanding the current nineteen-measurement Explorer.',
 'Launch_COMET_Explorer.command':'Mac double-click launcher: locates this checkout and starts the local Python viewer server; opens saved HTML directly if Python is unavailable.',
 'pyproject.toml':'Python package metadata and core/report dependency groups; it does not contain scientific measurements.',
 'requirements.txt':'Compatible dependency version ranges for the complete scientific reporting environment.',
 'requirements-lock.txt':'Exact recorded dependency versions, with a macOS-only marker for appnope; supports environment reproduction.',
 'TDP43_COMET_analysis.ipynb':'Current main scientific report: eight executed code cells, nineteen metric definitions, saved results and interpretation.',
 'TDP43_native_supporting_analysis.ipynb':'Historical eight-export native-coordinate supporting report. Saved outputs are background; its rerun has a different scope and shared-output side effects.',
 'comet_spatial/__init__.py':'Declares the reusable Python analysis package.',
 'comet_spatial/core.py':'Shared grid, fixed-transform, mask-containment, count-binning and condition-comparison primitives, including the separate strict method.',
 'comet_spatial/core_view.py':'Validates a saved strict numerical run and turns its own snapshot into a viewer payload; reports missing strict inputs separately.',
 'comet_spatial/exploratory.py':'Streams the twelve selected raw exports, counts PLA/ChAT midpoint proxies and records exploratory provenance/support.',
 'comet_spatial/multiresolution.py':'Builds four genuine count grids and the full unsampled PLA point cache from selected raw exports.',
 'comet_spatial/section_means.py':'Derives current fixed-three count means/differences from saved counts while preserving historical variable-support summaries.',
 'comet_spatial/measurements.py':'Reference Python implementation of all nineteen section-bin measurements, defined-section means and three comparisons.',
 'comet_spatial/measurement_features.py':'Matches PLA area/intensity/marker vectors to exact source objects and adds exact same-section nearest-neighbor distances immutably.',
 'comet_spatial/context_geometry.py':'Traces every boundary/gap of the finest observed-object bin domain; supplies a metric-independent footprint, not a tissue mask.',
 'comet_spatial/alignment_replay.py':'Replays frozen historical placement for a reproducibility check; it does not fit a new anatomical alignment.',
 'comet_spatial/manifest.py':'Reads and checks source/section/transform/approval/mask metadata and produces preflight diagnostics for the strict method.',
 'comet_spatial/native_atlas.py':'Historical native-export summaries, count/association maps, shape QC, point samples and source-review windows for the original intake.',
 'scripts/build_repository_appendix.py':'Rebuilds this complete selected-file catalog and its static workflow SVG, then checks coverage and Markdown links.',
 'scripts/comet_measurements.js':'Browser counterpart of the nineteen Python measurements; computes the same statistics from embedded point/attribute caches.',
 'scripts/comet_measurement_controls.js':'Connects measurement/comparison controls, fixed 8K downloads, persistent footprint, hover tables and fine-detail navigation.',
 'scripts/comet_detail_grid.js':'Rebins full-precision points in a local 100/50/25/10-unit window while retaining full-section share/neighbor context.',
 'scripts/comet_vector_export.js':'Writes exact tile/outline SVG and rasterizes it for PNG downloads; the UI fixes PNG width to 8,000 pixels.',
 'scripts/comet_plot_lifecycle.js':'Initializes hidden plots at real dimensions, decodes previews, manages plot resources and reports startup readiness.',
 'scripts/comet_support_detail.js':'Linked observed-support maps, baseline section counts and full point details; support remains independent of the selected metric.',
 'scripts/comet_alignment_detail.js':'Detailed 2D section placement/review controls using saved transforms and unchanged full PLA locations.',
 'scripts/comet_core_explorer.html':'Current browser layout/style and shared view logic; contains payload/module placeholders, not the raw CSVs.',
 'scripts/spatial_explorer.html':'Historical native-atlas browser template; its sampled point display and eight-export scope differ from the current app.',
 'scripts/build_comet_core_explorer.py':'Bundles Plotly, validated caches, alignment assets, context geometry and local JS/CSS into one offline HTML file.',
 'scripts/build_measurement_features.py':'CLI wrapper that extracts the source-verified attribute cache from authorized original CSVs.',
 'scripts/build_measurement_report.py':'Calculates all nineteen metrics on four global grids; writes NPZ/CSV reports and true-vector/600-DPI figure pairs.',
 'scripts/validate_measurement_engines.py':'Checks complete real-data Python/JavaScript arrays, finite masks, original count results and unchanged geometry.',
 'scripts/build_current_notebook.py':'Generates the current main notebook source and clears saved execution output; follow structural edits with execution.',
 'scripts/execute_notebook.py':'Executes notebook cells with its Python environment and atomically saves only successfully validated outputs.',
 'scripts/build_notebook.py':'Current notebook entry point delegates to the modern builder; retains an explicitly named historical observed-support notebook builder.',
 'scripts/build_native_notebook.py':'Generates the separate historical native supporting notebook; rerunning it can rewrite shared report/validation outputs.',
 'scripts/build_section_mean_maps.py':'Derives/exports fixed-three means, bin CSVs, NPZ matrices, portable point payload and immutable count-run records.',
 'scripts/build_section_mean_figures.py':'Draws current raw-count means/differences with shared linear scales and disclosed display caps.',
 'scripts/build_review_figures.py':'Exports detailed alignment atlases and observed-support panels from the selected saved count/point run.',
 'scripts/build_comet_core_report.py':'Connects strict preflight diagnostics and saved exploratory runs, updates workflow assets and rebuilds the current app.',
 'scripts/build_comet_workflow.py':'Draws the current experiment-to-results workflow used by the report/app build.',
 'scripts/build_detailed_figures.py':'Earlier multiresolution count/support atlas; its historical support-based estimator must not replace current means.',
 'scripts/build_exploratory_figures.py':'Earlier exploratory mean/difference/support figures from the selected completed raw exports.',
 'scripts/build_findings.py':'Historical descriptive native-export findings and source-review targets; does not establish the current condition comparison.',
 'scripts/build_multiresolution_maps.py':'CLI wrapper for full raw recounting on the four recorded aligned grids.',
 'scripts/build_report.py':'Historical native report/figure/workflow build; can rewrite shared output names and is not the current app entry point.',
 'scripts/build_spatial_explorer.py':'Builds the historical portable native supporting app from the native atlas payload.',
 'scripts/configure_local_inputs.py':'Relocates raw source paths only after checking thirteen hashes, twelve selected sections and the interrupted-run exclusion.',
 'scripts/extract_alignment_snapshot.py':'Extracts frozen placement parameters from the former app with source hashes and section/source relationships.',
 'scripts/inventory_data.py':'Profiles the original intake files, measurement columns and duplicates; records observation separately from scientific assignment.',
 'scripts/refresh_review_notebook.py':'Historical notebook review-section insertion/refresh helper; its older headings are not a general modern notebook rebuild.',
 'scripts/reproduce_alignment_check.py':'Reproduces the saved alignment-check image and records pixel/hash/transform comparisons.',
 'scripts/run_analysis.py':'Strict tissue-mask pipeline runner; validates its inputs before producing mask-valid section means and contrasts.',
 'scripts/run_exploratory_maps.py':'CLI for authorized exploratory counting from selected raw CSVs, without inventing tissue coverage.',
 'scripts/serve_app.py':'Optional standard-library localhost-only server. Serves only outputs/app; does not rerun analysis or serve raw inputs.',
 'metadata/analysis_manifest.json':'Selected source paths/hashes, twelve section assignments, fixed transforms, grid and strict-input attestations.',
 'metadata/cohort_selection.json':'Explicit twelve-section cohort authority and thirteen-export inventory, with job 4978 superseded by 5403.',
 'metadata/scientist_directed_mean_policy.json':'14 November scientist-authorized three-section count denominator and assumed-zero/uncertain-coverage policy.',
 'metadata/calculation_functions_policy.json':'Original thirteen PDF definitions, current nineteen-metric catalog and zero/missing/comparison provenance.',
 'metadata/spatial_extensions_policy_2026-11-19.json':'Dated six-metric/fine-detail/footprint extension snapshot. Its original optional-12K field is historical; the later fixed-size protocol overrides the UI setting.',
 'metadata/detailed_visual_parameters.json':'Current global/local grids, context, scales and fixed 8,000-pixel PNG display/export policy.',
 'metadata/alignment_support_review_parameters.json':'Dated detailed-review settings and unchanged full-point/alignment provenance.',
 'metadata/background_provenance.json':'The historical PLA–ChAT repository revision, research role and inspected background materials.',
 'metadata/data_dictionary.csv':'Column-by-column dictionary of original input fields and observed types/units.',
 'metadata/data_dictionary.json':'Machine-readable version of the original input-field dictionary.',
 'metadata/descriptive_findings_parameters.json':'Historical native descriptive size/association/review rules, not transferred condition-analysis constants.',
 'metadata/environment.json':'Recorded Python/platform/package and execution provenance; not the dependency installer.',
 'metadata/exploratory_authorization.json':'Recorded permission and scope for exploratory analysis without strict tissue-mask inputs.',
 'metadata/explorer_display_parameters.json':'Earlier native app starting display choices and its separate point-sampling convention.',
 'metadata/grid_parameters.json':'Original common aligned extent, edge definitions and unverified physical-coordinate calibration.',
 'metadata/input_manifest.csv':'Original intake-file inventory and source metadata in spreadsheet-readable form.',
 'metadata/input_manifest.json':'Machine-readable original intake-file inventory with recorded hashes/paths.',
 'metadata/instruction_provenance.json':'Recorded original instruction PDF identity, page count, hash and review provenance; not the PDF itself.',
 'metadata/local_paths.json':'Local source/workspace/background paths and copy policy; these paths are not portable scientific identities.',
 'metadata/native_atlas_parameters.json':'Historical native bin widths, deterministic display sampling and shape/intensity histogram settings.',
 'metadata/sample_metadata.csv':'Original observed intake metadata; older unresolved assignments are superseded by selected-section/cohort authority.',
 'metadata/section_template.json':'Example schema for supplying a section, source, mask and transform; it is not a real new sample.',
 'metadata/selected_section_metadata.csv':'Explicit current animal/condition/arm/source relationships for the twelve completed sections.',
 'docs/appendix/README.md':'Entry point for this explanatory appendix, with an end-to-end map and reading routes.',
 'docs/appendix/calculations.md':'Complete calculation definitions, worked examples, missingness and current/historical method distinctions.',
 'docs/appendix/code_reference.md':'File-by-file explanation of Python/JavaScript/templates and their call/data flow.',
 'docs/appendix/repository_guide.md':'Detailed root/notebook/docs/metadata/test guide, vocabulary and safe rerun routes.',
 'docs/appendix/file_catalog.md':'Every selected repository file, individually linked and explained, including repeated result artifacts.',
 'docs/appendix/file_inventory.json':'Machine-readable complete file catalog; supports coverage validation and regeneration from a ZIP.',
 'docs/appendix/diagrams/data_to_visuals.svg':'Scalable overview from original exports and verified metadata through calculations to scientific/app visuals.',
}


def paths_for(root, repository):
    command=['git','-C',str(repository),'ls-files','--cached','--others','--exclude-standard','--deduplicate','-z']
    try:result=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    except OSError:result=None
    if result is not None and result.returncode==0:
        paths={p.decode() for p in result.stdout.split(b'\0') if p}
    else:
        inventory=root/APPENDIX/'file_inventory.json'
        if not inventory.is_file():raise RuntimeError('Git file listing unavailable and no published inventory exists')
        paths={r['path'] for r in json.loads(inventory.read_text())['files']}
    paths|={p.relative_to(root).as_posix() for p in (root/APPENDIX).rglob('*') if p.is_file()}
    paths|={str(APPENDIX/'file_catalog.md'),str(APPENDIX/'file_inventory.json'),'scripts/build_repository_appendix.py'}
    return sorted(paths)


def symbols(path):
    if path.suffix=='.py':
        tree=ast.parse(path.read_text());out=[]
        for item in tree.body:
            if isinstance(item,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                out.append({'name':item.name,'line':item.lineno,'kind':'class' if isinstance(item,ast.ClassDef) else 'function'})
                if isinstance(item,ast.ClassDef):
                    out.extend({'name':item.name+'.'+m.name,'line':m.lineno,'kind':'method'} for m in item.body if isinstance(m,(ast.FunctionDef,ast.AsyncFunctionDef)))
        return out
    if path.suffix=='.js':
        text=path.read_text();return [{'name':m.group(1),'line':text[:m.start()].count('\n')+1,'kind':'function'} for m in re.finditer(r'\bfunction\s+([A-Za-z_$][\w$]*)\s*\(',text)]
    return []


def artifact_purpose(rel):
    name=Path(rel).name;stem=Path(rel).stem
    if rel=='outputs/app/index.html':return 'The current self-contained offline nineteen-measurement Explorer: embedded data, Plotly and app code; open this file to view results.'
    if rel=='outputs/app/native_explorer.html':return 'Historical self-contained native supporting app for the original eight-export intake; different data/summary scope.'
    if rel=='outputs/validation.json':return 'Latest combined analysis/software verification, with current update records; detailed dated evidence is kept in protocols.'
    if rel=='outputs/publication_manifest.json':return 'Selected repository publication inventory and validation record; earlier publication records remain dated in protocols.'
    if rel.startswith('outputs/protocols/'):
        if name=='instructions_extracted.json':return 'Recorded text/page extraction from the original scientist instructions; not an executable or independent assignment authority.'
        return 'Dated audit/provenance record for '+stem.replace('_',' ')+'. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.'
    if name=='latest_run.json':return 'Small pointer selecting the active immutable run in '+str(Path(rel).parent)+'. Loaders prefer the copied local run directory before recorded absolute paths.'
    if rel.startswith('outputs/calculation_functions/'):
        if name=='report.json':return 'Definitions, settings, per-arm/resolution comparison summaries, figure manifest and validation for this metric run.'
        if name=='summary.csv':return 'One row per measurement × comparison × arm × global grid; documents defined/missing counts, ranges and metric N.'
        if name=='validation.json':return 'Metric-run conservation/subset, count-preservation, geometry and provenance checks.'
        if name.endswith('.npz'):
            label=stem.replace('_',' ')
            return 'Compressed numerical arrays for '+label+' on '+Path(rel).parent.name.replace('_',' ')+' bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.'
        if name.endswith(('.png','.svg')):return 'Saved '+('full-range' if '_detail_' not in name else 'disclosed contrast-limited')+' scientific figure for '+stem.replace('_',' ')+'. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.'
    if rel.startswith('outputs/measurement_features/'):
        if name=='features.json':return 'Full-precision PLA area/intensity/ChAT vectors indexed to exact cached objects; the later run also contains full-section nearest-neighbor distances and predecessor lineage.'
        return 'Validation of the attribute cache, source/object-order matching and any later spatial-vector extension.'
    if rel.startswith('outputs/section_means/'):
        if name=='view_payload.json':return 'Four-grid fixed-three count means plus source section matrices and complete unsampled PLA locations; active run selection comes from latest_run.json.'
        if name.endswith('_bins.csv'):return 'Complete '+stem.split('_')[0].upper()+' spatial bin table for '+Path(rel).parent.name.replace('_',' ')+': three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.'
        if name.endswith('_matrices.npz'):return 'Compressed '+stem.split('_')[0].upper()+' grid matrices behind the count means, differences, eligibility and observed support at this resolution.'
        if name=='source_record.json':return 'Identity/hash of the unchanged raw-count predecessor used to derive this immutable fixed-three run.'
        if name=='validation.json':return 'Count conservation, fixed denominator, exact source/transform/point and derived mean checks for this run.'
        if name=='detailed_figure_manifest.json':return 'Figure paths, parameters, scales and captions for this count-run figure library.'
        if name.endswith(('.png','.svg')):return 'Saved fixed-three PLA count '+('means plus difference' if 'means_and_difference' in name else 'difference')+' figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.'
    if rel.startswith('outputs/exploratory_multiresolution/'):
        if name=='view_payload.json':return 'Raw-validated four-resolution count cache and full PLA point provenance; current analysis reuses these counts/positions, while its older observed-support means remain historical.'
        return 'Saved multiresolution predecessor '+stem.replace('_',' ')+': identifies grids, input hashes, conservation and recorded historical summary settings.'
    if rel.startswith('outputs/inventory/'):
        roles={'column_profiles.csv':'Per-column missingness/type/range profiles from the original intake.',
          'file_audit.json':'Original file identity/classification and duplicate audit.',
          'reference_manifest.csv':'References to background inputs kept separate from active experiment files.',
          'report.md':'Readable original intake inventory findings and unresolved-at-the-time observations.',
          'sample_metadata_observed.csv':'File-observed sample clues; scientific identity is supplied by later explicit metadata.',
          'summary.json':'Original intake totals and schema summary.',
          'validation.json':'Inventory/source-row/schema validation results.',
          'within_input_overlap.csv':'Overlap between historical exports; rows here do not create additional animals.'}
        return roles.get(name,'Original intake audit artifact; compare with later selected-cohort metadata before using assignments.')
    if rel.startswith('outputs/native_atlas/'):
        return 'Historical native-export source-object review windows '+('including morphology eligibility/QC targeting' if 'morphology' in name else 'for selected high/low association patterns')+'. Coordinates identify inspection targets, not validated cell classes.'
    if rel.startswith('outputs/core_view/'):
        return 'Saved strict viewer payload and its input blockers; absence of strict masks does not block the separate authorized exploratory app.'
    if rel.startswith('outputs/comet_core/'):
        if name=='context_geometry.json':return 'Exact finest observed-object occupancy and merged grid-edge boundaries, with holes, provenance hash and explicit non-tissue status.'
        if name=='alignment_snapshot.json':return 'Frozen former-app section/source IDs, colors and placement transforms for replay, not a fresh fit.'
        if name=='alignment_replay_validation.json':return 'Pixel/hash/transform checks comparing the reproduced alignment-check figure with its saved reference.'
        if name=='asset_audit.json':return 'Inventory and provenance of available alignment/data assets; distinguishes detections from absent microscopy/masks.'
        if name=='manifest.json':return 'Figure library manifest tied by hash to the selected count payload.'
        if name.startswith('alignment_check'):return 'Original or reproduced alignment-check image/vector asset. Its purpose is placement reproducibility, not independent anatomical validation.'
        if name.startswith('alignment_detail'):return 'High-resolution saved two-dimensional section-alignment atlas for the named PLA arm.'
        if name.startswith('observed_support'):return 'High-resolution per-condition detection-support map; counts supporting sections, not verified tissue area.'
        if name.endswith(('.png','.svg')):
            return ('Retained browser export with settings encoded in its SVG/protocol' if 'vector' in name or 'px_' in name else 'Dated app screenshot/review figure documenting the interface at that time')+'. Earlier 12K/selector demonstrations are historical; current PNG downloads are fixed at 8K.'
    if name.startswith('test_log_'):return 'Saved software-check output for '+stem.removeprefix('test_log_').replace('_',' ')+'. Expected fictional BLOCKED fixtures in these logs are not failures of the current exploratory results.'
    raise ValueError('Add an explicit artifact purpose for '+rel)


def describe(root, repository, rel):
    path=root/rel
    if not path.is_file():path=repository/rel
    if rel in PURPOSES:purpose=PURPOSES[rel]
    elif rel.startswith('outputs/'):purpose=artifact_purpose(rel)
    elif rel.startswith('tests/') and rel.endswith('.py'):purpose='Regression checks for '+Path(rel).stem.removeprefix('test_').replace('_',' ')+'. Named test methods below identify the concrete behaviors; see the test-by-test guide.'
    elif rel.startswith('docs/appendix/diagrams/'):
        if path.name=='diagram_manifest.json':purpose='Diagram rendering audit: Mermaid renderer/source version, originating document/block, source and SVG hashes, and successful local render checks.'
        else:purpose='Rendered vector flow diagram for '+path.stem.replace('_',' ')+'. Its editable Mermaid source appears in the corresponding appendix chapter; it does not contain measured specimen images.'
    elif rel.startswith('docs/') and path.is_file():purpose='Reader documentation: '+path.read_text().splitlines()[0].lstrip('# ')+'. Its current/historical scope is explained in the repository guide.'
    elif rel.startswith('scripts/') and path.suffix=='.py':purpose=(ast.get_docstring(ast.parse(path.read_text())) or '').split('\n')[0]
    else:raise ValueError('Add a file purpose for '+rel)
    record={'path':rel,'purpose':purpose,'format':path.suffix.lstrip('.') or 'configuration/metadata'}
    if path.is_file():
        if path.suffix in ('.py','.js'):record['code_items']=symbols(path)
        if path.suffix=='.csv':
            with path.open(encoding='utf-8-sig',newline='') as f:record['columns']=next(csv.reader(f),[])
        if path.suffix=='.npz':
            with zipfile.ZipFile(path) as f:record['arrays']=[n.removesuffix('.npy') for n in f.namelist()]
        if path.suffix=='.png':
            with path.open('rb') as f:header=f.read(24)
            if header[:8]==b'\x89PNG\r\n\x1a\n':record['pixels']=list(struct.unpack('>II',header[16:24]))
        if path.suffix=='.ipynb':
            nb=json.loads(path.read_text());code=[c for c in nb['cells'] if c['cell_type']=='code']
            record['notebook']={'cells':len(nb['cells']),'code_cells':len(code),'executed_code_cells':sum(c.get('execution_count') is not None for c in code),'saved_png_outputs':sum('image/png' in o.get('data',{}) for c in code for o in c.get('outputs',[]))}
    return record


def link(rel):return '../../'+quote(rel,safe='/._-')


def render_catalog(records):
    lines=['# Complete repository file catalog','',
     'Every file selected by Git for this project is listed individually below, including source files, tests, metadata, notebooks and repeated generated figures/tables. File contents are explained in the linked code, calculation and repository guides. Files in the hidden `.git/` database are version-control internals; raw-input and temporary directories are intentionally excluded from publication.','',
     '[Appendix home](README.md) · [Calculations](calculations.md) · [Code reference](code_reference.md) · [Repository guide](repository_guide.md)','',
     f'**Catalog coverage: {len(records)} selected files.** The accompanying [machine-readable inventory](file_inventory.json) records every path, purpose, source entry point, CSV header and NPZ array name. Regenerate with `python scripts/build_repository_appendix.py`; use `--check` to validate file coverage and local links.','',
     'Generated artifacts are data or rendered output, not additional executable code. A PNG/SVG pair depicts one calculation twice; two saved runs of the same section are not independent animals. `latest_run.json` selects the active run. Older figures/protocols remain dated evidence and may show earlier controls or denominators.','']
    directory=None
    for rec in records:
        parent=str(Path(rec['path']).parent)
        if parent!=directory:
            directory=parent;lines.extend(['## '+('Repository root' if parent=='.' else '`'+parent+'`'),''])
        lines.extend(['### ['+Path(rec['path']).name+']('+link(rec['path'])+')','',rec['purpose'],''])
        items=rec.get('code_items',[])
        if items:
            names=', '.join('['+i['name']+']('+link(rec['path'])+'#L'+str(i['line'])+')' for i in items)
            lines.extend(['**Named code items:** '+names+'.',''])
        if 'notebook' in rec:
            n=rec['notebook'];lines.extend([f"**Saved notebook structure:** {n['cells']} cells, {n['code_cells']} code cells, {n['executed_code_cells']} with execution counts, {n['saved_png_outputs']} PNG outputs. See the notebook guide for scope and rerun side effects.",''])
        if 'pixels' in rec:lines.extend([f"**Raster dimensions:** {rec['pixels'][0]:,} × {rec['pixels'][1]:,} pixels. These are export dimensions, not microscope calibration or extra scientific bins.",''])
        if 'columns' in rec:lines.extend(['**CSV columns:** '+', '.join('`'+c.replace('`','')+'`' for c in rec['columns'])+'.',''])
        if 'arrays' in rec:lines.extend(['**Stored arrays:** '+', '.join('`'+c+'`' for c in rec['arrays'])+'.',''])
    return '\n'.join(lines).rstrip()+'\n'


def workflow_svg():
    stages=[
      ('1  Original exports and explicit metadata','HALO object tables + scientist-defined animal/condition/arm mapping','Raw inputs stay local; preserve source file names and hashes.'),
      ('2  Verify sources and select the cohort','Twelve completed sections; three animals per condition in each arm','Interrupted job 4978 is superseded by 5403; copies are not new animals.'),
      ('3  Preserve measured object placement','Bounding-box midpoint → saved reflection/translation → aligned X/Y','No new alignment fit, physical calibration or fluorescence pixels.'),
      ('4  Save reusable counts and object attributes','Four global grids + all PLA points + area/intensity/ChAT flags','Compute exact nearest neighbors across each complete section.'),
      ('5  Calculate within each section and bin','Nineteen counts, fractions, sizes, intensity and spacing summaries','Empty counts/sums: assumed zero. Missing object statistics: undefined.'),
      ('6  Average animals before contrasting conditions','Equal mean of defined section values → Homecage H and Running R','Three animals are available per condition; report metric-defined N.'),
      ('7  Compare and retain spatial context','R − H  |  100 × (R − H)/H  |  log₂(R/H)','Zero and missing stay distinct; retain independent observed-object context.'),
      ('8  Save reports and explore in the offline app','NPZ/CSV + executed notebook + vector/600-DPI figures + bundled HTML','Fine local bins and section details; fixed 8K PNG or scalable SVG downloads.'),
    ]
    width=1120;height=1710;parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
      '<title id="title">From raw HALO exports to COMET spatial visuals</title><desc id="desc">Eight numbered stages explain source validation, unchanged positioning, reusable counts and attributes, section measurements, animal averages, contrasts and offline visualization.</desc>',
      '<rect width="100%" height="100%" fill="#ffffff"/><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="none" stroke="#687f90" stroke-width="1.5"/></marker></defs>',
      '<g font-family="Arial, sans-serif"><text x="60" y="52" fill="#19354a" font-size="31" font-weight="bold">From raw HALO exports to COMET visuals</text><text x="60" y="88" fill="#567183" font-size="21">Current exploratory analysis · object rows are not independent animals</text>']
    for i,(title,line1,line2) in enumerate(stages):
        y=125+i*190
        if i:parts.append(f'<path d="M560,{y-42} V{y-7}" fill="none" stroke="#687f90" stroke-width="2.5" marker-end="url(#arrow)"/>')
        parts.extend([f'<rect x="60" y="{y}" width="1000" height="145" rx="12" fill="#f4f7fa" stroke="#c4d3de" stroke-width="1.5"/>',
          f'<text x="85" y="{y+37}" fill="#19354a" font-size="25" font-weight="bold">{html.escape(title)}</text>',
          f'<text x="85" y="{y+78}" fill="#36586e" font-size="21">{html.escape(line1)}</text>',
          f'<text x="85" y="{y+113}" fill="#567183" font-size="19">{html.escape(line2)}</text>'])
    parts.extend(['<text x="60" y="1681" fill="#795d25" font-size="20">Coverage remains uncertain. Footprint boundaries are detection context, not verified tissue masks.</text></g></svg>'])
    return ''.join(parts)


def check_links(root,repository=None):
    errors=[];checked=0
    docs=[root/'README.md',*(root/APPENDIX).glob('*.md')]
    for p in docs:
        text=p.read_text()
        if text.count('```')%2:errors.append(str(p.relative_to(root))+': unclosed code fence')
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',text):
            parts=target.strip('<>').split('#',1);target=parts[0];fragment=parts[1] if len(parts)>1 else ''
            if not target or re.match(r'^[A-Za-z]+:',target):continue
            checked+=1
            candidate=(p.parent/unquote(target)).resolve()
            exists=candidate.exists()
            if not exists and repository is not None:
                try:exists=(repository/candidate.relative_to(root)).exists()
                except ValueError:pass
            if not exists:errors.append(str(p.relative_to(root))+': missing '+target)
            elif fragment and candidate.suffix=='.md' and candidate.is_file():
                headings=[]
                for raw in re.findall(r'^#{1,6}\s+(.+)$',candidate.read_text(),re.M):
                    raw=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',raw).replace('`','').lower()
                    headings.append(re.sub(r'[^\w\s-]','',raw).replace(' ','-'))
                if unquote(fragment) not in headings:errors.append(str(p.relative_to(root))+': missing heading '+target+'#'+fragment)
    return checked,errors


def build(root=ROOT,repository=None,check=False):
    root=Path(root).resolve();repository=Path(repository).resolve() if repository else root
    out=root/APPENDIX;out.mkdir(parents=True,exist_ok=True)
    (out/'diagrams').mkdir(exist_ok=True)
    if not check:(out/'diagrams/data_to_visuals.svg').write_text(workflow_svg())
    selected=paths_for(root,repository)
    if check:
        inventory=json.loads((out/'file_inventory.json').read_text());recorded={r['path'] for r in inventory['files']}
        if recorded!=set(selected):raise RuntimeError('Catalog coverage changed: missing='+str(sorted(set(selected)-recorded))+' extra='+str(sorted(recorded-set(selected))))
        catalog=(out/'file_catalog.md').read_text()
        if any(']('+link(rel)+')' not in catalog for rel in selected):raise RuntimeError('A selected file lacks its individual catalog entry')
    else:
        records=[describe(root,repository,rel) for rel in selected]
        data={'schema_version':'repository-appendix-file-inventory-v1','scope':'Git-tracked and deliberately selected publishable project files, plus this appendix. Excludes Git internal database, ignored raw inputs, environments and temporary/unselected runs.','count':len(records),'files':records}
        (out/'file_inventory.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
        (out/'file_catalog.md').write_text(render_catalog(records))
    checked,errors=check_links(root,repository)
    manifest=out/'diagrams/diagram_manifest.json'
    if manifest.is_file():
        for item in json.loads(manifest.read_text()).get('diagrams',[]):
            blocks=re.findall(r'```mermaid\n([\s\S]*?)```',(out/item['source_document']).read_text())
            source=blocks[item['mermaid_block']-1]
            if sha256(source.encode()).hexdigest()!=item.get('source_sha256'):errors.append('Stale rendered diagram source: '+item['svg_file'])
            if sha256((out/'diagrams'/item['svg_file']).read_bytes()).hexdigest()!=item.get('svg_sha256'):errors.append('Changed rendered diagram bytes: '+item['svg_file'])
    if errors:raise RuntimeError('\n'.join(errors))
    return {'status':'passed','files_documented':len(selected),'local_links_checked':checked,'raw_inputs_modified':False,'analysis_executed':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--repository',type=Path);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    print(json.dumps(build(repository=args.repository,check=args.check),indent=2))
