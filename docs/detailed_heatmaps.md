# Detailed spatial maps: resolution and source review

The 12 November 2026 update adds genuinely recounted 1,000-, 500-, 250- and 100-export-unit grids on the same unchanged aligned field. The 250-unit view has 100 columns × 96 rows (16 times the original number of bins). The finest 100-unit view has 250 columns × 240 rows (100 times the original number of bins). These are numerical export units; physical pixel size and micrometer calibration remain unverified.

## What the extra detail answers

Use the broad map to locate a region, choose a finer grid to inspect within-region variation, then inspect individual section contributions and exact exported PLA midpoint locations. A group map alone cannot show whether a feature occurs in every animal or is driven by a single section. The linked section views make that distinction visible.

The object views reconstruct the locations of exported detections. They do not display original fluorescence, segmentation boundaries, tissue masks or validated anatomical regions. A dot is a bounding-box midpoint, not a measured cell centroid or a literal PLA molecule. The full selected PLA coordinate set is retained; no sampled subset supplies the heatmap counts.

## Recounting, rather than magnifying the original map

At every resolution, all raw PLA and ChAT objects are assigned to the grid containing their unchanged transformed midpoint. Per-section raw counts are calculated before condition means. The exact exploratory rule remains `observed_support = (PLA + ChAT) > 0`; a ChAT-only supported bin contributes a PLA count of zero. A section-bin with no exported objects has unknown tissue status and does not contribute to the exploratory mean.

Each resolution therefore changes both bin area and observed-support denominators. A fine difference cannot be reconstructed by interpolating a coarse difference, and averaging fine-bin means generally does not reproduce a coarse-bin mean. Only **raw section counts** aggregate exactly across nested grids. In particular, 250- and 100-unit grids are not nested within one another; both subdivide the 500-unit grid. Validation checks the appropriate nested raw-count relationships.

Both arms use one shared, symmetric, zero-centered linear difference scale **within each resolution**. Color limits and raw counts change across resolutions. Compare the recorded color bars rather than treating identical colors at different bin widths as identical effects. Counts are neither normalized by area nor smoothed or interpolated. No statistical tests are added.

Large outlying differences can compress smaller differences toward white. The app therefore provides a shared symmetric linear **display range**, and a supplementary 100-unit figure uses ±25 counts. Values beyond the selected range receive endpoint colors; the displayed clipped-bin count identifies this saturation. Hover values, tables and saved arrays retain their exact uncapped values. This is a reversible color-display choice, not normalization, trimming or a change in the calculation. Full-range figures remain available. Do not read an endpoint color as the actual maximum.

Finer grids make detection support sparser. Inspect the four observed-section N maps and the minimum-N display filter alongside every comparison. N=3 remains detected-object support in three sections, not proof that an entire bin is tissue-covered. Finer patterns, selected maxima and single-bin differences remain exploratory and correlated. They do not add biological replication beyond three animals per condition.

## Files, figures and rerun

`outputs/exploratory_multiresolution/latest_run.json` selects a new immutable multiresolution run. Its index identifies per-resolution payloads, section/count matrices, full PLA point provenance, source hashes, parameters and cross-grid validation. Earlier 1,000-unit runs remain preserved, and the recounted 1,000-unit arrays are checked against that baseline.

`scripts/build_detailed_figures.py` exports 300-DPI PNGs and SVGs: fine two-arm differences, a four-resolution sensitivity atlas, condition means, four observed-support maps, and six individual-section maps per arm. SVG heatmap tiles are embedded as high-resolution rasters to keep scientific exports manageable; labels remain editable vector text.

The main notebook recomputes the raw sources, validates the numerical outputs, saves the detailed figures and rebuilds the offline app. See the README for the project environment and executor. The user-authorized exploratory mode stays separate from the still-pending strict mask-based results.

## Scientist handoff

Use [scientist_questions.md](scientist_questions.md) for eight plain-language questions about the experiment, anatomy, existing images/outlines, object-center measurements, exclusions, treatment and controls. Scientists can point to existing records or the imaging contact. The analysis team and imaging analyst handle file conversion, coordinate mapping, calibration metadata and source-object linkage using [technical_handoff_requirements.md](technical_handoff_requirements.md).

## Detailed alignment and support tabs

The alignment tab uses the selected fine grid and every selected PLA location in saved/native coordinate views, with the original frozen alignment check retained. Zoomed individual-section views reveal local point detail; camera rotation and stack spacing affect the view only. The observed-support tab uses four discrete colors for N=0,1,2,3 and a local membership view identifying the sections behind a bin's count. Source-object positions and counts remain the same saved measurements.

`outputs/comet_core/detailed_review/` contains three additional 300-DPI PNG/SVG review figures: a detailed four-panel observed-support map and a six-section PLA-location atlas per arm. `scripts/build_review_figures.py` renders these from the validated saved payload, with its hash recorded. `scripts/refresh_review_notebook.py` executes only the self-contained review display cell and preserves the previously executed raw-analysis cells. This is a presentation refresh; it does not re-read raw exports or recalculate alignment or condition differences.

Technical references checked 12 November 2026: [Plotly heatmaps](https://plotly.com/javascript/heatmaps/) documents explicit cell edges and missing-value behavior; [Plotly events](https://plotly.com/javascript/plotlyjs-events/) documents linked click and zoom events. These support the viewer implementation, not anatomical or biological validity.
