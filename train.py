
import pandas as pd
import scipy
import scipy.sparse as sps
import implicit
import numpy as np
from time import perf_counter as pc
import json


class ContentEngine(object):

    def __init__(self):
        self.user_items = None
        self.item_index = None
        self.user_index = None
        self.df_items_lookup = None
        self.model = None

    def train(self, df):
        
        #read csv into pandas dataframe
        df = pd.read_csv(df)
        #df = df.iloc[:1000,:]
        print('training model')

        #create dataframe for items to get content vectors 
        df_items = df.iloc[:,3:]
        df_items.drop_duplicates(inplace=True, subset='catalog_item_id')
        df_items.reset_index(inplace=True)

        #create df with just columns needed to return final output
        self.df_items_lookup = df_items.sort_values(by='catalog_item_name').reset_index().loc[:,['catalog_item_id','catalog_item_name', 'brand_name']]


        #create pivot table for matrix factorization
        df = df.groupby(['user_id_hash', 'catalog_item_name'])['quantity'].sum().unstack()

        #create sparse matrix
        sdf = df.astype(pd.SparseDtype("float", np.nan))
        sdf2 = sdf.sparse.to_coo()

        #get list of user and item indexes for lookup later
        self.user_index = list(df.index)
        self.item_index = pd.DataFrame(df.columns)

        # initialize a model
        self.model = implicit.lmf.LogisticMatrixFactorization(factors=20)
        # train the model on a sparse matrix of item/user/confidence weights
        fit = self.model.fit(sdf2.T)

        # recommend items for a user
        self.user_items = sdf2.tocsr()
        print('training complete!')



    def predict(self, request_id):
    
        #get request data with user id
        #content = request.json
        #request_id = content['user_id_hash']
        #end

        #get top 10 recommendations for user id
        #try:
        user_id = self.user_index.index(request_id)
        recommendations = self.model.recommend(user_id, self.user_items, N=5)
        out = pd.DataFrame(recommendations,columns=['item_index','score'])
        #out['user_id_hash'] = request_id
        out = out.merge(self.item_index, how='left', left_on='item_index', right_index=True).drop(columns='item_index')
        out = out.merge(self.df_items_lookup, how='left', on='catalog_item_name')
        #except: print('invalid user id')
        
        #convert recommendations from dataframe to json
        keys = ['score','catalog_item_name','catalog_item_id', 'brand_name']
        values = [[i for i in out.iloc[:,0]],[i for i in out.iloc[:,1]],[i for i in out.iloc[:,2]],[i for i in out.iloc[:,3]] ]
        d = dict(zip(keys, values))
        json_data=[d]
        
        return json.dumps(json_data)


content_engine = ContentEngine()