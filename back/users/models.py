from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    email=models.EmailField(
        verbose_name='Email',
        max_length=250,
        unique=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('-id',)

    def __str__(self):
        return self.username
    
    
    