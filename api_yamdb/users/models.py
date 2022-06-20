from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **other_fields):
        user = self.model(email=email, password=password, **other_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **other_fields):
        user = self.model(email=email, password=password, **other_fields)
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator',),
        ('admin', 'admin'),
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
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
        verbose_name='Код подтверждения'
    )
    objects = UserManager()

    def __str__(self):
        return self.username
