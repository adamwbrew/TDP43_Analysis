# Derived-data dictionary: fixed-three condition means

Current authority: [14 November policy](../metadata/scientist_directed_mean_policy.json). The active run is selected by [outputs/section_means/latest_run.json](../outputs/section_means/latest_run.json). Earlier observed-N means retain their own historical method and must not be substituted for these fields.

The separate [raw dictionary](../metadata/data_dictionary.json) describes twenty exported columns and preserves ranges from the initial eight-export inventory. The derived fields below belong to the current twelve-section analysis. Arrays use row-major `[y,x]` indexing on identical edges for all sections at each resolution. Export-coordinate units are uncalibrated; no physical distances are implied.

## Counts, means and differences

| Field or concept | Definition | Representation and limits |
|---|---|---|
| Per-section `pla_counts` | Number of aligned PLA-class bounding-box midpoints assigned once to a section-bin | Nonnegative integer matrix; empty bins are 0 |
| Per-section `chat_counts` | Number of aligned ChAT-class midpoints in a section-bin | Nonnegative integer matrix; context/support only |
| `homecage_count_sum`, `running_count_sum` | Sum of the three selected section PLA counts for that condition | Nonnegative whole-valued arrays; NPZ may store these sums as floats |
| `homecage_mean`, `running_mean` | Corresponding three-section count sum divided by 3 | Fractional raw count per bin; not a percentage or area density |
| `difference` | Running mean minus Homecage mean | Signed floating-point count difference; full-grid arithmetic is retained in NPZ and bin CSV |
| `display_difference` | Difference restricted to the arm's plotting domain | Float with `NaN` outside the domain in NPZ |
| `raw_arithmetic_difference` | Full-grid difference preserved in the viewer payload | Includes numerical zeros outside the plotted domain |
| `section_denominator` / `mean_denominator_each_condition` | Number of sections used in each condition mean | Fixed integer 3 at every bin; not verified tissue N |

In the JSON viewer payload, plotted means and `difference` are `null` outside the display domain; JSON does not encode `NaN`. Saved NPZ mean/difference arrays and bin CSVs retain full-grid arithmetic values. Thus a plotted `null` is not a measured zero. Within the plotted field, zero means a numerical zero under the agreed assumed-zero policy; it does not demonstrate tissue presence.

## Observed support and coverage uncertainty

| Field or concept | Definition | Interpretation |
|---|---|---|
| Per-section `observed_support` | `pla_counts + chat_counts > 0` | A detected-object observation, not tissue coverage |
| `homecage_observed_section_n`, `running_observed_section_n` | Number of sections with observed support, from 0 to 3 | Diagnostic only; never a mean denominator |
| JSON `homecage_n`, `running_n`; CSV `homecage_observed_N`, `running_observed_N` | Names exposing those same observed-section counts | Preserve the diagnostic meaning despite the shorter aliases |
| `homecage_assumed_zero_section_n`, `running_assumed_zero_section_n` | 3 minus observed-section N | Number of completely object-empty section-bins assigned assumed zero; excludes ChAT-only bins, whose PLA count is also 0 |
| CSV `homecage_assumed_zero_sections`, `running_assumed_zero_sections` | CSV aliases for those assumed-zero diagnostics | A warning about unobserved positions, not proof of absent tissue |
| `observed_union` / CSV `display_domain` | At least one observed PLA or ChAT object in any of the arm's six sections | A plotting domain shared by its two conditions; not a tissue outline |
| `displayable` | Bin belongs to that observed union and has a finite calculated difference | Permits a whole-condition zero where only the other condition has observations |
| `tissue_coverage_known`, `coverage_verified`, `tissue_coverage_verified` | Explicit coverage-status fields in arrays, CSV or run metadata | False throughout this mask-free analysis; no 100% mask-containment claim |

## Provenance and figures

Section, physical-section, animal, condition, arm and source-file identifiers link counts to the twelve selected sources. Source rows and native/aligned midpoint positions are retained with the count predecessor and viewer payload. The current run records its source payload hash, fixed-three policy, unchanged transforms and arithmetic validation. All 310,024 selected PLA positions are retained; the points are exported detections, not original microscopy pixels.

Each resolution has its own counts and shared color limits. The default is 100 export units; 1,000, 500 and 250 are coarser grids on the same aligned field. The mean is always divided by 3 at every resolution. Scientific figure exports use 600-DPI PNG and SVG versions at 100 and 250 units. Contrast-limited images change only the displayed color range, disclose saturated values and retain uncapped numerical values.
