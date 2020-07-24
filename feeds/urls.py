from django.urls import path
from feeds import views

app_name = 'feeds'

urlpatterns = [
    path('', views.HomeView, name="home"),
    path('search/<str:pk>', views.SearchView, name="search"),
    path('<str:pk>', views.ForYouView, name="for_you"),
]