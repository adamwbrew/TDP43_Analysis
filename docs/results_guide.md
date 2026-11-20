# Reading the current COMET spatial results

Open [the offline app](../outputs/app/index.html). The default PLA-count analysis averages **all three animal sections per condition**, treating empty section-bins as zero, then subtracts Homecage from Running. HK1 and PFKP remain separate. This follows the [14 November scientist clarification](scientist_clarifications_2026-11-14.md); coverage is uncertain and no further asset requests block the task.

The app offers **19 measurements and three comparisons**: the thirteen requested in the calculation-functions PDF, page 1, plus six complementary measurements added on 19 November. Use the measurement selector for counts, sizes, area, intensity or ChAT-associated PLA, and the comparison selector for signed difference, percent change or log2 fold change. These controls reuse the same detailed map, grids, alignment and point inspection. [The function guide](calculation_functions.md) gives the definitions and zero/missing rules.

The default is a detailed **100-export-unit** grid. Choose either condition mean or the selected comparison, then inspect the linked section contributions and full PLA midpoint positions. The 1,000-, 500- and 250-unit grids provide coarser views of the same counted objects. Smaller bins change counts and sparsity, so numerical magnitudes are not directly comparable across resolutions.

## The three visual families

| View | How to read it | What it supports and what remains uncertain |
|---|---|---|
| **Condition means and selected comparison** | For the default count, each condition is the sum of three section PLA counts divided by three. For other measurements, average defined section values equally, then compare conditions. Positive values indicate higher Running means and negative values higher Homecage means. A true comparison zero is the center of the diverging scale; undefined values are blank. Both arms share the selected symmetric linear comparison range. | A descriptive comparison with metric-specific units and missingness. Empty count/sum bins contribute assumed zero, while object means, percentiles and fractions can be undefined. Neither coverage nor acquisition equivalence is established by these calculations. |
| **Saved alignment and section inspection** | Compare individual sections at the same location and inspect their unchanged saved placement. Full PLA point positions remain available; the original six-panel alignment check is preserved. | Reproduction and inspection of fixed coordinate operations. The scientists consider the anatomical regions comparable for this comparison. Reconstructed positions remain bounding-box midpoints, and no serial 3D anatomy is claimed. |
| **Observed-support diagnostics** | The four condition-by-arm panels count sections with at least one exported PLA or ChAT object in a bin, from zero to three. Inspect the individual-section counts alongside them. | Detection support only. These maps neither determine the current denominator nor verify full tissue coverage. A support count of zero does not prove absent tissue, and three does not prove complete coverage. |

Each arm's plotted field includes bins with observed objects in any of its six sections. Bins outside that union are blank. The saved complete-grid tables retain the arithmetic values; this display boundary does not establish tissue presence or absence. A location with observations in only one condition can still show a difference because the other condition's three empty counts enter as zeros.

## Choose a measurement that answers the question

| Question | Useful selections | Read alongside it |
|---|---|---|
| Where are more PLA detections, or more detections above/below a size threshold? | PLA count, large PLA count, small PLA count | Section contributions, observed support and cutoff sensitivity |
| Does the detected size distribution differ? | Large PLA fraction, mean/median/90th-percentile PLA area | Measurement-defined section N and object counts; sparse bins can give unstable summaries |
| Is a change in total detected PLA area driven by object number or size? | Total PLA area alongside PLA count and mean area | All three maps; summed area alone does not identify the cause |
| Does exported PLA intensity differ? | Mean PLA intensity | Defined-section N and acquisition/staining context; intensity units are uncalibrated |
| Does exported ChAT association differ? | Associated PLA count/fraction, associated large PLA count, associated mean area | Total PLA count, associated-object counts and defined-section N |

Only ChAT is currently available for marker selection. Association comes from the flag on each PLA row, not from counting separate ChAT-class objects. The configurable area cutoff defaults to 0.1 in the column labeled µm²; calibration is unverified, so threshold categories are descriptive measurement categories rather than validated biological classes.

Counts and total areas keep empty section-bins at zero. Means, quantiles and fractions requiring objects are missing when the necessary objects are absent. Their condition mean uses only defined section values, with equal weight per section, and reports an N from 0 to 3. **Measurement-defined N and observed-support N answer different questions.** For example, a ChAT-only bin can have observed support but no defined PLA area mean. The mean of section medians is not a pooled median.

The comparison named `absolute_difference` is signed **Running minus Homecage**, with the selected measurement's units. Percent change uses Homecage as its denominator and is blank when that mean is zero; Running zero with positive Homecage gives -100%. Log2 fold change is blank unless both means are positive. No pseudocount makes undefined comparisons finite. A ratio can become extreme when the Homecage mean is small, so inspect the two means rather than ranking bins by color alone.

## What the default fine grid shows

For the preserved **PLA-count / signed-difference** calculation, the recorded 100-unit run contains the following displayed-bin summaries. These summaries do not describe every selectable measurement or ratio:

| Arm | Displayed bins | Running lower | Running higher | Equal means |
|---|---:|---:|---:|---:|
| HK1 | 29,708 | 14,859 | 6,943 | 7,906 |
| PFKP | 30,344 | 10,678 | 7,699 | 11,967 |

Negative differences occupy more displayed bins than positive differences in both arms under this chosen estimator. These are correlated spatial bins, not independent biological samples or significance tests. Their counts depend on resolution, display domain and the assumed-zero convention; they do not establish validated anatomical hotspots or causal exercise effects. Three animals per condition remain the biological sample size, and the same animals occur in both arms.

## Inspect, export and interpret

Select a bin or region to read both condition means, the selected comparison, its measurement-defined N and section contributions. Use full point detail to inspect the detections behind a pattern. A large contrast with low support or only one defined section deserves particular caution because unknown tissue coverage and sparse measurement sampling may contribute to it. The next scientific step is to assess whether a pattern is consistent across animals and meaningful for the experiment, not to treat a strong color as validation.

The saved figure library provides **600-DPI PNGs and SVG versions** for detailed maps. Full-range signed maps preserve the common symmetric scale. The default PLA-count presentation uses a labeled ±25 difference range and 0–25 mean range, with full-range restore; other measurements use their own units and scales. Additional contrast views explicitly disclose saturated bins; exact uncapped values remain in the matrices, CSVs and app. The three-column figures place Homecage mean, Running mean and their comparison together; condition means share a sequential range across both conditions and both arms. Saved representative figures document their settings; they do not cover every possible configurable cutoff.

Use [the base count-run pointer](../outputs/section_means/latest_run.json) or [the added calculation-run pointer](../outputs/calculation_functions/latest_run.json) to locate numerical results and figure/provenance records. The [attribute-cache pointer](../outputs/measurement_features/latest_run.json) records the added area, intensity and association data matched to the exact prior objects; count caches alone cannot recreate those attributes. Read [the original count methods](exploratory_methods.md) and [the added function guide](calculation_functions.md) for the appropriate arithmetic. Older observed-support-N count means remain historical and must not be substituted for the current fixed-three count results. The historical strict-mask calculation is distinct from the agreed mask-free analysis; this extension preserves the current domain and uncertain-coverage labels.

## Persistent spatial context and finer detail

The pale footprint and thin neutral outline remain visible independently of the selected measurement. They follow the original finest observed-object bins, preserve holes and disconnected regions, and are **not tissue masks**. Undefined values stay undefined inside this location context. Toggle the context to inspect colors alone.

The detailed window can rebin full-precision PLA coordinates at 100, 50, 25 or 10 exported units, without sampling, smoothing or interpolation. Small bins can have few objects and fewer defined sections; inspect the object dots and section contributions. The whole-field comparison retains its original four grids. Save exact vector SVG for arbitrary magnification, or the fixed 8,000-pixel-wide PNG for sharing. Export resolution improves sharpness; it does not add biological measurements.

For every file, the calculation equations and end-to-end flow diagrams, see the [repository appendix](appendix/README.md).
