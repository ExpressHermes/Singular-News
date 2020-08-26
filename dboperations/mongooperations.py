from pymongo import MongoClient
from bson import ObjectId
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
        self.client = MongoClient(
            'mongodb+srv://ansh-indus:ansh-lehri-indus@cluster0.ynwdl.mongodb.net/%s?retryWrites=true&w=majority' % (db_name))

        # connecting to database
        self.db = self.client[db_name]
        self.genre = Genres()
        self.api = NewsAPI()

    def insertEverything(self, categories=' '):
        # for every category in genre list as well as
        # headlines and trending news and populate the
        # collection by calling api
        categories = self.genre.List
        for category in categories:
            # retrieve articles from NewsAPI class
            articles = self.api.getHeadOrCategory(category)
            collection = self.db[category]
            print('Getting %s articles' % category)
            try:
                for article in articles['value']:
                    collection.insert_one(article)
                print('Done....')
            except Exception as e:
                print('Exception:', e)
                # return

    def insertHeadlines(self):
        # for every category in genre list insert top
        # headlines articles into collection
        articles = self.api.getHeadOrCategory()
        collection = self.db['Headlines']
        print('Getting Headline articles')
        try:
            for article in articles['value']:
                collection.insert_one(article)
            print('Done.....')
        except Exception as e:
            print('Exception:', e)

    def insertTopNews(self):
        # insert top articles into collection
        articles = self.api.getTopOrsearchQuery()
        collection = self.db['Top']
        print('Getting Top News articles')
        try:
            for article in articles['value']:
                collection.insert_one(article)
            print('Done.....')
        except Exception as e:
            print('Exception:', e)

    def insertTrending(self):
        # get trending articles
        articles = self.api.trendingTopics()
        collection = self.db['Trending']
        print('Getting Trending articles')
        try:
            for article in articles['value']:
                collection.insert_one(article)
            print('Done.....')
        except Exception as e:
            print('Exception:', e)

    def getArticles(self, category, number=10):
        # get every article for given category
        # number : total number of articles to be retrieved, default = 10
        collection = self.db[category]
        cursor = collection.find({}).sort(
            [("datePublished", -1)]).limit(number)
        articles = []
        if cursor:
            for r in cursor:
                articles.append(r)
        return articles

    def getOneArticle(self, id, category):
        collection = self.db[category]
        cursor = collection.find({'_id': ObjectId(id)})
        for i in cursor:
            return i
        return -1

    def delEverything(self, db_name):
        # delete every document in every category
        # inside db
        categories = self.genre.List
        categories.append('Headlines')
        categories.append('Trending')
        categories.append('Top')

        for category in categories:
            print('Deleting %s ' % category)
            collection = self.db[category]
            try:
                collection.delete_many({})
                print('Done.....')
            except Exception as e:
                print('Exception:', e)
