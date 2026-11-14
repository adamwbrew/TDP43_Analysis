# Read-only input inventory

This is an input audit, not a biological result.

- CSV files: 8; bytes: 710,775,898.
- Exported rows, including possible repeated analyses: 2,146,037.
- Files byte-identical to historical reference CSVs (SHA-256): 8/8.
- Filenames and embedded region labels are observations, not approved new-study metadata.
- Full column counts, types, missingness, categorical counts and numeric ranges are in column_profiles.csv and file_audit.json.

| File | Job token | Exported region text | Rows | PLA-label rows | ChAT-label rows |
|---|---|---|---:|---:|---:|
| input_001 | 4594 | 22M_Pfkp-TDP43 PLA | 186,343 | 9,112 | 177,231 |
| input_002 | 4595 | 24M_Pfkp-TDP43 PLA | 297,584 | 7,999 | 289,585 |
| input_003 | 4596 | 22M_Hk1-TDP43 PLA | 238,084 | 15,282 | 222,802 |
| input_004 | 4597 | 24M_Hk1-TDP43 PLA | 356,745 | 43,918 | 312,827 |
| input_005 | 4999 | 22M_TDP43-Pfkp_tight | 184,684 | 8,412 | 176,272 |
| input_006 | 5000 | 24M_TDP43-Pfkp_tight | 295,677 | 7,733 | 287,944 |
| input_007 | 5001 | 22M_TDP43-Hk1_tight | 237,144 | 14,984 | 222,160 |
| input_008 | 5002 | 24M_TDP43-Hk1_tight | 349,776 | 41,237 | 308,539 |

## What the evidence demonstrates

SHA-256 agreement establishes byte-identical copies of the files in the reference locations. It does not establish that the new experiment has the same scientific assignments or that the instructions authorize reusing those assignments. Embedded label text and object class labels are preserved without upgrading them to validated biological identity.

Within-input overlap compares full exported rows and, separately, all exported values except Analysis Region and Object Id. Shared measurement signatures show exact agreement of exported image path, algorithm, type, measurements and boxes. Repeated measurement values can occur; these signatures are evidence of overlap, not a validated biological-object matching procedure. Fractions use distinct signatures, not row multiplicities. Do not pool candidate reruns as independent sections/animals.

## Analysis blockers

- No scientist-approved mapping of these exports to the new experiment, animals, conditions, PLA arms, physical sections and repeated analyses.
- No centroid fields are supplied; the requested aligned-centroid definition is unresolved. Historical bounding-box midpoint proxies require explicit scientific clarification before use.
- No approved alignment transforms/reference anatomy, aligned tissue masks, coordinate calibration or verified common grid supplied in the inventoried data directory.
- Byte-identical historical copies and overlapping analyses are documented; current section mapping and ROI/rerun inclusion resolution remain needed.

## Provenance and reruns

Source files were opened read-only. No source files were moved or edited. The command records complete SHA-256 hashes; row parsing uses Python's CSV reader with UTF-8 BOM handling. Numeric ranges describe exported values; header units are not calibration validation. UTC timestamps are execution provenance. Existing metadata/sample_metadata.csv is preserved on rerun; refreshed observed suggestions are written to outputs/inventory/sample_metadata_observed.csv.
