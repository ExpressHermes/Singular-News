from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from users.models import User, UserInterest
from dboperations.mongooperations import MongoOperations
import requests
import json
from pprint import pprint as pp

EverythingDB = MongoOperations('everything')
HeadlinesDB = MongoOperations('headlines')

def HomeView(request):
    url = ('http://newsapi.org/v2/top-headlines?country=in&apiKey=2278558f7fdd483d93adeae366323f21')
    response = (requests.get(url)).json()
    return render(request, 'feeds/home.html', {'articles': response['articles'], 'tag': 'popular'})

def SearchView(request, pk):
    articles = EverythingDB.getArticles(pk)
    # pp(articles)
    return render(request, 'feeds/home.html', {'articles': articles, 'tag': pk})


# view for showing user's personalised feed
@login_required
def ForYouView(request, pk):
    user_interests = json.loads(UserInterest.objects.get(user=request.user).interests)
    articles = dict()
    for category in user_interests.keys():
        print(category)
        response = HeadlinesDB.getArticles(category)
        articles[category] = response
        # pp(response)
    # pp(articles)
    return render(request, 'feeds/for_you.html', {'articles': articles, 'tag': 'for-you'})