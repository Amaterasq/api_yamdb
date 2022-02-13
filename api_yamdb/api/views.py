import uuid
from rest_framework import viewsets, status, filters, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework import permissions

from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from api.serializers import (
    SendCodeSerializer,
    CheckCodeSerializer,
    UserSerializer,
    GenreSerializer,
    TitleSerializer,
    TitleCreateSerializer,
    ReviewSerializer,
    CommentsSerializer,
    CategorySerializer
)
from api.permissions import (
    IsAdmin, IsAdminOrReadOnly, IsAuthorOrAdminOrModeratorOrReadOnly
)
from api.filters import TitlesFilter
from reviews.models import Category, Genre, Title, Review, User
from api_yamdb.settings import YAMBD_EMAIL


@api_view(['POST'])
def send_confirmation_code(request):
    '''
    Генерирует код, привязывает его к юзеру и
    отправляет его на почту пользователя.
    Код доступен в корне в папке sent_emails
    '''
    serializer = SendCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    if not User.objects.filter(username=username, email=email).exists():
        if (
            User.objects.filter(username=username).exists()
            or User.objects.filter(email=email).exists()
        ):
            return Response(
                {"result": "Этот email или username уже используются."},
                status=status.HTTP_400_BAD_REQUEST
            )
        User.objects.create_user(username=username, email=email)
    user = User.objects.get(username=username)
    user.confirmation_code = uuid.uuid4()
    user.save()
    send_mail(
        'Подтверждение аккаунта на Yamdb',
        f'Код подтверждения: {user.confirmation_code}',
        YAMBD_EMAIL,
        [email],
        fail_silently=True,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    '''
    Достает введеный код и сверяет с присвоенным юзеру.
    Возвращает токен для авторизации.
    '''
    serializer = CheckCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if confirmation_code == user.confirmation_code:
        token = AccessToken.for_user(user)
        return Response(
            {'token': f'{token}'},
            status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
    )


class UsersViewSet(viewsets.ModelViewSet):
    '''
    Получение всех юзеров от имени админа.
    Создание/изменение/удаление/получение юзера по
    username вроде должно работать.
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]


class UserDetailPach(APIView):
    '''
    Работа с эндпоинтом <users/me/>.
    Получение и изменение детальной информации о себе.
    '''
    def get(self, request):
        if request.user.is_anonymous:
            return Response(
                'Вы не авторизованы', status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        if request.user.is_anonymous:
            return Response(
                'Вы не авторизованы', status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update',):
            return TitleCreateSerializer
        return TitleSerializer


class PropertyTitleBaseClass(mixins.ListModelMixin,
                             mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class CategoryViewSet(PropertyTitleBaseClass):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GenresViewSet(PropertyTitleBaseClass):

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class CommentsViewSet(viewsets.ModelViewSet):
    """Отбираем только нужные комментарии к отзыву"""
    serializer_class = CommentsSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModeratorOrReadOnly,
    )

    def get_comment(self):
        return get_object_or_404(Review,
                                 id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_comment().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review_id=self.get_comment())


class ReviewViewSet(viewsets.ModelViewSet):
    """Отбираем только нужные отзывы к произведению"""
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModeratorOrReadOnly,
    )

    def get_review(self):
        return get_object_or_404(Title,
                                 id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_review().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_review()
        )
