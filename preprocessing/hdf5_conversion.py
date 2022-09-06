import pandas as pd 
import vaex as vx

grant = pd.read_csv('grant_grant.csv')
grant = vx.from_pandas(grant)
grant.export('grant_grant.hdf5',progress=True)
del grant

cit = pd.read_csv('grant_cite.csv')
cit = vx.from_pandas(cit)
cit.export('grant_cite.hdf5',progress=True)
del cit

ipc = pd.read_csv('grant_ipc.csv')
ipc['section'] = ipc['ipc'].str[0]
ipc['class'] = ipc['ipc'].str[:3]
ipc['subclass'] = ipc['ipc'].str[:4]
ipc['group'] = ipc['ipc'].str[:7]
ipc['sub-group'] = ipc['ipc']
ipc.drop(ipc,inplace=True)

ipc = vx.from_pandas(ipc)
ipc.export('grant_ipc.hdf5',progress=True)
