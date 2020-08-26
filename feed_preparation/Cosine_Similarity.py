import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from .Singular_Value_Decomposition import SVD

class Similarity:
    
    def __init__(self,category):
        
        self.svd = SVD(category)
        self.svd.Truncated_SVD()
        
        # Checking if number of users are enough or not
        if self.svd.flag==0:
            return
        
    def rated_doc_df(self):
        
        self.rated_docs_df = pd.DataFrame()       
        self.rated_docs = list(self.svd.doc_ids.keys()) 
       
        self.rated_docs_index = {self.rated_docs[i]:i for i in range(0,len(self.rated_docs))}
        del self.rated_docs
        
        for ids in self.rated_docs_index:
            
            doc = self.svd.svd_user_score_df.loc[ids]
            self.rated_docs_df[ids] = doc
            
    def cosine_sim(self):
        
        self.rated_doc_df()
        self.similarity_score = cosine_similarity(self.rated_docs_df.T,self.svd.svd_user_score_df)
        
    def user_top_news(self,similarity_score,user=None):
        
        
        # Preparing score for user feed
        # Score of articles r added based on articles rated by user
        doc_score = {key:0 for key in self.svd.index}
        
        if user==None:
            return
        
        for doc in user:
            for key in range(0,len(self.svd.index)):
                if self.svd.index[key] == doc['article_id']:
                    continue
                doc_score[self.svd.index[key]]+=similarity_score[self.rated_docs_index[doc['article_id']]][key]
        
        return (doc_score)        
        
    
    
    
        
            
    
            
    
