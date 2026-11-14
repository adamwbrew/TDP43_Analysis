# Reading the current COMET spatial results

Open [the offline app](../outputs/app/index.html). The current analysis averages **all three animal sections per condition**, treating empty section-bins as zero, then subtracts Homecage from Running. HK1 and PFKP remain separate. This follows the [14 November scientist clarification](scientist_clarifications_2026-11-14.md); coverage is uncertain and no further asset requests block the task.

The default is a detailed **100-export-unit** grid. Choose Homecage mean, Running mean or Running minus Homecage, then inspect the linked section contributions and full PLA midpoint positions. The 1,000-, 500- and 250-unit grids provide coarser views of the same counted objects. Smaller bins change counts and sparsity, so numerical magnitudes are not directly comparable across resolutions.

## The three visual families

| View | How to read it | What it supports and what remains uncertain |
|---|---|---|
| **Condition means and differences** | Each condition is the sum of three section PLA counts divided by three. Positive differences indicate higher Running means; negative differences indicate higher Homecage means. White denotes a numerical zero on the diverging scale. Both arms share the selected symmetric linear difference range. | A descriptive raw-count comparison under the agreed zero-fill convention. An empty bin contributes zero even if tissue presence is unknown. Counts are not corrected for tissue area, staining, acquisition or segmentation. |
| **Saved alignment and section inspection** | Compare individual sections at the same location and inspect their unchanged saved placement. Full PLA point positions remain available; the original six-panel alignment check is preserved. | Reproduction and inspection of fixed coordinate operations. The scientists consider the anatomical regions comparable for this comparison. Reconstructed positions remain bounding-box midpoints, and no serial 3D anatomy is claimed. |
| **Observed-support diagnostics** | The four condition-by-arm panels count sections with at least one exported PLA or ChAT object in a bin, from zero to three. Inspect the individual-section counts alongside them. | Detection support only. These maps neither determine the current denominator nor verify full tissue coverage. A support count of zero does not prove absent tissue, and three does not prove complete coverage. |

Each arm's plotted field includes bins with observed objects in any of its six sections. Bins outside that union are blank. The saved complete-grid tables retain the arithmetic values; this display boundary does not establish tissue presence or absence. A location with observations in only one condition can still show a difference because the other condition's three empty counts enter as zeros.

## What the default fine grid shows

The recorded 100-unit run contains the following displayed-bin summaries:

| Arm | Displayed bins | Running lower | Running higher | Equal means |
|---|---:|---:|---:|---:|
| HK1 | 29,708 | 14,859 | 6,943 | 7,906 |
| PFKP | 30,344 | 10,678 | 7,699 | 11,967 |

Negative differences occupy more displayed bins than positive differences in both arms under this chosen estimator. These are correlated spatial bins, not independent biological samples or significance tests. Their counts depend on resolution, display domain and the assumed-zero convention; they do not establish validated anatomical hotspots or causal exercise effects. Three animals per condition remain the biological sample size, and the same animals occur in both arms.

## Inspect, export and interpret

Select a bin or region to read both condition means, the difference and all section contributions. Use full point detail to inspect the detections behind a pattern. A large difference with low observed support deserves particular caution because unknown tissue coverage may contribute to it. The next scientific step is to assess whether a pattern is consistent across the three animals and meaningful for the experiment, not to treat a strong color as validation.

The saved figure library provides **600-DPI PNGs and SVG versions** for 100- and 250-unit maps. Full-range signed maps preserve the common symmetric scale. The app defaults to a labeled ±25 difference range and 0–25 mean range, with full-range restore. Additional contrast views explicitly disclose saturated bins; exact uncapped values remain in the matrices, CSVs and app. The three-column figure places Homecage mean, Running mean and their difference together; condition means share a sequential range across both conditions and both arms.

Use [the current run pointer](../outputs/section_means/latest_run.json) to locate its numerical matrices, bin tables, figure manifest, policy, source trace and validation. Read [the methods](exploratory_methods.md) for the exact arithmetic. Older observed-support-N means remain historical and must not be substituted for the current fixed-three results. The original PDF's strict-mask calculation is also a distinct historical specification; it is not a new prerequisite for this agreed analysis.
