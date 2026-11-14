# Verified research and method rationale

Sources checked 9 November 2026. These motivate methods and follow-up; they do not establish findings for this dataset. The PDF's initial count-map specification governs the implementation. No new biological mechanism, normalization, clustering or significance analysis is added.

| Verified primary source | Why it matters here | What it cannot establish here |
|---|---|---|
| Söderberg et al. (2006), *Nature Methods* 3:995–1000, [DOI 10.1038/nmeth947](https://www.nature.com/articles/nmeth947), [PMID 17072308](https://pubmed.ncbi.nlm.nih.gov/17072308/) | Introduces antibody-linked proximity detection with localized rolling-circle amplification in cells/tissues. Supports treating PLA as an assay with object-detection and specificity requirements. | Counts alone do not demonstrate a direct interaction, stoichiometry or flux in these inputs. |
| Barone et al. (2026), *Acta Neuropathologica* 151:26, [DOI 10.1007/s00401-026-02996-6](https://doi.org/10.1007/s00401-026-02996-6), [PMID 41838122](https://pubmed.ncbi.nlm.nih.gov/41838122/) | Reports TDP-43/HK1 mechanisms using disease models and complementary biochemical/metabolic experiments. Motivates retaining arm-specific questions and orthogonal validation. | Disease-model mechanisms and reported PFK findings cannot be transferred to an uncharacterized running/homecage study. |
| Manzo et al. (2019), *eLife* 8:e45114, [DOI 10.7554/eLife.45114](https://elifesciences.org/articles/45114), [PMID 31180318](https://pubmed.ncbi.nlm.nih.gov/31180318/) | Manipulates glycolysis in TDP-43 models, including Drosophila PFK. Motivates functional follow-up rather than interpreting spatial proximity as enzyme activity. | Fly PFK is not proof of mammalian PFKP interaction, nor an expected exercise effect. |
| Navikas et al. (2024), *Scientific Reports* 14:5025, [DOI 10.1038/s41598-024-55387-w](https://www.nature.com/articles/s41598-024-55387-w) | Demonstrates a COMET image-to-feature spatial workflow; supports inspecting segmentation and extraction provenance. | Its lung-cancer panel, masks, cell identities and analysis settings do not supply those of this experiment. |

## Official technical documentation

- [Shapely covers](https://shapely.readthedocs.io/en/stable/reference/shapely.covers.html) defines a predicate requiring no point of the bin to be outside the mask. Apply it to the full bin polygon, preserving mask holes; reject invalid geometry. Exact shared boundary is allowed; exterior slivers are not rounded away. No buffer, convex hull or percentage tolerance substitutes for the PDF rule.
- [NumPy histogram2d](https://numpy.org/doc/stable/reference/generated/numpy.histogram2d.html) documents explicit edges and raw counts. Matrix axis order must be recorded and checked against visual X/Y orientation. Density mode would change the requested count estimand and is not used.
- [COMET manufacturer documentation](https://lunaphore.com/products/comet/) describes OME-TIFF output and compatible analysis software. This does not establish that source microscopy pixels, calibration, acquisition settings or tissue masks were supplied locally.

## Interpretation of the requested method

The strict mask test prevents missing tissue from masquerading as low signal. Keeping fully covered empty bins as zeros prevents selective omission of low-count regions. Per-section means avoid allowing sections with more objects to receive more weight. Coverage maps reveal where the contributing sections change across space; their counts are not confidence intervals or independent animal counts.

The estimator remains descriptive and sensitive to staining, imaging, segmentation, bin dimensions, section thickness, anatomical level and which sections contribute. A difference can reflect these factors as well as biological signal. If several sections belong to one animal, section weighting can overweight that animal; document this before any later inferential extension. No machine learning is justified for the initial requested output.

## Concrete next scientific actions

Supply the already accepted transforms, tissue masks, alignment-check source, object-coordinate definition and explicit sample mapping. Review paired original channels and segmentation alongside any eventual high/low difference regions. Confirm assay controls and acquisition comparability before interpreting them. Plan functional or biochemical validation only after the actual experiment and intended decision are clarified.
