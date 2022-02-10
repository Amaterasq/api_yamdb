from rest_framework import serializers

from django.db.models import Avg
from datetime import date

from reviews.models import Review, Title, Genre, Category, Comment, User


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Нельзя выбрать такое имя")
        return value


class CheckCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        model = User


class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        model = User
        read_only_fields = ("role", )


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
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )
    score = serializers.IntegerField(max_value=10, min_value=0)

    def validate(self, data):
        """
        Проверка на существование отзыва.
        """
        title = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        if self.context['request'].method == 'POST':
            if Review.objects.filter(title=title, author=user).exists():
                raise serializers.ValidationError('Вы уже оставляли отзыв!')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title
        read_only_fields = ('category', 'genre', 'rating',)

    def get_rating(self, obj):
        """
        Считаем рэйтинг произведения.
        """
        list = Review.objects.filter(title_id=obj.id)
        rating = list.aggregate(Avg('score'))
        return rating.get('score__avg')


class TitleCreateSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=True
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=True
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        """
        Проверяем год выпуска композиции.
        """
        year_today = date.today().year
        if year_today < value:
            raise serializers.ValidationError(
                f'Год выпуска не может быть больше {year_today} г.'
            )
        return value
