from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('', views.signup, name='signup'),
    path('signup_message', views.signup_message, name='signup_message'),
    path('activate/<uid64>/<token>', views.activate_account, name='activate'),
    path('login/', views.user_login,name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user/interests/', views.interests, name='interests'),
    path('user/profile/', views.profile, name='profile'),
    path('feedback/', views.feedback, name='feedback'),
    path('help', views.help, name='help')
]