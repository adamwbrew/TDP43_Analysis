# COMET PDF: acceptance checklist for the three core views

**Separate exploratory branch:** the user has authorized midpoint/object-support maps, now calculated in the main report/app. They do not satisfy the strict tissue-mask checklist and are not marked as such. Their exact estimand and limits are in `exploratory_methods.md`.

The two-page [instruction PDF](../COMET_Spatial_PLA_Heatmap_Codex_Instructions.pdf) defines the requested initial analysis. Its outputs are two separate Running − Homecage difference maps, the same prior alignment-check figure, and four condition-specific section-coverage maps. Grouping these into three viewer tabs does not change their scientific meaning. Native object maps and historical findings cannot substitute for these outputs.

| Core view | PDF requirements | What the display means | Acceptance evidence |
|---|---|---|---|
| **Difference heatmaps**: TDP43–HK1 and TDP43–PFKP | Page 1 §§1–4; page 2 §§5–7. Keep arms separate. Reuse the unchanged accepted transforms, orientation and reference. Use one recorded grid across every included section and condition. Assign each PLA centroid once, count within each section, and then average valid sections equally. | Each value is Running mean raw PLA count per bin minus Homecage mean raw PLA count per bin. Positive means more in Running; negative means fewer. It is neither a fraction nor a density, and it is not an animal-level statistical test. | Saved section counts and tissue-validity matrices reproduce each mean, each valid-section N and each displayed subtraction. The page-2 example 3,5,4 versus 7,8,9 gives +4. Both arms share one zero-centered diverging scale with identical symmetric limits. Missing bins remain visually distinct from true zero difference. Use the exact color-bar wording required by page 2 §5. |
| **Alignment check**: the previously accepted figure reproduced for inspection | Page 1 §§1–3; page 2 §7. Reuse numerical transforms, anatomical orientation, reference and existing masks. Never realign. Confirm by inspection that the same figure matches the prior accepted alignment. | An unchanged-transform overlay is a way to inspect the supplied correspondence. It cannot establish correspondence or replace the previously accepted figure merely because it looks plausible. Object coordinates are reconstructed detections, not original fluorescence pixels. | Retain the reference figure and provenance plus the original plotting recipe: layers, layout, axis limits, orientation, sampling and styling where needed for reproduction. Retain native coordinates and apply only the supplied fixed transform to centroids and masks. A generic new overlay must be labeled an inspection aid until exact reproduction is established. This is the requested comparison with existing evidence, not a new blanket approval workflow. |
| **Coverage**: HK1/Running, HK1/Homecage, PFKP/Running and PFKP/Homecage | Page 1 §§1,3–4; page 2 §§6–7. A section contributes only if 100% of the entire bin lies within its own existing tissue mask. Exclude even slightly partial bins. Preserve holes; treat raster cells by full footprints conservatively. | N is the number of valid physical tissue sections contributing to that condition's mean at that bin. It is not the number of animals, detections or nonempty signal bins. A fully covered section with zero PLA still increases N and contributes count 0. | Four N matrices match the sum of individual section-validity matrices. Difference is displayable only where N≥1 independently in both conditions. Section-ID hover lists valid contributing sections and their raw counts; excluded sections are identified as excluded, never inserted as zero. |

The shared infrastructure must preserve source-file IDs and hashes, section IDs, animal IDs, physical-section relationships, PLA type, condition, centroid definition, exact selection criteria, masks, numerical fixed transforms, units, grid edges and display orientation (page 2 §§6–7). Explicit source documentation may establish these facts; filenames and old conclusions cannot. The supplied PDF requests centroids. A proxy needs an explicit applicable scientific amendment rather than a silent bounding-box fallback.

The PDF permits reusing an existing grid or defining configurable recorded bin dimensions when no existing grid is available (page 1 §2). It does not require a new uniform-grid approval gate. The implementation accepts explicit increasing edge arrays shared across all sections; it never silently changes their boundaries.

The initial version must not smooth, interpolate, normalize or run statistical tests (page 2 §5). Changing a viewer filter cannot alter the saved scientific comparison unless the analyst deliberately runs a new documented analysis. In particular, preview sampling affects displayed coordinate points only; all selected objects enter the count verification.

## Current completion criteria

- [x] User-selected twelve-section cohort, six animals, condition/arm assignments and completed-versus-interrupted relationships are recorded; current raw copies match all source hashes.
- [x] All twelve numerical transforms and original orientation/reference are recovered and replayed unchanged.
- [x] The same prior alignment-check PNG is reproduced and compared with identical pixels and bytes; original proposal flags remain visible provenance.
- [x] One configurable shared 25 × 24 grid of 1,000 export-unit bins is recorded before any contrast, with rationale and no physical-scale claim.
- [ ] Existing tissue masks and their native/aligned coordinate mapping are available for all twelve sections.
- [ ] Measured centroids or clarification accepting the documented former midpoint proxy are supplied.
- [ ] Two difference maps and four coverage maps are computed from the selected raw objects using strict full-bin validity, with saved matrices reproducing every displayed value.

See `metadata/grid_parameters.json` for the initial grid and `docs/scientist_questions.md` for the two remaining input priorities. The PDF states that alignment was accepted; old snapshot flags do not create a new approval gate. Exact replay demonstrates reproduction, not biological correspondence.

Until the actual masks and position definition exist, difference and coverage views show precise blockers rather than synthetic maps, historical contrasts or zero-filled arrays. Software fixtures exercise arithmetic and geometry in temporary folders only.

## Viewer payload contract

`comet_spatial.core_view.build_core_view_payload` reads a selected immutable run and verifies its saved per-section counts against every saved object-provenance coordinate, then verifies the arm means, N and differences against those sections. It does not create a new alignment or mask. `outputs/core_view/payload.json` is the intended viewer sidecar.

The payload supplies shared grid edges and display directions; one symmetric difference color limit; separate HK1/PFKP matrices; per-section counts and tissue-validity for contribution hover; section/animal/condition/source provenance; and paired native/fixed-aligned coordinate previews. Mask outlines come only from recorded run geometry or existing masks whose hashes match. Any sampled object preview declares its method, limit and selected-object total. Numeric missing values are JSON `null`; a valid measured zero is `0`.

With no verified run, the payload has `status: "blocked"`, `grid: null`, `arms: {}` and unavailable core views. A completed numerical snapshot can have `status: "numerical_ready"` while its alignment reproduction remains unresolved. Those states must remain distinct in the viewer.
