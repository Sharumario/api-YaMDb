from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator',),
        ('admin', 'admin'),
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=16,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Пользовательская роль'
    )
    confirmation_code = models.CharField(
        max_length=8,
        verbose_name='Код подтверждения',
        blank=True
    )

    def __str__(self):
        return self.username
