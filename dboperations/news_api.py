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
                        'x-rapidapi-key': "f4e6d5ac1bmsh1ea91fbdf3d6af2p1165d6jsn42963a0a5b08",
                        'x-bingapis-sdk': "true"
                        }
        self.querystring = {"freshness": "Week", "count": "20", "mkt": "en-IN", "originalImg": "true",  "safeSearch":"Off","textFormat":"Raw"}
                        

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
