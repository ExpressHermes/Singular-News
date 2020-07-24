from pymongo import MongoClient
from .news_api import NewsAPI
from .genre_list import Genres

class MongoOperations:
    '''
    All db operations

    Guidelines:
        1. To insert everything, call Genres class and pass genre_list 
            as an argument
    '''
    def __init__(self, db_name):
        self.client = MongoClient('mongodb+srv://ansh-indus:ansh-lehri-indus@cluster0.ynwdl.mongodb.net/%s?retryWrites=true&w=majority' % (db_name))

        # connecting to database
        self.db = self.client[db_name]  
        self.genre = Genres()
        self.api = NewsAPI() 


    def insertEverything(self):
        # for every category in genre list populate the
        # collection by calling api 
        categories = self.genre.genre_list
        for category in categories:
            # retrieve articles from NewsAPI class
            articles = self.api.getEverything(category)
            collection = self.db[category]
            try:
                collection.insert_many(articles)
                return 1
            except Exception as e:
                print(e)
                return 0
    

    def insertTopHeadlines(self):
        # for every category in genre list insert top 
        # headlines articles into collection
        categories = self.genre.genre_list
        for category in categories:
            articles = self.api.getTopHeadlines(category)
            collection = self.db[category]
            try:
                collection.insert_many(articles)
                return 1
            except Exception as e:
                print(e)
                return 0
    

    def getArticles(self, category):
        # get every article for given category
        collection = self.db[category]
        articles = collection.find({})
        return articles

        
    
    