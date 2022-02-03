from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    send_confirmation_code,
    get_jwt_token,
    UsersViewSet,
    UserDetailPach
)

router = DefaultRouter()
router.register(r'users', UsersViewSet)

urlpatterns = [
    path('auth/signup/', send_confirmation_code),
    path('auth/token/', get_jwt_token),
    path('users/me/', UserDetailPach.as_view()),
    path('', include(router.urls),),
]
