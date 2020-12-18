
"""Indus URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('feeds/', include('feeds.urls')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='plain/text')),
    path('sitemap.xml', TemplateView.as_view(template_name='sitemap.xml', content_type='plain/text')),
    path('', include('users.urls')),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name ="users/password_reset.html" ),name ="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name ="users/password_confirm.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name ="users/password_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name ="users/password_done.html"), name="password_reset_complete"),
]
