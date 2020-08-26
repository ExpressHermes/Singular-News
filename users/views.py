from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from .token import account_activation_token
from .forms import SignUpForm, UserLoginForm, FeedbackForm
from .models import User, UserInterest, UserFeedback
import json
from pprint import pprint as pp


def signup(request):
    # if user alreasy logged in, redirect to explore
    if request.user.is_authenticated:
        return redirect('feeds:home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Account activation!'
            message = render_to_string('users/acc_activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return redirect('users:signup_message')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def signup_message(request):
    return render(request, 'users/signup_message.html')


def activate_account(request, uid64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.add_message(request, messages.INFO,
                             'Account activated successfully!')
        return redirect('users:interests')
    else:
        # user.delete()
        messages.add_message(request, messages.ERROR,
                             'Account activation failed. Signup again!')
        return('user:signup')


def user_login(request):
    # if user alreasy logged in, redirect to explore
    if request.user.is_authenticated:
        return redirect('feeds:home')

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
                messages.add_message(
                    request, messages.ERROR, 'User not active. Login Failed')
                return redirect('users:login')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Invaild credentials')
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
    CHOICES = ('Business', 'Entertainment', 'Lifestyle', 'Politics',
               'Sports', 'World', 'ScienceAndTechnology', 'India')
    if request.method == 'POST':
        form = request.POST
        choices = dict()
        for key, value in form.items():
            if key in CHOICES:
                choices[key] = value
        if choices:
            choices = json.dumps(choices)
            user_interest, created = UserInterest.objects.get_or_create(
                user=request.user)
            user_interest.interests = choices
            user_interest.save()
        messages.add_message(request, messages.INFO,
                             'Interests has been added successfully')
        return redirect('feeds:home')

    return render(request, 'users/interests.html')


@login_required
def profile(request):
    user = request.user
    try:
        user_interests = json.loads(
            UserInterest.objects.get(user=user).interests)
    except:
        user_interests = []
    return render(request, 'users/profile.html', {'user': user, 'interests': user_interests})


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,
                                 'Feedback successfully submitted')
            return redirect('users:feedback')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid input')
            form = FeedbackForm(request.POST)
            pp(form.errors)
        # print(form)
    else:
        form = FeedbackForm()
    return render(request, 'users/feedback.html', {'form': form})


def help(request):
    return render(request, 'users/help.html')
