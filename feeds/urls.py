from django.urls import path
from feeds import views

app_name = 'feeds'

urlpatterns = [
    path('explore', views.home, name="home"),
    path('explore/<str:tag>', views.explore, name='explore'),
    path('article/bookmark', views.add_bookmark, name='bookmark_article'),
    path('user/bookmark', views.get_bookmark, name='get_bookmark'),
    path('user/del_bookmark', views.delete_bookmark, name='delete_bookmark'),
    path('user/<str:tag>', views.for_you, name="for_you"),
]
