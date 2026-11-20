# Complete repository file catalog

Every file selected by Git for this project is listed individually below, including source files, tests, metadata, notebooks and repeated generated figures/tables. File contents are explained in the linked code, calculation and repository guides. Files in the hidden `.git/` database are version-control internals; raw-input and temporary directories are intentionally excluded from publication.

[Appendix home](README.md) · [Calculations](calculations.md) · [Code reference](code_reference.md) · [Repository guide](repository_guide.md)

**Catalog coverage: 527 selected files.** The accompanying [machine-readable inventory](file_inventory.json) records every path, purpose, source entry point, CSV header and NPZ array name. Regenerate with `python scripts/build_repository_appendix.py`; use `--check` to validate file coverage and local links.

Generated artifacts are data or rendered output, not additional executable code. A PNG/SVG pair depicts one calculation twice; two saved runs of the same section are not independent animals. `latest_run.json` selects the active run. Older figures/protocols remain dated evidence and may show earlier controls or denominators.

## Repository root

### [.DS_Store](../../.DS_Store)

Existing tracked macOS Finder display metadata. It contains no analysis code; unrelated local changes are excluded from this update.

### [.gitattributes](../../.gitattributes)

Preserves scientific CSV bytes, marks binary artifacts and identifies generated output files for Git review.

### [.gitignore](../../.gitignore)

Selects publishable code/results while excluding raw inputs, instruction PDFs, environments and unselected generated runs.

### [Launch_COMET_Explorer.command](../../Launch_COMET_Explorer.command)

Mac double-click launcher: locates this checkout and starts the local Python viewer server; opens saved HTML directly if Python is unavailable.

### [README.md](../../README.md)

The starting instructions for viewing, rerunning and understanding the current nineteen-measurement Explorer.

### [TDP43_COMET_analysis.ipynb](../../TDP43_COMET_analysis.ipynb)

Current main scientific report: eight executed code cells, nineteen metric definitions, saved results and interpretation.

**Saved notebook structure:** 16 cells, 8 code cells, 8 with execution counts, 12 PNG outputs. See the notebook guide for scope and rerun side effects.

### [TDP43_native_supporting_analysis.ipynb](../../TDP43_native_supporting_analysis.ipynb)

Historical eight-export native-coordinate supporting report. Saved outputs are background; its rerun has a different scope and shared-output side effects.

**Saved notebook structure:** 33 cells, 15 code cells, 15 with execution counts, 10 PNG outputs. See the notebook guide for scope and rerun side effects.

## `comet_spatial`

### [__init__.py](../../comet_spatial/__init__.py)

Declares the reusable Python analysis package.

### [alignment_replay.py](../../comet_spatial/alignment_replay.py)

Replays frozen historical placement for a reproducibility check; it does not fit a new anatomical alignment.

**Named code items:** [boundary_points](../../comet_spatial/alignment_replay.py#L15), [transform_xy](../../comet_spatial/alignment_replay.py#L27), [style](../../comet_spatial/alignment_replay.py#L37), [alignment_figure](../../comet_spatial/alignment_replay.py#L44).

### [context_geometry.py](../../comet_spatial/context_geometry.py)

Traces every boundary/gap of the finest observed-object bin domain; supplies a metric-independent footprint, not a tissue mask.

**Named code items:** [footprint_geometry](../../comet_spatial/context_geometry.py#L7), [build_context_geometry](../../comet_spatial/context_geometry.py#L33).

### [core.py](../../comet_spatial/core.py)

Shared grid, fixed-transform, mask-containment, count-binning and condition-comparison primitives, including the separate strict method.

**Named code items:** [GridSpec](../../comet_spatial/core.py#L18), [GridSpec.__post_init__](../../comet_spatial/core.py#L33), [GridSpec.shape](../../comet_spatial/core.py#L46), [GridSpec.cells](../../comet_spatial/core.py#L49), [FixedTransform](../../comet_spatial/core.py#L57), [FixedTransform.__post_init__](../../comet_spatial/core.py#L66), [FixedTransform.points](../../comet_spatial/core.py#L76), [FixedTransform.geometry](../../comet_spatial/core.py#L81), [_points](../../comet_spatial/core.py#L90), [assign_centroid_bins](../../comet_spatial/core.py#L99), [count_section](../../comet_spatial/core.py#L113), [SectionCounts](../../comet_spatial/core.py#L141), [_valid_mask](../../comet_spatial/core.py#L148), [polygon_tissue_validity](../../comet_spatial/core.py#L157), [raster_cell_footprints](../../comet_spatial/core.py#L171), [SectionResult](../../comet_spatial/core.py#L192), [ArmSummary](../../comet_spatial/core.py#L203), [summarize_by_arm](../../comet_spatial/core.py#L213), [shared_symmetric_limit](../../comet_spatial/core.py#L259).

### [core_view.py](../../comet_spatial/core_view.py)

Validates a saved strict numerical run and turns its own snapshot into a viewer payload; reports missing strict inputs separately.

**Named code items:** [_read_json](../../comet_spatial/core_view.py#L29), [_run_file](../../comet_spatial/core_view.py#L33), [_json_matrix](../../comet_spatial/core_view.py#L45), [_blocked](../../comet_spatial/core_view.py#L52), [_load_arrays](../../comet_spatial/core_view.py#L68), [_provenance_preview](../../comet_spatial/core_view.py#L81), [_mask_geometry](../../comet_spatial/core_view.py#L153), [_alignment_geometry](../../comet_spatial/core_view.py#L179), [build_core_view_payload](../../comet_spatial/core_view.py#L203).

### [exploratory.py](../../comet_spatial/exploratory.py)

Streams the twelve selected raw exports, counts PLA/ChAT midpoint proxies and records exploratory provenance/support.

**Named code items:** [_json](../../comet_spatial/exploratory.py#L35), [_matrix](../../comet_spatial/exploratory.py#L39), [summarize_observed_sections](../../comet_spatial/exploratory.py#L46), [count_raw_section](../../comet_spatial/exploratory.py#L84), [run_exploratory_maps](../../comet_spatial/exploratory.py#L170).

### [manifest.py](../../comet_spatial/manifest.py)

Reads and checks source/section/transform/approval/mask metadata and produces preflight diagnostics for the strict method.

**Named code items:** [sha256_file](../../comet_spatial/manifest.py#L22), [empty_manifest](../../comet_spatial/manifest.py#L30), [section_template](../../comet_spatial/manifest.py#L55), [load_manifest](../../comet_spatial/manifest.py#L79), [grid_from_manifest](../../comet_spatial/manifest.py#L84), [display_directions_from_manifest](../../comet_spatial/manifest.py#L91), [validate_manifest](../../comet_spatial/manifest.py#L111), [preflight_manifest](../../comet_spatial/manifest.py#L370).

### [measurement_features.py](../../comet_spatial/measurement_features.py)

Matches PLA area/intensity/marker vectors to exact source objects and adds exact same-section nearest-neighbor distances immutably.

**Named code items:** [nearest_neighbor_distances](../../comet_spatial/measurement_features.py#L27), [spatial_feature_policy](../../comet_spatial/measurement_features.py#L44), [point_order_hash](../../comet_spatial/measurement_features.py#L54), [feature_number](../../comet_spatial/measurement_features.py#L60), [extract_section_features](../../comet_spatial/measurement_features.py#L69), [locate_saved_counts](../../comet_spatial/measurement_features.py#L123), [build_feature_cache](../../comet_spatial/measurement_features.py#L131), [load_feature_cache](../../comet_spatial/measurement_features.py#L184), [ensure_spatial_feature_cache](../../comet_spatial/measurement_features.py#L213).

### [measurements.py](../../comet_spatial/measurements.py)

Reference Python implementation of all nineteen section-bin measurements, defined-section means and three comparisons.

**Named code items:** [_numbers](../../comet_spatial/measurements.py#L46), [_selected_payload](../../comet_spatial/measurements.py#L51), [compare_conditions](../../comet_spatial/measurements.py#L58), [_bins](../../comet_spatial/measurements.py#L90), [_section_values](../../comet_spatial/measurements.py#L103), [compute_measurement](../../comet_spatial/measurements.py#L210).

### [multiresolution.py](../../comet_spatial/multiresolution.py)

Builds four genuine count grids and the full unsampled PLA point cache from selected raw exports.

**Named code items:** [_save_json](../../comet_spatial/multiresolution.py#L31), [_matrix](../../comet_spatial/multiresolution.py#L36), [grid_at_width](../../comet_spatial/multiresolution.py#L43), [aggregate_counts](../../comet_spatial/multiresolution.py#L57), [refinement_checks](../../comet_spatial/multiresolution.py#L67), [support_statistics](../../comet_spatial/multiresolution.py#L83), [_read_pla_points](../../comet_spatial/multiresolution.py#L101), [_compare_baseline](../../comet_spatial/multiresolution.py#L122), [build_multiresolution_maps](../../comet_spatial/multiresolution.py#L147).

### [native_atlas.py](../../comet_spatial/native_atlas.py)

Historical native-export summaries, count/association maps, shape QC, point samples and source-review windows for the original intake.

**Named code items:** [native_edges](../../comet_spatial/native_atlas.py#L53), [midpoint_coordinates](../../comet_spatial/native_atlas.py#L63), [raw_grid](../../comet_spatial/native_atlas.py#L74), [sampled_indices](../../comet_spatial/native_atlas.py#L88), [distribution](../../comet_spatial/native_atlas.py#L96), [morphology_summary](../../comet_spatial/native_atlas.py#L112), [_json_rows](../../comet_spatial/native_atlas.py#L130), [export_payload](../../comet_spatial/native_atlas.py#L141), [duplicate_review](../../comet_spatial/native_atlas.py#L192), [save_figures](../../comet_spatial/native_atlas.py#L215), [source_review_targets](../../comet_spatial/native_atlas.py#L280), [morphology_object_review_targets](../../comet_spatial/native_atlas.py#L314), [build](../../comet_spatial/native_atlas.py#L378), [main](../../comet_spatial/native_atlas.py#L438).

### [section_means.py](../../comet_spatial/section_means.py)

Derives current fixed-three count means/differences from saved counts while preserving historical variable-support summaries.

**Named code items:** [summarize_section_means](../../comet_spatial/section_means.py#L15).

## `docs/appendix`

### [README.md](../../docs/appendix/README.md)

Entry point for this explanatory appendix, with an end-to-end map and reading routes.

### [calculations.md](../../docs/appendix/calculations.md)

Complete calculation definitions, worked examples, missingness and current/historical method distinctions.

### [code_reference.md](../../docs/appendix/code_reference.md)

File-by-file explanation of Python/JavaScript/templates and their call/data flow.

## `docs/appendix/diagrams`

### [calculations_flow_1.svg](../../docs/appendix/diagrams/calculations_flow_1.svg)

Rendered vector flow diagram for calculations flow 1. Its editable Mermaid source appears in the corresponding appendix chapter; it does not contain measured specimen images.

### [calculations_flow_2.svg](../../docs/appendix/diagrams/calculations_flow_2.svg)

Rendered vector flow diagram for calculations flow 2. Its editable Mermaid source appears in the corresponding appendix chapter; it does not contain measured specimen images.

### [code_reference_flow_1.svg](../../docs/appendix/diagrams/code_reference_flow_1.svg)

Rendered vector flow diagram for code reference flow 1. Its editable Mermaid source appears in the corresponding appendix chapter; it does not contain measured specimen images.

### [code_reference_flow_2.svg](../../docs/appendix/diagrams/code_reference_flow_2.svg)

Rendered vector flow diagram for code reference flow 2. Its editable Mermaid source appears in the corresponding appendix chapter; it does not contain measured specimen images.

### [data_to_visuals.svg](../../docs/appendix/diagrams/data_to_visuals.svg)

Scalable overview from original exports and verified metadata through calculations to scientific/app visuals.

### [diagram_manifest.json](../../docs/appendix/diagrams/diagram_manifest.json)

Diagram rendering audit: Mermaid renderer/source version, originating document/block, source and SVG hashes, and successful local render checks.

### [overview_flow_1.svg](../../docs/appendix/diagrams/overview_flow_1.svg)

Rendered vector flow diagram for overview flow 1. Its editable Mermaid source appears in the corresponding appendix chapter; it does not contain measured specimen images.

### [repository_guide_flow_1.svg](../../docs/appendix/diagrams/repository_guide_flow_1.svg)

Rendered vector flow diagram for repository guide flow 1. Its editable Mermaid source appears in the corresponding appendix chapter; it does not contain measured specimen images.

## `docs/appendix`

### [file_catalog.md](../../docs/appendix/file_catalog.md)

Every selected repository file, individually linked and explained, including repeated result artifacts.

### [file_inventory.json](../../docs/appendix/file_inventory.json)

Machine-readable complete file catalog; supports coverage validation and regeneration from a ZIP.

### [repository_guide.md](../../docs/appendix/repository_guide.md)

Detailed root/notebook/docs/metadata/test guide, vocabulary and safe rerun routes.

## `docs`

### [background_reuse.md](../../docs/background_reuse.md)

Reader documentation: Previous project: what is reused and what changes. Its current/historical scope is explained in the repository guide.

### [calculation_functions.md](../../docs/calculation_functions.md)

Reader documentation: Spatial measurements and condition comparisons. Its current/historical scope is explained in the repository guide.

### [comet_alignment_asset_trace.md](../../docs/comet_alignment_asset_trace.md)

Reader documentation: Trace of the previous app's saved alignment. Its current/historical scope is explained in the repository guide.

### [comet_pdf_acceptance_checklist.md](../../docs/comet_pdf_acceptance_checklist.md)

Reader documentation: COMET PDF: acceptance checklist for the three core views. Its current/historical scope is explained in the repository guide.

### [derived_data_dictionary.md](../../docs/derived_data_dictionary.md)

Reader documentation: Derived-data dictionary: counts and selectable spatial measurements. Its current/historical scope is explained in the repository guide.

### [detailed_heatmaps.md](../../docs/detailed_heatmaps.md)

Reader documentation: Detailed spatial maps: resolution and source review. Its current/historical scope is explained in the repository guide.

### [exploratory_methods.md](../../docs/exploratory_methods.md)

Reader documentation: Methods: current three-section condition means. Its current/historical scope is explained in the repository guide.

### [historical_findings_and_visual_transfer.md](../../docs/historical_findings_and_visual_transfer.md)

Reader documentation: Prior findings and visual practices used in this project. Its current/historical scope is explained in the repository guide.

### [project_brief.md](../../docs/project_brief.md)

Reader documentation: COMET spatial PLA project brief. Its current/historical scope is explained in the repository guide.

### [research_methods.md](../../docs/research_methods.md)

Reader documentation: Verified research and method rationale. Its current/historical scope is explained in the repository guide.

### [results_guide.md](../../docs/results_guide.md)

Reader documentation: Reading the current COMET spatial results. Its current/historical scope is explained in the repository guide.

### [scientist_clarifications_2026-11-14.md](../../docs/scientist_clarifications_2026-11-14.md)

Reader documentation: Scientist clarifications: 14 November 2026. Its current/historical scope is explained in the repository guide.

### [scientist_questions.md](../../docs/scientist_questions.md)

Reader documentation: Scientist clarification status: resolved. Its current/historical scope is explained in the repository guide.

### [technical_handoff_requirements.md](../../docs/technical_handoff_requirements.md)

Reader documentation: COMET spatial PLA analysis: technical handoff requirements. Its current/historical scope is explained in the repository guide.

### [workflow.md](../../docs/workflow.md)

Reader documentation: Experiment-to-results workflow. Its current/historical scope is explained in the repository guide.

## `metadata`

### [alignment_support_review_parameters.json](../../metadata/alignment_support_review_parameters.json)

Dated detailed-review settings and unchanged full-point/alignment provenance.

### [analysis_manifest.json](../../metadata/analysis_manifest.json)

Selected source paths/hashes, twelve section assignments, fixed transforms, grid and strict-input attestations.

### [background_provenance.json](../../metadata/background_provenance.json)

The historical PLA–ChAT repository revision, research role and inspected background materials.

### [calculation_functions_policy.json](../../metadata/calculation_functions_policy.json)

Original thirteen PDF definitions, current nineteen-metric catalog and zero/missing/comparison provenance.

### [cohort_selection.json](../../metadata/cohort_selection.json)

Explicit twelve-section cohort authority and thirteen-export inventory, with job 4978 superseded by 5403.

### [data_dictionary.csv](../../metadata/data_dictionary.csv)

Column-by-column dictionary of original input fields and observed types/units.

**CSV columns:** `column`, `description`, `units_or_representation`, `observed_types`, `missing_count_all_files`, `nonfinite_count_all_files`, `numeric_min_all_files`, `numeric_max_all_files`, `limitations`.

### [data_dictionary.json](../../metadata/data_dictionary.json)

Machine-readable version of the original input-field dictionary.

### [descriptive_findings_parameters.json](../../metadata/descriptive_findings_parameters.json)

Historical native descriptive size/association/review rules, not transferred condition-analysis constants.

### [detailed_visual_parameters.json](../../metadata/detailed_visual_parameters.json)

Current global/local grids, context, scales and fixed 8,000-pixel PNG display/export policy.

### [environment.json](../../metadata/environment.json)

Recorded Python/platform/package and execution provenance; not the dependency installer.

### [exploratory_authorization.json](../../metadata/exploratory_authorization.json)

Recorded permission and scope for exploratory analysis without strict tissue-mask inputs.

### [explorer_display_parameters.json](../../metadata/explorer_display_parameters.json)

Earlier native app starting display choices and its separate point-sampling convention.

### [grid_parameters.json](../../metadata/grid_parameters.json)

Original common aligned extent, edge definitions and unverified physical-coordinate calibration.

### [input_manifest.csv](../../metadata/input_manifest.csv)

Original intake-file inventory and source metadata in spreadsheet-readable form.

**CSV columns:** `file_id`, `source_path`, `relative_path`, `format`, `size_bytes`, `sha256`, `job_token_from_filename`, `historical_byte_identical_copy_count`, `historical_byte_identical_paths`, `sample_assignment_status`, `row_count`, `column_count`, `exported_analysis_regions`, `true_centroid_fields_present`.

### [input_manifest.json](../../metadata/input_manifest.json)

Machine-readable original intake-file inventory with recorded hashes/paths.

### [instruction_provenance.json](../../metadata/instruction_provenance.json)

Recorded original instruction PDF identity, page count, hash and review provenance; not the PDF itself.

### [local_paths.json](../../metadata/local_paths.json)

Local source/workspace/background paths and copy policy; these paths are not portable scientific identities.

### [native_atlas_parameters.json](../../metadata/native_atlas_parameters.json)

Historical native bin widths, deterministic display sampling and shape/intensity histogram settings.

### [sample_metadata.csv](../../metadata/sample_metadata.csv)

Original observed intake metadata; older unresolved assignments are superseded by selected-section/cohort authority.

**CSV columns:** `file_id`, `exported_analysis_region`, `rows_in_export_region`, `animal_id`, `condition`, `pla_arm`, `physical_section_id`, `roi_id`, `biological_replicate_id`, `technical_repeat_of`, `include_in_primary_analysis`, `approved_alignment_id`, `aligned_centroid_source`, `tissue_mask_source`, `coordinate_units`, `assignment_status`, `evidence`.

### [scientist_directed_mean_policy.json](../../metadata/scientist_directed_mean_policy.json)

14 November scientist-authorized three-section count denominator and assumed-zero/uncertain-coverage policy.

### [section_template.json](../../metadata/section_template.json)

Example schema for supplying a section, source, mask and transform; it is not a real new sample.

### [selected_section_metadata.csv](../../metadata/selected_section_metadata.csv)

Explicit current animal/condition/arm/source relationships for the twelve completed sections.

**CSV columns:** `section_id`, `physical_section_id`, `animal_id`, `condition`, `pla_type`, `pla_arm`, `job`, `source_file_id`, `source_path`, `source_filename`, `source_sha256`, `source_rows`, `marker_panel`, `exported_analysis_region`, `saved_center_x`, `saved_center_y`, `saved_flip`, `reference_job`, `assignment_status`, `assignment_authority`, `tissue_mask_status`.

### [spatial_extensions_policy_2026-11-19.json](../../metadata/spatial_extensions_policy_2026-11-19.json)

Dated six-metric/fine-detail/footprint extension snapshot. Its original optional-12K field is historical; the later fixed-size protocol overrides the UI setting.

## `outputs/app`

### [index.html](../../outputs/app/index.html)

The current self-contained offline nineteen-measurement Explorer: embedded data, Plotly and app code; open this file to view results.

### [native_explorer.html](../../outputs/app/native_explorer.html)

Historical self-contained native supporting app for the original eight-export intake; different data/summary scope.

## `outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures`

### [large_pla_fraction_absolute_difference_100.png](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/large_pla_fraction_absolute_difference_100.png)

Saved full-range scientific figure for large pla fraction absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,036 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [large_pla_fraction_absolute_difference_100.svg](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/large_pla_fraction_absolute_difference_100.svg)

Saved full-range scientific figure for large pla fraction absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [large_pla_fraction_absolute_difference_detail_100.png](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/large_pla_fraction_absolute_difference_detail_100.png)

Saved disclosed contrast-limited scientific figure for large pla fraction absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,036 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [large_pla_fraction_absolute_difference_detail_100.svg](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/large_pla_fraction_absolute_difference_detail_100.svg)

Saved disclosed contrast-limited scientific figure for large pla fraction absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [marker_associated_pla_count_absolute_difference_100.png](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/marker_associated_pla_count_absolute_difference_100.png)

Saved full-range scientific figure for marker associated pla count absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,010 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [marker_associated_pla_count_absolute_difference_100.svg](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/marker_associated_pla_count_absolute_difference_100.svg)

Saved full-range scientific figure for marker associated pla count absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [marker_associated_pla_count_absolute_difference_detail_100.png](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/marker_associated_pla_count_absolute_difference_detail_100.png)

Saved disclosed contrast-limited scientific figure for marker associated pla count absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 8,904 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [marker_associated_pla_count_absolute_difference_detail_100.svg](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/marker_associated_pla_count_absolute_difference_detail_100.svg)

Saved disclosed contrast-limited scientific figure for marker associated pla count absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [mean_pla_area_absolute_difference_100.png](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/mean_pla_area_absolute_difference_100.png)

Saved full-range scientific figure for mean pla area absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,010 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [mean_pla_area_absolute_difference_100.svg](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/mean_pla_area_absolute_difference_100.svg)

Saved full-range scientific figure for mean pla area absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [mean_pla_area_absolute_difference_detail_100.png](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/mean_pla_area_absolute_difference_detail_100.png)

Saved disclosed contrast-limited scientific figure for mean pla area absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 8,904 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [mean_pla_area_absolute_difference_detail_100.svg](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/mean_pla_area_absolute_difference_detail_100.svg)

Saved disclosed contrast-limited scientific figure for mean pla area absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [pla_count_log2_fold_change_100.png](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/pla_count_log2_fold_change_100.png)

Saved full-range scientific figure for pla count log2 fold change 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 8,904 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [pla_count_log2_fold_change_100.svg](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/pla_count_log2_fold_change_100.svg)

Saved full-range scientific figure for pla count log2 fold change 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [pla_count_log2_fold_change_detail_100.png](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/pla_count_log2_fold_change_detail_100.png)

Saved disclosed contrast-limited scientific figure for pla count log2 fold change detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 8,904 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [pla_count_log2_fold_change_detail_100.svg](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/pla_count_log2_fold_change_detail_100.svg)

Saved disclosed contrast-limited scientific figure for pla count log2 fold change detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [pla_count_percent_change_100.png](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/pla_count_percent_change_100.png)

Saved full-range scientific figure for pla count percent change 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,116 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [pla_count_percent_change_100.svg](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/pla_count_percent_change_100.svg)

Saved full-range scientific figure for pla count percent change 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [pla_count_percent_change_detail_100.png](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/pla_count_percent_change_detail_100.png)

Saved disclosed contrast-limited scientific figure for pla count percent change detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,010 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [pla_count_percent_change_detail_100.svg](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/figures/pla_count_percent_change_detail_100.svg)

Saved disclosed contrast-limited scientific figure for pla count percent change detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

## `outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc`

### [report.json](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/report.json)

Definitions, settings, per-arm/resolution comparison summaries, figure manifest and validation for this metric run.

## `outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_100`

### [large_pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_100/large_pla_count.npz)

Compressed numerical arrays for large pla count on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [large_pla_fraction.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_100/large_pla_fraction.npz)

Compressed numerical arrays for large pla fraction on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_large_pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_100/marker_associated_large_pla_count.npz)

Compressed numerical arrays for marker associated large pla count on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_100/marker_associated_pla_count.npz)

Compressed numerical arrays for marker associated pla count on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_fraction.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_100/marker_associated_pla_fraction.npz)

Compressed numerical arrays for marker associated pla fraction on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_mean_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_100/marker_associated_pla_mean_area.npz)

Compressed numerical arrays for marker associated pla mean area on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_100/mean_pla_area.npz)

Compressed numerical arrays for mean pla area on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_intensity.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_100/mean_pla_intensity.npz)

Compressed numerical arrays for mean pla intensity on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [median_pla_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_100/median_pla_area.npz)

Compressed numerical arrays for median pla area on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [p90_pla_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_100/p90_pla_area.npz)

Compressed numerical arrays for p90 pla area on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_100/pla_count.npz)

Compressed numerical arrays for pla count on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [small_pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_100/small_pla_count.npz)

Compressed numerical arrays for small pla count on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [total_pla_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_100/total_pla_area.npz)

Compressed numerical arrays for total pla area on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

## `outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_1000`

### [large_pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_1000/large_pla_count.npz)

Compressed numerical arrays for large pla count on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [large_pla_fraction.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_1000/large_pla_fraction.npz)

Compressed numerical arrays for large pla fraction on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_large_pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_1000/marker_associated_large_pla_count.npz)

Compressed numerical arrays for marker associated large pla count on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_1000/marker_associated_pla_count.npz)

Compressed numerical arrays for marker associated pla count on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_fraction.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_1000/marker_associated_pla_fraction.npz)

Compressed numerical arrays for marker associated pla fraction on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_mean_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_1000/marker_associated_pla_mean_area.npz)

Compressed numerical arrays for marker associated pla mean area on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_1000/mean_pla_area.npz)

Compressed numerical arrays for mean pla area on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_intensity.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_1000/mean_pla_intensity.npz)

Compressed numerical arrays for mean pla intensity on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [median_pla_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_1000/median_pla_area.npz)

Compressed numerical arrays for median pla area on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [p90_pla_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_1000/p90_pla_area.npz)

Compressed numerical arrays for p90 pla area on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_1000/pla_count.npz)

Compressed numerical arrays for pla count on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [small_pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_1000/small_pla_count.npz)

Compressed numerical arrays for small pla count on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [total_pla_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_1000/total_pla_area.npz)

Compressed numerical arrays for total pla area on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

## `outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_250`

### [large_pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_250/large_pla_count.npz)

Compressed numerical arrays for large pla count on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [large_pla_fraction.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_250/large_pla_fraction.npz)

Compressed numerical arrays for large pla fraction on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_large_pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_250/marker_associated_large_pla_count.npz)

Compressed numerical arrays for marker associated large pla count on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_250/marker_associated_pla_count.npz)

Compressed numerical arrays for marker associated pla count on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_fraction.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_250/marker_associated_pla_fraction.npz)

Compressed numerical arrays for marker associated pla fraction on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_mean_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_250/marker_associated_pla_mean_area.npz)

Compressed numerical arrays for marker associated pla mean area on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_250/mean_pla_area.npz)

Compressed numerical arrays for mean pla area on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_intensity.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_250/mean_pla_intensity.npz)

Compressed numerical arrays for mean pla intensity on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [median_pla_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_250/median_pla_area.npz)

Compressed numerical arrays for median pla area on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [p90_pla_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_250/p90_pla_area.npz)

Compressed numerical arrays for p90 pla area on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_250/pla_count.npz)

Compressed numerical arrays for pla count on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [small_pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_250/small_pla_count.npz)

Compressed numerical arrays for small pla count on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [total_pla_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_250/total_pla_area.npz)

Compressed numerical arrays for total pla area on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

## `outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_500`

### [large_pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_500/large_pla_count.npz)

Compressed numerical arrays for large pla count on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [large_pla_fraction.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_500/large_pla_fraction.npz)

Compressed numerical arrays for large pla fraction on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_large_pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_500/marker_associated_large_pla_count.npz)

Compressed numerical arrays for marker associated large pla count on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_500/marker_associated_pla_count.npz)

Compressed numerical arrays for marker associated pla count on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_fraction.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_500/marker_associated_pla_fraction.npz)

Compressed numerical arrays for marker associated pla fraction on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_mean_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_500/marker_associated_pla_mean_area.npz)

Compressed numerical arrays for marker associated pla mean area on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_500/mean_pla_area.npz)

Compressed numerical arrays for mean pla area on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_intensity.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_500/mean_pla_intensity.npz)

Compressed numerical arrays for mean pla intensity on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [median_pla_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_500/median_pla_area.npz)

Compressed numerical arrays for median pla area on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [p90_pla_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_500/p90_pla_area.npz)

Compressed numerical arrays for p90 pla area on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_500/pla_count.npz)

Compressed numerical arrays for pla count on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [small_pla_count.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_500/small_pla_count.npz)

Compressed numerical arrays for small pla count on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [total_pla_area.npz](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/resolution_500/total_pla_area.npz)

Compressed numerical arrays for total pla area on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

## `outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc`

### [summary.csv](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/summary.csv)

One row per measurement × comparison × arm × global grid; documents defined/missing counts, ranges and metric N.

**CSV columns:** `bin_width`, `measurement`, `comparison`, `arm`, `units`, `area_cutoff`, `marker`, `eligible_bins`, `defined_comparison_bins`, `undefined_eligible_bins`, `negative_bins`, `positive_bins`, `equal_bins`, `minimum`, `maximum`, `homecage_metric_N_0`, `running_metric_N_0`.

### [validation.json](../../outputs/calculation_functions/20261118T025635444707Z_fed14133d6cc/validation.json)

Metric-run conservation/subset, count-preservation, geometry and provenance checks.

## `outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures`

### [large_pla_fraction_absolute_difference_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/large_pla_fraction_absolute_difference_100.png)

Saved full-range scientific figure for large pla fraction absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,036 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [large_pla_fraction_absolute_difference_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/large_pla_fraction_absolute_difference_100.svg)

Saved full-range scientific figure for large pla fraction absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [large_pla_fraction_absolute_difference_detail_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/large_pla_fraction_absolute_difference_detail_100.png)

Saved disclosed contrast-limited scientific figure for large pla fraction absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,036 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [large_pla_fraction_absolute_difference_detail_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/large_pla_fraction_absolute_difference_detail_100.svg)

Saved disclosed contrast-limited scientific figure for large pla fraction absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [marker_associated_pla_area_fraction_absolute_difference_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/marker_associated_pla_area_fraction_absolute_difference_100.png)

Saved full-range scientific figure for marker associated pla area fraction absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,036 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [marker_associated_pla_area_fraction_absolute_difference_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/marker_associated_pla_area_fraction_absolute_difference_100.svg)

Saved full-range scientific figure for marker associated pla area fraction absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [marker_associated_pla_area_fraction_absolute_difference_detail_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/marker_associated_pla_area_fraction_absolute_difference_detail_100.png)

Saved disclosed contrast-limited scientific figure for marker associated pla area fraction absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,036 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [marker_associated_pla_area_fraction_absolute_difference_detail_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/marker_associated_pla_area_fraction_absolute_difference_detail_100.svg)

Saved disclosed contrast-limited scientific figure for marker associated pla area fraction absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [marker_associated_pla_count_absolute_difference_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/marker_associated_pla_count_absolute_difference_100.png)

Saved full-range scientific figure for marker associated pla count absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,010 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [marker_associated_pla_count_absolute_difference_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/marker_associated_pla_count_absolute_difference_100.svg)

Saved full-range scientific figure for marker associated pla count absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [marker_associated_pla_count_absolute_difference_detail_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/marker_associated_pla_count_absolute_difference_detail_100.png)

Saved disclosed contrast-limited scientific figure for marker associated pla count absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 8,904 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [marker_associated_pla_count_absolute_difference_detail_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/marker_associated_pla_count_absolute_difference_detail_100.svg)

Saved disclosed contrast-limited scientific figure for marker associated pla count absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [mean_pla_area_absolute_difference_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/mean_pla_area_absolute_difference_100.png)

Saved full-range scientific figure for mean pla area absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,010 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [mean_pla_area_absolute_difference_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/mean_pla_area_absolute_difference_100.svg)

Saved full-range scientific figure for mean pla area absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [mean_pla_area_absolute_difference_detail_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/mean_pla_area_absolute_difference_detail_100.png)

Saved disclosed contrast-limited scientific figure for mean pla area absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 8,904 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [mean_pla_area_absolute_difference_detail_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/mean_pla_area_absolute_difference_detail_100.svg)

Saved disclosed contrast-limited scientific figure for mean pla area absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [mean_pla_nearest_neighbor_distance_absolute_difference_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/mean_pla_nearest_neighbor_distance_absolute_difference_100.png)

Saved full-range scientific figure for mean pla nearest neighbor distance absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,010 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [mean_pla_nearest_neighbor_distance_absolute_difference_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/mean_pla_nearest_neighbor_distance_absolute_difference_100.svg)

Saved full-range scientific figure for mean pla nearest neighbor distance absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [mean_pla_nearest_neighbor_distance_absolute_difference_detail_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/mean_pla_nearest_neighbor_distance_absolute_difference_detail_100.png)

Saved disclosed contrast-limited scientific figure for mean pla nearest neighbor distance absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,010 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [mean_pla_nearest_neighbor_distance_absolute_difference_detail_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/mean_pla_nearest_neighbor_distance_absolute_difference_detail_100.svg)

Saved disclosed contrast-limited scientific figure for mean pla nearest neighbor distance absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [median_pla_intensity_absolute_difference_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/median_pla_intensity_absolute_difference_100.png)

Saved full-range scientific figure for median pla intensity absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 8,983 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [median_pla_intensity_absolute_difference_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/median_pla_intensity_absolute_difference_100.svg)

Saved full-range scientific figure for median pla intensity absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [median_pla_intensity_absolute_difference_detail_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/median_pla_intensity_absolute_difference_detail_100.png)

Saved disclosed contrast-limited scientific figure for median pla intensity absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,089 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [median_pla_intensity_absolute_difference_detail_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/median_pla_intensity_absolute_difference_detail_100.svg)

Saved disclosed contrast-limited scientific figure for median pla intensity absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [pla_area_cv_absolute_difference_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/pla_area_cv_absolute_difference_100.png)

Saved full-range scientific figure for pla area cv absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 8,957 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [pla_area_cv_absolute_difference_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/pla_area_cv_absolute_difference_100.svg)

Saved full-range scientific figure for pla area cv absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [pla_area_cv_absolute_difference_detail_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/pla_area_cv_absolute_difference_detail_100.png)

Saved disclosed contrast-limited scientific figure for pla area cv absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 8,983 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [pla_area_cv_absolute_difference_detail_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/pla_area_cv_absolute_difference_detail_100.svg)

Saved disclosed contrast-limited scientific figure for pla area cv absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [pla_area_iqr_absolute_difference_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/pla_area_iqr_absolute_difference_100.png)

Saved full-range scientific figure for pla area iqr absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,010 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [pla_area_iqr_absolute_difference_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/pla_area_iqr_absolute_difference_100.svg)

Saved full-range scientific figure for pla area iqr absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [pla_area_iqr_absolute_difference_detail_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/pla_area_iqr_absolute_difference_detail_100.png)

Saved disclosed contrast-limited scientific figure for pla area iqr absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 8,983 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [pla_area_iqr_absolute_difference_detail_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/pla_area_iqr_absolute_difference_detail_100.svg)

Saved disclosed contrast-limited scientific figure for pla area iqr absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [pla_count_log2_fold_change_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/pla_count_log2_fold_change_100.png)

Saved full-range scientific figure for pla count log2 fold change 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 8,904 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [pla_count_log2_fold_change_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/pla_count_log2_fold_change_100.svg)

Saved full-range scientific figure for pla count log2 fold change 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [pla_count_log2_fold_change_detail_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/pla_count_log2_fold_change_detail_100.png)

Saved disclosed contrast-limited scientific figure for pla count log2 fold change detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 8,904 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [pla_count_log2_fold_change_detail_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/pla_count_log2_fold_change_detail_100.svg)

Saved disclosed contrast-limited scientific figure for pla count log2 fold change detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [pla_count_percent_change_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/pla_count_percent_change_100.png)

Saved full-range scientific figure for pla count percent change 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,116 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [pla_count_percent_change_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/pla_count_percent_change_100.svg)

Saved full-range scientific figure for pla count percent change 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [pla_count_percent_change_detail_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/pla_count_percent_change_detail_100.png)

Saved disclosed contrast-limited scientific figure for pla count percent change detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,010 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [pla_count_percent_change_detail_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/pla_count_percent_change_detail_100.svg)

Saved disclosed contrast-limited scientific figure for pla count percent change detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [section_pla_share_absolute_difference_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/section_pla_share_absolute_difference_100.png)

Saved full-range scientific figure for section pla share absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 8,983 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_pla_share_absolute_difference_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/section_pla_share_absolute_difference_100.svg)

Saved full-range scientific figure for section pla share absolute difference 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

### [section_pla_share_absolute_difference_detail_100.png](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/section_pla_share_absolute_difference_detail_100.png)

Saved disclosed contrast-limited scientific figure for section pla share absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

**Raster dimensions:** 9,089 × 5,262 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_pla_share_absolute_difference_detail_100.svg](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/figures/section_pla_share_absolute_difference_detail_100.svg)

Saved disclosed contrast-limited scientific figure for section pla share absolute difference detail 100. PNG is 600 DPI; SVG preserves vector measurement tiles, footprint and colorbar.

## `outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f`

### [report.json](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/report.json)

Definitions, settings, per-arm/resolution comparison summaries, figure manifest and validation for this metric run.

## `outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100`

### [large_pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/large_pla_count.npz)

Compressed numerical arrays for large pla count on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [large_pla_fraction.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/large_pla_fraction.npz)

Compressed numerical arrays for large pla fraction on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_large_pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/marker_associated_large_pla_count.npz)

Compressed numerical arrays for marker associated large pla count on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_area_fraction.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/marker_associated_pla_area_fraction.npz)

Compressed numerical arrays for marker associated pla area fraction on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/marker_associated_pla_count.npz)

Compressed numerical arrays for marker associated pla count on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_fraction.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/marker_associated_pla_fraction.npz)

Compressed numerical arrays for marker associated pla fraction on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_mean_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/marker_associated_pla_mean_area.npz)

Compressed numerical arrays for marker associated pla mean area on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/mean_pla_area.npz)

Compressed numerical arrays for mean pla area on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_intensity.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/mean_pla_intensity.npz)

Compressed numerical arrays for mean pla intensity on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_nearest_neighbor_distance.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/mean_pla_nearest_neighbor_distance.npz)

Compressed numerical arrays for mean pla nearest neighbor distance on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [median_pla_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/median_pla_area.npz)

Compressed numerical arrays for median pla area on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [median_pla_intensity.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/median_pla_intensity.npz)

Compressed numerical arrays for median pla intensity on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [p90_pla_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/p90_pla_area.npz)

Compressed numerical arrays for p90 pla area on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [pla_area_cv.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/pla_area_cv.npz)

Compressed numerical arrays for pla area cv on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [pla_area_iqr.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/pla_area_iqr.npz)

Compressed numerical arrays for pla area iqr on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/pla_count.npz)

Compressed numerical arrays for pla count on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [section_pla_share.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/section_pla_share.npz)

Compressed numerical arrays for section pla share on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [small_pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/small_pla_count.npz)

Compressed numerical arrays for small pla count on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [total_pla_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_100/total_pla_area.npz)

Compressed numerical arrays for total pla area on resolution 100 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

## `outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000`

### [large_pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/large_pla_count.npz)

Compressed numerical arrays for large pla count on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [large_pla_fraction.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/large_pla_fraction.npz)

Compressed numerical arrays for large pla fraction on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_large_pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/marker_associated_large_pla_count.npz)

Compressed numerical arrays for marker associated large pla count on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_area_fraction.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/marker_associated_pla_area_fraction.npz)

Compressed numerical arrays for marker associated pla area fraction on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/marker_associated_pla_count.npz)

Compressed numerical arrays for marker associated pla count on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_fraction.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/marker_associated_pla_fraction.npz)

Compressed numerical arrays for marker associated pla fraction on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_mean_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/marker_associated_pla_mean_area.npz)

Compressed numerical arrays for marker associated pla mean area on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/mean_pla_area.npz)

Compressed numerical arrays for mean pla area on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_intensity.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/mean_pla_intensity.npz)

Compressed numerical arrays for mean pla intensity on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_nearest_neighbor_distance.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/mean_pla_nearest_neighbor_distance.npz)

Compressed numerical arrays for mean pla nearest neighbor distance on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [median_pla_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/median_pla_area.npz)

Compressed numerical arrays for median pla area on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [median_pla_intensity.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/median_pla_intensity.npz)

Compressed numerical arrays for median pla intensity on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [p90_pla_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/p90_pla_area.npz)

Compressed numerical arrays for p90 pla area on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [pla_area_cv.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/pla_area_cv.npz)

Compressed numerical arrays for pla area cv on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [pla_area_iqr.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/pla_area_iqr.npz)

Compressed numerical arrays for pla area iqr on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/pla_count.npz)

Compressed numerical arrays for pla count on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [section_pla_share.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/section_pla_share.npz)

Compressed numerical arrays for section pla share on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [small_pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/small_pla_count.npz)

Compressed numerical arrays for small pla count on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [total_pla_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_1000/total_pla_area.npz)

Compressed numerical arrays for total pla area on resolution 1000 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

## `outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250`

### [large_pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/large_pla_count.npz)

Compressed numerical arrays for large pla count on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [large_pla_fraction.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/large_pla_fraction.npz)

Compressed numerical arrays for large pla fraction on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_large_pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/marker_associated_large_pla_count.npz)

Compressed numerical arrays for marker associated large pla count on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_area_fraction.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/marker_associated_pla_area_fraction.npz)

Compressed numerical arrays for marker associated pla area fraction on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/marker_associated_pla_count.npz)

Compressed numerical arrays for marker associated pla count on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_fraction.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/marker_associated_pla_fraction.npz)

Compressed numerical arrays for marker associated pla fraction on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_mean_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/marker_associated_pla_mean_area.npz)

Compressed numerical arrays for marker associated pla mean area on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/mean_pla_area.npz)

Compressed numerical arrays for mean pla area on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_intensity.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/mean_pla_intensity.npz)

Compressed numerical arrays for mean pla intensity on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_nearest_neighbor_distance.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/mean_pla_nearest_neighbor_distance.npz)

Compressed numerical arrays for mean pla nearest neighbor distance on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [median_pla_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/median_pla_area.npz)

Compressed numerical arrays for median pla area on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [median_pla_intensity.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/median_pla_intensity.npz)

Compressed numerical arrays for median pla intensity on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [p90_pla_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/p90_pla_area.npz)

Compressed numerical arrays for p90 pla area on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [pla_area_cv.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/pla_area_cv.npz)

Compressed numerical arrays for pla area cv on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [pla_area_iqr.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/pla_area_iqr.npz)

Compressed numerical arrays for pla area iqr on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/pla_count.npz)

Compressed numerical arrays for pla count on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [section_pla_share.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/section_pla_share.npz)

Compressed numerical arrays for section pla share on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [small_pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/small_pla_count.npz)

Compressed numerical arrays for small pla count on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [total_pla_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_250/total_pla_area.npz)

Compressed numerical arrays for total pla area on resolution 250 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

## `outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500`

### [large_pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/large_pla_count.npz)

Compressed numerical arrays for large pla count on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [large_pla_fraction.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/large_pla_fraction.npz)

Compressed numerical arrays for large pla fraction on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_large_pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/marker_associated_large_pla_count.npz)

Compressed numerical arrays for marker associated large pla count on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_area_fraction.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/marker_associated_pla_area_fraction.npz)

Compressed numerical arrays for marker associated pla area fraction on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/marker_associated_pla_count.npz)

Compressed numerical arrays for marker associated pla count on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_fraction.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/marker_associated_pla_fraction.npz)

Compressed numerical arrays for marker associated pla fraction on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [marker_associated_pla_mean_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/marker_associated_pla_mean_area.npz)

Compressed numerical arrays for marker associated pla mean area on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/mean_pla_area.npz)

Compressed numerical arrays for mean pla area on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_intensity.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/mean_pla_intensity.npz)

Compressed numerical arrays for mean pla intensity on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [mean_pla_nearest_neighbor_distance.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/mean_pla_nearest_neighbor_distance.npz)

Compressed numerical arrays for mean pla nearest neighbor distance on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [median_pla_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/median_pla_area.npz)

Compressed numerical arrays for median pla area on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [median_pla_intensity.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/median_pla_intensity.npz)

Compressed numerical arrays for median pla intensity on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [p90_pla_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/p90_pla_area.npz)

Compressed numerical arrays for p90 pla area on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [pla_area_cv.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/pla_area_cv.npz)

Compressed numerical arrays for pla area cv on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [pla_area_iqr.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/pla_area_iqr.npz)

Compressed numerical arrays for pla area iqr on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/pla_count.npz)

Compressed numerical arrays for pla count on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [section_pla_share.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/section_pla_share.npz)

Compressed numerical arrays for section pla share on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [small_pla_count.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/small_pla_count.npz)

Compressed numerical arrays for small pla count on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

### [total_pla_area.npz](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/resolution_500/total_pla_area.npz)

Compressed numerical arrays for total pla area on resolution 500 bins: section values/defined flags, two condition means/N, eligibility and all three contrasts/reasons.

**Stored arrays:** `section_ids`, `section_values`, `section_defined`, `x_edges`, `y_edges`, `hk1_homecage_mean`, `hk1_running_mean`, `hk1_homecage_valid_section_n`, `hk1_running_valid_section_n`, `hk1_eligibility`, `hk1_absolute_difference`, `hk1_absolute_difference_missing_reason`, `hk1_percent_change`, `hk1_percent_change_missing_reason`, `hk1_log2_fold_change`, `hk1_log2_fold_change_missing_reason`, `pfkp_homecage_mean`, `pfkp_running_mean`, `pfkp_homecage_valid_section_n`, `pfkp_running_valid_section_n`, `pfkp_eligibility`, `pfkp_absolute_difference`, `pfkp_absolute_difference_missing_reason`, `pfkp_percent_change`, `pfkp_percent_change_missing_reason`, `pfkp_log2_fold_change`, `pfkp_log2_fold_change_missing_reason`.

## `outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f`

### [summary.csv](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/summary.csv)

One row per measurement × comparison × arm × global grid; documents defined/missing counts, ranges and metric N.

**CSV columns:** `bin_width`, `measurement`, `comparison`, `arm`, `units`, `area_cutoff`, `marker`, `eligible_bins`, `defined_comparison_bins`, `undefined_eligible_bins`, `negative_bins`, `positive_bins`, `equal_bins`, `minimum`, `maximum`, `homecage_metric_N_0`, `running_metric_N_0`.

### [validation.json](../../outputs/calculation_functions/20261119T222024277618Z_4adcf19fac8f/validation.json)

Metric-run conservation/subset, count-preservation, geometry and provenance checks.

## `outputs/calculation_functions`

### [latest_run.json](../../outputs/calculation_functions/latest_run.json)

Small pointer selecting the active immutable run in outputs/calculation_functions. Loaders prefer the copied local run directory before recorded absolute paths.

## `outputs/comet_core`

### [alignment_replay_validation.json](../../outputs/comet_core/alignment_replay_validation.json)

Pixel/hash/transform checks comparing the reproduced alignment-check figure with its saved reference.

### [alignment_snapshot.json](../../outputs/comet_core/alignment_snapshot.json)

Frozen former-app section/source IDs, colors and placement transforms for replay, not a fresh fit.

### [asset_audit.json](../../outputs/comet_core/asset_audit.json)

Inventory and provenance of available alignment/data assets; distinguishes detections from absent microscopy/masks.

### [context_geometry.json](../../outputs/comet_core/context_geometry.json)

Exact finest observed-object occupancy and merged grid-edge boundaries, with holes, provenance hash and explicit non-tissue status.

## `outputs/comet_core/detailed_review`

### [alignment_detail_hk1.png](../../outputs/comet_core/detailed_review/alignment_detail_hk1.png)

High-resolution saved two-dimensional section-alignment atlas for the named PLA arm.

**Raster dimensions:** 9,898 × 7,608 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [alignment_detail_hk1.svg](../../outputs/comet_core/detailed_review/alignment_detail_hk1.svg)

High-resolution saved two-dimensional section-alignment atlas for the named PLA arm.

### [alignment_detail_pfkp.png](../../outputs/comet_core/detailed_review/alignment_detail_pfkp.png)

High-resolution saved two-dimensional section-alignment atlas for the named PLA arm.

**Raster dimensions:** 9,898 × 7,608 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [alignment_detail_pfkp.svg](../../outputs/comet_core/detailed_review/alignment_detail_pfkp.svg)

High-resolution saved two-dimensional section-alignment atlas for the named PLA arm.

### [manifest.json](../../outputs/comet_core/detailed_review/manifest.json)

Figure library manifest tied by hash to the selected count payload.

### [observed_support_detail_100.png](../../outputs/comet_core/detailed_review/observed_support_detail_100.png)

High-resolution per-condition detection-support map; counts supporting sections, not verified tissue area.

**Raster dimensions:** 8,169 × 8,181 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [observed_support_detail_100.svg](../../outputs/comet_core/detailed_review/observed_support_detail_100.svg)

High-resolution per-condition detection-support map; counts supporting sections, not verified tissue area.

## `outputs/comet_core/figures`

### [alignment_check_reference.png](../../outputs/comet_core/figures/alignment_check_reference.png)

Original or reproduced alignment-check image/vector asset. Its purpose is placement reproducibility, not independent anatomical validation.

**Raster dimensions:** 5,070 × 3,580 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [alignment_check_reproduced.png](../../outputs/comet_core/figures/alignment_check_reproduced.png)

Original or reproduced alignment-check image/vector asset. Its purpose is placement reproducibility, not independent anatomical validation.

**Raster dimensions:** 5,070 × 3,580 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [alignment_check_reproduced.svg](../../outputs/comet_core/figures/alignment_check_reproduced.svg)

Original or reproduced alignment-check image/vector asset. Its purpose is placement reproducibility, not independent anatomical validation.

### [calculation_functions_controls_2026-11-17.png](../../outputs/comet_core/figures/calculation_functions_controls_2026-11-17.png)

Dated app screenshot/review figure documenting the interface at that time. Earlier 12K/selector demonstrations are historical; current PNG downloads are fixed at 8K.

### [calculation_functions_heatmaps_2026-11-17.png](../../outputs/comet_core/figures/calculation_functions_heatmaps_2026-11-17.png)

Dated app screenshot/review figure documenting the interface at that time. Earlier 12K/selector demonstrations are historical; current PNG downloads are fixed at 8K.

### [export_size_explanation_2026-11-19.png](../../outputs/comet_core/figures/export_size_explanation_2026-11-19.png)

Dated app screenshot/review figure documenting the interface at that time. Earlier 12K/selector demonstrations are historical; current PNG downloads are fixed at 8K.

**Raster dimensions:** 1,600 × 1,100 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [fine_detail_10_unit_grid_2026-11-19.png](../../outputs/comet_core/figures/fine_detail_10_unit_grid_2026-11-19.png)

Dated app screenshot/review figure documenting the interface at that time. Earlier 12K/selector demonstrations are historical; current PNG downloads are fixed at 8K.

**Raster dimensions:** 1,600 × 1,100 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [fine_detail_mean_area_vector_2026-11-19.svg](../../outputs/comet_core/figures/fine_detail_mean_area_vector_2026-11-19.svg)

Retained browser export with settings encoded in its SVG/protocol. Earlier 12K/selector demonstrations are historical; current PNG downloads are fixed at 8K.

### [fixed_alignment_app_2026-11-14.png](../../outputs/comet_core/figures/fixed_alignment_app_2026-11-14.png)

Dated app screenshot/review figure documenting the interface at that time. Earlier 12K/selector demonstrations are historical; current PNG downloads are fixed at 8K.

### [fixed_support_app_2026-11-14.png](../../outputs/comet_core/figures/fixed_support_app_2026-11-14.png)

Dated app screenshot/review figure documenting the interface at that time. Earlier 12K/selector demonstrations are historical; current PNG downloads are fixed at 8K.

### [fixed_three_difference_app_2026-11-14.png](../../outputs/comet_core/figures/fixed_three_difference_app_2026-11-14.png)

Dated app screenshot/review figure documenting the interface at that time. Earlier 12K/selector demonstrations are historical; current PNG downloads are fixed at 8K.

### [fixed_three_mean_app_2026-11-14.png](../../outputs/comet_core/figures/fixed_three_mean_app_2026-11-14.png)

Dated app screenshot/review figure documenting the interface at that time. Earlier 12K/selector demonstrations are historical; current PNG downloads are fixed at 8K.

### [high_resolution_detail_12000px_2026-11-19.png](../../outputs/comet_core/figures/high_resolution_detail_12000px_2026-11-19.png)

Retained browser export with settings encoded in its SVG/protocol. Earlier 12K/selector demonstrations are historical; current PNG downloads are fixed at 8K.

**Raster dimensions:** 12,000 × 12,600 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [high_resolution_mean_area_8000px_2026-11-19.png](../../outputs/comet_core/figures/high_resolution_mean_area_8000px_2026-11-19.png)

Retained browser export with settings encoded in its SVG/protocol. Earlier 12K/selector demonstrations are historical; current PNG downloads are fixed at 8K.

**Raster dimensions:** 8,000 × 8,126 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [mean_area_whole_field_vector_2026-11-19.svg](../../outputs/comet_core/figures/mean_area_whole_field_vector_2026-11-19.svg)

Retained browser export with settings encoded in its SVG/protocol. Earlier 12K/selector demonstrations are historical; current PNG downloads are fixed at 8K.

### [pla_count_whole_field_12000px_2026-11-19.png](../../outputs/comet_core/figures/pla_count_whole_field_12000px_2026-11-19.png)

Retained browser export with settings encoded in its SVG/protocol. Earlier 12K/selector demonstrations are historical; current PNG downloads are fixed at 8K.

**Raster dimensions:** 12,000 × 12,190 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [pla_count_whole_field_8000px_2026-11-19.png](../../outputs/comet_core/figures/pla_count_whole_field_8000px_2026-11-19.png)

Retained browser export with settings encoded in its SVG/protocol. Earlier 12K/selector demonstrations are historical; current PNG downloads are fixed at 8K.

**Raster dimensions:** 8,000 × 8,126 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [spatial_controls_2026-11-19.png](../../outputs/comet_core/figures/spatial_controls_2026-11-19.png)

Dated app screenshot/review figure documenting the interface at that time. Earlier 12K/selector demonstrations are historical; current PNG downloads are fixed at 8K.

**Raster dimensions:** 1,600 × 1,100 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [spatial_outline_heatmaps_2026-11-19.png](../../outputs/comet_core/figures/spatial_outline_heatmaps_2026-11-19.png)

Dated app screenshot/review figure documenting the interface at that time. Earlier 12K/selector demonstrations are historical; current PNG downloads are fixed at 8K.

**Raster dimensions:** 1,600 × 1,100 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

## `outputs/core_view`

### [payload.json](../../outputs/core_view/payload.json)

Saved strict viewer payload and its input blockers; absence of strict masks does not block the separate authorized exploratory app.

## `outputs/exploratory_multiresolution/20261112T230929125171Z_55527b6c71a2`

### [index.json](../../outputs/exploratory_multiresolution/20261112T230929125171Z_55527b6c71a2/index.json)

Saved multiresolution predecessor index: identifies grids, input hashes, conservation and recorded historical summary settings.

### [parameters.json](../../outputs/exploratory_multiresolution/20261112T230929125171Z_55527b6c71a2/parameters.json)

Saved multiresolution predecessor parameters: identifies grids, input hashes, conservation and recorded historical summary settings.

### [validation.json](../../outputs/exploratory_multiresolution/20261112T230929125171Z_55527b6c71a2/validation.json)

Saved multiresolution predecessor validation: identifies grids, input hashes, conservation and recorded historical summary settings.

### [view_payload.json](../../outputs/exploratory_multiresolution/20261112T230929125171Z_55527b6c71a2/view_payload.json)

Raw-validated four-resolution count cache and full PLA point provenance; current analysis reuses these counts/positions, while its older observed-support means remain historical.

## `outputs/exploratory_multiresolution`

### [latest_run.json](../../outputs/exploratory_multiresolution/latest_run.json)

Small pointer selecting the active immutable run in outputs/exploratory_multiresolution. Loaders prefer the copied local run directory before recorded absolute paths.

## `outputs/inventory`

### [column_profiles.csv](../../outputs/inventory/column_profiles.csv)

Per-column missingness/type/range profiles from the original intake.

**CSV columns:** `file_id`, `column`, `missing_count`, `numeric_count`, `non_numeric_count`, `non_finite_count`, `integer_valued_count`, `zero_count`, `negative_count`, `numeric_min`, `numeric_max`, `examples`, `categorical_counts`, `observed_type`.

### [file_audit.json](../../outputs/inventory/file_audit.json)

Original file identity/classification and duplicate audit.

### [reference_manifest.csv](../../outputs/inventory/reference_manifest.csv)

References to background inputs kept separate from active experiment files.

**CSV columns:** `path`, `filename`, `size_bytes`, `sha256`.

### [report.md](../../outputs/inventory/report.md)

Readable original intake inventory findings and unresolved-at-the-time observations.

### [sample_metadata_observed.csv](../../outputs/inventory/sample_metadata_observed.csv)

File-observed sample clues; scientific identity is supplied by later explicit metadata.

**CSV columns:** `file_id`, `exported_analysis_region`, `rows_in_export_region`, `animal_id`, `condition`, `pla_arm`, `physical_section_id`, `roi_id`, `biological_replicate_id`, `technical_repeat_of`, `include_in_primary_analysis`, `approved_alignment_id`, `aligned_centroid_source`, `tissue_mask_source`, `coordinate_units`, `assignment_status`, `evidence`.

### [summary.json](../../outputs/inventory/summary.json)

Original intake totals and schema summary.

### [validation.json](../../outputs/inventory/validation.json)

Inventory/source-row/schema validation results.

### [within_input_overlap.csv](../../outputs/inventory/within_input_overlap.csv)

Overlap between historical exports; rows here do not create additional animals.

**CSV columns:** `left_file_id`, `right_file_id`, `byte_identical`, `exact_exported_row_signatures_shared`, `measurement_signatures_shared_excluding_region_and_object_id`, `left_unique_measurement_signature_count`, `right_unique_measurement_signature_count`, `left_signature_shared_fraction`, `right_signature_shared_fraction`, `interpretation`.

## `outputs/measurement_features/20261118T023734594332Z_ab4d15ecc15b`

### [features.json](../../outputs/measurement_features/20261118T023734594332Z_ab4d15ecc15b/features.json)

Full-precision PLA area/intensity/ChAT vectors indexed to exact cached objects; the later run also contains full-section nearest-neighbor distances and predecessor lineage.

### [validation.json](../../outputs/measurement_features/20261118T023734594332Z_ab4d15ecc15b/validation.json)

Validation of the attribute cache, source/object-order matching and any later spatial-vector extension.

## `outputs/measurement_features/20261119T221023384317Z_ab4d15ecc15b`

### [features.json](../../outputs/measurement_features/20261119T221023384317Z_ab4d15ecc15b/features.json)

Full-precision PLA area/intensity/ChAT vectors indexed to exact cached objects; the later run also contains full-section nearest-neighbor distances and predecessor lineage.

### [validation.json](../../outputs/measurement_features/20261119T221023384317Z_ab4d15ecc15b/validation.json)

Validation of the attribute cache, source/object-order matching and any later spatial-vector extension.

## `outputs/measurement_features`

### [latest_run.json](../../outputs/measurement_features/latest_run.json)

Small pointer selecting the active immutable run in outputs/measurement_features. Loaders prefer the copied local run directory before recorded absolute paths.

## `outputs/native_atlas`

### [morphology_object_review_targets.csv](../../outputs/native_atlas/morphology_object_review_targets.csv)

Historical native-export source-object review windows including morphology eligibility/QC targeting. Coordinates identify inspection targets, not validated cell classes.

**CSV columns:** `file_id`, `job_id`, `source_filename`, `source_sha256`, `source_row_index_zero_based`, `source_csv_record_number_including_header`, `object_id`, `object_type`, `exported_analysis_region`, `review_reason`, `rank_within_reason`, `xmin`, `xmax`, `ymin`, `ymax`, `x_midpoint`, `y_midpoint`, `exported_area`, `minimum_diameter`, `maximum_diameter`, `diameter_ratio_minimum_over_maximum`, `diameter_ratio_eligible`, `exported_ChAT_flag`, `retained_in_raw_PLA_count`, `coordinate_units`, `area_units`, `diameter_units`, `coordinate_proxy`, `selection_scope`, `scientific_status`.

### [review_targets.csv](../../outputs/native_atlas/review_targets.csv)

Historical native-export source-object review windows for selected high/low association patterns. Coordinates identify inspection targets, not validated cell classes.

**CSV columns:** `file_id`, `job_id`, `source_filename`, `source_sha256`, `review_reason`, `rank_within_reason`, `x_bin`, `y_bin`, `xmin`, `xmax`, `ymin`, `ymax`, `PLA_count`, `PLA_ChAT_flag_positive`, `PLA_ChAT_flag_fraction`, `ChAT_count`, `coordinate_units`, `coordinate_proxy`, `tissue_coverage_status`, `scientific_status`.

## `outputs/protocols`

### [alignment_support_review_2026-11-12.json](../../outputs/protocols/alignment_support_review_2026-11-12.json)

Dated audit/provenance record for alignment support review 2026-11-12. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [calculation_csv_browser_export_2026-11-17.json](../../outputs/protocols/calculation_csv_browser_export_2026-11-17.json)

Dated audit/provenance record for calculation csv browser export 2026-11-17. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [calculation_engine_parity_2026-11-17.json](../../outputs/protocols/calculation_engine_parity_2026-11-17.json)

Dated audit/provenance record for calculation engine parity 2026-11-17. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [calculation_engine_parity_2026-11-19.json](../../outputs/protocols/calculation_engine_parity_2026-11-19.json)

Dated audit/provenance record for calculation engine parity 2026-11-19. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [calculation_functions_2026-11-17.json](../../outputs/protocols/calculation_functions_2026-11-17.json)

Dated audit/provenance record for calculation functions 2026-11-17. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [comet_core_focus_2026-11-11.json](../../outputs/protocols/comet_core_focus_2026-11-11.json)

Dated audit/provenance record for comet core focus 2026-11-11. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [comet_core_focus_2026-11-11_final.json](../../outputs/protocols/comet_core_focus_2026-11-11_final.json)

Dated audit/provenance record for comet core focus 2026-11-11 final. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [detailed_heatmaps_2026-11-12.json](../../outputs/protocols/detailed_heatmaps_2026-11-12.json)

Dated audit/provenance record for detailed heatmaps 2026-11-12. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [exploratory_count_maps_2026-11-11.json](../../outputs/protocols/exploratory_count_maps_2026-11-11.json)

Dated audit/provenance record for exploratory count maps 2026-11-11. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [export_resolution_clarity_2026-11-19.json](../../outputs/protocols/export_resolution_clarity_2026-11-19.json)

Dated audit/provenance record for export resolution clarity 2026-11-19. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [export_size_browser_check_2026-11-19.json](../../outputs/protocols/export_size_browser_check_2026-11-19.json)

Dated audit/provenance record for export size browser check 2026-11-19. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [fixed_export_size_2026-11-19.json](../../outputs/protocols/fixed_export_size_2026-11-19.json)

Dated audit/provenance record for fixed export size 2026-11-19. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [fixed_three_means_2026-11-14.json](../../outputs/protocols/fixed_three_means_2026-11-14.json)

Dated audit/provenance record for fixed three means 2026-11-14. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [instructions_extracted.json](../../outputs/protocols/instructions_extracted.json)

Recorded text/page extraction from the original scientist instructions; not an executable or independent assignment authority.

### [native_atlas_upgrade_snapshot.json](../../outputs/protocols/native_atlas_upgrade_snapshot.json)

Dated audit/provenance record for native atlas upgrade snapshot. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [nearest_neighbor_validation_2026-11-19.json](../../outputs/protocols/nearest_neighbor_validation_2026-11-19.json)

Dated audit/provenance record for nearest neighbor validation 2026-11-19. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [project_setup_snapshot.json](../../outputs/protocols/project_setup_snapshot.json)

Dated audit/provenance record for project setup snapshot. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [publication_2026-11-14.json](../../outputs/protocols/publication_2026-11-14.json)

Dated audit/provenance record for publication 2026-11-14. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [publication_portability_2026-11-19.json](../../outputs/protocols/publication_portability_2026-11-19.json)

Dated audit/provenance record for publication portability 2026-11-19. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [repository_appendix_validation_2026-11-19.json](../../outputs/protocols/repository_appendix_validation_2026-11-19.json)

Dated audit/provenance record for repository appendix validation 2026-11-19. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [source_revalidation_2026-11-14.json](../../outputs/protocols/source_revalidation_2026-11-14.json)

Dated audit/provenance record for source revalidation 2026-11-14. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [spatial_browser_validation_2026-11-19.json](../../outputs/protocols/spatial_browser_validation_2026-11-19.json)

Dated audit/provenance record for spatial browser validation 2026-11-19. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [spatial_extension_preservation_2026-11-19.json](../../outputs/protocols/spatial_extension_preservation_2026-11-19.json)

Dated audit/provenance record for spatial extension preservation 2026-11-19. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

### [spatial_extensions_2026-11-19.json](../../outputs/protocols/spatial_extensions_2026-11-19.json)

Dated audit/provenance record for spatial extensions 2026-11-19. Its timestamp fixes the code/inputs/settings/checks it describes; later updates do not retroactively alter it.

## `outputs`

### [publication_manifest.json](../../outputs/publication_manifest.json)

Selected repository publication inventory and validation record; earlier publication records remain dated in protocols.

## `outputs/section_means/20261114T175717494903Z_ab4d15ecc15b`

### [detailed_figure_manifest.json](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/detailed_figure_manifest.json)

Figure paths, parameters, scales and captions for this count-run figure library.

## `outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/figures`

### [section_mean_differences_100.png](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/figures/section_mean_differences_100.png)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 9,010 × 5,316 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_mean_differences_100.svg](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/figures/section_mean_differences_100.svg)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_mean_differences_250.png](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/figures/section_mean_differences_250.png)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 9,010 × 5,316 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_mean_differences_250.svg](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/figures/section_mean_differences_250.svg)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_mean_differences_contrast_100.png](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/figures/section_mean_differences_contrast_100.png)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 8,957 × 5,316 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_mean_differences_contrast_100.svg](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/figures/section_mean_differences_contrast_100.svg)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_mean_differences_contrast_250.png](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/figures/section_mean_differences_contrast_250.png)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 8,957 × 5,316 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_mean_differences_contrast_250.svg](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/figures/section_mean_differences_contrast_250.svg)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_means_and_difference_100.png](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/figures/section_means_and_difference_100.png)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 11,255 × 8,754 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_means_and_difference_100.svg](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/figures/section_means_and_difference_100.svg)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_means_and_difference_250.png](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/figures/section_means_and_difference_250.png)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 11,255 × 8,754 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_means_and_difference_250.svg](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/figures/section_means_and_difference_250.svg)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_means_and_difference_contrast_100.png](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/figures/section_means_and_difference_contrast_100.png)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 11,202 × 8,754 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_means_and_difference_contrast_100.svg](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/figures/section_means_and_difference_contrast_100.svg)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_means_and_difference_contrast_250.png](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/figures/section_means_and_difference_contrast_250.png)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 11,202 × 8,754 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_means_and_difference_contrast_250.svg](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/figures/section_means_and_difference_contrast_250.svg)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

## `outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_100`

### [hk1_bins.csv](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_100/hk1_bins.csv)

Complete HK1 spatial bin table for resolution 100: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [hk1_matrices.npz](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_100/hk1_matrices.npz)

Compressed HK1 grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

### [pfkp_bins.csv](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_100/pfkp_bins.csv)

Complete PFKP spatial bin table for resolution 100: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [pfkp_matrices.npz](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_100/pfkp_matrices.npz)

Compressed PFKP grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

## `outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_1000`

### [hk1_bins.csv](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_1000/hk1_bins.csv)

Complete HK1 spatial bin table for resolution 1000: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [hk1_matrices.npz](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_1000/hk1_matrices.npz)

Compressed HK1 grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

### [pfkp_bins.csv](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_1000/pfkp_bins.csv)

Complete PFKP spatial bin table for resolution 1000: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [pfkp_matrices.npz](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_1000/pfkp_matrices.npz)

Compressed PFKP grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

## `outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_250`

### [hk1_bins.csv](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_250/hk1_bins.csv)

Complete HK1 spatial bin table for resolution 250: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [hk1_matrices.npz](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_250/hk1_matrices.npz)

Compressed HK1 grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

### [pfkp_bins.csv](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_250/pfkp_bins.csv)

Complete PFKP spatial bin table for resolution 250: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [pfkp_matrices.npz](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_250/pfkp_matrices.npz)

Compressed PFKP grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

## `outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_500`

### [hk1_bins.csv](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_500/hk1_bins.csv)

Complete HK1 spatial bin table for resolution 500: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [hk1_matrices.npz](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_500/hk1_matrices.npz)

Compressed HK1 grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

### [pfkp_bins.csv](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_500/pfkp_bins.csv)

Complete PFKP spatial bin table for resolution 500: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [pfkp_matrices.npz](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/resolution_500/pfkp_matrices.npz)

Compressed PFKP grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

## `outputs/section_means/20261114T175717494903Z_ab4d15ecc15b`

### [source_record.json](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/source_record.json)

Identity/hash of the unchanged raw-count predecessor used to derive this immutable fixed-three run.

### [validation.json](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/validation.json)

Count conservation, fixed denominator, exact source/transform/point and derived mean checks for this run.

### [view_payload.json](../../outputs/section_means/20261114T175717494903Z_ab4d15ecc15b/view_payload.json)

Four-grid fixed-three count means plus source section matrices and complete unsampled PLA locations; active run selection comes from latest_run.json.

## `outputs/section_means/20261118T025601453031Z_ab4d15ecc15b`

### [detailed_figure_manifest.json](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/detailed_figure_manifest.json)

Figure paths, parameters, scales and captions for this count-run figure library.

## `outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/figures`

### [section_mean_differences_100.png](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/figures/section_mean_differences_100.png)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 9,010 × 5,316 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_mean_differences_100.svg](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/figures/section_mean_differences_100.svg)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_mean_differences_250.png](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/figures/section_mean_differences_250.png)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 9,010 × 5,316 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_mean_differences_250.svg](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/figures/section_mean_differences_250.svg)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_mean_differences_contrast_100.png](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/figures/section_mean_differences_contrast_100.png)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 8,957 × 5,316 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_mean_differences_contrast_100.svg](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/figures/section_mean_differences_contrast_100.svg)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_mean_differences_contrast_250.png](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/figures/section_mean_differences_contrast_250.png)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 8,957 × 5,316 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_mean_differences_contrast_250.svg](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/figures/section_mean_differences_contrast_250.svg)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_means_and_difference_100.png](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/figures/section_means_and_difference_100.png)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 11,255 × 8,754 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_means_and_difference_100.svg](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/figures/section_means_and_difference_100.svg)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_means_and_difference_250.png](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/figures/section_means_and_difference_250.png)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 11,255 × 8,754 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_means_and_difference_250.svg](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/figures/section_means_and_difference_250.svg)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_means_and_difference_contrast_100.png](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/figures/section_means_and_difference_contrast_100.png)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 11,202 × 8,754 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_means_and_difference_contrast_100.svg](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/figures/section_means_and_difference_contrast_100.svg)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_means_and_difference_contrast_250.png](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/figures/section_means_and_difference_contrast_250.png)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 11,202 × 8,754 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_means_and_difference_contrast_250.svg](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/figures/section_means_and_difference_contrast_250.svg)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

## `outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_100`

### [hk1_bins.csv](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_100/hk1_bins.csv)

Complete HK1 spatial bin table for resolution 100: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [hk1_matrices.npz](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_100/hk1_matrices.npz)

Compressed HK1 grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

### [pfkp_bins.csv](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_100/pfkp_bins.csv)

Complete PFKP spatial bin table for resolution 100: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [pfkp_matrices.npz](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_100/pfkp_matrices.npz)

Compressed PFKP grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

## `outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_1000`

### [hk1_bins.csv](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_1000/hk1_bins.csv)

Complete HK1 spatial bin table for resolution 1000: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [hk1_matrices.npz](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_1000/hk1_matrices.npz)

Compressed HK1 grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

### [pfkp_bins.csv](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_1000/pfkp_bins.csv)

Complete PFKP spatial bin table for resolution 1000: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [pfkp_matrices.npz](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_1000/pfkp_matrices.npz)

Compressed PFKP grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

## `outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_250`

### [hk1_bins.csv](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_250/hk1_bins.csv)

Complete HK1 spatial bin table for resolution 250: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [hk1_matrices.npz](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_250/hk1_matrices.npz)

Compressed HK1 grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

### [pfkp_bins.csv](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_250/pfkp_bins.csv)

Complete PFKP spatial bin table for resolution 250: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [pfkp_matrices.npz](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_250/pfkp_matrices.npz)

Compressed PFKP grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

## `outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_500`

### [hk1_bins.csv](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_500/hk1_bins.csv)

Complete HK1 spatial bin table for resolution 500: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [hk1_matrices.npz](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_500/hk1_matrices.npz)

Compressed HK1 grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

### [pfkp_bins.csv](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_500/pfkp_bins.csv)

Complete PFKP spatial bin table for resolution 500: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [pfkp_matrices.npz](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/resolution_500/pfkp_matrices.npz)

Compressed PFKP grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

## `outputs/section_means/20261118T025601453031Z_ab4d15ecc15b`

### [source_record.json](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/source_record.json)

Identity/hash of the unchanged raw-count predecessor used to derive this immutable fixed-three run.

### [validation.json](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/validation.json)

Count conservation, fixed denominator, exact source/transform/point and derived mean checks for this run.

### [view_payload.json](../../outputs/section_means/20261118T025601453031Z_ab4d15ecc15b/view_payload.json)

Four-grid fixed-three count means plus source section matrices and complete unsampled PLA locations; active run selection comes from latest_run.json.

## `outputs/section_means/20261119T221951584723Z_ab4d15ecc15b`

### [detailed_figure_manifest.json](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/detailed_figure_manifest.json)

Figure paths, parameters, scales and captions for this count-run figure library.

## `outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/figures`

### [section_mean_differences_100.png](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/figures/section_mean_differences_100.png)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 9,010 × 5,316 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_mean_differences_100.svg](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/figures/section_mean_differences_100.svg)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_mean_differences_250.png](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/figures/section_mean_differences_250.png)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 9,010 × 5,316 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_mean_differences_250.svg](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/figures/section_mean_differences_250.svg)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_mean_differences_contrast_100.png](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/figures/section_mean_differences_contrast_100.png)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 8,957 × 5,316 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_mean_differences_contrast_100.svg](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/figures/section_mean_differences_contrast_100.svg)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_mean_differences_contrast_250.png](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/figures/section_mean_differences_contrast_250.png)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 8,957 × 5,316 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_mean_differences_contrast_250.svg](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/figures/section_mean_differences_contrast_250.svg)

Saved fixed-three PLA count difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_means_and_difference_100.png](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/figures/section_means_and_difference_100.png)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 11,255 × 8,754 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_means_and_difference_100.svg](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/figures/section_means_and_difference_100.svg)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_means_and_difference_250.png](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/figures/section_means_and_difference_250.png)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 11,255 × 8,754 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_means_and_difference_250.svg](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/figures/section_means_and_difference_250.svg)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_means_and_difference_contrast_100.png](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/figures/section_means_and_difference_contrast_100.png)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 11,202 × 8,754 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_means_and_difference_contrast_100.svg](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/figures/section_means_and_difference_contrast_100.svg)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

### [section_means_and_difference_contrast_250.png](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/figures/section_means_and_difference_contrast_250.png)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

**Raster dimensions:** 11,202 × 8,754 pixels. These are export dimensions, not microscope calibration or extra scientific bins.

### [section_means_and_difference_contrast_250.svg](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/figures/section_means_and_difference_contrast_250.svg)

Saved fixed-three PLA count means plus difference figure; contrast variants disclose saturation, and resolution is identified in the filename/manifest.

## `outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_100`

### [hk1_bins.csv](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_100/hk1_bins.csv)

Complete HK1 spatial bin table for resolution 100: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [hk1_matrices.npz](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_100/hk1_matrices.npz)

Compressed HK1 grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

### [pfkp_bins.csv](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_100/pfkp_bins.csv)

Complete PFKP spatial bin table for resolution 100: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [pfkp_matrices.npz](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_100/pfkp_matrices.npz)

Compressed PFKP grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

## `outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_1000`

### [hk1_bins.csv](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_1000/hk1_bins.csv)

Complete HK1 spatial bin table for resolution 1000: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [hk1_matrices.npz](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_1000/hk1_matrices.npz)

Compressed HK1 grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

### [pfkp_bins.csv](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_1000/pfkp_bins.csv)

Complete PFKP spatial bin table for resolution 1000: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [pfkp_matrices.npz](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_1000/pfkp_matrices.npz)

Compressed PFKP grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

## `outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_250`

### [hk1_bins.csv](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_250/hk1_bins.csv)

Complete HK1 spatial bin table for resolution 250: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [hk1_matrices.npz](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_250/hk1_matrices.npz)

Compressed HK1 grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

### [pfkp_bins.csv](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_250/pfkp_bins.csv)

Complete PFKP spatial bin table for resolution 250: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [pfkp_matrices.npz](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_250/pfkp_matrices.npz)

Compressed PFKP grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

## `outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_500`

### [hk1_bins.csv](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_500/hk1_bins.csv)

Complete HK1 spatial bin table for resolution 500: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [hk1_matrices.npz](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_500/hk1_matrices.npz)

Compressed HK1 grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

### [pfkp_bins.csv](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_500/pfkp_bins.csv)

Complete PFKP spatial bin table for resolution 500: three-section means, R−H and observed-support diagnostics, including missing/outside-domain status.

**CSV columns:** `arm`, `xmin`, `xmax`, `ymin`, `ymax`, `homecage_mean`, `running_mean`, `running_minus_homecage`, `mean_denominator_each_condition`, `homecage_observed_N`, `running_observed_N`, `homecage_assumed_zero_sections`, `running_assumed_zero_sections`, `display_domain`, `coverage_verified`.

### [pfkp_matrices.npz](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/resolution_500/pfkp_matrices.npz)

Compressed PFKP grid matrices behind the count means, differences, eligibility and observed support at this resolution.

**Stored arrays:** `homecage_mean`, `running_mean`, `difference`, `display_difference`, `homecage_count_sum`, `running_count_sum`, `homecage_observed_section_n`, `running_observed_section_n`, `homecage_complete_observed_support`, `running_complete_observed_support`, `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n`, `observed_union`, `displayable`, `tissue_coverage_known`.

## `outputs/section_means/20261119T221951584723Z_ab4d15ecc15b`

### [source_record.json](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/source_record.json)

Identity/hash of the unchanged raw-count predecessor used to derive this immutable fixed-three run.

### [validation.json](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/validation.json)

Count conservation, fixed denominator, exact source/transform/point and derived mean checks for this run.

### [view_payload.json](../../outputs/section_means/20261119T221951584723Z_ab4d15ecc15b/view_payload.json)

Four-grid fixed-three count means plus source section matrices and complete unsampled PLA locations; active run selection comes from latest_run.json.

## `outputs/section_means`

### [latest_run.json](../../outputs/section_means/latest_run.json)

Small pointer selecting the active immutable run in outputs/section_means. Loaders prefer the copied local run directory before recorded absolute paths.

## `outputs`

### [test_log_appendix_publication_2026-11-19.txt](../../outputs/test_log_appendix_publication_2026-11-19.txt)

Saved software-check output for appendix publication 2026-11-19. Expected fictional BLOCKED fixtures in these logs are not failures of the current exploratory results.

### [test_log_calculation_functions_2026-11-17.txt](../../outputs/test_log_calculation_functions_2026-11-17.txt)

Saved software-check output for calculation functions 2026-11-17. Expected fictional BLOCKED fixtures in these logs are not failures of the current exploratory results.

### [test_log_calculation_functions_final_2026-11-17.txt](../../outputs/test_log_calculation_functions_final_2026-11-17.txt)

Saved software-check output for calculation functions final 2026-11-17. Expected fictional BLOCKED fixtures in these logs are not failures of the current exploratory results.

### [test_log_export_clarity_2026-11-19.txt](../../outputs/test_log_export_clarity_2026-11-19.txt)

Saved software-check output for export clarity 2026-11-19. Expected fictional BLOCKED fixtures in these logs are not failures of the current exploratory results.

### [test_log_fixed_export_size_2026-11-19.txt](../../outputs/test_log_fixed_export_size_2026-11-19.txt)

Saved software-check output for fixed export size 2026-11-19. Expected fictional BLOCKED fixtures in these logs are not failures of the current exploratory results.

### [test_log_fixed_three_2026-11-14.txt](../../outputs/test_log_fixed_three_2026-11-14.txt)

Saved software-check output for fixed three 2026-11-14. Expected fictional BLOCKED fixtures in these logs are not failures of the current exploratory results.

### [test_log_publication_2026-11-14.txt](../../outputs/test_log_publication_2026-11-14.txt)

Saved software-check output for publication 2026-11-14. Expected fictional BLOCKED fixtures in these logs are not failures of the current exploratory results.

### [test_log_spatial_extensions_2026-11-19.txt](../../outputs/test_log_spatial_extensions_2026-11-19.txt)

Saved software-check output for spatial extensions 2026-11-19. Expected fictional BLOCKED fixtures in these logs are not failures of the current exploratory results.

### [validation.json](../../outputs/validation.json)

Latest combined analysis/software verification, with current update records; detailed dated evidence is kept in protocols.

## Repository root

### [pyproject.toml](../../pyproject.toml)

Python package metadata and core/report dependency groups; it does not contain scientific measurements.

### [requirements-lock.txt](../../requirements-lock.txt)

Exact recorded dependency versions, with a macOS-only marker for appnope; supports environment reproduction.

### [requirements.txt](../../requirements.txt)

Compatible dependency version ranges for the complete scientific reporting environment.

## `scripts`

### [build_comet_core_explorer.py](../../scripts/build_comet_core_explorer.py)

Bundles Plotly, validated caches, alignment assets, context geometry and local JS/CSS into one offline HTML file.

**Named code items:** [load_exploratory](../../scripts/build_comet_core_explorer.py#L20), [load_multiresolution](../../scripts/build_comet_core_explorer.py#L79), [build](../../scripts/build_comet_core_explorer.py#L135).

### [build_comet_core_report.py](../../scripts/build_comet_core_report.py)

Connects strict preflight diagnostics and saved exploratory runs, updates workflow assets and rebuilds the current app.

**Named code items:** [build](../../scripts/build_comet_core_report.py#L17).

### [build_comet_workflow.py](../../scripts/build_comet_workflow.py)

Draws the current experiment-to-results workflow used by the report/app build.

**Named code items:** [build](../../scripts/build_comet_workflow.py#L12).

### [build_current_notebook.py](../../scripts/build_current_notebook.py)

Generates the current main notebook source and clears saved execution output; follow structural edits with execution.

**Named code items:** [measurement_cells](../../scripts/build_current_notebook.py#L8), [build](../../scripts/build_current_notebook.py#L51).

### [build_detailed_figures.py](../../scripts/build_detailed_figures.py)

Earlier multiresolution count/support atlas; its historical support-based estimator must not replace current means.

**Named code items:** [build](../../scripts/build_detailed_figures.py#L22).

### [build_exploratory_figures.py](../../scripts/build_exploratory_figures.py)

Earlier exploratory mean/difference/support figures from the selected completed raw exports.

**Named code items:** [build](../../scripts/build_exploratory_figures.py#L22).

### [build_findings.py](../../scripts/build_findings.py)

Historical descriptive native-export findings and source-review targets; does not establish the current condition comparison.

**Named code items:** [build](../../scripts/build_findings.py#L15).

### [build_measurement_features.py](../../scripts/build_measurement_features.py)

CLI wrapper that extracts the source-verified attribute cache from authorized original CSVs.

### [build_measurement_report.py](../../scripts/build_measurement_report.py)

Calculates all nineteen metrics on four global grids; writes NPZ/CSV reports and true-vector/600-DPI figure pairs.

**Named code items:** [save_figure](../../scripts/build_measurement_report.py#L40), [build](../../scripts/build_measurement_report.py#L102).

### [build_multiresolution_maps.py](../../scripts/build_multiresolution_maps.py)

CLI wrapper for full raw recounting on the four recorded aligned grids.

**Named code items:** [main](../../scripts/build_multiresolution_maps.py#L13).

### [build_native_notebook.py](../../scripts/build_native_notebook.py)

Generates the separate historical native supporting notebook; rerunning it can rewrite shared report/validation outputs.

**Named code items:** [build](../../scripts/build_native_notebook.py#L8).

### [build_notebook.py](../../scripts/build_notebook.py)

Current notebook entry point delegates to the modern builder; retains an explicitly named historical observed-support notebook builder.

**Named code items:** [review_cells](../../scripts/build_notebook.py#L7), [build_historical_observed_support_report](../../scripts/build_notebook.py#L31), [build](../../scripts/build_notebook.py#L294).

### [build_report.py](../../scripts/build_report.py)

Historical native report/figure/workflow build; can rewrite shared output names and is not the current app entry point.

**Named code items:** [save](../../scripts/build_report.py#L22), [build](../../scripts/build_report.py#L30).

### [build_repository_appendix.py](../../scripts/build_repository_appendix.py)

Rebuilds this complete selected-file catalog and its static workflow SVG, then checks coverage and Markdown links.

**Named code items:** [paths_for](../../scripts/build_repository_appendix.py#L116), [symbols](../../scripts/build_repository_appendix.py#L131), [artifact_purpose](../../scripts/build_repository_appendix.py#L145), [describe](../../scripts/build_repository_appendix.py#L206), [link](../../scripts/build_repository_appendix.py#L234), [render_catalog](../../scripts/build_repository_appendix.py#L237), [workflow_svg](../../scripts/build_repository_appendix.py#L261), [check_links](../../scripts/build_repository_appendix.py#L287), [build](../../scripts/build_repository_appendix.py#L312).

### [build_review_figures.py](../../scripts/build_review_figures.py)

Exports detailed alignment atlases and observed-support panels from the selected saved count/point run.

**Named code items:** [build](../../scripts/build_review_figures.py#L20).

### [build_section_mean_figures.py](../../scripts/build_section_mean_figures.py)

Draws current raw-count means/differences with shared linear scales and disclosed display caps.

**Named code items:** [build](../../scripts/build_section_mean_figures.py#L19).

### [build_section_mean_maps.py](../../scripts/build_section_mean_maps.py)

Derives/exports fixed-three means, bin CSVs, NPZ matrices, portable point payload and immutable count-run records.

**Named code items:** [locate_run](../../scripts/build_section_mean_maps.py#L20), [json_array](../../scripts/build_section_mean_maps.py#L29), [build](../../scripts/build_section_mean_maps.py#L36).

### [build_spatial_explorer.py](../../scripts/build_spatial_explorer.py)

Builds the historical portable native supporting app from the native atlas payload.

**Named code items:** [build](../../scripts/build_spatial_explorer.py#L14).

### [comet_alignment_detail.js](../../scripts/comet_alignment_detail.js)

Detailed 2D section placement/review controls using saved transforms and unchanged full PLA locations.

**Named code items:** [inversePoint](../../scripts/comet_alignment_detail.js#L5), [forwardPoint](../../scripts/comet_alignment_detail.js#L12), [binIndex](../../scripts/comet_alignment_detail.js#L16), [nativeTileGrid](../../scripts/comet_alignment_detail.js#L23), [exactTileMesh](../../scripts/comet_alignment_detail.js#L39), [pointCoordinates](../../scripts/comet_alignment_detail.js#L52), [sharedCountRange](../../scripts/comet_alignment_detail.js#L59), [joinRows](../../scripts/comet_alignment_detail.js#L84), [activeCache](../../scripts/comet_alignment_detail.js#L94), [customCounts](../../scripts/comet_alignment_detail.js#L101), [customPoints](../../scripts/comet_alignment_detail.js#L108), [countLimit](../../scripts/comet_alignment_detail.js#L116), [ranges](../../scripts/comet_alignment_detail.js#L120), [axisPair](../../scripts/comet_alignment_detail.js#L142), [heatTrace](../../scripts/comet_alignment_detail.js#L149), [pointTrace](../../scripts/comet_alignment_detail.js#L158), [installWorkspace](../../scripts/comet_alignment_detail.js#L168), [currentEntries](../../scripts/comet_alignment_detail.js#L195), [forwardRect](../../scripts/comet_alignment_detail.js#L196), [localRange](../../scripts/comet_alignment_detail.js#L201), [selectPoint](../../scripts/comet_alignment_detail.js#L208), [renderDetail](../../scripts/comet_alignment_detail.js#L216), [renderAlignmentNow](../../scripts/comet_alignment_detail.js#L248), [detailedAlignment](../../scripts/comet_alignment_detail.js#L302).

### [comet_core_explorer.html](../../scripts/comet_core_explorer.html)

Current browser layout/style and shared view logic; contains payload/module placeholders, not the raw CSVs.

### [comet_detail_grid.js](../../scripts/comet_detail_grid.js)

Rebins full-precision points in a local 100/50/25/10-unit window while retaining full-section share/neighbor context.

**Named code items:** [uniqueBySection](../../scripts/comet_detail_grid.js#L9), [detailGrid](../../scripts/comet_detail_grid.js#L19), [projectedDomain](../../scripts/comet_detail_grid.js#L34), [selectedRecord](../../scripts/comet_detail_grid.js#L46), [calculate](../../scripts/comet_detail_grid.js#L57).

### [comet_measurement_controls.js](../../scripts/comet_measurement_controls.js)

Connects measurement/comparison controls, fixed 8K downloads, persistent footprint, hover tables and fine-detail navigation.

**Named code items:** [observedContextVisible](../../scripts/comet_measurement_controls.js#L11), [observedFootprintTraces](../../scripts/comet_measurement_controls.js#L12), [detailAnalysis](../../scripts/comet_measurement_controls.js#L21), [selectedExportOptions](../../scripts/comet_measurement_controls.js#L29), [exportMeasurementImage](../../scripts/comet_measurement_controls.js#L38), [measurementMeta](../../scripts/comet_measurement_controls.js#L50), [measurementKey](../../scripts/comet_measurement_controls.js#L51), [formatMeasurement](../../scripts/comet_measurement_controls.js#L52), [comparisonLabel](../../scripts/comet_measurement_controls.js#L53), [metricUnits](../../scripts/comet_measurement_controls.js#L54), [intensiveMeasurement](../../scripts/comet_measurement_controls.js#L55), [measurementFeaturesAvailable](../../scripts/comet_measurement_controls.js#L56), [measurementResult](../../scripts/comet_measurement_controls.js#L57), [metricSectionMap](../../scripts/comet_measurement_controls.js#L64), [metricSectionValues](../../scripts/comet_measurement_controls.js#L65), [validMetricN](../../scripts/comet_measurement_controls.js#L66), [metricDomainMatrix](../../scripts/comet_measurement_controls.js#L67), [shownMetricMatrix](../../scripts/comet_measurement_controls.js#L68), [contribution](../../scripts/comet_measurement_controls.js#L69), [hoverMatrix](../../scripts/comet_measurement_controls.js#L73), [applyMeasurementText](../../scripts/comet_measurement_controls.js#L84), [resetMeasurementRange](../../scripts/comet_measurement_controls.js#L105), [refreshMeasurementSelection](../../scripts/comet_measurement_controls.js#L111), [initializeMeasurements](../../scripts/comet_measurement_controls.js#L116), [renderMeasurementDifferences](../../scripts/comet_measurement_controls.js#L128), [downloadMeasurementTable](../../scripts/comet_measurement_controls.js#L148).

### [comet_measurements.js](../../scripts/comet_measurements.js)

Browser counterpart of the nineteen Python measurements; computes the same statistics from embedded point/attribute caches.

**Named code items:** [binIndex](../../scripts/comet_measurements.js#L32), [rows](../../scripts/comet_measurements.js#L37), [objectRows](../../scripts/comet_measurements.js#L38), [quantile](../../scripts/comet_measurements.js#L39), [compareConditions](../../scripts/comet_measurements.js#L40), [select](../../scripts/comet_measurements.js#L53), [validateGrid](../../scripts/comet_measurements.js#L54), [prepare](../../scripts/comet_measurements.js#L55), [sectionValues](../../scripts/comet_measurements.js#L73), [calculate](../../scripts/comet_measurements.js#L113).

### [comet_plot_lifecycle.js](../../scripts/comet_plot_lifecycle.js)

Initializes hidden plots at real dimensions, decodes previews, manages plot resources and reports startup readiness.

**Named code items:** [createPlotLifecycle](../../scripts/comet_plot_lifecycle.js#L5), [track](../../scripts/comet_plot_lifecycle.js#L15), [status](../../scripts/comet_plot_lifecycle.js#L16), [mainWidth](../../scripts/comet_plot_lifecycle.js#L17), [withPanel](../../scripts/comet_plot_lifecycle.js#L18), [dimensions](../../scripts/comet_plot_lifecycle.js#L27), [axisRanges](../../scripts/comet_plot_lifecycle.js#L28), [saveEvents](../../scripts/comet_plot_lifecycle.js#L29), [fit](../../scripts/comet_plot_lifecycle.js#L33), [record](../../scripts/comet_plot_lifecycle.js#L37), [render](../../scripts/comet_plot_lifecycle.js#L38), [removePreview](../../scripts/comet_plot_lifecycle.js#L45), [purge](../../scripts/comet_plot_lifecycle.js#L46), [purgeTree](../../scripts/comet_plot_lifecycle.js#L47), [suspend](../../scripts/comet_plot_lifecycle.js#L48), [hydrate](../../scripts/comet_plot_lifecycle.js#L55), [whenIdle](../../scripts/comet_plot_lifecycle.js#L60), [imagesReady](../../scripts/comet_plot_lifecycle.js#L61), [activate](../../scripts/comet_plot_lifecycle.js#L62), [boot](../../scripts/comet_plot_lifecycle.js#L66), [install](../../scripts/comet_plot_lifecycle.js#L76).

### [comet_support_detail.js](../../scripts/comet_support_detail.js)

Linked observed-support maps, baseline section counts and full point details; support remains independent of the selected metric.

**Named code items:** [sections](../../scripts/comet_support_detail.js#L13), [nMatrix](../../scripts/comet_support_detail.js#L14), [sourcePoints](../../scripts/comet_support_detail.js#L15), [matrixMembership](../../scripts/comet_support_detail.js#L16), [ensureWorkspace](../../scripts/comet_support_detail.js#L23), [setWindow](../../scripts/comet_support_detail.js#L60), [setBinAtCentre](../../scripts/comet_support_detail.js#L61), [windowShape](../../scripts/comet_support_detail.js#L62), [mapLayout](../../scripts/comet_support_detail.js#L63), [bindOverview](../../scripts/comet_support_detail.js#L64), [renderOverview](../../scripts/comet_support_detail.js#L69), [populateSectionOptions](../../scripts/comet_support_detail.js#L77), [pointsInWindow](../../scripts/comet_support_detail.js#L78), [crop](../../scripts/comet_support_detail.js#L83), [countMaximum](../../scripts/comet_support_detail.js#L85), [gridShapes](../../scripts/comet_support_detail.js#L86), [renderDetail](../../scripts/comet_support_detail.js#L87), [highlight](../../scripts/comet_support_detail.js#L103), [render](../../scripts/comet_support_detail.js#L104).

### [comet_vector_export.js](../../scripts/comet_vector_export.js)

Writes exact tile/outline SVG and rasterizes it for PNG downloads; the UI fixes PNG width to 8,000 pixels.

**Named code items:** [color](../../scripts/comet_vector_export.js#L7), [svg](../../scripts/comet_vector_export.js#L14), [download](../../scripts/comet_vector_export.js#L74).

### [configure_local_inputs.py](../../scripts/configure_local_inputs.py)

Relocates raw source paths only after checking thirteen hashes, twelve selected sections and the interrupted-run exclusion.

**Named code items:** [digest](../../scripts/configure_local_inputs.py#L20), [configure](../../scripts/configure_local_inputs.py#L28), [main](../../scripts/configure_local_inputs.py#L111).

### [execute_notebook.py](../../scripts/execute_notebook.py)

Executes notebook cells with its Python environment and atomically saves only successfully validated outputs.

**Named code items:** [main](../../scripts/execute_notebook.py#L17).

### [extract_alignment_snapshot.py](../../scripts/extract_alignment_snapshot.py)

Extracts frozen placement parameters from the former app with source hashes and section/source relationships.

**Named code items:** [sha256](../../scripts/extract_alignment_snapshot.py#L22), [asset](../../scripts/extract_alignment_snapshot.py#L30), [extract](../../scripts/extract_alignment_snapshot.py#L34), [main](../../scripts/extract_alignment_snapshot.py#L140).

### [inventory_data.py](../../scripts/inventory_data.py)

Profiles the original intake files, measurement columns and duplicates; records observation separately from scientific assignment.

**Named code items:** [sha256](../../scripts/inventory_data.py#L38), [write_csv](../../scripts/inventory_data.py#L46), [write_json](../../scripts/inventory_data.py#L56), [signature](../../scripts/inventory_data.py#L61), [empty_profile](../../scripts/inventory_data.py#L71), [profile_value](../../scripts/inventory_data.py#L78), [infer_type](../../scripts/inventory_data.py#L104), [audit_csv](../../scripts/inventory_data.py#L116), [dictionary_entry](../../scripts/inventory_data.py#L198), [main](../../scripts/inventory_data.py#L226).

### [refresh_review_notebook.py](../../scripts/refresh_review_notebook.py)

Historical notebook review-section insertion/refresh helper; its older headings are not a general modern notebook rebuild.

**Named code items:** [main](../../scripts/refresh_review_notebook.py#L19).

### [reproduce_alignment_check.py](../../scripts/reproduce_alignment_check.py)

Reproduces the saved alignment-check image and records pixel/hash/transform comparisons.

**Named code items:** [sha](../../scripts/reproduce_alignment_check.py#L25), [build](../../scripts/reproduce_alignment_check.py#L29).

### [run_analysis.py](../../scripts/run_analysis.py)

Strict tissue-mask pipeline runner; validates its inputs before producing mask-valid section means and contrasts.

**Named code items:** [save_json](../../scripts/run_analysis.py#L36), [asset_path](../../scripts/run_analysis.py#L43), [display_directions](../../scripts/run_analysis.py#L48), [read_objects](../../scripts/run_analysis.py#L53), [load_existing_mask](../../scripts/run_analysis.py#L95), [write_objects](../../scripts/run_analysis.py#L115), [orient_axes](../../scripts/run_analysis.py#L124), [export_figures](../../scripts/run_analysis.py#L136), [save_matrices](../../scripts/run_analysis.py#L206), [execute](../../scripts/run_analysis.py#L226), [main](../../scripts/run_analysis.py#L321).

### [run_exploratory_maps.py](../../scripts/run_exploratory_maps.py)

CLI for authorized exploratory counting from selected raw CSVs, without inventing tissue coverage.

**Named code items:** [main](../../scripts/run_exploratory_maps.py#L12).

### [serve_app.py](../../scripts/serve_app.py)

Optional standard-library localhost-only server. Serves only outputs/app; does not rerun analysis or serve raw inputs.

**Named code items:** [app_directory](../../scripts/serve_app.py#L21), [AppRequestHandler](../../scripts/serve_app.py#L35), [AppRequestHandler.send_head](../../scripts/serve_app.py#L38), [AppRequestHandler.list_directory](../../scripts/serve_app.py#L51), [port_number](../../scripts/serve_app.py#L56), [main](../../scripts/serve_app.py#L66).

### [spatial_explorer.html](../../scripts/spatial_explorer.html)

Historical native-atlas browser template; its sampled point display and eight-export scope differ from the current app.

### [validate_measurement_engines.py](../../scripts/validate_measurement_engines.py)

Checks complete real-data Python/JavaScript arrays, finite masks, original count results and unchanged geometry.

**Named code items:** [digest](../../scripts/validate_measurement_engines.py#L24), [selected_path](../../scripts/validate_measurement_engines.py#L32), [geometry_digest](../../scripts/validate_measurement_engines.py#L42), [validate](../../scripts/validate_measurement_engines.py#L91).

## `tests`

### [test_alignment_detail.py](../../tests/test_alignment_detail.py)

Regression checks for alignment detail. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [AlignmentDetailAcceptanceTests](../../tests/test_alignment_detail.py#L14), [AlignmentDetailAcceptanceTests.evaluate](../../tests/test_alignment_detail.py#L15), [AlignmentDetailAcceptanceTests.test_native_reflection_reorders_rectangles_counts_and_support_exactly](../../tests/test_alignment_detail.py#L21), [AlignmentDetailAcceptanceTests.test_three_dimensional_tiles_are_constant_count_faces_and_leave_gaps](../../tests/test_alignment_detail.py#L39), [AlignmentDetailAcceptanceTests.test_numeric_boundary_membership_is_single_and_outer_maximum_included](../../tests/test_alignment_detail.py#L54), [AlignmentDetailAcceptanceTests.test_native_points_use_every_stored_raw_coordinate_without_sampling](../../tests/test_alignment_detail.py#L58), [AlignmentDetailAcceptanceTests.test_rotated_native_bins_are_not_replaced_by_approximate_rectangles](../../tests/test_alignment_detail.py#L67), [AlignmentDetailAcceptanceTests.test_no_app_or_multiresolution_does_not_require_dom_or_change_saved_renderer](../../tests/test_alignment_detail.py#L77), [AlignmentDetailAcceptanceTests.test_shared_count_range_includes_larger_other_arm_and_preserves_values](../../tests/test_alignment_detail.py#L81).

### [test_configure_local_inputs.py](../../tests/test_configure_local_inputs.py)

Regression checks for configure local inputs. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [ConfigureLocalInputsTests](../../tests/test_configure_local_inputs.py#L12), [ConfigureLocalInputsTests.fixture](../../tests/test_configure_local_inputs.py#L13), [ConfigureLocalInputsTests.without_paths](../../tests/test_configure_local_inputs.py#L52), [ConfigureLocalInputsTests.test_default_folder_relocates_all_thirteen_hash_verified_sources_only](../../tests/test_configure_local_inputs.py#L60), [ConfigureLocalInputsTests.test_explicit_data_directory_and_check_only_leave_manifest_byte_identical](../../tests/test_configure_local_inputs.py#L75), [ConfigureLocalInputsTests.test_interrupted_export_hash_mismatch_aborts_without_partial_manifest_write](../../tests/test_configure_local_inputs.py#L87), [ConfigureLocalInputsTests.test_missing_completed_export_aborts_without_changing_paths](../../tests/test_configure_local_inputs.py#L97), [ConfigureLocalInputsTests.test_changed_cohort_authority_is_rejected_before_relocation](../../tests/test_configure_local_inputs.py#L106).

### [test_core_explorer_build.py](../../tests/test_core_explorer_build.py)

Regression checks for core explorer build. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [CoreExplorerBuildTests](../../tests/test_core_explorer_build.py#L17), [CoreExplorerBuildTests.fixture](../../tests/test_core_explorer_build.py#L18), [CoreExplorerBuildTests.test_missing_core_stays_blocked_and_reference_pixels_are_embedded](../../tests/test_core_explorer_build.py#L32), [CoreExplorerBuildTests.test_identical_replay_is_verified_without_embedding_duplicate_pixels](../../tests/test_core_explorer_build.py#L46), [CoreExplorerBuildTests.test_fresh_clone_embeds_local_reference_when_original_machine_is_unavailable](../../tests/test_core_explorer_build.py#L64), [CoreExplorerBuildTests.test_changed_local_reference_is_rejected_even_when_original_pixels_are_available](../../tests/test_core_explorer_build.py#L75), [CoreExplorerBuildTests.exploratory_fixture](../../tests/test_core_explorer_build.py#L85), [CoreExplorerBuildTests.test_exploratory_payload_remains_separate_from_blocked_strict_results](../../tests/test_core_explorer_build.py#L96), [CoreExplorerBuildTests.test_portable_copy_loads_local_run_when_recorded_absolute_location_is_gone](../../tests/test_core_explorer_build.py#L108), [CoreExplorerBuildTests.test_exploratory_payload_cannot_claim_to_be_strict_pdf_result](../../tests/test_core_explorer_build.py#L130), [CoreExplorerBuildTests.test_mode_bootstrap_targets_exist_in_real_initial_html_or_earlier_markup](../../tests/test_core_explorer_build.py#L137), [CoreExplorerBuildTests.multiresolution_fixture](../../tests/test_core_explorer_build.py#L168), [CoreExplorerBuildTests.test_multiresolution_loader_preserves_complete_points_and_uses_portable_run](../../tests/test_core_explorer_build.py#L184), [CoreExplorerBuildTests.test_current_maps_report_ready_without_historical_exploratory_run](../../tests/test_core_explorer_build.py#L196), [CoreExplorerBuildTests.test_multiresolution_loader_rejects_failed_validation_and_incomplete_points](../../tests/test_core_explorer_build.py#L209), [CoreExplorerBuildTests.test_support_module_dom_targets_and_namespace_match_real_markup](../../tests/test_core_explorer_build.py#L231), [CoreExplorerBuildTests.test_plot_lifecycle_measures_hidden_views_refits_and_releases_contexts](../../tests/test_core_explorer_build.py#L258), [CoreExplorerBuildTests.test_lifecycle_is_installed_before_core_initializes_and_has_accessible_status](../../tests/test_core_explorer_build.py#L327), [CoreExplorerBuildTests.test_shared_display_range_preserves_values_and_compares_both_condition_means](../../tests/test_core_explorer_build.py#L347), [CoreExplorerBuildTests.test_changed_saved_reference_pixels_are_rejected](../../tests/test_core_explorer_build.py#L378).

### [test_core_view.py](../../tests/test_core_view.py)

Regression checks for core view. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [CoreViewAcceptanceTests](../../tests/test_core_view.py#L20), [CoreViewAcceptanceTests.setUp](../../tests/test_core_view.py#L21), [CoreViewAcceptanceTests.tearDown](../../tests/test_core_view.py#L95), [CoreViewAcceptanceTests.write_json](../../tests/test_core_view.py#L99), [CoreViewAcceptanceTests.write_snapshot](../../tests/test_core_view.py#L102), [CoreViewAcceptanceTests.save_summary](../../tests/test_core_view.py#L107), [CoreViewAcceptanceTests.test_no_run_has_no_default_scientific_arrays](../../tests/test_core_view.py#L114), [CoreViewAcceptanceTests.test_current_blocked_preflight_prevents_stale_run_display](../../tests/test_core_view.py#L122), [CoreViewAcceptanceTests.test_verified_numerics_preserve_zero_shared_grid_scale_and_pending_alignment](../../tests/test_core_view.py#L127), [CoreViewAcceptanceTests.test_matrix_tampering_is_not_presented_as_a_result](../../tests/test_core_view.py#L148), [CoreViewAcceptanceTests.test_changed_fixed_transform_is_detected_from_saved_coordinates](../../tests/test_core_view.py#L159), [CoreViewAcceptanceTests.test_missing_saved_outline_disables_alignment_without_filling_missing_geometry](../../tests/test_core_view.py#L167), [CoreViewAcceptanceTests.test_mask_artifact_hash_change_is_an_integrity_failure](../../tests/test_core_view.py#L178), [CoreViewAcceptanceTests.test_section_contributions_are_exact_valid_zero_counts](../../tests/test_core_view.py#L184), [CoreViewAcceptanceTests.test_missing_opposite_condition_is_null_and_not_a_true_zero](../../tests/test_core_view.py#L191).

### [test_detail_grid.py](../../tests/test_detail_grid.py)

Regression checks for detail grid. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [fixture](../../tests/test_detail_grid.py#L12), [ExactDetailGridTests](../../tests/test_detail_grid.py#L57), [ExactDetailGridTests.run_helper](../../tests/test_detail_grid.py#L58), [ExactDetailGridTests.calculated](../../tests/test_detail_grid.py#L67), [ExactDetailGridTests.test_exact_source_rebinning_keeps_boundary_points_and_three_animal_weights](../../tests/test_detail_grid.py#L73), [ExactDetailGridTests.test_section_share_uses_full_section_total_including_objects_outside_detail](../../tests/test_detail_grid.py#L88), [ExactDetailGridTests.test_cached_full_section_neighbor_distances_are_sliced_not_recomputed](../../tests/test_detail_grid.py#L97), [ExactDetailGridTests.test_marker_flags_and_areas_keep_source_order_after_nonprefix_selection](../../tests/test_detail_grid.py#L107), [ExactDetailGridTests.test_regular_grid_covers_requested_window_and_counts_its_entire_extent](../../tests/test_detail_grid.py#L116), [ExactDetailGridTests.test_domain_projects_baseline_centers_and_does_not_fill_undefined_metrics](../../tests/test_detail_grid.py#L128), [ExactDetailGridTests.test_large_grid_invalid_window_and_misaligned_features_are_rejected](../../tests/test_detail_grid.py#L139).

### [test_exploratory.py](../../tests/test_exploratory.py)

Regression checks for exploratory. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [grid](../../tests/test_exploratory.py#L16), [section](../../tests/test_exploratory.py#L20), [ExploratoryAcceptanceTests](../../tests/test_exploratory.py#L26), [ExploratoryAcceptanceTests.test_chat_only_zero_increases_support_but_empty_bin_stays_missing](../../tests/test_exploratory.py#L27), [ExploratoryAcceptanceTests.test_equal_section_means_pdf_arithmetic_and_arms_separate](../../tests/test_exploratory.py#L37), [ExploratoryAcceptanceTests.test_repeated_physical_section_rejected](../../tests/test_exploratory.py#L47), [ExploratoryAcceptanceTests.source_case](../../tests/test_exploratory.py#L54), [ExploratoryAcceptanceTests.test_fixed_transform_midpoints_all_counts_and_pla_row_provenance](../../tests/test_exploratory.py#L75), [ExploratoryAcceptanceTests.test_unknown_object_class_fails](../../tests/test_exploratory.py#L92), [ExploratoryAcceptanceTests.test_reversed_and_nonfinite_boxes_fail](../../tests/test_exploratory.py#L96), [ExploratoryAcceptanceTests.test_duplicate_id_across_known_classes_fails](../../tests/test_exploratory.py#L102), [ExploratoryAcceptanceTests.test_source_hash_mismatch_fails_before_counting](../../tests/test_exploratory.py#L106).

### [test_explorer_payload.py](../../tests/test_explorer_payload.py)

Regression checks for explorer payload. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [ExplorerAssemblyTests](../../tests/test_explorer_payload.py#L13), [ExplorerAssemblyTests.test_saved_html_carries_data_and_historical_image_without_script_injection](../../tests/test_explorer_payload.py#L14), [ExplorerAssemblyTests.test_supporting_navigation_resolves_to_existing_project_files](../../tests/test_explorer_payload.py#L46).

### [test_inventory.py](../../tests/test_inventory.py)

Regression checks for inventory. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [InventoryTests](../../tests/test_inventory.py#L11), [InventoryTests.setUp](../../tests/test_inventory.py#L12), [InventoryTests.write_fixture](../../tests/test_inventory.py#L26), [InventoryTests.test_bom_and_quoted_fields_preserve_exported_text](../../tests/test_inventory.py#L34), [InventoryTests.test_malformed_rows_are_counted_without_entering_measurement_profiles](../../tests/test_inventory.py#L46), [InventoryTests.test_missing_nonfinite_and_reversed_boxes_remain_auditable](../../tests/test_inventory.py#L55), [InventoryTests.test_repeat_rows_keep_multiplicity_while_region_and_id_exclusions_are_explicit](../../tests/test_inventory.py#L70), [InventoryTests.test_hash_and_audit_do_not_modify_source_bytes_or_mtime](../../tests/test_inventory.py#L90).

### [test_manifest.py](../../tests/test_manifest.py)

Regression checks for manifest. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [ManifestAcceptanceTests](../../tests/test_manifest.py#L14), [ManifestAcceptanceTests.setUp](../../tests/test_manifest.py#L15), [ManifestAcceptanceTests.tearDown](../../tests/test_manifest.py#L53), [ManifestAcceptanceTests.asset](../../tests/test_manifest.py#L56), [ManifestAcceptanceTests.report](../../tests/test_manifest.py#L59), [ManifestAcceptanceTests.test_complete_signed_manifest_can_pass](../../tests/test_manifest.py#L62), [ManifestAcceptanceTests.test_empty_template_is_honestly_blocked](../../tests/test_manifest.py#L65), [ManifestAcceptanceTests.test_unconfirmed_relationships_are_not_inferred](../../tests/test_manifest.py#L71), [ManifestAcceptanceTests.test_absent_accepted_transform_and_alignment_reference_block](../../tests/test_manifest.py#L75), [ManifestAcceptanceTests.test_changed_input_hash_blocks](../../tests/test_manifest.py#L83), [ManifestAcceptanceTests.test_missing_mask_and_centroid_definition_block](../../tests/test_manifest.py#L87), [ManifestAcceptanceTests.test_unapproved_bounding_box_proxy_blocks](../../tests/test_manifest.py#L94), [ManifestAcceptanceTests.test_approved_proxy_still_needs_hashed_amendment](../../tests/test_manifest.py#L98), [ManifestAcceptanceTests.test_coordinate_unit_mismatch_blocks](../../tests/test_manifest.py#L102), [ManifestAcceptanceTests.test_reference_space_mismatch_blocks](../../tests/test_manifest.py#L106), [ManifestAcceptanceTests.test_anatomical_terms_without_explicit_display_direction_block](../../tests/test_manifest.py#L110), [ManifestAcceptanceTests.test_explicit_display_direction_does_not_guess_from_anatomy](../../tests/test_manifest.py#L114), [ManifestAcceptanceTests.test_literal_legacy_display_directions_are_unambiguous](../../tests/test_manifest.py#L120), [ManifestAcceptanceTests.test_invalid_explicit_display_direction_blocks_despite_literal_fallback](../../tests/test_manifest.py#L125), [ManifestAcceptanceTests.test_pla_object_declaration_is_required_even_for_all_rows](../../tests/test_manifest.py#L130), [ManifestAcceptanceTests.test_mixed_source_requires_class_column_and_exact_pla_labels](../../tests/test_manifest.py#L134), [ManifestAcceptanceTests.test_mixed_source_exact_class_definition_passes_metadata_only](../../tests/test_manifest.py#L141), [ManifestAcceptanceTests.test_pla_class_values_cannot_be_coerced_from_numbers](../../tests/test_manifest.py#L147), [ManifestAcceptanceTests.test_repeated_source_selection_blocks](../../tests/test_manifest.py#L153), [ManifestAcceptanceTests.test_included_superseded_source_blocks](../../tests/test_manifest.py#L159), [ManifestAcceptanceTests.test_overlapping_selectors_on_consolidated_source_block](../../tests/test_manifest.py#L163), [ManifestAcceptanceTests.test_disjoint_selectors_on_consolidated_source_are_allowed](../../tests/test_manifest.py#L170), [ManifestAcceptanceTests.test_malformed_or_missing_manifest_returns_blocker](../../tests/test_manifest.py#L179).

### [test_measurement_features.py](../../tests/test_measurement_features.py)

Regression checks for measurement features. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [MeasurementFeatureTests](../../tests/test_measurement_features.py#L13), [MeasurementFeatureTests.fixture](../../tests/test_measurement_features.py#L14), [MeasurementFeatureTests.test_full_precision_attributes_preserve_identity_order_and_reflection](../../tests/test_measurement_features.py#L29), [MeasurementFeatureTests.test_same_length_reordered_objects_and_changed_coordinates_are_rejected](../../tests/test_measurement_features.py#L41), [MeasurementFeatureTests.test_changed_raw_source_is_rejected_before_attributes_are_reused](../../tests/test_measurement_features.py#L49), [MeasurementFeatureTests.test_portable_cache_rejects_corrupt_bytes_and_identity_vector](../../tests/test_measurement_features.py#L54), [MeasurementFeatureTests.test_nearest_neighbors_are_exact_same_section_distances_without_point_mutation](../../tests/test_measurement_features.py#L70), [MeasurementFeatureTests.test_duplicate_positions_keep_zero_spacing_and_singletons_are_undefined](../../tests/test_measurement_features.py#L79), [MeasurementFeatureTests.test_optional_spacing_vector_is_validated_when_present_and_old_cache_stays_readable](../../tests/test_measurement_features.py#L86).

### [test_measurement_ui.py](../../tests/test_measurement_ui.py)

Regression checks for measurement ui. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [MeasurementUiTests](../../tests/test_measurement_ui.py#L38), [MeasurementUiTests.run_node](../../tests/test_measurement_ui.py#L39), [MeasurementUiTests.test_primary_mean_retains_defined_condition_when_comparison_is_undefined](../../tests/test_measurement_ui.py#L49), [MeasurementUiTests.test_selection_changes_do_not_reuse_stale_statistics_or_coerce_undefined_to_zero](../../tests/test_measurement_ui.py#L64), [MeasurementUiTests.test_missing_feature_cache_preserves_baseline_but_rejects_other_measurements](../../tests/test_measurement_ui.py#L79), [MeasurementUiTests.test_selected_csv_includes_units_valid_n_raw_support_and_missing_reason](../../tests/test_measurement_ui.py#L89), [MeasurementUiTests.test_actual_controls_cover_pdf_functions_and_bootstrap_engine_before_views](../../tests/test_measurement_ui.py#L113), [MeasurementUiTests.test_footprint_is_metric_independent_vector_boundary_and_does_not_fill_missing_values](../../tests/test_measurement_ui.py#L145), [MeasurementUiTests.test_catalog_drives_all_nineteen_controls_and_section_share_uses_percentage_points](../../tests/test_measurement_ui.py#L160), [MeasurementUiTests.test_detail_rebin_is_bounded_cached_and_exports_its_actual_grid_and_provenance](../../tests/test_measurement_ui.py#L177), [MeasurementUiTests.test_export_uses_explicit_eight_k_width_reports_errors_and_prevents_parallel_allocations](../../tests/test_measurement_ui.py#L197).

### [test_measurements.py](../../tests/test_measurements.py)

Regression checks for measurements. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [fixture](../../tests/test_measurements.py#L18), [clean](../../tests/test_measurements.py#L62), [MeasurementArithmeticTests](../../tests/test_measurements.py#L76), [MeasurementArithmeticTests.test_all_nineteen_section_measurements_from_hand_calculated_objects](../../tests/test_measurements.py#L77), [MeasurementArithmeticTests.test_section_weighting_does_not_pool_objects_or_replace_missing_means_with_zero](../../tests/test_measurements.py#L94), [MeasurementArithmeticTests.test_empty_bin_counts_and_sums_zero_but_fractions_and_intensives_undefined](../../tests/test_measurements.py#L108), [MeasurementArithmeticTests.test_cutoff_boundary_is_inclusive_and_configurable](../../tests/test_measurements.py#L124), [MeasurementArithmeticTests.test_comparisons_follow_condition_means_and_mask_zeros_without_pseudocounts](../../tests/test_measurements.py#L138), [MeasurementArithmeticTests.test_invalid_features_contaminate_only_relevant_metric_bins](../../tests/test_measurements.py#L154), [MeasurementArithmeticTests.test_arms_eligibility_and_inputs_stay_separate_and_unchanged](../../tests/test_measurements.py#L168), [MeasurementArithmeticTests.test_misaligned_points_feature_lengths_hashes_and_duplicate_specimens_are_rejected](../../tests/test_measurements.py#L180), [MeasurementArithmeticTests.test_section_share_uses_its_own_full_section_total_and_keeps_zero_total_missing](../../tests/test_measurements.py#L191), [MeasurementArithmeticTests.test_marker_area_fraction_is_area_weighted_and_unknown_denominators_stay_missing](../../tests/test_measurements.py#L211), [MeasurementArithmeticTests.test_median_intensity_and_iqr_use_within_section_type7_quantiles](../../tests/test_measurements.py#L224), [MeasurementArithmeticTests.test_area_cv_is_population_requires_two_positive_mean_and_is_numerically_stable](../../tests/test_measurements.py#L237), [MeasurementArithmeticTests.test_nearest_neighbor_uses_precomputed_full_section_values_and_accepts_duplicate_zeros](../../tests/test_measurements.py#L251), [BrowserMeasurementParityTests](../../tests/test_measurements.py#L267), [BrowserMeasurementParityTests.test_every_measurement_comparison_and_edge_case_matches_python](../../tests/test_measurements.py#L268), [BrowserMeasurementParityTests.test_browser_helpers_cover_boundary_and_zero_log_cases](../../tests/test_measurements.py#L292).

### [test_multiresolution_maps.py](../../tests/test_multiresolution_maps.py)

Regression checks for multiresolution maps. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [reference_grid](../../tests/test_multiresolution_maps.py#L16), [MultiresolutionAcceptanceTests](../../tests/test_multiresolution_maps.py#L20), [MultiresolutionAcceptanceTests.test_raw_boundaries_refine_exactly_to_every_requested_grid](../../tests/test_multiresolution_maps.py#L21), [MultiresolutionAcceptanceTests.test_aggregation_rejects_partial_or_noninteger_factors](../../tests/test_multiresolution_maps.py#L36), [MultiresolutionAcceptanceTests.make_case](../../tests/test_multiresolution_maps.py#L44), [MultiresolutionAcceptanceTests.test_fresh_run_preserves_all_points_and_recomputes_finer_support](../../tests/test_multiresolution_maps.py#L73), [MultiresolutionAcceptanceTests.test_hash_failure_leaves_no_published_payload](../../tests/test_multiresolution_maps.py#L109).

### [test_native_atlas.py](../../tests/test_native_atlas.py)

Regression checks for native atlas. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [NativeAtlasTests](../../tests/test_native_atlas.py#L11), [NativeAtlasTests.frame](../../tests/test_native_atlas.py#L12), [NativeAtlasTests.payload](../../tests/test_native_atlas.py#L21), [NativeAtlasTests.test_all_source_rows_conserved_for_each_class_and_width](../../tests/test_native_atlas.py#L25), [NativeAtlasTests.test_internal_edges_and_outer_max_are_counted_once](../../tests/test_native_atlas.py#L34), [NativeAtlasTests.test_class_balanced_samples_are_reproducible_unique_and_bounded](../../tests/test_native_atlas.py#L40), [NativeAtlasTests.test_bad_boxes_and_repeated_object_ids_fail_without_silent_drop](../../tests/test_native_atlas.py#L47), [NativeAtlasTests.test_zero_diameter_exclusion_affects_ratio_only](../../tests/test_native_atlas.py#L55), [NativeAtlasTests.test_native_extent_is_full_envelope_and_never_supplies_anatomy](../../tests/test_native_atlas.py#L64), [NativeAtlasTests.test_selected_flag_extremes_require_recorded_full_count_support](../../tests/test_native_atlas.py#L73), [NativeAtlasTests.test_morphology_review_uses_full_source_records_and_keeps_count_denominator](../../tests/test_native_atlas.py#L82).

### [test_run_analysis.py](../../tests/test_run_analysis.py)

Regression checks for run analysis. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [PortableFullRunAcceptanceTests](../../tests/test_run_analysis.py#L30), [PortableFullRunAcceptanceTests.test_real_runner_saves_geometry_and_self_contained_exact_core_views](../../tests/test_run_analysis.py#L31).

### [test_runner.py](../../tests/test_runner.py)

Regression checks for runner. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [RunnerIntegrationTests](../../tests/test_runner.py#L20), [RunnerIntegrationTests.setUp](../../tests/test_runner.py#L21), [RunnerIntegrationTests.tearDown](../../tests/test_runner.py#L75), [RunnerIntegrationTests.asset](../../tests/test_runner.py#L78), [RunnerIntegrationTests.run_cli](../../tests/test_runner.py#L81), [RunnerIntegrationTests.test_blocked_manifest_saves_blockers_and_no_maps](../../tests/test_runner.py#L89), [RunnerIntegrationTests.test_ready_preflight_does_not_run_analysis](../../tests/test_runner.py#L95), [RunnerIntegrationTests.test_full_run_saves_correct_separate_counts_shared_limits_and_pending_review](../../tests/test_runner.py#L100), [RunnerIntegrationTests.test_mixed_object_rows_are_not_silently_counted_as_pla](../../tests/test_runner.py#L128), [RunnerIntegrationTests.test_partial_mask_remains_invalid_while_valid_empty_bins_stay_zero](../../tests/test_runner.py#L135).

### [test_section_mean_build.py](../../tests/test_section_mean_build.py)

Regression checks for section mean build. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [json_matrix](../../tests/test_section_mean_build.py#L21), [SectionMeanBuildAcceptanceTests](../../tests/test_section_mean_build.py#L28), [SectionMeanBuildAcceptanceTests.fixture](../../tests/test_section_mean_build.py#L29), [SectionMeanBuildAcceptanceTests.test_fixed_three_zero_condition_and_immutable_points_transforms_and_history](../../tests/test_section_mean_build.py#L103), [SectionMeanBuildAcceptanceTests.test_derived_latest_pointer_resolves_portably](../../tests/test_section_mean_build.py#L162), [SectionMeanBuildAcceptanceTests.test_all_zero_differences_keep_nonzero_colour_range](../../tests/test_section_mean_build.py#L173), [SectionMeanBuildAcceptanceTests.test_empty_arm_stays_blank_with_explicit_zero_arithmetic_and_null_stats](../../tests/test_section_mean_build.py#L184), [SectionMeanBuildAcceptanceTests.test_incomplete_cached_source_validation_cannot_publish_derived_run](../../tests/test_section_mean_build.py#L197).

### [test_section_means.py](../../tests/test_section_means.py)

Regression checks for section means. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [fixture](../../tests/test_section_means.py#L9), [FixedSectionMeansTests](../../tests/test_section_means.py#L22), [FixedSectionMeansTests.test_three_section_arithmetic_and_explicit_coverage_flags](../../tests/test_section_means.py#L23), [FixedSectionMeansTests.test_all_empty_bins_are_assumed_zero_but_outside_union_display_domain](../../tests/test_section_means.py#L34), [FixedSectionMeansTests.test_missing_policy_keeps_denominator_three_without_available_subset_reweighting](../../tests/test_section_means.py#L44), [FixedSectionMeansTests.test_condition_with_no_objects_can_compare_only_under_explicit_zero_policy](../../tests/test_section_means.py#L58), [FixedSectionMeansTests.test_arms_remain_separate_and_repeated_sections_or_animals_rejected](../../tests/test_section_means.py#L70), [FixedSectionMeansTests.test_explicit_policy_and_exact_three_sections_required](../../tests/test_section_means.py#L82).

### [test_serve_app.py](../../tests/test_serve_app.py)

Regression checks for serve app. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [AppLauncherTests](../../tests/test_serve_app.py#L14), [AppLauncherTests.saved_app](../../tests/test_serve_app.py#L15), [AppLauncherTests.test_saved_app_is_found_without_analysis_inputs](../../tests/test_serve_app.py#L21), [AppLauncherTests.test_missing_saved_app_explains_how_to_get_it_without_starting_server](../../tests/test_serve_app.py#L26), [AppLauncherTests.test_symlink_cannot_serve_a_raw_file_outside_the_app](../../tests/test_serve_app.py#L35), [AppLauncherTests.test_directory_index_cannot_bypass_symlink_check](../../tests/test_serve_app.py#L48), [AppLauncherTests.test_server_binds_only_loopback_and_port_conflict_is_actionable](../../tests/test_serve_app.py#L62).

### [test_spatial_context_export.py](../../tests/test_spatial_context_export.py)

Regression checks for spatial context export. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [ring](../../tests/test_spatial_context_export.py#L19), [segments](../../tests/test_spatial_context_export.py#L23), [DetectedObjectContextTests](../../tests/test_spatial_context_export.py#L28), [DetectedObjectContextTests.test_exact_nonuniform_edges_preserve_inner_hole_and_do_not_mutate_inputs](../../tests/test_spatial_context_export.py#L29), [DetectedObjectContextTests.test_disconnected_components_keep_their_gap_and_empty_context_stays_empty](../../tests/test_spatial_context_export.py#L41), [DetectedObjectContextTests.test_context_source_fingerprint_ignores_selected_metric_values_and_uses_finest_grid](../../tests/test_spatial_context_export.py#L52), [DetectedObjectContextTests.test_context_rejects_mismatched_or_nonincreasing_geometry](../../tests/test_spatial_context_export.py#L68), [VectorExportTests](../../tests/test_spatial_context_export.py#L76), [VectorExportTests.export](../../tests/test_spatial_context_export.py#L77), [VectorExportTests.options](../../tests/test_spatial_context_export.py#L82), [VectorExportTests.test_svg_is_real_vector_with_exact_finite_tile_count_zero_values_and_safe_text](../../tests/test_spatial_context_export.py#L90), [VectorExportTests.test_all_undefined_metric_still_draws_context_without_filling_its_hole](../../tests/test_spatial_context_export.py#L106), [VectorExportTests.test_context_can_be_hidden_without_changing_numerical_tiles](../../tests/test_spatial_context_export.py#L123), [VectorExportTests.test_color_clamps_only_display_endpoints_and_rejects_invalid_limits](../../tests/test_spatial_context_export.py#L131), [VectorExportTests.test_extreme_png_window_is_rejected_before_allocating_canvas_or_object_urls](../../tests/test_spatial_context_export.py#L138).

### [test_spatial_core.py](../../tests/test_spatial_core.py)

Regression checks for spatial core. Named test methods below identify the concrete behaviors; see the test-by-test guide.

**Named code items:** [grid](../../tests/test_spatial_core.py#L14), [SpatialAcceptanceTests](../../tests/test_spatial_core.py#L18), [SpatialAcceptanceTests.test_internal_outer_and_corner_boundaries_assigned_once](../../tests/test_spatial_core.py#L19), [SpatialAcceptanceTests.test_duplicate_object_ids_rejected](../../tests/test_spatial_core.py#L29), [SpatialAcceptanceTests.test_missing_object_id_cannot_be_a_new_detection](../../tests/test_spatial_core.py#L33), [SpatialAcceptanceTests.test_nonfinite_centroid_is_not_silently_discarded](../../tests/test_spatial_core.py#L37), [SpatialAcceptanceTests.test_complete_boundary_inclusion_and_tiny_sliver_exclusion](../../tests/test_spatial_core.py#L41), [SpatialAcceptanceTests.test_mask_hole_rejects_cell_even_with_center_inside_tissue](../../tests/test_spatial_core.py#L48), [SpatialAcceptanceTests.test_invalid_or_absent_mask_fails_instead_of_becoming_zero](../../tests/test_spatial_core.py#L53), [SpatialAcceptanceTests.test_raster_uses_full_footprints_and_preserves_false_hole](../../tests/test_spatial_core.py#L59), [SpatialAcceptanceTests.test_raster_no_center_resampling_of_partial_coverage](../../tests/test_spatial_core.py#L69), [SpatialAcceptanceTests.test_supplied_transform_applies_identically_to_centroids_and_mask](../../tests/test_spatial_core.py#L74), [SpatialAcceptanceTests.section](../../tests/test_spatial_core.py#L82), [SpatialAcceptanceTests.test_pdf_example_equal_section_means_and_separate_arms](../../tests/test_spatial_core.py#L86), [SpatialAcceptanceTests.test_valid_zero_is_included_and_missing_tissue_is_excluded](../../tests/test_spatial_core.py#L99), [SpatialAcceptanceTests.test_no_opposite_group_support_stays_missing](../../tests/test_spatial_core.py#L112), [SpatialAcceptanceTests.test_repeated_physical_section_cannot_be_extra_replication](../../tests/test_spatial_core.py#L119), [SpatialAcceptanceTests.test_invalid_grid_and_transform_rejected](../../tests/test_spatial_core.py#L126).
