import requests
import json
from pprint import pprint as pp

class NewsAPI:
    '''
        Configuring NewsApi and calling it to retrieve
        articles in different category
    '''
    def __init__(self):
        self.url = "https://bing-news-search1.p.rapidapi.com/news"
        self.headers = {
                          'x-rapidapi-host': "bing-news-search1.p.rapidapi.com",
                          'x-rapidapi-key': "d2800226fbmsh54763bace2a7bdep160c0fjsnc6f5b28aeb83",
                          'x-bingapis-sdk': "true"
                        }
        self.querystring = {"freshness": "Week", "sortBy": "Date", "count": "20", "mkt": "en-IN", "originalImg": "true",  "safeSearch":"Off","textFormat":"Raw"}
                        

    def getHeadOrCategory(self, category=""):
        # for headlines leave category empty
        # or search news in a category
        if category:
            self.querystring['category'] = category
        response = requests.request("GET", self.url, headers=self.headers, params=self.querystring)
        response = response.json()
        # response = json.dumps(response.json())
        # descriptions = [article["description"] for article in response["value"]]
        return response


    def getTopOrsearchQuery(self, q=""):
        # for top news leave q empty
        # search news related to q
        searchUrl = self.url + "/search?q=" + q
        response = requests.request("GET", searchUrl, headers=self.headers, params=self.querystring).json()
        return response
        # pp(response)
    

    def trendingTopics(self):
        # search trending news
        searchUrl = self.url + "/trendingtopics"
        response = requests.request("GET", searchUrl, headers=self.headers, params=self.querystring).json()
        return response
        # pp(response)
