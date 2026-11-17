# scifact: BGE-M3 (All) vs RRF (BM25 + MiniLM)

nDCG@10: BGE-M3 (All) 0.692, RRF (BM25 + MiniLM) 0.718 (300 queries).

| Per query (Δ beyond ±0.1) | Queries | Mean lexical overlap |
|---|:-:|:-:|
| BGE-M3 (All) clearly better | 40 | 47% |
| No clear difference | 204 | |
| RRF (BM25 + MiniLM) clearly better | 56 | 41% |

Lexical overlap = share of the query words (> 3 letters) found in the closest relevant document.

## BGE-M3 (All) clearly better

### Query 1221: Δ nDCG@10 +1.00 (BGE-M3 (All) 1.00, RRF (BM25 + MiniLM) 0.00)

> The genomic aberrations found in matasteses are very similar to those found in the primary tumor.

- Relevant documents: 1. First relevant at rank 1 (BGE-M3 (All)) vs 29 (RRF (BM25 + MiniLM))
- Lexical overlap: 22% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Evolution of metastasis revealed by mutational landscapes of chemical… | 1 | Diverse tumorigenic pathways in ovarian serous carcinoma. |  |
| 2 | Pancreatic cancer genomes reveal aberrations in axon guidance pathway… |  | Intratumor heterogeneity and branched evolution revealed by multiregi… |  |
| 3 | High prevalence of evolutionarily conserved and species-specific geno… |  | Aberrant luminal progenitors as the candidate target population for b… |  |
| 4 | Comprehensive genomic characterization defines human glioblastoma gen… |  | Array-based Comparative Genomic Hybridization for Genome-Wide Screeni… |  |
| 5 | Deregulated DNA polymerase beta induces chromosome instability and tu… |  | PHC3, a component of the hPRC-H complex, associates with E2F6 during … |  |

### Query 212: Δ nDCG@10 +0.64 (BGE-M3 (All) 1.00, RRF (BM25 + MiniLM) 0.36)

> CR is associated with higher methylation age.

- Relevant documents: 1. First relevant at rank 1 (BGE-M3 (All)) vs 6 (RRF (BM25 + MiniLM))
- Lexical overlap: 75% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Caloric restriction delays age-related methylation drift | 1 | DNA methylation and healthy human aging |  |
| 2 | Age‐associated microRNA expression in human peripheral blood is assoc… |  | Diverse interventions that extend mouse lifespan suppress shared age-… |  |
| 3 | DNA methylation and healthy human aging |  | Widespread and tissue specific age-related DNA methylation changes in… |  |
| 4 | Widespread and tissue specific age-related DNA methylation changes in… |  | Age-Associated Sperm DNA Methylation Alterations: Possible Implicatio… |  |
| 5 | DNA methylation age of human tissues and cell types |  | DNA methylation age of human tissues and cell types |  |

### Query 644: Δ nDCG@10 +0.64 (BGE-M3 (All) 1.00, RRF (BM25 + MiniLM) 0.36)

> Insulin increases risk of severe kidney failure.

- Relevant documents: 1. First relevant at rank 1 (BGE-M3 (All)) vs 6 (RRF (BM25 + MiniLM))
- Lexical overlap: 83% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Diabetes treatments and risk of amputation, blindness, severe kidney … | 1 | Metabolic syndrome as a risk factor for diabetes. |  |
| 2 | Acute kidney injury and chronic kidney disease: an integrated clinica… |  | Mechanisms linking obesity to insulin resistance and type 2 diabetes |  |
| 3 | Oxidative stress in renal dysfunction: mechanisms, clinical sequelae … |  | QT and QTc dispersion are accurate predictors of cardiac death in new… |  |
| 4 | Obesity, type 2 diabetes, and cancer: the insulin and IGF connection. |  | Obesity, type 2 diabetes, and cancer: the insulin and IGF connection. |  |
| 5 | Mechanisms linking obesity to insulin resistance and type 2 diabetes |  | Acute kidney injury and chronic kidney disease: an integrated clinica… |  |

### Query 1180: Δ nDCG@10 +0.61 (BGE-M3 (All) 1.00, RRF (BM25 + MiniLM) 0.39)

> The PRR MDA5 is a sensor of RNA virus infection.

- Relevant documents: 1. First relevant at rank 1 (BGE-M3 (All)) vs 5 (RRF (BM25 + MiniLM))
- Lexical overlap: 75% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Immune signaling by RIG-I-like receptors. | 1 | RIG-I-mediated antiviral responses to single-stranded RNA bearing 5'-… |  |
| 2 | RIG-I-mediated antiviral responses to single-stranded RNA bearing 5'-… |  | Ribose 2′-O-methylation provides a molecular signature for the distin… |  |
| 3 | Ribose 2′-O-methylation provides a molecular signature for the distin… |  | A Conserved Histidine in the RNA Sensor RIG-I Controls Immune Toleran… |  |
| 4 | Role of chicken melanoma differentiation-associated gene 5 in inducti… |  | Alphavirus-derived small RNAs modulate pathogenesis in disease vector… |  |
| 5 | Cytosolic viral sensor RIG-I is a 5'-triphosphate-dependent transloca… |  | Immune signaling by RIG-I-like receptors. | 1 |

### Query 1024: Δ nDCG@10 +0.61 (BGE-M3 (All) 1.00, RRF (BM25 + MiniLM) 0.39)

> Recurrent mutations occur frequently within CTCF anchor sites adjacent to oncogenes.

- Relevant documents: 1. First relevant at rank 1 (BGE-M3 (All)) vs 5 (RRF (BM25 + MiniLM))
- Lexical overlap: 50% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | 3D Chromosome Regulatory Landscape of Human Pluripotent Cells. | 1 | Characterization of constitutive CTCF/cohesin loci: a possible role i… |  |
| 2 | Characterization of constitutive CTCF/cohesin loci: a possible role i… |  | Specific sites in the C terminus of CTCF interact with the SA2 subuni… |  |
| 3 | Colorectal Cancers from Distinct Ancestral Populations Show Variation… |  | Colorectal Cancers from Distinct Ancestral Populations Show Variation… |  |
| 4 | Specific sites in the C terminus of CTCF interact with the SA2 subuni… |  | Reverse engineering of TLX oncogenic transcriptional networks identif… |  |
| 5 | Replication stress activates DNA repair synthesis in mitosis |  | 3D Chromosome Regulatory Landscape of Human Pluripotent Cells. | 1 |

## RRF (BM25 + MiniLM) clearly better

### Query 659: Δ nDCG@10 -1.00 (BGE-M3 (All) 0.00, RRF (BM25 + MiniLM) 1.00)

> Ivermectin is used to treat lymphatic filariasis.

- Relevant documents: 1. First relevant at rank >100 (BGE-M3 (All)) vs 1 (RRF (BM25 + MiniLM))
- Lexical overlap: 40% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Wedelolactone exhibits anti-fibrotic effects on human hepatic stellat… |  | “Rapid-Impact Interventions”: How a Policy of Integrated Control for … | 1 |
| 2 | Metformin reverses established lung fibrosis in a bleomycin model |  | Role of gut commensal microflora in the development of experimental a… |  |
| 3 | Imiquimod 5% cream for the treatment of superficial basal cell carcin… |  | An IL-13 inhibitor blocks the development of hepatic fibrosis during … |  |
| 4 | Oral fingolimod (FTY720) for relapsing multiple sclerosis. |  | Efficacy of the 6-month thrice-weekly regimen in the treatment of new… |  |
| 5 | Interaction of cytosine arabinoside and lovastatin in human leukemia … |  | Resazurin microtiter assay plate: simple and inexpensive method for d… |  |

### Query 94: Δ nDCG@10 -1.00 (BGE-M3 (All) 0.00, RRF (BM25 + MiniLM) 1.00)

> Albendazole is used to treat lymphatic filariasis.

- Relevant documents: 1. First relevant at rank 27 (BGE-M3 (All)) vs 1 (RRF (BM25 + MiniLM))
- Lexical overlap: 40% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Emerging role of bisphosphonates in the clinic--antitumor activity an… |  | “Rapid-Impact Interventions”: How a Policy of Integrated Control for … | 1 |
| 2 | Amylase, Lipase, and Acute Pancreatitis in People With Type 2 Diabete… |  | Reduction in skin grafting after the introduction of hydrofiber dress… |  |
| 3 | Inflammatory monocyte/macrophage modulation by liposome-entrapped spi… |  | Combining indoor residual spraying and insecticide-treated nets for m… |  |
| 4 | Interaction of cytosine arabinoside and lovastatin in human leukemia … |  | Oral ciclopirox olamine displays biological activity in a phase I stu… |  |
| 5 | Optimal therapy for reduction of lipoprotein(a). |  | Efficacy of the 6-month thrice-weekly regimen in the treatment of new… |  |

### Query 185: Δ nDCG@10 -0.71 (BGE-M3 (All) 0.29, RRF (BM25 + MiniLM) 1.00)

> Breast cancer development is determined exclusively by genetic factors.

- Relevant documents: 1. First relevant at rank 10 (BGE-M3 (All)) vs 1 (RRF (BM25 + MiniLM))
- Lexical overlap: 57% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Risk for breast cancer development determined by mammographic parench… |  | Gene–environment interactions in 7610 women with breast cancer: prosp… | 1 |
| 2 | Role of birthweight in the etiology of breast cancer. |  | Clinical and pathologic characteristics of patients with BRCA-positiv… |  |
| 3 | Management of women who have a genetic predisposition for breast canc… |  | Risk for breast cancer development determined by mammographic parench… |  |
| 4 | Estrogens, progestogens, normal breast cell proliferation, and breast… |  | Intrinsic genetic characteristics determine tumor-modifying capacity … |  |
| 5 | Clinical and pathologic characteristics of patients with BRCA-positiv… |  | Management of women who have a genetic predisposition for breast canc… |  |

### Query 478: Δ nDCG@10 -0.68 (BGE-M3 (All) 0.32, RRF (BM25 + MiniLM) 1.00)

> Golli-deficient T-cells prefer to differentiate into an anergic phenotype in the adaptive immune response when there are increased levels of Ca2+ in the cytosol.

- Relevant documents: 1. First relevant at rank 8 (BGE-M3 (All)) vs 1 (RRF (BM25 + MiniLM))
- Lexical overlap: 19% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Memory CD4+ T cells induce innate responses independently of pathogen |  | Golli protein negatively regulates store depletion-induced calcium in… | 1 |
| 2 | Differentiation of effector CD4 T cell populations (*). |  | Expression of Golli mRNA during development in primary immune lymphoi… |  |
| 3 | The frequency and immunodominance of islet-specific CD8+ T-cell respo… |  | Invariant natural killer T cells: bridging innate and adaptive immuni… |  |
| 4 | Antigen availability determines CD8⁺ T cell-dendritic cell interactio… |  | Thymic expression of the golli-myelin basic protein gene in the SJL/J… |  |
| 5 | Frontrunners of T cell activation: Initial, localized Ca2+ signals me… |  | Functional analysis via standardized whole-blood stimulation systems … |  |

### Query 1278: Δ nDCG@10 -0.68 (BGE-M3 (All) 0.32, RRF (BM25 + MiniLM) 1.00)

> The treatment of cancer patients with co-IR blockade does not cause any adverse autoimmune events.

- Relevant documents: 1. First relevant at rank 8 (BGE-M3 (All)) vs 1 (RRF (BM25 + MiniLM))
- Lexical overlap: 30% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Beyond melanoma: inhibiting the PD-1/PD-L1 pathway in solid tumors. |  | Is autoimmunity the Achilles' heel of cancer immunotherapy? | 1 |
| 2 | Immunotherapy of metastatic kidney cancer. |  | In vitro characterization of the anti-PD-1 antibody nivolumab, BMS-93… |  |
| 3 | Radiation and Dual Checkpoint Blockade Activates Non-Redundant Immune… |  | Beyond melanoma: inhibiting the PD-1/PD-L1 pathway in solid tumors. |  |
| 4 | Combination cancer immunotherapies tailored to the tumour microenviro… |  | Immunotherapy of metastatic kidney cancer. |  |
| 5 | Key questions about the checkpoint blockade-are microRNAs an answer? |  | CD28 and ITK signals regulate autoreactive T cell trafficking |  |
