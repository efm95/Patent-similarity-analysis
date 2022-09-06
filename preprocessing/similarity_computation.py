import vaex as vx
import numpy as np
import pickle as pkl
from scipy.spatial.distance import cosine
from tqdm import tqdm
from joblib import Parallel, delayed

cit = vx.open('grant_cite.hdf5')
cit.rename('src','sender')
cit.rename('dst','receiver')

grant = vx.open('grant_grant.hdf5')
grant = grant['patnum','pubdate','owner']
grant.rename('patnum','sender')
grant['index'] = vx.vrange(0,len(grant))
grant.rename('index','senderPos')
cit = cit.join(grant, on='sender',allow_duplication=True)

grant.rename('sender','receiver')
grant.rename('senderPos','receiverPos')
grant.rename('pubdate','pubdate_rec')
grant.rename('owner','owner_rec')
cit = cit.join(grant, on='receiver',allow_duplication=True)

print('Edge list: ',cit.head())

with open('embeddings.pkl', "rb") as fIn:
    emb = pkl.load(fIn)['embeddings']

print('New edgelist: ',cit.head())

def cos(row,sender_pos,receiver_pos):
    a = sender_pos[row]
    b = receiver_pos[row]
    return 1-cosine(a,b)

def TexSim(df,emb_matrix):
    df['index'] = vx.vrange(0,len(df))  
    sim = np.array([])
    index_df = np.array([],dtype=np.int64)
    years = list(range(1976,2022))
    for y in tqdm(years):
        tmp_total = df[df['pubdate'].str.contains(y)]
        tmp = tmp_total['receiverPos','senderPos','index'].to_pandas_df()
        row_index = tmp['index'].to_numpy()
        sender_pos = emb_matrix[np.array(tmp.senderPos,dtype=np.int64)]
        receiver_pos = emb_matrix[np.array(tmp.receiverPos,dtype=np.int64)]
        sim_curr = Parallel(n_jobs=-1)(delayed(cos)(i,sender_pos,receiver_pos) for i in range(len(tmp)))
        sim = np.append(sim,sim_curr)
        index_df = np.append(index_df,row_index)        
    out = vx.from_arrays(index=index_df,sim=sim)
    return out

sim = TexSim(df=cit,
             emb_matrix=emb)

cit['index'] = vx.vrange(0,len(cit))
cit = cit.join(sim,how='inner',on='index',allow_duplications=True)
cit.drop(['index','senderPos','receiverPos'],inplace=True)

cit.extract('citation_with_similarity.hdf5',progress=True)