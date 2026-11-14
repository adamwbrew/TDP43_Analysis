# COMET spatial PLA project brief

Updated 14 November 2026. Current authority is the [scientist feedback and final averaging instruction](scientist_clarifications_2026-11-14.md): **average all three sections per condition, treating empty section-bins as zero; label coverage as uncertain.** This supersedes the earlier observed-support denominator and the original PDF's tissue-mask requirement for the agreed task. No further scientist questions or asset requests block this analysis.

## Scientific question and intended use

For TDP43–HK1 and TDP43–PFKP separately, where do mean raw PLA counts differ between Running and Homecage after applying the existing alignment? Present both condition means and **Running minus Homecage** to show what produces a difference. The maps support comparison of the selected animal sections and focused scientific followup. They do not alone establish direct binding, cell identity, metabolic flux or a causal exercise effect.

## Design and sources

| Item | Current selection and interpretation |
|---|---|
| Homecage | 21F, 23M, 24M; three independent animals |
| Running | 22F, 21M, 22M; three independent animals |
| PLA arms | One HK1 section and a different PFKP section per animal; the same animals occur in both arms |
| Physical sections | Twelve completed sections; one section per animal per arm |
| Selected input | Twelve object-results CSVs from `entire Chat dataset/`, comprising 3,010,776 detections: 310,024 PLA and 2,700,752 ChAT |
| Interrupted export | Job 4978 retained for audit; completed 5403 supplies that section |
| Earlier eight-export intake | A preserved historical inventory of overlapping alternatives, not additional sections or animals |

The user selected this exact former-app cohort and supplied byte-identical raw sources; the assignments are not inferred from filenames alone. [Cohort selection](../metadata/cohort_selection.json) and [section metadata](../metadata/selected_section_metadata.csv) record the source identities, hashes and animal/condition/arm relationships. Source files and historical projects are preserved.

Rows are detected objects, not independent biological replicates or automatically cells or molecules. The biological sample size is three animals per condition. The two PLA arms are analyzed separately and are not independent replications of the animal comparison.

## Measurements and spatial method

The exports contain twenty raw fields covering identity/class, PLA and ChAT flags, object size, intensity, bounding-box limits and source metadata. [The raw-field dictionary](../metadata/data_dictionary.json) retains the initial eight-export inventory ranges; those ranges are not relabeled as a fresh twelve-section audit.

The current accepted position proxy is `(XMin+XMax)/2, (YMin+YMax)/2`. These bounding-box midpoints are not measured segmentation centroids. Apply each section's recovered saved translation/reflection once, with no refitting, scaling or warping. HK1 retains 21F/job 4998 as reference; PFKP retains the different 21F/job 5020 reference. The scientists consider the anatomical regions and saved alignment sufficient for this comparison; no renewed anatomical approval is requested.

All sections and both arms use identical bin edges at each recorded resolution: 1,000, 500, 250 and 100 export units. The default detailed view is **100**, with an unchanged aligned extent. Numerical bin widths are analysis settings; physical calibration is not claimed, and physical-distance labels and scale bars are omitted. The current requested presentation is **2D**, with no serial-section construction.

For each arm and bin:

```text
Homecage mean = sum of its three section PLA counts / 3
Running mean = sum of its three section PLA counts / 3
Difference = Running mean − Homecage mean
```

Empty PLA section-bins contribute zero. The denominator remains three regardless of detected-object support. This is equal weighting of the three selected animal sections within each condition and arm.

**Coverage is uncertain.** A zero does not demonstrate that tissue was present and fully analyzed. Each arm's plots show the six-section union of bins containing any observed PLA/ChAT object, with blank space outside that plotting domain; full-grid arithmetic zeros remain saved. That union is not a tissue mask. Four observed-support maps remain useful diagnostics, without changing the mean denominator or claiming verified coverage.

## Outputs and validation record

The app and main notebook present detailed condition means and differences, linked individual-section counts and all 310,024 PLA positions. The prior alignment-check figure and unchanged transform provenance are retained. Differences use one symmetric linear zero-centered scale across both arms within a resolution. Counts are unsmoothed, uninterpolated and unnormalized; no statistical tests are part of this version.

Current scientific exports include **600-DPI PNGs and SVG versions** at 100 and 250 units: full-range differences, explicitly contrast-limited views and panels showing both means alongside their difference. Source records, per-resolution matrices/CSV tables, observed support, assumed-zero diagnostics, display-domain flags and arithmetic validation accompany each immutable `outputs/section_means/` run. [The latest-run pointer](../outputs/section_means/latest_run.json) identifies the active snapshot.

The section-mean builder reuses validated exact per-section count caches and independently checks sums divided by three and Running minus Homecage. A full raw recount remains available. [The README](../README.md) separates those rerun routes; [methods](exploratory_methods.md) and the [derived dictionary](derived_data_dictionary.md) define the fields.

## Historical PDF contract

The original two-page PDF specified the two separate contrasts and unchanged alignment check (p. 1, sections 1-2), strict 100% mask-valid bin eligibility and valid-section averaging (p. 1, sections 3-4), and shared linear signed plotting plus saved numerical/validation outputs (p. 2, sections 5-7). The current instruction preserves arm separation, fixed alignment, contrast direction, common grids and traceable outputs, while explicitly selecting fixed-three mask-free averaging and uncertain coverage.

The original strict-mask test has not been performed or claimed for this analysis. Its earlier missing-input checklist and the old observed-N estimators are retained as historical provenance in [the technical record](technical_handoff_requirements.md), not active requests. Original images, tissue outlines, further anatomy approval, calibration and serial 3D data are not prerequisites for the agreed task.
