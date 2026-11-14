# COMET spatial PLA analysis: technical handoff requirements

Updated 14 November 2026. Audience: analysis developers and the imaging analyst.

## Current authority and work

The [14 November scientist clarifications](scientist_clarifications_2026-11-14.md) supersede the earlier request list where they change the requested analysis. Current work uses the selected twelve completed sections and their unchanged saved alignment, with HK1 and PFKP processed separately. There are three animal sections per condition in each arm; the same animals occur in both arms.

- Produce detailed **2D** condition means and Running minus Homecage comparisons. Preserve the source identities and fixed transforms. Do not refit alignment or reopen anatomical approval.
- Do not require original images or tissue outlines as conditions for the current requested analysis. Do not infer new tissue masks from detections.
- Treat the scientist's stated anatomical comparability as the working context. Do not claim that numerical alignment establishes additional anatomical correspondence.
- Omit physical-distance labels and scale bars. Do not invent calibration, measured serial depth or physical 3D anatomy.
- Preserve the recorded object-position definition and the distinction between bounding-box midpoints and measured segmentation centroids. Earlier centroid/export requests below are historical documentation, not another current gate.
- The final user instruction is: **“Average all three, treating empty section-bins as zero; label coverage as uncertain”.** For each condition and arm, sum the three selected section PLA counts and divide by three at every shared bin; then calculate Running minus Homecage. Empty PLA section-bins contribute zero, regardless of ChAT or all-object occupancy. There are no pending scientist questions or input gates for this agreed method.
- The averaging denominator is always three. It is not a verified tissue-coverage count. Label coverage as uncertain; do not claim that zero counts establish tissue presence or that all three section masks contain the bin. Keep observed-object support, if displayed, a separately named diagnostic. Preserve earlier observed-support outputs as historical results rather than relabeling them as the newly selected condition mean.

## Relation to the original PDF

The original PDF p. 1, sections 3-4 requires existing masks, 100% bin containment, covered zero-PLA bins and a denominator equal to the number of mask-valid sections. PDF p. 2 requires the corresponding tissue-validity and coverage matrices to be retained. Those rules remain the definition of the archived strict-mask workflow. They have not been validated on this dataset because the actual masks are not available.

The current mask-free request is a protocol clarification/change, not evidence that the original mask test can be performed from points alone. Label the selected denominator and support definition accurately in figures, tables and saved parameters. An observed-detection support count must not be called verified full-bin tissue coverage. The selected fixed three-section average includes empty section-bins as zero and always divides by three, with coverage uncertainty disclosed. Retain the original PDF and historical workflow for provenance; do not use their former missing-input requests to block the current authorized task.

## Historical checklist retained for provenance

The material below records the earlier 12 November investigation and technical handoff requirements. **Its questions and missing-input gates are superseded for the current requested analysis. Do not send this section as an active scientist questionnaire.** It remains useful if the original strict mask-based workflow is specifically requested in future, and preserves the section lookup and scientific limitations.

---

# COMET spatial PLA analysis: technical handoff requirements

Audience: the analysis developers and imaging/HALO analyst. Updated 12 November 2026.

**This is an internal technical checklist, not the question list to send to scientists.** The scientist-facing questions are in [scientist_questions.md](scientist_questions.md). Scientists can identify the biological intent, existing records, original images and the appropriate imaging contact. Our team will handle file inspection, faithful conversion, coordinate mapping, source-object linkage and software validation with that imaging analyst. These implementation details are not a survey for the experimental scientists.

The detailed previous checklist is retained below so its requirements and section lookup remain available. Its requests for exports, coordinate definitions and grid details are work items for the technical handoff. Existing scientific requirements are preserved; this document adds no new cohort selection, alignment approval or mask-inference permission.

---

## Preserved detailed checklist

Prepared 12 November 2026. Please return file locations or exports alongside the answers below. If an asset was not retained, record that explicitly so we can decide the appropriate next step.

**The first three requests resolve the missing inputs for the PDF's strict analysis.** The later questions improve interpretation and source-image review; they do not prevent viewing the calculated exploratory maps.

### Short agenda to send ahead

1. Where are the original tissue masks/analysis ROIs, including holes and exclusions, for each selected section?
2. What coordinate mapping and calibration relate those masks, object exports and source images?
3. Can measured object centroids be exported, or is a documented bounding-box midpoint approximation intended?
4. What anatomical or physical scale should the grid resolve, and is an accepted grid already recorded?
5. What explains sparse or unequal detected-object support, and which regions need review first?
6. Where are the original fluorescence channels, segmentation overlays and matching image/settings metadata?
7. Did condition coincide with staining, acquisition, composite placement or processing batch?
8. What anatomical levels, orientation, section thickness and missing regions are documented?
9. Which treatment records and PLA/probe/antibody/imaging controls define this comparison?
10. What scientific decision or followup should the maps guide?

The detailed requests, reasons, answer spaces and section lookup below can accompany that agenda. The app now offers exploratory 1,000-, 500-, 250- and 100-export-unit grids; none is yet a verified physical scale. Their finer detail does not resolve the first three missing-input requests.

## What is already established

- The selected cohort is the former app's 12 completed sections from six animals: Homecage 21F, 23M and 24M; Running 22F, 21M and 22M. Each animal contributes one HK1 section and a different PFKP section. The same animals appear in both arms, giving three biological replicates per condition, not six independent replicates per condition.
- All 13 newly supplied expanded CSVs match the recorded historical source hashes. Twelve are primary; interrupted job 4978 is retained for audit and replaced by completed job 5403. The eight alternative exports in `Initial Data` are not added as new sections or animals.
- The former app's saved coordinate transforms are recovered and reused unchanged. Its alignment-check figure has been reproduced without refitting. We are not requesting a new alignment or another approval of those transforms. Please identify a correction only if the recorded section mapping or intended saved version is wrong.
- Calculated exploratory difference maps and observed-object support maps are available. Their positions are bounding-box midpoints, and their support rule is at least one detected PLA or ChAT object in a bin. These are not the strict tissue-mask results. The user authorized this exploratory version separately; [exploratory_methods.md](exploratory_methods.md) records its assumptions.

The required strict outputs remain: two separate Running minus Homecage mean-PLA-count maps, the reproduced alignment check, and four condition-by-arm valid-section coverage maps. The source is `COMET_Spatial_PLA_Heatmap_Codex_Instructions.pdf`, pp. 1-2. The strict rule counts a section only where its existing tissue mask contains the entire bin; a fully covered bin with no PLA contributes zero. A bin with missing tissue must not be assigned zero (p. 1, sections 1-4).

## Priority 1: inputs needed for the strict PDF maps

### 1. Where are the existing tissue-analysis masks or ROI boundaries for these 12 sections?

**Please locate or export the original geometry**, including ventricular cavities, tears, disconnected tissue and analysis exclusions. Does it define tissue actually eligible for this HALO analysis, or only the outer tissue edge? If tissue and analysis-ROI exclusions are stored separately, supply both and explain which regions were analyzed. Identify the source section, image, annotation name/version and any manual edits. If no such masks were saved, please say so and identify who can decide whether new mask creation is scientifically appropriate.

**Evidence and requirement:** the expanded folder contains 13 object-results CSVs and no mask sidecars. The `Analysis Region` field is a label, not polygon geometry. The former app's visible outlines are derived from detected objects; its cavity polygons are internal anchors. Neither provides full-bin tissue validity. PDF p. 1, section 3 requires existing masks and says not to infer coverage from PLA or create a replacement unless specifically requested.

**Files to return:** original HALO/project annotation exports or existing binary masks, mapped to the section table below. Preserve original formats and metadata; conversion can follow. GeoJSON Polygon/MultiPolygon with holes is directly useful. An existing raster needs its exact cell footprint and coordinate mapping. A screenshot or a point-cloud silhouette is insufficient.

**Unlocks:** per-section strict bin eligibility, valid tissue zeros, both condition means, the two strict difference maps and all four true tissue-coverage maps.

**Answer / file location / owner:** ______________________________

### 2. How do mask coordinates, object coordinates and the saved frame relate?

For each geometry source, please provide its **native or already-aligned frame, X/Y directions, units, image resolution level, pixel size, crop origin and any offsets**. For rasters, identify the mapping of pixel edges to coordinates, rather than only pixel-center positions. Confirm whether all sections share the same export-coordinate scale, and whether the geometry already received any transformation. Already-aligned masks must not be transformed again.

Please supply the source-image calibration or export documentation. The area-column label in square micrometers does not establish the X/Y coordinate scale. If physical calibration cannot be recovered, can a common object/mask export-coordinate scale be documented? That can support counts per common export-unit bin without claiming a micrometer resolution.

**Evidence and requirement:** current positions and saved transforms are in export units with unverified physical calibration. PDF p. 1, sections 2-3 requires objects, masks and identical grid boundaries in the same aligned space; conservative full-bin containment cannot be tested if their scales or origins differ.

**Files to return:** image/export calibration metadata and a per-mask coordinate description, linked to section IDs and the original image. **Unlocks:** correct mask placement and comparable bin footprints across all sections; a documented physical scale where available.

**Answer / file location / owner:** ______________________________

### 3. Are measured PLA-object centroids available, or should the strict first pass explicitly use bounding-box midpoints?

The current CSVs provide `XMin`, `XMax`, `YMin` and `YMax`. The exploratory version uses `x=(XMin+XMax)/2`, `y=(YMin+YMax)/2`. These positions are not measured segmentation centroids and can differ for irregular objects.

**Please provide either** measured centroid X/Y fields with their coordinate definition and section/source-file plus `Object Id` linkage, **or** a documented instruction accepting this midpoint approximation for the strict first pass. If centroids require a new export, preserve linkage to the existing segmentation, object class and source IDs; explain any changed detections or segmentation version.

**Requirement:** PDF p. 1, section 2 assigns each PLA object once using its aligned centroid. The midpoint approximation is currently authorized for the separate exploratory maps; that does not silently amend the strict centroid requirement. **Unlocks:** a resolved object-position definition and auditable per-section PLA counts on the common grid.

**Answer / centroid export or intended definition:** ______________________________

## Priority 2: interpretation, spatial scale and source review

These followups do not introduce new gates, realignment or statistical tests. Where information is already recorded, a file or protocol reference is enough.

| Question to answer | Evidence or context | What the answer enables |
|---|---|---|
| **4. Is there an existing accepted common grid? If so, provide its exact X/Y edges and bin dimensions. Otherwise, what anatomical scale is the first-pass map intended to resolve?** | The recorded fallback is 1,000 by 1,000 export-unit bins, 25 X bins by 24 Y bins, chosen before the contrast. PDF p. 1, section 2 permits a configurable recorded grid if none exists. This default can remain while a scientific preference is considered; do not select resolution to favor an effect. | Reuse of the intended grid, or a scientifically motivated later resolution check. Physical-scale interpretation still needs question 2. |
| **5. What explains sparse or unequal observed support: actual tissue edges/holes, analysis-ROI exclusions, ChAT scarcity, acquisition/segmentation failures or incomplete capture? Which locations should receive source-image review first?** | Exploratory eligibility depends on detecting any PLA or ChAT object. A ChAT-only bin contributes zero PLA, but a bin with neither class has unknown coverage. PLA itself can make a section eligible, so the denominator can depend on signal and differ between conditions. Existing one/two/three-section support views are descriptive checks; even three observed sections do not prove full-bin tissue coverage. The strict PDF requires at least one mask-valid section in each condition (p. 1, section 3). | Interpretation of denominator changes and targeted QC without treating observed support as a tissue mask. Supply the actual masks to resolve tissue eligibility. |
| **6. Where are the original fluorescence channels, image metadata and segmentation/object overlays for the selected sections? Can selected native-coordinate review windows be opened against the same image/version?** | CSV `Image Location` values point to Windows `H:` TIFF paths; those pixels were not supplied with the object tables. Reconstructed midpoint maps are not microscopy. The latest exploratory run includes source-coordinate review windows. | Checks for genuine PLA puncta, ChAT context, merged/split detections, background, edge artifacts and the accuracy of midpoint locations. Return image access locations, channel identities, resolution/crop mapping and relevant HALO algorithm/settings exports. |
| **7. Did condition coincide with staining, imaging, slide/composite placement or processing batch? How were source composites assembled and analyzed?** | The archived analysis of these matched exports flagged Running at lower source-image X and Homecage at higher X. That layout is a provenance concern, not proof of bias; a post-detection coordinate translation alone cannot alter object association. Shared image IDs do not establish independent pairing or remove confounding. | An assessment of acquisition/processing alternatives to biology. Provide per-section staining batch, slide/image position, acquisition date/settings, exposure/gain, preprocessing/background subtraction and segmentation settings/version, including manual changes. |
| **8. What anatomical region and section level does each sample represent, and are levels comparable within each arm and across arms?** | Saved alignment preserves the former coordinates; it does not establish equivalent section levels or cross-arm anatomical homology. HK1 and PFKP use different physical sections and separate 21F reference origins. Exploded-stack spacing is a display control, not measured depth. | Appropriate anatomical labels and interpretation of locations. Provide section level/thickness, orientation, serial order or physical Z if known, and known tears or missing regions. This is contextual documentation, not a request to refit alignment or invent depth. |
| **9. What animal/treatment and assay-control records define the comparison?** | The six-animal condition assignment is settled, but condition labels alone do not record exposure, timing or assay specificity. PLA proximity/association is not by itself direct binding or metabolic flux. | Boundaries on biological claims and useful followup. Provide animal background (species, strain/genotype, age/sex), Running protocol and timing to collection, treatment allocation and any exclusion history; identify PLA negative/positive, probe/antibody and imaging controls and their results. Additional controls need not be invented to calculate the descriptive first-pass maps. |
| **10. What scientific decision should these maps guide, and which observations would trigger a followup?** | The current deliverable is raw, unsmoothed mean PLA count per eligible bin, separately for HK1 and PFKP. PDF p. 2, section 5 excludes normalization and statistical tests in this version. Three animals per condition remain the biological sample size. | A focused review plan: for example, prioritize source-image QC or a specified anatomical region for an independently validated followup. State the intended question and practical next step without turning exploratory bin patterns into validated conclusions. |

## Section lookup for returned masks and metadata

Please fill the mask/ROI filename or source annotation for each physical section. If one file contains multiple section geometries, identify the corresponding annotation/region ID. Supply coordinate mapping alongside it (question 2).

| Section ID | Animal | Condition | PLA arm | Completed job | Existing mask/ROI file or annotation |
|---|---|---|---|---:|---|
| 21F_Hk1 | 21F | Homecage | HK1 | 4998 | __________________ |
| 23M_Hk1 | 23M | Homecage | HK1 | 5007 | __________________ |
| 24M_Hk1 | 24M | Homecage | HK1 | 5002 | __________________ |
| 22F_Hk1 | 22F | Running | HK1 | 4997 | __________________ |
| 21M_Hk1 | 21M | Running | HK1 | 5006 | __________________ |
| 22M_Hk1 | 22M | Running | HK1 | 5001 | __________________ |
| 21F_Pfkp | 21F | Homecage | PFKP | 5020 | __________________ |
| 23M_Pfkp | 23M | Homecage | PFKP | 5005 | __________________ |
| 24M_Pfkp | 24M | Homecage | PFKP | 5000 | __________________ |
| 22F_Pfkp | 22F | Running | PFKP | 5403 | __________________ |
| 21M_Pfkp | 21M | Running | PFKP | 5003 | __________________ |
| 22M_Pfkp | 22M | Running | PFKP | 4999 | __________________ |

Full source filenames, paths and hashes are in [selected_section_metadata.csv](../metadata/selected_section_metadata.csv); assignment and reuse provenance are in [cohort_selection.json](../metadata/cohort_selection.json). The saved reference is the former app's **Feature-aligned** view, with HK1/job 4998 and PFKP/job 5020 as separate references, X rightward and Y downward. Flag discrepancies against these records; settled identities and fixed transforms do not need to be supplied or approved again.

## Suggested return package

Return this completed question list, the existing mask/annotation files, a section-to-mask coordinate table, centroid export or written position-definition clarification, and links to the relevant image/protocol records. For each item, mark **provided**, **not retained**, or **owner/location identified**. Keep original inputs and versions intact.

Once the required inputs are resolved, the strict workflow will preserve the fixed alignment, test full-bin inclusion including holes and boundary slivers, retain valid zero-PLA bins, and save the requested means, differences, valid-section N and per-section validity with provenance (PDF p. 2, sections 6-7). It will not convert exploratory detection support into a tissue mask.
