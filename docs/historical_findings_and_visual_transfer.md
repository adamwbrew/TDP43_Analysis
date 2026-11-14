# Prior findings and visual practices used in this project

**Calculated exploratory maps now available:** under the user’s further explicit authorization, the main app/notebook calculate separate raw-count differences and observed-section support from all twelve sources. These are distinct from the former ChAT-association findings and from the still-pending strict tissue-mask result; see `exploratory_methods.md`.

Reviewed 9 November 2026; cohort and alignment update 11 November 2026.

**Current scope:** the user has now selected the former app’s twelve completed sections and supplied their expanded exports in this project. Those exact source assignments and fixed transforms are now applicable, and the prior alignment-check PNG has been regenerated identically without refitting. The main app centers the PDF’s three visual deliverables; initial-eight-file native/morphology work is supporting material. Existing tissue masks and the centroid definition remain unresolved.
 The former project provides substantive findings, working visual examples and reusable analysis design. It also defines the limits of what can be transferred. This report makes that connection visible, while keeping the current measurements and historical results distinguishable.

## Source and verification

The accessible source is `/Users/adambrewer/Desktop/Coding/Bio_Data_Analysis`, local revision `f7fda4e36774b456c0e7b6df24f9666332198586`. Connected GitHub access verified [`main` at `4631e1517f85de2c4bfb59879bf44f406770a903`](https://github.com/adamwbrew/Bio_Data_Analysis/commit/4631e1517f85de2c4bfb59879bf44f406770a903) and read its [results guide](https://github.com/adamwbrew/Bio_Data_Analysis/blob/main/docs/results_guide.md). The local and remote revision identifiers differ; all exact numerical checks and copied figures below identify the local saved source files rather than claiming that the entire local checkout matches remote `main`.

The review read the saved scientific and audit notebooks, result guide, quickstart, comparison tables, normalization and morphology summaries, image-layout audit, review records and relevant plotting/app code. Four relevant high-resolution figures were visually inspected and copied byte for byte, with their PNG/SVG source hashes. The machine-readable [historical context](../outputs/native_atlas/historical_context.json) records the source paths, hashes, exact values, verification scope and captions used in the new app.

The former expanded analysis used **13 exports, retaining 12 physical sections from six animals**, with one section per animal per PLA arm. The same six animals appear in both arms: three Home cage and three Running animals, rather than twelve independent animals. Saved tables contain **3,010,776 detections: 310,024 PLA and 2,700,752 ChAT**. The interrupted repeat was excluded from those primary results.

The initial eight exports match the historical `Initial Data` collection; four also occur among the expanded inputs. Their overlap audit is retained separately. On 11 November 2026 the user selected the former app’s twelve completed sections and added their expanded raw files. All thirteen new-folder hashes match the historical source manifest; interrupted 4978 is excluded for 5403. The applicable roster is now explicit in [cohort_selection.json](../metadata/cohort_selection.json); the eight alternatives are not added as independent sections.

## Findings retained as historical evidence

The historical primary outcome was the percentage of PLA detections with ChAT signal within each animal: `100 × ChAT-positive PLA / all PLA`. Each group then averaged three animal percentages equally. The exact means were recomputed from the **saved animal-level numerators and denominators** and agreed with saved contrast tables to less than `1e-10`. The historical raw-data analysis was not rerun.

| Historical outcome | TDP43–HK1 | TDP43–PFKP |
|---|---:|---:|
| Home-cage equal-animal mean | 53.59% | 73.20% |
| Running equal-animal mean | 31.58% | 50.62% |
| Home cage − Running | +22.01 percentage points | +22.58 percentage points |
| Omit one animal from each group, all nine combinations | +16.16 to +30.80 points | +19.22 to +27.59 points |
| Common PLA-size mixture | +23.47 points | +24.07 points |
| Common learned size/shape mixture, exploratory K=3 | +22.89 points | +23.30 points |

The omitted-animal intervals are sensitivity ranges, **not confidence intervals**. Their nine cells reuse the same animals. Size and morphology checks show that these simple measurement mixtures did not remove the old association contrast. They do not correct tissue area, ChAT availability, sampled anatomy, acquisition or segmentation, and do not show that exercise caused the result.

Sources: historical `outputs/spatial_handoff/tables/animal_summary.csv.gz`, `condition_contrasts.csv.gz`, `condition_standardization.csv.gz`, and `ml_standardized.csv.gz`; hashes are in the context JSON.

![Historical animal observations and contrasts](../outputs/native_atlas/historical_figures/13_condition_averages_difference.png)

**HISTORICAL EXPANDED PLA–ChAT DATASET.** Each dot is a mouse. Thick lines are equal-animal means; black intervals omit one animal per group. The right-hand panels use summed ChAT-overlap area / summed PLA area, a different outcome from the left-hand object percentages. These values are not new COMET count-map findings. The figure's useful practice is to connect all animal observations to the stated group estimator and difference.

Two further historical findings lead to concrete checks:

- **Source-image layout coincided with condition.** All twelve former sections placed Running at lower X and Home cage at higher X; all six within-source-image/arm association contrasts were positive. The saved layout summary flags acquisition and composite provenance for review. A post-detection coordinate offset cannot by itself change association. Shared image IDs do not establish experimental pairing or eliminate confounding. Current source-image relationships need an independent audit.
- **Shape-model exclusions did not change the primary denominator.** Summing the twelve rows of `ml_audit.csv.gz` gives 49,618 excluded of 310,024 PLA, or 16.0%, because diameter ratios were unusable. Those detections remained in primary results. The useful practice is separate QC reporting and native-coordinate review targets. The former cluster fit and exclusion parameters are not current defaults.

![Historical denominator and direction audit](../outputs/native_atlas/historical_figures/17_normalization_both_directions.png)

**HISTORICAL EXPANDED PLA–ChAT DATASET.** Opposite subtraction directions reverse the same contrast. Rows answer distinct measurement/weighting questions; pooling detections is a diagnostic that changes animal weights. The current PDF prohibits normalization and statistical tests in the first count-map pass (p. 2), so these analyses are shown as historical context rather than inserted into the new count-map calculation.

## Visual practices transferred

The former project did more than draw a coarse heat map. It reconstructed fine native coordinates, layered marker context, showed individual specimens, used common scales, exposed denominators on hover and explained how a scientist should follow up. These practices remain useful before accepted group anatomical maps are available.

![Historical fine native-coordinate overlay](../outputs/native_atlas/historical_figures/02_native_overlay_hk1.png)

**HISTORICAL EXPANDED PLA–ChAT DATASET.** Separate HK1 sections, with ChAT midpoint counts in gray and PLA midpoint counts in color at 100 × 100 export-unit bins. Shared scales help compare measurement magnitudes within the arm. The layer image reconstructs detections; it is not original microscopy, calibrated anatomy, or current-data output. Current native reconstructions use current detections and disclosed current display bin widths.

| Former working practice and source | Transfer into the current project | Scientific boundary |
|---|---|---|
| Fine PLA/marker overlays: `bio_visuals/handoff_plots.py::native_atlas` and `bio_visuals/explorer.html::channels` | Current source-specific midpoint reconstructions, marker context and fine/coarse inspection; preserve x/y aspect and native image-y direction. | A bounding-box midpoint is a proxy, not a measured object centroid or microscopy pixel. Object occupancy is not tissue coverage. |
| Shared measurement scales: `explorer.html::maximum`, `channels`, and `nativeHover` | Keep comparable panels on a shared scale; show actual bin count and source coordinates on hover. | A log display reveals dynamic range but does not normalize biological measurements. Per-map maximum normalization would destroy count comparability. |
| Question-led findings: `PLA_ChAT_scientific_analysis.ipynb`, `condition_comparison.html::readingGuide`, explorer view guides | Explain the question, how to read the view, supported finding, uncertainty and next source-image or metadata check. | A convincing visual does not supply missing sample identity, a valid denominator or anatomical correspondence. |
| Independent specimen panels and supporting readouts: `handoff_plots.py::detailed_section` | Compare native exports and alternate analyses visibly; show counts, marker context, distributions and overlap audits separately. | Repeated ROI exports or marker analyses cannot be promoted into independent biological replicates. |
| Review queues: `handoff.py`, `morphology_ml.py` | Export declared native-coordinate windows and original object/source identifiers for microscopy review. | Extreme windows are selected audit targets, not representative prevalence samples or validated anatomical hotspots. |
| Offline interaction plus high-resolution figures: `standalone_app.py`, `docs/results_guide.md` | A connected saved Plotly explorer, static PNG/SVG companions and simple reading instructions. | Controls explore saved measurements. They do not silently rerun the analysis or manufacture unavailable biological outputs. |

The resulting visual improvement comes from richer **current** measured spatial structure and evidence, supported by the former project's visual design. Historical images are clearly captioned reference panels and remain separate from those current findings.

## Why the old aligned layers cannot become current accepted maps

![Historical alignment proposal comparison](../outputs/native_atlas/historical_figures/19_feature_alignment_before_after.png)

**HISTORICAL EXPANDED PLA–ChAT DATASET; COMPUTATIONAL PROPOSALS.** Native, cavity-centered and feature/flip views compare old detection-derived geometry. The source caption explicitly calls these geometric suggestions rather than anatomical approvals. All twelve historical review records lack full approval, and no independently supplied tissue masks were identified in the available project assets.

The new PDF says an alignment has already been accepted and requires preserving it, existing masks and fixed geometry (p. 1). It prohibits new alignment and signal-derived masks. That newer instruction takes precedence. The recovered saved transforms are now linked to all twelve selected current source copies by hash, and the same prior figure reproduces pixel-for-pixel. The original proposed/unreviewed flags are retained as provenance; the newer PDF directs reuse of this saved alignment. No new fit or approval process is imposed. Actual tissue masks and a documented centroid definition are still required.

Once those assets and the authoritative sample mapping are matched, the required output remains raw mean PLA counts per fully covered bin and condition, their signed difference, and the separate contributing-section maps. Fully covered zero-count bins are valid zeros; unobserved or partially covered bins are missing. Current native-coordinate reconstructions and file-level measurements are useful now, while their blank background cannot establish tissue absence.

The transferred foundation therefore includes better reconstructions, clearer explanations, specimen-aware comparisons, QC navigation and provenance. Historical ChAT-fraction conclusions, cutoffs and K-means models do not become new count-map findings. Animal assignments and fixed transforms now apply because the user selected this exact cohort. The count-grid configuration is recorded separately; no tissue masks or anatomical depth are invented.
