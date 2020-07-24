from django.urls import path, include
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm
from . import views

app_name = 'users'

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name="users/login.html"),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('interests/', views.interests, name="interests"),
    path('profile/', views.profile, name="profile"),
]