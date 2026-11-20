# COMET spatial PLA Explorer

Explore **19 spatial measurements** using **Running − Homecage**, **percent change**, or **log2 fold change**, alongside the saved **2D alignment** and **observed-section support**. TDP43–HK1 and TDP43–PFKP stay separate. The default remains PLA count and Running − Homecage.

The offline app contains saved measurements and object detail. The scientific notebook, selected caches, numerical tables and **600-DPI PNG/SVG figures** support rerunning and review. **Viewing needs no Python, installation, raw CSVs or internet connection.**

## Open the app — no installation

1. On this repository’s GitHub page, choose **Code → Download ZIP**. Unzip the download. You can also use an ordinary `git clone`.
2. Open the unzipped folder, then **`outputs` → `app` → `index.html`** in Chrome, Edge, Firefox or Safari.
3. Wait for **“All 2D views loaded · ready to inspect.”** Open any of the three tabs. No zoom adjustment is needed to initialize the plots.

GitHub’s file preview does not run the app. Download and open the HTML locally. Keep it as an `.html` file. This is a large file because it includes the plots, saved measurements and full object-detail cache; allow the initial load to finish.

**Mac shortcut:** double-click **[Launch_COMET_Explorer.command](Launch_COMET_Explorer.command)** in the downloaded folder. If macOS asks which application opens the command, use Terminal; opening `outputs/app/index.html` directly is always an alternative.

**Optional local server**, using Python already installed on your computer:

```bash
python3 scripts/serve_app.py
```

This opens **http://127.0.0.1:8050/** automatically. Keep the terminal open; press **Ctrl+C** to stop it. Only the saved app folder is served, on your computer. If that port is occupied, use `python3 scripts/serve_app.py --port 8051`. No analysis dependencies or raw data are needed.

For a detailed explanation of every file, all calculations and the raw-data-to-visuals workflow, read the [repository appendix](docs/appendix/README.md). It includes worked examples, flow diagrams, a source-code guide and a complete file catalog.

## What to look at

- **Exploratory differences:** select a measurement and comparison, then view the comparison or either condition mean. Area cutoff and marker controls apply to the measurements that use them. The finest calculated grid is the default. Shared linear color controls reveal smaller contrasts; saturated bins are counted, exact values remain available, and **Restore full range** shows the complete numerical range.
- **Alignment review:** inspect the unchanged saved 2D placement, individual sections and all **310,024 PLA midpoint positions**. Visibility, zoom and point controls change the display, not the alignment or measurements.
- **Observed support:** inspect the number of sections containing exported objects in each bin. Click a bin to see all six section contributions and its condition means. This diagnostic does not change the denominator.

The **Detected-object footprint** outline keeps spatial context visible when a selected statistic or ratio is undefined. It comes from the fixed 100-unit observed PLA/ChAT domain, including its gaps; it is not a tissue boundary. The outline does not fill missing measurements or alter which bins are eligible.

For closer inspection, choose **Open fine detail**. Its default **25-unit bins** are recalculated from the original full-precision points; **Spatial detail: calculated bin width** offers 100, 50, 25 or 10 units. This is exact local rebinning, with no spatial interpolation. The original whole-field grids remain unchanged. Smaller bins are sparser and do not add biological replication. The app can select coarser detail bins with an explicit notice to stay within its local grid limit; reduce the window if it is still too large.

**Download a heatmap:** choose **Whole aligned field**, **Current map zoom** or **Fine detailed window**, then use the arm's **PNG** or **SVG** button. PNGs are fixed at **8,000 pixels wide**, preserving aspect ratio; SVGs use scalable vector geometry. To export finer calculated bins, use **Fine detailed window** after choosing their width above. The saved 600-DPI figure library remains available separately.

Download figures and bin tables from the app. The [results guide](docs/results_guide.md) explains how to read each view; the [main notebook](TDP43_COMET_analysis.ipynb) contains saved figures, checks, methods and scientific interpretation. Large notebooks may not preview on GitHub; download and open in VS Code or Jupyter to read the saved outputs. Rerunning is unnecessary for viewing.

## The scientific calculation

For the default **PLA count**, the scientist’s answers relayed on **14 November 2026** specify:

```text
Condition mean = (section 1 PLA count + section 2 PLA count + section 3 PLA count) / 3
Difference = Running mean − Homecage mean
```

**Empty section-bins contribute assumed zero; tissue coverage remains uncertain.** The mean always includes all three sections. Observed support counts detections, not verified tissue coverage. Each arm’s display is blank outside the union of observed PLA/ChAT bins across its six sections; complete-grid arithmetic remains in the numerical tables.

The **17 November calculation-functions instructions (p. 1)** define the first 13 size, area, intensity and marker-associated measurements. Six additions on **19 November** bring the total to 19: section PLA share, marker-associated PLA area fraction, median PLA intensity, PLA area interquartile range, PLA area coefficient of variation and mean PLA nearest-neighbor distance. Calculate each measurement within each section-bin, average defined section values equally by condition, then compare the two condition means. Counts and summed areas keep empty bins as zero. Object means, medians, percentiles and within-bin fractions are missing when their required objects are absent, so their defined-section N can be below three and is reported. A condition mean of section medians is not a pooled-object median.

The three comparisons are `R − H`, `100 × (R − H) / H`, and `log2(R / H)`. **`absolute_difference` is signed Running − Homecage**, not the absolute value of a difference. Undefined ratios stay missing; no pseudocount is added. Only **ChAT** is currently selectable for marker-associated PLA, using the association flag on each PLA row. The configurable area cutoff defaults to **0.1 in the exported area units**; the CSV labels these µm², but calibration has not been independently verified. See [all 19 definitions and missing-value rules](docs/calculation_functions.md).

**Section PLA share** reports a bin's percent of the total PLA count in that same physical section, so empty bins contribute zero when the section total is positive. **Nearest-neighbor distance** finds the closest other PLA detection across the full same-section point set, then averages those distances within each bin. It uses unverified export-coordinate units and is sensitive to detection density and missing neighbors at field boundaries; it is not cell spacing or proof of colocalization. The six additions retain the same three animals per condition and do not add biological replication.

There are **three animals per condition**, six animals total, with a different HK1 and PFKP section per animal. The same animals appear in both arms. The twelve completed exports contain **3,010,776 objects: 310,024 PLA and 2,700,752 ChAT**. Interrupted job 4978 is audit-only and superseded by 5403; the earlier eight exports are not added as new samples.

Positions are bounding-box midpoint proxies using the unchanged prior transforms. These are reconstructed object maps, not fluorescence images or serial 3D anatomy. The default raw-count maps are unsmoothed, uninterpolated and unnormalized; no statistical significance or causal effect is claimed. Physical-distance labels and scale bars are omitted as requested. See the [exact scientist clarifications](docs/scientist_clarifications_2026-11-14.md), [methods](docs/exploratory_methods.md), [workflow](docs/workflow.md) and [derived-data dictionary](docs/derived_data_dictionary.md).

## Recalculate the saved results

This is for analysts changing or checking calculations. It is separate from opening the app.

Run commands from the repository root with **Python 3.12 or newer**:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
```

On Windows, activate with `.venv\Scripts\activate` instead of `source`. The lock records the tested versions; `requirements.txt` provides broader version ranges when a platform needs different compatible packages.

**Recalculate from saved caches** — no raw CSVs or former-project folder required when both selected caches are present:

```bash
python scripts/execute_notebook.py TDP43_COMET_analysis.ipynb
```

This executes every current notebook cell, checks the calculation rules, writes immutable result runs, exports the figures, and rebuilds the app. The report reuses validated saved per-section counts and the selected PLA attribute cache by default. Allow several minutes for high-resolution exports. Reload the HTML after it finishes. The executor saves the notebook only after successful execution.

The old count cache alone cannot recover area, intensity or association measurements. Keep the selected run under **`outputs/measurement_features/`** as well as **`outputs/exploratory_multiresolution/`** for a complete cached rerun. If the attribute cache is unavailable, original CSVs are needed once to extract it; opening an already-built app still needs neither cache nor raw data.

Older complete attribute caches are extended automatically with exact same-section nearest-neighbor distances when rebuilding the report or app. This writes a new cache run linked to the predecessor hash, using saved coordinates; it does not require rereading the CSVs or change the original cache.

To rebuild only the app presentation from the selected saved results:

```bash
python scripts/build_comet_core_explorer.py
```

Standalone calculation/export steps are:

```bash
python scripts/build_section_mean_maps.py
python scripts/build_section_mean_figures.py
python scripts/build_review_figures.py
python scripts/build_comet_core_report.py
```

To calculate the 19 measurements and three comparisons from the saved attribute cache:

```bash
python scripts/build_measurement_report.py
python scripts/build_comet_core_explorer.py
```

This preserves the previous alignment, grid and coverage diagnostics. The selected numerical run is recorded in `outputs/calculation_functions/latest_run.json`; the app's controls explore the same measurements without changing source-object positions.

To run the software checks:

```bash
python -m unittest discover -s tests
```

Some browser-rendering logic tests also require **Node.js**; those tests report a skip when Node is unavailable. Node is unnecessary for viewing or calculating the results.

## Recount the original CSVs

Raw CSVs, microscopy files and the instruction PDF are **not included in Git**. Obtain the authorized original inputs separately. Preserve their exact filenames. Place the expanded exports in `entire Chat dataset/` under the repository, or supply their folder explicitly:

```bash
python scripts/configure_local_inputs.py --data-dir "/path/to/entire Chat dataset"
```

The configuration step verifies recorded file hashes before relocating paths. It does not alter sample assignments, transforms, policy or raw files. Then run:

```bash
TDP43_RECOUNT_RAW=1 python scripts/execute_notebook.py TDP43_COMET_analysis.ipynb
```

To extract the added area, intensity and association attributes independently, using those same configured raw sources:

```bash
python scripts/build_measurement_features.py
python scripts/build_measurement_report.py
python scripts/build_comet_core_explorer.py
```

Feature extraction checks every PLA object's identifier, source row, raw-file hash and unchanged native/aligned midpoint coordinates. It does not refit the alignment or resample objects.

On PowerShell, set `$env:TDP43_RECOUNT_RAW="1"` before the execution command. Without that environment variable the notebook reuses saved counts. Full recounts check the raw input hashes, conserve counts across four grids and retain object/source provenance.

The original PDF’s strict tissue-mask pipeline remains a **separate historical specification**. Its missing-mask preflight messages do not block the scientist-authorized fixed-three comparison.

## Where files live

| Location | Purpose |
|---|---|
| [`outputs/app/index.html`](outputs/app/index.html) | Self-contained current offline app; open locally after downloading |
| [`TDP43_COMET_analysis.ipynb`](TDP43_COMET_analysis.ipynb) | Executed current scientific report |
| [`outputs/section_means/latest_run.json`](outputs/section_means/latest_run.json) | Selects the included current numerical run, bin CSVs, matrices and 600-DPI figures |
| [`outputs/calculation_functions/latest_run.json`](outputs/calculation_functions/latest_run.json) | Selects the added measurement/comparison numerical report and representative 600-DPI figures |
| [`outputs/measurement_features/latest_run.json`](outputs/measurement_features/latest_run.json) | Selects the full-precision PLA attributes matched to the unchanged count/point cache |
| [`outputs/exploratory_multiresolution/latest_run.json`](outputs/exploratory_multiresolution/latest_run.json) | Selects the included raw-validated count cache; its old variable-N summaries are historical |
| [`outputs/comet_core/detailed_review/`](outputs/comet_core/detailed_review/) | High-resolution alignment atlases and support maps |
| [`metadata/scientist_directed_mean_policy.json`](metadata/scientist_directed_mean_policy.json) | Current averaging rule and explicit coverage uncertainty |
| [`metadata/calculation_functions_policy.json`](metadata/calculation_functions_policy.json) | Added measurement definitions, empty-bin rules, comparison rules and PDF provenance |
| [`metadata/selected_section_metadata.csv`](metadata/selected_section_metadata.csv) | Animal, condition, section, source and duplicate relationships |
| [`outputs/validation.json`](outputs/validation.json), [`outputs/protocols/`](outputs/protocols/) | Recorded analysis verification and provenance |

Only deliberately selected, verified result snapshots are committed. Dated predecessors retained for comparison/provenance are identified in the appendix catalog; unselected generated runs and local workspace-copy records stay on the analysis computer. New generated runs are ignored until deliberately selected for a future results update. Input paths recorded in historical provenance identify the original machine; cached reruns resolve the copied local snapshots.

The [earlier native supporting app](outputs/app/native_explorer.html) and [supporting notebook](TDP43_native_supporting_analysis.ipynb) concern the original eight-export intake. They are preserved as background, with a different scope from the current twelve-section comparison. The [former PLA–ChAT repository](https://github.com/adamwbrew/Bio_Data_Analysis) supplies methodological provenance, not expected results for these maps.
