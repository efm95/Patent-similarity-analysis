import pandas as pd
import logging
import pickle
from sentence_transformers import SentenceTransformer, LoggingHandler

import timeit



logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])

if __name__ == '__main__':

    start = timeit.default_timer()

    df = pd.read_csv('grant_grant.csv',usecols=['patnum','abstract'])

    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Max Sequence Length:", model.max_seq_length)
    model.max_seq_length = 256
    print("Updated max Sequence Length:", model.max_seq_length)

    #Start the multi-process pool on all available CUDA devices
    pool = model.start_multi_process_pool()

    #Compute the embeddings using the multi-process pool
    emb = model.encode_multi_process(df['abstract'], pool)
    print("Embeddings computed. Shape:", emb.shape)
    
    model.stop_multi_process_pool(pool)
    
    #Store embeddings
    with open('embeddings.pkl', "wb") as fOut:
        pickle.dump({'embeddings': emb}, fOut, protocol=pickle.HIGHEST_PROTOCOL)
    
    stop = timeit.default_timer()
    print('Time: ', stop - start) 


