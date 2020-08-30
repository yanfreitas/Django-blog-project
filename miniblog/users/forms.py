from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profiles


class UserRegisterForm(UserCreationForm):
    """Form that allows the user to register on the site"""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """Form that allows the user update it's account on the site"""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """Form that allows the user update it's profile image"""
    class Meta:
        model = Profiles
        fields = ['image']

