from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email, is_staff=True, is_superuser=True, **kwargs
        )
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    username = models.TextField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=1000, blank=True)
    confirmation_code = models.CharField(max_length=50, default='1')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    USER_ROLE = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    role = models.CharField(max_length=9, choices=USER_ROLE, default='user')

    objects = CustomUserManager()
