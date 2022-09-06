import vaex as vx
import pandas as pd
import numpy as np 

cit = vx.open('citation_with_similarity.hdf5')
sender_cit = cit.groupby(cit['sender'],agg='count')
sender_cit.rename('count','sender_citation_count')
cit = cit.join(sender_cit,on='sender',how='inner',allow_duplication=True)

pubdates = cit['pubdate','pubdate_rec'].to_pandas_df()
pubdates['pubdate'] = pd.to_datetime(pubdates['pubdate'])
pubdates['pubdate_Rec'] = pd.to_datetime(pubdates['pubdate_rec'])

cit['lag'] = np.array(pubdates['pubdate']-pubdates['pubdate_Rec'])

cit.export('cit_with_sim_sendcount_lag.hdf5',progress=True)