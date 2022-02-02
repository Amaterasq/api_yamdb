from audioop import avg
from rest_framework import serializers
from django.db.models import Avg


from reviews.models import Review, Titles, Genre, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Titles

    def get_rating(self, obj):
        list = Review.objects.filter(title_id=obj.id)
        rating = list.aggregate(Avg('score'))
        return int(rating.get('score__avg'))
