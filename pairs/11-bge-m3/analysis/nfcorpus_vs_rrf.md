# nfcorpus: BGE-M3 (All) vs RRF (BM25 + MiniLM)

nDCG@10: BGE-M3 (All) 0.336, RRF (BM25 + MiniLM) 0.342 (323 queries).

| Per query (Δ beyond ±0.1) | Queries | Mean lexical overlap |
|---|:-:|:-:|
| BGE-M3 (All) clearly better | 49 | 64% |
| No clear difference | 228 | |
| RRF (BM25 + MiniLM) clearly better | 46 | 69% |

Lexical overlap = share of the query words (> 3 letters) found in the closest relevant document.

## BGE-M3 (All) clearly better

### Query PLAIN-1473: Δ nDCG@10 +0.61 (BGE-M3 (All) 1.00, RRF (BM25 + MiniLM) 0.39)

> kohlrabi

- Relevant documents: 1. First relevant at rank 1 (BGE-M3 (All)) vs 5 (RRF (BM25 + MiniLM))
- Lexical overlap: 100% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Glucoraphanin and 4-hydroxyglucobrassicin contents in seeds of 59 cul… | 1 | Hibiscus anthocyanins rich extract-induced apoptotic cell death in hu… |  |
| 2 | Bioavailability and kinetics of sulforaphane in humans after consumpt… |  | Vitamin D deficiency treated by consuming UVB-irradiated mushrooms |  |
| 3 | Carrageenan induces interleukin-8 production through distinct Bcl10 p… |  | Effect of cruciferous vegetable consumption on heterocyclic aromatic … |  |
| 4 | Goji berry effects on macular characteristics and plasma antioxidant … |  | An evidence-based systematic review of acai (Euterpe oleracea) by the… |  |
| 5 | Effect of treatment with a colloidal oatmeal lotion on the acneform e… |  | Glucoraphanin and 4-hydroxyglucobrassicin contents in seeds of 59 cul… | 1 |

### Query PLAIN-551: Δ nDCG@10 +0.61 (BGE-M3 (All) 0.61, RRF (BM25 + MiniLM) 0.00)

> amnesia

- Relevant documents: 2. First relevant at rank 1 (BGE-M3 (All)) vs >100 (RRF (BM25 + MiniLM))
- Lexical overlap: 0% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Amnesic shellfish poison. | 1 | Traumatic brain injuries in illustrated literature: experience from a… |  |
| 2 | Effects of Aerobic Exercise on Mild Cognitive Impairment |  | Elevated Serum Pesticide Levels and Risk of Parkinson Disease |  |
| 3 | Cognitive impairment and dementia in neurocysticercosis: a cross-sect… |  | Statin Use and Breast Cancer Survival: A Nationwide Cohort Study from… |  |
| 4 | Is dementia reversible in patients with neurocysticercosis? |  | Blueberry Supplementation Improves Memory in Older Adults |  |
| 5 | Prevalence of Cognitive Impairment without Dementia in the United Sta… |  | Biocompatibility of micro- and nano-particles in the colon. Part II. |  |

### Query PLAIN-1320: Δ nDCG@10 +0.49 (BGE-M3 (All) 0.49, RRF (BM25 + MiniLM) 0.00)

> Harvard Physicians’ Study II

- Relevant documents: 6. First relevant at rank 1 (BGE-M3 (All)) vs 11 (RRF (BM25 + MiniLM))
- Lexical overlap: 67% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Multivitamins in the Prevention of Cancer in Men: The Physicians’ Hea… | 1 | Physician disclosure of healthy personal behaviors improves credibili… |  |
| 2 | Multivitamins in the Prevention of Cardiovascular Disease in Men: The… | 1 | How evidence-based medicine biases physicians against nutrition. |  |
| 3 | Vitamins E and C in the Prevention of Cardiovascular Disease in Men: … |  | Moses Maimonides: medieval physician and scholar. |  |
| 4 | Prescribing “placebo treatments”: results of national survey of US in… |  | Barriers to providing nutrition counseling cited by physicians: a sur… |  |
| 5 | Long-term morbidity and mortality of overweight adolescents. A follow… |  | Physicians' health habits are associated with lifestyle counseling fo… |  |

### Query PLAIN-2291: Δ nDCG@10 +0.45 (BGE-M3 (All) 0.45, RRF (BM25 + MiniLM) 0.00)

> ultra-processed foods

- Relevant documents: 5. First relevant at rank 1 (BGE-M3 (All)) vs 13 (RRF (BM25 + MiniLM))
- Lexical overlap: 67% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Profits and pandemics: prevention of harmful effects of tobacco, alco… | 1 | Lipophilic and hydrophilic antioxidant capacities of common foods in … |  |
| 2 | Concentrations of polybrominated diphenyl ethers, hexachlorobenzene a… |  | Processed tart cherry products--comparative phytochemical content, in… |  |
| 3 | Processed meat and colorectal cancer: a review of epidemiologic and e… |  | Beyond celery and starter culture: advances in natural/organic curing… |  |
| 4 | Dioxins, dibenzofurans, dioxin-like PCBs, and DDE in U.S. fast food, … |  | The Role of Whole Grains in Body Weight Regulation |  |
| 5 | Immune potentiation of ultrafine dietary particles in normal subjects… |  | Oxidative processes in meat and meat products: Quality implications. |  |

### Query PLAIN-1537: Δ nDCG@10 +0.43 (BGE-M3 (All) 0.75, RRF (BM25 + MiniLM) 0.32)

> low-carb diets

- Relevant documents: 45. First relevant at rank 1 (BGE-M3 (All)) vs 2 (RRF (BM25 + MiniLM))
- Lexical overlap: 50% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Low-carbohydrate diets and all-cause and cause-specific mortality: Tw… | 1 | Effects of very-low-carbohydrate (horsemeat- or beef-based) diets and… |  |
| 2 | The effect of a plant-based low-carbohydrate ("Eco-Atkins") diet on b… | 1 | The effect of a plant-based low-carbohydrate ("Eco-Atkins") diet on b… | 1 |
| 3 | Effects of very-low-carbohydrate (horsemeat- or beef-based) diets and… |  | A low-fat vegan diet and a conventional diabetes diet in the treatmen… |  |
| 4 | Low-Carbohydrate Diets and All-Cause Mortality: A Systematic Review a… | 1 | Low-carbohydrate diets and all-cause and cause-specific mortality: Tw… | 1 |
| 5 | Negative effect of a low-carbohydrate, high-protein, high-fat diet on… | 1 | Very-low-carbohydrate ketogenic diet v. low-fat diet for long-term we… | 1 |

## RRF (BM25 + MiniLM) clearly better

### Query PLAIN-3026: Δ nDCG@10 -1.00 (BGE-M3 (All) 0.00, RRF (BM25 + MiniLM) 1.00)

> Vitamin C-Enriched Bacon

- Relevant documents: 1. First relevant at rank 18 (BGE-M3 (All)) vs 1 (RRF (BM25 + MiniLM))
- Lexical overlap: 33% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Airborne mutagens produced by frying beef, pork and a soy-based food. |  | Effects of vitamins C and E on N-nitroso compound formation, carcinog… | 2 |
| 2 | Supplementation with vitamin C and N-acetyl-cysteine increases oxidat… |  | Survey of naturally and conventionally cured commercial frankfurters,… |  |
| 3 | Well-done meat intake and the risk of breast cancer. |  | Flaxseed fed pork: n-3 fatty acid enrichment and contribution to diet… |  |
| 4 | Vitamins C and E and Beta Carotene Supplementation and Cancer Risk: A… |  | Safety considerations and potential interactions of vitamins: should … |  |
| 5 | Occurrence of heterocyclic amines in cooked meat products. |  | Effect of vitamin C supplements on physical performance. |  |

### Query PLAIN-3342: Δ nDCG@10 -0.51 (BGE-M3 (All) 0.30, RRF (BM25 + MiniLM) 0.81)

> Is Coconut Milk Good For You?

- Relevant documents: 3. First relevant at rank 2 (BGE-M3 (All)) vs 1 (RRF (BM25 + MiniLM))
- Lexical overlap: 67% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Coconut oil predicts a beneficial lipid profile in pre-menopausal wom… |  | The cholesterol-lowering effect of coconut flakes in humans with mode… | 2 |
| 2 | The cholesterol-lowering effect of coconut flakes in humans with mode… | 2 | Coconut oil predicts a beneficial lipid profile in pre-menopausal wom… |  |
| 3 | An Open-Label Pilot Study to Assess the Efficacy and Safety of Virgin… |  | The intravenous use of coconut water. |  |
| 4 | Cocoa, Blood Pressure, and Cardiovascular Health. |  | Dietary intake and the risk of coronary heart disease among the cocon… | 2 |
| 5 | Effects of dietary coconut oil, butter and safflower oil on plasma li… |  | Effects of dietary coconut oil, butter and safflower oil on plasma li… |  |

### Query PLAIN-2081: Δ nDCG@10 -0.50 (BGE-M3 (All) 0.50, RRF (BM25 + MiniLM) 1.00)

> shelf life

- Relevant documents: 1. First relevant at rank 3 (BGE-M3 (All)) vs 1 (RRF (BM25 + MiniLM))
- Lexical overlap: 100% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | The effect of blood removal on oxidation and shelf life of broiler br… |  | Oxidative stability and shelf-life evaluation of selected culinary oi… | 1 |
| 2 | gamma-Irradiation dose: effects on baby-leaf spinach ascorbic acid, c… |  | Half-lives of serum PCB congener concentrations in environmentally ex… |  |
| 3 | Oxidative stability and shelf-life evaluation of selected culinary oi… | 1 | Comparative and meta-analytic insights into life extension via dietar… |  |
| 4 | Modifying the processing and handling of frozen broccoli for increase… |  | Microbiology of fresh and restructured lamb meat: a review. |  |
| 5 | Microbiology of fresh and restructured lamb meat: a review. |  | Ten years of life: Is it a matter of choice? |  |

### Query PLAIN-2019: Δ nDCG@10 -0.47 (BGE-M3 (All) 0.00, RRF (BM25 + MiniLM) 0.47)

> rickets

- Relevant documents: 3. First relevant at rank >100 (BGE-M3 (All)) vs 1 (RRF (BM25 + MiniLM))
- Lexical overlap: 100% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Identification of cheese mite species inoculated on Mimolette and Mil… |  | Low Vitamin D Status: Definition, Prevalence, Consequences and Correc… | 1 |
| 2 | The autopsy of chicken nuggets reads "chicken little". |  | Sexual selection and genital anatomy of male primates. |  |
| 3 | Roundup disrupts male reproductive functions by triggering calcium-me… |  | Statin Use and Breast Cancer Survival: A Nationwide Cohort Study from… |  |
| 4 | Environmental obesogens: organotins and endocrine disruption via nucl… |  | The autopsy of chicken nuggets reads "chicken little". |  |
| 5 | The relevance of tick bites to the production of IgE antibodies to th… |  | Dietary sources of inorganic microparticles and their intake in healt… |  |

### Query PLAIN-291: Δ nDCG@10 -0.42 (BGE-M3 (All) 0.00, RRF (BM25 + MiniLM) 0.42)

> Stool Size and Breast Cancer Risk

- Relevant documents: 13. First relevant at rank 19 (BGE-M3 (All)) vs 1 (RRF (BM25 + MiniLM))
- Lexical overlap: 60% of the query words appear in the closest relevant document

| Rank | BGE-M3 (All) | Rel. | RRF (BM25 + MiniLM) | Rel. |
|:-:|---|:-:|---|:-:|
| 1 | Occupational sitting and health risks: a systematic review. |  | Fecal weight, colon cancer risk, and dietary intake of nonstarch poly… | 1 |
| 2 | Environmental cadmium and breast cancer risk |  | Fecal weight, colon cancer risk, and dietary intake of nonstarch poly… | 1 |
| 3 | Long-term statin use and risk of ductal and lobular breast cancer amo… |  | Diet and breast cancer: understanding risks and benefits. |  |
| 4 | Statin use and risk of breast cancer: a meta-analysis of observationa… |  | Dietary fiber intake and risk of breast cancer: a meta-analysis of pr… |  |
| 5 | Body-mass index and incidence of cancer: a systematic review and meta… |  | Preschool diet and adult risk of breast cancer. |  |
