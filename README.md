# Patent-similarity-analysis
Patent citation analysis from paper "Drivers of the decrease of patent similarities from 1976 to 2021"

In order to replicate the analysis provided by the paper, the following steps must be executed:
1. download the data through https://github.com/efm95/patents
2. execute `hdf5_conversion.py`
3. execute `embeddings_computation.py`
4. execute `similarity_computation.py`
5. execute `cit_count_and_lag.py`
6. execute `jaccard_sim.py`

Once the preprocessing phase is done, it is possible to reproduce the analysis through the R scrit `analysis.R`. 
