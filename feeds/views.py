from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import requests
import json
from pprint import pprint as pp

# NEWSAPP_API_KEY = 2278558f7fdd483d93adeae366323f21

def HomeView(request):
    url = ('http://newsapi.org/v2/top-headlines?country=in&apiKey=2278558f7fdd483d93adeae366323f21')
    response = (requests.get(url)).json()
    return render(request, 'feeds/home.html', {'articles': response['articles'], 'tag': 'popular'})

def SearchView(request, pk):
    url = 'http://newsapi.org/v2/everything?q=' + pk + '&sortBy=popularity&apiKey=2278558f7fdd483d93adeae366323f21'
    response = (requests.get(url)).json()
    return render(request, 'feeds/home.html', {'articles': response['articles'], 'tag': pk})