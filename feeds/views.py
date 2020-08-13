from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages
from users.models import User, UserInterest
from dboperations.mongooperations import MongoOperations
from dboperations.interactiondb import UserGenreDB
from dboperations.news_api import NewsAPI 
from django.http import JsonResponse
from feed_preparation.Feed_Formation import feed_formation
import requests
import json
import datetime
from pprint import pprint as pp

EverythingDB = MongoOperations('everything')
UserGenreDB = UserGenreDB()
# NewsAPI =   NewsAPI()
# feed = feed_formation()


def home(request):
    # EverythingDB.delEverything('everything')
    # EverythingDB.insertEverything()
    # EverythingDB.insertHeadlines()
    # EverythingDB.insertTopNews()
    # EverythingDB.insertTrending()
    # feed.feed_prepare()
    articles = dict()
    articles['Headlines'] = EverythingDB.getArticles('Headlines', number=5)
    articles['Top'] = EverythingDB.getArticles('Top', number=5)
    return render(request, 'feeds/home.html', {'articles': articles})


def explore(request, tag):
    data = EverythingDB.getArticles(tag, number=20)
    articles = []
    if data:
        for d in data:
            d['id']  = d['_id']
            d['datePublished'] = d['datePublished'][:10]
            articles.append(d)
        # pp(articles)
    return render(request, 'feeds/explore.html', {'articles': articles, 'tag': tag})


# view for showing user's personalised feed
@login_required
def for_you(request, tag):
    try:
        user_interests = json.loads(UserInterest.objects.get(user=request.user).interests)
    except Exception as e:
        print(e)
        user_interests = dict()
    articles = dict()
    for category in user_interests.keys():
        # print('Getting %s articles.....' % category)
        data = UserGenreDB.get_feed_articles(category=category, user_id=request.user.id)
        # print('Done')
        response = []
        if data:
            for d in data:
                d['id']  = d['_id']
                response.append(d)
        articles[category] = response
        # pp(articles)
    return render(request, 'feeds/for_you.html', {'articles': articles, 'tag': 'for-you'})


@login_required
def add_bookmark(request):
    if request.method == 'GET' and request.is_ajax():
        category = request.GET.get('category')
        event = request.GET.get('event')
        article_id = request.GET.get('article_id')
        user_id = request.user.id
        # Inserting document inside document
        UserGenreDB.add_interaction(category, article_id, user_id, event)

        # add message
        # messages.add_message(request, messages.INFO, 'Added to bookmarks')
        return JsonResponse({'success': True}, status=200)
    else:
        # add message
        # messages.add_message(request, messages.ERROR, 'Failed!')
        return JsonResponse({'success': False}, status=400)

@login_required
def get_bookmark(request):
    try:
        user_interests = json.loads(UserInterest.objects.get(user=request.user).interests)
    except Exception as e:
        user_interests = dict()
    articles = dict()
    for category in user_interests.keys():
        data = UserGenreDB.get_bookmark_articles(category=category, user_id=request.user.id)
        response = []
        if data:
            for d in data:
                d['id']  = d['_id']
                response.append(d)
        articles[category] = response
        # pp(articles)
    return render(request, 'feeds/bookmark.html', {'articles': articles})


