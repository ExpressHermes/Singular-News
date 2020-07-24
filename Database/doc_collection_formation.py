from mongo_database import Databases
from news_api import News_API
from genres_list import Genres

database = Databases()
api = News_API()
genres = Genres()

database.doc_database()
genres.genres_list()

for i in genres.list:
    
    # calling news api with q=genre name
    all_articles = api.newsapi.get_everything(q=f'{i}',
                                      sources='the-times-of-india,the-hindu,google-news-in',
                                      domains='timesofindia.indiatimes.com,thehindu.com,news.google.com',
                                      from_param='2020-07-13',
                                      to='2020-07-15',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)
    
    # opening collections according to genre in list of genres from genres_list.py
    if i=='sports':
     collection = database.doc_db.sports
    elif i=='business':
     collection = database.doc_db.business
    elif i=='entertainment':
     collection = database.doc_db.entertainment
    elif i=='health':
     collection = database.doc_db.health
    elif i=='science':
     collection = database.doc_db.science
    elif i=='technology':
     collection = database.doc_db.technology
     
    #inserting articles into the required collection
    collection.insert_many(all_articles['articles'])

