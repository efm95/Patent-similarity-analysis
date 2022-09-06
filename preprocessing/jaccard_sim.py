import vaex as vx
import pandas as pd
import numpy as np
from joblib import Parallel, delayed
from tqdm import tqdm


cit = vx.open('cit_with_sim_sendcount_lag.hdf5')
cit = cit[cit['lag']>0]
cit = cit.sample(n=1000000,random_state=10091995)
cit = cit.to_pandas_df()
ipc = vx.open('grant_ipc.hdf5')

def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))

def jaccard(row):
    send = tmp.iloc[row,0]
    rec = tmp.iloc[row,1]
    
    send_ipc = ipc[ipc.patnum==send].to_pandas_df()
    rec_ipc = ipc[ipc.patnum==rec].to_pandas_df()
    
    jac_sec = jaccard_similarity(send_ipc['section'],rec_ipc['section'])
    jac_class = jaccard_similarity(send_ipc['class'],rec_ipc['class'])
    jac_sub_class = jaccard_similarity(send_ipc['subclass'],rec_ipc['subclass'])
    jac_group = jaccard_similarity(send_ipc['group'],rec_ipc['group'])
    sub_grpup = jaccard_similarity(send_ipc['sub-group'],rec_ipc['sub-group'])
    
    return jac_sec,jac_class,jac_sub_class,jac_group,sub_grpup

years = list(range(1976,2022))
jac_matrix = np.zeros(shape=(0,5))
for y in years:
   
    tmp = cit[cit.pub_date.str.contains(str(y))]
    sec = Parallel(n_jobs=-1,verbose=True)(delayed(jaccard)(i) for i in tqdm(range(len(tmp))))
    jac_matrix = np.append(jac_matrix,sec,axis=0)
    print('Year ',y,' --DONE')
    

jac  = pd.DataFrame(data = jac_matrix,columns = ['jac_section','jac_class','jac_sub-class','jac_group','jac_sub-group'])
cit = pd.merge([cit,jac],axis=1)
cit.to_csv('sample_cit_complete.csv',index=False)

