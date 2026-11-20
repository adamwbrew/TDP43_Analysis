# Spatial measurements and condition comparisons

The scientist's **COMET Spatial Heatmaps: Calculation Functions**, supplied on 17 November 2026, specifies the first 13 measurements and three condition comparisons on **page 1**. Six exploratory additions on **19 November** bring the total to **19 measurements**. The additions preserve the cohort, fixed alignment, object positions, grid and coverage diagnostics. The default remains **PLA count** with **Running minus Homecage**. The source PDF's SHA-256 and the implemented decisions are recorded in [the calculation policy](../metadata/calculation_functions_policy.json).

## What is preserved, and what coverage means

Each arm has three Homecage and three Running animal sections. HK1 and PFKP remain separate; the same six animals occur in both arms. Each PLA detection retains its full-precision bounding-box midpoint proxy and unchanged saved transform. The current data do not contain measured centroids, and no object is moved or resampled to add these calculations.

Page 1 asks to retain existing masks and a 100% tissue-coverage rule. The actual current analysis preserves the [scientist-directed policy agreed on 14 November](scientist_clarifications_2026-11-14.md): empty section-bins contribute assumed zero for counts, and tissue coverage is uncertain. This extension preserves that existing implementation. It does **not** introduce tissue masks or claim that the historical 100% containment test has been passed.

The plotting domain remains each arm's union of bins containing any exported PLA or ChAT object across its six sections. A bin outside that domain stays blank. Within the domain, a section with no detections can supply an assumed zero count even though tissue presence is unknown. Observed-section N is still a detection-support diagnostic; it is not a verified tissue count or, for the new intensive measurements, the number of defined section values.

## The 19 measurements

The first 13 definitions implement the PDF's page 1 table; rows 14–19 are the subsequent additions. Compute them **per section, per bin**, before any averaging across animals. Let `n` be the bin's total PLA count, `a` an individual PLA object's exported area, `t` the selected area cutoff and `m` its selected-marker association flag. The default `t` is **0.1**; `a >= t` includes equality. The units are those of the export, whose area column is labeled `Area (µm²)`; physical calibration has not been independently verified.

| # | Measurement / saved ID | Per-section calculation | Empty-bin result / units |
|---|---|---|---|
| 1 | PLA count / `pla_count` | Count all selected PLA detections | 0; PLA detections per bin |
| 2 | Large PLA count / `large_pla_count` | Count PLA with `a >= t` | 0; PLA detections per bin |
| 3 | Small PLA count / `small_pla_count` | Count PLA with `a < t` | 0; PLA detections per bin |
| 4 | Large PLA fraction / `large_pla_fraction` | Large PLA count divided by `n` | Missing if `n = 0`; fraction from 0 to 1 |
| 5 | Mean PLA area / `mean_pla_area` | Sum of PLA areas divided by `n` | Missing if `n = 0`; exported area units |
| 6 | Median PLA area / `median_pla_area` | Median of PLA object areas | Missing if `n = 0`; exported area units |
| 7 | 90th-percentile PLA area / `p90_pla_area` | 90th percentile of PLA object areas | Missing if `n = 0`; exported area units |
| 8 | Total PLA area / `total_pla_area` | Sum of all PLA object areas | 0; exported area units per bin |
| 9 | Mean PLA intensity / `mean_pla_intensity` | Mean exported `Average Intensity` across PLA objects | Missing if `n = 0`; exported intensity units |
| 10 | Marker-associated PLA count / `marker_associated_pla_count` | Count PLA whose selected-marker flag is 1 | 0; PLA detections per bin |
| 11 | Marker-associated PLA fraction / `marker_associated_pla_fraction` | Marker-associated PLA count divided by `n` | Missing if `n = 0`; fraction from 0 to 1 |
| 12 | Marker-associated large PLA count / `marker_associated_large_pla_count` | Count marker-associated PLA with `a >= t` | 0; PLA detections per bin |
| 13 | Marker-associated PLA mean area / `marker_associated_pla_mean_area` | Mean area among marker-associated PLA | Missing if no associated PLA; exported area units |
| 14 | Section PLA share / `section_pla_share` | `100 * n / total PLA count in this same physical section` | 0 for an empty bin when section total is positive; percent of that section's PLA |
| 15 | Marker-associated PLA area fraction / `marker_associated_pla_area_fraction` | Sum of associated PLA areas divided by sum of all PLA areas in the bin | Missing if total PLA area is 0; fraction from 0 to 1 |
| 16 | Median PLA intensity / `median_pla_intensity` | Median exported intensity of PLA detections | Missing if `n = 0`; exported intensity units |
| 17 | PLA area interquartile range / `pla_area_iqr` | 75th-percentile PLA area minus 25th-percentile PLA area | Missing if `n = 0`; 0 is valid with one object; exported area units |
| 18 | PLA area coefficient of variation / `pla_area_cv` | Population standard deviation of PLA area divided by mean area | Requires at least two PLA objects and positive mean area; unitless ratio |
| 19 | Mean PLA nearest-neighbor distance / `mean_pla_nearest_neighbor_distance` | For each PLA object, distance to its closest other PLA in the same section; mean those distances for objects in the bin | Missing without objects or without another object anywhere in the section; unverified export-coordinate units |

Medians and percentiles use the type-7 linear sample quantile, specified in the [official NumPy documentation](https://numpy.org/doc/stable/reference/generated/numpy.quantile.html). This interpolates between ranked **object measurements** when needed; it does not interpolate the spatial map. Large and small are configurable measurement categories, not validated biological object types.

The area IQR uses that same quantile definition for Q75 and Q25. The area CV uses population standard deviation with divisor `n` (`ddof=0` in [NumPy's standard-deviation definition](https://numpy.org/doc/stable/reference/generated/numpy.std.html)), then divides by the bin's mean PLA area. It is stored as a ratio, not multiplied by 100. Requiring two objects prevents a single detection from appearing to establish zero size variability; a positive mean is required to avoid division by zero.

Only **ChAT** is currently available as a marker selection. Its source is `ChAt-50 - FITC_E1 present` on the **PLA object's row**. Separate ChAT-class detections supply support/context maps; counting those objects is not a substitute for the association flag. A ChAT-associated PLA detection is not proof of cell identity, direct protein binding or a causal mechanism.

The associated-area fraction is weighted by detected area, while the existing associated-PLA fraction is weighted by object count. The two can differ when associated objects have different sizes. Section PLA share uses the **same physical section's** complete PLA count as its denominator, not a condition total, tissue area or a cross-arm pool. It describes how exported detections are distributed within that section and does not establish acquisition-adjusted abundance. A signed difference between two shares reported in percent is measured in percentage points; the separately selected percent-change comparison is a relative change.

### What nearest-neighbor distance establishes

Distances use the full, unchanged two-dimensional aligned PLA point set **within each physical section**. For every detection, find the nearest other detection, including one outside its bin, and then average distances for detections whose own positions fall inside the bin. Binning therefore does not artificially restrict the search to the selected tile. Sections and animals are never combined for the neighbor search, and the neighbors are PLA detections rather than separate ChAT detections.

The distances are precomputed exactly using [SciPy `cKDTree.query`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.cKDTree.query.html), with Euclidean distance and no approximation. A second detection at the same coordinate gives a valid zero distance; this does not merge identities or prove that two detections represent distinct biological structures. A section containing only one detection has no defined neighbor distance.

This is a descriptive summary of exported midpoint spacing. Coordinate calibration is unverified, and segmentation, missed detections, overall detection density and unobserved neighbors outside the sampled field can alter it. It has no tissue-boundary edge correction. The [official spatial point-pattern documentation](https://search.r-project.org/CRAN/refmans/spatstat.explore/html/Gest.html) explains why unobserved neighbors beyond the observation window can bias inference. This analysis does not estimate a corrected nearest-neighbor distribution, test clustering, measure cell spacing or demonstrate colocalization. Inspect individual sections and counts before interpreting a distance contrast.

## Average sections first, then compare conditions

For a selected measurement, calculate one section-level value in each bin. Average the defined values equally within Homecage to obtain `H`, and within Running to obtain `R`. There are three animal sections available per condition. This equal-section method prevents sections with many objects from automatically receiving more weight.

For counts and summed areas, an empty bin contributes 0, so all three sections enter the mean when their required attributes are valid. Section PLA share also contributes 0 for an empty bin when the section-wide denominator is positive. For object means, medians, percentiles and within-bin fractions, an empty bin contributes no defined value; CV additionally requires two objects and positive mean area. The condition mean therefore uses one, two or three defined sections, or remains missing when none is defined. The app and numerical output report **measurement-defined section N** for each condition. That N can differ from observed-support N: a ChAT-only bin has observed support but no PLA area mean, and an associated-PLA mean needs an associated PLA object.

For example, three section counts of 0, 4 and 8 average to 4. Three section area means of missing, 0.2 and 0.4 average to 0.3 with defined-section N = 2. A condition mean of section medians is the average of those medians; it is not the median of all pooled objects.

| Comparison ID | Calculation after condition averaging | Reading the sign / units |
|---|---|---|
| `absolute_difference` (default) | `R - H` | **Signed** difference in the selected measurement's units. Positive means higher Running. The name does not mean `abs(R - H)`. |
| `percent_change` | `100 * (R - H) / H` | Relative change using Homecage as the denominator, in percent. This differs from a percentage-point difference between two fractions. |
| `log2_fold_change` | `log2(R / H)` | A log2 ratio: +1 means twice the Homecage mean; -1 means half. Requires both means to be strictly positive. |

The comparisons are applied to condition means, not averaged object-level or section-pair ratios. No pseudocount, offset, automatic imputation or hidden clipping is introduced. The two arms share a symmetric, zero-centered linear comparison scale for the selected measurement and comparison. Display caps affect color only; exact values and missingness remain available.

For **section PLA share**, the underlying measurement is already in percent, so signed `R - H` uses **percentage points**. For the original fraction-valued measurements, signed `R - H` stays in **fraction units**: 0.2 corresponds to 20 percentage points. Selecting `percent_change` instead always uses the relative Homecage denominator; it is a different calculation.

## Missing values and zero decisions

These implement the page 1 notes while preserving the current uncertain-coverage policy.

| Situation | Result | Consequence for averaging or display |
|---|---|---|
| No PLA in a section-bin; selected measurement is a count or summed area | 0 under the agreed assumed-zero policy | Section contributes zero; tissue presence is still uncertain |
| Empty section-bin; selected measurement is section PLA share | 0 when that section's complete PLA count is positive | Section contributes zero; no division by a pooled condition count |
| Section has no PLA anywhere; selected measurement is section PLA share | Missing | No section-total denominator is manufactured |
| No PLA in a section-bin; measurement requires PLA objects | Missing | Section does not enter that measurement's condition mean |
| PLA present, but none is marker-associated | Associated counts and object-count fraction are 0; area fraction is 0 if total area is positive; associated mean area is missing | Defined N depends on the selected measurement |
| Sum of all PLA areas in a bin is 0 | Associated-area fraction is missing | Object-count association fraction can still be defined if PLA exists |
| One PLA object in a bin | Area IQR is 0; area CV is missing | A single object does not establish a size-variability ratio |
| Two or more PLA objects, but mean area is 0 | Area CV is missing | Positive mean area is required |
| Two different same-section PLA detections share a coordinate | Their nearest-neighbor distance can be 0 | Retain both object identities; zero is a valid observed distance |
| A section contains only one PLA detection | Nearest-neighbor distance is missing | The section cannot supply a nearest-other-object value |
| A required object attribute or marker flag is unavailable, malformed, nonfinite or negative | Dependent section-bin measurement is missing | No silent removal of an inconvenient object; affected condition N is reported |
| No defined section value in a condition | That condition mean is missing | All three comparisons are missing |
| `H = 0`, including `R = H = 0` | Percent change is missing | A zero denominator is not a zero percent change |
| `R = 0` and `H > 0` | Percent change is -100%; log2 fold change is missing | No finite log ratio is manufactured |
| `H <= 0` or `R <= 0` | Log2 fold change is missing | Requires positive means in both conditions |
| Bin outside the unchanged plotting domain | Blank, with outside-domain reason | Neither an observed zero nor a claim about tissue coverage |

The initial added attribute extraction retained all 310,024 selected PLA detections and reported no invalid area, intensity or ChAT-flag entries. The rules above also define behavior if a future input has unavailable attributes. A numerical zero and an undefined value are never interchangeable.

## How to use the new controls

Open the existing app and use the measurement and comparison selectors in the differences view. Changing the area cutoff affects the large/small categories and large fraction; marker controls affect the five associated measurements. The supported marker list reflects actual exported flags, so it currently contains ChAT only. The selected grid, alignment review, full object positions and support maps remain connected to the same data.

Read the measurement name, comparison and units before interpreting color. Inspect both condition means, their defined-section N and section contributions at a location. Percent and log2 maps can emphasize bins with small reference means; a vivid color alone does not establish a robust anatomical pattern. Check consistency across the three animals and the area-cutoff sensitivity before selecting a scientific follow-up. No additional significance test or machine-learning conclusion is inferred.

### Fine detail and persistent spatial context

Whole-field calculations retain their original 1,000-, 500-, 250- and 100-unit grids. A detailed window defaults to **25-unit bins**, with **100, 50, 25 and 10** available. Each local grid is calculated directly from saved full-precision object positions and their matched attributes, rather than enlarging or interpolating a coarse heatmap. Regular grid bounds extend outward to cover the requested window; all objects within that grid extent are counted, and the display crops to the requested view. The terminal upper grid edge is included in the last bin, consistent with the measurement engine.

All twelve sections remain in the local calculation. Section PLA share retains the complete physical-section PLA denominator, even when most objects lie outside the displayed window. Nearest-neighbor distance retains the previously computed full-section distances; it does not search for new neighbors only inside the cropped window. Each condition still averages defined section measurements with equal animal weights. Fine bins reveal more local variation and missingness, not more animals or calibrated microscopy resolution.

The unchanged 100-unit observed-object domain supplies local plotting eligibility by each fine bin's center. A fine bin's inherited eligibility is context from the source domain, not a newly validated tissue mask. Grids are limited to 400 rows and 400 columns to keep interactive calculations manageable. If the requested grid is larger, the app selects a coarser supported width and displays a notice; if even the coarsest width cannot fit, choose a smaller window.

The default-on **Detected-object footprint** outline is derived from that fixed 100-unit union of observed PLA/ChAT bins, preserving its gaps. It stays visible when a selected measurement or comparison becomes undefined, so missing metric values do not erase the spatial context. Its geometry does not change with metric selection, cutoff, comparison or local grid width. The outline is not a full tissue boundary and does not create values in undefined bins or extend eligibility.

### Downloads

Choose **Whole aligned field**, **Current map zoom** or **Fine detailed window**, then select the arm's **PNG** or **SVG** button. PNGs are fixed at **8,000 pixels wide**, with height preserving aspect ratio. SVGs retain vector bin tiles and the observed-domain outline.

PNG size does not change the calculated spatial bins. For finer bins, choose **Open fine detail**, set **Spatial detail: calculated bin width**, then download **Fine detailed window**. **Current map zoom** crops the existing global grid. Saved 600-DPI figures remain a separate library; exact values and defined-section N remain available for checking patterns.

## Saved files and rerunning

The [attribute-cache pointer](../outputs/measurement_features/latest_run.json) selects area, intensity and marker vectors matched exactly to the existing ordered PLA identities and coordinates. Source hashes and object/source-row matches are checked. The old count cache alone cannot reconstruct these attributes. The added `nearest_neighbor_distance` vector is derived from the same complete per-section midpoint arrays, with source geometry and neighbor-search parameters recorded; no microscopy pixels are required. Report/app rebuilds and cached notebook reruns extend older complete attribute caches automatically, saving a new immutable run and its predecessor hash without rereading or modifying raw CSVs. No extra nearest-neighbor extraction command is needed.

The [calculation-run pointer](../outputs/calculation_functions/latest_run.json) selects the numerical report and representative 600-DPI figures. Parameters record the measurement, comparison, cutoff, marker, grid, defined-section counts, missing-comparison reasons and source provenance. The app can explore other supported settings from its embedded full-precision cache without changing object positions. Representative saved figures do not imply that every possible cutoff has a precomputed figure.

With the selected count and feature caches present:

```bash
python scripts/build_measurement_report.py
python scripts/build_comet_core_explorer.py
```

To save a report with a different threshold, use, for example, `python scripts/build_measurement_report.py --area-cutoff 0.2 --marker chat`. That threshold is recorded with the new report; the app also permits exploration of supported settings from its saved attributes. Each report contains `resolution_<width>/<measurement_id>.npz` files for all 19 measurements and all three comparison arrays, plus `summary.csv`, `report.json` and `validation.json`. See the [derived-data dictionary](derived_data_dictionary.md) for exact field names.

Only when extracting attributes from authorized original CSVs is this additional step needed:

```bash
python scripts/build_measurement_features.py
```

See [the README](../README.md) for no-install viewing, environment setup and full notebook execution. Current results extend the previous fixed-three PLA-count report; they do not overwrite its historical numerical runs.
