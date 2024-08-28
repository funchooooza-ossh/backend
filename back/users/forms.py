from datetime import datetime
from django import forms
from posts.models import Post, Comment
from django.db import models
from users.models import CustomUser


class UserCreate(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','password','email']

class UserLogin(forms.Form):
   email = forms.EmailField()
   password = forms.CharField(widget=forms.PasswordInput)