import uuid
from rest_framework import viewsets, status, filters, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Avg

from api.serializers import (
    SendCodeSerializer,
    CheckCodeSerializer,
    UserSerializer,
    UserSerializer2,
    GenreSerializer,
    TitleCreateSerializer
)
from api.permissions import (
    IsAdmin, IsAdminOrReadOnly, IsAuthorOrAdminOrModerator
)
from api.serializers import (
    TitleSerializer, ReviewSerializer, CommentsSerializer, CategorySerializer
)
from api.filters import TitlesFilter
from reviews.models import Category, Genre, Title, Review, User


@api_view(['POST'])
def send_confirmation_code(request):
    '''
    Генерирует код, привязывает его к юзеру и
    отправляет его на почту пользователя.
    Код доступен в корне в папке sent_emails
    '''
    serializer = SendCodeSerializer(data=request.data)
    email = request.data.get('email', False)
    username = request.data.get('username', False)
    if serializer.is_valid():
        confirmation_code = uuid.uuid4()
        user = User.objects.filter(username=username, email=email).exists()
        if not user:
            if (User.objects.filter(username=username).exists()
                    or User.objects.filter(email=email).exists()):
                return Response(
                    {"result": "Этот email или username уже используются."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            User.objects.create_user(username=username, email=email)
        User.objects.filter(username=username).update(
            confirmation_code=make_password(
                confirmation_code, salt=None, hasher='default'
            )
        )
        send_mail(
            'Подтверждение аккаунта на Yamdb',
            f'Код подтверждения: {confirmation_code}',
            'Yamdb',
            [email],
            fail_silently=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt_token(request):
    '''
    Достает введеный код и сверяет с присвоенным юзеру.
    Возвращает токен для авторизации.
    '''
    serializer = CheckCodeSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if check_password(confirmation_code, user.confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'Неверный код подтверждения'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(
            'Вы не авторизованы', status=status.HTTP_401_UNAUTHORIZED
        )

    def patch(self, request):
        if request.user.is_staff or request.user.role == 'admin':
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        if request.user.is_anonymous:
            return Response(
                'Вы не авторизованы', status=status.HTTP_401_UNAUTHORIZED
            )
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer2(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'create':
            return TitleCreateSerializer
        return TitleSerializer

    def partial_update(self, request, pk=None):
        title = get_object_or_404(Title, pk=pk)
        serializer = TitleCreateSerializer(
            title,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class GenresViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class CommentsViewSet(viewsets.ModelViewSet):
    """Отбираем только нужные комментарии к отзыву"""
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorOrAdminOrModerator,)

    def get_queryset(self):
        review = get_object_or_404(Review,
                                   id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review_id=get_object_or_404(
                Review,
                id=self.kwargs.get('review_id'))
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """Отбираем только нужные отзывы к произведению"""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModerator,
                          )

    def get_queryset(self):
        title = get_object_or_404(Title,
                                  id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title,
                                    id=self.kwargs.get('title_id'))
        )
