from rest_framework import serializers

from reviews.models import Review, Title, Genre, Category, Comment, User


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Нельзя выбрать такое имя")
        return value


class CheckCodeSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
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
        fields = ('id', 'text', 'author', 'score', 'pub_date')


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
    rating = serializers.IntegerField(default=None, read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category',)
        model = Title
        read_only_fields = ('__all__',)


class TitleCreateSerializer(TitleSerializer):

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
