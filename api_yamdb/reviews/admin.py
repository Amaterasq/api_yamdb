from django.contrib import admin

from reviews.models import (
    User, Genre, Category, Title, GenreTitle, Review, Comment
)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category',)
    list_editable = ('category',)
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title_id', 'text', 'author', 'score', 'pub_date',)
    search_fields = ('title_id', 'author', 'pub_date',)
    list_editable = ('title_id',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review_id', 'text', 'author', 'pub_date',)
    search_fields = ('review_id', 'author', 'pub_date',)
    list_editable = ('review_id',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title_id', 'genre_id',)
    search_fields = ('title_id', 'genre_id',)
    list_editable = ('title_id', 'genre_id',)
    list_filter = ('genre_id',)
    empty_value_display = '-пусто-'


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User)
