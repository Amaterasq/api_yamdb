import uuid
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password

from users.models import User
from .serializers import (
    SendCodeSerializer,
    CheckCodeSerializer,
    UserSerializer
)
from .permissions import IsAdmin


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
        user = User.objects.filter(username=username).exists()
        if not user:
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
    search_fields = ['user__username', ]


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
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'Вы не авторизованы', status=status.HTTP_401_UNAUTHORIZED
        )
