from django.urls import path
from feeds import views

app_name = 'feeds'

urlpatterns = [
    path('', views.HomeView, name="home"),
    path('search/<str:pk>', views.SearchView, name="search"),
]