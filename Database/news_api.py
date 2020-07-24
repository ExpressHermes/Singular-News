# news api used

from newsapi import NewsApiClient

class News_API:
    
    def __init__(self):
        
        self.newsapi = NewsApiClient(api_key='8d3662c224214de986ef47032821f9eb')
        
    
