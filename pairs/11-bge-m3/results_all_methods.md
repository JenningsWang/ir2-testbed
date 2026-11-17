# BGE-M3 results (pair 11)

A difference is in bold only when its p-value is below 0.05 and its confidence interval excludes zero.

## scifact

| Method | nDCG@10 | Recall@100 | Compared with | Δ nDCG@10 [95 % CI] | p |
|---|:-:|:-:|---|:-:|:-:|
| *RRF* | 0.718 | 0.948 | | | |
| BGE-M3 (Dense) | 0.633 | 0.904 | RRF | **-0.085 [-0.116, -0.053]** | < 0.001 |
| BGE-M3 (Sparse) | 0.637 | 0.894 | RRF | **-0.081 [-0.114, -0.048]** | < 0.001 |
| BGE-M3 (Multi-vec) | 0.683 | 0.910 | RRF | **-0.035 [-0.063, -0.006]** | 0.020 |
| BGE-M3 (Dense+Sparse) | 0.667 | 0.917 | RRF | **-0.050 [-0.080, -0.020]** | 0.001 |
| BGE-M3 (All) | 0.692 | 0.914 | RRF | -0.026 [-0.054, +0.003] | 0.078 |

## nfcorpus

| Method | nDCG@10 | Recall@100 | Compared with | Δ nDCG@10 [95 % CI] | p |
|---|:-:|:-:|---|:-:|:-:|
| *RRF* | 0.342 | 0.310 | | | |
| BGE-M3 (Dense) | 0.315 | 0.283 | RRF | **-0.028 [-0.045, -0.010]** | 0.002 |
| BGE-M3 (Sparse) | 0.282 | 0.230 | RRF | **-0.060 [-0.080, -0.041]** | < 0.001 |
| BGE-M3 (Multi-vec) | 0.334 | 0.281 | RRF | -0.008 [-0.025, +0.009] | 0.339 |
| BGE-M3 (Dense+Sparse) | 0.326 | 0.288 | RRF | -0.016 [-0.033, +0.000] | 0.049 |
| BGE-M3 (All) | 0.336 | 0.289 | RRF | -0.006 [-0.022, +0.010] | 0.470 |

## arguana

| Method | nDCG@10 | Recall@100 | Compared with | Δ nDCG@10 [95 % CI] | p |
|---|:-:|:-:|---|:-:|:-:|
| *RRF* | 0.549 | 0.985 | | | |
| BGE-M3 (Dense) | 0.543 | 0.982 | RRF | -0.006 [-0.022, +0.009] | 0.415 |
| BGE-M3 (Sparse) | 0.387 | 0.940 | RRF | **-0.162 [-0.179, -0.146]** | < 0.001 |
| BGE-M3 (Multi-vec) | 0.512 | 0.968 | RRF | **-0.037 [-0.052, -0.022]** | < 0.001 |
| BGE-M3 (Dense+Sparse) | 0.524 | 0.987 | RRF | **-0.025 [-0.039, -0.011]** | < 0.001 |
| BGE-M3 (All) | 0.527 | 0.980 | RRF | **-0.022 [-0.036, -0.008]** | 0.002 |
