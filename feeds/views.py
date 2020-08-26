from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages
from users.models import User, UserInterest, UserBookmark
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
    articles['Headlines'] = EverythingDB.getArticles('Headlines', number=20)
    articles['Top'] = EverythingDB.getArticles('Top', number=5)
    for data in articles['Headlines']:
        data['id'] = data['_id']
    for data in articles['Top']:
        data['id'] = data['_id']
    # pp(articles)
    return render(request, 'feeds/home.html', {'articles': articles})


def explore(request, tag):
    data = EverythingDB.getArticles(tag, number=30)
    articles = []
    if data:
        for d in data:
            d['id'] = d['_id']
            d['datePublished'] = d['datePublished'][:10]
            articles.append(d)
        # pp(articles)
    return render(request, 'feeds/explore.html', {'articles': articles, 'tag': tag})


# view for showing user's personalised feed
@login_required
def for_you(request, tag):
    try:
        user_interests = json.loads(
            UserInterest.objects.get(user=request.user).interests)
    except Exception as e:
        print(e)
        user_interests = dict()
    articles = dict()
    for category in user_interests.keys():
        # try retrieving artciles from users prepared feed
        data = UserGenreDB.get_feed_articles(
            category=category, user_id=request.user.id)
        # if user feed has not been prepared
        if not data:
            data = EverythingDB.getArticles(category=category, number=10)

        response = []
        for d in data:
            d['id'] = d['_id']
            response.append(d)
        articles[category] = response

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

        if event == 'bookmark':
            try:
                user = UserBookmark.objects.get(User=request.user)
                # print('Here#1')
                if len(user.bookmarks) < 10:
                    # print('Here#2', len(user.bookmarks))

                    if user:
                        # print('Here#3')

                        if article_id not in user.bookmarks:
                            user.bookmarks.append(article_id)
                            user.save()
            except:
                # print('Here#4')
                user_bookmark = UserBookmark.objects.create(
                    User=request.user, bookmarks=[article_id])

        # add message
        # messages.add_message(request, messages.INFO, 'Added to bookmarks')
        return JsonResponse({'success': True}, status=200)
    else:
        # add message
        # messages.add_message(request, messages.ERROR, 'Failed!')
        return JsonResponse({'success': False}, status=400)


@login_required
def get_bookmark(request):
    bookmarks = None
    try:
        bookmarks = UserBookmark.objects.get(User=request.user).bookmarks
    except Exception as e:
        print(e)
    data = []
    if bookmarks:
        data = UserGenreDB.get_bookmark_articles(
            user_id=request.user.id, bookmarks=bookmarks)
        if data:
            for d in data:
                d['id'] = d['_id']
    return render(request, 'feeds/bookmark.html', {'articles': data})


@login_required
def delete_bookmark(request):
    if request.method == 'GET' and request.is_ajax:
        article_id = request.GET.get('article_id')
        user = UserBookmark.objects.get(User=request.user)
        user.bookmarks.remove(article_id)
        user.save()
        return JsonResponse({'success': True}, status=200)
