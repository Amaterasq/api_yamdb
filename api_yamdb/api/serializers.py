from rest_framework import serializers
from reviews.models import Review, Comments
from rest_framework.validators import UniqueTogetherValidator


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Comments
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        exclude = ('id',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title_id', 'author'],
                message='Отзыв на публикацию уже есть!'
            )
        ]
        fields = '__all__'
