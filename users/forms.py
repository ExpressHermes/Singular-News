from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User
 
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
