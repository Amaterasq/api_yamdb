from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator

import datetime


def current_year():
    return datetime.date.today().year


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


class Genre(models.Model):
    name = models.CharField(max_length=256,
                            unique=True,
                            blank=False,
                            null=False
                            )
    slug = models.SlugField(max_length=50,
                            unique=True,
                            blank=False,
                            null=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256,
                            unique=True,
                            blank=False,
                            null=False)
    slug = models.SlugField(max_length=50,
                            unique=True,
                            blank=False,
                            null=False)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256,
                            blank=False,
                            null=False)
    year = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(current_year())],
        blank=False,
        null=False
    )
    description = models.TextField(null=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='title'
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='title'
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='genre'
    )


class Review(models.Model):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name="reviews")
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews")
    score = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_review')
        ]


class Comment(models.Model):
    review_id = models.ForeignKey('Review',
                                  on_delete=models.CASCADE,
                                  blank=False,
                                  null=False,
                                  related_name="comments")
    text = models.TextField(blank=False,
                            null=False,)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="comments")
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True)

    def __str__(self):
        return self.text[:15]
