from dboperations.genre_list import Genres
from dboperations.interactiondb import UserGenreDB
from .Cosine_Similarity import Similarity



class feed_formation:
    
    def feed_prepare(self):

        genres = Genres()
        database = UserGenreDB()
       
        for category in genres.List:
            
            collection = database.db[category]
            similar = Similarity(category)
            
            if similar.svd.flag==0:
                continue
            
            user_feed = collection.find({})
            
            similar.cosine_sim()
            
            
            # Inserting prepared feed into database
            
            for user in user_feed:
                
                score_dict = similar.user_top_news(similar.similarity_score,user['articles'])
                
                top_feed = sorted(score_dict.items(),key=lambda sd:(sd[1],sd[0]),reverse=True)
                
                feed = [] 
                             
                for i in range(0,len(top_feed)):
                    feed.append(top_feed[i][0])
                    
                collection.update_one({'_id':user['_id']},{"$set":{'Feed':feed}})
            
        
        

