from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

import datetime


class User(AbstractUser):
    role = models.CharField(max_length=100,
                            blank=False,
                            null=False
                            )
    bio = models.TextField(
        'Биография',
        blank=True
    )


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


class Titles(models.Model):
    name = models.CharField(max_length=256,
                            blank=False,
                            null=False)
    year = models.IntegerField(
        ('year'),
        validators=[MinValueValidator(0),
                    MaxValueValidator(datetime.date.today().year)],
        blank=False,
        null=False
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_DEFAULT,
        null=True,
        default='Без категории',
        related_name='titles'
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    description = models.CharField(max_length=256,
                                   blank=True,
                                   null=True)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title_id = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='title'
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.SET_DEFAULT,
        null=True,
        default='Без жанра',
        related_name='genre'
    )

    # def __str__(self):
    #     return self.name


class Review(models.Model):
    title_id = models.ForeignKey(
        'Titles',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="reviews")
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="reviews")
    score = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title_id', 'author'],
                                    name='unique_review')
        ]


class Comments(models.Model):
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
        "Дата добавления",
        auto_now_add=True,
        db_index=True)

    def __str__(self):
        return self.text[:15]
