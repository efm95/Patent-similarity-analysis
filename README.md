# Patent-similarity-analysis

This repository contains the codes used for the analysis from the paper [Drivers of the decrease of patent similarities from 1976 to 2021](https://arxiv.org/abs/2212.06046). 

## Abstract 
The citation network of patents citing prior art arises from the legal obligation of patent applicants to properly disclose their invention. One way to study the relationship between current patents and their antecedents is by analyzing the similarity between the textual elements of patents. Patent similarity indicators have been constantly decreasing since the mid-70s. After exposing a computationally efficient way to compute similarity scores that leverages on state-of-the-art Natural Language Processing tools, this works aims to expand the current litterature on patent analysis by investigating the potential drivers of similarity decrease. This is carried out by modelling simiarity citation values across citing and cited patents through different General Additive Models specifications. We found that by using non-linear modelling techniques we are able to distinguish between distinct, temporally varying drivers of  the patent similarity levels that accounts for more variation in the data (R2~18) in comparison to the previous literature. Moreover, with such corrections in place, we conclude that the trend in similarity shows a different pattern than the one presented in previous studies. 


To replicate the analysis provided by the paper, the following steps must be executed:
1. download the data through https://github.com/efm95/patents
2. `hdf5_conversion.py`
3. `embeddings_computation.py`
4. `similarity_computation.py`
5. `cit_count_and_lag.py`
6. `jaccard_sim.py`

Once the preprocessing phase is done, it is possible to reproduce the analysis through the R script `analysis.R`.
