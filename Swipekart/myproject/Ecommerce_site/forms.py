from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Enter your Email Address'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter your Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter confirm Password'}))


    class Meta:
        model=User
        fields=['username','email','password1','password2']