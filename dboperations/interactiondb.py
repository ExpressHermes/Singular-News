from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from bson import ObjectId
from .mongooperations import MongoOperations
from .genre_list import Genres


class UserGenreDB:
    def __init__(self):
        self.client = MongoClient(
            'mongodb+srv://ansh-indus:ansh-lehri-indus@cluster0.ynwdl.mongodb.net/user_genre_db?retryWrites=true&w=majority')

        # connecting to database
        self.db = self.client['user_genre_db']
        self.genre = Genres()

    def add_interaction(self, coll_name, article_id, user_id, event):
        collection = self.db[coll_name]
        data = collection.find_one({'_id': user_id})

        # condtions to set ratings properly
        if event == 'unliked':
            event_value = -1
            event = 'rating'
        elif event == 'maybe':
            event_value = 0
            event = 'rating'
        elif event == 'liked':
            event_value = 1
            event = 'rating'
        else:
            event_value = 1

        if not data:
            try:
                collection.insert_one({
                    '_id': user_id,
                    'articles': [{
                        'article_id': article_id,
                        event: event_value
                    }]
                })
            except Exception as e:
                print(e)
        else:
            found = False
            for a in data['articles']:
                if a['article_id'] == article_id:
                    a[event] = a.get(event, 0) + event_value
                    found = True
                    break
            if not found:
                data['articles'].append({
                    'article_id': article_id,
                    event: event_value
                })
            try:
                collection.replace_one({'_id': user_id}, data)
            except Exception as e:
                print(e)

    def get_feed_articles(self, category, user_id):
        collection = self.db[category]
        user = collection.find_one({'_id': user_id})

        if user:
            EverythingDB = MongoOperations('everything')
            try:
                article_ids = user['Feed'][:11]
            except Exception as e:
                return None
            response = list()
            for id in article_ids:
                response.append(EverythingDB.getOneArticle(
                    id=id, category=category))
            return response

    def get_bookmark_articles(self, user_id, bookmarks):
        EverythingDB = MongoOperations('everything')
        search_list = self.genre.List
        search_list.append('Headlines')
        search_list.append('Top')
        response = []
        for b in bookmarks:
            for category in search_list:
                data = EverythingDB.getOneArticle(b, category)
                if data != -1:
                    response.append(data)
                    break
        return response
