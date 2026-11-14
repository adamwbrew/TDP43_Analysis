# Trace of the previous app's saved alignment

Read-only source review, 11 November 2026. The new two-page instruction PDF was read again in full. Its three visual deliverables are: two separate Running-minus-Homecage PLA count-difference maps; the previous alignment check reproduced without changing alignment; and four condition-specific coverage maps, which may be arranged as one panel figure (PDF pp. 1-2).

**Cohort update, 11 November 2026:** the user has explicitly selected the former app's 12 completed sections and added `entire Chat dataset/` under the new Desktop project. All 13 raw CSV hashes there match the recorded expanded sources; job 4978 remains an audited interrupted export superseded by 5403. The selected six-animal/two-arm assignments are now resolved for this cohort and recorded in [cohort_selection.json](../metadata/cohort_selection.json) and [selected_section_metadata.csv](../metadata/selected_section_metadata.csv). The newly added folder has no non-CSV tissue-mask assets. The earlier eight-file comparison below describes the initial intake, not the now-selected complete source set.

## What has now been recovered

**All 12 historical fixed transformations are present and replayable.** The previous app's numerical alignment is available both in its embedded explorer payload and in `outputs/spatial_handoff/tables/alignment_proposals.json` of the old project. Earlier statements that numerical transforms could not be located were too broad. The existing alignment view can be populated immediately, preserving the saved centers and flips rather than optimizing or refitting anything.

The remaining distinction is tissue coverage. The old app's visible silhouettes represent bins containing detections. They are not the independent tissue boundaries needed to decide whether 100% of an entire analysis bin was sampled. Recovering a display alignment does not recover those masks.

The newer PDF's statement that the alignment was accepted remains the current instruction. Historical `ready: false` and `approved: false` values are retained as provenance; they are not a request to redo the scientist's approval or realign sections.

## Exact source chain

1. Old app: `/Users/adambrewer/Desktop/Coding/Bio_Data_Analysis/outputs/spatial_handoff/app/index.html`.
2. Its explorer payload follows the JavaScript marker `const root=document.getElementById('...'), DATA=`. It contains 12 section records, native grids of widths 250, 500 and 1,000, fine 100-unit grids, full selected transform records in `proposed`, source filenames, historical labels and colors.
3. Every embedded `proposed` record exactly matches the corresponding saved row in `outputs/spatial_handoff/tables/alignment_proposals.json`.
4. Those selected transforms were originally produced from cavity annotations in `metadata/handoff_landmark_proposals.json`. Replaying them does **not** call the old `alignment_proposals` fitting/ranking function.
5. `bio_visuals/explorer.html`, lines 147-149, selects the saved frame and applies the saved center/flip to native grid coordinates. The Python equivalent is `bio_visuals/handoff.py`, lines 267-275.

The original app defaults to **Feature-aligned - proposed, all sections**, not its empty reviewed-only mode. Its flat and exploded views therefore already contained the numerical transformations the scientist recalls. The saved review table's blank approval flags did not prevent that historical display.

## Transformation convention and reference frames

For each source-native position `(x, y)`, the old app applies:

```text
x_aligned = sign_x * (x - saved_center_x)
y_aligned = sign_y * (y - saved_center_y)

sign_x = -1 for horizontal/both flips, otherwise +1
sign_y = -1 for vertical/both flips, otherwise +1
```

The extracted snapshot records the exactly equivalent affine matrix, including its signed translation, without fitting new parameters. X increases right and Y is displayed downward in the old map. Camera rotation changes the view; it does not change any transform.

| Historical job | Historical label | PLA arm | Saved cavity center X | Saved cavity center Y | Saved flip |
|---|---|---|---:|---:|---|
| 4998 | 21F | HK1 | 30904.110003 | 35852.614083 | none |
| 5007 | 23M | HK1 | 29605.787037 | 35299.151235 | none |
| 5002 | 24M | HK1 | 32361.684982 | 33262.820513 | none |
| 4997 | 22F | HK1 | 5868.154762 | 35945.238095 | vertical |
| 5006 | 21M | HK1 | 4492.180149 | 33817.532989 | none |
| 5001 | 22M | HK1 | 7453.948462 | 33127.098919 | vertical |
| 5020 | 21F | PFKP | 30305.378401 | 8037.670068 | none |
| 5005 | 23M | PFKP | 29861.387479 | 7791.370558 | none |
| 5000 | 24M | PFKP | 32152.658885 | 3475.866222 | vertical |
| 5403 | 22F | PFKP | 6198.573574 | 8728.340841 | vertical |
| 5003 | 21M | PFKP | 4968.274303 | 9409.419744 | none |
| 4999 | 22M | PFKP | 8464.542125 | 3529.184982 | vertical |

Table values are rounded for reading; the JSON snapshot preserves the full saved precision. HK1's orientation reference is historical 21F/job 4998. PFKP's is the different physical section historical 21F/job 5020. Each arm is centered on its own cavity. These two reference choices do not establish a global anatomical registration between arms.

The display grids are originally binned in each section's native frame. Subtracting a fractional cavity center gives each section a different aligned grid phase. Overlaying these grids is appropriate for replaying the old view, but their bins must not be averaged as if they were a shared aligned analysis grid. The requested new count maps need the selected raw object coordinates assigned once to one explicitly recorded common grid (PDF p. 1).

## Which visible outlines are actually masks?

| Saved object | What it represents | Suitable for strict 100% tissue validity? |
|---|---|---|
| `proposed.polygon_native` | Internal ventricular-cavity trace used as the anchor | No. It is an internal hole, not the outer tissue boundary. |
| `candidate_polygon` | Earlier automatic internal-void candidate | No. It is also a cavity proposal. |
| NPZ `support` | `n_all > 0`, meaning at least one PLA or ChAT object in that bin | No. Empty tissue bins cannot be distinguished from absent tissue. |
| App **Observed-bin silhouettes** | The same occupied-bin display, with value 1 where objects are observed | No. The app explicitly labels these as observations, not traced masks. |
| Six-panel static silhouette boundary | One-bin binary closing plus largest-component boundary points from occupied all-object bins | No. It is a plotting proxy, not supplied ROI geometry. |
| CSV names containing `tight`, or historical “outline” analyses | An owner-described HALO selection method whose resulting objects were exported | No. The actual annotation vertices/raster were not exported with those object tables. |

In `explorer.html`, lines 150-152, a bin without `n_all` is missing; the **support** metric returns 1 only after that occupancy check. Lines 225-227 explain the layer appearance. `feature_alignment.py`, lines 18-28, constructs the static outline proxy from occupied bins. `docs/tissue_outline_review.md`, lines 58-66, explicitly states that the “outline” exports lack polygon vertices, binary masks, annotation area and physical calibration.

Every inspected saved 1,000-unit `support` array exactly equals `n_all > 0` (12/12). All 11 older spatial CSV tables containing `roi_membership_known` contain only `False`. Neither the display grids nor the existing internal-cavity polygons establish the new PDF's full-bin tissue containment rule. No replacement mask was inferred or created during this review.

## Search scope and fresh verification

The review inspected both `output/` and `outputs/`, with no assumption based on their names. Singular `output/` contains exactly one budgeting PDF, `output/pdf/Lab_AI_Analysis_Cost_Overview.pdf`, and no alignment or mask assets. Plural `outputs/` contains 464 noncache files, including 36 NPZ archives and four workbooks. All NPZ keys and all workbook sheet names/headers were examined for additional geometry. The workbooks contain measurements and analysis tables; no supplied tissue-boundary sheet was identified.

The newer Desktop TDP43 project was inventoried again, including native-atlas payloads, metadata, outputs and recent file modification times. Its native-atlas app is an unaligned export-QC product. It contains no newer independent tissue geometry or replacement fixed alignment. This review searched only the specified old/new projects and the connected historical remote repository, not unrelated personal folders or past conversations.

GitHub `main` was freshly verified at `4631e1517f85de2c4bfb59879bf44f406770a903`. Its full recursive tree has 551 entries and was not truncated. The local old checkout remains `f7fda4e36774b456c0e7b6df24f9666332198586`, a parent of that merge. Git blob hashes for the critical code, app, proposal/review records and old alignment PNG exactly match current remote main (9/9). There is no newer alignment or tissue-mask file hidden by a local-versus-remote revision discrepancy.

The eight supplied current CSV hashes were rechecked. Four saved app inputs match current files byte for byte: job 4999/input_005, 5000/input_006, 5001/input_007 and 5002/input_008. The other four current files are earlier alternative exports not represented as separate layers in this saved 12-section app. Exact byte identity establishes which display transform belongs to an identical export; historical group labels remain marked as historical and are not silently promoted into current primary experimental assignments.

## Reproducible recovered assets

- [Exact alignment snapshot](../outputs/comet_core/alignment_snapshot.json): all 12 sections, unmodified 250/500-unit native display counts, saved center/flip/matrix, internal-cavity polygons, colors, source hashes, exact current-file matches and source-function-compatible 250-unit grid geometry.
- [Asset audit](../outputs/comet_core/asset_audit.json): search scope, source SHA-256 hashes, remote blob checks, occupancy semantics and a compact 500-unit snapshot for the interactive alignment review.
- [Extraction script](../scripts/extract_alignment_snapshot.py): recovers the payload without invoking registration or mask-generation code.

From the new project environment:

```bash
python scripts/extract_alignment_snapshot.py
```

The optional `--old-root`, `--input-manifest` and `--output-dir` arguments make source locations explicit. The script rechecks current CSV hashes, confirms all 12 embedded proposal records against saved JSON, verifies the app's 1,000-unit counts against saved NPZ arrays and records its own hash.

The old six-panel alignment-check figure is `outputs/spatial_handoff/figures/19_feature_alignment_before_after.png`. It is generated by `bio_visuals.feature_alignment.alignment_figure(geometry, proposals)`. Reproduction can use `alignment_figure_geometry_grid` from the snapshot and the saved `proposed` records. Do not call `alignment_proposals`. Replaying the plotting boundary operation uses the same saved count grid; it neither reselects alignment nor establishes a tissue mask. The previously saved PNG should be retained separately as the reference, rather than presenting a copied file as newly reproduced.

For source-function reproduction, the old direct environment `/Users/adambrewer/Desktop/Coding/Bio_Data_Analysis/.venv/bin/python` was verified to work as Python 3.9.6, with NumPy 2.0.2, pandas 2.3.3, SciPy 1.13.1, Matplotlib 3.9.4 and Plotly 6.9.0. Set a writable `MPLCONFIGDIR` and disable bytecode writes before importing old source. The `alignment_figure` function-source SHA-256 is `9363b6b370cabdfe18bb81f8f5df03079f68799106be6b5397ddefcdb266b458`. Its recorded original styling uses `handoff_plots.style()` and 300-DPI PNG export with `bbox_inches='tight'`.

## What can proceed now

The native-versus-saved alignment check, historical per-section overlays and display-order 3D stack can be replayed from the recovered fixed parameters. Stack spacing is an interface control; the layer axis is animal display order, not measured anatomical depth. The two PLA arms remain separate.

The two requested biological difference heatmaps and their four section-coverage maps still require actual existing tissue masks/outlines matched to the intended section roster, plus the documented raw-object/centroid selection. The shared 25 × 24 grid of 1,000 export-unit bins is now recorded in `metadata/grid_parameters.json`; it is configured without calculating a condition effect and does not establish physical scale. Occupancy-based substitutes would erase the distinction between a valid zero-PLA bin and unsampled tissue, directly violating PDF p. 1. The recovered alignment view is useful concrete progress while those remaining inputs are resolved.
