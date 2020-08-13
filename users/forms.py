from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.utils.translation import gettext_lazy as _
from users.models import User, UserFeedback
 
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'


class UserLoginForm(AuthenticationForm):
    pass


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = UserFeedback
        fields = ('name', 'email', 'first_visit', 'site_return', 'satisfaction', 'article_num', 'suggestion')
        labels = {
            'name': _('Name'),
            'email': _('Email address'),
            'first_visit': _('Is this your first visit?'),
            'site_return': _('How likely are you to return to this site?'),
            'satisfaction': _('How satisfied are you with the site?'),
            'article_num': _('Number of articles you want in your feed'),
            'suggestion': _('Additional changes, comments, feature requests')
        }
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.TextInput(attrs={'class': 'form-control'}),
            'first_visit' : forms.Select(attrs={'class': 'form-select'}),
            'site_return' : forms.Select(attrs={'class': 'form-select'}),
            'satisfaction' : forms.Select(attrs={'class': 'form-select'}),
            'article_num' : forms.NumberInput(attrs={'class': 'form-control'}),
            'suggestion' : forms.Textarea(attrs={'class': 'form-control'})
        }

       
# class UserInterestForm(forms.Form):
#     OPTIONS = (
#         ('GN', 'General'),
#         ('HL', 'Health'),
#         ('BS', 'Business'),
#         ('SP', 'Sports'),
#         ('PL', 'Politics'),
#     )

#     interests = forms.MultipleChoiceField(
#                         widget = forms.CheckboxSelectMultiple,
#                         choices = OPTIONS,
#                 )
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['interests'].widget.attrs['class'] = 'form-check-input'
