# Scientist clarifications: 14 November 2026

Source: scientist feedback relayed by the user in this project chat on 14 November 2026, followed by the user's final averaging instruction. The quotations below preserve the supplied wording.

These later instructions are the current authority where they change earlier requirements. The current clarification is complete: no further scientist answers or missing assets are prerequisites for the agreed analysis.

## Exact answers and resulting scope

**Original images**

> I don’t think having the images would be beneficial. They are huge files but also the data based spatial images you’ve already generated show you can appropriately place the objects.

Consequence: proceed from the supplied object measurements and preserved source identities. Original microscopy is not a prerequisite for this task.

**Tissue outlines and excluded areas**

> I do not think the tissue outlines or excluded areas are needed for this analysis. The previous document includes information of how to count bins as zero as compared to not present

Consequence: retire the outline request as a current gate. Use the explicit final averaging rule below. Do not infer new tissue masks or claim full-bin tissue validity.

**Anatomical comparability and alignment**

> They have comparable anatomical regions. If you overlay the data and average using the previously done alignment that is sufficient.

Consequence: use the stated anatomical comparability and recovered fixed transforms. Do not request additional anatomical approval or refit registration.

**Distance labels and scale bars**

> We don’t need distance labels or scale bars for now

Consequence: omit those labels and bars. No calibration or physical resolution is invented.

**Section relationships and presentation**

> No there are no consecutive sections right now. The 3D construction is not needed. We just want to average across the 3 sections per condition and subtract the averages between conditions.

Consequence: center the results on detailed 2D condition means and differences. Do not construct a serial anatomical volume or interpret display spacing as measured depth.

**Final averaging instruction**

> Average all three, treating empty section-bins as zero; label coverage as uncertain

Consequence: average all three selected sections at every bin. Treat an empty section-bin as zero PLA count. Keep coverage uncertainty explicit. This resolves the last outstanding comparison choice.

## Recorded current method

The selected data are twelve completed physical sections from six animals: three Homecage animals and three Running animals, each represented by one HK1 section and a different PFKP section. The two arms remain separate; their animals are shared rather than independent replications.

For each condition and arm, assign each selected PLA object's recorded bounding-box midpoint once to the common grid after applying its unchanged saved transform. At each bin:

```text
Condition mean = (section 1 PLA count + section 2 PLA count + section 3 PLA count) / 3
Difference = Running condition mean − Homecage condition mean
```

Empty PLA section-bins contribute zero, whether or not ChAT detections are present. The mean never excludes a section merely because that bin lacks detections. The denominator of three describes the chosen averaging design; it is not the number of sections verified to contain the entire bin's tissue.

Label coverage as uncertain. A numerical zero under this convention does not distinguish absent PLA in analyzed tissue from absent or unobserved tissue. Observed-object support may remain a separately labeled diagnostic, but it must not replace the fixed denominator or be called verified tissue coverage.

Preserve the fixed alignment, arm separation, common grid, direction of subtraction, shared linear zero-centered symmetric difference scales, unsmoothed raw counts and traceable saved results. Positions remain bounding-box midpoints, a reconstructed proxy rather than measured segmentation centroids. No new centroid-export or calibration request is introduced as a gate.

## Relation to the original PDF and previous outputs

The unchanged two-page PDF was rechecked. Page 1, section 3 defines a section as valid only when its existing tissue mask contains 100% of a bin; it includes covered zero-PLA bins and excludes missing tissue. Section 4 divides by the number of mask-valid sections. Page 2 requires the corresponding saved means, differences, section counts and per-section validity.

Those instructions distinguish zero from missing tissue when mask eligibility is known. They do not establish those cases from an empty object-table location alone. The later instructions explicitly select a different mask-free, fixed-three-section averaging convention. This is an authorized protocol change, not evidence that the original 100% tissue-containment test was performed or satisfied.

Earlier exploratory outputs used an observed-support denominator: sections with at least one PLA or ChAT object in a bin. Preserve their recorded provenance, but do not present that estimator as the newly selected condition average. Save new outputs with the fixed-three denominator and its coverage limitation clearly recorded.

The [technical handoff record](technical_handoff_requirements.md) retains the older strict-mask requirements as historical documentation. Those former requests must not block the current authorized analysis or reopen questions about images, outlines, anatomical approval, distance calibration or serial 3D data.
