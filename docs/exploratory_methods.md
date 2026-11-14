# Methods: current three-section condition means

The current method follows the scientist clarification of **14 November 2026**:

> Average all three, treating empty section-bins as zero; label coverage as uncertain

This replaces the earlier observed-support denominator for the active comparison. The [exact answers and policy change](scientist_clarifications_2026-11-14.md) and [machine-readable policy](../metadata/scientist_directed_mean_policy.json) preserve its authority. There are no remaining asset requests or scientist questions blocking the current task.

## Cohort and measurements

The selected cohort contains six animals and twelve completed physical sections. Homecage animals are 21F, 23M and 24M; Running animals are 22F, 21M and 22M. Each animal supplies one HK1 section and a different PFKP section. Each arm has three sections from three animals per condition. The same animals occur in both arms, so the arms are not independent animal replications.

The twelve sources contain 3,010,776 detected objects: 310,024 PLA and 2,700,752 ChAT. Interrupted job 4978 is excluded in favor of completed job 5403. The alternative `Initial Data` exports are not concatenated with this cohort. [Selected-section metadata](../metadata/selected_section_metadata.csv) and [cohort selection](../metadata/cohort_selection.json) retain source filenames, identities and hashes.

Each row is a detected object, not automatically a cell, molecule or biological replicate. PLA counts use the exported PLA object class, without requiring ChAT association. ChAT detections are retained as context and support diagnostics; they do not determine the condition-mean denominator.

## Positions, fixed alignment and grids

The supplied measurements provide bounding boxes. The recorded position is:

```text
x_native = (XMin + XMax) / 2
y_native = (YMin + YMax) / 2
```

This is a reconstructed bounding-box midpoint, not a measured segmentation centroid. Each position receives its saved section transform once. No cavity center, reflection, orientation or registration is refitted. HK1 uses the saved 21F/job 4998 reference and PFKP the separate 21F/job 5020 reference. The scientists consider the regions comparable for the current analysis; a shared numerical field does not establish additional anatomical correspondence across arms.

Identical increasing bin edges are applied to every section and both arms at each resolution. Bin widths are 1,000, 500, 250 and **100 export units**, with 100 as the default detailed view. The aligned extent is unchanged. At 100 units the complete grid contains 250 X bins by 240 Y bins. Lower edges are inclusive and upper edges exclusive, except for the final maximum edge. Each object enters one bin. Full counting retains all objects; no point sampling estimates the bin values. All 310,024 PLA positions remain available for detailed inspection.

Physical calibration is not claimed. Distance labels and scale bars are omitted as requested. The preserved map has X increasing right and Y downward. The requested presentation is 2D; there are no consecutive sections for serial reconstruction.

## Exact averaging and display rules

For PLA arm `a`, condition `c`, common bin `b` and its three selected sections, let `P(s,b)` be the raw count of aligned PLA midpoints:

```text
Mean(a,c,b) = [P(section 1,b) + P(section 2,b) + P(section 3,b)] / 3
Difference(a,b) = Mean(a,Running,b) − Mean(a,Homecage,b)
```

An empty PLA section-bin contributes zero. This holds whether ChAT objects are present or absent. Each section has equal weight; the denominator never changes with object occupancy. With one section per animal per arm, this is also an equal-animal average of these three section measurements. Millions of objects do not increase the biological sample size.

**Tissue coverage is uncertain.** An assumed zero does not establish that tissue was present and fully analyzed at that location. The denominator of three is the averaging design, not a mask-valid tissue-section count. Absence of exported detections may reflect no detected signal, absent or excluded tissue, or a technical difference.

For display, each arm uses the union of bins containing any observed PLA or ChAT object across its six sections. Outside that union, maps are blank; the complete-grid arithmetic values remain in the saved matrices and bin CSVs. The union is a plotting domain, not an inferred tissue mask. Within it, all three counts still enter each condition mean, including locations where an entire condition has no detections.

Observed support is saved separately:

```text
N_observed(a,c,b) = number of sections with at least one PLA or ChAT object in bin b
```

It ranges from zero to three and is diagnostic only. It never substitutes for the mean denominator and cannot verify complete tissue coverage. Any support-based display filter changes what is shown, not the fixed-three means.

## Figures and interpretation

Homecage and Running means use sequential count scales; differences use a linear diverging scale centered at zero with identical symmetric limits across both arms within a resolution. Numerical zero remains distinct from the blank display exterior. Counts are unsmoothed and uninterpolated, with no area normalization, percentage conversion or inferential tests. Changing bin width changes bin area and count magnitude; it is not evidence of a changed biological effect.

Current scientific exports are **600-DPI PNGs and SVG versions** at 100 and 250 units. Full-range difference figures retain the shared scale. Additional contrast figures use a disclosed ±25 display range, report saturated bins and preserve exact uncapped values in numerical outputs. Condition-mean/difference panels use one mean range across both conditions and both arms. Physical-distance labels and scale bars are omitted.

The maps answer where the selected raw-count means differ under the agreed assumed-zero policy. Read them with the individual animal sections and observed-support diagnostics. They can motivate a focused scientific followup, but do not alone establish anatomical hotspots, cell identity, direct binding, metabolic flux or a causal Running effect. The prior ChAT-associated PLA percentages are a different outcome and are not transferred into these count maps.

## Reproducibility and historical methods

`scripts/build_section_mean_maps.py` derives a new immutable `outputs/section_means/` run from saved raw-validated multiresolution section counts. It preserves the predecessor's source hash and policy, checks each mean against the three-section sum divided by three, and checks every difference against Running minus Homecage. This derivation reuses exact cached counts; it does not reread CSVs or fit alignment. Its full-grid NPZ/CSV outputs retain counts, means, differences, observed support, assumed-zero diagnostics and display-domain flags. `outputs/section_means/latest_run.json` identifies the selected run. `scripts/build_section_mean_figures.py` exports its figures.

For a fresh count cache, run `scripts/run_exploratory_maps.py` and `scripts/build_multiresolution_maps.py` against the raw sources, then derive section means and figures. [The README](../README.md) gives both rerun routes. Earlier `outputs/exploratory/` and `outputs/exploratory_multiresolution/` snapshots retain their original observed-support-N means as historical provenance; only their validated section counts and point/source records feed the current derivation.

The original PDF p. 1, sections 3-4 instead required existing tissue masks, strict 100% bin containment and a mask-valid-section denominator; p. 2 required corresponding tissue-validity outputs. The scientist-directed fixed-three method is an authorized change to that specification. It does not claim that the earlier strict mask test was performed. Its former missing-input requests are historical, not gates for the current work. The [technical handoff record](technical_handoff_requirements.md) preserves that distinction.
