# contains all MongoDB database collections

from pymongo import MongoClient

class Databases:
    
   
    def doc_database(self):
    # database containing all articles distributed genre wise
        
        self.client = MongoClient('mongodb+srv://ansh-indus:ansh-lehri-indus@cluster0.ynwdl.mongodb.net/indus_articles?retryWrites=true&w=majority')
        # change username and password to more common name 
        
        
        self.doc_db = self.client.get_database('indus_articles')   # connecting to database indus_articles
        
        
#add other databases here
    

        
    
    