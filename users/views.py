from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from .forms import SignUpForm
from .models import User, UserInterest
import json
from pprint import pprint as pp



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=user.email, password=raw_password)
            if user is not None:
                login(request, user)
            else:
                print("user is not authenticated")
            return redirect('user:interests')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def interests(request):
    CHOICES = ('technology','health','business', 'sports', 'politics', 'entertainment')
    if request.method == 'POST':
        form = request.POST
        choices = dict()
        for key, value in form.items():
            if key in CHOICES:
                choices[key] = value
        if choices:
            choices = json.dumps(choices)
            user_interest = UserInterest(interests=choices, user=request.user)
            user_interest.save()
        pp(choices)
        return redirect('feeds:home')

    return render(request, 'users/interests.html')


@login_required
def profile(request):
    user = request.user
    user_interests = json.loads(UserInterest.objects.get(user=user).interests)
    pp(user_interests)
    return render(request, 'users/profile.html', {'user': user, 'interests': user_interests})