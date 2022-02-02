from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth.models import User


from reviews.models import Titles, Genre, Category


class CategorySerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    category = CategorySerializer()

    class Meta:
        fields = '__all__'
        model = Titles
