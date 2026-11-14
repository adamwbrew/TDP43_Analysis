"""Regenerate report source; execute_notebook.py must follow to save outputs."""
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]


def build():
    md = nbf.v4.new_markdown_cell
    code = nbf.v4.new_code_cell
    cells = [md("""# TDP43 COMET spatial PLA analysis

**Input audit and analysis readiness — no biological contrast calculated.**

This project follows the supplied *COMET spatial PLA analysis: Codex implementation instructions*, pp. 1–2. Both complete pages were read and visually inspected, including any annotation information (none present). The requested result is two separate maps of **Running − Homecage mean PLA counts per spatial bin**, using existing accepted alignment and existing tissue masks. The initial version prohibits new alignment, smoothing, interpolation, normalization and statistical tests.

**What is missing:** the numerical accepted transforms/reference, existing tissue masks, current section/animal/condition/arm mapping and rerun resolution, and an authoritative centroid definition/grid/coordinate geometry. The PDF names these requirements but does not supply their data. The available historical records remain provisional; no historical assignment, parameter or conclusion is imported as current evidence.

Read the saved outputs without running code. This notebook executes the input audit report and software checks; it stops spatial analysis while required inputs remain unresolved."""),
    code("""from pathlib import Path
import hashlib, importlib.metadata, json, os, platform, sys
ROOT = Path.cwd()
if not (ROOT / 'metadata/input_manifest.json').exists():
    raise RuntimeError('Run from the project repository root.')
sys.path.insert(0, str(ROOT))
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'tmp/matplotlib'))
from IPython.display import display, Image, Markdown
import pandas as pd
import numpy as np
manifest = json.loads((ROOT / 'metadata/input_manifest.json').read_text())
summary = json.loads((ROOT / 'outputs/inventory/summary.json').read_text())
audit = json.loads((ROOT / 'outputs/inventory/file_audit.json').read_text())
print('Python:', platform.python_version())
print('Current report: input audit and blocked-analysis readiness, not experimental spatial results.')"""),
    md("""## Question, design and intended decision

Where do the two conditions differ in spatial PLA object counts, separately for TDP43-HK1 and TDP43-PFKP? The maps will guide source-image review of supported regions. The new PDF documents two conditions and two arms, but does not give animal numbers, assignments, pairing, controls, tissue levels or treatment details (p. 1; IDs to preserve on p. 2).

The requested averaging unit is a **physical tissue section**. Animals are the biological experimental units; multiple sections/analyses of one animal are not independent animals. Equal-section weighting can differ from equal-animal weighting if section numbers differ. No inferential test is requested. Current sample metadata deliberately preserve unknown fields.

Rows are exported detected objects, not necessarily cells or individual molecules. Counts alone cannot demonstrate binding, metabolic activity or a causal effect of running."""),
    code("""sample_metadata = pd.read_csv(ROOT / 'metadata/sample_metadata.csv', keep_default_na=False)
display(sample_metadata)
print('Biological sample size and current section/condition assignments: unresolved.')"""),
    md("""## Input inventory and provenance

**Question:** what was actually supplied, and can the report be traced back to it?

**How to read:** each row below represents a file. Job numbers are filename tokens only; Analysis Region strings are literal export labels. The count of files is not the number of unique sections or animals. The inventory script read every CSV row and retained input hashes, column profiles and overlap evidence. The next cell verifies the bytes still match that inventory; it does not silently rescan or reinterpret the experiment."""),
    code("""def file_hash(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(8*1024*1024), b''):
            h.update(block)
    return h.hexdigest()

integrity = []
for m in manifest:
    path = Path(m['source_path'])
    if not path.is_file():
        path = ROOT / 'Initial Data' / m['relative_path']
    actual = file_hash(path) if path.is_file() else None
    integrity.append({'file_id': m['file_id'], 'available': path.is_file(), 'sha256_matches': actual == m['sha256']})
integrity_df = pd.DataFrame(integrity)
display(integrity_df)
if not all(r['sha256_matches'] for r in integrity):
    raise RuntimeError('Inputs missing or changed: refresh inventory and resolve provenance before relying on saved values.')
display(pd.DataFrame(manifest)[['file_id','job_token_from_filename','exported_analysis_regions','row_count','historical_byte_identical_copy_count']])
print(f\"{summary['source_csv_count']} CSVs; {summary['source_bytes']:,} bytes; {summary['total_exported_rows_including_possible_repeats']:,} export rows including repeats.\")
print('SHA-256-identical to historical reference files:', summary['source_files_identical_to_historical_reference'])"""),
    md("""**Supported finding:** all eight supplied CSVs are byte-identical to historical inputs. This proves file-copy identity, not current experimental assignment. The user supplied these files for this project; no extra permission to use them is needed.

**Uncertainty / next investigation:** identify the physical sections and ROIs represented by each export, distinguish alternative analyses from unique sections, and select the intended primary analysis before aggregation. The next figures describe exports, not condition effects."""),
    code("""from scripts.build_report import build
build()
display(Image(filename=str(ROOT / 'outputs/figures/input_export_counts.png'), width=1000))"""),
    md("""**Reading the export-count figure:** horizontal bars split each file's rows by the literal exported object-class label. Files with more rows do not receive more biological weight. Counts include possible repeated detections across exports; no cross-file total is an independent sample count.

**What to investigate next:** whether the overlapping exports are box-vs-outline analyses, different ROIs or reruns. No contour geometry is inferred from their labels."""),
    code("""overlap = pd.read_csv(ROOT / 'outputs/inventory/within_input_overlap.csv')
columns = ['left_file_id','right_file_id','measurement_signatures_shared_excluding_region_and_object_id','left_signature_shared_fraction','right_signature_shared_fraction']
display(overlap.sort_values('measurement_signatures_shared_excluding_region_and_object_id', ascending=False)[columns].head(8))
display(Image(filename=str(ROOT / 'outputs/figures/input_measurement_overlap.png'), width=800))"""),
    md("""**Reading the overlap figure:** entry (row, column) is the percentage of the row export's distinct measurement signatures also found in the column export. The signature includes all exported fields except Analysis Region and Object Id. The diagonal is 100% by definition; asymmetric values have different denominators. This is exact exported-value agreement, not validated biological object matching, and it ignores repeated identical-signature multiplicity.

**Supported finding:** four file pairs share approximately 91–95% of distinct measurement signatures. These are strong candidates for repeated/alternative analyses. **Uncertainty:** their intended sample/ROI relationship is not resolved by those numbers. **Next:** document inclusions and relationships; never concatenate them as new animals.

## Data dictionary and measurement limits

All 20 source fields are profiled, including missingness and numerical ranges. Header-labelled area/diameter units are preserved as export labels. They do not validate X/Y calibration. Bounding-box minima/maxima are present; no centroid-named field is present. Native exploratory maps explicitly reconstruct bounding-box midpoints. Whether that proxy is acceptable for the PDF's requested aligned-centroid calculation remains unresolved."""),
    code("""dictionary = pd.read_csv(ROOT / 'metadata/data_dictionary.csv', keep_default_na=False)
display(dictionary[['column','units_or_representation','observed_types','missing_count_all_files','limitations']])
scan_validation = json.loads((ROOT / 'outputs/inventory/validation.json').read_text())
assert scan_validation.get('status') == 'passed', 'Full input scan validation failed'
display(Markdown('**Full scan validation:**'))
display(scan_validation)"""),
    md("""## Required spatial computation

For each PLA arm, bin b and condition c, let V(c,b) contain only sections whose **existing mask contains the complete bin area**. Count each accepted aligned centroid once, separately per section. A fully covered empty bin contributes **0**; absent or partly covered tissue contributes **nothing** to numerator or denominator (p. 1).

Mean(c,b) = sum of counts from valid sections / number of valid sections.

Difference(b) = Mean(Running,b) − Mean(Homecage,b).

Display a difference only if each condition has at least one valid section. Retain both contributing-section counts beside it. Keep all grid edges, axis directions and masks in the same documented aligned reference. Existing transformations are applied without fitting a new alignment. Mask holes and full raster cell footprints matter; bin-centre tests, convex hulls and object occupancy do not implement 100% coverage.

Both difference maps must share symmetric color limits around zero. Missing coverage must look different from zero difference. Preserve the actual grid without smoothing/interpolation/normalization (p. 2)."""),
    code("""display(Image(filename=str(ROOT / 'outputs/figures/workflow.png'), width=1000))
from comet_spatial.manifest import preflight_manifest
preflight = preflight_manifest(ROOT / 'metadata/analysis_manifest.json')
(ROOT / 'outputs/preflight.json').write_text(json.dumps(preflight, indent=2) + '\\n')
print('Spatial status:', preflight['status'])
display(pd.DataFrame({'unresolved_check': preflight['blockers']}))
assert preflight['status'] == 'blocked', 'Manifest changed: run the spatial CLI and update the report with actual outputs before claiming results.'"""),
    md("""## Software acceptance checks

The following tests use **synthetic software fixtures only**. They are not the new experiment and no synthetic heatmap is presented as a result. They verify valid empty bins, strict boundary/hole coverage, raster geometry, single bin assignment, fixed transforms, separate-arm averaging, missing coverage and input provenance. The PDF's arithmetic example (Homecage 3/5/4; Running 7/8/9) must yield +4 (p. 2). A passing software test does not approve anatomical alignment."""),
    code("""import contextlib, io, unittest
suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'), pattern='test_*.py')
log = io.StringIO()
with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
    test_result = unittest.TextTestRunner(stream=log, verbosity=1).run(suite)
print(f'{test_result.testsRun} synthetic software checks; failures={len(test_result.failures)}, errors={len(test_result.errors)}')
if not test_result.wasSuccessful():
    print(log.getvalue())
(ROOT / 'outputs/test_log.txt').write_text(log.getvalue())
assert test_result.testsRun > 0 and test_result.wasSuccessful(), 'Acceptance tests failed'
validation = {'aligned_condition_analysis_status': preflight['status'], 'aligned_condition_maps_generated': False,
              'native_export_maps_generated': True, 'native_exports_computed': len(atlas['exports']),
              'input_hashes_verified': len(integrity), 'all_input_hashes_match': all(r['sha256_matches'] for r in integrity),
              'tests_run': test_result.testsRun, 'test_failures': len(test_result.failures), 'test_errors': len(test_result.errors),
              'scope': 'Full native object reconstructions and descriptive export measurements; historical results retained as context; no new aligned condition contrast.'}
(ROOT / 'outputs/validation.json').write_text(json.dumps(validation, indent=2) + '\\n')
print(json.dumps(validation, indent=2))"""),
    md("""## Historical reuse and verified scientific context

The full comparison in `docs/background_reuse.md` distinguishes remote main `4631e1517f85de2c4bfb59879bf44f406770a903` from local historical HEAD `f7fda4e36774b456c0e7b6df24f9666332198586`. Existing notebook/audit patterns, source hashing, standalone Plotly delivery and high-resolution exports are reusable. Historical ChAT fractions, morphology clusters, point-support maps, provisional feature alignment, animal assignments and thresholds are unsuitable substitutes for this new count-map contract.

Primary sources verified on 9 November 2026:

- [Söderberg et al., 2006, Nature Methods](https://www.nature.com/articles/nmeth947): PLA method context and assay specificity. Does not establish direct binding or calibrated molecule counts in these data.
- [Barone et al., 2026, Acta Neuropathologica](https://pubmed.ncbi.nlm.nih.gov/41838122/): TDP-43/HK1 disease-model mechanisms. Supplies motivation, not this study's result.
- [Manzo et al., 2019, eLife](https://elifesciences.org/articles/45114): functional glycolysis experiments in TDP-43 models. Does not establish mammalian PFKP interaction from spatial counts.
- [Navikas et al., 2024, Scientific Reports](https://www.nature.com/articles/s41598-024-55387-w): COMET spatial extraction workflow. Its masks and segmentation settings cannot be transferred here.

[Shapely covers](https://shapely.readthedocs.io/en/stable/reference/shapely.covers.html) supports the no-exterior-point full-bin test; [NumPy histogram2d](https://numpy.org/doc/stable/reference/generated/numpy.histogram2d.html) documents explicit-edge counts and axis conventions. See `docs/research_methods.md` for verified identifiers, applicability and limitations.

## Actionable next steps

1. Locate the existing accepted numerical transforms, reference figure and its plotting recipe; preserve their identities/hashes. The new PDF states that alignment is accepted, while the available older metadata have no approvals. Locate the intended assets rather than fitting or self-approving replacements.
2. Supply existing tissue masks with exact coordinate geometry, including raster cell edges if applicable. No masks are inferred from detections.
3. Complete current sample/ROI/repeated-export relationships from authoritative experimental records, keeping animal and section IDs distinct.
4. Document centroid definition, units, reference axes and common grid. If a midpoint proxy is intended, clarify it explicitly.
5. Run the preflight and spatial pipeline; compare the reproduced alignment check to its accepted reference and inspect source channels/segmentation before interpreting count differences.

The offline explorer at `outputs/app/native_explorer.html` helps inspect supplied exports. It does not rerun computation or fill missing scientific metadata. No original files were changed; no data were pushed or published.""")]
    audit_cells = cells
    # Native evidence leads the report. The detailed inventory remains available
    # after the scientific figures instead of serving as the main result.
    audit_cells[5].source = """display(pd.DataFrame(integrity))
display(pd.DataFrame(manifest)[['file_id','job_token_from_filename','exported_analysis_regions','row_count','historical_byte_identical_copy_count']])
print('Eight source hashes verified before the native analysis; detailed parsing validation is saved separately.')"""
    audit_cells[7].source = "display(Image(filename=str(ROOT / 'outputs/figures/input_export_counts.png'), width=1000))"
    cells = [md("""# TDP43 COMET: spatial evidence and scientific review

This report reconstructs **where the supplied detections lie**, compares measurements across overlapping exports, audits morphology and carries forward verified findings from the former PLA–ChAT project. Spatial maps, channel layers, shared scales, source-coordinate review and per-figure explanations now lead the report.

The current native reconstructions use bounding-box midpoints, not microscope pixels or accepted anatomical centroids. The former study's animal-level results remain explicitly historical. The requested aligned **Running − Homecage** count maps still require their existing masks, numerical transforms and current sample relationships. Those limits do not prevent useful spatial and measurement analysis of the supplied exports.

Open `outputs/app/native_explorer.html` for linked native maps/overlays, bin and layer controls, a 3D measurement view, paired-export review, object/bin inspection and historical figures. The app is an offline snapshot; its controls do not rerun the raw analysis."""),
    code("""from pathlib import Path
import hashlib, json, os, platform, sys
ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'tmp/matplotlib'))
from IPython.display import display, Image, Markdown
import pandas as pd
import numpy as np
manifest = json.loads((ROOT/'metadata/input_manifest.json').read_text())
summary = json.loads((ROOT/'outputs/inventory/summary.json').read_text())
audit = json.loads((ROOT/'outputs/inventory/file_audit.json').read_text())
def file_hash(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''):
            h.update(block)
    return h.hexdigest()
integrity=[]
for m in manifest:
    p=Path(m['source_path'])
    if not p.exists():
        p=ROOT/'Initial Data'/m['relative_path']
    integrity.append({'file_id':m['file_id'],'available':p.is_file(),'sha256_matches':p.is_file() and file_hash(p)==m['sha256']})
assert all(r['sha256_matches'] for r in integrity), 'Missing/changed raw inputs; resolve before analysis.'
from comet_spatial.native_atlas import build as build_native_atlas
atlas = build_native_atlas(ROOT, figures=True)
from scripts.build_findings import build as build_findings
facts=build_findings(ROOT)
from scripts.build_report import build as build_report
build_report()
print('Full native recomputation:',len(atlas['exports']),'exports;',summary['total_exported_rows_including_possible_repeats'],'rows; all eight SHA-256 checks pass.')
print('Saved raw-count maps use all detections. Display point samples do not determine summaries.')"""),
    md("""## What the current exports show

These are **descriptive export-level findings**, not animal-level treatment effects. Four strongly overlapping file pairs remain separate; counts are never summed as independent sections.

The following findings are calculated from the actual CSV rows. The association flag is the exported ChAT-present value on PLA objects; it does not establish neuron identity or physical molecular binding."""),
    code("""display(Markdown(f'''- **Spatial structure:** eight unsmoothed native count reconstructions and channel overlays are now available at three recorded bin widths.
- **ChAT flag among PLA:** {facts['association_flag_percent_range'][0]:.2f}%–{facts['association_flag_percent_range'][1]:.2f}% across exports, each using all PLA in its own denominator.
- **Alternative-export sensitivity:** four overlapping pairs differ by {facts['pla_count_relative_change_percent_range'][0]:+.2f}% to {facts['pla_count_relative_change_percent_range'][1]:+.2f}% in PLA count; flag fractions change {facts['association_change_percentage_point_range'][0]:+.2f} to {facts['association_change_percentage_point_range'][1]:+.2f} percentage points in the specified right-minus-left direction.
- **Morphology review:** {facts['unusable_diameter_ratio_pla_including_repeats']:,} PLA rows have unusable diameter ratios, including repeats; all remain in counts and association summaries.
- **Actionable image review:** {len(atlas['review_targets'])} bin-window selection records target high counts and supported association extremes; {len(atlas['morphology_object_review_targets'])} full-source object records target invalid/zero diameters and area extremes. Selections can overlap across reasons; these are not unique-object or prevalence counts.'''))"""),
    md("""## 1. Where are the PLA detections?

**Question:** where does the raw export contain more PLA detections per native bin?

**How to read:** each panel is one export in its own original coordinate frame. Count every PLA bounding-box midpoint once. The shared logarithmic **color display** helps reveal sparse and dense regions; the saved matrices remain raw counts. Bin width is 128 unverified export units in this static figure; the viewer offers 64/128/256. These are new recorded exploratory resolutions, not assumed physical calibration or inherited scientific thresholds.

**Evidence and limit:** repeated spatial patterns are visible in candidate overlapping exports. Pale zero-count bins say only that no exported midpoint fell there; they are not confirmed empty tissue. No outline, anatomy, registration, missing data or original pixel image is invented.

**Next:** inspect bins in the viewer and use the native source windows to review image channels, segmentation and export scope."""),
    code("""display(Image(filename=str(ROOT/'outputs/native_atlas/figures/native_pla_count_atlas.png'),width=1250))"""),
    md("""## 2. How do PLA and ChAT detections occupy the source fields?

**How to read:** gray marks are sampled ChAT-labelled detections; PLA markers distinguish the literal exported ChAT-presence flag. Every marker is a reconstructed midpoint. The app lets you toggle layers, inspect object IDs and boxes, and compare a selected native bin against the full raw-count map.

The display is balanced by class so the much larger ChAT class does not hide PLA. It is not a prevalence sample: total counts, fractions, histograms and review-window counts use all relevant rows. Spatial overlap of reconstructed points is not molecular colocalization, tissue coverage or cell identity. No image-space correspondence across different specimens is implied."""),
    code("""display(Image(filename=str(ROOT/'outputs/native_atlas/figures/native_layer_overlay_atlas.png'),width=1250))
display(Image(filename=str(ROOT/'outputs/native_atlas/figures/export_signal_profiles.png'),width=1100))
signal_table=pd.read_csv(ROOT/'outputs/native_atlas/export_findings.csv')
display(signal_table[['file_id','job_token','exported_region_label','pla_count','pla_with_chat_flag','pla_chat_flag_percent']])"""),
    md("""## 3. Do alternative exports change the measured outcome?

**Question:** do strongly overlapping exports yield exactly the same PLA count and ChAT-presence fraction?

**How to read:** each row compares a pair selected by its high agreement in exported measurements. The left panel changes PLA count relative to the left export; the right panel changes the ChAT-presence fraction in **percentage points**. The plots label their different denominators explicitly. They are comparisons of exported measurements, not condition contrasts or independent replications.

**Evidence:** these outputs differ even though many measurements match. **Uncertainty:** a shared signature does not prove biological object identity or resolve whether the exports are ROI alternatives or reruns. **Next:** compare the linked native maps and record the intended source/inclusion decision before section-level averaging. Do not choose a primary export on the basis of a preferred biological result."""),
    code("""display(Image(filename=str(ROOT/'outputs/native_atlas/figures/overlapping_export_sensitivity.png'),width=1100))
display(pd.read_csv(ROOT/'outputs/native_atlas/overlapping_export_sensitivity.csv'))"""),
    md("""## 4. Which morphology measurements deserve review?

**How to read:** dots are PLA area medians, thick intervals the interquartile range and thin intervals the 1st–99th percentiles. These are object distributions, not animal uncertainty or confidence intervals. The x axis is logarithmic; its area units are literal HALO header units with unverified calibration. The right panel reports the fraction/count lacking a usable **minimum / maximum diameter** ratio.

A zero minimum with a positive maximum is retained as a valid ratio of zero. A nonpositive maximum or invalid/nonfinite diameter pair is excluded only from that ratio. Those objects remain in every raw-count and ChAT-presence summary. **Next:** inspect questionable sizes/diameters in source images before interpreting morphology or fitting any model. No clustering has been added to these current data."""),
    code("""display(Image(filename=str(ROOT/'outputs/native_atlas/figures/export_morphology_quality.png'),width=1100))
targets=pd.read_csv(ROOT/'outputs/native_atlas/review_targets.csv')
display(Markdown('**Source-image review windows:** selected examples for follow-up, not prevalence estimates. Counts and flags come from the source export; native windows are not tissue ROIs.'))
display(targets.head(16))"""),
    md("""Morphology targets below are selected from the **complete source objects**, independently of the capped display sample. They retain exact object IDs and source-record numbers, bounding boxes, measurements and reasons. An object can be selected for more than one reason. Review does not remove it from count or association denominators."""),
    code("""morphology_targets=pd.read_csv(ROOT/'outputs/native_atlas/morphology_object_review_targets.csv')
display(morphology_targets.head(16))"""),
    md("""## 5. Verified former findings and the visual practices carried forward

The previous analysis used the **historical expanded PLA–ChAT dataset**: twelve retained sections, six animals, three animals per condition. Its saved results are shown here as historical context with checked provenance. They are not recalculated from the current eight overlapping exports, and their group assignments do not become current metadata.

The main transferable practices are specimen-level displays, explicit denominators, shared map scales, native channel overlays, sensitivity comparisons, source-coordinate review and a question/evidence/limit/next explanation for every major result. The new viewer brings these practices into the current project without promoting old registration proposals into accepted anatomy."""),
    code("""history=json.loads((ROOT/'outputs/native_atlas/historical_context.json').read_text())
for row in history['rows']:
    display(Markdown(f\"### {row['title']}\\n\\n**Historical finding:** {row['finding']}\\n\\n**Evidence:** {row['evidence']}\\n\\n**Limit:** {row['limitation']}\\n\\n**Practice transferred / next:** {row['next_step']}\"))
for figure in history['figures'][:2]:
    display(Markdown('**'+figure['caption']+'**'))
    display(Image(filename=str(ROOT/figure['path']),width=1100))
print('Historical remote main:',history['remote_main'],'; see source hashes in historical_context.json.')"""),
    md("""## 6. Scope of the requested aligned comparison

Native reconstructions, descriptive export fractions and historical context are supporting analyses. The PDF's initial **aligned Running − Homecage count maps** retain their original contract: reuse accepted transforms/masks, strict full-bin coverage, valid zeros, section means, separate arms and no smoothing, normalization or tests. An optional native association map in the explorer has a different, explicitly shown denominator and is not that requested condition map.

The preflight below lists the missing numerical assets and sample relationships. It does not stop native exploration, and no native display proposes a new alignment or tissue mask. The 3D surface in the app shows a bin measurement as height; height is not anatomical depth."""),
    *audit_cells[2:]]
    notebook = nbf.v4.new_notebook(cells=cells, metadata={"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.12"}})
    nbf.write(notebook, ROOT / 'TDP43_native_supporting_analysis.ipynb')


if __name__ == '__main__':
    build()
