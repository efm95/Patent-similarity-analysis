# Patent-similarity-analysis

This repository contains the code used for the analysis in the paper [Drivers of the decrease of patent similarities from 1976 to 2021](https://arxiv.org/abs/2212.06046), published in *PLOS ONE*, 18(3), 2023.

## Abstract 
The citation network of patents citing prior art arises from the legal obligation of patent applicants to properly disclose their invention. One way to study the relationship between current patents and their antecedents is by analyzing the similarity between the textual elements of patents. Many patent similarity indicators have shown a constant decrease since the mid-70s. Although several explanations have been proposed, more comprehensive analyses of this phenomenon have been rare. In this paper, we use a computationally efficient measure of patent similarity scores that leverages state-of-the-art Natural Language Processing tools, to investigate potential drivers of this apparent similarity decrease. This is achieved by modeling patent similarity scores by means of generalized additive models. We found that non-linear modeling specifications are able to distinguish between distinct, temporally varying drivers of the patent similarity levels that explain more variation in the data (R2∼18%) compared to previous methods. Moreover, the model reveals an underlying trend in similarity scores that is fundamentally different from the one presented previously.

## Data 

The data were downloaded from the [USPTO bulk data repository](https://bulkdata.uspto.gov/) using the following [library](https://github.com/efm95/patents). The dataset used for this analysis has been uploaded to [Kaggle](https://www.kaggle.com/datasets/filippimazz/patents-citations).

## Effects and data pre-processing

All the effects and data treatment have been carried out using separate Python scripts. To obtain the same sample with the same covariates, run the scripts in the following order: 

1. `hdf5_conversion.py`: to process the data, we used the [vaex](https://vaex.io/docs/index.html#) library, hence, we first converted `csv` files into `hdf5`. 
2. `embeddings_computation.py`: positional embeddings have been computed using a pre-trained SBERT model from the [Sentence-Transformers](https://www.sbert.net/) library from the abstracts in the `grant_grant` file.

3. `similarity_computation.py`: once embeddings have been computed, we proceed by applying the parallelized loop to compute similarity scores for each combination of citing-cited patent in the `grant_cite` file. 

4. `cit_count_and_lag.py`: computation of temporal covariates like citation count and citation time lag.

5. `jaccard_sim.py`: from a reduced sample, Jaccard similarity scores have been computed across citations with respect to their distinct [IPC](https://www.wipo.int/classifications/ipc/en/) code. 

## Analysis

Once the preprocessing phase is done, it is possible to reproduce the analysis through the R script `analysis.R`. This consists of four GAM specifications using the `gam` function in the [`mgcv`](https://cran.r-project.org/web/packages/mgcv/mgcv.pdf) package: 

- *Model 0*: similarity = `s(sender publication date)`

- *Model 1*: similarity = `s(sender publication date)` + `s(time lag between citing and cited publication date in days)`

- *Model 2*: similarity = `s(sender publication date)` + `s(time lag between citing and cited publication date in days)` + `s(sender citation count in log)` + is the same organization?(binary) + is the sender owner an organization?(binary) + is the receiver owner an organization? (binary)

- *Model 3*: similarity = `s(sender publication date)` + `s(time lag between citing and cited publication date in days)` + `s(sender citation count in log)` + is the same organization?(binary) + is the sender owner an organization?(binary) + is the receiver owner an organization?(binary) + jaccard sim for IPC section (continuous) + jaccard sim for IPC class (continuous) + jaccard sim for IPC sub-class (continuous) + jaccard sim for IPC group (continuous) + jaccard sim for IPC subgroup (continuous)

where `s(...)` indicates a smooth term. 
