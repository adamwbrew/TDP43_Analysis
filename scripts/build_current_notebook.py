"""Current scientific report for the 14 November scientist-directed policy."""
from pathlib import Path
import nbformat as nb

ROOT = Path(__file__).resolve().parents[1]


def measurement_cells():
    return [nb.v4.new_markdown_cell('''## Spatial calculation functions · scientist update, 17 November 2026

The one-page calculation-functions PDF requests **13 section-level measurements** and **three comparisons**. The **19 November extension** adds six complementary measurements, bringing the current catalog to **19**: section PLA share, ChAT-associated share of PLA area, median PLA intensity, area interquartile range, area coefficient of variation and mean same-section nearest-neighbor distance. These additions answer the user's follow-up; they were not in the PDF. Size categories retain the adjustable default cutoff of **0.1 exported µm²**. ChAT is the only available non-PLA marker flag; HK1 and PFKP remain separate PLA arms.

Calculate each measurement per section and bin, then average defined section values equally within each condition. **Counts and summed areas retain assumed empty-bin zeros. Means, medians, 90th percentiles and fractions are undefined when their required objects are absent.** A marker-associated area mean needs associated PLA objects, not merely any PLA. Measurement-defined section N is shown separately from observed-object support N.

Comparisons follow the condition means: signed `R − H` (the PDF's `absolute_difference`), `100 × (R − H) / H`, or `log₂(R / H)`. A zero Homecage mean makes percent change undefined; zero Running with positive Homecage gives −100%. Log ratios require positive means in both conditions. No pseudocount is added. Fraction differences remain fractions, not automatically percentage points.

**Preserved scope:** existing object positions, saved transforms, four grids and current mask-free plotting domain are unchanged. The PDF's request to retain existing masks/100% coverage is recorded against the scientist-directed coverage policy agreed on 14 November; no masks or complete tissue coverage are invented. Source values come from `Area (µm²)`, `Average Intensity` and the ChAT-presence flag on PLA-class rows. Area labels do not independently calibrate X/Y distances or fluorescence intensity.

The tables below audit all **19 measurements × three comparisons × two arms × four grids**. A persistent pale footprint and thin outline preserve the location context when a statistic or ratio is undefined. This follows detected-object bins on the finest original 100-unit grid; it does not establish tissue boundaries or fill missing statistics. Detail figures use a disclosed shared color cap at the 95th percentile of nonzero absolute comparisons; saturated bins are counted and full-range companions retain all extremes. SVG exports retain vector tiles and boundaries rather than embedded map screenshots.

**What the additions answer:** section share shows where each section's PLA detections are concentrated, reducing the influence of unequal section totals while introducing its own compositional denominator. The area-associated fraction complements the count-associated fraction by weighting measured area. Median intensity and area IQR describe robust central tendency and spread; area CV uses population SD divided by positive mean and requires at least two objects in a bin. These do not correct acquisition, segmentation or tissue area. Same-section nearest-neighbor spacing is computed exactly from all PLA midpoint proxies before binning. It is not recomputed within each display bin or zoom window, and never joins animals. Duplicate positions give zero distance. Exported distance units are unverified; detection density, boundary truncation and missing objects affect interpretation, so no clustering or anatomical distance conclusion is claimed.

The app's detail window can genuinely rebin the original points at **100, 50, 25 or 10 exported-coordinate units**; the global comparison retains its original four grids. Smaller bins expose more spatial detail and often fewer defined objects/sections. An 8,000- or 12,000-pixel PNG increases export sharpness; it does not add measured biology. True vector SVG retains every calculated tile at arbitrary viewing magnification. All source PLA points remain available without sampling.

Read `docs/calculation_functions.md`, `metadata/calculation_functions_policy.json` and `metadata/spatial_extensions_policy_2026-11-19.json` for definitions, exact zero/missing rules and provenance. Official [NumPy quantile](https://numpy.org/doc/stable/reference/generated/numpy.quantile.html), [NumPy standard deviation](https://numpy.org/doc/stable/reference/generated/numpy.std.html) and [SciPy nearest-neighbor](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.cKDTree.query.html) documentation specify the numerical methods; no spatial interpolation is performed.'''),
    nb.v4.new_code_cell('''from pathlib import Path as _FunctionPath
import json as _function_json
import numpy as _function_np
import pandas as _function_pd
from IPython.display import display as _function_display, Image as _FunctionImage
from scripts.build_measurement_report import build as _build_function_report
from comet_spatial.measurement_features import build_feature_cache as _build_function_features
_function_root = _FunctionPath.cwd()
if not (_function_root/'outputs/measurement_features/latest_run.json').is_file():
    _build_function_features(_function_root)
function_run = _build_function_report(_function_root)
function_report = _function_json.loads((function_run/'report.json').read_text())
function_summary = _function_pd.read_csv(function_run/'summary.csv')
_function_display(function_summary.query("bin_width == 100 and comparison == 'absolute_difference'")[['measurement','arm','units','defined_comparison_bins','undefined_eligible_bins','homecage_metric_N_0','running_metric_N_0']])
print('All 19 measurements × 3 comparisons × 2 arms × 4 grids:', len(function_summary), 'summary rows')
print('Original PLA count results unchanged:', function_report['validation']['existing_PLA_count_results_unchanged'])
print('Large + small count partition conserved:', function_report['validation']['large_small_partition_conserved'])
print('No pseudocounts:', not function_report['validation']['pseudocounts_added'])
for _function_name in ['marker_associated_pla_count_absolute_difference_detail_100', 'mean_pla_area_absolute_difference_detail_100', 'pla_count_log2_fold_change_detail_100', 'section_pla_share_absolute_difference_detail_100', 'marker_associated_pla_area_fraction_absolute_difference_detail_100', 'mean_pla_nearest_neighbor_distance_absolute_difference_detail_100']:
    _function_display(_FunctionImage(filename=str(function_run/'figures'/(_function_name+'.png')),width=1450))
print('600-DPI examples plus full-range companions:', function_run/'figures')
print('Every section value, defined N, condition mean and all comparisons:', function_run/'resolution_100')
print('Blank statistics are not zero; tissue coverage remains uncertain.')''')]


def build():
    md, code = nb.v4.new_markdown_cell, nb.v4.new_code_cell
    cells = [md('''# COMET spatial PLA · spatial measurements and condition comparisons

The current analysis follows the scientist’s answers relayed on **14 November 2026**: use the former app’s twelve completed sections and saved alignment, average **all three sections per condition**, treat empty section-bins as zero, then subtract **Running − Homecage**. Tissue coverage remains uncertain. Original images, outlines, distance labels and 3D reconstruction are not required for this exploratory comparison.

The three visual families are the separate HK1/PFKP condition differences, detailed 2D alignment review, and four observed-support maps. Each difference is accompanied by its two condition means. All 310,024 exported PLA locations remain available for object-level inspection in the offline app. The **17 November calculation-functions update** supplied 13 measurements and three comparison choices; the **19 November extension** brings the catalog to 19 and adds persistent object-footprint context, finer local rebinning and high-resolution/vector exports. The fixed-three rule below applies to counts and summed areas; object statistics and fractions average defined section values.

**Change from the earlier report:** the old estimator divided by the number of sections containing objects in a bin. The current denominator is always three. Old results remain preserved in `outputs/exploratory/`, `outputs/exploratory_multiresolution/` and the archived notebook under `outputs/revisions/before_fixed_three_means_2026-11-14/`; their conclusions are not silently reused.

Open `outputs/app/index.html` to explore saved results. No rerun is needed for viewing. This notebook derives current means from previously raw-validated counts by default. Set `TDP43_RECOUNT_RAW=1` before execution for a full raw recount first.'''),
    code('''from pathlib import Path
import hashlib, json, os, sys
import numpy as np
import pandas as pd
from IPython.display import display, Image, Markdown
ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
os.environ.setdefault('MPLCONFIGDIR', str(ROOT/'tmp/matplotlib'))
from scripts.build_section_mean_maps import build as build_means, locate_run
from scripts.build_section_mean_figures import build as build_mean_figures
from scripts.build_review_figures import build as build_review_figures

raw_recomputed = os.environ.get('TDP43_RECOUNT_RAW') == '1'
if raw_recomputed:
    from comet_spatial.exploratory import run_exploratory_maps
    from comet_spatial.multiresolution import build_multiresolution_maps
    baseline = run_exploratory_maps(ROOT/'metadata/analysis_manifest.json', ROOT/'metadata/exploratory_authorization.json', ROOT/'outputs/exploratory')
    build_multiresolution_maps(ROOT/'metadata/analysis_manifest.json', ROOT/'metadata/exploratory_authorization.json', ROOT/'outputs/exploratory_multiresolution', baseline_directory=baseline)
source_path = locate_run(ROOT, 'exploratory_multiresolution')
source_bytes = source_path.read_bytes()
source_sha = hashlib.sha256(source_bytes).hexdigest()
run = build_means(ROOT)
result = json.loads((run/'view_payload.json').read_text())
figure_manifest = build_mean_figures(ROOT)
review = build_review_figures(ROOT)
sections = result['resolutions']['100']['sections']
section_table = pd.DataFrame([{k:s[k] for k in ['section_id','animal_id','condition','pla_type','source_rows','pla_objects','chat_objects']} for s in sections])
display(section_table)
print('Current immutable run:', run)
print('Raw CSVs recounted in this execution:', raw_recomputed)
print('Source payload SHA-256:', source_sha)
print('Objects:', result['validation']['source_totals'])
print('All selected PLA midpoint proxies:', result['validation']['full_pla_point_count'])'''),
    md('''## Design, measurements and averaging rule

Six animals supply twelve completed physical sections: Homecage **21F, 23M, 24M**, Running **22F, 21M, 22M**. Each animal has one HK1 section and a separate PFKP section. The arms are analyzed separately and do not provide independent replications of animals. Interrupted job 4978 is superseded by completed job 5403 and remains audit-only; historical duplicate exports are not concatenated.

The independent biological unit is the **animal: three per condition**. Rows are detected objects, not automatically cells or molecules. Positions are bounding-box midpoint proxies transformed by the unchanged saved reflection/translation matrices. No registration is refitted. The scientist confirms that the anatomical regions and prior alignment are sufficient for the current comparison; this does not turn object footprints into complete tissue masks.

For section s and bin b let P(s,b) be its raw PLA count. For each condition:

`Mean(b) = [P(section 1,b) + P(section 2,b) + P(section 3,b)] / 3`

`Difference(b) = Running mean(b) − Homecage mean(b)`

**Empty section-bins contribute assumed zero**, as explicitly directed by the user. These are not verified tissue-covered zeros. The display domain is the union of bins containing any exported PLA or ChAT object in any of the six sections within that arm. Outside that domain the map is blank; full-grid arithmetic zeros remain in numerical matrices/tables. A location with an entirely empty condition remains displayed when the other condition has objects there.

Observed support N counts sections containing ≥1 PLA or ChAT object. It is now a diagnostic, **never the averaging denominator**. Four common grids are retained (1,000, 500, 250 and 100 export units); the app opens at 100-unit resolution (250 × 240 bins). Physical distance is unverified and no physical scale bars are supplied. There is no smoothing, interpolation, normalization or statistical testing.'''),
    code('''# Independent checks of every current mean, difference, support diagnostic and global count.
checks = []
for width, payload in result['resolutions'].items():
    for arm, arrays in payload['arms'].items():
        union = np.asarray(arrays['displayable'], bool)
        verified = {}
        for condition, prefix in [('Homecage','homecage'), ('Running','running')]:
            group = [s for s in payload['sections'] if s['pla_type']==arm and s['condition']==condition]
            assert len(group)==len({s['animal_id'] for s in group})==3
            total = sum(np.asarray(s['pla_counts'], dtype=np.int64) for s in group)
            observed = sum((np.asarray(s['pla_counts'])+np.asarray(s['chat_counts'])>0).astype(int) for s in group)
            mean = total/3
            assert np.array_equal(observed, np.asarray(arrays[prefix+'_observed_section_n']))
            assert np.allclose(np.where(union,mean,np.nan), np.asarray(arrays[prefix+'_mean'],float),equal_nan=True)
            assert np.isclose(mean.sum(), sum(s['pla_objects'] for s in group)/3)
            verified[condition] = mean
        difference = verified['Running']-verified['Homecage']
        assert np.allclose(difference,np.asarray(arrays['raw_arithmetic_difference']))
        assert np.allclose(np.where(union,difference,np.nan),np.asarray(arrays['difference'],float),equal_nan=True)
        checks.append({'bin_width':int(width),'arm':arm,**payload['statistics'][arm]})
assert hashlib.sha256(source_path.read_bytes()).hexdigest()==source_sha
assert source_path.read_bytes()==source_bytes
assert sum(len(p['x']) for p in result['pla_points'])==310024
validation_table = pd.DataFrame(checks)
display(validation_table[['bin_width','arm','displayable_bins','whole_condition_zero_bins_displayed','minimum_difference','maximum_difference']])
print('All four resolutions independently verified; historical count payload unchanged.')
display(section_table.groupby(['pla_type','condition']).agg(sections=('section_id','size'),exported_PLA=('pla_objects','sum'),mean_PLA_per_section=('pla_objects','mean')))
print('Exported totals are descriptive counts, not tissue-area-adjusted biological abundance.')'''),
    md('''## 1 · Detailed condition difference maps

**Question:** where do the three-section mean raw PLA counts differ between Running and Homecage, separately for each PLA arm?

**How to read:** blue is lower mean count in Running, red is higher, white is zero difference. Gray lies outside the arm’s observed-object display domain. Both arms share a symmetric linear scale around zero. The first export shows the full numerical range. The second uses a clearly labeled ±25 display range to reveal smaller differences; extreme bins saturate in color and retain their exact values in hover and tables. PNG exports are 600 DPI; SVGs retain exact bin geometry.

**Evidence and limits:** each included object is counted once, each animal’s section has weight 1/3, and an entirely object-empty section-bin contributes zero by assumption. Fine bins reveal exported spatial detail but do not add animals, validate complete tissue sampling, or establish statistical significance. Bin width changes the quantity counted, so compare scales with care.

**Next:** compare the two underlying means, inspect the six individual section counts and examine support diagnostics at a feature. A count difference can reflect biological, staining, segmentation or sampling differences; this analysis alone cannot distinguish them.'''),
    code('''display(Image(filename=str(run/'figures/section_mean_differences_100.png'),width=1450))
display(Image(filename=str(run/'figures/section_mean_differences_contrast_100.png'),width=1450))
display(validation_table.query('bin_width == 100')[['arm','negative_difference_bins','positive_difference_bins','zero_difference_bins','fixed_section_denominator']])'''),
    md('''### The two means behind each subtraction

The left and middle columns show Homecage and Running means on one shared sequential scale across both arms and conditions. The right column shows the exact subtraction with one shared signed scale. A mean of zero can include bins assumed empty under the agreed rule; **coverage remains uncertain**. These are raw counts per bin, not density per tissue area and not the former project’s ChAT-associated PLA percentage outcome.'''),
    code('''display(Image(filename=str(run/'figures/section_means_and_difference_contrast_100.png'),width=1600))
print('Detail colours: means 0–25, differences ±25; saturated bins are counted in every panel. Exact values are unchanged.')
print('Full-range companion:', run/'figures/section_means_and_difference_100.png')'''),
    md('''## 2 · Detailed 2D alignment and object review

**Question:** where are the detected objects in the saved aligned frame, and do apparent group features occur in more than one section?

**How to read:** each atlas shows all exported PLA midpoint proxies for one arm, with Homecage sections above Running sections. Faint background tiles mark observed PLA/ChAT support rather than tissue boundaries. Every selected PLA point is retained, with no display sampling. The app provides aligned overlays, native/fixed views and local source-object inspection. No physical Z or serial reconstruction is used.

**Evidence:** the original twelve fixed matrices are unchanged, and the original alignment-check image remains pixel-identical to its historical reference. The scientist has accepted reuse for this exploratory comparison. Reproduction checks verify computational provenance; they do not independently validate biology.

**Next:** inspect consistency across all three animals and compare group features with individual sections. Object maps establish exported locations, not fluorescence intensity, cell identity, direct molecular binding or complete tissue coverage.'''),
    code('''replay = json.loads((ROOT/'outputs/comet_core/alignment_replay_validation.json').read_text())
reference = ROOT/'outputs/comet_core/figures/alignment_check_reference.png'
reproduced = ROOT/'outputs/comet_core/figures/alignment_check_reproduced.png'
assert reference.read_bytes()==reproduced.read_bytes()
assert hashlib.sha256(reference.read_bytes()).hexdigest()==replay['reference_sha256']
assert replay['transforms_unchanged'] and replay['pixel_identical_to_saved_reference']
for arm in ['hk1','pfkp']:
    display(Image(filename=str(ROOT/'outputs/comet_core/detailed_review'/('alignment_detail_'+arm+'.png')),width=1600))
print('Original fixed alignment retained. No 3D reconstruction or new fit.')'''),
    md('''## 3 · Observed support, with a fixed mean denominator

**Question:** which sections contain exported objects at each location, and where does the zero assumption matter most?

**How to read:** N=0,1,2,3 are four discrete colors. N counts sections with at least one PLA or ChAT detection. N=0 means no detections; N=3 means all three sections have detections. Neither proves tissue presence or full-bin coverage. The mean denominator stays **three at every displayed location**, regardless of N. For a condition with N=1, the remaining two section-bins contribute assumed zero.

**What this supports:** an audit of detection support and sensitivity to empty-bin assumptions, alongside the requested all-three-section average. The app links selected bins to a six-section table and detailed points. **Next:** inspect whether a contrast comes from broad agreement or one section; retain the stated coverage uncertainty when reporting it.'''),
    code('''display(Image(filename=str(ROOT/'outputs/comet_core/detailed_review/observed_support_detail_100.png'),width=1450))
support_rows=[]
for arm, arrays in result['resolutions']['100']['arms'].items():
    for condition,prefix in [('Homecage','homecage'),('Running','running')]:
        n=np.asarray(arrays[prefix+'_observed_section_n'])
        domain=np.asarray(arrays['displayable'],bool)
        support_rows.append({'arm':arm,'condition':condition,'mean_denominator':3,
                             **{f'displayed_bins_observed_N_{i}':int(((n==i)&domain).sum()) for i in range(4)}})
display(pd.DataFrame(support_rows))'''),
    md('''## Scientific scope, provenance and rerun

The original instruction PDF p. 1 §§3–4 defines a different strict method: whole-bin tissue-mask containment and a mask-valid section denominator. The later scientist/user answers authorize the current mask-free fixed-three exploratory comparison. The old strict test has **not** been passed and is preserved separately; it is not a gate on the now-authorized analysis.

Inputs, assignments and exclusions are recorded in `metadata/cohort_selection.json` and `metadata/selected_section_metadata.csv`. The exact updated rule is in `metadata/scientist_directed_mean_policy.json`; scientist statements are in `docs/scientist_clarifications_2026-11-14.md`. There are no pending scientist questions for the agreed comparison. Scientific limitations remain explicit rather than converted into new asset requests.

```mermaid
flowchart LR
    A[12 completed exports, six animals] --> B[Unchanged saved alignment]
    B --> C[Per-section PLA and ChAT bin counts]
    C --> D[Sum three PLA sections / 3 per condition]
    D --> E[Running minus Homecage, arms separate]
    C --> F[Observed support and all PLA points]
    E --> G[600 DPI figures, tables and offline app]
    F --> G
    C --> H[19 per-section measurements and defined-section means]
    H --> I[Three comparisons with fixed object-footprint context]
    I --> J[Exact finer local bins and vector or 8k/12k exports]
```

This run reuses validated raw-count arrays by default, derives new immutable means and exports saved figures. The historical source payload is hash-checked before/after. Set `TDP43_RECOUNT_RAW=1` to recount the twelve CSVs first. The README has exact environment and execution commands. Nothing is moved, pushed or published.'''),
    code('''from scripts.build_comet_core_report import build as build_report
report = build_report(ROOT)
print('Offline app rebuilt:', report)
print('600-DPI exported figures:', len(figure_manifest['figures'])+len(review['figures']))
print('Tables:', run/'resolution_100/hk1_bins.csv', 'and pfkp_bins.csv')
print('Current policy:', ROOT/'metadata/scientist_directed_mean_policy.json')
validation_path=ROOT/'outputs/validation.json'
validation=json.loads(validation_path.read_text())
validation.update(current_analysis='Nineteen per-section spatial measurements, defined-section condition means, three comparisons and fixed object-footprint context; coverage uncertain.',
    fixed_three_section_means_generated=True, fixed_section_denominator={'counts_sums_and_section_share':3,'object_statistics_and_fractions':'Number of defined section measurements, 0–3'},
    empty_bin_policy={'counts_sums_and_section_share':'assumed_zero; section share requires a positive section total','object_statistics_and_fractions':'undefined'},
    tissue_coverage_verified=False, current_run_directory=str(function_run), count_run_directory=str(run),
    measurement_count=19,comparison_count=3,summary_table_rows=len(function_summary),
    scientific_policy='metadata/calculation_functions_policy.json',spatial_extension_policy='metadata/spatial_extensions_policy_2026-11-19.json',
    raw_recomputed_this_execution=raw_recomputed, historical_count_source_sha256=source_sha,
    all_fixed_three_means_independently_verified=True, full_pla_point_provenance_count=310024,
    alignment_transforms_unchanged=True, high_resolution_png_dpi=600,
    current_notebook_scope='All current report cells executed using validated saved raw counts and matched object attributes, including exact same-section nearest-neighbor spacing; full raw recount is optional.',
    scientist_questions_pending=0)
validation_path.write_text(json.dumps(validation,indent=2)+'\\n')''')]
    position=next(i for i,c in enumerate(cells) if c.cell_type=='markdown' and c.source.startswith('## Scientific scope, provenance and rerun'))
    cells[position:position]=measurement_cells()
    notebook=nb.v4.new_notebook(cells=cells)
    notebook.metadata={'kernelspec':{'display_name':'Python 3 (TDP43)','language':'python','name':'python3'},
                       'language_info':{'name':'python','version':'3.12'},
                       'scientific_policy':'2026-11-19 nineteen section-level measurements; zero extensive/undefined intensive; uncertain coverage'}
    nb.write(notebook, ROOT/'TDP43_COMET_analysis.ipynb')
    print('Current notebook source generated; execute to save results.')


if __name__=='__main__':
    build()
