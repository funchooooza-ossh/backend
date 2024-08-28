from datetime import datetime
from django import forms
from posts.models import Post, Comment
from django.db import models
from users.models import CustomUser


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        
        fields = ["title", "description", "published"]

# class PostCreateForm(forms.Form):
#     title = forms.CharField()
#     description = forms.TextInput()
#     published = forms.CheckboxInput()
#     author = forms.HiddenInput()
#     create_date = forms.HiddenInput()


class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["description"]
