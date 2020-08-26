from dboperations.mongooperations import MongoOperations
from dboperations.interactiondb import UserGenreDB
import datetime
import re
from collections import defaultdict
import pandas as pd
from sklearn.decomposition import TruncatedSVD
import pprint

class SVD:
    
    def __init__(self,category):
        
        self.db_everything = MongoOperations('everything')
        self.db_user_genre = UserGenreDB()
        
        self.coll_everything = self.db_everything.db[category]
        self.coll_user_genre = self.db_user_genre.db[category]
   
        
    def age_of_article(self,doc_date):
        
        # calculate duration of articles 
 
        date=re.search(r"\d{4}-\d{2}-\d{2}",doc_date).group()
        date=datetime.datetime.strptime(date,'%Y-%m-%d').date()
        date_difference=datetime.date.today()-date
        return (date_difference.days)
        
    def articles(self):
        
        user_count = self.coll_user_genre.count_documents({})
        
        self.doc_source = defaultdict(list)
        
        # check if number of registered users in a genre
        self.flag=1
        if user_count < 6:
            print("OOOppppppps!!!!!!!!!!!!! Add more Users")
            self.flag=0
            return
        
        self.doc_cursor = self.coll_everything.find({},{'_id':1,'datePublished':1,'provider':1})
        self.doc_current_base_value = dict()     
        for doc in self.doc_cursor:   
            
            self.doc_source[doc['provider'][0]['name']].append(str(doc['_id']))   # Preparing dictionary of source pointing to articles from that source
            age = self.age_of_article(doc['datePublished']) 
            self.doc_current_base_value[str(doc['_id'])] = [700.0-age*100.0 for i in range(user_count)] # dictionary with base value of articles 
        
        if user_count==0:
            return
        
        self.user_cursor = self.coll_user_genre.find({},{'Feed':0})
        self.user_doc_score = defaultdict(list)
        self.doc_ids = dict()
        
        # Calculating score of articles given by user
        # by examining user behaviour
        
        for user in self.user_cursor:
            
            for doc in user['articles']:
                
                additional_count=0
                total=75
                flag=1
                
                if 'bookmark' in doc:
                    total=300
                elif 'rating' in doc:
                    if doc['rating']==-1:
                        total=75
                        flag=0
                    if doc['rating']==0:
                        total=165
                    if doc['rating']==1:
                        total=240
                if 'visit' in doc and flag!=0:
                    total=total+doc['visit']*15
                if total>300 and total<330:
                    total=300
                elif total>=330:
                    additional_count=total-300
                    total=300
                
                avg = (total/3)+(additional_count/15)-25
                
                self.user_doc_score[user['_id']].append([doc['article_id'],avg])
                if doc['article_id'] not in self.doc_ids:
                    self.doc_ids[doc['article_id']]=1
                
                
        # structure self.user_doc_score ------> {user_id:[[doc_id,score]]}
        
        self.user_id = [k for k in self.user_doc_score.keys() if self.user_doc_score[k]!=self.user_doc_score.default_factory()]        
        #print(self.doc_ids)        
    
    def user_score_dataframe(self):
        
        # Preparing dataframe
        self.articles()
        
        if self.flag==0:
            return 0
        
        self.user_score_df = pd.DataFrame(self.doc_current_base_value,index=self.user_id)
       
        users = self.coll_user_genre.find({'Sources':{"$exists":True}},{'Sources':1})
        
        # Giving bonus to articles which belong to source of user's choice
        
        for user in users:
            pprint.pprint(user)
            sources = user['Sources']
            for i in sources:
                for j in range(0,len(self.doc_source[i])):
                    
                    self.user_score_df.loc[user['_id']][self.doc_source[i][j]]+=5
      
        # Filling dataframe with score values
        
        for key in self.user_id:
            for i in self.user_doc_score[key]:
                self.user_score_df.loc[key,i[0]]+=i[1]
    
    def Truncated_SVD(self):
        
        self.user_score_dataframe()
        
        # returning back to feed_formation module bcoz number of users for a genre is less than required
        if self.flag==0:
            return
        
        self.index=list(self.doc_current_base_value.keys())
        svd = TruncatedSVD(n_components=5,random_state=0,n_iter=10)
        self.svd_user_score_df = svd.fit_transform(self.user_score_df.T)
        self.svd_user_score_df = pd.DataFrame(self.svd_user_score_df,index=self.index)        