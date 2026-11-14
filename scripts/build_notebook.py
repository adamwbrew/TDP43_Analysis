"""Build the actual exploratory-results notebook; execute to save outputs."""
from pathlib import Path
import nbformat as nbf
ROOT = Path(__file__).resolve().parents[1]


def review_cells():
    """A self-contained presentation update that can reuse validated raw results."""
    return [nbf.v4.new_markdown_cell('''## Detailed alignment and observed-support review

The app's alignment and observed-support tabs now use the same selected fine grid as the difference maps. The alignment view can show every selected PLA midpoint, per-section count tiles and individual section detail while preserving the original transforms and the original reproduced check. The support view uses four discrete colors for N=0,1,2,3, larger condition comparisons and a local section-membership view.

**How to read these saved figures:** the first four panels count sections with detected PLA or ChAT objects in each 100-unit bin. The following atlases show all PLA midpoint proxies separately for every section, Homecage above Running, on the unchanged aligned field. The faint background only marks bins with observed exported objects. It is not a tissue boundary.

**What this supports:** a detailed check of where exported detections occur and which sections enter the exploratory denominator. **What remains uncertain:** full tissue coverage, source fluorescence, anatomical correspondence and physical distance. Neither a dense point cloud nor N=3 establishes complete tissue coverage. The interactive stack's Z spacing is a viewing control, not physical depth.

Scientists are asked eight questions about biological intent, anatomical sampling, saved images/outlines, excluded regions, measured object centers, processing consistency, treatment and assay controls. They can provide existing records or an imaging contact. File conversion, coordinate mapping and code validation belong to the analysis team and imaging analyst; see `docs/technical_handoff_requirements.md`.'''),
    nbf.v4.new_code_cell('''from pathlib import Path as _ReviewPath
from IPython.display import display as _review_display, Image as _ReviewImage
from scripts.build_review_figures import build as _build_review_figures
_review_root = _ReviewPath.cwd()
_review_figures = _build_review_figures(_review_root)
for _review_name in ['observed_support_detail_100', 'alignment_detail_hk1', 'alignment_detail_pfkp']:
    _review_display(_ReviewImage(filename=str(_review_root/'outputs/comet_core/detailed_review'/(_review_name+'.png')), width=1350))
print('Presentation figures from validated saved arrays; no raw recomputation or new alignment fit.')
print('All PLA positions retained:', _review_figures['full_pla_point_count'])
print('Scientist questions: docs/scientist_questions.md')
print('Internal implementation handoff: docs/technical_handoff_requirements.md')''')]


def build_historical_observed_support_report():
    md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
    cells = [md('''# COMET spatial PLA: calculated exploratory maps and alignment review

**The two difference maps and four observed-support maps below are calculated from the selected raw data.** The prior alignment check is reproduced unchanged. The user authorized these exploratory calculations on 11 November 2026 while retaining the strict PDF results as pending.

The three visual families are:

1. **HK1 and PFKP difference heatmaps:** Running − Homecage mean raw PLA count per bin among sections with observed-object support.
2. **The previous alignment check:** the identical saved six-panel check, plus flat/3D interactive review with saved anchors, section controls and camera presets.
3. **Four observed-support maps:** contributing-section N for each condition and PLA arm, defined by detected PLA or ChAT objects rather than independently supplied tissue masks.

**Scope:** bounding-box midpoints approximate object positions. Observed support does not establish full-bin tissue coverage. These are the explicitly authorized exploratory results; the PDF's strict tissue-mask analysis remains pending.

Open `outputs/app/index.html` for the connected offline explorer. It opens with the calculated maps. Use its analysis-mode selector to inspect the separate pending strict-PDF view. A minimum observed-section filter hides low-support difference bins without changing their saved means or common color scale.'''),
    code('''from pathlib import Path
import hashlib, json, os, sys
ROOT = Path.cwd()
assert (ROOT/'metadata/exploratory_authorization.json').exists(), 'Run from the repository root.'
sys.path.insert(0, str(ROOT))
os.environ.setdefault('MPLCONFIGDIR', str(ROOT/'tmp/matplotlib'))
from IPython.display import display, Image, Markdown
import numpy as np
import pandas as pd
from comet_spatial.exploratory import run_exploratory_maps
from scripts.build_exploratory_figures import build as build_figures
from scripts.build_comet_core_report import build as build_report
# Full raw recomputation: every selected CSV is hashed before and after counting.
run = run_exploratory_maps(ROOT/'metadata/analysis_manifest.json',
                          ROOT/'metadata/exploratory_authorization.json', ROOT/'outputs/exploratory')
figure_result = build_figures(run)
report = build_report(ROOT)
result = json.loads((run/'view_payload.json').read_text())
findings = json.loads((run/'findings.json').read_text())
print('Calculated raw-data run:', run)
print('All source rows:', f"{result['validation']['source_totals']['source_rows']:,}")
print('PLA:', f"{result['validation']['source_totals']['pla_objects']:,}", 'ChAT:', f"{result['validation']['source_totals']['chat_objects']:,}")
print('Outside shared grid:', result['validation']['source_totals']['outside_grid_objects'])
print('Figures exported:', figure_result['figures'], 'PNG + SVG, 300-DPI PNGs')
print('Scientific status: authorized exploratory; strict tissue-mask PDF results pending.')'''),
    md('''## Experimental design, measurements and denominator

The selected cohort contains **six animals and twelve completed sections**, with one section per animal in each separate PLA arm. Homecage animals are 21F, 23M and 24M; Running animals are 22F, 21M and 22M. The same animals occur in both arms, so the arms do not provide independent biological replication. Animal identities and assignments come from the prior scientific handoff and the user's explicit selection of this exact cohort, linked to current source copies by SHA-256.

Interrupted export 4978 remains an audit input and is superseded by completed export 5403. The original eight alternative exports are not concatenated with this cohort.

**Positions:** `(XMin+XMax)/2, (YMin+YMax)/2`, followed by the unchanged saved section transform. These are bounding-box midpoints, not measured segmentation centroids or original fluorescence pixels. The shared 25 × 24 grid has 1,000 export-unit bins; X increases right and Y downward. Physical calibration is unverified. The separate arm reference frames are preserved without claiming cross-arm anatomical homology.

For section s and bin b, P is its raw PLA count and A its raw PLA + ChAT count. Define observed support O = `A > 0`. Within each condition and arm, `N_observed = sum(O)` and `Mean_observed = sum(P where O) / N_observed`. Subtract **Running − Homecage**, and display a difference only if each condition has N_observed ≥ 1.

A ChAT-only bin contributes PLA count zero. A bin with no exported objects is excluded from that section's exploratory mean; its tissue coverage remains unknown. This data-dependent support can omit real empty tissue and retain partially sampled edges. It is not the PDF's strict 100% mask-containment test.'''),
    code('''sections = result['sections']
section_table = pd.DataFrame([{k:s[k] for k in ['section_id','animal_id','condition','pla_type','source_rows','pla_objects','chat_objects','outside_grid_objects']} for s in sections])
display(section_table)
print('Biological sample size: three animals per condition; displayed objects and bins do not increase animal N.')
display(Markdown('Full source names, hashes and assignments: `metadata/selected_section_metadata.csv`.'))'''),
    md('''## 1 · Two calculated exploratory difference heatmaps

**Question:** where do observed-support mean PLA counts differ between Running and Homecage, separately for HK1 and PFKP?

**How to read:** blue means lower observed-support mean count in Running; red means higher. White is zero observed-count difference. Gray means one condition has no observed support at that bin. Both arms use **one symmetric, linear scale centered at zero**, preserved axes and exact bin edges. There is no smoothing, interpolation, area normalization or inferential test.

**Evidence:** every included PLA object is assigned once from the raw export; the means average section counts rather than pooled object observations. The table below describes spatial bins, which are correlated and are not independent biological replicates. The color limits are determined jointly from the actual signed differences, not from former ChAT-association results.'''),
    code('''display(Image(filename=str(run/'figures/exploratory_differences_two_arms.png'), width=1200))
difference_summary = pd.DataFrame([{'arm':arm, **{k:f[k] for k in ['displayable_bins','all_three_sections_per_condition_bins','lower_observed_support_comparison_bins','negative_difference_bins','positive_difference_bins','zero_difference_bins','minimum_difference','maximum_difference']}} for arm,f in findings['arms'].items()])
display(difference_summary)
for arm,f in findings['arms'].items():
    display(Markdown(f"**{arm}:** {f['negative_difference_bins']} of {f['displayable_bins']} comparable bins have a negative Running − Homecage difference; {f['positive_difference_bins']} are positive and {f['zero_difference_bins']} are exactly zero. The observed difference range is {f['minimum_difference']:.2f} to {f['maximum_difference']:.2f} PLA counts per bin."))'''),
    md('''**What this supports:** a description of the spatial distribution and magnitude of differences in the exported detections under the authorized support rule. It does not establish an exercise effect, direct binding, cell identity, metabolic flux or statistical significance.

**What remains uncertain:** sampled tissue area, segmentation/acquisition comparability, exact anatomical correspondence, irregular-object centroid error and the possibility that support selection changes the denominator. A broad negative count pattern can coexist with spatially localized positive bins; it is not the former project's ChAT-associated PLA percentage outcome.

**Next:** read the underlying condition means and support maps, inspect the six section contributions to a selected bin, then review source channels and segmentation at the exported native-coordinate windows. The interactive app exposes means, per-section PLA/ChAT counts, bin boundaries and a link from the selected bin to alignment review.'''),
    code('''display(Image(filename=str(run/'figures/exploratory_condition_means.png'), width=1100))
global_counts = section_table.groupby(['pla_type','condition'], sort=False).agg(sections=('section_id','size'),exported_pla_total=('pla_objects','sum'),mean_pla_per_export=('pla_objects','mean')).reset_index()
display(global_counts)
print('Global counts are descriptive exported detections, not tissue-area-adjusted abundance. A sum of variable-denominator spatial means is not an animal total.')'''),
    md('''## 2 · The unchanged previous alignment check

**Question:** does the review show the saved former alignment rather than a newly fitted registration?

**How to read:** rows are separate PLA arms; columns show native coordinates, saved cavity translation, and saved translation plus discrete reflection. Colors identify animals. Crosses mark the saved cavity origins. These outline displays reconstruct occupied detection grids, not tissue masks or original image pixels.

**Evidence:** all twelve saved transformation matrices are replayed exactly, and the regenerated original six-panel PNG matches its reference pixel-for-pixel. No fitting, scaling, arbitrary rotation or warping is performed. The PDF's instruction to reuse alignment is preserved; old proposed/unreviewed flags remain visible source provenance.

**Limits and next:** identical rendering verifies reproduction, not anatomical correspondence. The app offers flat/native/fixed views, section stepping, opacity, saved cavity/cue guides and cameras. Adjustable stack Z is display separation, not measured section depth. Use the source microscope images for biological review.'''),
    code('''def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
replay = json.loads((ROOT/'outputs/comet_core/alignment_replay_validation.json').read_text())
snapshot = json.loads((ROOT/'outputs/comet_core/alignment_snapshot.json').read_text())
assert sha(ROOT/'outputs/comet_core/alignment_snapshot.json') == replay['snapshot_sha256']
reference = ROOT/'outputs/comet_core/figures/alignment_check_reference.png'
reproduced = ROOT/'outputs/comet_core/figures/alignment_check_reproduced.png'
assert sha(reference) == replay['reference_sha256'] and sha(reproduced) == replay['reproduced_png_sha256']
assert reference.read_bytes() == reproduced.read_bytes() and replay['pixel_identical_to_saved_reference']
saved_by_job = {s['job']:s for s in snapshot['sections']}
manifest = json.loads((run/'manifest_snapshot.json').read_text())
for s in manifest['sections']:
    assert np.array_equal(s['transform']['matrix'], saved_by_job[s['job']]['fixed_transform_matrix'])
print('Twelve original matrices unchanged; saved reference and regenerated PNG identical.')
display(Image(filename=str(reproduced), width=1200))'''),
    md('''## 3 · Four calculated observed-support maps

**Question:** how many sections have exported objects in each bin, for each condition and PLA type?

**How to read:** the integer scale runs from 0 to 3 sections. N=0 means no exported PLA or ChAT objects in that condition/bin; it does **not** establish absent tissue. N=3 means all three sections have at least one detected object, but does **not** establish 100% coverage of the bin. The four panels use the same axes, edges and N scale.

**Evidence:** each N matrix is the sum of the corresponding section support indicators. ChAT-only bins increase N while contributing zero PLA. These maps reveal changing denominators and edge uncertainty behind the exploratory differences.

**Next:** prefer inspecting regions supported by more sections, and obtain the actual tissue annotations to replace observed support with the required complete-mask test. No true tissue-coverage map is claimed here.'''),
    code('''display(Image(filename=str(run/'figures/observed_support_four_panels.png'), width=1100))
support_summary = []
for arm,d in result['arms'].items():
    for condition,key in [('Homecage','homecage_n'),('Running','running_n')]:
        n = np.asarray(d[key])
        support_summary.append({'arm':arm,'condition':condition, **{f'bins_with_N_{i}':int((n==i).sum()) for i in range(4)}})
display(pd.DataFrame(support_summary))'''),
    md('''## Observed-support sensitivity: require all three sections in each condition

This view hides bins unless both conditions have detected objects in all three sections. It uses **the same saved means, differences and color limits**. It does not refit alignment, change counts or establish full tissue coverage.

**How to read:** compare the broad pattern with the first figure and identify where lower-support edge bins were removed. This is a display sensitivity check, not a confidence interval or an inferential test. The app offers minimum observed N values of 1, 2 or 3.'''),
    code('''display(Image(filename=str(run/'figures/exploratory_differences_all_three_observed.png'), width=1200))
sensitivity = pd.DataFrame([{'arm':arm, **row} for arm,f in findings['arms'].items() for row in f['observed_support_sensitivity']])
display(sensitivity)
print('Counts refer to spatial bins, not independent samples. Even N=3 observed support does not establish complete tissue coverage.')'''),
    md('''## Source-coordinate review targets

The next table links the most negative and most positive difference bin in each arm back to every section's raw PLA and ChAT counts. The complete table includes exact aligned bounds, inverse-transformed native-coordinate windows, source identifiers and paths in `selected_bin_review_windows.csv` inside the saved run.

These are selected extremes for microscopy/segmentation review, not representative samples or validated anatomical hotspots. Inspect original channels, giant/merged objects, thresholding, image placement, clipping and assay controls before biological interpretation. Original pixels have not been supplied; the project cannot perform that image-level validation itself.'''),
    code('''targets = pd.read_csv(run/'selected_bin_review_windows.csv')
display(targets[['arm','review_reason','section_id','condition','aligned_x_min','aligned_y_min','section_pla_count','section_chat_count','observed_support','running_minus_homecage']])
print('Native review windows:', run/'selected_bin_review_windows.csv')'''),
    md('''## Strict PDF results remain pending

The original PDF, pp. 1–2, requires existing tissue masks, complete bin containment, valid tissue-covered zeros and exclusion of even partially uncovered section-bins. Observed objects cannot establish those properties. The original strict analysis manifest is unchanged by this exploratory authorization.

The scientist-ready request is `docs/scientist_questions.md`: eight plain-language questions about the experiment and existing scientific records. The analysis team and imaging analyst handle file conversion, coordinate mapping and source-object linkage using `docs/technical_handoff_requirements.md`. Existing tissue outlines and the intended object-position measurement remain the strict analysis inputs to resolve. The user explicitly requested exploratory maps while keeping strict PDF results pending; this decision is recorded in `metadata/exploratory_authorization.json`.

The workflow is: verified raw objects → fixed alignment → one recorded shared grid → per-section PLA/ChAT counts → observed-support N and section means → separate Running − Homecage differences → linked figures and source review. Actual masks enable the separate strict workflow later.'''),
    code('''strict = json.loads((ROOT/'outputs/core_view/payload.json').read_text())
assert strict['status']=='blocked' and not strict['arms']
assert result['strict_pdf_results'] is False and result['strict_pdf_results_pending'] is True
assert result['validation']['count_conservation_passed']
# Independently check saved per-section supports, arm means, Ns and subtraction.
for s in sections:
    pla, chat = np.asarray(s['pla_counts']), np.asarray(s['chat_counts'])
    assert np.array_equal(np.asarray(s['observed_support']), (pla+chat)>0)
for arm,d in result['arms'].items():
    means={}
    for condition,key in [('Homecage','homecage'),('Running','running')]:
        part=[s for s in sections if s['pla_type']==arm and s['condition']==condition]
        n=sum(np.asarray(s['observed_support'],int) for s in part)
        total=sum(np.asarray(s['pla_counts']) for s in part)
        mean=np.divide(total,n,out=np.full(n.shape,np.nan),where=n>0)
        assert np.array_equal(n,np.asarray(d[key+'_n']))
        assert np.allclose(mean,np.asarray(d[key+'_mean'],float),equal_nan=True)
        means[condition]=mean
    assert np.allclose(means['Running']-means['Homecage'],np.asarray(d['difference'],float),equal_nan=True)
validation_path=ROOT/'outputs/validation.json'
validation=json.loads(validation_path.read_text())
validation.update(scope='Actual authorized exploratory raw-count differences and observed-section support, with unchanged saved alignment. Strict tissue-mask results remain pending.',
    exploratory_maps_generated=True, exploratory_raw_counts_recomputed=True,
    exploratory_run_directory=str(run), exploratory_source_totals=result['validation']['source_totals'],
    exploratory_input_hashes_verified_before_and_after=True, exploratory_matrices_independently_checked=True,
    aligned_condition_analysis_status='strict_pdf_pending', aligned_condition_maps_generated=False,
    strict_coverage_maps_generated=False, strict_pdf_results_pending=True,
    alignment_replay_pixel_identical=True, alignment_transforms_unchanged=True)
validation.update(multiresolution_maps_generated=True,
    multiresolution_run_directory=str(multi_run),
    multiresolution_widths_export_units=[1000,500,250,100],
    multiresolution_source_totals=multires['validation']['source_totals'],
    full_pla_point_provenance_count=multires['validation']['full_pla_point_count'],
    original_1000_unit_arrays_matched=multires['validation']['baseline_1000_comparison']['matched'],
    exact_refinement_checks=multires['validation']['exact_refinement_checks'],
    multiresolution_matrices_independently_checked=True,
    supporting_analysis_scope='Original eight-export native/morphology results remain separate; new aligned exploratory contrasts use the selected twelve completed exports.')
validation_path.write_text(json.dumps(validation,indent=2)+'\\n')
print('Actual raw counts, saved means, observed Ns and signed differences verified.')
print('Strict tissue-mask difference/coverage outputs remain uncalculated.')
print('Full software check log: outputs/test_log.txt')'''),
    md('''## Methods, provenance and rerun instructions

The main notebook recomputes the selected raw exports, exports figures and rebuilds the offline app. Each numerical run is retained under `outputs/exploratory/`; it contains source and authorization snapshots, section matrices, full selected PLA source-row/object/native/aligned provenance, separate arm means/differences/N, parameters, validation and high-resolution figures. `latest_run.json` identifies the current snapshot. No raw source file is changed and nothing is pushed or published.

Read `docs/exploratory_methods.md` for exact formulas and limitations, `docs/results_guide.md` for the figure overview, `docs/comet_alignment_asset_trace.md` for unchanged alignment provenance, and `docs/research_methods.md` for the verified primary-method references. Earlier ChAT-fraction/morphology findings remain separate supporting results, not expected values for these count maps.

To view, open the saved notebook or `outputs/app/index.html`; no rerun is needed. To recompute with raw inputs present, use the project environment and `python scripts/execute_notebook.py TDP43_COMET_analysis.ipynb`. The executor saves only after every code cell completes without errors. The README provides environment setup and standalone numerical/figure commands.''')]
    detail_cells = [md('''## Detailed heatmaps and linked section review · 12 November 2026

**Question:** what spatial variation is hidden by the original 25 × 24 grid, and which animals contribute to a local pattern?

The following maps genuinely recount all raw objects on 1,000-, 500-, 250- and 100-export-unit grids. The default app view uses 250 units (100 × 96 bins, 16 times as many as the original). The finest view uses 100 units (250 × 240 bins, 100 times as many). The aligned field and every saved transform stay unchanged. Physical calibration remains unknown.

**How to read:** both arms share the same symmetric linear signed scale within each resolution. Bin areas and color limits change between resolutions; equal colors across resolutions are not equal effects at a fixed scale. Finer bins have fewer contributing sections, so compare observed N alongside the difference. No interpolation, smoothing, normalization or statistical tests are added.

The app links zoomed maps to region-level condition views, six individual-section count maps and all selected PLA midpoint locations. These dots reconstruct detections; they are not fluorescence pixels, measured segmentation centroids, cell identities or a tissue mask. Point provenance retains object IDs, source rows and native coordinates.'''),
    code('''from comet_spatial.multiresolution import build_multiresolution_maps
from scripts.build_detailed_figures import build as build_detailed_figures
multi_run = build_multiresolution_maps(ROOT/'metadata/analysis_manifest.json',
    ROOT/'metadata/exploratory_authorization.json', ROOT/'outputs/exploratory_multiresolution',
    baseline_directory=run)
detail_figures = build_detailed_figures(multi_run)
multires = json.loads((multi_run/'view_payload.json').read_text())
assert multires['validation']['baseline_1000_comparison']['matched']
assert multires['validation']['full_pla_point_count'] == result['validation']['source_totals']['pla_objects']
assert multires['validation']['full_pla_point_count_matches_raw']
print('Fresh multi-resolution raw-data run:', multi_run)
print('Full PLA locations retained:', multires['validation']['full_pla_point_count'])
print('Original 1,000-unit section and condition arrays reproduced exactly.')
display(pd.read_csv(multi_run/'resolution_summary.csv'))
display(Image(filename=str(multi_run/'figures/detailed_differences_250.png'), width=1300))
display(Image(filename=str(multi_run/'figures/detailed_differences_100.png'), width=1300))'''),
    md('''### Resolution sensitivity and the means behind a fine-grid difference

**Evidence:** each raw section count is conserved at every resolution; counts on nested grids add exactly to their parent bins. Observed support and condition means are recalculated from those counts, rather than averaged from an old map. The 250- and 100-unit grids are not nested in one another; both subdivide 500 units.

**Limits:** the observed-support denominator itself depends on detection density and changes with grid width. A sharper map is not automatically a more reliable biological map. Empty object bins cannot reveal whether tissue was present. Selected fine-scale extremes need source-image review and independent masks.

Use the four-resolution atlas to assess resolution dependence, then inspect the individual condition means and support Ns. The atlas intentionally labels each resolution's scale limits.

Large outliers compress smaller differences toward white on the full scale. A supplementary **±25-count linear display** below shows smaller differences more clearly. Beyond-range bins saturate at the endpoints and are counted in each title; their exact values remain in the uncapped full-range figures and saved arrays. This changes color display only, not counts, means, support or biological inference.'''),
    code('''display(Image(filename=str(multi_run/'figures/resolution_sensitivity.png'), width=1500))
display(Image(filename=str(multi_run/'figures/fine_detail_contrast_100.png'), width=1300))
display(Image(filename=str(multi_run/'figures/detailed_means_100.png'), width=1100))
display(Image(filename=str(multi_run/'figures/detailed_support_100.png'), width=1100))'''),
    md('''### Six individual-section maps per arm

**Question:** does a group feature appear across animals, or mainly in one exported section?

Each panel is one animal's physical section at 100-unit resolution. All twelve section maps share one linear raw-count scale. Gray means no exported objects; a supported bin can have zero PLA if ChAT is present. Compare these maps with the group means; three animals per condition remain the independent biological sample size. Different sections in the two arms do not establish cross-arm anatomical homology.

**Next:** inspect the exact object IDs/native locations in the app's region view and request the corresponding fluorescence channels and segmentation overlays. These maps alone cannot distinguish staining, segmentation, sampling and biological explanations.'''),
    code('''display(Image(filename=str(multi_run/'figures/individual_sections_hk1_100.png'), width=1350))
display(Image(filename=str(multi_run/'figures/individual_sections_pfkp_100.png'), width=1350))
# Independently verify the saved finer-grid section means and missing values.
for width, payload in multires['resolutions'].items():
    assert payload['strict_pdf_results'] is False
    for arm, arrays in payload['arms'].items():
        verified_means = {}
        for condition, key in [('Homecage','homecage'),('Running','running')]:
            selected = [s for s in payload['sections'] if s['pla_type']==arm and s['condition']==condition]
            total = sum(np.asarray(s['pla_counts'], dtype=np.int64) for s in selected)
            n = sum((np.asarray(s['pla_counts'])+np.asarray(s['chat_counts'])>0).astype(int) for s in selected)
            mean = np.divide(total,n,out=np.full(n.shape,np.nan),where=n>0)
            assert np.array_equal(n,np.asarray(arrays[key+'_n']))
            assert np.allclose(mean,np.asarray(arrays[key+'_mean'],float),equal_nan=True)
            verified_means[condition] = mean
        assert np.allclose(verified_means['Running']-verified_means['Homecage'],np.asarray(arrays['difference'],float),equal_nan=True)
report = build_report(ROOT)
print('All four resolutions independently checked; detailed offline app rebuilt:', report)
print('Scientist clarification checklist: docs/scientist_questions.md')''')]
    detail_cells.extend(review_cells())
    insert = next(i for i,c in enumerate(cells) if c.cell_type=='markdown' and c.source.startswith('## Strict PDF results'))
    cells[insert:insert] = detail_cells
    cells[0].source += '\n\n**Detail update, 12 November 2026:** the report also saves freshly recounted four-resolution comparisons, fine condition/support maps and individual-section atlases. The app defaults to 250-unit bins and retains a 100-unit view plus linked exact-PLA-point inspection. The original 1,000-unit results below remain the baseline, not the current app default.'
    notebook=nbf.v4.new_notebook(cells=cells)
    notebook.metadata={'kernelspec':{'display_name':'Python 3 (TDP43)','language':'python','name':'python3'}, 'language_info':{'name':'python','version':'3.12'}}
    nbf.write(notebook,ROOT/'TDP43_COMET_analysis.ipynb')
    print('Exploratory-results notebook source rebuilt; execute to save all calculated outputs.')


def build():
    # The 14 November scientist/user clarification supersedes the old report's
    # variable observed-section denominator. The old generator remains auditable.
    from scripts.build_current_notebook import build as build_current
    build_current()


if __name__=='__main__':
    import sys
    sys.path.insert(0, str(ROOT))
    build()
