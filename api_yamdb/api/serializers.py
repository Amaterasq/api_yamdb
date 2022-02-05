from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from django.db.models import Avg

from reviews.models import Review, Title, Genre, Category, Comment
from reviews.models import User


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)


class CheckCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        model = User


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        exclude = ('title_id',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title_id', 'author'],
                message='Отзыв на публикацию уже есть!'
            )
        ]


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
        model = Title

    def get_rating(self, obj):
        list = Review.objects.filter(title_id=obj.id)
        rating = list.aggregate(Avg('score'))
        return int(rating.get('score__avg'))
