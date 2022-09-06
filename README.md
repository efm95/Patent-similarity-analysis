# Patent-similarity-analysis
Patent citation analysis from the paper "Drivers of the decrease of patent similarities from 1976 to 2021"

To replicate the analysis provided by the paper, the following steps must be executed:
1. download the data through https://github.com/efm95/patents
2. `hdf5_conversion.py`
3. `embeddings_computation.py`
4. `similarity_computation.py`
5. `cit_count_and_lag.py`
6. `jaccard_sim.py`

Once the preprocessing phase is done, it is possible to reproduce the analysis through the R script `analysis.R`.
