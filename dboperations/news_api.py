from newsapi import NewsApiClient

class NewsAPI:
    '''
        Configuring NewsApi and calling it to retrieve
        articles in different category
    '''
    def __init__(self):
        self.newsapi = NewsApiClient(api_key='8d3662c224214de986ef47032821f9eb')
        

    def getEverything(self, category):
        # return everything for q = category
        articles = api.newsapi.get_everything(q=category,
                                      sources='the-times-of-india,the-hindu,google-news-in',
                                      domains='timesofindia.indiatimes.com,thehindu.com,news.google.com',
                                      from_param='2020-07-13',
                                      to='2020-07-15',
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)
        return articles['articles']


    def getTopHeadlines(self, category):
        # return top headlines for category = category
        articles = newsapi.get_top_headlines(sources='the-times-of-india,the-hindu,google-news-in',
                                          category=category,
                                          language='en',
                                          country='in')
        return articles['articles']
