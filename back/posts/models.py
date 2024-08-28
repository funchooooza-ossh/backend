from typing import Any
from django.db import models
from users.models import CustomUser
from datetime import datetime


class Post(models.Model):

    id = models.PositiveIntegerField(
        primary_key=True
        )

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=False,
        blank=True,
        verbose_name='Author'
        )
    title = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name='Title'
    )
    description = models.TextField(
        max_length=150,
        null=False,
        blank=False,
        verbose_name='Desription'
    )
    create_date = models.DateTimeField(
        auto_now_add=True
    )
    published = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.title
    

class Comment(models.Model):

    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE,
        null=False,
        blank=False
        )
    description = models.TextField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name='Comment text'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Comment date',
        
    )
    author = models.ForeignKey(
        CustomUser,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.description[:20]
    


