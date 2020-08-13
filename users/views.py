from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, UserLoginForm, FeedbackForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, UserInterest, UserFeedback
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
                messages.add_message(request, messages.SUCCESS, 'Sign up successful!')
                login(request, user)
                return redirect('users:interests')
            else:
                messages.add_message(request, messages.ERROR, 'Sign up failed!')
                return redirect('users:signup')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user:
            if user.is_active:
                login(request, user)

                # add success message
                messages.add_message(request, messages.SUCCESS, 'Logged in')
                login(request, user)
                return redirect('feeds:home')
            else:
                # add failed message
                messages.add_message(request, messages.ERROR, 'User not active. Login Failed')
                return redirect('users:login')
        else:
            messages.add_message(request, messages.ERROR, 'Invaild credentials')
            return redirect('users:login') 
    else:
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Logged out!')
    return redirect('users:login')

@login_required
def interests(request):
    CHOICES = ('Business', 'Entertainment', 'Lifestyle', 'Politics', 'Sports', 'World', 'ScienceAndTechnology', 'India')
    if request.method == 'POST':
        form = request.POST
        choices = dict()
        for key, value in form.items():
            if key in CHOICES:
                choices[key] = value
        if choices:
            choices = json.dumps(choices)
            user_interest, created = UserInterest.objects.get_or_create(user=request.user)
            user_interest.interests = choices
            user_interest.save()
        messages.add_message(request, messages.INFO, 'Interests has been added successfully')
        return redirect('feeds:home')

    return render(request, 'users/interests.html')


@login_required
def profile(request):
    user = request.user
    user_interests = json.loads(UserInterest.objects.get(user=user).interests)
    return render(request, 'users/profile.html', {'user': user, 'interests': user_interests})


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Feedback successfully submitted')
            return redirect('users:feedback')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid input')
            form = FeedbackForm(request.POST)
            pp(form.errors)
        # print(form)
    else:
        form = FeedbackForm()
    return render(request, 'users/feedback.html', {'form': form})
            