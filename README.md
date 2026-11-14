# COMET spatial PLA Explorer

Explore **Homecage and Running mean PLA counts**, their **Running − Homecage difference**, the saved **2D alignment**, and **observed-section support**, separately for TDP43–HK1 and TDP43–PFKP.

The repository includes the working offline app, executed scientific notebook, selected saved count cache, numerical tables and **600-DPI PNG/SVG figures**. **Viewing needs no Python, installation, raw CSVs or internet connection.**

## Open the app — no installation

1. On this repository’s GitHub page, choose **Code → Download ZIP**. Unzip the download. You can also use an ordinary `git clone`.
2. Open the unzipped folder, then **`outputs` → `app` → `index.html`** in Chrome, Edge, Firefox or Safari.
3. Wait for **“All 2D views loaded · ready to inspect.”** Open any of the three tabs. No zoom adjustment is needed to initialize the plots.

GitHub’s file preview does not run the app. Download and open the HTML locally. Keep it as an `.html` file. It is about 77 MB because it includes the plots, saved measurements and full object-detail cache.

**Mac shortcut:** double-click **[Launch_COMET_Explorer.command](Launch_COMET_Explorer.command)** in the downloaded folder. If macOS asks which application opens the command, use Terminal; opening `outputs/app/index.html` directly is always an alternative.

**Optional local server**, using Python already installed on your computer:

```bash
python3 scripts/serve_app.py
```

This opens **http://127.0.0.1:8050/** automatically. Keep the terminal open; press **Ctrl+C** to stop it. Only the saved app folder is served, on your computer. If that port is occupied, use `python3 scripts/serve_app.py --port 8051`. No analysis dependencies or raw data are needed.

## What to look at

- **Exploratory differences:** choose Running − Homecage, Homecage mean or Running mean. The finest calculated grid is the default. Shared linear color controls reveal smaller contrasts; saturated bins are counted, exact values remain available, and **Restore full range** shows the complete numerical range.
- **Alignment review:** inspect the unchanged saved 2D placement, individual sections and all **310,024 PLA midpoint positions**. Visibility, zoom and point controls change the display, not the alignment or measurements.
- **Observed support:** inspect the number of sections containing exported objects in each bin. Click a bin to see all six section contributions and its condition means. This diagnostic does not change the denominator.

Download figures and bin tables from the app. The [results guide](docs/results_guide.md) explains how to read each view; the [main notebook](TDP43_COMET_analysis.ipynb) contains saved figures, checks, methods and scientific interpretation. Large notebooks may not preview on GitHub; download and open in VS Code or Jupyter to read the saved outputs. Rerunning is unnecessary for viewing.

## The scientific calculation

The scientist’s answers relayed on **14 November 2026** specify:

```text
Condition mean = (section 1 PLA count + section 2 PLA count + section 3 PLA count) / 3
Difference = Running mean − Homecage mean
```

**Empty section-bins contribute assumed zero; tissue coverage remains uncertain.** The mean always includes all three sections. Observed support counts detections, not verified tissue coverage. Each arm’s display is blank outside the union of observed PLA/ChAT bins across its six sections; complete-grid arithmetic remains in the numerical tables.

There are **three animals per condition**, six animals total, with a different HK1 and PFKP section per animal. The same animals appear in both arms. The twelve completed exports contain **3,010,776 objects: 310,024 PLA and 2,700,752 ChAT**. Interrupted job 4978 is audit-only and superseded by 5403; the earlier eight exports are not added as new samples.

Positions are bounding-box midpoint proxies using the unchanged prior transforms. These are reconstructed object maps, not fluorescence images or serial 3D anatomy. Counts are unsmoothed, uninterpolated and unnormalized; no statistical significance or causal effect is claimed. Physical-distance labels and scale bars are omitted as requested. See the [exact scientist clarifications](docs/scientist_clarifications_2026-11-14.md), [methods](docs/exploratory_methods.md), [workflow](docs/workflow.md) and [derived-data dictionary](docs/derived_data_dictionary.md).

## Recalculate the saved results

This is for analysts changing or checking calculations. It is separate from opening the app.

Run commands from the repository root with **Python 3.12 or newer**:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
```

On Windows, activate with `.venv\Scripts\activate` instead of `source`. The lock records the tested versions; `requirements.txt` provides broader version ranges when a platform needs different compatible packages.

**Recalculate from the included saved counts** — no raw CSVs or former-project folder required:

```bash
python scripts/execute_notebook.py TDP43_COMET_analysis.ipynb
```

This executes every current notebook cell, independently checks the three-section arithmetic, writes a new immutable result run, exports the figures, and rebuilds the app. The current report uses validated saved per-section counts by default. Allow several minutes for high-resolution exports. Reload the HTML after it finishes. The executor saves the notebook only after successful execution.

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

On PowerShell, set `$env:TDP43_RECOUNT_RAW="1"` before the execution command. Without that environment variable the notebook reuses saved counts. Full recounts check the raw input hashes, conserve counts across four grids and retain object/source provenance.

The original PDF’s strict tissue-mask pipeline remains a **separate historical specification**. Its missing-mask preflight messages do not block the scientist-authorized fixed-three comparison.

## Where files live

| Location | Purpose |
|---|---|
| [`outputs/app/index.html`](outputs/app/index.html) | Self-contained current offline app; open locally after downloading |
| [`TDP43_COMET_analysis.ipynb`](TDP43_COMET_analysis.ipynb) | Executed current scientific report |
| [`outputs/section_means/latest_run.json`](outputs/section_means/latest_run.json) | Selects the included current numerical run, bin CSVs, matrices and 600-DPI figures |
| [`outputs/exploratory_multiresolution/latest_run.json`](outputs/exploratory_multiresolution/latest_run.json) | Selects the included raw-validated count cache; its old variable-N summaries are historical |
| [`outputs/comet_core/detailed_review/`](outputs/comet_core/detailed_review/) | High-resolution alignment atlases and support maps |
| [`metadata/scientist_directed_mean_policy.json`](metadata/scientist_directed_mean_policy.json) | Current averaging rule and explicit coverage uncertainty |
| [`metadata/selected_section_metadata.csv`](metadata/selected_section_metadata.csv) | Animal, condition, section, source and duplicate relationships |
| [`outputs/validation.json`](outputs/validation.json), [`outputs/protocols/`](outputs/protocols/) | Recorded analysis verification and provenance |

Only a selected, verified result snapshot is committed. Superseded runs and local workspace-copy records stay on the analysis computer; new generated runs are ignored until deliberately selected for a future results update. Input paths recorded in historical provenance identify the original machine; cached reruns resolve the copied local snapshots.

The [earlier native supporting app](outputs/app/native_explorer.html) and [supporting notebook](TDP43_native_supporting_analysis.ipynb) concern the original eight-export intake. They are preserved as background, with a different scope from the current twelve-section comparison. The [former PLA–ChAT repository](https://github.com/adamwbrew/Bio_Data_Analysis) supplies methodological provenance, not expected results for these maps.
