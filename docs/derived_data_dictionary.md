# Derived-data dictionary: counts and selectable spatial measurements

Current authority: [14 November policy](../metadata/scientist_directed_mean_policy.json). The active run is selected by [outputs/section_means/latest_run.json](../outputs/section_means/latest_run.json). Earlier observed-N means retain their own historical method and must not be substituted for these fields.

The first sections below describe that preserved **base PLA-count report**. The [17 November calculation policy](../metadata/calculation_functions_policy.json) supplied the original 13 selectable measurements and three comparisons described later in this dictionary. For the added object means, quantiles and fractions, measurement-defined N can be below three; the base count report's fixed denominator must not be copied onto them.

The separate [raw dictionary](../metadata/data_dictionary.json) describes twenty exported columns and preserves ranges from the initial eight-export inventory. The derived fields below belong to the current twelve-section analysis. Arrays use row-major `[y,x]` indexing on identical edges for all sections at each resolution. Export-coordinate units are uncalibrated; no physical distances are implied.

## Counts, means and differences

| Field or concept | Definition | Representation and limits |
|---|---|---|
| Per-section `pla_counts` | Number of aligned PLA-class bounding-box midpoints assigned once to a section-bin | Nonnegative integer matrix; empty bins are 0 |
| Per-section `chat_counts` | Number of aligned ChAT-class midpoints in a section-bin | Nonnegative integer matrix; context/support only |
| `homecage_count_sum`, `running_count_sum` | Sum of the three selected section PLA counts for that condition | Nonnegative whole-valued arrays; NPZ may store these sums as floats |
| `homecage_mean`, `running_mean` | Corresponding three-section count sum divided by 3 | Fractional raw count per bin; not a percentage or area density |
| `difference` | Running mean minus Homecage mean | Signed floating-point count difference; full-grid arithmetic is retained in NPZ and bin CSV |
| `display_difference` | Difference restricted to the arm's plotting domain | Float with `NaN` outside the domain in NPZ |
| `raw_arithmetic_difference` | Full-grid difference preserved in the viewer payload | Includes numerical zeros outside the plotted domain |
| `section_denominator` / `mean_denominator_each_condition` | Number of sections used in each condition mean | Fixed integer 3 at every bin; not verified tissue N |

In the JSON viewer payload, plotted means and `difference` are `null` outside the display domain; JSON does not encode `NaN`. Saved NPZ mean/difference arrays and bin CSVs retain full-grid arithmetic values. Thus a plotted `null` is not a measured zero. Within the plotted field, zero means a numerical zero under the agreed assumed-zero policy; it does not demonstrate tissue presence.

## Observed support and coverage uncertainty

| Field or concept | Definition | Interpretation |
|---|---|---|
| Per-section `observed_support` | `pla_counts + chat_counts > 0` | A detected-object observation, not tissue coverage |
| `homecage_observed_section_n`, `running_observed_section_n` | Number of sections with observed support, from 0 to 3 | Diagnostic only; never a mean denominator |
| JSON `homecage_n`, `running_n`; CSV `homecage_observed_N`, `running_observed_N` | Names exposing those same observed-section counts | Preserve the diagnostic meaning despite the shorter aliases |
| `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n` | 3 minus observed-section N | Number of completely object-empty section-bins assigned assumed zero; excludes ChAT-only bins, whose PLA count is also 0 |
| CSV `homecage_assumed_zero_sections`, `running_assumed_zero_sections` | CSV aliases for those assumed-zero diagnostics | A warning about unobserved positions, not proof of absent tissue |
| `observed_union` / CSV `display_domain` | At least one observed PLA or ChAT object in any of the arm's six sections | A plotting domain shared by its two conditions; not a tissue outline |
| `displayable` | Bin belongs to that observed union and has a finite calculated difference | Permits a whole-condition zero where only the other condition has observations |
| `tissue_coverage_known`, `coverage_verified`, `tissue_coverage_verified` | Explicit coverage-status fields in arrays, CSV or run metadata | False throughout this mask-free analysis; no 100% mask-containment claim |

## Provenance and figures

Section, physical-section, animal, condition, arm and source-file identifiers link counts to the twelve selected sources. Source rows and native/aligned midpoint positions are retained with the count predecessor and viewer payload. The current run records its source payload hash, fixed-three policy, unchanged transforms and arithmetic validation. All 310,024 selected PLA positions are retained; the points are exported detections, not original microscopy pixels.

Each resolution has its own counts and shared color limits. The default is 100 export units; 1,000, 500 and 250 are coarser grids on the same aligned field. The mean is always divided by 3 at every resolution. Scientific figure exports use 600-DPI PNG and SVG versions at 100 and 250 units. Contrast-limited images change only the displayed color range, disclose saturated values and retain uncapped numerical values.

## Added full-precision PLA attribute cache

The selected cache is identified by [outputs/measurement_features/latest_run.json](../outputs/measurement_features/latest_run.json). It adds attributes to the existing ordered PLA objects, without changing coordinates or sample assignments. The original count cache alone does not contain enough information to reconstruct these measurements.

| Field | Definition | Units / validation |
|---|---|---|
| `area_um2` | One exported `Area (µm²)` value per PLA object, in exactly the existing point order | µm² as labeled in the export; independent physical calibration is unverified |
| `intensity` | One exported `Average Intensity` value per PLA object | Exported intensity units; physical scale and normalization are undocumented |
| `markers.chat` | The `ChAt-50 - FITC_E1 present` flag on each PLA row | 1 associated, 0 not associated; not a count of separate ChAT objects |
| `available_markers` | Marker IDs, display names and actual source columns | Currently `chat` / ChAT only; no unexported marker is inferred |
| `section_id`, `source_sha256` | Existing section identity and exact raw-source fingerprint | Matched to the point/count predecessor |
| `point_order_sha256` | Fingerprint of object IDs, source rows and full-precision native/aligned coordinates | Prevents an attribute vector from being attached to different ordered objects |
| `point_count` | Number of PLA entries in that section's vectors | All selected PLA objects retained; no resampling |
| `invalid_attribute_counts` | Number of unavailable or invalid entries by attribute | Nonfinite, malformed, absent or negative values stay missing; dependent bin measurements are undefined |

JSON uses `null` for unavailable attributes. The cache validation records source-hash checks before and after extraction, exact object-ID/source-row matching, unchanged native and aligned coordinates, complete PLA retention and source-class count conservation. The selected initial attribute extraction reports 310,024 PLA objects and no invalid area, intensity or ChAT-flag entries.

## Selectable measurements and comparisons

The [function guide](calculation_functions.md) supplies all 19 definitions: thirteen from the PDF's page 1 and six added on 19 November. The numerical report is selected by [outputs/calculation_functions/latest_run.json](../outputs/calculation_functions/latest_run.json). The following fields describe the underlying calculation result, independent of presentation or file-format aliases.

| Field or concept | Definition | Missingness / interpretation |
|---|---|---|
| `measurement.id` | One of the 19 measurement IDs | Default `pla_count` |
| `comparison.id` | `absolute_difference`, `percent_change` or `log2_fold_change` | Default `absolute_difference` is **signed** `R - H` |
| `area_cutoff` | Threshold in exported area units | Default 0.1; large uses `>=`, small uses `<`; no calibration is inferred |
| `marker` | Selected available association flag | Default/current marker `chat`; affects associated-PLA measurements |
| Per-section `values` | Selected measurement computed from that animal section's objects in each bin | Count/sum empty bins are 0; object means, quantiles and fractions are missing without requisite objects |
| Per-section `defined` | Whether that section-bin measurement is finite | Distinct from tissue validity and observed support |
| `homecage_mean`, `running_mean` | Equal-weight mean of defined section measurements in that condition | Missing if defined-section N is 0; not an object-pooled mean |
| `homecage_valid_section_n`, `running_valid_section_n` | Number of defined section measurements entering the condition mean | 0–3; **measurement-defined N**, not verified tissue N or observed-support N |
| `eligibility` | Copy of the existing per-arm display domain | Preserves the mask-free union of observed bins; independent of selected measurement's missingness |
| `comparison_value` | Selected comparison applied after condition averaging | Measurement units, percent or log2 ratio, according to selection |
| `difference` in the selectable result | Alias of the **selected comparison value** for the connected viewer | Can be percent or log2 when those comparisons are selected; read `comparison.id` rather than assuming raw count units |
| `absolute_difference` in the selectable result | Always the signed raw difference of the selected measurement's condition means | `R - H`; retains measurement units even when another comparison is selected |
| `displayable` | Eligible bin with a finite selected comparison | A ratio may be missing in a bin that remains eligible |
| `missing_reason` | Why the selected comparison is unavailable | Outside-domain, undefined condition means, zero Homecage reference, nonpositive log ratio inputs or nonfinite result |
| `coverage_verified` | Tissue-coverage status | False; the added functions do not invent masks |
| `quantile_method` | Within-section sample-quantile definition | `type7_linear`; ranked-object interpolation, not spatial interpolation |
| `pseudocount` | Offset added to ratios | `null`; no pseudocount or automatic offset is used |

Counts and sums continue to average all three section-bin zeros when required attributes are available. A zero fraction is defined when PLA exists and none qualifies; it is missing when there is no PLA denominator. Marker-associated mean area is missing when no associated PLA exists, even if other PLA is present. A condition average of section medians or 90th percentiles is not the corresponding quantile of pooled objects.

For percent change, `H = 0` is missing, while `R = 0` with `H > 0` is -100%. Log2 fold change requires `R > 0` and `H > 0`. A signed fraction difference of 0.2 corresponds to 20 percentage points; percent change uses the separate relative denominator `H`. JSON encodes missing results as `null`; numerical arrays use `NaN`, not fabricated zeros.

The source positions, support maps and prior fixed-three count runs remain preserved. Shared comparison color scales and display caps are presentation settings; uncapped values, defined-section counts and missingness support interpretation of every selected map.

## Added numerical report layout

Within the run selected by `outputs/calculation_functions/latest_run.json`:

| File / saved name | Contents |
|---|---|
| `report.json` | All measurement/comparison definitions, selected cutoff and marker, bin summaries, representative figure manifest, source hashes and validation |
| `validation.json` | Recorded preservation, partition and completeness checks from this derivation |
| `summary.csv` | One row per resolution × measurement × comparison × arm; 4 × 19 × 3 × 2 = 456 combinations |
| `resolution_<width>/<measurement_id>.npz` | Section values, means, defined-section N, eligibility and all three comparison arrays for one measurement at one grid width |
| NPZ `section_ids`, `section_values`, `section_defined` | Ordered section IDs and `[section,y,x]` measurement/defined arrays; the twelve sections retain their existing identities |
| NPZ `x_edges`, `y_edges` | Unchanged full-precision aligned grid edges |
| NPZ `hk1_homecage_mean`, `hk1_running_mean` and corresponding `pfkp_` fields | Condition means, with the arm prefix identifying the separately analyzed experiment |
| NPZ `<arm>_homecage_valid_section_n`, `<arm>_running_valid_section_n` | Measurement-defined N from 0 to 3 per condition/bin |
| NPZ `<arm>_eligibility` | Unchanged per-arm display-domain mask |
| NPZ `<arm>_absolute_difference`, `<arm>_percent_change`, `<arm>_log2_fold_change` | Explicitly named selected-measurement comparisons; missing results are `NaN` |
| NPZ `<arm>_<comparison>_missing_reason` | Reason strings; empty string for a defined comparison, explicit outside-domain or undefined-reference reasons otherwise |
| `figures/` | Representative fine-grid PNG/SVG comparison pairs, with cutoff, marker, units, color limit and defined-bin counts recorded in `report.json` |

The summary fields `eligible_bins`, `defined_comparison_bins` and `undefined_eligible_bins` distinguish an unchanged plotting domain from mathematical availability. `negative_bins`, `positive_bins` and `equal_bins` count defined comparison bins; they are spatial summaries, not biological replicates or significance tests. `homecage_metric_N_0` and `running_metric_N_0` count eligible bins with no defined section measurement. `minimum` and `maximum` describe finite displayed comparisons, not individual object measurements. A report built at a different cutoff records that choice in every summary row.

## Added spatial features and display geometry (19 November)

`nearest_neighbor_distance` is a full-precision vector indexed to the same ordered PLA identifiers, source rows and fixed aligned coordinates as the other attributes. Each value searches the entire same physical section before binning; it excludes the focal object, retains zero for distinct objects at identical positions and stays missing when no neighbor exists. Units are exported coordinate units, with no physical calibration or edge correction. `spatial_features` records exact cKDTree parameters and limitations; `predecessor_feature_payload_sha256` preserves cache lineage when an earlier cache is extended. No raw measurements or source positions are overwritten.

`outputs/comet_core/context_geometry.json` stores each arm's finest original 100-unit observed-domain `footprint`, unchanged `grid`, flattened boundary `x`/`y` vectors with null separators, occupied-bin/segment counts and a geometry hash. These detection-derived shapes preserve internal holes and are neither tissue masks nor a measurement eligibility update.

Fine local grids are temporary display calculations from exact source points and their matched attributes. Their whole-section share denominator and nearest-neighbor distances retain full-section context. They use the same three-animal, defined-section averaging and ratio rules. Local bin width, window, selected measurement, units, cutoff, marker and color limits are recorded in the SVG metadata. PNGs are rendered from that vector tile document, rather than enlarged browser screenshots.
